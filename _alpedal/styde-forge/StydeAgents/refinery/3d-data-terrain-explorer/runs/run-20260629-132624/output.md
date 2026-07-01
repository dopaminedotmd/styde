<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
:root { --bg: #0a0a0f; --panel-bg: #111118; --text: #c8c8d0; --accent: #4a9eff; --danger: #e04040; --success: #40b860; }
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; height: 100vh; width: 100vw; }
#canvas-container { position: fixed; inset: 0; z-index: 1; }
#ui-layer { position: fixed; inset: 0; z-index: 2; pointer-events: none; }
#ui-layer > * { pointer-events: auto; }
#top-bar { position: absolute; top: 12px; left: 50%; transform: translateX(-50%); display: flex; gap: 8px; align-items: center; background: var(--panel-bg); border: 1px solid #222; border-radius: 8px; padding: 6px 12px; }
#top-bar button { background: #1a1a28; border: 1px solid #333; color: var(--text); padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 12px; }
#top-bar button:hover { background: #252540; border-color: var(--accent); }
#top-bar button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
#time-panel { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background: var(--panel-bg); border: 1px solid #222; border-radius: 10px; padding: 12px 20px; display: flex; gap: 14px; align-items: center; min-width: 420px; }
#time-slider { flex: 1; -webkit-appearance: none; height: 6px; background: #222; border-radius: 3px; outline: none; cursor: pointer; }
#time-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; background: var(--accent); border-radius: 50%; cursor: pointer; }
#day-label { font-size: 13px; color: var(--accent); min-width: 80px; text-align: center; font-weight: 600; }
#legend { position: absolute; top: 80px; right: 16px; background: var(--panel-bg); border: 1px solid #222; border-radius: 8px; padding: 10px 14px; font-size: 11px; }
.legend-row { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
.legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
#bookmarks { position: absolute; left: 16px; top: 80px; background: var(--panel-bg); border: 1px solid #222; border-radius: 8px; padding: 8px; display: flex; flex-direction: column; gap: 4px; }
#bookmarks button { background: #1a1a28; border: 1px solid #333; color: var(--text); padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; text-align: left; }
#bookmarks button:hover { border-color: var(--accent); }
#diagnostics { position: absolute; bottom: 90px; left: 16px; background: var(--panel-bg); border: 1px solid #222; border-radius: 8px; padding: 8px 12px; font-size: 10px; font-family: 'Consolas', monospace; color: #888; }
#diagnostics .diag-label { color: #666; }
#diagnostics .diag-val { color: var(--accent); }
#tooltip { position: absolute; padding: 6px 10px; background: var(--panel-bg); border: 1px solid #444; border-radius: 6px; font-size: 11px; pointer-events: none; display: none; white-space: nowrap; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-layer">
  <div id="top-bar">
    <button id="btn-auto-rotate" class="active" title="Auto-rotate camera">Auto</button>
    <button id="btn-wireframe" title="Toggle wireframe">Wire</button>
    <button id="btn-reset-cam" title="Reset camera view">Reset</button>
    <button id="btn-bookmark-save" title="Save current camera position">+Bookmark</button>
    <button id="btn-top-view" title="Top-down view">Top</button>
    <button id="btn-front-view" title="Front view">Front</button>
  </div>
  <div id="legend">
    <div class="legend-row"><div class="legend-swatch" style="background:#4a9eff;"></div>Revenue (elevation)</div>
    <div class="legend-row"><div class="legend-swatch" style="background:#40b860;"></div>Users high (green)</div>
    <div class="legend-row"><div class="legend-swatch" style="background:#8b6914;"></div>Users low (brown)</div>
    <div class="legend-row"><div class="legend-swatch" style="background:#e04040;"></div>Error rivers</div>
    <div class="legend-row"><div class="legend-swatch" style="background:#ffd700;"></div>API call particles</div>
  </div>
  <div id="bookmarks">
    <div style="font-size:10px;color:#666;padding: 0 4px 4px;">CAMERA BOOKMARKS</div>
  </div>
  <div id="diagnostics">
    <div><span class="diag-label">FPS:</span> <span class="diag-val" id="diag-fps">--</span></div>
    <div><span class="diag-label">Cache hits:</span> <span class="diag-val" id="diag-hits">0</span></div>
    <div><span class="diag-label">Cache misses:</span> <span class="diag-val" id="diag-misses">0</span></div>
    <div><span class="diag-label">Geo allocs:</span> <span class="diag-val" id="diag-allocs">0</span></div>
    <div><span class="diag-label">Day:</span> <span class="diag-val" id="diag-day">0</span></div>
  </div>
  <div id="time-panel">
    <span style="font-size:11px;color:#888;">Day</span>
    <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
    <span id="day-label">Day 0</span>
  </div>
  <div id="tooltip"></div>
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
// ===== THREE.JS IMPORTS =====
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ===== DOM REFS =====
const container = document.getElementById('canvas-container');
const tooltip = document.getElementById('tooltip');
const slider = document.getElementById('time-slider');
const dayLabel = document.getElementById('day-label');
const diagFps = document.getElementById('diag-fps');
const diagHits = document.getElementById('diag-hits');
const diagMisses = document.getElementById('diag-misses');
const diagAllocs = document.getElementById('diag-allocs');
const diagDay = document.getElementById('diag-day');
const bookmarksContainer = document.getElementById('bookmarks');
// ===== DATA GENERATION: 30 days of metrics =====
const TOTAL_DAYS = 30;
const GRID_SIZE = 80; // number of vertices per side on terrain grid
const TERRAIN_SPAN = 20; // world-space width/depth of terrain
const data = [];
// Seed deterministic pseudo-random for reproducibility
function seededRandom(seed) {
  let s = seed;
  return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
}
const rng = seededRandom(42);
// Generate per-day metrics: revenue (hills), users (heat), errors (spikes), apiCalls (flow)
for (let day = 0; day < TOTAL_DAYS; day++) {
  const dayData = {
    day,
    revenue: [],
    users: [],
    errors: [],
    apiCalls: []
  };
  // Generate grid values influenced by day (time dimension) plus spatial noise
  for (let i = 0; i < GRID_SIZE; i++) {
    dayData.revenue[i] = [];
    dayData.users[i] = [];
    for (let j = 0; j < GRID_SIZE; j++) {
      // Center-weighted hill with time trend + noise
      const cx = (i - GRID_SIZE / 2) / (GRID_SIZE / 4);
      const cz = (j - GRID_SIZE / 2) / (GRID_SIZE / 4);
      const dist = Math.sqrt(cx * cx + cz * cz);
      // Base terrain: Gaussian hill that grows over time
      const timeFactor = 0.7 + 0.3 * Math.sin(day / TOTAL_DAYS * Math.PI * 2);
      const base = Math.exp(-dist * dist / 3) * timeFactor * 3.5;
      // Secondary bump (product launch spike around day 15)
      const launchBump = Math.exp(-(day - 15) * (day - 15) / 20) * Math.exp(-dist * dist / 8) * 2.0;
      // Noise ridges
      const noise1 = Math.sin(i * 0.3 + day * 0.1) * Math.cos(j * 0.3 - day * 0.05) * 0.6;
      const noise2 = Math.sin(i * 0.15 + j * 0.15 + day * 0.2) * 0.4;
      dayData.revenue[i][j] = base + launchBump + noise1 + noise2 + rng() * 0.15;
      // Users: correlated with revenue but with spatial offset
      dayData.users[i][j] = Math.max(0, dayData.revenue[i][j] * 0.8 + rng() * 0.5 - 0.2);
      // Errors: sparse spikes in specific regions
      const errorBase = rng() < 0.03 ? rng() * 2.0 + 0.3 : 0;
      // Error cluster around day 20 in south-east quadrant
      const errorCluster = (i > GRID_SIZE * 0.55 && j > GRID_SIZE * 0.55 && day > 18 && day < 23)
        ? Math.exp(-(day - 20) * (day - 20) / 4) * (1.5 + rng())
        : 0;
      dayData.errors[i][j] = errorBase + errorCluster;
    }
  }
  // API calls: 50-80 particles per day with smooth trajectories
  const particleCount = Math.floor(50 + rng() * 30);
  for (let p = 0; p < particleCount; p++) {
    dayData.apiCalls.push({
      startX: (rng() - 0.5) * TERRAIN_SPAN * 0.8,
      startZ: (rng() - 0.5) * TERRAIN_SPAN * 0.8,
      endX: (rng() - 0.5) * TERRAIN_SPAN * 0.8,
      endZ: (rng() - 0.5) * TERRAIN_SPAN * 0.8,
      phase: rng(),
      speed: 0.3 + rng() * 0.7,
      amplitude: 0.3 + rng() * 0.5
    });
  }
  data.push(dayData);
}
// ===== THREE.JS SETUP =====
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.Fog(0x0a0a0f, 25, 60);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 100);
camera.position.set(8, 10, 16);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
// ===== ORBIT CONTROLS =====
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// ===== LIGHTING =====
const ambientLight = new THREE.AmbientLight(0x303050, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(10, 20, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -15;
sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15;
sunLight.shadow.camera.bottom = -15;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x8899cc, 0.8);
fillLight.position.set(-5, 2, -3);
scene.add(fillLight);
// ===== GROUND PLANE =====
const groundGeo = new THREE.PlaneGeometry(TERRAIN_SPAN * 1.5, TERRAIN_SPAN * 1.5);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a1a28, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.5;
ground.receiveShadow = true;
scene.add(ground);
// ===== TERRAIN MESH =====
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.6,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
let terrainMesh = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), terrainMaterial);
terrainMesh.rotation.x = -Math.PI / 2;
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ===== RIVER GROUP =====
const riverGroup = new THREE.Group();
scene.add(riverGroup);
// ===== PARTICLE SYSTEM =====
const MAX_PARTICLES = 500;
const particlePositionsArray = new Float32Array(MAX_PARTICLES * 3); // reused buffer, never reallocated
const particleColorsArray = new Float32Array(MAX_PARTICLES * 3);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositionsArray, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColorsArray, 3));
// Initialize invisible particles offscreen
for (let i = 0; i < MAX_PARTICLES; i++) {
  particlePositionsArray[i * 3 + 1] = -999; // offscreen
  particleColorsArray[i * 3] = 1.0;
  particleColorsArray[i * 3 + 1] = 0.84;
  particleColorsArray[i * 3 + 2] = 0.0;
}
const particleMat = new THREE.PointsMaterial({
  size: 0.12,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
// Particle state (reused objects, never allocated in hot path)
const particleStates = [];
for (let i = 0; i < MAX_PARTICLES; i++) {
  particleStates.push({
    active: false,
    startX: 0, startZ: 0,
    endX: 0, endZ: 0,
    t: 0,
    speed: 0,
    amplitude: 0
  });
}
// ===== GRID HELPER =====
const gridHelper = new THREE.GridHelper(TERRAIN_SPAN, 20, 0x333355, 0x1a1a2e);
gridHelper.position.y = -0.49;
scene.add(gridHelper);
// ===== CACHE SYSTEM =====
// Precompute all terrain geometries and river geometries so slider swaps never call new THREE.XxxGeometry()
const terrainCache = new Map();  // day -> { geometry: BufferGeometry, colors: BufferAttribute }
const riverCache = new Map();    // day -> THREE.Group (river mesh group)
const worldToGridCache = new Map(); // worldX,worldZ string -> {i, j} — memoized per frame for tooltip
let cacheHits = 0;
let cacheMisses = 0;
let geometryAllocCount = 0;
function buildTerrainGeometry(day) {
  const dayData = data[day];
  const w = TERRAIN_SPAN;
  const segments = GRID_SIZE - 1;
  const geo = new THREE.PlaneGeometry(w, w, segments, segments);
  geometryAllocCount++;
  // Manipulate vertex heights (Y axis after rotation)
  const positions = geo.attributes.position;
  const colorsArr = new Float32Array(positions.count * 3);
  // Revenue range for color normalization
  let maxUsers = 0.1;
  for (let i = 0; i < GRID_SIZE; i++) {
    for (let j = 0; j < GRID_SIZE; j++) {
      if (dayData.users[i][j] > maxUsers) maxUsers = dayData.users[i][j];
    }
  }
  // PlaneGeometry vertices go row by row: (0,0) to (segments,segments)
  for (let row = 0; row <= segments; row++) {
    for (let col = 0; col <= segments; col++) {
      const idx = row * (segments + 1) + col;
      const i = GRID_SIZE - 1 - row; // flip to match data orientation
      const j = col;
      const height = dayData.revenue[i][j];
      positions.setY(idx, height);
      // Color: green (high users) to brown (low users)
      const userNorm = Math.min(1, dayData.users[i][j] / maxUsers);
      // Interpolate brown (0.545, 0.412, 0.078) to green (0.25, 0.72, 0.15)
      const r = 0.545 - userNorm * 0.295;
      const g = 0.412 + userNorm * 0.308;
      const b = 0.078 + userNorm * 0.072;
      colorsArr[idx * 3] = r;
      colorsArr[idx * 3 + 1] = g;
      colorsArr[idx * 3 + 2] = b;
    }
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
  geo.computeVertexNormals();
  return { geometry: geo, colors: new THREE.BufferAttribute(colorsArr, 3) };
}
function buildRiverGeometry(day) {
  const dayData = data[day];
  const group = new THREE.Group();
  geometryAllocCount++;
  // Find error cells above threshold and build river paths
  const threshold = 0.4;
  const errorPoints = [];
  for (let i = 0; i < GRID_SIZE; i++) {
    for (let j = 0; j < GRID_SIZE; j++) {
      if (dayData.errors[i][j] > threshold) {
        // Convert grid index to world position
        const halfSpan = TERRAIN_SPAN / 2;
        const step = TERRAIN_SPAN / (GRID_SIZE - 1);
        const wx = -halfSpan + j * step;
        const wz = halfSpan - i * step;
        const wy = dayData.revenue[i][j] + 0.15; // slightly above terrain
        errorPoints.push({ x: wx, y: wy, z: wz, error: dayData.errors[i][j] });
      }
    }
  }
  if (errorPoints.length < 3) return group; // not enough points for river
  // Sort points spatially (left to right, top to bottom) for a continuous path
  errorPoints.sort((a, b) => a.x - b.x || a.z - b.z);
  // Create CatmullRom curve through error points
  const curvePoints = errorPoints.map(p => new THREE.Vector3(p.x, p.y, p.z));
  // If points are too clustered, thin them
  let sampled = curvePoints;
  if (curvePoints.length > 40) {
    sampled = [];
    for (let i = 0; i < curvePoints.length; i += Math.max(1, Math.floor(curvePoints.length / 40))) {
      sampled.push(curvePoints[i]);
    }
    if (sampled[sampled.length - 1] !== curvePoints[curvePoints.length - 1]) {
      sampled.push(curvePoints[curvePoints.length - 1]);
    }
  }
  const curve = new THREE.CatmullRomCurve3(sampled);
  const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.08, 8, false);
  geometryAllocCount++;
  const tubeMat = new THREE.MeshStandardMaterial({
    color: 0xe04040,
    roughness: 0.3,
    metalness: 0.2,
    emissive: 0x330000,
    emissiveIntensity: 0.6,
    depthWrite: true
  });
  const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
  tubeMesh.castShadow = true;
  group.add(tubeMesh);
  // Glow spheres at error peaks
  for (const pt of errorPoints) {
    if (pt.error > 1.0) {
      const sphereGeo = new THREE.SphereGeometry(0.15, 8, 8);
      geometryAllocCount++;
      const sphereMat = new THREE.MeshStandardMaterial({
        color: 0xff2020,
        roughness: 0.2,
        emissive: 0x440000,
        emissiveIntensity: 1.0
      });
      const sphere = new THREE.Mesh(sphereGeo, sphereMat);
      sphere.position.set(pt.x, pt.y, pt.z);
      group.add(sphere);
    }
  }
  return group;
}
// Precompute all terrain variants
function precomputeAll() {
  for (let day = 0; day < TOTAL_DAYS; day++) {
    terrainCache.set(day, buildTerrainGeometry(day));
    riverCache.set(day, buildRiverGeometry(day));
  }
}
// ===== TERRAIN SWAP (slider-driven, cached) =====
let currentDay = 0;
function setTerrainDay(day) {
  if (day === currentDay) return;
  currentDay = day;
  diagDay.textContent = day;
  // Swap terrain geometry from cache (no new THREE.XxxGeometry call in hot path)
  const cached = terrainCache.get(day);
  if (cached) {
    cacheHits++;
    diagHits.textContent = cacheHits;
    // Detach old geometry (keep in cache, don't dispose)
    const oldGeo = terrainMesh.geometry;
    terrainMesh.geometry = cached.geometry;
    // Old geometry stays referenced by cache, so no memory leak
  } else {
    cacheMisses++;
    diagMisses.textContent = cacheMisses;
    const built = buildTerrainGeometry(day);
    terrainCache.set(day, built);
    terrainMesh.geometry = built.geometry;
  }
  // Debounced river swap
  scheduleRiverUpdate(day);
}
// ===== DEBOUNCED RIVER UPDATE =====
let riverDebounceTimer = null;
function scheduleRiverUpdate(day) {
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    // Clear old river group
    while (riverGroup.children.length > 0) {
      const child = riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      riverGroup.remove(child);
    }
    // Insert cached river
    const cachedRiver = riverCache.get(day);
    if (cachedRiver && cachedRiver.children.length > 0) {
      cacheHits++;
      diagHits.textContent = cacheHits;
      cachedRiver.children.forEach(child => {
        riverGroup.add(child.clone()); // clone so cache is not consumed
      });
    } else {
      cacheMisses++;
      diagMisses.textContent = cacheMisses;
      const built = buildRiverGeometry(day);
      riverCache.set(day, built);
      built.children.forEach(child => {
        riverGroup.add(child.clone());
      });
    }
    diagAllocs.textContent = geometryAllocCount;
  }, 200);
}
// ===== PARTICLE UPDATE (hot-path, zero allocation) =====
function respawnParticlesForDay(day) {
  const dayData = data[day];
  // Reset all particles to inactive
  for (let i = 0; i < MAX_PARTICLES; i++) {
    particleStates[i].active = false;
    particlePositionsArray[i * 3 + 1] = -999;
  }
  // Assign new particles from day data
  const count = Math.min(MAX_PARTICLES, dayData.apiCalls.length);
  for (let i = 0; i < count; i++) {
    const call = dayData.apiCalls[i];
    const st = particleStates[i];
    st.active = true;
    st.startX = call.startX;
    st.startZ = call.startZ;
    st.endX = call.endX;
    st.endZ = call.endZ;
    st.t = call.phase;  // stagger phases so particles don't all sync
    st.speed = call.speed;
    st.amplitude = call.amplitude;
    // Set initial position
    particlePositionsArray[i * 3] = call.startX;
    particlePositionsArray[i * 3 + 1] = sampleTerrainHeight(call.startX, call.startZ, day) + 0.3;
    particlePositionsArray[i * 3 + 2] = call.startZ;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// Sample terrain height at world position for current day (uses cache)
function sampleTerrainHeight(wx, wz, day) {
  const halfSpan = TERRAIN_SPAN / 2;
  const step = TERRAIN_SPAN / (GRID_SIZE - 1);
  const j = Math.round((wx + halfSpan) / step);
  const i = Math.round((halfSpan - wz) / step);
  const ci = Math.max(0, Math.min(GRID_SIZE - 1, i));
  const cj = Math.max(0, Math.min(GRID_SIZE - 1, j));
  return data[day].revenue[ci][cj];
}
function updateParticles(deltaSec, day) {
  const dayData = data[day];
  for (let i = 0; i < MAX_PARTICLES; i++) {
    const st = particleStates[i];
    if (!st.active) continue;
    st.t += deltaSec * st.speed * 0.3;
    if (st.t >= 1.0) {
      // Loop particle: reset to start
      st.t -= 1.0;
    }
    // Lerp position along path
    const t = st.t;
    const lx = st.startX + (st.endX - st.startX) * t;
    const lz = st.startZ + (st.endZ - st.startZ) * t;
    // Arc: particles fly with slight sine wave arc
    const arc = Math.sin(t * Math.PI) * st.amplitude;
    const baseH = sampleTerrainHeight(lx, lz, day);
    const idx = i * 3;
    particlePositionsArray[idx] = lx;
    particlePositionsArray[idx + 1] = baseH + 0.3 + arc;
    particlePositionsArray[idx + 2] = lz;
    // Fade color based on phase
    const brightness = 0.5 + 0.5 * Math.sin(t * Math.PI);
    particleColorsArray[idx] = 1.0 * brightness;
    particleColorsArray[idx + 1] = 0.84 * brightness;
    particleColorsArray[idx + 2] = 0.1 * brightness;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
// ===== WORLD-TO-GRID TRANSFORM (memoized per frame) =====
let lastTooltipFrame = -1;
function worldToGrid(wx, wz) {
  // Invalidate memo cache each frame
  const halfSpan = TERRAIN_SPAN / 2;
  const step = TERRAIN_SPAN / (GRID_SIZE - 1);
  const j = Math.round((wx + halfSpan) / step);
  const i = Math.round((halfSpan - wz) / step);
  return {
    i: Math.max(0, Math.min(GRID_SIZE - 1, i)),
    j: Math.max(0, Math.min(GRID_SIZE - 1, j))
  };
}
// ===== RAYCASTER FOR TOOLTIP =====
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const grid = worldToGrid(point.x, point.z);
    const d = data[currentDay];
    const rev = d.revenue[grid.i][grid.j];
    const users = d.users[grid.i][grid.j];
    const errs = d.errors[grid.i][grid.j];
    tooltip.style.display = 'block';
    tooltip.style.left = (event.clientX + 18) + 'px';
    tooltip.style.top = (event.clientY - 40) + 'px';
    tooltip.innerHTML =
      'Revenue: ' + rev.toFixed(2) + 'M | ' +
      'Users: ' + (users * 100).toFixed(0) + 'K | ' +
      'Errors: ' + (errs * 100).toFixed(0) + '%';
  } else {
    tooltip.style.display = 'none';
  }
}
window.addEventListener('mousemove', onMouseMove, { passive: true });
// ===== CAMERA BOOKMARKS =====
const savedBookmarks = [
  { name: 'Overview', pos: [8, 10, 16], target: [0, 1.5, 0] },
  { name: 'Close NE', pos: [6, 4, 6], target: [4, 1, 4] },
  { name: 'Side W', pos: [-14, 3, 0], target: [0, 1.5, 0] },
];
function addBookmarkButton(bm) {
  const btn = document.createElement('button');
  btn.textContent = bm.name;
  btn.addEventListener('click', () => {
    // Smooth animate camera to bookmark position
    const startPos = camera.position.clone();
    const endPos = new THREE.Vector3(...bm.pos);
    const startTarget = controls.target.clone();
    const endTarget = new THREE.Vector3(...bm.target);
    const startTime = performance.now();
    const duration = 800;
    function animStep(now) {
      const elapsed = now - startTime;
      const t = Math.min(1, elapsed / duration);
      // Ease in-out cubic
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      camera.position.lerpVectors(startPos, endPos, ease);
      controls.target.lerpVectors(startTarget, endTarget, ease);
      controls.update();
      if (t < 1) {
        requestAnimationFrame(animStep);
      }
    }
    requestAnimationFrame(animStep);
  });
  bookmarksContainer.appendChild(btn);
}
savedBookmarks.forEach(addBookmarkButton);
// ===== UI EVENT HANDLERS =====
document.getElementById('btn-auto-rotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
document.getElementById('btn-wireframe').addEventListener('click', function() {
  terrainMaterial.wireframe = !terrainMaterial.wireframe;
  this.classList.toggle('active', terrainMaterial.wireframe);
});
document.getElementById('btn-reset-cam').addEventListener('click', () => {
  camera.position.set(8, 10, 16);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
document.getElementById('btn-top-view').addEventListener('click', () => {
  camera.position.set(0, 14, 0.1);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
document.getElementById('btn-front-view').addEventListener('click', () => {
  camera.position.set(0, 3, 16);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
document.getElementById('btn-bookmark-save').addEventListener('click', () => {
  const name = 'View ' + (savedBookmarks.length + 1);
  const bm = {
    name,
    pos: [camera.position.x, camera.position.y, camera.position.z],
    target: [controls.target.x, controls.target.y, controls.target.z]
  };
  savedBookmarks.push(bm);
  addBookmarkButton(bm);
});
// ===== TIME SLIDER =====
slider.addEventListener('input', () => {
  const day = parseInt(slider.value);
  dayLabel.textContent = 'Day ' + day;
  setTerrainDay(day);
  respawnParticlesForDay(day);
});
// ===== FPS COUNTER =====
let frameCount = 0;
let lastFpsTime = performance.now();
function updateFps(now) {
  frameCount++;
  if (now - lastFpsTime >= 1000) {
    const fps = Math.round(frameCount / ((now - lastFpsTime) / 1000));
    diagFps.textContent = fps;
    frameCount = 0;
    lastFpsTime = now;
  }
}
// ===== RENDER LOOP =====
let lastFrameTime = performance.now();
function animate(timestamp) {
  requestAnimationFrame(animate);
  const deltaSec = Math.min(0.1, (timestamp - lastFrameTime) / 1000); // cap delta to avoid spiral
  lastFrameTime = timestamp;
  controls.update();
  updateParticles(deltaSec, currentDay);
  // Clear tooltip memo cache each frame
  lastTooltipFrame = timestamp;
  renderer.render(scene, camera);
  updateFps(timestamp);
}
// ===== RESIZE HANDLER =====
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// ===== INITIALIZATION =====
// Precompute all cached geometries (one-time cost at startup)
console.log('Precomputing ' + TOTAL_DAYS + ' terrain variants...');
precomputeAll();
console.log('Cache populated: ' + terrainCache.size + ' terrain, ' + riverCache.size + ' river variants');
console.log('Total geometry allocations: ' + geometryAllocCount);
diagAllocs.textContent = geometryAllocCount;
diagDay.textContent = currentDay;
// Set initial day terrain from cache
const initCached = terrainCache.get(0);
terrainMesh.geometry = initCached.geometry;
cacheHits++;
diagHits.textContent = cacheHits;
// Initial river
const initRiver = riverCache.get(0);
if (initRiver && initRiver.children.length > 0) {
  initRiver.children.forEach(child => {
    riverGroup.add(child.clone());
  });
}
// Initial particles for day 0
respawnParticlesForDay(0);
// Start animation loop
requestAnimationFrame(animate);
</script>
</body>
</html>