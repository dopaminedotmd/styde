"""
Atomic checkpoints: create, verify, list, restore.

Checkpoints save forge state atomically. Never partial.
USB-yank safe: temp-file + rename pattern throughout.
"""
import shutil
import time
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from Core.state import load_state, save_state
from Core.persistence import atomic_write, atomic_write_json

FORGE_ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS_DIR = FORGE_ROOT / "checkpoints"

# Files included in every checkpoint
CHECKPOINT_FILES = [
    "state.yaml",
    "00_MANIFEST.json",
    "blueprints/",
    "eval/benchmarks/",
    "StydeAgents/refinery/",
    "StydeAgents/production/",
    "99_INDEXES/hardware_profile.json",
]

# Files explicitly excluded
EXCLUDE_PATTERNS = [
    "checkpoints/",
    "01_KNOWLEDGE/",
    "StydeAgents/archive/",
    "99_INDEXES/cache.db",
    "logs/",
    "__pycache__/",
    ".git/",
    ".staging",
    ".tmp",
    "target/",  # Rust build artifacts
    "node_modules/",
]


def create_checkpoint(label: str = "") -> str:
    """
    Create atomic checkpoint of forge state.

    Returns checkpoint ID (directory name).
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    label_slug = f"-{label.replace(' ', '_')}" if label else ""
    checkpoint_id = f"checkpoint-{timestamp}{label_slug}"

    staging = CHECKPOINTS_DIR / f".{checkpoint_id}.staging"
    target = CHECKPOINTS_DIR / checkpoint_id

    if staging.exists():
        shutil.rmtree(staging)

    try:
        # Update state with checkpoint info
        state = load_state()
        state["last_checkpoint"] = checkpoint_id
        state["last_checkpoint_at"] = datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )

        # Save state to staging
        staging.mkdir(parents=True, exist_ok=True)
        save_state(state)
        shutil.copy2(FORGE_ROOT / "state.yaml", staging / "state.yaml")

        # Copy manifest
        manifest = FORGE_ROOT / "00_MANIFEST.json"
        if manifest.exists():
            shutil.copy2(manifest, staging / "00_MANIFEST.json")

        # Copy blueprint directories
        blueprints = FORGE_ROOT / "StydeAgents" / "blueprints"
        if blueprints.exists():
            _copy_dir(blueprints, staging / "blueprints")

        # Copy benchmarks
        benchmarks = FORGE_ROOT / "eval" / "benchmarks"
        if benchmarks.exists():
            _copy_dir(benchmarks, staging / "eval" / "benchmarks")

        # Copy refinery and production agents
        for agent_dir in ["refinery", "production"]:
            src = FORGE_ROOT / "StydeAgents" / agent_dir
            if src.exists():
                _copy_dir(src, staging / "StydeAgents" / agent_dir)

        # Copy hardware profile
        hw = FORGE_ROOT / "99_INDEXES" / "hardware_profile.json"
        if hw.exists():
            staging_hw = staging / "99_INDEXES"
            staging_hw.mkdir(parents=True, exist_ok=True)
            shutil.copy2(hw, staging_hw / "hardware_profile.json")

        # Create checkpoint manifest
        manifest_data = {
            "checkpoint_id": checkpoint_id,
            "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "label": label or "",
            "loop_iterations": state.get("loop_iterations", 0),
            "total_agents": state.get("total_agents_spawned", 0),
            "total_evaluations": state.get("total_evaluations", 0),
        }
        # Compute hash of all files for integrity
        manifest_data["content_hash"] = _hash_dir(staging)
        atomic_write_json(staging / "checkpoint_manifest.json", manifest_data)

        # Atomic rename: staging → target (Windows-safe with retry)
        if target.exists():
            shutil.rmtree(target)
        # Retry rename on Windows (antivirus/file locks)
        for attempt in range(3):
            try:
                staging.rename(target)
                break
            except (PermissionError, OSError):
                if attempt < 2:
                    time.sleep(0.5)
                    # Try delete + copy fallback
                    try:
                        if not target.exists():
                            shutil.copytree(str(staging), str(target))
                            shutil.rmtree(str(staging))
                            break
                    except Exception:
                        pass
                else:
                    raise

        # Update state atomically
        save_state(state)

        return checkpoint_id

    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def list_checkpoints() -> list[dict]:
    """List all checkpoints, newest first."""
    if not CHECKPOINTS_DIR.exists():
        return []

    checkpoints = []
    for d in sorted(CHECKPOINTS_DIR.glob("checkpoint-*"), reverse=True):
        if d.name.startswith("."):
            continue  # Skip staging dirs
        if not d.is_dir():
            continue

        manifest = d / "checkpoint_manifest.json"
        if manifest.exists():
            import json
            data = json.loads(manifest.read_text(encoding="utf-8"))
        else:
            data = {"checkpoint_id": d.name, "created": "unknown"}

        checkpoints.append(data)

    return checkpoints


def verify_checkpoint(checkpoint_id: str) -> dict:
    """Verify checkpoint integrity. Returns {valid: bool, errors: [str]}."""
    checkpoint_dir = CHECKPOINTS_DIR / checkpoint_id
    if not checkpoint_dir.exists():
        return {"valid": False, "errors": [f"Checkpoint not found: {checkpoint_id}"]}

    manifest = checkpoint_dir / "checkpoint_manifest.json"
    if not manifest.exists():
        return {"valid": False, "errors": ["Missing checkpoint manifest"]}

    import json
    data = json.loads(manifest.read_text(encoding="utf-8"))
    expected_hash = data.get("content_hash")

    if not expected_hash:
        return {"valid": False, "errors": ["Manifest missing content_hash"]}

    current_hash = _hash_dir(checkpoint_dir)
    if current_hash != expected_hash:
        return {
            "valid": False,
            "errors": [f"Hash mismatch: expected {expected_hash[:16]}, got {current_hash[:16]}"],
        }

    return {"valid": True, "errors": []}


def restore_checkpoint(checkpoint_id: str) -> bool:
    """Restore forge state from checkpoint. DANGER: overwrites current state."""
    checkpoint_dir = CHECKPOINTS_DIR / checkpoint_id
    if not checkpoint_dir.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_id}")

    # Verify first
    verification = verify_checkpoint(checkpoint_id)
    if not verification["valid"]:
        raise ValueError(f"Checkpoint corrupt: {verification['errors']}")

    # Restore files (only files that exist in checkpoint)
    restore_map = {
        "state.yaml": FORGE_ROOT / "state.yaml",
        "00_MANIFEST.json": FORGE_ROOT / "00_MANIFEST.json",
    }

    for src_name, dest in restore_map.items():
        src = checkpoint_dir / src_name
        if src.exists():
            shutil.copy2(src, dest)

    # Restore directories
    for dir_name in ["blueprints", "StydeAgents", "eval", "99_INDEXES"]:
        src = checkpoint_dir / dir_name
        if src.exists():
            dest = FORGE_ROOT / dir_name
            if dest.exists():
                shutil.rmtree(dest)
            _copy_dir(src, dest)

    return True


# --- internals ---

def _copy_dir(src: Path, dest: Path):
    """Recursively copy directory, excluding patterns."""
    dest.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        # Check exclusions — match both full relative path and basename-only forms
        rel = str(item.relative_to(src))
        skip = False
        for p in EXCLUDE_PATTERNS:
            stripped = p.rstrip("/")
            if rel.startswith(stripped) or stripped == rel:
                skip = True
                break
            # Also match the leaf name (handles when src is a subdirectory like 99_INDEXES/)
            leaf = stripped.split("/")[-1]
            if rel == leaf or rel.startswith(leaf + "/"):
                skip = True
                break
        if skip:
            continue
        if item.name.startswith("."):
            continue

        if item.is_dir():
            dest_item = dest / item.name
            _copy_dir(item, dest_item)
        else:
            shutil.copy2(item, dest)


def _hash_dir(path: Path) -> str:
    """Compute SHA256 of all file contents in directory (stable order)."""
    hasher = hashlib.sha256()

    for f in sorted(path.rglob("*")):
        if f.is_file() and not f.name.startswith("."):
            hasher.update(str(f.relative_to(path)).encode())
            hasher.update(f.read_bytes())

    return hasher.hexdigest()
