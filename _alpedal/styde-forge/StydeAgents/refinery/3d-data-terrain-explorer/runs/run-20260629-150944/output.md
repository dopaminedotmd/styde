<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a0f; --panel: #12121a; --border: #1e1e2e; --text: #c8c8d4; --accent: #4fc3f7; --warn: #ff8a65; --good: #81c784; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; height: 100vh; }
  #canvas-container { position: fixed; inset: 0; z-index: 1; }
  canvas { display: block; }
  #overlay { position: fixed; z-index: 10; pointer-events: none; inset: 0; }
  #overlay > * { pointer-events: auto; }
  #top-bar { position: absolute; top: 16px; left: 16px; right: 16px; display: flex; gap: 12px; align-items: flex-start; }
  .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; backdrop-filter: blur(12px); }
  #legend { min-width: 200px; }
  #legend h3 { font-size: 13px; font-weight: 600; margin-bottom: 8px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px; }
  .legend-row { display: flex; align-items: center; gap: 8px; font-size: 11px; margin: 4px 0; }
  .legend-swatch { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
  .legend-swatch.elevation { background: linear-gradient(180deg, #1a237e, #4fc3f7, #81c784, #ffeb3b, #ff8a65); }
  .legend-swatch.river { background: #ef5350; }
  .legend-swatch.particle { background: #ffab40; }
  #diagnostics { position: absolute; top: 16px; right: 16px; min-width: 180px; font-size: 11px; line-height: 1.6; }
  #diagnostics h3 { font-size: 11px; font-weight: 600; margin-bottom: 4px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.5px; }
  .diag-row { display: flex; justify-content: space-between; }
  .diag-val { color: var(--good); font-variant-numeric: tabular-nums; }
  .diag-val.miss { color: var(--warn); }
  #time-bar { position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 12px; }
  #time-slider { width: 360px; accent-color: var(--accent); cursor: pointer; }
  #time-label { font-size: 12px; font-variant-numeric: tabular-nums; min-width: 80px; text-align: center; color: var(--text); }
  #btn-auto-rotate { background: var(--panel); border: 1px solid var(--border); color: var(--text); padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 11px; transition: all 0.2s; }
  #btn-auto-rotate.active { background: var(--accent); color: #000; border-color: var(--accent); }
  #btn-auto-rotate:hover { border-color: var(--accent); }
  #bookmarks { position: absolute; bottom: 80px; left: 50%; transform: translateX(-50%); display: flex; gap: 6px; }
  .bookmark-btn { background: var(--panel); border: 1px solid var(--border); color: var(--text); padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 10px; transition: all 0.2s; }
  .bookmark-btn:hover { border-color: var(--accent); color: var(--accent); }
  #file-drop { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: var(--panel); border: 2px dashed var(--border); border-radius: 14px; padding: 32px 48px; text-align: center; display: none; z-index: 20; }
  #file-drop.visible { display: block; }
  #file-drop h3 { color: var(--accent); margin-bottom: 8px; font-size: 15px; }
  #file-drop p { font-size: 12px; color: #888; }
  #file-drop input { margin-top: 12px; }
  #btn-import { position: absolute; top: 16px; left: 220px; background: var(--panel); border: 1px solid var(--border); color: var(--text); padding: 8px 14px; border-radius: 6px; cursor: pointer; font-size: 11px; z-index: 11; }
  #btn-import:hover { border-color: var(--accent); }
  #tooltip { position: fixed; pointer-events: none; z-index: 15; background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; font-size: 11px; display: none; line-height: 1.5; }
  #metric-panel { position: absolute; top: 16px; left: 220px; display: flex; gap: 16px; }
  .metric { text-align: center; }
  .metric .label { font-size: 10px; color: #888; text-transform: uppercase; }
  .metric .value { font-size: 20px; font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="overlay">
  <div id="top-bar">
    <div id="legend" class="panel">
      <h3>Terrain Map</h3>
      <div class="legend-row"><span class="legend-swatch elevation"></span> Elevation (Revenue)</div>
      <div class="legend-row"><span class="legend-swatch river"></span> Error Rivers</div>
      <div class="legend-row"><span class="legend-swatch particle"></span> API Call Trails</div>
    </div>
    <div id="metric-panel">
      <div class="metric"><div class="label">Revenue</div><div class="value" id="met-rev">---</div></div>
      <div class="metric"><div class="label">Users</div><div class="value" id="met-users">---</div></div>
      <div class="metric"><div class="label">Errors</div><div class="value" id="met-err" style="color:var(--warn)">---</div></div>
    </div>
    <button id="btn-import" title="Import real data (JSON/CSV)">Import Data</button>
  </div>
  <div id="diagnostics" class="panel">
    <h3>Cache Diagnostics</h3>
    <div class="diag-row"><span>Terrain:</span><span class="diag-val" id="diag-terrain">H:0 M:0</span></div>
    <div class="diag-row"><span>River:</span><span class="diag-val" id="diag-river">H:0 M:0</span></div>
    <div class="diag-row"><span>Transform:</span><span class="diag-val" id="diag-transform">H:0 M:0</span></div>
    <div class="diag-row"><span>FPS:</span><span class="diag-val" id="diag-fps">60</span></div>
    <div class="diag-row"><span>Particles:</span><span class="diag-val" id="diag-particles">0</span></div>
  </div>
  <div id="tooltip"></div>
  <div id="bookmarks">
    <button class="bookmark-btn" data-view="overhead">Overhead</button>
    <button class="bookmark-btn" data-view="canyon">Canyon Fly</button>
    <button class="bookmark-btn" data-view="river">River Trace</button>
    <button class="bookmark-btn" data-view="peak">Peak View</button>
  </div>
  <div id="time-bar">
    <span style="font-size:11px;color:#888">Time</span>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label">T+0</span>
    <button id="btn-auto-rotate" class="active" title="Toggle auto-rotation">Auto-Rotate</button>
  </div>
  <div id="file-drop">
    <h3>Drop JSON Data File</h3>
    <p>Format: { "timeSeries": [{ "revenue": number, "users": number, "errors": number, "apiCalls": [[x,z],...] }, ...] }</p>
    <input type="file" id="file-input" accept=".json,.csv">
    <p style="margin-top:8px;font-size:10px;color:#666">Grid: 60x60, up to 200 time steps</p>
  </div>
</div>
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
/* ========================================================================
   DOM REFERENCES — all resolved once at init, never looked up again
   ======================================================================== */
const dom = {
  container: document.getElementById('canvas-container'),
  slider: document.getElementById('time-slider'),
  label: document.getElementById('time-label'),
  tooltip: document.getElementById('tooltip'),
  btnAuto: document.getElementById('btn-auto-rotate'),
  btnImport: document.getElementById('btn-import'),
  fileDrop: document.getElementById('file-drop'),
  fileInput: document.getElementById('file-input'),
  metRev: document.getElementById('met-rev'),
  metUsers: document.getElementById('met-users'),
  metErr: document.getElementById('met-err'),
  diagTerrain: document.getElementById('diag-terrain'),
  diagRiver: document.getElementById('diag-river'),
  diagTransform: document.getElementById('diag-transform'),
  diagFps: document.getElementById('diag-fps'),
  diagParticles: document.getElementById('diag-particles'),
  bookmarks: document.querySelectorAll('.bookmark-btn'),
};
/* ========================================================================
   CONFIGURATION
   ======================================================================== */
const GRID = 60;
const GRID_SPACING = 1.0;
const TERRAIN_SIZE = (GRID - 1) * GRID_SPACING;
const TIME_STEPS = 100;
const PARTICLE_COUNT = 500;
const ELEVATION_SCALE = 8.0;
/* ========================================================================
   CACHE DIAGNOSTICS — counters survive the full session
   ======================================================================== */
const cacheStats = {
  terrain: { hits: 0, misses: 0 },
  river: { hits: 0, misses: 0 },
  transform: { hits: 0, misses: 0 },
};
/* ========================================================================
   DATA GENERATION — synthetic but realistic multi-metric time series
   seeded pseudo-random so terrain is deterministic and reviewable
   ======================================================================== */
function mulberry32(a) {
  return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
function generateTerrainData(seed = 42) {
  const rng = mulberry32(seed);
  // Perlin-style octave noise for natural terrain shape
  function noise(x, z, t, octaves = 4) {
    let val = 0, amp = 1, freq = 1, max = 0;
    for (let o = 0; o < octaves; o++) {
      const nx = x * freq * 0.12 + t * 0.3;
      const nz = z * freq * 0.12 + t * 0.2;
      // Simple hash-based noise — deterministic and fast
      const ix = Math.floor(nx), iz = Math.floor(nz);
      const fx = nx - ix, fz = nz - iz;
      const sx = fx * fx * (3 - 2 * fx), sz = fz * fz * (3 - 2 * fz);
      const h = (ix * 127.1 + iz * 311.7) % 1;
      const n = h * 2 - 1;
      val += n * amp;
      max += amp;
      amp *= 0.5;
      freq *= 2.1;
    }
    return val / max;
  }
  const timeSeries = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const frame = {
      height: new Float32Array(GRID * GRID),
      vegetation: new Float32Array(GRID * GRID),
      error: new Float32Array(GRID * GRID),
      apiCalls: [],
      summary: { revenue: 0, users: 0, errors: 0 },
    };
    // Two competing growth centers that shift over time
    const center1X = 25 + Math.sin(t * 0.08) * 10;
    const center1Z = 25 + Math.cos(t * 0.06) * 8;
    const center2X = 35 + Math.cos(t * 0.07 + 1) * 12;
    const center2Z = 35 + Math.sin(t * 0.09 + 2) * 10;
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iz * GRID + ix;
        // Distance-based elevation from two growth centers
        const d1 = Math.sqrt((ix - center1X) ** 2 + (iz - center1Z) ** 2);
        const d2 = Math.sqrt((ix - center2X) ** 2 + (iz - center2Z) ** 2);
        let h = 3.0 * Math.exp(-d1 * 0.04) + 2.5 * Math.exp(-d2 * 0.05);
        // Add noise for natural texture
        h += noise(ix, iz, t, 4) * 1.2;
        h = Math.max(0, h);
        frame.height[idx] = h;
        // Vegetation (user density) — correlated with elevation but with noise
        let veg = h * 0.3 + noise(ix + 100, iz + 100, t * 0.5, 3) * 0.5;
        veg = Math.max(0, Math.min(1, veg));
        frame.vegetation[idx] = veg;
        // Error rate — inverse of vegetation where terrain is steep
        const errBase = (1 - veg) * 0.4;
        const errNoise = Math.abs(noise(ix + 200, iz + 200, t * 0.7, 2)) * 0.25;
        frame.error[idx] = Math.min(1, errBase + errNoise);
        frame.summary.revenue += h;
        frame.summary.users += veg;
        frame.summary.errors += frame.error[idx];
      }
    }
    // Normalize summaries
    const n = GRID * GRID;
    frame.summary.revenue = +(frame.summary.revenue / n * 100).toFixed(1);
    frame.summary.users = +(frame.summary.users / n * 100).toFixed(1);
    frame.summary.errors = +(frame.summary.errors / n * 100).toFixed(1);
    // API call particle positions — cluster near growth centers
    const apiCalls = [];
    for (let p = 0; p < 30; p++) {
      const angle = rng() * Math.PI * 2;
      const dist = rng() * 25;
      const cx = center1X + (rng() - 0.5) * 8;
      const cz = center1Z + (rng() - 0.5) * 8;
      apiCalls.push({ x: cx, z: cz });
    }
    frame.apiCalls = apiCalls;
    timeSeries.push(frame);
  }
  return timeSeries;
}
let timeSeriesData = generateTerrainData();
/* ========================================================================
   THREE.JS SCENE SETUP
   ======================================================================== */
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
dom.container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a0f');
scene.fog = new THREE.Fog('#0a0a0f', 30, 80);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(35, 28, 45);
camera.lookAt(TERRAIN_SIZE / 2, 0, TERRAIN_SIZE / 2);
/* ========================================================================
   LIGHTING
   ======================================================================== */
const ambient = new THREE.AmbientLight('#304060', 1.6);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffe8cc', 4.5);
sun.position.set(40, 35, 20);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 120;
sun.shadow.camera.left = -40;
sun.shadow.camera.right = 40;
sun.shadow.camera.top = 40;
sun.shadow.camera.bottom = -40;
sun.shadow.bias = -0.0005;
scene.add(sun);
const fill = new THREE.DirectionalLight('#8090c0', 0.8);
fill.position.set(-15, 8, -10);
scene.add(fill);
/* ========================================================================
   ORBIT CONTROLS
   ======================================================================== */
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(TERRAIN_SIZE / 2, 3, TERRAIN_SIZE / 2);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 8;
controls.maxDistance = 70;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
/* ========================================================================
   CAMERA BOOKMARKS
   ======================================================================== */
const bookmarks = {
  overhead: {
    position: new THREE.Vector3(TERRAIN_SIZE / 2, 50, TERRAIN_SIZE / 2 + 0.1),
    target: new THREE.Vector3(TERRAIN_SIZE / 2, 0, TERRAIN_SIZE / 2),
  },
  canyon: {
    position: new THREE.Vector3(10, 6, 8),
    target: new THREE.Vector3(35, 2, 30),
  },
  river: {
    position: new THREE.Vector3(20, 4, 55),
    target: new THREE.Vector3(30, 1, 15),
  },
  peak: {
    position: new THREE.Vector3(45, 18, 50),
    target: new THREE.Vector3(30, 7, 30),
  },
};
let bookmarkAnimating = false;
let bookmarkFrom = null;
let bookmarkTo = null;
let bookmarkProgress = 0;
const BOOKMARK_DURATION = 1.2; // seconds
function animateBookmark(name) {
  const bm = bookmarks[name];
  if (!bm) return;
  bookmarkAnimating = true;
  bookmarkFrom = {
    position: camera.position.clone(),
    target: controls.target.clone(),
  };
  bookmarkTo = bm;
  bookmarkProgress = 0;
}
/* ========================================================================
   TERRAIN MANAGER — on-demand geometry with cache
   ======================================================================== */
const terrainCache = new Map(); // Map<timeIndex, BufferGeometry>
let activeTerrainGeom = null;
let activeTerrainMesh = null;
let activeTimeIndex = -1;
// Vertex color gradient: low=deep blue, mid=green, high=yellow, peak=orange
function elevationColor(normalizedHeight) {
  const h = Math.max(0, Math.min(1, normalizedHeight));
  const r = h < 0.5 ? h * 0.2 : 0.1 + (h - 0.5) * 1.8;
  const g = h < 0.3 ? h * 0.4 : 0.12 + (h - 0.3) * 1.4;
  const b = 1.0 - h * 1.1;
  return [Math.min(1, r), Math.min(1, g), Math.max(0, b)];
}
function buildTerrainGeometry(timeIndex) {
  const data = timeSeriesData[timeIndex];
  const segments = GRID - 1;
  // Allocate vertex arrays
  const vertexCount = GRID * GRID;
  const positions = new Float32Array(vertexCount * 3);
  const colors = new Float32Array(vertexCount * 3);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const vi = idx * 3;
      positions[vi] = ix * GRID_SPACING;
      positions[vi + 1] = data.height[idx] * ELEVATION_SCALE;
      positions[vi + 2] = iz * GRID_SPACING;
      // Color by vegetation blended with elevation
      const veg = data.vegetation[idx];
      const elevNorm = data.height[idx] / 6.0;
      const [er, eg, eb] = elevationColor(elevNorm);
      // Vegetation tints green
      const cr = er * 0.6 + veg * 0.4;
      const cg = eg * 0.5 + veg * 0.5;
      const cb = eb * 0.7 + (1 - veg) * 0.3;
      colors[vi] = cr;
      colors[vi + 1] = cg;
      colors[vi + 2] = cb;
    }
  }
  // Build index array for triangle strips
  const indexCount = segments * segments * 6;
  const indices = new (indexCount > 65535 ? Uint32Array : Uint16Array)(indexCount);
  let ii = 0;
  for (let iz = 0; iz < segments; iz++) {
    for (let ix = 0; ix < segments; ix++) {
      const a = iz * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices[ii++] = a; indices[ii++] = c; indices[ii++] = b;
      indices[ii++] = b; indices[ii++] = c; indices[ii++] = d;
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(new THREE.BufferAttribute(indices, 1));
  geom.computeVertexNormals();
  return geom;
}
function getTerrainGeometry(timeIndex) {
  if (terrainCache.has(timeIndex)) {
    cacheStats.terrain.hits++;
    return terrainCache.get(timeIndex);
  }
  cacheStats.terrain.misses++;
  const geom = buildTerrainGeometry(timeIndex);
  terrainCache.set(timeIndex, geom);
  // Limit cache size: evict oldest when over 60 entries
  if (terrainCache.size > 60) {
    const firstKey = terrainCache.keys().next().value;
    const oldGeom = terrainCache.get(firstKey);
    if (oldGeom && oldGeom !== activeTerrainGeom) {
      oldGeom.dispose();
    }
    terrainCache.delete(firstKey);
  }
  return geom;
}
function applyTerrain(timeIndex) {
  if (timeIndex === activeTimeIndex) return;
  activeTimeIndex = timeIndex;
  const geom = getTerrainGeometry(timeIndex);
  activeTerrainGeom = geom;
  if (activeTerrainMesh) {
    activeTerrainMesh.geometry.dispose();
    scene.remove(activeTerrainMesh);
  }
  const material = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.72,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide,
  });
  const mesh = new THREE.Mesh(geom, material);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  scene.add(mesh);
  activeTerrainMesh = mesh;
  // Update particle heightfield texture (for vertex shader sampling)
  updateParticleHeightfield(timeIndex);
  // Trigger debounced river rebuild
  scheduleRiverRebuild(timeIndex);
  // Update summary metrics
  updateMetrics(timeIndex);
}
/* ========================================================================
   RIVER MANAGER — error path trace, TubeGeometry cached, debounced rebuild
   ======================================================================== */
const riverCache = new Map();
let activeRiverGroup = null;
let riverRebuildTimeout = null;
let pendingRiverTimeIndex = -1;
const RIVER_DEBOUNCE_MS = 200;
function traceErrorPath(timeIndex) {
  const data = timeSeriesData[timeIndex];
  // Find the ridge of highest error concentration using gradient ascent
  // Start from highest-error cell, walk toward steepest error gradient
  const visited = new Uint8Array(GRID * GRID);
  const points = [];
  // Find global max error
  let maxErr = -1, maxIdx = 0;
  for (let i = 0; i < GRID * GRID; i++) {
    if (data.error[i] > maxErr) { maxErr = data.error[i]; maxIdx = i; }
  }
  let currentIdx = maxIdx;
  let cz = Math.floor(currentIdx / GRID);
  let cx = currentIdx % GRID;
  for (let step = 0; step < 80; step++) {
    if (cx < 0 || cx >= GRID || cz < 0 || cz >= GRID) break;
    const idx = cz * GRID + cx;
    if (visited[idx]) break;
    visited[idx] = 1;
    const h = data.height[idx] * ELEVATION_SCALE + 0.25;
    points.push(new THREE.Vector3(cx * GRID_SPACING, h, cz * GRID_SPACING));
    // Walk toward neighbor with highest error
    let bestErr = -1, bestNX = cx, bestNZ = cz;
    for (let dz = -1; dz <= 1; dz++) {
      for (let dx = -1; dx <= 1; dx++) {
        if (dx === 0 && dz === 0) continue;
        const nx = cx + dx, nz = cz + dz;
        if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
        const nidx = nz * GRID + nx;
        if (visited[nidx]) continue;
        if (data.error[nidx] > bestErr) {
          bestErr = data.error[nidx];
          bestNX = nx;
          bestNZ = nz;
        }
      }
    }
    if (bestErr < 0.02) break; // Error too low, stop tracing
    cx = bestNX;
    cz = bestNZ;
  }
  return points;
}
function buildRiverGeometry(timeIndex) {
  const points = traceErrorPath(timeIndex);
  if (points.length < 4) return null;
  const curve = new THREE.CatmullRomCurve3(points);
  const tubeGeom = new THREE.TubeGeometry(curve, 80, 0.28, 8, false);
  return tubeGeom;
}
function getRiverGeometry(timeIndex) {
  if (riverCache.has(timeIndex)) {
    cacheStats.river.hits++;
    return riverCache.get(timeIndex);
  }
  cacheStats.river.misses++;
  const geom = buildRiverGeometry(timeIndex);
  riverCache.set(timeIndex, geom);
  if (riverCache.size > 40) {
    const firstKey = riverCache.keys().next().value;
    const old = riverCache.get(firstKey);
    if (old) old.dispose();
    riverCache.delete(firstKey);
  }
  return geom;
}
function scheduleRiverRebuild(timeIndex) {
  pendingRiverTimeIndex = timeIndex;
  if (riverRebuildTimeout) return; // Debounce: only schedule if not already waiting
  riverRebuildTimeout = setTimeout(() => {
    riverRebuildTimeout = null;
    rebuildRiver(pendingRiverTimeIndex);
  }, RIVER_DEBOUNCE_MS);
}
function rebuildRiver(timeIndex) {
  // Remove old river
  if (activeRiverGroup) {
    activeRiverGroup.traverse(child => {
      if (child.geometry && child.geometry !== activeTerrainGeom) child.geometry.dispose();
      if (child.material) child.material.dispose();
    });
    scene.remove(activeRiverGroup);
    activeRiverGroup = null;
  }
  const tubeGeom = getRiverGeometry(timeIndex);
  if (!tubeGeom) return;
  const riverMat = new THREE.MeshStandardMaterial({
    color: '#ef3530',
    roughness: 0.15,
    metalness: 0.3,
    emissive: '#3a0000',
    emissiveIntensity: 0.5,
  });
  const riverMesh = new THREE.Mesh(tubeGeom, riverMat);
  riverMesh.renderOrder = 1;
  riverMesh.material.depthTest = true;
  riverMesh.material.depthWrite = true;
  // Glow halo beneath river
  const glowGeom = tubeGeom.clone();
  const glowMat = new THREE.MeshBasicMaterial({
    color: '#ff4040',
    transparent: true,
    opacity: 0.18,
    depthWrite: false,
  });
  const glowMesh = new THREE.Mesh(glowGeom, glowMat);
  glowMesh.scale.set(1.5, 1.0, 1.5);
  glowMesh.renderOrder = 0;
  activeRiverGroup = new THREE.Group();
  activeRiverGroup.add(riverMesh);
  activeRiverGroup.add(glowMesh);
  scene.add(activeRiverGroup);
}
/* ========================================================================
   PARTICLE MANAGER — vertex-shader heightfield sampling via DataTexture
   Reuses BufferGeometry position array; never allocates per-frame
   ======================================================================== */
let particleSystem = null;
let particleHeightTexture = null;
let particlePositionsArray = null; // Reused Float32Array reference
function createHeightfieldTexture(timeIndex) {
  const data = timeSeriesData[timeIndex];
  const size = GRID;
  const pixels = new Float32Array(size * size);
  for (let i = 0; i < size * size; i++) {
    pixels[i] = data.height[i] * ELEVATION_SCALE;
  }
  const texture = new THREE.DataTexture(pixels, size, size, THREE.RedFormat, THREE.FloatType);
  texture.needsUpdate = true;
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  texture.wrapS = THREE.ClampToEdgeWrapping;
  texture.wrapT = THREE.ClampToEdgeWrapping;
  texture.colorSpace = THREE.NoColorSpace;
  return texture;
}
function updateParticleHeightfield(timeIndex) {
  if (particleHeightTexture) {
    particleHeightTexture.dispose();
  }
  particleHeightTexture = createHeightfieldTexture(timeIndex);
  if (particleSystem) {
    particleSystem.material.uniforms.heightMap.value = particleHeightTexture;
  }
}
function initParticles() {
  const count = PARTICLE_COUNT;
  // Initial random positions spread across terrain
  const positions = new Float32Array(count * 3);
  const offsets = new Float32Array(count * 2); // Random offsets for variety
  const speeds = new Float32Array(count); // Per-particle speed
  for (let i = 0; i < count; i++) {
    positions[i * 3] = Math.random() * TERRAIN_SIZE;
    positions[i * 3 + 1] = 0; // Will be set by vertex shader
    positions[i * 3 + 2] = Math.random() * TERRAIN_SIZE;
    offsets[i * 2] = Math.random() * 100;
    offsets[i * 2 + 1] = Math.random() * 100;
    speeds[i] = 0.3 + Math.random() * 1.2;
  }
  particlePositionsArray = positions;
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('offset', new THREE.BufferAttribute(offsets, 2));
  geom.setAttribute('speed', new THREE.BufferAttribute(speeds, 1));
  const heightTex = particleHeightTexture || createHeightfieldTexture(0);
  particleHeightTexture = heightTex;
  // Custom ShaderMaterial: vertex shader samples heightfield to set Y
  const material = new THREE.ShaderMaterial({
    uniforms: {
      heightMap: { value: heightTex },
      gridSize: { value: GRID },
      terrainSize: { value: TERRAIN_SIZE },
      time: { value: 0 },
      elevationScale: { value: ELEVATION_SCALE },
    },
    vertexShader: /* glsl */ `
      attribute vec2 offset;
      attribute float speed;
      uniform sampler2D heightMap;
      uniform float gridSize;
      uniform float terrainSize;
      uniform float time;
      uniform float elevationScale;
      varying float vAlpha;
      void main() {
        // Wrap XZ position with per-particle drift over time
        float driftSpeed = speed * 0.3;
        float px = mod(position.x + offset.x + time * driftSpeed * 0.7, terrainSize);
        float pz = mod(position.z + offset.y + time * driftSpeed * 0.5, terrainSize);
        // Sample heightfield texture for Y elevation
        float u = px / terrainSize;
        float v = pz / terrainSize;
        float h = texture2D(heightMap, vec2(u, v)).r;
        vec3 worldPos = vec3(px, h + 0.35, pz);
        vec4 mvPosition = modelViewMatrix * vec4(worldPos, 1.0);
        gl_Position = projectionMatrix * mvPosition;
        // Fade particles near texture edges (wrapping seam)
        float edgeDist = min(min(px, terrainSize - px), min(pz, terrainSize - pz));
        vAlpha = smoothstep(0.0, 3.0, edgeDist) * 0.85;
        gl_PointSize = (80.0 / -mvPosition.z) * (1.5 + speed * 0.8);
        gl_PointSize = clamp(gl_PointSize, 1.5, 8.0);
      }
    `,
    fragmentShader: /* glsl */ `
      varying float vAlpha;
      void main() {
        // Soft circular particle with warm glow
        float d = length(gl_PointCoord - 0.5) * 2.0;
        float alpha = 1.0 - smoothstep(0.3, 1.0, d);
        alpha *= vAlpha;
        vec3 color = mix(vec3(1.0, 0.55, 0.1), vec3(1.0, 0.85, 0.3), 1.0 - d);
        gl_FragColor = vec4(color, alpha);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  particleSystem = new THREE.Points(geom, material);
  particleSystem.renderOrder = 2;
  scene.add(particleSystem);
}
/* ========================================================================
   WORLD-TO-GRID TRANSFORM — memoized per frame
   ======================================================================== */
let worldToGridFrameId = -1;
const worldToGridMemo = new Map();
function worldToGrid(worldX, worldZ, frameId) {
  // Invalidate memo each new frame
  if (frameId !== worldToGridFrameId) {
    worldToGridMemo.clear();
    worldToGridFrameId = frameId;
  }
  const key = `${worldX.toFixed(2)}|${worldZ.toFixed(2)}`;
  if (worldToGridMemo.has(key)) {
    cacheStats.transform.hits++;
    return worldToGridMemo.get(key);
  }
  cacheStats.transform.misses++;
  const ix = Math.round(worldX / GRID_SPACING);
  const iz = Math.round(worldZ / GRID_SPACING);
  const result = {
    ix: Math.max(0, Math.min(GRID - 1, ix)),
    iz: Math.max(0, Math.min(GRID - 1, iz)),
  };
  worldToGridMemo.set(key, result);
  return result;
}
/* ========================================================================
   TOOLTIP / HOVER — uses worldToGrid memo, checks against active data
   ======================================================================== */
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let tooltipTimeout = null;
function updateTooltip(event, frameId) {
  if (!activeTerrainMesh || !activeTerrainGeom) {
    dom.tooltip.style.display = 'none';
    return;
  }
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(activeTerrainMesh);
  if (intersects.length === 0) {
    dom.tooltip.style.display = 'none';
    return;
  }
  const point = intersects[0].point;
  const grid = worldToGrid(point.x, point.z, frameId);
  const data = timeSeriesData[activeTimeIndex];
  if (!data) return;
  const idx = grid.iz * GRID + grid.ix;
  const h = data.height[idx];
  const veg = data.vegetation[idx];
  const err = data.error[idx];
  // Verify tooltip data matches visual elevation — state synchronization check
  const visualElevation = point.y;
  const dataElevation = h * ELEVATION_SCALE;
  const syncOk = Math.abs(visualElevation - dataElevation) < 0.5;
  dom.tooltip.style.display = 'block';
  dom.tooltip.style.left = (event.clientX + 18) + 'px';
  dom.tooltip.style.top = (event.clientY - 10) + 'px';
  dom.tooltip.innerHTML =
    `Grid (${grid.ix}, ${grid.iz})` +
    `<br>Elev: ${(h * ELEVATION_SCALE).toFixed(2)} ${syncOk ? '' : '⚠'}` +
    `<br>Users: ${(veg * 100).toFixed(1)}%` +
    `<br>Errors: ${(err * 100).toFixed(1)}%`;
}
/* ========================================================================
   METRICS UPDATE
   ======================================================================== */
function updateMetrics(timeIndex) {
  const s = timeSeriesData[timeIndex].summary;
  dom.metRev.textContent = '$' + s.revenue.toFixed(1) + 'K';
  dom.metUsers.textContent = s.users.toFixed(1) + '%';
  dom.metErr.textContent = s.errors.toFixed(2) + '%';
}
/* ========================================================================
   DIAGNOSTICS UPDATE
   ======================================================================== */
const fpsCounter = { frames: 0, lastTime: performance.now(), fps: 60 };
function updateDiagnostics() {
  fpsCounter.frames++;
  const now = performance.now();
  if (now - fpsCounter.lastTime >= 1000) {
    fpsCounter.fps = Math.round(fpsCounter.frames / ((now - fpsCounter.lastTime) / 1000));
    fpsCounter.frames = 0;
    fpsCounter.lastTime = now;
  }
  dom.diagFps.textContent = fpsCounter.fps;
  dom.diagTerrain.textContent = `H:${cacheStats.terrain.hits} M:${cacheStats.terrain.misses}`;
  dom.diagRiver.textContent = `H:${cacheStats.river.hits} M:${cacheStats.river.misses}`;
  dom.diagTransform.textContent = `H:${cacheStats.transform.hits} M:${cacheStats.transform.misses}`;
  dom.diagParticles.textContent = PARTICLE_COUNT;
}
/* ========================================================================
   TIME SLIDER — idempotent handler, guards against re-entry
   ======================================================================== */
let sliderChanging = false;
function onSliderChange() {
  // Idempotent guard: if already processing a change, skip
  if (sliderChanging) return;
  sliderChanging = true;
  const ti = parseInt(dom.slider.value, 10);
  dom.label.textContent = `T+${ti}`;
  applyTerrain(ti);
  sliderChanging = false;
}
/* ========================================================================
   EVENT BINDINGS
   ======================================================================== */
dom.slider.addEventListener('input', onSliderChange);
dom.slider.addEventListener('change', onSliderChange); // For snap on release
dom.btnAuto.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  dom.btnAuto.classList.toggle('active', controls.autoRotate);
});
dom.bookmarks.forEach(btn => {
  btn.addEventListener('click', () => {
    const view = btn.dataset.view;
    if (view) animateBookmark(view);
  });
});
// Tooltip: only track when OrbitControls is NOT being dragged
let isDragging = false;
renderer.domElement.addEventListener('pointerdown', () => {
  // OrbitControls handles its own drag state internally;
  // we track a short grace period after pointer up
  isDragging = true;
});
renderer.domElement.addEventListener('pointerup', () => {
  // Delay clearing drag flag so a quick click doesn't flash tooltip
  setTimeout(() => { isDragging = false; }, 80);
});
window.addEventListener('pointermove', (event) => {
  if (isDragging) {
    dom.tooltip.style.display = 'none';
    return;
  }
  if (tooltipTimeout) cancelAnimationFrame(tooltipTimeout);
  tooltipTimeout = requestAnimationFrame(() => {
    updateTooltip(event, worldToGridFrameId + 1);
  });
});
// Import data
dom.btnImport.addEventListener('click', () => {
  dom.fileDrop.classList.toggle('visible');
});
dom.fileInput.addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const raw = JSON.parse(e.target.result);
      if (raw.timeSeries && Array.isArray(raw.timeSeries) && raw.timeSeries.length > 0) {
        // Validate and convert imported data
        const steps = Math.min(raw.timeSeries.length, 200);
        const newData = [];
        for (let t = 0; t < steps; t++) {
          const src = raw.timeSeries[t];
          const frame = {
            height: new Float32Array(GRID * GRID),
            vegetation: new Float32Array(GRID * GRID),
            error: new Float32Array(GRID * GRID),
            apiCalls: [],
            summary: { revenue: 0, users: 0, errors: 0 },
          };
          // If imported data has grid arrays, use them; otherwise generate from summary
          if (src.height && src.height.length === GRID * GRID) {
            frame.height.set(src.height);
            frame.vegetation.set(src.vegetation || src.height.map(v => v / 6));
            frame.error.set(src.error || new Float32Array(GRID * GRID).fill(0.05));
          } else {
            // Generate terrain from summary values
            const revFactor = (src.revenue || 50) / 50;
            const userFactor = (src.users || 50) / 50;
            for (let i = 0; i < GRID * GRID; i++) {
              const iz = Math.floor(i / GRID);
              const ix = i % GRID;
              const d = Math.sqrt((ix - 30) ** 2 + (iz - 30) ** 2);
              frame.height[i] = revFactor * 4 * Math.exp(-d * 0.03);
              frame.vegetation[i] = userFactor * Math.exp(-d * 0.04);
              frame.error[i] = (1 - frame.vegetation[i]) * 0.3;
            }
          }
          frame.summary.revenue = src.revenue || 0;
          frame.summary.users = src.users || 0;
          frame.summary.errors = src.errors || 0;
          frame.apiCalls = src.apiCalls || [];
          newData.push(frame);
        }
        // Clear caches and replace data
        terrainCache.forEach(g => g.dispose());
        terrainCache.clear();
        riverCache.forEach(g => { if (g) g.dispose(); });
        riverCache.clear();
        timeSeriesData = newData;
        dom.slider.max = newData.length - 1;
        dom.slider.value = 0;
        activeTimeIndex = -1;
        if (activeRiverGroup) {
          activeRiverGroup.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); });
          scene.remove(activeRiverGroup);
          activeRiverGroup = null;
        }
        applyTerrain(0);
        dom.fileDrop.classList.remove('visible');
      }
    } catch (err) {
      console.warn('Import failed:', err.message);
      alert('Import error: ' + err.message);
    }
  };
  reader.readAsText(file);
});
// Window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ========================================================================
   RENDER LOOP
   ======================================================================== */
const clock = new THREE.Clock();
let frameId = 0;
function animate() {
  requestAnimationFrame(animate);
  frameId++;
  controls.update();
  // Bookmark animation
  if (bookmarkAnimating && bookmarkFrom && bookmarkTo) {
    bookmarkProgress += clock.getDelta() / BOOKMARK_DURATION;
    if (bookmarkProgress >= 1.0) {
      bookmarkProgress = 1.0;
      bookmarkAnimating = false;
    }
    const t = bookmarkProgress;
    // Ease in-out
    const ease = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
    camera.position.lerpVectors(bookmarkFrom.position, bookmarkTo.position, ease);
    controls.target.lerpVectors(bookmarkFrom.target, bookmarkTo.target, ease);
  }
  // Update particle shader time uniform (drives drift animation)
  if (particleSystem) {
    particleSystem.material.uniforms.time.value = performance.now() * 0.001;
  }
  // Update diagnostics every 30 frames (not every frame)
  if (frameId % 30 === 0) {
    updateDiagnostics();
  }
  renderer.render(scene, camera);
}
/* ========================================================================
   INITIALIZATION
   ======================================================================== */
function init() {
  // Create initial heightfield texture for particles
  particleHeightTexture = createHeightfieldTexture(0);
  // Apply initial terrain (time index 0)
  applyTerrain(0);
  // Initialize particle system
  initParticles();
  // Set slider range
  dom.slider.max = TIME_STEPS - 1;
  dom.slider.value = 0;
  dom.label.textContent = 'T+0';
  // Start render loop
  animate();
}
init();
/* ========================================================================
   EDGE CASE VALIDATION CHECKLIST (run at init and on import)
   ======================================================================== */
function validateState() {
  const issues = [];
  // Check all DOM refs resolved
  for (const [key, el] of Object.entries(dom)) {
    if (el === null || (el instanceof NodeList && el.length === 0)) {
      issues.push(`DOM ref '${key}' unresolved`);
    }
  }
  // Check data integrity
  if (!timeSeriesData || timeSeriesData.length === 0) issues.push('timeSeriesData empty');
  if (timeSeriesData.length > 0) {
    const f0 = timeSeriesData[0];
    if (!f0.height || f0.height.length !== GRID * GRID) issues.push('height array mismatch');
    if (!f0.vegetation || f0.vegetation.length !== GRID * GRID) issues.push('vegetation array mismatch');
    if (!f0.error || f0.error.length !== GRID * GRID) issues.push('error array mismatch');
  }
  // Check Three.js objects
  if (!renderer) issues.push('renderer missing');
  if (!scene) issues.push('scene missing');
  if (!camera) issues.push('camera missing');
  if (!controls) issues.push('controls missing');
  if (issues.length > 0) {
    console.warn('State validation issues:', issues);
  }
  return issues.length === 0;
}
// Validate after a short delay to let Three.js settle
setTimeout(validateState, 500);
console.log('3D Data Terrain Explorer ready — cache stats in top-right panel');
</script>
</body>
</html>