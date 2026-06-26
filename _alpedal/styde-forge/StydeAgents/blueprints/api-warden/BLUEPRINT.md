# API-Warden — Forge Dashboard Blueprint

## Purpose
Monitors the `/api/state` endpoint of the Forge dashboard, verifying availability, correctness, and performance. Generates uptime reports and latency histograms for operational visibility.

## Monitored Endpoint
- **URL**: `/api/state`
- **Method**: `GET`
- **Expected Content-Type**: `application/json`

## Health Checks

| # | Test | Criteria |
|---|------|----------|
| 1 | HTTP Status | Must return `200 OK` |
| 2 | JSON Validity | Response body must be parseable as valid JSON |
| 3 | Response Time | Latency must be < 500 ms |
| 4 | Field Completeness | All expected fields must be present in the JSON body |
| 5 | CORS Headers | Response must include permissive CORS headers (e.g. `Access-Control-Allow-Origin`) |

## Artifacts

### Uptime Report
- Produced every check cycle
- Records: timestamp, status (pass/fail), response time (ms), error detail (if any)

### Latency Histogram
- Bucketed response-time distribution (ms): 0–50, 50–100, 100–200, 200–300, 300–400, 400–500, 500+
- Updated after each check run

## Integration
Consumed by the Forge dashboard to display real-time API health. Alert thresholds (e.g. 3 consecutive failures) are configurable upstream.

## Failure Handling
- On non-200 status: log the HTTP code and reason
- On invalid JSON: log raw body snippet (first 1 KB)
- On timeout / connection error: mark as down, skip field validation
