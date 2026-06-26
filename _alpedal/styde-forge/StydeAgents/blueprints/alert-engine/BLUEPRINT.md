# Alert Engine — Blueprint

## Purpose

Monitor agent, GPU, and system telemetry against configurable alert rules and push real-time notifications to the Forge Dashboard when thresholds are breached.

## Overview

The **Alert Engine** is the monitoring and notification subsystem within the Forge Dashboard. It continuously evaluates configurable alert rules against live telemetry from agents, GPU clusters, and system resources. When a rule threshold is breached, it triggers a push notification directly in the dashboard.

## Architecture

```
┌─────────────────────┐
│   Telemetry Sources  │
│  ┌─────┐ ┌────┐ ┌──┐│
│  │Agent│ │GPU │ │RAM││
│  └──┬──┘ └─┬──┘ └┬─┘│
│     │      │     │   │
└─────┼──────┼─────┼───┘
      │      │     │
      ▼      ▼     ▼
┌─────────────────────┐
│   Alert Evaluator    │
│  ┌─────────────────┐│
│  │  Rule Engine     ││
│  │  • Thresholds    ││
│  │  • Cooldowns     ││
│  │  • Severities    ││
│  └────────┬────────┘│
└───────────┼─────────┘
            │ trigger
            ▼
┌─────────────────────┐
│  Notification Bus   │
│  ┌─────────────────┐│
│  │  Push Dispatcher ││
│  │  → Dashboard UI  ││
│  └─────────────────┘│
└─────────────────────┘
```

## Alert Rules

| Rule ID       | Metric              | Threshold         | Severity | Cooldown |
|---------------|---------------------|-------------------|----------|----------|
| gpu-temp      | GPU Temperature     | > 85 °C           | critical | 5 min    |
| ram-usage     | RAM Utilization     | > 90 %            | warning  | 10 min   |
| agent-failure | Agent Failure Rate  | > 10 %            | critical | 15 min   |
| score-drop    | Agent Score Drop    | > 15 points       | warning  | 30 min   |

## Flow

1. Telemetry sources publish metrics at regular intervals.
2. The Alert Evaluator checks every metric against all active rules.
3. On breach: a notification event is created, respecting per-rule cooldown.
4. The Notification Bus dispatches a push notification to the dashboard.
5. The user sees the alert in the dashboard notification panel.

## States

- **Normal** — all metrics within bounds.
- **Alerting** — threshold breached; notification sent.
- **Cooldown** — alert fired recently; suppressed until cooldown expires.
- **Recovered** — metric returned to normal; optional recovery notification.

## Configuration

All rules are defined in `config.yaml`. The engine reloads config on startup and can be hot-reloaded via a dashboard admin action.
