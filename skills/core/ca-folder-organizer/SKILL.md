---
name: ca-folder-organizer
description: Hanterar katalogstrukturen i repot och förhindrar att odefinierade mappar skapas. Kontrollera alltid denna skill innan en ny mapp skapas eller vid strukturering av projektet.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-folder-organizer

## Purpose

Manages the directory structure and prevents the creation of unauthorized folders.

## Rules

### 1. No Undefined Folders
Never create folders outside the defined structure without prior team consensus.

### 2. Create a New Category
If a new category of documents or folders is needed, a plan must first be created and approved in `01_plan/` (or by updating `ROADMAP.md`).

### 3. Do Not Delete Empty Folders
Never delete empty folders in the repo. They are predefined and have a specific purpose for future phases (e.g., `03_prototypes/` or `04_clients/_active/`).

### 4. Allowed Directory Structure

```
consulting.ai/
│
├── .agents/
│   ├── AGENTS.md
│   ├── skills.json
│   └── skills/
│
├── skills/
│   ├── SKILLS_INDEX.md
│   ├── core/
│   ├── planning/
│   ├── delivery/
│   └── reusable/
│
├── agents/
│   ├── templates/
│   └── deployed/
│
└── obsidian/
    ├── _RULES.md
    ├── _skills/
    ├── _users/
    ├── 00_strategy/
    ├── 01_plan/
    ├── 02_architecture/
    ├── 03_prototypes/
    ├── 04_clients/
    └── 05_ops/
```

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
