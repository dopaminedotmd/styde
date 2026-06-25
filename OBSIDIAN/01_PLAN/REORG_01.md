---
title: "REORG_01 — Separera skills (internt) från agents (kund)"
date: 2026-06-24
author: hermes
tags: [area/PLAN, status/DRAFT, author/HERMES, type/PLAN]
status: draft
---

# REORG_01 — Separera skills (internt) från agents (kund)

> [!warning] Läs hela dokumentet innan du agerar.
> Detta är en strukturell omorganisation som påverkar alla skills och framtida arbete.

> Senast uppdaterad: 2026-06-24

---

## 1. Problemet

Idag ligger ALLT i `skills/`:

```
skills/
├── core/              ← Internt: ca-brainstorming, ca-change-logger...
├── planning/          ← Internt: ca-plan-creator, ca-plan-reviewer...
├── building/          ← DELVIS internt: ca-agent-builder...
├── client-work/       ← DELVIS process: mallar för audit, offert, onboarding...
└── reusable/          ← (tom)
```

Problemet är att våra interna skills pratar **vårt språk** — de refererar till Hermes, till våra Obsidian-dokument, till våra arbetsflöden. Det är korrekt för internt bruk.

Men när `ca-agent-builder` genererar en agent åt en kund — den agenten ska vara **steril**. Den ska inte veta att Hermes finns. Den ska inte referera till `ca-brainstorming`. Den ska bara veta sitt uppdrag och sina verktyg.

**Lösning:** Separera i två träd.

---

## 2. Ny struktur

```
consulting.ai/
│
├── skills/              ← INTERNT. Våra bottars verktyg. Vårt språk.
│   ├── SKILLS_INDEX.md
│   ├── core/            ← Internt OS
│   │   ├── ca-brainstorming/
│   │   ├── ca-change-logger/
│   │   ├── ca-file-organizer/
│   │   ├── ca-folder-organizer/
│   │   └── ca-rules-enforcer/
│   ├── planning/        ← Vår planering
│   │   ├── ca-plan-creator/
│   │   └── ca-plan-reviewer/
│   └── delivery/        ← Vår leveransprocess (OMDÖPT från client-work + building)
│       ├── ca-agent-builder/   ← Genererar innehåll i agents/
│       ├── ca-audit-agent/
│       ├── ca-audit-reporter/
│       ├── ca-offert-writer/
│       └── ca-onboarding-lead/
│
├── agents/              ← EXTERNT. Det vi levererar till kund. STERILT.
│   ├── templates/       ← Mallar som används av ca-agent-builder för att generera
│   │   ├── _README.md
│   │   ├── fortnox-invoice/
│   │   │   ├── prompt.md
│   │   │   ├── tools.yaml
│   │   │   └── config.yaml
│   │   └── gmail-sort/
│   │       ├── prompt.md
│   │       ├── tools.yaml
│   │       └── config.yaml
│   └── deployed/        ← Aktiva kundleveranser
│       └── {kund_id}/{agent_id}/
│           ├── prompts/{v1.0.0.md → current.md}
│           ├── tools/{v1.0.0.yaml → current.yaml}
│           ├── config/current.yaml
│           └── tests/
    ├── input.json      ← Skapas av ca-agent-builder vid agentgenerering (mall: agents/templates/{agenttyp}/tests/)
    └── expected.json   ← Samma. Innehåller förväntat output-format för automatisk validering.

**Hur tester körs:** Ett enkelt bash-skript (`agents/deployed/run_tests.sh`) loopar över varje agents tests/, skickar input.json till agenten i dry-run-läge, och jämför output mot expected.json (fuzzy match — struktur, inte exakt text). Resultat: PASS/FAIL per agent. Körs manuellt efter deployment och automatiskt efter prompt-ändringar.
│
├── .agents/             ← OFÖRÄNDRAT. Pekar på skills/ för bot-discovery.
│   ├── AGENTS.md
│   ├── skills.json
│   └── skills/          ← Externa skills (addyosmani, kepano) — oförändrat
```

---

## 3. Regler — vad som gäller efter omorganisation

### Regel 1: skills/ är internt. Alltid.

Allt i `skills/` är våra verktyg. Här använder vi:
- Vårt språk (svenska, kortfattat)
- Våra begrepp (Hermes, ca-prefix, OBSIDIAN-referenser)
- Våra regler (ca-brainstorming kräver design före bygge)

