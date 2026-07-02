---
title: "Designspecifikation — Installation av Understand-Anything"
date: 2026-06-28
author: hermes
tags: [area/PLAN, status/APPROVED, author/HERMES, type/SPEC]
status: approved
---

# Designspecifikation — Installation av Understand-Anything

> Specifikation för lokal installation av Egonex-AI/Understand-Anything som agent-skills i repot.

---

## 1. Syfte och omfattning

Att installera Egonex-AI/Understand-Anything lokalt i utvecklingsmiljön styde.ai. Detta görs genom att integrera verktygets skills i projektets `.agents/`-katalog för att tillåta agenter att analysera kodbasen och bygga interaktiva grafer.

---

## 2. Arkitektur och komponenter

### 2.1 Förvaring av källkod
- Repot flyttas från den tillfälliga mappen till en permanent katalog på sökvägen `file:///C:/Users/William/styde.ai/.understand-anything/repo`.
- Katalogen `.understand-anything/` läggs till i `.gitignore` för att undvika att externa filer eller genererade grafer checkas in.

### 2.2 Skill-länkar (Junctions)
- Länkar skapas som directory junctions på Windows från `.understand-anything/repo/understand-anything-plugin/skills/{skill-namn}` till `.agents/skills/{skill-namn}`.
- Totalt 8 skills länkas:
  - `understand`
  - `understand-chat`
  - `understand-dashboard`
  - `understand-diff`
  - `understand-domain`
  - `understand-explain`
  - `understand-knowledge`
  - `understand-onboard`

### 2.3 Registrering
- De 8 nya skillsen registreras i `file:///C:/Users/William/styde.ai/.agents/skills.json` så att AI-verktygen kan upptäcka dem.

---

## 3. Gränssnitt och Dataformat

### 3.1 Uppdatering av `.agents/skills.json`
Följande sökvägar läggs till i `entries`-listan:
```json
    { "path": "./skills/understand" },
    { "path": "./skills/understand-chat" },
    { "path": "./skills/understand-dashboard" },
    { "path": "./skills/understand-diff" },
    { "path": "./skills/understand-domain" },
    { "path": "./skills/understand-explain" },
    { "path": "./skills/understand-knowledge" },
    { "path": "./skills/understand-onboard" }
```

---

## 4. Verifieringsplan

### 4.1 Manuella kontroller
- Kontrollera att alla 8 junction-mappar i `.agents/skills/` pekar på rätt målkataloger under `.understand-anything/repo/`.
- Validera att `file:///C:/Users/William/styde.ai/.agents/skills.json` innehåller korrekt JSON.
- Kontrollera att `.gitignore` ignorerar `.understand-anything/`.

---

## Comments

- 2026-06-28 | hermes: Initial specifikation skapad efter användarens val av lokal installation.
- 2026-06-28 | hermes: Planen har genomförts och verifierats.
