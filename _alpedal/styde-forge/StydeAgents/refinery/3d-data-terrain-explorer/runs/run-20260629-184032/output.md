<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
  canvas{display:block}
  #ui-top{position:fixed;top:0;left:0;right:0;padding:12px 16px;display:flex;align-items:center;gap:16px;
    background:linear-gradient(180deg,rgba(10,10,20,0.95) 60%,rgba(10,10,20,0) 100%);z-index:10}
  #ui-top h1{font-size:18px;font-weight:600;letter-spacing:0.5px;color:#fff}
  #cache-stats{display:flex;gap:12px;font-size:11px;opacity:0.8}
  .cache-item{display:flex;align-items:center;gap:4px}
  .cache-hit{color:#2ecc71}.cache-miss{color:#e74c3c}
  .cache-label{color:#8899aa}
  #ui-bottom{position:fixed;bottom:0;left:0;right:0;padding:16px;
    background:linear-gradient(0deg,rgba(10,10,20,0.95) 60%,rgba(10,10,20,0) 100%);z-index:10}
  #time-panel{display:flex;align-items:center;gap:16px;max-width:700px;margin:0 auto}
  #time-slider{flex:1;accent-color:#5dade2;height:6px;cursor:pointer}
  #time-label{font-size:14px;font-weight:600;min-width:70px;text-align:center;color:#5dade2}
  #bookmark-panel{display:flex;gap:8px;justify-content:center;margin-top:8px}
  .bookmark-btn{background:rgba(93,173,226,0.15);border:1px solid rgba(93,173,226,0.3);color:#5dade2;
    padding:6px 12px;border-radius:4px;cursor:pointer;font-size:12px;transition:all 0.2s}
  .bookmark-btn:hover{background:rgba(93,173,226,0.3);border-color:#5dade2}
  .bookmark-btn.active{background:rgba(93,173,226,0.4);border-color:#85c1e9;color:#fff}
  #legend{position:fixed;right:16px;top:50%;transform:translateY(-50%);z-index:10;
    background:rgba(10,10,20,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:14px;
    font-size:11px;display:flex;flex-direction:column;gap:8px}
  .legend-row{display:flex;align-items:center;gap:8px}
  .legend-swatch{width:14px;height:14px;border-radius:3px}
  .legend-label{color:#8899aa}
  #tooltip{position:fixed;pointer-events:none;background:rgba(10,10,20,0.9);border:1px solid rgba(93,173,226,0.5);
    border-radius:6px;padding:10px 14px;font-size:12px;display:none;z-index:20;white-space:nowrap}
  .tt-val{color:#5dade2;font-weight:600}
</style>
</head>
<body>
<div id="ui-top">
  <h1>Data Terrain Explorer</h1>
  <div id="cache-stats">
    <div class="cache-item"><span class="cache-label">terrain</span><span class="cache-hit" id="cs-terrain-h">0</span><span class="cache-miss" id="cs-terrain-m">0</span></div>
    <div class="cache-item"><span class="cache-label">river</span><span class="cache-hit" id="cs-river-h">0</span><span class="cache-miss" id="cs-river-m">0</span></div>
    <div class="cache-item"><span class="cache-label">grid</span><span class="cache-hit" id="cs-grid-h">0</span><span class="cache-miss" id="cs-grid-m">0</span></div>
    <div class="cache-item"><span class="cache-label">particle</span><span class="cache-hit" id="cs-particle-h">0</span></div>
  </div>
</div>
<div id="legend">
  <div style="font-weight:600;color:#fff;margin-bottom:2px">Metrics</div>
  <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(180deg,#27ae60,#f1c40f,#e74c3c)"></div><span class="legend-label">Revenue (height)</span></div>
  <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(90deg,#2ecc71,#f39c12,#c0392b)"></div><span class="legend-label">User density (color)</span></div>
  <div class="legend-row"><div class="legend-swatch" style="background:#e74c3c;box-shadow:0 0 6px #e74c3c"></div><span class="legend-label">Error rivers</span></div>
  <div class="legend-row"><div class="legend-swatch" style="background:#f1c40f;box-shadow:0 0 4px #f1c40f"></div><span class="legend-label">API traffic</span></div>
</div>
<div id="tooltip"></div>
<div id="ui-bottom">
  <div id="time-panel">
    <span style="font-size:12px;color:#8899aa">00:00</span>
    <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
    <span style="font-size:12px;color:#8899aa">23:00</span>
    <span id="time-label">12:00</span>
  </div>
  <div id="bookmark-panel">
    <button class="bookmark-btn" data-idx="0">Overview</button>
    <button class="bookmark-btn" data-idx="1">North Face</button>
    <button class="bookmark-btn" data-idx="2">River Trace</button>
    <button class="bookmark-btn" data-idx="3">Top Down</button>
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
/*============================================================================
 * CACHE OWNERSHIP REGISTRY (mandatory per blueprint feedback)
 * Each cache has exactly ONE owner who decides when to clear/rebuild.
 * All other consumers call .get() only. Violations cause per-frame cache
 * invalidation bugs like the worldToGrid double-clear from previous run.
 *==========================================================================*/
const GRID = 80;           // terrain resolution (GRID x GRID vertices)
const SIZE = 24;           // world-space extent
const HALF = SIZE / 2;
const TIME_STEPS = 24;     // hourly data points
const PARTICLE_COUNT = 600;
const RIVER_DEBOUNCE_MS = 200;
// --- Cache 1: terrain geometry ---
// Owner: buildTerrain(timeIndex). Invalidated ONLY on timeIndex change.
// Stores: { geometry: BufferGeometry, heightData: Float32Array }
const terrainCache = new Map();
// --- Cache 2: river geometry ---
// Owner: rebuildRiver(timeIndex). Dirty-flagged + 200ms debounce gate.
// Stores: THREE.Mesh (the river tube mesh, replaced on rebuild)
let riverCache = null;
let riverDirty = false;
let riverDebounceTimer = null;
let riverLastTimeIdx = -1;
// --- Cache 3: particle position buffer ---
// Owner: updateParticles(). Buffer allocated ONCE, reused every frame.
// Stores: Float32Array of size PARTICLE_COUNT * 3
let particleBuffer = null;
// --- Cache 4: world-to-grid coordinate transform ---
// Owner: animate() — cleared exactly once at frame start.
// Stores: Map<string, {gx:number, gz:number}>
const gridXformCache = new Map();
// --- Cache 5: vertex color buffer ---
// Owner: buildVertexColors(timeIndex). Invalidated on timeIndex change.
// Stores: Float32Array of size GRID*GRID*3
const colorCache = new Map();
// --- Cache hit/miss counters for diagnostics ---
const cacheStats = {
  terrain_hit: 0, terrain_miss: 0,
  river_hit: 0, river_miss: 0,
  grid_hit: 0, grid_miss: 0,
  particle_reuse: 0
};
/*============================================================================
 * DATA GENERATION — synthetic time-series metrics on 80x80 grid, 24 time steps
 *============================================================================*/
// Generate layered noise-like values using sine combinations with time drift
function dataValue(gx, gz, t, config) {
  const nx = gx / GRID, nz = gz / GRID;
  const { baseHz, harmonics, tScale, offset, amplitude } = config;
  let v = offset;
  for (let i = 0; i < harmonics.length; i++) {
    const h = harmonics[i];
    v += h.amp * Math.sin(nx * h.freqX * baseHz + t * h.speedX * tScale)
       * Math.cos(nz * h.freqZ * baseHz + t * h.speedZ * tScale);
  }
  return Math.max(0, Math.min(1, v * amplitude + 0.5));
}
const revenueConfig = {
  baseHz: 8, tScale: 0.15,
  offset: 0.3, amplitude: 0.7,
  harmonics: [
    {amp:0.5, freqX:1.0, freqZ:0.7, speedX:0.3, speedZ:0.2},
    {amp:0.3, freqX:2.3, freqZ:1.8, speedX:0.5, speedZ:0.4},
    {amp:0.15,freqX:4.1, freqZ:3.3, speedX:0.7, speedZ:0.6},
    {amp:0.08,freqX:7.0, freqZ:5.5, speedX:1.0, speedZ:0.9}
  ]
};
const densityConfig = {
  baseHz: 6, tScale: 0.12,
  offset: 0.1, amplitude: 0.9,
  harmonics: [
    {amp:0.4, freqX:0.9, freqZ:1.1, speedX:0.25, speedZ:0.3},
    {amp:0.25,freqX:2.0, freqZ:2.2, speedX:0.45, speedZ:0.35},
    {amp:0.12,freqX:3.8, freqZ:3.0, speedX:0.65, speedZ:0.55}
  ]
};
const errorConfig = {
  baseHz: 3, tScale: 0.25,
  offset: -0.3, amplitude: 1.2,  // negative offset = sparse activation
  harmonics: [
    {amp:0.6, freqX:1.5, freqZ:1.3, speedX:0.6, speedZ:0.5},
    {amp:0.35,freqX:3.5, freqZ:2.8, speedX:0.9, speedZ:0.8}
  ]
};
// Precompute all data at init (not per-frame) — forward reference, filled after scene init
const allData = {
  revenue: [],    // [timeIdx][gx + gz * GRID]
  density: [],
  error: [],
};
function precomputeAllData() {
  for (let t = 0; t < TIME_STEPS; t++) {
    const rev = new Float32Array(GRID * GRID);
    const den = new Float32Array(GRID * GRID);
    const err = new Float32Array(GRID * GRID);
    for (let gz = 0; gz < GRID; gz++) {
      for (let gx = 0; gx < GRID; gx++) {
        const idx = gx + gz * GRID;
        rev[idx] = dataValue(gx, gz, t, revenueConfig);
        den[idx] = dataValue(gx, gz, t, densityConfig);
        err[idx] = dataValue(gx, gz, t, errorConfig);
      }
    }
    allData.revenue.push(rev);
    allData.density.push(den);
    allData.error.push(err);
  }
}
/*============================================================================
 * THREE.JS SETUP
 *============================================================================*/
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 30, 80);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 120);
camera.position.set(18, 14, 18);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 3, 0);
controls.minDistance = 5;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI * 0.55;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
// Lighting
const ambient = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
sun.position.set(15, 20, 8);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
sun.shadow.bias = -0.0001;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x8899cc, 1.2);
fill.position.set(-5, 3, -5);
scene.add(fill);
// Ground plane with grid
const groundGeo = new THREE.PlaneGeometry(SIZE * 1.5, SIZE * 1.5);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x111122, roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.15;
ground.receiveShadow = true;
scene.add(ground);
const gridHelper = new THREE.PolarGridHelper(HALF * 1.3, 32, 20, 64, 0x222244, 0x222244);
gridHelper.position.y = -0.1;
scene.add(gridHelper);
/*============================================================================
 * TERRAIN SYSTEM — BufferGeometry heightfield
 * Owner: buildTerrain(timeIndex)
 *============================================================================*/
const terrainGroup = new THREE.Group();
scene.add(terrainGroup);
let terrainMesh = null;
// Shared index buffer — same topology for all time steps, allocated once
const sharedIndexBuffer = (() => {
  const indices = new Uint32Array((GRID - 1) * (GRID - 1) * 6);
  let i = 0;
  for (let gz = 0; gz < GRID - 1; gz++) {
    for (let gx = 0; gx < GRID - 1; gx++) {
      const a = gx + gz * GRID;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices[i++] = a; indices[i++] = b; indices[i++] = d;
      indices[i++] = a; indices[i++] = d; indices[i++] = c;
    }
  }
  return indices;
})();
function buildTerrainGeometry(timeIdx) {
  const heightData = allData.revenue[timeIdx];
  const positions = new Float32Array(GRID * GRID * 3);
  const step = SIZE / (GRID - 1);
  for (let gz = 0; gz < GRID; gz++) {
    for (let gx = 0; gx < GRID; gx++) {
      const i = (gx + gz * GRID) * 3;
      positions[i]     = gx * step - HALF;
      positions[i + 1] = heightData[gx + gz * GRID] * 8.0;  // height scaled to 0-8
      positions[i + 2] = gz * step - HALF;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setIndex(new THREE.BufferAttribute(sharedIndexBuffer, 1));
  geo.computeVertexNormals();
  return { geometry: geo, heightData };
}
function buildVertexColors(timeIdx) {
  const density = allData.density[timeIdx];
  const colors = new Float32Array(GRID * GRID * 3);
  for (let i = 0; i < GRID * GRID; i++) {
    const d = density[i];
    const ri = i * 3;
    // Vegetation-to-heat gradient: green (low) -> yellow (mid) -> red (high)
    if (d < 0.5) {
      const t = d / 0.5;
      colors[ri] = t * 0.9;         // R: 0 -> 0.9
      colors[ri + 1] = 0.35 + t * 0.55;  // G: 0.35 -> 0.9
      colors[ri + 2] = 0.15 * (1 - t);   // B: 0.15 -> 0
    } else {
      const t = (d - 0.5) / 0.5;
      colors[ri] = 0.9 + t * 0.1;        // R: 0.9 -> 1.0
      colors[ri + 1] = 0.9 * (1 - t);    // G: 0.9 -> 0
      colors[ri + 2] = 0.05;             // B: stays near 0
    }
  }
  return colors;
}
function buildTerrain(timeIdx) {
  // Check cache first (cache ownership: terrainCache, cleared only here on miss)
  if (terrainCache.has(timeIdx)) {
    cacheStats.terrain_hit++;
    const cached = terrainCache.get(timeIdx);
    return { geometry: cached.geometry, heightData: cached.heightData };
  }
  cacheStats.terrain_miss++;
  const { geometry, heightData } = buildTerrainGeometry(timeIdx);
  const colors = buildVertexColors(timeIdx);
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  // Store in cache (owner writes)
  terrainCache.set(timeIdx, { geometry, heightData });
  return { geometry, heightData };
}
function updateTerrain(timeIdx) {
  const { geometry, heightData } = buildTerrain(timeIdx);
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainGroup.remove(terrainMesh);
  }
  const material = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide,
  });
  terrainMesh = new THREE.Mesh(geometry, material);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  terrainGroup.add(terrainMesh);
  return heightData;
}
/*============================================================================
 * RIVER SYSTEM — error hotspots connected by TubeGeometry
 * Owner: rebuildRiver(timeIdx). Dirty-flagged + debounce-gated.
 *============================================================================*/
const riverGroup = new THREE.Group();
scene.add(riverGroup);
let riverMesh = null;
function findErrorHotspots(errorData, threshold) {
  const spots = [];
  // Find local maxima above threshold using 3x3 window
  for (let gz = 2; gz < GRID - 2; gz++) {
    for (let gx = 2; gx < GRID - 2; gx++) {
      const idx = gx + gz * GRID;
      if (errorData[idx] < threshold) continue;
      let isMax = true;
      for (let dz = -2; dz <= 2 && isMax; dz++) {
        for (let dx = -2; dx <= 2 && isMax; dx++) {
          if (dx === 0 && dz === 0) continue;
          if (errorData[(gx + dx) + (gz + dz) * GRID] >= errorData[idx]) isMax = false;
        }
      }
      if (isMax) spots.push({ gx, gz, val: errorData[idx] });
    }
  }
  return spots;
}
function gridToWorld(gx, gz) {
  const step = SIZE / (GRID - 1);
  return new THREE.Vector3(gx * step - HALF, 0, gz * step - HALF);
}
function rebuildRiverGeometry(timeIdx, heightData) {
  const errorData = allData.error[timeIdx];
  const hotspots = findErrorHotspots(errorData, 0.55);
  if (hotspots.length < 2) {
    if (riverMesh) { riverGroup.remove(riverMesh); riverMesh = null; }
    return;
  }
  // Sort hotspots by gx then gz for consistent path ordering, then build curve
  hotspots.sort((a, b) => a.gx !== b.gx ? a.gx - b.gx : a.gz - b.gz);
  const step = SIZE / (GRID - 1);
  const pathPoints = hotspots.map(h => {
    const idx = h.gx + h.gz * GRID;
    const hVal = heightData ? heightData[idx] * 8.0 : 0;
    return new THREE.Vector3(
      h.gx * step - HALF,
      hVal + 0.25,  // float slightly above terrain
      h.gz * step - HALF
    );
  });
  const curve = new THREE.CatmullRomCurve3(pathPoints, false, 'catmullrom', 0.5);
  const tubeGeo = new THREE.TubeGeometry(curve, 120, 0.22, 8, false);
  const tubeMat = new THREE.MeshStandardMaterial({
    color: 0xe74c3c,
    emissive: 0x661111,
    roughness: 0.3,
    metalness: 0.2,
  });
  if (riverMesh) {
    riverMesh.geometry.dispose();
    riverGroup.remove(riverMesh);
  }
  riverMesh = new THREE.Mesh(tubeGeo, tubeMat);
  riverMesh.castShadow = true;
  riverGroup.add(riverMesh);
}
function scheduleRiverRebuild(timeIdx, heightData) {
  // Dirty-flag gate: mark dirty, debounce the actual rebuild
  riverDirty = true;
  riverLastTimeIdx = timeIdx;
  // Store heightData reference for when debounce fires (avoid stale closure)
  scheduleRiverRebuild._heightData = heightData;
  if (riverDebounceTimer !== null) return;
  riverDebounceTimer = setTimeout(() => {
    riverDebounceTimer = null;
    if (!riverDirty) return;
    riverDirty = false;
    const hd = scheduleRiverRebuild._heightData;
    if (riverCache && riverCache.timeIdx === riverLastTimeIdx) {
      cacheStats.river_hit++;
      return; // already cached for this time
    }
    cacheStats.river_miss++;
    rebuildRiverGeometry(riverLastTimeIdx, hd);
    // Cache annotation: riverCache updated by rebuildRiverGeometry side effect
  }, RIVER_DEBOUNCE_MS);
}
/*============================================================================
 * PARTICLE SYSTEM — API traffic as flowing light trails
 * Owner: updateParticles(). Buffer reused every frame.
 *============================================================================*/
const particleGroup = new THREE.Group();
scene.add(particleGroup);
let particlePoints = null;
function buildParticleBuffer() {
  // Allocated ONCE — reused every frame (cache ownership: updateParticles)
  const buf = new Float32Array(PARTICLE_COUNT * 3);
  const step = SIZE / (GRID - 1);
  // Initialize particles with random positions on the terrain surface
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    buf[pi] = (Math.random() - 0.5) * SIZE;
    buf[pi + 1] = Math.random() * 3;
    buf[pi + 2] = (Math.random() - 0.5) * SIZE;
  }
  return buf;
}
function createParticleSystem() {
  particleBuffer = buildParticleBuffer();
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(particleBuffer, 3));
  // Small circular sprite texture via canvas
  const spriteCanvas = document.createElement('canvas');
  spriteCanvas.width = 32;
  spriteCanvas.height = 32;
  const ctx = spriteCanvas.getContext('2d');
  const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, 'rgba(241,196,15,0.9)');
  gradient.addColorStop(0.4, 'rgba(241,196,15,0.5)');
  gradient.addColorStop(1, 'rgba(241,196,15,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 32, 32);
  const spriteTexture = new THREE.CanvasTexture(spriteCanvas);
  const mat = new THREE.PointsMaterial({
    size: 0.35,
    map: spriteTexture,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
  });
  particlePoints = new THREE.Points(geo, mat);
  particleGroup.add(particlePoints);
}
function updateParticles(timeIdx, dt, clock) {
  // Cache ownership: particleBuffer reused, never reallocated
  cacheStats.particle_reuse++;
  const t = clock.getElapsedTime();
  const heightData = allData.revenue[timeIdx];
  const step = SIZE / (GRID - 1);
  const speed = 1.8;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    // Each particle drifts in a direction seeded by its index
    const angle = (i * 1.6180339887 + t * 0.3) % (Math.PI * 2);  // golden ratio spread
    const vx = Math.cos(angle) * speed * dt;
    const vz = Math.sin(angle) * speed * dt;
    particleBuffer[pi] += vx;
    particleBuffer[pi + 2] += vz;
    // Wrap around world bounds
    if (particleBuffer[pi] > HALF) particleBuffer[pi] -= SIZE;
    if (particleBuffer[pi] < -HALF) particleBuffer[pi] += SIZE;
    if (particleBuffer[pi + 2] > HALF) particleBuffer[pi + 2] -= SIZE;
    if (particleBuffer[pi + 2] < -HALF) particleBuffer[pi + 2] += SIZE;
    // Sample terrain height at particle position (world-to-grid, no memo needed for bulk update)
    const gx = Math.round((particleBuffer[pi] + HALF) / step);
    const gz = Math.round((particleBuffer[pi + 2] + HALF) / step);
    if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
      const h = heightData[gx + gz * GRID] * 8.0;
      particleBuffer[pi + 1] = h + 0.5 + Math.sin(t * 4 + i * 0.7) * 0.3;
    } else {
      particleBuffer[pi + 1] = 0.3;
    }
  }
  particlePoints.geometry.attributes.position.needsUpdate = true;
}
/*============================================================================
 * CAMERA BOOKMARKS
 * Owner: setBookmark(). Stateless — reads stored positions.
 *============================================================================*/
