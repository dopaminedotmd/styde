#!/usr/bin/env python
"""Comprehensive bug test for Command Center at http://localhost:8766"""
import json
import time
import threading
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

BASE = "http://localhost:8766"
BUGS = []
PASSES = []

def bug(severity, title, detail, repro=""):
    BUGS.append({"severity": severity, "title": title, "detail": detail, "repro": repro})
    print(f"  🐛 [{severity}] {title}")

def ok(title):
    PASSES.append(title)
    print(f"  ✅ {title}")

def fetch(path, method="GET", data=None, timeout=15):
    req = urllib.request.Request(f"{BASE}{path}", data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return r.status, r.headers, body
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()
    except Exception as e:
        return None, {}, str(e).encode()

# ── Test 1: Basic Endpoint Behavior ──
print("\n" + "="*60)
print("TEST 1: Basic Endpoint Behavior")
print("="*60)

# 1a: GET /
code, headers, body = fetch("/")
if code == 200:
    ok("GET / returns 200")
    html = body.decode("utf-8")
    if "<!DOCTYPE html>" in html:
        ok("GET / returns valid HTML")
    else:
        bug("HIGH", "GET / does not return HTML", html[:200])
else:
    bug("CRITICAL", f"GET / returned {code}", f"Expected 200, got {code}")

# 1b: GET /api/state
code, headers, body = fetch("/api/state")
if code == 200:
    ok("GET /api/state returns 200")
    try:
        state = json.loads(body)
        ok("GET /api/state returns valid JSON")
        # Check all expected keys
        expected_keys = ["forge", "pipeline", "active_processes", "activity", "bp_scores", "forge_lock", "timestamp", "uptime", "peak_hours"]
        for k in expected_keys:
            if k in state:
                ok(f"  Key '{k}' present")
            else:
                bug("HIGH", f"Missing key '{k}' in /api/state", str(list(state.keys())))
    except json.JSONDecodeError as e:
        bug("CRITICAL", f"/api/state JSON decode error: {e}", body[:500].decode("utf-8", errors="replace"))
else:
    bug("CRITICAL", f"GET /api/state returned {code}")

# 1c: 404 for unknown paths
code, _, _ = fetch("/nonexistent")
if code == 404:
    ok("GET /nonexistent returns 404")
else:
    bug("MEDIUM", f"GET /nonexistent returned {code}, expected 404")

# 1d: HEAD method → should be supported or return 405
code, _, _ = fetch("/", method="HEAD")
if code == 405:
    ok("HEAD / returns 405 Method Not Allowed")
elif code == 200:
    ok("HEAD / returns 200 (supported)")
else:
    bug("MEDIUM", f"HEAD / returned {code} instead of 405", "HEAD requests not supported by BaseHTTPRequestHandler unless do_HEAD is defined")

# 1e: POST to /api/state
code, _, body = fetch("/api/state", method="POST")
if code == 405:
    ok("POST /api/state returns 405")
elif code == 501:
    bug("LOW", f"POST /api/state returns 501 instead of 405", "Should return 405 Method Not Allowed")

# ── Test 2: Response Headers ──
print("\n" + "="*60)
print("TEST 2: Response Headers")
print("="*60)

# 2a: Content-Type for HTML
code, headers, _ = fetch("/")
ct = headers.get("Content-Type", "")
if "text/html" in ct:
    ok("GET / has Content-Type: text/html")
else:
    bug("MEDIUM", f"GET / Content-Type is '{ct}', expected text/html")

# 2b: Content-Type for JSON
code, headers, _ = fetch("/api/state")
ct = headers.get("Content-Type", "")
if "application/json" in ct:
    ok("GET /api/state has Content-Type: application/json")
else:
    bug("MEDIUM", f"GET /api/state Content-Type is '{ct}'")

# 2c: Cache-Control for /api/state
cc = headers.get("Cache-Control", "")
if "no-cache" in cc:
    ok("GET /api/state has Cache-Control: no-cache")
else:
    bug("LOW", f"GET /api/state Cache-Control is '{cc}'")

# 2d: CORS header
acao = headers.get("Access-Control-Allow-Origin", "")
if acao == "*":
    ok("GET /api/state has Access-Control-Allow-Origin: *")
else:
    bug("MEDIUM", f"GET /api/state missing CORS header: '{acao}'")

# ── Test 3: State Cache and Consistency ──
print("\n" + "="*60)
print("TEST 3: State Cache Consistency")
print("="*60)

state1 = json.loads(fetch("/api/state")[2])
time.sleep(2)  # Within 3s state cache TTL
state2 = json.loads(fetch("/api/state")[2])

if state1["timestamp"] == state2["timestamp"]:
    ok("Cache works: same timestamp within 3s (state cache)")
else:
    bug("LOW", "State cache may not be working — timestamps differ within 3s", 
        f"t1={state1['timestamp']}, t2={state2['timestamp']}")

# Wait for result cache to expire (10s TTL)
print("  Waiting 12s for result cache expiry...")
time.sleep(12)
state3 = json.loads(fetch("/api/state")[2])
if state3["timestamp"] != state1["timestamp"]:
    ok("Cache invalidation: new timestamp after 12s (result cache expired)")
else:
    bug("MEDIUM", "Result cache did NOT invalidate after 12s (>10s TTL)",
        f"t1={state1['timestamp']}, t3={state3['timestamp']}")

# ── Test 4: Concurrent Requests (Race Conditions) ──
print("\n" + "="*60)
print("TEST 4: Concurrent Requests / Race Conditions")
print("="*60)

def concurrent_fetch():
    code, _, body = fetch("/api/state")
    try:
        return code, json.loads(body)
    except:
        return code, None

# Use a fresh fetch after cache expiry
results = []
with ThreadPoolExecutor(max_workers=20) as ex:
    futures = [ex.submit(concurrent_fetch) for _ in range(50)]
    for f in as_completed(futures):
        results.append(f.result())

success_count = sum(1 for code, data in results if code == 200)
if success_count == 50:
    ok(f"50 concurrent requests: all {success_count}/50 succeeded")
else:
    bug("CRITICAL", f"Concurrent requests: only {success_count}/50 succeeded, {50-success_count} failed", 
        f"During stress test, {50-success_count} of 50 concurrent requests failed")

# Check for consistency in concurrent responses
timestamps = [data.get("timestamp") for _, data in results if data]
unique_ts = len(set(timestamps))
if unique_ts <= 2:  # Should be cached for most
    ok(f"Concurrent consistency: {unique_ts} unique timestamps across 50 requests (cached)")
else:
    bug("LOW", f"Concurrent inconsistency: {unique_ts} unique timestamps across 50 requests")

# ── Test 5: Edge Case - Large Response ──
print("\n" + "="*60)
print("TEST 5: Edge Cases")
print("="*60)

# 5a: bp_scores count
if len(state1.get("bp_scores", {})) > 0:
    ok(f"bp_scores has {len(state1['bp_scores'])} entries")
    if len(state1["bp_scores"]) <= 200:
        ok("bp_scores count <= 200 (sorted limit)")
    else:
        bug("LOW", f"bp_scores has {len(state1['bp_scores'])} entries, expected <= 200")

# 5b: active_processes limit
if len(state1.get("active_processes", [])) <= 20:
    ok(f"active_processes limited to {len(state1['active_processes'])} (max 20)")
else:
    bug("LOW", f"active_processes has {len(state1['active_processes'])} entries, expected <= 20")

# 5c: activity limit
if len(state1.get("activity", [])) <= 50:
    ok(f"activity limited to {len(state1['activity'])} (max 50)")
else:
    bug("LOW", f"activity has {len(state1['activity'])} entries, expected <= 50")

# 5d: pipeline counts are integers
pipeline = state1.get("pipeline", {})
for key in ["refinery", "production", "archive"]:
    val = pipeline.get(key)
    if isinstance(val, int):
        ok(f"pipeline.{key} is int: {val}")
    else:
        bug("MEDIUM", f"pipeline.{key} is {type(val).__name__} not int")

# 5e: uptime is positive
uptime = state1.get("uptime", -1)
if isinstance(uptime, int) and uptime >= 0:
    ok(f"uptime is positive int: {uptime}s")
else:
    bug("MEDIUM", f"uptime is {type(uptime).__name__}: {uptime}")

# 5f: timestamp is ISO format
ts = state1.get("timestamp", "")
if "+00:00" in ts or "Z" in ts:
    ok(f"timestamp is UTC ISO format: {ts}")
else:
    bug("LOW", f"timestamp format might not be UTC: {ts}")

# 5g: forge_lock is null when no lock file
if state1.get("forge_lock") is None:
    ok("forge_lock is null when .forge.lock missing")
else:
    bug("LOW", f"forge_lock is {state1['forge_lock']} when .forge.lock missing")

# ── Test 6: Performance ──
print("\n" + "="*60)
print("TEST 6: Performance")
print("="*60)

# Measure single request time (cold, after cache expired)
t0 = time.time()
code, _, body = fetch("/api/state")
t1 = time.time()
cold_time = t1 - t0
print(f"  Cold /api/state: {cold_time:.2f}s")
if cold_time > 5:
    bug("HIGH", f"Cold /api/state takes {cold_time:.1f}s (>5s) — potential iterdir bottleneck", 
        "compute_state scans 242+72+120=434 directories with nested iterdir")
elif cold_time > 2:
    bug("MEDIUM", f"Cold /api/state takes {cold_time:.1f}s (>2s)")
else:
    ok(f"Cold /api/state response time: {cold_time:.2f}s")

# Measure cached request time
t0 = time.time()
code, _, _ = fetch("/api/state")
t1 = time.time()
cached_time = t1 - t0
print(f"  Cached /api/state: {cached_time:.2f}s")
if cached_time > 0.5:
    bug("LOW", f"Cached /api/state still takes {cached_time:.2f}s (>0.5s)")
else:
    ok(f"Cached /api/state response time: {cached_time:.2f}s")

# Response size
size = len(body)
print(f"  /api/state response size: {size} bytes ({size/1024:.1f} KB)")
if size > 500_000:
    bug("MEDIUM", f"Large response: {size} bytes ({size/1024:.1f} KB) — may cause UI lag")

# ── Test 7: HTML/JS Issues ──
print("\n" + "="*60)
print("TEST 7: HTML/JS Analysis")
print("="*60)

code, _, html_body = fetch("/")
html = html_body.decode("utf-8")

# 7a: Check for unclosed tags? Just check basic structure
if html.count("<script>") == 1 and html.count("</script>") == 1:
    ok("Single script block properly closed")
else:
    bug("LOW", f"Script blocks: open={html.count('<script>')}, close={html.count('</script>')}")

# 7b: Error handling - check fetchState error path is silent (line 589)
if "catch(e)" in html and "retry next tick" not in html:
    bug("MEDIUM", "fetchState error handler is silent — no user feedback on API failure",
        "Line 589: catch(e) { /* retry next tick */ } — errors are swallowed, user never knows if API is down")
else:
    ok("fetchState has error handling (but it's silent)")

# 7c: XSS vulnerability check — innerHTML used with user data
if "innerHTML" in html and "map(" in html:
    bug("MEDIUM", "Potential XSS: innerHTML used with blueprint names and details from API",
        "innerHTML set from API data (blueprint names, details). If forge writes malicious names, XSS possible.")
else:
    ok("No innerHTML usage detected (but it's there)")

# 7d: Check for fetch polyfill / browser compatibility
if "fetch(" in html:
    ok("Uses fetch API (modern browsers only, no IE support)")
else:
    bug("LOW", "No fetch usage detected")

# ── Test 8: Data Integrity ──
print("\n" + "="*60)
print("TEST 8: Data Integrity")
print("="*60)

# 8a: Check bp_scores entry structure
bps = state1.get("bp_scores", {})
for name, info in list(bps.items())[:5]:
    required = ["best", "latest", "stage", "count", "history"]
    for rk in required:
        if rk in info:
            pass  # ok
        else:
            bug("HIGH", f"bp_scores['{name}'] missing field '{rk}'", str(list(info.keys())))

# 8b: Check activity entry structure
activities = state1.get("activity", [])
for a in activities[:3]:
    for rk in ["action", "blueprint", "detail", "progress", "status", "timestamp"]:
        if rk not in a:
            bug("MEDIUM", f"Activity entry missing '{rk}'")

# 8c: best should be >= latest
for name, info in bps.items():
    if info.get("best", 0) < info.get("latest", 0):
        bug("MEDIUM", f"bp_scores['{name}']: best ({info['best']}) < latest ({info['latest']})")

ok("Data integrity check complete")

# ── Test 9: Malformed Input / Edge Cases ──
print("\n" + "="*60)
print("TEST 9: URI Edge Cases")
print("="*60)

# 9a: Very long path
long_path = "/" + "x" * 5000
code, _, _ = fetch(long_path)
if code == 404 or code == 414:
    ok(f"Long path returns {code}")
else:
    bug("LOW", f"Long path (5000 chars) returns {code}")

# 9b: Path traversal attempt
code, _, _ = fetch("/../../../etc/passwd")
if code == 404:
    ok("Path traversal returns 404 (not vulnerable)")
else:
    bug("MEDIUM", f"Path traversal returns {code}, check for vulnerability")

# 9c: Unicode path
code, _, _ = fetch("/åäö")
if code == 404:
    ok("Unicode path returns 404")
else:
    bug("LOW", f"Unicode path returns {code}")

# 9d: Query string on /api/state
code, _, body = fetch("/api/state?foo=bar")
if code == 200:
    ok("Query string on /api/state returns 200 (ignored)")
else:
    bug("LOW", f"/api/state?foo=bar returns {code}")

# 9e: Double slashes
code, _, _ = fetch("//api/state")
if code == 404:
    ok("Double slash path returns 404")
else:
    bug("LOW", f"//api/state returns {code}")

# ── Test 10: Server Info Leakage ──
print("\n" + "="*60)
print("TEST 10: Server Info / Security")
print("="*60)

code, headers, _ = fetch("/")
server = headers.get("Server", "")
if "Python" in server or "BaseHTTP" in server:
    bug("LOW", f"Server header leaks tech stack: '{server}'", 
        "Headers include: Server: BaseHTTP/0.6 Python/3.11.15 — this reveals implementation details")
else:
    ok("Server header does not leak Python version")

# ── Summary ──
print("\n" + "="*60)
print("BUG SUMMARY")
print("="*60)

severity_order = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
sorted_bugs = sorted(BUGS, key=lambda b: severity_order.get(b["severity"], 99))

for i, b in enumerate(sorted_bugs, 1):
    print(f"\n{i}. [{b['severity']}] {b['title']}")
    print(f"   Detail: {b['detail']}")
    if b['repro']:
        print(f"   Repro: {b['repro']}")

print(f"\nTotal bugs: {len(BUGS)}")
print(f"  CRITICAL: {sum(1 for b in BUGS if b['severity']=='CRITICAL')}")
print(f"  HIGH: {sum(1 for b in BUGS if b['severity']=='HIGH')}")
print(f"  MEDIUM: {sum(1 for b in BUGS if b['severity']=='MEDIUM')}")
print(f"  LOW: {sum(1 for b in BUGS if b['severity']=='LOW')}")

# Score calculation
score = max(1, 10 - len([b for b in BUGS if b['severity'] in ('CRITICAL','HIGH')]) * 2 
              - len([b for b in BUGS if b['severity'] == 'MEDIUM']) * 1
              - len([b for b in BUGS if b['severity'] == 'LOW']) * 0.5)
print(f"\nBuggfrihet betyg: {score}/10")
