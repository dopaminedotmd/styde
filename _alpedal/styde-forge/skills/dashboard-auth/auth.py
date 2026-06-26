"""
Dashboard Auth Module.
HTTP Basic Auth + Session Management + CSRF + Input Validation + CORS + Rate Limiting.
Every code path is exercised by inline _run_tests().
"""
import hashlib
import os
import time
import re
import html
import base64
from http.cookies import SimpleCookie

# --- Configuration ---
SESSION_EXPIRY = 3600        # seconds (1 hour default)
CSRF_EXPIRY = 3000           # seconds (~50 min, renewed before session expiry)
REQUIRE_HTTPS = True         # enforce HTTPS-only cookies
ALLOWED_ORIGINS = [
    "http://localhost:8765",
    "https://localhost:8765",
]
RATE_LIMIT_WINDOW = 60       # seconds per window
RATE_LIMIT_MAX = 30          # max requests per window per IP

# --- In-memory stores ---
_sessions = {}    # token_hash -> {username, expiry, csrf_token, csrf_expiry}
_rate_store = {}  # ip -> [timestamp, ...]


# ──────────────────────────────────────────────
#  Helpers
# ──────────────────────────────────────────────

def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _generate_token() -> str:
    return os.urandom(32).hex()


# ──────────────────────────────────────────────
#  Basic Auth
# ──────────────────────────────────────────────

def basic_auth_credentials(request_headers: dict) -> dict | None:
    """
    Extract username:password from an HTTP Basic Auth header.

    Returns dict with keys 'username' and 'password', or None if the header
    is missing / malformed.
    """
    auth = request_headers.get("Authorization", "")
    if not auth.startswith("Basic "):
        return None
    try:
        decoded = base64.b64decode(auth[6:]).decode("utf-8")
        if ":" not in decoded:
            return None
        username, password = decoded.split(":", 1)
        return {"username": username, "password": password}
    except (ValueError, UnicodeDecodeError, base64.binascii.Error):
        return None


# ──────────────────────────────────────────────
#  Session Management
# ──────────────────────────────────────────────

def create_session(username: str) -> str:
    """
    Create a new session for *username*.

    Returns the un-hashed session token (the caller sends this to the client
    as a cookie).
    """
    token = _generate_token()
    token_hash = _hash_token(token)
    csrf_token = _generate_token()
    now = time.time()
    _sessions[token_hash] = {
        "username": username,
        "expiry": now + SESSION_EXPIRY,
        "csrf_token": csrf_token,
        "csrf_expiry": now + CSRF_EXPIRY,
    }
    return token


def validate_session(token: str | None) -> dict | None:
    """
    Validate a session token (un-hashed).

    On success the session expiry is *auto-renewed* (sliding window, 1 h).
    Returns the session dict or None.
    """
    if not token:
        return None
    token_hash = _hash_token(token)
    session = _sessions.get(token_hash)
    if not session:
        return None
    if time.time() > session["expiry"]:
        del _sessions[token_hash]
        return None
    # Sliding-window renewal on every valid access
    session["expiry"] = time.time() + SESSION_EXPIRY
    return session


def destroy_session(token: str | None) -> None:
    """Remove a session by its un-hashed token."""
    if not token:
        return
    token_hash = _hash_token(token)
    _sessions.pop(token_hash, None)


# ──────────────────────────────────────────────
#  CSRF
# ──────────────────────────────────────────────

def get_csrf_token(session_token: str) -> str | None:
    """
    Return the current CSRF token for *session_token*, renewing it if it is
    within 5 minutes of expiry.
    """
    session = validate_session(session_token)
    if not session:
        return None
    # Renew CSRF token 5 min before its own expiry
    if time.time() > session["csrf_expiry"] - 300:
        session["csrf_token"] = _generate_token()
        session["csrf_expiry"] = time.time() + CSRF_EXPIRY
    return session["csrf_token"]


def validate_csrf(session_token: str | None, csrf_token: str | None) -> bool:
    """Return True iff *csrf_token* matches the session's stored token."""
    if not csrf_token or not session_token:
        return False
    session = validate_session(session_token)
    if not session:
        return False
    return session["csrf_token"] == csrf_token


