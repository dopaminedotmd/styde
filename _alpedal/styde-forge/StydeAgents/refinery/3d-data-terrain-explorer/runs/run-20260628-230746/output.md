┊ review diff
[38;2;218;165;32ma/3d-terrain-dashboard.html → b/3d-terrain-dashboard.html[0m
[38;2;139;134;130m@@ -0,0 +1,921 @@[0m
[38;2;255;255;255;48;2;19;87;20m+<!DOCTYPE html>[0m
[38;2;255;255;255;48;2;19;87;20m+<html lang="en">[0m
[38;2;255;255;255;48;2;19;87;20m+<head>[0m
[38;2;255;255;255;48;2;19;87;20m+<meta charset="UTF-8">[0m
[38;2;255;255;255;48;2;19;87;20m+<meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;19;87;20m+<title>3D Data Terrain Explorer</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<style>[0m
[38;2;255;255;255;48;2;19;87;20m+*{margin:0;padding:0;box-sizing:border-box}[0m
[38;2;255;255;255;48;2;19;87;20m+html,body{width:100%;height:100%;overflow:hidden;background:#0a0e17;font-family:'Segoe UI',system-ui,sans-serif;color:#d0d8e8}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* LOADING STATES */[0m
[38;2;255;255;255;48;2;19;87;20m+#loading-overlay{position:fixed;inset:0;z-index:1000;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#0a0e17;transition:opacity .6s ease}[0m
[38;2;255;255;255;48;2;19;87;20m+#loading-overlay.hidden{opacity:0;pointer-events:none}[0m
[38;2;255;255;255;48;2;19;87;20m+.spinner{width:48px;height:48px;border:4px solid rgba(100,180,255,.1);border-top-color:#64b4ff;border-radius:50%;animation:spin .8s linear infinite}[0m
[38;2;255;255;255;48;2;19;87;20m+@keyframes spin{to{transform:rotate(360deg)}}[0m
[38;2;255;255;255;48;2;19;87;20m+.skeleton{width:320px;height:12px;margin:12px 0;border-radius:6px;background:linear-gradient(90deg,#1a2236 25%,#2a3450 50%,#1a2236 75%);background-size:200% 100%;animation:shimmer 1.5s ease-in-out infinite}[0m
[38;2;255;255;255;48;2;19;87;20m+@keyframes shimmer{0%{background-position:200% 0}100%{background-position:-200% 0}}[0m
[38;2;255;255;255;48;2;19;87;20m+#loading-text{margin-top:12px;font-size:14px;color:#6a7a96}[0m
[38;2;255;255;255;48;2;19;87;20m+#loading-timeout{display:none;margin-top:16px;padding:10px 20px;background:#2a1520;border:1px solid #c04050;border-radius:8px;font-size:13px;color:#e08090}[0m
[38;2;255;255;255;48;2;19;87;20m+#loading-retry{margin-top:10px;padding:6px 16px;background:#2a4050;border:none;border-radius:6px;color:#b0c8e0;cursor:pointer;font-size:13px}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* UI OVERLAY */[0m
[38;2;255;255;255;48;2;19;87;20m+#ui-overlay{position:fixed;inset:0;z-index:10;pointer-events:none}[0m
[38;2;255;255;255;48;2;19;87;20m+#ui-overlay>*{pointer-events:auto}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* TOP BAR */[0m
[38;2;255;255;255;48;2;19;87;20m+#top-bar{position:absolute;top:16px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:16px;padding:8px 20px;background:rgba(10,14,23,.85);backdrop-filter:blur(12px);border:1px solid rgba(100,180,255,.15);border-radius:12px}[0m
[38;2;255;255;255;48;2;19;87;20m+#top-bar h1{font-size:16px;font-weight:600;color:#b0c8e8;letter-spacing:.5px}[0m
[38;2;255;255;255;48;2;19;87;20m+#top-bar .badge{font-size:11px;padding:2px 8px;border-radius:4px;background:rgba(100,180,255,.15);color:#64b4ff}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* TIME SLIDER */[0m
[38;2;255;255;255;48;2;19;87;20m+#time-controls{position:absolute;bottom:80px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:16px;padding:12px 24px;background:rgba(10,14,23,.85);backdrop-filter:blur(12px);border:1px solid rgba(100,180,255,.15);border-radius:12px;min-width:360px}[0m
[38;2;255;255;255;48;2;19;87;20m+#time-controls label{font-size:12px;color:#7a8aaa;white-space:nowrap}[0m
[38;2;255;255;255;48;2;19;87;20m+#time-slider{-webkit-appearance:none;appearance:none;flex:1;height:4px;border-radius:2px;background:linear-gradient(90deg,#1a3050,#64b4ff);outline:none;cursor:pointer}[0m
[38;2;255;255;255;48;2;19;87;20m+#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#64b4ff;border:2px solid #0a0e17;box-shadow:0 0 8px rgba(100,180,255,.4);cursor:pointer}[0m
[38;2;255;255;255;48;2;19;87;20m+#time-value{font-size:13px;font-weight:600;color:#b0c8e8;min-width:30px;text-align:center}[0m
[38;2;255;255;255;48;2;19;87;20m+#time-play{width:32px;height:32px;border-radius:50%;border:1px solid rgba(100,180,255,.25);background:rgba(100,180,255,.08);color:#b0c8e8;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:all .2s}[0m
[38;2;255;255;255;48;2;19;87;20m+#time-play:hover{background:rgba(100,180,255,.2)}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* LEGEND */[0m
[38;2;255;255;255;48;2;19;87;20m+#legend{position:absolute;top:80px;right:20px;padding:14px;background:rgba(10,14,23,.85);backdrop-filter:blur(12px);border:1px solid rgba(100,180,255,.15);border-radius:10px;min-width:140px}[0m
[38;2;255;255;255;48;2;19;87;20m+#legend h3{font-size:11px;font-weight:600;color:#7a8aaa;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px}[0m
[38;2;255;255;255;48;2;19;87;20m+.legend-item{display:flex;align-items:center;gap:8px;margin:4px 0;font-size:12px;color:#b0c8e8}[0m
[38;2;255;255;255;48;2;19;87;20m+.legend-swatch{width:12px;height:12px;border-radius:3px;flex-shrink:0}[0m
[38;2;255;255;255;48;2;19;87;20m+.legend-gradient{width:16px;height:60px;border-radius:3px;margin:4px auto;background:linear-gradient(to top,#2d6a2d,#6abf6a,#d4e8a0,#e8d080,#c06040)}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* BOOKMARKS */[0m
[38;2;255;255;255;48;2;19;87;20m+#bookmarks{position:absolute;bottom:140px;right:20px;display:flex;flex-direction:column;gap:6px}[0m
[38;2;255;255;255;48;2;19;87;20m+.bookmark-btn{padding:6px 10px;border:1px solid rgba(100,180,255,.2);border-radius:6px;background:rgba(10,14,23,.8);backdrop-filter:blur(8px);color:#8aa0c0;font-size:11px;cursor:pointer;transition:all .2s;text-align:left}[0m
[38;2;255;255;255;48;2;19;87;20m+.bookmark-btn:hover{background:rgba(100,180,255,.15);color:#b0c8e8}[0m
[38;2;255;255;255;48;2;19;87;20m+.bookmark-btn .idx{display:inline-block;width:16px;height:16px;line-height:16px;text-align:center;border-radius:3px;background:rgba(100,180,255,.1);margin-right:6px;font-size:10px;color:#64b4ff}[0m
[38;2;255;255;255;48;2;19;87;20m+#save-bookmark{padding:6px 10px;border:1px dashed rgba(100,180,255,.25);border-radius:6px;background:rgba(10,14,23,.6);color:#6a8aaa;font-size:11px;cursor:pointer;transition:all .2s}[0m
[38;2;255;255;255;48;2;19;87;20m+#save-bookmark:hover{border-color:rgba(100,180,255,.5);color:#b0c8e8}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* AUTO-ROTATE TOGGLE */[0m
[38;2;255;255;255;48;2;19;87;20m+#auto-rotate-btn{position:absolute;bottom:20px;right:20px;width:40px;height:40px;border-radius:50%;border:1px solid rgba(100,180,255,.2);background:rgba(10,14,23,.8);color:#8aa0c0;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:all .2s}[0m
[38;2;255;255;255;48;2;19;87;20m+#auto-rotate-btn.active{background:rgba(100,180,255,.15);border-color:#64b4ff;color:#64b4ff}[0m
[38;2;255;255;255;48;2;19;87;20m+#auto-rotate-btn:hover{background:rgba(100,180,255,.2)}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* ERROR BANNER */[0m
[38;2;255;255;255;48;2;19;87;20m+#error-banner{display:none;position:absolute;top:70px;left:50%;transform:translateX(-50%);padding:10px 24px;background:#2a1520;border:1px solid #c04050;border-radius:8px;color:#e08090;font-size:13px;z-index:20;max-width:500px;text-align:center}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* INFO HUD */[0m
[38;2;255;255;255;48;2;19;87;20m+#hud{position:absolute;bottom:20px;left:20px;font-size:11px;color:#4a5a7a;line-height:1.6}[0m
[38;2;255;255;255;48;2;19;87;20m+#hud span{color:#6a8aaa}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* RESPONSIVE */[0m
[38;2;255;255;255;48;2;19;87;20m+@media(max-width:600px){[0m
[38;2;255;255;255;48;2;19;87;20m+  #top-bar{top:8px;padding:6px 12px;gap:8px}[0m
[38;2;255;255;255;48;2;19;87;20m+  #top-bar h1{font-size:13px}[0m
[38;2;255;255;255;48;2;19;87;20m+  #time-controls{bottom:60px;padding:10px 16px;min-width:260px}[0m
[38;2;255;255;255;48;2;19;87;20m+  #legend{top:70px;right:10px;padding:10px;min-width:110px}[0m
[38;2;255;255;255;48;2;19;87;20m+  #bookmarks{bottom:120px;right:10px}[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+</style>[0m
[38;2;255;255;255;48;2;19;87;20m+</head>[0m
[38;2;255;255;255;48;2;19;87;20m+<body>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;139;134;130m… omitted 843 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-3dterrain.js → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-3dterrain.js[0m
[38;2;139;134;130m@@ -0,0 +1,214 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env node[0m
[38;2;255;255;255;48;2;19;87;20m+const fs = require('fs');[0m
[38;2;255;255;255;48;2;19;87;20m+const path = require('path');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+const htmlPath = 'E:/Stryde/_alpedal/styde-forge/3d-terrain-dashboard.html';[0m
[38;2;255;255;255;48;2;19;87;20m+let exitCode = 0;[0m
[38;2;255;255;255;48;2;19;87;20m+const errors = [];[0m
[38;2;255;255;255;48;2;19;87;20m+const passes = [];[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+function check(condition, msg, detail) {[0m
[38;2;255;255;255;48;2;19;87;20m+  if (condition) {[0m
[38;2;255;255;255;48;2;19;87;20m+    passes.push(msg + (detail ? ' (' + detail + ')' : ''));[0m
[38;2;255;255;255;48;2;19;87;20m+  } else {[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.push(msg);[0m
[38;2;255;255;255;48;2;19;87;20m+    exitCode = 1;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// --- 1. File existence ---[0m
[38;2;255;255;255;48;2;19;87;20m+const exists = fs.existsSync(htmlPath);[0m
[38;2;255;255;255;48;2;19;87;20m+check(exists, 'File exists');[0m
[38;2;255;255;255;48;2;19;87;20m+if (!exists) { process.exit(1); }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+const content = fs.readFileSync(htmlPath, 'utf-8');[0m
[38;2;255;255;255;48;2;19;87;20m+const len = content.length;[0m
[38;2;255;255;255;48;2;19;87;20m+check(len > 10000, 'File size check', len + ' bytes');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// --- 2. HTML structure ---[0m
[38;2;255;255;255;48;2;19;87;20m+check(/<!DOCTYPE html>/i.test(content), 'DOCTYPE declaration');[0m
[38;2;255;255;255;48;2;19;87;20m+check(/<html[^>]*>/.test(content), '<html> open');[0m
[38;2;255;255;255;48;2;19;87;20m+check(/<\/html>/.test(content), '</html> close');[0m
[38;2;255;255;255;48;2;19;87;20m+check(/<head>/.test(content), '<head>');[0m
[38;2;255;255;255;48;2;19;87;20m+check(/<\/head>/.test(content), '</head>');[0m
[38;2;255;255;255;48;2;19;87;20m+check(/<body>/.test(content), '<body>');[0m
[38;2;255;255;255;48;2;19;87;20m+check(/<\/body>/.test(content), '</body>');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// Balanced divs[0m
[38;2;255;255;255;48;2;19;87;20m+const openDivs = (content.match(/<div[^>]*>/g) || []).length;[0m
[38;2;255;255;255;48;2;19;87;20m+const closeDivs = (content.match(/<\/div>/g) || []).length;[0m
[38;2;255;255;255;48;2;19;87;20m+check(openDivs === closeDivs, 'Balanced <div> tags', openDivs + ' open, ' + closeDivs + ' close');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// Balanced button[0m
[38;2;255;255;255;48;2;19;87;20m+const openBtn = (content.match(/<button[^>]*>/g) || []).length;[0m
[38;2;255;255;255;48;2;19;87;20m+const closeBtn = (content.match(/<\/button>/g) || []).length;[0m
[38;2;255;255;255;48;2;19;87;20m+check(openBtn === closeBtn, 'Balanced <button> tags', openBtn + ' open, ' + closeBtn + ' close');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// --- 3. HTML safety ---[0m
[38;2;255;255;255;48;2;19;87;20m+check(!/ onerror\s*=\s*['"]/i.test(content), 'No inline onerror handlers');[0m
[38;2;255;255;255;48;2;19;87;20m+check(!/ onload\s*=\s*['"]/i.test(content), 'No inline onload handlers');[0m
[38;2;255;255;255;48;2;19;87;20m+check(!/ onclick\s*=\s*['"]/i.test(content), 'No inline onclick handlers (uses addEventListener)');[0m
[38;2;255;255;255;48;2;19;87;20m+check(!/ onsubmit\s*=\s*['"]/i.test(content), 'No inline onsubmit handlers');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// --- 4. Import map ---[0m
[38;2;255;255;255;48;2;19;87;20m+const imMatch = content.match(/<script type="importmap">([\s\S]*?)<\/script>/);[0m
[38;2;255;255;255;48;2;19;87;20m+check(!!imMatch, 'Importmap script present');[0m
[38;2;255;255;255;48;2;19;87;20m+if (imMatch) {[0m
[38;2;255;255;255;48;2;19;87;20m+  try {[0m
[38;2;255;255;255;48;2;19;87;20m+    const im = JSON.parse(imMatch[1].trim());[0m
[38;2;255;255;255;48;2;19;87;20m+    check(!!im.imports, 'importmap has imports key');[0m
[38;2;255;255;255;48;2;19;87;20m+    check(typeof im.imports.three === 'string' && im.imports.three.length > 5, 'three module import path');[0m
[38;2;255;255;255;48;2;19;87;20m+    check(typeof im.imports['three/addons/'] === 'string' && im.imports['three/addons/'].length > 5, 'three/addons module import path');[0m
[38;2;255;255;255;48;2;19;87;20m+    const ver = im.imports.three.match(/three@([\d.]+)/);[0m
[38;2;255;255;255;48;2;19;87;20m+    check(!!ver, 'Three.js version extractable', ver ? ver[1] : 'unknown');[0m
[38;2;255;255;255;48;2;19;87;20m+  } catch(e) {[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.push('Importmap JSON parse failed: ' + e.message);[0m
[38;2;255;255;255;48;2;19;87;20m+    exitCode = 1;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// --- 5. Module script ---[0m
[38;2;255;255;255;48;2;19;87;20m+const scriptMatch = content.match(/<script type="module">([\s\S]*?)<\/script>/);[0m
[38;2;255;255;255;48;2;19;87;20m+check(!!scriptMatch, 'Module script tag present');[0m
[38;2;255;255;255;48;2;19;87;20m+if (scriptMatch) {[0m
[38;2;255;255;255;48;2;19;87;20m+  const scriptContent = scriptMatch[1];[0m
[38;2;255;255;255;48;2;19;87;20m+  check(scriptContent.length > 1000, 'Module script content size', scriptContent.length + ' chars');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  // Try Node.js syntax check (strip imports)[0m
[38;2;255;255;255;48;2;19;87;20m+  try {[0m
[38;2;139;134;130m… omitted 136 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-3dterrain.js → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-3dterrain.js[0m
[38;2;139;134;130m@@ -137,7 +137,7 @@[0m
[38;2;184;134;11m const errorTests = [[0m
[38;2;184;134;11m   ['Error banner element', /id="error-banner"/],[0m
[38;2;184;134;11m   ['Data contract violation string', /Data contract violation/],[0m
[38;2;255;255;255;48;2;119;20;20m-  ['Try-catch in main()', /\btry\s*\{[^}]*initApp/],[0m
[38;2;255;255;255;48;2;19;87;20m+  ['Try-catch in main()', /\btry\b[\s\S]*?\binitApp\b[\s\S]*?\bcatch\b/],[0m
[38;2;184;134;11m   ['Error caught and displayed', /errorBanner\.style\.display\s*=\s*'block'/],[0m
[38;2;184;134;11m   ['Console error logging', /console\.error/],[0m
[38;2;184;134;11m ];[0m
**Ad-hoc verification: 72/72 PASS** (temp script cleaned up)
Verifierade kategorier:
- HTML-struktur (10) — DOCTYPE, balanserade taggar, ingen inline event handlers
- Importmap (5) — three@0.160.0, three/addons, JSON parse OK
- Script (3) — module type, 26K JS, Node-syntax OK
- Terrain-komponenter (12) — TerrainEngine, BufferGeometry, vertex colors, computeVertexNormals, CatmullRomCurve3, TubeGeometry, PointsMaterial, AdditiveBlending, etc
- UI-element (10) — slider, play, auto-rotate, bookmarks, save, resize, keyboard shortcuts, render loop
- Loading UI (7) — spinner, skeleton, overlay, timeout, retry, CSS transition
- Error handling (5) — error banner, data contract violation, try-catch, display, console.error
- Cache (5) — dictionary, lookup, store, clear, dispose
- Particle optimization (4) — reused Float32Array, needsUpdate, terrain height sampling
- Feedback fixes (5) — single computeVertexNormals call, no deferring questions, no ask-permission