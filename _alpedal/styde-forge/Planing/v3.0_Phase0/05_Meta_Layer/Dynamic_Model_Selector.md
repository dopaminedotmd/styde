# Dynamic Model Selector

**Styde Forge v3.0 — Phase 0**
**Section:** 05_Meta_Layer

---

## 1. Purpose

Select the optimal model for each forge operation. In v3.0 this is
a simple rule-based selector: Flash for agents, Pro for eval/teacher.
v3.1+ adds historical-performance-weighted selection.

---

## 2. Model Selection Rules (v3.0)

```python
def select_model(role: str) -> str:
    """
    Simple, fast, predictable.

    Flash (agents):  $0.14/M output, fast, good enough
    Pro (eval):      $0.28/M output, highest quality
    """
    ROLES = {
        "agent":    "deepseek-v4-flash",
        "spawn":    "deepseek-v4-flash",
        "subagent": "deepseek-v4-flash",
        "self_eval":"deepseek-v4-flash",  # Agent evals itself
        "judge":    "deepseek-v4-pro",    # Quality-critical
        "teacher":  "deepseek-v4-pro",    # Quality-critical
        "meta":     "deepseek-v4-pro",    # Quality-critical
        "consensus":"deepseek-v4-pro",    # Quality-critical
    }
    return ROLES.get(role, "deepseek-v4-flash")
```

---

## 3. Why Not More Complex? (v3.0)

| Would add | Why we skip it in v3.0 |
|-----------|----------------------|
| Per-domain model selection | Flash is good enough for all 6 domains |
| Historical performance weighting | Not enough data yet (0 agents spawned) |
| Cost/latency trade-off | Flash is already cheapest + fastest |
| Hardware-aware model choice | We use API, not local models |

**v3.1+:** When Historical Learning has 500+ eval results, add per-domain
model performance tracking and dynamic selection.

---

## 4. Dual-Model Strategy (Flash + Pro)

| Role | Model | Tokens/iter | Cost/iter | % of calls |
|------|-------|-------------|-----------|------------|
| Agent spawn | `deepseek-v4-flash` | ~1200-2400 | ~$0.001 | 60% |
| Self-eval | `deepseek-v4-flash` | ~200-400 | ~$0.0002 | 20% |
| Judge eval | `deepseek-v4-pro` | ~400-800 | ~$0.001 | 10% |
| Teacher feedback | `deepseek-v4-pro` | ~400-800 | ~$0.001 | 10% |
| **Total per iteration** | | **~2200-4400** | **~$0.003** | 100% |

Caveman Ultra mode reduces these by 70%: ~700-1300 tokens/iteration, ~$0.001.

---

## 5. Model Failover

```python
def select_with_failover(role: str) -> str:
    primary = select_model(role)
    if model_available(primary):
        return primary

    # Failover: if Pro is down, use Flash for everything
    if "pro" in primary:
        log_warning(f"deepseek-v4-pro unavailable, falling back to flash")
        return "deepseek-v4-flash"

    # If Flash is down too, we're dead
    raise ForgeError("No models available")
```

---

## 6. Integration

- Called by `forge.py agent spawn` before each delegate_task
- Called by eval pipeline for judge model selection
- Called by teacher agent for feedback model
- Failover logged to `logs/errors/`
- Model usage tracked by Cost Token Tracking

---

## 7. Cost-Aware Routing (Phase 1+)

When multiple providers are available, route to cheapest that meets quality bar:

```python
def cost_aware_route(role: str, task_complexity: str = "medium") -> str:
    """
    Simple tasks → try Flash first
    Complex tasks → Pro directly (skip Flash retry)
    """
    ROUTES = {
        ("agent", "simple"):   "deepseek-v4-flash",
        ("agent", "medium"):   "deepseek-v4-flash",
        ("agent", "complex"):  "deepseek-v4-pro",    # Skip retries
        ("judge", "any"):      "deepseek-v4-pro",    # Quality-critical
        ("teacher", "any"):    "deepseek-v4-pro",    # Quality-critical
    }
    key = (role, task_complexity if role == "agent" else "any")
    return ROUTES.get(key, "deepseek-v4-flash")
```

### Cost Comparison

| Strategy | Cost/iteration | Quality | Risk |
|----------|---------------|---------|------|
| Flash only | $0.001 | Good | Complex tasks may need retries |
| Pro only | $0.005 | Best | 5× cost for simple tasks |
| **Cost-aware** | **$0.002** | **Best** | Slightly more complex routing |

---

**Status:** v3.0 — rule-based. v3.1+ — data-driven.

---

## Related Documents

- `02_Hardware/Hardware_Adaptation_Layer.md` — Hardware profiles with model defaults
- `10_Operations/Cost_Token_Tracking.md` — Cost tracking per model
- `10_Operations/API_Key_Management.md` — Key validation
- `10_Operations/Caveman_Ultra_Mode.md` — Token reduction strategy
