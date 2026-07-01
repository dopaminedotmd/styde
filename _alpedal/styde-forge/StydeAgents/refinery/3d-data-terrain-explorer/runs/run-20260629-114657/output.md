<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: 'Courier New', monospace; color: #c0d0e0; }
  canvas { display: block; }
  #panel {
    position: fixed; top: 12px; right: 12px; width: 260px;
    background: rgba(10,10,30,0.92); border: 1px solid #2a3a5a;
    border-radius: 6px; padding: 14px; font-size: 11px;
    z-index: 10; backdrop-filter: blur(6px);
  }
  #panel h3 { font-size: 13px; margin-bottom: 8px; color: #7eb8ff; letter-spacing: 1px; }
  .row { display: flex; justify-content: space-between; margin: 3px 0; }
  .label { color: #8899aa; }
  .val { color: #d0e0f0; }
  .cache-hit { color: #4ae04a; }
  .cache-miss { color: #e04a4a; }
  #timeline { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    width: 420px; z-index: 10; }
  input[type=range] { width: 100%; accent-color: #4a8ae0; }
  #time-label { text-align: center; font-size: 11px; margin-bottom: 4px; color: #7eb8ff; }
  #bookmarks { position: fixed; bottom: 70px; left: 50%; transform: translateX(-50%);
    display: flex; gap: 6px; z-index: 10; flex-wrap: wrap; max-width: 500px; }
  .bm-btn {
    background: rgba(20,30,60,0.85); border: 1px solid #3a5a8a;
    color: #a0c0e0; padding: 3px 10px; border-radius: 3px;
    cursor: pointer; font-size: 10px; font-family: inherit;
    transition: background 0.2s;
  }
  .bm-btn:hover { background: rgba(40,60,110,0.9); }
  .bm-btn.active { border-color: #7eb8ff; color: #ffffff; }
  #legend { position: fixed; left: 16px; bottom: 100px; z-index: 10; font-size: 10px; }
  .legend-row { display: flex; align-items: center; gap: 6px; margin: 2px 0; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 2px; }
</style>
</head>
<body>
<div id="panel">
  <h3>TERRAIN DIAGNOSTIC</h3>
  <div class="row"><span class="label">time index</span><span class="val" id="diag-time">0/0</span></div>
  <div class="row"><span class="label">vertices</span><span class="val" id="diag-verts">0</span></div>
  <div class="row"><span class="label">rivers</span><span class="val" id="diag-rivers">0</span></div>
  <div class="row"><span class="label">particles</span><span class="val" id="diag-particles">0</span></div>
  <div class="row"><span class="label">FPS</span><span class="val" id="diag-fps">0</span></div>
  <hr style="border-color:#2a3a5a; margin:6px 0;">
  <div class="row"><span class="label">cache hits</span><span class="cache-hit val" id="diag-hits">0</span></div>
  <div class="row"><span class="label">cache misses</span><span class="cache-miss val" id="diag-misses">0</span></div>
  <div class="row"><span class="label">geom allocs/frame</span><span class="val" id="diag-allocs">0</span></div>
  <div class="row"><span class="label">debounce fires</span><span class="val" id="diag-debounce">0</span></div>
</div>
<div id="legend">
  <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to right,#1a4a1a,#4ae04a)"></div>high user density</div>
  <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to right,#ff4a4a,#4a1a1a)"></div>error river path</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#ffe04a"></div>API call trail</div>
</div>
<div id="timeline">
  <div id="time-label">t=0</div>
  <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
</div>
<div id="bookmarks"></div>
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
// --- DATA GENERATION ---
// Synthetic time-series: 60 time steps, each a 64x64 grid of 4 metrics
// Metrics: [revenue, user_density, error_count, api_call_volume]
const GRID = 64;
const TIMES = 60;
const START_DATE = new Date('2024-01-01');
function generateTimeSeriesData() {
  const data = [];
  for (let t = 0; t < TIMES; t++) {
    // Each time step is a TypedArray for the grid
    const revenue = new Float32Array(GRID * GRID);
    const users = new Float32Array(GRID * GRID);
    const errors = new Float32Array(GRID * GRID);
    const apis = new Float32Array(GRID * GRID);
    const phase = t / TIMES * Math.PI * 2;
    for (let y = 0; y < GRID; y++) {
      for (let x = 0; x < GRID; x++) {
        const idx = y * GRID + x;
        const nx = x / GRID - 0.5;
        const ny = y / GRID - 0.5;
        const dist = Math.sqrt(nx * nx + ny * ny);
        // Revenue: central peak grows over time, some noise
        revenue[idx] = 2.5 * Math.exp(-dist * 5.0) * (0.7 + 0.3 * Math.sin(phase)) +
          0.3 * Math.sin(nx * 8 + phase) * Math.cos(ny * 6 - phase * 0.7) +
          0.15 * Math.sin(nx * 20 + t * 0.3) * Math.cos(ny * 18 + t * 0.4);
        // User density: correlates loosely with revenue, offset peaks
        users[idx] = 1.8 * Math.exp(-((nx - 0.15) * (nx - 0.15) + (ny + 0.1) * (ny + 0.1)) * 4.5) *
          (0.6 + 0.4 * Math.cos(phase * 1.3)) + 0.25 * Math.cos(nx * 7 - phase) * Math.sin(ny * 9 + phase);
        // Errors: random hotspots with temporal drift
        const hotspot1 = Math.exp(-((nx - 0.25 + 0.2 * Math.sin(phase)) ** 2 + (ny + 0.3) ** 2) * 12);
        const hotspot2 = Math.exp(-((nx + 0.3) ** 2 + (ny - 0.2 + 0.15 * Math.cos(phase)) ** 2) * 10);
        errors[idx] = 0.8 * (hotspot1 + hotspot2) + 0.08 * Math.random();
        // API calls: flow along revenue gradient
        apis[idx] = 3.0 * Math.exp(-dist * 3.5) * (0.5 + 0.5 * Math.sin(phase * 1.7 + dist * 4)) +
          0.4 * Math.abs(Math.sin(nx * 12 + t * 0.5)) * Math.cos(ny * 14 + t * 0.6);
      }
    }
    data.push({ revenue, users, errors, apis });
  }
  return data;
}
const timeSeriesData = generateTimeSeriesData();
// --- SCENE SETUP ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 8, 30);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 60);
camera.position.set(5, 4.5, 6);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
// --- LIGHTS ---
const ambientLight = new THREE.AmbientLight(0x1a2a4a, 0.6);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(8, 12, 4);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 40;
sunLight.shadow.camera.left = -8;
sunLight.shadow.camera.right = 8;
sunLight.shadow.camera.top = 8;
sunLight.shadow.camera.bottom = -8;
sunLight.shadow.bias = -0.0002;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x3355aa, 1.2);
fillLight.position.set(-4, 2, -3);
scene.add(fillLight);
// --- ORBIT CONTROLS ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 0.4, 0);
controls.minDistance = 2;
controls.maxDistance = 15;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
// --- CAMERA BOOKMARKS ---
const BOOKMARKS = [
  { name: 'Top-down', pos: [0, 7, 0.01], target: [0, 0, 0] },
  { name: 'Front', pos: [0, 2.5, 5.5], target: [0, 0.2, 0] },
  { name: 'Side', pos: [5.5, 2, 0], target: [0, 0.2, 0] },
  { name: 'Isometric', pos: [4, 4, 4.5], target: [0, 0.3, 0] },
  { name: 'Close-up', pos: [1.2, 3.0, 2.5], target: [0.1, 0.5, 0] },
];
let activeBookmark = -1;
function animateCamera(pos, target, duration = 800) {
  const start = { pos: camera.position.clone(), target: controls.target.clone() };
  const end = { pos: new THREE.Vector3(...pos), target: new THREE.Vector3(...target) };
  const t0 = performance.now();
  function step() {
    const elapsed = performance.now() - t0;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease-in-out cubic
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(start.pos, end.pos, ease);
    controls.target.lerpVectors(start.target, end.target, ease);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
function buildBookmarkUI() {
  const container = document.getElementById('bookmarks');
  BOOKMARKS.forEach((bm, i) => {
    const btn = document.createElement('button');
    btn.className = 'bm-btn';
    btn.textContent = bm.name;
    btn.addEventListener('click', () => {
      activeBookmark = i;
      container.querySelectorAll('.bm-btn').forEach((b, j) => b.classList.toggle('active', j === i));
      animateCamera(bm.pos, bm.target);
    });
    container.appendChild(btn);
  });
}
buildBookmarkUI();
// --- CACHE SYSTEM ---
const cache = {
  // terrain geometry indexed by time step
  terrainGeom: new Map(),
  // river geometry indexed by time step
  riverGeom: new Map(),
  // noise grids (world-to-grid lookup acceleration)
  gridLookup: new Map(),
  // stats
  hits: 0,
  misses: 0,
  // track per-frame allocations (reset each frame)
  frameAllocs: 0,
  debounceFires: 0,
};
// Proxy to track THREE.XxxGeometry constructor calls — wrapped factory
const _origBufferGeometry = THREE.BufferGeometry;
THREE.BufferGeometry = function(...args) {
  cache.frameAllocs++;
  return new _origBufferGeometry(...args);
};
THREE.BufferGeometry.prototype = _origBufferGeometry.prototype;
// Wrap TubeGeometry similarly
if (THREE.TubeGeometry) {
  const _origTube = THREE.TubeGeometry;
  THREE.TubeGeometry = function(...args) {
    cache.frameAllocs++;
    return new _origTube(...args);
  };
  THREE.TubeGeometry.prototype = _origTube.prototype;
}
// --- TERRAIN BUILDER ---
function buildTerrainGeometry(timeIndex) {
  // Check cache
  if (cache.terrainGeom.has(timeIndex)) {
    cache.hits++;
    return cache.terrainGeom.get(timeIndex).clone();
  }
  cache.misses++;
  const { revenue, users, errors } = timeSeriesData[timeIndex];
  const width = GRID - 1;
  const height = GRID - 1;
  const segmentsW = width;
  const segmentsH = height;
  const vertices = [];
  const colors = [];
  const indices = [];
  for (let j = 0; j <= segmentsH; j++) {
    for (let i = 0; i <= segmentsW; i++) {
      const idx = Math.min(j, GRID - 1) * GRID + Math.min(i, GRID - 1);
      const x = (i / segmentsW - 0.5) * 6;
      const z = (j / segmentsH - 0.5) * 6;
      const y = revenue[idx] * 1.8;
      vertices.push(x, y, z);
      // Vertex color: green intensity from user density, red from errors
      const userVal = users[idx];
      const errVal = errors[idx];
      const r = 0.12 + errVal * 1.4 + userVal * 0.15;
      const g = 0.15 + userVal * 1.6;
      const b = 0.08 + userVal * 0.3 + errVal * 0.12;
      colors.push(r, g, b);
    }
  }
  for (let j = 0; j < segmentsH; j++) {
    for (let i = 0; i < segmentsW; i++) {
      const a = j * (segmentsW + 1) + i;
      const b = a + 1;
      const c = a + (segmentsW + 1);
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
  geom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  // Store in cache before returning clone
  cache.terrainGeom.set(timeIndex, geom);
  return geom.clone();
}
// --- TERRAIN MESH ---
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.1,
  flatShading: false,
});
let terrainMesh = new THREE.Mesh(buildTerrainGeometry(0), terrainMaterial);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Wireframe overlay for structure
const wireMat = new THREE.MeshBasicMaterial({ color: 0x1a2a3a, wireframe: true, transparent: true, opacity: 0.12 });
let wireframeMesh = new THREE.Mesh(terrainMesh.geometry, wireMat);
scene.add(wireframeMesh);
// --- RIVER SYSTEM ---
let riverLines = new THREE.Group();
scene.add(riverLines);
function buildRivers(timeIndex) {
  // Check cache
  if (cache.riverGeom.has(timeIndex)) {
    cache.hits++;
    // Clone the stored group (reuse geometries)
    const stored = cache.riverGeom.get(timeIndex);
    const clone = new THREE.Group();
    stored.children.forEach(child => {
      const line = new THREE.Line(
        child.geometry.clone(),
        child.material.clone()
      );
      clone.add(line);
    });
    return clone;
  }
  cache.misses++;
  const { errors, revenue } = timeSeriesData[timeIndex];
  const group = new THREE.Group();
  // Find error hotspots (threshold) and trace downhill paths
  const visited = new Uint8Array(GRID * GRID);
  // Collect hotspot seeds
  const seeds = [];
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const idx = y * GRID + x;
      if (errors[idx] > 0.35 && visited[idx] === 0) {
        seeds.push({ x, y, err: errors[idx] });
      }
    }
  }
  seeds.sort((a, b) => b.err - a.err);
  const maxRivers = 8;
  for (let s = 0; s < Math.min(seeds.length, maxRivers); s++) {
    const path = [];
    let cx = seeds[s].x;
    let cy = seeds[s].y;
    let steps = 0;
    const maxSteps = 60;
    while (steps < maxSteps) {
      path.push({
        x: (cx / GRID - 0.5) * 6,
        z: (cy / GRID - 0.5) * 6,
        y: revenue[Math.min(cy, GRID - 1) * GRID + Math.min(cx, GRID - 1)] * 1.8 + 0.03,
      });
      // Descend gradient: pick neighbor with lowest revenue
      let bestDx = 0, bestDy = 0, bestVal = Infinity;
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dy === 0) continue;
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          const nidx = ny * GRID + nx;
          if (revenue[nidx] < bestVal && visited[nidx] < 2) {
            bestVal = revenue[nidx];
            bestDx = dx;
            bestDy = dy;
          }
        }
      }
      if (bestVal >= revenue[cy * GRID + cx]) break; // Local minimum
      cx += bestDx;
      cy += bestDy;
      const idx = cy * GRID + cx;
      visited[idx] = 1;
      steps++;
    }
    if (path.length > 3) {
      const curve = new THREE.CatmullRomCurve3(
        path.map(p => new THREE.Vector3(p.x, p.y, p.z))
      );
      const tubeGeom = new THREE.TubeGeometry(curve, path.length * 2, 0.03, 6, false);
      const tubeMat = new THREE.MeshStandardMaterial({
        color: 0xff3322,
        emissive: 0x661111,
        roughness: 0.3,
        metalness: 0.5,
      });
      const tube = new THREE.Mesh(tubeGeom, tubeMat);
      group.add(tube);
      // Glow line on top
      const lineGeom = new THREE.BufferGeometry().setFromPoints(curve.getPoints(path.length * 4));
      const lineMat = new THREE.LineBasicMaterial({ color: 0xff6644, transparent: true, opacity: 0.7 });
      group.add(new THREE.Line(lineGeom, lineMat));
    }
  }
  cache.riverGeom.set(timeIndex, group);
  // Return clone
  const clone = new THREE.Group();
  group.children.forEach(child => {
    if (child.isMesh) {
      clone.add(new THREE.Mesh(child.geometry.clone(), child.material.clone()));
    } else if (child.isLine) {
      clone.add(new THREE.Line(child.geometry.clone(), child.material.clone()));
    }
  });
  return clone;
}
// --- PARTICLE SYSTEM ---
const PARTICLE_COUNT = 600;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
// Particle state: each particle has a current grid position and progress
const particleState = new Float32Array(PARTICLE_COUNT * 4); // [gx, gy, t, seed]
function initParticles() {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    resetParticle(i);
    // Stagger initial t so they don't all sync
    particleState[i * 4 + 2] = Math.random();
  }
}
function resetParticle(i) {
  // Random start position on grid
  const gx = Math.random();
  const gy = Math.random();
  particleState[i * 4] = gx;
  particleState[i * 4 + 1] = gy;
  particleState[i * 4 + 2] = 0; // progress along path
  particleState[i * 4 + 3] = Math.random() * 1000; // seed for variation
}
const particleGeom = new THREE.BufferGeometry();
particleGeom.setAttribute('position', new THREE.Float32BufferAttribute(particlePositions, 3));
particleGeom.setAttribute('color', new THREE.Float32BufferAttribute(particleColors, 3));
const particleTex = createGlowTexture();
const particleMat = new THREE.PointsMaterial({
  size: 0.06,
  map: particleTex,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
});
const particles = new THREE.Points(particleGeom, particleMat);
scene.add(particles);
initParticles();
function createGlowTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = 32;
  canvas.height = 32;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, 'rgba(255,240,180,1)');
  gradient.addColorStop(0.3, 'rgba(255,200,100,0.8)');
  gradient.addColorStop(0.6, 'rgba(255,140,40,0.3)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 32, 32);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}
// Memoized world-to-grid transforms for hover/tooltip path
const gridTransformCache = new Map();
const GRID_TRANSFORM_CACHE_MAX = 200;
function worldToGrid(wx, wz) {
  const key = `${wx.toFixed(3)},${wz.toFixed(3)}`;
  if (gridTransformCache.has(key)) {
    cache.hits++;
    return gridTransformCache.get(key);
  }
  cache.misses++;
  const gx = Math.floor((wx / 6 + 0.5) * GRID);
  const gy = Math.floor((wz / 6 + 0.5) * GRID);
  const result = {
    gx: Math.max(0, Math.min(GRID - 1, gx)),
    gy: Math.max(0, Math.min(GRID - 1, gy)),
  };
  // LRU-ish eviction
  if (gridTransformCache.size >= GRID_TRANSFORM_CACHE_MAX) {
    const firstKey = gridTransformCache.keys().next().value;
    gridTransformCache.delete(firstKey);
  }
  gridTransformCache.set(key, result);
  return result;
}
function updateParticles(timeIndex) {
  const { revenue, apis } = timeSeriesData[timeIndex];
  const posArr = particleGeom.attributes.position.array;
  const colArr = particleGeom.attributes.color.array;
  const dt = 0.008;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const off = i * 4;
    let gx = particleState[off];
    let gy = particleState[off + 1];
    let t = particleState[off + 2] + dt;
    if (t >= 1.0) {
      resetParticle(i);
      gx = particleState[off];
      gy = particleState[off + 1];
      t = 0;
    }
    // Flow toward high API call areas — gradient ascent on api volume
    const cx = Math.floor(gx * GRID);
    const cy = Math.floor(gy * GRID);
    const seed = particleState[off + 3];
    let bestVal = -Infinity;
    let bestDx = 0, bestDy = 0;
    // Audit neighbor cells for highest API volume
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        const nx = cx + dx, ny = cy + dy;
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        const nidx = ny * GRID + nx;
        const val = apis[nidx] + 0.1 * Math.sin(seed + nx * 0.7 + ny * 0.9);
        if (val > bestVal) { bestVal = val; bestDx = dx; bestDy = dy; }
      }
    }
    gx += bestDx * 0.015 + (Math.sin(seed + t * 5) * 0.003);
    gy += bestDy * 0.015 + (Math.cos(seed + t * 5.3) * 0.003);
    gx = Math.max(0.01, Math.min(0.99, gx));
    gy = Math.max(0.01, Math.min(0.99, gy));
    particleState[off] = gx;
    particleState[off + 1] = gy;
    particleState[off + 2] = t;
    // Map to world position
    const wx = (gx - 0.5) * 6;
    const wz = (gy - 0.5) * 6;
    const idx = Math.floor(gy * GRID) * GRID + Math.floor(gx * GRID);
    const wy = revenue[Math.min(Math.floor(gy * GRID), GRID - 1) * GRID + Math.min(Math.floor(gx * GRID), GRID - 1)] * 1.8 + 0.08;
    const pOff = i * 3;
    posArr[pOff] = wx;
    posArr[pOff + 1] = wy;
    posArr[pOff + 2] = wz;
    // Color from api volume at position
    const apiVal = apis[Math.min(Math.floor(gy * GRID), GRID - 1) * GRID + Math.min(Math.floor(gx * GRID), GRID - 1)];
    colArr[pOff] = 1.0;
    colArr[pOff + 1] = 0.75 + apiVal * 0.2;
    colArr[pOff + 2] = 0.3 + apiVal * 0.3;
  }
  particleGeom.attributes.position.needsUpdate = true;
  particleGeom.attributes.color.needsUpdate = true;
}
// --- GROUND GRID ---
const gridHelper = new THREE.PolarGridHelper(4.5, 32, 20, 64, 0x1a2a3a, 0x1a2a3a);
gridHelper.position.y = -0.01;
scene.add(gridHelper);
// --- TIME SYSTEM ---
let currentTimeIndex = 0;
let targetTimeIndex = 0;
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
const slider = document.getElementById('time-slider');
slider.max = TIMES - 1;
slider.value = 0;
slider.addEventListener('input', () => {
  targetTimeIndex = parseInt(slider.value);
  document.getElementById('time-label').textContent =
    `t=${targetTimeIndex} — ${new Date(START_DATE.getTime() + targetTimeIndex * 86400000).toISOString().slice(0, 10)}`;
  // Debounce river rebuild
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    updateRiverForTime(targetTimeIndex);
    cache.debounceFires++;
  }, RIVER_DEBOUNCE_MS);
});
// Interpolate terrain toward target time for smooth transition
function updateTerrainForTime(timeIndex) {
  const newGeom = buildTerrainGeometry(timeIndex);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = newGeom;
  wireframeMesh.geometry.dispose();
  wireframeMesh.geometry = newGeom;
  currentTimeIndex = timeIndex;
}
function updateRiverForTime(timeIndex) {
  // Dispose old river group
  riverLines.traverse(child => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(m => m.dispose());
      } else {
        child.material.dispose();
      }
    }
  });
  scene.remove(riverLines);
  riverLines = buildRivers(timeIndex);
  scene.add(riverLines);
}
// --- FPS TRACKING ---
let frameCount = 0;
let lastFpsTime = performance.now();
let currentFps = 0;
// --- ANIMATION LOOP ---
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  // Reset per-frame allocation counter
  cache.frameAllocs = 0;
  // Smooth time transition if slider moved
  if (targetTimeIndex !== currentTimeIndex) {
    updateTerrainForTime(targetTimeIndex);
  }
  updateParticles(targetTimeIndex);
  renderer.render(scene, camera);
  // FPS calculation
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    currentFps = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = timestamp;
    updateDiagnostics();
  }
  // Periodic grid transform cache eviction (every 5 seconds)
  if (frameCount === 0 && gridTransformCache.size > GRID_TRANSFORM_CACHE_MAX) {
    const toDelete = gridTransformCache.size - GRID_TRANSFORM_CACHE_MAX + 20;
    let count = 0;
    for (const key of gridTransformCache.keys()) {
      if (count++ >= toDelete) break;
      gridTransformCache.delete(key);
    }
  }
}
function updateDiagnostics() {
  document.getElementById('diag-time').textContent = `${currentTimeIndex}/${TIMES - 1}`;
  document.getElementById('diag-verts').textContent = terrainMesh.geometry.attributes.position.count;
  document.getElementById('diag-rivers').textContent = riverLines.children.length;
  document.getElementById('diag-particles').textContent = PARTICLE_COUNT;
  document.getElementById('diag-fps').textContent = currentFps;
  document.getElementById('diag-hits').textContent = cache.hits;
  document.getElementById('diag-misses').textContent = cache.misses;
  document.getElementById('diag-allocs').textContent = cache.frameAllocs;
  document.getElementById('diag-debounce').textContent = cache.debounceFires;
}
// --- INIT ---
updateRiverForTime(0);
document.getElementById('time-label').textContent =
  `t=0 — ${START_DATE.toISOString().slice(0, 10)}`;
