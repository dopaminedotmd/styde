┊ review diff
[38;2;218;165;32ma/3d-data-terrain.html → b/3d-data-terrain.html[0m
[38;2;139;134;130m@@ -0,0 +1,644 @@[0m
[38;2;255;255;255;48;2;19;87;20m+<!DOCTYPE html>[0m
[38;2;255;255;255;48;2;19;87;20m+<html lang="en">[0m
[38;2;255;255;255;48;2;19;87;20m+<head>[0m
[38;2;255;255;255;48;2;19;87;20m+<meta charset="UTF-8">[0m
[38;2;255;255;255;48;2;19;87;20m+<meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;19;87;20m+<title>3D Data Terrain Explorer</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<style>[0m
[38;2;255;255;255;48;2;19;87;20m+  * { margin: 0; padding: 0; box-sizing: border-box; }[0m
[38;2;255;255;255;48;2;19;87;20m+  body { overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; }[0m
[38;2;255;255;255;48;2;19;87;20m+  canvas { display: block; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #panel { position: fixed; top: 12px; right: 12px; background: rgba(10,10,25,0.92);[0m
[38;2;255;255;255;48;2;19;87;20m+    color: #c8ccd4; padding: 14px 18px; border-radius: 10px; font-size: 12px;[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid rgba(100,140,220,0.25); min-width: 200px; z-index: 10;[0m
[38;2;255;255;255;48;2;19;87;20m+    backdrop-filter: blur(8px); }[0m
[38;2;255;255;255;48;2;19;87;20m+  #panel h3 { margin: 0 0 8px 0; font-size: 13px; color: #7ea8f0; letter-spacing: 0.5px; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #panel .row { display: flex; justify-content: space-between; margin: 3px 0; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #panel .val { color: #a0d0a0; font-variant-numeric: tabular-nums; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #timeline { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);[0m
[38;2;255;255;255;48;2;19;87;20m+    background: rgba(10,10,25,0.92); padding: 10px 20px; border-radius: 8px;[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid rgba(100,140,220,0.25); z-index: 10; backdrop-filter: blur(8px);[0m
[38;2;255;255;255;48;2;19;87;20m+    display: flex; align-items: center; gap: 10px; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #timeline label { color: #8899bb; font-size: 12px; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #timeslider { width: 240px; accent-color: #4a8cf0; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #timestep { color: #a0c8f0; font-size: 12px; min-width: 40px; text-align: center; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #bookmarks { position: fixed; bottom: 20px; left: 20px; background: rgba(10,10,25,0.92);[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(100,140,220,0.25);[0m
[38;2;255;255;255;48;2;19;87;20m+    z-index: 10; backdrop-filter: blur(8px); display: flex; gap: 6px; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #bookmarks button { background: rgba(60,100,180,0.25); border: 1px solid rgba(100,140,220,0.3);[0m
[38;2;255;255;255;48;2;19;87;20m+    color: #a0c0e0; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #bookmarks button:hover { background: rgba(80,120,200,0.45); }[0m
[38;2;255;255;255;48;2;19;87;20m+  #bookmarks button.save { background: rgba(40,140,70,0.3); border-color: rgba(80,180,100,0.4); }[0m
[38;2;255;255;255;48;2;19;87;20m+  #cache-panel { position: fixed; bottom: 20px; right: 20px; background: rgba(10,10,25,0.92);[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 10px 14px; border-radius: 8px; border: 1px solid rgba(100,140,220,0.25);[0m
[38;2;255;255;255;48;2;19;87;20m+    z-index: 10; backdrop-filter: blur(8px); font-size: 11px; color: #8899aa; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #cache-panel .hit { color: #6ab86a; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #cache-panel .miss { color: #c87040; }[0m
[38;2;255;255;255;48;2;19;87;20m+</style>[0m
[38;2;255;255;255;48;2;19;87;20m+</head>[0m
[38;2;255;255;255;48;2;19;87;20m+<body>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="panel">[0m
[38;2;255;255;255;48;2;19;87;20m+  <h3>Data Terrain</h3>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="row"><span>Revenue peak</span><span class="val" id="revPeak">--</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="row"><span>User density</span><span class="val" id="userDens">--</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="row"><span>Error rate</span><span class="val" id="errRate">--</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="row"><span>API calls/s</span><span class="val" id="apiRate">--</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="row"><span>FPS</span><span class="val" id="fps">--</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+</div>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="timeline">[0m
[38;2;255;255;255;48;2;19;87;20m+  <label>Time</label>[0m
[38;2;255;255;255;48;2;19;87;20m+  <input type="range" id="timeslider" min="0" max="9" value="0" step="1">[0m
[38;2;255;255;255;48;2;19;87;20m+  <span id="timestep">Day 1</span>[0m
[38;2;255;255;255;48;2;19;87;20m+</div>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="bookmarks">[0m
[38;2;255;255;255;48;2;19;87;20m+  <button class="save" id="saveBm">Save View</button>[0m
[38;2;255;255;255;48;2;19;87;20m+</div>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="cache-panel">[0m
[38;2;255;255;255;48;2;19;87;20m+  <div>Terrain: <span class="hit" id="cacheTerrain">0h/0m</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div>Rivers: <span class="hit" id="cacheRivers">0h/0m</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div>VertColors: <span class="hit" id="cacheColors">0h/0m</span></div>[0m
[38;2;255;255;255;48;2;19;87;20m+</div>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<script type="importmap">[0m
[38;2;255;255;255;48;2;19;87;20m+{[0m
[38;2;255;255;255;48;2;19;87;20m+  "imports": {[0m
[38;2;255;255;255;48;2;19;87;20m+    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",[0m
[38;2;255;255;255;48;2;19;87;20m+    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+</script>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<script type="module">[0m
[38;2;255;255;255;48;2;19;87;20m+import * as THREE from 'three';[0m
[38;2;255;255;255;48;2;19;87;20m+import { OrbitControls } from 'three/addons/controls/OrbitControls.js';[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;139;134;130m… omitted 566 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-terrain.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-terrain.py[0m
[38;2;139;134;130m@@ -0,0 +1,96 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Verify 3d-data-terrain.html — structural, JS syntax, feature completeness."""[0m
[38;2;255;255;255;48;2;19;87;20m+import re, sys[0m
[38;2;255;255;255;48;2;19;87;20m+from pathlib import Path[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+html_path = Path(r"E:\Stryde\_alpedal\styde-forge\3d-data-terrain.html")[0m
[38;2;255;255;255;48;2;19;87;20m+html = html_path.read_text(encoding="utf-8")[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. Structural[0m
[38;2;255;255;255;48;2;19;87;20m+if not html.strip().startswith("<!DOCTYPE html>"):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("Missing DOCTYPE")[0m
[38;2;255;255;255;48;2;19;87;20m+if not html.rstrip().endswith("</html>"):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("Missing closing </html>")[0m
[38;2;255;255;255;48;2;19;87;20m+if html.count("<script") != html.count("</script>"):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"Unbalanced script tags: {html.count('<script')} vs {html.count('</script>')}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. Extract JS content between <script type="module"> and </script>[0m
[38;2;255;255;255;48;2;19;87;20m+m = re.search(r'<script type="module">(.*?)</script>', html, re.DOTALL)[0m
[38;2;255;255;255;48;2;19;87;20m+if not m:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append("No module script found")[0m
[38;2;255;255;255;48;2;19;87;20m+    js = ""[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    js = m.group(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. Brace balancing[0m
[38;2;255;255;255;48;2;19;87;20m+braces = 0[0m
[38;2;255;255;255;48;2;19;87;20m+pairs = {"{": "}", "(": ")", "[": "]"}[0m
[38;2;255;255;255;48;2;19;87;20m+stack = [][0m
[38;2;255;255;255;48;2;19;87;20m+for i, ch in enumerate(js):[0m
[38;2;255;255;255;48;2;19;87;20m+    if ch in pairs:[0m
[38;2;255;255;255;48;2;19;87;20m+        stack.append(pairs[ch])[0m
[38;2;255;255;255;48;2;19;87;20m+    elif ch in pairs.values():[0m
[38;2;255;255;255;48;2;19;87;20m+        if not stack or stack[-1] != ch:[0m
[38;2;255;255;255;48;2;19;87;20m+            errors.append(f"Unbalanced {ch} at char {i}")[0m
[38;2;255;255;255;48;2;19;87;20m+            break[0m
[38;2;255;255;255;48;2;19;87;20m+        stack.pop()[0m
[38;2;255;255;255;48;2;19;87;20m+if stack:[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"Unclosed delimiters: {stack[-5:]}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. Key functions present[0m
[38;2;255;255;255;48;2;19;87;20m+required_fns = [[0m
[38;2;255;255;255;48;2;19;87;20m+    "function generateDataset",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function buildTerrainGeometry",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function getTerrain",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function findErrorPath",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function buildRiverGeometry",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function getRiver",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function scheduleRiver",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function spawnParticle",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function initParticles",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function updateParticles",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function setTimeStep",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function saveBookmark",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function goBookmark",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function animate",[0m
[38;2;255;255;255;48;2;19;87;20m+    "function updateFps",[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+for fn in required_fns:[0m
[38;2;255;255;255;48;2;19;87;20m+    if fn not in js:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"Missing: {fn}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 5. Key patterns[0m
[38;2;255;255;255;48;2;19;87;20m+checks = {[0m
[38;2;255;255;255;48;2;19;87;20m+    "OrbitControls import": "OrbitControls" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "BufferGeometry": "BufferGeometry" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "cache Map": "new Map()" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "Float32Array reuse": "particlePositions[i3]" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "debounce": "clearTimeout(riverDebounce)" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "vertexColors": "vertexColors: true" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "autoRotate": "autoRotate" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "bookmark animation": "lerpVectors" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "pre-cache loop": "getTerrain(t)" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "TubeGeometry river": "TubeGeometry" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "particle respawn": "p.life >= p.maxLife" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+    "sprite texture": "createRadialGradient" in js,[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+for name, present in checks.items():[0m
[38;2;255;255;255;48;2;19;87;20m+    if not present:[0m
[38;2;139;134;130m… omitted 18 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc-verifiering: PASS
15 funktioner, 12 feature-mönster, balanserade taggar och klamrar, inga geometri-konstruktorer i hot-path (animate/setTimeStep/updateParticles). Temp-script bortstädat.
E:\Stryde\_alpedal\styde-forge\3d-data-terrain.html — öppna i webbläsare, klart.