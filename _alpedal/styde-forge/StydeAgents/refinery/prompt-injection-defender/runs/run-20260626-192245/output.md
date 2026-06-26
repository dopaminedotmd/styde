┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\prompt-injection-defender\persona.md → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\prompt-injection-defender\persona.md[0m
[38;2;139;134;130m@@ -8,3 +8,5 @@[0m
[38;2;184;134;11m - Python: regex patterns, AST analysis, string scanning[0m
[38;2;184;134;11m - Output: return clean content + sanitization log[0m
[38;2;184;134;11m - Never trust agent output — always sanitize before passing as context[0m
[38;2;255;255;255;48;2;19;87;20m+- Methodology: always include a 'Methodology' subsection describing the detection approach (pattern matching, semantic analysis, heuristic rules)[0m
[38;2;255;255;255;48;2;19;87;20m+- Original Context: always include an 'Original Context' subsection contrasting findings against benign intent[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\prompt-injection-defender\BLUEPRINT.md → b/StydeAgents\blueprints\prompt-injection-defender\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -1,21 +1,149 @@[0m
[38;2;184;134;11m ---[0m
[38;2;255;255;255;48;2;119;20;20m-name: prompt-injection-defender[0m
[38;2;255;255;255;48;2;119;20;20m-domain: security[0m
[38;2;255;255;255;48;2;119;20;20m-version: 1[0m
[38;2;255;255;255;48;2;19;87;20m+# Configuration in config.yaml — see version_history, domain, dependencies there[0m
[38;2;255;255;255;48;2;19;87;20m+# This file is the canonical narrative specification.[0m
[38;2;184;134;11m ---[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m # Prompt Injection Defender[0m
[38;2;255;255;255;48;2;119;20;20m-**Domain:** security **Version:** 1[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Domain: security[0m
[38;2;255;255;255;48;2;19;87;20m+Version: 5 (see config.yaml for version history)[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Purpose[0m
[38;2;255;255;255;48;2;119;20;20m-Protects AI agent systems from prompt injection attacks. Sanitizes agent output before passing it as context to other agents, detects and strips jailbreak attempts ("IGNORE ALL PREVIOUS INSTRUCTIONS", role-playing, delimiters), and logs sanitization events.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Protects AI agent systems from prompt injection attacks. Sanitizes agent output before passing it as context to other agents, detects and strips jailbreak attempts, and logs sanitization events with full traceability.[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m ## Persona[0m
[38;2;255;255;255;48;2;119;20;20m-AI security specialist. Expert in prompt injection, jailbreak detection, output sanitization, and secure multi-agent communication patterns.[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-## Skills[0m
[38;2;255;255;255;48;2;119;20;20m-- Detection: identify injection patterns (ignore instructions, role-playing, delimiter attacks)[0m
[38;2;255;255;255;48;2;119;20;20m-- Sanitization: strip or neutralize injection payloads, extract safe content[0m
[38;2;255;255;255;48;2;119;20;20m-- Logging: record sanitization events (agent, pattern detected, action taken)[0m
[38;2;255;255;255;48;2;119;20;20m-- Bypass resistance: recursive patterns, encoding variations, nested injections[0m
[38;2;255;255;255;48;2;119;20;20m-- Python: regex, AST parsing, string analysis patterns[0m
[38;2;255;255;255;48;2;19;87;20m+See persona.md for full agent persona definition.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Architecture[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Detection Engine[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Parallel batch matching engine using concurrent.futures.ThreadPoolExecutor with max_workers=8. Each pattern has an individual timeout of 100ms. The engine batches all 22+ regex patterns into a single parallel evaluation pass, reducing worst-case latency from 11s+ (sequential) to ~100ms (parallel).[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Pattern matching uses re.SEARCH (not re.FULLMATCH) for all base64, hex, and encoding-variant patterns to find embedded payloads within longer strings. Inline lookaheads are used to match obfuscated injection boundaries without consuming characters.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Detection Pattern Library[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+All patterns are organized in five tiers, evaluated in parallel:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Tier 1: Direct injection (re.IGNORECASE, re.SEARCH)[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bIGNORE\s+ALL\b.*\bPREVIOUS\s+INSTRUCTIONS?\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bDISREGARD\b.*\bPRIOR\s+(DIRECTIVES|CONTEXT|PROMPTS?)\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bYour\s+new\s+prompt\s+is\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bNow\s+you\s+are\b.*\b(assistant|bot|AI)\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bFrom\s+now\s+on\b.*\byou\s+will\b'[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Tier 2: Role-playing and persona hijacking  (re.IGNORECASE, re.SEARCH)[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bDAN\b'  (Do Anything Now)[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bDo\s+Anything\s+Now\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bAct\s+as\s+if\b.*\b(no\s+rules|unlimited|no\s+restrictions)\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bYou\s+are\s+now\b.*\b(free|unleashed|unbounded|uncensored)\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bIgnore\s+(your\s+)?(ethics|safety|guidelines|policies?|rules?)\b'[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Tier 3: Delimiter-based injection (re.SEARCH)[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'\[\[\s*SYSTEM\s*:\s*.*?\]\]'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'<\s*(user|system|assistant)\s*>.*?<\s*/\s*(user|system|assistant)\s*>'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'---+\s*(NEW\s+)?(INSTRUCTION|PROMPT|CONTEXT)\s*---'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'```(?:\s*\w+)?\s*(?:SYSTEM|INSTRUCTION|PROMPT):'[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Tier 4: Encoding and obfuscation (re.SEARCH, loose anchoring)[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)(?:[A-Za-z0-9+/]{4,40}={0,2})\s*(?:ignore|disregard|forget|new\s+prompt)'  # base64 adjacent injection[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)0x[0-9a-fA-F]{4,}\s*(?:instruction|prompt|role)'  # hex adjacent injection[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'\\x[0-7]{3}|\\u[0-9a-fA-F]{4}|%[0-9a-fA-F]{2}'  # escaped/encoded chars near injection context[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)(?:normalize|transform|decode|convert)\s+(?:this|the\s+following)\s+(?:text|input|prompt|message)'[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Tier 5: Recursive and nested injection (re.DOTALL, re.SEARCH)[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(\bIGNORE\b.*?){2,}'  # stacked ignore directives[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?:role[\s-]*play|roleplay).*?(?:ignore|disregard|forget).*?(?:instruction|prompt|rule)'  # nested bypass[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bSIMULATE\b.*\bNEW\s+CONTEXT\b'[0m
[38;2;255;255;255;48;2;19;87;20m+  - r'(?i)\bFICTIONAL\b.*\bSCENARIO\b.*\bOVERRIDE\b'[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Sanitization Modes[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Two sanitization modes, configurable at init:[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;139;134;130m… omitted 83 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\prompt-injection-defender\config.yaml → b/D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\prompt-injection-defender\config.yaml[0m
[38;2;139;134;130m@@ -38,3 +38,9 @@[0m
[38;2;184;134;11m     score: 88.4[0m
[38;2;184;134;11m     previous_score: 88.6[0m
[38;2;184;134;11m     timestamp: '2026-06-26T19:22:43Z'[0m
[38;2;255;255;255;48;2;19;87;20m+  - from: 5.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    to: 6.0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    reason: 'MAJOR: applied all 4 feedback rounds — parallel engine (ThreadPoolExecutor, max_workers=8, 100ms timeout), loose anchoring (re.SEARCH), expanded regex library (DAN, ignore-direction, instruction-override), <REDACTED> placeholder, testing+validation section with FP<=2% targets, error-handling specs, pre-commit spell-check, persona methodology+context requirements'[0m
[38;2;255;255;255;48;2;19;87;20m+    score: null[0m
[38;2;255;255;255;48;2;19;87;20m+    previous_score: 88.4[0m
[38;2;255;255;255;48;2;19;87;20m+    timestamp: '2026-06-26T21:30:00Z'[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-prompt-injection-defender-v6.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-prompt-injection-defender-v6.py[0m
[38;2;139;134;130m@@ -0,0 +1,104 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+Ad-hoc verification: prompt-injection-defender blueprint v6[0m
[38;2;255;255;255;48;2;19;87;20m+Not a canonical test suite — temporary verification script.[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, sys, yaml, json[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+DIR = "D:\\styde\\_alpedal\\styde-forge\\StydeAgents\\blueprints\\prompt-injection-defender"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+checks = 0[0m
[38;2;255;255;255;48;2;19;87;20m+passed = 0[0m
[38;2;255;255;255;48;2;19;87;20m+failed = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check(name, condition, detail=""):[0m
[38;2;255;255;255;48;2;19;87;20m+    global checks, passed, failed[0m
[38;2;255;255;255;48;2;19;87;20m+    checks += 1[0m
[38;2;255;255;255;48;2;19;87;20m+    if condition:[0m
[38;2;255;255;255;48;2;19;87;20m+        passed += 1[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  PASS  {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        failed.append(name)[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  FAIL  {name}  {detail}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- File existence ---[0m
[38;2;255;255;255;48;2;19;87;20m+print("=== File existence ===")[0m
[38;2;255;255;255;48;2;19;87;20m+for f in ["BLUEPRINT.md", "config.yaml", "persona.md"]:[0m
[38;2;255;255;255;48;2;19;87;20m+    path = os.path.join(DIR, f)[0m
[38;2;255;255;255;48;2;19;87;20m+    check(f"exists: {f}", os.path.isfile(path))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- YAML validation ---[0m
[38;2;255;255;255;48;2;19;87;20m+print("\n=== YAML (config.yaml) ===")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(os.path.join(DIR, "config.yaml")) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    cfg = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+check("config.yaml is valid dict", isinstance(cfg, dict))[0m
[38;2;255;255;255;48;2;19;87;20m+check("blueprint.name == prompt-injection-defender",[0m
[38;2;255;255;255;48;2;19;87;20m+      cfg.get("blueprint", {}).get("name") == "prompt-injection-defender")[0m
[38;2;255;255;255;48;2;19;87;20m+hist = cfg["blueprint"]["version_history"][0m
[38;2;255;255;255;48;2;19;87;20m+check("5 version history entries", len(hist) == 5)[0m
[38;2;255;255;255;48;2;19;87;20m+check("last entry to: 6.0.0", hist[-1]["to"] == "6.0.0")[0m
[38;2;255;255;255;48;2;19;87;20m+check("last entry score: null", hist[-1]["score"] is None)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- BLUEPRINT.md content ---[0m
[38;2;255;255;255;48;2;19;87;20m+print("\n=== BLUEPRINT.md content ===")[0m
[38;2;255;255;255;48;2;19;87;20m+with open(os.path.join(DIR, "BLUEPRINT.md"), encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Parallel engine[0m
[38;2;255;255;255;48;2;19;87;20m+check("ThreadPoolExecutor", "ThreadPoolExecutor" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("max_workers=8", "max_workers=8" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("100ms timeout", "100ms" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("re.SEARCH loose anchoring", "re.SEARCH" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Expanded regex library[0m
[38;2;255;255;255;48;2;19;87;20m+check("DAN pattern", "DAN" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("Do Anything Now", "Do Anything Now" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("instruction-override variant ('Your new prompt is')", "Your\\s+new\\s+prompt" in bp or "Your new prompt" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("ignore-direction variants (DISREGARD)", "DISREGARD" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Sanitization[0m
[38;2;255;255;255;48;2;19;87;20m+check("STRIP_OR_REPLACE mode", "STRIP_OR_REPLACE" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("<REDACTED> placeholder", "<REDACTED>" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Testing & Validation[0m
[38;2;255;255;255;48;2;19;87;20m+check("Testing and Validation Strategy section", "Testing and Validation Strategy" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("FP <=1% (tier 1)", "<=1%" in bp or "<=1% false positive" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("FP <=2% (overall)", "<=2% false positive rate" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("FN <0.1% target", "<0.1%" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Error handling[0m
[38;2;255;255;255;48;2;19;87;20m+check("Regex compile failure fallback", "Regex compile failure" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("Pattern timeout handling", "Pattern timeout" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("LLM-as-judge fallback", "LLM-as-judge" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+check("Encoding decode failure", "Encoding decode failure" in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Logging[0m
[38;2;255;255;255;48;2;19;87;20m+check("Structured log (latency_ms field)", '"latency_ms"' in bp)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Pre-commit spell-check[0m
[38;2;139;134;130m… omitted 26 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verification: 31/31 checks passed. Temp script cleaned up.
This is ad-hoc verification, not a canonical test suite. The three modified files (BLUEPRINT.md, config.yaml, persona.md) pass all structural and content checks. No code was written/compiled/tested — these are documentation files only, so there is no build step or runtime to exercise.