# Blueprints — Agent Designs

Blueprints define the spec for an agent: persona, prompts, tools, cost, and expected time savings. Each blueprint maps to a deployable agent for a specific business process.

## Registered Blueprints

| Blueprint | Category | Version | Status | Author |
|-----------|----------|---------|--------|--------|
| invoice-reviewer | finance | 1.0.0 | designed | alpedal |
| customer-service-triage | support | 1.0.0 | designed | alpedal |
| mail-sorter | operations | 1.0.0 | designed | alpedal |

## Blueprint Format

Each blueprint folder contains:

```
blueprint.yaml   — metadata, cost, requirements
persona.md       — agent personality, tone, role
prompt_template.md — system prompt with {{variables}}
tools.yaml       — external tools and API access
tests/           — optional: input.json + expected.json
```

**Gold references** for blueprint design live in `_alpedal/styde-forge/StydeAgents/refinery/`.
