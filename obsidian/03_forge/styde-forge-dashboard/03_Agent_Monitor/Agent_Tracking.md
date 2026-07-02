# Agent Tracking

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Agent panel displays all active, completed, and failed agents in real-time. Data is fetched from Hermes CLI (`hermes process list --json`) and polled every 2 seconds.

---

## 2. Agent Types

| Type | Source | Description |
|------|--------|-------------|
| **Forge Agent** | `hermes process list` | Agents spawned by Forge loop |
| **Cron Job Agent** | `hermes cronjob list` | Scheduled jobs |
| **Manual Agent** | Spawned via Dashboard "New Agent" button | Manually started agent |
| **Chat Agent** | Chat panel | Agent running in chat (visible if spawning sub-agents) |

---

## 3. Agent List — Visual Design

```
┌──────────────────────────────────────────┐
│ 📡 AGENTS                        [3] [↻]│
├──────────────────────────────────────────┤
│                                          │
│ ● code-reviewer-v3              87/100  │
│   deepseek-v4-flash · 2m 34s            │
│   4.2K tokens · $0.012 · ⚡ 45 t/s       │
│   ████████████████████░░ 87%            │
│                                          │
│ ● test-generator-v2             64/100  │
│   deepseek-v4-flash · 1m 12s            │
│   2.1K tokens · $0.006 · ⚡ 38 t/s       │
│   ████████████░░░░░░░░ 64%              │
│                                          │
│ ✓ doc-writer-v1                  92/100 │
│   deepseek-v4-pro · 3m 45s              │
│   6.8K tokens · $0.019                   │
│   ✅ Completed                           │
│                                          │
│ ✗ sql-helper-v2                   FAIL  │
│   deepseek-v4-flash · 0m 23s            │
│   Error: API timeout                     │
│   🔄 Retry                              │
│                                          │
└──────────────────────────────────────────┘
```

---

## 4. Agent Card — Fields

| Field | Source | Format |
|-------|--------|--------|
| **Status** | Hermes process status | ● running / ✓ done / ✗ failed / ⏸ paused |
| **Name** | Agent blueprint name | `code-reviewer-v3` |
| **Score** | Eval result | `87/100` (shown only when done) |
| **Model** | Which model the agent uses | `deepseek-v4-flash` |
| **Time** | How long it has run | `2m 34s` (running) / `3m 45s` (done) |
| **Tokens** | Tokens used | `4.2K` |
| **Cost** | Estimated cost | `$0.012` |
| **Speed** | Tokens per second | `⚡ 45 t/s` (running only) |
| **Progress bar** | % of expected time/tokens | ████████░░ 87% |
| **Error** | Error message (if failed) | `API timeout` |

---

## 5. Live Updates

```
┌─────────────────────────────────────────┐
│           Poll Loop (every 2s)          │
│                                         │
│  hermes process list --json             │
│         │                               │
│         ▼                               │
│  ┌──────────────────┐                   │
│  │ Compare to cache │                   │
│  └────┬─────────┬───┘                   │
│       │         │                       │
│   New agent   Status change             │
│       │         │                       │
│       ▼         ▼                       │
│  ┌────────┐ ┌──────────┐               │
│  │Add to  │ │Update    │               │
│  │list    │ │existing  │               │
│  │(slide) │ │(morph)   │               │
│  └────────┘ └──────────┘               │
└─────────────────────────────────────────┘
```

**Optimizations:**
- Diff JSON — only send changes to UI
- Only re-render visible agents (virtual scroll for 50+ agents)
- Status dot animates only for running agents

---

## 6. Filtering & Sorting

```
┌──────────────────────────────────────────┐
│ 📡 AGENTS        [All ▼] [Most Recent ▼] │
├──────────────────────────────────────────┤
```

| Filter | Options |
|--------|---------|
| Status | All, Running, Completed, Failed, Paused |
| Model | All, deepseek-v4-flash, deepseek-v4-pro, ... |
| Type | All, Forge, Cron, Manual |

| Sort | Description |
|------|-------------|
| Most Recent | Last updated first (default) |
| Score | Highest score first |
| Time | Longest runtime first |
| Cost | Highest cost first |

---

## 7. Interactions

| Interaction | Result |
|-------------|--------|
| **Click agent** | Open Agent Detail View (right panel or modal) |
| **Double-click** | Focus agent output/log |
| **Right-click** | Context menu: View Details, Stop, Restart, Export |
| **✗ on failed agent** | Dismiss (hide from list, save to history) |
| **🔄 on failed agent** | Retry — restart agent with same parameters |

---

## 8. Empty States

| Scenario | Display |
|----------|---------|
| Forge not started | "No agents active. [Start Forge] to begin spawning." |
| Forge started, no agents yet | "Forge is running. Waiting for first agent spawn..." + spinner |
| All agents completed | "All agents completed. 3/3 passed quality gate (≥80)." |
| Filter yields 0 results | "No agents match filter 'Failed'. [Clear filter]" |

---

## 9. Agent History

Completed agents saved in local database (IndexedDB):
- Show last 100 agents
- Search historical agents
- Export agent data as JSON/CSV

---

**Status:** Phase 0 — Design
