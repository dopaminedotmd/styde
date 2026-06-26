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
