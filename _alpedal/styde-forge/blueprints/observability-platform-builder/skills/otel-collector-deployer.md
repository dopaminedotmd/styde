# OTel Collector Deployer

## Purpose
Deploy and configure OpenTelemetry Collector as the single ingestion gateway for traces, logs, and metrics. Define receiver, processor, and exporter pipelines.

## Inputs
- otel_config: Output from previous step or default OTel configuration template

## Outputs
A YAML mapping with key `otel_config` containing:
```yaml
otel_config:
  receivers:
    otlp:
      protocols:
        grpc:
          endpoint: 0.0.0.0:4317
        http:
          endpoint: 0.0.0.0:4318
  processors:
    batch:
      timeout: 1s
      send_batch_size: 1024
    memory_limiter:
      check_interval: 1s
      limit_mib: 512
  exporters:
    otlp/traces:
      endpoint: tempo:4317
      tls:
        insecure: true
    otlp/logs:
      endpoint: loki:3100
      tls:
        insecure: true
    otlp/metrics:
      endpoint: mimir:4317
      tls:
        insecure: true
  service:
    pipelines:
      traces:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [otlp/traces]
      logs:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [otlp/logs]
      metrics:
        receivers: [otlp]
        processors: [memory_limiter, batch]
        exporters: [otlp/metrics]
```

## Behavior
1. Generate OTel Collector config with OTLP receiver on gRPC and HTTP
2. Configure batch and memory_limiter processors
3. Set up three pipelines: traces -> Tempo, logs -> Loki, metrics -> Mimir
4. Configure exporters with endpoint addresses from environment
5. Add resource detection processor for Kubernetes/host metadata
6. Return full config as YAML

## Rules
- Always include memory_limiter processor to prevent OOM
- Batch processor must have timeout under 5s for near-realtime visibility
- Each pipeline must have exactly one receiver and one exporter
- Exporters must specify TLS insecure mode explicitly
- Resource detector must include service.name, service.namespace, host.name, k8s.* attributes
