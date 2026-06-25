# Resource Governor

**Styde Forge v3.0 — Phase 0**
**Section:** 02_Hardware

---

## 1. Purpose

Prevent resource exhaustion (VRAM, RAM, disk) during continuous multi-week
operation. The Resource Governor enforces limits, throttles when needed,
and alerts when thresholds are breached.

---

## 2. Resource Limits

| Resource | Machine-A Limit | Machine-B Limit | Action on Breach |
|----------|-----------------|-----------------|------------------|
| VRAM | 30 GB (88%) | 15 GB (83%) | Reduce parallel workers |
| RAM | 55 GB (86%) | 26 GB (81%) | Flush caches, reduce batch |
| Disk (USB) | 45 GB (94%) | 45 GB (94%) | Trigger maintenance |
| CPU temp | 85°C | 85°C | Pause + cool down |

---

## 3. Governor Logic

```python
class ResourceGovernor:
    def __init__(self, hardware_profile: str):
        self.limits = self._load_limits(hardware_profile)
        self.violations = 0
        self.throttle_level = 0  # 0=none, 1=light, 2=heavy, 3=emergency

    def check(self) -> str:
        """Check all resources. Return 'ok', 'warn', or 'critical'."""
        status = "ok"

        if self._vram_usage() > self.limits["vram_warn"]:
            status = "warn"
            self.violations += 1

        if self._vram_usage() > self.limits["vram_critical"]:
            status = "critical"
            self._emergency_throttle()

        if self._ram_usage() > self.limits["ram_warn"]:
            status = "warn"

        if self._disk_usage() > self.limits["disk_warn"]:
            status = "warn"
            self._request_maintenance()

        return status

    def _emergency_throttle(self):
        """Reduce all parallel activity immediately."""
        self.throttle_level = 3
        # Kill non-essential subagents
        # Flush all caches
        # Force checkpoint immediately
```

---

## 4. Throttle Levels

| Level | Name | Workers | Sampling | Models |
|-------|------|---------|----------|--------|
| 0 | Normal | Full | Full | Full |
| 1 | Light | -1 worker | Reduced samples | Smaller models |
| 2 | Heavy | 1 worker | VI only | Minimal models |
| 3 | Emergency | 0 workers | Paused | Paused |

---

## 5. Alerts

| Condition | Alert |
|-----------|-------|
| VRAM > 85% for 5 min | Self-Monitoring warning |
| Disk > 90% | Trigger maintenance cycle |
| 3 consecutive throttle events | Teacher alert + log |
| Temperature > 85°C | Immediate pause |

---

**Status:** Defined. To be implemented with Hardware Adaptation Layer.
