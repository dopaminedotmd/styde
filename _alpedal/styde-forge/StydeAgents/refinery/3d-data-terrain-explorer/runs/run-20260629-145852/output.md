```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0d1117;--panel:#161b22;--border:#30363d;--text:#c9d1d9;--accent:#58a6ff;--danger:#f85149;--ok:#3fb950;--warn:#d2991d}
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:system-ui,sans-serif;background:var(--bg);color:var(--text);overflow:hidden;height:100vh}
  #canvas-container{position:fixed;inset:0;z-index:0}
  #panel{position:fixed;top:12px;right:12px;z-index:10;background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:14px;width:280px;max-height:calc(100vh - 24px);overflow-y:auto;font-size:13px;display:flex;flex-direction:column;gap:10px}
  #panel h3{font-size:14px;color:var(--accent);margin:0 0 4px}
  #panel label{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:12px}
  #panel input[type=range]{flex:1;accent-color:var(--accent)}
  #panel input[type=file]{width:100%;font-size:11px;color:var(--text)}
  #panel button{background:var(--accent);color:#fff;border:none;border-radius:4px;padding:6px 10px;cursor:pointer;font-size:12px;width:100%}
  #panel button.danger{background:var(--danger)}
  #panel button:hover{filter:brightness(1.15)}
  #panel .stat-row{display:flex;justify-content:space-between;font-size:11px;color:#8b949e}
  #panel .stat-row span:last-child{color:var(--text);font-variant-numeric:tabular-nums}
  #bookmark-list{display:flex;flex-wrap:wrap;gap:4px}
  #bookmark-list button{width:auto;padding:3px 7px;font-size:10px;background:#21262d;border:1px solid var(--border)}
  #cache-panel{background:#0d1117;border:1px solid var(--border);border-radius:4px;padding:6px;font-size:10px;font-family:monospace;max-height:80px;overflow-y:auto}
  #cache-panel .hit{color:var(--ok)} #cache-panel .miss{color:var(--danger)}
  #drop-overlay{position:fixed;inset:0;z-index:99;background:rgba(88,166,255,0.15);border:3px dashed var(--accent);display:none;align-items:center;justify-content:center;font-size:20px;color:var(--accent);pointer-events:none}
  #drop-overlay.active{display:flex}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="drop-overlay">Drop CSV/JSON file here</div>
<div id="panel">
  <h3>3D Data Terrain Explorer</h3>
  <label>Time frame <span id="time-label">0/0</span></label>
  <input type="range" id="time-slider" min="0" max="0" value="0">
  <input type="file" id="file-input" accept=".csv,.json">
  <button id="btn-sample">Load Sample Data</button>
  <button id="btn-export">Export Terrain JSON</button>
  <button id="btn-bookmark">Save Bookmark</button>
  <label style="font-size:12px"><input type="checkbox" id="chk-autorot" checked> Auto-rotate</label>
  <label style="font-size:12px"><input type="checkbox" id="chk-wireframe"> Wireframe</label>
  <label style="font-size:12px"><input type="checkbox" id="chk-rivers" checked> Show rivers</label>
  <label style="font-size:12px"><input type="checkbox" id="chk-particles" checked> Show particles</label>
  <div id="bookmark-list"></div>
  <div class="stat-row"><span>Grid</span><span id="stat-grid">-</span></div>
  <div class="stat-row"><span>Vertices</span><span id="stat-verts">-</span></div>
  <div class="stat-row"><span>FPS</span><span id="stat-fps">-</span></div>
  <div class="stat-row"><span>Cache hit%</span><span id="stat-cache">-</span></div>
  <div id="cache-panel"></div>
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
// --- Cache Manager ---
class CacheManager {
  constructor() {
    this.store = new Map();
    this.hits = 0;
    this.misses = 0;
    this.log = [];
  }
  get(key) {
    if (this.store.has(key)) { this.hits++; this._addLog('hit', key); return this.store.get(key); }
    this.misses++; this._addLog('miss', key); return undefined;
  }
  set(key, value) { this.store.set(key, value); }
  has(key) { return this.store.has(key); }
  clear() { this.store.clear(); this.hits = 0; this.misses = 0; this.log = []; }
  rate() { const t = this.hits + this.misses; return t === 0 ? 100 : Math.round((this.hits / t) * 100); }
  _addLog(type, key) {
    this.log.unshift(`${type === 'hit' ? 'HIT' : 'MISS'} ${key}`);
    if (this.log.length > 50) this.log.pop();
  }
}
const cache = new CacheManager();
function updateCachePanel() {
  const el = document.getElementById('cache-panel');
  if (!el) return;
  el.innerHTML = cache.log.slice(0, 8).map(l => {
    const cls = l.startsWith('HIT') ? 'hit' : 'miss';
    return `<span class="${cls}">${l}</span>`;
  }).join('<br>');
  const rateEl = document.getElementById('stat-cache');
  if (rateEl) rateEl.textContent = cache.rate() + '%';
}
// --- Data model ---
let rawData = [];           // array of {t, revenue, users, errors, apiCalls, ...}
let gridSize = 64;          // terrain resolution
let currentFrame = 0;
let frameCount = 0;
// terrain caches: key = frame index
const terrainGeomCache = new Map();   // frame → BufferGeometry (non-disposed)
const riverGeomCache = new Map();     // frame → BufferGeometry
const heightCache = new Map();        // frame → Float32Array(gridSize*gridSize)
// --- Sample data generator (realistic patterns) ---
function generateSampleData() {
  const data = [];
  const baseDate = new Date('2024-01-01');
  for (let i = 0; i < 180; i++) {
    const d = new Date(baseDate);
    d.setDate(d.getDate() + i);
    const trend = i / 180;
    const seasonal = Math.sin(i * Math.PI * 2 / 30) * 0.3;
    const noise = (Math.random() - 0.5) * 0.15;
    const revenue = Math.round((500 + trend * 2000 + seasonal * 300 + noise * 200) * 100) / 100;
    const users = Math.round(300 + trend * 800 + seasonal * 150 + noise * 100);
    const errors = Math.max(0, Math.round(3 + seasonal * 5 + Math.abs(noise) * 15 + (i > 120 ? (i - 120) * 0.4 : 0)));
    const apiCalls = Math.round(revenue * 2.3 + (Math.random() - 0.5) * 200);
    data.push({ t: d.toISOString().slice(0, 10), revenue, users, errors, apiCalls });
  }
  return data;
}
// --- CSV parser ---
function parseCSV(text) {
  const lines = text.trim().split('\n');
  if (lines.length < 2) return null;
  const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
  const rows = [];
  for (let i = 1; i < lines.length; i++) {
    const vals = lines[i].split(',');
    if (vals.length < headers.length) continue;
    const row = {};
    headers.forEach((h, j) => {
      const v = vals[j].trim();
      row[h] = isNaN(Number(v)) ? v : Number(v);
    });
    if (!row.t && !row.timestamp && !row.date) continue;
    row.t = row.t || row.timestamp || row.date;
    rows.push(row);
  }
  return rows;
}
function parseJSON(text) {
  try {
    const parsed = JSON.parse(text);
    const arr = Array.isArray(parsed) ? parsed : (parsed.data || parsed.rows || []);
    return arr.map(r => ({ ...r, t: r.t || r.timestamp || r.date || '' }));
  } catch { return null; }
}
// --- Grid mapping: spread data points across the grid via spatial hash ---
// Each data point's "coordinate" is derived from its index and metric signature.
// Revenue → height, Users → green, Errors → red river seed, apiCalls → particle density.
function buildHeightField(frameIdx) {
  const cached = heightCache.get(frameIdx);
  if (cached) return cached;
  const row = rawData[frameIdx] || rawData[0];
  if (!row) {
    const empty = new Float32Array(gridSize * gridSize);
    heightCache.set(frameIdx, empty);
    return empty;
  }
  const heights = new Float32Array(gridSize * gridSize);
  const userArr = new Float32Array(gridSize * gridSize);
  const errArr = new Float32Array(gridSize * gridSize);
  // Seed deterministic noise from frame index so terrain has structure
  const seed = frameIdx * 127.1;
  const hash = (x, y) => {
    let h = seed + x * 374761393 + y * 668265263;
    h = (h ^ (h >> 13)) * 1274126177;
    return (h ^ (h >> 16)) / 2147483648;
  };
  const maxRevenue = Math.max(...rawData.map(d => d.revenue || 0), 1);
  const maxUsers = Math.max(...rawData.map(d => d.users || 0), 1);
  const maxErrors = Math.max(...rawData.map(d => d.errors || 0), 1);
  // Revenue peak creates a central mountain; noise adds terrain roughness
  const revNorm = (row.revenue || 0) / maxRevenue;
  const cx = gridSize / 2;
  const cz = gridSize / 2;
  const radius = gridSize * 0.35;
  for (let z = 0; z < gridSize; z++) {
    for (let x = 0; x < gridSize; x++) {
      const idx = z * gridSize + x;
      const dx = (x - cx) / radius;
      const dz = (z - cz) / radius;
      const dist = Math.sqrt(dx * dx + dz * dz);
      // Gaussian hill centered, height proportional to revenue
      const hill = revNorm * Math.exp(-dist * dist * 2.5);
      // Noise ridges
      const n = hash(x, z) * 0.25;
      // Secondary hills from seasonal pattern
      const s = Math.sin((x / gridSize) * Math.PI * 3 + frameIdx * 0.1) *
                Math.cos((z / gridSize) * Math.PI * 3 + frameIdx * 0.07) * 0.15;
      heights[idx] = Math.max(0.05, hill + n + s + 0.1);
      // User density affects green vertex color (stored separately for color mapping)
      const userNorm = (row.users || 0) / maxUsers;
      userArr[idx] = userNorm;
      // Error density affects red channel
      const errNorm = (row.errors || 0) / maxErrors;
      errArr[idx] = errNorm;
    }
  }
  const result = { heights, userArr, errArr };
  heightCache.set(frameIdx, result);
  return result;
}
// --- Terrain geometry builder ---
function buildTerrainGeometry(frameIdx) {
  const cacheKey = `terrain_${frameIdx}_${gridSize}`;
  const cached = cache.get(cacheKey);
  if (cached) return cached;
  const field = buildHeightField(frameIdx);
  const { heights, userArr, errArr } = field;
  const geom = new THREE.PlaneGeometry(20, 20, gridSize - 1, gridSize - 1);
  geom.rotateX(-Math.PI / 2);
  const pos = geom.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  let maxH = 0;
  for (let i = 0; i < pos.count; i++) {
    const h = heights[i];
    pos.setY(i, h * 8); // scale height
    if (h > maxH) maxH = h;
  }
  // Vertex colors: green channel = user density, red channel = error density, blue = height
  for (let i = 0; i < pos.count; i++) {
    const h = heights[i];
    colors[i * 3] = 0.15 + errArr[i] * 0.8;       // R: error presence
    colors[i * 3 + 1] = 0.3 + userArr[i] * 0.65;  // G: user density
    colors[i * 3 + 2] = 0.2 + h * 0.7;            // B: height/elevation
  }
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.computeVertexNormals();
  cache.set(cacheKey, geom);
  return geom;
}
// --- River geometry: trace error hotspots as paths ---
let riverGroup = new THREE.Group();
const riverLineCache = new Map(); // frameIdx → Line
function buildRiverGeometry(frameIdx) {
  const cached = riverLineCache.get(frameIdx);
  if (cached) return cached;
  const field = buildHeightField(frameIdx);
  const { heights, errArr } = field;
  const threshold = 0.5; // error threshold to consider a "river source"
  // Find high-error cells as river seed points
  const seeds = [];
  for (let z = 0; z < gridSize; z++) {
    for (let x = 0; x < gridSize; x++) {
      const idx = z * gridSize + x;
      if (errArr[idx] > threshold) {
        seeds.push({ x, z, err: errArr[idx] });
      }
    }
  }
  if (seeds.length === 0) {
    riverLineCache.set(frameIdx, null);
    return null;
  }
  // Sort by error intensity, take top seeds
  seeds.sort((a, b) => b.err - a.err);
  const topSeeds = seeds.slice(0, Math.min(8, seeds.length));
  const lines = [];
  const cellW = 20 / gridSize;
  for (const seed of topSeeds) {
    const points = [];
    let cx = seed.x;
    let cz = seed.z;
    // Flow downhill: follow gradient of height field
    for (let step = 0; step < 40; step++) {
      const idx = Math.round(cz) * gridSize + Math.round(cx);
      if (cx < 1 || cx >= gridSize - 1 || cz < 1 || cz >= gridSize - 1) break;
      const h = heights[idx];
      const wx = (cx / (gridSize - 1) - 0.5) * 20;
      const wz = (cz / (gridSize - 1) - 0.5) * 20;
      points.push(new THREE.Vector3(wx, h * 8 + 0.15, wz));
      // Gradient descent: move toward lowest neighbor
      let minH = h;
      let nx = cx, nz = cz;
      for (const [dx, dz] of [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, -1], [-1, 1], [1, 1]]) {
        const ni = (cz + dz) * gridSize + (cx + dx);
        if (ni >= 0 && ni < heights.length && heights[ni] < minH) {
          minH = heights[ni];
          nx = cx + dx;
          nz = cz + dz;
        }
      }
      if (minH >= h) break; // local minimum
      cx = nx;
      cz = nz;
    }
    if (points.length > 2) lines.push(points);
  }
  if (lines.length === 0) {
    riverLineCache.set(frameIdx, null);
    return null;
  }
  // Combine into one geometry via merging line geometries
  const group = new THREE.Group();
  const riverMat = new THREE.MeshBasicMaterial({ color: 0xff3333, transparent: true, opacity: 0.8 });
  for (const pts of lines) {
    const curve = new THREE.CatmullRomCurve3(pts);
    const tubeGeom = new THREE.TubeGeometry(curve, 32, 0.12, 6, false);
    const mesh = new THREE.Mesh(tubeGeom, riverMat);
    group.add(mesh);
  }
  riverLineCache.set(frameIdx, group);
  return group;
}
// --- Particle system: API call trails ---
let particleSystem = null;
const particleDataCache = new Map(); // frameIdx → {positions: Float32Array, velocities: Float32Array}
function buildParticleData(frameIdx) {
  const cached = particleDataCache.get(frameIdx);
  if (cached) return cached;
  const field = buildHeightField(frameIdx);
  const { heights } = field;
  const row = rawData[frameIdx] || rawData[0];
  const maxCalls = Math.max(...rawData.map(d => d.apiCalls || 0), 1);
  const callNorm = (row.apiCalls || 0) / maxCalls;
  const count = Math.floor(200 + callNorm * 800);
  const positions = new Float32Array(count * 3);
  const velocities = new Float32Array(count * 3);
  const cellW = 20 / gridSize;
  for (let i = 0; i < count; i++) {
    // Random starting position on the terrain surface
    const gx = Math.floor(Math.random() * gridSize);
    const gz = Math.floor(Math.random() * gridSize);
    const idx = gz * gridSize + gx;
    const h = heights[idx] * 8;
    const wx = (gx / (gridSize - 1) - 0.5) * 20;
    const wz = (gz / (gridSize - 1) - 0.5) * 20;
    positions[i * 3] = wx;
    positions[i * 3 + 1] = h + 0.3;
    positions[i * 3 + 2] = wz;
    // Velocity: flowing downhill
    velocities[i * 3] = (Math.random() - 0.5) * 0.3;
    velocities[i * 3 + 1] = -0.05;
    velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
  }
  const data = { positions, velocities, count };
  particleDataCache.set(frameIdx, data);
  return data;
}
function rebuildParticleSystem(frameIdx) {
  if (particleSystem) {
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
  }
  const data = buildParticleData(frameIdx);
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(data.positions, 3));
  const mat = new THREE.PointsMaterial({
    color: 0xffcc44,
    size: 0.15,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
  });
  particleSystem = new THREE.Points(geom, mat);
  return particleSystem;
}
// --- Three.js scene setup ---
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d1117);
scene.fog = new THREE.Fog(0x0d1117, 30, 80);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 200);
camera.position.set(16, 14, 18);
camera.lookAt(0, 2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 2, 0);
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.65;
controls.update();
// Lighting
const ambient = new THREE.AmbientLight(0x404060, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffffff, 2.5);
sun.position.set(20, 25, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 100;
sun.shadow.camera.left = -25;
sun.shadow.camera.right = 25;
sun.shadow.camera.top = 25;
sun.shadow.camera.bottom = -25;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4488ff, 0.8);
fill.position.set(-10, 5, -10);
scene.add(fill);
// Grid helper
const grid = new THREE.GridHelper(20, 20, 0x30363d, 0x21262d);
scene.add(grid);
// Scene objects (replaced on frame change)
let terrainMesh = null;
riverGroup = new THREE.Group();
scene.add(riverGroup);
// --- Bookmark system ---
const bookmarks = [];
function saveBookmark() {
  const bm = {
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
    name: `View ${bookmarks.length + 1}`,
  };
  bookmarks.push(bm);
  renderBookmarkList();
}
function loadBookmark(idx) {
  if (idx < 0 || idx >= bookmarks.length) return;
  const bm = bookmarks[idx];
  camera.position.set(bm.pos[0], bm.pos[1], bm.pos[2]);
  controls.target.set(bm.target[0], bm.target[1], bm.target[2]);
  controls.update();
}
function renderBookmarkList() {
  const el = document.getElementById('bookmark-list');
  if (!el) return;
  el.innerHTML = bookmarks.map((bm, i) =>
    `<button onclick="window._loadBm(${i})">${bm.name}</button>`
  ).join('');
  window._loadBm = loadBookmark;
}
// --- Frame loading (terrain + rivers + particles) ---
let dirtyRivers = true;
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
function loadFrame(idx) {
  currentFrame = idx;
  const timeLabel = document.getElementById('time-label');
  if (timeLabel) timeLabel.textContent = `${idx + 1}/${frameCount}`;
  const slider = document.getElementById('time-slider');
  if (slider) slider.value = idx;
  // Terrain swap (cached)
  const geom = buildTerrainGeometry(idx);
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.material.dispose();
    scene.remove(terrainMesh);
  }
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.7,
    metalness: 0.1,
    wireframe: document.getElementById('chk-wireframe')?.checked || false,
  });
  terrainMesh = new THREE.Mesh(geom, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Rivers (debounced)
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    rebuildRivers(idx);
    riverDebounceTimer = null;
  }, RIVER_DEBOUNCE_MS);
  // Particles
  if (document.getElementById('chk-particles')?.checked) {
    if (particleSystem) {
      scene.remove(particleSystem);
      particleSystem.geometry.dispose();
      particleSystem.material.dispose();
    }
    particleSystem = rebuildParticleSystem(idx);
    scene.add(particleSystem);
  }
  updateStats(idx);
}
function rebuildRivers(idx) {
  // Clear old rivers
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    if (child.material) child.material.dispose();
    riverGroup.remove(child);
  }
  if (!document.getElementById('chk-rivers')?.checked) return;
  const riverGeom = buildRiverGeometry(idx);
  if (riverGeom) {
    riverGroup.add(riverGeom);
  }
  dirtyRivers = false;
  updateCachePanel();
}
function updateStats(idx) {
  const elGrid = document.getElementById('stat-grid');
  const elVerts = document.getElementById('stat-verts');
  if (elGrid) elGrid.textContent = `${gridSize}x${gridSize}`;
  if (elVerts && terrainMesh) elVerts.textContent = terrainMesh.geometry.attributes.position.count.toLocaleString();
}
// --- FPS counter ---
let fpsFrames = 0;
let fpsTime = performance.now();
let currentFPS = 0;
// Dirty flag for particle animation: only update when moving
let particlesNeedUpdate = true;
function updateFPS(now) {
  fpsFrames++;
  if (now - fpsTime >= 1000) {
    currentFPS = Math.round(fpsFrames / ((now - fpsTime) / 1000));
    fpsFrames = 0;
    fpsTime = now;
    const el = document.getElementById('stat-fps');
    if (el) el.textContent = currentFPS;
  }
}
// --- Particle animation (reuses position array, no per-frame allocations) ---
function animateParticles(dt) {
  if (!particleSystem || !document.getElementById('chk-particles')?.checked) return;
  // Throttle: only update if camera moved or time changed
  if (!particlesNeedUpdate) return;
  const posAttr = particleSystem.geometry.attributes.position;
  const posArr = posAttr.array; // reuse, no allocation
  const field = buildHeightField(currentFrame);
  const { heights } = field;
  const cellW = 20 / gridSize;
  for (let i = 0; i < posArr.length; i += 3) {
    // Flow downhill with noise
    const wx = posArr[i];
    const wy = posArr[i + 1];
    const wz = posArr[i + 2];
    // Grid lookup (memoized per particle would be ideal; batch is acceptable)
    const gx = Math.round(((wx / 20) + 0.5) * (gridSize - 1));
    const gz = Math.round(((wz / 20) + 0.5) * (gridSize - 1));
    const cx = Math.max(0, Math.min(gridSize - 1, gx));
    const cz = Math.max(0, Math.min(gridSize - 1, gz));
    const idx = cz * gridSize + cx;
    const terrainH = (heights[idx] || 0.1) * 8;
    // Simple flow: move randomly but stay above terrain
    posArr[i] += (Math.random() - 0.5) * dt * 2;
    posArr[i + 2] += (Math.random() - 0.5) * dt * 2;
    posArr[i + 1] = terrainH + 0.3 + Math.sin(performance.now() * 0.005 + i) * 0.15;
    // Wrap around edges
    if (Math.abs(posArr[i]) > 10) posArr[i] *= -0.9;
    if (Math.abs(posArr[i + 2]) > 10) posArr[i + 2] *= -0.9;
    posArr[i + 1] = Math.max(0.1, posArr[i + 1]);
  }
  posAttr.needsUpdate = true;
  particlesNeedUpdate = false; // reset dirty flag
}
// --- Render loop ---
function animate(timestamp) {
  requestAnimationFrame(animate);
  const dt = Math.min(0.1, (timestamp - (animate.lastTime || timestamp)) / 1000);
  animate.lastTime = timestamp;
  controls.update();
  animateParticles(dt);
  renderer.render(scene, camera);
  updateFPS(timestamp);
  // Mark particles dirty on camera movement
  if (controls.autoRotate || controls._isDragging) {
    particlesNeedUpdate = true;
  }
}
animate.lastTime = performance.now();
// Track dragging for dirty flag
renderer.domElement.addEventListener('pointerdown', () => { controls._isDragging = true; });
renderer.domElement.addEventListener('pointerup', () => {
  controls._isDragging = false;
  particlesNeedUpdate = true;
});
// --- Resize handler ---
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- UI event bindings ---
document.getElementById('time-slider').addEventListener('input', (e) => {
  loadFrame(parseInt(e.target.value));
  particlesNeedUpdate = true;
});
document.getElementById('btn-sample').addEventListener('click', () => {
  rawData = generateSampleData();
  initFromData();
});
document.getElementById('btn-export').addEventListener('click', () => {
  const field = buildHeightField(currentFrame);
  const { heights, userArr, errArr } = field;
  const exportData = {
    frame: currentFrame,
    gridSize,
    timestamp: rawData[currentFrame]?.t || 'unknown',
    heights: Array.from(heights),
    userDensity: Array.from(userArr),
    errorDensity: Array.from(errArr),
    raw: rawData[currentFrame] || null,
  };
  const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `terrain_frame_${currentFrame}.json`;
  a.click();
  URL.revokeObjectURL(url);
});
document.getElementById('btn-bookmark').addEventListener('click', saveBookmark);
document.getElementById('chk-autorot').addEventListener('change', (e) => {
  controls.autoRotate = e.target.checked;
});
document.getElementById('chk-wireframe').addEventListener('change', (e) => {
  if (terrainMesh) terrainMesh.material.wireframe = e.target.checked;
});
document.getElementById('chk-rivers').addEventListener('change', (e) => {
  if (e.target.checked) {
    rebuildRivers(currentFrame);
  } else {
    while (riverGroup.children.length > 0) {
      const c = riverGroup.children[0];
      if (c.geometry) c.geometry.dispose();
      if (c.material) c.material.dispose();
      riverGroup.remove(c);
    }
  }
});
document.getElementById('chk-particles').addEventListener('change', (e) => {
  if (e.target.checked) {
    if (particleSystem) scene.remove(particleSystem);
    particleSystem = rebuildParticleSystem(currentFrame);
    scene.add(particleSystem);
    particlesNeedUpdate = true;
  } else if (particleSystem) {
    scene.remove(particleSystem);
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
    particleSystem = null;
  }
});
// --- File input: drag & drop + file picker ---
const fileInput = document.getElementById('file-input');
const dropOverlay = document.getElementById('drop-overlay');
function handleFile(file) {
  const reader = new FileReader();
  reader.onload = (ev) => {
    const text = ev.target.result;
    let parsed;
    if (file.name.endsWith('.json')) {
      parsed = parseJSON(text);
    } else {
      parsed = parseCSV(text);
    }
    if (parsed && parsed.length > 0) {
      rawData = parsed;
      initFromData();
    } else {
      alert('Could not parse file. Expected CSV with columns: t,revenue,users,errors,apiCalls or JSON array.');
    }
  };
  reader.readAsText(file);
}
fileInput.addEventListener('change', (e) => {
  if (e.target.files[0]) handleFile(e.target.files[0]);
});
document.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropOverlay.classList.add('active');
});
document.addEventListener('dragleave', () => {
  dropOverlay.classList.remove('active');
});
document.addEventListener('drop', (e) => {
  e.preventDefault();
  dropOverlay.classList.remove('active');
  if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
// --- Initialization ---
function initFromData() {
  frameCount = rawData.length;
  cache.clear();
  terrainGeomCache.clear();
  riverGeomCache.clear();
  heightCache.clear();
  particleDataCache.clear();
  riverLineCache.clear();
  const slider = document.getElementById('time-slider');
  slider.max = frameCount - 1;
  slider.value = 0;
  // Pre-build terrain geometries for all frames (cache priming)
  for (let i = 0; i < frameCount; i++) {
    buildHeightField(i);
    buildTerrainGeometry(i);
    buildRiverGeometry(i);
    buildParticleData(i);
  }
  updateCachePanel();
  loadFrame(0);
  if (particleSystem) scene.add(particleSystem);
  renderBookmarkList();
}
// Load sample data on start
rawData = generateSampleData();
initFromData();
console.log('3D Data Terrain Explorer ready.');
console.log('Grid:', gridSize + 'x' + gridSize, '| Frames:', frameCount);
console.log('Features: terrain heightfield, vertex colors, river paths, particle trails, orbit controls, bookmarks, export');
console.log('Cache system active — check panel for hit/miss rates.');
</script>
</body>
</html>
```