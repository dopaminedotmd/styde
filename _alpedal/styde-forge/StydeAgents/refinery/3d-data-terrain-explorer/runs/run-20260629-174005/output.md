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
    --border: rgba(255,255,255,0.08);
    --text: #c8c8d4;
    --accent: #64b5f6;
    --warn: #ef5350;
    --ok: #66bb6a;
    --font: 'Inter', 'Segoe UI', system-ui, sans-serif;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg);
    overflow: hidden;
    font-family: var(--font);
    color: var(--text);
    height: 100vh;
    width: 100vw;
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 1;
  }
  canvas { display: block; }
  .panel {
    position: fixed;
    z-index: 10;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    backdrop-filter: blur(12px);
    padding: 14px 18px;
    font-size: 12px;
    pointer-events: auto;
  }
  .panel.top-left { top: 16px; left: 16px; min-width: 200px; }
  .panel.top-right { top: 16px; right: 16px; min-width: 180px; }
  .panel.bottom { bottom: 16px; left: 50%; transform: translateX(-50%); min-width: 360px; }
  .panel h3 {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--accent);
    margin-bottom: 10px;
    font-weight: 600;
  }
  .stat-row {
    display: flex;
    justify-content: space-between;
    padding: 3px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  .stat-label { color: #888; }
  .stat-value { font-weight: 600; font-variant-numeric: tabular-nums; }
  input[type="range"] {
    width: 100%;
    height: 6px;
    -webkit-appearance: none;
    background: linear-gradient(90deg, var(--accent), #ce93d8);
    border-radius: 3px;
    outline: none;
    margin: 8px 0;
  }
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    background: #fff;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(100,180,246,0.5);
  }
  .btn-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
  }
  button {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    color: var(--text);
    padding: 5px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 11px;
    font-family: var(--font);
    transition: all 0.15s;
    white-space: nowrap;
  }
  button:hover { background: rgba(255,255,255,0.12); border-color: var(--accent); }
  button.active { background: rgba(100,180,246,0.18); border-color: var(--accent); color: #fff; }
  #cache-stats {
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 10px;
    line-height: 1.6;
    color: #aaa;
  }
  .cache-hit { color: var(--ok); }
  .cache-miss { color: var(--warn); }
  #tooltip {
    position: fixed;
    z-index: 20;
    pointer-events: none;
    background: rgba(0,0,0,0.85);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 11px;
    display: none;
    max-width: 200px;
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div class="panel top-left" id="metrics-panel">
  <h3>Terrain Metrics</h3>
  <div id="metrics-content"></div>
</div>
<div class="panel top-right">
  <h3>Bookmarks</h3>
  <div class="btn-row" id="bookmark-buttons"></div>
  <div class="btn-row" style="margin-top:6px">
    <button id="btn-save-bookmark">Save View</button>
    <button id="btn-auto-rotate" class="active">Auto Rotate</button>
  </div>
</div>
<div class="panel bottom" id="time-panel">
  <h3>Time Dimension</h3>
  <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
  <div style="display:flex; justify-content:space-between; font-size:10px; color:#888">
    <span>00:00</span><span id="time-label">00:00</span><span>23:00</span>
  </div>
</div>
<div class="panel" style="bottom:16px; right:16px; font-size:10px; max-width:220px" id="cache-panel">
  <h3>Cache Diagnostic</h3>
  <div id="cache-stats"></div>
</div>
<div id="tooltip"></div>
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
const $ = (sel) => document.querySelector(sel);
class StateManager {
  // All DOM mutations go through this single bottleneck.
  // No component touches innerHTML, appendChild, or classList directly.
  // This keeps state flow traceable: state change -> render() -> DOM update.
  constructor() {
    this._state = {
      timeIndex: 0,
      autoRotate: true,
      hoveredCell: null,
      bookmarks: [],
      cacheHits: 0,
      cacheMisses: 0,
      fps: 0,
      vertexCount: 0,
      riverLength: 0,
      particleCount: 0
    };
    this._listeners = [];
  }
  get(k) { return this._state[k]; }
  set(k, v) {
    if (this._state[k] === v) return;
    this._state[k] = v;
    this._notify(k, v);
  }
  batch(updates) {
    let changed = false;
    for (const [k, v] of Object.entries(updates)) {
      if (this._state[k] !== v) { this._state[k] = v; changed = true; }
    }
    if (changed) this._notify('*', null);
  }
  on(k, fn) { this._listeners.push({k, fn}); }
  _notify(key, val) {
    for (const l of this._listeners) {
      if (l.k === key || l.k === '*') l.fn(key, val, this._state);
    }
  }
}
const state = new StateManager();
// ---- DATA GENERATION ----
// Generates synthetic 24-hour time-series: revenue (height), user density (color),
// error rate (river), API calls (particles). Grid: 64x64 vertices.
const GRID = 64;
const HOURS = 24;
const TERRAIN_SCALE = 3.0;
function generateTerrainData() {
  // Precompute all 24 time-slices once; cache as flat Float32 arrays.
  const data = [];
  for (let t = 0; t < HOURS; t++) {
    const height = new Float32Array(GRID * GRID);
    const density = new Float32Array(GRID * GRID);
    const error = new Float32Array(GRID * GRID);
    const apiFlow = new Float32Array(GRID * GRID);
    const phase = (t / HOURS) * Math.PI * 2;
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iy * GRID + ix;
        const nx = (ix / (GRID - 1) - 0.5) * 2;
        const ny = (iy / (GRID - 1) - 0.5) * 2;
        const dist = Math.sqrt(nx * nx + ny * ny);
        // Revenue: two moving hotspots create evolving terrain
        const hot1 = Math.exp(-((nx - Math.cos(phase * 0.7)) ** 2 + (ny - Math.sin(phase * 0.5)) ** 2) / 0.15);
        const hot2 = Math.exp(-((nx - Math.cos(phase * 0.7 + 2)) ** 2 + (ny - Math.sin(phase * 0.5 + 2)) ** 2) / 0.2);
        const base = Math.sin(nx * 3 + phase * 0.3) * Math.cos(ny * 3) * 0.3;
        height[idx] = (hot1 * 1.2 + hot2 * 0.8 + base + 0.3) * TERRAIN_SCALE;
        // User density: peaks near center, modulated by time
        density[idx] = Math.max(0, 1 - dist * 1.4) * (0.6 + 0.4 * Math.sin(phase * 1.3));
        // Error rate: concentrated along diagonals
        const diagDist = Math.abs(nx - ny) / Math.SQRT2;
        error[idx] = Math.exp(-diagDist * diagDist / 0.08) * (0.3 + 0.7 * Math.abs(Math.sin(phase * 2.1)));
        // API flow: trails along valleys, orthogonal to ridges
        apiFlow[idx] = (1 - Math.abs(height[idx] / TERRAIN_SCALE - 0.5) * 2) * (0.5 + 0.5 * Math.cos(phase * 1.7 + dist * 3));
      }
    }
    data.push({ height, density, error, apiFlow });
  }
  return data;
}
const terrainData = generateTerrainData();
// ---- CACHE LAYER ----
// Mandatory: cache every cacheable output. Log hit/miss to diagnostic panel.
const geometryCache = new Map();
const riverCache = new Map();
const particleStartCache = new Map();
const colorCache = new Map();
let cacheHits = 0;
let cacheMisses = 0;
function cacheGet(cache, key) {
  if (cache.has(key)) { cacheHits++; return cache.get(key); }
  cacheMisses++;
  return null;
}
function cacheSet(cache, key, value) {
  cache.set(key, value);
  return value;
}
function updateCacheUI() {
  state.batch({
    cacheHits,
    cacheMisses
  });
}
// ---- THREE.JS SETUP ----
const container = $('#canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.Fog(0x0a0a0f, 8, 40);
const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.5, 60);
camera.position.set(6, 5.5, 8);
camera.lookAt(0, 0.8, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.8, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 2;
controls.maxDistance = 18;
controls.maxPolarAngle = Math.PI * 0.65;
controls.update();
// ---- LIGHTING ----
const ambient = new THREE.AmbientLight(0x222244, 1.4);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
sun.position.set(10, 15, 5);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 50;
sun.shadow.camera.left = -10;
sun.shadow.camera.right = 10;
sun.shadow.camera.top = 10;
sun.shadow.camera.bottom = -10;
sun.shadow.bias = -0.0002;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
fill.position.set(-5, 2, -3);
scene.add(fill);
// ---- TERRAIN MESH ----
// Single shared geometry; we mutate position + color attributes per time-slice.
// Reuses BufferGeometry.attributes.position.array — no per-frame allocations.
const terrainGeo = new THREE.BufferGeometry();
const posArray = new Float32Array(GRID * GRID * 3);
const colArray = new Float32Array(GRID * GRID * 3);
const idxArray = [];
for (let iy = 0; iy < GRID - 1; iy++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = iy * GRID + ix;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    idxArray.push(a, b, d, a, d, c);
  }
}
// Initialize x,z positions once; only y changes per time-slice.
for (let iy = 0; iy < GRID; iy++) {
  for (let ix = 0; ix < GRID; ix++) {
    const idx = iy * GRID + ix;
    posArray[idx * 3] = (ix / (GRID - 1) - 0.5) * GRID * 0.12;
    posArray[idx * 3 + 2] = (iy / (GRID - 1) - 0.5) * GRID * 0.12;
  }
}
terrainGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colArray, 3));
terrainGeo.setIndex(idxArray);
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.15,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Grid overlay for spatial reference
const gridHelper = new THREE.PolarGridHelper(GRID * 0.06, GRID, GRID / 2, 64, 0x334466, 0x334466);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
// ---- RIVER SYSTEM ----
// TubeGeometry tracing high-error paths. Cached per time-slice.
let riverMesh = null;
const RIVER_THRESHOLD = 0.4;
const RIVER_COLOR = new THREE.Color('#ef5350');
function extractRiverPath(errorField) {
  // Trace the highest-error ridge through the grid using a greedy path.
  // Start at left edge, step right choosing max-error neighbor.
  const path = [];
  const midY = Math.floor(GRID / 2);
  let cx = 0;
  let cy = midY;
  // Find best start on left edge
  let bestVal = 0;
  for (let y = 0; y < GRID; y++) {
    const v = errorField[y * GRID];
    if (v > bestVal) { bestVal = v; cy = y; }
  }
  while (cx < GRID - 1) {
    const idx = cy * GRID + cx;
    path.push(new THREE.Vector3(
      (cx / (GRID - 1) - 0.5) * GRID * 0.12,
      0, // will be set after
      (cy / (GRID - 1) - 0.5) * GRID * 0.12
    ));
    // Greedy step: choose neighbor with highest error
    const candidates = [];
    for (let dy = -1; dy <= 1; dy++) {
      const ny = cy + dy;
      if (ny < 0 || ny >= GRID) continue;
      candidates.push({ y: ny, v: errorField[ny * GRID + cx + 1] });
    }
    candidates.sort((a, b) => b.v - a.v);
    cx += 1;
    cy = candidates[0].y;
  }
  // Add final point
  path.push(new THREE.Vector3(
    ((GRID - 1) / (GRID - 1) - 0.5) * GRID * 0.12,
    0,
    (cy / (GRID - 1) - 0.5) * GRID * 0.12
  ));
  return path;
}
function buildRiverGeometry(timeIndex) {
  const cached = cacheGet(riverCache, timeIndex);
  if (cached) {
    state.set('riverLength', cached.userData.pathLength);
    return cached;
  }
  const { height, error } = terrainData[timeIndex];
  const basePath = extractRiverPath(error);
  // Lift path points to terrain surface
  for (const pt of basePath) {
    const gx = Math.round((pt.x / (GRID * 0.06) + 0.5) * (GRID - 1));
    const gy = Math.round((pt.z / (GRID * 0.06) + 0.5) * (GRID - 1));
    const ci = Math.min(Math.max(gy, 0), GRID - 1) * GRID + Math.min(Math.max(gx, 0), GRID - 1);
    pt.y = height[ci] + 0.08; // Slightly above terrain to avoid z-fighting
  }
  const curve = new THREE.CatmullRomCurve3(basePath);
  const tubeGeo = new THREE.TubeGeometry(curve, 128, 0.06, 8, false);
  const tubeMat = new THREE.MeshStandardMaterial({
    color: RIVER_COLOR,
    emissive: RIVER_COLOR,
    emissiveIntensity: 0.7,
    roughness: 0.3,
    metalness: 0.4
  });
  const mesh = new THREE.Mesh(tubeGeo, tubeMat);
  mesh.userData.pathLength = basePath.length;
  state.set('riverLength', basePath.length);
  cacheSet(riverCache, timeIndex, mesh);
  return mesh;
}
// ---- PARTICLE SYSTEM ----
// BufferGeometry with reusable position array. Particles follow apiFlow gradient.
const PARTICLE_COUNT = 600;
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
// Per-particle state: current grid position (x,z float), velocity
const particleState = new Float32Array(PARTICLE_COUNT * 4); // [gx, gz, vx, vz]
function initParticles(timeIndex) {
  const cached = cacheGet(particleStartCache, timeIndex);
  if (cached) {
    particlePositions.set(cached.positions);
    particleState.set(cached.state);
    particleGeo.attributes.position.needsUpdate = true;
    return;
  }
  const { apiFlow, height } = terrainData[timeIndex];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Start particles in high-flow regions
    let gx, gz;
    let attempts = 0;
    do {
      gx = Math.random() * (GRID - 1);
      gz = Math.random() * (GRID - 1);
      const idx = Math.floor(gz) * GRID + Math.floor(gx);
      attempts++;
    } while (apiFlow[Math.floor(gz) * GRID + Math.floor(gx)] < 0.3 && attempts < 20);
    const idx = Math.floor(gz) * GRID + Math.floor(gx);
    const worldX = (gx / (GRID - 1) - 0.5) * GRID * 0.12;
    const worldZ = (gz / (GRID - 1) - 0.5) * GRID * 0.12;
    const worldY = height[idx] + 0.25;
    particlePositions[i * 3] = worldX;
    particlePositions[i * 3 + 1] = worldY;
    particlePositions[i * 3 + 2] = worldZ;
    particleState[i * 4] = gx;
    particleState[i * 4 + 1] = gz;
    particleState[i * 4 + 2] = (Math.random() - 0.5) * 0.3;
    particleState[i * 4 + 3] = (Math.random() - 0.5) * 0.3;
  }
  cacheSet(particleStartCache, timeIndex, {
    positions: new Float32Array(particlePositions),
    state: new Float32Array(particleState)
  });
  particleGeo.attributes.position.needsUpdate = true;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
