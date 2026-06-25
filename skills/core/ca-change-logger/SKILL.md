---
name: ca-change-logger
description: Loggar alla ändringar i styde-repot. Använd denna skill efter varje genomförd åtgärd (skapat fil, ändrat fil, godkänt planer etc.) för att uppdatera dagens logg i OBSIDIAN/05_OPS/LOGS/.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-change-logger

## Syfte

Alla ändringar i styde loggas spårbart. Varje bot skriver en logg efter varje genomförd åtgärd.
Detta gör att William, Alpedal och framtida bottar alltid kan se vem som gjorde vad och när.

## Loggplats

Alla loggar skrivs till:

```
OBSIDIAN/05_OPS/LOGS/{YYYY-MM-DD}.md
```

En fil per dag. Skapas automatiskt av första boten som loggar den dagen.
OBSIDIAN/05_OPS/LOGS/_INDEX.md innehåller register över alla loggfiler.

## Format

Varje loggpost är en punkt i omvänd kronologisk ordning (nyaste överst):

```
- HH:MM | author: Kort beskrivning av vad som gjordes
```

Exempel:

```
- 14:32 | hermes: Skapade BUILD_PHASE_2.md med agent flow, security och dashboard-spec
- 14:15 | william: Godkände förslaget, justerade teamstruktur
- 13:50 | alpedal: Skrev onboarding-rapport
```

## När du loggar

Du loggar ALLTID efter:

| Åtgärd | Logga |
|--------|-------|
| Skapa ny fil (plan, skill, rapport) | `Skapade {filnamn} — {kort om vad den gör}` |
| Ändra befintlig fil | `Uppdaterade {filnamn} — {vad ändrades}` |
| Arkivera/ta bort innehåll | `Arkiverade {filnamn} — {anledning}` |
| Skapa ny mapp | `Skapade mappen {mapp}/` |
| Godkänna/approvera dokument | `Godkände {dokument} — {ändring}` |
| Bygga en testklient | `Byggde {kund}/ — {agenter}` |
| Genomföra en audit | `Genomförde audit {kund} — {resultat}` |

Du loggar INTE:
- Att du läser en fil (läsning är inte en ändring)
- Att du söker efter något
- Att du skriver en loggpost (det skapar cirkulär logg)
- Små temporära operationer (t.ex. "läste en rad för att förstå")

## Ordning

1. Gör ändringen
2. Öppna dagens loggfil (skapa om den inte finns)
3. Lägg till din loggrad ALLRA FÖRST (nyaste överst)
4. Spara

## Om filen inte finns

Skapa `OBSIDIAN/05_OPS/LOGS/{YYYY-MM-DD}.md` med frontmatter:

```yaml
---
title: "Change Log — {YYYY-MM-DD}"
date: {YYYY-MM-DD}
author: {din}
tags: [area/OPS, status/APPROVED, author/{DIN}, type/REPORT]
status: approved
---

# Change Log — {YYYY-MM-DD}

> Ändringar i styde denna dag.

```

## Kommentarer

- 2026-06-25 | hermes: Uppdaterade beskrivningen till svenska, bumpade version till 1.1.0 och lade till kommentarssektion.

