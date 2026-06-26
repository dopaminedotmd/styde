hardcoded secret scan on D:\styde area 30000 files checked 1800 unique files scanned
Security Audit Report: secrets-hardening-auditor
Target: D:\styde (whole workspace)
Scan date: 2026-06-26
Tool: regex-based scan + manual file inspection
findings:
  - file: apps/konsult-agent/konsult.py
    line: 56
    secret_type: api_key pattern (commented)
    value: "# api_key = os.getenv(\"OPENAI_API_KEY\") or os.getenv(\"ANTHROPIC_API_KEY\")"
    risk_level: LOW
    details: Commented-out credential pattern. No actual key present, but the pattern trains developers to think about api_key in source. Hallmark of placeholder code that never got wired to env vars.
    remediation: Remove the comment or replace with an active os.getenv() call wired to a real .env file. Add .env.example with OPENAI_API_KEY= and ANTHROPIC_API_KEY= stubs.
  - file: eval/benchmarks/code-review-basic/golden/case-1/input.py
    line: 3
    secret_type: plaintext password
    value: "admin123"
    risk_level: INFO (intentional test fixture)
    details: This file is a deliberate golden fixture for the code-review-basic benchmark. The hardcoded password is the test's intended finding, not a production leak. No action required.
    remediation: None. Verify the fixture stays inside eval/benchmarks/ and never enters a production deploy.
  - file: (missing)
    secret_type: .env.example template
    value: null
    risk_level: MEDIUM
    details: Root .gitignore has !.env.example (track it) but no .env.example exists anywhere. Forge .gitignore ignores .env.example. Developers have no documented list of required environment variables.
    remediation: Create .env.example at repo root listing OPENAI_API_KEY, ANTHROPIC_API_KEY, HERMES_PATH, FORGE_ROOT template values. Unify .gitignore policies.
  - file: _alpedal/styde-forge/Dashboard/web/server_8765.py
    line: 22
    secret_type: CSRF_SECRET
    value: secrets.token_hex(32) [dynamic]
    risk_level: PASS (secure pattern)
    details: Uses Python secrets module at runtime. No hardcoded value. Correct pattern. CSP, CORS, body limits, input validation also present.
    remediation: None.
  - file: _alpedal/styde-forge/99_INDEXES/hardware_profile.json
    secret_type: model provider config keys
    value: deepseek-v4-flash, deepseek-v4-pro
    risk_level: PASS (no credentials)
    details: Contains model names and provider identifiers. No API keys or tokens.
    remediation: None.
summary:
  critical: 0
  high: 0
  medium: 1
  low: 1
  info: 1 (intentional test fixture)
  pass: 2
verdict: CLEAN. No actual API keys, tokens, passwords, private keys, or connection strings are hardcoded in production source code. The codebase passes a zero-tolerance secrets policy for production code.
remaining gaps:
  - Missing .env.example prevents developers from knowing what env vars to set.
  - Commented os.getenv() call in konsult.py should be removed or activated.
  - Two .gitignore files disagree on .env.example tracking policy.
recommendations:
  - Create .env.example with stubs for all API keys used across the workspace.
  - Unify .gitignore: track .env.example at repo root, ignore .env and .env.local.
  - Strip the dead comment from konsult.py line 55-56.
  - Add git-secrets pre-commit hook config (.git-secrets pattern file) to prevent future real key commits.
  - Run git log --all -p --diff-filter=M -- '*.py' '*.json' '*.yaml' to check if any credentials were committed then scrubbed in git history.