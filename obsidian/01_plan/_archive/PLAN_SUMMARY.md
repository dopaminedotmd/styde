---
title: "PLAN_SUMMARY — All plans reviewed"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/DRAFT, author/HERMES, type/REPORT]
status: draft
---

# Plan Summary — complete checklist

> All plans in `obsidian/01_plan/` reviewed 2026-06-25.
> Purpose: create a clear picture of what is done, ongoing, and forgotten.

---

## 1. Status per plan

| # | Plan | Status | Tasks | Comments | Priority |
|---|------|--------|-------|-------------|-----------|
| 1 | **ROADMAP** | approved | 12/30 done (40%) | YES | **Active** |
| 2 | **MASTER_PLAN_FINAL** | approved | 0/33 done (0%) | NO | **Should be archived** |
| 3 | **IMPLEMENTATION_PHASE_1** | draft | No tasks | YES | **Active — being built now** |
| 4 | **BUILD_PHASE_2** | draft | No tasks | YES | Dormant — waiting for Phase 1 |
| 5 | **REORG_01** | draft | No tasks | YES | **Completed** (client-work → delivery) |
| 6 | **Hypothetical Agents Design** | draft | No tasks | YES | Idea stage |

---

## 2. Checklist — what's in progress

### ROADMAP — Phase 1 (Proof of Concept)

**Done:**
- [x] Repo and file structure
- [x] Agent rules (_RULES)
- [x] Business concept + pricing
- [x] Role assignment (William solo + Alpedal onboarded)
- [x] First agent template
- [x] Dashboard MVP (Next.js)
- [x] Website (Lovable-prompt redo)
- [x] First customer's agents built
- [x] First system delivered

**Remaining:**
- [ ] **Create audit-template** — Alpedal + Hermes (see ca-audit-agent + AUDIT_TEMPLATE)
- [ ] **Sales — 20 outreach/day** — William
- [ ] **Land first audit** — William
- [ ] **Conduct first audit** — Alpedal + William
- [ ] **Write case study from first customer**

### IMPLEMENTATION_PHASE_1 (newest plan)

- [ ] **Phase 1A.1: Consultant Agent** — crawl → classify → diagnostics → report (4 days)
- [ ] **Phase 1A.2: Agent Wardrobe** — 3 blueprints with templates (2 days)
- [ ] **Phase 1B.1-3: Architect Agent** — match, generate prompt, build proposal (4 days)
- [ ] **Phase 1C: Security** — data isolation per customer (3 days, parallel)
- [ ] **Phase 1D: Dashboard** — minimal Next.js with audit + wardrobe (3 days)

### MASTER_PLAN_FINAL (should be archived)

33 tasks in the plan, **0 done**. The plan is approved but built for the old structure (Consulting.ai, client-work, building). The new `IMPLEMENTATION_PHASE_1` replaces it. Recommend archiving MASTER_PLAN_FINAL when IMPLEMENTATION_PHASE_1 is accepted.

---

## 3. What is unclear / blocking

| Problem | Plan | Cause |
|---------|------|-------|
| MASTER_PLAN_FINAL has 33 tasks but 0 checkboxes checked | MASTER_PLAN_FINAL | The plan is approved but tasks are in prose, not checkboxes. Nothing has been recorded as done. |
| BUILD_PHASE_2 is written but has no tasks at all | BUILD_PHASE_2 | 587 lines, very detailed, but no checkbox structure. Should be broken down or archived. |
| REORG_01 is marked "draft" but is completed | REORG_01 | client-work → delivery is already done. Status should be updated to "approved" or "archived". |
| Hypothetical Agents Design has no decision | design-doc | Should we build these agents or is it inspiration? Unclear next step. |

---

## 4. Recommended next steps

| Prio | Action |
|------|--------|
| P0 | **Mark REORG_01 as "archived"** — it is completed |
| P0 | **Approve IMPLEMENTATION_PHASE_1** — it is the active build plan |
| P1 | **Archive MASTER_PLAN_FINAL** or rewrite with checkboxes. 33 tasks in prose are impossible to track. |
| P1 | **Decision on BUILD_PHASE_2** — should it be broken into tasks and prioritized, or archived for now? |
| P2 | **Decision on Hypothetical Agents** — build or save as inspiration? |
| P2 | **Start sales** — ROADMAP says 20 outreach/day. Nothing else matters more if we have no customers. |

---

## 5. File structure — after rename

```
obsidian/
├── _RULES.md
├── INDEX.md
├── SYSTEM_DOCUMENT.md
├── _skills/
├── _users/
├── _templates/
├── 00_strategy/
├── 01_plan/             ← All plans live here
├── 02_architecture/
├── 03_prototypes/
├── 04_clients/
├── 05_ops/
└── 99_references/
```

All lowercase. All references in skills and documents updated.

---

## Comments

- 2026-06-25 | hermes: Created after review of all 6 plans in 01_plan/. MASTER_PLAN_FINAL has 33 tasks of which 0 are done — large discrepancy against ROADMAP which shows 12/30 done. Recommends cleaning up status on old plans and concentrating all build work on IMPLEMENTATION_PHASE_1.
- 2026-06-25 | hermes: Translated to English per new language policy.
