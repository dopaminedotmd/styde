"""
Fast Command Center — port 8766.
Uses cached metrics + state.yaml scan only. No eval.yaml scanning.
Starts instantly even with 2700+ agents.
"""
import sys, json, time, threading
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

FORGE_ROOT = Path(r"E:\Stryde\_alpedal\styde-forge")
if str(FORGE_ROOT) not in sys.path:
    sys.path.insert(0, str(FORGE_ROOT))

PORT = 8766
_start = time.time()
_cache = {"data": None, "time": 0}
_lock = threading.Lock()


def get_state():
    now = time.time()
    with _lock:
        if _cache["data"] and (now - _cache["time"]) < 5:
            return _cache["data"]

    import yaml, os
    state = {"tiers": [], "totals": {}, "activity": [], "uptime": now - _start}

    # Fast counts
    refinery = production = archive = 0
    prod_bps = set()
    for zone, key in [("refinery", "refinery"), ("production", "production"), ("archive", "archive")]:
        zd = FORGE_ROOT / "StydeAgents" / zone
        if zd.exists():
            for bp in os.scandir(zd):
                if bp.is_dir():
                    runs = bp.path + "/runs"
                    if os.path.isdir(runs):
                        cnt = sum(1 for r in os.scandir(runs) if r.name.startswith("run-"))
                        if key == "refinery": refinery += cnt
                        elif key == "production": production += cnt; prod_bps.add(bp.name)
                        else: archive += cnt

    state["totals"] = {"refinery": refinery, "production": production, "archive": archive,
                        "total": refinery + production + archive}

    # Blueprint tier from state.yaml
    bp_dir = FORGE_ROOT / "StydeAgents" / "blueprints"
    bp_count = sum(1 for _ in os.scandir(str(bp_dir))) if bp_dir.exists() else 0

    tiers = []
    grouped = {}
    # Read state for scores
    try:
        sf = FORGE_ROOT / "state.yaml"
        if sf.exists():
            s = yaml.safe_load(sf.read_text(encoding="utf-8"))
            for a in s.get("agents", []):
                bp = a.get("blueprint", "")
                if bp not in grouped:
                    grouped[bp] = {"blueprint": bp, "stage": a.get("stage", "?"),
                                   "agents": 0, "scores": []}
                grouped[bp]["agents"] += 1

            for e in s.get("evaluations", []):
                bp = e.get("blueprint", "")
                sc = e.get("composite_score")
                if bp in grouped and sc is not None:
                    grouped[bp]["scores"].append(sc)
    except: pass

    for bp, info in sorted(grouped.items()):
        scores = info["scores"]
        avg = round(sum(scores) / len(scores), 1) if scores else 0
        tier = "S" if avg >= 90 else "A" if avg >= 85 else "B" if avg >= 80 else "C" if avg >= 70 else "D" if avg >= 50 else "F"
        tiers.append({"blueprint": bp, "tier": tier, "avg_score": avg,
                       "agents": info["agents"], "stage": info["stage"],
                       "production": bp in prod_bps})

    state["tiers"] = sorted(tiers, key=lambda x: x["avg_score"], reverse=True)
    state["blueprint_count"] = bp_count

    # Recent activity from state
    try:
        sf = FORGE_ROOT / "state.yaml"
        if sf.exists():
            s = yaml.safe_load(sf.read_text(encoding="utf-8"))
            state["activity"] = s.get("activity", [])[:10]
            state["loop_iterations"] = s.get("loop_iterations", 0)
            state["caveman_ultra"] = s.get("caveman_ultra", True)
            state["forge_lock"] = (FORGE_ROOT / ".forge.lock").exists()
    except: pass

    with _lock:
        _cache["data"] = state
        _cache["time"] = now
    return state


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def _json(self, data, code=200):
        body = json.dumps(data, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, html, code=200):
        body = html.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self._html(HTML)
        elif self.path == "/api/state":
            self._json(get_state())
        else:
            self._json({"error": "not found"}, 404)


HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Command Center :8766</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Consolas,monospace;background:#0a0a0f;color:#c0c0d0;padding:16px}
h1{color:#ff6b35;font-size:20px;margin-bottom:4px}
.sub{color:#666;font-size:11px;margin-bottom:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px}
.card{background:#111118;border:1px solid#2a2a35;border-radius:4px;padding:10px}
.card .l{color:#777;font-size:10px;text-transform:uppercase}
.card .v{font-size:24px;font-weight:bold}
.g{color:#4caf50}.o{color:#ff8c5a}.r{color:#f44336}.b{color:#42a5f5}.p{color:#ab47bc}
table{width:100%;border-collapse:collapse;font-size:12px;margin-top:12px}
th{text-align:left;color:#777;padding:5px 8px;border-bottom:1px solid#2a2a35}
td{padding:4px 8px;border-bottom:1px solid#1a1a25}
tr:hover{background:#151520}
.tier-S{color:#ffd700}.tier-A{color:#4caf50}.tier-B{color:#42a5f5}
.tier-C{color:#ff8c5a}.tier-D{color:#f44336}.tier-F{color:#666}
</style></head><body>
<h1>Forge Command Center</h1>
<div class="sub">Port 8766 | <span id="up"></span> | <span onclick="load()" style="color:#42a5f5;cursor:pointer">Refresh</span></div>
<div class="grid" id="cards"></div>
<h2 style="color:#ff8c5a;font-size:14px;margin:16px 0 8px">Blueprint Tiers</h2>
<table><thead><tr><th>Tier</th><th>Blueprint</th><th>Score</th><th>Agents</th><th>Prod</th></tr></thead><tbody id="tiers"></tbody></table>
<script>
async function load(){
 try{
  const r=await fetch('/api/state');const d=await r.json();
  const t=d.totals||{};
  document.getElementById('cards').innerHTML=
   `<div class="card"><div class="l">Total</div><div class="v p">${t.total||0}</div></div>
    <div class="card"><div class="l">Production</div><div class="v g">${t.production||0}</div></div>
    <div class="card"><div class="l">Refinery</div><div class="v o">${t.refinery||0}</div></div>
    <div class="card"><div class="l">Archive</div><div class="v r">${t.archive||0}</div></div>
    <div class="card"><div class="l">Blueprints</div><div class="v b">${d.blueprint_count||0}</div></div>
    <div class="card"><div class="l">Lock</div><div class="v ${d.forge_lock?'o':'g'}">${d.forge_lock?'ON':'OFF'}</div></div>`;
  document.getElementById('up').textContent='uptime: '+Math.floor(d.uptime/60)+'m';
  let rows='',shown=0;
  for(const bp of(d.tiers||[])){
   if(shown++>50)break;
   rows+=`<tr><td class="tier-${bp.tier}">${bp.tier}</td><td>${bp.blueprint}</td>
     <td class="${bp.avg_score>=85?'g':bp.avg_score>=70?'o':'r'}">${bp.avg_score}</td>
     <td>${bp.agents}</td><td>${bp.production?'⭐':''}</td></tr>`;
  }
  document.getElementById('tiers').innerHTML=rows||'<tr><td colspan="5">No data</td></tr>';
 }catch(e){document.getElementById('cards').innerHTML='<div class="card"><div class="v r">'+e.message+'</div></div>'}
}
load();setInterval(load,10000);
</script></body></html>"""


def main():
    import os
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.allow_reuse_address = True
    print(f"Command Center :{PORT} — http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main()
