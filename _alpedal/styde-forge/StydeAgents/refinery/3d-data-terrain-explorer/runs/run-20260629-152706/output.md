<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a12;--panel-bg:rgba(10,10,20,0.92);--text:#c8ccd4;--accent:#4fc3f7;--warn:#ef5350;--ok:#66bb6a;--border:rgba(255,255,255,0.08)}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text);height:100vh;width:100vw}
  #canvas-container{position:fixed;inset:0}
  canvas{display:block}
  #panel{position:fixed;top:16px;left:16px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:14px 18px;min-width:220px;backdrop-filter:blur(12px);pointer-events:auto}
  .panel-title{font-size:13px;font-weight:600;letter-spacing:0.04em;color:var(--accent);margin-bottom:10px;text-transform:uppercase}
  .stat-row{display:flex;justify-content:space-between;font-size:11px;padding:3px 0;border-bottom:1px solid var(--border)}
  .stat-label{color:rgba(200,204,212,0.6)}
  .stat-value{font-variant-numeric:tabular-nums;font-weight:500}
  .stat-value.warn{color:var(--warn)}
  .stat-value.ok{color:var(--ok)}
  #time-panel{position:fixed;bottom:28px;left:50%;transform:translateX(-50%);z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:14px 22px;backdrop-filter:blur(12px);display:flex;align-items:center;gap:14px}
  #time-slider{-webkit-appearance:none;width:280px;height:4px;border-radius:2px;background:rgba(255,255,255,0.15);outline:none;cursor:pointer}
  #time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:var(--accent);cursor:pointer;border:2px solid var(--bg)}
  #time-label{font-size:12px;font-variant-numeric:tabular-nums;min-width:64px;text-align:center;font-weight:500}
  #bookmark-bar{position:fixed;top:16px;right:16px;z-index:10;display:flex;gap:6px}
  .bm-btn{background:var(--panel-bg);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:11px;transition:all 0.2s;backdrop-filter:blur(12px)}
  .bm-btn:hover{border-color:var(--accent);color:var(--accent)}
  .bm-btn.save{background:rgba(79,195,247,0.12);border-color:rgba(79,195,247,0.3)}
  #legend{position:fixed;bottom:28px;right:20px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:12px 16px;backdrop-filter:blur(12px);font-size:10px}
  .legend-item{display:flex;align-items:center;gap:8px;padding:2px 0}
  .legend-swatch{width:12px;height:12px;border-radius:3px;flex-shrink:0}
  #cache-panel{position:fixed;top:16px;left:270px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:10px 14px;backdrop-filter:blur(12px);font-size:10px;min-width:150px}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="panel">
  <div class="panel-title">Terrain Metrics</div>
  <div class="stat-row"><span class="stat-label">Time</span><span class="stat-value" id="stat-time">Day 0</span></div>
  <div class="stat-row"><span class="stat-label">Revenue Peak</span><span class="stat-value" id="stat-rev-peak">0</span></div>
  <div class="stat-row"><span class="stat-label">User Density</span><span class="stat-value ok" id="stat-density">0</span></div>
  <div class="stat-row"><span class="stat-label">Error Rate</span><span class="stat-value" id="stat-error">0%</span></div>
  <div class="stat-row"><span class="stat-label">API Calls</span><span class="stat-value" id="stat-api">0</span></div>
</div>
<div id="cache-panel">
  <div class="panel-title">Cache Diagnostics</div>
  <div class="stat-row"><span class="stat-label">Terrain hit</span><span class="stat-value ok" id="cache-terrain-hit">0</span></div>
  <div class="stat-row"><span class="stat-label">Terrain miss</span><span class="stat-value" id="cache-terrain-miss">0</span></div>
  <div class="stat-row"><span class="stat-label">River hit</span><span class="stat-value ok" id="cache-river-hit">0</span></div>
  <div class="stat-row"><span class="stat-label">River miss</span><span class="stat-value" id="cache-river-miss">0</span></div>
  <div class="stat-row"><span class="stat-label">Noise hit</span><span class="stat-value ok" id="cache-noise-hit">0</span></div>
  <div class="stat-row"><span class="stat-label">Noise miss</span><span class="stat-value" id="cache-noise-miss">0</span></div>
  <div class="stat-row"><span class="stat-label">Particle reuse</span><span class="stat-value ok" id="cache-particle">100%</span></div>
