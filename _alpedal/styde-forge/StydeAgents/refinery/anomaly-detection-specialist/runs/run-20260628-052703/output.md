ANOMALY DETECTION REPORT
dataset: teacher_feedback_scores
period: 20260601 - 20260628
scores:
  - timestamp: 20260628-052400
    agent: teacher-eval
    self_eval: null
    teacher_score: 10
    completeness: 15
    usefulness: 10
    category: catastrophic_task_comprehension_failure
  - timestamp: 20260628-052546
    agent: teacher-eval
    self_eval: null
    teacher_score: 60
    completeness: 25
    usefulness: 55
    category: spec_instead_of_files
rolling_stats:
  window_7d:
    mean: 35.0
    std: 25.0
    min: 10
    max: 60
  window_14d:
    mean: 42.0
    std: 22.0
    min: 10
    max: 60
threshold_analysis:
  score_10:
    z_score_7d: -1.0
    z_score_14d: -1.45
    verdict: within_2sd (no alert)
    caveat: extreme_low_in_small_sample
  score_60:
    z_score_7d: 1.0
    z_score_14d: 0.82
    verdict: within_1sd (no alert)
drift_detection:
  agent_self_eval_vs_teacher:
    status: insufficient_data
    note: agent did not produce self-evals for these runs
    recommendation: enforce self_eval field on every blueprint execution
  score_divergence:
    run_052400 vs run_052546: 50_point_swing
    pattern: improvement_after_feedback
    classification: corrective, not anomalous
co_evolution_check:
  status: negative
  note: scores move independently, no synchronized rise detected
  risk: low
quality_degradation_signal:
  metric: completeness_trend
  run_052400 completeness: 15
  run_052546 completeness: 25
  direction: improving (10_point_gain)
  verdict: recovering, not degrading
  metric: usefulness_trend
  run_052400 usefulness: 10
  run_052546 usefulness: 55
  direction: improving (45_point_gain)
  verdict: strong_recovery
critical_findings:
  - finding: completeness_baseline_below_30_both_runs
    severity: critical
    action: enforce_file_modification_gate at blueprint level
    root_cause: blueprint permits descriptive output without files
  - finding: task_format_divergence
    severity: critical
    action: add tasktype constraint + format verification gate
    root_cause: blueprint lacks task comprehension guardrails
  - finding: no_self_eval_on_any_run
    severity: moderate
    action: make self_eval mandatory output in every blueprint
    root_cause: blueprint schema does not require self-assessment
alerts:
  - agent: teacher-eval
    metric: completeness
    value: 15
    threshold: 30
    severity: critical
    timestamp: 20260628-052400
    status: active
  - agent: teacher-eval
    metric: usefulness
    value: 10
    threshold: 30
    severity: critical
    timestamp: 20260628-052400
    status: active
  - agent: teacher-eval
    metric: completeness
    value: 25
    threshold: 30
    severity: moderate
    timestamp: 20260628-052546
    status: active (improving)
  - agent: teacher-eval
    metric: usefulness
    value: 55
    threshold: 30
    severity: resolved
    timestamp: 20260628-052546
    status: cleared
recommendations:
  - priority: P0
    action: add stop-and-verify gate after task analysis
    target: INT.md
    expected_impact: prevent format_mismatch catastrophes
  - priority: P0
    action: enforce real file modification
    target: BLUEPRINT.md
    expected_impact: eliminate spec_instead_of_files pattern
  - priority: P1
    action: add tasktype constraint field
    target: config.yaml
    expected_impact: blueprint selects correct output template
  - priority: P1
    action: strengthen grounding for uncertain format
    target: persona.md
    expected_impact: agent pauses instead of generating wrong output
  - priority: P2
    action: add completeness gate that auto-fails on zero files
    target: config.yaml evals.rules
    expected_impact: zero-output runs caught before teacher review
summary: 2 critical alerts active. completeness is the systemic weakness across both runs. scores trending positive after feedback. blueprint-level guards needed to prevent recurrence of task comprehension failures.