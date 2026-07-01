BLUEPRINT:
Alert Engine — Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification with a dispatch confirmation.
Architecture
Telemetry Sources → Alert Evaluator → Notification Bus → Dispatch Confirmations
Telemetry Sources: Agent, GPU, RAM metrics published at regular intervals.
Alert Evaluator: Rule engine applying thresholds, cooldowns, and severities.
Notification Bus: Push Dispatcher sending to dashboard + configured destinations.
Dispatch Confirmations: Records delivery status per alert for audit trail.
Alert Rules
Rule ID       Metric                 Threshold       Severity   Cooldown
gpu-temp      GPU Temperature        > 85 C          critical   5 min
ram-usage     RAM Utilization        > 90 %          warning    10 min
agent-failure Agent Failure Rate     > 10 %          critical   15 min
score-drop    Agent Score Drop       > 15 points     warning    30 min
stale-source  Metric Source Age      > 300 seconds   warning    5 min
Flow
1. Telemetry sources publish metrics at regular intervals.
2. Alert Evaluator checks every metric against all active rules.
3. On breach: evaluator checks cooldown and deduplication state first.
4. If allowed: a notification event is created with severity, rule ID, and metric value.
5. Dispatcher sends notification to dashboard UI and configured destinations.
6. Dispatcher records confirmation — destination, status, timestamp.
7. User sees alert in dashboard notification panel with delivery metadata.
States
Normal     — all metrics within bounds. No notification.
Alerting   — threshold breached. Notification dispatched and confirmed.
Cooldown   — alert fired recently. Suppressed until cooldown expires.
Recovered  — metric returned to normal. Optional recovery notification sent.
Degraded   — telemetry source silent beyond stale-source threshold.
Dispatches
After each dispatch, the engine records a confirmation entry:
- destination: email / slack / webhook / dashboard-ui
- status: sent / queued / failed
- timestamp: ISO-8601
- next-step: human-actionable instruction
Example dispatch record:
  rule: gpu-temp
  metric: 92 C
  severity: critical
  destination: slack
  status: sent
  timestamp: 2026-06-28T05:50:00Z
  next-step: Check cooling on worker-03 or throttle batch jobs
Variant notes for dispatch formats:
- Slack: uses webhook URL from config. Payload includes severity emoji, rule ID, metric value, and next-step.
- Email: uses SMTP relay from config. Body includes full dispatch record table.
- Webhook: raw JSON POST to configured endpoint. Payload includes all dispatch record fields plus agent metadata.
- Dashboard UI: in-app notification via WebSocket. No external dependency.
Edge Cases
- Stale telemetry: If a metric source has not published within stale-source threshold (default 300s), evaluator skips evaluation and logs a source-degraded event. Recovery notification fires when source resumes publishing.
- Null-payload flapping: Metrics arriving with null values are discarded silently. A consecutive null-count counter per source is maintained; if it exceeds 5, the source is marked degraded.
- Deduplication on identical alerts from different shards: Evaluator compares (rule_id, agent_id, metric_hash) across a 60-second dedup window. Duplicates within window are suppressed; only the first instance triggers dispatch.
- Cooldown edge case on restart: Cooldown state is persisted to disk (cooldown_state.yaml) and restored on engine restart so cooldowns survive a crash.
- Rate limit per agent: Max 10 alerts per agent per hour. Exceeded alerts are queued and dispatched when the window resets.
Configuration (config.yaml)
alert_engine:
  token_budget_cap: 1500
  max_example_count: 2
  rules:
    - id: gpu-temp
      metric: gpu_temperature
      threshold: 85
      operator: gt
      severity: critical
      cooldown_minutes: 5
    - id: ram-usage
      metric: ram_utilization
      threshold: 90
      operator: gt
      severity: warning
      cooldown_minutes: 10
    - id: agent-failure
      metric: agent_failure_rate
      threshold: 10
      operator: gt
      severity: critical
      cooldown_minutes: 15
    - id: score-drop
      metric: agent_score
      threshold: 15
      operator: drop_gt
      severity: warning
      cooldown_minutes: 30
    - id: stale-source
      metric: metric_source_age
      threshold: 300
      operator: gt
      severity: warning
      cooldown_minutes: 5
  rate_limit:
    max_alerts_per_agent_per_hour: 10
    dedup_window_seconds: 60
  dispatch:
    max_retries: 3
    retry_delay_seconds: 30
    destinations:
      - dashboard-ui
      - slack
      - email
      - webhook
  edge:
    stale_source_threshold_seconds: 300
    null_payload_max_consecutive: 5
    persist_cooldowns: true
    cooldown_state_file: cooldown_state.yaml