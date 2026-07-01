api gateway design for microservices platform
gateway: kong
proxy: openresty 1.25
port: 8443
plugins: bundled + go
rate limiting
  strategy: sliding-window
  storage: redis cluster (6 nodes)
  defaults:
    public: 100/min burst=200
    authenticated: 1000/min burst=2000
    premium: 10000/min burst=20000
  per-route overrides:
    /v1/auth/login: 10/min burst=20
    /v1/payments/charge: 30/min burst=60
    /v1/webhook/*: 200/min burst=500
  per-consumer tiers:
    free: 1000/hour
    pro: 10000/hour
    enterprise: 100000/hour
  headers: X-RateLimit-Limit X-RateLimit-Remaining X-RateLimit-Reset Retry-After
request transformation
  strip prefix: /v1 /v2 /v3 -> /
  add headers: X-Gateway-Id X-Request-Id X-Forwarded-Proto
  modify:
    /v1/*: add X-Api-Version: v1
    /v2/*: add X-Api-Version: v2
  oauth client-id injection:
    source: X-Client-Id header
    target: X-Authenticated-Client header
    validate: regex [a-z0-9]{20,40}
  response transformations:
    strip: Server X-Powered-By X-Kong-Admin-Latency
    add: X-Response-Time X-Gateway-Cache-Status
    cors:
      origin: regex ^https://(app|admin|partner)\.example\.com$
      methods: GET POST PUT DELETE PATCH
      headers: Authorization Content-Type X-Client-Id X-Api-Key
      max-age: 86400
api key management
  generation: ed25519 keypair
  key format:
    live: sk_live_{random:48}
    test: sk_test_{random:48}
  hashing: sha256 + hmac with server secret
  rotation policy:
    active keys: 2 per consumer (current + grace)
    rotation window: 90 days
    grace period: 30 days
    revocation:
      immediate: security incidents
      scheduled: 30-day notice
    automated:
      notify: email + webhook 45 days before expiry
      regenerate: on request via POST /v1/keys/rotate
  key scopes:
    scope format: resource:action
    available: users:read users:write payments:read payments:write webhooks:read admin:*
    validation: checked per-route via Kong ACL plugin
  key endpoints:
    POST /v1/keys                   create new key
    GET /v1/keys                    list keys (masked)
    DELETE /v1/keys/{id}            revoke key
    POST /v1/keys/{id}/rotate       rotate to new key
api versioning
  strategy: url-prefix
  base: https://api.example.com
  active versions:
    v1: 2024-01-01 to 2024-12-31     fully deprecated
    v2: 2024-06-01 to present         stable
    v3: 2025-01-01 to present         current
  content-negotiation:
    accept-header: Accept: application/vnd.example.v3+json
    header priority: X-Api-Version > Accept header > URL prefix
    default version: v3
  version mapping:
    v1 upstream: backend-v1.internal:8080
    v2 upstream: backend-v2.internal:8080
    v3 upstream: backend-v3.internal:8080
  sunset header: Sunset: Sat, 31 Dec 2024 23:59:59 GMT (auto on v1)
  deprecation header: Deprecation: true (auto on v1)
  changelog auto:
    route /v3/changelog -> returns openapi diff vs v2
  migration docs:
    route /v3/migration-guide -> returns md rendered as html
gateway monitoring
  metrics backend: prometheus + grafana
  kong plugin: prometheus (bundled)
  key metrics:
    requests_per_second       by route+status+consumer
    p50_p95_p99_latency       by route+upstream
    error_rate_4xx_5xx        by route+status_code
    upstream_health           by target + circuit_breaker_state
    rate_limit_hits           by route+tier
    cache_hit_ratio           by route
    key_expiration_rate       by time window
  dashboards:
    gateway_overview: rps latency error_rate upstream_health
    per_route_analytics: traffic patterns error breakdown
    consumer_tiers: usage by tier active keys
    api_version_migration: traffic share v1/v2/v3 sunset countdown
  alerting:
    latency p99 > 2000ms       critical pager
    error_rate_5xx > 1%         critical pager
    rate_limit_drops > 5%       warning slack
    upstream_pool_empty         critical pager
    key_revocation_burst > 10/hr warning email
  logging:
    json structured
    fields: request_id client_id route method status latency upstream_bytes
    sample rate: 100% for 5xx 10% for 2xx 50% for 4xx
    sink: elasticsearch ILM 30-day retention
  health:
    GET /health                   gateway alive
    GET /health/upstreams         each upstream status
    GET /health/plugins           all plugin statuses