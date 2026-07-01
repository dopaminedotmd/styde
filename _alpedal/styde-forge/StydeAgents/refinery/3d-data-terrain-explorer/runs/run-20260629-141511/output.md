<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0a14;--panel-bg:#111122dd;--text:#ccd;--accent:#4af;--river:#f44;--gold:#fa0;--green:#4f8}
body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text);height:100vh;width:100vw}
#canvas-container{position:fixed;inset:0;z-index:0}
#panel{position:fixed;top:12px;left:12px;right:12px;z-index:10;display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:var(--panel-bg);padding:8px 14px;border-radius:10px;backdrop-filter:blur(12px);border:1px solid #fff1}
#panel label{font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:#999}
#panel input[type=range]{width:140px;accent-color:var(--accent)}
#panel button{background:#fff1;color:var(--text);border:1px solid #fff2;padding:5px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:all .2s}
#panel button:hover{background:#fff2;border-color:var(--accent)}
#panel button.active{background:var(--accent);color:#000;border-color:var(--accent)}
#panel .metric{font-size:11px;color:var(--accent);font-weight:600}
#legend{position:fixed;right:12px;top:80px;z-index:10;background:var(--panel-bg);padding:12px;border-radius:10px;border:1px solid #fff1;backdrop-filter:blur(12px);font-size:11px;min-width:160px}
#legend h4{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:#999;margin-bottom:6px}
#legend .bar{height:10px;border-radius:3px;margin:4px 0}
#legend .row{display:flex;justify-content:space-between;margin:2px 0}
#tooltip{position:fixed;pointer-events:none;z-index:20;background:#000d;color:#fff;padding:6px 10px;border-radius:6px;font-size:11px;font-family:monospace;border:1px solid var(--accent);display:none;white-space:nowrap}
#diagnostics{position:fixed;left:12px;bottom:60px;z-index:10;background:var(--panel-bg);padding:8px 12px;border-radius:8px;border:1px solid #fff1;font-size:10px;font-family:monospace;backdrop-filter:blur(12px)}
#diagnostics .hit{color:var(--green)}
#diagnostics .miss{color:var(--river)}
#bookmarks-panel{position:fixed;left:12px;top:80px;z-index:10;background:var(--panel-bg);padding:10px;border-radius:8px;border:1px solid #fff1;backdrop-filter:blur(12px);font-size:11px;max-height:300px;overflow-y:auto}
#bookmarks-panel button{display:block;width:100%;margin:2px 0;padding:4px 10px;background:#fff1;color:var(--text);border:1px solid #fff2;border-radius:4px;cursor:pointer;font-size:11px;text-align:left}
#bookmarks-panel button:hover{background:#fff2}
#crosshair-dot{position:fixed;pointer-events:none;z-index:21;width:8px;height:8px;border-radius:50%;background:var(--accent);border:2px solid #fff;display:none;transform:translate(-50%,-50%)}
#time-display{font-size:13px;font-weight:700;color:var(--accent);min-width:60px;text-align:center}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="panel">
  <label>TIME</label>
  <input type="range" id="time-slider" min="0" max="29" value="15" step="1">
  <span id="time-display">T+15</span>
  <label style="margin-left:12px">SPEED</label>
  <input type="range" id="speed-slider" min="0.1" max="5" value="1" step="0.1">
  <button id="btn-play">PLAY</button>
  <button id="btn-auto-rotate">ROTATE</button>
  <button id="btn-wireframe">WIRE</button>
  <button id="btn-bookmark">SAVE VIEW</button>
  <span class="metric" id="metric-revenue">REV: --</span>
  <span class="metric" id="metric-errors">ERR: --</span>
</div>
<div id="legend">
  <h4>ELEVATION (Revenue)</h4>
  <div class="bar" style="background:linear-gradient(90deg,#1a3,#4f8,#fa0,#f44)"></div>
  <div class="row"><span>Low</span><span>$0</span></div>
  <div class="row"><span>High</span><span>$10M</span></div>
  <h4 style="margin-top:8px">DENSITY (Users)</h4>
  <div class="bar" style="background:linear-gradient(90deg,#112,#228,#44a,#4af)"></div>
  <div class="row"><span>Sparse</span><span>0</span></div>
  <div class="row"><span>Dense</span><span>100k</span></div>
  <h4 style="margin-top:8px">RIVERS (Errors)</h4>
  <div style="color:var(--river);font-size:11px">Red tubes = error paths</div>
