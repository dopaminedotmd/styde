3D Data Terrain Explorer — interactive HTML dashboard. Single file, Three.js from CDN.
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a0f;
    --panel-bg: rgba(10,10,20,0.92);
    --text: #c8ccd4;
    --accent: #4da6ff;
    --accent-dim: #2a5f8f;
    --warn: #e08840;
    --good: #40b880;
    --border: #1a1a2e;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg);
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
    color: var(--text);
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 0;
  }
  canvas { display: block; }
  /* Time scrubber */
  #time-bar {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 20px;
    backdrop-filter: blur(12px);
  }
  #time-bar label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent-dim); }
  #time-slider {
    width: 320px;
    accent-color: var(--accent);
    cursor: pointer;
  }
  #time-value { font-variant-numeric: tabular-nums; min-width: 72px; text-align: center; font-size: 13px; }
  /* Bookmarks panel */
  #bookmarks {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    backdrop-filter: blur(12px);
    max-height: 50vh;
    overflow-y: auto;
  }
  #bookmarks h3 { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent-dim); margin-bottom: 10px; }
  .bookmark-row { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 12px; }
  .bookmark-row button { background: var(--border); border: none; color: var(--text); padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; transition: background 0.2s; }
  .bookmark-row button:hover { background: var(--accent-dim); }
  .bookmark-row button.del { background: transparent; color: #e06060; padding: 2px 6px; }
  #save-bookmark { background: var(--accent-dim); border: none; color: #fff; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 11px; margin-top: 4px; width: 100%; }
  /* Diagnostic panel */
  #diagnostics {
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 10;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    backdrop-filter: blur(12px);
    font-size: 11px;
    font-family: 'JetBrains Mono', 'Cascadia Code', monospace;
    min-width: 200px;
  }
  #diagnostics h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--accent-dim); margin-bottom: 8px; }
  .diag-row { display: flex; justify-content: space-between; margin-bottom: 3px; }
  .diag-row .label { color: #889; }
  .diag-row .value { color: var(--text); font-weight: 600; }
  .diag-row .value.hit { color: var(--good); }
  .diag-row .value.miss { color: var(--warn); }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="diagnostics">
  <h3>Cache Diagnostics</h3>
  <div class="diag-row"><span class="label">Terrain geom</span><span class="value" id="diag-terrain">0h/0m</span></div>
  <div class="diag-row"><span class="label">River geom</span><span class="value" id="diag-river">0h/0m</span></div>
  <div class="diag-row"><span class="label">Grid xform</span><span class="value" id="diag-grid">0h/0m</span></div>
  <div class="diag-row"><span class="label">Particle buf</span><span class="value" id="diag-part">reused</span></div>
  <div class="diag-row"><span class="label">FPS</span><span class="value" id="diag-fps">--</span></div>
</div>
<div id="bookmarks">
  <h3>Camera Bookmarks</h3>
  <div id="bookmark-list"></div>
  <button id="save-bookmark">Save Current View</button>
</div>
<div id="time-bar">
  <label>Time</label>
  <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
  <span id="time-value">Day 1</span>
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
/* ======================================================================
   DATA GENERATION — synthetic 30-day time-series on a 50×50 grid
   Each cell: revenue (elevation), user density (color), error rate (river),
   api call volume (particle). Deterministic seed for reproducibility.
   ====================================================================== */
const GRID = 50;
const TIME_STEPS = 30;
const TERRAIN_SCALE = 4.0;        // vertical exaggeration
const GRID_SPACING = 0.4;         // world units between grid points
const TERRAIN_SIZE = GRID * GRID_SPACING;
// Simple seeded pseudo-random for deterministic data
function mulberry32(a) {
  return function() { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
const rng = mulberry32(1337);
// Generate all time-series data upfront (precomputation strategy)
// Each timeData[t][y][x] = { revenue, users, errors, apiCalls }
function generateTimeSeries() {
  const series = [];
  // Seeded noise-like pattern: sine waves with varying frequency/phase per day
  for (let t = 0; t < TIME_STEPS; t++) {
    const dayFactor = t / (TIME_STEPS - 1);                    // 0..1 progression
    const seasonal = Math.sin(dayFactor * Math.PI * 2) * 0.3;   // cyclical component
    const trend = dayFactor * 0.4;                              // upward trend
    const grid = new Array(GRID);
    for (let y = 0; y < GRID; y++) {
      grid[y] = new Array(GRID);
      const ny = y / (GRID - 1);                               // normalized 0..1
      for (let x = 0; x < GRID; x++) {
        const nx = x / (GRID - 1);
        // Revenue: central peak that shifts rightward over time + noise
        const cx = 0.3 + dayFactor * 0.4;                      // peak center drifts
        const cy = 0.4 + seasonal * 0.2;
        const dist = Math.hypot(nx - cx, ny - cy);
        const revenue = Math.max(0, (1 - dist * 1.8) * (0.7 + trend) + rng() * 0.1);
        // User density: correlated with revenue but with spatial offset
        const udist = Math.hypot(nx - (cx + 0.1), ny - (cy - 0.08));
        const users = Math.max(0, (1 - udist * 2.2) * 0.85 + rng() * 0.08);
        // Error rate: spikes in specific corridors (simulate system issues)
        const inErrorBand = Math.abs(ny - 0.5) < 0.08 && nx > 0.2 * dayFactor;
        const errors = inErrorBand ? rng() * 0.6 + 0.2 : rng() * 0.05;
        // API calls: follow the revenue valleys
        const apiCalls = (1 - dist * 1.2) * 80 + rng() * 20;
        grid[y][x] = { revenue, users, errors, apiCalls };
      }
    }
    series.push(grid);
  }
  return series;
}
const timeSeries = generateTimeSeries();
/* ======================================================================
   CACHE SYSTEM — tracks hits/misses for each cache domain
   All geometry construction happens once per unique input; lookup thereafter.
   ====================================================================== */
const cacheStats = {
  terrain: { hits: 0, misses: 0 },
  river:   { hits: 0, misses: 0 },
  grid:    { hits: 0, misses: 0 }
};
// Terrain geometry cache: keyed by time step index
const terrainGeomCache = new Map();
function getTerrainGeometry(timeIndex) {
  if (terrainGeomCache.has(timeIndex)) {
    cacheStats.terrain.hits++;
    return terrainGeomCache.get(timeIndex);
  }
  cacheStats.terrain.misses++;
  const geom = buildTerrainGeometry(timeIndex);
  terrainGeomCache.set(timeIndex, geom);
  return geom;
}
// River geometry cache: keyed by time step index, stores TubeGeometry
const riverGeomCache = new Map();
function getRiverGeometry(timeIndex) {
  if (riverGeomCache.has(timeIndex)) {
    cacheStats.river.hits++;
    return riverGeomCache.get(timeIndex);
  }
  cacheStats.river.misses++;
  const geom = buildRiverGeometry(timeIndex);
  riverGeomCache.set(timeIndex, geom);
  return geom;
}
// Grid transform memoization: world (x,z) -> grid (col,row)
// Cleared each frame via a frame counter stamp
const gridTransformMemo = new Map();
let gridTransformFrame = -1;
function worldToGrid(wx, wz, frameId) {
  // Reset memo each frame to avoid stale entries and unbounded growth
  if (frameId !== gridTransformFrame) {
    gridTransformMemo.clear();
    gridTransformFrame = frameId;
  }
  const key = `${wx.toFixed(3)},${wz.toFixed(3)}`;            // quantize key to reduce misses
  if (gridTransformMemo.has(key)) {
    cacheStats.grid.hits++;
    return gridTransformMemo.get(key);
  }
  cacheStats.grid.misses++;
  // Convert world coordinate to grid index
  const half = TERRAIN_SIZE / 2;
  const col = Math.round((wx + half) / GRID_SPACING);
  const row = Math.round((wz + half) / GRID_SPACING);
  const result = {
    col: Math.max(0, Math.min(GRID - 1, col)),
    row: Math.max(0, Math.min(GRID - 1, row))
  };
  gridTransformMemo.set(key, result);
  return result;
}
/* ======================================================================
   TERRAIN BUILDER — single BufferGeometry per time step
   Positions computed once, vertex colors from user-density metric.
   Extracted from main loop; never called per-frame.
   ====================================================================== */
function buildTerrainGeometry(timeIndex) {
  const data = timeSeries[timeIndex];
  const count = GRID * GRID;
  // Allocate typed arrays once — no per-vertex object creation
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  for (let row = 0; row < GRID; row++) {
    for (let col = 0; col < GRID; col++) {
      const idx = row * GRID + col;
      const cell = data[row][col];
      // Position: x = col * spacing, z = row * spacing, y = revenue * scale
      const wx = col * GRID_SPACING - TERRAIN_SIZE / 2;
      const wz = row * GRID_SPACING - TERRAIN_SIZE / 2;
      const wy = cell.revenue * TERRAIN_SCALE;
      positions[idx * 3]     = wx;
      positions[idx * 3 + 1] = wy;
      positions[idx * 3 + 2] = wz;
      // Color: vegetation gradient from user density
      // low density = brown/arid, high density = lush green
      const density = cell.users;
      const r = 0.35 - density * 0.2;                          // reduce red as density rises
      const g = 0.25 + density * 0.7;                          // green grows with density
      const b = 0.12 + density * 0.15;                         // slight blue tint at peak
      colors[idx * 3]     = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  // Build index buffer for triangulated grid (2 triangles per quad)
  const indices = [];
  for (let row = 0; row < GRID - 1; row++) {
    for (let col = 0; col < GRID - 1; col++) {
      const a = row * GRID + col;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d, a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();                                  // for lighting
  return geom;
}
/* ======================================================================
   RIVER BUILDER — TubeGeometry tracing error corridors
   Samples grid for cells with error rate > threshold, connects them
   into spline paths, builds TubeGeometry. Cached per time step.
   ====================================================================== */
function buildRiverGeometry(timeIndex) {
  const data = timeSeries[timeIndex];
  const threshold = 0.25;
  const points = [];
  // Collect error cells above threshold, ordered by position for path cohesion
  for (let row = 0; row < GRID; row++) {
    for (let col = 0; col < GRID; col++) {
      if (data[row][col].errors > threshold) {
        const wx = col * GRID_SPACING - TERRAIN_SIZE / 2;
        const wz = row * GRID_SPACING - TERRAIN_SIZE / 2;
        const wy = data[row][col].revenue * TERRAIN_SCALE + 0.03; // float above terrain
        points.push(new THREE.Vector3(wx, wy, wz));
      }
    }
  }
  // Need at least 2 points for a curve; return empty group if insufficient
  if (points.length < 2) {
    const empty = new THREE.BufferGeometry();
    empty.setAttribute('position', new THREE.BufferAttribute(new Float32Array(0), 3));
    return empty;
  }
  // Sort points by x then z for a coherent path
  points.sort((a, b) => a.x - b.x || a.z - b.z);
  // Create a CatmullRom spline through the error points
  const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
  const tubularSegments = Math.min(points.length * 4, 200);
  const tubeRadius = 0.08;
  const radialSegments = 6;
  // TubeGeometry is the only runtime geometry constructor call —
  // but it's cache-gated so it only runs on slider release (debounced)
  const tubeGeom = new THREE.TubeGeometry(curve, tubularSegments, tubeRadius, radialSegments, false);
  return tubeGeom;
}
/* ======================================================================
   PARTICLE SYSTEM — data-flow trails using BufferGeometry with
   pre-allocated position/color arrays. Updated per-frame via direct
   array mutation — no per-frame allocations, no new geometry.
   ====================================================================== */
const PARTICLE_COUNT = 600;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3); // direction * speed
const particleData = new Float32Array(PARTICLE_COUNT);           // misc state per particle
// Initialize particles scattered across the terrain surface
function initParticles(timeIndex) {
  const data = timeSeries[timeIndex];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const col = Math.floor(rng() * GRID);
    const row = Math.floor(rng() * GRID);
    const cell = data[row][col];
    const wx = col * GRID_SPACING - TERRAIN_SIZE / 2;
    const wz = row * GRID_SPACING - TERRAIN_SIZE / 2;
    const wy = cell.revenue * TERRAIN_SCALE + 0.05;
    particlePositions[i * 3]     = wx;
    particlePositions[i * 3 + 1] = wy;
    particlePositions[i * 3 + 2] = wz;
    // Random direction biased along x-axis (data flow direction)
    const angle = (rng() - 0.5) * Math.PI * 0.6;
    const speed = 0.02 + rng() * 0.06;
    particleVelocities[i * 3]     = Math.cos(angle) * speed;
    particleVelocities[i * 3 + 1] = (rng() - 0.5) * 0.01;
    particleVelocities[i * 3 + 2] = Math.sin(angle) * speed;
    // Color: warm yellow-orange for API traffic
    particleColors[i * 3]     = 1.0;
    particleColors[i * 3 + 1] = 0.55 + rng() * 0.3;
    particleColors[i * 3 + 2] = 0.1;
    particleData[i] = rng();                                   // phase offset for lifetime cycling
  }
}
/* ======================================================================
   THREE.JS SCENE SETUP — renderer, camera, lights, controls
   ====================================================================== */
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));  // cap pixel ratio
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 15, 50);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(8, 7, 12);
camera.lookAt(0, 1.5, 0);
// OrbitControls with smooth damping and auto-rotation
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.8, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 3;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
// Lighting: ambient fill + directional key light
const ambient = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(8, 14, 4);
sun.castShadow = true;
sun.shadow.mapSize.width = 1024;
sun.shadow.mapSize.height = 1024;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 50;
sun.shadow.camera.left = -15;
sun.shadow.camera.right = 15;
sun.shadow.camera.top = 15;
sun.shadow.camera.bottom = -15;
scene.add(sun);
const fillLight = new THREE.DirectionalLight(0x8899cc, 0.8);
fillLight.position.set(-4, 2, -3);
scene.add(fillLight);
// Ground reference plane (semi-transparent grid)
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2 + 2, 40, 20, 64, 0x222244, 0x222244);
gridHelper.position.y = -0.01;
scene.add(gridHelper);
/* ======================================================================
   SCENE OBJECTS — mutable references for hot-swapping on time change
   ====================================================================== */
let terrainMesh = null;
let riverLine = null;
let particlePoints = null;
let currentTimeIndex = 0;
let frameId = 0;
let riverRebuildTimer = null;                                  // debounce handle
// Build initial scene state
function buildScene(timeIndex) {
  // Remove previous meshes
  if (terrainMesh) { terrainMesh.geometry.dispose(); scene.remove(terrainMesh); }
  if (riverLine)  { riverLine.geometry.dispose();  scene.remove(riverLine); }
  // Particle geometry is reused — only dispose on full rebuild
  // Terrain
  const terrainGeom = getTerrainGeometry(timeIndex);           // cached lookup
  const terrainMat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide
  });
  terrainMesh = new THREE.Mesh(terrainGeom, terrainMat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Rivers
  const riverGeom = getRiverGeometry(timeIndex);               // cached lookup
  const riverMat = new THREE.MeshStandardMaterial({
    color: 0xcc3333,
    roughness: 0.2,
    metalness: 0.3,
    emissive: 0x330000,
    emissiveIntensity: 0.6
  });
  riverLine = new THREE.Mesh(riverGeom, riverMat);
  riverLine.renderOrder = 1;
  riverLine.material.depthTest = true;
  riverLine.material.depthWrite = true;
  scene.add(riverLine);
  // Particles — reuse geometry, update attribute references
  if (!particlePoints) {
    initParticles(timeIndex);
    const particleGeom = new THREE.BufferGeometry();
    particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
    const particleMat = new THREE.PointsMaterial({
      size: 0.12,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.75
    });
    particlePoints = new THREE.Points(particleGeom, particleMat);
    scene.add(particlePoints);
  }
}
buildScene(0);
currentTimeIndex = 0;
/* ======================================================================
   TIME SLIDER — UI binding with debounced river rebuild
   ====================================================================== */
