BLUEPRINT.md:
Alert Engine -- Blueprint
Purpose
Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.
Overview
The Alert Engine is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard.
Architecture
Telemetry Sources
  Agent telemetry publishes metrics via OTLP/gRPC on port 4317.
  GPU metrics polled via NVML and converted to OTLP metrics.
  System resource metrics (RAM, CPU, disk) sampled every 10 s via psutil, exported as OTLP gauges.
  All sources carry resource attributes: {service.name, service.instance.id, host.name}.
Alert Evaluator
  Stateless evaluator; one evaluation goroutine per alert rule.
  Reads pre-aggregated metric points from a ring buffer (last 60 s per source).
  Lock-free read path on the ring buffer; write side uses a single spinlock (1 us spin, then park).
  Rule execution shards by rule_id hash across a fixed worker pool (4 workers by default, configurable).
  Mutex policy:
    Per-rule CooldownState protected by a dedicated sync.Mutex.
    Lock order: always acquire rule-level lock before ring-buffer lock. Never invert.
    Timeout: 100 ms per lock acquisition; on timeout the evaluation is skipped and logged.
    Fallback: if 3 consecutive evaluations time out on the same rule, the rule is quarantined and a self-alert fires.
Notification Bus
  In-memory channel buffer of 1024 events.
  Fan-out dispatcher sends to Dashboard UI via WebSocket and optionally to a configurable webhook.
  Webhook delivery retries with exponential backoff (100 ms, 400 ms, 1.6 s, 6.4 s; max 4 attempts).
  On retry exhaustion: logged, no further action.
Concurrency & Recovery
Threading / Sharding Model
  Main loop: single goroutine reads telemetry source channels and pushes raw samples into per-source ring buffers.
  Evaluation pool: 4 goroutines (configurable via eval_workers). Each worker pulls rule IDs from a shared work-stealing queue. Rule evaluation is stateless except for cooldown state, which is protected per-rule as described above.
  Notification dispatch: single goroutine reads from the event channel and fans out to WebSocket and webhook concurrently.
  Sharding: no data-level sharding -- all metrics land in the same ring buffer. The fixed-queue work stealing ensures fairness without partitioning telemetry sources.
Recovery Notification Path
  When a metric returns within bounds after an alert has fired, the evaluator produces a recovery event with type: recovery.
  Recovery events follow the same dispatch path as alert events.
  Notification webhook includes an action field set to alert or recovery so downstream systems can differentiate.
  A recovery notification is sent at most once per alert-symptom instance, gated by the same cooldown expiry check.
Telemetry & Observability
Source Protocol: OTLP/gRPC
  All internal telemetry sources (agent reporters, GPU collector, system sampler) emit OpenTelemetry Protocol (OTLP) over gRPC on port 4317. The Alert Engine itself runs an OTLP gRPC server backed by the OpenTelemetry Collector's receiver.
  Canonical protobuf schema (field-level mapping):
  message ExportMetricsServiceRequest {
    repeated ResourceMetrics resource_metrics = 1;
  }
  message ResourceMetrics {
    Resource resource = 1;
    repeated ScopeMetrics scope_metrics = 2;
  }
  message ScopeMetrics {
    InstrumentationScope scope = 1;
    repeated Metric metrics = 2;
  }
  message Metric {
    string name = 1;                     // e.g. "gpu.temperature"
    string description = 2;
    string unit = 3;                     // e.g. "Cel", "%"
    oneof data {
      Gauge gauge = 4;                  // instantaneous values
      Sum sum = 5;                      // cumulative/delta counters
      Histogram histogram = 6;          // distribution
    }
  }
  message Gauge {
    repeated NumberDataPoint data_points = 1;
  }
  message NumberDataPoint {
    int64 time_unix_nano = 1;
    double as_double = 2;               // all Alert Engine metrics use double
    map<string, string> attributes = 3; // agent_id, host, gpu_index, etc.
  }
  message Sum {
    repeated NumberDataPoint data_points = 1;
    AggregationTemporality aggregation_temporality = 2;
    bool is_monotonic = 3;
  }
  Required resource attributes on every metric:
    service.name          "alert-engine" | "agent-metrics" | "gpu-metrics" | "system-metrics"
    service.instance.id   unique instance identifier (hostname-pid or container id)
    host.name             hostname of the machine emitting the metric
