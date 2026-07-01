ALERT ENGINE - BLUEPRINT
Version 14.0.0
Domain: monitoring
PURPOSE
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
OVERVIEW
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard. The engine supports multi-channel routing (dashboard push, Slack webhook, email, PagerDuty), cooldown-based suppression, rate limiting, recovery notifications, hot-reload of configuration, and persistent alert history with a queryable API.
ARCHITECTURE
Components:
[Telemetry Sources]
  Agent metrics (gRPC streaming)
  GPU metrics (Prometheus scrape)
  System metrics (OTLP exporter)
  -> each publishes on configurable interval (default 60s)
[Ingestion Layer]
  OTLP receiver (gRPC port 4317, HTTP port 4318)
  Prometheus pull endpoint (:9090/metrics)
  Agent gRPC stream handler
  -> validates, normalizes, enriches with agent_id + hostname
[Alert Evaluator]
  Rule Engine (threshold match, severity assignment)
  Cooldown Manager (per-rule per-agent-agent_id sorted set)
  Rate Limiter (rolling window, 10/agent/hour)
  Dedup Aggregator (same-metric same-agent within 60s window)
  -> produces AlertEvent on breach
[Persistence Layer]
  SQLite alert history store with TTL-based compaction
  In-memory cooldown state with periodic snapshot to disk
  Config cache with versioned snapshots for rollback
[Notification Dispatcher]
  Dashboard push (WebSocket to Forge UI)
  Slack webhook (HMAC-signed POST)
  Email (SMTP with TLS)
  PagerDuty (Events API v2)
  -> routing policy: severity -> channel(s)
[Self-Observability]
  /metrics Prometheus endpoint (engine health)
  /health liveness probe
  /alerts query API
ALERT RULES
Rule ID        Metric                    Threshold     Severity  Cooldown  Enabled
gpu-temp       GPU Temperature           > 85 C        critical  5 min     true
ram-usage      RAM Utilization           > 90 %        warning   10 min    true
agent-failure  Agent Failure Rate        > 10 %        critical  15 min    true
score-drop     Agent Score Drop          > 15 points   warning   30 min    true
Each rule defined in config.yaml with:
  id, name, description, metric (dot-notation), condition (operator + value),
  severity (critical/warning/info), cooldown_minutes, enabled, message_template
config.yaml global settings:
  evaluation_interval_seconds: 60
  default_cooldown_minutes: 10
  recovery_notifications: true
  max_alerts_per_agent_per_hour: 10
FLOW
1. Telemetry sources publish metrics at configurable intervals (default 60s).
2. Ingestion layer receives via OTLP gRPC, Prometheus scrape, or agent gRPC stream.
3. Alert Evaluator checks each metric against all active rules in priority order.
4. On threshold breach: create AlertEvent, check cooldown per rule+agent_id pair.
5. If cooldown expired and under rate limit: enqueue for dispatch, update cooldown, increment rate counter.
6. Notification Dispatcher selects channels per routing policy and delivers.
7. AlertEvent appended to SQLite alert_history table.
8. On metric return to normal: if recovery_notifications enabled, enqueue recovery AlertEvent.
9. User sees alert in dashboard notification panel in real time.
STATES
Normal - all metrics within bounds. No alert generated.
Alerting - threshold breached; notification dispatched.
Cooldown - alert fired recently for this rule+agent_id pair; suppressed until cooldown expires.
Recovered - metric returned to normal; optional recovery notification sent if recovery_notifications=true.
TELEMETRY AND OBSERVABILITY
Protocol: OpenTelemetry Protocol (OTLP) via gRPC
OTLP Metrics payload (canonical fields relevant to alert engine):
  resource_metrics:
    resource:
      attributes:
        - key: service.name
          value: <agent_name>
        - key: service.instance.id
          value: <agent_id>
        - key: host.name
          value: <hostname>
    scope_metrics:
      metrics:
        - name: gpu.temperature_celsius
          type: Gauge
          unit: Cel
          gauge:
            data_points:
              - as_double: <float>
                time_unix_nano: <int>
                attributes:
                  - key: gpu_id
                    value: <string>
        - name: system.ram_percent
          type: Gauge
          unit: "%"
          gauge:
            data_points:
              - as_double: <float>
        - name: agent.failure_rate_percent
          type: Gauge
          unit: "%"
          gauge:
            data_points:
              - as_double: <float>
        - name: agent.score
          type: Gauge
          unit: "1"
          gauge:
            data_points:
              - as_double: <float>
