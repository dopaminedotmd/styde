<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
  #canvas{position:fixed;top:0;left:0;width:100%;height:100%}
  #ui{position:fixed;top:16px;left:16px;z-index:10;display:flex;flex-direction:column;gap:10px;pointer-events:none}
  #ui>*{pointer-events:auto}
  .panel{background:rgba(10,10,20,0.88);backdrop-filter:blur(8px);border:1px solid rgba(100,140,200,0.25);border-radius:10px;padding:14px 18px;min-width:220px}
  .panel h3{font-size:12px;text-transform:uppercase;letter-spacing:0.08em;color:#74a9d8;margin-bottom:10px;font-weight:600}
  .slider-group{display:flex;align-items:center;gap:10px}
  .slider-group label{font-size:11px;color:#96adc8;white-space:nowrap;min-width:50px}
  .slider-group input[type=range]{flex:1;accent-color:#4a9fd8;height:4px}
  .slider-group .val{font-size:11px;color:#7eb8e0;min-width:32px;text-align:right;font-variant-numeric:tabular-nums}
  .btn{background:rgba(70,130,200,0.18);border:1px solid rgba(100,150,210,0.35);color:#b0cfe0;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:11px;transition:all .2s}
  .btn:hover{background:rgba(90,160,230,0.3);border-color:rgba(130,180,230,0.5)}
  .btn.active{background:rgba(60,140,220,0.4);border-color:#5aa0e0;color:#e0eef8}
  .bookmark-row{display:flex;gap:6px;flex-wrap:wrap}
  .bookmark-row .btn{flex:1;text-align:center;font-size:10px;padding:4px 8px}
  #diagnostics{position:fixed;bottom:16px;right:16px;z-index:10;font-size:10px;font-family:'Cascadia Code',Consolas,monospace;background:rgba(10,10,20,0.85);border:1px solid rgba(100,140,200,0.2);border-radius:8px;padding:10px 14px;line-height:1.5;pointer-events:none;min-width:200px}
  #diagnostics .miss{color:#e07070}
  #diagnostics .hit{color:#60c080}
  .title-bar{display:flex;align-items:center;justify-content:space-between}
  .metric{font-size:11px;color:#96adc8;display:flex;justify-content:space-between;margin:3px 0}
  .metric span:last-child{color:#b8d0e8;font-variant-numeric:tabular-nums}
</style>
</head>
<body>
<div id="canvas"></div>
<div id="ui">
  <div class="panel">
    <div class="title-bar"><h3>Terrain Explorer</h3><button class="btn" id="btnAutorotate" title="Auto-rotate">⟳</button></div>
    <div class="slider-group"><label>Time</label><input type="range" id="timeSlider" min="0" max="99" value="0"><span class="val" id="timeVal">T+0</span></div>
    <div class="slider-group"><label>Height</label><input type="range" id="heightScale" min="1" max="30" value="10"><span class="val" id="heightVal">1.0x</span></div>
    <div class="slider-group"><label>Speed</label><input type="range" id="particleSpeed" min="5" max="50" value="20"><span class="val" id="speedVal">2.0</span></div>
    <div class="metric"><span>Frame</span><span id="metricFPS">0</span></div>
    <div class="metric"><span>Particles</span><span id="metricParticles">0</span></div>
  </div>
  <div class="panel">
    <h3>Bookmarks</h3>
    <div class="bookmark-row" id="bookmarkRow">
      <button class="btn" data-bookmark="0">Overview</button>
      <button class="btn" data-bookmark="1">Valley</button>
      <button class="btn" data-bookmark="2">Peak</button>
      <button class="btn" data-bookmark="3">Rivers</button>
    </div>
  </div>
</div>
<div id="diagnostics">
  <div>Cache</div>
  <div>terrain: <span id="cacheTerrainHit" class="hit">0</span>/<span id="cacheTerrainMiss" class="miss">0</span></div>
  <div>rivers: <span id="cacheRiverHit" class="hit">0</span>/<span id="cacheRiverMiss" class="miss">0</span></div>
  <div>grid: <span id="cacheGridHit" class="hit">0</span>/<span id="cacheGridMiss" class="miss">0</span></div>
  <div>particles: <span id="cachePartHit" class="hit">0</span>/<span id="cachePartMiss" class="miss">0</span></div>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─── Synthetic time-series data generator (128x128 grid, 100 time steps) ───
const GRID = 128, STEPS = 100;
// Precompute noise-like data once; each time step is a heightfield + error mask + flow density
function buildDataset() {
  const heights = new Float32Array(GRID * GRID * STEPS);
  const errors = new Float32Array(GRID * GRID * STEPS);
  const density = new Float32Array(GRID * GRID * STEPS);
  const riverPaths = new Array(STEPS); // array of {points:[x,y,z][]}
  // Seed-based pseudo-noise using sine hash
  const hash = (x, y, t) => {
    const n = Math.sin(x * 12.9898 + y * 78.233 + t * 43.117) * 43758.5453;
    return n - Math.floor(n);
  };
  const lerp = (a, b, t) => a + (b - a) * t;
  const smooth = (x, y, t) => {
    // Multi-octave pseudo-noise
    let v = 0, amp = 1, freq = 0.005, total = 0;
    for (let o = 0; o < 4; o++) {
      v += hash(x * freq, y * freq, t * 0.3 + o) * amp;
      total += amp;
      amp *= 0.5; freq *= 2.3;
    }
    return v / total;
  };
  for (let t = 0; t < STEPS; t++) {
    const toff = t * GRID * GRID;
    // Linear trend rising over time then dipping
    const trend = 1 - Math.abs((t - 40) / 60) * 0.7;
    // River path: sinusoidal sweep across grid with time offset
    const riverPts = [];
    const riverYBase = 30 + Math.sin(t * 0.12) * 20;
    for (let i = 0; i < GRID; i++) {
      const x = i / (GRID - 1) * 2 - 1;
      const ry = (riverYBase + Math.sin(i * 0.08 + t * 0.05) * 15) / (GRID - 1);
      const rz = trend * (0.15 + Math.abs(Math.sin(i * 0.06)) * 0.25);
      riverPts.push(new THREE.Vector3(x, rz, ry * 2 - 1));
    }
    riverPaths[t] = riverPts;
    for (let y = 0; y < GRID; y++) {
      for (let x = 0; x < GRID; x++) {
        const idx = toff + y * GRID + x;
        const nx = x / GRID, ny = y / GRID;
        const s = smooth(x, y, t);
        // Height: central ridge with time-varying amplitude
        const distFromCenter = Math.sqrt((nx - 0.5) ** 2 + (ny - 0.5) ** 2);
        const ridge = 1 - distFromCenter * 1.6 + s * 0.35;
        heights[idx] = Math.max(0, ridge * trend * 1.8 + 0.08);
        // Error rate: clusters near river path
        const dRiver = Math.abs(ny - riverYBase / GRID) * 1.5 + Math.sin(nx * 12) * 0.06;
        errors[idx] = Math.max(0, 1 - dRiver * 5) * (0.5 + s * 0.5);
        // Density: inverse of height (more users in valleys)
        density[idx] = Math.max(0, (1 - heights[idx]) * 0.9 + s * 0.25);
      }
    }
  }
  return { heights, errors, density, riverPaths };
}
const DATASET = buildDataset();
// ─── Cache infrastructure ───
const cache = {
  terrainGeo: new Map(),     // key: timeStep → BufferGeometry
  riverGeo: new Map(),       // key: timeStep → TubeGeometry
  gridTransform: new Map(),  // key: worldX_worldZ → {gx,gy} (cleared per frame)
  hits: { terrain: 0, river: 0, grid: 0, particles: 0 },
  miss: { terrain: 0, river: 0, grid: 0, particles: 0 }
};
// Max cache entries to prevent unbounded growth
const CACHE_MAX = 40;
function cacheSet(map, key, val) {
  if (map.size >= CACHE_MAX) { const first = map.keys().next().value; map.delete(first); }
  map.set(key, val);
}
function updateDiagPanel() {
  document.getElementById('cacheTerrainHit').textContent = cache.hits.terrain;
  document.getElementById('cacheTerrainMiss').textContent = cache.miss.terrain;
  document.getElementById('cacheRiverHit').textContent = cache.hits.river;
  document.getElementById('cacheRiverMiss').textContent = cache.miss.river;
  document.getElementById('cacheGridHit').textContent = cache.hits.grid;
  document.getElementById('cacheGridMiss').textContent = cache.miss.grid;
  document.getElementById('cachePartHit').textContent = cache.hits.particles;
  document.getElementById('cachePartMiss').textContent = cache.miss.particles;
}
// ─── Three.js setup ───
const container = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 2.5, 8);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 20);
camera.position.set(1.6, 1.8, 2.2);
camera.lookAt(0, 0.5, 0);
// ─── Lighting ───
const ambient = new THREE.AmbientLight('#304060', 1.6);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffe8d0', 3.5);
sun.position.set(3, 5, 2);
scene.add(sun);
const fill = new THREE.DirectionalLight('#4060a0', 1.2);
fill.position.set(-2, 1, -1);
scene.add(fill);
// ─── Ground grid reference plane ───
const gridHelper = new THREE.PolarGridHelper(2.2, 36, 24, 64, '#1a2a40', '#1a2a40');
gridHelper.position.y = -0.02;
scene.add(gridHelper);
// ─── OrbitControls ───
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 0.5, 0);
controls.minDistance = 0.6;
controls.maxDistance = 5;
controls.maxPolarAngle = Math.PI * 0.75;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
// ─── Bookmarks ───
const bookmarks = [
  { pos: [1.6, 1.8, 2.2], target: [0, 0.5, 0] },
  { pos: [0.3, 0.9, 1.8], target: [0, 0.3, -0.3] },
  { pos: [-0.3, 2.0, 0.4], target: [0, 0.7, 0] },
  { pos: [1.3, 0.5, 1.5], target: [0, 0.2, -0.4] },
];
function applyBookmark(i) {
  const b = bookmarks[i];
  // Animate smoothly
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...b.pos);
  const endTarget = new THREE.Vector3(...b.target);
  const startTime = performance.now();
  const duration = 800;
  function anim(now) {
    const t = Math.min((now - startTime) / duration, 1);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
  document.querySelectorAll('#bookmarkRow .btn').forEach((b, j) => b.classList.toggle('active', j === i));
}
document.getElementById('bookmarkRow').addEventListener('click', e => {
  const btn = e.target.closest('[data-bookmark]');
  if (btn) applyBookmark(parseInt(btn.dataset.bookmark));
});
applyBookmark(0);
// ─── Terrain mesh (reusable, swap geometry on time change) ───
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), terrainMat);
terrainMesh.rotation.x = -Math.PI / 2;
terrainMesh.scale.set(2, 1, 2);
scene.add(terrainMesh);
// Build terrain geometry for a time step — cached per step
function buildTerrainGeo(t) {
  // Check cache
  const cached = cache.terrainGeo.get(t);
  if (cached) { cache.hits.terrain++; return cached; }
  cache.miss.terrain++;
  const toff = t * GRID * GRID;
  const segments = GRID - 1;
  const geo = new THREE.PlaneGeometry(2, 2, segments, segments);
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  // Pre-extract arrays to avoid per-vertex attribute lookups
  const posArr = pos.array;
  for (let i = 0; i < pos.count; i++) {
    const px = posArr[i * 3], py = posArr[i * 3 + 1];
    // PlaneGeometry gives XZ plane; map to grid coordinates
    const gx = Math.round((px * 0.5 + 0.5) * (GRID - 1));
    const gy = Math.round((py * 0.5 + 0.5) * (GRID - 1));
    const idx = toff + gy * GRID + gx;
    const h = DATASET.heights[idx];
    const d = DATASET.density[idx];
    posArr[i * 3 + 2] = h; // Z becomes height after rotation
    // Vegetation gradient: low density → brown, high density → green
    const r = 0.15 + d * 0.25;
    const g = 0.25 + d * 0.6;
    const b = 0.18 + d * 0.15;
    colors[i * 3] = r;
    colors[i * 3 + 1] = g;
    colors[i * 3 + 2] = b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  geo.attributes.position.needsUpdate = true;
  cacheSet(cache.terrainGeo, t, geo);
  return geo;
}
// ─── River geometry (TubeGeometry along error path) — cached per step ───
let riverLine = null;
function buildRiverGeo(t) {
  const cached = cache.riverGeo.get(t);
  if (cached) { cache.hits.river++; return cached; }
  cache.miss.river++;
  const pathPts = DATASET.riverPaths[t];
  const curve = new THREE.CatmullRomCurve3(pathPts);
  const tubeGeo = new THREE.TubeGeometry(curve, 100, 0.015, 8, false);
  cacheSet(cache.riverGeo, t, tubeGeo);
  return tubeGeo;
}
const riverMat = new THREE.MeshStandardMaterial({
  color: '#e04030',
  roughness: 0.3,
  metalness: 0.2,
  emissive: '#300808',
  emissiveIntensity: 0.5
});
// ─── Particle system (data flows as trails) ───
const PARTICLE_COUNT = 600;
// Reusable position array — allocated once
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleAlive = new Float32Array(PARTICLE_COUNT); // progress 0-1, -1 = dead
const particlePaths = new Array(PARTICLE_COUNT); // cached path for each particle
// Precompute flow paths: pick random start points near river path
function buildParticlePath(t) {
  const toff = t * GRID * GRID;
  const path = [];
  // Start at a random edge, flow toward center following height gradient
  const side = Math.floor(Math.random() * 4);
  let gx, gy;
  if (side === 0) { gx = Math.floor(Math.random() * GRID); gy = 0; }
  else if (side === 1) { gx = GRID - 1; gy = Math.floor(Math.random() * GRID); }
  else if (side === 2) { gx = Math.floor(Math.random() * GRID); gy = GRID - 1; }
  else { gx = 0; gy = Math.floor(Math.random() * GRID); }
  const maxSteps = 60;
  for (let s = 0; s < maxSteps; s++) {
    const idx = toff + gy * GRID + gx;
    const h = DATASET.heights[idx];
    const wx = (gx / (GRID - 1) - 0.5) * 2;
    const wz = (gy / (GRID - 1) - 0.5) * 2;
    path.push({ x: wx, y: h + 0.02, z: wz });
    // Gradient descent: move toward lowest neighbor
    let bestDgx = 0, bestDgy = 0, bestH = h;
    for (const [dx, dy] of [[-2,0],[2,0],[0,-2],[0,2],[-1,-1],[1,-1],[-1,1],[1,1]]) {
      const nx = gx + dx, ny = gy + dy;
      if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
      const nh = DATASET.heights[toff + ny * GRID + nx];
      if (nh < bestH) { bestH = nh; bestDgx = dx; bestDgy = dy; }
    }
    if (bestDgx === 0 && bestDgy === 0) break; // local minimum
    gx += bestDgx; gy += bestDgy;
    gx = Math.max(0, Math.min(GRID - 1, gx));
    gy = Math.max(0, Math.min(GRID - 1, gy));
  }
  return path;
}
function initParticles(t) {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particlePaths[i] = buildParticlePath(t);
    particleAlive[i] = Math.random(); // stagger start
    const p = particlePaths[i][0];
    particlePositions[i * 3] = p.x;
    particlePositions[i * 3 + 1] = p.y;
    particlePositions[i * 3 + 2] = p.z;
    particleColors[i * 3] = 0.6 + Math.random() * 0.4;
    particleColors[i * 3 + 1] = 0.7 + Math.random() * 0.3;
    particleColors[i * 3 + 2] = 0.9 + Math.random() * 0.1;
  }
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
// Reuse a PointsMaterial with additive blending
const particleMat = new THREE.PointsMaterial({
  size: 0.025,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.7
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
// ─── Update terrain for a given time step ───
let currentStep = 0;
function setTimeStep(t) {
  currentStep = t;
  // Swap cached terrain geometry — no new PlaneGeometry construction
  const geo = buildTerrainGeo(t);
  if (terrainMesh.geometry !== geo) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geo;
  }
  // Swap cached river geometry
  if (riverLine) { riverLine.geometry.dispose(); scene.remove(riverLine); }
  const riverGeo = buildRiverGeo(t);
  riverLine = new THREE.Mesh(riverGeo, riverMat);
  riverLine.renderOrder = 1;
  riverLine.material.depthTest = true;
  riverLine.material.depthWrite = true;
  riverLine.position.y = 0.005;
  scene.add(riverLine);
  // Rebuild particle paths for new time step
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particlePaths[i] = buildParticlePath(t);
    particleAlive[i] = Math.random();
    const p = particlePaths[i][0];
    particlePositions[i * 3] = p.x;
    particlePositions[i * 3 + 1] = p.y;
    particlePositions[i * 3 + 2] = p.z;
  }
}
// ─── Debounced river rebuild (200ms) on slider ───
let riverDebounceTimer = null;
function debouncedSetTimeStep(t) {
  // Terrain swap is instant (cached geometries)
  const geo = buildTerrainGeo(t);
  if (terrainMesh.geometry !== geo) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geo;
  }
  // Debounce river rebuild
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (riverLine) { riverLine.geometry.dispose(); scene.remove(riverLine); }
    const riverGeo = buildRiverGeo(t);
    riverLine = new THREE.Mesh(riverGeo, riverMat);
    riverLine.renderOrder = 1;
    riverLine.position.y = 0.005;
    scene.add(riverLine);
    currentStep = t;
    // Rebuild particle paths
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      particlePaths[i] = buildParticlePath(t);
      particleAlive[i] = Math.random();
      const p = particlePaths[i][0];
      particlePositions[i * 3] = p.x;
      particlePositions[i * 3 + 1] = p.y;
      particlePositions[i * 3 + 2] = p.z;
    }
    riverDebounceTimer = null;
  }, 200);
}
// ─── Per-frame particle update (reuses position arrays, no per-particle allocation) ───
function updateParticles(dt) {
  const speed = parseFloat(document.getElementById('particleSpeed').value) / 10;
  const posArr = particleGeo.attributes.position.array;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const path = particlePaths[i];
    if (!path || path.length < 2) continue;
    let prog = particleAlive[i];
    prog += dt * speed * 0.15;
    if (prog >= 1) { prog = 0; particlePaths[i] = buildParticlePath(currentStep); }
    particleAlive[i] = prog;
    const idxF = prog * (path.length - 1);
    const lo = Math.floor(idxF);
    const hi = Math.min(lo + 1, path.length - 1);
    const frac = idxF - lo;
    const a = path[lo], b = path[hi];
    // Reuse position array slots — no new object allocation
    posArr[i * 3] = a.x + (b.x - a.x) * frac;
    posArr[i * 3 + 1] = a.y + (b.y - a.y) * frac + 0.01;
    posArr[i * 3 + 2] = a.z + (b.z - a.z) * frac;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ─── FPS counter ───
let frameCount = 0, fpsTime = performance.now(), currentFPS = 0;
// ─── Render loop ───
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  updateParticles(dt);
  renderer.render(scene, camera);
  // FPS counter (update every 500ms)
  frameCount++;
  const now = performance.now();
  if (now - fpsTime >= 500) {
    currentFPS = Math.round(frameCount / ((now - fpsTime) / 1000));
    frameCount = 0; fpsTime = now;
    document.getElementById('metricFPS').textContent = currentFPS;
    document.getElementById('metricParticles').textContent = PARTICLE_COUNT;
    updateDiagPanel();
  }
}
// ─── UI event bindings ───
const timeSlider = document.getElementById('timeSlider');
const timeVal = document.getElementById('timeVal');
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value);
  timeVal.textContent = 'T+' + t;
  debouncedSetTimeStep(t);
});
const heightSlider = document.getElementById('heightScale');
const heightVal = document.getElementById('heightVal');
heightSlider.addEventListener('input', () => {
  const v = parseInt(heightSlider.value) / 10;
  heightVal.textContent = v.toFixed(1) + 'x';
  terrainMesh.scale.y = v;
});
const speedSlider = document.getElementById('particleSpeed');
const speedVal = document.getElementById('speedVal');
speedSlider.addEventListener('input', () => {
  speedVal.textContent = (parseInt(speedSlider.value) / 10).toFixed(1);
});
document.getElementById('btnAutorotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
// ─── Window resize ───
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Initialize ───
initParticles(0);
setTimeStep(0);
animate();
updateDiagPanel();
console.log('3D Data Terrain Explorer ready — cache precomputed, geometries reused, particles batched.');
</script>
</body>
</html>