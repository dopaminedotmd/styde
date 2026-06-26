```python
"""
rate_limit.py — Thread-safe token bucket rate limiter for Python web services.
Exports:
  TokenBucket         Thread-safe token bucket with configurable rate & burst.
  RateLimitConfig     Per-endpoint configuration dataclass.
  RateLimitError      Exception with consistent .statuscode and .retry_after.
  rate_limit          Decorator that applies a named config.
  RateLimiterMiddleware  WSGI middleware (callable) for per-endpoint limits.
  AdminBypass         Decorator/middleware flag to skip rate checks.
  RateLimitExceeded   Alias for 429 JSON body builder.
  BucketOverflow      Raised when token addition exceeds safe ceiling.
"""
import json
import threading
import time
import weakref
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
# ---------------------------------------------------------------------------
# Exceptions with guaranteed .statuscode and .retry_after fields
# ---------------------------------------------------------------------------
class RateLimitError(Exception):
    """Raised (or set on request) when a client exceeds its rate limit.
    Every instance carries .statuscode (429) and .retry_after (int).
    """
    def __init__(self, retry_after: int = 1, detail: str = "") -> None:
        self.statuscode: int = 429
        self.retry_after: int = retry_after
        self.detail: str = detail or "Rate limit exceeded. Try again later."
        super().__init__(self.detail)
    def to_json(self) -> str:
        return json.dumps({
            "error": "rate_limit_exceeded",
            "statuscode": self.statuscode,
            "retry_after": self.retry_after,
            "detail": self.detail,
        })
    @classmethod
    def from_retry_after(cls, retry_after: int, detail: str = "") -> "RateLimitError":
        return cls(retry_after=retry_after, detail=detail)
class BucketOverflow(Exception):
    """Raised when a token addition would overflow the configured max burst.
    This is a safety valve, not a client-facing error — it indicates a
    programming bug (e.g. negative rate config or runaway fill).
    """
    def __init__(self, bucket_name: str = "", current: float = 0.0, ceiling: float = 0.0) -> None:
        self.statuscode: int = 500
        self.bucket_name: str = bucket_name
        self.current: float = current
        self.ceiling: float = ceiling
        super().__init__(f"Bucket overflow on '{bucket_name}': {current:.2f} > {ceiling:.2f}")
# ---------------------------------------------------------------------------
# Token bucket — thread-safe, idle cleanup via weakref
# ---------------------------------------------------------------------------
class TokenBucket:
    """Token bucket with rate & burst control.
    Thread-safe via threading.Lock.  Idle buckets are automatically evicted
    from the bucket registry when their last external reference is dropped.
    """
    __slots__ = ("_rate", "_burst", "_tokens", "_last_refill",
                 "_lock", "_name", "__weakref__")
    def __init__(self, rate: float, burst: float, name: str = "") -> None:
        if rate <= 0:
            raise ValueError(f"rate must be > 0, got {rate}")
        if burst <= 0:
            raise ValueError(f"burst must be > 0, got {burst}")
        self._rate: float = rate
        self._burst: float = burst
        self._tokens: float = float(burst)
        self._last_refill: float = time.monotonic()
        self._lock: threading.Lock = threading.Lock()
        self._name: str = name
    @property
    def rate(self) -> float:
        return self._rate
    @property
    def burst(self) -> float:
        return self._burst
    @property
    def name(self) -> str:
        return self._name
    def _refill(self, now: float) -> None:
        elapsed = now - self._last_refill
        if elapsed > 0:
            added = elapsed * self._rate
            self._tokens = min(self._tokens + added, self._burst)
            self._last_refill = now
    def consume(self, tokens: float = 1.0) -> bool:
        """Try to consume *tokens*. Returns True if allowed, False otherwise.
        Thread-safe.  Refills opportunistically on every call.
        """
        if tokens <= 0:
            return True
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False
    def remaining(self) -> float:
        """Return the current token count (approximate, best-effort)."""
        with self._lock:
            self._refill(time.monotonic())
            return self._tokens
    def reset_time(self) -> float:
        """Return the estimated monotonic time when the bucket will be full."""
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            deficit = self._burst - self._tokens
            if deficit <= 0:
                return now
            return now + (deficit / self._rate)
    def force_add(self, tokens: float) -> None:
        """Add tokens without exceeding burst.  Raise BucketOverflow on overflow."""
        if tokens <= 0:
            return
        with self._lock:
            now = time.monotonic()
            self._refill(now)
            new_val = self._tokens + tokens
            if new_val > self._burst * 1.05:  # 5 % tolerance for rounding
                raise BucketOverflow(
                    bucket_name=self._name,
                    current=new_val,
                    ceiling=self._burst,
                )
            self._tokens = min(new_val, self._burst)
    def set_burst(self, burst: float) -> None:
        with self._lock:
            self._burst = burst
            self._tokens = min(self._tokens, self._burst)
    def set_rate(self, rate: float) -> None:
        with self._lock:
            self._rate = rate
    def __repr__(self) -> str:
        remaining = self.remaining()
        return (
            f"TokenBucket(name={self._name!r}, rate={self._rate}, "
            f"burst={self._burst}, remaining={remaining:.2f})"
        )
# ---------------------------------------------------------------------------
# Per-endpoint configuration
# ---------------------------------------------------------------------------
@dataclass
class RateLimitConfig:
    """Configuration for a single endpoint or named limit group."""
    rate: float              # tokens per second
    burst: float             # max accumulated tokens
    group: str = "default"   # logical group for shared buckets
    description: str = ""    # human-readable purpose
    def __post_init__(self) -> None:
        if self.rate <= 0:
            raise ValueError(f"rate must be > 0, got {self.rate}")
        if self.burst <= 0:
            raise ValueError(f"burst must be > 0, got {self.burst}")
        self._validate()
    def _validate(self) -> None:
        if self.rate > self.burst * 100:
            raise ValueError(
                f"rate ({self.rate}) is unreasonably high relative to "
                f"burst ({self.burst}); max recommended ratio is 100:1"
            )
# ---------------------------------------------------------------------------
# Admin bypass
# ---------------------------------------------------------------------------
class AdminBypass:
    """Inspectable flag for skipping rate checks.
    Usage:
        if not AdminBypass.is_active(request):
            limiter.check(request)
    """
    _header: str = "X-Admin-Bypass"
    _token: str = ""  # set at startup; empty = bypass disabled
    @classmethod
    def configure(cls, header: str = "X-Admin-Bypass", token: str = "") -> None:
        cls._header = header
        cls._token = token
    @classmethod
    def is_active(cls, headers: dict) -> bool:
        if not cls._token:
            return False
        return headers.get(cls._header, "") == cls._token
    @classmethod
    def active_token(cls) -> str:
        return cls._token
# ---------------------------------------------------------------------------
# Bucket registry — manages per-key buckets with automatic idle cleanup
# ---------------------------------------------------------------------------
class _BucketRegistry:
    """Internal registry that evicts unreferenced buckets."""
    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._buckets: dict[str, weakref.ref] = {}
        self._lifetimes: dict[str, float] = {}
        self._cleanup_interval: float = 300.0  # seconds
    def get_or_create(self, key: str, config: RateLimitConfig) -> TokenBucket:
        candidate = self._buckets.get(key)
        bucket = candidate() if candidate is not None else None  # dereference weakref
        if bucket is None:
            bucket = TokenBucket(
                rate=config.rate,
                burst=config.burst,
                name=key,
            )
            with self._lock:
                self._buckets[key] = weakref.ref(bucket)
                self._lifetimes[key] = time.monotonic()
        return bucket
    def cleanup_idle(self, max_idle: float = 3600.0) -> int:
        """Remove buckets that have been idle longer than *max_idle* seconds.
        Returns the number of buckets removed.
        """
        now = time.monotonic()
        removed = 0
        with self._lock:
            stale = [k for k, t in self._lifetimes.items()
                     if now - t > max_idle]
            for k in stale:
                ref = self._buckets.get(k)
                if ref is not None:
                    bucket = ref()
                    if bucket is not None:
                        remaining = bucket.remaining()
                        # only evict if bucket is mostly full (idle)
                        if remaining >= bucket.burst * 0.95:
                            del self._buckets[k]
                            del self._lifetimes[k]
                            removed += 1
        return removed
    def touch(self, key: str) -> None:
        with self._lock:
            self._lifetimes[key] = time.monotonic()
# ---------------------------------------------------------------------------
# Core limiter
# ---------------------------------------------------------------------------
class RateLimiter:
    """Central rate limiter holding a registry of per-endpoint configs.
    Thread-safe.  Supports decorator and middleware usage patterns.
    """
    def __init__(self) -> None:
        self._configs: dict[str, RateLimitConfig] = {}
        self._registry: _BucketRegistry = _BucketRegistry()
        self._lock: threading.Lock = threading.Lock()
    def add_config(self, name: str, config: RateLimitConfig) -> None:
        with self._lock:
            self._configs[name] = config
    def get_config(self, name: str) -> Optional[RateLimitConfig]:
        return self._configs.get(name)
    def check(self, key: str, config_name: str = "default",
              tokens: float = 1.0, headers: Optional[dict] = None) -> None:
        """Check rate limit for *key* (typically client IP + endpoint).
        Raises RateLimitError if the limit is exceeded.
        Otherwise returns None.
        """
        if headers is not None and AdminBypass.is_active(headers):
            return
        config = self._configs.get(config_name)
        if config is None:
            return  # no limit configured → allow
        bucket = self._registry.get_or_create(key, config)
        if not bucket.consume(tokens):
            retry_after = int(bucket.reset_time() - time.monotonic()) + 1
            raise RateLimitError(retry_after=retry_after)
        self._registry.touch(key)
    def headers(self, key: str, config_name: str = "default") -> dict[str, str]:
        """Return standard rate-limit response headers for *key*."""
        config = self._configs.get(config_name)
        if config is None:
            return {}
        bucket = self._registry.get_or_create(key, config)
        remaining = max(0, int(bucket.remaining()))
        reset = int(bucket.reset_time())
        return {
            "X-RateLimit-Limit": str(int(config.burst)),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset),
        }
    def cleanup_idle(self, max_idle: float = 3600.0) -> int:
        return self._registry.cleanup_idle(max_idle)
# ---------------------------------------------------------------------------
# Global limiter singleton — used by decorator and middleware
# ---------------------------------------------------------------------------
_limiter: RateLimiter = RateLimiter()
def get_limiter() -> RateLimiter:
    return _limiter
def configure(configs: dict[str, dict]) -> None:
    """Bulk-configure rate limits from a dict of name -> {rate, burst, ...}."""
    for name, params in configs.items():
        _limiter.add_config(name, RateLimitConfig(**params))
# ---------------------------------------------------------------------------
# Decorator-based rate limiting
# ---------------------------------------------------------------------------
def rate_limit(config_name: str = "default", tokens: float = 1.0,
               key_func: Optional[Callable[..., str]] = None) -> Callable:
    """Decorator that enforces a named rate limit on the wrapped function.
    *key_func* receives (*args, **kwargs) and returns a bucket key string.
    Default key is the function's module-qualified name.
    Raises RateLimitError (429) when the limit is exceeded.
    """
    if tokens <= 0:
        raise ValueError("tokens must be > 0")
    def decorator(func: Callable) -> Callable:
        func_key = f"{func.__module__}.{func.__qualname__}"
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = key_func(*args, **kwargs) if key_func is not None else func_key
            _limiter.check(key, config_name=config_name, tokens=tokens)
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__module__ = func.__module__
        wrapper.__doc__ = func.__doc__
        wrapper.__wrapped__ = func  # type: ignore[attr-defined]
        return wrapper
    return decorator
# ---------------------------------------------------------------------------
# WSGI middleware
# ---------------------------------------------------------------------------
class RateLimiterMiddleware:
    """WSGI middleware that enforces per-endpoint rate limits.
    Usage:
        app = RateLimiterMiddleware(wsgi_app, {
            "/api/v1/login":    RateLimitConfig(rate=2, burst=5, group="auth"),
            "/api/v1/register": RateLimitConfig(rate=1, burst=3, group="auth"),
        })
    """
    def __init__(self, app: Callable, endpoint_configs: Optional[dict[str, RateLimitConfig]] = None,
                 header_func: Optional[Callable[[str, dict], str]] = None) -> None:
        self._app: Callable = app
        self._endpoint_configs: dict[str, RateLimitConfig] = endpoint_configs or {}
        self._header_func: Callable[[str, dict], str] = header_func or _default_client_ip
        self._limiter: RateLimiter = get_limiter()
        for name, config in self._endpoint_configs.items():
            self._limiter.add_config(name, config)
    def __call__(self, environ: dict, start_response: Callable) -> list:
        path = environ.get("PATH_INFO", "/")
        config = self._resolve_config(path)
        client_ip = self._header_func(environ)
        headers_to_check = {
            "X-Admin-Bypass": environ.get("HTTP_X_ADMIN_BYPASS", ""),
        }
        if config is not None:
            key = f"{config.group}:{client_ip}"
            try:
                self._limiter.check(key, config_name=path, tokens=1.0,
                                    headers=headers_to_check)
            except RateLimitError as exc:
                body = exc.to_json().encode("utf-8")
                rh = {
                    "X-RateLimit-Limit": str(int(config.burst)),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + exc.retry_after)),
                    "Retry-After": str(exc.retry_after),
                    "Content-Type": "application/json",
                }
                status = "429 Too Many Requests"
                start_response(status, list(rh.items()))
                return [body]
            rl_headers = self._limiter.headers(key, config_name=path)
            def _start_response_with_headers(status: str, headers: list, exc_info: Any = None) -> Any:
                for hdr_key, hdr_val in rl_headers.items():
                    headers.append((hdr_key, hdr_val))
                return start_response(status, headers, exc_info)
            return self._app(environ, _start_response_with_headers)
        return self._app(environ, start_response)
    def _resolve_config(self, path: str) -> Optional[RateLimitConfig]:
        # exact match first, then prefix match
        if path in self._endpoint_configs:
            return self._endpoint_configs[path]
        for prefix, config in self._endpoint_configs.items():
            if path.startswith(prefix):
                return config
        return None
def _default_client_ip(environ: dict) -> str:
    return environ.get("REMOTE_ADDR", "127.0.0.1")
# ---------------------------------------------------------------------------
# Convenience: build a 429 JSON response without raising
# ---------------------------------------------------------------------------
def build_rate_limit_response(retry_after: int = 1, detail: str = "") -> tuple:
    """Return (body_bytes, headers_dict) for a standard 429 response."""
    err = RateLimitError(retry_after=retry_after, detail=detail)
    return err.to_json().encode("utf-8"), {
        "Content-Type": "application/json",
        "Retry-After": str(retry_after),
        "X-RateLimit-Limit": "0",
        "X-RateLimit-Remaining": "0",
        "X-RateLimit-Reset": str(int(time.time() + retry_after)),
    }
# ---------------------------------------------------------------------------
# Idle-cleanup worker (call periodically from a background thread)
# ---------------------------------------------------------------------------
def _cleanup_worker(interval: float = 300.0, max_idle: float = 3600.0) -> None:
    while True:
        time.sleep(interval)
        get_limiter().cleanup_idle(max_idle=max_idle)
# ---------------------------------------------------------------------------
# Module-level verification — auto-run on import to catch dead code / mislinks
# ---------------------------------------------------------------------------
def _verify_invariants() -> None:
    """Dead-code pass: confirm every exported symbol references an existing class.
    Also verifies that every exception class carries .statuscode and .retry_after.
    """
    _exports = {
        "TokenBucket", "RateLimitConfig", "RateLimitError",
        "rate_limit", "RateLimiterMiddleware", "AdminBypass",
        "RateLimitExceeded", "BucketOverflow", "get_limiter", "configure",
        "build_rate_limit_response", "RateLimiter",
    }
    _locals = set(globals().keys())
    _unresolved = _exports - _locals
    if _unresolved:
        raise RuntimeError(f"Dead-code violation — exported but undefined: {_unresolved}")
    # Verify exception field consistency
    for exc_cls in (RateLimitError, BucketOverflow):
        inst = exc_cls()
        if not hasattr(inst, "statuscode"):
            raise RuntimeError(f"{exc_cls.__name__} missing .statuscode")
        if inst.statuscode is None:
            raise RuntimeError(f"{exc_cls.__name__}.statuscode is None")
    # Verify AdminBypass interface
    assert hasattr(AdminBypass, "is_active")
    assert hasattr(AdminBypass, "configure")
    # Verify BucketOverflow has .retry_after for consistency
    bo = BucketOverflow()
    if not hasattr(bo, "retry_after"):
        raise RuntimeError("BucketOverflow missing .retry_after")
_verify_invariants()
# Re-export for convenience
RateLimitExceeded = RateLimitError
```