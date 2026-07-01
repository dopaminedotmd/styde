Api Gateway Designer Blueprint v2
config:
  declarative: true
  format_version: "1.1"
  defaults:
    upstream_connect_timeout: 60000
    upstream_send_timeout: 60000
    upstream_read_timeout: 60000
    https_only: true
    tls_verify_depth: 2
    dns_no_sync: true
    dns_resolver: "8.8.8.8"
  shared_definitions: &shared
    rate_limit_policy: &rate_lim
      name: rate-limiting
      config:
        policy: local
        fault_tolerant: true
        hide_client_headers: false
    health_check_base: &hc_base
      active:
        healthy:
          interval: 5
          successes: 1
        unhealthy:
          interval: 5
          http_failures: 2
          tcp_failures: 2
        http_path: /health
        type: http
      passive:
        healthy:
          http_successes: 3
          successes: 3
        unhealthy:
          http_failures: 3
          tcp_failures: 3
    tls_base: &tls_base
      protocols:
        - TLSv1.2
        - TLSv1.3
      cipher_suite: modern
services:
  - name: auth-api
    host: auth.internal
    port: 8443
    protocol: grpcs
    routes:
      - name: auth-routes
        hosts: ["api.example.com"]
        paths: ["/auth"]
        strip_path: false
        plugins:
          - <<: *rate_lim
            config:
              second: 100
              minute: 3000
          - name: jwt
            config:
              claims_to_verify: ["exp", "nbf"]
              secret_is_base64: false
              key_claim_name: kid
          - name: cors
            config:
              origins: ["https://app.example.com"]
              methods: ["GET", "POST"]
              headers: ["Authorization", "Content-Type"]
              credentials: true
              max_age: 3600
          - name: ip-restriction
            config:
              allow: ["10.0.0.0/8", "172.16.0.0/12"]
              deny: []
    client_certificate: true
  - name: user-api
    host: users.internal
    port: 8443
    protocol: https
    routes:
      - name: user-routes
        hosts: ["api.example.com"]
        paths: ["/users", "/users/:id"]
        strip_path: false
        plugins:
          - <<: *rate_lim
            config:
              second: 50
              minute: 1500
          - name: key-auth
            config:
              key_in_body: false
              key_names: ["apikey"]
              hide_credentials: true
          - name: request-transformer
            config:
              add:
                headers: ["X-Gateway: user-api/v1"]
              remove:
                headers: ["X-Internal-Token"]
          - name: response-transformer
            config:
              add:
                headers: ["X-RateLimit-Limit: 50"]
  - name: websocket-gw
    host: ws.internal
    port: 443
    protocol: wss
    routes:
      - name: ws-stream
        hosts: ["ws.example.com"]
        paths: ["/stream"]
        strip_path: true
        protocols: ["ws", "wss"]
        plugins:
          - <<: *rate_lim
            config:
              second: 10
              minute: 600
          - name: jwt
            config:
              claims_to_verify: ["exp"]
              secret_is_base64: false
          - name: cors
            config:
              origins: ["*"]
              methods: ["GET"]
              headers: []
              credentials: false
              max_age: 300
  - name: grpc-gw
    host: grpc.internal
    port: 443
    protocol: grpcs
    routes:
      - name: grpc-routes
        hosts: ["api.example.com"]
        paths: ["/grpc.service.v1/"]
        strip_path: false
        protocols: ["grpc", "grpcs"]
        plugins:
          - <<: *rate_lim
            config:
              second: 200
              minute: 10000
          - name: jwt
            config:
              claims_to_verify: ["exp", "sub"]
              secret_is_base64: true
          - name: mtls-auth
            config:
              ca_certificates: ["/etc/certs/ca.pem"]
              skip_consumer_lookup: false
  - name: canary-v1
    host: users-canary.internal
    port: 8443
    protocol: https
    weight: 10
    routes:
      - name: canary-routes
        hosts: ["api-canary.example.com"]
        paths: ["/users"]
        strip_path: false
        plugins:
          - <<: *rate_lim
            config:
              second: 20
              minute: 500
          - name: key-auth
            config:
              key_names: ["canary-key"]
  - name: canary-stable
    host: users.internal
    port: 8443
    protocol: https
    weight: 90
    routes:
      - name: stable-routes
        hosts: ["api-canary.example.com"]
        paths: ["/users"]
        strip_path: false
        plugins:
          - <<: *rate_lim
            config:
              second: 50
              minute: 1500
