---
name: ca-rules-enforcer
description: Flaggar för överträdelser av repo-regler (fel mapp, fel frontmatter, saknade kommentarer). Loggar avvikelser och lägger till kommentarer under ## Kommentarer utan att blockera körningen. Körs före granskning.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-rules-enforcer

## Purpose

Flags violations of established repo rules. It does not block execution, but logs deviations and comments.

## Checks Performed

1. **Wrong folder:** Checks if a document has been placed in a directory that does not match its document type (according to [[ca-file-organizer]]).
2. **Wrong frontmatter:** Validates that the YAML frontmatter contains all required fields based on file type:
   - For documents in `obsidian/`: `title`, `date`, `author`, `tags`, `status` (according to [[_RULES]]).
   - For skills in `skills/`: `name`, `description`, `version`, `owner`, `last-updated` (according to [[_README]] under `skills/`).
3. **Wrong tags:** Verifies that tags follow the defined system (`[area/*, status/*, author/*, type/*]`) according to [[_RULES]] (applies only to documents in `obsidian/`).
4. **Missing comments section:** Checks that the file has a `## Comments` section at the very bottom.

## Actions on Rule Violation

- Write a comment under the `## Comments` section in the affected document with a specific description of the rule violation.
- Notify the owner (e.g., William or Hermes) by clearly logging the deviation in the bot's execution report.
- **Do NOT block:** The agent is allowed to continue its work even if it contains rule violations. Review and blocking happen in the `ca-plan-reviewer` step.

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0, adjusted frontmatter validation to support skills separately, and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
