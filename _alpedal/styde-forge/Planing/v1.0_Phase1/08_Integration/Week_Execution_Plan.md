# Week Execution Plan — Phase 1

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 08_Integration
**References:** `IMPLEMENTATION_ORDER.md`, `PHASE1_SCOPE.md`, `PHASE1_ROADMAP.md`

---

## Overview

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Foundation | USB structure, hardware detection, Tauri scaffold, dark theme |
| 2 | Spawn + Chat | Blueprint loading, delegate_task, chat with streaming |
| 3 | Eval + Tools | Self-eval, judge-eval, composite scoring, chat tools |
| 4 | Improve + Monitor | Teacher agent, checkpoint, agent panel, start/stop |
| 5 | Polish + Integration | End-to-end test, Forge↔Dashboard bridge, bug fixes |
| 6 | Production hardening | Recovery, circuit breaker, P0 exit criteria |

---

## Week 1 — Foundation (Days 1-7)

### Day 1: Environment Verification
```
□ Verify Python 3.11+, pip, virtualenv
□ Verify Node.js 20+, npm
□ Verify Rust + Cargo
□ Verify Hermes Agent v0.17.0+
□ Verify DeepSeek API key
□ Verify nvidia-smi, CUDA
□ Verify WebView2
□ Install Tauri CLI: cargo install tauri-cli --version "^2"
□ Install Python deps: psutil, torch, faiss-cpu, pyyaml
```

### Day 2-3: Forge Foundation
```
□ persistence.py
  - atomic_write(path, content)
  - atomic_write_json(path, dict)
  - atomic_append(path, line)
  - Unit tests: force failure mid-write, verify no partial file

□ detect.py
  - nvidia-smi parsing → VRAM per GPU
  - psutil → RAM, CPU cores
  - Profile matching: Machine-A vs Machine-B
  - Save to hardware_profile.json

□ forge.py init
  - Create all USB directories (as per USB_Directory_Structure.md)
  - Initialize state.yaml (as per Data_Models.md)
  - Create 00_MANIFEST.json
  - Verify directory structure matches spec
```

### Day 4-5: Dashboard Shell
```
□ Tauri scaffold
  - npm create tauri-app@latest StydeForge -- --template vanilla
  - cargo build → verify .exe launches

□ Layout implementation
  - CSS Grid: 3 panels (30/35/35)
  - Dark theme CSS variables (#1a1a2e, #2a2a4a, #e0e0e0)
  - Custom title bar with controls
  - Panel headers with icons
  - Resizable panels (CSS resize)
  - Responsive breakpoints (tab mode at <1100px)

□ Empty states
  - No agents: placeholder message
  - Empty chat: welcome message with capabilities
  - Forge stopped: status bar shows "● Stopped"
```

### Day 6-7: DeepSeek Provider + Basic Chat
```
□ Provider registry (TypeScript)
  - ProviderRegistry class
  - ModelProvider interface implementation

□ DeepSeek provider
  - API key from config.json
  - chat() method — fetch to https://api.deepseek.com/v1/chat/completions
  - chatStream() — SSE parsing
  - validateAPIKey() — light ping
  - listModels() — hardcoded for now (v4-pro, v4-flash)

□ Basic chat panel
  - Message list (user + assistant)
  - Input field
  - Send button
  - Streaming display (typewriter effect)
  - Markdown rendering (marked.js)
  - Code syntax highlighting (highlight.js)

□ Config panel (basic)
  - config.json read/write
  - API key field (masked)
  - Model selector dropdown
```

---

## Week 2 — Spawn + Chat (Days 8-14)

### Day 8-9: Blueprint System
```
□ blueprint_loader.py
  - load_blueprint_context(name) → spawn_context dict
  - Read persona.md, BLUEPRINT.md, config.yaml, skills/
  - Build context string for delegate_task
  - Inject Caveman Ultra rules if enabled

□ blueprint_valid.py
  - validate_blueprint(name) → bool
  - Check required files exist
  - Validate config.yaml schema
  - Validate persona.md is non-empty
  - Report specific validation errors
```

### Day 10-11: Agent Spawning
```
□ spawn.py
  - spawn_agent(blueprint, benchmark) → agent_id
  - Load blueprint context
  - Load benchmark task + rubric
  - Build delegate_task call
  - Handle timeout (300s default)
  - Handle API errors (retry with backoff)
  - Capture output to output.md

□ Manual test
  - python forge.py spawn code-reviewer code-review-basic
  - Verify agent output saved
  - Verify agent appears in state.yaml
```

