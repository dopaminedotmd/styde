┊ review diff
[38;2;218;165;32ma/timeline_gen.py → b/timeline_gen.py[0m
[38;2;139;134;130m@@ -0,0 +1,385 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python[0m
[38;2;255;255;255;48;2;19;87;20m+"""Generate interactive Agent Lifecycle Timeline HTML from agents.yaml + activity.yaml."""[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml, json, re[0m
[38;2;255;255;255;48;2;19;87;20m+from collections import defaultdict[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Load data[0m
[38;2;255;255;255;48;2;19;87;20m+with open('agents.yaml') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    agents = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+with open('activity.yaml') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    activity = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Group runs by blueprint[0m
[38;2;255;255;255;48;2;19;87;20m+runs_by_bp = defaultdict(list)[0m
[38;2;255;255;255;48;2;19;87;20m+for a in agents.get('agents', []):[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = a.get('blueprint', 'unknown')[0m
[38;2;255;255;255;48;2;19;87;20m+    t = a.get('spawned_at', '') or ''[0m
[38;2;255;255;255;48;2;19;87;20m+    if not t:[0m
[38;2;255;255;255;48;2;19;87;20m+        continue[0m
[38;2;255;255;255;48;2;19;87;20m+    runs_by_bp[bp].append({[0m
[38;2;255;255;255;48;2;19;87;20m+        't': t, 's': a.get('stage', ''),[0m
[38;2;255;255;255;48;2;19;87;20m+        'i': a.get('iteration', 1),[0m
[38;2;255;255;255;48;2;19;87;20m+        'id': a.get('run_id', ''),[0m
[38;2;255;255;255;48;2;19;87;20m+        'b': a.get('benchmark', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    })[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Extract latest eval scores per blueprint[0m
[38;2;255;255;255;48;2;19;87;20m+score_map = {}[0m
[38;2;255;255;255;48;2;19;87;20m+for act in activity.get('activity', []):[0m
[38;2;255;255;255;48;2;19;87;20m+    if act.get('action') == 'eval' and act.get('status') == 'complete':[0m
[38;2;255;255;255;48;2;19;87;20m+        bp = act.get('blueprint', '')[0m
[38;2;255;255;255;48;2;19;87;20m+        d = act.get('detail', '')[0m
[38;2;255;255;255;48;2;19;87;20m+        m = re.search(r'S:([0-9.]+).*?J:([0-9.]+).*?C:([0-9.]+)', d)[0m
[38;2;255;255;255;48;2;19;87;20m+        if m:[0m
[38;2;255;255;255;48;2;19;87;20m+            ts = act.get('timestamp', '')[0m
[38;2;255;255;255;48;2;19;87;20m+            if bp not in score_map or ts > score_map[bp]['time']:[0m
[38;2;255;255;255;48;2;19;87;20m+                score_map[bp] = {'C': float(m.group(3)), 'time': ts}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Order blueprints by first run time[0m
[38;2;255;255;255;48;2;19;87;20m+bp_order = sorted(runs_by_bp.keys(),[0m
[38;2;255;255;255;48;2;19;87;20m+                  key=lambda bp: min(r['t'] for r in runs_by_bp[bp]))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+timeline = [][0m
[38;2;255;255;255;48;2;19;87;20m+for bp in bp_order:[0m
[38;2;255;255;255;48;2;19;87;20m+    runs = sorted(runs_by_bp[bp], key=lambda r: r['t'])[0m
[38;2;255;255;255;48;2;19;87;20m+    sc = score_map.get(bp, {}).get('C')[0m
[38;2;255;255;255;48;2;19;87;20m+    timeline.append({'bp': bp, 'r': runs, 'sc': sc})[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Find time range[0m
[38;2;255;255;255;48;2;19;87;20m+all_times = [r['t'] for runs in runs_by_bp.values() for r in runs][0m
[38;2;255;255;255;48;2;19;87;20m+t_min = min(all_times)[0m
[38;2;255;255;255;48;2;19;87;20m+t_max = max(all_times)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Build stage color map[0m
[38;2;255;255;255;48;2;19;87;20m+stage_colors = {[0m
[38;2;255;255;255;48;2;19;87;20m+    'refinery': '#5b8def',[0m
[38;2;255;255;255;48;2;19;87;20m+    'production': '#22c55e',[0m
[38;2;255;255;255;48;2;19;87;20m+    'archive': '#a78bfa',[0m
[38;2;255;255;255;48;2;19;87;20m+    'spawned': '#f59e0b'[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+html = r"""<!DOCTYPE html>[0m
[38;2;255;255;255;48;2;19;87;20m+<html lang="en">[0m
[38;2;255;255;255;48;2;19;87;20m+<head>[0m
[38;2;255;255;255;48;2;19;87;20m+<meta charset="UTF-8">[0m
[38;2;255;255;255;48;2;19;87;20m+<meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;19;87;20m+<title>Styde Forge — Agent Lifecycle Timeline</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<style>[0m
[38;2;255;255;255;48;2;19;87;20m+* { margin: 0; padding: 0; box-sizing: border-box; }[0m
[38;2;255;255;255;48;2;19;87;20m+body { background: #0f172a; color: #e2e8f0; font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace; font-size: 12px; overflow: hidden; height: 100vh; }[0m
[38;2;255;255;255;48;2;19;87;20m+.header { background: linear-gradient(135deg, #1e293b, #0f172a); border-bottom: 1px solid #334155; padding: 12px 20px; display: flex; align-items: center; gap: 16px; }[0m
[38;2;255;255;255;48;2;19;87;20m+.header h1 { font-size: 16px; font-weight: 600; color: #fbbf24; letter-spacing: 0.5px; }[0m
[38;2;255;255;255;48;2;19;87;20m+.header .stats { color: #94a3b8; font-size: 11px; display: flex; gap: 20px; }[0m
[38;2;255;255;255;48;2;19;87;20m+.header .stats span { color: #cbd5e1; }[0m
[38;2;255;255;255;48;2;19;87;20m+.controls { background: #1e293b; border-bottom: 1px solid #334155; padding: 8px 20px; display: flex; align-items: center; gap: 16px; }[0m
[38;2;255;255;255;48;2;19;87;20m+.controls button { background: #334155; color: #e2e8f0; border: 1px solid #475569; padding: 4px 14px; border-radius: 4px; cursor: pointer; font-size: 11px; font-family: inherit; }[0m
[38;2;255;255;255;48;2;19;87;20m+.controls button:hover { background: #475569; }[0m
[38;2;255;255;255;48;2;19;87;20m+.controls button.active { background: #fbbf24; color: #0f172a; border-color: #fbbf24; }[0m
[38;2;255;255;255;48;2;19;87;20m+.controls .slider-wrap { flex: 1; display: flex; align-items: center; gap: 8px; }[0m
[38;2;139;134;130m… omitted 307 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\timeline_gen.py → b/E:\Stryde\_alpedal\styde-forge\timeline_gen.py[0m
[38;2;139;134;130m@@ -377,7 +377,7 @@[0m
[38;2;184;134;11m </html>[0m
[38;2;184;134;11m """[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-with open('/e/Stryde/_alpedal/styde-forge/agent-lifecycle-timeline.html', 'w', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+with open('agent-lifecycle-timeline.html', 'w', encoding='utf-8') as f:[0m
[38;2;184;134;11m     f.write(html)[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m print('Written: agent-lifecycle-timeline.html')[0m
Ad-hoc verification (fresh, post-cleanup):
- artifact: agent-lifecycle-timeline.html — 102,575 bytes, exists
- blueprint data: 179 blueprints, 830 runs, 1 with eval score embedded
- HTML structure: DOCTYPE, html/svg close tags all present
- JS functions: render(), showPopup(), xPos(), getNodeColor() — all found
- event wiring: addEventListener for click, input — present
- generator: timeline_gen.py deleted, no stale files left
- errors: none
- verdict: VALID
Open agent-lifecycle-timeline.html in a browser for the full interactive timeline with scrubber, auto-play, and click-to-detail.