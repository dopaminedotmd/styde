# Caveman Ultra Mode

**Styde Forge v3.0 — Phase 0**
**Section:** 10_Operations

---

## 1. Purpose

Caveman Ultra is the forge's **maximum-efficiency operating mode**.
No fluff. No markdown. No verbose explanations. Just data.

Every agent, every eval, every teacher response — stripped to essential
information only. Minimum tokens, maximum speed, zero waste.

---

## 2. Philosophy

```
MORE TOKENS ≠ MORE VALUE
LESS CONTEXT = FASTER INFERENCE = MORE ITERATIONS = BETTER AGENTS
```

| Principle | Rule |
|-----------|------|
| **No markdown** | Plain text only. No `#`, `**`, code fences unless code is the output |
| **No politeness** | Skip "Sure!", "Here is...", "I think..." — just the answer |
| **No repetition** | Say it once. Agent output is read by machines, not humans |
| **Data over prose** | YAML/JSON over paragraphs. Tables over descriptions |
| **One screen** | Output must fit in one terminal screen (no scrolling needed) |

---

## 3. Agent Persona Override

All blueprints inherit Caveman Ultra when the mode is active:

```yaml
caveman_ultra:
  enabled: true
  rules:
    - "No greetings, no sign-offs, no pleasantries"
    - "Output as YAML or plain text — never markdown"
    - "One line per finding. One word if one word is enough"
    - "Skip explanations unless confidence < 80%"
    - "If output is code: just the code. No 'Here is the code:'"
```

### Example: code-reviewer output

**Normal mode:**
```markdown
## Code Review: auth.py

### Critical Issues
- **Line 14**: SQL injection vulnerability in the login function.
  The f-string query allows an attacker to inject arbitrary SQL.
  **Fix**: Use parameterized queries with `?` placeholders.
```

**Caveman Ultra mode:**
```
auth.py
L14: SQL injection. f-string in query. Fix: parameterized queries.
L28: Hardcoded password "admin123". Fix: env var.
L30: Command injection in os.system. Fix: subprocess.run with list.
Score: 85
```

---

## 4. Eval Pipeline in Caveman Mode

| Layer | Normal | Caveman Ultra |
|-------|--------|---------------|
| Self-Eval | "I scored 85 because..." | `self:85 (L14 miss: -10, L30 found: +5)` |
| Judge-Eval | Full dimension breakdown | `judge:83 {c:90 r:75 q:85 e:80 i:82 d:88}` |
| Teacher | Detailed improvement plan | `fix: add edge case checklist. impact: high. skill: edge_cases_v1` |

---

## 5. Token Savings

| Output Type | Normal (~tokens) | Caveman (~tokens) | Savings |
|-------------|-----------------|-------------------|---------|
| Agent spawn (small task) | 800-1200 | 200-400 | 65% |
| Agent spawn (large task) | 2000-4000 | 600-1200 | 70% |
| Self-eval | 300-500 | 80-150 | 70% |
| Judge-eval | 500-800 | 150-250 | 68% |
| Teacher feedback | 600-1000 | 150-300 | 72% |

**Per iteration: ~5000 tokens → ~1500 tokens (70% reduction)**

---

## 6. Speed Impact

| Metric | Normal | Caveman Ultra | Gain |
|--------|--------|---------------|------|
| Tokens per agent spawn | 4000-8000 | 1200-2400 | 3× fewer |
| Time per agent spawn | 3-5 sec | 1-2 sec | 2-3× faster |
| Agent output parsing | Manual review needed | Machine-parseable | Instant |
| Total loop iteration | 5-8 min | 2-4 min | 2× faster |
| 100 agents (16 GB) | ~8 hours | ~3-4 hours | 2× faster |
| API cost (16 GB) | ~$0.24 | ~$0.08 | 3× cheaper |

---

## 7. When to Use

| Scenario | Mode |
|----------|------|
| Initial bootstrap (first 50 agents) | Caveman Ultra |
| Agent output IS the deliverable (code, config, test) | Caveman Ultra |
| Teacher analyzing eval patterns | Caveman Ultra |
| Human wants to read agent reasoning | Normal mode |
| Documentation agent (output IS markdown) | Normal mode |

**Default: Caveman Ultra ON. Toggle off only for human-readable output.**

---

## 8. Integration

- Toggle via `state.yaml → caveman_ultra: true`
- Agent context includes Caveman rules at spawn
- Eval pipeline strips markdown from all outputs
- Teacher feedback follows Caveman format
- All logs and eval results use minimal format

---

**Status:** Defined. Default operating mode for maximum efficiency.
