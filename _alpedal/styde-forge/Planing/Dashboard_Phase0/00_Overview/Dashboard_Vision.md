# Dashboard Vision & Goals

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. What is StydeForge Dashboard?

StydeForge Dashboard is **the entire program** — not a separate webpage monitoring something else. It is the `StydeForge.exe` desktop application the user interacts with.

Three core functions in a single window:
- **Monitor** — view all agents, benchmarks, system health
- **Control** — start, pause, stop the Forge system
- **Chat** — a full agent that reads/writes files, runs commands, uses skills

---

## 2. Why?

**Today's problem (without Dashboard):**
- Agent monitoring requires terminal commands (`hermes process list`, `hermes cronjob list`)
- No overview of performance and cost over time
- Start/stop done manually via CLI
- No unified place to interact with the system
- Switching models = digging through config files

**Solution:**
A single .exe. Double-click. Everything is there.

---

## 3. Goals

### 3.1 Primary Goals (MVP — Phase 1)

| Goal | Description | Success Criterion |
|------|-------------|-------------------|
| **Agent Monitoring** | See all active/done agents in real-time | List updates within 2s of status change |
| **System Control** | Start/pause/stop Forge from one button | One click = entire pipeline stops |
| **Chat with Tools** | Chat with an AI agent that reads/writes files | Chat can edit a file on disk |
| **Model Switching** | Switch AI model in chat via dropdown | DeepSeek → OpenAI = one click |

### 3.2 Secondary Goals (Phase 2+)

| Goal | Description |
|------|-------------|
| **Benchmark View** | See performance over time — tokens/s, cost, eval results |
| **Custom Providers** | Connect custom LLM via REST endpoint |
| **Local Models** | Support Ollama, llama.cpp — run locally |
| **System Health** | CPU/GPU/RAM/Disk — live |
| **System Tray** | Minimize to tray, notifications for key events |
| **Auto Update** | App updates itself |

---

## 4. Non-Goals (what the Dashboard is NOT)

- **Not an IDE** — no code editor, no project management
- **Not a model trainer** — no fine-tuning, no dataset management
- **Not a web server** — runs locally, no remote access (MVP)
- **Not a terminal replacement** — advanced debugging still done in CLI

---

## 5. User Flow

```
1. Double-click StydeForge.exe
        │
2. Dashboard opens with 3 panels
        │
   ┌────┴────┬────────────┬────────────┐
   │ AGENTS  │ BENCHMARKS │    CHAT    │
   │ (list)  │  (graphs)  │ (full agent│
   └─────────┴────────────┴────────────┘
        │
3. Top bar: [▶ Start] [⏸ Pause] [⏹ Stop] [⚙ Settings]
        │
4. Chat always available — right/bottom panel
   • "read D:/config.yaml and optimize it"
   • Agent reads file, analyzes, writes back
   • "skill:code-review on D:/project/"
   • Agent runs code-review with that skill
```

---

## 6. Target Audience

**Primary:** Pontus (developer, AI engineer)
- Wants control over his agent ecosystem
- Frequently switches models (DeepSeek, OpenAI, local)
- Heavy skill usage
- Wants visibility without digging through logs

**Secondary:** Other developers running Hermes/StydeForge
- Same needs but with their own providers and skills

---

## 7. Success Metrics

| Metric | Target |
|--------|--------|
| Time from double-click to functional dashboard | < 3 seconds |
| Time to switch model in chat | < 5 seconds (select + verify) |
| Steps to stop Forge | 1 click |
| Chat response time (first token) | < 2 seconds |
| Memory usage (idle) | < 150 MB |
| Install size (.exe) | < 80 MB |

---

**Status:** Phase 0 — Design
