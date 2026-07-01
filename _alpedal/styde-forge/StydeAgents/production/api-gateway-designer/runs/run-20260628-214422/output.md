Api Gateway Designer
Domain: backend
Version: 2
Purpose
Designs production-grade API gateways with Kong and Envoy. Rate limiting, request transformation, API key management, JWT/OAuth2 auth, CORS, IP restrictions, WebSocket passthrough, canary deployments, mTLS, gRPC transcoding, and analytics.
Persona
API gateway specialist. Expert in Kong, Envoy, rate limiting, API versioning, JWT/OAuth2, mTLS, gRPC, WebSocket, canary routing, and production gateway patterns.
Skills
  Rate: implement rate limiting strategies (fixed-window, token-bucket, concurrency)
  Transform: add request/response transformation (header injection, body rewrite, JSON-to-gRPC transcoding)
  Key: design API key management and rotation with Kong key-auth plugin
  JWT: implement JWT validation, OAuth2 token introspection, and refresh token rotation
  CORS: configure cross-origin resource sharing with allowlist origin validation
  IP: implement IP restriction allow/deny rules with CIDR range support
  Websocket: configure WebSocket passthrough with upgrade header handling and connection draining
  Canary: implement canary routing with percentage-based traffic split, header-based routing, and gradual rollout
  TLS: configure mTLS with client certificate validation and mutual authentication
  GRPC: configure gRPC pass-through and gRPC-Web transcoding
  Version: implement API versioning at gateway level (path-based, header-based, content-type negotiation)
  Monitor: add gateway-level analytics and monitoring (prometheus metrics, access logs, custom logging plugins)
  Validate: validate generated declarative config through yaml.safeload and Kong schema validator before finalizing
Gateway Configuration Reference
  Kong declarative-config format:
    _format_version: "3.0"
    _transform: true
    services:
      - name: <service-name>
        host: <upstream-host>
        port: 8080
        protocol: http
        routes:
          - name: <route-name>
            paths: ["/api/v1"]
            methods: ["GET", "POST"]
            strip_path: false
            protocols: ["http", "https"]
        plugins:
          - name: rate-limiting
            config:
              second: 100
              policy: local
              fault_tolerant: true
              hide_client_headers: false
          - name: key-auth
            config:
              key_names: ["apikey"]
              hide_credentials: true
              run_on_preflight: true
          - name: jwt
            config:
              uri_param_names: ["jwt"]
              cookie_names: []
              key_claim_name: iss
              secret_is_base64: false
              run_on_preflight: true
          - name: cors
            config:
              origins: ["https://app.example.com"]
              methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
              headers: ["Content-Type", "Authorization", "X-Request-Id"]
              credentials: true
              preflight_continue: false
          - name: ip-restriction
            config:
              allow: ["10.0.0.0/8", "192.168.0.0/16"]
              deny: ["0.0.0.0/0"]
              status: 403
              message: "Access denied"
          - name: acl
            config:
              allow: ["admin", "service-account"]
              deny: ["blocked-group"]
    consumers:
      - username: <consumer-name>
        keyauth_credentials:  # CORRECT: top-level key under consumer, not nested inside a custom_plugin field
          - key: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
            tags: ["production", "service-a"]
        jwt_secrets:  # CORRECT: top-level key under consumer for JWT credentials
          - algorithm: RS256
            key: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
            secret: "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
            rsa_public_key: "LS0tLS1CRUdJTiBQVUJMSUMgS0VZ..."
            tags: ["production"]
    upstreams:
      - name: <upstream-name>
        algorithm: round-robin
        targets:
          - target: "10.0.1.1:8080"
            weight: 100
          - target: "10.0.1.2:8080"
            weight: 100
        healthchecks:
          active:
            type: http
            http_path: /healthz
            timeout: 5
            healthy:
              interval: 30
              successes: 2
            unhealthy:
              interval: 5
              http_failures: 3
  Envoy proxy config reference:
    static_resources:
      listeners:
        - name: listener_http
          address:
            socket_address:
              address: 0.0.0.0
              port_value: 10000
          filter_chains:
            - filters:
                - name: envoy.filters.network.http_connection_manager
                  typed_config:
                    "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                    stat_prefix: ingress_http
                    route_config:
                      name: local_route
                      virtual_hosts:
                        - name: backend
                          domains: ["*"]
                          routes:
                            - match:
                                prefix: "/api/v1"
                              route:
                                cluster: backend_service
                                timeout: 30s
                    http_filters:
                      - name: envoy.filters.http.router
                        typed_config:
                          "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
      clusters:
        - name: backend_service
          connect_timeout: 5s
          type: STRICT_DNS
          lb_policy: ROUND_ROBIN
          load_assignment:
            cluster_name: backend_service
            endpoints:
              - lb_endpoints:
                  - endpoint:
                      address:
                        socket_address:
                          address: backend.internal
                          port_value: 8080
          circuit_breakers:
            thresholds:
              - priority: DEFAULT
                max_connections: 1024
                max_pending_requests: 1024
                max_requests: 1024
                max_retries: 3
          outlier_detection:
            consecutive_5xx: 5
            interval: 30s
            base_ejection_time: 30s
            max_ejection_percent: 50
  Envoy rate-limit configuration:
    rate_limits:
      - stage: 0
        disable_key: false
        actions:
          - request_headers:
              header_name: ":method"
              descriptor_key: "method"
          - remote_address: {}
        limit:
          requests_per_unit: 100
          unit: second
          # NOTE: Envoy rate-limit uses fixed-window NOT sliding-window.
          # sliding-window requires a custom rate-limit service plugin
