Alert Engine — Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard. When the metric returns to normal, an optional recovery notification is sent. All rules, cooldowns, and escalation policies are defined in configuration and can be hot-reloaded via a dashboard admin action.
Architecture
[Telemetry Sources]
  Agent Telemetry --->|
  GPU Telemetry   --->|--> Alert Evaluator --> Notification Bus --> Dashboard UI
  System Telemetry--->|         |                      |
                               v                      v
                         Cooldown Cache          Push Dispatcher
                         (in-memory TTL)         (WebSocket + REST)
                               |
                               v
                         Persistence Layer
                         (SQLite / PostgreSQL)
Components
  Telemetry Sources — agents, GPU clusters, and system resource monitors publish structured metric payloads at regular intervals. Each payload includes agent_id, metric_name, value, and timestamp.
  Alert Evaluator — receives every metric payload and evaluates it against all active rules. Evaluation uses comparison operators defined in the rule. On threshold breach, the evaluator checks cooldown state; if the same metric-agent pair is in cooldown, the event is silently dropped. Otherwise, an alert instance is created and forwarded.
  Cooldown Cache — in-memory map keyed on (rule_id, agent_id). Each entry tracks last_triggered_at and expires after the rule's cooldown_seconds. Cache entries are ephemeral; on engine restart, cooldown is cold.
  Notification Bus — receives alert events from the evaluator and dispatches them through registered channels. Primary channel: WebSocket push to the Forge Dashboard real-time feed. Secondary channel: REST webhook for external integrations.
  Persistence Layer — stores alert rules and alert instances durably. See Data Model section below.
Alert Rules
Each rule is defined in YAML configuration under the alert_rules array.
Field                Type      Required  Description
id                   string    yes       Unique rule identifier. Used in cooldown keys.
metric               string    yes       Metric field name in telemetry payloads. Example: gpu_temperature, ram_usage_pct, agent_failure_rate, agent_score.
operator             string    yes       Comparison operator. See Operators table.
threshold            number    yes       Value to compare against.
severity             string    yes       Severity level: critical, warning, info.
cooldown_seconds     integer   yes       Minimum seconds between consecutive alerts for the same (rule_id, agent_id).
enabled              boolean   no        Default true. Set false to pause a rule without removing it.
recovery_enabled     boolean   no        Default false. When true, a recovery notification is sent when the metric returns below (or above for lt) the threshold.
description          string    no        Human-readable explanation of what this rule guards against.
Operators
Operator  Evaluates true when
gt        metric_value > threshold
gte       metric_value >= threshold
lt        metric_value < threshold
lte       metric_value <= threshold
eq        metric_value == threshold
neq       metric_value != threshold
outside   metric_value < lower OR metric_value > upper requires threshold_low + threshold_high
inside    metric_value >= lower AND metric_value <= upper requires threshold_low + threshold_high
Every operator must be implemented in the evaluator. Unrecognized operators cause the rule to be skipped and logged.
Example Rules
Rule: gpu-temp
  metric: gpu_temperature
  operator: gt
  threshold: 85
  severity: critical
  cooldown_seconds: 300
  recovery_enabled: true
  description: GPU temperature exceeds safe operating limit on agent worker-03.
Rule: ram-usage
  metric: ram_usage_pct
  operator: gt
  threshold: 90
  severity: warning
  cooldown_seconds: 600
  recovery_enabled: false
  description: RAM utilization above 90% on system resource monitor.
Rule: agent-failure
  metric: agent_failure_rate
  operator: gt
  threshold: 10
  severity: critical
  cooldown_seconds: 900
  recovery_enabled: true
  description: Agent failure rate exceeds 10% on any agent.
Rule: score-drop
  metric: agent_score
  operator: lt
  threshold: 15
  severity: warning
  cooldown_seconds: 1800
  recovery_enabled: true
  description: Agent score dropped below 15 points.
Rule: gpu-vram-warn
  metric: vram_usage_pct
  operator: gte
  threshold: 95
  severity: warning
  cooldown_seconds: 600
  recovery_enabled: false
  description: VRAM usage near capacity.
