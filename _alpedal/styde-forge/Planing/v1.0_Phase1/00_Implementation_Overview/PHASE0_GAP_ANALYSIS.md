# Phase 0 → Phase 1 Gap Analysis

**Styde Forge v3.0 + StydeForge Dashboard**
**Section:** 00_Implementation_Overview
**References:** All 53+36 Phase 0 documents

---

## 1. Purpose

Phase 0 designed everything. But design documents aren't code. This document identifies every gap between "designed" and "implementable" — missing details, ambiguous decisions, and things Phase 0 assumed but didn't specify.

---

## 2. Critical Gaps — Forge

### GAP-F01: Hermes `delegate_task()` API Contract
**Phase 0 says:** "Call delegate_task with goal, context, toolsets"
**Reality:** What exact parameters does Hermes v0.17.0 accept? What's the timeout behavior? Can we capture output programmatically or only through file writes?
**Action needed:** Test `delegate_task` manually with a simple prompt first. Document exact parameter contract before building `spawn.py`.
**Risk:** HIGH — if delegate_task doesn't work as assumed, entire spawn pipeline needs redesign.

### GAP-F02: Agent Output Capture Method
**Phase 0 says:** "Subagent produces output → saved to output.md"
**Reality:** How does the Forge parent process actually capture subagent output? delegate_task returns a summary, not raw agent output. We need the raw output for eval.
**Decision needed:** 
- Option A: Subagent writes to a known file path (requires file tools)
- Option B: Parse delegate_task return value
- Option C: Subagent returns structured YAML that parent extracts
**Recommendation:** Option A — most reliable. Subagent gets `write_file` tool and writes to `StydeAgents/refinery/<name>/runs/<run-id>/output.md`.

### GAP-F03: Self-Eval Mechanism
**Phase 0 says:** "Agent self-evaluates against rubric"
**Reality:** Can a subagent evaluate its own output? It would need the rubric in context AND its own output. This is circular. Or does the parent simulate a self-eval by asking the agent to score itself?
**Decision needed:** 
- Option A: Include self-eval instruction in subagent's prompt ("After completing task, score yourself against this rubric...")
- Option B: Parent spawns a separate self-eval call with agent output + rubric
**Recommendation:** Option A for simplicity. Add to Caveman Ultra prompt: "After output, append: SELF_EVAL: score=<N> dimensions={d1:v1,d2:v2...}"

### GAP-F04: Judge-Eval — Same or Different Model Instance?
**Phase 0 says:** "Independent model evaluates agent output"
**Reality:** We use deepseek-v4-pro. Is the judge a separate delegate_task call? Same API key? How do we prevent the judge from being affected by the agent's context?
**Action needed:** Judge runs in a completely fresh delegate_task call with only agent output + rubric in context. No blueprint skills, no persona. Clean slate.
**Risk:** LOW — straightforward implementation.

### GAP-F05: Blueprint Validation Criteria
**Phase 0 says:** "validate_blueprint(name) — must pass"
**Reality:** What exactly constitutes a valid blueprint? Phase 0 defines the structure but not the validation rules.
**Spec needed:**
```python
def validate_blueprint(name: str) -> bool:
    # Required files:
    required = ["persona.md", "BLUEPRINT.md", "config.yaml"]
    # Config must have: blueprint.name, hardware_profiles, agent, eval
    # Persona must be non-empty
    # BLUEPRINT.md must contain "## Purpose" section
    # Skills directory optional but must have SKILL.md if exists
```

### GAP-F06: Historical Context — How Much?
**Phase 0 says:** "Get historical context from Historical Learning System"
**Reality:** Historical Learning is Phase 2. In Phase 1, what context do we provide?
**Decision:** Phase 1 uses simple file-based context: last 3 eval results for this blueprint, formatted as YAML. No SQLite. No pattern extraction. Keep it simple.

### GAP-F07: Checkpoint — What Exactly Gets Saved?
**Phase 0 says:** "Copy all state to checkpoints/checkpoint-YYYYMMDD-HHMMSS/"
**Reality:** "All state" is vague. Which files? Entire USB? Just state.yaml + agents?
**Spec needed:**
```
Checkpoint includes:
- state.yaml
- All blueprint files (blueprints/<name>/*)
- All agent files in refinery/ and production/
- Latest evals (evals/ directory)
- Logs (since last checkpoint)
- hardware_profile.json
- cost_summary.json
Excludes:
- checkpoints/ directory (don't nest)
- 01_KNOWLEDGE/ (too large, reconstructed)
- archive/ (read-only, never changes)
```

### GAP-F08: RAG Initialization
**Phase 0 says:** "FAISS + all-MiniLM-L6-v2 on RTX 3080"
**Reality:** When is the index built? At init? On first spawn? What if 3080 is in use?
**Decision:** 
- Build index at `forge.py init` time (or `forge.py rag build`)
- If 3080 unavailable, skip RAG (graceful degradation)
- Rebuild index when new knowledge is added
- Store FAISS index on USB: `99_INDEXES/faiss_index.bin`

---

## 3. Critical Gaps — Dashboard

### GAP-D01: WebView2 Availability
**Phase 0 says:** "Tauri v2 with WebView2 on Windows"
**Reality:** Is WebView2 installed on Machine-B? What if not?
**Action needed:** Check `Get-ItemProperty "HKLM:\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"` in PowerShell. Bundle WebView2 bootstrapper if missing.
**Risk:** MEDIUM — without WebView2, Tauri app shows blank window.

