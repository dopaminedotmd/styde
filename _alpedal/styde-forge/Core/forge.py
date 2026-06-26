"""
Styde Forge v3.0 — The Crucible
Main CLI entry point.

Commands: init, status, spawn, eval, improve, checkpoint, recover, loop
"""
import sys
import time
from pathlib import Path

# Ensure forge root is on Python path
FORGE_ROOT = Path(__file__).resolve().parent.parent
if str(FORGE_ROOT) not in sys.path:
    sys.path.insert(0, str(FORGE_ROOT))

import yaml
import json
import subprocess
import hashlib
from datetime import datetime, timezone

from Core.persistence import atomic_write, atomic_write_json
from Core.detect import HardwareAdapter
from Core.state import load_state, save_state, batch_writes
from Core.blueprint import validate_blueprint, load_blueprint_context
from Core.spawn import build_spawn_prompt, run_id_for
from Core.evaluate import (
    load_agent_output,
    load_rubric,
    parse_eval_yaml,
    compute_composite,
    save_eval,
    build_self_eval_prompt,
    build_judge_eval_prompt,
)
from Core.teacher import (
    build_teacher_prompt,
    parse_teacher_response,
    save_teacher_review,
    apply_improvement,
    should_retry,
    determine_stage,
)
from Core.checkpoint import create_checkpoint, list_checkpoints
from Core.recovery import acquire_lock, release_lock, check_and_recover, is_locked
from Core.circuit_breaker import get_breaker, get_global_breaker
from Core.hermes_bridge import spawn_agent, run_eval, run_eval_combined, run_teacher, is_available as hermes_available
from Core.filestore import (
    FileStorageEngine,
    FileCategory,
    get_engine,
)
from Core.caveman import is_enabled as caveman_enabled, toggle as caveman_toggle, status_line as caveman_status
from Core.markdown_stripper import enforce_plain_text, is_markdown


def _state_file() -> Path:
    return FORGE_ROOT / "state.yaml"


# ═══════════════════════════════════════════════════════════════
# INIT
# ═══════════════════════════════════════════════════════════════

def cmd_init():
    """Create USB directory structure and initialize state."""
    print("=== Styde Forge v3.0 — Initializing ===")

    dirs = [
        "StydeAgents/data/benchmarks",
        "StydeAgents/data/knowledge",
        "StydeAgents/data/templates",
        "StydeAgents/refinery",
        "StydeAgents/production",
        "StydeAgents/archive",
        "StydeAgents/blueprints",
        "StydeAgents/blueprints-archive",
        "99_INDEXES",
        "logs",
        "scripts",
    ]
    for d in dirs:
        path = FORGE_ROOT / d
        path.mkdir(parents=True, exist_ok=True)

    print("\n--- Hardware Detection ---")
    try:
        adapter = HardwareAdapter()
        profile = adapter.detect()
        indexes = FORGE_ROOT / "99_INDEXES"
        indexes.mkdir(parents=True, exist_ok=True)
        atomic_write_json(indexes / "hardware_profile.json", profile)
        print(f"  Type: {profile['hardware']['type']}")
        print(f"  VRAM: {profile['hardware']['vram_gb']:.1f} GB")
        print(f"  RAM:  {profile['hardware']['ram_gb']:.1f} GB")
        print(f"  Sampling: {profile['adaptations']['sampling_method']}")
        hw_profile_name = "pontus-main" if profile["hardware"]["type"] == "B" else "pontus-beast"
    except Exception as e:
        print(f"  Warning: Hardware detection failed: {e}")
        profile = None
        hw_profile_name = "pontus-main"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state = {
        "forge_version": "3.0.0",
        "forge_codename": "The Crucible",
        "created": now,
        "last_checkpoint": None,
        "hardware_profile": hw_profile_name,
        "caveman_ultra": True,
        "loop_iterations": 0,
        "total_agents_spawned": 0,
        "total_evaluations": 0,
        "blueprints": [],
        "agents": [],
        "evaluations": [],
        "improvements": [],
    }
    content = yaml.dump(state, default_flow_style=False, allow_unicode=True)
    atomic_write(_state_file(), content)

    manifest = {
        "forge": {
            "version": "3.0.0",
            "codename": "The Crucible",
            "created": now,
            "last_updated": now,
            "sha256": hashlib.sha256(content.encode()).hexdigest()
        },
        "statistics": {
            "total_agents": 0,
            "total_evaluations": 0,
            "total_loop_iterations": 0,
            "storage_used_gb": 0.0,
            "storage_limit_gb": 48.0
        },
        "best_per_domain": {
            "coding": {"agent_id": None, "score": None},
            "research": {"agent_id": None, "score": None},
            "automation": {"agent_id": None, "score": None},
            "documentation": {"agent_id": None, "score": None},
            "testing": {"agent_id": None, "score": None},
            "meta": {"agent_id": None, "score": None}
        },
        "provenance": {
            "generation_chain": ["v3.0_hermes"],
            "hardware_profiles_used": [hw_profile_name]
        }
    }
    atomic_write_json(FORGE_ROOT / "00_MANIFEST.json", manifest)

    print(f"\n=== Forge initialized successfully ===")
    print(f"State: {_state_file()}")
    if profile:
        print(f"Profile: {profile['hardware']['type']} ({profile['hardware']['vram_gb']:.1f} GB VRAM)")


# ═══════════════════════════════════════════════════════════════
# STATUS
# ═══════════════════════════════════════════════════════════════

def cmd_status():
    """Show current forge status."""
    state = load_state()

    print(f"Styde Forge v{state['forge_version']} — {state['forge_codename']}")
    if state.get("hardware_profile"):
        print(f"Hardware: {state['hardware_profile']}")
    print(caveman_status())
    print(f"Loop iterations: {state.get('loop_iterations', 0)}")
    print(f"Total agents spawned: {state.get('total_agents_spawned', 0)}")
    print(f"Total evaluations: {state.get('total_evaluations', 0)}")

    agents = state.get("agents", [])
    refinery = [a for a in agents if a.get("stage") == "refinery"]
    production = [a for a in agents if a.get("stage") == "production"]
    archive = [a for a in agents if a.get("stage") == "archive"]

    print(f"Active blueprints: {len(state.get('blueprints', []))}")
    print(f"Agents in refinery: {len(refinery)}")
    print(f"Agents in production: {len(production)}")
    print(f"Agents archived: {len(archive)}")

    if state.get("last_checkpoint"):
        print(f"Last checkpoint: {state['last_checkpoint']}")
    else:
        print("No checkpoints yet.")


# ═══════════════════════════════════════════════════════════════
# SPAWN
# ═══════════════════════════════════════════════════════════════