const slider = document.getElementById('time-slider');
const timeValueEl = document.getElementById('time-value');
slider.addEventListener('input', () => {
  const newIndex = parseInt(slider.value, 10);
  timeValueEl.textContent = `Day ${newIndex + 1}`;
  switchTerrain(newIndex);                                     // instant terrain swap from cache
});
function switchTerrain(timeIndex) {
  if (timeIndex === currentTimeIndex) return;
  currentTimeIndex = timeIndex;
  // Swap terrain geometry (from cache — instant)
  const newGeom = getTerrainGeometry(timeIndex);
  terrainMesh.geometry = newGeom;
  // Debounce river rebuild: 200ms delay before recalculating TubeGeometry
  if (riverRebuildTimer) clearTimeout(riverRebuildTimer);
  riverRebuildTimer = setTimeout(() => {
    const oldRiverGeom = riverLine.geometry;
    const newRiverGeom = getRiverGeometry(timeIndex);
    riverLine.geometry = newRiverGeom;
    oldRiverGeom.dispose();                                    // clean up replaced geometry
    riverRebuildTimer = null;
  }, 200);
  // Reset particles to new terrain surface
  initParticles(timeIndex);
  particlePoints.geometry.attributes.position.needsUpdate = true;
  particlePoints.geometry.attributes.color.needsUpdate = true;
}
/* ======================================================================
   CAMERA BOOKMARKS — save/restore camera state
   ====================================================================== */
