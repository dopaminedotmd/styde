---
name: ca-agent-builder
description: Standard och mall för att bygga och driftsätta AI-agent-system åt kunder (prompt.md, tools.yaml, config.yaml). Använd denna skill vid utveckling, testning och driftsättning av klientagenter.
version: 1.1.0
owner: william
last-updated: 2026-06-25
---

# ca-agent-builder

## Purpose

Build and deliver AI agent systems for customers according to the styde standard.

## Agent Structure (per agent)

Each agent must be created with the following three files in its dedicated directory:
- `prompt.md` — Contains the system prompt (mission, rules, format).
- `tools.yaml` — Defines all external APIs and tools.
- `config.yaml` — Contains environment variables, schedules, and triggers.

Directory structure:
```
agents/
└── {customer_name}/
    └── {agent_name}/
        ├── prompt.md
        ├── tools.yaml
        ├── config.yaml
        ├── handler.py      # (Optional: custom code)
        └── tests/          # Test scenarios
            ├── input.json
            └── expected.json
```

## Prompt Design Template (prompt.md)

The system prompt must follow this format:

```markdown
# Agent: {AGENT_NAME}

## MISSION
{Exact description of what the agent should do and its role}

## TOOLS
- {Tool 1}: {description and purpose}
- {Tool 2}: {description and purpose}

## RULES
- {Rule 1}: {restrictions and what the agent must NOT do}
- {Rule 2}: {security requirements}

## OUTPUT FORMAT
{Structured response or JSON format that the dashboard expects}
```

## Tool Definitions (tools.yaml)

Tools (API, SMTP, databases) must be defined declaratively:

```yaml
tools:
  - name: {tool_name}
    type: api | smtp | database
    endpoint: {url or connection string}
    auth: api_key | oauth | basic
    methods: [GET, POST]
```

## Security Requirements

- **Sandbox:** Each agent runs in an isolated sandbox.
- **Secrets:** API keys are stored in encrypted configuration or environment variables, never hardcoded in prompts.
- **Logging:** All agent calls and actions are logged centrally.
- **Audit trail:** Every action must have a unique ID for traceability.
- **Destructive actions:** Require manual approval (e.g., deletion, payment).

## Deployment Flow

1. **Dev:** Build the agent and test locally with `tests/input.json`.
2. **Test:** Deploy in dev/staging environment and run verification tests.
3. **Approval:** Demonstrate the agent to the customer for formal approval.
4. **Prod:** Deploy to the customer's production environment.
5. **Monitoring:** Actively monitor the agent's behavior for the first 48 hours.

## Comments

- 2026-06-25 | hermes: Updated description to Swedish, bumped version to 1.1.0 and added comments section.
- 2026-06-25 | hermes: Translated body prose from Swedish to English. Added translation note.

---
**Translation note:** This file was translated from Swedish to English on 2026-06-25. All frontmatter YAML fields remain unchanged.
