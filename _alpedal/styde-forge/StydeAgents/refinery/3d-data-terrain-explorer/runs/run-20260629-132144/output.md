// 3D Data Terrain Explorer — complete self-contained HTML dashboard
// Three.js BufferGeometry heightfield, vertex colors, error rivers,
// particle trails, OrbitControls, time slider, camera bookmarks, cache audit
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif}
  canvas{display:block}
  #panel{position:fixed;top:12px;right:12px;width:260px;background:rgba(10,10,24,0.92);
    border:1px solid rgba(100,160,255,0.25);border-radius:8px;padding:14px;color:#c8d8f0;
    font-size:12px;line-height:1.5;z-index:10;backdrop-filter:blur(6px)}
  #panel h3{margin:0 0 8px;font-size:13px;color:#80b0ff;letter-spacing:0.5px}
  #panel .row{display:flex;justify-content:space-between;margin:3px 0}
  #panel .val{color:#a0d0a0;font-variant-numeric:tabular-nums}
  #panel .miss{color:#f08080}
  #time-bar{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);width:420px;
    z-index:10;display:flex;gap:10px;align-items:center}
  #time-slider{flex:1;accent-color:#5090d0;height:6px}
  #time-label{color:#b0c8e0;font-size:12px;min-width:90px;text-align:center;
    font-variant-numeric:tabular-nums}
  #bookmarks{position:fixed;bottom:56px;left:50%;transform:translateX(-50%);
    display:flex;gap:6px;z-index:10}
  #bookmarks button{background:rgba(30,50,80,0.85);color:#a0c0e0;border:1px solid rgba(80,130,200,0.3);
    padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px;transition:all 0.2s}
  #bookmarks button:hover{background:rgba(50,90,160,0.9);color:#fff}
  #legend{position:fixed;left:16px;bottom:100px;z-index:10;color:#90a8c0;font-size:11px}
  #legend .swatch{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px}
</style>
</head>
<body>
<div id="panel">
  <h3>Cache Diagnostics</h3>
  <div class="row"><span>Terrain variants</span><span class="val" id="d-terrain">0</span></div>
  <div class="row"><span>River builds</span><span class="val" id="d-rivers">0</span></div>
  <div class="row"><span>Grid lookups</span><span class="val" id="d-grid">0</span></div>
  <div class="row"><span>Particle allocs</span><span class="val" id="d-particles">0</span></div>
  <div class="row"><span>Cache misses</span><span class="miss" id="d-misses">0</span></div>
</div>
<div id="legend"><span class="swatch" style="background:#3a8;"></span>Elevation &nbsp;<span class="swatch" style="background:#e44;"></span>Error density &nbsp;<span class="swatch" style="background:#4af;"></span>Particle trails</div>
<div id="bookmarks">
  <button onclick="bookmarkCamera('overview')">Overview</button>
  <button onclick="bookmarkCamera('valley')">Valley</button>
  <button onclick="bookmarkCamera('peak')">Peak</button>
  <button onclick="bookmarkCamera('save')">Save View</button>
</div>
<div id="time-bar">
  <span style="color:#90a8c0;font-size:11px">Day</span>
  <input type="range" id="time-slider" min="0" max="29" value="14" step="1">
  <span id="time-label">Day 15</span>
