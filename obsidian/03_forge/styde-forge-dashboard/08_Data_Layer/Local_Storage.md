# Local Storage

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard uses a combination of local storage layers for different data types. All data is local — nothing leaves the machine.

---

## 2. Storage Layers

```
┌─────────────────────────────────────────────────────┐
│                  Storage Layers                      │
│                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ IndexedDB   │  │ localStorage │  │ File System │  │
│  │             │  │              │  │             │  │
│  │ • Sessions  │  │ • UI state   │  │ • Config    │  │
│  │ • Messages  │  │ • Panel size │  │ • Logs      │  │
│  │ • Agents    │  │ • Last model │  │ • Exports   │  │
│  │ • Benchmarks│  │ • Theme prefs│  │ • Backups   │  │
│  │ • Metrics   │  │              │  │             │  │
│  └─────────────┘  └──────────────┘  └────────────┘  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 3. IndexedDB — Main Database

### 3.1 Database: `stydeforge_dashboard`

```
Version 1:
├── sessions        (chat sessions)
├── messages        (chat messages)
├── agents          (agent history)
├── benchmarks      (performance data)
└── metrics         (system health over time)
```

### 3.2 Store: `agents`

```typescript
interface AgentRecord {
  id: string;                    // UUID
  name: string;
  blueprint: string;
  model: string;
  status: "running" | "completed" | "failed" | "cancelled";
  score?: number;
  score_breakdown?: Record<string, number>;
  tokens_in: number;
  tokens_out: number;
  cost_usd: number;
  duration_ms: number;
  started_at: string;            // ISO 8601
  finished_at?: string;
  error?: string;
  output?: string;
  log?: string;
}
```

### 3.3 Store: `benchmarks`

```typescript
interface BenchmarkRecord {
  id: string;                    // UUID
  agent_id: string;
  timestamp: string;             // ISO 8601
  model: string;
  tokens_per_second: number;
  ttft_ms: number;               // Time to first token
  total_tokens: number;
  cost_usd: number;
}
```

---

## 4. localStorage — UI State

```json
{
  "ui_state": {
    "active_tab": "chat",
    "panel_widths": {
      "agents": 0.30,
      "benchmarks": 0.35
    },
    "window_position": { "x": 100, "y": 50 },
    "window_size": { "width": 1400, "height": 900 },
    "window_maximized": false
  },
  "last_used": {
    "chat_model": "deepseek-v4-pro",
    "provider": "deepseek"
  },
  "onboarding_complete": true
}
```

---

## 5. File System — Config and Data

### 5.1 Config File

```
%APPDATA%/StydeForge/config.json
```

Dashboard's main configuration (see Configuration Panel).

### 5.2 API Keys

```
Windows Credential Manager:
  Target: StydeForge/deepseek
  Target: StydeForge/openai
  Target: StydeForge/anthropic
```

OS keychain — encrypted, secure.

### 5.3 Exports

```
Documents/StydeForge/exports/
  session-2026-06-25-code-review.json
  agent-code-reviewer-v3-output.md
```

### 5.4 Backups

```
%APPDATA%/StydeForge/backups/
  config-2026-06-25.json
  sessions-2026-06-25.json
```

---

## 6. Storage Limits

| Layer | Max Size | Cleanup Strategy |
|-------|----------|------------------|
| IndexedDB | 500MB (varies per webview) | Purge oldest-first at 80% |
| localStorage | 5-10MB | Minimal usage |
| Config file | Unlimited | Small file |
| Export folder | Unlimited | Manual |
| Backup folder | 100MB | Keep 5 most recent |

---

## 7. Migration

Database schema is versioned for future migrations:

```typescript
const DB_VERSION = 1;

const request = indexedDB.open("stydeforge_dashboard", DB_VERSION);

request.onupgradeneeded = (event) => {
  const db = event.target.result;
  const oldVersion = event.oldVersion;

  if (oldVersion < 1) {
    // Create initial stores
    db.createObjectStore("sessions", { keyPath: "id" });
    db.createObjectStore("messages", { keyPath: "id" });
    db.createObjectStore("agents", { keyPath: "id" });
    db.createObjectStore("benchmarks", { keyPath: "id" });
    db.createObjectStore("metrics", { keyPath: "id" });
  }

  // if (oldVersion < 2) { ... }  // Future migrations
};
```

---

**Status:** Phase 0 — Design
