# Blueprint Loading & Validation System

**Styde Forge v3.0**
**Section:** 02_Forge_Spawn
**References:** `Skill_Loading_Mechanism.md`, `Blueprint_Validation.md`, `Blueprint_Catalog.md`, `DECISIONS.md` D10
**Resolves:** GAP-F05

---

## 1. `scripts/blueprint_loader.py`

```python
"""
Blueprint loading system.
Loads blueprint context for agent spawning.
"""
from pathlib import Path
import yaml

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "blueprints"

def load_blueprint_context(blueprint_name: str) -> dict:
    """
    Load all context from a blueprint directory.
    
    Returns dict with:
        persona: str        — Persona content
        blueprint_md: str   — Blueprint purpose/description
        config: dict        — Parsed config.yaml
        skills: str         — Concatenated skill files
        toolsets: list[str] — Tools available to agent
        history: str        — Historical context (last 3 evals)
    """
    bp_dir = BLUEPRINTS_DIR / blueprint_name
    
    if not bp_dir.exists():
        raise FileNotFoundError(f"Blueprint not found: {bp_dir}")
    
    context = {}
    
    # 1. Persona
    persona_path = bp_dir / "persona.md"
    context["persona"] = persona_path.read_text(encoding="utf-8") if persona_path.exists() else ""
    
    # 2. Blueprint
    blueprint_path = bp_dir / "BLUEPRINT.md"
    context["blueprint_md"] = blueprint_path.read_text(encoding="utf-8") if blueprint_path.exists() else ""
    
    # 3. Config
    config_path = bp_dir / "config.yaml"
    context["config"] = yaml.safe_load(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    
    # 4. Skills (per D10: only blueprint skills, not all 85+ built-in)
    skills_content = ""
    skills_dir = bp_dir / "skills"
    if skills_dir.exists():
        for skill_file in sorted(skills_dir.glob("*.md")):
            skills_content += f"\n\n---\n## Skill: {skill_file.stem}\n"
            skills_content += skill_file.read_text(encoding="utf-8")
    context["skills"] = skills_content
    
    # 5. Toolsets
    context["toolsets"] = context["config"].get("agent", {}).get(
        "toolsets", ["terminal", "file", "web"]
    )
    
    # 6. Historical context (last 3 evals from state.yaml)
    context["history"] = _load_historical_context(blueprint_name)
    
    return context


def _load_historical_context(blueprint_name: str, max_evals: int = 3) -> str:
    """Load last N eval results for historical context."""
    from forge import load_state
    
    state = load_state()
    evals = [
        e for e in state.get("evaluations", [])
        if e.get("blueprint") == blueprint_name
    ]
    
    if not evals:
        return ""
    
    recent = evals[-max_evals:]
    lines = ["## Previous Evaluation Results"]
    for i, e in enumerate(recent, 1):
        score = e.get("composite_score", "?")
        passed = "PASSED" if e.get("passed") else "FAILED"
        lines.append(f"{i}. Score: {score} — {passed}")
    
    return "\n".join(lines)
```

## 2. `scripts/blueprint_valid.py`

```python
"""
Blueprint validation.
Checks required files and config schema before spawning.
"""
from pathlib import Path
import yaml

BLUEPRINTS_DIR = Path(__file__).resolve().parent.parent / "blueprints"

REQUIRED_FILES = [
    "persona.md",
    "BLUEPRINT.md",
    "config.yaml",
]

REQUIRED_CONFIG_KEYS = [
    ("blueprint", dict),
    ("blueprint.name", str),
    ("blueprint.domain", str),
    ("hardware_profiles", dict),
    ("agent", dict),
    ("agent.max_iterations", int),
    ("agent.timeout_seconds", int),
    ("eval", dict),
    ("eval.min_pass_score", (int, float)),
]

def validate_blueprint(blueprint_name: str) -> list[str]:
    """
    Validate a blueprint directory.
    Returns list of error strings (empty = valid).
    """
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
    blueprint_path = bp_dir / "BLUEPRINT.md"
    if blueprint_path.exists():
        content = blueprint_path.read_text(encoding="utf-8")
        if "## Purpose" not in content and "## purpose" not in content:
            errors.append("BLUEPRINT.md must contain '## Purpose' section")
    
    # Validate config.yaml
    config_path = bp_dir / "config.yaml"
    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            for key_path, expected_type in REQUIRED_CONFIG_KEYS:
                value = _get_nested(config, key_path)
                if value is None:
                    errors.append(f"config.yaml missing: {key_path}")
                elif not isinstance(value, expected_type):
                    errors.append(
                        f"config.yaml {key_path}: expected {expected_type}, got {type(value).__name__}"
                    )
        except yaml.YAMLError as e:
            errors.append(f"config.yaml parse error: {e}")
    
    # Validate skills directory (optional but must have .md files if exists)
    skills_dir = bp_dir / "skills"
    if skills_dir.exists():
        md_files = list(skills_dir.glob("*.md"))
        if not md_files:
            errors.append("skills/ directory exists but contains no .md files")
    
    return errors


def _get_nested(d: dict, key_path: str):
    """Get nested dict value by dot-separated key path."""
    keys = key_path.split(".")
    current = d
    for k in keys:
        if isinstance(current, dict):
            current = current.get(k)
        else:
            return None
    return current
```

## 3. Blueprint Directory Structure

```
blueprints/<name>/
├── persona.md          # Agent personality (required, min 50 chars)
├── BLUEPRINT.md        # Agent purpose + domain (required, must have ## Purpose)
├── config.yaml         # Configuration (required, validated schema)
├── skills/             # Domain-specific skills (optional)
│   ├── skill_one.md
│   └── skill_two.md
└── README.md           # Human-readable description (optional)
```

## 4. `config.yaml` Template

```yaml
blueprint:
  name: "code-reviewer"
  version: 1
  description: "Reviews code for bugs, security issues, and style violations"
  domain: "coding"

hardware_profiles:
  pontus-main:
    model: "deepseek-v4-flash"
    provider: "deepseek"
    eval_model: "deepseek-v4-pro"
    max_tokens: 8192
    temperature: 0.3

agent:
  max_iterations: 10
  timeout_seconds: 300
  retry_on_failure: true
  toolsets: ["terminal", "file", "web"]

eval:
  benchmarks:
    - "code-review-basic"
    - "code-review-security"
  judge_model: "deepseek-v4-pro"
  min_pass_score: 70
```

---

**Status:** Specification complete. Resolves GAP-F05.
