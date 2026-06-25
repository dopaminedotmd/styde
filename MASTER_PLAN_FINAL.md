---
title: "MASTER_PLAN_FINAL — styde"
date: 2026-06-24
author: hermes
status: approved
version: 1.0.0-final
---

# MASTER_PLAN_FINAL — styde

> AI-agent consulting för svenska SME-företag.
> *styde — från svenskans "styrd". Kontrollerad automation.*
> Granskad av Hermes, Antigravity (Sonnet), AgY (Gemini Pro), AgY Flash High.
> Status: ALLA BOTTAR ENADE. IMPLEMENTATION STARTAR.

---

## 1. Executive Summary

styde bygger AI-agent-system åt svenska SME-företag (10-250 anställda). Vi kartlägger deras IT-flöden, bygger agenter som automatiserar, och levererar en dashboard där personalen trycker på knappar.

**Status:** William bygger solo. Alpedal onboardas för audits och solutions review.  
**Plattform:** Alla kör Hermes. Samma CLI, samma skill-format, ingen konvertering.  
**Standard:** agentskills.io (Apache 2.0, skapad av Anthropic).  
**Skills-namnkonvention:** `ca-` prefix — `ca-file-organizer`, `ca-audit-agent`.  
**Kunskapsbas:** OBSIDIAN/ med YAML-frontmatter, wikilinks, callouts.

---

## 2. Systemarkitektur

### 2.1 Mappstruktur

```
consulting.ai/
│
├── .agents/
│   ├── AGENTS.md              ← "You MUST read OBSIDIAN/_RULES.md before proceeding."
│   ├── skills.json            ← { "entries": [
│   │                              { "path": "../skills/core" },
│   │                              { "path": "../skills/planning" },
│   │                              { "path": "../skills/delivery" },
│   │                              { "path": "../skills/reusable" }
│   │                            ] }
│   └── skills/                ← System-skills (externt installerade)
│
├── skills/                    ← VÅRT delade skills-bibliotek
│   ├── SKILLS_INDEX.md
│   ├── core/                  ← ca-change-logger, ca-file-organizer, ca-folder-organizer, ca-rules-enforcer
│   ├── planning/              ← ca-brainstorming, ca-plan-creator, ca-plan-reviewer
│   ├── delivery/              ← ca-agent-builder, ca-audit-agent, ca-audit-reporter, ca-offert-writer
│   └── reusable/              ← ca-fortnox-connector, ca-google-workspace-agent
│
└── OBSIDIAN/                  ← Kunskapsbas
    ├── _RULES.md              ← Bot-regler: taggar, frontmatter, kommentarer
    ├── _SKILLS/               ← Obsidian-specifika skills
    ├── _USERS/               ← william.md, alpedal.md (elb arkiverad)
    ├── 00_STRATEGY/           ← Business, market, pricing
    ├── 01_PLAN/               ← Roadmap
    ├── 02_ARCHITECTURE/       ← System, dashboard-spec, agent-framework
    ├── 03_PROTOTYPES/         ← Kod (William)
    ├── 04_CLIENTS/            ← Kundmallar + aktivt arbete
    └── 05_OPS/                ← Subscription, onboarding
```

### 2.2 Tre tekniska grundregler (ANTIGRAVITY-KRAV)

| # | Regel |
|---|-------|
| 1 | `.agents/skills.json` listar varje kategori-undermapp. Forward slash (`../skills/core`) — Windows-kompatibelt. |
| 2 | `.agents/AGENTS.md` innehåller explicit: "You MUST read OBSIDIAN/_RULES.md before proceeding." |
| 3 | Skill-mappar använder `resources/` (inte `assets/`) för templates. |

### 2.3 Skill-format

```
ca-my-skill/
├── SKILL.md          # OBLIGATORISKT
├── scripts/          # Valfritt
├── references/       # Valfritt
└── resources/        # Valfritt: templates
```

