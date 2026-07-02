"""
Build evaluation prompts for Hund agent output.
Self-eval + Judge-eval with Hund-specific scoring categories.
"""

from .core import load_blueprint, load_benchmark


def build_self_eval_prompt(agent_output: str, benchmark_name: str) -> str:
    """
    Build a self-evaluation prompt.
    The agent evaluates its OWN output against the benchmark criteria.
    """
    config = load_blueprint("hund-persona").get("config", {})
    eval_cfg = config.get("eval", {}) if isinstance(config, dict) else {}
    categories = eval_cfg.get("categories", [])

    parts = []

    parts.append("=== SJALV-EVALUERING ===")
    parts.append("Du har precis svarat pa scenarier som Hund.")
    parts.append("Utvardera dina egna svar arligt och kritiskt.")
    parts.append("")
    parts.append("=== DINA SVAR ===")
    parts.append(agent_output[-4000:])  # Last 4000 chars
    parts.append("")
    parts.append("=== BEDOMNINGSKRITERIER ===")

    for cat in categories:
        parts.append(f"- {cat}")

    parts.append("")
    parts.append("=== FORMAT ===")
    parts.append("Svara som YAML:")
    parts.append("```yaml")
    parts.append("evaluation:")
    for cat in categories:
        parts.append(f"  {cat}:")
        parts.append(f"    score: <0-100>")
        parts.append(f"    evidence: <specifikt citat eller observation>")

    parts.append("  overall:")
    parts.append("    score: <0-100>")
    parts.append("    passed: <true/false>")
    parts.append("    summary: <kort sammanfattning>")
    parts.append("```")

    return "\n".join(parts)


def build_judge_eval_prompt(agent_output: str, benchmark_name: str) -> str:
    """
    Build a judge evaluation prompt.
    Independent judge evaluates the agent's output.
    Uses stricter criteria — world-class standard.
    """
    benchmark = load_benchmark(benchmark_name)
    config = load_blueprint("hund-persona").get("config", {})
    eval_cfg = config.get("eval", {}) if isinstance(config, dict) else {}
    categories = eval_cfg.get("categories", [])
    weights = eval_cfg.get("category_weights", {})
    min_pass = eval_cfg.get("min_pass_score", 85)

    parts = []

    parts.append("=== OBEROENDE BEDOMNING ===")
    parts.append(f"Du ar en domare som utvarderar en AI-agents formaga att halla sig till Hunds persona.")
    parts.append(f"Var strikt. Godkant ar {min_pass}/100. Detta ska vara en agent i VARLDSKLASS.")
    parts.append("")
    parts.append("=== AGENTENS SVAR ===")
    parts.append(agent_output[-4000:])
    parts.append("")
    parts.append("=== BENCHMARK ===")
    parts.append(benchmark[-3000:])
    parts.append("")
    parts.append("=== BEDOMNINGSKRITERIER (viktade) ===")
    for cat in categories:
        w = weights.get(cat, 10)
        parts.append(f"- {cat} (vikt: {w}%)")
    parts.append("")
    parts.append("=== FORMAT ===")
    parts.append("Svara som YAML:")
    parts.append("```yaml")
    parts.append("judge_evaluation:")
    for cat in categories:
        parts.append(f"  {cat}:")
        parts.append(f"    score: <0-100>")
        parts.append(f"    passed: <true/false>")
        parts.append(f"    evidence: <specifikt citat>")
        parts.append(f"    note: <kort kommentar>")
    parts.append("  overall:")
    parts.append("    composite_score: <viktat medelvarde 0-100>")
    parts.append("    passed: <true/false>")
    parts.append("    quality_gate: <true om composite >= 85>")
    parts.append("    world_class: <true om composite >= 92>")
    parts.append("    summary: <1-2 meningar>")
    parts.append("    top_gap: <viktigaste omradet att forbattra>")
    parts.append("```")

    return "\n".join(parts)
