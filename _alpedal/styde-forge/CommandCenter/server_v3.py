"""
Forge Command Center v3 — High-performance real-time forge monitor
Port 8766. Background data collection, os.scandir(), accessibility, responsive.
"""
import sys, os, json, yaml, time, threading, re, gzip, io
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

FORGE_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = FORGE_ROOT / "state.yaml"
BP_DIR = FORGE_ROOT / "StydeAgents" / "blueprints"
REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"
PRODUCTION_DIR = FORGE_ROOT / "StydeAgents" / "production"
ARCHIVE_DIR = FORGE_ROOT / "StydeAgents" / "archive"
PORT = 8766
SERVER_START_TIME = time.time()

# ── Thread-safe state cache ──
_state_lock = threading.Lock()
_compute_lock = threading.Lock()  # prevents concurrent compute_state()
_cached_result = None
_last_scan = 0
SCAN_INTERVAL = 15  # background scan every 15s

def _scandir_count(path):
    """Fast directory count using os.scandir()."""
    if not os.path.isdir(path):
        return 0
    return sum(1 for e in os.scandir(path) if e.is_dir() and not e.name.startswith("_"))

def _scan_eval_scores(bp_path, max_runs=3):
    """Scan eval.yaml files for a blueprint using os.scandir. Returns list of scores (newest first)."""
    runs_path = os.path.join(bp_path, "runs")
    if not os.path.isdir(runs_path):
        return []
    entries = sorted(
        [e for e in os.scandir(runs_path) if e.name.startswith("run-") and e.is_dir()],
        key=lambda e: e.name, reverse=True
    )
    scores = []
    for e in entries[:max_runs]:
        ey = os.path.join(e.path, "eval.yaml")
        if os.path.isfile(ey):
            try:
                with open(ey, 'r', encoding='utf-8') as f:
                    ed = yaml.safe_load(f)
                cs = ed.get("composite", {}).get("composite_score", 0)
                if cs:
                    scores.append(cs)
            except Exception:
                pass
    return scores

def get_state():
    """Return full state. Recomputes if cache is older than SCAN_INTERVAL."""
    global _cached_result, _last_scan
    
    now = time.time()
    
    # Return cached if fresh
    if _cached_result and (now - _last_scan) < SCAN_INTERVAL:
        return _cached_result
    
    # Recompute (with lock to prevent concurrent computation)
    with _compute_lock:
        # Re-check after acquiring lock
        if _cached_result and (time.time() - _last_scan) < SCAN_INTERVAL:
            return _cached_result
        
        state = {}
        try:
            if STATE_FILE.exists():
                state = yaml.safe_load(STATE_FILE.read_text(encoding="utf-8")) or {}
        except Exception:
            state = {}

        agents = state.get("agents", []) or []
        evals = state.get("evaluations", []) or []
        activity = state.get("activity", []) or []

        forge_info = {
            "codename": state.get("forge_codename", "The Crucible"),
            "version": state.get("forge_version", "3.0"),
            "loop_iterations": state.get("loop_iterations", 0),
            "total_agents": state.get("total_agents", len(agents)),
            "total_evaluations": state.get("total_evaluations", len(evals)),
            "caveman_ultra": state.get("caveman_ultra", True),
            "last_checkpoint": str(state.get("last_checkpoint", "N/A"))[:30],
        }

        rn = _scandir_count(str(REFINERY_DIR))
        pn = _scandir_count(str(PRODUCTION_DIR))
        an = _scandir_count(str(ARCHIVE_DIR))

        active = []
        for a in activity:
            if a.get("status") == "running":
                active.append({
                    "action": a.get("action", "?"),
                    "blueprint": a.get("blueprint", "?"),
                    "detail": str(a.get("detail", ""))[:80],
                    "progress": a.get("progress", 0),
                    "timestamp": str(a.get("timestamp", "")),
                })

        recent = []
        for a in activity[:50]:
            recent.append({
                "action": a.get("action", "?"),
                "blueprint": a.get("blueprint", "?"),
                "detail": str(a.get("detail", ""))[:100],
                "progress": a.get("progress", 0),
                "status": a.get("status", "?"),
                "timestamp": str(a.get("timestamp", "")),
            })

        bp_scores = {}
        for a in agents:
            bp = a.get("blueprint", "")
            sc = a.get("composite_score")
            stage = a.get("stage", "refinery")
            if bp:
                entry = bp_scores.setdefault(bp, {"best": 0, "latest": 0, "stage": stage, "count": 0, "history": []})
                if sc is not None:
                    entry["best"] = max(entry["best"], sc)
                    entry["latest"] = sc
                entry["count"] += 1

        for e in evals:
            bp = e.get("blueprint", "")
            sc = e.get("composite_score")
            if bp and sc is not None:
                entry = bp_scores.setdefault(bp, {"best": 0, "latest": 0, "stage": "refinery", "count": 0, "history": []})
                entry["best"] = max(entry["best"], sc)
                entry["latest"] = max(entry["latest"], sc)

        prod_bps = set()
        if os.path.isdir(str(PRODUCTION_DIR)):
            for bp_entry in os.scandir(str(PRODUCTION_DIR)):
                if bp_entry.is_dir() and not bp_entry.name.startswith("_"):
                    prod_bps.add(bp_entry.name)
                    if bp_entry.name not in bp_scores:
                        bp_scores[bp_entry.name] = {"best": 0, "latest": 0, "stage": "production", "count": 0, "history": []}
                    else:
                        bp_scores[bp_entry.name]["stage"] = "production"

        # ── Scan eval history for trends ──
        _bp_dir_bases = [str(REFINERY_DIR), str(PRODUCTION_DIR), str(ARCHIVE_DIR), str(BP_DIR)]
        for bp_name in bp_scores:
            found = False
            for base in _bp_dir_bases:
                bp_path = os.path.join(base, bp_name)
                if os.path.isdir(bp_path):
                    scores = _scan_eval_scores(bp_path, max_runs=3)
                    if len(scores) >= 2:
                        if scores[0] > scores[1]:
                            bp_scores[bp_name]["trend"] = "up"
                        elif scores[0] < scores[1]:
                            bp_scores[bp_name]["trend"] = "down"
                        else:
                            bp_scores[bp_name]["trend"] = "flat"
                        bp_scores[bp_name]["prev_score"] = scores[1]
                    elif len(scores) == 1:
                        bp_scores[bp_name]["trend"] = "flat"
                        bp_scores[bp_name]["prev_score"] = scores[0]
                    else:
                        bp_scores[bp_name]["trend"] = "flat"
                        bp_scores[bp_name]["prev_score"] = 0
                    found = True
                    break
            if not found:
                bp_scores[bp_name]["trend"] = "flat"
                bp_scores[bp_name]["prev_score"] = 0

        lock = None
        lf = str(FORGE_ROOT / ".forge.lock")
        if os.path.isfile(lf):
            try:
                with open(lf) as f:
                    lock = json.load(f)
            except Exception:
                lock = {"pid": "?", "acquired": "?"}

        dt_now = datetime.now(timezone.utc)
        hour = dt_now.hour
        peak_active = (1 <= hour < 4) or (6 <= hour < 10)
        peak_msg = ""
        if 1 <= hour < 4:
            peak_msg = f"~{(4 - hour)}h left"
        elif 6 <= hour < 10:
            peak_msg = f"~{(10 - hour)}h left"

        result = {
            "forge": forge_info,
            "pipeline": {"refinery": rn, "production": pn, "archive": an},
            "active_processes": active[:20],
            "activity": recent,
            "bp_scores": dict(sorted(bp_scores.items(), key=lambda x: -x[1].get("best", 0))),
            "forge_lock": lock,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime": int(time.time() - SERVER_START_TIME),
            "peak_hours": {
                "active": peak_active,
                "current_utc": f"{hour:02d}:00 UTC",
                "ends": peak_msg,
                "slots": "01:00\u201304:00 / 06:00\u201310:00 UTC",
            },
        }

        _cached_result = result
        _last_scan = time.time()
        return result


