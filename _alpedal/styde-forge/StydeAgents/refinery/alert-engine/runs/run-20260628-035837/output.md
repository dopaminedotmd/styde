Alert Engine Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard.
Architecture
Telemetry Sources (Agent, GPU, RAM) -> Alert Evaluator (Rule Engine: Thresholds, Cooldowns, Severities, Escalation) -> Notification Bus (Push Dispatcher, Backpressure Circuit Breaker) -> Dashboard UI
Alert Rules
Rule ID       | Metric              | Mode               | Threshold         | Severity | Cooldown | EvaluationWindow | EscalationSeconds
------------- | ------------------- | ------------------ | ----------------- | -------- | -------- | ---------------- | -----------------
gpu-temp      | GPU Temperature     | static             | > 85 C            | critical | 5 min    | 1                | N/A
ram-usage     | RAM Utilization     | static             | > 90 %            | warning  | 10 min   | 1                | 120
agent-failure | Agent Failure Rate  | static             | > 10 %            | critical | 15 min   | 1                | N/A
score-drop    | Agent Score Drop    | dynamicdrop        | thresholdstatic=15, thresholddynamicdrop=0.15 | warning | 30 min   | evaluationwindowcount=5 | 60
Flow
1. Telemetry sources publish metrics at regular intervals (configurable, default 30s).
2. The Alert Evaluator checks every metric against all active rules. For rolling-window rules (evaluationwindowcount > 1), the metric is compared against the average of the last N evaluations.
3. On breach: a notification event is created, respecting per-rule cooldown. Each severity level has its own cooldown timer; escalating from warning to critical does not reset the warning cooldown unless escalationseconds=0.
4. The Notification Bus dispatches a push notification to the dashboard via a bounded-size queue, applying a circuit breaker if bus backpressure exceeds the configured threshold.
5. The user sees the alert in the dashboard notification panel.
6. On recovery (metric returns to normal for evaluationwindowcount consecutive evaluations), an optional recovery notification is sent.
States
- Normal: all metrics within bounds.
- Alerting: threshold breached; notification sent.
- Cooldown: alert fired recently; suppressed until cooldown expires.
- Recovered: metric returned to normal; optional recovery notification.
- Flapping: metric oscillates between Normal and Alerting faster than the flapping suppression interval. The engine suppresses further notifications until the metric stabilises in one state for evaluationwindowcount consecutive evaluations.
- Downtime: a telemetry source stops reporting for longer than the recovery-grace-period. The engine does not fire alert recovery until the source resumes and produces evaluationwindowcount consecutive healthy readings.
Configuration Data Model
All rules are defined in config.yaml. The engine reloads config on startup and can be hot-reloaded via a dashboard admin action.
Fields per rule:
- id: string, required. Unique rule identifier.
- metric: string, required. Name of the telemetry metric to evaluate.
- mode: enum[static, dynamicdrop], required. static uses thresholdstatic; dynamicdrop compares the current value to a rolling baseline and triggers if the drop exceeds thresholddynamicdrop.
- thresholdstatic: float, required when mode=static. The absolute threshold value (e.g. 85 for GPU temp, 90 for RAM usage). Ignored when mode=dynamicdrop.
- thresholddynamicdrop: float, required when mode=dynamicdrop. Fractional drop threshold (0.0-1.0) representing the minimum relative decline from baseline to trigger. Example: 0.15 means a 15% drop from the rolling average. Ignored when mode=static.
- severity: enum[warning, critical], required.
- cooldownseconds: int, required. Minimum seconds between consecutive alerts for this rule.
- evaluationwindowcount: int, default 1. Number of recent evaluations to include in the rolling window. A value of 1 means instantaneous evaluation (single sample). A value greater than 1 means the metric must breach the threshold for that many consecutive evaluations before an alert fires, AND must return to normal for that many consecutive evaluations before declaring recovery.
- escalationseconds: int, default 0. Seconds after a warning-level alert before it auto-escalates to critical. 0 means instant escalation (every warning immediately becomes critical). When non-zero, must be >= 60 to avoid rapid cycling between warning and critical states.
- flappingsuppressionseconds: int, default 120. If the same metric-agent pair toggles between Alerting and Normal more than once within this window, further notifications are suppressed until the metric holds a consistent state for evaluationwindowcount consecutive evaluations.
- recoverygraceperiodseconds: int, default 300. Seconds of missing telemetry before the engine treats the source as down. No recovery notification is fired during a downtime gap; the engine waits until the source resumes and produces evaluationwindowcount consecutive healthy readings.
Failure Modes
Bus Backpressure: The notification bus uses a bounded queue (capacity configurable, default 1000). If the queue exceeds 80 % capacity, the dispatcher enters backpressure mode and drops lower-severity (warning) alerts, logging each drop. If the queue reaches 100 % capacity, the circuit breaker opens: all outbound dispatch is blocked, the engine logs CRITICAL: Notification bus circuit breaker OPEN, and the operator must acknowledge or restart to reset.
Recovery Detection: When a telemetry source stops reporting, the engine starts a downtime timer. No evaluation occurs for that agent-metric during the gap. Once the recoverygraceperiodseconds expires, the engine marks the source as Down. When telemetry resumes, the engine waits for evaluationwindowcount consecutive normal readings before declaring Recovered. This prevents flapping-recovery noise during brief network blips.
Escalation Cycle Prevention: A warning-level rule with escalationseconds=0 escalates every breach to critical instantly. This is valid but creates a potential cycle: if the critical threshold is also breached, the rule re-fires immediately after cooldown. To mitigate, rules with severity=warning and escalationseconds=0 MUST also set evaluationwindowcount >= 3 to require sustained deviation before escalating. Rules with escalationseconds >= 60 have no such constraint.
Flapping Unification (Single Source of Truth): Flapping recovery uses the same evaluationwindowcount as initial alert detection. The Recovery Grace Period section above is the sole authority for all recovery logic. Step 4 of the Flow section references this section rather than duplicating recovery rules. Any implementation must read evaluationwindowcount from the rule config and apply it identically for detection and recovery.