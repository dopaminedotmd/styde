# Master Architecture Overview

**Styde Forge v3.0 — The Crucible**
**Phase 0 Design Document**

---

## 1. Vision

Styde Forge v3.0 is a **portable, evolutionary elite-agent refinery** on USB.

Raw agent blueprints are transformed into world-class specialized agents through
a continuous loop of spawning, evaluation, improvement, and checkpointing.

**Not a content factory — a refinery.** Quality over quantity. Nothing below
80/100 reaches the USB. Caveman Ultra mode ON by default: 70% fewer tokens.

---

## 2. Complete Architecture

```
                         ┌─────────────────────────┐
                         │     STYDE FORGE          │
                         │     (Parent Process)     │
                         └────────────┬────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
     ┌────────┴────────┐   ┌─────────┴─────────┐   ┌────────┴────────┐
     │  HARDWARE LAYER │   │    META-LAYER     │   │  TEACHER AGENT  │
     │                 │   │                   │   │                 │
     │ • Auto-detect   │   │ • Model Selector  │   │ • Analyze evals │
     │ • Profile match │   │ • Historical Learn│   │ • Give feedback │
     │ • Adapt params  │   │ • Version Incr    │   │ • Extract skills│
     │ • Resource Gov  │   │ • Health Monitor  │   │ • Coach agents  │
     │ • RAG embeddings│   │                   │   │                 │
     └────────┬────────┘   └─────────┬─────────┘   └────────┬────────┘
              │                       │                       │
              └───────────────────────┼───────────────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │    SUBAGENT SPAWN       │
                         │                         │
                         │ • Skill Loading         │
                         │ • Blueprint Validation  │
                         │ • Caveman Ultra inject  │
                         │ • RAG context injection │
                         │ • delegate_task()       │
                         └────────────┬────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
     ┌────────┴────────┐   ┌─────────┴─────────┐   ┌────────┴────────┐
     │  EVAL PIPELINE  │   │  KNOWLEDGE MGMT   │   │  HOOKS & EVENTS │
     │  (6 layers)     │   │                   │   │                 │
     │                 │   │ • Acquire sources │   │ • 17 events     │
     │ 1. Self-Eval    │   │ • Synthesize      │   │ • Webhooks      │
     │ 2. LLM-as-Judge │   │ • Index           │   │ • Scripts       │
     │ 3. Cross-Judge  │   │ • Store on USB    │   │ • Alerts        │
     │ 4. Bias Calib   │   │ • Retrieve context│   │ • Throttle      │
     │ 5. Auto-Valid   │   └───────────────────┘   └─────────────────┘
     │ 6. Bayesian Opt │
     └────────┬────────┘
              │
     ┌────────┴────────┐
     │ PERSISTENCE     │
     │                 │
     │ • Atomic writes │
     │ • Checkpoints   │
     │ • Recovery      │
     │ • Export/Import │
     └────────┬────────┘
              │
     ┌────────┴────────┐
     │      USB        │
     │   (48 GB)       │
     └─────────────────┘
```

---

## 3. Core Loop

```
DEFINE ──→ SPAWN ──→ EVALUATE ──→ IMPROVE ──→ CHECKPOINT
   ↑                                               │
   └───────────────────────────────────────────────┘
```

| Step | What happens | Model |
|------|-------------|-------|
| DEFINE | Load blueprint, validate, build context | — |
| SPAWN | delegate_task with Caveman Ultra + skills | `deepseek-v4-flash` |
| SELF-EVAL | Agent scores own output | `deepseek-v4-flash` |
| JUDGE-EVAL | Independent model judges against rubric | `deepseek-v4-pro` |
| IMPROVE | Teacher analyzes, proposes changes, extracts skills | `deepseek-v4-pro` |
| CHECKPOINT | Atomic snapshot of entire state | — |

---

## 4. Dual-Model Strategy

| Role | Model | Tokens/iter | Cost/iter |
|------|-------|-------------|-----------|
| Agent spawn | `deepseek-v4-flash` | ~1200-2400 | ~$0.001 |
| Judge eval | `deepseek-v4-pro` | ~400-800 | ~$0.001 |
| Teacher feedback | `deepseek-v4-pro` | ~400-800 | ~$0.001 |
| **Total per iteration** | | **~2000-4000** | **~$0.003** |

Caveman Ultra mode reduces tokens by 70%. Flash for 80% of calls, Pro for 20%.

---

## 5. Hardware Profiles

| Parameter | Machine-A (Beast) | Machine-B (Main/Pontus) |
|-----------|-------------------|------------------------|
| GPUs | 3090 24GB + 3080 10GB | 3080 10GB + 3070 Ti 8GB |
| Total VRAM | 34 GB | 18 GB |
| RAM | 64 GB DDR4 | 32 GB DDR5 |
| Sampling | NUTS (depth 11) | VI (depth 8) |
| Workers | 4 | 1-2 |
| Agent model | deepseek-v4-flash | deepseek-v4-flash |
| Eval model | deepseek-v4-pro | deepseek-v4-pro |

---

## 6. Design Principles

| Principle | Meaning |
|-----------|---------|
| **One logical home** | Every piece of data has exactly one canonical location |
| **Atomicity first** | All writes are transactional — never partial |
| **Hardware aware** | System auto-adapts to available resources |
| **Full traceability** | Every decision, eval, and version change is logged |
| **Quality gate** | Nothing below 80/100 is saved |
| **Caveman default** | 70% fewer tokens, 2× faster, 3× cheaper |
| **Self-contained** | The USB is the entire system |

---

## 7. Document Map

| Section | Documents | Purpose |
|---------|-----------|---------|
| 00_Overview | 12 | Architecture, loop, interfaces, data models, config, glossary |
| 01_Vision | 2 | Vision, goals, blueprint catalog |
| 02_Hardware | 2 | Adaptation layer, resource governor |
| 03_Eval_Pipeline | 7 | 6 eval layers + benchmark catalog |
| 04_Sampling_Stack | 5 | NUTS, HMC, VI, dual averaging, tree depth |
| 05_Meta_Layer | 4 | Model selector, learning, versioning, health |
| 06_Persistence_Safety | 4 | Atomic writes, checkpoints, recovery, risks |
| 07_Multi_Agent | 2 | Collaboration, security |
| 08_Import_Export | 2 | Import, sync strategy |
| 09_Risk_Maintenance | 1 | Maintenance and cleanup |
| 10_Operations | 7 | Skills, validation, logging, costs, oversight, API keys, Caveman Ultra |
| 11_Knowledge_Management | 1 | Knowledge lifecycle |
| 12_Teacher_Agent | 1 | Teacher loop, feedback, skill extraction |
| 13_Hooks_Events | 1 | Event system, hooks |

---

**Status:** Phase 0 — Design & Foundation
