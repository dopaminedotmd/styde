---
title: "AUDIT & INTEGRATION: Styde Forge v3.0 → styde.ai"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/DRAFT, author/HERMES, type/REPORT]
status: draft
---

# Audit & Integration: Styde Forge v3.0 → styde.ai

> Alpedal's agent refinery engine. Audit of what exists, how it fits in,
> and plan for integration with styde.ai.
> 51 design documents, 0 lines of code. Phase 0 — locked and complete.

---

## Part 1: Audit of Styde Forge v3.0

### 1.1 What It Is

Styde Forge is a **portable, evolutionary agent refinery** designed to
run on USB (48 GB). It spawns agents from blueprints, evaluates them with
a 6-layer eval pipeline, improves them via a Teacher Agent, and saves
checkpoints atomically.

**Core loop:** `DEFINE → SPAWN → EVALUATE → IMPROVE → CHECKPOINT`

### 1.2 Component Map

| # | Component | Doc count | Status | Maturity |
|---|-----------|-----------|--------|--------|
| 00 | Overview (architecture, data, interfaces) | 12 | Complete | High — all schemas, interfaces, state machines defined |
| 01 | Vision & Blueprints | 2 | Complete | 6 blueprints, 6 domains specified |
| 02 | Hardware (adaptation, governor) | 2 | Complete | Auto-detect Machine-A vs B, resource limits |
| 03 | Eval Pipeline (6 layers) | 7 | Complete | Self-eval → Judge → Consensus → Bias → Validation → Bayesian |
| 04 | Sampling Stack (NUTS, HMC, VI) | 5 | Complete | 4 methods, hardware-adapted |
| 05 | Meta-Layer (model, learning, version) | 4 | Complete | Dynamic model selector, historical learning, auto-version |
| 06 | Persistence & Safety | 4 | Complete | Atomic writes, checkpoints, recovery, risk register |
| 07 | Multi-Agent | 2 | Complete | Teacher-student pattern, agent isolation, knowledge sharing |
| 08 | Import/Export | 2 | Complete | Single-prompt import, sync strategy |
| 09 | Maintenance | 1 | Complete | Pruning, cleanup |
| 10 | Operations (skills, logging, costs) | 7 | Complete | Skill loading, blueprint validation, JSON-lines logging, Caveman Ultra |
| 11 | Knowledge Management | 1 | Complete | Knowledge lifecycle |
| 12 | Teacher Agent | 1 | Complete | Feedback loop, skill extraction, coaching |
| 13 | Hooks & Events | (in index, missing as separate file) | Missing | — |

### 1.3 Technical Highlights

**Strengths:**

| Strength | Detail |
|--------|--------|
| **Fully specified loop** | Core_Loop_Detail.md: exact steps, tool calls, prompts, error handling |
| **15 design decisions logged** | DECISIONS.md with alternatives + rationale |
| **Hardware-aware** | Auto-detect VRAM/RAM → adapts sampling, workers, models |
| **Dual-model strategy** | Flash (80% of calls, $0.001) + Pro (20%, eval $0.001) |
| **Caveman Ultra default** | 70% fewer tokens → 2× faster, 3× cheaper |
| **Data models ready** | 8 YAML/JSON schemas specified |
| **Component interfaces** | All component inputs/outputs defined as contracts |
| **USB structure specified** | 48 GB budget, 250-350 agents, 14 directories |

**Weaknesses / Risks:**

| Risk | Severity |
|------|-------------------|
| **0 lines of code.** The entire system is design. Phase 0 → Phase 1 requires 6 weeks of implementation. | High |
| **USB-based → single point of failure.** If the USB is lost, everything is gone (mitigated by checkpoint + import, but still). | Medium |
| **DeepSeek dependency.** The entire eval pipeline is built around deepseek-v4-pro. If the API changes/is deprioritized → system breaks. | Medium |
| **Machine A/B is Alpedal's specific hardware.** Not William's GTX 980 Ti (4GB). Portability between these machines, yes — but not to arbitrary hardware. | Low |
| **Hooks/Events missing.** The index lists it but the file hasn't been created. | Low |
| **No dashboard / UI.** Explicitly excluded in non-goals. This is a CLI/USB system. | Low (intentional) |

### 1.4 Rating

| Dimension | Rating (1-10) |
|-----------|---------------|
| Design quality | 9 — exceptionally detailed, every decision motivated |
| Completeness | 8 — 51 of 53 documents ready (hooks/events missing) |
| Feasibility | 6 — 6 weeks Phase 1, many dependencies |
| Code | 1 — only Python pseudocode, no executable code |
| Relevance for styde.ai | 5 — conceptually relevant, but parallel system |

**Total: 5.8/10** — Masterful design, zero execution.

---

## Part 2: Relevance for styde.ai

### 2.1 What Styde Forge Is NOT

Styde Forge is NOT:
- A customer dashboard
- An admin panel for William
- A system for deploying agents to customers
- An API gateway
- A replacement for styde.ai's Agent Wardrobe

Styde Forge IS:
- Alpedal's personal agent refinery
- A USB-based lab for experimenting with agent design
- An engine for iteratively improving agents through evolutionary loops

