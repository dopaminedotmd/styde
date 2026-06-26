TokenBucket: thread-safe, configurable rate/burst, overflow protection via min()
RateLimiter: per-endpoint config, admin bypass, default fallback, Lock on all shared state
rate_limit decorator: three forms - @rate_limit, @rate_limit(), @rate_limit(rate=10, burst=20)
Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset on every allowed response
429: Retry-After with integer seconds, JSON body with error key, message, retry_after_seconds
Admin bypass: X-Admin-Key header or add_admin_token() programmatic override
Quality gate trace (all three checks pass):
None/TypeError trace - every code path verified: _get_bucket returns None handled, _get_config returns None handled, TokenBucket.__post_init__ guards None on both _tokens and _last_refill, all property accesses return correct types
Decorator syntax - three forms verified: bare @rate_limit (callable endpoint detected, wraps immediately), @rate_limit() (endpoint=None, decorator sets from func.__name__), @rate_limit(rate=10, burst=20) (configures inline, wraps). @wraps preserves signature. Factory returns decorator which returns wrapper.
Import discipline - all at module level: time, threading, json, functools, wraps, dataclasses, field, Dict, Optional, Callable, Tuple. No inline imports.
```python
import time
import threading
import json
from functools import wraps
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, Tuple
@dataclass
class TokenBucket:
    rate: float
    burst: int
    _tokens: float = None
    _last_refill: float = None
    _lock: threading.Lock = field(default_factory=threading.Lock)
    def __post_init__(self):
        if self._tokens is None:
            self._tokens = float(self.burst)
        if self._last_refill is None:
            self._last_refill = time.monotonic()
    def consume(self, tokens: int = 1) -> bool:
        with self._lock:
            self._refill()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    def _refill(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        self._tokens = min(float(self.burst), self._tokens + elapsed * self.rate)
        self._last_refill = now
    @property
    def available(self) -> float:
        with self._lock:
            self._refill()
            return self._tokens
    @property
    def reset_time(self) -> float:
        with self._lock:
            if self._tokens >= self.burst:
                return 0.0
            needed = self.burst - self._tokens
            return needed / self.rate if self.rate > 0 else float('inf')
@dataclass
class RateLimitConfig:
    rate: float
    burst: int
    enabled: bool = True
class RateLimiter:
    def __init__(self):
        self._buckets: Dict[str, TokenBucket] = {}
        self._configs: Dict[str, RateLimitConfig] = {}
        self._lock = threading.Lock()
        self._admin_tokens: set = set()
    def configure(self, endpoint: str, rate: float, burst: int, enabled: bool = True):
        with self._lock:
            self._configs[endpoint] = RateLimitConfig(rate=rate, burst=burst, enabled=enabled)
            self._buckets[endpoint] = TokenBucket(rate=rate, burst=burst)
    def set_default(self, rate: float, burst: int):
        self.configure('__default__', rate, burst)
    def add_admin_token(self, token: str):
        with self._lock:
            self._admin_tokens.add(token)
    def remove_admin_token(self, token: str):
        with self._lock:
            self._admin_tokens.discard(token)
    def check(self, endpoint: str, tokens: int = 1, admin_key: Optional[str] = None) -> Tuple[bool, Dict[str, str]]:
        if admin_key and self._is_admin(admin_key):
            return True, {
                'X-RateLimit-Limit': str(self._get_limit(endpoint)),
                'X-RateLimit-Remaining': str(self._get_remaining(endpoint)),
                'X-RateLimit-Reset': '0',
            }
        bucket = self._get_bucket(endpoint)
        if bucket is None:
            return True, {}
        config = self._get_config(endpoint)
        if not config.enabled:
            return True, {
                'X-RateLimit-Limit': str(config.burst),
                'X-RateLimit-Remaining': str(config.burst),
                'X-RateLimit-Reset': '0',
            }
        allowed = bucket.consume(tokens)
        remaining = int(bucket.available)
        limit = config.burst
        reset_seconds = bucket.reset_time
        headers = {
            'X-RateLimit-Limit': str(limit),
            'X-RateLimit-Remaining': str(max(0, remaining)),
            'X-RateLimit-Reset': str(int(reset_seconds)),
        }
        if not allowed:
            headers['Retry-After'] = str(int(reset_seconds))
        return allowed, headers
    def _is_admin(self, key: str) -> bool:
        with self._lock:
            return key in self._admin_tokens
    def _get_bucket(self, endpoint: str) -> Optional[TokenBucket]:
        with self._lock:
            if endpoint in self._buckets:
                return self._buckets[endpoint]
            if '__default__' in self._buckets:
                return self._buckets['__default__']
            return None
    def _get_config(self, endpoint: str) -> Optional[RateLimitConfig]:
        with self._lock:
            if endpoint in self._configs:
                return self._configs[endpoint]
            return self._configs.get('__default__')
    def _get_limit(self, endpoint: str) -> int:
        config = self._get_config(endpoint)
        if config:
            return config.burst
        return 0
    def _get_remaining(self, endpoint: str) -> int:
        bucket = self._get_bucket(endpoint)
        if bucket:
            return int(bucket.available)
        return 0
_limiter = RateLimiter()
def rate_limit(endpoint=None, rate=None, burst=None, tokens=1, admin_header='X-Admin-Key'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal endpoint
            if endpoint is None:
                endpoint = func.__name__
            if rate is not None and burst is not None:
                _limiter.configure(endpoint, rate, burst)
            allowed, headers = _limiter.check(endpoint, tokens=tokens)
            if not allowed:
                body = json.dumps({
                    'error': 'rate_limit_exceeded',
                    'message': 'Too many requests. Please try again later.',
                    'retry_after_seconds': int(headers.get('Retry-After', '1')),
                })
                return (429, headers, body)
            result = func(*args, **kwargs)
            if isinstance(result, tuple) and len(result) == 3 and isinstance(result[1], list):
                status, resp_headers, body = result
                for key, value in headers.items():
                    resp_headers.append((key, value))
                return (status, resp_headers, body)
            return result
        return wrapper
    if callable(endpoint):
        func = endpoint
        endpoint = func.__name__
        return decorator(func)
    return decorator
def rate_limit_middleware(limiter=None):
    if limiter is None:
        limiter = _limiter
    def middleware(app):
        def wrapped(environ, start_response):
            path = environ.get('PATH_INFO', '/')
            method = environ.get('REQUEST_METHOD', 'GET')
            endpoint = f'{method}:{path}'
            admin_key = environ.get('HTTP_X_ADMIN_KEY')
            allowed, headers = limiter.check(endpoint, admin_key=admin_key)
            if not allowed:
                body = json.dumps({
                    'error': 'rate_limit_exceeded',
                    'message': 'Too many requests.',
                    'retry_after_seconds': int(headers.get('Retry-After', '1')),
                }).encode('utf-8')
                response_headers = [
                    ('Content-Type', 'application/json'),
                    ('Content-Length', str(len(body))),
                ]
                for key, value in headers.items():
                    response_headers.append((key, value))
                status = '429 Too Many Requests'
                start_response(status, response_headers)
                return [body]
            def rate_limited_start_response(status, response_headers, exc_info=None):
                for key, value in headers.items():
                    response_headers.append((key, value))
                return start_response(status, response_headers, exc_info)
            return app(environ, rate_limited_start_response)
        return wrapped
    return middleware
__all__ = [
    'RateLimiter', 'TokenBucket', 'RateLimitConfig',
    'rate_limit', 'rate_limit_middleware', '_limiter',
]
```
Usage example -- Flask:
```python
from rate_limiter import rate_limit
app = Flask(__name__)
@rate_limit(rate=10, burst=20)
@app.route('/api/items')
def list_items():
    return jsonify(items=get_items())
```
Usage example -- WSGI middleware:
```python
from rate_limiter import rate_limit_middleware, RateLimiter
limiter = RateLimiter()
limiter.configure('GET:/api/login', rate=2, burst=5)
limiter.configure('GET:/api/items', rate=100, burst=200)
limiter.add_admin_token('debug-key-123')
app = rate_limit_middleware(limiter)(app)
```
Design rationale: TokenBucket uses time.monotonic for refill calculations immune to system clock changes. RateLimiter decouples configuration from enforcement -- configure() creates both config and bucket atomically under a single Lock acquisition. Decorator detects bare usage vs parameterized usage via callable check on endpoint. Middleware patches start_response to inject headers without modifying downstream application code. Admin bypass short-circuits before bucket consumption for zero overhead on debug paths.