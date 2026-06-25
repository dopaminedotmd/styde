# Cost & Token Tracking

**Styde Forge v3.0 — Phase 0**
**Section:** 10_Operations

---

## 1. Purpose

Track token consumption and API costs per blueprint, per agent, and per loop
iteration. Critical since the forge uses cloud models (DeepSeek, Claude, Grok).

---

## 2. Cost Model

```python
MODEL_PRICING = {
    "deepseek-v4-flash":    {"input": 0.07, "output": 0.14},   # Agent spawn
    "deepseek-v4-pro":      {"input": 0.14, "output": 0.28},   # Eval + Teacher
    "claude-sonnet-4":      {"input": 3.00, "output": 15.00},  # Optional
    "grok-3":               {"input": 2.00, "output": 8.00},   # Optional
}
```

---

## 3. Tracking Implementation

```python
class CostTracker:
    def __init__(self):
        self.session_costs = {}  # Per agent/session

    def track_usage(self, agent_id: str, model: str,
                    input_tokens: int, output_tokens: int):
        pricing = MODEL_PRICING.get(model, {"input": 0, "output": 0})
        cost = (input_tokens / 1_000_000) * pricing["input"] + \
               (output_tokens / 1_000_000) * pricing["output"]

        if agent_id not in self.session_costs:
            self.session_costs[agent_id] = {
                "total_tokens": 0,
                "total_cost": 0.0,
                "model_usage": {}
            }

        entry = self.session_costs[agent_id]
        entry["total_tokens"] += input_tokens + output_tokens
        entry["total_cost"] += cost

        if model not in entry["model_usage"]:
            entry["model_usage"][model] = {"tokens": 0, "cost": 0.0}
        entry["model_usage"][model]["tokens"] += input_tokens + output_tokens
        entry["model_usage"][model]["cost"] += cost

    def get_summary(self, agent_id: str) -> dict:
        return self.session_costs.get(agent_id, {"total_tokens": 0, "total_cost": 0.0})

    def get_forge_total(self) -> dict:
        total_tokens = sum(c["total_tokens"] for c in self.session_costs.values())
        total_cost = sum(c["total_cost"] for c in self.session_costs.values())
        return {"total_tokens": total_tokens, "total_cost": round(total_cost, 4)}
```

---

## 4. Budget Management

```python
BUDGET_CONFIG = {
    "daily_limit_usd": 5.00,
    "weekly_limit_usd": 25.00,
    "per_agent_limit_usd": 2.00,
    "alert_at_percent": 80
}

def check_budget(cost_tracker: CostTracker) -> str:
    daily = cost_tracker.get_daily_cost()
    if daily > BUDGET_CONFIG["daily_limit_usd"] * 0.8:
        return f"WARNING: Daily spend at {daily:.2f}/{BUDGET_CONFIG['daily_limit_usd']}"
    return "OK"
```

---

## 5. Cost Optimization Strategies

| Strategy | Savings |
|----------|---------|
| Use local models for simple tasks | 100% |
| Cache model responses for repeated queries | 30-50% |
| Stricter eval → fewer re-spawns | 20-40% |
| Shorter contexts for preliminary evals | 15-25% |
| Batch evaluations when possible | 10-20% |

---

## 6. Storage

Cost data stored in:
- `logs/costs/daily.json` — daily aggregates
- `logs/costs/per_agent.json` — per-agent breakdown
- `99_INDEXES/cost_summary.json` — total forge cost

---

**Status:** Defined. Tracks tokens and cost per model/agent/loop.
