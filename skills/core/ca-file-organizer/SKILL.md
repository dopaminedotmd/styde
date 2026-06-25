---
name: ca-file-organizer
description: Styr var nya filer ska placeras och kontrollerar namngivningskonventioner (stora bokstäver med understreck) och katalogdjup (max 3 nivåer). Använd denna skill så fort en ny fil ska skapas eller flyttas.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-file-organizer

## Syfte

Kontrollerar var nya filer ska placeras samt ser till att namngivningskonventioner och djupbegränsningar följs.

## Regler

### 1. Namnkonvention
Alla nya filer ska namnges med stora bokstäver och understreck (underscore) istället för mellanslag:
`STORA_BOKSTÄVER_med_underscore.md`

### 2. Djupbegränsning
Filer får sparas maximalt 3 nivåer djupt i katalogstrukturen.

### 3. Ta aldrig bort filer
Radera eller rensa aldrig filer permanent. Gamla eller inaktuella filer ska arkiveras genom att uppdaterar deras frontmatter till:
`status: archived` och tagg `status/ARCHIVED`

### 4. Mappning (dokumenttyp → mapp)

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

## Kommentarer

- 2026-06-25 | hermes: Uppdaterade beskrivningen till svenska, bumpade version till 1.1.0 och lade till kommentarssektion.

