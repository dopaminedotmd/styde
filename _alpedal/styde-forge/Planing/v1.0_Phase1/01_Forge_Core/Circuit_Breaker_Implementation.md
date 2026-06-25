# Circuit Breaker Implementation

**Styde Forge v3.0**
**Section:** 01_Forge_Core
**References:** `Core_Loop_Detail.md` §7, `DECISIONS.md` D11

---

## 1. Purpose

Prevent cascade failures. If loop keeps failing, STOP — don't waste API money. Per-blueprint + global breakers.

---

## 2. States

```
closed ──[failures ≥ threshold]──→ open ──[timeout elapsed]──→ half_open
  ↑                                                              │
  └──────────────────[success]────────────────────────────────────┘
```

---

## 3. Implementation (Core/circuit_breaker.py)

```python
import time

class CircuitBreaker:
    """Per-blueprint or global circuit breaker."""
    
    def __init__(self, name: str, failure_threshold: int = 5, reset_timeout_min: int = 30):
        self.name = name
        self.threshold = failure_threshold
        self.reset_timeout = reset_timeout_min * 60
        self.failures = 0
        self.last_failure = None
        self.state = "closed"

    def record_failure(self):
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.threshold:
            self.state = "open"

    def record_success(self):
        if self.state == "half_open":
            self.state = "closed"
            self.failures = 0
        elif self.state == "closed":
            self.failures = max(0, self.failures - 1)

    def allow_request(self) -> bool:
        if self.state == "closed":
            return True
        if self.state == "open":
            if self.last_failure and (time.time() - self.last_failure > self.reset_timeout):
                self.state = "half_open"
                return True
            return False
        return True

# Breaker registry
_breakers: dict[str, CircuitBreaker] = {}

def get_breaker(name: str, threshold: int = 5) -> CircuitBreaker:
    if name not in _breakers:
        _breakers[name] = CircuitBreaker(name, threshold)
    return _breakers[name]

# Pre-configured
get_blueprint_breaker = lambda bp: get_breaker(f"blueprint:{bp}", 3)
get_global_breaker = lambda: get_breaker("global", 5)
```

---

## 4. Triggers

| Event | Breaker | Threshold |
|-------|---------|-----------|
| 3 consecutive eval < 70 | Per-blueprint | 3 → open |
| 5 API errors in 10 min | Global | 5 → open |
| delegate_task timeout 3× | Per-blueprint | 3 → open |
| Disk full | Global | 1 → open |

---

## 5. Integration

```python
# In forge.py cmd_loop():
breaker = get_blueprint_breaker(blueprint_name)
if not breaker.allow_request():
    print(f"BREAKER OPEN: {blueprint_name}. Skipping.")
    return

try:
    cmd_spawn(...)
    cmd_eval(...)
    cmd_improve(...)
    breaker.record_success()
except Exception:
    breaker.record_failure()
```

---

**Status:** Specification complete. Code in Core/circuit_breaker.py.
