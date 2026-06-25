# P0 Exit Criteria — Phase 1 Complete

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 08_Integration
**References:** `Phase0_to_Phase1_Transition.md` §1, Dashboard `Phase0_to_Phase1.md` §6

---

## 1. Forge Exit Criteria (12 items)

### Core Loop
- [ ] **F1:** `forge.py init` creates complete USB directory structure matching `USB_Directory_Structure.md`
- [ ] **F2:** Hardware detection works — `detect.py` produces valid `hardware_profile.json` via nvidia-smi
- [ ] **F3:** Blueprint loading validates and builds spawn context — `validate_blueprint()` identifies all required files
- [ ] **F4:** `forge.py spawn` successfully calls `delegate_task` — agent produces output to `output.md`

### Evaluation
- [ ] **F5:** Self-eval runs against rubric — produces valid YAML with score + dimensions
- [ ] **F6:** Judge-eval runs (deepseek-v4-pro, temp=0.1) — produces valid YAML independent of self-eval
- [ ] **F7:** Composite scoring weights correctly (self × 0.4 + judge × 0.6 in Phase 1)

### Improvement
- [ ] **F8:** Teacher analyzes eval — produces actionable improvement proposals
- [ ] **F9:** code-reviewer completes 10 loop iterations with improving scores
- [ ] **F10:** At least one agent reaches ≥ 85/100 composite score

### Safety
- [ ] **F11:** Checkpoint → crash → recovery works without data loss (test: force-kill during checkpoint, verify restore)
- [ ] **F12:** Atomic writes guarantee no partial files (test: disconnect USB during write, verify file integrity)

---

## 2. Dashboard Exit Criteria (10 items)

### Shell
- [ ] **D1:** `StydeForge.exe` launches on Windows via double-click (< 3 seconds to functional window)
- [ ] **D2:** Dark theme with 3 resizable panels displayed (CSS Grid, 30/35/35 split)
- [ ] **D3:** Custom title bar with window controls (minimize, maximize, close)

### Chat
- [ ] **D4:** Chat works with DeepSeek — streaming, first token < 2 seconds
- [ ] **D5:** Chat can read files — `read_file("D:/test.txt")` returns content
- [ ] **D6:** Chat can write files — `write_file(...)` with confirmation dialog

### Monitor & Control
- [ ] **D7:** Agent panel shows active agents from Hermes CLI (polls every 5s, updates within 5s of status change)
- [ ] **D8:** Start button spawns Forge process; Stop button gracefully shuts down with checkpoint

### Polish
- [ ] **D9:** App minimizes to system tray; tray icon shows status color
- [ ] **D10:** Configuration saves and loads — `config.json` persists provider + appearance settings

---

## 3. Integration Test Scenarios

### Test 1: Happy Path — One Complete Loop
```
1. Start StydeForge.exe
2. Configure DeepSeek provider (API key)
3. Press Start → Forge loop begins
4. code-reviewer agent spawned → appears in agent panel
5. Agent completes → status changes to "eval_pending"
6. Eval runs → score appears in agent detail
7. Teacher improves blueprint → version increments
8. Checkpoint created
9. After 10 iterations: agent reaches ≥ 85
10. Press Stop → graceful shutdown
```

### Test 2: Crash Recovery
```
1. Start Forge loop
2. Force-kill forge.py process mid-checkpoint
3. Restart forge.py
4. Verify: latest valid checkpoint restored
5. Verify: no partial/corrupted files
6. Verify: loop resumes from last checkpoint
```

### Test 3: USB Resilience
```
1. Run Forge from USB drive
2. Start loop
3. Physically disconnect USB during write
4. Reconnect USB
5. Verify: all files intact (old state preserved)
6. Verify: recovery log shows disconnect event
```

---

## 4. Performance Benchmarks

| Metric | Target | Measurement |
|--------|--------|-------------|
| Forge loop iteration (end-to-end) | < 60 seconds | `time python forge.py loop code-reviewer code-review-basic` |
| Agent spawn time | < 10 seconds | delegate_task call to output saved |
| Eval time (self + judge) | < 30 seconds | Both evals complete |
| Checkpoint time | < 5 seconds | Full state snapshot |
| Dashboard startup | < 3 seconds | Double-click to interactive |
| Dashboard memory (idle) | < 150 MB | Task Manager |
| `.exe` size | < 80 MB | `ls -lh StydeForge.exe` |
| Chat first token | < 2 seconds | DeepSeek streaming |

---

## 5. Sign-Off Checklist

Before declaring Phase 1 complete:

- [ ] All 12 Forge exit criteria met and verified
- [ ] All 10 Dashboard exit criteria met and verified
- [ ] All 3 integration tests pass
- [ ] All performance benchmarks within targets
- [ ] Pontus has reviewed and approved
- [ ] `state.yaml` shows `forge_version: "3.0.0"` and `loop_iterations > 0`
- [ ] At least one agent in `StydeAgents/production/`
- [ ] README updated with run instructions
- [ ] Known issues documented

---

## 6. Declaration

```
Phase 1 is complete when:

  An agent was spawned from a blueprint.
  It was evaluated against a benchmark.
  A teacher improved the blueprint.
  A checkpoint was created and recovered from.
  The dashboard monitored the entire process.
  It worked on both Machine-A and Machine-B.
  The USB was unplugged and replugged without data loss.
```

---

**Status:** Criteria defined. Check each box before declaring Phase 1 done.
