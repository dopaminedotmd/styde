"""
Styde Forge Dashboard v5 — Mission Control + Engine Command Center.
Run: python Core/dashboard.py  |  Open: http://localhost:8765

Features: 4 themes · GPU gauges · Agent modals · Engine counter · XP bars
NEW in v5: Engine Control Panel — start/stop forge loops, configure blueprints,
adjust concurrency, live process management from the dashboard.

Architecture:
  - SSE stream for real-time monitoring data
  - REST API endpoints for engine control actions
  - Subprocess management for forge engine lifecycle
"""
import json, os, yaml, time, glob, signal, subprocess, threading
from pathlib import Path
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue
from urllib.parse import urlparse, parse_qs

FORGE_ROOT = Path(__file__).resolve().parent.parent
PORT = 8765

sse_clients: list[Queue] = []
sse_lock = threading.Lock()
engine_lock = threading.Lock()

# Registry of running forge engine processes: pid -> {blueprint, benchmark, started_at, process}
running_engines: dict[int, dict] = {}


def broadcast(data: str):
    with sse_lock:
        dead = [q for q in sse_clients if not q.put_nowait(data)]
        for q in dead: sse_clients.remove(q)


# ═══════════════════════════════════════════════════════════════
# DATA FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def load_state():
    path = FORGE_ROOT / "state.yaml"
    if not path.exists(): return {}
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def get_forge_status() -> dict:
    lock_file = FORGE_ROOT / ".forge.lock"
    state = load_state()
    if not lock_file.exists():
        if state.get("total_agents_spawned", 0) > 0:
            return {"status": "sleeping", "label": "SLEEPING", "color": "#c0a030", "css_class": "forge-sleeping"}
        return {"status": "off", "label": "OFFLINE", "color": "#e04040", "css_class": "forge-off"}
    try:
        data = json.loads(lock_file.read_text(encoding="utf-8"))
        pid = data.get("pid", 0)
        if pid > 0:
            try: os.kill(pid, 0); return {"status": "running", "label": "RUNNING", "color": "#30c050", "css_class": "forge-running"}
            except OSError: pass
    except: pass
    return {"status": "crashed", "label": "CRASHED", "color": "#e04040", "css_class": "forge-crashed"}

def get_engine_info() -> list:
    """Get detailed info on all managed engine processes."""
    with engine_lock:
        result = []
        for pid, info in list(running_engines.items()):
            alive = False
            try: os.kill(pid, 0); alive = True
            except OSError: pass
            result.append({
                "pid": pid,
                "blueprint": info.get("blueprint", "?"),
                "benchmark": info.get("benchmark", "manual"),
                "started": info.get("started", "?"),
                "alive": alive,
                "status": "running" if alive else "dead",
            })
        # Also scan for orphan forge lock files
        for lf in FORGE_ROOT.glob(".forge.lock*"):
            try:
                d = json.loads(lf.read_text(encoding="utf-8"))
                opid = d.get("pid", 0)
                if opid > 0 and opid not in running_engines:
                    alive = False
                    try: os.kill(opid, 0); alive = True
                    except OSError: pass
                    if alive:
                        result.append({"pid": opid, "blueprint": d.get("blueprint","?"), "benchmark": d.get("benchmark","manual"),
                                       "started": d.get("acquired","?"), "alive": True, "status": "external"})
            except: pass
        return result

def get_engine_count() -> dict:
    engines = get_engine_info()
    running = sum(1 for e in engines if e["alive"])
    try:
        out = subprocess.run(["tasklist","/FI","IMAGENAME eq python.exe","/FO","CSV"], capture_output=True, text=True, timeout=5, errors='replace')
        py_count = out.stdout.count("python.exe")
    except: py_count = 0
    return {"engines": running, "python_processes": py_count, "processes": engines}