Self-Metrics Endpoint
  The Alert Engine exposes its own internal health and performance metrics on an HTTP endpoint at /metrics in Prometheus text format (OpenMetrics).
  Format:
  # HELP alert_engine_evaluations_total Total rule evaluations performed
  # TYPE alert_engine_evaluations_total counter
  alert_engine_evaluations_total{rule="gpu-temp",result="breach"} 142
  alert_engine_evaluations_total{rule="gpu-temp",result="normal"} 3871
  alert_engine_evaluations_total{rule="ram-usage",result="breach"} 12
  # HELP alert_engine_rule_latency_seconds Rule evaluation duration histogram
  # TYPE alert_engine_rule_latency_seconds histogram
  alert_engine_rule_latency_seconds_bucket{rule="gpu-temp",le="0.001"} 3200
  alert_engine_rule_latency_seconds_bucket{rule="gpu-temp",le="0.005"} 4010
  alert_engine_rule_latency_seconds_bucket{rule="gpu-temp",le="0.010"} 4012
  alert_engine_rule_latency_seconds_bucket{rule="gpu-temp",le="+Inf"} 4013
  alert_engine_rule_latency_seconds_sum{rule="gpu-temp"} 4.21
  alert_engine_rule_latency_seconds_count{rule="gpu-temp"} 4013
  # HELP alert_engine_mutex_contentions_total Mutex acquisition timeouts
  # TYPE alert_engine_mutex_contentions_total counter
  alert_engine_mutex_contentions_total{rule="gpu-temp",lock="cooldown"} 0
  alert_engine_mutex_contentions_total{rule="agent-failure",lock="ring-buffer"} 3
  # HELP alert_engine_queue_depth Current events pending in notification bus
  # TYPE alert_engine_queue_depth gauge
  alert_engine_queue_depth 0
  Prometheus scrape target config snippet (prometheus.yml):
  scrape_configs:
    - job_name: alert-engine
      scrape_interval: 15s
      metrics_path: /metrics
      static_configs:
        - targets:
            - localhost:9091
      metric_relabel_configs:
        - source_labels: [rule]
          regex: (.+)
          target_label: rule
          replacement: $1
Alert Webhook Contract
  When a notification is dispatched, the Alert Engine POSTs a JSON payload to each configured webhook URL. Webhook URLs are defined in config.yaml under webhooks.urls.
  JSON Schema (draft-07):
  {
    "$schema": "https://json-schema.org/draft-07/schema#",
    "$id": "https://forge.nousresearch.com/alert-webhook-v1",
    "title": "Alert Notification Payload",
    "type": "object",
    "required": [
      "id", "action", "rule_id", "metric", "value", "threshold",
      "severity", "source", "timestamp", "message"
    ],
    "properties": {
      "id": {
        "type": "string",
        "format": "uuid",
        "description": "Unique event identifier"
      },
      "action": {
        "type": "string",
        "enum": ["alert", "recovery"],
        "description": "alert or recovery"
      },
      "rule_id": {
        "type": "string",
        "description": "Alert rule identifier from config"
      },
      "metric": {
        "type": "string",
        "description": "Metric name, e.g. gpu.temperature"
      },
      "value": {
        "type": "number",
        "description": "Observed metric value at time of evaluation"
      },
      "threshold": {
        "type": "number",
        "description": "Threshold that was breached or returned from"
      },
      "operator": {
        "type": "string",
        "enum": [">", "<", ">=", "<=", "=="],
        "description": "Comparison operator for the threshold"
      },
      "severity": {
        "type": "string",
        "enum": ["critical", "warning", "info"],
        "description": "Severity level from the rule definition"
      },
      "source": {
        "type": "object",
        "required": ["agent_id", "host"],
        "properties": {
          "agent_id": { "type": "string" },
          "host": { "type": "string" },
          "gpu_index": { "type": "integer" }
        },
        "description": "Source attributes identifying where the metric originated"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "description": "ISO 8601 UTC timestamp of evaluation"
      },
      "message": {
        "type": "string",
        "description": "Human-readable alert message"
      },
      "cooldown_remaining": {
        "type": "integer",
        "description": "Seconds until cooldown expires (omitted for recovery)"
      }
    }
  }
  Example payload:
  {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "action": "alert",
    "rule_id": "gpu-temp",
    "metric": "gpu.temperature",
    "value": 92.0,
    "threshold": 85.0,
    "operator": ">",
    "severity": "critical",
    "source": {
      "agent_id": "worker-03",
      "host": "forge-gpu-03.nousresearch.com",
      "gpu_index": 0
    },
    "timestamp": "2026-06-28T12:34:56.789Z",
    "message": "GPU temperature at 92.0 C on agent worker-03 (threshold: > 85.0 C)",
    "cooldown_remaining": 240
  }
Webhook handler stub (Python / FastAPI):
  from fastapi import FastAPI, Request, HTTPException
  from pydantic import BaseModel, Field
  from typing import Optional
  from datetime import datetime
  import uuid
  app = FastAPI()
  class SourceModel(BaseModel):
      agent_id: str
      host: str
      gpu_index: Optional[int] = None
  class AlertPayload(BaseModel):
      id: uuid.UUID
      action: str                    # "alert" | "recovery"
      rule_id: str
      metric: str
      value: float
      threshold: float
      operator: str
      severity: str                  # "critical" | "warning" | "info"
      source: SourceModel
      timestamp: datetime
      message: str
      cooldown_remaining: Optional[int] = None
  @app.post("/webhook/forge-alert")
  async def handle_alert(payload: AlertPayload, request: Request):
      if payload.action == "alert":
          # dispatch to pager, slack, etc.
          print(f"ALERT: {payload.message}")
      elif payload.action == "recovery":
          print(f"RECOVERED: {payload.message}")
      return {"status": "acknowledged"}
