# Human Oversight Points

**Styde Forge v3.0 — Phase 0**
**Section:** 10_Operations

---

## 1. Purpose

Define exactly when and how a human should review, approve, or intervene
in the autonomous forge loop. Full autonomy is the goal — but Phase 0
needs strategic human touchpoints.

---

## 2. Oversight Gates

| Gate | Trigger | Action | Frequency |
|------|---------|--------|-----------|
| **Blueprint creation** | New blueprint added | Human reviews BLUEPRINT.md + persona.md | Per blueprint |
| **First spawn** | First agent from a new blueprint | Human reviews initial output | Once per blueprint |
| **Major version bump** | Version goes from v1.x → v2.0 | Human approves architecture change | Rare |
| **Eval score anomaly** | Score jumps/drops > 15 points | Human investigates cause | As needed |
| **Quality gate fail ×3** | Agent fails eval 3 times | Human decides: fix or scrap | As needed |
| **Budget threshold** | Daily cost > $4 (80% of $5 limit) | Human approves continued spend | Daily |
| **New domain** | Agent in a new domain added | Human reviews first eval | Per domain |
| **Security event** | Sandbox violation, prompt injection | Human investigates immediately | As needed |

---

## 3. Approval Workflow

```python
def check_oversight_needed(event_type: str, context: dict) -> str:
    """
    Returns 'auto', 'notify', or 'require_approval'
    """
    OVERSIGHT_RULES = {
        "blueprint_created":     "notify",
        "first_spawn":           "notify",
        "major_version_bump":    "require_approval",
        "eval_anomaly":          "notify",
        "quality_gate_fail_x3":  "require_approval",
        "budget_80_percent":     "notify",
        "new_domain":            "notify",
        "security_event":        "require_approval",
    }

    action = OVERSIGHT_RULES.get(event_type, "auto")

    if action == "require_approval":
        log_and_pause(f"Oversight required: {event_type}", context)
    elif action == "notify":
        log_and_continue(f"Oversight notification: {event_type}", context)

    return action
```

---

## 4. Human Commands

Quick commands for human oversight:

```
# Approve a pending change
forge approve <blueprint> <version>

# Reject and rollback
forge reject <blueprint> <version>

# Show pending approvals
forge pending

# Override quality gate for special case
forge override <agent_id> --score 85

# Set budget limit
forge budget --daily 10.00
```

---

## 5. Gradual Autonomy

| Phase | Human Role | Automation |
|-------|-----------|------------|
| Phase 0 | Review all blueprints, first spawns, major bumps | Loop runs automatically |
| Phase 1 | Review only anomalies and budget | All routine operations auto |
| Phase 2 | Review only security events | Near-full autonomy |
| Phase 3 | Strategic direction only | Full autonomy |

---

**Status:** Defined. 8 oversight gates, approval workflow, gradual autonomy path.
