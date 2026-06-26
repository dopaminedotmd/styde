# Mimir Metrics Engineer

## Purpose
Deploy Mimir for long-term metric storage. Configure ruler, alertmanager, compactor, and distributor with tenant isolation.

## Inputs
- otel_config: OTel collector config (used for receiver endpoint consistency)

## Outputs
A YAML mapping with key `mimir_endpoint` containing the Mimir HTTP endpoint (e.g. `http://mimir:8080`).

## Behavior
1. Generate Mimir configuration with distributor, ingester, querier, compactor
2. Configure ruler for recording rules and alertmanager for alert routing
3. Set up multi-tenant mode with per-tenant limits
4. Configure storage backend (local for dev, S3/GCS for production)
5. Set retention (default: 30d for metrics, 24h for rule evaluations)
6. Return the endpoint URL for Grafana datasource

## Mimir Config Template
```yaml
server:
  http_listen_port: 8080
  grpc_listen_port: 9095
multitenancy_enabled: true
distributor:
  pool:
    health_check_ingesters: true
ingester:
  max_block_duration: 2h
  max_block_size_bytes: 104857600
compactor:
  block_ranges: [2h, 12h, 24h]
  blocks_retention_period: 720h
ruler:
  alertmanager_url: http://alertmanager:8080
  rule_path: /var/mimir/rules
blocks_storage:
  backend: filesystem
  filesystem:
    dir: /var/mimir/blocks
  bucket_store:
    sync_dir: /var/mimir/tsdb
limits:
  max_global_series_per_user: 150000
  max_global_series_per_metric: 20000
  ingestion_rate: 10000
  ingestion_burst_size: 20000
```

## Rules
- Mimir must listen on port 8080 for HTTP queries and 9095 for gRPC
- Ingester max_block_duration should be 2h for optimal compaction
- Compactor block_ranges must be multiples of ingester block duration
- Blocks retention minimum: 720h (30 days)
- Multi-tenancy should be enabled with per-user series limits
- Always configure recording rules for RED metrics (Rate, Errors, Duration) per service
- Alertmanager config must include routing tree with severity-based receivers
