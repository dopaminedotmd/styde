# Tauri Project Setup + Layout Implementation

**StydeForge Dashboard — Mission Control**
**Section:** 06_Dashboard_Shell
**References:** `Desktop_Framework_Choice.md`, `Build_Pipeline.md`, `Layout_Design.md`, `Design_System.md`

---

## 1. Tauri v2 Project Scaffold

### 1.1 Prerequisites Check

```bash
# Verify tools
node --version          # ≥ 20
npm --version           # ≥ 9
rustc --version         # ≥ 1.77
cargo --version

# Install Tauri CLI
cargo install tauri-cli --version "^2"

# Verify WebView2 (Windows)
# PowerShell: Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
# If missing: download from https://developer.microsoft.com/en-us/microsoft-edge/webview2/
```

### 1.2 Project Creation

```bash
cd D:\styde\_alpedal\styde-forge\Dashboard

# Create Tauri v2 project with vanilla HTML/CSS/JS template
npm create tauri-app@latest . -- --template vanilla-ts

# Project structure:
# Dashboard/
# ├── src/           # Frontend (TypeScript)
# │   ├── main.ts
# │   ├── styles.css
# │   └── index.html
# ├── src-tauri/     # Rust backend
# │   ├── Cargo.toml
# │   ├── tauri.conf.json
# │   └── src/
# │       └── main.rs
# ├── package.json
# └── tsconfig.json

# Install frontend deps
npm install marked highlight.js chart.js

# First build
cargo tauri dev    # Dev mode with hot reload
cargo tauri build  # Production .exe
```

