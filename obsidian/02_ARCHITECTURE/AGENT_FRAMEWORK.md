---
title: "Agent Framework — Hur vi bygger AI-agenter"
date: 2026-06-24
author: william
tags: [area/ARKITEKTUR, status/DRAFT, author/WILLIAM, type/SPEC]
status: draft
---

# Agent Framework — How We Build AI Agents

> [!note] Framework
> Template and structure for every AI agent we build for customers.
> Last updated: 2026-06-24

## What is an Agent?

An agent is an AI unit that:
- Has a specific mission (a system prompt)
- Has access to tools (API calls, databases, file systems)
- Runs automatically (cron/trigger) or manually (button in dashboard) (see [[DASHBOARD_SPEC]])
- Returns a result displayed in the dashboard

## Agent Structure (Per Agent)

```
agents/
├── {customer_name}/
│   ├── {agent-name}/
│   │   ├── prompt.md       # System prompt (mission, rules, output format)
│   │   ├── tools.yaml      # Tools the agent has access to
│   │   ├── config.yaml     # Schedule, triggers, environment variables
│   │   ├── handler.py      # (if custom code is needed) Execution logic
│   │   └── tests/
│   │       ├── input.json
│   │       └── expected.json
│   └── README.md           # Overview of customer's agents
```

## Prompt Design (Template)

```
# Agent: {NAME}

## MISSION
{Exact description of what the agent does}

## TOOLS
- {Tool 1}: {description}
- {Tool 2}: {description}

## RULES
- {Rule 1}: {what the agent must NOT do}
- {Rule 2}: {security rules}

## OUTPUT FORMAT
{Structured output that the dashboard expects}
```

## Tools

Each agent has access to specific tools. Defined in tools.yaml.

```yaml
tools:
  - name: fortnox_get_invoices
    type: api
    endpoint: https://api.fortnox.se/3/invoices
    auth: api_key
    methods: [GET, POST]
```

## Security

- Each agent runs in sandbox (isolation)
- API keys stored in encrypted config, never in prompt
- All actions are logged (see [[SYSTEM_OVERVIEW]] API Gateway)
- Manual approval for destructive actions (delete, pay)
- Audit trail: each agent action has a unique ID

## Deployment

1. Build agent in dev environment
2. Test with test input
3. Approved by customer (demo) (see [[ONBOARDING]])
4. Deploy to production
- Monitor first 48h (responsible: [[william|William]])

## Comments

- 2026-06-24 | william: created
- 2026-06-24 | hermes: Linked to dashboard spec, system overview, onboarding, and tech lead role.

> *Translated from Swedish to English by Hermes on 2026-06-25.*
