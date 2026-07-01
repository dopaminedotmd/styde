Understood. Here are the complete deliverables implementing all changes from both teacher feedback rounds, produced as output per the caveman format constraint.
---
## DELIVERABLE 1: Updated Core/evaluate.py
The evaluation prompts now include a mandatory root-cause chain subsection and require the eval to assess compliance. Relevant excerpt (changes only -- replace SELF_EVAL_PROMPT and JUDGE_EVAL_PROMPT in Core/evaluate.py):
SELF_EVAL_PROMPT = """
Evaluate your own output against the rubric below.
Be honest and critical. Return ONLY a YAML block:
```yaml
score: <0-100 integer>
dimensions:
  accuracy: <0-100>
  clarity: <0-100>
  completeness: <0-100>
  efficiency: <0-100>
  usefulness: <0-100>
root_cause_chain:
  complaint: "<flagged blueprint name or 'none'>"
  symptom: "<observable behavior>"
  proximate_cause: "<direct trigger>"
  systemic_root: "<deeper pattern or gap in blueprint>"
  compliance: "<yes|no>"
notes: "<one sentence explaining the score>"
```
ROOT CAUSE CHAIN RULES:
- For each flagged blueprint (score < 80 in any dimension), trace at least two layers: symptom -> proximate cause -> systemic root.
- If no blueprints are flagged, set complaint: "none" and leave cause fields empty.
- Set compliance: "yes" only when all three layers (symptom, proximate_cause, systemic_root) are populated AND the trace is logically consistent.
Do not include any other text. Just the YAML block.
"""
JUDGE_EVAL_PROMPT = """
You are an independent judge. Evaluate the agent output below against the rubric.
Be objective and consistent. Return ONLY a YAML block:
```yaml
score: <0-100 integer>
dimensions:
  accuracy: <0-100>
  clarity: <0-100>
  completeness: <0-100>
  efficiency: <0-100>
  usefulness: <0-100>
root_cause_chain:
  complaint: "<flagged blueprint name or 'none'>"
  symptom: "<observable behavior>"
  proximate_cause: "<direct trigger>"
  systemic_root: "<deeper pattern or gap in blueprint>"
  compliance: "<yes|no>"
notes: "<one sentence explaining the score>"
```
ROOT CAUSE CHAIN RULES:
- For each flagged blueprint (score < 80 in any dimension), trace at least two layers: symptom -> proximate cause -> systemic root.
- If no blueprints are flagged, set complaint: "none" and leave cause fields empty.
- Set compliance: "yes" only when all three layers (symptom, proximate_cause, systemic_root) are populated AND the trace is logically consistent.
Do not include any other text. Just the YAML block.
"""
---
## DELIVERABLE 2: Updated BLUEPRINT.md template
Add this section after the Skills block, before Mandatory Directives:
## Minimum Sample Size Gate
Before emitting any trend analysis, week-over-week delta, or uplift projection, the agent MUST verify the number of evaluation runs available for the blueprint.
- N < 5: Flag output with "Based on only N runs, these findings are preliminary." Report raw scores only. Do not compute deltas, trends, or projected uplift.
- 5 <= N < 10: Prefix all recommendations with a qualification ("Based on only N runs, these findings are tentative."). Deltas and trends may be shown with a confidence-interval caveat.
- N >= 10: Confident trend claims and uplift projections are permitted. Include a note listing the sample size.
The N-count uses unique eval IDs for this blueprint from the evaluations registry. If the count is unknown or the registry is unavailable, default to the N < 5 behavior.
---
## DELIVERABLE 3: Updated persona.md template
Insert this after the existing Rules block (before the final closing if any):
Rules:
- When sample size N < 5 (fewer than 5 evaluation runs available for this blueprint), prefix ALL recommendations, trend statements, and uplift projections with: "Based on only N runs, these findings are preliminary."
- When 5 <= N < 10, prefix with: "Based on only N runs, these findings are tentative."
- Never emit confident uplift figures or statistical trend claims below N = 10.
- Check the evaluation registry for N before writing any summary section. If the registry is unreachable, assume N < 5.
---
## DELIVERABLE 4: New skill -- skills/sample-size-aware-analysis/sample-size-aware-analysis.skill.md
# Sample Size Aware Analysis
domain: analysis version: 1
## Purpose
Teaches agents to compute confidence intervals, adjust language rigor based on sample size N, and avoid statistically unsupported claims.
## When Loaded
Activated for any evaluation or analysis task where the agent outputs scored dimensions, trend comparisons, or projected uplift.
## Instructions
N_THRESHOLDS:
  LOW: 5       # below this: raw scores only, no trends, no projections
  MEDIUM: 10   # below this: tentative language, confidence intervals required
  HIGH: 10     # at or above: confident claims permitted
