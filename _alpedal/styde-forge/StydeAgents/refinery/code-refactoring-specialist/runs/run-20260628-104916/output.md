Now I have the full picture. BLUEPRINT.md (v10.2.0) and persona.md are stale — config.yaml shows v12.1.0 but the .md files haven't been updated with the changes from feedback entries 20260628-104215 (79.0) and 20260628-104800 (84.4). FEEDBACK.md already records them.
Below is the complete delta — what needs to change in each file, with anchors and evidence.
---
Pending changes from FEEDBACK.md entries currently NOT reflected in BLUEPRINT.md or persona.md:
Entry: 20260628-104215 (score: 79.0)
Entry: 20260628-104800 (score: 84.4)
## BLUEPRINT.md changes
### 1. ANTI-PATTERN section (new section after Conventions, before Validation)
anchor: after line 35 (end of Conventions section)
mode: insertafter
change:
|## ANTI-PATTERNS
|Rules the agent MUST NOT violate:
|- Do not inline file contents when the persona requires a separate REASONING section. If the blueprint proposes a two-pass workflow, actually output two distinct sections — analysis first, patches second — not a single merged block.
|- Do not emit digests, summary tables, or verification protocol sections. Output exactly the requested data plus a one-line verdict. Redundant structure that duplicates file content is a clarity defect.
### 2. Impact scale enforcement (modify existing output validation)
anchor: line 37-46 (Validation & Verification section)
mode: replace within evidence list item 1
change: Replace "Format: `diff: {file:path, change: \"replaced X with Y\", lines: L1-L5}`." with:
"Format: `diff: {file:path, change: \"replaced X with Y\", lines: L1-L5}`. Impact labels MUST use a numeric or ordinal scale (1-5 or none/low/medium/high/critical). Validate this in the post-processing step — any subjective label (e.g. 'significant', 'major impact') without a corresponding scale value is a format defect."
### 3. Mandatory pre-read step (new section after Edge Cases and Ambiguities)
anchor: after line 72 (end of Edge Cases and Ambiguities section)
mode: insertafter
change:
|## Evaluation Workflow
|1. **Mandatory pre-read**: Before evaluating any item, read ALL referenced files (depend-on-current-version, etc.) via terminal/read_file — do not defer or skip. A pre-read is not optional; skipping it is a completeness violation.
|2. **Structured analysis first**: Output a structured analysis first (dimensions assessed, gap found, fix rationale), then emit patch commands in a section prefixed with `# PATCHES`. This is the REASONING → ACTION two-pass rule.
|3. **Completeness gate**: After writing findings, verify that every evaluation item has a corresponding finding. If any item was deferred, mark it as 'incomplete' and explain why. If any item is missing a finding, the output fails the completeness gate.
### 4. Explicit path references (modify output template finding format)
anchor: lines 74-79 (Diff and Reproduction Guidance section)
mode: replace
change:
|## Diff and Reproduction Guidance
|For every improvement or change:
|- Include a `diff` sub-field with the exact text changed (or reference to a patch block). References MUST use explicit file paths and line numbers — NOT vague names like 'depend-on-current-version' or 'config file'. Format: `diff: {file: "StydeAgents/blueprints/code-refactoring-specialist/config.yaml", anchor: "version_history -> [0].reason", mode: "replace", change: "replaced X with Y"}`.
|- Include a `reproduction` sub-field with commands or steps to verify the fix.
|- Include a `validation` sub-field with the evidence type and result (lint pass, build green, eval delta). Evidence entries MUST reference a specific eval suite filename (e.g., `gsm8k.yaml` or `human_eval_v2.json`) — not a vague category like 'math' or 'coding'.
|- Include a `measured` sub-field with before/after numeric scores where applicable. Do not use speculative impact estimates like 'likely improves performance'. Use 'pylint score: 8.2 -> 9.1' or 'eval score: 89.8 -> 91.0'.
|- Impact labels in all change entries MUST use numeric/ordinal scale (1-5 or none/low/medium/high/critical). Subjective qualifiers without scale mapping are defects.
## persona.md changes
### 5. No-defer constraint
anchor: after line 2 (after the existing Language consistency rule)
mode: insertafter
change:
|Completeness rule: Never defer a finding item unless the source file is inaccessible (404, permission denied, network error). Deferred items count as incomplete and reduce the composite score. If you must defer, output the item marked as 'DEFERRED: <reason>' — do not silently skip it.
### 6. CONSISTENCY dimension in quality gate
anchor: after line 6 (after Decision-making bullet)
mode: insertafter
change:
|- CONSISTENCY: Before writing patches, verify all self-imposed rules (score completeness, section requirements, label standards) are followed in the same output. Every rule the agent imposes on itself must be satisfied in the output it produces. Self-contradiction (e.g. requiring a REASONING section but inlining content) is a USEfulness defect.
### 7. Reasoning-first gate
anchor: after line 9 (after Priority bullet)
mode: insertafter
change:
|- Pre-patch gate: Before writing patches, I have produced the structured analysis (not just internal reasoning). The analysis section must exist in the output before any patch block. Output order: analysis → # PATCHES → verification.
---
## config.yaml changes
### 8. Bump version
anchor: blueprint.version
mode: replace
change: version: 12.2.0
### 9. Add version_history entry (at TOP of list, newest first)
anchor: version_history -> before entry 0 (insert at top)
mode: insertbefore
change:
|- from: 12.1.0
  to: 12.2.0
  reason: 'MINOR: teacher feedback applied — added ANTI-PATTERN section, impact scale validation, mandatory pre-read step, completeness gate, explicit path references in BLUEPRINT.md; added no-defer constraint, CONSISTENCY dimension, reasoning-first gate in persona.md'
  score: null
  previous_score: 84.4
  timestamp: '2026-06-28T15:00:00Z'
---
Verification protocol:
- diff: verify each anchor above maps to correct insertion point in target files
- compile: run `python -m py_compile` on any changed .py files (none changed)
- import: N/A (no Python files changed)
- eval re-score: re-run teacher evaluation on code-refactoring-specialist blueprint; expected delta: 84.4 -> 86+ (all changes address documented weaknesses)
- smoke test: after applying, run `grep -c "ANTI-PATTERNS\|Mandatory pre-read\|Completeness gate\|Never defer\|CONSISTENCY" StydeAgents/blueprints/code-refactoring-specialist/BLUEPRINT.md` — expect 3 matches; grep persona.md for "Never defer" and "CONSISTENCY" — expect 2 matches