# StydeForge Dashboard — Phase 0 Index

**Project:** StydeForge Mission Control
**Type:** Desktop application — agent control, monitoring, chat
**Version:** 1.0
**Status:** Phase 0 — Complete ✅

---

## Document Overview (35 documents)

| # | Section | Document | Description |
|---|---------|----------|-------------|
| 00 | Overview | `DASHBOARD_INDEX.md` | This index |
| 00 | Overview | `Dashboard_Vision.md` | Vision, goals, success criteria |
| 00 | Overview | `Application_Architecture.md` | High-level architecture, components, data flow |
| 01 | Application Shell | `Window_Management.md` | Window management, size, position, multi-monitor |
| 01 | Application Shell | `Lifecycle_Management.md` | Start/pause/stop the StydeForge system |
| 01 | Application Shell | `Process_Control.md` | Spawn/kill Hermes processes, cron jobs |
| 01 | Application Shell | `System_Tray_Integration.md` | Minimize to tray, status indicator, notifications |
| 02 | UI/UX | `Layout_Design.md` | Grid system, 3 panels, resizable, responsive |
| 02 | UI/UX | `Design_System.md` | Dark theme, typography, color palette, icons |
| 02 | UI/UX | `Component_Library.md` | Reusable components (buttons, panels, tabs) |
| 03 | Agent Monitor | `Agent_Tracking.md` | Active/done/failed agent list, live updates |
| 03 | Agent Monitor | `Agent_Detail_View.md` | Detail view: tokens, cost, log, output, history |
| 03 | Agent Monitor | `Spawn_New_Agent.md` | Spawn agent manually from dashboard |
| 04 | Benchmark Panel | `Performance_Metrics.md` | Tokens/s, latency, cost — per agent and model |
| 04 | Benchmark Panel | `Quality_Benchmarks.md` | Eval results (HumanEval, MMLU, custom benchmarks) |
| 04 | Benchmark Panel | `Visualization_Strategy.md` | Graphs, time series, comparisons — Chart.js |
| 05 | Chat Interface | `Chat_Architecture.md` | Chat window, streaming, markdown rendering |
| 05 | Chat Interface | `Chat_Agent_Tools.md` | Tools: read/write/edit files, run commands |
| 05 | Chat Interface | `Skill_Command_System.md` | "skill:X" → load + run skill in chat |
| 05 | Chat Interface | `Chat_Persistence.md` | Save/restore sessions, export |
| 06 | Model Providers | `Provider_Architecture.md` | Abstract interface for model backends |
| 06 | Model Providers | `Built_In_Providers.md` | DeepSeek, OpenAI, Anthropic — built-in providers |
| 06 | Model Providers | `Custom_Provider_API.md` | Connect custom LLM: REST, OpenAI-compatible |
| 06 | Model Providers | `Local_Model_Support.md` | Ollama, llama.cpp, local inference |
| 06 | Model Providers | `Provider_Configuration_UI.md` | Add/remove/switch provider in UI |
| 07 | System Control | `Start_Stop_Pipeline.md` | Start/pause/stop the entire Forge loop |
| 07 | System Control | `Configuration_Panel.md` | Settings: models, providers, paths, resources |
| 07 | System Control | `Health_Monitoring.md` | CPU, GPU, RAM, disk — live system health |
| 08 | Data Layer | `Hermes_CLI_Bridge.md` | Call Hermes commands from the app |
| 08 | Data Layer | `Real_Time_Updates.md` | Polling vs WebSocket vs IPC — strategy |
| 08 | Data Layer | `Local_Storage.md` | IndexedDB/SQLite for history, settings |
| 09 | Technical Stack | `Desktop_Framework_Choice.md` | Tauri vs Electron vs Python — analysis and choice |
| 09 | Technical Stack | `Build_Pipeline.md` | How to build StydeForge.exe |
| 09 | Technical Stack | `Auto_Update.md` | Self-update, version management |
| 10 | Phase Transition | `Phase0_to_Phase1.md` | Design → implementation: scope, prioritization |

---

## Recommended Reading Order

1. `DASHBOARD_INDEX.md` ← You are here
2. `Dashboard_Vision.md` — Why are we building this?
3. `Application_Architecture.md` — High-level overview of the app
4. `02_UI_UX/Layout_Design.md` — What does it look like?
5. `06_Model_Provider_System/Provider_Architecture.md` — Chat engine
6. `05_Chat_Interface/Chat_Agent_Tools.md` — What can the chat do?
7. `09_Technical_Stack/Desktop_Framework_Choice.md` — Technology choice
8. Then: Application Shell → Agent Monitor → Benchmark → System Control → Data Layer → Build → Phase Transition

---

## Design Principles

| Principle | Meaning |
|-----------|---------|
| **App = Mission Control** | The dashboard is the entire program — no separate service |
| **One button for everything** | Start, pause, stop StydeForge from one place |
| **Provider-agnostic** | Switch model with one click — DeepSeek, OpenAI, custom |
| **Chat is an agent** | Not just Q&A — it reads/writes/edits files |
| **Dark and compact** | Terminal aesthetic, nothing unnecessary |
| **Portable** | Single .exe — no dependencies, no installation |

---

**Status:** Phase 0 — Complete ✅. 35 design documents across 10 sections.
**Last Updated:** 2026-06-25