**SKILL.md frontmatter:**
```yaml
---
name: ca-my-skill
description: Kort triggarbeskrivning
version: 1.0.0
owner: william
last-updated: 2026-06-24
---
```

### 2.4 Progressiv inläsning

1. **Discovery** — boten ser bara `name` + `description`
2. **Activation** — task matchar description → laddar full SKILL.md
3. **Execution** — boten följer instruktionerna

---

## 3. Implementation Plan

### Fas 0: Foundation (1 dag)

**Mål:** Repo-struktur + externa skills på plats. Noll risk.

#### Task 0.1: Skapa `.agents/skills.json`

- [ ] Skapa: `.agents/skills.json`

```json
{
  "entries": [
    { "path": "../skills/core" },
    { "path": "../skills/planning" },
    { "path": "../skills/delivery" },
    { "path": "../skills/reusable" }
  ]
}
```

- [ ] Verifiera: `cat .agents/skills.json` visar JSON utan syntaxfel
- [ ] **Commit**

#### Task 0.2: Skapa `.agents/AGENTS.md`

- [ ] Skapa: `.agents/AGENTS.md`

```markdown
# Agent Rules — styde

You MUST read OBSIDIAN/_RULES.md before proceeding with any task in this repository.
All planning documents are in OBSIDIAN/. All skills are in skills/ (custom) and .agents/skills/ (external).
Use ca- prefix for all styde skills.
```

- [ ] Verifiera: filen existerar, innehåller "You MUST read"
- [ ] **Commit**

#### Task 0.3: Skapa `skills/`-struktur

- [ ] Skapa mappar:

```bash
mkdir -p skills/core skills/planning skills/delivery skills/reusable
```

- [ ] Skapa: `skills/SKILLS_INDEX.md` med innehåll:

```markdown
# Skills Index — styde

| Skill | Kategori | Owner | Version | Beskrivning |
|-------|----------|-------|---------|-------------|
```

- [ ] Verifiera: alla 5 undermappar + index skapade
- [ ] **Commit**

#### Task 0.4: Installera externa skills

- [ ] Installera Addy Osmani:

```bash
npx skills add addyosmani/agent-skills
```

Expected: success-meddelande, skills installeras som individuella mappar i `.agents/skills/`

- [ ] Installera Kepano Obsidian:

```bash
npx skills add kepano/obsidian-skills
```

Expected: success-meddelande, skills installeras som individuella mappar i `.agents/skills/`

- [ ] **Kommentar:** Taste Skill installeras i Fas 3 (dashboard v2).
- [ ] **Commit**

#### Task 0.5: Verifiera skill-discovery

- [ ] Test: be en bot att använda `ca-file-organizer`. Boten ska svara att skillen inte finns än.
- [ ] Test: be en bot att lista tillgängliga skills. Ska inkludera både `.agents/skills/` och `skills/`.
- [ ] Expected: discovery fungerar från båda träden.

> Fas 0 klar när: alla 5 tasks är gröna.

---

### Fas 1: Core Skills (1-2 veckor)

**Mål:** Sex interna skills som blockerar allt annat.

| Prio | Skill | Kategori | Byggs av |
|------|-------|----------|----------|
| 0.5 | `ca-brainstorming` | planning | Hermes |
| 1 | `ca-file-organizer` | core | Hermes |
| 2 | `ca-folder-organizer` | core | Hermes |
| 3 | `ca-rules-enforcer` | core | Hermes |
| 4 | `ca-plan-creator` | planning | Hermes |
| 5 | `ca-plan-reviewer` | planning | Hermes |

#### Task 1.1: Bygg `ca-brainstorming`

- [ ] Skapa: `skills/planning/ca-brainstorming/SKILL.md`

