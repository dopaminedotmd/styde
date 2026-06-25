"""
Circuit breaker: per-blueprint + global failure protection.

States: closed → open → half_open → closed
Triggers: consecutive eval failures, API errors, timeouts.
"""
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent

# Default thresholds
DEFAULT_MAX_FAILURES = 3
DEFAULT_COOLDOWN_SECONDS = 300  # 5 minutes
DEFAULT_HALF_OPEN_MAX = 1  # 1 trial before full open
DEFAULT_GLOBAL_MAX_FAILURES = 5
DEFAULT_GLOBAL_WINDOW_SECONDS = 600  # 10 minutes


class CircuitBreaker:
    """Per-blueprint circuit breaker."""

    def __init__(
        self,
        name: str,
        max_failures: int = DEFAULT_MAX_FAILURES,
        cooldown_seconds: int = DEFAULT_COOLDOWN_SECONDS,
    ):
        self.name = name
        self.max_failures = max_failures
        self.cooldown_seconds = cooldown_seconds
        self.state = "closed"
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.last_state_change = time.time()
        self.total_failures = 0
        self.total_successes = 0

    def record_failure(self) -> str:
        """Record a failure. Returns new state."""
        self.failure_count += 1
        self.total_failures += 1
        self.last_failure_time = time.time()

        if self.state == "half_open":
            # Half-open failure → back to open
            self.state = "open"
            self.last_state_change = time.time()
        elif self.state == "closed" and self.failure_count >= self.max_failures:
            self.state = "open"
            self.last_state_change = time.time()

        return self.state

    def record_success(self) -> str:
        """Record a success. Returns new state."""
        self.total_successes += 1

        if self.state == "half_open":
            self.state = "closed"
            self.failure_count = 0
            self.last_state_change = time.time()
        elif self.state == "closed":
            self.failure_count = 0  # Reset on success

        return self.state

    def can_proceed(self) -> bool:
        """Check if operation can proceed."""
        if self.state == "closed":
            return True

        if self.state == "open":
            # Check cooldown
            if self.last_failure_time is None:
                self.last_failure_time = time.time()
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.cooldown_seconds:
                self.state = "half_open"
                self.last_state_change = time.time()
                return True
            return False

        if self.state == "half_open":
            return True

        return False

    def reset(self):
        """Force reset to closed state."""
        self.state = "closed"
        self.failure_count = 0
        self.last_failure_time = None
        self.last_state_change = time.time()

    def status(self) -> dict:
        """Get current status."""
        return {
            "name": self.name,
            "state": self.state,
            "failure_count": self.failure_count,
            "total_failures": self.total_failures,
            "total_successes": self.total_successes,
            "last_failure": (
                datetime.fromtimestamp(self.last_failure_time, tz=timezone.utc).isoformat()
                if self.last_failure_time
                else None
            ),
            "last_state_change": datetime.fromtimestamp(
                self.last_state_change, tz=timezone.utc
            ).isoformat(),
            "cooldown_remaining": (
                max(0, self.cooldown_seconds - (time.time() - (self.last_failure_time or 0)))
                if self.state == "open" and self.last_failure_time
                else 0
            ),
        }


class GlobalCircuitBreaker:
    """Global circuit breaker — protects against systemic failures."""

    def __init__(
        self,
        max_failures: int = DEFAULT_GLOBAL_MAX_FAILURES,
        window_seconds: int = DEFAULT_GLOBAL_WINDOW_SECONDS,
    ):
        self.max_failures = max_failures
        self.window_seconds = window_seconds
        self.state = "closed"
        self.failure_times: list[float] = []
        self.last_state_change = time.time()

    def record_failure(self) -> str:
        """Record a global failure. Returns new state."""
        now = time.time()
        self.failure_times.append(now)
        # Prune old failures outside window
        cutoff = now - self.window_seconds
        self.failure_times = [t for t in self.failure_times if t >= cutoff]

        if self.state == "closed" and len(self.failure_times) >= self.max_failures:
            self.state = "open"
            self.last_state_change = now
        elif self.state == "half_open":
            self.state = "open"
            self.last_state_change = now

        return self.state

    def record_success(self) -> str:
        """Record global success."""
        if self.state == "half_open":
            self.state = "closed"
            self.failure_times.clear()
            self.last_state_change = time.time()
        return self.state

    def can_proceed(self) -> bool:
        """Check if system can proceed."""
        if self.state == "closed":
            return True
        if self.state == "open":
            # Auto-transition to half_open after window
            if self.last_state_change + self.window_seconds < time.time():
                self.state = "half_open"
                self.last_state_change = time.time()
                return True
            return False
        return True  # half_open

    def reset(self):
        """Force reset."""
        self.state = "closed"
        self.failure_times.clear()
        self.last_state_change = time.time()

    def status(self) -> dict:
        """Get current status."""
        return {
            "name": "global",
            "state": self.state,
            "recent_failures": len(self.failure_times),
            "max_failures": self.max_failures,
            "window_seconds": self.window_seconds,
            "last_state_change": datetime.fromtimestamp(
                self.last_state_change, tz=timezone.utc
            ).isoformat(),
        }


# --- Blueprint breaker registry ---

_breakers: dict[str, CircuitBreaker] = {}
_global_breaker: Optional[GlobalCircuitBreaker] = None


def get_breaker(blueprint_name: str) -> CircuitBreaker:
    """Get or create circuit breaker for a blueprint."""
    if blueprint_name not in _breakers:
        _breakers[blueprint_name] = CircuitBreaker(name=blueprint_name)
    return _breakers[blueprint_name]


def get_global_breaker() -> GlobalCircuitBreaker:
    """Get or create global circuit breaker."""
    global _global_breaker
    if _global_breaker is None:
        _global_breaker = GlobalCircuitBreaker()
    return _global_breaker


def all_breakers() -> dict[str, dict]:
    """Get status of all breakers."""
    result = {}
    for name, breaker in _breakers.items():
        result[name] = breaker.status()
    if _global_breaker:
        result["_global"] = _global_breaker.status()
    return result


def reset_all():
    """Reset all circuit breakers."""
    for breaker in _breakers.values():
        breaker.reset()
    if _global_breaker:
        _global_breaker.reset()
