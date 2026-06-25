# Lifecycle Management

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard is the master controller for the entire StydeForge system. Three states:

```
         ┌──────────────┐
    ┌───→│  STOPPED     │←───┐
    │    └──────┬───────┘    │
    │           │ [Start]    │ [Stop]
    │           ▼            │
    │    ┌──────────────┐    │
    │    │  RUNNING     │────┘
    │    └──────┬───────┘
    │           │ [Pause]
    │           ▼
    │    ┌──────────────┐
    └────│  PAUSED      │
         └──────────────┘
              │ [Start] = Resume
```

---

## 2. State: STOPPED

**UI indicator:** Red status dot + "StydeForge: Inactive"

| Property | Value |
|----------|-------|
| Hermes processes | No Forge processes running |
| Cron jobs | Paused |
| Agent panel | Shows "No agents active" |
| System resources | Dashboard uses minimal CPU/RAM |
| On exit | Prompt whether to start Forge |

---

## 3. State: RUNNING

**UI indicator:** Green status dot + "StydeForge: Running — 3 agents active"

**Startup sequence:**

```
Dashboard [▶ Start]
     │
     ├─→ 1. Validate config
     │      └─ Check all providers have API keys
     │
     ├─→ 2. Start Hermes Forge loop
     │      └─ Spawn as child process: hermes forge start
     │
     ├─→ 3. Start cron jobs
     │      └─ If auto-start of specific jobs is configured
     │
     └─→ 4. Begin polling agent status
            └─ Every 2 seconds: hermes process list
```

**Child process management:**
- Hermes runs as child process under Dashboard
- Dashboard owns the process lifecycle
- If Dashboard crashes → Hermes gets graceful shutdown
- If Hermes crashes → Dashboard shows error, offers restart

---

## 4. State: PAUSED

**UI indicator:** Yellow status dot + "StydeForge: Paused"

| Component | Action |
|-----------|--------|
| Agent spawning | No new agents started |
| Active agents | Allowed to finish current task |
| Cron jobs | Temporarily disabled (set to pause mode) |
| Eval pipeline | Paused after current evaluation |
| Dashboard UI | Continues updating, shows paused status |

**Resume:** Click [▶ Start] → everything resumes where it was.

---

## 5. Stop Sequence (Graceful Shutdown)

```
Dashboard [⏹ Stop]
     │
     ├─→ 1. Show confirmation dialog
     │      "Stop StydeForge? 3 agents currently running."
     │      [Stop Anyway] [Wait Until Done] [Cancel]
     │
     ├─→ 2. Signal stop to Forge loop
     │      └─ Let current agents finish (timeout: 30s)
     │
     ├─→ 3. Save checkpoints
     │      └─ All active agents save their state
     │
     ├─→ 4. Stop cron jobs
     │      └─ Set status=paused on all active cron jobs
     │
     ├─→ 5. Kill Hermes process
     │      └─ SIGTERM → wait 5s → SIGKILL
     │
     └─→ 6. Update UI
            └─ Red dot, "StydeForge: Inactive"
```

---

## 6. Edge Cases

| Scenario | Behavior |
|----------|----------|
| User closes window (✕) | If Forge running: minimize to tray (default) or prompt |
| User closes via tray | Close fully (if Forge not running) or prompt |
| Windows shutdown/reboot | Dashboard captures WM_QUERYENDSESSION → graceful shutdown |
| Power loss / force kill | Next start: "Forge shut down unexpectedly. Restore?" → run recovery |
| Double-launch of Dashboard | Second instance detects first → focus existing window → exit |

---

## 7. Auto-Start

Optional (⚙ settings):
- Start Dashboard with Windows
- Auto-start Forge when Dashboard opens
- Start minimized to system tray

---

**Status:** Phase 0 — Design
