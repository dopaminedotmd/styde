==============================================================================
API GATEWAY DESIGN — Gateway Zero
==============================================================================
SCOPE: New API gateway for styde.ai backend microservices (Forge, Agent, Eval, Dashboard)
==============================================================================
1. RATE LIMITING STRATEGY
==============================================================================
gateway:
  rate_limiting:
    strategy: sliding_window
    window: 60s
    tiers:
      free:
        requests_per_window: 30
        burst: 5
        concurrency: 2
      pro:
        requests_per_window: 300
        burst: 50
        concurrency: 10
      enterprise:
        requests_per_window: 3000
        burst: 500
        concurrency: 50
    per_endpoint_overrides:
      /api/v1/eval:
        window: 60s
        requests_per_window: 20
        reason: eval is GPU-bound, protect inference
      /api/v1/forge/spawn:
        window: 300s
        requests_per_window: 5
        reason: spawns are expensive workloads
      /api/v1/health:
        window: 60s
        requests_per_window: 300
        reason: health check needs no throttle
    headers:
      - X-RateLimit-Limit
      - X-RateLimit-Remaining
      - X-RateLimit-Reset
      - Retry-After
    backend: redis
    redis_key_format: "ratelimit:{tier}:{client_id}:{endpoint}"
    quota_exhausted_response: 429
    quota_exhausted_body:
      error: rate_limit_exceeded
      retry_after_seconds: "{reset}"
==============================================================================
2. REQUEST/RESPONSE TRANSFORMATION
==============================================================================
gateway:
  transformations:
    request:
      - name: strip_version_prefix
        match: ^/api/v[0-9]+/(.+)
        rewrite: /{1}
        reason: upstream services dont need version in path
      - name: inject_auth_context
        headers:
          add:
            X-Client-Id: "{api_key.client_id}"
            X-Client-Tier: "{api_key.tier}"
            X-Request-Id: "{uuid}"
          strip:
            - Authorization
            - X-Api-Key
        reason: downstream services read headers not raw auth tokens
      - name: normalize_content_type
        condition: content_type == "application/x-www-form-urlencoded"
        action: convert_to_json
        reason: all internal services expect JSON
      - name: cors_preflight
        match: OPTIONS
        action: respond_with_204
        headers:
          Access-Control-Allow-Origin: "{origin}"
          Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH
          Access-Control-Allow-Headers: Content-Type, Authorization, X-Api-Key
          Access-Control-Max-Age: 86400
    response:
      - name: wrap_pagination
        condition: response_headers contains "X-Total-Count"
        body_transform:
          wrap_under: "data"
          add_meta:
            page: "{request.query.page | default: 1}"
            per_page: "{request.query.per_page | default: 25}"
            total: "{response.header.X-Total-Count}"
            pages: "{ceil(total / per_page)}"
      - name: standard_error_envelope
        condition: status_code >= 400
        body_transform:
          wrap_under: "error"
          add_fields:
            code: "{status_code}"
            request_id: "{response.header.X-Request-Id}"
            timestamp: "{now_iso}"
      - name: compress_large_responses
        condition: response_body_size > 10240
        header:
          Content-Encoding: gzip
        body: gzip(response_body)
==============================================================================
3. API KEY MANAGEMENT & ROTATION
==============================================================================
gateway:
  api_key_management:
    key_format: "sk_gw_{prefix}_{suffix}"
    prefix_length: 8
    suffix_length: 32
    entropy_source: os.urandom
    hash_storage: sha256_bcrypt
    rotation:
      policy: monthly
      grace_period_days: 7
      overlapping_keys: 2
        - current: active for all requests
        - previous: active for legacy clients, rotates out after grace
    endpoints:
      create:
        method: POST
        path: /api/v1/keys
        auth: admin_only
        body:
          tier: pro
          label: "forge-ci-key"
      revoke:
        method: DELETE
        path: /api/v1/keys/{key_prefix}
        auth: admin_or_owner
        action: insta_revoke_with_zero_ttl_cache_bust
      list:
        method: GET
        path: /api/v1/keys
        auth: admin_or_owner
        response:
          - key_prefix
          - label
          - tier
          - created_at
          - expires_at
          - last_used_at
    cache:
      engine: redis
      ttl: 300s
      negative_ttl: 30s
      stale_while_revalidate: 60s
    rate_limit_based_on_key: true
    enforce_key_expiry: true
    auto_renew_within_days: 3
