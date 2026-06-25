# Desktop Framework Choice

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

Choosing a desktop framework is the most important technical decision. It affects size, performance, development speed, and platform support.

---

## 2. Candidates

### 2.1 Tauri v2

| Pros | Cons |
|------|------|
| ✅ Small .exe (~5MB) | ⚠ Rust knowledge required for backend |
| ✅ Memory efficient (~50MB idle) | ⚠ Younger ecosystem |
| ✅ Native performance (Rust) | |
| ✅ WebView-based UI (HTML/CSS/JS) | |
| ✅ Built-in process management | |
| ✅ Filesystem API in Rust | |
| ✅ Windows, Mac, Linux | |
| ✅ System tray support | |
| ✅ Auto-updater built-in | |
| ✅ Secure (least privilege) | |
| ✅ Active development, good docs | |

### 2.2 Electron

| Pros | Cons |
|------|------|
| ✅ Mature ecosystem | ❌ Large .exe (~150MB) |
| ✅ Chromium + Node.js | ❌ High memory usage (~200MB idle) |
| ✅ Large community | ❌ Slow startup |
| ✅ Many pre-built packages | ❌ Security concerns (Node in renderer) |

### 2.3 Python + WebView (pywebview / Flask + browser)

| Pros | Cons |
|------|------|
| ✅ Python — already installed | ❌ Larger distribution |
| ✅ Fast prototyping | ❌ No official packager |
| ✅ Good for Pontus (Python experience) | ❌ Lower performance |
| | ❌ No native system tray |

### 2.4 WPF / .NET (Windows-only)

| Pros | Cons |
|------|------|
| ✅ Native Windows | ❌ Windows only |
| ✅ High performance | ❌ No web-based UI |
| ✅ Good tooling (Visual Studio) | ❌ Less flexible UI |
| | ❌ Heavier development |

---

## 3. Recommendation: Tauri v2

**Why Tauri?**

| Need | How Tauri solves it |
|------|---------------------|
| Small .exe | ~5MB vs Electron's ~150MB |
| Chat with markdown | WebView — HTML/CSS/JS works perfectly |
| Process management | Rust `std::process::Command` — native, safe |
| Filesystem | Rust `std::fs` — fast, safe, atomic |
| GPU monitoring | Rust `nvml` crate — direct NVIDIA API |
| System tray | `tauri-plugin-tray` — built-in |
| Build .exe | `tauri build` → one .msi/.exe |
| Performance | Rust backend — no JS in backend |

---

## 4. Tauri Architecture in the Dashboard

```
┌──────────────────────────────────────────┐
│              Tauri App                    │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │         WebView (Frontend)         │  │
│  │  HTML + CSS + JS (Web Components)  │  │
│  │  • Chart.js (graphs)               │  │
│  │  • marked.js (markdown)            │  │
│  │  • highlight.js (syntax)           │  │
│  └──────────────┬─────────────────────┘  │
│                 │ IPC (invoke)            │
│  ┌──────────────┴─────────────────────┐  │
│  │         Rust Backend               │  │
│  │  • Process manager (spawn/kill)    │  │
│  │  • Hermes CLI bridge               │  │
│  │  • File system ops                 │  │
│  │  • GPU monitoring (nvml)           │  │
│  │  • System info (sysinfo)           │  │
│  │  • Credential store                │  │
│  └────────────────────────────────────┘  │
│                                          │
└──────────────────────────────────────────┘
```

---

## 5. Final Score Comparison

| Factor | Tauri | Electron | Python+WebView | WPF |
|--------|-------|----------|----------------|-----|
| .exe size | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Memory usage | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Startup time | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| UI flexibility | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Native integration | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Dev speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Community/support | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Cross-platform | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐ |
| **TOTAL** | **37** | **31** | **28** | **26** |

---

## 6. Risks with Tauri

| Risk | Mitigation |
|------|------------|
| Rust knowledge needed | Dashboard backend is relatively simple (CLI calls, filesystem, system info) — learnable threshold |
| WebView limitations | Windows uses WebView2 (Edge/Chromium) — works well |
| Smaller community | Tauri is growing fast, good docs, active Discord |
| Tauri APIs change | Pin version in Cargo.toml, test on upgrade |

---

## 7. Alternative: Hybrid Tauri + Python

If the Rust learning curve is too steep initially:

```
Tauri (Rust) ←── HTTP/localhost ──→ Python microservice
     │                                    │
  Frontend                          Hermes CLI bridge
  Filesystem                        Heavy processing
  GPU monitoring
```

Python runs as a sidecar for Hermes interaction. Tauri handles UI + filesystem + GPU. Python handles Hermes commands.

**Recommendation: Start with pure Tauri. Add Python sidecar only if needed.**

---

**Status:** Phase 0 — Design