# ── HTML ──
INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Forge Command Center v3</title>
<style>
:root {
  --bg: #0a0a0f; --bg-gradient: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0a14 100%);
  --surface: rgba(22,22,35,0.7); --surface-hover: rgba(30,30,48,0.8);
  --glass: rgba(22,22,35,0.55); --glass-strong: rgba(18,18,30,0.75);
  --border: rgba(255,255,255,0.06); --border-light: rgba(255,255,255,0.1);
  --text: #e4e4ed; --text-dim: #8e8e9e; --text-bright: #f5f5fc;
  --accent: #7c7cf8; --accent-glow: rgba(124,124,248,0.12);
  --green: #3dd68c; --green-dim: rgba(61,214,140,0.1);
  --amber: #f5a623; --amber-dim: rgba(245,166,35,0.1);
  --red: #f14668; --red-dim: rgba(241,70,104,0.1);
  --blue: #54a0ff; --blue-dim: rgba(84,160,255,0.08);
  --purple: #b37feb;
  --radius: 12px; --radius-sm: 8px;
  --font: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', system-ui, sans-serif;
  --mono: 'SF Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.3); --shadow-md: 0 4px 16px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.5);
  --blur: saturate(180%) blur(20px);
}
.light-theme {
  --bg: #f2f2f7; --bg-gradient: linear-gradient(135deg, #f2f2f7 0%, #e8e8f0 50%, #f0f0f5 100%);
  --surface: rgba(255,255,255,0.75); --surface-hover: rgba(255,255,255,0.9);
  --glass: rgba(255,255,255,0.6); --glass-strong: rgba(255,255,255,0.8);
  --border: rgba(0,0,0,0.06); --border-light: rgba(0,0,0,0.1);
  --text: #1d1d2e; --text-dim: #86868b; --text-bright: #0d0d1a;
  --accent: #5e5ce6; --accent-glow: rgba(94,92,230,0.08);
  --green: #30b576; --green-dim: rgba(48,181,118,0.1);
  --amber: #d69111; --amber-dim: rgba(214,145,17,0.1);
  --red: #e03050; --red-dim: rgba(224,48,80,0.1);
  --blue: #3b82f6; --blue-dim: rgba(59,130,246,0.08);
  --purple: #8b5cf6;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06); --shadow-md: 0 4px 16px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.12);
  --blur: saturate(180%) blur(24px);
}
.light-theme .bp-detail-panel{box-shadow:0 8px 40px rgba(0,0,0,0.15)}
.light-theme .bp-detail-panel::before{background:rgba(0,0,0,0.15)}

*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
body{font-family:var(--font);background:var(--bg);background-image:var(--bg-gradient);color:var(--text);height:100vh;display:flex;flex-direction:column;overflow:hidden;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:6px}

/* ── Top bar (Apple-style navigation bar) ── */
.topbar{display:flex;align-items:center;gap:14px;padding:8px 20px;background:var(--glass-strong);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);border-bottom:1px solid var(--border);font-size:11px;flex-shrink:0;min-height:44px;z-index:10}
.topbar .title{font-size:14px;font-weight:600;color:var(--text-bright);letter-spacing:-0.3px;font-family:var(--font)}
.topbar .stat{display:flex;align-items:center;gap:5px}
.topbar .stat .num{font-weight:600;font-size:12px;font-family:var(--mono);color:var(--text-bright)}
.topbar .stat .label{color:var(--text-dim);font-size:9px;text-transform:uppercase;letter-spacing:0.4px;font-weight:500}
.topbar .divider{width:1px;height:20px;background:var(--border)}
.topbar .spacer{flex:1}
.theme-btn{background:var(--glass);backdrop-filter:var(--blur);border:1px solid var(--border);border-radius:20px;cursor:pointer;font-size:14px;padding:4px 10px;line-height:1;transition:all 0.2s cubic-bezier(0.25,0.1,0.25,1);color:var(--text)}
.theme-btn:hover{background:var(--surface-hover);border-color:var(--border-light);transform:scale(1.05)}
.lock-dot{width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0}
.lock-locked{background:var(--green);box-shadow:0 0 10px rgba(61,214,140,0.4);animation:pulseLive 2s ease-in-out infinite}
.lock-free{background:var(--text-dim)}
.peak-badge{font-size:8px;padding:3px 8px;border-radius:20px;letter-spacing:0.4px;font-weight:600;text-transform:uppercase;backdrop-filter:var(--blur)}
.peak-on{background:var(--red-dim);color:var(--red);border:1px solid rgba(241,70,104,0.2)}
.peak-off{background:var(--green-dim);color:var(--green);border:1px solid rgba(61,214,140,0.15)}
.badge{font-size:8px;padding:3px 8px;border-radius:20px;text-transform:uppercase;font-weight:600;letter-spacing:0.4px;backdrop-filter:var(--blur)}
.badge-on{background:var(--green-dim);color:var(--green);border:1px solid rgba(61,214,140,0.15)}
.badge-off{background:var(--red-dim);color:var(--red);border:1px solid rgba(241,70,104,0.2)}
@keyframes pulseLive{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.5;transform:scale(0.85)}}

/* ── Main layout ── */
.main-wrap{display:flex;flex:1;overflow:hidden}

