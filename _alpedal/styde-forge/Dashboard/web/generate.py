#!/usr/bin/env python
"""
Generate a standalone, self-contained Mission Control HTML page
with embedded Forge state data. No server needed — just open the file.
"""
import json
import subprocess
import sys
import yaml
import time
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent.parent
WEB_DIR = Path(__file__).resolve().parent
STATE_FILE = FORGE_ROOT / "state.yaml"
BENCHMARKS_DIR = FORGE_ROOT / "eval" / "benchmarks"
AGENTS_DIR = FORGE_ROOT / "StydeAgents"
OUTPUT_FILE = WEB_DIR / "mission_control.html"


def detect_gpus():
    gpus = []
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,name,memory.total,utilization.gpu,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 5:
                        gpus.append({
                            "index": int(parts[0]),
                            "name": parts[1],
                            "vram_gb": round(float(parts[2]) / 1024, 1),
                            "load_pct": int(float(parts[3])),
                            "temp_c": int(float(parts[4])),
                        })
    except Exception:
        pass
    return gpus


def build_state():
    state = {
        "forge_version": "3.0.0",
        "forge_codename": "The Crucible",
        "caveman_ultra": True,
        "loop_iterations": 0,
        "total_agents_spawned": 0,
        "total_evaluations": 0,
        "agents": [],
        "blueprints": [],
        "evaluations": [],
        "benchmarks": [],
        "hardware_profile": {"type": "unknown"},
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    # Load state.yaml
    if STATE_FILE.exists():
        raw = yaml.safe_load(STATE_FILE.read_text(encoding="utf-8")) or {}
        for k in ["forge_version", "forge_codename", "caveman_ultra", "loop_iterations",
                   "total_agents_spawned", "total_evaluations", "agents", "blueprints", "evaluations"]:
            state[k] = raw.get(k, state[k])

    # Live hardware detection
    try:
        from Core.detect import HardwareAdapter
        hw = HardwareAdapter().detect()
        hw["gpus"] = detect_gpus()
        state["hardware_profile"] = hw
    except Exception:
        state["hardware_profile"] = {"type": "unknown", "gpus": detect_gpus()}

    # Add RAM info
    try:
        import psutil
        state["hardware_profile"]["ram_gb"] = round(psutil.virtual_memory().total / (1024**3), 1)
    except ImportError:
        pass

    # Scan benchmarks
    if BENCHMARKS_DIR.exists():
        for bm_dir in sorted(BENCHMARKS_DIR.iterdir()):
            if bm_dir.is_dir():
                task_file = bm_dir / "task.md"
                eval_file = bm_dir / "eval.yaml"
                golden_dir = bm_dir / "golden"
                cases = len(list(golden_dir.iterdir())) if golden_dir.exists() else 0
                state["benchmarks"].append({
                    "name": bm_dir.name,
                    "has_task": task_file.exists(),
                    "has_eval": eval_file.exists(),
                    "cases": cases,
                })

    # Scan refinery agents
    refinery = AGENTS_DIR / "refinery"
    if refinery.exists():
        for agent_dir in sorted(refinery.iterdir()):
            if agent_dir.is_dir():
                meta_file = agent_dir / "AGENT.json"
                if meta_file.exists():
                    try:
                        meta = json.loads(meta_file.read_text(encoding="utf-8"))
                        state["agents"].append({
                            "name": meta.get("name", agent_dir.name),
                            "blueprint": meta.get("blueprint", "?"),
                            "stage": "refinery",
                            "status": meta.get("status", "?"),
                            "composite_score": meta.get("self_eval", {}).get("score"),
                            "spawned": meta.get("spawned"),
                        })
                    except Exception:
                        pass

    return state


def generate():
    state = build_state()
    state_json = json.dumps(state, indent=2, default=str)

    # Read the HTML template
    template = (WEB_DIR / "index.html").read_text(encoding="utf-8")

    # Replace the fetch with embedded data
    # Match: "const API = '/api/state';" -> embed state
    # Match: fetchState function -> simplified
    embedded = template.replace(
        "const API = '/api/state';",
        "const EMBEDDED_STATE = " + state_json + ";"
    ).replace(
        "async function fetchState() {\n  try {\n    const r = await fetch(API);\n    STATE = await r.json();\n    renderAll(STATE);\n    refreshCount++;\n  } catch(e) { console.error('Fetch failed:', e); }\n}",
        "function fetchState() {\n  STATE = EMBEDDED_STATE;\n  renderAll(EMBEDDED_STATE);\n  refreshCount++;\n}"
    )

    OUTPUT_FILE.write_text(embedded, encoding="utf-8")
    print(f"Generated: {OUTPUT_FILE}")
    print(f"  Agents: {len(state['agents'])}")
    print(f"  Blueprints: {len(state['blueprints'])}")
    print(f"  Benchmarks: {len(state['benchmarks'])}")
    hw = state.get("hardware_profile", {})
    if isinstance(hw, dict):
        gpus = hw.get("gpus", [])
        print(f"  GPUs: {len(gpus)}")
        for g in gpus:
            print(f"    GPU{g['index']}: {g['name']} — {g['vram_gb']}GB")


if __name__ == "__main__":
    generate()