### 1.3 `tauri.conf.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/tauri-apps/tauri/dev/crates/tauri-config-schema/schema.json",
  "productName": "StydeForge",
  "version": "1.0.0",
  "identifier": "com.alpedal.stydeforge",
  "build": {
    "frontendDist": "../dist",
    "devUrl": "http://localhost:1420",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build"
  },
  "app": {
    "title": "StydeForge — Mission Control",
    "windows": [
      {
        "title": "StydeForge — Mission Control",
        "width": 1400,
        "height": 900,
        "minWidth": 900,
        "minHeight": 600,
        "decorations": false,
        "resizable": true
      }
    ],
    "security": {
      "csp": "default-src 'self'; connect-src 'self' https://api.deepseek.com https://api.openai.com https://api.anthropic.com"
    },
    "trayIcon": {
      "iconPath": "icons/icon.png",
      "iconAsTemplate": true
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

---

## 2. HTML Layout

### 2.1 `src/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StydeForge — Mission Control</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <!-- Title Bar -->
  <header id="titlebar">
    <div class="titlebar-left">
      <span class="logo">⬡</span>
      <span class="title">StydeForge</span>
      <span class="subtitle">— Mission Control</span>
    </div>
    <div class="titlebar-center">
      <button id="btn-start" class="ctrl-btn" title="Start Forge">▶</button>
      <button id="btn-pause" class="ctrl-btn" title="Pause Forge">⏸</button>
      <button id="btn-stop" class="ctrl-btn" title="Stop Forge">⏹</button>
      <span class="divider">│</span>
      <span id="forge-status" class="status-indicator">● Stopped</span>
    </div>
    <div class="titlebar-right">
      <button id="btn-settings" class="ctrl-btn" title="Settings">⚙</button>
      <button id="btn-minimize" class="window-btn">─</button>
      <button id="btn-maximize" class="window-btn">□</button>
      <button id="btn-close" class="window-btn">✕</button>
    </div>
  </header>

  <!-- Main Content -->
  <main id="dashboard">
    <!-- Agent Panel -->
    <section id="panel-agents" class="panel">
      <div class="panel-header">
        <span class="panel-icon">📡</span>
        <span class="panel-title">AGENTS</span>
        <span id="agent-count" class="panel-badge">0</span>
      </div>
      <div id="agent-list" class="panel-content">
        <div class="empty-state">No agents active. Start Forge or spawn manually.</div>
      </div>
    </section>

    <!-- Benchmark Panel -->
    <section id="panel-benchmarks" class="panel">
      <div class="panel-header">
        <span class="panel-icon">📊</span>
        <span class="panel-title">BENCHMARKS</span>
      </div>
      <div id="benchmark-content" class="panel-content">
        <div class="empty-state">No benchmark data yet. Run agents to collect metrics.</div>
      </div>
    </section>

    <!-- Chat Panel -->
    <section id="panel-chat" class="panel">
      <div class="panel-header">
        <span class="panel-icon">💬</span>
        <span class="panel-title">CHAT</span>
        <select id="model-selector" class="model-dropdown">
          <option value="deepseek-v4-pro">DeepSeek V4 Pro</option>
          <option value="deepseek-v4-flash">DeepSeek V4 Flash</option>
        </select>
      </div>
      <div id="chat-messages" class="panel-content">
        <div class="empty-state">
          <strong>StydeForge Chat</strong>
          <p>Ask me anything. I can read/write files, run commands, and use skills.</p>
          <p>Try: <code>read D:/config.yaml</code> or <code>skill:code-review on D:/project/</code></p>
        </div>
      </div>
      <div id="chat-input-area">
        <textarea id="chat-input" placeholder="Type a message..." rows="2"></textarea>
        <button id="btn-send" class="send-btn">↑</button>
      </div>
    </section>
  </main>

  <!-- Status Bar -->
  <footer id="statusbar">
    <span id="status-dot" class="dot stopped">●</span>
    <span id="status-text">Stopped</span>
    <span class="sep">|</span>
    <span id="status-agents">0 agents</span>
    <span class="sep">|</span>
    <span id="status-tokens">0 tokens</span>
    <span class="sep">|</span>
    <span id="status-cost">$0.000</span>
    <span class="sep">|</span>
    <span id="status-speed">⚡ 0 t/s</span>
  </footer>

  <script type="module" src="main.ts"></script>
</body>
</html>
```

---

## 3. CSS — Dark Theme Design System

### 3.1 `src/styles.css`

```css
/* === CSS Variables — Dark Theme === */
:root {
  /* Backgrounds */
  --bg-primary: #0d0d1a;
  --bg-secondary: #1a1a2e;
  --bg-tertiary: #2a2a4a;
  --bg-hover: #3a3a5a;
  --bg-input: #1a1a2e;
  
  /* Text */
  --text-primary: #e0e0e0;
  --text-secondary: #a0a0b0;
  --text-muted: #606070;
  --text-accent: #7c3aed;
  
  /* Borders */
  --border-color: #2a2a4a;
  --border-focus: #7c3aed;
  
  /* Status colors */
  --status-running: #22c55e;
  --status-paused: #eab308;
  --status-stopped: #ef4444;
  --status-done: #3b82f6;
  --status-failed: #ef4444;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 12px;
  --spacing-lg: 16px;
  --spacing-xl: 24px;
  
  /* Typography */
  --font-mono: 'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace;
  --font-sans: 'Inter', 'Segoe UI', system-ui, sans-serif;
  --font-size-xs: 11px;
  --font-size-sm: 12px;
  --font-size-md: 13px;
  --font-size-lg: 14px;
  --font-size-xl: 16px;
  
  /* Layout */
  --titlebar-height: 40px;
  --statusbar-height: 28px;
  --panel-header-height: 36px;
}

/* === Reset === */
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100vh;
  overflow: hidden;
  font-family: var(--font-sans);
  font-size: var(--font-size-md);
  color: var(--text-primary);
  background: var(--bg-primary);
}

/* === Title Bar === */
#titlebar {
  height: var(--titlebar-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--spacing-md);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  user-select: none;
  -webkit-app-region: drag;
}

.titlebar-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.logo {
  font-size: 18px;
  color: var(--text-accent);
}

.title {
  font-weight: 700;
  font-size: var(--font-size-lg);
  color: var(--text-primary);
}

