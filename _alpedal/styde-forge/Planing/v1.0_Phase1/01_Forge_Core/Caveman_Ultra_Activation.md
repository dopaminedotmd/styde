# Caveman Ultra Activation

**Styde Forge v3.0**
**Section:** 01_Forge_Core
**References:** `Caveman_Ultra_Mode.md`, `DECISIONS.md` D05

---

## 1. Purpose

Caveman Ultra is Forge's maximum-efficiency mode. 70% fewer tokens, 2× faster, 3× cheaper. ON by default. Every agent spawn injects these rules.

---

## 2. Rules (injected into agent context)

```
CAVEMAN ULTRA MODE ACTIVE:
- No markdown. Plain text or YAML only.
- No greetings, no sign-offs, no pleasantries.
- One line per finding. One word if one word is enough.
- Skip explanations unless confidence < 80%.
- If output is code: just the code. No "Here is the code:".
- Output must fit in one terminal screen.
```

---

## 3. Implementation

```python
# Core/caveman.py (or inline in spawn.py)

CAVEMAN_RULES = """
CAVEMAN ULTRA MODE ACTIVE:
- No markdown. Plain text or YAML only.
- No greetings, no sign-offs, no pleasantries.
- One line per finding. One word if one word is enough.
- Skip explanations unless confidence < 80%.
- If output is code: just the code. No "Here is the code:".
"""

def is_caveman_enabled() -> bool:
    """Check state.yaml for caveman_ultra toggle."""
    from state import load_state
    return load_state().get("caveman_ultra", True)

def inject_caveman(context: str) -> str:
    """Inject Caveman Ultra rules into agent context."""
    if is_caveman_enabled():
        return CAVEMAN_RULES + "\n" + context
    return context

def toggle_caveman(enable: bool = None) -> bool:
    """Toggle or query Caveman mode."""
    from state import load_state, save_state
    state = load_state()
    if enable is not None:
        state["caveman_ultra"] = enable
        save_state(state)
    return state.get("caveman_ultra", True)
```

---

## 4. Token Savings

| Output | Normal | Caveman | Savings |
|--------|--------|---------|---------|
| Agent spawn | 4000-8000 | 1200-2400 | 70% |
| Self-eval | 300-500 | 80-150 | 70% |
| Judge-eval | 500-800 | 150-250 | 68% |
| Teacher | 600-1000 | 150-300 | 72% |
| **Per iteration** | **~5000** | **~1500** | **70%** |

Combined with RAG: ~90% reduction (8000→800 tokens).

---

## 5. When to Toggle OFF

Only disable for human-readable output:
- Documentation agent (output IS markdown)
- Debugging (need verbose agent reasoning)
- First-run verification (confirm agent understands task)

**Default: ON. Toggle: `python forge.py config set caveman_ultra false`**

---

**Status:** Specification complete.
