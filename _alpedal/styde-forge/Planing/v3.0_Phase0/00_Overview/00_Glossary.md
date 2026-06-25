# Styde Forge v3.0 — Glossary

**"The Crucible"**
**Phase 0 — Reference**

Complete glossary of all terms in the Styde Forge ecosystem.
Use as reference when reading design documents and during Phase 1 implementation.

---

## A

**Agent**
A spawned instance of a blueprint. An agent is a specialized AI running in an isolated `delegate_task` call. Example: `agent-code-reviewer-20260625-123000`.

**Agent ID**
Unique identifier for a spawned agent. Format: `agent-<blueprint>-<YYYYMMDD>-<HHMMSS>`.

**Atomic Write**
A write that either completes fully or not at all. Uses temp-file → rename pattern to prevent corrupted files from USB disconnect or crash.

**Automatic Recovery**
Mechanism that detects on startup whether the previous session crashed and restores the latest valid checkpoint.

**Automatic Validation**
Layer 5 of the eval pipeline. Automated tests (static analysis, linting, coverage check) run against agent output.

**Automatic Version Increment**
Meta-layer component that automatically bumps a blueprint's version based on eval delta: Major (>0.15 + architecture change), Minor (>0.10), Patch (>0.01).

## B

**Bayesian Weight Optimization**
Layer 6 of the eval pipeline. Uses NUTS (Machine-A) or VI (Machine-B) to dynamically adjust rubric weights based on historical performance.

**Benchmark**
Standardized test for evaluating an agent. Each benchmark has a `task.md` (task) and `rubric.yaml` (scoring criteria). 6 benchmarks exist: code-review-basic, research-basic, automation-basic, documentation-basic, testing-basic, meta-basic.

**Bias Calibration**
Layer 4 of the eval pipeline. Periodic calibration of judges against known benchmarks to detect and correct systematic bias.

**Blueprint**
A template defining an agent type. Consists of `BLUEPRINT.md` (purpose/domain), `persona.md` (voice/behavior), `config.yaml` (model choice, hardware profile), `skills/` (domain-specific skills), and `versions/` (version history).

## C

**Caveman Ultra**
Maximum-efficiency operating mode. 70% fewer tokens. No markdown, no fluff, data only. Default: ON.

**Checkpoint**
An atomic snapshot of the entire forge state at a point in time. Contains `state.yaml`, all blueprints, agents, and eval results. Used for recovery and portability.

**Circuit Breaker**
Pattern that stops cascade failures. After 3-5 consecutive failures, halts the loop to prevent wasted API costs. States: closed → open → half_open → closed.

**Composite Score**
Weighted sum of self-eval and judge-eval. Formula: `self_eval.score * 0.3 + judge_eval.score * 0.5 + consensus_adjustment * 0.2`. Determines whether the agent passes the quality gate.

**Cross-Judge Consensus**
Layer 3 of the eval pipeline. Multiple independent judges (e.g. DeepSeek + Claude + Grok) evaluate the same agent output and results are compared to identify deviations.

**The Crucible**
Codename for Styde Forge v3.0. Refers to the melting pot where raw blueprints are refined into elite agents.

## D

**delegate_task**
Hermes Agent tool that spawns a subagent with specific context, goal, and tools.

**Domain**
Knowledge area a blueprint/agent specializes in. Six domains: Coding, Research, Automation, Documentation, Testing, Meta.

**Dual Averaging**
Adaptive step-size algorithm in the sampling stack. Used to dynamically adjust NUTS step-size.

## E

**Eval Pipeline**
Six-layer evaluation system: 1) Self-Eval, 2) LLM-as-Judge, 3) Cross-Judge Consensus, 4) Bias Calibration, 5) Automatic Validation, 6) Bayesian Weight Optimization.

## F

**FAISS**
Vector indexing library used by RAG. Stores embeddings in-memory for fast similarity search. Runs on RTX 3080.

**Forge**
The entire system: blueprints, spawn mechanism, eval pipeline, improvement loop, checkpoint system.

**Forge Loop**
The core cycle: Define → Spawn → Evaluate → Improve → Checkpoint.

## H

**Hardware Adaptation Layer**
Auto-detects GPU/RAM/CPU at startup and adapts sampling, model selection, and resource limits.