def cmd_spawn(blueprint_name: str, benchmark: str = "", task: str = ""):
    """Spawn an agent via Hermes delegate_task."""
    # Circuit breaker check
    breaker = get_breaker(blueprint_name)
    global_breaker = get_global_breaker()

    if not breaker.can_proceed():
        print(f"ERROR: Circuit breaker OPEN for '{blueprint_name}'. Try again later.")
        sys.exit(1)
    if not global_breaker.can_proceed():
        print(f"ERROR: Global circuit breaker OPEN. System cooling down.")
        sys.exit(1)

    print(f"=== Spawning agent: {blueprint_name} ===")

    # Build spawn context
    try:
        spawn = build_spawn_prompt(blueprint_name, benchmark=benchmark, task=task)
    except ValueError as e:
        print(f"ERROR: {e}")
        breaker.record_failure()
        global_breaker.record_failure()
        sys.exit(1)

    print(f"  Run ID: {spawn['run_id']}")
    print(f"  Output: {spawn['output_path']}")
    print(f"  Toolsets: {spawn['toolsets']}")
    if spawn.get("model_override"):
        print(f"  Model: {spawn['model_override']}")
    print(f"  Caveman Ultra: {spawn['caveman']}")
    print()

    # Save spawn context for reference
    context_path = Path(spawn["output_path"]).parent / "spawn_context.yaml"
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_data = {
        "blueprint": blueprint_name,
        "benchmark": benchmark or "manual",
        "task": task or "",
        "run_id": spawn["run_id"],
        "caveman": spawn["caveman"],
        "spawned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    context_path.write_text(
        yaml.dump(context_data, default_flow_style=False, allow_unicode=True),
        encoding="utf-8",
    )

    # Update state
    state = load_state()
    state["total_agents_spawned"] = state.get("total_agents_spawned", 0) + 1
    if blueprint_name not in state.get("blueprints", []):
        state.setdefault("blueprints", []).append(blueprint_name)
    state.setdefault("agents", []).append({
        "blueprint": blueprint_name,
        "run_id": spawn["run_id"],
        "stage": "refinery",
        "spawned_at": context_data["spawned_at"],
        "benchmark": benchmark or "manual",
        "status": "spawned",
    })
    save_state(state)

    breaker.record_success()
    global_breaker.record_success()

    # Execute agent via Hermes
    print(f"  Executing agent via Hermes...")
    model = spawn.get("model_override") or "deepseek-v4-flash"

    result = spawn_agent(
        goal=spawn["goal"],
        context=spawn.get("context", ""),
        model=model,
        toolsets=spawn["toolsets"],
        timeout=300,
    )

    if result["success"]:
        output_text = result["output"]

        # Post-process: skip markdown stripping when caveman is ON
        # (agent was explicitly told NO markdown in caveman rules)
        if not spawn.get("caveman", True) and is_markdown(output_text):
            stripped = enforce_plain_text(output_text)
            reduction = len(output_text) - len(stripped)
            print(f"  Stripped markdown ({reduction} chars removed)")
            output_text = stripped

        output_path = Path(spawn["output_path"])
        output_path.write_text(output_text, encoding="utf-8")
        print(f"  Agent completed. Output saved to: {output_path}")
        print(f"  Output length: {len(output_text)} chars")

        # Update agent status
        for agent in state.get("agents", []):
            if agent.get("run_id") == spawn["run_id"]:
                agent["status"] = "completed"
                break
        save_state(state)
    else:
        print(f"  Agent FAILED: {result['stderr'][:200]}")
        breaker.record_failure()
        global_breaker.record_failure()


# ═══════════════════════════════════════════════════════════════
# EVAL
# ═══════════════════════════════════════════════════════════════

def cmd_eval(blueprint_name: str, run_id: str, benchmark: str = ""):
    """Evaluate agent output from a specific run."""
    print(f"=== Evaluating {blueprint_name} run {run_id} ===")

    run_dir = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{run_id}"

    try:
        output = load_agent_output(run_dir)
    except FileNotFoundError:
        print(f"ERROR: Agent output not found at {run_dir / 'output.md'}")
        print("Has the agent completed its run?")
        sys.exit(1)

    rubric = load_rubric(benchmark) if benchmark else ""
    bench_name = benchmark or "manual"

    print(f"  Output: {len(output)} chars")
    print(f"  Benchmark: {bench_name}")

    # Self-eval prompt
    self_prompt = build_self_eval_prompt(output, rubric)
    self_prompt_path = run_dir / "self_eval_prompt.txt"
    self_prompt_path.write_text(self_prompt, encoding="utf-8")
    print(f"  Self-eval prompt saved to: {self_prompt_path}")

    # Judge-eval prompt
    judge_prompt = build_judge_eval_prompt(output, rubric)
    judge_prompt_path = run_dir / "judge_eval_prompt.txt"
    judge_prompt_path.write_text(judge_prompt, encoding="utf-8")
    print(f"  Judge-eval prompt saved to: {judge_prompt_path}")

    # Run self-eval via Hermes
    print(f"\n  Running self-eval...")
    self_result = run_eval(self_prompt, model="deepseek-v4-flash", timeout=60)
    if self_result["success"]:
        (run_dir / "self_eval_response.txt").write_text(self_result["output"], encoding="utf-8")
        parsed = parse_eval_yaml(self_result["output"])
        print(f"  Self-eval: {parsed.get('score', '?')}/100" if parsed else f"  Self-eval: response saved ({len(self_result['output'])} chars)")
    else:
        print(f"  Self-eval FAILED: {self_result['stderr'][:100]}")

    # Run judge-eval via Hermes
    print(f"  Running judge-eval...")
    judge_result = run_eval(judge_prompt, model="deepseek-v4-flash", timeout=90)
    if judge_result["success"]:
        (run_dir / "judge_eval_response.txt").write_text(judge_result["output"], encoding="utf-8")
        parsed = parse_eval_yaml(judge_result["output"])
        print(f"  Judge-eval: {parsed.get('score', '?')}/100" if parsed else f"  Judge-eval: response saved ({len(judge_result['output'])} chars)")
    else:
        print(f"  Judge-eval FAILED: {judge_result['stderr'][:100]}")

    # Auto-process results
    if self_result["success"] and judge_result["success"]:
        print(f"\n  Auto-processing eval results...")
        cmd_eval_results(blueprint_name, run_id, benchmark)
    else:
        print(f"\n  Manual intervention needed. Run:")
        print(f"  python Core/forge.py eval-results {blueprint_name} {run_id}")


