# Skill Extraction System

**Styde Forge v3.0**
**Section:** 04_Forge_Improve
**References:** `Skill_Loading_Mechanism.md` §5, `Teacher_Agent.md` §5

---

## 1. Purpose

Extract successful patterns from high-scoring agent runs (≥85) into reusable SKILL.md files. These skills get loaded in future spawns — agents get smarter over time.

---

## 2. Implementation

```python
# Core/skills.py

def extract_skill(agent_output: str, eval_result: dict, blueprint_name: str) -> str | None:
    """Extract a skill from a successful run. Returns SKILL.md content or None."""
    composite = eval_result.get("composite", {})
    if composite.get("score", 85) < 85:
        return None
    
    agent_id = eval_result.get("agent_id", "unknown")
    score = composite.get("score", 85)
    
    skill = f"""---
name: {blueprint_name}-extracted-{agent_id[:8]}
description: Extracted from successful {blueprint_name} run
version: 1.0.0
source_agent: {agent_id}
source_score: {score}
---

# Extracted Skill: {blueprint_name}

**Source:** Agent {agent_id} (score: {score})
**Domain:** {eval_result.get('blueprint', blueprint_name)}

## Successful Pattern

[Extracted from agent output — review before use]

## When to Use

[Conditions where this pattern applies]

## Anti-Patterns to Avoid

[What didn't work, learned from evals]
"""
    return skill


def save_extracted_skill(blueprint_name: str, skill_content: str):
    """Save extracted skill to blueprint's skills/ directory."""
    from pathlib import Path
    from persistence import atomic_write
    
    skills_dir = Path(f"blueprints/{blueprint_name}/skills/extracted")
    skills_dir.mkdir(parents=True, exist_ok=True)
    
    import time
    skill_name = f"skill-{int(time.time())}.md"
    atomic_write(skills_dir / skill_name, skill_content)
    
    return str(skills_dir / skill_name)


def extract_skill_from_success(agent_output: str, eval_result: dict, blueprint_name: str) -> str | None:
    """
    Full pipeline: extract + save skill from successful run.
    Called from teacher or forge.py cmd_improve.
    """
    skill = extract_skill(agent_output, eval_result, blueprint_name)
    if skill:
        path = save_extracted_skill(blueprint_name, skill)
        print(f"  ✓ Skill extracted: {path}")
        return path
    return None
```

---

## 3. Skill Lifecycle

```
agent run (≥85) → extract pattern → save to blueprint/skills/extracted/
                                        ↓
                           loaded in future spawns (Skill_Loading_Mechanism)
                                        ↓
                           if pattern proves reliable → promote to blueprint/skills/
```

---

## 4. Teacher Integration

Teacher automatically calls `extract_skill_from_success()` when composite ≥ 85:

```python
# In teacher.py analyze_eval():
if composite_score >= 85:
    skill_path = extract_skill_from_success(agent_output, eval_data, blueprint_name)
    teacher_review["extracted_skills"].append(skill_path)
```

---

**Status:** Specification complete.
