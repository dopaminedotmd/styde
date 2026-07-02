---
title: "SKILLS_INDEX — Index of skills in styde"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# Skills Index — styde

| Skill | Category | Owner | Version | Description |
|-------|----------|-------|---------|-------------|
| [[ca-brainstorming\|ca-brainstorming]] | planning | william | 2.1.0 | Must be used before any form of coding, project scaffolding, or implementation. Enforces design-first and mini-spec that must be approved by William before code is written. |
| [[skill-creator\|skill-creator]] | external | anthropic | 1.0.0 | Create, modify and improve skills with eval-driven iteration and benchmarking. S-rank. |
| [[brainstorming\|brainstorming]] | external | obra | 1.0.0 | 9-step design-before-code process with visual companion, spec-review and HARD-GATE. S-rank. |
| [[ca-file-organizer\|ca-file-organizer]] | core | william | 1.1.0 | Controls where new files should be placed and checks naming conventions (uppercase with underscores) and directory depth (max 3 levels). |
| [[ca-folder-organizer\|ca-folder-organizer]] | core | william | 1.1.0 | Manages the directory structure in the repo and prevents undefined folders from being created. |
| [[ca-rules-enforcer\|ca-rules-enforcer]] | core | william | 1.1.0 | Flags violations of repo rules (wrong folder, wrong frontmatter, missing comments). Logs deviations and adds comments under ## Comments. |
| [[ca-plan-creator\|ca-plan-creator]] | planning | william | 1.1.0 | Creates new implementation plans from PLAN_TEMPLATE.md. Ensures correct frontmatter, tags, and structure in obsidian/01_plan/. |
| [[ca-plan-reviewer\|ca-plan-reviewer]] | planning | william | 1.1.0 | Reviews planning documents against repo rules and checklist before implementation. Validates frontmatter, tags, and comments section. |
| [[ca-agent-builder\|ca-agent-builder]] | delivery | william | 1.1.0 | Standard and template for building and deploying AI agent systems for customers (prompt.md, tools.yaml, config.yaml). |
| [[ca-audit-agent\|ca-audit-agent]] | delivery | alpedal | 1.1.0 | Conducts customer audits to map IT flows, systems, costs, and identify automation opportunities. |
| [[ca-audit-reporter\|ca-audit-reporter]] | delivery | alpedal | 1.1.0 | Writes structured and actionable audit reports in obsidian/04_clients/_active/ from AUDIT_TEMPLATE.md. |
| [[ca-offert-writer\|ca-offert-writer]] | delivery | william | 1.1.0 | Creates formal quotes in obsidian/04_clients/_active/ from OFFERT_TEMPLATE.md. Follows pricing rules for Audit, Build, and Operate (SLA levels). |
| [[ca-onboarding-lead\|ca-onboarding-lead]] | delivery | william | 1.1.0 | Guides the customer step-by-step through the onboarding process, from kickoff and dashboard setup to agent deployment, training, and go-live. |
| [[ca-change-logger\|ca-change-logger]] | core | william | 1.1.0 | Logs all changes in the styde repo. Updates the daily log in obsidian/05_ops/logs/ after every completed action. |

## Comments

- 2026-06-25 | hermes: Added frontmatter, updated all skill descriptions to Swedish, bumped versions for the updated internal skills, and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged. Column header "Beskrivning" was changed to "Description".