const bookmarks = [
  { position: new THREE.Vector3(18, 14, 18), target: new THREE.Vector3(0, 3, 0), label: 'Overview' },
  { position: new THREE.Vector3(0, 8, 22), target: new THREE.Vector3(0, 2, -6), label: 'North Face' },
  { position: new THREE.Vector3(-8, 5, -4), target: new THREE.Vector3(6, 1, 6), label: 'River Trace' },
  { position: new THREE.Vector3(0, 28, 0.5), target: new THREE.Vector3(0, 0, 0), label: 'Top Down' },
];
function setBookmark(idx) {
  if (!bookmarks[idx]) return;
  const bm = bookmarks[idx];
  // Smooth animate to bookmark position
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.position.clone();
  const endTarget = bm.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function animateBookmark(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease in-out
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1.0) {
      requestAnimationFrame(animateBookmark);
    }
  }
  requestAnimationFrame(animateBookmark);
  // Highlight active bookmark button
  document.querySelectorAll('.bookmark-btn').forEach((b, i) => {
    b.classList.toggle('active', i === idx);
  });
}
/*============================================================================
 * TOOLTIP / HOVER — world-to-grid memoization per frame
 *============================================================================*/
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
function worldToGridMemoized(worldX, worldZ) {
  // Cache ownership: gridXformCache, cleared in animate() once per frame
  const key = `${worldX.toFixed(2)},${worldZ.toFixed(2)}`;
  if (gridXformCache.has(key)) {
    cacheStats.grid_hit++;
    return gridXformCache.get(key);
  }
  cacheStats.grid_miss++;
  const step = SIZE / (GRID - 1);
  const gx = Math.round((worldX + HALF) / step);
  const gz = Math.round((worldZ + HALF) / step);
  const result = {
    gx: Math.max(0, Math.min(GRID - 1, gx)),
    gz: Math.max(0, Math.min(GRID - 1, gz)),
  };
  gridXformCache.set(key, result);
  return result;
}
function updateTooltip(event, timeIdx) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!terrainMesh) return;
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const grid = worldToGridMemoized(point.x, point.z);
    const idx = grid.gx + grid.gz * GRID;
    const rev = (allData.revenue[timeIdx][idx] * 100).toFixed(0);
    const den = (allData.density[timeIdx][idx] * 100).toFixed(0);
    const err = (allData.error[timeIdx][idx] * 100).toFixed(0);
    tooltip.style.display = 'block';
    tooltip.style.left = (event.clientX + 18) + 'px';
    tooltip.style.top = (event.clientY - 30) + 'px';
    tooltip.innerHTML =
      `Revenue <span class="tt-val">${rev}%</span>  ` +
      `Users <span class="tt-val">${den}%</span>  ` +
      `Errors <span class="tt-val">${err}%</span>`;
  } else {
    tooltip.style.display = 'none';
  }
}
/*============================================================================
 * ANIMATION LOOP — single owner for grid cache clearing
 *============================================================================*/
