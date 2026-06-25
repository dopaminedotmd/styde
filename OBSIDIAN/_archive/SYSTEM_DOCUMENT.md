---
title: "styde — Systemöversikt"
date: 2026-06-24
author: william
tags: [area/ARKITEKTUR, status/APPROVED, author/WILLIAM, type/SPEC]
status: approved
aliases:
  - System Document
  - Systemöversikt
---

# styde — System Overview

> A complete description of what we've built, how it works, and how you get on board.
> Written for Alpedal — but also as a reference for William.
>
> *Last updated: 24 June 2026*

---

> [!important] Read this first
> This is not a finished system — it's a **hypothesis under test**.
> Roles, prices, and structure are prototypes until reality says otherwise.
> Everything can and should be questioned.

---

## 1. The basic idea

We build **AI agent systems** for Swedish SME companies.

Not consulting hours. Not a one-off project. A **productized system**:

| What | How |
|-----|-----|
| We step into a company | Conduct a structured audit |
| We map their IT workflows | Identify bottlenecks and manual work |
| We build AI agents | Automate the repetitive |
| We deliver a dashboard | Staff press buttons — no coding required |
| We bill monthly | Subscription — not hours |

The model is **audit → build → operate**. The customer pays for the result, not for our time.

---

## 2. What we've built

### Folder structure

```
consulting.ai/
├── MASTER_PLAN_FINAL.md    ← The entire hypothesis written down
├── obsidian/               ← All documentation (you are here)
│   ├── _RULES.md           ← Rules for all bots
│   ├── SYSTEM_DOCUMENT.md  ← This file
│   ├── _users/             ← Onboarding files per person
│   └── _templates/         ← Templates for plans and reports
├── skills/                 ← 11 ca-skills (internal)
└── .agents/                ← Antigravity's system + external skills
    ├── AGENTS.md           ← Points to _RULES.md
    ├── skills/             ← External skills (addyosmani + kepano)
    └── skills.json         ← Registers the skills/ folder
```

### The 11 internal skills (ca-prefix)

These are the **tools** that control how our AI agent (Hermes) behaves. Each skill is an instruction file that activates automatically for the right task.

| Skill | What it does | When it's used |
|-------|-------------|-----------------|
| `ca-brainstorming` | Forces design-first before building | Before every new feature |
| `ca-file-organizer` | Controls where files are placed | On all file operations |
| `ca-folder-organizer` | Keeps folder structure clean | When creating folders |
| `ca-rules-enforcer` | Flags rule violations | Continuously |
| `ca-plan-creator` | Creates plans according to template | During planning |
| `ca-plan-reviewer` | Reviews plans against standard | Before approval |
| `ca-agent-builder` | Template for building AI agents for customers | In the build phase |
| `ca-audit-agent` | Conducts customer audits in a structured way | With new customers |
| `ca-audit-reporter` | Writes the audit report | After audit |
| `ca-offert-writer` | Generates quote from report | Directly after audit |
| `ca-onboarding-lead` | Guides the customer from contract to go-live | In the operations phase |

### External skills installed

In addition to our own skills, we've installed external packages:

- **addyosmani/agent-skills** — 24 skills for discipline, code quality, testing, review, etc.
- **kepano/obsidian-skills** — 5 skills for Obsidian syntax and canvas

> [!tip] How skills work
> A skill is a `.md` file with instructions. Antigravity reads it automatically when you request a matching task. You don't need to say "use skill X" — it happens automatically.

---

## 3. The tool: Antigravity (Hermes)

Everyone on the team runs the **same setup** — this is decided and everyone's environment supports it.

| Tool | What it is |
|---------|------------|
| **VS Code** | Editor — everyone runs this |
| **Antigravity** | VS Code branch with built-in AI agent (Google DeepMind) |
| **Hermes CLI** | Command-line tool alongside — for scripting and automation |

Antigravity + Hermes CLI complement each other: Antigravity for interactive work in the editor, Hermes CLI for execution outside.

### Why the same tools for everyone?

|- **Skills are portable** — a skill Alpedal writes works directly for William
|- **Document format is shared** — same frontmatter, same folders, same conventions
|- **No "my bot does X differently"** — one shared standard

> [!note] Setup
> VS Code + Antigravity is installed as a normal VS Code branch. Hermes CLI is installed separately.
> Skills are read automatically from the `.agents/` folder — no manual configuration step required.

---

## 4. How to get on board

### Step 1 — Clone the repo

```bash
git clone [repo-url]
cd styde
```

### Step 2 — Open in VS Code / Cursor

Antigravity activates automatically. Skills load on startup.

### Step 3 — Run the onboarding prompt

Copy the content of [[PROMPT_ONBOARD_TEAM]] and paste it into your Antigravity chat.

Your bot then does three things automatically:

1. **Reads the entire system** — MASTER_PLAN_FINAL, this file, _RULES, all skills
2. **Scans your history** — which projects, tools, and experiences you have
3. **Writes a report** to `obsidian/_users/[your-name].md`

William reads the report → we discuss → roles are finalized.

> [!warning] Important detail
> The report is written by **your** bot about **you**. That's intentional.
> Your bot knows your projects, your strengths, and your blind spots better than you do.
> Trust it.

---

## 5. Business model (hypothesis)

```
AUDIT ──→ BUILD ──→ OPERATE
```

| Phase | Price (prototype) | What's included |
|-----|-----------------|-----------|
| **Audit** | 19,900 SEK | Mapping of IT workflows + structured report |
| **Build** | 99,000–300,000 SEK | Agents built + dashboard delivered |
| **Operate** | 4,900–19,900 SEK/month | Operations, updates, support, new automation |

> [!caution] These numbers are untested
> No customer has paid yet. Pricing will be adjusted after the first 5 leads.
> No one on the team should cite these numbers externally without checking with William.

---

## 6. The team (hypothesis)

| Person | Intended role | Confirmed? |
|--------|-----------|------------|
| **William** | Founder · Builder · Everything | William builds everything solo (decided 2026-06-24) |
| **Alpedal** | Solutions Architect · Audits | Hypothesis — determined via onboarding |

The onboarding reports determine the roles. Nothing is predetermined.

---

## 7. Decisions that apply (can be renegotiated)

| Decision | Applies until... |
|--------|----------------|
| `skills/` at root level | Someone has a concretely better structure |
| `ca-` prefix for skills | It creates confusion |
| Everyone runs VSCode + Antigravity + Hermes CLI | Everyone's setup supports it — locked in |
| Next.js + Tailwind for dashboard | Decided — finalized |
| William = GDPR responsible | Another person formally takes responsibility |

> [!note] How to renegotiate a decision
> Write a proposal under `## Comments` in the relevant document with date and author tag.
> We discuss — no one changes without consensus.

---

## 8. What remains

Before we can take the first customer:

- [x] William builds everything solo (decided 2026-06-24, see BUILD_PHASE_2)
- [ ] Run [[PROMPT_ONBOARD_TEAM]] — get Alpedal's onboarding report
- [ ] Analyze the reports — adjust roles and plan
- [ ] Land first customer — test the entire hypothesis against reality
- [ ] Iterate — everything is prototype until proven otherwise

---

## Comments

- 2026-06-24 | william: Foundation document. Everything is prototype. Alpedal's report determines the next step.
- 2026-06-24 | hermes: Restructured for onboarding — clearer steps, Obsidian callouts, wikilinks.
- 2026-06-24 | william: William's role is also a hypothesis. Sales is not locked in. Tech setup (VSCode + Antigravity + Hermes CLI) is locked in — everyone's setup supports it.

---
*Translation note: This file was translated from Swedish to English on 2025-06-25.*
