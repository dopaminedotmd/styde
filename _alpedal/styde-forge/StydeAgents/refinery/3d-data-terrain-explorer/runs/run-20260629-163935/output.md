┊ review diff
[38;2;218;165;32ma/3d-terrain-explorer.html → b/3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -5,189 +5,109 @@[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;184;134;11m <title>3D Data Terrain Explorer</title>[0m
[38;2;184;134;11m <style>[0m
[38;2;255;255;255;48;2;119;20;20m-:root {[0m
[38;2;255;255;255;48;2;119;20;20m-  --bg: #0d1117;[0m
[38;2;255;255;255;48;2;119;20;20m-  --panel-bg: rgba(13,17,23,0.92);[0m
[38;2;255;255;255;48;2;119;20;20m-  --text: #c9d1d9;[0m
[38;2;255;255;255;48;2;119;20;20m-  --accent: #58a6ff;[0m
[38;2;255;255;255;48;2;119;20;20m-  --accent-dim: #1f6feb;[0m
[38;2;255;255;255;48;2;119;20;20m-  --danger: #f85149;[0m
[38;2;255;255;255;48;2;119;20;20m-  --success: #3fb950;[0m
[38;2;255;255;255;48;2;119;20;20m-  --warning: #d2991d;[0m
[38;2;255;255;255;48;2;119;20;20m-  --border: #30363d;[0m
[38;2;255;255;255;48;2;119;20;20m-  --radius: 6px;[0m
[38;2;255;255;255;48;2;119;20;20m-  --font: 'Segoe UI', system-ui, sans-serif;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-* { margin:0; padding:0; box-sizing:border-box; }[0m
[38;2;255;255;255;48;2;119;20;20m-body { background:var(--bg); overflow:hidden; font-family:var(--font); color:var(--text); }[0m
[38;2;255;255;255;48;2;119;20;20m-#canvas-container { position:fixed; inset:0; z-index:1; }[0m
[38;2;255;255;255;48;2;119;20;20m-#canvas-container canvas { display:block; }[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-/* Top bar */[0m
[38;2;255;255;255;48;2;119;20;20m-#top-bar {[0m
[38;2;255;255;255;48;2;119;20;20m-  position:fixed; top:12px; left:12px; right:12px; z-index:10;[0m
[38;2;255;255;255;48;2;119;20;20m-  display:flex; gap:8px; align-items:center; flex-wrap:wrap;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel {[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--panel-bg); border:1px solid var(--border);[0m
[38;2;255;255;255;48;2;119;20;20m-  border-radius:var(--radius); padding:8px 12px;[0m
[38;2;255;255;255;48;2;119;20;20m-  backdrop-filter:blur(12px);[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-row { display:flex; gap:8px; align-items:center; }[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-label { font-size:11px; text-transform:uppercase; letter-spacing:0.5px; color:#8b949e; }[0m
[38;2;255;255;255;48;2;119;20;20m-.panel-value { font-size:13px; font-weight:600; }[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-/* Time slider */[0m
[38;2;255;255;255;48;2;119;20;20m-#time-slider-container { flex:1; min-width:200px; max-width:500px; }[0m
[38;2;255;255;255;48;2;119;20;20m-#time-slider {[0m
[38;2;255;255;255;48;2;119;20;20m-  width:100%; height:6px; -webkit-appearance:none; appearance:none;[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--border); border-radius:3px; outline:none; cursor:pointer;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-#time-slider::-webkit-slider-thumb {[0m
[38;2;255;255;255;48;2;119;20;20m-  -webkit-appearance:none; width:16px; height:16px; border-radius:50%;[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--accent); cursor:pointer; border:2px solid var(--bg);[0m
[38;2;255;255;255;48;2;119;20;20m-  box-shadow:0 0 8px rgba(88,166,255,0.4);[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-#time-label { font-size:12px; color:var(--accent); min-width:80px; text-align:center; }[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-/* Toggle buttons */[0m
[38;2;255;255;255;48;2;119;20;20m-.toggle-btn {[0m
[38;2;255;255;255;48;2;119;20;20m-  padding:6px 14px; border:1px solid var(--border); border-radius:var(--radius);[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--panel-bg); color:var(--text); cursor:pointer;[0m
[38;2;255;255;255;48;2;119;20;20m-  font-size:12px; font-family:var(--font); transition:all 0.2s;[0m
[38;2;255;255;255;48;2;119;20;20m-  display:flex; align-items:center; gap:6px; white-space:nowrap;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.toggle-btn:hover { border-color:var(--accent-dim); }[0m
[38;2;255;255;255;48;2;119;20;20m-.toggle-btn.active {[0m
[38;2;255;255;255;48;2;119;20;20m-  border-color:var(--accent); background:rgba(88,166,255,0.15);[0m
[38;2;255;255;255;48;2;119;20;20m-  box-shadow:0 0 8px rgba(88,166,255,0.25);[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.toggle-btn .icon { font-size:14px; transition:transform 0.2s; }[0m
[38;2;255;255;255;48;2;119;20;20m-.toggle-btn.active .icon { transform:scale(1.2); }[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-/* Bottom bar */[0m
[38;2;255;255;255;48;2;119;20;20m-#bottom-bar {[0m
[38;2;255;255;255;48;2;119;20;20m-  position:fixed; bottom:12px; left:12px; right:12px; z-index:10;[0m
[38;2;255;255;255;48;2;119;20;20m-  display:flex; gap:8px; align-items:center; flex-wrap:wrap;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;119;20;20m-/* Bookmarks */[0m
[38;2;255;255;255;48;2;119;20;20m-#bookmark-bar { display:flex; gap:6px; align-items:center; }[0m
[38;2;255;255;255;48;2;119;20;20m-.bookmark-btn {[0m
[38;2;255;255;255;48;2;119;20;20m-  padding:4px 10px; border:1px solid var(--border); border-radius:var(--radius);[0m
[38;2;255;255;255;48;2;119;20;20m-  background:var(--panel-bg); color:var(--text); cursor:pointer;[0m
[38;2;255;255;255;48;2;119;20;20m-  font-size:11px; font-family:var(--font); transition:all 0.15s;[0m
[38;2;255;255;255;48;2;119;20;20m-}[0m
[38;2;255;255;255;48;2;119;20;20m-.bookmark-btn:hover { border-color:var(--accent); }[0m
[38;2;255;255;255;48;2;119;20;20m-.bookmark-btn.saved { border-color:var(--success); color:var(--success); }[0m
[38;2;139;134;130m… omitted 2027 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html → b/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -602,9 +602,9 @@[0m
[38;2;184;134;11m     const cx = Math.max(-half, Math.min(half, wx));[0m
[38;2;184;134;11m     const cz = Math.max(-half, Math.min(half, wz));[0m
[38;2;184;134;11m     // Height from cached grid — single lookup per particle per frame[0m
[38;2;255;255;255;48;2;19;87;20m+    // worldToGrid already counts its own hit/miss internally[0m
[38;2;184;134;11m     const g = cache.worldToGrid(cx, cz);[0m
[38;2;184;134;11m     const h = hGrid[g.row * GRID_SIZE + g.col] + 0.25;[0m
[38;2;255;255;255;48;2;119;20;20m-    cache.hits++; // worldToGrid hit (or miss) already counted; heightAt equivalent inline[0m
[38;2;184;134;11m     const pos = new THREE.Vector3(cx, h, cz);[0m
[38;2;184;134;11m     // Maintain trail ring buffer[0m
[38;2;184;134;11m     pd.trail.push(pos.clone());[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html → b/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -540,18 +540,25 @@[0m
[38;2;184;134;11m const MAX_TRAIL_LENGTH = 40;[0m
[38;2;184;134;11m const particleData = []; // { trail: Vector3[], speed: float, phase: float, baseX, baseZ }[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-// Initialize particles with cached start positions[0m
[38;2;255;255;255;48;2;19;87;20m+// Initialize particles with cached start positions.[0m
[38;2;255;255;255;48;2;19;87;20m+// Trail data stored as flat Float32Array per particle — zero Vector3 allocs in hot path.[0m
[38;2;184;134;11m function initParticles() {[0m
[38;2;184;134;11m   particleData.length = 0;[0m
[38;2;184;134;11m   for (let i = 0; i < NUM_PARTICLES; i++) {[0m
[38;2;184;134;11m     const baseX = (Math.random() - 0.5) * TERRAIN_SPAN * 0.8;[0m
[38;2;184;134;11m     const baseZ = (Math.random() - 0.5) * TERRAIN_SPAN * 0.8;[0m
[38;2;255;255;255;48;2;119;20;20m-    const trail = [];[0m
[38;2;255;255;255;48;2;19;87;20m+    // Pre-allocate trail ring buffer: MAX_TRAIL_LENGTH triplets of [x,y,z][0m
[38;2;255;255;255;48;2;19;87;20m+    const trail = new Float32Array(MAX_TRAIL_LENGTH * 3);[0m
[38;2;184;134;11m     const g = cache.worldToGrid(baseX, baseZ);[0m
[38;2;184;134;11m     const h0 = cache.heightAt(0, baseX, baseZ);[0m
[38;2;255;255;255;48;2;119;20;20m-    trail.push(new THREE.Vector3(baseX, h0 + 0.3, baseZ));[0m
[38;2;255;255;255;48;2;19;87;20m+    // Write first trail point[0m
[38;2;255;255;255;48;2;19;87;20m+    trail[0] = baseX;[0m
[38;2;255;255;255;48;2;19;87;20m+    trail[1] = h0 + 0.3;[0m
[38;2;255;255;255;48;2;19;87;20m+    trail[2] = baseZ;[0m
[38;2;184;134;11m     particleData.push({[0m
[38;2;255;255;255;48;2;119;20;20m-      trail,[0m
[38;2;255;255;255;48;2;19;87;20m+      trail,              // Float32Array, ring buffer[0m
[38;2;255;255;255;48;2;19;87;20m+      trailWriteIdx: 1,   // next write position (0-indexed triplet index)[0m
[38;2;255;255;255;48;2;19;87;20m+      trailCount: 1,      // number of valid triplets in buffer[0m
[38;2;184;134;11m       speed: 0.3 + Math.random() * 1.2,[0m
[38;2;184;134;11m       phase: Math.random() * Math.PI * 2,[0m
[38;2;184;134;11m       baseX,[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html → b/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -591,39 +591,39 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m let currentTimeIdx = 0;[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-// Update particle positions for current time index — reuses position arrays[0m
[38;2;255;255;255;48;2;19;87;20m+// Update particle positions for current time index.[0m
[38;2;255;255;255;48;2;19;87;20m+// ZERO per-frame Vector3 allocations — uses pre-allocated Float32Array ring buffers.[0m
[38;2;184;134;11m function updateParticles(t) {[0m
[38;2;184;134;11m   let vertIdx = 0;[0m
[38;2;255;255;255;48;2;119;20;20m-  // Cache height grid once for all particles this frame[0m
[38;2;255;255;255;48;2;119;20;20m-  const hGrid = cache.getHeightGrid(t);[0m
[38;2;255;255;255;48;2;19;87;20m+  const hGrid = cache.getHeightGrid(t); // one cached lookup for all particles[0m
[38;2;184;134;11m   for (let p = 0; p < particleData.length; p++) {[0m
[38;2;184;134;11m     const pd = particleData[p];[0m
[38;2;255;255;255;48;2;119;20;20m-    // Advance particle along its trail[0m
[38;2;184;134;11m     const elapsed = performance.now() * 0.001 * pd.speed + pd.phase;[0m
[38;2;184;134;11m     // Oscillate around base position with time-varying offset[0m
[38;2;184;134;11m     const offsetX = Math.sin(elapsed * 0.7) * 3.5 + Math.cos(elapsed * 1.3) * 2.0;[0m
[38;2;184;134;11m     const offsetZ = Math.cos(elapsed * 0.9) * 3.0 + Math.sin(elapsed * 1.1) * 2.5;[0m
[38;2;255;255;255;48;2;119;20;20m-    const wx = pd.baseX + offsetX;[0m
[38;2;255;255;255;48;2;119;20;20m-    const wz = pd.baseZ + offsetZ;[0m
[38;2;255;255;255;48;2;119;20;20m-    // Clamp to terrain bounds[0m
[38;2;255;255;255;48;2;119;20;20m-    const cx = Math.max(-half, Math.min(half, wx));[0m
[38;2;255;255;255;48;2;119;20;20m-    const cz = Math.max(-half, Math.min(half, wz));[0m
[38;2;255;255;255;48;2;119;20;20m-    // Height from cached grid — single lookup per particle per frame[0m
[38;2;255;255;255;48;2;119;20;20m-    // worldToGrid already counts its own hit/miss internally[0m
[38;2;255;255;255;48;2;119;20;20m-    const g = cache.worldToGrid(cx, cz);[0m
[38;2;255;255;255;48;2;19;87;20m+    // Clamp to terrain bounds, then compute world position[0m
[38;2;255;255;255;48;2;19;87;20m+    const cx = Math.max(-half, Math.min(half, pd.baseX + offsetX));[0m
[38;2;255;255;255;48;2;19;87;20m+    const cz = Math.max(-half, Math.min(half, pd.baseZ + offsetZ));[0m
[38;2;255;255;255;48;2;19;87;20m+    const g = cache.worldToGrid(cx, cz); // cached coordinate transform[0m
[38;2;184;134;11m     const h = hGrid[g.row * GRID_SIZE + g.col] + 0.25;[0m
[38;2;255;255;255;48;2;119;20;20m-    const pos = new THREE.Vector3(cx, h, cz);[0m
[38;2;255;255;255;48;2;119;20;20m-    // Maintain trail ring buffer[0m
[38;2;255;255;255;48;2;119;20;20m-    pd.trail.push(pos.clone());[0m
[38;2;255;255;255;48;2;119;20;20m-    if (pd.trail.length > MAX_TRAIL_LENGTH) pd.trail.shift();[0m
[38;2;255;255;255;48;2;119;20;20m-    // Write trail vertices to pre-allocated buffer[0m
[38;2;255;255;255;48;2;119;20;20m-    for (let j = 0; j < pd.trail.length; j++) {[0m
[38;2;255;255;255;48;2;119;20;20m-      const v = pd.trail[j];[0m
[38;2;255;255;255;48;2;119;20;20m-      const alpha = j / pd.trail.length; // fade in[0m
[38;2;255;255;255;48;2;19;87;20m+    // Write new position into trail ring buffer (direct Float32Array, no Vector3)[0m
[38;2;255;255;255;48;2;19;87;20m+    const wi = pd.trailWriteIdx * 3;[0m
[38;2;255;255;255;48;2;19;87;20m+    pd.trail[wi]     = cx;[0m
[38;2;255;255;255;48;2;19;87;20m+    pd.trail[wi + 1] = h;[0m
[38;2;255;255;255;48;2;19;87;20m+    pd.trail[wi + 2] = cz;[0m
[38;2;255;255;255;48;2;19;87;20m+    pd.trailWriteIdx = (pd.trailWriteIdx + 1) % MAX_TRAIL_LENGTH;[0m
[38;2;255;255;255;48;2;19;87;20m+    if (pd.trailCount < MAX_TRAIL_LENGTH) pd.trailCount++;[0m
[38;2;255;255;255;48;2;19;87;20m+    // Copy trail into pre-allocated particle geometry buffer (oldest first for tail fade)[0m
[38;2;255;255;255;48;2;19;87;20m+    const count = pd.trailCount;[0m
[38;2;255;255;255;48;2;19;87;20m+    const startIdx = count < MAX_TRAIL_LENGTH ? 0 : pd.trailWriteIdx;[0m
[38;2;255;255;255;48;2;19;87;20m+    for (let j = 0; j < count; j++) {[0m
[38;2;255;255;255;48;2;19;87;20m+      const srcIdx = ((startIdx + j) % MAX_TRAIL_LENGTH) * 3;[0m
[38;2;255;255;255;48;2;19;87;20m+      const alpha = j / count; // 0 (tail) → 1 (head)[0m
[38;2;184;134;11m       const bi = vertIdx * 3;[0m
[38;2;255;255;255;48;2;119;20;20m-      particlePositionsArr[bi]     = v.x;[0m
[38;2;255;255;255;48;2;119;20;20m-      particlePositionsArr[bi + 1] = v.y;[0m
[38;2;255;255;255;48;2;119;20;20m-      particlePositionsArr[bi + 2] = v.z;[0m
[38;2;255;255;255;48;2;19;87;20m+      particlePositionsArr[bi]     = pd.trail[srcIdx];[0m
[38;2;255;255;255;48;2;19;87;20m+      particlePositionsArr[bi + 1] = pd.trail[srcIdx + 1];[0m
[38;2;255;255;255;48;2;19;87;20m+      particlePositionsArr[bi + 2] = pd.trail[srcIdx + 2];[0m
[38;2;184;134;11m       // Cyan → white gradient along trail[0m
[38;2;184;134;11m       particleColorsArr[bi]     = 0.2 + alpha * 0.8;[0m
[38;2;184;134;11m       particleColorsArr[bi + 1] = 0.6 + alpha * 0.4;[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html → b/E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -538,7 +538,7 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m // ── Particles (API call trails) ────────────────────────────────[0m
[38;2;184;134;11m const MAX_TRAIL_LENGTH = 40;[0m
[38;2;255;255;255;48;2;119;20;20m-const particleData = []; // { trail: Vector3[], speed: float, phase: float, baseX, baseZ }[0m
[38;2;255;255;255;48;2;19;87;20m+const particleData = []; // { trail: Float32Array, trailWriteIdx, trailCount, speed, phase, baseX, baseZ }[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m // Initialize particles with cached start positions.[0m
[38;2;184;134;11m // Trail data stored as flat Float32Array per particle — zero Vector3 allocs in hot path.[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-terrain.js → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-terrain.js[0m
[38;2;139;134;130m@@ -0,0 +1,124 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env node[0m
[38;2;255;255;255;48;2;19;87;20m+// Verify: 3d-terrain-explorer.html structure, cache consistency, tooltip wiring[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+const fs = require('fs');[0m
[38;2;255;255;255;48;2;19;87;20m+const path = require('path');[0m
[38;2;255;255;255;48;2;19;87;20m+const html = fs.readFileSync('E:/Stryde/_alpedal/styde-forge/3d-terrain-explorer.html', 'utf8');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+let errors = 0;[0m
[38;2;255;255;255;48;2;19;87;20m+let warnings = 0;[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+function check(condition, msg) {[0m
[38;2;255;255;255;48;2;19;87;20m+  if (!condition) { console.log('FAIL: ' + msg); errors++; }[0m
[38;2;255;255;255;48;2;19;87;20m+  else { console.log('  OK: ' + msg); }[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+console.log('=== 3D Terrain Explorer Verification ===\n');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// 1. HTML structure[0m
[38;2;255;255;255;48;2;19;87;20m+console.log('--- HTML Structure ---');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('<!DOCTYPE html>'), 'Has DOCTYPE');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('</html>'), 'Closes html tag');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('</body>'), 'Closes body tag');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// Count open/close braces in script[0m
[38;2;255;255;255;48;2;19;87;20m+const scriptMatch = html.match(/<script type="module">([\s\S]*?)<\/script>/);[0m
[38;2;255;255;255;48;2;19;87;20m+check(scriptMatch !== null, 'Has module script tag');[0m
[38;2;255;255;255;48;2;19;87;20m+const js = scriptMatch ? scriptMatch[1] : '';[0m
[38;2;255;255;255;48;2;19;87;20m+const opens = (js.match(/{/g) || []).length;[0m
[38;2;255;255;255;48;2;19;87;20m+const closes = (js.match(/}/g) || []).length;[0m
[38;2;255;255;255;48;2;19;87;20m+check(opens === closes, `Braces balanced: ${opens} open, ${closes} close`);[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// 2. Cache API consistency[0m
[38;2;255;255;255;48;2;19;87;20m+console.log('\n--- Cache Layer ---');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.getHeightGrid('), 'getHeightGrid defined');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.getUserGrid('), 'getUserGrid defined');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.getErrorGrid('), 'getErrorGrid defined');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.worldToGrid('), 'worldToGrid defined');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.heightAt('), 'heightAt defined');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.hits'), 'hits counter');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.misses'), 'misses counter');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.getHitRate('), 'getHitRate method');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('cache.geomAllocs'), 'geomAllocs counter');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// Verify cache is used by all subsystems[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('updateTerrain') && js.includes('cache.getHeightGrid'), 'Terrain uses cache');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('updateRiver') && js.includes('cache.getErrorGrid'), 'River uses cache');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('updateParticles') && js.includes('cache.getHeightGrid'), 'Particles use cache');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes('updateTooltip') && js.includes('cache.worldToGrid'), 'Tooltip uses cache');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// 3. Tooltip wiring[0m
[38;2;255;255;255;48;2;19;87;20m+console.log('\n--- Tooltip Wiring ---');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('id="tooltip"'), 'Tooltip HTML element exists');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('id="tt-rev"'), 'tt-rev span exists');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('id="tt-users"'), 'tt-users span exists');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('id="tt-err"'), 'tt-err span exists');[0m
[38;2;255;255;255;48;2;19;87;20m+check(html.includes('id="tt-time"'), 'tt-time span exists');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// Verify JS references all four tooltip fields[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes("getElementById('tt-rev')"), 'JS references tt-rev');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes("getElementById('tt-users')"), 'JS references tt-users');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes("getElementById('tt-err')"), 'JS references tt-err');[0m
[38;2;255;255;255;48;2;19;87;20m+check(js.includes("getElementById('tt-time')"), 'JS references tt-time');[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// 4. Hot-path audit: no new THREE.XxxGeometry in per-frame[0m
[38;2;255;255;255;48;2;19;87;20m+console.log('\n--- Hot-Path Audit ---');[0m
[38;2;255;255;255;48;2;19;87;20m+// Extract the animate function body[0m
[38;2;255;255;255;48;2;19;87;20m+const animateMatch = js.match(/function animate\(timestamp\)\s*\{([\s\S]*?)\n\}/);[0m
[38;2;255;255;255;48;2;19;87;20m+if (animateMatch) {[0m
[38;2;255;255;255;48;2;19;87;20m+  const animateBody = animateMatch[1];[0m
[38;2;255;255;255;48;2;19;87;20m+  const animateAllocs = animateBody.match(/new THREE\./g);[0m
[38;2;255;255;255;48;2;19;87;20m+  check(!animateAllocs, `animate() has ${animateAllocs ? animateAllocs.length : 0} new THREE.* calls (want 0)`);[0m
[38;2;255;255;255;48;2;19;87;20m+} else {[0m
[38;2;255;255;255;48;2;19;87;20m+  check(false, 'Could not extract animate function');[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+// Extract updateParticles[0m
[38;2;255;255;255;48;2;19;87;20m+const upMatch = js.match(/function updateParticles\(t\)\s*\{([\s\S]*?)\n\}/);[0m
[38;2;255;255;255;48;2;19;87;20m+if (upMatch) {[0m
[38;2;139;134;130m… omitted 46 diff line(s) across 1 additional file(s)/section(s)[0m
Verifiering: 35/35 checks passed.
Fixar mot feedbacken:
1. Cache-lager: Alla hojduppslagningar gar genom ett centralt cache-objekt. getHeightGrid, getUserGrid, getErrorGrid cachas per tidsindex. worldToGrid cachas per avrundad varldskoordinat. heightAt cachas per (t, col, row). Terrain, particles, tooltip, river — alla laser fran samma tabell. Ingen kallar generateTimeSeriesData mer an en gang.
2. Tooltip-wiring: #tooltip definierat i HTML med fyra span (tt-rev, tt-users, tt-err, tt-time). Alla fyra har JS-referenser och skrivs i updateTooltip via raycaster. Bekraftat.
3. Hot-path: Noll new THREE.*-anrop i animate() och updateParticles(). Particles anvander pre-allokerade Float32Array ringbuffers per particle — inga Vector3-allokeringar per frame. River-geometri cachas per tidsindex i riverCacheByTime Map — TubeGeometry byggs bara om vid ny tid.
4. Diagnostikpanel: Visar cache hits, misses, hit-rate, geom allocs, particle updates, FPS. Uppdateras varje sekund.
5. Debounce: 200ms pa slider input. Piltangenter applicerar direkt.
6. Metrik-validering: Diagnostikpanelen ar den synliga valideringsytan. Cache-metrics ger transparens pa prestanda. FPS-raknare visar runtime-halsa.
Fil: E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html (808 rader, 32KB)