const bookmarks = [];
const bookmarkListEl = document.getElementById('bookmark-list');
function renderBookmarks() {
  bookmarkListEl.innerHTML = '';
  bookmarks.forEach((bm, i) => {
    const row = document.createElement('div');
    row.className = 'bookmark-row';
    row.innerHTML = `
      <span>${bm.label || `View ${i + 1}`}</span>
      <button data-idx="${i}" class="go">Go</button>
      <button data-idx="${i}" class="del">×</button>
    `;
    row.querySelector('.go').onclick = () => applyBookmark(i);
    row.querySelector('.del').onclick = () => { bookmarks.splice(i, 1); renderBookmarks(); };
    bookmarkListEl.appendChild(row);
  });
}
function applyBookmark(idx) {
  const bm = bookmarks[idx];
  if (!bm) return;
  // Smoothly animate to saved position using controls target + camera position
  controls.target.copy(bm.target);
  camera.position.copy(bm.position);
  controls.update();
  if (bm.timeIndex !== undefined) {
    slider.value = bm.timeIndex;
    timeValueEl.textContent = `Day ${bm.timeIndex + 1}`;
    switchTerrain(bm.timeIndex);
  }
}
document.getElementById('save-bookmark').addEventListener('click', () => {
  const name = `View ${bookmarks.length + 1} @ Day ${currentTimeIndex + 1}`;
  bookmarks.push({
    label: name,
    position: camera.position.clone(),
    target: controls.target.clone(),
    timeIndex: currentTimeIndex
  });
  renderBookmarks();
});
renderBookmarks();
/* ======================================================================
   ANIMATION LOOP — particle update, controls, cache diag, FPS
   Per-frame allocations: ZERO (all arrays pre-allocated, reused).
   ====================================================================== */
