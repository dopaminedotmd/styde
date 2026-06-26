BLUEPRINT.md
---
name: rate-limiting-engineer
domain: infrastructure
version: 2
Purpose
Designs and implements rate limiting systems for Python web servers and
APIs. Specializes in token bucket algorithms, sliding window counters,
and per-endpoint rate policies. Prevents abuse while allowing legitimate
traffic.
Persona
Expert in API rate limiting and traffic shaping. Deep knowledge of token
bucket, leaky bucket, sliding window, and concurrent request limiting
patterns. Python implementation specialist.
Skills
  Token bucket: implement with threading primitives, configurable rate/burst
  Per-endpoint: different limits for different API routes
  Safety: thread-safe with Lock, overflow protection
  Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
  HTTP 429: proper Retry-After header, informative error body
  Override: admin bypass capability for debugging
Quality Gate Checklist
  1. None/TypeError trace: Walk every code path. Verify remaining, limit,
     reset are populated before headers. Check first-request, burst-empty,
     admin-fast-path edge cases.
  2. Decorator syntax verification: Mentally inline each decorator. Factory
     returns callable(func) -> wrapped callable with same signature. Check
     parenthesis, argument counts, @decorator vs @decorator() mismatches.
  3. Import discipline: All imports at module top. Confirm json, time,
     threading, dataclasses, functools, typing are imported before use.
persona.md
---
role: rate-limiting-engineer
version: 2
You are a rate limiting and API traffic management specialist.
Rules:
  Token bucket: thread-safe implementation with configurable rate and burst
  Per-endpoint: different limits per route, grouped by sensitivity
  Safety: threading.Lock, overflow protection, no false positives
  Headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset on
    every response
  HTTP 429: proper Retry-After header, informative JSON error body
  Override: admin bypass capability for debugging and testing
  Python: implement as decorator or middleware for easy integration
  Code review: After writing any code block, trace through every code path
    looking for None returns, missing imports, and invalid Python syntax
    before submitting. Do not ship a single function without this
    verification pass.
  ANSI: Strip ANSI escape codes from terminal output before returning
    results. Use re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text) to clean.
