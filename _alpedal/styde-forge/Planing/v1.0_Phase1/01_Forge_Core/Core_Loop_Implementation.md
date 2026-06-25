# Core Loop Implementation

**Styde Forge v3.0**
**Section:** 01_Forge_Core
**References:** `Core_Loop_Detail.md`, `State_Machines.md`, `Component_Interfaces.md`

---

## 1. Purpose

This is the executable specification for `forge.py` — the main orchestrator that implements the DEFINE → SPAWN → EVALUATE → IMPROVE → CHECKPOINT loop.

Every function signature, every file path, every error case is specified here. Phase 1 code is this document made executable.

---

## 2. File: `scripts/forge.py`

### 2.1 CLI Interface

```bash
# Bootstrap
python scripts/forge.py init                          # Create USB structure + state.yaml

# Single-step commands
python scripts/forge.py spawn <blueprint> <benchmark> # DEFINE + SPAWN
python scripts/forge.py eval <agent_id> <benchmark>   # EVALUATE
python scripts/forge.py improve <blueprint>           # IMPROVE
python scripts/forge.py checkpoint                    # CHECKPOINT

# Full loop
python scripts/forge.py loop <blueprint> <benchmark>  # Full DEFINE→CHECKPOINT
python scripts/forge.py loop-all                      # Loop all active blueprints

# Management
python scripts/forge.py status                        # Show forge state
python scripts/forge.py reset <blueprint>             # Reset blueprint to draft
```

### 2.2 Entry Point