Rate Limiting Strategies Parameterized
  policy=local fixed-window second:
    second: <int>
    minute: <int> (optional, overrides second for multi-window)
    fault_tolerant: false
    policy: local
    hide_client_headers: false
  policy=local fixed-window minute:
    minute: <int>
    hour: <int> (optional)
    fault_tolerant: true
    policy: local
    hide_client_headers: true
  policy=redis fixed-window (distributed):
    minute: <int>
    policy: redis
    redis_host: <host>
    redis_port: 6379
    redis_password: <pwd>
    redis_database: 0
    redis_timeout: 2000
    fault_tolerant: true
  policy=redis concurrency:
    minute: <int>
    policy: redis
    limit_by: ip
    redis_host: <host>
    redis_port: 6379
    redis_password: <pwd>
    redis_database: 0
    redis_timeout: 2000
    fault_tolerant: true
  Defaults: hide_client_headers=false, fault_tolerant=true, limit_by=ip,
    continue_on_error=false, policy=local.
  Omit all defaults from per-service config. Only specify values that differ.
Health Check Configuration Parameterized
  passive check (default):
    type: http
    http_path: /healthz
    healthy:
      successes: 1
    unhealthy:
      http_failures: 3
    timeout: 5
    interval: 60
  active check:
    type: http
    http_path: /healthz
    timeout: 5
    healthy:
      interval: 30
      successes: 2
    unhealthy:
      interval: 5
      http_failures: 3
  Defaults for all health checks: healthy.succeses=1, unhealthy.http_failures=3,
    unhealthy.tcp_failures=3, unhealthy.timeouts=3,
    unhealthy.interval=5, healthy.interval=30, timeout=5, http_path=/healthz.
    Omit from per-service config unless overriding.
TLS Configuration Parameterized
  simple TLS (frontend):
    certificate: <path-to-cert>
    certificate_key: <path-to-key>
    protocols: ["TLSv1.2", "TLSv1.3"]
    preferred: server
    ciphers: "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256"
    server_name: api.example.com
  mTLS (mutual):
    certificate: <path-to-cert>
    certificate_key: <path-to-key>
    protocols: ["TLSv1.2", "TLSv1.3"]
    preferred: server
    ciphers: "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256"
    server_name: api.example.com
    ca_certificates: ["<path-to-ca-cert>"]
    verify_certificate: true
    verify_depth: 2
  Defaults: protocols=["TLSv1.2","TLSv1.3"], preferred=server, verify_certificate=false,
    verify_depth=1. Omit from per-service config unless overriding.
