# Phase 2 — Exact Scope

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 00_Overview
**References:** `Phase0_to_Phase1_Transition.md` §3, `PHASE1_SCOPE.md` §2, `PHASE1_ROADMAP.md`

---

## 1. What Phase 2 Builds

Phase 2 deepens eval rigor, adds learning systems, enables multi-agent collaboration,
and brings the dashboard to P1/P2 maturity.

### Forge — Eval Depth (P0)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `bayesian_weights.py` — NUTS/VI-driven weight optimization | ~250 | `Bayesian_Weight_Optimization.md` |
| `cross_judge.py` — Multi-model judge panel | ~200 | `Cross_Judge_Consensus.md` |
| `bias_calibrator.py` — Periodic calibration runs | ~150 | `Bias_Calibration.md` |
| `eval_runner.py` — Upgraded: dynamic weights + multi-judge | ~100 (add) | Phase 1 `eval_runner.py` |
| **Eval Depth subtotal** | **~700** | |

### Forge — Learning Systems (P1)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `historical_learning.py` — SQLite + pattern extraction | ~300 | `Historical_Learning_System.md` |
| `auto_version.py` — Semantic versioning from eval deltas | ~120 | `Automatic_Version_Increment.md` |
| `model_selector.py` — Dynamic model choice per task | ~150 | `Dynamic_Model_Selector.md` |
| `self_monitor.py` — Health metrics + anomaly detection | ~200 | `Self_Monitoring_Health.md` |
| **Learning Systems subtotal** | **~770** | |

### Forge — Resource Management (P2)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `resource_governor.py` — VRAM/RAM/disk limits | ~180 | `Resource_Governor.md` |
| `gpu_balancer.py` — Multi-GPU work distribution | ~150 | `Hardware_Adaptation_Layer.md` |
| `task_queue.py` — Priority-based queue with batching | ~200 | Phase 1 spawn pipeline |
| **Resource Management subtotal** | **~530** | |

### Forge — Multi-Agent (P3)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `phase_gates.py` — Approval checkpoints between steps | ~120 | — |
| `agent_comms.py` — Structured inter-agent messaging | ~180 | `Multi_Agent_Collaboration.md` |
| `task_decomposer.py` — Auto-break complex tasks | ~250 | Phase 1 spawn |
| `specialized_roles.py` — Role-specific prompts + tools | ~100 | Phase 1 Top 20 Agents |
| **Multi-Agent subtotal** | **~650** | |

### Forge — Automation (P4)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `auto_benchmarks.py` — Generate new test tasks | ~250 | Phase 1 eval |
| `prompt_optimizer.py` — Improve prompts from eval data | ~200 | Phase 1 teacher |
| `curriculum.py` — Progressive difficulty scaling | ~150 | Phase 1 teacher |
| `knowledge_graph.py` — Neo4j/SQLite graph of relationships | ~300 | `Knowledge_Management.md` |
| **Automation subtotal** | **~900** | |

### Forge — Cost & Efficiency
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `smart_cache.py` — Cache common responses, 30-50% token savings | ~150 | Phase 1 cost tracking |
| `batch_eval.py` — Batch multiple evals in one API call | ~120 | Phase 1 eval |
| **Efficiency subtotal** | **~270** | |

### Forge — Blueprint Lifecycle (NEW)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `version_history.py` — Git-like diffable history per blueprint | ~200 | `auto_version.py` |
| `blueprint_diff.py` — Semantic diff between blueprint versions | ~150 | — |
| `rollback.py` — Atomic rollback to any previous version | ~100 | `checkpoint.py` |
| **Blueprint Lifecycle subtotal** | **~450** | |

### Forge — CI/CD Integration (NEW)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `forge.py ci` — Run benchmark suite, output JUnit XML | ~150 | Phase 1 eval |
| `github_actions/setup-forge` — Composite action for CI | ~80 | — |
| `ci_reporter.py` — PR comments, status checks, badge generation | ~120 | — |
| **CI/CD subtotal** | **~350** | |

### Forge — Natural Language Control (NEW)
| Component | Lines (est.) | Phase 0 Ref |
|-----------|-------------|-------------|
| `forge_chat.py` — Chat-driven Forge: "Improve my email drafter" | ~250 | — |
| `nl_blueprint.py` — Describe agent in Swedish → blueprint + benchmark | ~200 | `Import_Strategy.md` |
| `forge_voice.py` — Voice interface via Hermes TTS/STT | ~100 | — |
| **NL Control subtotal** | **~550** | |

