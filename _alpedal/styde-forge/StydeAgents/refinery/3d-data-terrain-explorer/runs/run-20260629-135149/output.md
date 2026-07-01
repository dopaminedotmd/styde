┊ review diff
[38;2;218;165;32ma/3d-terrain-explorer.html → b/3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -5,70 +5,189 @@[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;184;134;11m <title>3D Data Terrain Explorer</title>[0m
[38;2;184;134;11m <style>[0m
[38;2;255;255;255;48;2;119;20;20m-  *{margin:0;padding:0;box-sizing:border-box}[0m
[38;2;255;255;255;48;2;119;20;20m-  body{overflow:hidden;background:#0a0a14;font-family:'Segoe UI',system-ui,sans-serif}[0m
[38;2;255;255;255;48;2;119;20;20m-  canvas{display:block}[0m
[38;2;255;255;255;48;2;119;20;20m-  #ui{position:fixed;bottom:0;left:0;right:0;padding:12px 16px;[0m
[38;2;255;255;255;48;2;119;20;20m-      background:linear-gradient(transparent,rgba(0,0,0,0.85));[0m
[38;2;255;255;255;48;2;119;20;20m-      display:flex;gap:16px;align-items:center;flex-wrap:wrap;[0m
[38;2;255;255;255;48;2;119;20;20m-      z-index:10;pointer-events:none}[0m
[38;2;255;255;255;48;2;119;20;20m-  #ui>*{pointer-events:auto}[0m
[38;2;255;255;255;48;2;119;20;20m-  #time-slider{flex:1;min-width:200px;max-width:600px;accent-color:#4fc3f7}[0m
[38;2;255;255;255;48;2;119;20;20m-  #time-label{color:#ddd;font-size:13px;min-width:120px;text-align:center}[0m
[38;2;255;255;255;48;2;119;20;20m-  button{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);[0m
[38;2;255;255;255;48;2;119;20;20m-         color:#ddd;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;[0m
[38;2;255;255;255;48;2;119;20;20m-         transition:all 0.2s}[0m
[38;2;255;255;255;48;2;119;20;20m-  button:hover{background:rgba(255,255,255,0.18);border-color:rgba(255,255,255,0.4)}[0m
[38;2;255;255;255;48;2;119;20;20m-  button.active{background:rgba(79,195,247,0.25);border-color:#4fc3f7;color:#4fc3f7;[0m
[38;2;255;255;255;48;2;119;20;20m-                 outline:1px solid rgba(79,195,247,0.5);outline-offset:2px}[0m
[38;2;255;255;255;48;2;119;20;20m-  button.bookmark-active{background:rgba(255,234,0,0.2);border-color:#ffea00;color:#ffea00}[0m
[38;2;255;255;255;48;2;119;20;20m-  #bookmarks{display:flex;gap:4px}[0m
[38;2;255;255;255;48;2;119;20;20m-  #diag{position:fixed;top:10px;right:10px;background:rgba(0,0,0,0.75);[0m
[38;2;255;255;255;48;2;119;20;20m-        color:#aaa;font-size:11px;padding:8px 12px;border-radius:6px;[0m
[38;2;255;255;255;48;2;119;20;20m-        font-family:monospace;z-index:10;line-height:1.5;[0m
[38;2;255;255;255;48;2;119;20;20m-        border:1px solid rgba(255,255,255,0.1)}[0m
[38;2;255;255;255;48;2;119;20;20m-  #diag .val{color:#4fc3f7}[0m
[38;2;255;255;255;48;2;119;20;20m-  #tooltip{position:fixed;pointer-events:none;opacity:0;[0m
[38;2;255;255;255;48;2;119;20;20m-           background:rgba(0,0,0,0.85);color:#fff;font-size:11px;[0m
[38;2;255;255;255;48;2;119;20;20m-           padding:8px 12px;border-radius:4px;border:1px solid rgba(255,255,255,0.2);[0m
[38;2;255;255;255;48;2;119;20;20m-           z-index:20;transition:opacity 0.15s;max-width:200px}[0m
[38;2;255;255;255;48;2;119;20;20m-  #tooltip.pinned{pointer-events:auto;border-color:#ffea00;[0m
[38;2;255;255;255;48;2;119;20;20m-                  background:rgba(10,10,30,0.92)}[0m
[38;2;255;255;255;48;2;119;20;20m-  #tooltip .pin-indicator{display:none;color:#ffea00;margin-left:4px;font-size:10px}[0m
[38;2;255;255;255;48;2;119;20;20m-  #tooltip.pinned .pin-indicator{display:inline}[0m
[38;2;255;255;255;48;2;119;20;20m-  #legend{position:fixed;top:10px;left:10px;background:rgba(0,0,0,0.7);[0m
[38;2;255;255;255;48;2;119;20;20m-          padding:10px;border-radius:6px;z-index:10;font-size:11px;color:#ccc;[0m
[38;2;255;255;255;48;2;119;20;20m-          border:1px solid rgba(255,255,255,0.1);pointer-events:none}[0m
[38;2;255;255;255;48;2;119;20;20m-  .legend-row{display:flex;align-items:center;gap:6px;margin:2px 0}[0m
[38;2;255;255;255;48;2;119;20;20m-  .legend-swatch{width:14px;height:14px;border-radius:3px}[0m
[38;2;255;255;255;48;2;19;87;20m+:root {[0m
[38;2;255;255;255;48;2;19;87;20m+  --bg: #0d1117;[0m
[38;2;255;255;255;48;2;19;87;20m+  --panel-bg: rgba(13,17,23,0.92);[0m
[38;2;255;255;255;48;2;19;87;20m+  --text: #c9d1d9;[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent: #58a6ff;[0m
[38;2;255;255;255;48;2;19;87;20m+  --accent-dim: #1f6feb;[0m
[38;2;255;255;255;48;2;19;87;20m+  --danger: #f85149;[0m
[38;2;255;255;255;48;2;19;87;20m+  --success: #3fb950;[0m
[38;2;255;255;255;48;2;19;87;20m+  --warning: #d2991d;[0m
[38;2;255;255;255;48;2;19;87;20m+  --border: #30363d;[0m
[38;2;255;255;255;48;2;19;87;20m+  --radius: 6px;[0m
[38;2;255;255;255;48;2;19;87;20m+  --font: 'Segoe UI', system-ui, sans-serif;[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+* { margin:0; padding:0; box-sizing:border-box; }[0m
[38;2;255;255;255;48;2;19;87;20m+body { background:var(--bg); overflow:hidden; font-family:var(--font); color:var(--text); }[0m
[38;2;255;255;255;48;2;19;87;20m+#canvas-container { position:fixed; inset:0; z-index:1; }[0m
[38;2;255;255;255;48;2;19;87;20m+#canvas-container canvas { display:block; }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Top bar */[0m
[38;2;255;255;255;48;2;19;87;20m+#top-bar {[0m
[38;2;255;255;255;48;2;19;87;20m+  position:fixed; top:12px; left:12px; right:12px; z-index:10;[0m
[38;2;255;255;255;48;2;19;87;20m+  display:flex; gap:8px; align-items:center; flex-wrap:wrap;[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.panel {[0m
[38;2;255;255;255;48;2;19;87;20m+  background:var(--panel-bg); border:1px solid var(--border);[0m
[38;2;255;255;255;48;2;19;87;20m+  border-radius:var(--radius); padding:8px 12px;[0m
[38;2;255;255;255;48;2;19;87;20m+  backdrop-filter:blur(12px);[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.panel-row { display:flex; gap:8px; align-items:center; }[0m
[38;2;255;255;255;48;2;19;87;20m+.panel-label { font-size:11px; text-transform:uppercase; letter-spacing:0.5px; color:#8b949e; }[0m
[38;2;255;255;255;48;2;19;87;20m+.panel-value { font-size:13px; font-weight:600; }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* Time slider */[0m
[38;2;255;255;255;48;2;19;87;20m+#time-slider-container { flex:1; min-width:200px; max-width:500px; }[0m
[38;2;255;255;255;48;2;19;87;20m+#time-slider {[0m
[38;2;255;255;255;48;2;19;87;20m+  width:100%; height:6px; -webkit-appearance:none; appearance:none;[0m
[38;2;255;255;255;48;2;19;87;20m+  background:var(--border); border-radius:3px; outline:none; cursor:pointer;[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+#time-slider::-webkit-slider-thumb {[0m
[38;2;139;134;130m… omitted 2054 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verification complete (40/40 passed, 0 failed)
Checks covered:
  File integrity: exists, >10KB, valid HTML structure, importmap defined
  Three.js: THREE import, OrbitControls import
  All 10 classes/factories present (CacheManager, ObjectPool, TerrainBuilder, ParticleSystem, RiverBuilder, BookmarkManager, TooltipManager, GridTransform, TerrainExplorer, data generator)
  Zero stubs: no TODO/FIXME/stub/NotImplemented found
  Cache: hit/miss tracking, hitRate(), LRU eviction (50-entry cap), diagnostics panel
  Object pool: acquire/release/factory+resetter, Vector3 pool instantiation
  UX affordances: #tooltip.pinned CSS, pin/unpin logic, Escape handler, .toggle-btn.active CSS with icon transform, classList.toggle calls
  Performance: debounce timer (200ms), BufferGeometry reuse via needsUpdate, in-place updateGeometry(), dispose chains on geometry+materials
  Animation: requestAnimationFrame loop, renderer.render()
  Bookmarks: localStorage persistence, keyboard restore (1-8)
  Time: slider input element, setTimeStep() method
Runtime verification (browser) not possible in this environment. Open 3d-terrain-explorer.html in a modern browser with internet access (Three.js loads from CDN). Expected: terrain renders, orbit controls work, time slider reshapes heights, particles flow, rivers trace error paths, tooltips pin on click, bookmarks save/restore.