# Week Execution Plan — Phase 2

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 08_Integration
**References:** `IMPLEMENTATION_ORDER.md`, `PHASE2_SCOPE.md`

---

## Overview

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1-2 | Eval Depth | Bayesian weights, cross-judge consensus, bias calibration |
| 3-4 | Learning Systems | Historical learning (SQLite), auto-version, model selector, self-monitor |
| 5-6 | Resource Management | Resource governor, GPU balancer, task queue |
| 7-8 | Multi-Agent | Phase gates, agent comms, task decomposer, specialized roles |
| 9-10 | Automation | Smart cache, batch eval, auto benchmarks, prompt optimizer, curriculum |
| 11-12 | Integration + Dashboard P1/P2 | E2E tests, dashboard panels, providers, polish |

---

## Weeks 1-2 — Eval Depth (Days 1-14)

### Days 1-3: Bias Calibration
```
□ bias_calibrator.py
  - calibrate_judge(model_name, benchmarks) → bias_profile
  - Run against HumanEval, MMLU, and code-review-basic
  - Measure: leniency (avg score above baseline), strictness (below), variance
  - Store per-model profiles in 99_INDEXES/bias_profiles/
  - Output: bias_calibration.yaml per model

□ Validation
  - deepseek-v4-pro bias profile generated
  - deepseek-v4-flash bias profile generated
  - Ollama Qwen3.6-27B bias profile generated (if available)
  - Manual review: do bias scores match intuition?
```

### Days 4-7: Cross-Judge Consensus
```
□ cross_judge.py
  - CrossJudgePanel class
  - Primary judge: deepseek-v4-pro (temp=0.1)
  - Secondary judge: deepseek-v4-flash (temp=0.1)
  - Each judge: fresh delegate_task, agent output + rubric only
  - Apply bias_calibrator to each judge's raw score
  - Variance detection: flag if any judge >15 points from median
  - Consensus: median of calibrated scores
  - Consensus score: 0-1 range (how much judges agree)

□ Validation
  - Run against 5 existing agent outputs
  - Compare: single judge vs multi-judge scores
  - Verify: variance detection catches real disagreements
  - Verify: calibrated scores closer than raw scores
```

### Days 8-11: Bayesian Weight Optimization
```
□ bayesian_weights.py
  - Weight space: w_self, w_judge, w_consensus (sum = 1)
  - Prior: Dirichlet(1,1,1)
  - Likelihood: how well weighted composite predicts ground truth
  - NUTS sampler (Machine-A) or VI (Machine-B)
  - Minimum 30 evals before first optimization
  - Re-optimize every 20 new evals
  - Output: optimized_weights.yaml per blueprint

□ Validation
  - Test with synthetic eval data (known ground truth)
  - Verify weights converge to expected values
  - Compare NUTS vs VI results
  - Verify fallback: fixed weights if <30 evals
```

### Days 12-14: Eval Runner Upgrade
```
□ eval_runner.py upgrade
  - load bayesian_weights per blueprint (or fixed if unavailable)
  - replace single judge with CrossJudgePanel
  - apply bias calibration
  - composite = w_self*self + w_judge*judge + w_consensus*consensus
  - backward compatible: Phase 1 behavior if phase2_features.bayesian_weights=false
  - Update forge.py eval command

□ Validation
  - Run existing code-review-basic eval with Phase 1 weights → same score
  - Run with Phase 2 weights → different (hopefully better calibrated) score
  - Verify feature flag toggles correctly
```

---

## Weeks 3-4 — Learning Systems (Days 15-28)

### Days 15-18: Historical Learning (SQLite)
```
□ historical_learning.py
  - SQLite schema: evals, patterns, blueprints, versions, agents
  - Migration: import all existing eval/*.yaml files into DB
  - Pattern extraction:
    * Slowest-improving dimension per blueprint
    * Correlated blueprints (score movements together)
    * Threshold analysis (what score predicts production?)
  - API: get_blueprint_history(name) → DataFrame-like
  - API: extract_patterns() → list[Pattern]
  - WAL mode, async writes

□ forge.py upgrade-phase2
  - Creates forge_history.db
  - Migrates existing data
  - Validates integrity
  - Non-destructive (works on copy first)
```

### Days 19-21: Automatic Version Increment
```
□ auto_version.py
  - Parse current version: MAJOR.MINOR.PATCH
  - Rules:
    * Score ≥85 (quality gate) → MAJOR bump
    * Score improved ≥5 pts → MINOR bump
    * Score changed <5 pts → PATCH bump
  - Update blueprint config.yaml on save
  - Version history in blueprint metadata
  - CLI: forge.py version <blueprint> → show history

□ Validation
  - Test all bump scenarios
  - Verify version persists across sessions
  - Verify version history in SQLite
```

### Days 22-24: Dynamic Model Selector
```
□ model_selector.py
  - Model profiles: quality, cost_per_1k_tokens, latency
  - Decision matrix based on task type:
    * EVAL → deepseek-v4-pro (quality critical)
    * SPAWN_SIMPLE → deepseek-v4-flash (cost efficient)
    * BATCH_LOW → local model (free, if available)
  - Track cost vs Phase 1 baseline
  - Override via blueprint config: agent.model_override

□ Validation
  - Spawn agent with flash → verify lower cost, acceptable quality
  - Spawn agent with pro → verify higher quality
  - Verify cost tracking differences
```