/* ── Left: Activity feed ── */
.activity-panel{flex:0 0 370px;display:flex;flex-direction:column;border-right:1px solid var(--border);background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur)}
.activity-header{padding:10px 16px;font-size:10px;font-weight:600;border-bottom:1px solid var(--border);color:var(--text-dim);flex-shrink:0;display:flex;justify-content:space-between;align-items:center;text-transform:uppercase;letter-spacing:0.8px}
.activity-list{flex:1;overflow-y:auto;overflow-x:hidden}
.activity-list::-webkit-scrollbar{width:5px}
.activity-list::-webkit-scrollbar-track{background:transparent}
.activity-list::-webkit-scrollbar-thumb{background:var(--border-light);border-radius:20px}
.activity-list::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,0.15)}
.activity-item{display:flex;align-items:flex-start;gap:8px;padding:8px 14px;border-bottom:1px solid var(--border);font-size:10px;line-height:1.4;transition:all 0.15s cubic-bezier(0.25,0.1,0.25,1)}
.activity-item:hover{background:var(--surface-hover)}
.activity-item.running{border-left:3px solid var(--blue)}
.activity-item.complete{border-left:3px solid var(--green)}
.activity-item.failed{border-left:3px solid var(--red)}
.activity-icon{font-size:12px;flex-shrink:0;margin-top:1px;opacity:0.8}
.activity-body{flex:1;min-width:0}
.activity-action{font-weight:600;font-size:8px;text-transform:uppercase;letter-spacing:0.6px}
.activity-action.spawn{color:var(--accent)}
.activity-action.eval{color:var(--green)}
.activity-action.improve{color:var(--amber)}
.activity-action.loop{color:var(--blue)}
.activity-action.promote{color:var(--purple)}
.activity-bp{font-weight:600;color:var(--text-bright);font-size:10px}
.activity-detail{color:var(--text-dim);font-size:9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px}
.activity-time{color:var(--text-dim);font-size:8px;flex-shrink:0;font-family:var(--mono)}
.activity-progress{height:2px;background:var(--border);border-radius:20px;margin-top:4px;overflow:hidden}
.activity-progress .fill{height:100%;border-radius:20px;background:var(--blue);transition:width 0.6s cubic-bezier(0.25,0.1,0.25,1)}
.empty-state{padding:40px 20px;text-align:center;color:var(--text-dim);font-size:10px;line-height:1.6}
.empty-state .icon{font-size:28px;margin-bottom:8px;opacity:0.35}

/* ── Center ── */
.center-panel{flex:1;display:flex;flex-direction:column;overflow:hidden;background:rgba(0,0,0,0.08)}

/* Pipeline bar */
.pipeline-bar{display:flex;gap:12px;padding:12px 16px;border-bottom:1px solid var(--border);background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);flex-shrink:0}
.pipeline-stage{flex:1;padding:10px 14px;border-radius:var(--radius);background:var(--surface);text-align:center;border:1px solid var(--border);transition:all 0.2s cubic-bezier(0.25,0.1,0.25,1);cursor:default}
.pipeline-stage:hover{border-color:var(--border-light);transform:translateY(-1px);box-shadow:var(--shadow-sm)}
.pipeline-stage .count{font-size:22px;font-weight:700;font-family:var(--mono);letter-spacing:-1px}
.pipeline-stage .label{font-size:9px;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.8px;margin-top:2px;font-weight:500}
.pipeline-stage.refinery .count{color:var(--amber)}
.pipeline-stage.production .count{color:var(--green)}
.pipeline-stage.archive .count{color:var(--red)}

/* Active processes */
.active-section{padding:10px 16px;border-bottom:1px solid var(--border);flex-shrink:0;background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur)}
.section-title{font-size:9px;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;display:flex;align-items:center;gap:8px;font-weight:600}
.section-count{font-size:8px;color:var(--text-dim);background:var(--border);padding:2px 8px;border-radius:20px}
.active-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:8px}
.active-card{padding:8px 10px;border-radius:var(--radius-sm);background:var(--surface);border:1px solid var(--border);font-size:9px;transition:all 0.2s cubic-bezier(0.25,0.1,0.25,1)}
.active-card:hover{background:var(--surface-hover);border-color:var(--border-light);transform:translateY(-1px);box-shadow:var(--shadow-sm)}
.active-card .ac-action{font-weight:600;text-transform:uppercase;font-size:8px;color:var(--blue);letter-spacing:0.5px}
.active-card .ac-bp{font-weight:600;font-size:10px;margin-top:1px}
.active-card .ac-detail{color:var(--text-dim);font-size:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:1px}
.active-card .ac-progress{height:3px;background:var(--border);border-radius:20px;margin-top:5px;overflow:hidden}
.active-card .ac-progress .fill{height:100%;border-radius:20px;background:var(--blue);transition:width 1s cubic-bezier(0.25,0.1,0.25,1)}

/* Search & filter bar */
.toolbar{display:flex;gap:8px;padding:10px 16px;border-bottom:1px solid var(--border);flex-shrink:0;align-items:center;background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur)}
.search-box{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:5px 12px;color:var(--text);font-size:10px;width:190px;font-family:var(--font);transition:all 0.2s;outline:none}
.search-box:focus{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-glow)}
.search-box::placeholder{color:var(--text-dim)}
.filter-btn{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:5px 12px;color:var(--text-dim);font-size:9px;cursor:pointer;transition:all 0.2s cubic-bezier(0.25,0.1,0.25,1);font-family:var(--font);font-weight:500}
.filter-btn:hover{color:var(--text);border-color:var(--border-light);background:var(--surface-hover)}
.filter-btn.active{color:var(--accent);border-color:var(--accent);background:var(--accent-glow);font-weight:600}
.sort-select{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:5px 10px;color:var(--text);font-size:9px;font-family:var(--font);cursor:pointer;outline:none}
.sort-select:focus{border-color:var(--accent)}

/* Blueprint score grid */
.bp-section{flex:1;overflow-y:auto;padding:8px 16px 16px}
.bp-section::-webkit-scrollbar{width:5px}
.bp-section::-webkit-scrollbar-track{background:transparent}
.bp-section::-webkit-scrollbar-thumb{background:var(--border-light);border-radius:20px}
.bp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:6px}
.bp-card{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:var(--radius-sm);font-size:9px;border:1px solid var(--border);background:var(--surface);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);transition:all 0.2s cubic-bezier(0.25,0.1,0.25,1);cursor:pointer}
.bp-card:hover{background:var(--surface-hover);border-color:var(--border-light);transform:translateY(-1px);box-shadow:var(--shadow-sm)}
.bp-card:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.bp-card .bp-name{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:500;font-size:9.5px}
.bp-card .bp-score{font-weight:700;font-size:11px;min-width:28px;text-align:right;font-family:var(--mono)}
.bp-card .bp-bar{flex:0 0 50px;height:4px;background:var(--border);border-radius:20px;overflow:hidden}
.bp-card .bp-bar .fill{height:100%;border-radius:20px;transition:width 0.5s cubic-bezier(0.25,0.1,0.25,1)}
.bp-card .bp-evals{font-size:8px;color:var(--text-dim);min-width:16px;text-align:center}
.bp-card .bp-stage{font-size:7px;padding:2px 6px;border-radius:20px;text-transform:uppercase;font-weight:600;letter-spacing:0.4px}
.bp-card .bp-stage.prod{background:var(--green-dim);color:var(--green)}
.bp-card .bp-stage.ref{background:var(--amber-dim);color:var(--amber)}
.bp-card .bp-stage.arch{background:var(--red-dim);color:var(--red)}
.bp-card .bp-history{display:flex;gap:3px;align-items:center;margin-left:2px}
.bp-card .bp-dot{width:11px;height:11px;border-radius:4px;font-size:7px;font-weight:700;display:flex;align-items:center;justify-content:center;line-height:1;color:#fff}
.score-0{color:var(--text-dim)}
.score-low{color:var(--red)}
.score-mid{color:var(--amber)}
.score-high{color:var(--green)}

/* Score distribution chart */
.score-dist{display:flex;gap:4px;padding:10px 16px;align-items:flex-end;border-bottom:1px solid var(--border);flex-shrink:0;background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur)}
.score-dist .dist-bar{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer;padding:4px 3px;border-radius:var(--radius-sm);transition:all 0.2s;position:relative}
.score-dist .dist-bar:hover{background:var(--surface-hover)}
.score-dist .dist-bar.active{background:var(--accent-glow)}
.score-dist .dist-fill{border-radius:4px 4px 0 0;width:70%;min-height:3px;transition:height 0.5s cubic-bezier(0.25,0.1,0.25,1)}
.score-dist .dist-label{font-size:7px;color:var(--text-dim);text-transform:uppercase;font-weight:500;letter-spacing:0.3px}
.score-dist .dist-count{font-size:9px;color:var(--text-bright);font-weight:700;font-family:var(--mono)}

