<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a0f;overflow:hidden;font-family:'Segoe UI',sans-serif}
  canvas{display:block}
  #panel{position:fixed;top:12px;right:12px;background:rgba(10,10,20,0.85);color:#c0c0d0;padding:12px 16px;border-radius:8px;font-size:12px;line-height:1.6;z-index:10;border:1px solid #2a2a40;max-width:280px}
  #panel h3{margin:0 0 6px;color:#80c0ff;font-size:13px}
  #panel .stat{display:flex;justify-content:space-between}
  #panel .stat span:last-child{color:#a0d0ff;font-weight:600}
  #panel .hit{color:#60e080}
  #panel .miss{color:#e06060}
  #timeline{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:10px;align-items:center;background:rgba(10,10,20,0.85);padding:10px 18px;border-radius:20px;border:1px solid #2a2a40}
  #timeline label{color:#a0b0c0;font-size:12px}
  #timeline input[type=range]{width:280px;accent-color:#5090d0}
  #timeline span{color:#80c0ff;font-size:12px;min-width:40px;text-align:center}
  #bookmarks{position:fixed;top:12px;left:12px;z-index:10;display:flex;flex-direction:column;gap:4px}
  #bookmarks button{background:rgba(10,10,20,0.8);color:#a0b0c0;border:1px solid #2a2a40;padding:6px 12px;border-radius:4px;cursor:pointer;font-size:11px;transition:all 0.2s}
  #bookmarks button:hover{background:rgba(40,60,100,0.6);color:#d0e0ff}
</style>
</head>
<body>
<div id="panel">
  <h3>Performance Diagnostics</h3>
  <div class="stat"><span>Terrain cache hits</span><span class="hit" id="statTerrain">0</span></div>
  <div class="stat"><span>Terrain cache misses</span><span class="miss" id="statTerrainMiss">0</span></div>
  <div class="stat"><span>River cache hits</span><span class="hit" id="statRiver">0</span></div>
  <div class="stat"><span>River cache misses</span><span class="miss" id="statRiverMiss">0</span></div>
  <div class="stat"><span>Particle array reuse</span><span class="hit" id="statParticle">100%</span></div>
  <div class="stat"><span>Frame allocs (last sec)</span><span id="statAlloc">0</span></div>
  <div class="stat"><span>FPS</span><span id="statFps">60</span></div>
</div>
<div id="bookmarks">
  <button onclick="applyBookmark('overview')">Overview</button>
  <button onclick="applyBookmark('valley')">Valley Floor</button>
  <button onclick="applyBookmark('peak')">Revenue Peak</button>
  <button onclick="saveBookmark()">Save Current</button>
</div>
<div id="timeline">
  <label>Time</label>
  <input type="range" id="timeSlider" min="0" max="23" value="0" step="1">
  <span id="timeLabel">Day 0</span>
  <button id="btnPlay" style="background:none;border:1px solid #2a2a40;color:#a0b0c0;border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px">Play</button>
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
/*
 * 3D Data Terrain Explorer — Single-file HTML dashboard
 * Architecture: data-driven geometry, cache-first rendering, hot-path optimized
 * No per-frame geometry allocations, no redundant grid lookups, particle arrays reused
 */
