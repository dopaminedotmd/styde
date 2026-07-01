```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a0f;color:#c8ccd4;font-family:'Segoe UI',system-ui,sans-serif;overflow:hidden;height:100vh}
#container{position:fixed;inset:0;z-index:1}
#ui{position:fixed;z-index:10;pointer-events:none}
#ui>*{pointer-events:auto}
#time-panel{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px;background:rgba(16,16,28,.92);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:10px 20px}
#time-slider{-webkit-appearance:none;width:320px;height:6px;border-radius:3px;background:linear-gradient(90deg,#1a3a5c,#3a7bd5);outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#5b9cf5;border:2px solid #fff;cursor:pointer;box-shadow:0 0 12px rgba(91,156,245,.5)}
#time-label{font-size:13px;color:#8b92a0;min-width:90px;text-align:center}
#time-value{font-size:14px;font-weight:600;color:#d0d6e0;min-width:48px;text-align:center}
#diagnostics{position:fixed;top:16px;right:16px;background:rgba(16,16,28,.88);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:10px 14px;font-size:11px;line-height:1.6;color:#6b7280;min-width:160px}
#diagnostics .val{color:#a0b4cc;font-weight:600}
#diagnostics .hit{color:#34d399}
#diagnostics .miss{color:#f87171}
#toolbar{position:fixed;top:16px;left:16px;display:flex;flex-direction:column;gap:6px}
.tool-btn{background:rgba(16,16,28,.88);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:8px 14px;font-size:12px;color:#8b92a0;cursor:pointer;transition:all .15s;text-align:left;white-space:nowrap}
.tool-btn:hover{color:#c8ccd4;border-color:rgba(255,255,255,.16)}
.tool-btn.active{color:#5b9cf5;border-color:#5b9cf5;background:rgba(91,156,245,.1);box-shadow:0 0 8px rgba(91,156,245,.15)}
.tool-btn .icon{display:inline-block;width:14px;margin-right:6px;text-align:center}
#bookmarks{position:fixed;left:16px;top:200px;display:flex;flex-direction:column;gap:4px}
.bm-btn{background:rgba(16,16,28,.78);border:1px solid rgba(255,255,255,.06);border-radius:6px;padding:5px 10px;font-size:11px;color:#6b7280;cursor:pointer;transition:all .12s}
.bm-btn:hover{color:#a0b4cc;border-color:rgba(255,255,255,.14)}
#tooltip{position:fixed;pointer-events:none;background:rgba(8,8,18,.94);border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:8px 12px;font-size:12px;color:#c8ccd4;display:none;z-index:20;line-height:1.5}
#tooltip.pinned{pointer-events:auto;border-color:#5b9cf5;box-shadow:0 0 16px rgba(91,156,245,.2)}
#tooltip .pin-indicator{font-size:10px;color:#5b9cf5;margin-left:6px;display:none}
#tooltip.pinned .pin-indicator{display:inline}
#legend{position:fixed;bottom:24px;right:24px;background:rgba(16,16,28,.82);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:12px 16px;font-size:11px;color:#6b7280;line-height:1.7}
.legend-row{display:flex;align-items:center;gap:8px}
.legend-swatch{width:12px;height:12px;border-radius:3px;flex-shrink:0}
</style>
</head>
<body>
<div id="container"></div>
<div id="ui">
  <div id="toolbar">
    <button class="tool-btn" id="btn-autorot" onclick="toggleAutoRotate()"><span class="icon">↻</span> Auto-Rotate</button>
    <button class="tool-btn" id="btn-rivers" onclick="toggleRivers()"><span class="icon">〰</span> Rivers</button>
    <button class="tool-btn" id="btn-particles" onclick="toggleParticles()"><span class="icon">✦</span> Particles</button>
    <button class="tool-btn" id="btn-wireframe" onclick="toggleWireframe()"><span class="icon">▦</span> Wireframe</button>
  </div>
  <div id="bookmarks">
    <button class="bm-btn" onclick="saveBookmark(1)">⌖ Save View 1</button>
    <button class="bm-btn" onclick="loadBookmark(1)">↗ Load View 1</button>
    <button class="bm-btn" onclick="saveBookmark(2)">⌖ Save View 2</button>
    <button class="bm-btn" onclick="loadBookmark(2)">↗ Load View 2</button>
  </div>
  <div id="time-panel">
    <span id="time-label">Timestep</span>
    <input type="range" id="time-slider" min="0" max="49" value="0" step="1">
    <span id="time-value">0/49</span>
  </div>
  <div id="diagnostics">
    <div>Cache hits: <span class="val hit" id="diag-hits">0</span></div>
    <div>Cache misses: <span class="val miss" id="diag-misses">0</span></div>
    <div>Pool size: <span class="val" id="diag-pool">0</span></div>
    <div>FPS: <span class="val" id="diag-fps">0</span></div>
    <div>Vertex count: <span class="val" id="diag-verts">0</span></div>
  </div>
  <div id="tooltip"><span id="tt-content"></span><span class="pin-indicator"> 📌pinned</span></div>
  <div id="legend">
    <div class="legend-row"><span class="legend-swatch" style="background:#f59e0b"></span> Revenue (elevation)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(135deg,#064e3b,#34d399)"></span> User density (vegetation)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#ef4444"></span> Error rivers</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#60a5fa"></span> API particles</div>
  </div>
</div>
<script type="importmap">
{"imports":{
  "three":"https://unpkg.com/three@0.160.0/build/three.module.js",
  "three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"
}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// --- DATA GENERATION (lazy-evaluated per timestep) ---
const GRID = 128;
const TIMESTEPS = 50;
const _dataCache = new Map(); // lazy: compute only when first accessed
function generateTimestep(t) {
  if (_dataCache.has(t)) return _dataCache.get(t);
  const h = new Float32Array(GRID * GRID);
  const c = new Float32Array(GRID * GRID);
  const phase = t / TIMESTEPS;
  // Multi-octave noise approximation seeded by t for temporal coherence
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const nx = ix / GRID - 0.5;
      const ny = iy / GRID - 0.5;
      const d = Math.sqrt(nx * nx + ny * ny);
      const a1 = Math.sin(nx * 12.7 + phase * Math.PI * 2) * Math.cos(ny * 9.3);
      const a2 = Math.sin(nx * 5.1 - phase * 1.7) * Math.cos(ny * 7.8 + 0.4);
      const a3 = Math.sin((nx + ny) * 3.3 + phase * 3.1) * 0.5;
      const ridge = 1 - Math.abs(Math.sin(d * 8 - phase * 2.5) * 1.3);
      const height = (a1 * 0.6 + a2 * 0.5 + a3 * 0.4 + ridge * 0.7) * (1 - d * 1.2);
      h[iy * GRID + ix] = Math.max(0, height * 2.5);
      const veg = (Math.sin(nx * 8 + phase * 1.2) * Math.cos(ny * 6 - phase * 0.9) + 1) / 2;
      c[iy * GRID + ix] = veg;
    }
  }
  const entry = { height: h, vegetation: c };
  _dataCache.set(t, entry);
  return entry;
}
// --- CACHE SYSTEM with hit/miss tracking ---
const cacheStats = { hits: 0, misses: 0 };
const terrainCache = new Map(); // timestep -> BufferGeometry
const riverCache = new Map();   // timestep -> THREE.Group
const noiseGridCache = new Map(); // seed -> Float32Array
function cacheGet(map, key) {
  if (map.has(key)) { cacheStats.hits++; return map.get(key); }
  cacheStats.misses++;
  return null;
}
function cacheSet(map, key, val) { map.set(key, val); return val; }
// --- OBJECT POOL for particles ---
class ParticlePool {
  constructor(maxSize) {
    this.pool = [];
    this.active = [];
    // Pre-allocate position array BufferGeometry
    const positions = new Float32Array(maxSize * 3);
    const colors = new Float32Array(maxSize * 3);
    const sizes = new Float32Array(maxSize);
    for (let i = 0; i < maxSize; i++) {
      this.pool.push({
        index: i,
        life: 0, maxLife: 0,
        vx: 0, vy: 0, vz: 0,
        startX: 0, startY: 0, startZ: 0
      });
      sizes[i] = 0;
    }
    this.geo = new THREE.BufferGeometry();
    this.geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    this.geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    this.geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    this.posArr = positions;
    this.colArr = colors;
    this.sizeArr = sizes;
    this.maxSize = maxSize;
    this.activeCount = 0;
  }
  acquire(x, y, z) {
    if (this.activeCount >= this.maxSize) return null;
    const p = this.pool[this.activeCount];
    p.startX = x; p.startY = y; p.startZ = z;
    p.vx = (Math.random() - 0.5) * 0.3;
    p.vy = Math.random() * 0.8 + 0.3;
    p.vz = (Math.random() - 0.5) * 0.3;
    p.life = 0;
    p.maxLife = 2 + Math.random() * 4;
    const i = this.activeCount;
    const i3 = i * 3;
    this.posArr[i3] = x; this.posArr[i3 + 1] = y; this.posArr[i3 + 2] = z;
    this.colArr[i3] = 0.38; this.colArr[i3 + 1] = 0.65; this.colArr[i3 + 2] = 0.98;
    this.sizeArr[i] = 0.06 + Math.random() * 0.08;
    this.activeCount++;
    this.geo.attributes.position.needsUpdate = true;
    this.geo.attributes.color.needsUpdate = true;
    this.geo.attributes.size.needsUpdate = true;
    return p;
  }
  // Compact active list: swap-dead to end, shrink count
  _compact(now) {
    let write = 0;
    for (let read = 0; read < this.activeCount; read++) {
      const p = this.pool[read];
      p.life += 0.016;
      if (p.life >= p.maxLife) continue; // dead, skip
      const frac = p.life / p.maxLife;
      const i3w = write * 3, i3r = read * 3;
      // Update position during compact pass
      const x = p.startX + p.vx * p.life * 2;
      const z = p.startZ + p.vz * p.life * 2;
      const y = p.startY + p.vy * p.life * (1 - frac);
      this.posArr[i3w] = x; this.posArr[i3w + 1] = y; this.posArr[i3w + 2] = z;
      this.colArr[i3w] = this.colArr[i3r];
      this.colArr[i3w + 1] = this.colArr[i3r + 1];
      this.colArr[i3w + 2] = this.colArr[i3r + 2];
      // Fade alpha via size
      this.sizeArr[write] = this.sizeArr[read] * (1 - frac);
      // Swap pool entries
      if (write !== read) this.pool[write] = p;
      write++;
    }
    const released = this.activeCount - write;
    this.activeCount = write;
    // Zero out dead entries' sizes so they don't render
    for (let i = write; i < write + released && i < this.maxSize; i++) {
      this.sizeArr[i] = 0;
    }
    this.geo.attributes.position.needsUpdate = true;
    this.geo.attributes.color.needsUpdate = true;
    this.geo.attributes.size.needsUpdate = true;
    this.geo.setDrawRange(0, write);
    return released;
  }
  update(now) { return this._compact(now); }
}
// --- WORLD-TO-GRID memoization (per-frame cache) ---
const w2gCache = new Map();
let w2gFrameId = 0;
function worldToGrid(wx, wz, frameId) {
  if (frameId !== w2gFrameId) { w2gCache.clear(); w2gFrameId = frameId; }
  const key = `${wx.toFixed(4)},${wz.toFixed(4)}`;
  if (w2gCache.has(key)) return w2gCache.get(key);
  const gx = Math.floor((wx + 4) / 8 * GRID);
  const gy = Math.floor((wz + 4) / 8 * GRID);
  const r = { gx: Math.max(0, Math.min(GRID - 1, gx)), gy: Math.max(0, Math.min(GRID - 1, gy)) };
  w2gCache.set(key, r);
  return r;
}
// --- THREE.JS SETUP ---
const container = document.getElementById('container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 6, 30);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.3, 60);
camera.position.set(6, 5.5, 8);
camera.lookAt(0, 1.5, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 1.5, 0);
controls.minDistance = 2.5;
controls.maxDistance = 18;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
// --- LIGHTING ---
const ambient = new THREE.AmbientLight(0x1a1a3a, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
sun.position.set(8, 14, 4);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 40;
sun.shadow.camera.left = -10;
sun.shadow.camera.right = 10;
sun.shadow.camera.top = 10;
sun.shadow.camera.bottom = -10;
scene.add(sun);
const rim = new THREE.DirectionalLight(0x335577, 1.2);
rim.position.set(-4, 2, -6);
scene.add(rim);
// --- GROUND PLANE ---
const groundGeo = new THREE.PlaneGeometry(16, 16);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x111122, roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.1;
ground.receiveShadow = true;
scene.add(ground);
// --- BUILD TERRAIN GEOMETRY (cached) ---
function buildTerrainGeometry(timestep) {
  const cached = cacheGet(terrainCache, timestep);
  if (cached) return cached;
  const data = generateTimestep(timestep);
  const h = data.height;
  const v = data.vegetation;
  const geo = new THREE.PlaneGeometry(8, 8, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position.array;
  const vertCount = pos.length / 3;
  const colors = new Float32Array(vertCount * 3);
  for (let i = 0; i < vertCount; i++) {
    const i3 = i * 3;
    const gx = Math.round((pos[i3] / 8 + 0.5) * (GRID - 1));
    const gy = Math.round((pos[i3 + 2] / 8 + 0.5) * (GRID - 1));
    const gi = Math.max(0, Math.min(GRID * GRID - 1, gy * GRID + gx));
    const elev = h[gi];
    pos[i3 + 1] = elev;
    const veg = v[gi];
    // Low vegetation = brown, high = vibrant green
    const r = 0.08 + veg * 0.12;
    const g = 0.18 + veg * 0.55;
    const b = 0.06 + veg * 0.12;
    colors[i3] = r; colors[i3 + 1] = g; colors[i3 + 2] = b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  return cacheSet(terrainCache, timestep, geo);
}
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.55, metalness: 0.05, flatShading: false
});
let terrainMesh = new THREE.Mesh(buildTerrainGeometry(0), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// --- RIVER SYSTEM (cached TubeGeometry, debounced rebuild) ---
let riverGroup = new THREE.Group();
scene.add(riverGroup);
let riverVisible = true;
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
function buildRiverGeometry(timestep) {
  const cached = cacheGet(riverCache, timestep);
  if (cached) return cached;
  // Clear old
  while (riverGroup.children.length) riverGroup.remove(riverGroup.children[0]);
  const data = generateTimestep(timestep);
  const h = data.height;
  // Trace error paths: find local minima chains with low vegetation as anomaly proxy
  const paths = [];
  const visited = new Uint8Array(GRID * GRID);
  // Seed from low-vegetation grid cells (anomaly proxy)
  for (let iy = 1; iy < GRID - 1; iy++) {
    for (let ix = 1; ix < GRID - 1; ix++) {
      const idx = iy * GRID + ix;
      if (visited[idx]) continue;
      if (data.vegetation[idx] > 0.25) continue; // not anomalous enough
      // Trace downhill from seed
      const path = [];
      let cx = ix, cy = iy;
      let steps = 0;
      while (steps < 200) {
        const ci = cy * GRID + cx;
        if (visited[ci]) break;
        visited[ci] = 1;
        path.push({ x: (cx / GRID - 0.5) * 8, z: (cy / GRID - 0.5) * 8, elev: h[ci] + 0.08 });
        // Find lowest neighbor
        let bestD = -1, bestN = null;
        for (let dy = -1; dy <= 1; dy++) {
          for (let dx = -1; dx <= 1; dx++) {
            if (dx === 0 && dy === 0) continue;
            const nx = cx + dx, ny = cy + dy;
            if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
            const ni = ny * GRID + nx;
            if (visited[ni]) continue;
            const d = h[ni];
            if (d < bestD || bestD < 0) { bestD = d; bestN = { x: nx, y: ny }; }
          }
        }
        if (!bestN || bestD >= h[ci]) break; // local minimum reached
        cx = bestN.x; cy = bestN.y;
        steps++;
      }
      if (path.length > 8) paths.push(path);
    }
  }
  // Create TubeGeometry for each path
  const mat = new THREE.MeshStandardMaterial({
    color: 0xef4444, roughness: 0.3, metalness: 0.4, emissive: 0x330000, emissiveIntensity: 0.6
  });
  const group = new THREE.Group();
  paths.forEach(path => {
    if (path.length < 2) return;
    const curve = new THREE.CatmullRomCurve3(
      path.map(p => new THREE.Vector3(p.x, p.elev, p.z)),
      false, 'catmullrom', 0.5
    );
    const tubeGeo = new THREE.TubeGeometry(curve, Math.min(path.length * 2, 80), 0.03, 6, false);
    const tube = new THREE.Mesh(tubeGeo, mat);
    tube.castShadow = true;
    group.add(tube);
  });
  return cacheSet(riverCache, timestep, group);
}
function updateRivers(timestep, immediate) {
  if (!riverVisible) return;
  if (immediate) {
    if (riverDebounceTimer) { clearTimeout(riverDebounceTimer); riverDebounceTimer = null; }
    const cached = buildRiverGeometry(timestep);
    riverGroup.clear();
    cached.children.forEach(c => riverGroup.add(c.clone()));
    return;
  }
  // Debounced path
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    riverDebounceTimer = null;
    const cached = buildRiverGeometry(timestep);
    riverGroup.clear();
    cached.children.forEach(c => riverGroup.add(c.clone()));
  }, RIVER_DEBOUNCE_MS);
}
// --- PARTICLE SYSTEM (object pool) ---
let particlePool = new ParticlePool(800);
let particleSystem;
let particlesVisible = true;
function initParticleSystem() {
  const mat = new THREE.PointsMaterial({
    size: 0.09, vertexColors: true, blending: THREE.AdditiveBlending,
    depthWrite: false, transparent: true, opacity: 0.7
  });
  particleSystem = new THREE.Points(particlePool.geo, mat);
  particleSystem.renderOrder = 1;
  scene.add(particleSystem);
}
initParticleSystem();
// --- TIME SLIDER ---
let currentTimestep = 0;
const slider = document.getElementById('time-slider');
const timeValue = document.getElementById('time-value');
function setTimestep(t, immediateRivers) {
  currentTimestep = t;
  slider.value = t;
  timeValue.textContent = `${t}/${TIMESTEPS - 1}`;
  // Swap terrain geometry (instant, cached)
  const newGeo = buildTerrainGeometry(t);
  if (terrainMesh.geometry !== newGeo) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = newGeo;
  }
  // Debounced river update
  updateRivers(t, immediateRivers);
  // Update diagnostic vertex count
  document.getElementById('diag-verts').textContent = newGeo.attributes.position.count;
}
slider.addEventListener('input', () => {
  setTimestep(parseInt(slider.value), false);
});
slider.addEventListener('change', () => {
  // On release, force immediate river update
  setTimestep(parseInt(slider.value), true);
});
// Initial build
setTimestep(0, true);
// --- PARTICLE SPAWNING ---
function spawnParticles(dt) {
  if (!particlesVisible) return;
  const data = generateTimestep(currentTimestep);
  const spawnCount = Math.floor(4 + Math.random() * 6);
  for (let s = 0; s < spawnCount; s++) {
    const sx = (Math.random() - 0.5) * 7;
    const sz = (Math.random() - 0.5) * 7;
    const g = worldToGrid(sx, sz, frameCounter);
    const elev = data.height[g.gy * GRID + g.gx] + 0.15;
    particlePool.acquire(sx, elev, sz);
  }
}
// --- TOGGLE FUNCTIONS ---
function toggleAutoRotate() {
  controls.autoRotate = !controls.autoRotate;
  document.getElementById('btn-autorot').classList.toggle('active', controls.autoRotate);
}
function toggleRivers() {
  riverVisible = !riverVisible;
  riverGroup.visible = riverVisible;
  document.getElementById('btn-rivers').classList.toggle('active', riverVisible);
  if (riverVisible) updateRivers(currentTimestep, true);
}
function toggleParticles() {
  particlesVisible = !particlesVisible;
  if (particleSystem) particleSystem.visible = particlesVisible;
  document.getElementById('btn-particles').classList.toggle('active', particlesVisible);
}
function toggleWireframe() {
  terrainMat.wireframe = !terrainMat.wireframe;
  document.getElementById('btn-wireframe').classList.toggle('active', terrainMat.wireframe);
}
// Init toggle states
document.getElementById('btn-autorot').classList.add('active');
document.getElementById('btn-rivers').classList.add('active');
document.getElementById('btn-particles').classList.add('active');
// --- CAMERA BOOKMARKS ---
const bookmarks = { 1: null, 2: null };
function saveBookmark(slot) {
  bookmarks[slot] = {
    pos: camera.position.clone(),
    target: controls.target.clone()
  };
  try { localStorage.setItem(`bm_${slot}`, JSON.stringify({
    px: bookmarks[slot].pos.x, py: bookmarks[slot].pos.y, pz: bookmarks[slot].pos.z,
    tx: bookmarks[slot].target.x, ty: bookmarks[slot].target.y, tz: bookmarks[slot].target.z
  })); } catch(e) {}
}
function loadBookmark(slot) {
  // Try localStorage first
  if (!bookmarks[slot]) {
    try {
      const raw = localStorage.getItem(`bm_${slot}`);
      if (raw) {
        const d = JSON.parse(raw);
        camera.position.set(d.px, d.py, d.pz);
        controls.target.set(d.tx, d.ty, d.tz);
        controls.update();
        return;
      }
    } catch(e) {}
    return;
  }
  camera.position.copy(bookmarks[slot].pos);
  controls.target.copy(bookmarks[slot].target);
  controls.update();
}
// Restore bookmarks from localStorage on init
[1, 2].forEach(slot => {
  try {
    const raw = localStorage.getItem(`bm_${slot}`);
    if (raw) {
      const d = JSON.parse(raw);
      bookmarks[slot] = { pos: new THREE.Vector3(d.px, d.py, d.pz), target: new THREE.Vector3(d.tx, d.ty, d.tz) };
    }
  } catch(e) {}
});
// --- CLICK-TO-PIN TOOLTIP ---
const tooltipEl = document.getElementById('tooltip');
const ttContent = document.getElementById('tt-content');
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let pinnedTooltip = null; // { screenX, screenY, worldX, worldY, elev, veg, timestep }
function updateTooltip(event) {
  if (pinnedTooltip) return; // pinned, don't move
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObject(terrainMesh, false);
  if (hits.length > 0) {
    const p = hits[0].point;
    const g = worldToGrid(p.x, p.z, frameCounter);
    const data = generateTimestep(currentTimestep);
    const idx = g.gy * GRID + g.gx;
    const elev = data.height[idx];
    const veg = data.vegetation[idx];
    tooltipEl.style.display = 'block';
    tooltipEl.style.left = (event.clientX + 18) + 'px';
    tooltipEl.style.top = (event.clientY - 10) + 'px';
    ttContent.textContent = `Elev: ${elev.toFixed(3)} | Veg: ${veg.toFixed(3)} | Grid: (${g.gx},${g.gy})`;
  } else {
    if (!pinnedTooltip) tooltipEl.style.display = 'none';
  }
}
function pinTooltip(event) {
  if (pinnedTooltip) {
    // Unpin
    pinnedTooltip = null;
    tooltipEl.classList.remove('pinned');
    tooltipEl.style.display = 'none';
    return;
  }
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObject(terrainMesh, false);
  if (hits.length > 0) {
    const p = hits[0].point;
    const g = worldToGrid(p.x, p.z, frameCounter);
    const data = generateTimestep(currentTimestep);
    const idx = g.gy * GRID + g.gx;
    pinnedTooltip = {
      screenX: event.clientX, screenY: event.clientY,
      worldX: p.x, worldZ: p.z,
      elev: data.height[idx], veg: data.vegetation[idx],
      gx: g.gx, gy: g.gy, timestep: currentTimestep
    };
    tooltipEl.classList.add('pinned');
    tooltipEl.style.display = 'block';
    tooltipEl.style.left = (event.clientX + 18) + 'px';
    tooltipEl.style.top = (event.clientY - 10) + 'px';
    ttContent.textContent = `Elev: ${pinnedTooltip.elev.toFixed(3)} | Veg: ${pinnedTooltip.veg.toFixed(3)} | Grid: (${g.gx},${g.gy})`;
  }
}
window.addEventListener('mousemove', updateTooltip, { passive: true });
window.addEventListener('click', (e) => {
  // Only pin if clicking on terrain (not UI)
  if (e.target === renderer.domElement) pinTooltip(e);
});
// --- ANIMATION LOOP ---
let frameCounter = 0;
let spawnAccum = 0;
const fpsHistory = [];
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  frameCounter++;
  controls.update();
  // Spawn particles
  spawnAccum += dt;
  while (spawnAccum > 0.12) {
    spawnAccum -= 0.12;
    spawnParticles(dt);
  }
  particlePool.update(dt);
  // Update pinned tooltip if timestep changed
  if (pinnedTooltip && pinnedTooltip.timestep !== currentTimestep) {
    const data = generateTimestep(currentTimestep);
    const idx = pinnedTooltip.gy * GRID + pinnedTooltip.gx;
    pinnedTooltip.elev = data.height[idx];
    pinnedTooltip.veg = data.vegetation[idx];
    pinnedTooltip.timestep = currentTimestep;
    ttContent.textContent = `Elev: ${pinnedTooltip.elev.toFixed(3)} | Veg: ${pinnedTooltip.veg.toFixed(3)} | Grid: (${pinnedTooltip.gx},${pinnedTooltip.gy})`;
  }
  renderer.render(scene, camera);
  // FPS tracking
  fpsHistory.push(1 / Math.max(dt, 0.001));
  if (fpsHistory.length > 30) fpsHistory.shift();
  if (frameCounter % 10 === 0) {
    const avgFps = fpsHistory.reduce((a, b) => a + b, 0) / fpsHistory.length;
    document.getElementById('diag-fps').textContent = Math.round(avgFps);
    document.getElementById('diag-hits').textContent = cacheStats.hits;
    document.getElementById('diag-misses').textContent = cacheStats.misses;
    document.getElementById('diag-pool').textContent = particlePool.activeCount;
  }
}
// --- RESIZE ---
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- KEYBOARD SHORTCUTS ---
window.addEventListener('keydown', (e) => {
  switch(e.key.toLowerCase()) {
    case 'r': toggleRivers(); break;
    case 'p': toggleParticles(); break;
    case 'w': toggleWireframe(); break;
    case 'a': toggleAutoRotate(); break;
    case '1': loadBookmark(1); break;
    case '2': loadBookmark(2); break;
    case 'arrowleft': setTimestep(Math.max(0, currentTimestep - 1), true); break;
    case 'arrowright': setTimestep(Math.min(TIMESTEPS - 1, currentTimestep + 1), true); break;
  }
});
// Start
animate();
console.log('3D Data Terrain Explorer ready — ' + TIMESTEPS + ' timesteps, ' + GRID + 'x' + GRID + ' grid');
</script>
</body>
</html>
```