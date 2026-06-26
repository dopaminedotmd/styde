# Loki Log Aggregator

## Purpose
Configure Loki for log aggregation. Set up boltdb-shipper, querier, ingester, and structured metadata extraction.

## Inputs
- otel_config: OTel collector config (used for receiver endpoint consistency)

## Outputs
A YAML mapping with key `loki_endpoint` containing the Loki HTTP endpoint (e.g. `http://loki:3100`).

## Behavior
1. Generate Loki configuration with ingester, querier, and distributor components
2. Configure boltdb-shipper for index and object storage
3. Set up structured metadata parsing with logfmt, json, and regex stages
4. Configure retention (default: 14d for logs, 7d for chunk store)
5. Enable label extraction from log content (service, level, trace_id, env)
6. Return the endpoint URL for Grafana datasource

## Loki Config Template
```yaml
server:
  http_listen_port: 3100
  grpc_listen_port: 9095
auth:
  enabled: false
ingester:
  chunk_idle_period: 30m
  chunk_retain_period: 1m
  max_chunk_age: 1h
schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v12
      index:
        prefix: loki_index_
        period: 24h
storage_config:
  boltdb_shipper:
    active_index_directory: /var/loki/index
    cache_location: /var/loki/cache
    shared_store: filesystem
  filesystem:
    directory: /var/loki/chunks
limits_config:
  reject_old_samples: true
  reject_old_samples_max_age: 168h
  max_query_series: 500
```

## Rules
- Loki must listen on port 3100 for HTTP queries
- Chunk idle period should match OTel collector batch interval (1-30m)
- Schema config must use v12 or later for structured metadata support
- boltdb-shipper is the minimum storage; production uses S3/GCS
- Max_query_series limits prevent runaway queries (default 500, increase with caution)
- Always configure reject_old_samples with max_age matching retention
