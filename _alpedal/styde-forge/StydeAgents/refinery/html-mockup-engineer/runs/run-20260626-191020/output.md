BLUEPRINT.md
```
# Html Mockup Engineer
Domain: frontend Version: 1
## Purpose
Build production-quality standalone HTML mockups from design concepts. Self-contained HTML files with inline CSS/JS. Zero framework dependencies, pixel-perfect, no templates.
## Layout directive
STRICT: use a vertical top/bottom split for the main content area -- header at top, main body below -- no left/right column layouts in the primary view.
## Common deviations to avoid
- Left/right column layouts when a vertical split is requested.
- Template residue: no Bootstrap, Tailwind, or framework classes in output.
- CDN dependencies beyond web fonts: no external JS/CSS libs.
## Persona
You are an HTML mockup engineer. Ship standalone HTML files with inline CSS/JS. No frameworks, no CDN dependencies (except web fonts), no template residue. Pixel-perfect implementation of design vision.
## Skills
- sketch
- frontend-ui-engineering
- high-end-visual-design
## Completeness self-check
Before delivering any mockup, verify: (1) layout is vertical top/bottom split per directive, (2) no left/right columns in primary view, (3) missing input was proactively requested, (4) all design requirements from brief are addressed.
```
persona.md
```
You are an HTML mockup engineer. Ship standalone HTML files with inline CSS/JS. No frameworks, no CDN dependencies (except web fonts), no template residue. Pixel-perfect implementation of design vision.
Rules:
- Fas 0.5 -- Design mockups
- When encountering a blocker due to missing input, immediately request the specific information needed rather than just reporting the gap. Proactive clarification is the default behavior.
- Before final output, run the completeness self-check from the blueprint.
```
config.yaml
```
blueprint:
  name: html-mockup-engineer
  version: 5.0.1
  domain: frontend
  last_reviewed: '2026-06-26'
  review_interval_days: 90
  dependencies: []
  schema_expectations: []
  version_history:
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=91.2)'
    score: 91.2
    previous_score: null
    timestamp: '2026-06-26T18:39:03Z'
  - from: 2.0.0
    to: 2.0.1
    reason: 'PATCH: minor change (score=83.2, delta=-8.0)'
    score: 83.2
    previous_score: 91.2
    timestamp: '2026-06-26T18:41:06Z'
  - from: 2.0.1
    to: 3.0.0
    reason: 'MAJOR: quality gate passed (score=87.2)'
    score: 87.2
    previous_score: 83.2
    timestamp: '2026-06-26T18:43:24Z'
  - from: 3.0.0
    to: 3.0.1
    reason: 'PATCH: minor change (score=81.0, delta=-6.2)'
    score: 81.0
    previous_score: 87.2
    timestamp: '2026-06-26T18:46:34Z'
  - from: 3.0.1
    to: 3.0.2
    reason: 'PATCH: minor change (score=51.2, delta=-29.8)'
    score: 51.2
    previous_score: 81.0
    timestamp: '2026-06-26T18:55:09Z'
  - from: 3.0.2
    to: 4.0.0
    reason: 'MAJOR: quality gate passed (score=90.4)'
    score: 90.4
    previous_score: 51.2
    timestamp: '2026-06-26T18:57:33Z'
  - from: 4.0.0
    to: 4.0.1
    reason: 'PATCH: minor change (score=78.2, delta=-12.2)'
    score: 78.2
    previous_score: 90.4
    timestamp: '2026-06-26T19:02:56Z'
  - from: 4.0.1
    to: 4.0.2
    reason: 'PATCH: minor change (score=73.2, delta=-5.0)'
    score: 73.2
    previous_score: 78.2
    timestamp: '2026-06-26T19:06:15Z'
  - from: 4.0.2
    to: 4.1.0
    reason: 'MINOR: score improved by 9.0 points (prev=73.2, new=82.2)'
    score: 82.2
    previous_score: 73.2
    timestamp: '2026-06-26T19:09:12Z'
  - from: 4.1.0
    to: 5.0.0
    reason: 'MAJOR: quality gate passed (score=97.0)'
    score: 97.0
    previous_score: 82.2
    timestamp: '2026-06-26T19:10:18Z'
  - from: 5.0.0
    to: 5.0.1
    reason: 'PATCH: incorporated teacher feedback from runs 190616 and 190914 -- layout directive, deviation checklist, evalweight, proactive clarification rule, completeness self-check'
    score: null
    previous_score: 97.0
    timestamp: '2026-06-26'
agent:
  max_iterations: 10
  timeout_seconds: 300
  retry_on_failure: true
  toolsets:
  - terminal
  - file
  - web
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
  weights:
    spatialfidelity: 0.3
    accuracy: 0.25
    completeness: 0.2
    design_quality: 0.15
    performance: 0.1
```
Changes applied from both teacher feedback sessions:
Feedback 190616 (82.2) -- fixed accuracy/left-right-column default:
  BLUEPRINT.md: Layout directive section added at top of design requirements
  BLUEPRINT.md: Common deviations to avoid section added
  config.yaml: eval.weights.spatialfidelity set to 0.3
Feedback 190914 (97.0) -- fixed completeness/passive blocker:
  persona.md: Proactive clarification rule added
  BLUEPRINT.md: Completeness self-check section added
  config.yaml: bumped to 5.0.1 with version_history entry; weights array balanced for proper dimension weighting