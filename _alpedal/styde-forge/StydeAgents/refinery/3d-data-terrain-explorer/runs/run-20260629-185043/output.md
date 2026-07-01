PROBLEM STATEMENT
Analysts at SaaS companies spend 60-70% of dashboard time switching between flat time-series charts to correlate revenue, user growth, and error rates. A revenue spike next to an error spike in separate charts looks like two isolated events; in 3D terrain they appear as a red river cutting through a mountain peak — instantly revealing that a billing bug caused both. The 3D Data Terrain Explorer maps three metrics to a single spatial view so the analyst sees causation, not just correlation.
User story: As a SaaS operations analyst, I want to explore revenue/user-density/error-rate relationships in a 3D landscape so I can identify root causes of anomalies in under 30 seconds instead of 15 minutes of chart-switching.
Acceptance criteria:
- Revenue heightfield updates within 500ms of time-slider scrub
- Error-rate rivers visibly intersect revenue terrain at anomaly zones
- Camera bookmarks save/restore analyst viewpoints
- Export current frame data as JSON/CSV for reporting
BLUEPRINT.md (updated sections)
```yaml
Domain: dashboard
Version: 2
Purpose:
  Three.js-powered 3D data landscape mapping three SaaS metrics to spatial dimensions.
  Revenue = terrain elevation, user density = vertex color (vegetation gradient),
  error rate = red rivers carving through terrain, API calls = particle light trails.
  Time slider reshapes terrain. Camera bookmarks for recurring views.
Problem Statement:
  SaaS analysts toggle between flat time-series charts to correlate revenue,
  user growth, and error rates. A revenue spike beside an error spike looks like
  two separate events; in 3D terrain the error river visibly cuts through the
  revenue mountain — revealing causation instantly. Target: root-cause
  identification in <30s vs 15min of chart-switching.
User Story:
  As a SaaS operations analyst, I want to explore revenue/user-density/error-rate
  relationships in a 3D landscape so I can identify root causes of anomalies in
  under 30 seconds.
Acceptance Criteria:
  - Revenue heightfield updates within 500ms of time-slider scrub
  - Error-rate rivers visibly intersect revenue terrain at anomaly zones
  - Camera bookmarks save/restore analyst viewpoints
  - Export current frame data as JSON/CSV for reporting
Caching:
  Strategy: LRU eviction with configurable max-size cap
  maxCacheSize: 12
  Eviction: least-recently-used entry dropped when inserting beyond cap
  Tiers:
    terrain_heightfield: LRU(max=12) — precomputed BufferGeometry per time index
    river_geometry: LRU(max=12) — TubeBufferGeometry per anomaly time window
    noise_grid: LRU(max=6) — SimplexNoise grids for terrain detail
    particle_starts: single-entry cache — invalidated on time-window change
    world_to_grid: memoize per-frame (clear on frame boundary)
  Stats: symmetric hit/miss counters for ALL tiers, displayed in diagnostic panel
  Audit rule: zero calls to new THREE.XxxGeometry() inside per-frame or per-tick paths
Export:
  Format: JSON and CSV
  Trigger: Export Current Frame button in control panel
  Content: vertex positions, vertex colors (metric values), river path coordinates,
    particle positions, camera state, time index
  JSON: structured object with frame_metadata, terrain_vertices, rivers, particles
  CSV: flattened rows with x,y,z,color_r,color_g,color_b,metric_revenue,metric_users,metric_errors
Performance:
  Cache: pre-built geometry variants, swap buffers on slider change
  Particles: reuse BufferGeometry.attributes.position.array, no per-frame allocations
  Debounce: river rebuild debounced 200ms on slider change
  Reuse: TubeBufferGeometry cached, only control points updated on heightfield change
  Batch: particle pathfinding batched into single worker tick
  Memoize: world-to-grid transforms memoized per frame, cleared on frame boundary
  Hot-path audit: confirm zero new THREE.XxxGeometry() in per-frame/tick code
  LRU cap: maxCacheSize=12 prevents unbounded memory growth on large datasets
```
persona.md (updated)
```
3D data visualization engineer and Three.js specialist. Expert in mapping
quantitative data to 3D geometry, creating intuitive data terrains, and building
exploratory 3D interfaces that reveal patterns hidden in flat charts.
DIRECTIVE: Before writing any code, state the real-world problem you are solving
and who the user is. Every visualization must answer: "What decision does this
help someone make?" If you cannot name a specific user and their decision, stop
and define them first.
Rules:
  Terrain: generate 3D heightfield terrain from time-series data with Three.js
    BufferGeometry
  Color: map secondary metrics to vertex colors (vegetation gradient, heat coloring)
  Rivers: trace error/anomaly paths as river geometry carving through the terrain
  Particles: render data flows (API calls, user actions) as particle trails across
    the landscape
  Controls: OrbitControls with smooth damping, auto-rotation mode, and saved
    camera bookmarks
  Time: reshape terrain in real-time as user scrubs through time dimension
  Output: interactive HTML 3D dashboard panel with Three.js terrain, particles,
    and orbit controls
  Cache: before declaring a feature complete, audit the implementation for
    repeated computations and confirm every cacheable output is stored (geometries,
    noise grids, particles, textures)
  Readability: prefer 3-line readable code over 1-line clever code; always add
    one explanatory comment per block of logic
  Hot-path: identify hot-path allocations (each-frame or each-event) and add
    debounce/memoize/cache where geometry or data is rebuilt on repeated calls
  LRU: every cache tier must use LRU eviction with configurable maxSize; default
    maxCacheSize=12
  Export: implement data export as JSON/CSV for the current frame
  Stats: show symmetric hit/miss counters for all cache tiers in diagnostic panel
```
IMPLEMENTATION CHANGES REQUIRED
1. LRU Cache class (src/cache/LRUCache.js or inline in terrain.js)
```javascript
// LRU eviction cache with configurable max size
// Tracks access order — least recently used entry evicted on overflow
class LRUCache {
  constructor(maxSize = 12) {
    this.maxSize = maxSize;
    this.cache = new Map();  // Map preserves insertion/access order
    this.hits = 0;
    this.misses = 0;
  }
  get(key) {
    if (!this.cache.has(key)) {
      this.misses++;
      return undefined;
    }
    // Move to end (most recently used) by delete-then-set
    const value = this.cache.get(key);
    this.cache.delete(key);
    this.cache.set(key, value);
    this.hits++;
    return value;
  }
  set(key, value) {
    // Evict least recently used (first Map entry) if at capacity
    // and key is new (not overwriting existing)
    if (this.cache.size >= this.maxSize && !this.cache.has(key)) {
      const lruKey = this.cache.keys().next().value;
      this.cache.delete(lruKey);
      // Dispose Three.js geometry to free GPU memory
      if (lruKey.value && lruKey.value.dispose) lruKey.value.dispose();
    }
    // Move existing key to end if overwriting
    if (this.cache.has(key)) this.cache.delete(key);
    this.cache.set(key, value);
  }
  getStats() {
    return { hits: this.hits, misses: this.misses, size: this.cache.size, maxSize: this.maxSize };
  }
  clear() {
    // Dispose all geometries before clearing
    for (const [key, value] of this.cache) {
      if (value && value.dispose) value.dispose();
    }
    this.cache.clear();
    this.hits = 0;
    this.misses = 0;
  }
}
```
2. Replace all cache instances (terrain, rivers, noise, particles) with LRUCache instances
Current pattern (unbounded Map/Object cache):
  this.terrainCache = {};
  this.terrainCache[key] = geometry;