```python
#!/usr/bin/env python3
"""
Styde Forge v3.0 — The Crucible
Portable evolutionary agent refinery.
Phase 1 implementation of Core_Loop_Detail.md.
"""
import sys
import argparse
from pathlib import Path

# Project root (USB drive)
FORGE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = FORGE_ROOT / "scripts"
BLUEPRINTS_DIR = FORGE_ROOT / "blueprints"
AGENTS_DIR = FORGE_ROOT / "StydeAgents"
LOGS_DIR = FORGE_ROOT / "logs"
CHECKPOINTS_DIR = FORGE_ROOT / "09_CHECKPOINTS"
STATE_FILE = FORGE_ROOT / "state.yaml"

def main():
    parser = argparse.ArgumentParser(description="Styde Forge v3.0")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Initialize forge structure")
    
    p = sub.add_parser("spawn", help="Spawn agent from blueprint")
    p.add_argument("blueprint")
    p.add_argument("benchmark")
    
    p = sub.add_parser("eval", help="Evaluate agent")
    p.add_argument("agent_id")
    p.add_argument("benchmark")
    
    p = sub.add_parser("improve", help="Improve blueprint based on evals")
    p.add_argument("blueprint")
    
    sub.add_parser("checkpoint", help="Create checkpoint")
    
    p = sub.add_parser("loop", help="Run complete forge loop")
    p.add_argument("blueprint")
    p.add_argument("benchmark")
    
    sub.add_parser("loop-all", help="Loop all active blueprints")
    sub.add_parser("status", help="Show forge status")

    args = parser.parse_args()
    
    if args.command == "init":
        cmd_init()
    elif args.command == "spawn":
        cmd_spawn(args.blueprint, args.benchmark)
    elif args.command == "eval":
        cmd_eval(args.agent_id, args.benchmark)
    elif args.command == "improve":
        cmd_improve(args.blueprint)
    elif args.command == "checkpoint":
        cmd_checkpoint()
    elif args.command == "loop":
        cmd_loop(args.blueprint, args.benchmark)
    elif args.command == "loop-all":
        cmd_loop_all()
    elif args.command == "status":
        cmd_status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

## 3. Command Implementations

### 3.1 `cmd_init()` — Bootstrap Forge

```python
def cmd_init():
    """Create USB directory structure and initialize state."""
    from persistence import atomic_write, atomic_write_json
    from detect import HardwareAdapter
    
    print("=== Styde Forge v3.0 — Initializing ===")
    
    # 1. Create directory structure
    dirs = [
        "01_KNOWLEDGE",
        "StydeAgents/data/benchmarks",
        "StydeAgents/data/knowledge",
        "StydeAgents/data/templates",
        "StydeAgents/refinery",
        "StydeAgents/production",
        "StydeAgents/archive",
        "03_HOOKS/integrations",
        "03_HOOKS/events",
        "04_SKILLS/modular",
        "04_SKILLS/composable",
        "05_LOOPS/self_improvement/v1",
        "05_LOOPS/self_improvement/v2",
        "05_LOOPS/self_improvement/metrics",
        "06_IMPROVEMENTS/global",
        "06_IMPROVEMENTS/version_decisions",
        "06_IMPROVEMENTS/health_history",
        "06_IMPROVEMENTS/validation_summaries",
        "07_GENERATIONS/archive",
        "08_TEACHER_LOGS",
        "09_CHECKPOINTS",
        "10_IMPORT",
        "99_INDEXES",
        "hardware",
        "logs/loops",
        "logs/agents",
        "logs/errors",
        "logs/security",
        "logs/validation",
        "logs/costs",
        "logs/recovery",
        "blueprints",
        "eval/benchmarks",
        "eval/results",
        "scripts",
    ]
    
    for d in dirs:
        path = FORGE_ROOT / d
        path.mkdir(parents=True, exist_ok=True)
        print(f"  Created: {d}/")
    
    # 2. Detect hardware
    print("\n--- Hardware Detection ---")
    adapter = HardwareAdapter()
    profile = adapter.detect()
    atomic_write_json(FORGE_ROOT / "99_INDEXES/hardware_profile.json", profile)
    print(f"  Type: {profile['type']}")
    print(f"  VRAM: {profile['vram_gb']:.1f} GB")
    print(f"  RAM:  {profile['ram_gb']:.1f} GB")
    print(f"  Sampling: {profile['adaptations']['sampling_method']}")
    
    # 3. Initialize state.yaml
    import yaml
    from datetime import datetime, timezone
    
    state = {
        "forge_version": "3.0.0",
        "forge_codename": "The Crucible",
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "last_checkpoint": None,
        "hardware_profile": "pontus-main" if profile["type"] == "B" else "pontus-beast",
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
    atomic_write(STATE_FILE, content)
    
    # 4. Create manifest
    import hashlib, json
    manifest = {
        "forge": {
            "version": "3.0.0",
            "codename": "The Crucible",
            "created": state["created"],
            "last_updated": state["created"],
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
            "hardware_profiles_used": [state["hardware_profile"]]
        }
    }
    atomic_write_json(FORGE_ROOT / "00_MANIFEST.json", manifest)
    
    print("\n=== Forge initialized successfully ===")
    print(f"State: {STATE_FILE}")
    print(f"Profile: {profile['type']} ({profile['vram_gb']:.1f} GB VRAM)")
```

### 3.2 `cmd_spawn(blueprint, benchmark)` — DEFINE + SPAWN

```python
def cmd_spawn(blueprint_name: str, benchmark_name: str):
    """DEFINE: Load blueprint + SPAWN: delegate_task."""
    from blueprint_loader import load_blueprint_context
    from blueprint_valid import validate_blueprint
    from spawn import spawn_agent
    import yaml
    
    print(f"=== Spawning: {blueprint_name} vs {benchmark_name} ===")
    
    # DEFINE
    # 1. Validate blueprint
    errors = validate_blueprint(blueprint_name)
    if errors:
        print(f"ERROR: Blueprint validation failed:")
        for e in errors:
            print(f"  - {e}")
        return
    
    # 2. Load context
    context = load_blueprint_context(blueprint_name)
    
    # 3. Load benchmark task + rubric
    benchmark_dir = FORGE_ROOT / "eval/benchmarks" / benchmark_name
    task = (benchmark_dir / "task.md").read_text(encoding="utf-8")
    rubric = yaml.safe_load((benchmark_dir / "rubric.yaml").read_text(encoding="utf-8"))
    
    # SPAWN
    # 4. Spawn agent
    result = spawn_agent(
        blueprint=blueprint_name,
        task=task,
        rubric=rubric,
        context=context,
        toolsets=context.get("toolsets", ["terminal", "file", "web"]),
        timeout=300
    )
    
    if result["status"] == "success":
        print(f"  Agent: {result['agent_id']}")
        print(f"  Output: {result['output_path']}")
        print(f"  Duration: {result['duration_ms']}ms")
    else:
        print(f"  FAILED: {result['reason']}")
```

### 3.3 `cmd_eval(agent_id, benchmark)` — EVALUATE

```python
def cmd_eval(agent_id: str, benchmark_name: str):
    """EVALUATE: Self-eval + Judge-eval + Composite score."""
    from eval_runner import run_self_eval, run_judge_eval
    from composite_scorer import calculate_composite
    import yaml
    
    print(f"=== Evaluating: {agent_id} ===")
    
    # Load rubric
    benchmark_dir = FORGE_ROOT / "eval/benchmarks" / benchmark_name
    rubric = yaml.safe_load((benchmark_dir / "rubric.yaml").read_text(encoding="utf-8"))
    
    # Load agent output
    agent_dir = AGENTS_DIR / "refinery" / agent_id
    output = (agent_dir / "runs/latest/output.md").read_text(encoding="utf-8")
    
    # Self-eval
    print("  Self-eval...")
    self_eval = run_self_eval(agent_id, output, rubric)
    print(f"    Score: {self_eval['score']}")
    
    # Judge-eval
    print("  Judge-eval...")
    judge_eval = run_judge_eval(agent_id, output, rubric)
    print(f"    Score: {judge_eval['score']} (model: {judge_eval.get('model', 'unknown')})")
    
    # Composite
    composite = calculate_composite(self_eval, judge_eval)
    passed = composite["score"] >= 70
    status = "PASSED" if passed else "FAILED"
    
    print(f"  Composite: {composite['score']} → {status}")
    
    # Save eval
    eval_data = {
        "run_id": f"run-{agent_id}",
        "agent_id": agent_id,
        "self_eval": self_eval,
        "judge_eval": judge_eval,
        "composite_score": composite["score"],
        "passed": passed,
        "min_pass_score": 70
    }
    
    eval_path = agent_dir / "evals/latest.yaml"
    from persistence import atomic_write
    atomic_write(eval_path, yaml.dump(eval_data, allow_unicode=True))
```

### 3.4 `cmd_improve(blueprint)` — IMPROVE

```python
def cmd_improve(blueprint_name: str):
    """IMPROVE: Teacher analyzes eval, proposes improvements."""
    from teacher import analyze_eval, apply_improvements
    import yaml
    
    print(f"=== Improving: {blueprint_name} ===")
    
    # Find latest agent for this blueprint
    state = load_state()
    agents = [a for a in state.get("agents", []) if a["blueprint"] == blueprint_name]
    if not agents:
        print("  No agents found for this blueprint")
        return
    
    latest = agents[-1]
    agent_dir = AGENTS_DIR / latest["stage"] / latest["name"]
    eval_path = agent_dir / "evals/latest.yaml"
    
    if not eval_path.exists():
        print("  No eval found. Run 'forge.py eval' first.")
        return
    
    eval_data = yaml.safe_load(eval_path.read_text(encoding="utf-8"))
    
    # Teacher analysis
    teacher_review = analyze_eval(latest["name"], blueprint_name, eval_data)
    
    print(f"  Diagnosis: {teacher_review['diagnosis']['primary_weakness']}")
    print(f"  Root cause: {teacher_review['diagnosis']['root_cause']}")
    
    for imp in teacher_review.get("improvements", []):
        print(f"  → {imp['target']}: {imp['change']} [{imp['impact']}]")
    
    # Apply improvements
    if teacher_review["composite_score"] >= 85:
        if latest.get("evals_passed", 0) >= 2:
            # 3 consecutive ≥85 → promote
            print(f"  *** PROMOTING to production! ***")
            apply_improvements(blueprint_name, teacher_review, promote=True)
        else:
            print(f"  Passed ({latest.get('evals_passed', 0)+1}/3 consecutive ≥85)")
            apply_improvements(blueprint_name, teacher_review, promote=False)
    elif teacher_review["composite_score"] >= 70:
        retries = latest.get("retries", 0)
        if retries >= 3:
            print(f"  Max retries ({retries}) → archiving")
            apply_improvements(blueprint_name, teacher_review, promote=False, archive=True)
        else:
            print(f"  Needs work — scheduling retry ({retries+1}/3)")
            apply_improvements(blueprint_name, teacher_review, promote=False, retry=True)
    else:
        print(f"  Failed (<70) → archiving")
        apply_improvements(blueprint_name, teacher_review, promote=False, archive=True)
```

### 3.5 `cmd_checkpoint()` — CHECKPOINT

```python
def cmd_checkpoint():
    """CHECKPOINT: Atomic snapshot of forge state."""
    from checkpoint import create_checkpoint
    
    print("=== Creating checkpoint ===")
    result = create_checkpoint()
    
    if result["success"]:
        print(f"  Checkpoint: {result['checkpoint_id']}")
        print(f"  Size: {result['size_mb']:.1f} MB")
        print(f"  Duration: {result['duration_ms']}ms")
    else:
        print(f"  FAILED: {result['reason']}")
```

### 3.6 `cmd_loop(blueprint, benchmark)` — Full Loop

```python
def cmd_loop(blueprint_name: str, benchmark_name: str):
    """Run one complete forge loop iteration."""
    from circuit_breaker import get_breaker
    
    breaker = get_breaker(blueprint_name)
    
    if not breaker.allow_request():
        print(f"CIRCUIT BREAKER OPEN for {blueprint_name}. Skipping.")
        return
    
    try:
        # Step 1: SPAWN
        cmd_spawn(blueprint_name, benchmark_name)
        
        # Step 2: EVALUATE
        state = load_state()
        agents = [a for a in state["agents"] if a["blueprint"] == blueprint_name]
        if not agents:
            breaker.record_failure()
            return
        agent_id = agents[-1]["name"]
        cmd_eval(agent_id, benchmark_name)
        
        # Step 3: IMPROVE
        cmd_improve(blueprint_name)
        
        # Step 4: CHECKPOINT (every 5 loops)
        state = load_state()
        if state["loop_iterations"] % 5 == 0:
            cmd_checkpoint()
        
        # Success
        breaker.record_success()
        state["loop_iterations"] += 1
        save_state(state)
        
    except Exception as e:
        print(f"Loop error: {e}")
        breaker.record_failure()
        import traceback
        traceback.print_exc()
```

---

## 4. Helper Functions

```python
def load_state() -> dict:
    """Load forge state from state.yaml."""
    import yaml
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}. Run 'forge.py init' first.")
    return yaml.safe_load(STATE_FILE.read_text(encoding="utf-8"))