### 2.2 Overlap and Conflicts

| Area | styde.ai | Styde Forge | Conflict? |
|--------|----------|-------------|-----------|
| Agent blueprints | `agents/templates/` + Agent Wardrobe | `blueprints/` with persona.md + BLUEPRINT.md | **Overlap** — two blueprint systems |
| Agent evaluation | Feedback loop (BUILD_PHASE_2 §2) | 6-layer eval pipeline | **Complementary** — Forge is deeper |
| Model selection | Not specified | Dynamic Model Selector | **Complementary** — Forge is more advanced |
| Versioning | `agents/deployed/{customer}/{agent}/prompts/v{}.md` | Automatic Version Increment | **Overlap** — two version systems |
| Checkpoint/safety | Built into API Gateway | Atomic writes + recovery | **Complementary** — different layers |
| Skills | `skills/` (root) + `.agents/skills/` | Per-blueprint skill loading | **Conflict** — Forge has isolated skills per blueprint |
| Hardware | Cloud (Vercel + VPS) | Local (USB, Machine-A/B) | **Different** — no conflicts |
| Dashboard | Next.js + Tailwind | Explicitly excluded (non-goal) | **Complementary** — Forge has no UI |

### 2.3 What styde.ai Can Adopt from Styde Forge

| Concept | From Forge | To styde.ai | Value |
|---------|------------|---------------|-------|
| **Eval pipeline** | 6-layer evaluation | `ca-agent-reviewer` (BUILD_PHASE_2 §2.1) | Raises quality of agent review |
| **Teacher-Student pattern** | Teacher analyzes → coaches | Improvement loop (BUILD_PHASE_2 §2.2) | More structured feedback |
| **Caveman Ultra** | 70% token reduction | All internal agent prompts | Lowers cost, increases speed |
| **Blueprint structure** | `persona.md + BLUEPRINT.md + config.yaml + skills/` | `agents/templates/{agenttype}/` + Agent Wardrobe | More detailed agent definition |
| **JSON-lines logging** | Structured machine-readable logging | `obsidian/05_ops/logs/` + API Gateway | Better traceability |
| **Atomic writes** | Temp→rename for all persistence | API Gateway + deployment scripts | Prevents corrupted files |
| **Hardware profiles** | Auto-detect + param adaptation | Not relevant (cloud) | — |
| **Bayesian Weight Optimization** | Adaptive eval weights | Version 2 of agent review | Long-term quality improvement |

### 2.4 What Should NOT Be Adopted

| Concept | Why not |
|---------|-------------|
| USB-as-primary-store | styde.ai is cloud-based |
| Local hardware detection | Runs on VPS, not gaming rigs |
| DeepSeek exclusivity | styde.ai should be provider-agnostic |
| Separate blueprint system | We already have `agents/templates/` + REORG_01 |
| Portable one-prompt import | Irrelevant for cloud deployment |

---

## Part 3: Integration Plan

### 3.1 Strategy: Incremental Adoption, Not Fusion

Styde Forge and styde.ai remain **separate systems** with clear interfaces.
Alpedal runs Forge locally. William builds styde.ai in the cloud. Adoption happens
by **concepts and patterns** from Forge being integrated into styde.ai's
agent-building process — not by merging the systems.

### 3.2 Integration Points

```
ALPEDAL (Styde Forge)              WILLIAM (styde.ai)
─────────────────────              ────────────────────
Blueprints/                       agents/templates/
  persona.md                        prompt.md
  BLUEPRINT.md          ──→        tools.yaml
  config.yaml                       config.yaml
  skills/                           (per customer)
       │
       │ (When Forge agent reaches ≥85/100)
       ▼
Eval Pipeline          ──→        ca-agent-reviewer
  LLM-as-Judge                      (BUILD_PHASE_2 §2.1)
  Self-Eval
  Cross-Judge
       │
       │ (Improvement suggestions)
       ▼
Teacher Agent          ──→        Agent improvement loop
  Feedback                          (BUILD_PHASE_2 §2.2)
  Skill extraction
  Anti-patterns
```

**Flow:**
1. Alpedal designs a blueprint in Forge → runs eval loop → agent reaches ≥85/100
2. Alpedal exports the blueprint to styde.ai's `agents/templates/{agenttype}/`
3. William/Architect Agent adapts the blueprint for customer (fill in variables, tone-of-voice)
4. Agent is deployed to customer via styde.ai's dashboard
5. Feedback from customer + logs → back to Forge for further refinement

### 3.3 Implementation Order

