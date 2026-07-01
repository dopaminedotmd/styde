Alert Engine — Blueprint (Revised)
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard.
Architecture
  Telemetry Sources (Agent, GPU, RAM)
       |      |     |
       v      v     v
  Alert Evaluator
    Rule Engine
      Thresholds
      Cooldowns
      Severities
       |
       | trigger
       v
  Notification Bus
    Push Dispatcher -> Dashboard UI
Alert Rules
  Rule ID         | Metric              | Threshold    | Severity | Cooldown
  gpu-temp        | GPU Temperature     | > 85 C       | critical | 5 min
  ram-usage       | RAM Utilization     | > 90 %       | warning  | 10 min
  agent-failure   | Agent Failure Rate  | > 10 %       | critical | 15 min
  score-drop      | Agent Score Drop    | > 15 points  | warning  | 30 min
Flow
  1. Telemetry sources publish metrics at regular intervals.
  2. Alert Evaluator checks every metric against all active rules.
  3. On breach: notification event created, respecting per-rule cooldown.
  4. Notification Bus dispatches push notification to the dashboard.
  5. User sees alert in dashboard notification panel.
  6. On recovery: optional recovery notification sent after metric normalizes.
Dispatch Format
  Canonical notification payload:
    severity: critical | warning | info
    rule_id: string
    agent_id: string
    metric: string
    value: number
    threshold: string
    timestamp: ISO8601
    message: string
  Variant table:
    alert     | includes value, threshold, timestamp | always sent
    recovery  | includes recovery timestamp, duration | optional, configurable
    suppression| includes suppressed_until, reason     | internal, not pushed
Operators Table
  Operator | Logic                        | Example
  gt       | value > threshold            | gpu_temp > 85
  gte      | value >= threshold           | ram_usage >= 90
  lt       | value < threshold            | score < 10
  lte      | value <= threshold           | failure_rate <= 5
  eq       | value == threshold           | status == offline
  neq      | value != threshold           | agent != active
  dropgt   | value drops below threshold  | cpu_temp dropgt 40
  rate     | rate of change > threshold   | error_rate rate 5
States
  Normal     | all metrics within bounds
  Alerting   | threshold breached, notification sent
  Cooldown   | alert fired recently, suppressed until cooldown expires
  Recovered  | metric returned to normal, optional recovery notification
Configuration (config.yaml)
  alert_engine:
    rate_limit:
      alerts_per_agent_per_hour: 10
      alerts_per_rule_per_minute: 5
    alert_budget:
      budget_per_second: 50
      burst_limit: 100
    max_alerts_per_rule: 100
    evaluation_interval_seconds: 15
    rules:
      - id: gpu-temp
        metric: gpu.temperature
        threshold:
          operator: gt
          value: 85
        severity: critical
        cooldown_seconds: 300
        recovery_notification: true
      - id: ram-usage
        metric: system.ram.percent
        threshold:
          operator: gt
          value: 90
        severity: warning
        cooldown_seconds: 600
        recovery_notification: false
    recovery:
      cooldown_seconds: 300
      renotify_window_seconds: 3600
      escalation:
        - after_minutes: 10
          severity: warning -> critical
        - after_minutes: 30
          notify_extra_channel: pager
Edge Cases: Silent Metric Sources
  Stale Telemetry
    Metric timestamp older than 2x evaluation_interval_seconds is flagged as stale.
    Evaluator logs warning and skips evaluation for that metric-agent pair.
    If 3 consecutive stale readings: evaluator emits a staleness alert (severity=warning, rule_id=stale-telemetry).
  Null-Payload Flapping
    Agent sends metrics with null values intermittently.
    Evaluator counts nulls per agent per 5-minute window.
    If null ratio > 0.2 in window: agent is marked flapping, alerts suppressed entirely for that agent for 10 minutes.
    Flapping state is published as a system notification.
  Deduplication on Identical Alerts from Different Shards
    Two shards report the same metric+value+timestamp within 1-second window.
    Dedup key: hash(metric + value + round(timestamp, 1s)).
    Only first notification dispatched; duplicates are counted (dedup_counter) in alerts_dropped metric.
    Dedup counter resets per evaluation window.
  Missing Metric
    Expected metric absent for >= 3 evaluation cycles: evaluator emits a missing-data alert.
    severity: info, message: "Metric {metric} missing from agent {agent_id} for {seconds}s".
Rule CRUD API
  All operations require admin authentication.
  POST   /api/v1/rules           body: RuleConfig    response: {id, status}
  GET    /api/v1/rules           query: ?agent=id    response: [RuleConfig]
  GET    /api/v1/rules/{id}      params: id          response: RuleConfig
  PUT    /api/v1/rules/{id}      body: RuleConfig    response: {id, status}
  DELETE /api/v1/rules/{id}      params: id          response: {deleted}
  PATCH  /api/v1/rules/{id}/activate   body: {active: bool}
  Rate-limited to 10 mutations per minute per admin user.