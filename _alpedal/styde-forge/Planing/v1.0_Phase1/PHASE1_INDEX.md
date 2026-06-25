# Phase 1 — Implementation Index

**Styde Forge v3.0 "The Crucible" + StydeForge Dashboard**
**Status:** Phase 1 — COMPLETE ✅
**Created:** 2026-06-25
**Updated:** 2026-06-25 (all 29 docs written)

---

## Purpose

Phase 1 is **implementation**. Phase 0 designed everything. Phase 1 builds it.

This index covers both:
- **Forge** — The portable evolutionary agent refinery (core loop, spawn, eval, improve, persist)
- **Dashboard** — The Tauri v2 Mission Control desktop app (chat, monitor, control)

Every Phase 1 document references exactly which Phase 0 design it implements.

---

## Document Map (29 implementation documents, 8 sections)

### 00 — Implementation Overview (3 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 1 | `PHASE1_SCOPE.md` | `Phase0_to_Phase1_Transition.md`, `Dashboard Phase0_to_Phase1.md` | Exact scope: what gets built, what's deferred |
| 2 | `IMPLEMENTATION_ORDER.md` | `DECISIONS.md` (D09 sequential loop), `Core_Loop_Detail.md` | Build order with dependency graph |
| 3 | `PHASE0_GAP_ANALYSIS.md` | All 53+36 Phase 0 docs | Design→Implementation gaps: what needs code, what's deferred |

### 01 — Forge Core Infrastructure (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 4 | `Core_Loop_Implementation.md` | `Core_Loop_Detail.md`, `State_Machines.md` | Step-by-step implementation of DEFINE→SPAWN→EVAL→IMPROVE→CHECKPOINT |
| 5 | `Bootstrap_Scripts.md` | `USB_Directory_Structure.md`, `Hardware_Adaptation_Layer.md` | `forge.py`, `detect.py`, directory creation, state.yaml init |
| 6 | `Circuit_Breaker_Implementation.md` | `Core_Loop_Detail.md` §7, `DECISIONS.md` D11 | Per-blueprint + global circuit breaker |
| 7 | `Caveman_Ultra_Activation.md` | `Caveman_Ultra_Mode.md`, `DECISIONS.md` D05 | Context injection, toggle, format enforcement |

### 02 — Forge Spawn System (3 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 8 | `Delegate_Task_Integration.md` | `Skill_Loading_Mechanism.md`, `Component_Interfaces.md` §3.2 | Exact `delegate_task()` calls with context construction |
| 9 | `Blueprint_Loading_System.md` | `Blueprint_Catalog.md`, `Blueprint_Validation.md` | Load, validate, build spawn context from blueprint |
| 10 | `RAG_Context_Injection.md` | `RAG_Retrieval.md`, `DECISIONS.md` D12 | FAISS + all-MiniLM-L6-v2 on RTX 3080 |

### 03 — Forge Eval Pipeline (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 11 | `Eval_Spec_Format.md` | agent-skill-creator v6, `Benchmark_Catalog.md` | Binary checks + golden cases + rollout runner. Replaces rubric.yaml |
| 12 | `Eval_Pipeline_Implementation.md` | `Self_Evaluation_System.md`, `LLM_as_Judge.md`, `Core_Loop_Detail.md` §3 | Combined self-eval + judge-eval + composite with rollout integration |
| 13 | `Quality_Gates.md` | agent-skill-creator v6 | Validation + security scan as hard gates before checkpoint |
| 14 | `Staleness_Detection.md` | agent-skill-creator v6 | Review tracking, dependency health, schema drift — auto-flag stale agents |

### 04 — Forge Improvement & Teacher (3 docs) ✅
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 15 | `Teacher_Integration.md` | `Teacher_Agent.md`, `Core_Loop_Detail.md` §4 | Teacher analyzes evals, proposes improvements |
| 16 | `Blueprint_Improvement_Loop.md` | `Core_Loop_Detail.md` §4, `State_Machines.md` §2-3 | Passed→promote, needs-work→retry, failed→archive |
| 17 | `Skill_Extraction_System.md` | `Skill_Loading_Mechanism.md` §5, `Teacher_Agent.md` §5 | Extract patterns from ≥85 runs into new skills |

