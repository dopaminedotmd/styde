API-Warden initializing. Monitoring target: Forge Dashboard /api/state.
No endpoint reachable yet. First check cannot proceed because target origin is not configured in this environment. Required: base URL for the Forge dashboard (e.g., http://localhost:8080 or https://forge.example.com).
Until a base URL is provided, all health checks remain skipped. No uptime report, no latency histogram, no alert state.
yaml
status: idle
reason: missing_base_url
action_required: provide target origin URL for /api/state
checks_executed: 0
checks_passed: 0
checks_failed: 0
latency_histogram_ms: {}
last_alert: null
After a base URL is configured, API-Warden begins checking every 60 seconds. Three consecutive failures trigger an alert. All checks must pass for a clean pass. Any deviation (wrong status code, slow response, missing field, missing CORS header) is logged with exact observed and expected values.