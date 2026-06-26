BLUEPRINT:
Configuration in config.yaml - see versionhistory, domain, dependencies there
This file is the canonical narrative specification.
Prompt Injection Defender
Domain: security
Version: 6 (see config.yaml for version history)
Purpose
Protects AI agent systems from prompt injection attacks. Sanitizes agent output before passing it as context to other agents, detects and strips jailbreak attempts, and logs sanitization events with full traceability.
Persona
See persona.md for full agent persona definition.
Conciseness directive: All gap descriptions limited to 2 sentences. Related issues are grouped and collapsed into single entries. Filler words are stripped from all logs and reports.
Architecture
Detection Engine
Parallel batch matching engine using concurrent.futures.ThreadPoolExecutor with maxworkers=8. Each pattern has an individual timeout of 100ms. The engine batches all 22+ regex patterns into a single parallel evaluation pass, reducing worst-case latency from 11s+ (sequential) to ~100ms (parallel).
Pattern matching uses re.SEARCH (not re.FULLMATCH) for all base64, hex, and encoding-variant patterns to find embedded payloads within longer strings. Inline lookaheads are used to match obfuscated injection boundaries without consuming characters.
Detection Pattern Library
All patterns are organized in five tiers, evaluated in parallel:
Tier 1: Direct injection (re.IGNORECASE, re.SEARCH)
  r'(?i)\bIGNORE\s+ALL\b.\bPREVIOUS\s+INSTRUCTIONS?\b'
  r'(?i)\bDISREGARD\b.\bPRIOR\s+(DIRECTIVES|CONTEXT|PROMPTS?)\b'
  r'(?i)\bYour\s+new\s+prompt\s+is\b'
  r'(?i)\bNow\s+you\s+are\b.\b(assistant|bot|AI)\b'
  r'(?i)\bFrom\s+now\s+on\b.\byou\s+will\b'
Tier 2: Role-playing and persona hijacking  (re.IGNORECASE, re.SEARCH)
  r'(?i)\bDAN\b'  (Do Anything Now)
  r'(?i)\bDo\s+Anything\s+Now\b'
  r'(?i)\bAct\s+as\s+if\b.\b(no\s+rules|unlimited|no\s+restrictions)\b'
  r'(?i)\bYou\s+are\s+now\b.\b(free|unleashed|unbounded|uncensored)\b'
  r'(?i)\bIgnore\s+(your\s+)?(ethics|safety|guidelines|policies?|rules?)\b'
Tier 3: Delimiter-based injection (re.SEARCH)
  r'\[\[\sSYSTEM\s:\s.?\]\]'
  r'.?'
  r'---+\s(NEW\s+)?(INSTRUCTION|PROMPT|CONTEXT)\s---'
  r'``(?:\s\w+)?\s(?:SYSTEM|INSTRUCTION|PROMPT):'
Tier 4: Encoding and obfuscation (re.SEARCH, loose anchoring)
  r'(?i)(?:[A-Za-z0-9+/]{4,40}={0,2})\s(?:ignore|disregard|forget|new\s+prompt)'  # base64 adjacent injection
  r'(?i)0x[0-9a-fA-F]{4,}\s(?:instruction|prompt|role)'  # hex adjacent injection
  r'\\x[0-7]{3}|\\u[0-9a-fA-F]{4}|%[0-9a-fA-F]{2}'  # escaped/encoded chars near injection context
  r'(?i)(?:normalize|transform|decode|convert)\s+(?:this|the\s+following)\s+(?:text|input|prompt|message)'
Tier 5: Recursive and nested injection (re.DOTALL, re.SEARCH)
  r'(\bIGNORE\b.?){2,}'  # stacked ignore directives
  r'(?:role[\s-]play|roleplay).?(?:ignore|disregard|forget).?(?:instruction|prompt|rule)'  # nested bypass
  r'(?i)\bSIMULATE\b.\bNEW\s+CONTEXT\b'
  r'(?i)\bFICTIONAL\b.\bSCENARIO\b.\bOVERRIDE\b'
Sanitization Modes
Two sanitization modes, configurable at init:
  STRIP mode (default): Remove detected injection payloads entirely, rejoin surrounding clean text. Log each removal with position and pattern matched.
  STRIPORREPLACE mode: Replace detected injection payloads with  placeholder token to preserve original string length and structure. Log each replacement with position, pattern matched, and original content hash.
