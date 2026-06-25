# Prompt — AgY CLI: Genomför REORG_01

> Du ska utföra omorganisationen i styde enligt OBSIDIAN/01_PLAN/REORG_01.md.
> Läs den planen först. Denna prompt specificerar EXAKT vad som ska göras.

## Läs först (i denna ordning)

1. OBSIDIAN/_RULES.md — taggar, frontmatter, kommentarer
2. skills/SKILLS_INDEX.md — nuvarande skill-lista
3. .agents/skills.json — nuvarande discovery-config
4. OBSIDIAN/01_PLAN/REORG_01.md — hela planen
5. OBSIDIAN/01_PLAN/BUILD_PHASE_2.md — för kontext (behöver inte agera på den)
6. OBSIDIAN/INDEX.md — för att hitta rätt wikilänkar
7. OBSIDIAN/02_ARCHITECTURE/SYSTEM_OVERVIEW.md — för att uppdatera wikilänkar i arkitekturdokument

## Steg 1: Omdöp client-work → delivery

Flytta katalogen:
```
mv skills/client-work skills/delivery
```

Uppdatera .agents/skills.json: ändra `"../skills/client-work"` till `"../skills/delivery"`

Uppdatera följande filer som wikilänkar till `client-work/`:
- OBSIDIAN/INDEX.md: ändra `client-work` → `delivery` i beskrivning och ansvar
- skills/SKILLS_INDEX.md: ändra kategori `client-work` → `delivery` för alla ca-audit-*, ca-offert-*, ca-onboarding-* skills
- Alla SKILL.md-filer i skills/delivery/ som refererar till `client-work` internt (finns troligen inga, men sök)

Verifiera:
```
ls skills/delivery/
```
Ska visa: ca-agent-builder, ca-audit-agent, ca-audit-reporter, ca-offert-writer, ca-onboarding-lead

## Steg 2: Slå ihop building/ → delivery/

Flytta ca-agent-builder:
```
mv skills/building/ca-agent-builder skills/delivery/ca-agent-builder
```

Ta bort den tomma building/-mappen:
```
rmdir skills/building
```

Uppdatera .agents/skills.json: ta bort `"../skills/building"` från entries-listan

Uppdatera skills/SKILLS_INDEX.md: ta bort raden för building-kategorin (finns ingen kategorirad, men säkerställ att ca-agent-builder står under delivery)

## Steg 3: Skapa agents/-struktur

```
mkdir -p agents/templates agents/deployed
```

Skapa agents/templates/_README.md:

```markdown
---
title: "_README — Agents Templates"
date: 2026-06-24
author: agy
tags: [area/OPS, status/APPROVED, author/AGY, type/TEMPLATE]
status: approved
---

# _README — Agents Templates

Detta är mallar för AI-agenter som vi levererar till kunder.

## Struktur

Varje template är en mapp med:
- `prompt.md` — Agentens system prompt. STERIL. Inga interna referenser.
- `tools.yaml` — API-verktyg agenten har tillgång till
- `config.yaml` — Mall för kundspecifik konfiguration
- `tests/` — input.json + expected.json för testning

## Regler

- Ingenting i templates/ refererar till Hermes, ca-skills, OBSIDIAN eller våra interna system
- Allt kundspecifikt (e-post, mapp-ID, max_cost) ligger i config.yaml, ALDRIG i prompt.md
- ca-agent-builder använder dessa mallar för att generera agents/deployed/{kund}/

## Användning

1. ca-agent-builder läser template för rätt agenttyp
2. Fyller i kundspecifik data från audit
3. Skriver till agents/deployed/{kund}/{agent}/
4. Skapar tests/input.json + expected.json från template
```

## Steg 4: Uppdatera INDEX.md och SKILLS_INDEX.md

### INDEX.md
Ändra sektionen för `02_ARCHITECTURE/` och `03_PROTOTYPES/` om de refererar till gamla kategorier.
Hela INDEX.md börjar med att lista alla kategorier. Uppdatera beskrivningen för "delivery" där den används som exempel (om den refereras).

### SKILLS_INDEX.md
Uppdatera kategorin för alla skills som nu ligger under delivery istället för client-work eller building.

## Steg 5: Uppdatera wikilänkar

Sök efter alla filer som refererar till `[[client-work/` eller `[[building/` och uppdatera till `[[delivery/`.

Använd:
```
grep -r "client-work" OBSIDIAN/ skills/ --include="*.md" -l
grep -r "building/" OBSIDIAN/ skills/ --include="*.md" -l
```

Uppdatera varje träff:
- `[[client-work/...]]` → `[[delivery/...]]`
- `[[building/...]]` → `[[delivery/...]]`

## Steg 6: Uppdatera AGENT_PATTERNS.md (skapas som referens)

OBSIDIAN/05_OPS/AGENT_PATTERNS.md behöver inte finnas än — den skapas när första mönstret upptäcks. Skapa den som en tom mall med YAML-frontmatter om den inte finns.

## Steg 7: Verifiera

Kör följande kontroller:

1. `ls skills/` — ska visa: core/ planning/ delivery/
2. `ls agents/` — ska visa: templates/ deployed/
3. `cat .agents/skills.json` — ska lista core, planning, delivery (inte building, inte client-work)
4. `ls skills/delivery/` — ska visa alla 5 skills
5. `grep -r "client-work" OBSIDIAN/ skills/ --include="*.md"` — ska vara tomt
6. `grep -r "building/" OBSIDIAN/ skills/ --include="*.md"` — ska vara tomt (förutom om "building" förekommer som vanligt ord)

## Logga

Efter varje steg, logga i OBSIDIAN/05_OPS/LOGS/2026-06-24.md enligt ca-change-logger-formatet:

```
- HH:MM | agy: Omdöpte client-work → delivery
- HH:MM | agy: Slog ihop building → delivery
- HH:MM | agy: Skapade agents/-struktur med templates/_README.md
- HH:MM | agy: Uppdaterade INDEX.md och SKILLS_INDEX.md
- HH:MM | agy: Uppdaterade wikilänkar (client-work → delivery)
- HH:MM | agy: Verifierade REORG_01 — alla kontroller OK
```

## Klart

När alla steg är klara och verifierade, svara med:

"REORG_01 GENOMFÖRD — alla 7 steg klara och verifierade."
