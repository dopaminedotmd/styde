# Phase 0 → Phase 1 Transition Plan

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Phase 0 Completion Criteria

Phase 0 is complete when ALL of the following are true:

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Master architecture documented | ✅ |
| 2 | Vision and goals defined | ✅ |
| 3 | All 6 blueprints specified | ✅ |
| 4 | All 6 benchmarks defined with rubrics | ✅ |
| 5 | Eval pipeline designed (6 layers) | ✅ |
| 6 | Sampling stack designed (4 methods) | ✅ |
| 7 | Meta-layer designed (4 components) | ✅ |
| 8 | Persistence & safety designed | ✅ |
| 9 | Multi-agent collaboration designed | ✅ |
| 10 | Import strategy defined | ✅ |
| 11 | Maintenance strategy defined | ✅ |
| 12 | Operations docs complete (5 docs) | ✅ |
| 13 | USB directory structure specified | ✅ |
| 14 | All data models defined (8 schemas) | ✅ |
| 15 | Core loop specified step-by-step | ✅ |
| 16 | Component interfaces defined | ✅ |
| 17 | Blueprint catalog complete | ✅ |
| 18 | Benchmark catalog complete | ✅ |
| 19 | All 9 risks have mitigations | ✅ |
| 20 | Phase 0→1 transition plan exists | ← You are here |

---

## 2. What Phase 1 Builds

### Phase 1 Goal
**Execute the first complete loop iteration.** One blueprint, one benchmark,
one spawn, one eval, one improvement, one checkpoint. Prove the loop works
end-to-end.

### Phase 1 Scope

| Week | Deliverable | Details |
|------|-------------|---------|
| 1 | **Forge infrastructure** | Rebuild scripts/, state.yaml, hardware detection, USB directory structure |
| 1 | **Blueprint loading** | Implement `load_blueprint_context()` from Skill_Loading_Mechanism.md |
| 2 | **Agent spawning** | `delegate_task` integration with full blueprint context |
| 2 | **Self-evaluation** | Agent self-evals against rubric |
| 3 | **LLM-as-Judge** | Independent model evaluates agent output |
| 3 | **Composite scoring** | Weight self-eval + judge-eval → pass/fail |
| 4 | **Improvement loop** | Teacher analyzes eval → proposes blueprint improvements |
| 4 | **Checkpoint system** | Atomic snapshots with integrity verification |
| 5 | **Recovery system** | Crash detection + automatic checkpoint restore |
| 5 | **End-to-end test** | One complete loop: code-reviewer vs code-review-basic |
| 6 | **Second blueprint** | Bring research-synthesizer online |
| 6 | **Parallel loops** | Run two independent loops simultaneously |

### Phase 1 Exit Criteria
- [ ] code-reviewer completes 10 loop iterations with improving scores
- [ ] At least one agent reaches ≥ 85/100
- [ ] Checkpoint → crash → recovery works without data loss
- [ ] Export → import on different machine works
- [ ] Second blueprint reaches ≥85×3 (production-ready)

---

## 3. What Phase 2 Builds

| Feature | Details |
|---------|---------|
| Bayesian Weight Optimization | Dynamic eval weights via NUTS/VI |
| Cross-Judge Consensus | Multiple judges with variance detection |
| Bias Calibration | Periodic calibration against known benchmarks |
| Historical Learning System | SQLite database with pattern extraction |
| Automatic Version Increment | Semantic versioning based on eval deltas |
| Self-Monitoring Dashboard | Real-time health metrics |
| Resource Governor | VRAM/RAM/disk limit enforcement |
| All 6 blueprints active | Full domain coverage |

---

## 4. What Phase 3 Builds

| Feature | Details |
|---------|---------|
| Multi-agent collaboration | Peer review, specialized teams |
| Dynamic Model Selector | Automatic model choice per task |
| Automated loop execution | Cron-driven autonomous operation |
| Advanced maintenance | Intelligent pruning + compression |
| Full autonomy | Phase 3 from Human Oversight model |

---

## 5. Risk Assessment for Phase 1

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| delegate_task context too large | Medium | Truncate skills, compress history |
| Judge model inconsistent | Medium | Use same model + temperature=0.1 |
| USB I/O too slow for many writes | Low | Batch writes, async checkpoints |
| Agent timeout on complex tasks | Medium | Increase timeout, simplify first tasks |

---

## 6. Immediate Next Actions (Day 1 of Phase 1)

1. Rebuild `scripts/forge.py` with validated spawn pipeline
2. Rebuild `hardware/detect.py` with auto-profiling
3. Create `state.yaml` from Data_Models.md schema
4. Implement `atomic_write()` from Filesystem_Transactions.md
5. Spawn first code-reviewer agent against code-review-basic
6. Run first complete eval (self-eval + judge-eval)
7. Create first checkpoint
8. Celebrate first working loop iteration 🎉

---

**Status:** Phase 0 complete. Phase 1 ready to begin on your command.
