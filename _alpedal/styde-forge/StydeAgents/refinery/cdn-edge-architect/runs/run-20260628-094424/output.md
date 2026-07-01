Blueprint: CDN Edge Architecture
Version: 1.0
Domain: devops
Target: Production-ready edge/CDN infrastructure
Assessment:
Requirements call for a globally distributed content delivery system with edge compute, caching hierarchy, and WAF. Solution must handle dynamic request routing at edge while maintaining sub-50ms P95 latency for cache hits.
Architecture Overview:
Edge Layer:
  Primary: Cloudflare Workers (800+ PoPs)
  Fallback: Lambda@Edge (for origin-facing transformations)
  DNS: Cloudflare for anycast routing
Cache Hierarchy:
  Tier 1: Browser cache (max-age headers, ETags)
  Tier 2: Cloudflare Edge Cache (ARL-aware, stale-while-revalidate)
  Tier 3: Cloudflare Tiered Cache Topology (top-level data centers)
  Tier 4: Origin Shield (regional集中 caching layer)
  Tier 5: Origin (load-balanced, multi-region)
Validation:
  yamllint -s infra/**/*.yaml  # Enforce strict indentation (2 spaces)
  cfmt -check configs/         # Cloudflare config validator
Edge Compute Implementation:
workflow CloudflareWorker:
  1. Request received at edge PoP
  2. Check cache: if hit AND fresh, return immediately
  3. If stale: serve stale while revalidating (stale-while-revalidate: 86400)
  4. Route to Tier 3 or origin shield based on request type
  5. Apply WAF rules before origin fetch
  6. Cache response with ARL-based TTL
worker main:
  import { getAssetFromKV } from '@cloudflare/kv-asset-handler'
  async function handleRequest(event) {
    const request = event.request
    const url = new URL(request.url)
    // WAF check at edge
    const wafResult = await checkWAF(request)
    if (!wafResult.allowed) {
      return new Response(JSON.stringify({ error: wafResult.reason }), {
        status: 403,
        headers: { 'content-type': 'application/json' }
      })
    }
    // Cache-first strategy
    const cacheKey = buildCacheKey(url)
    const cachedResponse = await caches.default.match(cacheKey)
    if (cachedResponse) {
      if (isFresh(cachedResponse)) return cachedResponse
      event.waitUntil(refreshCache(request, cacheKey))
      return cachedResponse  // stale-while-revalidate
    }
    // Route to origin shield
    const response = await fetch(url, {
      cf: {
        cacheTtl: calculateTTL(url),
        cacheKey,
        polish: 'lossy',
        mirage: true
      }
    })
    return response
}
Cache Hierarchy Configuration:
yaml
tiered_cache:
  enabled: true
  topology: smart  # Cloudflare automatically routes to parent cache
  cache_by_device_type: false
  cache_by_language: true
  cache_by_cookie: [session_id]
  default_ttl:
    static_assets: 31536000  # 1 year
    api_responses: 300       # 5 minutes
    html_pages: 600          # 10 minutes
  stale_while_revalidate: 86400  # serve stale for 24h during revalidation
  cache_reserve: true  # higher cache hit ratio at edge PoPs
origin_shield:
  enabled: true
  regions:
    - us-east
    - eu-west
    - ap-southeast
  min_file_size: 0
  max_file_size: 524288000  # 500MB
  cooldown_ttl: 3600
  shield_pop: auto  # Cloudflare picks nearest
waf:
  mode: log_for_first_hour  # learning mode
  rules:
    - name: block_tor_exit_nodes
      action: block
      priority: 1
      expression: '(ip.geoip.asnum eq 396982)'
    - name: rate_limit_api
      action: challenge
      priority: 2
      period: 60
      requests_threshold: 100
      expression: 'starts_with(http.request.uri.path, "/api/")'
    - name: sql_injection
      action: block
      priority: 3
      expression: 'any(waf.tags, http.request.body.raw matches ".*(union.*select|select.*from|drop.*table).*")'
    - name: xss
      action: block
      priority: 4
      expression: 'any(waf.tags, http.request.uri.query contains "<script")'
    - name: block_bad_bots
      action: block
      priority: 5
      expression: 'cf.client.bot'
lambda_at_edge:
  - function: origin-request-rewrite
    trigger: origin-request
    description: Rewrites S3 signed URLs and normalizes paths
    timeout: 5
    memory: 256
    runtime: nodejs20.x
  - function: origin-response-headers
    trigger: origin-response
    description: Adds security headers (HSTS, CSP, X-Frame-Options)
    timeout: 5
    memory: 128
    runtime: nodejs20.x
  - function: viewer-request-auth
    trigger: viewer-request
    description: JWT validation for authenticated content
    timeout: 5
    memory: 256
    runtime: nodejs20.x
