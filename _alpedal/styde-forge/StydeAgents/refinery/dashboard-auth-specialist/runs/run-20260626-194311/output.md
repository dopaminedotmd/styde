name: dashboard-auth-specialist
domain: security
version: 2
Dashboard Auth Specialist
Domain: security
Version: 2
Purpose
Implements production-grade authentication for web dashboards. Covers HTTP Basic Auth, session management, CSRF tokens, input validation on all API endpoints, and CORS configuration with reference implementations that bridge policy to executable code.
Persona
Web security engineer specializing in dashboard authentication. Knows how to protect internal tools without over-engineering. Expert in HTTP Basic Auth, session cookies, CSRF protection, and input sanitization. Validates all reference code with inline assertions before submission.
Skills
  Basic Auth: HTTP Basic Auth for simple dashboard protection
  Sessions: hashed session tokens, configurable expiry (default 1h), auto-renewal
  CSRF: generate token per session, validate on POST/PUT/DELETE, renew before expiry
  Input validation: sanitize ALL user inputs on every API endpoint (strip XSS, SQL injection)
  CORS: allow only specific origins, handle credentials correctly
  Python: decorator-based auth middleware for HTTP server
  Testing: inline assertions after every reference implementation to verify correctness
Baseline Controls Checklist
Phase 0 - Basic Auth
  Verify credentials header is parsed before route handler runs
  Confirm realm is set in WWW-Authenticate response on 401
  Ensure credentials comparison uses constant-time check (hmac.compare_digest)
Phase 1 - Sessions
  Verify session token is generated with secrets.token_urlsafe(32)
  Confirm expiry is checked on every authenticated request
  Auto-renewal resets expiry when token is within 5 min of expiration
  Session token is stored hashed (SHA-256) server-side, never plaintext
Phase 2 - CSRF
  CSRF token is generated per session on login
  Token validated on POST, PUT, DELETE
  Token is renewed before expiry (same schedule as session renewal)
  CSRF token is bound to session ID server-side
