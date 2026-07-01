Alert Engine Blueprint
Version: 1.1
Based-on-feedback: 20260628-035532 (90.6/100), 628-035318 (91.6/100)
Purpose: Monitor agent, GPU, and system telemetry against configurable alert rules. Push real-time notifications to the Forge Dashboard on threshold breach. Support flapping detection, alert aggregation, escalation policies, and configurable rolling-window evaluation.
Data Model
alert_rule:
  id: string (uuid)
  metric: enum [gpu_temperature, ram_utilization, agent_failure_rate, agent_score, system_load]
  metric_field: string (e.g. "gpu.temperature_celsius")
  source_type: enum [agent, gpu, system]
  operator: enum [gt, lt, gte, lte, eq]
  threshold: float
  severity: enum [info, warning, critical]
  cooldown_seconds: int
  evaluation_window_count: int (default 5, rolling window size)
  flapping_threshold: int (default 3, number of breaches within window to confirm)
  aggregation_key: string (default "", empty = per-instance, "service" = group by service, "version" = group by version)
  recovery_enabled: bool (default true)
  enabled: bool (default true)
  created_at: timestamp
alert_event:
  id: string (uuid)
  rule_id: string
  source_id: string (agent id, gpu id, or system id)
  metric_value: float
  threshold: float
  severity: string
  state: enum [alerting, recovered, escalated]
  message: string
  aggregation_group: string (populated from aggregation_key if set)
  parent_event_id: string (null for first, links aggregated events)
  timestamp: timestamp
  acknowledged: bool (default false)
  acknowledged_by: string (null)
  ticket_ref: string (null, populated on escalation to ticket system)