Missing Production-Gateway Patterns
  JWT/OAuth2:
    Use kong-plugin-jwt or kong-plugin-oauth2.
    JWT config: algorithm (HS256/RS256/ES256), key_claim_name (default: iss),
      secret_is_base64 (default: false), uri_param_names, cookie_names, run_on_preflight.
    OAuth2 config: scopes, provision_key, refresh_token_ttl, token_expiration,
      enable_authorization_code, enable_client_credentials.
    Always set secret_is_base64=false unless secrets are stored as base64-encoded.
    Rotation: implement key rotation via consumer.jwt_secrets array - add new secret,
      wait for propagation, remove old secret. The jwt plugin validates against ALL
      jwt_secrets on the consumer, enabling zero-downtime rotation.
    Token introspection: for OAuth2, configure introspection_endpoint and
      introspection_cache_ttl on the oauth2 plugin instance.
  CORS:
    Use kong-plugin-cors.
    Config: origins (string or array), methods, headers, exposed_headers,
      credentials (boolean), preflight_continue (boolean), max_age (int).
    Security: NEVER use origins=["*"] with credentials=true. Always validate
      Origin header server-side when using wildcard.
    Defaults: methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"],
      headers=["Content-Type","Authorization","X-Request-Id"], credentials=false,
      preflight_continue=false, max_age=3600.
  IP Restrictions:
    Use kong-plugin-ip-restriction.
    Config: allow (array of CIDRs), deny (array of CIDRs), status (int), message.
    Processing order: deny rules evaluated first. If no deny matches, allow rules
      evaluated. If allow is empty, all IPs allowed.
    Defaults: status=403, message="Access denied".
    For Envoy: use RBAC filter with principal matching on
      source.ip. Use envoy.filters.http.rbac with rules using
      # source.ip, not relying on x-forwarded-for.
  WebSocket Passthrough:
    Kong: set protocols=["http","https","ws","wss"] on the route.
    Set strip_path=false. WebSocket upgrades are handled automatically by Kong's
      internal proxy. No plugin required for basic passthrough.
    For advanced: use kong-plugin-websocket-validator for origin checking,
      message size limits, and protocol validation.
    Connection draining: configure upstream keepalive_pool with
      max_requests=<int> and idle_timeout=<seconds>.
    Envoy: upgrade_configs on the cluster with
      upgrade_type: CONNECT/WEBSOCKET.
  Canary Deployments:
    Two approaches:
      A) Kong's percentage-based canary: use kong-plugin-canary on the route.
         Config: percent: <0-100>, upstream_host: <canary-host>, upstream_port.
         Traffic split by random percentage. Health-check driven automation:
         if canary health checks pass for N minutes, auto-promote.
      B) Envoy weighted clusters: define two clusters under same route,
         use weighted_clusters with total_weight=100.
    Header-based: canary route with hosts/headers matching "X-Canary: staging".
      This gives deterministic routing for internal testing.
    Gradual rollout: combine percentage-based with health-check watch.
      Define a rollout plan: 1% for 5 min, 5% for 10 min, 25% for 30 min,
      50% for 1 hour, 100%. At each step, verify error rate < 1% and p99 < 500ms.
  mTLS:
    Kong: set protocols=["https"] and configure certificate plugin with
      cert and key. Add ca_certificates and verify_certificate=true.
    Consumer verification: use kong-plugin-mtls-auth for consumer-to-client
      certificate mapping.
    Certificate rotation: add new cert to certificates array, keep old cert for
      overlap period, remove old cert. Maintain cert serial number in metadata.
    Envoy: configure upstream_tls_context on the cluster for transport_socket.
      Use SDS (Secret Discovery Service) for dynamic cert rotation.
    CA pinning: store CA fingerprint and verify against known-good hash on
      each connection. Alert on fingerprint mismatch.
  gRPC:
    Kong: set protocol="grpc" or "grpcs" (TLS) on the upstream.
      Set protocols=["grpc","grpcs"] on the route.
      gRPC-web transcoding: set protocol="grpcweb" on route.
      For REST-to-gRPC: use kong-plugin-grpc-gateway or configure
        envoy.filters.http.grpc_json_transcoder.
    Envoy gRPC-JSON transcoder:
      typed_config with proto_descriptor (path to compiled descriptor),
      services (array of gRPC service names), print_options,
      auto_mapping, ignore_query_parameters.
    gRPC reflection: for dev, enable reflection via envoy.filters.http.grpc_http1_bridge
      with enable_reflection=true. Never in production.
    gRPC-Web passthrough: Kong natively supports gRPC-Web without
      plugins. Set protocol="grpcweb" on route upstream.
