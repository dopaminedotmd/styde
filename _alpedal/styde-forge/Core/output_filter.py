"""
Output Quality Pre-Filter — catch obviously bad spawns before expensive eval.

Cheap heuristics that run in <10ms to detect:
- Empty/near-empty output
- Obvious errors ("I cannot", "I'm unable", tracebacks)
- Markdown violations in caveman mode
- Refusal patterns ("I'll help", "Let me know", no actual output)
- Repetition / loop traps

Returns {pass: bool, reason: str, score_estimate: int}
"""
import re
from pathlib import Path

# Patterns that indicate a FAILED spawn (score likely < 30)
FAIL_PATTERNS = [
    (r"^\s*$", "empty output"),
    (r"^(OK|ok|done|yes|no)\s*$", "single-word output"),
    (r"I('m|\s+am)\s+(sorry|unable|not able|cannot|can't)\s", "refusal pattern"),
    (r"I\s+(will|could|would|can)\s+help", "help-offer pattern (no output)"),
    (r"Let\s+me\s+know\s+if", "sign-off pattern"),
    (r"Traceback\s*\(most recent", "Python traceback in output"),
    (r"Error:\s*(cannot|unable|failed|timeout)", "error message as output"),
    (r"Here\s+is\s+(the|your|a)\s+(code|output|result|file)s*\s*:", "preamble without content"),
    (r"^\s*#\s", "markdown heading in caveman mode"),
    (r"^\s*\*\*", "markdown bold in caveman mode"),
]

# Patterns indicating WEAK spawn (score likely < 50)
WEAK_PATTERNS = [
    (r"^\s*#{1,3}\s", "markdown heading"),
    (r"```[\w]*\s*\n", "code fence"),
    (r"^\s*[-*]\s", "markdown list"),
    (r"^\s*>\s", "blockquote"),
    (r"(perhaps|maybe|possibly|I think|in my opinion)", "hedging language"),
    (r"(Hope this helps|Let me know|Feel free|Happy to)", "AI-isms"),
]

# Minimum output length by stage
MIN_OUTPUT_CHARS = 50
MIN_OUTPUT_LINES = 1


def filter_output(output: str, caveman: bool = True) -> dict:
    """Pre-filter agent output. Returns verdict dict.

    Returns:
        {pass: bool, reason: str, score_estimate: int}
        score_estimate: rough guess (0-100) to decide if eval is worth it
    """
    if not output or not output.strip():
        return {"pass": False, "reason": "completely empty output", "score_estimate": 0}

    text = output.strip()
    length = len(text)
    lines = text.count("\n") + 1

    # Too short
    if length < MIN_OUTPUT_CHARS:
        return {"pass": False, "reason": f"output too short ({length} chars)", "score_estimate": 10}
    if lines < MIN_OUTPUT_LINES:
        return {"pass": False, "reason": f"output too few lines ({lines})", "score_estimate": 15}

    # Check fail patterns
    for pattern, label in FAIL_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return {"pass": False, "reason": f"fail pattern: {label}", "score_estimate": 20}

    # Check weak patterns
    weak_hits = []
    for pattern, label in WEAK_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            weak_hits.append(label)

    if len(weak_hits) >= 3:
        return {"pass": False, "reason": f"multiple weak patterns: {', '.join(weak_hits[:3])}",
                "score_estimate": 35}
    elif len(weak_hits) >= 1:
        # Still pass, but flag as low quality
        return {"pass": True, "reason": f"weak: {weak_hits[0]}", "score_estimate": 55,
                "warnings": weak_hits}

    # Good output
    # Estimate score based on length and complexity
    if length > 2000:
        score_est = 80
    elif length > 500:
        score_est = 65
    else:
        score_est = 50

    return {"pass": True, "reason": "output looks valid", "score_estimate": score_est}
