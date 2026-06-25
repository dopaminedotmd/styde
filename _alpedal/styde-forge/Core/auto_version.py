"""
Automatic semantic versioning for blueprints.
Versions are bumped based on eval score changes.

Schema: MAJOR.MINOR.PATCH
  MAJOR: quality gate passed (≥85) — structural readiness
  MINOR: score improved by ≥5 points
  PATCH: score changed <5 points or minor tweaks
"""
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from Core.persistence import atomic_write

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "blueprints"


def get_version(blueprint_name: str) -> str:
    """Get current version of a blueprint. Returns '0.0.0' if none."""
    config = _load_config(blueprint_name)
    if config is None:
        return "0.0.0"
    return config.get("blueprint", {}).get("version", "0.0.0")


def bump_version(
    blueprint_name: str,
    score: float,
    previous_score: Optional[float] = None,
) -> str:
    """
    Bump blueprint version based on eval score.

    Rules:
      score ≥ 85        → MAJOR bump  (quality gate passed)
      score improved ≥5  → MINOR bump  (meaningful improvement)
      otherwise          → PATCH bump  (minor tweak)

    Returns new version string.
    """
    config = _load_config(blueprint_name)
    if config is None:
        raise FileNotFoundError(f"Blueprint not found: {blueprint_name}")

    current = config.get("blueprint", {}).get("version", "0.0.0")
    major, minor, patch = _parse_version(current)

    delta = score - previous_score if previous_score is not None else 0

    if score >= 85:
        major += 1
        minor = 0
        patch = 0
        reason = f"MAJOR: quality gate passed (score={score})"
    elif delta >= 5:
        minor += 1
        patch = 0
        reason = f"MINOR: score improved by {delta:.1f} points (prev={previous_score}, new={score})"
    else:
        patch += 1
        reason = f"PATCH: minor change (score={score}, delta={delta:.1f})"

    new_version = f"{major}.{minor}.{patch}"

    # Update config
    if "blueprint" not in config:
        config["blueprint"] = {}
    config["blueprint"]["version"] = new_version

    # Record version history
    if "version_history" not in config["blueprint"]:
        config["blueprint"]["version_history"] = []

    config["blueprint"]["version_history"].append({
        "from": current,
        "to": new_version,
        "reason": reason,
        "score": score,
        "previous_score": previous_score,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })

    # Write back
    config_path = BLUEPRINTS_DIR / blueprint_name / "config.yaml"
    content = yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False)
    atomic_write(config_path, content)

    return new_version


def bump_manual(
    blueprint_name: str,
    bump_type: str,
    reason: str = "Manual bump",
) -> str:
    """
    Manually bump a specific version component.

    Args:
        bump_type: 'major', 'minor', or 'patch'
        reason: Human-readable reason
    """
    config = _load_config(blueprint_name)
    if config is None:
        raise FileNotFoundError(f"Blueprint not found: {blueprint_name}")

    current = config.get("blueprint", {}).get("version", "0.0.0")
    major, minor, patch = _parse_version(current)

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    new_version = f"{major}.{minor}.{patch}"

    if "blueprint" not in config:
        config["blueprint"] = {}
    config["blueprint"]["version"] = new_version

    if "version_history" not in config["blueprint"]:
        config["blueprint"]["version_history"] = []

    config["blueprint"]["version_history"].append({
        "from": current,
        "to": new_version,
        "reason": reason,
        "score": None,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    })

    config_path = BLUEPRINTS_DIR / blueprint_name / "config.yaml"
    content = yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False)
    atomic_write(config_path, content)

    return new_version


def get_history(blueprint_name: str) -> list[dict]:
    """Get version history for a blueprint."""
    config = _load_config(blueprint_name)
    if config is None:
        return []
    return config.get("blueprint", {}).get("version_history", [])


def latest_score(blueprint_name: str) -> Optional[float]:
    """Get the score from the latest version bump. None if no history."""
    history = get_history(blueprint_name)
    if not history:
        return None
    return history[-1].get("score")


# --- internals ---

def _load_config(blueprint_name: str) -> Optional[dict]:
    config_path = BLUEPRINTS_DIR / blueprint_name / "config.yaml"
    if not config_path.exists():
        return None
    return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}


def _parse_version(version) -> tuple[int, int, int]:
    """Parse version that may be int, float, or string."""
    if isinstance(version, (int, float)):
        return int(version), 0, 0
    try:
        parts = str(version).split(".")
        return int(parts[0]), int(parts[1]) if len(parts) > 1 else 0, int(parts[2]) if len(parts) > 2 else 0
    except (ValueError, IndexError):
        return 0, 0, 0
