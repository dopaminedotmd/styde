# Quality Benchmarks

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

Quality benchmarks measure not speed/cost but how *good* the agent's output is. Data comes from the StydeForge Forge eval pipeline (LLM-as-Judge, Self-Eval, etc.).

---

## 2. Eval Score Card — Visual Design

```
┌──────────────────────────────────────────────────┐
│ 📊 QUALITY BENCHMARKS                            │
├──────────────────────────────────────────────────┤
│                                                  │
│  Overall Quality Score (last 10 agents)          │
│  ┌────────────────────────────────────────────┐  │
│  │ 100│    ●                                 │  │
│  │  80│ ●  ●  ●──●──●  ●                    │  │
│  │  60│          ●     ●  ●                 │  │
│  │  40│                        ●            │  │
│  │    └──────────────────────────────────────│  │
│  │    agent1 agent2 agent3 ...       agent10 │  │
│  │    Avg: 78.3  Median: 82  Quality gate: 80│  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Score Distribution                              │
│  ┌────────────────────────────────────────────┐  │
│  │  90-100 │████████████████████████ 26      │  │
│  │  80-89  │████████████████████████████ 33   │  │
│  │  70-79  │███████████████ 19                │  │
│  │  60-69  │██████████ 12                     │  │
│  │  <60    │████ 6                             │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Score by Blueprint                              │
│  ┌────────────────────────────────────────────┐  │
│  │ code-review-v3    ██████████████ 87 avg   │  │
│  │ test-generator    ████████████ 82 avg     │  │
│  │ doc-writer        ██████ 68 avg           │  │
│  │ refactor          ██████████████ 85 avg   │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 3. Eval Categories

Each agent can be evaluated across multiple categories:

| Category | Weight (default) | Description |
|----------|-----------------|-------------|
| **Code Quality** | 30% | Correctness, bugs, edge cases |
| **Completeness** | 25% | Meets all requirements in the prompt |
| **Best Practices** | 20% | Follows established conventions |
| **Efficiency** | 15% | Optimized, no unnecessary code |
| **Documentation** | 10% | Clear comments, README |

Weights are configurable per blueprint.

---

## 4. Score Types

| Type | Description | Source |
|------|-------------|--------|
| **Self-Eval** | Agent assesses its own output | The agent itself |
| **LLM-as-Judge** | Independent model assesses against rubric | deepseek-v4-pro |
| **Cross-Judge** | Multiple judges → consensus | Multiple models |
| **Auto-Validation** | Automated tests (if available) | Test suite |
| **Human Score** | Manual human assessment | User |

---

## 5. Quality Gate

| Score | Status | Color | Action |
|-------|--------|-------|--------|
| ≥90 | Exceptional | Green (bright) | Checkpoint + save |
| 80-89 | Approved | Green | Checkpoint + save |
| 70-79 | Failed | Yellow | Mark for improvement |
| 60-69 | Weak | Orange | Teacher agent analyzes |
| <60 | Poor | Red | Discarded (doesn't reach USB), logged |

---

## 6. Trend Analysis

The dashboard analyzes trends over time:

| Trend | Meaning |
|-------|---------|
| **Rising scores** | Blueprint/agent improving over iterations → positive |
| **Falling scores** | Regression — something has degraded → warning |
| **Flat curve** | Agent has reached a ceiling → consider new blueprint |
| **High variance** | Unstable quality → investigate prompt/skills |
| **Low variance** | Stable, predictable quality → good |

---

## 7. Per-Blueprint Comparison

| Blueprint | Agents | Avg Score | Best | Worst | Trend |
|-----------|--------|-----------|------|-------|-------|
| code-reviewer-v3 | 47 | 87.3 | 96 | 72 | ↗ rising |
| test-generator-v2 | 32 | 82.1 | 91 | 65 | → stable |
| doc-writer-v1 | 18 | 68.4 | 82 | 41 | ↘ falling |
| refactor-v2 | 25 | 85.0 | 94 | 78 | ↗ rising |

---

## 8. Benchmark Types (Future)

When StydeForge supports external benchmarks:

| Benchmark | Type | Description |
|-----------|------|-------------|
| HumanEval | Code | Python functions from docstrings |
| MBPP | Code | Basic Python programs |
| SWE-bench | Code | Real GitHub issues |
| MMLU | Knowledge | Multidisciplinary knowledge |
| Custom | Custom | User-defined benchmarks |

---

**Status:** Phase 0 — Design
