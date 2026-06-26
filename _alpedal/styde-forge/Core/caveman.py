"""
Caveman Ultra — maximum-efficiency operating mode.

No markdown. No fluff. No pleasantries. Just data.
70% fewer tokens, 2× faster, 3× cheaper.

Toggle via state.yaml → caveman_ultra: true|false
Injected into every agent spawn context.
"""
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent

# === Core rules injected into agent context ===

CAVEMAN_RULES = """\
CAVEMAN ULTRA MODE — MANDATORY OUTPUT FORMAT:

DO NOT output markdown. EVER. No # headings, no **bold**, no `code fences`,
no bullet lists with -, no numbered lists, no --- separators, no > blockquotes.
Plain text and YAML only. YAML for structured data, plain text for everything else.

DO NOT include any of these:
- Greetings (no "Hello", "Sure!", "Here is", "I think", "Let me")
- Sign-offs (no "Hope this helps", "Let me know if...")
- Explanations unless confidence < 80%
- Filler words (no "perhaps", "maybe", "just", "simply", "basically")
- Code fences or markdown formatting

DO:
- Start directly with the answer
- One line per finding. One word if one word is enough
- Use YAML for structured data: `key: value`
- Output pure result — skip the wrapping paper
- If output is code: just the code, no "Here is the code:"
- Fit output in one terminal screen when possible

FORMAT VIOLATIONS WILL CAUSE THE AGENT TO BE REJECTED.
"""

# Minimal rules variant for very tight token budgets
CAVEMAN_RULES_MINIMAL = (
    "CAVEMAN ULTRA: No markdown. No fluff. Plain text or YAML only. "
    "One line per finding. Start directly with the answer."
)

# === Eval-specific rules ===

CAVEMAN_EVAL_RULES = """\
CAVEMAN EVAL MODE — OUTPUT ONLY THIS YAML:

score: <0-100>
dimensions:
  accuracy: <0-100>
  clarity: <0-100>
  completeness: <0-100>
  efficiency: <0-100>
  usefulness: <0-100>
strengths: <one line>
weaknesses: <one line>

No other text. No markdown. No explanation.
"""

# === Teacher-specific rules ===

CAVEMAN_TEACHER_RULES = """\
CAVEMAN TEACHER MODE — OUTPUT ONLY THIS YAML:

diagnosis:
  weakest_dimension: <name>
  root_cause: <one line>
improvements:
  - target: <what to change>
    change: <what to do>
    reason: <why>
    expected_impact: <low|medium|high>
summary: <one line>
retry_recommended: <true|false>

No other text. No markdown. No explanation.
"""


def is_enabled() -> bool:
    """Check if Caveman Ultra is active in state.yaml."""
    from Core.state import load_state
    try:
        return load_state().get("caveman_ultra", True)
    except FileNotFoundError:
        return True  # default ON


def toggle(enable: bool | None = None) -> bool:
    """Toggle or query Caveman mode. Returns current state."""
    from Core.state import load_state, save_state
    state = load_state()
    if enable is not None:
        state["caveman_ultra"] = enable
        save_state(state)
    return state.get("caveman_ultra", True)


def inject(context: str, minimal: bool = False) -> str:
    """Inject Caveman Ultra rules into agent context. No-op if disabled."""
    if not is_enabled():
        return context
    rules = CAVEMAN_RULES_MINIMAL if minimal else CAVEMAN_RULES
    return f"{rules}\n\n{context}"


def inject_eval(prompt: str) -> str:
    """Inject Caveman eval rules. No-op if disabled."""
    if not is_enabled():
        return prompt
    return f"{CAVEMAN_EVAL_RULES}\n\n{prompt}"


def inject_teacher(prompt: str) -> str:
    """Inject Caveman teacher rules. No-op if disabled."""
    if not is_enabled():
        return prompt
    return f"{CAVEMAN_TEACHER_RULES}\n\n{prompt}"


def status_line() -> str:
    """Return a one-line status string."""
    return f"Caveman Ultra: {'ON' if is_enabled() else 'OFF'}"