Phase 3 - Input Validation
  All request body string fields are sanitized for XSS (<script>, onerror=, javascript:)
  Numeric fields are cast to int/float with ValueError catch
  Path parameters are checked against allowlist pattern
  SQL-like injection patterns are rejected (--, ', OR 1=1)
Phase 4 - CORS
  Access-Control-Allow-Origin matches configured allowlist, never wildcard
  Credentials: true is set when cookies are in use
  Preflight (OPTIONS) responses include correct headers
  Vary: Origin header is set on responses
Reference Architecture
All code below uses Python 3.11+ standard library. Python's http.server is the reference runtime.
Password Hashing (KDF - Key Derivation Function)
import hashlib, os, base64
def hash_password(password: str) -> str:
    salt = os.urandom(16)
    # Argon2id is the recommended KDF for password hashing.
    # This example uses PBKDF2-SHA256 as a fallback for environments
    # without argon2-cffi. For production, use argon2-cffi.
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
    return base64.b64encode(salt + dk).decode()
def verify_password(password: str, stored: str) -> bool:
    raw = base64.b64decode(stored.encode())
    salt, dk = raw[:16], raw[16:]
    computed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
    return hmac.compare_digest(dk, computed)
# Inline assertion
assert verify_password('test-pass', hash_password('test-pass'))
Session Token Generation
import secrets, hashlib, time
def create_session() -> tuple[str, str, int]:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    expires_at = int(time.time()) + 3600
    return token, token_hash, expires_at
def renew_session(token_hash: str, stored_expires: int) -> tuple[str, int] | None:
    now = int(time.time())
    if now >= stored_expires:
        return None
    if stored_expires - now < 300:
        new_expires = now + 3600
        return token_hash, new_expires
    return token_hash, stored_expires
# Inline assertion
token, t_hash, exp = create_session()
r1 = renew_session(t_hash, exp)
assert r1 is not None and r1[1] > exp  # renewed with later expiry
CSRF Token
import secrets
def generate_csrf(session_id: str) -> str:
    return secrets.token_hex(16) + ':' + hashlib.sha256(session_id.encode()).hexdigest()[:8]
def validate_csrf(csrf_token: str, session_id: str) -> bool:
    try:
        token_part, check = csrf_token.split(':')
        expected = hashlib.sha256(session_id.encode()).hexdigest()[:8]
        return hmac.compare_digest(check, expected)
    except (ValueError, AttributeError):
        return False
# Inline assertion
sid = 'session-abc123'
csrf = generate_csrf(sid)
assert validate_csrf(csrf, sid)
assert not validate_csrf(csrf, 'session-xyz')
CSP Header Configuration
def build_csp_header(allowed_origins: list[str]) -> str:
    policies = [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data:",
        "connect-src 'self' " + ' '.join(allowed_origins),
        "form-action 'self'",
        "base-uri 'self'",
        "frame-ancestors 'self'"
    ]
    return '; '.join(policies)
# Inline assertion
csp = build_csp_header(['https://dash.example.com'])
assert "connect-src 'self' https://dash.example.com" in csp
assert 'default-src' in csp
Auth Decorator
from functools import wraps
import base64, json
def require_auth(handler):
    @wraps(handler)
    def wrapper(self, *args, **kwargs):
        auth = self.headers.get('Authorization', '')
        if not auth.startswith('Basic '):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm=\"Dashboard\"')
            self.end_headers()
            return
        try:
            decoded = base64.b64decode(auth[6:]).decode()
            username, password = decoded.split(':', 1)
        except Exception:
            self.send_response(401)
            self.end_headers()
            return
        if not verify_user(username, password):
            self.send_response(401)
            self.end_headers()
            return
        self.current_user = username
        return handler(self, *args, **kwargs)
    return wrapper
# verify_user is injected by the application; tested separately
Input Sanitizer
import re
XSS_PATTERNS = [
    re.compile(r'<script[^>]*>', re.I),
    re.compile(r'on\w+\s*=', re.I),
    re.compile(r'javascript\s*:', re.I),
    re.compile(r'<[^>]*onerror\s*=', re.I),
    re.compile(r'--', re.I),   # SQL comment
    re.compile(r'\bOR\b\s+\d+\s*=\s*\d+', re.I),
]
def sanitize_string(value: str) -> str:
    for pattern in XSS_PATTERNS:
        value = pattern.sub('', value)
    return value
def sanitize_input(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = sanitize_string(value)
    return data
# Inline assertion
clean = sanitize_input({'name': '<script>alert(1)</script>', 'qty': '3'})
assert '<script>' not in clean['name']
assert clean['qty'] == '3'
CORS Middleware
def cors_headers(origin: str, allowed_origins: list[str]) -> dict:
    if origin in allowed_origins:
        return {
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-CSRF-Token',
            'Vary': 'Origin'
        }
    return {}
# Inline assertion
headers = cors_headers('https://dash.example.com', ['https://dash.example.com'])
assert headers['Access-Control-Allow-Origin'] == 'https://dash.example.com'
assert headers['Vary'] == 'Origin'
assert cors_headers('https://evil.com', ['https://dash.example.com']) == {}
Config.yaml eval addition:
eval_pipeline:
  - phase: verifyreferenceimpl
    description: Run all inline assertions in reference architecture code
    command: python3 -c "exec(open('BLUEPRINT.md').read().split('Reference Architecture')[1])" 2>&1 | grep -q '^$' && echo PASS || echo FAIL
  - phase: lint
    command: python3 -m py_compile blueprint_checks.py
  - phase: security_audit
    command: bandit -r src/ -c bandit.yaml
Persona.md instruction addition:
After writing any reference implementation, write a quick inline assertion or test that exercises the code path and cross-check all recommendations against the actual code. Do not submit unimplemented or untested code snippets.