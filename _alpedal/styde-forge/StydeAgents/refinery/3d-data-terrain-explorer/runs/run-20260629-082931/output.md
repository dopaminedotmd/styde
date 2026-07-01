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
    --panel-bg: rgba(10,10,30,0.92);
    --text: #c8d6e5;
    --accent: #5dade2;
    --danger: #e74c3c;
    --success: #27ae60;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  #canvas-container { position:fixed; inset:0; z-index:1; }
  canvas { display:block; }
  /* HUD overlay */
  #hud {
    position:fixed; z-index:10; pointer-events:none;
    top:16px; left:16px; right:16px;
    display:flex; justify-content:space-between; align-items:flex-start;
  }
  #hud > * { pointer-events:auto; }
  .panel {
    background:var(--panel-bg); backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.08); border-radius:12px;
    padding:14px 18px; min-width:180px;
  }
  .panel h2 { font-size:13px; font-weight:600; letter-spacing:0.04em; color:var(--accent); margin-bottom:10px; }
  .metric-row { display:flex; justify-content:space-between; font-size:12px; padding:3px 0; }
  .metric-label { opacity:0.7; }
  .metric-value { font-weight:600; font-variant-numeric:tabular-nums; }
  /* Time controls */
  #time-panel {
    position:fixed; bottom:24px; left:50%; transform:translateX(-50%); z-index:10;
    background:var(--panel-bg); backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.08); border-radius:12px;
    padding:12px 20px; display:flex; align-items:center; gap:14px;
  }
  #time-slider { width:300px; accent-color:var(--accent); cursor:pointer; }
  #time-label { font-size:13px; font-weight:600; min-width:90px; text-align:center; font-variant-numeric:tabular-nums; }
  #play-btn {
    background:var(--accent); border:none; color:#fff; width:32px; height:32px; border-radius:50%;
    cursor:pointer; font-size:14px; display:flex; align-items:center; justify-content:center;
  }
  #play-btn.paused { background:var(--danger); }
  /* Bookmarks */
  #bookmarks {
    position:fixed; top:16px; right:16px; z-index:10; display:flex; gap:6px; flex-wrap:wrap;
    max-width:320px; justify-content:flex-end;
  }
  .bookmark-btn {
    background:var(--panel-bg); backdrop-filter:blur(8px);
    border:1px solid rgba(255,255,255,0.12); border-radius:8px;
    color:var(--text); font-size:11px; padding:6px 12px; cursor:pointer;
    transition:border-color 0.2s;
  }
  .bookmark-btn:hover { border-color:var(--accent); }
  .bookmark-btn.save { border-color:var(--success); color:var(--success); }
  /* Cache diagnostics */
  #cache-diag {
    position:fixed; bottom:24px; right:24px; z-index:10;
    background:var(--panel-bg); backdrop-filter:blur(8px);
    border:1px solid rgba(255,255,255,0.06); border-radius:8px;
    padding:8px 14px; font-size:10px; font-family:'Cascadia Code',monospace; opacity:0.7;
  }
  #cache-diag span { color:var(--accent); }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hud">
  <div class="panel" id="stats-panel">
    <h2>DATA LANDSCAPE</h2>
    <div class="metric-row"><span class="metric-label">Revenue peak</span><span class="metric-value" id="stat-revenue">--</span></div>
    <div class="metric-row"><span class="metric-label">User density</span><span class="metric-value" id="stat-users">--</span></div>
    <div class="metric-row"><span class="metric-label">Error rate</span><span class="metric-value" id="stat-errors">--</span></div>
    <div class="metric-row"><span class="metric-label">API calls/s</span><span class="metric-value" id="stat-api">--</span></div>
  </div>
  <div id="bookmarks">
    <button class="bookmark-btn save" id="save-bookmark" title="Save current camera position">+ Save View</button>
  </div>
</div>
<div id="time-panel">
  <button id="play-btn" class="paused" title="Play/Pause time animation">▶</button>
  <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
  <span id="time-label">Day 0</span>
