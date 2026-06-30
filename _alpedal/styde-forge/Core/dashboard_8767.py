"""
Styde Forge Statistics Dashboard — Port 8767.

Lightweight, temporary dashboard showing forge improvement metrics.
Uses ThreadingHTTPServer for Windows reliability. Metrics collected
asynchronously in background.

Start: python Core/dashboard_8767.py
Stop:  Ctrl+C or kill process
"""
import sys
import json
import time
import threading
import os
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

# Ensure forge root is on path
FORGE_ROOT = Path(__file__).resolve().parent.parent
if str(FORGE_ROOT) not in sys.path:
    sys.path.insert(0, str(FORGE_ROOT))

PORT = 8767
_start_time = time.time()

# Simple in-memory cache populated by background thread
_metrics_cache = {"status": "collecting", "data": None}
_cache_lock = threading.Lock()


def _fast_collect_metrics() -> dict:
    """Fast metrics collection — uses scandir for speed."""
    refinery_dir = FORGE_ROOT / "StydeAgents" / "refinery"
    production_dir = FORGE_ROOT / "StydeAgents" / "production"
    archive_dir = FORGE_ROOT / "StydeAgents" / "archive"
    blueprints_dir = FORGE_ROOT / "StydeAgents" / "blueprints"

    refinery = production = archive = blueprints = 0
    prod_bps = set()
    arch_bps = set()

    # Fast scandir
    for zone_dir in [refinery_dir, production_dir, archive_dir]:
        if not zone_dir.exists():
            continue
        try:
            for entry in os.scandir(zone_dir):
                if not entry.is_dir() or entry.name.startswith("_"):
                    continue
                runs = entry.path + "/runs"
                if os.path.isdir(runs):
                    try:
                        count = sum(1 for r in os.scandir(runs) if r.name.startswith("run-"))
                    except Exception:
                        count = 0
                    if zone_dir == refinery_dir:
                        refinery += count
                    elif zone_dir == production_dir:
                        production += count
                        if count > 0:
                            prod_bps.add(entry.name)
                    else:
                        archive += count
                        if count > 0:
                            arch_bps.add(entry.name)
        except Exception:
            pass

    if blueprints_dir.exists():
        try:
            blueprints = sum(1 for e in os.scandir(blueprints_dir) if e.is_dir() and not e.name.startswith("_"))
        except Exception:
            pass

    # Get forge state for loop/version
    loop_iter = total_spawned = 0
    caveman = True
    try:
        import yaml
        sf = FORGE_ROOT / "state.yaml"
        if sf.exists():
            s = yaml.safe_load(sf.read_text(encoding="utf-8"))
            loop_iter = s.get("loop_iterations", 0)
            total_spawned = s.get("total_agents_spawned", 0)
            caveman = s.get("caveman_ultra", True)
    except Exception:
        pass

    # Lock status
    lock_active = (FORGE_ROOT / ".forge.lock").exists()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "forge": {
            "version": "3.1.0",
            "caveman_ultra": caveman,
            "lock_active": lock_active,
            "loop_iterations": loop_iter,
            "total_agents_spawned": total_spawned,
        },
        "counts": {
            "total": refinery + production + archive,
            "refinery": refinery,
            "production": production,
            "archive": archive,
            "blueprints": blueprints,
            "blueprints_production": len(prod_bps),
            "blueprints_archived": len(arch_bps),
        },
        "activity": {"note": "Fast mode — score distribution not scanned"},
    }


def _background_collector():
    """Background thread: periodically update metrics cache."""
    while True:
        try:
            data = _fast_collect_metrics()
            with _cache_lock:
                _metrics_cache["status"] = "ok"
                _metrics_cache["data"] = data
                _metrics_cache["updated"] = datetime.now(timezone.utc).isoformat()
        except Exception as e:
            with _cache_lock:
                _metrics_cache["status"] = "error"
                _metrics_cache["error"] = str(e)
        time.sleep(15)  # Update every 15 seconds


# Start background collector immediately
_collector_thread = threading.Thread(target=_background_collector, daemon=True)
_collector_thread.start()


def collect_dashboard_data() -> dict:
    """Collect dashboard data from cache + live hook/health info."""
    with _cache_lock:
        cached = dict(_metrics_cache)

    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": time.time() - _start_time,
        "metrics": cached.get("data") or {"status": cached.get("status", "unknown")},
    }

    # Hook stats (lightweight)
    try:
        from Core.hooks import get_hooks
        data["hooks"] = get_hooks().summary()
    except Exception:
        data["hooks"] = {"total_hooks": 0}

    # Health (lightweight)
    try:
        from Core.auto_heal import get_healer
        healer = get_healer()
        data["health"] = {
            "last_check": datetime.fromtimestamp(healer.last_check, tz=timezone.utc).isoformat()
                         if healer.last_check else None,
            "heals_applied": len(healer.heals_applied),
        }
    except Exception:
        data["health"] = {"heals_applied": 0}

    # Pattern library stats
    try:
        from Core.pattern_library import get_library
        data["patterns"] = get_library().stats()
    except Exception:
        data["patterns"] = {"total_patterns": 0}

    # Circuit breakers
    try:
        from Core.circuit_breaker import all_breakers
        breakers = all_breakers()
        open_breakers = {k: v for k, v in breakers.items() if v.get("state") != "closed"}
        data["breakers"] = {"total": len(breakers), "open": len(open_breakers)}
    except Exception:
        data["breakers"] = {"total": 0, "open": 0}

    return data


