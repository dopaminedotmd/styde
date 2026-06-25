# System Startup & Shutdown Sequence

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Startup Sequence

Exact order of operations when Styde Forge starts:

```
1. LOAD STATE
   └── Read state.yaml → get version, profile, iterations

2. DETECT HARDWARE
   └── nvidia-smi → GPU names, VRAM
   └── psutil → RAM, CPU cores
   └── Classify: Machine-A (≥28GB VRAM) or Machine-B (<28GB)

3. MATCH PROFILE
   └── hardware/profiles.yaml → adaptations
   └── Set: sampling method, tree depth, models, concurrency

4. VALIDATE CREDENTIALS
   └── Check DEEPSEEK_API_KEY exists
   └── Warn if optional keys missing (ANTHROPIC, XAI)
   └── Test API connectivity (quick health check)

5. VERIFY INTEGRITY
   └── Check last checkpoint exists and is valid
   └── If not: run Automatic Recovery
   └── Verify USB is writable

6. LOAD BLUEPRINTS
   └── Scan blueprints/ directory
   └── Validate each (structural check)
   └── Report: N blueprints loaded, N valid, N with warnings

7. READY
   └── Display: version, profile, blueprints, iterations
   └── Caveman Ultra: ON (default)
   └── Model: deepseek-v4-flash (agent) / deepseek-v4-pro (eval)
   └── Waiting for loop command
```

### Startup Output Example

```
Styde Forge v3.0 — The Crucible
Profile: pontus-main (Machine-B)
VRAM: 18.0 GB | RAM: 31.9 GB | CPU: 8 cores
Sampling: VI (depth 8) | Workers: 1
Models: flash (agent) / pro (eval)
Caveman Ultra: ON
Blueprints: 6 loaded, 6 valid
Status: Ready. 0 iterations completed.
```

---

## 2. Shutdown Sequence

```
1. COMPLETE CURRENT OPERATION
   └── Don't interrupt mid-spawn or mid-eval

2. CREATE CHECKPOINT
   └── Atomic snapshot of current state

3. WRITE SHUTDOWN MARKER
   └── .clean_shutdown file → proves clean exit

4. CLOSE LOGS
   └── Flush all log buffers
   └── Write final log entry

5. RELEASE RESOURCES
   └── Remove lock file
   └── Close USB handles

6. REPORT
   └── Iterations this session: N
   └── Agents spawned: N
   └── Total cost: $X.XXXX
```

---

## 3. Crash vs Clean Shutdown Detection

| Scenario | Detection | Next Startup Action |
|----------|-----------|--------------------|
| Clean shutdown | `.clean_shutdown` exists | Normal startup |
| Process crash | Stale `.running.lock` (>5 min) | Auto-recovery |
| Power loss | Missing `.clean_shutdown` | Auto-recovery |
| USB disconnect | I/O error on access | Remount + recovery |

---

## 4. Startup Health Checks

```python
def startup_health_check() -> dict:
    return {
        "state_ok": state_yaml_valid(),
        "hw_detected": gpu_count() > 0,
        "api_reachable": test_api_connectivity(),
        "usb_writable": test_usb_write(),
        "checkpoint_valid": verify_latest_checkpoint(),
        "blueprints_valid": all_blueprints_valid(),
        "disk_space_gb": free_space_gb(),
        "status": "ready" | "degraded" | "blocked"
    }
```

---

**Status:** Defined. 7-step startup, 6-step shutdown, health checks.
