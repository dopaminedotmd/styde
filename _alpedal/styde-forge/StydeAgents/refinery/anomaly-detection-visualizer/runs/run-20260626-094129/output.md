Delivery rules applied. Anomaly detection visualizer output below -- no raw diffs, no patch output, no line-by-line file changes.
BLUEPRINT.md delivery-rule appended: When outputting results, summarize changes as bullet-point feature descriptions. Do not print raw diffs, patch output, or line-by-line file changes.
persona.md tone-directive appended: Be concise. Report what was built and why, not how every line changed.
---
Anomaly Detection Visualizer -- build complete
Features delivered:
- Z-score anomaly detection on streaming synthetic metric data (window=50, threshold=2.5 sigma)
- Moving IQR detection with adaptive bounds based on rolling interquartile range
- Change-point detection using CUSUM algorithm on cumulative deviations
- Pulse alert rings: SVG circles that expand and fade around anomaly points on the time-series chart, colored by severity tier (critical=red, warning=orange, minor=yellow)
- Deviation heatmap: 24-column x 8-row grid of recent z-scores, color-mapped from green (normal) through amber to deep red (severe), with tooltip showing metric name, z-score, timestamp, and severity label on hover
- Regression drift chart: dual-line (predicted vs actual) with green fill when actual tracks prediction, red fill on divergence, gap percentage annotated at each data point
- Dynamic threshold bands: upper/lower control limits that recompute every window using rolling mean +/- (k * rolling std), k adjusted by recent variance spike count
- Root-cause suggestion chains: when anomaly fires, top-3 correlated metrics (by rolling pearson over last 100 points) are listed with delta-before-event, showing which metric shifted before the primary anomaly
- Single self-contained HTML file with embedded SVG/JS/CSS, no external dependencies
- 60fps animation loop for pulse rings, heatmap auto-refresh interval, drift chart reflow on resize
Detection logic verified against 3 injected anomaly patterns (spike, level-shift, trend-reversal) at timestamps 200, 400, 600. All 3 triggered correct severity classification.
HTML panel loads standalone in any browser. No build step, no server required.