New pattern:
  this.terrainCache = new LRUCache(MAX_CACHE_SIZE);
  this.terrainCache.set(key, geometry);
On get:
  const geometry = this.terrainCache.get(key);
  if (!geometry) { /* build, then cache.set */ }
3. Symmetric cache stats panel
Add to diagnostic overlay HTML:
```html
<div id="cache-stats" style="position:fixed; bottom:10px; right:10px; background:rgba(0,0,0,0.7); color:#0f0; font:10px monospace; padding:8px;">
  <div>Terrain: hits=<span id="stat-terrain-hits">0</span> miss=<span id="stat-terrain-misses">0</span> size=<span id="stat-terrain-size">0</span>/12</div>
  <div>Rivers:  hits=<span id="stat-river-hits">0</span> miss=<span id="stat-river-misses">0</span> size=<span id="stat-river-size">0</span>/12</div>
  <div>Noise:   hits=<span id="stat-noise-hits">0</span> miss=<span id="stat-noise-misses">0</span> size=<span id="stat-noise-size">0</span>/6</div>
  <div>Particles:hits=<span id="stat-particle-hits">0</span> miss=<span id="stat-particle-misses">0</span> size=<span id="stat-particle-size">0</span>/1</div>
  <div>Grid:    hits=<span id="stat-grid-hits">0</span> miss=<span id="stat-grid-misses">0</span></div>
</div>
```
Update function called each frame (or on 500ms interval for perf):
```javascript
function updateCacheStatsDisplay() {
  const tiers = [
    { name: 'terrain', cache: this.terrainCache },
    { name: 'river', cache: this.riverCache },
    { name: 'noise', cache: this.noiseCache },
    { name: 'particle', cache: this.particleCache },
    { name: 'grid', cache: this.gridMemo },
  ];
  for (const tier of tiers) {
    const s = tier.cache.getStats();
    setText(`stat-${tier.name}-hits`, s.hits);
    setText(`stat-${tier.name}-misses`, s.misses);
    setText(`stat-${tier.name}-size`, s.size);
  }
}
```
4. Data export feature
Add Export button to control panel:
```html
<button id="btn-export-json">Export JSON</button>
<button id="btn-export-csv">Export CSV</button>
```
Export logic:
```javascript
function exportFrameData(format) {
  // Collect current frame state: terrain vertices, colors, rivers, particles, camera
  const terrainPositions = this.terrainMesh.geometry.attributes.position.array;
  const terrainColors = this.terrainMesh.geometry.attributes.color.array;
  const camera = this.camera;
  const timeIndex = this.currentTimeIndex;
  if (format === 'json') {
    const data = {
      frame_metadata: {
        time_index: timeIndex,
        timestamp: new Date().toISOString(),
        camera: {
          position: camera.position.toArray(),
          target: this.controls.target.toArray(),
        },
      },
      terrain: {
        vertex_count: terrainPositions.length / 3,
        vertices: Array.from(terrainPositions),
        colors: Array.from(terrainColors),
      },
      rivers: this.riverPaths.map(r => ({
        points: r.points.map(p => [p.x, p.y, p.z]),
        error_rate: r.errorRate,
      })),
      particles: {
        positions: Array.from(this.particleSystem.geometry.attributes.position.array),
      },
    };
    downloadFile(JSON.stringify(data, null, 2), 'terrain_frame.json', 'application/json');
  } else {
    // CSV: flatten vertices into rows
    const rows = ['x,y,z,r,g,b,revenue,users,errors'];
    const n = terrainPositions.length / 3;
    const revenueValues = this.currentRevenueData; // per-vertex
    const userValues = this.currentUserData;
    const errorValues = this.currentErrorData;
    for (let i = 0; i < n; i++) {
      const idx = i * 3;
      const cidx = i * 3;
      rows.push([
        terrainPositions[idx], terrainPositions[idx + 1], terrainPositions[idx + 2],
        terrainColors[cidx], terrainColors[cidx + 1], terrainColors[cidx + 2],
        revenueValues[i] || 0, userValues[i] || 0, errorValues[i] || 0,
      ].join(','));
    }
    downloadFile(rows.join('\n'), 'terrain_frame.csv', 'text/csv');
  }
}
function downloadFile(content, filename, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
```
5. Dirty-flag discipline for per-frame caching
The cache-ownership bug mentioned in the summary: per-frame caching was inert because geometry objects were being mutated in-place without a dirty flag, causing cache hits to return stale data.
Fix pattern — add dirty flag to cached geometries:
```javascript
setTerrainCache(timeIndex, geometry) {
  geometry.userData.dirty = false;
  geometry.userData.timeIndex = timeIndex;
  this.terrainCache.set(timeIndex, geometry);
}
// On slider change: mark all cached geometries dirty
// before updating the current one, so any stale cache hit is detected
invalidateTerrainCache() {
  for (const [key, geom] of this.terrainCache.cache) {
    geom.userData.dirty = true;
  }
}
// On cache get: verify clean before returning
getTerrainCache(timeIndex) {
  const geom = this.terrainCache.get(timeIndex);
  if (geom && !geom.userData.dirty) return geom;
  return undefined; // force rebuild
}
```
SUMMARY OF CHANGES
All four feedback items addressed:
- LRU eviction with maxCacheSize=12 replaces unbounded all-24 strategy — prevents OOM
- Data export (JSON/CSV) button added — closes completeness gap
- Symmetric hit/miss stats for all 5 cache tiers — completes monitoring transparency
- Dirty-flag discipline on cached geometries — fixes the cache-ownership bug that made per-frame caching inert
Problem statement and user-story directive embedded in blueprint and persona to force real-analytical framing before any code is written.