# Start / Stop Pipeline

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

System Control is the Dashboard's "power buttons" — start, pause, and stop the entire StydeForge Forge loop from one place. One click = the whole system reacts.

---

## 2. Control Bar (top bar)

```
┌──────────────────────────────────────────────────────────────┐
│ [▶ Start Forge] [⏸ Pause] [⏹ Stop] │ ⚙ │ ● Forge Running │
└──────────────────────────────────────────────────────────────┘
```

Three distinct buttons with clear icons and colors:

| Button | Color | Active when |
|--------|-------|-------------|
| ▶ Start | Green (`#10b981`) | Forge is STOPPED or PAUSED |
| ⏸ Pause | Yellow (`#f59e0b`) | Forge is RUNNING |
| ⏹ Stop | Red (`#ef4444`) | Forge is RUNNING or PAUSED |

---

## 3. Start Sequence

```
User clicks [▶ Start Forge]
        │
        ▼
┌─────────────────────────────────┐
│ 1. Pre-flight checks            │
│    • Config validated?          │
│    • At least one provider active?│
│    • Hermes CLI accessible?     │
│    • Sufficient disk/VRAM?      │
└────────────┬────────────────────┘
             │ ✅ All OK
             ▼
┌─────────────────────────────────┐
│ 2. Start Hermes Forge loop      │
│    $ hermes forge start         │
│    → Spawn as child process     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 3. Start cron jobs              │
│    (if auto-started in config)  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 4. Begin polling                │
│    Agent status every 2s        │
│    System health every 10s      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 5. UI updates                   │
│    ● Running — green dot        │
│    Status bar: active           │
│    Agent panel: live            │
└─────────────────────────────────┘
```

---

## 4. Pause Sequence

```
User clicks [⏸ Pause]
        │
        ▼
┌─────────────────────────────────┐
│ 1. Signal pause to Forge        │
│    $ hermes forge pause         │
│    → Send SIGINT                │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 2. Wait for current agents      │
│    to finish (max 60s)          │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 3. Pause cron jobs              │
│    Set status=paused on all     │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ 4. UI updates                   │
│    ● Paused — yellow dot        │
│    "Forge Paused — 2 agents     │
│     waiting in queue"           │
└─────────────────────────────────┘
```

---

## 5. Stop Sequence

```
User clicks [⏹ Stop]
        │
        ▼
┌─────────────────────────────────┐
│ Confirmation dialog             │
│ ┌─────────────────────────────┐ │
│ │ Stop StydeForge?            │ │
│ │                             │ │
│ │ 3 agents are running.       │ │
│ │ 2 cron jobs are active.     │ │
│ │                             │ │
│ │ [Force Stop]  [Graceful]   │ │
│ │              [Cancel]      │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

**Graceful Stop (recommended):**

```
1. Signal stop
   $ hermes forge stop --graceful
   → Let agents finish (timeout: 30s)

2. Save checkpoints
   All active agents save their state

3. Stop cron jobs
   Set status=paused

4. Kill Hermes process
   SIGTERM → 5s → SIGKILL

5. UI updates
   ● Stopped — red dot (grey if idle)
```

**Force Stop (emergency):**

```
1. SIGKILL directly to Hermes process
2. All agents aborted (no checkpoint)
3. Cron jobs paused
4. Warning: "Force stop — work may be lost"
```

---

## 6. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+S` | Start Forge |
| `Ctrl+Shift+P` | Pause Forge |
| `Ctrl+Shift+X` | Stop Forge |

---

## 7. Edge Cases

| Scenario | Behavior |
|----------|----------|
| Start when already running | Button inactive — "Already running" |
| Stop when already stopped | Button inactive — "Already stopped" |
| Start without providers | Dialog: "No AI providers configured. Set up a provider first." → Open provider settings |
| Start without Hermes CLI | Dialog: "Hermes CLI not found. Install Hermes Agent first." |
| Pause with 0 agents | Goes to paused state immediately |
| Dashboard closed while Forge running | Minimize to tray (see Lifecycle Management) |

---

**Status:** Phase 0 — Design
