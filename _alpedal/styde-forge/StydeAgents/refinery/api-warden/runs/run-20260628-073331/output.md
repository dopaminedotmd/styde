STATUS: CHECKS=5 FAILED=5 ALERT=ACTIVE (3 consecutive failures threshold exceeded)
endpoint: /api/state
method: GET
cycle_id: 20260628-093337
timestamp: 2026-06-28T09:33:37Z
checks:
  - id: 1
    name: HTTP Status
    result: FAIL
    observed: connection refused
    expected: 200
    severity: P0
  - id: 2
    name: JSON Validity
    result: FAIL
    observed: no response body
    expected: valid JSON
    severity: P0
    depends_on: 1
  - id: 3
    name: Response Time
    result: FAIL
    observed: no response
    expected: < 500 ms
    severity: P2
    depends_on: 1
  - id: 4
    name: Field Completeness
    result: FAIL
    observed: no response body
    expected: all required fields present
    severity: P1
    depends_on: 1,2
  - id: 5
    name: CORS Headers
    result: FAIL
    observed: no response headers
    expected: Access-Control-Allow-Origin present
    severity: P2
    depends_on: 1
alert: active
alert_reason: 3 consecutive failures - connection refused on all ports (5000, 8000, 3000)
action_priority:
  - P0: start the Forge dashboard server
  - P1: verify /api/state route exists when server is up
  - P2: add CORS middleware and timeout guardrails