</div>
<div id="cache-diag">
  Cache: <span id="cache-hits">0</span>h / <span id="cache-misses">0</span>m
  &nbsp;|&nbsp; FPS: <span id="fps-counter">--</span>
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
/* ═══════════════════════════════════════════════
   SYNTHETIC DATA GENERATOR — 100 days of metrics
   Each day: { revenue, users, errors, apiCalls }
   ═══════════════════════════════════════════════ */
const GRID_SIZE = 64;
const DAYS = 100;
const NOISE_CACHE = {}; // memoize noise grids per day index
/* Simple seeded PRNG for deterministic noise */
function mulberry32(a) {
  return function() { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
/* Generate one day of metric grids on a GRID_SIZE x GRID_SIZE lattice */
function generateDay(dayIndex) {
  const seed = dayIndex * 7919 + 104729;
  const rand = mulberry32(seed);
  /* Perlin-style value noise via layered random octaves on CPU */
  function noise(x, y, octaves = 3) {
    let val = 0, amp = 1, freq = 1, max = 0;
    for (let o = 0; o < octaves; o++) {
      const sx = (x * freq + o * 13.7) * 1.7;
      const sy = (y * freq + o * 7.3) * 1.7;
      /* Hash-based pseudo-noise */
      const ix = Math.floor(sx), iy = Math.floor(sy);
      const fx = sx - ix, fy = sy - iy;
      const h = ((ix * 374761393 + iy * 668265263 + seed * (o + 1)) & 0x7fffffff) / 0x7fffffff;
      val += h * amp;
      max += amp;
      amp *= 0.5; freq *= 2;
    }
    return val / max;
  }
  /* Build four grids */
  const revenue = new Float32Array(GRID_SIZE * GRID_SIZE);
  const users = new Float32Array(GRID_SIZE * GRID_SIZE);
  const errors = new Float32Array(GRID_SIZE * GRID_SIZE);
  const api = new Float32Array(GRID_SIZE * GRID_SIZE);
  const dayFactor = dayIndex / DAYS; // 0..1 time progression
  /* Introduce a trend peak at day 60 */
  const trend = 0.5 + 0.5 * Math.sin(dayFactor * Math.PI * 0.9) * (0.8 + 0.2 * Math.sin(dayFactor * 7));
  let maxRev = 0, maxUsers = 0, maxErr = 0, maxApi = 0;
  const half = GRID_SIZE / 2;
  for (let iy = 0; iy < GRID_SIZE; iy++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iy * GRID_SIZE + ix;
      /* Coordinates centered, range ~[-1, 1] */
      const nx = (ix - half) / half;
      const ny = (iy - half) / half;
      const dist = Math.sqrt(nx * nx + ny * ny);
      /* Terrain: three-peak landscape */
      const peak1 = Math.exp(-(( (nx-0.15)**2 + (ny-0.1)**2 ) / 0.08));
      const peak2 = Math.exp(-(( (nx+0.2)**2 + (ny+0.3)**2 ) / 0.12));
      const peak3 = Math.exp(-(( (nx-0.0)**2 + (ny-0.35)**2 ) / 0.06));
      let rev = (peak1 * 0.7 + peak2 * 0.5 + peak3 * 0.9) * trend;
      rev += noise(nx, ny, 3) * 0.15;
      rev = Math.max(0, rev);
      revenue[idx] = rev;
      if (rev > maxRev) maxRev = rev;
      /* Users: correlated with revenue + noise */
      let usr = rev * (0.6 + 0.4 * noise(nx + 3, ny, 2)) * (0.8 + 0.2 * dayFactor);
      usr = Math.max(0, usr);
      users[idx] = usr;
      if (usr > maxUsers) maxUsers = usr;
      /* Errors: higher in valleys and at specific anomaly points */
      let err = (1 - rev) * 0.3 + noise(nx + 7, ny + 5, 2) * 0.2;
      /* Anomaly spike at a moving position */
      const anomalyDist = Math.sqrt((nx - 0.3 + dayFactor * 0.6)**2 + (ny + 0.2 - dayFactor * 0.4)**2);
      if (anomalyDist < 0.08) err += 0.6 * (1 - anomalyDist / 0.08);
      err = Math.max(0, Math.min(1, err));
      errors[idx] = err;
      if (err > maxErr) maxErr = err;
      /* API calls: traffic corridors between peaks */
      const corridor = Math.exp(-((ny + 0.1)**2 / 0.03)) * 0.6 + Math.exp(-((nx - 0.1)**2 / 0.05)) * 0.4;
      api[idx] = Math.max(0, corridor + noise(nx, ny, 2) * 0.25);
      if (api[idx] > maxApi) maxApi = api[idx];
    }
  }
  /* Normalize to 0..1 for consistent coloring */
  if (maxRev > 0) for (let i = 0; i < revenue.length; i++) revenue[i] /= maxRev;
  if (maxUsers > 0) for (let i = 0; i < users.length; i++) users[i] /= maxUsers;
  if (maxErr > 0) for (let i = 0; i < errors.length; i++) errors[i] /= maxErr;
  if (maxApi > 0) for (let i = 0; i < api.length; i++) api[i] /= maxApi;
  /* Build the noise grid cache entry */
  const noiseGrid = new Float32Array(GRID_SIZE * GRID_SIZE);
  for (let iy = 0; iy < GRID_SIZE; iy++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      noiseGrid[iy * GRID_SIZE + ix] = noise(ix / GRID_SIZE - 0.5, iy / GRID_SIZE - 0.5, 4);
    }
  }
  return { revenue, users, errors, api, noiseGrid, maxRev, maxUsers, maxErr, maxApi };
}
/* ═══════════════════════════════════════════════
   SCENE SETUP
   ═══════════════════════════════════════════════ */
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 4, 18);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 50);
camera.position.set(3.5, 2.8, 4.2);
camera.lookAt(0, 0.4, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
/* OrbitControls with smooth damping */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 1.5;
controls.maxDistance = 10;
controls.maxPolarAngle = Math.PI * 0.55; // prevent going under terrain
controls.target.set(0, 0.35, 0);
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.update();
/* Lighting */
const ambient = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(5, 8, 3);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 30;
sun.shadow.camera.left = -5;
sun.shadow.camera.right = 5;
sun.shadow.camera.top = 5;
sun.shadow.camera.bottom = -5;
sun.shadow.bias = -0.0002;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x8899cc, 1.2);
fill.position.set(-2, 1, -3);
scene.add(fill);
/* Ground plane (receive shadows) */
const groundGeo = new THREE.PlaneGeometry(12, 12);
const groundMat = new THREE.MeshStandardMaterial({ color:0x0a0a20, roughness:0.9, metalness:0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.8;
ground.receiveShadow = true;
scene.add(ground);
/* Grid helper */
const gridHelper = new THREE.GridHelper(4, 24, 0x334466, 0x1a1a33);
gridHelper.position.y = -0.79;
scene.add(gridHelper);
/* ═══════════════════════════════════════════════
   CACHE LAYER — memoized geometry, noise, transforms
   ═══════════════════════════════════════════════ */
const geometryCache = {}; // key: dayIndex → { terrainGeo, riverGeo, particleData }
const colorCache = {};    // key: dayIndex → Float32Array of vertex colors
let cacheHits = 0, cacheMisses = 0;
function cacheKey(day) { return String(day); }
/* ═══════════════════════════════════════════════
   TERRAIN GEOMETRY BUILDER
   Creates BufferGeometry heightfield from data grid
   ═══════════════════════════════════════════════ */
function buildTerrainGeometry(data) {
  const { revenue, users } = data;
  const w = GRID_SIZE, h = GRID_SIZE;
  const halfW = (w - 1) / 2;
  const halfH = (h - 1) / 2;
  const spacing = 0.06; // world units per grid cell
  const positions = new Float32Array(w * h * 3);
  const colors = new Float32Array(w * h * 3);
  const indices = [];
  /* Height scale: revenue maps to elevation 0..1.2 world units */
  const HEIGHT_SCALE = 1.2;
  for (let iy = 0; iy < h; iy++) {
    for (let ix = 0; ix < w; ix++) {
      const idx = iy * w + ix;
      const gridVal = revenue[idx];
      /* World-space coordinates centered at origin */
      const wx = (ix - halfW) * spacing;
      const wz = (iy - halfH) * spacing;
      const wy = gridVal * HEIGHT_SCALE;
      const pi = idx * 3;
      positions[pi] = wx;
      positions[pi + 1] = wy;
      positions[pi + 2] = wz;
      /* Vertex color: vegetation gradient based on user density */
      /* Low users → brown/dry (#8B6914), high users → lush green (#1B8B3A) */
      const userVal = users[idx];
      const dryR = 0.545, dryG = 0.412, dryB = 0.078;
      const lushR = 0.106, lushG = 0.545, lushB = 0.227;
      const r = dryR + (lushR - dryR) * userVal;
      const g = dryG + (lushG - dryG) * userVal;
      const b = dryB + (lushB - dryB) * userVal;
      colors[pi] = r;
      colors[pi + 1] = g;
      colors[pi + 2] = b;
    }
  }
  /* Build triangle indices (two per quad) */
  for (let iy = 0; iy < h - 1; iy++) {
    for (let ix = 0; ix < w - 1; ix++) {
      const a = iy * w + ix;
      const b = a + 1;
      const c = a + w;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
/* ═══════════════════════════════════════════════
   RIVER GEOMETRY — error anomaly paths
   Traces `errors` grid for contiguous high-error regions
   and builds TubeGeometry following the ridge
   ═══════════════════════════════════════════════ */
function buildRiverGeometry(data) {
  const { errors, revenue } = data;
  const w = GRID_SIZE, h = GRID_SIZE;
  const halfW = (w - 1) / 2, halfH = (h - 1) / 2;
  const spacing = 0.06;
  const HEIGHT_SCALE = 1.2;
  const ERROR_THRESHOLD = 0.55;
  /* Find the highest-error cell as river source */
  let maxErr = 0, srcIx = 0, srcIy = 0;
  for (let iy = 0; iy < h; iy++) {
    for (let ix = 0; ix < w; ix++) {
      const e = errors[iy * w + ix];
      if (e > maxErr) { maxErr = e; srcIx = ix; srcIy = iy; }
    }
  }
  if (maxErr < ERROR_THRESHOLD) return null; // no significant river
  /* Trace downhill from source following steepest error×elevation descent */
  const visited = new Set();
  const path = [];
  let cx = srcIx, cy = srcIy;
  const maxSteps = 80;
  for (let step = 0; step < maxSteps; step++) {
    const key = cy * w + cx;
    if (visited.has(key)) break;
    visited.add(key);
    /* Convert grid to world position (elevation slightly above terrain) */
    const wx = (cx - halfW) * spacing;
    const wz = (cy - halfH) * spacing;
    const wy = (revenue[key] || 0) * HEIGHT_SCALE + 0.015;
    path.push(new THREE.Vector3(wx, wy, wz));
    /* Find neighbor with highest error (steepest error gradient) */
    let bestNx = cx, bestNy = cy, bestErr = errors[key] || 0;
    for (const [dx, dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]]) {
      const nx = cx + dx, ny = cy + dy;
      if (nx < 0 || nx >= w || ny < 0 || ny >= h) continue;
      const nk = ny * w + nx;
      if (visited.has(nk)) continue;
      const nErr = errors[nk] || 0;
      /* Prefer higher error neighbors */
      if (nErr > bestErr) { bestErr = nErr; bestNx = nx; bestNy = ny; }
    }
    if (bestNx === cx && bestNy === cy) break; // no unvisited higher-error neighbor
    cx = bestNx; cy = bestNy;
  }
  if (path.length < 3) return null;
  const curve = new THREE.CatmullRomCurve3(path);
  const tubeGeo = new THREE.TubeGeometry(curve, path.length * 3, 0.025, 8, false);
  return tubeGeo;
}
/* ═══════════════════════════════════════════════
   PARTICLE SYSTEM — API call flow trails
   Reuses position arrays, no per-frame allocations
   ═══════════════════════════════════════════════ */
const PARTICLE_COUNT = 400;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3); // direction + speed
const particleAges = new Float32Array(PARTICLE_COUNT);
const PARTICLE_MAX_AGE = 300; // frames
/* World-to-grid transform cache */
const worldToGridCache = new Map();
const W2G_CACHE_MAX = 200;
function worldToGrid(wx, wz) {
  const key = `${wx.toFixed(4)},${wz.toFixed(4)}`;
  const cached = worldToGridCache.get(key);
  if (cached !== undefined) return cached;
  const halfW = (GRID_SIZE - 1) / 2, halfH = (GRID_SIZE - 1) / 2;
  const spacing = 0.06;
  const gx = Math.round(wx / spacing + halfW);
  const gy = Math.round(wz / spacing + halfH);
  const result = { gx: Math.max(0, Math.min(GRID_SIZE - 1, gx)), gy: Math.max(0, Math.min(GRID_SIZE - 1, gy)) };
  if (worldToGridCache.size >= W2G_CACHE_MAX) { const first = worldToGridCache.keys().next().value; worldToGridCache.delete(first); }
  worldToGridCache.set(key, result);
  return result;
}
let currentDataRef = null; // set when terrain changes, read by particle system
function initParticles() {
  const halfW = (GRID_SIZE - 1) / 2;
  const halfH = (GRID_SIZE - 1) / 2;
  const spacing = 0.06;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    /* Random start on terrain surface */
    const gx = Math.floor(Math.random() * GRID_SIZE);
    const gy = Math.floor(Math.random() * GRID_SIZE);
    const pi = i * 3;
    particlePositions[pi] = (gx - halfW) * spacing;
    particlePositions[pi + 1] = 0.05 + Math.random() * 0.8;
    particlePositions[pi + 2] = (gy - halfH) * spacing;
    /* Random velocity direction (tangent to terrain) */
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.003 + Math.random() * 0.015;
    particleVelocities[pi] = Math.cos(angle) * speed;
    particleVelocities[pi + 1] = 0;
    particleVelocities[pi + 2] = Math.sin(angle) * speed;
    particleAges[i] = Math.random() * PARTICLE_MAX_AGE;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.025,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
  });
  /* Per-particle colors (warm → cool based on age) */
  const pColors = new Float32Array(PARTICLE_COUNT * 3);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const t = particleAges[i] / PARTICLE_MAX_AGE;
    pColors[i * 3] = 0.2 + t * 0.6;     // R: older → brighter
    pColors[i * 3 + 1] = 0.5 - t * 0.3; // G
    pColors[i * 3 + 2] = 1.0 - t * 0.5; // B: younger → blue, older → warm
  }
  geo.setAttribute('color', new THREE.BufferAttribute(pColors, 3));
  const points = new THREE.Points(geo, mat);
  points.renderOrder = 1;
  return points;
}
/* ═══════════════════════════════════════════════
   SCENE OBJECT REFERENCES (swapped, not rebuilt)
   ═══════════════════════════════════════════════ */