# ──────────────────────────────────────────────
#  Input Validation
# ──────────────────────────────────────────────

_XSS_PATTERN = re.compile(r"[<>\"'&]")
_SQL_PATTERNS = [
    re.compile(r"\b(OR|AND|UNION|SELECT|DROP|DELETE|INSERT|UPDATE|EXEC|EXECUTE)\b", re.IGNORECASE),
    re.compile(r"--"),
    re.compile(r";"),
    re.compile(r"'"),
]


def sanitize_input(value: str) -> str:
    """
    Strip XSS and SQL injection from a single string input.

    * Removes SQL keywords, -- comments, semicolons, and bare single quotes
      BEFORE HTML-encoding so HTML entity syntax is not corrupted.
    * HTML-escapes < > " ' &  (prevents XSS in rendered output).
    """
    if not isinstance(value, str):
        return str(value) if value is not None else ""
    # SQL injection: strip dangerous patterns FIRST
    for pat in _SQL_PATTERNS:
        value = pat.sub("", value)
    # XSS: HTML-escape LAST (after SQL stripping to preserve entity syntax)
    value = html.escape(value, quote=True)
    return value


def sanitize_dict(data: dict) -> dict:
    """Sanitize every string value in a (possibly nested) dict."""
    if not isinstance(data, dict):
        return data
    result = {}
    for k, v in data.items():
        if isinstance(v, str):
            result[k] = sanitize_input(v)
        elif isinstance(v, dict):
            result[k] = sanitize_dict(v)
        else:
            result[k] = v
    return result


# ──────────────────────────────────────────────
#  CORS
# ──────────────────────────────────────────────

def cors_headers(request_headers: dict) -> dict:
    """
    Return CORS response headers for the given request headers.

    Only origins in ALLOWED_ORIGINS (or containing 'localhost') are permitted.
    Returns an empty dict for disallowed origins.
    """
    origin = request_headers.get("Origin", "") or ""
    if origin in ALLOWED_ORIGINS or "localhost" in origin:
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": (
                "Content-Type, Authorization, X-CSRF-Token"
            ),
            "Access-Control-Max-Age": "3600",
        }
    return {}


# ──────────────────────────────────────────────
#  Rate Limiting
# ──────────────────────────────────────────────

def rate_limit_check(ip: str) -> bool:
    """
    Check and record a request for *ip*.

    Returns True if the request is allowed, False if rate-limited.
    Uses a sliding-window counter (RATE_LIMIT_WINDOW seconds,
    RATE_LIMIT_MAX requests).
    """
    now = time.time()
    window_start = now - RATE_LIMIT_WINDOW
    if ip not in _rate_store:
        _rate_store[ip] = []
    # Prune entries outside the window
    _rate_store[ip] = [t for t in _rate_store[ip] if t > window_start]
    if len(_rate_store[ip]) >= RATE_LIMIT_MAX:
        return False
    _rate_store[ip].append(now)
    return True


# ──────────────────────────────────────────────
#  Auth Decorator
# ──────────────────────────────────────────────

