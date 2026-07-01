BLUEPRINT: Alert Engine
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached. Every alert dispatch includes a delivery confirmation visible to the user.
Overview
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification. After dispatch, it emits a structured confirmation showing destination, delivery status, and the next action the user should take.
Architecture
Telemetry Sources (Agent / GPU / RAM)
  |  metrics stream
  v
Alert Evaluator
  - Rule Engine: thresholds, cooldowns, severities
  - Cooldown Manager: per-rule-agent cooldown tracker
  - Dispatch Tracker: per-alert delivery log
  |  trigger
  v
Notification Bus
  - Push Dispatcher: delivers to dashboard UI
  - Dispatch Logger: records destination, status, timestamp
  - Output Formatter: builds the Dispatches section in the output
Alert Rules
Rule ID            Metric              Threshold     Severity  Cooldown
gpu-temp           GPU Temperature     > 85 C        critical   5 min
ram-usage          RAM Utilization     > 90 %        warning    10 min
agent-failure      Agent Failure Rate  > 10 %        critical   15 min
score-drop         Agent Score Drop    > 15 points   warning    30 min
Flow
1. Telemetry sources publish metrics at regular intervals.
2. The Alert Evaluator checks every metric against all active rules.
3. On breach:
   a. Cooldown check: skip if same metric-agent pair fired within cooldown window.
   b. Create notification event with rule ID, metric value, severity, timestamp.
   c. Dispatcher sends push notification to dashboard.
4. Dispatch confirmation is emitted immediately after sending:
   - destination (e.g. dashboard-ui, slack-webhook, email-gateway)
   - delivery status (sent / queued / failed)
   - human-actionable next-step instruction per alert
5. The Dispatches section is appended to the engine output, listing every alert's action taken, timestamp, and result.
6. On recovery: optional recovery notification, confirmed the same way.
States
  Normal     - all metrics within bounds. Silence is healthy.
  Alerting   - threshold breached; dispatch confirmed with result.
  Cooldown   - alert fired recently; suppressed silently until cooldown expires.
  Recovered  - metric returned to normal; optional confirmed recovery notification.
Dispatch Confirmation Format (agent output)
When an alert fires, the engine prints:
Dispatching [rule-id] for <agent-name>
After that line, the agent MUST emit a concrete dispatch confirmation block:
Dispatch: {
  rule: gpu-temp
  agent: worker-03
  destination: dashboard-ui
  status: sent
  timestamp: 2026-06-28T05:45:00Z
  next_step: "Inspect GPU cooling on worker-03. Check fan speed and thermal paste. Escalate if temp exceeds 95 C for 2 consecutive readings."
}
The 'next_step' field is mandatory and must be specific to the alert type and agent — not a generic message.
Output Template (Dispatches section)
The Dispatches section mirrors the existing engine-state structure and is appended to every engine output cycle:
Dispatches:
  - alert: gpu-temp
    agent: worker-03
    action: push-notify
    destination: dashboard-ui
    status: sent
    timestamp: 2026-06-28T05:45:00Z
    next_step: Inspect GPU cooling on worker-03.
  - alert: ram-usage
    agent: worker-07
    action: push-notify
    destination: dashboard-ui
    status: sent
    timestamp: 2026-06-28T05:46:00Z
    next_step: Identify processes consuming > 90% RAM on worker-07. Kill or migrate non-critical workloads.
When status is 'failed', the next_step must include the fallback channel and retry instruction:
  - alert: agent-failure
    agent: worker-12
    action: push-notify
    destination: dashboard-ui
    status: failed
    fallback: slack-webhook
    fallback_status: queued
    timestamp: 2026-06-28T05:47:00Z
    next_step: Dashboard delivery failed. Check slack-webhook for queued notification. If both channels fail, SSH into worker-12 directly.
When status is 'queued', the next_step must include expected delivery eta:
  - alert: score-drop
    agent: worker-04
    action: push-notify
    destination: email-gateway
    status: queued
    eta: 30s
    timestamp: 2026-06-28T05:48:00Z
    next_step: Notification queued for email delivery (eta 30s). Check email inbox. No action needed if delivery succeeds within eta.
Configuration
All rules are defined in config.yaml. The engine reloads config on startup and supports hot-reload via a dashboard admin action.
Each rule in config.yaml includes an optional 'next_step' template that the engine fills with the agent name and current metric value. If not provided, the engine uses a default template based on the metric type.
Self-Preservation Constraints
- Never alert on the same metric-agent pair more than once per cooldown window.
- Do not evaluate config that is malformed or missing required fields — log and skip.
- Respect global rate limit of 10 alerts per agent per hour.
- Log dispatch failures internally; never crash on bad config or network error.
- Accuracy over speed — prefer a true positive over a rushed evaluation.