---
title: "MASTER PLAN — Huvudplan för styde.ai"
date: 2026-06-25
author: hermes
tags: [area/PLAN, status/APPROVED, author/HERMES, type/PLAN]
status: approved
---

# MASTER PLAN — styde.ai

> En gemensam källa till sanning för hela styde.ai. Ersätter alla tidigare implementationsplaner, roadmaps och faser.

---

## 1. Vad vi är
styde.ai bygger och driftar skräddarsydda AI-agentsystem för svenska små och medelstora företag (SMEs). Vi arbetar enligt modellen: **Audit → Build → Operate**.

---

## 2. Teamet
- **William:** Builder + Seller. Äger plattform, kod, infrastruktur, server och kundrelationer.
- **Alpedal:** Auditor + Blueprint Designer. Äger agentkvalitet, logiska mönster, audits och blueprint-specifikationer.

---

## 3. Faserna (sekventiella, körs ej parallellt)

### Fas 1: FIRST BLOOD (Vecka 1-3)
**Mål:** Bygg Consultant Agent v0.1 (CLI) och boka det första säljmötet.
- **Sprint 01:** Consultant Agent v0.1 (Python CLI) + serverkonfiguration (SSH/nvm/pg) + 3 initiala blueprints.
- **Sprint 02:** Testa Consultant Agent på 5 verkliga sajter + fixa buggar + utvärdera kvalitet.
- **Sprint 03:** Säljförberedelser: Skapa en automatiserad PDF-rapportmall från agentens output + audit-processbeskrivning.

### Fas 2: FIRST CUSTOMER (Vecka 4-8)
**Mål:** 20 säljutskick per dag → landa första auditen → leverera första betalda agentsystemet.
- **Sprint 04-05:** Sälj och uppsökande verksamhet (20 leads/dag). Utrullning av första audits.
- **Sprint 06-07:** Genomför första riktiga kundauditen och skriv rapporten.
- **Sprint 08-09:** Bygg kundens agenter utifrån Alpedals blueprints.
- **Sprint 10-11:** Driftsätt agenterna på vår delade server och verifiera driften.

### Fas 3: THE MOAT (Vecka 9-16)
**Mål:** Dashboard + evaluerings-pipeline + självlärande agenter baserade på körningshistorik.
- **Dashboard:** En Next.js-app med rollbaserad behörighet (Customer + Admin i samma app).
- **Eval Pipeline v1:** Självutvärdering + Judge-modell efter varje agentkörning.
- **RAG Engine v1:** Lokal RAG (om servern har GPU) eller Pinecone (om vi har 3+ kunder).

### Fas 4: SCALE (Månad 4-12)
**Mål:** 5+ kunder under drift, 1.5M - 2.0M SEK ARR.
- Återanvändbart bibliotek av agent-blueprints.
- Kontinuerlig förbättring av mallar via historisk eval-data.

---

## 4. Arkitekturöversikt
Systemet bygger på en centraliserad utveckling och körning:
- **Shared Server:** Fysisk maskin med Ubuntu Server 24.04 LTS.
- **Next.js + Express API:** Dashboard och runtime på samma maskin.
- **PostgreSQL:** Sparar kunder, loggar och agenttillstånd.
- **Agent Blueprints:** Strukturerade YAML/Markdown-definitioner enligt Alpedals format.

---

## 5. Serverkonfiguration
Utveckling och produktion körs på en delad fysisk server för maximal kostnadseffektivitet, låg latens och lokal datasäkerhet (GDPR). Detaljerad instruktion finns i [[SERVER_SETUP]].

---

## 6. Gällande Beslut
- **Caveman Mode:** Alla interna bot-prompter ska köras med Caveman-komprimering för att spara 70%+ av tokens.
- **GDPR först:** Kunddata sparas lokalt på vår server. Inga molntjänster för känsliga rådata.
- **Modeller:** Vi använder befintliga API-nycklar (OpenAI/Anthropic) för agenternas LLM-anrop.
- **Inget kodande utan Mini-spec:** Alla funktioner i svalan måste brainstormas enligt `ca-brainstorming` innan kod skrivs.

---

## 7. Vad vi uttryckligen INTE bygger än
Följande sparas i backloggen och byggs **inte** i Fas 1 eller Fas 2:
- **StydeForge Desktop (Tauri-app):** Deprioriterad. Alpedal använder CLI/SSH eller Next.js-dashboard.
- **Pinecone / Vektor-databaser:** Vi använder enkla markdown-filer för mönster tills vi har minst 3 kunder.
- **FAISS lokalt:** William har ett GTX 980 Ti med 4GB VRAM. Inga tunga lokala inbäddningsmodeller körs i Fas 1.
- **Publik hemsida med inloggning:** Vi kör dashboard via Cloudflare Tunnel med begränsad access först.

---

## Comments
- 2026-06-25 | hermes: Skapad efter godkänd total reboot. Ersätter alla gamla planer.
