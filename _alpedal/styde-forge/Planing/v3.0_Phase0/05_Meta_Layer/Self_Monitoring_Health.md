# Self-Monitoring & Health Dashboard

**Styde Forge v3.0 — Phase 0**
**Section:** 05_Meta_Layer

---

## 1. Purpose

Continuously monitor reactor health, stability, and improvement rate.
Detect degradation before it becomes critical.

---

## 2. Health Metrics (per cycle)

```python
{
    "overall_health": 87,              # 0-100
    "avg_eval_score_last_10": 83.5,
    "improvement_trend": +0.12,        # per cycle
    "risk_level": "low",               # low | medium | high
    "sampling_efficiency": 0.82,       # ESS per minute
    "error_rate_last_24h": 2,
    "hardware_utilization": {
        "vram_percent": 72,
        "ram_percent": 58
    },
    "last_checkpoint": "2026-06-25T12:00:00Z"
}
```

---

## 3. Warning System

| Condition | Action |
|-----------|--------|
| Risk > 70 | Auto-pause + Teacher Alert |
| Negative trend 5+ cycles | Increase exploration |
| High error rate | Stronger recovery mode |
| VRAM > 90% | Scale down workers |
| No checkpoint 2h+ | Force checkpoint |

---

## 4. Health Score Formula

```
Health = EvalTrend(30%) + ErrorRate(25%) + Hardware(20%)
       + SamplingQuality(15%) + CheckpointFreshness(10%)
```

---

## 5. Long-Term Improvement Metrics

Tracks whether the forge actually gets smarter over weeks/months:

```python
def long_term_metrics() -> dict:
    return {
        "weeks_running": 0,
        "total_iterations": 0,
        "agents_spawned": 0,
        "agents_saved_to_usb": 0,

        "trends": {
            "avg_score_week1": None,     # Baseline
            "avg_score_current_week": None,
            "score_trend": "flat",       # declining | flat | improving | accelerating

            "first_pass_rate_week1": None,  # % agents ≥80 on first try
            "first_pass_rate_current": None,
            "efficiency_trend": "flat",

            "avg_tokens_per_agent_week1": None,
            "avg_tokens_current": None,
            "token_efficiency": "flat",   # using fewer tokens = getting more efficient

            "avg_retries_per_agent": None,
            "retry_trend": "flat",        # fewer retries = agents getting better
        },

        "top_agents": [],  # Top 10 by score
        "most_improved": [],  # Agents with largest version-to-version delta
    }
```

### Key Questions Answered

| Question | Metric |
|----------|--------|
| Is the forge getting better? | `score_trend` — should be "improving" or "accelerating" |
| Are agents getting more efficient? | `token_efficiency` — should decrease over time |
| Which blueprints improve fastest? | `most_improved` list |
| Are we spending more or less per agent? | `cost_per_agent` trend |
| Is first-pass rate improving? | `first_pass_rate` — should increase |

---

**Status:** Implemented. Monitoring-ready.
