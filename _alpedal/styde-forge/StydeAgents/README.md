# StydeAgents

Agent lifecycle storage. Three states, one flow.

```
data/ ──→ refinery/ ──→ production/ ──→ archive/
 ↑                        │
 └──────── feedback ──────┘
```

| Directory | Purpose | State |
|-----------|---------|-------|
| `data/` | Raw data — benchmarks, knowledge, templates | Static, never modified by agents |
| `refinery/` | Agents in the Forge loop (spawn → eval → improve) | In progress, iterating |
| `production/` | World-class agents (≥ 80/100), ready to deploy | Complete, deployed |
| `archive/` | Retired/rejected agents with lessons preserved | Read-only, reference |

## Move Rules

| From | To | When |
|------|----|------|
| `refinery/` | `production/` | Agent reaches ≥ 85/100 on 3 consecutive evals |
| `production/` | `archive/` | Agent deprecated or replaced by better version |
| `refinery/` | `archive/` | Agent fails ≥ 80/100 after 3 improvement cycles |
