# Window Management

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Window Behavior

```
┌─────────────────────────────────────────────────────────────┐
│ StydeForge — Mission Control                          ─ □ ✕│
├─────────────────────────────────────────────────────────────┤
│ [▶ Start] [⏸ Pause] [⏹ Stop] [⚙ Settings]                │
├──────────────────┬──────────────────────┬───────────────────┤
│                  │                      │                   │
│   AGENT PANEL    │   BENCHMARK PANEL    │   CHAT PANEL      │
│   (30%)          │   (35%)              │   (35%)           │
│                  │                      │                   │
│                  │                      │                   │
│                  │                      │                   │
│                  │                      │                   │
├──────────────────┴──────────────────────┴───────────────────┤
│ Status: ● Forge Running | 3 agents active | 12.4K tokens   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Specifications

| Property | Value | Note |
|----------|-------|------|
| Default size | 1400×900 px | Comfortably fits all 3 panels |
| Minimum size | 900×600 px | Panels collapse to tabs below 1100px |
| Maximized | Fullscreen with margins | Optimized for 1080p and 1440p |
| Position | Remembers last position | Saved in config |
| Always on top | Toggle (⚙ settings) | For "mission control" feel |
| Title bar | Custom dark title bar | Not Windows default |
| Rounded corners | 8px border-radius | Modern feel |

---

## 3. Panel Layout

### 3.1 Standard Layout (≥1400px width)

```
┌──────────┬───────────────┬───────────────┐
│ AGENTS   │ BENCHMARKS    │ CHAT          │
│          │               │               │
│ 30%      │ 35%           │ 35%           │
│          │               │               │
│ scroll   │ scroll        │ scroll        │
└──────────┴───────────────┴───────────────┘
```

### 3.2 Compact Layout (900-1399px)

```
┌─────────────────┬──────────────────────┐
│ AGENTS (40%)    │ CHAT (60%)           │
│                 │                      │
│ BENCHMARKS      │                      │
│ (hidden — tab   │                      │
│  at top)        │                      │
└─────────────────┴──────────────────────┘
```

### 3.3 Minimal Layout (<900px)

```
┌────────────────────────────────────────┐
│ [Agents] [Benchmarks] [Chat]  ← tabs  │
├────────────────────────────────────────┤
│                                        │
│          Active panel                  │
│                                        │
└────────────────────────────────────────┘
```

---

## 4. Draggable Panels

All panel borders are **draggable** (resize handles):
- Cursor changes to ↔ at panel boundary
- Minimum panel width: 200px
- Layout saved in localStorage, restored on next launch
- Double-click panel boundary → reset to default proportions

---

## 5. Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| `Ctrl+1` | Focus Agent panel |
| `Ctrl+2` | Focus Benchmark panel |
| `Ctrl+3` | Focus Chat panel |
| `Ctrl+Shift+S` | Start Forge |
| `Ctrl+Shift+P` | Pause Forge |
| `Ctrl+Shift+X` | Stop Forge |
| `Ctrl+,` | Open Settings |
| `Ctrl+K` | Focus chat input |
| `Escape` | Blur/unfocus input field |

---

## 6. Multi-Monitor

| Scenario | Behavior |
|----------|----------|
| Primary screen (1080p) | Standard layout, maximized |
| Secondary screen (1440p/4K) | Move window = keep layout, scale up |
| 3+ screens | Remember position per screen configuration |

---

## 7. Window State

Window state saved in config:
```json
{
  "window": {
    "x": 100,
    "y": 50,
    "width": 1400,
    "height": 900,
    "maximized": false,
    "always_on_top": false,
    "panels": {
      "agents_width": 0.30,
      "benchmarks_width": 0.35
    }
  }
}
```

---

**Status:** Phase 0 — Design