```markdown
---
name: ca-brainstorming
description: Use before any build task. Explore, question, design before code.
version: 1.0.0
owner: william
last-updated: 2026-06-24
---

# ca-brainstorming

## When to use
Activate before any implementation task. This skill forces a design-first approach.

## Workflow
1. **Explore:** List 3 alternative approaches to the problem.
2. **Question:** Write down 3 assumptions and test each one.
3. **Design:** Create a mini-spec (max 10 lines) before any code.
4. **Get approval:** Post the mini-spec as a comment in the relevant plan document.
5. **Only then:** Proceed to implementation.

## Rule
No code before an approved design. Ever.
```

- [ ] **Commit**

#### Task 1.2: Bygg `ca-file-organizer`

- [ ] Skapa: `skills/core/ca-file-organizer/SKILL.md`

Innehåll: styr var nya filer läggs. Namnkonvention `STOR_BOKSTAVER_med_underscore.md`. Max 3 nivåer. Arkiv: `status/ARCHIVED`.

- [ ] **Commit**

#### Task 1.3: Bygg `ca-folder-organizer`

- [ ] Skapa: `skills/core/ca-folder-organizer/SKILL.md`

Innehåll: skapa aldrig mappar utanför definierade. Ny kategori → plan i `01_PLAN/` först.

- [ ] **Commit**

#### Task 1.4: Bygg `ca-rules-enforcer`

- [ ] Skapa: `skills/core/ca-rules-enforcer/SKILL.md`

Innehåll: flaggar brott (fel mapp, fel frontmatter, fel taggar, saknad kommentarssektion). Blockerar INTE. Skriver kommentar + notifierar ägaren.

- [ ] **Commit**

#### Task 1.5: Bygg `ca-plan-creator`

- [ ] Skapa: `skills/planning/ca-plan-creator/SKILL.md`

Innehåll: använder PLAN_TEMPLATE.md i OBSIDIAN/_TEMPLATES/. Se till att frontmatter är korrekt. Taggar enligt _RULES.md.

- [ ] **Commit**

#### Task 1.6: Bygg `ca-plan-reviewer`

- [ ] Skapa: `skills/planning/ca-plan-reviewer/SKILL.md`

Innehåll: granskar planer. Checklista: frontmatter OK? Taggar rätt? Mapp rätt? Kommentarssektion finns? Inga placeholder ("TBD", "TODO")?

- [ ] **Commit**

#### Task 1.7: Testacceptans

- [ ] Test 1: Bot skapar ny plan → använder PLAN_TEMPLATE.md, frontmatter korrekt
- [ ] Test 2: Bot lägger fil i rätt OBSIDIAN/-mapp
- [ ] Test 3: Bot anropar rätt skill baserat på task
- [ ] Test 4: Kommentarsystem: datum + author + text, rätt format

> Fas 1 klar när: alla 4 tester gröna.

---

### Fas 2: Foundation — System & Försäljning (4-6 veckor)

**Mål:** Dashboard MVP, hemsida, audit-system, första betalda kund.

| # | Uppgift | Ansvarig | Start |
|---|---------|----------|-------|
| 2.1 | Bygg `ca-obsidian-markdown` + `ca-obsidian-frontmatter` | Hermes | Dag 1 |
| 2.2 | Bygg dashboard MVP | William | Dag 1 |
| 2.3 | Bygg hemsida | William | Dag 1 |
| 2.4 | Bygg `ca-audit-agent` + `ca-audit-reporter` | Hermes (mall) → Alpedal (test) | Dag 1 |
| 2.5 | **Försäljning: 20 outreach/dag** | William | **Dag 1 — parallellt** |
| 2.6 | Bygg `ca-agent-builder` | William + Hermes | Vecka 2 |
| 2.7 | Land första audit | William + Alpedal | Vecka 2-4 |
| 2.8 | Genomför första audit | Alpedal + William | Vecka 3-5 |
| 2.9 | Bygg första kundens agenter | William | Vecka 4-6 |
| 2.10 | Leverera första systemet | Alla | Vecka 6 |
| 2.11 | Skriv case study | William | Vecka 6 |