### GAP-D02: Hermes CLI Output Parsing
**Phase 0 says:** "Call hermes process list, parse output"
**Reality:** Hermes CLI output format may change between versions. Is there a `--json` flag?
**Action needed:** Test `hermes process list --json` or `hermes --json process list`. If no JSON flag exists, parse text output with regex (fragile).
**Risk:** MEDIUM — text parsing breaks on Hermes updates.

### GAP-D03: Provider API Key Storage
**Phase 0 says:** "Encrypted local storage (OS keychain)"
**Reality:** Tauri has `tauri-plugin-store` for secure storage. But setup complexity is non-trivial.
**Decision:** Phase 1 uses plain config.json (local machine, no remote access). Phase 2 adds OS keychain. Accept the risk for MVP.

### GAP-D04: Chat Tool Execution Security
**Phase 0 says:** "Confirmation dialog for all commands"
**Reality:** When chat's AI requests `write_file("C:/critical/system32/...")`, we need more than a confirmation dialog. We need path allowlisting.
**Spec needed:**
```
Allowed paths for write_file:
- D:\* (project files)
- C:\Users\Pontus\.hermes\* (Hermes config)
- Any path under USB drive
- Explicit deny: C:\Windows*, C:\Program Files*, C:\*
```

### GAP-D05: Real-Time Agent Updates
**Phase 0 says:** "Poll every 2 seconds"
**Reality:** Is 2s too aggressive? What if Hermes has 100+ agents?
**Decision:** Phase 1 polls every 5s. Virtual scroll for >20 agents. Delta updates (only send changed agents). Phase 2 adds WebSocket if possible.

---

## 4. Assumptions to Validate

| # | Assumption | Validation Method | Risk |
|---|-----------|-------------------|------|
| A1 | Hermes v0.17.0+ installed and working | `hermes --version` | LOW |
| A2 | DeepSeek API key configured | `hermes config get providers.deepseek.api_key` | LOW |
| A3 | Python 3.11+ with psutil, torch, faiss available | `python -c "import psutil, torch, faiss"` | MEDIUM |
| A4 | RTX 3080 accessible (CUDA) | `python -c "import torch; print(torch.cuda.is_available())"` | LOW |
| A5 | GPU enum quirk documented (dev0=3080, dev1=3070Ti) | Already known from memory | LOW |
| A6 | USB drive at D:\ (48 GB) writable | `test -w /d/` | LOW |
| A7 | Node.js 20+ and Rust installed | `node --version && rustc --version` | MEDIUM |
| A8 | Tauri CLI installable | `cargo install tauri-cli --version "^2"` | MEDIUM |
| A9 | WebView2 available on Windows | PowerShell registry check | MEDIUM |
| A10 | Hermes CLI supports --json output | `hermes process list --json 2>&1` | MEDIUM |

---

## 5. Design Decisions Needed Before Code

These are questions Phase 0 didn't answer that need decisions NOW:

| # | Question | Options | Recommendation |
|---|----------|---------|----------------|
| Q1 | Self-eval: inline or separate call? | Inline in agent prompt vs separate delegate_task | **Inline** — simpler, fewer API calls |
| Q2 | Judge model: exact prompt template? | Use Teacher prompt template adapted for judging | Use Core_Loop_Detail.md §3b template |
| Q3 | Blueprints: 6 Phase 0 or 20 Top 20 Agents? | Start with 6 core, add Top 20 later | **6 core first** (proven in Phase 0), then Tier 1 agents |
| Q4 | Dashboard: Tauri sidecar or pure Tauri? | Python sidecar vs pure Rust backend | **Pure Tauri** — Rust for Hermes CLI is simple enough |
| Q5 | Checkpoint frequency? | Every loop vs every N loops vs time-based | **Every 5 loops** (configurable) |
| Q6 | Retry strategy for failed spawns? | 3 retries with backoff vs 1 retry vs none | **3 retries** with 5s/10s/20s backoff |

---

## 6. Things Phase 0 Got Right (No Gaps)

These are solid — implement directly from Phase 0 docs:

- ✅ USB directory structure — exactly specified
- ✅ Data models — all YAML/JSON schemas complete
- ✅ State machines — all states and transitions defined
- ✅ Component interfaces — inputs/outputs specified
- ✅ Hardware profiles — Machine-A and Machine-B detailed
- ✅ Caveman Ultra rules — exact tokens to inject
- ✅ Dashboard layout — CSS Grid with exact dimensions
- ✅ Provider architecture — TypeScript interfaces complete
- ✅ Atomic write pattern — temp-file + rename is standard
- ✅ Circuit breaker — states and thresholds defined

---

## 7. Summary

| Category | Items | Status |
|----------|-------|--------|
| Critical Forge gaps | 8 | Need decisions before code |
| Critical Dashboard gaps | 5 | Need validation before code |
| Assumptions to validate | 10 | Day 1 checks |
| Design decisions pending | 6 | Decide before building |
| Solid (no gaps) | 10 | Ready for code |

**Bottom line:** Phase 0 is 80% code-ready. The remaining 20% is mostly API contract validation (delegate_task behavior, Hermes CLI output format) and a few design decisions that need explicit answers. These don't block starting — they get resolved during the first few days of implementation.

---

**Status:** Gap analysis complete. Resolve Q1-Q6 and validate A1-A10 on Day 1.