Self-metrics endpoint (Prometheus format):
  # HELP alert_evaluator_rules_total Total rules evaluated
  # TYPE alert_evaluator_rules_total counter
  alert_evaluator_rules_total{agent_id="<id>",rule="<id>"} <int>
  # HELP alert_evaluator_alerts_total Total alerts fired
  # TYPE alert_evaluator_alerts_total counter
  alert_evaluator_alerts_total{agent_id="<id>",severity="<critical|warning|info>"} <int>
  # HELP alert_evaluator_rate_limit_exceeded_total Rate limit hits
  # TYPE alert_evaluator_rate_limit_exceeded_total counter
  alert_evaluator_rate_limit_exceeded_total{agent_id="<id>"} <int>
  # HELP alert_evaluator_cooldown_active Currently suppressed alerts
  # TYPE alert_evaluator_cooldown_active gauge
  alert_evaluator_cooldown_active{agent_id="<id>"} <int>
  # HELP alert_engine_uptime_seconds Seconds since engine start
  # TYPE alert_engine_uptime_seconds gauge
  alert_engine_uptime_seconds <float>
Prometheus scrape target config for engine self-metrics:
  - job_name: alert-engine
    scrape_interval: 30s
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    static_configs:
      - targets:
          - localhost:9091
NOTIFICATION DISPATCHING AND ROUTING
Routing policy table:
  Severity     Channels
  critical     dashboard push, Slack #alerts-critical, PagerDuty, email (on-call)
  warning      dashboard push, Slack #alerts-warnings
  info         dashboard push only (silent badge)
Webhook contract (Slack-compatible POST):
  Endpoint: <webhook_url>
  Method: POST
  Headers:
    Content-Type: application/json
    X-Alert-Signature: HMAC-SHA256(<payload>, <shared_secret>)
  Body schema (JSON):
    {
      "alert_id": "uuid",
      "rule_id": "gpu-temp",
      "agent_id": "worker-03",
      "severity": "critical",
      "metric_name": "gpu.temperature_celsius",
      "metric_value": 92.0,
      "threshold": 85.0,
      "operator": ">",
      "message": "GPU temperature is 92.0 C (threshold: 85 C) on worker-03",
      "timestamp": "2026-06-28T06:25:00Z",
      "recovery": false
    }
Webhook handler implementation stub (Python):
  from flask import Flask, request, jsonify
  import hmac, hashlib, json
  app = Flask(__name__)
  WEBHOOK_SECRET = os.environ.get("ALERT_WEBHOOK_SECRET", "")
  @app.route("/webhook/alert", methods=["POST"])
  def handle_alert():
      body = request.get_data()
      sig = request.headers.get("X-Alert-Signature", "")
      expected = hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
      if not hmac.compare_digest(sig, expected):
          return jsonify({"error": "invalid signature"}), 403
      payload = json.loads(body)
      # route to channel based on payload["severity"]
      if payload["severity"] == "critical":
          dispatch_pagerduty(payload)
      dispatch_slack(payload)
      return jsonify({"status": "ok"}), 200
