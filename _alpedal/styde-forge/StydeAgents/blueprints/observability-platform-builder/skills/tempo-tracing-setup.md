# Tempo Tracing Setup

## Purpose
Set up Grafana Tempo for distributed tracing. Configure OTLP ingress, query-frontend, compactor, and storage backend.

## Inputs
- otel_config: OTel collector config from previous step (used for endpoint consistency)
- tempo_endpoint: Optional pre-existing endpoint override

## Outputs
A YAML mapping with key `tempo_endpoint` containing the Tempo query endpoint (e.g. `http://tempo:3200`).

## Behavior
1. Generate Tempo configuration with OTLP gRPC and HTTP ingress
2. Configure ingester, querier, query-frontend, compactor, and distributor components
3. Set up storage backend (local filesystem for dev, S3/GCS for production)
4. Configure search and traceql enabled
5. Set retention policies (default: 7d for hot data, 30d for cold)
6. Return the query endpoint URL for Grafana datasource configuration

## Tempo Config Template
```yaml
server:
  http_listen_port: 3200
  grpc_listen_port: 4317
distributor:
  receivers:
    otlp:
      protocols:
        grpc: {}
        http: {}
ingester:
  max_block_duration: 30m
  trace_idle_period: 10s
compactor:
  compaction:
    block_retention: 336h
storage:
  trace:
    backend: local
    local:
      path: /var/tempo/traces
    wal:
      path: /var/tempo/wal
```

## Rules
- Tempo must listen on port 3200 for queries and 4317 for OTLP gRPC
- Ingester max_block_duration must match OTel collector batch interval
- Compactor block_retention minimum: 168h (7 days)
- Query-frontend must be enabled for TraceQL queries
- Always configure search.enabled: true for ad-hoc trace discovery
- Production deployments must use S3 or GCS backend, not local
