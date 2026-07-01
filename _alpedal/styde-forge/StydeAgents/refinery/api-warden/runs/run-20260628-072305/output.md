```json
{
  "check_id": "20260628_0732",
  "timestamp": "2026-06-28T07:32:00Z",
  "endpoint": {
    "url": "http://localhost:8765/api/state",
    "method": "GET",
    "server": "BaseHTTP/0.6 Python/3.11.15",
    "port": 8765,
    "process": "server_8765.py"
  },
  "health_checks": [
    {
      "test": 1,
      "name": "HTTP Status 200",
      "expected": "200 OK",
      "observed": "200 OK",
      "result": "PASS"
    },
    {
      "test": 2,
      "name": "JSON Validity",
      "expected": "parseable JSON",
      "observed": "valid JSON, 13 top-level keys: forge, pipeline, agents, blueprints, blueprint_scores, evaluations, improvements, active_processes, hardware, skills, activity, timestamp, stats",
      "result": "PASS"
    },
    {
      "test": 3,
      "name": "Response Time",
      "expected": "< 500 ms",
      "observed": "569 ms (cold: 1431 ms), average over 3 runs: 855 ms",
      "result": "FAIL",
      "root_cause_hint": "get_hardware() calls nvidia-smi subprocess every request (no cache) plus psutil.cpu_percent(interval=0.3) blocking I/O. nvidia-smi adds 200-300ms, cpu_percent adds 300ms. Recommend caching hardware data with 5-10s TTL to bring latency < 200ms."
    },
    {
      "test": 4,
      "name": "Field Completeness",
      "expected": "top-level keys: 'state', 'version', 'timestamp'",
      "observed": "'state' not found as top-level key. 'version' not found as top-level key (nested under forge.version). 'timestamp' present.",
      "result": "FAIL",
      "root_cause_hint": "Blueprint config expects state, version, timestamp at top level. API returns state under forge object and version nested under forge.version. Either update config required_fields to ['forge', 'pipeline', 'timestamp'] or add top-level state/version aliases in compute_state()."
    },
    {
      "test": 5,
      "name": "CORS Headers",
      "expected": "Access-Control-Allow-Origin present and permissive",
      "observed": "When Origin matches allowed list (localhost:8765): PASS — ACA-O, ACA-Credentials, ACA-Methods, ACA-Headers, ACA-Max-Age all present. When Origin is external (evil.com): FAIL — no CORS headers sent at all. CORS is locked to localhost only, not permissive.",
      "result": "PARTIAL_FAIL",
      "root_cause_hint": "ALLOWED_ORIGINS in server_8765.py line 23 only permits localhost:8765 and 127.0.0.1:8765. For dashboard monitoring from external tools, add monitoring domain to allowed origins or use wildcard 'Access-Control-Allow-Origin: *' for the /api/state endpoint specifically."
    }
  ],
  "latency_histogram_ms": {
    "0-50": 0,
    "50-100": 0,
    "100-200": 0,
    "200-300": 0,
    "300-400": 0,
    "400-500": 0,
    "500+": 3,
    "notes": "All observed latencies exceed 500ms threshold. Cold start can spike to 5300ms due to nvidia-smi + subprocess overhead on first call after inactivity."
  },
  "consecutive_failures": 2,
  "alert_triggered": false,
  "alert_after": 3,
  "uptime_report_entry": {
    "timestamp": "2026-06-28T07:32:00Z",
    "status": "DEGRADED",
    "pass_count": 2,
    "fail_count": 3,
    "response_time_ms": 569,
    "errors": [
      "response_time: 569ms exceeds 500ms threshold",
      "field_completeness: missing top-level keys 'state' and 'version'",
      "cors_headers: not permissive for external origins"
    ]
  }
}
```
Run complete. 2 of 5 checks pass. Alert threshold at 2 consecutive failures (3 needed to trigger). Next check in 60s.