### Days 25-28: Self-Monitoring + Health
```
□ self_monitor.py
  - Track: loop_duration, eval_latency, spawn_success_rate, api_errors
  - Anomaly: z-score >3 on any metric in sliding window
  - Health checks: disk_space, db_integrity, api_key_valid
  - CLI: forge.py health → status report
  - API: get_health() → JSON for dashboard

□ Validation
  - Run 10 loops, verify metrics collected
  - Inject anomaly (kill API key) → verify detection
  - Verify health endpoint returns valid JSON
```

---

## Weeks 5-6 — Resource Management (Days 29-42)

### Days 29-32: Resource Governor
```
□ resource_governor.py
  - Per-blueprint limits: vram_gb, ram_gb, disk_mb, timeout_s
  - Limits from blueprint config.yaml: agent.resources
  - Soft limit: warn at 80% usage
  - Hard limit: kill agent at 100% (with checkpoint)
  - Track usage in agent metadata

□ Validation
  - Set low VRAM limit (0.5 GB) → verify agent killed
  - Verify soft limit warning appears in logs
  - Verify agent state updated on kill
```

### Days 33-36: GPU Load Balancer
```
□ gpu_balancer.py
  - Detect GPUs via CUDA + NVML
  - Assign by type: LLM to 3080 (more VRAM), embeddings to 3070 Ti
  - Handle CUDA quirk (dev0=3080, dev1=3070Ti)
  - Fallback: CPU if GPUs saturated
  - Balance: if GPU A >80% util, route to GPU B

□ Validation
  - Verify GPU detection works on both machines
  - Test with dual workload: LLM + FAISS on separate GPUs
  - Verify fallback when one GPU offline
```

### Days 37-42: Task Queue System
```
□ task_queue.py
  - PriorityQueue class
  - Levels: CRITICAL, HIGH, NORMAL, LOW, BATCH
  - FIFO within same priority
  - Max concurrent: configurable (3 default)
  - Batching: group LOW into one API call
  - Starvation: age-based priority boost (+1 level every 5 min)

□ Validation
  - Submit 10 tasks with mixed priorities
  - Verify CRITICAL processed first
  - Verify batching: NORMAL grouped into one call
  - Verify starvation boost activates
```

---

## Weeks 7-8 — Multi-Agent (Days 43-56)

### Days 43-46: Phase Gates
```
□ phase_gates.py
  - Define phases in blueprint: PLAN → CODE → REVIEW → TEST → DEPLOY
  - Gate approval: teacher evaluates phase output
  - Retry: max 3 per phase, then escalate to human
  - Gate config: phases[].gate = {evaluator, max_retries, timeout}

□ Validation
  - Two-phase task: PLAN → CODE
  - Inject bad PLAN → verify gate rejects, retries
  - Verify max 3 retries → escalation
  - Verify successful pass → next phase starts
```

### Days 47-50: Agent Communication
```
□ agent_comms.py
  - Message protocol: {from, to, type, payload, timestamp, correlation_id}
  - Types: HANDOFF, REQUEST, RESPONSE, BROADCAST, ERROR
  - Transport: file-based inbox dir per agent
  - Agent polls inbox every 5s during execution
  - Handoff: Agent A writes output → Agent B's inbox

□ Validation
  - Agent A sends HANDOFF to Agent B
  - Agent B receives, processes, sends RESPONSE
  - Verify correlation_id tracking
  - Verify BROADCAST reaches all agents
```

### Days 51-53: Task Decomposer
```
□ task_decomposer.py
  - Input: complex task description
  - LLM decomposes into sub-tasks
  - Sub-tasks: {id, description, depends_on[], toolsets[], estimated_tokens}
  - Validation: no circular deps, all deps exist
  - Output: ordered execution plan

□ Validation
  - Decompose "Build a REST API with auth, tests, and docs"
  - Verify 5+ sub-tasks generated
  - Verify dependency tree is valid (no cycles)
  - Verify each sub-task has appropriate toolsets
```

### Days 54-56: Specialized Roles
```
□ specialized_roles.py
  - Role registry: Researcher, Debugger, SecurityAuditor, Refactorer, Architect, DevOps
  - Each role: system prompt additions + toolsets
  - Blueprint config: agent.role → loads role definition
  - Role inheritance: base persona + role additions

□ Validation
  - Spawn Security Auditor agent → verify security tools loaded
  - Spawn Researcher agent → verify research tools loaded
  - Verify role prompt injected correctly
```

---

## Weeks 9-10 — Automation (Days 57-70)

