# Component Library

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

All reusable UI components. Built as Web Components or vanilla JS — no frameworks. Each component has HTML structure, CSS, and JS behavior defined.

---

## 2. Component Catalog

### 2.1 `sf-button`

```html
<sf-button variant="primary" icon="▶">
  Start Forge
</sf-button>
```

| Attribute | Values | Description |
|-----------|--------|-------------|
| `variant` | `primary`, `secondary`, `danger`, `ghost` | Visual style |
| `size` | `sm`, `md`, `lg` | Size (default: md) |
| `icon` | Any emoji/unicode | Icon before text |
| `disabled` | boolean | Inactive button |

### 2.2 `sf-panel`

```html
<sf-panel title="Agents" icon="📡" collapsible pinned>
  <!-- panel content -->
</sf-panel>
```

| Attribute | Values | Description |
|-----------|--------|-------------|
| `title` | string | Panel header text |
| `icon` | string | Panel icon |
| `collapsible` | boolean | Can be collapsed |
| `pinned` | boolean | Pinned (can't be closed) |

### 2.3 `sf-tabs`

```html
<sf-tabs>
  <sf-tab label="Agents" icon="📡" active>
    <!-- content -->
  </sf-tab>
  <sf-tab label="Benchmarks" icon="📊">
    <!-- content -->
  </sf-tab>
</sf-tabs>
```

### 2.4 `sf-status-bar`

```html
<sf-status-bar>
  <sf-status-item icon="●" value="Running" />
  <sf-status-item label="Agents" value="3" />
  <sf-status-item label="Tokens" value="12.4K" />
  <sf-status-item label="Cost" value="$0.037" />
</sf-status-bar>
```

### 2.5 `sf-agent-card`

```html
<sf-agent-card
  name="code-reviewer-v3"
  model="deepseek-v4-flash"
  status="running"
  score="87"
  tokens="4.2K"
  cost="$0.012"
  time="2m 34s">
</sf-agent-card>
```

Visual design:
```
┌─────────────────────────────────────┐
│ ● code-reviewer-v3         87/100  │
│   deepseek-v4-flash · 2m 34s       │
│   4.2K tokens · $0.012              │
│ ████████████████████░░ 87%  ⚡45t/s│
└─────────────────────────────────────┘
```

### 2.6 `sf-chart`

```html
<sf-chart type="line" data="..." width="100%" height="200px">
</sf-chart>
```

| Attribute | Values | Description |
|-----------|--------|-------------|
| `type` | `line`, `bar`, `gauge`, `sparkline` | Chart type |
| `data` | JSON | Data points |
| `width` | CSS value | Width |
| `height` | CSS value | Height |
| `dark` | boolean | Always true in our case |

### 2.7 `sf-log-viewer`

```html
<sf-log-viewer lines="100" filter="ERROR" auto-scroll>
  log text...
</sf-log-viewer>
```

Virtual scrolling for performance with large logs.

### 2.8 `sf-modal`

```html
<sf-modal title="Stop Forge?" open>
  <p>3 agents are still running.</p>
  <sf-button variant="danger">Stop Anyway</sf-button>
  <sf-button variant="secondary">Cancel</sf-button>
</sf-modal>
```

### 2.9 `sf-toast`

```html
<sf-toast type="success" message="Agent completed!" duration="5000">
</sf-toast>
```

Floats in from bottom-right, auto-dismiss.

---

## 3. Chat-Specific Components

### 3.1 `sf-chat-message`

```html
<sf-chat-message role="user" timestamp="15:42">
  optimize my config
</sf-chat-message>

<sf-chat-message role="assistant" model="deepseek-v4-pro" tokens="342" time="1.2s">
  I've read your config.yaml. Here's my analysis...
</sf-chat-message>
```

### 3.2 `sf-chat-input`

```html
<sf-chat-input
  placeholder="Ask anything... /skill:name for skills"
  model-selector
  provider="deepseek"
  model="deepseek-v4-pro">
</sf-chat-input>
```

### 3.3 `sf-tool-call` (embedded in chat)

```html
<sf-tool-call tool="read_file" status="running">
  Reading D:/config.yaml...
</sf-tool-call>

<sf-tool-call tool="read_file" status="done" result="..." time="0.3s">
  Read 42 lines from config.yaml
</sf-tool-call>
```

---

## 4. Provider Components

### 4.1 `sf-provider-card`

```html
<sf-provider-card
  name="DeepSeek"
  models="deepseek-v4-pro, deepseek-v4-flash"
  status="connected"
  latency="120ms">
</sf-provider-card>
```

### 4.2 `sf-provider-form`

```html
<sf-provider-form mode="add">
  <!-- Form to add new provider -->
  <sf-input label="Provider Name" />
  <sf-input label="API Base URL" />
  <sf-input label="API Key" type="password" />
  <sf-button variant="primary">Test Connection</sf-button>
</sf-provider-form>
```

---

## 5. Component States

Every component has defined states:

| State | CSS Class | Example |
|-------|-----------|---------|
| Default | — | Normal state |
| Hover | `.hover` | Mouse over |
| Active | `.active` | Clicked |
| Focus | `.focus` | Keyboard focus |
| Disabled | `.disabled` | Inactive |
| Loading | `.loading` | Shows spinner |
| Error | `.error` | Error state |
| Empty | `.empty` | No data |

---

## 6. Implementation

All components implemented as **Web Components** (Custom Elements v1):

```javascript
class SfButton extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  static get observedAttributes() {
    return ['variant', 'size', 'disabled'];
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>/* scoped CSS */</style>
      <button class="sf-button ${this.getAttribute('variant')}">
        <slot></slot>
      </button>
    `;
  }
}

customElements.define('sf-button', SfButton);
```

**Benefits:**
- No frameworks — zero dependencies
- Scoped CSS — no style collisions
- Native web standard — works in all WebView environments
- Easy to test — each component isolated

---

**Status:** Phase 0 — Design
