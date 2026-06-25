# Provider Architecture

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The provider system is an abstraction layer allowing chat to communicate with any AI model — DeepSeek, OpenAI, Anthropic, local models, or a custom REST endpoint.

All providers implement the same interface. Switching models is a dropdown selection — no restart, no config file editing.

---

## 2. Architecture

```
┌──────────────────────────────────────────────────┐
│                  Chat Controller                  │
│                                                  │
│  this.provider.chat({                            │
│    model: "deepseek-v4-pro",                     │
│    messages: [...],                              │
│    tools: [...],                                 │
│    stream: true                                  │
│  })                                              │
│         │                                        │
│         ▼                                        │
│  ┌──────────────────────────────────────┐        │
│  │        Provider Registry             │        │
│  │                                      │        │
│  │  providers.get("deepseek")           │        │
│  │  providers.get("openai")             │        │
│  │  providers.get("anthropic")          │        │
│  │  providers.get("custom:my-llm")      │        │
│  │  providers.get("ollama:llama3")      │        │
│  └──────────┬───────────────────────────┘        │
│             │                                    │
│  ┌──────────┴───────────────────────────┐        │
│  │       ModelProvider Interface        │        │
│  │                                      │        │
│  │  + name: string                      │        │
│  │  + models: Model[]                   │        │
│  │  + chat(req): Response               │        │
│  │  + chatStream(req): AsyncIterator    │        │
│  │  + listModels(): Model[]             │        │
│  │  + validateKey(): boolean            │        │
│  └──────────────────────────────────────┘        │
└──────────────────────────────────────────────────┘
```

---

## 3. ModelProvider Interface

### 3.1 TypeScript Definition

```typescript
interface ModelProvider {
  /** Unique provider name */
  name: string;

  /** Display name in UI */
  displayName: string;

  /** Provider icon (emoji or URL) */
  icon: string;

  /** Base URL for API */
  baseURL: string;

  /** Available models */
  models: Model[];

  /** Send a chat completion request */
  chat(request: ChatRequest): Promise<ChatResponse>;

  /** Stream a chat completion */
  chatStream(request: ChatRequest): AsyncGenerator<ChatChunk>;

  /** List available models (from the API) */
  listModels(): Promise<Model[]>;

  /** Validate API key */
  validateAPIKey(): Promise<boolean>;

  /** URL to obtain an API key */
  apiKeyURL?: string;
}

interface Model {
  id: string;
  name: string;
  contextWindow: number;
  maxOutputTokens: number;
  pricing?: {
    input: number;   // per 1M tokens
    output: number;  // per 1M tokens
  };
}

interface ChatRequest {
  model: string;
  messages: Message[];
  tools?: Tool[];
  max_tokens?: number;
  temperature?: number;
}

interface ChatResponse {
  id: string;
  model: string;
  content: string;
  tool_calls?: ToolCall[];
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

interface ChatChunk {
  content?: string;
  tool_calls?: ToolCall[];
  done: boolean;
}
```

---

## 4. Provider Registry

```typescript
class ProviderRegistry {
  private providers: Map<string, ModelProvider> = new Map();

  register(provider: ModelProvider): void {
    this.providers.set(provider.name, provider);
  }

  get(name: string): ModelProvider | undefined {
    return this.providers.get(name);
  }

  list(): ModelProvider[] {
    return Array.from(this.providers.values());
  }

  /** Find the right provider for a model */
  resolveModel(modelId: string): { provider: ModelProvider; model: Model } | null {
    for (const provider of this.providers.values()) {
      const model = provider.models.find(m => m.id === modelId);
      if (model) return { provider, model };
    }
    return null;
  }
}
```

---

## 5. Provider Configuration

```json
{
  "providers": {
    "deepseek": {
      "name": "deepseek",
      "displayName": "DeepSeek",
      "icon": "🔮",
      "baseURL": "https://api.deepseek.com/v1",
      "api_key": "sk-...",
      "enabled": true,
      "models": [
        {
          "id": "deepseek-v4-pro",
          "name": "DeepSeek V4 Pro",
          "contextWindow": 128000,
          "maxOutputTokens": 8192,
          "pricing": { "input": 0.27, "output": 1.10 }
        },
        {
          "id": "deepseek-v4-flash",
          "name": "DeepSeek V4 Flash",
          "contextWindow": 128000,
          "maxOutputTokens": 8192,
          "pricing": { "input": 0.14, "output": 0.55 }
        }
      ]
    }
  }
}
```

---

## 6. Provider Lifecycle

```
┌─────────────────┐
│ 1. REGISTERED   │  ← Provider exists in config but not validated
└────────┬────────┘
         │ validateAPIKey()
         ▼
┌─────────────────┐
│ 2. CONNECTED    │  ← API key verified, models listed
└────────┬────────┘
         │ chat() / chatStream()
         ▼
┌─────────────────┐
│ 3. ACTIVE       │  ← Currently in use in a chat
└────────┬────────┘
         │ API error / timeout
         ▼
┌─────────────────┐
│ 4. ERROR        │  ← Temporary error → auto-retry → back to 2
└────────┬────────┘
         │ Persistent error / invalid key
         ▼
┌─────────────────┐
│ 5. DISCONNECTED │  ← Shown as disconnected in UI
└─────────────────┘
```

---

## 7. Provider Error Scenarios

| Error | Behavior |
|-------|----------|
| API timeout (15s) | Retry ×3 with exponential backoff (1s, 2s, 4s) |
| 401 Unauthorized | Mark provider as disconnected, show error |
| 429 Rate Limit | Wait for `Retry-After` header, else 10s |
| 5xx Server Error | Retry ×2, then fallback to another provider if available |
| Network error | Show "No connection", auto-retry when network restored |

---

## 8. Provider Fallback

If primary provider fails, try next:

```typescript
async function chatWithFallback(request: ChatRequest): Promise<ChatResponse> {
  const providers = getEnabledProviders();

  for (const provider of providers) {
    try {
      return await provider.chat(request);
    } catch (error) {
      console.warn(`Provider ${provider.name} failed:`, error);
      continue;
    }
  }

  throw new Error("All providers failed");
}
```

---

**Status:** Phase 0 — Design
