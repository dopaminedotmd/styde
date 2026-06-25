"""
Styde Forge Dashboard v3 — Premium Mission Control.

Run: python Core/dashboard.py
Open: http://localhost:8765

SSE real-time. Animated. KPI cards. Score chart. Agent leaderboard.
Blueprint details. Cost tracking. Toast notifications.
"""
import json
import yaml
import time
import threading
from pathlib import Path
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue

FORGE_ROOT = Path(__file__).resolve().parent.parent
PORT = 8765

sse_clients: list[Queue] = []
sse_lock = threading.Lock()

def broadcast(data: str):
    with sse_lock:
        dead = []
        for q in sse_clients:
            try: q.put_nowait(data)
            except: dead.append(q)
        for q in dead: sse_clients.remove(q)

def load_state():
    path = FORGE_ROOT / "state.yaml"
    if not path.exists(): return {}
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def get_agents(state):
    agents = state.get("agents", [])
    return (
        sum(1 for a in agents if a.get("stage") == "refinery"),
        sum(1 for a in agents if a.get("stage") == "production"),
        sum(1 for a in agents if a.get("stage") == "archive"),
    )

def get_scores(state):
    return [e.get("composite_score", 0) for e in state.get("evaluations", [])[-40:]]

def get_checkpoints():
    cp_dir = FORGE_ROOT / "checkpoints"
    if not cp_dir.exists(): return []
    cps = []
    for cp in sorted(cp_dir.glob("checkpoint-*"), reverse=True)[:10]:
        if cp.name.startswith("."): continue
        m = cp / "checkpoint_manifest.json"
        if m.exists():
            d = json.loads(m.read_text(encoding="utf-8"))
            cps.append({"id": cp.name[:35], "created": d.get("created","?")[:19], "label": d.get("label",""), "loops": d.get("loop_iterations",0)})
    return cps

def get_recent_agents(state):
    agents = state.get("agents", [])
    evals = state.get("evaluations", [])
    improvements = state.get("improvements", [])
    recent = sorted(agents, key=lambda a: a.get("spawned_at",""), reverse=True)[:25]
    result = []
    for a in recent:
        score = None
        dims = {}
        teacher_diag = ""
        for e in evals:
            if e.get("run_id") == a.get("run_id"):
                score = e.get("composite_score")
                break
        for imp in improvements:
            if imp.get("run_id") == a.get("run_id"):
                teacher_diag = imp.get("diagnosis", "") or imp.get("summary", "")
                break
        result.append({
            "run_id": a.get("run_id","?")[:15],
            "blueprint": a.get("blueprint","?"),
            "stage": a.get("stage","?"),
            "status": a.get("status","?"),
            "score": score,
            "spawned": (a.get("spawned_at","") or "")[:16],
            "teacher": teacher_diag[:60],
            "version": a.get("version",""),
        })
    return result

def get_blueprints():
    bp_dir = FORGE_ROOT / "blueprints"
    if not bp_dir.exists(): return []
    bps = []
    for d in sorted(bp_dir.iterdir()):
        if d.is_dir() and not d.name.startswith("."):
            config = d / "config.yaml"
            version = "?"
            domain = ""
            if config.exists():
                try:
                    cfg = yaml.safe_load(config.read_text(encoding="utf-8"))
                    bp = cfg.get("blueprint", {})
                    version = bp.get("version", "?")
                    domain = bp.get("domain", "")
                except: pass
            bps.append({"name": d.name, "version": str(version), "domain": domain})
    return bps

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
            if output.exists():
                runs.append((run_dir.name, bp_dir.name, output.read_text(encoding="utf-8")[:800], output.stat().st_mtime))
                break
    if not runs: return None
    runs.sort(key=lambda r: r[3], reverse=True)
    return runs[0]

def get_leaderboard(state):
    """Top production agents by score."""
    agents = state.get("agents", [])
    evals = state.get("evaluations", [])
    scored = []
    for a in agents:
        if a.get("stage") != "production": continue
        for e in evals:
            if e.get("run_id") == a.get("run_id"):
                scored.append({
                    "blueprint": a.get("blueprint","?"),
                    "score": e.get("composite_score", 0),
                    "run_id": a.get("run_id","?")[:12],
                })
                break
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:8]

