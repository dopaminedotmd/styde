Alert Engine — Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard.
Architecture
Telemetry Sources  →  Alert Evaluator  →  Notification Bus
  Agent / GPU / RAM      Rule Engine          Push Dispatcher
                         Thresholds             → Dashboard UI
                         Cooldowns
                         Severities
Alert Rules
Rule ID          Metric              Threshold    Severity   Cooldown
gpu-temp         GPU Temperature     > 85 C       critical   5 min
ram-usage        RAM Utilization     > 90 %       warning    10 min
agent-failure    Agent Failure Rate  > 10 %       critical   15 min
score-drop       Agent Score Drop    > 15 points  warning    30 min
Flow
Telemetry sources publish metrics at regular intervals.
The Alert Evaluator checks every metric against all active rules.
On breach: a notification event is created, respecting per-rule cooldown.
The Notification Bus dispatches a push notification to the dashboard.
The user sees the alert in the dashboard notification panel.
States
Normal — all metrics within bounds.
Alerting — threshold breached; notification sent.
Cooldown — alert fired recently; suppressed until cooldown expires.
Recovered — metric returned to normal; optional recovery notification.
Execution Constraints
This section is the single source of truth for all throttling and concurrency logic within the Alert Engine. No other section of this blueprint duplicates these definitions.
Rate Limiting (global, per agentid)
Enforced as an in-memory counter with a rolling-window sorted set: each alert event for a given agentid records a Unix-millisecond timestamp into a Redis sorted set (zset) keyed agent:alerts:<agentid>:<hour-bucket>. Before dispatching any alert, the engine runs ZREMRANGEBYSCORE to evict entries older than 3600 seconds, then ZCARD to count remaining entries. If count >= 10, the alert is dropped and an internal log line is written (rate limit exceeded for agent <agentid>). The sorted-set approach ensures O(log N) insertion and eviction. On agent restart the counter resets to zero; no state is persisted across restarts for the rate-limit counter. Config reference: config.yaml:rate_limit.max_per_agent_per_hour
Cooldown (per rule, per metric-agent pair)
Each rule defines a cooldown duration in seconds (see config.yaml:rules[].cooldown_seconds). After an alert is dispatched for a specific (rule_id, agentid) pair, the engine stores the last-fired timestamp in an in-memory dictionary (last_fired: dict[(rule_id, agentid)] = timestamp_ms). Before dispatching, the evaluator checks if time_since_last < cooldown_seconds * 1000. If yes, the alert is suppressed (silent — no repeated notification). Cooldown state is ephemeral: lost on engine restart, which is acceptable because a restart implies a fresh evaluation cycle.
Concurrency
Alert evaluation runs on a single-threaded async event loop (asyncio). Evaluations are serialized per-telemetry-source: a single metric batch is fully evaluated (all rules) before the next batch enters. This prevents race conditions on the cooldown dictionary and the rate-limit counter. The notification bus uses an internal dispatch queue with one producer (evaluator) and one consumer (HTTP push sender), ensuring ordered delivery. If the push sender is busy (in-flight request), subsequent notifications buffer up to config.yaml:dispatch.queue_capacity entries; excess notifications are dropped with a warning log.
Constraints & Limits
10 alerts per agent per hour — implemented as in-memory counter with rolling-window sorted set (see Execution Constraints: Rate Limiting above). Reset on agent restart.
Never alert on same metric-agent pair more than once per cooldown window — enforced by cooldown dictionary (see Execution Constraints: Cooldown above).
Do not evaluate malformed or missing config — log and skip. The evaluator validates each rule at load time and on hot-reload; invalid rules are collected into a skipped_rules list and logged at WARN level.
Global dispatch queue capped at config.yaml:dispatch.queue_capacity (default: 256). Beyond capacity, alerts are dropped with a WARN log.
Self-preservation — the evaluator wraps each metric evaluation in a try/except. Errors in a single rule evaluation never crash the engine; they are logged and the next metric continues.
Persistent Alert History Store
All dispatched alerts are recorded into a persistent SQLite store at data/alerts.db. Schema:
table alert_history (
  id          integer primary key autoincrement,
  rule_id     text not null,
  agentid     text not null,
  metric      text not null,
  value       real not null,
  threshold   real not null,
  severity    text not null,
  message     text not null,
  triggered_at integer not null,  -- unix epoch seconds
  recovered_at integer             -- unix epoch seconds, null until recovery
)
TTL-based compaction runs every 60 seconds via a background task: DELETE FROM alert_history WHERE triggered_at < unixepoch() - config.yaml:alert_history.retention_days * 86400. Default retention: 30 days.
GET /alerts endpoint
Exposed by the Notification Bus HTTP server on config.yaml:api.port. Parameters (query string):
agentid  (optional) — filter by agent identifier, default: all agents
page     (optional) — page number, 1-indexed, default: 1
per_page (optional) — results per page, max 100, default: 20
severity (optional) — filter by severity level (critical, warning)
since    (optional) — unix epoch timestamp, only alerts triggered after this point
Response format (JSON):
{
  "data": [
    {
      "id": 1,
      "rule_id": "gpu-temp",
      "agentid": "agent-03",
      "metric": "GPU Temperature",
      "value": 92.0,
      "threshold": 85.0,
      "severity": "critical",
      "message": "GPU temperature at 92 C on agent agent-03.",
      "triggered_at": 1719000000,
      "recovered_at": null
    }
  ],
  "page": 1,
  "per_page": 20,
  "total": 1
}
Security
Webhook HMAC signature verification: If config.yaml:webhook.secret is set, every outgoing push notification includes an X-Signature header. The value is HMAC-SHA256 of the JSON payload body, hex-encoded, keyed by webhook.secret. The dashboard UI verifies this signature on receipt; notifications with missing or invalid signatures are rejected. Config reference: config.yaml:webhook.secret
IP allowlisting: The alert receiver endpoint (used by telemetry sources to push metrics) binds to config.yaml:api.bind_address and rejects requests from IPs not in config.yaml:api.allowed_ips. If allowed_ips is empty or omitted, the endpoint binds to 127.0.0.1 only.
TLS requirement: The alert receiver endpoint and the GET /alerts HTTP server both require TLS when config.yaml:api.tls.enabled is true. Cert and key paths are set via config.yaml:api.tls.cert_path and config.yaml:api.tls.key_path. In production environments this flag defaults to true. Config reference: config.yaml:api.tls
Configuration
All rules and engine parameters are defined in config.yaml. Key top-level keys:
rules — array of rule objects, each with fields: id, metric, threshold, comparator (gt/lt/gte/lte), severity, cooldown_seconds
rate_limit — object with field max_per_agent_per_hour (default: 10)
api — object with fields port, bind_address, allowed_ips, tls
webhook — object with field secret (optional)
dispatch — object with field queue_capacity (default: 256)
alert_history — object with field retention_days (default: 30)
Full schema is documented in config.schema.json. The engine validates config.yaml against this schema on startup and on every hot-reload.
Hot-Reload Mechanism
The engine uses inotify (Linux inotify, Windows via ReadDirectoryChangesW abstraction) to watch for modifications to config.yaml and all blueprint files in the blueprints/ directory. On a change event:
1. The watcher reads the new config into memory without replacing the active config.
2. Schema validation is applied. If validation fails, the change is rejected and the previous config remains active; a WARN log is emitted with the validation errors.
3. On successful validation, the active config pointer is atomically swapped (atomic pointer swap via rename(2) on the temp file before loading; the live config is a Rust Arc<Config> or Python threading.RLock-protected reference, ensuring readers never see a half-written state).
4. The previous active config is serialized to data/config_snapshots/<timestamp>.yaml before being discarded, providing versioned config snapshots for rollback. A maximum of config.yaml:hot_reload.max_snapshots (default: 10) snapshots are retained; older snapshots are pruned on each reload.
5. The evaluator reset loop picks up the new rules, cooldowns, and rate-limit settings on the next evaluation tick (within 1 second).
Rollback is performed by copying a snapshot from data/config_snapshots/ back to config.yaml and touching the inotify watch file to trigger a reload. Config reference: config.yaml:hot_reload