Alert Rules
Rule ID  Metric  Threshold  Severity  Cooldown
gpu-temp  GPU Temperature  > 85 Cel  critical  5 min
ram-usage  RAM Utilization  > 90 %  warning  10 min
agent-failure  Agent Failure Rate  > 10 %  critical  15 min
score-drop  Agent Score Drop  > 15 points  warning  30 min
Flow
  Telemetry sources publish OTLP/gRPC metrics to port 4317.
  The Alert Evaluator reads from the ring buffer and checks every metric against all active rules.
  On breach: a notification event is created, respecting per-rule cooldown and mutex policy.
  The Notification Bus dispatches a push notification to the dashboard via WebSocket and optionally to webhook endpoints.
  The user sees the alert in the dashboard notification panel.
States
  Normal -- all metrics within bounds.
  Alerting -- threshold breached; notification sent.
  Cooldown -- alert fired recently; suppressed until cooldown expires.
  Recovered -- metric returned to normal; optional recovery notification (see Recovery path).
  Quarantined -- rule has exceeded mutex contention threshold; auto-disabled; self-alert fired.
Configuration
All rules are defined in config.yaml. The engine reloads config on startup and can be hot-reloaded via a dashboard admin action.
config.yaml snippet:
  alert_engine:
    otlp_receiver:
      port: 4317
      max_recv_msg_size_mib: 4
    eval_workers: 4
    ring_buffer_seconds: 60
    mutex:
      acquisition_timeout_ms: 100
      max_consecutive_timeouts: 3
    prometheus:
      enabled: true
      listen: ":9091"
    webhooks:
      urls:
        - https://hooks.example.com/forge-alerts
      retry:
        initial_delay_ms: 100
        max_attempts: 4
    rules:
      - id: gpu-temp
        metric: gpu.temperature
        operator: ">"
        threshold: 85.0
        severity: critical
        cooldown: 5m
      - id: ram-usage
        metric: system.memory.usage_percent
        operator: ">"
        threshold: 90.0
        severity: warning
        cooldown: 10m
---
persona.md:
Alert Engine -- Persona
Identity
Title: Alert Engine
Role: Forge Dashboard Monitoring Subsystem
Domain: Infrastructure monitoring, threshold evaluation, notification dispatch
Voice & Tone
  Alerting: Direct, concise, actionable. Uses metric values and agent names.
  Recovery: Calm, informative, confirms resolution.
  System messages (internal): Technical, precise, timestamped.
Responsibilities
  Monitor -- Continuously evaluate OTLP/gRPC telemetry streams from agents, GPUs, and system resources.
  Detect -- Identify threshold breaches via the rule engine with minimal false positives.
  Notify -- Deliver push notifications to the Forge Dashboard in real time. Dispatch webhook payloads per the defined JSON Schema contract.
  Suppress -- Respect cooldowns and mutex contention quarantine to avoid alert fatigue.
  Recover -- Notify when metrics return to acceptable ranges, differentiating action: alert from action: recovery.
  Self-observe -- Expose internal health metrics on the /metrics Prometheus endpoint for observability pipeline.
Communication Style
Situation  Style
Alert triggered  "[CRITICAL] GPU temperature at 92 Cel on agent worker-03."
Alert resolved  "[RECOVERY] GPU temperature back to 62 Cel on agent worker-03."
Cooldown active  (silent -- no repeated notification)
Mutex timeout  "[INTERNAL] Rule gpu-temp skipped -- cooldown lock timed out at 2026-06-28T12:34:56Z"
Webhook exhaustion  "[INTERNAL] Webhook delivery failed for alert a1b2c3d4 after 4 retries"
Constraints
  Never alert on the same metric-agent pair more than once per cooldown window.
  Do not evaluate config that is malformed or missing required fields -- log and skip.
  Respect global rate limit of 10 alerts per agent per hour.
  Respect mutex acquisition timeout of 100 ms; quarantine rules that exceed 3 consecutive timeouts.
Verification Checklist
  Verify all service contracts, notification channels, and observability hooks are specified before considering the blueprint complete:
    [ ] OTLP/gRPC port and protobuf schema defined
    [ ] Webhook endpoint URL(s) configured and JSON Schema payload validated
    [ ] Prometheus /metrics endpoint reachable and scrape target registered
    [ ] Recovery notification path wired (action: recovery in webhook body)
    [ ] Mutex policy documented (lock ordering, timeout, fallback, quarantine)
Decision-making Principles
  Accuracy over speed -- prefer a true positive over a rushed evaluation.
  Silence is healthy -- no news means all metrics are within bounds.
  Self-preservation -- log errors internally; never crash on bad input.
  Contract fidelity -- never emit a webhook payload that violates the defined JSON Schema.