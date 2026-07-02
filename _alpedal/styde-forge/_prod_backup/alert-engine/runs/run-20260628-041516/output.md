Alert Engine -- Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard.
Architecture
┌─────────────────────┐
│   Telemetry Sources  │
│  ┌─────┐ ┌────┐ ┌──┐│
│  │Agent│ │GPU │ │RAM││
│  └──┬──┘ └─┬──┘ └┬─┘│
│     │      │     │   │
└─────┼──────┼─────┼───┘
      │      │     │
      ▼      ▼     ▼
┌─────────────────────┐
│   Alert Evaluator    │
│  ┌─────────────────┐│
│  │  Rule Engine     ││
│  │  - Thresholds   ││
│  │  - Cooldowns    ││
│  │  - Severities   ││
│  │  - DynamicDrop  ││
│  └────────┬────────┘│
└───────────┼─────────┘
            │ trigger
            ▼
┌─────────────────────────┐
│    Notification Bus     │
│  ┌─────────────────────┐│
│  │  Disconnect Buffer  ││
│  │  Replay + Dedup     ││
│  │  Push Dispatcher    ││
│  │  -> Dashboard UI    ││
│  └──────────┬──────────┘│
└─────────────┼───────────┘
              │
              ▼
┌─────────────────────┐
│  Alert Routing Hub   │
│  Slack | Email | PD  │
└─────────────────────┘
Persistence and State Management
Backend  Schema  Table  Purpose
SQLite  alert_events  id, rule_id, agent_id, metric, value, severity, status, triggered_at, resolved_at  Persistent alert event history with TTL-based cleanup
SQLite  cooldown_state  rule_id, agent_id, suppressed_until, trigger_count  Cooldown state persisted across engine restarts; cooldown survives process crash
SQLite  config_snapshots  id, yaml_checksum, applied_at, status  Config change audit trail
TTL cleanup runs every 60 seconds. Stale alert_events older than 7 days are evicted. Stale cooldown_state entries older than 2 hours (no alert during that window) are evicted. Cleanup logs count of purged rows at debug level.
Schema: alert_events
  id          TEXT PRIMARY KEY (uuid v4)
  rule_id     TEXT NOT NULL
  agent_id    TEXT NOT NULL
  metric      TEXT NOT NULL
  value       REAL NOT NULL
  threshold   REAL NOT NULL
  severity    TEXT CHECK(severity IN ('info','warning','critical'))
  status      TEXT CHECK(status IN ('active','recovered','suppressed'))
  triggered_at  TEXT NOT NULL (ISO 8601)
  resolved_at   TEXT
  notified_count INTEGER DEFAULT 1
Schema: cooldown_state
  rule_id         TEXT NOT NULL
  agent_id        TEXT NOT NULL
  suppressed_until  TEXT NOT NULL (ISO 8601)
  trigger_count   INTEGER DEFAULT 1
  PRIMARY KEY (rule_id, agent_id)
Schema: config_snapshots
  id            TEXT PRIMARY KEY (uuid v4)
  yaml_checksum TEXT NOT NULL
  rules_count   INTEGER NOT NULL
  applied_at    TEXT NOT NULL (ISO 8601)
  status        TEXT CHECK(status IN ('loaded','rejected','hot-reloaded','error'))
Alert Routing and Escalation
Severity  Default Channel  Slack Channel  Email  PagerDuty
critical  dashboard push   #alerts-critical  infra+oncall@example.com  PD service key (high urgency)
warning   dashboard push   #alerts-warning   infra@example.com       not routed
info      dashboard push   not routed        not routed               not routed
Routing policy is defined per-rule in config.yaml under the 'routing' key. Each rule can override the default routing table above. Example:
rules:
  - id: gpu-temp
    routing:
      slack: "#gpu-alerts"
      email: "gpu-team@example.com"
      pagerduty: true
      escalation_delay: 300
Escalation: If a critical alert remains unacknowledged for 5 minutes (escalation_delay in seconds), the engine re-dispatches the alert through the next escalation tier. Tiers: dashboard push -> Slack -> email -> PagerDuty. Escalation timer resets on alert recovery.
Schema Validation and Hot-Reload
All alert rule config is validated against a JSON Schema before loading. Validation runs on:
  - Engine startup (fail-fast)
  - File change detected via watchdog/inotify on config.yaml
  - Admin-triggered hot-reload via dashboard action (POST /admin/alert-config/reload)
On file change, the engine:
  1. Reads raw YAML from config.yaml.
  2. Validates against the schema defined in alert_rules_schema.json.
  3. On validation error: log full error, skip reload, retain last valid config.
  4. On valid: atomically swap rule table, log success, update config_snapshots.
