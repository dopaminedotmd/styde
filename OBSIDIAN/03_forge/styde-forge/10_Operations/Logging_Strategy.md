# Logging Strategy

**Styde Forge v3.0 — Phase 0**
**Section:** 10_Operations

---

## 1. Purpose

Structured, searchable, space-efficient logging across all forge operations.
Every decision, spawn, eval, and error must be traceable.

---

## 2. Log Structure

```
logs/
├── forge.log                    # Main log (JSON-lines)
├── loops/
│   └── loop-<timestamp>.jsonl   # Per loop-iteration
├── agents/
│   └── <agent-id>.jsonl         # Per agent: spawn, runs, results
├── errors/
│   └── error-<timestamp>.jsonl  # Crashes, incidents, anomalies
├── security/
│   └── security.log             # Security events (prompt injections, sandbox violations)
├── validation/
│   └── validation.log           # Blueprint validation results
└── recovery/
    └── recovery.log             # Crash recovery events
```

---

## 3. Log Format (JSON-Lines)

Every log entry is one line of JSON:

```json
{
  "timestamp": "2026-06-25T12:30:00Z",
  "level": "INFO",
  "component": "forge.spawn",
  "operation": "agent_spawn",
  "blueprint": "code-reviewer",
  "agent_id": "agent-code-reviewer-20260625-123000",
  "model": "deepseek-v4-pro",
  "duration_ms": 2340,
  "status": "success",
  "details": "Agent spawned with 3 skills"
}
```

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed step-by-step (off by default) |
| INFO | Normal operations (spawn, eval, checkpoint) |
| WARN | Non-critical issues (low eval, retry) |
| ERROR | Failures (crash, timeout, corrupted state) |
| CRITICAL | Data loss risk (USB disconnect, disk full) |

---

## 4. What Gets Logged

| Event | Level | Fields |
|-------|-------|--------|
| Blueprint created | INFO | name, version |
| Agent spawned | INFO | blueprint, agent_id, model, skills_loaded |
| Self-eval completed | INFO | agent_id, self_score |
| Judge eval completed | INFO | agent_id, judge_model, composite_score |
| Weight update | DEBUG | old_weights, new_weights, delta |
| Checkpoint created | INFO | checkpoint_id, size_bytes |
| Recovery triggered | WARN | checkpoint_used, transactions_replayed |
| Crash detected | ERROR | last_operation, stack_trace |
| Quality gate failed | WARN | agent_id, score, reason |
| Disk > 90% | WARN | current_usage_gb, limit_gb |
| USB disconnect | CRITICAL | last_checkpoint_age_seconds |

---

## 5. Log Rotation & Retention

| File | Max Size | Retention |
|------|----------|-----------|
| forge.log | 50 MB | 30 days |
| Per-loop logs | 10 MB | 90 days |
| Per-agent logs | 5 MB | Until agent archived |
| Error logs | 20 MB | 90 days |
| Security logs | 10 MB | 180 days |

Rotation: rename to `.1`, `.2`, etc. Keep last 5 rotations.

---

## 6. Query Examples

```bash
# All errors in last 24h
grep '"level":"ERROR"' logs/forge.log | tail -20

# All spawns for a blueprint
grep '"blueprint":"code-reviewer"' logs/forge.log

# Average eval score today
grep '"operation":"judge_eval"' logs/forge.log | jq '.composite_score'
```

---

**Status:** Defined. JSON-lines format, 8 log categories, rotation policy.
