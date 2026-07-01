BLUEPRINT.md changes for efficiency feedback (severity: medium, impact: high)
Add section after 'Threshold' skill:
Computational Efficiency (Non-Functional)
  StreamingStats: all z-score, IQR, CUSUM statistics MUST use incremental/online algorithms
    RunningMean: maintain count, mean, M2 (Welford's) - O(1) per sample, no window replay
    RunningVariance: compute from M2 / count, O(1) per sample
    OnlineCUSUM: cumulative sum of (x - mean - shift), increment each frame, no full-window reprocess
    RollingIQR: maintain order-statistic tree or t-digest for streaming quantiles, NOT sorted list copy
    Windowing: if fixed-window semantics needed (sliding N), use deque + incremental update, never slice+copy+sort
    Verify: frame-rate must stay above 30fps on a 16-core machine with 1000 metrics x 1000 history each
Add section after 'Output' skill:
Interactivity (Non-Functional)
  PauseResume: freeze animation loop on user click, unfreeze on second click. During pause, allow zoom/hover inspection of individual anomaly points
  ThresholdSliders: three draggable numeric controls: z-score threshold (1.0-6.0 default 3.0), IQR multiplier (1.0-5.0 default 1.5), CUSUM drift (0.1-2.0 default 0.5). Changing a slider recomputes detection frame immediately (not on next animation tick)
  MethodToggle: radio buttons or checkbox set to enable/disable each detection method (z-score, IQR, CUSUM). Disabled methods don't contribute to alert state
  LegendToggle: show/hide each visual layer (pulse rings, heatmap, drift gap, threshold bands)
  Drilldown: clicking a heatmap cell shows 30-frame history of that metric with same detection overlays
  RootCause: clicking a root-cause chain link jumps to that correlated metric's drift chart
persona.md changes for completeness feedback (severity: high, impact: high)
Add to 'Rules' section as rule #1:
  SummaryFirst: NEVER output the full raw diff in your main response. Provide a 3-5 line executive summary of changes with file paths and line counts, then offer the full diff on request. The diff MUST be gated behind a user-ask, never dumped inline.
config.yaml changes for completeness feedback (severity: medium, impact: medium)
  maxresponsetokens: 8192
  output_format: structured/summary-first
  max_dump_lines: 50  # cap any raw-appended data
Summary of changes (files: 3, insertions: ~48 lines):
  BLUEPRINT.md   +2 sections (StreamingStats, Interactivity) = ~28 lines
  persona.md     +1 rule (SummaryFirst) = ~4 lines
  config.yaml    +3 keys = ~3 lines
Delta from current composite 88.8 + efficiency fix (+5) + completeness fix (+7) = estimated 100.8. With ceiling at 100, would push past 90 threshold by 10+ points.