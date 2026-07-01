description: |
  Evaluate CDN edge architecture for a global web application requiring low-latency delivery across North America, Europe, and Asia-Pacific. Assess Cloudflare Workers for edge compute, Fastly for cache tiering, and Lambda@Edge for request routing.
artifacts:
  - cdn-comparison-matrix.md
  - edge-worker-implementation.js
  - caching-strategy-diagram.md
tags:
  - cdn
  - edge-compute
  - cloudflare-workers
  - fastly
  - lambda-edge
  - caching
  - waf
inputs:
  origin_domains:
    - api.example.com
    - www.example.com
    - static.example.com
  traffic_estimates:
    monthly_requests: 500000000
    global_regions:
      - na
      - eu
      - apac
    peak_rps: 25000
  security_requirements:
    - waf
    - ddos-protection
    - bot-management
methods:
  verify-hard-numbers:
    do_not_hand_write_yaml_keys: true
    use_exact_key_value_format_from_schema: true
    validation:
      - compare published edgelist against observed traceroute paths
      - confirm cache hit ratio claims against origin access logs
      - verify latency percentiles with synthetic probes every 5 minutes
    yaml_lint_pass:
      before_final_output: true
      validator: yaml.safe_load()
      on_error: reject and regenerate with syntax corrections
outputs:
  domain_provider_table:
    domain: api.example.com
    recommended_provider: cloudflare
    service: workers + cache
    confidence: 0.92
    rationale: existing dns, built-in ddos, fastest ttfw in na/eu
    domain: static.example.com
    recommended_provider: fastly
    service: object-storage-origin shield
    confidence: 0.88
    rationale: highest cache-hit ratio for immutable assets, purging api
    domain: www.example.com
    recommended_provider: lambda-edge
    service: origin-shield + request-routing
    confidence: 0.85
    rationale: aws-native, low-latency failover, custom routing at edge
  required_output_fields:
    - domain
    - recommended_provider
    - service
    - confidence
    - rationale
workedexample:
  scenario: Evaluate cdn for video-streaming platform with 2 billion monthly requests
  domains:
    - vod.cdn.example.com
    - live.cdn.example.com
    - api.cdn.example.com
  validation_steps:
    1. run yaml.safe_load() on output before delivery
    2. compare published pop count against real traceroute data
    3. verify cache hit ratio against sample origin logs
    4. confirm latency p95 with 24-hour synthetic probe run
  output_sample:
    domain: vod.cdn.example.com
    recommended_provider: fastly
    service: vod-origin-shield-plus-cache
    confidence: 0.94
    rationale: fastly edge-compute for manifest transformation, highest throughput
    domain: live.cdn.example.com
    recommended_provider: cloudflare
    service: workers-hls-repackage
    confidence: 0.90
    rationale: real-time stream repackaging at edge, global anycast
    domain: api.cdn.example.com
    recommended_provider: lambda-edge
    service: geo-routing-plus-auth
    confidence: 0.87
    rationale: aws-native, best latency inside us-east-1, custom auth logic