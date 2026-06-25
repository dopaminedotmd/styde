# Phase 2 — Planning Index

**Styde Forge v3.0 "The Crucible" + StydeForge Dashboard**
**Status:** Phase 2 — PLANNING 🔵
**Created:** 2026-06-25
**Depends on:** Phase 1 complete (working core loop + dashboard MVP)

---

## Purpose

Phase 2 deepens the forge. Where Phase 1 proved the loop works, Phase 2 makes it **rigorous** — 
Bayesian eval weights, multi-judge consensus, historical learning, resource governance, 
and the first multi-agent collaboration patterns.

This index covers both:
- **Forge** — Eval depth, learning systems, resource management, multi-agent
- **Dashboard** — P1/P2 features: benchmark panels, health monitoring, additional providers

Every Phase 2 document references exactly which Phase 0 design it implements.

---

## What Changed from Phase 1

| Phase 1 | Phase 2 |
|---------|---------|
| Single judge (deepseek-v4-pro) | Cross-Judge Consensus (3+ judges) |
| Fixed eval weights (0.4/0.6) | Bayesian Weight Optimization (NUTS/VI) |
| File-based history (last 3 evals) | Historical Learning System (SQLite + pattern extraction) |
| Manual version bumps | Automatic Version Increment |
| YOLO resource usage | Resource Governor (VRAM/RAM/disk limits) |
| Sequential single-agent loop | Multi-agent collaboration (Phase Gates, Agent Comms) |
| Simple file-based evals | Smart Caching, Batch Processing, Anomaly Detection |
| Dashboard MVP (chat + agent list) | Dashboard P1: benchmark panels, health, more providers |

---

## Document Map (planned ~38 documents, 11 sections)

### 00 — Overview (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 1 | `PHASE2_INDEX.md` | — | This index |
| 2 | `PHASE2_SCOPE.md` | `Phase0_to_Phase1_Transition.md` §3, `PHASE1_SCOPE.md` §2 | Exact scope: what gets built, what's deferred to Phase 3 |
| 3 | `IMPLEMENTATION_ORDER.md` | `DECISIONS.md`, Phase 1 order | Build order with dependency graph |
| 4 | `PHASE1_TO_PHASE2_TRANSITION.md` | Phase 1 exit criteria | Prerequisites and entry gates for Phase 2 |

### 01 — Bayesian Optimization (3 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 5 | `Bayesian_Weight_Implementation.md` | `Bayesian_Weight_Optimization.md` | NUTS/VI-driven dynamic eval weight optimization |
| 6 | `Cross_Judge_Consensus_Implementation.md` | `Cross_Judge_Consensus.md` | Multi-model judge panel with variance detection |
| 7 | `Bias_Calibration_Implementation.md` | `Bias_Calibration.md` | Periodic calibration against known benchmarks |

### 02 — Multi-Judge Eval (already covered above in 01)
> Cross-Judge Consensus and Bias Calibration are the two eval upgrades. Bayesian weights tie them together.

### 03 — Learning Systems (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 8 | `Historical_Learning_Implementation.md` | `Historical_Learning_System.md` | SQLite database + pattern extraction from eval history |
| 9 | `Automatic_Version_Implementation.md` | `Automatic_Version_Increment.md` | Semantic versioning based on eval deltas |
| 10 | `Dynamic_Model_Selector_Implementation.md` | `Dynamic_Model_Selector.md` | Auto-select model per task based on cost/quality profile |
| 11 | `Self_Monitoring_Implementation.md` | `Self_Monitoring_Health.md` | Real-time health metrics + anomaly detection |

### 04 — Resource Management (3 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 12 | `Resource_Governor_Implementation.md` | `Resource_Governor.md` | VRAM/RAM/disk limit enforcement per agent |
| 13 | `GPU_Load_Balancing.md` | `Hardware_Adaptation_Layer.md` | Distribute work across 3080 + 3070 Ti |
| 14 | `Intelligent_Queue_System.md` | Phase 1 spawn pipeline | Priority-based task queue with batching |

### 05 — Multi-Agent Collaboration (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 15 | `Phase_Gates_Implementation.md` | — | Structured approval checkpoints between task steps |
| 16 | `Agent_Communication_Protocol.md` | `Multi_Agent_Collaboration.md` | Structured info exchange between agents |
| 17 | `Task_Decomposition_Engine.md` | Phase 1 spawn | Auto-break complex tasks into sub-tasks |
| 18 | `Specialized_Roles.md` | Phase 1 Top 20 Agents | Researcher, Debugger, Security Auditor, Refactorer, Architect |

### 06 — Automation & Knowledge (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 19 | `Auto_Benchmark_Generation.md` | Phase 1 eval | System creates new test tasks automatically |
| 20 | `Prompt_Optimization_System.md` | Phase 1 teacher | Improve prompts based on eval results |
| 21 | `Curriculum_Learning.md` | Phase 1 teacher | Progressively harder tasks as agents improve |
| 22 | `Knowledge_Graph_Implementation.md` | `Knowledge_Management.md` | Connect blueprints, agents, results in graph form |

