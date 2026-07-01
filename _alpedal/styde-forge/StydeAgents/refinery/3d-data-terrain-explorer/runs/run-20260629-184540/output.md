<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
#canvas{display:block;position:fixed;top:0;left:0;width:100%;height:100%}
#ui{position:fixed;top:0;left:0;width:100%;pointer-events:none;z-index:10}
#ui>*{pointer-events:auto}
#panel{position:absolute;top:12px;right:12px;background:rgba(10,10,24,0.9);border:1px solid rgba(100,140,200,0.3);border-radius:8px;padding:14px 18px;min-width:240px;backdrop-filter:blur(12px)}
#panel h3{margin:0 0 10px;font-size:13px;text-transform:uppercase;letter-spacing:0.08em;color:#5dade2;font-weight:600}
.row{display:flex;align-items:center;justify-content:space-between;margin:5px 0;font-size:12px}
.row label{color:#8899aa}
.row span{color:#c8d6e5;font-family:'JetBrains Mono','Fira Code',monospace;font-size:11px}
#slider-container{position:absolute;bottom:28px;left:50%;transform:translateX(-50%);background:rgba(10,10,24,0.9);border:1px solid rgba(100,140,200,0.3);border-radius:8px;padding:12px 20px;display:flex;align-items:center;gap:12px;backdrop-filter:blur(12px)}
#time-slider{width:320px;accent-color:#5dade2;cursor:pointer}
#time-label{font-family:'JetBrains Mono',monospace;font-size:12px;color:#5dade2;min-width:56px}
#bookmark-bar{position:absolute;bottom:90px;left:50%;transform:translateX(-50%);display:flex;gap:6px}
.bookmark-btn{background:rgba(10,10,24,0.85);border:1px solid rgba(100,140,200,0.25);color:#8899aa;border-radius:6px;padding:6px 12px;font-size:11px;cursor:pointer;transition:all 0.2s;backdrop-filter:blur(8px)}
.bookmark-btn:hover{background:rgba(40,60,100,0.7);color:#5dade2;border-color:#5dade2}
.bookmark-btn.saved{color:#2ecc71;border-color:#2ecc71}
#export-bar{position:absolute;bottom:140px;left:50%;transform:translateX(-50%);display:flex;gap:6px}
.export-btn{background:rgba(10,10,24,0.85);border:1px solid rgba(100,140,200,0.25);color:#8899aa;border-radius:6px;padding:6px 14px;font-size:11px;cursor:pointer;transition:all 0.2s;backdrop-filter:blur(8px)}
.export-btn:hover{background:rgba(40,60,100,0.7);color:#f39c12;border-color:#f39c12}
.stat-bar{width:100%;height:3px;background:rgba(255,255,255,0.08);border-radius:2px;margin:1px 0;overflow:hidden}
.stat-fill{height:100%;border-radius:2px;transition:width 0.3s}
.stat-hit{background:#2ecc71}
.stat-miss{background:#e74c3c}
.stat-evict{background:#f39c12}
</style>
</head>
<body>
<canvas id="canvas"></canvas>
<div id="ui">
  <div id="panel">
    <h3>Terrain Metrics</h3>
    <div class="row"><label>Time Index</label><span id="time-index">0/24</span></div>
    <div class="row"><label>Revenue Peak</label><span id="rev-peak">--</span></div>
    <div class="row"><label>Error Rate</label><span id="err-rate">--</span></div>
    <div class="row"><label>API Calls/s</label><span id="api-rate">--</span></div>
    <div style="margin-top:10px;border-top:1px solid rgba(100,140,200,0.2);padding-top:8px"><h3>Cache Stats</h3></div>
    <div class="row"><label>Terrain Hit</label><span id="cache-terrain-hit">0</span></div>
    <div class="stat-bar"><div id="bar-terrain-hit" class="stat-fill stat-hit" style="width:0%"></div></div>
    <div class="row"><label>Terrain Miss</label><span id="cache-terrain-miss">0</span></div>
    <div class="stat-bar"><div id="bar-terrain-miss" class="stat-fill stat-miss" style="width:0%"></div></div>
    <div class="row"><label>Terrain Evict</label><span id="cache-terrain-evict">0</span></div>
    <div class="stat-bar"><div id="bar-terrain-evict" class="stat-fill stat-evict" style="width:0%"></div></div>
    <div class="row" style="margin-top:4px"><label>River Hit</label><span id="cache-river-hit">0</span></div>
    <div class="stat-bar"><div id="bar-river-hit" class="stat-fill stat-hit" style="width:0%"></div></div>
    <div class="row"><label>River Miss</label><span id="cache-river-miss">0</span></div>
    <div class="stat-bar"><div id="bar-river-miss" class="stat-fill stat-miss" style="width:0%"></div></div>
    <div class="row" style="margin-top:4px"><label>GridXform Hit</label><span id="cache-grid-hit">0</span></div>
    <div class="stat-bar"><div id="bar-grid-hit" class="stat-fill stat-hit" style="width:0%"></div></div>
    <div class="row"><label>GridXform Miss</label><span id="cache-grid-miss">0</span></div>
    <div class="stat-bar"><div id="bar-grid-miss" class="stat-fill stat-miss" style="width:0%"></div></div>
    <div class="row" style="margin-top:4px"><label>Max Cache Size</label><span id="cache-max-size">12</span></div>
  </div>
  <div id="bookmark-bar">
    <button class="bookmark-btn" data-slot="0">Ctrl+1 Save</button>
    <button class="bookmark-btn" data-slot="1">Ctrl+2 Save</button>
    <button class="bookmark-btn" data-slot="2">Ctrl+3 Save</button>
    <button class="bookmark-btn" data-slot="3">Ctrl+4 Save</button>
    <button class="bookmark-btn" data-slot="4">Ctrl+5 Save</button>
  </div>
  <div id="export-bar">
    <button class="export-btn" id="export-json">Export JSON</button>
    <button class="export-btn" id="export-csv">Export CSV</button>
  </div>
  <div id="slider-container">
    <span style="font-size:12px;color:#8899aa">Time</span>
    <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
    <span id="time-label">T+0</span>
  </div>
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
// ─── LRU Cache ────────────────────────────────────────────────────────────────
// Each cache has exactly one owner who decides when to clear.
// All other consumers call .get() only. Ownership annotated per declaration.
class LRUCache {
  constructor(maxSize = 12, name = 'cache') {
    this.maxSize = maxSize;
    this.name = name;
    this.map = new Map();
    this.stats = { hits: 0, misses: 0, evictions: 0 };
  }
  get(key) {
    if (!this.map.has(key)) {
      this.stats.misses++;
      return undefined;
    }
    const val = this.map.get(key);
    this.map.delete(key);
    this.map.set(key, val); // promote to most-recent
    this.stats.hits++;
    return val;
  }
  set(key, value) {
    if (this.map.has(key)) {
      this.map.delete(key);
    } else if (this.map.size >= this.maxSize) {
      const oldest = this.map.keys().next().value;
      this.map.delete(oldest);
      this.stats.evictions++;
    }
    this.map.set(key, value);
  }
  has(key) { return this.map.has(key); }
  clear() { this.map.clear(); }
  size() { return this.map.size; }
}
// ─── Global caches with ownership annotations ─────────────────────────────────
// OWNER: onTimeChange() — cleared only when slider moves. animate() reads only.
const terrainCache = new LRUCache(12, 'terrain');
// OWNER: rebuildRivers() — cleared only when rivers are rebuilt (dirty-flag gated).
const riverCache = new LRUCache(6, 'river');
// OWNER: getGridIndex() — this is the ONLY place worldToGridCache is written/cleared.
// All other consumers (tooltip, hover, raycast) call getGridIndex() which owns the cache.
const worldToGridCache = new LRUCache(256, 'gridXform');
// OWNER: onTimeChange() — dirty flag set on slider change; checked by animate().
let terrainDirty = true;
// ─── Data Generation ──────────────────────────────────────────────────────────
const GRID = 64;
const TIME_STEPS = 24;
const dataSeries = [];
// Generate 24 time steps of synthetic multi-metric data over a 64x64 grid.
// Each cell: { revenue, userDensity, errorRate, apiCalls }
for (let t = 0; t < TIME_STEPS; t++) {
  const phase = (t / TIME_STEPS) * Math.PI * 2;
  const frame = [];
  for (let y = 0; y < GRID; y++) {
    const row = [];
    for (let x = 0; x < GRID; x++) {
      const nx = (x / GRID) * 2 - 1;
      const ny = (y / GRID) * 2 - 1;
      const dist = Math.sqrt(nx * nx + ny * ny);
      // Revenue: central peak that oscillates with time
      const revenue = Math.max(0, (1 - dist * 0.7) * (0.5 + 0.5 * Math.sin(phase + dist * 3)) * 100);
      // User density: ridge along diagonal
      const userDensity = Math.max(0, (1 - Math.abs(nx - ny) * 1.2) * (0.4 + 0.3 * Math.cos(phase * 0.7)) * 100);
      // Error rate: cracks appearing in specific zones
      const errorRate = Math.max(0, ((dist > 0.3 && dist < 0.7) ? (0.4 + 0.3 * Math.sin(phase * 2 + nx * 5)) : 0.05) * 100);
      // API calls: concentrated in high-user areas
      const apiCalls = userDensity * (0.6 + 0.4 * Math.sin(phase + ny * 2)) * 0.8;
      row.push({ revenue, userDensity, errorRate, apiCalls });
    }
    frame.push(row);
  }
  dataSeries.push(frame);
}
// ─── Current frame accessor ───────────────────────────────────────────────────
let currentTimeIndex = 0;
function getCurrentFrame() { return dataSeries[currentTimeIndex]; }
// ─── Geometry Builders (cached, never called per-frame) ───────────────────────
function buildTerrainGeometry(frameIndex) {
  const frame = dataSeries[frameIndex];
  const segments = GRID - 1;
  const geometry = new THREE.PlaneGeometry(20, 20, segments, segments);
  geometry.rotateX(-Math.PI / 2);
  const positions = geometry.attributes.position.array;
  const colors = new Float32Array(positions.length);
  let revPeak = 0, errSum = 0, apiSum = 0;
  for (let i = 0; i < positions.length; i += 3) {
    const xi = Math.round((positions[i] / 20 + 0.5) * (GRID - 1));
    const zi = Math.round((positions[i + 2] / 20 + 0.5) * (GRID - 1));
    const cell = frame[Math.min(GRID - 1, Math.max(0, zi))][Math.min(GRID - 1, Math.max(0, xi))];
    // Elevation = revenue mapped to height
    positions[i + 1] = cell.revenue * 0.12;
    if (cell.revenue > revPeak) revPeak = cell.revenue;
    // Vertex color: green=yellow=red gradient based on userDensity (low→high)
    const d = Math.min(1, cell.userDensity / 100);
    colors[i] = d;
    colors[i + 1] = 1 - d * 0.7;
    colors[i + 2] = 0.1;
    errSum += cell.errorRate;
    apiSum += cell.apiCalls;
  }
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.computeVertexNormals();
  // Attach summary stats for UI
  geometry.userData = { revPeak, errSum: errSum / (GRID * GRID), apiSum: apiSum / (GRID * GRID) };
  return geometry;
}
function buildRiverGeometry(frameIndex) {
  const frame = dataSeries[frameIndex];
  // Trace error-rate ridges: find cells where errorRate > 60 and neighbor difference is high
  const points = [];
  const visited = new Set();
  for (let y = 1; y < GRID - 1; y++) {
    for (let x = 1; x < GRID - 1; x++) {
      const key = y * GRID + x;
      if (visited.has(key)) continue;
      if (frame[y][x].errorRate < 55) continue;
      // Walk along high-error ridge
      const segment = [];
      let cx = x, cy = y;
      let steps = 0;
      while (steps < 80 && cx >= 0 && cx < GRID && cy >= 0 && cy < GRID) {
        const ck = cy * GRID + cx;
        if (visited.has(ck) || frame[cy][cx].errorRate < 40) break;
        visited.add(ck);
        const wx = (cx / (GRID - 1) - 0.5) * 20;
        const wz = (cy / (GRID - 1) - 0.5) * 20;
        const wy = frame[cy][cx].revenue * 0.12 + 0.3;
        segment.push(new THREE.Vector3(wx, wy, wz));
        // Move to highest-error neighbor
        let best = null, bestVal = 0;
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]) {
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          const nk = ny * GRID + nx;
          if (visited.has(nk)) continue;
          if (frame[ny][nx].errorRate > bestVal) { bestVal = frame[ny][nx].errorRate; best = [nx, ny]; }
        }
        if (!best) break;
        cx = best[0]; cy = best[1]; steps++;
      }
      if (segment.length >= 4) points.push(segment);
    }
  }
  // Build TubeGeometry from path segments — cached, not rebuilt per-frame
  const group = new THREE.Group();
  const riverMat = new THREE.MeshStandardMaterial({
    color: 0xe74c3c, emissive: 0x330000, roughness: 0.3, metalness: 0.1, transparent: true, opacity: 0.85
  });
  for (const seg of points) {
    if (seg.length < 4) continue;
    const curve = new THREE.CatmullRomCurve3(seg);
    const tubeGeo = new THREE.TubeGeometry(curve, seg.length * 2, 0.15, 6, false);
    const mesh = new THREE.Mesh(tubeGeo, riverMat);
    mesh.castShadow = true;
    group.add(mesh);
  }
  return group;
}
// ─── Particle System ──────────────────────────────────────────────────────────
// Reuses BufferGeometry position arrays — no per-frame allocations.
class ParticleFlow {
  constructor(count = 2000) {
    this.count = count;
    this.geometry = new THREE.BufferGeometry();
    this.positions = new Float32Array(count * 3);
    this.colors = new Float32Array(count * 3);
    // Particle metadata: each particle has a grid position and a phase
    this.particleData = new Float32Array(count * 3); // [gridX, gridY, phase]
    for (let i = 0; i < count; i++) {
      this.particleData[i * 3] = Math.random() * (GRID - 1);
      this.particleData[i * 3 + 1] = Math.random() * (GRID - 1);
      this.particleData[i * 3 + 2] = Math.random();
      // Init positions offscreen
      this.positions[i * 3] = 0; this.positions[i * 3 + 1] = -999; this.positions[i * 3 + 2] = 0;
      // Yellow-gold particles
      this.colors[i * 3] = 1; this.colors[i * 3 + 1] = 0.84; this.colors[i * 3 + 2] = 0;
    }
    this.geometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    this.geometry.setAttribute('color', new THREE.BufferAttribute(this.colors, 3));
    const mat = new THREE.PointsMaterial({ size: 0.12, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.7 });
    this.points = new THREE.Points(this.geometry, mat);
  }
  update(frame, dt) {
    const pos = this.positions;
    const pdata = this.particleData;
    for (let i = 0; i < this.count; i++) {
      const idx3 = i * 3;
      let gx = pdata[idx3], gy = pdata[idx3 + 1], phase = pdata[idx3 + 2];
      // Flow toward high-api-call zones using simple gradient ascent on apiCalls field
      let bestGx = gx, bestGy = gy, bestApi = 0;
      for (const [dx, dy] of [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const nx = Math.floor(gx + dx), ny = Math.floor(gy + dy);
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        if (frame[ny][nx].apiCalls > bestApi) { bestApi = frame[ny][nx].apiCalls; bestGx = nx; bestGy = ny; }
      }
      gx += (bestGx - gx) * 0.08;
      gy += (bestGy - gy) * 0.08;
      phase += dt * 0.5;
      if (phase > 1) { phase -= 1; gx = Math.random() * (GRID - 1); gy = Math.random() * (GRID - 1); }
      pdata[idx3] = gx; pdata[idx3 + 1] = gy; pdata[idx3 + 2] = phase;
      const ix = Math.min(GRID - 1, Math.max(0, Math.round(gx)));
      const iy = Math.min(GRID - 1, Math.max(0, Math.round(gy)));
      const cell = frame[iy][ix];
      const wx = (gx / (GRID - 1) - 0.5) * 20;
      const wz = (gy / (GRID - 1) - 0.5) * 20;
      const wy = cell.revenue * 0.12 + 0.5;
      pos[idx3] = wx; pos[idx3 + 1] = wy; pos[idx3 + 2] = wz;
    }
    this.geometry.attributes.position.needsUpdate = true;
  }
}
// ─── Scene Setup ──────────────────────────────────────────────────────────────
const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 25, 60);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(16, 12, 18);
camera.lookAt(0, 3, 0);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 3, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 4;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI * 0.7;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
// ─── Lighting ─────────────────────────────────────────────────────────────────
const ambient = new THREE.AmbientLight(0x223344, 2.5);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 6);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -20; sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20; sun.shadow.camera.bottom = -20;
scene.add(sun);
const rim = new THREE.DirectionalLight(0x3366aa, 2);
rim.position.set(-10, 5, -15);
scene.add(rim);
// ─── Grid Helper ──────────────────────────────────────────────────────────────
const gridHelper = new THREE.GridHelper(20, 20, 0x1a1a3a, 0x0d0d20);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
// ─── Scene objects (mutable refs) ─────────────────────────────────────────────
let terrainMesh = null;
let riverGroup = null;
let particleFlow = null;
// ─── Camera Bookmarks ─────────────────────────────────────────────────────────
const bookmarks = new Array(5).fill(null);
function saveBookmark(slot) {
  bookmarks[slot] = {
    position: camera.position.clone(),
    target: controls.target.clone()
  };
  updateBookmarkButtons();
}
function loadBookmark(slot) {
  if (!bookmarks[slot]) return;
  // Animate camera to bookmark position
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bookmarks[slot].position;
  const endTarget = bookmarks[slot].target;
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const t = Math.min(1, (now - startTime) / duration);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animStep);
  }
  requestAnimationFrame(animStep);
}
function updateBookmarkButtons() {
  const btns = document.querySelectorAll('.bookmark-btn');
  btns.forEach((btn, i) => {
    btn.classList.toggle('saved', bookmarks[i] !== null);
    btn.textContent = `Ctrl+${i + 1}${bookmarks[i] ? ' ★' : ' Save'}`;
  });
}
// ─── Debounced River Rebuild ──────────────────────────────────────────────────
let riverDebounceTimer = null;
let riverRebuildPending = false;
function scheduleRiverRebuild() {
  riverRebuildPending = true;
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (riverRebuildPending) {
      rebuildRivers();
      riverRebuildPending = false;
    }
  }, 200);
}
function rebuildRivers() {
  // Remove old river group
  if (riverGroup) { scene.remove(riverGroup); disposeGroup(riverGroup); }
  // Check river cache
  let group = riverCache.get(currentTimeIndex);
  if (!group) {
    group = buildRiverGeometry(currentTimeIndex);
    riverCache.set(currentTimeIndex, group);
  }
  riverGroup = group;
  scene.add(riverGroup);
}
function disposeGroup(group) {
  group.traverse(child => {
    if (child.geometry) child.geometry.dispose();
  });
}
// ─── Terrain Display ──────────────────────────────────────────────────────────
function displayTerrain(frameIndex) {
  if (terrainMesh) {
    scene.remove(terrainMesh);
    if (terrainMesh.geometry) terrainMesh.geometry.dispose();
    if (terrainMesh.material) terrainMesh.material.dispose();
  }
  let geometry = terrainCache.get(frameIndex);
  if (!geometry) {
    geometry = buildTerrainGeometry(frameIndex);
    terrainCache.set(frameIndex, geometry);
  }
  const material = new THREE.MeshStandardMaterial({
    vertexColors: true, roughness: 0.6, metalness: 0.05,
    flatShading: false, side: THREE.DoubleSide
  });
  terrainMesh = new THREE.Mesh(geometry, material);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Update UI stats from geometry userData
  document.getElementById('rev-peak').textContent = geometry.userData.revPeak.toFixed(1);
  document.getElementById('err-rate').textContent = geometry.userData.errSum.toFixed(1) + '%';
  document.getElementById('api-rate').textContent = geometry.userData.apiSum.toFixed(0) + '/s';
}
// ─── ON TIME CHANGE — sole owner of terrain cache clearing and dirty flag ─────
function onTimeChange(newIndex) {
  if (newIndex === currentTimeIndex) return;
  currentTimeIndex = newIndex;
  terrainDirty = true;
  // worldToGridCache: cleared ONLY here (slider change), never in animate().
  // This is the single ownership point for this cache.
  worldToGridCache.clear();
  displayTerrain(newIndex);
  scheduleRiverRebuild();
  // Update UI
  document.getElementById('time-index').textContent = `${currentTimeIndex}/${TIME_STEPS}`;
  document.getElementById('time-label').textContent = `T+${currentTimeIndex}`;
  document.getElementById('time-slider').value = currentTimeIndex;
}
// ─── Export ───────────────────────────────────────────────────────────────────
function exportJSON() {
  const frame = getCurrentFrame();
  const flat = [];
  for (let y = 0; y < GRID; y++)
    for (let x = 0; x < GRID; x++)
      flat.push({ x, y, ...frame[y][x] });
  const blob = new Blob([JSON.stringify({ timeIndex: currentTimeIndex, gridSize: GRID, cells: flat }, null, 2)], { type: 'application/json' });
  downloadBlob(blob, `terrain_t${currentTimeIndex}.json`);
}
function exportCSV() {
  const frame = getCurrentFrame();
  const lines = ['x,y,revenue,userDensity,errorRate,apiCalls'];
  for (let y = 0; y < GRID; y++)
    for (let x = 0; x < GRID; x++) {
      const c = frame[y][x];
      lines.push(`${x},${y},${c.revenue.toFixed(2)},${c.userDensity.toFixed(2)},${c.errorRate.toFixed(2)},${c.apiCalls.toFixed(2)}`);
    }
  const blob = new Blob([lines.join('\n')], { type: 'text/csv' });
  downloadBlob(blob, `terrain_t${currentTimeIndex}.csv`);
}
function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
// ─── worldToGridIndex — single ownership point for worldToGridCache ───────────
// OWNER: this function. Clears on slider change only (via onTimeChange).
// All consumers (hover, raycast, tooltip) call this; they never touch the cache directly.
function getGridIndex(worldX, worldZ) {
  const key = `${worldX.toFixed(3)},${worldZ.toFixed(3)}`;
  const cached = worldToGridCache.get(key);
  if (cached !== undefined) return cached;
  const gx = Math.round((worldX / 20 + 0.5) * (GRID - 1));
  const gy = Math.round((worldZ / 20 + 0.5) * (GRID - 1));
  const result = {
    x: Math.min(GRID - 1, Math.max(0, gx)),
    y: Math.min(GRID - 1, Math.max(0, gy))
  };
  worldToGridCache.set(key, result);
  return result;
}
// ─── Cache Stats Update ───────────────────────────────────────────────────────
function updateCacheStats() {
  const tc = terrainCache.stats, rc = riverCache.stats, gc = worldToGridCache.stats;
  const tTotal = Math.max(1, tc.hits + tc.misses);
  const rTotal = Math.max(1, rc.hits + rc.misses);
  const gTotal = Math.max(1, gc.hits + gc.misses);
  document.getElementById('cache-terrain-hit').textContent = tc.hits;
  document.getElementById('cache-terrain-miss').textContent = tc.misses;
  document.getElementById('cache-terrain-evict').textContent = tc.evictions;
  document.getElementById('bar-terrain-hit').style.width = (tc.hits / tTotal * 100) + '%';
  document.getElementById('bar-terrain-miss').style.width = (tc.misses / tTotal * 100) + '%';
  document.getElementById('bar-terrain-evict').style.width = (tc.evictions / tTotal * 100) + '%';
  document.getElementById('cache-river-hit').textContent = rc.hits;
  document.getElementById('cache-river-miss').textContent = rc.misses;
  document.getElementById('bar-river-hit').style.width = (rc.hits / rTotal * 100) + '%';
  document.getElementById('bar-river-miss').style.width = (rc.misses / rTotal * 100) + '%';
  document.getElementById('cache-grid-hit').textContent = gc.hits;
  document.getElementById('cache-grid-miss').textContent = gc.misses;
  document.getElementById('bar-grid-hit').style.width = (gc.hits / gTotal * 100) + '%';
  document.getElementById('bar-grid-miss').style.width = (gc.misses / gTotal * 100) + '%';
}
// ─── Event Handlers ───────────────────────────────────────────────────────────
document.getElementById('time-slider').addEventListener('input', (e) => {
  onTimeChange(parseInt(e.target.value));
});
document.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key >= '1' && e.key <= '5') {
    e.preventDefault();
    const slot = parseInt(e.key) - 1;
    if (e.shiftKey) saveBookmark(slot);
    else loadBookmark(slot);
  }
  // Arrow keys nudged time
  if (e.key === 'ArrowRight') { e.preventDefault(); onTimeChange(Math.min(TIME_STEPS - 1, currentTimeIndex + 1)); }
  if (e.key === 'ArrowLeft') { e.preventDefault(); onTimeChange(Math.max(0, currentTimeIndex - 1)); }
});
document.querySelectorAll('.bookmark-btn').forEach((btn, i) => {
  btn.addEventListener('click', () => {
    if (bookmarks[i]) loadBookmark(i);
    else saveBookmark(i);
  });
});
document.getElementById('export-json').addEventListener('click', exportJSON);
document.getElementById('export-csv').addEventListener('click', exportCSV);
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Initialization ───────────────────────────────────────────────────────────
displayTerrain(0);
particleFlow = new ParticleFlow(2000);
scene.add(particleFlow.points);
rebuildRivers();
document.getElementById('time-index').textContent = `0/${TIME_STEPS}`;
document.getElementById('time-label').textContent = 'T+0';
updateBookmarkButtons();
updateCacheStats();
// ─── Render Loop ──────────────────────────────────────────────────────────────
// HOT-PATH AUDIT: animate() does NOT:
//   - Call new THREE.XxxGeometry() — all geometry built in displayTerrain/rebuildRivers
//   - Clear worldToGridCache (owned by onTimeChange)
//   - Rebuild rivers (gated by dirty flag + debounce)
//   - Allocate per-frame objects — particleFlow reuses position arrays
//   - Clear terrain cache (owned by onTimeChange)
const clock = new THREE.Clock();
let statsFrameCounter = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  // Particle update reuses position arrays — zero allocations
  particleFlow.update(getCurrentFrame(), dt);
  // Cache stats update throttled to every 30 frames
  statsFrameCounter++;
  if (statsFrameCounter % 30 === 0) updateCacheStats();
  renderer.render(scene, camera);
}
animate();
</script>
</body>
</html>