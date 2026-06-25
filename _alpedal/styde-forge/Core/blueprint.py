"""
Blueprint loading and validation.
Loads blueprint context for agent spawning.
"""
import yaml
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "blueprints"

REQUIRED_FILES = ["persona.md", "BLUEPRINT.md", "config.yaml"]


def load_blueprint_context(blueprint_name: str) -> dict:
    """Load all context from a blueprint directory."""
    bp_dir = BLUEPRINTS_DIR / blueprint_name

    if not bp_dir.exists():
        raise FileNotFoundError(f"Blueprint not found: {bp_dir}")

    context = {}

    # Persona
    persona_path = bp_dir / "persona.md"
    context["persona"] = persona_path.read_text(encoding="utf-8") if persona_path.exists() else ""

    # Blueprint
    bp_path = bp_dir / "BLUEPRINT.md"
    context["blueprint_md"] = bp_path.read_text(encoding="utf-8") if bp_path.exists() else ""

    # Config
    config_path = bp_dir / "config.yaml"
    context["config"] = yaml.safe_load(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}

    # Skills
    skills_content = ""
    skills_dir = bp_dir / "skills"
    if skills_dir.exists():
        for skill_file in sorted(skills_dir.glob("*.md")):
            skills_content += f"\n\n---\n## Skill: {skill_file.stem}\n"
            skills_content += skill_file.read_text(encoding="utf-8")
    context["skills"] = skills_content

    # Toolsets
    agent_cfg = context["config"].get("agent", {}) if isinstance(context["config"], dict) else {}
    context["toolsets"] = agent_cfg.get("toolsets", ["terminal", "file", "web"])

    # History
    context["history"] = _load_historical_context(blueprint_name)

    return context


def validate_blueprint(blueprint_name: str) -> list[str]:
    """Validate blueprint. Returns list of error strings (empty = valid)."""
    bp_dir = BLUEPRINTS_DIR / blueprint_name
    errors = []

    if not bp_dir.exists():
        return [f"Blueprint directory not found: {bp_dir}"]

    # Check required files
    for filename in REQUIRED_FILES:
        if not (bp_dir / filename).exists():
            errors.append(f"Missing required file: {filename}")

    # Validate persona
    persona_path = bp_dir / "persona.md"
    if persona_path.exists():
        content = persona_path.read_text(encoding="utf-8").strip()
        if len(content) < 50:
            errors.append(f"persona.md too short ({len(content)} chars, min 50)")

    # Validate BLUEPRINT.md
    bp_path = bp_dir / "BLUEPRINT.md"
    if bp_path.exists():
        content = bp_path.read_text(encoding="utf-8")
        if "## Purpose" not in content and "## purpose" not in content:
            errors.append("BLUEPRINT.md must contain '## Purpose' section")

    # Validate config.yaml
    config_path = bp_dir / "config.yaml"
    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            if not isinstance(config, dict):
                errors.append("config.yaml is not a valid YAML mapping")
            else:
                if "blueprint" not in config:
                    errors.append("config.yaml missing 'blueprint' section")
                else:
                    if "name" not in config["blueprint"]:
                        errors.append("config.yaml missing 'blueprint.name'")
                    if "domain" not in config["blueprint"]:
                        errors.append("config.yaml missing 'blueprint.domain'")
        except yaml.YAMLError as e:
            errors.append(f"config.yaml parse error: {e}")

    # Validate skills
    skills_dir = bp_dir / "skills"
    if skills_dir.exists():
        md_files = list(skills_dir.glob("*.md"))
        if not md_files:
            errors.append("skills/ directory exists but contains no .md files")

    return errors


def _load_historical_context(blueprint_name: str, max_evals: int = 3) -> str:
    """Load last N eval results for historical context."""
    try:
        from Core.state import load_state
        state = load_state()
    except (FileNotFoundError, ImportError):
        return ""

    evals = [e for e in state.get("evaluations", []) if e.get("blueprint") == blueprint_name]
    if not evals:
        return ""

    recent = evals[-max_evals:]
    lines = ["## Previous Evaluation Results"]
    for i, e in enumerate(recent, 1):
        score = e.get("composite_score", "?")
        passed = "PASSED" if e.get("passed") else "FAILED"
        lines.append(f"{i}. Score: {score} — {passed}")

    return "\n".join(lines)
