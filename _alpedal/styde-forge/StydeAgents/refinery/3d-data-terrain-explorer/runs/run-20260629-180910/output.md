<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a14;--panel-bg:#12122a;--text:#c8d6e5;--accent:#4dabf7;--warn:#ff6b6b;--ok:#51cf66;--border:#2a2a4a;--input-bg:#1a1a30}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;overflow:hidden;height:100vh;width:100vw}
  #canvas-container{position:fixed;inset:0;z-index:1}
  canvas{display:block}
  #dashboard{position:fixed;bottom:0;left:50%;transform:translateX(-50%);z-index:10;width:94%;max-width:1100px;padding:12px 16px;display:flex;flex-direction:column;gap:8px}
  #timeline{display:flex;align-items:center;gap:12px;background:var(--panel-bg);border:1px solid var(--border);border-radius:8px;padding:8px 14px}
  #time-slider{flex:1;-webkit-appearance:none;height:6px;background:linear-gradient(90deg,var(--accent),var(--warn));border-radius:3px;outline:none;cursor:pointer}
  #time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#fff;border:2px solid var(--accent);cursor:pointer}
  #time-label{min-width:100px;text-align:center;font-size:13px;font-variant-numeric:tabular-nums}
  #controls-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
  button{background:var(--input-bg);color:var(--text);border:1px solid var(--border);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.15s}
  button:hover{background:var(--accent);color:#000;border-color:var(--accent)}
  button.active{background:var(--accent);color:#000;border-color:var(--accent)}
  #bookmark-bar{display:flex;gap:6px;align-items:center;margin-left:auto}
  #bookmark-bar select{background:var(--input-bg);color:var(--text);border:1px solid var(--border);padding:5px 10px;border-radius:6px;font-size:12px;cursor:pointer}
  #diag-panel{position:fixed;top:12px;right:12px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:8px;padding:10px 14px;font-size:11px;line-height:1.6;min-width:180px}
  #diag-panel .metric{display:flex;justify-content:space-between;gap:16px}
  #diag-panel .metric span:last-child{font-variant-numeric:tabular-nums;color:var(--accent)}
  #tooltip{position:fixed;pointer-events:none;z-index:20;background:var(--panel-bg);border:1px solid var(--border);border-radius:6px;padding:8px 12px;font-size:11px;display:none;white-space:nowrap}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="dashboard">
  <div id="timeline">
    <span style="font-size:12px;color:var(--accent)">TIME</span>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label">Day 0</span>
    <button id="btn-play">Play</button>
    <button id="btn-auto-rotate">Auto</button>
  </div>
  <div id="controls-row">
    <button id="btn-top">Top View</button>
    <button id="btn-persp">Perspective</button>
    <button id="btn-side">Side View</button>
    <button id="btn-wireframe">Wireframe</button>
    <button id="btn-rivers">Toggle Rivers</button>
    <button id="btn-particles">Toggle Particles</button>
    <div id="bookmark-bar">
      <select id="bookmark-select"><option value="">Bookmarks</option></select>
      <button id="btn-save-bm">Save</button>
      <button id="btn-del-bm">Del</button>
    </div>
  </div>
</div>
<div id="diag-panel">
  <div style="font-weight:700;margin-bottom:4px;color:var(--accent)">PERF DIAG</div>
  <div class="metric"><span>FPS</span><span id="diag-fps">60</span></div>
  <div class="metric"><span>Cache Hit%</span><span id="diag-cache">0</span></div>
  <div class="metric"><span>Allocs/frame</span><span id="diag-allocs">0</span></div>
  <div class="metric"><span>River Builds</span><span id="diag-rb">0</span></div>
  <div class="metric"><span>Particles</span><span id="diag-pc">0</span></div>
</div>
<div id="tooltip"></div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ────────────────────────────────────────────
// CACHE SYSTEM — tracks hit/miss for diagnostics
// ────────────────────────────────────────────
const cache = {
  terrain: new Map(),    // key: timestep → {geometry, heightfield}
  river: new Map(),      // key: timestep → TubeGeometry
  worldToGrid: new Map(),// key: `${wx|wy}` → {gx, gy}
  hits: 0,
  misses: 0,
  get(storage, key) {
    if (storage.has(key)) { this.hits++; return storage.get(key); }
    this.misses++; return null;
  },
  set(storage, key, val) { storage.set(key, val); return val; },
  ratio() { const t = this.hits + this.misses; return t ? Math.round(100 * this.hits / t) : 0; },
  resetCounters() { this.hits = 0; this.misses = 0; },
  clearAll() { this.terrain.clear(); this.river.clear(); this.worldToGrid.clear(); this.resetCounters(); }
};
// ────────────────────────────────────────────
// SYNTHETIC TIME-SERIES DATA (90 days, 50x50 grid)
// ────────────────────────────────────────────
const GRID = 50;
const DAYS = 90;
const GRID_SPACING = 1.0;
// Data arrays: [day][row][col] — pre-generated noise fields
function generateDataset() {
  const data = [];
  // Seed-based deterministic noise via stacked sine waves (fast to compute, cache-friendly)
  for (let d = 0; d < DAYS; d++) {
    const t = d / DAYS;
    const day = [];
    for (let r = 0; r < GRID; r++) {
      const row = [];
      for (let c = 0; c < GRID; c++) {
        const nx = c / GRID, ny = r / GRID;
        // Revenue: multi-octave sine terrain that shifts over time
        const rev = 1.5 * Math.sin(nx * 6 + t * 4) * Math.cos(ny * 5 + t * 3)
                  + 0.8 * Math.sin(nx * 12 - t * 2) * Math.cos(ny * 10 + t * 5)
                  + 0.4 * Math.sin(nx * 18 + t * 6) * Math.cos(ny * 15 - t * 3)
                  + 0.2 * (Math.sin(nx * 24) * Math.cos(ny * 20 + t));
        // User density: offset phase for secondary metric
        const users = 0.6 + 0.4 * Math.sin(nx * 7 + t * 3.5 + 2) * Math.cos(ny * 6 + t * 2.5 + 1);
        // Error rate: gaussian blobs that move
        const dx1 = nx - 0.3 - t * 0.15, dy1 = ny - 0.5 + t * 0.1;
        const dx2 = nx - 0.7 + t * 0.1, dy2 = ny - 0.3 - t * 0.12;
        const errors = 0.25 * Math.exp(-(dx1*dx1 + dy1*dy1) * 30)
                     + 0.20 * Math.exp(-(dx2*dx2 + dy2*dy2) * 40)
                     + 0.05 * Math.abs(Math.sin(nx * 20 + t * 8) * Math.cos(ny * 18));
        row.push({ revenue: rev, users, errors });
      }
      day.push(row);
    }
    data.push(day);
  }
  return data;
}
const dataset = generateDataset();
// ────────────────────────────────────────────
// TERRAIN BUILD (cached per timestep)
// ────────────────────────────────────────────
function buildTerrainGeometry(timestep) {
  const cached = cache.get(cache.terrain, timestep);
  if (cached) return cached;
  const day = dataset[timestep];
  const w = GRID, h = GRID;
  const vertices = new Float32Array(w * h * 3);
  const colors = new Float32Array(w * h * 3);
  const heightfield = new Float32Array(w * h);
  let minH = Infinity, maxH = -Infinity;
  // First pass: collect heights
  for (let r = 0; r < h; r++) {
    for (let c = 0; c < w; c++) {
      const idx = r * w + c;
      const val = day[r][c].revenue;
      heightfield[idx] = val;
      if (val < minH) minH = val;
      if (val > maxH) maxH = val;
    }
  }
  const hRange = maxH - minH || 1;
  // Second pass: position vertices and compute vertex colors from user density
  for (let r = 0; r < h; r++) {
    for (let c = 0; c < w; c++) {
      const idx = r * w + c;
      const vIdx = idx * 3;
      const d = day[r][c];
      // XZ plane positioning
      vertices[vIdx] = (c - w / 2) * GRID_SPACING;
      vertices[vIdx + 1] = heightfield[idx] * 4; // Y = elevation scaled
      vertices[vIdx + 2] = (r - h / 2) * GRID_SPACING;
      // Vegetation gradient: user density maps to green intensity, blended with warm base
      const u = d.users; // 0..1
      colors[vIdx] = 0.15 + u * 0.25;     // R: brown → warm
      colors[vIdx + 1] = 0.30 + u * 0.55;  // G: sparse → lush green
      colors[vIdx + 2] = 0.10 + u * 0.15;  // B: low blue
    }
  }
  // Build indices for the grid quads (two triangles per cell)
  const indices = [];
  for (let r = 0; r < h - 1; r++) {
    for (let c = 0; c < w - 1; c++) {
      const a = r * w + c;
      const b = a + 1;
      const d = (r + 1) * w + c;
      const e = d + 1;
      indices.push(a, b, d, b, e, d);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals(); // called once at build time, not per frame
  const result = { geometry: geo, heightfield };
  cache.set(cache.terrain, timestep, result);
  return result;
}
// ────────────────────────────────────────────
// RIVER GEOMETRY — traces error hot paths (cached per timestep)
// ────────────────────────────────────────────
let riverRebuildTimer = null;
function buildRiverGeometry(timestep) {
  const cached = cache.get(cache.river, timestep);
  if (cached) return cached;
  const day = dataset[timestep];
  // Find error hotspots via threshold and trace downhill from each
  const threshold = 0.15;
  const errorPoints = [];
  for (let r = 0; r < GRID; r++) {
    for (let c = 0; c < GRID; c++) {
      if (day[r][c].errors > threshold) {
        errorPoints.push({ r, c, err: day[r][c].errors });
      }
    }
  }
  // Sort by error magnitude, take top N as river sources
  errorPoints.sort((a, b) => b.err - a.err);
  const sources = errorPoints.slice(0, 5);
  // For each source, trace downhill through the revenue heightfield
  const paths = [];
  const hf = cache.get(cache.terrain, timestep)?.heightfield;
  if (!hf) return null;
  for (const src of sources) {
    const path = [];
    let cr = src.r, cc = src.c;
    const maxSteps = 40;
    for (let s = 0; s < maxSteps; s++) {
      if (cr < 0 || cr >= GRID || cc < 0 || cc >= GRID) break;
      path.push(new THREE.Vector3(
        (cc - GRID / 2) * GRID_SPACING,
        hf[cr * GRID + cc] * 4 + 0.15,
        (cr - GRID / 2) * GRID_SPACING
      ));
      // Steepest descent among 8 neighbors
      let bestDr = 0, bestDc = 0, lowestH = hf[cr * GRID + cc];
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          if (dr === 0 && dc === 0) continue;
          const nr = cr + dr, nc = cc + dc;
          if (nr < 0 || nr >= GRID || nc < 0 || nc >= GRID) continue;
          const nh = hf[nr * GRID + nc];
          if (nh < lowestH) { lowestH = nh; bestDr = dr; bestDc = dc; }
        }
      }
      if (bestDr === 0 && bestDc === 0) break; // local minimum
      cr += bestDr; cc += bestDc;
    }
    if (path.length >= 2) paths.push(path);
  }
  // Merge paths into a single group
  const group = new THREE.Group();
  const riverMat = new THREE.MeshBasicMaterial({
    color: 0xff4444, transparent: true, opacity: 0.7, side: THREE.DoubleSide
  });
  for (const pts of paths) {
    const curve = new THREE.CatmullRomCurve3(pts);
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.12, 6, false);
    const mesh = new THREE.Mesh(tubeGeo, riverMat);
    group.add(mesh);
  }
  cache.set(cache.river, timestep, group);
  diagState.riverBuilds++;
  return group;
}
// ────────────────────────────────────────────
// PARTICLE SYSTEM — data flow trails (BufferGeometry reuse, CPU-side pos array)
// ────────────────────────────────────────────
const PARTICLE_COUNT = 600;
let particleGeo, particleMat, particleSystem;
let particleData = []; // {path, progress, speed}
let particlePositions; // Float32Array reference to geo.attributes.position.array
function initParticles() {
  // Pre-compute paths from dataset across all days
  const allPaths = [];
  // Generate flow paths: pick random start points and trace them through revenue valleys
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const startDay = Math.floor(Math.random() * DAYS);
    const sr = Math.floor(Math.random() * GRID);
    const sc = Math.floor(Math.random() * GRID);
    const path = [];
    let cr = sr, cc = sc;
    for (let d = startDay; d < Math.min(startDay + 5, DAYS); d++) {
      const day = dataset[d];
      // Move toward lower revenue (valley flow) with slight randomness
      let bestDr = 0, bestDc = 0, lowest = day[cr][cc].revenue;
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          const nr = cr + dr, nc = cc + dc;
          if (nr < 0 || nr >= GRID || nc < 0 || nc >= GRID) continue;
          const v = day[nr][nc].revenue - 0.1 * Math.random();
          if (v < lowest) { lowest = v; bestDr = dr; bestDc = dc; }
        }
      }
      cr += bestDr; cc += bestDc;
      cr = Math.max(0, Math.min(GRID - 1, cr));
      cc = Math.max(0, Math.min(GRID - 1, cc));
      const h = day[cr][cc].revenue * 4;
      path.push(new THREE.Vector3(
        (cc - GRID / 2) * GRID_SPACING,
        h + 0.3,
        (cr - GRID / 2) * GRID_SPACING
      ));
    }
    if (path.length >= 2) allPaths.push(path);
  }
  // Reuse single buffer: allocate once
  const count = Math.min(allPaths.length, PARTICLE_COUNT);
  particlePositions = new Float32Array(count * 3);
  // Initialize at first point of each path
  for (let i = 0; i < count; i++) {
    const p = allPaths[i][0];
    particlePositions[i * 3] = p.x;
    particlePositions[i * 3 + 1] = p.y;
    particlePositions[i * 3 + 2] = p.z;
  }
  particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  // Simple circle sprite via canvas
  const canvas = document.createElement('canvas');
  canvas.width = 16; canvas.height = 16;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
  gradient.addColorStop(0, 'rgba(255,200,100,1)');
  gradient.addColorStop(0.4, 'rgba(255,140,40,0.7)');
  gradient.addColorStop(1, 'rgba(255,80,20,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 16, 16);
  const texture = new THREE.CanvasTexture(canvas);
  particleMat = new THREE.PointsMaterial({
    size: 0.35, map: texture, blending: THREE.AdditiveBlending,
    depthWrite: false, transparent: true, opacity: 0.85
  });
  particleSystem = new THREE.Points(particleGeo, particleMat);
  // Store particle state for per-frame update
  particleData = allPaths.slice(0, count).map(path => ({
    path, progress: 0, speed: 0.002 + Math.random() * 0.006
  }));
  diagState.particleCount = count;
}
// Per-frame particle update: reuse particlePositions array, no allocations
function updateParticles() {
  if (!particleSystem || !particleSystem.visible) return;
  const pos = particlePositions;
  for (let i = 0; i < particleData.length; i++) {
    const pd = particleData[i];
    pd.progress += pd.speed;
    if (pd.progress >= 1) pd.progress = 0; // loop back
    const idx = Math.floor(pd.progress * (pd.path.length - 1));
    const frac = pd.progress * (pd.path.length - 1) - idx;
    const a = pd.path[idx];
    const b = pd.path[Math.min(idx + 1, pd.path.length - 1)];
    // Linear interpolation between path points
    pos[i * 3] = a.x + (b.x - a.x) * frac;
    pos[i * 3 + 1] = a.y + (b.y - a.y) * frac;
    pos[i * 3 + 2] = a.z + (b.z - a.z) * frac;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ────────────────────────────────────────────
// WORLD-TO-GRID COORDINATE TRANSFORM (memoized, cleared each frame)
// ────────────────────────────────────────────
function worldToGrid(wx, wy, heightfield) {
  const key = `${wx.toFixed(2)}|${wy.toFixed(2)}`;
  const cached = cache.get(cache.worldToGrid, key);
  if (cached) return cached;
  const gx = Math.round(wx / GRID_SPACING + GRID / 2);
  const gy = Math.round(wy / GRID_SPACING + GRID / 2);
  const result = {
    gx: Math.max(0, Math.min(GRID - 1, gx)),
    gy: Math.max(0, Math.min(GRID - 1, gy))
  };
  cache.set(cache.worldToGrid, key, result);
  return result;
}
// ────────────────────────────────────────────
// SCENE SETUP
// ────────────────────────────────────────────
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 40, 120);
const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.5, 200);
camera.position.set(30, 22, 35);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 3, 0);
controls.minDistance = 8;
controls.maxDistance = 80;
controls.maxPolarAngle = Math.PI * 0.7;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
// Lighting
const ambient = new THREE.AmbientLight(0x404060, 1.2);
scene.add(ambient);
const dirLight = new THREE.DirectionalLight(0xffeedd, 1.8);
dirLight.position.set(20, 30, 15);
scene.add(dirLight);
const fillLight = new THREE.DirectionalLight(0x6688cc, 0.6);
fillLight.position.set(-15, 5, -10);
scene.add(fillLight);
// Ground grid
const gridHelper = new THREE.GridHelper(GRID * GRID_SPACING, GRID, 0x333355, 0x222244);
gridHelper.position.y = -2;
scene.add(gridHelper);
// ────────────────────────────────────────────
// STATE
// ────────────────────────────────────────────
let currentTimestep = 0;
let terrainMesh = null;
let riverGroup = null;
let wireframeMode = false;
let riversVisible = true, particlesVisible = true;
let isPlaying = false;
let playInterval = null;
let bookmarks = [];
const diagState = {
  fps: 60, allocs: 0, riverBuilds: 0, particleCount: 0, frameCount: 0, lastFpsTime: performance.now()
};
// ────────────────────────────────────────────
// SCENE UPDATE: swap terrain + rivers for current timestep
// ────────────────────────────────────────────
function updateScene(timestep) {
  currentTimestep = Math.max(0, Math.min(DAYS - 1, timestep));
  // Terrain: remove old, insert cached or build new
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    scene.remove(terrainMesh);
  }
  const { geometry } = buildTerrainGeometry(currentTimestep);
  const mat = new THREE.MeshPhongMaterial({
    vertexColors: true, side: THREE.DoubleSide,
    flatShading: false, shininess: 15,
    wireframe: wireframeMode
  });
  terrainMesh = new THREE.Mesh(geometry, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Rivers: debounced rebuild
  if (riversVisible) {
    if (riverGroup) { scene.remove(riverGroup); /* TubeGeometry disposed inside group */ }
    if (riverRebuildTimer) clearTimeout(riverRebuildTimer);
    riverRebuildTimer = setTimeout(() => {
      riverGroup = buildRiverGeometry(currentTimestep);
      if (riverGroup && riversVisible) scene.add(riverGroup);
      riverRebuildTimer = null;
    }, 200); // 200ms debounce
  }
  // Clear worldToGrid cache each frame
  cache.worldToGrid.clear();
  diagState.allocs = 0;
  document.getElementById('time-slider').value = currentTimestep;
  document.getElementById('time-label').textContent = `Day ${currentTimestep}`;
}
// Initial build
updateScene(0);
initParticles();
scene.add(particleSystem);
// ────────────────────────────────────────────
// EVENT HANDLERS
// ────────────────────────────────────────────
document.getElementById('time-slider').addEventListener('input', (e) => {
  const t = parseInt(e.target.value);
  updateScene(t);
});
document.getElementById('btn-play').addEventListener('click', () => {
  isPlaying = !isPlaying;
  const btn = document.getElementById('btn-play');
  btn.textContent = isPlaying ? 'Pause' : 'Play';
  btn.classList.toggle('active', isPlaying);
  if (isPlaying) {
    playInterval = setInterval(() => {
      let next = currentTimestep + 1;
      if (next >= DAYS) next = 0;
      updateScene(next);
      document.getElementById('time-slider').value = next;
    }, 180);
  } else {
    clearInterval(playInterval);
    playInterval = null;
  }
});
document.getElementById('btn-auto-rotate').addEventListener('click', (e) => {
  controls.autoRotate = !controls.autoRotate;
  e.target.classList.toggle('active', controls.autoRotate);
});
// Camera presets
const presets = {
  top:    { pos: [0, 40, 1], target: [0, 0, 0] },
  persp:  { pos: [30, 22, 35], target: [0, 3, 0] },
  side:   { pos: [0, 5, 45], target: [0, 2, 0] }
};
function animateCamera(pos, target, duration = 800) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...pos);
  const endTarget = new THREE.Vector3(...target);
  const startTime = performance.now();
  function step() {
    const elapsed = performance.now() - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
document.getElementById('btn-top').addEventListener('click', () => animateCamera(presets.top.pos, presets.top.target));
document.getElementById('btn-persp').addEventListener('click', () => animateCamera(presets.persp.pos, presets.persp.target));
document.getElementById('btn-side').addEventListener('click', () => animateCamera(presets.side.pos, presets.side.target));
document.getElementById('btn-wireframe').addEventListener('click', (e) => {
  wireframeMode = !wireframeMode;
  e.target.classList.toggle('active', wireframeMode);
  if (terrainMesh) terrainMesh.material.wireframe = wireframeMode;
});
document.getElementById('btn-rivers').addEventListener('click', (e) => {
  riversVisible = !riversVisible;
  e.target.classList.toggle('active', !riversVisible);
  if (riverGroup) riverGroup.visible = riversVisible;
  if (riversVisible && !riverGroup) {
    riverGroup = buildRiverGeometry(currentTimestep);
    if (riverGroup) scene.add(riverGroup);
  }
});
document.getElementById('btn-particles').addEventListener('click', (e) => {
  particlesVisible = !particlesVisible;
  e.target.classList.toggle('active', !particlesVisible);
  particleSystem.visible = particlesVisible;
});
// Bookmarks
function updateBookmarkSelect() {
  const sel = document.getElementById('bookmark-select');
  sel.innerHTML = '<option value="">Bookmarks</option>';
  for (let i = 0; i < bookmarks.length; i++) {
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = bookmarks[i].label || `View ${i + 1}`;
    sel.appendChild(opt);
  }
}
document.getElementById('bookmark-select').addEventListener('change', (e) => {
  const idx = parseInt(e.target.value);
  if (isNaN(idx) || !bookmarks[idx]) return;
  const bm = bookmarks[idx];
  animateCamera(bm.pos, bm.target);
});
document.getElementById('btn-save-bm').addEventListener('click', () => {
  const label = prompt('Bookmark name:') || `View ${bookmarks.length + 1}`;
  bookmarks.push({
    label,
    pos: camera.position.toArray(),
    target: controls.target.toArray()
  });
  updateBookmarkSelect();
});
document.getElementById('btn-del-bm').addEventListener('click', () => {
  const sel = document.getElementById('bookmark-select');
  const idx = parseInt(sel.value);
  if (isNaN(idx) || !bookmarks[idx]) return;
  bookmarks.splice(idx, 1);
  updateBookmarkSelect();
});
// Tooltip hover
const raycaster = new THREE.Raycaster();
const tooltip = document.getElementById('tooltip');
const mouse = new THREE.Vector2();
let hoveredHeightfield = null;
renderer.domElement.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (terrainMesh) {
    const hits = raycaster.intersectObject(terrainMesh);
    if (hits.length > 0 && hoveredHeightfield) {
      const pt = hits[0].point;
      const grid = worldToGrid(pt.x, pt.z, hoveredHeightfield);
      const d = dataset[currentTimestep][grid.gy][grid.gx];
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 18) + 'px';
      tooltip.style.top = (e.clientY - 18) + 'px';
      tooltip.innerHTML = `Revenue: ${d.revenue.toFixed(2)} &nbsp;Users: ${d.users.toFixed(2)} &nbsp;Errors: ${(d.errors * 100).toFixed(1)}%`;
    } else {
      tooltip.style.display = 'none';
    }
  }
});
renderer.domElement.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
// Resize
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'w': document.getElementById('btn-wireframe').click(); break;
    case 'r': document.getElementById('btn-rivers').click(); break;
    case 'p': document.getElementById('btn-particles').click(); break;
    case 'a': document.getElementById('btn-auto-rotate').click(); break;
    case 'arrowleft': updateScene(currentTimestep - 1); break;
    case 'arrowright': updateScene(currentTimestep + 1); break;
    case ' ': e.preventDefault(); document.getElementById('btn-play').click(); break;
  }
});
// ────────────────────────────────────────────
// RENDER LOOP — no allocations in hot path
// ────────────────────────────────────────────
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  updateParticles();
  // Update hover reference to current heightfield
  const terrainCache = cache.get(cache.terrain, currentTimestep);
  hoveredHeightfield = terrainCache ? terrainCache.heightfield : null;
  renderer.render(scene, camera);
  // Diagnostic update (every 30 frames)
  diagState.frameCount++;
  if (diagState.frameCount % 30 === 0) {
    const now = performance.now();
    diagState.fps = Math.round(30000 / (now - diagState.lastFpsTime));
    diagState.lastFpsTime = now;
    document.getElementById('diag-fps').textContent = diagState.fps;
    document.getElementById('diag-cache').textContent = cache.ratio();
    document.getElementById('diag-allocs').textContent = diagState.allocs;
    document.getElementById('diag-rb').textContent = diagState.riverBuilds;
    document.getElementById('diag-pc').textContent = diagState.particleCount;
  }
}
animate();
console.log('3D Data Terrain Explorer ready — W:wireframe R:rivers P:particles A:auto-rotate Arrows:time Space:play');
</script>
</body>
</html>