States
  Normal — all metrics are within bounds defined by active rules. No action taken.
  Alerting — a metric breached a rule threshold. An alert instance is created, persisted, and a push notification is dispatched via the Notification Bus.
  Cooldown — an alert was fired for a (rule_id, agent_id) pair within the last N seconds (where N = cooldown_seconds). All subsequent breaches are silently suppressed until the cooldown window expires.
  Recovered — a metric that was in Alerting state returns to within bounds. If recovery_enabled is true on the rule, a recovery notification is dispatched. The alert instance is updated with a resolved_at timestamp.
Escalation Policy
Configurable per rule. When an alert remains in Alerting state for longer than escalation_seconds, a secondary notification is sent to the escalation channel (email, pager, or higher-severity dashboard badge).
Config block:
escalation:
  escalation_seconds: 3600
  escalation_channel: email
  escalation_recipient: ops@nousresearch.com
If escalation_seconds is not set, no escalation occurs for that rule.
Recovery Notifications
When a rule has recovery_enabled set to true, the Alert Evaluator continues monitoring the metric after an alert fires. Once the metric returns to a value that would NOT breach the threshold (strictly below for gt/gte/outside operators, strictly above for lt/lte/outside operators), the evaluator:
  1. Sets the associated alert instance status to resolved with a resolved_at timestamp.
  2. Dispatches a recovery notification through the Notification Bus.
  3. Clears the cooldown cache entry for that (rule_id, agent_id), allowing immediate re-alerting if the metric breaches again.
Recovery notifications are subject to the same global rate limit as alert notifications.
Flow Detail
  1. Telemetry source publishes metric payload: {agent_id: "worker-03", metric: "gpu_temperature", value: 92, timestamp: "2026-06-28T10:00:00Z"}.
  2. Alert Evaluator loads all rules matching metric == "gpu_temperature".
  3. For each matching rule, evaluator applies operator (gt) against threshold (85). 92 > 85 is true.
  4. Evaluator checks cooldown cache for key (gpu-temp, worker-03). If present and not expired, drop event. Otherwise proceed.
  5. Evaluator creates alert instance: {id: uuid, rule_id: "gpu-temp", agent_id: "worker-03", metric_value: 92, threshold: 85, severity: "critical", triggered_at: now, status: "firing"}.
  6. Alert instance is persisted to the database. Cooldown cache entry is set with TTL = 300s.
  7. Notification Bus formats the payload and pushes via WebSocket to the dashboard. Payload: {type: "alert", severity: "critical", rule_id: "gpu-temp", agent_id: "worker-03", metric_value: 92, threshold: 85, message: "GPU temperature at 92C on agent worker-03."}.
  8. Dashboard displays the alert in the notification panel. User acknowledges or dismisses it.
  9. On next telemetry interval, value drops to 62C. Evaluator finds no breach for gt 85. Since recovery_enabled is true and there is an active (unresolved) alert instance for (gpu-temp, worker-03), evaluator marks the instance resolved with resolved_at timestamp and dispatches a recovery notification: {type: "recovery", rule_id: "gpu-temp", agent_id: "worker-03", message: "GPU temperature back to 62C on agent worker-03."}.
Rate Limiting
  Global — maximum 10 alert notifications per agent per hour, regardless of how many rules breach. Counted from persisted alert instances with status firing and triggered_at within the last 3600 seconds. When the limit is reached, further alerts for that agent are silently dropped until the hourly window resets.
  Per rule — maximum 5 alert notifications per (rule_id, agent_id) per hour, regardless of the per-rule cooldown_seconds value. Enforced via a sliding window counter keyed on (rule_id, agent_id, hour_bucket).
Configuration
All rules and engine settings are defined in a single config.yaml file. The engine reads config on startup. A hot-reload endpoint is available via the dashboard admin panel; calling it triggers a config file re-read and rule cache rebuild. If the config file is malformed or missing required fields, the engine logs the error, skips the offending rule, and continues with the remaining valid rules. The engine never crashes on bad input.
Config file structure:
engine:
  rate_limit:
    alerts_per_agent_per_hour: 10
    alerts_per_rule_per_hour: 5
  evaluation_interval_seconds: 15
  persistence:
    backend: sqlite
    path: /var/lib/forge/alert_engine.db
    auto_migrate: true
  auth:
    enabled: true
    mechanism: api_key
    api_key_header: X-Forge-Api-Key
    rbac_rules_path: /etc/forge/rbac.yaml
  websocket:
    port: 8082
    heartbeat_interval_seconds: 30
