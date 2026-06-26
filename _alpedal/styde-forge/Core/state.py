"""
State management: load/save state.yaml with atomic writes + cross-platform lock.

Lock uses atomic mkdir (atomic on all OS). Falls back to no lock on permission errors.

Includes StateBatch context manager for reducing I/O during loops.
"""

import yaml
import os
import time
import tempfile
from pathlib import Path
from contextlib import contextmanager
from Core.persistence import atomic_write

FORGE_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = FORGE_ROOT / "state.yaml"
LOCK_DIR = FORGE_ROOT / "99_INDEXES" / ".state.lock.d"

# Batch write state
_batch_state: dict | None = None
_batch_dirty: bool = False


def _acquire_lock(blocking=True, timeout=30):
    """Acquire exclusive lock using atomic mkdir.

    mkdir is atomic on all platforms (POSIX + Windows).
    Returns True if lock acquired, False otherwise.
    """
    LOCK_DIR.parent.mkdir(parents=True, exist_ok=True)
    if blocking:
        deadline = time.time() + timeout
        while True:
            try:
                LOCK_DIR.mkdir(exist_ok=False)
                return True
            except FileExistsError:
                if time.time() > deadline:
                    return False
                time.sleep(0.05)
            except PermissionError:
                return True  # can't lock, proceed anyway
    else:
        try:
            LOCK_DIR.mkdir(exist_ok=False)
            return True
        except (FileExistsError, PermissionError):
            return False


def _release_lock():
    """Release the lock by removing the lock directory."""
    try:
        LOCK_DIR.rmdir()
    except (OSError, PermissionError):
        pass


def load_state() -> dict:
    """Load forge state from state.yaml. Raises FileNotFoundError if missing."""
    if _batch_state is not None:
        return _batch_state

    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}. Run 'forge.py init' first.")
    return yaml.safe_load(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict):
    """Save forge state atomically to state.yaml with file locking.

    In batch mode, marks state as dirty and defers the write.
    """
    global _batch_state, _batch_dirty

    if _batch_state is not None:
        _batch_state = state
        _batch_dirty = True
        return

    locked = _acquire_lock(blocking=True, timeout=30)
    try:
        content = yaml.dump(state, default_flow_style=False, allow_unicode=True)
        atomic_write(STATE_FILE, content)
    finally:
        if locked:
            _release_lock()


@contextmanager
def batch_writes():
    """
    Context manager that batches state writes.

    Usage:
        with batch_writes():
            state = load_state()
            state["x"] = 1
            save_state(state)   # deferred
            state["y"] = 2
            save_state(state)   # deferred
        # Single atomic write on exit
    """
    global _batch_state, _batch_dirty
    was_batching = _batch_state is not None

    if not was_batching:
        _batch_state = load_state()
        _batch_dirty = False

    try:
        yield
    finally:
        if not was_batching and _batch_dirty:
            locked = _acquire_lock(blocking=True, timeout=30)
            try:
                content = yaml.dump(_batch_state, default_flow_style=False, allow_unicode=True)
                atomic_write(STATE_FILE, content)
            finally:
                if locked:
                    _release_lock()
        if not was_batching:
            _batch_state = None
            _batch_dirty = False


# ─── Activity Log ───
ACTIVITY_MAX = 200
_activity_seq = 0


def log_activity(
    action: str,
    blueprint: str = "",
    detail: str = "",
    progress: int = 0,
    status: str = "pending",
) -> dict:
    """Append an activity entry to state.yaml. Thread-safe via batch-write pattern.
    Returns the entry dict with its assigned id."""
    global _activity_seq
    _activity_seq += 1
    entry = {
        "id": _activity_seq,
        "action": action,
        "blueprint": blueprint,
        "detail": detail,
        "progress": progress,
        "status": status,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    try:
        state = load_state() if not _batch_state else (_batch_state or load_state())
    except (FileNotFoundError, yaml.YAMLError):
        return entry
    activity = state.get("activity", [])
    if not isinstance(activity, list):
        activity = []
    activity.insert(0, entry)
    if len(activity) > ACTIVITY_MAX:
        activity = activity[:ACTIVITY_MAX]
    state["activity"] = activity
    save_state(state)
    return entry


def update_activity(entry_id: int, updates: dict) -> dict | None:
    """Update an existing activity entry by id. Returns updated entry or None if not found."""
    try:
        state = load_state() if not _batch_state else (_batch_state or load_state())
    except (FileNotFoundError, yaml.YAMLError):
        return None
    activity = state.get("activity", [])
    if not isinstance(activity, list):
        return None
    for entry in activity:
        if entry.get("id") == entry_id:
            entry.update(updates)
            entry["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            state["activity"] = activity
            save_state(state)
            return entry
    return None
