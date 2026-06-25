# Benchmark Catalog

**Styde Forge v3.0 — Phase 0**
**Section:** 03_Eval_Pipeline

---

## 1. Overview

Six standardized benchmarks — one per domain. Each benchmark has a task
definition and a scoring rubric. Used to evaluate agent output consistently
across versions.

---

## 2. Benchmark Summary

| # | Benchmark | Domain | Difficulty | Dimensions |
|---|-----------|--------|------------|------------|
| 1 | `code-review-basic` | Coding | Medium | Correctness, Completeness, Clarity, False Positives |
| 2 | `research-basic` | Research | Medium | Source Quality, Synthesis Depth, Structure, Confidence |
| 3 | `automation-basic` | Automation | Medium | Completeness, Error Handling, Structure, Practicality |
| 4 | `documentation-basic` | Documentation | Medium | Clarity, Completeness, Correctness, Structure |
| 5 | `testing-basic` | Testing | Medium | Coverage, Correctness, Edge Cases, Runnability |
| 6 | `meta-basic` | Meta | Hard | Insight, Solution Concreteness, Impact, Testability |

---

## 3. Detailed Benchmark Specifications

### 3.1 code-review-basic

| Attribute | Value |
|-----------|-------|
| **Domain** | Coding & Software Engineering |
| **Task** | Review Python code with 12 known issues (critical, high, medium, low) |
| **Known issues** | 4 critical (SQL injection, hardcoded creds, command injection, path traversal), 3 high, 3 medium, 2 low |
| **Min pass** | 70/100 |
| **World-class** | 85/100 |

### 3.2 research-basic

| Attribute | Value |
|-----------|-------|
| **Domain** | Research & Knowledge Management |
| **Task** | Research "WebAssembly outside the browser (WASI)" |
| **Requirements** | 5+ credible sources, confidence assessment, 2+ knowledge gaps |
| **Min pass** | 70/100 |

### 3.3 automation-basic

| Attribute | Value |
|-----------|-------|
| **Domain** | Automation & Orchestration |
| **Task** | Design CSV → JSON automation workflow |
| **Requirements** | 5 steps with commands, 3+ error scenarios, clear dependencies |
| **Min pass** | 70/100 |

### 3.4 documentation-basic

| Attribute | Value |
|-----------|-------|
| **Domain** | Documentation & Communication |
| **Task** | Document `forge.py` CLI for newcomers |
| **Requirements** | 5 sections, working examples, troubleshooting, prerequisites |
| **Min pass** | 70/100 |

### 3.5 testing-basic

| Attribute | Value |
|-----------|-------|
| **Domain** | Testing & Evaluation |
| **Task** | Write test suite for `parse_config()` function |
| **Requirements** | 6 test cases, edge case reasoning, runnable tests |
| **Min pass** | 70/100 |

### 3.6 meta-basic

| Attribute | Value |
|-----------|-------|
| **Domain** | Meta-Self-Improvement |
| **Task** | Analyze forge design and propose one improvement |
| **Requirements** | Specific weakness, concrete fix, quantified impact, test design |
| **Min pass** | 70/100 |

---

## 4. Scoring Dimensions (All Benchmarks)

| Dimension | Typical Weight | Description |
|-----------|---------------|-------------|
| Correctness / Completeness | 25-35% | Does the output meet functional requirements? |
| Quality / Depth | 20-30% | How thorough and insightful is the analysis? |
| Structure / Clarity | 15-20% | Is the output well-organized and readable? |
| Robustness / Edge Cases | 15-20% | Are edge cases and error conditions addressed? |
| Practicality / Runnability | 10-20% | Can the output be immediately used/executed? |

---

## 5. Benchmark Lifecycle

```
active → calibrating → deprecated
   │          │            │
   │          │            └── No longer used
   │          └── Being recalibrated against new standards
   └── Currently in use for evaluations
```

---

**Status:** All 6 benchmarks defined with tasks and rubrics.
