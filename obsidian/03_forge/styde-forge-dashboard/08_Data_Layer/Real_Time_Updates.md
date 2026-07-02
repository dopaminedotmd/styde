# Real-Time Updates

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard needs real-time updates — agent status, performance, system health. Polling is the primary strategy (simple, reliable), with possible migration to WebSocket/SSE in the future.

---

## 2. Polling Architecture

```
┌─────────────────────────────────────────┐
│           Polling Architecture           │
│                                         │
│  UI ──→ Tauri Command ──→ Hermes CLI   │
│   ↑                          │          │
│   └──────── JSON ────────────┘          │
│                                         │
│  Each poll:                             │
│  1. Invoke hermes command               │
│  2. Parse JSON                          │
│  3. Diff against cache                  │
│  4. Update only changed data            │
│  5. Push to UI (delta only)             │
└─────────────────────────────────────────┘
```

---

## 3. Poll Frequencies

| Data | Frequency | Timeout | Strategy |
|------|-----------|---------|----------|
| Agent list | 2s | 5s | Fast — core data |
| Agent details (open) | 2s | 5s | Live update when detail view open |
| Performance metrics | 5s | 10s | Medium |
| System health | 10s | 15s | Slow — changes gradually |
| Cron jobs | 30s | 15s | Rare — status only |
| Skills | On startup | 10s | One-time |

---

## 4. Smart Polling

Poll frequency adapts dynamically:

```
┌──────────────────────────────────────────────────┐
│ Smart Polling Rules                              │
│                                                  │
│  Tab visible?        → Normal frequency          │
│  Tab hidden?         → Halved frequency          │
│  Window minimized?   → Minimal frequency (×0.25) │
│  No agents?          → 5s instead of 2s          │
│  High CPU (>80%)?    → Increase interval (+50%)  │
│  User scrolling?     → Pause non-visible polls   │
└──────────────────────────────────────────────────┘
```

---

## 5. Delta Updates

Instead of sending the entire agent list each time, send only changes:

```typescript
interface AgentDelta {
  added: Agent[];       // New agents
  removed: string[];    // IDs of removed agents
  updated: Agent[];     // Agents with changed status
}

function computeDelta(oldAgents: Agent[], newAgents: Agent[]): AgentDelta {
  const oldIds = new Set(oldAgents.map(a => a.id));
  const newIds = new Set(newAgents.map(a => a.id));

  return {
    added: newAgents.filter(a => !oldIds.has(a.id)),
    removed: oldAgents.filter(a => !newIds.has(a.id)).map(a => a.id),
    updated: newAgents.filter(a => {
      const old = oldAgents.find(o => o.id === a.id);
      return old && old.status !== a.status;
    })
  };
}
```

---

## 6. WebSocket/SSE (Phase 2+)

Future optimization — Hermes could expose a WebSocket server:

```
Dashboard ←──WebSocket──→ Hermes Agent
              │
              ├─ agent.status.changed
              ├─ agent.completed
              ├─ benchmark.updated
              └─ system.health
```

**Benefits:**
- Immediate updates (no poll delay)
- Lower bandwidth
- Server push

**Drawbacks:**
- Requires Hermes support (not available today)
- More complex (connection management, reconnect)
- Polling is "good enough" for MVP

---

## 7. Offline Handling

The Dashboard functions offline (except for cloud-model chat):

| Feature | Offline Behavior |
|---------|-----------------|
| Agent monitoring | Works (Hermes is local) |
| System health | Works (local data) |
| Local chat (Ollama) | Works |
| Cloud chat | Shows "Offline — switch to local model" |
| Web search | Inactive |

---

**Status:** Phase 0 — Design
