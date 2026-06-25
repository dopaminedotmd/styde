# Blueprint Validation

**Styde Forge v3.0 — Phase 0**
**Section:** 10_Operations

---

## 1. Purpose

Validate that a blueprint is structurally complete and semantically correct
before it can be used to spawn agents. Prevents broken blueprints from
entering the loop.

---

## 2. Validation Rules

```python
def validate_blueprint(blueprint_name: str) -> dict:
    """
    Returns:
        {"valid": True/False, "errors": [...], "warnings": [...]}
    """
    bp_dir = BLUEPRINTS_DIR / blueprint_name
    errors = []
    warnings = []

    # === STRUCTURAL VALIDATION ===

    # Required files
    required_files = ["BLUEPRINT.md", "persona.md", "config.yaml"]
    for f in required_files:
        if not (bp_dir / f).exists():
            errors.append(f"Saknar obligatorisk fil: {f}")

    # Required directories
    required_dirs = ["skills", "versions"]
    for d in required_dirs:
        if not (bp_dir / d).is_dir():
            errors.append(f"Saknar obligatorisk mapp: {d}/")

    # === CONTENT VALIDATION ===

    # BLUEPRINT.md must have Purpose section
    if (bp_dir / "BLUEPRINT.md").exists():
        content = (bp_dir / "BLUEPRINT.md").read_text()
        if "## Purpose" not in content and "## Syfte" not in content:
            errors.append("BLUEPRINT.md saknar Purpose/Syfte-sektion")
        if "## Domain" not in content and "## Domän" not in content:
            warnings.append("BLUEPRINT.md saknar Domain/Domän-sektion")

    # persona.md must be non-empty
    if (bp_dir / "persona.md").exists():
        persona = (bp_dir / "persona.md").read_text()
        if len(persona.strip()) < 50:
            errors.append("persona.md är för kort (< 50 tecken)")

    # config.yaml must parse correctly
    if (bp_dir / "config.yaml").exists():
        try:
            config = load_yaml(bp_dir / "config.yaml")
            # Must have blueprint section
            if "blueprint" not in config:
                errors.append("config.yaml saknar 'blueprint:'-sektion")
            # Must have agent section
            if "agent" not in config:
                warnings.append("config.yaml saknar 'agent:'-sektion")
            # Must have eval section
            if "eval" not in config:
                warnings.append("config.yaml saknar 'eval:'-sektion")
        except Exception as e:
            errors.append(f"config.yaml kan inte parsas: {e}")

    # === SEMANTIC VALIDATION ===

    # At least one benchmark registered
    if "eval" in config:
        benchmarks = config.get("eval", {}).get("benchmarks", [])
        if not benchmarks:
            warnings.append("Inga benchmarks registrerade i eval.benchmarks")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

---

## 3. Validation Gates

| Gate | When | Blocks Spawn? |
|------|------|---------------|
| Structural | On blueprint create | Yes |
| Content | On blueprint edit | Yes |
| Semantic | Before spawn | No (warning only) |
| Full | Before entering loop | Yes |

---

## 4. Integration

- Called automatically by `forge.py blueprint create` after template generation
- Called by `forge.py agent spawn` before spawning
- Called by `forge.py loop` before entering the loop
- Validation results logged to `logs/validation/`

---

**Status:** Defined. Prevents broken blueprints from spawning.
