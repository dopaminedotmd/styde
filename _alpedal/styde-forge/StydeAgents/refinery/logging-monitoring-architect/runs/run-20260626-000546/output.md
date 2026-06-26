OTel tracing pipeline
Instrument all services with OpenTelemetry SDK. Use W3C TraceContext propagation. Set up OTel Collector as gateway with tail-based sampling. Export to Jaeger for trace storage and Grafana Tempo for trace-to-metric bridging.
Sample rate: 100% for error traces, 1% for success traces. Priority sampling on high-traffic endpoints.
Add span attributes: service.name, operation, http.method, http.status_code, error=true, db.system, db.statement (sanitized).
Structured logging with correlation IDs
All logs in JSON format. Every log line carries trace_id, span_id, service.name, environment, timestamp (RFC3339). Logger configured with OTel SpanContext injection.
Log levels: DEBUG (dev), INFO (business events), WARN (degraded paths), ERROR (failures), FATAL (process abort).
PII redaction middleware strips emails, SSNs, credit cards from log payloads before emission.
Centralized via Loki or Elasticsearch. Index by service + environment + date.
RED/USE metrics
Rate (requests/sec), Errors (error count, error ratio), Duration (latency p50/p95/p99) per endpoint per service.
USE for resources: CPU utilization, memory usage, disk IOPS, network bytes in/out per pod/container.
Custom business metrics: active users, order throughput, queue depth, cache hit ratio.
Exposed via /metrics endpoint (Prometheus format). Collected by Prometheus with 15s scrape interval.
Alert rules
Prometheus rules grouped by severity.
P0 (paginate):
- HighErrorRate: error_ratio > 5% over 5m
- ServiceDown: up{} == 0 for 1m
- HighLatency: http_request_duration_seconds_p99 > 5s over 5m
- DiskSpaceCritical: node_filesystem_avail_bytes< 5% for 2m
P1 (notify):
- ElevatedErrorRate: error_ratio > 2% over 10m
- QueueBacklog: queue_depth > 1000 for 5m
- CacheMissSpike: cache_hit_ratio < 0.8 for 5m
P2 (ticket):
- CertificateExpiring: certificate_expiry_days < 14
- ResourceConstraint: cpu_usage > 80% over 15m
Alertmanager routes to PagerDuty (P0/P1) and Slack (all). Runbooks linked in alert annotations.
Grafana dashboards
Dashboard 1 — Service Overview (RED):
Row per service. QPS, error rate, latency heatmap, top 5 slowest endpoints.
Dashboard 2 — Resource Overview (USE):
CPU/Mem/Disk per node. Kubernetes pod count. Network throughput.
Dashboard 3 — Dependencies:
Service graph from traces. Span latency waterfall. Error propagation paths.
Dashboard 4 — Business:
Customer-facing KPIs. Active sessions, successful order rate, funnel drop-off.
All dashboards use Prometheus datasource, with Tempo and Loki as secondary sources for drill-down. Variables: $service, $environment, $time_range.