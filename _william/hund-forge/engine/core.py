"""
hund-forge — Persona Refinement Engine
Specialiserad Forge for att gora Hund till en agent i varldsklass.

Loop: Spawn -> Eval (self+judge) -> Teacher -> Improve -> Version
"""

from pathlib import Path
from datetime import datetime, timezone
import yaml
import json
import uuid
import sys

FORGE_ROOT = Path(__file__).resolve().parent.parent
BLUEPRINTS_DIR = FORGE_ROOT / "blueprints"
BENCHMARKS_DIR = FORGE_ROOT / "benchmarks"
RUNS_DIR = FORGE_ROOT / "runs"


def load_blueprint(name: str) -> dict:
    """Load a blueprint directory."""
    bp_dir = BLUEPRINTS_DIR / name
    if not bp_dir.exists():
        raise FileNotFoundError(f"Blueprint not found: {bp_dir}")

    ctx = {}
    for fname in ["persona.md", "BLUEPRINT.md", "config.yaml"]:
        fp = bp_dir / fname
        if fp.exists():
            content = fp.read_text(encoding="utf-8")
            if fname.endswith(".yaml"):
                content = yaml.safe_load(content)
            ctx[fname.replace(".md", "").replace(".yaml", "")] = content

    return ctx


def load_benchmark(name: str) -> str:
    """Load a benchmark file."""
    bp = BENCHMARKS_DIR / f"{name}.md"
    if not bp.exists():
        raise FileNotFoundError(f"Benchmark not found: {bp}")
    return bp.read_text(encoding="utf-8")


def load_state() -> dict:
    """Load forge state."""
    sf = FORGE_ROOT / "state.yaml"
    if not sf.exists():
        return _default_state()
    return yaml.safe_load(sf.read_text(encoding="utf-8"))


def save_state(state: dict):
    """Save forge state atomically."""
    sf = FORGE_ROOT / "state.yaml"
    content = yaml.dump(state, default_flow_style=False, allow_unicode=True)
    sf.write_text(content, encoding="utf-8")


def _default_state() -> dict:
    return {
        "forge_version": "1.0.0",
        "forge_codename": "Hundsmaltan",
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "loop_iterations": 0,
        "total_spawns": 0,
        "total_evals": 0,
        "blueprints": [],
        "runs": [],
        "evaluations": [],
        "improvements": [],
    }


def create_run(blueprint_name: str, benchmark_name: str) -> dict:
    """Create a new run entry."""
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_DIR / f"run-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    run = {
        "run_id": run_id,
        "blueprint": blueprint_name,
        "benchmark": benchmark_name,
        "started_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "spawned",
        "output_path": str(run_dir / "output.md"),
        "eval_path": str(run_dir / "eval.yaml"),
        "teacher_path": str(run_dir / "teacher.md"),
    }

    # Update state
    state = load_state()
    state["total_spawns"] = state.get("total_spawns", 0) + 1
    state.setdefault("runs", []).append(run)
    save_state(state)

    return run


def update_run(run_id: str, updates: dict):
    """Update a run entry in state."""
    state = load_state()
    for run in state.get("runs", []):
        if run["run_id"] == run_id:
            run.update(updates)
            break
    save_state(state)


def get_run_dir(run_id: str) -> Path:
    """Get the run directory path."""
    return RUNS_DIR / f"run-{run_id}"


def list_runs(blueprint_name: str = None, limit: int = 10) -> list:
    """List recent runs, optionally filtered by blueprint."""
    state = load_state()
    runs = state.get("runs", [])
    if blueprint_name:
        runs = [r for r in runs if r["blueprint"] == blueprint_name]
    runs.sort(key=lambda r: r.get("started_at", ""), reverse=True)
    return runs[:limit]
