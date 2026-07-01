<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a14;--panel-bg:#111122cc;--text:#c8d6e5;--accent:#48dbfb;--warn:#ff6b6b;--good:#51cf66;--border:#2d3561}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  #canvas-container{position:fixed;inset:0;z-index:1}
  #ui-layer{position:fixed;inset:0;z-index:10;pointer-events:none}
  #ui-layer>*{pointer-events:auto}
  #time-panel{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);background:var(--panel-bg);backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:10px;padding:12px 20px;display:flex;align-items:center;gap:14px}
  #time-slider{width:260px;accent-color:var(--accent);cursor:pointer}
  #time-label{min-width:90px;text-align:center;font-variant-numeric:tabular-nums}
  #bookmark-bar{position:absolute;top:16px;right:16px;display:flex;gap:8px}
  #bookmark-bar button{background:var(--panel-bg);backdrop-filter:blur(12px);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:border-color .2s}
  #bookmark-bar button:hover{border-color:var(--accent)}
  #bookmark-bar button.save{color:var(--good);border-color:var(--good)}
  #diagnostic-panel{position:absolute;top:16px;left:16px;background:var(--panel-bg);backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:10px;padding:12px 16px;font-size:11px;line-height:1.6;min-width:180px}
  #diagnostic-panel .title{color:var(--accent);font-weight:600;margin-bottom:4px}
  #diagnostic-panel .hit{color:var(--good)}
  #diagnostic-panel .miss{color:var(--warn)}
  #legend{position:absolute;bottom:24px;left:24px;background:var(--panel-bg);backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:10px;padding:12px 16px;font-size:11px;display:flex;gap:20px}
  .legend-item{display:flex;align-items:center;gap:6px}
  .legend-swatch{width:12px;height:12px;border-radius:3px}
  #tooltip{position:absolute;pointer-events:none;background:var(--panel-bg);backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:12px;display:none;white-space:nowrap}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-layer">
  <div id="diagnostic-panel">
    <div class="title">CACHE DIAGNOSTICS</div>
    <div>Terrain: <span id="diag-terrain-hit" class="hit">0</span>h / <span id="diag-terrain-miss" class="miss">0</span>m</div>
    <div>River: <span id="diag-river-hit" class="hit">0</span>h / <span id="diag-river-miss" class="miss">0</span>m</div>
    <div>Grid Xform: <span id="diag-grid-hit" class="hit">0</span>h / <span id="diag-grid-miss" class="miss">0</span>m</div>
    <div>Particle: <span id="diag-particle-hit" class="hit">0</span>h / <span id="diag-particle-miss" class="miss">0</span>m</div>
    <div>FPS: <span id="diag-fps">--</span></div>
  </div>
  <div id="bookmark-bar">
    <button onclick="saveBookmark()" class="save">+ SAVE VIEW</button>
    <button onclick="loadBookmark(0)">V1 Default</button>
    <button onclick="loadBookmark(1)">V2 Top-down</button>
    <button onclick="loadBookmark(2)">V3 River</button>
  </div>
  <div id="tooltip"></div>
  <div id="time-panel">
    <span style="font-size:12px">TIME</span>
    <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
    <span id="time-label">T=0</span>
  </div>
  <div id="legend">
    <div class="legend-item"><div class="legend-swatch" style="background:#4ecdc4"></div> Revenue (height)</div>
    <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(to top,#2d5016,#7ec845)"></div> User density</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#ff6b6b;width:18px;height:2px;border-radius:1px"></div> Error rivers</div>
    <div class="legend-item"><div class="legend-swatch" style="background:#ffe66d;border-radius:50%"></div> API particles</div>
  </div>
</div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ── GRID & DATA CONFIG ──────────────────────────────────────────
const GRID = 50;
const TIME_STEPS = 24;
const TERRAIN_SIZE = 20;
const HEIGHT_SCALE = 6;
// Synthetic time-series: 4 metrics × TIME_STEPS × GRID×GRID
// Generated procedurally at init — seeded pseudo-deterministic
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
// ── CACHE SYSTEM ────────────────────────────────────────────────
// All cacheable outputs store results; hit/miss counters wired to diagnostic panel consumers
const cache = {
  terrainGeo: new Map(),      // key: timeStep → BufferGeometry
  riverGeo: new Map(),        // key: timeStep → TubeGeometry
  particleStarts: null,       // Float32Array — computed once
  gridXform: new Map(),       // key: "ix,iz" → {worldX,worldZ,height} per frame reset
  gridXformTick: -1,          // frame counter for gridXform invalidation
  stats: {terrain:{hit:0,miss:0},river:{hit:0,miss:0},grid:{hit:0,miss:0},particle:{hit:0,miss:0}}
};
// ── DATA GENERATION ─────────────────────────────────────────────
// 4-channel time-series: [revenue, users, errors, apiCalls] per (t, x, z)
const dataChannels = new Float32Array(TIME_STEPS * GRID * GRID * 4);
const rand = mulberry32(1337);
for (let t = 0; t < TIME_STEPS; t++) {
  const tFrac = t / (TIME_STEPS - 1);
  // Trending revenue peak at mid-period
  const revenueTrend = Math.sin(tFrac * Math.PI) * 0.7 + 0.3;
  for (let ix = 0; ix < GRID; ix++) {
    const xFrac = ix / (GRID - 1);
    for (let iz = 0; iz < GRID; iz++) {
      const zFrac = iz / (GRID - 1);
      const base = (ix * GRID + iz) * 4;
      const idx = t * GRID * GRID * 4 + base;
      // Revenue: 3 hills that grow/shrink with time
      const hill1 = Math.exp(-((xFrac-0.3)**2+(zFrac-0.3)**2)/0.08) * revenueTrend;
      const hill2 = Math.exp(-((xFrac-0.7)**2+(zFrac-0.6)**2)/0.06) * (1 - tFrac * 0.4);
      const hill3 = Math.exp(-((xFrac-0.5)**2+(zFrac-0.7)**2)/0.1) * (tFrac * 1.2);
      dataChannels[idx]     = Math.max(0, hill1 + hill2 + hill3 + rand() * 0.08);
      dataChannels[idx + 1] = (Math.sin(xFrac * 3 + tFrac * 2) * 0.3 + Math.cos(zFrac * 5 - tFrac) * 0.3 + 0.5) * (dataChannels[idx] * 0.6 + 0.4);
      dataChannels[idx + 2] = rand() < 0.03 + tFrac * 0.06 ? rand() * 0.9 + 0.1 : 0;
      dataChannels[idx + 3] = 0.15 + rand() * 0.35 + (xFrac > 0.4 && xFrac < 0.6 && zFrac > 0.3 && zFrac < 0.7 ? 0.4 : 0);
    }
  }
}
// ── THREE.JS SETUP ──────────────────────────────────────────────
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 25, 70);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 120);
camera.position.set(18, 14, 22);
camera.lookAt(0, 3, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 2, 0);
controls.minDistance = 5;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
// ── LIGHTING ────────────────────────────────────────────────────
const ambientLight = new THREE.AmbientLight(0x404066, 1.2);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 2.5);
sunLight.position.set(25, 30, 15);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 80;
sunLight.shadow.camera.left = -30; sunLight.shadow.camera.right = 30;
sunLight.shadow.camera.top = 30; sunLight.shadow.camera.bottom = -30;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const rimLight = new THREE.DirectionalLight(0x6688cc, 0.8);
rimLight.position.set(-10, 5, -15);
scene.add(rimLight);
// Grid plane for reference
const gridHelper = new THREE.PolarGridHelper(12, 32, 20, 64, 0x2d3561, 0x1a1a3a);
gridHelper.position.y = -0.02;
scene.add(gridHelper);
// ── TERRAIN SYSTEM ──────────────────────────────────────────────
let terrainMesh = null;
let currentTerrainGeo = null;
function buildTerrainGeometry(timeStep) {
  // Check cache
  if (cache.terrainGeo.has(timeStep)) {
    cache.stats.terrain.hit++;
    return cache.terrainGeo.get(timeStep).clone();
  }
  cache.stats.terrain.miss++;
  const geo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  // Pre-allocate color array for vertex coloring
  const colors = new Float32Array(pos.count * 3);
  const tBase = timeStep * GRID * GRID * 4;
  for (let i = 0; i < pos.count; i++) {
    // Map vertex index to grid cell
    const ix = i % GRID;
    const iz = Math.floor(i / GRID);
    const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
    const z = (iz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
    const dIdx = tBase + (ix * GRID + iz) * 4;
    const height = dataChannels[dIdx] * HEIGHT_SCALE;
    const userDensity = dataChannels[dIdx + 1];
    pos.setXYZ(i, x, height, z);
    // Vegetation gradient: low density=brown, high density=green
    colors[i * 3]     = 0.18 + userDensity * 0.15;
    colors[i * 3 + 1] = 0.31 + userDensity * 0.45;
    colors[i * 3 + 2] = 0.09 + userDensity * 0.12;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  // Cache the geometry (without colors — colors baked per time step anyway)
  cache.terrainGeo.set(timeStep, geo);
  return geo.clone();
}
function updateTerrain(timeStep) {
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    scene.remove(terrainMesh);
  }
  const geo = buildTerrainGeometry(timeStep);
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide
  });
  terrainMesh = new THREE.Mesh(geo, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
}
// ── RIVER SYSTEM ────────────────────────────────────────────────
let riverLine = null;
// Debounce control for river rebuilds
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
function buildRiverGeometry(timeStep) {
  if (cache.riverGeo.has(timeStep)) {
    cache.stats.river.hit++;
    return cache.riverGeo.get(timeStep).clone();
  }
  cache.stats.river.miss++;
  // Trace error hotspots into path points
  const tBase = timeStep * GRID * GRID * 4;
  const points = [];
  // Walk from left to right, picking highest error cell in each column
  for (let ix = 0; ix < GRID; ix++) {
    let bestZ = 0, bestErr = 0;
    for (let iz = 0; iz < GRID; iz++) {
      const err = dataChannels[tBase + (ix * GRID + iz) * 4 + 2];
      if (err > bestErr) { bestErr = err; bestZ = iz; }
    }
    if (bestErr > 0.1) {
      const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const z = (bestZ / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const height = dataChannels[tBase + (ix * GRID + bestZ) * 4] * HEIGHT_SCALE + 0.3;
      points.push(new THREE.Vector3(x, height, z));
    }
  }
  if (points.length < 2) {
    // Fallback: straight line across center
    points.push(new THREE.Vector3(-TERRAIN_SIZE/2, 0.3, 0));
    points.push(new THREE.Vector3(TERRAIN_SIZE/2, 0.3, 0));
  }
  const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
  // Use TubeGeometry with cached result
  const tubeGeo = new THREE.TubeGeometry(curve, 80, 0.12, 8, false);
  cache.riverGeo.set(timeStep, tubeGeo);
  return tubeGeo.clone();
}
function updateRiver(timeStep) {
  // Debounce: clear any pending rebuild, schedule new one
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (riverLine) { riverLine.geometry.dispose(); scene.remove(riverLine); }
    const geo = buildRiverGeometry(timeStep);
    const mat = new THREE.MeshStandardMaterial({
      color: 0xff4444,
      emissive: 0x330000,
      roughness: 0.3,
      metalness: 0.4
    });
    riverLine = new THREE.Mesh(geo, mat);
    riverLine.renderOrder = 1;
    riverLine.material.depthTest = true;
    riverLine.material.depthWrite = true;
    scene.add(riverLine);
    riverDebounceTimer = null;
  }, RIVER_DEBOUNCE_MS);
}
// ── PARTICLE SYSTEM ─────────────────────────────────────────────
const PARTICLE_COUNT = 300;
let particleGeo = null;
let particleMat = null;
let particlePoints = null;
// Particle state: pre-computed start positions, reused velocity buffer
let particleVelocities = null; // Float32Array reused per particle index
// Each particle tracks its grid index to avoid repeated world→grid transforms
let particleGridIX = new Int32Array(PARTICLE_COUNT);
let particleGridIZ = new Int32Array(PARTICLE_COUNT);
let particleLife = new Float32Array(PARTICLE_COUNT);
function initParticles() {
  if (cache.particleStarts) {
    cache.stats.particle.hit++;
  } else {
    cache.stats.particle.miss++;
    cache.particleStarts = new Float32Array(PARTICLE_COUNT * 3);
  }
  particleVelocities = new Float32Array(PARTICLE_COUNT * 3);
  particleGeo = new THREE.BufferGeometry();
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  particleLife = new Float32Array(PARTICLE_COUNT);
  // Scatter particles randomly across terrain plane
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Random start on the terrain surface
    const ix = Math.floor(Math.random() * GRID);
    const iz = Math.floor(Math.random() * GRID);
    particleGridIX[i] = ix;
    particleGridIZ[i] = iz;
    const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
    const z = (iz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
    // Height will be set per-frame from terrain data — start at 0
    positions[i * 3] = x;
    positions[i * 3 + 1] = 0.5;
    positions[i * 3 + 2] = z;
    // Velocity: small random drift; consumer = per-frame position update
    particleVelocities[i * 3]     = (Math.random() - 0.5) * 0.3;
    particleVelocities[i * 3 + 1] = 0;
    particleVelocities[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
    particleLife[i] = Math.random();
  }
  cache.particleStarts.set(positions);
  particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  // Color attribute: yellow-to-orange based on life
  const colors = new Float32Array(PARTICLE_COUNT * 3);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    colors[i * 3]     = 1.0;
    colors[i * 3 + 1] = 0.6 + particleLife[i] * 0.3;
    colors[i * 3 + 2] = 0.2;
  }
  particleGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  particleMat = new THREE.PointsMaterial({
    size: 0.15,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.85
  });
  particlePoints = new THREE.Points(particleGeo, particleMat);
  particlePoints.renderOrder = 2;
  scene.add(particlePoints);
}
// ── WORLD-TO-GRID MEMOIZATION ───────────────────────────────────
let gridXformFrameId = -1;
function worldToGrid(worldX, worldZ) {
  // Memoize per-frame: gridXform cache is cleared each frame
  const key = `${worldX.toFixed(3)},${worldZ.toFixed(3)}`;
  if (cache.gridXformTick === gridXformFrameId && cache.gridXform.has(key)) {
    cache.stats.grid.hit++;
    return cache.gridXform.get(key);
  }
  cache.stats.grid.miss++;
  const ix = Math.round(((worldX / TERRAIN_SIZE) + 0.5) * (GRID - 1));
  const iz = Math.round(((worldZ / TERRAIN_SIZE) + 0.5) * (GRID - 1));
  const clampedIX = Math.max(0, Math.min(GRID - 1, ix));
  const clampedIZ = Math.max(0, Math.min(GRID - 1, iz));
  const sx = (clampedIX / (GRID - 1) - 0.5) * TERRAIN_SIZE;
  const sz = (clampedIZ / (GRID - 1) - 0.5) * TERRAIN_SIZE;
  const result = {ix: clampedIX, iz: clampedIZ, worldX: sx, worldZ: sz};
  if (cache.gridXformTick !== gridXformFrameId) {
    cache.gridXform.clear();
    cache.gridXformTick = gridXformFrameId;
  }
  cache.gridXform.set(key, result);
  return result;
}
// ── BOOKMARK SYSTEM ─────────────────────────────────────────────
const bookmarks = [
  {pos:[18,14,22],target:[0,2,0]},
  {pos:[0,30,2],target:[0,2,0]},
  {pos:[8,4,-12],target:[-4,3,6]}
];
function saveBookmark() {
  bookmarks.push({
    pos: camera.position.toArray(),
    target: controls.target.toArray()
  });
  // Add a button dynamically
  const idx = bookmarks.length - 1;
  const bar = document.getElementById('bookmark-bar');
  const btn = document.createElement('button');
  btn.textContent = `V${idx+1} User`;
  btn.onclick = () => loadBookmark(idx);
  bar.appendChild(btn);
}
function loadBookmark(idx) {
  if (idx < 0 || idx >= bookmarks.length) return;
  const bm = bookmarks[idx];
  // Smooth animate to bookmark
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animStep() {
    const elapsed = performance.now() - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out cubic
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animStep);
  }
  animStep();
}
// ── TOOLTIP (HOVER) ─────────────────────────────────────────────
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!terrainMesh) return;
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const grid = worldToGrid(point.x, point.z);
    const tBase = currentTimeStep * GRID * GRID * 4;
    const dIdx = tBase + (grid.ix * GRID + grid.iz) * 4;
    const revenue = (dataChannels[dIdx] * 100).toFixed(0);
    const users = (dataChannels[dIdx + 1] * 100).toFixed(0);
    const errors = (dataChannels[dIdx + 2] * 100).toFixed(1);
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 16) + 'px';
    tooltip.style.top = (e.clientY - 40) + 'px';
    tooltip.innerHTML = `Revenue: ${revenue}% | Users: ${users}% | Errors: ${errors}%`;
  } else {
    tooltip.style.display = 'none';
  }
});
// ── SLIDER HANDLER ──────────────────────────────────────────────
let currentTimeStep = 0;
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
slider.addEventListener('input', () => {
  const t = parseInt(slider.value);
  timeLabel.textContent = `T=${t}`;
  currentTimeStep = t;
  updateTerrain(t);
  updateRiver(t);
});
// ── FPS COUNTER ────────────────────────────────────────────────
let fpsFrames = 0, fpsLastTime = performance.now();
// ── ANIMATION LOOP ──────────────────────────────────────────────
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  gridXformFrameId++;
  // Update particles — reuse position array, no per-particle allocation
  if (particlePoints && currentTimeStep !== undefined) {
    const posArr = particleGeo.attributes.position.array;
    const tBase = currentTimeStep * GRID * GRID * 4;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      // Advance particle position by velocity
      posArr[i * 3]     += particleVelocities[i * 3] * 0.016;
      posArr[i * 3 + 2] += particleVelocities[i * 3 + 2] * 0.016;
      // Wrap around terrain bounds
      if (Math.abs(posArr[i * 3]) > TERRAIN_SIZE / 2) {
        posArr[i * 3] = -posArr[i * 3] * 0.9;
        particleVelocities[i * 3] *= -1;
      }
      if (Math.abs(posArr[i * 3 + 2]) > TERRAIN_SIZE / 2) {
        posArr[i * 3 + 2] = -posArr[i * 3 + 2] * 0.9;
        particleVelocities[i * 3 + 2] *= -1;
      }
      // Sample terrain height at particle position — use memoized grid transform
      const grid = worldToGrid(posArr[i * 3], posArr[i * 3 + 2]);
      const dIdx = tBase + (grid.ix * GRID + grid.iz) * 4;
      const terrainH = dataChannels[dIdx] * HEIGHT_SCALE;
      // Float particles above terrain
      posArr[i * 3 + 1] = terrainH + 0.4 + Math.sin(timestamp * 0.003 + i) * 0.2;
    }
    particleGeo.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
  // FPS counter consumer: diagnostic panel display
  fpsFrames++;
  if (timestamp - fpsLastTime >= 1000) {
    const fps = Math.round(fpsFrames / ((timestamp - fpsLastTime) / 1000));
    document.getElementById('diag-fps').textContent = fps;
    // Update cache diagnostic display
    document.getElementById('diag-terrain-hit').textContent = cache.stats.terrain.hit;
    document.getElementById('diag-terrain-miss').textContent = cache.stats.terrain.miss;
    document.getElementById('diag-river-hit').textContent = cache.stats.river.hit;
    document.getElementById('diag-river-miss').textContent = cache.stats.river.miss;
    document.getElementById('diag-grid-hit').textContent = cache.stats.grid.hit;
    document.getElementById('diag-grid-miss').textContent = cache.stats.grid.miss;
    document.getElementById('diag-particle-hit').textContent = cache.stats.particle.hit;
    document.getElementById('diag-particle-miss').textContent = cache.stats.particle.miss;
    fpsFrames = 0;
    fpsLastTime = timestamp;
  }
}
// ── INITIALIZATION ──────────────────────────────────────────────
updateTerrain(0);
updateRiver(0);
initParticles();
requestAnimationFrame(animate);
// ── RESIZE HANDLER ──────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Expose bookmark functions to global scope for onclick handlers
window.saveBookmark = saveBookmark;
window.loadBookmark = loadBookmark;
console.log('3D Data Terrain Explorer initialized');
console.log('Cache system: terrain|river|grid-xform|particle — hit/miss tracked');
console.log('Features: heightfield terrain, vertex-color density, error rivers, API particles, bookmarks, time slider');
</script>
</body>
</html>