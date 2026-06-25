---
title: "_alpedal — Alpedal's Domain"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# _alpedal — Alpedal's Domain

> Auditor. Blueprint Designer. Systems Thinker.
> This is the lab where raw ideas become precision agents.
> Styde Forge — the portable evolutionary agent refinery — is the heart.

---

## What This Is

Alpedal's **personal workspace** within styde.ai — an isolated environment for:

| Activity | Tool |
|----------|------|
| **Agent Design** | Blueprint creation in Forge format (`persona.md` + `blueprint.yaml` + `tools.yaml`) |
| **Agent Refinement** | [[styde-forge/Planing/PHASE0_COMPLETE\|Styde Forge v3.0]] — the portable evolutionary agent refinery |
| **Agent Monitoring** | Styde Forge Dashboard — Tauri desktop app (Mission Control) |
| **Customer Audits** | Mapping IT flows, systems, and automation potential |
| **Pattern Recognition** | Discovering recurring automation patterns no one else sees |
| **Experimentation** | Free exploration without affecting the main system |

---

## What This Is NOT

- ❌ **Not the plan** — [[obsidian/01_plan/MASTER_PLAN\|MASTER_PLAN.md]] is the single source of truth
- ❌ **Not production code** — everything here is experimental until William approves
- ❌ **Not customer deliverables** — customer agents are built in `agent-blueprints/`, not here
- ❌ **Not shared space** — this is Alpedal's. William's space is `_william/`

---

## Styde Forge — Overview

Two integrated projects, one ecosystem.

```
┌──────────────────────────┐     ┌──────────────────────────┐
│   StydeForge Dashboard   │     │   Hermes Agent           │
│   (Tauri desktop app)    │────▶│   (CLI + Runtime)        │
│                          │     │                          │
│  • Monitor agents        │     │  • Forge core loop       │
│  • Control pipeline      │     │  • Agent spawning        │
│  • Chat with AI          │     │  • 6-layer eval pipeline │
│  • View benchmarks       │     │  • Skill loading         │
│  • System health         │     │  • Cron jobs             │
└──────────────────────────┘     └──────────────────────────┘
         │                                │
         │  hermes process list           │
         │  hermes forge start/stop       │
         │  hermes delegate_task          │
         └────────────────────────────────┘
```

The Dashboard is the face. Hermes/Forge is the engine.

---

## 1. Styde Forge — The Refinery

> *"Where raw agents are forged into elite through precision and iterative purity."*

**Status:** Phase 0 COMPLETE ✅ — 53 design documents, 14 sections, 8 architecture decisions, 9 risks mitigated.

**Core Loop:**
```
DEFINE → SPAWN → EVALUATE → IMPROVE → CHECKPOINT
    ↑_________________________________________|
```

| Step | Description |
|------|-------------|
| **DEFINE** | Blueprint loaded, skills isolated per agent (3-5, not 85). Caveman Ultra activated. |
| **SPAWN** | Agent launched via `delegate_task()`. Dual-model: deepseek-v4-flash (agent runs) + deepseek-v4-pro (eval/teacher). |
| **EVALUATE** | 6-layer pipeline: Self-Eval → LLM-as-Judge → Cross-Judge Consensus → Bias Calibration → Auto-Validation → Bayesian Weight Optimization |
| **IMPROVE** | Teacher Agent analyzes → diagnoses → extracts skills → coaches the agent |
| **CHECKPOINT** | Atomic write (temp → rename). **Quality gate ≥ 80/100.** Anything below is discarded. |

### Architecture — 14 Sections

