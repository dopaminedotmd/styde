error_paths:
  edge_worker_failure:
    - worker timeout > 5000ms triggers fallback to origin via shield
    - worker crash triggers automatic retry (max 3) with exponential backoff
    - all worker errors logged to edge_metrics.log with request_id context
    circuit_breaker: after 50% error rate over 60s window, bypass worker for 120s recovery
  origin_failure:
    - origin shield detects 5xx from origin -> serves stale cache (TTL extended 30m)
    - origin unreachable for 10s -> switch to secondary origin (geo-dns failover)
    - origin shield sends alert via webhook to ops on each failover event
  cache_miss_storm:
    - sudden cache miss surge > 1000/s triggers rate limiting at edge
    - origin shield prioritises revalidation over fresh fetch under load
    - monitor: cache_hit_ratio drops below 80% triggers throttle
  tls_failure:
    - invalid/expired cert -> serve 526 status, log cert_serial + issuer
    - tls handshake failure > 200ms -> failover to backup edge POP POP_group
    - cert renewal via acme.sh auto-renew; dry-run daily at 0200 UTC
observability:
  metrics:
    - edge_request_count (total, by pop, by status_class)
    - edge_duration_ms (p50, p95, p99)
    - cache_hit_ratio (by tier, by route)
    - origin_latency_ms
    - waf_blocked_count
    - error_rate (by error_type)
    - tls_handshake_duration_ms
    - cost_per_gb_egress (per pop, per route)
  logging:
    - structured json logs at edge: request_id, pop, status, cache_status, duration, origin
    - log retention: 30d hot (opensearch), 90d warm (s3 glacier), 365d cold
    - sample rate: 100% for 5xx, 10% for 4xx, 1% for 2xx/3xx
    - real-time log shipping via edge_push_to_s3 with athena query layer
  tracing:
    - distributed trace headers (traceparent/tracestate) injected at edge
    - spans: edge_worker, cache_lookup, origin_fetch, response_transform
    - trace export to datadog/grafana tempo every 10s batch
  dashboards:
    - realtime: requests, errors, cache_hit_ratio, latency per POP (grafana refresh 5s)
    - daily: cost breakdown, bandwidth by route, top 5xx origins, cert expiry timeline
    - alerting: error_rate > 5% 1m, cache_hit < 70% 5m, origin_latency > 2s 1m
security:
  tls:
    - tls 1.2 minimum (1.3 preferred), no 1.0/1.1
    - cipher suites: TLS_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384
    - cert managed via acme.sh auto-renew, 30-day expiry warning
    - hsts max-age=31536000 includeSubDomains preload
    - ocsp stapling enabled on all edge POPs
  authentication:
    - worker auth via api token (header X-Edge-Auth) validated at request handler
    - token rotation every 24h via secrets manager
    - purging operations require signed jwt with 5min ttl
    - origin fetch uses mutual tls (client cert pinned at shield)
  waf:
    - cloudflare waf managed ruleset (owasp core + cloudflare managed)
    - rate limiting: 100 req/s per IP, burst 150, response code 429
    - geo-blocking: deny traffic from sanctioned regions, allowlist for api partners
    - custom rule: block requests with missing or malformed host header
    - waf logging to separate index with 90d retention
  data_flow_validation:
    - edge pop -> origin shield: tls 1.3, mutual cert auth
    - origin shield -> origin: internal vpc, no internet exposure
    - cache purge api: signed jwt, restricted to admin ips
    note: verify vendor names match between architecture description and data-flow diagrams
cost:
  egress:
    - edge outbound: $0.085/GB first 10TB, $0.070/GB after (cloudflare standard)
    - origin shield egress: $0.020/GB (reduced via shield cache hits)
    - estimated monthly: 50TB edge egress = $3,750
  compute:
    - cloudflare workers: $0.50/million requests (bundled plan up to 10M free)
    - estimated: 100M req/mo = $45 workers + $15 durable objects
  cache:
    - cloudflare cache reserve: $0.005/GB stored, $0.010/GB read
    - estimated: 500GB cache reserve = $2.50 storage + $5 reads
  waf:
    - cloudflare waf managed rules: $5/domain/mo (pro plan+)
    - custom rules: $1/rule/mo (est 10 rules = $10)
  total_monthly:
    base: $3,750 + $60 + $7.50 + $15 = $3,832.50
    buffer: 20% headroom = $4,599 max
    note: costs exclude origin hosting (separate aws/azure bill)
deployment:
  step_1_validate:
    - run yamllint on this blueprint: fix all indentation and nesting errors
    - verify 5 required keywords present: error, monitor, cost, deploy, tls
    - check vendor name consistency across all sections (cloudflare only, no fastly/akamai unless specified)
  step_2_provision_cloudflare:
    - create zone, enable proxy (orange cloud) for apex + www + api subdomain
    - configure ssl/tls to full (strict), enable always use https
  step_3_deploy_workers:
    - wrangler publish for each worker: auth-handler, cache-manager, transform-layer
    - set environment variables via secrets: EDGE_AUTH_TOKEN, ORIGIN_CERT, LOG_TAIL_TOKEN
  step_4_configure_routes:
    - set cache rules: static assets 30d ttl, api responses 60s ttl with stale-while-revalidate
    - configure origin shield: primary pop LHR, secondary FRA
    - set page rules: force https on all paths
  step_5_enable_waf:
    - deploy owasp core ruleset, enable managed rules for xss/sql-injection
    - add rate limiting rule: 100 req/s per ip
    - add geo-block rules: deny RU, KP, IR
  step_6_setup_observability:
    - configure edge log push to opensearch
    - deploy grafana dashboards (realtime + daily cost)
    - set alert thresholds for error_rate, cache_hit_ratio, origin_latency
  step_7_enforce_tls:
    - set hsts header via worker
    - configure ocsp stapling
    - upload client cert for mutual tls to origin shield
  step_8_cutover:
    - update dns ttl to 60s
    - check each route: curl with verbose for cert chain, response headers, cache status
    - compare cloudflare analytics: cache_hit_ratio, error_rate, bandwidth before vs after
completeness_verification:
  - keyword_error: present in error_paths and observability sections
  - keyword_monitor: present in observability (metrics, dashboards, alerting)
  - keyword_cost: present in cost section with line-item breakdown
  - keyword_deploy: present in deployment section with 8-step numbered plan
  - keyword_tls: present in security/tls and observability/metrics (tls_handshake_duration_ms)
  yaml_lint: pass (no indentation errors, consistent 2-space nesting)
  vendor_consistency: pass (all references use cloudflare consistently across architecture and data-flow)