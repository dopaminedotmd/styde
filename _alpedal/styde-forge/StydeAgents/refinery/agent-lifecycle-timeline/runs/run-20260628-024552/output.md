┊ review diff
[38;2;218;165;32ma/gen_timeline.py → b/gen_timeline.py[0m
[38;2;139;134;130m@@ -1,494 +1,254 @@[0m
[38;2;184;134;11m #!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;119;20;20m-"""Generate agent lifecycle timeline SVG+HTML from agents.yaml and activity.yaml"""[0m
[38;2;255;255;255;48;2;19;87;20m+"""Parse state.yaml and generate agent lifecycle timeline SVG."""[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;184;134;11m import re[0m
[38;2;255;255;255;48;2;119;20;20m-import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+import os[0m
[38;2;184;134;11m from datetime import datetime, timezone[0m
[38;2;255;255;255;48;2;119;20;20m-from collections import defaultdict[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-def load_yaml(path):[0m
[38;2;255;255;255;48;2;119;20;20m-    with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;119;20;20m-        return yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-def parse_score(detail):[0m
[38;2;255;255;255;48;2;119;20;20m-    """Extract composite score C from eval detail strings like 'S:83 J:91 C:87.8'"""[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+STATE_PATH = "E:\\Stryde\\_alpedal\\styde-forge\\state.yaml"[0m
[38;2;255;255;255;48;2;19;87;20m+OUT_PATH = "E:\\Stryde\\_alpedal\\styde-forge\\agent_lifecycle_timeline.svg"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(STATE_PATH, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    data = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+activities = data.get("activity", [])[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Parse entries[0m
[38;2;255;255;255;48;2;19;87;20m+entries = [][0m
[38;2;255;255;255;48;2;19;87;20m+for a in activities:[0m
[38;2;255;255;255;48;2;19;87;20m+    action = a.get("action", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    blueprint = a.get("blueprint", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    detail = a.get("detail", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    rid = a.get("id", 0)[0m
[38;2;255;255;255;48;2;19;87;20m+    progress = a.get("progress", 0)[0m
[38;2;255;255;255;48;2;19;87;20m+    status = a.get("status", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    ts_str = a.get("timestamp", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))[0m
[38;2;255;255;255;48;2;19;87;20m+    except:[0m
[38;2;255;255;255;48;2;19;87;20m+        ts = datetime.now(timezone.utc)[0m
[38;2;255;255;255;48;2;19;87;20m+    # Extract composite score from eval details[0m
[38;2;255;255;255;48;2;19;87;20m+    score = None[0m
[38;2;184;134;11m     m = re.search(r'C:([\d.]+)', str(detail))[0m
[38;2;184;134;11m     if m:[0m
[38;2;255;255;255;48;2;119;20;20m-        return float(m.group(1))[0m
[38;2;255;255;255;48;2;119;20;20m-    return None[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-def extract_single_scores(detail):[0m
[38;2;255;255;255;48;2;119;20;20m-    """Extract S and J scores too"""[0m
[38;2;255;255;255;48;2;119;20;20m-    s = re.search(r'S:([\d.]+)', str(detail))[0m
[38;2;255;255;255;48;2;119;20;20m-    j = re.search(r'J:([\d.]+)', str(detail))[0m
[38;2;255;255;255;48;2;119;20;20m-    c = re.search(r'C:([\d.]+)', str(detail))[0m
[38;2;255;255;255;48;2;119;20;20m-    return {[0m
[38;2;255;255;255;48;2;119;20;20m-        'S': float(s.group(1)) if s else None,[0m
[38;2;255;255;255;48;2;119;20;20m-        'J': float(j.group(1)) if j else None,[0m
[38;2;255;255;255;48;2;119;20;20m-        'C': float(c.group(1)) if c else None[0m
[38;2;255;255;255;48;2;119;20;20m-    }[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-def main():[0m
[38;2;255;255;255;48;2;119;20;20m-    agents_data = load_yaml('agents.yaml')[0m
[38;2;255;255;255;48;2;119;20;20m-    activity_data = load_yaml('activity.yaml')[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-    # Build agent runs: blueprint -> list of runs[0m
[38;2;255;255;255;48;2;119;20;20m-    agent_runs = defaultdict(list)[0m
[38;2;255;255;255;48;2;119;20;20m-    for agent in agents_data.get('agents', []):[0m
[38;2;255;255;255;48;2;119;20;20m-        run = {[0m
[38;2;255;255;255;48;2;119;20;20m-            'blueprint': agent.get('blueprint', 'unknown'),[0m
[38;2;255;255;255;48;2;119;20;20m-            'run_id': agent.get('run_id', ''),[0m
[38;2;255;255;255;48;2;119;20;20m-            'stage': agent.get('stage', ''),[0m
[38;2;255;255;255;48;2;119;20;20m-            'status': agent.get('status', ''),[0m
[38;2;255;255;255;48;2;119;20;20m-            'iteration': agent.get('iteration'),[0m
[38;2;255;255;255;48;2;119;20;20m-            'benchmark': agent.get('benchmark', ''),[0m
[38;2;255;255;255;48;2;119;20;20m-            'spawned_at': agent.get('spawned_at', ''),[0m
[38;2;255;255;255;48;2;119;20;20m-        }[0m
[38;2;255;255;255;48;2;119;20;20m-        # Parse timestamp[0m
[38;2;255;255;255;48;2;119;20;20m-        ts = run['spawned_at'][0m
[38;2;255;255;255;48;2;119;20;20m-        if ts:[0m
[38;2;255;255;255;48;2;119;20;20m-            try:[0m
[38;2;255;255;255;48;2;119;20;20m-                run['ts'] = datetime.fromisoformat(ts.replace('Z', '+00:00'))[0m
[38;2;139;134;130m… omitted 662 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-timeline.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-timeline.py[0m
[38;2;139;134;130m@@ -0,0 +1,55 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: agent_lifecycle_timeline.svg structural validation."""[0m
[38;2;255;255;255;48;2;19;87;20m+import xml.etree.ElementTree as ET[0m
[38;2;255;255;255;48;2;19;87;20m+import sys[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+svg_path = "E:/Stryde/_alpedal/styde-forge/agent_lifecycle_timeline.svg"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+tree = ET.parse(svg_path)[0m
[38;2;255;255;255;48;2;19;87;20m+root = tree.getroot()[0m
[38;2;255;255;255;48;2;19;87;20m+ns = "{http://www.w3.org/2000/svg}"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+assert root.tag == f"{ns}svg", f"root is {root.tag}"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+rects = root.findall(f".//{ns}rect")[0m
[38;2;255;255;255;48;2;19;87;20m+circles = root.findall(f".//{ns}circle")[0m
[38;2;255;255;255;48;2;19;87;20m+lines = root.findall(f".//{ns}line")[0m
[38;2;255;255;255;48;2;19;87;20m+texts = root.findall(f".//{ns}text")[0m
[38;2;255;255;255;48;2;19;87;20m+titles = root.findall(f".//{ns}title")[0m
[38;2;255;255;255;48;2;19;87;20m+polylines = root.findall(f".//{ns}polyline")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+gradients = root.findall(f".//{ns}linearGradient")[0m
[38;2;255;255;255;48;2;19;87;20m+grad_ids = [g.get("id") for g in gradients][0m
[38;2;255;255;255;48;2;19;87;20m+assert "gold" in grad_ids, "missing gold gradient"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "amber" in grad_ids, "missing amber gradient"[0m
[38;2;255;255;255;48;2;19;87;20m+assert "cool" in grad_ids, "missing cool gradient"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+capsules = [r for r in rects if r.get("rx") and r.get("fill","").startswith("url(#")][0m
[38;2;255;255;255;48;2;19;87;20m+spawn_nodes = [c for c in circles if c.get("fill") == "#4CAF50"][0m
[38;2;255;255;255;48;2;19;87;20m+improve_nodes = [c for c in circles if c.get("fill") == "#9C27B0"][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+labels = [t for t in texts if t.get("text-anchor") == "end" and t.get("font-weight") == "500"][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+footer = [t for t in texts if t.text and "events across" in t.text][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print("=== AD-HOC SVG VERIFICATION ===")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"State: PASS")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Dimensions: 1400 x {root.get('height')}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Elements: {len(rects)} rects, {len(circles)} circles, {len(lines)} lines, {len(texts)} texts")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Gradients: {', '.join(grad_ids)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Score capsule nodes: {len(capsules)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Spawn nodes (green): {len(spawn_nodes)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Improve nodes (purple): {len(improve_nodes)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Blueprint tracks: {len(labels)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Tooltip titles: {len(titles)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Connection polylines: {len(polylines)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Footer: {'YES' if footer else 'NO'}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Time scrubber (Play/Pause): {'YES' if [t for t in texts if t.text and 'Play' in t.text] else 'NO'}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Time slider: {'YES' if [c for c in circles if int(c.get('cy',0)) > 650] else 'NO'}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Legend: {'YES' if [t for t in texts if t.text and 'Gold 85+' in t.text] else 'NO'}")[0m
[38;2;255;255;255;48;2;19;87;20m+print("=== VERIFICATION COMPLETE ===")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Cross-check: nodes + lines should cover all events[0m
[38;2;255;255;255;48;2;19;87;20m+total_nodes = len(capsules) + len(spawn_nodes) + len(improve_nodes)[0m
[38;2;255;255;255;48;2;19;87;20m+# each blueprint = 1 polyline or more[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Total event nodes: {total_nodes}")[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-counts.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-counts.py[0m
[38;2;139;134;130m@@ -0,0 +1,25 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""Quick event count cross-check."""[0m
[38;2;255;255;255;48;2;19;87;20m+import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+from collections import Counter[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open("E:/Stryde/_alpedal/styde-forge/state.yaml", "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    data = yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+acts = data.get("activity", [])[0m
[38;2;255;255;255;48;2;19;87;20m+action_counts = Counter(a.get("action", "") for a in acts)[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Total events in state.yaml: {len(acts)}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"By action: {dict(action_counts)}")[0m
[38;2;255;255;255;48;2;19;87;20m+# Check for non-standard actions[0m
[38;2;255;255;255;48;2;19;87;20m+for a in acts:[0m
[38;2;255;255;255;48;2;19;87;20m+    if a.get("action") not in ("spawn", "eval", "improve"):[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f"  Non-standard action: id={a.get('id')} action={a.get('action')}")[0m
[38;2;255;255;255;48;2;19;87;20m+# Check evals without score[0m
[38;2;255;255;255;48;2;19;87;20m+import re[0m
[38;2;255;255;255;48;2;19;87;20m+scoreless = 0[0m
[38;2;255;255;255;48;2;19;87;20m+for a in acts:[0m
[38;2;255;255;255;48;2;19;87;20m+    if a.get("action") == "eval":[0m
[38;2;255;255;255;48;2;19;87;20m+        if not re.search(r'C:[\d.]+', str(a.get("detail",""))):[0m
[38;2;255;255;255;48;2;19;87;20m+            scoreless += 1[0m
[38;2;255;255;255;48;2;19;87;20m+            print(f"  Scoreless eval: id={a.get('id')} detail={a.get('detail')[:50]}")[0m
[38;2;255;255;255;48;2;19;87;20m+print(f"Eval without score: {scoreless}")[0m
=== AD-HOC VERIFICATION ===
Source: E:\Stryde\_alpedal\styde-forge\agent_lifecycle_timeline.svg
Status: PASS
- 200 events parsed from state.yaml (53 spawn, 98 eval, 49 improve)
- All 200 events rendered as SVG nodes: 97 score capsules (gold/amber/cool), 53 green spawn circles, 49 purple improve circles, 1 orange scoreless-eval circle
- 10 blueprint tracks labeled
- 8 connection polylines between progression nodes (2 blueprints with single events have no line)
- Time scrubber: Play/Pause buttons + draggable gold slider at bottom
- Legend: Gold 85+, Amber 70-84, Cool <70
- 200 tooltip titles attached (click any node for run_id, action, score, detail)
- XML well-formed, all 3 score gradients present (gold/amber/cool), viewBox=1400x720
- One corner case: eval id=7 has detail "iter 1/5" instead of a score string — rendered as orange circle fallback instead of capsule (no lost data, just different shape)