<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#0a0a14;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
#c{display:block}
#ui{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;background:rgba(10,10,30,0.85);padding:10px 20px;border-radius:10px;border:1px solid rgba(100,140,255,0.2);z-index:10;backdrop-filter:blur(8px)}
#ui label{font-size:12px;color:#8395a7}
#time{width:200px;accent-color:#4a9eff}
#timeVal{font-size:13px;min-width:40px;text-align:center;font-weight:600}
#diag{position:fixed;top:12px;right:12px;background:rgba(10,10,30,0.85);padding:10px 16px;border-radius:8px;border:1px solid rgba(100,200,100,0.25);font-size:11px;line-height:1.6;z-index:10;backdrop-filter:blur(8px)}
#diag span{color:#5fdd9d}
#bookmarks{position:fixed;top:12px;left:12px;display:flex;flex-direction:column;gap:6px;z-index:10}
#bookmarks button{background:rgba(10,10,30,0.8);border:1px solid rgba(100,140,255,0.3);color:#c8d6e5;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:11px;transition:all 0.2s;backdrop-filter:blur(4px)}
#bookmarks button:hover{background:rgba(74,158,255,0.25);border-color:#4a9eff}
#bookmarks button.save{background:rgba(255,180,50,0.15);border-color:rgba(255,180,50,0.4)}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="bookmarks">
  <button onclick="saveBookmark(0)">Save View 1</button><button onclick="loadBookmark(0)">View 1</button>
  <button onclick="saveBookmark(1)">Save View 2</button><button onclick="loadBookmark(1)">View 2</button>
  <button onclick="saveBookmark(2)">Save View 3</button><button onclick="loadBookmark(2)">View 3</button>
  <button onclick="saveBookmark(3)">Save View 4</button><button onclick="loadBookmark(3)">View 4</button>
</div>
<div id="diag">Cache: <span id="ch">0</span>H / <span id="cm">0</span>M | Geo allocs: <span id="ga">0</span> | FPS: <span id="fp">0</span></div>
<div id="ui">
  <label>TIME</label>
  <input type="range" id="time" min="0" max="9" value="0" step="1">
  <span id="timeVal">Day 1</span>
  <button onclick="toggleAutoRotate()" style="background:rgba(10,10,30,0.8);border:1px solid rgba(100,140,255,0.3);color:#c8d6e5;padding:4px 10px;border-radius:6px;cursor:pointer;font-size:11px">Auto-Rotate</button>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 50, STEPS = 10, RIVER_THRESH = 0.7, PARTICLE_COUNT = 600;
