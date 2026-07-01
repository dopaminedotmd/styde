api-warden v1.0 monitoring script
python3 << 'PYEOF'
import requests
import time
import json
import sys
import os
from collections import defaultdict
from datetime import datetime, timezone
ENDPOINT = "http://localhost:5000/api/state"
INTERVAL = 60
TIMEOUT = 5
REQUIRED_FIELDS = ["status", "state", "version"]
EXPECTED_ORIGIN = "*"
LATENCY_BUCKETS = [0, 50, 100, 200, 300, 400, 500]
BUCKET_LABELS = ["0-50", "50-100", "100-200", "200-300", "300-400", "400-500", "500+"]
uptime_log = []
latency_histogram = defaultdict(int)
consecutive_failures = 0
def bucket_latency(ms):
    for i, bound in enumerate(LATENCY_BUCKETS):
        if ms <= bound:
            return BUCKET_LABELS[i]
    return BUCKET_LABELS[-1]
def check_endpoint():
    start = time.time()
    try:
        resp = requests.get(ENDPOINT, timeout=TIMEOUT)
        elapsed_ms = round((time.time() - start) * 1000)
    except requests.exceptions.Timeout:
        return {"status": "fail", "checks": {"http_status": "timeout", "latency": None}, "latency_ms": None, "error": "timeout"}
    except requests.exceptions.ConnectionError as e:
        return {"status": "fail", "checks": {"http_status": "connection_error", "latency": None}, "latency_ms": None, "error": f"connection_error: {e}"}
    except Exception as e:
        return {"status": "fail", "checks": {"http_status": "exception", "latency": None}, "latency_ms": None, "error": str(e)}
    failed_checks = {}
    if resp.status_code != 200:
        failed_checks["http_status"] = f"expected 200, got {resp.status_code}"
    if elapsed_ms >= 500:
        failed_checks["latency"] = f"expected <500ms, got {elapsed_ms}ms"
    try:
        body = resp.json()
    except json.JSONDecodeError:
        failed_checks["json_valid"] = f"invalid json: {resp.text[:1024]}"
        body = {}
    missing = [f for f in REQUIRED_FIELDS if f not in body]
    if missing:
        failed_checks["field_completeness"] = f"missing fields: {missing}"
    cors_origin = resp.headers.get("Access-Control-Allow-Origin", "")
    if cors_origin != EXPECTED_ORIGIN:
        failed_checks["cors_headers"] = f"expected Access-Control-Allow-Origin: {EXPECTED_ORIGIN}, got: {cors_origin}"
    overall = "pass" if not failed_checks else "fail"
    return {"status": overall, "checks": failed_checks, "latency_ms": elapsed_ms, "error": None}
def histogram_lines():
    if sum(latency_histogram.values()) < 2:
        return ["insufficient data for histogram"]
    lines = []
    for label in BUCKET_LABELS:
        count = latency_histogram.get(label, 0)
        bar = "#" * min(count, 40)
        lines.append(f"  {label:>8}ms | {count:>4} {bar}")
    return lines
def run_cycle(cycle_num):
    global consecutive_failures
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = check_endpoint()
    result["timestamp"] = ts
    result["cycle"] = cycle_num
    uptime_log.append(result)
    if result["status"] == "pass":
        consecutive_failures = 0
        if result["latency_ms"] is not None:
            bucket = bucket_latency(result["latency_ms"])
            latency_histogram[bucket] += 1
    else:
        consecutive_failures += 1
    report = {
        "timestamp": ts,
        "cycle": cycle_num,
        "status": result["status"],
        "response_time_ms": result["latency_ms"],
        "consecutive_failures": consecutive_failures,
        "check_count": len(uptime_log),
        "pass_count": sum(1 for r in uptime_log if r["status"] == "pass"),
        "fail_count": sum(1 for r in uptime_log if r["status"] == "fail"),
        "checks": result["checks"] if result["checks"] else None,
        "error": result["error"],
        "alert": consecutive_failures >= 3
    }
    payload = json.dumps(report, indent=2)
    print(payload)
    if consecutive_failures >= 3:
        print(f"ALERT: {consecutive_failures} consecutive failures at cycle {cycle_num}", file=sys.stderr)
    print(f"UPTIME: pass={report['pass_count']} fail={report['fail_count']} total={report['check_count']}")
    hlines = histogram_lines()
    for l in hlines:
        print(l)
    sys.stdout.flush()
def main():
    print("api-warden starting | endpoint: " + ENDPOINT + " | interval: " + str(INTERVAL) + "s")
    sys.stdout.flush()
    cycle = 0
    while True:
        cycle += 1
        run_cycle(cycle)
        time.sleep(INTERVAL)
if __name__ == "__main__":
    main()
PYEOF