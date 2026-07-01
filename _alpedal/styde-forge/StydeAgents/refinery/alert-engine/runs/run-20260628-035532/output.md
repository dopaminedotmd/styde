Alert Engine — Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Identity
Title: Alert Engine
Role: Forge Dashboard Monitoring Subsystem
Domain: Infrastructure monitoring, threshold evaluation, notification dispatch
Voice: Direct, concise, actionable. Uses metric values and agent names.
Recovery: Calm, confirms resolution.
Internal: Technical, precise, timestamped.
Constraints
  Never alert on same metric-agent pair more than once per cooldown window.
  Do not evaluate malformed or missing config — log and skip.
  Rate limit: 10 alerts per agent per hour.
Decision Principles
  Accuracy over speed.
  Silence is healthy — no news means metrics within bounds.
  Self-preservation — log errors internally, never crash on bad input.
Architecture
Telemetry Sources (Agent, GPU, RAM, Score)
  | publish metrics
  v
Alert Evaluator
  | Rule Engine (Thresholds, Cooldowns, Severities)
  | trigger
  v
Notification Bus
  | Push Dispatcher -> Dashboard UI
  v
Dashboard Notification Panel
Alert Rules
Rule ID        Metric                 Threshold        Severity  Cooldown
gpu-temp       GPU Temperature        > 85 C           critical  5 min
ram-usage      RAM Utilization        > 90 %           warning   10 min
agent-failure  Agent Failure Rate     > 10 %           critical  15 min
score-drop     Agent Score Drop       > 15 points      warning   30 min
Flow
  Telemetry sources publish metrics at intervals.
  Alert Evaluator checks each metric against all active rules.
  On breach: notification event created if cooldown has expired.
  Notification Bus dispatches push to dashboard.
  User sees alert in notification panel.
States
  Normal       — all metrics within bounds
  Alerting     — threshold breached, notification sent
  Cooldown     — alert fired recently, suppressed until cooldown expires
  Recovered    — metric returned to normal, optional recovery notification
Configuration
All rules defined in config.yaml. Engine reloads config on startup; hot-reload via dashboard admin action.
Data Model and Storage
Alert Rule Schema
Field          Type     Description
rule_id        string   Unique identifier, e.g. gpu-temp
metric         string   Telemetry metric name
source         string   Source type: agent | gpu | system
operator       string   Comparison: gt | gte | lt | lte | eq | neq
threshold      float    Threshold value
severity       string   critical | warning | info
cooldown_sec   int      Suppression window in seconds
rate_limit     int      Max alerts per hour per agent
enabled        bool     Rule active or disabled
created_at     datetime Rule creation timestamp
updated_at     datetime Last modification timestamp
Alert Instance Schema
Field          Type     Description
alert_id       string   Unique alert instance id (uuid)
rule_id        string   Source rule
agent_id       string   Agent that triggered the alert
metric_value   float    Value that breached the threshold
severity       string   Inherited from rule
state          string   normal | alerting | cooldown | recovered
fired_at       datetime First breach timestamp
cooldown_until datetime When next alert allowed for this pair
resolved_at    datetime Nullable, set on recovery
notified       bool     Whether push was dispatched
Storage Backend
  Primary store: SQLite (single-node) / PostgreSQL (multi-node).
  Time-series data (raw telemetry): kept in-memory ring buffer for evaluation, not persisted beyond recent window. Historical alert instances retained in relational store for dashboard audit view.
Migrations
  Schema versioned via Alembic (if PostgreSQL) or embedded SQL migration file executed at engine startup (if SQLite). Migration path: v001_initial -> v002_add_operator_field -> v003_add_rate_limit.
Authentication and Authorization
Operations requiring auth
  Operation            Auth required  Scope
  List alerts          Yes            alerts:read
  Create/update rule   Yes            alerts:write
  Delete rule          Yes            alerts:admin
  Acknowledge alert    Yes            alerts:write
  Trigger hot-reload   Yes            admin:config
Auth mechanism
  API key in header X-API-Key or Bearer JWT. JWT payload includes sub (agent/user id), scopes array, and exp. API keys mapped to scopes in operator config.
RBAC scopes
  alerts:read   — view alert rules and active alert instances
  alerts:write  — create/edit rules, acknowledge alerts
  alerts:admin  — delete rules, manage cooldowns
  admin:config  — hot-reload, modify global rate limits
Alert ownership and visibility
  Alert instances tagged with agent_id. Agents can only read alerts tagged to them. Operators (human users) with alerts:read scope can view alerts across all agents. No cross-agent visibility for unprivileged API keys.