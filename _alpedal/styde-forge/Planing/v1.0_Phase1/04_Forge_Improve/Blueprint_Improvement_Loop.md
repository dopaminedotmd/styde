# Blueprint Improvement Loop

**Styde Forge v3.0**
**Section:** 04_Forge_Improve
**References:** `Core_Loop_Detail.md` §4, `State_Machines.md` §2-3, `Teacher_Agent.md`

---

## 1. State Machine

```
eval pending → composite score computed
  │
  ├── ≥85 × 3 consecutive → PROMOTE: refinery/ → production/
  ├── 70-84               → RETRY:  update blueprint, re-spawn (max 3)
  └── <70                 → ARCHIVE: refinery/ → archive/
```

---

## 2. Implementation

```python
# Core/improve.py or inline in forge.py

def apply_loop_result(blueprint_name: str, agent_id: str, composite: dict, teacher_review: dict) -> str:
    """
    Apply the result of one loop iteration.
    Returns: 'promoted', 'retrying', 'archived', 'retry_exhausted'
    """
    from state import load_state, save_state
    from forge import AGENTS_DIR
    import shutil
    
    state = load_state()
    agents = [a for a in state["agents"] if a["name"] == agent_id]
    if not agents:
        return "not_found"
    
    agent = agents[0]
    score = composite["score"]
    
    # Track consecutive passes
    if composite["passed"]:
        agent["evals_passed"] = agent.get("evals_passed", 0) + 1
    else:
        agent["evals_passed"] = 0
        agent["retries"] = agent.get("retries", 0) + 1
    
    agent["composite_score"] = score
    
    # --- PROMOTE ---
    if agent["evals_passed"] >= 3:
        src = AGENTS_DIR / "refinery" / agent_id
        dst = AGENTS_DIR / "production" / agent_id
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
        agent["stage"] = "production"
        agent["status"] = "deployed"
        
        for bp in state["blueprints"]:
            if bp["name"] == blueprint_name:
                bp["status"] = "stable"
        
        save_state(state)
        return "promoted"
    
    # --- ARCHIVE ---
    if score < 70:
        src = AGENTS_DIR / "refinery" / agent_id
        dst = AGENTS_DIR / "archive" / agent_id
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.move(str(src), str(dst))
        agent["stage"] = "archive"
        agent["status"] = "archived"
        save_state(state)
        return "archived"
    
    # --- RETRY (max 3) ---
    if agent.get("retries", 0) >= 3:
        src = AGENTS_DIR / "refinery" / agent_id
        dst = AGENTS_DIR / "archive" / agent_id
        if src.exists():
            shutil.move(str(src), str(dst))
        agent["stage"] = "archive"
        agent["status"] = "retry_exhausted"
        save_state(state)
        return "retry_exhausted"
    
    # Apply teacher improvements to blueprint
    for imp in teacher_review.get("improvements", []):
        target_path = Path(f"blueprints/{blueprint_name}/{imp['target']}")
        if target_path.exists():
            current = target_path.read_text(encoding="utf-8")
            note = f"\n## Improvement ({datetime.now():%Y-%m-%d})\n{imp['change']}\n"
            from persistence import atomic_write
            atomic_write(target_path, current + note)
    
    agent["status"] = "retrying"
    
    for bp in state["blueprints"]:
        if bp["name"] == blueprint_name:
            bp["version"] += 1
    
    save_state(state)
    return "retrying"
```

---

## 3. Loop Termination

| State | Action |
|-------|--------|
| promoted | Move to production/, celebrate |
| retrying | Update blueprint, re-spawn (max 3 attempts) |
| retry_exhausted | Archive, log lessons |
| archived | Archive, log lessons, circuit breaker check |

---

**Status:** Specification complete.