### Dashboard — P1/P2 Features
| Component | Technology | Phase 0 Ref |
|-----------|-----------|-------------|
| Benchmark panel (Chart.js graphs) | HTML/CSS/JS | `Performance_Metrics.md`, `Visualization_Strategy.md` |
| Health monitoring panel | HTML/CSS/JS + Rust polling | `Health_Monitoring.md` |
| OpenAI + Anthropic providers | TypeScript | `Built_In_Providers.md` |
| Ollama provider | TypeScript + Rust sidecar | `Local_Model_Support.md` |
| Custom provider (OpenAI-compatible) | TypeScript | `Custom_Provider_API.md` |
| Agent detail view (tokens, cost, history) | HTML/CSS/JS | `Agent_Detail_View.md` |
| Spawn New Agent from UI | HTML/CSS/JS + Rust | `Spawn_New_Agent.md` |
| System tray + notifications | Rust (tauri) | `System_Tray_Integration.md` |
| Chat sessions (save/load) | IndexedDB | `Chat_Persistence.md` |
| Auto-update | Rust (tauri-updater) | `Auto_Update.md` |

### Forge Total: ~5,170 lines (new + modified)
### Dashboard: Reuses existing Tauri scaffold, adds ~8 panels/features

---

## 2. What Phase 2 Does NOT Build (Deferred to Phase 3)

| Feature | Why deferred | Phase |
|---------|-------------|-------|
| Hierarchical Multi-Agent (manager→workers) | Needs stable agent comms first | Phase 3 |
| Supervised Collaborative Refinement (SCR) | Production-grade; needs Phase 2 foundation | Phase 3 |
| Agent Memory Sharing (cross-agent) | Needs knowledge graph first | Phase 3 |
| Conflict Resolution (contradictory outputs) | Rare in sequential loops | Phase 3 |
| Evolutionary Algorithms for Blueprints | Needs genetic representation system | Phase 3 |
| Meta-Learning (learn how to improve) | Needs historical learning data first | Phase 3 |
| Cross-Project Learning | Needs multiple forge instances | Phase 3 |
| Forge Evolution Engine (self-modify) | Ultimate autonomy — Phase 3 goal | Phase 3 |
| Agent DNA / Genetic Representation | Needs evolutionary framework | Phase 3 |
| Long-term Goal Tracking (weeks/months) | Needs autonomous loop first | Phase 3 |
| Web UI / Command Center (beyond dashboard) | Dashboard covers this | Phase 3 |
| Visual Loop Debugger | Nice to have | Phase 3 |
| Blueprint Visual Editor | GUI complexity | Phase 3 |
| Plugin System | Extensibility architecture | Phase 3 |

---

## 3. What Phase 2 Upgrades from Phase 1

| Phase 1 Component | Phase 2 Change |
|-------------------|----------------|
| `eval_runner.py` | + dynamic Bayesian weights, + multi-judge consensus, + bias calibration |
| `composite_scorer.py` | Fixed weights → NUTS/VI-optimized weights that evolve per blueprint |
| `teacher.py` | + historical context from SQLite, + pattern extraction |
| `forge.py` | + `forge.py optimize` (Bayesian), + `forge.py calibrate` (bias) |
| `blueprint.py` | + auto-version increment on save |
| `state.yaml` | + `eval_weights` section, + `learning` section, + `resource_limits` |
| Dashboard chat | + patch + terminal tools, + /skill commands |
| Dashboard providers | + OpenAI, Anthropic, Ollama, custom |
| Dashboard agent panel | + detail view, + spawn button |

---

## 4. Phase 2 Exit Criteria

