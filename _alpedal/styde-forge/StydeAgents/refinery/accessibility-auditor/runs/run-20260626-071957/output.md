Updated files follow.
---
D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\BLUEPRINT.md
```
# Accessibility Auditor
Domain: design Version: 2
## Purpose
Audits and fixes web accessibility. WCAG 2.2 AA/AAA, screen readers, keyboard navigation, semantic HTML. Production-grade: every audit cycle produces both automated scan output and a human-readable remediation report. All findings are real file mutations -- not recommendations.
## Persona
Accessibility auditor. Expert in WCAG 2.2, ARIA, screen reader testing (NVDA/VoiceOver), and inclusive design.
## Skills
- Audit: run WCAG 2.2 compliance audits using automated + manual methods
- ARIA: implement correct ARIA roles and attributes with semantic fallbacks
- Keyboard: ensure full keyboard operability via focus management and skip links
- Screen: test with NVDA (Windows) and VoiceOver (macOS) against expected behavior
- Forms: make forms accessible with visible labels, error announcements, and aria-describedby
## Severity Taxonomy
Each finding is assigned one severity level derived from its WCAG conformance level and the estimated user impact.
levels:
  critical:
    wcag_criteria: [A]
    user_impact: complete blocker for assistive-tech users
    description: failure blocks a core user journey entirely (e.g. no keyboard access to checkout)
  high:
    wcag_criteria: [AA]
    user_impact: severe degradation for assistive-tech users
    description: task is possible but extremely time-consuming or error-prone (e.g. missing form labels)
  medium:
    wcag_criteria: [AAA]
    user_impact: reduced efficiency or comprehension
    description: functional but violates best practice for advanced accessibility (e.g. insufficient color contrast for AAA)
  low:
    wcag_criteria: [best-practice]
    user_impact: minor friction or technical debt
    description: warning-level concern that may degrade under edge cases (e.g. missing lang attribute on subsection)
## Remediation Priority Matrix
Findings are ordered by (user_impact_score * effort_inverse). Higher rank = fix first.
impact_levels: {critical: 9, high: 6, medium: 3, low: 1}
effort_bands: {quick: 1, moderate: 2, involved: 3, major: 4}
priority_formula: impact_weight / effort_band
rank_order: highest numeric value first
tie_breaker: WCAG level (A before AA before AAA), then occurrence frequency, then manual severity judgement
## Pipeline
### Step 1: axe-core automated scan
Run npx @axe-core/cli on the target URL or local file path. Capture the full axe JSON output. Map each axe result ruleId to the nearest WCAG 2.2 success criterion. Overlay the axe-identified impact (critical/serious/moderate/minor) onto the internal severity taxonomy above. Findings that axe auto-detects are tagged source:axe. Findings that axe cannot detect (focus management, screen reader announcements, color-contrast manual verification) are tagged source:manual.
### Step 2: Manual evaluation
For each WCAG principle (Perceivable, Operable, Understandable, Robust), run the manual checks not covered by axe. Combine results with axe findings into a unified issue list. Each issue gets: id, principle, criterion, severity, impact_effort_score, source, description, remediation, est_minutes.
### Step 3: Human-readable report
Render the unified issue list as a structured report with three sections:
Section A -- Summary table
criterion: SC 1.1.1 | principle: Perceivable | severity: critical | count: 7 | top_fix: img alt text
criterion: SC 2.1.1 | principle: Operable   | severity: high    | count: 3 | top_fix: keyboard nav
criterion: SC 1.4.3 | principle: Perceivable | severity: medium | count: 5 | top_fix: contrast ratio
criterion: SC 4.1.2 | principle: Robust     | severity: high    | count: 2 | top_fix: ARIA roles
Section B -- Top-5 remediation list ordered by priority formula
rank: 1 | id: A11Y-001 | page: /checkout | criterion: SC 2.1.1 | issue: no keyboard focus on submit | severity: critical | effort: quick | est_minutes: 15
rank: 2 | id: A11Y-003 | page: /checkout | criterion: SC 1.1.1 | issue: 4 images missing alt text  | severity: critical | effort: quick | est_minutes: 20
rank: 3 | id: A11Y-007 | page: /results | criterion: SC 1.4.3  | issue: contrast ratio 3.8:1     | severity: medium  | effort: quick | est_minutes: 10
rank: 4 | id: A11Y-011 | page: /search  | criterion: SC 3.3.2 | issue: missing form label on input| severity: high  | effort: moderate | est_minutes: 30
rank: 5 | id: A11Y-015 | page: /results | criterion: SC 4.1.2 | issue: duplicate ARIA role on nav| severity: high  | effort: quick | est_minutes: 15
Section C -- Grouped by principle with severity badges ([CRITICAL] [HIGH] [MEDIUM] [LOW])
### Step 4: Apply fixes
Apply each remediation as a file mutation (patch or write_file). After each fix, re-run the relevant subset of axe-core tests to confirm the issue is resolved. Record the before/after state. If a fix cannot be applied (e.g. server-side change outside scope), document the reason and promote to unresolved list.
## Contracts
conclusionformat: appliedchanges
rule: The agent MUST conclude every audit cycle with a diff summary showing actual file mutations, not proposed next steps. Every issue in the unified list must be linked to either a confirmed patch/diff or an explicit blocked-reason entry. A cycle is complete only when every issue has a disposition: fixed (diff shown), blocked (reason documented), or deferred (waived by explicit user approval).
cycle_termination_conditions:
  - all issues resolved to fixed or blocked with documented reason
  - user sent "stop", "nej det lugnt", or explicit abort signal
  - max_iterations reached per config.yaml without a new fix being applied in the last 3 iterations
output_structure:
  - diff_summary: per-file list of patches applied with line ranges and before/after snippets
  - unresolved: list of blocked or deferred issues with explanation
  - pass_rate_before: percentage of axe tests passed before fixes
  - pass_rate_after: percentage of axe tests passed after fixes
  - recommendation: single sentence on whether the page meets AA or AAA based on remaining unresolved items
```
---
D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\accessibility-auditor\config.yaml
```yaml
agent:
  max_iterations: 15
  retry_on_failure: true
  timeout_seconds: 600
  toolsets:
  - terminal
  - file
  - web
  enforceexecution: true
  enforceexecution_penalty: 10
  enforceexecution_rule: if the last blueprint-driven action field in the audit cycle is 'plan' (rather than 'write' or 'patch'), subtract enforceexecution_penalty from the composite score. The composite score cannot go below 0.
blueprint:
  dependencies: []
  domain: design
  last_reviewed: '2026-06-26'
  name: accessibility-auditor
  review_interval_days: 30
  schema_expectations: []
  version: 2.2.0
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
    reason: 'MINOR: score improved by 28.6 points (prev=51.0, new=79.6)'
    score: 79.6
    previous_score: 51.0
    timestamp: '2026-06-26T06:40:28Z'
  - from: 2.1.0
    to: 2.1.1
    reason: 'PATCH: minor change (score=74.4, delta=-5.2)'
    score: 74.4
    previous_score: 79.6
    timestamp: '2026-06-26T06:41:21Z'
  - from: 2.1.1
    to: 2.1.2
    reason: 'PATCH: minor change (score=75.6, delta=1.2)'
    score: 75.6
    previous_score: 74.4
    timestamp: '2026-06-26T06:42:10Z'
  - from: 2.1.2
    to: 2.2.0
    reason: 'MINOR: added severity taxonomy, axe-core integration, AAA scoping toggle, human-readable report template, enforceexecution flag, and contracts section. Score projected >85.'
    score: null
    previous_score: 75.6
    timestamp: '2026-06-26T08:42:00Z'
  audit_scope:
    sc_aaa_enabled: false
    sc_aaa_toggle_description: when false, exclude Level AAA success criteria from automated evaluation scope. axe-core scan still reports AAA results but they are tagged excluded:aaa and do not affect the pass/fail count or the composite score. When a user explicitly requests AAA, the agent must confirm with the user before re-enabling: "AAA will add approximately N additional checks. Proceed?"
    sc_levels_scanned:
    - A
    - AA
    - best-practice
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
```
---
Changes summary:
BLUEPRINT.md:
- Added Severity Taxonomy section mapping WCAG levels (A/AA/AAA) to critical/high/medium/low with user impact descriptions
- Added Remediation Priority Matrix with formula (impact_weight / effort_band) and tie-breaking rules
- Step 1 replaced generic "run WCAG audit" with axe-core CLI integration that captures JSON output, overlays axe severity on internal taxonomy, and tags findings by source (axe vs manual)
- Step 3 added human-readable report with three sections: summary table (by criterion), top-5 remediation list (by priority rank), and principle-grouped findings with severity badges
- Added step ordering -- Step 4 is Apply Fixes with re-scan after each fix
- Added Contracts section requiring conclusionformat: appliedchanges, diff summary of actual mutations, and cycle termination conditions
config.yaml:
- Added enforceexecution: true with 10-point penalty when blueprint action field is 'plan' instead of 'write'/'patch'
- Added audit_scope.sc_aaa_enabled: false toggle under blueprint section with user confirmation protocol
- Set sc_levels_scanned to A, AA, best-practice (AAA excluded by default)
- Bumped max_iterations to 15 and timeout to 600s to accommodate axe-core runs and multiple fix cycles
- Added version 2.2.0 entry with projection score null (to be set after next eval run)
Target: move from 75.6 to 85+ by eliminating the plan-only anti-pattern and grounding every finding in either a real patch or a blocked-reason entry.