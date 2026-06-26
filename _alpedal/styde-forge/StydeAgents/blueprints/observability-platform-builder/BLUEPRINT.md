# Observability Platform Builder
Domain: devops Version: 1

## Purpose
Builds observability platforms using the LGTM stack. OpenTelemetry collector for ingestion, Tempo for distributed tracing, Loki for log aggregation, Mimir for long-term metric storage, Grafana for dashboards and SLO management. Enables full-stack observability with SLI/SLO tracking and burn-rate alerting.

## Persona
Observability platform engineer. Expert in LGTM stack, distributed tracing, and SLI/SLO management.

## Pipeline
5-step pipeline: deploy OTel collector -> setup Tempo tracing + configure Loki logs + deploy Mimir metrics (parallel) -> define SLOs. The OTel collector is the single ingestion gateway; tracing, logging, and metrics are deployed in parallel as they are independent pillars; SLOs depend on all three being operational.

## Skills
- otel-collector-deployer: Deploy OpenTelemetry Collector with receivers, processors, and exporters for traces/logs/metrics
- tempo-tracing-setup: Set up Grafana Tempo with OTLP ingress, query-frontend, and compactor
- loki-log-aggregator: Configure Loki for structured log aggregation with boltdb-shipper and querier
- mimir-metrics-engineer: Deploy Mimir for long-term metric storage with ruler, alertmanager, and compactor
- slo-manager: Define SLIs and SLOs in Grafana with multi-window burn-rate alerts and dashboard panels

## State Contract
Key                          Produced By              Consumed By             Format
otel_config                  deploy-otel-collector    tempo-tracing-setup     yaml
otel_config                  deploy-otel-collector    configure-loki-logs     yaml
otel_config                  deploy-otel-collector    deploy-mimir-metrics    yaml
tempo_endpoint               setup-tempo-tracing      define-slos             string
loki_endpoint                configure-loki-logs      define-slos             string
mimir_endpoint               deploy-mimir-metrics     define-slos             string
slo_definitions              define-slos              (final output)          yaml
grafana_datasources          define-slos              (final output)          yaml

## Error Boundaries
Step                        Strategy      Max Retries   Fallback         Rationale
deploy-otel-collector       halt          0             -                All pillars depend on OTel collector
setup-tempo-tracing         halt          0             -                Tracing is critical for distributed debugging
configure-loki-logs         retry         2             -                Logs are important but retryable on transient infra failures
deploy-mimir-metrics        retry         2             -                Metrics storage is important but retryable
define-slos                 halt          0             -                SLOs require all three pillars to be operational
