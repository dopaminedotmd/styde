---
title: "_alpedal — Alpedals domän"
date: 2026-06-25
author: hermes
tags: [area/OPS, status/APPROVED, author/HERMES, type/TEMPLATE]
status: approved
---

# _alpedal — Alpedals domän

> Auditor. Blueprint Designer. Systemtänkare.
> Det här är labbet där råa idéer blir precisions-agenter.
> Styde Forge — den portabla evolutionära agent-smältugnen — är hjärtat.

---

## Vad detta är

Detta är Alpedals **personliga workspace** inom styde.ai — en isolerad miljö för:

| Aktivitet | Verktyg |
|-----------|---------|
| **Agent-design** | Blueprint-skapande enligt Forge-format (`persona.md` + `blueprint.yaml` + `tools.yaml`) |
| **Agent-raffinering** | [[styde-forge/PHASE0_COMPLETE\|Styde Forge v3.0]] — den portabla evolutionära agent-smältugnen |
| **Agent-övervakning** | Styde Forge Dashboard — Tauri desktop app (Mission Control) |
| **Kund-audits** | Kartläggning av IT-flöden, system, och automationspotential |
| **Mönster-spaning** | Upptäcka återkommande automation patterns som ingen annan ser |
| **Experiment** | Fri utforskning utan påverkan på main-systemet |

---

## Vad detta INTE är

- ❌ **Inte planen** — [[obsidian/01_plan/MASTER_PLAN\|MASTER_PLAN.md]] är den enda källan till sanning
- ❌ **Inte produktionskod** — allt här är experimentellt tills William godkänner
- ❌ **Inte kundleveranser** — agenter för kund byggs i `agent-blueprints/`, inte här
- ❌ **Inte gemensam yta** — detta är Alpedals. Williams yta är `_william/`

---

## Styde Forge — Översikt

Två integrerade projekt, ett ekosystem.

```
┌──────────────────────────┐     ┌──────────────────────────┐
│   StydeForge Dashboard   │     │   Hermes Agent           │
│   (Tauri desktop app)    │────▶│   (CLI + Runtime)        │
│                          │     │                          │
│  • Monitor agents        │     │  • Forge core loop       │
│  • Control pipeline      │     │  • Agent spawning        │
│  • Chat with AI          │     │  • 6-layer eval pipeline │
│  • View benchmarks       │     │  • Skill loading         │
│  • System health         │     │  • Cron jobs             │
└──────────────────────────┘     └──────────────────────────┘
         │                                │
         │  hermes process list           │
         │  hermes forge start/stop       │
         │  hermes delegate_task          │
         └────────────────────────────────┘
```

Dashboard är ansiktet. Hermes/Forge är motorn.

---

## 1. Styde Forge — Smältugnen

> *"Where raw agents are forged into elite through precision and iterative purity."*

**Status:** Phase 0 COMPLETE ✅ — 53 designdokument, 14 sektioner, 8 arkitekturbeslut, 9 risker mitigaterade.

**Kärnloop:**
```
DEFINE → SPAWN → EVALUATE → IMPROVE → CHECKPOINT
    ↑_________________________________________|
```

| Steg | Beskrivning |
|------|-------------|
| **DEFINE** | Blueprint laddas, skills isoleras per agent (3-5 st, inte 85). Caveman Ultra aktiveras. |
| **SPAWN** | Agent startas via `delegate_task()`. Dual-model: deepseek-v4-flash (agentkörning) + deepseek-v4-pro (eval/teacher). |
| **EVALUATE** | 6-lagers pipeline: Self-Eval → LLM-as-Judge → Cross-Judge Consensus → Bias Calibration → Auto-Validation → Bayesian Weight Optimization |
| **IMPROVE** | Teacher Agent analyserar → diagnosticerar → extraherar skills → coachar agenten |
| **CHECKPOINT** | Atomär write (temp → rename). **Quality gate ≥ 80/100.** Allt under kastas. |

### Arkitektur — 14 sektioner

