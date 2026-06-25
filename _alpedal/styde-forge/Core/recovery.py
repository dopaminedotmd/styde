"""
Crash detection and checkpoint recovery.

Detects crashes via lock file. Restores from latest valid checkpoint.
"""
import os
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from Core.checkpoint import list_checkpoints, verify_checkpoint, restore_checkpoint
from Core.state import load_state

FORGE_ROOT = Path(__file__).resolve().parent.parent
LOCK_FILE = FORGE_ROOT / ".forge.lock"
RECOVERY_LOG = FORGE_ROOT / "logs" / "recovery.log"


def acquire_lock() -> bool:
    """Acquire forge lock. Returns False if already locked."""
    if LOCK_FILE.exists():
        # Check if stale (process dead but lock remains)
        try:
            data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            pid = data.get("pid", 0)
            if _process_alive(pid):
                return False
            # Stale lock — process is dead
            _log_recovery("Stale lock detected (PID %d dead). Clearing.", pid)
        except (json.JSONDecodeError, ValueError):
            pass
        LOCK_FILE.unlink(missing_ok=True)

    lock_data = {
        "pid": os.getpid(),
        "acquired": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    LOCK_FILE.write_text(json.dumps(lock_data), encoding="utf-8")
    return True


def release_lock():
    """Release forge lock."""
    LOCK_FILE.unlink(missing_ok=True)


def is_locked() -> bool:
    """Check if forge is currently locked/running."""
    if not LOCK_FILE.exists():
        return False
    try:
        data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
        pid = data.get("pid", 0)
        return _process_alive(pid)
    except (json.JSONDecodeError, ValueError):
        LOCK_FILE.unlink(missing_ok=True)
        return False


def detect_crash() -> bool:
    """
    Detect if last run crashed.

    Crash = lock file exists but process is dead, or
    state.yaml shows loop_iterations but last_checkpoint is old.
    """
    # Check lock file
    if LOCK_FILE.exists():
        try:
            data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
            pid = data.get("pid", 0)
            if not _process_alive(pid):
                _log_recovery("Crash detected: lock file exists but PID %d is dead.", pid)
                return True
        except (json.JSONDecodeError, ValueError):
            _log_recovery("Crash detected: corrupt lock file.")
            return True

    # Check state consistency
    try:
        state = load_state()
        loops = state.get("loop_iterations", 0)
        last_checkpoint = state.get("last_checkpoint")

        if loops > 0 and not last_checkpoint:
            _log_recovery("Crash detected: %d loops but no checkpoints.", loops)
            return True
    except FileNotFoundError:
        pass  # No state means no crash to detect

    return False


def recover() -> bool:
    """
    Attempt recovery from crash.

    1. Find latest valid checkpoint
    2. Restore from it
    3. Clean up lock file
    4. Log recovery event

    Returns True if recovery succeeded.
    """
    _log_recovery("Recovery initiated.")

    # Find latest valid checkpoint
    checkpoints = list_checkpoints()
    valid_checkpoint: Optional[str] = None

    for cp in checkpoints:
        cid = cp.get("checkpoint_id", "")
        if not cid:
            continue
        verification = verify_checkpoint(cid)
        if verification["valid"]:
            valid_checkpoint = cid
            break
        else:
            _log_recovery(
                "Checkpoint %s invalid: %s", cid, "; ".join(verification["errors"])
            )

    if not valid_checkpoint:
        _log_recovery("Recovery failed: no valid checkpoints found.")
        return False

    _log_recovery("Restoring from checkpoint: %s", valid_checkpoint)

    try:
        restore_checkpoint(valid_checkpoint)
        release_lock()
        _log_recovery("Recovery complete. Restored from %s.", valid_checkpoint)
        return True
    except Exception as e:
        _log_recovery("Recovery failed: %s", str(e))
        return False


def check_and_recover() -> bool:
    """
    Full crash detection + recovery cycle.
    Safe to call at startup. Returns True if recovery was needed and succeeded.
    """
    if not detect_crash():
        # Clean up any stale lock
        if LOCK_FILE.exists():
            try:
                data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
                pid = data.get("pid", 0)
                if not _process_alive(pid):
                    LOCK_FILE.unlink(missing_ok=True)
            except (json.JSONDecodeError, ValueError):
                LOCK_FILE.unlink(missing_ok=True)
        return False

    return recover()


# --- internals ---

def _process_alive(pid: int) -> bool:
    """Check if a process with given PID is alive (Windows + Unix)."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def _log_recovery(msg: str, *args):
    """Append to recovery log."""
    log_dir = RECOVERY_LOG.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{timestamp}] {msg % args if args else msg}\n"

    with open(RECOVERY_LOG, "a", encoding="utf-8") as f:
        f.write(line)