/* Trend arrow */
.bp-trend{font-size:13px;line-height:1;flex-shrink:0;width:16px;text-align:center}
.bp-trend.up{color:var(--green)}
.bp-trend.down{color:var(--red)}
.bp-trend.flat{color:var(--text-dim)}

/* ── Right sidebar ── */
.info-panel{flex:0 0 210px;display:flex;flex-direction:column;border-left:1px solid var(--border);background:var(--glass);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);font-size:10px;padding:14px 12px;overflow-y:auto}
.info-panel::-webkit-scrollbar{width:5px}
.info-panel::-webkit-scrollbar-track{background:transparent}
.info-panel::-webkit-scrollbar-thumb{background:var(--border-light);border-radius:20px}
.info-section{margin-bottom:14px}
.info-title{font-size:9px;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px;padding-bottom:6px;border-bottom:1px solid var(--border);font-weight:600}
.info-row{display:flex;justify-content:space-between;padding:3px 0}
.info-row .key{color:var(--text-dim);font-size:9px}
.info-row .val{font-weight:600;font-family:var(--mono);font-size:10px;color:var(--text-bright)}
.info-row .val.green{color:var(--green)}
.info-row .val.amber{color:var(--amber)}

/* Toast */
.toast{position:fixed;bottom:20px;right:20px;background:var(--glass-strong);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);border:1px solid var(--red);color:var(--red);padding:10px 16px;border-radius:var(--radius);font-size:10px;z-index:1000;animation:slideIn 0.35s cubic-bezier(0.25,0.1,0.25,1);max-width:320px;box-shadow:var(--shadow-lg)}
.toast.info{background:var(--glass-strong);border-color:var(--blue);color:var(--blue)}
@keyframes slideIn{from{transform:translateY(16px);opacity:0}to{transform:translateY(0);opacity:1}}

/* Error banner */
.error-banner{display:none;background:var(--red-dim);backdrop-filter:var(--blur);border-bottom:1px solid var(--red);color:var(--red);text-align:center;padding:6px;font-size:9px;font-weight:600;letter-spacing:0.3px}

/* Refresh indicator */
.refresh-dot{width:7px;height:7px;border-radius:50%;background:var(--text-dim);display:inline-block;transition:all 0.2s cubic-bezier(0.25,0.1,0.25,1)}
.refresh-dot.flash{background:var(--accent);box-shadow:0 0 10px var(--accent);transform:scale(1.3)}

/* BP Detail panel */
.bp-detail-panel{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:var(--glass-strong);backdrop-filter:var(--blur);-webkit-backdrop-filter:var(--blur);border:1px solid var(--border-light);border-radius:var(--radius);padding:0;z-index:1001;min-width:320px;max-width:520px;box-shadow:var(--shadow-lg);animation:fadeIn 0.2s cubic-bezier(0.25,0.1,0.25,1)}
.bp-detail-panel::before{content:'';position:fixed;inset:0;background:rgba(0,0,0,0.35);z-index:-1;backdrop-filter:blur(4px)}
.bp-detail-header{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-bottom:1px solid var(--border);font-weight:600;font-size:11px}
.bp-detail-title{color:var(--text-bright)}
.bp-detail-close{background:var(--surface);border:1px solid var(--border);color:var(--text-dim);cursor:pointer;font-size:13px;padding:3px 8px;border-radius:20px;transition:all 0.2s}
.bp-detail-close:hover{color:var(--text);background:var(--surface-hover);border-color:var(--border-light)}
.bp-detail-body{padding:12px 14px;font-size:10px}
.detail-row{display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--border)}
.detail-row .val{font-weight:600;font-family:var(--mono)}
.detail-trend{display:flex;gap:5px;margin-top:5px}
@keyframes fadeIn{from{opacity:0;transform:translate(-50%,-48%) scale(0.97)}to{opacity:1;transform:translate(-50%,-50%) scale(1)}}

/* ── Responsive ── */
@media(max-width:1100px){.info-panel{flex:0 0 170px}.activity-panel{flex:0 0 300px}.bp-grid{grid-template-columns:repeat(auto-fill,minmax(210px,1fr))}}
@media(max-width:800px){.main-wrap{flex-direction:column}.activity-panel{flex:0 0 auto;max-height:260px;border-right:none;border-bottom:1px solid var(--border)}.info-panel{flex:0 0 auto;border-left:none;border-top:1px solid var(--border);max-height:220px}.bp-grid{grid-template-columns:1fr}.active-grid{grid-template-columns:1fr 1fr}}
@media(max-width:500px){.topbar{gap:6px;padding:6px 10px;font-size:9px}.topbar .title{font-size:12px}.active-grid{grid-template-columns:1fr}.pipeline-bar{gap:6px;padding:8px 10px}.toolbar{flex-wrap:wrap}}
</style>
</head>
<body>

<div class="topbar" role="banner">
  <span class="title" aria-label="Forge Command Center">⚡ FORGE CMD CTR</span>
  <span class="divider" aria-hidden="true"></span>
  <span class="stat"><span class="lock-dot" id="lockDot" aria-label="Forge lock status"></span><span id="lockLabel">idle</span></span>
  <span class="stat"><span class="num" id="statLoop">-</span><span class="label">loops</span></span>
  <span class="stat"><span class="num" id="statAgents">-</span><span class="label">agents</span></span>
  <span class="stat"><span class="num" id="statEvals">-</span><span class="label">evals</span></span>
  <span class="stat"><span class="num" id="statActive">0</span><span class="label">active</span></span>
  <span class="spacer"></span>
  <button id="themeToggle" class="theme-btn" onclick="toggleTheme()" aria-label="Toggle light/dark theme" title="Toggle theme">🌙</button>
  <span class="stat" style="cursor:pointer;gap:2px" onclick="fetchState();showRefreshIndicator()" title="Click to refresh (or press R)">
    <span class="refresh-dot" id="refreshIndicator"></span>
    <span style="font-size:9px;color:var(--text-dim)" id="lastUpdateTime">--:--:--</span>
  </span>
  <span id="cavemanBadge" class="badge badge-on">CAVEMAN ON</span>
  <span id="peakBadge" class="peak-badge peak-off">⚡ PEAK</span>
  <span style="color:var(--text-dim);font-size:9px;font-family:var(--mono)" id="uptimeDisplay">0s</span>
