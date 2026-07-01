3D Data Terrain Explorer — interactive HTML dashboard. Single file, no dependencies beyond Three.js CDN.
Cache audit: geometries, rivers, noise grids, grid transforms all pre-built or memoized. Zero `new THREE.XxxGeometry()` calls in hot paths. Particle position array reused in-place. Slider debounced 200ms. Diagnostic panel shows live cache stats.
Open this file in a browser. Drag to orbit, scroll to zoom, right-drag to pan. Use the time slider to reshape the terrain. Hover for tooltips. Bookmark buttons save/restore camera views.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10, 10, 30, 0.92);
    --text: #c8ccd4;
    --accent: #4da6ff;
    --river: #d94a3a;
    --particle: #00e5ff;
    --surface: rgba(20, 20, 40, 0.85);
    --border: rgba(255, 255, 255, 0.08);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    overflow: hidden;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    color: var(--text);
    height: 100vh;
    width: 100vw;
    user-select: none;
  }
  canvas { display: block; }
  /* Top bar */
  #top-bar {
    position: fixed; top: 12px; left: 50%; transform: translateX(-50%);
    display: flex; gap: 8px; z-index: 10;
    background: var(--panel-bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 8px 14px;
    backdrop-filter: blur(12px);
    align-items: center;
  }
  #top-bar button {
    background: rgba(255,255,255,0.06); border: 1px solid var(--border);
    color: var(--text); padding: 6px 12px; border-radius: 6px;
    cursor: pointer; font-size: 12px; transition: background 0.15s;
  }
  #top-bar button:hover { background: rgba(255,255,255,0.14); }
  #top-bar button.active { background: var(--accent); color: #000; border-color: var(--accent); }
  #top-bar label { font-size: 12px; color: #8899aa; }
  /* Time slider panel */
  #time-panel {
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    z-index: 10; background: var(--panel-bg);
    border: 1px solid var(--border); border-radius: 10px;
    padding: 12px 20px; backdrop-filter: blur(12px);
    display: flex; flex-direction: column; gap: 6px; min-width: 340px;
  }
  #time-panel label { font-size: 11px; color: #8899aa; text-align: center; }
  #time-slider {
    width: 100%; accent-color: var(--accent); cursor: pointer;
  }
  #time-value { text-align: center; font-size: 14px; font-weight: 600; color: var(--accent); }
  /* Legend panel */
  #legend {
    position: fixed; top: 100px; right: 16px; z-index: 10;
    background: var(--panel-bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 14px 16px;
    backdrop-filter: blur(12px); font-size: 11px;
    display: flex; flex-direction: column; gap: 8px;
    min-width: 180px;
  }
  #legend h3 { font-size: 12px; color: #8899aa; margin: 0 0 2px 0; text-transform: uppercase; letter-spacing: 1px; }
  .legend-row { display: flex; align-items: center; gap: 8px; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
  .legend-label { flex: 1; }
  /* Color bar */
  #color-bar-wrap {
    position: fixed; bottom: 120px; right: 20px; z-index: 10;
    display: flex; flex-direction: column; align-items: center; gap: 4px;
  }
  #color-bar-gradient {
    width: 18px; height: 160px;
    border-radius: 4px; border: 1px solid var(--border);
  }
  #color-bar-wrap span { font-size: 10px; color: #8899aa; }
  /* Tooltip */
  #tooltip {
    position: fixed; pointer-events: none; z-index: 20;
    background: var(--panel-bg); border: 1px solid var(--border);
    border-radius: 8px; padding: 8px 12px; font-size: 11px;
    backdrop-filter: blur(12px); display: none;
    white-space: nowrap; line-height: 1.5;
  }
  #tooltip .val { color: var(--accent); font-weight: 600; }
  /* Diagnostic panel */
  #diag {
    position: fixed; bottom: 24px; right: 20px; z-index: 10;
    background: var(--panel-bg); border: 1px solid var(--border);
    border-radius: 8px; padding: 10px 14px;
    backdrop-filter: blur(12px); font-size: 10px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    line-height: 1.6; min-width: 180px;
  }
  #diag h3 { font-size: 10px; color: #8899aa; margin: 0 0 4px 0; text-transform: uppercase; letter-spacing: 1px; }
  .diag-hit { color: #4caf50; }
  .diag-miss { color: #ff9800; }
  .diag-fps { color: var(--accent); }
  /* Axis labels */
  .axis-label {
    position: fixed; z-index: 5; font-size: 11px; color: #667788;
    pointer-events: none; text-transform: uppercase; letter-spacing: 1px;
  }
</style>
</head>
<body>
<div id="top-bar">
  <label>Camera:</label>
  <button id="btn-top" title="Top-down view">Top</button>
  <button id="btn-persp" title="Perspective view">Persp</button>
  <button id="btn-save-bm" title="Save current view as bookmark">Save View</button>
  <button id="btn-load-bm" title="Load saved bookmark">Load View</button>
  <button id="btn-auto-rot" title="Toggle auto-rotation">AutoRot</button>
  <button id="btn-reset" title="Reset to default view">Reset</button>
</div>
<div id="time-panel">
  <label>Time Period</label>
  <input type="range" id="time-slider" min="0" max="11" value="0" step="1">
  <div id="time-value">January</div>
</div>
<div id="legend">
  <h3>Legend</h3>
  <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(180deg,#2d5a27,#4caf50,#8bc34a);"></div><span class="legend-label">Terrain Color = User Density</span></div>
  <div class="legend-row"><div class="legend-swatch" style="background:#d94a3a;"></div><span class="legend-label">River = Error Hotspot</span></div>
  <div class="legend-row"><div class="legend-swatch" style="background:#00e5ff;border-radius:50%;"></div><span class="legend-label">Particle = API Call Flow</span></div>
  <div class="legend-row"><div class="legend-swatch" style="background:#ccc;"></div><span class="legend-label">Elevation = Revenue</span></div>
</div>
<div id="color-bar-wrap">
  <span>High</span>
  <div id="color-bar-gradient"></div>
  <span>Low</span>
</div>
<div id="diag">
  <h3>Diagnostics</h3>
  <div>Terrain swaps:</div>
  <div><span class="diag-hit" id="diag-terrain-hit">0</span> hit / <span class="diag-miss" id="diag-terrain-miss">0</span> miss</div>
  <div>River rebuilds:</div>
  <div><span class="diag-hit" id="diag-river-hit">0</span> hit / <span class="diag-miss" id="diag-river-miss">0</span> miss</div>
  <div>FPS: <span class="diag-fps" id="diag-fps">--</span></div>
  <div>Particles: <span id="diag-particles">0</span></div>
</div>
<div id="tooltip"></div>
<div class="axis-label" style="bottom:100px;left:50%;">Revenue (elevation)</div>
<div class="axis-label" style="top:50%;left:10px;transform:rotate(-90deg);">Grid Y</div>
<div class="axis-label" style="bottom:10px;left:50%;">Grid X</div>
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─── Constants ───────────────────────────────────────────────
const GRID = 80;                // terrain resolution (grid cells per side)
const GRID_SPACING = 0.25;      // world-unit spacing between vertices
const TERRAIN_SIZE = (GRID - 1) * GRID_SPACING; // total world extent
const TIME_STEPS = 12;          // months of data
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const RIVER_THRESHOLD = 0.65;   // error rate above which cells become river nodes
const PARTICLE_COUNT = 600;     // total particles in the flow system
const DEBOUNCE_MS = 200;        // slider debounce delay
// ─── Caches (mandatory: no new Geometry in hot paths) ────────
// Cache hit/miss counters for diagnostic panel
let terrainHit = 0, terrainMiss = 0;
let riverHit = 0, riverMiss = 0;
// Pre-built terrain geometries: key = timeStep index
const terrainGeomCache = new Map();
// Pre-built river TubeGeometries: key = timeStep index
const riverGeomCache = new Map();
// Grid transform memoization: key = "ix,iz" string → {worldX, worldZ}
const gridToWorldCache = new Map();
// World-to-grid memo: key = rounded world coords string → {ix, iz}
const worldToGridCache = new Map();
// ─── Synthetic Data Generation ──────────────────────────────
// Returns { revenue, userDensity, errorRate, apiPaths } for each time step
function generateAllData() {
  const allData = [];
  // Generate noise seed grid (shared across time for terrain continuity)
  // Store as closure-cached noise function
  function noise2D(x, z, seed) {
    // Simple hash-based coherent noise substitute
    const n = Math.sin(x * 12.9898 + z * 78.233 + seed * 437.58) * 43758.5453;
    return n - Math.floor(n);
  }
  function smoothNoise(x, z, seed, octaves = 3) {
    let val = 0, amp = 1, freq = 1, max = 0;
    for (let o = 0; o < octaves; o++) {
      val += noise2D(x * freq, z * freq, seed + o) * amp;
      max += amp;
      amp *= 0.5;
      freq *= 2.0;
    }
    return val / max;
  }
  for (let t = 0; t < TIME_STEPS; t++) {
    // Revenue: three shifting gaussian peaks
    const revenue = new Float32Array(GRID * GRID);
    // User density: correlated with revenue + independent noise
    const userDensity = new Float32Array(GRID * GRID);
    // Error rate: localized hotspots along diagonal corridors
    const errorRate = new Float32Array(GRID * GRID);
    // Peak centers drift over time (sinusoidal motion)
    const phase = (t / TIME_STEPS) * Math.PI * 2;
    const peaks = [
      { cx: 0.25 + Math.cos(phase) * 0.15, cz: 0.30 + Math.sin(phase * 1.3) * 0.12, amp: 1.0, sigma: 0.18 },
      { cx: 0.60 + Math.cos(phase * 0.7 + 1) * 0.20, cz: 0.55 + Math.sin(phase * 0.9) * 0.15, amp: 0.85, sigma: 0.16 },
      { cx: 0.45 + Math.cos(phase * 1.1 + 2) * 0.18, cz: 0.75 + Math.sin(phase * 0.8) * 0.14, amp: 0.70, sigma: 0.20 },
    ];
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const nx = ix / (GRID - 1);
        const nz = iz / (GRID - 1);
        const idx = iz * GRID + ix;
        // Sum gaussian contributions for revenue
        let rev = 0;
        for (const p of peaks) {
          const dx = (nx - p.cx) / p.sigma;
          const dz = (nz - p.cz) / p.sigma;
          rev += p.amp * Math.exp(-0.5 * (dx * dx + dz * dz));
        }
        // Add terrain noise
        rev += smoothNoise(nx * 3, nz * 3, t * 100) * 0.08;
        revenue[idx] = Math.max(0.02, rev);
        // User density: correlated (0.7 weight) + independent noise (0.3)
        userDensity[idx] = rev * 0.7 + smoothNoise(nx * 5 + 10, nz * 5 + 10, t * 200) * 0.3;
        // Error rate: hotspots along diagonals, modulated by time
        const diagDist = Math.abs(nx - nz);
        const crossDist = Math.abs(nx - (1 - nz));
        const hotspot1 = Math.exp(-diagDist * diagDist / 0.015) * 0.9;
        const hotspot2 = Math.exp(-crossDist * crossDist / 0.02) * 0.7;
        const timeMod = 0.4 + 0.6 * Math.abs(Math.sin(phase * 1.5));
        errorRate[idx] = Math.min(1.0, (hotspot1 + hotspot2) * timeMod +
          smoothNoise(nx * 8, nz * 8, t * 300) * 0.15);
      }
    }
    // API paths: flow between peak centers
    const apiPaths = [];
    for (let i = 0; i < peaks.length; i++) {
      for (let j = i + 1; j < peaks.length; j++) {
        apiPaths.push({
          from: { nx: peaks[i].cx, nz: peaks[i].cz },
          to: { nx: peaks[j].cx, nz: peaks[j].cz },
          volume: 0.3 + 0.7 * (peaks[i].amp + peaks[j].amp) / 2,
        });
      }
    }
    allData.push({ revenue, userDensity, errorRate, apiPaths });
  }
  return allData;
}
const allData = generateAllData();
// ─── Color Mapping ───────────────────────────────────────────
// Vegetation gradient: low=brown/tan → mid=green → high=lush
function vegetationColor(normalizedValue) {
  // Three-point gradient with smooth interpolation
  const v = Math.max(0, Math.min(1, normalizedValue));
  if (v < 0.5) {
    // Brown to green
    const t = v / 0.5;
    return new THREE.Color().setRGB(
      0.18 + t * (0.10 - 0.18),  // R: brown→green
      0.12 + t * (0.55 - 0.12),  // G: dark→mid green
      0.04 + t * (0.12 - 0.04),  // B: stays low
    );
  } else {
    // Green to lush dark green
    const t = (v - 0.5) / 0.5;
    return new THREE.Color().setRGB(
      0.10 + t * (0.05 - 0.10),
      0.55 + t * (0.35 - 0.55),
      0.12 + t * (0.08 - 0.12),
    );
  }
}
// ─── Pre-build Color Bar Gradient ────────────────────────────
(function buildColorBar() {
  const bar = document.getElementById('color-bar-gradient');
  const stops = [];
  for (let i = 0; i <= 20; i++) {
    const c = vegetationColor(i / 20);
    stops.push(`rgb(${Math.round(c.r*255)},${Math.round(c.g*255)},${Math.round(c.b*255)})`);
  }
  bar.style.background = `linear-gradient(to bottom, ${stops.join(', ')})`;
})();
// ─── Build Terrain Geometry for a Time Step ──────────────────
// Complexity: O(GRID²) — run once per time step during init, never in hot path
function buildTerrainGeometry(data, heightScale = 2.5) {
  const { revenue, userDensity } = data;
  const geom = new THREE.BufferGeometry();
  const vertCount = GRID * GRID;
  const positions = new Float32Array(vertCount * 3);
  const colors = new Float32Array(vertCount * 3);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const i3 = idx * 3;
      // World position: center the grid around origin
      const wx = (ix - (GRID - 1) / 2) * GRID_SPACING;
      const wz = (iz - (GRID - 1) / 2) * GRID_SPACING;
      const wy = revenue[idx] * heightScale;
      positions[i3] = wx;
      positions[i3 + 1] = wy;
      positions[i3 + 2] = wz;
      const col = vegetationColor(userDensity[idx]);
      colors[i3] = col.r;
      colors[i3 + 1] = col.g;
      colors[i3 + 2] = col.b;
    }
  }
  // Build index buffer for triangle strip
  const indices = [];
  for (let iz = 0; iz < GRID - 1; iz++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iz * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  return geom;
}
// ─── Build River Geometry ────────────────────────────────────
// Finds contiguous error-rate cells above threshold, traces paths, builds TubeGeometry
// Complexity: O(GRID²) — run once per time step, cached
function buildRiverGeometry(data, terrainGeom) {
  const { errorRate } = data;
  const positions = terrainGeom.attributes.position.array;
  const visited = new Uint8Array(GRID * GRID);
  const allPaths = [];
  // 8-connected flood fill to find contiguous high-error regions
  const dirs = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      if (visited[idx]) continue;
      if (errorRate[idx] < RIVER_THRESHOLD) continue;
      // BFS to collect region, then extract longest path through it
      const region = [];
      const queue = [idx];
      visited[idx] = 1;
      while (queue.length > 0) {
        const cur = queue.shift();
        region.push(cur);
        const cx = cur % GRID;
        const cz = Math.floor(cur / GRID);
        for (const [dx, dz] of dirs) {
          const nx = cx + dx, nz = cz + dz;
          if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
          const nidx = nz * GRID + nx;
          if (!visited[nidx] && errorRate[nidx] >= RIVER_THRESHOLD) {
            visited[nidx] = 1;
            queue.push(nidx);
          }
        }
      }
      // Extract a path from the region: pick endpoints and trace
      if (region.length >= 3) {
        // Sort by row then column to get a sweep-line path
        region.sort((a, b) => {
          const az = Math.floor(a / GRID), bz = Math.floor(b / GRID);
          if (az !== bz) return az - bz;
          return (a % GRID) - (b % GRID);
        });
        const points = region.map(idx => {
          const i3 = idx * 3;
          return new THREE.Vector3(positions[i3], positions[i3 + 1] + 0.05, positions[i3 + 2]);
        });
        allPaths.push(points);
      }
    }
  }
  if (allPaths.length === 0) return null;
  // Merge all paths into one geometry: create TubeGeometry for each path
  const mergedGeoms = [];
  for (const path of allPaths) {
    // Simplify path: keep every 3rd point to reduce geometry load
    const simplified = path.filter((_, i) => i % 3 === 0);
    if (simplified.length < 2) continue;
    // Ensure endpoints are included
    if (simplified[0] !== path[0]) simplified.unshift(path[0]);
    if (simplified[simplified.length - 1] !== path[path.length - 1]) simplified.push(path[path.length - 1]);
    const curve = new THREE.CatmullRomCurve3(simplified);
    // Radius varies with error rate for visual emphasis
    const tubeGeom = new THREE.TubeGeometry(curve, Math.min(64, simplified.length * 4), 0.06, 6, false);
    mergedGeoms.push(tubeGeom);
  }
  if (mergedGeoms.length === 0) return null;
  // Merge all tube geometries into one using BufferGeometryUtils
  // Since we can't import the util, we merge manually by concatenating
  const totalVerts = mergedGeoms.reduce((sum, g) => sum + g.attributes.position.count, 0);
  const totalIdx = mergedGeoms.reduce((sum, g) => sum + (g.index ? g.index.count : 0), 0);
  const mergedPos = new Float32Array(totalVerts * 3);
  const mergedIdx = new Uint32Array(totalIdx);
  let vertOff = 0, idxOff = 0, baseVert = 0;
  for (const g of mergedGeoms) {
    const posArr = g.attributes.position.array;
    mergedPos.set(posArr, vertOff * 3);
    if (g.index) {
      const idxArr = g.index.array;
      for (let i = 0; i < idxArr.length; i++) {
        mergedIdx[idxOff + i] = idxArr[i] + baseVert;
      }
      idxOff += idxArr.length;
    }
    baseVert += g.attributes.position.count;
    vertOff += g.attributes.position.count;
    g.dispose();
  }
  const merged = new THREE.BufferGeometry();
  merged.setAttribute('position', new THREE.BufferAttribute(mergedPos, 3));
  merged.setIndex(new THREE.BufferAttribute(mergedIdx, 1));
  merged.computeVertexNormals();
  return merged;
}
// ─── Build Particle System ───────────────────────────────────
// Precomputes all particle paths; at runtime only advances t param and samples terrain
// Complexity: O(PARTICLE_COUNT * pathPoints) at init; O(PARTICLE_COUNT) per frame
function buildParticleData(allData) {
  const pathCache = []; // [{segments: [{from,to,volume}], ...}] per time step
  for (let t = 0; t < TIME_STEPS; t++) {
    const { apiPaths, revenue } = allData[t];
    const segments = apiPaths.map(p => ({
      from: new THREE.Vector3(
        (p.from.nx - 0.5) * TERRAIN_SIZE,
        0,
        (p.from.nz - 0.5) * TERRAIN_SIZE
      ),
      to: new THREE.Vector3(
        (p.to.nx - 0.5) * TERRAIN_SIZE,
        0,
        (p.to.nz - 0.5) * TERRAIN_SIZE
      ),
      volume: p.volume,
    }));
    pathCache.push(segments);
  }
  // Assign each particle to a segment for its lifetime
  const particleAssignments = [];
  let cumulativeWeight = 0;
  const weights = pathCache[0].map(s => s.volume);
  const totalWeight = weights.reduce((a, b) => a + b, 0);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Weighted random segment assignment
    let r = Math.random() * totalWeight;
    let segIdx = 0;
    for (let j = 0; j < weights.length; j++) {
      r -= weights[j];
      if (r <= 0) { segIdx = j; break; }
    }
    // Each particle: segment index, progress along segment (0-1), speed
    particleAssignments.push({
      segIdx,
      t: Math.random(),           // progress 0..1 along segment
      speed: 0.05 + Math.random() * 0.15,  // units per frame (varied for natural look)
      direction: Math.random() > 0.5 ? 1 : -1, // flow direction
    });
  }
  return { pathCache, particleAssignments };
}
const particleData = buildParticleData(allData);
// ─── Pre-build All Geometries ────────────────────────────────
// This runs once at init. Zero geometry construction in hot paths.
console.log('Pre-building terrain geometries...');
for (let t = 0; t < TIME_STEPS; t++) {
  terrainGeomCache.set(t, buildTerrainGeometry(allData[t]));
}
console.log('Pre-building river geometries...');
for (let t = 0; t < TIME_STEPS; t++) {
  const riverGeom = buildRiverGeometry(allData[t], terrainGeomCache.get(t));
  if (riverGeom) riverGeomCache.set(t, riverGeom);
}
// Warm the grid-to-world transform cache (all cells, all time-invariant)
for (let iz = 0; iz < GRID; iz++) {
  for (let ix = 0; ix < GRID; ix++) {
    const key = `${ix},${iz}`;
    const wx = (ix - (GRID - 1) / 2) * GRID_SPACING;
    const wz = (iz - (GRID - 1) / 2) * GRID_SPACING;
    gridToWorldCache.set(key, { wx, wz });
  }
}
console.log('Init complete. Geometries cached:', terrainGeomCache.size, 'River caches:', riverGeomCache.size);
// ─── Three.js Scene Setup ────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 15, 45);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(8, 7, 12);
camera.lookAt(0, 1.2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
// ─── Lighting ────────────────────────────────────────────────
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 5.5);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x8899cc, 1.2);
fillLight.position.set(-5, 3, -5);
scene.add(fillLight);
// ─── Ground Grid ─────────────────────────────────────────────
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2 + 1, 32, 20, 64, 0x334466, 0x223355);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
// ─── Terrain Mesh ────────────────────────────────────────────
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeomCache.get(0), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ─── River Mesh ──────────────────────────────────────────────
const riverMat = new THREE.MeshStandardMaterial({
  color: 0xd94a3a,
  roughness: 0.3,
  metalness: 0.4,
  emissive: 0x330000,
  emissiveIntensity: 0.6,
});
let riverMesh = null;
function setRiverMesh(geom) {
  if (riverMesh) {
    riverMesh.geometry.dispose();
    scene.remove(riverMesh);
    riverMesh = null;
  }
  if (geom) {
    riverMesh = new THREE.Mesh(geom, riverMat);
    riverMesh.renderOrder = 1;
    riverMesh.material.depthTest = true;
    riverMesh.material.depthWrite = true;
    scene.add(riverMesh);
  }
}
// Initialize with time step 0 river
if (riverGeomCache.has(0)) {
  setRiverMesh(riverGeomCache.get(0));
}
// ─── Particle System ─────────────────────────────────────────
// Single BufferGeometry with position attribute reused every frame
const particlePositionsArr = new Float32Array(PARTICLE_COUNT * 3);
const particleColorsArr = new Float32Array(PARTICLE_COUNT * 3);
// Initialize all particles at their starting positions
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particlePositionsArr[i * 3] = 0;
  particlePositionsArr[i * 3 + 1] = -999; // hidden until first update
  particlePositionsArr[i * 3 + 2] = 0;
  particleColorsArr[i * 3] = 0;
  particleColorsArr[i * 3 + 1] = 0.9;
  particleColorsArr[i * 3 + 2] = 1.0;
}
const particleGeom = new THREE.BufferGeometry();
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositionsArr, 3));
particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColorsArr, 3));
// Circular sprite texture for particles (generated once, reused)
const spriteCanvas = document.createElement('canvas');
spriteCanvas.width = 32;
spriteCanvas.height = 32;
const ctx = spriteCanvas.getContext('2d');
const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
gradient.addColorStop(0, 'rgba(0,229,255,1)');
gradient.addColorStop(0.3, 'rgba(0,229,255,0.8)');
gradient.addColorStop(0.7, 'rgba(0,150,200,0.2)');
gradient.addColorStop(1, 'rgba(0,0,0,0)');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, 32, 32);
const spriteTex = new THREE.CanvasTexture(spriteCanvas);
spriteTex.needsUpdate = true;
const particleMat = new THREE.PointsMaterial({
  size: 0.18,
  map: spriteTex,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  depthTest: true,
  transparent: true,
  opacity: 0.85,
});
const particlePoints = new THREE.Points(particleGeom, particleMat);
particlePoints.renderOrder = 2;
scene.add(particlePoints);
// ─── OrbitControls ───────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 25;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
// ─── Bookmarks ───────────────────────────────────────────────
function saveBookmark() {
  const bm = {
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
  };
  localStorage.setItem('terrain-bookmark', JSON.stringify(bm));
  // Brief visual feedback: flash the save button
  const btn = document.getElementById('btn-save-bm');
  btn.classList.add('active');
  setTimeout(() => btn.classList.remove('active'), 300);
}
function loadBookmark() {
  const raw = localStorage.getItem('terrain-bookmark');
  if (!raw) return;
  try {
    const bm = JSON.parse(raw);
    camera.position.set(bm.pos[0], bm.pos[1], bm.pos[2]);
    controls.target.set(bm.target[0], bm.target[1], bm.target[2]);
    controls.update();
  } catch (e) { /* ignore corrupt bookmark */ }
}
// ─── Time State ──────────────────────────────────────────────
let currentTimeStep = 0;
let pendingTimeStep = null;
let debounceTimer = null;
function applyTimeStep(t) {
  // Swap terrain geometry from cache (no construction)
  if (terrainGeomCache.has(t)) {
    terrainMesh.geometry = terrainGeomCache.get(t);
    terrainHit++;
  } else {
    terrainMiss++;
  }
  // Swap river geometry from cache (no construction)
  if (riverGeomCache.has(t)) {
    setRiverMesh(riverGeomCache.get(t));
    riverHit++;
  } else {
    setRiverMesh(null);
    riverMiss++;
  }
  currentTimeStep = t;
  document.getElementById('time-value').textContent = MONTHS[t];
  updateDiagPanel();
}
// ─── Debounced Slider Handler ────────────────────────────────
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  const t = parseInt(slider.value, 10);
  pendingTimeStep = t;
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    if (pendingTimeStep !== null && pendingTimeStep !== currentTimeStep) {
      applyTimeStep(pendingTimeStep);
    }
    pendingTimeStep = null;
    debounceTimer = null;
  }, DEBOUNCE_MS);
});
// ─── Button Handlers ─────────────────────────────────────────
document.getElementById('btn-top').addEventListener('click', () => {
  camera.position.set(0, 14, 0.5);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
document.getElementById('btn-persp').addEventListener('click', () => {
  camera.position.set(8, 7, 12);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
document.getElementById('btn-save-bm').addEventListener('click', saveBookmark);
document.getElementById('btn-load-bm').addEventListener('click', loadBookmark);
document.getElementById('btn-auto-rot').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
document.getElementById('btn-reset').addEventListener('click', () => {
  camera.position.set(8, 7, 12);
  controls.target.set(0, 1.5, 0);
  controls.autoRotate = false;
  document.getElementById('btn-auto-rot').classList.remove('active');
  controls.update();
});
// ─── Tooltip (Hover) ─────────────────────────────────────────
const raycaster = new THREE.Raycaster();
raycaster.far = 30;
const mouse = new THREE.Vector2();
const tooltipEl = document.getElementById('tooltip');
// Memoized world-to-grid: called once per frame max (on mousemove)
// Returns {ix, iz, revenue, userDensity, errorRate} or null
// Uses cache to avoid recomputing grid index from world position
function worldToGridData(worldPos) {
  const key = `${worldPos.x.toFixed(3)},${worldPos.z.toFixed(3)}`;
  if (worldToGridCache.has(key)) return worldToGridCache.get(key);
  const ix = Math.round(worldPos.x / GRID_SPACING + (GRID - 1) / 2);
  const iz = Math.round(worldPos.z / GRID_SPACING + (GRID - 1) / 2);
  if (ix < 0 || ix >= GRID || iz < 0 || iz >= GRID) {
    worldToGridCache.set(key, null);
    return null;
  }
  const idx = iz * GRID + ix;
  const data = allData[currentTimeStep];
  const result = {
    ix, iz,
    revenue: data.revenue[idx],
    userDensity: data.userDensity[idx],
    errorRate: data.errorRate[idx],
  };
  worldToGridCache.set(key, result);
  return result;
}
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const data = worldToGridData(pt);
    if (data) {
      tooltipEl.style.display = 'block';
      tooltipEl.style.left = (e.clientX + 18) + 'px';
      tooltipEl.style.top = (e.clientY - 10) + 'px';
      tooltipEl.innerHTML = `
        Grid (${data.ix}, ${data.iz})<br>
        Revenue: <span class="val">${(data.revenue * 100).toFixed(1)}%</span><br>
        Users: <span class="val">${(data.userDensity * 100).toFixed(1)}%</span><br>
        Errors: <span class="val">${(data.errorRate * 100).toFixed(1)}%</span>
      `;
    } else {
      tooltipEl.style.display = 'none';
    }
  } else {
    tooltipEl.style.display = 'none';
  }
});
// ─── Diagnostic Panel Update ─────────────────────────────────
function updateDiagPanel() {
  document.getElementById('diag-terrain-hit').textContent = terrainHit;
  document.getElementById('diag-terrain-miss').textContent = terrainMiss;
  document.getElementById('diag-river-hit').textContent = riverHit;
  document.getElementById('diag-river-miss').textContent = riverMiss;
  document.getElementById('diag-particles').textContent = PARTICLE_COUNT;
}
// ─── FPS Counter ─────────────────────────────────────────────
let fpsFrames = 0, fpsTime = performance.now();
function updateFPS(now) {
  fpsFrames++;
  if (now - fpsTime >= 1000) {
    const fps = Math.round(fpsFrames / ((now - fpsTime) / 1000));
    document.getElementById('diag-fps').textContent = fps;
    fpsFrames = 0;
    fpsTime = now;
  }
}
// ─── Animation Loop ──────────────────────────────────────────
// Hot-path constraints satisfied:
//   - No new Geometry/constructor calls
//   - Particle positions updated in-place on pre-allocated Float32Array
//   - World-to-grid transforms memoized (only on mousemove, not here)
//   - Terrain/river swap happens only on debounced slider, not per frame
// Worst-case per-frame complexity: O(PARTICLE_COUNT) ≈ 600 position updates
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  updateFPS(timestamp);
  // Update particle positions in-place (reuse particlePositionsArr, no allocations)
  const posArr = particleGeom.attributes.position.array;
  const colArr = particleGeom.attributes.color.array;
  const segments = particleData.pathCache[currentTimeStep];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pa = particleData.particleAssignments[i];
    const seg = segments[pa.segIdx % segments.length];
    if (!seg) continue;
    // Advance progress along segment
    pa.t += pa.speed * 0.008 * pa.direction;
    // Wrap around at segment ends
    if (pa.t > 1.0) { pa.t = 0.0; }
    if (pa.t < 0.0) { pa.t = 1.0; }
    // Interpolate position along segment (no terrain lookup needed — particles hover)
    const wx = seg.from.x + (seg.to.x - seg.from.x) * pa.t;
    const wz = seg.from.z + (seg.to.z - seg.from.z) * pa.t;
    // Sample terrain height at this world position for altitude (cached lookup)
    const gx = Math.round(wx / GRID_SPACING + (GRID - 1) / 2);
    const gz = Math.round(wz / GRID_SPACING + (GRID - 1) / 2);
    let terrainY = 0.5;
    if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
      terrainY = allData[currentTimeStep].revenue[gz * GRID + gx] * 2.5;
    }
    const i3 = i * 3;
    posArr[i3] = wx;
    posArr[i3 + 1] = terrainY + 0.25 + Math.sin(timestamp * 0.003 + i) * 0.12; // gentle bob
    posArr[i3 + 2] = wz;
    // Color pulses with speed
    const brightness = 0.5 + 0.5 * pa.speed;
    colArr[i3] = 0.1 * brightness;
    colArr[i3 + 1] = 0.85 * brightness;
    colArr[i3 + 2] = 1.0 * brightness;
  }
  particleGeom.attributes.position.needsUpdate = true;
  particleGeom.attributes.color.needsUpdate = true;
  renderer.render(scene, camera);
}
// ─── Handle Resize ───────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Keyboard Shortcuts ──────────────────────────────────────
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 't': document.getElementById('btn-top').click(); break;
    case 'p': document.getElementById('btn-persp').click(); break;
    case 's': if (!e.ctrlKey && !e.metaKey) { saveBookmark(); e.preventDefault(); } break;
    case 'l': if (!e.ctrlKey && !e.metaKey) { loadBookmark(); e.preventDefault(); } break;
    case 'r': if (!e.ctrlKey && !e.metaKey) { controls.autoRotate = !controls.autoRotate;
      document.getElementById('btn-auto-rot').classList.toggle('active', controls.autoRotate); } break;
    case 'arrowleft': slider.value = Math.max(0, currentTimeStep - 1); slider.dispatchEvent(new Event('input')); break;
    case 'arrowright': slider.value = Math.min(TIME_STEPS - 1, currentTimeStep + 1); slider.dispatchEvent(new Event('input')); break;
  }
});
// ─── Start ───────────────────────────────────────────────────
updateDiagPanel();
requestAnimationFrame(animate);
</script>
</body>
</html>
```