| # | Section | Docs | Core |
|---|---------|------|------|
| 00 | Overview | 12 | Architecture, data models, core loop, interfaces, state machines, config, testing |
| 01 | Vision | 2 | Vision & goals, blueprint catalog (6 domains) |
| 02 | Hardware | 2 | Auto-detect Machine-A vs B, resource governor, GPU adaptation |
| 03 | Eval Pipeline | 7 | 6-layer eval: self → judge → consensus → bias → validation → Bayesian |
| 04 | Sampling Stack | 5 | NUTS, Hamiltonian MC, Variational Inference, Dual Averaging, Tree Depth |
| 05 | Meta-Layer | 4 | Dynamic model selector, historical learning, auto-version, self-monitoring |
| 06 | Persistence & Safety | 4 | Atomic writes, checkpoints, recovery, risk register |
| 07 | Multi-Agent | 2 | Teacher-student pattern, agent isolation, knowledge sharing |
| 08 | Import/Export | 2 | Single-prompt import, sync strategy |
| 09 | Risk & Maintenance | 1 | Pruning, cleanup |
| 10 | Operations | 7 | Skill loading, blueprint validation, JSON-lines logging, Caveman Ultra, costs, API keys, human oversight |
| 11 | Knowledge Management | 1 | Knowledge lifecycle |
| 12 | Teacher Agent | 1 | Feedback loop, skill extraction, coaching |
| 13 | Hooks & Events | 1 | 17 events, 4 hook types |
| 14 | RAG Retrieval | 1 | Retrieval-Augmented Generation |

Full architecture: [[styde-forge/Planing/00_Overview/Master_Architecture_Overview]]

### Design Decisions (8 Key)

| # | Decision | Why |
|---|----------|-----|
| D001 | Meta-layer over Docker swarm | 18 GB VRAM on Machine-B. One model at a time. |
| D002 | Quality gate ≥ 80/100 | Quality over quantity. Mediocre agents waste USB space. |
| D003 | VI as default on Machine-B | Speed over precision. NUTS for Machine-A only. |
| D004 | JSON-lines logging | Machine-readable, append-safe, no DB dependency. |
| D005 | YAML state (not database) | Human-readable, diffable, zero dependencies. |
| D006 | Atomic writes for everything | USB disconnect is risk #1. Temp-file + rename. |
| D007 | Sequential loop (v3.0) | Focused teacher attention. Parallel in v3.1+. |
| D008 | Per-blueprint skill loading | Cleaner context = sharper agents. 3-5 skills, not 85. |

---

## 2. Styde Forge Dashboard — Mission Control

**Status:** Phase 0 COMPLETE ✅ — 36 design documents, 10 sections.

A **Tauri-based desktop application** (`StydeForge.exe`) serving as the command center for the entire ecosystem.

| Section | Contents |
|---------|----------|
| **00 Overview** | Vision, app architecture, index |
| **01 Application Shell** | Window management, lifecycle, process control, system tray |
| **02 UI/UX** | Layout, design system, component library, onboarding flow |
| **03 Agent Monitor** | Live tracking, detail view, spawn new agents |
| **04 Benchmark Panel** | Performance, quality, visualization |
| **05 Chat Interface** | Full AI chat with tools (read/write files, terminal, web, skills) |
| **06 Model Provider System** | Multi-model: DeepSeek, OpenAI, Anthropic, custom REST, local Ollama |
| **07 System Control** | Start/pause/stop Forge pipeline with one click, config, health |
| **08 Data Layer** | Hermes CLI bridge, polling, local storage, real-time updates |
| **09 Technical Stack** | Tauri v2, Rust + React, build pipeline, auto-update |
| **10 Phase Transition** | Phase 0 → Phase 1 roadmap |

---

## Top 20 Agents — World-Class Priority Queue

20 agents designed for the Forge loop. Ranked by business impact.

### Tier 1 — Revenue Generators (Build First)

| # | Agent | Customer Value |
|---|-------|----------------|
| 1 | **Consultant Auditor** | Crawls site → classifies digital maturity → audit report. THE SALES HOOK. |
| 2 | **Invoice Processor** | PDF → extracts line items, VAT, dates → JSON. 5-15h/week saved. |
| 3 | **Customer Service Triage** | Email/chat → classify → draft or route. Response time: hours → seconds. |
| 4 | **Meeting Summarizer** | Transcript → decisions, actions, owners, deadlines. Zero post-meeting admin. |
| 5 | **Email Drafter** | Context + company knowledge → professional email. 2-5h/week saved. |

