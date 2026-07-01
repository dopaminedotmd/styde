┊ review diff
[38;2;218;165;32ma/E:\tmp\timeline_gen.py → b/E:\tmp\timeline_gen.py[0m
[38;2;139;134;130m@@ -0,0 +1,228 @@[0m
[38;2;255;255;255;48;2;19;87;20m+import re[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+from datetime import datetime, timezone[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open('state.yaml', 'r') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+doc = yaml.safe_load(content)[0m
[38;2;255;255;255;48;2;19;87;20m+activities = doc.get('activity', [])[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+blueprint_evals = {}[0m
[38;2;255;255;255;48;2;19;87;20m+for act in activities:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = act.get('blueprint', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    action = act.get('action', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    ts = act.get('timestamp', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    detail = act.get('detail', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    run_id = act.get('id', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    progress = act.get('progress', 0)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    if bp not in blueprint_evals:[0m
[38;2;255;255;255;48;2;19;87;20m+        blueprint_evals[bp] = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    score = None[0m
[38;2;255;255;255;48;2;19;87;20m+    if action == 'eval':[0m
[38;2;255;255;255;48;2;19;87;20m+        m = re.search(r'C:([\d.]+)', detail)[0m
[38;2;255;255;255;48;2;19;87;20m+        if m:[0m
[38;2;255;255;255;48;2;19;87;20m+            score = float(m.group(1))[0m
[38;2;255;255;255;48;2;19;87;20m+    elif action == 'improve':[0m
[38;2;255;255;255;48;2;19;87;20m+        m = re.search(r'C:([\d.]+)', detail)[0m
[38;2;255;255;255;48;2;19;87;20m+        if m:[0m
[38;2;255;255;255;48;2;19;87;20m+            score = float(m.group(1))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    blueprint_evals[bp].append({[0m
[38;2;255;255;255;48;2;19;87;20m+        'action': action,[0m
[38;2;255;255;255;48;2;19;87;20m+        'id': run_id,[0m
[38;2;255;255;255;48;2;19;87;20m+        'timestamp': ts,[0m
[38;2;255;255;255;48;2;19;87;20m+        'detail': detail[:60],[0m
[38;2;255;255;255;48;2;19;87;20m+        'score': score,[0m
[38;2;255;255;255;48;2;19;87;20m+        'progress': progress[0m
[38;2;255;255;255;48;2;19;87;20m+    })[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+scored_bps = {}[0m
[38;2;255;255;255;48;2;19;87;20m+for bp, events in blueprint_evals.items():[0m
[38;2;255;255;255;48;2;19;87;20m+    scored = [e for e in events if e['score'] is not None][0m
[38;2;255;255;255;48;2;19;87;20m+    if len(scored) >= 2:[0m
[38;2;255;255;255;48;2;19;87;20m+        scored_bps[bp] = events[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def first_ts(bp):[0m
[38;2;255;255;255;48;2;19;87;20m+    events = scored_bps[bp][0m
[38;2;255;255;255;48;2;19;87;20m+    return min(e['timestamp'] for e in events)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+sorted_bps = sorted(scored_bps.keys(), key=first_ts)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+all_ts = [][0m
[38;2;255;255;255;48;2;19;87;20m+for bp in sorted_bps:[0m
[38;2;255;255;255;48;2;19;87;20m+    for e in scored_bps[bp]:[0m
[38;2;255;255;255;48;2;19;87;20m+        all_ts.append(e['timestamp'])[0m
[38;2;255;255;255;48;2;19;87;20m+all_ts.sort()[0m
[38;2;255;255;255;48;2;19;87;20m+t_min = all_ts[0][0m
[38;2;255;255;255;48;2;19;87;20m+t_max = all_ts[-1][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+bp_eval_counts = {bp: len([e for e in scored_bps[bp] if e['action'] == 'eval']) for bp in sorted_bps}[0m
[38;2;255;255;255;48;2;19;87;20m+top_bps = sorted(bp_eval_counts.keys(), key=lambda b: bp_eval_counts[b], reverse=True)[:10][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print("Top 10 blueprints by eval count:")[0m
[38;2;255;255;255;48;2;19;87;20m+for bp in top_bps:[0m
[38;2;255;255;255;48;2;19;87;20m+    evals = [e for e in scored_bps[bp] if e['action'] == 'eval' and e['score'] is not None][0m
[38;2;255;255;255;48;2;19;87;20m+    songs = [f"{e['timestamp'][-8:-3]}@{e['score']:.0f}" for e in evals][0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  {bp}: {bp_eval_counts[bp]} evals - {', '.join(songs)}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"\nTime range: {t_min} to {t_max}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def ts_to_epoch(t):[0m
[38;2;255;255;255;48;2;19;87;20m+    return datetime.fromisoformat(t.replace('Z', '+00:00')).timestamp()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+epoch_min = ts_to_epoch(t_min)[0m
[38;2;255;255;255;48;2;19;87;20m+epoch_max = ts_to_epoch(t_max)[0m
[38;2;255;255;255;48;2;19;87;20m+span = epoch_max - epoch_min if epoch_max > epoch_min else 3600[0m
[38;2;139;134;130m… omitted 150 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\e\tmp\timeline_gen_v2.py → b/E:\e\tmp\timeline_gen_v2.py[0m
[38;2;139;134;130m@@ -0,0 +1,324 @@[0m
[38;2;255;255;255;48;2;19;87;20m+import re[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+from datetime import datetime, timezone[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open('state.yaml', 'r') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    content = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+doc = yaml.safe_load(content)[0m
[38;2;255;255;255;48;2;19;87;20m+activities = doc.get('activity', [])[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+blueprint_evals = {}[0m
[38;2;255;255;255;48;2;19;87;20m+for act in activities:[0m
[38;2;255;255;255;48;2;19;87;20m+    bp = act.get('blueprint', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    action = act.get('action', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    ts = act.get('timestamp', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    detail = act.get('detail', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    run_id = act.get('id', '')[0m
[38;2;255;255;255;48;2;19;87;20m+    progress = act.get('progress', 0)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    if bp not in blueprint_evals:[0m
[38;2;255;255;255;48;2;19;87;20m+        blueprint_evals[bp] = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    score = None[0m
[38;2;255;255;255;48;2;19;87;20m+    if action == 'eval':[0m
[38;2;255;255;255;48;2;19;87;20m+        m = re.search(r'C:([\d.]+)', detail)[0m
[38;2;255;255;255;48;2;19;87;20m+        if m:[0m
[38;2;255;255;255;48;2;19;87;20m+            score = float(m.group(1))[0m
[38;2;255;255;255;48;2;19;87;20m+    elif action == 'improve':[0m
[38;2;255;255;255;48;2;19;87;20m+        m = re.search(r'C:[\d.]+\s+composite', detail.lower())[0m
[38;2;255;255;255;48;2;19;87;20m+        mm = re.search(r'C:([\d.]+)', detail)[0m
[38;2;255;255;255;48;2;19;87;20m+        if mm:[0m
[38;2;255;255;255;48;2;19;87;20m+            score = float(mm.group(1))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    blueprint_evals[bp].append({[0m
[38;2;255;255;255;48;2;19;87;20m+        'action': action,[0m
[38;2;255;255;255;48;2;19;87;20m+        'id': run_id,[0m
[38;2;255;255;255;48;2;19;87;20m+        'timestamp': ts,[0m
[38;2;255;255;255;48;2;19;87;20m+        'detail': detail[:60],[0m
[38;2;255;255;255;48;2;19;87;20m+        'score': score,[0m
[38;2;255;255;255;48;2;19;87;20m+        'progress': progress[0m
[38;2;255;255;255;48;2;19;87;20m+    })[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def ts_to_epoch(t):[0m
[38;2;255;255;255;48;2;19;87;20m+    return datetime.fromisoformat(t.replace('Z', '+00:00')).timestamp()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Deduplicate: if two events of same type have same score within 5 sec, keep first[0m
[38;2;255;255;255;48;2;19;87;20m+def dedup_events(events):[0m
[38;2;255;255;255;48;2;19;87;20m+    if not events:[0m
[38;2;255;255;255;48;2;19;87;20m+        return events[0m
[38;2;255;255;255;48;2;19;87;20m+    sorted_ev = sorted(events, key=lambda e: e['timestamp'])[0m
[38;2;255;255;255;48;2;19;87;20m+    result = [sorted_ev[0]][0m
[38;2;255;255;255;48;2;19;87;20m+    for ev in sorted_ev[1:]:[0m
[38;2;255;255;255;48;2;19;87;20m+        last = result[-1][0m
[38;2;255;255;255;48;2;19;87;20m+        tdiff = abs(ts_to_epoch(ev['timestamp']) - ts_to_epoch(last['timestamp']))[0m
[38;2;255;255;255;48;2;19;87;20m+        same_type = ev['action'] == last['action'][0m
[38;2;255;255;255;48;2;19;87;20m+        same_score = abs((ev['score'] or 0) - (last['score'] or 0)) < 0.5 if ev['score'] is not None and last['score'] is not None else False[0m
[38;2;255;255;255;48;2;19;87;20m+        if same_type and same_score and tdiff < 5:[0m
[38;2;255;255;255;48;2;19;87;20m+            continue[0m
[38;2;255;255;255;48;2;19;87;20m+        result.append(ev)[0m
[38;2;255;255;255;48;2;19;87;20m+    return result[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for bp in blueprint_evals:[0m
[38;2;255;255;255;48;2;19;87;20m+    blueprint_evals[bp] = dedup_events(blueprint_evals[bp])[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+scored_bps = {}[0m
[38;2;255;255;255;48;2;19;87;20m+for bp, events in blueprint_evals.items():[0m
[38;2;255;255;255;48;2;19;87;20m+    scored = [e for e in events if e['score'] is not None][0m
[38;2;255;255;255;48;2;19;87;20m+    if len(scored) >= 2:[0m
[38;2;255;255;255;48;2;19;87;20m+        scored_bps[bp] = events[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def first_ts(bp):[0m
[38;2;255;255;255;48;2;19;87;20m+    events = scored_bps[bp][0m
[38;2;255;255;255;48;2;19;87;20m+    return min(e['timestamp'] for e in events)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+sorted_bps = sorted(scored_bps.keys(), key=first_ts)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+all_ts = [][0m
[38;2;255;255;255;48;2;19;87;20m+for bp in sorted_bps:[0m
[38;2;139;134;130m… omitted 246 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\e\tmp\timeline_gen_v2.py → b/E:\e\tmp\timeline_gen_v2.py[0m
[38;2;139;134;130m@@ -16,21 +16,13 @@[0m
[38;2;184;134;11m     detail = act.get('detail', '')[0m
[38;2;184;134;11m     run_id = act.get('id', '')[0m
[38;2;184;134;11m     progress = act.get('progress', 0)[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;184;134;11m     if bp not in blueprint_evals:[0m
[38;2;184;134;11m         blueprint_evals[bp] = [][0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;184;134;11m     score = None[0m
[38;2;184;134;11m     if action == 'eval':[0m
[38;2;184;134;11m         m = re.search(r'C:([\d.]+)', detail)[0m
[38;2;184;134;11m         if m:[0m
[38;2;184;134;11m             score = float(m.group(1))[0m
[38;2;255;255;255;48;2;119;20;20m-    elif action == 'improve':[0m
[38;2;255;255;255;48;2;119;20;20m-        m = re.search(r'C:[\d.]+\s+composite', detail.lower())[0m
[38;2;255;255;255;48;2;119;20;20m-        mm = re.search(r'C:([\d.]+)', detail)[0m
[38;2;255;255;255;48;2;119;20;20m-        if mm:[0m
[38;2;255;255;255;48;2;119;20;20m-            score = float(mm.group(1))[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;184;134;11m     blueprint_evals[bp].append({[0m
[38;2;184;134;11m         'action': action,[0m
[38;2;184;134;11m         'id': run_id,[0m
[38;2;139;134;130m@@ -43,7 +35,6 @@[0m
[38;2;184;134;11m def ts_to_epoch(t):[0m
[38;2;184;134;11m     return datetime.fromisoformat(t.replace('Z', '+00:00')).timestamp()[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-# Deduplicate: if two events of same type have same score within 5 sec, keep first[0m
[38;2;184;134;11m def dedup_events(events):[0m
[38;2;184;134;11m     if not events:[0m
[38;2;184;134;11m         return events[0m
[38;2;139;134;130m@@ -68,12 +59,7 @@[0m
[38;2;184;134;11m     if len(scored) >= 2:[0m
[38;2;184;134;11m         scored_bps[bp] = events[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-def first_ts(bp):[0m
[38;2;255;255;255;48;2;119;20;20m-    events = scored_bps[bp][0m
[38;2;255;255;255;48;2;119;20;20m-    return min(e['timestamp'] for e in events)[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-sorted_bps = sorted(scored_bps.keys(), key=first_ts)[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;19;87;20m+sorted_bps = sorted(scored_bps.keys(), key=lambda b: min(e['timestamp'] for e in scored_bps[b]))[0m
[38;2;184;134;11m all_ts = [][0m
[38;2;184;134;11m for bp in sorted_bps:[0m
[38;2;184;134;11m     for e in scored_bps[bp]:[0m
[38;2;139;134;130m@@ -90,7 +76,6 @@[0m
[38;2;184;134;11m     evals = [e for e in scored_bps[bp] if e['action'] == 'eval' and e['score'] is not None][0m
[38;2;184;134;11m     scores_str = ' -> '.join([f"{e['score']:.0f}" for e in evals])[0m
[38;2;184;134;11m     print(f"  {bp}: {len(evals)} evals: {scores_str}")[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;184;134;11m print(f"\nTime range: {t_min} to {t_max}")[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m epoch_min = ts_to_epoch(t_min)[0m
[38;2;139;134;130m@@ -104,7 +89,6 @@[0m
[38;2;184;134;11m margin_t = 40[0m
[38;2;184;134;11m margin_r = 40[0m
[38;2;184;134;11m margin_b = 40[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;184;134;11m n_tracks = len(top_bps)[0m
[38;2;184;134;11m plot_w = svg_w - margin_l - margin_r - label_w[0m
[38;2;184;134;11m plot_h = n_tracks * track_h + 20[0m
[38;2;139;134;130m@@ -124,166 +108,121 @@[0m
[38;2;184;134;11m     else:[0m
[38;2;184;134;11m         return '#4A90D9'[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-# Track color palette (dark theme)[0m
[38;2;255;255;255;48;2;119;20;20m-palette = ['#1a1a2e', '#16213e', '#0f3460', '#1a1a3e', '#12122e', '#1e1e3e', '#0a0a2e', '#18183e', '#14142e', '#1c1c3e'][0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines = [][0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" style="background:#0d0d1a;font-family:monospace">')[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-# defs for gradients and filters[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('<defs>')[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('<linearGradient id="bg-grad" x1="0" y1="0" x2="0" y2="1">')[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('<stop offset="0%" stop-color="#0d0d1a"/>')[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('<stop offset="100%" stop-color="#12122e"/>')[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('</linearGradient>')[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('<filter id="glow">')[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('<feGaussianBlur stdDeviation="2" result="blur"/>')[0m
[38;2;255;255;255;48;2;119;20;20m-svg_lines.append('<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>')[0m
[38;2;139;134;130m… omitted 244 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\e\tmp\timeline_gen_v2.py → b/E:\e\tmp\timeline_gen_v2.py[0m
[38;2;139;134;130m@@ -255,7 +255,7 @@[0m
[38;2;184;134;11m S.append('</svg>')[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m svg_content = '\n'.join(S)[0m
[38;2;255;255;255;48;2;119;20;20m-outpath = '/e/Stryde/_alpedal/styde-forge/agent_timeline.svg'[0m
[38;2;255;255;255;48;2;19;87;20m+outpath = 'agent_timeline.svg'[0m
[38;2;184;134;11m with open(outpath, 'w') as f:[0m
[38;2;184;134;11m     f.write(svg_content)[0m
[38;2;184;134;11m print(f"SVG: {len(svg_content)} chars -> {outpath}")[0m
agent_timeline.svg created (28 KB, 290 lines).
6 blueprint tracks, 38 eval nodes across 90 minutes.
Tracks from top to bottom:
- activity-feed-designer — 10 evals: 85 -> 93 -> 92 -> 92 -> 91 -> 89 -> 95 -> 89 -> 88 -> 69
- 3d-data-terrain-explorer — 10 evals: 90 -> 87 -> 87 -> 87 -> 78 -> 85 -> 90 -> 93 -> 91 -> 68
- adaptive-metric-layout — 7 evals: 87 -> 80 -> 77 -> 90 -> 77 -> 88 -> 62
- aesthetic-style-composer — 6 evals: 87 -> 85 -> 84 -> 85 -> 76 -> 63
- ab-testing-statistician — 3 evals: 68 -> 74 -> 92
- accessibility-auditor — 2 evals: 51 -> 88
Timeline: 23:48 UTC to 01:26 UTC (June 27-28, 2026).
Interactive features embedded in the SVG:
- Gold circles (85+) = production gate passed
- Amber circles (70-84) = improving
- Blue circles (below 70) = early/struggling
- Small dots = spawn (grey) / improve (darker)
- Click any eval node: popup shows run_id, action, composite score, benchmark, stage
- Time scrubber bar at bottom with gold playhead and play button
- Vertical grid lines with hour:minute labels
- Score legend explaining color scheme
Open agent_timeline.svg in a browser to use the interactive features.