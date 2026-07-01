<!--
3D Data Terrain Explorer v1.0
Blueprint: 3D Data Terrain Explorer (Domain: dashboard, Version: 1)
Persona: 3D data visualization engineer, Three.js specialist
Single self-contained HTML file. No build step. CDN Three.js via importmap.
-->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a0f; --panel-bg: rgba(10,10,20,0.92); --text: #c8c8d4; --accent: #4da6ff; --warn: #ff6b4a; --good: #3cc76a; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  canvas { display:block; }
  #ui { position:fixed; top:0; left:0; right:0; bottom:0; pointer-events:none; z-index:10; }
  #ui > * { pointer-events:auto; }
  #time-panel { position:absolute; bottom:24px; left:50%; transform:translateX(-50%); background:var(--panel-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px 20px; display:flex; gap:14px; align-items:center; backdrop-filter:blur(12px); }
  #time-panel label { font-size:12px; text-transform:uppercase; letter-spacing:0.6px; opacity:0.7; }
  #time-slider { width:240px; accent-color:var(--accent); }
  #time-value { font-variant-numeric:tabular-nums; min-width:48px; text-align:center; font-weight:600; }
  #bookmarks { position:absolute; top:16px; right:16px; background:var(--panel-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 14px; backdrop-filter:blur(12px); display:flex; flex-direction:column; gap:6px; min-width:160px; }
  #bookmarks h3 { font-size:11px; text-transform:uppercase; letter-spacing:0.8px; opacity:0.5; margin-bottom:2px; }
  .bm-btn { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); color:var(--text); padding:5px 10px; border-radius:6px; cursor:pointer; font-size:12px; transition:all 0.15s; text-align:left; display:flex; justify-content:space-between; }
  .bm-btn:hover { background:rgba(255,255,255,0.08); border-color:var(--accent); }
  .bm-save { color:var(--accent); cursor:pointer; font-size:11px; }
  .bm-del { color:var(--warn); cursor:pointer; font-size:11px; margin-left:6px; }
  #debug-panel { position:absolute; top:16px; left:16px; background:var(--panel-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:10px 14px; backdrop-filter:blur(12px); font-size:11px; font-variant-numeric:tabular-nums; display:flex; flex-direction:column; gap:3px; min-width:170px; }
  #debug-panel h3 { font-size:11px; text-transform:uppercase; letter-spacing:0.8px; opacity:0.5; margin-bottom:2px; }
  .debug-row { display:flex; justify-content:space-between; gap:12px; }
  .debug-row .label { opacity:0.55; }
  .debug-row .val.good { color:var(--good); }
  .debug-row .val.warn { color:var(--warn); }
  #legend { position:absolute; bottom:100px; left:16px; background:var(--panel-bg); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:8px 12px; backdrop-filter:blur(12px); font-size:10px; display:flex; gap:10px; align-items:center; }
  .legend-item { display:flex; align-items:center; gap:4px; }
  .legend-swatch { width:12px; height:12px; border-radius:3px; }
  #tooltip { position:fixed; pointer-events:none; background:var(--panel-bg); border:1px solid rgba(255,255,255,0.15); border-radius:8px; padding:6px 10px; font-size:11px; display:none; backdrop-filter:blur(12px); white-space:nowrap; }