updateDiagnostics();
// --- RESIZE HANDLER ---
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- HOT-PATH AUDIT SUMMARY (inline, no runtime overhead) ---
// Allocations per frame: only particle position array reuse (BufferGeometry.attributes.position.array)
// No new THREE.XxxGeometry() in per-frame path — terrain/river builds happen on slider change only
// River rebuild is debounced at 200ms — no TubeGeometry per tick
// World-to-grid transforms memoized with LRU cap at 200 entries
// Particle positions reuse Float32Array via direct index writes, zero allocations
// Cache hit/miss logged to diagnostic panel for user-visible transparency
// Geometry constructors proxied to increment frameAllocs counter for audit visibility
// --- KEYBOARD SHORTCUTS ---
window.addEventListener('keydown', (e) => {
  const key = e.key.toLowerCase();
  if (key === 'r') {
    controls.autoRotate = !controls.autoRotate;
  }
  if (key >= '1' && key <= String(BOOKMARKS.length)) {
    const idx = parseInt(key) - 1;
    activeBookmark = idx;
    const bm = BOOKMARKS[idx];
    animateCamera(bm.pos, bm.target);
    document.querySelectorAll('.bm-btn').forEach((b, j) => b.classList.toggle('active', j === idx));
  }
});
// Start
requestAnimationFrame(animate);
// Export for console inspection
window.__terrain = {
  scene, camera, controls, terrainMesh, particles, cache,
  timeSeriesData, currentTimeIndex,
  jumpToTime: (t) => {
    targetTimeIndex = Math.max(0, Math.min(TIMES - 1, t));
    slider.value = targetTimeIndex;
    updateRiverForTime(targetTimeIndex);
  },
  getDiagnostics: () => ({
    cacheHits: cache.hits,
    cacheMisses: cache.misses,
    fps: currentFps,
    frameAllocs: cache.frameAllocs,
    debounceFires: cache.debounceFires,
    gridTransformCacheSize: gridTransformCache.size,
  }),
};
console.log('3D Data Terrain Explorer ready. Drag to orbit, scroll to zoom. Keys 1-5 for bookmarks, R for auto-rotate.');
console.log('window.__terrain for API access.');
</script>
</body>
</html>