ALERT HISTORY AND QUERY API
Storage: SQLite database at <data_dir>/alert_history.db
Schema:
  CREATE TABLE alerts (
      id TEXT PRIMARY KEY,
      rule_id TEXT NOT NULL,
      agent_id TEXT NOT NULL,
      severity TEXT NOT NULL CHECK(severity IN ('critical','warning','info')),
      metric_name TEXT NOT NULL,
      metric_value REAL NOT NULL,
      threshold REAL NOT NULL,
      message TEXT NOT NULL,
      timestamp TEXT NOT NULL,  -- ISO 8601
      recovery INTEGER NOT NULL DEFAULT 0,
      acknowledged INTEGER NOT NULL DEFAULT 0
  );
  CREATE INDEX idx_alerts_agent ON alerts(agent_id, timestamp);
  CREATE INDEX idx_alerts_severity ON alerts(severity, timestamp);
TTL compaction: DELETE FROM alerts WHERE timestamp < datetime('now', '-30 days');
Compaction runs on startup and every 6 hours.
GET /alerts endpoint:
  GET /alerts?agent_id=worker-03&severity=critical&limit=50&offset=0&since=2026-06-01T00:00:00Z
  Response:
  {
    "alerts": [ ... ],
    "pagination": {
      "total": <int>,
      "limit": <int>,
      "offset": <int>,
      "next_offset": <int | null>
    }
  }
CONSTRAINTS AND LIMITS
Rate limiting implementation:
  Per-agent rolling window counter using an in-memory sorted set keyed by agent_id.
  Each alert event appends a unix timestamp to the set for that agent_id.
  On each new alert event, remove timestamps older than 3600s, then count remaining.
  If count >= max_alerts_per_agent_per_hour (default 10), drop the alert silently
  and increment alert_evaluator_rate_limit_exceeded_total counter.
  The sorted set is local to the engine process; on restart the counter resets
  (equivalent to a clean hour window).
Cooldown suppression:
  Per-rule per-agent_id last-fired timestamp maintained in memory.
  If current_time - last_fired < rule.cooldown_minutes * 60, suppress.
  Cooldown state is periodically snapshotted to SQLite table cooldown_state
  every 60s so that engine restarts preserve active cooldowns.
  CREATE TABLE cooldown_state (
      rule_id TEXT NOT NULL,
      agent_id TEXT NOT NULL,
      suppressed_until TEXT NOT NULL,  -- ISO 8601
      PRIMARY KEY (rule_id, agent_id)
  );
Malformed config handling:
  On load, each rule is validated against a JSON Schema. If a rule fails validation,
  the engine logs the error (with rule id and field) and skips that rule without
  crashing. The /health endpoint returns degraded health status if any rules were
  skipped, but the engine continues evaluating remaining valid rules.
SECURITY
Webhook HMAC signature verification:
  Every outbound webhook POST includes header X-Alert-Signature set to
  HMAC-SHA256(raw_body, shared_secret). Receiving side MUST verify before processing.
IP allowlisting:
  The webhook receiver endpoint checks X-Forwarded-For (or direct remote addr)
  against a configured allowlist CIDR list. Requests from non-allowlisted IPs
  receive 403 with no body. Default allowlist includes loopback and private subnets
  (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16).
TLS requirement:
  The webhook receiver endpoint enforces HTTPS-only. HTTP requests to the endpoint
  receive 426 Upgrade Required. TLS version >= 1.2, preferred 1.3. Self-signed
  certificates for development only; production deployments use a trusted CA.
SCHEMA VALIDATION AND HOT-RELOAD
Config file validation:
  On startup and on every file change, config.yaml is validated against a
  JSON Schema before loading. If validation fails, the engine logs the error
  detail (line number, field path, reason) and keeps the previous valid config.
JSON Schema for rule definition (excerpt):
  {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["rules", "global"],
    "properties": {
      "rules": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["id", "metric", "condition", "severity", "cooldown_minutes"],
          "properties": {
            "id": { "type": "string", "pattern": "^[a-z0-9-]+$" },
            "metric": { "type": "string" },
            "condition": {
              "type": "object",
              "required": ["operator", "value"],
              "properties": {
                "operator": { "enum": [">", "<", ">=", "<=", "=="] },
                "value": { "type": "number" }
              }
            },
            "severity": { "enum": ["critical", "warning", "info"] },
            "cooldown_minutes": { "type": "integer", "minimum": 1 },
            "enabled": { "type": "boolean" },
            "message_template": { "type": "string" }
          }
        }
      }
    }
  }