| Phase | What | Who | Time |
|-----|-----|-----|-----|
| **Now** | Accept Styde Forge as Alpedal's internal tool. No code changes in styde.ai. | Both | 0 days |
| **Phase 1** | Adopt Caveman Ultra in all styde.ai internal prompts/skills. Copy prompt pattern from `10_Operations/Caveman_Ultra_Mode.md`. | Hermes | 1 day |
| **Phase 2** | Upgrade `ca-agent-reviewer` with lessons from Forge's eval pipeline. Add composite scoring (self-eval 30% + judge 50% + consensus 20%). | Hermes | 2 days |
| **Phase 3** | Create `ca-forge-bridge` — a new skill that enables styde.ai to import a Forge blueprint and convert to `agents/templates/` format. | Hermes | 2 days |
| **Phase 4** | Adopt JSON-lines format for styde.ai's logs in `05_ops/logs/`. | Hermes | 1 day |
| **Phase 5** | (Future) When Forge is in production: automatic sync Forge → styde.ai templates when a blueprint reaches ≥85/100. | Alpedal + Hermes | 3 days |

### 3.4 Architecture Decisions

| # | Decision | Rationale |
|---|--------|------------|
| 1 | **Styde Forge and styde.ai remain separate repos.** | Different purposes, different hardware, different owners. Integration via API/export, not merge. |
| 2 | **Forge blueprints → styde.ai templates (one-way).** | Forge is the refinery; styde.ai is the delivery platform. Templates flow from Forge to styde.ai, never the reverse. |
| 3 | **Caveman Ultra becomes default in styde.ai.** | Immediate cost savings. No downsides. |
| 4 | **Alpedal owns Forge. William owns styde.ai.** | Clear domains. Alpedal = agent design. William = platform + customer. |
| 5 | **No Forge-specific components in styde.ai's customer deliveries.** | Customer agents must be sterile. Forge's internal mechanisms (eval, teacher, sampling) belong in Forge, not with the customer. |

---

## Part 4: Rules That Must Be Rewritten

### 4.1 _RULES.md — Changes

| § | Change | Reason |
|----|---------|-------|
| §10 (Logging) | Add: "Logs are written in JSON-lines format for machine readability. See `ca-change-logger` for schema." | Adopt Forge's log format |
| New §11 | "Styde Forge: Alpedal's agent refinery is a separate system. Blueprints are exported from Forge to styde.ai via `ca-forge-bridge`. No Forge components may appear in customer deliveries." | Clear boundary between systems |

### 4.2 MASTER_PLAN_FINAL — Changes

| Section | Change |
|---------|---------|
| §6 (External skills) | Add reference to Styde Forge as Alpedal's tool, not a skill package |
| §2.3 (Skill format) | No change — Forge's skills are isolated per blueprint and do not affect styde.ai's skill format |

### 4.3 REORG_01 — Confirm

REORG_01's principles are confirmed and reinforced:
- `skills/` = internal (our bots) ✓
- `agents/` = customer deliveries (sterile) ✓
- `agents/templates/` = where Forge blueprints land ✓

### 4.4 BUILD_PHASE_2 — Update

| § | Change |
|----|---------|
| §2.1 (Feedback loop) | Replace simple "analysis agent" with Forge-inspired composite scoring: self-eval (30%) + judge (50%) + consensus (20%) |
| §2.2 (Cross-agent review) | Forge's Cross-Judge Consensus complements — used for anonymous review between customers' agents |

### 4.5 IMPLEMENTATION_PHASE_1 — Update

| § | Change |
|----|---------|
| Phase 1A.2 (Agent Wardrobe) | Blueprint format updated: `blueprint.yaml` gets `forge_source: true/false` to mark if the blueprint originates from Forge |
| New Phase 1E | `ca-forge-bridge` — converts Forge blueprint → styde.ai template |

### 4.6 SYSTEM_DOCUMENT.md — Update

| Section | Change |
|---------|---------|
| §2 (What we have built) | Add reference to Styde Forge as Alpedal's agent refinery |
| §6 (The team) | Alpedal's role clarified: owns Forge, designs blueprints, conducts audits |

### 4.7 INDEX.md — Update

Add under `02_architecture/`:
```
- [[FORGE_INTEGRATION]] | Styde Forge → styde.ai integration spec | William + Alpedal
```

---

## Part 5: Immediate Next Steps

| Prio | Action | Responsible |
|------|--------|----------|
| P0 | **Pull StydeForge into the repo** — copy `v3.0_Phase0/` to `obsidian/03_prototypes/styde-forge/` as reference | Hermes (now) |
| P0 | **Create `ca-forge-bridge`** — new skill for converting Forge blueprint → styde.ai template | Hermes |
| P1 | **Adopt Caveman Ultra** — update all ca-skills to run Caveman Ultra as default | Hermes |
| P1 | **Update ca-agent-reviewer** — composite scoring from Forge's eval pipeline | Hermes |
| P2 | **Update planning documents** — _RULES.md, BUILD_PHASE_2, IMPLEMENTATION_PHASE_1 | Hermes |
| P2 | **Let Alpedal review this audit** — confirm the interpretation is correct | Alpedal |

---

## Comments

<!-- Translated from Swedish to English by Hermes Agent on 2025-06-25 -->
- 2026-06-25 | hermes: Full audit of Styde Forge v3.0 (51 documents, 0 code). Assessed as exceptional design (9/10) but 0 execution (1/10). Recommends incremental adoption — adopt Caveman Ultra, eval patterns, blueprint format — without merging the systems. Forge and styde.ai remain separate with a clear interface.
