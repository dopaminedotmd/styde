name: api-gateway-design
version: 1.0
domain: backend
gateway:
  provider: kong
  version: 3.x
  deployment:
    topology:
      mode: hybrid
      control_plane:
        count: 2
        placement: multi-az
        database: postgresql
      data_plane:
        count: 4
        placement: multi-region
        auto_scaling:
          min: 2
          max: 10
          metric: cpu_utilization
          threshold: 70
    ingress:
      protocol: https
      tls_termination: data_plane
      tls_certificate: letsencrypt
      tls_renewal: automated
rate_limiting:
  strategy: sliding_window
  default:
    requests: 1000
    period: 60s
  tiers:
    - name: free
      requests: 10
      period: 60s
      burst: 5
    - name: basic
      requests: 100
      period: 60s
      burst: 20
    - name: premium
      requests: 1000
      period: 60s
      burst: 100
  error_response:
    status: 429
    headers:
      retry_after: true
      rate_limit_remaining: true
      rate_limit_reset: true
authentication:
  primary: oauth2
  provider: auth0
  flows:
    - authorization_code
    - client_credentials
  secondary: jwt
  jwt_issuer: https://auth.example.com
  jwt_algorithm: RS256
  api_key_header: X-API-Key
  api_key_location: header
  api_key_rotation_days: 90
tls:
  termination_point: data_plane
  minimum_version: 1.3
  cipher_suites:
    - TLS_AES_256_GCM_SHA384
    - TLS_CHACHA20_POLY1305_SHA256
  hsts:
    enabled: true
    max_age: 31536000
secret_storage:
  provider: vault
  backend: aws_sm
  rotation:
    api_keys: 90d
    jwt_signing: 180d
    database_credentials: 30d
  encryption_at_rest: aes256
request_transformation:
  strip_prefix: true
  plugins:
    - name: request-transformer
      add_headers:
        - X-Forwarded-For
        - X-Request-Id
        - X-Gateway-Version
    - name: cors
      origins:
        - https://app.example.com
      methods:
        - GET
        - POST
        - PUT
        - DELETE
      headers:
        - Authorization
        - Content-Type
      credentials: true
api_versioning:
  strategy: url_prefix
  format: /v{major}
  header_override: Accept-Version
  backwards_compatible: true
  sunset_period_days: 180
  default_version: v1
monitoring:
  metrics:
    - request_count
    - latency_p50
    - latency_p95
    - latency_p99
    - error_rate
    - rate_limit_hits
  logging:
    access_logs: structured_json
    log_level: warn
    retention_days: 90
  alerts:
    - condition: error_rate > 5
      channel: pagerduty
      priority: critical
    - condition: latency_p99 > 2000
      channel: slack
      priority: high
    - condition: rate_limit_hits > 100
      channel: email
      priority: medium
rate_limiting applied. Transform configured. Key rotation set to 90 days. Versioning active at /v{major}. Monitoring pipeline deployed with alerting.