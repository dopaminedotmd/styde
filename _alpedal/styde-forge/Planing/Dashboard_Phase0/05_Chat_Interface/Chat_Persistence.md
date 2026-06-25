# Chat Persistence

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

All chat sessions are stored locally in IndexedDB. No data leaves the machine. Sessions can be loaded, searched, exported, and deleted.

---

## 2. Data Storage

### 2.1 Database Schema (IndexedDB)

```
Database: stydeforge_dashboard
├── Object Store: sessions
│   ├── id (string, primary key)
│   ├── title (string)
│   ├── created_at (ISO timestamp)
│   ├── updated_at (ISO timestamp)
│   ├── model (string)
│   ├── provider (string)
│   ├── message_count (integer)
│   ├── total_tokens (integer)
│   └── pinned (boolean)
│
├── Object Store: messages
│   ├── id (string, primary key)
│   ├── session_id (string, indexed)
│   ├── role (enum: user, assistant, system, tool)
│   ├── content (string)
│   ├── tool_calls (JSON, nullable)
│   ├── tool_results (JSON, nullable)
│   ├── tokens (integer, nullable)
│   ├── timestamp (ISO timestamp)
│   └── index (integer)  // order in session
│
└── Object Store: settings
    ├── key (string, primary key)
    └── value (JSON)
```

### 2.2 Save Strategy

| Event | Action |
|-------|--------|
| User sends message | Save message immediately |
| AI starts streaming | Save placeholder, update on stream end |
| Tool call starts | Save tool_call message |
| Tool call complete | Save tool_result message |
| New session created | Save session metadata |
| Session title generated | Update session title (auto: first 50 chars of first message) |

---

## 3. Session List

```
┌──────────────────────────────────────────────────┐
│ 💬 SESSIONS                        [+New] [🔍]  │
├──────────────────────────────────────────────────┤
│                                                  │
│ 📌 Optimize config for Machine-B                 │
│    deepseek-v4-pro · 8 messages · 15:42          │
│                                                  │
│    Code review PR #42                            │
│    deepseek-v4-flash · 15 messages · Yesterday   │
│                                                  │
│    Debug CORS error in API                       │
│    gpt-4o · 23 messages · 2026-06-24             │
│                                                  │
│    ...                                            │
└──────────────────────────────────────────────────┘
```

| Element | Description |
|---------|-------------|
| 📌 Pin | Pinned session (always shown at top) |
| Title | Auto-generated from first message (editable) |
| Model | Which model was used |
| Messages | Number of messages in session |
| Date | Last updated |
| Search | 🔍 — free-text search among sessions |

---

## 4. Export

| Format | Content | Usage |
|--------|---------|-------|
| **JSON** | Full session — messages, tool calls, results, metadata | Import to another Dashboard, backup |
| **Markdown** | Messages only (user + assistant) — readable conversation | Share with others, save as documentation |
| **Text** | Assistant responses only — no tool calls | Extract agent output |

---

## 5. Import

```
┌──────────────────────────────────────┐
│ Import Session                       │
│                                      │
│ [Select file] session-2026-06-25.json│
│                                      │
│ Format: JSON (StydeForge export)     │
│                                      │
│ [Cancel]              [Import]       │
└──────────────────────────────────────┘
```

Imported sessions marked with `[Imported]` tag.

---

## 6. Cleanup

| Rule | Description |
|------|-------------|
| Auto-cleanup | Sessions older than 90 days → archive |
| Archive | Moved to separate store, not deleted |
| Manual cleanup | Settings → "Delete all sessions older than X" |
| Pinned sessions | Never auto-cleaned |
| Size limit | Max 500MB total for all sessions → warning at 80% |

---

## 7. Settings (per user)

```json
{
  "chat_settings": {
    "auto_title": true,
    "save_history": true,
    "max_sessions": 100,
    "auto_cleanup_days": 90,
    "default_model": "deepseek-v4-pro",
    "system_prompt": "default",
    "streaming": true,
    "show_tool_calls": true
  }
}
```

---

**Status:** Phase 0 — Design
