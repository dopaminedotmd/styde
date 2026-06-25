---
title: "_RULES — Bot-regler för styde"
date: 2026-06-24
author: william
tags: [area/STRATEGI, status/APPROVED, author/WILLIAM, type/TEMPLATE]
status: approved
---

# _RULES.md — Bot-regler för styde

> [!important] Läs först
> ALLA bottar läser detta först innan de skriver, skapar eller ändrar något.
> Granskad och godkänd i [[MASTER_PLAN_FINAL]].
> Senast uppdaterad: 2026-06-24

## 1. Obligatorisk frontmatter (YAML)

Varje dokument måste starta med:

```yaml
---
title: "Kort beskrivande titel"
date: 2026-06-24
author: william | alpedal | hermes
tags: [area/*, status/*, author/*, type/*]
status: draft | review | approved | archived
---
```

## 2. Taggsystem

### Område (area/)

| Tagg | När |
|------|-----|
| `area/STRATEGI` | Business, pricing, offer |
| `area/PLAN` | Roadmaps, faser, sprintar |
| `area/ARKITEKTUR` | System, dashboard, agent-spec |
| `area/KLIENT` | Kundarbete, mallar |
| `area/OPS` | Drift, subscription, onboarding |
| `area/REFERENS` | Research, länkar |

### Status (status/)

| Tagg | När |
|------|------|
| `status/DRAFT` | Utkast, inte färdigt |
| `status/REVIEW` | Klart för granskning |
| `status/APPROVED` | Godkänt, kan användas |
| `status/ARCHIVED` | Gammalt, ersatt |

### Författare (author/)

| Tagg | Vem |
|------|-----|
|| `author/WILLIAM` | William |
|| `author/ALPEDAL` | Alpedal |
|| `author/HERMES` | Hermes (William's AI) |

### Typ (type/)

| Tagg | Vad |
|------|-----|
| `type/CONCEPT` | Idé, koncept, brain-dump |
| `type/PLAN` | Planering, roadmap |
| `type/REPORT` | Rapport, audit, analys |
| `type/SPEC` | Specifikation, krav |
| `type/TEMPLATE` | Mall för återanvändning |

## 3. Dokumentstruktur

```
---
[frontmatter]
---

# Titel

> Kort beskrivning (1-2 meningar)

## Sektion 1
Innehåll...

### Undersektion
Innehåll...

## Sektion 2
...

## Kommentarer
- 2026-06-24 | william: första utkastet
- 2026-06-25 | william: ser bra ut
```

- H1 `#` för titel. H2 `##` för sektioner. H3 `###` för undersektioner.
- Inget djupare än H3.
- Tabeller för strukturerad data. Listor för steg/items.

## 4. Skrivstandard

- **Svenska.** Alltid.
- **Kortfattat.** Ingen utfyllnad.
- **Inga emojis.** Noll.
- **Fakta först.** En mening om vad dokumentet innehåller, sen detaljer.

## 5. Filstruktur — var saker läggs

| Typ av dokument | Mapp |
|-----------------|------|
| Bot-regler, taggar, format | `_RULES.md` |
| Huvudindex för planeringshubben | `INDEX.md` |
| Personprofiler för teamet | `_USERS/` |
| Mallar för planer, möten | `_TEMPLATES/` |
| Obsidian-specifika skills | `_SKILLS/` |
| Strategi, business concept, marknad | `00_STRATEGY/` |
| Planer, roadmaps, sprintar | `01_PLAN/` |
| Arkitektur, specar, tekniska beslut | `02_ARCHITECTURE/` |
| Prototyper, mockups, kod-sketcher | `03_PROTOTYPES/` |
| Kundarbete, mallar | `04_CLIENTS/` |
| Drift, subscription, processer | `05_OPS/` |
| Research, länkar, inspiration | `99_REFERENCES/` |

## 6. Kommentarer i dokument

Alla dokument har en `## Kommentarer`-sektion längst ner.
Skriv in dina tankar där med format:

```
- YYYY-MM-DD | författare: kommentaren här
```

## 7. Säkerhetsregler för bottar

- Ändra ALDRIG någon annans dokument utan att kommentera först
- Radera ALDRIG — markera som `status/ARCHIVED` istället
- Om osäker: skriv under `## Kommentarer` och fråga
- Alla förslag ska vara spårbara (author-tagg + datum)

## 8. När du skapar ett nytt dokument

1. Använd mallen i `_TEMPLATES/PLAN_TEMPLATE.md`
2. Fyll i frontmatter med rätt taggar
3. Skriv kort och strukturerat
4. Lägg till en `## Kommentarer`-sektion sist
5. Lägg filen i rätt mapp enligt §5

## 9. Systemarkitektur

Fullständig arkitektur: se [[MASTER_PLAN_FINAL]] (rotnivå).

Kortfattat:
- `skills/` — våra interna ca-skills (core, planning, delivery, reusable)
- `.agents/skills/` — externa skills (addyosmani, kepano)
- `.agents/skills.json` — registrerar `skills/`-undermappar
- `.agents/AGENTS.md` — pekar hit

## 10. Logging — alla ändringar loggas

Alla bottar måste logga sina ändringar enligt [[ca-change-logger]].
Loggarna skrivs till `OBSIDIAN/05_OPS/LOGS/{YYYY-MM-DD}.md`.

Läs [[ca-change-logger]] för fulla instruktioner om format och när du loggar.

## Kommentarer

- 2026-06-24 | hermes: Uppdaterad efter MASTER_PLAN_FINAL. Lade till §9 (systemarkitektur-referens).
- 2026-06-24 | hermes: Omstrukturerat enligt Obsidian-standard, lagt till wikilinks och callouts.
