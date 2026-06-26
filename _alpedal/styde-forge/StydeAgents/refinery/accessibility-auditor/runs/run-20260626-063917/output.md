Tva feedback-rundor identifierar samma rotorsak: blueprinten deklarerar närvaro men producerar inget arbete. Har läst in båda rapporterna och nuvarande filer. Agerar som Accessibility Auditor. Resultat:
--- Resolverade ändringar ---
BLUEPRINT.md — ersätt hela innehållet med:
# Accessibility Auditor  
Domain: design Version: 2  
## Purpose  
Audits and fixes web accessibility. WCAG 2.2 AA/AAA, screen readers, keyboard navigation, semantic HTML.  
## Task  
You are given a target web page URL or HTML file. Your job is to produce a WCAG 2.2 AA compliance audit and, where violations are found, apply fixes.  
Role: Accessibility Auditor  
Goal: Identify all WCAG 2.2 AA violations on the target, rank them by severity, and produce a corrected version of the page that passes AA.  
Output artifact: `audit-output/accessibility-report.yaml` (structured violations) + `audit-output/index.fixed.html` (remediated page)  
Validation criteria:  
  - Report lists each violation with WCAG SC ID, element selector, impact, and recommended fix  
  - Fixed page passes automated check: no new violations introduced, original violations reduced by >=90%  
  - All interactive elements receive visible focus indicators  
  - All form inputs have programmatic labels  
  - All non-decorative images have alt text  
MergeStrategy: deepmerge (blueprint config merges into agent defaults; blueprint fields win on collision)  
## Persona  
Accessibility auditor. Expert in WCAG 2.2, ARIA, screen reader testing (NVDA/VoiceOver), and inclusive design.  
## Skills  
  Audit: run WCAG 2.2 compliance audits  
  ARIA: implement correct ARIA roles and attributes  
  Keyboard: ensure full keyboard operability  
  Screen: test with NVDA and VoiceOver  
  Forms: make forms accessible with labels and error messages  
---
config.yaml — uppdatera med tasktemplate och tasklifecycle:
agent:
  max_iterations: 10
  retry_on_failure: true
  timeout_seconds: 300
  toolsets:
  - terminal
  - file
  - web
blueprint:
  dependencies: []
  domain: design
  last_reviewed: '2026-06-26'
  name: accessibility-auditor
  review_interval_days: 90
  schema_expectations: []
  version: 2.1.0
  version_history:
  - from: 1.0.0
    to: 2.0.0
    reason: 'MAJOR: quality gate passed (score=92.4)'
    score: 92.4
    previous_score: null
    timestamp: '2026-06-25T23:00:50Z'
  - from: 2.0.0
    to: 2.0.1
    reason: 'PATCH: minor change (score=81.2, delta=-11.2)'
    score: 81.2
    previous_score: 92.4
    timestamp: '2026-06-26T00:45:52Z'
  - from: 2.0.1
    to: 2.0.2
    reason: 'PATCH: minor change (score=63.2, delta=-18.0)'
    score: 63.2
    previous_score: 81.2
    timestamp: '2026-06-26T06:37:11Z'
  - from: 2.0.2
    to: 2.0.3
    reason: 'PATCH: minor change (score=51.0, delta=-12.2)'
    score: 51.0
    previous_score: 63.2
    timestamp: '2026-06-26T06:38:00Z'
  - from: 2.0.3
    to: 2.1.0
    reason: 'MINOR: added tasktemplate with lifecycle wiring + mergestrategy'
    score: null
    previous_score: 51.0
    timestamp: '2026-06-26T08:39:19Z'
tasktemplate:
  requiredfields:
    - target_url
    - compliance_level
  field_defaults:
    compliance_level: AA
    output_format: yaml
    include_fixes: true
    auto_validate: true
  mergestrategy: deepmerge
  validation:
    pre_run:
      - check: target_url exists and is reachable
        fail_action: prompt_user
      - check: compliance_level in [A, AA, AAA]
        fail_action: clamp_to_AA
    post_run:
      - check: report contains at least one violation or pass declaration
        fail_action: regenerate
      - check: fixed page passes axe-core or equivalent automated check
        fail_action: log_warning
tasklifecycle:
  readfrequency: once
  timeout: 600
  artifactpath: audit-output/
  artifact_naming: blueprint-{name}-{timestamp}
  iteration_limit: 3
eval:
  benchmarks: []
  judge_model: deepseek-v4-pro
  min_pass_score: 70
hardware_profiles:
  pontus-main:
    eval_model: deepseek-v4-pro
    max_tokens: 8192
    model: deepseek-v4-flash
    provider: deepseek
    temperature: 0.3
---
Sammanfattning av ändringar mot feedback:
Feedback 1 (score=63.2, completeness critical):
  - BLUEPRINT.md: ersatt enkel beskrivning med konkret task-block som specificerar role, goal, output artifact och validation criteria. Agenten får nu en exekverbar instruktion istället för en persona-bio.
  - config.yaml: lagt till tasktemplate.requiredfields som tvingar target_url och compliance_level. Inga fler tomma körningar.
Feedback 2 (score=51.0, execution gap):
  - BLUEPRINT.md: lagt till MergeStrategy: deepmerge som explicit fält. Agenten vet nu hur blueprint-config ska kombineras med agent-defaults.
  - config.yaml: lagt till tasklifecycle med readfrequency (once), timeout (600s), artifactpath (audit-output/), artifact_naming. Lagt till validation både pre_run (url reachable, level valid) och post_run (report non-empty, auto-verify fixes).
Ny version: 2.1.0, score reset i väntan på nästa eval.