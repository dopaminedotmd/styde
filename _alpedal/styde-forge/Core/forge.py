"""
Styde Forge v3.0 — The Crucible
Main CLI entry point.
"""
import sys
import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

from Core.persistence import atomic_write, atomic_write_json
from Core.detect import HardwareAdapter
from Core.state import load_state, save_state

FORGE_ROOT = Path(__file__).resolve().parent.parent


def _state_file() -> Path:
    return FORGE_ROOT / "state.yaml"


def cmd_init():
    """Create USB directory structure and initialize state."""
    print("=== Styde Forge v3.0 — Initializing ===")

    dirs = [
        "StydeAgents/data/benchmarks",
        "StydeAgents/data/knowledge",
        "StydeAgents/data/templates",
        "StydeAgents/refinery",
        "StydeAgents/production",
        "StydeAgents/archive",
        "99_INDEXES",
        "logs",
        "scripts",
        "blueprints",
    ]
    for d in dirs:
        path = FORGE_ROOT / d
        path.mkdir(parents=True, exist_ok=True)

    # Detect hardware
    print("\n--- Hardware Detection ---")
    try:
        adapter = HardwareAdapter()
        profile = adapter.detect()
        indexes = FORGE_ROOT / "99_INDEXES"
        indexes.mkdir(parents=True, exist_ok=True)
        atomic_write_json(indexes / "hardware_profile.json", profile)
        print(f"  Type: {profile['hardware']['type']}")
        print(f"  VRAM: {profile['hardware']['vram_gb']:.1f} GB")
        print(f"  RAM:  {profile['hardware']['ram_gb']:.1f} GB")
        print(f"  Sampling: {profile['adaptations']['sampling_method']}")
        hw_profile_name = "pontus-main" if profile["hardware"]["type"] == "B" else "pontus-beast"
    except Exception as e:
        print(f"  Warning: Hardware detection failed: {e}")
        profile = None
        hw_profile_name = "pontus-main"

    # Initialize state.yaml
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state = {
        "forge_version": "3.0.0",
        "forge_codename": "The Crucible",
        "created": now,
        "last_checkpoint": None,
        "hardware_profile": hw_profile_name,
        "caveman_ultra": True,
        "loop_iterations": 0,
        "total_agents_spawned": 0,
        "total_evaluations": 0,
        "blueprints": [],
        "agents": [],
        "evaluations": [],
        "improvements": [],
    }
    content = yaml.dump(state, default_flow_style=False, allow_unicode=True)
    atomic_write(_state_file(), content)

    # Create manifest
    manifest = {
        "forge": {
            "version": "3.0.0",
            "codename": "The Crucible",
            "created": now,
            "last_updated": now,
            "sha256": hashlib.sha256(content.encode()).hexdigest()
        },
        "statistics": {
            "total_agents": 0,
            "total_evaluations": 0,
            "total_loop_iterations": 0,
            "storage_used_gb": 0.0,
            "storage_limit_gb": 48.0
        },
        "best_per_domain": {
            "coding": {"agent_id": None, "score": None},
            "research": {"agent_id": None, "score": None},
            "automation": {"agent_id": None, "score": None},
            "documentation": {"agent_id": None, "score": None},
            "testing": {"agent_id": None, "score": None},
            "meta": {"agent_id": None, "score": None}
        },
        "provenance": {
            "generation_chain": ["v3.0_hermes"],
            "hardware_profiles_used": [hw_profile_name]
        }
    }
    atomic_write_json(FORGE_ROOT / "00_MANIFEST.json", manifest)

    print(f"\n=== Forge initialized successfully ===")
    print(f"State: {_state_file()}")
    if profile:
        print(f"Profile: {profile['hardware']['type']} ({profile['hardware']['vram_gb']:.1f} GB VRAM)")


def cmd_status():
    """Show current forge status."""
    state = load_state()

    print(f"Styde Forge v{state['forge_version']} — {state['forge_codename']}")
    if state.get("hardware_profile"):
        print(f"Hardware: {state['hardware_profile']}")
    print(f"Caveman Ultra: {'ON' if state.get('caveman_ultra', True) else 'OFF'}")
    print(f"Loop iterations: {state.get('loop_iterations', 0)}")
    print(f"Total agents spawned: {state.get('total_agents_spawned', 0)}")
    print(f"Total evaluations: {state.get('total_evaluations', 0)}")

    agents = state.get("agents", [])
    refinery = [a for a in agents if a.get("stage") == "refinery"]
    production = [a for a in agents if a.get("stage") == "production"]
    archive = [a for a in agents if a.get("stage") == "archive"]

    print(f"Active blueprints: {len(state.get('blueprints', []))}")
    print(f"Agents in refinery: {len(refinery)}")
    print(f"Agents in production: {len(production)}")
    print(f"Agents archived: {len(archive)}")

    if state.get("last_checkpoint"):
        print(f"Last checkpoint: {state['last_checkpoint']}")
    else:
        print("No checkpoints yet.")
