# Implementation Order — Dependency Graph

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 00_Overview
**References:** `DECISIONS.md`, Phase 1 `IMPLEMENTATION_ORDER.md`

---

## 1. Dependency Graph

```
Phase 1 Complete (working loop)
        │
        ├── P0: Eval Depth ─────────────────────────────────────┐
        │   │                                                     │
        │   ├── bias_calibrator.py  ← Needs: eval history        │
        │   │                                                     │
        │   ├── cross_judge.py      ← Needs: working eval        │
        │   │                           pipeline + 2nd model      │
        │   │                                                     │
        │   └── bayesian_weights.py ← Needs: 50+ evals for       │
        │                               convergence              │
        │                         ↓                               │
        ├── P1: Learning Systems ─────────────────────────────────┤
        │   │                                                     │
        │   ├── historical_learning.py ← Needs: eval history     │
        │   │                              (SQLite)              │
        │   ├── auto_version.py        ← Needs: eval deltas      │
        │   ├── model_selector.py      ← Needs: cost tracking    │
        │   └── self_monitor.py        ← Needs: running loop     │
        │                         ↓                               │
        ├── P2: Resource Management ──────────────────────────────┤
        │   │                                                     │
        │   ├── resource_governor.py   ← Needs: detect.py        │
        │   ├── gpu_balancer.py        ← Needs: hardware profile │
        │   └── task_queue.py          ← Needs: spawn pipeline   │
        │                         ↓                               │
        ├── P3: Multi-Agent ─────────────────────────────────────┤
        │   │                                                     │
        │   ├── phase_gates.py         ← Needs: eval pipeline    │
        │   ├── agent_comms.py         ← Needs: spawn pipeline   │
        │   ├── task_decomposer.py     ← Needs: spawn + eval     │
        │   └── specialized_roles.py   ← Needs: blueprint system │
        │                         ↓                               │
        └── P4: Automation + Dashboard ──────────────────────────┘
            │
            ├── auto_benchmarks.py     ← Needs: eval pipeline
            ├── prompt_optimizer.py    ← Needs: teacher + evals
            ├── curriculum.py          ← Needs: eval pipeline
            ├── knowledge_graph.py     ← Needs: historical learning
            ├── smart_cache.py         ← No dependencies
            ├── batch_eval.py          ← Needs: eval pipeline
            │
            └── Dashboard P1/P2 ─────── Parallel track
                ├── Benchmark panel    ← Needs: eval data
                ├── Health monitoring  ← Needs: self_monitor
                ├── New providers      ← No dependencies
                ├── Agent detail       ← Needs: agent panel
                └── Auto-update        ← No dependencies
```

---

## 2. Build Sequence — Forge

### Phase A: Eval Foundation (Week 1-2)
```
Priority 1 — Bayesian weights depend on multi-judge. Multi-judge depends on calibration.
Build in reverse dependency order:

  1. bias_calibrator.py
     - calibrate_judge(model, benchmarks) → bias_profile
     - Run against known benchmarks (HumanEval, MMLU scores)
     - Measure per-model leniency/strictness
     - Output: bias_calibration.yaml per model

  2. cross_judge.py
     - CrossJudgePanel class
     - Primary judge: deepseek-v4-pro (temp=0.1)
     - Secondary judge: deepseek-v4-flash (cheaper)
     - Tertiary judge: local model via Ollama (Qwen3.6-27B)
     - Variance detection: flag if any judge deviates >15 points
     - Consensus: median or mean after outlier removal

  3. bayesian_weights.py
     - NUTS sampler for weight space exploration
     - Prior: uniform(0,1) for each eval dimension
     - Likelihood: eval score accuracy vs ground truth
     - VI fallback on Machine-B (faster, less precise)
     - Output: optimized_weights.yaml per blueprint
     - Minimum 30 evals before optimization runs
     - Re-optimize every 20 new evals

  4. eval_runner.py (upgrade)
     - Replace fixed 0.4/0.6 → bayesian_weights.get(blueprint)
     - Replace single judge → CrossJudgePanel.evaluate()
     - Add bias_calibrator.apply() to raw scores
     - Backward compatible: if no Bayesian weights, use Phase 1 fixed weights
```