alert_rules:
  - id: gpu-temp
    metric: gpu_temperature
    operator: gt
    threshold: 85
    severity: critical
    cooldown_seconds: 300
    recovery_enabled: true
    description: GPU temperature exceeds safe operating limit.
  - id: ram-usage
    metric: ram_usage_pct
    operator: gt
    threshold: 90
    severity: warning
    cooldown_seconds: 600
    recovery_enabled: false
    description: RAM utilization above 90%.
Data Model and Storage
The Alert Engine uses two persistent stores: a rules store for rule definitions and an alerts store for alert instances.
Alert Rule Schema (relational table: alert_rules)
Column              Type       Constraints
id                  TEXT       PRIMARY KEY
metric              TEXT       NOT NULL
operator            TEXT       NOT NULL
threshold           REAL       NOT NULL
threshold_low       REAL       NULL (for inside/outside operators)
threshold_high      REAL       NULL (for inside/outside operators)
severity            TEXT       NOT NULL CHECK (severity IN ('critical','warning','info'))
cooldown_seconds    INTEGER    NOT NULL DEFAULT 300
enabled             INTEGER    NOT NULL DEFAULT 1
recovery_enabled    INTEGER    NOT NULL DEFAULT 0
escalation_seconds  INTEGER    NULL
escalation_channel  TEXT       NULL
description         TEXT       NULL
updated_at          TEXT       NOT NULL DEFAULT CURRENT_TIMESTAMP
created_at          TEXT       NOT NULL DEFAULT CURRENT_TIMESTAMP
Rule CRUD API
Clients manage rules through a RESTful HTTP API mounted on the Forge Dashboard backend. All CRUD operations require authentication (see Auth section).
Endpoint                        Method  Auth Required  Description
/api/v1/alert/rules             GET     read            List all rules. Supports ?enabled=true/false and ?severity=critical filters.
/api/v1/alert/rules/:id         GET     read            Get a single rule by ID.
/api/v1/alert/rules             POST    write           Create a new rule. Body must include metric, operator, threshold, severity, cooldown_seconds. Returns 201 on success, 422 on validation failure.
/api/v1/alert/rules/:id         PUT     write           Replace an existing rule. Full body required. Returns 200 on success, 404 if not found.
/api/v1/alert/rules/:id         PATCH   write           Partial update on an existing rule. Only supplied fields are changed. Returns 200 on success, 404 if not found.
/api/v1/alert/rules/:id         DELETE  write           Delete a rule. Returns 204 on success, 404 if not found. Does not delete historical alert instances associated with the rule.
/api/v1/alert/rules/hot-reload  POST    admin           Re-read config.yaml and rebuild the rule cache. Returns 200 with reloaded rule count.
All POST/PUT/PATCH requests accept JSON body with Content-Type: application/json. Validation returns a detailed error object listing each invalid field.
Alert Instance Schema (relational table: alert_instances)
Column           Type       Constraints
id               TEXT       PRIMARY KEY
rule_id          TEXT       NOT NULL REFERENCES alert_rules(id) ON DELETE RESTRICT
agent_id         TEXT       NOT NULL
metric_value     REAL       NOT NULL
threshold        REAL       NOT NULL
severity         TEXT       NOT NULL
status           TEXT       NOT NULL DEFAULT 'firing' CHECK (status IN ('firing','resolved','acknowledged'))
triggered_at     TEXT       NOT NULL
resolved_at      TEXT       NULL
acknowledged_at  TEXT       NULL
acknowledged_by  TEXT       NULL
notification_sent INTEGER   NOT NULL DEFAULT 0
Index: idx_instances_status on alert_instances(status)
Index: idx_instances_agent on alert_instances(agent_id)
Index: idx_instances_rule_agent_time on alert_instances(rule_id, agent_id, triggered_at)
Storage Backend
  Development / single-node: SQLite via the path configured in engine.persistence.path. Auto-migration is enabled by default; the engine creates tables if they do not exist and applies schema version upgrades on startup.
  Production / multi-node: PostgreSQL. The engine.persistence.backend setting controls which driver is loaded. Connection string is read from engine.persistence.dsn when backend is postgresql.
  Time-series data (metric history for dashboards and trend detection): optional. If engine.persistence.timeseries_backend is set to influxdb or timescaledb, metric payloads are also forwarded to the time-series store at a configurable sample rate.
