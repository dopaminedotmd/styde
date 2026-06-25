# Phase 1 → Phase 2 Transition Plan

**Styde Forge v3.0 — Phase 2**
**Section:** 00_Overview
**References:** Phase 1 `P0_Exit_Criteria.md`, Phase 1 `PHASE1_SCOPE.md` §4

---

## 1. Phase 1 Completion Criteria (Entry Gates for Phase 2)

Phase 2 starts ONLY when Phase 1 meets ALL of the following:

| # | Criterion | Phase 1 Exit Ref | Verifiable By |
|---|-----------|-----------------|---------------|
| 1 | Core loop works end-to-end | F1-F4 | `forge.py loop code-reviewer code-review-basic` completes |
| 2 | Self-eval + judge-eval produce valid scores | F5-F7 | `eval.yaml` contains composite score |
| 3 | Teacher produces actionable improvements | F8 | `teacher_review.yaml` has concrete proposals |
| 4 | code-reviewer completes 10 loop iterations | F9 | `loop_iterations >= 10` in state.yaml |
| 5 | At least one agent reaches ≥85/100 | F10 | Agent in `StydeAgents/production/` |
| 6 | Checkpoint → crash → recovery works | F11 | Force-kill during checkpoint, verify restore |
| 7 | Atomic writes guarantee no partial files | F12 | USB disconnect test passes |
| 8 | Dashboard launches, chat with DeepSeek works | D1-D6 | `StydeForge.exe` functional |
| 9 | Agent panel shows live agents | D7 | Polling updates within 5s |
| 10 | Start/Stop buttons function | D8 | Graceful shutdown with checkpoint |

**Minimum bar for Phase 2 entry:** Criteria 1-5 (core loop works). 6-10 can be hardened during Phase 2.

---

## 2. Environment Readiness for Phase 2

### New Dependencies
| Dependency | Purpose | Install |
|-----------|---------|---------|
| SQLite3 | Historical learning DB | Built into Python 3.11+ ✅ |
| numpy | Bayesian optimization math | `pip install numpy` |
| scipy | NUTS/HMC sampling | `pip install scipy` |
| sklearn | Pattern extraction (PCA, clustering) | `pip install scikit-learn` |
| httpx | Async HTTP for multi-judge calls | `pip install httpx` |
| Chart.js | Dashboard benchmark graphs | `npm install chart.js` |
| tauri-plugin-store | Secure config storage | Cargo dependency |
| tauri-updater | Auto-update | Cargo dependency |

### Hardware Requirements
| Resource | Machine-A (Beast) | Machine-B (Main) |
|----------|-------------------|------------------|
| VRAM | 22 GB (3080+3070Ti) | 18 GB (3080+3070Ti) |
| RAM | 32 GB | 32 GB |
| Disk (USB) | 48 GB — need ≥10 GB free | Same |
| SQLite DB size | ~50 MB after 1000 evals | Same |

---

## 3. What Changes from Phase 1

### Architecture Changes
```
Phase 1:                          Phase 2:
  forge.py                         forge.py
  ├── spawn.py                     ├── spawn.py
  ├── eval_runner.py (single)      ├── eval_runner.py (multi-judge + Bayesian)
  ├── teacher.py                   ├── teacher.py (SQLite context)
  ├── checkpoint.py                ├── checkpoint.py
  └── (no history)                 ├── historical_learning.py ← NEW
                                   ├── auto_version.py ← NEW
                                   ├── model_selector.py ← NEW
                                   ├── self_monitor.py ← NEW
                                   ├── resource_governor.py ← NEW
                                   ├── gpu_balancer.py ← NEW
                                   ├── task_queue.py ← NEW
                                   ├── phase_gates.py ← NEW
                                   ├── agent_comms.py ← NEW
                                   ├── task_decomposer.py ← NEW
                                   ├── specialized_roles.py ← NEW
                                   ├── smart_cache.py ← NEW
                                   ├── batch_eval.py ← NEW
                                   ├── bias_calibrator.py ← NEW
                                   ├── cross_judge.py ← NEW
                                   └── bayesian_weights.py ← NEW
```

