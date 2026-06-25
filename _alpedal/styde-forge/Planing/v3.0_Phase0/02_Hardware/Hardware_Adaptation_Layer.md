# Hardware Adaptation Layer

**Styde Forge v3.0 — Phase 0**
**Section:** 02_Hardware

---

## 1. Purpose

Automatically detect current hardware at Forge startup and adapt all critical
parameters — sampling method, model selection, concurrency, and resource limits — 
for optimal performance and stability.

---

## 2. Detection

```python
class HardwareAdaptationLayer:
    def _detect_hardware(self) -> dict:
        vram_gb = 0.0
        try:
            if torch.cuda.is_available():
                vram_gb = sum(
                    torch.cuda.get_device_properties(i).total_memory
                    for i in range(torch.cuda.device_count())
                ) / (1024**3)
        except:
            pass

        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_cores = psutil.cpu_count(logical=False)

        if vram_gb >= 28:
            return {"type": "A", "power": "high"}
        else:
            return {"type": "B", "power": "medium"}
```

---

## 3. Hardware Profiles

### Machine-A (Beast)
| Resource | Spec |
|----------|------|
| GPUs | RTX 3090 (24GB) + RTX 3080 (10GB) |
| Total VRAM | 34 GB |
| RAM | 64 GB DDR4 |
| Sampling | NUTS (depth 11) |
| Max workers | 4 |
| Models | 70B-405B (quantized) |

### Machine-B (Main — Current)
| Resource | Spec |
|----------|------|
| GPUs | RTX 3080 (10GB) + RTX 3070 Ti (8GB) |
| Total VRAM | 18 GB |
| RAM | 32 GB DDR5 |
| Sampling | VI (depth 8) |
| Max workers | 1-2 |
| Models | 7B-14B |

---

## 4. Auto-Adaptation

```python
def _generate_adaptations(self) -> dict:
    if p["power_level"] == "high":
            return {
                "sampling_method": "NUTS",
                "max_tree_depth": 11,
                "bayesian_samples": 2800,
                "checkpoint_interval_min": 45,
                "max_parallel_subagents": 3,
                "agent_model": "deepseek-v4-flash",
                "agent_provider": "deepseek",
                "eval_model": "deepseek-v4-pro",
                "eval_provider": "deepseek",
                "teacher_model": "deepseek-v4-pro",
                "teacher_provider": "deepseek",
                "vi_iterations": 800
            }
        else:  # Machine-B
            return {
                "sampling_method": "VI",
                "max_tree_depth": 8,
                "bayesian_samples": 1400,
                "checkpoint_interval_min": 25,
                "max_parallel_subagents": 1,
                "agent_model": "deepseek-v4-flash",
                "agent_provider": "deepseek",
                "eval_model": "deepseek-v4-pro",
                "eval_provider": "deepseek",
                "teacher_model": "deepseek-v4-pro",
                "teacher_provider": "deepseek",
                "vi_iterations": 400
            }
```

---

## 5. Atomic Profile Storage

Profiles are saved atomically to `99_INDEXES/hardware_profile.json` using
temp-file + rename pattern. Never partial, never corrupted.

---

**Status:** Implemented. Core component for portability.

---

## Related Documents

- `Resource_Governor.md` — Enforces limits based on detected hardware
- `00_Overview/Config_Reference.md` — All adaptation parameters
- `08_Import_Export/Sync_Strategy.md` — Cross-machine adaptation in action
- `04_Sampling_Stack/` — Sampler chosen by hardware profile