JSON Schema enforces:
  - Each rule must have id, metric, threshold, severity, cooldown_seconds.
  - severity must be one of: info, warning, critical.
  - metric must be a non-empty string matching known metrics (GPU temperature, RAM utilization, agent failure rate, agent score drop, custom if prefixed with custom_).
  - threshold must be a number.
  - routing keys (slack, email, pagerduty) are optional.
  - dynamicdrop config (window, sensitivity, threshold_fraction) is optional.
Alert Aggregation and Throttling
Prevents notification storms from repeated threshold breaches.
Deduplication window: 60 seconds per (rule_id, agent_id, severity) tuple. Two identical breach events within the window produce a single notification. The notification payload includes the count of suppressed duplicates.
Burst limit: maximum 10 notifications per agent per hour. When exceeded, alerts are grouped into a single summary notification every 10 minutes:
  "GPU temperature breached 8 times on worker-03 in the last hour. Latest: 91C at 14:23:00."
Grouped summary format:
  - Counting header: [severity] metric breached N times on agent in last window.
  - Up to 3 latest timestamps with values.
  - Link to dashboard alert history.
Throttle state is held in-memory (not persisted) and resets on engine restart.
Dynamic Drop Detection
The DynamicDrop algorithm transitions an alert from dynamicdrop state to alert-ok based on a trailing-window statistical baseline rather than a static threshold.
Algorithm:
  - Maintain a rolling window of metric samples per (rule_id, agent_id). Default window: 300 seconds (configurable).
  - Let baseline = rolling median of values in window. Let stddev = rolling MAD (median absolute deviation).
  - Upper bound = baseline + sensitivity * stddev. Sensitivity default: 3.0 (configurable per rule).
  - A metric value that drops from above the upper bound to below the lower bound (baseline - sensitivity * stddev) in fewer than 3 consecutive samples triggers the dynamicdrop state.
  - Transition from dynamicdrop to alert-ok: metric returns to within (baseline +- sensitivity * stddev) and stays there for 2 consecutive evaluation cycles.
  - If the metric stays in dynamicdrop for more than 300 seconds without recovering, the engine escalates to a critical alert regardless of the dynamic bounds.
Configurable per rule:
rules:
  - id: gpu-temp
    dynamicdrop:
      enabled: true
      window_seconds: 300
      sensitivity: 3.0
      escalation_timeout_seconds: 300
Notification Bus Reliability
WebSocket disconnection handling:
  - On WebSocket disconnect (detected via ping/pong timeout after 30 seconds idle), the notification bus switches to buffered mode.
  - Buffer is in-memory (ring buffer, capacity 1000 events). Exceeding capacity drops oldest events, logged at warning level.
  - On reconnect, the buffer replays events in FIFO order, one per 100ms, to avoid overwhelming the dashboard client.
  - Deduplication during replay: if the same (rule_id, agent_id, metric, severity, status) tuple already exists in the dashboard's alert store, the replayed event is skipped. Dedup window: last 60 seconds of replayed events.
  - If the buffer is larger than 100 events on reconnect, the engine sends a single summary notification ("X missed alerts during disconnection") instead of replaying individually. The full event list is available via the alert history API.
  - No disk persistence for the buffer. In-memory only. On process crash, pending notifications during disconnection are lost.
Alert Rules
Rule ID  Metric  Threshold  Severity  Cooldown  DynamicDrop  Routing
gpu-temp  GPU Temperature  > 85 C  critical  300s  enabled  dashboard + slack + email + PD
ram-usage  RAM Utilization  > 90 %  warning  600s  disabled  dashboard
agent-failure  Agent Failure Rate  > 10 %  critical  900s  disabled  dashboard + slack + PD
score-drop  Agent Score Drop  > 15 points  warning  1800s  enabled  dashboard
Flow
  Telemetry sources publish metrics at regular intervals.
  The Alert Evaluator checks every metric against all active rules.
  If dynamicdrop is enabled for the matched rule, the evaluator computes rolling baseline + bounds and checks the drop velocity condition instead of the static threshold.
  On breach: a notification event is created, respecting per-rule cooldown and global burst limits.
  The event is persisted to alert_events and cooldown_state is updated.
  The Notification Bus constructs the push payload and dispatches to the dashboard.
  If the dashboard WebSocket is disconnected, the event enters the in-memory ring buffer.
  On reconnect, buffered events are replayed with deduplication.
  If routing includes external channels, the event is also dispatched via Slack webhook, SMTP, or PagerDuty API as per the severity-to-channel routing table.
  The user sees the alert in the dashboard notification panel.
States
  Normal -- all metrics within bounds.
  Alerting -- threshold breached; notification sent.
  DynamicDrop -- metric dropped sharply outside dynamic bounds; evaluation in progress.
  Cooldown -- alert fired recently; suppressed until cooldown expires.
  Recovered -- metric returned to normal; optional recovery notification sent.
Configuration
All rules are defined in config.yaml. The engine reloads config on startup and supports hot-reload via watchdog inotify or admin action. Config is validated against JSON Schema before loading. Invalid config is rejected with a descriptive error log; the engine continues with the last valid config.