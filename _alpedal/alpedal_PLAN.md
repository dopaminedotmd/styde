---
title: "Sammanställd planering — William & Alpedal"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/APPROVED, author/HERMES, type/PLAN]
status: approved
---

# Sammanställd planering — styde.ai

> En samlad planering för William och Alpedal som beskriver styrkor, fokusområden och nästa steg för att ta styde.ai från planering till drift.

---

## 1. Styrkor och fokusområden

För att nå maximalt tempo och undvika planeringsparalys fokuserar vi på våra respektive spetskompetenser.

### William (Builder & Seller)
- **Styrkor:** Fullstack-utveckling (Python, Next.js, Express), infrastruktur/serverarkitektur samt kundkontakt och uppsökande försäljning (outreach).
- **Varför:** William har den tekniska förmågan att snabbt koda fungerande prototyper och plattformar samt energin för direkt kundkontakt.
- **Fokusområde:** Utveckling av core-systemet (CLI, server, Express-API, Next.js-dashboard) samt att driva inflödet av leads.

### Alpedal (Auditor & Blueprint Designer)
- **Styrkor:** Struktur, systemtänkande, mönsterigenkänning samt design av agent-blueprints (logik, persona, prompts, kravspecifikationer).
- **Varför:** Alpedal är extremt skicklig på att kartlägga affärsprocesser, hitta flaskhalsar och definiera exakta instruktioner (blueprints) för hur agenter ska lösa problem.
- **Fokusområde:** Utveckling av kundaudits (kartläggning av kunders flöden) samt arkitektur av agenternas beteende och instruktioner.

---

## 2. Vad vi bör fokusera på härnäst och varför

Vårt omedelbara fokus är **Fas 1: FIRST BLOOD**. Vi behöver en fungerande minsta produkt (MVP) för att visa potentiella kunder, och vi behöver en gemensam arbetsyta på servern.

1. **William: Consultant Agent v0.1 + Serverkonfiguration**
   - *Varför:* Vi kan inte sälja utan att visa vad vi gör. Consultant Agent v0.1 (CLI) ger oss en automatiserad rapport som vi kan använda som säljpitch. Servern behövs för att vi båda ska kunna utveckla och köra agenter på samma fysiska maskin.
2. **Alpedal: Agent Blueprints + Audit-struktur**
   - *Varför:* Blueprints är styde.ai:s kärna. Genom att designa tre mallar (`invoice-reviewer`, `customer-service-triage`, `mail-sorter`) sätter Alpedal standarden för hur våra framtida leveranser ser ut.

---

## 3. Detaljerad checklista för William

### Sprint 01 — "First Blood" (2026-06-26 — 2026-06-28)
- [ ] Bygg `konsult-agent` v0.1 (Python CLI som tar en URL och genererar en YAML-rapport).
- [ ] Sätt upp den gemensamma fysiska servern (Ubuntu Server + SSH-nycklar + Node.js + PostgreSQL).
- [ ] Konfigurera brandvägg (UFW) och Git-repo på servern.

### Sprint 02 — Kvalitetssäkring (3 dagar)
- [ ] Testa `konsult-agent` på 5 verkliga företagssajter och åtgärda felaktigheter.
- [ ] Justera LLM-prompterna i agenten baserat på Alpedals feedback.

### Sprint 03 — Säljinfrastruktur (3 dagar)
- [ ] Skapa ett script som exporterar YAML-rapporten till en snygg PDF.
- [ ] Testa PDF-exporten med data från de 5 testsajterna.

---

## 4. Detaljerad checklista för Alpedal

### Sprint 01 — "First Blood" (2026-06-26 — 2026-06-28)
- [x] Designa blueprint för `invoice-reviewer` (skapa `persona.md`, `blueprint.yaml`, `tools.yaml`).
- [x] Designa blueprint för `customer-service-triage` (skapa `persona.md`, `blueprint.yaml`, `tools.yaml`).
- [x] Designa blueprint för `mail-sorter` (skapa `persona.md`, `blueprint.yaml`, `tools.yaml`).

### Sprint 02 — Kvalitetssäkring (3 dagar)
- [ ] Utvärdera kvaliteten på `konsult-agent` på de 5 testsajterna tillsammans med William.
- [ ] Identifiera logiska felaktigheter i agentens slutsatser och skriv ner mönster för förbättringar.

### Sprint 03 — Audit-struktur (3 dagar)
- [ ] Skapa ett standardiserat audit-processdokument (hur vi genomför en kundaudit).
- [ ] Skapa en mall för slutgiltig kundaudit-rapport.

---

## Comments
- 2026-06-25 | hermes: Skapad efter Williams begäran om en sammanställd planering med checkboxar.
