<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #ccc; }
  #canvas-container { position: fixed; inset: 0; z-index: 0; }
  #ui-panel { position: fixed; top: 16px; left: 16px; z-index: 10; background: rgba(10,10,20,0.85); border: 1px solid #2a2a40; border-radius: 10px; padding: 16px; min-width: 240px; backdrop-filter: blur(10px); }
  #ui-panel h2 { font-size: 15px; font-weight: 600; margin-bottom: 12px; color: #8af; letter-spacing: 0.5px; }
  .ui-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 12px; }
  .ui-row label { min-width: 70px; color: #aaa; }
  .ui-row input[type="range"] { flex: 1; accent-color: #4af; }
  .ui-row span { min-width: 36px; text-align: right; color: #8cf; font-variant-numeric: tabular-nums; }
  button { background: #1a1a30; border: 1px solid #3a3a50; color: #ccc; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 11px; transition: all 0.15s; }
  button:hover { background: #2a2a40; border-color: #5af; color: #fff; }
  button.active { background: #234; border-color: #4af; color: #8cf; }
  #bookmark-bar { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }
  .bm-btn { font-size: 10px; padding: 3px 7px; }
  #diag-panel { position: fixed; bottom: 16px; right: 16px; z-index: 10; background: rgba(10,10,20,0.85); border: 1px solid #2a2a40; border-radius: 10px; padding: 12px 16px; font-size: 11px; backdrop-filter: blur(10px); min-width: 200px; }
  #diag-panel h3 { font-size: 12px; color: #8af; margin-bottom: 8px; }
  .diag-row { display: flex; justify-content: space-between; gap: 16px; margin-bottom: 3px; }
  .diag-val { color: #8cf; font-variant-numeric: tabular-nums; }
  #legend { position: fixed; bottom: 16px; left: 16px; z-index: 10; background: rgba(10,10,20,0.85); border: 1px solid #2a2a40; border-radius: 10px; padding: 10px 14px; font-size: 10px; backdrop-filter: blur(10px); }
  .legend-item { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; }
  .legend-swatch { width: 12px; height: 12px; border-radius: 2px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-panel">
  <h2>Data Terrain Explorer</h2>
  <div class="ui-row">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label">Day 1</span>
  </div>
  <div class="ui-row">
    <label>Height</label>
    <input type="range" id="height-scale" min="1" max="20" value="8" step="0.5">
    <span id="height-label">8.0x</span>
  </div>
  <div class="ui-row">
    <label>Auto-rotate</label>
    <button id="btn-autorot" class="active">ON</button>
  </div>
  <div style="margin-top:10px;font-size:11px;color:#aaa;">Bookmarks</div>
  <div id="bookmark-bar">
    <button class="bm-btn" data-idx="0">Top-down</button>
    <button class="bm-btn" data-idx="1">Valley</button>
    <button class="bm-btn" data-idx="2">Peak</button>
    <button class="bm-btn" data-idx="3">Rivers</button>
  </div>
  <button id="btn-save-bm" style="margin-top:6px;width:100%;">Save Current View</button>
</div>
<div id="diag-panel">
  <h3>Diagnostics</h3>
  <div class="diag-row"><span>FPS</span><span class="diag-val" id="diag-fps">60</span></div>
  <div class="diag-row"><span>Terrain Cache</span><span class="diag-val" id="diag-tcache">miss:1</span></div>
  <div class="diag-row"><span>River Cache</span><span class="diag-val" id="diag-rcache">miss:1</span></div>
  <div class="diag-row"><span>Grid Xform Cache</span><span class="diag-val" id="diag-gcache">hits:0</span></div>
  <div class="diag-row"><span>Particle Allocs</span><span class="diag-val" id="diag-palloc">0/frame</span></div>
  <div class="diag-row"><span>Geo Constructors</span><span class="diag-val" id="diag-gcon">0/tick</span></div>
</div>
<div id="legend">
  <div style="font-weight:600;margin-bottom:6px;color:#aaa;">Legend</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#228B22;"></div> High user density</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#8B4513;"></div> Low user density</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#ff3333;"></div> Error rivers</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#ffdd44;"></div> API call particles</div>
</div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ── Synthetic time-series data ──────────────────────────────────────────────
// 100 days, 20x20 grid. Each cell has revenue, userDensity, errorRate, apiCalls.
const GRID = 20;
const DAYS = 100;
const dataSeries = [];
// Seedable pseudo-random for reproducibility
function mulberry32(a) {
  return function() { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
const rng = mulberry32(42);
// Generate base landscapes then evolve them across days
const baseHills = [];
for (let i = 0; i < 5; i++) {
  baseHills.push({ cx: rng() * (GRID-1), cy: rng() * (GRID-1), amp: 0.5 + rng() * 1.5, sx: 3 + rng() * 8, sy: 3 + rng() * 8 });
}
const baseValleys = [];
for (let i = 0; i < 3; i++) {
  baseValleys.push({ cx: rng() * (GRID-1), cy: rng() * (GRID-1), width: 2 + rng() * 4, angle: rng() * Math.PI * 2 });
}
const errorSources = [];
for (let i = 0; i < 3; i++) {
  errorSources.push({ cx: 3 + rng() * 14, cy: 3 + rng() * 14, phase: rng() * Math.PI * 2, period: 20 + rng() * 60 });
}
for (let day = 0; day < DAYS; day++) {
  const t = day / DAYS;
  const grid = [];
  for (let y = 0; y < GRID; y++) {
    const row = [];
    for (let x = 0; x < GRID; x++) {
      // Revenue: sum of gaussian hills with time drift
      let revenue = 0;
      for (const h of baseHills) {
        const dx = (x - h.cx) / h.sx;
        const dy = (y - h.cy) / h.sy;
        // Hills shift slowly over time
        const shiftX = Math.sin(t * Math.PI * 2 + h.cx) * 1.5;
        const shiftY = Math.cos(t * Math.PI * 2 + h.cy) * 1.5;
        const dx2 = (x - h.cx - shiftX) / h.sx;
        const dy2 = (y - h.cy - shiftY) / h.sy;
        revenue += h.amp * Math.exp(-(dx2 * dx2 + dy2 * dy2));
      }
      // Add valley depressions
      for (const v of baseValleys) {
        const proj = (x - v.cx) * Math.cos(v.angle) + (y - v.cy) * Math.sin(v.angle);
        const perp = -(x - v.cx) * Math.sin(v.angle) + (y - v.cy) * Math.cos(v.angle);
        const valleyFactor = Math.exp(-(perp * perp) / (v.width * v.width));
        revenue -= 0.6 * valleyFactor * Math.abs(Math.sin(proj * 0.8 + t * 2));
      }
      revenue = Math.max(0.05, revenue);
      // User density: correlated with revenue but with independent variation
      const userDensity = revenue * (0.6 + 0.4 * rng()) + 0.1 * Math.sin(x * 1.3 + t * 4) * Math.cos(y * 1.1 + t * 3);
      // Error rate: pulses from sources, higher in valleys
      let errorRate = 0.02;
      for (const es of errorSources) {
        const dist = Math.sqrt((x - es.cx) ** 2 + (y - es.cy) ** 2);
        const pulse = Math.max(0, Math.sin(t * Math.PI * 2 * (60 / es.period) + es.phase));
        errorRate += 0.15 * pulse * Math.exp(-dist / 5);
      }
      errorRate += 0.03 * (1 - revenue); // errors rise where revenue is low
      errorRate = Math.min(0.6, Math.max(0, errorRate));
      // API calls: proportional to user density with daily cycle
      const apiCalls = userDensity * (3 + 2 * Math.sin(t * Math.PI * 2 + x * 0.5 + y * 0.5)) * (0.8 + 0.4 * rng());
      row.push({ revenue, userDensity, errorRate, apiCalls });
    }
    grid.push(row);
  }
  dataSeries.push(grid);
}
// ── Three.js setup ──────────────────────────────────────────────────────────
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 30, 80);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 200);
camera.position.set(18, 14, 22);
camera.lookAt(GRID / 2, 2, GRID / 2);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(GRID / 2, 2, GRID / 2);
controls.enableDamping = true;
controls.dampingFactor = 0.12;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// ── Lighting ────────────────────────────────────────────────────────────────
const ambient = new THREE.AmbientLight(0x1a1a3a, 1.2);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(25, 30, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 120;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
sun.shadow.bias = -0.0001;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x3344aa, 1.0);
fill.position.set(-10, 5, -8);
scene.add(fill);
// Grid plane under the terrain
const gridHelper = new THREE.GridHelper(GRID, GRID, 0x333355, 0x1a1a2e);
gridHelper.position.set(GRID / 2, -0.01, GRID / 2);
scene.add(gridHelper);
// ── Cache infrastructure ────────────────────────────────────────────────────
// Track hits/misses for diagnostic panel
const cacheStats = { terrainHit: 0, terrainMiss: 0, riverHit: 0, riverMiss: 0, gridXformHits: 0 };
let perFrameAllocs = 0;
let perTickGeoConstructors = 0;
// Pre-built terrain geometry cache: keyed by day index
const terrainCache = new Map();
// Pre-built river geometry cache
const riverCache = new Map();
// World-to-grid coordinate transform memoization (per frame)
const gridXformMemo = new Map();
function resetPerFrameCounters() {
  perFrameAllocs = 0;
  gridXformMemo.clear();
}
function resetPerTickCounters() {
  perTickGeoConstructors = 0;
}
// ── Terrain geometry builder (called only on slider change, never per-frame) ─
// Uses BufferGeometry with pre-allocated Float32Arrays — no per-vertex allocation
const terrainGroup = new THREE.Group();
scene.add(terrainGroup);
function buildTerrainGeometry(dayIndex) {
  // Cache check
  if (terrainCache.has(dayIndex)) {
    cacheStats.terrainHit++;
    updateDiag();
    return terrainCache.get(dayIndex);
  }
  cacheStats.terrainMiss++;
  perTickGeoConstructors++;
  updateDiag();
  const grid = dataSeries[dayIndex];
  const segments = GRID - 1;
  const vertCount = GRID * GRID;
  // Pre-allocate arrays — single allocation per build, never per-frame
  const positions = new Float32Array(vertCount * 3);
  const colors = new Float32Array(vertCount * 3);
  const indices = [];
  // Height range for normalization
  let minRevenue = Infinity, maxRevenue = -Infinity;
  let minDensity = Infinity, maxDensity = -Infinity;
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const d = grid[y][x];
      if (d.revenue < minRevenue) minRevenue = d.revenue;
      if (d.revenue > maxRevenue) maxRevenue = d.revenue;
      if (d.userDensity < minDensity) minDensity = d.userDensity;
      if (d.userDensity > maxDensity) maxDensity = d.userDensity;
    }
  }
  const revRange = maxRevenue - minRevenue || 1;
  const densRange = maxDensity - minDensity || 1;
  // Build vertex positions and colors — single-pass, pre-allocated arrays
  const heightScale = parseFloat(document.getElementById('height-scale').value);
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const idx = y * GRID + x;
      const d = grid[y][x];
      const h = d.revenue * heightScale;
      // Position: stride 3
      positions[idx * 3] = x;
      positions[idx * 3 + 1] = h;
      positions[idx * 3 + 2] = y;
      // Vertex color: vegetation gradient by user density
      // Low density = brown, high density = green
      const t = (d.userDensity - minDensity) / densRange;
      const r = 0.15 + t * 0.05;       // brownish → less brown
      const g = 0.12 + t * 0.55;       // dark → green
      const b = 0.05 + t * 0.08;
      colors[idx * 3] = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  // Build triangle indices — two triangles per grid cell
  for (let y = 0; y < segments; y++) {
    for (let x = 0; x < segments; x++) {
      const a = y * GRID + x;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  // Store in cache
  terrainCache.set(dayIndex, geometry);
  return geometry;
}
// Material: shared instance, never re-created
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.1,
  flatShading: false,
});
let terrainMesh = null;
function updateTerrain(dayIndex) {
  resetPerTickCounters();
  const geometry = buildTerrainGeometry(dayIndex);
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainGroup.remove(terrainMesh);
  }
  terrainMesh = new THREE.Mesh(geometry, terrainMaterial);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  terrainGroup.add(terrainMesh);
  updateDiag();
}
// ── River geometry ──────────────────────────────────────────────────────────
// Trace error paths: find cells where errorRate > threshold, connect into splines
const riversGroup = new THREE.Group();
scene.add(riversGroup);
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
function buildRiverGeometry(dayIndex) {
  if (riverCache.has(dayIndex)) {
    cacheStats.riverHit++;
    updateDiag();
    return riverCache.get(dayIndex);
  }
  cacheStats.riverMiss++;
  perTickGeoConstructors++;
  updateDiag();
  const grid = dataSeries[dayIndex];
  const threshold = 0.15;
  // Find high-error cells as river waypoints
  const errorCells = [];
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      if (grid[y][x].errorRate > threshold) {
        const h = grid[y][x].revenue * parseFloat(document.getElementById('height-scale').value);
        errorCells.push({ x, y, h: h + 0.05, err: grid[y][x].errorRate });
      }
    }
  }
  // Sort cells into river paths using simple nearest-neighbor chaining
  const used = new Set();
  const paths = [];
  for (const cell of errorCells) {
    const key = `${cell.x},${cell.y}`;
    if (used.has(key)) continue;
    const path = [cell];
    used.add(key);
    // Extend path by finding nearest unused error cell (within radius 3)
    let current = cell;
    let extended = true;
    while (extended) {
      extended = false;
      let nearest = null;
      let nearestDist = 3.5;
      for (const other of errorCells) {
        const ok = `${other.x},${other.y}`;
        if (used.has(ok)) continue;
        const dist = Math.sqrt((other.x - current.x) ** 2 + (other.y - current.y) ** 2);
        if (dist < nearestDist) { nearest = other; nearestDist = dist; }
      }
      if (nearest) {
        path.push(nearest);
        used.add(`${nearest.x},${nearest.y}`);
        current = nearest;
        extended = true;
      }
    }
    if (path.length >= 3) paths.push(path);
  }
  // Build tube geometries for each path, reuse single material
  const riverMaterial = new THREE.MeshStandardMaterial({
    color: 0xff3333,
    roughness: 0.3,
    metalness: 0.4,
    emissive: 0x330000,
    emissiveIntensity: 0.6,
  });
  const group = new THREE.Group();
  for (const path of paths) {
    if (path.length < 2) continue;
    // Create CatmullRom curve through path points
    const points = path.map(p => new THREE.Vector3(p.x, p.h, p.y));
    const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 4, 0.15, 8, false);
    const tube = new THREE.Mesh(tubeGeo, riverMaterial);
    tube.castShadow = true;
    group.add(tube);
  }
  riverCache.set(dayIndex, group);
  return group;
}
function updateRivers(dayIndex) {
  // Debounce: clear pending, schedule rebuild after delay
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    // Clear old rivers
    while (riversGroup.children.length > 0) {
      riversGroup.remove(riversGroup.children[0]);
    }
    const riverGroup = buildRiverGeometry(dayIndex);
    // Clone the group contents into riversGroup
    riverGroup.children.forEach(child => {
      riversGroup.add(child.clone());
    });
    updateDiag();
    riverDebounceTimer = null;
  }, RIVER_DEBOUNCE_MS);
}
// ── Particle system for API call trails ─────────────────────────────────────
const particlesGroup = new THREE.Group();
scene.add(particlesGroup);
const PARTICLE_COUNT = 500;
// Pre-allocate position array — reused every frame, never re-allocated
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
// Per-particle state for pathfinding — allocated once
const particleStates = [];
for (let i = 0; i < PARTICLE_COUNT; i++) {
  // Random starting positions on the grid
  particleStates.push({
    x: Math.random() * (GRID - 1),
    z: Math.random() * (GRID - 1),
    vx: (Math.random() - 0.5) * 0.3,
    vz: (Math.random() - 0.5) * 0.3,
    life: Math.random(),
  });
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
// Particle texture: small glowing dot, created once
const particleCanvas = document.createElement('canvas');
particleCanvas.width = 16;
particleCanvas.height = 16;
const pctx = particleCanvas.getContext('2d');
const gradient = pctx.createRadialGradient(8, 8, 0, 8, 8, 8);
gradient.addColorStop(0, 'rgba(255,255,200,1)');
gradient.addColorStop(0.3, 'rgba(255,220,100,0.8)');
gradient.addColorStop(1, 'rgba(255,150,50,0)');
pctx.fillStyle = gradient;
pctx.fillRect(0, 0, 16, 16);
const particleTexture = new THREE.CanvasTexture(particleCanvas);
const particleMaterial = new THREE.PointsMaterial({
  size: 0.25,
  map: particleTexture,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85,
});
const particleSystem = new THREE.Points(particleGeo, particleMaterial);
particlesGroup.add(particleSystem);
let currentDayForParticles = 0;
function updateParticles(dayIndex, dt) {
  currentDayForParticles = dayIndex;
  const grid = dataSeries[dayIndex];
  const heightScale = parseFloat(document.getElementById('height-scale').value);
  // Reuse pre-allocated position/color arrays — zero new allocations
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const p = particleStates[i];
    // Flow toward high-API-call regions (data flow visualization)
    const gx = Math.floor(Math.min(GRID - 1, Math.max(0, p.x)));
    const gz = Math.floor(Math.min(GRID - 1, Math.max(0, p.z)));
    const cell = grid[gz][gx];
    // Gradient toward higher API call density
    let gx2 = gx, gz2 = gz;
    if (gx > 0 && gx < GRID - 1 && gz > 0 && gz < GRID - 1) {
      const neighbors = [
        { dx: 0, dz: -1, v: grid[gz-1]?.[gx]?.apiCalls || 0 },
        { dx: 0, dz: 1, v: grid[gz+1]?.[gx]?.apiCalls || 0 },
        { dx: -1, dz: 0, v: grid[gz]?.[gx-1]?.apiCalls || 0 },
        { dx: 1, dz: 0, v: grid[gz]?.[gx+1]?.apiCalls || 0 },
      ];
      let best = neighbors[0];
      for (const n of neighbors) { if (n.v > best.v) best = n; }
      gx2 = gx + best.dx;
      gz2 = gz + best.dz;
    }
    // Update velocity toward gradient
    p.vx += (gx2 - p.x) * 0.02 * dt;
    p.vz += (gz2 - p.z) * 0.02 * dt;
    // Damping
    p.vx *= 0.98;
    p.vz *= 0.98;
    // Speed clamp
    const speed = Math.sqrt(p.vx * p.vx + p.vz * p.vz);
    const maxSpeed = 0.5;
    if (speed > maxSpeed) { p.vx = (p.vx / speed) * maxSpeed; p.vz = (p.vz / speed) * maxSpeed; }
    p.x += p.vx * dt;
    p.z += p.vz * dt;
    // Wrap around edges
    if (p.x < 0) p.x += GRID - 1;
    if (p.x >= GRID) p.x -= GRID - 1;
    if (p.z < 0) p.z += GRID - 1;
    if (p.z >= GRID) p.z -= GRID - 1;
    // Bilinear height lookup for terrain-following
    const fx = p.x - Math.floor(p.x);
    const fz = p.z - Math.floor(p.z);
    const ix = Math.floor(Math.min(GRID - 1, Math.max(0, p.x)));
    const iz = Math.floor(Math.min(GRID - 1, Math.max(0, p.z)));
    const ix2 = Math.min(GRID - 1, ix + 1);
    const iz2 = Math.min(GRID - 1, iz + 1);
    const h00 = (grid[iz]?.[ix]?.revenue || 0) * heightScale;
    const h10 = (grid[iz]?.[ix2]?.revenue || 0) * heightScale;
    const h01 = (grid[iz2]?.[ix]?.revenue || 0) * heightScale;
    const h11 = (grid[iz2]?.[ix2]?.revenue || 0) * heightScale;
    const h = (h00 * (1-fx) + h10 * fx) * (1-fz) + (h01 * (1-fx) + h11 * fx) * fz;
    // Write to pre-allocated arrays — no allocation
    const i3 = i * 3;
    particlePositions[i3] = p.x;
    particlePositions[i3 + 1] = h + 0.3; // float above terrain
    particlePositions[i3 + 2] = p.z;
    // Color by API call intensity at current cell
    const apiIntensity = Math.min(1, cell.apiCalls / 10);
    particleColors[i3] = 1.0;
    particleColors[i3 + 1] = 0.75 + apiIntensity * 0.25;
    particleColors[i3 + 2] = 0.2 + apiIntensity * 0.3;
  }
  // Mark dirty — Three.js detects this without allocation
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
// ── Memoized world-to-grid transform (for hover/tooltip path) ───────────────
function worldToGrid(worldPos) {
  const key = `${worldPos.x.toFixed(2)},${worldPos.z.toFixed(2)}`;
  if (gridXformMemo.has(key)) {
    cacheStats.gridXformHits++;
    return gridXformMemo.get(key);
  }
  const gx = Math.round(Math.min(GRID - 1, Math.max(0, worldPos.x)));
  const gz = Math.round(Math.min(GRID - 1, Math.max(0, worldPos.z)));
  const result = { gx, gz };
  gridXformMemo.set(key, result);
  return result;
}
// ── Camera bookmarks ────────────────────────────────────────────────────────
const bookmarks = [
  { pos: [GRID/2, 30, GRID/2 + 0.1], target: [GRID/2, 0, GRID/2], label: 'Top-down' },
  { pos: [2, 4, 0], target: [8, 2, 8], label: 'Valley' },
  { pos: [16, 8, 20], target: [12, 3, 8], label: 'Peak' },
  { pos: [0, 6, GRID/2], target: [GRID/2, 2, GRID/2], label: 'Rivers' },
];
function gotoBookmark(idx) {
  if (idx < 0 || idx >= bookmarks.length) return;
  const bm = bookmarks[idx];
  // Animate via simple lerp toward target
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out
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
// ── UI bindings ─────────────────────────────────────────────────────────────
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const heightSlider = document.getElementById('height-scale');
const heightLabel = document.getElementById('height-label');
const btnAutorot = document.getElementById('btn-autorot');
let currentDay = 0;
timeSlider.addEventListener('input', () => {
  currentDay = parseInt(timeSlider.value);
  timeLabel.textContent = `Day ${currentDay + 1}`;
  updateTerrain(currentDay);
  updateRivers(currentDay);
});
heightSlider.addEventListener('input', () => {
  heightLabel.textContent = parseFloat(heightSlider.value).toFixed(1) + 'x';
  // Invalidate terrain cache on height change — heights differ
  terrainCache.clear();
  riverCache.clear();
  cacheStats.terrainHit = 0; cacheStats.terrainMiss = 0;
  cacheStats.riverHit = 0; cacheStats.riverMiss = 0;
  updateTerrain(currentDay);
  updateRivers(currentDay);
});
btnAutorot.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAutorot.textContent = controls.autoRotate ? 'ON' : 'OFF';
  btnAutorot.classList.toggle('active', controls.autoRotate);
});
// Bookmark buttons
document.querySelectorAll('.bm-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.idx);
    gotoBookmark(idx);
  });
});
// Save current view as new bookmark
document.getElementById('btn-save-bm').addEventListener('click', () => {
  const bm = {
    pos: [camera.position.x, camera.position.y, camera.position.z],
    target: [controls.target.x, controls.target.y, controls.target.z],
    label: `View ${bookmarks.length + 1}`,
  };
  bookmarks.push(bm);
  // Add button to bar
  const btn = document.createElement('button');
  btn.className = 'bm-btn';
  btn.textContent = bm.label;
  btn.dataset.idx = bookmarks.length - 1;
  btn.addEventListener('click', () => gotoBookmark(parseInt(btn.dataset.idx)));
  document.getElementById('bookmark-bar').appendChild(btn);
});
// ── Diagnostic panel update ─────────────────────────────────────────────────
function updateDiag() {
  document.getElementById('diag-tcache').textContent =
    `hits:${cacheStats.terrainHit} miss:${cacheStats.terrainMiss}`;
  document.getElementById('diag-rcache').textContent =
    `hits:${cacheStats.riverHit} miss:${cacheStats.riverMiss}`;
  document.getElementById('diag-gcache').textContent =
    `hits:${cacheStats.gridXformHits}`;
  document.getElementById('diag-palloc').textContent =
    `${perFrameAllocs}/frame`;
  document.getElementById('diag-gcon').textContent =
    `${perTickGeoConstructors}/tick`;
}
// FPS tracking
let frameCount = 0;
let lastFpsTime = performance.now();
let currentFps = 60;
// ── Render loop ─────────────────────────────────────────────────────────────
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(0.1, clock.getDelta());
  // Per-frame counter reset
  resetPerFrameCounters();
  controls.update();
  // Update particles each frame — zero allocations, reuses pre-allocated arrays
  updateParticles(currentDay, dt);
  renderer.render(scene, camera);
  // FPS calculation
  frameCount++;
  const now = performance.now();
  if (now - lastFpsTime >= 500) {
    currentFps = Math.round(frameCount / ((now - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = now;
    document.getElementById('diag-fps').textContent = currentFps;
  }
  // Update grid-transform cache hits display every 30 frames
  if (frameCount % 30 === 0) {
    document.getElementById('diag-gcache').textContent =
      `hits:${cacheStats.gridXformHits}`;
  }
}
// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case '1': gotoBookmark(0); break;
    case '2': gotoBookmark(1); break;
    case '3': gotoBookmark(2); break;
    case '4': gotoBookmark(3); break;
    case 'r': controls.autoRotate = !controls.autoRotate;
              btnAutorot.textContent = controls.autoRotate ? 'ON' : 'OFF';
              btnAutorot.classList.toggle('active', controls.autoRotate);
              break;
    case 'f': camera.position.set(GRID/2, 30, GRID/2 + 0.1);
              controls.target.set(GRID/2, 0, GRID/2); controls.update(); break;
  }
});
// ── Initialize ──────────────────────────────────────────────────────────────
updateTerrain(0);
updateRivers(0);
animate();
console.log('3D Data Terrain Explorer initialized.');
console.log(`Grid: ${GRID}x${GRID}, Days: ${DAYS}, Particles: ${PARTICLE_COUNT}`);
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan, 1-4=bookmarks, R=autorot, F=top-down');
</script>
</body>
</html>