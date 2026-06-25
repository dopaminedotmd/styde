# Chat Agent Tools

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The chat agent has access to tools — just like Hermes has `read_file`, `write_file`, `terminal`, etc. Tools are executed by the Dashboard's Rust backend (Tauri) for secure filesystem and process access.

---

## 2. Tool Architecture

```
User: "read D:/config.yaml and optimize"
        │
        ▼
┌────────────────────┐
│ Chat Controller    │
│                    │
│ 1. Send to         │
│    AI Provider     │
│    + tool defs     │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ AI Provider responds│
│ {                  │
│   "tool_calls": [{ │
│     "name":        │
│     "read_file",   │
│     "args": {      │
│       "path":      │
│     "D:/config..." │
│     }              │
│   }]               │
│ }                  │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ Tauri Rust Backend │
│ • read_file()      │
│ • write_file()     │
│ • terminal()       │
│ • search_files()   │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ Result to AI       │
│ Provider           │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ AI Provider responds│
│ with analysis      │
└────────────────────┘
```

---

## 3. Tool Definitions (OpenAI format)

### 3.1 read_file

```json
{
  "name": "read_file",
  "description": "Read a file from the local filesystem. Returns content with line numbers.",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Absolute path to the file to read"
      },
      "offset": {
        "type": "integer",
        "description": "Line number to start from (1-indexed)",
        "default": 1
      },
      "limit": {
        "type": "integer",
        "description": "Max lines to read (default: 500)",
        "default": 500
      }
    },
    "required": ["path"]
  }
}
```

### 3.2 write_file

```json
{
  "name": "write_file",
  "description": "Write content to a file. Overwrites the entire file. Creates parent directories automatically. Requires user confirmation before execution.",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Absolute path to the file to write"
      },
      "content": {
        "type": "string",
        "description": "Complete content to write to the file"
      }
    },
    "required": ["path", "content"]
  }
}
```

### 3.3 patch

```json
{
  "name": "patch",
  "description": "Targeted find-and-replace edit in a file. Shows diff before applying.",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "File to edit"
      },
      "old_string": {
        "type": "string",
        "description": "Text to find (must be unique)"
      },
      "new_string": {
        "type": "string",
        "description": "Replacement text"
      }
    },
    "required": ["path", "old_string", "new_string"]
  }
}
```

### 3.4 search_files

```json
{
  "name": "search_files",
  "description": "Search file contents (regex) or find files by name (glob). Ripgrep-backed.",
  "parameters": {
    "type": "object",
    "properties": {
      "pattern": {
        "type": "string",
        "description": "Regex pattern (content search) or glob pattern (file search)"
      },
      "path": {
        "type": "string",
        "description": "Directory to search in",
        "default": "."
      },
      "target": {
        "type": "string",
        "enum": ["content", "files"],
        "description": "Search file contents or find files by name",
        "default": "content"
      },
      "file_glob": {
        "type": "string",
        "description": "Filter by file pattern (e.g., '*.py')"
      }
    },
    "required": ["pattern"]
  }
}
```

### 3.5 terminal

```json
{
  "name": "terminal",
  "description": "Execute a shell command. REQUIRES USER CONFIRMATION. Use with caution.",
  "parameters": {
    "type": "object",
    "properties": {
      "command": {
        "type": "string",
        "description": "Shell command to execute"
      },
      "workdir": {
        "type": "string",
        "description": "Working directory for the command"
      },
      "timeout": {
        "type": "integer",
        "description": "Max seconds before timeout (default: 60)",
        "default": 60
      }
    },
    "required": ["command"]
  }
}
```

### 3.6 web_search

```json
{
  "name": "web_search",
  "description": "Search the web for information. Returns up to 5 results.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query"
      }
    },
    "required": ["query"]
  }
}
```

### 3.7 web_extract

```json
{
  "name": "web_extract",
  "description": "Extract and read content from a web page URL. Returns markdown.",
  "parameters": {
    "type": "object",
    "properties": {
      "url": {
        "type": "string",
        "description": "URL to extract content from"
      }
    },
    "required": ["url"]
  }
}
```

### 3.8 spawn_agent

```json
{
  "name": "spawn_agent",
  "description": "Spawn a new agent to work on a task independently.",
  "parameters": {
    "type": "object",
    "properties": {
      "goal": {
        "type": "string",
        "description": "Task description for the sub-agent"
      },
      "skills": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Skills to load"
      },
      "model": {
        "type": "string",
        "description": "Model to use (default: chat model)"
      }
    },
    "required": ["goal"]
  }
}
```

---

## 4. Confirmation Dialogs

Some tools require user confirmation before execution:

| Tool | Confirmation | Reason |
|------|-------------|--------|
| `write_file` | Yes — show diff | Can overwrite important files |
| `patch` | Yes — show unified diff | Can modify files unexpectedly |
| `terminal` | Yes — show command | Can run anything |
| `spawn_agent` | Yes — show parameters | Can start costly processes |
| `read_file` | No | Read-only — safe |
| `search_files` | No | Read-only — safe |
| `web_search` | No | Read-only — safe |
| `web_extract` | No | Read-only — safe |

---

## 5. Tool Call UI

```
┌─ Tool Call ──────────────────────────────────────┐
│ 🔧 read_file("D:/StydeForge/config.yaml")        │
│ ✅ Read 87 lines — 0.3s                          │
│ ┌──────────────────────────────────────────────┐ │
│ │ [Expand to see file content]              [▼] │ │
│ └──────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

| State | Icon | Description |
|-------|------|-------------|
| Pending | 🔧 | Awaiting execution |
| Running | ⏳ | Executing... |
| Success | ✅ | Done — with time and result |
| Error | ❌ | Error — with error message |
| Awaiting Confirm | ⚠ | Awaiting user confirmation |

---

## 6. System Prompt

```markdown
You are StydeForge Chat Agent — an AI assistant with access to the local
filesystem and terminal. You can:

- Read, write, and edit files (read_file, write_file, patch)
- Search codebases (search_files)
- Run terminal commands (terminal) — use caution
- Search the web (web_search, web_extract)
- Spawn sub-agents for complex tasks (spawn_agent)
- Use skills (invoke with /skill:name or load via skill_load)

Always ask for confirmation before destructive operations (write, delete,
terminal commands). Show diffs before editing files. Be concise — Caveman
Ultra principles apply.
```

---

**Status:** Phase 0 — Design