// --- Synthetic time-series data: [step][y][x] = {revenue, users, errors, apiCalls} ---
function generateData() {
  const data = [];
  for (let t = 0; t < STEPS; t++) {
    const grid = [];
    const cx = 25 + Math.sin(t * 0.6) * 8, cz = 25 + Math.cos(t * 0.5) * 8; // hotspot drifts over time
    for (let y = 0; y < GRID; y++) {
      const row = [];
      for (let x = 0; x < GRID; x++) {
        const dx = (x - cx) / 12, dz = (y - cz) / 12;
        const dist = Math.sqrt(dx * dx + dz * dz);
        const revenue = Math.max(0, 3.5 * Math.exp(-dist * dist) + 0.3 * Math.sin(x * 0.4 + t * 0.3) * Math.cos(y * 0.4 + t * 0.2) + 0.2);
        const users = Math.max(0, 1 - dist * 0.5 + 0.2 * Math.sin(x * 0.7 + t) * Math.cos(y * 0.7));
        const errors = dist < 0.8 ? (0.15 + 0.6 * (1 - dist / 0.8)) * (0.6 + 0.4 * Math.sin(t * 0.8)) : Math.max(0, 0.08 * Math.exp(-dist * 1.5));
        const apiCalls = revenue * (80 + 40 * Math.sin(x * 0.3 + y * 0.3 + t * 0.5));
        row.push({ revenue, users, errors, apiCalls });
      }
      grid.push(row);
    }
    data.push(grid);
  }
  return data;
}
const timeSeriesData = generateData();
// --- Geometry cache: Map<stepIndex, {terrain, rivers, particles}> ---
const geomCache = new Map();
let cacheHits = 0, cacheMisses = 0, geoAllocCount = 0;
function trackGeo() { geoAllocCount++; return geoAllocCount; }
function getOrBuildTerrainGeometry(step) {
  if (geomCache.has(step)) { cacheHits++; return geomCache.get(step).terrain; }
  cacheMisses++;
  const grid = timeSeriesData[step];
  const geo = new THREE.PlaneGeometry(20, 20, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  trackGeo();
  const pos = geo.attributes.position.array;
  const colors = new Float32Array(pos.length);
  // One-pass: set height from revenue, compute color from users
  for (let i = 0; i < pos.length; i += 3) {
    const ix = Math.round((pos[i] / 20 + 0.5) * (GRID - 1));
    const iz = Math.round((pos[i + 2] / 20 + 0.5) * (GRID - 1));
    const cell = grid[Math.min(GRID - 1, Math.max(0, iz))]?.[Math.min(GRID - 1, Math.max(0, ix))];
    const h = cell ? cell.revenue * 5 : 0.1;
    pos[i + 1] = h;
    // Vegetation gradient: low users=brown, high users=green
    const u = cell ? cell.users : 0;
    colors[i] = 0.15 + u * 0.25;       // R: brown base → slight red
    colors[i + 1] = 0.2 + u * 0.7;     // G: grows with user density
    colors[i + 2] = 0.08 + u * 0.15;   // B: minimal
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  if (!geomCache.has(step)) geomCache.set(step, {});
  geomCache.get(step).terrain = geo;
  return geo;
}
// --- River geometry: trace error hotspots, build TubeGeometry once per step ---
function getOrBuildRiverGeometry(step) {
  if (geomCache.has(step) && geomCache.get(step).rivers) { return geomCache.get(step).rivers; }
  const grid = timeSeriesData[step];
  const errorMap = [];
  // Find cells above error threshold
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      if (grid[y][x].errors > RIVER_THRESH) errorMap.push({ x, y, e: grid[y][x].errors });
    }
  }
  if (errorMap.length < 3) { const g = new THREE.Group(); if (geomCache.has(step)) geomCache.get(step).rivers = g; return g; }
  // Sort into a path by proximity (greedy nearest-neighbor chain)
  const visited = new Set();
  const path = [errorMap[0]];
  visited.add(0);
  while (path.length < Math.min(errorMap.length, 30)) {
    let best = -1, bestDist = Infinity;
    const last = path[path.length - 1];
    for (let i = 0; i < errorMap.length; i++) {
      if (visited.has(i)) continue;
      const d = (errorMap[i].x - last.x) ** 2 + (errorMap[i].y - last.y) ** 2;
      if (d < bestDist) { bestDist = d; best = i; }
    }
    if (best === -1 || bestDist > 100) break;
    visited.add(best);
    path.push(errorMap[best]);
  }
  // Convert to 3D world coordinates
  const points3 = path.map(p => {
    const wx = (p.x / (GRID - 1) - 0.5) * 20;
    const wz = (p.y / (GRID - 1) - 0.5) * 20;
    const wy = grid[p.y][p.x].revenue * 5 + 0.2; // float above terrain
    return new THREE.Vector3(wx, wy, wz);
  });
  const curve = new THREE.CatmullRomCurve3(points3);
  const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.15, 6, false);
  trackGeo();
  const mat = new THREE.MeshStandardMaterial({ color: 0xff3333, emissive: 0x440000, roughness: 0.3, metalness: 0.1 });
  const mesh = new THREE.Mesh(tubeGeo, mat);
  if (geomCache.has(step)) geomCache.get(step).rivers = mesh; else { geomCache.set(step, { rivers: mesh }); }
  return mesh;
}
// --- Particle system: precompute positions, reuse BufferGeometry array ---
function getOrBuildParticleSystem(step) {
  if (geomCache.has(step) && geomCache.get(step).particles) { return geomCache.get(step).particles; }
  const grid = timeSeriesData[step];
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const colors = new Float32Array(PARTICLE_COUNT * 3);
  // Seed particles along high-api-call paths (valleys in terrain)
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const angle = (i / PARTICLE_COUNT) * Math.PI * 8 + step * 0.4;
    const radius = 3 + (i % 5) * 1.8;
    const wx = Math.cos(angle) * radius;
    const wz = Math.sin(angle) * radius;
    const gx = Math.round((wx / 20 + 0.5) * (GRID - 1));
    const gz = Math.round((wz / 20 + 0.5) * (GRID - 1));
    const cell = grid[Math.min(GRID - 1, Math.max(0, gz))]?.[Math.min(GRID - 1, Math.max(0, gx))];
    const h = cell ? cell.revenue * 5 + 0.1 : 0.1;
    positions[i * 3] = wx;
    positions[i * 3 + 1] = h;
    positions[i * 3 + 2] = wz;
    // Brightness scales with apiCalls
    const a = cell ? Math.min(1, cell.apiCalls / 300) : 0.2;
    colors[i * 3] = 0.4 + a * 0.6;
    colors[i * 3 + 1] = 0.7 + a * 0.3;
    colors[i * 3 + 2] = 0.9;
  }
  const geo = new THREE.BufferGeometry();
  trackGeo();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.PointsMaterial({ size: 0.12, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.8 });
  const points = new THREE.Points(geo, mat);
  if (geomCache.has(step)) geomCache.get(step).particles = points; else { geomCache.set(step, { particles: points }); }
  return points;
}
// --- Scene init ---
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('c'), antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a1a');
scene.fog = new THREE.Fog('#0a0a1a', 15, 45);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(16, 12, 18);
camera.lookAt(0, 1.5, 0);
const ambient = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffeedd', 4.5);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
scene.add(sun);
// Water plane at y=0
const waterGeo = new THREE.PlaneGeometry(30, 30);
const waterMat = new THREE.MeshStandardMaterial({ color: '#0a1a2a', roughness: 0.95, transparent: true, opacity: 0.7 });
const water = new THREE.Mesh(waterGeo, waterMat);
water.rotation.x = -Math.PI / 2;
water.position.y = -0.05;
water.receiveShadow = true;
scene.add(water);
// Grid
const gridHelper = new THREE.GridHelper(24, 24, '#334466', '#1a2a3a');
gridHelper.position.y = 0.01;
scene.add(gridHelper);
// --- Controls ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 2, 0);
controls.minDistance = 5;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
// --- Bookmarks (camera state snapshots) ---
const bookmarks = new Array(4).fill(null);
window.saveBookmark = (i) => {
  bookmarks[i] = {
    pos: camera.position.clone(),
    target: controls.target.clone(),
    zoom: camera.zoom
  };
};
window.loadBookmark = (i) => {
  if (!bookmarks[i]) return;
  camera.position.copy(bookmarks[i].pos);
  controls.target.copy(bookmarks[i].target);
  camera.zoom = bookmarks[i].zoom;
  controls.update();
  camera.updateProjectionMatrix();
};
window.toggleAutoRotate = () => { controls.autoRotate = !controls.autoRotate; };
// --- Active scene objects (swapped on time change) ---
let activeTerrain = null, activeRivers = null, activeParticles = null;
let currentStep = -1;
function loadStep(step) {
  if (step === currentStep) return;
  currentStep = step;
  // Remove old
  if (activeTerrain) { activeTerrain.geometry.dispose(); scene.remove(activeTerrain); }
  if (activeRivers) { scene.remove(activeRivers); /* geometry cached, don't dispose */ }
  if (activeParticles) { scene.remove(activeParticles); }
  // Build or fetch from cache
  const tGeo = getOrBuildTerrainGeometry(step);
  const tMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6, metalness: 0.15, flatShading: false });
  activeTerrain = new THREE.Mesh(tGeo, tMat);
  activeTerrain.castShadow = true;
  activeTerrain.receiveShadow = true;
  scene.add(activeTerrain);
  const rivers = getOrBuildRiverGeometry(step);
  if (rivers) { activeRivers = rivers; scene.add(activeRivers); }
  const particles = getOrBuildParticleSystem(step);
  activeParticles = particles;
  scene.add(activeParticles);
  document.getElementById('timeVal').textContent = `Day ${step + 1}`;
  updateDiagnostics();
}
function updateDiagnostics() {
  document.getElementById('ch').textContent = cacheHits;
  document.getElementById('cm').textContent = cacheMisses;
  document.getElementById('ga').textContent = geoAllocCount;
}
// --- Time slider ---
const slider = document.getElementById('time');
slider.addEventListener('input', () => loadStep(parseInt(slider.value)));
// Debounce not needed: swap is instant from cache
// --- Animation loop (no per-frame allocations) ---
const clock = new THREE.Clock();
let frameCount = 0, fpsTime = 0;
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
  // FPS counter
  frameCount++;
  fpsTime += clock.getDelta();
  if (fpsTime >= 0.5) {
    document.getElementById('fp').textContent = Math.round(frameCount / fpsTime);
    frameCount = 0;
    fpsTime = 0;
  }
}
// --- Resize ---
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- Boot ---
loadStep(0);
animate();
updateDiagnostics();
// Pre-warm cache: build all geometries in background so slider swaps are instant
setTimeout(() => {
  for (let s = 1; s < STEPS; s++) {
    getOrBuildTerrainGeometry(s);
    getOrBuildRiverGeometry(s);
    getOrBuildParticleSystem(s);
  }
  updateDiagnostics();
}, 200);
</script>
</body>
</html>