### Day 12-14: Chat Enhancement
```
□ Chat tool: read_file
  - Tauri Rust command: read_file(path) → content
  - UI: show file path + content in chat
  - Path allowlisting enforcement

□ Chat tool: write_file
  - Tauri Rust command: write_file(path, content)
  - UI: confirmation dialog with diff preview
  - Path allowlisting enforcement

□ Chat tool: search_files
  - Tauri Rust command: search_files(pattern, path)
  - UI: show results in chat

□ Skill command system
  - Parse /skill:name in chat input
  - Load skill from Hermes skills directory
  - Inject into next chat message context
```

---

## Week 3 — Eval Pipeline (Days 15-21)

### Day 15-16: Self-Evaluation
```
□ eval_runner.py — run_self_eval(agent_id, benchmark)
  - Load agent output from output.md
  - Load benchmark rubric
  - Spawn agent with self-eval prompt:
    "Evaluate your output against rubric. Return YAML: {score: N, dimensions: {...}, notes: '...'}"
  - Parse self-eval YAML
  - Save to self_eval.yaml

□ Error handling
  - Agent didn't include self-eval → score=0
  - Unparseable self-eval → score=0, flag for review
  - Agent timeout during self-eval → score=0
```

### Day 17-18: Judge Evaluation
```
□ eval_runner.py — run_judge_eval(agent_id, benchmark)
  - Fresh delegate_task with ONLY:
    - Agent output
    - Rubric
    - Scoring instructions
  - No blueprint context, no persona
  - Model: deepseek-v4-pro, temperature=0.1
  - Parse judge YAML output
  - Save to judge_eval.yaml

□ Composite scoring
  - composite_score = self_eval × 0.3 + judge_eval × 0.5 + consensus × 0.2
  - Phase 1: consensus = 0 (no multi-judge yet)
  - So: composite = self × 0.4 + judge × 0.6
  - passed = composite >= 70
  - Save to eval.yaml

□ forge.py eval CLI
  - python forge.py eval <agent_id> <benchmark>
  - Runs self-eval + judge-eval + composite
  - Prints result table
```

### Day 19-21: Dashboard Agent Panel
```
□ Hermes CLI bridge (Rust)
  - hermes process list → parse output
  - hermes cronjob list → parse output
  - hermes status → get system info
  - Poll every 5 seconds

□ Agent panel UI
  - Agent cards: name, status, model, score
  - Status indicators: ● running, ✓ done, ✗ failed
  - Click → detail view (token count, cost, duration)
  - Empty state: "No agents active"

□ Status bar
  - ●/○ status indicator
  - Agent count
  - Token count (from Hermes CLI)
  - Cost estimate (tokens × rate)
```

---

## Week 4 — Improvement + Control (Days 22-28)

### Day 22-23: Teacher Agent
```
□ teacher.py
  - analyze_eval(agent_id, blueprint) → teacher_review
  - delegate_task with:
    - Eval results (self + judge)
    - Previous evaluations (last 3)
    - Teacher prompt template (from Teacher_Agent.md)
  - Teacher diagnoses root causes
  - Proposes concrete improvements
  - Extracts patterns if score ≥ 85
  - Output: teacher_review.yaml

□ forge.py improve CLI
  - python forge.py improve <blueprint>
  - Calls teacher
  - Applies improvements to blueprint
  - Promotes/retries/archives agent based on score
```

### Day 24-25: Checkpoint System
```
□ checkpoint.py
  - create_checkpoint() → checkpoint_id
  - Lock state.yaml
  - Copy state to checkpoints/checkpoint-YYYYMMDD-HHMMSS/
  - Verify integrity (file count + size check)
  - Atomic rename staging → checkpoint
  - Update state.yaml → last_checkpoint
  - Increment loop_iterations

□ forge.py checkpoint CLI
  - python forge.py checkpoint
  - Creates checkpoint
  - Prints summary
```

