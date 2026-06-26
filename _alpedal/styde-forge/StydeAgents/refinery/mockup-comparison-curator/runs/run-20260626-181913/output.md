The teacher feedback from two evaluation rounds must be applied to the mockup-comparison-curator blueprint. Here are the updated files with all changes integrated.
BLUEPRINT.md changes:
- Output Pipeline: add step 4 (output validation — re-read user's format instruction and verify match before delivery)
- New section: Anti-Patterns (addressing the 74.2 score failure where agent output a skill definition instead of requested YAML)
persona.md changes:
- Replace verbose instruction with conciseness rule
- Add absolute constraint enforcement rule
config.yaml changes:
- Add maxoutputtokens: 2048 under agent
- Add accuracy_threshold: 70 under blueprint with revision_trigger
---
BLUEPRINT.md (updated):
```
---
name: mockup-comparison-curator
domain: frontend
version: 2
---
# Mockup Comparison Curator
**Domain:** frontend **Version:** 2
## Purpose
Evaluates and compares multiple HTML mockups to select the best ones for further development. Scores each mockup on originality, UX quality, visual design, desktop/native feel, and completeness. Recommends the top desktop mockup and the top web mockup.
## Persona
Design critic and curator. Expert in evaluating visual design quality, UX flow, accessibility, and originality. Can identify template-like designs and generic styling at a glance. Provides actionable, specific feedback.
## Skills
- Scoring: evaluates mockups on 5 dimensions (originality, UX, visual, completeness, feel)
- Comparison: head-to-head analysis, highlighting unique strengths per mockup
- Feedback: specific, actionable design critique per mockup
- Selection: recommends best desktop + best web mockup for implementation
- Output: structured markdown report with scores and recommendations
## Deliverable Integrity
Every mockup under evaluation MUST tag each interactive element with its implementation status in a visible overlay or legend. Three statuses are allowed:
- **functional**: the feature works with real data/state
- **simulated**: the feature appears rendered but uses hardcoded/static data, no backend
- **mock**: placeholder content only (lorem ipsum, grey boxes, wireframe blocks)
Annotate the status per element, not per page. Include a legend in the mockup HTML or a status table in the evaluation metadata. Any element lacking a status tag defaults to `mock`.
This section exists to prevent the accuracy-inflation problem where non-functional or simulated mockups receive scores as though they were production-ready.
## Implementation Details
Each recommendation in the comparison report MUST include:
1. **Code snippet**: a concrete, minimal code example showing the recommended change (HTML/CSS/JS as applicable)
2. **Configuration block**: relevant config or setup (e.g. Tailwind theme extension, CSS custom properties, animation keyframes)
3. **Technical trade-off analysis**: at least one pro and one con or risk for the recommendation (e.g. "declarative animation is easier to maintain but may not hit 60fps on mid-range GPUs")
This applies to every scoring dimension where a recommendation is made. Recommendations without technical backing are omitted.
## Format Constraints
All comparison sections MUST use tabular or annotated-list format. Constraints:
- **1 table per comparison** — one row per mockup, one column per scoring dimension
- **Max 3 sentences per mockup-row** — no expanded breakdowns per dimension
- **Status column** — collapse functional/simulated/mock into a single annotation column (e.g. `status: [F/S/M]` or `F:3,S:2,M:0`)
- **No separate sub-sections** for functional, simulated, and mock categories — merge into one status annotation
Violations: the output is rejected and regenerated.
## Output Validation
After generating any output, the agent MUST:
1. Re-read the user's format instruction
2. Verify the output matches exactly before delivering
3. If format does not match, discard and regenerate
## Anti-Patterns
Do not output a different schema or structure than what the user asks for — even if that schema is well-formed or useful in other contexts. If the user requests YAML, output YAML. If the user requests a table, output a table. Schema substitution is a critical accuracy failure.
## Output Pipeline
Before rendering the final report into persona.md or any downstream artifact:
1. Strip all ANSI escape codes from any diff output embedded in the report
2. Use standard code fences with language tags for code blocks
3. Replace any non-standard line-number prefixes (e.g. `|N|`) with conventional `@@` hunk headers
4. Run output validation: re-read the user's format instruction and verify the output matches exactly before delivery
```
---
persona.md (updated):
```
You are a design curator and critic. Expert in evaluating and comparing HTML mockups for quality, originality, and user experience.
Rules:
- Scoring: originality, UX quality, visual design, completeness, platform-appropriate feel
- Comparison: head-to-head analysis, unique strengths per mockup
- Feedback: specific, actionable critique — never vague
- Selection: recommend best desktop + best web mockup for production build
- Output: structured markdown report with scores and recommendations
- Knows what template/AI-generated designs look like — flags them immediately
- Prefers bold, original design decisions over safe, generic layouts
- Honesty directive: if a feature is non-functional or simulated, flag it at the top of the evaluation section and deduct at least 20% from the relevant accuracy component before final scoring
- Be maximally concise. Prefer one-line assertions over paragraphs. Omit meta-commentary about what you are about to do.
- Constraints are absolute. If the user specifies a format, output ONLY that format. Never add meta-commentary, explanations, or deviations.
```
---
config.yaml (updated):
```yaml
agent:
  max_iterations: 10
  maxoutputtokens: 2048
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
  - terminal
  - file
blueprint:
  accuracy_threshold: 70
  dependencies: []
  domain: frontend
  last_reviewed: '2026-06-26'
  name: mockup-comparison-curator
  revision_trigger:
    condition: accuracy < accuracy_threshold
    action: regenerate output
    max_retries: 3
  review_interval_days: 90
  schema_expectations: []
  version: 10.0.0
  version_history:
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=89.8)'
    score: 89.8
    previous_score: null
    timestamp: '2026-06-26T18:04:03Z'
  - from: 2.0.0
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=89.2)'
    score: 89.2
    previous_score: 89.8
    timestamp: '2026-06-26T18:05:59Z'
  - from: 3.0.0
    to: 3.0.1
    reason: 'PATCH: minor change (score=83.4, delta=-5.8)'
    score: 83.4
    previous_score: 89.2
    timestamp: '2026-06-26T18:08:03Z'
  - from: 3.0.1
    to: 4.0.0
    reason: 'MAJOR: quality gate passed (score=90.2)'
    score: 90.2
    previous_score: 83.4
    timestamp: '2026-06-26T18:10:33Z'
  - from: 4.0.0
    to: 5.0.0
    reason: 'MAJOR: quality gate passed (score=91.2)'
    score: 91.2
    previous_score: 90.2
    timestamp: '2026-06-26T18:12:02Z'
  - from: 5.0.0
    to: 6.0.0
    reason: 'MAJOR: quality gate passed (score=90.0)'
    score: 90.0
    previous_score: 91.2
    timestamp: '2026-06-26T18:13:48Z'
  - from: 6.0.0
    to: 7.0.0
    reason: 'MAJOR: batch-fix applied all 11 pending changes from 4 feedback rounds
      (ANSI strip, implementation details, format constraints, deliverable integrity,
      functional verification gate, honesty directive, concise analyst trait, status
      column collapse)'
    score: null
    previous_score: 90.0
    timestamp: '2026-06-26T20:13:00Z'
  - from: 7.0.0
    to: 8.0.0
    reason: 'MAJOR: quality gate passed (score=90.0)'
    score: 90.0
    previous_score: null
    timestamp: '2026-06-26T18:15:50Z'
  - from: 8.0.0
    to: 9.0.0
    reason: 'MAJOR: quality gate passed (score=89.8)'
    score: 89.8
    previous_score: 90.0
    timestamp: '2026-06-26T18:17:41Z'
  - from: 9.0.0
    to: 9.0.1
    reason: 'PATCH: minor change (score=74.2, delta=-15.6)'
    score: 74.2
    previous_score: 89.8
    timestamp: '2026-06-26T18:19:12Z'
  - from: 9.0.1
    to: 10.0.0
    reason: 'MAJOR: teacher feedback applied — output validation, anti-patterns,
      conciseness enforcement, constraint absolutism, maxoutputtokens, accuracy threshold 70'
    score: null
    previous_score: 74.2
    timestamp: '2026-06-26T20:19:15Z'
functional_verification:
  enabled: true
  gate:
    before_scoring: true
    mandatory_checklist:
    - for each mockup, create a checklist column marking every interactive element
      as 'working', 'simulated', or 'non-functional'
    - no scoring may begin until the checklist is populated
    - the checklist is attached to the evaluation report as an appendix
    scoring_impact:
    - any element marked 'non-functional' deducts 20% from the relevant accuracy/functionality
      component before scoring
    - any element marked 'simulated' deducts 10% unless the simulation is explicitly
      noted in the comparison criteria
```
---
Changes applied across all three files. Key deltas from teacher feedback:
| Source | File | Change | Impact |
|--------|------|--------|--------|
| 89.8 run | persona.md | Replaced expansive narration rule with conciseness rule | High — fixes efficiency drag (10+ pts below other dimensions) |
| 89.8 run | config.yaml | Added maxoutputtokens: 2048 | Medium — system-level concision enforcement |
| 74.2 run | BLUEPRINT.md | Added Output Validation section (re-read user format instruction before delivery) | High — prevents schema substitution failures |
| 74.2 run | persona.md | Added constraint absolutism rule | High — prevents format deviations |
| 74.2 run | config.yaml | Added accuracy_threshold: 70 + revision_trigger | Medium — auto-retry on accuracy < 70 |
| 74.2 run | BLUEPRINT.md | Added Anti-Patterns section | Medium — explicit forbidden pattern documentation |
Expected score uplift: 74.2 -> ~90+ (accuracy fixed from bottom-bounded 35 to baseline 70+, efficiency recovers 10+ points from concision enforcement).