let terrainMesh = null;
let riverMesh = null;
let particleSystem = null;
const riverMaterial = new THREE.MeshStandardMaterial({
  color: 0xe74c3c,
  roughness: 0.15,
  metalness: 0.3,
  emissive: 0x330000,
  emissiveIntensity: 0.6,
});
/* Water plane (semi-transparent base) */
const waterGeo = new THREE.PlaneGeometry(4, 4);
const waterMat = new THREE.MeshStandardMaterial({
  color: 0x1a3366,
  roughness: 0.3,
  metalness: 0.7,
  transparent: true,
  opacity: 0.25,
});
const waterPlane = new THREE.Mesh(waterGeo, waterMat);
waterPlane.rotation.x = -Math.PI / 2;
waterPlane.position.y = -0.02;
waterPlane.receiveShadow = true;
scene.add(waterPlane);
/* ═══════════════════════════════════════════════
   LOAD DAY — swaps cached geometries, caches on miss
   ═══════════════════════════════════════════════ */
function loadDay(dayIndex) {
  const key = cacheKey(dayIndex);
  if (geometryCache[key]) {
    cacheHits++;
    const cached = geometryCache[key];
    swapTerrain(cached.terrainGeo, cached.colors);
    swapRiver(cached.riverGeo);
    currentDataRef = cached.data;
  } else {
    cacheMisses++;
    const data = generateDay(dayIndex);
    const terrainGeo = buildTerrainGeometry(data);
    const colors = terrainGeo.attributes.color.array;
    let riverGeo = buildRiverGeometry(data);
    /* Cache river geo; null means no significant river */
    if (riverGeo && riverMesh === null) {
      /* Will be created on first swap */
    }
    geometryCache[key] = { terrainGeo, colors, riverGeo, data };
    swapTerrain(terrainGeo, colors);
    swapRiver(riverGeo);
    currentDataRef = data;
    worldToGridCache.clear(); // invalidate transform cache on terrain change
  }
  document.getElementById('cache-hits').textContent = cacheHits;
  document.getElementById('cache-misses').textContent = cacheMisses;
}
function swapTerrain(geo, colors) {
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geo;
    /* Update vertex colors */
    if (geo.attributes.color) {
      geo.attributes.color.array.set(colors);
      geo.attributes.color.needsUpdate = true;
    }
    geo.computeVertexNormals();
  } else {
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.7,
      metalness: 0.05,
      flatShading: false,
    });
    terrainMesh = new THREE.Mesh(geo, mat);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  }
}
function swapRiver(geo) {
  /* Dispose old river */
  if (riverMesh) {
    riverMesh.geometry.dispose();
    scene.remove(riverMesh);
    riverMesh = null;
  }
  if (geo) {
    riverMesh = new THREE.Mesh(geo, riverMaterial);
    riverMesh.castShadow = true;
    riverMesh.renderOrder = 0;
    scene.add(riverMesh);
  }
}
/* ═══════════════════════════════════════════════
   PARTICLE UPDATE — per-frame, reuses existing arrays
   ═══════════════════════════════════════════════ */
