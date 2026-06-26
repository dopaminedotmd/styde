# Styde Forge API Reference

Two HTTP servers provide monitoring and control. Both serve localhost only.

---

## Mission Control (port 8765)

Production-grade API with security headers, CSRF protection, and gzip compression.

Base URL: `http://localhost:8765`

### GET Endpoints

### GET /
Serves the Mission Control HTML dashboard.

Response 200: `text/html` with dashboard UI. Gzip compressed if client supports it.

Security headers: CSP, X-Frame-Options: DENY, X-Content-Type-Options: nosniff, Referrer-Policy, Permissions-Policy.

### GET /index.html
Alias for `GET /`.

### GET /api/state
Full forge state including blueprint scores, tier breakdown, subagent status, activity, uptime.

Response 200: `application/json`

```json
{
  "bp_scores": {
    "code-reviewer": {
      "best": 92.0,
      "latest": 87.8,
      "avg": 87.2,
      "count": 3,
      "stage": "refinery",
      "run_id": "20260626-120751",
      "iteration": 3
    }
  },
  "tiers": {
    "General": {
      "tier": "General",
      "total": 7,
      "passed": 2,
      "avg_score": 72.4,
      "highest": 92.0,
      "agents": [
        {
          "name": "mockup-to-code-converter",
          "score": 0,
          "best": 0,
          "target": 95,
          "stage": "not_started",
          "eval_count": 0,
          "progress": 0
        }
      ],
      "subagent": {
        "id": 1,
        "status": "pending",
        "current_bp": "",
        "progress": 0,
        "started_at": null,
        "finished_at": null,
        "error": null
      }
    }
  },
  "totals": {
    "total": 46,
    "production": 0,
    "refinery": 12,
    "passed_target": 0,
    "avg_all": 67.3
  },
  "forge_lock": {"pid": 15620, "acquired": "2026-06-26T17:42:54Z"},
  "activity": [],
  "uptime": 3600,
  "timestamp": "2026-06-26T20:00:00Z"
}
```

### GET /api/health
Simple health check.

Response 200: `application/json`

```json
{"status": "ok", "uptime": 3600.0}
```

### GET /api/state.yaml
Raw state.yaml content.

Response 200: `text/yaml`

Returns the raw state.yaml file bytes.

### GET /api/skills
List all available skills from blueprint skill directories.

Response 200: `application/json`

```json
{
  "skills": [
    {"name": "code-review", "blueprint": "code-reviewer", "path": ".../skills/code-review.md"}
  ]
}
```

### GET /api/activity
Recent activity log entries.

Response 200: `application/json`

```json
{
  "activity": [
    {"action": "spawn", "blueprint": "code-reviewer", "detail": "Spawn complete", "progress": 100, "status": "complete", "timestamp": "..."}
  ]
}
```

### GET /api/csrf-token
Generate a signed CSRF token for POST requests.

Response 200: `application/json`

```json
{"csrf_token": "<signed-token-string>"}
```

### POST Endpoints

All POST endpoints require:
- Header `X-CSRF-Token`: valid CSRF token (obtain via `GET /api/csrf-token`)
- Header `Content-Type`: `application/json`
- Request body: JSON, max 64 KB

### POST /api/spawn
Dispatch an agent spawn via subprocess.

Request body:
```json
{"blueprint": "code-reviewer"}
```

Response 200: `application/json`
```json
{"ok": true}
```

### POST /api/eval
Run evaluation on an agent run.

Request body:
```json
{"blueprint": "code-reviewer", "run_id": "latest"}
```

`run_id` optional, defaults to "latest".

Response 200: `application/json`
```json
{"ok": true}
```

### POST /api/improve
Run teacher improvement on a specific run.

Request body:
```json
{"blueprint": "code-reviewer", "run_id": "20260626-120751"}
```

`run_id` is required.

Response 200: `application/json`
```json
{"ok": true}
```

### POST /api/toggle-caveman
Toggle Caveman Ultra mode on/off in state.yaml.

Request body: (empty or any JSON)

Response 200: `application/json`
```json
{"ok": true}
```

### POST /api/loop
Dispatch a full forge loop (spawn → eval → improve cycle).

Request body: (empty or any JSON)

Response 200: `application/json`
```json
{"ok": true}
```

---

## Command Center (port 8766)

Minimalist read-only API. No security headers.

Base URL: `http://localhost:8766`

### GET Endpoints

### GET /
Serves the Command Center HTML dashboard.

Response 200: `text/html`

Dark-themed sidebar + tier grid. Polls `/api/state` every 3 seconds.

### GET /api/state
Blueprint scores + tier stats + activity + lock status. Same general structure as Mission Control but computed directly (not cached).

Response 200: `application/json`

Structure identical to Mission Control `/api/state` but computed from live `load_state()` call (no cache).

---

## Error Responses

### 404 Not Found
```json
{"error": "not found"}
```

### 400 Bad Request
```json
{"error": "invalid blueprint name"}
```

### 403 Forbidden
```json
{"error": "invalid or missing CSRF token"}
```

### 413 Payload Too Large
```json
{"error": "request body too large"}
```
