# Skill Loading Mechanism

**Styde Forge v3.0 — Phase 0**
**Section:** 10_Operations

---

## 1. Purpose

Define exactly how skills from a blueprint are loaded and injected when a
subagent is spawned via Hermes `delegate_task`. This is the bridge between
a blueprint definition and a running agent.

---

## 2. Loading Flow

```
Blueprint (blueprints/<name>/)
  │
  ├── persona.md           → Injected as system context
  ├── BLUEPRINT.md         → Agent's purpose and domain
  ├── config.yaml          → Model selection, hardware profile, eval config
  └── skills/              → Domain-specific Skill files
      ├── SKILL.md
      └── SKILL.md
            │
            ▼
  Parent Hermes reads all skill files
            │
            ▼
  delegate_task(
      goal=task,
      context=persona + blueprint_purpose + skills_content,
      toolsets=config.toolsets
  )
            │
            ▼
  Subagent spawned with full domain context
```

---

## 3. Implementation

```python
def load_blueprint_context(blueprint_name: str) -> dict:
    """Load all context from a blueprint for agent spawning."""
    bp_dir = BLUEPRINTS_DIR / blueprint_name

    # 1. Persona (system context)
    persona = (bp_dir / "persona.md").read_text(encoding="utf-8")

    # 2. Blueprint purpose
    blueprint_md = (bp_dir / "BLUEPRINT.md").read_text(encoding="utf-8")

    # 3. Config
    config = load_yaml(bp_dir / "config.yaml")

    # === BUILD SKILLS CONTEXT ===
    skills_content = ""
    skills_dir = bp_dir / "skills"
    if skills_dir.exists():
        for skill in skills_dir.iterdir():
            skill_file = skill / "SKILL.md" if skill.is_dir() else skill
            if skill_file.exists():
                skills_content += f"\n\n---\n## Skill: {skill.name}\n"
                skills_content += skill_file.read_text(encoding="utf-8")

    # === CAVEMAN ULTRA OVERRIDE ===
    caveman_rules = ""
    if state.get("caveman_ultra", True):
        caveman_rules = """
CAVEMAN ULTRA MODE ACTIVE:
- No markdown. Plain text or YAML only.
- No greetings, no sign-offs, no pleasantries.
- One line per finding. One word if one word is enough.
- Skip explanations unless confidence < 80%.
- If output is code: just the code. No "Here is the code:".
- Output must fit in one terminal screen.
"""

    # 5. Historical context
    history = get_historical_context(blueprint_name)

    # Build spawn context
    spawn_context = f"""
You are a {blueprint_name} agent in the Styde Forge ecosystem.

## Your Purpose
{blueprint_md}

## Your Persona
{persona}

## Your Skills
{skills_content}

## Historical Context
{history}
"""

    return {
        "context": spawn_context,
        "persona": persona,
        "skills": skills_content,
        "config": config,
        "toolsets": config.get("agent", {}).get("toolsets", ["terminal", "file", "web"])
    }
```

---

## 4. Skill Isolation

Each subagent only loads skills from its own blueprint — not all 85+ built-in
Hermes skills. This gives:

- **Cleaner context** — 3-5 domain-specific skills instead of 85
- **Sharper focus** — agent isn't distracted by irrelevant capabilities
- **Better performance** — less context = faster inference
- **Security** — agent can only use skills it was designed for

---

## 5. Dynamic Skill Creation

After evaluation, successful patterns are extracted as new skills:

```python
def extract_skill_from_success(agent_output: str, eval_result: dict) -> str:
    """Extract a reusable skill from a successful agent run."""
    if eval_result["composite_score"] < 85:
        return None  # Only extract from excellent runs

    skill_content = f"""# Skill: Extracted from {eval_result['agent_id']}

**Source:** Agent {eval_result['agent_id']}
**Score:** {eval_result['composite_score']}
**Domain:** {eval_result['domain']}

## Pattern
[Extracted successful pattern from agent output]

## When to Use
[Conditions where this pattern applies]

## Anti-Patterns to Avoid
[What didn't work, learned from eval]
"""
    return skill_content
```

---

## 6. Integration

- Called by `forge.py agent spawn`
- Skills loaded fresh each spawn (no stale cache)
- New skills auto-saved to blueprint's `skills/` directory
- Historical context from Historical Learning System

---

**Status:** Defined. Core spawn mechanism.

---

## Related Documents

- `Blueprint_Validation.md` — Validates blueprint before loading
- `01_Vision/Blueprint_Catalog.md` — All 6 blueprints
- `03_Eval_Pipeline/Benchmark_Catalog.md` — Benchmarks loaded as tasks
- `05_Meta_Layer/Dynamic_Model_Selector.md` — Model choice at spawn
- `05_Meta_Layer/Historical_Learning_System.md` — Historical context injection
