agent: styde-forge-teacher
metric: completeness-score
window: 7-day
values: [92.4, null, null, null, null, null, null]
moving_avg: 92.4
std_dev: 0.0
threshold_2sigma_alert: false
threshold_3sigma_critical: false
agent: styde-forge-teacher
metric: action-gap
description: blueprint describes fix but produces zero files
severity: critical
flagged: true
details: agent diagnosed missing input handling but output a specification document instead of modifying BLUEPRINT.md or config.yaml. zero files written. this is a null-action pattern — the agent produces analysis but does not execute.
agent: styde-forge-teacher
metric: self-eval-vs-teacher-drift
self_eval: 88.0
teacher_score: 92.4
delta: +4.4
direction: teacher_ahead
alert: false
note: teacher scoring higher than self-eval indicates undervaluation bias, not overconfidence. no action needed.
agent: styde-forge-teacher
metric: co-evolution-risk
window_comparison: all_feedback
scores_rising: true
quality_improving: false
flagged: true
details: both feedback cycles recommend the same class of fix (add guardrails to BLUEPRINT.md). score rose from null to 92.4 not because the agent fixed root cause but because the second run had lucky input (better-specified task). the underlying defect — agent fails to write files — was not corrected between runs. this is a textbook co-evolution signal: score increases without capability improvement.
aggregate_risk: moderate
components:
  action-execution-gap: critical
  drift-no-divergence: pass
  co-evolution-positive: moderate
recommendation: hold promotion from staging. require three consecutive teacher runs where the agent both diagnoses AND produces files for each blueprint change listed in feedback before promotion to production. trigger manual review if action-execution-gap repeats.