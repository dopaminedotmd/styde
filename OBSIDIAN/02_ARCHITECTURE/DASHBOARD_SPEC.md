---
title: "Dashboard Spec — v1 (MVP)"
date: 2026-06-24
author: william
tags: [area/ARKITEKTUR, status/DRAFT, author/WILLIAM, type/SPEC]
status: draft
---

# Dashboard Spec — v1 (MVP)

> [!note] Specifikation
> Specifikation för första versionen av kunddashboarden.
> Senast uppdaterad: 2026-06-24

## Syfte

Kundens personal ska kunna:
1. Se alla aktiva AI-agenter (se [[AGENT_FRAMEWORK]])
2. Starta/trigga en agent manuellt
3. Se historik — vad har agenterna gjort?
4. Se status — fungerar allt? (se [[SYSTEM_OVERVIEW]])

## Skärmar (MVP)

### 1. Dashboard Home

```
[Header: styde — Företagsnamn]
[Statusrad: Alla agenter aktiva ✓]

[Agentkort 1]  [Agentkort 2]  [Agentkort 3]
  Namn           Namn           Namn
  Status: OK     Status: OK     Status: PAUSAD
  Senast: idag   Senast: igår  Senast: måndag
  [Kör nu]       [Kör nu]      [Kör nu]
```

Varje agentkort visar:
- Agentnamn (eget, t.ex. "Fakturahanteraren")
- Statusindikator (aktiv/pausad/fel)
- Senaste körning
- Knapp: "Kör nu"
- Klick → detaljvy

### 2. Agentdetalj

```
[Tillbaka]                        [Redigera inställningar]

## Fakturahanteraren

Status: Aktiv OK
Skapad: 2026-05-01
Senaste körning: 2026-06-24 08:30 (OK — 12 fakturor processade)

Senaste 10 körningar:
| Tid | Status | Resultat |
|-----|--------|----------|
| 08:30 idag | OK | 12 fakturor |
| 08:30 igår | OK | 8 fakturor |
| 08:30 måndag | Fel | Anslutning misslyckades |

[Kör nu]  [Pausa agent]  [Visa logg]
```

### 3. Aktivitetsslogg

```
## All aktivitet — senaste 30 dagarna

| Tid | Agent | Händelse | Status |
|-----|-------|----------|--------|
| 08:30 idag | Fakturahanteraren | Automatisk körning | OK |
| 07:15 idag | Mailhanteraren | Manuell körning (Kalle) | OK |
| 16:00 igår | Rapportsystemet | Automatisk körning | FEL |
```

## Tekniska krav (MVP)

- Inloggning: enkel e-post + lösenord
- Roller: admin (full) / viewer (se bara)
- Mobilvänlig (responsiv)
- Ladda snabbt (<2s)
- Bone White #E3E3E4 som basfärg (aldrig vit) (se [[MASTER_PLAN_FINAL]] design-standarder)

## Designprinciper

- Renskrivet, modernt, professionellt
- Statusindikatorer ska synas direkt
- Kräver ingen utbildning — kunden fattar direkt
- Fel ska synas rött och tydligt

## Framtida versioner

- Diagram och statistik
- Kostnadsbesparing per agent
- Multi-tenant admin (vår adminpanel)
- Rolhantering (anpassade per kund)
- Notifikationer (email, Slack)

## Kommentarer

- 2026-06-24 | william: skapad
- 2026-06-24 | hermes: Länkat till agent-framework, systemöversikt och designriktlinjer.
