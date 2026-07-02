"""
Build spawn prompts for Hund persona evaluation.
"""

from .core import load_blueprint, load_benchmark


def build_spawn_prompt(blueprint_name: str, benchmark_name: str) -> dict:
    """
    Build a deployable spawn prompt for a Hund agent.

    Returns dict ready for use with Hermes delegate_task or manual copy-paste
    to Codex/Claude Code.

    The agent is instructed to respond to each scenario as Hund would,
    and output its responses for evaluation.
    """
    ctx = load_blueprint(blueprint_name)
    benchmark = load_benchmark(benchmark_name)

    persona = ctx.get("persona", "")
    blueprint_md = ctx.get("BLUEPRINT", "")
    config = ctx.get("config", {})

    # Extract agent config
    agent_cfg = config.get("agent", {}) if isinstance(config, dict) else {}
    model = agent_cfg.get("model_override", "deepseek-v4-pro")
    toolsets = agent_cfg.get("toolsets", [])

    # Build the goal
    goal_parts = []

    goal_parts.append("=== DIN IDENTITET ===")
    goal_parts.append(persona)
    goal_parts.append("")
    goal_parts.append("=== DIN UPPGIFT ===")
    goal_parts.append(blueprint_md)
    goal_parts.append("")
    goal_parts.append("=== SCENARIER ===")
    goal_parts.append(benchmark)
    goal_parts.append("")
    goal_parts.append("=== INSTRUKTIONER ===")
    goal_parts.append("Svara pa varje scenario EXAKT som hund skulle svara.")
    goal_parts.append("Numrera dina svar: [S1], [S2], osv.")
    goal_parts.append("Ingen sjalv-evaluering. Bara rena svar.")
    goal_parts.append("Output ska vara ren text — ingen markdown, inga kodblock.")

    goal = "\n".join(goal_parts)

    return {
        "goal": goal,
        "toolsets": toolsets,
        "model_override": model,
    }
