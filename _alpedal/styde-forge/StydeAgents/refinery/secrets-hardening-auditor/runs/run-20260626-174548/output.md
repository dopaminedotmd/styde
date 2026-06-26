secrets-hardening-audit:styde-forge
timestamp:2026-06-26T19:46:00Z
scanner-version:1
policy:zero-secrets
status:FAIL
findings:
  - id: F001
    severity: CRITICAL
    type: private-key-exposure
    file: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/output.md
    line: 372
    secret-type: RSA Private Key
    snippet: "-----BEGIN RSA PRIVATE KEY----- ... -----END RSA PRIVATE KEY-----"
    exposed-in: agent-generated run artifact (markdown output)
    risk: full cryptographic key compromise if leaked outside repo; enables impersonation, decryption, MITM
    remediation:
      - purge all run artifacts containing private keys from git history using git filter-repo or BFG
      - add runs/ directory pattern to .gitignore (runs/*.md, runs/*.txt)
      - instruct container-orchestrator agent to REDACT or mask private key blocks in generated output
      - rotate any key pair that matches the exposed modulus
      - add quality_gates.py check: flag any file containing -----BEGIN.*PRIVATE KEY-----
  - id: F002
    severity: CRITICAL
    type: private-key-exposure
    file: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/self_eval_prompt.txt
    line: 391
    secret-type: RSA Private Key
    snippet: "-----BEGIN RSA PRIVATE KEY-----"
    risk: same as F001
    remediation: same as F001 — consolidate into git-history scrub + runs/ ignore + agent output masking
  - id: F003
    severity: CRITICAL
    type: private-key-exposure
    file: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/judge_eval_prompt.txt
    line: 391
    secret-type: RSA Private Key
    snippet: "-----BEGIN RSA PRIVATE KEY-----"
    risk: same as F001
    remediation: same as F001 — shared pattern across all runs artifacts
  - id: F004
    severity: HIGH
    type: hardcoded-credentials
    file: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/output.md
    line: 257
    secret-type: Database Credentials
    snippet: "DATABASE_URL: postgresql+asyncpg://devuser:devpass@postgres:5432/devdb"
    risk: database access with clear-text password in agent output
    remediation: replace dev credentials with env var references (${DB_URL}); mask in generated output
  - id: F005
    severity: HIGH
    type: hardcoded-credentials
    file: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/output.md
    line: 258
    secret-type: Redis Credentials
    snippet: "REDIS_URL: redis://:devcachepass@redis:6379/0"
    risk: cache access with clear-text password
    remediation: same as F004 — env var reference in agent output templates
  - id: F006
    severity: HIGH
    type: hardcoded-credentials
    file: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/output.md
    line: 259
    secret-type: Secret Key
    snippet: "SECRET_KEY: dev-secret-change-in-production"
    risk: session signing key exposed
    remediation: replace with env var placeholder; mask in agent output
  - id: F007
    severity: MED
    type: hardcoded-password
    file: eval/benchmarks/code-review-basic/golden/case-1/input.py
    line: 3
    secret-type: Default Password
    snippet: "password = \"admin123\""
    context: eval benchmark fixture — intentional for code review test case
    risk: low in isolation (test data), but establishes pattern; downstream consumers may copy
    remediation: annotate as intentional test fixture; add comment "# TEST FIXTURE — NOT REAL" to prevent copy-paste accidents
  - id: F008
    severity: HIGH
    type: missing-gitignore-entry
    file: .gitignore
    line: 0
    secret-type: .env file not gitignored
    snippet: ".env.example present in gitignore (line 43) but .env, .env.local, .env.production are NOT"
    risk: developer .env files with real secrets can be accidentally committed
    remediation: add lines: .env, .env.local, .env.production, .env.staging to .gitignore
  - id: F009
    severity: MED
    type: hardcoded-credentials
    file: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/output.md
    line: 368
    secret-type: Production Database Credentials
    snippet: "DATABASE_URL: postgresql+asyncpg://appuser:S3cur3P@ssw0rd!@postgres-svc:5432/appdb"
    risk: production-grade credentials in agent output artifact
    remediation: same as F001-F003 block — runs artifact masking for ALL credential patterns
consolidated-remediation:
  - severity: CRITICAL
    pattern: private-keys-in-runs-artifacts
    files: [F001, F002, F003]
    action:
      - git filter-repo --path-glob 'runs/*.md' --path-glob 'runs/*.txt' --invert-paths  # scrub history
      - add runs/ to .gitignore
      - patch container-orchestrator agent prompt: "REDACT any -----BEGIN * PRIVATE KEY----- block before writing output"
      - add quality_gates pattern: r'-----BEGIN\s+(RSA|EC|DSA|OPENSSH)\s+PRIVATE\s+KEY-----' severity=critical
  - severity: HIGH
    pattern: credentials-in-runs-artifacts
    files: [F004, F005, F006, F009]
    action:
      - patch container-orchestrator agent prompt: "Replace all hardcoded passwords/tokens/keys in YAML config blocks with environment variable placeholders (e.g. ${DB_URL})"
      - add quality_gates pattern: r'(password|secret|PWD|credential)\s*[:=]\s*["\']?(?!\$)'
  - severity: HIGH
    pattern: gitignore-missing-env
    files: [F008]
    action: add .env .env.local .env.production .env.staging to .gitignore before next commit
  - severity: MED
    pattern: test-fixture-credentials
    files: [F007]
    action: add "# TEST FIXTURE — NOT A REAL SECRET" comment to eval benchmark fixtures that contain credential-like strings
defenses-already-present:
  - quality_gates.py:_scan_api_keys — detects Google AIza API keys, xAI tokens, bearer tokens
  - quality_gates.py:_scan_credentials — detects hardcoded password=, secret=, token= assignments
  - quality_gates.py: .env file detection — flags .env/.env.local/.env.production as CRITICAL
  - quality_gates.py: placeholder key detection — flags "YOUR_KEY_HERE"
  - quality_gates.py: empty key detection — flags "api_key: ''"
  - hermes_bridge.py: uses os.environ.get for HERMES_PATH (env-var pattern)
missing-defenses:
  - no .env entry in .gitignore (only .env.example is ignored)
  - no git-secrets or pre-commit hook configured
  - no runs/ output masking policy
  - no private key pattern in quality_gates regex list
  - no automated scrub of agent-generated output before commit
  - no git history scanning tool integrated
recommendation-priority:
  1: add .env .env.local .env.production .env.staging to .gitignore (5-minute fix, blocks future leaks)
  2: add "-----BEGIN.*PRIVATE KEY-----" pattern to quality_gates._scan_credentials (CRITICAL)
  3: scrub git history of runs/ artifacts containing keys (git filter-repo)
  4: patch container-orchestrator agent prompt: mask credentials and keys in output generation
  5: add pre-commit hook: quality_gates.run() on every commit
  6: add pre-push hook: git-secrets --scan
verification: re-scan after fixes — all findings must resolve to zero
verification-command: python3 -c "from Core.quality_gates import scan_forge; findings = scan_forge(); print(f'{len(findings)} findings'); assert len(findings) == 0"