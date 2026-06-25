---
title: "Agent Framework — Hur vi bygger AI-agenter"
date: 2026-06-24
author: william
tags: [area/ARKITEKTUR, status/DRAFT, author/WILLIAM, type/SPEC]
status: draft
---

# Agent Framework — Hur vi bygger AI-agenter

> [!note] Ramverk
> Mall och struktur för varje AI-agent vi bygger åt kund.
> Senast uppdaterad: 2026-06-24

## Vad är en agent?

En agent är en AI-enhet som:
- Har ett specifikt uppdrag (en system prompt)
- Har tillgång till verktyg (API-anrop, databaser, filsystem)
- Körs automatiskt (cron/trigger) eller manuellt (knapp i dashboard) (se [[DASHBOARD_SPEC]])
- Returnerar ett resultat som visas i dashboard

## Agent-struktur (per agent)

```
agents/
├── {kundnamn}/
│   ├── {agent-name}/
│   │   ├── prompt.md       # System prompt (uppdrag, regler, output-format)
│   │   ├── tools.yaml      # Verktyg agenten har tillgång till
│   │   ├── config.yaml     # Schedule, triggers, miljövariabler
			│   │   ├── handler.py      # (om custom-kod behövs) Körlogik
│   │   └── tests/
│   │       ├── input.json
│   │       └── expected.json
│   └── README.md           # Översikt av kundens agenter
```

## Prompt-design (mall)

```
# Agent: {NAMN}

## UPPDRAG
{Exakt beskrivning av vad agenten gör}

## VERKTYG
- {Tool 1}: {beskrivning}
- {Tool 2}: {beskrivning}

## REGLER
- {Regel 1}: {vad agenten INTE får göra}
- {Regel 2}: {säkerhetsregler}

## OUTPUT-FORMAT
{Strukturerad output som dashboarden förväntar sig}
```

## Verktyg (tools)

Varje agent har tillgång till specifika verktyg. Definieras i tools.yaml.

```yaml
tools:
  - name: fortnox_get_invoices
    type: api
    endpoint: https://api.fortnox.se/3/invoices
    auth: api_key
    methods: [GET, POST]
```

## Säkerhet

- Varje agent körs i sandbox (isolering)
- API-nycklar lagras i krypterad config, aldrig i prompt
- Alla åtgärder loggas (se [[SYSTEM_OVERVIEW]] API Gateway)
- Manuellt godkännande för destruktiva handlingar (radera, betala)
- Audit trail: varje agent-action har ett unikt ID

## Deployment

1. Bygg agent i dev-miljö
2. Testa med test-input
3. Godkänn av kund (demo) (se [[ONBOARDING]])
4. Deploya till produktion
- Monitorera första 48h (ansvar: [[william|William]])

## Kommentarer

- 2026-06-24 | william: skapad
- 2026-06-24 | hermes: Länkat till dashboard-spec, systemöversikt, onboarding, och tech lead roll.
