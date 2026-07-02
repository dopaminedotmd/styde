# Anomaly Detection Visualizer

Domain: dashboard
Version: 2

## Purpose

Real-time anomaly detection with rich visual signatures. Monitors metric streams and surfaces anomalies through multiple visual modes: pulse alerts (glowing rings that emanate from anomaly points), deviation heatmaps (grid of recent values colored by z-score), regression drift indicators (line showing how model prediction diverges from reality), and root-cause suggestion chains (correlated metrics that changed before the anomaly).

## Deliverable

anomaly-dashboard.html - A self-contained single-file HTML dashboard, interactive with live-updating data streams.

## Persona

Anomaly detection expert and real-time monitoring visualization specialist. Skilled in statistical process control, z-score/ESD detection, change-point algorithms, and designing alert visualizations that communicate urgency and context.

## ARTIFACT-FIRST DIRECTIVE

No specification text. Deliver working code as the final output. If the final output is a spec/design document instead of code, the task is failed.

## DELIVERABLE CHECKLIST

- [ ] anomaly-dashboard.html is a single self-contained HTML file
- [ ] No external dependencies (no CDN, no imports)
- [ ] All CSS and JS inline
- [ ] Runs in browser offline
- [ ] Implements z-score detection on streaming metrics
- [ ] Implements moving IQR detection
- [ ] Implements change-point detection
- [ ] Pulse ring animations on anomaly points
- [ ] Deviation heatmap with severity coloring
- [ ] Drift chart (prediction vs actual)
- [ ] Root-cause correlated metric suggestions
- [ ] Dynamic threshold bands
- [ ] Handles data gaps >3s with dashed connectors and annotation 'Data gap - interpolation paused'
- [ ] Handles no-data state (first 10 polls) with grey heatmap and 'Awaiting stream...' label
- [ ] Downsampling at 10K points to 2000
- [ ] Safari box-shadow fallback (6 layer cap, 2 outline layers)
- [ ] Drift predictions use exponential smoothing on rolling window (min 7 points) — NOT random noise
- [ ] Root cause uses Pearson correlation on lagged variables, only report |r| > 0.3
- [ ] Output complete with event loop and closing tags — no truncation
- [ ] Blinking anomaly alert pulse-dot in status badge
- [ ] Verification panel cross-references displayed values against computed metrics
- [ ] Broken stream handling: timeout and corrupt JSON detected with error indicator, not crash
- [ ] Resource bar rendering uses exact pixel/tick precision via floor-division

## FORBIDDEN PRACTICES

- Do NOT generate predictions by adding random noise to actual values
- Do NOT fabricate root cause chains with hardcoded or heuristic thresholds — use real correlation analysis
- Do NOT emit truncated output — if generation risks truncation, reduce scope rather than emit partial result
- Do NOT simulate statistical methods with fake data — use honest fallback with stated limitation

## Edge Cases

- 796-line file cutoff: If the generated HTML panel exceeds 796 lines, the browser rendering engine may clip the anomaly pulse animations. Split output into a main panel file and a detail overlay file when line count exceeds this threshold.
- Max-points-before-slowdown overflow: When the metrics stream accumulates more than 10,000 data points, the live-updating heatmap degrades from 60 fps to sub-10 fps. Implement automatic downsampling to 2000 points before rendering the heatmap slice.
- Empty or partial input: If the metric stream produces a gap longer than 3 seconds, the drift chart must display a dashed connector and a tooltip annotation reading 'Data gap - interpolation paused'. If no data arrives within the first 10 polling cycles, render a placeholder state: a grey heatmap with 'Awaiting stream...' label and zero pulse rings.
- Browser compatibility: The pulse ring CSS animation uses box-shadow with 8 layers. Safari 15.x collapses after 6 box-shadow layers. Emit a -webkit- prefixed fallback that caps at 6 layers and uses outline for the remaining 2.
- Broken stream: If the data source returns timeout (no data > 5s) or corrupt JSON (parse error), render a red error panel with 'Stream error — retrying' label. Do not crash or show blank page.

## Architecture

- Incremental DOM updates via data-attribute binding and CSS transitions
- No full SVG redraws - targeted element updates only
- Realistic data seeding with jitter, autocorrelation, and spike distribution
- Single requestAnimationFrame loop for all animation timers
- Drift chart uses simple exponential smoothing (SES) with alpha=0.3 on a rolling window of min 7 points for predictions
- Root cause analysis computes Pearson correlation between primary metric and candidate metrics over a lagged window of 20 samples; emits only pairs with |r| > 0.3
- Verification panel shows computed z-scores, correlation values, and data gap statistics alongside displayed values, using direct pixel-to-value mapping
