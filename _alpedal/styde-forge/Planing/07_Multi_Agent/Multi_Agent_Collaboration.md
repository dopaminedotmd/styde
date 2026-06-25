# Multi-Agent Collaboration

**Styde Forge v3.0 — Phase 0**
**Section:** 07_Multi_Agent

---

## 1. Collaboration Patterns

### Teacher-Student (v3.0 Current)
```
Parent (Teacher) → Spawns subagent → Evaluates → Gives feedback → Updates blueprint
```

### Peer Review (v3.1+)
```
Parent → Agent A (produces) + Agent B (reviews) → Parent compares → Synthesizes
```

### Specialized Team (v3.2+)
```
Parent → Architect + Coder + Reviewer + Tester → Parallel execution
```

---

## 2. Agent Isolation

| Boundary | Mechanism |
|----------|-----------|
| Context | Separate conversation (delegate_task) |
| Filesystem | Per-agent sandbox directory |
| Skills | Only blueprint-specific skills loaded |
| Model | Independently selected |
| State | No shared mutable state |

---

## 3. Knowledge Sharing

Agents share through USB filesystem, not shared memory:

```
Agent A → eval/results/ → Historical Learning → Agent B context
```

Benefits:
- No prompt injection between agents
- Full traceability
- Knowledge survives individual failures

---

## 4. Conflict Prevention

| Conflict | Prevention |
|----------|------------|
| Same file editing | Per-agent sandboxes |
| Contradictory evals | Cross-Judge Consensus |
| Resource contention | Resource Governor |
| Version conflicts | Auto Version Increment |

---

**Status:** Teacher-Student pattern active. Team patterns defined for v3.1+.
