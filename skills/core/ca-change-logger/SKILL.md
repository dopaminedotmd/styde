---
name: ca-change-logger
description: Loggar alla ändringar i styde-repot. Använd denna skill efter varje genomförd åtgärd (skapat fil, ändrat fil, godkänt planer etc.) för att uppdatera dagens logg i obsidian/05_ops/logs/.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-change-logger

## Purpose

All changes in styde are logged traceably. Every bot writes a log after every completed action.
This allows William, Alpedal, and future bots to always see who did what and when.

## Log Location

All logs are written to:

```
obsidian/05_ops/logs/{YYYY-MM-DD}.md
```

One file per day. Created automatically by the first bot that logs that day.
obsidian/05_ops/logs/_INDEX.md contains the register of all log files.

## Format

Each log entry is a bullet point in reverse chronological order (newest first):

```
- HH:MM | author: Short description of what was done
```

Example:

```
- 14:32 | hermes: Created BUILD_PHASE_2.md with agent flow, security, and dashboard spec
- 14:15 | william: Approved the proposal, adjusted team structure
- 13:50 | alpedal: Wrote onboarding report
```

## When to Log

You ALWAYS log after:

| Action | Log |
|--------|-------|
| Create a new file (plan, skill, report) | `Created {filename} — {brief description of what it does}` |
| Modify an existing file | `Updated {filename} — {what changed}` |
| Archive/remove content | `Archived {filename} — {reason}` |
| Create a new folder | `Created folder {folder}/` |
| Approve/approve a document | `Approved {document} — {change}` |
| Build a test client | `Built {customer}/ — {agents}` |
| Perform an audit | `Performed audit {customer} — {result}` |

You do NOT log:
- That you read a file (reading is not a change)
- That you searched for something
- That you wrote a log entry (that creates a circular log)
- Small temporary operations (e.g., "read a line to understand")

## Order

1. Make the change
2. Open today's log file (create if it doesn't exist)
3. Add your log entry FIRST (newest first)
4. Save

## If the File Doesn't Exist

Create `obsidian/05_ops/logs/{YYYY-MM-DD}.md` with frontmatter:

```yaml
---
title: "Change Log — {YYYY-MM-DD}"
date: {YYYY-MM-DD}
author: {yours}
tags: [area/OPS, status/APPROVED, author/{YOURS}, type/REPORT]
status: approved
---

# Change Log — {YYYY-MM-DD}

> Changes in styde on this day.

```

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
