# Data Models

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Purpose

Define exact schemas for all YAML and JSON data structures in the forge.
Every component reads and writes data in these formats.

---

## 2. Global State (`state.yaml`)

```yaml
forge_version: "3.0.0"
forge_codename: "The Crucible"
created: "2026-06-25T12:00:00Z"
last_checkpoint: "2026-06-25T12:00:00Z"
hardware_profile: "pontus-main"
caveman_ultra: true               # Max-efficiency mode ON by default
loop_iterations: 0
total_agents_spawned: 0
total_evaluations: 0

blueprints:
  - name: "code-reviewer"
    version: 1
    status: "draft"            # draft | testing | stable | deprecated
    domain: "coding"
    last_eval_score: null
    created: "2026-06-25T10:00:00Z"

agents:
  - name: "invoice-processor"
    blueprint: "invoice-processor"
    version: 3
    stage: "production"          # refinery | production | archive
    status: "deployed"           # pending_spawn | running | eval_pending | retrying | deployed | archived
    path: "StydeAgents/production/invoice-processor/"
    composite_score: 89
    evals_passed: 5
    spawned: "2026-06-25T12:30:00Z"

evaluations:
  - agent_id: "agent-code-reviewer-20260625-123000"
    blueprint: "code-reviewer"
    benchmark: "code-review-basic"
    run_id: "run-20260625-123500"
    composite_score: 83
    passed: true
    timestamp: "2026-06-25T12:45:00Z"

improvements:
  - blueprint: "code-reviewer"
    from_version: 1
    to_version: 2
    eval_delta: 0.12
    changes: "Added edge case handling for empty input"
    timestamp: "2026-06-25T13:00:00Z"
```

---

## 3. Master Manifest (`00_MANIFEST.json`)

```json
{
  "forge": {
    "version": "3.0.0",
    "codename": "The Crucible",
    "created": "2026-06-25T12:00:00Z",
    "last_updated": "2026-06-25T12:00:00Z",
    "sha256": "abc123..."
  },
  "statistics": {
    "total_agents": 0,
    "total_evaluations": 0,
    "total_loop_iterations": 0,
    "storage_used_gb": 0.0,
    "storage_limit_gb": 48.0
  },
  "best_per_domain": {
    "coding": {"agent_id": null, "score": null},
    "research": {"agent_id": null, "score": null},
    "automation": {"agent_id": null, "score": null},
    "documentation": {"agent_id": null, "score": null},
    "testing": {"agent_id": null, "score": null},
    "meta": {"agent_id": null, "score": null}
  },
  "provenance": {
    "generation_chain": ["v3.0_hermes"],
    "hardware_profiles_used": ["pontus-main"]
  }
}
```

---

## 4. Agent Metadata (`AGENT.md`)

```markdown
# Agent: agent-code-reviewer-20260625-123000

**Blueprint:** code-reviewer
**Blueprint Version:** 1
**Domain:** coding
**Benchmark:** code-review-basic
**Model:** deepseek-v4-pro
**Status:** completed
**Spawned:** 2026-06-25T12:30:00Z
**Completed:** 2026-06-25T12:35:00Z

## Runs
- run-20260625-123500: code-review-basic — Score: 83 — PASSED

## Lineage
- Parent blueprint: code-reviewer v1
- Model: deepseek-v4-pro
- Spawned by: Styde Forge v3.0
```

---

## 5. Eval Result (`eval.yaml`)

```yaml
run_id: "run-20260625-123500"
agent_id: "agent-code-reviewer-20260625-123000"
blueprint: "code-reviewer"
benchmark: "code-review-basic"
timestamp: "2026-06-25T12:45:00Z"

self_eval:
  score: 85
  dimensions:
    correctness: 90
    robustness: 75
    code_quality: 88
    efficiency: 82
    innovation: 80
    documentation: 95
  notes: "Hittade alla kritiska buggar. Missade edge case med null input."

judge_eval:
  model: "deepseek-v4-pro"
  score: 83
  dimensions:
    correctness: 90
    robustness: 75
    code_quality: 85
    efficiency: 80
    innovation: 82
    documentation: 88
  notes: "Bra analys men missade minnesläcka i process_pool()"

composite_score: 83
self_judge_agreement: 0.94    # Correlation between self-eval and judge
passed: true
min_pass_score: 70
```

---

## 6. Blueprint Config (`config.yaml`)

```yaml
blueprint:
  name: "code-reviewer"
  version: 1
  description: "Granskar kod för buggar, säkerhetshål och stilbrott"
  domain: "coding"

hardware_profiles:
  pontus-main:
    model: "deepseek-v4-flash"
    provider: "deepseek"
    eval_model: "deepseek-v4-pro"
    max_tokens: 8192
    temperature: 0.3
  pontus-light:
    model: "deepseek-v4-flash"
    provider: "deepseek"
    eval_model: "deepseek-v4-pro"
    max_tokens: 4096
    temperature: 0.3
  pontus-beast:
    model: "deepseek-v4-flash"
    provider: "deepseek"
    eval_model: "deepseek-v4-pro"
    max_tokens: 16384
    temperature: 0.3

agent:
  max_iterations: 10
  timeout_seconds: 300
  retry_on_failure: true
  toolsets: ["terminal", "file", "web"]

eval:
  benchmarks:
    - "code-review-basic"
    - "code-review-security"
  judge_model: "deepseek-v4-pro"
  min_pass_score: 0.70
```

---

## 7. Hardware Profile (`hardware_profile.json`)

```json
{
  "hardware": {
    "type": "B",
    "vram_gb": 18.4,
    "ram_gb": 31.9,
    "cpu_cores": 8,
    "power_level": "medium",
    "detected_at": "2026-06-25T12:00:00Z",
    "platform": "Windows"
  },
  "adaptations": {
    "sampling_method": "VI",
    "max_tree_depth": 8,
    "bayesian_samples": 1400,
    "checkpoint_interval_min": 25,
    "max_parallel_subagents": 1,
    "preferred_models": ["Qwen2.5-14B", "DeepSeek-Coder-14B", "Hermes-4-14B"],
    "vi_iterations": 400
  }
}
```

---

## 8. Log Entry (JSON-Lines)

```json
{
  "timestamp": "2026-06-25T12:30:00Z",
  "level": "INFO",
  "component": "forge.spawn",
  "operation": "agent_spawn",
  "blueprint": "code-reviewer",
  "agent_id": "agent-code-reviewer-20260625-123000",
  "model": "deepseek-v4-pro",
  "duration_ms": 2340,
  "status": "success"
}
```

---

**Status:** Defined. All schemas locked for Phase 1 implementation.

---

## Related Documents

- `USB_Directory_Structure.md` — Where each data model lives on disk
- `Config_Reference.md` — All configurable parameters and their types
- `Component_Interfaces.md` — How data flows between components
- `Core_Loop_Detail.md` — When each schema is read/written in the loop
- `06_Persistence_Safety/Filesystem_Transactions.md` — How data is safely written
