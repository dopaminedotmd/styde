# Provider Configuration UI

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

A dedicated settings panel for managing providers: add, remove, test, enable/disable. All changes happen directly in the UI — no config file editing needed.

---

## 2. Provider Settings — Full View

```
┌──────────────────────────────────────────────────────────┐
│ ⚙ SETTINGS — Providers                                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Active Providers                                        │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🔮 DeepSeek                          ● Connected  │  │
│  │    deepseek-v4-pro · deepseek-v4-flash              │  │
│  │    Latency: 120ms · Rate limit: 60 req/min         │  │
│  │    [Edit] [Test] [Disable] [Remove]                │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🦙 Ollama (Local)                    ● Connected  │  │
│  │    llama3.2:3b · codellama:7b · deepseek-r1:8b    │  │
│  │    GPU: RTX 3080 (6.2GB used / 10GB)              │  │
│  │    [Refresh Models] [Disable]                     │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🧠 OpenAI                            ○ Disabled   │  │
│  │    [Configure] [Enable] [Remove]                   │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🖥 My LLM Server                   ⚠ Error        │  │
│  │    Connection refused: http://192.168.1.100:8000   │  │
│  │    [Edit] [Retry] [Disable] [Remove]               │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  [+ Add Provider]                                       │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  Default Chat Model                                     │
│  [deepseek-v4-pro                    ▼]                 │
│                                                          │
│  Fallback Behavior                                      │
│  ○ None — fail if primary model is down                 │
│  ● Auto-fallback — try next available model             │
│                                                          │
│  [Close]                                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Edit Provider

```
┌──────────────────────────────────────────────────┐
│ EDIT PROVIDER: DeepSeek                          │
├──────────────────────────────────────────────────┤
│                                                  │
│  Display Name: [DeepSeek________________]        │
│  API Base URL: [https://api.deepseek.com/v1___]  │
│                                                  │
│  API Key:                                        │
│  [••••••••••••••••••••••••••••]  [👁 Show]      │
│                                                  │
│  API Format: [OpenAI Compatible ▼]               │
│                                                  │
│  ┌─ Models ────────────────────────────────────┐ │
│  │ [Refresh from API]                          │ │
│  │                                              │ │
│  │ deepseek-v4-pro      128K ctx  $0.27/$1.10  │ │
│  │ deepseek-v4-flash    128K ctx  $0.14/$0.55  │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  Advanced                                        │
│  Timeout: [60___] seconds                       │
│  Max Retries: [3_]                               │
│                                                  │
│  [Cancel]                    [Save & Test]       │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 4. Quick Switch (in Chat Header)

The most common interaction — switching models — must be immediate:

```
┌──────────────────────────────────────────┐
│ 💬 CHAT   [deepseek-v4-pro        ▼]    │
│           ─────────────────────────      │
│           🔮 DeepSeek                    │
│           ○ deepseek-v4-pro    (Pro)     │
│           ○ deepseek-v4-flash  (Flash)   │
│           ─────────────────────────      │
│           🦙 Ollama (Local)              │
│           ○ llama3.2:3b                 │
│           ○ codellama:7b                │
│           ○ deepseek-r1:8b              │
│           ─────────────────────────      │
│           ⚙ Manage Providers...         │
└──────────────────────────────────────────┘
```

---

## 5. Status Indicators

| Indicator | Meaning |
|-----------|---------|
| ● Connected | API key verified, models listed |
| ○ Disabled | Provider exists but is disabled |
| ⚠ Error | Connection error (show error message) |
| ⏳ Testing | Testing connection... |
| 🔄 Refreshing | Fetching model list... |

---

## 6. Security — API Keys

| Rule | Implementation |
|------|---------------|
| Storage | Encrypted in OS keyring (Windows Credential Manager) |
| Display in UI | Masked (`sk-••••••••••`) |
| Copy | "Copy to clipboard" button (cleared from clipboard after 30s) |
| Export | API keys excluded when exporting settings |
| Logging | API keys are NEVER written to logs |

---

## 7. Validation

| Validation | Rules |
|------------|-------|
| Provider name | Unique, alphanumeric + hyphens, max 32 characters |
| API Base URL | Must be a valid URL (https:// or http://) |
| API Key | At least 8 characters (if required) |
| Timeout | 5-300 seconds |
| Max retries | 0-5 |

---

**Status:** Phase 0 — Design
