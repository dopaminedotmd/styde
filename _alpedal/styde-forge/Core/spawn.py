"""
Subagent spawning via Hermes delegate_task.

Builds complete spawn context from blueprint + benchmark.
Caveman Ultra injected by default. Subagent writes output to output.md.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

from Core.blueprint import load_blueprint_context, validate_blueprint

FORGE_ROOT = Path(__file__).resolve().parent.parent
REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"

CAVEMAN_ULTRA_RULES = """
CAVEMAN ULTRA MODE ACTIVE. Rules:
- No filler words. No "I think", "let me", "let's", "perhaps".
- No markdown. No headings, no bold, no lists, no code fences.
- Plain text only. Short sentences. Direct answers.
- No explanations unless asked.
- No asking clarifying questions — make your best guess and execute.
- Maximum information density per token.
- Output pure result. Skip the wrapping paper.
"""


def build_spawn_prompt(
    blueprint_name: str,
    benchmark: str = "",
    task: str = "",
    caveman: bool = True,
) -> dict:
    """
    Build complete delegate_task spawn context.

    Returns dict ready for delegate_task():
        {goal, context, toolsets, model_override}

    The subagent is instructed to write output to:
        StydeAgents/refinery/{blueprint_name}/runs/{run_id}/output.md
    """
    errors = validate_blueprint(blueprint_name)
    if errors:
        raise ValueError(f"Blueprint validation failed: {'; '.join(errors)}")

    ctx = load_blueprint_context(blueprint_name)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    output_path = REFINERY_DIR / blueprint_name / "runs" / f"run-{run_id}" / "output.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Build goal
    goal_parts = []
    goal_parts.append(f"## PERSONA\n{ctx['persona']}")
    goal_parts.append(f"## BLUEPRINT\n{ctx['blueprint_md']}")

    if task:
        goal_parts.append(f"## TASK\n{task}")
    elif benchmark:
        benchmark_task = _load_benchmark_task(benchmark)
        goal_parts.append(f"## TASK\n{benchmark_task}")

    goal_parts.append(f"\n## INSTRUCTIONS")
    goal_parts.append("Complete the task above. Output your result directly in your response.")
    goal_parts.append("Do NOT use write_file. Just respond with your answer.")

    if caveman:
        goal_parts.insert(0, CAVEMAN_ULTRA_RULES)

    goal = "\n\n".join(goal_parts)

    # Build context string (skills, history) for hermes_bridge
    context_parts = []
    if ctx.get("skills"):
        context_parts.append(f"## LOADED SKILLS\n{ctx['skills']}")
    if ctx.get("history"):
        context_parts.append(ctx["history"])
    context = "\n\n".join(context_parts) if context_parts else ""

    # Toolsets from config
    toolsets = ctx.get("toolsets", ["terminal", "file", "web"])

    # Model from config
    agent_cfg = ctx.get("config", {}).get("agent", {}) if isinstance(ctx.get("config"), dict) else {}
    model_override = agent_cfg.get("model_override")

    return {
        "goal": goal,
        "context": context,
        "toolsets": toolsets,
        "model_override": model_override,
        "run_id": run_id,
        "output_path": str(output_path),
        "blueprint": blueprint_name,
        "benchmark": benchmark or "manual",
        "caveman": caveman,
    }


def run_id_for(blueprint_name: str) -> str:
    """Generate a new run ID for a blueprint (does not create directories)."""
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


# --- internals ---

def _load_benchmark_task(benchmark_name: str) -> str:
    """Load task description from benchmark directory."""
    bench_dir = FORGE_ROOT / "eval" / "benchmarks" / benchmark_name
    if not bench_dir.exists():
        return f"Complete the task for benchmark: {benchmark_name}"

    task_file = bench_dir / "task.md"
    if task_file.exists():
        return task_file.read_text(encoding="utf-8")

    # Fallback: build from golden cases
    golden = bench_dir / "golden"
    if golden.exists():
        cases = sorted(golden.glob("case-*"))
        if cases:
            lines = [f"Complete the {benchmark_name} task."]
            for case in cases:
                input_file = case / "input.py"
                if input_file.exists():
                    code = input_file.read_text(encoding="utf-8")
                    lines.append(f"\n## Input ({case.name})\n```python\n{code}\n```")
            return "\n".join(lines)

    return f"Complete the task for benchmark: {benchmark_name}"