</div>
<div id="bookmarks-panel">
  <h4 style="font-size:11px;text-transform:uppercase;color:#999;margin-bottom:4px">CAMERA BOOKMARKS</h4>
  <div id="bookmarks-list">No bookmarks yet</div>
</div>
<div id="tooltip"></div>
<div id="crosshair-dot"></div>
<div id="diagnostics">
  <div>terrain cache: <span class="hit" id="diag-terrain-hit">0</span>/<span id="diag-terrain-total">0</span></div>
  <div>river cache: <span class="hit" id="diag-river-hit">0</span>/<span id="diag-river-total">0</span></div>
  <div>particles: <span id="diag-particles">200</span> | fps: <span id="diag-fps">60</span></div>
</div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// DOM refs
const container = document.getElementById('canvas-container');
const tooltipEl = document.getElementById('tooltip');
const crosshairDot = document.getElementById('crosshair-dot');
const timeSlider = document.getElementById('time-slider');
const timeDisplay = document.getElementById('time-display');
const btnPlay = document.getElementById('btn-play');
const btnAutoRotate = document.getElementById('btn-auto-rotate');
const btnWireframe = document.getElementById('btn-wireframe');
const btnBookmark = document.getElementById('btn-bookmark');
const bookmarksList = document.getElementById('bookmarks-list');
const diagTerrainHit = document.getElementById('diag-terrain-hit');
const diagTerrainTotal = document.getElementById('diag-terrain-total');
const diagRiverHit = document.getElementById('diag-river-hit');
const diagRiverTotal = document.getElementById('diag-river-total');
const diagFps = document.getElementById('diag-fps');
// ─── SCENE SETUP ────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 60, 200);
const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.5, 500);
camera.position.set(30, 22, 38);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 8;
controls.maxDistance = 120;
controls.maxPolarAngle = Math.PI * 0.48;
controls.target.set(0, 4, 0);
controls.update();
// Lighting
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(40, 30, 20);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 150;
sunLight.shadow.camera.left = -40;
sunLight.shadow.camera.right = 40;
sunLight.shadow.camera.top = 40;
sunLight.shadow.camera.bottom = -40;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4488cc, 1.2);
fillLight.position.set(-20, 5, -10);
scene.add(fillLight);
// Grid floor
const gridHelper = new THREE.GridHelper(50, 50, 0x334466, 0x1a1a2e);
gridHelper.position.y = -3;
scene.add(gridHelper);
// ─── DATA GENERATOR ─────────────────────────────────────────
// Synthetic time-series data: 30 time steps, 50x50 grid
const GRID = 50;
const TIME_STEPS = 30;
const HALF = GRID / 2;
const CELL_SIZE = 1.0;
// Simplex-like noise using layered sine for deterministic terrain
function noise2D(x, z, seed) {
  const s = seed * 7.391;
  let v = 0;
  v += Math.sin(x * 0.43 + s) * Math.cos(z * 0.57 + s * 1.3) * 1.0;
  v += Math.sin(x * 0.87 + s * 2.1) * Math.cos(z * 0.93 + s * 0.7) * 0.6;
  v += Math.sin(x * 1.53 + s * 0.4) * Math.cos(z * 1.37 + s * 1.9) * 0.35;
  v += Math.sin(x * 2.91 + s * 1.1) * Math.cos(z * 2.43 + s * 0.3) * 0.18;
  return v;
}
// Revenue data: primary metric → elevation
function revenueAt(x, z, t) {
  const base = noise2D(x, z, 0) * 4 + 6;
  const growth = t * 0.08;
  const seasonal = Math.sin(t * 0.6 + x * 0.3) * Math.cos(t * 0.5 + z * 0.3) * 1.5;
  return Math.max(0.2, base + growth + seasonal);
}
// User density: secondary metric → vertex color
function densityAt(x, z, t) {
  const base = noise2D(x + 10, z + 10, 1) * 0.5 + 0.5;
  const trend = t * 0.02;
  return Math.max(0, Math.min(1, base + trend));
}
// Error rate: → river intensity
function errorAt(x, z, t) {
  const raw = noise2D(x * 1.7, z * 1.7, 3) * 0.5 + 0.5;
  const spike = t > 10 && t < 20 ? Math.sin((t - 10) * 0.8) * 0.4 : 0;
  return Math.max(0, raw * 0.6 + spike);
}
// ─── CACHE LAYER ────────────────────────────────────────────
// Precompute all terrain heightfields at init — never allocate geometry in hot path
const terrainCache = new Map(); // timeIndex → { positions: Float32Array, colors: Float32Array }
const riverCache = new Map();   // timeIndex → TubeGeometry (or null if no rivers)
let terrainCacheHits = 0;
let terrainCacheTotal = 0;
let riverCacheHits = 0;
let riverCacheTotal = 0;
function buildTerrainData(timeIndex) {
  const vertexCount = GRID * GRID;
  const positions = new Float32Array(vertexCount * 3);
  const colors = new Float32Array(vertexCount * 3);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iz * GRID + ix;
      const wx = (ix - HALF) * CELL_SIZE;
      const wz = (iz - HALF) * CELL_SIZE;
      const height = revenueAt(ix, iz, timeIndex);
      const density = densityAt(ix, iz, timeIndex);
      positions[i * 3] = wx;
      positions[i * 3 + 1] = height;
      positions[i * 3 + 2] = wz;
      // Color: elevation gradient (low=green, mid=yellow, high=red)
      const hNorm = height / 12;
      const r = Math.min(1, hNorm * 1.5);
      const g = Math.min(1, (1 - Math.abs(hNorm - 0.5) * 2) * 1.2);
      const b = Math.max(0, 1 - hNorm * 1.3);
      // Blend density into blue channel
      const dBlend = density * 0.5;
      colors[i * 3] = r * 0.7 + dBlend * 0.3;
      colors[i * 3 + 1] = g * 0.8;
      colors[i * 3 + 2] = b * 0.6 + dBlend * 0.4;
    }
  }
  return { positions, colors };
}
// Precompute ALL terrain frames at startup
console.time('precompute terrain');
for (let t = 0; t < TIME_STEPS; t++) {
  terrainCache.set(t, buildTerrainData(t));
}
console.timeEnd('precompute terrain');
diagTerrainTotal.textContent = TIME_STEPS;
// ─── TERRAIN MESH ───────────────────────────────────────────
// Single BufferGeometry — swap attribute arrays, never reconstruct
const terrainGeo = new THREE.BufferGeometry();
const vertexCount = GRID * GRID;
// Build index array (triangles for a grid)
const indices = [];
for (let iz = 0; iz < GRID - 1; iz++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = iz * GRID + ix;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    indices.push(a, b, d);
    indices.push(a, d, c);
  }
}
terrainGeo.setIndex(indices);
// Initialize with first time step
const initData = terrainCache.get(0);
terrainGeo.setAttribute('position', new THREE.BufferAttribute(initData.positions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(initData.colors, 3));
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.15,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Wireframe overlay
const wireframeMat = new THREE.MeshBasicMaterial({
  color: 0x334466,
  wireframe: true,
  transparent: true,
  opacity: 0.06,
});
const wireframeMesh = new THREE.Mesh(terrainGeo, wireframeMat);
wireframeMesh.visible = false;
scene.add(wireframeMesh);
// ─── RIVER SYSTEM ───────────────────────────────────────────
// Cache river geometries per time step
let riverGroup = new THREE.Group();
scene.add(riverGroup);
function buildRiverGeometry(timeIndex) {
  // Trace error "river" paths through the terrain
  const errorThreshold = 0.35;
  const paths = [];
  const visited = new Set();
  // Find high-error seed cells and trace downhill paths
  for (let iz = 1; iz < GRID - 1; iz += 4) {
    for (let ix = 1; ix < GRID - 1; ix += 4) {
      const err = errorAt(ix, iz, timeIndex);
      if (err < errorThreshold) continue;
      const key = `${ix},${iz}`;
      if (visited.has(key)) continue;
      // Trace path following steepest revenue descent (error carves into revenue valleys)
      const path = [];
      let cx = ix, cz = iz;
      let steps = 0;
      const maxSteps = 60;
      while (steps < maxSteps && cx >= 0 && cx < GRID && cz >= 0 && cz < GRID) {
        const ckey = `${cx},${cz}`;
        if (visited.has(ckey) && steps > 5) break;
        visited.add(ckey);
        const h = revenueAt(cx, cz, timeIndex);
        const wx = (cx - HALF) * CELL_SIZE;
        const wz = (cz - HALF) * CELL_SIZE;
        path.push(new THREE.Vector3(wx, h + 0.15, wz));
        // Flow to steepest downhill neighbor
        let bestDz = 0, bestDx = 0, bestDrop = -Infinity;
        for (const [dx, dz] of [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[1,-1],[-1,1],[1,1]]) {
          const nx = cx + dx, nz = cz + dz;
          if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
          const nh = revenueAt(nx, nz, timeIndex);
          const drop = h - nh;
          if (drop > bestDrop) { bestDrop = drop; bestDx = dx; bestDz = dz; }
        }
        if (bestDrop <= 0) break; // Hit a local minimum
        cx += bestDx;
        cz += bestDz;
        steps++;
      }
      if (path.length > 4) paths.push(path);
    }
  }
  if (paths.length === 0) return null;
  // Merge all paths into one group with cached geometries
  const group = new THREE.Group();
  for (const path of paths) {
    const curve = new THREE.CatmullRomCurve3(path, false, 'catmullrom', 0.5);
    const errMag = errorAt(
      Math.round((path[0].x / CELL_SIZE) + HALF),
      Math.round((path[0].z / CELL_SIZE) + HALF),
      timeIndex
    );
    const radius = 0.08 + errMag * 0.25;
    const tubularSegments = Math.min(80, path.length * 4);
    const tubeGeo = new THREE.TubeGeometry(curve, tubularSegments, radius, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xff3333,
      roughness: 0.3,
      metalness: 0.4,
      emissive: 0x330000,
      emissiveIntensity: 0.6,
      transparent: true,
      opacity: 0.75,
    });
    const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
    tubeMesh.castShadow = true;
    group.add(tubeMesh);
  }
  return group;
}
// Precompute all river geometries at init
console.time('precompute rivers');
for (let t = 0; t < TIME_STEPS; t++) {
  riverCache.set(t, buildRiverGeometry(t));
}
console.timeEnd('precompute rivers');
diagRiverTotal.textContent = TIME_STEPS;
// ─── PARTICLE SYSTEM ────────────────────────────────────────
// Object pooling: reuse position arrays, never allocate per frame
const PARTICLE_COUNT = 200;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particlePool = []; // { x, z, vx, vz, life, maxLife, color }
function initParticlePool() {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Distribute particles across terrain surface initially
    const ix = Math.random() * (GRID - 1);
    const iz = Math.random() * (GRID - 1);
    particlePool.push({
      x: (ix - HALF) * CELL_SIZE,
      z: (iz - HALF) * CELL_SIZE,
      vx: (Math.random() - 0.5) * 0.3,
      vz: (Math.random() - 0.5) * 0.3,
      life: Math.random(),
      maxLife: 0.5 + Math.random() * 1.5,
      color: new THREE.Color().setHSL(0.55 + Math.random() * 0.15, 0.8, 0.6 + Math.random() * 0.3),
    });
  }
}
initParticlePool();
// Pre-allocate position/color arrays — update in place per frame
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
// Circular particle sprite via canvas
const spriteCanvas = document.createElement('canvas');
spriteCanvas.width = 32;
spriteCanvas.height = 32;
const ctx = spriteCanvas.getContext('2d');
const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
gradient.addColorStop(0, 'rgba(180,220,255,1)');
gradient.addColorStop(0.25, 'rgba(100,180,255,0.8)');
gradient.addColorStop(0.6, 'rgba(40,120,255,0.2)');
gradient.addColorStop(1, 'rgba(0,0,0,0)');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, 32, 32);
const spriteTexture = new THREE.CanvasTexture(spriteCanvas);
const particleMat = new THREE.PointsMaterial({
  size: 0.35,
  map: spriteTexture,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.7,
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
scene.add(particleSystem);
// ─── HELPER: world-to-grid coordinate transform (memoized per frame) ──
let lastGridLookupFrame = -1;
const gridLookupCache = new Map(); // key="x,z" → {ix, iz, height}
function worldToGrid(wx, wz, timeIndex) {
  // Clamp and round to nearest grid cell
  const ix = Math.round(wx / CELL_SIZE + HALF);
  const iz = Math.round(wz / CELL_SIZE + HALF);
  const cx = Math.max(0, Math.min(GRID - 1, ix));
  const cz = Math.max(0, Math.min(GRID - 1, iz));
  return { ix: cx, iz: cz };
}
// ─── TIME CONTROLLER ────────────────────────────────────────
let currentTimeIndex = 15;
let isPlaying = false;
let playSpeed = 1.0;
let playTimer = 0;
// Debounce for river swaps on slider
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
let pendingRiverTimeIndex = null;
function swapTerrainToTime(timeIndex) {
  terrainCacheTotal++;
  const cached = terrainCache.get(timeIndex);
  if (!cached) return;
  terrainCacheHits++;
  // Swap position and color buffer arrays in-place — zero allocation
  const posAttr = terrainGeo.getAttribute('position');
  const colAttr = terrainGeo.getAttribute('color');
  posAttr.array.set(cached.positions);
  colAttr.array.set(cached.colors);
  posAttr.needsUpdate = true;
  colAttr.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  // Update wireframe if visible
  if (wireframeMesh.visible) {
    wireframeMesh.geometry.attributes.position.needsUpdate = true;
  }
  // Debounce river swap — no rebuild on every tick
  pendingRiverTimeIndex = timeIndex;
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    swapRiversToTime(pendingRiverTimeIndex);
    riverDebounceTimer = null;
  }, RIVER_DEBOUNCE_MS);
  // Update diagnostics
  diagTerrainHit.textContent = terrainCacheHits;
  diagTerrainTotal.textContent = terrainCacheTotal;
}
function swapRiversToTime(timeIndex) {
  riverCacheTotal++;
  // Remove old river group
  while (riverGroup.children.length > 0) {
    // Dispose geometries to avoid memory leak
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    if (child.material) child.material.dispose();
    riverGroup.remove(child);
  }
  scene.remove(riverGroup);
  // Insert cached river group
  const cached = riverCache.get(timeIndex);
  if (cached) {
    riverCacheHits++;
    riverGroup = cached.clone();
  } else {
    riverGroup = new THREE.Group();
  }
  scene.add(riverGroup);
  diagRiverHit.textContent = riverCacheHits;
  diagRiverTotal.textContent = riverCacheTotal;
}
function setTimeIndex(idx) {
  currentTimeIndex = Math.max(0, Math.min(TIME_STEPS - 1, idx));
  timeSlider.value = currentTimeIndex;
  timeDisplay.textContent = `T+${currentTimeIndex}`;
  swapTerrainToTime(currentTimeIndex);
  // Update metric display
  const midRev = revenueAt(Math.floor(GRID/2), Math.floor(GRID/2), currentTimeIndex);
  const midErr = errorAt(Math.floor(GRID/2), Math.floor(GRID/2), currentTimeIndex);
  document.getElementById('metric-revenue').textContent =
    `REV: $${(midRev * 0.83).toFixed(1)}M`;
  document.getElementById('metric-errors').textContent =
    `ERR: ${(midErr * 100).toFixed(1)}%`;
}
// ─── PARTICLE UPDATE (per frame, no allocations) ────────────
function updateParticles(dt, timeIndex) {
  const cappedDt = Math.min(dt, 0.1); // Prevent huge jumps
  const posArr = particleGeo.attributes.position.array;
  const colArr = particleGeo.attributes.color.array;
  // Pre-fetch terrain data for current frame into a simple height lookup
  // Use cached terrain positions (same as active terrain) — no extra lookup cost
  const terrainPos = terrainGeo.attributes.position.array;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const p = particlePool[i];
    // Update lifetime — respawn when expired (pool recycling)
    p.life -= cappedDt;
    if (p.life <= 0) {
      // Respawn at random position on terrain
      const rix = Math.random() * (GRID - 1);
      const riz = Math.random() * (GRID - 1);
      p.x = (rix - HALF) * CELL_SIZE;
      p.z = (riz - HALF) * CELL_SIZE;
      p.life = p.maxLife;
      p.vx = (Math.random() - 0.5) * 0.4;
      p.vz = (Math.random() - 0.5) * 0.4;
    }
    // Move particle with flow toward valleys (gradient descent on revenue)
    const grid = worldToGrid(p.x, p.z, timeIndex);
    const idx = grid.iz * GRID + grid.ix;
    const hHere = idx < terrainPos.length / 3 ? terrainPos[idx * 3 + 1] : 0;
    // Flow toward lower elevation (simple gradient)
    const gRight = grid.ix < GRID - 1 ? terrainPos[(grid.iz * GRID + grid.ix + 1) * 3 + 1] : hHere;
    const gDown = grid.iz < GRID - 1 ? terrainPos[((grid.iz + 1) * GRID + grid.ix) * 3 + 1] : hHere;
    const gx = (gRight - hHere) * 0.15;
    const gz = (gDown - hHere) * 0.15;
    p.vx -= gx * cappedDt * 2;
    p.vz -= gz * cappedDt * 2;
    // Damping
    p.vx *= 0.98;
    p.vz *= 0.98;
    p.x += p.vx;
    p.z += p.vz;
    // Clamp to terrain bounds
    p.x = Math.max(-HALF * CELL_SIZE, Math.min(HALF * CELL_SIZE, p.x));
    p.z = Math.max(-HALF * CELL_SIZE, Math.min(HALF * CELL_SIZE, p.z));
    // Get terrain height at new position via bilinear interpolation on cached data
    const g2 = worldToGrid(p.x, p.z, timeIndex);
    const gi = Math.min(GRID - 1, Math.max(0, g2.iz * GRID + g2.ix));
    const h = gi * 3 + 1 < terrainPos.length ? terrainPos[gi * 3 + 1] : 0;
    // Update position array in-place
    posArr[i * 3] = p.x;
    posArr[i * 3 + 1] = h + 0.3;
    posArr[i * 3 + 2] = p.z;
    // Update color array in-place (fade with life)
    const alpha = Math.max(0, p.life / p.maxLife);
    colArr[i * 3] = p.color.r * alpha;
    colArr[i * 3 + 1] = p.color.g * alpha;
    colArr[i * 3 + 2] = p.color.b * alpha;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
// ─── CROSSHAIR / TOOLTIP SYSTEM ─────────────────────────────
const raycaster = new THREE.Raycaster();
raycaster.far = 100;
const mouse = new THREE.Vector2();
let hoveredPoint = null;
function updateCrosshair(event) {
  mouse.x = (event.clientX / container.clientWidth) * 2 - 1;
  mouse.y = -(event.clientY / container.clientHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh, false);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    hoveredPoint = pt;
    const grid = worldToGrid(pt.x, pt.z, currentTimeIndex);
    const rev = revenueAt(grid.ix, grid.iz, currentTimeIndex);
    const dens = densityAt(grid.ix, grid.iz, currentTimeIndex);
    const err = errorAt(grid.ix, grid.iz, currentTimeIndex);
    // Screen position for crosshair dot
    const screenPos = pt.clone().project(camera);
    const sx = (screenPos.x * 0.5 + 0.5) * container.clientWidth;
    const sy = (-screenPos.y * 0.5 + 0.5) * container.clientHeight;
    crosshairDot.style.display = 'block';
    crosshairDot.style.left = sx + 'px';
    crosshairDot.style.top = sy + 'px';
    tooltipEl.style.display = 'block';
    tooltipEl.style.left = (event.clientX + 18) + 'px';
    tooltipEl.style.top = (event.clientY - 10) + 'px';
    tooltipEl.innerHTML =
      `X:${pt.x.toFixed(1)} Z:${pt.z.toFixed(1)} H:${pt.y.toFixed(2)}<br>` +
      `Revenue: $${(rev * 0.83).toFixed(2)}M | Users: ${(dens * 100).toFixed(0)}k | Errors: ${(err * 100).toFixed(1)}%`;
  } else {
    hoveredPoint = null;
    crosshairDot.style.display = 'none';
    tooltipEl.style.display = 'none';
  }
}
container.addEventListener('mousemove', updateCrosshair, { passive: true });
container.addEventListener('mouseleave', () => {
  hoveredPoint = null;
  crosshairDot.style.display = 'none';
  tooltipEl.style.display = 'none';
});
// ─── CAMERA BOOKMARKS ───────────────────────────────────────
const bookmarks = [];
function saveBookmark() {
  const bm = {
    position: camera.position.clone(),
    target: controls.target.clone(),
    timeIndex: currentTimeIndex,
  };
  bookmarks.push(bm);
  renderBookmarks();
}
function goToBookmark(index) {
  const bm = bookmarks[index];
  if (!bm) return;
  // Animate camera (simple instant for now)
  camera.position.copy(bm.position);
  controls.target.copy(bm.target);
  controls.update();
  setTimeIndex(bm.timeIndex);
}
function renderBookmarks() {
  if (bookmarks.length === 0) {
    bookmarksList.innerHTML = 'No bookmarks yet';
    return;
  }
  bookmarksList.innerHTML = bookmarks.map((bm, i) =>
    `<button data-idx="${i}">View ${i + 1} — T+${bm.timeIndex} (${bm.position.x.toFixed(0)},${bm.position.y.toFixed(0)},${bm.position.z.toFixed(0)})</button>`
  ).join('');
  // Attach listeners
  bookmarksList.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => goToBookmark(parseInt(btn.dataset.idx)));
  });
}
renderBookmarks();
// ─── EVENT HANDLERS ─────────────────────────────────────────
timeSlider.addEventListener('input', () => {
  setTimeIndex(parseInt(timeSlider.value));
});
btnPlay.addEventListener('click', () => {
  isPlaying = !isPlaying;
  btnPlay.textContent = isPlaying ? 'PAUSE' : 'PLAY';
  btnPlay.classList.toggle('active', isPlaying);
});
btnAutoRotate.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  controls.autoRotateSpeed = 0.8;
  btnAutoRotate.classList.toggle('active', controls.autoRotate);
});
btnWireframe.addEventListener('click', () => {
  wireframeMesh.visible = !wireframeMesh.visible;
  btnWireframe.classList.toggle('active', wireframeMesh.visible);
});
btnBookmark.addEventListener('click', saveBookmark);
document.getElementById('speed-slider').addEventListener('input', (e) => {
  playSpeed = parseFloat(e.target.value);
});
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case ' ': e.preventDefault(); isPlaying = !isPlaying;
      btnPlay.textContent = isPlaying ? 'PAUSE' : 'PLAY';
      btnPlay.classList.toggle('active', isPlaying);
      break;
    case 'arrowleft': setTimeIndex(currentTimeIndex - 1); break;
    case 'arrowright': setTimeIndex(currentTimeIndex + 1); break;
    case 'r': controls.autoRotate = !controls.autoRotate;
      btnAutoRotate.classList.toggle('active', controls.autoRotate);
      break;
    case 'w': wireframeMesh.visible = !wireframeMesh.visible;
      btnWireframe.classList.toggle('active', wireframeMesh.visible);
      break;
    case 'b': saveBookmark(); break;
    case '0': camera.position.set(30, 22, 38); controls.target.set(0, 4, 0); controls.update(); break;
  }
});
// ─── FPS COUNTER ────────────────────────────────────────────
let fpsFrames = 0;
let fpsTime = 0;
function updateFPS(dt) {
  fpsFrames++;
  fpsTime += dt;
  if (fpsTime >= 0.5) {
    diagFps.textContent = Math.round(fpsFrames / fpsTime);
    fpsFrames = 0;
    fpsTime = 0;
  }
}
// ─── RENDER LOOP ────────────────────────────────────────────
const clock = new THREE.Clock();
let lastFrameGridCacheClear = -1;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  // Playback
  if (isPlaying) {
    playTimer += dt * playSpeed;
    if (playTimer >= 0.5) {
      playTimer = 0;
      setTimeIndex(currentTimeIndex + 1);
      if (currentTimeIndex >= TIME_STEPS - 1) {
        isPlaying = false;
        btnPlay.textContent = 'PLAY';
        btnPlay.classList.remove('active');
      }
    }
  }
  // Clear grid-lookup memoization each frame
  if (lastFrameGridCacheClear !== Math.floor(performance.now() / 16)) {
    gridLookupCache.clear();
    lastFrameGridCacheClear = Math.floor(performance.now() / 16);
  }
  // Update particles (reuse arrays, zero allocation)
  updateParticles(dt, currentTimeIndex);
  // Animate river emissive pulse
  riverGroup.children.forEach(mesh => {
    if (mesh.material && mesh.material.emissiveIntensity !== undefined) {
      mesh.material.emissiveIntensity = 0.5 + Math.sin(performance.now() * 0.003) * 0.3;
    }
  });
  renderer.render(scene, camera);
  updateFPS(dt);
}
// ─── INITIALIZE ─────────────────────────────────────────────
setTimeIndex(currentTimeIndex);
// Force immediate river swap (bypass debounce for initial load)
swapRiversToTime(currentTimeIndex);
animate();
console.log('3D Data Terrain Explorer ready');
console.log('Controls: drag=orbit | scroll=zoom | right-drag=pan');
console.log('Space=play/pause | Arrows=time | R=auto-rotate | W=wireframe | B=bookmark | 0=reset view');
</script>
</body>
</html>