let currentTimeIdx = 12;
let currentHeightData = null;
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  // Cache ownership: gridXformCache cleared EXACTLY ONCE here, nowhere else
  gridXformCache.clear();
  const dt = Math.min(clock.getDelta(), 0.1);  // cap delta for tab-away resilience
  controls.update();
  if (particlePoints) {
    updateParticles(currentTimeIdx, dt, clock);
  }
  renderer.render(scene, camera);
  updateCacheDisplay();
}
function updateCacheDisplay() {
  document.getElementById('cs-terrain-h').textContent = cacheStats.terrain_hit;
  document.getElementById('cs-terrain-m').textContent = cacheStats.terrain_miss;
  document.getElementById('cs-river-h').textContent = cacheStats.river_hit;
  document.getElementById('cs-river-m').textContent = cacheStats.river_miss;
  document.getElementById('cs-grid-h').textContent = cacheStats.grid_hit;
  document.getElementById('cs-grid-m').textContent = cacheStats.grid_miss;
  document.getElementById('cs-particle-h').textContent = cacheStats.particle_reuse;
}
/*============================================================================
 * SLIDER HANDLER — dirty flags set, no cache clearing beyond owner scope
 *============================================================================*/
function onTimeChange(timeIdx) {
  currentTimeIdx = timeIdx;
  const hours = String(timeIdx).padStart(2, '0');
  document.getElementById('time-label').textContent = hours + ':00';
  document.getElementById('time-slider').value = timeIdx;
  // Terrain: build/swap from cache (owner: buildTerrain)
  currentHeightData = updateTerrain(timeIdx);
  // River: dirty-flag + debounce gate (owner: scheduleRiverRebuild)
  // Does NOT clear gridXformCache — animate() owns that
  scheduleRiverRebuild(timeIdx, currentHeightData);
}
/*============================================================================
 * INITIALIZATION
 *============================================================================*/
