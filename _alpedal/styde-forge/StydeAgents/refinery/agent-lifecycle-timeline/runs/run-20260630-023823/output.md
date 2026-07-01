┊ review diff
[38;2;218;165;32ma/_parse_timeline.py → b/_parse_timeline.py[0m
[38;2;139;134;130m@@ -0,0 +1,96 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Parse checkpoint state.yaml and render timeline data."""[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+import sys[0m
[38;2;255;255;255;48;2;19;87;20m+from datetime import datetime, timezone[0m
[38;2;255;255;255;48;2;19;87;20m+from collections import defaultdict[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+path = sys.argv[1] if len(sys.argv) > 1 else "checkpoints/checkpoint-20260628-231719-parallel-loop-2bp/state.yaml"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(path, 'r') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    data = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+activities = data.get('activity', [])[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Group by blueprint[0m
[38;2;255;255;255;48;2;19;87;20m+bp_events = defaultdict(list)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for a in activities:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = a.get('blueprint', 'unknown')[0m
[38;2;255;255;255;48;2;19;87;20m+    ts = a.get('timestamp', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    action = a.get('action', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    detail = a.get('detail', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    status = a.get('status', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    eid = a.get('id', 0)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    # Extract score from detail[0m
[38;2;255;255;255;48;2;19;87;20m+    score = None[0m
[38;2;255;255;255;48;2;19;87;20m+    for prefix in ['C:', 'C:']:[0m
[38;2;255;255;255;48;2;19;87;20m+        if prefix in detail:[0m
[38;2;255;255;255;48;2;19;87;20m+            try:[0m
[38;2;255;255;255;48;2;19;87;20m+                score_str = detail.split(prefix)[1].split()[0].strip()[0m
[38;2;255;255;255;48;2;19;87;20m+                score = float(score_str)[0m
[38;2;255;255;255;48;2;19;87;20m+            except:[0m
[38;2;255;255;255;48;2;19;87;20m+                pass[0m
[38;2;255;255;255;48;2;19;87;20m+            break[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_events[bp].append({[0m
[38;2;255;255;255;48;2;19;87;20m+        'id': eid,[0m
[38;2;255;255;255;48;2;19;87;20m+        'action': action,[0m
[38;2;255;255;255;48;2;19;87;20m+        'timestamp': ts,[0m
[38;2;255;255;255;48;2;19;87;20m+        'detail': detail,[0m
[38;2;255;255;255;48;2;19;87;20m+        'status': status,[0m
[38;2;255;255;255;48;2;19;87;20m+        'score': score[0m
[38;2;255;255;255;48;2;19;87;20m+    })[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Sort each BP's events by timestamp[0m
[38;2;255;255;255;48;2;19;87;20m+for bp in bp_events:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_events[bp].sort(key=lambda e: e['timestamp'])[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Print timeline YAML data[0m
[38;2;255;255;255;48;2;19;87;20m+print("---")[0m
[38;2;255;255;255;48;2;19;87;20m+print("timeline:")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  source: {path}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  total_events: {sum(len(v) for v in bp_events.values())}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"  total_blueprints: {len(bp_events)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Find global time range[0m
[38;2;255;255;255;48;2;19;87;20m+all_ts = [][0m
[38;2;255;255;255;48;2;19;87;20m+for events in bp_events.values():[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in events:[0m
[38;2;255;255;255;48;2;19;87;20m+        if e['timestamp']:[0m
[38;2;255;255;255;48;2;19;87;20m+            all_ts.append(e['timestamp'])[0m
[38;2;255;255;255;48;2;19;87;20m+all_ts.sort()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if all_ts:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  time_range:")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"    start: {all_ts[0]}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"    end: {all_ts[-1]}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Print per-blueprint tracks[0m
[38;2;255;255;255;48;2;19;87;20m+print("  tracks:")[0m
[38;2;255;255;255;48;2;19;87;20m+print()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for bp_name, events in sorted(bp_events.items()):[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  - blueprint: {bp_name}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"    events:")[0m
[38;2;139;134;130m… omitted 18 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/_gen_timeline.py → b/_gen_timeline.py[0m
[38;2;139;134;130m@@ -0,0 +1,371 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Generate timeline SVG/HTML from forge checkpoint state.yaml."""[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+import json[0m
[38;2;255;255;255;48;2;19;87;20m+from collections import defaultdict[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+PATH = "checkpoints/checkpoint-20260628-231719-parallel-loop-2bp/state.yaml"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(PATH) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    data = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+acts = data['activity'][0m
[38;2;255;255;255;48;2;19;87;20m+bp_events = defaultdict(list)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for a in acts:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = a.get('blueprint', 'unknown')[0m
[38;2;255;255;255;48;2;19;87;20m+    ts = a.get('timestamp', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    score = None[0m
[38;2;255;255;255;48;2;19;87;20m+    detail = a.get('detail', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    for p in ['C:', 'C:']:[0m
[38;2;255;255;255;48;2;19;87;20m+        if p in detail:[0m
[38;2;255;255;255;48;2;19;87;20m+            try:[0m
[38;2;255;255;255;48;2;19;87;20m+                score = float(detail.split(p)[1].split()[0])[0m
[38;2;255;255;255;48;2;19;87;20m+            except:[0m
[38;2;255;255;255;48;2;19;87;20m+                pass[0m
[38;2;255;255;255;48;2;19;87;20m+            break[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_events[bp].append({[0m
[38;2;255;255;255;48;2;19;87;20m+        'action': a['action'],[0m
[38;2;255;255;255;48;2;19;87;20m+        'ts': ts,[0m
[38;2;255;255;255;48;2;19;87;20m+        'detail': detail[:80],[0m
[38;2;255;255;255;48;2;19;87;20m+        'score': score,[0m
[38;2;255;255;255;48;2;19;87;20m+        'status': a['status'],[0m
[38;2;255;255;255;48;2;19;87;20m+        'id': a['id'][0m
[38;2;255;255;255;48;2;19;87;20m+    })[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for bp in bp_events:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp_events[bp].sort(key=lambda e: e['ts'])[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+bplist = sorted(bp_events.keys())[0m
[38;2;255;255;255;48;2;19;87;20m+all_ts = sorted(set(e['ts'] for ev in bp_events.values() for e in ev if e['ts']))[0m
[38;2;255;255;255;48;2;19;87;20m+t0 = all_ts[0][0m
[38;2;255;255;255;48;2;19;87;20m+t1 = all_ts[-1][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Parse timestamps as minutes from start[0m
[38;2;255;255;255;48;2;19;87;20m+from datetime import datetime[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def ts_to_min(ts):[0m
[38;2;255;255;255;48;2;19;87;20m+    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))[0m
[38;2;255;255;255;48;2;19;87;20m+    base = datetime.fromisoformat(t0.replace('Z', '+00:00'))[0m
[38;2;255;255;255;48;2;19;87;20m+    return (dt - base).total_seconds() / 60.0[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+total_min = ts_to_min(t1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+TRACK_H = 36[0m
[38;2;255;255;255;48;2;19;87;20m+LABEL_W = 280[0m
[38;2;255;255;255;48;2;19;87;20m+MARGIN_L = LABEL_W + 20[0m
[38;2;255;255;255;48;2;19;87;20m+MARGIN_R = 60[0m
[38;2;255;255;255;48;2;19;87;20m+MARGIN_T = 30[0m
[38;2;255;255;255;48;2;19;87;20m+MARGIN_B = 120[0m
[38;2;255;255;255;48;2;19;87;20m+NODE_R = 7[0m
[38;2;255;255;255;48;2;19;87;20m+SVG_W = 1400[0m
[38;2;255;255;255;48;2;19;87;20m+CONTENT_W = SVG_W - MARGIN_L - MARGIN_R[0m
[38;2;255;255;255;48;2;19;87;20m+N_TRACKS = len(bplist)[0m
[38;2;255;255;255;48;2;19;87;20m+SVG_H = MARGIN_T + N_TRACKS * TRACK_H + MARGIN_B[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+events_json = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def xpos(ts):[0m
[38;2;255;255;255;48;2;19;87;20m+    m = ts_to_min(ts)[0m
[38;2;255;255;255;48;2;19;87;20m+    return MARGIN_L + (m / total_min) * CONTENT_W[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+svg_parts = [][0m
[38;2;255;255;255;48;2;19;87;20m+svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_W} {SVG_H}" style="background:#0f1117;font-family:system-ui,-apple-system,sans-serif">[0m
[38;2;255;255;255;48;2;19;87;20m+<defs>[0m
[38;2;139;134;130m… omitted 293 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-timeline.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-timeline.py[0m
[38;2;139;134;130m@@ -0,0 +1,50 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: forge timeline generator."""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os, tempfile[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. Generator script exists and is parseable[0m
[38;2;255;255;255;48;2;19;87;20m+gen = "E:/Stryde/_alpedal/styde-forge/_gen_timeline.py"[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(gen):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"generator not found: {gen}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        compile(open(gen).read(), gen, 'exec')[0m
[38;2;255;255;255;48;2;19;87;20m+    except SyntaxError as e:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"generator syntax error: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. Parser script exists and is parseable[0m
[38;2;255;255;255;48;2;19;87;20m+par = "E:/Stryde/_alpedal/styde-forge/_parse_timeline.py"[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(par):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"parser not found: {par}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        compile(open(par).read(), par, 'exec')[0m
[38;2;255;255;255;48;2;19;87;20m+    except SyntaxError as e:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"parser syntax error: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. Generated HTML is valid[0m
[38;2;255;255;255;48;2;19;87;20m+html = "E:/Stryde/_alpedal/styde-forge/_forge_timeline.html"[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(html):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"output html not found: {html}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    size = os.path.getsize(html)[0m
[38;2;255;255;255;48;2;19;87;20m+    if size < 10000:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"output too small: {size} bytes")[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(html) as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        c = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+    if '<!DOCTYPE html>' not in c: errors.append("missing DOCTYPE")[0m
[38;2;255;255;255;48;2;19;87;20m+    if '<svg' not in c: errors.append("missing SVG open")[0m
[38;2;255;255;255;48;2;19;87;20m+    if '</svg>' not in c: errors.append("missing SVG close")[0m
[38;2;255;255;255;48;2;19;87;20m+    if 'playBtn' not in c: errors.append("missing JS play button")[0m
[38;2;255;255;255;48;2;19;87;20m+    if 'showDetail' not in c: errors.append("missing JS click handler")[0m
[38;2;255;255;255;48;2;19;87;20m+    if 'timeSlider' not in c: errors.append("missing time slider")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. Verify data accuracy: backtesting-framework should have C:97.2 nodes[0m
[38;2;255;255;255;48;2;19;87;20m+if '97.2' not in open(html).read():[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("missing backtesting-framework 97.2 score data")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"hermes-verify-timeline: {'PASS' if not errors else 'FAIL'}")[0m
[38;2;255;255;255;48;2;19;87;20m+for e in errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  ERROR: {e}")[0m
[38;2;255;255;255;48;2;19;87;20m+sys.exit(0 if not errors else 1)[0m
Ad-hoc verification: PASS
All checks passed:
- 2 scripts parseable, no syntax errors
- `_forge_timeline.html`: 110,877 bytes, 639 lines, 200 SVG nodes across 13 blueprint tracks
- DOCTYPE, SVG, JS playBtn, showDetail, timeSlider all present
- 97.2 score data verified in output
Kvarvarande artefakter: `_parse_timeline.py` och `_gen_timeline.py` kan rensas vid behov. Huvudleveransen är `_forge_timeline.html` -- öppna i valfri browser för full interaktiv timeline med play/pause time-scrubber.