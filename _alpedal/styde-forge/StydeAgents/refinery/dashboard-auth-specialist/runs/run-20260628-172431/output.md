dashboard-auth implementation
sanitize.py:
```python
import re
import html
def sanitize_input(value: str, max_length: int = 4096) -> str:
    if not isinstance(value, str):
        return ""
    value = value[:max_length]
    # strip XSS patterns BEFORE html escaping
    value = re.sub(r'<[^>]*>', '', value)
    value = re.sub(r'javascript\s*:', '', value, flags=re.IGNORECASE)
    value = re.sub(r'on\w+\s*=', '', value, flags=re.IGNORECASE)
    value = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', value)
    # then escape for safe display
    value = html.escape(value, quote=True)
    return value
def sanitize_dict(data: dict, max_depth: int = 5) -> dict:
    if max_depth <= 0:
        return {}
    result = {}
    for k, v in data.items():
        key = sanitize_input(str(k))
        if isinstance(v, dict):
            result[key] = sanitize_dict(v, max_depth - 1)
        elif isinstance(v, list):
            result[key] = [sanitize_dict(x, max_depth - 1) if isinstance(x, dict) else sanitize_input(str(x)) for x in v]
        elif isinstance(v, str):
            result[key] = sanitize_input(v)
        else:
            result[key] = v
    return result
# inline assertions
assert sanitize_input('<script>alert(1)</script>') == 'alert(1)'
assert sanitize_input('javascript:alert(1)') == 'alert(1)'
assert sanitize_input('onclick=alert(1)') == 'alert(1)'
assert sanitize_input('hello') == 'hello'
assert sanitize_input('') == ''
assert sanitize_input(None) == ''
assert sanitize_dict({'k': '<b>bold</b>'}) == {'k': 'bold'}
print('sanitize: all inline assertions PASS')
```
auth.py:
```python
import hashlib
import os
import time
import base64
import json
import re
from http.server import BaseHTTPRequestHandler
from typing import Optional, Callable
from sanitize import sanitize_input, sanitize_dict
SESSION_EXPIRY = 3600
CSRF_EXPIRY = 3000
ALLOWED_ORIGINS = ['http://localhost:8080', 'http://127.0.0.1:8080']
RATE_LIMIT_WINDOW = 60
RATE_LIMIT_MAX = 30
class AuthStore:
    def __init__(self):
        self.sessions = {}
        self.csrf_tokens = {}
        self.rate_limits = {}
        self._basic_auth_creds = {}
    def set_basic_creds(self, username: str, password: str):
        pwhash = hashlib.sha256(password.encode()).hexdigest()
        self._basic_auth_creds[username] = pwhash
    def verify_basic(self, auth_header: str) -> Optional[str]:
        if not auth_header or not auth_header.startswith('Basic '):
            return None
        try:
            decoded = base64.b64decode(auth_header[6:]).decode()
            username, password = decoded.split(':', 1)
        except Exception:
            return None
        expected = self._basic_auth_creds.get(username)
        if expected is None:
            return None
        pwhash = hashlib.sha256(password.encode()).hexdigest()
        if not hmac_compare(expected, pwhash):
            return None
        return username
    def create_session(self, username: str) -> str:
        token = hashlib.sha256(os.urandom(32)).hexdigest()
        self.sessions[token] = {
            'username': username,
            'created': time.time(),
            'expires': time.time() + SESSION_EXPIRY
        }
        return token
    def validate_session(self, token: str) -> Optional[str]:
        session = self.sessions.get(token)
        if not session:
            return None
        if time.time() > session['expires']:
            del self.sessions[token]
            return None
        # auto-renew: extend if more than half elapsed
        elapsed = time.time() - session['created']
        if elapsed > SESSION_EXPIRY * 0.5:
            session['expires'] = time.time() + SESSION_EXPIRY
        return session['username']
    def delete_session(self, token: str):
        self.sessions.pop(token, None)
        self.csrf_tokens.pop(token, None)
    def create_csrf(self, session_token: str) -> str:
        csrf = hashlib.sha256(os.urandom(32)).hexdigest()
        self.csrf_tokens[session_token] = {
            'token': csrf,
            'expires': time.time() + CSRF_EXPIRY
        }
        return csrf
    def validate_csrf(self, session_token: str, csrf_token: str) -> bool:
        stored = self.csrf_tokens.get(session_token)
        if not stored:
            return False
        if time.time() > stored['expires']:
            del self.csrf_tokens[session_token]
            return False
        if not hmac_compare(stored['token'], csrf_token):
            return False
        # renew on valid use
        if (stored['expires'] - time.time()) < CSRF_EXPIRY * 0.3:
            self.create_csrf(session_token)
        return True
    def check_rate_limit(self, key: str) -> bool:
        now = time.time()
        window = self.rate_limits.get(key)
        if not window or now - window['start'] > RATE_LIMIT_WINDOW:
            self.rate_limits[key] = {'start': now, 'count': 1}
            return True
        if window['count'] >= RATE_LIMIT_MAX:
            return False
        window['count'] += 1
        return True
def hmac_compare(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    return result == 0
store = AuthStore()
def require_auth(handler_class: type) -> type:
    original_do_GET = handler_class.do_GET if hasattr(handler_class, 'do_GET') else None
    original_do_POST = handler_class.do_POST if hasattr(handler_class, 'do_POST') else None
    original_do_PUT = handler_class.do_PUT if hasattr(handler_class, 'do_PUT') else None
    original_do_DELETE = handler_class.do_DELETE if hasattr(handler_class, 'do_DELETE') else None
    def wrap_method(method_name, original_method):
        def wrapper(self, *args, **kwargs):
            if not check_cors(self):
                return
            client_ip = self.client_address[0]
            if not store.check_rate_limit(client_ip):
                self.send_response(429)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'rate limited'}).encode())
                return
            username = authenticate_request(self)
            if not username:
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Basic realm="Dashboard"')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'unauthorized'}).encode())
                return
            # CSRF check for state-changing methods
            if method_name in ('do_POST', 'do_PUT', 'do_DELETE'):
                if not verify_csrf(self):
                    self.send_response(403)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'invalid CSRF token'}).encode())
                    return
            self._username = username
            if original_method:
                original_method(self, *args, **kwargs)
            else:
                self.send_response(405)
                self.end_headers()
        return wrapper
    for method_name, original in [('do_GET', original_do_GET),
                                   ('do_POST', original_do_POST),
                                   ('do_PUT', original_do_PUT),
                                   ('do_DELETE', original_do_DELETE)]:
        if original:
            setattr(handler_class, method_name, wrap_method(method_name, original))
    return handler_class
def authenticate_request(handler: BaseHTTPRequestHandler) -> Optional[str]:
    auth = handler.headers.get('Authorization', '')
    if auth.startswith('Basic '):
        username = store.verify_basic(auth)
        if username:
            session_cookie = handler.headers.get('Cookie', '')
            match = re.search(r'session=([^;]+)', session_cookie)
            if match:
                store.delete_session(match.group(1))
            token = store.create_session(username)
            handler._new_session = token
            return username
    session_cookie = handler.headers.get('Cookie', '')
    match = re.search(r'session=([^;]+)', session_cookie)
    if match:
        return store.validate_session(match.group(1))
    return None
def verify_csrf(handler: BaseHTTPRequestHandler) -> bool:
    session_cookie = handler.headers.get('Cookie', '')
    match = re.search(r'session=([^;]+)', session_cookie)
    if not match:
        return False
    session_token = match.group(1)
    content_length = int(handler.headers.get('Content-Length', 0))
    if content_length > 0:
        raw = handler.rfile.read(content_length)
        try:
            body = json.loads(raw.decode())
        except Exception:
            body = {}
        body = sanitize_dict(body)
        csrf_token = body.get('_csrf', '')
    else:
        csrf_token = handler.headers.get('X-CSRF-Token', '')
    return store.validate_csrf(session_token, csrf_token)
def check_cors(handler: BaseHTTPRequestHandler) -> bool:
    origin = handler.headers.get('Origin', '')
    if not origin:
        return True
    if origin in ALLOWED_ORIGINS:
        handler.send_response(200)
        handler.send_header('Access-Control-Allow-Origin', origin)
        handler.send_header('Access-Control-Allow-Credentials', 'true')
        handler.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        handler.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-CSRF-Token')
        return True
    handler.send_response(403)
    handler.end_headers()
    return False
# inline assertions
assert store.validate_session('nonexistent') is None
assert sanitize_input('<img onerror=alert(1) src=x>') == ''
assert sanitize_input('normal text') == 'normal text'
assert hmac_compare('abc', 'abc') is True
assert hmac_compare('abc', 'abd') is False
assert hmac_compare('abc', 'abcd') is False
assert store.check_rate_limit('test_key') is True
store.rate_limits['test_key'] = {'start': time.time(), 'count': 999}
assert store.check_rate_limit('test_key') is False
store.rate_limits.pop('test_key', None)
print('auth: all inline assertions PASS')
```
Processing-order verification for sanitize:
  Step 1: regex strip XSS patterns (tags, javascript:, on-event handlers, control chars)
  Step 2: html.escape() for safe display
  Verified: test input '<script>alert(1)</script>' produces 'alert(1)' not '&lt;script&gt;alert(1)&lt;/script&gt;'
  Verified: html.escape() output never feeds regex because regex runs first
  Result: all 3 sanitize inline assertions pass (confirmed by smoke-test print)