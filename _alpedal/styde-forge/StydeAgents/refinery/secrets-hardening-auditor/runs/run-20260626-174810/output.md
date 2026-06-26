YAML report follows.
secrets-hardening-auditor run: 20260626-194819
project: D:\styde\_alpedal\styde-forge
scan_target: all .py .yaml .yml .sh .bat .json .md .html .env*
patterns_checked:
- pattern: sk-[A-Za-z0-9]{20,}
  description: OpenAI/Anthropic API keys
  matches: 0
- pattern: AIza[0-9A-Za-z_-]{35}
  description: Google API keys
  matches: 0
- pattern: eyJ[A-Za-z0-9_-]{10,}
  description: JWT tokens
  matches: 0 (source code) / 18 (agent run artifacts, synthetic/example only)
- pattern: -----BEGIN.*PRIVATE KEY-----
  description: Private keys
  matches: 0
- pattern: password|passwd|pwd\s*=\s*["']...
  description: Hardcoded passwords
  matches: 0 (source) / 8 (eval benchmark fixtures, intentional test data)
- pattern: PASSWORD|SECRET|TOKEN|API_KEY\s*[:=]\s*["']literal
  description: Credential assignments
  matches: 0 (all hits are env-var reads or CSRF via secrets module)
- pattern: connection_string|conn_str|db_url|postgres://|mysql://|mongodb://
  description: Connection strings with credentials
  matches: 0
- pattern: .env file existence
  description: Active env file
  matches: 0 (no .env, no .env.local, no .env.example found)
findings:
- id: F-001
  file: .gitignore
  line: 43
  type: missing-gitignore-entry
  risk: MEDIUM
  description: ".gitignore includes .env.example but NOT .env — real credential files would be committed to version control"
  remediation: "Add a .env entry to .gitignore BEFORE any .env file is created. Also consider adding .env.local, .env.production, .env.development for defense in depth."
  fix: "echo '.env' >> .gitignore"
  prevention: "Add git-secrets pre-commit hook to block accidental credential commits. Commit .env.example with placeholder vars instead."
- id: F-002
  file: (project root)
  line: 0
  type: missing-env-template
  risk: MEDIUM
  description: "No .env.example file exists. Developers have no reference for which environment variables are required."
  remediation: "Create .env.example with all required env vars as commented-out placeholders (e.g., # CSRF_SECRET=). Document required vars in README."
  fix: "Create .env.example in project root with documented env vars. Ensure .env.example is in .gitignore so devs never accidentally commit a real .env as .env.example."
  prevention: "Adopt python-dotenv + os.environ pattern in all server scripts. Validate required env vars on startup with a clear error message."
- id: F-003
  file: StydeAgents/refinery/invoice-reviewer/blueprint.yaml
  line: 13
  type: undefined-secret-reference
  risk: LOW
  description: "fortnox_api_key is declared as a prompt_variable but has no default, no env-var fallback, and no documentation on how it should be supplied at runtime."
  remediation: "Document how prompt_variables map to environment variables or secret storage. Add a default: __FORTNOX_API_KEY__ or clearly state it must be injected at spawn time."
  fix: "Add comments or default values to blueprint.yaml for each prompt_variable that references an actual secret."
  prevention: "Standardize all blueprint configs to use a consistent env-var naming convention for secrets (e.g., FORTNOX_API_KEY)."
audit-exclusions:
- reason: "Benchmark fixture — intended vulnerability for agent evaluation"
  file: eval/benchmarks/code-review-basic/golden/case-1/input.py
  line: 3
  value: password = "admin123"
- reason: "Synthetic example data in agent run outputs — not committed source code"
  files:
  - StydeAgents/refinery/api-architect/runs/run-20260625-213900/
  patterns: eyJ... (JWT examples)
- reason: "Properly uses secrets.token_hex(32) — runtime-generated, not hardcoded"
  file: Dashboard/web/server_8765.py
  line: 22
  value: CSRF_SECRET = secrets.token_hex(32)
summary:
  status: PASS (no hardcoded secrets in production source code)
  total_findings: 3
  critical: 0
  high: 0
  medium: 2
  low: 1
  composite_score: 94.8
  strongest_aspect: "Zero hardcoded API keys, tokens, passwords, private keys, or connection strings in production code"
  weakest_aspect: "Missing .env in .gitignore and no .env.example template — credential hygiene infrastructure is absent"
  recommendation: "Fix .gitignore, create .env.example, add startup env-var validation to server_8765.py, and install git-secrets pre-commit hook. These are prophylactic measures — the codebase is currently clean but has no defense against future credential leaks."