# Built-In Providers

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard ships with pre-configured providers for the most common AI services. The user only needs to enter an API key — everything else is pre-configured.

---

## 2. DeepSeek

```typescript
class DeepSeekProvider implements ModelProvider {
  name = "deepseek";
  displayName = "DeepSeek";
  icon = "🔮";
  baseURL = "https://api.deepseek.com/v1";
  apiKeyURL = "https://platform.deepseek.com/api_keys";

  models = [
    {
      id: "deepseek-v4-pro",
      name: "DeepSeek V4 Pro",
      contextWindow: 128000,
      maxOutputTokens: 8192,
      pricing: { input: 0.27, output: 1.10 }
    },
    {
      id: "deepseek-v4-flash",
      name: "DeepSeek V4 Flash",
      contextWindow: 128000,
      maxOutputTokens: 8192,
      pricing: { input: 0.14, output: 0.55 }
    }
  ];

  // OpenAI-compatible API — uses standard fetch
  async chat(req: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseURL}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: req.model,
        messages: req.messages,
        tools: req.tools,
        max_tokens: req.max_tokens,
        temperature: req.temperature
      })
    });
    // ... parse response
  }
}
```

| Model | Context | Price (in/out per 1M) | Description |
|--------|---------|------------------------|-------------|
| v4-pro | 128K | $0.27 / $1.10 | Best quality — eval, teacher |
| v4-flash | 128K | $0.14 / $0.55 | Fastest — agent spawn |

---

## 3. OpenAI

```typescript
class OpenAIProvider implements ModelProvider {
  name = "openai";
  displayName = "OpenAI";
  icon = "🧠";
  baseURL = "https://api.openai.com/v1";
  apiKeyURL = "https://platform.openai.com/api-keys";

  models = [
    {
      id: "gpt-4o",
      name: "GPT-4o",
      contextWindow: 128000,
      maxOutputTokens: 16384,
      pricing: { input: 2.50, output: 10.00 }
    },
    {
      id: "gpt-4o-mini",
      name: "GPT-4o Mini",
      contextWindow: 128000,
      maxOutputTokens: 16384,
      pricing: { input: 0.15, output: 0.60 }
    }
  ];
}
```

---

## 4. Anthropic

```typescript
class AnthropicProvider implements ModelProvider {
  name = "anthropic";
  displayName = "Anthropic";
  icon = "🎭";
  baseURL = "https://api.anthropic.com/v1";
  apiKeyURL = "https://console.anthropic.com/keys";

  models = [
    {
      id: "claude-sonnet-4-20250514",
      name: "Claude Sonnet 4",
      contextWindow: 200000,
      maxOutputTokens: 8192,
      pricing: { input: 3.00, output: 15.00 }
    },
    {
      id: "claude-haiku-3-5",
      name: "Claude Haiku 3.5",
      contextWindow: 200000,
      maxOutputTokens: 8192,
      pricing: { input: 0.80, output: 4.00 }
    }
  ];

  // Anthropic uses a different API format — conversion required
  async chat(req: ChatRequest): Promise<ChatResponse> {
    // Convert OpenAI tool format → Anthropic tool format
    // Convert response back
  }
}
```

| Note | Description |
|------|-------------|
| API format | Requires conversion: OpenAI tools → Anthropic tools |
| Headers | `x-api-key` instead of `Authorization: Bearer` |
| Version | `anthropic-version: 2023-06-01` |

---

## 5. Provider Comparison

| Property | DeepSeek | OpenAI | Anthropic |
|----------|----------|--------|-----------|
| API format | OpenAI-compatible ✅ | Native OpenAI | Proprietary ⚠ |
| Tool calling | Yes | Yes | Yes |
| Streaming (SSE) | Yes | Yes | Yes |
| Pricing | $ | $$$ | $$$$ |
| Default for StydeForge | ✅ | — | — |

---

## 6. Provider Configuration (UI)

In the settings panel:

```
┌──────────────────────────────────────────────────┐
│ ⚙ PROVIDERS                                      │
├──────────────────────────────────────────────────┤
│                                                  │
│ 🔮 DeepSeek                        ● Connected  │
│    API Key: sk-••••••••••                        │
│    Models: deepseek-v4-pro, deepseek-v4-flash     │
│    [Test Connection] [Edit] [Disable]             │
│                                                  │
│ 🧠 OpenAI                          ○ Configure  │
│    API Key: [________________]                   │
│    [Save & Test]                                  │
│                                                  │
│ 🎭 Anthropic                       ○ Configure  │
│    API Key: [________________]                   │
│    [Save & Test]                                  │
│                                                  │
│ [+ Add Custom Provider]                          │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

**Status:** Phase 0 — Design