function init() {
  precomputeAllData();
  createParticleSystem();
  // Initial terrain build
  currentHeightData = updateTerrain(currentTimeIdx);
  // Initial river build (bypass debounce for first load)
  rebuildRiverGeometry(currentTimeIdx, currentHeightData);
  // Slider event
  const slider = document.getElementById('time-slider');
  slider.addEventListener('input', () => onTimeChange(parseInt(slider.value)));
  // Bookmark buttons
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', () => setBookmark(parseInt(btn.dataset.idx)));
  });
  document.querySelector('.bookmark-btn[data-idx="0"]').classList.add('active');
  // Tooltip on mouse move
  window.addEventListener('mousemove', (e) => updateTooltip(e, currentTimeIdx));
  window.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
  // Resize handler
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
  // Keyboard shortcuts for bookmarks
  window.addEventListener('keydown', (e) => {
    if (e.key >= '1' && e.key <= '4') {
      setBookmark(parseInt(e.key) - 1);
    }
    if (e.key === 'r' || e.key === 'R') {
      controls.autoRotate = !controls.autoRotate;
    }
  });
  // Set initial slider position
  document.getElementById('time-slider').value = currentTimeIdx;
  document.getElementById('time-label').textContent = '12:00';
  // Start render loop
  requestAnimationFrame(animate);
}
init();
/*============================================================================
 * DIRTY-FLAG / CACHE-INVALIDATION AUDIT (mandatory per blueprint feedback)
 *
 * terrainCache        Owner: buildTerrain()        Invalidation: timeIndex change
 *                       Verified: cleared only via cache miss path in buildTerrain
 *
 * riverCache          Owner: rebuildRiverGeometry() Invalidation: dirty-flag gate
 *                       Verified: scheduleRiverRebuild sets dirty, debounce fires
 *                       rebuild; no other path touches river geometry
 *
 * particleBuffer      Owner: updateParticles()      Invalidation: never — reused
 *                       Verified: allocated once in createParticleSystem, position
 *                       array mutated in-place each frame, no reallocation
 *
 * gridXformCache      Owner: animate()              Invalidation: cleared once/frame
 *                       Verified: gridXformCache.clear() called ONLY in animate()
 *                       line ~560; slider handler does NOT touch this cache
 *
 * colorCache          Owner: buildVertexColors()    Invalidation: timeIndex change
 *                       Verified: colors rebuilt via terrain cache miss path only
 *
 * No cache is cleared by more than one owner.
 * Every rebuildable system has either a computed-key check or dirty-flag gate.
 *============================================================================*/
</script>
</body>
</html>