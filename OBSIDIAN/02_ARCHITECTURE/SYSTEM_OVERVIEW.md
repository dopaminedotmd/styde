---
title: "System Overview — Arkitektur"
date: 2026-06-24
author: william
tags: [area/ARKITEKTUR, status/DRAFT, author/WILLIAM, type/SPEC]
status: draft
---

# System Overview — Arkitektur

> [!note] Arkitektur
> Teknisk arkitektur för styde.
> Senast uppdaterad: 2026-06-24

## Hög nivå

```mermaid
graph TD
    KP[Kundens personal] <--> DB[Dashboard (UI)]
    DB <--> AG[API Gateway]
    AG --> A1[Agent 1]
    AG --> A2[Agent 2]
    AG --> AN[Agent N]
    A1 --> INT[Integrationer: API:er, databaser, filsystem]
    A2 --> INT
    AN --> INT
    classDef default fill:#F4F4F6,stroke:#1A1A1A,stroke-width:1px;
```

## Komponenter

### 1. Dashboard (frontend)
- Byggs av [[william|William]]
- Modern webapp (React? Svelte? William väljer själv)
- Inloggning, rollhantering, aktivitetslogg
- Varje agent har en "knapp" eller automatiserad trigger
- Grund-MVP: lista agenter, status, historik, manuell trigger (se [[DASHBOARD_SPEC]])

### 2. API Gateway (backend)
- Hanterar auth, routing, logging
- Tar emot requests från dashboard
- Skickar till rätt agent
- Returnerar resultat till dashboard

### 3. AI Agents
- Varje agent är en isolerad AI-enhet
- Byggs med ramverk (Next.js + Tailwind) (se [[LINKS]])
- Agenten har: system prompt + tools (API-anrop) (se [[AGENT_FRAMEWORK]])
- Agenter kan vara:
  - **Triggerade** (klick i dashboard) — "Skicka rapporten"
  - **Schemalagda** (cron) — "Kolla fakturor varje måndag"
  - **Event-drivna** (webhook) — "När mail kommer, processa"

### 4. Integrationer
- Ansluter agenter till kundens system
- Vanliga: Google Workspace, Office 365, Slack, email, databaser, filservrar
- Anpassade API-integrationer per kund

## MVP (minimum)

Dashboard: En sida som listar agenter, en knapp per agent, en logg.
Backend: Express, auth, routing.
Agenter: Python-baserade, en prompt + tools.

[[william|William]] väljer tech stack. Denna spec beskriver VAD som ska byggas, inte HUR (se [[MASTER_PLAN_FINAL]] för godkänd teknik-stack).

## Framtida utveckling

- Agent-bibliotek (återanvändbara agentkomponenter)
- Self-service portal för enklare deployment
- Kund-specifik träning av agenter
- Analytics: vad gör agenterna? Vad sparar kunden?

## Kommentarer

- 2026-06-24 | william: skapad
- 2026-06-24 | hermes: Länkat till team, dashboard-spec, agent-spec, masterplan, och lagt till Mermaid-diagram.
