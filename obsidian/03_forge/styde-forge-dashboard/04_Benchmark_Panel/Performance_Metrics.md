# Performance Metrics

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The benchmark panel displays performance metrics over time: tokens per second, latency, and cost — per agent, per model, and aggregated.

---

## 2. Live Metrics — Visual Design

```
┌──────────────────────────────────────────────────┐
│ 📊 BENCHMARKS                        [24h ▼]    │
├──────────────────────────────────────────────────┤
│                                                  │
│  Tokens per Second (live)                        │
│  ┌────────────────────────────────────────────┐  │
│  │ 60│                   ╭─╮                  │  │
│  │ 40│     ╭──╮   ╭─────╯ ╰──╮  ╭─           │  │
│  │ 20│╭───╯  ╰───╯          ╰──╯             │  │
│  │  0│└────────────────────────────────────── │  │
│  │   15:30    15:35     15:40     15:45      │  │
│  │   Avg: 42 t/s  Peak: 68 t/s  Now: 45 t/s │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  ┌──────────────┬──────────────┬──────────────┐  │
│  │  Latency     │  Cost/hr     │  Agents/hr   │  │
│  │              │              │              │  │
│  │   1.2s       │   $0.042     │    4.2       │  │
│  │   avg resp   │   running    │   completed  │  │
│  │   ↓ 0.3s     │   ↑ $0.005   │   ↑ 1.1      │  │
│  └──────────────┴──────────────┴──────────────┘  │
│                                                  │
│  Per-Model Performance                           │
│  ┌────────────────────────────────────────────┐  │
│  │ Model              t/s    Lat    Cost/1K  │  │
│  │ ───────────────────────────────────────────┤  │
│  │ deepseek-v4-flash  52    0.8s   $0.00027  │  │
│  │ deepseek-v4-pro    28    2.1s   $0.00110  │  │
│  │ gpt-4o             35    1.5s   $0.00500  │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 3. Metrics

### 3.1 Primary Metrics

| Metric | Unit | Description | Data Source |
|--------|------|-------------|-------------|
| **Tokens/s** | tokens/second | Throughput | Hermes log (token counter) |
| **Latency** | milliseconds | Time to first token (TTFT) | Provider API |
| **Cost/token** | USD | Cost per 1000 tokens | Provider price list |
| **Cost/hr** | USD | Total cost per hour | Aggregated from all agents |
| **Agents/hr** | count | Completed agents per hour | Agent history |

### 3.2 Secondary Metrics

| Metric | Description |
|--------|-------------|
| **Queue depth** | Number of agents in queue |
| **Avg agent duration** | Average time per agent |
| **Success rate** | % agents passing quality gate (≥80) |
| **Token efficiency** | Output tokens / input tokens (should be high) |
| **Error rate** | % agents that error |

---

## 4. Time Intervals

| Interval | Resolution | Description |
|----------|------------|-------------|
| Live (5 min) | Per second | Real-time — last 5 minutes |
| 1 hour | Per minute | Last hour |
| 24 hours | Per 5 minutes | Last 24 hours |
| 7 days | Per hour | Last week |
| 30 days | Per day | Last month |

---

## 5. Per-Model Comparison

Table comparing all models:

| Column | Description |
|--------|-------------|
| Model | Model name |
| Provider | Provider (DeepSeek, OpenAI, etc.) |
| t/s (avg) | Average tokens/second |
| t/s (peak) | Highest measured tokens/second |
| Latency (avg) | Average TTFT |
| Latency (p95) | 95th percentile latency |
| Cost/1K tokens | Cost per 1000 tokens |
| Agents run | Number of agents run with this model |
| Avg Score | Average eval score for this model |

---

## 6. Charts — Specification

### 6.1 Tokens per Second (line chart)

- X-axis: time
- Y-axis: tokens/s
- One line per model (color-coded)
- Hover: exact value + timestamp
- Annotations: mark when a new agent spawned

### 6.2 Cost Over Time (stacked area)

- X-axis: time
- Y-axis: cost (USD)
- Stacked area per model
- Cumulative total as a separate line

### 6.3 Agent Throughput (bar chart)

- X-axis: time buckets (per hour)
- Y-axis: number of completed agents
- Bars: green (score ≥80), yellow (60-79), red (<60)

### 6.4 Latency Distribution (histogram)

- X-axis: latency buckets (0-500ms, 500ms-1s, 1-2s, 2-5s, 5s+)
- Y-axis: number of requests
- Per model

---

## 7. Data Storage

Performance data stored locally:

```json
{
  "timestamp": "2026-06-25T15:42:00Z",
  "agent_id": "ag-xyz-123",
  "model": "deepseek-v4-flash",
  "provider": "deepseek",
  "metrics": {
    "tokens_in": 4200,
    "tokens_out": 2642,
    "total_tokens": 6842,
    "duration_ms": 225000,
    "ttft_ms": 850,
    "cost_usd": 0.019,
    "tokens_per_second": 30.4
  }
}
```

**Storage strategy:**
- Raw data: IndexedDB — last 30 days
- Aggregated data: by hour, day, week — compressed
- Cleanup: older than 30 days → keep aggregates, delete raw data

---

**Status:** Phase 0 — Design
