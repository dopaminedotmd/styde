# Blueprint Catalog

**Styde Forge v3.0 — Phase 0**
**Section:** 01_Vision

---

## 1. Overview

Six domain-specific agent blueprints covering the core competency areas.
Each blueprint defines an agent's purpose, persona, configuration, and
evaluation criteria.

---

## 2. Blueprint Summary

| # | Blueprint | Domain | Purpose | Key Skills |
|---|-----------|--------|---------|------------|
| 1 | `code-reviewer` | Coding & Software Engineering | Code review for bugs, security, style | Static analysis, security patterns, PEP 8 |
| 2 | `research-synthesizer` | Research & Knowledge Management | Multi-source research synthesis | Web search, source evaluation, synthesis |
| 3 | `automation-orchestrator` | Automation & Orchestration | Workflow design and automation | Scripting, chaining, error handling |
| 4 | `documentation-writer` | Documentation & Communication | Technical documentation | Clarity, structure, audience awareness |
| 5 | `testing-evaluator` | Testing & Evaluation | Test design and execution | Test coverage, edge cases, assertions |
| 6 | `meta-improver` | Meta-Self-Improvement | Forge self-improvement | Analysis, metrics, proposal design |

---

## 3. Detailed Blueprint Specifications

### 3.1 code-reviewer

| Attribute | Value |
|-----------|-------|
| **Domain** | Coding & Software Engineering |
| **Input** | Source code (diff, file, or PR) |
| **Output** | Structured review with severity-ranked findings |
| **Quality threshold** | ≥ 80/100, ≥ 85% bug detection rate |
| **Model** | `deepseek-v4-flash` (agent) / `deepseek-v4-pro` (eval) |
| **Benchmarks** | code-review-basic |

### 3.2 research-synthesizer

| Attribute | Value |
|-----------|-------|
| **Domain** | Research & Knowledge Management |
| **Input** | Research topic or question |
| **Output** | Structured synthesis with sources, confidence levels, gaps |
| **Quality threshold** | ≥ 80/100, ≥ 5 credible sources |
| **Model** | `deepseek-v4-flash` (agent) / `deepseek-v4-pro` (eval) |
| **Benchmarks** | research-basic |

### 3.3 automation-orchestrator

| Attribute | Value |
|-----------|-------|
| **Domain** | Automation & Orchestration |
| **Input** | Workflow description |
| **Output** | Step-by-step automation plan with error handling |
| **Quality threshold** | ≥ 80/100, all steps implementable |
| **Model** | `deepseek-v4-flash` (agent) / `deepseek-v4-pro` (eval) |
| **Benchmarks** | automation-basic |

### 3.4 documentation-writer

| Attribute | Value |
|-----------|-------|
| **Domain** | Documentation & Communication |
| **Input** | Technical topic or system |
| **Output** | Clear, structured documentation for target audience |
| **Quality threshold** | ≥ 80/100, accessible to newcomers |
| **Model** | `deepseek-v4-flash` (agent) / `deepseek-v4-pro` (eval) |
| **Benchmarks** | documentation-basic |

### 3.5 testing-evaluator

| Attribute | Value |
|-----------|-------|
| **Domain** | Testing & Evaluation |
| **Input** | Code to test + test requirements |
| **Output** | Complete test suite with edge cases |
| **Quality threshold** | ≥ 80/100, ≥ 85% edge case coverage |
| **Model** | `deepseek-v4-flash` (agent) / `deepseek-v4-pro` (eval) |
| **Benchmarks** | testing-basic |

### 3.6 meta-improver

| Attribute | Value |
|-----------|-------|
| **Domain** | Meta-Self-Improvement |
| **Input** | Forge metrics and design documents |
| **Output** | Concrete improvement proposal with quantified impact |
| **Quality threshold** | ≥ 80/100, proposal is specific and testable |
| **Model** | `deepseek-v4-flash` (agent) / `deepseek-v4-pro` (eval) |
| **Benchmarks** | meta-basic |

---

## 4. Blueprint Lifecycle

```
draft → testing → stable → deprecated
   │        │         │
   │        │         └── No longer used (archived)
   │        └── Actively used, proven reliable
   └── Initial definition, not yet validated
```

---

**Status:** All 6 blueprints defined. Ready for Phase 1 spawn.