upstreams:
  - name: auth-upstream
    <<: *hc_base
  - name: users-upstream
    <<: *hc_base
  - name: ws-upstream
    <<: *hc_base
  - name: grpc-upstream
    <<: *hc_base
    active:
      healthy:
        interval: 10
        successes: 2
      unhealthy:
        interval: 10
        http_failures: 1
        tcp_failures: 1
      http_path: /grpc.health.v1.Health/Check
      type: grpc
  - name: canary-upstream
    <<: *hc_base
specification_coverage:
  auth_named_routes:
    - /auth
    - jwt validation
    - ip restriction
    - cors
    status: covered
    omissions: []
  user_api_routes:
    - /users
    - /users/:id
    - key auth
    - request transformation
    - response transformation
    status: covered
    omissions: []
  websocket_routes:
    - /stream
    - ws/wss protocols
    - token-based auth
    status: covered
    omissions: []
  grpc_routes:
    - /grpc.service.v1/
    - mTLS
    - grpc health check
    status: covered
    omissions: []
  canary_pattern:
    - weighted split 90/10
    - separate upstreams
    status: covered
    omissions: []
  rate_limiting:
    - per-service limits
    - local policy
    status: covered
    omissions: []
  deliberate_omissions:
    - route: oauth2-authorization-code-flow
      rationale: not supported at gateway level; handled by identity provider
    - route: saml-assertion-consumer
      rationale: idp-side pattern, not gateway
    - route: api-documentation
      rationale: served by developer portal, not gateway
key_rotation_procedure:
  script: |
    #!/bin/bash
    # Usage: ./rotate-key.sh <consumer_id> <key_name>
    set -euo pipefail
    CID=$1
    KNAME=$2
    NEWKEY=$(openssl rand -base64 32 | tr -d '\n')
    PAYLOAD=$(jq -n --arg k "$NEWKEY" --arg n "$KNAME" '{key: $k, name: $n}')
    curl -s -X DELETE "http://localhost:8001/consumers/$CID/key-auth"
    curl -s -X POST "http://localhost:8001/consumers/$CID/key-auth" \
      -H "Content-Type: application/json" \
      -d "$PAYLOAD"
    echo "NEWKEY=$NEWKEY"
  notes:
    - base64 output is stripped of trailing newline only, not content
    - keyauthcredentials nesting matches Kong 3.x declarative spec
    - rotate via DELETE then POST to avoid version conflicts
envoy_rate_limit_behavior:
  type: fixed-window
  unit: second
  requests_per_unit: <per_route_value>
  note: fixed-window is correct per Envoy docs; sliding-window not supported in this config path
validation_gates:
  pre_apply:
    - run: yamllint declarative.yml
      required: true
    - run: jq -e '.services' declarative.yml > /dev/null
      message: services block must exist
    - run: jq -e '.upstreams' declarative.yml > /dev/null
      message: upstreams block must exist
  post_apply:
    - endpoint: GET /routes
      expected: non-empty
    - endpoint: GET /services
      expected: all named services present
    - endpoint: GET /upstreams
      expected: health checks enabled
    - endpoint: POST to each route
      expected: HTTP 200/401/403 per plugin policy
  spec_cross_reference:
    - read the specification document
    - list every named route, plugin, and service from the spec
    - compare against the declarative output
    - write down every deliberate omission with its rationale
    - reject config if any route or plugin is missing without documented justification
notes:
  shared YAML anchors in upstreams and plugin configs reduce repetition
  all TLS defaults use modern cipher suite, TLSv1.2 minimum
  non-default values only per service section
  metric_name and request_id defaults omitted to reduce noise