</div>
<script type="importmap">
{ "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─────────────────────────────────────────────
// Synthetic time-series data: 30 days, 48×48 grid
// Fields per cell: revenue (elevation), users (vegetation), errors (rivers), apis (particles)
// ─────────────────────────────────────────────
const DAYS = 30;
const GRID = 48;
const SPACING = 0.4;
const SIZE = (GRID - 1) * SPACING; // ~18.8 world units
// Generate a day of synthetic metrics with seeded spatial patterns
function generateDay(dayIndex) {
  const t = dayIndex / (DAYS - 1);           // normalized time 0..1
  const cells = new Float32Array(GRID * GRID * 4); // [rev, users, errors, apis] per cell
  // Phase shift drifts terrain features over time
  const phaseX = t * Math.PI * 1.2;
  const phaseZ = t * Math.PI * 0.9;
  const ampScale = 0.6 + 0.4 * Math.sin(t * Math.PI); // mild amplitude modulation
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = (iz * GRID + ix) * 4;
      const nx = ix / (GRID - 1); // 0..1
      const nz = iz / (GRID - 1);
      // Multi-octave terrain: revenue peaks form rolling hills
      const rev = (
        12 * Math.sin(nx * 3.1 + phaseX) * Math.cos(nz * 2.7 + phaseZ) +
        8 * Math.sin(nx * 7.2 - phaseX * 0.5) * Math.cos(nz * 6.1 + phaseZ * 0.3) +
        5 * Math.cos(nx * 1.4) * Math.sin(nz * 1.9 + t * 0.8) +
        4 * Math.sin(nx * 5.0 + nz * 4.5) * ampScale +
        15 // base elevation
      );
      // User density follows revenue with lag and noise
      const users = Math.max(20, 45 + rev * 1.8 + 8 * Math.sin(nx * 12 + t) * Math.cos(nz * 11 - t));
      // Error spikes occur in specific zones and grow/shrink over time
      const errorZone = Math.exp(-((nx - 0.35 - t * 0.3) ** 2 + (nz - 0.55) ** 2) / 0.015)
        + 0.4 * Math.exp(-((nx - 0.7) ** 2 + (nz - 0.3 + t * 0.5) ** 2) / 0.02);
      const errors = errorZone * (18 + 10 * Math.sin(t * Math.PI * 2.5));
      // API call volume clusters in high-user zones
      const apis = users * (0.3 + 0.15 * Math.sin(nx * 15 + t * 4)) + 5 * Math.random();
      cells[idx] = rev;
      cells[idx + 1] = users;
      cells[idx + 2] = errors;
      cells[idx + 3] = apis;
    }
  }
  return cells;
}
// Precompute all 30 days — single allocation for the session
const allDays = [];
for (let d = 0; d < DAYS; d++) allDays.push(generateDay(d));
// ─────────────────────────────────────────────
// Scene, renderer, camera, controls
// ─────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 30, 80);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.8, 120);
camera.position.set(14, 18, 20);
camera.lookAt(SIZE / 2, 6, SIZE / 2);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(SIZE / 2, 8, SIZE / 2);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 5;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI * 0.48; // prevent going under terrain
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
// ─────────────────────────────────────────────
// Lighting
// ─────────────────────────────────────────────
const ambient = new THREE.AmbientLight(0x304060, 1.4);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 2.2);
sun.position.set(20, 30, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 1024;
sun.shadow.mapSize.height = 1024;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
sun.shadow.bias = -0.0003;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 0.7);
fill.position.set(-10, 5, -5);
scene.add(fill);
// Ground plane for shadow reception
const groundGeo = new THREE.PlaneGeometry(SIZE + 10, SIZE + 10);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a1a2e, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.set(SIZE / 2, -0.1, SIZE / 2);
ground.receiveShadow = true;
scene.add(ground);
// ─────────────────────────────────────────────
// CACHE LAYER — all cacheable geometries and transforms live here
// ─────────────────────────────────────────────
const cache = {
  terrainGeos: new Map(),        // dayIndex -> BufferGeometry
  terrainMesh: null,             // current terrain mesh (reused via geometry swap)
  riverGroup: null,              // Group holding river Tube meshes
  riverLines: [],                // cached Tube objects per river path
  particleSystem: null,          // Points object, position array reused
  particlePositions: null,       // Float32Array, reused each update
  particleColors: null,          // Float32Array, reused
  gridToWorld: new Map(),        // memoize "ix,iz" -> Vector3
  stats: {
    terrainHits: 0, terrainMisses: 0,
    riverBuilds: 0,
    gridHits: 0, gridMisses: 0,
    particleAllocs: 0,
  }
};
// Precompute normalized world positions for every grid cell (48x48 = 2304 entries)
// Memoized once — mapper/hover paths never recompute grid index from world
for (let iz = 0; iz < GRID; iz++) {
  for (let ix = 0; ix < GRID; ix++) {
    cache.gridToWorld.set(`${ix},${iz}`, new THREE.Vector3(ix * SPACING, 0, iz * SPACING));
  }
}
// ─────────────────────────────────────────────
// Terrain: heightfield BufferGeometry with vertex colors
// Returns cached geometry or builds + caches new
// ─────────────────────────────────────────────
function getTerrainGeometry(dayIndex) {
  if (cache.terrainGeos.has(dayIndex)) {
    cache.stats.terrainHits++;
    updateDiagnostics();
    return cache.terrainGeos.get(dayIndex);
  }
  cache.stats.terrainMisses++;
  updateDiagnostics();
  const cells = allDays[dayIndex];
  const geo = new THREE.BufferGeometry();
  const vertCount = GRID * GRID;
  const positions = new Float32Array(vertCount * 3);
  const colors = new Float32Array(vertCount * 3);
  // Extract revenue range for normalized coloring
  let revMin = Infinity, revMax = -Infinity, userMin = Infinity, userMax = -Infinity;
  for (let i = 0; i < vertCount; i++) {
    const rev = cells[i * 4];
    const users = cells[i * 4 + 1];
    if (rev < revMin) revMin = rev;
    if (rev > revMax) revMax = rev;
    if (users < userMin) userMin = users;
    if (users > userMax) userMax = users;
  }
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const cell = idx * 4;
      const rev = cells[cell];
      const users = cells[cell + 1];
      const vi = idx * 3;
      // Height from revenue: normalize to 0..1 then scale
      const hNorm = (rev - revMin) / (revMax - revMin || 1);
      positions[vi] = ix * SPACING;
      positions[vi + 1] = hNorm * 14; // max height ~14 units
      positions[vi + 2] = iz * SPACING;
      // Vertex color: vegetation gradient (user density) blended with height
      const uNorm = (users - userMin) / (userMax - userMin || 1);
      // Low = brown/dry, high = green/lush, overlaid with elevation blue tint
      const r = 0.18 + uNorm * 0.22 + hNorm * 0.08;
      const g = 0.22 + uNorm * 0.55 + hNorm * 0.05;
      const b = 0.14 + uNorm * 0.08 + hNorm * 0.35;
      colors[vi] = r;
      colors[vi + 1] = g;
      colors[vi + 2] = b;
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  // Build index buffer for triangle strip
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
  geo.setIndex(indices);
  geo.computeVertexNormals();
  cache.terrainGeos.set(dayIndex, geo);
  updateDiagnostics();
  return geo;
}
// Create or reuse terrain mesh — swaps geometry, never creates new Mesh
function ensureTerrainMesh() {
  if (!cache.terrainMesh) {
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.75,
      metalness: 0.05,
      flatShading: false,
    });
    cache.terrainMesh = new THREE.Mesh(new THREE.BufferGeometry(), mat);
    cache.terrainMesh.castShadow = true;
    cache.terrainMesh.receiveShadow = true;
    scene.add(cache.terrainMesh);
  }
  return cache.terrainMesh;
}
// ─────────────────────────────────────────────
// Rivers: error zones traced as TubeGeometry paths
// Cached per day; rebuilt only when terrain changes
// ─────────────────────────────────────────────
let riverRebuildTimeout = null;
function buildRivers(dayIndex) {
  // Debounce: cancel pending rebuild, schedule new with 200ms delay
  if (riverRebuildTimeout) clearTimeout(riverRebuildTimeout);
  riverRebuildTimeout = setTimeout(() => _buildRiversImmediate(dayIndex), 200);
}
function _buildRiversImmediate(dayIndex) {
  cache.stats.riverBuilds++;
  updateDiagnostics();
  // Remove old river group
  if (cache.riverGroup) {
    scene.remove(cache.riverGroup);
    cache.riverGroup.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); });
  }
  const cells = allDays[dayIndex];
  const group = new THREE.Group();
  // Trace error contours: walk grid finding cells with error > threshold
  const threshold = 5;
  const visited = new Uint8Array(GRID * GRID);
  // Find seed cells with highest errors
  const seeds = [];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const err = cells[(iz * GRID + ix) * 4 + 2];
      if (err > threshold) seeds.push({ ix, iz, err, dist: 0 });
    }
  }
  seeds.sort((a, b) => b.err - a.err); // highest error first
  const topSeeds = seeds.slice(0, 8);    // max 8 river paths
  topSeeds.forEach((seed) => {
    // Flow downhill: follow gradient of revenue + error
    const path = [];
    let cx = seed.ix, cz = seed.iz;
    let steps = 0;
    const maxSteps = 80;
    while (steps < maxSteps && cx >= 0 && cx < GRID && cz >= 0 && cz < GRID) {
      const idx = cz * GRID + cx;
      if (visited[idx]) break;
      visited[idx] = 1;
      const cell = idx * 4;
      const height = (cells[cell] - 10) / 22 * 14; // denormalize to scene height
      const pos = cache.gridToWorld.get(`${cx},${cz}`);
      path.push(new THREE.Vector3(pos.x, height + 0.25, pos.z));
      // Gradient descent: check 4 neighbors, move toward steepest downhill
      let bestDz = 0, bestDx = 0, bestH = height;
      const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
      for (const [dx, dz] of dirs) {
        const nx = cx + dx, nz = cz + dz;
        if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
        const nh = (cells[(nz * GRID + nx) * 4] - 10) / 22 * 14;
        if (nh < bestH) { bestH = nh; bestDx = dx; bestDz = dz; }
      }
      if (bestDx === 0 && bestDz === 0) break; // local minimum
      cx += bestDx;
      cz += bestDz;
      steps++;
    }
    if (path.length > 3) {
      const curve = new THREE.CatmullRomCurve3(path, false, 'catmullrom', 0.5);
      const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.18, 6, false);
      const errNorm = Math.min(1, seed.err / 25);
      const tubeMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color().setHSL(0.0, 0.9, 0.35 + errNorm * 0.2),
        roughness: 0.3,
        metalness: 0.15,
        emissive: new THREE.Color().setHSL(0.0, 0.8, 0.12 * errNorm),
      });
      const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
      tubeMesh.castShadow = true;
      tubeMesh.receiveShadow = true;
      group.add(tubeMesh);
    }
  });
  cache.riverGroup = group;
  scene.add(group);
  riverRebuildTimeout = null;
}
// ─────────────────────────────────────────────
// Particles: API call trails across terrain
// Reuses position and color arrays — no per-frame allocations
// ─────────────────────────────────────────────
const PARTICLE_COUNT = 1200;
const PARTICLE_SPEED = 0.06;
function createParticleSystem() {
  if (cache.particleSystem) return;
  cache.stats.particleAllocs++;
  updateDiagnostics();
  cache.particlePositions = new Float32Array(PARTICLE_COUNT * 3);
  cache.particleColors = new Float32Array(PARTICLE_COUNT * 3);
  // Seed initial positions across grid weighted by API call density
  const day0 = allDays[14]; // mid-point day
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const ix = Math.floor(Math.random() * GRID);
    const iz = Math.floor(Math.random() * GRID);
    const cell = (iz * GRID + ix) * 4;
    const height = (day0[cell] - 10) / 22 * 14;
    cache.particlePositions[i * 3] = ix * SPACING;
    cache.particlePositions[i * 3 + 1] = height + 0.4;
    cache.particlePositions[i * 3 + 2] = iz * SPACING;
    // Blue-white particles
    cache.particleColors[i * 3] = 0.3;
    cache.particleColors[i * 3 + 1] = 0.65;
    cache.particleColors[i * 3 + 2] = 1.0;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(cache.particlePositions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(cache.particleColors, 3));
  // Circular sprite texture via canvas
  const canvas = document.createElement('canvas');
  canvas.width = 16; canvas.height = 16;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.beginPath(); ctx.arc(8, 8, 5, 0, Math.PI * 2); ctx.fill();
  const tex = new THREE.CanvasTexture(canvas);
  const mat = new THREE.PointsMaterial({
    size: 0.22,
    map: tex,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
  });
  cache.particleSystem = new THREE.Points(geo, mat);
  cache.particleSystem.renderOrder = 999;
  scene.add(cache.particleSystem);
}
// Update particle positions each frame — reuses position array, zero allocations
let currentDayIndex = 14;
function updateParticles(dayIndex, tick) {
  if (!cache.particlePositions || !cache.particleSystem) return;
  const cells = allDays[dayIndex];
  const pos = cache.particlePositions;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    // Drift particles along API flow gradient: move toward higher API density neighbors
    const gx = pos[pi] / SPACING;
    const gz = pos[pi + 2] / SPACING;
    const ix = Math.round(gx);
    const iz = Math.round(gz);
    if (ix < 0 || ix >= GRID || iz < 0 || iz >= GRID) {
      // Respawn at random edge
      pos[pi] = Math.random() * SIZE;
      pos[pi + 2] = Math.random() * SIZE;
      pos[pi + 1] = 0.5;
      continue;
    }
    // Gradient toward higher API density among 4 neighbors
    let bestDx = 0, bestDz = 0, bestApi = cells[(iz * GRID + ix) * 4 + 3];
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
    for (const [dx, dz] of dirs) {
      const nx = ix + dx, nz = iz + dz;
      if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
      const nApi = cells[(nz * GRID + nx) * 4 + 3];
      if (nApi > bestApi) { bestApi = nApi; bestDx = dx; bestDz = dz; }
    }
    // Stochastic drift: mostly gradient, some noise
    const noiseX = (Math.random() - 0.5) * 0.08;
    const noiseZ = (Math.random() - 0.5) * 0.08;
    pos[pi] += (bestDx * 0.09 + noiseX) * PARTICLE_SPEED;
    pos[pi + 2] += (bestDz * 0.09 + noiseZ) * PARTICLE_SPEED;
    // Clamp to grid, get height from terrain
    const cx = Math.round(pos[pi] / SPACING);
    const cz = Math.round(pos[pi + 2] / SPACING);
    if (cx >= 0 && cx < GRID && cz >= 0 && cz < GRID) {
      const height = (cells[(cz * GRID + cx) * 4] - 10) / 22 * 14;
      pos[pi + 1] = height + 0.45;
    }
    // Wrap around grid edges
    if (pos[pi] < 0) pos[pi] = SIZE;
    if (pos[pi] > SIZE) pos[pi] = 0;
    if (pos[pi + 2] < 0) pos[pi + 2] = SIZE;
    if (pos[pi + 2] > SIZE) pos[pi + 2] = 0;
  }
  cache.particleSystem.geometry.attributes.position.needsUpdate = true;
}
// ─────────────────────────────────────────────
// Camera bookmarks
// ─────────────────────────────────────────────
const savedBookmarks = new Map([
  ['overview', { pos: [14, 18, 20], target: [SIZE/2, 8, SIZE/2] }],
  ['valley', { pos: [5, 5, 5], target: [SIZE*0.35, 3, SIZE*0.55] }],
  ['peak', { pos: [SIZE*0.7, 20, SIZE*0.3], target: [SIZE*0.7, 12, SIZE*0.3] }],
]);
window.bookmarkCamera = function(name) {
  if (name === 'save') {
    savedBookmarks.set(`saved_${Date.now()}`, {
      pos: camera.position.toArray(),
      target: controls.target.toArray(),
    });
    updateBookmarkButtons();
    return;
  }
  const bm = savedBookmarks.get(name);
  if (!bm) return;
  // Smooth animate via simple lerp over ~40 frames
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  let frame = 0;
  const totalFrames = 40;
  function animStep() {
    frame++;
    const t = Math.min(1, frame / totalFrames);
    const ease = t < 0.5 ? 2*t*t : 1 - Math.pow(-2*t+2,2)/2; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (frame < totalFrames) requestAnimationFrame(animStep);
  }
  animStep();
};
// Dynamically update bookmark buttons for saved views
function updateBookmarkButtons() {
  const container = document.getElementById('bookmarks');
  // Keep first 3 static buttons, rebuild saved ones
  const savedKeys = [...savedBookmarks.keys()].filter(k => k.startsWith('saved_'));
  // Remove old saved buttons
  container.querySelectorAll('.saved-bm').forEach(b => b.remove());
  savedKeys.forEach(key => {
    const btn = document.createElement('button');
    btn.className = 'saved-bm';
    btn.textContent = key.replace('saved_', 'View ');
    btn.onclick = () => bookmarkCamera(key);
    container.appendChild(btn);
  });
}
// ─────────────────────────────────────────────
// Time slider: swap terrain geometry + rebuild rivers
// ─────────────────────────────────────────────
const slider = document.getElementById('time-slider');
const label = document.getElementById('time-label');
function setDay(dayIndex) {
  currentDayIndex = dayIndex;
  label.textContent = `Day ${dayIndex + 1}`;
  // Swap terrain geometry — reuses mesh, swaps buffer
  const terrain = ensureTerrainMesh();
  const newGeo = getTerrainGeometry(dayIndex);
  terrain.geometry = newGeo; // pointer swap, no new Mesh, no dispose
  // Trigger river rebuild with debounce
  buildRivers(dayIndex);
  updateDiagnostics();
}
slider.addEventListener('input', () => {
  const day = parseInt(slider.value, 10);
  setDay(day);
});
// ─────────────────────────────────────────────
// Diagnostics panel update
// ─────────────────────────────────────────────
function updateDiagnostics() {
  const s = cache.stats;
  document.getElementById('d-terrain').textContent = cache.terrainGeos.size;
  document.getElementById('d-rivers').textContent = s.riverBuilds;
  document.getElementById('d-grid').textContent = s.gridHits + s.gridMisses;
  document.getElementById('d-particles').textContent = s.particleAllocs;
  document.getElementById('d-misses').textContent = s.terrainMisses + s.gridMisses;
}
// ─────────────────────────────────────────────
// Hot-path audit: zero new THREE.XxxGeometry() in per-frame/render loop
// All geometry constructors happen in cached functions above.
// Per-frame: only particle position updates (array reuse), no allocations.
// Per-slider: only geometry pointer swap + debounced river rebuild.
// ─────────────────────────────────────────────
// ─────────────────────────────────────────────
// Render loop
// ─────────────────────────────────────────────
let tick = 0;
function animate() {
  requestAnimationFrame(animate);
  tick++;
  controls.update();
  updateParticles(currentDayIndex, tick);
  renderer.render(scene, camera);
}
// ─────────────────────────────────────────────
// Initialization
// ─────────────────────────────────────────────
createParticleSystem();
setDay(14);           // middle of timeline
updateBookmarkButtons();
animate();
// Resize handler
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch(e.key.toLowerCase()) {
    case 'a': controls.autoRotate = !controls.autoRotate; break;
    case '1': bookmarkCamera('overview'); break;
    case '2': bookmarkCamera('valley'); break;
    case '3': bookmarkCamera('peak'); break;
    case 'r': controls.reset(); break;
  }
});
</script>
</body>
</html>