</div>

<div class="error-banner" id="errorBanner" role="alert"></div>

<div class="main-wrap" role="main">
  <!-- Left: Activity Feed -->
  <div class="activity-panel" role="complementary" aria-label="Activity feed">
    <div class="activity-header">
      <span>📡 LIVE ACTIVITY</span>
      <span id="activityCount">0</span>
    </div>
    <div class="activity-list" id="activityList" role="log" aria-live="polite"></div>
  </div>

  <!-- Center -->
  <div class="center-panel">
    <div class="pipeline-bar" id="pipelineBar" role="region" aria-label="Pipeline overview">
      <div class="pipeline-stage refinery" tabindex="0">
        <div class="count" id="pipeRefinery">-</div>
        <div class="label">Refinery</div>
      </div>
      <div class="pipeline-stage production" tabindex="0">
        <div class="count" id="pipeProduction">-</div>
        <div class="label">Production</div>
      </div>
      <div class="pipeline-stage archive" tabindex="0">
        <div class="count" id="pipeArchive">-</div>
        <div class="label">Archive</div>
      </div>
    </div>

    <div class="active-section" id="activeSection" role="region" aria-label="Active processes">
      <div class="section-title">▶ Active Processes <span class="section-count" id="activeCount">0</span></div>
      <div class="active-grid" id="activeGrid"></div>
    </div>

    <!-- Score distribution -->
    <div class="score-dist" id="scoreDist" role="region" aria-label="Score distribution">
      <div class="dist-bar" onclick="setScoreFilter('95',this)" title="Click to filter: 95+ score"><div class="dist-count" id="dist95">0</div><div class="dist-fill" style="background:var(--green)" id="distBar95"></div><div class="dist-label">95+</div></div>
      <div class="dist-bar" onclick="setScoreFilter('85',this)" title="Click to filter: 85+ score"><div class="dist-count" id="dist85">0</div><div class="dist-fill" style="background:var(--green)" id="distBar85"></div><div class="dist-label">85+</div></div>
      <div class="dist-bar" onclick="setScoreFilter('70',this)" title="Click to filter: 70+ score"><div class="dist-count" id="dist70">0</div><div class="dist-fill" style="background:var(--amber)" id="distBar70"></div><div class="dist-label">70+</div></div>
      <div class="dist-bar" onclick="setScoreFilter('50',this)" title="Click to filter: 50+ score"><div class="dist-count" id="dist50">0</div><div class="dist-fill" style="background:var(--amber)" id="distBar50"></div><div class="dist-label">50+</div></div>
      <div class="dist-bar" onclick="setScoreFilter('0',this)" title="Click to filter: &lt;50 score"><div class="dist-count" id="dist0">0</div><div class="dist-fill" style="background:var(--red)" id="distBar0"></div><div class="dist-label">&lt;50</div></div>
    </div>

    <!-- Search + filters -->
    <div class="toolbar" role="toolbar" aria-label="Blueprint filters">
      <input type="search" class="search-box" id="bpSearch" placeholder="🔍 Search blueprints..." aria-label="Search blueprints">
      <button class="filter-btn active" data-filter="all" onclick="setFilter('all',this)" aria-pressed="true">All</button>
      <button class="filter-btn" data-filter="production" onclick="setFilter('production',this)" aria-pressed="false">Production</button>
      <button class="filter-btn" data-filter="refinery" onclick="setFilter('refinery',this)" aria-pressed="false">Refinery</button>
      <button class="filter-btn" data-filter="archive" onclick="setFilter('archive',this)" aria-pressed="false">Archive</button>
      <select class="sort-select" id="bpSort" onchange="render()" aria-label="Sort blueprints">
        <option value="best">Best score</option>
        <option value="latest">Latest score</option>
        <option value="name">Name</option>
        <option value="evals">Most evals</option>
      </select>
    </div>

    <!-- Blueprint cards -->
    <div class="bp-section" role="region" aria-label="Blueprint scores">
      <div class="bp-grid" id="bpGrid"></div>
    </div>
  </div>

  <!-- Right: Info -->
  <div class="info-panel" id="infoPanel" role="complementary" aria-label="Forge information">
    <div class="info-section">
      <div class="info-title">Forge</div>
      <div class="info-row"><span class="key">Codename</span><span class="val" id="infoCodename">-</span></div>
      <div class="info-row"><span class="key">Version</span><span class="val" id="infoVersion">-</span></div>
      <div class="info-row"><span class="key">Checkpoint</span><span class="val" id="infoCheckpoint" style="font-size:8px">-</span></div>
    </div>
    <div class="info-section">
      <div class="info-title">Pipeline</div>
      <div class="info-row"><span class="key">Total</span><span class="val" id="infoTotalAgents">-</span></div>
      <div class="info-row"><span class="key">Evals</span><span class="val" id="infoTotalEvals">-</span></div>
      <div class="info-row"><span class="key">Loops</span><span class="val" id="infoLoopIter">-</span></div>
      <div class="info-row"><span class="key">Blueprints</span><span class="val" id="infoBpCount">-</span></div>
    </div>
    <div class="info-section">
      <div class="info-title">Lock</div>
      <div class="info-row"><span class="key">PID</span><span class="val green" id="infoLockPid">-</span></div>
      <div class="info-row"><span class="key">Since</span><span class="val" id="infoLockTime">-</span></div>
    </div>
    <div class="info-section">
      <div class="info-title">Status</div>
      <div class="info-row"><span class="key">Avg Score</span><span class="val amber" id="infoAvgScore">-</span></div>
      <div class="info-row"><span class="key">≥85</span><span class="val green" id="infoHighScore">-</span></div>
      <div class="info-row"><span class="key">Server</span><span class="val" id="infoUptime">-</span></div>
    </div>
  </div>
</div>

<div id="toastContainer" aria-live="assertive"></div>

<script>
"use strict";
let state = {};
let currentFilter = "all";
let currentScoreFilter = null;
let errorCount = 0;

// ── Theme toggle ──
function getTheme() {
  try { return localStorage.getItem("forge-cc-theme") || "dark"; }
  catch(e) { return "dark"; }
}
function setTheme(theme) {
  try { localStorage.setItem("forge-cc-theme", theme); }
  catch(e) {}
  applyTheme(theme);
}
function applyTheme(theme) {
  const html = document.documentElement;
  const btn = document.getElementById("themeToggle");
  if (theme === "light") {
    html.classList.add("light-theme");
    if (btn) btn.textContent = "☀️";
  } else {
    html.classList.remove("light-theme");
    if (btn) btn.textContent = "🌙";
  }
}
function toggleTheme() {
  const current = getTheme();
  setTheme(current === "dark" ? "light" : "dark");
}
// Apply saved theme on load
applyTheme(getTheme());

