---
title: "MASTER_PLAN_FINAL — styde"
date: 2026-06-24
author: hermes
status: approved
version: 1.0.0-final
---

# MASTER_PLAN_FINAL — styde

> AI-agent consulting for Swedish SME companies.
> *styde — from the Swedish "styrd". Controlled automation.*
> Reviewed by Hermes, Antigravity (Sonnet), AgY (Gemini Pro), AgY Flash High.
> Status: ALL BOTS UNIFIED. IMPLEMENTATION STARTS.

---

## 1. Executive Summary

styde builds AI-agent systems for Swedish SME companies (10-250 employees). We map their IT flows, build agents that automate, and deliver a dashboard where staff press buttons.

**Status:** William building solo. Alpedal being onboarded for audits and solutions review.  
**Platform:** Everyone runs Hermes. Same CLI, same skill format, no conversion.  
**Standard:** agentskills.io (Apache 2.0, created by Anthropic).  
**Skill naming convention:** `ca-` prefix — `ca-file-organizer`, `ca-audit-agent`.  
**Knowledge base:** obsidian/ with YAML frontmatter, wikilinks, callouts.

---

## 2. System Architecture

### 2.1 Folder Structure

```
consulting.ai/
│
├── .agents/
│   ├── AGENTS.md              ← "You MUST read obsidian/_RULES.md before proceeding."
│   ├── skills.json            ← { "entries": [
│   │                              { "path": "../skills/core" },
│   │                              { "path": "../skills/planning" },
│   │                              { "path": "../skills/delivery" },
│   │                              { "path": "../skills/reusable" }
│   │                            ] }
│   └── skills/                ← System skills (externally installed)
│
├── skills/                    ← OUR shared skills library
│   ├── SKILLS_INDEX.md
│   ├── core/                  ← ca-change-logger, ca-file-organizer, ca-folder-organizer, ca-rules-enforcer
│   ├── planning/              ← ca-brainstorming, ca-plan-creator, ca-plan-reviewer
│   ├── delivery/              ← ca-agent-builder, ca-audit-agent, ca-audit-reporter, ca-offert-writer
│   └── reusable/              ← ca-fortnox-connector, ca-google-workspace-agent
│
└── obsidian/                  ← Knowledge base
    ├── _RULES.md              ← Bot rules: tags, frontmatter, comments
    ├── _skills/               ← Obsidian-specific skills
    ├── _users/               ← william.md, alpedal.md (elb archived)
    ├── 00_strategy/           ← Business, market, pricing
    ├── 01_plan/               ← Roadmap
    ├── 02_architecture/       ← System, dashboard-spec, agent-framework
    ├── 03_prototypes/         ← Code (William)
    ├── 04_clients/            ← Customer templates + active work
    └── 05_ops/                ← Subscription, onboarding
```

### 2.2 Three Technical Ground Rules (ANTIGRAVITY REQUIREMENTS)

| # | Rule |
|---|-------|
| 1 | `.agents/skills.json` lists each category subfolder. Forward slash (`../skills/core`) — Windows-compatible. |
| 2 | `.agents/AGENTS.md` explicitly contains: "You MUST read obsidian/_RULES.md before proceeding." |
| 3 | Skill folders use `resources/` (not `assets/`) for templates. |

### 2.3 Skill Format

```
ca-my-skill/
├── SKILL.md          # REQUIRED
├── scripts/          # Optional
├── references/       # Optional
└── resources/        # Optional: templates
```

**SKILL.md frontmatter:**
```yaml
---
name: ca-my-skill
description: Short trigger description
version: 1.0.0
owner: william
last-updated: 2026-06-24
---
```

### 2.4 Progressive Loading

1. **Discovery** — bot sees only `name` + `description`
2. **Activation** — task matches description → loads full SKILL.md
3. **Execution** — bot follows instructions

---

## 3. Implementation Plan

### Phase 0: Foundation (1 day)

**Goal:** Repo structure + external skills in place. Zero risk.

#### Task 0.1: Create `.agents/skills.json`

- [ ] Create: `.agents/skills.json`

```json
{
  "entries": [
    { "path": "../skills/core" },
    { "path": "../skills/planning" },
    { "path": "../skills/delivery" },
    { "path": "../skills/reusable" }
  ]
}
```

- [ ] Verify: `cat .agents/skills.json` shows JSON without syntax errors
- [ ] **Commit**