Migration Strategy
  Phase 1: Auto-create tables on startup using CREATE TABLE IF NOT EXISTS. Schema version stored in a meta table (schema_version with version integer). On each startup, the engine compares the stored version against the code's expected version and runs migration scripts sequentially.
  Phase 2: Migration scripts live in migrations/ directory as numbered files: 001_create_alert_rules.sql, 002_create_alert_instances.sql, 003_add_escalation_columns.sql, etc. Each script is idempotent and wrapped in a transaction.
  Phase 3: On schema mismatch, the engine logs the upgrade plan, runs migrations, and updates schema_version. If a migration fails, the engine logs the error and exits cleanly — it does not start with an inconsistent schema.
Authentication and Authorization
  Auth Mechanism: API key passed via the X-Forge-Api-Key header. Keys are pre-generated, stored as SHA-256 hashes in the database (api_keys table), and associated with a role name.
  RBAC: Roles define allowed scopes. Scopes are hierarchical:
    Scope           Privileges
    alert:read      List and view alert rules, view alert instances, view alert history
    alert:write     Create, update, delete alert rules; acknowledge alert instances
    alert:admin     Full access including hot-reload, config changes, user management
    alert:webhook   Receive webhook notifications (outbound)
    Roles in config:
      viewer   -> alert:read
      operator -> alert:read, alert:write
      admin    -> alert:read, alert:write, alert:admin
      webhook  -> alert:webhook
  Ownership and Visibility:
    Rules are global — any authenticated user with alert:read can see all rules.
    Alert instances are scoped to agents that the authenticated user has access to. The user's scope includes a list of allowed agent_id patterns (glob-style: worker-*, gpu-rack-03). If no agent pattern is set, the user sees all instances.
    When creating a rule, the creator's user_id is stored in the rule's created_by field (TEXT, nullable). This enables per-user rule listings but does not restrict visibility for other users with alert:read.
  Unauthenticated Access:
    The /api/v1/alert/rules/hot-reload endpoint returns 401 if no API key is provided.
    All CRUD endpoints return 401 if no API key is provided.
    WebSocket connections for dashboard notifications are authenticated at connection time using the same API key mechanism. Invalid keys are disconnected immediately with a 4001 close code.
  Key Management:
    API keys are managed through a separate admin endpoint at /api/v1/admin/keys (requires alert:admin scope). Keys are issued by name, stored hashed, and returned in plaintext exactly once at creation time.
Constraints
  Never alert on the same (rule_id, agent_id) pair more than once per cooldown window.
  Never evaluate config that is malformed or missing required fields — log the error and skip the rule.
  Respect global rate limit of 10 alerts per agent per hour. Respect per-rule rate limit of 5 alerts per (rule_id, agent_id) per hour.
  Cooldown cache is ephemeral — no persistence between engine restarts.
  Recovery notifications are optional and explicitly enabled per rule.
Decision-making Principles
  Accuracy over speed — prefer a true positive over a rushed evaluation. If the evaluator cannot parse a metric payload, it logs the parse failure and moves to the next payload without alerting.
  Silence is healthy — no news means all metrics are within bounds. Absence of alert notifications is not a bug; it is the normal operating state.
  Self-preservation — log errors internally; never crash on bad input. Malformed config, empty metric payloads, missing fields, and unknown operators all produce log entries and are safely skipped.
Error Handling
  Invalid rule config — log error, skip rule, continue.
  Unknown operator — log warning, skip rule, continue.
  Corrupt telemetry payload — log error, skip payload, continue.
  Database write failure — log error, queue alert for retry, continue evaluation.
  Websocket push failure — log error, continue (alerts are still persisted; client reconnection will receive missed alerts on reconnect).
  Hot-reload with invalid config — log error, continue with previous config, notify admin via error channel.