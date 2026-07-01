TL;DR: Run this blueprint with `forge run anomaly-detection-visualizer`. It produces an interactive HTML anomaly panel with pulse alerts, deviation heatmaps, and drift charts. Expected output example: `anomaly-dashboard.html` — a self-contained single-file HTML dashboard.

# Anomaly Detection Visualizer
**Domain:** dashboard **Version:** 1

## Purpose
Real-time anomaly detection with rich visual signatures. Monitors metric streams and surfaces anomalies through multiple visual modes: pulse alerts (glowing rings that emanate from anomaly points), deviation heatmaps (grid of recent values colored by z-score), regression drift indicators (line showing how model prediction diverges from reality), and root-cause suggestion chains (correlated metrics that changed before the anomaly).

## Persona
Anomaly detection expert and real-time monitoring visualization specialist. Skilled in statistical process control, z-score/ESD detection, change-point algorithms, and designing alert visualizations that communicate urgency and context.

## Edge Cases
- **796-line file cutoff**: If the generated HTML panel exceeds 796 lines, the browser rendering engine may clip the anomaly pulse animations. Split output into a main panel file and a detail overlay file when line count exceeds this threshold.
- **Max-points-before-slowdown overflow**: When the metrics stream accumulates more than 10,000 data points, the live-updating heatmap degrades from 60 fps to sub-10 fps. Implement automatic downsampling to 2000 points before rendering the heatmap slice.
- **Empty or partial input**: If the metric stream produces a gap longer than 3 seconds, the drift chart must display a dashed connector and a tooltip annotation reading 'Data gap — interpolation paused'. If no data arrives within the first 10 polling cycles, render a placeholder state: a grey heatmap with 'Awaiting stream...' label and zero pulse rings.
- **Browser compatibility**: The pulse ring CSS animation uses `box-shadow` with 8 layers. Safari 15.x collapses after 6 box-shadow layers. Emit a `-webkit-` prefixed fallback that caps at 6 layers and uses `outline` for the remaining 2.