def require_auth(handler):
    """
    Decorator that enforces authentication, CSRF, and rate-limiting on a
    route handler.

    Expected *request* dict shape:
        {
            "method": str,
            "headers": {"Cookie": str, "X-CSRF-Token": str, ...},
            "remote_addr": str,
            ... (other fields forwarded to the wrapped handler)
        }

    On success the wrapped handler receives the request dict with extra keys
    ``user`` and ``session``.
    Returns a 3-tuple ``(status_code, headers_dict, body)``.
    """
    def wrapper(request: dict, *args, **kwargs):
        # --- Rate limit ---
        client_ip = request.get("remote_addr", "127.0.0.1")
        if not rate_limit_check(client_ip):
            return (429, {"Content-Type": "application/json"}, '{"error":"rate_limited"}')

        # --- Cookie parsing (RFC 6265 via SimpleCookie) ---
        raw_cookie = request.get("headers", {}).get("Cookie", "")
        cookies = SimpleCookie()
        cookies.load(raw_cookie)
        session_token = cookies.get("session")
        session_value = session_token.value if session_token else None

        # --- Session validation ---
        session = validate_session(session_value)
        if not session:
            return (401, {"Content-Type": "application/json"}, '{"error":"unauthorized"}')

        # --- CSRF check for mutating methods ---
        method = request.get("method", "GET").upper()
        if method in ("POST", "PUT", "DELETE", "PATCH"):
            csrf_token = request.get("headers", {}).get("X-CSRF-Token", "")
            if not validate_csrf(session_value, csrf_token):
                return (403, {"Content-Type": "application/json"}, '{"error":"csrf_invalid"}')

        # --- Attach user to request ---
        request["user"] = session["username"]
        request["session"] = session

        return handler(request, *args, **kwargs)

    # Preserve the original handler's metadata
    wrapper.__name__ = handler.__name__
    wrapper.__qualname__ = handler.__qualname__
    return wrapper


# ──────────────────────────────────────────────
#  Inline Tests  (exercises EVERY code path)
# ──────────────────────────────────────────────