**Vad som händer i `skills/` stannar i `skills/`.** Ingen extern part ser innehållet.

### Regel 2: agents/ är kundens. Alltid.

Allt i `agents/` är vad kunden får. Här använder vi:
- Kundens språk (engelska eller svenska beroende på kund)
- Inga interna referenser (ingen Hermes, inget OBSIDIAN, inga ca-prefix)
- Rena prompt.md + tools.yaml + config.yaml

Ingenting i `agents/` refererar till `skills/` eller våra interna dokument.

### Regel 3: ca-agent-builder är bryggan

`ca-agent-builder` (i `skills/delivery/`) är den enda skill som får röra `agents/`. Den:
- Är själv intern — använder vårt språk, läser våra mallar
- **Genererar sterilt** — output i `agents/` har noll spår av oss
- Hämtar mallar från `agents/templates/` och fyller i kundspecifik data
- Skriver resultatet till `agents/deployed/{kund}/{agent}/`

**ca-agent-builder läser från `skills/` men skriver till `agents/`.**

### Regel 4: .agents/ pekar på skills/ — oförändrat

`.agents/skills.json` och `.agents/AGENTS.md` fortsätter peka på `skills/`-kategorierna.
`.agents/skills.json` ändras för att matcha de nya kategorinamnen (client-work → delivery).
Ingenting i `.agents/` pekar på `agents/` — det är våra bottars discovery, inte kundens.

### Regel 5: Förbättringar vandrar från deployed → templates

När en prompt-förbättring i `agents/deployed/{kund}/{agent}/` bedöms som **generell** (gäller agenttypen, inte kundspecifik) — den förs tillbaka till templates.

**Flöde:**
1. `ca-agent-reviewer` analyserar loggar och flaggar en förbättring
2. William godkänner förbättringen för den specifika kunden
3. `ca-agent-reviewer` bedömer: Är detta generellt för agenttypen?
4. Om JA → ca-agent-builder uppdaterar `agents/templates/{agenttyp}/prompt.md` och bumpar template-version
5. Nästa kund med samma agenttyp startar på den förbättrade baslinjen

**Regel:** Minst 2 olika kunder måste ha samma förbättring innan den flyttas till templates.
**Ansvar:** William godkänner. ca-agent-reviewer flaggar. ca-agent-builder utför.

---

## 4. Genomförande — steg för steg

### Steg 1: Omdöp client-work → delivery

```
Flytta: skills/client-work/ → skills/delivery/
Ändra: .agents/skills.json  ← client-work → delivery
Uppdatera: alla skills som wikilänkar till "client-work/"
```

### Steg 2: Slå ihop building/ → delivery/

```
Flytta: skills/building/ca-agent-builder/ → skills/delivery/
Ta bort: skills/building/ (mappen)
Uppdatera: .agents/skills.json  ← ta bort building från listan
Uppdatera: SKILLS_INDEX.md
```

### Steg 3: Skapa agents/-struktur

```
Skapa: agents/
Skapa: agents/templates/
Skapa: agents/templates/_README.md
Skapa: agents/deployed/
Skapa: agents/deployed/_README.md
```

### Steg 4: Rensa ca-agent-builder/SKILL.md + lägg till positivt exempel

ca-agent-builder får INTE längre referera till "OBSIDIAN/02_ARCHITECTURE/..." i sina genererade agenter.
Dess instruktioner för prompt.md, tools.yaml, config.yaml ska vara rena — de ska inte nämna Hermes eller våra system.

Exempel på vad som ska bort från genererad output:
- ~~"Använd ca-brainstorming för att..."~~
- ~~"Se OBSIDIAN/02_ARCHITECTURE/..."~~
- ~~"Körs av Hermes..."~~

**Positivt exempel — hur en steril prompt.md ska se ut:**

```markdown
# Agent: Fakturahanteraren

## UPPDRAG
Hämta obetalda fakturor från Fortnox varje måndag 08:00.
Kontrollera att varje faktura har korrekt moms och förfallodatum.
Vid avvikelse: skicka notis till kundansvarig via Slack.

## VERKTYG
- Fortnox API: hämta fakturor, uppdatera status
- Slack API: skicka meddelanden till kanal

## REGLER
- Ändra ALDRIG en fakturas belopp
- Skicka ALDRIG betalning — endast notis
- Vid osäkerhet: flagga för manuell granskning

## OUTPUT-FORMAT
{ "status": "ok" | "flag" | "error", "message": "...", "fakturor": [...] }
```

