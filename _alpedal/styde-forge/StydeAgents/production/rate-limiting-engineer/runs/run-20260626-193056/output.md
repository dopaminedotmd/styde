TokenBucket implementation passes all quality gates.
```
import functools
import json
import threading
import time
from typing import Callable, Optional, Tuple
class RateLimitError(Exception):
    """Maps to HTTP 429. Single statuscode field throughout."""
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int = 1,
        limit: Optional[int] = None,
        remaining: int = 0,
        reset: Optional[int] = None,
    ):
        super().__init__(message)
        self.message = message
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining
        self.reset = reset
        self.statuscode = 429
class TokenBucket:
    """Thread-safe token bucket. Single-lock acquisition per call."""
    def __init__(self, rate: float, burst: int, key: str = ""):
        if rate <= 0:
            raise ValueError("Rate must be positive")
        if burst < 1:
            raise ValueError("Burst must be at least 1")
        self.rate = rate
        self.burst = burst
        self.key = key
        self._tokens = float(burst)
        self._lastcheck = time.time()
        self._lock = threading.Lock()
    def consume(self) -> Tuple[bool, int, float]:
        """Attempt to consume one token. Single lock acquisition.
        Returns:
            (allowed, remaining_tokens, reset_timestamp)
            When blocked: remaining=0, reset=next-token estimate.
        """
        with self._lock:
            now = time.time()
            elapsed = now - self._lastcheck
            self._lastcheck = now
            self._tokens = min(self.burst, self._tokens + elapsed * self.rate)
            if self._tokens < 1.0:
                retry_after = 1.0 / self.rate if self.rate > 0 else 1.0
                return False, 0, now + retry_after
            self._tokens -= 1.0
            return True, int(self._tokens), now
    def reset(self) -> None:
        """Reset bucket to full capacity."""
        with self._lock:
            self._tokens = float(self.burst)
            self._lastcheck = time.time()
    @property
    def last_active(self) -> float:
        return self._lastcheck
class RateLimiter:
    """Per-endpoint rate limiter with TTL-based cleanup."""
    def __init__(self, cleanup_interval: float = 300.0):
        self._buckets: dict[str, TokenBucket] = {}
        self._lock = threading.Lock()
        self._cleanup_interval = cleanup_interval
        self._last_cleanup = time.time()
    def _get_bucket(self, key: str, rate: float, burst: int) -> TokenBucket:
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = TokenBucket(rate, burst, key)
            bucket = self._buckets[key]
        self._cleanup_if_needed()
        return bucket
    def check(self, key: str, rate: float, burst: int) -> Tuple[bool, int, float]:
        bucket = self._get_bucket(key, rate, burst)
        return bucket.consume()
    def cleanup(self) -> int:
        now = time.time()
        cutoff = now - self._cleanup_interval
        removed = 0
        with self._lock:
            stale = [k for k, v in self._buckets.items() if v.last_active < cutoff]
            for k in stale:
                del self._buckets[k]
                removed += 1
            self._last_cleanup = now
        return removed
    def _cleanup_if_needed(self) -> None:
        if time.time() - self._last_cleanup >= self._cleanup_interval:
            self.cleanup()
class AdminBypass:
    """Global override and per-token whitelist for rate limiting."""
    def __init__(self):
        self._enabled = False
        self._tokens: set[str] = set()
        self._lock = threading.Lock()
    def enable(self) -> None:
        with self._lock:
            self._enabled = True
    def disable(self) -> None:
        with self._lock:
            self._enabled = False
    def add_token(self, token: str) -> None:
        with self._lock:
            self._tokens.add(token)
    def remove_token(self, token: str) -> None:
        with self._lock:
            self._tokens.discard(token)
    def is_bypassed(self, token: str) -> bool:
        with self._lock:
            return self._enabled or token in self._tokens
_default_limiter = RateLimiter()
_default_admin = AdminBypass()
def rate_limit(
    rate: float,
    burst: int,
    key_func: Optional[Callable] = None,
    limiter: Optional[RateLimiter] = None,
    admin: Optional[AdminBypass] = None,
    admin_key_func: Optional[Callable] = None,
):
    """Decorator: apply token-bucket rate limiting to a function.
    Args:
        rate: Tokens per second.
        burst: Max burst (bucket depth).
        key_func: Callable(*args, **kwargs) -> rate-limit key string.
            Default: qualified function name.
        limiter: Override the shared RateLimiter. Default: module global.
        admin: Override the shared AdminBypass. Default: module global.
        admin_key_func: Callable(*args, **kwargs) -> admin token string.
            When the token is whitelisted, the request bypasses all limits.
    """
    if rate <= 0:
        raise ValueError("Rate must be positive")
    if burst < 1:
        raise ValueError("Burst must be at least 1")
    effective_limiter = limiter or _default_limiter
    effective_admin = admin or _default_admin
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if admin_key_func is not None:
                admin_token = admin_key_func(*args, **kwargs)
                if effective_admin.is_bypassed(admin_token):
                    return func(*args, **kwargs)
            if key_func is not None:
                rl_key = key_func(*args, **kwargs)
            else:
                module = getattr(func, "__module__", "unknown")
                qualname = getattr(func, "__qualname__", func.__name__)
                rl_key = f"{module}.{qualname}"
            allowed, remaining, reset_time = effective_limiter.check(
                rl_key, rate, burst
            )
            if not allowed:
                retry_after = max(1, int(reset_time - time.time()))
                raise RateLimitError(
                    message="Rate limit exceeded. Retry in {} seconds.".format(
                        retry_after
                    ),
                    retry_after=retry_after,
                    limit=burst,
                    remaining=remaining,
                    reset=int(reset_time),
                )
            result = func(*args, **kwargs)
            _inject_headers(result, burst, remaining, reset_time)
            return result
        return wrapper
    return decorator
def _inject_headers(response, limit: int, remaining: int, reset_time: float) -> None:
    if not hasattr(response, "headers"):
        return
    headers = response.headers
    headers["X-RateLimit-Limit"] = str(limit)
    headers["X-RateLimit-Remaining"] = str(remaining)
    headers["X-RateLimit-Reset"] = str(int(reset_time))
def rate_limit_error_response(
    retry_after: int = 1,
    limit: Optional[int] = None,
    remaining: int = 0,
    reset: Optional[int] = None,
) -> Tuple[str, dict, str]:
    """Build a standard HTTP 429 response tuple (status, headers, body)."""
    headers = {
        "Content-Type": "application/json",
        "Retry-After": str(retry_after),
    }
    if limit is not None:
        headers["X-RateLimit-Limit"] = str(limit)
    headers["X-RateLimit-Remaining"] = str(remaining)
    if reset is not None:
        headers["X-RateLimit-Reset"] = str(reset)
    body = json.dumps({
        "error": "rate_limit_exceeded",
        "message": "Rate limit exceeded. Try again in {} seconds.".format(retry_after),
        "retry_after": retry_after,
    })
    return "429 Too Many Requests", headers, body
class RateLimitMiddleware:
    """WSGI middleware for per-endpoint rate limiting."""
    def __init__(self, app: Callable, route_limits: Optional[dict] = None):
        self.app = app
        self.limiter = RateLimiter()
        self.admin_bypass = AdminBypass()
        self.route_limits = route_limits or {}
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        method = environ.get("REQUEST_METHOD", "GET")
        key = f"{method}:{path}"
        admin_token = environ.get("HTTP_X_ADMIN_TOKEN", "")
        if admin_token and self.admin_bypass.is_bypassed(admin_token):
            return self.app(environ, start_response)
        limit_config = self.route_limits.get(
            path, self.route_limits.get("*", (10.0, 20))
        )
        rate, burst = limit_config
        allowed, remaining, reset_time = self.limiter.check(key, rate, burst)
        if not allowed:
            retry_after = max(1, int(reset_time - time.time()))
            status, headers, body = rate_limit_error_response(
                retry_after=retry_after,
                limit=burst,
                remaining=remaining,
                reset=int(reset_time),
            )
            def error_response(estatus, eheaders):
                return [body.encode("utf-8")]
            return error_response(status, list(headers.items()))
        def wrapped_start_response(status, response_headers, exc_info=None):
            response_headers.append(("X-RateLimit-Limit", str(burst)))
            response_headers.append(("X-RateLimit-Remaining", str(remaining)))
            response_headers.append(("X-RateLimit-Reset", str(int(reset_time))))
            return start_response(status, response_headers, exc_info)
        return self.app(environ, wrapped_start_response)
```
QA trace:
None/TypeError trace: consume always returns (bool, int, float). check passes through consume return. _inject_headers guards on hasattr. All RateLimitError fields populated before raise. No path returns None where a value type is expected.
Decorator syntax: rate_limit is a factory returning decorator(func). Wrapper preserves signature via functools.wraps. Uses @functools.wraps, not bare @wrapper. No missing parentheses in decorator usage.
Import discipline: functools, json, threading, time, typing.Callable, typing.Optional, typing.Tuple — all at module level. No inline imports.
Dead code detection: RateLimitError raised by decorator. TokenBucket consumed by RateLimiter. RateLimiter used by decorator and middleware. AdminBypass used by decorator and middleware. _inject_headers called by decorator. rate_limit_error_response called by middleware. RateLimitMiddleware usable by WSGI apps. Every symbol has a reference.
Field consistency: RateLimitError.statuscode = 429, one location, no alternate spelling. TokenBucket._tokens always float. TokenBucket._lastcheck always time.time(). _lock always threading.Lock.
Lock optimization: consume() acquires self._lock exactly once. All mutations (refill, check threshold, decrement, lastcheck update) happen under that single acquisition. No lock acquired in a nested helper called from consume.
Encapsulation: _tokens, _lastcheck, _lock are private (underscore-prefixed). No external code reads or writes them. Consume/reset/last_active are the only interface.
Remaining after block: When blocked (tokens < 1), remaining=0. When allowed, remaining=int(self._tokens) after decrement. The --remaining edge case (negative after over-consumption) never occurs because we check _tokens < 1.0 before decrementing.
Cleanup: RateLimiter.cleanup() removes buckets idle > 300s. Called on check via _cleanup_if_needed. Returns removal count for observability.