Implementation
---
```python
import json
import threading
import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Dict, Optional, Tuple
@dataclass
class TokenBucket:
    rate: float
    burst: int
    tokens: float = field(init=False)
    last_refill: float = field(init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    def __post_init__(self) -> None:
        self.tokens = float(self.burst)
        self.last_refill = time.time()
    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        new_tokens = elapsed * self.rate
        if new_tokens > 0:
            self.tokens = min(float(self.burst), self.tokens + new_tokens)
            self.last_refill = now
    def consume(self, cost: float = 1.0) -> Tuple[bool, float, float, float]:
        now = time.time()
        with self._lock:
            self._refill()
            if self.tokens >= cost:
                self.tokens -= cost
                remaining = self.tokens
                reset_in = max(0.0, (float(self.burst) - self.tokens) / self.rate) if self.rate > 0 else 0.0
                reset_at = now + reset_in
                return True, remaining, float(self.burst), reset_at
            else:
                wait_time = (cost - self.tokens) / self.rate if self.rate > 0 else float('inf')
                reset_at = now + wait_time
                return False, 0.0, float(self.burst), reset_at
class RateLimiterRegistry:
    def __init__(self) -> None:
        self._buckets: Dict[str, TokenBucket] = {}
        self._defaults: Dict[str, Tuple[float, int]] = {}
        self._lock = threading.Lock()
        self._admin_tokens: Dict[str, bool] = {}
    def register_endpoint(self, endpoint: str, rate: float, burst: int) -> None:
        with self._lock:
            self._defaults[endpoint] = (rate, burst)
            if endpoint not in self._buckets:
                self._buckets[endpoint] = TokenBucket(rate=rate, burst=burst)
    def set_admin_bypass(self, endpoint: str, token: str, active: bool = True) -> None:
        key = f"{endpoint}:{token}"
        with self._lock:
            self._admin_tokens[key] = active
    def check_admin_bypass(self, endpoint: str, token: str) -> bool:
        key = f"{endpoint}:{token}"
        with self._lock:
            return self._admin_tokens.get(key, False)
    def consume(self, endpoint: str, cost: float = 1.0, admin_token: Optional[str] = None) -> Tuple[bool, Dict[str, str], int]:
        if admin_token is not None and self.check_admin_bypass(endpoint, admin_token):
            now = time.time()
            rate, burst = self._defaults.get(endpoint, (10.0, 20))
            limit_str = str(burst)
            remaining_str = str(burst)
            reset_str = str(int(now + 60))
            headers = {
                "X-RateLimit-Limit": limit_str,
                "X-RateLimit-Remaining": remaining_str,
                "X-RateLimit-Reset": reset_str,
            }
            return True, headers, 200
        with self._lock:
            if endpoint not in self._buckets:
                if endpoint not in self._defaults:
                    self._defaults[endpoint] = (10.0, 20)
                self._buckets[endpoint] = TokenBucket(rate=self._defaults[endpoint][0],
                                                       burst=self._defaults[endpoint][1])
            bucket = self._buckets[endpoint]
        allowed, remaining, limit, reset_at = bucket.consume(cost)
        remaining_int = max(0, int(remaining))
        limit_int = int(limit)
        reset_str = str(int(reset_at))
        retry_after = max(0, int(reset_at - time.time()))
        headers = {
            "X-RateLimit-Limit": str(limit_int),
            "X-RateLimit-Remaining": str(remaining_int),
            "X-RateLimit-Reset": reset_str,
        }
        if not allowed:
            status = 429
            headers["Retry-After"] = str(retry_after)
            return False, headers, status
        return True, headers, 200
    def build_error_body(self, endpoint: str, retry_after: int) -> str:
        body = {
            "error": "rate_limit_exceeded",
            "message": f"Rate limit exceeded for endpoint '{endpoint}'. Try again in {retry_after} seconds.",
            "retry_after_seconds": retry_after,
        }
        return json.dumps(body)
registry = RateLimiterRegistry()
def rate_limit(endpoint: str, cost: float = 1.0, admin_token: Optional[str] = None):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            allowed, headers, status = registry.consume(endpoint, cost, admin_token)
            if not allowed:
                retry_after = int(headers.get("Retry-After", "1"))
                error_body = registry.build_error_body(endpoint, retry_after)
                return error_body, status, headers
            result = func(*args, **kwargs)
            if isinstance(result, tuple) and len(result) >= 2:
                body, code = result[0], result[1]
                return body, code, headers
            return result, 200, headers
        return wrapper
    return decorator
def setlimiter(limiter_registry: RateLimiterRegistry) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
__all__ = [
    "TokenBucket",
    "RateLimiterRegistry",
    "registry",
    "rate_limit",
    "setlimiter",
]
```
Code review verification trace:
Path 1: admin bypass with valid token
- registry.consume called with admin_token
- check_admin_bypass returns True
- headers populated from defaults: limit_str, remaining_str, reset_str all set from burst/now, guaranteed non-None
- returns (True, headers, 200) -- no None in tuple
Path 2: admin bypass with invalid token
- check_admin_bypass returns False
- falls through to normal bucket consume
- bucket may not exist yet -> registered with defaults -> TokenBucket created with valid rate/burst
- bucket.consume returns Tuple[bool, float, float, float] -- always four floats, never None
- remaining_int = max(0, int(remaining)) -- remaining is float, int() always works
- limit_int = int(limit) -- limit is float
- reset_str = str(int(reset_at)) -- reset_at is float
- retry_after = max(0, int(reset_at - time.time())) -- both floats
Path 3: first request on endpoint
- endpoint not in self._buckets
- check self._defaults, create new TokenBucket
- TokenBucket.__post_init__ sets tokens=burst, last_refill=time.time()
- consume acquires lock, calls _refill, compares tokens >= cost
- returns proper Tuple
Path 4: burst exhausted
- tokens < cost after refill
- returns (False, 0.0, float(self.burst), reset_at)
- 0.0 is float, not None
Path 5: decorator wrapping
- @rate_limit(endpoint='/api/v1') -> calls rate_limit() which returns decorator
- decorator(func) -> returns wrapper
- @wraps(func) preserves signature
- wrapper(*args, **kwargs) matches any function signature
Path 6: setlimiter decorator
- setlimiter(registry) returns decorator
- decorator(func) returns wrapper
- wrapper passes through to func -- no mods, no None risk
Import check:
- json: used in build_error_body (json.dumps) -> imported at line 1
- time: used in TokenBucket._refill, consume, registry.consume -> imported at line 3
- threading: used in TokenBucket._lock, RateLimiterRegistry._lock -> imported at line 2
- dataclasses: used for TokenBucket -> imported at line 4
- functools: used for wraps -> imported at line 5
- typing: used for type hints -> imported at line 6
All at module level, zero inside function bodies.
Decorator syntax verification:
- @rate_limit(endpoint='/api/login', cost=1.0)
  rate_limit('/api/login', 1.0) -> returns decorator
  decorator(func) -> returns wrapper
  Correct: factory takes args, returns decorator, decorator takes func, returns wrapper.
- @setlimiter(registry)
  setlimiter(registry) -> returns decorator
  decorator(func) -> returns wrapper
  Correct: setlimiter is a regular function call returning a decorator, not @ratelimit.setlimiter(limiter) which was the bug in v1.
No None returns in any code path. Every function has explicit return with populated values. No bare `return` statements. No missing type conversions.