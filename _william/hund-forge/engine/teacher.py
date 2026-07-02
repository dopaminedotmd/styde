"""
Teacher module — analyzes eval results and proposes concrete improvements
to Hund's persona, code, or skills.
"""

from .core import load_blueprint, load_state


def build_teacher_prompt(
    agent_output: str,
    self_eval: dict,
    judge_eval: dict,
    blueprint_name: str,
) -> str:
    """
    Build a teacher analysis prompt.
    The teacher reads the agent's output + both evals and proposes
    specific, actionable improvements to Hund's blueprint or code.
    """
    config = load_blueprint(blueprint_name).get("config", {})
    eval_cfg = config.get("eval", {}) if isinstance(config, dict) else {}

    composite = judge_eval.get("overall", {}).get("composite_score", 0)
    passed = judge_eval.get("overall", {}).get("passed", False)
    top_gap = judge_eval.get("overall", {}).get("top_gap", "unknown")
    world_class = judge_eval.get("overall", {}).get("world_class", False)

    parts = []

    parts.append("=== LARARE — FORBATTRINGSANALYS ===")
    parts.append(f"Du analyserar en Hund-agent som fick {composite}/100 poang.")
    parts.append(f"Godkant: {passed}. Varldsklass: {world_class}.")
    parts.append(f"Huvudsakligt gap: {top_gap}")
    parts.append("")
    parts.append("Din uppgift: foresla KONKRETA forbattringar som gor Hund battre.")
    parts.append("")
    parts.append("=== AGENTENS SVAR ===")
    parts.append(agent_output[-3000:])
    parts.append("")
    parts.append("=== SJALV-EVAL ===")
    parts.append(format_eval_for_teacher(self_eval))
    parts.append("")
    parts.append("=== DOMAR-EVAL ===")
    parts.append(format_eval_for_teacher(judge_eval))
    parts.append("")
    parts.append("=== FORMAT ===")
    parts.append("Svara som YAML med KONKRETA atgarder:")
    parts.append("```yaml")
    parts.append("teacher_analysis:")
    parts.append("  diagnosis: <1-2 meningar — vad ar grundproblemet?>")
    parts.append("  improvements:")
    parts.append("    - target: <persona.md | BLUEPRINT.md | config.yaml | code | skill>")
    parts.append("      priority: <critical | high | medium | low>")
    parts.append("      change: <exakt vad som ska andras>")
    parts.append("      reason: <varfor — koppla till specifik eval-svaghet>")
    parts.append("      expected_impact: <uppskattad poangforbattring>")
    parts.append("  retry_recommended: <true/false>")
    parts.append("  retry_reason: <om true — vad har forandrats som motiverar nytt forsok?>")
    parts.append("```")

    return "\n".join(parts)


def format_eval_for_teacher(eval_data: dict) -> str:
    """Format an eval dict for teacher consumption."""
    if not eval_data:
        return "(ingen data)"

    lines = []
    for key, value in eval_data.items():
        if key == "overall":
            continue
        if isinstance(value, dict):
            score = value.get("score", "?")
            evidence = value.get("evidence", "")
            note = value.get("note", "")
            lines.append(f"  {key}: {score}/100")
            if evidence:
                lines.append(f"    belagg: {evidence}")
            if note:
                lines.append(f"    not: {note}")

    overall = eval_data.get("overall", {})
    if overall:
        score = overall.get("score", overall.get("composite_score", "?"))
        lines.append(f"  total: {score}/100")

    return "\n".join(lines)
