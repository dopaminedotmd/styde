api-warden check: 2026-06-28T07:39:42Z
cycle: 1/1
endpoint: http://localhost:8765/api/state
STATUS: DEGRADED  (2 pass, 3 fail)
health checks:
 1  HTTP_STATUS ............. PASS
    expected: 200
    got: 200
 2  JSON_VALIDITY ........... PASS
    expected: parseable JSON
    got: valid JSON (612792 bytes, 13 top-level keys)
 3  RESPONSE_TIME ........... FAIL
    expected: < 500 ms
    observed: 1280 ms (time_starttransfer - time_pretransfer)
    note: 1.28s server processing, 2.56x threshold
 4  FIELD_COMPLETENESS ...... FAIL
    expected: state, version, timestamp at root
    observed: timestamp present; state missing at root (nested under forge.is_working); version missing at root (nested under forge.version)
    severity: high — consumers expecting flat schema will break
 5  CORS_HEADERS ............ FAIL
    expected: Access-Control-Allow-Origin, Access-Control-Allow-Methods, Access-Control-Allow-Headers
    observed: none of the three required CORS headers present
    note: OPTIONS preflight returns 204 with 0 CORS headers
action items by priority:
  P0  FIELD_COMPLETENESS: add state and version keys at JSON root, or update config.required_fields to match forge.version / forge.is_working nesting
  P1  CORS_HEADERS: server must emit Access-Control-Allow-Origin: * (or origin-echo) on all responses; add Allow-Methods and Allow-Headers to OPTIONS handler
  P2  RESPONSE_TIME: 1.28s server-side processing exceeds 500ms threshold by 2.56x — likely caused by get_hardware() calling nvidia-smi subprocess + psutil.cpu_percent(interval=0.5) on every request; cache hardware telemetry with 5s TTL
latency histogram (1 sample, insufficient for distribution): bucket 500+ (1)
uptime: 0 consecutive passes since session start, 1 consecutive failure (field + CORS + latency)
---
note: this is a live check against the running server on port 8765. The output is a monitoring report, not a file write. No artifacts were persisted.