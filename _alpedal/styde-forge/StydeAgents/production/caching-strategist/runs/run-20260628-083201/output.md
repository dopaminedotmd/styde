skill: Caching Strategist
domain: backend
version: 1
scenario: you run a stock API serving 5000 req/s. database queries cost 200ms. users tolerate 50ms p95.
solution:
layer 1: browser cache
  Cache-Control: public, max-age=60, stale-while-revalidate=300
  covers repeat requests from same user. zero cost.
layer 2: CDN (CloudFront / Fastly)
  TTL: 60s for prices, 300s for metadata
  purge-on-write via AWS Lambda@Edge / Fastly surrogate key purge
  origins see only cache-miss traffic (~2% of total)
layer 3: Redis (cache-aside with stampede protection)
  pattern: cache-aside + mutex lock on miss
  TTL: 120s base, with jitter (TTL = 120 + rand(0,30))
  locking: SET NX EX 5 on cache miss, double-check after lock acquired
  prevents stampede: only one worker recomputes, rest wait for lock or serve stale
layer 4: write-through for mutable data
  on update: write DB, write Redis, purge CDN key
  consistency: eventual in ~5s for CDN, immediate for Redis
invalidation strategy:
  key format: stock:{symbol}:{type}:{version}
  version bump on schema change -> instant global invalidation
  zset-based invalidation log for async purge workers
circuit breakers:
  if Redis latency > 10ms, fall through to DB (degraded path)
  if Redis down entirely, serve CDN stale + queue repopulate
metrics to monitor:
  hit ratio: target > 90%
  p99 latency: target < 30ms
  stale serve ratio: target < 1%
  stampede events: target 0
this stack handles 5000 req/s on a single Redis 6GB instance and one CDN distribution.