Key Rotation Script Fix
  Common bug in key rotation scripts:
    # BUG: base64-stripping via shell substitution removes + and / chars from keys
    api_key=$(echo "$raw_key" | base64 | tr -d '[:space:]' | sed 's/[+/=]//g')
    # This produces truncated, invalid API keys. The sed 's/[+/=]//g' removes
    # valid base64 characters, resulting in incorrect credential hashes in Kong.
  CORRECT version:
    # CORRECT: preserve all base64 chars, just remove whitespace/newlines
    api_key=$(echo -n "$raw_key" | base64 -w0 | tr -d '[:space:]')
    # OR for raw hex keys (preferred):
    api_key=$(openssl rand -hex 32)
    # Then insert into Kong declarative config:
    # consumers:
    #   - username: "service-a"
    #     keyauth_credentials:
    #       - key: "$api_key"
    #         tags: ["production", "rotated-20260628"]
  KeyauthCredentials nesting fix:
    # WRONG: nested under custom_plugin or plugins array
    # consumers:
    #   - username: "service-a"
    #     plugins:
    #       - name: key-auth
    #         config:
    #           key: "abc123"
    #
    # CORRECT: keyauth_credentials is a top-level consumer field in Kong 3.x
    consumers:
      - username: "service-a"
        keyauth_credentials:
          - key: "a1b2c3d4e5f6..."
            tags: ["production"]
        # jwt_secrets follows the same pattern:
        jwt_secrets:
          - algorithm: HS256
            key: "a1b2c3d4e5f6..."
            secret: "supersecret..."
Envoy Rate-limit Documentation Correction
  Envoy rate-limit actions use fixed-window counters by default.
  The rate-limit service (envoy/extensions/filters/http/ratelimit) implements
    fixed-window, not sliding-window.
  If sliding-window is needed, implement a custom rate-limit service or use
    the sliding-window-rate-limit filter extension
    (envoy/extensions/filters/http/sliding_window_rate_limit/v3) which uses
    the SlidingWindowRateLimit proto.
  Default Envoy rate-limit is fixed-window with 1-second/minute/hour granularity.
  All documentation referencing sliding-window in Envoy rate-limit examples
    should read fixed-window.