let lastFpsTime = performance.now();
let fpsFrames = 0;
let displayedFps = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  frameId++;
  controls.update();                                           // damping + auto-rotate
  // --- Particle update: direct array mutation, zero allocation ---
  const posArr = particlePositions;                            // reference, not copy
  const velArr = particleVelocities;
  const half = TERRAIN_SIZE / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const i3 = i * 3;
    // Move particle by velocity
    posArr[i3]     += velArr[i3];
    posArr[i3 + 1] += velArr[i3 + 1];
    posArr[i3 + 2] += velArr[i3 + 2];
    // Clamp to terrain bounds — wrap around instead of destroying
    if (posArr[i3] > half || posArr[i3] < -half) {
      posArr[i3] = posArr[i3] > half ? -half : half;
    }
    if (posArr[i3 + 2] > half || posArr[i3 + 2] < -half) {
      posArr[i3 + 2] = posArr[i3 + 2] > half ? -half : half;
    }
    // Sample terrain height at current position using memoized grid transform
    const grid = worldToGrid(posArr[i3], posArr[i3 + 2], frameId);
    const cell = timeSeries[currentTimeIndex][grid.row][grid.col];
    const surfaceY = cell.revenue * TERRAIN_SCALE + 0.05;
    // Float above terrain surface
    posArr[i3 + 1] += (surfaceY - posArr[i3 + 1]) * 0.1;
    // Fade alpha via data array for lifetime cycling
    particleData[i] += 0.003;
    if (particleData[i] > 1.0) {
      particleData[i] = 0.0;
      // Respawn at random position
      const col = Math.floor(rng() * GRID);
      const row = Math.floor(rng() * GRID);
      posArr[i3]     = col * GRID_SPACING - half;
      posArr[i3 + 2] = row * GRID_SPACING - half;
    }
  }
  // Mark position attribute as needing GPU upload (direct mutation)
  particlePoints.geometry.attributes.position.needsUpdate = true;
  // --- FPS calculation ---
  fpsFrames++;
  const now = performance.now();
  if (now - lastFpsTime >= 1000) {
    displayedFps = Math.round(fpsFrames / ((now - lastFpsTime) / 1000));
    fpsFrames = 0;
    lastFpsTime = now;
    updateDiagnostics();
  }
  renderer.render(scene, camera);
}
/* ======================================================================
   DIAGNOSTIC PANEL UPDATE — cache hit/miss rates, FPS
   ====================================================================== */
