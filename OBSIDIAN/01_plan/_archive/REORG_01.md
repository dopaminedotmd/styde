---
title: "REORG_01 — Separate skills (internal) from agents (customer)"
date: 2026-06-24
author: hermes
tags: [area/PLAN, status/DRAFT, author/HERMES, type/PLAN]
status: draft
---

# REORG_01 — Separate skills (internal) from agents (customer)

> [!warning] Read the entire document before you act.
> This is a structural reorganization that affects all skills and future work.

> Last updated: 2026-06-24

---

## 1. The Problem

Today EVERYTHING is in `skills/`:

```
skills/
├── core/              ← Internal: ca-brainstorming, ca-change-logger...
├── planning/          ← Internal: ca-plan-creator, ca-plan-reviewer...
├── building/          ← PARTIALLY internal: ca-agent-builder...
├── client-work/       ← PARTIALLY process: templates for audit, proposal, onboarding...
└── reusable/          ← (empty)
```

The problem is that our internal skills speak **our language** — they reference Hermes, our Obsidian documents, our workflows. That is correct for internal use.

But when `ca-agent-builder` generates an agent for a customer — that agent must be **sterile**. It must not know that Hermes exists. It must not reference `ca-brainstorming`. It should only know its mission and its tools.

**Solution:** Separate into two trees.

---

## 2. New structure

```
consulting.ai/
│
├── skills/              ← INTERNAL. Our bots' tools. Our language.
│   ├── SKILLS_INDEX.md
│   ├── core/            ← Internal OS
│   │   ├── ca-brainstorming/
│   │   ├── ca-change-logger/
│   │   ├── ca-file-organizer/
│   │   ├── ca-folder-organizer/
│   │   └── ca-rules-enforcer/
│   ├── planning/        ← Our planning
│   │   ├── ca-plan-creator/
│   │   └── ca-plan-reviewer/
│   └── delivery/        ← Our delivery process (RENAMED from client-work + building)
│       ├── ca-agent-builder/   ← Generates content in agents/
│       ├── ca-audit-agent/
│       ├── ca-audit-reporter/
│       ├── ca-offert-writer/
│       └── ca-onboarding-lead/
│
├── agents/              ← EXTERNAL. What we deliver to customers. STERILE.
│   ├── templates/       ← Templates used by ca-agent-builder to generate
│   │   ├── _README.md
│   │   ├── fortnox-invoice/
│   │   │   ├── prompt.md
│   │   │   ├── tools.yaml
│   │   │   └── config.yaml
│   │   └── gmail-sort/
│   │       ├── prompt.md
│   │       ├── tools.yaml
│   │       └── config.yaml
│   └── deployed/        ← Active customer deliveries
│       └── {customer_id}/{agent_id}/
│           ├── prompts/{v1.0.0.md → current.md}
│           ├── tools/{v1.0.0.yaml → current.yaml}
│           ├── config/current.yaml
│           └── tests/
    ├── input.json      ← Created by ca-agent-builder at agent generation (template: agents/templates/{agent_type}/tests/)
    └── expected.json   ← Same. Contains expected output format for automatic validation.

**How tests run:** A simple bash script (`agents/deployed/run_tests.sh`) loops over each agent's tests/, sends input.json to the agent in dry-run mode, and compares output against expected.json (fuzzy match — structure, not exact text). Result: PASS/FAIL per agent. Run manually after deployment and automatically after prompt changes.
│
├── .agents/             ← UNCHANGED. Points to skills/ for bot-discovery.
│   ├── AGENTS.md
│   ├── skills.json
│   └── skills/          ← External skills (addyosmani, kepano) — unchanged
```

---

## 3. Rules — what applies after the reorganization

### Rule 1: skills/ is internal. Always.

Everything in `skills/` is our tools. Here we use:
- Our language (Swedish, concise)
- Our concepts (Hermes, ca-prefix, obsidian references)
- Our rules (ca-brainstorming requires design before build)

**What happens in `skills/` stays in `skills/`.** No external party sees the content.

### Rule 2: agents/ is the customer's. Always.

Everything in `agents/` is what the customer gets. Here we use:
- The customer's language (English or Swedish depending on the customer)
- No internal references (no Hermes, no obsidian, no ca-prefix)
- Clean prompt.md + tools.yaml + config.yaml

Nothing in `agents/` references `skills/` or our internal documents.

### Rule 3: ca-agent-builder is the bridge

`ca-agent-builder` (in `skills/delivery/`) is the only skill allowed to touch `agents/`. It:
- Is itself internal — uses our language, reads our templates
- **Generates sterile** — output in `agents/` has zero traces of us
- Fetches templates from `agents/templates/` and fills in customer-specific data
- Writes the result to `agents/deployed/{customer}/{agent}/`

**ca-agent-builder reads from `skills/` but writes to `agents/`.**

### Rule 4: .agents/ points to skills/ — unchanged

`.agents/skills.json` and `.agents/AGENTS.md` continue to point to the `skills/` categories.
`.agents/skills.json` is changed to match the new category names (client-work → delivery).
Nothing in `.agents/` points to `agents/` — that is our bots' discovery, not the customer's.

### Rule 5: Improvements travel from deployed → templates

When a prompt improvement in `agents/deployed/{customer}/{agent}/` is deemed **generic** (applies to the agent type, not customer-specific) — it is brought back to templates.

**Flow:**
1. `ca-agent-reviewer` analyzes logs and flags an improvement
2. William approves the improvement for the specific customer
3. `ca-agent-reviewer` assesses: Is this generic for the agent type?
4. If YES → ca-agent-builder updates `agents/templates/{agent_type}/prompt.md` and bumps the template version
5. The next customer with the same agent type starts on the improved baseline