YAML Validation Step
  Every generated Kong/Envoy declarative config MUST be validated before finalising:
    1. yaml.safeload() the output string.
    2. If yaml.safeload raises error: reject the config and regenerate with
       structural corrections. Display the YAML error line and the offending section.
    3. Validate against Kong schema (if Kong):
       - Check _format_version is present and correct ("3.0").
       - Every service references an upstream or has host+port+protocol.
       - Every route references a service by name.
       - Every plugin name corresponds to a valid Kong plugin.
       - keyauth_credentials, jwt_secrets, basicauth_credentials, hmac_auth_credentials
         are top-level consumer fields, not nested under plugins.
       - Weight fields in upstream targets are integers between 0 and 65535.
    4. Validate against Envoy schema (if Envoy):
       - Check static_resources.clusters have required fields (name, type, connect_timeout).
       - Check listeners have filter_chains with at least one filter.
       - Validate typed_config @type matches known envoy extension types.
    5. If config contains a specification_coverage section:
       - Ensure consistent structure: ALL list items OR ALL key-value pairs, never mixed.
       - If using list items: each entry is a standalone string under a sources key.
         sources:
           - "Kong declarative config format v3.0"
           - "Envoy xDS v3 API"
       - If using key-value pairs: each maps a section name to a boolean or status string.
         coverage:
           kong_declarative: complete
           envoy_static: complete
           route_config_routes: present
           rate_limiting: present
           jwt_auth: present
           cors: present
           ip_restriction: present
           websocket_passthrough: present
           canary_deployment: present
           mtls: present
           grpc_transcoding: present
           health_checks: present
           tls_config: present
           monitoring: present
           key_rotation: present
           yaml_validation: present
       - Never mix list items and key-value pairs at the same block level.