### Phase B: Learning Systems (Week 3-4)
```
Priority 2 — These make the forge smarter. Depend on eval pipeline working.

  5. historical_learning.py
     - SQLite schema: evals, patterns, blueprints, versions
     - Pattern extraction queries:
       * "What dimension improves slowest for code-reviewer?"
       * "Which blueprints correlate with each other?"
       * "What eval threshold predicts production readiness?"
     - Teacher gets historical context from SQLite, not just last 3 evals
     - DB location: 99_INDEXES/forge_history.db
     - WAL mode for concurrent reads during writes

  6. auto_version.py
     - Version schema: MAJOR.MINOR.PATCH
     - MAJOR bump: quality gate passed (≥85) → structural change
     - MINOR bump: score improved by ≥5 points
     - PATCH bump: score changed <5 points or teacher tweak
     - Auto-increment on blueprint save
     - Version history in blueprint metadata

  7. model_selector.py
     - Cost/quality profiles per model:
       * deepseek-v4-pro: high quality, high cost
       * deepseek-v4-flash: medium quality, low cost
       * local Qwen3.6-27B: variable quality, zero cost
     - Decision matrix:
       * Eval tasks → deepseek-v4-pro (quality critical)
       * Simple spawns → deepseek-v4-flash (cost efficient)
       * Batch/low-priority → local model (free)
     - Track cost savings vs Phase 1 baseline

  8. self_monitor.py
     - Metrics: loop_duration, eval_latency, spawn_success_rate, api_errors
     - Anomaly detection: z-score > 3 on any metric → alert
     - Health endpoint for dashboard polling
     - Log anomalies to state.yaml + logs/
```

### Phase C: Resource Management (Week 5-6)
```
Priority 3 — Needed when running 5+ agents simultaneously.

  9. resource_governor.py
     - Per-agent limits: VRAM (GB), RAM (GB), disk (MB), timeout (s)
     - Enforce via config.yaml limits
     - Soft limit: warn at 80%, hard limit: kill at 100%
     - Respect hardware profile (Machine-A vs Machine-B)
     - Track usage in agent metadata

  10. gpu_balancer.py
      - Detect both GPUs (3080 + 3070 Ti) via CUDA/NVML
      - Assign local model to 3080 (more VRAM), FAISS to 3070 Ti
      - If one GPU busy, route to other
      - Handle CUDA enumeration quirk (dev0=3080, dev1=3070Ti)
      - Fall back to CPU if both GPUs saturated

  11. task_queue.py
      - Priority levels: CRITICAL, HIGH, NORMAL, LOW, BATCH
      - FIFO within same priority
      - Batching: group LOW-priority evals into one API call
      - Max concurrent: 3 (Machine-B), 5 (Machine-A)
      - Starvation prevention: age-based priority boost
```

### Phase D: Multi-Agent (Week 7-8)
```
Priority 4 — Enables complex workflows. Phase gates first (simplest).

  12. phase_gates.py
      - Define checkpoints in agent workflow: PLAN → CODE → REVIEW → TEST → DEPLOY
      - After each phase: teacher evaluates output, approves/rejects
      - Reject → agent retries that phase (not whole task)
      - Max retries per phase: 3
      - Gate config in blueprint config.yaml: phases[].gate

  13. agent_comms.py
      - Message format: {from, to, type, payload, timestamp}
      - Types: HANDOFF, REQUEST, RESPONSE, BROADCAST
      - Transport: file-based (write to agent inbox dir)
      - Inbox: StydeAgents/refinery/<name>/inbox/
      - Poll inbox every 5s during agent execution

  14. task_decomposer.py
      - Input: complex task description
      - Output: ordered list of sub-tasks with dependencies
      - Uses LLM to decompose (one delegate_task call)
      - Sub-task format: {id, description, depends_on[], toolsets[], estimated_tokens}
      - Validate: no circular dependencies, all deps exist

  15. specialized_roles.py
      - Role definitions with custom system prompts
      - Roles: Researcher, Debugger, Security Auditor, Refactorer, Architect, DevOps
      - Each role gets role-specific toolsets (e.g., Security Auditor gets extra scan tools)
      - Role config in blueprint config.yaml: agent.role
      - Inherits from base agent persona + role-specific additions
```

