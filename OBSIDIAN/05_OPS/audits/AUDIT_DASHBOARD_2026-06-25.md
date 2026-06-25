---
title: "System Audit — Admin Dashboard Planning"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/DRAFT, author/HERMES, type/REPORT]
status: draft
---

# System Audit: styde — Preparing for Admin Dashboard

> Part 1 of 2. Hermes (DeepSeek Pro) → Opus (Antigravity/Claude).
> Purpose: Full system audit in preparation for building internal admin dashboard.
> This dashboard is for US (William + Alpedal) — not for customers.

---

## 1. Current State — What Actually Exists

### 1.1 Code (Production Code)

| Type | Count | Status |
|-----|-------|--------|
| Python files | 0 | Does not exist |
| JavaScript/TS | 0 | Does not exist |
| Next.js project | 0 | Nothing created |
| API/backend | 0 | Nothing deployed |
| Database | 0 | No PostgreSQL |
| Dashboard | 0 | No code written |

**Conclusion: styde has 0 lines of production code.** Everything is documentation.

### 1.2 Skills (Internal)

| # | Skill | Category | Version | Status |
|---|-------|----------|---------|--------|
| 1 | ca-brainstorming | planning | 2.1.0 | Active — instructions, not code |
| 2 | ca-file-organizer | core | 1.1.0 | Active — instructions |
| 3 | ca-folder-organizer | core | 1.1.0 | Active — instructions |
| 4 | ca-rules-enforcer | core | 1.1.0 | Active — instructions |
| 5 | ca-plan-creator | planning | 1.1.0 | Active — instructions |
| 6 | ca-plan-reviewer | planning | 1.1.0 | Active — instructions |
| 7 | ca-agent-builder | delivery | 1.1.0 | Active — instructions |
| 8 | ca-audit-agent | delivery | 1.1.0 | Active — instructions |
| 9 | ca-audit-reporter | delivery | 1.1.0 | Active — instructions |
| 10 | ca-offert-writer | delivery | 1.1.0 | Active — instructions |
| 11 | ca-onboarding-lead | delivery | 1.1.0 | Active — instructions |
| 12 | ca-change-logger | core | 1.1.0 | Active — instructions |

**All 12 skills are markdown instructions. No skill contains executable code.**

### 1.3 Skills (External — in .agents/skills/)

| Source | Count | Type |
|-------|-------|-----|
| addyosmani/agent-skills | 24 | Discipline, build, test, review |
| kepano/obsidian-skills | 5 | Obsidian format, canvas |
| JuliusBrussee/caveman | 7 | Compression efficiency |
| anthropic/skill-creator | 1 | Skill creation |
| obra/brainstorming | 1 | Design-first |

**Total: 37 external skills installed.** Excluding the 5 kepano skills, the majority focus on code quality and discipline — no code to apply them to.

### 1.4 Planning Documents

| # | Document | Status | Tasks completed |
|---|----------|--------|------------------|
| 1 | MASTER_PLAN_FINAL | approved | 0/33 |
| 2 | ROADMAP | approved | 12/30 (40%) |
| 3 | IMPLEMENTATION_PHASE_1 | draft | 0 started |
| 4 | BUILD_PHASE_2 | draft | 0 tasks defined |
| 5 | REORG_01 | draft (completed) | All steps done |
| 6 | PLAN_SUMMARY | draft | N/A (analysis) |

**Problem:** 6 plans with overlapping scope. MASTER_PLAN_FINAL has 33 tasks but 0 are checked off. IMPLEMENTATION_PHASE_1 is supposed to replace it, but it's still a draft.

### 1.5 Customer Data

| Folder | Contents |
|------|----------|
| obsidian/04_clients/ | Only templates (AUDIT_TEMPLATE, OFFERT_TEMPLATE) |
| agents/deployed/ | Created but empty |
| agents/templates/ | Created, _README.md exists, no agent types yet |

**0 customers. 0 ongoing audits. 0 agents deployed.**

---

## 2. Dashboard — What's Been Spec'd

### 2.1 Customer Dashboard (DASHBOARD_SPEC.md)

Three screens spec'd for MVP:
- Dashboard Home — agent cards with status + "Run Now"
- Agent Detail — history, logs, configuration
- Activity Log — last 30 days

### 2.2 Admin Functions (BUILD_PHASE_2.md §4)

Prioritized build order defined:
- P1: Agent list, manual trigger, run history, login, empty state
- P2: Agent detail view, tenant admin, role management, error notifications
- P3: Agent configuration, improvement suggestions, cost analysis
- P4: White-label, SLA dashboard, webhooks

### 2.3 Admin Dashboard (Ours — IMPLEMENTATION_PHASE_1 §1D)

Minimal dashboard spec'd in Phase 1D:
- Page 1: `/` — run test-audit or view latest
- Page 2: `/garderob` — browse agent blueprints
- Page 3: `/kunder` — list customers and their agents (empty)

---

## 3. Gap Analysis — Admin Dashboard vs Reality

### 3.1 What the Admin Dashboard NEEDS (William's Requirements)

Based on your description, you want:

