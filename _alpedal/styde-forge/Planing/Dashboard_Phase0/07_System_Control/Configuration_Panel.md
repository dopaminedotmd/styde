# Configuration Panel

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

All configuration in one place. No manual config-file editing — everything through the UI.

---

## 2. Settings View

```
┌──────────────────────────────────────────────────────────┐
│ ⚙ SETTINGS                                               │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [Providers] [Forge] [Appearance] [Chat] [Advanced]      │
│                                                          │
│  ┌─ Forge Settings ────────────────────────────────────┐ │
│  │                                                      │ │
│  │ Hermes Profile: [default          ▼]                 │ │
│  │ Hermes Path: [C:/Users/Pontus/.hermes________]       │ │
│  │                                                      │ │
│  │ Default Agent Model: [deepseek-v4-flash ▼]           │ │
│  │ Default Eval Model:  [deepseek-v4-pro  ▼]            │ │
│  │ Teacher Model:       [deepseek-v4-pro  ▼]            │ │
│  │                                                      │ │
│  │ Max Concurrent Agents: [4__]                         │ │
│  │ Agent Timeout (min):   [30__]                        │ │
│  │                                                      │ │
│  │ ☑ Caveman Ultra Mode (default on)                    │ │
│  │ ☑ Auto-evaluate after completion                     │ │
│  │ ☐ Save failed agents (score < 80)                    │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌─ Appearance ────────────────────────────────────────┐ │
│  │                                                      │ │
│  │ Theme: Dark (only)                                   │ │
│  │ Font Size: [14__] px                                 │ │
│  │ Font: [JetBrains Mono_____________]                  │ │
│  │                                                      │ │
│  │ Default Layout: [3 panels ▼]                         │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌─ Chat Settings ─────────────────────────────────────┐ │
│  │                                                      │ │
│  │ Default Chat Model: [deepseek-v4-pro ▼]              │ │
│  │                                                      │ │
│  │ ☑ Streaming enabled                                  │ │
│  │ ☑ Show tool calls in chat                            │ │
│  │ ☑ Auto-save sessions                                 │ │
│  │ ☐ Confirm before tool execution                      │ │
│  │                                                      │ │
│  │ Max Context Messages: [50___]                        │ │
│  │ Session Auto-Cleanup: [90___] days                   │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌─ Advanced ──────────────────────────────────────────┐ │
│  │                                                      │ │
│  │ ☐ Start with Windows                                 │ │
│  │ ☐ Auto-start Forge on launch                         │ │
│  │ ☑ Minimize to tray on close                          │ │
│  │ ☑ Show notifications                                 │ │
│  │                                                      │ │
│  │ Log Level: [INFO_____ ▼]                             │ │
│  │ Log Path: [C:/Users/Pontus/.hermes/logs_______]      │ │
│  │                                                      │ │
│  │ [Export All Settings]  [Import Settings]              │ │
│  │ [Reset to Defaults]                                  │ │
│  │                                                      │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                          │
│  [Close]  [Save]                                        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Setting Categories

### 3.1 Providers

See `06_Model_Provider_System/Provider_Configuration_UI.md`

### 3.2 Forge

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| Hermes Profile | Dropdown | `default` | Which Hermes profile to use |
| Hermes Path | Path | `~/.hermes` | Path to Hermes installation |
| Default Agent Model | Dropdown | `deepseek-v4-flash` | Model for agent spawning |
| Default Eval Model | Dropdown | `deepseek-v4-pro` | Model for evaluation |
| Teacher Model | Dropdown | `deepseek-v4-pro` | Model for teacher agent |
| Max Concurrent Agents | Number | 4 | Max simultaneous agents |
| Agent Timeout | Number | 30 | Max time per agent (minutes) |
| Caveman Ultra | Checkbox | true | 70% fewer tokens, 2× faster |
| Auto-evaluate | Checkbox | true | Run eval after each agent |
| Save failed | Checkbox | false | Save agents below quality gate |

### 3.3 Appearance

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| Font Size | Number | 14 | Base font size in px |
| Font | Dropdown | JetBrains Mono | Font (monospace) |
| Default Layout | Dropdown | 3 panels | Startup layout |

### 3.4 Chat

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| Default Chat Model | Dropdown | `deepseek-v4-pro` | Model for chat |
| Streaming | Checkbox | true | Stream responses token-by-token |
| Show Tool Calls | Checkbox | true | Show tool calls in chat |
| Auto-save | Checkbox | true | Auto-save sessions |
| Confirm Tools | Checkbox | false | Confirm before write/terminal |
| Max Context | Number | 50 | Max messages in context |
| Auto-Cleanup | Number | 90 | Purge sessions older than X days |

### 3.5 Advanced

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| Start with Windows | Checkbox | false | Auto-start on Windows login |
| Auto-start Forge | Checkbox | false | Start Forge on launch |
| Minimize to tray | Checkbox | true | Close = minimize to tray |
| Notifications | Checkbox | true | Show Windows notifications |
| Log Level | Dropdown | INFO | INFO / DEBUG / WARN / ERROR |
| Log Path | Path | `~/.hermes/logs` | Log file path |

---

## 4. Configuration Format

```json
{
  "version": "1.0",
  "forge": {
    "hermes_profile": "default",
    "hermes_path": "C:/Users/Pontus/.hermes",
    "agent_model": "deepseek-v4-flash",
    "eval_model": "deepseek-v4-pro",
    "teacher_model": "deepseek-v4-pro",
    "max_concurrent_agents": 4,
    "agent_timeout_minutes": 30,
    "caveman_ultra": true,
    "auto_evaluate": true,
    "save_failed": false
  },
  "appearance": {
    "font_size": 14,
    "font": "JetBrains Mono",
    "default_layout": "3-panels"
  },
  "chat": {
    "default_model": "deepseek-v4-pro",
    "streaming": true,
    "show_tool_calls": true,
    "auto_save": true,
    "confirm_tools": false,
    "max_context_messages": 50,
    "auto_cleanup_days": 90
  },
  "advanced": {
    "start_with_windows": false,
    "auto_start_forge": false,
    "minimize_to_tray": true,
    "notifications": true,
    "log_level": "INFO",
    "log_path": "C:/Users/Pontus/.hermes/logs"
  }
}
```

---

## 5. Validation

| Field | Validation |
|-------|------------|
| Hermes Path | Must point to an existing directory containing `hermes` binary |
| Agent Timeout | 1-120 minutes |
| Max Concurrent Agents | 1-16 |
| Font Size | 10-24 px |
| Max Context Messages | 10-200 |

---

## 6. Import / Export

| Action | Description |
|--------|-------------|
| Export Settings | JSON file — ALL settings (except API keys) |
| Import Settings | Load JSON → merge (not replace) |
| Reset Defaults | Reset ALL to factory defaults → confirmation dialog |

---

**Status:** Phase 0 — Design
