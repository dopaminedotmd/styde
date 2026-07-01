cdn-edge-architect-blueprint
architecture:
  edge-compute: cloudflare-workers
  cdn-tier: multi-region-pull
  origin-shield: regional-tier
  dns-routing: geo-latency-based
  cache-strategy: stale-while-revalidate
component-design:
  worker-routes:
    - path: /api/*
      compute: cloudflare-worker
      memory: 128mb
      timeout: 30s
      cache-ttl: 60s
    - path: /static/*
      compute: none
      cache-ttl: 31536000s
      cache-control: immutable
    - path: /auth/*
      compute: lambda-edge
      memory: 256mb
      timeout: 5s
  cache-hierarchy:
    tier-1: browser-cache (private, max-age)
    tier-2: pop-cache (shared, stale-while-revalidate)
    tier-3: regional-hub (origin-shield, 2x pop-ttl)
    tier-4: origin (no-cache, bypass for writes)
data-flow:
  request: dns -> cloudfront/cloudflare -> pop-cache -> worker/lambda -> origin-shield -> origin
  cache-hit: pop returns cached response, header age-checked
  cache-miss: pop requests origin-shield, origin-shield coalesces concurrent requests
  purge: surrogate-key based, instant invalidation on cache-tags
api-surface:
  worker-api:
    endpoint: /purge
    method: POST
    auth: internal-hmac
    payload: {tags: [string], urls: [string]}
  origin-api:
    endpoint: /waf/rules
    method: PUT
    auth: bearer-token
    payload: {rule-id: string, action: block|challenge|allow}
waf-config:
  rate-limit: 1000rpm per-ip
  challenge-threshold: 100rpm per-ip
  block-rules:
    - known-bots (user-agent blocklist)
    - sql-injection patterns
    - path-traversal patterns
  geo-filter: allowlist only (production regions)
origin-optimization:
  shield-regions: us-east-1, eu-west-1, ap-southeast-1
  shield-ttl-multiplier: 2
  connection-keepalive: 60s
  load-balancer: round-robin with least-connections fallback
  health-check: /health endpoint, 5s interval, 2 failures to drain