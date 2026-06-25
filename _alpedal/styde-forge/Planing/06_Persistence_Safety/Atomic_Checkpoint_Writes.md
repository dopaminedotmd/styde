# Atomic Checkpoint Writes

**Styde Forge v3.0 — Phase 0**
**Section:** 06_Persistence_Safety

---

## 1. Purpose

Create complete, verifiable, restorable snapshots of forge state.
Checkpoints are the foundation of portability and recovery.
Every checkpoint is written atomically — never partial, never corrupted.

---

## 2. Creation Process

```
1. Acquire lock on state.yaml
2. Create staging directory: checkpoints/.staging-YYYYMMDD-HHMMSS/
3. Copy all state to staging:
   - state.yaml
   - blueprints/ (all)
   - agents/ (metadata only, not sandboxes)
   - eval/results/
4. Verify staging integrity:
   - All required files present
   - state.yaml is valid YAML
   - Total size > minimum threshold
   - SHA256 hash computed
5. Atomic rename: staging → checkpoints/checkpoint-YYYYMMDD-HHMMSS/
6. Release lock
7. Update state.yaml → last_checkpoint
8. Log checkpoint event
```

---

## 3. Implementation

```python
def create_checkpoint() -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    staging = CHECKPOINTS_DIR / f".staging-{ts}"
    final = CHECKPOINTS_DIR / f"checkpoint-{ts}"

    # Lock
    lockfile = CHECKPOINTS_DIR / ".lock"
    acquire_lock(lockfile)

    try:
        # Copy to staging
        staging.mkdir()
        copy_forge_state(staging)

        # Verify
        if not verify_checkpoint(staging):
            shutil.rmtree(staging)
            raise CheckpointError("Integrity check failed")

        # Atomic rename (same filesystem = atomic)
        os.replace(str(staging), str(final))

        # Update state
        update_last_checkpoint(ts)

        # Log
        log_checkpoint(final.name, get_dir_size(final))

        return final.name

    finally:
        release_lock(lockfile)
```

---

## 4. Integrity Verification

```python
def verify_checkpoint(cp_dir: Path) -> bool:
    """Verify checkpoint integrity."""

    # Required files
    required = ["state.yaml"]
    for f in required:
        if not (cp_dir / f).exists():
            return False

    # Required directories
    required_dirs = ["blueprints"]
    for d in required_dirs:
        if not (cp_dir / d).is_dir():
            return False

    # state.yaml must be valid
    try:
        state = load_yaml(cp_dir / "state.yaml")
        required_keys = ["forge_version", "hardware_profile"]
        for k in required_keys:
            if k not in state:
                return False
    except:
        return False

    # Size sanity check (must not be suspiciously small)
    total_size = sum(f.stat().st_size for f in cp_dir.rglob("*") if f.is_file())
    if total_size < 100:
        return False

    # Blueprint count must match
    bp_count = len(list((cp_dir / "blueprints").iterdir()))
    state_bp_count = len(state.get("blueprints", []))
    if bp_count != state_bp_count:
        return False

    return True
```

---

## 5. Checkpoint Schedule

| Trigger | Frequency | Rationale |
|---------|-----------|-----------|
| Normal operation | Every 25-45 min | Hardware-dependent interval |
| Before agent spawn | Immediately | Safety net before risky operation |
| Before USB eject | Immediately | Final state capture |
| After significant improvement | Immediately | Don't lose progress |
| Manual | Via `forge.py checkpoint` | User discretion |
| Emergency | On resource warning | Last resort before throttle |

---

## 6. Checkpoint Retention

| Age | Action |
|-----|--------|
| < 24 hours | Keep all |
| 1-7 days | Keep hourly |
| 7-30 days | Keep daily |
| > 30 days | Delete |

Maximum checkpoints: 50. Oldest deleted when limit reached.

---

## 7. Storage Budget

Checkpoints share 3 GB of the 48 GB USB budget.
At ~5-10 MB per checkpoint × 50 max = 250-500 MB typical usage.

---

## 8. Integration

- Foundation for machine-to-machine portability
- Enables safe rollback after failed improvements
- Used by Export system for consistent snapshots
- Automatic Recovery depends on checkpoint integrity
- Checkpoint history stored in `09_CHECKPOINTS/`

---

**Status:** Implemented. Core safety feature for the forge.
