# Implementation Order — Dependency Graph

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 00_Implementation_Overview
**References:** `DECISIONS.md` D09 (sequential loop), `Core_Loop_Detail.md`

---

## 1. Dependency Graph

```
                    ┌─────────────────────┐
                    │   forge.py init     │  ← No dependencies
                    │   detect.py         │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ blueprint_loader.py │  ← Needs: USB dirs
                    │ blueprint_valid.py  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │    spawn.py         │  ← Needs: blueprint loaded
                    │    rag.py (optional)│
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │  eval_runner.py     │  ← Needs: agent output
                    │  composite_scorer.py│
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │   teacher.py        │  ← Needs: eval results
                    │   skill_extract.py  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ persistence.py      │  ← Used by ALL components
                    │ checkpoint.py       │
                    │ recovery.py         │
                    │ circuit_breaker.py  │
                    └─────────────────────┘

Dashboard (parallel track, minimal coupling):
                    ┌─────────────────────┐
                    │ Tauri scaffold       │  ← No dependencies
                    │ Layout + Theme       │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ DeepSeek provider    │  ← Needs: config.json
                    │ Chat panel           │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┘
                    │ Chat tools           │  ← Needs: providers working
                    │ (read/write/search)  │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │ Hermes CLI bridge    │  ← Needs: hermes installed
                    │ Agent panel          │
                    │ Start/Stop buttons   │
                    └─────────────────────┘

Integration (connects both):
    Forge ─── Hermes CLI bridge ─── Dashboard
    (scripts call hermes, dashboard polls hermes process list)
```

---

## 2. Build Sequence — Forge

### Phase A: Foundation (Day 1-2)
```
Priority 1 — Must exist before anything else:
  1. persistence.py  → atomic_write(), atomic_write_json(), atomic_append()
  2. detect.py       → nvidia-smi + psutil → hardware_profile.json
  3. forge.py init   → Create full USB directory structure
  4. state.yaml      → Initialize from Data_Models.md schema
```

### Phase B: Spawn Pipeline (Day 3-5)
```
Priority 2 — Core loop can't start without spawn:
  5. blueprint_loader.py → load_blueprint_context()
  6. blueprint_valid.py  → validate_blueprint()
  7. spawn.py            → spawn_agent() wrapping delegate_task
  8. rag.py              → Embed + FAISS + inject (optional, can add later)
```

### Phase C: Eval Pipeline (Day 6-8)
```
Priority 3 — Needs spawn output:
  9.  eval_runner.py      → run_self_eval() + run_judge_eval()
  10. composite_scorer.py → calculate_composite()
  11. forge.py eval       → CLI: python forge.py eval <agent> <benchmark>
```

### Phase D: Improvement Loop (Day 9-11)
```
Priority 4 — Needs eval results:
  12. teacher.py           → analyze_eval(), propose_improvements()
  13. skill_extract.py     → extract_skill_from_success()
  14. forge.py improve     → CLI: python forge.py improve <blueprint>
```

### Phase E: Safety & Polish (Day 12-14)
```
Priority 5 — Production hardening:
  15. checkpoint.py        → create_checkpoint(), verify_integrity()
  16. recovery.py          → detect_crash(), restore_from_checkpoint()
  17. circuit_breaker.py   → CircuitBreaker class
  18. forge.py loop        → Full loop: python forge.py loop <blueprint> <benchmark>
```

---

## 3. Build Sequence — Dashboard

### Phase F: Shell (Day 1-4)
```
Priority 1 — Must exist before any UI:
  19. Tauri scaffold        → cargo + npm init
  20. Layout + Theme        → CSS Grid 3-panel + dark theme CSS variables
  21. Title bar             → Custom window chrome
```

### Phase G: Chat Core (Day 5-8)
```
Priority 2 — Chat is the primary interaction point:
  22. Provider registry     → TypeScript ProviderRegistry class
  23. DeepSeek provider     → Implements ModelProvider interface
  24. Chat panel            → Streaming messages + markdown rendering
  25. Config panel          → config.json CRUD
```

### Phase H: Chat Tools (Day 9-11)
```
Priority 3 — Chat needs tools to be useful:
  26. read_file tool        → Tauri filesystem → file content
  27. write_file tool       → Confirmation dialog → atomic write
  28. search_files tool     → ripgrep-style search
  29. Skill commands        → /skill:name → load + execute
```

### Phase I: Monitor & Control (Day 12-15)
```
Priority 4 — Needs Hermes CLI bridge:
  30. Hermes CLI bridge     → Rust Command: hermes process list, hermes cronjob list
  31. Agent panel           → Poll every 2s, render agent cards
  32. Start/Stop buttons    → Spawn/kill Hermes + Forge processes
  33. Status bar            → Live metrics from Hermes CLI
  34. System tray           → Minimize, notifications
```

---

## 4. Integration Day (Day 16-18)

```
Priority 6 — Wire everything together:
  35. Forge ↔ Dashboard bridge  → Dashboard starts Forge scripts via Hermes
  36. End-to-end test           → code-reviewer loop from dashboard Start button
  37. Bug fixes + polish        → Based on real usage
```

---

## 5. Parallel Work Strategy

Forge and Dashboard can be built in **parallel** — they share only the Hermes CLI bridge:

```
Week 1:  Forge Phase A+B (Foundation + Spawn)  ||  Dashboard Phase F (Shell)
Week 2:  Forge Phase C (Eval)                  ||  Dashboard Phase G (Chat Core)
Week 3:  Forge Phase D+E (Improve + Safety)   ||  Dashboard Phase H (Chat Tools)
Week 4:  Integration                           ||  Dashboard Phase I (Monitor)
```

---

## 6. Critical Path

The critical path is the one that blocks everything else:

```
forge.py init → blueprint_loader.py → spawn.py → eval_runner.py → teacher.py → checkpoint.py
                                                                                    ↓
                                                                           forge.py loop
                                                                                    ↓
                                                                     Dashboard Start/Stop
```

**If spawn doesn't work, eval can't run. If eval can't run, teacher can't improve. If teacher can't improve, there's no loop.**

---

## 7. Quick Wins (Do These First)

| # | Task | Time | Impact |
|---|------|------|--------|
| 1 | `persistence.py` | 2h | Every other component uses it |
| 2 | `detect.py` | 1h | Auto-adapt on any machine |
| 3 | `forge.py init` | 2h | Creates all directories |
| 4 | Tauri scaffold + layout | 4h | Visible progress instantly |
| 5 | DeepSeek provider | 3h | Chat works immediately |

**First day deliverables (8h):**
- [x] USB directory structure created
- [x] Hardware profile detected and saved
- [x] Tauri app launches with dark theme
- [ ] Chat with DeepSeek works (streaming)

---

**Status:** Build order defined. Follow this sequence.