### Phase E: Automation + Dashboard (Week 9-12)
```
Priority 5 — Polish, efficiency, and UX.

  16. smart_cache.py
      - Cache key: hash(prompt + model + temperature)
      - Cache store: 99_INDEXES/cache.db (SQLite, separate from history)
      - TTL: 24h default, configurable per blueprint
      - Invalidation: on blueprint version bump
      - Stats: cache hit rate, token savings

  17. batch_eval.py
      - Group N evals into one API call
      - Prompt: "Evaluate these N agent outputs against rubric..."
      - Response: array of N eval YAML blocks
      - N max: 5 (context window limit)
      - Fall back to individual evals if batch fails

  18. auto_benchmarks.py
      - Generate new benchmark tasks from existing ones
      - Use LLM to create variations (same rubric, different task)
      - Validate: generated benchmark must pass manual review
      - Store in eval/benchmarks/auto/
      - Max auto-benchmarks: 20 (avoid infinite generation)

  19. prompt_optimizer.py
      - Analyze eval results to find weak prompt areas
      - A/B test: old prompt vs optimized prompt on same task
      - Accept if optimized score > old score + 2 points
      - Track prompt versions in blueprint metadata

  20. curriculum.py
      - Difficulty levels: EASY, MEDIUM, HARD, EXPERT
      - Agent starts at EASY, advances when score ≥85 for 3 consecutive runs
      - Benchmark must have tasks at all difficulty levels
      - curriculum config in benchmark metadata

  21. knowledge_graph.py
      - Nodes: Blueprint, Agent, Eval, Pattern, Skill, Benchmark
      - Edges: SPAWNED_FROM, EVALUATED_AGAINST, IMPROVED_BY, EXTRACTED_FROM
      - Store: SQLite with adjacency table (no Neo4j dependency)
      - Queries: "Show all agents that improved from pattern X"
      - Visualize: export to DOT/Graphviz
```

---

## 3. Build Sequence — Dashboard

### Phase F: Providers + Detail (Week 5-7, parallel with Forge P2)
```
  22. OpenAI provider        → TypeScript, implements ModelProvider
  23. Anthropic provider     → TypeScript, implements ModelProvider
  24. Ollama provider        → TypeScript + Rust sidecar for ollama.exe
  25. Custom provider UI     → Web Components, OpenAI-compatible endpoint
  26. Agent detail view      → Click agent → tokens, cost, eval history, logs
  27. Chat sessions          → IndexedDB save/load, export to markdown
```

### Phase G: Monitoring + Control (Week 8-10, parallel with Forge P3)
```
  28. Benchmark panel        → Chart.js line charts: score over time, per blueprint
  29. Health monitoring      → Poll self_monitor.py, render gauges for CPU/GPU/RAM
  30. System tray            → Tauri tray API, minimize, notifications on agent completion
  31. Spawn from UI          → Form: blueprint selector + benchmark selector → spawn
```

### Phase H: Polish + Auto-update (Week 11-12)
```
  32. Auto-update            → tauri-updater plugin, GitHub releases
  33. Configuration polish   → All settings in UI, save/load config profiles
  34. Error states           → Graceful handling of all failure modes
```

---

## 4. Parallel Work Strategy

```
Week 1-2:   Forge P0 (Eval Depth)             ||  Dashboard: prep work (deps, planning)
Week 3-4:   Forge P1 (Learning)               ||  Dashboard: prep work
Week 5-6:   Forge P2 (Resources)              ||  Dashboard P1 (Providers + Detail)
Week 7-8:   Forge P3 (Multi-Agent)            ||  Dashboard P1 (Monitoring)
Week 9-10:  Forge P4 (Automation)             ||  Dashboard P2 (Spawn, Tray, Polish)
Week 11-12: Integration + E2E tests           ||  Dashboard P2 (Auto-update)
```

---

## 5. Critical Path

```
bias_calibrator → cross_judge → bayesian_weights → historical_learning
                                                         ↓
                                              teacher.py (upgraded)
                                                         ↓
                                              phase_gates → agent_comms → task_decomposer
```

**Bayesian weights block historical learning. Historical learning blocks multi-agent.**

---

## 6. Quick Wins (Do These First in Each Tier)

| # | Task | Time | Impact |
|---|------|------|--------|
| 1 | `smart_cache.py` | 3h | 30% token savings immediately |
| 2 | `batch_eval.py` | 3h | 3-5× cheaper evals |
| 3 | `model_selector.py` | 4h | Routes simple tasks to cheap models |
| 4 | `bias_calibrator.py` | 4h | Foundation for all eval improvements |
| 5 | OpenAI provider (Dashboard) | 2h | Unlocks GPT-4 for chat |

---

**Status:** Build order defined. Follow this sequence.
