OTEL COLLECTOR PIPELINE
Agent mode: deployment
Receiver: OTLP gRPC + HTTP on default ports
Processors: batch, memory_limiter, attributes (env=staging, service.version=$ENV)
Exporters: otlp (Tempo), loki (logs), prometheusremotewrite (Mimir)
Pipeline config:
receivers:
  otlp:
    protocols:
      grpc: endpoint: 0.0.0.0:4317
      http: endpoint: 0.0.0.0:4318
processors:
  batch:
    timeout: 5s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
  attributes:
    actions:
      - key: deployment.environment
        value: staging
        action: upsert
exporters:
  otlp/tempo:
    endpoint: tempo:4317
    tls: insecure: true
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
  prometheusremotewrite/mimir:
    endpoint: http://mimir:9009/api/v1/push
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlp/tempo]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [loki]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [prometheusremotewrite/mimir]
TEMPO CONFIG
distributor:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
ingester:
  trace_idle_period: 10s
  max_block_duration: 5m
compactor:
  compaction:
    block_retention: 48h
storage:
  trace:
    backend: s3
    s3:
      bucket: tempo-traces
      endpoint: minio:9000
      access_key: ${MINIO_ACCESS_KEY}
      secret_key: ${MINIO_SECRET_KEY}
    block:
      version: vParquet3
LOKI CONFIG
auth_enabled: false
server:
  http_listen_port: 3100
ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
  chunk_idle_period: 5m
  chunk_retain_period: 30s
schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: s3
      schema: v13
      index:
        prefix: index_
        period: 24h
storage_config:
  s3:
    bucket: loki-logs
    endpoint: minio:9000
    access_key_id: ${MINIO_ACCESS_KEY}
    secret_access_key: ${MINIO_SECRET_KEY}
MIMIR CONFIG
multitenancy_enabled: false
distributor:
  ring:
    kvstore:
      store: inmemory
ingester:
  ring:
    kvstore:
      store: inmemory
storage:
  engine: blocks
  s3:
    bucket: mimir-metrics
    endpoint: minio:9000
    access_key_id: ${MINIO_ACCESS_KEY}
    secret_access_key: ${MINIO_SECRET_KEY}
blocks_storage:
  s3:
    bucket: mimir-blocks
    endpoint: minio:9000
    access_key_id: ${MINIO_ACCESS_KEY}
    secret_access_key: ${MINIO_SECRET_KEY}
compactor:
  retention: 30d
SLI/SLO DASHBOARD IN GRAFANA
Datasources provisioned:
- Tempo: http://tempo:3200
- Loki: http://loki:3100
- Mimir: http://mimir:9009/prometheus
SLIs tracked:
- latency: histogram_quantile(0.99, rate(tempo_request_duration_seconds_bucket[5m]))
- error_rate: sum(rate(tempo_spans_rejected_total[5m])) / sum(rate(tempo_spans_received_total[5m]))
- throughput: sum(rate(tempo_spans_received_total[5m]))
- log_error_rate: sum(rate({app=~".*"} |= "error"[5m])) / sum(rate({app=~".*"}[5m]))
- availability: up{job=~"observability.*"}
SLO targets:
- p99 latency <= 500ms: 99.9%
- error rate < 0.1%: 99.9%
- log error budget: 99.5%
- service uptime: 99.99%
Deployment: Docker Compose with services listed, MinIO for S3-compatible storage, all configs mounted as volumes. Single-node mode for dev/staging. Scale Tempo ingesters + Mimir ingesters for prod.