### 07 — Dashboard P1/P2 (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 23 | `Benchmark_Panel_Implementation.md` | `Performance_Metrics.md`, `Quality_Benchmarks.md`, `Visualization_Strategy.md` | Graphs, time series, comparisons |
| 24 | `Health_Monitoring_Dashboard.md` | `Health_Monitoring.md` | CPU, GPU, RAM, disk — live in dashboard |
| 25 | `Additional_Providers.md` | `Built_In_Providers.md`, `Local_Model_Support.md` | OpenAI, Anthropic, Ollama, custom providers |
| 26 | `Dashboard_Polish.md` | `Agent_Detail_View.md`, `Spawn_New_Agent.md`, `Auto_Update.md` | Detail views, spawn from UI, auto-update |

### 08 — Blueprint Lifecycle (3 docs) (NEW)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 27 | `Version_History_Implementation.md` | `auto_version.py` | Git-like diffable history per blueprint |
| 28 | `Blueprint_Diff_Implementation.md` | — | Semantic diff between versions |
| 29 | `Rollback_Implementation.md` | `checkpoint.py` | Atomic rollback to any previous version |

### 09 — CI/CD Integration (2 docs) (NEW)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 30 | `CI_Runner_Implementation.md` | Phase 1 eval | JUnit XML, GitHub Actions, PR comments |
| 31 | `Setup_Forge_Action.md` | — | Composite GitHub Action for CI |

### 10 — Natural Language Control (3 docs) (NEW)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 32 | `NL_Forge_Control.md` | — | Chat-driven Forge: spawn/eval/improve via natural language |
| 33 | `NL_Blueprint_Creation.md` | `Import_Strategy.md` | Describe agent in Swedish → blueprint + benchmark |
| 34 | `Voice_Interface.md` | — | Voice control via Hermes TTS/STT |

### 11 — Integration & Delivery (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 35 | `P1_Exit_Criteria.md` | Phase 1 P0 criteria | All Phase 2 exit criteria |
| 36 | `Week_Execution_Plan.md` | This index | Weekly breakdown: tasks, dependencies, milestones |
| 37 | `Smart_Caching_Implementation.md` | Phase 1 cost tracking | Cache common model responses, batch evals |
| 38 | `End_to_End_Test_Plan.md` | Phase 1 test plan | Multi-agent + multi-judge end-to-end validation |

---

## Reading Order

1. `PHASE2_INDEX.md` ← You are here
2. `00_Overview/PHASE2_SCOPE.md` — What we build (and what stays in Phase 3)
3. `00_Overview/IMPLEMENTATION_ORDER.md` — Dependency graph + build sequence
4. `00_Overview/PHASE1_TO_PHASE2_TRANSITION.md` — Entry gates from Phase 1
5. Then: 01→02→03→04→05→06→07 depending on priority

---

## Priority Tiers

| Tier | Domain | Why First |
|------|--------|-----------|
| **P0 — Eval Depth** | Bayesian weights, Cross-judge, Bias calibration | Directly improves agent quality. Depends only on working eval pipeline |
| **P1 — Intelligence** | Historical learning, Auto-version, Model selector | Makes the forge smarter over time |
| **P2 — Scale** | Resource governor, GPU balancing, Queue system | Needed when running 10+ agents |
| **P3 — Collaboration** | Multi-agent, Phase gates, Agent comms | Enables complex workflows |
| **P4 — Lifecycle** | Blueprint version history, diff, rollback | Production-grade blueprint management |
| **P5 — Developer XP** | CI/CD, NL control, Voice | Makes Forge accessible without CLI |
| **P6 — Polish** | Dashboard P1/P2, Automation, Knowledge graph | UX and advanced features |

---

## Design Principles (inherited + new)

| Principle | Meaning |
|-----------|---------|
| **Rigor over speed** | Phase 2 trades loop speed for eval depth. Bayesian beats fixed weights |
| **Data-driven** | Every decision backed by eval history. No more manual weight tuning |
| **Graceful degradation** | If NUTS fails, fall back to fixed weights. If judge 2 fails, use judge 1 |
| **Resource-aware** | Governor prevents one agent from starving others |
| **All Phase 0 + Phase 1 principles still apply** | Atomicity, hardware awareness, traceability, quality gate, Caveman default |

---

## Status

- **Phase 0:** 53+36 documents — COMPLETE ✅
- **Phase 1:** 29 docs written, code in progress — BUILDING 🔨
- **Phase 2:** Planning initiated — IN PROGRESS 🔵
- **Phase 2 Docs:** 0/38 written

*"Phase 1 forged the steel. Phase 2 tempers the blade."*
