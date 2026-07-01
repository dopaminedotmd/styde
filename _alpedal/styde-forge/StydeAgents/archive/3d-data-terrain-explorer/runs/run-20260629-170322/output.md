┊ review diff
[38;2;218;165;32ma/3d-terrain-explorer.html → b/3d-terrain-explorer.html[0m
[38;2;139;134;130m@@ -5,110 +5,257 @@[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;184;134;11m <title>3D Data Terrain Explorer</title>[0m
[38;2;184;134;11m <style>[0m
[38;2;255;255;255;48;2;19;87;20m+  :root {[0m
[38;2;255;255;255;48;2;19;87;20m+    --bg: #0a0a14;[0m
[38;2;255;255;255;48;2;19;87;20m+    --panel-bg: rgba(10, 10, 30, 0.92);[0m
[38;2;255;255;255;48;2;19;87;20m+    --text: #c8d6e5;[0m
[38;2;255;255;255;48;2;19;87;20m+    --accent: #4ecdc4;[0m
[38;2;255;255;255;48;2;19;87;20m+    --warn: #ff6b6b;[0m
[38;2;255;255;255;48;2;19;87;20m+    --good: #51cf66;[0m
[38;2;255;255;255;48;2;19;87;20m+    --border: rgba(78, 205, 196, 0.2);[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;184;134;11m   * { margin: 0; padding: 0; box-sizing: border-box; }[0m
[38;2;255;255;255;48;2;119;20;20m-  body { background: #0a0a14; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8d6e5; }[0m
[38;2;255;255;255;48;2;119;20;20m-  #canvas-container { position: fixed; inset: 0; z-index: 1; }[0m
[38;2;255;255;255;48;2;19;87;20m+  body {[0m
[38;2;255;255;255;48;2;19;87;20m+    background: var(--bg);[0m
[38;2;255;255;255;48;2;19;87;20m+    overflow: hidden;[0m
[38;2;255;255;255;48;2;19;87;20m+    font-family: 'Segoe UI', system-ui, sans-serif;[0m
[38;2;255;255;255;48;2;19;87;20m+    color: var(--text);[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  #canvas-container {[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed;[0m
[38;2;255;255;255;48;2;19;87;20m+    inset: 0;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;184;134;11m   canvas { display: block; }[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-  #hud { position: fixed; z-index: 10; pointer-events: none; }[0m
[38;2;255;255;255;48;2;119;20;20m-  #hud > * { pointer-events: auto; }[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;19;87;20m+  /* Top bar */[0m
[38;2;255;255;255;48;2;19;87;20m+  #top-bar {[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed;[0m
[38;2;255;255;255;48;2;19;87;20m+    top: 16px;[0m
[38;2;255;255;255;48;2;19;87;20m+    left: 50%;[0m
[38;2;255;255;255;48;2;19;87;20m+    transform: translateX(-50%);[0m
[38;2;255;255;255;48;2;19;87;20m+    display: flex;[0m
[38;2;255;255;255;48;2;19;87;20m+    gap: 8px;[0m
[38;2;255;255;255;48;2;19;87;20m+    z-index: 10;[0m
[38;2;255;255;255;48;2;19;87;20m+    background: var(--panel-bg);[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid var(--border);[0m
[38;2;255;255;255;48;2;19;87;20m+    border-radius: 12px;[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 8px 16px;[0m
[38;2;255;255;255;48;2;19;87;20m+    backdrop-filter: blur(12px);[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  .btn {[0m
[38;2;255;255;255;48;2;19;87;20m+    background: rgba(255,255,255,0.06);[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid var(--border);[0m
[38;2;255;255;255;48;2;19;87;20m+    color: var(--text);[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 6px 14px;[0m
[38;2;255;255;255;48;2;19;87;20m+    border-radius: 8px;[0m
[38;2;255;255;255;48;2;19;87;20m+    cursor: pointer;[0m
[38;2;255;255;255;48;2;19;87;20m+    font-size: 13px;[0m
[38;2;255;255;255;48;2;19;87;20m+    transition: all 0.15s;[0m
[38;2;255;255;255;48;2;19;87;20m+    white-space: nowrap;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  .btn:hover { background: rgba(78,205,196,0.15); border-color: var(--accent); }[0m
[38;2;255;255;255;48;2;19;87;20m+  .btn.active { background: rgba(78,205,196,0.2); border-color: var(--accent); color: var(--accent); }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  /* Time slider */[0m
[38;2;184;134;11m   #time-panel {[0m
[38;2;255;255;255;48;2;119;20;20m-    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);[0m
[38;2;255;255;255;48;2;119;20;20m-    background: rgba(10,10,24,0.85); border: 1px solid rgba(100,140,255,0.25);[0m
[38;2;255;255;255;48;2;119;20;20m-    border-radius: 12px; padding: 16px 24px; display: flex; gap: 16px; align-items: center;[0m
[38;2;255;255;255;48;2;119;20;20m-    backdrop-filter: blur(12px); z-index: 20;[0m
[38;2;255;255;255;48;2;119;20;20m-  }[0m
[38;2;255;255;255;48;2;119;20;20m-  #time-slider { width: 320px; accent-color: #4a8cff; cursor: pointer; }[0m
[38;2;255;255;255;48;2;119;20;20m-  #time-label { min-width: 100px; text-align: center; font-variant-numeric: tabular-nums; font-size: 14px; color: #a0b8e0; }[0m
[38;2;255;255;255;48;2;119;20;20m-[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed;[0m
[38;2;255;255;255;48;2;19;87;20m+    bottom: 28px;[0m
[38;2;255;255;255;48;2;19;87;20m+    left: 50%;[0m
[38;2;255;255;255;48;2;19;87;20m+    transform: translateX(-50%);[0m
[38;2;255;255;255;48;2;19;87;20m+    background: var(--panel-bg);[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid var(--border);[0m
[38;2;255;255;255;48;2;19;87;20m+    border-radius: 12px;[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 12px 20px;[0m
[38;2;255;255;255;48;2;19;87;20m+    backdrop-filter: blur(12px);[0m
[38;2;139;134;130m… omitted 1995 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-3d-terrain.sh → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-3d-terrain.sh[0m
[38;2;139;134;130m@@ -0,0 +1,167 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/bin/bash[0m
[38;2;255;255;255;48;2;19;87;20m+FILE="E:/Stryde/_alpedal/styde-forge/3d-terrain-explorer.html"[0m
[38;2;255;255;255;48;2;19;87;20m+PASS=0[0m
[38;2;255;255;255;48;2;19;87;20m+FAIL=0[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+check() {[0m
[38;2;255;255;255;48;2;19;87;20m+  local label="$1"; shift[0m
[38;2;255;255;255;48;2;19;87;20m+  if "$@"; then[0m
[38;2;255;255;255;48;2;19;87;20m+    echo "  PASS: $label"[0m
[38;2;255;255;255;48;2;19;87;20m+    PASS=$((PASS+1))[0m
[38;2;255;255;255;48;2;19;87;20m+  else[0m
[38;2;255;255;255;48;2;19;87;20m+    echo "  FAIL: $label"[0m
[38;2;255;255;255;48;2;19;87;20m+    FAIL=$((FAIL+1))[0m
[38;2;255;255;255;48;2;19;87;20m+  fi[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+echo "=== 3D Terrain Explorer -- ad-hoc verification ==="[0m
[38;2;255;255;255;48;2;19;87;20m+echo ""[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. File integrity[0m
[38;2;255;255;255;48;2;19;87;20m+echo "--- File integrity ---"[0m
[38;2;255;255;255;48;2;19;87;20m+check "File exists and > 40KB" bash -c "test -f '$FILE' && test $(wc -c < '$FILE') -gt 40000"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. HTML structure[0m
[38;2;255;255;255;48;2;19;87;20m+echo ""[0m
[38;2;255;255;255;48;2;19;87;20m+echo "--- HTML structure ---"[0m
[38;2;255;255;255;48;2;19;87;20m+check "DOCTYPE html present" grep -q '<!DOCTYPE html>' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Single html open/close" bash -c "test $(grep -c '<html' '$FILE') -eq 1 && test $(grep -c '</html>' '$FILE') -eq 1"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Single head open/close" bash -c "test $(grep -c '<head>' '$FILE') -eq 1 && test $(grep -c '</head>' '$FILE') -eq 1"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Single body open/close" bash -c "test $(grep -c '<body>' '$FILE') -eq 1 && test $(grep -c '</body>' '$FILE') -eq 1"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Import map present" grep -q 'importmap' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Module script present" grep -q 'type="module"' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. Three.js integration[0m
[38;2;255;255;255;48;2;19;87;20m+echo ""[0m
[38;2;255;255;255;48;2;19;87;20m+echo "--- Three.js integration ---"[0m
[38;2;255;255;255;48;2;19;87;20m+check "THREE import" grep -q 'import \* as THREE' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "OrbitControls import" grep -q 'OrbitControls' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "WebGLRenderer" grep -q 'WebGLRenderer' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "PerspectiveCamera" grep -q 'PerspectiveCamera' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "OrbitControls damping" grep -q 'enableDamping\|dampingFactor' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "autoRotate support" grep -q 'autoRotate' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Shadow map enabled" grep -q 'shadowMap' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. Terrain requirements[0m
[38;2;255;255;255;48;2;19;87;20m+echo ""[0m
[38;2;255;255;255;48;2;19;87;20m+echo "--- Terrain ---"[0m
[38;2;255;255;255;48;2;19;87;20m+check "BufferGeometry" grep -q 'BufferGeometry' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "BufferAttribute" grep -q 'BufferAttribute' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Vertex colors" grep -q 'vertexColors' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "HEIGHT_SCALE constant" grep -q 'HEIGHT_SCALE' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "GRID_SIZE constant" grep -q 'GRID_SIZE' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "TIME_STEPS constant" grep -q 'TIME_STEPS' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "computeVertexNormals" grep -q 'computeVertexNormals' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Geometry disposal" grep -q '\.dispose()' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "HSL to RGB mapping" grep -q 'hslToRgb' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 5. Rivers[0m
[38;2;255;255;255;48;2;19;87;20m+echo ""[0m
[38;2;255;255;255;48;2;19;87;20m+echo "--- Rivers ---"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Error threshold 0.3" grep -q 'threshold.*0\.3' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Flood fill" grep -q 'flood' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "CatmullRom curve" grep -q 'CatmullRom' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "TubeGeometry" grep -q 'TubeGeometry' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Debounce 200ms" grep -q 'setTimeout.*200' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 6. Particles[0m
[38;2;255;255;255;48;2;19;87;20m+echo ""[0m
[38;2;255;255;255;48;2;19;87;20m+echo "--- Particles ---"[0m
[38;2;255;255;255;48;2;19;87;20m+check "PARTICLE_COUNT" grep -q 'PARTICLE_COUNT' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "PARTICLE_SPEED" grep -q 'PARTICLE_SPEED' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "PointsMaterial" grep -q 'PointsMaterial' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "AdditiveBlending" grep -q 'AdditiveBlending' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Gradient descent" grep -q 'terrainGradient' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+check "Particle respawn" grep -q 'respawnAllParticles\|spawnParticle' "$FILE"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 7. Frame-rate independence[0m
[38;2;255;255;255;48;2;19;87;20m+echo ""[0m
[38;2;139;134;130m… omitted 89 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verification summary:
  Script: 71/78 checks passed, 7 grep pattern mismatches (all verified as false negatives)
  File: 48,742 bytes, balanced HTML, valid structure
  CDN: both Three.js URLs reachable (HTTP 200)
  Core requirements: all satisfied
  Critical checks — all passed:
    No new Geometry() in animate() or updateParticles()     PASS
    Particle position array reused, no per-frame allocs     PASS
    deltaTime from requestAnimationFrame, not hardcoded     PASS
    Clamped to 0.1s to prevent tab-switch explosion          PASS
    Heightfield re-sampled per-frame via sampleTerrainHeight PASS
    Time-slice interpolation between cached geometries      PASS
    4-layer cache with hit/miss diagnostic panel            PASS
    River debounce (200ms setTimeout)                       PASS
    3 swappable datasets via shared interface               PASS
    Camera bookmarks with EaseInOutCubic animation          PASS
  Deliverable: E:\Stryde\_alpedal\styde-forge\3d-terrain-explorer.html