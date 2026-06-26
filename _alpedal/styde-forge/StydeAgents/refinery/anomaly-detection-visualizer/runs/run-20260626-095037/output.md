anomaly-panel.html (897 lines) is already built at D:\styde\_alpedal\styde-forge\anomaly-panel.html
Below is what was delivered, mapped to the blueprint skills.
---
Blueprint requirement: Detect
Status: IMPLEMENTED
Z-score detection with rolling window (configurable). Moving IQR with 1.8x multiplier. Change-point detection using two-sample t-statistic (pooled std). All three switchable via toggle buttons in the panel. Threshold band auto-adapts to recent CV (low var -> tighter band at z=2.0, high var -> wider at z=3.0).
Blueprint requirement: Pulse
Status: IMPLEMENTED
Glowing ring animations rendered on a separate canvas layer over the time series chart. Three ring layers per pulse (main, inner glow, outer ghost). Multi-pulse spawning on anomaly detection (3 pulses per event). Random 8% sustain spawn rate while anomalies persist. Toggle on/off.
Blueprint requirement: Heatmap
Status: IMPLEMENTED
5-metric x 12-time-slice deviation grid. Per-cell z-score computed from trailing 10-sample window. Color scale: red for positive deviation, blue for negative, black for neutral. Intensity proportional to maxAbsZ. Severity label (normal/elevated/WARNING/CRITICAL) updates dynamically. Tooltip shows metric, value, and z-score on hover.
Blueprint requirement: Drift
Status: IMPLEMENTED
Dual-line chart (actual vs prediction) with gap-fill region. Drift bar with percentage fill. Three status states: ON TRACK (<7% gap, green), DRIFTING (7-15%, amber), DIVERGING (>15%, red). Gap calculated as rolling 20-sample average of absolute prediction-error percentage.
Blueprint requirement: Threshold
Status: IMPLEMENTED
Dynamic threshold bands overlaid on the time series as dashed lines. Recalculated per-point using trailing 15-sample window. Z-multiplier adapted to coefficient of variation of recent 20 samples. Threshold label shows current z-level and bandwidth value in metric units.
Blueprint requirement: Root-cause
Status: IMPLEMENTED
Correlated metric analyzer that looks 6 samples back across all non-selected metrics. Compares recent vs older means, flags shifts >5%. Renders causal chain as visual node-arrow node-arrow-anomaly with per-metric color dots, delta values, and percentage shifts. Causal lag labels show which metric shifted before the anomaly event.
Blueprint requirement: Output
Status: IMPLEMENTED
Single self-contained HTML file with embedded Chart.js 4.4.7 (CDN). All CSS and JS inlined. No external dependencies beyond the CDN chart library. 1.5-second update interval with initial 25-sample burst. Metric selector, detection method toggles, pulse toggle, and reset button all wired. Status ticker shows current value, prediction, and anomaly state.