---
name: ca-plan-creator
description: Skapar nya implementationsplaner utifrån PLAN_TEMPLATE.md. Säkerställer korrekt frontmatter, taggar och struktur i obsidian/01_plan/. Använd denna skill när en ny implementationsplan ska initieras.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-plan-creator

## Purpose

Creates new planning documents using the `PLAN_TEMPLATE.md` template and validates structure and metadata at creation time.

## Creation Instructions

1. **Read the template:** Use the content of [[PLAN_TEMPLATE]] (`obsidian/_templates/PLAN_TEMPLATE.md`) as the base for the new document.
2. **Define required frontmatter:**
   - Fill in `title` with a short descriptive heading.
   - Set `date` to today's date (format YYYY-MM-DD).
   - Set `author` to the name of the agent/person creating the plan.
   - Set `status: draft`.
3. **Fill in tags according to [[_RULES]] §2:**
   - Every plan must contain tags in the format `tags: [area/PLAN, status/DRAFT, author/*, type/PLAN]` where the author (`author/*`) is adapted.
4. **Structure sections:** Fill in Goal, Background, Step-by-Step, Timeline, Resources, and Risks.
5. **Create comments section:** Add a `## Comments` section at the very end of the document with the format `- YYYY-MM-DD | author: created`.
6. **Placement:** Save the file in the directory `obsidian/01_plan/` (according to rules in [[ca-file-organizer]]).

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
