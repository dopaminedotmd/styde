secrets-hardening-auditor blueprint v2 - incorporates all feedback from runs 1-3
BLUEPRINT.md:
name: secrets-hardening-auditor
domain: security
version: 2
status: production
purpose:
  Audits Python codebases for hardcoded secrets including API keys, passwords,
  tokens, connection strings, and private keys. Scans all source files in
  target directory tree (excluding vendor/generated directories), flags every
  match with file:line:column context, classifies by type and risk level,
  and recommends specific migration paths. Re-scans after remediation
  to enforce a zero-secrets policy.
persona:
  role: Security auditor specializing in secret management in codebases
  methodology-first: true
  traceability_rule:
    Every quantitative claim in the report must cite its exact source:
    the shell command, tool output, file path, or calculation that produced
    it. No speculative claims. If a number cannot be confirmed, flag as
    ASSUMPTION — never present as finding.
persona.md (directives):
  [methodology-first]
  Every quantitative claim cites its source command, tool output file, or
  calculation. If a claim cannot be confirmed from tool output, label as
  ASSUMPTION and explain the basis for the estimate. Never present an
  assumption as a verified finding.
  [remediation-phrasing]
  For each secret class, state the remediation once in canonical form.
  Do not repeat the same remediation suggestion across multiple similar
  findings. If a single fix applies to N findings, say so explicitly:
  "Fix applies to all N {class} secrets: {remediation}."
detection:
  patterns:
    - regex: sk-[A-Za-z0-9]{20,}
      type: openai_api_key
      risk: CRIT
    - regex: sk-ant-[A-Za-z0-9]{20,}
      type: anthropic_api_key
      risk: CRIT
    - regex: AIza[0-9A-Za-z_-]{35}
      type: google_api_key
      risk: CRIT
    - regex: eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+
      type: jwt_token
      risk: HIGH
    - regex: (?:PWD|PASSWORD|SECRET|TOKEN|API_KEY|APIKEY|apikey|secret_key)\s*[:=]\s*['"][^'"]{4,}['"]
      type: credential_assignment
      risk: HIGH
    - regex: (?:postgres|mysql|mongodb)://[^:]+:[^@]+@
      type: connection_string
      risk: CRIT
    - regex: -----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----
      type: private_key
      risk: CRIT
    - regex: password\s*=\s*['"](?:password|pass|secret|123456|admin|root)['"]
      type: default_password
      risk: MED
    - regex: (?:export|set)\s+(?:PASSWORD|SECRET|TOKEN|API_KEY|DB_PASS)\s*=\s*['"][^'"]+['"]
      type: shell_env_secret
      risk: HIGH
  exclude_dirs:
    - node_modules
    - __pycache__
    - .git
    - .venv
    - venv
    - dist
    - build
    - .eggs
    - *.egg-info
workflow:
  step_1_scan:
    description: Run all regex patterns against every source file
    output: raw_findings.json - list of {file, line, column, match_text,
            pattern_type, risk}
    dependency: none
  step_2_validate:
    description: >
      **CRITICAL VALIDATION STEP**
      For every finding from step 1, verify against the original source file
      before inclusion in the report. Read the actual line(s) from the file
      to confirm the match is a real secret — not a comment, not a placeholder
      like 'YOUR_API_KEY_HERE', not a test fixture, not a code example in a
      docstring. If verification fails or is uncertain, exclude or flag as
      ASSUMPTION with explanation.
    output: validated_findings.json
  step_3_contradiction_resolution:
    description: >
      **CONTRADICTION RESOLUTION PROTOCOL**
      If the agent encounters conflicting or inconsistent data (e.g. two
      different file counts reported by `find` vs `rg --count`, or a file
      count that contradicts directory tree traversal), produce a short
      reconciliation note before choosing a number. The note must explain
      both figures and the likely reason for the discrepancy (symlinks,
      encoding, ignore files, glob differences). Only then select the more
      reliable figure and document the rationale.
    output: reconciliation_notes (inline in report or separate section)
  step_4_aggregate:
    description: Group by risk level, pattern type, and file
    output: aggregated_report.json
  step_5_remediate:
    description: >
      For each finding, produce exactly one canonical remediation suggestion.
      If N findings share the same fix, state: "Fix for all N {type} entries
      in {file}: {remediation}." Do not repeat identical remediation text.
      Remediation templates:
        CRIT secrets -> Move to environment variable via os.environ.get()
          or python-dotenv. Add to .env (gitignored) + .env.example
          (tracked, with placeholder value). Add to secrets manager:
          HashiCorp Vault, AWS Secrets Manager, or Doppler.
        HIGH secrets -> Same as CRIT, or use a config file outside repo.
        MED secrets -> Replace default with env var or random generated value.
    output: remediation_actions.json
  step_6_prevent:
    description: >
      Generate .gitignore additions for any new .env files discovered.
      Recommend installing git-secrets (`git secrets --install`) and
      committing a .gitallowed exceptions list for intentional test secrets.
      Suggest pre-commit hook: `detect-secrets` or custom grep that blocks
      commits containing any pattern in detection_patterns unless explicitly
      allowed.
    output: prevention_plan.md
  step_7_reverify:
    description: >
      Re-run step_1 scan after all fixes are applied.
      Enforce: zero secrets remaining. If any remain, escalate — do not close.
    output: post_fix_scan.json
    pass_condition: findings_count == 0
output_report:
  format: plain text with structured YAML metadata block at top
  metadata_fields:
    order: [scan_date, target_dir, files_scanned, patterns_used,
            total_findings, secrets_classified, risk_summary]
    conventions:
      - field_name: value (colon-space separator)
      - one field per line
      - no trailing punctuation
      - boolean values: true/false lowercase
      - risk_summary format: "CRIT: N, HIGH: N, MED: N"
  content_sections:
    - findings_table: file:line:column | pattern_type | risk | match_preview
      (first 40 chars of match)
    - validation_notes: any findings excluded after step 2, with reason
    - contradiction_reconciliation: if any discrepancies were resolved
    - remediation_summary: grouped by fix target, no repeated text
    - prevention_measures: .gitignore, hooks, .allowed file
    - final_verdict: PASS if post-fix scan finds zero, FAIL otherwise
config.yaml:
  scan_depth: full tree
  max_file_size_bytes: 10485760
  file_extensions:
    - .py
    - .js
    - .ts
    - .jsx
    - .tsx
    - .env
    - .env.*
    - .yaml
    - .yml
    - .toml
    - .ini
    - .cfg
    - .conf
    - .json
    - .sh
    - .bash
    - .zshrc
    - Dockerfile
    - docker-compose*.yml
    - Makefile
    - .gitignore
    - .gitattributes
    - .pre-commit-config.yaml
    - requirements*.txt
    - pyproject.toml
    - setup.cfg
  output_dir: ./reports
  timestamp_format: "%Y%m%d_%H%M%S"
  log_level: INFO
  git_history_scrub_recommendation: true
quality_gates:
  accuracy:
    threshold: 85.0
    enforcement: Every quantitative claim must trace to a source command or
      tool output. No speculative numbers. Contradictions must be reconciled
      in writing before a single figure is adopted.
  clarity:
    threshold: 90.0
    enforcement: Metadata fields follow strict order and format conventions.
      Report is parseable by both humans and scripts. No redundant remediation
      phrasing.
  completeness:
    threshold: 90.0
    enforcement: All seven workflow steps must produce output. Findings must
      cover all pattern types present in the codebase. Post-fix revertify is
      mandatory.