| # | Sektion | Dokument | Kärna |
|---|---------|----------|-------|
| 00 | Overview | 12 | Arkitektur, data models, core loop, interfaces, state machines, config, testing |
| 01 | Vision | 2 | Vision & goals, blueprint catalog (6 domäner) |
| 02 | Hardware | 2 | Auto-detect Machine-A vs B, resource governor, GPU-anpassning |
| 03 | Eval Pipeline | 7 | 6-lagers eval: self → judge → konsensus → bias → validering → Bayesian |
| 04 | Sampling Stack | 5 | NUTS, Hamiltonian MC, Variational Inference, Dual Averaging, Tree Depth |
| 05 | Meta-Layer | 4 | Dynamic model selector, historical learning, auto-version, self-monitoring |
| 06 | Persistence & Safety | 4 | Atomära writes, checkpoints, recovery, risk register |
| 07 | Multi-Agent | 2 | Teacher-student pattern, agent-isolering, kunskapsdelning |
| 08 | Import/Export | 2 | Single-prompt import, sync-strategi |
| 09 | Risk & Maintenance | 1 | Pruning, cleanup |
| 10 | Operations | 7 | Skill loading, blueprint validation, JSON-lines logging, Caveman Ultra, kostnader, API keys, human oversight |
| 11 | Knowledge Management | 1 | Kunskapslivscykel |
| 12 | Teacher Agent | 1 | Feedback loop, skill extraction, coaching |
| 13 | Hooks & Events | 1 | 17 events, 4 hook-typer |
| 14 | RAG Retrieval | 1 | Retrieval-Augmented Generation |

Läs hela: [[styde-forge/00_Overview/Master_Architecture_Overview]]

### Designbeslut (8 nyckelbeslut)

| # | Beslut | Varför |
|---|--------|--------|
| D001 | Meta-layer över Docker swarm | 18 GB VRAM på Machine-B. En modell åt gången. |
| D002 | Quality gate ≥ 80/100 | Kvalitet över kvantitet. Mediokra agenter slösar USB-utrymme. |
| D003 | VI som default på Machine-B | Hastighet över precision. NUTS endast för Machine-A. |
| D004 | JSON-lines logging | Maskinläsbart, append-safe, ingen DB-beroende. |
| D005 | YAML state (inte databas) | Människoläsbart, diffbart, noll beroenden. |
| D006 | Atomära writes för allt | USB-disconnect är risk #1. Temp-fil + rename. |
| D007 | Sekventiell loop (v3.0) | Fokuserad teacher attention. Parallell i v3.1+. |
| D008 | Per-blueprint skill loading | Renare kontext = vassare agenter. 3-5 skills, inte 85. |

---

## 2. Styde Forge Dashboard — Mission Control

**Status:** Phase 0 COMPLETE ✅ — 36 designdokument, 10 sektioner.

En **Tauri-baserad desktop-applikation** (`StydeForge.exe`) som är kommandocentralen för hela ekosystemet.

| Sektion | Innehåll |
|---------|----------|
| **00 Overview** | Vision, app-arkitektur, index |
| **01 Application Shell** | Fönsterhantering, livscykel, processkontroll, system tray |
| **02 UI/UX** | Layout, designsystem, komponentbibliotek, onboarding-flow |
| **03 Agent Monitor** | Live-spårning, detaljvy, spawna nya agenter |
| **04 Benchmark Panel** | Prestanda, kvalitet, visualisering |
| **05 Chat Interface** | Full AI-chat med tools (read/write files, terminal, web, skills) |
| **06 Model Provider System** | Multi-model: DeepSeek, OpenAI, Anthropic, custom REST, lokal Ollama |
| **07 System Control** | Start/pausa/stoppa Forge-pipeline med ett klick, konfiguration, hälsa |
| **08 Data Layer** | Hermes CLI bridge, polling, local storage, realtidsuppdateringar |
| **09 Technical Stack** | Tauri v2, Rust + React, bygg-pipeline, auto-update |
| **10 Phase Transition** | Phase 0 → Phase 1 roadmap |

---

## Top 20 Agenter — Världsklassprioritet

20 agenter designade för Forge-loopen. Rangordnade efter affärspåverkan.

### Tier 1 — Intäktsgeneratorer (Bygg först)

| # | Agent | Kundvärde |
|---|-------|-----------|
| 1 | **Consultant Auditor** | Crawlar sajt → klassificerar digital mognad → audit-rapport. SÄLJKROKEN. |
| 2 | **Invoice Processor** | PDF → extraherar radobjekt, moms, datum → JSON. 5-15h/vecka besparing. |
| 3 | **Customer Service Triage** | E-post/chat → klassificerar → utkast eller vidareskickning. Svarstid: timmar → sekunder. |
| 4 | **Meeting Summarizer** | Transkript → beslut, actions, ägare, deadlines. Noll post-mötes-admin. |
| 5 | **Email Drafter** | Kontext + företagskunskap → professionellt mail. 2-5h/vecka besparing. |

