# Layout Design

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Main Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ StydeForge — Mission Control                              ─ □ ✕ │
├──────────────────────────────────────────────────────────────────┤
│ [▶ Start] [⏸ Pause] [⏹ Stop]  │ ⚙ │ ● Forge Running — 3 agents│
├──────────────┬───────────────────────┬───────────────────────────┤
│              │                       │                           │
│   AGENTS     │    BENCHMARKS         │    CHAT                   │
│              │                       │                           │
│ ┌──────────┐ │  ┌─────────────────┐  │ ┌───────────────────────┐ │
│ │Agent 1   │ │  │  Tokens/s ████  │  │ │ User: optimize my     │ │
│ │● running │ │  │  Latency  ██    │  │ │ config                │ │
│ │deepseek  │ │  │  Cost     █     │  │ │                       │ │
│ └──────────┘ │  └─────────────────┘  │ │ Agent: Reading your    │ │
│ ┌──────────┐ │                       │ │ config.yaml...         │ │
│ │Agent 2   │ │  ┌─────────────────┐  │ │                       │ │
│ │✓ done    │ │  │  Eval Scores    │  │ │ ───────────────────── │ │
│ │87/100    │ │  │  ████████░░ 78% │  │ │                       │ │
│ └──────────┘ │  └─────────────────┘  │ │ [Type message...]     │ │
│ ┌──────────┐ │                       │ └───────────────────────┘ │
│ │Agent 3   │ │  ┌─────────────────┐  │                           │
│ │✗ failed │ │  │  Model compare  │  │                           │
│ └──────────┘ │  └─────────────────┘  │                           │
│              │                       │                           │
├──────────────┴───────────────────────┴───────────────────────────┤
│ Status: ● Running | 3/3 agents | 12,432 tokens | $0.037 cost     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Grid System

CSS Grid-based layout:

```css
.dashboard {
  display: grid;
  grid-template-columns: 30% 35% 35%;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "titlebar titlebar titlebar"
    "agents   benches  chat"
    "status   status   status";
  height: 100vh;
}
```

| Grid Area | Content | Height |
|-----------|---------|--------|
| `titlebar` | Custom title bar + control buttons + status | 48px |
| `agents` | Agent panel — scrollable list | flex 1 |
| `benches` | Benchmark panel — charts | flex 1 |
| `chat` | Chat panel — messages + input | flex 1 |
| `status` | Status bar — tokens, cost, agents | 32px |

---

## 3. Title Bar

```
┌──────────────────────────────────────────────────────────────────┐
│ [S] StydeForge — Mission Control                          ─ □ ✕ │
├──────────────────────────────────────────────────────────────────┤
│ [▶ Start] [⏸ Pause] [⏹ Stop] │ ⚙ │ ● Forge Running — 3 active │
└──────────────────────────────────────────────────────────────────┘
```

| Element | Position | Description |
|---------|----------|-------------|
| Logo | Left, 24×24px | "S" in a hexagon |
| Title | Left, after logo | "StydeForge — Mission Control" |
| Control buttons | Left, after title | Start/Pause/Stop with icons |
| Settings | Right, before window buttons | ⚙ gear icon |
| Status indicator | Between controls and ⚙ | Green/Yellow/Red dot + text |
| Window buttons | Far right | Minimize/Maximize/Close |

---

## 4. Panel Design

### 4.1 Panel Header

Each panel has a header:

```
┌────────────────────────┐
│ 📡 AGENTS    [📌] [✕] │  ← header: icon + title + pin/close
├────────────────────────┤
│                        │
│   Content              │  ← scrollable content
│                        │
└────────────────────────┘
```

### 4.2 Panel Properties

| Property | Description |
|----------|-------------|
| Header height | 36px |
| Background | `#1a1a2e` (dark blue) |
| Border | 1px `#2a2a4a` between panels |
| Scrollbar | Custom thin (6px), dark |
| Min width | 200px |
| Resize handle | 4px wide, cursor changes to `col-resize` |

### 4.3 Panel Tabs (compact mode)

When window is <1100px wide:

```
┌──────────────────────┐
│ [Agents][Bench][Chat] │  ← tabs
├──────────────────────┤
│                      │
│  Active panel        │
│                      │
└──────────────────────┘
```

---

## 5. Status Bar

```
┌──────────────────────────────────────────────────────────────────┐
│ ● Running | 3 agents | 12,432 tokens | $0.037 | ⚡ 45 t/s | 23°C│
└──────────────────────────────────────────────────────────────────┘
```

| Field | Format | Update Interval |
|-------|--------|-----------------|
| Status | ●/○ icon + text | On state change |
| Agents | "X agents" | Every 2s |
| Tokens | "12.4K tokens" | Every 10s |
| Cost | "$0.037" | Every 10s |
| Speed | "⚡ 45 t/s" | Every 10s |
| CPU temp | "23°C" | Every 30s |

---

## 6. Responsive Design

| Breakpoint | Layout |
|-----------|--------|
| ≥1400px | Three panels side by side (30/35/35) |
| 1100-1399px | Two panels (agents + chat), benchmarks as tab |
| 900-1099px | Two panels (40/60) |
| <900px | One panel at a time with tabs |

---

## 7. Empty States

| State | Display |
|-------|---------|
| No agents | "No agents active. Start Forge or spawn manually." + [Start Forge] button |
| No benchmarks | "No benchmark data yet. Run agents to collect metrics." |
| Empty chat | "StydeForge Chat — ask me anything. I can read/write files, run commands, and use skills." |
| Forge not started | All panels show empty states, status bar: "● Stopped" |

---

**Status:** Phase 0 — Design
