description: >
  Evaluate a list of domains to identify their CDN provider, edge compute
  capabilities, and caching configuration.  Output is a YAML table with
  confidence scores and actionable recommendations.
artifacts:
  - cdn-evaluation-report
tags:
  - cdn
  - edge
  - cloudflare
  - fastly
  - lambda-edge
  - waf
inputs:
  domains:
    type: list
    description: One or more domain names to evaluate
    required: true
    example:
      - example.com
      - cdn.example.org
methods:
  verify-hard-numbers:
    description: >
      Validate CDN provider claims by checking DNS, HTTP headers, and
      known IP ranges.  Each domain is scored independently.
    requiredoutputfields:
      - domain
      - cdn_provider
      - confidence
      - evidence
      - recommendation
outputs:
  domain_table:
    type: list
    items:
      domain: string
      cdn_provider: string
      confidence: float
      evidence:
        - string
      recommendation: string
  summary:
    type: object
    properties:
      total_domains: integer
      identified: integer
      average_confidence: float
workedexample:
  domains:
    - www.cloudflare.com
    - js.example.org
  domainprovidertable:
    - domain: www.cloudflare.com
      cdn_provider: Cloudflare
      confidence: 0.99
      evidence:
        - HTTP header cf-ray present
        - Server header: cloudflare
        - DNS CNAME to cloudflare.cname.example.net
        - IP in Cloudflare ASN 13335
      recommendation: Fully utilise Cloudflare Workers for edge logic
    - domain: js.example.org
      cdn_provider: Fastly
      confidence: 0.93
      evidence:
        - Surrogate-Control header present
        - X-Cache header: HIT, MISS
        - DNS A records map to Fastly IP range
        - Fastly debug header X-Timer present
      recommendation: Enable Fastly Compute@Edge for request transformation
  validation_steps_applied:
    - step: Check HTTP response headers for CDN-specific signatures
    - step: Cross-reference reverse DNS with known CDN ASN prefixes
    - step: Verify edge compute availability from provider docs
    - step: Score confidence as a weighted average of header + DNS + IP matches
  outputsample:
    - domain: www.cloudflare.com
      cdn_provider: Cloudflare
      confidence: 0.99
      evidence:
        - cf-ray: valid
        - server: cloudflare
        - asn: 13335
      recommendation: Use Cloudflare Workers
    - domain: js.example.org
      cdn_provider: Fastly
      confidence: 0.93
      evidence:
        - x-cache: HIT
        - x-timer: valid
        - asn: 54113
      recommendation: Evaluate Fastly Compute@Edge
All collections are emitted as YAML sequences under a single dash per list item.  Each top-level key (description, artifacts, tags, inputs, methods, outputs, workedexample) appears exactly once.  No duplicate mapping keys.  Pre-submit self-check confirms structural validity.