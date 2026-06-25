# Chat Architecture

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The chat panel is a full AI agent — not just a chatbot. It can read/write/edit files, run terminal commands, use skills, and spawn sub-agents. All through the same chat interface.

---

## 2. Chat Panel — Visual Design

```
┌──────────────────────────────────────────────────┐
│ 💬 CHAT    [deepseek-v4-pro ▼] [+New session]    │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─ System Message ────────────────────────────┐ │
│  │ StydeForge Chat Agent. I can:               │ │
│  │ • Read/write/edit files                     │ │
│  │ • Run terminal commands                     │ │
│  │ • Use skills ("skill:name")                 │ │
│  │ • Search codebases                          │ │
│  │ • Spawn sub-agents                          │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │ 👤 You                             15:42     │ │
│  │ Read through D:/StydeForge/config.yaml and   │ │
│  │ optimize settings for my hardware            │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Tool Call ─────────────────────────────────┐ │
│  │ 🔧 read_file("D:/StydeForge/config.yaml")   │ │
│  │ ✅ Read 87 lines — 0.3s                     │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │ 🤖 StydeForge Agent               15:42     │ │
│  │ deepseek-v4-pro · 342 tokens · 1.2s         │ │
│  │                                              │ │
│  │ I've analyzed your config. Here are my      │ │
│  │ recommendations:                             │ │
│  │                                              │ │
│  │ 1. **Worker count**: 4 → 2 (18GB VRAM        │ │
│  │    total, 4 workers overloads)               │ │
│  │ 2. **Model selection**: Flash is the right   │ │
│  │    choice for 80% of agents                  │ │
│  │ 3. **Sampling**: Switch to VI depth 8 for    │ │
│  │    your Machine-B profile                    │ │
│  │                                              │ │
│  │ Should I apply these changes?                │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │ 👤 You                             15:43     │ │
│  │ Yes, apply the changes                       │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Tool Call ─────────────────────────────────┐ │
│  │ 🔧 patch("config.yaml", old, new)           │ │
│  │ ✅ 3 changes applied — 0.2s                 │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │ 🤖 StydeForge Agent               15:43     │ │
│  │ Done! Changes saved:                         │ │
│  │ • workers: 2                                 │ │
│  │ • sampling: VI depth 8                       │ │
│  │ • model: deepseek-v4-flash (already set)     │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │ [/spawn] [/skill:name] [/clear]              │ │
│  │ ┌────────────────────────────────────────┐   │ │
│  │ │ Type message...                 [📎] [▶]│   │ │
│  │ └────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 3. Message Types

| Type | Icon | Color | Description |
|------|------|-------|-------------|
| **User** | 👤 | Blue background (right-aligned) | User message |
| **Assistant** | 🤖 | Gray background (left-aligned) | AI response |
| **System** | ℹ | Gray text, centered | System messages |
| **Tool Call** | 🔧 | Indented, border-left | Tool call (shown before result) |
| **Tool Result** | ✅/❌ | Indented, border-left | Tool call result |
| **Error** | ⚠ | Red background | Error messages |
| **Skill** | 📦 | Purple accent | Skill usage |

---

## 4. Streaming

AI responses stream token-by-token (like ChatGPT):

```
🤖 StydeForge Agent
I've analyzed your config. Here are my│  ← printed continuously
```

| Streaming Detail | Value |
|------------------|-------|
| Type | Server-Sent Events (SSE) via fetch API |
| Rendering | Append to textContent, no re-render |
| Markdown | Rendered incrementally (last paragraph "live") |
| Abort | Click ⏹ during streaming → abort fetch |

---

## 5. Markdown Rendering

Chat supports full markdown:

| Element | Rendering |
|---------|-----------|
| **Bold** | `**text**` → bold |
| *Italic* | `*text*` → italic |
| `Inline code` | `` `code` `` → monospace with background |
| ```Code block``` | Syntax highlighting (via highlight.js or Prism) |
| > Blockquote | Indented with border-left |
| Tables | Rendered as HTML tables |
| Lists | Bullet and numbered lists |

---

## 6. Model Selector

Dropdown in chat header:

```
[deepseek-v4-pro        ▼]
───────────────────────────
 deepseek-v4-pro
 deepseek-v4-flash
 gpt-4o          (OpenAI)
 claude-sonnet-4 (Anthropic)
 ollama:llama3   (Local)
───────────────────────────
 ⚙ Manage Providers...
```

- Shows all active providers and their models
- Last used model is default
- Model switch takes effect for the next message
- **Not** mid-conversation (can confuse the agent)

---

## 7. Session Management

| Function | Description |
|----------|-------------|
| New session | `[+New session]` — clears chat, new context |
| Save session | Automatically on each message (IndexedDB) |
| Load session | List of previous sessions: date, title, message count |
| Delete session | Right-click → Delete |
| Export | JSON (full conversation with tool calls) |

---

## 8. Input Field — Special Functions

| Function | Trigger | Description |
|----------|---------|-------------|
| Send | Enter | Send message |
| New line | Shift+Enter | Line break within message |
| Attachment | 📎 button | Attach file (inserted as context) |
| `/spawn` | `/spawn <blueprint> <task>` | Spawn an agent from chat |
| `/skill:name` | `/skill:code-review` | Load a specific skill |
| `/clear` | `/clear` | Clear chat |
| `/export` | `/export` | Export session |
| `/model` | `/model <name>` | Switch model |
| `@file` | `@D:/path/file.ts` | Autocomplete file path |

---

## 9. Conversation Context

| Parameter | Default | Description |
|-----------|---------|-------------|
| Max context length | 100K tokens | Provider- and model-specific |
| Context window | Full session | All messages + tool results |
| System prompt | Yes | StydeForge Chat Agent with tool definitions |
| Context trimming | Smart | Keep last N messages, trim oldest |

---

**Status:** Phase 0 — Design