### Tier 2 — Efficiency Multipliers

| # | Agent | Customer Value |
|---|-------|----------------|
| 6 | **Document Classifier** | Classifies document type → routes. Foundation for all document workflows. |
| 7 | **Contract Reviewer** | Contract → key clauses, risks → flagged. Legal review time -70%. |
| 8 | **Report Writer** | Data + template → polished business report. 4h → 15 min. |
| 9 | **Data Cleaner** | Messy spreadsheet → duplicates, errors, fixes → cleans. |
| 10 | **Calendar Assistant** | Natural language → find slots, book, invite. 1-2h/week saved. |

### Tier 3 — Capability Builders

| # | Agent | Customer Value |
|---|-------|----------------|
| 11 | **Code Reviewer** | Code → bugs, security, style → suggestions. |
| 12 | **SQL Query Generator** | Natural language + schema → correct SQL. Non-tech staff query databases. |
| 13 | **Translator (SV↔EN)** | Business docs with correct tone, terminology, legal precision. |
| 14 | **Social Media Writer** | Company news → platform-optimized posts. |
| 15 | **Onboarding Guide** | Role + handbook → personalized onboarding plan. |

### Tier 4 — Specialized Agents

| # | Agent | Customer Value |
|---|-------|----------------|
| 16 | **GDPR Compliance Checker** | Privacy policy → GDPR gaps → article references. Audit: weeks → hours. |
| 17 | **Inventory Forecaster** | Sales history → stock predictions 30/60/90 days. |
| 18 | **Recruitment Screener** | CVs + job description → ranked candidates → screening questions. 50 CVs → top 5. |
| 19 | **Competitor Monitor** | Competitor surveillance → changes detected → weekly brief. |
| 20 | **Meta-Improver** | Analyzes Forge eval results → systemic improvements. Makes ALL other agents better. |

### Build Timeline

```
Week 1-2:   #1 Consultant Auditor + #5 Email Drafter
Week 3-4:   #2 Invoice Processor + #3 Customer Service Triage
Week 5-6:   #6 Document Classifier + #10 Calendar Assistant
Week 7-8:   #4 Meeting Summarizer + #8 Report Writer + #7 Contract Reviewer
Week 9-10:  #16 GDPR Checker + #14 Social Media Writer
Week 11-12: #11 Code Reviewer + #20 Meta-Improver (starts the self-improvement loop)
Week 13+:   Remaining agents in priority order
```

---

## Phase 1 Roadmap — 50 Features

For when the core loop works. Priority tiers:

| Tier | Criteria | When |
|------|----------|------|
| **P0 — Foundation** | Core loop must work first | Week 1-2 |
| **P1 — High Impact** | Big gains, implementable in days | Week 3-6 |
| **P2 — Scaling** | Needed for 100+ agents | Week 7-10 |
| **P3 — Excellence** | Polish, UX, long-term | Phase 2+ |

### P0 — Foundation
1. Working Core Loop (end-to-end)
2. Blueprint → Spawn → Eval pipeline
3. Atomic Checkpoint & Recovery
4. Hardware Detection & Adaptation
5. Caveman Ultra mode

### P1 — High Impact (Selection)

**Multi-Agent:** Phase Gates, Task Decomposition Engine, Agent-to-Agent Communication, Hierarchical Multi-Agent, Agent Memory Sharing, Conflict Resolution, Specialized Agent Roles (7).

**Resource Management:** Dynamic VRAM/RAM Allocation, GPU Load Balancing (3080 + 3070 Ti), Intelligent Queue System.

**Automation:** Automatic Benchmark Generation, Automatic Prompt Optimization, Curriculum Learning, Evolutionary Algorithms for Blueprints, Meta-Learning.

**RAG & Memory:** Knowledge Graph, Semantic Search over History, Memory Consolidation, Cross-Project Learning.