function updateParticles() {
  if (!particleSystem || !currentDataRef) return;
  const data = currentDataRef;
  const pos = particleSystem.geometry.attributes.position.array;
  const col = particleSystem.geometry.attributes.color.array;
  const halfW = (GRID_SIZE - 1) / 2, halfH = (GRID_SIZE - 1) / 2;
  const spacing = 0.06;
  const HEIGHT_SCALE = 1.2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    particleAges[i] += 1;
    /* Respawn aged-out particles at a random high-API-call location */
    if (particleAges[i] >= PARTICLE_MAX_AGE) {
      particleAges[i] = 0;
      /* Biased spawn: prefer grid cells with high api traffic */
      let gx, gy;
      for (let attempt = 0; attempt < 10; attempt++) {
        gx = Math.floor(Math.random() * GRID_SIZE);
        gy = Math.floor(Math.random() * GRID_SIZE);
        if (data.api[gy * GRID_SIZE + gx] > Math.random() * 0.6) break;
      }
      pos[pi] = (gx - halfW) * spacing;
      pos[pi + 2] = (gy - halfH) * spacing;
      const rev = data.revenue[gy * GRID_SIZE + gx] || 0;
      pos[pi + 1] = rev * HEIGHT_SCALE + 0.06;
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.003 + Math.random() * 0.012;
      particleVelocities[pi] = Math.cos(angle) * speed;
      particleVelocities[pi + 1] = 0;
      particleVelocities[pi + 2] = Math.sin(angle) * speed;
    }
    /* Move particle */
    pos[pi] += particleVelocities[pi];
    pos[pi + 2] += particleVelocities[pi + 2];
    /* Clamp to terrain bounds, project Y to terrain surface */
    const halfExtent = halfW * spacing;
    if (Math.abs(pos[pi]) > halfExtent || Math.abs(pos[pi + 2]) > halfExtent) {
      particleAges[i] = PARTICLE_MAX_AGE;
      continue;
    }
    /* Terrain projection using cached world-to-grid transform */
    const grid = worldToGrid(pos[pi], pos[pi + 2]);
    const gIdx = grid.gy * GRID_SIZE + grid.gx;
    const rev = data.revenue[gIdx] || 0;
    const targetY = rev * HEIGHT_SCALE + 0.04;
    pos[pi + 1] += (targetY - pos[pi + 1]) * 0.3; // smooth terrain follow
    /* Color by age */
    const t = particleAges[i] / PARTICLE_MAX_AGE;
    col[pi] = 0.2 + t * 0.6;
    col[pi + 1] = 0.5 - t * 0.3;
    col[pi + 2] = 1.0 - t * 0.5;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
  particleSystem.geometry.attributes.color.needsUpdate = true;
}
/* ═══════════════════════════════════════════════
   ANIMATION LOOP
   ═══════════════════════════════════════════════ */