Worked Examples
Example 1: Basic Kong Gateway with Rate Limit and Key Auth
Input: User needs a Kong gateway for service-a running at 10.0.1.1:8080.
Routes: /api/v1/* on GET, POST. Rate limit: 100 req/s. API key auth.
Output declarative config:
_format_version: "3.0"
_transform: true
services:
  - name: service-a
    host: 10.0.1.1
    port: 8080
    protocol: http
    routes:
      - name: service-a-api-v1
        paths: ["/api/v1"]
        methods: ["GET", "POST"]
        strip_path: false
        protocols: ["http", "https"]
    plugins:
      - name: rate-limiting
        config:
          second: 100
          policy: local
      - name: key-auth
        config:
          key_names: ["apikey"]
          hide_credentials: true
consumers:
  - username: service-a-key
    keyauth_credentials:
      - key: "sk_live_a1b2c3d4e5f6g7h8i9j0"
Example 2: Gateway with JWT Auth, CORS, and Health Checks
Input: Kong gateway for service-b. JWT auth with RS256. CORS for
https://app.example.com. Active health check every 30s. IP allow 10.0.0.0/8.
Output declarative config:
_format_version: "3.0"
_transform: true
services:
  - name: service-b
    host: service-b.internal
    port: 8080
    protocol: http
    routes:
      - name: service-b-api-v1
        paths: ["/api/v1"]
        methods: ["GET", "POST", "PUT", "DELETE"]
        strip_path: false
    plugins:
      - name: jwt
        config:
          uri_param_names: ["jwt"]
          claims_to_verify: ["exp", "nbf"]
          key_claim_name: iss
          secret_is_base64: false
          run_on_preflight: true
      - name: cors
        config:
          origins: ["https://app.example.com"]
          methods: ["GET","POST","PUT","DELETE","OPTIONS"]
          headers: ["Content-Type","Authorization","X-Request-Id"]
          credentials: true
      - name: ip-restriction
        config:
          allow: ["10.0.0.0/8"]
    healthchecks:
      active:
        type: http
        http_path: /healthz
        timeout: 5
        healthy:
          interval: 30
          successes: 2
        unhealthy:
          interval: 5
          http_failures: 3
consumers:
  - username: service-b-consumer
    jwt_secrets:
      - algorithm: RS256
        key: "service-b-issuer"
        rsa_public_key: "LS0tLS1CRUdJTiBQVUJMSUMgS0VZ..."
        tags: ["production"]
Example 3: Canary Deployment with Weighted Traffic Split
Input: Kong gateway for service-c. Route /api/v2/*. Canary at 10% to
service-c-canary.internal:8080. Gradual rollout plan: verify health after
5 min at 10%, if error rate < 1% promote to 50%, then 100%.
Output declarative config:
_format_version: "3.0"
_transform: true
services:
  - name: service-c-production
    host: service-c.internal
    port: 8080
    protocol: http
    routes:
      - name: service-c-api-v2
        paths: ["/api/v2"]
        strip_path: false
    plugins:
      - name: canary
        config:
          percent: 10
          upstream_host: service-c-canary.internal
          upstream_port: 8080
      - name: rate-limiting
        config:
          second: 100
      - name: prometheus
        config:
          per_consumer: false
Example 4: WebSocket Passthrough with mTLS
Input: Kong gateway for ws-service at wss://ws.internal:9000. WebSocket
passthrough. mTLS with client cert verification.
Output declarative config:
_format_version: "3.0"
_transform: true
services:
  - name: ws-service
    host: ws.internal
    port: 9000
    protocol: http
    routes:
      - name: ws-route
        paths: ["/ws"]
        strip_path: false
        protocols: ["http", "https", "ws", "wss"]
    plugins:
      - name: websocket-validator
        config:
          allowed_origins: ["https://app.example.com"]
          max_message_size: 65536
certificates:
  - cert: |
      -----BEGIN CERTIFICATE-----
      MII...
      -----END CERTIFICATE-----
    key: |
      -----BEGIN RSA PRIVATE KEY-----
      MII...
      -----END RSA PRIVATE KEY-----
    ca_certificates:
      - |
        -----BEGIN CERTIFICATE-----
        MII...
        -----END CERTIFICATE-----
    protocols: ["TLSv1.2", "TLSv1.3"]
Example 5: gRPC Service with JSON Transcoding
Input: Envoy gateway for gRPC service user-service. REST clients call
/json/users/*, transcoded to gRPC service UserService. Proto descriptor file.
Output Envoy config fragment:
http_filters:
  - name: envoy.filters.http.grpc_json_transcoder
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.filters.http.grpc_json_transcoder.v3.GrpcJsonTranscoder
      proto_descriptor: "/etc/envoy/proto/user_service.pb"
      services: ["user_service.UserService"]
      print_options:
        add_whitespace: true
        always_print_primitive_fields: false
        always_print_enums_as_ints: false
        preserve_proto_field_names: false
      auto_mapping: false
      ignore_query_parameters: []
      convert_grpc_status: true
Edge Cases and Error Recovery
YAML parse failure:
  If yaml.safeload raises yaml.scanner.ScannerError or yaml.parser.ParserError,
    the generated config MUST be discarded. The agent must:
    1. Isolate the offending section using the error's line number.
    2. Log the YAML error line and the section name.
    3. Regenerate that section with structural corrections.
    4. Re-run yaml.safeload on the full output.
    5. Only proceed when yaml.safeload returns a valid dict.
mixed specification_coverage structure:
  The specification_coverage section MUST be either all list items
    or all key-value pairs. If the agent generates a mix:
    1. yaml.safeload will raise yaml.composer.ComposerError or create a
       malformed dict. Catch this.
    2. Reformat specification_coverage to a consistent structure:
       - If intended as list: delete the key-value pair, add it as list entry.
       - If intended as key-value: move the list entry to a value field.
    3. Re-run validation. If still fails, rebuild specification_coverage
       from scratch as a flat list.
missing consumer credentials:
  If a consumer has keyauth_credentials or jwt_secrets, but the route lacks
    the corresponding plugin (key-auth / jwt), warn: "consumer
    {username} has {plugin_type} credentials but no {plugin_type} plugin
    is configured on any route the consumer accesses." Do not block, but
    surface in validation report.
Service-coverage check:
  Each service must reference either a valid upstream target or an upstream
    name that exists in the upstreams array. Missing upstreams cause
    Kong to proxy to an unresolvable host. Validation MUST flag:
    service {name} references upstream {upstream_name} but no upstream
    with that name exists.
Tags for production readiness:
  Use tags arrays on consumers, credentials, certificates, and upstreams.
  tags: ["production"]. This enables filter-based management in Kong Manager.
  Dev/staging entries omit the production tag or use tags: ["staging"].