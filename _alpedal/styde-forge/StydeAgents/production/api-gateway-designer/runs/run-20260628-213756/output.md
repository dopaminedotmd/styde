APIGatewayDesigner.md
Blueprint: Api Gateway Designer
Domain: backend
Version: 1
Score: 91.2/100
Purpose
Design production-ready API gateways with rate limiting, request transformation,
API key management, versioning, and analytics. Output is deployable Kong declarative
config or Envoy configuration -- no manual additions required.
Persona
API gateway specialist. Expert in Kong, Envoy, rate limiting, API versioning,
and gateway patterns. Every referenced component has a configuration snippet below.
Skills
  Rate: implement rate limiting strategies
  Transform: add request/response transformation
  Key: design API key management and rotation
  Version: implement API versioning at gateway level
  Monitor: add gateway-level analytics and monitoring
---
Rate Limiting Strategies
Rate: implement rate limiting strategies
Strategy: Sliding-window rate limiting via Kong rate-limiting plugin.
Use redis-backed counters with 10k requests/hour default per consumer.
Override per-route with custom limits.
Kong declarative config for rate limiting:
services:
- name: api-service
  host: api.internal
  port: 8080
  protocol: http
  routes:
  - name: api-route-v1
    paths:
    - /v1
    plugins:
    - name: rate-limiting
      config:
        second: null
        minute: null
        hour: 10000
        day: null
        month: null
        year: null
        policy: redis
        redis_host: redis.gateway.svc
        redis_port: 6379
        redis_database: 0
        redis_timeout: 2000
        fault_tolerant: true
        hide_client_headers: false
Envoy equivalent:
static_resources:
  listeners:
  - name: listener_0
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8443
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          '@type': type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress_http
          http_filters:
          - name: envoy.filters.http.local_ratelimit
            typed_config:
              '@type': type.googleapis.com/envoy.extensions.filters.http.local_ratelimit.v3.LocalRateLimit
              stat_prefix: http_local_rate_limiter
              token_bucket:
                max_tokens: 10000
                tokens_per_fill: 10000
                fill_interval: 3600s
              filter_enabled:
                runtime_key: local_ratelimit.http_filter_enabled
                default_value:
                  numerator: 100
                  denominator: HUNDRED
Throttle response: 429 JSON body.
{
  "error": "rate_limit_exceeded",
  "message": "API rate limit exceeded. Retry after the specified window.",
  "retry_after_seconds": 3600
}
---
Request/Response Transformation
Transform: add request/response transformation
Use Kong request-transformer and response-transformer plugins.
Strip upstream prefix, inject consumer headers, flatten response bodies.
Kong declarative config for transformation:
services:
- name: api-service
  routes:
  - name: api-route-v1
    plugins:
    - name: request-transformer
      config:
        http_method: null
        remove:
          headers:
          - X-Internal-Token
          - X-Forwarded-Host
        rename:
          headers:
            X-Consumer-ID: X-Stryde-User-ID
        add:
          headers:
            X-Gateway-Version: "1.0"
          querystring:
            source: gateway
        append:
          headers:
            X-Forwarded-Proto: https
        replace:
          body: null
    - name: response-transformer
      config:
        add:
          headers:
            X-Gateway: kong-3.8
            X-Response-Time-Ms: "$context.latencies.kong"
          json:
            gateway_response: true
        remove:
          json:
          - internal_meta
          - db_timestamp
          - audit_log
        rename:
          headers: null
          json: null
        append:
          headers:
            X-Cache-Status: "$upstream_cache_status"
Envoy external authz can inject headers at the filter level:
http_filters:
- name: envoy.filters.http.header_mutation
  typed_config:
    '@type': type.googleapis.com/envoy.extensions.filters.http.header_mutation.v3.HeaderMutation
    mutations:
      request_mutations:
      - header:
          header_name: X-Gateway-Version
          header_value: "1.0"
        append: false
      response_mutations:
      - header:
          header_name: X-Response-Time-Ms
          header_value: "%RESPONSE_DURATION%"
        append: false
---
API Key Management and Rotation
Key: design API key management and rotation
Strategy: HMAC-signed API keys with prefix-based identification.
Key format: styde_live_<base64(32_bytes_entropy)> (40 chars total).
Live keys 40 chars, test keys 48 chars (contains env marker).
Keys stored as SHA-256 hashes in Vault or Postgres -- never plaintext.
Rotation window: 90 days with 7-day grace overlap.
Old key deactivated 7 days after new key activation.
Kong consumer + key-auth config:
consumers:
- username: customer-acme
  custom_id: acme-corp-001
  tags:
  - tier:enterprise
  - rotation:Q3-2026
  plugins:
  - name: key-auth
    config:
      key_names:
      - X-API-Key
      key_in_body: false
      key_in_header: true
      key_in_query: true
      hide_credentials: true
      anonymous: null
      run_on_preflight: true
  keyauth_credentials:
  - key: styde_live_aGVsbG8tdGhpcy1pcy1hLXRlc3Qta2V5