#### Task 0.2: Create `.agents/AGENTS.md`

- [ ] Create: `.agents/AGENTS.md`

```markdown
# Agent Rules — styde

You MUST read obsidian/_RULES.md before proceeding with any task in this repository.
All planning documents are in obsidian/. All skills are in skills/ (custom) and .agents/skills/ (external).
Use ca- prefix for all styde skills.
```

- [ ] Verify: file exists, contains "You MUST read"
- [ ] **Commit**

#### Task 0.3: Create `skills/` structure

- [ ] Create folders:

```bash
mkdir -p skills/core skills/planning skills/delivery skills/reusable
```

- [ ] Create: `skills/SKILLS_INDEX.md` with content:

```markdown
# Skills Index — styde

| Skill | Category | Owner | Version | Description |
|-------|----------|-------|---------|-------------|
```

- [ ] Verify: all 5 subfolders + index created
- [ ] **Commit**

#### Task 0.4: Install external skills

- [ ] Install Addy Osmani:

```bash
npx skills add addyosmani/agent-skills
```

Expected: success message, skills installed as individual folders in `.agents/skills/`

- [ ] Install Kepano Obsidian:

```bash
npx skills add kepano/obsidian-skills
```

Expected: success message, skills installed as individual folders in `.agents/skills/`

- [ ] **Comment:** Taste Skill installed in Phase 3 (dashboard v2).
- [ ] **Commit**

#### Task 0.5: Verify skill discovery

- [ ] Test: ask a bot to use `ca-file-organizer`. The bot should respond that the skill doesn't exist yet.
- [ ] Test: ask a bot to list available skills. Should include both `.agents/skills/` and `skills/`.
- [ ] Expected: discovery works from both trees.

> Phase 0 complete when: all 5 tasks are green.

---

### Phase 1: Core Skills (1-2 weeks)

**Goal:** Six internal skills that block everything else.

| Prio | Skill | Category | Built by |
|------|-------|----------|----------|
| 0.5 | `ca-brainstorming` | planning | Hermes |
| 1 | `ca-file-organizer` | core | Hermes |
| 2 | `ca-folder-organizer` | core | Hermes |
| 3 | `ca-rules-enforcer` | core | Hermes |
| 4 | `ca-plan-creator` | planning | Hermes |
| 5 | `ca-plan-reviewer` | planning | Hermes |

#### Task 1.1: Build `ca-brainstorming`

- [ ] Create: `skills/planning/ca-brainstorming/SKILL.md`

```markdown
---
name: ca-brainstorming
description: Use before any build task. Explore, question, design before code.
version: 1.0.0
owner: william
last-updated: 2026-06-24
---

# ca-brainstorming

## When to use
Activate before any implementation task. This skill forces a design-first approach.

## Workflow
1. **Explore:** List 3 alternative approaches to the problem.
2. **Question:** Write down 3 assumptions and test each one.
3. **Design:** Create a mini-spec (max 10 lines) before any code.
4. **Get approval:** Post the mini-spec as a comment in the relevant plan document.
5. **Only then:** Proceed to implementation.

## Rule
No code before an approved design. Ever.
```

- [ ] **Commit**

#### Task 1.2: Build `ca-file-organizer`

- [ ] Create: `skills/core/ca-file-organizer/SKILL.md`

Content: governs where new files go. Naming convention `CAPITAL_LETTERS_with_underscores.md`. Max 3 levels. Archive: `status/ARCHIVED`.

- [ ] **Commit**

#### Task 1.3: Build `ca-folder-organizer`

- [ ] Create: `skills/core/ca-folder-organizer/SKILL.md`

Content: never create folders outside defined ones. New category → plan in `01_plan/` first.

- [ ] **Commit**

#### Task 1.4: Build `ca-rules-enforcer`

- [ ] Create: `skills/core/ca-rules-enforcer/SKILL.md`

Content: flags violations (wrong folder, wrong frontmatter, wrong tags, missing comment section). Does NOT block. Writes comment + notifies owner.

- [ ] **Commit**

#### Task 1.5: Build `ca-plan-creator`

- [ ] Create: `skills/planning/ca-plan-creator/SKILL.md`

Content: uses PLAN_TEMPLATE.md in obsidian/_templates/. Ensures frontmatter is correct. Tags according to _RULES.md.

- [ ] **Commit**

#### Task 1.6: Build `ca-plan-reviewer`

