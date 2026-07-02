# Application Architecture

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    StydeForge.exe                        │
│                   (Desktop Application)                   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │                  UI Layer (HTML/CSS/JS)             │  │
│  │  ┌───────────┐  ┌────────────┐  ┌───────────────┐  │  │
│  │  │  Agents   │  │ Benchmarks │  │    Chat       │  │  │
│  │  │  Panel    │  │   Panel    │  │    Panel      │  │  │
│  │  └─────┬─────┘  └─────┬──────┘  └───────┬───────┘  │  │
│  └────────┼──────────────┼─────────────────┼──────────┘  │
│           │              │                 │              │
│  ┌────────┴──────────────┴─────────────────┴──────────┐  │
│  │                Core Controller                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │  │
│  │  │Process   │  │Benchmark │  │ Chat Controller  │  │  │
│  │  │Monitor   │  │Engine    │  │                  │  │  │
│  │  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │  │
│  └───────┼─────────────┼────────────────┼────────────┘  │
│          │             │                │                │
│  ┌───────┴─────────────┴────────────────┴────────────┐  │
│  │                  Data Layer                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │  │
│  │  │ Hermes   │  │ Local DB │  │ Provider API     │ │  │
│  │  │ CLI      │  │(IndexedDB│  │ Layer            │ │  │
│  │  │ Bridge   │  │ /SQLite) │  │                  │ │  │
│  │  └──────────┘  └──────────┘  └──────────────────┘ │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Desktop Shell (Tauri)                  │  │
│  │  • Window management    • System tray              │  │
│  │  • Native file dialogs  • Auto-start               │  │
│  │  • Process spawning     • File system access       │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
         │                 │                  │
         ▼                 ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│ Hermes CLI   │  │ File System  │  │ AI Provider APIs │
│ (hermes ...) │  │ (D:/, /logs) │  │ (DeepSeek,       │
│              │  │              │  │  OpenAI, Custom)  │
└──────────────┘  └──────────────┘  └──────────────────┘
```

---

## 2. Layers

### 2.1 Desktop Shell (Tauri)

Responsibilities:
- Create the application window
- System tray integration (minimize, notifications)
- Start/stop Hermes as child process
- Native features: filesystem, file dialogs, auto-start
- Low resource usage (Rust backend, ~5-10MB)

### 2.2 UI Layer (HTML/CSS/JS)

Three main panels in a responsive grid:
- **Agent Panel** (left 30%) — agent list, status, details
- **Benchmark Panel** (center/right 35%) — graphs, performance data
- **Chat Panel** (right/bottom 35%) — chat with full agent

### 2.3 Core Controller

Business logic:
- **Process Monitor** — polls Hermes CLI, keeps agent list synchronized
- **Benchmark Engine** — collects performance data, computes graphs
- **Chat Controller** — manages provider selection, tool calls, streaming

### 2.4 Data Layer

- **Hermes CLI Bridge** — calls `hermes process list`, `hermes cronjob list`, etc.
- **Local DB** — stores history (agent history, chat logs, benchmarks)
- **Provider API Layer** — abstract interface to AI models

---

## 3. Tech Stack (preliminary)

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Desktop Shell | **Tauri v2** (Rust) | Small .exe (~5MB), native performance, memory efficient |
| UI Rendering | HTML/CSS/JS via Tauri WebView | Full flexibility, easy styling |
| Charts | Chart.js (lightweight) | Good performance, dark theme support |
| Chat Rendering | Markdown + syntax highlighting | Code blocks, tables, formatting |
| Local DB | IndexedDB (MVP) → SQLite (Phase 2) | No server dependencies |
| Process Communication | Tauri Command API (Rust ↔ JS) | Safe IPC, typed |
| Build System | Tauri CLI + GitHub Actions | Build .exe for Windows |

---

## 4. Communication Flows

### 4.1 Agent Monitoring

```
UI ──→ Core Controller ──→ Hermes CLI Bridge ──→ hermes process list
                                                      │
UI ←── Core Controller ←── Hermes CLI Bridge ←───────┘
(polls every 2 seconds)
```

### 4.2 Chat with Tools

```
User: "read D:/config.yaml"
        │
Chat Controller:
  1. Send to chosen AI Provider (DeepSeek/OpenAI/etc.)
     with tool definitions
  2. Provider responds: tool_call: read_file("D:/config.yaml")
  3. Chat Controller executes via Tauri filesystem API
  4. Result sent back to provider
  5. Provider formulates response
  6. Streamed to UI (markdown)
```

### 4.3 System Control

```
UI [▶ Start] ──→ Core Controller ──→ Tauri spawn process
                                        │
                              ┌─────────┴──────────┐
                              │ Hermes process     │
                              │ (Forge loop)       │
                              └────────────────────┘

UI [⏹ Stop] ──→ Core Controller ──→ kill process
                              ┌─────────┴──────────┐
                              │ Graceful shutdown  │
                              │ → save checkpoints │
                              │ → stop cron jobs   │
                              └────────────────────┘
```

---

## 5. Security Model

| Feature | Risk | Mitigation |
|---------|------|------------|
| Chat runs terminal commands | Malicious commands | Confirmation dialog for all commands, sandbox mode |
| Chat writes files | Overwrites important files | Show diff before write, `--dry-run` first |
| Chat reads files | Reads sensitive data | No mitigation — user's responsibility (local app) |
| Custom providers | API keys stored | Encrypted local storage (OS keychain) |

---

## 6. Configuration

`StydeForge.exe` reads config from:
```
%APPDATA%/StydeForge/config.json
```

```json
{
  "hermes_path": "C:/Users/Pontus/.hermes/",
  "providers": {
    "deepseek": {
      "api_key": "sk-...",
      "default_model": "deepseek-v4-pro"
    },
    "openai": {
      "api_key": "sk-...",
      "default_model": "gpt-4o"
    }
  },
  "ui": {
    "theme": "dark",
    "font_size": 14,
    "start_minimized": false
  },
  "forge": {
    "auto_start": false,
    "stop_on_exit": true
  }
}
```

---

**Status:** Phase 0 — Design