> **Kritiskt:** Försäljning (2.5) startar dag 1, inte efter dashboard/hemsida.
> Genomsnittlig säljcykel: 2-4 veckor → matchar byggtiden för MVP.

---

### Fas 3: Skala (efter första kund)

- Dashboard v2 (Taste Skill aktiveras)
- Första reusable-skill född ur kundarbete
- `ca-plugin-manager` byggs (grupperar skills i bundles om max 10)
- 5 betalda audits, 3 implementationer, 2 subscriptioner

### Fas 4: Väx (12 månader)

- 15+ audits, 8+ implementationer, 5+ subscriptioner
- 1,5-2 MSEK ARR
- Varje ny kund snabbare än förra — flywheel snurrar

---

## 4. Business Model

### 4.1 Tre-stegsmodell

| Steg | Pris | Tid | Beskrivning |
|------|------|-----|-------------|
| **Audit** | 19 900 kr | 2 dagar | Kartläggning, rapport, offert. **Avräkningsklausul:** vid Build-köp ≤30 dagar dras 19 900 kr av från Build-priset. |
| **Build** | 99 000-300 000 kr | 3-4 veckor | Agenter + dashboard + integrationer + utbildning |
| **Operate** | 4 900-19 900 kr/mån | Löpande | Drift, uppdateringar, support |

### 4.2 Subscription-tiers med SLA

| Nivå | Pris | Agenter | SLA | Inkluderat |
|------|------|---------|-----|------------|
| Basic | 4 900 kr/mån | 1-3 | Mail 24h vardagar | Driftövervakning, buggfixar. Inga förändringar i agentlogik. |
| Pro | 9 900 kr/mån | 4-8 | Mail+telefon 8h vardagar | + 2h fri utvecklingstid/mån för finjusteringar. |
| Enterprise | 19 900 kr/mån | Obegränsat | Priority 2h dygnet runt | + 6h fri utvecklingstid/mån. Vitmärkt dashboard. Säljs först efter 3 stabila Pro-kunder. |

### 4.3 Kundekonomi (exempel Pro-kund år 1)

Audit 19 900 + Build 150 000 + Sub 118 800 = **288 700 kr**

---

## 5. Team & Ansvar

| Person | Roll | Ansvar |
|--------|------|--------|
| William | Founder, Creative Director, Builder, **GDPR-ansvarig (interim)** | Vision, försäljning, bygga allt, kundrelation, dataskydd |
| Alpedal | Solutions Architect | Kundaudits, kartläggning, rapportskrivning |

---

## 6. Externa Skills — Installationsordning

| # | Skill | När | Varför |
|---|-------|-----|--------|
| 1 | `addyosmani/agent-skills` | Fas 0 | Disciplin: Define→Plan→Build→Verify→Review→Ship |
| 2 | `kepano/obsidian-skills` | Fas 0 | Konsistent Obsidian-syntax för alla dokument |
| 3 | `Leonxlnx/taste-skill` | Fas 3 | Installera nu, aktivera vid dashboard v2 |

**Ej nu:**
- Obra Superpowers — Fas 3 (sub-agenter)
- LobeHub — Fas 4 (kund-UI)
- Dify — **ALDRIG** (konkurrerande filosofi)
- sickn33 — **installera INTE** (studera konceptet, bygg egen `ca-plugin-manager`)
- OpenClaw — raderas

**Regel:** Sök VoltAgent Awesome List ALLTID innan ny reusable-skill byggs. Installera bara om uppenbart relevant inom 2 minuter från README.

---

## 7. Risker

