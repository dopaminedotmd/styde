# Provider Integration + Chat Tools

**StydeForge Dashboard — Mission Control**
**Section:** 07_Dashboard_Chat
**References:** `Provider_Architecture.md`, `Built_In_Providers.md`, `Chat_Agent_Tools.md`, `Chat_Architecture.md`

---

## Part A: Provider Integration (`src/providers/`)

### `src/providers/types.ts`

```typescript
export interface ModelProvider {
  name: string;
  displayName: string;
  icon: string;
  baseURL: string;
  models: Model[];
  chat(request: ChatRequest): Promise<ChatResponse>;
  chatStream(request: ChatRequest): AsyncGenerator<ChatChunk>;
  listModels(): Promise<Model[]>;
  validateAPIKey(): Promise<boolean>;
}

export interface Model {
  id: string;
  name: string;
  contextWindow: number;
  maxOutputTokens: number;
  pricing?: { input: number; output: number };
}

export interface ChatRequest {
  model: string;
  messages: Message[];
  tools?: Tool[];
  max_tokens?: number;
  temperature?: number;
}

export interface Message {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
  tool_calls?: ToolCall[];
}

export interface Tool {
  type: "function";
  function: {
    name: string;
    description: string;
    parameters: Record<string, unknown>;
  };
}

export interface ToolCall {
  id: string;
  type: "function";
  function: { name: string; arguments: string };
}

export interface ChatResponse {
  id: string;
  model: string;
  content: string;
  tool_calls?: ToolCall[];
  usage: { prompt_tokens: number; completion_tokens: number; total_tokens: number };
}

export interface ChatChunk {
  content?: string;
  tool_calls?: ToolCall[];
  done: boolean;
}
```

### `src/providers/registry.ts`

```typescript
import { ModelProvider, Model, ChatRequest, ChatResponse } from "./types";

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

  resolveModel(modelId: string): { provider: ModelProvider; model: Model } | null {
    for (const provider of this.providers.values()) {
      const model = provider.models.find(m => m.id === modelId);
      if (model) return { provider, model };
    }
    return null;
  }

  async chatWithFallback(request: ChatRequest): Promise<ChatResponse> {
    const providers = this.list();
    for (const provider of providers) {
      try {
        return await provider.chat(request);
      } catch (error) {
        console.warn(`Provider ${provider.name} failed:`, error);
      }
    }
    throw new Error("All providers failed");
  }
}

export const registry = new ProviderRegistry();
```

### `src/providers/deepseek.ts`

```typescript
import { ModelProvider, Model, ChatRequest, ChatResponse, ChatChunk } from "./types";

const DEEPSEEK_MODELS: Model[] = [
  {
    id: "deepseek-v4-pro",
    name: "DeepSeek V4 Pro",
    contextWindow: 128000,
    maxOutputTokens: 8192,
    pricing: { input: 0.27, output: 1.10 },
  },
  {
    id: "deepseek-v4-flash",
    name: "DeepSeek V4 Flash",
    contextWindow: 128000,
    maxOutputTokens: 8192,
    pricing: { input: 0.14, output: 0.55 },
  },
];

export class DeepSeekProvider implements ModelProvider {
  name = "deepseek";
  displayName = "DeepSeek";
  icon = "🔮";
  baseURL = "https://api.deepseek.com/v1";
  models = DEEPSEEK_MODELS;

  private apiKey: string;

  constructor(apiKey: string) {
    this.apiKey = apiKey;
  }

  async chat(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseURL}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: request.model,
        messages: request.messages,
        tools: request.tools,
        max_tokens: request.max_tokens || 4096,
        temperature: request.temperature || 0.7,
        stream: false,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`DeepSeek API error (${response.status}): ${error}`);
    }

    const data = await response.json();
    const choice = data.choices[0];

    return {
      id: data.id,
      model: data.model,
      content: choice.message?.content || "",
      tool_calls: choice.message?.tool_calls,
      usage: data.usage,
    };
  }

  async *chatStream(request: ChatRequest): AsyncGenerator<ChatChunk> {
    const response = await fetch(`${this.baseURL}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        ...request,
        stream: true,
      }),
    });

    const reader = response.body?.getReader();
    if (!reader) throw new Error("No response body");

    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = line.slice(6);
          if (data === "[DONE]") {
            yield { done: true };
            return;
          }
          try {
            const parsed = JSON.parse(data);
            const delta = parsed.choices[0]?.delta;
            yield {
              content: delta?.content || "",
              tool_calls: delta?.tool_calls,
              done: false,
            };
          } catch {
            // Skip unparseable chunks
          }
        }
      }
    }
    yield { done: true };
  }

  async listModels(): Promise<Model[]> {
    return this.models;
  }

  async validateAPIKey(): Promise<boolean> {
    try {
      await this.chat({
        model: "deepseek-v4-flash",
        messages: [{ role: "user", content: "ping" }],
        max_tokens: 1,
      });
      return true;
    } catch {
      return false;
    }
  }
}
```

---

## Part B: Chat Interface with Tools

### `src/chat/chat-controller.ts`

```typescript
import { registry } from "../providers/registry";
import { DeepSeekProvider } from "../providers/deepseek";
import { Message, ToolCall, ChatResponse } from "../providers/types";
import { invoke } from "@tauri-apps/api/core";

