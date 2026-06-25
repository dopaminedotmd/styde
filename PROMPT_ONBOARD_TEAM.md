# Prompt — Total System Audit

> Copy this prompt to any bot (Hermes, Antigravity Sonnet, AgY Gemini, etc.).
> The bot shall perform a complete system audit and deliver a structured review with ratings, improvement suggestions, and risk analysis.

---

## Prompt (send to the bot)

```
Du ska genomföra en TOTAL SYSTEMAUDIT av styde.

Målet är att du läser hela systemet — varenda mapp, varenda skill, varenda plan —
och lämnar en strukturerad review med betyg, förbättringsförslag och kritik.

Var ärlig. Var konstruktiv. Håll inget tillbaka. Din uppgift är att hitta svagheter.

## Steg 1: Läs auktoritetsdokumenten (i denna ordning)

1. README.md — rotbeskrivning
2. MASTER_PLAN_FINAL.md — hela planen, beslutad och granskad
3. .agents/AGENTS.md — bot-regler
4. obsidian/_RULES.md — taggar, frontmatter, kommentarer
5. obsidian/INDEX.md — hubben
6. obsidian/SYSTEM_DOCUMENT.md — systemöversikt
7. .agents/skills.json — skill-discovery config

## Steg 2: Läs alla skills

Läs ALLA SKILL.md-filer. Både interna och externa.

Det är:
- skills/core/*/SKILL.md
- skills/planning/*/SKILL.md
- skills/delivery/*/SKILL.md
- .agents/skills/*/SKILL.md (externa)

Läs varje skills SKILL.md. Förstå vad den gör, när den triggas, om den är korrekt.

## Steg 3: Läs alla obsidian-dokument

Läs vartenda dokument i obsidian/:
- _RULES.md, INDEX.md, SYSTEM_DOCUMENT.md
- 00_strategy/ — business, market, offer, pricing
- 01_plan/ — roadmap, build phase, reorg
- 02_architecture/ — system overview, dashboard, agent framework
- 04_clients/ — mallar, templates
- 05_ops/ — onboarding, subscription, logs, agent patterns
- 99_references/ — länkar
- _users/ — profiler (william, alpedal, elb)
- _templates/ — mallar för planer, agendor

## Steg 4: Läs agents/-strukturen

- agents/templates/_README.md
- agents/deployed/_README.md

Förstå vad som är tänkt att hamna här och om strukturen är korrekt.

## Steg 5: Verifiera strukturell hälsa

Kontrollera:
1. Finns .gitignore? Är den korrekt?
2. Är SKILLS_INDEX.md korrekt? Inga trasiga tabeller?
3. Är .agents/skills.json korrekt? Alla sökvägar existenta?
4. Finns dubbletter av skills?
5. Finns gamla referenser (byggnader, client-work, Elb) som borde städats?
6. Unicodeproblem i konfigurationsfiler?
7. Finns obsidian-dokument utan frontmatter eller ## Kommentarer?
8. Är loggningen aktiv? Finns dagens logg?

## Steg 6: Skriv audit-rapport

Skapa filen: obsidian/00_strategy/SYSTEM_AUDIT_{YYYY-MM-DD}.md

Frontmatter:
---
title: "System Audit — {YYYY-MM-DD}"
date: {YYYY-MM-DD}
author: {din_bot}
tags: [area/STRATEGI, status/DRAFT, author/{DIN}, type/REPORT]
status: draft
---

Rapporten ska innehålla:

### 1. Sammanfattning (Executive Summary)
Kort: vad är systemets hälsa? Är det byggbart? Vad är största risken?

### 2. Betyg per kategori

Använd skala 1-10 (där 10 = perfekt):

| Kategori | Betyg | Kommentar |
|----------|-------|-----------|
| Struktur & navigation | X/10 | |
| Skills (interna) | X/10 | |
| Skills (externa) | X/10 | |
| Planer & roadmap | X/10 | |
| Arkitektur & specar | X/10 | |
| OPS & logging | X/10 | |
| Säkerhet & regler | X/10 | |
| **TOTAL** | **X/10** | |

### 3. Styrkor (Top 3-5)
Vad är bra? Vad ska vi absolut inte ändra?

### 4. Svagheter (Top 5+)
Vad är dåligt, trasigt, eller riskfyllt? Var specifik — peka på exakta filer och rader.

### 5. Förbättringsförslag (prioordnad)

| Prio | Förslag | Effekt | Arbetsinsats |
|------|---------|--------|--------------|
| P0 | | | |
| P0 | | | |
| P1 | | | |
| P1 | | | |
| P2 | | | |

### 6. Riskanalys

| Risk | Impact | Sannolikhet | Hantering |
|------|--------|-------------|-----------|
| | | | |

### 7. Övriga synpunkter

Allt som inte passar ovan. Konstruktiv kritik, idéer, vägval som borde diskuteras.

## Steg 7: Verifiera

När rapporten är skriven, svara med:
"SYSTEM AUDIT KLAR — rapport skriven till obsidian/00_strategy/SYSTEM_AUDIT_{YYYY-MM-DD}.md"
```

---

## When the report is in

William reads:
- `obsidian/00_strategy/SYSTEM_AUDIT_{YYYY-MM-DD}.md`

He then sees a complete picture of the system's health, ratings per category, and can prioritize improvements based on the bot's analysis.

The report also becomes a baseline — the next audit uses this one as a reference, so we can see if we're improving.

---
*Translation note: This file was translated from Swedish to English on 2025-06-25. The prompt code block was left in Swedish as it is sent directly to bots that understand Swedish.*