function fmtTime(ts) {
  if (!ts) return "";
  try {
    const d = new Date(ts), diff = Math.floor((Date.now() - d.getTime()) / 1000);
    if (diff < 5) return "now";
    if (diff < 60) return diff + "s";
    if (diff < 3600) return Math.floor(diff/60) + "m";
    if (diff < 86400) return Math.floor(diff/3600) + "h";
    return d.toLocaleDateString();
  } catch(e) { return ts; }
}

function scoreClass(s) {
  if (!s && s !== 0) return "score-0";
  if (s >= 85) return "score-high";
  if (s >= 60) return "score-mid";
  return "score-low";
}

function barColor(s) {
  if (s >= 85) return "var(--green)";
  if (s >= 60) return "var(--amber)";
  if (s >= 30) return "var(--red)";
  return "var(--text-dim)";
}

function actionIcon(a) {
  const map = {spawn:"🌱",eval:"📊",improve:"🔧",loop:"🔄",promote:"🏆",archive:"📦"};
  return map[a] || "•";
}

function toast(msg, type) {
  type = type || "error";
  const el = document.createElement("div");
  el.className = "toast " + (type === "info" ? "info" : "");
  el.textContent = msg;
  el.setAttribute("role","alert");
  document.getElementById("toastContainer").appendChild(el);
  setTimeout(function(){ el.remove(); }, 4000);
}

function setFilter(f, btn) {
  currentFilter = f;
  currentScoreFilter = null;
  document.querySelectorAll(".filter-btn").forEach(function(b){
    b.classList.remove("active");
    b.setAttribute("aria-pressed","false");
  });
  if (btn) {
    btn.classList.add("active");
    btn.setAttribute("aria-pressed","true");
  }
  document.querySelectorAll(".dist-bar").forEach(function(b){ b.classList.remove("active"); });
  render();
}

function setScoreFilter(range, el) {
  if (currentScoreFilter === range) {
    currentScoreFilter = null;
    if (el) el.classList.remove("active");
  } else {
    currentScoreFilter = range;
    document.querySelectorAll(".dist-bar").forEach(function(b){ b.classList.remove("active"); });
    if (el) el.classList.add("active");
    // Deselect stage filter buttons
    document.querySelectorAll(".filter-btn").forEach(function(b){
      b.classList.remove("active");
      b.setAttribute("aria-pressed","false");
    });
    currentFilter = "all";
  }
  render();
}

