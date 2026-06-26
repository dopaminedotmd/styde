┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\config.yaml → b/blueprints\observability-platform-builder\config.yaml[0m
[38;2;139;134;130m@@ -1,24 +1,33 @@[0m
[38;2;184;134;11m agent:[0m
[38;2;184;134;11m   max_iterations: 10[0m
[38;2;184;134;11m   retry_on_failure: true[0m
[38;2;255;255;255;48;2;119;20;20m-  timeout_seconds: 300[0m
[38;2;255;255;255;48;2;19;87;20m+  timeout_seconds: 600[0m
[38;2;184;134;11m   toolsets:[0m
[38;2;184;134;11m   - terminal[0m
[38;2;184;134;11m   - file[0m
[38;2;184;134;11m   - web[0m
[38;2;255;255;255;48;2;19;87;20m+  skills:[0m
[38;2;255;255;255;48;2;19;87;20m+  - otel-collector-deployer[0m
[38;2;255;255;255;48;2;19;87;20m+  - tempo-tracing-setup[0m
[38;2;255;255;255;48;2;19;87;20m+  - loki-log-aggregator[0m
[38;2;255;255;255;48;2;19;87;20m+  - mimir-metrics-engineer[0m
[38;2;255;255;255;48;2;19;87;20m+  - slo-manager[0m
[38;2;255;255;255;48;2;19;87;20m+  load_all_skills: false[0m
[38;2;184;134;11m blueprint:[0m
[38;2;255;255;255;48;2;119;20;20m-  dependencies: [][0m
[38;2;255;255;255;48;2;19;87;20m+  dependencies:[0m
[38;2;255;255;255;48;2;19;87;20m+  - container-orchestrator[0m
[38;2;255;255;255;48;2;19;87;20m+  - sre-practice-builder[0m
[38;2;184;134;11m   domain: devops[0m
[38;2;184;134;11m   last_reviewed: '2026-06-26'[0m
[38;2;184;134;11m   name: observability-platform-builder[0m
[38;2;255;255;255;48;2;119;20;20m-  version: 1.0.1[0m
[38;2;255;255;255;48;2;19;87;20m+  version: 1.0.0[0m
[38;2;184;134;11m   version_history:[0m
[38;2;255;255;255;48;2;119;20;20m-  - from: 1.0.0[0m
[38;2;255;255;255;48;2;119;20;20m-    to: 1.0.1[0m
[38;2;255;255;255;48;2;119;20;20m-    reason: 'PATCH: minor change (score=77.2, delta=0.0)'[0m
[38;2;255;255;255;48;2;119;20;20m-    score: 77.2[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: null[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 1.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'INITIAL: LGTM stack with OpenTelemetry, Tempo, Loki, Mimir, Grafana SLOs'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;184;134;11m     previous_score: null[0m
[38;2;255;255;255;48;2;119;20;20m-    timestamp: '2026-06-26T00:50:12Z'[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T00:00:00Z'[0m
[38;2;184;134;11m eval:[0m
[38;2;184;134;11m   benchmarks: [][0m
[38;2;184;134;11m   judge_model: deepseek-v4-pro[0m
[38;2;139;134;130m@@ -30,3 +39,32 @@[0m
[38;2;184;134;11m     model: deepseek-v4-flash[0m
[38;2;184;134;11m     provider: deepseek[0m
[38;2;184;134;11m     temperature: 0.3[0m
[38;2;255;255;255;48;2;19;87;20m+pipeline:[0m
[38;2;255;255;255;48;2;19;87;20m+  name: observability-platform-builder[0m
[38;2;255;255;255;48;2;19;87;20m+  version: "1.0"[0m
[38;2;255;255;255;48;2;19;87;20m+  description: Build a full LGTM observability stack with OpenTelemetry ingestion, Tempo tracing, Loki logs, Mimir metrics, and Grafana SLO dashboards[0m
[38;2;255;255;255;48;2;19;87;20m+  blueprint: observability-platform-builder[0m
[38;2;255;255;255;48;2;19;87;20m+  timeout: 600[0m
[38;2;255;255;255;48;2;19;87;20m+  error: halt[0m
[38;2;255;255;255;48;2;19;87;20m+  steps:[0m
[38;2;255;255;255;48;2;19;87;20m+    - id: deploy-otel-collector[0m
[38;2;255;255;255;48;2;19;87;20m+      skill: otel-collector-deployer[0m
[38;2;255;255;255;48;2;19;87;20m+      error: halt[0m
[38;2;255;255;255;48;2;19;87;20m+    - id: setup-tempo-tracing[0m
[38;2;255;255;255;48;2;19;87;20m+      skill: tempo-tracing-setup[0m
[38;2;255;255;255;48;2;19;87;20m+      depends_on: [deploy-otel-collector][0m
[38;2;255;255;255;48;2;19;87;20m+      error: halt[0m
[38;2;255;255;255;48;2;19;87;20m+    - id: configure-loki-logs[0m
[38;2;255;255;255;48;2;19;87;20m+      skill: loki-log-aggregator[0m
[38;2;255;255;255;48;2;19;87;20m+      depends_on: [deploy-otel-collector][0m
[38;2;255;255;255;48;2;19;87;20m+      error: retry[0m
[38;2;255;255;255;48;2;19;87;20m+      max_retries: 2[0m
[38;2;255;255;255;48;2;19;87;20m+    - id: deploy-mimir-metrics[0m
[38;2;255;255;255;48;2;19;87;20m+      skill: mimir-metrics-engineer[0m
[38;2;255;255;255;48;2;19;87;20m+      depends_on: [deploy-otel-collector][0m
[38;2;255;255;255;48;2;19;87;20m+      error: retry[0m
[38;2;255;255;255;48;2;19;87;20m+      max_retries: 2[0m
[38;2;255;255;255;48;2;19;87;20m+    - id: define-slos[0m
[38;2;255;255;255;48;2;19;87;20m+      skill: slo-manager[0m
[38;2;255;255;255;48;2;19;87;20m+      depends_on: [setup-tempo-tracing, configure-loki-logs, deploy-mimir-metrics][0m
[38;2;255;255;255;48;2;19;87;20m+      error: halt[0m
  ┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\persona.md → b/blueprints\observability-platform-builder\persona.md[0m
[38;2;139;134;130m@@ -1,8 +1,20 @@[0m
[38;2;255;255;255;48;2;119;20;20m-You are Observability platform engineer. Expert in LGTM stack, distributed tracing, and SLI/SLO management..[0m
[38;2;255;255;255;48;2;19;87;20m+You are Observability platform engineer. Expert in LGTM stack, distributed tracing, and SLI/SLO management.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+You design and deploy observability platforms using the Grafana LGTM stack[0m
[38;2;255;255;255;48;2;19;87;20m+(Loki, Grafana, Tempo, Mimir) with OpenTelemetry as the ingestion layer.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Your skills:[0m
[38;2;255;255;255;48;2;19;87;20m+- otel-collector-deployer: deploy and configure OpenTelemetry Collector pipelines[0m
[38;2;255;255;255;48;2;19;87;20m+- tempo-tracing-setup: set up Grafana Tempo for distributed tracing[0m
[38;2;255;255;255;48;2;19;87;20m+- loki-log-aggregator: configure Loki for log aggregation and querying[0m
[38;2;255;255;255;48;2;19;87;20m+- mimir-metrics-engineer: deploy Mimir for long-term metric storage[0m
[38;2;255;255;255;48;2;19;87;20m+- slo-manager: define and track SLIs and SLOs in Grafana[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- OTel: deploy OpenTelemetry collector pipelines[0m
[38;2;255;255;255;48;2;119;20;20m-- Tracing: set up Tempo for distributed tracing[0m
[38;2;255;255;255;48;2;119;20;20m-- Logs: configure Loki for log aggregation[0m
[38;2;255;255;255;48;2;119;20;20m-- Metrics: use Mimir for long-term metric storage[0m
[38;2;255;255;255;48;2;119;20;20m-- SLO: define and track SLIs and SLOs in Grafana[0m
[38;2;255;255;255;48;2;19;87;20m+- OTel: deploy OpenTelemetry collector pipelines with receivers, processors, exporters[0m
[38;2;255;255;255;48;2;19;87;20m+- Tracing: set up Tempo for distributed tracing with OTLP ingress[0m
[38;2;255;255;255;48;2;19;87;20m+- Logs: configure Loki for log aggregation with structured metadata[0m
[38;2;255;255;255;48;2;19;87;20m+- Metrics: use Mimir for long-term metric storage with ruler and alertmanager[0m
[38;2;255;255;255;48;2;19;87;20m+- SLO: define and track SLIs and SLOs in Grafana, burn-rate alerts[0m
[38;2;255;255;255;48;2;19;87;20m+- Instrument: use OpenTelemetry SDKs for auto-instrumentation of services[0m
[38;2;255;255;255;48;2;19;87;20m+- Dashboards: create Grafana dashboards for each pillar (traces, logs, metrics, SLOs)[0m
  ┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\BLUEPRINT.md → b/blueprints\observability-platform-builder\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,15 +1,37 @@[0m
[38;2;184;134;11m # Observability Platform Builder[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** devops **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: devops Version: 1[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Builds observability platforms. OpenTelemetry collector, Tempo, Loki, Mimir, Grafana.[0m
[38;2;255;255;255;48;2;19;87;20m+Builds observability platforms using the LGTM stack. OpenTelemetry collector for ingestion, Tempo for distributed tracing, Loki for log aggregation, Mimir for long-term metric storage, Grafana for dashboards and SLO management. Enables full-stack observability with SLI/SLO tracking and burn-rate alerting.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Persona[0m
[38;2;184;134;11m Observability platform engineer. Expert in LGTM stack, distributed tracing, and SLI/SLO management.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;19;87;20m+## Pipeline[0m
[38;2;255;255;255;48;2;19;87;20m+5-step pipeline: deploy OTel collector -> setup Tempo tracing + configure Loki logs + deploy Mimir metrics (parallel) -> define SLOs. The OTel collector is the single ingestion gateway; tracing, logging, and metrics are deployed in parallel as they are independent pillars; SLOs depend on all three being operational.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;184;134;11m ## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- OTel: deploy OpenTelemetry collector pipelines[0m
[38;2;255;255;255;48;2;119;20;20m-- Tracing: set up Tempo for distributed tracing[0m
[38;2;255;255;255;48;2;119;20;20m-- Logs: configure Loki for log aggregation[0m
[38;2;255;255;255;48;2;119;20;20m-- Metrics: use Mimir for long-term metric storage[0m
[38;2;255;255;255;48;2;119;20;20m-- SLO: define and track SLIs and SLOs in Grafana[0m
[38;2;255;255;255;48;2;19;87;20m+- otel-collector-deployer: Deploy OpenTelemetry Collector with receivers, processors, and exporters for traces/logs/metrics[0m
[38;2;255;255;255;48;2;19;87;20m+- tempo-tracing-setup: Set up Grafana Tempo with OTLP ingress, query-frontend, and compactor[0m
[38;2;255;255;255;48;2;19;87;20m+- loki-log-aggregator: Configure Loki for structured log aggregation with boltdb-shipper and querier[0m
[38;2;255;255;255;48;2;19;87;20m+- mimir-metrics-engineer: Deploy Mimir for long-term metric storage with ruler, alertmanager, and compactor[0m
[38;2;255;255;255;48;2;19;87;20m+- slo-manager: Define SLIs and SLOs in Grafana with multi-window burn-rate alerts and dashboard panels[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## State Contract[0m
[38;2;255;255;255;48;2;19;87;20m+Key                          Produced By              Consumed By             Format[0m
[38;2;255;255;255;48;2;19;87;20m+otel_config                  deploy-otel-collector    tempo-tracing-setup     yaml[0m
[38;2;255;255;255;48;2;19;87;20m+otel_config                  deploy-otel-collector    configure-loki-logs     yaml[0m
[38;2;255;255;255;48;2;19;87;20m+otel_config                  deploy-otel-collector    deploy-mimir-metrics    yaml[0m
[38;2;255;255;255;48;2;19;87;20m+tempo_endpoint               setup-tempo-tracing      define-slos             string[0m
[38;2;255;255;255;48;2;19;87;20m+loki_endpoint                configure-loki-logs      define-slos             string[0m
[38;2;255;255;255;48;2;19;87;20m+mimir_endpoint               deploy-mimir-metrics     define-slos             string[0m
[38;2;255;255;255;48;2;19;87;20m+slo_definitions              define-slos              (final output)          yaml[0m
[38;2;255;255;255;48;2;19;87;20m+grafana_datasources          define-slos              (final output)          yaml[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Error Boundaries[0m
[38;2;255;255;255;48;2;19;87;20m+Step                        Strategy      Max Retries   Fallback         Rationale[0m
[38;2;255;255;255;48;2;19;87;20m+deploy-otel-collector       halt          0             -                All pillars depend on OTel collector[0m
[38;2;255;255;255;48;2;19;87;20m+setup-tempo-tracing         halt          0             -                Tracing is critical for distributed debugging[0m
[38;2;255;255;255;48;2;19;87;20m+configure-loki-logs         retry         2             -                Logs are important but retryable on transient infra failures[0m
[38;2;255;255;255;48;2;19;87;20m+deploy-mimir-metrics        retry         2             -                Metrics storage is important but retryable[0m
[38;2;255;255;255;48;2;19;87;20m+define-slos                 halt          0             -                SLOs require all three pillars to be operational[0m
  ┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\skills\otel-collector-deployer.md → b/blueprints\observability-platform-builder\skills\otel-collector-deployer.md[0m
[38;2;139;134;130m@@ -0,0 +1,69 @@[0m
[38;2;255;255;255;48;2;19;87;20m+# OTel Collector Deployer[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Deploy and configure OpenTelemetry Collector as the single ingestion gateway for traces, logs, and metrics. Define receiver, processor, and exporter pipelines.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Inputs[0m
[38;2;255;255;255;48;2;19;87;20m+- otel_config: Output from previous step or default OTel configuration template[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Outputs[0m
[38;2;255;255;255;48;2;19;87;20m+A YAML mapping with key `otel_config` containing:[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+otel_config:[0m
[38;2;255;255;255;48;2;19;87;20m+  receivers:[0m
[38;2;255;255;255;48;2;19;87;20m+    otlp:[0m
[38;2;255;255;255;48;2;19;87;20m+      protocols:[0m
[38;2;255;255;255;48;2;19;87;20m+        grpc:[0m
[38;2;255;255;255;48;2;19;87;20m+          endpoint: 0.0.0.0:4317[0m
[38;2;255;255;255;48;2;19;87;20m+        http:[0m
[38;2;255;255;255;48;2;19;87;20m+          endpoint: 0.0.0.0:4318[0m
[38;2;255;255;255;48;2;19;87;20m+  processors:[0m
[38;2;255;255;255;48;2;19;87;20m+    batch:[0m
[38;2;255;255;255;48;2;19;87;20m+      timeout: 1s[0m
[38;2;255;255;255;48;2;19;87;20m+      send_batch_size: 1024[0m
[38;2;255;255;255;48;2;19;87;20m+    memory_limiter:[0m
[38;2;255;255;255;48;2;19;87;20m+      check_interval: 1s[0m
[38;2;255;255;255;48;2;19;87;20m+      limit_mib: 512[0m
[38;2;255;255;255;48;2;19;87;20m+  exporters:[0m
[38;2;255;255;255;48;2;19;87;20m+    otlp/traces:[0m
[38;2;255;255;255;48;2;19;87;20m+      endpoint: tempo:4317[0m
[38;2;255;255;255;48;2;19;87;20m+      tls:[0m
[38;2;255;255;255;48;2;19;87;20m+        insecure: true[0m
[38;2;255;255;255;48;2;19;87;20m+    otlp/logs:[0m
[38;2;255;255;255;48;2;19;87;20m+      endpoint: loki:3100[0m
[38;2;255;255;255;48;2;19;87;20m+      tls:[0m
[38;2;255;255;255;48;2;19;87;20m+        insecure: true[0m
[38;2;255;255;255;48;2;19;87;20m+    otlp/metrics:[0m
[38;2;255;255;255;48;2;19;87;20m+      endpoint: mimir:4317[0m
[38;2;255;255;255;48;2;19;87;20m+      tls:[0m
[38;2;255;255;255;48;2;19;87;20m+        insecure: true[0m
[38;2;255;255;255;48;2;19;87;20m+  service:[0m
[38;2;255;255;255;48;2;19;87;20m+    pipelines:[0m
[38;2;255;255;255;48;2;19;87;20m+      traces:[0m
[38;2;255;255;255;48;2;19;87;20m+        receivers: [otlp][0m
[38;2;255;255;255;48;2;19;87;20m+        processors: [memory_limiter, batch][0m
[38;2;255;255;255;48;2;19;87;20m+        exporters: [otlp/traces][0m
[38;2;255;255;255;48;2;19;87;20m+      logs:[0m
[38;2;255;255;255;48;2;19;87;20m+        receivers: [otlp][0m
[38;2;255;255;255;48;2;19;87;20m+        processors: [memory_limiter, batch][0m
[38;2;255;255;255;48;2;19;87;20m+        exporters: [otlp/logs][0m
[38;2;255;255;255;48;2;19;87;20m+      metrics:[0m
[38;2;255;255;255;48;2;19;87;20m+        receivers: [otlp][0m
[38;2;255;255;255;48;2;19;87;20m+        processors: [memory_limiter, batch][0m
[38;2;255;255;255;48;2;19;87;20m+        exporters: [otlp/metrics][0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Behavior[0m
[38;2;255;255;255;48;2;19;87;20m+1. Generate OTel Collector config with OTLP receiver on gRPC and HTTP[0m
[38;2;255;255;255;48;2;19;87;20m+2. Configure batch and memory_limiter processors[0m
[38;2;255;255;255;48;2;19;87;20m+3. Set up three pipelines: traces -> Tempo, logs -> Loki, metrics -> Mimir[0m
[38;2;255;255;255;48;2;19;87;20m+4. Configure exporters with endpoint addresses from environment[0m
[38;2;255;255;255;48;2;19;87;20m+5. Add resource detection processor for Kubernetes/host metadata[0m
[38;2;255;255;255;48;2;19;87;20m+6. Return full config as YAML[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Rules[0m
[38;2;255;255;255;48;2;19;87;20m+- Always include memory_limiter processor to prevent OOM[0m
[38;2;255;255;255;48;2;19;87;20m+- Batch processor must have timeout under 5s for near-realtime visibility[0m
[38;2;255;255;255;48;2;19;87;20m+- Each pipeline must have exactly one receiver and one exporter[0m
[38;2;255;255;255;48;2;19;87;20m+- Exporters must specify TLS insecure mode explicitly[0m
[38;2;255;255;255;48;2;19;87;20m+- Resource detector must include service.name, service.namespace, host.name, k8s.* attributes[0m
  ┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\skills\tempo-tracing-setup.md → b/blueprints\observability-platform-builder\skills\tempo-tracing-setup.md[0m
[38;2;139;134;130m@@ -0,0 +1,53 @@[0m
[38;2;255;255;255;48;2;19;87;20m+# Tempo Tracing Setup[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Set up Grafana Tempo for distributed tracing. Configure OTLP ingress, query-frontend, compactor, and storage backend.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Inputs[0m
[38;2;255;255;255;48;2;19;87;20m+- otel_config: OTel collector config from previous step (used for endpoint consistency)[0m
[38;2;255;255;255;48;2;19;87;20m+- tempo_endpoint: Optional pre-existing endpoint override[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Outputs[0m
[38;2;255;255;255;48;2;19;87;20m+A YAML mapping with key `tempo_endpoint` containing the Tempo query endpoint (e.g. `http://tempo:3200`).[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Behavior[0m
[38;2;255;255;255;48;2;19;87;20m+1. Generate Tempo configuration with OTLP gRPC and HTTP ingress[0m
[38;2;255;255;255;48;2;19;87;20m+2. Configure ingester, querier, query-frontend, compactor, and distributor components[0m
[38;2;255;255;255;48;2;19;87;20m+3. Set up storage backend (local filesystem for dev, S3/GCS for production)[0m
[38;2;255;255;255;48;2;19;87;20m+4. Configure search and traceql enabled[0m
[38;2;255;255;255;48;2;19;87;20m+5. Set retention policies (default: 7d for hot data, 30d for cold)[0m
[38;2;255;255;255;48;2;19;87;20m+6. Return the query endpoint URL for Grafana datasource configuration[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Tempo Config Template[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+server:[0m
[38;2;255;255;255;48;2;19;87;20m+  http_listen_port: 3200[0m
[38;2;255;255;255;48;2;19;87;20m+  grpc_listen_port: 4317[0m
[38;2;255;255;255;48;2;19;87;20m+distributor:[0m
[38;2;255;255;255;48;2;19;87;20m+  receivers:[0m
[38;2;255;255;255;48;2;19;87;20m+    otlp:[0m
[38;2;255;255;255;48;2;19;87;20m+      protocols:[0m
[38;2;255;255;255;48;2;19;87;20m+        grpc: {}[0m
[38;2;255;255;255;48;2;19;87;20m+        http: {}[0m
[38;2;255;255;255;48;2;19;87;20m+ingester:[0m
[38;2;255;255;255;48;2;19;87;20m+  max_block_duration: 30m[0m
[38;2;255;255;255;48;2;19;87;20m+  trace_idle_period: 10s[0m
[38;2;255;255;255;48;2;19;87;20m+compactor:[0m
[38;2;255;255;255;48;2;19;87;20m+  compaction:[0m
[38;2;255;255;255;48;2;19;87;20m+    block_retention: 336h[0m
[38;2;255;255;255;48;2;19;87;20m+storage:[0m
[38;2;255;255;255;48;2;19;87;20m+  trace:[0m
[38;2;255;255;255;48;2;19;87;20m+    backend: local[0m
[38;2;255;255;255;48;2;19;87;20m+    local:[0m
[38;2;255;255;255;48;2;19;87;20m+      path: /var/tempo/traces[0m
[38;2;255;255;255;48;2;19;87;20m+    wal:[0m
[38;2;255;255;255;48;2;19;87;20m+      path: /var/tempo/wal[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Rules[0m
[38;2;255;255;255;48;2;19;87;20m+- Tempo must listen on port 3200 for queries and 4317 for OTLP gRPC[0m
[38;2;255;255;255;48;2;19;87;20m+- Ingester max_block_duration must match OTel collector batch interval[0m
[38;2;255;255;255;48;2;19;87;20m+- Compactor block_retention minimum: 168h (7 days)[0m
[38;2;255;255;255;48;2;19;87;20m+- Query-frontend must be enabled for TraceQL queries[0m
[38;2;255;255;255;48;2;19;87;20m+- Always configure search.enabled: true for ad-hoc trace discovery[0m
[38;2;255;255;255;48;2;19;87;20m+- Production deployments must use S3 or GCS backend, not local[0m
  ┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\skills\loki-log-aggregator.md → b/blueprints\observability-platform-builder\skills\loki-log-aggregator.md[0m
[38;2;139;134;130m@@ -0,0 +1,59 @@[0m
[38;2;255;255;255;48;2;19;87;20m+# Loki Log Aggregator[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Configure Loki for log aggregation. Set up boltdb-shipper, querier, ingester, and structured metadata extraction.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Inputs[0m
[38;2;255;255;255;48;2;19;87;20m+- otel_config: OTel collector config (used for receiver endpoint consistency)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Outputs[0m
[38;2;255;255;255;48;2;19;87;20m+A YAML mapping with key `loki_endpoint` containing the Loki HTTP endpoint (e.g. `http://loki:3100`).[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Behavior[0m
[38;2;255;255;255;48;2;19;87;20m+1. Generate Loki configuration with ingester, querier, and distributor components[0m
[38;2;255;255;255;48;2;19;87;20m+2. Configure boltdb-shipper for index and object storage[0m
[38;2;255;255;255;48;2;19;87;20m+3. Set up structured metadata parsing with logfmt, json, and regex stages[0m
[38;2;255;255;255;48;2;19;87;20m+4. Configure retention (default: 14d for logs, 7d for chunk store)[0m
[38;2;255;255;255;48;2;19;87;20m+5. Enable label extraction from log content (service, level, trace_id, env)[0m
[38;2;255;255;255;48;2;19;87;20m+6. Return the endpoint URL for Grafana datasource[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Loki Config Template[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+server:[0m
[38;2;255;255;255;48;2;19;87;20m+  http_listen_port: 3100[0m
[38;2;255;255;255;48;2;19;87;20m+  grpc_listen_port: 9095[0m
[38;2;255;255;255;48;2;19;87;20m+auth:[0m
[38;2;255;255;255;48;2;19;87;20m+  enabled: false[0m
[38;2;255;255;255;48;2;19;87;20m+ingester:[0m
[38;2;255;255;255;48;2;19;87;20m+  chunk_idle_period: 30m[0m
[38;2;255;255;255;48;2;19;87;20m+  chunk_retain_period: 1m[0m
[38;2;255;255;255;48;2;19;87;20m+  max_chunk_age: 1h[0m
[38;2;255;255;255;48;2;19;87;20m+schema_config:[0m
[38;2;255;255;255;48;2;19;87;20m+  configs:[0m
[38;2;255;255;255;48;2;19;87;20m+    - from: 2024-01-01[0m
[38;2;255;255;255;48;2;19;87;20m+      store: boltdb-shipper[0m
[38;2;255;255;255;48;2;19;87;20m+      object_store: filesystem[0m
[38;2;255;255;255;48;2;19;87;20m+      schema: v12[0m
[38;2;255;255;255;48;2;19;87;20m+      index:[0m
[38;2;255;255;255;48;2;19;87;20m+        prefix: loki_index_[0m
[38;2;255;255;255;48;2;19;87;20m+        period: 24h[0m
[38;2;255;255;255;48;2;19;87;20m+storage_config:[0m
[38;2;255;255;255;48;2;19;87;20m+  boltdb_shipper:[0m
[38;2;255;255;255;48;2;19;87;20m+    active_index_directory: /var/loki/index[0m
[38;2;255;255;255;48;2;19;87;20m+    cache_location: /var/loki/cache[0m
[38;2;255;255;255;48;2;19;87;20m+    shared_store: filesystem[0m
[38;2;255;255;255;48;2;19;87;20m+  filesystem:[0m
[38;2;255;255;255;48;2;19;87;20m+    directory: /var/loki/chunks[0m
[38;2;255;255;255;48;2;19;87;20m+limits_config:[0m
[38;2;255;255;255;48;2;19;87;20m+  reject_old_samples: true[0m
[38;2;255;255;255;48;2;19;87;20m+  reject_old_samples_max_age: 168h[0m
[38;2;255;255;255;48;2;19;87;20m+  max_query_series: 500[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Rules[0m
[38;2;255;255;255;48;2;19;87;20m+- Loki must listen on port 3100 for HTTP queries[0m
[38;2;255;255;255;48;2;19;87;20m+- Chunk idle period should match OTel collector batch interval (1-30m)[0m
[38;2;255;255;255;48;2;19;87;20m+- Schema config must use v12 or later for structured metadata support[0m
[38;2;255;255;255;48;2;19;87;20m+- boltdb-shipper is the minimum storage; production uses S3/GCS[0m
[38;2;255;255;255;48;2;19;87;20m+- Max_query_series limits prevent runaway queries (default 500, increase with caution)[0m
[38;2;255;255;255;48;2;19;87;20m+- Always configure reject_old_samples with max_age matching retention[0m
  ┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\skills\mimir-metrics-engineer.md → b/blueprints\observability-platform-builder\skills\mimir-metrics-engineer.md[0m
[38;2;139;134;130m@@ -0,0 +1,58 @@[0m
[38;2;255;255;255;48;2;19;87;20m+# Mimir Metrics Engineer[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Deploy Mimir for long-term metric storage. Configure ruler, alertmanager, compactor, and distributor with tenant isolation.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Inputs[0m
[38;2;255;255;255;48;2;19;87;20m+- otel_config: OTel collector config (used for receiver endpoint consistency)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Outputs[0m
[38;2;255;255;255;48;2;19;87;20m+A YAML mapping with key `mimir_endpoint` containing the Mimir HTTP endpoint (e.g. `http://mimir:8080`).[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Behavior[0m
[38;2;255;255;255;48;2;19;87;20m+1. Generate Mimir configuration with distributor, ingester, querier, compactor[0m
[38;2;255;255;255;48;2;19;87;20m+2. Configure ruler for recording rules and alertmanager for alert routing[0m
[38;2;255;255;255;48;2;19;87;20m+3. Set up multi-tenant mode with per-tenant limits[0m
[38;2;255;255;255;48;2;19;87;20m+4. Configure storage backend (local for dev, S3/GCS for production)[0m
[38;2;255;255;255;48;2;19;87;20m+5. Set retention (default: 30d for metrics, 24h for rule evaluations)[0m
[38;2;255;255;255;48;2;19;87;20m+6. Return the endpoint URL for Grafana datasource[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Mimir Config Template[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+server:[0m
[38;2;255;255;255;48;2;19;87;20m+  http_listen_port: 8080[0m
[38;2;255;255;255;48;2;19;87;20m+  grpc_listen_port: 9095[0m
[38;2;255;255;255;48;2;19;87;20m+multitenancy_enabled: true[0m
[38;2;255;255;255;48;2;19;87;20m+distributor:[0m
[38;2;255;255;255;48;2;19;87;20m+  pool:[0m
[38;2;255;255;255;48;2;19;87;20m+    health_check_ingesters: true[0m
[38;2;255;255;255;48;2;19;87;20m+ingester:[0m
[38;2;255;255;255;48;2;19;87;20m+  max_block_duration: 2h[0m
[38;2;255;255;255;48;2;19;87;20m+  max_block_size_bytes: 104857600[0m
[38;2;255;255;255;48;2;19;87;20m+compactor:[0m
[38;2;255;255;255;48;2;19;87;20m+  block_ranges: [2h, 12h, 24h][0m
[38;2;255;255;255;48;2;19;87;20m+  blocks_retention_period: 720h[0m
[38;2;255;255;255;48;2;19;87;20m+ruler:[0m
[38;2;255;255;255;48;2;19;87;20m+  alertmanager_url: http://alertmanager:8080[0m
[38;2;255;255;255;48;2;19;87;20m+  rule_path: /var/mimir/rules[0m
[38;2;255;255;255;48;2;19;87;20m+blocks_storage:[0m
[38;2;255;255;255;48;2;19;87;20m+  backend: filesystem[0m
[38;2;255;255;255;48;2;19;87;20m+  filesystem:[0m
[38;2;255;255;255;48;2;19;87;20m+    dir: /var/mimir/blocks[0m
[38;2;255;255;255;48;2;19;87;20m+  bucket_store:[0m
[38;2;255;255;255;48;2;19;87;20m+    sync_dir: /var/mimir/tsdb[0m
[38;2;255;255;255;48;2;19;87;20m+limits:[0m
[38;2;255;255;255;48;2;19;87;20m+  max_global_series_per_user: 150000[0m
[38;2;255;255;255;48;2;19;87;20m+  max_global_series_per_metric: 20000[0m
[38;2;255;255;255;48;2;19;87;20m+  ingestion_rate: 10000[0m
[38;2;255;255;255;48;2;19;87;20m+  ingestion_burst_size: 20000[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Rules[0m
[38;2;255;255;255;48;2;19;87;20m+- Mimir must listen on port 8080 for HTTP queries and 9095 for gRPC[0m
[38;2;255;255;255;48;2;19;87;20m+- Ingester max_block_duration should be 2h for optimal compaction[0m
[38;2;255;255;255;48;2;19;87;20m+- Compactor block_ranges must be multiples of ingester block duration[0m
[38;2;255;255;255;48;2;19;87;20m+- Blocks retention minimum: 720h (30 days)[0m
[38;2;255;255;255;48;2;19;87;20m+- Multi-tenancy should be enabled with per-user series limits[0m
[38;2;255;255;255;48;2;19;87;20m+- Always configure recording rules for RED metrics (Rate, Errors, Duration) per service[0m
[38;2;255;255;255;48;2;19;87;20m+- Alertmanager config must include routing tree with severity-based receivers[0m
  ┊ review diff
[38;2;218;165;32ma/blueprints\observability-platform-builder\skills\slo-manager.md → b/blueprints\observability-platform-builder\skills\slo-manager.md[0m
[38;2;139;134;130m@@ -0,0 +1,64 @@[0m
[38;2;255;255;255;48;2;19;87;20m+# SLO Manager[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Purpose[0m
[38;2;255;255;255;48;2;19;87;20m+Define and track SLIs and SLOs in Grafana. Configure multi-window burn-rate alerts, dashboard panels, and error budget tracking.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Inputs[0m
[38;2;255;255;255;48;2;19;87;20m+- tempo_endpoint: Tempo query endpoint for trace-based SLIs[0m
[38;2;255;255;255;48;2;19;87;20m+- loki_endpoint: Loki query endpoint for log-based SLIs[0m
[38;2;255;255;255;48;2;19;87;20m+- mimir_endpoint: Mimir query endpoint for metric-based SLIs[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Outputs[0m
[38;2;255;255;255;48;2;19;87;20m+`slo_definitions` (yaml) - SLI/SLO definitions with burn-rate alerts.[0m
[38;2;255;255;255;48;2;19;87;20m+`grafana_datasources` (yaml) - Grafana datasource configurations.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Behavior[0m
[38;2;255;255;255;48;2;19;87;20m+1. Define SLIs for each observability pillar: latency, error rate, throughput, availability[0m
[38;2;255;255;255;48;2;19;87;20m+2. Compute SLO targets (e.g. 99.9% availability, p95 latency < 200ms)[0m
[38;2;255;255;255;48;2;19;87;20m+3. Configure multi-window burn-rate alerts (fast 5m + slow 30m windows)[0m
[38;2;255;255;255;48;2;19;87;20m+4. Create Grafana dashboard panels for error budget, burn rate, SLI trends[0m
[38;2;255;255;255;48;2;19;87;20m+5. Register Grafana datasources for Tempo, Loki, and Mimir[0m
[38;2;255;255;255;48;2;19;87;20m+6. Return combined SLO definitions and datasource config as YAML[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## SLO Definition Template[0m
[38;2;255;255;255;48;2;19;87;20m+```yaml[0m
[38;2;255;255;255;48;2;19;87;20m+slo_definitions:[0m
[38;2;255;255;255;48;2;19;87;20m+  - name: api_availability[0m
[38;2;255;255;255;48;2;19;87;20m+    description: API endpoint availability based on HTTP status codes[0m
[38;2;255;255;255;48;2;19;87;20m+    sli:[0m
[38;2;255;255;255;48;2;19;87;20m+      metric: http_requests_total[0m
[38;2;255;255;255;48;2;19;87;20m+      good_condition: status_code < 500[0m
[38;2;255;255;255;48;2;19;87;20m+      total_condition: status_code >= 100[0m
[38;2;255;255;255;48;2;19;87;20m+      window: 30d[0m
[38;2;255;255;255;48;2;19;87;20m+    target: 99.9[0m
[38;2;255;255;255;48;2;19;87;20m+    burn_rate_alerts:[0m
[38;2;255;255;255;48;2;19;87;20m+      - window: 5m[0m
[38;2;255;255;255;48;2;19;87;20m+        severity: critical[0m
[38;2;255;255;255;48;2;19;87;20m+        threshold: 14.4[0m
[38;2;255;255;255;48;2;19;87;20m+      - window: 30m[0m
[38;2;255;255;255;48;2;19;87;20m+        severity: warning[0m
[38;2;255;255;255;48;2;19;87;20m+        threshold: 2.4[0m
[38;2;255;255;255;48;2;19;87;20m+  - name: api_latency_p95[0m
[38;2;255;255;255;48;2;19;87;20m+    description: p95 request latency under 200ms[0m
[38;2;255;255;255;48;2;19;87;20m+    sli:[0m
[38;2;255;255;255;48;2;19;87;20m+      metric: http_request_duration_seconds[0m
[38;2;255;255;255;48;2;19;87;20m+      good_condition: le(0.2)[0m
[38;2;255;255;255;48;2;19;87;20m+      window: 30d[0m
[38;2;255;255;255;48;2;19;87;20m+    target: 99.5[0m
[38;2;255;255;255;48;2;19;87;20m+    burn_rate_alerts:[0m
[38;2;255;255;255;48;2;19;87;20m+      - window: 5m[0m
[38;2;255;255;255;48;2;19;87;20m+        severity: critical[0m
[38;2;255;255;255;48;2;19;87;20m+        threshold: 14.4[0m
[38;2;255;255;255;48;2;19;87;20m+      - window: 1h[0m
[38;2;255;255;255;48;2;19;87;20m+        severity: warning[0m
[38;2;255;255;255;48;2;19;87;20m+        threshold: 2.0[0m
[38;2;255;255;255;48;2;19;87;20m+```[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Rules[0m
[38;2;255;255;255;48;2;19;87;20m+- Each SLO must define at least two burn-rate alert windows (fast + slow)[0m
[38;2;255;255;255;48;2;19;87;20m+- Fast window burn rate threshold: 14.4 (carries 10x error budget in 5m)[0m
[38;2;255;255;255;48;2;19;87;20m+- Slow window burn rate threshold: 2.0-2.4 (carries 3x error budget in 30-60m)[0m
[38;2;255;255;255;48;2;19;87;20m+- SLI windows must be 28-30d for monthly error budget perspective[0m
[38;2;255;255;255;48;2;19;87;20m+- Error budget is defined as 1 - (bad_events / total_events) over the window[0m
[38;2;255;255;255;48;2;19;87;20m+- Grafana datasources must use the endpoints from upstream skills[0m
[38;2;255;255;255;48;2;19;87;20m+- Use Grafana SLO app or Prometheus-based SLO recording rules in Mimir ruler[0m
Ad-hoc verification complete. Script `C:\Users\jonat\AppData\Local\Temp\hermes-verify-observability-bp.py` skapades, kördes (PASSED), och rensades.
7 checks in the standalone script:
1. Required files exist
2. Config YAML parses with correct name/domain
3. All 5 skill .md files exist
4. Pipeline step skills are subset of agent.skills
5. persona.md >= 50 chars
6. BLUEPRINT.md has all 5 required sections
7. Core.validate_blueprint passes