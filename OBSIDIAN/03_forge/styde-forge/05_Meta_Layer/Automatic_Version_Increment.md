# Automatic Version Increment

**Styde Forge v3.0 — Phase 0**
**Section:** 05_Meta_Layer

---

## 1. Purpose

Automatically determine correct version numbers (MAJOR.MINOR.PATCH) for
blueprint updates based on eval deltas, architecture changes, and domain
trends. Manual versioning doesn't scale past 100+ versions per week.

---

## 2. Semantic Versioning Rules

```
MAJOR.MINOR.PATCH  (e.g., 2.4.1)

MAJOR: Architecture redesign, domain shift, or >0.15 eval delta + arch change
MINOR: Significant improvement (>0.10 delta) or new capability
PATCH: Small improvement, bug fix, or version bump for tracking
```

---

## 3. Decision Matrix

```python
def determine_version(old_version: str, eval_delta: float,
                      architecture_change: bool, domain_trend: float) -> str:
    major, minor, patch = map(int, old_version.split("."))

    # MAJOR: Architecture changed + big improvement
    if architecture_change and eval_delta > 0.15:
        return f"{major + 1}.0.0"

    # MINOR: Significant improvement
    elif eval_delta > 0.10:
        return f"{major}.{minor + 1}.0"

    # MINOR: Moderate improvement with positive trend
    elif eval_delta > 0.03 and domain_trend > 0:
        return f"{major}.{minor + 1}.0"

    # PATCH: Small improvement or flat
    elif eval_delta > 0.0:
        return f"{major}.{minor}.{patch + 1}"

    # PATCH: Even if no improvement (version tracking)
    else:
        return f"{major}.{minor}.{patch + 1}"

    # No bump if eval went DOWN (agent rejected, not saved)
```

---

## 4. Full Decision Table

| Eval Delta | Architecture Change | Domain Trend | Result | Example |
|------------|-------------------|--------------|--------|---------|
| +0.19 | Yes | Above avg | MAJOR (+1.0.0) | v2.4.1 → v3.0.0 |
| +0.14 | No | Above avg | MINOR (+0.1.0) | v2.4.1 → v2.5.0 |
| +0.08 | No | Stable | MINOR (+0.1.0) | v2.4.1 → v2.5.0 |
| +0.04 | No | Stable | PATCH (+0.0.1) | v2.4.1 → v2.4.2 |
| +0.02 | No | Stable | PATCH (+0.0.1) | v2.4.1 → v2.4.2 |
| +0.01 | No | Declining | PATCH (+0.0.1) | v2.4.1 → v2.4.2 |
| -0.05 | — | — | NO BUMP (rejected) | — |

---

## 5. Architecture Change Detection

```python
def detect_architecture_change(old_blueprint: dict, new_blueprint: dict) -> bool:
    """
    Detect if the blueprint underwent architectural changes.

    Signals:
    - Persona significantly rewritten (>30% different)
    - New skills added
    - Skills removed or replaced
    - Config structure changed (new sections)
    """
    signals = 0

    # Persona change
    old_persona = old_blueprint.get("persona", "")
    new_persona = new_blueprint.get("persona", "")
    if text_difference(old_persona, new_persona) > 0.30:
        signals += 1

    # Skill changes
    old_skills = set(old_blueprint.get("skills", []))
    new_skills = set(new_blueprint.get("skills", []))
    if old_skills != new_skills:
        signals += 1

    # Config structure change
    old_keys = set(old_blueprint.get("config", {}).keys())
    new_keys = set(new_blueprint.get("config", {}).keys())
    if old_keys != new_keys:
        signals += 1

    return signals >= 2
```

---

## 6. Version Decision Log

Every version change is logged:

```yaml
version_decision:
  blueprint: "code-reviewer"
  timestamp: "2026-06-25T13:00:00Z"
  old_version: "2.4.1"
  new_version: "3.0.0"
  eval_delta: 0.19
  architecture_change: true
  domain_trend: "above_average"
  decision: "MAJOR"
  reason: "Architecture change + significant eval improvement (+0.19)"
```

---

## 7. Integration

- Called after every successful eval (score ≥ 80)
- Decision logged to `06_IMPROVEMENTS/version_decisions/`
- Version history stored in `07_GENERATIONS/version_history.json`
- Automatic update of `00_MANIFEST.json` with latest versions
- Historical Learning tracks which version bumps correlate with sustained improvement

---

## 8. Blueprint Diff & Changelog

Every version change generates a diff showing exactly what changed:

```yaml
version_diff:
  blueprint: "code-reviewer"
  old_version: "2.4.1"
  new_version: "3.0.0"
  timestamp: "2026-06-25T13:00:00Z"
  eval_delta: 0.19

  changes:
    persona:
      status: "modified"
      diff_summary: "Added edge case checklist, rewrote review process"
      lines_added: 12
      lines_removed: 3

    skills:
      - name: "sql_injection_detection"
        status: "added"
        reason: "Extracted from agent-code-reviewer-20260625-123000"
      - name: "edge_case_checklist_v1"
        status: "added"
        reason: "Teacher recommendation from cycle 47"

    config:
      status: "unchanged"

  changelog: |
    v3.0.0:
    - Added edge case detection checklist to persona
    - New skill: sql_injection_detection (extracted from agent)
    - New skill: edge_case_checklist_v1 (teacher recommendation)
    - Eval improvement: +0.19 (83 → expected ~87-90)
```

### Rollback Support

```python
def rollback_blueprint(name: str, target_version: str):
    """Restore a blueprint to a previous version."""
    versions_dir = BLUEPRINTS_DIR / name / "versions"
    target_file = versions_dir / f"v{target_version}.yaml"

    if not target_file.exists():
        raise VersionError(f"Version {target_version} not found")

    # Save current as backup
    current = load_blueprint(name)
    save_version(name, current)

    # Restore target
    target = load_yaml(target_file)
    save_blueprint(name, target)

    log(f"Rolled back {name} from {current['version']} to {target_version}")
```

---

**Status:** Implemented. Semantic versioning with 7 decision rules.
