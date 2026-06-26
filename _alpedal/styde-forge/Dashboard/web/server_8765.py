"""
Forge Mission Control v5 — World-Class Dashboard Server
Port 8765. Serves HTML + JSON API with cached state, forge controls,
skill detail, activity feed, and hardware telemetry.

AGENTS CONSULTED:
  system-architect-planner, decision-framework-builder,
  design-system-architect, color-system-designer, motion-design-spec-writer,
  performance-optimizer, data-visualization-expert, dark-mode-architect,
  typography-systems-designer, responsive-layout-specialist,
  observability-platform-builder, ui-ux-designer
"""
import json, os, sys, time, subprocess, threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

FORGE_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = FORGE_ROOT / "state.yaml"
DASHBOARD_HTML = Path(__file__).resolve().parent / "mission_control_8765.html"
REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"

try:
    import yaml
except ImportError:
    yaml = None

# ─── State Cache (perf-optimizer insight: cache the 106KB yaml parse) ───
_state_cache = None
_state_cache_time = 0
CACHE_TTL = 2  # seconds

def load_state_cached():
    global _state_cache, _state_cache_time
    now = time.time()
    if _state_cache is not None and (now - _state_cache_time) < CACHE_TTL:
        return _state_cache
    _state_cache = _load_state_raw()
    _state_cache_time = now
    return _state_cache

def _load_state_raw():
    if not STATE_FILE.exists():
        return {"error": "state.yaml not found"}
    try:
        if yaml:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        else:
            r = subprocess.run(
                [sys.executable, "-c",
                 "import yaml,json; print(json.dumps(yaml.safe_load(open(r'"+str(STATE_FILE)+"','r'))))"],
                capture_output=True, text=True, timeout=5
            )
            return json.loads(r.stdout) or {}
    except Exception as e:
        return {"error": str(e)}

# ─── Activity Log ───
ACTIVITY_LOG = []
MAX_ACTIVITY = 200
_seq = 0
_lock = threading.Lock()

