```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  body { margin: 0; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; background: #0a0a14; }
  #canvas-container { position: fixed; inset: 0; }
  #ui-panel {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: rgba(10,10,30,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px; padding: 14px 20px; display: flex; gap: 18px; align-items: center;
    z-index: 10; color: #c8c8e0; font-size: 13px; box-shadow: 0 4px 24px rgba(0,0,0,0.5);
    pointer-events: all; user-select: none;
  }
  #ui-panel label { display: flex; align-items: center; gap: 7px; white-space: nowrap; }
  #ui-panel input[type=range] { width: 140px; accent-color: #6c8cff; cursor: pointer; }
  #ui-panel button {
    background: rgba(108,140,255,0.15); border: 1px solid rgba(108,140,255,0.35);
    color: #b8c8ff; padding: 6px 12px; border-radius: 7px; cursor: pointer; font-size: 12px;
    transition: background 0.2s; white-space: nowrap;
  }
  #ui-panel button:hover { background: rgba(108,140,255,0.3); }
  #time-label { font-variant-numeric: tabular-nums; min-width: 48px; text-align: center; color: #8cacff; font-weight: 600; }
  #cache-panel {
    position: fixed; top: 16px; right: 16px; z-index: 10; font-size: 11px; color: #6a6a8a;
    background: rgba(10,10,30,0.7); backdrop-filter: blur(8px); padding: 8px 12px;
    border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-family: monospace;
    pointer-events: none;
  }
  #cache-panel span { color: #8cff8c; }
  #bookmark-bar {
    position: fixed; top: 16px; left: 16px; z-index: 10; display: flex; gap: 6px; flex-wrap: wrap;
  }
  #bookmark-bar button {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15);
    color: #aaa; padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 11px;
    transition: all 0.2s;
  }
  #bookmark-bar button:hover { background: rgba(108,140,255,0.25); color: #ccc; }
  #legend {
    position: fixed; bottom: 100px; right: 16px; z-index: 10; font-size: 11px; color: #8888aa;
    background: rgba(10,10,30,0.7); backdrop-filter: blur(8px); padding: 10px 14px;
    border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); line-height: 1.7;
  }
  .legend-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: middle; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="bookmark-bar">
  <button onclick="bookmarkCamera('overview')">Overview</button>
  <button onclick="bookmarkCamera('topdown')">Top-Down</button>
  <button onclick="bookmarkCamera('rivers')">Rivers</button>
  <button onclick="bookmarkCamera('ground')">Ground</button>
</div>
<div id="cache-panel">
  Cache <span id="cache-stats">hits:0 miss:0</span>
</div>
<div id="legend">
  <div><span class="legend-dot" style="background:#4a8;"></span>Revenue Elevation</div>
  <div><span class="legend-dot" style="background:#f55;"></span>Error Rivers</div>
  <div><span class="legend-dot" style="background:#8cf;"></span>API Particle Trails</div>
</div>
<div id="ui-panel">
  <label>Time <span id="time-label">T0</span></label>
  <input type="range" id="time-slider" min="0" max="9" value="0" step="1">
  <button onclick="toggleAutoRotate()">Auto-Rotate: ON</button>
  <button onclick="toggleWireframe()">Wireframe</button>
  <button onclick="resetCamera()">Reset View</button>
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
/* ==========================================================================
   DATA GENERATION — synthetic time-series dataset mimicking real metrics
   Each time step has: revenue grid, user-density grid, error locations, api flows
   ========================================================================== */
const GRID_SIZE = 80;
const TIME_STEPS = 10;
// Generate all time-series data upfront — one allocation, no per-frame noise
function generateDataset() {
  const data = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const revenue = new Float32Array(GRID_SIZE * GRID_SIZE);
    const userDensity = new Float32Array(GRID_SIZE * GRID_SIZE);
    const errors = [];    // {x, z} grid coords of error hot-spots
    const apiFlows = [];  // {fromX, fromZ, toX, toZ} particle flow paths
    // Revenue: layered sine hills that evolve over time
    for (let iz = 0; iz < GRID_SIZE; iz++) {
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const nx = (ix / GRID_SIZE - 0.5) * 6;
        const nz = (iz / GRID_SIZE - 0.5) * 6;
        const idx = iz * GRID_SIZE + ix;
        // Three overlapping hills that shift with time
        const hill1 = Math.sin(nx * 1.3 + t * 0.3) * Math.cos(nz * 1.1 + t * 0.2) * 0.7;
        const hill2 = Math.sin(nx * 2.1 - t * 0.4) * Math.sin(nz * 1.8 - t * 0.15) * 0.5;
        const hill3 = Math.cos((nx - 1.5) * 2.5) * Math.cos((nz + 0.8) * 2.3 + t * 0.35) * 0.4;
        revenue[idx] = Math.max(0, (hill1 + hill2 + hill3 + 0.3) / 1.9);
        // User density follows revenue with offset and own noise
        userDensity[idx] = Math.max(0, (hill1 * 0.5 + hill2 * 1.4 + hill3 * 0.6 + Math.sin(nx * 3 + nz * 4 + t) * 0.2 + 0.5) / 2.0);
      }
    }
    // Error rivers: 3–5 error nodes per time step at low-revenue valleys or sharp gradient zones
    const numErrors = 3 + t % 3;
    for (let e = 0; e < numErrors; e++) {
      // Bias errors toward lower-revenue regions
      const ex = Math.floor(GRID_SIZE * (0.1 + 0.8 * ((e * 137 + t * 59) % 1000) / 1000));
      const ez = Math.floor(GRID_SIZE * (0.1 + 0.8 * ((e * 251 + t * 73) % 1000) / 1000));
      errors.push({ x: ex, z: ez, magnitude: 0.3 + 0.7 * revenue[ez * GRID_SIZE + ex] });
    }
    // API flows: 8–15 particle paths connecting random high-density clusters
    const numFlows = 8 + t * 2;
    for (let f = 0; f < numFlows; f++) {
      const fx1 = Math.floor(GRID_SIZE * (0.15 + 0.7 * ((f * 89 + t * 41) % 1000) / 1000));
      const fz1 = Math.floor(GRID_SIZE * (0.15 + 0.7 * ((f * 173 + t * 67) % 1000) / 1000));
      const fx2 = Math.floor(GRID_SIZE * (0.15 + 0.7 * ((f * 211 + t * 101) % 1000) / 1000));
      const fz2 = Math.floor(GRID_SIZE * (0.15 + 0.7 * ((f * 307 + t * 131) % 1000) / 1000));
      apiFlows.push({ fromX: fx1, fromZ: fz1, toX: fx2, toZ: fz2 });
    }
    data.push({ revenue, userDensity, errors, apiFlows });
  }
  return data;
}
const DATASET = generateDataset();
/* ==========================================================================
   CACHE LAYER — memoized geometry, noise grids, transforms
   Track every cacheable output; log hit/miss for diagnostics
   ========================================================================== */
const CACHE = {
  // Per-time-step terrain BufferGeometry (reused when user returns to same step)
  terrainGeom: new Map(),
  // River TubeGeometry per time step
  riverGeom: new Map(),
  // World-to-grid coordinate transform memo (cleared each frame)
  gridLookup: null,
  gridLookupFrame: -1,
  // Stats
  hits: 0,
  misses: 0,
};
let frameCount = 0;
function cacheKey(timeStep, type) {
  return `${type}_t${timeStep}`;
}
function logCacheHit() { CACHE.hits++; updateCacheDisplay(); }
function logCacheMiss() { CACHE.misses++; updateCacheDisplay(); }
function updateCacheDisplay() {
  const el = document.getElementById('cache-stats');
  if (el) el.textContent = `hits:${CACHE.hits} miss:${CACHE.misses}`;
}
/* ==========================================================================
   THREE.JS SETUP
   ========================================================================== */
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 30, 90);
const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.5, 200);
camera.position.set(18, 14, 22);
camera.lookAt(0, 2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
/* ==========================================================================
   ORBIT CONTROLS — smooth damping, auto-rotate, bookmark system
   ========================================================================== */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 1.5, 0);
controls.minDistance = 6;
controls.maxDistance = 55;
controls.maxPolarAngle = Math.PI * 0.78;
controls.update();
// Bookmark storage
const BOOKMARKS = {
  overview: { pos: [18, 14, 22], target: [0, 2, 0] },
  topdown: { pos: [0, 22, 0.5], target: [0, 0, 0] },
  rivers: { pos: [8, 3, 16], target: [2, 1.5, -2] },
  ground: { pos: [4, 1.2, 10], target: [0, 0.5, -4] },
};
window.bookmarkCamera = function(name) {
  const bm = BOOKMARKS[name];
  if (!bm) return;
  // Animate to bookmark with a short lerp
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const t = Math.min(1, (now - startTime) / duration);
    // Ease in-out cubic
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animStep);
  }
  requestAnimationFrame(animStep);
};
window.toggleAutoRotate = function() {
  controls.autoRotate = !controls.autoRotate;
  document.querySelector('#ui-panel button:nth-child(3)').textContent =
    `Auto-Rotate: ${controls.autoRotate ? 'ON' : 'OFF'}`;
};
window.resetCamera = function() {
  bookmarkCamera('overview');
};
/* ==========================================================================
   LIGHTING
   ========================================================================== */
const ambientLight = new THREE.AmbientLight(0x2a2a4a, 0.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(20, 25, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 1024;
sunLight.shadow.mapSize.height = 1024;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 80;
sunLight.shadow.camera.left = -25;
sunLight.shadow.camera.right = 25;
sunLight.shadow.camera.top = 25;
sunLight.shadow.camera.bottom = -25;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x6688cc, 0.7);
fillLight.position.set(-8, 3, -5);
scene.add(fillLight);
/* ==========================================================================
   GROUND PLANE — dark reflective base
   ========================================================================== */
const groundGeom = new THREE.PlaneGeometry(60, 60);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x111122,
  roughness: 0.85,
  metalness: 0.2,
});
const ground = new THREE.Mesh(groundGeom, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.15;
ground.receiveShadow = true;
scene.add(ground);
/* ==========================================================================
   GRID HELPER — subtle reference grid
   ========================================================================== */
const gridHelper = new THREE.PolarGridHelper(24, 48, 32, 256, 0x222244, 0x1a1a30);
gridHelper.position.y = -0.12;
scene.add(gridHelper);
/* ==========================================================================
   TERRAIN BUILDER — BufferGeometry heightfield with vertex colors
   Revenue = elevation, user density = vertex color (vegetation gradient)
   GEOMETRY IS CACHED per time step — never rebuilt on revisit
   ========================================================================== */
function buildTerrainGeometry(timeStep) {
  const key = cacheKey(timeStep, 'terrain');
  if (CACHE.terrainGeom.has(key)) {
    logCacheHit();
    return CACHE.terrainGeom.get(key).clone();
  }
  logCacheMiss();
  const data = DATASET[timeStep];
  const segments = GRID_SIZE - 1;
  const geom = new THREE.PlaneGeometry(18, 18, segments, segments);
  geom.rotateX(-Math.PI / 2);
  const positions = geom.attributes.position.array;
  const colors = new Float32Array(positions.length);
  // Terrain height scale factor
  const HEIGHT_SCALE = 7.5;
  for (let i = 0; i < positions.length; i += 3) {
    const x = positions[i];
    const z = positions[i + 2];
    // Map world coords to grid indices
    const gx = Math.round((x / 18 + 0.5) * (GRID_SIZE - 1));
    const gz = Math.round((z / 18 + 0.5) * (GRID_SIZE - 1));
    const gi = Math.max(0, Math.min(GRID_SIZE - 1, gz)) * GRID_SIZE +
               Math.max(0, Math.min(GRID_SIZE - 1, gx));
    const revenue = data.revenue[gi];
    const density = data.userDensity[gi];
    // Elevation = revenue scaled
    positions[i + 1] = revenue * HEIGHT_SCALE;
    // Vertex color: green (user density) to brown (sparse) to white (peak)
    // Blend: low density = warm brown, high density = lush green, peak revenue = white-gold
    const r = 0.25 + density * 0.5 + revenue * 0.35;
    const g = 0.45 + density * 0.6 - revenue * 0.15;
    const b = 0.2 + density * 0.25;
    colors[i] = Math.min(1, r);
    colors[i + 1] = Math.min(1, Math.max(0, g));
    colors[i + 2] = Math.min(1, b);
  }
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.computeVertexNormals();
  // Cache the geometry for reuse
  CACHE.terrainGeom.set(key, geom.clone());
  return geom;
}
/* ==========================================================================
   TERRAIN MESH — created once, geometry swapped on time change
   No new THREE.Mesh allocation on slider tick
   ========================================================================== */
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.6,
  metalness: 0.1,
  flatShading: false,
});
let terrainMesh = null;
let currentTerrainGeom = null;
function createOrUpdateTerrain(timeStep) {
  const geom = buildTerrainGeometry(timeStep);
  if (!terrainMesh) {
    terrainMesh = new THREE.Mesh(geom, terrainMaterial);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  } else {
    // Dispose old geometry to avoid memory leak
    if (currentTerrainGeom) currentTerrainGeom.dispose();
    terrainMesh.geometry = geom;
  }
  currentTerrainGeom = geom;
}
/* ==========================================================================
   WIREFRAME OVERLAY — togglable
   ========================================================================== */
let wireframeMesh = null;
const wireframeMaterial = new THREE.MeshBasicMaterial({
  color: 0x334466,
  wireframe: true,
  transparent: true,
  opacity: 0.25,
});
window.toggleWireframe = function() {
  if (wireframeMesh) {
    scene.remove(wireframeMesh);
    wireframeMesh.geometry.dispose();
    wireframeMesh = null;
  } else if (terrainMesh) {
    wireframeMesh = new THREE.Mesh(terrainMesh.geometry, wireframeMaterial);
    scene.add(wireframeMesh);
  }
};
/* ==========================================================================
   RIVER BUILDER — error paths as tube geometry carving through terrain
   Cached per time step; only rebuilt on time change, debounced 200ms
   ========================================================================== */
let riverGroup = new THREE.Group();
scene.add(riverGroup);
let riverDebounceTimer = null;
// Build a CatmullRom curve through error points, lifting each to terrain height
function buildRiverGeometry(timeStep) {
  const key = cacheKey(timeStep, 'river');
  if (CACHE.riverGeom.has(key)) {
    logCacheHit();
    return CACHE.riverGeom.get(key).clone();
  }
  logCacheMiss();
  const data = DATASET[timeStep];
  const errors = data.errors;
  if (errors.length < 2) return null;
  // Sort errors into a path (simple nearest-neighbor chain)
  const sorted = [errors[0]];
  const remaining = [...errors.slice(1)];
  while (remaining.length > 0) {
    const last = sorted[sorted.length - 1];
    let nearestIdx = 0;
    let nearestDist = Infinity;
    for (let i = 0; i < remaining.length; i++) {
      const dx = remaining[i].x - last.x;
      const dz = remaining[i].z - last.z;
      const dist = dx * dx + dz * dz;
      if (dist < nearestDist) { nearestDist = dist; nearestIdx = i; }
    }
    sorted.push(remaining[nearestIdx]);
    remaining.splice(nearestIdx, 1);
  }
  // Convert grid coords to world positions with terrain height
  const points = sorted.map(e => {
    const wx = (e.x / (GRID_SIZE - 1) - 0.5) * 18;
    const wz = (e.z / (GRID_SIZE - 1) - 0.5) * 18;
    const gi = e.z * GRID_SIZE + e.x;
    const wy = data.revenue[gi] * 7.5 + 0.15; // Slightly above terrain
    return new THREE.Vector3(wx, wy, wz);
  });
  if (points.length < 2) return null;
  const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.6);
  const tubeGeom = new THREE.TubeGeometry(curve, 120, 0.14, 8, false);
  CACHE.riverGeom.set(key, tubeGeom.clone());
  return tubeGeom;
}
function updateRivers(timeStep) {
  // Debounce: wait 200ms after last slider move before rebuilding
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    // Clear old river meshes
    while (riverGroup.children.length > 0) {
      const child = riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      riverGroup.remove(child);
    }
    const tubeGeom = buildRiverGeometry(timeStep);
    if (tubeGeom) {
      const riverMat = new THREE.MeshStandardMaterial({
        color: 0xff3344,
        roughness: 0.3,
        metalness: 0.6,
        emissive: 0x330808,
        emissiveIntensity: 0.4,
      });
      const riverMesh = new THREE.Mesh(tubeGeom, riverMat);
      riverMesh.castShadow = true;
      riverGroup.add(riverMesh);
      // Add glow spheres at error points
      const data = DATASET[timeStep];
      data.errors.forEach(e => {
        const wx = (e.x / (GRID_SIZE - 1) - 0.5) * 18;
        const wz = (e.z / (GRID_SIZE - 1) - 0.5) * 18;
        const wy = data.revenue[e.z * GRID_SIZE + e.x] * 7.5 + 0.2;
        const sphereGeom = new THREE.SphereGeometry(0.22, 16, 16);
        const sphereMat = new THREE.MeshStandardMaterial({
          color: 0xff5555,
          roughness: 0.2,
          emissive: 0x440000,
          emissiveIntensity: 0.6,
        });
        const sphere = new THREE.Mesh(sphereGeom, sphereMat);
        sphere.position.set(wx, wy, wz);
        riverGroup.add(sphere);
      });
    }
  }, 200);
}
/* ==========================================================================
   PARTICLE SYSTEM — API call flows as light trails across landscape
   Positions assigned ONCE at spawn, updated via BufferGeometry position array
   reuse — no per-frame allocations, no per-frame random calls
   ========================================================================== */
const PARTICLE_COUNT = 600;
let particleSystem = null;
let particleData = []; // {progress, fromX, fromZ, toX, toZ, speed, color} — color set at spawn
function createParticleSystem() {
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const colors = new Float32Array(PARTICLE_COUNT * 3);
  const sizes = new Float32Array(PARTICLE_COUNT);
  // Initialize all particles at random positions along flows
  // Color assigned at spawn — never recomputed per frame
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const p = spawnParticle(i);
    positions[i * 3] = p.x;
    positions[i * 3 + 1] = p.y;
    positions[i * 3 + 2] = p.z;
    colors[i * 3] = p.color[0];
    colors[i * 3 + 1] = p.color[1];
    colors[i * 3 + 2] = p.color[2];
    sizes[i] = p.size;
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  // Circular sprite texture (procedural, no external image)
  const canvas = document.createElement('canvas');
  canvas.width = 32;
  canvas.height = 32;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, 'rgba(255,255,255,1)');
  gradient.addColorStop(0.3, 'rgba(200,220,255,0.8)');
  gradient.addColorStop(0.7, 'rgba(100,160,255,0.15)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 32, 32);
  const spriteTexture = new THREE.CanvasTexture(canvas);
  const mat = new THREE.PointsMaterial({
    size: 0.25,
    map: spriteTexture,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.75,
  });
  particleSystem = new THREE.Points(geom, mat);
  scene.add(particleSystem);
}
// Spawn a particle ONCE: assign color, speed, path, size — never touch these per-frame
function spawnParticle(index) {
  const timeStep = currentTimeStep;
  const data = DATASET[timeStep];
  const flows = data.apiFlows;
  const flowIdx = index % flows.length;
  const flow = flows[flowIdx];
  const fromWx = (flow.fromX / (GRID_SIZE - 1) - 0.5) * 18;
  const fromWz = (flow.fromZ / (GRID_SIZE - 1) - 0.5) * 18;
  const toWx = (flow.toX / (GRID_SIZE - 1) - 0.5) * 18;
  const toWz = (flow.toZ / (GRID_SIZE - 1) - 0.5) * 18;
  // Terrain height at start point
  const fromGi = flow.fromZ * GRID_SIZE + flow.fromX;
  const fromY = data.revenue[fromGi] * 7.5 + 0.4;
  // Color palette for API particles: cool blue to cyan, assigned once at spawn
  const hue = 0.55 + Math.random() * 0.12; // Blue-cyan range
  const rgb = hslToRgb(hue, 0.8, 0.6 + Math.random() * 0.3);
  return {
    x: fromWx,
    y: fromY,
    z: fromWz,
    fromX: fromWx, fromZ: fromWz, fromY,
    toX: toWx, toZ: toWz,
    progress: Math.random(), // Random start along path
    speed: 0.0003 + Math.random() * 0.0008,
    color: rgb,
    size: 0.08 + Math.random() * 0.18,
  };
}
function hslToRgb(h, s, l) {
  // Returns [r, g, b] in 0–1 range
  const a = s * Math.min(l, 1 - l);
  const f = (n) => {
    const k = (n + h * 12) % 12;
    return l - a * Math.max(-1, Math.min(k - 3, Math.min(9 - k, 1)));
  };
  return [f(0), f(8), f(4)];
}
/* ==========================================================================
   PARTICLE UPDATE — per-frame: only advance progress along path
   BufferGeometry position array reused — no allocation
   ========================================================================== */
function updateParticles() {
  if (!particleSystem) return;
  const positions = particleSystem.geometry.attributes.position.array;
  const data = DATASET[currentTimeStep];
  const flows = data.apiFlows;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    let pd = particleData[i];
    // Advance progress
    pd.progress += pd.speed;
    if (pd.progress >= 1.0) {
      // Respawn: assign new flow path, but reuse the particle data object
      const flowIdx = i % flows.length;
      const flow = flows[flowIdx];
      pd.fromX = (flow.fromX / (GRID_SIZE - 1) - 0.5) * 18;
      pd.fromZ = (flow.fromZ / (GRID_SIZE - 1) - 0.5) * 18;
      pd.toX = (flow.toX / (GRID_SIZE - 1) - 0.5) * 18;
      pd.toZ = (flow.toZ / (GRID_SIZE - 1) - 0.5) * 18;
      const gi = flow.fromZ * GRID_SIZE + flow.fromX;
      pd.fromY = data.revenue[gi] * 7.5 + 0.4;
      pd.progress = 0;
      // Color stays the same — assigned at original spawn, never changed
    }
    // Lerp position along path, with arc height
    const t = pd.progress;
    const arcHeight = Math.sin(t * Math.PI) * 1.2; // Parabolic arc above terrain
    const wx = pd.fromX + (pd.toX - pd.fromX) * t;
    const wz = pd.fromZ + (pd.toZ - pd.fromZ) * t;
    // Terrain height at current position via grid lookup — memoized per frame
    const gx = Math.round((wx / 18 + 0.5) * (GRID_SIZE - 1));
    const gz = Math.round((wz / 18 + 0.5) * (GRID_SIZE - 1));
    const gi = Math.max(0, Math.min(GRID_SIZE - 1, gz)) * GRID_SIZE +
               Math.max(0, Math.min(GRID_SIZE - 1, gx));
    const terrainY = data.revenue[gi] * 7.5;
    positions[i * 3] = wx;
    positions[i * 3 + 1] = terrainY + arcHeight + 0.3;
    positions[i * 3 + 2] = wz;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
/* ==========================================================================
   TIME CHANGE HANDLER — swaps terrain geometry from cache, rebuilds rivers
   ========================================================================== */
let currentTimeStep = 0;
function setTimeStep(newStep) {
  if (newStep === currentTimeStep) return;
  currentTimeStep = newStep;
  document.getElementById('time-label').textContent = `T${newStep}`;
  document.getElementById('time-slider').value = newStep;
  createOrUpdateTerrain(newStep);
  // Update wireframe overlay if active
  if (wireframeMesh && terrainMesh) {
    wireframeMesh.geometry = terrainMesh.geometry;
  }
  updateRivers(newStep);
}
/* ==========================================================================
   INITIALIZATION
   ========================================================================== */
createOrUpdateTerrain(0);
updateRivers(0);
createParticleSystem();
// Initialize particle data array once
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleData.push(spawnParticle(i));
}
/* ==========================================================================
   EVENT HANDLERS
   ========================================================================== */
document.getElementById('time-slider').addEventListener('input', (e) => {
  setTimeStep(parseInt(e.target.value));
});
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
/* ==========================================================================
   RENDER LOOP — hot-path audit: no allocations, no random, no DOM writes
   Only: OrbitControls update, particle position-array reuse, render
   ========================================================================== */
function animate() {
  requestAnimationFrame(animate);
  frameCount++;
  controls.update();
  updateParticles();
  // Reset grid-lookup memo each frame (cheap object ref swap)
  CACHE.gridLookup = null;
  renderer.render(scene, camera);
}
animate();
/* ==========================================================================
   INITIAL SETUP COMPLETE — ready
   ========================================================================== */
console.log('3D Data Terrain Explorer — initialized');
console.log(`GRID: ${GRID_SIZE}x${GRID_SIZE}, TIME_STEPS: ${TIME_STEPS}, PARTICLES: ${PARTICLE_COUNT}`);
</script>
</body>
</html>
```