Cost Complexity Tradeoff:
Cost comparison with baseline:
  Baseline option: Single-origin deployment behind Cloudflare Free plan
    Cost: $0/month (Cloudflare) + $50/month (single server)
    Latency: 150-300ms (no edge compute, no 分散 caching)
    Capacity: 10TB/month free bandwidth
    Limitation: no WAF, no edge compute, no tiered cache
  Selected option: Cloudflare Pro + Workers Unbound + Tiered Cache
    Cost: $200/month (Pro) + $5-10/month (Workers) + $0 (Tiered Cache included)
    Latency: 10-40ms cache hit, 80-150ms cache miss
    Capacity: Unlimited bandwidth
    Benefit: WAF included, 800+ PoPs, edge compute, tiered cache
  Lambda@Edge add-on:
    Cost: $0.60 per 1M requests + $0.00005 per 128MB-second
    Estimated monthly: $30-50 for 50M requests/month
    Alternative without Lambda: Pure Workers-based solution avoids Lambda costs
    Recommendation: Use Lambda only for S3 origin request rewriting (can't replace with Workers)
  Tradeoff rationale: $30-60/month premium buys 5-10x latency improvement, 99.99% availability SLA, built-in DDoS protection, and reduces origin load by 95%+. The jump from $0 to $60/month is justified by the capacity improvement from 10TB to unlimited bandwidth and the inclusion of managed WAF. For sites under 10TB/month with no auth requirements, baseline is sufficient.
Deployment Steps:
phase_1_foundation:
  - Register domain on Cloudflare (or transfer DNS)
  - Enable proxy on DNS records (orange cloud)
  - Configure SSL/TLS: Full (strict)
  - Verify SSL certificate issuance (15-30 min)
  yamllint configs/foundation.yaml  # validate before proceeding
phase_2_caching:
  - Enable Tiered Cache in Cloudflare dashboard
  - Configure Cache Rules:
    - Bypass cache on /admin/*, /checkout/*
    - Cache static extensions: css,js,png,jpg,svg,woff2,ttf
    - Edge TTL: 1 year for immutable assets
  - Enable Cache Reserve for cold-start optimization
  yamllint configs/cache.yaml
phase_3_waf:
  - Enable WAF (skip initial setup, use Learning Mode for 24h)
  - Review WAF events after 24h learning period
  - Deploy managed rulesets (OWASP, Cloudflare Managed)
  - Add custom rules per specification above
  - Set mode to High Security after false positive review
  yamllint configs/waf.yaml
phase_4_edge_workers:
  - Write and deploy Workers via wrangler deploy
  - Test in preview environment with sample traffic
  - Gradual rollout: 5% -> 25% -> 50% -> 100%
  - Monitor Worker CPU time and duration
  yamllint configs/workers.yaml
phase_5_lambda_edge:
  - Package Lambda functions with AWS SAM or CDK
  - Deploy to us-east-1 (required for CloudFront)
  - Associate with CloudFront distribution
  - Test each trigger type
  - Monitor errors, duration, throttles
  yamllint configs/lambda.yaml
phase_6_monitoring:
  - Set up Cloudflare Analytics dashboard
  - Configure alerts: cache ratio < 70%, error rate > 1%
  - Track metrics: cache hit ratio, origin bandwidth, WAF events, worker cpu
  - Budget alerts: worker invocation > 10M/month, bandwidth > 1TB/day
  - Health check endpoint: GET /health returns 200 with ok
  pattern: every 30 seconds from 3 regions
Error Handling:
  worker error catch:
    - Network error: retry with exponential backoff (3 attempts, 1s/2s/4s)
    - 502 from origin: serve stale cache if available, else 503 maintenance page
    - Worker timeout (30s limit): cede to origin, no edge processing
    - KV miss for asset handler: fallback to bucket origin
  origins:
    primary: https://origin.example.com
    fallback: https://fallback-origin.example.com
    health_check_interval: 30
    health_check_path: /health
    failover_threshold: 3 consecutive failures
Monitoring Events:
  events:
    - cache_hit_ratio_below_70:
        severity: warning
        action: review caching rules, check for uncacheable content
    - worker_error_rate_above_1_percent:
        severity: critical
        action: rollback worker to previous version, investigate error
    - waf_block_rate_surge:
        severity: info
        action: review WAF events, check for false positives
    - origin_latency_above_500ms:
        severity: warning
        action: scale origin, check origin shield health
    - monthly_cost_above_budget:
        severity: info
        action: review bandwidth usage, optimize cache TTLs
Expected Outcomes:
  cache_hit_ratio: 85-95% after 2 weeks warmup
  p95_latency_cache_hit: <30ms
  p95_latency_cache_miss: <150ms
  origin_offload: reduce origin bandwidth by 90%+
  waf_false_positive_rate: <0.1%
  uptime: 99.99% (Cloudflare SLA)
  monthly_cost: $50-100/month (Pro+Workers only) or $80-150/month (with Lambda@Edge)