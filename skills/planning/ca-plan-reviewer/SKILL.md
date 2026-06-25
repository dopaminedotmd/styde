---
name: ca-plan-reviewer
description: Granskar planeringsdokument mot repo-regler och checklista före implementering. Validerar frontmatter, taggar, kommentarssektion och letar efter placeholders (TBD, TODO).
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-plan-reviewer

## Purpose

Reviews planning documents against established repo rules and ensures quality before implementation begins.

## Review Checklist

1. **Frontmatter OK?**
   - Does it contain title, date, author, tags, and status?
2. **Tags correct?**
   - Do they follow the structure `[area/*, status/*, author/*, type/*]` according to [[_RULES]]?
3. **Folder correct?**
   - Is the file saved in the correct subdirectory according to [[ca-file-organizer]]?
4. **Comments section present?**
   - Does the section `## Comments` exist at the very bottom of the document?
5. **No placeholders?**
   - Are there any text passages containing temporary markers such as "TBD", "TODO", "implement later", or similar?

## Actions on Result

### If the review fails (deviations found)
- Write a comment under the `## Comments` section in the document with specific feedback on what needs to be addressed.
- Set the document's status to `status: draft`.

### If the review passes (no deviations)
- Update the document's status to `status: review` (and tag to `status/REVIEW`).
- Log the approval in the comments: `- YYYY-MM-DD | author: reviewed and approved for review`.

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