### 05 — Forge Persistence & Safety (covered) ✅
> Implementation code in `Teacher_and_Persistence.md`. Separate docs deferred to Phase 2.

### 06 — Dashboard Shell & UI (covered) ✅
> `Tauri_Setup_and_Layout.md` + `Dashboard_Shell_Complete.md` cover all 4 planned docs.

### 07 — Dashboard Chat & Providers (covered) ✅
> `Provider_and_Chat_Implementation.md` covers all 4 planned docs including custom providers + Ollama.

### 08 — Integration & Delivery (4 docs)
| # | Document | References Phase 0 | Description |
|---|----------|-------------------|-------------|
| 28 | `Forge_Dashboard_Bridge.md` | `Hermes_CLI_Bridge.md`, `Real_Time_Updates.md`, `Start_Stop_Pipeline.md` | Tauri↔Hermes CLI communication, process control |
| 29 | `End_to_End_Test_Plan.md` | `Testing_Strategy.md`, `Core_Loop_Detail.md` | One complete loop: code-reviewer vs code-review-basic |
| 30 | `P0_Exit_Criteria.md` | `Phase0_to_Phase1_Transition.md` §1, Dashboard §6 | All 20 Phase 0 criteria + 10 Dashboard DoD items |
| 31 | `Week_Execution_Plan.md` | `PHASE1_ROADMAP.md`, `Top_20_Agents.md` | Weekly breakdown: tasks, owners, dependencies, milestones |

---

## Reading Order

1. `PHASE1_INDEX.md` ← You are here
2. `00_Implementation_Overview/PHASE1_SCOPE.md` — What we build (and what we don't)
3. `00_Implementation_Overview/IMPLEMENTATION_ORDER.md` — Dependency graph + build sequence
4. `00_Implementation_Overview/PHASE0_GAP_ANALYSIS.md` — What Phase 0 missed / what needs decisions
5. `08_Integration/Week_Execution_Plan.md` — Week-by-week plan
6. Then: 01→02→03→04→05 (Forge) or 06→07 (Dashboard) depending on focus

---

## Quick Start — Day 1 of Phase 1

```bash
# 1. Verify environment
nvidia-smi              # GPUs detected
hermes --version        # Hermes Agent v0.17.0+
python --version        # Python 3.11+

# 2. Bootstrap Forge
cd D:\styde\_alpedal\styde-forge
python scripts/forge.py init           # Create USB directory structure

# 3. Verify hardware profile
python scripts/detect.py               # Auto-detect and save profile

# 4. Spawn first agent
python scripts/forge.py spawn code-reviewer code-review-basic

# 5. Evaluate
python scripts/eval_runner.py run agent-code-reviewer-<timestamp> code-review-basic

# 6. Checkpoint
python scripts/forge.py checkpoint
```

---

## Design Principles (inherited from Phase 0)

| Principle | Meaning |
|-----------|---------|
| **One logical home** | Every file has exactly one canonical location |
| **Atomicity first** | All writes are transactional — never partial |
| **Hardware aware** | Auto-detect on startup, adapt parameters |
| **Full traceability** | Every decision, eval, and version change logged |
| **Quality gate** | Nothing below 80/100 saved. ≥85×3 → production |
| **Caveman default** | 70% fewer tokens, 2× faster |
| **Code from docs** | Phase 1 code is Phase 0 docs made executable |

---

## Status

- **Forge Phase 0:** 53 documents, 14 sections — COMPLETE ✅
- **Dashboard Phase 0:** 36 documents, 10 sections — COMPLETE ✅
- **Phase 1 Docs:** 29 documents, 8 sections — COMPLETE ✅
- **Phase 1 Code:** Core/ stubs created (14 files), 2 modules implemented (quality_gates.py, staleness.py)
- **First Blueprint:** code-reviewer — ready to spawn
- **First Benchmark:** code-review-basic — binary checks + 3 golden cases

*"Phase 0 designed the blueprint. Phase 1 forges the steel."*
