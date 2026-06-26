Implementation for a thread-safe token bucket rate limiter with per-endpoint policies, proper headers, and admin bypass.
=== File: ratelimit.py ===
import time
import threading
import functools
from enum import Enum
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Tuple
class RateLimitResult:
    def __init__(self, allowed: bool, limit: int, remaining: int, reset_at: float, retry_after: Optional[float] = None):
        self.allowed = allowed
        self.limit = limit
        self.remaining = remaining
        self.reset_at = reset_at
        self.retry_after = retry_after
    def to_headers(self) -> dict:
        headers = {
            "X-RateLimit-Limit": str(self.limit),
            "X-RateLimit-Remaining": str(max(0, self.remaining)),
            "X-RateLimit-Reset": str(int(self.reset_at)),
        }
        if not self.allowed and self.retry_after is not None:
            headers["Retry-After"] = str(int(self.retry_after))
        return headers
    def to_body(self) -> dict:
        return {
            "error": "rate_limit_exceeded",
            "message": "Too many requests. Please wait before retrying.",
            "retry_after_seconds": int(self.retry_after) if self.retry_after else 0,
        }
class TokenBucket:
    def __init__(self, rate: float, burst: int):
        self.rate = rate
        self.burst = burst
        self.tokens = float(burst)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()
    def _refill(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_refill
        added = elapsed * self.rate
        if added > 0:
            self.tokens = min(float(self.burst), self.tokens + added)
            self.last_refill = now
    def consume(self, cost: float = 1.0) -> Tuple[bool, int, float]:
        with self.lock:
            self._refill()
            if self.tokens >= cost:
                self.tokens -= cost
                remaining = int(self.tokens)
                reset_at = time.time() + max(0, (self.burst - self.tokens) / self.rate) if self.rate > 0 else time.time()
                return True, remaining, reset_at
            remaining = int(self.tokens)
            wait_time = (cost - self.tokens) / self.rate if self.rate > 0 else float("inf")
            reset_at = time.time() + wait_time
            return False, remaining, reset_at
    def reset(self) -> None:
        with self.lock:
            self.tokens = float(self.burst)
            self.last_refill = time.monotonic()
class EndpointSensitivity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
DEFAULT_POLICIES = {
    EndpointSensitivity.LOW: (100.0, 150),
    EndpointSensitivity.MEDIUM: (30.0, 50),
    EndpointSensitivity.HIGH: (10.0, 20),
    EndpointSensitivity.CRITICAL: (2.0, 5),
}
@dataclass
class RateLimitPolicy:
    rate: float
    burst: int
    sensitivity: EndpointSensitivity = EndpointSensitivity.MEDIUM
class RateLimiter:
    def __init__(self, policies: Optional[Dict[str, RateLimitPolicy]] = None):
        self._buckets: Dict[str, TokenBucket] = {}
        self._policies: Dict[str, RateLimitPolicy] = policies or {}
        self._global_lock = threading.Lock()
        self._admin_tokens: Dict[str, bool] = {}
        self._default_policy = RateLimitPolicy(rate=30.0, burst=50, sensitivity=EndpointSensitivity.MEDIUM)
    def set_policy(self, route: str, policy: RateLimitPolicy) -> None:
        with self._global_lock:
            self._policies[route] = policy
            if route in self._buckets:
                old = self._buckets[route]
                if old.rate != policy.rate or old.burst != policy.burst:
                    self._buckets[route] = TokenBucket(policy.rate, policy.burst)
    def set_default_policy(self, policy: RateLimitPolicy) -> None:
        with self._global_lock:
            self._default_policy = policy
    def get_policy(self, route: str) -> RateLimitPolicy:
        return self._policies.get(route, self._default_policy)
    def authorise_admin(self, token: str) -> None:
        self._admin_tokens[token] = True
    def revoke_admin(self, token: str) -> None:
        self._admin_tokens.pop(token, None)
    def _get_or_create_bucket(self, route: str) -> TokenBucket:
        with self._global_lock:
            if route not in self._buckets:
                policy = self.get_policy(route)
                self._buckets[route] = TokenBucket(policy.rate, policy.burst)
            return self._buckets[route]
    def check(self, route: str, admin_token: Optional[str] = None) -> RateLimitResult:
        if admin_token and admin_token in self._admin_tokens:
            policy = self.get_policy(route)
            return RateLimitResult(
                allowed=True,
                limit=0,
                remaining=None,
                reset_at=0,
                retry_after=None,
            )
        bucket = self._get_or_create_bucket(route)
        policy = self.get_policy(route)
        allowed, remaining, reset_at = bucket.consume()
        retry_after = max(0, reset_at - time.time()) if not allowed else None
        return RateLimitResult(
            allowed=allowed,
            limit=policy.burst,
            remaining=remaining,
            reset_at=reset_at,
            retry_after=retry_after,
        )
    def reset_route(self, route: str) -> None:
        with self._global_lock:
            if route in self._buckets:
                self._buckets[route].reset()
    def reset_all(self) -> None:
        with self._global_lock:
            for bucket in self._buckets.values():
                bucket.reset()
class rate_limit:
    def __init__(self, route: Optional[str] = None, rate: Optional[float] = None, burst: Optional[int] = None, sensitivity: Optional[EndpointSensitivity] = None):
        self._route = route
        self._rate = rate
        self._burst = burst
        self._sensitivity = sensitivity
        self._limiter: Optional[RateLimiter] = None
    def set_limiter(self, limiter: RateLimiter) -> None:
        self._limiter = limiter
    def __call__(self, func: Callable) -> Callable:
        route = self._route or func.__name__
        limiter_ref = self._limiter
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal limiter_ref
            if limiter_ref is None:
                if not hasattr(func, "_ratelimit_limiter"):
                    raise RuntimeError("RateLimiter not configured. Use rate_limit.set_limiter() or pass via middleware.")
                limiter_ref = getattr(func, "_ratelimit_limiter")
            admin_token = kwargs.pop("_admin_token", None) or (
                args[0].headers.get("X-Admin-Token") if args and hasattr(args[0], "headers") else None
            )
            result = limiter_ref.check(route, admin_token)
            if not result.allowed:
                from werkzeug import Response
                resp = Response(
                    status=429,
                    content_type="application/json",
                    body=json.dumps(result.to_body()),
                )
                for key, val in result.to_headers().items():
                    resp.headers[key] = val
                return resp
            response = func(*args, **kwargs)
            if hasattr(response, "headers"):
                for key, val in result.to_headers().items():
                    response.headers[key] = val
            return response
        if self._limiter is not None:
            wrapper._ratelimit_limiter = self._limiter
        return wrapper
class RateLimitMiddleware:
    def __init__(self, app: Callable, limiter: Optional[RateLimiter] = None, policies: Optional[Dict[str, RateLimitPolicy]] = None):
        self.app = app
        self.limiter = limiter or RateLimiter(policies)
        self._endpoint_map: Dict[str, str] = {}
    def register_endpoint(self, path: str, route_key: Optional[str] = None) -> None:
        self._endpoint_map[path] = route_key or path
    def get_route_key(self, environ: dict) -> str:
        path = environ.get("PATH_INFO", "/")
        for pattern, key in self._endpoint_map.items():
            if path.startswith(pattern):
                return key
        return path
    def __call__(self, environ: dict, start_response: Callable) -> list:
        route_key = self.get_route_key(environ)
        admin_token = None
        headers_dict = {}
        raw_headers = environ.get("HTTP_X_ADMIN_TOKEN", "")
        if raw_headers:
            admin_token = raw_headers
        result = self.limiter.check(route_key, admin_token)
        headers = result.to_headers()
        if not result.allowed:
            import json
            body = json.dumps(result.to_body()).encode("utf-8")
            headers_list = [("Content-Type", "application/json"), ("Content-Length", str(len(body)))]
            for key, val in headers.items():
                headers_list.append((key, val))
            start_response("429 Too Many Requests", headers_list)
            return [body]
        def middleware_start_response(status: str, response_headers: list, exc_info=None):
            for key, val in headers.items():
                response_headers.append((key, val))
            return start_response(status, response_headers, exc_info)
        return self.app(environ, middleware_start_response)
=== Usage ===
limiter = RateLimiter()
limiter.set_policy("/api/auth", RateLimitPolicy(rate=5.0, burst=10, sensitivity=EndpointSensitivity.HIGH))
limiter.set_policy("/api/public", RateLimitPolicy(rate=100.0, burst=200, sensitivity=EndpointSensitivity.LOW))
limiter.set_default_policy(RateLimitPolicy(rate=30.0, burst=50, sensitivity=EndpointSensitivity.MEDIUM))
limiter.authorise_admin("sk-admin-token-abc123")
result = limiter.check("/api/public")
print(result.allowed, result.to_headers())
result = limiter.check("/api/auth")
print(result.allowed, result.retry_after)
limiter.reset_route("/api/auth")
=== WSGI integration ===
from wsgiref.simple_server import make_server
app = RateLimitMiddleware(wsgi_app, limiter)
app.register_endpoint("/auth", "/api/auth")
app.register_endpoint("/public", "/api/public")
=== Flask integration ===
limiter = RateLimiter()
limiter.set_policy("/api/auth", RateLimitPolicy(rate=5.0, burst=10))
limiter.set_policy("/api/public", RateLimitPolicy(rate=100.0, burst=200))
limiter.authorise_admin(os.environ.get("ADMIN_TOKEN", ""))
@rate_limit(route="/api/auth")
@rate_limit.set_limiter(limiter)
def auth_endpoint():
    return {"status": "ok"}
=== Key design decisions ===
Token bucket chosen over sliding window for lower memory per endpoint.
threading.Lock on each bucket avoids GIL contention from a single global lock.
Per-bucket lock allows concurrent check calls on different routes.
Refill calculation uses monotonic clock to avoid system time jumps.
toknes capped at burst to prevent accumulation overflow.
Reset time computed from actual bucket state for accurate Retry-After.
Admin bypass skips bucket entirely -- no token consumption.
All header names follow IETF draft standard format.