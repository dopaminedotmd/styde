# Phase 1 — Exact Scope

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 00_Implementation_Overview
**References:** `Phase0_to_Phase1_Transition.md`, `Dashboard Phase0_to_Phase1.md`, `PHASE1_ROADMAP.md`

---

## 1. What Phase 1 Builds

Phase 1 builds the **minimum viable system**: one complete forge loop iteration + a functional dashboard with chat.

### Forge — Core Loop (P0)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `forge.py` — Main orchestrator | ~300 | `Core_Loop_Detail.md` |
| `detect.py` — Hardware detection | ~80 | `Hardware_Adaptation_Layer.md` |
| `blueprint_loader.py` — Load + validate | ~150 | `Skill_Loading_Mechanism.md`, `Blueprint_Validation.md` |
| `spawn.py` — delegate_task wrapper | ~100 | `Component_Interfaces.md` §3.2 |
| `eval_runner.py` — Self-eval + judge-eval | ~250 | `Core_Loop_Detail.md` §3 |
| `composite_scorer.py` — Weighted scoring | ~80 | `Core_Loop_Detail.md` §3e |
| `teacher.py` — Feedback + skill extraction | ~200 | `Teacher_Agent.md` |
| `persistence.py` — Atomic writes + checkpoints | ~150 | `Filesystem_Transactions.md`, `Atomic_Checkpoint_Writes.md` |
| `recovery.py` — Crash detection + restore | ~120 | `Automatic_Recovery.md` |
| `circuit_breaker.py` — Failure protection | ~80 | `Core_Loop_Detail.md` §7 |
| `rag.py` — FAISS + embeddings on 3080 | ~150 | `RAG_Retrieval.md` |
| **Forge total** | **~1,660** | |

### Dashboard — Mission Control (P0)
| Component | Technology | Phase 0 Ref |
|-----------|-----------|-------------|
| Tauri scaffold | Rust + HTML/CSS/JS | `Desktop_Framework_Choice.md` |
| 3-panel layout | CSS Grid | `Layout_Design.md` |
| Dark theme | CSS variables | `Design_System.md` |
| DeepSeek provider | TypeScript | `Provider_Architecture.md`, `Built_In_Providers.md` |
| Chat panel (streaming) | Web Components + marked.js | `Chat_Architecture.md` |
| Chat tools (read/write/search) | Rust commands + Tauri invoke | `Chat_Agent_Tools.md` |
| Agent panel (list agents) | Web Components + polling | `Agent_Tracking.md` |
| Hermes CLI bridge | Rust `std::process::Command` | `Hermes_CLI_Bridge.md` |
| Start/Stop buttons | Rust + Tauri events | `Start_Stop_Pipeline.md` |
| Status bar | Web Components | `Layout_Design.md` §5 |
| Configuration panel | Web Components + JSON | `Configuration_Panel.md` |

---

## 2. What Phase 1 Does NOT Build (Deferred to Phase 2+)

### Forge — Deferred
| Feature | Why deferred | Phase |
|---------|-------------|-------|
| Bayesian Weight Optimization | Needs ≥100 evals for convergence | Phase 2 |
| Cross-Judge Consensus (multi-model) | Needs working judge first | Phase 2 |
| Bias Calibration | Needs benchmark history | Phase 2 |
| Historical Learning System (SQLite) | Keep simple: YAML logs first | Phase 2 |
| Automatic Version Increment | Manual bumps sufficient initially | Phase 2 |
| Dynamic Model Selector | Single-model eval (deepseek-v4-pro) is enough | Phase 2 |
| Resource Governor | YOLO on Machine-B (18GB is plenty for API calls) | Phase 2 |
| Multi-agent collaboration | Sequential loop first (D09) | Phase 3 |
| Full autonomy (cron-driven) | Manual/semi-automated first | Phase 3 |
| NUTS/HMC/VI sampling | Only VI on Machine-B, skip HMC/NUTS | Phase 2 |

### Dashboard — Deferred
| Feature | Why deferred | Phase |
|---------|-------------|-------|
| Benchmark panel (graphs) | Needs agent data first | P2 (dashboard) |
| System Health Monitoring | Nice to have | P2 (dashboard) |
| Ollama provider | Not critical | P2 (dashboard) |
| Custom provider (OpenAI-compatible) | Not critical | P2 (dashboard) |
| Spawn New Agent from dashboard | Manual spawn via Hermes CLI works | P2 (dashboard) |
| Auto-update | Manual updates fine for MVP | P2 (dashboard) |
| Multiple additional providers (Anthropic) | DeepSeek covers both Forge needs | P1 (dashboard) |

---

## 3. Minimum Viable Loop

The absolute minimum that proves Phase 1 is working:

```
1. python scripts/forge.py init              # USB dirs + state.yaml
2. python scripts/detect.py                  # Hardware profile
3. python scripts/forge.py spawn code-reviewer code-review-basic
   → delegate_task creates agent
   → Agent produces output
4. python scripts/eval_runner.py run <agent-id> code-review-basic
   → Self-eval runs
   → Judge-eval runs
   → Composite score computed
5. python scripts/forge.py improve <blueprint>
   → Teacher analyzes eval
   → Blueprint updated or agent promoted/archived
6. python scripts/forge.py checkpoint
   → State snapshot saved atomically
```

**One loop iteration. End-to-end.** That's the Phase 1 goal.

---

## 4. Exit Criteria — Phase 1 Complete

### Forge Exit Criteria
- [ ] `forge.py init` creates complete USB directory structure
- [ ] Hardware detection works (nvidia-smi → hardware_profile.json)
- [ ] Blueprint loading validates and builds spawn context
- [ ] `forge.py spawn` successfully calls `delegate_task`
- [ ] Self-eval runs against rubric, produces YAML score
- [ ] Judge-eval runs (deepseek-v4-pro), produces YAML score
- [ ] Composite scoring weights self+judge correctly
- [ ] Teacher analyzes eval, proposes concrete improvements
- [ ] Code-reviewer completes 10 loop iterations with improving scores
- [ ] At least one agent reaches ≥85/100
- [ ] Checkpoint → crash → recovery works without data loss
- [ ] Atomic writes guarantee no partial files (tested with forced USB disconnect)

### Dashboard Exit Criteria
- [ ] `StydeForge.exe` launches on Windows (double-click)
- [ ] Dark theme with 3 resizable panels displayed
- [ ] Chat works with DeepSeek (streaming)
- [ ] Chat can read files (`read_file`)
- [ ] Chat can write files (`write_file` with confirmation)
- [ ] Agent panel shows active agents from Hermes
- [ ] Start/Stop buttons function (spawn/kill Hermes processes)
- [ ] Status bar shows agent count, tokens, cost
- [ ] App minimizes to system tray
- [ ] Configuration saves and loads (config.json)

---

## 5. What Success Looks Like

After Phase 1, Pontus can:

1. **Plug in USB** on any machine
2. **Double-click StydeForge.exe** → dashboard opens
3. **Press Start** → Forge loop begins
4. **Watch agents improve** in the agent panel
5. **Chat with DeepSeek** to inspect results, tweak configs
6. **Press Stop** → graceful shutdown with checkpoint
7. **Unplug USB** → everything saved atomically

---

**Status:** Scope locked. This is what Phase 1 delivers.