**Historical Learning System**
Central learning engine that analyzes all previous generations to extract patterns, skills, and anti-patterns.

**HMC (Hamiltonian Monte Carlo)**
MCMC sampling method using Hamiltonian dynamics. Used as verification sampler alongside NUTS.

**Hook**
Lightweight integration point (< 40 KB) that triggers an action on specific forge events (webhook, script, alert, throttle).

## I

**Import Strategy**
One-prompt process to import the entire forge on a new machine with automatic hardware adaptation.

## J

**Judge**
A separate LLM that independently evaluates agent output against a rubric. Not the same model the agent used. Always uses `deepseek-v4-pro`.

## K

**Knowledge Base**
Indexed, sourced knowledge within a domain. Stored in `01_KNOWLEDGE/<domain>/`. Includes `corpus.md`, `index.json`, and `sources/`.

## L

**LLM-as-Judge**
Primary evaluation method: an independent model assesses agent output against a defined rubric.

**Loop Iteration**
One complete cycle: Define → Spawn → Evaluate → Improve → Checkpoint.

## M

**Machine-A / Machine-B**
Machine profiles. A = strong (3090 24GB + 3080 10GB, 34GB VRAM). B = medium (3080 10GB + 3070 Ti 8GB, 18GB VRAM).

**Meta-Layer**
Orchestration layer: Model Selector, Historical Learning, Version Increment, Health Monitoring.

**Meta-Improver**
Blueprint for agents that improve the forge itself — analyzes metrics and proposes system improvements.

## N

**NUTS (No-U-Turn Sampler)**
Advanced HMC variant that automatically determines optimal trajectory length. Primary sampler for Machine-A.

## P

**Parent**
The main Styde Forge process that orchestrates everything: spawns subagents, runs eval, manages checkpoints. Runs on Hermes Agent.

**Persona**
An agent's voice, role, and approach. Defined in `persona.md` in each blueprint.

**Phase 0**
Design phase. All architecture, data models, and interfaces defined. No executable code. 54 documents.

**Phase 1**
First implementation phase. One working loop iteration with one blueprint and one benchmark.

**PrecisionForge**
Design philosophy: one logical home, atomicity first, hardware aware, full traceability.

## Q

**Quality Gate**
Quality threshold. Agents must score ≥80/100 to pass an eval.
≥85/100 on 3 consecutive evals → promoted to production.
70-84 iterates (max 3 attempts). <70 rejected to archive.

## R

**RAG (Retrieval-Augmented Generation)**
Retrieves relevant knowledge chunks using embeddings instead of dumping everything into context. Runs on RTX 3080. Reduces tokens by 67%.

**Resource Governor**
Monitors VRAM/RAM/disk and throttles when needed to prevent resource exhaustion.

**Rubric**
Scoring criteria for a benchmark. Defines dimensions, weights, and score ranges.

## S

**Sampling Stack**
Four sampling methods: NUTS, HMC, Dual Averaging, Variational Inference.

**Self-Evaluation**
Agent evaluates its own output before submission to judge. Provides self-awareness and feeds Historical Learning.

**Skill**
Modular, reusable capability. Stored as `SKILL.md`. Loaded into agent context at spawn.

**Skill Loading Mechanism**
Process that reads a blueprint's skills and injects them into the agent's `delegate_task` context. Only blueprint-specific skills (3-5), not all 85+ built-in.

**Subagent**
A spawned agent instance running a specific task in isolated context.

## T

**Teacher Agent**
Meta-cognitive layer that analyzes eval results, provides feedback, and extracts skills from successful agents.

**Tree Depth Optimization**
Dynamic adjustment of NUTS tree depth based on performance, hardware, and domain.

## U

**USB**
The physical medium where the entire forge is stored. 48 GB budget. Fully portable between machines.

**USB Directory Structure**
Exact folder layout: `00_MANIFEST.json` through `99_INDEXES/`. 12 top-level directories with strict inclusion/exclusion rules. Designed for self-documentation.

## V

**Variational Inference (VI)**
Fast approximate Bayesian inference. Primary sampler for Machine-B where VRAM is limited.

**Version**
Semantic versioning: MAJOR.MINOR.PATCH. Auto-determined by Automatic Version Increment. Every change generates a diff and changelog.

---

**Status:** Complete glossary. 60+ terms defined.