### Days 57-59: Smart Cache + Batch Eval
```
□ smart_cache.py
  - Cache key: hash(prompt + model + temperature + rubric_id)
  - TTL: 24h default, configurable
  - Invalidate: blueprint version bump
  - Stats: hit rate, token savings, cache size

□ batch_eval.py
  - Group N evals into one API call (N ≤ 5)
  - Prompt: array of agent outputs + rubrics
  - Response: array of eval YAML blocks
  - Fallback: individual if batch fails

□ Validation
  - Run same eval twice → verify cache hit on second
  - Batch 3 evals → verify 3 results returned
  - Verify cache invalidates on version bump
```

### Days 60-63: Auto Benchmark Generation
```
□ auto_benchmarks.py
  - Input: existing benchmark (code-review-basic)
  - LLM generates variations: same rubric, different code
  - Validate: generated benchmark passes validation checks
  - Store: eval/benchmarks/auto/<name>/
  - Cap: max 20 auto-benchmarks

□ Validation
  - Generate 3 variations of code-review-basic
  - Run existing agent against generated benchmarks
  - Verify scores are reasonable (not all 100 or 0)
  - Manual review of generated quality
```

### Days 64-67: Prompt Optimizer
```
□ prompt_optimizer.py
  - Analyze eval dimension scores → find weak areas
  - Propose prompt changes to target weak dimensions
  - A/B test: old prompt vs new prompt on same task
  - Accept: new_score > old_score + 2
  - Track prompt versions

□ Validation
  - Run A/B test with intentional poor prompt
  - Verify optimizer detects weak dimension
  - Verify new prompt scores higher
  - Verify rejection if no improvement
```

### Days 68-70: Curriculum Learning
```
□ curriculum.py
  - Difficulty levels per benchmark: EASY, MEDIUM, HARD, EXPERT
  - Agent starts at EASY
  - Advance: score ≥85 for 3 consecutive runs
  - Demote: score <70 for 3 consecutive runs
  - Track: curriculum position per agent

□ Validation
  - Agent runs EASY 3× with ≥85 → advances to MEDIUM
  - Agent runs MEDIUM 3× with <70 → demotes to EASY
  - Verify benchmark has tasks at all levels
```

---

## Weeks 11-12 — Integration + Dashboard (Days 71-84)

### Days 71-73: Knowledge Graph
```
□ knowledge_graph.py
  - Nodes: Blueprint, Agent, Eval, Pattern, Skill, Benchmark
  - Edges: SPAWNED_FROM, EVALUATED_AGAINST, IMPROVED_BY, EXTRACTED_FROM
  - SQLite adjacency table
  - Queries: "Show all agents improved by pattern X"
  - Export: DOT format for Graphviz visualization

□ Validation
  - Run 10 loops → graph populated
  - Query: "blueprints with most agents" → verify
  - Export DOT → verify valid syntax
```

### Days 74-78: Dashboard P1 — Providers + Detail
```
□ OpenAI provider → chat works with GPT-4
□ Anthropic provider → chat works with Claude
□ Ollama provider → chat works with local Qwen
□ Custom provider UI → add/remove/configure
□ Agent detail view → click agent card → full details
□ Chat sessions → save/load/export sessions
```

### Days 79-81: Dashboard P2 — Monitoring + Control
```
□ Benchmark panel → Chart.js line charts
□ Health monitoring → CPU/GPU/RAM/Disk gauges
□ System tray → minimize, notifications
□ Spawn from UI → blueprint + benchmark form
□ Auto-update → tauri-updater integration
```

### Days 82-84: End-to-End Tests + Polish
```
□ Full E2E test: multi-agent + multi-judge
□ Performance: verify Phase 2 loop <90s (Phase 1 was <60s)
□ Cost audit: verify ≥25% savings vs Phase 1
□ Bug fixes from integration testing
□ Documentation: README, run instructions, troubleshooting
□ Pontus review + final adjustments
```

---

## Milestone Summary

| Milestone | End of Week | Success Criterion |
|-----------|------------|-------------------|
| **M1: Eval Rigor** | Week 2 | Bayesian weights + multi-judge working |
| **M2: Learning Live** | Week 4 | SQLite history + auto-version + model selector |
| **M3: Scale Ready** | Week 6 | Resource governor prevents crashes at 10+ agents |
| **M4: Agents Collaborate** | Week 8 | Two agents hand off work via phase gates |
| **M5: Self-Improving** | Week 10 | Cache saves 30%, auto-benchmarks generate valid tasks |
| **M6: Phase 2 Complete** | Week 12 | All exit criteria met, Pontus approved |

---

## Risk Timeline

| Week | Risk | Mitigation |
|------|------|------------|
| 1-2 | NUTS doesn't converge | Fall back to fixed weights |
| 1-2 | Multi-judge 3× API cost | Use flash model, batch judges |
| 3-4 | SQLite migration corrupts data | Copy-first migration, validate |
| 5-6 | GPU quirk causes wrong assignments | Use known workaround from memory |
| 7-8 | Agent comms race conditions | File locks, correlation IDs |
| 9-10 | Auto-benchmarks low quality | Manual review gate, max 20 limit |
| 11-12 | Integration scope creep | Strict P0 exit criteria. New ideas → Phase 3 |

---

**Status:** Plan defined. 12 weeks, 6 milestones, 12 exit criteria categories.
