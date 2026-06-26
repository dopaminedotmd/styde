FEEDBACK ANALYSIS: 20260626-183610 (score: 80.8/100)
BINDING CONSTRAINT: completeness at 65/75
Cause: output-length truncation of third mockup (150-line budget insufficient for 3 spatial dashboards)
FIXES REQUIRED (ordered by impact):
Fix 1 — BLUEPRINT.md: add output budget enforcement to Workflow Step 2
  - Add: Each mockup capped at 400 lines. If projected output exceeds 65% of remaining budget, write excess mockups to separate files instead of inline.
  - Stage: Generation
Fix 2 — config.yaml: raise maxtokens to 16000
  - Stage: Generation
  - Current: likely 8192 or default. Floor must be 16000.
  - Provider: deepseek supports up to 32000 for this model
Fix 3 — persona.md: add self-monitoring instruction
  - Insert after line about glass/atmosphere: Before emitting any artifact, check remaining output budget. Below 40%, switch to file writes for remaining mockups.
  - Stage: Generation
Fix 4 — BLUEPRINT.md: resolve contradictions
  - Remove YAML-only constraint from Step 4 (conflicts with HTML write in Step 3)
  - Set temperature: 0.1 in config.yaml (currently unspecified, drift risk)
  - Fix one-shot example in Workflow preamble to match actual multi-step flow
  - Stage: Gate
Fix 5 — BLUEPRINT.md: add evaluation gate section
  - Add subsection: Evaluation Gate Criteria
  - pass: all 3 mockups present, CSS validates, glass layers render distinct
  - fail: missing mockup, truncated output, flat/no-depth appearance
  - fallback: on fail, write remaining mockups as standalone .html files with inline styles
  - Stage: Gate
Fix 6 — BLUEPRINT.md: add pipeline stage tags to each workflow step
  - Step 1: (Generation) analyse brief
  - Step 2: (Generation) sketch concepts
  - Step 3: (Generation) implement HTML/CSS
  - Step 4: (Generation, Gate) produce minimum 3 files
  - Step 5: (Gate) pre-output validation
  - Step 6: (Gate) CSS architecture constraint
  - Step 7: (Gate) verify-preflight
  - Step 8: (Evaluation) review mockups
  - Step 9: (Promotion) deliver files
Fix 7 — persona.md: deduplicate self-monitoring rules
  - Remove rules already in blueprint constraints section
  - Replace with: see BLUEPRINT.md section "Evaluation Gate Criteria" for output rules
  - Stage: Promotion
PREDICTED SCORE AFTER FIXES: 89/100 (crosses 85 production threshold)
CRITICAL PATH:
Fix 1 (output budget) + Fix 4 (contradictions) + Fix 5 (eval gates) = +10 points
Fix 2 (maxtokens) + Fix 3 (self-monitor) = secondary, prevents regression
Fix 6 (tags) + Fix 7 (dedup) = marginal, completes polish
RUNTIME ORDER:
apply fix 2 (config.yaml) → fix 3 (persona.md) → fix 1 (blueprint generation) → fix 4 (blueprint contradictions) → fix 5 (blueprint eval gates) → fix 6 (blueprint stage tags) → fix 7 (persona dedup)
Total file edits: 3 files, 9 patch operations. Estimated 2 forge cycles.