def get_gpu_info() -> list:
    gpus = []
    try:
        r = subprocess.run(["nvidia-smi","--query-gpu=index,name,memory.total,utilization.gpu,temperature.gpu,memory.used",
                           "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=10, errors='replace')
        if r.returncode == 0:
            for line in r.stdout.strip().split("\n"):
                if line.strip():
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) >= 6:
                        gpus.append({"idx": int(parts[0]), "name": parts[1], "vram_total": round(float(parts[2])/1024,1),
                                     "vram_used": round(float(parts[5])/1024,1), "load": int(float(parts[3])), "temp": int(float(parts[4]))})
    except: pass
    return gpus

def compute_training_pct(agent: dict) -> tuple:
    stage = agent.get("stage","refinery"); status = agent.get("status","?")
    if stage == "production": return 100, "PRODUCTION"
    if stage == "archive": return 100, "ARCHIVED"
    if status == "spawned": return 25, "Spawning..."
    if status == "completed": return 50, "Awaiting eval"
    version = agent.get("version","1.0.0")
    try: parts = version.split("."); major = int(parts[0]); minor = int(parts[1]) if len(parts)>1 else 0
    except: major, minor = 1, 0
    pct = min(55 + (max(major-1,0)*2+minor)*10, 95)
    return pct, f"Training... (v{version})"

def get_recent_agents(state):
    agents = state.get("agents",[]); evals = state.get("evaluations",[]); improvements = state.get("improvements",[])
    recent = sorted(agents, key=lambda a: a.get("spawned_at",""), reverse=True)[:30]
    result = []
    for a in recent:
        score = None; eval_detail = None
        for e in evals:
            if e.get("run_id") == a.get("run_id"): score = e.get("composite_score"); eval_detail = e; break
        teacher_diag = ""; teacher_detail = None
        for imp in improvements:
            if imp.get("run_id") == a.get("run_id"): teacher_diag = (imp.get("diagnosis","") or imp.get("summary","")); teacher_detail = imp; break
        training_pct, training_label = compute_training_pct(a)
        result.append({"run_id": a.get("run_id","?")[:15], "blueprint": a.get("blueprint","?"), "stage": a.get("stage","?"),
                       "status": a.get("status","?"), "score": score, "spawned": (a.get("spawned_at","") or "")[:16],
                       "teacher": teacher_diag[:80], "version": a.get("version",""), "benchmark": a.get("benchmark","?"),
                       "training_pct": training_pct, "training_label": training_label, "eval": eval_detail, "improvement": teacher_detail})
    return result

def get_blueprints():
    bp_dir = FORGE_ROOT / "blueprints"
    if not bp_dir.exists(): return []
    bps = []
    for d in sorted(bp_dir.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            cfg = d / "config.yaml"; version = "?"; domain = ""
            if cfg.exists():
                try: c = yaml.safe_load(cfg.read_text(encoding="utf-8")); bp = c.get("blueprint",{}); version = bp.get("version","?"); domain = bp.get("domain","")
                except: pass
            bps.append({"name": d.name, "version": str(version), "domain": domain})
    return bps

def get_checkpoints():
    cp_dir = FORGE_ROOT / "checkpoints"
    if not cp_dir.exists(): return []
    cps = []
    for cp in sorted(cp_dir.glob("checkpoint-*"), reverse=True)[:10]:
        if cp.name.startswith("."): continue
        m = cp / "checkpoint_manifest.json"
        if m.exists():
            d = json.loads(m.read_text(encoding="utf-8")); cps.append({"id": cp.name[:35], "created": d.get("created","?")[:19], "label": d.get("label",""), "loops": d.get("loop_iterations",0)})
    return cps

def get_latest_output():
    refinery = FORGE_ROOT / "StydeAgents" / "refinery"
    if not refinery.exists(): return None
    runs = []
    for bp_dir in refinery.iterdir():
        if not bp_dir.is_dir(): continue
        rd = bp_dir / "runs"
        if not rd.exists(): continue
        for run_dir in sorted(rd.glob("run-*"), reverse=True):
            output = run_dir / "output.md"
            if output.exists(): runs.append((run_dir.name, bp_dir.name, output.read_text(encoding="utf-8")[:1000], output.stat().st_mtime)); break
    if not runs: return None
    runs.sort(key=lambda r: r[3], reverse=True); return runs[0]

def get_leaderboard(state):
    agents = state.get("agents",[]); evals = state.get("evaluations",[])
    scored = [{"blueprint": a.get("blueprint","?"), "score": e.get("composite_score",0), "run_id": a.get("run_id","?")[:12]}
              for a in agents if a.get("stage")=="production"
              for e in evals if e.get("run_id")==a.get("run_id")]
    scored.sort(key=lambda x: x["score"], reverse=True); return scored[:10]

def get_system_health():
    import psutil
    return {"cpu": psutil.cpu_percent(interval=0.1), "ram_pct": psutil.virtual_memory().percent,
            "ram_gb": round(psutil.virtual_memory().used/(1024**3),1), "ram_total": round(psutil.virtual_memory().total/(1024**3),1),
            "disk_pct": psutil.disk_usage(str(FORGE_ROOT)).percent, "disk_free": round(psutil.disk_usage(str(FORGE_ROOT)).free/(1024**3),1)}

def get_scores(state):
    return [e.get("composite_score",0) for e in state.get("evaluations",[])[-60:]]

def get_benchmarks():
    bm_dir = FORGE_ROOT / "eval" / "benchmarks"
    if not bm_dir.exists(): return []
    return [d.name for d in sorted(bm_dir.iterdir()) if d.is_dir()]

def build_state_json():
    state = load_state()
    agents_list = state.get("agents",[])
    refinery = sum(1 for a in agents_list if a.get("stage")=="refinery")
    production = sum(1 for a in agents_list if a.get("stage")=="production")
    archive = sum(1 for a in agents_list if a.get("stage")=="archive")
    scores = get_scores(state)
    return json.dumps({
        "ts": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        "version": state.get("forge_version","?"), "hardware": state.get("hardware_profile","?"),
        "caveman": state.get("caveman_ultra",False), "loops": state.get("loop_iterations",0),
        "spawned": state.get("total_agents_spawned",0), "evaluations": state.get("total_evaluations",0),
        "refinery": refinery, "production": production, "archive": archive,
        "last_checkpoint": (state.get("last_checkpoint") or "")[:35],
        "scores": scores, "score_avg": round(sum(scores)/len(scores),1) if scores else 0,
        "score_max": max(scores) if scores else 0, "score_min": min(scores) if scores else 0,
        "score_trend": "up" if len(scores)>=2 and scores[-1]>scores[-2] else ("down" if len(scores)>=2 and scores[-1]<scores[-2] else "flat"),
        "checkpoints": get_checkpoints(), "agents": get_recent_agents(state),
        "blueprints": get_blueprints(), "benchmarks": get_benchmarks(), "leaderboard": get_leaderboard(state),
        "health": get_system_health(), "latest_output": None,
        "forge_status": get_forge_status(), "engines": get_engine_count(), "gpus": get_gpu_info(),
    })

def sse_broadcaster():
    while True:
        try: broadcast(f"data: {build_state_json()}\n\n")
        except: pass
        time.sleep(2)


# ═══════════════════════════════════════════════════════════════
# ENGINE CONTROL — Process Management
# ═══════════════════════════════════════════════════════════════

def start_engine(blueprint: str, benchmark: str = "manual") -> dict:
    """Spawn a forge engine as a subprocess. Returns {success, pid, blueprint, message}."""
    import sys
    cmd = [sys.executable, str(FORGE_ROOT / "Core" / "forge.py"), "loop", blueprint]
    if benchmark and benchmark != "manual":
        cmd.append(benchmark)
    try:
        proc = subprocess.Popen(cmd, cwd=str(FORGE_ROOT),
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0)
        pid = proc.pid
        started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with engine_lock:
            running_engines[pid] = {"blueprint": blueprint, "benchmark": benchmark, "started": started, "process": proc}
        return {"success": True, "pid": pid, "blueprint": blueprint, "benchmark": benchmark, "message": f"Engine started: {blueprint} (PID {pid})"}
    except Exception as e:
        return {"success": False, "pid": 0, "message": str(e)}

def stop_engine(pid: int) -> dict:
    """Stop a specific engine by PID."""
    with engine_lock:
        info = running_engines.pop(pid, None)
    if not info:
        # Try to kill anyway
        try: os.kill(pid, signal.SIGTERM); return {"success": True, "pid": pid, "message": f"Killed PID {pid}"}
        except OSError: return {"success": False, "pid": pid, "message": f"No such engine: PID {pid}"}
    proc = info.get("process")
    try:
        if os.name == 'nt':
            subprocess.run(["taskkill", "/PID", str(pid), "/F", "/T"], capture_output=True, timeout=10)
        else:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
    except: pass
    return {"success": True, "pid": pid, "blueprint": info.get("blueprint","?"), "message": f"Engine stopped: {info.get('blueprint','?')} (PID {pid})"}

def stop_all_engines() -> dict:
    pids = list(running_engines.keys())
    results = [stop_engine(pid) for pid in pids]
    return {"success": True, "stopped": len(results), "results": results}


# ═══════════════════════════════════════════════════════════════
# HTML TEMPLATE
# ═══════════════════════════════════════════════════════════════

HTML_PATH = FORGE_ROOT / "Dashboard" / "mission-control.html"
if HTML_PATH.exists():
    HTML = HTML_PATH.read_text(encoding="utf-8")
else:
    HTML = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Styde Forge — Command Center v5</title>
<style>
:root {
  --bg: #060612; --card: #0c0c22; --border: #1a1a40; --text: #b0b0c8; --dim: #505080;
  --accent: #5060e0; --accent2: #7060f0; --green: #30c050; --yellow: #c0a030; --red: #e04040; --blue: #4080ff;
  --xp-bg: #0d0d28; --xp-full: #30c050; --xp-training: #4070e0; --xp-spawn: #4040a0; --xp-eval: #808030; --xp-archive: #303040;
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-xl: 16px;
  --shadow-card: 0 2px 8px rgba(0,0,0,0.3); --shadow-modal: 0 8px 32px rgba(0,0,0,0.6);
  --transition-fast: 150ms ease; --transition-base: 250ms ease; --transition-slow: 400ms ease;
  font-family: 'Segoe UI','Inter',system-ui,sans-serif; font-size: 13px; line-height: 1.5;
}
[data-theme="light"] { --bg: #f0f2f8; --card: #fff; --border: #d8dae8; --text: #1a1a3a; --dim: #8888aa; --green: #18a040; --yellow: #b09020; --red: #d03030; --blue: #3068e0; --xp-bg: #e8eaf0; --xp-archive: #c8cad0; --shadow-card: 0 1px 4px rgba(0,0,0,0.08); --shadow-modal: 0 4px 24px rgba(0,0,0,0.15); }
[data-theme="oled"] { --bg: #000; --card: #0a0a10; --border: #1a1a28; --text: #c0c0d0; --dim: #484878; --accent: #6070ff; --green: #20d060; --blue: #5090ff; --xp-bg: #0a0a16; }
[data-theme="forest"] { --bg: #0f1410; --card: #182018; --border: #283428; --text: #b8c8b8; --dim: #588058; --accent: #40b860; --green: #40d060; --yellow: #c0b030; --red: #e05040; --blue: #4088e0; --xp-bg: #142018; }
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);padding:16px;transition:background var(--transition-slow),color var(--transition-slow);min-height:100vh}
h1{font-size:22px;font-weight:700;color:#d0d0f0;letter-spacing:-.5px}h1 span{color:var(--accent)}
.sub{color:var(--dim);font-size:11px;margin-bottom:14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}

/* Tabs */
.tabs{display:flex;gap:0;margin-bottom:14px}
.tab-btn{padding:6px 16px;border:1px solid var(--border);background:var(--card);color:var(--dim);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1px;cursor:pointer;transition:all var(--transition-fast)}
.tab-btn:first-child{border-radius:var(--radius-sm) 0 0 var(--radius-sm)}
.tab-btn:last-child{border-radius:0 var(--radius-sm) var(--radius-sm) 0}
.tab-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.tab-panel{display:none}.tab-panel.active{display:block}

/* Status bar */
.forge-status{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;padding:3px 10px;border-radius:12px;background:var(--card);border:1px solid var(--border)}
.forge-status .orb{width:10px;height:10px;border-radius:50%;display:inline-block}
.forge-running .orb{animation:pulse 1.2s infinite}.forge-sleeping .orb{animation:pulse 3s infinite}
.forge-running{color:var(--green);border-color:rgba(48,192,80,.3)}.forge-running .orb{background:var(--green)}
.forge-sleeping{color:var(--yellow);border-color:rgba(192,160,48,.3)}.forge-sleeping .orb{background:var(--yellow)}
.forge-off .orb,.forge-crashed .orb{background:var(--red)}
.forge-off,.forge-crashed{color:var(--red);border-color:rgba(224,64,64,.3)}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 8px currentColor}50%{opacity:.3;box-shadow:0 0 2px currentColor}}

.engine-counter{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:700;color:var(--dim);padding:3px 10px;border-radius:12px;background:var(--card);border:1px solid var(--border)}
.engine-counter .eng-num{color:var(--accent);font-size:14px}

.theme-toggle{display:inline-flex;gap:4px;margin-left:auto}
.theme-btn{width:22px;height:22px;border-radius:50%;border:2px solid var(--border);cursor:pointer;transition:transform .15s,border-color .15s;padding:0}
.theme-btn:hover{transform:scale(1.15);border-color:var(--accent)}
.theme-btn.active{border-color:var(--accent);box-shadow:0 0 6px var(--accent)}
.btn-dark{background:#1a1b1e}.btn-light{background:#fff}.btn-oled{background:#000;border-color:#333}.btn-forest{background:#2d4a2d}

/* KPI */
.kpi-row{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-md);padding:10px 16px;min-width:90px;text-align:center;transition:transform .2s,box-shadow .2s}
.kpi:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(80,96,224,.15)}
.kpi .num{font-size:24px;font-weight:800;color:#e8e8f8}
.kpi .lbl{font-size:9px;color:var(--dim);text-transform:uppercase;letter-spacing:1.5px;margin-top:2px}
.kpi-ok{border-color:rgba(48,192,80,.2)}.kpi-ok .num{color:var(--green)}
.kpi-warn{border-color:rgba(192,160,48,.2)}.kpi-warn .num{color:var(--yellow)}
.kpi-blue{border-color:rgba(64,128,255,.2)}.kpi-blue .num{color:var(--blue)}

/* Control Panel */
.ctrl-panel{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-md);padding:16px;margin-bottom:12px}
.ctrl-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:8px}
.ctrl-row:last-child{margin-bottom:0}
.ctrl-label{font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:1px;min-width:60px}
.ctrl-select,.ctrl-input{background:var(--xp-bg);border:1px solid var(--border);color:var(--text);padding:6px 10px;border-radius:var(--radius-sm);font-size:11px;min-width:160px}
.ctrl-select:focus,.ctrl-input:focus{outline:none;border-color:var(--accent)}
.ctrl-btn{padding:6px 16px;border:none;border-radius:var(--radius-sm);font-size:11px;font-weight:600;cursor:pointer;transition:all var(--transition-fast);text-transform:uppercase;letter-spacing:.5px}
.btn-start{background:var(--green);color:#000}.btn-start:hover{background:#40e060;box-shadow:0 0 12px rgba(48,192,80,.4)}
.btn-stop{background:var(--red);color:#fff}.btn-stop:hover{background:#f05050;box-shadow:0 0 12px rgba(224,64,64,.4)}
.btn-stop-all{background:#802020;color:#ff8888}
.engine-count{display:flex;align-items:center;gap:6px}
.engine-count input[type=range]{width:80px;accent-color:var(--accent)}
.engine-count .count-display{font-size:18px;font-weight:700;color:var(--accent);min-width:20px;text-align:center}

/* Engine process list */
.engine-list{margin-top:8px}
.eng-item{display:flex;align-items:center;gap:8px;padding:6px 10px;background:var(--xp-bg);border-radius:var(--radius-sm);margin-bottom:4px;font-size:11px}
.eng-item .eng-pid{color:var(--accent);font-weight:700;min-width:50px}
.eng-item .eng-bp{color:var(--text);flex:1}
.eng-item .eng-started{color:var(--dim);font-size:10px}
.eng-item .eng-status{font-size:9px;font-weight:700;text-transform:uppercase;padding:2px 8px;border-radius:10px}
.eng-status-running{background:rgba(48,192,80,.15);color:var(--green)}
.eng-status-dead{background:rgba(224,64,64,.15);color:var(--red)}
.eng-item .eng-kill{background:none;border:1px solid var(--red);color:var(--red);font-size:9px;padding:2px 8px;border-radius:3px;cursor:pointer;transition:all var(--transition-fast)}
.eng-item .eng-kill:hover{background:var(--red);color:#fff}

/* Grid */
.grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:12px;max-width:1500px;margin-bottom:12px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:1500px}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-md);padding:14px}
.card h2{color:#7070c0;font-size:10px;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center}
.card h2 .subtitle{font-size:9px;color:var(--dim);letter-spacing:1px;text-transform:none;font-weight:400}

/* Score chart */
.chart{display:flex;align-items:flex-end;gap:2px;height:80px;position:relative}
.chart .bar{flex:1;min-width:4px;border-radius:2px 2px 0 0;transition:height .3s}
.bar-prod{background:linear-gradient(to top,#2040a0,#4070e0)}.bar-mid{background:linear-gradient(to top,#605020,#a08030)}.bar-low{background:linear-gradient(to top,#602020,#a04040)}
.score-overlay{position:absolute;top:4px;right:4px;font-size:22px;font-weight:800}
.score-up{color:var(--green)}.score-down{color:var(--red)}.score-flat{color:var(--dim)}
.chart-legend{display:flex;gap:14px;margin-top:4px;font-size:10px;color:var(--dim)}
.chart-legend span{display:flex;align-items:center;gap:3px}.chart-legend .swatch{width:10px;height:4px;border-radius:2px}

/* Agent table */
.agent-table{width:100%;font-size:11px;border-collapse:collapse}
.agent-table th{text-align:left;color:var(--dim);font-weight:600;padding:3px 6px;border-bottom:1px solid var(--border);font-size:9px;text-transform:uppercase;letter-spacing:1px}
.agent-table td{padding:4px 6px;border-bottom:1px solid #101028;vertical-align:middle}
.agent-table tr{cursor:pointer;transition:background .15s}
.agent-table tr:hover{background:rgba(80,96,224,.08)}
.score-cell{font-weight:700;font-size:12px}
.badge{display:inline-block;padding:1px 6px;border-radius:3px;font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.badge-prod{background:#0a1a35;color:var(--blue)}.badge-ref{background:#1a1a08;color:var(--yellow)}.badge-arch{background:#1a0a0a;color:var(--red)}

/* XP bar */
.xp-cell{min-width:100px}
.xp-bar-wrap{display:flex;align-items:center;gap:4px}
.xp-bar-outer{flex:1;background:var(--xp-bg);border-radius:3px;height:12px;overflow:hidden}
.xp-bar-fill{height:100%;border-radius:3px;transition:width .5s ease}
.xp-bar-label{font-size:8px;color:var(--dim);min-width:50px;text-align:right;white-space:nowrap}
.xp-fill-full{background:var(--xp-full)}
.xp-fill-training{background:linear-gradient(90deg,#3060c0,var(--xp-training),#3060c0);background-size:200% 100%;animation:shimmer 2s linear infinite}
.xp-fill-spawn{background:linear-gradient(90deg,#202040,var(--xp-spawn),#202040);background-size:200% 100%;animation:shimmer 1.5s linear infinite}
.xp-fill-eval{background:linear-gradient(90deg,#505020,var(--xp-eval),#505020);background-size:200% 100%;animation:shimmer 2s linear infinite}
.xp-fill-archived{background:var(--xp-archive)}
@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}

/* GPU */
.gpu-item{display:flex;align-items:center;gap:8px;padding:4px 0;border-bottom:1px solid #101028;font-size:11px}
.gpu-item:last-child{border:none}
.gpu-name{color:var(--text);min-width:130px}
.gpu-bar-wrap{flex:1;background:var(--xp-bg);border-radius:3px;height:7px;overflow:hidden}
.gpu-bar{height:100%;border-radius:3px;transition:width .5s}
.gpu-bar-load{background:linear-gradient(to right,#3060c0,#40a0f0)}.gpu-bar-mem{background:linear-gradient(to right,#8050c0,#c080f0)}
.gpu-stat{color:var(--dim);font-size:9px;min-width:55px;text-align:right}
.gpu-temp-ok{color:var(--green)}.gpu-temp-warm{color:var(--yellow)}.gpu-temp-hot{color:var(--red)}

/* Modal */
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:1000;justify-content:center;align-items:flex-start;padding:40px 20px;overflow-y:auto}
.modal-overlay.open{display:flex}
.modal{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:20px;max-width:650px;width:100%;animation:modalIn .25s ease;box-shadow:var(--shadow-modal)}
@keyframes modalIn{from{opacity:0;transform:translateY(20px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
.modal-close{float:right;background:none;border:none;color:var(--dim);font-size:20px;cursor:pointer;padding:2px 8px}
.modal-close:hover{color:var(--text)}
.modal h3{color:var(--accent);font-size:15px;margin-bottom:4px}
.modal h4{color:var(--dim);font-size:10px;text-transform:uppercase;letter-spacing:2px;margin:12px 0 4px}
.modal .meta{color:var(--dim);font-size:11px;margin-bottom:10px}
.modal .eval-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.modal .eval-dim{background:var(--xp-bg);padding:6px 10px;border-radius:var(--radius-sm)}
.modal .eval-dim .dim-label{color:var(--dim);font-size:8px;text-transform:uppercase}
.modal .eval-dim .dim-score{font-size:16px;font-weight:700}
.modal .teacher-box{background:var(--xp-bg);padding:8px 12px;border-radius:var(--radius-sm);font-size:11px;color:var(--text);margin-top:6px;white-space:pre-wrap;max-height:180px;overflow-y:auto;line-height:1.5}
.modal .teacher-box strong{color:var(--accent)}

/* Misc */
.lb-row{display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid #101028;font-size:11px}
.lb-row:last-child{border:none}
.lb-rank{width:20px;height:20px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;margin-right:6px;flex-shrink:0}
.lb-rank-1{background:linear-gradient(135deg,#c0a020,#ffd700);color:#000}.lb-rank-2{background:linear-gradient(135deg,#808090,#c0c0c0);color:#000}.lb-rank-3{background:linear-gradient(135deg,#804020,#cd7f32);color:#fff}.lb-rank-n{background:#181838;color:var(--dim)}
.cp-item{display:flex;justify-content:space-between;font-size:10px;padding:3px 0;border-bottom:1px solid #101028}.cp-item:last-child{border:none}
.bp-grid{display:flex;flex-wrap:wrap;gap:5px;max-height:220px;overflow-y:auto}
.bp-chip{background:#0e0e28;border:1px solid #1a1a40;border-radius:5px;padding:5px 8px;font-size:10px;cursor:pointer;transition:all .2s}
.bp-chip:hover{border-color:var(--accent);background:#121230}
.bp-chip .bp-name{color:#b0b0d0;font-weight:600}.bp-chip .bp-ver{color:var(--accent);font-size:9px;margin-left:4px}
.toast-container{position:fixed;top:14px;right:14px;z-index:9999}
.toast{background:#0c1a0c;border:1px solid #1a3a1a;color:var(--green);padding:8px 14px;border-radius:5px;margin-bottom:5px;font-size:11px;animation:slideIn .3s ease;max-width:280px}
.toast-warn{background:#1a1a08;border-color:#3a3a1a;color:var(--yellow)}.toast-err{background:#1a0a0a;border-color:#3a1a1a;color:var(--red)}
@keyframes slideIn{from{transform:translateX(120%);opacity:0}to{transform:translateX(0);opacity:1}}
.footer{color:#202050;font-size:9px;text-align:center;margin-top:16px;letter-spacing:1px}
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:#202050;border-radius:3px}
.spinner{display:inline-block;width:12px;height:12px;border:2px solid var(--dim);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@media(max-width:1100px){.grid{grid-template-columns:1fr}.grid-2{grid-template-columns:1fr}}
</style>
</head>
<body>

<h1>Styde <span>Forge</span> — Command Center v5</h1>
<div class="sub">
  <span class="forge-status" id="forge-status"><span class="orb"></span><span>---</span></span>
  <span class="engine-counter">&#9881; <span class="eng-num" id="eng-count">0</span> engine<span id="eng-plural">s</span></span>
  <span style="color:var(--dim)" id="clock">--:--:--</span>
  <span style="color:var(--dim)">&middot;</span>
  <span style="color:var(--dim)" id="hw">---</span>
  <span class="theme-toggle">
    <button class="theme-btn btn-dark active" onclick="setTheme('dark')" title="Dark"></button>
    <button class="theme-btn btn-light" onclick="setTheme('light')" title="Light"></button>
    <button class="theme-btn btn-oled" onclick="setTheme('oled')" title="OLED"></button>
    <button class="theme-btn btn-forest" onclick="setTheme('forest')" title="Forest"></button>
  </span>
</div>

<!-- TAB NAVIGATION -->
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('monitor')">Monitor</button>
  <button class="tab-btn" onclick="switchTab('control')">Control</button>
</div>

<!-- MONITOR TAB -->
<div class="tab-panel active" id="tab-monitor">
  <div class="kpi-row" id="kpis"></div>
  <div class="grid">
    <div class="card"><h2>Score Trends <span class="subtitle">last 60 evals</span></h2><div class="chart" id="chart"></div><div class="chart-legend"><span><span class="swatch" style="background:linear-gradient(to top,#2040a0,#4070e0)"></span> &#8805;85</span><span><span class="swatch" style="background:linear-gradient(to top,#605020,#a08030)"></span> 70-84</span><span><span class="swatch" style="background:linear-gradient(to top,#602020,#a04040)"></span> &lt;70</span></div></div>
    <div class="card"><h2>Leaderboard</h2><div id="leaderboard"></div></div>
    <div class="card"><h2>System Health</h2><div id="health"></div></div>
  </div>
  <div class="grid-2 gpu-card" id="gpu-section" style="display:none"><div class="card"><h2>GPU Health</h2><div id="gpus"></div></div></div>
  <div class="grid-2">
    <div class="card"><h2>Agents <span class="subtitle">click for details</span></h2><div style="max-height:380px;overflow-y:auto"><table class="agent-table"><thead><tr><th>Blueprint</th><th>Run</th><th>Score</th><th>Training</th><th>Stage</th><th>Teacher</th></tr></thead><tbody id="agents"></tbody></table></div></div>
    <div class="card"><h2>Blueprints <span class="subtitle" id="bp-count"></span></h2><div class="bp-grid" id="blueprints"></div></div>
  </div>
  <div class="grid-2" style="margin-top:12px">
    <div class="card"><h2>Checkpoints</h2><div style="max-height:160px;overflow-y:auto" id="checkpoints"></div></div>
    <div class="card"><h2>Latest Agent Output</h2><div style="font:10px/1.4 'Consolas',monospace;color:#7080a0;max-height:160px;overflow-y:auto;white-space:pre-wrap;background:#060610;padding:8px;border-radius:4px" id="output-preview">Waiting...</div><div style="font-size:9px;color:var(--dim);margin-top:3px" id="output-meta"></div></div>
  </div>
</div>

<!-- CONTROL TAB -->
<div class="tab-panel" id="tab-control">
  <div class="ctrl-panel">
    <h2 style="margin-bottom:12px">ENGINE LAUNCHER</h2>
    <div class="ctrl-row">
      <span class="ctrl-label">Blueprint</span>
      <select class="ctrl-select" id="ctrl-blueprint"></select>
      <span class="ctrl-label">Benchmark</span>
      <select class="ctrl-select" id="ctrl-benchmark"><option value="manual">Manual</option></select>
    </div>
    <div class="ctrl-row">
      <span class="ctrl-label">Engines</span>
      <div class="engine-count">
        <input type="range" id="ctrl-count" min="1" max="4" value="1" oninput="document.getElementById('ctrl-count-val').textContent=this.value">
        <span class="count-display" id="ctrl-count-val">1</span>
      </div>
      <button class="ctrl-btn btn-start" onclick="launchEngines()">&#9654; LAUNCH</button>
      <button class="ctrl-btn btn-stop-all" onclick="stopAllEngines()">&#9632; STOP ALL</button>
      <span id="ctrl-status" style="font-size:11px;color:var(--dim);margin-left:8px"></span>
    </div>
  </div>

  <div class="grid-2">
    <div class="card">
      <h2>Active Engines <span class="subtitle" id="eng-list-count">0 running</span></h2>
      <div class="engine-list" id="engine-list"><span style="color:var(--dim);font-size:11px">No engines running. Launch one above.</span></div>
    </div>
    <div class="card">
      <h2>Quick Actions</h2>
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:4px">
        <div style="display:flex;gap:8px;align-items:center">
          <span style="color:var(--dim);font-size:10px">Forge Status:</span>
          <span id="ctrl-fs" style="font-weight:700;font-size:12px">---</span>
        </div>
        <div style="display:flex;gap:8px;align-items:center">
          <span style="color:var(--dim);font-size:10px">Python Processes:</span>
          <span id="ctrl-py" style="font-size:12px;color:var(--accent)">0</span>
        </div>
        <div style="display:flex;gap:8px;align-items:center">
          <span style="color:var(--dim);font-size:10px">GPU Count:</span>
          <span id="ctrl-gpu" style="font-size:12px;color:var(--accent)">0</span>
        </div>
        <hr style="border-color:var(--border);margin:4px 0">
        <button class="ctrl-btn" style="background:var(--accent);color:#fff" onclick="window.open('/stream')">&#8635; Raw SSE Stream</button>
        <button class="ctrl-btn" style="background:var(--dim);color:#fff" onclick="document.querySelector('.btn-dark').click()">Dark Theme</button>
      </div>
    </div>
  </div>
</div>

<!-- MODAL -->
<div class="modal-overlay" id="modal-overlay">
<div class="modal"><button class="modal-close" onclick="closeModal()">&times;</button><div id="modal-content"></div></div>
</div>

<div class="toast-container" id="toasts"></div>
<div class="footer">Styde Forge v5 &middot; Command Center &middot; Built on Hermes Agent &middot; <span id="cost"></span></div>

<script>
/* ═══════════ THEME ═══════════ */
const TK='forge-theme-v5';
function setTheme(t){
  document.documentElement.setAttribute('data-theme',t);
  localStorage.setItem(TK,JSON.stringify({theme:t,v:1,ts:Date.now()}));
  document.querySelectorAll('.theme-btn').forEach(b=>b.classList.remove('active'));
  document.querySelector('.btn-'+t)?.classList.add('active');
}
setTheme((()=>{try{return JSON.parse(localStorage.getItem(TK)).theme||'dark'}catch(e){return'dark'}})());

/* ═══════════ TABS ═══════════ */
function switchTab(name){
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  document.querySelector('.tab-btn:nth-child('+(name==='monitor'?1:2)+')').classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}

/* ═══════════ ENGINE CONTROL ═══════════ */
async function apiCall(endpoint, method='GET', body=null){
  try{
    const opts={method,headers:{}};
    if(body){opts.headers['Content-Type']='application/json';opts.body=JSON.stringify(body);}
    const r=await fetch(endpoint,opts);
    return await r.json();
  }catch(e){return{success:false,message:String(e)};}
}

async function launchEngines(){
  const bp=document.getElementById('ctrl-blueprint').value;
  const bm=document.getElementById('ctrl-benchmark').value;
  const count=parseInt(document.getElementById('ctrl-count').value)||1;
  const st=document.getElementById('ctrl-status');
  st.innerHTML='<span class="spinner"></span> Launching...';
  const proms=[];
  for(let i=0;i<count;i++) proms.push(apiCall('/api/engines/start','POST',{blueprint:bp,benchmark:bm}));
  const results=await Promise.all(proms);
  const ok=results.filter(r=>r.success).length;
  st.textContent=ok+'/'+count+' engines launched';
  addToast(ok+' engine(s) started','toast');
}

async function killEngine(pid){
  const r=await apiCall('/api/engines/stop','POST',{pid});
  addToast(r.message,'toast-warn');
}

async function stopAllEngines(){
  if(!confirm('Stop ALL engines?'))return;
  const st=document.getElementById('ctrl-status');
  st.innerHTML='<span class="spinner"></span> Stopping...';
  const r=await apiCall('/api/engines/stop-all','POST');
  st.textContent='Stopped '+r.stopped+' engine(s)';
  addToast('All engines stopped','toast-warn');
}

function addToast(msg,cls='toast'){
  const t=document.createElement('div');t.className=cls;t.textContent=msg;
  document.getElementById('toasts').appendChild(t);setTimeout(()=>t.remove(),4000);
}

/* ═══════════ MODAL ═══════════ */
let agentData=[];
function openModal(idx){
  const a=agentData[idx];if(!a)return;
  const ev=a.eval||{};const imp=a.improvement||{};
  const sc=a.score!==null?a.score:'\u2014';
  const scClr=a.score>=85?'#30c050':(a.score>=70?'#c0a030':'#e04040');
  let dimsHtml='';
  const dims=ev.dimensions||{};
  Object.entries(dims).forEach(([k,v])=>{
    const ds=typeof v==='object'?(v.score||v):v;
    dimsHtml+='<div class="eval-dim"><div class="dim-label">'+k.replace(/_/g,' ').replace(/\b\w/g,c=>c.toUpperCase())+'</div><div class="dim-score" style="color:'+(ds>=85?'#30c050':ds>=70?'#c0a030':'#e04040')+'">'+ds+'</div></div>';
  });
  let teacherHtml='';
  if(imp.diagnosis)teacherHtml+='<div class="teacher-box"><strong>Diagnosis:</strong> '+imp.diagnosis+'</div>';
  if(imp.summary)teacherHtml+='<div class="teacher-box"><strong>Summary:</strong> '+imp.summary+'</div>';
  if(ev.composite_score)teacherHtml+='<div style="margin-top:6px;font-size:9px;color:var(--dim)">Composite: '+ev.composite_score+' &middot; Passed: '+(ev.passed?'Yes':'No')+' &middot; Benchmark: '+(ev.benchmark||'?')+'</div>';
  document.getElementById('modal-content').innerHTML=
    '<h3>'+a.blueprint+'</h3>'+
    '<div class="meta">Run: '+a.run_id+' &middot; Stage: '+a.stage+' &middot; Status: '+a.status+' &middot; Version: '+(a.version||'?')+' &middot; Spawned: '+a.spawned+'</div>'+
    '<h4>Score: <span style="color:'+scClr+';font-size:18px">'+sc+'</span></h4>'+
    (dimsHtml?'<h4>Evaluation Dimensions</h4><div class="eval-grid">'+dimsHtml+'</div>':'')+
    (teacherHtml?'<h4>Teacher Analysis</h4>'+teacherHtml:'')+
    '<div style="margin-top:12px;font-size:9px;color:var(--dim)">Training: '+(a.training_label||'?')+' ('+(a.training_pct||0)+'%)</div>';
  document.getElementById('modal-overlay').classList.add('open');document.body.style.overflow='hidden';
}
function closeModal(){document.getElementById('modal-overlay').classList.remove('open');document.body.style.overflow='';}
document.getElementById('modal-overlay').addEventListener('click',function(e){if(e.target===this)closeModal();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal();});

/* ═══════════ SSE ═══════════ */
let prevProduction=0;
const evtSource=new EventSource('/stream');
evtSource.onmessage=function(event){
  const d=JSON.parse(event.data);
  agentData=d.agents||[];
  document.getElementById('clock').textContent=d.ts;
  document.getElementById('hw').textContent=d.hardware;

  // Forge status
  const fs=d.forge_status||{};
  const fe=document.getElementById('forge-status');
  fe.innerHTML='<span class="orb"></span><span>'+fs.label+'</span>';
  fe.className='forge-status '+(fs.css_class||'');
  document.getElementById('ctrl-fs').textContent=fs.label;

  // Engine info
  const eng=d.engines||{};
  document.getElementById('eng-count').textContent=eng.engines||0;
  document.getElementById('eng-plural').textContent=eng.engines===1?'':'s';
  document.getElementById('ctrl-py').textContent=eng.python_processes||0;
  document.getElementById('ctrl-gpu').textContent=(d.gpus||[]).length;
  renderEngineList(eng.processes||[]);

  // Toasts
  if(d.production>prevProduction&&prevProduction>0)addToast('AGENT PROMOTED TO PRODUCTION');
  if(fs.status==='crashed')addToast('FORGE CRASHED','toast-err');
  prevProduction=d.production;

  // KPIs
  const trendIcon=d.score_trend==='up'?'\u25B2':(d.score_trend==='down'?'\u25BC':'\u25A0');
  const trendCls=d.score_trend==='up'?'score-up':(d.score_trend==='down'?'score-down':'score-flat');
  document.getElementById('kpis').innerHTML=
    '<div class="kpi"><div class="num">'+d.spawned+'</div><div class="lbl">Spawned</div></div>'+
    '<div class="kpi"><div class="num">'+d.evaluations+'</div><div class="lbl">Evaluations</div></div>'+
    '<div class="kpi kpi-blue"><div class="num">'+d.loops+'</div><div class="lbl">Loops</div></div>'+
    '<div class="kpi kpi-ok"><div class="num">'+d.production+'</div><div class="lbl">Production</div></div>'+
    '<div class="kpi kpi-warn"><div class="num">'+d.refinery+'</div><div class="lbl">Refinery</div></div>'+
    '<div class="kpi"><div class="num">'+d.score_avg+' <span style="font-size:12px" class="'+trendCls+'">'+trendIcon+'</span></div><div class="lbl">Avg Score</div></div>'+
    '<div class="kpi"><div class="num">'+d.blueprints.length+'</div><div class="lbl">Blueprints</div></div>';

  // Chart
  const chart=document.getElementById('chart');let bars='';const max=Math.max(...d.scores,100);
  d.scores.forEach(s=>{let cls=s>=85?'bar-prod':(s>=70?'bar-mid':'bar-low');bars+='<div class="bar '+cls+'" style="height:'+Math.max(s/max*80,2)+'px" title="'+s+'"></div>';});
  const lastScore=d.scores.length?d.scores[d.scores.length-1]:0;
  const scoreCls=lastScore>=85?'score-up':(lastScore>=70?'score-flat':'score-down');
  chart.innerHTML=bars+'<div class="score-overlay '+scoreCls+'">'+lastScore+'</div>';

  // GPU
  const gs=document.getElementById('gpu-section'),gd=document.getElementById('gpus');
  if(d.gpus&&d.gpus.length){gs.style.display='';let gh='';
    d.gpus.forEach(g=>{const tc=g.temp>80?'gpu-temp-hot':(g.temp>65?'gpu-temp-warm':'gpu-temp-ok');
    gh+='<div class="gpu-item"><span class="gpu-name">'+g.name+'</span><span class="gpu-stat" style="color:var(--blue)">Load '+g.load+'&#37;</span><div class="gpu-bar-wrap"><div class="gpu-bar gpu-bar-load" style="width:'+g.load+'%"></div></div><span class="gpu-stat" style="color:#c080f0">VRAM '+g.vram_used+'/'+g.vram_total+'G</span><div class="gpu-bar-wrap"><div class="gpu-bar gpu-bar-mem" style="width:'+(g.vram_used/g.vram_total*100)+'%"></div></div><span class="gpu-stat '+tc+'">'+g.temp+'&deg;C</span></div>';});
    gd.innerHTML=gh;}else{gs.style.display='none';}

  // Agents
  let ah='';
  d.agents.forEach((a,i)=>{
    let badge=a.stage==='production'?'<span class="badge badge-prod">PROD</span>':(a.stage==='archive'?'<span class="badge badge-arch">ARCH</span>':'<span class="badge badge-ref">REF</span>');
    let sc=a.score!==null?a.score:'\u2014';let scClr=a.score>=85?'color:#30c050':(a.score>=70?'color:#c0a030':'color:#e04040');
    let xpc=a.stage==='archive'?'xp-fill-archived':(a.training_pct===100?'xp-fill-full':(a.training_pct<=25?'xp-fill-spawn':(a.training_pct<=55?'xp-fill-eval':'xp-fill-training')));
    ah+='<tr onclick="openModal('+i+')"><td>'+a.blueprint+'</td><td style="color:#404070">'+a.run_id+'</td><td class="score-cell" style="'+scClr+'">'+sc+'</td><td class="xp-cell"><div class="xp-bar-wrap"><div class="xp-bar-outer"><div class="xp-bar-fill '+xpc+'" style="width:'+a.training_pct+'%"></div></div><span class="xp-bar-label">'+a.training_label+'</span></div></td><td>'+badge+'</td><td style="color:#5050a0;font-size:9px">'+a.teacher+'</td></tr>';
  });
  document.getElementById('agents').innerHTML=ah||'<tr><td colspan="6" style="color:#505070">No agents.</td></tr>';

  // Leaderboard
  let lh='';d.leaderboard.forEach((a,i)=>{let rc=i===0?'lb-rank-1':(i===1?'lb-rank-2':(i===2?'lb-rank-3':'lb-rank-n'));lh+='<div class="lb-row"><span><span class="lb-rank '+rc+'">'+(i+1)+'</span>'+a.blueprint+'</span><span style="font-weight:700;color:'+(a.score>=90?'#40e040':(a.score>=85?'#40c040':'#c0a030'))+'">'+a.score+'</span></div>';});
  document.getElementById('leaderboard').innerHTML=lh||'<span style="color:#505070">No production agents yet.</span>';

  // Health
  const h=d.health;
  document.getElementById('health').innerHTML='<div style="margin-bottom:6px"><span style="color:#8080b0">CPU</span><span style="float:right">'+h.cpu+'&#37;</span><div style="background:var(--xp-bg);border-radius:3px;height:4px;margin-top:2px"><div style="background:linear-gradient(to right,#3060c0,#40a0f0);height:4px;border-radius:3px;width:'+Math.min(h.cpu,100)+'%"></div></div></div><div style="margin-bottom:6px"><span style="color:#8080b0">RAM</span><span style="float:right">'+h.ram_gb+'/'+h.ram_total+' GB</span><div style="background:var(--xp-bg);border-radius:3px;height:4px;margin-top:2px"><div style="background:linear-gradient(to right,#8050c0,#c080f0);height:4px;border-radius:3px;width:'+h.ram_pct+'%"></div></div></div><div><span style="color:#8080b0">Disk</span><span style="float:right">'+h.disk_free+' GB free</span><div style="background:var(--xp-bg);border-radius:3px;height:4px;margin-top:2px"><div style="background:linear-gradient(to right,#c05030,#f08040);height:4px;border-radius:3px;width:'+h.disk_pct+'%"></div></div></div>';

  // Misc
  document.getElementById('checkpoints').innerHTML=d.checkpoints.map(c=>'<div class="cp-item"><span>'+c.id+'</span><span style="color:#404080">'+c.created+'</span></div>').join('')||'<span style="color:#505070">No checkpoints.</span>';
  document.getElementById('blueprints').innerHTML=d.blueprints.map(b=>'<div class="bp-chip"><span class="bp-name">'+b.name+'</span><span class="bp-ver">v'+b.version+'</span></div>').join('')||'<span style="color:#505070">No blueprints.</span>';
  document.getElementById('bp-count').textContent=d.blueprints.length+' total';
  document.getElementById('cost').textContent='Est. tokens: '+(d.cost.tokens/1000).toFixed(0)+'k \u00B7 Cost: $'+d.cost.cost.toFixed(4);

  // Populate blueprint/benchmark selectors (once)
  if(!window._selectorsPopulated){
    const bs=d.blueprints||[];const bms=d.benchmarks||[];
    document.getElementById('ctrl-blueprint').innerHTML=bs.map(b=>'<option value="'+b.name+'">'+b.name+' (v'+b.version+')</option>').join('');
    document.getElementById('ctrl-benchmark').innerHTML='<option value="manual">Manual</option>'+bms.filter(b=>b!=='code-review-basic').map(b=>'<option value="'+b+'">'+b+'</option>').join('');
    window._selectorsPopulated=true;
  }
};

function renderEngineList(processes){
  const el=document.getElementById('engine-list');
  const cnt=document.getElementById('eng-list-count');
  if(!processes||!processes.length){el.innerHTML='<span style="color:var(--dim);font-size:11px">No engines running. Launch one above.</span>';cnt.textContent='0 running';return;}
  cnt.textContent=processes.filter(p=>p.alive).length+' running';
  el.innerHTML=processes.map(p=>
    '<div class="eng-item"><span class="eng-pid">PID '+p.pid+'</span><span class="eng-bp">'+p.blueprint+' ('+p.benchmark+')</span><span class="eng-started">'+p.started+'</span><span class="eng-status '+(p.alive?'eng-status-running':'eng-status-dead')+'">'+(p.alive?'RUNNING':'DEAD')+'</span>'+(p.alive?'<button class="eng-kill" onclick="killEngine('+p.pid+')">KILL</button>':'')+'</div>'
  ).join('');
}

evtSource.onerror=function(){setTimeout(()=>location.reload(),5000);};
</script>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════════
# HTTP SERVER with REST API
# ═══════════════════════════════════════════════════════════════

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/stream":
            self._serve_sse()
            return

        if path == "/api/engines":
            self._json_response(get_engine_info())
            return

        if path == "/api/state":
            self._json_response(json.loads(build_state_json()))
            return

        # Serve HTML for everything else
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        body = {}
        if length > 0:
            try: body = json.loads(self.rfile.read(length))
            except: pass

        if path == "/api/engines/start":
            bp = body.get("blueprint", "code-reviewer")
            bm = body.get("benchmark", "manual")
            result = start_engine(bp, bm)
            self._json_response(result)
            return

        if path == "/api/engines/stop":
            pid = body.get("pid", 0)
            if pid:
                result = stop_engine(int(pid))
            else:
                result = {"success": False, "message": "Missing pid"}
            self._json_response(result)
            return

        if path == "/api/engines/stop-all":
            result = stop_all_engines()
            self._json_response(result)
            return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'{"error":"not found"}')

    def _json_response(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode("utf-8"))

    def _serve_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        q = Queue()
        with sse_lock: sse_clients.append(q)
        try:
            data = build_state_json()
            self.wfile.write(f"data: {data}\n\n".encode("utf-8"))
            self.wfile.flush()
            while True:
                try:
                    msg = q.get(timeout=30)
                    self.wfile.write(msg.encode("utf-8"))
                    self.wfile.flush()
                except:
                    self.wfile.write(b": heartbeat\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError): pass
        finally:
            with sse_lock:
                if q in sse_clients: sse_clients.remove(q)

    def log_message(self, format, *args): pass


def run_dashboard():
    HTTPServer.allow_reuse_address = True
    threading.Thread(target=sse_broadcaster, daemon=True).start()
    server = HTTPServer(("localhost", PORT), DashboardHandler)
    print(f"\n  STYDE FORGE COMMAND CENTER v5")
    print(f"  ==============================")
    print(f"  URL:     http://localhost:{PORT}")
    print(f"  API:     http://localhost:{PORT}/api/engines")
    print(f"  Stream:  http://localhost:{PORT}/stream")
    print(f"  Features: 4 themes · GPU · Modals · XP bars · Engine Control Panel")
    print(f"  Press Ctrl+C to stop\n")
    try: server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Shutting down...")
        stop_all_engines()
        server.server_close()

if __name__ == "__main__":
    run_dashboard()
