"""
Agent Runner — full agent lifecycle orchestration.

Encapsulates: build -> spawn -> post-process -> eval -> improve.
Used by forge.py cmd_loop and can be called standalone.
"""
from pathlib import Path
from datetime import datetime, timezone

from Core.spawn import build_spawn_prompt
from Core.caveman import is_enabled as caveman_enabled
from Core.markdown_stripper import enforce_plain_text, is_markdown
from Core.hermes_bridge import spawn_agent, run_eval_combined, run_teacher
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
)
from Core.state import load_state, save_state
from Core.circuit_breaker import get_breaker, get_global_breaker

FORGE_ROOT = Path(__file__).resolve().parent.parent


class AgentRunResult:
    """Result of a single agent run cycle."""
    def __init__(self):
        self.blueprint: str = ""
        self.run_id: str = ""
        self.success: bool = False
        self.output_chars: int = 0
        self.markdown_stripped: bool = False
        self.self_eval_score: int | None = None
        self.judge_eval_score: int | None = None
        self.composite_score: int | None = None
        self.passed: bool = False
        self.teacher_diagnosis: str = ""
        self.error: str = ""
        self.duration_seconds: float = 0


def run_agent(
    blueprint_name: str,
    benchmark: str = "",
    task: str = "",
    *,
    model: str | None = None,
    timeout: int = 300,
    run_eval_after: bool = True,
    run_teacher_after: bool = True,
) -> AgentRunResult:
    """
    Run a single agent through the full lifecycle.

    Steps:
    1. Build spawn prompt from blueprint
    2. Execute via Hermes
    3. Post-process output (caveman enforcement)
    4. Self-eval + judge-eval
    5. Teacher analysis + improvement

    Returns AgentRunResult with all scores and metadata.
    """
    result = AgentRunResult()
    result.blueprint = blueprint_name
    start = datetime.now(timezone.utc)

    # Circuit breaker
    breaker = get_breaker(blueprint_name)
    global_breaker = get_global_breaker()
    if not breaker.can_proceed() or not global_breaker.can_proceed():
        result.error = "Circuit breaker open"
        return result

    # 1. Build spawn context
    try:
        spawn = build_spawn_prompt(blueprint_name, benchmark=benchmark, task=task)
    except ValueError as e:
        result.error = str(e)
        breaker.record_failure()
        return result

    result.run_id = spawn["run_id"]
    run_dir = FORGE_ROOT / "StydeAgents" / "refinery" / blueprint_name / "runs" / f"run-{spawn['run_id']}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # 2. Execute agent
    agent_model = model or spawn.get("model_override") or "deepseek-v4-flash"
    agent_result = spawn_agent(
        goal=spawn["goal"],
        context=spawn.get("context", ""),
        model=agent_model,
        toolsets=spawn["toolsets"],
        timeout=timeout,
    )

    if not agent_result["success"]:
        result.error = agent_result.get("stderr", "Unknown error")[:200]
        breaker.record_failure()
        global_breaker.record_failure()
        result.duration_seconds = (datetime.now(timezone.utc) - start).total_seconds()
        return result

    # 3. Post-process
    output_text = agent_result["output"]
    if spawn.get("caveman") and is_markdown(output_text):
        output_text = enforce_plain_text(output_text)
        result.markdown_stripped = True

    (run_dir / "output.md").write_text(output_text, encoding="utf-8")
    result.output_chars = len(output_text)
    result.success = True
    breaker.record_success()
    global_breaker.record_success()

    # Update state
    state = load_state()
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
    })
    save_state(state)

    # 4. Eval
    if not run_eval_after:
        result.duration_seconds = (datetime.now(timezone.utc) - start).total_seconds()
        return result

    try:
        output = load_agent_output(run_dir)
        rubric = load_rubric(benchmark) if benchmark else ""

        self_prompt = build_self_eval_prompt(output, rubric)
        judge_prompt = build_judge_eval_prompt(output, rubric)

        combined = run_eval_combined(self_prompt, judge_prompt, model="deepseek/deepseek-chat", timeout=120)
        self_success = combined["success"] and bool(combined.get("self_output"))
        judge_success = combined["success"] and bool(combined.get("judge_output"))

        if self_success or judge_success:
            self_parsed = parse_eval_yaml(combined.get("self_output", "")) if self_success else None
            judge_parsed = parse_eval_yaml(combined.get("judge_output", "")) if judge_success else None
            if self_parsed and judge_parsed:
                composite = compute_composite(self_parsed, judge_parsed)
                save_eval(run_dir, self_parsed, judge_parsed, composite, blueprint_name, benchmark or "manual")
                result.self_eval_score = self_parsed.get("score", 0)
                result.judge_eval_score = judge_parsed.get("score", 0)
                result.composite_score = composite["composite_score"]
                result.passed = composite["passed"]
                state = load_state()
                state["total_evaluations"] = state.get("total_evaluations", 0) + 1
                save_state(state)
    except Exception as e:
        result.error = f"Eval error: {e}"

    # 5. Teacher
    if not run_teacher_after:
        result.duration_seconds = (datetime.now(timezone.utc) - start).total_seconds()
        return result

    try:
        eval_path = run_dir / "eval.yaml"
        if eval_path.exists():
            import yaml
            eval_data = yaml.safe_load(eval_path.read_text(encoding="utf-8"))
            teacher_prompt = build_teacher_prompt(eval_data, [])
            teacher_result = run_teacher(teacher_prompt, model="deepseek/deepseek-chat", timeout=90)

            if teacher_result["success"]:
                review = parse_teacher_response(teacher_result["output"])
                if review:
                    save_teacher_review(run_dir, review)
                    composite_score = eval_data.get("composite", {}).get("composite_score", 0)
                    apply_improvement(blueprint_name, composite_score, review)
                    result.teacher_diagnosis = review.get("diagnosis", {}).get("weakest_dimension", "")
    except Exception as e:
        if not result.error:
            result.error = f"Teacher error: {e}"

    result.duration_seconds = (datetime.now(timezone.utc) - start).total_seconds()
    return result


def run_agent_batch(
    blueprints: list[str],
    benchmark: str = "",
    *,
    parallel: bool = False,
    max_per_blueprint: int = 1,
) -> list[AgentRunResult]:
    """
    Run multiple agents, optionally with multiple iterations per blueprint.

    Args:
        blueprints: List of blueprint names to run
        benchmark: Benchmark name for all
        parallel: NOT IMPLEMENTED — reserved for future parallel execution
        max_per_blueprint: Iterations per blueprint

    Returns list of AgentRunResult for each run.
    """
    results = []
    for bp in blueprints:
        for i in range(max_per_blueprint):
            r = run_agent(bp, benchmark=benchmark)
            results.append(r)
    return results
