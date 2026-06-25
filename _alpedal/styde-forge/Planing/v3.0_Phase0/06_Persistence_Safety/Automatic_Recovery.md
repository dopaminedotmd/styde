# Automatic Recovery

**Styde Forge v3.0 — Phase 0**
**Section:** 06_Persistence_Safety

---

## 1. Purpose

Automatically detect and recover from crashes, USB disconnects, and other
failures without data loss. Runs at every Forge startup.

---

## 2. Crash Detection

```python
def detect_crash() -> bool:
    """Check if previous run ended abnormally."""

    # Check for stale lock file
    lockfile = FORGE_ROOT / ".running.lock"
    if lockfile.exists():
        lock_age = time.time() - lockfile.stat().st_mtime
        if lock_age > 300:  # 5 minutes
            return True

    # Check transaction log for incomplete operations
    last_tx = read_last_transaction()
    if last_tx and last_tx["status"] == "started":
        return True

    # Check for missing clean shutdown marker
    if not (FORGE_ROOT / ".clean_shutdown").exists():
        return True

    return False
```

---

## 3. Recovery Process

```
1. Detect crash (stale lock, missing shutdown marker, mid-operation TX)
2. Find most recent valid checkpoint (verify integrity)
3. Restore from checkpoint
4. Replay transactions after checkpoint timestamp
5. Verify state integrity
6. Clear crash indicators
7. Resume operation
```

```python
def recover():
    if not detect_crash():
        return  # Clean state

    log("Crash detected. Starting recovery...")

    # Find latest valid checkpoint
    checkpoints = sorted(CHECKPOINTS_DIR.glob("checkpoint-*"), reverse=True)
    valid_cp = None
    for cp in checkpoints:
        if verify_checkpoint(cp):
            valid_cp = cp
            break

    if not valid_cp:
        raise RecoveryError("No valid checkpoint found!")

    # Restore
    log(f"Restoring from {valid_cp.name}")
    restore_checkpoint(valid_cp.name)

    # Replay post-checkpoint transactions
    cp_time = parse_checkpoint_time(valid_cp.name)
    transactions_replayed = replay_transactions_after(cp_time)

    # Verify
    if not verify_forge_state():
        raise RecoveryError("State verification failed after recovery")

    # Clear crash indicators
    clear_crash_indicators()

    log(f"Recovery complete. {transactions_replayed} transactions replayed.")
```

---

## 4. Recovery Log

Every recovery event is logged for analysis:

```json
{
  "timestamp": "2026-06-25T14:30:00Z",
  "event": "recovery",
  "crash_detected_by": "stale_lock",
  "checkpoint_used": "checkpoint-20260625-142500",
  "transactions_replayed": 3,
  "data_loss_estimate": "~2 minutes",
  "recovery_successful": true
}
```

---

## 5. Failure Scenarios & Recovery

| Scenario | Detection | Recovery Action | Max Data Loss |
|----------|-----------|----------------|---------------|
| Process crash | Stale lock file | Restore last checkpoint | Last few minutes |
| USB disconnect | I/O errors on next access | Remount + restore | Last checkpoint |
| Power loss | No shutdown marker | Restore last checkpoint | Last checkpoint |
| Corrupted state.yaml | Parse error on load | Restore last checkpoint | Last checkpoint |
| Disk full mid-write | Write error | Atomic writes prevent corruption | None |
| Half-written checkpoint | Integrity check fail | Use previous checkpoint | Two checkpoints |

---

## 6. Crash Prevention

Proactive measures to reduce crash likelihood:

- **Graceful shutdown**: Write `.clean_shutdown` marker on normal exit
- **Transaction logging**: Every write logged before execution
- **Periodic health checks**: Self-Monitoring detects issues before crash
- **Resource governor**: Prevents VRAM/RAM/disk exhaustion
- **Timeout enforcement**: Agents killed after 300s, no zombie processes

---

## 7. Integration

- Runs automatically at every Forge startup
- Uses Atomic Checkpoints as recovery points
- Transaction log enables replay of post-checkpoint operations
- Recovery log tracks all incidents for trend analysis
- Self-Monitoring correlates recovery frequency with system health

---

**Status:** Implemented. Runs at every startup.

---

## Related Documents

- `Atomic_Checkpoint_Writes.md` — Checkpoints that recovery depends on
- `Filesystem_Transactions.md` — Atomic writes that prevent corruption
- `Risk_Register.md` — Risks that recovery mitigates (R01, R06)
- `05_Meta_Layer/Self_Monitoring_Health.md` — Health monitoring correlation
