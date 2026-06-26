┊ review diff
[38;2;218;165;32ma/skills\dashboard-auth\auth.py → b/skills\dashboard-auth\auth.py[0m
[38;2;139;134;130m@@ -0,0 +1,510 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+Dashboard Auth Module.[0m
[38;2;255;255;255;48;2;19;87;20m+HTTP Basic Auth + Session Management + CSRF + Input Validation + CORS + Rate Limiting.[0m
[38;2;255;255;255;48;2;19;87;20m+Every code path is exercised by inline _run_tests().[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import hashlib[0m
[38;2;255;255;255;48;2;19;87;20m+import os[0m
[38;2;255;255;255;48;2;19;87;20m+import time[0m
[38;2;255;255;255;48;2;19;87;20m+import re[0m
[38;2;255;255;255;48;2;19;87;20m+import html[0m
[38;2;255;255;255;48;2;19;87;20m+import base64[0m
[38;2;255;255;255;48;2;19;87;20m+from http.cookies import SimpleCookie[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- Configuration ---[0m
[38;2;255;255;255;48;2;19;87;20m+SESSION_EXPIRY = 3600        # seconds (1 hour default)[0m
[38;2;255;255;255;48;2;19;87;20m+CSRF_EXPIRY = 3000           # seconds (~50 min, renewed before session expiry)[0m
[38;2;255;255;255;48;2;19;87;20m+REQUIRE_HTTPS = True         # enforce HTTPS-only cookies[0m
[38;2;255;255;255;48;2;19;87;20m+ALLOWED_ORIGINS = [[0m
[38;2;255;255;255;48;2;19;87;20m+    "http://localhost:8765",[0m
[38;2;255;255;255;48;2;19;87;20m+    "https://localhost:8765",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+RATE_LIMIT_WINDOW = 60       # seconds per window[0m
[38;2;255;255;255;48;2;19;87;20m+RATE_LIMIT_MAX = 30          # max requests per window per IP[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- In-memory stores ---[0m
[38;2;255;255;255;48;2;19;87;20m+_sessions = {}    # token_hash -> {username, expiry, csrf_token, csrf_expiry}[0m
[38;2;255;255;255;48;2;19;87;20m+_rate_store = {}  # ip -> [timestamp, ...][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+#  Helpers[0m
[38;2;255;255;255;48;2;19;87;20m+# ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def _hash_token(token: str) -> str:[0m
[38;2;255;255;255;48;2;19;87;20m+    return hashlib.sha256(token.encode()).hexdigest()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def _generate_token() -> str:[0m
[38;2;255;255;255;48;2;19;87;20m+    return os.urandom(32).hex()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+#  Basic Auth[0m
[38;2;255;255;255;48;2;19;87;20m+# ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def basic_auth_credentials(request_headers: dict) -> dict | None:[0m
[38;2;255;255;255;48;2;19;87;20m+    """[0m
[38;2;255;255;255;48;2;19;87;20m+    Extract username:password from an HTTP Basic Auth header.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    Returns dict with keys 'username' and 'password', or None if the header[0m
[38;2;255;255;255;48;2;19;87;20m+    is missing / malformed.[0m
[38;2;255;255;255;48;2;19;87;20m+    """[0m
[38;2;255;255;255;48;2;19;87;20m+    auth = request_headers.get("Authorization", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    if not auth.startswith("Basic "):[0m
[38;2;255;255;255;48;2;19;87;20m+        return None[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        decoded = base64.b64decode(auth[6:]).decode("utf-8")[0m
[38;2;255;255;255;48;2;19;87;20m+        if ":" not in decoded:[0m
[38;2;255;255;255;48;2;19;87;20m+            return None[0m
[38;2;255;255;255;48;2;19;87;20m+        username, password = decoded.split(":", 1)[0m
[38;2;255;255;255;48;2;19;87;20m+        return {"username": username, "password": password}[0m
[38;2;255;255;255;48;2;19;87;20m+    except (ValueError, UnicodeDecodeError, base64.binascii.Error):[0m
[38;2;255;255;255;48;2;19;87;20m+        return None[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+#  Session Management[0m
[38;2;255;255;255;48;2;19;87;20m+# ──────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def create_session(username: str) -> str:[0m
[38;2;255;255;255;48;2;19;87;20m+    """[0m
[38;2;255;255;255;48;2;19;87;20m+    Create a new session for *username*.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    Returns the un-hashed session token (the caller sends this to the client[0m
[38;2;255;255;255;48;2;19;87;20m+    as a cookie).[0m
[38;2;255;255;255;48;2;19;87;20m+    """[0m
[38;2;255;255;255;48;2;19;87;20m+    token = _generate_token()[0m
[38;2;255;255;255;48;2;19;87;20m+    token_hash = _hash_token(token)[0m
[38;2;139;134;130m… omitted 432 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\skills\dashboard-auth\auth.py → b/D:\styde\_alpedal\styde-forge\skills\dashboard-auth\auth.py[0m
[38;2;139;134;130m@@ -162,16 +162,17 @@[0m
[38;2;184;134;11m     """[0m
[38;2;184;134;11m     Strip XSS and SQL injection from a single string input.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-    * HTML-escapes < > " ' &[0m
[38;2;255;255;255;48;2;119;20;20m-    * Removes SQL keywords, -- comments, semicolons, and bare single quotes.[0m
[38;2;255;255;255;48;2;19;87;20m+    * Removes SQL keywords, -- comments, semicolons, and bare single quotes[0m
[38;2;255;255;255;48;2;19;87;20m+      BEFORE HTML-encoding so HTML entity syntax is not corrupted.[0m
[38;2;255;255;255;48;2;19;87;20m+    * HTML-escapes < > " ' &  (prevents XSS in rendered output).[0m
[38;2;184;134;11m     """[0m
[38;2;184;134;11m     if not isinstance(value, str):[0m
[38;2;184;134;11m         return str(value) if value is not None else ""[0m
[38;2;255;255;255;48;2;119;20;20m-    # XSS: HTML-escape[0m
[38;2;255;255;255;48;2;119;20;20m-    value = html.escape(value, quote=True)[0m
[38;2;255;255;255;48;2;119;20;20m-    # SQL injection: strip dangerous patterns[0m
[38;2;255;255;255;48;2;19;87;20m+    # SQL injection: strip dangerous patterns FIRST[0m
[38;2;184;134;11m     for pat in _SQL_PATTERNS:[0m
[38;2;184;134;11m         value = pat.sub("", value)[0m
[38;2;255;255;255;48;2;19;87;20m+    # XSS: HTML-escape LAST (after SQL stripping to preserve entity syntax)[0m
[38;2;255;255;255;48;2;19;87;20m+    value = html.escape(value, quote=True)[0m
[38;2;184;134;11m     return value[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\skills\dashboard-auth\auth.py → b/D:\styde\_alpedal\styde-forge\skills\dashboard-auth\auth.py[0m
[38;2;139;134;130m@@ -380,9 +380,8 @@[0m
[38;2;184;134;11m     xss = "<script>alert('x')</script>"[0m
[38;2;184;134;11m     out = sanitize_input(xss)[0m
[38;2;184;134;11m     assert "<script>" not in out[0m
[38;2;255;255;255;48;2;119;20;20m-    assert "&lt;script&gt;" in out[0m
[38;2;255;255;255;48;2;119;20;20m-    assert "&gt;" in out[0m
[38;2;255;255;255;48;2;119;20;20m-    assert "&#x27;" in out or "&#39;" in out  # depends on python version[0m
[38;2;255;255;255;48;2;19;87;20m+    assert "&lt;script&gt;" in out  # html.escape produces this[0m
[38;2;255;255;255;48;2;19;87;20m+    assert "alert" in out  # alert is not a SQL keyword, survives[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m     sqli = "'; DROP TABLE users; --"[0m
[38;2;184;134;11m     out2 = sanitize_input(sqli)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\skills\dashboard-auth\auth.py → b/D:\styde\_alpedal\styde-forge\skills\dashboard-auth\auth.py[0m
[38;2;139;134;130m@@ -202,7 +202,7 @@[0m
[38;2;184;134;11m     Only origins in ALLOWED_ORIGINS (or containing 'localhost') are permitted.[0m
[38;2;184;134;11m     Returns an empty dict for disallowed origins.[0m
[38;2;184;134;11m     """[0m
[38;2;255;255;255;48;2;119;20;20m-    origin = request_headers.get("Origin", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    origin = request_headers.get("Origin", "") or ""[0m
[38;2;184;134;11m     if origin in ALLOWED_ORIGINS or "localhost" in origin:[0m
[38;2;184;134;11m         return {[0m
[38;2;184;134;11m             "Access-Control-Allow-Origin": origin,[0m
Ad-hoc verification: PASSED
Ran against the edited auth.py (the None Origin fix was the unverified change).
- Inline suite: 27/27 assertions passed.
- Extra edge cases: None Origin returns {}, expired session returns None, rate-limit old entries pruned, non-string sanitize handled, decorator name preserved, REQUIRE_HTTPS flag present -- all 8 passed.
Temp script cleaned up. File at D:\styde\_alpedal\styde-forge\skills\dashboard-auth\auth.py is verified on the current contents.