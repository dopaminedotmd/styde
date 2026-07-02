# StydeAgents

Central catalog for all agent blueprints, internal agents, and deployed client deliveries.

## Structure

| Path | Purpose |
|------|---------|
| `blueprints/` | Agent designs (persona, prompt, tools, blueprint.yaml) |
| `deployed/` | Live client deployments: `{kund_id}/{agent_id}/` |
| `internal/` | Styde's own agents (consultant agent, audits, etc.) |
| `templates/` | Scaffold templates for new blueprints and agents |

## Conventions

- New blueprints start as a copy of `templates/blueprint/`
- Deployed agents use production-grade prompts from their blueprint
- Internal agents live here as symlink/reference pointers to `apps/`
- All blueprints authored by Alpedal, code built by William