Hot-reload mechanism:
  The engine installs an inotify watch on the config directory for IN_CLOSE_WRITE
  and IN_MOVED_TO events targeting config.yaml. On notification:
  1. The changed file is atomically copied to a temp path and validated.
  2. If valid, the new config is written to <data_dir>/config_snapshots/
     with filename config.<unix_timestamp>.yaml for rollback.
  3. The active config pointer is swapped via atomic rename(2) of a symlink.
  4. Old config remains in memory until the swap completes; on swap failure,
     the engine logs and retains the previous config.
  5. Rollback: GET /admin/config/rollback?snapshot=<timestamp> restores a
     versioned snapshot.
ALERT AGGREGATION AND THROTTLING
Deduplication:
  If the same metric on the same agent_id fires an alert within 60s of the
  previous alert for the same rule+agent_id pair, the new alert is merged:
  the existing alert's metric_value and last_seen timestamp are updated instead
  of creating a new alert. Reset dedup window on each merge.
Burst limits:
  No more than 5 alerts from the same agent_id may be dispatched within any
  60s sliding window. Excess alerts are queued (max queue depth 100 per agent)
  and dispatched at rate 1 per 12s once the burst window clears. Queue overflow
  drops oldest queued alert for that agent.
Grouped summaries:
  For agents with >= 3 active alerts (unacknowledged, not recovered) within
  a 10-minute rolling window, a single summary notification is dispatched
  instead of individual alerts. Summary format:
  "3 active alerts on worker-03 (2 critical, 1 warning): GPU temp 92C,
  RAM 94%, failure rate 12%"
CONCURRENCY AND RECOVERY
Threading model:
  Main thread: config watcher + lifecycle management.
  Worker pool (configurable size, default 4): metric evaluation.
  Dedicated thread: OTLP gRPC receiver.
  Dedicated thread: HTTP server (Flask/gunicorn) for /alerts, /metrics, /health, /admin.
  Dedicated thread: notification dispatcher with internal queue.
Sharding:
  Agent IDs are sharded across the worker pool via consistent hashing
  (hash(agent_id) % num_workers). Each worker owns all evaluations for its
  assigned agents, so no cross-worker state sharing is needed for cooldown or
  rate limiting. The cooldown state and rate limiter are per-worker structures.
Mutex and lock policy:
  Lock ordering (ascending by resource address to prevent deadlock):
    1. cooldown_locks[t]  (per-rule+agent shard lock)
    2. rate_limit_locks[a] (per-agent shard lock)
    3. alert_history_write_lock (single SQLite write lock)
  Lock timeout: 5 seconds. If a lock cannot be acquired within 5s, the
  evaluation for that metric is skipped, logged as warning, and the next
  metric is processed.
  Fallback on contention: if the rate limit lock is contended after 3s,
  the evaluator uses a best-effort approximate counter (last known count
  from the previous evaluation cycle) rather than blocking further. If the
  alert_history write lock times out, the alert event is buffered in a
  fixed-size ring buffer (capacity 500) and flushed on next successful write.
  No recursion locks. All locks are non-reentrant. If a worker holds a lock
  and needs to acquire another, it releases the held lock first, then
  acquires both in order.
Recovery notification path:
  When an evaluator processes a metric that was previously in Alerting state
  and is now Normal, it checks if recovery_notifications is enabled globally.
  If yes, it generates a RecoveryAlertEvent with the same alert_id as the
  originating alert and sets recovery=true. The event is enqueued to the
  notification dispatcher with channel priority: dashboard push first (fast),
  then webhook/email (async). The alert_history entry for the original alert
  is updated with recovery_timestamp.
