┊ review diff
[38;2;218;165;32ma/dashboard.html → b/dashboard.html[0m
[38;2;139;134;130m@@ -0,0 +1,871 @@[0m
[38;2;255;255;255;48;2;19;87;20m+<!DOCTYPE html>[0m
[38;2;255;255;255;48;2;19;87;20m+<html lang="en">[0m
[38;2;255;255;255;48;2;19;87;20m+<head>[0m
[38;2;255;255;255;48;2;19;87;20m+<meta charset="UTF-8">[0m
[38;2;255;255;255;48;2;19;87;20m+<meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;19;87;20m+<title>3D Data Terrain Explorer</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<style>[0m
[38;2;255;255;255;48;2;19;87;20m+  * { margin: 0; padding: 0; box-sizing: border-box; }[0m
[38;2;255;255;255;48;2;19;87;20m+  body { overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #canvas-container { position: fixed; inset: 0; }[0m
[38;2;255;255;255;48;2;19;87;20m+  canvas { display: block; }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  /* Time slider bar */[0m
[38;2;255;255;255;48;2;19;87;20m+  #timebar {[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);[0m
[38;2;255;255;255;48;2;19;87;20m+    background: rgba(10,10,30,0.85); backdrop-filter: blur(12px);[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid rgba(255,255,255,0.12); border-radius: 14px;[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 14px 22px; display: flex; align-items: center; gap: 16px;[0m
[38;2;255;255;255;48;2;19;87;20m+    z-index: 10; min-width: 520px;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  #timebar label { color: #99aabb; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; white-space: nowrap; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #time-slider { flex: 1; -webkit-appearance: none; height: 6px; border-radius: 3px; background: linear-gradient(90deg, #2a3a5c, #4a7ab5, #2a3a5c); outline: none; cursor: pointer; }[0m
[38;2;255;255;255;48;2;19;87;20m+  #time-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 22px; height: 22px; border-radius: 50%; background: #6ab4ff; border: 2px solid #fff; cursor: pointer; box-shadow: 0 0 14px rgba(106,180,255,0.5); }[0m
[38;2;255;255;255;48;2;19;87;20m+  #time-label { color: #ddeeff; font-size: 13px; font-weight: 600; min-width: 64px; text-align: center; }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  /* Bookmark bar */[0m
[38;2;255;255;255;48;2;19;87;20m+  #bookmarks {[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed; top: 20px; left: 50%; transform: translateX(-50%);[0m
[38;2;255;255;255;48;2;19;87;20m+    display: flex; gap: 8px; z-index: 10;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  .bookmark-btn {[0m
[38;2;255;255;255;48;2;19;87;20m+    background: rgba(10,10,30,0.8); backdrop-filter: blur(8px);[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid rgba(255,255,255,0.15); border-radius: 8px;[0m
[38;2;255;255;255;48;2;19;87;20m+    color: #99aabb; padding: 8px 16px; cursor: pointer; font-size: 12px;[0m
[38;2;255;255;255;48;2;19;87;20m+    transition: all 0.2s; white-space: nowrap;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  .bookmark-btn:hover { background: rgba(40,60,100,0.7); color: #ddeeff; border-color: rgba(106,180,255,0.4); }[0m
[38;2;255;255;255;48;2;19;87;20m+  .bookmark-btn.active { background: rgba(30,60,120,0.7); color: #6ab4ff; border-color: #6ab4ff; }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  /* Diagnostic panel */[0m
[38;2;255;255;255;48;2;19;87;20m+  #diagnostics {[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed; top: 90px; right: 16px;[0m
[38;2;255;255;255;48;2;19;87;20m+    background: rgba(10,10,30,0.82); backdrop-filter: blur(8px);[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid rgba(255,255,255,0.1); border-radius: 10px;[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 12px 16px; z-index: 10; font-size: 11px; color: #778899;[0m
[38;2;255;255;255;48;2;19;87;20m+    min-width: 180px; font-family: 'Consolas', 'Courier New', monospace;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  #diagnostics .diag-title { color: #8899aa; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }[0m
[38;2;255;255;255;48;2;19;87;20m+  .diag-row { display: flex; justify-content: space-between; margin: 2px 0; }[0m
[38;2;255;255;255;48;2;19;87;20m+  .diag-row .val { color: #aaccee; }[0m
[38;2;255;255;255;48;2;19;87;20m+  .diag-row .hit { color: #4ec97a; }[0m
[38;2;255;255;255;48;2;19;87;20m+  .diag-row .miss { color: #e05555; }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  /* Legend */[0m
[38;2;255;255;255;48;2;19;87;20m+  #legend {[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed; bottom: 110px; left: 20px;[0m
[38;2;255;255;255;48;2;19;87;20m+    background: rgba(10,10,30,0.78); backdrop-filter: blur(8px);[0m
[38;2;255;255;255;48;2;19;87;20m+    border: 1px solid rgba(255,255,255,0.1); border-radius: 10px;[0m
[38;2;255;255;255;48;2;19;87;20m+    padding: 14px; z-index: 10; font-size: 11px; color: #8899aa;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  .legend-item { display: flex; align-items: center; gap: 8px; margin: 5px 0; }[0m
[38;2;255;255;255;48;2;19;87;20m+  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }[0m
[38;2;255;255;255;48;2;19;87;20m+  .legend-gradient { width: 80px; height: 10px; border-radius: 3px; flex-shrink: 0; }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  /* Loading */[0m
[38;2;255;255;255;48;2;19;87;20m+  #loading {[0m
[38;2;255;255;255;48;2;19;87;20m+    position: fixed; inset: 0; display: flex; align-items: center; justify-content: center;[0m
[38;2;255;255;255;48;2;19;87;20m+    background: #0a0a14; z-index: 100; color: #6ab4ff; font-size: 16px;[0m
[38;2;255;255;255;48;2;19;87;20m+    transition: opacity 0.5s;[0m
[38;2;255;255;255;48;2;19;87;20m+  }[0m
[38;2;255;255;255;48;2;19;87;20m+  #loading.hidden { opacity: 0; pointer-events: none; }[0m
[38;2;255;255;255;48;2;19;87;20m+</style>[0m
[38;2;255;255;255;48;2;19;87;20m+</head>[0m
[38;2;255;255;255;48;2;19;87;20m+<body>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="canvas-container"></div>[0m
[38;2;255;255;255;48;2;19;87;20m+<div id="loading">Building 3D Terrain...</div>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;139;134;130m… omitted 793 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\dashboard.html → b/E:\Stryde\_alpedal\styde-forge\dashboard.html[0m
[38;2;139;134;130m@@ -597,8 +597,10 @@[0m
[38;2;184;134;11m     this.terrainMesh.castShadow = true;[0m
[38;2;184;134;11m     this.scene.add(this.terrainMesh);[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-    // Wireframe overlay for grid readability[0m
[38;2;255;255;255;48;2;19;87;20m+    // Wireframe overlay for grid readability — cached per timestep[0m
[38;2;255;255;255;48;2;19;87;20m+    this.wireframeCache = new Map(); // key: timestep → WireframeGeometry[0m
[38;2;184;134;11m     const wireGeo = new THREE.WireframeGeometry(geo, 1);[0m
[38;2;255;255;255;48;2;19;87;20m+    this.wireframeCache.set(this.currentTimestep, wireGeo);[0m
[38;2;184;134;11m     const wireMat = new THREE.MeshBasicMaterial({ color: 0x334466, transparent: true, opacity: 0.12 });[0m
[38;2;184;134;11m     this.wireframe = new THREE.Mesh(wireGeo, wireMat);[0m
[38;2;184;134;11m     this.scene.add(this.wireframe);[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\dashboard.html → b/E:\Stryde\_alpedal\styde-forge\dashboard.html[0m
[38;2;139;134;130m@@ -679,7 +679,7 @@[0m
[38;2;184;134;11m     this.scene.add(gridHelper);[0m
[38;2;184;134;11m   }[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-  // Pre-build and cache all 24 terrain + river geometries at init[0m
[38;2;255;255;255;48;2;19;87;20m+  // Pre-build and cache all 24 terrain + river + wireframe geometries at init[0m
[38;2;184;134;11m   // This ensures no THREE.XxxGeometry() calls on slider change[0m
[38;2;184;134;11m   _preCacheAllGeometries() {[0m
[38;2;184;134;11m     for (let t = 0; t < TIME_STEPS; t++) {[0m
[38;2;139;134;130m@@ -687,6 +687,11 @@[0m
[38;2;184;134;11m       if (!this.cache.getTerrain(t)) {[0m
[38;2;184;134;11m         const geo = this.terrainBuilder.buildTimestep(t);[0m
[38;2;184;134;11m         this.cache.setTerrain(t, geo);[0m
[38;2;255;255;255;48;2;19;87;20m+      }[0m
[38;2;255;255;255;48;2;19;87;20m+      // Build and cache wireframe geometry for this terrain[0m
[38;2;255;255;255;48;2;19;87;20m+      if (!this.wireframeCache.has(t)) {[0m
[38;2;255;255;255;48;2;19;87;20m+        const cachedGeo = this.cache.getTerrain(t);[0m
[38;2;255;255;255;48;2;19;87;20m+        this.wireframeCache.set(t, new THREE.WireframeGeometry(cachedGeo, 1));[0m
[38;2;184;134;11m       }[0m
[38;2;184;134;11m       // Build and cache river geometry[0m
[38;2;184;134;11m       if (!this.cache.getRiver(t)) {[0m
  ┊ review diff
[38;2;218;165;32ma/E:\Stryde\_alpedal\styde-forge\dashboard.html → b/E:\Stryde\_alpedal\styde-forge\dashboard.html[0m
[38;2;139;134;130m@@ -709,9 +709,9 @@[0m
[38;2;184;134;11m     this.terrainMesh.geometry.dispose();[0m
[38;2;184;134;11m     // Swap to cached geometry[0m
[38;2;184;134;11m     this.terrainMesh.geometry = cachedGeo;[0m
[38;2;255;255;255;48;2;119;20;20m-    // Update wireframe to match[0m
[38;2;255;255;255;48;2;19;87;20m+    // Swap wireframe from cache — no allocation[0m
[38;2;184;134;11m     this.wireframe.geometry.dispose();[0m
[38;2;255;255;255;48;2;119;20;20m-    this.wireframe.geometry = new THREE.WireframeGeometry(cachedGeo, 1);[0m
[38;2;255;255;255;48;2;19;87;20m+    this.wireframe.geometry = this.wireframeCache.get(t);[0m
[38;2;184;134;11m   }[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m   // Debounced river swap[0m
Verification: PASS
Ad-hoc checks mot dashboard.html (34,606 bytes):
  JS syntax: PASS (node --check, 28,724 chars extracted)
  Klasser: 5/5 (CacheManager, TerrainBuilder, RiverBuilder, ParticleSystem, DataTerrainScene)
  Pre-cache: 24 terrain + 24 wireframe + 24 river geometries byggda vid init
  WireframeCache: fixad — inga nya WireframeGeometry vid slider-byte
  Debounce: 200ms på river-rebuilds
  Bookmarks: 5 knappar + tangentbord 1-5
  Diagnostikpanel: cache hit/miss + FPS + timestep
  Hot-path: 0 st new THREE.*Geometry i per-frame eller per-tick-kod
  Particle: 600 partiklar, position-array muteras in-place, noll allokering
Öppna E:\Stryde\_alpedal\styde-forge\dashboard.html i webbläsare.
Pil vänster/höger scrubbar tid, 1-5 byter vy, R togglar auto-rotate.