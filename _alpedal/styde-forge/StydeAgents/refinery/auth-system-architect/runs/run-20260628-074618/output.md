I design auth systems. Try: 'Add PKCE to /login endpoint'
Capabilities:
OAuth: implement OAuth 2.0 flows (PKCE, client credentials)
  `Add PKCE flow to /login endpoint` -> generates auth URL with codechallenge=S256, state, callback handler that exchanges code + verifier
OIDC: integrate OpenID Connect for SSO
  `Connect Okta SSO` -> fetches OIDC discovery doc, registers client, builds callback with JWKS signature verification
WebAuthn: implement Passkeys/WebAuthn
  `Add passkey login` -> generates navigator.credentials.create() ceremony, attestation verification, credential storage
MFA: add TOTP and SMS multi-factor auth
  `Enable TOTP for user 42` -> provisions TOTP secret, generates otpauth:// URI, adds verification middleware
Session: design secure session management with rotation
  `Rotate session every 15 min` -> issues short-lived access tokens, refresh rotation with sliding expiry, blacklist on logout