class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for statistics dashboard."""

    def log_message(self, format, *args):
        pass

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, default=str, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status: int = 200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]

        if path == "/":
            self._send_html(DASHBOARD_HTML)
        elif path == "/api/stats":
            self._send_json(collect_dashboard_data())
        elif path == "/api/metrics":
            with _cache_lock:
                self._send_json(_metrics_cache.get("data") or {"status": _metrics_cache.get("status", "unknown")})
        elif path == "/api/health":
            try:
                from Core.auto_heal import run_health_check
                self._send_json(run_health_check(auto_fix=False))
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        elif path == "/api/hooks":
            try:
                from Core.hooks import get_hooks
                self._send_json(get_hooks().summary())
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        elif path == "/api/patterns":
            try:
                from Core.pattern_library import get_library
                self._send_json(get_library().stats())
            except Exception as e:
                self._send_json({"error": str(e)}, 500)
        else:
            self._send_json({"error": "Not found", "path": path}, 404)


# ═══════════════════════════════════════════════════
# Dashboard HTML
# ═══════════════════════════════════════════════════

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Forge — Stats Dashboard :8767</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Consolas', 'Monaco', monospace; background: #0a0a0f; color: #c0c0d0;
       padding: 20px; min-height: 100vh; }
h1 { color: #ff6b35; font-size: 22px; margin-bottom: 5px; }
.subtitle { color: #666; font-size: 12px; margin-bottom: 20px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
.card { background: #111118; border: 1px solid #2a2a35; border-radius: 6px; padding: 12px; }
.card .label { color: #777; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; }
.card .value { font-size: 26px; font-weight: bold; margin: 3px 0; }
.card .detail { font-size: 10px; color: #555; }
.green { color: #4caf50; } .orange { color: #ff8c5a; } .red { color: #f44336; }
.blue { color: #42a5f5; } .purple { color: #ab47bc; }
h2 { color: #ff8c5a; font-size: 15px; margin: 18px 0 8px 0; border-bottom: 1px solid #2a2a35; padding-bottom: 4px; }
table { width: 100%; border-collapse: collapse; font-size: 12px; margin-top: 6px; }
th { text-align: left; color: #777; padding: 5px 8px; border-bottom: 1px solid #2a2a35; }
td { padding: 4px 8px; border-bottom: 1px solid #1a1a25; }
tr:hover { background: #151520; }
.error { color: #f44336; font-size: 12px; padding: 8px; background: #1a1010; border-radius: 4px; }
.refresh { color: #42a5f5; cursor: pointer; font-size: 11px; }
.version-tag { font-size: 10px; color: #555; }
</style>
</head>
<body>
<h1>Styde Forge <span class="version-tag">v3.1</span></h1>
<div class="subtitle">
  Port 8767 | Stats Dashboard |
  <span class="refresh" onclick="fetchData()">Refresh</span>
  <span style="float:right;font-size:11px;color:#555;" id="uptime"></span>
</div>
<div id="error" class="error" style="display:none;"></div>
<div class="grid" id="counts"></div>

<h2>Forge State</h2>
<div class="grid" id="forgeState"></div>

<h2>Hooks & Health</h2>
<div class="grid" id="hooksHealth"></div>

<h2>Pattern Library</h2>
<div id="patterns"></div>

<h2>Circuit Breakers</h2>
<div id="breakers"></div>

<h2>Improvements Active</h2>
<div class="card" style="margin-top:10px;">
  <table>
    <tr><th>Module</th><th>Status</th><th>Description</th></tr>
    <tr><td>Core/hooks.py</td><td class="green">LIVE</td><td>Lifecycle event hooks (on_spawn, on_eval, on_promote, on_archive, ...)</td></tr>
    <tr><td>Core/auto_heal.py</td><td class="green">LIVE</td><td>Auto-healing: stale lock, corrupt cache, 0-byte forge, disk check</td></tr>
    <tr><td>Core/pattern_library.py</td><td class="green">LIVE</td><td>Reusable success patterns from production agents</td></tr>
    <tr><td>Core/metrics.py</td><td class="green">LIVE</td><td>Filesystem-based metrics collector</td></tr>
    <tr><td>Core/dashboard_8767.py</td><td class="green">LIVE</td><td>This dashboard — port 8767</td></tr>
    <tr><td>Core/forge.py (hooks)</td><td class="green">INTEGRATED</td><td>Hooks fired at spawn, eval, improve, promote, archive stages</td></tr>
    <tr><td>Core/forge.py (auto-heal)</td><td class="green">INTEGRATED</td><td>Health check runs before every loop start</td></tr>
    <tr><td>Core/forge.py (patterns)</td><td class="green">INTEGRATED</td><td>Patterns extracted on agent promotion</td></tr>
  </table>
</div>

<script>
async function fetchData() {
  try {
    const r = await fetch('/api/stats');
    const d = await r.json();
    document.getElementById('error').style.display = 'none';
    render(d);
  } catch(e) {
    document.getElementById('error').style.display = 'block';
    document.getElementById('error').textContent = 'API: ' + e.message;
  }
}

function render(d) {
  const m = d.metrics || {};
  const c = m.counts || {};
  const f = m.forge || {};

  document.getElementById('uptime').textContent =
    'uptime: ' + Math.floor((d.uptime_seconds||0)/60) + 'm ' + Math.floor((d.uptime_seconds||0)%60) + 's';

  document.getElementById('counts').innerHTML = `
    <div class="card"><div class="label">Total Agents</div><div class="value purple">${c.total||0}</div><div class="detail">All stages</div></div>
    <div class="card"><div class="label">Production</div><div class="value green">${c.production||0}</div><div class="detail">${c.blueprints_production||0} blueprints</div></div>
    <div class="card"><div class="label">Refinery</div><div class="value orange">${c.refinery||0}</div><div class="detail">In training</div></div>
    <div class="card"><div class="label">Archive</div><div class="value red">${c.archive||0}</div><div class="detail">${c.blueprints_archived||0} blueprints</div></div>
    <div class="card"><div class="label">Blueprints</div><div class="value blue">${c.blueprints||0}</div><div class="detail">Total defined</div></div>
  `;

  document.getElementById('forgeState').innerHTML = `
    <div class="card"><div class="label">Caveman Ultra</div><div class="value ${f.caveman_ultra?'green':'red'}">${f.caveman_ultra?'ON':'OFF'}</div></div>
    <div class="card"><div class="label">Lock Active</div><div class="value ${f.lock_active?'orange':'green'}">${f.lock_active?'YES':'NO'}</div></div>
    <div class="card"><div class="label">Loop Iterations</div><div class="value blue">${f.loop_iterations||0}</div></div>
    <div class="card"><div class="label">Total Spawned</div><div class="value purple">${f.total_agents_spawned||0}</div></div>
  `;

  const hh = d.hooks || {};
  const he = d.health || {};
  document.getElementById('hooksHealth').innerHTML = `
    <div class="card"><div class="label">Registered Hooks</div><div class="value blue">${hh.total_hooks||0}</div><div class="detail">${Object.keys(hh.events||{}).length||0} event types</div></div>
    <div class="card"><div class="label">Health Checks</div><div class="value ${he.last_check?'green':'orange'}">${he.last_check?'Active':'Pending'}</div><div class="detail">${he.heals_applied||0} heals applied</div></div>
    <div class="card"><div class="label">Breakers Open</div><div class="value ${(d.breakers||{}).open?'red':'green'}">${(d.breakers||{}).open||0}</div></div>
  `;

  const p = d.patterns || {};
  document.getElementById('patterns').innerHTML = `
    <div class="card"><div class="label">Pattern Library</div>
    <div>Total patterns: <strong class="purple">${p.total_patterns||0}</strong></div>
    <div>Total reuse: ${p.total_reuse||0}</div>
    ${p.top_pattern ? '<div>Top: <strong>'+p.top_pattern.name+'</strong> ('+p.top_pattern.score+')</div>' : ''}
    </div>
  `;

  document.getElementById('breakers').innerHTML = `
    <div class="card"><div class="label">Circuit Breakers</div>
    <div>Total: ${(d.breakers||{}).total||0} | Open: <strong class="${(d.breakers||{}).open?'red':'green'}">${(d.breakers||{}).open||0}</strong></div></div>
  `;
}

fetchData();
setInterval(fetchData, 10000);
</script>
</body>
</html>"""


def main():
    """Start the dashboard server."""
    server = ThreadingHTTPServer(("0.0.0.0", PORT), DashboardHandler)
    server.allow_reuse_address = True

    print(f"=== Styde Forge Statistics Dashboard ===")
    print(f"Port: {PORT}")
    print(f"URL:  http://localhost:{PORT}")
    print(f"API:  http://localhost:{PORT}/api/stats")
    print(f"Metrics collection: background (every 15s)")
    print(f"Press Ctrl+C to stop.")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
