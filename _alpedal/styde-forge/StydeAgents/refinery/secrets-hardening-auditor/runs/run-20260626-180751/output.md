Secrets Hardening Audit Report
===============================
Target: D:\styde\_alpedal\styde-forge
Date: 2026-06-26
Files scanned: 34172 total (69 Python, rest configs/run artifacts/docs)
Depth: Full tree (34K files - Large Codebase Optimization applied)
CI/CD: No pipeline configs found (.github, .gitlab-ci.yml, .circleci) - N/A
Categories covered: 3 (API keys, DB credentials/connection strings, tokens/secrets)
CATEGORY 1: API KEYS (sk-, AIza-, xai-, Bearer patterns)
=========================================================
Source: rg -n 'sk-[A-Za-z0-9]{32,}' -g '!checkpoints/**' --type py + broad all-file scan
Result: 0 findings in production code
Evidence: All pattern scans returned empty result sets
Status: CLEAN
CATEGORY 2: DATABASE CREDENTIALS / CONNECTION STRINGS
======================================================
Source: rg -n '(postgresql://|mysql:***@]+@' -g filters
FINDING HD-CONN-001 | CRITICAL
  File: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/self_eval_prompt.txt
  Line: 387
  Context: Agent-generated Kubernetes Secret manifest example
  Value: postgresql+asyncpg://appuser:S3cur3P@ssw0rd!@postgres-svc:5432/appdb
  Type: Connection string with embedded credentials
  Tag: production (agent promoted to production tier)
  Risk: Example/demo credential - agent hallucinated inline creds in output
  Note: This is agent-generated example text, not a real deployed secret. However, it trains the agent to produce output with hardcoded credentials in production-tier runs.
FINDING HD-CONN-002 | CRITICAL
  File: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/self_eval_prompt.txt
  Line: 388
  Value: redis://:r3d1sS3cr3t@redis-svc:6379/0
  Tag: production
  Note: Same context as HD-CONN-001
FINDING HD-CONN-003 | HIGH
  File: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/judge_eval_prompt.txt
  Line: 277
  Value: redis://:devcachepass@redis:6379/0
  Tag: production
  Note: Same production agent run, different eval artifact
FINDING HD-CONN-004 | MEDIUM
  File: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/self_eval_prompt.txt
  Line: 389
  Value: SECRET_KEY: "k8s-production-secret-key-must-be-at-least-32-bytes"
  Tag: production
  Note: Example secret key in manifest output
CATEGORY 3: TOKENS / SECRETS (JWT, Bearer, npm_, ghp_, SSH keys)
==================================================================
Source: Multi-pattern rg across all file types
FINDING HD-TOK-001 | LOW
  File: StydeAgents/production/container-orchestrator/runs/run-20260626-000800/self_eval_prompt.txt
  Line: 391
  Value: [REDACTED PRIVATE KEY] (BEGIN RSA PRIVATE KEY header)
  Tag: production
  Note: The actual key content is [REDACTED] - this is a placeholder/example block. The header/footer lines trigger the detector but no real private key data is present.
CATEGORY 4: PRODUCTION SOURCE CODE (Core/*.py, Dashboard/*.py, CommandCenter/*.py)
=====================================================================================
Source: rg for all secret patterns across Core/, Dashboard/, CommandCenter/ excluding test/fixture/vendor
Result: 0 hardcoded secrets
Evidence:
  Core/quality_gates.py: Contains its own _scan_api_keys() and _scan_credentials() functions that detect secrets in agent output. These are detector functions, not hardcoded creds.
  Dashboard/web/server_8765.py: CSRF_SECRET = secrets.token_hex(32) - runtime-generated random value. Verified via hex dump: 73 65 63 72 65 74 73 2e 74 6f 6b 65 6e 5f 68 65 78 28 33 32 29
  Core/hermes_bridge.py: Uses os.environ.get("HERMES_PATH", "") for API key config. No hardcoded values.
Status: CLEAN - production source code uses env vars and runtime generation
CATEGORY 5: DELIBERATELY-VULNERABLE / TEST FIXTURES
=====================================================
FINDING HD-BENCH-001 | INFO (deliberately-vulnerable)
  File: eval/benchmarks/code-review-basic/golden/case-1/input.py
  Line: 3
  Value: password = "admin123"
  Tag: deliberately-vulnerable / fixture
  Note: This file is part of a code-review benchmark suite. The hardcoded password is intentional test data for evaluating code review agents.
  Risk: Zero - excluded from production risk scoring per Scope & Filtering rules
CATEGORY 6: INFRASTRUCTURE / PREVENTION
========================================
FINDING HD-INFRA-001 | MEDIUM
  .gitignore: Line 43 lists .env.example but MISSING .env pattern
  Evidence: grep -n '\.env' .gitignore returned only ".env.example"
  Risk: Developers could accidentally commit .env with real secrets
  Remediation: Add ".env" and ".env.local" to .gitignore
FINDING HD-INFRA-002 | MEDIUM
  No .env.example template exists anywhere in repo
  Evidence: find . -name '.env.example' returned empty
  Risk: No documented contract for required env vars
  Remediation: Create .env.example with placeholder entries for all env vars
FINDING HD-INFRA-003 | MEDIUM
  No pre-commit hooks configured for secret scanning
  Evidence: .pre-commit-config.yaml does not exist; .git/hooks/ are default
  Risk: No gating mechanism prevents accidental secret commits
  Remediation: Configure git-secrets or detect-secrets pre-commit hook
FINDING HD-INFRA-004 | MEDIUM
  No CI/CD pipeline configs found for automated secret scanning
  Evidence: No .github/, .gitlab-ci.yml, .circleci/config.yml files
  Risk: No automated scanning in CI pipeline; secrets could be committed without detection
  Context: This is a local Forge project, not a CI-deployed service. Risk is contextual.
CATEGORY 7: GIT HISTORY
========================
Source: git log -p -S "sk-" + git log -p -S "token" -- .
Result: No real secrets found in git history. Only artifacts:
  - "demo-token-very-long-secure-string" (placeholder text, exists in current tree)
  - CDN cache-control keys (configuration keys, not secrets)
  - "strydeforge-auth-key" (certificate chain key name in agent output)
Status: CLEAN - no real credential exposure in commit history
RISK SCORING
============
CRITICAL: 2 (HD-CONN-001, HD-CONN-002) - production agent run artifacts with example creds
HIGH: 1 (HD-CONN-003) - additional example cred in same production agent
MEDIUM: 4 (HD-CONN-004, HD-INFRA-001/2/3)
LOW: 1 (HD-TOK-001)
INFO: 1 (HD-BENCH-001)
PASS/FAIL: PASS (0 critical in production source code)
Production threshold: NOT MET (production agent run artifacts contain example embedded credentials, indicating the agent generates output with hardcoded creds when producing Kubernetes manifests)
KEY REMEDIATIONS
================
1. Production source code is clean - env vars and runtime generation used throughout
2. The container-orchestrator agent produces example K8s Secrets with inline credentials in its output. This is a behavioral pattern that must be fixed in the blueprint: add instruction to never include example credentials in output, use ${} placeholders or references to secret managers instead.
3. Add .env to .gitignore
4. Create .env.example template
5. Consider adding git-secrets pre-commit hook for defense-in-depth