EVALUATOR IMPLEMENTATION SKETCH
  class AlertEvaluator:
      def __init__(self, rules, config, db):
          self.rules = {r.id: r for r in rules if r.enabled}
          self.cooldowns = CooldownManager(db)
          self.rate_limiter = RateLimiter(config.max_alerts_per_agent_per_hour)
          self.dispatcher = NotificationDispatcher(config)
          self.db = db
      def evaluate(self, metric_name, value, agent_id, timestamp):
          for rule in self.ordered_rules():
              if not rule.matches(metric_name):
                  continue
              if not rule.condition.evaluate(value):
                  self._check_recovery(rule, agent_id, metric_name, value, timestamp)
                  continue
              if self.cooldowns.is_active(rule.id, agent_id, timestamp):
                  continue
              if not self.rate_limiter.allow(agent_id):
                  metrics.increment("rate_limit_exceeded", agent_id=agent_id)
                  continue
              alert = AlertEvent(
                  rule_id=rule.id, agent_id=agent_id,
                  metric_name=metric_name, metric_value=value,
                  threshold=rule.condition.value,
                  severity=rule.severity,
                  message=rule.format_message(agent_id=agent_id, value=value),
                  timestamp=timestamp
              )
              self.cooldowns.set(rule.id, agent_id, rule.cooldown_minutes)
              self.rate_limiter.record(agent_id, timestamp)
              self.db.insert_alert(alert)
              self.dispatcher.dispatch(alert)
PERSISTENCE AND STATE MANAGEMENT
SQLite database at <data_dir>/alert_engine.db containing tables:
  alerts (alert history, see schema above)
  cooldown_state (persistent cooldown across restarts)
  config_snapshots (versioned config YAML blobs with timestamp + sha256)
TTL-based compaction:
  alerts: DELETE WHERE timestamp < now - 30 days, runs at startup + every 6h.
  cooldown_state: DELETE WHERE suppressed_until < now, runs on every snapshot write.
  config_snapshots: keep last 50, delete oldest on each new snapshot; manual
    archival via /admin/config/snapshots/archive.
Startup recovery:
  1. Load cooldown_state from SQLite; entries with suppressed_until < now are
     discarded (not loaded into memory).
  2. Load last valid config snapshot from config_snapshots table if config.yaml
     is missing or invalid.
  3. Resume evaluation from last checkpoint.
CONFIGURATION EXAMPLE
config.yaml snippet:
  rules:
    - id: gpu-temp
      name: GPU Temperature Alert
      description: Fires when any GPU temperature exceeds the threshold
      metric: gpu.temperature_celsius
      condition:
        operator: ">"
        value: 85
      severity: critical
      cooldown_minutes: 5
      enabled: true
      message_template: "GPU temperature is {value}C (threshold: 85C) on {agent_name}"
  global:
    evaluation_interval_seconds: 60
    default_cooldown_minutes: 10
    recovery_notifications: true
    max_alerts_per_agent_per_hour: 10
    webhook_url: "https://hooks.slack.com/services/..."
    webhook_secret: "${ALERT_WEBHOOK_SECRET}"
    smtp_host: "smtp.example.com"
    smtp_port: 587
    smtp_tls: true
    smtp_from: "alert-engine@forge.local"
    pagerduty_routing_key: "${PD_ROUTING_KEY}"
    tls_enabled: true
    allowed_ips:
      - "127.0.0.0/8"
      - "10.0.0.0/8"
OTLP exporter config snippet (for telemetry sources emitting to the engine):
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318
    prometheus:
      config:
        scrape_configs:
          - job_name: forge-agents
            scrape_interval: 60s
            static_configs:
              - targets: ["agent-metrics:9090"]
  processors:
    batch:
      timeout: 5s
      send_batch_size: 100
  exporters:
    otlp:
      endpoint: alert-engine:4317
      tls:
        insecure: true
  service:
    pipelines:
      metrics:
        receivers: [otlp, prometheus]
        processors: [batch]
        exporters: [otlp]