- [ ] Create: `skills/planning/ca-plan-reviewer/SKILL.md`

Content: reviews plans. Checklist: frontmatter OK? Tags correct? Folder correct? Comment section present? No placeholders ("TBD", "TODO")?

- [ ] **Commit**

#### Task 1.7: Test Acceptance

- [ ] Test 1: Bot creates new plan → uses PLAN_TEMPLATE.md, frontmatter correct
- [ ] Test 2: Bot places file in correct obsidian/ folder
- [ ] Test 3: Bot invokes correct skill based on task
- [ ] Test 4: Comment system: date + author + text, correct format

> Phase 1 complete when: all 4 tests green.

---

### Phase 2: Foundation — System & Sales (4-6 weeks)

**Goal:** Dashboard MVP, website, audit system, first paying customer.

| # | Task | Responsible | Start |
|---|---------|----------|-------|
| 2.1 | Build `ca-obsidian-markdown` + `ca-obsidian-frontmatter` | Hermes | Day 1 |
| 2.2 | Build dashboard MVP | William | Day 1 |
| 2.3 | Build website | William | Day 1 |
| 2.4 | Build `ca-audit-agent` + `ca-audit-reporter` | Hermes (template) → Alpedal (test) | Day 1 |
| 2.5 | **Sales: 20 outreach/day** | William | **Day 1 — parallel** |
| 2.6 | Build `ca-agent-builder` | William + Hermes | Week 2 |
| 2.7 | Land first audit | William + Alpedal | Week 2-4 |
| 2.8 | Conduct first audit | Alpedal + William | Week 3-5 |
| 2.9 | Build first customer's agents | William | Week 4-6 |
| 2.10 | Deliver first system | All | Week 6 |
| 2.11 | Write case study | William | Week 6 |

> **Critical:** Sales (2.5) starts day 1, not after dashboard/website.
> Average sales cycle: 2-4 weeks → matches MVP build time.

---

### Phase 3: Scale (after first customer)

- Dashboard v2 (Taste Skill activated)
- First reusable skill born from customer work
- `ca-plugin-manager` built (groups skills in bundles of max 10)
- 5 paid audits, 3 implementations, 2 subscriptions

### Phase 4: Grow (12 months)

- 15+ audits, 8+ implementations, 5+ subscriptions
- 1.5-2 MSEK ARR
- Each new customer faster than the last — flywheel spinning

---

## 4. Business Model

### 4.1 Three-step Model

| Step | Price | Time | Description |
|------|------|-----|-------------|
| **Audit** | 19,900 SEK | 2 days | Mapping, report, proposal. **Deduction clause:** if Build purchased ≤30 days, 19,900 SEK deducted from Build price. |
| **Build** | 99,000-300,000 SEK | 3-4 weeks | Agents + dashboard + integrations + training |
| **Operate** | 4,900-19,900 SEK/month | Ongoing | Operations, updates, support |

### 4.2 Subscription Tiers with SLA

| Tier | Price | Agents | SLA | Included |
|------|------|---------|-----|------------|
| Basic | 4,900 SEK/month | 1-3 | Email 24h weekdays | Operational monitoring, bug fixes. No changes to agent logic. |
| Pro | 9,900 SEK/month | 4-8 | Email+phone 8h weekdays | + 2h free development time/month for fine-tuning. |
| Enterprise | 19,900 SEK/month | Unlimited | Priority 2h around the clock | + 6h free development time/month. White-label dashboard. Sold only after 3 stable Pro customers. |

### 4.3 Customer Economics (example Pro customer year 1)

Audit 19,900 + Build 150,000 + Sub 118,800 = **288,700 SEK**

---

## 5. Team & Responsibilities

| Person | Role | Responsibility |
|--------|------|--------|
| William | Founder, Creative Director, Builder, **GDPR responsible (interim)** | Vision, sales, build everything, customer relations, data protection |
| Alpedal | Solutions Architect | Customer audits, mapping, report writing |

---

## 6. External Skills — Installation Order

| # | Skill | When | Why |
|---|-------|-----|--------|
| 1 | `addyosmani/agent-skills` | Phase 0 | Discipline: Define→Plan→Build→Verify→Review→Ship |
| 2 | `kepano/obsidian-skills` | Phase 0 | Consistent Obsidian syntax for all documents |
| 3 | `Leonxlnx/taste-skill` | Phase 3 | Install now, activate at dashboard v2 |

