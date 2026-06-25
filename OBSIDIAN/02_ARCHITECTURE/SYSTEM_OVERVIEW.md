---
title: "System Overview — Arkitektur"
date: 2026-06-24
author: william
tags: [area/ARKITEKTUR, status/DRAFT, author/WILLIAM, type/SPEC]
status: draft
---

# System Overview — Architecture

> [!note] Architecture
> Technical architecture for styde.
> Last updated: 2026-06-24

## High Level

```mermaid
graph TD
    KP[Customer Staff] <--> DB[Dashboard (UI)]
    DB <--> AG[API Gateway]
    AG --> A1[Agent 1]
    AG --> A2[Agent 2]
    AG --> AN[Agent N]
    A1 --> INT[Integrations: APIs, databases, file systems]
    A2 --> INT
    AN --> INT
    classDef default fill:#F4F4F6,stroke:#1A1A1A,stroke-width:1px;
```

## Components

### 1. Dashboard (Frontend)
- Built by [[william|William]]
- Modern webapp (React? Svelte? William chooses)
- Login, role management, activity log
- Each agent has a "button" or automated trigger
- Base MVP: list agents, status, history, manual trigger (see [[DASHBOARD_SPEC]])

### 2. API Gateway (Backend)
- Handles auth, routing, logging
- Receives requests from dashboard
- Routes to the right agent
- Returns results to dashboard

### 3. AI Agents
- Each agent is an isolated AI unit
- Built with framework (Next.js + Tailwind) (see [[LINKS]])
- The agent has: system prompt + tools (API calls) (see [[AGENT_FRAMEWORK]])
- Agents can be:
  - **Triggered** (click in dashboard) — "Send the report"
  - **Scheduled** (cron) — "Check invoices every Monday"
  - **Event-driven** (webhook) — "When email arrives, process it"

### 4. Integrations
- Connects agents to customer systems
- Common: Google Workspace, Office 365, Slack, email, databases, file servers
- Custom API integrations per customer

## MVP (Minimum)

Dashboard: One page listing agents, one button per agent, a log.
Backend: Express, auth, routing.
Agents: Python-based, one prompt + tools.

[[william|William]] chooses tech stack. This spec describes WHAT to build, not HOW (see [[MASTER_PLAN_FINAL]] for approved tech stack).

## Future Development

- Agent library (reusable agent components)
- Self-service portal for easier deployment
- Customer-specific training of agents
- Analytics: what do the agents do? What does the customer save?

## Comments

- 2026-06-24 | william: created
- 2026-06-24 | hermes: Linked to team, dashboard spec, agent spec, master plan, and added Mermaid diagram.

> *Translated from Swedish to English by Hermes on 2026-06-25.*
