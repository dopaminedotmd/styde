# Security Model

**Styde Forge v3.0 — Phase 0**
**Section:** 07_Multi_Agent

---

## 1. Threat Model

| Threat | Vector | Severity |
|--------|--------|----------|
| Prompt injection | Malicious task description injected into subagent | High |
| Cross-agent contamination | One agent's output poisons another's context | Medium |
| Resource exhaustion | Agent spawns fork bomb or fills disk | High |
| Data exfiltration | Agent reads sensitive files | Medium |
| USB tampering | Malicious USB content on import | Low |

---

## 2. Mitigations

### Prompt Injection
- Subagents receive task in isolated `delegate_task` context
- No agent can modify another agent's task
- All agent inputs pass through Parent validation

### Cross-Agent Contamination
- No shared mutable state between agents
- Knowledge sharing via read-only eval results
- Each agent gets fresh context per spawn

### Resource Exhaustion
- Resource Governor enforces VRAM/RAM/disk limits
- Subagents have timeout (300s default)
- Sandbox directories are size-limited

### Data Exfiltration
- Agents run in sandbox directories
- No access to `~/.hermes/` or system files
- File operations limited to forge directories

### USB Tampering
- Import validates structure before loading
- Checksum verification on checkpoints
- State is always restorable from last valid checkpoint

---

## 3. Sandbox Rules

```python
AGENT_SANDBOX_RULES = {
    "allowed_dirs": ["sandbox/<agent_id>/", "eval/results/"],
    "forbidden_dirs": ["~/.hermes/", "~/.ssh/", "/etc/", "C:/Windows/"],
    "max_file_size_mb": 100,
    "max_total_size_mb": 500,
    "timeout_seconds": 300,
    "max_subprocesses": 10
}
```

---

## 4. Audit Trail

Every agent action is logged:
- Task description (immutable after spawn)
- Model selected + why
- All tool calls with timestamps
- Output + self-evaluation
- Eval results + judge notes

---

**Status:** Security model defined. Sandboxing in v3.0.
