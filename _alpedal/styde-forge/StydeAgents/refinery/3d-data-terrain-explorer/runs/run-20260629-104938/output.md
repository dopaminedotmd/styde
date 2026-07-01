I ser att du vill ha den körbara HTML-artefakten direkt — ingen write_file, bara svaret. Här är artifact.
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: system-ui, sans-serif; }
  canvas { display: block; }
  #panel {
    position: fixed; top: 12px; left: 12px;
    background: rgba(10,10,30,0.85); color: #c8d6e5;
    padding: 14px 18px; border-radius: 8px; border: 1px solid #2d3a5c;
    font-size: 12px; z-index: 10; min-width: 200px; backdrop-filter: blur(6px);
  }
  #panel h2 { font-size: 14px; margin: 0 0 8px 0; color: #7bed9f; }
  .row { display: flex; justify-content: space-between; margin: 3px 0; }
  .label { color: #8395a7; }
  .val { color: #dfe6e9; font-variant-numeric: tabular-nums; }
  #time-slider { width: 100%; margin: 10px 0 4px 0; accent-color: #7bed9f; }
  #time-label { text-align: center; color: #7bed9f; font-weight: 600; }
  .bookmark-btn {
    display: block; width: 100%; margin: 3px 0; padding: 4px 8px;
    background: #1e2a45; color: #a4b0be; border: 1px solid #3d4f6b;
    border-radius: 4px; cursor: pointer; font-size: 11px; text-align: left;
  }
  .bookmark-btn:hover { background: #2d3f5e; color: #dfe6e9; }
  #cache-panel {
    position: fixed; bottom: 12px; right: 12px;
    background: rgba(10,10,30,0.85); color: #8395a7;
    padding: 8px 14px; border-radius: 6px; border: 1px solid #2d3a5c;
    font-size: 10px; z-index: 10; backdrop-filter: blur(6px);
  }
</style>
</head>
<body>
<div id="panel">
  <h2>Data Terrain</h2>
  <div class="row"><span class="label">Revenue (elevation)</span><span class="val" id="val-rev">--</span></div>
  <div class="row"><span class="label">Users (green density)</span><span class="val" id="val-usr">--</span></div>
  <div class="row"><span class="label">Errors (red rivers)</span><span class="val" id="val-err">--</span></div>
  <div class="row"><span class="label">API calls (particles)</span><span class="val" id="val-api">--</span></div>
  <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
  <div id="time-label">Hour 0</div>
  <div style="margin-top:8px;color:#7bed9f;font-weight:600">Bookmarks</div>
  <button class="bookmark-btn" data-idx="0">Overview</button>
  <button class="bookmark-btn" data-idx="1">River Valley</button>
  <button class="bookmark-btn" data-idx="2">Revenue Peak</button>
  <button class="bookmark-btn" data-idx="3">Top-down</button>
  <button class="bookmark-btn save-bm">Save current view</button>
</div>
<div id="cache-panel">
  Cache hits: <span id="cache-hit">0</span> / misses: <span id="cache-miss">0</span>
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
// ── Synthetic time-series data (24 hours) ──
const GRID = 80;
const HOURS = 24;
const data = [];
for (let h = 0; h < HOURS; h++) {
  const t = h / HOURS;
  const grid = [];
  for (let z = 0; z < GRID; z++) {
    const row = [];
    for (let x = 0; x < GRID; x++) {
      const nx = (x / GRID - 0.5) * 4;
      const nz = (z / GRID - 0.5) * 4;
      // Revenue: two shifting peaks (morning + evening) with noise
      const peak1 = Math.exp(-((nx-0.8)**2 + (nz+0.4)**2) * (1.4 - 0.3*Math.sin(t*Math.PI)));
      const peak2 = Math.exp(-((nx+0.5)**2 + (nz-0.6)**2) * (1.2 + 0.4*Math.cos(t*Math.PI)));
      const noise = Math.sin(nx*3.7+t*2)*Math.cos(nz*2.9+t)*0.12;
      const revenue = (peak1*0.6 + peak2*0.35 + noise + 0.08) * (0.7 + 0.3*Math.sin(t*Math.PI));
      // Users: density shifts from peak1 toward peak2 over time
      const users = (peak1*(1-t)*0.8 + peak2*t*0.8 + Math.abs(noise)*1.5 + 0.1);
      // Errors: inverse of users + noise spike at specific locations
      const errSpike = (Math.abs(nx+0.3) < 0.25 && Math.abs(nz-0.2) < 0.25) ? 0.7*Math.sin(t*Math.PI*3) : 0;
      const errors = Math.max(0, (1-users)*0.45 + errSpike + Math.random()*0.06);
      // API calls: follow users with lag
      const apiCalls = users*0.7 + 0.05*Math.sin(t*6+nx*2);
      row.push({ revenue, users, errors, apiCalls });
    }
    grid.push(row);
  }
  data.push(grid);
}
// ── Cache stores ──
const terrainCache = new Map();     // timeIdx -> { geometry, material }
const riverPositionsCache = new Map(); // timeIdx -> Float32Array of river path positions
let cacheHits = 0, cacheMisses = 0;
function logCache(hit) { hit ? cacheHits++ : cacheMisses++; updateCacheDisplay(); }
function updateCacheDisplay() {
  document.getElementById('cache-hit').textContent = cacheHits;
  document.getElementById('cache-miss').textContent = cacheMisses;
}
// ── Scene setup ──
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.FogExp2(0x0a0a18, 0.00025);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.5, 80);
camera.position.set(8, 7, 10);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
// ── Lighting ──
const ambient = new THREE.AmbientLight(0x2d3a5c, 1.5);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(8, 12, 4);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 40;
sun.shadow.camera.left = -10; sun.shadow.camera.right = 10;
sun.shadow.camera.top = 10; sun.shadow.camera.bottom = -10;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
fill.position.set(-3, 2, -5);
scene.add(fill);
// ── Grid helper ──
const gridHelper = new THREE.GridHelper(12, 20, 0x1e2a45, 0x141c2e);
gridHelper.position.y = -0.01;
scene.add(gridHelper);
// ── Build terrain geometry (cached per time index) ──
function buildTerrainGeom(timeIdx) {
  const cached = terrainCache.get(timeIdx);
  if (cached) { logCache(true); return cached; }
  logCache(false);
  const grid = data[timeIdx];
  const segs = GRID - 1;
  const geom = new THREE.PlaneGeometry(10, 10, segs, segs);
  geom.rotateX(-Math.PI/2);
  const pos = geom.attributes.position;
  const colorsArr = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    const x = Math.round((pos.getX(i)/10 + 0.5) * (GRID-1));
    const z = Math.round((pos.getZ(i)/10 + 0.5) * (GRID-1));
    const cell = grid[Math.min(z, GRID-1)][Math.min(x, GRID-1)];
    // Revenue → Y elevation
    pos.setY(i, cell.revenue * 3.5);
    // Users → green channel, Errors → red channel
    colorsArr[i*3]   = cell.errors * 1.8;          // R: error intensity
    colorsArr[i*3+1] = cell.users * 1.1;            // G: user density
    colorsArr[i*3+2] = 0.25 + cell.revenue * 0.3;   // B: subtle revenue tint
  }
  geom.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
  geom.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide,
  });
  const result = { geometry: geom, material: mat };
  terrainCache.set(timeIdx, result);
  return result;
}
// ── River geometry (cached positions per time index) ──
function buildRiverLine(timeIdx) {
  const cached = riverPositionsCache.get(timeIdx);
  if (cached) { logCache(true); return cached; }
  logCache(false);
  const grid = data[timeIdx];
  const path = [];
  // Trace error ridge: start at high-error point, walk downhill along error gradient
  let cx = 35, cz = 38; // near error spike region
  for (let step = 0; step < 120; step++) {
    const x = Math.round(cx), z = Math.round(cz);
    if (x < 1 || x >= GRID-1 || z < 1 || z >= GRID-1) break;
    const cell = grid[z][x];
    const wx = (cx/GRID - 0.5) * 10;
    const wz = (cz/GRID - 0.5) * 10;
    const wy = cell.revenue * 3.5 + 0.04;
    path.push(wx, wy, wz);
    // Walk toward highest error neighbor
    let bestErr = -1, bestDx = 0, bestDz = 0;
    for (const [dx, dz] of [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]) {
      const nx = x+dx, nz = z+dz;
      if (nx<0||nx>=GRID||nz<0||nz>=GRID) continue;
      const e = grid[nz][nx].errors;
      if (e > bestErr) { bestErr = e; bestDx = dx; bestDz = dz; }
    }
    if (bestErr < 0.02) break;
    cx += bestDx * 0.6; cz += bestDz * 0.6;
  }
  const arr = new Float32Array(path);
  riverPositionsCache.set(timeIdx, arr);
  return arr;
}
function buildRiverTube(timeIdx) {
  const positions = buildRiverLine(timeIdx);
  const curve = new THREE.CatmullRomCurve3(
    Array.from({length: positions.length/3}, (_,i) =>
      new THREE.Vector3(positions[i*3], positions[i*3+1], positions[i*3+2])
    )
  );
  const tubeGeom = new THREE.TubeGeometry(curve, 80, 0.06, 6, false);
  const tubeMat = new THREE.MeshStandardMaterial({
    color: 0xff3b3b, emissive: 0x661111, roughness: 0.3, metalness: 0.4
  });
  return new THREE.Mesh(tubeGeom, tubeMat);
}
// ── Particles (API call trails) ──
const PARTICLE_COUNT = 600;
const particleGeom = new THREE.BufferGeometry();
// Pre-allocate position array — reused every frame, no per-frame allocation
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = []; // { baseX, baseZ, phase, speed, amplitude }
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleData.push({
    baseX: (Math.random() - 0.5) * 10,
    baseZ: (Math.random() - 0.5) * 10,
    phase: Math.random() * Math.PI * 2,
    speed: 0.6 + Math.random() * 1.8,
    amplitude: 0.15 + Math.random() * 0.5,
  });
  // Initialize colors: warm yellow-orange
  particleColors[i*3]   = 1.0;
  particleColors[i*3+1] = 0.75 + Math.random()*0.25;
  particleColors[i*3+2] = 0.2 + Math.random()*0.3;
}
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
// Create canvas texture for glow particle sprite
const spriteCanvas = document.createElement('canvas');
spriteCanvas.width = 32; spriteCanvas.height = 32;
const ctx = spriteCanvas.getContext('2d');
const gradient = ctx.createRadialGradient(16,16,0,16,16,16);
gradient.addColorStop(0,'rgba(255,220,140,1)');
gradient.addColorStop(0.3,'rgba(255,180,60,0.7)');
gradient.addColorStop(0.7,'rgba(255,100,20,0.1)');
gradient.addColorStop(1,'rgba(255,40,0,0)');
ctx.fillStyle = gradient;
ctx.fillRect(0,0,32,32);
const spriteTex = new THREE.CanvasTexture(spriteCanvas);
const particleMat = new THREE.PointsMaterial({
  size: 0.18, map: spriteTex, vertexColors: true,
  blending: THREE.AdditiveBlending, depthWrite: false, transparent: true,
});
const particles = new THREE.Points(particleGeom, particleMat);
scene.add(particles);
// ── OrbitControls ──
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 1.2, 0);
controls.maxPolarAngle = Math.PI * 0.7;
controls.minDistance = 3;
controls.maxDistance = 25;
controls.update();
// ── Bookmarks ──
const bookmarks = [
  { pos: [8,7,10], target: [0,1.2,0], label: 'Overview' },
  { pos: [2,2.5,6], target: [-1.5,1.0,2.0], label: 'River Valley' },
  { pos: [1,6,2], target: [2.5,2.0,-1.2], label: 'Revenue Peak' },
  { pos: [0,10,0.3], target: [0,1.0,0], label: 'Top-down' },
];
const userBookmarks = [];
function applyBookmark(bm) {
  camera.position.set(...bm.pos);
  controls.target.set(...bm.target);
  controls.update();
}
document.querySelectorAll('.bookmark-btn[data-idx]').forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.idx);
    applyBookmark(bookmarks[idx]);
  });
});
document.querySelector('.save-bm').addEventListener('click', () => {
  const bm = {
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
    label: `View ${userBookmarks.length+1}`,
  };
  userBookmarks.push(bm);
  const panel = document.getElementById('panel');
  const btn = document.createElement('button');
  btn.className = 'bookmark-btn';
  btn.textContent = bm.label;
  btn.addEventListener('click', () => applyBookmark(bm));
  panel.appendChild(btn);
});
// ── Scene objects (mutable) ──
let terrainMesh = null;
let riverMesh = null;
let currentTimeIdx = 0;
function setTime(idx, immediate = true) {
  currentTimeIdx = idx;
  document.getElementById('time-slider').value = idx;
  document.getElementById('time-label').textContent = `Hour ${idx}:00`;
  const grid = data[idx];
  // Update stats
  let sumRev=0,sumUsr=0,sumErr=0,sumApi=0, n = GRID*GRID;
  for (const row of grid) for (const c of row) {
    sumRev+=c.revenue; sumUsr+=c.users; sumErr+=c.errors; sumApi+=c.apiCalls;
  }
  document.getElementById('val-rev').textContent = (sumRev/n*100).toFixed(1)+'%';
  document.getElementById('val-usr').textContent = (sumUsr/n*100).toFixed(1)+'%';
  document.getElementById('val-err').textContent = (sumErr/n*100).toFixed(1)+'%';
  document.getElementById('val-api').textContent = (sumApi/n*100).toFixed(1)+'%';
  // Swap terrain (cached geometry, no new construction if cached)
  if (terrainMesh) scene.remove(terrainMesh);
  const { geometry, material } = buildTerrainGeom(idx);
  terrainMesh = new THREE.Mesh(geometry, material);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Swap river (debounced via immediate flag, cached TubeGeometry per tick)
  if (immediate) {
    if (riverMesh) scene.remove(riverMesh);
    riverMesh = buildRiverTube(idx);
    scene.add(riverMesh);
  }
}
// ── Debounced river rebuild ──
let riverDebounceTimer = null;
function debouncedSetTime(idx) {
  setTime(idx, false); // terrain swaps immediately
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (riverMesh) scene.remove(riverMesh);
    riverMesh = buildRiverTube(idx);
    scene.add(riverMesh);
  }, 200);
}
// ── Time slider ──
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  debouncedSetTime(parseInt(slider.value));
});
// ── Update particles each frame (reuse pre-allocated arrays, no allocation) ──
const clock = new THREE.Clock();
function updateParticles(timeIdx, elapsed) {
  const grid = data[timeIdx];
  const arr = particleGeom.attributes.position.array;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    // World-space position with orbiting motion
    const angle = elapsed * pd.speed + pd.phase;
    const wx = pd.baseX + Math.cos(angle) * pd.amplitude;
    const wz = pd.baseZ + Math.sin(angle) * pd.amplitude;
    // Sample terrain height at world position (memoize grid lookup)
    const gx = Math.round((wx/10 + 0.5) * (GRID-1));
    const gz = Math.round((wz/10 + 0.5) * (GRID-1));
    const cx = Math.max(0, Math.min(GRID-1, gx));
    const cz = Math.max(0, Math.min(GRID-1, gz));
    const wy = grid[cz][cx].revenue * 3.5 + 0.12;
    arr[i*3]   = wx;
    arr[i*3+1] = wy;
    arr[i*3+2] = wz;
  }
  particleGeom.attributes.position.needsUpdate = true;
}
// ── Init ──
setTime(0);
applyBookmark(bookmarks[0]);
// ── Render loop ──
function animate() {
  requestAnimationFrame(animate);
  const elapsed = clock.getElapsedTime();
  controls.update();
  updateParticles(currentTimeIdx, elapsed);
  renderer.render(scene, camera);
}
animate();
// ── Resize ──
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ── Keyboard shortcuts ──
window.addEventListener('keydown', (e) => {
  if (e.key === 'r') controls.autoRotate = !controls.autoRotate;
  if (e.key === 'ArrowLeft')  { slider.value = Math.max(0, currentTimeIdx-1); debouncedSetTime(parseInt(slider.value)); }
  if (e.key === 'ArrowRight') { slider.value = Math.min(23, currentTimeIdx+1); debouncedSetTime(parseInt(slider.value)); }
  if (e.key >= '0' && e.key <= '4') {
    const idx = parseInt(e.key);
    if (idx < bookmarks.length) applyBookmark(bookmarks[idx]);
  }
});
</script>
</body>
</html>