def save_state(state: dict):
    """Save forge state atomically."""
    import yaml
    from persistence import atomic_write
    content = yaml.dump(state, default_flow_style=False, allow_unicode=True)
    atomic_write(STATE_FILE, content)

def cmd_status():
    """Show current forge status."""
    state = load_state()
    print(f"Styde Forge v{state['forge_version']} — {state['forge_codename']}")
    print(f"Hardware: {state['hardware_profile']}")
    print(f"Caveman Ultra: {'ON' if state.get('caveman_ultra', True) else 'OFF'}")
    print(f"Loop iterations: {state['loop_iterations']}")
    print(f"Total agents spawned: {state['total_agents_spawned']}")
    print(f"Total evaluations: {state['total_evaluations']}")
    print(f"Active blueprints: {len(state['blueprints'])}")
    print(f"Agents in refinery: {len([a for a in state['agents'] if a['stage'] == 'refinery'])}")
    print(f"Agents in production: {len([a for a in state['agents'] if a['stage'] == 'production'])}")
    print(f"Agents archived: {len([a for a in state['agents'] if a['stage'] == 'archive'])}")
    if state['last_checkpoint']:
        print(f"Last checkpoint: {state['last_checkpoint']}")
    else:
        print("No checkpoints yet.")

def cmd_loop_all():
    """Loop all active blueprints."""
    state = load_state()
    active = [b for b in state["blueprints"] if b["status"] in ["draft", "testing"]]
    if not active:
        print("No active blueprints.")
        return
    
    for bp in active:
        benchmarks = load_blueprint_context(bp["name"]).get("eval", {}).get("benchmarks", [])
        if benchmarks:
            cmd_loop(bp["name"], benchmarks[0])
```

---

## 5. Error Handling Contract

Every command must handle these error classes:

| Error | Behavior |
|-------|----------|
| `BlueprintNotFound` | Print error, skip blueprint, do NOT crash |
| `ValidationError` | Print specific validation errors, skip |
| `SpawnTimeout` | Retry once, then mark failed |
| `APIError (429)` | Wait 5s, retry. Max 3 retries |
| `APIError (5xx)` | Wait 10s, retry. Max 2 retries |
| `DiskFull` | Trigger maintenance, pause loop |
| `USBDisconnected` | Emergency save to temp, alert |
| `KeyboardInterrupt` | Graceful shutdown, save state |

---

## 6. Logging

All commands log to `logs/forge.log` in JSON-lines format:

```python
import json, time

def log_event(level: str, component: str, operation: str, **kwargs):
    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "level": level,
        "component": component,
        "operation": operation,
        **kwargs
    }
    with open(FORGE_ROOT / "logs/forge.log", "a") as f:
        f.write(json.dumps(entry) + "\n")
```

---

**Status:** Specification complete. This is the blueprint for `forge.py`.