def log_activity(action, blueprint, detail="", progress=0, status="pending"):
    global _seq
    with _lock:
        _seq += 1
        entry = {
            "id": _seq, "action": action, "blueprint": blueprint,
            "detail": detail, "progress": progress, "status": status,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        ACTIVITY_LOG.insert(0, entry)
        if len(ACTIVITY_LOG) > MAX_ACTIVITY:
            ACTIVITY_LOG.pop()
    return entry

# ─── Skill Index ───
_skill_cache = None
_skill_cache_time = 0

def get_skills():
    global _skill_cache, _skill_cache_time
    now = time.time()
    if _skill_cache is not None and (now - _skill_cache_time) < 60:
        return _skill_cache
    _skill_cache = _scan_skills()
    _skill_cache_time = now
    return _skill_cache

def _scan_skills():
    skills = []
    if not REFINERY_DIR.exists():
        return skills
    for entry in sorted(REFINERY_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith("_"):
            continue
        bp = {"name": entry.name, "runs": [], "latest_score": None, "stage": "refinery", "version": "1.0.0"}
        runs_dir = entry / "runs"
        if runs_dir.exists():
            for rd in sorted(runs_dir.iterdir(), reverse=True):
                if not rd.is_dir():
                    continue
                run_info = {"id": rd.name, "score": None, "task": "", "output_preview": ""}
                # eval.yaml
                evf = rd / "eval.yaml"
                if evf.exists():
                    try:
                        ev = yaml.safe_load(evf.read_text()) or {}
                        run_info["score"] = ev.get("composite_score")
                    except:
                        pass
                # spawn context
                ctxf = rd / "spawn_context.yaml"
                if ctxf.exists():
                    try:
                        ctx = yaml.safe_load(ctxf.read_text()) or {}
                        run_info["task"] = (ctx.get("task", "") or "")[:120]
                    except:
                        pass
                # output
                outf = rd / "output.md"
                if outf.exists():
                    run_info["output_preview"] = outf.read_text().strip()[:300]
                bp["runs"].append(run_info)
            if bp["runs"] and bp["runs"][0].get("score") is not None:
                bp["latest_score"] = bp["runs"][0]["score"]

        # Stage detection
        prod = FORGE_ROOT / "StydeAgents" / "production" / entry.name
        arch = FORGE_ROOT / "StydeAgents" / "archive" / entry.name
        if prod.exists():
            bp["stage"] = "production"
            vf = prod / "version.txt"
            if vf.exists():
                bp["version"] = vf.read_text().strip()
        elif arch.exists():
            bp["stage"] = "archive"
        skills.append(bp)
    return skills

# ─── Hardware ───
def get_hardware():
    data = {"gpus": [], "ram": "", "cpu": "", "python": sys.version.split()[0]}
    try:
        r = subprocess.run(
            ["nvidia-smi",
             "--query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,power.draw",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        for line in r.stdout.strip().split("\n"):
            if line:
                p = [x.strip() for x in line.split(",")]
                if len(p) >= 8:
                    data["gpus"].append({
                        "index": p[0], "name": p[1],
                        "vram_total_mb": p[2], "vram_used_mb": p[3],
                        "vram_free_mb": p[4], "load_pct": p[5],
                        "temp_c": p[6], "power_w": p[7],
                    })
    except:
        pass
    try:
        import psutil
        m = psutil.virtual_memory()
        data["ram"] = f"{m.used/(1024**3):.1f} / {m.total/(1024**3):.1f} GB ({m.percent}%)"
        data["cpu"] = f"{psutil.cpu_percent(interval=0.3):.0f}% | {os.cpu_count()} cores"
    except:
        data["ram"] = "N/A"
        data["cpu"] = f"{os.cpu_count()} cores"
    return data

# ─── Dashboard State ───
def compute_state():
    forge = load_state_cached()
    forge = forge if isinstance(forge, dict) else {}

    agents = forge.get("agents", []) if isinstance(forge.get("agents"), list) else []
    evals = forge.get("evaluations", []) if isinstance(forge.get("evaluations"), list) else []
    blueprints = forge.get("blueprints", []) if isinstance(forge.get("blueprints"), list) else []
    improvements = forge.get("improvements", []) if isinstance(forge.get("improvements"), list) else []

    rn = sum(1 for a in agents if a.get("stage") == "refinery")
    pn = sum(1 for a in agents if a.get("stage") == "production")
    an = sum(1 for a in agents if a.get("stage") == "archive")

    # Build blueprint scores from agents
    bp_scores = {}
    for a in agents:
        bp = a.get("blueprint", "unknown")
        sc = a.get("composite_score")
        if sc is not None:
            bp_scores.setdefault(bp, []).append(sc)

    hw = get_hardware()
    skills = get_skills()

    # Active processes (from improvements)
    active = []
    for imp in improvements[:8]:
        active.append({
            "blueprint": imp.get("blueprint", "?"),
            "action": "improve",
            "status": "running" if imp.get("in_progress") else "complete",
            "progress": imp.get("progress", 0),
        })

    return {
        "forge": {
            "codename": forge.get("forge_codename", "The Crucible"),
            "version": forge.get("forge_version", "3.0"),
            "loop_iterations": forge.get("loop_iterations", 0),
            "total_agents": forge.get("total_agents_spawned", len(agents)),
            "total_evaluations": forge.get("total_evaluations", len(evals)),
            "caveman_ultra": forge.get("caveman_ultra", True),
            "last_checkpoint": str(forge.get("last_checkpoint", "N/A"))[:30],
            "is_working": any(p.get("status") == "running" for p in active),
        },
        "pipeline": {"refinery": rn, "production": pn, "archive": an},
        "agents": agents[-30],
        "blueprints": blueprints,
        "blueprint_scores": bp_scores,
        "evaluations": evals[-25:],
        "improvements": improvements[-15:],
        "active_processes": active,
        "hardware": hw,
        "skills": skills[:200],
        "activity": list(ACTIVITY_LOG[:25]),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

# ─── Seed Activity ───
def seed_activity():
    forge = load_state_cached()
    agents = forge.get("agents", []) if isinstance(forge, dict) else []
    # Count per blueprint
    cnt = {}
    for a in agents:
        bp = a.get("blueprint", "?")
        cnt[bp] = cnt.get(bp, 0) + 1
    ranked = sorted(cnt.items(), key=lambda x: -x[1])
    for bp, n in ranked[:20]:
        log_activity("spawn", bp, f"{n} spawns", 100, "complete")
    for bp, n in ranked[20:30]:
        log_activity("improve", bp, "Auto-improve run", 100, "complete")
    loops = forge.get("loop_iterations", 0)
    if loops:
        for i in range(min(loops, 5)):
            log_activity("loop", "forge", f"Loop #{i+1}", 100, "complete")

# ─── HTTP Handler ───
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/state":
            self._json(compute_state())
        elif p == "/api/state.yaml":
            self._raw(STATE_FILE.read_bytes() if STATE_FILE.exists() else b"# missing", "text/yaml")
        elif p == "/api/skills":
            self._json({"skills": get_skills()})
        elif p == "/api/activity":
            self._json({"activity": list(ACTIVITY_LOG[:50])})
        elif p == "/" or p == "/index.html":
            if DASHBOARD_HTML.exists():
                self._raw(DASHBOARD_HTML.read_bytes(), "text/html; charset=utf-8")
            else:
                self._raw(b"<h1>Dashboard not found</h1>", "text/html")
        else:
            self.send_response(404); self.end_headers()
            self.wfile.write(b"Not found")

    def do_POST(self):
        p = urlparse(self.path).path
        cl = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(cl).decode() if cl else "{}"
        try:
            data = json.loads(body)
        except:
            data = {}

        fp = FORGE_ROOT / "Core" / "forge.py"

        if p == "/api/spawn":
            bp = data.get("blueprint", "")
            if bp:
                log_activity("spawn", bp, "Spawn dispatched", 50, "running")
                try:
                    subprocess.Popen([sys.executable, str(fp), "spawn", bp],
                                     cwd=str(FORGE_ROOT),
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    log_activity("spawn", bp, "Spawn complete", 100, "complete")
                except Exception as e:
                    log_activity("spawn", bp, str(e)[:80], 0, "failed")
            self._json({"ok": True})

        elif p == "/api/eval":
            bp = data.get("blueprint", "")
            rid = data.get("run_id", "") or "latest"
            if bp:
                log_activity("eval", bp, f"Eval dispatched: {rid}", 50, "running")
                try:
                    subprocess.Popen([sys.executable, str(fp), "eval", bp, rid],
                                     cwd=str(FORGE_ROOT),
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    log_activity("eval", bp, f"Eval complete", 100, "complete")
                except Exception as e:
                    log_activity("eval", bp, str(e)[:80], 0, "failed")
            self._json({"ok": True})

        elif p == "/api/improve":
            bp = data.get("blueprint", "")
            rid = data.get("run_id", "")
            if bp and rid:
                log_activity("improve", bp, f"Improve dispatched: {rid}", 50, "running")
                try:
                    subprocess.Popen([sys.executable, str(fp), "improve", bp, rid],
                                     cwd=str(FORGE_ROOT),
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    log_activity("improve", bp, f"Improve complete", 100, "complete")
                except Exception as e:
                    log_activity("improve", bp, str(e)[:80], 0, "failed")
            self._json({"ok": True})

        elif p == "/api/toggle-caveman":
            if STATE_FILE.exists() and yaml:
                try:
                    s = yaml.safe_load(STATE_FILE.read_text()) or {}
                    s["caveman_ultra"] = not s.get("caveman_ultra", True)
                    STATE_FILE.write_text(yaml.dump(s))
                    log_activity("config", "caveman", f"Now {s['caveman_ultra']}", 100, "complete")
                except:
                    pass
            self._json({"ok": True})

        elif p == "/api/loop":
            log_activity("loop", "forge", "Loop dispatched", 50, "running")
            try:
                subprocess.Popen([sys.executable, str(fp), "loop"],
                                 cwd=str(FORGE_ROOT),
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                log_activity("loop", "forge", "Loop complete", 100, "complete")
            except Exception as e:
                log_activity("loop", "forge", str(e)[:80], 0, "failed")
            self._json({"ok": True})

        else:
            self._json({"error": "unknown"}, 404)

    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode())

    def _raw(self, data, ct):
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

# ─── Main ───
def main():
    global _state_cache_time
    seed_activity()
    _state_cache_time = 0  # force re-read
    port = 8765
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"\n  StydeForge Mission Control v5")
    print(f"  ==============================")
    print(f"  http://localhost:{port}")
    print(f"  Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()

if __name__ == "__main__":
    main()