// Tool definitions sent to the AI model
const CHAT_TOOLS = [
  {
    type: "function" as const,
    function: {
      name: "read_file",
      description: "Read the contents of a file",
      parameters: {
        type: "object",
        properties: {
          path: { type: "string", description: "Absolute path to the file" },
        },
        required: ["path"],
      },
    },
  },
  {
    type: "function" as const,
    function: {
      name: "write_file",
      description: "Write content to a file (requires user confirmation)",
      parameters: {
        type: "object",
        properties: {
          path: { type: "string", description: "Absolute path to the file" },
          content: { type: "string", description: "Content to write" },
        },
        required: ["path", "content"],
      },
    },
  },
  {
    type: "function" as const,
    function: {
      name: "search_files",
      description: "Search for a pattern in files",
      parameters: {
        type: "object",
        properties: {
          pattern: { type: "string", description: "Search pattern (regex)" },
          path: { type: "string", description: "Directory to search in" },
        },
        required: ["pattern"],
      },
    },
  },
  {
    type: "function" as const,
    function: {
      name: "hermes_command",
      description: "Run a Hermes CLI command",
      parameters: {
        type: "object",
        properties: {
          args: {
            type: "array",
            items: { type: "string" },
            description: "Hermes command arguments",
          },
        },
        required: ["args"],
      },
    },
  },
];

// Tool execution
async function executeToolCall(toolCall: ToolCall): Promise<string> {
  const { name, arguments: argsStr } = toolCall.function;
  const args = JSON.parse(argsStr);

  try {
    switch (name) {
      case "read_file": {
        const content = await invoke<string>("read_file", { path: args.path });
        return content;
      }
      case "write_file": {
        // Requires user confirmation in UI before calling this
        await invoke("write_file", { path: args.path, content: args.content });
        return `File written: ${args.path}`;
      }
      case "search_files": {
        const results = await invoke<string>("search_files", {
          pattern: args.pattern,
          path: args.path || ".",
        });
        return results || "No matches found.";
      }
      case "hermes_command": {
        const output = await invoke<string>("hermes_command", { args: args.args });
        return output;
      }
      default:
        return `Unknown tool: ${name}`;
    }
  } catch (error) {
    return `Tool error: ${error}`;
  }
}

export class ChatController {
  private messages: Message[] = [];
  private model: string;

  constructor(model: string = "deepseek-v4-pro") {
    this.model = model;
  }

  setModel(model: string) {
    this.model = model;
  }

  addSystemPrompt(prompt: string) {
    this.messages.push({ role: "system", content: prompt });
  }

