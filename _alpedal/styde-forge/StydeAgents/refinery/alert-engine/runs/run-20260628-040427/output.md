Alert Engine — Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Architecture
Telemetry Sources (Agent / GPU / RAM) → Alert Evaluator (Rule Engine: thresholds, cooldowns, severities) → Notification Bus (Push Dispatcher → Dashboard UI)
Alert Rules
gpu-temp     GPU Temperature     > 85 C    critical   5 min
ram-usage    RAM Utilization     > 90 %    warning   10 min
agent-failure Agent Failure Rate > 10 %   critical  15 min
score-drop   Agent Score Drop    > 15 pts  warning   30 min
Flow
Telemetry sources publish metrics at regular intervals. The Alert Evaluator checks every metric against all active rules. On breach: a notification event is created, respecting per-rule cooldown and suppression state. The Notification Bus dispatches a push notification to the dashboard. The user sees the alert in the dashboard notification panel.
States
Normal — all metrics within bounds. No notifications sent. Silence is healthy.
Alerting — threshold breached. Notification created and dispatched. Cooldown timer starts for this rule-agent pair.
Cooldown — alert fired recently. Duplicate notifications suppressed until cooldown expires. Timer is per (rule_id, agent_id) key.
Recovered — metric returned to normal range after an alerting state. Optional recovery notification sent. Cooldown state is cleared on recovery.
Flapping — metric oscillates across threshold within a detection window. Auto-escalation logic takes over: each alternation increments a flapping counter. At N alternations within M seconds, severity escalates one tier (warning → critical). Recovery is gated: a metric must remain in normal range for a configurable hold-down period (default 2x cooldown) before exiting the flapping state. This prevents repeated alert-recovery cycles from generating notification noise.
Data Model
AlertRule:
  id: string
  metric: string
  severity: string [warning, critical]
  cooldown_seconds: int
  threshold_mode: string [static, dynamicdrop]
  threshold_static: float | null  # used ONLY when threshold_mode = static
  threshold_dynamicdrop:         # used ONLY when threshold_mode = dynamicdrop
    baseline_window_seconds: int
    deviation_factor: float
  escalation:
    enabled: boolean
    auto_tier: string [none, single, multi]
    auto_tier_count: int | null  # max auto-escalation tiers; if null, unlimited
  flapping:
    enabled: boolean
    max_alternations: int        # default 3
    detection_window_seconds: int # default 60
    holddown_seconds: int | null # if null = 2x cooldown_seconds
  recovery_notification: boolean # default false
  suppression:
    start_hour: int | null       # 24h format, UTC
    end_hour: int | null
Cooldown Reset Matrix
Each entry shows whether the cooldown timer resets when a new alert arrives at a different severity while the previous severity is still in cooldown.
previous \ current | warning (new) | critical (new)
warning                      no reset        reset to critical cooldown
critical                     no reset        no reset (already in critical cooldown)
Cooldown duration always uses the current alert's severity. When a warning alert is in cooldown (10 min) and a critical alert arrives for the same rule-agent pair, the cooldown resets to the critical duration (5 min) and the new critical notification IS dispatched. When a critical alert is in cooldown (5 min) and a warning arrives, the cooldown is NOT reset—the warning is suppressed until the critical cooldown expires. Same-severity arrivals during cooldown are always suppressed.
Cost implication: resetting cooldown from warning to critical costs one additional notification dispatch. The prior warning's remaining cooldown time is lost. Notification rate-limit counters are decremented per dispatch.
Example timers:
  t=0  warning alert → cooldown = 600s, notification sent
  t=30 critical alert → cooldown resets to 300s, critical notification sent. Warning's remaining 570s is discarded.
  t=60 warning alert → suppressed (critical cooldown has 270s remaining, no reset on warning→current)
  t=330 cooldown expires. t=335 critical alert → cooldown = 300s, notification sent.
Escalation Configuration
Auto-ticketing tier behavior: when auto_tier = single or multi, each escalation fires a new notification at the escalated severity. If a warning always escalates to critical (e.g. auto_tier_count = 1 and severity = warning), the warning-level notification is sent once, and the escalated critical notification is sent immediately after. The escalation does NOT loop—auto_tier_count caps the maximum number of escalation steps. To prevent infinite loops, auto_tier_count must be >= 1 when auto_tier is enabled. A warning with auto_tier = single and auto_tier_count = 1 produces exactly two notifications: one warning, one critical. No further criticals are fired for that alert unless a new metric evaluation triggers it fresh.
Race Conditions and Concurrency
Cooldown reset atomicity
Two alerts for the same rule-agent pair arriving in the same evaluation tick are processed sequentially under a per-rule-agent mutex. The mutex serializes: read current cooldown state → evaluate severity → write new cooldown state. Without atomicity, two concurrent checks could both see cooldown == expired and both dispatch, violating the single-notification-per-cooldown guarantee.
Implementation: per-rule-agent lock stored in a concurrent dictionary keyed by (rule_id, agent_id). Lock acquisition uses try_lock with a 10ms spin-retry, then fail-open (log and skip) to avoid deadlock on a stuck goroutine.
Hot-reload thread-safety
Config reload (triggered via dashboard admin action) replaces the active rule set atomically using a pointer swap. During swap:
  - The old rule set reference is retained until all in-flight evaluations against it complete.
  - A generation counter on the rule set allows evaluators to detect staleness and re-acquire the new set.
  - Cooldown state (which is keyed by rule_id) survives reload: if a rule with the same id exists in the new config, its cooldown timers are preserved. Rules removed from config have their cooldown state garbage-collected after the max cooldown window passes.
Locking strategy: per-rule-agent mutex described above, NOT a global lock. A global lock would serialize all evaluations and become a bottleneck at 100+ agents each publishing 3+ metrics per tick. Per-rule-agent mutexes are O(1) per evaluation and scale linearly with agent count.
Configuration
Rules defined in config.yaml (see config.example.yaml for full reference). Engine reloads config on startup and on SIGHUP or dashboard admin reload action.
JSON Alert Payload Examples
Minimal:
{"alert_id":"a-001","rule":"gpu-temp","agent":"worker-03","severity":"critical","metric_value":92,"threshold":85,"timestamp":"2026-06-28T06:10:00Z"}
Typical:
{"alert_id":"a-001","rule":"gpu-temp","agent":"worker-03","severity":"critical","metric_value":92,"threshold":85,"unit":"celsius","timestamp":"2026-06-28T06:10:00Z","cooldown_remaining":240,"notification_count":1}
With enrichment:
{"alert_id":"a-001","rule":"gpu-temp","agent":"worker-03","agent_group":"inference-cluster-a","severity":"critical","metric_value":92,"threshold":85,"unit":"celsius","previous_value":78,"trend":"rising","timestamp":"2026-06-28T06:10:00Z","cooldown_remaining":240,"notification_count":1,"enrichment":{"gpu_index":2,"process_name":"llama-inference","host":"node-07.az-eastus"}}
Dashboard Integration
The Notification Bus pushes to the Forge Dashboard via two paths:
  WebSocket — real-time stream on /ws/alerts. Payload schema matches the typical JSON above. Dashboard subscribes on login, auto-reconnects with exponential backoff (1s, 2s, 4s, max 30s). Refresh cadence: push-based, no polling.
  REST API — GET /api/v1/alerts returns paginated alert history. Query parameters: ?agent=worker-03&severity=critical&since=2026-06-28T00:00:00Z&limit=50. Used for initial page load and historical search. Cache TTL on dashboard side: 10s for active alerts, 60s for history.