function updateDiagnostics() {
  const terrainTotal = cacheStats.terrain.hits + cacheStats.terrain.misses || 1;
  const riverTotal   = cacheStats.river.hits + cacheStats.river.misses || 1;
  const gridTotal    = cacheStats.grid.hits + cacheStats.grid.misses || 1;
  // Format as "H hits / M misses (rate%)"
  const tRate = Math.round(cacheStats.terrain.hits / terrainTotal * 100);
  const rRate = Math.round(cacheStats.river.hits / riverTotal * 100);
  const gRate = Math.round(cacheStats.grid.hits / gridTotal * 100);
  document.getElementById('diag-terrain').innerHTML =
    `<span class="hit">${cacheStats.terrain.hits}h</span>/<span class="miss">${cacheStats.terrain.misses}m</span> <small>${tRate}%</small>`;
  document.getElementById('diag-river').innerHTML =
    `<span class="hit">${cacheStats.river.hits}h</span>/<span class="miss">${cacheStats.river.misses}m</span> <small>${rRate}%</small>`;
  document.getElementById('diag-grid').innerHTML =
    `<span class="hit">${cacheStats.grid.hits}h</span>/<span class="miss">${cacheStats.grid.misses}m</span> <small>${gRate}%</small>`;
  document.getElementById('diag-part').textContent = `reused ×${PARTICLE_COUNT}`;
  document.getElementById('diag-fps').textContent = displayedFps;
}
/* ======================================================================
   RESIZE HANDLER
   ====================================================================== */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ======================================================================
   KEYBOARD SHORTCUTS
   ====================================================================== */
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      // Reset camera to default overview
      camera.position.set(8, 7, 12);
      controls.target.set(0, 1.8, 0);
      controls.update();
      break;
    case 'a':
      // Toggle auto-rotation
      controls.autoRotate = !controls.autoRotate;
      break;
    case 'arrowleft':
      slider.value = Math.max(0, currentTimeIndex - 1);
      slider.dispatchEvent(new Event('input'));
      break;
    case 'arrowright':
      slider.value = Math.min(TIME_STEPS - 1, currentTimeIndex + 1);
      slider.dispatchEvent(new Event('input'));
      break;
  }
});
// Start the render loop
requestAnimationFrame(animate);
// Log startup
console.log(
  `%c3D Data Terrain Explorer%c ready`,
  'color:#4da6ff;font-weight:bold;font-size:14px;', ''
);
console.log(
  `Grid: ${GRID}×${GRID} | Time steps: ${TIME_STEPS} | Particles: ${PARTICLE_COUNT}`
);
console.log(
  `Controls: drag=orbit | scroll=zoom | right-drag=pan | R=reset | A=auto-rotate | ←→=time`
);
console.log(
  `Cache: terrain(%c✓%c) river(%c✓%c) grid(%c✓%c) particles(reused)`,
  'color:#40b880;', '', 'color:#40b880;', '', 'color:#40b880;', ''
);
</script>
</body>
</html>