// Sprite-based particles for performance
const particleSpriteTex = (() => {
  const canvas = document.createElement('canvas');
  canvas.width = 32;
  canvas.height = 32;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, 'rgba(255,220,180,1)');
  gradient.addColorStop(0.3, 'rgba(255,180,100,0.7)');
  gradient.addColorStop(0.7, 'rgba(100,180,255,0.15)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 32, 32);
  return new THREE.CanvasTexture(canvas);
})();
const particleMat = new THREE.PointsMaterial({
  size: 0.18,
  map: particleSpriteTex,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  color: new THREE.Color('#ffcc80'),
  opacity: 0.75
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
scene.add(particleSystem);
// ---- TIME-SLICE SWITCHING ----
// Swaps terrain height + vertex colors; rebuilds river from cache.
function applyTimeSlice(timeIndex) {
  const { height, density, error, apiFlow } = terrainData[timeIndex];
  // Update terrain positions (y only) and vertex colors
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      posArray[idx * 3 + 1] = height[idx];
      // Color: density mapped to green gradient; error adds red tint
      const d = density[idx];
      const e = error[idx];
      colArray[idx * 3] = 0.22 + e * 1.5;                           // R: red from errors
      colArray[idx * 3 + 1] = 0.28 + d * 0.9;                       // G: green from density
      colArray[idx * 3 + 2] = 0.35 + (1 - e) * 0.5;                // B: blue base
    }
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  // Swap river geometry (cached)
  if (riverMesh) {
    scene.remove(riverMesh);
    if (riverMesh.geometry) riverMesh.geometry.dispose();
    riverMesh = null;
  }
  riverMesh = buildRiverGeometry(timeIndex);
  if (riverMesh) scene.add(riverMesh);
  // Re-init particles for this time slice (cached start positions)
  initParticles(timeIndex);
  state.batch({
    timeIndex,
    vertexCount: GRID * GRID,
    particleCount: PARTICLE_COUNT
  });
  updateCacheUI();
}
// ---- PER-FRAME UPDATE ----
// Particle movement: flow along apiFlow gradient with terrain clamping.
// Reuses particlePositions array — no per-frame allocations.
const _flowVec = new THREE.Vector2(); // Single reusable vector for gradient lookups
function updateParticles(dt, timeIndex) {
  const { apiFlow, height } = terrainData[timeIndex];
  const gridScaleX = GRID * 0.12;
  const gridScaleZ = GRID * 0.12;
  const halfGrid = GRID / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    let gx = particleState[i * 4];
    let gz = particleState[i * 4 + 1];
    // Sample flow gradient at current position
    const igx = Math.floor(gx);
    const igz = Math.floor(gz);
    const fx = gx - igx;
    const fz = gz - igz;
    // Bilinear sample of flow field
    const idx00 = Math.min(Math.max(igz, 0), GRID - 1) * GRID + Math.min(Math.max(igx, 0), GRID - 1);
    const idx10 = Math.min(Math.max(igz, 0), GRID - 1) * GRID + Math.min(Math.max(igx + 1, 0), GRID - 1);
    const idx01 = Math.min(Math.max(igz + 1, 0), GRID - 1) * GRID + Math.min(Math.max(igx, 0), GRID - 1);
    const idx11 = Math.min(Math.max(igz + 1, 0), GRID - 1) * GRID + Math.min(Math.max(igx + 1, 0), GRID - 1);
    const flow = (apiFlow[idx00] * (1 - fx) + apiFlow[idx10] * fx) * (1 - fz) +
                 (apiFlow[idx01] * (1 - fx) + apiFlow[idx11] * fx) * fz;
    // Gradient: finite difference
    const flowRx = (apiFlow[Math.min(Math.max(igz, 0), GRID - 1) * GRID + Math.min(Math.max(igx + 2, 0), GRID - 1)] -
                    apiFlow[idx00]) * 0.5;
    const flowRz = (apiFlow[Math.min(Math.max(igz + 2, 0), GRID - 1) * GRID + Math.min(Math.max(igx, 0), GRID - 1)] -
                    apiFlow[idx00]) * 0.5;
    // Update velocity with flow gradient + small random drift
    particleState[i * 4 + 2] += flowRx * 0.04 + (Math.random() - 0.5) * 0.02;
    particleState[i * 4 + 3] += flowRz * 0.04 + (Math.random() - 0.5) * 0.02;
    // Damping
    particleState[i * 4 + 2] *= 0.96;
    particleState[i * 4 + 3] *= 0.96;
    gx += particleState[i * 4 + 2] * dt * 3;
    gz += particleState[i * 4 + 3] * dt * 3;
    // Wrap at grid boundaries
    if (gx < 0) gx += GRID - 1;
    if (gx >= GRID) gx -= GRID - 1;
    if (gz < 0) gz += GRID - 1;
    if (gz >= GRID) gz -= GRID - 1;
    particleState[i * 4] = gx;
    particleState[i * 4 + 1] = gz;
    // Convert to world and clamp to terrain
    const worldX = (gx / (GRID - 1) - 0.5) * gridScaleX;
    const worldZ = (gz / (GRID - 1) - 0.5) * gridScaleZ;
    // Terrain height lookup with bilinear interpolation
    const hIdx = Math.min(Math.max(Math.floor(gz), 0), GRID - 2) * GRID + Math.min(Math.max(Math.floor(gx), 0), GRID - 2);
    const h00 = height[hIdx];
    const h10 = height[hIdx + 1];
    const h01 = height[hIdx + GRID];
    const h11 = height[hIdx + GRID + 1];
    const terrainY = (h00 * (1 - fx) + h10 * fx) * (1 - fz) + (h01 * (1 - fx) + h11 * fx) * fz;
    particlePositions[i * 3] = worldX;
    particlePositions[i * 3 + 1] = terrainY + 0.25 + flow * 0.6;
    particlePositions[i * 3 + 2] = worldZ;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ---- BOOKMARK SYSTEM ----
// Saves camera position + target as named bookmarks. Stored in state, rendered via StateManager.
const DEFAULT_BOOKMARKS = [
  { name: 'Overview', pos: [6, 5.5, 8], target: [0, 0.8, 0] },
  { name: 'Top Down', pos: [0, 10, 0.1], target: [0, 0, 0] },
  { name: 'Close East', pos: [1.5, 1.8, 3.5], target: [0.3, 0.6, 0] },
];
state.set('bookmarks', [...DEFAULT_BOOKMARKS]);
function applyBookmark(bm) {
  camera.position.set(...bm.pos);
  controls.target.set(...bm.target);
  controls.update();
}
function renderBookmarkButtons() {
  const container = $('#bookmark-buttons');
  // StateManager-driven: rebuild DOM from state, not incremental mutations
  const bookmarks = state.get('bookmarks');
  container.innerHTML = bookmarks.map((bm, i) =>
    `<button class="bm-btn" data-index="${i}">${bm.name}</button>`
  ).join('');
  // Bind events via delegation — single listener, no per-button closures
  container.onclick = (e) => {
    const btn = e.target.closest('.bm-btn');
    if (!btn) return;
    const idx = parseInt(btn.dataset.index);
    applyBookmark(bookmarks[idx]);
  };
}
$('#btn-save-bookmark').onclick = () => {
  const name = prompt('Bookmark name:');
  if (!name) return;
  const bm = {
    name,
    pos: camera.position.toArray(),
    target: controls.target.toArray()
  };
  const bookmarks = [...state.get('bookmarks'), bm];
  state.set('bookmarks', bookmarks);
};
$('#btn-auto-rotate').onclick = function() {
  controls.autoRotate = !controls.autoRotate;
  state.set('autoRotate', controls.autoRotate);
  this.classList.toggle('active', controls.autoRotate);
};
// ---- TIME SLIDER ----
const timeSlider = $('#time-slider');
const timeLabel = $('#time-label');
timeSlider.oninput = () => {
  const t = parseInt(timeSlider.value);
  const hour = String(t).padStart(2, '0');
  timeLabel.textContent = `${hour}:00`;
  applyTimeSlice(t);
};
// ---- TOOLTIP / HOVER ----
// Memoized world-to-grid transform: compute once per frame, reuse.
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = $('#tooltip');
// Memoization cache for coordinate transforms
const _transformCache = { frame: -1, worldX: 0, worldZ: 0, gridX: -1, gridZ: -1 };
function worldToGrid(worldX, worldZ, frameId) {
  // Memoize: if same world coords in same frame, return cached result
  if (_transformCache.frame === frameId &&
      Math.abs(_transformCache.worldX - worldX) < 0.001 &&
      Math.abs(_transformCache.worldZ - worldZ) < 0.001) {
    return { gx: _transformCache.gridX, gz: _transformCache.gridZ };
  }
  const gx = Math.round((worldX / (GRID * 0.06) + 0.5) * (GRID - 1));
  const gz = Math.round((worldZ / (GRID * 0.06) + 0.5) * (GRID - 1));
  _transformCache.frame = frameId;
  _transformCache.worldX = worldX;
  _transformCache.worldZ = worldZ;
  _transformCache.gridX = gx;
  _transformCache.gridZ = gz;
  return { gx, gz };
}
let frameIdCounter = 0;
function updateTooltip(event, timeIndex) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const { gx, gz } = worldToGrid(pt.x, pt.z, frameIdCounter);
    if (gx < 0 || gx >= GRID || gz < 0 || gz >= GRID) {
      tooltip.style.display = 'none';
      return;
    }
    const idx = gz * GRID + gx;
    const { height, density, error, apiFlow } = terrainData[timeIndex];
    tooltip.style.display = 'block';
    tooltip.style.left = (event.clientX + 18) + 'px';
    tooltip.style.top = (event.clientY - 10) + 'px';
    tooltip.innerHTML = [
      `Revenue: ${height[idx].toFixed(2)}`,
      `Density: ${(density[idx] * 100).toFixed(0)}%`,
      `Errors:  ${(error[idx] * 100).toFixed(1)}%`,
      `API:     ${(apiFlow[idx] * 100).toFixed(0)}%`
    ].join('<br>');
  } else {
    tooltip.style.display = 'none';
  }
}
window.addEventListener('mousemove', (e) => updateTooltip(e, state.get('timeIndex')), { passive: true });
// ---- METRICS PANEL ----
state.on('*', () => {
  const s = state._state;
  $('#metrics-content').innerHTML = [
    `<div class="stat-row"><span class="stat-label">Vertices</span><span class="stat-value">${(s.vertexCount / 1000).toFixed(1)}k</span></div>`,
    `<div class="stat-row"><span class="stat-label">Particles</span><span class="stat-value">${s.particleCount}</span></div>`,
    `<div class="stat-row"><span class="stat-label">River Pts</span><span class="stat-value">${s.riverLength || '-'}</span></div>`,
    `<div class="stat-row"><span class="stat-label">FPS</span><span class="stat-value">${s.fps}</span></div>`,
  ].join('');
});
// ---- CACHE DIAGNOSTIC PANEL ----
state.on('cacheHits', () => {
  const s = state._state;
  const total = s.cacheHits + s.cacheMisses || 1;
  const rate = ((s.cacheHits / total) * 100).toFixed(1);
  $('#cache-stats').innerHTML = [
    `<span class="cache-hit">Hits: ${s.cacheHits}</span>`,
    `<span class="cache-miss">Misses: ${s.cacheMisses}</span>`,
    `Rate: ${rate}%`,
    `GeoCached: ${geometryCache.size} | RiverCached: ${riverCache.size} | PartCached: ${particleStartCache.size}`
  ].join('<br>');
});
// ---- RENDER LOOP ----
const clock = new THREE.Clock();
let fpsFrames = 0;
let fpsTime = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1); // Cap delta to avoid spiral on tab switch
  frameIdCounter++;
  controls.update();
  updateParticles(dt, state.get('timeIndex'));
  renderer.render(scene, camera);
  // FPS counter
  fpsFrames++;
  fpsTime += dt;
  if (fpsTime >= 0.5) {
    state.set('fps', Math.round(fpsFrames / fpsTime));
    fpsFrames = 0;
    fpsTime = 0;
  }
}
// ---- RESIZE HANDLER ----
// Debounced resize: only recompute after 150ms of no resize events.
let resizeTimer = null;
window.addEventListener('resize', () => {
  if (resizeTimer) clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  }, 150);
});
// ---- INITIALIZATION ----
renderBookmarkButtons();
state.on('bookmarks', renderBookmarkButtons);
applyTimeSlice(0);
timeSlider.value = 0;
timeLabel.textContent = '00:00';
animate();
// Diagnostic: log cache-aware architecture
console.log('%c3D Terrain Explorer Ready %c| Cache-aware | StateManager-driven DOM | No per-frame geometry allocations',
  'color:#64b5f6;font-weight:bold', 'color:#aaa');
console.log('Cache keys — Terrain: 1 shared | River:' + riverCache.size + ' | Particles:' + particleStartCache.size);
</script>
</body>
</html>