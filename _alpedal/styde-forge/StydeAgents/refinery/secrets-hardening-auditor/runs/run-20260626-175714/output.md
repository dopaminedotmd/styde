Secrets Hardening Auditor — REP-20260626-1957
source: git ls-files (tracked), grep, read_file
EVALUATIONTIMESTAMP: 2026-06-26T19:57:00Z
TOTALSCORE: 88/100
SCOPEBOUNDARIES: git-tracked files in D:/styde/_alpedal/styde-forge (4,918 files). Excluded checkpoints/ (gitignored build artifacts, zero tracked files). Excluded .git/ internals and binary files in 99_INDEXES/.
FINDINGS (ordered CRITICAL -> LOW)
File | Line | Secret Type | Risk Level | Remediation | Verified
eval/benchmarks/code-review-basic/golden/case-1/input.py | 3 | Hardcoded password "admin123" | CRITICAL | Replace with os.environ.get('DB_PASSWORD') and set via env var or .env | verified via read_file: line 3 literal
eval/benchmarks/code-review-basic/golden/case-1/input.py | 2 | SQL injection (f-string in query) | CRITICAL | Use parameterized queries (cursor.execute('SELECT * FROM users WHERE name = ?', (items[0],))) | verified via read_file: line 2 f-string
scripts/parallel_spawn.py | 181 | os.system call (potential injection) | HIGH | Use subprocess.run([sys.executable, ...], check=True) instead of os.system | verified via read_file: line 181
.gitignore | 43 | .env not excluded from git | MEDIUM | Add '.env' and '.env.*' to .gitignore (only .env.example is excluded) | verified via read_file: .gitignore line 43
full codebase | N/A | No env-var or secret-manager pattern | MEDIUM | Add python-dotenv to requirements; replace all existing hardcoded passwords with os.environ.get() | verified via grep: zero os.environ[] and zero load_dotenv imports across all tracked .py files
StydeAgents/refinery/invoice-reviewer/blueprint.yaml | 14 | Variable name contains 'api_key' | INFO | Use <SECRET> or env_var_name per naming convention; current usage is metadata-only (not a value) | verified via read_file: blueprint.yaml line 14
ASSUMPTIONS
claim: 4,918 tracked files | source: git ls-files | wc -l | confidence: 100% (direct command output)
claim: checkpoints/ contains zero tracked files | source: git ls-files checkpoints/ | wc -l = 0 | confidence: 100%
claim: no .env files exist in repo | source: git ls-files | grep -c '\.env\b' = 0 + find . -name '.env' (no results) | confidence: 100%
ASSUMPTION: The vendor-specific key patterns (sk-*, AIza*, xai-*, AKIA*) may miss keys from less common providers (Azure, IBM, DigitalOcean, etc.) | confidence: 90% — no fallback pattern for unknown provider keys exists in the scan
RAW DATA APPENDIX (contradiction resolution)
Discrepancy: file count mismatch between two sources
  source A: git ls-files = 4,918
  source B: find . -type f (excluding .git) = 33,947
  root cause: checkpoints/ contains ~29K generated files (agent run outputs, evaluation artifacts) that are gitignored. find counts all files on disk; git ls-files only counts tracked files.
  chosen value: 4,918 (git ls-files) — only tracked files are in-scope for this audit. Untracked build artifacts are ephemeral and excluded per SCOPEBOUNDARIES.
---
SUMMARY
2 CRITICAL findings (hardcoded password + SQL injection in eval benchmark test data). 1 HIGH (os.system call). 2 MEDIUM (.gitignore gap, no env-var pattern). The eval benchmark files are test/validation fixtures — they are committed intentionally as test targets for the code-review evaluation pipeline. Their presence is deliberate (the quality_gates.py scanner uses similar patterns to validate agents). However, the .gitignore gap and absence of env-var patterns across the full codebase are genuine hardening deficiencies.