**Not now:**
- Obra Superpowers — Phase 3 (sub-agents)
- LobeHub — Phase 4 (customer UI)
- Dify — **NEVER** (competing philosophy)
- sickn33 — **DO NOT install** (study the concept, build own `ca-plugin-manager`)
- OpenClaw — deleted

**Rule:** Search VoltAgent Awesome List ALWAYS before building new reusable skill. Install only if obviously relevant within 2 minutes from README.

---

## 7. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Bots don't find `skills/` subfolders | High | `.agents/skills.json` per category, forward slash |
| William as sole builder (bus factor) | High | Standardized tech stack + full documentation. Hermes builds skills in parallel. |
| Customer data in agent prompts → GDPR | High | William = interim DPO. Data processing agreement with customer before audit. Evaluate on-prem/local model for sensitive data. |
| Skill version breakage | Medium | Pin skill version in `skills.json`. Automatic generation of skills.json via script. |
| Context window exhaustion | Medium | Progressive loading (only name+description at discovery) |
| No one wants to pay for audit | Medium | Deduction clause makes audit risk-free. If 5 leads say no → evaluate pricing. |
| SLA breach | High | Don't sell Enterprise until 3 Pro customers are stable |
| Competition via relationship sales we don't see | Medium | Build references quickly. First customer = case study. |

---

## 8. Tech Stack

Dashboard: **Next.js + Tailwind CSS**  
Backend API: **Node.js Express (REST)**  
Hosting: **Vercel (frontend), VPS of choice (backend)**  
No exceptions without team discussion. Document everything in `02_architecture/`.

---

## 9. obsidian Format

All documents in obsidian/ follow:

```yaml
---
title: "Document Title"
date: 2026-06-24
author: william
tags: [area/STRATEGY, status/APPROVED, author/WILLIAM, type/PLAN]
status: draft
---
```

Tags: `area/STRATEGY | PLAN | ARCHITECTURE | CLIENT | OPS | REFERENCE`  
Status: `status/DRAFT | REVIEW | APPROVED | ARCHIVED`  
Type: `type/CONCEPT | PLAN | REPORT | SPEC | TEMPLATE`

Comments at bottom: `- YYYY-MM-DD | author: text`

---

## 10. Decision Log

| Date | Decision | Consensus |
|-------|--------|-----------|
| 2026-06-24 | `skills/` at root level, subfolders in skills.json | All |
| 2026-06-24 | `ca-` prefix for internal skills | All |
| 2026-06-24 | `resources/` (not `assets/`) in skill folders | All |
| 2026-06-24 | `.agents/AGENTS.md` explicit instruction | All |
| 2026-06-24 | Core skills first, rest on customer time | All |
| 2026-06-24 | sickn33: study, DO NOT install | All* |
| 2026-06-24 | Taste Skill installed now, activated v2 | All |
| 2026-06-24 | Sales starts day 1 in Phase 2 (parallel) | All |
| 2026-06-24 | Deduction clause on audit | All |
| 2026-06-24 | SLA defined per tier | All |
| 2026-06-24 | Next.js + Tailwind for dashboard | All |
| 2026-06-24 | William = GDPR responsible (interim) | All |
| 2026-06-24 | `ca-brainstorming` as prio 0.5 | All |
| 2026-06-24 | `ca-rules-enforcer` at prio 3 | All |
| 2026-06-24 | `ca-plugin-manager` in backlog, built when needed | All |

> *AgY Flash High proposed hybrid sickn33 — majority voted for own build. Decided.

---

## 11. Reusable vs Delivery

- ≥2 customers (or obviously generic) → `skills/reusable/`
- 1 customer → `skills/delivery/`
- After each customer build: 1 hour scheduled to extract generic skill

---

## 12. Immediate Next Steps (Phase 0 — today)

1. William creates `.agents/skills.json` (per category, forward slash)
2. William creates `.agents/AGENTS.md` ("You MUST read obsidian/_RULES.md")
3. William creates `skills/` folder with 5 subfolders + SKILLS_INDEX.md
4. `npx skills add addyosmani/agent-skills`
5. `npx skills add kepano/obsidian-skills`
6. Verify skill discovery from both trees
7. Hermes starts building `ca-brainstorming` (prio 0.5)

## Comments

- 2026-06-25 | hermes: Translated to English per new language policy.