**Rule:** At least 2 different customers must have the same improvement before it is moved to templates.
**Responsibility:** William approves. ca-agent-reviewer flags. ca-agent-builder executes.

---

## 4. Execution — step by step

### Step 1: Rename client-work → delivery

```
Move: skills/client-work/ → skills/delivery/
Change: .agents/skills.json  ← client-work → delivery
Update: all skills that wikilink to "client-work/"
```

### Step 2: Merge building/ → delivery/

```
Move: skills/building/ca-agent-builder/ → skills/delivery/
Remove: skills/building/ (the folder)
Update: .agents/skills.json  ← remove building from the list
Update: SKILLS_INDEX.md
```

### Step 3: Create agents/ structure

```
Create: agents/
Create: agents/templates/
Create: agents/templates/_README.md
Create: agents/deployed/
Create: agents/deployed/_README.md
```

### Step 4: Clean ca-agent-builder/SKILL.md + add positive example

ca-agent-builder MUST NO LONGER reference "obsidian/02_architecture/..." in its generated agents.
Its instructions for prompt.md, tools.yaml, config.yaml must be clean — they must not mention Hermes or our systems.

Examples of what must be removed from generated output:
- ~~"Use ca-brainstorming to..."~~
- ~~"See obsidian/02_architecture/..."~~
- ~~"Run by Hermes..."~~

**Positive example — what a sterile prompt.md should look like:**

```markdown
# Agent: Invoice Manager

## MISSION
Fetch unpaid invoices from Fortnox every Monday at 08:00.
Verify that each invoice has correct VAT and due date.
On deviation: send notification to account manager via Slack.

## TOOLS
- Fortnox API: fetch invoices, update status
- Slack API: send messages to channel

## RULES
- NEVER change an invoice's amount
- NEVER send payment — only notification
- When uncertain: flag for manual review

## OUTPUT FORMAT
{ "status": "ok" | "flag" | "error", "message": "...", "invoices": [...] }
```

Note: No mention of Hermes, ca-skills, obsidian, orchestration systems, or internal processes. The agent is independent.

### Step 5: Create agents/templates/_README.md

A brief instruction to future bots about what templates are and how they are used.
No internal references.

### Step 6: Update INDEX.md and SKILLS_INDEX.md

- INDEX.md: change paths for delivery
- SKILLS_INDEX.md: remove building, rename client-work → delivery

### Step 7: Update all internal wikilinks

All skills that reference `[[client-work/...]]` or `[[building/...]]` must be updated.

---

## 5. What does NOT change

| Item | Status |
|-----|--------|
| `.agents/AGENTS.md` | Unchanged |
| `.agents/skills.json` | Category updates only |
| `.agents/skills/` (external skills) | Unchanged |
| `obsidian/` | No changes |
| `MASTER_PLAN_FINAL.md` | No changes |
| `README.md` | No changes |
| All ca-skill names | Retained (ca-agent-builder continues to be called ca-agent-builder) |

---

## 6. Verification — after reorganization

1. `ls skills/` shows: `core/`, `planning/`, `delivery/`
2. `ls agents/` shows: `templates/`, `deployed/`
3. `.agents/skills.json` lists `../skills/core`, `../skills/planning`, `../skills/delivery`
4. All skills in `skills/delivery/` have their SKILL.md intact
5. `ca-agent-builder` still generates correct templates
6. **Test case:** ca-agent-builder generates output against `agents/templates/fortnox-invoice/` with test data. The result is reviewed manually: prompt.md contains no internal references (Hermes, ca-prefix, obsidian).

---

## Comments

- 2026-06-24 | hermes: Created. Decision from conversation with William: skills = internal, agents = customer's. No Oteck in the project.
- 2026-06-24 | hermes: Updated after bot review — specified deployed/ structure, added Rule 5 (improvement migration), positive prompt example in step 4, test case in verification, config/prompt separation in structure.
- 2026-06-24 | antigravity: Reviewed. The skills/agents separation is correct and necessary. Four points:
  1. `agents/deployed/` lacks a defined folder structure. Suggestion: `agents/deployed/{tenant_id}/{agent_id}/prompts/v{N}.md`. Without this → chaos at customer 3.
  2. No rule governs how improvements travel from `deployed/` back to `templates/`. This is the critical hole in the self-improvement system. Add Rule 5 (see below).
  3. Step 4 lists what should be REMOVED from ca-agent-builder but does not specify what should be INCLUDED. A positive example output is needed — a clean, sterile prompt.md.
  4. Verification §6 point 5 is impossible to verify automatically without a test case. Add: `ca-agent-builder` generates a test output against `agents/templates/fortnox-invoice/` and is reviewed manually.
- 2026-06-24 | antigravity: PROPOSAL Rule 5 (self-improvement system): When an approved prompt improvement in `agents/deployed/{customer}/` is deemed generic (applies to the agent type, not customer-specific) → ca-agent-reviewer flags for template update → William approves → ca-agent-builder updates `agents/templates/{agent_type}/prompt.md` and bumps template version. The next customer with the same agent type already starts on the improved baseline. Without this loop, individual customers' agents improve but not the system as a whole.
- 2026-06-24 | antigravity: Supplementary points for REORG_01:
  5. Dependency isolation: Each deployed agent may need its own library versions. We should plan for virtual environments (venv/package.json) per agent directory to avoid version conflicts when scaling.
  6. Separation of configuration and prompt: Customer-specific parameters (e.g. email addresses, folder IDs) must reside entirely in `config.yaml` so that `prompt.md` remains sterile and directly transferable to `templates/`.

<!-- Translated from Swedish to English, 2026-06-25 -->