function render() {
  const d = state;
  if (!d || !d.forge) return;

  // Topbar
  const lock = d.forge_lock;
  const lockEl = document.getElementById("lockDot");
  if (lock) {
    lockEl.className = "lock-dot lock-locked";
    lockEl.setAttribute("aria-label","Forge running");
    document.getElementById("lockLabel").textContent = "running";
  } else {
    lockEl.className = "lock-dot lock-free";
    lockEl.setAttribute("aria-label","Forge idle");
    document.getElementById("lockLabel").textContent = "idle";
  }
  document.getElementById("statLoop").textContent = d.forge.loop_iterations || 0;
  document.getElementById("statAgents").textContent = d.forge.total_agents || 0;
  document.getElementById("statEvals").textContent = d.forge.total_evaluations || 0;
  const active = d.active_processes || [];
  document.getElementById("statActive").textContent = active.length;

  const cav = document.getElementById("cavemanBadge");
  const cu = d.forge.caveman_ultra;
  cav.textContent = cu ? "CAVEMAN ON" : "CAVEMAN OFF";
  cav.className = "badge " + (cu ? "badge-on" : "badge-off");

  const pk = d.peak_hours || {};
  const pb = document.getElementById("peakBadge");
  if (pk.active) {
    pb.textContent = "⚡ PEAK " + (pk.ends || "");
    pb.className = "peak-badge peak-on";
    pb.title = "DeepSeek 2x pricing! " + (pk.slots||"");
  } else {
    pb.textContent = "⚡ OFF-PEAK";
    pb.className = "peak-badge peak-off";
    pb.title = "DeepSeek off-peak. " + (pk.slots||"");
  }
  document.getElementById("uptimeDisplay").textContent = Math.floor(d.uptime/60) + "m";

  // Pipeline
  const pipe = d.pipeline || {};
  document.getElementById("pipeRefinery").textContent = pipe.refinery || 0;
  document.getElementById("pipeProduction").textContent = pipe.production || 0;
  document.getElementById("pipeArchive").textContent = pipe.archive || 0;

  // Activity
  const acts = d.activity || [];
  const al = document.getElementById("activityList");
  document.getElementById("activityCount").textContent = acts.length;
  if (acts.length === 0) {
    al.innerHTML = '<div class="empty-state"><div class="icon">📡</div>No forge activity yet<br><span style="font-size:9px">Start a forge run to see activity</span></div>';
  } else {
    al.innerHTML = acts.map(function(a){
      const st = a.status === "running" ? "running" : a.status === "complete" ? "complete" : "failed";
      const pct = Math.min(a.progress || 0, 100);
      return '<div class="activity-item '+st+'" role="listitem">'
        +'<span class="activity-icon" aria-hidden="true">'+actionIcon(a.action)+'</span>'
        +'<div class="activity-body">'
        +'<div><span class="activity-action '+a.action+'">'+a.action+'</span> <span class="activity-bp">'+(a.blueprint||"?")+'</span></div>'
        +'<div class="activity-detail">'+(a.detail||"")+'</div>'
        +(st==="running"?'<div class="activity-progress" role="progressbar" aria-valuenow="'+pct+'" aria-valuemin="0" aria-valuemax="100"><div class="fill" style="width:'+pct+'%"></div></div>':"")
        +'</div>'
        +'<span class="activity-time">'+fmtTime(a.timestamp)+'</span>'
        +'</div>';
    }).join("");
  }

  // Active processes
  const ag = document.getElementById("activeGrid");
  document.getElementById("activeCount").textContent = active.length;
  if (active.length === 0) {
    ag.innerHTML = '<div class="empty-state" style="padding:10px;font-size:9px">No active processes</div>';
  } else {
    ag.innerHTML = active.map(function(a){
      const pct = Math.min(a.progress || 0, 100);
      return '<div class="active-card">'
        +'<div class="ac-action">'+a.action+'</div>'
        +'<div class="ac-bp">'+a.blueprint+'</div>'
        +'<div class="ac-detail">'+(a.detail||"").slice(0,50)+'</div>'
        +'<div class="ac-progress" role="progressbar" aria-valuenow="'+pct+'" aria-valuemin="0" aria-valuemax="100"><div class="fill" style="width:'+pct+'%"></div></div>'
        +'</div>';
    }).join("");
  }

  // Score distribution
  const bps = d.bp_scores || {};
  const entries = Object.entries(bps);
  const dist = {95:0, 85:0, 70:0, 50:0, 0:0};
  entries.forEach(function(e){
    const s = e[1].best || 0;
    if (s >= 95) dist[95]++;
    else if (s >= 85) dist[85]++;
    else if (s >= 70) dist[70]++;
    else if (s >= 50) dist[50]++;
    else dist[0]++;
  });
  const maxDist = Math.max(1, ...Object.values(dist));
  const total = entries.length || 1;
  var distLabels = {"95":"95+","85":"85+","70":"70+","50":"50+","0":"<50"};
  ["95","85","70","50","0"].forEach(function(k){
    document.getElementById("dist"+k).textContent = dist[k];
    document.getElementById("distBar"+k).style.height = Math.max(2, (dist[k]/maxDist)*40) + "px";
    // Update tooltip with percentage
    var pct = ((dist[k] / total) * 100).toFixed(1);
    var barEl = document.getElementById("distBar"+k).parentElement;
    barEl.title = distLabels[k] + ": " + dist[k] + " av " + total + " (" + pct + "%) — Klicka för att filtrera";
  });

  // Filter + sort blueprints
  const search = (document.getElementById("bpSearch").value || "").toLowerCase();
  const sort = document.getElementById("bpSort").value;
  let filtered = entries.filter(function(e){
    const info = e[1];
    if (currentFilter === "production" && info.stage !== "production") return false;
    if (currentFilter === "refinery" && info.stage === "production") return false;
    if (currentFilter === "archive" && info.stage !== "archive") return false;
    if (search && !e[0].toLowerCase().includes(search)) return false;
    // Score filter
    if (currentScoreFilter) {
      const s = info.best || 0;
      const r = parseInt(currentScoreFilter);
      if (r === 95 && s < 95) return false;
      else if (r === 85 && (s < 85 || s >= 95)) return false;
      else if (r === 70 && (s < 70 || s >= 85)) return false;
      else if (r === 50 && (s < 50 || s >= 70)) return false;
      else if (r === 0 && s >= 50) return false;
    }
    return true;
  });

  // Sort
  if (sort === "best") filtered.sort(function(a,b){ return (b[1].best||0) - (a[1].best||0); });
  else if (sort === "latest") filtered.sort(function(a,b){ return (b[1].latest||0) - (a[1].latest||0); });
  else if (sort === "name") filtered.sort(function(a,b){ return a[0].localeCompare(b[0]); });
  else if (sort === "evals") filtered.sort(function(a,b){ return (b[1].count||0) - (a[1].count||0); });

  const bg = document.getElementById("bpGrid");
  if (filtered.length === 0) {
    bg.innerHTML = '<div class="empty-state"><div class="icon">🔍</div>No blueprints match<br><span style="font-size:9px">Try a different filter or search term</span></div>';
  } else {
    bg.innerHTML = filtered.map(function(e){
      const name = e[0], info = e[1];
      const best = info.best || 0;
      const latest = info.latest || 0;
      const pct = Math.min(best, 100);
      const stage = info.stage || "refinery";
      const stageClass = stage === "production" ? "prod" : stage === "archive" ? "arch" : "ref";
      const stageLabel = stage === "production" ? "PROD" : stage === "archive" ? "ARCH" : "REF";
      const hist = (info.history||[]).slice(0,3).map(function(h){
        const s = h.score||0;
        return '<span class="bp-dot" style="background:'+barColor(s)+'" title="Score: '+s.toFixed(1)+'" aria-label="Score '+Math.round(s)+'">'+Math.round(s)+'</span>';
      }).join("");
      // Trend arrow
      var trendIcon = "→", trendClass = "flat";
      if (info.trend === "up") { trendIcon = "↑"; trendClass = "up"; }
      else if (info.trend === "down") { trendIcon = "↓"; trendClass = "down"; }
      var trendTitle = "Trend: " + (info.trend==="up"?"Stigande":info.trend==="down"?"Själande":"Oförändrad");
      if (info.prev_score !== undefined) trendTitle += " (förra: " + info.prev_score.toFixed(1) + ")";
      return '<div class="bp-card" tabindex="0" role="listitem" aria-label="'+name+' score '+best.toFixed(1)+'" onclick="toggleDetail(\''+name+'\')" onkeydown="if(event.key===\'Enter\')toggleDetail(\''+name+'\')">'
        +'<span class="bp-stage '+stageClass+'" aria-label="Stage '+stageLabel+'">'+stageLabel+'</span>'
        +'<span class="bp-name" title="'+name+'">'+name+'</span>'
        +'<span class="bp-trend '+trendClass+'" title="'+trendTitle+'">'+trendIcon+'</span>'
        +'<span class="bp-evals" title="'+info.count+' evaluations">'+info.count+'x</span>'
        +'<div class="bp-bar"><div class="fill" style="width:'+pct+'%;background:'+barColor(best)+'"></div></div>'
        +'<span class="bp-score '+scoreClass(best)+'" title="Latest: '+latest.toFixed(1)+'">'+best.toFixed(1)+'</span>'
        +(hist?'<span class="bp-history">'+hist+'</span>':"")
        +'</div>';
    }).join("");
  }

  // Info panel
  const f = d.forge || {};
  document.getElementById("infoCodename").textContent = f.codename || "-";
  document.getElementById("infoVersion").textContent = f.version || "-";
  document.getElementById("infoCheckpoint").textContent = (f.last_checkpoint || "-").slice(0,22);
  document.getElementById("infoTotalAgents").textContent = f.total_agents || 0;
  document.getElementById("infoTotalEvals").textContent = f.total_evaluations || 0;
  document.getElementById("infoLoopIter").textContent = f.loop_iterations || 0;

  // Blueprint count
  const uniqueBps = Object.keys(bps).length;
  document.getElementById("infoBpCount").textContent = uniqueBps;

  // Lock
  const lp = document.getElementById("infoLockPid");
  if (lock) {
    lp.textContent = lock.pid || "?";
    lp.className = "val green";
    document.getElementById("infoLockTime").textContent = lock.acquired ? (lock.acquired+"").slice(11,19) : "?";
  } else {
    lp.textContent = "none";
    lp.className = "val";
    document.getElementById("infoLockTime").textContent = "-";
  }

  // Stats
  const allBest = entries.map(function(e){ return e[1].best||0; });
  if (allBest.length) {
    const avg = allBest.reduce(function(a,b){ return a+b; }, 0) / allBest.length;
    document.getElementById("infoAvgScore").textContent = avg.toFixed(1);
    document.getElementById("infoHighScore").textContent = allBest.filter(function(s){ return s >= 85; }).length;
  }
  document.getElementById("infoUptime").textContent = Math.floor(d.uptime/60) + "m";
  
  // Last updated
  document.getElementById("lastUpdateTime").textContent = new Date().toLocaleTimeString();
}

let _animFrame = null;
function animateValue(el, oldVal, newVal, duration) {
  if (oldVal === newVal) { el.textContent = newVal; return; }
  const start = performance.now();
  const diff = newVal - oldVal;
  function step(now) {
    const pct = Math.min((now - start) / duration, 1);
    el.textContent = Math.round(oldVal + diff * pct);
    if (pct < 1) _animFrame = requestAnimationFrame(step);
  }
  if (_animFrame) cancelAnimationFrame(_animFrame);
  _animFrame = requestAnimationFrame(step);
}