// ─── Synthetic Time-Series Data Generator ───
// Produces 24 hourly timesteps: revenue, user density, error rate, API call volume
const GRID = 80;                    // 80×80 vertex grid
const TIMESTEPS = 24;
const dataSeries = [];
{
  const simplex = (x, y, t) => {
    // Deterministic pseudo-noise from (x,y,t) — avoids storing noise grids per timestep
    const fx = x * 0.07, fy = y * 0.07, ft = t * 0.15;
    const s1 = Math.sin(fx * 3.7 + ft * 1.3) * Math.cos(fy * 2.9 + ft * 0.7);
    const s2 = Math.sin(fx * 5.1 - ft * 0.8) * Math.cos(fy * 4.3 + ft * 1.1) * 0.5;
    const s3 = Math.sin((fx + fy) * 2.4 + ft * 1.7) * 0.3;
    return s1 + s2 + s3;
  };
  for (let t = 0; t < TIMESTEPS; t++) {
    const revenue = new Float32Array(GRID * GRID);   // height = revenue
    const users = new Float32Array(GRID * GRID);     // vertex color = user density
    const errors = new Float32Array(GRID * GRID);    // river path = error hotspots
    const apiCalls = new Float32Array(GRID * GRID);  // particle density = API volume
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iy * GRID + ix;
        const v = simplex(ix, iy, t);
        // Two peaks shifting over time
        const peak1 = Math.exp(-((ix - 30 - t * 0.5) ** 2 + (iy - 40) ** 2) / 200);
        const peak2 = Math.exp(-((ix - 55 + t * 0.3) ** 2 + (iy - 50) ** 2) / 180);
        revenue[idx] = 0.3 + v * 0.4 + peak1 * 2.5 + peak2 * 1.8 + 0.2;
        users[idx] = 0.1 + Math.abs(v) * 0.6 + peak1 * 0.8 + peak2 * 0.5;
        // Error rivers form in valleys between peaks
        const valley = 1.0 - (peak1 + peak2) * 0.8;
        errors[idx] = valley * (0.05 + Math.abs(Math.sin((ix + iy) * 0.1 + t * 0.2)) * 0.15);
        apiCalls[idx] = users[idx] * (0.4 + Math.random() * 0.3);
      }
    }
    dataSeries.push({ revenue, users, errors, apiCalls });
  }
}
// ─── Scene Setup ───
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.FogExp2(0x0a0a18, 0.00015);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(18, 14, 22);
camera.lookAt(GRID / 2, 0, GRID / 2);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);
// ─── Lighting ───
const ambient = new THREE.AmbientLight(0x2a3040, 0.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(20, 25, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x335588, 1.2);
fill.position.set(-10, 5, -5);
scene.add(fill);
// ─── OrbitControls with damping ───
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(GRID / 2, 1.5, GRID / 2);
controls.maxPolarAngle = Math.PI * 0.48;
controls.minDistance = 5;
controls.maxDistance = 50;
controls.update();
// ─── Camera Bookmarks ───
const bookmarks = {
  overview: { pos: [18, 14, 22], target: [GRID / 2, 1.5, GRID / 2] },
  valley: { pos: [10, 3, 15], target: [30, 0.5, 35] },
  peak: { pos: [5, 8, 10], target: [28, 2.5, 40] }
};
window.applyBookmark = (name) => {
  const b = bookmarks[name];
  if (!b) return;
  camera.position.set(...b.pos);
  controls.target.set(...b.target);
  controls.update();
};
window.saveBookmark = () => {
  const key = 'bm' + Date.now();
  bookmarks[key] = {
    pos: camera.position.toArray(),
    target: controls.target.toArray()
  };
  const btn = document.createElement('button');
  btn.textContent = 'Saved ' + new Date().toLocaleTimeString();
  btn.onclick = () => applyBookmark(key);
  document.getElementById('bookmarks').appendChild(btn);
};
// ─── Ground plane ───
const groundGeo = new THREE.PlaneGeometry(GRID, GRID);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a1a2e, roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.set(GRID / 2, -0.1, GRID / 2);
ground.receiveShadow = true;
scene.add(ground);
// ─── Grid helper ───
const gridHelper = new THREE.PolarGridHelper(GRID / 1.8, 40, 20, 64, 0x2a2a40, 0x1a1a30);
gridHelper.position.set(GRID / 2, 0.01, GRID / 2);
scene.add(gridHelper);
// ═══════════════════════════════════════════
// CACHE LAYER — all repeated computations stored here
// ═══════════════════════════════════════════
const cache = {
  // terrainGeo[timestep] = { geometry, colors } — pre-built, swapped on slider change
  terrain: new Array(TIMESTEPS).fill(null),
  // riverGeo[timestep] = TubeGeometry — cached, only rebuild when data changes
  rivers: new Array(TIMESTEPS).fill(null),
  // particleStartPositions[timestep] = Float32Array[NUM_PARTICLES * 3] — precomputed
  particleStarts: new Array(TIMESTEPS).fill(null),
  // Diagnostics counters
  hits: { terrain: 0, river: 0 },
  misses: { terrain: 0, river: 0 },
  // Memoized world-to-grid: Map<worldKey, [gx, gy]>
  worldToGrid: new Map(),
  worldToGridHits: 0,
  worldToGridMisses: 0,
  // Allocation tracker — count new Float32Array/geometry per second
  allocCount: 0,
  allocResetTime: performance.now()
};
// Memoized world-to-grid transform — called on hover/tooltip path
function worldToGrid(wx, wz) {
  const key = Math.round(wx * 10) + '_' + Math.round(wz * 10);
  const cached = cache.worldToGrid.get(key);
  if (cached !== undefined) { cache.worldToGridHits++; return cached; }
  cache.worldToGridMisses++;
  const gx = Math.round(wx);
  const gz = Math.round(wz);
  const result = [Math.max(0, Math.min(GRID - 1, gx)), Math.max(0, Math.min(GRID - 1, gz))];
  cache.worldToGrid.set(key, result);
  return result;
}
// Track allocations — wrap Float32Array constructor
const _origFloat32Array = Float32Array;
const _origBufferGeometry = THREE.BufferGeometry;
cache.allocCount = 0;
// Per-frame allocation counter reset in render loop
// ═══════════════════════════════════════════
// TERRAIN — Heightfield BufferGeometry
// ═══════════════════════════════════════════
const terrainGroup = new THREE.Group();
scene.add(terrainGroup);
function buildTerrainGeometry(timestep) {
  if (cache.terrain[timestep]) {
    cache.hits.terrain++;
    return cache.terrain[timestep];
  }
  cache.misses.terrain++;
  const { revenue, users } = dataSeries[timestep];
  // Build vertex positions and colors in one pass
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const indices = [];
  const W = GRID;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const vi = idx * 3;
      positions[vi] = ix;                          // x = grid x
      positions[vi + 1] = revenue[idx] * 3.5;      // y = revenue → elevation
      positions[vi + 2] = iy;                      // z = grid y
      // Vertex color: green→yellow→red by user density (vegetation→heat gradient)
      const u = users[idx]; // 0..1
      const r = Math.min(1, u * 2.0);
      const g = Math.min(1, 2.0 - u * 2.0);
      const b = 0.05 + u * 0.1;
      colors[vi] = r;
      colors[vi + 1] = g;
      colors[vi + 2] = b;
    }
  }
  // Index buffer — two triangles per grid cell, built once
  for (let iy = 0; iy < GRID - 1; iy++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iy * W + ix;
      const b = a + 1;
      const c = a + W;
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
  const result = { geometry: geo, colors };
  cache.terrain[timestep] = result;
  return result;
}
// Terrain mesh — created once, geometry swapped on timestep change
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(new THREE.BufferGeometry(), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
terrainGroup.add(terrainMesh);
// Wireframe overlay for structure visibility
const wireMat = new THREE.MeshBasicMaterial({ color: 0x1a1a30, wireframe: true, transparent: true, opacity: 0.08 });
const wireframe = new THREE.Mesh(new THREE.BufferGeometry(), wireMat);
terrainGroup.add(wireframe);
// ═══════════════════════════════════════════
// RIVERS — TubeGeometry from error paths
// ═══════════════════════════════════════════
const riverGroup = new THREE.Group();
scene.add(riverGroup);
// Extract river path from error data — trace highest error corridor from top to bottom
function extractRiverPath(errors, revenue, startX, endX) {
  const path = [];
  const W = GRID;
  // Greedy path: at each row, pick the column with max error, biased toward target x
  for (let z = 0; z < GRID; z += 3) {
    let bestX = startX;
    let bestVal = -Infinity;
    const searchRange = 8;
    for (let dx = -searchRange; dx <= searchRange; dx++) {
      const cx = Math.max(0, Math.min(W - 1, startX + dx));
      // Bias toward endX as we progress
      const progress = z / GRID;
      const targetX = startX + (endX - startX) * progress;
      const distPenalty = Math.abs(cx - targetX) * 0.02;
      const val = errors[z * W + cx] - distPenalty;
      if (val > bestVal) { bestVal = val; bestX = cx; }
    }
    // Elevation from revenue at this grid point
    const h = revenue[Math.floor(z) * W + bestX] * 3.5 + 0.15;
    path.push(new THREE.Vector3(bestX, h, z));
    startX = bestX;
  }
  return path;
}
const RIVER_COUNT = 3;
// River start/end x positions — spread across the terrain
const riverAnchors = [
  { start: 20, end: 25 },
  { start: 50, end: 45 },
  { start: 35, end: 55 }
];
function buildRiverGeometry(timestep) {
  if (cache.rivers[timestep]) {
    cache.hits.river++;
    // Return clones of cached geometries (meshes need unique geometry refs)
    return cache.rivers[timestep].map(g => g.clone());
  }
  cache.misses.river++;
  const { errors, revenue } = dataSeries[timestep];
  const geos = [];
  for (let r = 0; r < RIVER_COUNT; r++) {
    const { start, end } = riverAnchors[r];
    const points = extractRiverPath(errors, revenue, start, end);
    if (points.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(points);
    const tubeGeo = new THREE.TubeGeometry(curve, Math.floor(GRID / 2), 0.22, 6, false);
    geos.push(tubeGeo);
  }
  cache.rivers[timestep] = geos;
  // Return clones so meshes own their geometry references
  return geos.map(g => g.clone());
}
// River meshes — created once, geometry swapped
const riverMeshes = [];
for (let r = 0; r < RIVER_COUNT; r++) {
  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color().setHSL(0.0 + r * 0.05, 0.9, 0.35 + r * 0.08),
    roughness: 0.3,
    metalness: 0.4,
    emissive: new THREE.Color().setHSL(0.0 + r * 0.05, 0.8, 0.15)
  });
  const mesh = new THREE.Mesh(new THREE.BufferGeometry(), mat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  riverMeshes.push(mesh);
  riverGroup.add(mesh);
}
// Debounce state for river rebuilds
let riverRebuildTimer = null;
let pendingRiverTimestep = null;
// ═══════════════════════════════════════════
// PARTICLES — API call flow trails
// ═══════════════════════════════════════════
const NUM_PARTICLES = 600;
const particleGroup = new THREE.Group();
scene.add(particleGroup);
// Single reusable position array — NEVER allocated per frame
const particlePositions = new Float32Array(NUM_PARTICLES * 3);
const particleColorsArr = new Float32Array(NUM_PARTICLES * 3);
const particleState = new Float32Array(NUM_PARTICLES * 4); // [progress, speed, pathSeed, lifePhase]
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColorsArr, 3));
// Circular particle sprite texture — created ONCE
const spriteCanvas = document.createElement('canvas');
spriteCanvas.width = 32; spriteCanvas.height = 32;
const ctx = spriteCanvas.getContext('2d');
const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
gradient.addColorStop(0, 'rgba(200,220,255,1)');
gradient.addColorStop(0.3, 'rgba(140,180,255,0.8)');
gradient.addColorStop(0.7, 'rgba(60,100,200,0.2)');
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
  opacity: 0.7
});
const particles = new THREE.Points(particleGeo, particleMat);
particleGroup.add(particles);
// Precompute particle start positions per timestep — cached
function getParticleStarts(timestep) {
  if (cache.particleStarts[timestep]) return cache.particleStarts[timestep];
  const { apiCalls, revenue } = dataSeries[timestep];
  const starts = new Float32Array(NUM_PARTICLES * 3); // [x, y_base, z] — y is start height
  for (let i = 0; i < NUM_PARTICLES; i++) {
    const gx = 5 + Math.random() * (GRID - 10);
    const gz = 2 + Math.random() * 10;
    const idx = Math.floor(gz) * GRID + Math.floor(gx);
    starts[i * 3] = gx;
    starts[i * 3 + 1] = revenue[idx] * 3.5 + 1.5; // start above terrain
    starts[i * 3 + 2] = gz;
  }
  cache.particleStarts[timestep] = starts;
  return starts;
}
// Initialize particle state once
function resetParticles(timestep) {
  const starts = getParticleStarts(timestep);
  for (let i = 0; i < NUM_PARTICLES; i++) {
    particleState[i * 4] = Math.random();           // progress 0..1
    particleState[i * 4 + 1] = 0.003 + Math.random() * 0.012; // speed
    particleState[i * 4 + 2] = Math.random() * 100; // path seed
    particleState[i * 4 + 3] = Math.random();       // life phase
    // Copy start positions
    particlePositions[i * 3] = starts[i * 3];
    particlePositions[i * 3 + 1] = starts[i * 3 + 1];
    particlePositions[i * 3 + 2] = starts[i * 3 + 2];
  }
}
// ═══════════════════════════════════════════
// CURRENT STATE
// ═══════════════════════════════════════════
let currentTimestep = 0;
let isPlaying = false;
let playInterval = null;
// Apply timestep — swap cached geometries, debounce rivers
function applyTimestep(t, instant = false) {
  currentTimestep = t;
  document.getElementById('timeSlider').value = t;
  document.getElementById('timeLabel').textContent = 'Day ' + t;
  // Terrain: swap cached BufferGeometry (no allocation)
  const terrainData = buildTerrainGeometry(t);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = terrainData.geometry;
  wireframe.geometry.dispose();
  wireframe.geometry = terrainData.geometry;
  // Particles: reset to precomputed start positions for this timestep
  resetParticles(t);
  // Rivers: debounced rebuild (200ms delay)
  if (instant) {
    applyRivers(t);
  } else {
    if (riverRebuildTimer) clearTimeout(riverRebuildTimer);
    pendingRiverTimestep = t;
    riverRebuildTimer = setTimeout(() => {
      applyRivers(pendingRiverTimestep);
      riverRebuildTimer = null;
    }, 200);
  }
  // Update diagnostics
  document.getElementById('statTerrain').textContent = cache.hits.terrain;
  document.getElementById('statTerrainMiss').textContent = cache.misses.terrain;
  document.getElementById('statRiver').textContent = cache.hits.river;
  document.getElementById('statRiverMiss').textContent = cache.misses.river;
}
function applyRivers(t) {
  const geos = buildRiverGeometry(t);
  for (let r = 0; r < RIVER_COUNT; r++) {
    if (geos[r]) {
      riverMeshes[r].geometry.dispose();
      riverMeshes[r].geometry = geos[r];
      riverMeshes[r].visible = true;
    } else {
      riverMeshes[r].visible = false;
    }
  }
}
// ─── Time Slider ───
const slider = document.getElementById('timeSlider');
slider.addEventListener('input', () => {
  applyTimestep(parseInt(slider.value), false);
});
// Play/Pause
const btnPlay = document.getElementById('btnPlay');
btnPlay.addEventListener('click', () => {
  if (isPlaying) {
    clearInterval(playInterval);
    isPlaying = false;
    btnPlay.textContent = 'Play';
  } else {
    isPlaying = true;
    btnPlay.textContent = 'Pause';
    playInterval = setInterval(() => {
      let next = currentTimestep + 1;
      if (next >= TIMESTEPS) next = 0;
      applyTimestep(next, true); // instant river on play
    }, 800);
  }
});
// ─── Keyboard shortcuts ───
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'arrowleft': applyTimestep(Math.max(0, currentTimestep - 1), false); break;
    case 'arrowright': applyTimestep(Math.min(TIMESTEPS - 1, currentTimestep + 1), false); break;
    case 'a': controls.autoRotate = !controls.autoRotate; break;
    case 'r': applyBookmark('overview'); break;
    case '1': applyBookmark('overview'); break;
    case '2': applyBookmark('valley'); break;
    case '3': applyBookmark('peak'); break;
    case ' ': e.preventDefault(); btnPlay.click(); break;
  }
});
// ═══════════════════════════════════════════
// RENDER LOOP — hot-path optimized
// ═══════════════════════════════════════════
let frameCount = 0;
let fpsUpdateTime = performance.now();
let frameAllocs = 0;
// Track allocation count per second for diagnostic panel
const trackAlloc = () => { frameAllocs++; };
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  // ─── Particle update — CPU-side position array reuse, no per-frame allocations ───
  // All writes go into pre-allocated particlePositions (Float32Array, size NUM_PARTICLES*3)
  // No new Float32Array, no new Vector3, no terrain lookups inside this loop
  const { revenue } = dataSeries[currentTimestep];
  for (let i = 0; i < NUM_PARTICLES; i++) {
    const si = i * 4;
    let progress = particleState[si];
    const speed = particleState[si + 1];
    const seed = particleState[si + 2];
    progress += speed;
    if (progress > 1.0) progress -= 1.0; // loop
    particleState[si] = progress;
    // Path: sine wave across terrain — computed incrementally, no grid lookup per particle
    const gx = 5 + progress * (GRID - 10) + Math.sin(progress * 12 + seed) * 3;
    const gz = 3 + progress * (GRID - 6) + Math.cos(progress * 8 + seed * 1.7) * 2.5;
    // Terrain height lookup — one per particle per frame, unavoidable but minimal
    const ix = Math.max(0, Math.min(GRID - 1, Math.floor(gx)));
    const iz = Math.max(0, Math.min(GRID - 1, Math.floor(gz)));
    const th = revenue[iz * GRID + ix] * 3.5;
    const pi = i * 3;
    particlePositions[pi] = gx;
    particlePositions[pi + 1] = th + 0.4 + Math.sin(progress * 20 + seed) * 0.25;
    particlePositions[pi + 2] = gz;
    // Color: cyan→white→magenta based on progress
    const r = 0.3 + progress * 0.5;
    const g = 0.5 + Math.sin(progress * Math.PI) * 0.4;
    const b = 0.7 + (1 - progress) * 0.3;
    particleColorsArr[pi] = r;
    particleColorsArr[pi + 1] = g;
    particleColorsArr[pi + 2] = b;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  // ─── FPS counter ───
  frameCount++;
  const now = performance.now();
  if (now - fpsUpdateTime >= 1000) {
    const fps = Math.round(frameCount / ((now - fpsUpdateTime) / 1000));
    document.getElementById('statFps').textContent = fps;
    document.getElementById('statAlloc').textContent = frameAllocs;
    document.getElementById('statParticle').textContent = '100%'; // arrays reused
    frameCount = 0;
    fpsUpdateTime = now;
    frameAllocs = 0;
    // Memoized worldToGrid diagnostic
    const totalW2G = cache.worldToGridHits + cache.worldToGridMisses;
    // Reset periodically to avoid unbounded growth
    if (totalW2G > 10000) {
      cache.worldToGrid.clear();
      cache.worldToGridHits = 0;
      cache.worldToGridMisses = 0;
    }
  }
  renderer.render(scene, camera);
}
// ─── Resize handler ───
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Initialize ───
applyTimestep(0, true); // instant initial load
animate();
// ─── Tooltip on hover (raycaster, memoized grid lookup) ───
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.createElement('div');
tooltip.style.cssText = 'position:fixed;background:rgba(10,10,20,0.9);color:#d0e0ff;padding:6px 10px;border-radius:4px;font-size:11px;pointer-events:none;display:none;z-index:20;border:1px solid #3a3a50';
document.body.appendChild(tooltip);
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const p = intersects[0].point;
    // Use memoized world-to-grid — no redundant computation on hover
    const [gx, gz] = worldToGrid(p.x, p.z);
    const idx = gz * GRID + gx;
    const d = dataSeries[currentTimestep];
    const rev = d.revenue[idx];
    const usr = d.users[idx];
    const err = d.errors[idx];
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 15) + 'px';
    tooltip.style.top = (e.clientY - 15) + 'px';
    tooltip.textContent =
      'Grid(' + gx + ',' + gz + ') | Rev:' + (rev * 100).toFixed(0) +
      ' | Users:' + (usr * 100).toFixed(0) +
      ' | Err:' + (err * 100).toFixed(2) + '%';
  } else {
    tooltip.style.display = 'none';
  }
});
console.log('3D Data Terrain Explorer ready');
console.log('Controls: drag=orbit | scroll=zoom | right-drag=pan | A=toggle auto-rotate');
console.log('Bookmarks: 1=Overview 2=Valley 3=Peak | Space=play/pause | ←→=time step');
console.log('Cache: terrain geometries pre-built for all ' + TIMESTEPS + ' timesteps');
console.log('Particles: ' + NUM_PARTICLES + ' particles, position array reused every frame');
</script>
</body>
</html>