Notera: Inget omnämnande av Hermes, ca-skills, OBSIDIAN, orkestreringssystem eller interna processer. Agenten är självständig.

### Steg 5: Skapa agents/templates/_README.md

En kort instruktion till framtida bottar om vad templates är och hur de används.
Inga interna referenser.

### Steg 6: Uppdatera INDEX.md och SKILLS_INDEX.md

- INDEX.md: ändra sökvägar för delivery
- SKILLS_INDEX.md: ta bort building, omdöp client-work → delivery

### Steg 7: Uppdatera alla interna wikilänkar

Alla skills som refererar till `[[client-work/...]]` eller `[[building/...]]` måste uppdateras.

---

## 5. Vad som INTE förändras

| Sak | Status |
|-----|--------|
| `.agents/AGENTS.md` | Oförändrad |
| `.agents/skills.json` | Endast kategoriuppdateringar |
| `.agents/skills/` (externa skills) | Oförändrat |
| `OBSIDIAN/` | Ingen ändring |
| `MASTER_PLAN_FINAL.md` | Ingen ändring |
| `README.md` | Ingen ändring |
| Alla ca-skill-namn | Behålls (ca-agent-builder fortsätter heta ca-agent-builder) |

---

## 6. Verifiering — efter omorganisation

1. `ls skills/` visar: `core/`, `planning/`, `delivery/`
2. `ls agents/` visar: `templates/`, `deployed/`
3. `.agents/skills.json` listar `../skills/core`, `../skills/planning`, `../skills/delivery`
4. Alla skills i `skills/delivery/` har sina SKILL.md intakta
5. `ca-agent-builder` genererar fortfarande korrekta mallar
6. **Testfall:** ca-agent-builder genererar output mot `agents/templates/fortnox-invoice/` med testdata. Resultatet granskas manuellt: prompt.md innehåller inga interna referenser (Hermes, ca-prefix, OBSIDIAN).

---

## Kommentarer

- 2026-06-24 | hermes: Skapad. Beslut från samtal med William: skills = internt, agents = kundens. Inget Oteck i projektet.
- 2026-06-24 | hermes: Uppdaterad efter bot-granskning — specificerade deployed/-struktur, la till Regel 5 (förbättringsvandring), positivt prompt-exempel i steg 4, testfall i verifiering, config/prompt-separation i struktur.
- 2026-06-24 | antigravity: Granskat. Separationen skills/agents är korrekt och nödvändig. Fyra synpunkter:
  1. `agents/deployed/` saknar definierad mappstruktur. Förslag: `agents/deployed/{tenant_id}/{agent_id}/prompts/v{N}.md`. Utan detta → kaos vid kund 3.
  2. Ingen regel styr hur förbättringar vandrar från `deployed/` tillbaka till `templates/`. Det är det kritiska hålet i självförbättringssystemet. Lägg till Regel 5 (se nedan).
  3. Steg 4 listar vad som ska BORT ur ca-agent-builder men specificerar inte vad som ska IN. Behövs ett positivt exempelutfall — en ren, steril prompt.md.
  4. Verifiering §6 punkt 5 är omöjlig att verifiera automatiskt utan ett testfall. Lägg till: `ca-agent-builder` genererar en testoutput mot `agents/templates/fortnox-invoice/` och granskas manuellt.
- 2026-06-24 | antigravity: FÖRSLAG Regel 5 (självförbättringssystemet): När en godkänd prompt-förbättring i `agents/deployed/{kund}/` bedöms vara generell (gäller agenttypen, inte kundspecifik) → ca-agent-reviewer flaggar för template-uppdatering → William godkänner → ca-agent-builder uppdaterar `agents/templates/{agenttyp}/prompt.md` och bumpar template-version. Nästa kund med samma agenttyp startar redan på förbättrad baseline. Utan denna loop förbättras enskilda kunders agenter men inte systemet som helhet.
- 2026-06-24 | antigravity: Kompletterande synpunkter för REORG_01:
  5. Beroendeisolering: Varje deployed agent kan behöva egna biblioteksversioner. Vi bör planera för virtuella miljöer (venv/package.json) per agentkatalog för att undvika versionskonflikter vid uppskalning.
  6. Separering av konfiguration och prompt: Kundspecifika parametrar (t.ex. e-postadresser, mapp-ID) måste ligga helt i `config.yaml` så att `prompt.md` förblir steril och direkt överförbar till `templates/`.

