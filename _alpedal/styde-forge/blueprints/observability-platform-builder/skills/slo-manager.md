# SLO Manager

## Purpose
Define and track SLIs and SLOs in Grafana. Configure multi-window burn-rate alerts, dashboard panels, and error budget tracking.

## Inputs
- tempo_endpoint: Tempo query endpoint for trace-based SLIs
- loki_endpoint: Loki query endpoint for log-based SLIs
- mimir_endpoint: Mimir query endpoint for metric-based SLIs

## Outputs
`slo_definitions` (yaml) - SLI/SLO definitions with burn-rate alerts.
`grafana_datasources` (yaml) - Grafana datasource configurations.

## Behavior
1. Define SLIs for each observability pillar: latency, error rate, throughput, availability
2. Compute SLO targets (e.g. 99.9% availability, p95 latency < 200ms)
3. Configure multi-window burn-rate alerts (fast 5m + slow 30m windows)
4. Create Grafana dashboard panels for error budget, burn rate, SLI trends
5. Register Grafana datasources for Tempo, Loki, and Mimir
6. Return combined SLO definitions and datasource config as YAML

## SLO Definition Template
```yaml
slo_definitions:
  - name: api_availability
    description: API endpoint availability based on HTTP status codes
    sli:
      metric: http_requests_total
      good_condition: status_code < 500
      total_condition: status_code >= 100
      window: 30d
    target: 99.9
    burn_rate_alerts:
      - window: 5m
        severity: critical
        threshold: 14.4
      - window: 30m
        severity: warning
        threshold: 2.4
  - name: api_latency_p95
    description: p95 request latency under 200ms
    sli:
      metric: http_request_duration_seconds
      good_condition: le(0.2)
      window: 30d
    target: 99.5
    burn_rate_alerts:
      - window: 5m
        severity: critical
        threshold: 14.4
      - window: 1h
        severity: warning
        threshold: 2.0
```

## Rules
- Each SLO must define at least two burn-rate alert windows (fast + slow)
- Fast window burn rate threshold: 14.4 (carries 10x error budget in 5m)
- Slow window burn rate threshold: 2.0-2.4 (carries 3x error budget in 30-60m)
- SLI windows must be 28-30d for monthly error budget perspective
- Error budget is defined as 1 - (bad_events / total_events) over the window
- Grafana datasources must use the endpoints from upstream skills
- Use Grafana SLO app or Prometheus-based SLO recording rules in Mimir ruler
