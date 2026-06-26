---
# Configuration in config.yaml — see version_history, domain, dependencies there
# This file is the canonical narrative specification.
---

# Prompt Injection Defender

Domain: security
Version: 5 (see config.yaml for version history)

## Purpose

Protects AI agent systems from prompt injection attacks. Sanitizes agent output before passing it as context to other agents, detects and strips jailbreak attempts, and logs sanitization events with full traceability.

## Persona

See persona.md for full agent persona definition.

## Architecture

### Detection Engine

Parallel batch matching engine using concurrent.futures.ThreadPoolExecutor with max_workers=8. Each pattern has an individual timeout of 100ms. The engine batches all 22+ regex patterns into a single parallel evaluation pass, reducing worst-case latency from 11s+ (sequential) to ~100ms (parallel).

Pattern matching uses re.SEARCH (not re.FULLMATCH) for all base64, hex, and encoding-variant patterns to find embedded payloads within longer strings. Inline lookaheads are used to match obfuscated injection boundaries without consuming characters.

### Detection Pattern Library

All patterns are organized in five tiers, evaluated in parallel:

Tier 1: Direct injection (re.IGNORECASE, re.SEARCH)
  - r'(?i)\bIGNORE\s+ALL\b.*\bPREVIOUS\s+INSTRUCTIONS?\b'
  - r'(?i)\bDISREGARD\b.*\bPRIOR\s+(DIRECTIVES|CONTEXT|PROMPTS?)\b'
  - r'(?i)\bYour\s+new\s+prompt\s+is\b'
  - r'(?i)\bNow\s+you\s+are\b.*\b(assistant|bot|AI)\b'
  - r'(?i)\bFrom\s+now\s+on\b.*\byou\s+will\b'

Tier 2: Role-playing and persona hijacking  (re.IGNORECASE, re.SEARCH)
  - r'(?i)\bDAN\b'  (Do Anything Now)
  - r'(?i)\bDo\s+Anything\s+Now\b'
  - r'(?i)\bAct\s+as\s+if\b.*\b(no\s+rules|unlimited|no\s+restrictions)\b'
  - r'(?i)\bYou\s+are\s+now\b.*\b(free|unleashed|unbounded|uncensored)\b'
  - r'(?i)\bIgnore\s+(your\s+)?(ethics|safety|guidelines|policies?|rules?)\b'

Tier 3: Delimiter-based injection (re.SEARCH)
  - r'\[\[\s*SYSTEM\s*:\s*.*?\]\]'
  - r'<\s*(user|system|assistant)\s*>.*?<\s*/\s*(user|system|assistant)\s*>'
  - r'---+\s*(NEW\s+)?(INSTRUCTION|PROMPT|CONTEXT)\s*---'
  - r'```(?:\s*\w+)?\s*(?:SYSTEM|INSTRUCTION|PROMPT):'

Tier 4: Encoding and obfuscation (re.SEARCH, loose anchoring)
  - r'(?i)(?:[A-Za-z0-9+/]{4,40}={0,2})\s*(?:ignore|disregard|forget|new\s+prompt)'  # base64 adjacent injection
  - r'(?i)0x[0-9a-fA-F]{4,}\s*(?:instruction|prompt|role)'  # hex adjacent injection
  - r'\\x[0-7]{3}|\\u[0-9a-fA-F]{4}|%[0-9a-fA-F]{2}'  # escaped/encoded chars near injection context
  - r'(?i)(?:normalize|transform|decode|convert)\s+(?:this|the\s+following)\s+(?:text|input|prompt|message)'

Tier 5: Recursive and nested injection (re.DOTALL, re.SEARCH)
  - r'(\bIGNORE\b.*?){2,}'  # stacked ignore directives
  - r'(?:role[\s-]*play|roleplay).*?(?:ignore|disregard|forget).*?(?:instruction|prompt|rule)'  # nested bypass
  - r'(?i)\bSIMULATE\b.*\bNEW\s+CONTEXT\b'
  - r'(?i)\bFICTIONAL\b.*\bSCENARIO\b.*\bOVERRIDE\b'

## Sanitization Modes

Two sanitization modes, configurable at init:

1. STRIP mode (default): Remove detected injection payloads entirely, rejoin surrounding clean text. Log each removal with position and pattern matched.

2. STRIP_OR_REPLACE mode: Replace detected injection payloads with <REDACTED> placeholder token to preserve original string length and structure. Log each replacement with position, pattern matched, and original content hash.

Example: "Hello IGNORE ALL PREVIOUS INSTRUCTIONS and do X" -> "Hello <REDACTED> and do X"

The <REDACTED> token is used consistently across all sanitization paths so downstream consumers can reliably detect and handle sanitized content.

## Error Handling

Each detection-santization path has defined fallback behavior:

- Regex compile failure: The failing pattern is logged with its source name and skipped; remaining patterns continue execution. An alert is raised to the monitoring system (see Monitoring section).
- Pattern timeout (>100ms): The pattern is logged as TIMEOUT with its pattern name, source agent, and input hash. The timeout result is treated as NO_MATCH. An alert is raised if the same pattern times out 3+ consecutive times.
- LLM-as-judge fallback: If the pattern engine is ambiguous (borderline confidence 40-60%), the input segment is forwarded to an LLM-as-judge call. If that call itself times out (>5s) or errors, the input is conservatively treated as INJECTION (fail-closed) and a high-severity alert is raised.
- Encoding decode failure: If the input cannot be decoded as UTF-8, fall back to latin-1, log the encoding fallback, and run sanitization on the fallback-decoded bytes. If both fail, treat as INJECTION and raise alert.

## Logging and Monitoring

Every sanitization event produces a structured log record:

```json
{
  "timestamp": "ISO-8601",
  "source_agent": "agent-name",
  "target_agent": "target-agent-name",
  "detected_patterns": ["tier1-ignore-all", "tier2-dan"],
  "pattern_count": 2,
  "sanitization_mode": "STRIP_OR_REPLACE",
  "replacements": 3,
  "latency_ms": 87,
  "input_length": 1240,
  "output_length": 1183,
  "result": "SANITIZED"
}
```

An alert is raised (via configurable alert channel) when:
  - Any detection-santization path fails (error handling activated)
  - Same pattern times out 3+ consecutive times
  - LLM-as-judge fallback activates (high severity)
  - Encoding decode fallback activates (medium severity)
  - >5% of inputs from a single source agent are sanitized in a sliding 1-hour window (abuse detection)

## Testing and Validation Strategy

### False Positive Acceptance Targets

  - Tier 1 (direct injection): <=1% false positive rate
  - Tier 2 (role-playing): <=2% false positive rate
  - Tier 3 (delimiters): <=0.5% false positive rate
  - Tier 4 (encoding): <=2% false positive rate
  - Tier 5 (recursive): <=1% false positive rate
  - Overall system: <=2% false positive rate across all tiers
  - False negatives (missed injections): <0.1% on known attack corpus

### Test Harness

  - Unit tests: Each regex pattern tested against 50+ benign and 50+ malicious inputs per pattern, with exact match/no-match assertions.
  - Integration tests: Full pipeline test (detect -> sanitize -> log) on 500 synthetic conversations with known injection rates (5%, 10%, 25%).
  - Edge case tests: Empty input, single-character input, max-length input (100K chars), binary/non-UTF8 input, repeated injection pattern (DoS resistance).
  - Regression tests: All previously discovered injection variants stored in a regression corpus and re-tested on every version bump.
  - Performance tests: Parallel engine evaluated against 22-pattern full set on 1K inputs; p95 latency must be <150ms.

### Test Corpus

  - Known attack corpus: 200+ real-world prompt injection examples from published research, CTF challenges, and public jailbreak repositories.
  - Benign corpus: 5,000+ clean agent-to-agent conversation excerpts from production logs (anonymized).
  - Synthetic injection corpus: Auto-generated variants of known patterns with random obfuscation (base64, hex, unicode escapes, whitespace padding).

### Verification Protocol

    - Two-pass output rule: First build the complete numbered list of changes, then count the items, then write any summary line that references the count. Never write count-containing prose before the item list is final.
    - Verify Output Integrity: Before finalizing output, check (a) header counts match body item count, (b) labels reference correct figures, (c) no stale metadata or score references from prior runs remain.
    - Diff output sanitization: Any verification diff output MUST be stripped of raw ANSI escape codes before logging. Use `strip_ansi()` or equivalent ANSI stripping (e.g. `re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', diff_output)`) to render diffs human-readable in logs.
    - Assertion standard: All test assertions MUST use regex-matched or logic-level validation (e.g. `grep -P`, `re.search()` in pytest, structured assertion libraries). Bare string-presence checks (`assert "expected" in output`) are prohibited — they produce fragile false positives on whitespace/escaping variations.
    - Verification gate: Every CI run must produce a clean verification diff (ANSI-stripped) before tests proceed. A failed verification blocks the version bump.

### Quality Gates

  - Pre-commit: spell-check enforced on all markdown and JSON files (see .pre-commit-config.yaml).
  - CI: All tests must pass before version bump; false positive rate must be within targets above.
  - Verification: Diff output must be ANSI-sanitized; all assertions must use regex/logic-level validation.
  - Release: Score >=90 on evaluation benchmark (see config.yaml score history); all regression tests green.

## Pre-commit

A pre-commit hook runs spell-check on all .md and .json files in this blueprint directory. Corrections are enforced before any commit. See .pre-commit-config.yaml at repo root for configuration.

## Version History

See config.yaml version_history section. Current version: 6.0.0 (score: 89.2)