### P2 — Scaling (Selection)
Anomaly Detection, Smart Caching, Batch Processing, Token Budgeting, Cost Forecasting, Versioned Vector Database, Immutable Event Log, Multi-Project Support.

### P3 — Excellence (Selection)
Web UI / Command Center, Visual Loop Debugger, Blueprint Visual Editor, Plugin System, Forge Evolution Engine, Self-Improving Forge, Agent DNA / Genetic Representation.

Full roadmap: [[styde-forge/Planing/v1.0_Phase1/PHASE1_ROADMAP]]

---

## Agent Lifecycle (StydeAgents)

```
data/ ──→ refinery/ ──→ production/ ──→ archive/
 ↑                        │
 └──────── feedback ──────┘
```

| Directory | Purpose | Status |
|-----------|---------|--------|
| `data/` | Raw data — benchmarks, knowledge, templates | Static |
| `refinery/` | Agents in the Forge loop (spawn → eval → improve) | In progress |
| `production/` | World-class agents (≥ 85/100, 3 consecutive evals) | Ready |
| `archive/` | Retired/rejected agents | Lessons preserved |

---

## Alpedal's Role

| Responsibility | Priority | When |
|----------------|----------|------|
| Design agent blueprints (Forge format) | P0 | Sprint 01 → |
| Conduct customer audits | P0 | When first audit is booked |
| Own Styde Forge — roadmap, design, implementation | P0 | Ongoing |
| Test Consultant Agent output (quality review) | P1 | Sprint 02 |
| Write patterns for AGENT_PATTERNS.md | P1 | After first agents run |
| Design eval rubrics for agent quality | P2 | Phase 3 |

### Growth Path

| Month | Level |
|-------|-------|
| **1-2** | Blueprint designer + audit partner (no code) |
| **3-4** | Start coding: simple Python scripts for audit automation |
| **5-6** | Build Forge eval scripts (Python) on shared server |
| **7+** | Independent builder — implement Forge core loop + dashboard |

---

## Workflow

1. Read [[obsidian/_RULES]] — format, tags, rules
2. Read [[obsidian/01_plan/SPRINT_CURRENT]] — active sprint
3. Read [[obsidian/01_plan/MASTER_PLAN]] — the single plan
4. Design blueprints here in `_alpedal/`
5. When a blueprint is mature → export to `agent-blueprints/`
6. Log all changes → [[obsidian/05_ops/logs/_INDEX\|daily log]]

---

## Links

| Resource | Path |
|----------|------|
| Master Plan | [[obsidian/01_plan/MASTER_PLAN]] |
| Current Sprint | [[obsidian/01_plan/SPRINT_CURRENT]] |
| Sprint Log (dopamine) | [[obsidian/01_plan/SPRINT_LOG]] |
| Bot Rules | [[obsidian/_RULES]] |
| Forge Architecture | [[styde-forge/Planing/00_Overview/Master_Architecture_Overview]] |
| Forge Phase 0 Index | [[styde-forge/Planing/00_Overview/PHASE0_INDEX]] |
| Forge Phase 1 Roadmap | [[styde-forge/Planing/v1.0_Phase1/PHASE1_ROADMAP]] |
| Top 20 Agents | [[styde-forge/Planing/Top_20_Agents]] |
| Blueprint Catalog | [[styde-forge/Planing/01_Vision/Blueprint_Catalog]] |
| Dashboard Index | [[styde-forge/Planing/Dashboard_Phase0/00_Overview/DASHBOARD_INDEX]] |
| Onboarding Process | [[obsidian/05_ops/ONBOARDING]] |
| Offer Template | [[obsidian/04_CLIENTS/TEMPLATES/OFFERT_TEMPLATE]] |
| Audit Template | [[obsidian/04_CLIENTS/TEMPLATES/AUDIT_TEMPLATE]] |

---

## Comments

- 2026-06-25 | hermes: README upgraded to full domain documentation. Includes Forge + Dashboard, Top 20 agents, Phase 1 roadmap (50 features), agent lifecycle, and workflow. Translated to English.