### Tier 2 — Effektivitetsmultiplikatorer

| # | Agent | Kundvärde |
|---|-------|-----------|
| 6 | **Document Classifier** | Klassificerar dokumenttyp → dirigerar. Grund för alla dokumentflöden. |
| 7 | **Contract Reviewer** | Kontrakt → nyckelklausuler, risker → flaggat. Juridisk granskning -70% tid. |
| 8 | **Report Writer** | Data + mall → polerad affärsrapport. 4h → 15 min. |
| 9 | **Data Cleaner** | Stökig spreadsheet → hittar dubbletter, fel, saknade värden → städar. |
| 10 | **Calendar Assistant** | Naturligt språk → hitta tider, boka, bjud in. 1-2h/vecka besparing. |

### Tier 3 — Förmågebyggare

| # | Agent | Kundvärde |
|---|-------|-----------|
| 11 | **Code Reviewer** | Kod → buggar, säkerhetshål, stilbrott → förslag. |
| 12 | **SQL Query Generator** | Naturligt språk + schema → korrekt SQL. Icke-tekniker kan fråga databaser. |
| 13 | **Translator (SV↔EN)** | Affärsdokument med rätt ton, terminologi, juridisk precision. |
| 14 | **Social Media Writer** | Företagsnyheter → plattformsoptimerade inlägg. |
| 15 | **Onboarding Guide** | Roll + handbok → personlig onboarding-plan. |

### Tier 4 — Specialiserade agenter

| # | Agent | Kundvärde |
|---|-------|-----------|
| 16 | **GDPR Compliance Checker** | Integritetspolicy → GDPR-luckor → artikelreferenser. Revision: veckor → timmar. |
| 17 | **Inventory Forecaster** | Försäljningshistorik → lagerprognos 30/60/90 dagar. |
| 18 | **Recruitment Screener** | CV:n + jobbeskrivning → rankade kandidater → screeningfrågor. 50 CV → topp 5. |
| 19 | **Competitor Monitor** | Konkurrentbevakning → förändringar → veckobrief. |
| 20 | **Meta-Improver** | Analyserar Forge eval-resultat → systemförbättringar. Gör ALLA andra agenter bättre. |

### Byggordning

```
Vecka 1-2:   #1 Consultant Auditor + #5 Email Drafter
Vecka 3-4:   #2 Invoice Processor + #3 Customer Service Triage
Vecka 5-6:   #6 Document Classifier + #10 Calendar Assistant
Vecka 7-8:   #4 Meeting Summarizer + #8 Report Writer + #7 Contract Reviewer
Vecka 9-10:  #16 GDPR Checker + #14 Social Media Writer
Vecka 11-12: #11 Code Reviewer + #20 Meta-Improver (startar självförbättringsloopen)
Vecka 13+:   Resterande agenter i prioritetsordning
```

---

## Phase 1 Roadmap — 50 funktioner

När kärnloopen fungerar. Prioritetstiers:

| Tier | Kriterium | När |
|------|-----------|-----|
| **P0 — Foundation** | Kärnloopen måste fungera först | Vecka 1-2 |
| **P1 — High Impact** | Stora vinster, implementerbart på dagar | Vecka 3-6 |
| **P2 — Scaling** | Behövs för 100+ agenter | Vecka 7-10 |
| **P3 — Excellence** | Polering, UX, långsiktigt | Fas 2+ |

### P0 — Foundation
1. Fungerande Core Loop (end-to-end)
2. Blueprint → Spawn → Eval pipeline
3. Atomic Checkpoint & Recovery
4. Hardware Detection & Adaptation
5. Caveman Ultra mode

### P1 — High Impact (urval)

**Multi-Agent:** Phase Gates, Task Decomposition Engine, Agent-to-Agent Communication, Hierarchical Multi-Agent, Agent Memory Sharing, Conflict Resolution, Specialized Agent Roles (7 st).

**Resurshantering:** Dynamic VRAM/RAM Allocation, GPU Load Balancing (3080 + 3070 Ti), Intelligent Queue System.

**Automation:** Automatic Benchmark Generation, Automatic Prompt Optimization, Curriculum Learning, Evolutionary Algorithms for Blueprints, Meta-Learning.

