agent: observability-platform-engineer
blueprint: observability-platform-builder
version: 1
domain: devops
status: active
pipeline:
  collector:
    instance: otel-collector-01
    version: 0.120.0
    config_path: /etc/otel/config.yaml
    receivers:
      - otlp:
          protocols:
            grpc:
              endpoint: 0.0.0.0:4317
            http:
              endpoint: 0.0.0.0:4318
      - hostmetrics:
          collection_interval: 30s
      - kubeletstats:
          collection_interval: 30s
      - prometheus:
          config:
            scrape_configs:
              - job_name: node-exporter
                static_configs:
                  - targets:
                      - localhost:9100
    processors:
      - memory_limiter:
          check_interval: 5s
          limit_mib: 512
          spike_limit_mib: 128
      - batch:
          timeout: 5s
          send_batch_size: 1024
      - attributes:
          actions:
            - key: environment
              value: production
              action: upsert
            - key: cluster
              value: styde-forge-prod
              action: upsert
      - resourcedetection:
          detectors:
            - env
            - system
            - eks
    exporters:
      - otlp/tempo:
          endpoint: tempo.monitoring.svc:4317
          tls:
            insecure: true
      - otlp/loki:
          endpoint: loki-gateway.monitoring.svc:4317
          tls:
            insecure: true
      - prometheusremotewrite/mimir:
          endpoint: http://mimir-nginx.monitoring.svc:8080/api/v1/push
          resource_to_telemetry_conversion:
            enabled: true
      - logging:
          verbosity: detailed
          sampling_initial: 5
          sampling_thereafter: 200
    service:
      pipelines:
        traces:
          receivers:
            - otlp
          processors:
            - memory_limiter
            - batch
            - attributes
            - resourcedetection
          exporters:
            - otlp/tempo
            - logging
        metrics:
          receivers:
            - otlp
            - hostmetrics
            - kubeletstats
            - prometheus
          processors:
            - memory_limiter
            - batch
            - attributes
            - resourcedetection
          exporters:
            - prometheusremotewrite/mimir
            - logging
        logs:
          receivers:
            - otlp
          processors:
            - memory_limiter
            - batch
            - attributes
            - resourcedetection
          exporters:
            - otlp/loki
            - logging
tempo:
  version: 2.7.0
  namespace: monitoring
  storage:
    backend: s3
    s3:
      bucket: styde-tempo-traces
      endpoint: s3.eu-west-1.amazonaws.com
    trace_retention_period: 336h
  ingester:
    max_block_duration: 30m
    max_block_bytes: 500_000_000
  compactor:
    compaction:
      block_retention: 48h
  querier:
    search:
      max_duration: 168h
  metrics_generator:
    enabled: true
    registry:
      collection_interval: 30s
    processor:
      span_metrics:
        histogram_buckets:
          - 0.001
          - 0.005
          - 0.01
          - 0.025
          - 0.05
          - 0.1
          - 0.25
          - 0.5
          - 1
          - 2.5
          - 5
          - 10
      service_graphs:
        max_items: 10000
        wait: 10s
loki:
  version: 3.4.0
  namespace: monitoring
  storage:
    type: s3
    s3:
      bucket: styde-loki-logs
      region: eu-west-1
  ingester:
    max_chunk_age: 2h
    chunk_target_size: 1572864
    chunk_retain_period: 3m
  compactor:
    retention_enabled: true
    retention_rules:
      - selector:
          match:
            - '{environment="production"}'
        period: 720h
      - selector:
          match:
            - '{environment="staging"}'
        period: 168h
  ruler:
    evaluation_interval: 1m
    rules:
      - name: high_error_rate
        expr: rate({app=~".+"} |= `error` [5m]) / rate({app=~".+"}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
mimir:
  version: 2.15.0
  namespace: monitoring
  storage:
    backend: s3
    s3:
      bucket_name: styde-mimir-metrics
      endpoint: s3.eu-west-1.amazonaws.com
  ingester:
    blocks_storage:
      bucket_store:
        sync_dir: /data/mimir/tsdb-sync
  compactor:
    retention: 720h
  ruler:
    evaluation_interval: 1m
    rules:
      - name: api-error-rate-slo
        expr: |
          (
            sum(rate(http_requests_total{status_code=~"5.."}[5m]))
            /
            sum(rate(http_requests_total[5m]))
          ) * 100 > 1
        for: 5m
        labels:
          severity: critical
          sli: error_rate
        annotations:
          summary: API error rate exceeds 1%
slo:
  framework: grafana-slo
  slis:
    - name: api-availability
      objective: 99.9
      window: 30d
      burn_rate:
        - name: critical
          threshold: 14.4
          window: 5m
        - name: warning
          threshold: 6
          window: 30m
      indicator:
        type: prometheus
        metric: |
          (
            sum(rate(http_requests_total{status_code!~"5.."}[1m]))
            /
            sum(rate(http_requests_total[1m]))
          ) * 100
    - name: api-latency-p99
      objective: 95
      window: 30d
      burn_rate:
        - name: critical
          threshold: 14.4
          window: 5m
      indicator:
        type: prometheus
        metric: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
        threshold: 0.5
    - name: trace-ingestion
      objective: 99.5
      window: 7d
      indicator:
        type: prometheus
        metric: |
          (
            sum(rate(tempo_ingester_bytes_received_total[5m]))
            /
            sum(rate(tempo_ingester_bytes_received_total[5m]) + rate(tempo_ingester_bytes_dropped_total[5m]))
          ) * 100
grafana:
  version: 11.5.0
  namespace: monitoring
  datasources:
    - name: Mimir
      type: prometheus
      url: http://mimir-nginx.monitoring.svc:8080/prometheus
      access: proxy
      isDefault: true
    - name: Loki
      type: loki
      url: http://loki-gateway.monitoring.svc:3100
      access: proxy
    - name: Tempo
      type: tempo
      url: http://tempo-query-frontend.monitoring.svc:3100
      access: proxy
      derivedFields:
        - name: traceID
          type: field
          datasourceUid: tempo
          matcherRegex: '(?:traceID|trace_id)=(\w+)'
  dashboards:
    - name: Service Overview
      panels:
        - title: Request Rate
          datasource: Mimir
          query: sum(rate(http_requests_total[5m]))
        - title: Error Rate
          datasource: Mimir
          query: sum(rate(http_requests_total{status_code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100
        - title: P99 Latency
          datasource: Mimir
          query: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
        - title: Recent Errors
          datasource: Loki
          query: '{app=~".+"} |= `error`'
    - name: SLO Dashboard
      panels:
        - title: API Availability SLO
          datasource: Mimir
          query: grafana_slo_api_availability_burn_rate
        - title: Error Budget
          datasource: Mimir
          query: grafana_slo_api_availability_error_budget_remaining
alerts:
  - name: TraceDropped
    condition: rate(tempo_ingester_bytes_dropped_total[5m]) > 0
    severity: warning
    channel: pagerduty:observability
  - name: MimirIngestionLag
    condition: mimir_ingester_memory_series > 5000000
    severity: critical
    channel: slack:styde-ops
  - name: LokiRequestErrors
    condition: rate(loki_request_duration_seconds_count{status_code=~"5.."}[5m]) > 0.01
    severity: warning
    channel: slack:styde-ops