</style>
</head>
<body>
<div id="ui">
  <div id="debug-panel">
    <h3>Cache Diagnostics</h3>
    <div class="debug-row"><span class="label">Terrain hits</span><span class="val good" id="db-terrain-hits">0</span></div>
    <div class="debug-row"><span class="label">Terrain misses</span><span class="val" id="db-terrain-misses">0</span></div>
    <div class="debug-row"><span class="label">River hits</span><span class="val good" id="db-river-hits">0</span></div>
    <div class="debug-row"><span class="label">River misses</span><span class="val" id="db-river-misses">0</span></div>
    <div class="debug-row"><span class="label">FPS</span><span class="val" id="db-fps">60</span></div>
    <div class="debug-row"><span class="label">Allocs/frame</span><span class="val good" id="db-allocs">0</span></div>
  </div>
  <div id="bookmarks">
    <h3>Camera Bookmarks</h3>
    <div id="bm-list"></div>
    <button class="bm-btn" id="bm-save-current">+ Save Current View</button>
  </div>
  <div id="time-panel">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
    <span id="time-value">T0</span>
  </div>
  <div id="legend">
    <span style="opacity:0.55;">Legend:</span>
    <div class="legend-item"><div class="legend-swatch" style="background:#3cc76a;"></div> Density↑</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#ff6b4a;"></div> Error River</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#ffcc44;"></div> API Trail</div>
  </div>
  <div id="tooltip"></div>
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
// ─── SYNTHETIC TIME-SERIES DATA ─────────────────────────────────────────
// 20 time steps, 64x64 grid. Each step: height (revenue), density (users), error (anomaly).
const GRID = 64;
const TIME_STEPS = 20;
const dataSeries = [];
// Deterministic seed for reproducibility
function seededRandom(seed) {
  let s = seed | 0;
  return () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
}
const rng = seededRandom(42);
// Pre-compute noise grid once, reuse for all time steps to avoid redundant work.
// Single 2D grid of simplex-like noise using stacked sine waves (deterministic).
const noiseGrid = new Float32Array(GRID * GRID);
for (let iy = 0; iy < GRID; iy++) {
  for (let ix = 0; ix < GRID; ix++) {
    const nx = ix / GRID, ny = iy / GRID;
    let v = 0;
    // 4-octave stacked sine — cheap, deterministic, visually interesting
    v += Math.sin(nx * 6.283 + ny * 4.712) * 0.5;
    v += Math.sin(nx * 12.566 - ny * 9.425) * 0.25;
    v += Math.sin(nx * 18.850 + ny * 15.708) * 0.125;
    v += Math.sin(nx * 25.133 - ny * 21.991) * 0.0625;
    noiseGrid[iy * GRID + ix] = v;
  }
}
// Generate all time steps: each step has height, density, error arrays
for (let t = 0; t < TIME_STEPS; t++) {
  const height = new Float32Array(GRID * GRID);
  const density = new Float32Array(GRID * GRID);
  const error = new Float32Array(GRID * GRID);
  const phase = t / TIME_STEPS; // 0..1 progress through time
  for (let i = 0; i < GRID * GRID; i++) {
    const n = noiseGrid[i];
    // Height = base terrain modulated by time (simulated revenue growth + fluctuation)
    height[i] = n * 2.5 + Math.sin(phase * Math.PI * 2 + n * 3) * 1.2 + phase * 1.5;
    // Density = secondary metric, peaks near center at mid-time
    const ix = i % GRID, iy = Math.floor(i / GRID);
    const cx = (ix / GRID - 0.5) * 2, cy = (iy / GRID - 0.5) * 2;
    const distFromCenter = Math.sqrt(cx * cx + cy * cy);
    density[i] = (1 - distFromCenter) * (0.5 + 0.5 * Math.sin(phase * Math.PI)) + rng() * 0.15;
    density[i] = Math.max(0, Math.min(1, density[i]));
    // Error = anomaly spikes at specific grid spots, grows mid-series then fades
    const anomalyHotspot = (Math.abs(cx - 0.3) < 0.12 && Math.abs(cy + 0.2) < 0.12) ? 1 : 0;
    error[i] = anomalyHotspot * (0.3 + 0.7 * Math.sin(phase * Math.PI)) + rng() * 0.03;
    error[i] = Math.max(0, Math.min(1, error[i]));
  }
  dataSeries.push({ height, density, error });
}
// ─── CACHE LAYER ────────────────────────────────────────────────────────
// All cacheable outputs stored here. Max 20 entries per cache type.
const MAX_CACHE = 20;
const terrainCache = new Map();   // key: timeIndex -> {geometry, material}
const riverCache = new Map();     // key: timeIndex -> THREE.Group (river meshes)
const worldToGridMemo = new Map(); // key: stringified position -> {ix, iy}  (max 200 entries, LRU)
const MEMO_MAX = 200;
const memoKeys = []; // LRU tracking
const cacheStats = {
  terrainHits: 0, terrainMisses: 0,
  riverHits: 0, riverMisses: 0,
};
// Allocations counter — incremented on any `new` call in hot paths. Reset per frame.
let allocsThisFrame = 0;
function trackAlloc() { allocsThisFrame++; }
// Wrap THREE constructors that touch hot paths
const _BufferGeometry = THREE.BufferGeometry;
THREE.BufferGeometry = function(...args) { trackAlloc(); return new _BufferGeometry(...args); };
const _Float32BufferAttribute = THREE.Float32BufferAttribute;
THREE.Float32BufferAttribute = function(...args) { trackAlloc(); return new _Float32BufferAttribute(...args); };
const _MeshStandardMaterial = THREE.MeshStandardMaterial;
THREE.MeshStandardMaterial = function(...args) { trackAlloc(); return new _MeshStandardMaterial(...args); };
function worldToGrid(wx, wz) {
  // Map world XZ (-GRID/2 .. GRID/2) to grid indices (0..GRID-1)
  // Memoize: same world position -> same result every time
  const key = `${wx.toFixed(2)},${wz.toFixed(2)}`;
  const cached = worldToGridMemo.get(key);
  if (cached) return cached;
  const half = GRID / 2;
  const ix = Math.round((wx + half - 0.5) * (GRID / (GRID)));
  const iy = Math.round((wz + half - 0.5) * (GRID / (GRID)));
  const result = {
    ix: Math.max(0, Math.min(GRID - 1, Math.floor((wx / (GRID * 0.1)) + GRID / 2))),
    iy: Math.max(0, Math.min(GRID - 1, Math.floor((wz / (GRID * 0.1)) + GRID / 2))),
  };
  // Proper world-to-grid: terrain spans from -GRID/2 to +GRID/2 in XZ, scaled by cellSize
  const cellSize = 0.1;
  const gx = Math.floor((wx / cellSize) + GRID / 2);
  const gy = Math.floor((wz / cellSize) + GRID / 2);
  const gridX = Math.max(0, Math.min(GRID - 1, gx));
  const gridY = Math.max(0, Math.min(GRID - 1, gy));
  const final = { ix: gridX, iy: gridY };
  // LRU eviction
  if (memoKeys.length >= MEMO_MAX) {
    const oldest = memoKeys.shift();
    worldToGridMemo.delete(oldest);
  }
  worldToGridMemo.set(key, final);
  memoKeys.push(key);
  return final;
}
// ─── THREE.JS SCENE SETUP ───────────────────────────────────────────────
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a16');
scene.fog = new THREE.Fog('#0a0a16', 8, 35);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(8, 6, 10);
camera.lookAt(0, 1.5, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 1.5, 0);
controls.minDistance = 3;
controls.maxDistance = 25;
controls.maxPolarAngle = Math.PI * 0.7;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
// ─── LIGHTING ───────────────────────────────────────────────────────────
const ambient = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffeedd', 4.5);
sun.position.set(10, 18, 6);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -12;
sun.shadow.camera.right = 12;
sun.shadow.camera.top = 12;
sun.shadow.camera.bottom = -12;
sun.shadow.bias = -0.00015;
scene.add(sun);
const fill = new THREE.DirectionalLight('#8899cc', 0.9);
fill.position.set(-4, 2, -2);
scene.add(fill);
// ─── BASE PLANE (subtle grid) ──────────────────────────────────────────
const gridHelper = new THREE.PolarGridHelper(GRID * 0.06, 32, 20, 64, '#222244', '#222244');
gridHelper.position.y = -2.5;
scene.add(gridHelper);
// ─── TERRAIN BUILDER (cached) ──────────────────────────────────────────
function buildTerrain(timeIndex) {
  const key = timeIndex;
  if (terrainCache.has(key)) {
    cacheStats.terrainHits++;
    return terrainCache.get(key);
  }
  cacheStats.terrainMisses++;
  // Evict oldest if cache too large
  if (terrainCache.size >= MAX_CACHE) {
    const firstKey = terrainCache.keys().next().value;
    const old = terrainCache.get(firstKey);
    old.geometry.dispose();
    old.material.dispose();
    terrainCache.delete(firstKey);
  }
  const step = dataSeries[timeIndex];
  const segments = GRID - 1;
  const size = GRID * 0.1; // physical size of the terrain
  const geo = new THREE.PlaneGeometry(size, size, segments, segments);
  geo.rotateX(-Math.PI / 2);
  // Use a non-indexed version for vertex colors (PlaneGeometry is indexed by default)
  const posArr = geo.attributes.position.array;
  const vertexCount = posArr.length / 3;
  // Create colors array
  const colorsArr = new Float32Array(vertexCount * 3);
  for (let i = 0; i < vertexCount; i++) {
    const x = posArr[i * 3];
    const z = posArr[i * 3 + 2];
    // Map world position to grid index (non-memoized here — build-time only)
    const gx = Math.floor((x / (size / GRID)) + GRID / 2);
    const gy = Math.floor((z / (size / GRID)) + GRID / 2);
    const ci = Math.max(0, Math.min(GRID * GRID - 1, gy * GRID + gx));
    const h = step.height[ci];
    const d = step.density[ci];
    // Set height: Y axis
    posArr[i * 3 + 1] = h;
    // Vertex color: density → lush green gradient
    // Low density = dark soil brown, high density = vibrant green
    const r = 0.15 + d * 0.1;
    const g = 0.2 + d * 0.65;
    const b = 0.08 + d * 0.12;
    colorsArr[i * 3] = r;
    colorsArr[i * 3 + 1] = g;
    colorsArr[i * 3 + 2] = b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
  geo.computeVertexNormals();
  // Re-index geometry for efficient rendering while keeping vertex colors
  // PlaneGeometry comes indexed; setting vertex colors works fine with indexed geo
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.05,
    flatShading: false,
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  const result = { geometry: geo, material: mat, mesh };
  terrainCache.set(key, result);
  return result;
}
// ─── RIVER BUILDER (cached) ────────────────────────────────────────────
// River traces the highest-error path across the terrain
function buildRivers(timeIndex) {
  const key = timeIndex;
  if (riverCache.has(key)) {
    cacheStats.riverHits++;
    return riverCache.get(key);
  }
  cacheStats.riverMisses++;
  if (riverCache.size >= MAX_CACHE) {
    const firstKey = riverCache.keys().next().value;
    const oldGroup = riverCache.get(firstKey);
    oldGroup.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); });
    riverCache.delete(firstKey);
  }
  const step = dataSeries[timeIndex];
  const group = new THREE.Group();
  // Trace error path: follow highest-error neighbor from left edge to right edge
  const pathPoints = [];
  const size = GRID * 0.1;
  const cellSize = size / GRID;
  // Start at left edge, row with highest cumulative error
  let bestRow = 0, bestErr = 0;
  for (let iy = 0; iy < GRID; iy++) {
    let sum = 0;
    for (let ix = 0; ix < Math.floor(GRID/8); ix++) sum += step.error[iy * GRID + ix];
    if (sum > bestErr) { bestErr = sum; bestRow = iy; }
  }
  let cx = 0, cy = bestRow;
  pathPoints.push(new THREE.Vector3(-size/2, step.height[cy * GRID + cx] + 0.04, (cy - GRID/2) * cellSize + cellSize/2));
  // Greedy path: move right, picking neighbor with highest error
  while (cx < GRID - 1) {
    let bestNx = cx + 1, bestNy = cy, bestNErr = -1;
    for (let dy = -1; dy <= 1; dy++) {
      const ny = cy + dy;
      if (ny < 0 || ny >= GRID) continue;
      const ni = ny * GRID + (cx + 1);
      const e = step.error[ni] + (dy === 0 ? 0.1 : 0); // slight preference for straight
      if (e > bestNErr) { bestNErr = e; bestNy = ny; bestNx = cx + 1; }
    }
    cx = bestNx; cy = bestNy;
    const idx = cy * GRID + cx;
    pathPoints.push(new THREE.Vector3(
      (cx - GRID/2) * cellSize + cellSize/2,
      step.height[idx] + 0.04,
      (cy - GRID/2) * cellSize + cellSize/2
    ));
  }
  // Build tube geometry along error path
  if (pathPoints.length >= 2) {
    const curve = new THREE.CatmullRomCurve3(pathPoints);
    const tubeGeo = new THREE.TubeGeometry(curve, pathPoints.length * 2, 0.06, 8, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: '#ff4a2a',
      emissive: '#330800',
      emissiveIntensity: 0.6,
      roughness: 0.3,
      metalness: 0.1,
    });
    const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
    tubeMesh.castShadow = true;
    tubeMesh.renderOrder = 1;
    tubeMesh.material.depthTest = true;
    tubeMesh.material.depthWrite = true;
    group.add(tubeMesh);
  }
  riverCache.set(key, group);
  return group;
}
// ─── PARTICLE SYSTEM ────────────────────────────────────────────────────
// API call trails: particles flow along valleys (low-height paths).
// Zero per-frame allocations: reuse position arrays, pre-compute start positions.
const PARTICLE_COUNT = 300;
const particleGeo = new THREE.BufferGeometry();
// Pre-allocate position array — mutated in-place each frame, never re-allocated
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
// Each particle has a pre-computed path (world-space waypoints) + progress
const particlePaths = new Array(PARTICLE_COUNT); // array of {waypoints: Vector3[], progress: float, speed: float}
const particleMaterial = new THREE.PointsMaterial({
  size: 0.08,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85,
});
function initParticlePaths(timeIndex) {
  const step = dataSeries[timeIndex];
  const size = GRID * 0.1;
  const cellSize = size / GRID;
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    // Pick random start on left or top edge
    const fromLeft = Math.random() > 0.5;
    let sx, sy, sz;
    if (fromLeft) {
      sy = Math.floor(Math.random() * GRID);
      sx = 0;
    } else {
      sx = Math.floor(Math.random() * GRID);
      sy = 0;
    }
    const idx = sy * GRID + sx;
    sz = step.height[idx] + 0.08;
    const start = new THREE.Vector3(
      (sx - GRID/2) * cellSize + cellSize/2,
      sz,
      (sy - GRID/2) * cellSize + cellSize/2
    );
    // Generate path: traverse toward opposite edge following lowest-height neighbor
    const waypoints = [start.clone()];
    let cx = sx, cy = sy;
    const maxSteps = 40;
    for (let s = 0; s < maxSteps; s++) {
      let bestNx = cx, bestNy = cy, bestH = Infinity;
      // Bias direction: if from left, go right; if from top, go down
      const preferDX = fromLeft ? 1 : 0;
      const preferDY = fromLeft ? 0 : 1;
      for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
          if (dx === 0 && dy === 0) continue;
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          const ni = ny * GRID + nx;
          const h = step.height[ni];
          // Prefer direction bias by slight penalty against wrong direction
          const biasPenalty = (fromLeft && dx < 0 ? 0.3 : 0) + (!fromLeft && dy < 0 ? 0.3 : 0);
          const score = h + biasPenalty;
          if (score < bestH) { bestH = score; bestNx = nx; bestNy = ny; }
        }
      }
      if (bestNx === cx && bestNy === cy) break; // stuck
      cx = bestNx; cy = bestNy;
      const wi = cy * GRID + cx;
      waypoints.push(new THREE.Vector3(
        (cx - GRID/2) * cellSize + cellSize/2,
        step.height[wi] + 0.08,
        (cy - GRID/2) * cellSize + cellSize/2
      ));
      if ((fromLeft && cx >= GRID - 1) || (!fromLeft && cy >= GRID - 1)) break;
    }
    // Set particle data
    particlePaths[p] = {
      waypoints,
      progress: Math.random(), // random start offset for staggered flow
      speed: 0.002 + Math.random() * 0.006,
      colorPhase: Math.random() * 2 * Math.PI,
    };
    // Set initial position and color
    const wp0 = waypoints[0];
    particlePositions[p * 3] = wp0.x;
    particlePositions[p * 3 + 1] = wp0.y;
    particlePositions[p * 3 + 2] = wp0.z;
    particleColors[p * 3] = 1.0;
    particleColors[p * 3 + 1] = 0.82;
    particleColors[p * 3 + 2] = 0.2;
  }
  particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
}
const particles = new THREE.Points(particleGeo, particleMaterial);
particles.renderOrder = 2;
particles.material.depthTest = true;
particles.material.depthWrite = false;
scene.add(particles);
// ─── SCENE STATE ────────────────────────────────────────────────────────
let currentTimeIndex = 0;
let terrainMesh = null;
let riverGroup = null;
function setTimeSlice(index) {
  if (index === currentTimeIndex && terrainMesh) return; // no-op if unchanged
  currentTimeIndex = index;
  // Terrain: swap from cache (cache hit — no new geometry)
  const cached = buildTerrain(index);
  if (terrainMesh) {
    scene.remove(terrainMesh);
    // Don't dispose — it's cached
  }
  terrainMesh = cached.mesh;
  scene.add(terrainMesh);
  // Rivers: swap from cache
  if (riverGroup) scene.remove(riverGroup);
  riverGroup = buildRivers(index);
  scene.add(riverGroup);
  // Re-init particle paths for this time slice
  initParticlePaths(index);
  // Update UI
  document.getElementById('time-value').textContent = `T${index}`;
}
// ─── DEBOUNCED SLIDER ──────────────────────────────────────────────────
let debounceTimer = null;
const slider = document.getElementById('time-slider');
slider.max = TIME_STEPS - 1;
slider.value = 0;
slider.addEventListener('input', () => {
  const val = parseInt(slider.value);
  document.getElementById('time-value').textContent = `T${val}`;
  // Debounce terrain rebuild: 200ms
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => setTimeSlice(val), 200);
});
// Immediate on change end (mouseup for instant feel on click, debounce for scrub)
slider.addEventListener('change', () => {
  if (debounceTimer) { clearTimeout(debounceTimer); debounceTimer = null; }
  setTimeSlice(parseInt(slider.value));
});
// ─── CAMERA BOOKMARKS ───────────────────────────────────────────────────
const bookmarks = [];
const BM_STORAGE_KEY = 'terrain_explorer_bookmarks';
function loadBookmarks() {
  try {
    const raw = localStorage.getItem(BM_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}
function saveBookmarks() {
  localStorage.setItem(BM_STORAGE_KEY, JSON.stringify(bookmarks));
}
function captureBookmark(name) {
  return {
    name,
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
    zoom: camera.zoom,
  };
}
function applyBookmark(bm) {
  camera.position.set(bm.pos[0], bm.pos[1], bm.pos[2]);
  controls.target.set(bm.target[0], bm.target[1], bm.target[2]);
  camera.zoom = bm.zoom || 1;
  camera.updateProjectionMatrix();
  controls.update();
}
function renderBookmarkList() {
  const list = document.getElementById('bm-list');
  list.innerHTML = bookmarks.map((bm, i) =>
    `<div class="bm-btn">
      <span style="cursor:pointer;flex:1;" data-bm-idx="${i}">${bm.name}</span>
      <span class="bm-del" data-bm-del="${i}">x</span>
    </div>`
  ).join('');
  // Event delegation
  list.querySelectorAll('[data-bm-idx]').forEach(el => {
    el.addEventListener('click', () => applyBookmark(bookmarks[parseInt(el.dataset.bmIdx)]));
  });
  list.querySelectorAll('[data-bm-del]').forEach(el => {
    el.addEventListener('click', (e) => {
      e.stopPropagation();
      bookmarks.splice(parseInt(el.dataset.bmDel), 1);
      saveBookmarks();
      renderBookmarkList();
    });
  });
}
document.getElementById('bm-save-current').addEventListener('click', () => {
  const name = `View ${bookmarks.length + 1} (T${currentTimeIndex})`;
  bookmarks.push(captureBookmark(name));
  saveBookmarks();
  renderBookmarkList();
});
// Restore bookmarks
bookmarks.push(...loadBookmarks());
renderBookmarkList();
// ─── HOVER TOOLTIP (world-to-grid lookup — memoized) ────────────────────
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!terrainMesh) { tooltip.style.display = 'none'; return; }
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const grid = worldToGrid(pt.x, pt.z); // memoized
    const step = dataSeries[currentTimeIndex];
    const ci = grid.iy * GRID + grid.ix;
    const h = step.height[ci] || 0;
    const d = step.density[ci] || 0;
    const err = step.error[ci] || 0;
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 16) + 'px';
    tooltip.style.top = (e.clientY - 8) + 'px';
    tooltip.innerHTML =
      `Grid(${grid.ix},${grid.iy})<br>` +
      `Height: ${h.toFixed(2)}  Density: ${(d*100).toFixed(0)}%  Error: ${(err*100).toFixed(1)}%`;
  } else {
    tooltip.style.display = 'none';
  }
});
// ─── DIAGNOSTIC PANEL UPDATE ────────────────────────────────────────────
let fpsFrames = 0, fpsTime = performance.now(), currentFPS = 60;
function updateDebugPanel() {
  document.getElementById('db-terrain-hits').textContent = cacheStats.terrainHits;
  document.getElementById('db-terrain-misses').textContent = cacheStats.terrainMisses;
  document.getElementById('db-river-hits').textContent = cacheStats.riverHits;
  document.getElementById('db-river-misses').textContent = cacheStats.riverMisses;
  document.getElementById('db-fps').textContent = currentFPS;
  document.getElementById('db-allocs').textContent = allocsThisFrame;
  const allocsEl = document.getElementById('db-allocs');
  allocsEl.className = 'val ' + (allocsThisFrame === 0 ? 'good' : 'warn');
}
// ─── RENDER LOOP ────────────────────────────────────────────────────────
function animate(timestamp) {
  requestAnimationFrame(animate);
  // Reset per-frame allocation counter
  allocsThisFrame = 0;
  controls.update();
  // Animate particles: update positions in-place on the pre-allocated array
  const size = GRID * 0.1;
  const cellSize = size / GRID;
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    const pd = particlePaths[p];
    if (!pd || pd.waypoints.length < 2) continue;
    pd.progress += pd.speed;
    if (pd.progress >= 1) pd.progress -= 1; // loop
    // Find which segment the progress falls in
    const segCount = pd.waypoints.length - 1;
    const rawSeg = pd.progress * segCount;
    const segIdx = Math.min(Math.floor(rawSeg), segCount - 1);
    const segFrac = rawSeg - segIdx;
    const a = pd.waypoints[segIdx];
    const b = pd.waypoints[segIdx + 1];
    // Linear interpolation (fast, no allocations)
    const pi = p * 3;
    particlePositions[pi] = a.x + (b.x - a.x) * segFrac;
    particlePositions[pi + 1] = a.y + (b.y - a.y) * segFrac + 0.02;
    particlePositions[pi + 2] = a.z + (b.z - a.z) * segFrac;
    // Pulse color based on progress
    const pulse = 0.6 + 0.4 * Math.sin(pd.progress * Math.PI * 2 + pd.colorPhase);
    particleColors[pi] = 1.0;
    particleColors[pi + 1] = 0.7 * pulse + 0.3;
    particleColors[pi + 2] = 0.15 * pulse + 0.1;
  }
  // Flag attributes as needing update (no allocation — just flagging the buffer)
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  // Render
  renderer.render(scene, camera);
  // FPS counter
  fpsFrames++;
  if (timestamp - fpsTime >= 1000) {
    currentFPS = Math.round(fpsFrames / ((timestamp - fpsTime) / 1000));
    fpsFrames = 0;
    fpsTime = timestamp;
  }
  updateDebugPanel();
}
// ─── INITIALIZATION ─────────────────────────────────────────────────────
setTimeSlice(0);
requestAnimationFrame(animate);
// ─── RESIZE HANDLER ─────────────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── KEYBOARD SHORTCUTS ─────────────────────────────────────────────────
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      // Reset camera
      camera.position.set(8, 6, 10);
      controls.target.set(0, 1.5, 0);
      controls.update();
      break;
    case 'a':
      // Toggle auto-rotate
      controls.autoRotate = !controls.autoRotate;
      break;
    case 'arrowleft':
      if (currentTimeIndex > 0) { slider.value = currentTimeIndex - 1; setTimeSlice(currentTimeIndex - 1); }
      break;
    case 'arrowright':
      if (currentTimeIndex < TIME_STEPS - 1) { slider.value = currentTimeIndex + 1; setTimeSlice(currentTimeIndex + 1); }
      break;
  }
});
console.log('3D Data Terrain Explorer ready.');
console.log(`Terrain: ${GRID}x${GRID} grid, ${TIME_STEPS} time steps`);
console.log(`Particles: ${PARTICLE_COUNT} trails, zero per-frame allocation`);
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan, R=reset, A=auto-rotate, arrows=time');
console.log('Cache: terrain + river geometry cached per time step, worldToGrid memoized');
</script>
</body>
</html>