Retention: alert_events older than 30 days are archived to cold storage. Rule config is never automatically deleted.
Alert Rules (canonical reference — see Config Format section for YAML schema)
| Rule ID | Metric | Field | Operator | Threshold | Severity | Cooldown |
| gpu-temp | gpu_temperature | gpu.temperature_celsius | gt | 85 | critical | 300 |
| ram-usage | ram_utilization | system.ram_percent | gt | 90 | warning | 600 |
| agent-failure | agent_failure_rate | agent.failure_rate_percent | gt | 10 | critical | 900 |
| score-drop | agent_score | agent.score_points | lt | score_baseline - 15 | warning | 1800 |
For score-drop, baseline is a rolling average of the last evaluation_window_count evaluations (default 5). Drop is calculated as rolling_average - current_score. The minimum drop to trigger is 15 points. Detection requires flapping_threshold (default 3) consecutive evaluations meeting the condition within the rolling window — this eliminates transient blips.
Monitoring and Alerting
Flapping Detection
Each rule defines flapping_threshold (integer, default 3). The engine maintains a sliding boolean buffer of length evaluation_window_count per (rule_id, source_id). On each evaluation:
1. Append current breach status (true/false) to buffer.
2. Count true entries in buffer.
3. If count >= flapping_threshold AND previous engine state was Normal: transition to Alerting.
4. If count < flapping_threshold AND previous engine state was Alerting: transition to Recovered (grace period).
5. If count == 0 AND previous engine state was Alerting and recovery_enabled: fire recovery notification.
This prevents single-spike false positives while still detecting sustained degradation quickly.
Alert Aggregation
When aggregation_key is non-empty (e.g. "service", "version"), the engine groups alert_events by that key before dispatching. Per (aggregation_group, severity): at most one aggregated event is emitted per cooldown window. The aggregated event's message includes count of contributing sources and a sample list:
"Alert: 4 agents in service 'api-gateway' exceeded 90% RAM (samples: agent-03=94%, agent-07=92%)"
Individual source-level events remain in the database for drill-down but do not trigger separate notifications.
Escalation Policy
Severity to notification channel mapping:
- info: dashboard toast only
- warning: dashboard toast + notification panel badge
- critical: dashboard toast + panel badge + auto-create ticket in tracking system
Escalation chain per event:
1. Initial alert fires per rule config.
2. If event remains unacknowledged for >= 300 seconds (configurable via escalation_seconds on rule): severity bumps one level (warning -> critical, critical -> +page).
3. At critical+page, the notification bus creates a PagerDuty/webhook event in addition to dashboard alerts.
4. Acknowledging the event resets the escalation timer but does not clear the alert.
5. Recovery notification cancels any pending escalation.
Failure Modes
Bus Backpressure Handling
The notification bus uses bounded queues (capacity 10,000 events per channel). When full:
1. New events are dropped with a log warning at most once per 60 seconds.
2. A circuit-breaker pattern protects each output channel (dashboard WS, ticket API, webhook).
3. After 5 consecutive delivery failures to a channel, that channel is marked degraded and retried with exponential backoff (1s, 2s, 4s, 8s, 16s, max 30s).
4. After 30s of consecutive failures, the channel is tripped open — no further delivery attempts until a health-check probe succeeds (polled every 60s).
5. When channel recovers, queued events are replayed oldest-first up to queue capacity.
Recovery Detection Grace Period
On first normal reading after an alerting state, the engine waits evaluation_window_count evaluations before declaring Recovered. Each intermediate evaluation must also be normal. This prevents flapping between alerting/recovered on boundary metrics (e.g. GPU bouncing between 84C and 86C). The grace period is configurable via recovery_delay_evaluations (default same as evaluation_window_count).
Malformed Config Handling
The engine validates all rules on load. Rules missing required fields (threshold, operator, metric_field) are logged and skipped. The engine continues operating on valid rules. On hot-reload, the transition is atomic: the new rule set replaces the old one only after full validation passes. If validation fails, the previous rule set remains active and an error is logged.
State Transitions
Normal -> Alerting: flapping_threshold consecutive breaches within evaluation_window_count evaluations.
Alerting -> Cooldown: notification dispatched; cooldown_seconds timer starts. During cooldown, same (rule_id, source_id) pair does not fire another notification even if metric stays breached.
Cooldown -> Alerting: cooldown expires AND metric is still breached (re-evaluated immediately on expiry).
Any State -> Recovered: evaluation_window_count consecutive normal readings AND recovery_enabled=true. Optional recovery notification dispatched.
Cooldown -> Normal: metric returns to normal during cooldown. No notification. Next evaluation starts from Normal state.
If recovery_enabled=false: engine transitions silently from Alerting/Cooldown to Normal without notification.
Configuration Format (config.yaml)
alerts:
  rules:
    - id: gpu-temp
      source_type: gpu
      metric_field: gpu.temperature_celsius
      operator: gt
      threshold: 85
      severity: critical
      cooldown_seconds: 300
      evaluation_window_count: 5
      flapping_threshold: 3
      aggregation_key: ""
      recovery_enabled: true
      enabled: true
      escalation_seconds: 300
    - id: score-drop
      source_type: agent
      metric_field: agent.score_points
      operator: lt
      threshold_mode: dynamic_drop
      drop_baseline_window: 5
      drop_minimum: 15
      severity: warning
      cooldown_seconds: 1800
      evaluation_window_count: 5
      flapping_threshold: 3
      aggregation_key: "service"
      recovery_enabled: true
      enabled: true
      escalation_seconds: 0
global:
  max_alerts_per_agent_per_hour: 10
  notification_bus_queue_capacity: 10000
  channel_circuit_breaker_threshold: 5
  channel_circuit_breaker_backoff_max_seconds: 30
  event_retention_days: 30
Integration Points
Telemetry ingestion: accepts structured JSON over HTTP POST at /api/v1/telemetry. Expected fields: source_id, source_type, timestamp, metrics (map of field_name -> value).
Dashboard push: real-time WebSocket connection to Forge Dashboard at /ws/alerts. Events serialized as JSON with fields: id, rule_id, severity, state, message, timestamp, aggregation_group, source_count (when aggregated).
Ticket system webhook: configured via environment variable ALERT_TICKET_WEBHOOK_URL. Payload: JSON POST with event details, link back to dashboard drill-down view.