### State File Changes
```yaml
# New top-level sections in state.yaml:
eval_weights:           # Per-blueprint Bayesian weights
  code-reviewer:
    self_eval: 0.35
    judge_eval: 0.50
    consensus: 0.15
    optimized_at: "2026-07-15T..."
    method: "nuts"
    convergence_iterations: 47

learning:               # Historical learning state
  db_path: "99_INDEXES/forge_history.db"
  patterns_extracted: 12
  last_extraction: "2026-07-20T..."

resource_limits:        # Per-blueprint resource caps
  code-reviewer:
    vram_gb: 4.0
    ram_gb: 2.0
    disk_mb: 100
    timeout_s: 300

model_routing:          # Model selector state
  default_spawn: "deepseek-v4-flash"
  default_eval: "deepseek-v4-pro"
  cost_savings_vs_phase1: 0.32
```

---

## 4. Data Migration from Phase 1

Phase 1 data MUST be preserved and migrated:

| Phase 1 Data | Phase 2 Location | Migration |
|-------------|-----------------|-----------|
| `state.yaml` | Upgraded in-place | `forge.py upgrade` adds new sections |
| Agent outputs | `StydeAgents/refinery/*/runs/` | Read-only, imported into SQLite |
| Eval results | `StydeAgents/refinery/*/runs/*/eval.yaml` | Imported into `forge_history.db` |
| Blueprints | `blueprints/*/` | Auto-versioned on first Phase 2 save |
| Benchmarks | `eval/benchmarks/*/` | Unchanged |
| `hardware_profile.json` | `99_INDEXES/` | Unchanged |
| Checkpoints | `checkpoints/` | Read-only, new format for Phase 2 checkpoints |

### Migration Script
```bash
python scripts/forge.py upgrade-phase2
# 1. Creates forge_history.db from existing eval files
# 2. Adds eval_weights, learning, resource_limits, model_routing to state.yaml
# 3. Auto-versions all existing blueprints (start at 1.0.0)
# 4. Validates all data integrity
# 5. Creates Phase 2 checkpoint
```

---

## 5. Risk: Breaking Phase 1 During Phase 2 Development

| Risk | Mitigation |
|------|------------|
| Phase 2 code breaks working Phase 1 loop | Feature flags: all Phase 2 features default OFF. `caveman_ultra: true` in state.yaml → Phase 1 behavior |
| New dependencies fail to install | requirements-phase2.txt separate from Phase 1. Fall back gracefully |
| SQLite migration corrupts data | Migration runs on COPY of data. Original untouched until verified |
| Multi-judge API costs explode | Judge count configurable (1-5). Default: 2 in Phase 2, 3+ optional |

### Feature Flag System
```python
# Phase 2 features controlled by state.yaml flags:
phase2_features:
  bayesian_weights: false     # Enable after 30+ evals
  cross_judge: false          # Enable after bias calibration
  bias_calibration: false     # Enable after 10+ evals per model
  historical_learning: false  # Enable after SQLite migration
  auto_version: true          # Safe to enable immediately
  model_selector: false       # Enable after cost tracking works
  resource_governor: false    # Enable when running 5+ agents
  multi_agent: false          # Enable after phase gates tested
```

---

## 6. Immediate Next Actions (Day 1 of Phase 2)

1. Verify Phase 1 exit criteria 1-5 are met
2. Install Phase 2 Python dependencies
3. Run `forge.py upgrade-phase2` to create SQLite DB + migrate data
4. Enable `auto_version: true` (safe, no side effects)
5. Run first bias calibration against known benchmarks
6. Implement `smart_cache.py` (quick win, no dependencies)
7. Implement `batch_eval.py` (immediate cost savings)
8. Celebrate Phase 2 Day 1 🎉

---

**Status:** Transition plan defined. Entry gates specified.
