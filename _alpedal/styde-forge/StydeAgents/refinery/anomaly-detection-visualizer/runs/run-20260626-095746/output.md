┊ review diff
[38;2;218;165;32ma/anomaly-panel.html → b/anomaly-panel.html[0m
[38;2;139;134;130m@@ -3,813 +3,548 @@[0m
[38;2;184;134;11m <head>[0m
[38;2;184;134;11m <meta charset="UTF-8">[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;119;20;20m-<title>ANOMALY DETECTION ENGINE v2</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<title>Anomaly Detection Visualizer</title>[0m
[38;2;184;134;11m <style>[0m
[38;2;184;134;11m *{margin:0;padding:0;box-sizing:border-box}[0m
[38;2;255;255;255;48;2;119;20;20m-body{background:#080c16;color:#c8d6e5;font-family:'Segoe UI',system-ui,sans-serif;padding:16px;overflow-x:hidden}[0m
[38;2;255;255;255;48;2;119;20;20m-.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;max-width:1400px;margin:0 auto}[0m
[38;2;255;255;255;48;2;119;20;20m-@media(max-width:900px){.grid{grid-template-columns:1fr}}[0m
[38;2;255;255;255;48;2;119;20;20m-.card{background:linear-gradient(160deg,#0f1322,#0a0e1a);border:1px solid #1a2332;border-radius:10px;padding:14px;position:relative;overflow:hidden}[0m
[38;2;255;255;255;48;2;119;20;20m-.card h2{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:#475569;margin-bottom:10px;display:flex;align-items:center;gap:8px}[0m
[38;2;255;255;255;48;2;119;20;20m-.full{grid-column:1/-1}[0m
[38;2;255;255;255;48;2;119;20;20m-.metric-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}[0m
[38;2;255;255;255;48;2;119;20;20m-.metric-tag{padding:5px 12px;border-radius:16px;font-size:11px;font-weight:600;cursor:pointer;border:1px solid transparent;transition:.15s;background:#161f30;color:#64748b}[0m
[38;2;255;255;255;48;2;119;20;20m-.metric-tag.active{background:rgba(59,130,246,.2);border-color:#3b82f6;color:#60a5fa}[0m
[38;2;255;255;255;48;2;119;20;20m-.metric-tag.alert{background:rgba(239,68,68,.15);border-color:#ef4444;color:#f87171}[0m
[38;2;255;255;255;48;2;119;20;20m-.control-bar{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn{background:#161f30;border:1px solid #1e293b;color:#64748b;padding:5px 12px;border-radius:6px;font-size:11px;cursor:pointer;transition:.15s;font-weight:600}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn:hover{background:#1e293b;color:#c8d6e5}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn.active{background:rgba(59,130,246,.2);border-color:#3b82f6;color:#60a5fa}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn.danger{background:rgba(239,68,68,.15);border-color:#ef4444;color:#f87171}[0m
[38;2;255;255;255;48;2;119;20;20m-.chart-box{position:relative;height:200px;width:100%}[0m
[38;2;255;255;255;48;2;119;20;20m-.chart-box canvas{position:absolute;top:0;left:0;width:100%;height:100%}[0m
[38;2;255;255;255;48;2;119;20;20m-.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700}[0m
[38;2;255;255;255;48;2;119;20;20m-.badge.critical{background:#ef4444;color:#fff}[0m
[38;2;255;255;255;48;2;119;20;20m-.badge.warning{background:#f59e0b;color:#000}[0m
[38;2;255;255;255;48;2;119;20;20m-.badge.ok{background:#22c55e;color:#000}[0m
[38;2;255;255;255;48;2;119;20;20m-.badge.info{background:#3b82f6;color:#fff}[0m
[38;2;255;255;255;48;2;119;20;20m-.ticker{font-size:11px;color:#475569;font-family:'SF Mono','Consolas',monospace;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}[0m
[38;2;255;255;255;48;2;119;20;20m-.ticker .ts{color:#475569}[0m
[38;2;255;255;255;48;2;119;20;20m-.ticker .val{color:#e2e8f0;font-weight:600}[0m
[38;2;255;255;255;48;2;119;20;20m-.ticker .anom{color:#ef4444;font-weight:700}[0m
[38;2;255;255;255;48;2;119;20;20m-.heatmap-grid{display:grid;gap:2px;margin-top:4px}[0m
[38;2;255;255;255;48;2;119;20;20m-.heatmap-cell{width:100%;aspect-ratio:1;border-radius:2px;position:relative;transition:.1s;cursor:pointer;min-height:12px}[0m
[38;2;255;255;255;48;2;119;20;20m-.heatmap-cell:hover{transform:scale(1.3);z-index:10;outline:2px solid #fff}[0m
[38;2;255;255;255;48;2;119;20;20m-.heatmap-cell .tip{display:none;position:absolute;bottom:110%;left:50%;transform:translateX(-50%);background:#1a2332;border:1px solid #263040;padding:5px 8px;border-radius:5px;font-size:10px;white-space:nowrap;z-index:20;color:#e2e8f0;pointer-events:none}[0m
[38;2;255;255;255;48;2;119;20;20m-.heatmap-cell:hover .tip{display:block}[0m
[38;2;255;255;255;48;2;119;20;20m-.drift-bar{height:6px;border-radius:3px;background:#1a2332;position:relative;margin:3px 0 6px;overflow:hidden}[0m
[38;2;255;255;255;48;2;119;20;20m-.drift-fill{height:100%;border-radius:3px;transition:width .4s,background .4s}[0m
[38;2;255;255;255;48;2;119;20;20m-.drift-label{font-size:10px;display:flex;justify-content:space-between;color:#475569}[0m
[38;2;255;255;255;48;2;119;20;20m-.causal-chain{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin-top:6px;font-size:11px}[0m
[38;2;255;255;255;48;2;119;20;20m-.causal-node{background:#161f30;border:1px solid #1e293b;border-radius:5px;padding:4px 10px;display:flex;align-items:center;gap:5px;font-size:11px}[0m
[38;2;255;255;255;48;2;119;20;20m-.causal-node .delta{font-weight:700;font-size:10px}[0m
[38;2;255;255;255;48;2;119;20;20m-.causal-node .delta.up{color:#ef4444}[0m
[38;2;255;255;255;48;2;119;20;20m-.causal-node .delta.down{color:#22c55e}[0m
[38;2;255;255;255;48;2;119;20;20m-.causal-arrow{color:#334155;font-size:12px}[0m
[38;2;255;255;255;48;2;119;20;20m-.causal-root{color:#f59e0b;font-size:9px;background:rgba(245,158,11,.12);border-radius:8px;padding:2px 6px}[0m
[38;2;255;255;255;48;2;19;87;20m+body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI','SF Pro',system-ui,sans-serif;overflow-x:hidden}[0m
[38;2;255;255;255;48;2;19;87;20m+.panel{max-width:1400px;margin:0 auto;padding:16px}[0m
[38;2;255;255;255;48;2;19;87;20m+h1{font-size:18px;font-weight:600;color:#e8edf5;letter-spacing:0.3px;display:flex;align-items:center;gap:10px;margin-bottom:12px}[0m
[38;2;255;255;255;48;2;19;87;20m+h1 span{font-size:11px;background:#1a1f2e;color:#5a7a9a;padding:2px 8px;border-radius:4px;font-weight:400}[0m
[38;2;255;255;255;48;2;19;87;20m+.row{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px}[0m
[38;2;255;255;255;48;2;19;87;20m+.row-3{grid-template-columns:1fr 1fr 1fr}[0m
[38;2;255;255;255;48;2;19;87;20m+.card{background:#111827;border:1px solid #1e293b;border-radius:10px;padding:14px;position:relative;overflow:hidden}[0m
[38;2;255;255;255;48;2;19;87;20m+.card-title{font-size:11px;font-weight:600;color:#5a7a9a;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center}[0m
[38;2;255;255;255;48;2;19;87;20m+.card-title .badge{font-size:9px;background:#1a2a3a;color:#3a6a8a;padding:1px 6px;border-radius:3px}[0m
[38;2;255;255;255;48;2;19;87;20m+canvas{width:100%;height:140px;display:block;border-radius:6px;background:#0d1522}[0m
[38;2;255;255;255;48;2;19;87;20m+.chart-wrap{position:relative}[0m
[38;2;255;255;255;48;2;19;87;20m+.chart-wrap svg{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none}[0m
[38;2;255;255;255;48;2;19;87;20m+.alert-row{background:#0d1522;border-radius:6px;padding:8px 10px;margin-top:6px;display:flex;align-items:center;gap:8px;font-size:12px;border-left:3px solid #ef4444}[0m
[38;2;255;255;255;48;2;19;87;20m+.alert-row.sev-1{border-left-color:#f59e0b}[0m
[38;2;255;255;255;48;2;19;87;20m+.alert-row.sev-2{border-left-color:#ef4444}[0m
[38;2;255;255;255;48;2;19;87;20m+.alert-row.sev-3{border-left-color:#7c3aed}[0m
[38;2;255;255;255;48;2;19;87;20m+.alert-time{color:#5a7a9a;font-size:10px;white-space:nowrap}[0m
[38;2;255;255;255;48;2;19;87;20m+.alert-val{color:#e8edf5;font-weight:600;font-family:monospace}[0m
[38;2;255;255;255;48;2;19;87;20m+.alert-msg{color:#94a3b8;flex:1}[0m
[38;2;255;255;255;48;2;19;87;20m+.pulse-dot{width:8px;height:8px;border-radius:50%;display:inline-block;flex-shrink:0;animation:pulse-glow 1.5s ease-out infinite}[0m
[38;2;255;255;255;48;2;19;87;20m+.pulse-dot.red{background:#ef4444;box-shadow:0 0 8px #ef4444}[0m
[38;2;255;255;255;48;2;19;87;20m+.pulse-dot.amber{background:#f59e0b;box-shadow:0 0 8px #f59e0b}[0m
[38;2;255;255;255;48;2;19;87;20m+.pulse-dot.purple{background:#7c3aed;box-shadow:0 0 8px #7c3aed}[0m
[38;2;255;255;255;48;2;19;87;20m+@keyframes pulse-glow{[0m
[38;2;255;255;255;48;2;19;87;20m+0%{box-shadow:0 0 0 0 rgba(239,68,68,0.6);transform:scale(1)}[0m
[38;2;255;255;255;48;2;19;87;20m+50%{box-shadow:0 0 0 10px rgba(239,68,68,0);transform:scale(1.2)}[0m
[38;2;255;255;255;48;2;19;87;20m+100%{box-shadow:0 0 0 0 rgba(239,68,68,0);transform:scale(1)}[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.heatmap-grid{display:grid;grid-template-columns:repeat(24,1fr);gap:2px;height:120px}[0m
[38;2;255;255;255;48;2;19;87;20m+.heatmap-cell{position:relative;border-radius:2px;cursor:crosshair;transition:opacity 0.15s}[0m
[38;2;139;134;130m… omitted 1244 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-anomaly-panel.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-anomaly-panel.py[0m
[38;2;139;134;130m@@ -0,0 +1,105 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: anomaly-panel.html structure and feature completeness."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, re, sys, json, tempfile, shutil[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+HTML = r"D:\styde\_alpedal\styde-forge\anomaly-panel.html"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(HTML):[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"FAIL: file not found at {HTML}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(HTML, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+passes = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- structural checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+if "<!DOCTYPE html>" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append("doctype present")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("missing doctype")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "</html>" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append("html close tag present")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("missing html close")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- feature checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+features = {[0m
[38;2;255;255;255;48;2;19;87;20m+    "z-score detection": r"zScore\s*\(|z.?Score|Math\.abs\(z\)\s*>\s*2",[0m
[38;2;255;255;255;48;2;19;87;20m+    "moving IQR": r"iqr_lo|iqr_hi|1\.5\s*\*\s*iqr",[0m
[38;2;255;255;255;48;2;19;87;20m+    "change-point / CUSUM": r"cusumPoint|CUSUM|change.?point",[0m
[38;2;255;255;255;48;2;19;87;20m+    "animated pulse rings (SVG)": r"pulse.?ring|throbber|spawnPulse",[0m
[38;2;255;255;255;48;2;19;87;20m+    "deviation heatmap": r"heatmap|heatmap.?grid|heatmap.?cell",[0m
[38;2;255;255;255;48;2;19;87;20m+    "drift chart pred vs actual": r"driftCanvas|driftHistory|predicted.*actual",[0m
[38;2;255;255;255;48;2;19;87;20m+    "drift gap fill (green/red)": r"drift.*fill|gap.*color|rgba\(16,185,129",[0m
[38;2;255;255;255;48;2;19;87;20m+    "root-cause suggestion": r"suggestCauses|causal.?chain|causal.?link",[0m
[38;2;255;255;255;48;2;19;87;20m+    "dynamic threshold band": r"dynamic.*threshold|threshold.*band|bandWidth",[0m
[38;2;255;255;255;48;2;19;87;20m+    "severity coloring (3 levels)": r"severity.*[123]|sev-1|sev-2|sev-3",[0m
[38;2;255;255;255;48;2;19;87;20m+    "tooltip on heatmap cell": r"tooltip|class.*tooltip",[0m
[38;2;255;255;255;48;2;19;87;20m+    "live update interval": r"setInterval.*tickLoop",[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for label, pattern in features.items():[0m
[38;2;255;255;255;48;2;19;87;20m+    if re.search(pattern, content, re.IGNORECASE):[0m
[38;2;255;255;255;48;2;19;87;20m+        passes.append(f"feature: {label}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"MISSING feature: {label}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- tag balance (rough) ---[0m
[38;2;255;255;255;48;2;19;87;20m+open_script = content.count("<script")[0m
[38;2;255;255;255;48;2;19;87;20m+close_script = content.count("</script>")[0m
[38;2;255;255;255;48;2;19;87;20m+if open_script == close_script:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append("script tags balanced")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"script tag mismatch: {open_script} open, {close_script} close")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- count canvas elements ---[0m
[38;2;255;255;255;48;2;19;87;20m+canvas_count = content.count("<canvas")[0m
[38;2;255;255;255;48;2;19;87;20m+if canvas_count >= 2:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append(f"canvas elements: {canvas_count}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"expected >=2 canvas, found {canvas_count}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- JS check: no syntax errors (basic parse validation) ---[0m
[38;2;255;255;255;48;2;19;87;20m+# extract JS between <script> and </script>[0m
[38;2;255;255;255;48;2;19;87;20m+js_body_match = re.search(r"<script>(.*?)</script>", content, re.DOTALL)[0m
[38;2;255;255;255;48;2;19;87;20m+if js_body_match:[0m
[38;2;255;255;255;48;2;19;87;20m+    js_body = js_body_match.group(1)[0m
[38;2;255;255;255;48;2;19;87;20m+    tmpdir = tempfile.mkdtemp()[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        jsfile = os.path.join(tmpdir, "check.js")[0m
[38;2;255;255;255;48;2;19;87;20m+        with open(jsfile, "w") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+            f.write(js_body)[0m
[38;2;255;255;255;48;2;19;87;20m+        ret = os.system(f'node --check "{jsfile}" 2>nul')[0m
[38;2;255;255;255;48;2;19;87;20m+        if ret == 0:[0m
[38;2;255;255;255;48;2;19;87;20m+            passes.append("JavaScript syntax: valid (node --check)")[0m
[38;2;255;255;255;48;2;19;87;20m+        else:[0m
[38;2;139;134;130m… omitted 27 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-anomaly-panel.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-anomaly-panel.py[0m
[38;2;139;134;130m@@ -0,0 +1,105 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: anomaly-panel.html structure and feature completeness."""[0m
[38;2;255;255;255;48;2;19;87;20m+import os, re, sys, json, tempfile, shutil[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+HTML = r"D:\styde\_alpedal\styde-forge\anomaly-panel.html"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(HTML):[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"FAIL: file not found at {HTML}")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(HTML, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+passes = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- structural checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+if "<!DOCTYPE html>" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append("doctype present")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("missing doctype")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if "</html>" in content:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append("html close tag present")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("missing html close")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- feature checks ---[0m
[38;2;255;255;255;48;2;19;87;20m+features = {[0m
[38;2;255;255;255;48;2;19;87;20m+    "z-score detection": r"zScore\s*\(|z.?Score|Math\.abs\(z\)\s*>\s*2",[0m
[38;2;255;255;255;48;2;19;87;20m+    "moving IQR": r"iqr_lo|iqr_hi|1\.5\s*\*\s*iqr",[0m
[38;2;255;255;255;48;2;19;87;20m+    "change-point / CUSUM": r"cusumPoint|CUSUM|change.?point",[0m
[38;2;255;255;255;48;2;19;87;20m+    "animated pulse rings (SVG)": r"pulse.?ring|throbber|spawnPulse",[0m
[38;2;255;255;255;48;2;19;87;20m+    "deviation heatmap": r"heatmap|heatmap.?grid|heatmap.?cell",[0m
[38;2;255;255;255;48;2;19;87;20m+    "drift chart pred vs actual": r"driftCanvas|driftHistory|predicted.*actual",[0m
[38;2;255;255;255;48;2;19;87;20m+    "drift gap fill (green/red)": r"drift.*fill|gap.*color|rgba\(16,185,129",[0m
[38;2;255;255;255;48;2;19;87;20m+    "root-cause suggestion": r"suggestCauses|causal.?chain|causal.?link",[0m
[38;2;255;255;255;48;2;19;87;20m+    "dynamic threshold band": r"dynamic.*threshold|threshold.*band|bandWidth",[0m
[38;2;255;255;255;48;2;19;87;20m+    "severity coloring (3 levels)": r"severity.*[123]|sev-1|sev-2|sev-3",[0m
[38;2;255;255;255;48;2;19;87;20m+    "tooltip on heatmap cell": r"tooltip|class.*tooltip",[0m
[38;2;255;255;255;48;2;19;87;20m+    "live update interval": r"setInterval.*tickLoop",[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for label, pattern in features.items():[0m
[38;2;255;255;255;48;2;19;87;20m+    if re.search(pattern, content, re.IGNORECASE):[0m
[38;2;255;255;255;48;2;19;87;20m+        passes.append(f"feature: {label}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"MISSING feature: {label}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- tag balance (rough) ---[0m
[38;2;255;255;255;48;2;19;87;20m+open_script = content.count("<script")[0m
[38;2;255;255;255;48;2;19;87;20m+close_script = content.count("</script>")[0m
[38;2;255;255;255;48;2;19;87;20m+if open_script == close_script:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append("script tags balanced")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"script tag mismatch: {open_script} open, {close_script} close")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- count canvas elements ---[0m
[38;2;255;255;255;48;2;19;87;20m+canvas_count = content.count("<canvas")[0m
[38;2;255;255;255;48;2;19;87;20m+if canvas_count >= 2:[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.append(f"canvas elements: {canvas_count}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"expected >=2 canvas, found {canvas_count}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- JS check: no syntax errors (basic parse validation) ---[0m
[38;2;255;255;255;48;2;19;87;20m+# extract JS between <script> and </script>[0m
[38;2;255;255;255;48;2;19;87;20m+js_body_match = re.search(r"<script>(.*?)</script>", content, re.DOTALL)[0m
[38;2;255;255;255;48;2;19;87;20m+if js_body_match:[0m
[38;2;255;255;255;48;2;19;87;20m+    js_body = js_body_match.group(1)[0m
[38;2;255;255;255;48;2;19;87;20m+    tmpdir = tempfile.mkdtemp()[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        jsfile = os.path.join(tmpdir, "check.js")[0m
[38;2;255;255;255;48;2;19;87;20m+        with open(jsfile, "w") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+            f.write(js_body)[0m
[38;2;255;255;255;48;2;19;87;20m+        ret = os.system(f'node --check "{jsfile}" 2>nul')[0m
[38;2;255;255;255;48;2;19;87;20m+        if ret == 0:[0m
[38;2;255;255;255;48;2;19;87;20m+            passes.append("JavaScript syntax: valid (node --check)")[0m
[38;2;255;255;255;48;2;19;87;20m+        else:[0m
[38;2;139;134;130m… omitted 27 diff line(s) across 1 additional file(s)/section(s)[0m
17/17 PASS, temp verifier cleaned. Only changed file: D:\styde\_alpedal\styde-forge\anomaly-panel.html (unchanged since first write). Verifier temp script recreated, executed, and removed in this turn — no stray artifacts.