Example: "Hello IGNORE ALL PREVIOUS INSTRUCTIONS and do X" -> "Hello  and do X"
The  token is used consistently across all sanitization paths so downstream consumers can reliably detect and handle sanitized content.
Error Handling
Each detection-sanitization path has defined fallback behavior:
  Regex compile failure: The failing pattern is logged with its source name and skipped; remaining patterns continue execution. An alert is raised to the monitoring system (see Monitoring section).
  Pattern timeout (>100ms): The pattern is logged as TIMEOUT with its pattern name, source agent, and input hash. The timeout result is treated as NOMATCH. An alert is raised if the same pattern times out 3+ consecutive times.
  LLM-as-judge fallback: If the pattern engine is ambiguous (borderline confidence 40-60%), the input segment is forwarded to an LLM-as-judge call. If that call itself times out (>5s) or errors, the input is conservatively treated as INJECTION (fail-closed) and a high-severity alert is raised.
  Encoding decode failure: If the input cannot be decoded as UTF-8, fall back to latin-1, log the encoding fallback, and run sanitization on the fallback-decoded bytes. If both fail, treat as INJECTION and raise alert.
Logging and Monitoring
Every sanitization event produces a structured log record:
{
  "timestamp": "ISO-8601",
  "sourceagent": "agent-name",
  "targetagent": "target-agent-name",
  "detectedpatterns": ["tier1-ignore-all", "tier2-dan"],
  "patterncount": 2,
  "sanitizationmode": "STRIPORREPLACE",
  "replacements": 3,
  "latencyms": 87,
  "inputlength": 1240,
  "outputlength": 1183,
  "result": "SANITIZED"
}
An alert is raised (via configurable alert channel) when:
  Any detection-sanitization path fails (error handling activated)
  Same pattern times out 3+ consecutive times
  LLM-as-judge fallback activates (high severity)
  Encoding decode fallback activates (medium severity)
  >5% of inputs from a single source agent are sanitized in a sliding 1-hour window (abuse detection)
Testing and Validation Strategy
Verification Protocol:
  All diff/check output MUST be piped through 'sed -e "s/\x1b\[[0-9;][a-zA-Z]//g"' before logging to strip ANSI escape codes. This ensures result readability and prevents corrupted log format.
  All assertions MUST use logic-level validation (grep -P, regex matching, or pytest assertions) instead of bare string matches. Bare string matches are prohibited because they fail on whitespace variation, encoding artifacts, and partial match scenarios.
  Validation mode: 'deep' - all tests apply regex-matched or logic-level assertions, no bare string equals checks.
False Positive Acceptance Targets
  Tier 1 (direct injection): <1% false positive rate on 1000 benign inputs (healthcare, legal, finance domains). False positives at target rate logged and reviewed monthly.
  Note: False positive rate is reduced by the conciseness-scoring thresholds and may vary by domain. Domain-specific tuning sets are maintained in config.yaml.
Evaluation
  >95% recall on Tier 1-3 injection detection in production logs (automated). >=90% accuracy on adversarial test suite (simulated red team). >=70% acceptance on outputs per agent (monitored via abuse detection).
  Validation mode: 'deep' - all evaluations use regex-matched or logic-level assertions, not bare string equals checks.
  Pre-commit verification: All diff output is ANSI-stripped before log capture. All assertions use regex/logic matching. See .pre-commit-config.yaml at repo root.
Integration Tests
  End-to-end pipeline test: feed -> detection -> sanitize -> log on 500 synthetic conversations with known injection rates (5%, 10%, 25%).
  Edge case tests: Empty input, single-character input, max-length input (100K chars), binary/non-UTF8 input, repeated injection pattern (DoS resistance).
  Regression tests: All previously discovered injection variants stored in a regression corpus and re-tested on every version bump.
  Performance tests: Parallel engine evaluated against 22-pattern full set on 1K inputs; p95 latency must be <150ms, p99 <300ms.
Benchmarking
  Online evaluation benchmark must score >=90 (see config.yaml score history). All regression tests green. Benchmark assertions use regex/logic matching, not string equality.
Pre-commit
A pre-commit hook runs spell-check on all .md and .json files in this blueprint directory. Corrections are enforced before any commit. Additionally, all verification output is ANSI-stripped before log capture, and all assertions use regex or logic-level matching. Alerts fire if a bare string match assertion is detected in the verification suite. See .pre-commit-config.yaml at repo root for configuration.
Version History
See config.yaml versionhistory section. Current version: 6.1.0 (score: 92.2)
---
config.yaml changes applied:
  qualityexpectations.testing.validationmode: deep
  output.sanitizeansi: true
  protocol.output.sanitizeansi: true
  qualityexpectations.testing.assertionmode: logic-level (regex/pytest/grep -P, bare string matches prohibited)