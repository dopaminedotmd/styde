---
title: "_RULES — Bot-regler för styde"
date: 2026-06-24
author: william
tags: [area/STRATEGI, status/APPROVED, author/WILLIAM, type/TEMPLATE]
status: approved
---

# _RULES.md — Bot Rules for styde

> [!important] Read first
> ALL bots read this first before they write, create, or change anything.
> Reviewed and approved in [[MASTER_PLAN_FINAL]].
> Last updated: 2026-06-24

## 1. Mandatory frontmatter (YAML)

Every document must start with:

```yaml
---
title: "Kort beskrivande titel"
date: 2026-06-24
author: william | alpedal | hermes
tags: [area/*, status/*, author/*, type/*]
status: draft | review | approved | archived
---
```

## 2. Tag system

### Area (area/)

| Tag | When |
|------|-----|
| `area/STRATEGI` | Business, pricing, offer |
| `area/PLAN` | Roadmaps, phases, sprints |
| `area/ARKITEKTUR` | System, dashboard, agent spec |
| `area/KLIENT` | Client work, templates |
| `area/OPS` | Operations, subscription, onboarding |
| `area/REFERENS` | Research, links |

### Status (status/)

| Tag | When |
|------|------|
| `status/DRAFT` | Draft, not finished |
| `status/REVIEW` | Ready for review |
| `status/APPROVED` | Approved, can be used |
| `status/ARCHIVED` | Old, replaced |

### Author (author/)

| Tag | Who |
|------|-----|
|| `author/WILLIAM` | William |
|| `author/ALPEDAL` | Alpedal |
|| `author/HERMES` | Hermes (William's AI) |

### Type (type/)

| Tag | What |
|------|-----|
| `type/CONCEPT` | Idea, concept, brain-dump |
| `type/PLAN` | Planning, roadmap |
| `type/REPORT` | Report, audit, analysis |
| `type/SPEC` | Specification, requirements |
| `type/TEMPLATE` | Template for reuse |

## 3. Document structure

```
---
[frontmatter]
---

# Title

> Short description (1-2 sentences)

## Section 1
Content...

### Subsection
Content...

## Section 2
...

## Comments
- 2026-06-24 | william: first draft
- 2026-06-25 | william: looks good
```

- H1 `#` for title. H2 `##` for sections. H3 `###` for subsections.
- No deeper than H3.
- Tables for structured data. Lists for steps/items.

## 4. Writing standard

- **Swedish.** Always.
- **Concise.** No filler.
- **No emojis.** Zero.
- **Facts first.** One sentence about what the document contains, then details.

## 5. File structure — where things go

| Document type | Folder |
|-----------------|------|
| Bot rules, tags, format | `_RULES.md` |
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

## 6. Comments in documents

All documents have a `## Comments` section at the bottom.
Write your thoughts there with the format:

```
- YYYY-MM-DD | author: comment here
```

## 7. Security rules for bots

- NEVER change anyone else's document without commenting first
- NEVER delete — mark as `status/ARCHIVED` instead
- If unsure: write under `## Comments` and ask
- All suggestions must be traceable (author tag + date)

## 8. When you create a new document

1. Use the template in `_templates/PLAN_TEMPLATE.md`
2. Fill in frontmatter with correct tags
3. Write concisely and structured
4. Add a `## Comments` section last
5. Place the file in the correct folder according to §5

## 9. Systemarkitektur

Fullständig arkitektur: se [[MASTER_PLAN]].

I korthet:
- `skills/` — våra interna ca-skills (core, planning, delivery, reusable)
- `.agents/skills/` — externa skills (addyosmani, kepano)
- `.agents/skills.json` — registrerar subkataloger i `skills/`
- `.agents/AGENTS.md` — pekar hit

## 10. Loggning — alla ändringar loggas

Alla botar måste logga sina ändringar enligt [[ca-change-logger]].
Loggar skrivs till `obsidian/05_ops/logs/{YYYY-MM-DD}.md`.

Läs [[ca-change-logger]] för instruktioner om format och när du ska logga.

## 11. Server-först-principen

- All kod, utveckling och databaser körs på vår delade fysiska server (se [[SERVER_SETUP]]).
- William och Alpedal utvecklar direkt på servern via SSH (VS Code Remote).
- Next.js dashboard och Express runtime körs lokalt på servern.
- Cloudflare Tunnel används för att exponera tjänster mot webben när så behövs. Inga onödiga molnresurser skapas.

## 12. Sprintsystemet (ADHD-vänligt)

- Vi arbetar i sprintar om max 3 dagar och max 3 uppgifter per sprint.
- Aktiv sprint definieras i [[SPRINT_CURRENT]].
- Nya idéer placeras alltid under backlog/idéer i sprintdokumentet och får aldrig läggas till i pågående sprint utan godkännande.
- Botar får INTE föreslå arbete eller skriva kod utanför den aktiva sprintens omfattning.

## Comments

- 2026-06-24 | hermes: Updated after MASTER_PLAN_FINAL. Added §9 (system architecture reference).
- 2026-06-24 | hermes: Restructured according to Obsidian standard, added wikilinks and callouts.
- 2026-06-25 | hermes: Uppdaterat §9 med nya plan-länkar samt lagt till §11 (Server) och §12 (Sprints) i samband med total reboot.

---
*Translation note: This file was translated from Swedish to English on 2025-06-25.*
