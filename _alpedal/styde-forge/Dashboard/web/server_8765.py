"""
Forge Mission Control v6 - Production-Grade Dashboard Server
Port 8765. Serves HTML + JSON API with cached state, forge controls,
skill detail, activity feed, hardware telemetry, gzip compression,
and health endpoint.

Security: CSP, CORS (locked), CSRF tokens, security headers,
body size limiting, input validation. OWASP-aligned.
"""
import json, os, sys, time, subprocess, threading, gzip, io, hmac, hashlib, secrets, re
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

FORGE_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_FILE = FORGE_ROOT / "state.yaml"
DASHBOARD_HTML = Path(__file__).resolve().parent / "mission_control_8765.html"
REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"

# --- Security ---
MAX_BODY_BYTES = 65536  # 64 KB request body limit
CSRF_SECRET = secrets.token_hex(32)
ALLOWED_ORIGINS = frozenset(["http://localhost:8765", "http://127.0.0.1:8765"])
BLUEPRINT_RE = re.compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")
RUN_ID_RE = re.compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")

def csrf_token() -> str:
    """Generate a signed CSRF token valid for this session."""
    ts = str(int(time.time()))
    raw = ts + "." + secrets.token_hex(16)
    sig = hmac.new(CSRF_SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()[:16]
    return f"{raw}.{sig}"

def verify_csrf(token: str) -> bool:
    """Verify a signed CSRF token (30-minute expiry)."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return False
        ts_str, nonce, sig = parts[0], parts[1], parts[2]
        ts = int(ts_str)
        if time.time() - ts > 1800:  # 30 min expiry
            return False
        expected_sig = hmac.new(CSRF_SECRET.encode(), (ts_str + "." + nonce).encode(), hashlib.sha256).hexdigest()[:16]
        return hmac.compare_digest(sig, expected_sig)
    except (ValueError, IndexError):
        return False

def validate_blueprint(name: str) -> bool:
    """Block path traversal and command injection via blueprint names."""
    return bool(BLUEPRINT_RE.match(name))

def validate_run_id(rid: str) -> bool:
    """Block path traversal and command injection via run IDs."""
    return bool(RUN_ID_RE.match(rid))

def security_headers(handler, mime_type="text/html; charset=utf-8", add_csp=True):
    """Emit OWASP-aligned security headers."""
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.send_header("X-Frame-Options", "DENY")
    handler.send_header("X-XSS-Protection", "0")  # Deprecated; CSP handles it.
    handler.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
    handler.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    if add_csp:
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data: blob:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "object-src 'none'"
        )
        handler.send_header("Content-Security-Policy", csp)

try:
    import yaml
except ImportError:
    yaml = None

# --- State Cache ---
_state_cache = None
_state_cache_time = 0
CACHE_TTL = 5  # seconds

# --- Server Uptime ---
SERVER_START_TIME = time.time()

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
def _merge_state_activity():
    """Merge activity from state.yaml into in-memory ACTIVITY_LOG using composite key."""
    global _seq
    try:
        forge = load_state_cached()
        state_activity = forge.get("activity", [])
        if not isinstance(state_activity, list):
            return
        # Composite key: (action, blueprint, detail, timestamp) — avoids ID counter collision
        existing = {(e.get("action"), e.get("blueprint"), e.get("detail"), e.get("timestamp")) for e in ACTIVITY_LOG}
        with _lock:
            for entry in state_activity:
                key = (entry.get("action"), entry.get("blueprint"), entry.get("detail"), entry.get("timestamp"))
                if key not in existing:
                    ACTIVITY_LOG.insert(0, entry)
                    existing.add(key)
                    if len(ACTIVITY_LOG) > MAX_ACTIVITY:
                        ACTIVITY_LOG.pop()
                    if entry.get("id", 0) > _seq:
                        _seq = entry["id"]
    except Exception:
        pass


def _lock_is_alive() -> bool:
    """Check if .forge.lock exists with a live PID."""
    lockf = FORGE_ROOT / ".forge.lock"
    if not lockf.exists():
        return False
    try:
        import json as _j
        data = _j.loads(lockf.read_text())
        pid = int(data.get("pid", 0))
        if pid <= 0:
            return False
        import ctypes
        # PROCESS_QUERY_INFORMATION = 0x0400
        h = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)
        if not h:
            return False
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    except Exception:
        return False


def _get_active_batch() -> dict:
    """Get info about the currently running forge batch/lock."""
    lockf = FORGE_ROOT / ".forge.lock"
    if not lockf.exists():
        return {"running": False, "pid": None, "started": None}
    try:
        import json as _j
        data = _j.loads(lockf.read_text())
        pid = int(data.get("pid", 0))
        started = data.get("acquired", "")
        # Check if PID alive
        import ctypes
        h = ctypes.windll.kernel32.OpenProcess(0x0400, False, pid)
        alive = bool(h)
        if h:
            ctypes.windll.kernel32.CloseHandle(h)
        # Scan for newest run dirs
        from pathlib import Path as _P
        newest_run, newest_time = None, 0
        rdir = FORGE_ROOT / "StydeAgents" / "refinery"
        if rdir.exists():
            candidates = sorted(rdir.glob("*/runs/run-*"))
            if candidates:
                newest_run = str(candidates[-1].relative_to(FORGE_ROOT))
        return {"running": alive, "pid": pid, "started": started, "latest_run": newest_run}
    except Exception:
        return {"running": False, "pid": None, "started": None}


def compute_state():
    """Compute the full dashboard state. Catches all exceptions and returns
    partial data with an 'error' key instead of crashing the API."""
    try:
        _merge_state_activity()
    except Exception:
        pass

    try:
        forge = load_state_cached()
    except Exception as e:
        return {"error": f"Failed to load state: {e}", "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

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

    hw = {}
    try:
        hw = get_hardware()
    except Exception:
        pass
    skills = []
    try:
        skills = get_skills()
    except Exception:
        pass

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
            "is_working": any(p.get("status") == "running" for p in active) or _lock_is_alive(),
            "active_batch": _get_active_batch(),
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
        "activity": list(ACTIVITY_LOG[:50]),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "stats": _safe_compute_stats(forge, agents, bp_scores),
    }


def _safe_compute_stats(forge, agents, bp_scores):
    """Wrapper around _compute_stats that catches exceptions."""
    try:
        return _compute_stats(forge, agents, bp_scores)
    except Exception:
        return {}


def _compute_stats(forge, agents, bp_scores):
    """Compute aggregate stats for the dashboard header."""
    # Average score from blueprint_scores
    all_scores = []
    for bp, scores in bp_scores.items():
        if isinstance(scores, list):
            all_scores.extend(scores)
    avg_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else None

    # Score distribution buckets
    dist = {"0-20": 0, "20-40": 0, "40-60": 0, "60-80": 0, "80-100": 0}
    for s in all_scores:
        if s < 20: dist["0-20"] += 1
        elif s < 40: dist["20-40"] += 1
        elif s < 60: dist["40-60"] += 1
        elif s < 80: dist["60-80"] += 1
        else: dist["80-100"] += 1

    # Production rate
    total = len(agents)
    prod = sum(1 for a in agents if a.get("stage") == "production")
    arch = sum(1 for a in agents if a.get("stage") == "archive")

    # Top blueprints by score
    bp_avgs = {}
    for bp, scores in bp_scores.items():
        if isinstance(scores, list) and scores:
            bp_avgs[bp] = round(sum(scores) / len(scores), 1)
    top_bps = sorted(bp_avgs.items(), key=lambda x: -x[1])[:10]

    return {
        "avg_score": avg_score,
        "total_scored": len(all_scores),
        "distribution": dist,
        "production_rate": round(prod / total * 100, 1) if total else 0,
        "total_agents": total,
        "production_count": prod,
        "archive_count": arch,
        "top_blueprints": [{"name": k, "avg_score": v} for k, v in top_bps],
        "total_spawns": forge.get("total_agents_spawned", 0),
        "total_evals": forge.get("total_evaluations", 0),
        "loop_iterations": forge.get("loop_iterations", 0),
    }

# ─── Seed Activity ───
def seed_activity():
    _merge_state_activity()
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

    def _set_cors(self):
        """Set CORS header only if origin matches allowed list."""
        origin = self.headers.get("Origin", "")
        if origin in ALLOWED_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Credentials", "true")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-CSRF-Token")
            self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        """CORS preflight."""
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/api/state":
            self._json(compute_state())
        elif p == "/api/health":
            self._json({"status": "ok", "uptime": round(time.time() - SERVER_START_TIME, 1)})
        elif p == "/api/state.yaml":
            self._raw(STATE_FILE.read_bytes() if STATE_FILE.exists() else b"# missing", "text/yaml")
        elif p == "/api/skills":
            self._json({"skills": get_skills()})
        elif p == "/api/activity":
            self._json({"activity": list(ACTIVITY_LOG[:50])})
        elif p == "/api/csrf-token":
            self._json({"csrf_token": csrf_token()})
        elif p == "/" or p == "/index.html":
            if DASHBOARD_HTML.exists():
                self._raw(DASHBOARD_HTML.read_bytes(), "text/html; charset=utf-8")
            else:
                self._raw(b"<h1>Dashboard not found</h1>", "text/html")
        else:
            self._json({"error": "not found"}, 404)

    def do_POST(self):
        p = urlparse(self.path).path

        # CSRF check on all POST endpoints except health/ping
        token = self.headers.get("X-CSRF-Token", "")
        if not verify_csrf(token):
            self._json({"error": "invalid or missing CSRF token"}, 403)
            return

        # Body size limit
        raw_cl = self.headers.get("Content-Length", "0")
        try:
            cl = int(raw_cl)
        except ValueError:
            self._json({"error": "invalid Content-Length"}, 400)
            return
        if cl > MAX_BODY_BYTES:
            self._json({"error": "request body too large"}, 413)
            return
        body = self.rfile.read(cl).decode("utf-8", errors="replace") if cl else "{}"
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json({"error": "invalid JSON body"}, 400)
            return

        fp = FORGE_ROOT / "Core" / "forge.py"

        if p == "/api/spawn":
            bp = data.get("blueprint", "")
            if not bp or not validate_blueprint(bp):
                self._json({"error": "invalid blueprint name"}, 400)
                return
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
            if not bp or not validate_blueprint(bp) or not validate_run_id(rid):
                self._json({"error": "invalid blueprint or run_id"}, 400)
                return
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
            if not bp or not rid or not validate_blueprint(bp) or not validate_run_id(rid):
                self._json({"error": "invalid blueprint or run_id"}, 400)
                return
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
        self._set_cors()
        security_headers(self, "application/json", add_csp=False)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2, default=str).encode())

    def _raw(self, data, ct):
        self.send_response(200)
        self.send_header("Content-Type", ct)
        self._set_cors()
        is_html = "html" in ct
        security_headers(self, ct, add_csp=is_html)
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        # Gzip support for HTML
        accept = self.headers.get("Accept-Encoding", "")
        if "gzip" in accept and isinstance(data, bytes) and len(data) > 256:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
                gz.write(data)
            data = buf.getvalue()
            self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(data)))
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
