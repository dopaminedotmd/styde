#!/usr/bin/env python
"""
StydeForge Mission Control — Web Server
Serves the dashboard HTML and a real-time state API.
"""
import json
import time
import yaml
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

FORGE_ROOT = Path(__file__).resolve().parent.parent.parent
WEB_DIR = Path(__file__).resolve().parent
STATE_FILE = FORGE_ROOT / "state.yaml"
AGENTS_DIR = FORGE_ROOT / "StydeAgents"
BENCHMARKS_DIR = FORGE_ROOT / "eval" / "benchmarks"

LOG_BUFFER = []
MAX_LOG_LINES = 100


def log(level: str, msg: str):
    ts = time.strftime("%H:%M:%S")
    LOG_BUFFER.append({"ts": ts, "level": level, "msg": msg})
    if len(LOG_BUFFER) > MAX_LOG_LINES:
        LOG_BUFFER.pop(0)


def _detect_gpus():
    gpus = []
    try:
        import subprocess
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


def load_forge_state():
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
        "hardware_profile": None,
        "recent_logs": list(LOG_BUFFER),
    }

    # Load state.yaml
    if STATE_FILE.exists():
        try:
            raw = yaml.safe_load(STATE_FILE.read_text(encoding="utf-8"))
            if raw:
                state["forge_version"] = raw.get("forge_version", state["forge_version"])
                state["forge_codename"] = raw.get("forge_codename", state["forge_codename"])
                state["caveman_ultra"] = raw.get("caveman_ultra", True)
                state["loop_iterations"] = raw.get("loop_iterations", 0)
                state["total_agents_spawned"] = raw.get("total_agents_spawned", 0)
                state["total_evaluations"] = raw.get("total_evaluations", 0)
                state["agents"] = raw.get("agents", [])
                state["blueprints"] = raw.get("blueprints", [])
                state["evaluations"] = raw.get("evaluations", [])
                state["hardware_profile"] = raw.get("hardware_profile")
        except Exception as e:
            log("error", f"Failed to load state.yaml: {e}")

    # Try hardware_profile.json
    hw_file = FORGE_ROOT / "99_INDEXES" / "hardware_profile.json"
    if hw_file.exists():
        try:
            state["hardware_profile"] = json.loads(hw_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    # Live hardware detection
    if not state["hardware_profile"] or isinstance(state["hardware_profile"], str):
        try:
            from Core.detect import HardwareAdapter
            adapter = HardwareAdapter()
            hw = adapter.detect()
            hw["gpus"] = _detect_gpus()
            state["hardware_profile"] = hw
        except Exception as e:
            state["hardware_profile"] = {"type": "unknown", "error": str(e), "gpus": _detect_gpus()}
    elif isinstance(state["hardware_profile"], dict) and "gpus" not in state["hardware_profile"]:
        state["hardware_profile"]["gpus"] = _detect_gpus()

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
                        if not any(a.get("name") == meta.get("name") for a in state["agents"]):
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

    state["recent_logs"] = list(LOG_BUFFER)
    return state


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            state = load_forge_state()
            self.wfile.write(json.dumps(state, indent=2, default=str).encode())
        elif self.path == "/" or self.path == "":
            self.path = "/index.html"
            super().do_GET()
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass


def main():
    import argparse
    parser = argparse.ArgumentParser(description="StydeForge Mission Control Web Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()

    log("info", f"Mission Control starting on http://{args.host}:{args.port}")
    server = HTTPServer((args.host, args.port), DashboardHandler)
    print(f"\n  STYDEFORGE MISSION CONTROL")
    print(f"  =========================")
    print(f"  URL: http://{args.host}:{args.port}")
    print(f"  Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