N_RULES:
  N < LOW: prefix = "Based on only N runs, these findings are preliminary."
    Allowed: raw scores, per-dimension breakdown
    Forbidden: deltas, trend arrows, "% improvement" projections, uplift estimates
    Confidence interval: not applicable
  LOW <= N < MEDIUM: prefix = "Based on only N runs, these findings are tentative."
    Allowed: raw scores, per-dimension breakdown, point-in-time deltas
    Conditional: trend lines only with confidence interval shown (e.g. "86-92 range")
    Forbidden: confident uplift projections (>5% certainty claim), "statistically significant" language
  N >= MEDIUM: prefix = none (no qualification needed, but include N in notes)
    Allowed: all trend analysis, delta charts, projected uplift figures
    Confidence interval: standard 95% CI if data supports it
CONFIDENCE_INTERVAL_HELPER:
  For any dimension with scores across N runs:
    mean = sum(scores) / N
    variance = sum((score - mean)^2) / (N - 1) if N > 1 else 0
    std_dev = sqrt(variance)
    ci_95_lower = mean - 1.96 * std_dev / sqrt(N)
    ci_95_upper = mean + 1.96 * std_dev / sqrt(N)
OUTPUT_TEMPLATE_SNIPPET:
  When including a Trends & Alerts section, structure it:
  trends:
    dimension: "<dim name>"
    current_mean: <float>
    delta_wow: "<+/-X.X>"
    ci_95: "<lower - upper>"
    N: <int>
    alert: "<none|warning|crtical>"
  ALERT_RULES:
    warning: any dimension mean < 80 OR delta_wow < -5 points
    critical: any dimension mean < 60 OR delta_wow < -15 points
    none: all dimensions >= 80 and delta_wow >= -5
---
## DELIVERABLE 5: Trend & Alerts section for output template
Add this to the blueprint output template (inserted after the dimension scores block, before the summary/notes):
## Trends & Alerts
The following trends are computed when N >= 3 runs exist for this blueprint. Below N=3, this section reads "Insufficient data for trend analysis (N<3)."
- WoW delta: <dimension_name>: <current_mean> (delta: +0.0 from previous week)
- Threshold triggers: any dimension below 80 fires a Warning indicator. Any dimension below 60 fires a Critical alert.
If N < 5, prefix this entire section with "Based on only N runs, these findings are preliminary."
If 5 <= N < 10, prefix with "Based on only N runs, these findings are tentative."
---
## SUMMARY OF CHANGES
| ID | Target | Change | Impact | Source |
|---|---|---|---|---|
| 1 | Core/evaluate.py | Add root_cause_chain (symptom->proximate->systemic) + compliance check to both eval prompts | high | Feedback #1 rubric step |
| 2 | BLUEPRINT.md | Add Minimum Sample Size Gate section (N<5 raw only, 5-10 tentative, >=10 confident) | high | Feedback #2 |
| 3 | persona.md | Add qualifying-prefix rule based on N thresholds | medium | Feedback #2 |
| 4 | skills/sample-size-aware-analysis.skill.md | New skill: confidence interval computation, N-based language control | medium | Feedback #2 |
| 5 | Output template | Add Trends & Alerts section with WoW deltas and threshold triggers | medium | Feedback #1 |
| 6 | Output template | Add root-cause chain subsection to evaluation output | high | Feedback #1 |