### Eval Depth
- [ ] Bayesian weight optimization converges within 50 evals per blueprint
- [ ] Cross-judge consensus (3 judges) detects and flags outlier scores
- [ ] Bias calibration completes in <5 minutes, produces calibration report
- [ ] Composite scores more stable (std dev <5 points vs Phase 1's ~10)

### Learning Systems
- [ ] Historical learning extracts ≥3 patterns from 100+ evals
- [ ] Auto-version correctly bumps major/minor/patch based on eval deltas
- [ ] Model selector picks cheaper model for simple tasks, saves ≥20% cost
- [ ] Self-monitor detects anomalies within 3 loop iterations

### Resource Management
- [ ] Resource governor prevents any agent from exceeding VRAM limit
- [ ] GPU balancer distributes work across 3080 + 3070 Ti
- [ ] Task queue correctly prioritizes and batches without starvation

### Multi-Agent
- [ ] Phase gates prevent garbage from propagating (≤2% false approvals)
- [ ] Agent-to-agent communication delivers messages with <1s latency
- [ ] Task decomposer splits a complex task into ≥3 sub-tasks correctly

### Dashboard
- [ ] Benchmark panel shows live graphs with <5s update latency
- [ ] Health monitoring shows CPU/GPU/RAM/disk in real-time
- [ ] OpenAI + Anthropic + Ollama providers all work (streaming)
- [ ] Spawn New Agent from UI completes successfully
- [ ] Auto-update downloads and applies updates

### Cost & Efficiency
- [ ] Smart caching saves ≥30% tokens on repeated patterns
- [ ] Batch eval processes ≥3 evals in one API call
- [ ] Total cost per loop iteration reduced by ≥25% vs Phase 1

### Blueprint Lifecycle
- [ ] Version history stores every blueprint change with timestamp + diff
- [ ] Semantic diff identifies what actually changed (not just whitespace)
- [ ] Rollback to any version restores exact blueprint state
- [ ] At least 10 versions stored for code-reviewer blueprint

### CI/CD
- [ ] `forge.py ci` runs full benchmark suite, exits non-zero on failure
- [ ] JUnit XML output compatible with GitHub Actions
- [ ] PR comments posted when agent score changes by ≥2 points
- [ ] Status badge shows current top agent score

### Natural Language Control
- [ ] "Forge, improve my email drafter" spawns eval loop for that blueprint
- [ ] "Forge, bygg en agent som granskar svenska avtal" creates blueprint + benchmark
- [ ] Voice interface: speak command → STT → Forge action → TTS response
- [ ] NL commands cover all major forge operations (spawn, eval, improve, status)

---

## 5. What Success Looks Like

After Phase 2, Pontus can:

1. **Trust eval scores** — Bayesian weights + multi-judge + bias calibration = confidence
2. **See the forge learning** — Historical patterns extracted, versions auto-incremented
3. **Run 10+ agents safely** — Resource governor prevents crashes, queue prevents starvation
4. **Collaborate between agents** — Agent A passes work to Agent B with phase gates
5. **Use any model** — Switch between DeepSeek, OpenAI, Anthropic, Ollama from dashboard
6. **Monitor everything** — Live graphs of scores, costs, health in dashboard
7. **Save money** — Smart caching + batch evals + model selector cut costs significantly
8. **Track blueprint evolution** — Full version history with diffs, rollback to any point
9. **Run CI on agents** — GitHub Actions runs benchmark suite on every blueprint change
10. **Talk to Forge** — "Forge, förbättra min code-reviewer" — på svenska, i chat eller röst

---

## 6. Risk Assessment for Phase 2

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| NUTS doesn't converge with <100 evals | Medium | Medium | Fall back to fixed weights, mark blueprint as "insufficient data" |
| Multi-judge increases API cost 3× | High | Medium | Use cheaper models for 2nd/3rd judge (deepseek-v4-flash). Batch judges |
| SQLite on USB causes latency | Low | Medium | WAL mode, async writes, keep DB <100MB |
| Ollama integration breaks on Windows | Medium | Low | Test early, fall back to API providers |
| GPU balancing conflicts with CUDA enumeration | Medium | Low | Use known quirk workaround (dev0=3080, dev1=3070Ti) |
| Multi-agent comms add complexity without value | Low | High | Start with Phase Gates only (simplest pattern), add comms only if needed |
| NL commands misinterpreted by LLM | Medium | Medium | Strict command grammar, confirmation before destructive actions |
| Blueprint version history bloats USB | Low | Low | Max 50 versions. Compress diffs. Prune versions older than 90 days |
| CI runner slow on GitHub free tier | Medium | Low | Cache dependencies, limit benchmark suite to 5 tasks in CI |

---

**Status:** Scope locked. This is what Phase 2 delivers.