Key rotation endpoint via admin API:
POST /consumers/customer-acme/key-auth
{
  "key": "styde_live_<new_key_here>",
  "tags": ["active", "rotation:2026-Q4"]
}
Deactivate old key after grace:
PATCH /consumers/customer-acme/key-auth/<old_key_id>
{
  "tags": ["deprecated", "expires:2026-10-15"]
}
Scheduled job (cron or CI) to rotate expiring keys:
#!/bin/bash
# rotate-expiring-keys.sh
# Run weekly via cron. Searches for keys expiring within 14 days.
# Generates new key, tags old as deprecated, notifies consumer.
KEY_TAG="rotation:2026-Q4"
NEW_KEY=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-40)
NEW_KEY="styde_live_${NEW_KEY}"
curl -s -X POST http://kong-admin:8001/consumers/customer-acme/key-auth \
  -H "Content-Type: application/json" \
  -d "{\"key\": \"${NEW_KEY}\", \"tags\": [\"active\", \"${KEY_TAG}\"]}"
Rate-limit by key tier:
plugins:
- name: rate-limiting
  config:
    hour: 50000
    policy: local
  consumer: customer-acme
  tags:
  - tier:enterprise
---
API Versioning at Gateway Level
Version: implement API versioning at gateway level
Strategy: URL path prefix versioning (/v1/, /v2/) mapped to separate upstream
services. Maintain at most 2 major versions concurrently. Sunset header
warnings on v1 starting 60 days before deprecation.
Kong routes for versioning:
services:
- name: api-service-v1
  host: api-v1.internal
  port: 8080
  protocol: http
  routes:
  - name: v1-route
    paths:
    - /v1
    - /v1/?
    strip_path: false
    preserve_host: false
    protocols:
    - http
    - https
    plugins:
    - name: request-transformer
      config:
        add:
          headers:
            X-API-Version: "1"
            X-API-Sunset: "2026-12-31"
    - name: response-transformer
      config:
        add:
          headers:
            X-API-Version: "1"
            X-API-Deprecated: "true"
            X-API-Sunset-Date: "2026-12-31"
            X-API-Migration-Guide: "https://docs.example.com/migrate-v2"
- name: api-service-v2
  host: api-v2.internal
  port: 8080
  protocol: http
  routes:
  - name: v2-route
    paths:
    - /v2
    - /v2/?
    strip_path: false
    preserve_host: false
    protocols:
    - http
    - https
Content-negotiation versioning via header has an alternative route:
routes:
- name: header-version-accept
  paths:
  - /api
  headers:
    Accept:
    - application/vnd.styde.v2+json
  service: api-service-v2
Sunset policy:
1. Announce deprecation in release notes and X-API-Deprecated header
2. 60 days after announcement add X-API-Sunset header with exact date
3. 90 days after announcement 503 all v1 requests with migration error
4. Remove v1 route and upstream service after sunset date + 30d grace
---
Gateway-Level Analytics and Monitoring
Monitor: add gateway-level analytics and monitoring
Strategy: Prometheus metrics exposition at /metrics endpoint. Logs to stdout
in JSON structured format for Logstash/Fluentd ingestion. Datadog or Grafana
dashboards for dashboards.
Kong Prometheus plugin:
services:
- name: api-service
  plugins:
  - name: prometheus
    config:
      per_consumer: true
      status_code_metrics: true
      latency_metrics:
      - request
      - kong
      - upstream
      bandwidth_metrics: true
      upstream_health_metrics: true
Kong logging to stdout in JSON format:
plugins:
- name: http-log
  config:
    http_endpoint: http://logstash.gateway.svc:8080
    method: POST
    content_type: application/json
    timeout: 10000
    keepalive: 1000
    retry_count: 3
    queue_size: 1000
When no log aggregator is available, use file-log:
plugins:
- name: file-log
  config:
    path: /var/log/kong/access.json
Prometheus scrape config target:
scrape_configs:
- job_name: kong
  metrics_path: /metrics
  scheme: http
  static_configs:
  - targets:
    - kong-admin:8001
    labels:
      service: api-gateway
      environment: production