def cmd_eval_results(blueprint_name: str, run_id: str, benchmark: str = ""):
    """Process eval results after manual scoring."""
    print(f"=== Processing eval results for {blueprint_name} run {run_id} ===")

    run_dir = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{run_id}"

    # Look for self-eval response
    self_eval = None
    for fname in ["self_eval_response.txt", "self_eval_result.txt"]:
        fpath = run_dir / fname
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8")
            self_eval = parse_eval_yaml(text)
            if self_eval:
                print(f"  Self-eval: {self_eval.get('score', '?')}/100")
                break

    if not self_eval:
        print("WARNING: No self-eval result found.")
        print(f"Place self-eval response in: {run_dir / 'self_eval_response.txt'}")

    # Look for judge-eval response
    judge_eval = None
    for fname in ["judge_eval_response.txt", "judge_eval_result.txt"]:
        fpath = run_dir / fname
        if fpath.exists():
            text = fpath.read_text(encoding="utf-8")
            judge_eval = parse_eval_yaml(text)
            if judge_eval:
                print(f"  Judge-eval: {judge_eval.get('score', '?')}/100")
                break

    if not judge_eval:
        print("WARNING: No judge-eval result found.")
        print(f"Place judge-eval response in: {run_dir / 'judge_eval_response.txt'}")

    if not self_eval or not judge_eval:
        print("Cannot compute composite without both evals. Exiting.")
        sys.exit(1)

    # Compute composite
    composite = compute_composite(self_eval, judge_eval)
    print(f"  Composite: {composite['composite_score']}/100")
    print(f"  Passed: {composite['passed']}")
    print(f"  Quality gate (>=80): {composite['quality_gate']}")
    print(f"  Production ready (>=85): {composite['production_ready']}")

    # Save eval
    bench_name = benchmark or "manual"
    save_eval(run_dir, self_eval, judge_eval, composite, blueprint_name, bench_name)

    # Update state
    state = load_state()
    state["total_evaluations"] = state.get("total_evaluations", 0) + 1
    state.setdefault("evaluations", []).append({
        "blueprint": blueprint_name,
        "run_id": run_id,
        "composite_score": composite["composite_score"],
        "passed": composite["passed"],
        "benchmark": bench_name,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    save_state(state)

    print(f"  Eval saved to: {run_dir / 'eval.yaml'}")
    print()
    print("To improve the blueprint, run:")
    print(f"  python Core/forge.py improve {blueprint_name} {run_id}")


# ═══════════════════════════════════════════════════════════════
# IMPROVE
# ═══════════════════════════════════════════════════════════════

def cmd_improve(blueprint_name: str, run_id: str):
    """Run teacher agent to analyze eval and propose improvements."""
    print(f"=== Teacher analyzing {blueprint_name} run {run_id} ===")

    run_dir = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{run_id}"
    eval_path = run_dir / "eval.yaml"

    if not eval_path.exists():
        print(f"ERROR: No eval found. Run 'eval-results' first.")
        sys.exit(1)

    eval_data = yaml.safe_load(eval_path.read_text(encoding="utf-8"))
    composite = eval_data.get("composite", {})
    composite_score = composite.get("composite_score", 0)

    print(f"  Composite score: {composite_score}/100")

    # Build teacher prompt
    state = load_state()
    previous_evals = [
        e for e in state.get("evaluations", [])
        if e.get("blueprint") == blueprint_name and e.get("run_id") != run_id
    ]
    teacher_prompt = build_teacher_prompt(eval_data, previous_evals)

    prompt_path = run_dir / "teacher_prompt.txt"
    prompt_path.write_text(teacher_prompt, encoding="utf-8")
    print(f"  Teacher prompt saved to: {prompt_path}")

    # Run teacher via Hermes
    print(f"\n  Running teacher analysis...")
    teacher_result = run_teacher(teacher_prompt, model="deepseek-v4-flash", timeout=90)
    if teacher_result["success"]:
        (run_dir / "teacher_response.txt").write_text(teacher_result["output"], encoding="utf-8")
        print(f"  Teacher response saved ({len(teacher_result['output'])} chars)")

        # Auto-apply improvements
        print(f"\n  Auto-applying improvements...")
        cmd_apply_improvements(blueprint_name, run_id)
    else:
        print(f"  Teacher FAILED: {teacher_result['stderr'][:100]}")
        print(f"  Manual intervention needed. Save response to: {run_dir / 'teacher_response.txt'}")
        print(f"  Then run: python Core/forge.py apply-improvements {blueprint_name} {run_id}")


def cmd_apply_improvements(blueprint_name: str, run_id: str):
    """Apply teacher's proposed improvements."""
    print(f"=== Applying improvements for {blueprint_name} run {run_id} ===")

    run_dir = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{run_id}"
    response_path = run_dir / "teacher_response.txt"

    if not response_path.exists():
        print(f"ERROR: No teacher response found at {response_path}")
        print("Run the teacher prompt first, save response, then run this.")
        sys.exit(1)

    text = response_path.read_text(encoding="utf-8")
    review = parse_teacher_response(text)

    if not review:
        print("WARNING: Could not parse teacher response as YAML.")
        print("Saving raw response anyway.")
        review = {"diagnosis": {"raw_response": text}, "improvements": [], "summary": "Unparseable"}

    # Save review
    save_teacher_review(run_dir, review)

    # Load eval for score
    eval_path = run_dir / "eval.yaml"
    eval_data = yaml.safe_load(eval_path.read_text(encoding="utf-8")) if eval_path.exists() else {}
    composite_score = eval_data.get("composite", {}).get("composite_score", 0)

    # Apply version bump
    new_version = apply_improvement(blueprint_name, composite_score, review)
    print(f"  Diagnosis: {review.get('diagnosis', {}).get('weakest_dimension', 'unknown')}")
    print(f"  Root cause: {review.get('diagnosis', {}).get('root_cause', 'unknown')}")
    print(f"  Summary: {review.get('summary', 'none')}")

    improvements = review.get("improvements", [])
    for i, imp in enumerate(improvements, 1):
        print(f"  Improvement {i}: [{imp.get('target', '?')}] {imp.get('change', '?')}")
        print(f"    Reason: {imp.get('reason', '?')}")
        print(f"    Impact: {imp.get('expected_impact', '?')}")

    if review.get("pattern"):
        p = review["pattern"]
        print(f"  Pattern extracted: {p.get('name', '?')} — {p.get('description', '?')}")

    # Determine stage
    state = load_state()
    recent_evals = [
        e for e in state.get("evaluations", [])
        if e.get("blueprint") == blueprint_name
    ]
    consecutive_passes = 0
    for e in reversed(recent_evals[-10:]):
        if e.get("composite_score", 0) >= 85:
            consecutive_passes += 1
        else:
            break

    stage = determine_stage(composite_score, consecutive_passes)
    print(f"  Blueprint version: {new_version}")
    print(f"  Agent stage: {stage}")

    # Update agent in state
    for agent in state.get("agents", []):
        if agent.get("run_id") == run_id:
            agent["stage"] = stage
            agent["version"] = new_version
            agent["status"] = "improved"
            break

    state.setdefault("improvements", []).append({
        "blueprint": blueprint_name,
        "run_id": run_id,
        "version": new_version,
        "diagnosis": review.get("diagnosis", {}).get("weakest_dimension", ""),
        "summary": review.get("summary", ""),
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    save_state(state)

    # Should retry?
    iteration = len(recent_evals) + 1
    if should_retry(composite_score, iteration, consecutive_passes):
        print(f"\n  Agent needs more work. Retry spawn (iteration {iteration}/10).")
        print(f"  Run: python Core/forge.py spawn {blueprint_name}")
    else:
        print(f"\n  Agent complete after {iteration} iterations.")
        if stage == "production":
            print(f"  PROMOTED TO PRODUCTION.")
        elif stage == "archive":
            print(f"  ARCHIVED — failed quality gate.")
        else:
            print(f"  Max iterations reached — keeping in refinery.")

    print(f"  Review saved to: {run_dir / 'teacher_review.yaml'}")


# ═══════════════════════════════════════════════════════════════
# CHECKPOINT
# ═══════════════════════════════════════════════════════════════

def cmd_checkpoint(label: str = ""):
    """Create atomic checkpoint."""
    print("=== Creating checkpoint ===")

    state = load_state()
    iteration = state.get("loop_iterations", 0) + 1
    state["loop_iterations"] = iteration
    save_state(state)

    checkpoint_id = create_checkpoint(label)
    print(f"Checkpoint created: {checkpoint_id}")
    print(f"Loop iteration: {iteration}")

    checkpoints = list_checkpoints()
    print(f"Total checkpoints: {len(checkpoints)}")


# ═══════════════════════════════════════════════════════════════
# LOOP
# ═══════════════════════════════════════════════════════════════

def cmd_loop(blueprint_name: str, benchmark: str = "", max_iterations: int = 10):
    """Run complete forge loop: spawn -> eval -> improve -> checkpoint. Repeat."""
    print(f"=== Forge Loop: {blueprint_name} ===")
    print(f"Benchmark: {benchmark or 'manual'}")
    print(f"Max iterations: {max_iterations}")
    print()

    _loop_start = time.time()
    _iter_times = []

    # Acquire lock
    if not acquire_lock():
        print("ERROR: Forge is already running. Stop it first.")
        sys.exit(1)

    breaker = get_breaker(blueprint_name)
    global_breaker = get_global_breaker()

    try:
        for i in range(1, max_iterations + 1):
            print(f"--- Iteration {i}/{max_iterations} ---")

            if not breaker.can_proceed():
                print(f"  Circuit breaker OPEN for '{blueprint_name}'. Skipping.")
                continue
            if not global_breaker.can_proceed():
                print(f"  Global circuit breaker OPEN. Cooling down.")
                break

            # Load state once per iteration (batched saves at end)
            state = load_state()

            # 1. SPAWN
            print(f"  Spawning...")
            try:
                spawn = build_spawn_prompt(blueprint_name, benchmark=benchmark)
            except ValueError as e:
                print(f"  ERROR: {e}")
                breaker.record_failure()
                continue

            run_dir = Path(spawn["output_path"]).parent
            run_dir.mkdir(parents=True, exist_ok=True)

            # Execute agent
            model = spawn.get("model_override") or "deepseek-v4-flash"
            result = spawn_agent(
                goal=spawn["goal"],
                context=spawn.get("context", ""),
                model=model,
                toolsets=spawn["toolsets"],
                timeout=300,
            )

            if not result["success"]:
                print(f"  Agent FAILED: {result['stderr'][:200]}")
                breaker.record_failure()
                global_breaker.record_failure()
                continue

            # Post-process: skip markdown stripping when caveman is ON
            # (agent was explicitly told NO markdown in caveman rules)
            output_text = result["output"]
            caveman_on = spawn.get("caveman", True)
            if not caveman_on and is_markdown(output_text):
                stripped = enforce_plain_text(output_text)
                reduction = len(output_text) - len(stripped)
                print(f"  Stripped markdown ({reduction} chars removed)")
                output_text = stripped

            (run_dir / "output.md").write_text(output_text, encoding="utf-8")
            print(f"  Completed: {len(output_text)} chars")

            breaker.record_success()
            global_breaker.record_success()

            # Track spawn in state (deferred save)
            state["total_agents_spawned"] = state.get("total_agents_spawned", 0) + 1
            if blueprint_name not in state.get("blueprints", []):
                state.setdefault("blueprints", []).append(blueprint_name)
            state.setdefault("agents", []).append({
                "blueprint": blueprint_name,
                "run_id": spawn["run_id"],
                "stage": "refinery",
                "spawned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "benchmark": benchmark or "manual",
                "status": "completed",
                "iteration": i,
            })
            state["loop_iterations"] = i

            # 2. EVAL — combined self + judge in ONE call (50% less overhead)
            print(f"  Evaluating (combined)...")
            try:
                output = load_agent_output(run_dir)
                rubric = load_rubric(benchmark) if benchmark else ""

                self_prompt = build_self_eval_prompt(output, rubric)
                judge_prompt = build_judge_eval_prompt(output, rubric)

                combined = run_eval_combined(self_prompt, judge_prompt,
                                             model="deepseek-v4-flash", timeout=120)

                if combined["success"]:
                    self_parsed = parse_eval_yaml(combined["self_output"])
                    judge_parsed = parse_eval_yaml(combined["judge_output"])

                    # Save raw responses for debugging
                    (run_dir / "self_eval_response.txt").write_text(
                        combined["self_output"], encoding="utf-8")
                    (run_dir / "judge_eval_response.txt").write_text(
                        combined["judge_output"], encoding="utf-8")

                    if self_parsed and judge_parsed:
                        composite = compute_composite(self_parsed, judge_parsed)
                        save_eval(run_dir, self_parsed, judge_parsed, composite,
                                  blueprint_name, benchmark or "manual")
                        print(f"  Self: {self_parsed.get('score','?')}/100  "
                              f"Judge: {judge_parsed.get('score','?')}/100  "
                              f"Composite: {composite['composite_score']}/100")
                        state["total_evaluations"] = state.get("total_evaluations", 0) + 1
                    else:
                        print(f"  Eval parse failed. Raw responses saved.")
                        # Fall back to separate calls
                        print(f"  Retrying with separate calls...")
                        self_result = run_eval(self_prompt, model="deepseek-v4-flash", timeout=60)
                        judge_result = run_eval(judge_prompt, model="deepseek-v4-flash", timeout=90)
                        if self_result["success"] and judge_result["success"]:
                            self_parsed = parse_eval_yaml(self_result["output"])
                            judge_parsed = parse_eval_yaml(judge_result["output"])
                            if self_parsed and judge_parsed:
                                composite = compute_composite(self_parsed, judge_parsed)
                                save_eval(run_dir, self_parsed, judge_parsed, composite,
                                          blueprint_name, benchmark or "manual")
                                state["total_evaluations"] = state.get("total_evaluations", 0) + 1
                else:
                    print(f"  Eval FAILED: {combined.get('stderr', '')[:100]}")
                    # Retry with separate calls
                    print(f"  Retrying with separate calls...")
                    self_result = run_eval(self_prompt, model="deepseek-v4-flash", timeout=60)
                    judge_result = run_eval(judge_prompt, model="deepseek-v4-flash", timeout=90)
                    if self_result["success"] and judge_result["success"]:
                        self_parsed = parse_eval_yaml(self_result["output"])
                        judge_parsed = parse_eval_yaml(judge_result["output"])
                        if self_parsed and judge_parsed:
                            composite = compute_composite(self_parsed, judge_parsed)
                            save_eval(run_dir, self_parsed, judge_parsed, composite,
                                      blueprint_name, benchmark or "manual")
                            state["total_evaluations"] = state.get("total_evaluations", 0) + 1
                    else:
                        print(f"  Eval still FAILED. Continuing to next iteration.")
                        continue

            except Exception as e:
                print(f"  Eval ERROR: {e}")
                continue

            # 3. IMPROVE (teacher)
            print(f"  Teacher analyzing...")
            try:
                eval_path = run_dir / "eval.yaml"
                if not eval_path.exists():
                    print(f"  No eval.yaml — skipping teacher.")
                else:
                    eval_data = yaml.safe_load(eval_path.read_text(encoding="utf-8"))
                    teacher_prompt = build_teacher_prompt(eval_data, [])
                    teacher_result = run_teacher(teacher_prompt, model="deepseek-v4-flash", timeout=90)

                    if teacher_result["success"]:
                        review = parse_teacher_response(teacher_result["output"])
                        if review:
                            save_teacher_review(run_dir, review)
                            composite_score = eval_data.get("composite", {}).get("composite_score", 0)
                            apply_improvement(blueprint_name, composite_score, review)
                            print(f"  Diagnosis: {review.get('diagnosis', {}).get('weakest_dimension', '?')}")

                            # Save feedback for next spawn's context
                            _save_blueprint_feedback(blueprint_name, review, composite_score, spawn["run_id"])

                            state.setdefault("improvements", []).append({
                                "blueprint": blueprint_name,
                                "run_id": spawn["run_id"],
                                "diagnosis": review.get("diagnosis", {}).get("weakest_dimension", ""),
                                "summary": review.get("summary", ""),
                                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                            })
                        else:
                            print(f"  Teacher parse failed.")
                    else:
                        print(f"  Teacher FAILED.")
            except Exception as e:
                print(f"  Teacher ERROR: {e}")

            # 4. STAGE TRANSITION
            # After improve, determine if agent should move stages
            eval_data = _safe_load_eval(run_dir)
            if eval_data:
                composite_score = eval_data.get("composite", {}).get("composite_score", 0)
                consecutive = _count_consecutive_passes(state, blueprint_name, composite_score)
                new_stage = determine_stage(composite_score, consecutive)

                # Update last agent entry with correct stage
                if state.get("agents"):
                    state["agents"][-1]["stage"] = new_stage

                if new_stage == "production":
                    _promote_agent(blueprint_name, spawn["run_id"])
                    print(f"  *** PROMOTED TO PRODUCTION *** (score={composite_score}/100, {consecutive} consecutive passes)")
                    save_state(state)
                    break  # Done — agent is production-ready
                elif new_stage == "archive":
                    _archive_agent(blueprint_name, spawn["run_id"])
                    print(f"  Archived (score={composite_score}/100 < 70)")
                    save_state(state)
                    if not should_retry(composite_score, i, consecutive, max_iterations):
                        print(f"  Giving up after {i} attempts.")
                        break

            # SAVE STATE ONCE per iteration (was 3x before)
            save_state(state)

            print()

        # Checkpoint after loop
        print("--- Loop Complete ---")
        cmd_checkpoint(f"loop-{blueprint_name}")

    finally:
        release_lock()


# ── Stage Transition Helpers ──

def _count_consecutive_passes(state: dict, blueprint_name: str, current_score: float) -> int:
    """Count how many consecutive runs (including current) scored >= 85."""
    agents = state.get("agents", [])
    bp_agents = [a for a in agents if a.get("blueprint") == blueprint_name]
    count = 1 if current_score >= 85 else 0
    for a in reversed(bp_agents[:-1]):  # Skip the just-added entry
        run_id = a.get("run_id", "")
        # Check both refinery and production
        for zone in ["refinery", "production"]:
            bp_dir = FORGE_ROOT / "StydeAgents" / zone / blueprint_name / "runs" / f"run-{run_id}"
            eval_path = bp_dir / "eval.yaml"
            if eval_path.exists():
                try:
                    e = yaml.safe_load(eval_path.read_text(encoding="utf-8"))
                    cs = e.get("composite", {}).get("composite_score", 0)
                    if cs >= 85:
                        count += 1
                        break  # Found eval, stop searching zones
                except Exception:
                    pass
        else:
            break  # No eval found for this run — chain is broken
    return count


def _promote_agent(blueprint_name: str, run_id: str):
    """Move agent's run directory from refinery to production.
    Also archives the blueprint definition to StydeAgents/blueprints-archive/."""
    # Move agent run files
    src = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{run_id}"
    dst = FORGE_ROOT / "StydeAgents" / "production" / blueprint_name / "runs" / f"run-{run_id}"
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(src), str(dst))
        try:
            src.parent.rmdir()
            src.parent.parent.rmdir()
        except OSError:
            pass

    # Archive blueprint definition to reduce clutter in blueprints/
    bp_src = FORGE_ROOT / "StydeAgents" / "blueprints" / blueprint_name
    bp_dst = FORGE_ROOT / "StydeAgents" / "blueprints-archive" / blueprint_name
    if bp_src.exists() and not bp_dst.exists():
        bp_dst.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.move(str(bp_src), str(bp_dst))
        print(f"  📦 Blueprint archived: {blueprint_name} → StydeAgents/blueprints-archive/")


def _archive_agent(blueprint_name: str, run_id: str):
    """Move agent's run directory from refinery to archive."""
    src = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{run_id}"
    dst = FORGE_ROOT / "StydeAgents" / "archive" / blueprint_name / "runs" / f"run-{run_id}"
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(src), str(dst))
        try:
            src.parent.rmdir()
            src.parent.parent.rmdir()
        except OSError:
            pass


def _safe_load_eval(run_dir: Path) -> dict | None:
    """Load eval.yaml safely. Returns None if missing or corrupt."""
    ep = Path(run_dir) / "eval.yaml"
    if not ep.exists():
        return None
    try:
        return yaml.safe_load(ep.read_text(encoding="utf-8")) or {}
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
# PARALLEL LOOP
# ═══════════════════════════════════════════════════════════════

def cmd_loop_parallel(
    blueprint_names: list[str],
    benchmark: str = "",
    max_iterations: int = 10,
    max_workers: int = 3,
):
    """Run forge loops for MULTIPLE blueprints in parallel.

    Each blueprint runs in its own thread. State changes are collected
    per-thread and merged once at the end — no race conditions.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    print(f"=== Parallel Forge Loop: {len(blueprint_names)} blueprints ===")
    print(f"Blueprints: {', '.join(blueprint_names)}")
    print(f"Benchmark: {benchmark or 'manual'}")
    print(f"Max iterations per blueprint: {max_iterations}")
    print(f"Max workers: {max_workers}")
    print()
    _loop_start = time.time()

    if not acquire_lock():
        print("ERROR: Forge is already running. Stop it first.")
        sys.exit(1)

    global_breaker = get_global_breaker()

    def _run_one_parallel(bp_name: str) -> dict:
        breaker = get_breaker(bp_name)
        ch = {"agents": [], "improvements": [], "spawns": 0, "evals": 0, "iters": 0, "bps": [bp_name]}
        res = {"blueprint": bp_name, "iterations": 0, "scores": []}

        for i in range(1, max_iterations + 1):
            if not breaker.can_proceed():
                print(f"  [{bp_name}] Breaker OPEN. Skip.")
                continue
            if not global_breaker.can_proceed():
                print(f"  [{bp_name}] Global breaker OPEN.")
                break

            print(f"  [{bp_name}] Iter {i}/{max_iterations}")
            try:
                spawn = build_spawn_prompt(bp_name, benchmark=benchmark)
            except ValueError as e:
                print(f"  [{bp_name}] ERROR: {e}")
                breaker.record_failure()
                continue

            rd = Path(spawn["output_path"]).parent
            rd.mkdir(parents=True, exist_ok=True)
            model = spawn.get("model_override") or "deepseek-v4-flash"
            result = spawn_agent(
                goal=spawn["goal"], context=spawn.get("context", ""),
                model=model, toolsets=spawn["toolsets"], timeout=300,
            )
            if not result["success"]:
                print(f"  [{bp_name}] FAILED: {result['stderr'][:200]}")
                breaker.record_failure(); global_breaker.record_failure()
                continue

            ot = result["output"]
            if not spawn.get("caveman", True) and is_markdown(ot):
                ot = enforce_plain_text(ot)
            (rd / "output.md").write_text(ot, encoding="utf-8")
            print(f"  [{bp_name}] Done: {len(ot)} chars")
            breaker.record_success(); ch["spawns"] += 1

            ch["agents"].append({
                "blueprint": bp_name, "run_id": spawn["run_id"],
                "stage": "refinery",
                "spawned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "benchmark": benchmark or "manual", "status": "completed", "iteration": i,
            })

            # EVAL
            print(f"  [{bp_name}] Eval...")
            try:
                output = load_agent_output(rd)
                rubric = load_rubric(benchmark) if benchmark else ""
                sp = build_self_eval_prompt(output, rubric)
                jp = build_judge_eval_prompt(output, rubric)
                combined = run_eval_combined(sp, jp, model="deepseek-v4-flash", timeout=120)
                if combined["success"]:
                    sparsed = parse_eval_yaml(combined["self_output"])
                    jparsed = parse_eval_yaml(combined["judge_output"])
                    if sparsed and jparsed:
                        composite = compute_composite(sparsed, jparsed)
                        save_eval(rd, sparsed, jparsed, composite, bp_name, benchmark or "manual")
                        res["scores"].append(composite["composite_score"])
                        ch["evals"] += 1
            except Exception as e:
                print(f"  [{bp_name}] Eval err: {e}")
                continue

            # IMPROVE
            print(f"  [{bp_name}] Teacher...")
            try:
                ep = rd / "eval.yaml"
                if ep.exists():
                    ed = yaml.safe_load(ep.read_text(encoding="utf-8"))
                    tp = build_teacher_prompt(ed, [])
                    tr = run_teacher(tp, model="deepseek-v4-flash", timeout=90)
                    if tr["success"]:
                        review = parse_teacher_response(tr["output"])
                        if review:
                            save_teacher_review(rd, review)
                            cs = ed.get("composite", {}).get("composite_score", 0)
                            apply_improvement(bp_name, cs, review)
                            _save_blueprint_feedback(bp_name, review, cs, spawn["run_id"])
                            ch["improvements"].append({
                                "blueprint": bp_name, "run_id": spawn["run_id"],
                                "diagnosis": review.get("diagnosis", {}).get("weakest_dimension", ""),
                                "summary": review.get("summary", ""),
                                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                            })
            except Exception as e:
                print(f"  [{bp_name}] Teacher err: {e}")
            res["iterations"] = i; ch["iters"] = max(ch["iters"], i)

            # 4. STAGE TRANSITION
            eval_data = _safe_load_eval(rd)
            if eval_data and ch["agents"]:
                composite_score = eval_data.get("composite", {}).get("composite_score", 0)
                # Count consecutive from state (load separately — thread-safe read)
                try:
                    s2 = load_state()
                    consecutive = _count_consecutive_passes(s2, bp_name, composite_score)
                except Exception:
                    consecutive = 1 if composite_score >= 85 else 0
                new_stage = determine_stage(composite_score, consecutive)
                ch["agents"][-1]["stage"] = new_stage

                if new_stage == "production":
                    _promote_agent(bp_name, spawn["run_id"])
                    print(f"  [{bp_name}] *** PROMOTED TO PRODUCTION *** (score={composite_score}, {consecutive} passes)")
                    break
                elif new_stage == "archive":
                    _archive_agent(bp_name, spawn["run_id"])
                    print(f"  [{bp_name}] Archived (score={composite_score})")
                    if not should_retry(composite_score, i, consecutive, max_iterations):
                        break

        return {"results": res, "changes": ch}

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(_run_one_parallel, bp): bp for bp in blueprint_names}
            all_res, all_ch = [], []
            for f in as_completed(futures):
                bn = futures[f]
                try:
                    d = f.result(); all_res.append(d["results"]); all_ch.append(d["changes"])
                    r = d["results"]; avg = sum(r["scores"]) / len(r["scores"]) if r["scores"] else 0
                    print(f"  DONE {bn}: {r['iterations']} it, {len(r['scores'])} ev, avg={avg:.0f}")
                except Exception as e:
                    print(f"  FAILED {bn}: {e}")

        state = load_state()
        for sc in all_ch:
            state["total_agents_spawned"] = state.get("total_agents_spawned", 0) + sc["spawns"]
            state["total_evaluations"] = state.get("total_evaluations", 0) + sc["evals"]
            state["loop_iterations"] = max(state.get("loop_iterations", 0), sc["iters"])
            for b in sc["bps"]:
                if b not in state.get("blueprints", []): state.setdefault("blueprints", []).append(b)
            state.setdefault("agents", []).extend(sc["agents"])
            state.setdefault("improvements", []).extend(sc["improvements"])
        save_state(state)

        print("\n=== Parallel Loop Complete ===")
        for r in all_res:
            sc = r["scores"]; avg = sum(sc) / len(sc) if sc else 0; best = max(sc) if sc else 0
            print(f"  {r['blueprint']:25s}  {r['iterations']:2d} it  {len(sc):2d} ev  avg={avg:5.1f}  best={best:5.0f}")
        cmd_checkpoint(f"parallel-loop-{len(blueprint_names)}bp")
    finally:
        release_lock()


def _save_blueprint_feedback(blueprint_name: str, review: dict, score: float, run_id: str):
    """Save teacher feedback to FEEDBACK.md for context injection on next spawn."""
    bp_dir = FORGE_ROOT / "StydeAgents" / "blueprints" / blueprint_name
    bp_dir.mkdir(parents=True, exist_ok=True)
    fp = bp_dir / "FEEDBACK.md"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    diag = review.get("diagnosis", {})
    imps = review.get("improvements", [])
    entry = f"\n---\n## Feedback from {run_id} (score: {score}/100)\n"
    entry += f"**Weakest:** {diag.get('weakest_dimension','?')} | **Cause:** {diag.get('root_cause','?')} | **Severity:** {diag.get('severity','?')}\n"
    entry += f"**Changes:**\n"
    for imp in imps:
        entry += f"- **{imp.get('target','?')}**: {imp.get('change','?')} _(impact: {imp.get('expected_impact','?')})_\n"
    entry += f"**Summary:** {review.get('summary','')}\n"

    existing = fp.read_text(encoding="utf-8") if fp.exists() else ""
    entries = existing.split("\n---\n")
    kept = entries[-9:] if len(entries) > 9 else entries[-5:] if len(entries) > 5 else entries
    fp.write_text("\n---\n".join(kept + [entry]), encoding="utf-8")


def cmd_state_prune(max_per_bp: int = 20):
    """Trim state.yaml: keep only last N entries per blueprint.
    
    Older entries are moved to 'archive_entries' for preservation.
    """
    print(f"=== State Prune: keep {max_per_bp} agents per blueprint ===")
    state = load_state()
    agents = state.get("agents", [])
    from collections import defaultdict
    
    by_bp = defaultdict(list)
    for i, a in enumerate(agents):
        by_bp[a.get("blueprint", "?")].append((i, a))
    
    archived = []
    kept_indices = set()
    pruned = 0
    
    for bp, items in sorted(by_bp.items()):
        # Sort by spawned_at (always a string)
        items.sort(key=lambda x: str(x[1].get("spawned_at", "")))
        if len(items) > max_per_bp:
            # Keep latest N
            keep = items[-max_per_bp:]
            prune = items[:-max_per_bp]
            for idx, a in prune:
                archived.append(a)
                pruned += 1
            for idx, a in keep:
                kept_indices.add(idx)
        else:
            for idx, a in items:
                kept_indices.add(idx)
    
    state["agents"] = [agents[i] for i in sorted(kept_indices)]
    state.setdefault("archive_entries", []).extend(archived)
    
    # Clean up duplicate blueprints list
    unique_bps = sorted(set(a.get("blueprint", "?") for a in state["agents"]))
    state["blueprints"] = unique_bps
    
    save_state(state)
    print(f"Pruned: {pruned} agents archived. State: {len(state['agents'])} entries.")
    print(f"Total archived entries: {len(state.get('archive_entries', []))}")


# ═══════════════════════════════════════════════════════════════
# RECOVER
# ═══════════════════════════════════════════════════════════════

def cmd_recover():
    """Check for crashes and recover if needed."""
    print("=== Recovery Check ===")

    if check_and_recover():
        print("Recovery successful. Forge restored from last valid checkpoint.")
        state = load_state()
        print(f"Current state: {state.get('loop_iterations', 0)} iterations")
        print(f"Last checkpoint: {state.get('last_checkpoint', 'none')}")
    else:
        print("No crash detected. Forge is healthy.")


# ═══════════════════════════════════════════════════════════════
# FILE STORAGE
# ═══════════════════════════════════════════════════════════════

def cmd_storage_status():
    """Show file storage usage across all buckets."""
    from Core.filestore import get_engine
    engine = get_engine()
    usage = engine.get_storage_usage()
    policies = engine.get_lifecycle_policies()

    print("=== File Storage Status ===")
    print(f"Total files: {usage['total_files']}")
    print(f"Total size: {usage['total_size_mb']:.2f} MB ({usage['total_size_gb']:.4f} GB)")
    print()
    for cat, info in usage["buckets"].items():
        pct = (info["size_bytes"] / max(info["max_size_mb"] * 1024 * 1024, 1)) * 100
        print(f"  {cat:12s}  {info['files']:4d} files  {info['size_mb']:8.2f} MB  {pct:5.1f}% of limit")
    print()
    print("Lifecycle Policies:")
    for bucket, policy in policies.items():
        rules = "; ".join(f"{k}={v}d" for k, v in policy["rules"].items())
        print(f"  {bucket:20s}  {rules}")


def cmd_storage_upload():
    """Upload a file directly."""
    if len(sys.argv) < 4:
        print("Usage: forge.py storage upload <filepath> [category]")
        print("Categories: artifact (default), avatar, dataset, knowledge, media, backup, log, temp")
        sys.exit(1)
    filepath = sys.argv[3]
    cat_name = sys.argv[4] if len(sys.argv) > 4 else "artifact"
    try:
        category = FileCategory(cat_name)
    except ValueError:
        print(f"Invalid category: {cat_name}")
        print(f"Valid: {', '.join(c.value for c in FileCategory)}")
        sys.exit(1)

    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    data = path.read_bytes()
    engine = get_engine()
    result = engine.upload_file(data, path.name, category)
    print(f"=== Upload Complete ===")
    print(f"  Bucket: {result['bucket']}")
    print(f"  Key:    {result['key']}")
    print(f"  Size:   {result['size']} bytes")
    print(f"  SHA256: {result['sha256'][:16]}...")


def cmd_storage_list():
    """List files in a category."""
    if len(sys.argv) < 3:
        print("Usage: forge.py storage list <category> [prefix]")
        sys.exit(1)
    cat_name = sys.argv[3]
    prefix = sys.argv[4] if len(sys.argv) > 4 else ""
    try:
        category = FileCategory(cat_name)
    except ValueError:
        print(f"Invalid category: {cat_name}")
        sys.exit(1)

    engine = get_engine()
    files = engine.list_files(category, prefix)
    print(f"=== Files in {category.value} ===")
    if not files:
        print("  (empty)")
    for f in files:
        modified = f["modified"][:19] if f.get("modified") else "?"
        print(f"  {f['key']:60s}  {f['size']:>10,} bytes  {modified}")


def cmd_storage_presigned():
    """Generate a presigned upload URL."""
    if len(sys.argv) < 4:
        print("Usage: forge.py storage presigned <filename> [category] [expires_in]")
        sys.exit(1)
    filename = sys.argv[3]
    cat_name = sys.argv[4] if len(sys.argv) > 4 else "artifact"
    expires = int(sys.argv[5]) if len(sys.argv) > 5 else 3600
    try:
        category = FileCategory(cat_name)
    except ValueError:
        print(f"Invalid category: {cat_name}")
        sys.exit(1)

    engine = get_engine()
    result = engine.request_upload(filename, category, expires)
    print(f"=== Presigned Upload URL ===")
    print(f"  URL:     {result['url']}")
    print(f"  Key:     {result['key']}")
    print(f"  Bucket:  {result['bucket']}")
    print(f"  Expires: {result['expires_at']}")
    print(f"  Max:     {result['max_size_mb']} MB")


def cmd_storage_chunked_start():
    """Start a chunked upload session."""
    if len(sys.argv) < 5:
        print("Usage: forge.py storage chunked-start <filename> <total_size> [category]")
        sys.exit(1)
    filename = sys.argv[3]
    total_size = int(sys.argv[4])
    cat_name = sys.argv[5] if len(sys.argv) > 5 else "artifact"
    try:
        category = FileCategory(cat_name)
    except ValueError:
        print(f"Invalid category: {cat_name}")
        sys.exit(1)

    engine = get_engine()
    result = engine.start_chunked_upload(filename, total_size, category=category)
    print(f"=== Chunked Upload Session ===")
    print(f"  Upload ID:   {result['upload_id']}")
    print(f"  File ID:     {result['file_id']}")
    print(f"  Chunks:      {result['total_chunks']}")
    print(f"  Chunk size:  {result['chunk_size']:,} bytes")
    print(f"  File ID to use for subsequent commands: {result['file_id']}")


def cmd_storage_process():
    """Process an image or video file."""
    if len(sys.argv) < 5:
        print("Usage: forge.py storage process <bucket> <key>")
        sys.exit(1)
    bucket = sys.argv[3]
    key = sys.argv[4]

    engine = get_engine()
    results = engine.auto_process(bucket, key)
    print(f"=== Processing Results ===")
    for r in results:
        if "error" in r:
            print(f"  ERROR: {r['error']}")
        elif "info" in r:
            print(f"  {r['info']}")
        else:
            size_pct = r.get("original_size_pct", "N/A")
            ratio = r.get("compression_ratio", "N/A")
            print(f"  {r['variant']:15s}  {r['key']:50s}  {r['size']:>8,} bytes  {size_pct}%  ratio={ratio}")


def cmd_storage_cdn():
    """Manage CDN distributions."""
    if len(sys.argv) < 4:
        # List distributions
        engine = get_engine()
        dists = engine.list_distributions()
        print(f"=== CDN Distributions ===")
        if not dists:
            print("  No distributions configured.")
        for d in dists:
            print(f"  {d['name']:20s}  {d['domain']:30s}  {d['status']:15s}  {d.get('comment', '')}")
        return

    sub = sys.argv[3]
    if sub == "create" and len(sys.argv) >= 6:
        name = sys.argv[4]
        bucket = sys.argv[5]
        comment = sys.argv[6] if len(sys.argv) > 6 else ""
        engine = get_engine()
        result = engine.create_cdn_distribution(name, bucket, comment)
        print(f"=== CDN Distribution Created ===")
        print(f"  Name:   {result['name']}")
        print(f"  Domain: {result['domain']}")
        print(f"  ID:     {result['id']}")
    elif sub == "invalidate" and len(sys.argv) >= 6:
        name = sys.argv[4]
        paths = sys.argv[5].split(",")
        engine = get_engine()
        result = engine.invalidate_cache(name, paths)
        print(f"=== Cache Invalidation ===")
        print(f"  ID:    {result['id']}")
        print(f"  Paths: {', '.join(result['paths'])}")
        print(f"  Status: {result['status']}")
    else:
        print("Usage:")
        print("  forge.py storage cdn                           List distributions")
        print("  forge.py storage cdn create <name> <bucket>     Create distribution")
        print("  forge.py storage cdn invalidate <name> <paths>  Invalidate cache")


def cmd_storage():
    """Dispatch file storage subcommands."""
    if len(sys.argv) < 3:
        print("Usage: forge.py storage <subcommand> [args]")
        print()
        print("Subcommands:")
        print("  status                          Show storage usage and lifecycle policies")
        print("  upload <filepath> [category]    Upload a file")
        print("  list <category> [prefix]        List files in a category")
        print("  presigned <filename> [cat] [exp] Generate presigned upload URL")
        print("  chunked-start <file> <size> [cat]  Start chunked upload session")
        print("  process <bucket> <key>          Process image/video")
        print("  cdn [create|invalidate] ...     Manage CDN")
        sys.exit(0)

    sub = sys.argv[2]
    commands = {
        "status": cmd_storage_status,
        "upload": cmd_storage_upload,
        "list": cmd_storage_list,
        "presigned": cmd_storage_presigned,
        "chunked-start": cmd_storage_chunked_start,
        "process": cmd_storage_process,
        "cdn": cmd_storage_cdn,
    }
    handler = commands.get(sub)
    if handler:
        handler()
    else:
        print(f"Unknown storage subcommand: {sub}")
        print("Run 'forge.py storage' for help.")
        sys.exit(1)
# ═══════════════════════════════════════════════════════════════

def cmd_config(sub: str = "", value: str = ""):
    """Manage forge configuration. Subcommands: caveman [on|off]"""
    if sub == "caveman":
        if value.lower() in ("on", "true", "1"):
            caveman_toggle(True)
            print("Caveman Ultra: ON")
        elif value.lower() in ("off", "false", "0"):
            caveman_toggle(False)
            print("Caveman Ultra: OFF")
        else:
            print(f"Caveman Ultra: {'ON' if caveman_enabled() else 'OFF'}")
            print("Usage: forge.py config caveman [on|off]")
    else:
        print("Usage: forge.py config caveman [on|off]")


def main():
    if len(sys.argv) < 2:
        print("Styde Forge v3.0 — The Crucible")
        print()
        print("Commands:")
        print("  init                              Create USB directory structure")
        print("  status                            Show forge status")
        print("  config caveman [on|off]           Toggle Caveman Ultra mode")
        print("  spawn <blueprint> [benchmark]     Spawn an agent")
        print("  eval <blueprint> <run_id> [bm]    Create eval prompts")
        print("  eval-results <blueprint> <run_id> Process eval results")
        print("  improve <blueprint> <run_id>      Teacher analysis")
        print("  apply-improvements <bp> <run_id>  Apply teacher improvements")
        print("  checkpoint [label]                Create atomic checkpoint")
        print("  loop <blueprint> [bm] [max]       Full forge loop")
        print("  loop-parallel <b1,b2,...> [bm] [max] [w]  Parallel forge loops")
        print("  recover                           Check and recover from crash")
        print("  staleness <blueprint>              Check blueprint freshness")
        print("  state-prune [max_per_bp]            Trim state.yaml (default: 20/bp)")
        print("  storage <subcommand> [args]       File storage commands")
        print()
        print("Quick start: python Core/forge.py init && python Core/forge.py status")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "init":
        cmd_init()
    elif cmd == "status":
        cmd_status()
    elif cmd == "config":
        sub = sys.argv[2] if len(sys.argv) > 2 else ""
        val = sys.argv[3] if len(sys.argv) > 3 else ""
        cmd_config(sub, val)
    elif cmd == "spawn":
        if len(sys.argv) < 3:
            print("Usage: forge.py spawn <blueprint> [benchmark] [--task <text>]")
            sys.exit(1)
        bp = sys.argv[2]
        bm = ""
        task = ""
        args = sys.argv[3:]
        while args:
            if args[0] == "--task" and len(args) > 1:
                task = args[1]
                args = args[2:]
            elif not args[0].startswith("--"):
                bm = args[0]
                args = args[1:]
            else:
                args = args[1:]
        cmd_spawn(bp, benchmark=bm, task=task)
    elif cmd == "eval":
        if len(sys.argv) < 4:
            print("Usage: forge.py eval <blueprint> <run_id> [benchmark]")
            sys.exit(1)
        bm = sys.argv[4] if len(sys.argv) > 4 else ""
        cmd_eval(sys.argv[2], sys.argv[3], benchmark=bm)
    elif cmd == "eval-results":
        if len(sys.argv) < 4:
            print("Usage: forge.py eval-results <blueprint> <run_id> [benchmark]")
            sys.exit(1)
        bm = sys.argv[4] if len(sys.argv) > 4 else ""
        cmd_eval_results(sys.argv[2], sys.argv[3], benchmark=bm)
    elif cmd == "improve":
        if len(sys.argv) < 4:
            print("Usage: forge.py improve <blueprint> <run_id>")
            sys.exit(1)
        cmd_improve(sys.argv[2], sys.argv[3])
    elif cmd == "apply-improvements":
        if len(sys.argv) < 4:
            print("Usage: forge.py apply-improvements <blueprint> <run_id>")
            sys.exit(1)
        cmd_apply_improvements(sys.argv[2], sys.argv[3])
    elif cmd == "checkpoint":
        label = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_checkpoint(label)
    elif cmd == "loop":
        if len(sys.argv) < 3:
            print("Usage: forge.py loop <blueprint> [benchmark] [max_iterations]")
            sys.exit(1)
        bp = sys.argv[2]
        bm = sys.argv[3] if len(sys.argv) > 3 else ""
        max_iter = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        cmd_loop(bp, benchmark=bm, max_iterations=max_iter)
    elif cmd == "loop-parallel":
        if len(sys.argv) < 3:
            print("Usage: forge.py loop-parallel <bp1,bp2,bp3> [--bm bench] [--max N] [--w N]")
            sys.exit(1)
        bp_list = sys.argv[2].split(",")
        bm = ""
        max_iter = 10
        workers = 3
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--bm" and i + 1 < len(sys.argv):
                bm = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--max" and i + 1 < len(sys.argv):
                max_iter = int(sys.argv[i + 1]); i += 2
            elif sys.argv[i] == "--w" and i + 1 < len(sys.argv):
                workers = int(sys.argv[i + 1]); i += 2
            else:
                i += 1
        cmd_loop_parallel(bp_list, benchmark=bm, max_iterations=max_iter, max_workers=workers)
    elif cmd == "recover":
        cmd_recover()
    elif cmd == "staleness":
        if len(sys.argv) < 3:
            print("Usage: forge.py staleness <blueprint>")
            sys.exit(1)
        from Core.staleness import check_staleness
        result = check_staleness(FORGE_ROOT / "StydeAgents" / "blueprints" / sys.argv[2])
        print("Staleness check:")
        for c in result.get("checks", []):
            status = "OK" if c.get("passed") else "STALE"
            print(f"  [{status}] {c.get('layer','?')}: {c.get('detail','?')}")
        print(f"Recommendation: {result.get('recommendation','?')}")
    elif cmd == "state-prune":
        max_bp = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        cmd_state_prune(max_per_bp=max_bp)
    elif cmd == "storage":
        cmd_storage()
    else:
        print(f"Unknown command: {cmd}")
        print("Run 'python Core/forge.py' for help.")
        sys.exit(1)


if __name__ == "__main__":
    main()
