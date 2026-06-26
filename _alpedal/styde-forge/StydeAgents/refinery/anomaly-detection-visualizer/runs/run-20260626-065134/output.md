┊ review diff
[38;2;218;165;32ma/anomaly-panel.html → b/anomaly-panel.html[0m
[38;2;139;134;130m@@ -0,0 +1,897 @@[0m
[38;2;255;255;255;48;2;19;87;20m+<!DOCTYPE html>[0m
[38;2;255;255;255;48;2;19;87;20m+<html lang="en">[0m
[38;2;255;255;255;48;2;19;87;20m+<head>[0m
[38;2;255;255;255;48;2;19;87;20m+<meta charset="UTF-8">[0m
[38;2;255;255;255;48;2;19;87;20m+<meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;19;87;20m+<title>ANOMALY DETECTION PANEL v1</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>[0m
[38;2;255;255;255;48;2;19;87;20m+<style>[0m
[38;2;255;255;255;48;2;19;87;20m+*{margin:0;padding:0;box-sizing:border-box}[0m
[38;2;255;255;255;48;2;19;87;20m+body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI','SF Pro',system-ui,sans-serif;padding:20px;overflow-x:hidden}[0m
[38;2;255;255;255;48;2;19;87;20m+.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:1400px;margin:0 auto}[0m
[38;2;255;255;255;48;2;19;87;20m+@media(max-width:900px){.grid{grid-template-columns:1fr}}[0m
[38;2;255;255;255;48;2;19;87;20m+.card{background:linear-gradient(145deg,#111827,#0f1322);border:1px solid #1e293b;border-radius:12px;padding:16px;position:relative;overflow:hidden}[0m
[38;2;255;255;255;48;2;19;87;20m+.card h2{font-size:13px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#64748b;margin-bottom:12px}[0m
[38;2;255;255;255;48;2;19;87;20m+.card h2 .counter{color:#f59e0b;margin-left:8px;font-size:11px}[0m
[38;2;255;255;255;48;2;19;87;20m+.full{grid-column:1/-1}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-bar{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:12px}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-tag{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;border:1px solid transparent;transition:.2s;background:#1e293b;color:#94a3b8}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-tag.active{background:rgba(59,130,246,.2);border-color:#3b82f6;color:#60a5fa}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-tag.alert{background:rgba(239,68,68,.15);border-color:#ef4444;color:#f87171}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-tag.warn{background:rgba(245,158,11,.15);border-color:#f59e0b;color:#fbbf24}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Pulse canvas layer */[0m
[38;2;255;255;255;48;2;19;87;20m+#pulseCanvas{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:2}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Chart wrappers */[0m
[38;2;255;255;255;48;2;19;87;20m+.chart-wrap{position:relative;height:220px}[0m
[38;2;255;255;255;48;2;19;87;20m+.chart-wrap canvas{z-index:1;position:relative}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Heatmap */[0m
[38;2;255;255;255;48;2;19;87;20m+.heatmap-grid{display:grid;gap:2px;margin-top:4px}[0m
[38;2;255;255;255;48;2;19;87;20m+.heatmap-cell{width:100%;aspect-ratio:1;border-radius:2px;position:relative;transition:.15s;cursor:pointer;min-height:14px}[0m
[38;2;255;255;255;48;2;19;87;20m+.heatmap-cell:hover{transform:scale(1.4);z-index:10;outline:2px solid #fff}[0m
[38;2;255;255;255;48;2;19;87;20m+.heatmap-cell .tooltip{display:none;position:absolute;bottom:110%;left:50%;transform:translateX(-50%);background:#1e293b;border:1px solid #334155;padding:6px 10px;border-radius:6px;font-size:11px;white-space:nowrap;z-index:20;color:#e2e8f0;pointer-events:none}[0m
[38;2;255;255;255;48;2;19;87;20m+.heatmap-cell:hover .tooltip{display:block}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Root cause chain */[0m
[38;2;255;255;255;48;2;19;87;20m+.causal-chain{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:8px}[0m
[38;2;255;255;255;48;2;19;87;20m+.causal-node{background:#1e293b;border:1px solid #334155;border-radius:6px;padding:6px 12px;font-size:12px;display:flex;align-items:center;gap:6px}[0m
[38;2;255;255;255;48;2;19;87;20m+.causal-node .delta{font-weight:700;font-size:11px}[0m
[38;2;255;255;255;48;2;19;87;20m+.causal-node .delta.up{color:#ef4444}[0m
[38;2;255;255;255;48;2;19;87;20m+.causal-node .delta.down{color:#22c55e}[0m
[38;2;255;255;255;48;2;19;87;20m+.causal-arrow{color:#475569;font-size:14px}[0m
[38;2;255;255;255;48;2;19;87;20m+.causal-root{color:#f59e0b;font-size:10px;background:rgba(245,158,11,.15);border-radius:10px;padding:2px 8px}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Drift */[0m
[38;2;255;255;255;48;2;19;87;20m+.drift-bar{height:8px;border-radius:4px;background:#1e293b;position:relative;margin:4px 0 8px;overflow:hidden}[0m
[38;2;255;255;255;48;2;19;87;20m+.drift-fill{height:100%;border-radius:4px;transition:width .5s ease,background .5s}[0m
[38;2;255;255;255;48;2;19;87;20m+.drift-label{font-size:11px;display:flex;justify-content:space-between;color:#64748b}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Severity badge */[0m
[38;2;255;255;255;48;2;19;87;20m+.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700}[0m
[38;2;255;255;255;48;2;19;87;20m+.badge.critical{background:#ef4444;color:#fff}[0m
[38;2;255;255;255;48;2;19;87;20m+.badge.warning{background:#f59e0b;color:#000}[0m
[38;2;255;255;255;48;2;19;87;20m+.badge.info{background:#3b82f6;color:#fff}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Status ticker */[0m
[38;2;255;255;255;48;2;19;87;20m+.ticker{font-size:12px;color:#475569;font-family:'SF Mono','Consolas',monospace;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}[0m
[38;2;255;255;255;48;2;19;87;20m+.ticker .ts{color:#64748b}[0m
[38;2;255;255;255;48;2;19;87;20m+.ticker .val{color:#e2e8f0;font-weight:600}[0m
[38;2;255;255;255;48;2;19;87;20m+.ticker .anom{color:#ef4444;font-weight:700}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Controls */[0m
[38;2;255;255;255;48;2;19;87;20m+.controls{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}[0m
[38;2;255;255;255;48;2;19;87;20m+.btn{background:#1e293b;border:1px solid #334155;color:#94a3b8;padding:6px 14px;border-radius:6px;font-size:12px;cursor:pointer;transition:.2s;font-weight:600}[0m
[38;2;255;255;255;48;2;19;87;20m+.btn:hover{background:#334155;color:#e2e8f0}[0m
[38;2;255;255;255;48;2;19;87;20m+.btn.active{background:rgba(59,130,246,.2);border-color:#3b82f6;color:#60a5fa}[0m
[38;2;255;255;255;48;2;19;87;20m+.btn.danger{background:rgba(239,68,68,.15);border-color:#ef4444;color:#f87171}[0m
[38;2;255;255;255;48;2;19;87;20m+.btn.danger:hover{background:rgba(239,68,68,.3)}[0m
[38;2;255;255;255;48;2;19;87;20m+</style>[0m
[38;2;255;255;255;48;2;19;87;20m+</head>[0m
[38;2;255;255;255;48;2;19;87;20m+<body>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<div class="grid">[0m
[38;2;255;255;255;48;2;19;87;20m+  <!-- METRIC SELECTOR + STATUS -->[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="card full">[0m
[38;2;255;255;255;48;2;19;87;20m+    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">[0m
[38;2;255;255;255;48;2;19;87;20m+      <h2 style="margin:0">ANOMALY DETECTION ENGINE <span id="alarmCount" class="badge info">0 active</span></h2>[0m
[38;2;139;134;130m… omitted 819 diff line(s) across 1 additional file(s)/section(s)[0m
Built. Single self-contained HTML file at:
D:\styde\_alpedal\styde-forge\anomaly-panel.html
panel: anomaly-panel.html | ~34 KB | zero dependencies (Chart.js via CDN)
what it does:
detection modes: Z-Score, Moving IQR, Change-Point  selectable via toggle buttons
pulse: animated glow rings emanate from anomaly points on the time-series chart  three concentric rings (main + inner glow + outer ghost) with fade-out
heatmap: 12-column time-slice deviation grid, 5 metrics x recent slices, colored by z-score intensity  red=positive deviation, blue=negative, dark=normal  tooltip shows metric+value+z on hover
drift: prediction-vs-actual line chart with gap-fill area  green bar when on track (<7%), yellow at 7-15%, red when diverging (>15%)
threshold: dynamic z-score bands overlay on time chart  adapts to recent variance (CV-based: low var=2.0, high var=3.0)
root cause: scans other metrics for >5% shifts preceding the anomaly  displays causal chain with direction arrows and percentage deltas
open in browser to run. No server needed. Data auto-generates with 15% anomaly injection rate, 1.5s update interval.