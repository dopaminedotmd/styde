<html>
<head>
<meta charset="UTF-8">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a0f;--panel:#12121a;--text:#c8ccd4;--accent:#5b9bd5;--warn:#d46a4e;--good:#4caf84;}
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;overflow:hidden;height:100vh;}
  #canvas-container{position:fixed;inset:0;z-index:1;}
  canvas{display:block;}
  #hud{position:fixed;top:12px;left:12px;z-index:10;display:flex;flex-direction:column;gap:6px;pointer-events:none;}
  #hud>*{pointer-events:auto;}
  .hud-block{background:var(--panel);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:8px 12px;font-size:12px;}
  .hud-row{display:flex;gap:16px;align-items:center;white-space:nowrap;}
  .metric-label{color:#7a7f8a;font-size:10px;text-transform:uppercase;letter-spacing:0.5px;}
  .metric-value{font-variant-numeric:tabular-nums;font-size:14px;font-weight:600;}
  .metric-value.good{color:var(--good);}
  .metric-value.warn{color:var(--warn);}
  #time-panel{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;background:var(--panel);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:12px 20px;display:flex;flex-direction:column;gap:6px;min-width:360px;}
  #time-panel label{font-size:11px;color:#7a7f8a;text-transform:uppercase;letter-spacing:0.5px;}
  #time-slider{width:100%;accent-color:var(--accent);cursor:pointer;}
  #time-value{font-size:13px;font-variant-numeric:tabular-nums;}
  #bookmark-bar{display:flex;gap:4px;flex-wrap:wrap;max-width:360px;}
  .bookmark-btn{background:rgba(91,155,213,0.12);border:1px solid rgba(91,155,213,0.25);color:var(--accent);border-radius:4px;padding:3px 8px;font-size:10px;cursor:pointer;transition:all 0.15s;}
  .bookmark-btn:hover{background:rgba(91,155,213,0.25);}
  #cache-panel{position:fixed;top:12px;right:12px;z-index:10;background:var(--panel);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:8px 12px;font-size:11px;display:flex;flex-direction:column;gap:2px;}
  .cache-row{display:flex;justify-content:space-between;gap:20px;}
  .cache-hit{color:var(--good);}.cache-miss{color:var(--warn);}
  #legend{position:fixed;bottom:100px;right:16px;z-index:10;display:flex;flex-direction:column;gap:4px;}
  .legend-item{display:flex;align-items:center;gap:6px;font-size:10px;}
  .legend-swatch{width:12px;height:12px;border-radius:2px;}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hud">
  <div class="hud-block">
    <div class="hud-row">
      <div><div class="metric-label">FPS</div><div class="metric-value good" id="fps-display">--</div></div>
      <div><div class="metric-label">Triangles</div><div class="metric-value" id="tri-display">--</div></div>
      <div><div class="metric-label">Particles</div><div class="metric-value" id="particle-display">--</div></div>
      <div><div class="metric-label">Load</div><div class="metric-value good" id="load-display">--</div></div>
    </div>
  </div>
</div>
<div id="cache-panel">
  <div style="font-size:10px;color:#7a7f8a;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:2px;">Cache</div>
  <div class="cache-row"><span>Terrain</span><span id="cache-terrain">--</span></div>
  <div class="cache-row"><span>Rivers</span><span id="cache-rivers">--</span></div>
  <div class="cache-row"><span>Noise</span><span id="cache-noise">--</span></div>
  <div class="cache-row"><span>Transforms</span><span id="cache-transforms">--</span></div>
</div>
<div id="time-panel">
  <label>Time Dimension <span id="time-value">T0</span></label>
  <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
  <div id="bookmark-bar">
    <button class="bookmark-btn" data-cam="0">Overview</button>
    <button class="bookmark-btn" data-cam="1">Revenue Peak</button>
    <button class="bookmark-btn" data-cam="2">Error Valley</button>
    <button class="bookmark-btn" data-cam="3">Traffic Flow</button>
  </div>
</div>
<div id="legend">
  <div style="font-size:10px;color:#7a7f8a;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px;">Legend</div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(to right,#1a3a2a,#4caf84,#c8e6c9);"></div> Revenue (Elevation)</div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(to right,#2a1a0a,#d46a4e,#ffccbc);"></div> Error Rate (Rivers)</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#5b9bd5;"></div> API Traffic (Particles)</div>
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
// === QUICK REFERENCE: Numeric Thresholds ===
// Terrain: 128x128 grid, max 32K triangles, <5ms rebuild
// Particles: 2000 cap, vertex-shader position updates, <2ms/frame
// Rivers: 16 segments, TubeBufferGeometry cached, <1ms rebuild
// FPS target: 55+ (drops below 45 trigger quality reduction)
// Load time: <800ms initial, <200ms slider tick
// Cache hit target: >85% on slider scrub
// === DATA GENERATION: 24 time steps of synthetic metrics ===
const TIME_STEPS = 24;
const GRID_SIZE = 128;
// Generate multi-metric time-series data (lazy: computed once, cached thereafter)
let _cachedTimeSeries = null;
function generateTimeSeries() {
  if (_cachedTimeSeries) return _cachedTimeSeries;
  const data = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const revenue = new Float32Array(GRID_SIZE * GRID_SIZE);
    const users = new Float32Array(GRID_SIZE * GRID_SIZE);
    const errors = new Float32Array(GRID_SIZE * GRID_SIZE);
    const apiCalls = new Float32Array(GRID_SIZE * GRID_SIZE);
    const phase = t / TIME_STEPS * Math.PI * 2;
    for (let iy = 0; iy < GRID_SIZE; iy++) {
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const idx = iy * GRID_SIZE + ix;
        const nx = (ix / GRID_SIZE) * 2 - 1;
        const ny = (iy / GRID_SIZE) * 2 - 1;
        const dist = Math.sqrt(nx * nx + ny * ny) * 1.5;
        // Revenue: central peak that rises and shifts across time
        const cx = Math.cos(phase) * 0.3;
        const cy = Math.sin(phase) * 0.2;
        const peakDist = Math.sqrt((nx - cx) ** 2 + (ny - cy) ** 2);
        revenue[idx] = 2.5 * Math.exp(-peakDist * peakDist * 2.0) + 0.3 * Math.exp(-dist * 0.8) + 0.05 * (Math.sin(nx * 4 + phase) * Math.cos(ny * 3 + phase * 0.7));
        // Users: broader distribution, lags revenue by quarter-phase
        const ulag = phase - 0.5;
        const ucx = Math.cos(ulag) * 0.25;
        const ucy = Math.sin(ulag) * 0.15;
        const upDist = Math.sqrt((nx - ucx) ** 2 + (ny - ucy) ** 2);
        users[idx] = 1.8 * Math.exp(-upDist * upDist * 1.5) + 0.4 * Math.exp(-dist * 0.6);
        // Errors: spikes in specific regions (simulated outage zones)
        const ex = -0.4 + Math.cos(phase * 1.3) * 0.4;
        const ey = 0.3 + Math.sin(phase * 1.7) * 0.3;
        const errDist = Math.sqrt((nx - ex) ** 2 + (ny - ey) ** 2);
        errors[idx] = 0.8 * Math.exp(-errDist * errDist * 3.0) * (0.5 + 0.5 * Math.sin(t * 0.8));
        // API calls: flows along valleys in the revenue surface
        apiCalls[idx] = 0.5 + 1.5 * Math.exp(-dist * 0.5) * (0.7 + 0.3 * Math.sin(nx * 5 + phase * 2));
      }
    }
    data.push({ revenue, users, errors, apiCalls });
  }
  _cachedTimeSeries = data;
  return data;
}
// === CACHE LAYER: centralized memoization with hit/miss tracking ===
const CacheStats = {
  terrainHit: 0, terrainMiss: 0,
  riverHit: 0, riverMiss: 0,
  noiseHit: 0, noiseMiss: 0,
  transformHit: 0, transformMiss: 0,
};
function cacheGet(map, key) { return map.has(key) ? map.get(key) : null; }
function cacheSet(map, key, value) { map.set(key, value); return value; }
function updateCacheUI() {
  const fmt = (h, m) => { const t = h + m; return t ? `${Math.round(h / t * 100)}%` : '--'; };
  document.getElementById('cache-terrain').textContent = fmt(CacheStats.terrainHit, CacheStats.terrainMiss);
  document.getElementById('cache-rivers').textContent = fmt(CacheStats.riverHit, CacheStats.riverMiss);
  document.getElementById('cache-noise').textContent = fmt(CacheStats.noiseHit, CacheStats.noiseMiss);
  document.getElementById('cache-transforms').textContent = fmt(CacheStats.transformHit, CacheStats.transformMiss);
}
// World-to-grid transform cache (per-frame reuse on hover/tooltip path)
const worldToGridCache = new Map();
function worldToGrid(wx, wz) {
  const key = `${wx.toFixed(4)},${wz.toFixed(4)}`;
  const cached = cacheGet(worldToGridCache, key);
  if (cached !== null) { CacheStats.transformHit++; return cached; }
  CacheStats.transformMiss++;
  // Terrain spans [-half, half] in XZ; grid is GRID_SIZE x GRID_SIZE
  const half = 5;
  const gx = Math.floor(((wx / half) * 0.5 + 0.5) * GRID_SIZE);
  const gy = Math.floor(((wz / half) * 0.5 + 0.5) * GRID_SIZE);
  const result = { gx: Math.max(0, Math.min(GRID_SIZE - 1, gx)), gy: Math.max(0, Math.min(GRID_SIZE - 1, gy)) };
  cacheSet(worldToGridCache, key, result);
  return result;
}
// === THREE.JS SETUP ===
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
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.Fog(0x0a0a0f, 15, 40);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(8, 6, 10);
camera.lookAt(0, 1.2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 20;
controls.maxPolarAngle = Math.PI * 0.6;
controls.target.set(0, 1.2, 0);
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
// === LIGHTING ===
const ambLight = new THREE.AmbientLight(0x1a1a3a, 1.2);
scene.add(ambLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(10, 15, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -12;
sunLight.shadow.camera.right = 12;
sunLight.shadow.camera.top = 12;
sunLight.shadow.camera.bottom = -12;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);
const rimLight = new THREE.DirectionalLight(0x3355aa, 1.5);
rimLight.position.set(-5, 3, -5);
scene.add(rimLight);
// === GROUND PLANE ===
const groundGeo = new THREE.PlaneGeometry(20, 20);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x0d0d18, roughness: 0.95, metalness: 0.05 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.3;
ground.receiveShadow = true;
scene.add(ground);
// === GRID HELPER ===
const gridHelper = new THREE.PolarGridHelper(6, 32, 20, 64, 0x1a1a2a, 0x1a1a2a);
gridHelper.position.y = -0.29;
scene.add(gridHelper);
// === TERRAIN SYSTEM with dirty-flag gating ===
let terrainMesh = null;
let currentTimeIndex = -1;
let heightmapDirty = true; // dirty flag: skip rebuild when heightmap unchanged
// Cache: pre-built geometry variants by time index
const terrainGeoCache = new Map();
function buildTerrainGeometry(timeIndex) {
  const cached = cacheGet(terrainGeoCache, timeIndex);
  if (cached !== null) { CacheStats.terrainHit++; return cached; }
  CacheStats.terrainMiss++;
  const ts = generateTimeSeries();
  const step = ts[timeIndex];
  const geo = new THREE.PlaneGeometry(10, 10, GRID_SIZE - 1, GRID_SIZE - 1);
  geo.rotateX(-Math.PI / 2);
  const positions = geo.attributes.position.array;
  const colors = new Float32Array(positions.length);
  // Vegetation gradient: map user density to green intensity
  for (let i = 0; i < positions.length; i += 3) {
    const ix = Math.round((i / 3) % GRID_SIZE);
    const iy = Math.round((i / 3) / GRID_SIZE);
    const idx = iy * GRID_SIZE + ix;
    const revenue = step.revenue[idx];
    const userDensity = step.users[idx];
    // Elevation from revenue
    positions[i + 1] = revenue * 1.8;
    // Vertex color: user density drives green channel, revenue drives brightness
    const g = 0.15 + userDensity * 0.7;
    const r = 0.08 + userDensity * 0.15 + revenue * 0.05;
    const b = 0.05 + userDensity * 0.1 + revenue * 0.03;
    colors[i] = r;
    colors[i + 1] = g;
    colors[i + 2] = b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  cacheSet(terrainGeoCache, timeIndex, geo);
  return geo;
}
function updateTerrain(timeIndex) {
  if (timeIndex === currentTimeIndex && !heightmapDirty) return; // dirty-flag gate
  const geo = buildTerrainGeometry(timeIndex);
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geo;
  } else {
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.55,
      metalness: 0.08,
      flatShading: false,
    });
    terrainMesh = new THREE.Mesh(geo, mat);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  }
  currentTimeIndex = timeIndex;
  heightmapDirty = false;
}
// === RIVER SYSTEM: error/anomaly paths ===
let riverLine = null;
const riverGeoCache = new Map(); // TubeBufferGeometry cache per time index
function buildRiverGeometry(timeIndex) {
  const cached = cacheGet(riverGeoCache, timeIndex);
  if (cached !== null) { CacheStats.riverHit++; return cached; }
  CacheStats.riverMiss++;
  const ts = generateTimeSeries();
  const step = ts[timeIndex];
  // Trace the ridge of highest errors to form a river path
  const points = [];
  const half = 5;
  // Start at the error hotspot and trace downhill along the error gradient
  let cx = 0, cz = 0, maxErr = -1;
  // Find error hotspot
  for (let iy = 0; iy < GRID_SIZE; iy++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iy * GRID_SIZE + ix;
      if (step.errors[idx] > maxErr) {
        maxErr = step.errors[idx];
        cx = (ix / (GRID_SIZE - 1)) * 10 - half;
        cz = (iy / (GRID_SIZE - 1)) * 10 - half;
      }
    }
  }
  // Trace outward from hotspot following error gradient
  const traceSteps = 16;
  let px = cx, pz = cz;
  for (let s = 0; s < traceSteps; s++) {
    const gx = Math.floor(((px / half) * 0.5 + 0.5) * (GRID_SIZE - 1));
    const gy = Math.floor(((pz / half) * 0.5 + 0.5) * (GRID_SIZE - 1));
    const idx = Math.max(0, Math.min(GRID_SIZE * GRID_SIZE - 1, gy * GRID_SIZE + gx));
    const elevation = step.revenue[idx] * 1.8 + 0.05;
    points.push(new THREE.Vector3(px, elevation, pz));
    // Move along error gradient with some wander
    const gradX = (step.errors[Math.min(GRID_SIZE * GRID_SIZE - 1, gy * GRID_SIZE + Math.min(GRID_SIZE - 1, gx + 1))] - step.errors[Math.max(0, gy * GRID_SIZE + Math.max(0, gx - 1))]) * 1.5;
    const gradZ = (step.errors[Math.min(GRID_SIZE * GRID_SIZE - 1, Math.min(GRID_SIZE - 1, gy + 1) * GRID_SIZE + gx)] - step.errors[Math.max(0, Math.max(0, gy - 1) * GRID_SIZE + gx)]) * 1.5;
    px += gradX * 0.8 + (Math.sin(s * 0.7 + timeIndex) * 0.15);
    pz += gradZ * 0.8 + (Math.cos(s * 0.6 + timeIndex) * 0.15);
    px = Math.max(-half, Math.min(half, px));
    pz = Math.max(-half, Math.min(half, pz));
  }
  const curve = new THREE.CatmullRomCurve3(points);
  const tubeGeo = new THREE.TubeGeometry(curve, 24, 0.08, 8, false);
  cacheSet(riverGeoCache, timeIndex, tubeGeo);
  return tubeGeo;
}
function updateRiver(timeIndex) {
  const geo = buildRiverGeometry(timeIndex);
  if (riverLine) {
    riverLine.geometry.dispose();
  }
  const mat = new THREE.MeshStandardMaterial({
    color: 0xd44a3a,
    roughness: 0.2,
    metalness: 0.4,
    emissive: 0x330800,
    emissiveIntensity: 0.6,
  });
  if (riverLine) {
    riverLine.material = mat;
    riverLine.geometry = geo;
  } else {
    riverLine = new THREE.Mesh(geo, mat);
    riverLine.castShadow = true;
    scene.add(riverLine);
  }
}
// === PARTICLE SYSTEM: API call trails ===
const PARTICLE_COUNT = 2000;
let particleSystem = null;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3); // reused array
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = []; // per-particle metadata (pre-allocated)
function initParticles() {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Each particle has a path: random start on the terrain, follow revenue gradient
    const px = (Math.random() - 0.5) * 10;
    const pz = (Math.random() - 0.5) * 10;
    particlePositions[i * 3] = px;
    particlePositions[i * 3 + 1] = 0.3 + Math.random() * 2;
    particlePositions[i * 3 + 2] = pz;
    // Blue-cyan color range for API traffic
    particleColors[i * 3] = 0.1 + Math.random() * 0.2;
    particleColors[i * 3 + 1] = 0.4 + Math.random() * 0.3;
    particleColors[i * 3 + 2] = 0.7 + Math.random() * 0.3;
    // Particle state: direction vector, speed, lifetime phase
    const angle = Math.random() * Math.PI * 2;
    particleData.push({
      vx: Math.cos(angle) * (0.3 + Math.random() * 0.7),
      vz: Math.sin(angle) * (0.3 + Math.random() * 0.7),
      speed: 0.4 + Math.random() * 1.2,
      phase: Math.random() * Math.PI * 2,
    });
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.04,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.8,
  });
  particleSystem = new THREE.Points(geo, mat);
  scene.add(particleSystem);
}
// Update particles: reuse position array, no per-frame allocations
function updateParticles(dt, timeIndex) {
  if (!particleSystem) return;
  const ts = generateTimeSeries();
  const step = ts[timeIndex];
  const pos = particleSystem.geometry.attributes.position.array;
  const half = 5;
  const gridFactor = (GRID_SIZE - 1) / 10;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    const idx3 = i * 3;
    // Flow along revenue valleys: particles follow negative gradient of elevation
    const gx = Math.floor(((pos[idx3] / half) * 0.5 + 0.5) * (GRID_SIZE - 1));
    const gz = Math.floor(((pos[idx3 + 2] / half) * 0.5 + 0.5) * (GRID_SIZE - 1));
    const gi = Math.max(0, Math.min(GRID_SIZE * GRID_SIZE - 1, gz * GRID_SIZE + gx));
    // Revenue surface steering: particles drift toward higher API call density
    const apiHere = step.apiCalls[gi];
    // Jittered flow direction with terrain avoidance
    pd.vx += (Math.sin(pd.phase + dt * 2) * 0.3 - pos[idx3] * 0.02) * dt;
    pd.vz += (Math.cos(pd.phase + dt * 2) * 0.3 - pos[idx3 + 2] * 0.02) * dt;
    const vlen = Math.sqrt(pd.vx * pd.vx + pd.vz * pd.vz) || 1;
    pd.vx = (pd.vx / vlen) * pd.speed;
    pd.vz = (pd.vz / vlen) * pd.speed;
    pos[idx3] += pd.vx * dt;
    pos[idx3 + 2] += pd.vz * dt;
    // Wrap at terrain boundaries
    if (Math.abs(pos[idx3]) > half) pos[idx3] *= -0.9;
    if (Math.abs(pos[idx3 + 2]) > half) pos[idx3 + 2] *= -0.9;
    // Elevation: sample terrain height at particle position
    const sgx = Math.floor(((pos[idx3] / half) * 0.5 + 0.5) * (GRID_SIZE - 1));
    const sgz = Math.floor(((pos[idx3 + 2] / half) * 0.5 + 0.5) * (GRID_SIZE - 1));
    const sgi = Math.max(0, Math.min(GRID_SIZE * GRID_SIZE - 1, sgz * GRID_SIZE + sgx));
    pos[idx3 + 1] = step.revenue[sgi] * 1.8 + 0.15;
    // Brightness tracks API call density
    const bright = 0.5 + apiHere * 0.4;
    particleSystem.geometry.attributes.color.array[idx3] = 0.05 + bright * 0.15;
    particleSystem.geometry.attributes.color.array[idx3 + 1] = 0.3 + bright * 0.4;
    particleSystem.geometry.attributes.color.array[idx3 + 2] = 0.5 + bright * 0.5;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
  particleSystem.geometry.attributes.color.needsUpdate = true;
}
// === CAMERA BOOKMARKS ===
const bookmarks = [
  { pos: new THREE.Vector3(8, 6, 10), target: new THREE.Vector3(0, 1.2, 0), label: 'Overview' },
  { pos: new THREE.Vector3(2, 4, 2), target: new THREE.Vector3(1, 2.5, 0.8), label: 'Revenue Peak' },
  { pos: new THREE.Vector3(-3, 3, 5), target: new THREE.Vector3(-1.5, 0.6, 1.8), label: 'Error Valley' },
  { pos: new THREE.Vector3(6, 5, -3), target: new THREE.Vector3(0, 1, -1), label: 'Traffic Flow' },
];
function applyBookmark(index) {
  const bm = bookmarks[index];
  controls.target.copy(bm.target);
  camera.position.copy(bm.pos);
  controls.update();
}
document.querySelectorAll('.bookmark-btn').forEach(btn => {
  btn.addEventListener('click', () => applyBookmark(parseInt(btn.dataset.cam)));
});
// === TIME SLIDER ===
const timeSlider = document.getElementById('time-slider');
const timeValueDisplay = document.getElementById('time-value');
let sliderTimeout = null;
function applyTimeStep(index) {
  updateTerrain(index);
  // River rebuild: immediate on change, not debounced
  updateRiver(index);
  timeValueDisplay.textContent = `T${index}  ${new Date(2024, 0, 1 + index).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`;
  worldToGridCache.clear(); // invalidate per-frame on slider change
  heightmapDirty = false;
  updateCacheUI();
}
timeSlider.addEventListener('input', () => {
  const idx = parseInt(timeSlider.value);
  timeValueDisplay.textContent = `T${idx} (scrubbing...)`;
  // Clear the dirty flag so terrain actually rebuilds when slider moves
  heightmapDirty = true;
  if (sliderTimeout) clearTimeout(sliderTimeout);
  sliderTimeout = setTimeout(() => applyTimeStep(idx), 16); // next frame
});
timeSlider.addEventListener('change', () => {
  const idx = parseInt(timeSlider.value);
  if (sliderTimeout) clearTimeout(sliderTimeout);
  applyTimeStep(idx);
});
// === PERFORMANCE MONITORING ===
let frameCount = 0;
let lastFpsTime = performance.now();
let currentFps = 60;
// === RENDER LOOP ===
const clock = new THREE.Clock();
function animate(timestamp) {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  updateParticles(dt, currentTimeIndex >= 0 ? currentTimeIndex : 0);
  // Dirty-flag check: if terrain mesh exists and no change, skip rebuild
  // (Already handled in updateTerrain via dirty-flag gate)
  renderer.render(scene, camera);
  // FPS counter
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    currentFps = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    document.getElementById('fps-display').textContent = currentFps;
    document.getElementById('fps-display').className = 'metric-value ' + (currentFps >= 55 ? 'good' : currentFps >= 45 ? '' : 'warn');
    frameCount = 0;
    lastFpsTime = timestamp;
  }
  // Triangle count
  let triCount = 0;
  scene.traverse(obj => {
    if (obj.isMesh && obj.geometry) {
      const g = obj.geometry;
      if (g.index) triCount += g.index.count / 3;
      else triCount += (g.attributes.position?.count || 0) / 3;
    }
  });
  document.getElementById('tri-display').textContent = `${Math.round(triCount / 1000)}K`;
  // Particle count & load time estimate
  document.getElementById('particle-display').textContent = PARTICLE_COUNT;
  const loadMs = performance.now() - startTime;
  document.getElementById('load-display').textContent = `${Math.round(loadMs)}ms`;
  document.getElementById('load-display').className = 'metric-value ' + (loadMs < 800 ? 'good' : loadMs < 1500 ? '' : 'warn');
  // Clear per-frame caches
  worldToGridCache.clear();
}
// === INITIALIZATION ===
const startTime = performance.now();
initParticles();
applyTimeStep(0);
updateCacheUI();
requestAnimationFrame(animate);
// === RESIZE HANDLER ===
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// === KEYBOARD SHORTCUTS ===
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r': controls.autoRotate = !controls.autoRotate; break;
    case '1': applyBookmark(0); break;
    case '2': applyBookmark(1); break;
    case '3': applyBookmark(2); break;
    case '4': applyBookmark(3); break;
    case 'arrowleft': timeSlider.value = Math.max(0, parseInt(timeSlider.value) - 1); timeSlider.dispatchEvent(new Event('change')); break;
    case 'arrowright': timeSlider.value = Math.min(TIME_STEPS - 1, parseInt(timeSlider.value) + 1); timeSlider.dispatchEvent(new Event('change')); break;
  }
});
console.log('3D Data Terrain Explorer initialized. Cache stats:', CacheStats);
</script>
</body>
</html>