.subtitle {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.titlebar-center {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  -webkit-app-region: no-drag;
}

.titlebar-right {
  display: flex;
  align-items: center;
  gap: 2px;
  -webkit-app-region: no-drag;
}

.ctrl-btn, .window-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 4px 8px;
  font-size: var(--font-size-md);
  border-radius: 4px;
}

.ctrl-btn:hover, .window-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.window-btn:last-child:hover {
  background: var(--status-failed);
}

.status-indicator {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.divider {
  color: var(--border-color);
}

/* === Main Dashboard Grid === */
#dashboard {
  display: grid;
  grid-template-columns: 30% 35% 35%;
  grid-template-rows: 1fr;
  height: calc(100vh - var(--titlebar-height) - var(--statusbar-height));
  gap: 0;
}

/* === Panels === */
.panel {
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-color);
  overflow: hidden;
}

.panel:last-child {
  border-right: none;
}

.panel-header {
  height: var(--panel-header-height);
  display: flex;
  align-items: center;
  padding: 0 var(--spacing-md);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  font-size: var(--font-size-xs);
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
  gap: var(--spacing-sm);
}

.panel-icon {
  font-size: 14px;
}

.panel-title {
  flex: 1;
}

.panel-badge {
  background: var(--text-accent);
  color: white;
  font-size: var(--font-size-xs);
  padding: 1px 6px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.model-dropdown {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 2px 6px;
  font-size: var(--font-size-xs);
  font-family: var(--font-sans);
  cursor: pointer;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--spacing-md);
}

/* Scrollbar */
.panel-content::-webkit-scrollbar {
  width: 6px;
}
.panel-content::-webkit-scrollbar-track {
  background: var(--bg-primary);
}
.panel-content::-webkit-scrollbar-thumb {
  background: var(--bg-tertiary);
  border-radius: 3px;
}

/* === Empty States === */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--text-muted);
  text-align: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl);
}

.empty-state strong {
  color: var(--text-secondary);
}

.empty-state code {
  background: var(--bg-tertiary);
  padding: 2px 6px;
  border-radius: 3px;
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

/* === Chat === */
#panel-chat .panel-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.chat-message {
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 8px;
  max-width: 85%;
  font-size: var(--font-size-md);
  line-height: 1.5;
}

.chat-message.user {
  align-self: flex-end;
  background: var(--text-accent);
  color: white;
}

.chat-message.assistant {
  align-self: flex-start;
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.chat-message pre {
  background: var(--bg-primary);
  padding: var(--spacing-md);
  border-radius: 6px;
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

.chat-message code {
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}

#chat-input-area {
  display: flex;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

#chat-input {
  flex: 1;
  background: var(--bg-input);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: var(--spacing-sm) var(--spacing-md);
  font-family: var(--font-sans);
  font-size: var(--font-size-md);
  resize: none;
  outline: none;
}

#chat-input:focus {
  border-color: var(--border-focus);
}

.send-btn {
  background: var(--text-accent);
  color: white;
  border: none;
  border-radius: 6px;
  padding: var(--spacing-sm) var(--spacing-md);
  cursor: pointer;
  font-size: var(--font-size-lg);
  font-weight: 700;
}

.send-btn:hover {
  opacity: 0.9;
}

/* === Agent Cards === */
.agent-card {
  background: var(--bg-tertiary);
  border-radius: 6px;
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  border-left: 3px solid var(--border-color);
}

.agent-card.running { border-left-color: var(--status-running); }
.agent-card.done { border-left-color: var(--status-done); }
.agent-card.failed { border-left-color: var(--status-failed); }

.agent-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.agent-name {
  font-weight: 600;
  font-size: var(--font-size-md);
}

.agent-status {
  font-size: var(--font-size-xs);
  padding: 2px 8px;
  border-radius: 4px;
}