| Risk | Impact | Mitigering |
|------|--------|------------|
| Bottar hittar inte `skills/` undermappar | Hög | `.agents/skills.json` per kategori, forward slash |
| William som ensam builder (bus factor) | Hög | Standardiserad tech stack + full dokumentation. Hermes bygger skills parallellt. |
| Kunddata i agent-prompts → GDPR | Hög | William = interim DPO. Dataprocessing-avtal med kund före audit. Utvärdera on-prem/lokal modell för känslig data. |
| Skill versionsbrott | Medel | Pinna skill-version i `skills.json`. Automatisk generering av skills.json via script. |
| Context window exhaustion | Medel | Progressiv inläsning (endast name+description vid discovery) |
| Ingen vill betala för audit | Medel | Avräkningsklausul gör audit riskfri. Om 5 leads säger nej → utvärdera pris. |
| SLA-brott | Hög | Sälj inte Enterprise förrän 3 Pro-kunder är stabila |
| Konkurrens via relationsförsäljning vi inte ser | Medel | Bygg referenser snabbt. Första kund = case study. |

---

## 8. Tech Stack

Dashboard: **Next.js + Tailwind CSS**  
Backend API: **Node.js Express (REST)**  
Hosting: **Vercel (frontend), valfri VPS (backend)**  
Inga undantag utan teamdiskussion. Dokumentera allt i `02_ARCHITECTURE/`.

---

## 9. OBSIDIAN-format

Alla dokument i OBSIDIAN/ följer:

```yaml
---
title: "Dokumenttitel"
date: 2026-06-24
author: william
tags: [area/STRATEGI, status/APPROVED, author/WILLIAM, type/PLAN]
status: draft
---
```

Taggar: `area/STRATEGI | PLAN | ARKITEKTUR | KLIENT | OPS | REFERENS`  
Status: `status/DRAFT | REVIEW | APPROVED | ARCHIVED`  
Typ: `type/CONCEPT | PLAN | REPORT | SPEC | TEMPLATE`

Kommentarer i botten: `- YYYY-MM-DD | author: text`

---

## 10. Beslutslogg

| Datum | Beslut | Konsensus |
|-------|--------|-----------|
| 2026-06-24 | `skills/` på rotnivå, undermappar i skills.json | Alla |
| 2026-06-24 | `ca-` prefix för interna skills | Alla |
| 2026-06-24 | `resources/` (inte `assets/`) i skill-mappar | Alla |
| 2026-06-24 | `.agents/AGENTS.md` explicit instruktion | Alla |
| 2026-06-24 | Core-skills först, resten på kundtid | Alla |
| 2026-06-24 | sickn33: studera, installera INTE | Alla* |
| 2026-06-24 | Taste Skill installeras nu, aktiveras v2 | Alla |
| 2026-06-24 | Försäljning startar dag 1 i Fas 2 (parallellt) | Alla |
| 2026-06-24 | Avräkningsklausul på audit | Alla |
| 2026-06-24 | SLA definierat per tier | Alla |
| 2026-06-24 | Next.js + Tailwind för dashboard | Alla |
| 2026-06-24 | William = GDPR-ansvarig (interim) | Alla |
| 2026-06-24 | `ca-brainstorming` som prio 0.5 | Alla |
| 2026-06-24 | `ca-rules-enforcer` på prio 3 | Alla |
| 2026-06-24 | `ca-plugin-manager` i backlog, byggs vid behov | Alla |

> *AgY Flash High föreslog hybrid sickn33 — majoriteten röstade för egen bygge. Beslutat.

---

## 11. Reusable vs Delivery

- ≥2 kunder (eller uppenbart generisk) → `skills/reusable/`
- 1 kund → `skills/delivery/`
- Efter varje kundbygge: 1 timme schemalagd för att extrahera generell skill

---

## 12. Omedelbara Nästa Steg (Fas 0 — idag)

1. William skapar `.agents/skills.json` (per kategori, forward slash)
2. William skapar `.agents/AGENTS.md` ("You MUST read OBSIDIAN/_RULES.md")
3. William skapar `skills/`-mapp med 5 undermappar + SKILLS_INDEX.md
4. `npx skills add addyosmani/agent-skills`
5. `npx skills add kepano/obsidian-skills`
6. Verifiera skill-discovery från båda träden
7. Hermes börjar bygga `ca-brainstorming` (prio 0.5)
