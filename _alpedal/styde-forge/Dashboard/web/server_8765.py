"""
Forge Mission Control — Dashboard Server (port 8765)
Serves the dashboard and a /api/state endpoint with live Forge + hardware data.
"""
import json
import os
import sys
import time
import subprocess
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

FORGE_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = FORGE_ROOT / "state.yaml"
DASHBOARD_HTML = Path(__file__).resolve().parent / "mission_control_8765.html"

try:
    import yaml
except ImportError:
    yaml = None


def load_state():
    """Load Forge state from state.yaml."""
    if not STATE_FILE.exists():
        return {"error": "state.yaml not found", "path": str(STATE_FILE)}
    try:
        if yaml:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        else:
            import subprocess
            r = subprocess.run(
                [sys.executable, "-c", "import yaml,json; print(json.dumps(yaml.safe_load(open(r'" + str(STATE_FILE) + "','r'))))"],
                capture_output=True, text=True
            )
            return json.loads(r.stdout)
    except Exception as e:
        return {"error": str(e), "path": str(STATE_FILE)}


def get_hardware():
    """Get GPU, RAM, CPU info."""
    data = {"gpus": [], "ram": "", "cpu": "", "python": sys.version.split()[0]}
    try:
        # GPU via nvidia-smi
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,power.draw",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        for line in r.stdout.strip().split("\n"):
            if line:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) >= 8:
                    data["gpus"].append({
                        "index": parts[0],
                        "name": parts[1],
                        "vram_total_mb": parts[2],
                        "vram_used_mb": parts[3],
                        "vram_free_mb": parts[4],
                        "load_pct": parts[5],
                        "temp_c": parts[6],
                        "power_w": parts[7],
                    })
    except Exception:
        pass

    try:
        import psutil
        mem = psutil.virtual_memory()
        data["ram"] = f"{mem.used / (1024**3):.1f} / {mem.total / (1024**3):.1f} GB ({mem.percent}%)"
        data["cpu"] = f"{psutil.cpu_percent(interval=0.5):.1f}% | {os.cpu_count()} cores"
    except ImportError:
        data["ram"] = "psutil not installed"
        data["cpu"] = f"{os.cpu_count()} cores (no load data)"

    return data


def compute_dashboard_state():
    """Merge Forge state + hardware into one JSON payload for the dashboard."""
    forge = load_state()

    # Compute derived stats
    agents = forge.get("agents", []) if isinstance(forge, dict) else []
    evaluations = forge.get("evaluations", []) if isinstance(forge, dict) else []
    blueprints = forge.get("blueprints", []) if isinstance(forge, dict) else []
    improvements = forge.get("improvements", []) if isinstance(forge, dict) else []

    refinery_count = sum(1 for a in agents if a.get("stage") == "refinery")
    production_count = sum(1 for a in agents if a.get("stage") == "production")
    archive_count = sum(1 for a in agents if a.get("stage") == "archive")

    # Score distribution by blueprint
    blueprint_scores = {}
    for ev in evaluations:
        bp = ev.get("blueprint", "unknown")
        score = ev.get("composite_score", 0)
        if bp not in blueprint_scores:
            blueprint_scores[bp] = []
        blueprint_scores[bp].append(score)

    # Agent status breakdown
    status_counts = {}
    for a in agents:
        s = a.get("status", "unknown")
        status_counts[s] = status_counts.get(s, 0) + 1

    hardware = get_hardware()

    return {
        "forge": {
            "codename": forge.get("forge_codename", "The Crucible"),
            "version": forge.get("forge_version", "3.0.0"),
            "loop_iterations": forge.get("loop_iterations", 0),
            "total_agents": forge.get("total_agents_spawned", len(agents)),
            "total_evaluations": forge.get("total_evaluations", len(evaluations)),
            "caveman_ultra": forge.get("caveman_ultra", True),
            "last_checkpoint": forge.get("last_checkpoint", "N/A"),
            "last_checkpoint_at": forge.get("last_checkpoint_at", ""),
        },
        "pipeline": {
            "refinery": refinery_count,
            "production": production_count,
            "archive": archive_count,
        },
        "agents": agents[-50:],  # Last 50 agents
        "blueprints": blueprints,
        "blueprint_scores": blueprint_scores,
        "evaluations": evaluations[-30:],  # Last 30 evaluations
        "improvements": improvements[-20:],
        "status_counts": status_counts,
        "hardware": hardware,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


class DashboardHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress log noise

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            state = compute_dashboard_state()
            self.wfile.write(json.dumps(state, indent=2, default=str).encode())

        elif path == "/api/state.yaml":
            # Raw state.yaml for debugging
            self.send_response(200)
            self.send_header("Content-Type", "text/yaml")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            if STATE_FILE.exists():
                self.wfile.write(STATE_FILE.read_bytes())
            else:
                self.wfile.write(b"# state.yaml not found")

        elif path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            if DASHBOARD_HTML.exists():
                self.wfile.write(DASHBOARD_HTML.read_bytes())
            else:
                self.wfile.write(b"<h1>Dashboard not found. Run build step first.</h1>")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")


def main():
    port = 8765
    server = HTTPServer(("127.0.0.1", port), DashboardHandler)
    print(f"\n  StydeForge Mission Control")
    print(f"  ==========================")
    print(f"  Server: http://localhost:{port}")
    print(f"  API:    http://localhost:{port}/api/state")
    print(f"  Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()


if __name__ == "__main__":
    main()
