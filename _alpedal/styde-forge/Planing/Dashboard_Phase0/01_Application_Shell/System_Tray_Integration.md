# System Tray Integration

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard minimizes to system tray instead of closing entirely — so Forge can keep running in the background.

```
Windows System Tray (taskbar, right side)
┌──────────────────────────────────────────┐
│  ▲  🌐  🔊  [S]  15:34              │
│              ↑                          │
│         StydeForge icon                 │
└──────────────────────────────────────────┘

Right-click icon:
┌────────────────────┐
│ Open Dashboard     │
│ ─────────────      │
│ Status: ● Running  │
│ Agents: 3 active   │
│ Tokens: 12.4K      │
│ ─────────────      │
│ ▶ Start Forge      │
│ ⏸ Pause Forge     │
│ ⏹ Stop Forge      │
│ ─────────────      │
│ ⚙ Settings        │
│ ─────────────      │
│ Exit               │
└────────────────────┘
```

---

## 2. Tray Icon

| Property | Description |
|----------|-------------|
| Icon | Stylized "S" (StydeForge logo) — 16×16 and 32×32 px |
| Color (active) | Green — Forge running |
| Color (paused) | Yellow — Forge paused |
| Color (inactive) | Gray — Forge stopped |
| Color (error) | Red — Forge crashed or errored |

---

## 3. Minimize Behavior

| Action | Result |
|--------|--------|
| Click ✕ (close button) | Minimize to tray (if Forge running) |
| Click ✕ (Forge not active) | Prompt: "Close or minimize?" |
| Double-click tray icon | Open/restore Dashboard window |
| Right-click → Open Dashboard | Restore window, focus |
| Windows+D (show desktop) | Dashboard minimizes normally |
| Alt+Tab | Dashboard visible in Alt+Tab list |

---

## 4. Notifications

Dashboard sends Windows notifications for key events:

| Event | Notification |
|-------|-------------|
| Agent completed (score ≥80) | "✅ Agent 'code-reviewer v3' done! Score: 87/100" |
| Agent completed (score <80) | "⚠ Agent 'sql-helper' scored 62/100 — below quality gate" |
| Forge crashed | "🔴 StydeForge crashed. Click to view log." |
| High resource usage | "⚠ CPU 92% for 30s — may impact performance" |
| Checkpoint saved | "💾 Checkpoint saved: 2026-06-25 15:42" |
| New version available | "🔄 StydeForge v1.1 available! Click to update." |

---

## 5. Notification Interaction

| Click on notification | Result |
|----------------------|--------|
| Agent notification | Open Dashboard → focus agent detail view |
| Crash notification | Open Dashboard → show error log |
| Update notification | Start update process |

---

## 6. Configuration

```json
{
  "tray": {
    "minimize_to_tray": true,
    "show_notifications": true,
    "notification_events": [
      "agent_completed",
      "agent_failed",
      "forge_crashed",
      "update_available"
    ],
    "start_minimized": false
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `minimize_to_tray` | true | Close = minimize to tray |
| `show_notifications` | true | Show Windows notifications |
| `notification_events` | ["agent_completed", "agent_failed", "forge_crashed", "update_available"] | Events that trigger notifications |
| `start_minimized` | false | Start Dashboard minimized on Windows startup |

---

## 7. Edge Cases

| Scenario | Behavior |
|----------|----------|
| Dashboard starts while Forge already running (from previous session) | Detect existing process, attach to it, don't prompt |
| Windows Explorer crashes/restarts | Tray icon auto-recreated |
| User "closes" via tray while Forge running | Prompt: "Forge is running. [Stop Forge + Exit] [Minimize] [Cancel]" |
| Tray icon not visible (Windows hides it) | Use system "show all icons"; Dashboard shows instruction on first run |

---

**Status:** Phase 0 — Design
