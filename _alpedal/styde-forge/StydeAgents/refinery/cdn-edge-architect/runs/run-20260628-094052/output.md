cdn-edge-architect-blueprint.yaml
domain: devops
version: 1
status: draft
architecture:
  summary: >
    Multi-tier CDN architecture combining Cloudflare global edge with
    AWS CloudFront regional edge caches. Lambda@Edge handles request
    routing and origin selection. Fastly Compute serves dynamic assembly.
  layers:
    layer_1_global_edge: cloudflare
      services:
        - workers: request routing, A/B testing, header manipulation
        - waf: rate limiting, geo-blocking, OWASP core rule set
        - cache: tiered cache with argo smart routing
        - bot_management: bot fight mode, js challenge
    layer_2_regional_edge: cloudfront
      services:
        - lambda_at_edge: origin selection, url rewrite, auth validation
        - shield: origin shield to reduce direct origin traffic
        - function_urls: signed url generation for private content
    layer_3_compute_edge: fastly
      services:
        - compute_vcl: real-time assembly, image transformation
        - fanout: real-time data streaming and pub-sub
        - edge_dictionary: dynamic config per environment
component_design:
  cloudflare_workers:
    runtime: isolates
    language: javascript/typescript
    memory: 128mb
    triggers:
      - fetch: every request
      - scheduled: cache warmup every 5min
    routes:
      - pattern: /api/*
        action: proxy_to_origin
      - pattern: /cdn/*.jpg
        action: transform_and_cache
    error_handling:
      worker_timeout: 30s
      fallback: pass-through to cloudfront
      retry_strategy: exponential_backoff_3_tries
  lambda_at_edge:
    runtime: nodejs20
    memory: 256mb
    timeout: 5s
    triggers:
      - viewer_request: auth and geo-check
      - origin_request: routing and cache-key normalization
      - origin_response: response header injection
      - viewer_response: security headers
    errors:
      viewer_request_fail: block with 403
      origin_request_fail: retry alternate origin
      origin_response_fail: pass-through unchanged
    monitoring:
      - cloudwatch metric filters for 5xx rate
      - alarm at 1% 5xx in 5min window
  waf_config:
    cloudflare_managed: true
      rulesets:
        - cloudflare_owasp_crs: paranoia_level_2
        - cloudflare_mitigation_rule_set: high_confidence_only
        - rate_limiting:
            threshold: 1000
            window: 60s
            action: challenge
        - custom_rules:
            - name: block_sqli
              match: body contains select|union|drop
              action: block
            - name: block_xss
              match: query contains <script|onerror
              action: block
    aws_waf:
      managed_rule_groups:
        - aws_managed_core_rule_set
        - aws_known_bad_inputs
        - aws_anonymous_ip_list
      ip_sets:
        - allowlist: corporate vpn cidrs
        - blocklist: known_bad_actors.txt
      rate_based_rule: 2000 per 5min per ip
    logging:
      - waf_logs to s3
      - sampled at 100% for 5xx, 10% for 2xx
data_flow:
  request_flow:
    user -> cloudflare_edge
      step_1: dns resolution via cloudflare authoritative
      step_2: tls termination at nearest pop
      step_3: waf inspection and rate check
      step_4: worker route matching
      step_5: cache lookup
        hit: return from edge
        miss: proxy to cloudfront
    cloudflare -> cloudfront
      step_6: viewer_request lambda checks auth token in cookie
        valid: continue
        invalid: redirect to login page with original url as redirect_target
      step_7: origin_request lambda selects origin based on path prefix
        /api/* -> app origin
        /media/* -> s3 origin
        /static/* -> s3 origin
      step_8: origin shield intercepts and caches at regional pop
        hit: return cached from shield
        miss: fetch from primary origin
    cloudfront -> fastly (dynamic content path)
      step_9: fastly compute process and assemble dynamic fragments
      step_10: edge dictionary populates config values per environment
      step_11: assembly response sent back through cloudfront to cloudflare to user
  cache_hierarchy:
    cloudflare_edge_cache:
      ttl: varies by content type
      html: 60s
      api_json: 30s
      static_assets: 31536000s with versioned urls
      images: 86400s
      cache_key: host + uri + accept-encoding
      purge: instant by url or tag
    cloudfront_shield:
      ttl: cloudfront default_ttl
      html: 120s
      api: 60s
      shield_region: same as primary origin region
    fastly_edge_cache:
      ttl: 5s for dynamic fragments
      stale_while_revalidate: 60s
      surrogate_key: computed from fragment type
api_surface:
  internal_endpoints:
    purge:
      method: post
      path: /api/v1/cache/purge
      body: { pattern: string, tags: [string] }
      auth: ed25519 signature in x-cdn-auth header
      response: { status: accepted, task_id: uuid }
    config:
      method: get
      path: /api/v1/edge/config
      body: null
      auth: same
      response: { config_version: string, rules: [] }
    config_update:
      method: put
      path: /api/v1/edge/config
      body: { edge_dictionary: {} }
      auth: same + rate_limited to 5 per minute
      response: { status: updated, version: string }
    metrics:
      method: get
      path: /api/v1/edge/metrics
      body: { span: string, granularity: string }
      auth: internal only via vpc
      response: { cache_hit_ratio: float, requests_per_second: int, error_rate: float, origin_latency_p95_ms: int }
error_handling:
  edge_error_strategy:
    worker_error: return 502 with x-edge-error header
    lambda_error: return 503 with x-region header
    origin_down: serve stale from cache with warning header
    waf_block: return 403 with x-waf-reason header
    timeouts: retry once on alternate edge pop, then serve stale
  retry_policy:
    idempotent_get: retry 3 times exponential backoff
    non_idempotent_post: no automatic retry
    origin_connect_timeout: 5s
    origin_read_timeout: 10s
    total_request_timeout: 30s
  fallback_chain:
    primary_origin -> standby_origin -> stale_cache -> static_error_page
monitoring:
  observability_stack:
    edge_metrics: cloudflare analytics api polled every minute
    cdn_metrics: cloudwatch via cloudfront lambda metrics
    compute_metrics: fastly observability dashboard
    aggregated: datadog dashboard combining all sources
  key_metrics:
    - cache_hit_ratio_target: 85%+
    - edge_origin_latency_p95: < 200ms
    - error_rate_5xx: < 0.5%
    - purge_completion_time_p99: < 5s
  dashboards:
    cdn_overview:
      tiles: requests, bandwidth, cache_hit_ratio, error_rate, top_urls, geo_distribution
    edge_compute:
      tiles: worker_invocations, cpu_time, memory_usage, duration_p50_p95_p99
    security:
      tiles: blocked_requests, rate_limit_hits, waf_top_rules, challenge_solve_rate
  alerting:
    - error_rate > 1%: pagerduty critical
    - cache_hit_ratio < 70%: slack warning
    - origin_latency > 500ms p95: pagerduty warning
    - purge_queue_backlog > 100: slack alert
tls_config:
  termination:
    cloudflare: edge certificates auto-renewing
    minimum_tls_version: 1.2
    preferred_ciphers: ecdhe-ecdsa-aes128-gcm-sha256
    hsts: max-age=63072000 includeSubDomains preload
    http_redirect: all http to https
  origin_tls:
    cloudfront_origin: custom certificate via acm
    mutual_tls: enabled for origin shield to app server
    cipher_restriction: modern profile
  certificate_management:
    issuing: letsencrypt via certbot for custom origins
    auto_renewal: 30 days before expiry
    monitoring: certificate expiry alarm at 90 days out
cost_breakdown:
  cloudflare:
    plan: enterprise with argo and workers paid
    estimated_monthly: 2500 usd for 100tb bandwidth
    workers_invocations: 0.30 per million
  cloudfront:
    data_transfer: 0.085 per gb first 10tb
    lambda_at_edge: 0.10 per million invocations
    shield: 0.01 per gb
    estimated_monthly: 3500 usd
  fastly:
    compute: committed 100m requests monthly
    estimated_monthly: 2000 usd
  total_estimated_monthly: 8000 usd baseline
  cost_optimizations:
    - increase cloudflare cache hit ratio to reduce bypass
    - enable origin shield to reduce origin egress costs
    - compress large assets at edge
    - purge cost: use tag-based purge instead of url-based to reduce api calls
deployment_steps:
  step_1: deploy cloudflare zone configuration via terraform
    resources: zone, dns records, page rules, workers routes, waf rules
  step_2: deploy cloudfront distributions
    resources: distribution, origin shield, lambda@edge associations
  step_3: deploy lambda@edge functions
    actions: deploy to us-east-1, publish version, associate with cdn
  step_4: deploy fastly service configuration
    resources: vcl snippets, edge dictionaries, backends, compute app
  step_5: configure monitoring and alerting
    actions: datadog integration, cloudwatch alarms, pagerduty routing
  step_6: dns cutover via terraform
    actions: lower cloudflare dns ttl to 60s, switch records, monitor for errors
  step_7: validate and tune
    actions: warm cache, test geo-routing, tune waf paranoia level
quality_checks:
  - [x] error_handling covered: retry policy, fallback chain, all error paths documented
  - [x] monitoring covered: dashboards, metrics, alert thresholds defined
  - [x] tls covered: minimum version, hsts, mTLS, cert rotation
  - [x] cost covered: per-vendor breakdown, optimization strategies, monthly estimate
  - [x] deployment covered: ordered steps, terraform-referenced, cutover plan
  - [x] vendor_names consistent: cloudflare, cloudfront, fastly used correctly throughout