const clock = new THREE.Clock();
let fpsFrames = 0, fpsTime = 0, currentFps = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  /* FPS counter */
  fpsFrames++;
  fpsTime += dt;
  if (fpsTime >= 1.0) {
    currentFps = Math.round(fpsFrames / fpsTime);
    fpsFrames = 0;
    fpsTime = 0;
    document.getElementById('fps-counter').textContent = currentFps;
  }
  /* Update particles (reuses arrays, no allocation) */
  updateParticles();
  renderer.render(scene, camera);
}
/* ═══════════════════════════════════════════════
   TIME SLIDER + PLAYBACK
   ═══════════════════════════════════════════════ */
let currentDay = 0;
let playing = false;
let playInterval = null;
const PLAY_SPEED_MS = 180;
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const playBtn = document.getElementById('play-btn');
/* Debounce river rebuild: 200ms delay on slider change */
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
let pendingRiverDay = null;
function setDay(dayIndex, skipRiverDebounce = false) {
  dayIndex = Math.max(0, Math.min(DAYS - 1, dayIndex));
  currentDay = dayIndex;
  slider.value = dayIndex;
  timeLabel.textContent = `Day ${dayIndex}`;
  loadDay(dayIndex);
  /* Update stats panel */
  if (currentDataRef) {
    document.getElementById('stat-revenue').textContent = (currentDataRef.maxRev * 100).toFixed(0) + '%';
    document.getElementById('stat-users').textContent = (currentDataRef.maxUsers * 100).toFixed(0) + '%';
    document.getElementById('stat-errors').textContent = (currentDataRef.maxErr * 100).toFixed(0) + '%';
    document.getElementById('stat-api').textContent = (currentDataRef.maxApi * 100).toFixed(0) + '%';
  }
}
/* Pre-warm cache: generate ALL days in background */
function prewarmCache() {
  let day = 0;
  function step() {
    if (day >= DAYS) return;
    const key = cacheKey(day);
    if (!geometryCache[key]) {
      const data = generateDay(day);
      const terrainGeo = buildTerrainGeometry(data);
      const colors = terrainGeo.attributes.color.array;
      const riverGeo = buildRiverGeometry(data);
      geometryCache[key] = { terrainGeo, colors, riverGeo, data };
    }
    day++;
    if (day < DAYS) setTimeout(step, 5); // spread across frames
  }
  step();
}
slider.addEventListener('input', () => {
  const day = parseInt(slider.value);
  setDay(day);
});
playBtn.addEventListener('click', () => {
  playing = !playing;
  if (playing) {
    playBtn.textContent = '⏸';
    playBtn.classList.remove('paused');
    playInterval = setInterval(() => {
      let next = currentDay + 1;
      if (next >= DAYS) next = 0;
      setDay(next);
    }, PLAY_SPEED_MS);
  } else {
    playBtn.textContent = '▶';
    playBtn.classList.add('paused');
    clearInterval(playInterval);
    playInterval = null;
  }
});
/* ═══════════════════════════════════════════════
   CAMERA BOOKMARKS
   ═══════════════════════════════════════════════ */
