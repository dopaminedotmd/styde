---
title: "_README — skills/"
date: 2026-06-24
author: hermes
tags: [area/OPS, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# _README — skills/

> This is styde's internal toolbox.
> Everything here is used by our bots to run the company — plan, build, deliver.
> Nothing here leaks to the customer.

---

## What Is a Skill?

A skill is an instruction file (SKILL.md) that tells a bot HOW to perform a certain type of task. When a bot gets a task that matches a skill's description — the bot reads the skill and follows the instructions.

Think: a manual for your bot. Instead of you writing the same instruction every time, you write it once in a skill.

---

## Structure

```
skills/
├── SKILLS_INDEX.md       ← Registry of all skills (bots read this first)
├── core/                 ← Internal OS — core functions always used
│   ├── ca-brainstorming/     ← Enforces design-first before building
│   ├── ca-change-logger/     ← Logs all changes in the repo
│   ├── ca-file-organizer/    ← Controls where files are placed
│   ├── ca-folder-organizer/  ← Keeps folder structure clean
│   └── ca-rules-enforcer/    ← Flags rule violations
├── planning/             ← Our planning and prioritization
│   ├── ca-plan-creator/      ← Creates plans according to template
│   └── ca-plan-reviewer/     ← Reviews plans against standard
└── delivery/             ← Our delivery process — audit → build → deploy
    ├── ca-agent-builder/     ← Builds AI agents for customers (generates agents/)
    ├── ca-audit-agent/       ← Conducts customer audits
    ├── ca-audit-reporter/    ← Writes audit reports
    ├── ca-offert-writer/     ← Writes quotes
    └── ca-onboarding-lead/   ← Guides the customer from contract to go-live
```

Each skill is a folder with a SKILL.md plus optional support files (scripts/, references/, resources/).

---

## Skill Naming Convention

All our skills start with `ca-` (styde).

| Prefix | Example | Meaning |
|--------|---------|-----------|
| `ca-` | ca-brainstorming | styde — internal skill |
| (external) | obsidian-markdown | From addyosmani/kepano — installed in .agents/skills/ |

The `ca-` prefix ensures our skills never collide with external skills.

---

## How Skills Are Used (for humans)

### If You're New
1. Browse SKILLS_INDEX.md — see what's available
2. Read the SKILL.md of the skill you're interested in
3. Ask your bot to do something — the bot finds the right skill on its own

### If You're Creating a New Skill
1. Decide the category (core/planning/delivery — see above)
2. Create a folder: `skills/{category}/ca-your-new-skill/`
3. Create SKILL.md with frontmatter (name, description, version, owner, last-updated)
4. Register in SKILLS_INDEX.md — add a row to the table
5. Done. Bots find it automatically via discovery.

### If You're Updating a Skill
1. Modify SKILL.md
2. Bump the version in frontmatter
3. Update last-updated
4. Log the change in obsidian/05_ops/logs/

---

## Skill Format

Every SKILL.md has YAML frontmatter:

```yaml
---
name: ca-example
description: Short description that bots match against
version: 1.0.0
owner: william
last-updated: 2026-06-24
---
```

Then comes the instructions in markdown. Write for your bot — short, clear, step-by-step.

---

## Skill vs Agent — Important Difference

| | skills/ | agents/ |
|---|---------|---------|
| **What** | Our tools | Customer's agents |
| **Language** | Ours (Swedish, ca-prefix, Hermes) | Customer's (sterile, professional) |
| **Who uses** | Our bots | The customer |
| **Content** | Instructions to bots | prompt.md + tools.yaml + config.yaml |
| **Seen by customer** | No | Yes |

`skills/delivery/ca-agent-builder` is the bridge — it's our skill but generates content in `agents/`.

---

## Discovery — How Bots Find Skills

1. `.agents/AGENTS.md` points the bot to obsidian/_RULES.md
2. `.agents/skills.json` lists the skills/ categories
3. The bot reads SKILLS_INDEX.md — sees all skills with name + description
4. When a task matches a skill's description → the bot loads the full SKILL.md
5. The bot follows the instructions

This is called progressive loading — the bot only sees headers until it needs the details. Saves token space.

---

## FAQ

**Why can't I just put everything in one folder?**
Because bots need to find the right skill quickly. Categories (core/planning/delivery) make discovery faster and clearer.

**Can a skill reference another skill?**
Yes. Use wikilinks: `[[ca-brainstorming]]`. The bot reads the linked skill when needed.

**What happens if two skills have similar descriptions?**
The bot picks the one with the most specific description. If both match equally well — the bot asks you.

**Can I write a skill in English?**
No. All skills are in Swedish. That's our working language.

---

## Comments

- 2026-06-24 | hermes: Created. Describes the skill system for human team members.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged. Note: the FAQ entry "Can I write a skill in English? No. All skills are in Swedish." has been preserved as-is since it reflects a policy decision that may have changed with this translation.