  async sendMessage(
    userContent: string,
    onChunk: (chunk: string) => void
  ): Promise<ChatResponse> {
    this.messages.push({ role: "user", content: userContent });

    const { provider } = registry.resolveModel(this.model) || {};
    if (!provider) throw new Error(`No provider for model: ${this.model}`);

    // Streaming response
    let fullContent = "";
    let toolCalls: ToolCall[] = [];

    for await (const chunk of provider.chatStream({
      model: this.model,
      messages: this.messages,
      tools: CHAT_TOOLS,
    })) {
      if (chunk.content) {
        fullContent += chunk.content;
        onChunk(chunk.content);
      }
      if (chunk.tool_calls) {
        toolCalls = chunk.tool_calls;
      }
      if (chunk.done) break;
    }

    // Handle tool calls
    if (toolCalls.length > 0) {
      this.messages.push({
        role: "assistant",
        content: fullContent,
        tool_calls: toolCalls,
      });

      for (const toolCall of toolCalls) {
        const result = await executeToolCall(toolCall);
        this.messages.push({
          role: "tool",
          content: result,
        });

        // Notify UI about tool execution
        onChunk(`\n\n🔧 **${toolCall.function.name}** → Done\n`);
      }

      // Get final response after tool calls
      const finalResponse = await provider.chat({
        model: this.model,
        messages: this.messages,
      });

      this.messages.push({
        role: "assistant",
        content: finalResponse.content,
      });

      onChunk(finalResponse.content);
      return finalResponse;
    }

    this.messages.push({ role: "assistant", content: fullContent });
    return {
      id: "",
      model: this.model,
      content: fullContent,
      usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 },
    };
  }

  clearHistory() {
    this.messages = [];
  }

  getHistory(): Message[] {
    return [...this.messages];
  }
}
```

---

## Part C: Configuration Loading

### `src/config.ts`

```typescript
interface AppConfig {
  providers: Record<string, {
    api_key: string;
    default_model: string;
    enabled: boolean;
  }>;
  chat: {
    default_model: string;
    streaming: boolean;
    max_context_messages: number;
  };
  appearance: {
    font_size: number;
    font: string;
  };
  forge: {
    hermes_profile: string;
    caveman_ultra: boolean;
    auto_evaluate: boolean;
  };
}

const DEFAULT_CONFIG: AppConfig = {
  providers: {},
  chat: {
    default_model: "deepseek-v4-pro",
    streaming: true,
    max_context_messages: 50,
  },
  appearance: {
    font_size: 14,
    font: "JetBrains Mono",
  },
  forge: {
    hermes_profile: "default",
    caveman_ultra: true,
    auto_evaluate: true,
  },
};

export async function loadConfig(): Promise<AppConfig> {
  try {
    const raw = localStorage.getItem("stydeforge-config");
    if (raw) {
      return { ...DEFAULT_CONFIG, ...JSON.parse(raw) };
    }
  } catch {
    console.warn("Failed to load config, using defaults");
  }
  return DEFAULT_CONFIG;
}

export async function saveConfig(config: AppConfig): Promise<void> {
  localStorage.setItem("stydeforge-config", JSON.stringify(config));
}
```

---

## Part D: Initialization Flow

```typescript
// src/main.ts — App initialization

import { registry } from "./providers/registry";
import { DeepSeekProvider } from "./providers/deepseek";
import { ChatController } from "./chat/chat-controller";
import { loadConfig } from "./config";

async function initApp() {
  const config = await loadConfig();

  // Register DeepSeek provider
  const deepseekKey = config.providers["deepseek"]?.api_key;
  if (deepseekKey) {
    const deepseek = new DeepSeekProvider(deepseekKey);
    const valid = await deepseek.validateAPIKey();
    if (valid) {
      registry.register(deepseek);
    }
  }

  // Initialize chat
  const chat = new ChatController(config.chat.default_model);

  // Wire up UI
  setupAgentPanel();
  setupStatusBar();
  setupControlButtons();
  setupChatInput(chat);
  startPolling();
}

initApp();
```

---

**Status:** Provider + Chat tools fully specified. Ready for implementation.