def estimate_cost(state):
    """Rough cost estimate based on spawns and evals."""
    spawns = state.get("total_agents_spawned", 0)
    evals = state.get("total_evaluations", 0)
    # Assume ~2000 tokens per spawn, ~500 per eval. DeepSeek ~$0.27/1M tokens.
    spawn_tokens = spawns * 2000
    eval_tokens = evals * 500 * 2  # self + judge
    total_tokens = spawn_tokens + eval_tokens
    cost = total_tokens * 0.27 / 1_000_000
    return {"tokens": total_tokens, "cost": round(cost, 4)}

def get_system_health():
    import psutil
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage(str(FORGE_ROOT))
    return {
        "cpu": cpu,
        "ram_pct": mem.percent,
        "ram_gb": round(mem.used / (1024**3), 1),
        "ram_total": round(mem.total / (1024**3), 1),
        "disk_pct": disk.percent,
        "disk_free": round(disk.free / (1024**3), 1),
    }

def build_state_json():
    state = load_state()
    refinery, production, archive = get_agents(state)
    scores = get_scores(state)
    cost = estimate_cost(state)
    health = get_system_health()

    return json.dumps({
        "ts": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        "version": state.get("forge_version","?"),
        "hardware": state.get("hardware_profile","?"),
        "caveman": state.get("caveman_ultra", False),
        "loops": state.get("loop_iterations", 0),
        "spawned": state.get("total_agents_spawned", 0),
        "evaluations": state.get("total_evaluations", 0),
        "refinery": refinery, "production": production, "archive": archive,
        "last_checkpoint": (state.get("last_checkpoint") or "")[:35],
        "scores": scores,
        "score_avg": round(sum(scores)/len(scores),1) if scores else 0,
        "score_max": max(scores) if scores else 0,
        "score_min": min(scores) if scores else 0,
        "score_trend": "up" if len(scores)>=2 and scores[-1]>scores[-2] else ("down" if len(scores)>=2 and scores[-1]<scores[-2] else "flat"),
        "checkpoints": get_checkpoints(),
        "agents": get_recent_agents(state),
        "blueprints": get_blueprints(),
        "leaderboard": get_leaderboard(state),
        "cost": cost,
        "health": health,
        "latest_output": None,
    })

def sse_broadcaster():
    while True:
        try:
            data = build_state_json()
            broadcast(f"data: {data}\n\n")
        except: pass
        time.sleep(2)


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Styde Forge — Mission Control</title>
<style>
:root{--bg:#060612;--card:#0c0c22;--border:#1a1a40;--text:#b0b0c8;--dim:#505080;--accent:#5060e0;--green:#30c050;--yellow:#c0a030;--red:#e04040;--blue:#4080ff}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font:13px/1.5 'Segoe UI','Inter',system-ui,sans-serif;padding:20px}
h1{font-size:22px;font-weight:700;color:#d0d0f0;letter-spacing:-0.5px}
h1 span{color:var(--accent)}
.sub{color:var(--dim);font-size:11px;margin-bottom:18px}
.live-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--green);margin-right:5px;animation:pulse 1.5s infinite;vertical-align:middle}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 8px var(--green)}50%{opacity:.3;box-shadow:0 0 2px var(--green)}}

