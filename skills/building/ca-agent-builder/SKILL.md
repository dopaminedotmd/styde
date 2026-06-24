---
name: ca-agent-builder
description: Template for building AI agents for clients. Prompt design, tools, security.
version: 1.0.0
owner: elb
last-updated: 2026-06-24
---

# ca-agent-builder

## Syfte

Bygga och leverera AI-agent-system för kunder enligt Consulting.ai-standard.

## Agent-struktur (per agent)

Varje agent ska skapas med följande tre filer i sin dedikerade katalog:
- `prompt.md` — Innehåller systemprompt (uppdrag, regler, format).
- `tools.yaml` — Definierar alla externa API:er och verktyg.
- `config.yaml` — Innehåller miljövariabler, schedules och triggers.

Katalogstruktur:
```
agents/
└── {kundnamn}/
    └── {agentnamn}/
        ├── prompt.md
        ├── tools.yaml
        ├── config.yaml
        ├── handler.py      # (Valfritt: custom-kod)
        └── tests/          # Testsituationer
            ├── input.json
            └── expected.json
```

## Prompt-design-mall (prompt.md)

Systemprompten ska följa detta format:

```markdown
# Agent: {AGENTNAMN}

## UPPDRAG
{Exakt beskrivning av vad agenten ska göra och dess roll}

## VERKTYG
- {Tool 1}: {beskrivning och syfte}
- {Tool 2}: {beskrivning och syfte}

## REGLER
- {Regel 1}: {begränsningar och vad agenten INTE får göra}
- {Regel 2}: {säkerhetsföreskrifter}

## OUTPUT-FORMAT
{Strukturerat svar eller JSON-format som dashboarden förväntar sig}
```

## Verktygsdefinition (tools.yaml)

Verktyg (API, SMTP, databaser) ska definieras deklarativt:

```yaml
tools:
  - name: {verktygsnamn}
    type: api | smtp | database
    endpoint: {url eller anslutningssträng}
    auth: api_key | oauth | basic
    methods: [GET, POST]
```

## Säkerhetskrav

- **Sandbox:** Varje agent körs i en isolerad sandbox.
- **Secrets:** API-nycklar lagras i krypterad konfiguration eller miljövariabler, aldrig hårdkodade i prompts.
- **Loggning:** Alla agent-anrop och åtgärder loggas centralt.
- **Audit trail:** Varje åtgärd ska ha ett unikt ID för spårbarhet.
- **Destruktiva åtgärder:** Kräver manuellt godkännande (t.ex. radering, betalning).

## Deployments-flöde

1. **Dev:** Bygg agenten och testa lokalt med `tests/input.json`.
2. **Test:** Driftsätt i dev/staging-miljö och kör verifieringstester.
3. **Godkännande:** Demonstrera agenten för kunden för formellt godkännande.
4. **Prod:** Deploya till kundens produktionsmiljö.
5. **Monitorering:** Övervaka agentens beteende aktivt under de första 48 timmarna.