.agent-status.running { background: rgba(34, 197, 94, 0.15); color: var(--status-running); }
.agent-status.done { background: rgba(59, 130, 246, 0.15); color: var(--status-done); }
.agent-status.failed { background: rgba(239, 68, 68, 0.15); color: var(--status-failed); }

.agent-meta {
  font-size: var(--font-size-xs);
  color: var(--text-muted);
  font-family: var(--font-mono);
}

/* === Status Bar === */
#statusbar {
  height: var(--statusbar-height);
  display: flex;
  align-items: center;
  padding: 0 var(--spacing-md);
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  gap: var(--spacing-sm);
  font-family: var(--font-mono);
}

.dot { font-size: 8px; }
.dot.running { color: var(--status-running); }
.dot.stopped { color: var(--status-stopped); }
.dot.paused { color: var(--status-paused); }

.sep { color: var(--border-color); }

/* === Responsive === */
@media (max-width: 1100px) {
  #dashboard {
    grid-template-columns: 1fr;
  }
  .panel:nth-child(2),
  .panel:nth-child(3) {
    display: none;
  }
  /* TODO: Tab navigation for mobile-width */
}
```

---

## 4. Tauri Rust Backend — `src-tauri/src/main.rs`

```rust
// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::process::Command;
use std::fs;

#[tauri::command]
fn read_file(path: String) -> Result<String, String> {
    fs::read_to_string(&path)
        .map_err(|e| format!("Failed to read {}: {}", path, e))
}

#[tauri::command]
fn write_file(path: String, content: String) -> Result<(), String> {
    // Security: allowlist check
    let allowed = path.starts_with("D:\\") 
        || path.starts_with(&std::env::var("USERPROFILE").unwrap_or_default());
    if !allowed {
        return Err("Path not allowed. Write access limited to D:\\ and user home.".into());
    }
    fs::write(&path, content)
        .map_err(|e| format!("Failed to write {}: {}", path, e))
}

#[tauri::command]
fn search_files(pattern: String, path: String) -> Result<String, String> {
    let output = Command::new("rg")
        .args(["--no-heading", "-n", &pattern, &path])
        .output()
        .map_err(|e| format!("Search failed: {}", e))?;
    String::from_utf8(output.stdout)
        .map_err(|e| format!("Invalid UTF-8: {}", e))
}

#[tauri::command]
fn hermes_command(args: Vec<String>) -> Result<String, String> {
    let output = Command::new("hermes")
        .args(&args)
        .output()
        .map_err(|e| format!("Hermes command failed: {}", e))?;
    String::from_utf8(output.stdout)
        .map_err(|e| format!("Invalid UTF-8: {}", e))
}

#[tauri::command]
fn get_system_info() -> Result<String, String> {
    // Return hardware info for status bar
    let gpu = Command::new("nvidia-smi")
        .args(["--query-gpu=utilization.gpu,temperature.gpu", "--format=csv,noheader,nounits"])
        .output()
        .ok()
        .and_then(|o| String::from_utf8(o.stdout).ok())
        .unwrap_or_default();
    Ok(gpu)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            read_file,
            write_file,
            search_files,
            hermes_command,
            get_system_info,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

---

## 5. First Build Verification

```bash
cd D:\styde\_alpedal\styde-forge\Dashboard

# Dev mode (opens window with hot reload)
cargo tauri dev

# Production build
cargo tauri build
# Output: src-tauri/target/release/StydeForge.exe (~5-8 MB)

# Verify
ls -lh src-tauri/target/release/StydeForge.exe
```

### Success criteria:
- [ ] Window opens with dark theme
- [ ] 3 panels visible (Agents, Benchmarks, Chat)
- [ ] Title bar shows "StydeForge — Mission Control"
- [ ] Custom window controls work (min/max/close)
- [ ] Empty states show in all panels
- [ ] Status bar visible at bottom
- [ ] `.exe` is < 10 MB
- [ ] Memory usage < 150 MB idle

---

**Status:** Specification complete. Ready for `npm create tauri-app`.
