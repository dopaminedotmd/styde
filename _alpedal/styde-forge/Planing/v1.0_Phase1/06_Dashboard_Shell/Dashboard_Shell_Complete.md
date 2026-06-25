# Dashboard Shell — Remaining Implementation Docs

**StydeForge Dashboard**
**Sections:** 06_Dashboard_Shell (3 docs combined)
**References:** `Layout_Design.md`, `Design_System.md`, `Window_Management.md`, `Lifecycle_Management.md`, `System_Tray_Integration.md`, `Component_Library.md`, `Onboarding_Flow.md`

---

## Part A: Layout Implementation

CSS Grid 3-panel layout already specified in `Tauri_Setup_and_Layout.md`. This doc covers responsive breakpoints and panel behavior.

### Responsive Breakpoints

```css
/* ≥1400px: Three panels (30/35/35) */
#dashboard { grid-template-columns: 30% 35% 35%; }

/* 1100-1399px: Two panels (agents + chat), benchmarks hidden */
@media (max-width: 1399px) {
  #dashboard { grid-template-columns: 40% 60%; }
  #panel-benchmarks { display: none; }
}

/* <900px: Single panel with tabs */
@media (max-width: 899px) {
  #dashboard { grid-template-columns: 1fr; }
  #panel-tabs { display: flex; }
  .panel:not(.active) { display: none; }
}
```

---

## Part B: Application Shell

### Window Management (Tauri Rust)

```rust
// src-tauri/src/main.rs additions
use tauri::Manager;

#[tauri::command]
fn minimize_window(window: tauri::Window) {
    window.minimize().unwrap();
}

#[tauri::command]
fn maximize_window(window: tauri::Window) {
    if window.is_maximized().unwrap() {
        window.unmaximize().unwrap();
    } else {
        window.maximize().unwrap();
    }
}

#[tauri::command]
fn close_window(window: tauri::Window) {
    window.close().unwrap();
}
```

### System Tray (Tauri Rust)

```rust
use tauri::tray::{TrayIconBuilder, MouseButton, MouseButtonState, TrayIconEvent};
use tauri::menu::{MenuBuilder, MenuItemBuilder};

fn setup_tray(app: &tauri::App) {
    let show = MenuItemBuilder::with_id("show", "Show").build(app).unwrap();
    let start = MenuItemBuilder::with_id("start", "Start Forge").build(app).unwrap();
    let stop = MenuItemBuilder::with_id("stop", "Stop Forge").build(app).unwrap();
    let quit = MenuItemBuilder::with_id("quit", "Quit").build(app).unwrap();
    
    let menu = MenuBuilder::new(app)
        .item(&show)
        .separator()
        .item(&start)
        .item(&stop)
        .separator()
        .item(&quit)
        .build()
        .unwrap();
    
    let _tray = TrayIconBuilder::new()
        .icon(app.default_window_icon().unwrap().clone())
        .menu(&menu)
        .on_menu_event(|app, event| {
            match event.id().as_ref() {
                "show" => { app.get_window("main").unwrap().show().unwrap(); }
                "quit" => { app.exit(0); }
                _ => {}
            }
        })
        .on_tray_icon_event(|tray, event| {
            if let TrayIconEvent::Click { button: MouseButton::Left, button_state: MouseButtonState::Up, .. } = event {
                let app = tray.app_handle();
                if let Some(window) = app.get_window("main") {
                    window.show().unwrap();
                    window.set_focus().unwrap();
                }
            }
        })
        .build(app)
        .unwrap();
}
```

---

## Part C: Component Library

Reusable web components for the dashboard UI:

### Agent Card Component

