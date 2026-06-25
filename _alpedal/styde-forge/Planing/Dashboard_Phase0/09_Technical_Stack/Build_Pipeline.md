# Build Pipeline

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

Build `StydeForge.exe` from source — step by step. Target: a single `.exe` file the user double-clicks. No installation required.

---

## 2. Project Structure

```
StydeForge/
├── Dashboard/
│   ├── src-tauri/              ← Rust backend
│   │   ├── Cargo.toml
│   │   ├── tauri.conf.json
│   │   ├── src/
│   │   │   ├── main.rs         ← Entry point
│   │   │   ├── commands.rs     ← Tauri commands
│   │   │   ├── hermes.rs       ← Hermes CLI bridge
│   │   │   ├── system.rs       ← System info/GPU
│   │   │   └── storage.rs      ← Credential store
│   │   └── icons/              ← App icons
│   │
│   ├── src/                    ← Frontend (HTML/CSS/JS)
│   │   ├── index.html
│   │   ├── css/
│   │   │   └── dashboard.css
│   │   ├── js/
│   │   │   ├── app.js          ← Main app
│   │   │   ├── agents.js       ← Agent panel
│   │   │   ├── benchmarks.js   ← Benchmark panel
│   │   │   ├── chat.js         ← Chat panel
│   │   │   ├── providers.js    ← Provider management
│   │   │   ├── system.js       ← System control
│   │   │   └── storage.js      ← IndexedDB
│   │   └── components/         ← Web Components
│   │       ├── sf-button.js
│   │       ├── sf-panel.js
│   │       ├── sf-agent-card.js
│   │       ├── sf-chart.js
│   │       ├── sf-chat-message.js
│   │       └── ...
│   │
│   ├── package.json            ← JS dependencies (Chart.js, etc.)
│   └── vite.config.js          ← Build tool
│
├── Dashboard_Phase0/           ← Design docs (this!)
└── v3.0_Phase0/                ← Forge design docs
```

---

## 3. Dependencies

### 3.1 Rust (Cargo.toml)

```toml
[dependencies]
tauri = { version = "2", features = ["tray-icon"] }
tauri-plugin-shell = "2"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
sysinfo = "0.31"           # System info
nvml-wrapper = "0.10"      # NVIDIA GPU
keyring = "3"              # Credential store
tokio = { version = "1", features = ["full"] }
```

### 3.2 JavaScript (package.json)

```json
{
  "dependencies": {
    "chart.js": "^4.4.0",
    "marked": "^12.0.0",
    "highlight.js": "^11.9.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@tauri-apps/cli": "^2.0.0"
  }
}
```

---

## 4. Build Steps

```
┌─────────────────────────────────────────┐
│ 1. Install dependencies                 │
│    $ cd Dashboard                       │
│    $ npm install                        │
│    $ cargo fetch                        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. Build frontend                       │
│    $ npm run build                      │
│    → Vite bundles HTML/CSS/JS to dist/  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. Build Tauri (Rust + bundle)          │
│    $ cargo tauri build                  │
│    → Compile Rust                       │
│    → Embed dist/                        │
│    → Create StydeForge.exe              │
│    → Create .msi installer              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. Output                               │
│    src-tauri/target/release/            │
│    ├── StydeForge.exe     (~6MB)        │
│    └── StydeForge.msi     (~3MB)        │
└─────────────────────────────────────────┘
```

---

## 5. CI/CD (GitHub Actions)

```yaml
name: Build StydeForge

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Setup Rust
        uses: actions-rust-lang/setup-rust-toolchain@v1

      - name: Install dependencies
        run: |
          cd Dashboard
          npm install

      - name: Build
        run: |
          cd Dashboard
          npm run build
          cargo tauri build

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: StydeForge-Windows
          path: Dashboard/src-tauri/target/release/StydeForge.exe
```

---

## 6. Release Process

```
1. Update version in tauri.conf.json
   "version": "1.0.0"

2. Create git tag
   $ git tag v1.0.0
   $ git push --tags

3. CI builds automatically

4. GitHub Release:
   • StydeForge.exe (portable)
   • StydeForge.msi (installer)
   • Changelog

5. Auto-updater fetches new version
```

---

## 7. File Size Budget

| Component | Expected Size |
|-----------|---------------|
| Tauri runtime (Rust) | ~2MB |
| WebView2 (system) | 0MB (part of Windows) |
| Frontend (HTML/CSS/JS) | ~500KB |
| Chart.js + marked + highlight.js | ~200KB |
| Web Components | ~100KB |
| Icons + assets | ~200KB |
| **Total .exe** | **~3-5MB** |
| .msi installer | ~2MB |

---

## 8. Development Environment

```bash
# First time setup
$ cd Dashboard
$ npm install
$ cargo tauri dev        # Start dev server with hot reload

# UI development (without Rust)
$ npm run dev            # Vite dev server on localhost:5173

# Build release
$ cargo tauri build      # Production build
```

---

**Status:** Phase 0 — Design
