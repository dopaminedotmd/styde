# Testing Strategy

**Styde Forge v3.0 — Phase 0**
**Section:** 00_Overview

---

## 1. Purpose

Define how the forge itself is tested — not how agents are evaluated
(that's the Eval Pipeline), but how we verify that the forge infrastructure
works correctly.

---

## 2. Test Pyramid

```
            ┌──────┐
            │ E2E  │  1 test: complete loop iteration
            │      │
           ┌┴──────┴┐
           │Integration│  5 tests: component pairs
           │          │
          ┌┴──────────┴┐
          │   Unit      │  15+ tests: individual functions
          │             │
         ┌┴─────────────┴┐
         │   Validation  │  Lint, type check, schema validation
         └───────────────┘
```

---

## 3. Unit Tests

### State Management
- [ ] `load_state()` returns correct defaults on fresh forge
- [ ] `save_state()` writes valid YAML
- [ ] `save_state()` + `load_state()` roundtrip is lossless
- [ ] Corrupted state.yaml triggers recovery

### Blueprint Operations
- [ ] `validate_blueprint()` catches missing BLUEPRINT.md
- [ ] `validate_blueprint()` catches missing persona.md
- [ ] `validate_blueprint()` catches invalid config.yaml
- [ ] `validate_blueprint()` passes on valid blueprint
- [ ] `load_blueprint_context()` includes persona + skills

### Hardware Detection
- [ ] `detect_hardware()` returns valid dict on real hardware
- [ ] `classify_machine()` correctly identifies Machine-B (18 GB)
- [ ] `classify_machine()` correctly identifies Machine-A (34 GB)
- [ ] `get_adaptations()` returns correct VI config for Machine-B

### Checkpoint System
- [ ] `create_checkpoint()` writes all required files
- [ ] `verify_checkpoint()` detects corrupted checkpoint
- [ ] `verify_checkpoint()` passes on valid checkpoint
- [ ] `restore_checkpoint()` correctly restores state

### Atomic Writes
- [ ] `atomic_write()` doesn't leave temp files on success
- [ ] `atomic_write()` doesn't corrupt original on crash
- [ ] `atomic_write()` handles disk full gracefully

---

## 4. Integration Tests

### Spawn Pipeline
- [ ] Blueprint → context → delegate_task template is valid
- [ ] Benchmark task.md is correctly loaded
- [ ] Skills are properly concatenated into context

### Eval Pipeline
- [ ] Self-eval template includes all rubric dimensions
- [ ] Judge-eval template includes agent output
- [ ] Composite score calculation is correct

### Loop Integration
- [ ] Full loop for code-reviewer → code-review-basic (manual)
- [ ] Checkpoint before and after loop iteration
- [ ] State.yaml correctly increments loop_iterations

### Hardware Adaptation
- [ ] Detection → profile match → adaptation chain works end-to-end
- [ ] Adaptation values are within valid ranges

### Recovery
- [ ] Simulated crash → recovery restores last checkpoint
- [ ] Recovery log correctly records the event

---

## 5. End-to-End Test

**The One Test That Must Pass:**

```
1. Start with fresh forge
2. Create code-reviewer blueprint
3. Spawn agent against code-review-basic
4. Agent produces output
5. Self-eval runs
6. Judge-eval runs
7. Composite score calculated
8. Score ≥ 70 → agent saved
9. Checkpoint created
10. Simulate crash (delete state.yaml)
11. Recovery restores from checkpoint
12. state.yaml matches pre-crash state
13. Export forge → import on "different machine"
14. Imported forge has same blueprints, agents, eval results
15. Hardware profile adapted to new machine
```

---

## 6. Test Environment

### Primary (Machine-B)
- RTX 3080 10GB + RTX 3070 Ti 8GB
- 32 GB RAM
- Windows 11
- Hermes Agent v0.17.0
- DeepSeek-v4-pro (API)

### Secondary (Machine-A — when available)
- RTX 3090 24GB + RTX 3080 10GB
- 64 GB RAM
- Same software stack

---

## 7. Test Data

- **Valid blueprints**: All 6 blueprints in `blueprints/`
- **Valid benchmarks**: All 6 benchmarks in `eval/benchmarks/`
- **Corrupted state.yaml**: Truncated file, invalid YAML, missing keys
- **Corrupted checkpoint**: Missing files, wrong sizes
- **Edge case blueprints**: Empty persona, missing config, circular references

---

## 8. Test Automation (Phase 1)

```bash
# Run all tests
python -m pytest tests/ -v

# Unit tests only
python -m pytest tests/unit/ -v

# Integration tests (need Hermes running)
python -m pytest tests/integration/ -v --hermes

# E2E test (full loop, slow)
python tests/e2e/test_full_loop.py
```

---

## 9. Quality Gates for Forge Code

| Gate | Tool | Threshold |
|------|------|-----------|
| Lint | ruff | Zero errors |
| Type check | mypy | Zero errors |
| Test coverage | pytest-cov | ≥ 80% |
| Security scan | bandit | Zero high/critical |

---

**Status:** Defined. 15+ unit, 5 integration, 1 E2E test specified.