1. **Full overview of the system** — not just customers, everything
2. **All customers on one screen** — customer list with status
3. **All agents per customer** — quick overview for support
4. **Direct chat into the system** — talk to agents/backend
5. **Responsive customer support** — quickly see and act

### 3.2 What's Missing

| Need | Spec exists? | Code exists? | Gap |
|-------|------------|------------|-----|
| Customer overview (all customers) | Partially (Phase 1D: `/kunder`) | No | Large |
| Agent overview per customer | Partially (DASHBOARD_SPEC) | No | Large |
| System health/status | Not spec'd at all | No | Brand new |
| Direct chat | Not spec'd | No | Brand new |
| Log overview (global) | Partially (activity log) | No | Large |
| Skill management (see which skills are active) | Not spec'd | No | Brand new |
| Plan status (which phase are we in?) | Not spec'd | No | Brand new |
| Prompt management (edit agent prompts) | Yes (BUILD_PHASE_2 §4, P3) | No | Large |
| Economy/pricing overview | Not spec'd | No | Brand new |

### 3.3 The Architecture Gap

The dashboard spec (DASHBOARD_SPEC.md) conflates two things:
- **Customer dashboard** — for customer staff (see agents, press buttons)
- **Admin dashboard** — for us (see all customers, all status, direct support)

These are two different systems sharing a backend. They must be separated.

---

## 4. Risks — Prioritized

| # | Risk | Impact | Probability |
|---|------|--------|-------------|
| 1 | **Plan-drowning** — 6 overlapping plans, no clear "source of truth" | High | 100% (happened) |
| 2 | **0 code built** — all energy on documentation, nothing executable | Critical | 100% |
| 3 | **No customers** — sales haven't started | High | 100% |
| 4 | **Admin dashboard spec'd too early** — dashboard is P2, build Consultant Agent first | Medium | 50% |
| 5 | **External skills unused** — 37 skills for code quality, 0 lines of code | Low | 100% |
| 6 | **Alpedal not onboarded** — onboarding report missing, no active role | Medium | 80% |
| 7 | **Master Plan vs Implementation Plan** — two parallel "master" documents | Medium | 100% |

---

## 5. Hermes Recommendations

### 5.1 IMMEDIATE (this week)

1. **Archive MASTER_PLAN_FINAL** — replaced by IMPLEMENTATION_PHASE_1. Status: archived.
2. **Approve IMPLEMENTATION_PHASE_1** — make it the ONLY active build plan.
3. **Start building the Consultant Agent** — this is P0. No dashboard before there's something to show.
4. **Start sales** — 20 outreach/day. The system doesn't matter without customers.

### 5.2 Dashboard Build — Right Order

Admin dashboard is not priority 1. Correct build order:

```
1. Consultant Agent (show value → get customers)
2. Agent Wardrobe (blueprints → reusability)
3. Architect Agent (match → generate)
4. Customer Dashboard MVP (give the customer something to look at)
5. Admin Dashboard (our overview — only once we HAVE customers to overview)
```

The admin dashboard is important but secondary to getting the first customer. Build it when you have ≥2 deployed agents with ≥1 customer.

### 5.3 Admin Dashboard — Right Scope

When built, separate into two views:

**View 1: System View (dev/admin)**
- Customer list with status
- Agents per customer with live status
- Global activity log (all customers)
- System health (API Gateway status, agent uptime)
- Skill index (which skills are installed, versions)
- Direct prompt editor (open an agent's prompt and adjust)

**View 2: Customer View (what the customer sees)**
- Own agents with status
- Run button
- Own activity log
- Own statistics

### 5.4 Chat-Into-The-System

William mentioned direct chat. This is a powerful idea but requires thoughtful implementation:

- The chat is a prompt box that sends directly to Hermes/Antigravity with full system context
- Used for: "Show all errors from Customer X this week", "Update prompt for Agent Y", "What's the status of our pipeline?"
- Implementation: API endpoint that takes text → routes to right agent → returns answer + action
- This is a P3 feature — build the base dashboard first

---

## 6. Summary — State of the Union

| Dimension | Status | Rating (1-10) |
|-----------|--------|---------------|
| Documentation | Extensive, structured | 8 |
| Planning | 6 overlapping plans, messy | 4 |
| Code | 0 lines | 1 |
| Skills (internal) | 12, well-defined | 7 |
| Skills (external) | 37, over-installed for current state | 5 (excessive) |
| Customer base | 0 customers | 1 |
| Dashboard | Spec'd but not built | 2 |
| Sales | Not started | 1 |
| Team | William solo, Alpedal inactive | 3 |

**Total score: 3.6/10**

Strengths: The thinking is solid. The architecture is well thought through. The skills system is robust.

Weaknesses: Nothing is built. No customers. Too much planning, too little execution.

**Recommendation: Stop planning. Start building. Consultant Agent first.**

---

## Comments

<!-- Translated from Swedish to English by Hermes Agent on 2025-06-25 -->
- 2026-06-25 | hermes (DeepSeek Pro): Part 1 of system audit complete. 37 external skills, 12 internal, 0 lines of code. Admin dashboard is important but build Consultant Agent first. See continuation in §7 (prompt to Opus).
