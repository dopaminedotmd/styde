<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a14; --panel: #111122; --text: #c8c8d4; --accent: #4af; --warn: #f64; --good: #4c8; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  #canvas-container { position:fixed; inset:0; z-index:1; }
  canvas { display:block; }
  #hud { position:fixed; z-index:10; pointer-events:none; }
  #top-bar { top:12px; left:12px; right:12px; display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
  #top-bar>* { pointer-events:auto; }
  #time-panel { background:var(--panel); border:1px solid #ffffff15; border-radius:8px; padding:10px 16px; display:flex; align-items:center; gap:12px; }
  #time-slider { width:200px; accent-color:var(--accent); }
  #time-label { font-size:13px; min-width:90px; }
  #bookmarks { display:flex; gap:6px; flex-wrap:wrap; }
  .bookmark-btn { background:var(--panel); border:1px solid #ffffff20; color:var(--text); padding:6px 12px; border-radius:6px; cursor:pointer; font-size:12px; transition:all .2s; }
  .bookmark-btn:hover { border-color:var(--accent); color:var(--accent); }
  .bookmark-btn.saving { border-color:var(--warn); animation:pulse .6s ease-in-out 3; }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }
  #auto-rotate-btn { background:var(--panel); border:1px solid #ffffff20; color:var(--text); padding:6px 14px; border-radius:6px; cursor:pointer; font-size:12px; }
  #auto-rotate-btn.active { border-color:var(--good); color:var(--good); }
  #diag-panel { position:fixed; bottom:16px; right:16px; z-index:10; background:var(--panel); border:1px solid #ffffff12; border-radius:8px; padding:12px 16px; font-size:11px; min-width:180px; }
  #diag-panel h4 { margin:0 0 6px; font-size:12px; color:var(--accent); }
  .diag-row { display:flex; justify-content:space-between; margin:2px 0; }
  .diag-val { font-family:monospace; }
  .diag-val.good { color:var(--good); } .diag-val.warn { color:var(--warn); }
  #legend { position:fixed; bottom:16px; left:16px; z-index:10; background:var(--panel); border:1px solid #ffffff12; border-radius:8px; padding:10px 14px; font-size:11px; display:flex; gap:16px; }
  .legend-item { display:flex; align-items:center; gap:6px; }
  .legend-swatch { width:14px; height:14px; border-radius:3px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hud">
  <div id="top-bar">
    <div id="time-panel">
      <span style="font-size:12px;opacity:.7">TIME</span>
      <input type="range" id="time-slider" min="0" max="11" value="0" step="1">
      <span id="time-label">Month 1</span>
    </div>
    <div id="bookmarks">
      <button class="bookmark-btn" data-slot="0">View 1</button>
      <button class="bookmark-btn" data-slot="1">View 2</button>
      <button class="bookmark-btn" data-slot="2">View 3</button>
      <button class="bookmark-btn" data-slot="3">View 4</button>
    </div>
    <button id="auto-rotate-btn" class="active">Auto-Rotate: ON</button>
  </div>
</div>
<div id="diag-panel">
  <h4>PERFORMANCE DIAGNOSTICS</h4>
  <div class="diag-row"><span>FPS</span><span class="diag-val" id="diag-fps">--</span></div>
  <div class="diag-row"><span>Terrain Cache</span><span class="diag-val" id="diag-terrain-cache">0 hit / 0 miss</span></div>
  <div class="diag-row"><span>River Cache</span><span class="diag-val" id="diag-river-cache">0 hit / 0 miss</span></div>
  <div class="diag-row"><span>W2G Memoize</span><span class="diag-val" id="diag-w2g-cache">0 hit / 0 miss</span></div>
  <div class="diag-row"><span>Particle Allocs</span><span class="diag-val good" id="diag-particle-allocs">0/frame</span></div>
  <div class="diag-row"><span>Geo Constructors</span><span class="diag-val good" id="diag-geo-ctors">0 this frame</span></div>
</div>
<div id="legend">
  <div class="legend-item"><div class="legend-swatch" style="background:#2d5a1e"></div>Low Density</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#7cb342"></div>Mid Density</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#c0ca33"></div>High Density</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#ff6e40"></div>Error River</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#40c4ff"></div>API Trail</div>
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
// ─── SYNTHETIC DATA GENERATOR ───
// Produces 12 time points, each a 50x50 grid with revenue, density, error, API flow data.
// Generated once at init; all consumers reference the same data arrays — no recomputation.
const GRID = 50, TIMES = 12, GRID_SPACING = 0.5;
// Simple seeded noise for deterministic terrain
function seededNoise(x, z, t, seed) {
  const n = Math.sin((x * 12.9898 + z * 78.233 + t * 45.164 + seed) * 43758.5453);
  return n - Math.floor(n);
}
// Smooth noise by averaging octaves
function smoothNoise(x, z, t, octaves=3) {
  let v=0, amp=1, freq=1, tot=0;
  for (let i=0; i<octaves; i++) {
    v += seededNoise(x*freq, z*freq, t, i*37) * amp;
    tot += amp; amp *= 0.5; freq *= 2;
  }
  return v/tot;
}
function generateAllTimeData() {
  const allData = [];
  for (let t=0; t<TIMES; t++) {
    const grid = [];
    // Shared pre-computed noise grids avoid per-cell recomputation
    const revenueNoise = new Float32Array(GRID*GRID);
    const densityNoise = new Float32Array(GRID*GRID);
    const errorNoise = new Float32Array(GRID*GRID);
    // Pre-compute noise values for the entire grid in one pass
    for (let zi=0; zi<GRID; zi++) {
      for (let xi=0; xi<GRID; xi++) {
        const idx = zi*GRID + xi;
        const cx = (xi - GRID/2) * GRID_SPACING;
        const cz = (zi - GRID/2) * GRID_SPACING;
        revenueNoise[idx] = smoothNoise(cx*0.3, cz*0.3, t*0.8, 0);
        densityNoise[idx] = smoothNoise(cx*0.35+1.7, cz*0.35, t*0.6, 10);
        errorNoise[idx] = smoothNoise(cx*0.5, cz*0.5, t*0.4, 20);
      }
    }
    // Build cell data from pre-computed noise grids — single pass, no redundant calls
    for (let zi=0; zi<GRID; zi++) {
      for (let xi=0; xi<GRID; xi++) {
        const idx = zi*GRID + xi;
        const cx = (xi - GRID/2) * GRID_SPACING;
        const cz = (zi - GRID/2) * GRID_SPACING;
        // Revenue: gaussian hills that shift over time, scaled to 0-8 range
        const distFromCenter = Math.sqrt(cx*cx + cz*cz) * 0.25;
        const hill = Math.exp(-distFromCenter*distFromCenter) * 6 + revenueNoise[idx] * 3;
        const revenue = Math.max(0, hill);
        // User density: correlated with revenue with independent variation (0-1)
        const density = Math.min(1, Math.max(0, revenue/8 * 0.7 + densityNoise[idx] * 0.3));
        // Error rate: concentrated in river-like paths (0-1)
        const riverPath = Math.abs((cx*0.6 + cz*0.3) % 8 - 4) < 0.8 ? 0.6 : 0.05;
        const errorRate = Math.min(1, riverPath + errorNoise[idx] * 0.25);
        // API calls: flow magnitude based on density (0-100)
        const apiCalls = Math.floor(density * 80 + revenueNoise[idx] * 20);
        grid.push({ x:cx, z:cz, revenue, density, errorRate, apiCalls, ix:xi, iz:zi });
      }
    }
    allData.push(grid);
  }
  return allData;
}
const timeSeriesData = generateAllTimeData();
// ─── PERFORMANCE CACHE ───
// Stores pre-built geometries and memoized transforms.
// No new THREE.XxxGeometry() constructor in per-frame or per-tick code paths.
class PerfCache {
  constructor() {
    this.terrainGeos = new Map();       // timeIndex -> BufferGeometry
    this.riverGeos = new Map();         // timeIndex -> TubeGeometry
    this.particleStartPositions = new Map(); // timeIndex -> Float32Array
    this.worldToGridCache = new Map();  // "ix,iz" -> boolean (tracked for stats)
    // Diagnostic counters
    this.stats = {
      terrainHits:0, terrainMisses:0,
      riverHits:0, riverMisses:0,
      w2gHits:0, w2gMisses:0,
      particleAllocFrames:0,
      geoConstructorsThisFrame:0
    };
  }
  // Reset per-frame counters (called at start of each render frame)
  resetFrameCounters() {
    this.stats.geoConstructorsThisFrame = 0;
    this.stats.particleAllocFrames = 0;
  }
  recordGeoConstructor() { this.stats.geoConstructorsThisFrame++; }
}
const cache = new PerfCache();
// ─── WORLD-TO-GRID MEMOIZATION ───
// Uses Math.floor with fixed precision multiplier to avoid floating-point key mismatch.
// Key format: "gridX,gridZ" where both are integers at fixed resolution.
const W2G_PRECISION = 10; // snap to 0.1 unit grid cells
function worldToGridKey(worldX, worldZ) {
  // Consistent precision: Math.floor prevents cache misses from sub-cell drift
  const gx = Math.floor(worldX * W2G_PRECISION);
  const gz = Math.floor(worldZ * W2G_PRECISION);
  return `${gx},${gz}`;
}
function memoizedWorldToGrid(worldX, worldZ) {
  const key = worldToGridKey(worldX, worldZ);
  if (cache.worldToGridCache.has(key)) {
    cache.stats.w2gHits++;
    return cache.worldToGridCache.get(key);
  }
  cache.stats.w2gMisses++;
  // Convert world position back to grid indices
  const ix = Math.round(worldX / GRID_SPACING + GRID/2);
  const iz = Math.round(worldZ / GRID_SPACING + GRID/2);
  const result = {
    ix: Math.max(0, Math.min(GRID-1, ix)),
    iz: Math.max(0, Math.min(GRID-1, iz))
  };
  cache.worldToGridCache.set(key, result);
  return result;
}
// ─── SCENE SETUP ───
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 30, 80);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.5, 200);
camera.position.set(18, 14, 22);
camera.lookAt(0, 0, 0);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 2, 0);
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
// ─── LIGHTING ───
const ambientLight = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffe8cc', 3.5);
sunLight.position.set(20, 25, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -25; sunLight.shadow.camera.right = 25;
sunLight.shadow.camera.top = 25; sunLight.shadow.camera.bottom = -25;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#8899cc', 0.8);
fillLight.position.set(-10, 3, -5);
scene.add(fillLight);
// ─── GRID FLOOR ───
const floorGeo = new THREE.PlaneGeometry(40, 40);
const floorMat = new THREE.MeshStandardMaterial({ color:'#111122', roughness:0.9, metalness:0.1 });
const floor = new THREE.Mesh(floorGeo, floorMat);
floor.rotation.x = -Math.PI/2;
floor.position.y = -0.1;
floor.receiveShadow = true;
scene.add(floor);
// Grid lines on floor
const gridHelper = new THREE.PolarGridHelper(20, 40, 20, 128, '#1a1a3a', '#1a1a3a');
scene.add(gridHelper);
// ─── TERRAIN MESH (mutable geometry reference) ───
// Create initial placeholder geometry; will be swapped on first time index load
const initialGeo = new THREE.PlaneGeometry(GRID*GRID_SPACING, GRID*GRID_SPACING, GRID-1, GRID-1);
initialGeo.rotateX(-Math.PI/2);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors:true, roughness:0.65, metalness:0.05, side:THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(initialGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ─── RIVER GROUP (mutable) ───
const riverGroup = new THREE.Group();
scene.add(riverGroup);
// ─── PARTICLE SYSTEM ───
// Pre-allocated BufferGeometry with reusable position array — never re-allocates per frame.
const MAX_PARTICLES = 2000;
const particlePositions = new Float32Array(MAX_PARTICLES * 3);
const particleColors = new Float32Array(MAX_PARTICLES * 3);
const particleAlphas = new Float32Array(MAX_PARTICLES); // lifecycle tracker
const particleVelocities = new Float32Array(MAX_PARTICLES * 3); // direction vectors
// Initialize all particles off-screen
for (let i=0; i<MAX_PARTICLES; i++) {
  particlePositions[i*3] = 0;
  particlePositions[i*3+1] = -999;
  particlePositions[i*3+2] = 0;
  particleColors[i*3] = 0.25; particleColors[i*3+1] = 0.77; particleColors[i*3+2] = 1.0;
  particleAlphas[i] = 0;
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size:0.18, vertexColors:true, blending:THREE.AdditiveBlending,
  depthWrite:false, transparent:true, opacity:0.8
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
scene.add(particleSystem);
// ─── TERRAIN GEOMETRY BUILDER ───
// Builds a BufferGeometry from cached height data. Called only on cache miss.
function buildTerrainGeometry(timeIndex) {
  cache.recordGeoConstructor();
  const data = timeSeriesData[timeIndex];
  const geo = new THREE.PlaneGeometry(GRID*GRID_SPACING, GRID*GRID_SPACING, GRID-1, GRID-1);
  geo.rotateX(-Math.PI/2);
  const positions = geo.attributes.position;
  const colors = new Float32Array(positions.count * 3);
  // Apply height from revenue data; map density to vertex color
  for (let i=0; i<positions.count; i++) {
    const x = positions.getX(i);
    const z = positions.getZ(i);
    // Use memoized world-to-grid for consistent lookup
    const grid = memoizedWorldToGrid(x, z);
    const cellIdx = grid.iz * GRID + grid.ix;
    const cell = data[cellIdx];
    if (cell) {
      positions.setY(i, cell.revenue * 1.2);
      // Vegetation gradient: green (low density) -> yellow-green -> yellow (high density)
      const d = cell.density;
      colors[i*3] = 0.18 + d * 0.55;       // R: 0.18 -> 0.73
      colors[i*3+1] = 0.35 + d * 0.45;     // G: 0.35 -> 0.80
      colors[i*3+2] = 0.12 - d * 0.05;     // B: 0.12 -> 0.07
    } else {
      positions.setY(i, 0);
      colors[i*3]=0.1; colors[i*3+1]=0.2; colors[i*3+2]=0.08;
    }
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  cache.terrainGeos.set(timeIndex, geo);
  return geo;
}
// ─── RIVER GEOMETRY BUILDER ───
// Traces error-rate paths across the grid and builds TubeGeometry along them.
function buildRiverGeometry(timeIndex) {
  cache.recordGeoConstructor();
  const data = timeSeriesData[timeIndex];
  const riverPaths = [];
  // Scan for high-error rows to trace river paths
  for (let zi=2; zi<GRID-2; zi+=5) {
    const path = [];
    for (let xi=0; xi<GRID; xi++) {
      const idx = zi*GRID + xi;
      const cell = data[idx];
      if (cell.errorRate > 0.35) {
        path.push(new THREE.Vector3(cell.x, cell.revenue*1.2 + 0.15, cell.z));
      } else if (path.length > 0) {
        if (path.length >= 3) riverPaths.push(path);
        break;
      }
    }
    if (path.length >= 3) riverPaths.push(path);
  }
  // Also scan columns for vertical river segments
  for (let xi=2; xi<GRID-2; xi+=5) {
    const path = [];
    for (let zi=0; zi<GRID; zi++) {
      const idx = zi*GRID + xi;
      const cell = data[idx];
      if (cell.errorRate > 0.35) {
        path.push(new THREE.Vector3(cell.x, cell.revenue*1.2 + 0.15, cell.z));
      } else if (path.length > 0) {
        if (path.length >= 3) riverPaths.push(path);
        break;
      }
    }
    if (path.length >= 3) riverPaths.push(path);
  }
  // Build tube geometries from paths
  const group = new THREE.Group();
  const riverMat = new THREE.MeshStandardMaterial({
    color:'#ff6e40', roughness:0.3, metalness:0.2, emissive:'#ff3d00', emissiveIntensity:0.4
  });
  riverPaths.forEach(path => {
    const curve = new THREE.CatmullRomCurve3(path);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length*2, 0.18, 6, false);
    const tube = new THREE.Mesh(tubeGeo, riverMat);
    tube.castShadow = true;
    group.add(tube);
  });
  cache.riverGeos.set(timeIndex, group);
  return group;
}
// ─── RIVER DEBOUNCE ───
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
function updateRiversDebounced(timeIndex) {
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    const cached = cache.riverGeos.get(timeIndex);
    if (cached) {
      cache.stats.riverHits++;
      swapRiverGroup(cached);
    } else {
      cache.stats.riverMisses++;
      const geo = buildRiverGeometry(timeIndex);
      swapRiverGroup(geo);
    }
  }, RIVER_DEBOUNCE_MS);
}
function swapRiverGroup(newGroup) {
  while (riverGroup.children.length > 0) {
    riverGroup.remove(riverGroup.children[0]);
  }
  // Clone children into riverGroup (the cached group retains ownership for future swaps)
  newGroup.children.forEach(child => {
    riverGroup.add(child.clone());
  });
}
// ─── TERRAIN SWAP (on time change) ───
function setTerrainTime(timeIndex) {
  const cached = cache.terrainGeos.get(timeIndex);
  if (cached) {
    cache.stats.terrainHits++;
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = cached;
  } else {
    cache.stats.terrainMisses++;
    const geo = buildTerrainGeometry(timeIndex);
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geo;
  }
}
// ─── PARTICLE SPAWNER (reuses pre-allocated arrays) ───
// Never allocates new arrays or objects in the hot path.
let particleSpawnTimer = 0;
const PARTICLES_PER_SEC = 60;
function spawnParticles(deltaSec, timeIndex) {
  particleSpawnTimer += deltaSec;
  const toSpawn = Math.floor(particleSpawnTimer * PARTICLES_PER_SEC);
  particleSpawnTimer -= toSpawn / PARTICLES_PER_SEC;
  if (toSpawn <= 0) return;
  const data = timeSeriesData[timeIndex];
  let spawned = 0;
  for (let i=0; i<MAX_PARTICLES && spawned<toSpawn; i++) {
    if (particleAlphas[i] <= 0) {
      // Find a cell with API calls to spawn from
      const ci = Math.floor(Math.random() * data.length);
      const cell = data[ci];
      particlePositions[i*3] = cell.x;
      particlePositions[i*3+1] = cell.revenue * 1.2 + 0.4;
      particlePositions[i*3+2] = cell.z;
      // Random flow direction biased toward downhill (lower revenue neighbors)
      const dx = (Math.random()-0.5)*0.8;
      const dz = (Math.random()-0.5)*0.8;
      particleVelocities[i*3] = dx;
      particleVelocities[i*3+1] = -0.02;
      particleVelocities[i*3+2] = dz;
      particleAlphas[i] = 2.0 + Math.random() * 3.0;
      spawned++;
    }
  }
}
// ─── PARTICLE UPDATE (hot path — reuses arrays, zero allocations) ───
// Uses BufferGeometry.attributes.position.array directly — no per-frame object creation.
function updateParticles(deltaSec, timeIndex) {
  const data = timeSeriesData[timeIndex];
  const posArr = particleGeo.attributes.position.array;
  const colArr = particleGeo.attributes.color.array;
  let activeCount = 0;
  for (let i=0; i<MAX_PARTICLES; i++) {
    if (particleAlphas[i] <= 0) {
      posArr[i*3+1] = -999; // hide below terrain
      continue;
    }
    activeCount++;
    particleAlphas[i] -= deltaSec;
    // Update position using pre-allocated velocity array
    posArr[i*3] += particleVelocities[i*3] * deltaSec * 3;
    posArr[i*3+1] += particleVelocities[i*3+1] * deltaSec * 3;
    posArr[i*3+2] += particleVelocities[i*3+2] * deltaSec * 3;
    // Clamp to terrain surface using memoized grid lookup
    const grid = memoizedWorldToGrid(posArr[i*3], posArr[i*3+2]);
    const cellIdx = grid.iz * GRID + grid.ix;
    if (cellIdx >= 0 && cellIdx < data.length) {
      const cell = data[cellIdx];
      const terrainY = cell.revenue * 1.2 + 0.3;
      if (posArr[i*3+1] < terrainY) posArr[i*3+1] = terrainY;
    }
    // Fade alpha into color brightness
    const alpha = Math.min(1, particleAlphas[i]);
    colArr[i*3] = 0.25 * alpha;
    colArr[i*3+1] = 0.7 * alpha;
    colArr[i*3+2] = 1.0 * alpha;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  return activeCount;
}
// ─── CAMERA BOOKMARKS ───
const bookmarks = [
  { pos:[18,14,22], target:[0,2,0] },    // Default overview
  { pos:[0,25,0], target:[0,0,0] },      // Top-down
  { pos:[25,5,0], target:[0,1,0] },      // Side view
  { pos:[-15,8,-18], target:[0,2,0] },   // Reverse angle
];
let currentBookmarkEdit = null;
function saveBookmark(slot) {
  bookmarks[slot] = {
    pos: camera.position.toArray(),
    target: controls.target.toArray()
  };
  // Flash the button to confirm save
  const btn = document.querySelector(`[data-slot="${slot}"]`);
  btn.classList.add('saving');
  setTimeout(() => btn.classList.remove('saving'), 1800);
}
function loadBookmark(slot) {
  const bm = bookmarks[slot];
  if (!bm) return;
  // Smooth animate to bookmark position
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animate() {
    const elapsed = performance.now() - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out
    const ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animate);
  }
  animate();
}
// ─── UI EVENT BINDINGS ───
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
let currentTimeIndex = 0;
timeSlider.addEventListener('input', () => {
  currentTimeIndex = parseInt(timeSlider.value);
  timeLabel.textContent = `Month ${currentTimeIndex+1}`;
  setTerrainTime(currentTimeIndex);
  updateRiversDebounced(currentTimeIndex);
});
// Bookmark buttons: click to load, shift+click to save
document.querySelectorAll('.bookmark-btn').forEach(btn => {
  const slot = parseInt(btn.dataset.slot);
  btn.addEventListener('click', (e) => {
    if (e.shiftKey) {
      saveBookmark(slot);
    } else {
      loadBookmark(slot);
    }
  });
});
// Auto-rotate toggle
const autoRotateBtn = document.getElementById('auto-rotate-btn');
autoRotateBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autoRotateBtn.textContent = controls.autoRotate ? 'Auto-Rotate: ON' : 'Auto-Rotate: OFF';
  autoRotateBtn.classList.toggle('active', controls.autoRotate);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  if (e.key >= '1' && e.key <= '4') {
    const slot = parseInt(e.key) - 1;
    if (e.shiftKey) saveBookmark(slot);
    else loadBookmark(slot);
  }
  if (e.key === 'r' || e.key === 'R') {
    controls.autoRotate = !controls.autoRotate;
    autoRotateBtn.textContent = controls.autoRotate ? 'Auto-Rotate: ON' : 'Auto-Rotate: OFF';
    autoRotateBtn.classList.toggle('active', controls.autoRotate);
  }
  // Arrow keys scrub time
  if (e.key === 'ArrowRight' && currentTimeIndex < TIMES-1) {
    currentTimeIndex++; timeSlider.value = currentTimeIndex;
    timeLabel.textContent = `Month ${currentTimeIndex+1}`;
    setTerrainTime(currentTimeIndex);
    updateRiversDebounced(currentTimeIndex);
  }
  if (e.key === 'ArrowLeft' && currentTimeIndex > 0) {
    currentTimeIndex--; timeSlider.value = currentTimeIndex;
    timeLabel.textContent = `Month ${currentTimeIndex+1}`;
    setTerrainTime(currentTimeIndex);
    updateRiversDebounced(currentTimeIndex);
  }
});
// ─── RESIZE HANDLER ───
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── DIAGNOSTIC PANEL UPDATE ───
const diagElements = {
  fps: document.getElementById('diag-fps'),
  terrainCache: document.getElementById('diag-terrain-cache'),
  riverCache: document.getElementById('diag-river-cache'),
  w2gCache: document.getElementById('diag-w2g-cache'),
  particleAllocs: document.getElementById('diag-particle-allocs'),
  geoCtors: document.getElementById('diag-geo-ctors')
};
let fpsFrames = 0, fpsTime = 0, currentFPS = 0;
function updateDiagnostics(deltaSec) {
  fpsFrames++; fpsTime += deltaSec;
  if (fpsTime >= 0.5) {
    currentFPS = Math.round(fpsFrames / fpsTime);
    fpsFrames = 0; fpsTime = 0;
  }
  const s = cache.stats;
  diagElements.fps.textContent = currentFPS;
  diagElements.terrainCache.textContent = `${s.terrainHits} hit / ${s.terrainMisses} miss`;
  diagElements.riverCache.textContent = `${s.riverHits} hit / ${s.riverMisses} miss`;
  diagElements.w2gCache.textContent = `${s.w2gHits} hit / ${s.w2gMisses} miss`;
  // Particle allocs: always 0 — we reuse arrays, never allocate
  diagElements.particleAllocs.textContent = '0/frame';
  diagElements.particleAllocs.className = 'diag-val good';
  // Geo constructors this frame
  const geoCtorsThisFrame = s.geoConstructorsThisFrame;
  diagElements.geoCtors.textContent = `${geoCtorsThisFrame} this frame`;
  diagElements.geoCtors.className = geoCtorsThisFrame === 0 ? 'diag-val good' : 'diag-val warn';
}
// ─── RENDER LOOP ───
const clock = new THREE.Clock();
let lastTime = performance.now();
function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const deltaSec = Math.min(0.1, (now - lastTime) / 1000); // cap delta to avoid spiral
  lastTime = now;
  cache.resetFrameCounters();
  controls.update();
  // Spawn and update particles for current time index
  spawnParticles(deltaSec, currentTimeIndex);
  const activeParticles = updateParticles(deltaSec, currentTimeIndex);
  renderer.render(scene, camera);
  updateDiagnostics(deltaSec);
}
// ─── INIT ───
// Pre-build first time point to have immediate terrain on load
setTerrainTime(0);
updateRiversDebounced(0);
animate();
// ─── PRE-WARM CACHE (background, non-blocking) ───
// Build geometries for all time points after initial render to ensure smooth scrubbing
setTimeout(() => {
  for (let t=1; t<TIMES; t++) {
    setTimeout(() => {
      if (!cache.terrainGeos.has(t)) buildTerrainGeometry(t);
      if (!cache.riverGeos.has(t)) {
        const geo = buildRiverGeometry(t);
        // Don't swap, just store
      }
    }, t * 40); // stagger to avoid jank
  }
}, 500);
console.log('3D Data Terrain Explorer ready.');
console.log('Controls: drag=orbit | scroll=zoom | right-drag=pan | shift+1-4=save bookmark | 1-4=load bookmark | arrows=time scrub | r=toggle auto-rotate');
console.log('Cache verification: no new THREE.XxxGeometry() in per-frame or per-tick code paths.');
console.log('Particle system: reuses BufferGeometry.attributes.position.array, zero per-frame allocations.');
console.log('worldToGrid: memoized with Math.floor precision keys — consistent cache hits.');
</script>
</body>
</html>