### Day 26-28: Dashboard System Control
```
□ Start/Stop buttons
  - ▶ Start: Spawns Hermes + Forge loop as child process
    - Tauri Rust: std::process::Command::new("python").arg("forge.py").arg("loop")...
    - Track process handle
  - ⏸ Pause: Send SIGINT / graceful stop
    - Save checkpoint before stopping
    - Stop cron jobs
  - ⏹ Stop: Kill process + checkpoint

□ System tray
  - Minimize to tray
  - Tray icon with status color
  - Right-click menu: Show/Hide, Start/Stop, Exit
  - Notification on agent completion/failure

□ Configuration panel
  - config.json editor UI
  - Model selection
  - Provider management (add/remove)
  - Path configuration
  - Save + apply without restart
```

---

## Week 5 — Integration & Testing (Days 29-35)

### Day 29-30: Forge↔Dashboard Bridge
```
□ Bridge implementation
  - Dashboard Start button → spawns forge.py loop
  - Dashboard polls Hermes CLI for agent status
  - Dashboard Stop button → graceful shutdown + checkpoint
  - Forge output visible in agent panel
  - Forge errors visible in dashboard

□ End-to-end test
  - Click Start in dashboard
  - Forge loop runs: code-reviewer vs code-review-basic
  - Agents appear in panel
  - Scores update
  - Checkpoint created
  - Click Stop → graceful shutdown
```

### Day 31-33: Bug Fixes & Edge Cases
```
□ Test scenarios:
  - USB disconnect during checkpoint
  - API rate limit hit (429)
  - Agent timeout
  - Dashboard closed during Forge loop
  - Multiple agents running
  - No GPU detected (fallback)
  - Missing blueprint
  - Invalid config

□ Fixes:
  - Based on real testing
  - Edge case handling
  - Error messages
  - Logging
```

### Day 34-35: P0 Exit Criteria Verification
```
□ Forge exit criteria (12 items)
□ Dashboard exit criteria (10 items)
□ Document results
□ Fix remaining issues
```

---

## Week 6 — Hardening (Days 36-42)

### Day 36-37: Recovery System
```
□ recovery.py
  - detect_crash() → bool
    - Check lock file exists but process dead
    - Check state.yaml consistency
  - restore_from_checkpoint() → bool
    - Find latest valid checkpoint
    - Restore state
    - Verify integrity
    - Log recovery event
```

### Day 38-39: Circuit Breaker
```
□ circuit_breaker.py
  - CircuitBreaker class
  - Per-blueprint breakers
  - Global breaker
  - State transitions: closed → open → half_open → closed

□ Triggers:
  - 3 consecutive eval < 70 → blueprint breaker open
  - 5 API errors in 10 min → global breaker open
  - delegate_task timeout 3× → blueprint breaker open
```

### Day 40-42: Final Polish
```
□ Second blueprint: research-synthesizer
  - Bring online
  - Test eval loop
  - Verify quality gate

□ Documentation
  - README updates
  - Run instructions
  - Troubleshooting guide

□ Performance
  - Profile loop speed
  - Optimize slow components
  - Token cost audit

□ Handoff
  - Pontus review
  - Final adjustments
  - Phase 1 complete declaration
```

---

## Milestone Summary

| Milestone | End of Week | Success Criterion |
|-----------|------------|-------------------|
| **M1: Foundation** | Week 1 | USB structure + Tauri app launches |
| **M2: First Spawn** | Week 2 | code-reviewer agent spawned via Forge |
| **M3: First Eval** | Week 3 | Self-eval + judge-eval works end-to-end |
| **M4: First Complete Loop** | Week 4 | DEFINE→SPAWN→EVAL→IMPROVE→CHECKPOINT |
| **M5: Dashboard MVP** | Week 5 | Chat + agent panel + start/stop works |
| **M6: Phase 1 Complete** | Week 6 | All 22 P0 exit criteria met |

---

## Risk Timeline

| Week | Risk | Mitigation |
|------|------|------------|
| 1 | WebView2 not installed | Bundle bootstrapper, fallback to CLI |
| 1 | Tauri CLI install fails | Use npm create tauri-app alternative |
| 2 | delegate_task doesn't work as expected | Test manually Day 1, adapt spawn.py |
| 3 | Judge eval inconsistent | Temperature=0.1, structured YAML output |
| 4 | Teacher doesn't produce actionable feedback | Tight prompt template, structured output req |
| 5 | Integration bugs | Test early, test often. Don't wait for Week 5 |
| 6 | Scope creep (adding Phase 2 features) | Strict P0-only. New ideas → Phase 2 backlog |

---

**Status:** Plan defined. 6 weeks, 6 milestones, 22 exit criteria.