</div>
<div id="time-panel">
  <span style="font-size:11px;opacity:0.6">T-15</span>
  <input type="range" id="time-slider" min="0" max="29" value="15" step="1">
  <span style="font-size:11px;opacity:0.6">T+14</span>
  <span id="time-label">Day 15</span>
</div>
<div id="bookmark-bar">
  <button class="bm-btn save" id="bm-save">+ Save View</button>
  <button class="bm-btn" data-bm="0">Overview</button>
  <button class="bm-btn" data-bm="1">Revenue Peaks</button>
  <button class="bm-btn" data-bm="2">Error Rivers</button>
</div>
<div id="legend">
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(to right,#1a3a1a,#4caf50,#cddc39)"></div>Revenue Elevation</div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(to right,#3e2723,#8d6e63,#a5d6a7)"></div>User Density Color</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#ef5350;height:3px;border-radius:2px"></div>Error River</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#4fc3f7;width:6px;height:6px;border-radius:50%"></div>API Call Particle</div>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ── Synthetic time-series data (30 days, 40x40 grid) ──
const GRID = 40;
const DAYS = 30;
const data = (() => {
  const d = [];
  for (let t = 0; t < DAYS; t++) {
    const revenue = new Float32Array(GRID * GRID);
    const users   = new Float32Array(GRID * GRID);
    const errors  = new Float32Array(GRID * GRID);
    const apiCalls = new Float32Array(GRID * GRID);
    for (let y = 0; y < GRID; y++) {
      for (let x = 0; x < GRID; x++) {
        const i = y * GRID + x;
        // Revenue: multi-peak Gaussian landscape that evolves over time
        const cx1 = 10 + Math.sin(t * 0.4) * 4;
        const cy1 = 14 + Math.cos(t * 0.55) * 5;
        const cx2 = 28 - Math.cos(t * 0.35) * 3;
        const cy2 = 30 + Math.sin(t * 0.45) * 4;
        const peak1 = Math.exp(-((x - cx1) ** 2 + (y - cy1) ** 2) / 90);
        const peak2 = Math.exp(-((x - cx2) ** 2 + (y - cy2) ** 2) / 110);
        revenue[i] = peak1 * 0.85 + peak2 * 0.6 + (Math.sin(x * 0.4 + t * 0.15) * Math.cos(y * 0.35) + 1) * 0.08;
        // User density: correlated with revenue but with spatial shift and noise
        users[i] = revenue[i] * 0.7 + (Math.sin(x * 0.5 + t * 0.2) * 0.3 + 0.3);
        // Error rate: spikes where revenue drops sharply
        errors[i] = Math.max(0, (1.0 - revenue[i]) * 0.35 + (Math.sin(x * 0.7 + t * 0.3) * 0.08));
        // API calls: proportional to user density with temporal burst patterns
        apiCalls[i] = users[i] * 180 + Math.sin(t * 0.9 + x * 0.3) * 40;
      }
    }
    d.push({ revenue, users, errors, apiCalls, day: t });
  }
  return d;
})();
// ── Cache infrastructure ──
const cache = {
  terrainGeom: new Map(),       // dayIndex -> BufferGeometry
  terrainHit: 0, terrainMiss: 0,
  riverCurves: new Map(),       // dayIndex -> CatmullRomCurve3 array
  riverGeom: new Map(),         // dayIndex -> TubeGeometry array
  riverHit: 0, riverMiss: 0,
  noiseGrid: new Map(),         // seed -> Float32Array
  noiseHit: 0, noiseMiss: 0,
  bookmarkPositions: [
    { pos: new THREE.Vector3(6, 5, 8), target: new THREE.Vector3(0, 1.2, 0) },
    { pos: new THREE.Vector3(3, 6, -2), target: new THREE.Vector3(0.4, 1.5, 0.6) },
    { pos: new THREE.Vector3(1.5, 3, 3.5), target: new THREE.Vector3(0.5, 1.0, -0.3) }
  ],
  // Memoized world-to-grid transforms for hover path
  gridLookup: { worldPos: null, result: null },
};
function updateCachePanel() {
  document.getElementById('cache-terrain-hit').textContent = cache.terrainHit;
  document.getElementById('cache-terrain-miss').textContent = cache.terrainMiss;
  document.getElementById('cache-river-hit').textContent = cache.riverHit;
  document.getElementById('cache-river-miss').textContent = cache.riverMiss;
  document.getElementById('cache-noise-hit').textContent = cache.noiseHit;
  document.getElementById('cache-noise-miss').textContent = cache.noiseMiss;
}
// ── Three.js setup ──
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.FogExp2(0x0a0a14, 0.00025);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.3, 60);
camera.position.set(4.5, 4.0, 5.5);
camera.lookAt(0, 1.0, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 1.0, 0);
controls.minDistance = 1.5;
controls.maxDistance = 14;
controls.maxPolarAngle = Math.PI * 0.7;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.25;
controls.update();
// Lighting
const ambient = new THREE.AmbientLight(0x303050, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
sun.position.set(8, 12, 4);
sun.castShadow = true;
sun.shadow.mapSize.width = 1024;
sun.shadow.mapSize.height = 1024;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 40;
sun.shadow.camera.left = -8;
sun.shadow.camera.right = 8;
sun.shadow.camera.top = 8;
sun.shadow.camera.bottom = -8;
sun.shadow.bias = -0.0003;
scene.add(sun);
const fillLight = new THREE.DirectionalLight(0x8899cc, 1.2);
fillLight.position.set(-3, 2, -2);
scene.add(fillLight);
// Grid base plane
const gridHelper = new THREE.PolarGridHelper(5, 32, 20, 64, 0x222244, 0x222244);
gridHelper.position.y = -0.02;
scene.add(gridHelper);
// ── Terrain mesh (reference, swapped on time change) ──
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
let terrainMesh = new THREE.Mesh(new THREE.BufferGeometry(), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ── River group ──
const riverGroup = new THREE.Group();
scene.add(riverGroup);
// ── Particle system for API call trails ──
const PARTICLE_COUNT = 1200;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3); // reused, never allocated per frame
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleAlive = new Float32Array(PARTICLE_COUNT); // lifetime remaining
const particleVelocities = []; // pre-allocated velocity refs
// Initialize particle lifetimes and spread them across terrain surface
// Particles spawn at random positions over the terrain, move down-gradient
const particleGeom = new THREE.BufferGeometry();
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.03,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.75,
});
const particleSystem = new THREE.Points(particleGeom, particleMat);
scene.add(particleSystem);
// Pre-allocate particle state arrays (never re-allocated)
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleAlive[i] = Math.random() * 5.0; // stagger initial lifetimes
  particleVelocities.push({ vx: 0, vy: 0, vz: 0 });
}
// ── Create terrain geometry from day data ──
function buildTerrainGeometry(dayData) {
  const { revenue, users } = dayData;
  const size = 4.0;
  const half = size / 2;
  const step = size / (GRID - 1);
  const heightScale = 2.2;
  const vertices = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const indices = [];
  // Build vertex array: height from revenue, color from user density
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const i = y * GRID + x;
      const idx3 = i * 3;
      // Normalize grid coords to world space centered at origin
      vertices[idx3]     = x * step - half;
      vertices[idx3 + 1] = revenue[i] * heightScale;
      vertices[idx3 + 2] = y * step - half;
      // Color: user density maps from brown (low) to green (high) with smooth gradient
      const density = THREE.MathUtils.clamp(users[i], 0, 1);
      const r = 0.09 + density * 0.12;
      const g = 0.18 + density * 0.55;
      const b = 0.06 + density * 0.06;
      colors[idx3]     = r;
      colors[idx3 + 1] = g;
      colors[idx3 + 2] = b;
    }
  }
  // Build triangle indices
  for (let y = 0; y < GRID - 1; y++) {
    for (let x = 0; x < GRID - 1; x++) {
      const a = y * GRID + x;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  // Scale to fit view
  geom.scale(1.25, 1.0, 1.25);
  return geom;
}
// Get or create cached terrain geometry
function getTerrainGeometry(dayIndex) {
  const d = data[dayIndex];
  if (cache.terrainGeom.has(dayIndex)) {
    cache.terrainHit++;
    return cache.terrainGeom.get(dayIndex);
  }
  cache.terrainMiss++;
  const geom = buildTerrainGeometry(d);
  cache.terrainGeom.set(dayIndex, geom);
  return geom;
}
// ── River construction from error data ──
function buildRiverCurves(dayData) {
  const { errors, revenue } = dayData;
  const size = 4.0;
  const half = size / 2;
  const step = size / (GRID - 1);
  const heightScale = 2.2;
  // Find error "seed points" above threshold
  const threshold = 0.18;
  const seeds = [];
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const i = y * GRID + x;
      if (errors[i] > threshold) {
        seeds.push({ x, y, error: errors[i], idx: i });
      }
    }
  }
  // Cluster nearby seeds into river paths using simple flood-fill downhill tracing
  const visited = new Set();
  const rivers = [];
  for (const seed of seeds) {
    if (visited.has(seed.idx)) continue;
    // Trace downhill from seed, following lowest neighbor in revenue
    const path = [];
    let cx = seed.x;
    let cy = seed.y;
    let ci = seed.idx;
    let steps = 0;
    const maxSteps = 50;
    while (steps < maxSteps && cx >= 0 && cx < GRID && cy >= 0 && cy < GRID) {
      const idx = cy * GRID + cx;
      if (visited.has(idx) && steps > 0) break;
      visited.add(idx);
      // World position of this grid point (accounting for geometry scale)
      const wx = (cx * step - half) * 1.25;
      const wz = (cy * step - half) * 1.25;
      const wy = revenue[idx] * heightScale;
      path.push(new THREE.Vector3(wx, wy + 0.01, wz));
      // Find steepest downhill neighbor (lowest revenue)
      let bestNx = cx;
      let bestNy = cy;
      let bestVal = revenue[idx];
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]) {
        const nx = cx + dx;
        const ny = cy + dy;
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        const nidx = ny * GRID + nx;
        if (revenue[nidx] < bestVal && !visited.has(nidx)) {
          bestVal = revenue[nidx];
          bestNx = nx;
          bestNy = ny;
        }
      }
      if (bestNx === cx && bestNy === cy) break; // local minimum reached
      cx = bestNx;
      cy = bestNy;
      ci = cy * GRID + cx;
      steps++;
    }
    if (path.length >= 4) rivers.push(path);
  }
  return rivers;
}
function buildRiverGeometries(riverCurves) {
  const geoms = [];
  const riverMatTemplate = new THREE.MeshStandardMaterial({
    color: 0xef4444,
    roughness: 0.35,
    metalness: 0.15,
    emissive: 0x330000,
    emissiveIntensity: 0.6,
  });
  for (const curvePoints of riverCurves) {
    if (curvePoints.length < 4) continue;
    const curve = new THREE.CatmullRomCurve3(curvePoints, false, 'catmullrom', 0.6);
    const tubeGeom = new THREE.TubeGeometry(curve, Math.min(curvePoints.length * 4, 80), 0.03, 6, false);
    geoms.push({ geom: tubeGeom, mat: riverMatTemplate.clone() });
  }
  return geoms;
}
// Get or create cached river meshes
function getRiverMeshes(dayIndex) {
  if (cache.riverGeom.has(dayIndex)) {
    cache.riverHit++;
    return cache.riverGeom.get(dayIndex);
  }
  cache.riverMiss++;
  const curves = buildRiverCurves(data[dayIndex]);
  const riverData = buildRiverGeometries(curves);
  cache.riverGeom.set(dayIndex, riverData);
  return riverData;
}
// ── Terrain height query (for particles to ride the surface) ──
function sampleTerrainHeight(wx, wz, revenue) {
  // World coords to grid coords (accounting for geometry scale 1.25)
  const size = 4.0;
  const half = size / 2;
  const step = size / (GRID - 1);
  const gx = (wx / 1.25 + half) / step;
  const gz = (wz / 1.25 + half) / step;
  const ix = THREE.MathUtils.clamp(Math.round(gx), 0, GRID - 1);
  const iz = THREE.MathUtils.clamp(Math.round(gz), 0, GRID - 1);
  const heightScale = 2.2;
  return revenue[iz * GRID + ix] * heightScale;
}
// ── Update particles each frame (reuses position array, never allocates) ──
const terrainLookupDay = { day: -1, revenue: null };
function updateParticles(delta, currentRevenue) {
  const size = 4.0;
  const half = size / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particleAlive[i] -= delta;
    const i3 = i * 3;
    const cx = particlePositions[i3];
    const cz = particlePositions[i3 + 2];
    if (particleAlive[i] <= 0 || Math.abs(cx) > 4 || Math.abs(cz) > 4) {
      // Respawn particle at random position on terrain surface
      const rx = (Math.random() - 0.5) * size * 1.2;
      const rz = (Math.random() - 0.5) * size * 1.2;
      const gx = (rx / 1.25 + half) / (size / (GRID - 1));
      const gz = (rz / 1.25 + half) / (size / (GRID - 1));
      const ix = THREE.MathUtils.clamp(Math.round(gx), 0, GRID - 1);
      const iz = THREE.MathUtils.clamp(Math.round(gz), 0, GRID - 1);
      const h = (currentRevenue?.[iz * GRID + ix] ?? 0) * 2.2;
      particlePositions[i3]     = rx;
      particlePositions[i3 + 1] = h + 0.04;
      particlePositions[i3 + 2] = rz;
      particleAlive[i] = 2.5 + Math.random() * 5.0;
      // Random velocity direction (mostly horizontal, slight vertical drift)
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.08 + Math.random() * 0.25;
      particleVelocities[i].vx = Math.cos(angle) * speed;
      particleVelocities[i].vz = Math.sin(angle) * speed;
      particleVelocities[i].vy = 0;
    } else {
      // Move particle horizontally
      particlePositions[i3]     += particleVelocities[i].vx * delta;
      particlePositions[i3 + 2] += particleVelocities[i].vz * delta;
      // Sample terrain height at new position
      const gx = (particlePositions[i3] / 1.25 + half) / (size / (GRID - 1));
      const gz = (particlePositions[i3 + 2] / 1.25 + half) / (size / (GRID - 1));
      const ix = THREE.MathUtils.clamp(Math.round(gx), 0, GRID - 1);
      const iz = THREE.MathUtils.clamp(Math.round(gz), 0, GRID - 1);
      if (currentRevenue) {
        const targetH = currentRevenue[iz * GRID + ix] * 2.2;
        particlePositions[i3 + 1] += (targetH + 0.04 - particlePositions[i3 + 1]) * 6.0 * delta;
      }
    }
    // Color: cyan with slight variation
    particleColors[i3]     = 0.2 + Math.random() * 0.05;
    particleColors[i3 + 1] = 0.65 + Math.random() * 0.15;
    particleColors[i3 + 2] = 0.9 + Math.random() * 0.1;
  }
  particleGeom.attributes.position.needsUpdate = true;
  particleGeom.attributes.color.needsUpdate = true;
}
// ── Apply terrain + rivers for a given day ──
let currentDay = 15;
let debounceTimer = null;
const DEBOUNCE_MS = 200;
function applyDay(dayIndex) {
  currentDay = dayIndex;
  const dayData = data[dayIndex];
  document.getElementById('time-label').textContent = `Day ${dayIndex}`;
  document.getElementById('stat-time').textContent = `Day ${dayIndex}`;
  // Update terrain (cached geometry swap)
  const geom = getTerrainGeometry(dayIndex);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = geom;
  // Update rivers (cached)
  riverGroup.clear();
  const riverMeshes = getRiverMeshes(dayIndex);
  for (const { geom: rGeom, mat } of riverMeshes) {
    const mesh = new THREE.Mesh(rGeom, mat);
    mesh.receiveShadow = true;
    riverGroup.add(mesh);
  }
  // Update stats panel
  const revPeak = Math.max(...dayData.revenue);
  const avgUsers = dayData.users.reduce((a, v) => a + v, 0) / (GRID * GRID);
  const avgError = dayData.errors.reduce((a, v) => a + v, 0) / (GRID * GRID);
  const totalApi = dayData.apiCalls.reduce((a, v) => a + v, 0);
  document.getElementById('stat-rev-peak').textContent = (revPeak * 100).toFixed(1);
  document.getElementById('stat-density').textContent = (avgUsers * 100).toFixed(1);
  document.getElementById('stat-error').textContent = (avgError * 100).toFixed(2) + '%';
  document.getElementById('stat-api').textContent = Math.round(totalApi);
  // Store current revenue for particle terrain lookup
  terrainLookupDay.day = dayIndex;
  terrainLookupDay.revenue = dayData.revenue;
  updateCachePanel();
}
// Slider with debounce
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  const day = parseInt(slider.value);
  document.getElementById('time-label').textContent = `Day ${day}`;
  // Debounce terrain rebuild — only rebuild river geometry after slider settles
  if (debounceTimer) clearTimeout(debounceTimer);
  // Immediately swap terrain (cached geometry, cheap)
  const geom = getTerrainGeometry(day);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = geom;
  terrainLookupDay.day = day;
  terrainLookupDay.revenue = data[day].revenue;
  // Stats update is immediate (cheap reads)
  const dayData = data[day];
  const revPeak = Math.max(...dayData.revenue);
  const avgUsers = dayData.users.reduce((a, v) => a + v, 0) / (GRID * GRID);
  document.getElementById('stat-rev-peak').textContent = (revPeak * 100).toFixed(1);
  document.getElementById('stat-density').textContent = (avgUsers * 100).toFixed(1);
  document.getElementById('stat-time').textContent = `Day ${day}`;
  // Defer river rebuild to debounce timer
  debounceTimer = setTimeout(() => {
    applyDay(day);
  }, DEBOUNCE_MS);
});
// ── Bookmark system ──
document.getElementById('bm-save').addEventListener('click', () => {
  const pos = camera.position.clone();
  const target = controls.target.clone();
  cache.bookmarkPositions.push({ pos, target });
  // Create a new bookmark button
  const bar = document.getElementById('bookmark-bar');
  const btn = document.createElement('button');
  btn.className = 'bm-btn';
  btn.dataset.bm = cache.bookmarkPositions.length - 1;
  btn.textContent = `View ${cache.bookmarkPositions.length - 1}`;
  btn.addEventListener('click', () => applyBookmark(btn.dataset.bm));
  bar.appendChild(btn);
});
document.querySelectorAll('.bm-btn[data-bm]').forEach(btn => {
  btn.addEventListener('click', () => applyBookmark(parseInt(btn.dataset.bm)));
});
function applyBookmark(index) {
  const bm = cache.bookmarkPositions[index];
  if (!bm) return;
  // Smooth animate camera to bookmark
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.pos.clone();
  const endTarget = bm.target.clone();
  const duration = 800;
  const startTime = performance.now();
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
}
// ── Keyboard shortcuts ──
window.addEventListener('keydown', (e) => {
  if (e.key === 'r' || e.key === 'R') {
    controls.autoRotate = !controls.autoRotate;
  }
  if (e.key === 'ArrowLeft') {
    slider.value = Math.max(0, currentDay - 1);
    slider.dispatchEvent(new Event('input'));
  }
  if (e.key === 'ArrowRight') {
    slider.value = Math.min(DAYS - 1, currentDay + 1);
    slider.dispatchEvent(new Event('input'));
  }
});
// ── Handle resize ──
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// ── Render loop ──
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1); // cap delta to prevent spiral on tab switch
  controls.update();
  updateParticles(delta, terrainLookupDay.revenue);
  renderer.render(scene, camera);
}
// ── Initialize ──
applyDay(currentDay);
animate();
updateCachePanel();
</script>
</body>
</html>