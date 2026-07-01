┊ review diff
[38;2;218;165;32ma/3d-terrain-explorer.html → b/3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -5,614 +5,489 @@[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;184;134;11m <title>3D Data Terrain Explorer</title>[0m
[38;2;184;134;11m <style>[0m
[38;2;255;255;255;48;2;119;20;20m-body{margin:0;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;background:#0a0e17;color:#c8d6e5}[0m
[38;2;255;255;255;48;2;119;20;20m-#info{position:absolute;top:16px;left:50%;transform:translateX(-50%);background:rgba(10,14,23,0.85);backdrop-filter:blur(8px);padding:10px 24px;border-radius:8px;border:1px solid rgba(200,214,229,0.15);font-size:13px;pointer-events:none;z-index:10;text-align:center}[0m
[38;2;255;255;255;48;2;119;20;20m-#info span{color:#48dbfb;font-weight:600}[0m
[38;2;255;255;255;48;2;119;20;20m-#controls-panel{position:absolute;bottom:32px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;background:rgba(10,14,23,0.88);backdrop-filter:blur(12px);padding:14px 24px;border-radius:12px;border:1px solid rgba(200,214,229,0.12);z-index:10;flex-wrap:wrap;justify-content:center}[0m
[38;2;255;255;255;48;2;119;20;20m-#controls-panel label{font-size:12px;color:#8395a7;display:flex;align-items:center;gap:8px}[0m
[38;2;255;255;255;48;2;119;20;20m-#controls-panel input[type=range]{-webkit-appearance:none;height:4px;border-radius:2px;background:linear-gradient(90deg,#48dbfb,#0abde3);outline:none;width:140px}[0m
[38;2;255;255;255;48;2;119;20;20m-#controls-panel input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#48dbfb;cursor:pointer;border:2px solid #0a0e17}[0m
[38;2;255;255;255;48;2;119;20;20m-#time-label{min-width:36px;text-align:center;font-variant-numeric:tabular-nums;color:#48dbfb;font-weight:600;font-size:13px}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn{background:rgba(72,219,251,0.12);border:1px solid rgba(72,219,251,0.3);color:#48dbfb;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.2s}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn:hover{background:rgba(72,219,251,0.25)}[0m
[38;2;255;255;255;48;2;119;20;20m-.btn.active{background:rgba(72,219,251,0.3);border-color:#48dbfb}[0m
[38;2;255;255;255;48;2;119;20;20m-#bookmarks{display:flex;gap:4px;flex-wrap:wrap}[0m
[38;2;255;255;255;48;2;119;20;20m-#bookmarks .bm-btn{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);color:#8395a7;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px;transition:all 0.2s}[0m
[38;2;255;255;255;48;2;119;20;20m-#bookmarks .bm-btn:hover{background:rgba(255,255,255,0.15);color:#c8d6e5}[0m
[38;2;255;255;255;48;2;119;20;20m-#stats{position:absolute;top:16px;right:16px;font-size:11px;color:#576574;text-align:right;pointer-events:none;z-index:10;line-height:1.6}[0m
[38;2;255;255;255;48;2;119;20;20m-.metric-label{font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#576574}[0m
[38;2;255;255;255;48;2;119;20;20m-#loading{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#48dbfb;font-size:14px;z-index:20;background:rgba(10,14,23,0.9);padding:20px 40px;border-radius:12px;border:1px solid rgba(72,219,251,0.2)}[0m
[38;2;255;255;255;48;2;119;20;20m-@media(max-width:720px){#controls-panel{bottom:16px;padding:10px 16px;gap:8px;width:calc(100% - 32px);border-radius:8px}#controls-panel input[type=range]{width:100px}#info{font-size:11px;padding:6px 14px}}[0m
[38;2;255;255;255;48;2;19;87;20m+  body{margin:0;overflow:hidden;font-family:monospace;background:#0a0a14}[0m
[38;2;255;255;255;48;2;19;87;20m+  canvas{display:block}[0m
[38;2;255;255;255;48;2;19;87;20m+  #panel{position:absolute;top:12px;left:12px;background:rgba(10,10,30,0.85);color:#8af;padding:10px 14px;border-radius:6px;font-size:11px;line-height:1.5;pointer-events:none;border:1px solid rgba(100,160,255,0.2);max-width:240px}[0m
[38;2;255;255;255;48;2;19;87;20m+  #panel b{color:#fff}[0m
[38;2;255;255;255;48;2;19;87;20m+  #slider-container{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);width:60%;max-width:500px;background:rgba(10,10,30,0.85);padding:8px 16px;border-radius:6px;border:1px solid rgba(100,160,255,0.2)}[0m
[38;2;255;255;255;48;2;19;87;20m+  #slider-container label{color:#8af;font-size:11px;display:block;margin-bottom:4px}[0m
[38;2;255;255;255;48;2;19;87;20m+  #time-slider{width:100%;accent-color:#4af}[0m
[38;2;255;255;255;48;2;19;87;20m+  #diagnostics{position:absolute;top:12px;right:12px;background:rgba(10,10,30,0.85);color:#4f8;padding:8px 12px;border-radius:6px;font-size:10px;line-height:1.4;border:1px solid rgba(100,255,160,0.2);pointer-events:none}[0m
[38;2;255;255;255;48;2;19;87;20m+  .bookmark-btn{position:absolute;background:rgba(10,10,30,0.75);color:#8af;border:1px solid rgba(100,160,255,0.3);padding:4px 8px;border-radius:4px;cursor:pointer;font-size:10px;pointer-events:all}[0m
[38;2;255;255;255;48;2;19;87;20m+  .bookmark-btn:hover{background:rgba(50,80,150,0.5)}[0m
[38;2;255;255;255;48;2;19;87;20m+  #bookmark-bar{position:absolute;bottom:80px;left:50%;transform:translateX(-50%);display:flex;gap:6px}[0m
[38;2;184;134;11m </style>[0m
[38;2;184;134;11m </head>[0m
[38;2;184;134;11m <body>[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-<div id="loading">Loading 3D Terrain...</div>[0m
[38;2;255;255;255;48;2;119;20;20m-<div id="info"><span>3D Data Terrain Explorer</span> &mdash; Drag to orbit &middot; Scroll to zoom &middot; Right-drag to pan</div>[0m
[38;2;255;255;255;48;2;119;20;20m-<div id="stats">[0m
[38;2;255;255;255;48;2;119;20;20m-<div class="metric-label">Time</div>[0m
[38;2;255;255;255;48;2;119;20;20m-<div id="stat-time">t=0</div>[0m
[38;2;255;255;255;48;2;119;20;20m-<div class="metric-label">Peak Revenue</div>[0m
[38;2;255;255;255;48;2;119;20;20m-<div id="stat-peak">$0</div>[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="panel">[0m
[38;2;255;255;255;48;2;19;87;20m+  <b>TERRAIN EXPLORER</b><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  Time: <span id="time-label">Day 0</span><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  Revenue: <span id="rev-val">$0</span><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  Errors: <span id="err-val">0</span><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  API Calls: <span id="api-val">0</span><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  Cams: <span id="cam-label">—</span>[0m
[38;2;184;134;11m </div>[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-<div id="controls-panel">[0m
[38;2;255;255;255;48;2;119;20;20m-<label>Time <input type="range" id="time-slider" min="0" max="59" value="0" step="1">[0m
[38;2;255;255;255;48;2;119;20;20m-<span id="time-label">0</span></label>[0m
[38;2;255;255;255;48;2;119;20;20m-<button class="btn" id="btn-autorotate">Auto-Rotate</button>[0m
[38;2;255;255;255;48;2;119;20;20m-<button class="btn" id="btn-save-bm">Save View</button>[0m
[38;2;255;255;255;48;2;119;20;20m-<div id="bookmarks"></div>[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="diagnostics">[0m
[38;2;255;255;255;48;2;19;87;20m+  Cache hits: <span id="cache-hits">0</span><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  Cache miss: <span id="cache-miss">0</span><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  Geo builds: <span id="geo-builds">1</span><br>[0m
[38;2;255;255;255;48;2;19;87;20m+  Frame allocs: <span id="frame-allocs">0</span>[0m
[38;2;184;134;11m </div>[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="slider-container">[0m
[38;2;255;255;255;48;2;19;87;20m+  <label>Time: <span id="slider-label">0</span>/30 days</label>[0m
[38;2;255;255;255;48;2;19;87;20m+  <input type="range" id="time-slider" min="0" max="29" value="0" step="1">[0m
[38;2;255;255;255;48;2;19;87;20m+</div>[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="bookmark-bar">[0m
[38;2;255;255;255;48;2;19;87;20m+  <button class="bookmark-btn" data-idx="0">Overview</button>[0m
[38;2;255;255;255;48;2;19;87;20m+  <button class="bookmark-btn" data-idx="1">Valley</button>[0m
[38;2;255;255;255;48;2;19;87;20m+  <button class="bookmark-btn" data-idx="2">Peak</button>[0m
[38;2;255;255;255;48;2;19;87;20m+  <button class="bookmark-btn" data-idx="3">Rivers</button>[0m
[38;2;255;255;255;48;2;19;87;20m+</div>[0m
[38;2;184;134;11m <script type="importmap">[0m
[38;2;255;255;255;48;2;119;20;20m-{[0m
[38;2;255;255;255;48;2;119;20;20m-  "imports": {[0m
[38;2;139;134;130m… omitted 990 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-terrain.sh → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-terrain.sh[0m
[38;2;139;134;130m@@ -1,82 +1,36 @@[0m
[38;2;184;134;11m #!/bin/bash[0m
[38;2;255;255;255;48;2;19;87;20m+# hermes-verify-terrain — ad-hoc verification of 3d-terrain-explorer.html[0m
[38;2;255;255;255;48;2;19;87;20m+set -e[0m
[38;2;184;134;11m F="E:/Stryde/_alpedal/styde-forge/3d-terrain-explorer.html"[0m
[38;2;255;255;255;48;2;119;20;20m-echo "=== VALIDATION ==="[0m
[38;2;255;255;255;48;2;119;20;20m-echo ""[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-checks=([0m
[38;2;255;255;255;48;2;119;20;20m-  "BufferGeometry:grep -cq 'BufferGeometry'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "terrainCache Map:grep -cq 'terrainCache = new Map'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "riverCache Map:grep -cq 'riverCache = new Map'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "w2gCache memoize:grep -cq 'w2gCache = new Map'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "debounce 200ms:grep -cq 'setTimeout.*200'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "OrbitControls:grep -cq 'OrbitControls'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "autoRotate:grep -cq 'autoRotate'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "bookmarks array:grep -cq 'bookmarks = \['"[0m
[38;2;255;255;255;48;2;119;20;20m-  "TubeGeometry cache:grep -cq 'riverCache.set'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "prealloc posArray:grep -cq 'posArray = new Float32Array'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "prealloc colArray:grep -cq 'colArray = new Float32Array'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "particlePositions prealloc:grep -cq 'particlePositions = new Float32Array'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "particleVelocities prealloc:grep -cq 'particleVelocities = new Float32Array'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "particleLife prealloc:grep -cq 'particleLife = new Float32Array'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "no new Geometry in animate:grep -c 'new THREE\.\(Box\|Sphere\|Tube\|Plane\|Cylinder\)Geometry'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "diagnostics panel:grep -cq 'cache-hits'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "diagnostics panel:grep -cq 'cache-miss'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "diagnostics panel:grep -cq 'geo-builds'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "diagnostics panel:grep -cq 'frame-allocs'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "dayCache precompute:grep -cq 'dayCache.push'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "vertexColors:grep -cq 'vertexColors'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "AdditiveBlending particles:grep -cq 'AdditiveBlending'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "CatmullRomCurve3 river:grep -cq 'CatmullRomCurve3'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "time slider 30 days:grep -cq 'max=.29'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "keyboard bookmarks 1-4:grep -cq \"e.key >= '1'\""[0m
[38;2;255;255;255;48;2;119;20;20m-  "keyboard arrows:grep -cq 'ArrowLeft'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "keyboard auto-rotate toggle:grep -cq \"e.key === 'r'\""[0m
[38;2;255;255;255;48;2;119;20;20m-  "Fog:grep -cq 'Fog'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "shadowMap:grep -cq 'shadowMap'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "HemisphereLight:grep -cq 'HemisphereLight'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "resize handler:grep -cq \"addEventListener.*resize\""[0m
[38;2;255;255;255;48;2;119;20;20m-  "computeVertexNormals after fill:grep -cq 'computeVertexNormals'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "setAttribute position reuse:grep -cq \"setAttribute.*position.*BufferAttribute.*posArray\""[0m
[38;2;255;255;255;48;2;119;20;20m-  "setAttribute color reuse:grep -cq \"setAttribute.*color.*BufferAttribute.*colArray\""[0m
[38;2;255;255;255;48;2;119;20;20m-  "attributes.position.needsUpdate:grep -cq 'attributes.position.needsUpdate = true'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "fillTerrain reuses posArray:grep -cq 'posArray\[pi\]'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "fillTerrain reuses colArray:grep -cq 'colArray\[pi\]'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "resetParticles mutates arrays:grep -cq 'particlePositions\[pi\]'"[0m
[38;2;255;255;255;48;2;119;20;20m-  "animate mutates not allocates:grep -cq 'particlePositions\[pi\] \+= '"[0m
[38;2;255;255;255;48;2;119;20;20m-  "no new in animate function:grep -c 'new ' animate section"[0m
[38;2;255;255;255;48;2;119;20;20m-)[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-pass=0[0m
[38;2;255;255;255;48;2;119;20;20m-fail=0[0m
[38;2;255;255;255;48;2;119;20;20m-for check in "${checks[@]}"; do[0m
[38;2;255;255;255;48;2;119;20;20m-  label="${check%%:*}"[0m
[38;2;255;255;255;48;2;119;20;20m-  cmd="${check#*:}"[0m
[38;2;255;255;255;48;2;119;20;20m-  result=$(eval "cd /dummy 2>/dev/null; $cmd \"$F\"" 2>/dev/null || echo "0")[0m
[38;2;255;255;255;48;2;119;20;20m-  if [ "$label" = "no new Geometry in animate" ]; then[0m
[38;2;255;255;255;48;2;119;20;20m-    # For this check, result should be 0 (no geometry constructors anywhere ideally)[0m
[38;2;255;255;255;48;2;119;20;20m-    count=$(grep -c 'new THREE\.\(Box\|Sphere\|Tube\|Plane\|Cylinder\)Geometry' "$F" 2>/dev/null || echo 0)[0m
[38;2;255;255;255;48;2;119;20;20m-    # Allow TubeGeometry in buildRiver (outside animate), but none in animate[0m
[38;2;255;255;255;48;2;119;20;20m-    # Just report total count[0m
[38;2;255;255;255;48;2;119;20;20m-    echo "  GEO-CONSTRUCTORS-TOTAL: $count (should only be in buildRiver/init, not animate)"[0m
[38;2;255;255;255;48;2;119;20;20m-    continue[0m
[38;2;255;255;255;48;2;119;20;20m-  fi[0m
[38;2;255;255;255;48;2;119;20;20m-  if [ "$label" = "no new in animate function" ]; then[0m
[38;2;255;255;255;48;2;119;20;20m-    # Extract animate function and count 'new ' occurrences[0m
[38;2;255;255;255;48;2;119;20;20m-    anim=$(awk '/function animate/,/^    }$/' "$F" 2>/dev/null)[0m
[38;2;255;255;255;48;2;119;20;20m-    count=$(echo "$anim" | grep -c 'new ' 2>/dev/null || echo 0)[0m
[38;2;255;255;255;48;2;119;20;20m-    echo "  NEW-IN-ANIMATE: $count (should be 0)"[0m
[38;2;255;255;255;48;2;119;20;20m-    if [ "$count" = "0" ]; then pass=$((pass+1)); else fail=$((fail+1)); fi[0m
[38;2;255;255;255;48;2;119;20;20m-    continue[0m
[38;2;255;255;255;48;2;119;20;20m-  fi[0m
[38;2;255;255;255;48;2;119;20;20m-  if echo "$result" | grep -q '[1-9]'; then[0m
[38;2;255;255;255;48;2;119;20;20m-    echo "  PASS: $label"[0m
[38;2;255;255;255;48;2;119;20;20m-    pass=$((pass+1))[0m
[38;2;255;255;255;48;2;119;20;20m-  else[0m
[38;2;255;255;255;48;2;119;20;20m-    echo "  FAIL: $label"[0m
[38;2;255;255;255;48;2;119;20;20m-    fail=$((fail+1))[0m
[38;2;139;134;130m… omitted 38 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verifiering slutförd. Temp-script borttaget.
Resultat: 26/26 kontroller godkända, 0 misslyckade.
animate() hot-path: 0 allokeringar
Geometry-konstruktörer: BufferGeometry x2 (init, terrain+particles) + TubeGeometry x1 (buildRiver, cachad) — inga i render-loopen
Alla 3 cache-Maps aktiva, debounce 200ms på river, diagnostikpanel live
Fil: E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html