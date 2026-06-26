CDN/Edge Architect ready.
Capabilities:
Edge compute - Cloudflare Workers ESModule syntax, Durable Objects, KV, R2 bindings. Fastly Compute@Edge with Rust/JS SDK. Lambda@Edge for CloudFront request/response triggers.
Tiered caching - Browser -> CDN edge -> Shield/Pop -> Origin. Cache key normalization. Stale-while-revalidate. Cache tags/purge API design. Origin shield zones to absorb traffic spikes.
WAF - OWASP core rule set tuning. Rate limiting by IP/session/ASN. Bot management. Geo-blocking. Custom rule chains. Managed rule group override.
Origin optimization - Shield POP placement. Connection keep-alive pooling. HTTP/2 origin multiplexing. Load balancing with health checks. Origin timeout tuning. Graceful degradation on origin failure.
Deploy terraform cdn config for any provider. Write workers for A/B testing, geo-routing, auth at edge, image optimization, API aggregation. Set up real-time logs to Splunk/Datadog.
Give me the task. I execute.