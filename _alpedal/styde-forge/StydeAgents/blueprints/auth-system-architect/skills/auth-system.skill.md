# Auth System Capabilities

This skill defines procedural workflows for authentication system tasks. Load with skill_view(name='auth-system').

## OAuth 2.0 (PKCE, Client Credentials)

When user requests PKCE flow:
1. Generate code_verifier (43-128 chars, unreserved characters)
2. Derive code_challenge = base64url(sha256(code_verifier))
3. Build authorization URL with response_type=code, client_id, redirect_uri, code_challenge, code_challenge_method=S256, state
4. On callback: exchange authorization_code + code_verifier for tokens at /token endpoint
5. Return access_token, refresh_token, expires_in, token_type

When user requests client credentials:
1. POST /token with grant_type=client_credentials, client_id, client_secret
2. Return access_token with configured scopes

## OpenID Connect (SSO)

When user requests OIDC SSO integration:
1. Fetch OIDC discovery document from issuer /.well-known/openid-configuration
2. Register client (dynamic registration or manual config)
3. Build authorization request with scope=openid+profile+email, response_type=code
4. On callback: verify ID token signature against JWKS from discovery URL
5. Validate iss, aud, nonce, exp claims
6. Return userinfo from ID token claims or /userinfo endpoint

## WebAuthn / Passkeys

When user requests passkey login:
1. Generate challenge (16+ bytes random)
2. Call navigator.credentials.create() with publicKey params: rp (id, name), user (id, name, displayName), challenge, pubKeyCredParams (alg -7 ES256), authenticatorSelection (residentKey=required, userVerification=preferred)
3. On creation response: parse attestationObject and clientDataJSON
4. Verify authenticator data, store credentialId + publicKey + counter
5. For authentication: navigator.credentials.get() with challenge, allowCredentials=[stored credentialIds]
6. Verify assertion signature, check counter for cloned authenticator detection

## MFA (TOTP, SMS)

When user requests TOTP:
1. Generate 16-byte random secret
2. Create otpauth:// URI with secret, issuer, user email
3. Generate QR code (send as base64 image or link)
4. Verify: compare user-supplied 6-digit code against TOTP(time=current, secret, digits=6, period=30)
5. Allow 1-step skew (check T-30, T, T+30)

When user requests SMS MFA:
1. Generate 6-digit random code
2. Store hash(code + phone + timestamp) with TTL 300s
3. Send via SMS provider (Twilio, AWS SNS, etc.)
4. Verify: compare user code, check expiration, invalidate after use or 3 failed attempts

## Session Management (Rotation)

When user requests session rotation:
1. Issue access token with short expiry (15 min default)
2. Issue refresh token with longer expiry (7 day default), store its hash server-side
3. On refresh: validate refresh token hash, revoke old refresh token, issue new pair
4. On logout: blacklist refresh token hash, add access token to denylist until expiry
5. For sliding rotation: check remaining refresh TTL, if below 50% issue new refresh token without reducing total expiry

## SAML 2.0 (SSO)

When user requests SAML SSO integration:
1. Fetch IdP metadata XML from configured metadata URL or uploaded file
2. Parse IdP entity ID, SSO endpoint URLs, and X.509 signing certificate
3. Generate SP metadata with ACS URL, entity ID, and audience restriction
4. Build SP-initiated SSO: redirect user to IdP SingleSignOnService with RelayState
5. Build IdP-initiated SSO: expose ACS endpoint that accepts SAMLResponse POST
6. On ACS callback: validate SAML response signature against IdP certificate
7. Verify Assertion conditions (NotBefore, NotOnOrAfter, AudienceRestriction)
8. Extract NameID and attributes, create or match local user session

## Magic Links

When user requests magic link login:
1. Generate cryptographically random token (32+ bytes, base64url-encoded)
2. Compute token_hash = sha256(token), store with user_id and expiry (15 min default) in database
3. Build login URL: https://app.example.com/auth/magic-link?token=<token>
4. Send email with login link via configured email provider (SendGrid, SES, SMTP)
5. On click: look up token_hash, verify not expired, check single-use flag
6. Mark token as used (or delete), issue session tokens for the user
7. Return success response; on failure (expired/used/invalid) show error page with option to request new link

## RBAC (Role-Based Access Control)

When user requests RBAC:
1. Define Role model with name, description, and hierarchy_level (higher = more privileged)
2. Define Permission model with resource, action (create/read/update/delete/admin), and optional conditions
3. Create many-to-many role-permissions and user-roles associations
4. Implement authorization middleware: extract user from session/token, load user roles + permissions
5. Check against required permission for the route: if user has any role with the matching resource+action, allow
6. For hierarchy-based access: if user role level >= required role level, cascade permissions down
7. Return 403 Forbidden with structured error body on denied access

## ABAC (Attribute-Based Access Control)

When user requests ABAC:
1. Define Policy model with effect (Allow/Deny), subjects (user attributes), resources, actions, and conditions (boolean expressions)
2. Build attribute resolver: pull user attributes (department, clearance, location), resource attributes (classification, owner, sensitivity), and environment attributes (time, network zone)
3. Implement policy evaluation engine: for each matching policy, evaluate conditions using attribute values
4. Apply deny-override or first-match-wins strategy
5. Return Permit or Deny decision with optional obligations (log, MFA challenge)

## API Key Management

When user requests API key generation:
1. Generate random API key using HMAC-SHA256 with server secret, prefix with a 4-char identifier (sk_live_xxx)
2. Hash the key with bcrypt (cost 10), store hash + masked prefix + expiry + scopes + user_id
3. Return the raw key exactly once in the response (never logged or stored in plaintext)
4. For key rotation: generate new key with same scopes, add to valid keys, deactivate old key after a grace period
5. For key revocation: set key status to revoked, add to immediate denylist

## Rate Limiting

When user requests rate limiting:
1. Select algorithm: sliding window (default), token bucket, or fixed window
2. For sliding window: store request timestamps per key (user_id, API key hash, or IP) in Redis sorted set
3. On each request: count timestamps in current window, if count exceeds limit return 429 with Retry-After header
4. For token bucket: initialize bucket with capacity and refill rate, consume tokens on each request
5. Return rate limit headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset on every response

## Security Headers for Auth Endpoints

When user requests security headers on auth endpoints:
1. Set Strict-Transport-Security: max-age=31536000; includeSubDomains
2. Set Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self'
3. Set X-Content-Type-Options: nosniff
4. Set X-Frame-Options: DENY
5. Set Cache-Control: no-store, no-cache, must-revalidate on all token responses
6. Set Pragma: no-cache
7. Apply to all /auth/*, /token/*, /saml/*, /magic-link/* responses
