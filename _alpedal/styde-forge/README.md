# StydeForge

**Portable Evolutionary Elite Agent Refinery + Mission Control Dashboard**

---

## What is StydeForge?

Two integrated projects:

### 1. StydeForge Forge — The Refinery (`Planing/v3.0_Phase0/`)

A portable USB-based system that transforms raw agent blueprints into world-class specialized agents through a continuous loop of spawning, evaluation, improvement, and checkpointing.

- **Dual-model strategy:** deepseek-v4-flash (agents) + deepseek-v4-pro (eval/teacher)
- **Caveman Ultra:** 70% fewer tokens, 2x faster, 3x cheaper
- **Quality gate:** Nothing below 80/100 reaches the USB
- **Hardware-aware:** Auto-adapts to available GPUs
- **Status:** Phase 0 design — 53 documents, 13 sections

### 2. StydeForge Dashboard — Mission Control (`Planing/Dashboard_Phase0/`)

A Tauri-based desktop application (`StydeForge.exe`) that serves as the command center for the entire StydeForge ecosystem.

- **Monitor:** Live agent tracking, benchmark visualization, system health
- **Control:** Start/pause/stop the Forge pipeline with one click
- **Chat:** Full AI agent with tools (read/write files, terminal, web, skills)
- **Multi-model:** DeepSeek, OpenAI, Anthropic, custom REST, local Ollama
- **Status:** Phase 0 design — 36 documents, 10 sections

---

## Project Structure

```
StydeForge/
├── README.md                     ← You are here
│
├── Planing/v3.0_Phase0/                  ← Forge design (Phase 0)
│   ├── 00_Overview/              (architecture, core loop, data models)
│   ├── 01_Vision/                (vision, goals, blueprint catalog)
│   ├── 02_Hardware/              (adaptation layer, resource governor)
│   ├── 03_Eval_Pipeline/         (6-layer eval system)
│   ├── 04_Sampling_Stack/        (NUTS, HMC, VI)
│   ├── 05_Meta_Layer/            (model selection, learning)
│   ├── 06_Persistence_Safety/    (atomic writes, recovery)
│   ├── 07_Multi_Agent/           (collaboration, security)
│   ├── 08_Import_Export/         (import, sync)
│   ├── 09_Risk_Maintenance/      (maintenance, cleanup)
│   ├── 10_Operations/            (skills, logging, costs, Caveman)
│   ├── 11_Knowledge_Management/  (knowledge lifecycle)
│   ├── 12_Teacher_Agent/         (teacher loop, feedback)
│   └── 13_Hooks_Events/          (event system, hooks)
│
├── Planing/Dashboard_Phase0/             ← Dashboard design (Phase 0)
│   ├── 00_Overview/              (vision, architecture, index)
│   ├── 01_Application_Shell/     (window, lifecycle, processes, tray)
│   ├── 02_UI_UX/                 (layout, design system, components, onboarding)
│   ├── 03_Agent_Monitor/         (tracking, detail view, spawn)
│   ├── 04_Benchmark_Panel/       (performance, quality, visualization)
│   ├── 05_Chat_Interface/        (chat, tools, skills, persistence)
│   ├── 06_Model_Provider_System/ (abstraction, built-in, custom, local)
│   ├── 07_System_Control/        (start/stop, config, health)
│   ├── 08_Data_Layer/            (Hermes bridge, polling, storage)
│   ├── 09_Technical_Stack/       (framework choice, build, auto-update)
│   └── 10_Phase_Transition/      (roadmap to implementation)
│
└── Dashboard/                    ← Implementation (Phase 1+)
    └── (Tauri project — empty, ready to build)
```

---

## How They Connect

```
┌──────────────────────┐     ┌──────────────────────┐
│   StydeForge.exe     │     │   Hermes Agent       │
│   (Dashboard)        │────▶│   (CLI + Runtime)    │
│                      │     │                      │
│  • Monitor agents    │     │  • Forge loop        │
│  • Control pipeline  │     │  • Agent spawning    │
│  • Chat with AI      │     │  • Eval pipeline     │
│  • View benchmarks   │     │  • Skill loading     │
│  • System health     │     │  • Cron jobs         │
└──────────────────────┘     └──────────────────────┘
         │                            │
         │  hermes process list       │
         │  hermes forge start/stop   │
         │  hermes delegate_task      │
         └────────────────────────────┘
```

The Dashboard is the face. Hermes/Forge is the engine.

---

## Current Status

| Component | Phase | Status |
|-----------|-------|--------|
| Forge (v3.0) | Phase 0 — Design | ✅ Complete (53 docs) |
| Dashboard | Phase 0 — Design | ✅ Complete (36 docs) |
| Dashboard | Phase 1 — Implementation | ⬜ Not started |

---

## Next Steps (P0 Priority)

1. **Core loop** → Blueprint spawn → Eval pipeline (Forge)
2. **Dashboard shell** → Chat with tools → Agent monitor (Dashboard)
3. These are the two tracks that make everything real

---

## Reading Order

1. `Planing/v3.0_Phase0/00_Overview/PHASE0_INDEX.md` — Forge overview
2. `Planing/Dashboard_Phase0/00_Overview/DASHBOARD_INDEX.md` — Dashboard overview
3. Then dive into the section that interests you

---

**Last Updated:** 2026-06-25
