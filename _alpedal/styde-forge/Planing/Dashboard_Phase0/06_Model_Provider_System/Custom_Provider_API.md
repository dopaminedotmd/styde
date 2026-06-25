# Custom Provider API

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

Users can connect their own LLM via a REST endpoint. As long as the API is OpenAI-compatible (de facto standard), it works directly. A custom adapter system handles non-standard APIs.

---

## 2. OpenAI-Compatible APIs (Auto-Detect)

Many services and local servers use OpenAI's API format. These work directly:

| Service | Example baseURL |
|---------|-----------------|
| OpenRouter | `https://openrouter.ai/api/v1` |
| Groq | `https://api.groq.com/openai/v1` |
| Together | `https://api.together.xyz/v1` |
| Fireworks | `https://api.fireworks.ai/inference/v1` |
| xAI (Grok) | `https://api.x.ai/v1` |
| Ollama | `http://localhost:11434/v1` |
| vLLM | `http://localhost:8000/v1` |
| LiteLLM | `http://localhost:4000/v1` |
| Your own | `https://your-server.com/v1` |

---

## 3. Add Custom Provider — UI

```
┌──────────────────────────────────────────────────┐
│ + ADD CUSTOM PROVIDER                            │
├──────────────────────────────────────────────────┤
│                                                  │
│  Provider Name: [My LLM Server________]          │
│  Icon: [🖥] (emoji)                              │
│                                                  │
│  ┌─ API Configuration ─────────────────────────┐ │
│  │ API Base URL:                               │ │
│  │ [https://my-server.com/v1______________]     │ │
│  │                                              │ │
│  │ API Format: [OpenAI Compatible ▼]            │ │
│  │              OpenAI Compatible                │ │
│  │              Anthropic Format                 │ │
│  │              Custom Adapter                   │ │
│  │                                              │ │
│  │ API Key: [••••••••••______________]          │ │
│  │ (optional for local servers)                 │ │
│  │                                              │ │
│  │ API Key Header: [Authorization: Bearer ***  │ │
│  │ (default: Authorization: Bearer)             │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Models ────────────────────────────────────┐ │
│  │ ○ Auto-detect (fetch from /models endpoint) │ │
│  │ ● Manual:                                    │ │
│  │                                              │ │
│  │ Model ID: [my-model-v1__________]           │ │
│  │ Display Name: [My Model V1__________]        │ │
│  │ Context Window: [128000____]                 │ │
│  │ Max Output: [8192______]                     │ │
│  │                                              │ │
│  │ [+ Add Another Model]                        │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Advanced ──────────────────────────────────┐ │
│  │ ☐ Custom headers:                           │ │
│  │   [{"key": "X-Custom", "value": "..."}]     │ │
│  │                                              │ │
│  │ Timeout: [60___] seconds                    │ │
│  │ Max Retries: [3_]                            │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  [Cancel]                    [Test & Save]       │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 4. Auto-Detection

When user clicks "Test & Save":

```
1. GET {baseURL}/models → list models
   └─ If 200: auto-populate model list
   └─ If 404/401: ask for manual configuration

2. POST {baseURL}/chat/completions
   → Test message: "Say 'OK' if you can read this."
   └─ If 200: ✅ Connection successful!
   └─ If error: show detailed error message

3. Save provider to config
```

---

## 5. Custom Adapter (for Non-Standard APIs)

If the API is not OpenAI-compatible, the user can write a small adapter:

```javascript
// Adapt request before sending
function adaptRequest(openAIRequest) {
  return {
    // Your API format here
    prompt: openAIRequest.messages.map(m => m.content).join("\n"),
    max_tokens: openAIRequest.max_tokens
  };
}

// Adapt response to OpenAI format
function adaptResponse(yourAPIResponse) {
  return {
    id: yourAPIResponse.id,
    model: yourAPIResponse.model,
    content: yourAPIResponse.text,
    usage: {
      prompt_tokens: yourAPIResponse.usage.input,
      completion_tokens: yourAPIResponse.usage.output,
      total_tokens: yourAPIResponse.usage.total
    }
  };
}
```

**Planned for Phase 2+** — not in MVP. MVP only supports OpenAI-compatible APIs directly.

---

## 6. Configuration Storage

```json
{
  "providers": {
    "custom:my-llm": {
      "name": "custom:my-llm",
      "displayName": "My LLM Server",
      "icon": "🖥",
      "baseURL": "https://my-server.com/v1",
      "api_key": "sk-...",
      "api_format": "openai",
      "api_key_header": "Authorization: Bearer",
      "timeout": 60,
      "max_retries": 3,
      "custom_headers": {},
      "enabled": true,
      "models": [
        {
          "id": "my-model-v1",
          "name": "My Model V1",
          "contextWindow": 128000,
          "maxOutputTokens": 8192
        }
      ]
    }
  }
}
```

---

## 7. Provider Namespace

Custom providers are prefixed with `custom:` to avoid name conflicts with built-in providers:

| Prefix | Type |
|--------|------|
| `deepseek` | Built-in |
| `openai` | Built-in |
| `anthropic` | Built-in |
| `ollama:` | Local provider (Ollama) |
| `custom:` | User-defined |
| `litellm:` | LiteLLM proxy |

---

**Status:** Phase 0 — Design
