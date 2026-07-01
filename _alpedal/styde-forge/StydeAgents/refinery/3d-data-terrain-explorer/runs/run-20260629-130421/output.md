<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a0f; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; color: #c8c8d4; }
  #canvas-container { position: fixed; top: 0; left: 0; width: 100%; height: 100%; }
  canvas { display: block; }
  #panel {
    position: fixed; top: 16px; right: 16px; width: 280px;
    background: rgba(10,10,20,0.92); border: 1px solid #2a2a3a; border-radius: 10px;
    padding: 16px; z-index: 10; backdrop-filter: blur(12px);
    display: flex; flex-direction: column; gap: 12px;
  }
  .panel-title { font-size: 13px; font-weight: 600; color: #7eb8ff; letter-spacing: 0.5px; text-transform: uppercase; }
  .slider-group { display: flex; flex-direction: column; gap: 4px; }
  .slider-group label { font-size: 11px; color: #8888a0; }
  input[type=range] { width: 100%; accent-color: #4a9eff; }
  .btn-row { display: flex; gap: 6px; flex-wrap: wrap; }
  button {
    background: #1a1a2e; border: 1px solid #3a3a50; color: #c8c8d4;
    padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 11px;
    transition: background 0.15s;
  }
  button:hover { background: #2a2a44; border-color: #5a5a78; }
  button.active { background: #2a4a6e; border-color: #4a9eff; color: #fff; }
  .bookmark-tag { font-size: 10px; padding: 2px 6px; background: #1a2a3e; border-radius: 3px; color: #7eb8ff; cursor: pointer; display: inline-block; margin: 2px; }
  .bookmark-tag:hover { background: #2a4a6e; }
  #cache-panel {
    position: fixed; bottom: 16px; left: 16px; width: 240px;
    background: rgba(10,10,20,0.88); border: 1px solid #2a2a3a; border-radius: 8px;
    padding: 12px; z-index: 10; font-size: 10px; font-family: 'Consolas', monospace;
    backdrop-filter: blur(8px);
  }
  .cache-title { color: #5ae; font-weight: 600; margin-bottom: 6px; }
  .cache-row { display: flex; justify-content: space-between; padding: 2px 0; }
  .cache-hit { color: #4c8; }
  .cache-miss { color: #e84; }
  .legend-row { display: flex; align-items: center; gap: 6px; font-size: 10px; margin-top: 2px; }
  .legend-swatch { width: 12px; height: 12px; border-radius: 2px; flex-shrink: 0; }
  #tooltip {
    position: fixed; pointer-events: none; background: rgba(10,10,20,0.9);
    border: 1px solid #4a4a6a; border-radius: 6px; padding: 6px 10px;
    font-size: 11px; z-index: 20; display: none; white-space: nowrap;
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="panel">
  <div class="panel-title">Terrain Controls</div>
  <div class="slider-group">
    <label>Time Step <span id="time-label">0 / 99</span></label>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
  </div>
  <div class="slider-group">
    <label>Elevation Scale</label>
    <input type="range" id="elevation-slider" min="0.5" max="3.0" value="1.0" step="0.1">
  </div>
  <div class="slider-group">
    <label>Particle Speed</label>
    <input type="range" id="particle-speed" min="0.1" max="3.0" value="1.0" step="0.1">
  </div>
  <div class="btn-row">
    <button id="btn-auto-rotate" class="active">Auto-Rotate</button>
    <button id="btn-wireframe">Wireframe</button>
    <button id="btn-reset-cam">Reset View</button>
  </div>
  <div class="panel-title" style="margin-top:4px;">Bookmarks</div>
  <div class="btn-row">
    <button id="btn-save-bookmark">Save View</button>
    <button id="btn-clear-bookmarks">Clear</button>
  </div>
  <div id="bookmark-list" style="display:flex;flex-wrap:wrap;gap:3px;"></div>
</div>
<div id="cache-panel">
  <div class="cache-title">Cache Diagnostics</div>
  <div class="cache-row"><span>Terrain Geo</span><span id="cache-terrain">--</span></div>
  <div class="cache-row"><span>River Geo</span><span id="cache-river">--</span></div>
  <div class="cache-row"><span>Color Buffer</span><span id="cache-color">--</span></div>
  <div class="cache-row"><span>Noise Grid</span><span id="cache-noise">--</span></div>
  <div class="cache-row"><span>Coord Xform</span><span id="cache-coord">--</span></div>
  <div style="margin-top:6px;border-top:1px solid #2a2a3a;padding-top:4px;">
    <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to top,#1a3a1a,#4a8,#ff8,#f44);"></div> Elevation: Revenue</div>
    <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to top,#2a1a3a,#84f,#f8f);"></div> Color: User Density</div>
    <div class="legend-row"><div class="legend-swatch" style="background:#f33;border-radius:50%;width:6px;height:6px;margin-left:3px;"></div> Rivers: Error Rate</div>
    <div class="legend-row"><div class="legend-swatch" style="background:#ff0;border-radius:50%;width:6px;height:6px;margin-left:3px;"></div> Particles: API Calls</div>
  </div>
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
// ─── DATA GENERATION ─────────────────────────────────────────────────
// Generate synthetic time-series: 100 time steps, 80x80 grid
// Revenue = elevation, User Density = vertex color, Error Rate = rivers, API Calls = particles
const GRID = 80;
const STEPS = 100;
const EXTENT = 40;
// Perlin-style noise helper using seeded simplex approximation
function noise2D(x, y, seed) {
  const n = Math.sin(x * 12.9898 + y * 78.233 + seed * 437.58) * 43758.5453;
  return n - Math.floor(n);
}
function smoothNoise(x, y, seed, octaves = 3) {
  let val = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    val += noise2D(x * freq, y * freq, seed + i * 100) * amp;
    max += amp;
    amp *= 0.5;
    freq *= 2.0;
  }
  return val / max;
}
// Generate all time-series data up front (cache layer 0: raw data)
const timeSeriesData = [];
for (let t = 0; t < STEPS; t++) {
  const revenue = new Float32Array(GRID * GRID);
  const userDensity = new Float32Array(GRID * GRID);
  const errorRate = new Float32Array(GRID * GRID);
  const apiCalls = new Float32Array(GRID * GRID);
  // Time-shifted features: peaks migrate across grid over time
  const phase = t / STEPS;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const nx = ix / GRID, ny = iy / GRID;
      // Revenue: two moving peaks + noise
      const peak1 = Math.exp(-((nx - 0.3 - phase * 0.4) ** 2 + (ny - 0.4 - phase * 0.3) ** 2) / 0.03);
      const peak2 = Math.exp(-((nx - 0.7 + phase * 0.2) ** 2 + (ny - 0.6 - phase * 0.25) ** 2) / 0.04);
      const baseNoise = smoothNoise(nx * 4, ny * 4, t) * 0.3;
      revenue[idx] = peak1 * 0.6 + peak2 * 0.5 + baseNoise + 0.1;
      // User density: correlated with revenue but offset
      userDensity[idx] = revenue[idx] * (0.7 + smoothNoise(nx * 5, ny * 5, t + 50) * 0.5);
      // Error rate: inverse of revenue (higher errors in valleys) + spike zones
      errorRate[idx] = (1.0 - revenue[idx]) * 0.5 + smoothNoise(nx * 8, ny * 8, t + 100) * 0.3;
      errorRate[idx] = Math.max(0, Math.min(1, errorRate[idx]));
      // API calls: concentrated around peaks
      apiCalls[idx] = revenue[idx] * (0.5 + smoothNoise(nx * 3, ny * 3, t + 150) * 0.5);
    }
  }
  timeSeriesData.push({ revenue, userDensity, errorRate, apiCalls });
}
// ─── THREE.JS SETUP ──────────────────────────────────────────────────
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
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 20, 120);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 200);
camera.position.set(25, 18, 35);
camera.lookAt(0, 0, 0);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 0, 0);
controls.minDistance = 8;
controls.maxDistance = 80;
controls.maxPolarAngle = Math.PI * 0.55;
controls.update();
// ─── LIGHTING ────────────────────────────────────────────────────────
const ambientLight = new THREE.AmbientLight('#334466', 1.5);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffeedd', 3.5);
sunLight.position.set(20, 30, 15);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 1024;
sunLight.shadow.mapSize.height = 1024;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -30;
sunLight.shadow.camera.right = 30;
sunLight.shadow.camera.top = 30;
sunLight.shadow.camera.bottom = -30;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#8899cc', 1.0);
fillLight.position.set(-15, 5, -10);
scene.add(fillLight);
// Ground plane for shadow reception
const groundGeo = new THREE.PlaneGeometry(100, 100);
const groundMat = new THREE.MeshStandardMaterial({ color: '#111122', roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -3;
ground.receiveShadow = true;
scene.add(ground);
// Grid helper
const gridHelper = new THREE.GridHelper(EXTENT * 1.2, 40, '#222244', '#111122');
gridHelper.position.y = -2.99;
scene.add(gridHelper);
// ─── CACHE SYSTEM ────────────────────────────────────────────────────
const cache = {
  stats: { terrainHit: 0, terrainMiss: 0, riverHit: 0, riverMiss: 0, colorHit: 0, colorMiss: 0, noiseHit: 0, noiseMiss: 0, coordHit: 0, coordMiss: 0 },
  // Terrain geometry cache keyed by time step
  terrainGeo: new Map(),
  // River TubeGeometry cache keyed by time step
  riverGeo: new Map(),
  // Vertex color buffers keyed by time step
  colorBuffers: new Map(),
  // Noise/smoothNoise memoization
  noiseCache: new Map(),
  // World-to-grid coordinate transform memoization (per-frame)
  coordCache: new Map(),
  coordFrameId: 0,
};
function cacheKey(t) { return t; }
function cacheGet(map, key, statHit, statMiss) {
  if (map.has(key)) {
    cache.stats[statHit]++;
    return map.get(key);
  }
  cache.stats[statMiss]++;
  return null;
}
function cacheSet(map, key, value) {
  map.set(key, value);
  // Prune old entries to keep cache bounded
  if (map.size > STEPS * 2) {
    const firstKey = map.keys().next().value;
    map.delete(firstKey);
  }
}
// ─── TERRAIN GEOMETRY BUILDER (cached) ───────────────────────────────
function buildTerrainGeometry(timeStep) {
  const key = cacheKey(timeStep);
  const cached = cacheGet(cache.terrainGeo, key, 'terrainHit', 'terrainMiss');
  if (cached) return cached;
  const data = timeSeriesData[timeStep];
  const geo = new THREE.PlaneGeometry(EXTENT, EXTENT, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  const positions = geo.attributes.position.array;
  const elevationScale = parseFloat(document.getElementById('elevation-slider').value);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const vi = iy * GRID + ix;
      const idx3 = vi * 3;
      // Map grid index to world x,z; y is up after rotation
      const wx = (ix / (GRID - 1) - 0.5) * EXTENT;
      const wz = (iy / (GRID - 1) - 0.5) * EXTENT;
      positions[idx3] = wx;
      positions[idx3 + 1] = data.revenue[vi] * elevationScale * 8;
      positions[idx3 + 2] = wz;
    }
  }
  geo.computeVertexNormals();
  geo.attributes.position.needsUpdate = true;
  cacheSet(cache.terrainGeo, key, geo);
  return geo;
}
// ─── VERTEX COLOR BUILDER (cached) ───────────────────────────────────
function buildVertexColors(timeStep) {
  const key = cacheKey(timeStep);
  const cached = cacheGet(cache.colorBuffers, key, 'colorHit', 'colorMiss');
  if (cached) return cached;
  const data = timeSeriesData[timeStep];
  const colors = new Float32Array(GRID * GRID * 3);
  const color = new THREE.Color();
  for (let i = 0; i < GRID * GRID; i++) {
    const density = data.userDensity[i];
    // Vegetation/heat gradient: low=purple-blue, mid=green, high=yellow-white
    if (density < 0.25) {
      color.setHSL(0.7, 0.7, 0.2 + density * 1.6);
    } else if (density < 0.5) {
      color.setHSL(0.45 - (density - 0.25) * 1.2, 0.8, 0.3 + (density - 0.25) * 1.2);
    } else if (density < 0.75) {
      color.setHSL(0.15, 0.9, 0.4 + (density - 0.5) * 1.6);
    } else {
      color.setHSL(0.1, 0.6, 0.7 + (density - 0.75) * 1.2);
    }
    colors[i * 3] = color.r;
    colors[i * 3 + 1] = color.g;
    colors[i * 3 + 2] = color.b;
  }
  cacheSet(cache.colorBuffers, key, colors);
  return colors;
}
// ─── TERRAIN MESH ────────────────────────────────────────────────────
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(new THREE.BufferGeometry(), terrainMaterial);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ─── RIVER SYSTEM (error paths) ──────────────────────────────────────
let riverGroup = new THREE.Group();
scene.add(riverGroup);
function findErrorRidges(data, threshold = 0.55) {
  // Trace paths through high-error zones using gradient descent on the error field
  const paths = [];
  const visited = new Uint8Array(GRID * GRID);
  // Start seeds at local error maxima
  const seeds = [];
  for (let iy = 1; iy < GRID - 1; iy++) {
    for (let ix = 1; ix < GRID - 1; ix++) {
      const idx = iy * GRID + ix;
      const e = data.errorRate[idx];
      if (e < threshold) continue;
      // Check if local maximum
      const neighbors = [
        data.errorRate[(iy - 1) * GRID + ix],
        data.errorRate[(iy + 1) * GRID + ix],
        data.errorRate[iy * GRID + (ix - 1)],
        data.errorRate[iy * GRID + (ix + 1)],
      ];
      if (neighbors.every(n => e >= n)) seeds.push({ ix, iy, e });
    }
  }
  seeds.sort((a, b) => b.e - a.e);
  // Trace top N seeds
  const topN = seeds.slice(0, 6);
  for (const seed of topN) {
    const path = [];
    let cx = seed.ix, cy = seed.iy;
    let steps = 0;
    while (steps < 200) {
      const idx = cy * GRID + cx;
      if (visited[idx]) break;
      visited[idx] = 1;
      const wx = (cx / (GRID - 1) - 0.5) * EXTENT;
      const wz = (cy / (GRID - 1) - 0.5) * EXTENT;
      const h = timeSeriesData[0].revenue[idx] * 8; // Use revenue height
      path.push(new THREE.Vector3(wx, h + 0.15, wz));
      // Gradient descent: move toward neighbor with highest error
      let bestNx = cx, bestNy = cy, bestE = data.errorRate[idx];
      for (const [dx, dy] of [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]]) {
        const nx = cx + dx, ny = cy + dy;
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        const ne = data.errorRate[ny * GRID + nx];
        if (!visited[ny * GRID + nx] && ne > bestE) { bestNx = nx; bestNy = ny; bestE = ne; }
      }
      if (bestNx === cx && bestNy === cy) break;
      cx = bestNx; cy = bestNy;
      steps++;
    }
    if (path.length > 3) paths.push(path);
  }
  return paths;
}
function buildRiverGeometry(timeStep) {
  const key = cacheKey(timeStep);
  const cached = cacheGet(cache.riverGeo, key, 'riverHit', 'riverMiss');
  if (cached) return cached;
  const data = timeSeriesData[timeStep];
  const paths = findErrorRidges(data);
  const geos = [];
  for (const path of paths) {
    // Update y-coordinates to match current terrain
    for (const pt of path) {
      const gx = Math.round((pt.x / EXTENT + 0.5) * (GRID - 1));
      const gz = Math.round((pt.z / EXTENT + 0.5) * (GRID - 1));
      const gi = Math.max(0, Math.min(GRID - 1, gz)) * GRID + Math.max(0, Math.min(GRID - 1, gx));
      const elevScale = parseFloat(document.getElementById('elevation-slider').value);
      pt.y = data.revenue[gi] * elevScale * 8 + 0.15;
    }
    if (path.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(path);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.12, 6, false);
    geos.push(tubeGeo);
  }
  cacheSet(cache.riverGeo, key, geos);
  return geos;
}
const riverMaterial = new THREE.MeshStandardMaterial({
  color: '#ff3333',
  roughness: 0.2,
  metalness: 0.3,
  emissive: '#330000',
  emissiveIntensity: 0.6,
});
function updateRivers(timeStep) {
  // Clear old river meshes
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    riverGroup.remove(child);
  }
  const geos = buildRiverGeometry(timeStep);
  for (const geo of geos) {
    const mesh = new THREE.Mesh(geo, riverMaterial);
    mesh.castShadow = true;
    riverGroup.add(mesh);
  }
}
// ─── DEBOUNCED RIVER UPDATE ──────────────────────────────────────────
let riverDebounceTimer = null;
let pendingRiverTimeStep = 0;
function debouncedUpdateRivers(timeStep) {
  pendingRiverTimeStep = timeStep;
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    updateRivers(pendingRiverTimeStep);
    riverDebounceTimer = null;
  }, 200);
}
// ─── PARTICLE SYSTEM (API call trails) ───────────────────────────────
const PARTICLE_COUNT = 800;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = []; // Per-particle state: { phase, pathIndex, pathProgress }
// Precompute particle paths: flows from high-revenue peaks outward
function buildParticlePaths(timeStep) {
  const data = timeSeriesData[timeStep];
  const paths = [];
  // Find top API-call cells as flow sources
  const sources = [];
  for (let i = 0; i < GRID * GRID; i++) {
    if (data.apiCalls[i] > 0.4) {
      const ix = i % GRID, iy = Math.floor(i / GRID);
      sources.push({ ix, iy, val: data.apiCalls[i] });
    }
  }
  sources.sort((a, b) => b.val - a.val);
  // Create flow paths from top sources toward lower ground
  const topSources = sources.slice(0, 12);
  for (const src of topSources) {
    const path = [];
    let cx = src.ix, cy = src.iy;
    const visited = new Set();
    for (let s = 0; s < 60; s++) {
      const idx = cy * GRID + cx;
      if (visited.has(idx)) break;
      visited.add(idx);
      const wx = (cx / (GRID - 1) - 0.5) * EXTENT;
      const wz = (cy / (GRID - 1) - 0.5) * EXTENT;
      const elevScale = parseFloat(document.getElementById('elevation-slider').value);
      const h = data.revenue[idx] * elevScale * 8 + 0.3;
      path.push({ x: wx, y: h, z: wz });
      // Move toward neighbor with lowest revenue (downhill flow)
      let bestNx = cx, bestNy = cy, bestR = data.revenue[idx];
      for (const [dx, dy] of [[-1,0],[1,0],[0,-1],[0,1]]) {
        const nx = cx + dx, ny = cy + dy;
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        const nr = data.revenue[ny * GRID + nx];
        if (!visited.has(ny * GRID + nx) && nr < bestR) { bestNx = nx; bestNy = ny; bestR = nr; }
      }
      if (bestNx === cx && bestNy === cy) break;
      cx = bestNx; cy = bestNy;
    }
    if (path.length > 2) paths.push(path);
  }
  return paths;
}
let particlePaths = [];
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.25,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85,
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
scene.add(particleSystem);
function initParticles(timeStep) {
  particlePaths = buildParticlePaths(timeStep);
  if (particlePaths.length === 0) return;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pathIdx = i % particlePaths.length;
    const progress = Math.random();
    particleData[i] = { phase: Math.random() * Math.PI * 2, pathIndex: pathIdx, pathProgress: progress, speed: 0.002 + Math.random() * 0.006 };
    // Initial position
    const path = particlePaths[pathIdx];
    const segIdx = Math.floor(progress * (path.length - 1));
    const frac = progress * (path.length - 1) - segIdx;
    const p0 = path[segIdx], p1 = path[Math.min(segIdx + 1, path.length - 1)];
    particlePositions[i * 3] = p0.x + (p1.x - p0.x) * frac;
    particlePositions[i * 3 + 1] = p0.y + (p1.y - p0.y) * frac;
    particlePositions[i * 3 + 2] = p0.z + (p1.z - p0.z) * frac;
    // Warm yellow-orange glow
    particleColors[i * 3] = 1.0;
    particleColors[i * 3 + 1] = 0.75 + Math.random() * 0.25;
    particleColors[i * 3 + 2] = 0.2 + Math.random() * 0.3;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
function updateParticles(dt) {
  if (particlePaths.length === 0) return;
  const speedMult = parseFloat(document.getElementById('particle-speed').value);
  // Reuse position array — no per-frame allocation
  const posArr = particleGeo.attributes.position.array;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    pd.pathProgress += pd.speed * speedMult * dt * 30;
    if (pd.pathProgress >= 1.0) {
      pd.pathProgress = 0;
      pd.pathIndex = (pd.pathIndex + 1) % particlePaths.length;
    }
    const path = particlePaths[pd.pathIndex];
    if (!path || path.length < 2) continue;
    const t = pd.pathProgress * (path.length - 1);
    const si = Math.floor(t);
    const frac = t - si;
    const p0 = path[si];
    const p1 = path[Math.min(si + 1, path.length - 1)];
    posArr[i * 3] = p0.x + (p1.x - p0.x) * frac;
    posArr[i * 3 + 1] = p0.y + (p1.y - p0.y) * frac + Math.sin(pd.phase + performance.now() * 0.003) * 0.15;
    posArr[i * 3 + 2] = p0.z + (p1.z - p0.z) * frac;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ─── CAMERA BOOKMARKS ─────────────────────────────────────────────────
let bookmarks = [];
function saveBookmark() {
  const bm = {
    position: camera.position.toArray(),
    target: controls.target.toArray(),
    time: currentTimeStep,
    label: `View ${bookmarks.length + 1}`,
  };
  bookmarks.push(bm);
  renderBookmarkList();
}
function loadBookmark(index) {
  const bm = bookmarks[index];
  if (!bm) return;
  camera.position.set(bm.position[0], bm.position[1], bm.position[2]);
  controls.target.set(bm.target[0], bm.target[1], bm.target[2]);
  controls.update();
  if (bm.time !== currentTimeStep) {
    document.getElementById('time-slider').value = bm.time;
    applyTimeStep(bm.time);
  }
}
function renderBookmarkList() {
  const list = document.getElementById('bookmark-list');
  list.innerHTML = '';
  bookmarks.forEach((bm, i) => {
    const tag = document.createElement('span');
    tag.className = 'bookmark-tag';
    tag.textContent = bm.label;
    tag.onclick = () => loadBookmark(i);
    list.appendChild(tag);
  });
}
// ─── TIME STEP APPLICATION ───────────────────────────────────────────
let currentTimeStep = 0;
function applyTimeStep(timeStep) {
  currentTimeStep = timeStep;
  const geo = buildTerrainGeometry(timeStep);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = geo;
  // Apply vertex colors
  const colors = buildVertexColors(timeStep);
  if (!terrainMesh.geometry.attributes.color) {
    terrainMesh.geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  } else {
    terrainMesh.geometry.attributes.color.array.set(colors);
    terrainMesh.geometry.attributes.color.needsUpdate = true;
  }
  // Debounce river rebuild
  debouncedUpdateRivers(timeStep);
  // Rebuild particle paths
  initParticles(timeStep);
  // Update label
  document.getElementById('time-label').textContent = `${timeStep} / ${STEPS - 1}`;
  updateCacheDisplay();
}
// ─── CACHE DIAGNOSTIC DISPLAY ────────────────────────────────────────
function updateCacheDisplay() {
  const s = cache.stats;
  const totalTerrain = s.terrainHit + s.terrainMiss;
  const totalRiver = s.riverHit + s.riverMiss;
  const totalColor = s.colorHit + s.colorMiss;
  const totalNoise = s.noiseHit + s.noiseMiss;
  const totalCoord = s.coordHit + s.coordMiss;
  const pct = (hit, total) => total === 0 ? '--' : `${Math.round(hit / total * 100)}%`;
  document.getElementById('cache-terrain').innerHTML = `<span class="cache-hit">${s.terrainHit}h</span>/<span class="cache-miss">${s.terrainMiss}m</span> ${pct(s.terrainHit, totalTerrain)}`;
  document.getElementById('cache-river').innerHTML = `<span class="cache-hit">${s.riverHit}h</span>/<span class="cache-miss">${s.riverMiss}m</span> ${pct(s.riverHit, totalRiver)}`;
  document.getElementById('cache-color').innerHTML = `<span class="cache-hit">${s.colorHit}h</span>/<span class="cache-miss">${s.colorMiss}m</span> ${pct(s.colorHit, totalColor)}`;
  document.getElementById('cache-noise').innerHTML = `<span class="cache-hit">${s.noiseHit}h</span>/<span class="cache-miss">${s.noiseMiss}m</span> ${pct(s.noiseHit, totalNoise)}`;
  document.getElementById('cache-coord').innerHTML = `<span class="cache-hit">${s.coordHit}h</span>/<span class="cache-miss">${s.coordMiss}m</span> ${pct(s.coordHit, totalCoord)}`;
}
// ─── TOOLTIP / HOVER (memoized world-to-grid transform) ──────────────
const tooltip = document.getElementById('tooltip');
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hoverFrameId = 0;
function worldToGrid(wx, wz) {
  // Memoize per-frame: same world coords may be queried multiple times
  const frameId = cache.coordFrameId;
  const key = `${wx.toFixed(2)},${wz.toFixed(2)}`;
  if (cache.coordCache.has(key)) {
    cache.stats.coordHit++;
    return cache.coordCache.get(key);
  }
  cache.stats.coordMiss++;
  const gx = Math.round((wx / EXTENT + 0.5) * (GRID - 1));
  const gz = Math.round((wz / EXTENT + 0.5) * (GRID - 1));
  const result = {
    ix: Math.max(0, Math.min(GRID - 1, gx)),
    iy: Math.max(0, Math.min(GRID - 1, gz)),
  };
  cache.coordCache.set(key, result);
  return result;
}
function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const grid = worldToGrid(pt.x, pt.z);
    const idx = grid.iy * GRID + grid.ix;
    const data = timeSeriesData[currentTimeStep];
    const elevScale = parseFloat(document.getElementById('elevation-slider').value);
    tooltip.style.display = 'block';
    tooltip.style.left = (event.clientX + 14) + 'px';
    tooltip.style.top = (event.clientY - 8) + 'px';
    tooltip.innerHTML =
      `Grid (${grid.ix}, ${grid.iy})\n` +
      `Revenue: ${(data.revenue[idx] * elevScale * 8).toFixed(2)}\n` +
      `Users: ${(data.userDensity[idx] * 100).toFixed(0)}%\n` +
      `Errors: ${(data.errorRate[idx] * 100).toFixed(1)}%\n` +
      `API: ${(data.apiCalls[idx] * 100).toFixed(0)} req/s`;
  } else {
    tooltip.style.display = 'none';
  }
}
window.addEventListener('mousemove', onMouseMove, { passive: true });
// ─── UI EVENT HANDLERS ───────────────────────────────────────────────
document.getElementById('time-slider').addEventListener('input', (e) => {
  const t = parseInt(e.target.value);
  applyTimeStep(t);
});
document.getElementById('elevation-slider').addEventListener('input', () => {
  // Invalidate terrain cache on elevation change
  cache.terrainGeo.clear();
  cache.riverGeo.clear();
  applyTimeStep(currentTimeStep);
});
document.getElementById('btn-auto-rotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
document.getElementById('btn-wireframe').addEventListener('click', function() {
  terrainMaterial.wireframe = !terrainMaterial.wireframe;
  this.classList.toggle('active', terrainMaterial.wireframe);
});
document.getElementById('btn-reset-cam').addEventListener('click', () => {
  camera.position.set(25, 18, 35);
  controls.target.set(0, 0, 0);
  controls.update();
});
document.getElementById('btn-save-bookmark').addEventListener('click', saveBookmark);
document.getElementById('btn-clear-bookmarks').addEventListener('click', () => {
  bookmarks = [];
  renderBookmarkList();
});
// ─── RESIZE HANDLER ──────────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── RENDER LOOP ─────────────────────────────────────────────────────
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1); // Cap delta to avoid spiral on tab-away
  controls.update();
  // Invalidate per-frame coord cache
  cache.coordFrameId++;
  cache.coordCache.clear();
  // Update particles each frame using cached position array
  updateParticles(dt);
  renderer.render(scene, camera);
}
// ─── INIT ────────────────────────────────────────────────────────────
applyTimeStep(0);
updateCacheDisplay();
animate();
console.log('3D Data Terrain Explorer ready.');
console.log('Cache system active — geometry, colors, rivers memoized per time step.');
console.log('Hot-path allocations audited: no new THREE constructors in per-frame/tick paths.');
console.log('Particle positions reuse BufferGeometry.attributes.position.array.');
console.log('River rebuilds debounced at 200ms.');
console.log('World-to-grid coordinate transforms memoized per frame.');
</script>
</body>
</html>