/* KPIs */
.kpi-row{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.kpi{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:12px 18px;min-width:100px;text-align:center;transition:transform .2s,box-shadow .2s}
.kpi:hover{transform:translateY(-2px);box-shadow:0 4px 12px rgba(80,96,224,.15)}
.kpi .num{font-size:26px;font-weight:800;color:#e8e8f8;transition:color .3s}
.kpi .lbl{font-size:10px;color:var(--dim);text-transform:uppercase;letter-spacing:1.5px;margin-top:3px}
.kpi-ok{border-color:#1a3a1a}.kpi-ok .num{color:var(--green)}
.kpi-warn{border-color:#3a3a1a}.kpi-warn .num{color:var(--yellow)}
.kpi-hot{border-color:#3a1a1a}.kpi-hot .num{color:var(--red)}
.kpi-blue{border-color:#1a2a4a}.kpi-blue .num{color:var(--blue)}

/* Grid */
.grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:14px;max-width:1400px;margin-bottom:14px}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:1400px}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:16px;transition:border-color .3s}
.card:hover{border-color:#282860}
.card h2{color:#7070c0;font-size:10px;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
.card h2 .subtitle{font-size:9px;color:var(--dim);letter-spacing:1px;text-transform:none;font-weight:400}

/* Score chart */
.chart{display:flex;align-items:flex-end;gap:3px;height:90px;position:relative}
.chart .bar{flex:1;min-width:6px;border-radius:2px 2px 0 0;transition:height .3s,background .3s}
.bar-prod{background:linear-gradient(to top,#2040a0,#4070e0)}
.bar-mid{background:linear-gradient(to top,#605020,#a08030)}
.bar-low{background:linear-gradient(to top,#602020,#a04040)}
.score-overlay{position:absolute;top:4px;right:4px;font-size:24px;font-weight:800}
.score-up{color:var(--green)}.score-down{color:var(--red)}.score-flat{color:var(--dim)}
.chart-legend{display:flex;gap:16px;margin-top:6px;font-size:10px;color:var(--dim)}
.chart-legend span{display:flex;align-items:center;gap:4px}
.chart-legend .swatch{width:12px;height:4px;border-radius:2px}

/* Agent table */
.agent-table{width:100%;font-size:11px;border-collapse:collapse}
.agent-table th{text-align:left;color:var(--dim);font-weight:600;padding:4px 8px;border-bottom:1px solid var(--border);font-size:9px;text-transform:uppercase;letter-spacing:1px}
.agent-table td{padding:5px 8px;border-bottom:1px solid #101028}
.agent-table tr:hover{background:rgba(80,96,224,.05)}
.score-cell{font-weight:700;font-size:13px}
.badge{display:inline-block;padding:1px 7px;border-radius:3px;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.badge-prod{background:#0a1a35;color:var(--blue)}
.badge-ref{background:#1a1a08;color:var(--yellow)}
.badge-arch{background:#1a0a0a;color:var(--red)}

/* Leaderboard */
.lb-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid #101028;font-size:12px}
.lb-row:last-child{border:none}
.lb-rank{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;margin-right:8px}
.lb-rank-1{background:linear-gradient(135deg,#c0a020,#ffd700);color:#000}
.lb-rank-2{background:linear-gradient(135deg,#808090,#c0c0c0);color:#000}
.lb-rank-3{background:linear-gradient(135deg,#804020,#cd7f32);color:#fff}
.lb-rank-n{background:#181838;color:var(--dim)}

/* Checkpoints */
.cp-item{display:flex;justify-content:space-between;font-size:11px;padding:3px 0;border-bottom:1px solid #101028}
.cp-item:last-child{border:none}

/* Blueprint chips */
.bp-grid{display:flex;flex-wrap:wrap;gap:6px;max-height:250px;overflow-y:auto}
.bp-chip{background:#0e0e28;border:1px solid #1a1a40;border-radius:6px;padding:6px 10px;font-size:11px;cursor:pointer;transition:all .2s}
.bp-chip:hover{border-color:var(--accent);background:#121230}
.bp-chip .bp-name{color:#b0b0d0;font-weight:600}
.bp-chip .bp-ver{color:var(--accent);font-size:10px;margin-left:6px}
.bp-chip .bp-domain{color:var(--dim);font-size:9px;display:block}

/* Toast notifications */
.toast-container{position:fixed;top:16px;right:16px;z-index:9999}
.toast{background:#0c1a0c;border:1px solid #1a3a1a;color:var(--green);padding:10px 16px;border-radius:6px;margin-bottom:6px;font-size:12px;animation:slideIn .3s ease;max-width:300px}
@keyframes slideIn{from{transform:translateX(120%);opacity:0}to{transform:translateX(0);opacity:1}}

/* Scrollbar */
::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:#202050;border-radius:3px}

.footer{color:#202050;font-size:10px;text-align:center;margin-top:20px;letter-spacing:1px}

@media(max-width:1000px){.grid{grid-template-columns:1fr}.grid-2{grid-template-columns:1fr}}
</style>
</head>
<body>
<h1>Styde <span>Forge</span> — Mission Control</h1>
<div class="sub"><span class="live-dot"></span> LIVE · The Crucible v3.0 · <span id="clock">--</span> · <span id="hw"></span></div>

<div class="kpi-row" id="kpis"></div>

<div class="grid">
<div class="card" style="grid-column:span 1">
<h2>Score Trends <span class="subtitle">last 40 evals</span></h2>
<div class="chart" id="chart"></div>
<div class="chart-legend">
<span><span class="swatch" style="background:linear-gradient(to top,#2040a0,#4070e0)"></span> ≥85 Production</span>
<span><span class="swatch" style="background:linear-gradient(to top,#605020,#a08030)"></span> 70-84</span>
<span><span class="swatch" style="background:linear-gradient(to top,#602020,#a04040)"></span> &lt;70</span>
</div>
</div>
<div class="card">
<h2>Leaderboard <span class="subtitle">top production agents</span></h2>
<div id="leaderboard"></div>
</div>
<div class="card">
<h2>System Health</h2>
<div id="health"></div>
</div>
</div>

<div class="grid-2">
<div class="card">
<h2>Recent Agents</h2>
<div style="max-height:350px;overflow-y:auto"><table class="agent-table"><thead><tr><th>Blueprint</th><th>Run</th><th>Score</th><th>Stage</th><th>Teacher</th></tr></thead><tbody id="agents"></tbody></table></div>
</div>
<div class="card">
<h2>Blueprints <span class="subtitle" id="bp-count"></span></h2>
<div class="bp-grid" id="blueprints"></div>
</div>
</div>

<div class="grid-2" style="margin-top:14px">
<div class="card">
<h2>Checkpoints</h2>
<div style="max-height:180px;overflow-y:auto" id="checkpoints"></div>
</div>
<div class="card">
<h2>Latest Agent Output</h2>
<div style="font:10px/1.4 'Consolas',monospace;color:#7080a0;max-height:180px;overflow-y:auto;white-space:pre-wrap;background:#060610;padding:10px;border-radius:4px" id="output-preview">Waiting for agent output...</div>
<div style="font-size:10px;color:var(--dim);margin-top:4px" id="output-meta"></div>
</div>
</div>

<div class="toast-container" id="toasts"></div>
<div class="footer">Styde Forge v3.0 · Pontus Styde · Built on Hermes Agent · <span id="cost"></span></div>

<script>
let prevProduction = 0;
let prevScore = 0;

const evtSource = new EventSource("/stream");
evtSource.onmessage = function(event) {
    const d = JSON.parse(event.data);
    document.getElementById("clock").textContent = d.ts;
    document.getElementById("hw").textContent = d.hardware;

    // Toast on new production agent
    if (d.production > prevProduction && prevProduction > 0) {
        const toast = document.createElement("div");
        toast.className = "toast";
        toast.textContent = "AGENT PROMOTED TO PRODUCTION";
        document.getElementById("toasts").appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }
    prevProduction = d.production;

    // KPIs
    const trendIcon = d.score_trend === "up" ? "▲" : (d.score_trend === "down" ? "▼" : "■");
    const trendCls = d.score_trend === "up" ? "score-up" : (d.score_trend === "down" ? "score-down" : "score-flat");
    document.getElementById("kpis").innerHTML =
        '<div class="kpi"><div class="num">'+d.spawned+'</div><div class="lbl">Agents Spawned</div></div>'+
        '<div class="kpi"><div class="num">'+d.evaluations+'</div><div class="lbl">Evaluations</div></div>'+
        '<div class="kpi kpi-blue"><div class="num">'+d.loops+'</div><div class="lbl">Loop Iterations</div></div>'+
        '<div class="kpi kpi-ok"><div class="num">'+d.production+'</div><div class="lbl">In Production</div></div>'+
        '<div class="kpi kpi-warn"><div class="num">'+d.refinery+'</div><div class="lbl">In Refinery</div></div>'+
        '<div class="kpi"><div class="num">'+d.score_avg+' <span style="font-size:14px" class="'+trendCls+'">'+trendIcon+'</span></div><div class="lbl">Avg Score</div></div>'+
        '<div class="kpi"><div class="num">'+d.blueprints.length+'</div><div class="lbl">Blueprints</div></div>';

    // Score chart
    const chart = document.getElementById("chart");
    let bars = "";
    const max = Math.max(...d.scores, 100);
    d.scores.forEach(s => {
        let cls = s >= 85 ? "bar-prod" : (s >= 70 ? "bar-mid" : "bar-low");
        bars += '<div class="bar '+cls+'" style="height:'+Math.max(s/max*90,3)+'px" title="'+s+'"></div>';
    });
    const lastScore = d.scores.length ? d.scores[d.scores.length-1] : 0;
    const scoreCls = lastScore >= 85 ? "score-up" : (lastScore >= 70 ? "score-flat" : "score-down");
    chart.innerHTML = bars + '<div class="score-overlay '+scoreCls+'">'+lastScore+'</div>';

    // Agents table
    let agentHtml = "";
    d.agents.forEach(a => {
        let badge = a.stage === "production" ? '<span class="badge badge-prod">PROD</span>' :
                    (a.stage === "archive" ? '<span class="badge badge-arch">ARCH</span>' :
                    '<span class="badge badge-ref">REF</span>');
        let sc = a.score !== null ? a.score : "—";
        let scCls = a.score >= 85 ? 'color:#30c050' : (a.score >= 70 ? 'color:#c0a030' : 'color:#e04040');
        agentHtml += '<tr><td>'+a.blueprint+'</td><td style="color:#404070">'+a.run_id+'</td>'+
            '<td class="score-cell" style="'+scCls+'">'+sc+'</td>'+
            '<td>'+badge+'</td><td style="color:#5050a0;font-size:10px">'+a.teacher+'</td></tr>';
    });
    document.getElementById("agents").innerHTML = agentHtml || '<tr><td colspan="5" style="color:#505070">No agents.</td></tr>';

    // Leaderboard
    let lbHtml = "";
    d.leaderboard.forEach((a, i) => {
        let rankCls = i === 0 ? "lb-rank-1" : (i === 1 ? "lb-rank-2" : (i === 2 ? "lb-rank-3" : "lb-rank-n"));
        let scCls = a.score >= 90 ? 'color:#40e040' : (a.score >= 85 ? 'color:#40c040' : 'color:#c0a030');
        lbHtml += '<div class="lb-row"><span><span class="lb-rank '+rankCls+'">'+(i+1)+'</span>'+a.blueprint+'</span><span style="font-weight:700;'+scCls+'">'+a.score+'</span></div>';
    });
    document.getElementById("leaderboard").innerHTML = lbHtml || '<span style="color:#505070">No production agents yet.</span>';

    // Health
    const h = d.health;
    document.getElementById("health").innerHTML =
        '<div style="margin-bottom:8px"><span style="color:#8080b0">CPU</span> <span style="float:right">'+h.cpu+'%</span><div style="background:#101028;border-radius:3px;height:4px;margin-top:2px"><div style="background:linear-gradient(to right,#3060c0,#40a0f0);height:4px;border-radius:3px;width:'+Math.min(h.cpu,100)+'%"></div></div></div>'+
        '<div style="margin-bottom:8px"><span style="color:#8080b0">RAM</span> <span style="float:right">'+h.ram_gb+' / '+h.ram_total+' GB</span><div style="background:#101028;border-radius:3px;height:4px;margin-top:2px"><div style="background:linear-gradient(to right,#8050c0,#c080f0);height:4px;border-radius:3px;width:'+h.ram_pct+'%"></div></div></div>'+
        '<div><span style="color:#8080b0">Disk</span> <span style="float:right">'+h.disk_free+' GB free</span><div style="background:#101028;border-radius:3px;height:4px;margin-top:2px"><div style="background:linear-gradient(to right,#c05030,#f08040);height:4px;border-radius:3px;width:'+h.disk_pct+'%"></div></div></div>';

    // Checkpoints
    let cpHtml = "";
    d.checkpoints.forEach(c => {
        cpHtml += '<div class="cp-item"><span>'+c.id+'</span><span style="color:#404080">'+c.created+'</span></div>';
    });
    document.getElementById("checkpoints").innerHTML = cpHtml || '<span style="color:#505070">No checkpoints.</span>';

    // Blueprints
    let bpHtml = "";
    d.blueprints.forEach(b => {
        bpHtml += '<div class="bp-chip"><span class="bp-name">'+b.name+'</span><span class="bp-ver">v'+b.version+'</span><span class="bp-domain">'+b.domain+'</span></div>';
    });
    document.getElementById("blueprints").innerHTML = bpHtml || '<span style="color:#505070">No blueprints.</span>';
    document.getElementById("bp-count").textContent = d.blueprints.length + " total";

    // Cost footer
    document.getElementById("cost").textContent = "Est. tokens: "+(d.cost.tokens/1000).toFixed(0)+"k · Cost: $"+d.cost.cost.toFixed(4);
};
</script>
</body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/stream":
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
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def log_message(self, format, *args): pass


def run_dashboard():
    threading.Thread(target=sse_broadcaster, daemon=True).start()
    server = HTTPServer(("localhost", PORT), DashboardHandler)
    print(f"Dashboard v3: http://localhost:{PORT}")
    print("SSE real-time · Animated · Leaderboard · Health · Cost tracking")
    try: server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()

if __name__ == "__main__":
    run_dashboard()
