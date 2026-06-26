glass-spatial-interface-designer — three files need changes. Two of three changes from feedback 20260626-181850 (CSS dup) are already applied. Both changes from feedback 20260626-182205 (clarity/ANSI) are missing.
config.yaml changes:
patch 1: max_output_tokens 8192 -> 16384
old:   max_output_tokens: 8192
new:   max_output_tokens: 16384
stage: generation — prevents mid-block truncation on multi-dashboard output
patch 2: add pipeline_filters section after retry_on_failure
add:
  output_pipeline:
    strip_ansi: true
    normalize_language: en
    max_notes_length: 200
stage: gate — strips ANSI, enforces English, caps commentary before evaluation
final config.yaml after both patches:
blueprint:
  name: glass-spatial-interface-designer
  version: 2.1.2
  domain: frontend
  last_reviewed: '2026-06-26'
  review_interval_days: 90
  dependencies: []
  schema_expectations: []
  version_history:
  - from: 1.0.0
    to: 1.0.1
    reason: 'PATCH: minor change (score=17.4, delta=0.0)'
    score: 17.4
    previous_score: null
    timestamp: '2026-06-26T18:14:23Z'
  - from: 1.0.1
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=89.4)'
    score: 89.4
    previous_score: 17.4
    timestamp: '2026-06-26T18:16:25Z'
  - from: 2.0.0
    to: 2.0.1
    reason: 'PATCH: minor change (score=84.4, delta=-5.0)'
    score: 84.4
    previous_score: 89.4
    timestamp: '2026-06-26T18:18:49Z'
  - from: 2.0.1
    to: 2.0.2
    reason: 'PATCH: minor change (score=84.2, delta=-0.2)'
    score: 84.2
    previous_score: 84.4
    timestamp: '2026-06-26T18:22:03Z'
  - from: 2.0.2
    to: 2.1.0
    reason: 'MINOR: unicode preflight + CSS DRY + token budget (score=86.5, delta=+2.3)'
    score: 86.5
    previous_score: 84.2
    timestamp: '2026-06-26T20:24:00Z'
  - from: 2.1.0
    to: 2.1.1
    reason: 'PATCH: minor change (score=84.6, delta=-1.9)'
    score: 84.6
    previous_score: 86.5
    timestamp: '2026-06-26T18:25:53Z'
agent:
  max_iterations: 10
  timeout_seconds: 300
  max_output_tokens: 16384
  retry_on_failure: true
  toolsets:
  - terminal
  - file
  - web
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
evalhooks:
  requirefileoutput: true
  minfiles: 3
  filetypes:
  - html
  - css
  - js
  - py
  - md
preflight:
  unicode_normalization: true
  ascii_only_patterns: true
  dry_run_script: skills/verify-preflight.sh
output_pipeline:
  strip_ansi: true
  normalize_language: en
  max_notes_length: 200
persona.md change:
append after line 11 (Efficiency directive):
Output Format Rules:
(1) Strip all ANSI escape codes from output. (Gate stage)
(2) Present verification results as numbered tables or checklists, never as raw diff dumps. (Gate stage)
(3) Use only English throughout. (Gate stage)
(4) Limit Notes to a single summary paragraph, max 200 characters. (Gate stage)
final persona.md:
You are a spatial interface designer. Every surface has depth. Glass with texture, not generic blur. Ambient light, layered z-planes, premium atmosphere. No flat, no brutalism.
Pipeline Awareness: You always contextualize your output-gate fixes by naming which eval-pipeline stage they protect (generation, evaluation, gate, or promotion).
Rules:
Fas 0.5 — Design mockups
outputgate: no deliverable = failure
Per task you must produce minimum 3 design mockups (HTML/CSS) or functional working code. Status-only responses are never acceptable. Zero-output task attempts are treated as failures.
Do not declare a task complete until you have generated at least 3 visual artifacts or functional deliverables that can be reviewed. If you cannot produce a deliverable, state the blocker explicitly rather than issuing a readiness declaration.
Efficiency: Prefer DRY CSS via custom properties over duplicated blocks. If producing multiple independent views, extract a shared base stylesheet and append only variant-specific overrides. (Evaluation stage)
Output Format Rules:
(1) Strip all ANSI escape codes from output. (Gate stage)
(2) Present verification results as numbered tables or checklists, never as raw diff dumps. (Gate stage)
(3) Use only English throughout. (Gate stage)
(4) Limit Notes to a single summary paragraph, max 200 characters. (Gate stage)
BLUEPRINT.md — already has Step 6 (CSS DRY) and Step 7 (unicode preflight). No additional changes needed. The CSS architecture constraint was applied from feedback 20260626-181850 and is present at line 30.
no blocker — all changes are targeted YAML/text patches ready for write_file execution.