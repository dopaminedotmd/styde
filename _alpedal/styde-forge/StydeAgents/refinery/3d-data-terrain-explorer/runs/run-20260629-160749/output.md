<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0d1117; --panel: #161b22; --border: #30363d; --text: #c9d1d9; --accent: #58a6ff; --warn: #f0883e; --good: #3fb950; --bad: #f85149; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; height: 100vh; }
  #canvas-container { position: fixed; inset: 0; z-index: 1; }
  #ui-panel { position: fixed; top: 16px; right: 16px; z-index: 10; background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 16px; width: 280px; max-height: calc(100vh - 32px); overflow-y: auto; display: flex; flex-direction: column; gap: 12px; font-size: 13px; }
  .panel-section { border-bottom: 1px solid var(--border); padding-bottom: 10px; }
  .panel-section:last-child { border-bottom: none; padding-bottom: 0; }
  label { display: block; margin-bottom: 4px; color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  input[type="range"] { width: 100%; accent-color: var(--accent); }
  .time-label { display: flex; justify-content: space-between; font-size: 12px; }
  button { background: #21262d; color: var(--text); border: 1px solid var(--border); border-radius: 4px; padding: 6px 10px; cursor: pointer; font-size: 12px; width: 100%; text-align: left; transition: background 0.15s; }
  button:hover { background: #30363d; }
  button.active { border-color: var(--accent); background: #1f2a3a; }
  .stat-row { display: flex; justify-content: space-between; padding: 2px 0; font-size: 11px; font-family: 'Cascadia Code', 'Fira Code', monospace; }
  .stat-val { color: var(--accent); }
  .stat-hit { color: var(--good); }
  .stat-miss { color: var(--warn); }
  .legend { display: flex; gap: 12px; flex-wrap: wrap; font-size: 10px; }
  .legend-item { display: flex; align-items: center; gap: 4px; }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
  h3 { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #8b949e; margin-bottom: 6px; }
  #cache-panel { font-size: 10px; }
  .metric-bar { height: 4px; border-radius: 2px; margin-top: 2px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-panel">
  <div class="panel-section">
    <h3>Time</h3>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <div class="time-label"><span id="time-current">Day 1</span><span id="time-total">Day 100</span></div>
    <div style="display:flex;gap:4px;margin-top:4px;">
      <button id="btn-play" style="flex:1;text-align:center;">Play</button>
      <button id="btn-pause" style="flex:1;text-align:center;">Pause</button>
    </div>
  </div>
  <div class="panel-section">
    <h3>Bookmarks</h3>
    <div id="bookmark-list" style="display:flex;flex-direction:column;gap:4px;"></div>
    <button id="btn-save-bookmark" style="margin-top:4px;">Save Current View</button>
  </div>
  <div class="panel-section">
    <h3>Legend</h3>
    <div class="legend">
      <div class="legend-item"><span class="legend-dot" style="background:#3fb950;"></span> Revenue (elevation)</div>
      <div class="legend-item"><span class="legend-dot" style="background:#f85149;"></span> Error rivers</div>
      <div class="legend-item"><span class="legend-dot" style="background:#58a6ff;"></span> API trails</div>
      <div class="legend-item"><span class="legend-dot" style="background:linear-gradient(135deg,#1a3a1a,#ffdd57);"></span> User density (color)</div>
    </div>
  </div>
  <div class="panel-section" id="cache-panel">
    <h3>Cache Diagnostics</h3>
    <div id="cache-stats"></div>
  </div>
</div>
<script type="importmap">
{ "imports": { "three": "https://unpkg.com/three@0.160.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/" } }
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// Cache manager with hit/miss tracking
class CacheManager {
  constructor() {
    this.store = new Map();
    this.stats = { hits: 0, misses: 0, stores: 0, keys: 0 };
  }
  get(key) {
    if (this.store.has(key)) { this.stats.hits++; return this.store.get(key); }
    this.stats.misses++; return null;
  }
  set(key, value) {
    if (!this.store.has(key)) this.stats.keys++;
    this.stats.stores++;
    this.store.set(key, value);
    return value;
  }
  has(key) { return this.store.has(key); }
  getStats() {
    const total = this.stats.hits + this.stats.misses;
    return { ...this.stats, total, hitRate: total ? ((this.stats.hits / total) * 100).toFixed(1) : '0.0' };
  }
}
// World-to-grid memoization with bounded LRU
class GridMemo {
  constructor(capacity = 256) {
    this.cache = new Map();
    this.capacity = capacity;
    this.hits = 0;
    this.misses = 0;
  }
  getKey(wx, wz) {
    // Quantize to reduce cache churn from floating point drift
    return `${wx.toFixed(4)},${wz.toFixed(4)}`;
  }
  get(wx, wz) {
    const key = this.getKey(wx, wz);
    if (this.cache.has(key)) { this.hits++; return this.cache.get(key); }
    this.misses++; return null;
  }
  set(wx, wz, value) {
    const key = this.getKey(wx, wz);
    if (this.cache.size >= this.capacity) {
      // Evict oldest entry
      const first = this.cache.keys().next().value;
      this.cache.delete(first);
    }
    this.cache.set(key, value);
    return value;
  }
  getStats() { return { hits: this.hits, misses: this.misses }; }
}
const gridMemo = new GridMemo();
// Generate synthetic time-series data
// Grid: 80x80, Time steps: 100
const GRID = 80;
const STEPS = 100;
const WIDTH = 20; // world width
function generateDataset() {
  // Simple pseudo-random with seed for reproducibility
  function seeded(seed) {
    let s = seed;
    return () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
  }
  const rng = seeded(42);
  // Base terrain shape: two hills + valley
  const elevation0 = new Float32Array(GRID * GRID);
  const users0 = new Float32Array(GRID * GRID);
  const errors0 = new Float32Array(GRID * GRID);
  const api0 = new Float32Array(GRID * GRID);
  const cx1 = GRID * 0.35, cz1 = GRID * 0.4, r1 = GRID * 0.25;
  const cx2 = GRID * 0.65, cz2 = GRID * 0.6, r2 = GRID * 0.2;
  const cx3 = GRID * 0.5, cz3 = GRID * 0.5, r3 = GRID * 0.15; // valley/error hotspot
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      // Two Gaussian hills for revenue
      const d1 = Math.sqrt((ix - cx1) ** 2 + (iz - cz1) ** 2) / r1;
      const d2 = Math.sqrt((ix - cx2) ** 2 + (iz - cz2) ** 2) / r2;
      const d3 = Math.sqrt((ix - cx3) ** 2 + (iz - cz3) ** 2) / r3;
      const hill1 = Math.exp(-d1 * d1) * 0.7;
      const hill2 = Math.exp(-d2 * d2) * 0.5;
      const valley = Math.exp(-d3 * d3) * 0.3;
      elevation0[idx] = hill1 + hill2 - valley * 0.5 + 0.1;
      // User density correlates with elevation but with noise
      users0[idx] = (hill1 * 0.6 + hill2 * 0.4 + rng() * 0.2);
      // Errors concentrate in the valley between hills
      errors0[idx] = valley * 0.8 + rng() * 0.15;
      // API traffic follows users
      api0[idx] = users0[idx] * (0.5 + rng() * 0.5);
    }
  }
  // Normalize
  const norm = (arr) => {
    let min = Infinity, max = -Infinity;
    for (let i = 0; i < arr.length; i++) { if (arr[i] < min) min = arr[i]; if (arr[i] > max) max = arr[i]; }
    const range = max - min || 1;
    for (let i = 0; i < arr.length; i++) arr[i] = (arr[i] - min) / range;
  };
  norm(elevation0);
  norm(users0);
  norm(errors0);
  norm(api0);
  // Generate time series by evolving from base
  const data = [];
  for (let t = 0; t < STEPS; t++) {
    const phase = t / STEPS;
    const elevation = new Float32Array(GRID * GRID);
    const users = new Float32Array(GRID * GRID);
    const errors = new Float32Array(GRID * GRID);
    const api = new Float32Array(GRID * GRID);
    for (let i = 0; i < GRID * GRID; i++) {
      // Revenue grows over time, seasonal oscillation
      const seasonal = Math.sin(phase * Math.PI * 4) * 0.15;
      const trend = phase * 0.3;
      elevation[i] = Math.max(0, Math.min(1, elevation0[i] + trend + seasonal * elevation0[i]));
      // User base grows
      users[i] = Math.max(0, Math.min(1, users0[i] + trend * 0.5));
      // Errors spike mid-period then get fixed
      const errorPhase = Math.sin(phase * Math.PI * 2) * 0.3;
      errors[i] = Math.max(0, Math.min(1, errors0[i] + errorPhase * errors0[i] - trend * 0.15));
      // API traffic grows
      api[i] = Math.max(0, Math.min(1, api0[i] + trend * 0.6 + seasonal * 0.1));
    }
    data.push({ elevation, users, errors, api, time: t });
  }
  return data;
}
const dataset = generateDataset();
// Cache manager instance
const cache = new CacheManager();
// Build terrain geometry for a given time step
function buildTerrainGeometry(step) {
  const cacheKey = `terrain_geom_${step}`;
  const cached = cache.get(cacheKey);
  if (cached) return cached;
  const { elevation, users } = dataset[step];
  const geo = new THREE.PlaneGeometry(WIDTH, WIDTH, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2); // lay flat on XZ
  const pos = geo.attributes.position;
  const colorsArr = new Float32Array(pos.count * 3);
  // Elevation scale
  const heightScale = 4.0;
  const hw = WIDTH / 2;
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i);
    const z = pos.getZ(i);
    // Map world position to grid index
    const gx = Math.round(((x + hw) / WIDTH) * (GRID - 1));
    const gz = Math.round(((z + hw) / WIDTH) * (GRID - 1));
    const idx = Math.min(Math.max(gz, 0), GRID - 1) * GRID + Math.min(Math.max(gx, 0), GRID - 1);
    const h = elevation[idx] * heightScale;
    pos.setY(i, h);
    // Vertex colors from user density: cool green (low) to warm yellow (high)
    const u = users[idx];
    colorsArr[i * 3] = 0.1 + u * 0.5;       // R
    colorsArr[i * 3 + 1] = 0.2 + u * 0.7;   // G
    colorsArr[i * 3 + 2] = 0.1 + (1 - u) * 0.15; // B
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
  geo.computeVertexNormals();
  geo.attributes.position.needsUpdate = true;
  cache.set(cacheKey, geo);
  return geo;
}
// Weighted gradient descent for river pathfinding
// Uses: 70% elevation descent, 20% error gradient, 10% random perturbation
function traceRiverPath(startGX, startGZ, step, maxSteps = 200) {
  const { elevation, errors } = dataset[step];
  const points = [];
  let gx = startGX, gz = startGZ;
  const visited = new Set();
  for (let s = 0; s < maxSteps; s++) {
    // Clamp to grid
    gx = Math.max(1, Math.min(GRID - 2, Math.round(gx)));
    gz = Math.max(1, Math.min(GRID - 2, Math.round(gz)));
    const key = `${gx},${gz}`;
    if (visited.has(key)) break;
    visited.add(key);
    const idx = gz * GRID + gx;
    const hw = WIDTH / 2;
    const wx = (gx / (GRID - 1)) * WIDTH - hw;
    const wz = (gz / (GRID - 1)) * WIDTH - hw;
    const wy = elevation[idx] * 4.0 + 0.05;
    points.push(new THREE.Vector3(wx, wy, wz));
    // Sample 8 neighbors for weighted gradient
    const dirs = [
      [-1, -1], [0, -1], [1, -1],
      [-1, 0],           [1, 0],
      [-1, 1],  [0, 1],  [1, 1]
    ];
    let bestScore = Infinity;
    let bestDGX = 0, bestDGZ = 0;
    const candidates = [];
    for (const [dx, dz] of dirs) {
      const nx = gx + dx, nz = gz + dz;
      if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
      const nidx = nz * GRID + nx;
      // Weighted score: 70% elevation descent, 20% error gradient favor, 10% random
      const elevScore = elevation[nidx] * 0.7;
      const errScore = (1 - errors[nidx]) * 0.2; // prefer higher errors (lower score)
      const randScore = Math.random() * 0.1;
      const score = elevScore + errScore + randScore;
      candidates.push({ dx, dz, score });
      if (score < bestScore) {
        bestScore = score;
        bestDGX = dx;
        bestDGZ = dz;
      }
    }
    // Randomized perturbation: occasionally pick second-best for organic meanders
    if (candidates.length > 1 && Math.random() < 0.2) {
      candidates.sort((a, b) => a.score - b.score);
      const pick = candidates[Math.floor(Math.random() * Math.min(3, candidates.length))];
      bestDGX = pick.dx;
      bestDGZ = pick.dz;
    }
    // Check if we've reached a local minimum (flat area or edge)
    const currentElev = elevation[idx];
    const nextIdx = (gz + bestDGZ) * GRID + (gx + bestDGX);
    if (nextIdx >= 0 && nextIdx < GRID * GRID) {
      if (elevation[nextIdx] >= currentElev && points.length > 10) break; // reached basin
    }
    gx += bestDGX;
    gz += bestDGZ;
  }
  return points;
}
// Build river geometry (cached per time step)
function buildRiverGeometry(step) {
  const cacheKey = `river_geom_${step}`;
  const cached = cache.get(cacheKey);
  if (cached) return cached;
  const group = new THREE.Group();
  const { errors } = dataset[step];
  // Find error hotspots as river sources (top 5% error regions)
  const threshold = 0.7;
  const sources = [];
  for (let iz = 0; iz < GRID; iz += 8) {
    for (let ix = 0; ix < GRID; ix += 8) {
      if (errors[iz * GRID + ix] > threshold) {
        sources.push([ix, iz]);
        if (sources.length >= 6) break;
      }
    }
    if (sources.length >= 6) break;
  }
  // Fallback sources
  if (sources.length === 0) {
    sources.push([Math.floor(GRID * 0.35), Math.floor(GRID * 0.4)]);
    sources.push([Math.floor(GRID * 0.5), Math.floor(GRID * 0.5)]);
    sources.push([Math.floor(GRID * 0.65), Math.floor(GRID * 0.6)]);
  }
  const riverMat = new THREE.MeshStandardMaterial({
    color: 0xf85149,
    emissive: 0x330000,
    roughness: 0.4,
    metalness: 0.1,
    transparent: true,
    opacity: 0.85
  });
  for (const [sx, sz] of sources) {
    const pathPoints = traceRiverPath(sx, sz, step);
    if (pathPoints.length < 3) continue;
    // Create a simple ribbon along the path
    const curve = new THREE.CatmullRomCurve3(pathPoints, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, Math.min(pathPoints.length * 2, 100), 0.08, 6, false);
    const mesh = new THREE.Mesh(tubeGeo, riverMat);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    group.add(mesh);
  }
  cache.set(cacheKey, group);
  return group;
}
// Build particle system for API flow trails
// Particles reuse position array — no per-frame allocations
function buildParticleSystem(step) {
  const { api } = dataset[step];
  const count = 500;
  const positions = new Float32Array(count * 3);
  const velocities = new Float32Array(count * 3); // stored direction
  const lifetimes = new Float32Array(count);
  const hw = WIDTH / 2;
  // Seed particles in high-API zones
  const candidates = [];
  for (let i = 0; i < GRID * GRID; i++) {
    if (api[i] > 0.4) candidates.push(i);
  }
  for (let i = 0; i < count; i++) {
    const srcIdx = candidates[Math.floor(Math.random() * candidates.length)];
    const gx = srcIdx % GRID;
    const gz = Math.floor(srcIdx / GRID);
    const wx = (gx / (GRID - 1)) * WIDTH - hw;
    const wz = (gz / (GRID - 1)) * WIDTH - hw;
    positions[i * 3] = wx;
    positions[i * 3 + 1] = api[srcIdx] * 4.0 + 0.3;
    positions[i * 3 + 2] = wz;
    // Random initial velocity direction (flow downhill-ish)
    const angle = Math.random() * Math.PI * 2;
    velocities[i * 3] = Math.cos(angle) * 0.3;
    velocities[i * 3 + 1] = -0.1 - Math.random() * 0.2;
    velocities[i * 3 + 2] = Math.sin(angle) * 0.3;
    lifetimes[i] = Math.random() * 3;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  // Store velocities and lifetimes as user data for reuse
  geo.userData = { velocities, lifetimes, api, count };
  const mat = new THREE.PointsMaterial({
    color: 0x58a6ff,
    size: 0.08,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7
  });
  const points = new THREE.Points(geo, mat);
  return points;
}
// Update particles — reuse position array, no allocations
function updateParticles(points, step, dt) {
  const geo = points.geometry;
  const { velocities, lifetimes, api, count } = geo.userData;
  const positions = geo.attributes.position.array;
  const { elevation } = dataset[step];
  const hw = WIDTH / 2;
  for (let i = 0; i < count; i++) {
    lifetimes[i] -= dt;
    if (lifetimes[i] <= 0) {
      // Respawn at high-API zone
      let gx, gz;
      do {
        gx = Math.floor(Math.random() * GRID);
        gz = Math.floor(Math.random() * GRID);
      } while (api && api[gz * GRID + gx] < 0.3);
      const wx = (gx / (GRID - 1)) * WIDTH - hw;
      const wz = (gz / (GRID - 1)) * WIDTH - hw;
      positions[i * 3] = wx;
      positions[i * 3 + 2] = wz;
      // Snap Y to terrain height
      const idx = gz * GRID + gx;
      positions[i * 3 + 1] = elevation[idx] * 4.0 + 0.3;
      const angle = Math.random() * Math.PI * 2;
      velocities[i * 3] = Math.cos(angle) * 0.3;
      velocities[i * 3 + 1] = -0.1 - Math.random() * 0.2;
      velocities[i * 3 + 2] = Math.sin(angle) * 0.3;
      lifetimes[i] = 2 + Math.random() * 4;
    } else {
      // Move particle — reuse array, no allocation
      positions[i * 3] += velocities[i * 3] * dt;
      positions[i * 3 + 1] += velocities[i * 3 + 1] * dt;
      positions[i * 3 + 2] += velocities[i * 3 + 2] * dt;
      // Clamp to terrain surface + small offset
      const wx = positions[i * 3];
      const wz = positions[i * 3 + 2];
      const gx = Math.round(((wx + hw) / WIDTH) * (GRID - 1));
      const gz = Math.round(((wz + hw) / WIDTH) * (GRID - 1));
      if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
        const terrainH = elevation[gz * GRID + gx] * 4.0;
        if (positions[i * 3 + 1] < terrainH + 0.1) {
          positions[i * 3 + 1] = terrainH + 0.1;
          velocities[i * 3 + 1] = Math.abs(velocities[i * 3 + 1]) * 0.5; // bounce
        }
      }
    }
  }
  geo.attributes.position.needsUpdate = true;
}
// Scene setup
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d1117);
scene.fog = new THREE.Fog(0x0d1117, 15, 50);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(12, 10, 14);
camera.lookAt(0, 1.5, 0);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
// Lighting
const ambientLight = new THREE.AmbientLight(0x334466, 1.5);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
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
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x8899cc, 0.8);
fillLight.position.set(-5, 3, -8);
scene.add(fillLight);
// Grid helper
const gridHelper = new THREE.GridHelper(WIDTH, 40, 0x30363d, 0x1a1f2a);
gridHelper.position.y = 0.01;
scene.add(gridHelper);
// Scene objects (mutable references)
let terrainMesh = null;
let riverGroup = null;
let particleSystem = null;
let currentStep = 0;
// Build full scene for a time step
function buildScene(step) {
  // Remove old objects
  if (terrainMesh) { terrainMesh.geometry.dispose(); terrainMesh.material.dispose(); scene.remove(terrainMesh); }
  if (riverGroup) {
    riverGroup.traverse(child => { if (child.geometry) child.geometry.dispose(); if (child.material) child.material.dispose(); });
    scene.remove(riverGroup);
  }
  if (particleSystem) { particleSystem.geometry.dispose(); particleSystem.material.dispose(); scene.remove(particleSystem); }
  // Terrain
  const terrainGeo = buildTerrainGeometry(step);
  // Sort cache key for terrain material — only allocate once, reuse
  let terrainMat = cache.get('terrain_material');
  if (!terrainMat) {
    terrainMat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.75,
      metalness: 0.05,
      flatShading: false
    });
    cache.set('terrain_material', terrainMat);
  }
  terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Rivers
  riverGroup = buildRiverGeometry(step);
  scene.add(riverGroup);
  // Particles (fresh system per step — positions reset to step data)
  particleSystem = buildParticleSystem(step);
  scene.add(particleSystem);
  currentStep = step;
}
// Bookmark system with time-based lerp
const bookmarks = [];
let bookmarkTransition = null; // { from, to, duration, elapsed }
function saveBookmark(name) {
  bookmarks.push({
    name,
    position: camera.position.clone(),
    target: controls.target.clone()
  });
  renderBookmarkList();
}
function gotoBookmark(index, duration = 1.2) {
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  bookmarkTransition = {
    fromPos: camera.position.clone(),
    fromTarget: controls.target.clone(),
    toPos: bm.position.clone(),
    toTarget: bm.target.clone(),
    duration,
    elapsed: 0
  };
  controls.autoRotate = false;
  // Re-enable auto-rotate after transition
  setTimeout(() => { controls.autoRotate = true; }, duration * 1000 + 200);
}
function updateBookmarkTransition(dt) {
  if (!bookmarkTransition) return;
  bookmarkTransition.elapsed += dt;
  const t = Math.min(bookmarkTransition.elapsed / bookmarkTransition.duration, 1.0);
  // Time-based lerp — guarantees arrival at t=1
  camera.position.lerpVectors(bookmarkTransition.fromPos, bookmarkTransition.toPos, t);
  controls.target.lerpVectors(bookmarkTransition.fromTarget, bookmarkTransition.toTarget, t);
  controls.update();
  if (t >= 1.0) bookmarkTransition = null;
}
function renderBookmarkList() {
  const list = document.getElementById('bookmark-list');
  list.innerHTML = bookmarks.map((bm, i) =>
    `<button class="bm-btn" data-index="${i}">${i + 1}. ${bm.name}</button>`
  ).join('');
  // Attach event listeners
  list.querySelectorAll('.bm-btn').forEach(btn => {
    btn.addEventListener('click', () => gotoBookmark(parseInt(btn.dataset.index)));
  });
}
// Default bookmarks
function initDefaultBookmarks() {
  const defaults = [
    { name: 'Overview', pos: [12, 10, 14], target: [0, 1.5, 0] },
    { name: 'Hill 1 Closeup', pos: [3, 4, -2], target: [-2, 1.2, -1.5] },
    { name: 'Valley (Errors)', pos: [2, 2.5, 2], target: [0, 0.8, 0] },
    { name: 'Hill 2 Top', pos: [4, 5, 5], target: [3, 1.5, 2] },
  ];
  bookmarks.length = 0;
  for (const d of defaults) {
    bookmarks.push({
      name: d.name,
      position: new THREE.Vector3(...d.pos),
      target: new THREE.Vector3(...d.target)
    });
  }
  renderBookmarkList();
}
// UI bindings
const timeSlider = document.getElementById('time-slider');
const timeCurrent = document.getElementById('time-current');
const timeTotal = document.getElementById('time-total');
const btnPlay = document.getElementById('btn-play');
const btnPause = document.getElementById('btn-pause');
const btnSaveBookmark = document.getElementById('btn-save-bookmark');
const cacheStats = document.getElementById('cache-stats');
timeTotal.textContent = `Day ${STEPS}`;
let isPlaying = false;
let lastDebounceTime = 0;
const DEBOUNCE_MS = 200;
// Debounced time change
function setTimeStep(step) {
  const now = performance.now() / 1000;
  // Debounce: skip if within cooldown (except for initial load and manual exact stop)
  if (now - lastDebounceTime < DEBOUNCE_MS / 1000 && step !== currentStep && document.activeElement === timeSlider) {
    // Schedule trailing call
    if (window._debounceTimer) clearTimeout(window._debounceTimer);
    window._debounceTimer = setTimeout(() => setTimeStepImmediate(step), DEBOUNCE_MS);
    return;
  }
  lastDebounceTime = now;
  setTimeStepImmediate(step);
}
function setTimeStepImmediate(step) {
  if (step === currentStep) return;
  // Only rebuild if terrain data changed (swap buffer approach)
  // For simplicity, full rebuild with cached geometries
  const geo = buildTerrainGeometry(step); // will hit cache after first build
  if (terrainMesh && terrainMesh.geometry !== geo) {
    terrainMesh.geometry = geo;
    terrainMesh.geometry.computeVertexNormals();
  }
  // Update rivers — cached per step
  if (riverGroup) {
    riverGroup.traverse(child => { if (child.geometry) child.geometry.dispose(); if (child.material) child.material.dispose(); });
    scene.remove(riverGroup);
  }
  riverGroup = buildRiverGeometry(step);
  scene.add(riverGroup);
  // Reset particles to step state
  if (particleSystem) { particleSystem.geometry.dispose(); particleSystem.material.dispose(); scene.remove(particleSystem); }
  particleSystem = buildParticleSystem(step);
  scene.add(particleSystem);
  currentStep = step;
  timeSlider.value = step;
  timeCurrent.textContent = `Day ${step + 1}`;
}
timeSlider.addEventListener('input', () => {
  setTimeStep(parseInt(timeSlider.value));
});
btnPlay.addEventListener('click', () => { isPlaying = true; });
btnPause.addEventListener('click', () => { isPlaying = false; });
btnSaveBookmark.addEventListener('click', () => {
  const name = `View ${bookmarks.length + 1}`;
  saveBookmark(name);
});
// Update cache stats display
function updateCacheDisplay() {
  const stats = cache.getStats();
  const memoStats = gridMemo.getStats();
  cacheStats.innerHTML = `
    <div class="stat-row"><span>Terrain builds</span><span class="stat-val">${stats.stores}</span></div>
    <div class="stat-row"><span>Cache hits</span><span class="stat-hit">${stats.hits}</span></div>
    <div class="stat-row"><span>Cache misses</span><span class="stat-miss">${stats.misses}</span></div>
    <div class="stat-row"><span>Hit rate</span><span class="stat-val">${stats.hitRate}%</span></div>
    <div class="stat-row"><span>Grid memo hits</span><span class="stat-hit">${memoStats.hits}</span></div>
    <div class="stat-row"><span>Grid memo misses</span><span class="stat-miss">${memoStats.misses}</span></div>
  `;
}
// Animation loop
const clock = new THREE.Clock();
let playAccum = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  // Play mode
  if (isPlaying) {
    playAccum += dt;
    const stepDuration = 0.5; // seconds per time step
    if (playAccum >= stepDuration) {
      playAccum -= stepDuration;
      const nextStep = (currentStep + 1) % STEPS;
      setTimeStepImmediate(nextStep);
    }
  }
  // Bookmark transition (time-based lerp)
  updateBookmarkTransition(dt);
  controls.update();
  // Update particles — reuse position arrays
  if (particleSystem && !bookmarkTransition) {
    updateParticles(particleSystem, currentStep, dt);
  }
  renderer.render(scene, camera);
  // Update diagnostics every second
  if (Math.floor(performance.now() / 1000) !== Math.floor((performance.now() - dt * 1000) / 1000)) {
    updateCacheDisplay();
  }
}
// Handle resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r': controls.autoRotate = !controls.autoRotate; break;
    case 'f': gotoBookmark(0); break; // Overview
    case '1': gotoBookmark(0); break;
    case '2': if (bookmarks.length > 1) gotoBookmark(1); break;
    case '3': if (bookmarks.length > 2) gotoBookmark(2); break;
    case '4': if (bookmarks.length > 3) gotoBookmark(3); break;
    case ' ': e.preventDefault(); isPlaying = !isPlaying; break;
    case 'arrowleft': setTimeStep(Math.max(0, currentStep - 1)); break;
    case 'arrowright': setTimeStep(Math.min(STEPS - 1, currentStep + 1)); break;
  }
});
// Initialize
initDefaultBookmarks();
buildScene(0);
updateCacheDisplay();
animate();
// Log startup
console.log('3D Data Terrain Explorer ready');
console.log(`Grid: ${GRID}x${GRID}, Time steps: ${STEPS}`);
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan, R=toggle auto-rotate');
console.log('Bookmarks: press 1-4, F=overview, Space=play/pause');
console.log('Performance: cached geometries, debounced time slider, reused particle arrays');
</script>
</body>
</html>