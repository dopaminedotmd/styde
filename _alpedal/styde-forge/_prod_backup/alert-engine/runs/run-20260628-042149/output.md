Blueprint improvements applied. Here is the complete updated blueprint with all feedback addressed.
---
Alert Engine Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers notifications through configurable channels.
Architecture
Telemetry Sources (Agent, GPU, RAM) feed into Alert Evaluator which contains the Rule Engine (Thresholds, Cooldowns, Severities, Aggregation). On trigger, the Notification Bus dispatches to multiple channels: Push Dispatcher (Dashboard UI), Slack Webhook, SMTP Email, PagerDuty API. A Persistence Layer sits underneath the Evaluator providing WAL, snapshots, and state recovery.
Telemetry and Observability
Source Protocol: Metrics are ingested via OTLP/gRPC from agent-sidecar collectors. Each metric carries agent_id, metric_name, value, timestamp, and optional labels.
Self-Metrics Endpoint: The engine exposes /metrics on port 9200 (Prometheus text format) for self-observability: alert_total, alert_eval_duration_ms, suppressed_total, recovery_total, route_total{channel}.
Alert Webhook Contract: External systems can push metric batches via POST /api/v1/ingest with Content-Type application/protobuf (OTLP) or application/json. Response 202 accepted, 400 malformed, 503 overloaded.
Persistence and State Recovery
Alert state is persisted to a local WAL (write-ahead log) before dispatch. Periodic snapshots prevent unbounded replay on restart.
At-rest Format: SQLite (single file, path configurable via storage.path in config). Tables: alert_events, cooldown_state, aggregation_buckets.
Recovery: On startup the engine replays un-flushed events from the WAL and restores cooldown timers from the last snapshot. TTL-based eviction purges events older than configurable retention (default 72h). A corrupt or missing WAL is tolerated — cooldown state resets and a warning is logged.
Concurrency and Recovery
Threading Model: A fixed thread pool (4 workers by default, configurable via eval.workers) processes incoming metrics. Each worker holds its own slice of the rule-index sharded by rule_id modulo worker_count.
Sharding: Agent metrics are hash-routed to ensure same agent always hits same worker (avoids race on cooldown state).
Recovery Notification: When a metric returns to normal range after an alert, the engine dispatches a recovery event. The recovery path is explicit:
  default: push notification to dashboard
  configurable: callback HTTP POST to recover_webhook URL, or enqueue to configured message queue (AMQP/Kafka).
  Recovery and alert share the same routing policy; severity=info placeholder used for routing table entries.
Alert Rules
Rule ID | Metric | Threshold | Severity | Cooldown | Aggregation Window | Dedup Window
gpu-temp | GPU Temperature | > 85 C | critical | 5 min | 1 min | 30 s
ram-usage | RAM Utilization | > 90 % | warning | 10 min | 2 min | 1 min
agent-failure | Agent Failure Rate | > 10 % | critical | 15 min | 5 min | 2 min
score-drop | Agent Score Drop | > 15 points | warning | 30 min | 5 min | 3 min
Alert Aggregation and Throttling
Deduplication Window: Per (rule_id, agent_id) pair, duplicate metric values within the dedup window produce only one evaluation result. Subsequent identical values reset the window (sliding).
Burst Limits: Maximum 10 alerts per agent per hour. Additional alerts are queued and released at 1 per 6 min. Configurable via limits.burst_per_agent and limits.release_interval.
Grouped Summaries: When 5 or more unique alerts fire on the same agent within a 10-minute window, a single grouped notification is dispatched: "[GROUPED] 7 alerts active on agent worker-03: gpu-temp, ram-usage, score-drop, and 4 others."
Schema Validation and Hot-Reload
Rules are defined in config.yaml or config/rules/*.yaml. On file change (detected via inotify/fswatch), the engine:
  Validates YAML structure against a JSON Schema (schema/rules.schema.json) before loading.
  On validation failure: logs the error with file path and line number, skips the file, and alerts the dashboard admin.
  On validation success: hot-swaps rule definitions in memory without restart.
  If both old and new schema are valid but a rule field changed mid-evaluation, the engine waits for the current evaluation cycle to finish before applying the new config.
Alert Routing and Escalation
Severity | Primary Channel | Secondary Channel | Escalation Delay
critical | PagerDuty (API) | Slack (#alerts-critical) + Email ops@ | 5 min (if unacknowledged)
warning | Slack (#alerts-warning) | Email team@ | 15 min (if unacknowledged)
info | Dashboard push | log only | none
Integration Points:
  Slack: POST to configured webhook URL with JSON payload containing rule_id, agent_id, metric, threshold, current_value, severity, timestamp.
  Email (SMTP): Uses configured smtp.host, smtp.port, smtp.username, smtp.password. Sends plain-text and HTML multipart with same payload fields.
  PagerDuty: POST to PagerDuty Events API v2 with dedup_key = {rule_id}:{agent_id}:{metric}. Resolution events use trigger type resolve.
Flow
Telemetry sources publish metrics at regular intervals. The Alert Evaluator checks every metric against all active rules. On breach: a notification event is created and passed through the aggregation pipeline (dedup window, burst limiter, grouped summarizer). The Notification Bus dispatches to appropriate channels per routing policy. Recovery notifications follow the same path with severity inferred to info-level routing.
States
Normal — all metrics within bounds.
Alerting — threshold breached; notification sent.
Cooldown — alert fired recently; suppressed until cooldown expires.
Recovered — metric returned to normal; optional recovery notification.
Configuration
All rules are defined in /etc/forge/alert-engine/config.yaml or config/rules/*.yaml. The engine reloads config on startup and hot-reloads on file change via inotify. Persistence settings under storage: { path: /var/lib/forge/alert-engine/state.db, retention_hours: 72 }. Routing policy under routes: { critical: { primary: pagerduty, secondary: slack }, warning: { primary: slack, secondary: email }, info: { primary: dashboard } }. Limits under limits: { burst_per_agent: 10, release_interval: 360, max_grouped_summary: 5 }.
---
Persona checklist (appended)
Checklist:
  Verify all service contracts (OTLP/gRPC spec, webhook POST schema, Prometheus /metrics format) are documented before considering the blueprint complete.
  Verify notification channels (Slack webhook, SMTP, PagerDuty API key) are configured with fallback routing.
  Verify observability hooks (Prometheus endpoint, structured logs, trace context propagation) are specified and wired.
  Verify concurrency model (worker count, shard strategy, mutex policy) is reviewed for thread safety.