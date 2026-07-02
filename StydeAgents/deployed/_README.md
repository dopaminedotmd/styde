# Deployed Agents — Live Client Deliveries

Each subfolder is a running agent deployment: `{kund_id}/{agent_id}/`.

## Structure per Agent

```
{kund_id}/
├── {agent_id}/
│   ├── blueprints/         — frozen copy of the blueprint at deploy time
│   ├── config/             — runtime config (env vars, secrets refs)
│   ├── data/               — agent working data (logs, outputs)
│   └── README.md           — deployment record
```

## Active Deployments

*None yet.*