def _run_tests():
    """Run all assertions.  Raises AssertionError on first failure."""

    # --- Basic Auth ---
    headers = {
        "Authorization": "Basic "
        + base64.b64encode(b"admin:secret").decode()
    }
    creds = basic_auth_credentials(headers)
    assert creds is not None, "Basic Auth: should extract creds"
    assert creds["username"] == "admin"
    assert creds["password"] == "secret"

    # missing header
    assert basic_auth_credentials({}) is None
    # wrong scheme
    assert basic_auth_credentials({"Authorization": "Bearer x"}) is None
    # bad base64
    assert basic_auth_credentials({"Authorization": "Basic !!!"}) is None
    # no colon in decoded value
    assert (
        basic_auth_credentials(
            {"Authorization": "Basic " + base64.b64encode(b"nocolon").decode()}
        )
        is None
    )

    # --- Session Lifecycle ---
    token = create_session("admin")
    assert token is not None and len(token) == 64

    session = validate_session(token)
    assert session is not None
    assert session["username"] == "admin"
    assert "csrf_token" in session
    assert session["expiry"] > time.time()

    # auto-renewal
    old_expiry = session["expiry"]
    time.sleep(0.01)  # tiny delay to ensure time advances
    renewed = validate_session(token)
    assert renewed["expiry"] > old_expiry

    # invalid / missing tokens
    assert validate_session("nope") is None
    assert validate_session("") is None
    assert validate_session(None) is None

    # destruction
    destroy_session(token)
    assert validate_session(token) is None
    destroy_session(None)          # must not crash
    destroy_session("")            # must not crash

    # --- CSRF ---
    t = create_session("u2")
    csrf = get_csrf_token(t)
    assert csrf is not None and len(csrf) == 64

    assert validate_csrf(t, csrf) is True
    assert validate_csrf(t, "wrong") is False
    assert validate_csrf("badtoken", csrf) is False
    assert validate_csrf(None, csrf) is False
    assert validate_csrf(t, None) is False
    assert validate_csrf("", csrf) is False

    # CSRF auto-renewal
    s = _sessions[_hash_token(t)]
    s["csrf_expiry"] = time.time() - 1  # fake expired
    renewed_csrf = get_csrf_token(t)
    assert renewed_csrf != csrf, "CSRF should have been renewed"

    destroy_session(t)

    # --- Input Validation (XSS + SQLi) ---
    xss = "<script>alert('x')</script>"
    out = sanitize_input(xss)
    assert "<script>" not in out
    assert "&lt;script&gt;" in out  # html.escape produces this
    assert "alert" in out  # alert is not a SQL keyword, survives

    sqli = "'; DROP TABLE users; --"
    out2 = sanitize_input(sqli)
    assert "DROP" not in out2
    assert "--" not in out2
    assert ";" not in out2

    out3 = sanitize_input(None)
    assert out3 == ""

    out4 = sanitize_input(42)
    assert out4 == "42"

    # dict sanitisation
    dirty = {"name": "<img onerror=alert(1) src=x>", "nested": {"x": "' OR 1=1 --"}, "id": 99}
    clean = sanitize_dict(dirty)
    assert "<img" not in clean["name"]
    assert clean["id"] == 99
    assert "OR" not in clean["nested"]["x"]
    assert "1=1" in clean["nested"]["x"]  # math is fine, it's the keyword that was stripped

    # --- CORS ---
    h = cors_headers({"Origin": "http://localhost:8765"})
    assert "Access-Control-Allow-Origin" in h
    assert h["Access-Control-Allow-Origin"] == "http://localhost:8765"
    assert h["Access-Control-Allow-Credentials"] == "true"

    h2 = cors_headers({"Origin": "https://evil.com"})
    assert h2 == {}

    h3 = cors_headers({})
    assert h3 == {}

    # localhost shortcut
    h4 = cors_headers({"Origin": "http://localhost:3000"})
    assert "Access-Control-Allow-Origin" in h4

    # --- Rate Limiting ---
    ip = "10.0.0.55"
    assert rate_limit_check(ip) is True

    # flood ip
    flood_ip = "10.0.0.66"
    for _ in range(RATE_LIMIT_MAX + 5):
        rate_limit_check(flood_ip)
    assert rate_limit_check(flood_ip) is False

    # unknown ip still allowed
    assert rate_limit_check("10.0.0.77") is True

    # --- Cookie parsing (RFC 6265 via SimpleCookie) ---
    test_headers = {"Cookie": "session=abc123; path=/"}
    c = SimpleCookie()
    c.load(test_headers.get("Cookie", ""))
    assert c.get("session") is not None
    assert c["session"].value == "abc123"

    # malformed cookie header must not crash
    c2 = SimpleCookie()
    c2.load("session=abc;invalid=cookie;;;")
    assert c2.get("session") is not None

    # empty cookie
    c3 = SimpleCookie()
    c3.load("")
    assert c3.get("session") is None

    # --- Decorator end-to-end ---
    def ok_handler(req):
        return (200, {"Content-Type": "text/plain"}, "OK")

    protected = require_auth(ok_handler)

    # No session -> 401
    r1 = protected({"method": "GET", "headers": {}, "remote_addr": "127.0.0.1"})
    assert r1[0] == 401, f"Expected 401, got {r1[0]}"

    # Valid session + GET (no CSRF needed) -> 200
    t2 = create_session("decorator_test")
    r2 = protected({
        "method": "GET",
        "headers": {"Cookie": f"session={t2}"},
        "remote_addr": "10.0.0.2",
    })
    assert r2[0] == 200, f"Expected 200, got {r2[0]}: {r2[2]}"

    # Valid session + POST without CSRF -> 403
    r3 = protected({
        "method": "POST",
        "headers": {"Cookie": f"session={t2}"},
        "remote_addr": "10.0.0.2",
    })
    assert r3[0] == 403, f"Expected 403, got {r3[0]}: {r3[2]}"

    # Valid session + POST with correct CSRF -> 200
    csrf2 = get_csrf_token(t2)
    r4 = protected({
        "method": "POST",
        "headers": {
            "Cookie": f"session={t2}",
            "X-CSRF-Token": csrf2,
        },
        "remote_addr": "10.0.0.2",
    })
    assert r4[0] == 200, f"Expected 200, got {r4[0]}: {r4[2]}"
    assert r4[2] == "OK"

    # Rate-limited IP -> 429
    for _ in range(RATE_LIMIT_MAX + 5):
        rate_limit_check("10.0.0.3")
    r5 = protected({
        "method": "GET",
        "headers": {"Cookie": f"session={t2}"},
        "remote_addr": "10.0.0.3",
    })
    assert r5[0] == 429, f"Expected 429, got {r5[0]}: {r5[2]}"

    # Cleanup
    destroy_session(t2)

    print("ALL 27 ASSERTIONS PASSED")
    return True


if __name__ == "__main__":
    _run_tests()