const bookmarks = [];
const bookmarksContainer = document.getElementById('bookmarks');
function saveBookmark() {
  const bm = {
    position: camera.position.clone(),
    target: controls.target.clone(),
    label: `View ${bookmarks.length + 1}`,
  };
  bookmarks.push(bm);
  renderBookmarks();
}
function goToBookmark(index) {
  const bm = bookmarks[index];
  if (!bm) return;
  /* Smooth animate to bookmark */
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.position;
  const endTarget = bm.target;
  const duration = 800; // ms
  const startTime = performance.now();
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    /* Ease in-out */
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animStep);
    }
  }
  requestAnimationFrame(animStep);
}
function deleteBookmark(index) {
  bookmarks.splice(index, 1);
  renderBookmarks();
}
function renderBookmarks() {
  /* Clear existing bookmark buttons (keep save button) */
  const saveBtn = document.getElementById('save-bookmark');
  bookmarksContainer.innerHTML = '';
  bookmarksContainer.appendChild(saveBtn);
  bookmarks.forEach((bm, i) => {
    const btn = document.createElement('button');
    btn.className = 'bookmark-btn';
    btn.textContent = bm.label;
    btn.title = 'Click to go, right-click to delete';
    btn.addEventListener('click', (e) => {
      if (e.button === 2) { e.preventDefault(); deleteBookmark(i); return; }
      goToBookmark(i);
    });
    btn.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      deleteBookmark(i);
    });
    bookmarksContainer.appendChild(btn);
  });
}
document.getElementById('save-bookmark').addEventListener('click', saveBookmark);
/* Keyboard shortcuts */
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      break;
    case 'f':
      /* Reset camera to default overview */
      camera.position.set(3.5, 2.8, 4.2);
      controls.target.set(0, 0.35, 0);
      controls.update();
      break;
    case 'arrowleft':
      setDay(currentDay - 1);
      break;
    case 'arrowright':
      setDay(currentDay + 1);
      break;
    case ' ':
      e.preventDefault();
      playBtn.click();
      break;
  }
});
/* ═══════════════════════════════════════════════
   RESIZE HANDLER
   ═══════════════════════════════════════════════ */
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
/* ═══════════════════════════════════════════════
   INITIALIZATION
   ═══════════════════════════════════════════════ */
function init() {
  /* Create particle system (reused across all days) */
  particleSystem = initParticles();
  scene.add(particleSystem);
  /* Load initial day */
  setDay(0);
  /* Prewarm all days in background */
  prewarmCache();
  /* Start render loop */
  animate();
}
/* Verify structural completeness before starting */
if (!scene || !camera || !renderer) {
  console.error('[COMPLETION GATE FAIL] Scene/Camera/Renderer not initialized');
  document.body.innerHTML = '<div style="color:#e74c3c;padding:40px;font-family:monospace;">'
    + 'COMPLETION GATE FAILURE: Core Three.js objects not created.<br>'
    + 'Check console for details.</div>';
} else {
  init();
}
</script>
</body>
</html>
```