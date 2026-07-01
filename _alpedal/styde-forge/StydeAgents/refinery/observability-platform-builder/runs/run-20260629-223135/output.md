otelconfig:
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
      sendbatchsize: 1024
    memorylimiter:
      checkinterval: 1s
      limitmib: 512
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
        processors: [memorylimiter, batch]
        exporters: [otlp/traces]
      logs:
        receivers: [otlp]
        processors: [memorylimiter, batch]
        exporters: [otlp/logs]
      metrics:
        receivers: [otlp]
        processors: [memorylimiter, batch]
        exporters: [otlp/metrics]
tempoendpoint: http://tempo:3200
lokiendpoint: http://loki:3100
mimirendpoint: http://mimir:8080
slodefinitions:
  slos:
  - name: api-availability
    description: API service availability (5xx < 0.1%)
    sli:
      metric: http_requests_total
      goodcondition: status !~ "^5"
      window: 30d
    target: 99.9
    burnratealerts:
    - window: 5m
      severity: critical
      threshold: 14.4
    - window: 30m
      severity: warning
      threshold: 2.4
  - name: api-latency-p95
    description: p95 request latency under 200ms
    sli:
      metric: http_request_duration_seconds
      goodcondition: le(0.2)
      window: 30d
    target: 99.5
    burnratealerts:
    - window: 5m
      severity: critical
      threshold: 14.4
    - window: 1h
      severity: warning
      threshold: 2.0
  - name: api-error-rate
    description: Error rate below 0.5% of all requests
    sli:
      metric: http_requests_total
      goodcondition: status =~ "^2"
      window: 30d
    target: 99.5
    burnratealerts:
    - window: 5m
      severity: critical
      threshold: 14.4
    - window: 30m
      severity: warning
      threshold: 2.4
  - name: trace-completeness
    description: Traces reaching Tempo with complete spans
    sli:
      metric: traces_completed_total
      goodcondition: trace_root_span == true
      window: 30d
    target: 99.0
    burnratealerts:
    - window: 5m
      severity: critical
      threshold: 14.4
    - window: 1h
      severity: warning
      threshold: 2.0
grafanadatasources:
  datasources:
  - name: Tempo
    type: tempo
    url: http://tempo:3200
    access: proxy
    isDefault: false
  - name: Loki
    type: loki
    url: http://loki:3100
    access: proxy
    isDefault: false
    jsonData:
      maxLines: 5000
  - name: Mimir
    type: prometheus
    url: http://mimir:8080/prometheus
    access: proxy
    isDefault: true
    jsonData:
      httpMethod: POST
      prometheusType: Mimir