==============================================================================
4. API VERSIONING AT GATEWAY LEVEL
==============================================================================
gateway:
  versioning:
    strategy: url_path_prefix
    pattern: /api/v{major}/
    versions:
      v1:
        status: active
        upstream_root: http://localhost:8100
        sunset_date: null
      v2:
        status: beta
        upstream_root: http://localhost:8200
        sunset_date: 2026-09-01
        gradual_rollout:
          percentage: 10
          match_header: X-Canary: true
    content_negotiation:
      accept_header: "application/vnd.styde.v{major}+json"
      preference: header_overrides_path
      fallback: latest
    backward_compat:
      - endpoint: /api/v1/eval
        v2_migration_map:
          /evaluate -> /eval
          body.field: results -> body.field: outputs
        compat_layer: enabled
      - endpoint: /api/v1/forge/status
        dropped_in_v2_reason: "replaced by /api/v2/forge/sessions"
    deprecation_headers:
      Warn: "299 - /api/v1 will be removed on 2026-09-01"
      Sunset: "Sat, 01 Sep 2026 00:00:00 GMT"
      X-Deprecated: "true" (only for v1)
    legacy_redirect:
      from: /api/{version_not_specified}
      to: /api/v1/{path}
      status: 307
==============================================================================
5. GATEWAY-LEVEL ANALYTICS & MONITORING
==============================================================================
gateway:
  monitoring:
    logs:
      access_log:
        format: json
        fields:
          - request_id
          - client_ip (anonymized: first 3 octets)
          - method
          - path (sanitized: no query strings with tokens)
          - status_code
          - response_time_ms
          - upstream_latency_ms
          - bytes_sent
          - tier
          - api_key_prefix (last 4 chars)
        backend: fluentd -> elasticsearch
      error_log:
        level: warn
        sinks:
          - stdout
          - file: /var/log/gateway/error.log
          - external: sentry.io
    metrics:
      format: prometheus
      path: /metrics
      port: 9091
      labels:
        - endpoint
        - method
        - status_class (2xx, 4xx, 5xx)
        - tier
        - version
      counters:
        - name: gateway_requests_total
        - name: gateway_rate_limited_total
        - name: gateway_auth_failed_total
        - name: gateway_upstream_errors_total
      histograms:
        - name: gateway_response_duration_seconds
          buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
        - name: gateway_upstream_duration_seconds
          buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
      gauges:
        - name: gateway_active_connections
        - name: gateway_upstream_health
          labels: [upstream]
    dashboards:
      tool: grafana
      datasource: prometheus
      panels:
        - title: Requests per second
          metric: rate(gateway_requests_total[1m])
          type: timeseries
        - title: P50/P95/P99 latency
          metric: gateway_response_duration_seconds
          type: heatmap
        - title: Rate limited requests
          metric: rate(gateway_rate_limited_total[1m])
          type: timeseries
        - title: Upstream health
          metric: gateway_upstream_health
          type: stat
        - title: Error rate by endpoint
          metric: rate(gateway_requests_total{status_class="5xx"}[5m])
          type: bar
        - title: Tier distribution
          metric: gateway_requests_total
          type: pie
    alerts:
      rules:
        - name: high_error_rate
          condition: rate(gateway_upstream_errors_total[5m]) > 0.05
          severity: critical
          channel: pagerduty
        - name: rate_limiting_spike
          condition: rate(gateway_rate_limited_total[1m]) > 100
          severity: warning
          channel: slack
        - name: p99_latency_breach
          condition: gateway_response_duration_seconds{p99} > 5.0
          severity: warning
          channel: slack
        - name: upstream_down
          condition: gateway_upstream_health < 1
          severity: critical
          channel: pagerduty
==============================================================================
DEPLOYMENT CONFIG
==============================================================================
gateway:
  engine: kong
  database: postgresql (declarative, no db mode)
  config_file: /etc/kong/kong.yml
  plugins:
    - rate-limiting
    - rate-limiting-advanced (for sliding window)
    - request-transformer
    - response-transformer
    - key-auth
    - ip-restriction
    - acl
    - prometheus
    - file-log
    - correlation-id
    - proxy-cache
  deployment:
    replicas: 2
    health_check:
      path: /status
      interval: 10s
      unhealthy_threshold: 3
    tls:
      cert: /etc/kong/tls/fullchain.pem
      key: /etc/kong/tls/privkey.pem
      protocols: [TLSv1.3, TLSv1.2]
  upstreams:
    - name: forge
      host: forge.styde.internal
      port: 8100
      healthcheck:
        path: /health
      circuit_breaker:
        max_fails: 5
        timeout: 30s
    - name: agent
      host: agent.styde.internal
      port: 8200
    - name: eval
      host: eval.styde.internal
      port: 8300
==============================================================================
Gateway Zero delivers Kong-based API gateway with sliding window rate limiting
per tier, request/response transforms that strip auth and normalize payloads,
SHA256-bcrypt hashed API keys with monthly rotation and 7-day grace, URL-path
versioning with canary rollouts and deprecation headers, and Prometheus metrics
for Grafana dashboards with alerting to PagerDuty and Slack.
==============================================================================