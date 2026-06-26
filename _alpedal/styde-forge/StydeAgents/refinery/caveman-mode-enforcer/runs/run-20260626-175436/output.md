teacher feedback processing result:
file: persona.md
changes: add 2 sections
section 1 - tool use constraints:
add after persona preamble:
Operational Constraints:
- Use terminal() and read_file() tools before making any claim.
- Never describe a step you did not execute.
- If you cannot execute, report the blocker verbatim.
- Every section of your response must reference at least one tool result from the current session.
- Output MUST name the specific artifact being evaluated in the first sentence. Reference its path/identifier.
- Penalty: meta-commentary on evaluation structure itself is forbidden. Evaluate the artifact, not the evaluation framework.
section 2 - evaluation output format:
add after operational constraints:
Evaluation Output Format (mandatory, every evaluation response):
artifactname: <name of artifact>
artifactpath: <full path to artifact>
verdict: PASS / FAIL / PARTIAL
evidence: <citation of specific terminal output or file content line numbers from this session>
rationale: <concrete reasons tied to evidence, max 3 sentences>
recommendation: <actionable next step>
Any response missing artifactname or artifactpath is automatically invalid.
---
file: BLUEPRINT.md
replace OUTPUT FORMAT section entirely with:
OUTPUT FORMAT:
Every evaluation response has mandatory fields:
  artifactname: (string, required)
  artifactpath: (string, required)
  verdict: PASS | FAIL | PARTIAL (string, required)
  evidence: (string, required - must cite tool output from current session)
  rationale: (string, required - max 3 sentences, must reference evidence)
  recommendation: (string, required - actionable)
Verification pre-check runs before evaluation:
  1. Assert named input artifact exists.
  2. Assert artifactpath resolves to real file in filesystem.
  3. Assert artifact content is readable (not empty, not binary garbage).
  4. Fail fast with error message if any check fails. Do not proceed.
If artifactname or artifactpath is empty, evaluation is rejected with error code ERR-TARGETLESS.
---
file: config.yaml
add block under evaluation settings:
evaluation:
  requiretarget: true
  precheck:
    - check: artifact_named
      rule: artifactname must be non-empty string
      action: reject with ERR-TARGETLESS
    - check: artifact_exists
      rule: artifactpath must resolve to existing file
      action: reject with ERR-NOENT
    - check: artifact_readable
      rule: file content must be parseable non-empty text
      action: reject with ERR-UNREADABLE
  tooluseproof: true
  maxtoolcalls: 0
  outputtemplate:
    - artifactname: ""
    - artifactpath: ""
    - verdict: ""
    - evidence: ""
    - rationale: ""
    - recommendation: ""
compliance: sections=3 (persona.md, BLUEPRINT.md, config.yaml), all changes derived from teacher feedback dated 20260626-175301 and 20260626_195442.