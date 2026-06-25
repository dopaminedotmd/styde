---
title: "_README — skills/"
date: 2026-06-24
author: hermes
tags: [area/OPS, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# _README — skills/

> Detta är styde:s interna verktygslåda.
> Allt här används av våra bottar för att driva företaget — planera, bygga, leverera.
> Ingenting här läcker till kund.

---

## Vad är en skill?

En skill är en instruktionsfil (SKILL.md) som talar om för en bot HUR den ska utföra en viss typ av uppgift. När en bot får en uppgift som matchar en skills beskrivning — läser boten skillen och följer instruktionerna.

Tänk: en manual för din bot. Istället för att du skriver samma instruktion varje gång, skriver du den en gång i en skill.

---

## Struktur

```
skills/
├── SKILLS_INDEX.md       ← Register över alla skills (botar läser detta först)
├── core/                 ← Internt OS — grundfunktioner som alltid används
│   ├── ca-brainstorming/     ← Tvingar design-first före bygge
│   ├── ca-change-logger/     ← Loggar alla ändringar i repot
│   ├── ca-file-organizer/    ← Styr var filer läggs
│   ├── ca-folder-organizer/  ← Håller mappstruktur ren
│   └── ca-rules-enforcer/    ← Flaggar brott mot regler
├── planning/             ← Vår planering och prioritering
│   ├── ca-plan-creator/      ← Skapar planer enligt mall
│   └── ca-plan-reviewer/     ← Granskar planer mot standard
└── delivery/             ← Vår leveransprocess — audit → bygg → driftsätt
    ├── ca-agent-builder/     ← Bygger AI-agenter åt kunder (genererar agents/)
    ├── ca-audit-agent/       ← Genomför kundaudits
    ├── ca-audit-reporter/    ← Skriver audit-rapporter
    ├── ca-offert-writer/     ← Skriver offerter
    └── ca-onboarding-lead/   ← Guidar kunden från kontrakt till go-live
```

Varje skill är en mapp med ett SKILL.md plus eventuella stödfiler (scripts/, references/, resources/).

---

## Skill-namnkonvention

Alla våra skills börjar med `ca-` (styde).

| Prefix | Exempel | Betydelse |
|--------|---------|-----------|
| `ca-` | ca-brainstorming | styde — intern skill |
| (externa) | obsidian-markdown | Från addyosmani/kepano — installeras i .agents/skills/ |

`ca-` prefixet gör att våra skills aldrig kolliderar med externa skills.

---

## Hur skills används (för människor)

### För dig som är ny
1. Bläddra i SKILLS_INDEX.md — se vad som finns
2. Läs SKILL.md i den skill du är intresserad av
3. Be din bot göra något — boten hittar rätt skill själv

### För dig som skapar en ny skill
1. Bestäm kategori (core/planning/delivery — se ovan)
2. Skapa en mapp: `skills/{kategori}/ca-din-nya-skill/`
3. Skapa SKILL.md med frontmatter (name, description, version, owner, last-updated)
4. Registrera i SKILLS_INDEX.md — lägg till en rad i tabellen
5. Done. Botar hittar den automatiskt via discovery.

### För dig som uppdaterar en skill
1. Ändra SKILL.md
2. Bumpa version i frontmatter
3. Uppdatera last-updated
4. Logga ändringen i OBSIDIAN/05_OPS/LOGS/

---

## Skill-format

Varje SKILL.md har YAML-frontmatter:

```yaml
---
name: ca-exempel
description: Kort beskrivning som botar matchar mot
version: 1.0.0
owner: william
last-updated: 2026-06-24
---
```

Sen kommer instruktionerna i markdown. Skriv för din bot — kort, tydligt, steg-för-steg.

---

## Skill vs Agent — viktig skillnad

| | skills/ | agents/ |
|---|---------|---------|
| **Vad** | Våra verktyg | Kundens agenter |
| **Språk** | Vårt (svenska, ca-prefix, Hermes) | Kundens (sterilt, professionellt) |
| **Vem använder** | Våra bottar | Kunden |
| **Innehåll** | Instruktioner till bottar | prompt.md + tools.yaml + config.yaml |
| **Syns av kund** | Nej | Ja |

`skills/delivery/ca-agent-builder` är bryggan — den är vår skill men genererar innehåll i `agents/`.

---

## Discovery — hur botar hittar skills

1. `.agents/AGENTS.md` pekar boten till OBSIDIAN/_RULES.md
2. `.agents/skills.json` listar skills/-kategorierna
3. Boten läser SKILLS_INDEX.md — ser alla skills med name + description
4. När en uppgift matchar en skills description → boten laddar hela SKILL.md
5. Boten följer instruktionerna

Detta kallas progressiv inläsning — boten ser bara rubriker tills den behöver detaljerna. Sparar tokenutrymme.

---

## FAQ

**Varför kan jag inte bara lägga allt i en mapp?**
För att botar måste hitta rätt skill snabbt. Kategorier (core/planning/delivery) gör discovery snabbare och tydligare.

**Kan en skill referera till en annan skill?**
Ja. Använd wikilinks: `[[ca-brainstorming]]`. Boten läser den länkade skillen vid behov.

**Vad händer om två skills har liknande beskrivning?**
Boten väljer den med mest specifik beskrivning. Om båda matchar lika bra — boten frågar dig.

**Kan jag skriva en skill på engelska?**
Nej. Alla skills är på svenska. Det är vårt arbetsspråk.

---

## Kommentarer

- 2026-06-24 | hermes: Skapad. Beskriver skill-systemet för mänskliga teammedlemmar.
