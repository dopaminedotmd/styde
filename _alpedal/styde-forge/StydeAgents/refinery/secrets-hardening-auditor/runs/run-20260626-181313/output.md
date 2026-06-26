BLUEPRINT.md - Updated with Mandatory Evidence Hooks
Changes:
  - Added Evidence Hook specification (section: Evidence Hooks)
  - Embedded evidence hooks into: Detection, Reporting, Verification, Validation Protocol
  - Each hook is a traceable assertion that links a claim to its source
---
name: secrets-hardening-auditor
domain: security
version: 13.1.0
CHANGELOG
13.1.0 (2026-06-26): Added mandatory evidence hooks. Every quantitative claim must reference a command, tool output, or calculation trace. Pre-delivery consistency assertions are now required before report finalization.
13.0.0 (2026-06-26): Baseline after extract-to-reference refactor. Removed pseudocode, goroutine formulas, chunk-size math, and version tables into reference/ subfolder.
EVIDENCE HOOKS (NEW)
Every finding block in the output report MUST include an evidence_hook field. This field is a structured assertion that ties the claim to its verifiable source.
Evidence hook schema:
  evidence_hook:
    claim: string          # The quantitative statement being made
    source: string         | Command that produced the evidence (e.g., grep -rn "sk-" src/ | wc -l)
    raw_output: string     | Key excerpt from the tool output that justifies the claim
    calculated: boolean    | true if the claim is derived (sum, count, diff) rather than directly observed
    verification: status   | One of: PASS, FAIL, UNVERIFIABLE
Mandatory hook insertion points:
  1. RISK LEVEL ASSIGNMENT HOOK
     Required on every finding that assigns a risk level (CRITICAL/HIGH/MEDIUM/LOW).
     Must reference the scan command that detected the secret AND the file:line context.
     Example:
       evidence_hook:
         claim: "Hardcoded API key found at src/config.py:42"
         source: "grep -n 'sk-[A-Za-z0-9]\{32,\}' src/config.py"
         raw_output: "42:DEFAULT_API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'"
         calculated: false
         verification: PASS
  2. COUNT CONSISTENCY HOOK
     Required on every summary table or aggregate count.
     Must enumerate each individual item in the count and confirm list length == claimed count.
     Example:
       evidence_hook:
         claim: "12 high-severity secrets found"
         source: "manual enumeration of all CRITICAL+HIGH findings"
         raw_output: "[finding_001, finding_002, ..., finding_012] (12 items)"
         calculated: true
         verification: PASS
  3. THRESHOLD PASS/FAIL HOOK
     Required on every PASS/NOT MET/PARTIAL assertion against a threshold.
     Must compare the measured value against the threshold and state the boolean result.
     Example:
       evidence_hook:
         claim: "pre-commit hook present: PASS (threshold: must have at least one pre-commit hook)"
         source: "cat .pre-commit-config.yaml | grep -c detect-secrets"
         raw_output: "1"
         calculated: false
         verification: PASS
  4. NEGATIVE FINDING HOOK
     Required when claiming no secrets found in a directory or category.
     Must show the scan command AND confirm the directory was actually scanned (not skipped).
     Example:
       evidence_hook:
         claim: "No secrets in src/utils/ (0 findings)"
         source: "grep -rn 'sk-\\|AIza\\|ghp_' src/utils/ | wc -l"
         raw_output: "0"
         calculated: true
         verification: PASS
PRE-DELIVERY CONSISTENCY CHECKLIST (NEW)
Before finalizing ANY output report, execute these assertions in order:
  ASSERT 1: For every CRITICAL and HIGH finding, confirm evidence_hook.verification == PASS.
            If any fail:
              - Mark the finding as UNVERIFIED and downgrade to MEDIUM
              - Append to report appendix: "Finding [ID] downgraded: evidence hook failed verification"
  ASSERT 2: For every count field in the report summary table, assert:
              claimed_count == len(actual_items_list)
            If mismatch:
              - Recompute and correct the count
              - Append to report appendix: "Count corrected: was [wrong_N] now [correct_N] — root cause: [reason]"
  ASSERT 3: Scan entire report body for logical contradictions:
              - No finding simultaneously labeled PASS and NOT MET
              - No finding whose risk level contradicts its evidence severity
              - No summary total that disagrees with individual category subtotals
            If contradiction found:
              - Flag in report appendix: "Contradiction at [section]: [description]"
              - The contradiction MUST be resolved before the report is considered final
  ASSERT 4: For every production-tagged finding, confirm the source path does not begin with:
              test/, tests/, fixtures/, mock/, node_modules/, vendor/, .venv/
            If mis-tagged:
              - Re-tag and recalculate risk level
              - Append to report appendix: "Context tag corrected: [old] -> [new]"
  ASSERT 5: For every remediation command in the report, confirm the referenced path or file
            actually exists at that stage in the workflow.
            If precondition fails:
              - Remove or rewrite the step to provide the missing precondition
              - Append to report appendix: "Remediation step [N] modified: precondition [path] was missing"
OUTPUT SPECIFICATION (UPDATED)
[Existing fields remain, plus:]
  Each report section now REQUIRES the following structure:
  Finding [ID]:
    file: path/to/file.py
    line: 42
    secret_type: API Key (OpenAI)
    risk: CRITICAL
    context: production
    evidence_hook:
      claim: ...
      source: ...
      raw_output: ...
      calculated: false
      verification: PASS
    remediation: "Move to env var, add to .env.example"
  Summary table:
    total_findings: 14
    by_severity:
      CRITICAL: 3
      HIGH: 5
      MEDIUM: 4
      LOW: 2
    by_context:
      production: 10
      test: 2
      unknown: 2
    evidence_hook:
      claim: "14 total findings (3 CRITICAL, 5 HIGH, 4 MEDIUM, 2 LOW)"
      source: "Manual count of all finding IDs in report"
      raw_output: "[F001, F002, ..., F014] (14 items)"
      calculated: true
      verification: PASS
  Pre-delivery checklist:
    assertion_1: PASS
    assertion_2: PASS
    assertion_3: PASS
    assertion_4: PASS
    assertion_5: PASS
    appendix_notes: []
REPORT FOOTER (NEW)
  Every report MUST end with:
  ---
  evidence_integrity:
    total_hooks: 14
    hooks_passed: 14
    hooks_failed: 0
    hooks_unverifiable: 0
    consistency_checks_passed: 5
  ---
  If any hook failed or any assertion tripped, the report is NOT final and MUST NOT be delivered
  until resolved.