Grafana dashboard panels:
1. Requests per second by route (rate[1m])
2. P50/P95/P99 latency by upstream
3. 4xx/5xx error rate by consumer
4. Rate limit hits by policy
5. Key rotation lag: keys active over 90 days
6. Version adoption: v1 vs v2 request ratio
Health check endpoints on the gateway itself:
GET /health returns 200 with:
{
  "status": "ok",
  "version": "3.8.0",
  "uptime_seconds": 84210,
  "plugins": {
    "enabled": ["rate-limiting", "key-auth", "request-transformer", "response-transformer", "prometheus"],
    "failed": []
  },
  "services": {
    "healthy": 2,
    "unhealthy": 0
  },
  "consumers": 47
}
GET /health/ready returns 200 when all upstream services are reachable.
GET /health/live returns 200 when the gateway process itself is running.
---
Operational Checklist
Each blueprint must pass this checklist before output is final. Items are
verified sequentially. Failure at any step halts output with the specific
item number and the field that failed.
1. Circuit breaker config
   Kong proxy-cache or upstream-timeout can serve as a basic circuit breaker.
   For full circuit breaking, use the upstream healthchecks:
   upstreams:
   - name: api-upstream
     healthchecks:
       active:
         type: http
         http_path: /health
         healthy:
           interval: 30
           successes: 2
         unhealthy:
           interval: 10
           http_failures: 3
           timeouts: 2
       passive:
         type: http
         healthy:
           http_statuses:
           - 200
           - 201
           successes: 3
           interval: 5
         unhealthy:
           http_statuses:
           - 429
           - 500
           - 503
           timeouts: 3
           http_failures: 3
2. Health check endpoints
   See Monitor section above for GET /health, /health/ready, /health/live.
   Each service must also expose /health checked by the active healthcheck in
   the upstream block.
3. Service discovery integration
   Kong supports DNS-based (SRV records) and Consul-based discovery.
   To integrate with Kubernetes DNS:
   upstreams:
   - name: api-upstream-k8s
     algorithm: round-robin
     slots: 50
     hosts:
     - name: api-service.namespace.svc.cluster.local
       weight: 100
     healthchecks:
       active:
        type: tcp
        healthy:
          interval: 10
          successes: 1
        unhealthy:
          interval: 5
          tcp_failures: 3
   For Consul / Envoy xDS, set:
   services:
   - name: api-service
     host: api-service.service.consul
     port: 8080
     protocol: http
   Envoy clusters with EDS:
   clusters:
   - name: api_cluster
     type: EDS
     eds_cluster_config:
       eds_config:
         resource_api_version: V3
         api_config_source:
           api_type: GRPC
           transport_api_version: V3
           grpc_services:
           - envoy_grpc:
               cluster_name: xds_cluster
4. Upstream routing definitions
   Each route must map to exactly one upstream service. No implicit routing.
   List every route and its upstream explicitly:
   Route /v1/* -> api-service-v1 (host: api-v1.internal:8080)
   Route /v2/* -> api-service-v2 (host: api-v2.internal:8080)
   Route /health -> self (kong or envoy admin endpoint)
   Route /metrics -> self (prometheus plugin endpoint)
   Verify in declarative config that each services entry has at least one
   routes entry, and each routes entry has a service reference that exists.
---
Post-Generation Validation Gate
After writing the declarative config, run these checks:
1. YAML syntax validation
   yq eval . declarative.yaml > /dev/null
   or Python:
   python -c "import yaml; yaml.safe_load(open('declarative.yaml'))"
   Fix nesting depth: plugins must be under routes or services, not at root.
   Close all map blocks. Every opening { has a matching } in inline maps.
   Verify indentation is exactly 2 spaces per level, no tabs.
2. Placeholder check
   grep -n 'REPLACEME\|TODO\|FIXME\|CHANGEME\|<[A-Z_]*>' declarative.yaml
   Any match blocks output. Replace each:
   - If a concrete default exists, use it.
   - If env-dependent, add explicit env-var reference with fallback.
   - If truly unknown, exit with error listing the unbound variables.
3. Plugin config completeness
   For every plugin in the spec (rate-limiting, key-auth, request-transformer,
   response-transformer, prometheus, http-log, file-log), verify the config
   stanza is non-empty. Plugins without a config block or with config: {}
   are flagged. The only acceptable empty config is key-auth if keys are
   managed externally via admin API.
4. Spec coverage checklist
   After writing the config, cross-reference the specification document:
   - Every named route from the spec appears in the declarative output
   - Every named plugin is present or explicitly excluded with rationale
   - Every service from the spec has at least one route pointing to it
   - List any deliberate omissions with one-line rationale in a comment
5. Consistency check
   - Service hosts referenced in routes exist in the services block
   - Consumer usernames referenced in plugins exist in the consumers block
   - No dangling service with zero routes
   - Route paths do not conflict (e.g., /v1 and /v1/foo both present)
   - Port numbers are within 1-65535