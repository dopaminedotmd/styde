---
name: ca-file-organizer
description: Styr var nya filer ska placeras och kontrollerar namngivningskonventioner (stora bokstäver med understreck) och katalogdjup (max 3 nivåer). Använd denna skill så fort en ny fil ska skapas eller flyttas.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-file-organizer

## Purpose

Controls where new files should be placed and ensures that naming conventions and depth restrictions are followed.

## Rules

### 1. Naming Convention
All new files must be named with uppercase letters and underscores instead of spaces:
`UPPERCASE_LETTERS_with_underscores.md`

### 2. Depth Restriction
Files may be saved at most 3 levels deep in the directory structure.

### 3. Never Delete Files
Never permanently delete or purge files. Old or outdated files should be archived by updating their frontmatter to:
`status: archived` and tag `status/ARCHIVED`

### 4. Mapping (document type → folder)

| Document Type | Folder |
|-----------------|------|
| Bot rules, tags, formats | `_RULES.md` |
| Main index for the planning hub | `INDEX.md` |
| Person profiles for the team | `_users/` |
| Templates for plans, meetings | `_templates/` |
| Obsidian-specific skills | `_skills/` |
| Strategy, business concept, market | `00_strategy/` |
| Plans, roadmaps, sprints | `01_plan/` |
| Architecture, specs, technical decisions | `02_architecture/` |
| Prototypes, mockups, code sketches | `03_prototypes/` |
| Client work, templates | `04_clients/` |
| Operations, subscription, processes | `05_ops/` |
| Research, links, inspiration | `99_references/` |

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