function toggleDetail(name) {
  const existing = document.getElementById("bp-detail");
  if (existing) existing.remove();
  
  const info = (state.bp_scores || {})[name];
  if (!info) return;
  
  const detail = document.createElement("div");
  detail.id = "bp-detail";
  detail.className = "bp-detail-panel";
  detail.setAttribute("role", "dialog");
  detail.setAttribute("aria-label", name + " details");
  detail.innerHTML = '<div class="bp-detail-header">'
    +'<span class="bp-detail-title">'+name+'</span>'
    +'<button class="bp-detail-close" onclick="document.getElementById(\"bp-detail\").remove()" aria-label="Close">✕</button>'
    +'</div>'
    +'<div class="bp-detail-body">'
    +'<div class="detail-row"><span>Best Score</span><span class="val" style="color:'+barColor(info.best||0)+'">'+(info.best||0).toFixed(1)+'</span></div>'
    +'<div class="detail-row"><span>Latest Score</span><span class="val" style="color:'+barColor(info.latest||0)+'">'+(info.latest||0).toFixed(1)+'</span></div>'
    +'<div class="detail-row"><span>Stage</span><span class="val">'+(info.stage||"?").toUpperCase()+'</span></div>'
    +'<div class="detail-row"><span>Evaluations</span><span class="val">'+(info.count||0)+'</span></div>'
    +'<div class="detail-row"><span>Score Trend</span></div>'
    +'<div class="detail-trend">'+(info.history||[]).slice(0,5).map(function(h){
        const s = h.score||0;
        return '<span class="bp-dot" style="background:'+barColor(s)+'" title="'+s.toFixed(1)+'">'+Math.round(s)+'</span>';
      }).join(" ")+'</div>'
    +'</div>';
  document.body.appendChild(detail);
  detail.addEventListener("click", function(e){ if (e.target === detail) detail.remove(); });
}

// Keyboard shortcuts
document.addEventListener("keydown", function(e) {
  if (e.key === "r" && !e.ctrlKey && !e.altKey && !e.metaKey && document.activeElement === document.body) {
    fetchState();
    showRefreshIndicator();
  }
  if (e.key === "Escape") {
    const d = document.getElementById("bp-detail");
    if (d) d.remove();
  }
  if ((e.ctrlKey || e.metaKey) && e.key === "f") {
    e.preventDefault();
    document.getElementById("bpSearch").focus();
  }
});

function showRefreshIndicator() {
  const el = document.getElementById("refreshIndicator");
  el.classList.add("flash");
  setTimeout(function(){ el.classList.remove("flash"); }, 300);
}

async function fetchState() {
  try {
    const r = await fetch("/api/state");
    if (!r.ok) throw new Error("HTTP "+r.status);
    state = await r.json();
    errorCount = 0;
    render();
    document.getElementById("errorBanner").style.display = "none";
  } catch(e) {
    errorCount++;
    if (errorCount === 1) toast("Connection lost — retrying...", "error");
    if (errorCount >= 3) {
      document.getElementById("errorBanner").style.display = "block";
      document.getElementById("errorBanner").textContent = "⚠ Connection lost — retrying every 3s...";
    }
  }
}

// Event listeners
document.getElementById("bpSearch").addEventListener("input", render);

// ── SSE live updates with polling fallback ──
function connectSSE() {
  if (typeof EventSource === "undefined") {
    // Fallback to polling for browsers without SSE support
    console.log("SSE not supported, falling back to 3s polling");
    fetchState();
    setInterval(fetchState, 3000);
    return;
  }

  const es = new EventSource("/api/stream");
  es.onopen = function() {
    errorCount = 0;
    document.getElementById("errorBanner").style.display = "none";
    showRefreshIndicator();
  };
  es.onmessage = function(e) {
    try {
      state = JSON.parse(e.data);
      errorCount = 0;
      render();
      document.getElementById("errorBanner").style.display = "none";
      showRefreshIndicator();
    } catch(err) {
      errorCount++;
      if (errorCount === 1) toast("Parse error — retrying...", "error");
    }
  };
  es.onerror = function(e) {
    errorCount++;
    if (errorCount >= 3) {
      document.getElementById("errorBanner").style.display = "block";
      document.getElementById("errorBanner").textContent = "\u26a0 Connection lost — SSE reconnecting...";
    }
    // EventSource auto-reconnects after ~3s by default
  };
}

// Init
connectSSE();
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def _send_response(self, body, content_type, code=200, cache="no-cache", extra_headers=None):
        """Send response with optional GZIP compression."""
        # GZIP if client supports it and body > 1KB
        accept_encoding = self.headers.get("Accept-Encoding", "")
        if "gzip" in accept_encoding and len(body) > 1024:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb", compresslevel=5) as gz:
                gz.write(body if isinstance(body, bytes) else body.encode())
            body = buf.getvalue()
            content_encoding = "gzip"
        else:
            content_encoding = None
        
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options", "nosniff")
        if content_encoding:
            self.send_header("Content-Encoding", content_encoding)
            self.send_header("Vary", "Accept-Encoding")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        try:
            self.wfile.write(body)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass  # client disconnected, nothing to do
    
    def _send_sse_headers(self):
        """Send SSE stream headers (no Content-Length, chunked transfer)."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

    def handle(self):
        """Override to suppress connection-aborted tracebacks."""
        try:
            super().handle()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            pass
    
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send_response(INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path == "/favicon.ico":
            # Tiny inline favicon (forge icon)
            fav = b"\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x20\x00\x68\x04\x00\x00\x16\x00\x00\x00" + b"\x00" * 100
            self._send_response(fav, "image/x-icon", cache="max-age=86400")
        elif self.path == "/api/state":
            data = get_state()
            body = json.dumps(data, default=str).encode("utf-8")
            self._send_response(body, "application/json",
                               extra_headers={"Access-Control-Allow-Origin": "*"})
        elif self.path == "/api/stream":
            self._send_sse_headers()
            try:
                while True:
                    data = get_state()
                    payload = f"data: {json.dumps(data, default=str)}\n\n"
                    self.wfile.write(payload.encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(3)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass
        elif self.path == "/api/debug":
            import time as _t
            info = {
                "cached": bool(_cached_result),
                "cache_age": _t.time() - _last_scan if _last_scan else -1,
                "cache_ttl": SCAN_INTERVAL,
                "cache_keys": list(_cached_result.keys()) if _cached_result else [],
                "bp_count": len(_cached_result.get("bp_scores", {})) if _cached_result else 0,
            }
            self._send_response(json.dumps(info).encode(), "application/json")
        else:
            self._send_response(b"Not found", "text/plain", code=404)

    def log_message(self, *args):
        pass


def main():
    import socket
    # Pre-warm cache before accepting connections
    print("Pre-warming cache...", flush=True)
    t0 = time.time()
    get_state()
    print(f"Cache warm: {time.time()-t0:.1f}s — ready to serve", flush=True)
    
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.allow_reuse_address = True
    print(f"\u26a1 Forge Command Center v3 \u2192 http://localhost:{PORT}")
    print(f"   Cache TTL: {SCAN_INTERVAL}s, os.scandir() for speed")
    print(f"   Responsive, accessible, with search & filters")
    print(f"   Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.server_close()


if __name__ == "__main__":
    main()