**RAG & Minne:** Knowledge Graph, Semantic Search over History, Memory Consolidation, Cross-Project Learning.

### P2 — Scaling (urval)
Anomaly Detection, Smart Caching, Batch Processing, Token Budgeting, Cost Forecasting, Versioned Vector Database, Immutable Event Log, Multi-Project Support.

### P3 — Excellence (urval)
Web UI / Command Center, Visual Loop Debugger, Blueprint Visual Editor, Plugin System, Forge Evolution Engine, Self-Improving Forge, Agent DNA / Genetic Representation.

Full roadmap: [[styde-forge/../Planing/v1.0_Phase1/PHASE1_ROADMAP]]

---

## Agent-livscykel (StydeAgents)

```
data/ ──→ refinery/ ──→ production/ ──→ archive/
 ↑                        │
 └──────── feedback ──────┘
```

| Katalog | Syfte | Status |
|---------|-------|--------|
| `data/` | Rådata — benchmarks, kunskap, mallar | Statisk |
| `refinery/` | Agenter i Forge-loopen (spawn → eval → improve) | Pågående |
| `production/` | Världsklass-agenter (≥ 85/100, 3 konsekutiva evals) | Redo |
| `archive/` | Pensionerade/underkända agenter | Lärdomar bevarade |

---

## Alpedals roll

| Ansvar | Prioritet | När |
|--------|-----------|-----|
| Designa agent-blueprints (Forge-format) | P0 | Sprint 01 → |
| Genomföra kund-audits | P0 | När första audit bokas |
| Äga Styde Forge — roadmap, design, implementation | P0 | Kontinuerligt |
| Testa Consultant Agent-output (kvalitetsgranskning) | P1 | Sprint 02 |
| Skriva mönster för AGENT_PATTERNS.md | P1 | Efter första agenter körs |
| Designa eval-rubriker för agentkvalitet | P2 | Fas 3 |

### Tillväxtbana

| Månad | Nivå |
|-------|------|
| **1-2** | Blueprint designer + audit-partner (ingen kod) |
| **3-4** | Börjar koda: enkla Python-script för audit-automation |
| **5-6** | Bygger Forge eval-script (Python) på delad server |
| **7+** | Självständig byggare — implementerar Forge core loop + dashboard |

---

## Arbetsflöde

1. Läs [[obsidian/_RULES]] — format, taggar, regler
2. Läs [[obsidian/01_plan/SPRINT_CURRENT]] — pågående sprint
3. Läs [[obsidian/01_plan/MASTER_PLAN]] — den enda planen
4. Designa blueprints här i `_alpedal/`
5. När en blueprint är mogen → exportera till `agent-blueprints/`
6. Logga alla ändringar → [[obsidian/05_ops/logs/_INDEX\|daglig logg]]

---

## Länkar

| Resurs | Sökväg |
|--------|--------|
| Master Plan | [[obsidian/01_plan/MASTER_PLAN]] |
| Pågående sprint | [[obsidian/01_plan/SPRINT_CURRENT]] |
| Sprint-log (dopamin) | [[obsidian/01_plan/SPRINT_LOG]] |
| Regler för botar | [[obsidian/_RULES]] |
| Forge arkitektur | [[styde-forge/00_Overview/Master_Architecture_Overview]] |
| Forge Phase 0 index | [[styde-forge/00_Overview/PHASE0_INDEX]] |
| Forge Phase 1 roadmap | [[styde-forge/../Planing/v1.0_Phase1/PHASE1_ROADMAP]] |
| Top 20 agenter | [[styde-forge/../Planing/Top_20_Agents]] |
| Blueprint-katalog | [[styde-forge/01_Vision/Blueprint_Catalog]] |
| Dashboard index | [[styde-forge/../Dashboard_Phase0/00_Overview/DASHBOARD_INDEX]] |
| Onboarding-process | [[obsidian/05_ops/ONBOARDING]] |
| Kund-offertmall | [[obsidian/04_CLIENTS/TEMPLATES/OFFERT_TEMPLATE]] |
| Audit-mall | [[obsidian/04_CLIENTS/TEMPLATES/AUDIT_TEMPLATE]] |

---

## Comments

- 2026-06-25 | hermes: README uppgraderad till full domän-dokumentation. Inkluderar Forge + Dashboard, Top 20 agenter, Phase 1 roadmap (50 funktioner), agent-livscykel, och arbetsflöde.