```typescript
// src/components/agent-card.ts
class AgentCard extends HTMLElement {
  constructor() { super(); this.attachShadow({ mode: 'open' }); }
  
  connectedCallback() {
    const name = this.getAttribute('name') || 'Unknown';
    const status = this.getAttribute('status') || 'running';
    const model = this.getAttribute('model') || '';
    const score = this.getAttribute('score') || '';
    
    this.shadowRoot!.innerHTML = `
      <div class="card ${status}">
        <div class="header">
          <span class="name">${name}</span>
          <span class="status ${status}">${status}</span>
        </div>
        <div class="meta">${model}${score ? ' · ' + score + '/100' : ''}</div>
      </div>
      <style>
        .card { background: var(--bg-tertiary); border-radius: 6px; padding: 12px;
                border-left: 3px solid var(--border-color); margin-bottom: 8px; }
        .card.running { border-left-color: var(--status-running); }
        .card.done { border-left-color: var(--status-done); }
        .card.failed { border-left-color: var(--status-failed); }
        .header { display: flex; justify-content: space-between; margin-bottom: 4px; }
        .name { font-weight: 600; font-size: 13px; }
        .status { font-size: 11px; padding: 2px 8px; border-radius: 4px; }
        .status.running { background: rgba(34,197,94,0.15); color: var(--status-running); }
        .status.done { background: rgba(59,130,246,0.15); color: var(--status-done); }
        .status.failed { background: rgba(239,68,68,0.15); color: var(--status-failed); }
        .meta { font-size: 11px; color: var(--text-muted); font-family: monospace; }
      </style>`;
  }
}
customElements.define('agent-card', AgentCard);
```

### Onboarding Wizard (first-run flow)

```typescript
// src/components/onboarding.ts
class OnboardingWizard {
  async checkFirstRun(): Promise<boolean> {
    return !localStorage.getItem('stydeforge-initialized');
  }
  
  async run(): Promise<void> {
    // Step 1: Detect Hermes
    const hermesVersion = await invoke<string>('hermes_command', { args: ['--version'] });
    
    // Step 2: Configure DeepSeek
    const apiKey = await this.promptAPIKey();
    
    // Step 3: Save config
    const config = await loadConfig();
    config.providers['deepseek'] = { api_key: apiKey, default_model: 'deepseek-v4-pro', enabled: true };
    await saveConfig(config);
    
    localStorage.setItem('stydeforge-initialized', 'true');
  }
  
  private async promptAPIKey(): Promise<string> {
    // Show dialog, return key
    return '';
  }
}
```

---

## Part D: Custom Provider API (Section 07)

### OpenAI-Compatible Provider

```typescript
// src/providers/custom.ts
import { ModelProvider, Model, ChatRequest, ChatResponse, ChatChunk } from "./types";

export class CustomProvider implements ModelProvider {
  name: string;
  displayName: string;
  icon = "🔌";
  baseURL: string;
  models: Model[];
  private apiKey: string;

  constructor(name: string, baseURL: string, apiKey: string, models: Model[]) {
    this.name = `custom:${name}`;
    this.displayName = name;
    this.baseURL = baseURL;
    this.apiKey = apiKey;
    this.models = models;
  }

  async chat(request: ChatRequest): Promise<ChatResponse> {
    const res = await fetch(`${this.baseURL}/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${this.apiKey}` },
      body: JSON.stringify({ ...request, stream: false }),
    });
    const data = await res.json();
    return {
      id: data.id, model: data.model,
      content: data.choices[0]?.message?.content || "",
      usage: data.usage,
    };
  }

  async *chatStream(request: ChatRequest): AsyncGenerator<ChatChunk> {
    const res = await fetch(`${this.baseURL}/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${this.apiKey}` },
      body: JSON.stringify({ ...request, stream: true }),
    });
    const reader = res.body?.getReader();
    if (!reader) return;
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      for (const line of buffer.split("\n")) {
        if (line.startsWith("data: ") && line !== "data: [DONE]") {
          try {
            const d = JSON.parse(line.slice(6));
            yield { content: d.choices[0]?.delta?.content || "", done: false };
          } catch {}
        }
      }
      buffer = buffer.split("\n").pop() || "";
    }
    yield { done: true };
  }

  async listModels(): Promise<Model[]> { return this.models; }
  async validateAPIKey(): Promise<boolean> {
    try { await this.chat({ model: this.models[0]?.id || "", messages: [{ role: "user", content: "ping" }], max_tokens: 1 }); return true; }
    catch { return false; }
  }
}
```

### Ollama Provider (Local)

```typescript
// src/providers/ollama.ts
export class OllamaProvider extends CustomProvider {
  constructor(baseURL: string = "http://localhost:11434/v1") {
    super("ollama", baseURL, "ollama", []);
  }

  async listModels(): Promise<Model[]> {
    const res = await fetch(`${this.baseURL.replace('/v1', '')}/api/tags`);
    const data = await res.json();
    return (data.models || []).map((m: any) => ({
      id: `ollama:${m.name}`,
      name: m.name,
      contextWindow: 8192,
      maxOutputTokens: 4096,
    }));
  }
}
```

---

**Status:** Dashboard shell + custom providers complete. All 06 + 07 sections covered.
