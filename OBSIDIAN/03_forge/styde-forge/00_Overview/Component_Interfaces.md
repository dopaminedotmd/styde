# Component Interfaces

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Purpose

Define exactly how the major forge components communicate — inputs, outputs,
and data formats. This is the contract that Phase 1 implements against.

---

## 2. Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    PARENT HERMES                         │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │
│  │ Hardware     │   │ Meta-Layer   │   │ Eval       │  │
│  │ Adaptation   │   │              │   │ Pipeline   │  │
│  │              │   │ ┌──────────┐ │   │            │  │
│  │ detect()     │   │ │ Model    │ │   │ self_eval  │  │
│  │   → profile  │   │ │ Selector │ │   │ judge_eval │  │
│  └──────┬───────┘   │ └────┬─────┘ │   │ validate   │  │
│         │           │      │       │   └─────┬──────┘  │
│         │           │ ┌────┴─────┐ │         │         │
│         │           │ │Historical│ │         │         │
│         │           │ │Learning  │ │         │         │
│         │           │ └────┬─────┘ │         │         │
│         │           │      │       │         │         │
│         │           │ ┌────┴─────┐ │         │         │
│         │           │ │Version   │ │         │         │
│         │           │ │Increment │ │         │         │
│         │           │ └──────────┘ │         │         │
│         │           └──────┬───────┘         │         │
│         │                  │                 │         │
│         ▼                  ▼                 ▼         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              PERSISTENCE LAYER                    │  │
│  │  atomic_write()  checkpoint()  recover()         │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         │                               │
│                         ▼                               │
│                   ┌──────────┐                          │
│                   │   USB    │                          │
│                   └──────────┘                          │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Interface Definitions

### 3.1 Hardware Adaptation → Meta-Layer

```
INPUT:  (none — called at startup)
OUTPUT: hardware_profile.json

{
  "type": "A" | "B",
  "vram_gb": float,
  "ram_gb": float,
  "cpu_cores": int,
  "power_level": "high" | "medium",
  "adaptations": {
    "sampling_method": "NUTS" | "VI",
    "max_tree_depth": int,
    "bayesian_samples": int,
    "max_parallel_subagents": int,
    "preferred_models": [str, ...]
  }
}
```

### 3.2 Meta-Layer → Subagent Spawn

```
INPUT:  blueprint_name, benchmark_name (or task_string)
OUTPUT: delegate_task() call

delegate_task(
    goal: str,          # Task from benchmark or user
    context: str,       # Persona + blueprint + skills + history
    toolsets: [str]     # ["terminal", "file", "web"]
)
```

### 3.3 Subagent → Eval Pipeline

```
INPUT:  agent_output.md (written to agents/<id>/runs/<run>/output.md)
        rubric.yaml (loaded from eval/benchmarks/<name>/rubric.yaml)
OUTPUT: eval.yaml

{
  "run_id": str,
  "agent_id": str,
  "self_eval": {
    "score": int,         # 0-100
    "dimensions": {str: int},
    "notes": str
  },
  "judge_eval": {
    "model": str,
    "score": int,
    "dimensions": {str: int},
    "notes": str
  },
  "composite_score": int,
  "passed": bool
}
```

### 3.4 Eval Pipeline → Bayesian Weight Optimization

```
INPUT:  eval.yaml (current evaluation)
        eval/results/<blueprint>.yaml (historical evaluations)
OUTPUT: updated_weights

{
  "dimensions": {
    "correctness": 0.28,
    "robustness": 0.22,
    "code_quality": 0.19,
    "efficiency": 0.14,
    "innovation": 0.08,
    "documentation": 0.09
  },
  "method": "VI" | "NUTS",
  "samples": int,
  "converged": bool
}
```

### 3.5 Eval Pipeline → Historical Learning

```
INPUT:  eval.yaml (all evaluations)
        teacher feedback
        agent output patterns
OUTPUT: historical_knowledge.db

Tables:
  - model_performance(model, domain, score, timestamp)
  - successful_patterns(pattern_name, domain, success_rate, skill_ref)
  - anti_patterns(pattern_name, domain, frequency, lesson)
  - version_history(blueprint, old_version, new_version, delta, changes)
```

### 3.6 Eval Pipeline → Automatic Version Increment

```
INPUT:  eval.yaml (delta vs previous version)
        architecture_change: bool
OUTPUT: new_version: str

Rules:
  delta > 0.15 AND architecture_change → Major
  delta > 0.10 → Minor
  delta > 0.01 → Patch
  delta ≤ 0 → No bump
```

### 3.7 All Components → Persistence Layer

```
INPUT:  path: str, content: str | dict
OUTPUT: success: bool

Methods:
  atomic_write(path, content)     # Single file, atomic
  atomic_write_json(path, dict)   # JSON, atomic
  atomic_append(path, line)       # Append line to log
  transactional_save(dir, files)  # Multi-file, atomic

Guarantees:
  - Never partial writes
  - Temp file → rename pattern
  - fsync before rename
  - Crash-safe: old or new file exists, never corrupted
```

---

## 4. Data Flow Summary

```
Startup:
  HardwareAdapter.detect() → adaptations
  adaptations → MetaLayer.configure()

Loop Iteration:
  MetaLayer.load_blueprint(name) → spawn_context
  MetaLayer.spawn(spawn_context) → agent_output
  EvalPipeline.evaluate(agent_output, rubric) → eval_result
  BayesianOpt.update(eval_result) → new_weights
  HistoricalLearning.record(eval_result) → updated_db
  VersionIncrement.decide(eval_result) → new_version
  Persistence.atomic_write_all() → USB
```

---

**Status:** All interfaces defined. Ready for Phase 1 contract implementation.

---

## Related Documents

- `Master_Architecture_Overview.md` — High-level architecture
- `Core_Loop_Detail.md` — How interfaces are used in the loop
- `Data_Models.md` — Exact data formats for each interface
- `05_Meta_Layer/Dynamic_Model_Selector.md` — Model selection interface
- `03_Eval_Pipeline/LLM_as_Judge.md` — Judge evaluation interface
- `06_Persistence_Safety/Filesystem_Transactions.md` — Persistence interface
