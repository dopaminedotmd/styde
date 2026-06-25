# Phase 0 → Phase 1 Transition

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

Phase 0 is design — nothing has been implemented. Phase 1 is the first implementation: a working MVP with core functionality.

---

## 2. Phase 0 — Summary

| Metric | Value |
|--------|-------|
| Design documents | 35 |
| Sections | 10 |
| Pages estimated | ~200+ |
| Status | ✅ Complete |

**What Phase 0 has specified:**
- Application architecture and all layers
- All UI components and their states
- Provider system (DeepSeek, OpenAI, Anthropic, Custom, Local)
- Chat agent with 8 tools
- Skill command system
- Agent monitoring and benchmark visualization
- System control (start/pause/stop)
- Health monitoring (CPU, GPU, RAM, disk)
- Data layer (Hermes CLI bridge, IndexedDB, polling)
- Tech stack (Tauri v2, Rust, HTML/CSS/JS)
- Build pipeline and auto-update

---

## 3. Phase 1 — Scope (MVP)

**P0 is the only priority for Phase 1.** Do not start P1 or P2 until P0 is complete and stable. The critical path is: **Core Loop → Blueprint Spawn → Eval Pipeline** (Forge) and **Dashboard Shell → Chat with Tools → Agent Monitor** (Dashboard). Everything else depends on these.

### 3.1 Must have — P0 (critical path)

| Feature | Priority | Estimated Time |
|---------|----------|----------------|
| Tauri app launches and shows window | P0 | 2 days |
| Basic layout (3 panels, resizable) | P0 | 3 days |
| Dark theme and design system | P0 | 2 days |
| DeepSeek provider (API key → chat) | P0 | 2 days |
| Chat panel with streaming | P0 | 3 days |
| Chat: read_file, write_file, search_files tools | P0 | 3 days |
| Hermes CLI bridge (process list) | P0 | 2 days |
| Agent panel (list agents, status) | P0 | 3 days |
| Start/Stop buttons for Forge | P0 | 2 days |
| Status bar with basic info | P0 | 1 day |

**P0 total: ~23 days**

### 3.2 Should Have (P1)

| Feature | Priority | Estimated Time |
|---------|----------|----------------|
| Chat: patch, terminal tools (with confirmation) | P1 | 2 days |
| Chat: skill commands (/skill:name) | P1 | 2 days |
| Additional providers (OpenAI, Anthropic) | P1 | 2 days |
| Agent Detail View | P1 | 3 days |
| Configuration panel | P1 | 3 days |
| System tray + notifications | P1 | 2 days |
| Chat sessions (save/load) | P1 | 2 days |

**P1 total: ~16 days**

### 3.3 Nice to Have (P2)

| Feature | Priority | Estimated Time |
|---------|----------|----------------|
| Benchmark panel (graphs) | P2 | 5 days |
| System Health Monitoring | P2 | 3 days |
| Ollama provider | P2 | 2 days |
| Custom provider (OpenAI-compatible) | P2 | 2 days |
| Spawn New Agent (from dashboard) | P2 | 2 days |
| Auto-update | P2 | 2 days |

**P2 total: ~16 days**

---

## 4. Phase 1 — Timeline (estimated)

```
Week 1-2:   Foundation (Tauri, layout, theme, DeepSeek provider)
            → App launches, dark theme, chat works

Week 3-4:   Chat tools + Hermes bridge
            → Chat can read/write files, agent panel works

Week 5-6:   Agent panel + Forge control
            → Start/stop Forge, see agents in real-time

Week 7-8:   P1 features
            → More providers, skills, detail view, configuration

Week 9+:    P2 features
            → Benchmarks, health, local model, custom provider
```

**MVP (P0) complete:** ~6 weeks
**v1.0 (P0+P1):** ~10 weeks
**v1.1 (P0+P1+P2):** ~14 weeks

---

## 5. Technical Prerequisites

Before Phase 1 can begin:

| Prerequisite | Status |
|--------------|--------|
| Rust installed | Needs install (`rustup`) |
| Node.js 20+ | Needs verification |
| Tauri CLI | Needs install (`cargo install tauri-cli`) |
| Hermes Agent | Already installed ✅ |
| DeepSeek API key | Already configured in Hermes ✅ |

---

## 6. Definition of Done — Phase 1 MVP

- [ ] `StydeForge.exe` launches on Windows
- [ ] Dark theme with 3 panels displayed
- [ ] Chat works with DeepSeek (streaming)
- [ ] Chat can read files (`read_file`)
- [ ] Chat can write files (`write_file` with confirmation)
- [ ] Agent panel shows active agents from Hermes
- [ ] Start/Stop buttons function
- [ ] Status bar shows basic info
- [ ] App minimizes to system tray
- [ ] Configuration saves and loads

---

## 7. Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Tauri APIs change | Low | Medium | Pin versions |
| Hermes CLI output changes | Medium | Medium | Use `--json` flag, validate schema |
| WebView2 not installed | Low (Windows 10+) | High | Bundle WebView2 in installer |
| Rust compile time | High (first build) | Low | CI builds, develop with `cargo tauri dev` |
| Performance with many agents | Medium | Medium | Virtual scroll, delta updates |

---

## 8. Next Steps

1. **Set up development environment:**
   ```bash
   cargo install tauri-cli --version "^2"
   npm create tauri-app@latest StydeForge -- --template vanilla
   ```

2. **Create basic layout:**
   - HTML/CSS per `Layout_Design.md` and `Design_System.md`

3. **Implement DeepSeek provider:**
   - Per `Provider_Architecture.md` and `Built_In_Providers.md`

4. **Iterative development:**
   - One feature at a time
   - Test against real Hermes installation
   - Show Pontus early and often for feedback

---

**Status:** Phase 0 — Complete ✅. Ready for Phase 1.
