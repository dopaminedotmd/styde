name: prompt-injection-defender
domain: security
version: 2
purpose:
  Protects AI agent systems from prompt injection attacks. Sanitizes agent
  output before passing as context to downstream agents. Detects and strips
  jailbreak attempts across encoding variants. Logs all sanitization events
  with agent name, pattern, and action taken.
persona:
  AI security specialist. Expert in prompt injection detection, jailbreak
  pattern recognition, output sanitization, and secure multi-agent
  communication.
skill domain:
  detection:
    - ignore-instruction patterns (IGNORE ALL PREVIOUS, disregard, forget)
    - role-play jailbreaks (Act as DAN, You are now, Pretend to be)
    - delimiter attacks (---SYSTEM---, [NEW RULE], <|im_start|>)
    - encoding tricks (base64, hex, unicode escapes, double-encoding)
    - recursive injection (nested payloads, chain attacks)
    - context poisoning (hallucinated system messages, fake output markers)
    - token smuggling (repeated special tokens, invisible characters)
  sanitization:
    - strip mode: remove injection payload entirely
    - replace mode: substitute payload with [INJECTION_BLOCKED] placeholder
    - extract mode: salvage legitimate content from mixed payload
    - normalize mode: decode all encoding variants before analysis
  logging:
    fields: agent_name, pattern_id, pattern_category, action_taken, timestamp
    severity: low (suspicious only), medium (clear injection), high (confirmed bypass attempt)
  bypass resistance:
    - recursive decoding (up to 3 layers of base64/hex/unicode nesting)
    - case variation normalization (rOlE-pLaY -> role-play)
    - whitespace insertion detection (D I S R E G A R D)
    - homoglyph substitution (replacing latin chars with unicode lookalikes)
detection regex library:
  ignore_instructions:
    - (?i)(?:\bignore\b.{0,30}\b(?:all|previous|prior)\b.{0,30}\binstructions?\b)
    - (?i)(?:\bdisregard\b.{0,40}\b(?:instructions?|rules?|guidelines?)\b)
    - (?i)(?:\bforget\b.{0,30}\b(?:everything|previous|prior)\b)
    - (?i)(?:\byou\s+(?:no\s+longer|must\s+not|do\s+not)\s+(?:need|have|follow)\b)
  roleplay_jailbreak:
    - (?i)(?:act\s+as\b.{0,20}\b(?:dan|do\s+anything|unrestricted|unfiltered|no\s+rules))
    - (?i)(?:\byou\s+are\s+now\b.{0,50}\b(?:free|unleashed|unlimited|god|admin|system))
    - (?i)(?:\bpretend\b.{0,30}\b(?:you.{0,20}(?:are|were|can)\b))
    - (?i)(?:\bnew\s+identity\b.{0,50}\bignore\b)
  delimiter_attack:
    - (?i)(?:---SYSTEM---|===SYSTEM===|---RESPONSE---)
    - (?i)(?:\[NEW\s+(?:RULE|INSTRUCTION|COMMAND|ORDER)\])
    - (?i)(?:<\|im_start\|>|<\|system\|>|<\|assistant\|>)
    - (?i)(?:\\begin\{system\}|\\end\{system\})
  encoding_trick:
    - ^[A-Za-z0-9+/]{20,}={0,2}$  (base64 candidate)
    - ^(?:[0-9a-fA-F]{2}\s*){16,}$  (hex candidate)
    - (?i)(?:\\u[0-9a-fA-F]{4}){4,}  (unicode escape cluster)
    - (?i)(?:&#x[0-9a-fA-F]{2,4};){4,}  (HTML entity encoding)
  context_poisoning:
    - (?i)(?:this\s+is\s+(?:a\s+)?(?:system|new|override)\s+(?:message|prompt|instruction))
    - (?i)(?:you\s+will\s+now\s+respond\s+as\b)
    - (?i)(?:end\s+of\s+(?:previous\s+)?output\b)
validation and testing strategy:
  unit tests:
    - each regex pattern tested against positive matches (known injection)
    - each regex pattern tested against negative matches (benign content)
    - false-positive rate per pattern must be below 0.5% on a 10K sample corpus
  integration tests:
    - pipeline test: raw agent output -> detector -> sanitizer -> clean output
    - recursive decode test: base64(hex(unicode(injection))) -> detection
    - mixed payload test: legitimate content bookending injection -> extract mode
  acceptance criteria:
    - detection rate on known injection dataset: >= 95%
    - false-positive rate across benign corpus: <= 1.0%
    - latentency per 1K tokens: < 100ms
    - no false-negative on severity=high patterns
  regression suite:
    - run against injection dataset after every regex change
    - track detection rate and false-positive rate per version
    - auto-reject any change that drops detection below 93% or raises FP above 1.5%
error handling:
  malformed input:
    - non-string input: log error, return empty string, no crash
    - excessively long input (>100K chars): chunk at 50K, sanitize each chunk, reassemble
    - binary/non-utf-8 content: log warning, return original unmodified
  regex failure:
    - catastrophic backtracking timeout: 500ms per regex, abort that pattern, log
    - invalid regex: log error, skip pattern, continue with remaining
  pipeline failure:
    - any stage fails: log full trace, return original content (fail-open for safety)
    - downstream agent dependency: record in log, do not block pipeline
config:
  yaml_source: config.yaml
  runtime_params:
    max_recursive_depth: 3
    regex_timeout_ms: 500
    max_chunk_size: 50000
    fail_open: true
    log_level: info
requirement definitions:
  Canonical location: config.yaml under key requirements.
  BLUEPRINT.md references: "See config.yaml -> requirements for authoritative definitions."
  This eliminates dual-location redundancy. All versioned requirement specs
  (detection rate, FP rate, latency, bypass depth) live in config.yaml only.
version notes:
  v1 -> v2 changes:
    - Consolidated requirement definitions into config.yaml (single canonical location)
    - Extracted all YAML configuration blocks from BLUEPRINT.md into config.yaml
    - Added validation and testing strategy section with acceptance criteria
    - Expanded detection regex library from 8 patterns to 22 patterns across 5 categories
    - Added error-handling specifications for malformed input, regex failure, pipeline failure
    - Added false-positive rate targets at both per-pattern (0.5%) and aggregate (1.0%) levels