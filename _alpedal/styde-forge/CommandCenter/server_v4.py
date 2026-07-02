"""
Forge Command Center v4 — Serverar Nexus Forge (mockup 22)
Port 8766. Clean server: serves index.html + /api/state + /api/stream
"""
import sys, os, json, yaml, time, threading, gzip, io
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

FORGE_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = FORGE_ROOT / "state.yaml"
REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"
PRODUCTION_DIR = FORGE_ROOT / "StydeAgents" / "production"
ARCHIVE_DIR = FORGE_ROOT / "StydeAgents" / "archive"
HTML_FILE = Path(__file__).resolve().parent / "index.html"
PORT = 8766
SERVER_START = time.time()

_compute_lock = threading.Lock()
_cached_result = None
_last_scan = 0
CACHE_TTL = 15

# Load HTML
def load_html():
    hp = Path(__file__).resolve().parent / "index.html"
    with open(hp, encoding='utf-8') as f:
        return f.read()

INDEX_HTML = None  # loaded on first request

def _scandir_count(path):
    if not os.path.isdir(path): return 0
    return sum(1 for e in os.scandir(path) if e.is_dir() and not e.name.startswith("_"))

def get_state():
    global _cached_result, _last_scan
    now = time.time()
    if _cached_result and (now - _last_scan) < CACHE_TTL:
        return _cached_result
    with _compute_lock:
        if _cached_result and (time.time() - _last_scan) < CACHE_TTL:
            return _cached_result
        state = {}
        try:
            if STATE_FILE.exists():
                state = yaml.safe_load(STATE_FILE.read_text(encoding="utf-8")) or {}
        except Exception: state = {}
        agents = state.get("agents",[]) or []
        evals = state.get("evaluations",[]) or []
        activity = state.get("activity",[]) or []
        forge_info = {
            "codename": state.get("forge_codename","The Crucible"),
            "version": state.get("forge_version","3.0"),
            "loop_iterations": state.get("loop_iterations",0),
            "total_agents": state.get("total_agents",len(agents)),
            "total_evaluations": state.get("total_evaluations",len(evals)),
            "caveman_ultra": state.get("caveman_ultra",True),
            "last_checkpoint": str(state.get("last_checkpoint","N/A"))[:30],
        }
        rn = _scandir_count(str(REFINERY_DIR))
        pn = _scandir_count(str(PRODUCTION_DIR))
        an = _scandir_count(str(ARCHIVE_DIR))
        recent = []
        for a in activity[:50]:
            recent.append({
                "action": a.get("action","?"),"blueprint": a.get("blueprint","?"),
                "detail": str(a.get("detail",""))[:100],"progress": a.get("progress",0),
                "status": a.get("status","?"),"timestamp": str(a.get("timestamp","")),
            })
        active = [r for r in recent if r["status"]=="running"][:20]
        bp_scores = {}
        for a in agents:
            bp = a.get("blueprint",""); sc = a.get("composite_score")
            stage = a.get("stage","refinery")
            if bp:
                e = bp_scores.setdefault(bp,{"best":0,"latest":0,"stage":stage,"count":0,"history":[]})
                if sc is not None: e["best"] = max(e["best"],sc); e["latest"] = sc
                e["count"] += 1
        for ev in evals:
            bp = ev.get("blueprint",""); sc = ev.get("composite_score")
            if bp and sc is not None:
                e = bp_scores.setdefault(bp,{"best":0,"latest":0,"stage":"refinery","count":0,"history":[]})
                e["best"] = max(e["best"],sc); e["latest"] = max(e["latest"],sc)
        prod_bps = set()
        if os.path.isdir(str(PRODUCTION_DIR)):
            for bp_entry in os.scandir(str(PRODUCTION_DIR)):
                if bp_entry.is_dir() and not bp_entry.name.startswith("_"):
                    prod_bps.add(bp_entry.name)
                    if bp_entry.name in bp_scores: bp_scores[bp_entry.name]["stage"] = "production"
                    else: bp_scores[bp_entry.name] = {"best":0,"latest":0,"stage":"production","count":0,"history":[]}
        lock = None
        lf = str(FORGE_ROOT / ".forge.lock")
        if os.path.isfile(lf):
            try:
                with open(lf) as f: lock = json.load(f)
            except Exception: lock = {"pid":"?","acquired":"?"}
        dt_now = datetime.now(timezone.utc); hour = dt_now.hour
        peak_active = (1 <= hour < 4) or (6 <= hour < 10)
        peak_msg = f"~{(4-hour)}h" if 1<=hour<4 else f"~{(10-hour)}h" if 6<=hour<10 else ""
        result = {
            "forge": forge_info,
            "pipeline": {"refinery":rn,"production":pn,"archive":an},
            "active_processes": active, "activity": recent,
            "bp_scores": dict(sorted(bp_scores.items(), key=lambda x: -x[1].get("best",0))),
            "forge_lock": lock,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "uptime": int(time.time()-SERVER_START),
            "peak_hours": {"active":peak_active,"current_utc":f"{hour:02d}:00 UTC","ends":peak_msg,"slots":"01:00\u201304:00 / 06:00\u201310:00 UTC"},
        }
        _cached_result = result; _last_scan = time.time()
        return result

class Handler(BaseHTTPRequestHandler):
    def _send(self, body, ct, code=200, cache="no-cache", extra=None):
        accept = self.headers.get("Accept-Encoding","")
        if "gzip" in accept and len(body) > 1024:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf,mode="wb",compresslevel=5) as gz: gz.write(body if isinstance(body,bytes) else body.encode())
            body = buf.getvalue(); enc = "gzip"
        else: enc = None
        self.send_response(code)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", cache)
        self.send_header("X-Content-Type-Options","nosniff")
        if enc: self.send_header("Content-Encoding",enc); self.send_header("Vary","Accept-Encoding")
        if extra:
            for k,v in extra.items(): self.send_header(k,v)
        self.end_headers()
        try: self.wfile.write(body)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError): pass
    
    def handle(self):
        try: super().handle()
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError): pass
    
    def do_GET(self):
        global INDEX_HTML
        if self.path in ("/","/index.html"):
            if INDEX_HTML is None:
                INDEX_HTML = load_html()
            self._send(INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path == "/api/state":
            data = get_state()
            self._send(json.dumps(data,default=str).encode("utf-8"), "application/json", extra={"Access-Control-Allow-Origin":"*"})
        elif self.path == "/api/stream":
            self.send_response(200)
            self.send_header("Content-Type","text/event-stream")
            self.send_header("Cache-Control","no-cache")
            self.send_header("Access-Control-Allow-Origin","*")
            self.send_header("X-Accel-Buffering","no")
            self.end_headers()
            try:
                while True:
                    data = get_state()
                    payload = f"data: {json.dumps(data,default=str)}\n\n"
                    self.wfile.write(payload.encode("utf-8"))
                    self.wfile.flush()
                    time.sleep(3)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError): pass
        else:
            self._send(b"Not found", "text/plain", code=404)
    
    def log_message(self, *a): pass

def main():
    print("Pre-warming cache...", flush=True)
    t0 = time.time(); get_state()
    print(f"Cache warm: {time.time()-t0:.1f}s", flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.allow_reuse_address = True
    print(f"\u26a1 Nexus Forge v4 \u2192 http://localhost:{PORT}")
    print(f"   Monitor | Analytics | Insights")
    print(f"   Ctrl+C to stop")
    try: server.serve_forever()
    except KeyboardInterrupt: print("\nShutdown."); server.server_close()

if __name__ == "__main__": main()
