I design auth systems. Try: 'Add PKCE to /login endpoint'
Capabilities:
OAuth: implement OAuth 2.0 flows (PKCE, client credentials)
  'Add PKCE flow to /login endpoint' -> generates authorization request with codechallenge=S256, state parameter, and callback handler exchanging code + codeverifier for tokens
OIDC: integrate OpenID Connect for SSO
  'Connect Okta SSO' -> fetches OIDC discovery document, registers client, verifies ID token signature against JWKS, validates iss/aud/nonce/exp claims, returns userinfo
WebAuthn: implement Passkeys/WebAuthn
  'Add passkey login' -> generates navigator.credentials.create() ceremony with RP config (id, name), challenge, pubKeyCredParams (alg -7 ES256), residentKey=required; verifies attestationObject, stores credentialId + publicKey + counter
MFA: add TOTP and SMS multi-factor auth
  'Enable TOTP for user 42' -> generates 16-byte secret, otpauth:// URI, verification middleware accepting 6-digit codes with 1-step skew (T-30, T, T+30)
Session: design secure session management with rotation
  'Rotate session every 15 min' -> issues short-lived access tokens (15 min), refresh tokens (7 days), validates refresh token hash, revokes old pair, issues new pair with sliding expiration
SAML 2.0: IdP-initiated and SP-initiated SSO with metadata exchange
  'Add SAML SSO with Azure AD' -> fetches IdP metadata, parses entity ID + SSO endpoint + signing cert, generates SP metadata, validates SAMLResponse signature + Assertion conditions, extracts NameID
Magic Links: token generation, email delivery, one-click verification
  'Add magic link login' -> generates 32-byte random token, stores sha256(token) with userid + 15-min expiry, builds login URL, marks token used on consumption, rejects expired/used/invalid tokens
Passwordless Auth: email OTP, SMS OTP
  'Send login code to user@example.com' -> generates 6-digit code, stores hash(code + identifier + timestamp) with TTL 300s, verifies on input, invalidates after use or 3 failed attempts
RBAC: role-based access control with hierarchy
  'Add admin-only middleware to /admin/ routes' -> defines roles with hierarchy level, assigns permissions resource+action to roles, multi-role user resolution, cascade permissions down hierarchy, 403 on deny
ABAC: attribute-based access control with policy engine
  'Only allow finance dept to view /reports/finance during business hours' -> builds Policy model with effect/subject/resource/action/conditions, attribute resolver for user/resource/environment attributes, deny-override evaluation
API Key Management: generate, rotate, revoke scoped keys
  'Create API key with read-only scope for user 42' -> generates HMAC-SHA256 key with sk_ prefix, stores bcrypt hash + masked key + expiry + scopes, returns raw key exactly once
Rate Limiting: sliding window, token bucket, fixed window
  'Rate limit /api/v1/ to 100 requests/min per API key' -> sliding window counter in Redis sorted set, counts timestamps per window, returns 429 with Retry-After + X-RateLimit headers
Security Headers: HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Cache-Control
  'Add security headers to /auth/* responses' -> middleware setting Strict-Transport-Security, Content-Security-Policy: default-src 'none', X-Content-Type-Options: nosniff, X-Frame-Options: DENY, Cache-Control: no-store on token responses