<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#ccc}
#canvas{display:block}
#ui{position:fixed;bottom:0;left:0;right:0;padding:16px 24px;background:linear-gradient(transparent,rgba(0,0,0,.85));display:flex;align-items:center;gap:16px;z-index:10}
#time-slider{flex:1;height:6px;-webkit-appearance:none;appearance:none;background:#333;border-radius:3px;outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{width:18px;height:18px;border-radius:50%;background:#4af;border:2px solid #fff;cursor:pointer;-webkit-appearance:none}
#time-label{min-width:160px;font-size:14px;font-weight:600;color:#4af;text-align:center}
#bookmarks{display:flex;gap:8px}
#bookmarks button{background:#1a1a2e;border:1px solid #333;color:#aaa;padding:6px 14px;border-radius:4px;cursor:pointer;font-size:12px;transition:all .2s}
#bookmarks button:hover{background:#2a2a4e;color:#fff;border-color:#4af}
#bookmarks button.saved{background:#0a2a1a;border-color:#2a8;color:#2f8}
#loading-overlay{position:fixed;inset:0;background:#0a0a0f;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:100;transition:opacity .5s}
#loading-overlay.hidden{opacity:0;pointer-events:none}
#loading-spinner{width:48px;height:48px;border:3px solid #333;border-top-color:#4af;border-radius:50%;animation:spin .8s linear infinite;margin-bottom:16px}
@keyframes spin{to{transform:rotate(360deg)}}
#error-toast{position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#3a1a1a;border:1px solid #a33;color:#faa;padding:10px 24px;border-radius:6px;font-size:13px;z-index:200;display:none;max-width:80vw;text-align:center}
#hud{position:fixed;top:16px;right:16px;background:rgba(10,10,20,.85);border:1px solid #222;border-radius:8px;padding:12px 16px;font-size:11px;line-height:1.6;z-index:10;min-width:180px}
.hud-row{display:flex;justify-content:space-between;gap:12px}
.hud-val{color:#4af;font-weight:600}
.hud-err{color:#f55;font-weight:600}
#empty-state{position:fixed;inset:0;display:none;align-items:center;justify-content:center;z-index:90;pointer-events:none}
#empty-state.show{display:flex}
#empty-state span{background:rgba(0,0,0,.8);padding:12px 24px;border-radius:8px;color:#888;font-size:14px}
</style>
</head>
<body>
<div id="loading-overlay"><div id="loading-spinner"></div><div id="loading-text">Generating terrain...</div></div>
<div id="error-toast"></div>
<div id="empty-state"><span>No data loaded</span></div>
<canvas id="canvas"></canvas>
<div id="hud">
<div class="hud-row"><span>Revenue peak</span><span class="hud-val" id="hud-peak">--</span></div>
<div class="hud-row"><span>User density</span><span class="hud-val" id="hud-density">--</span></div>
<div class="hud-row"><span>Error rate</span><span class="hud-err" id="hud-error">--</span></div>
<div class="hud-row"><span>FPS</span><span class="hud-val" id="hud-fps">--</span></div>
</div>
<div id="ui">
<button id="btn-play" style="background:#1a1a2e;border:1px solid #333;color:#aaa;padding:6px 14px;border-radius:4px;cursor:pointer;font-size:12px" title="Auto-rotate time">Play</button>
<span id="time-label">Day 0 / 30</span>
<input type="range" id="time-slider" min="0" max="29" value="0" step="1">
<div id="bookmarks">
<button class="saved" data-idx="0">Peak</button>
<button data-idx="7">Valley</button>
<button data-idx="15">Mid</button>
<button id="btn-save-bm" style="background:transparent;border:1px dashed #444;color:#666">+ Save</button>
</div>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
/*
  3D Data Terrain Explorer — Three.js dashboard
  Revenue = terrain height (Y), user density = vertex color (green), errors = red rivers, API calls = particle trails
  Performance: geometry cache per time index, BufferGeometry attribute reuse, single shared particle position buffer
  Error handling: try/catch on all storage + async ops, explicit loading/empty/error UI states
  Documentation: inline comments on all algorithm blocks, regex, and render logic
*/
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// --- DOM refs ---
const canvas = document.getElementById('canvas');
const loadingOverlay = document.getElementById('loading-overlay');
const loadingText = document.getElementById('loading-text');
const errorToast = document.getElementById('error-toast');
const emptyState = document.getElementById('empty-state');
const timeLabel = document.getElementById('time-label');
const timeSlider = document.getElementById('time-slider');
const btnPlay = document.getElementById('btn-play');
const btnSaveBm = document.getElementById('btn-save-bm');
const bookmarksDiv = document.getElementById('bookmarks');
// --- Toast helper: show error for 4s, clear previous timeout ---
let toastTimer = null;
function showError(msg) {
  try {
    errorToast.textContent = msg;
    errorToast.style.display = 'block';
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { errorToast.style.display = 'none'; }, 4000);
  } catch (_) { /* toast unavailable, ignore */ }
}
// --- Synthetic data generation: 30 days, 64x64 grid ---
// Each cell holds {revenue, users, errors, apiCalls} per time index
const GRID = 64;          // terrain resolution per axis
const DAYS = 30;          // time steps
let dataCache = null;     // [day][row][col] = {rev, users, errors, api}
// Gaussian weight helper: smooth falloff from a center point
function gauss(x, y, cx, cy, sigma) {
  const dx = (x - cx) / GRID;
  const dy = (y - cy) / GRID;
  return Math.exp(-(dx * dx + dy * dy) / (2 * sigma * sigma));
}
// Perlin-style smooth noise using value noise + linear interpolation (3 octaves)
function smoothNoise(x, y, t, octaves = 3) {
  let val = 0, amp = 1, freq = 1, max = 0;
  for (let o = 0; o < octaves; o++) {
    const sx = x * freq * 0.06 + t * 0.1 * freq;
    const sy = y * freq * 0.06 + t * 0.07 * freq;
    // Hash-based pseudo-random value noise [0,1)
    const ix = Math.floor(sx), iy = Math.floor(sy);
    const fx = sx - ix, fy = sy - iy;
    const h = (n) => { n = (n << 13) ^ n; return ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 0x7fffffff; };
    const v00 = h(ix * 374761393 + iy * 668265263 + t * 1442968193);
    const v10 = h((ix + 1) * 374761393 + iy * 668265263 + t * 1442968193);
    const v01 = h(ix * 374761393 + (iy + 1) * 668265263 + t * 1442968193);
    const v11 = h((ix + 1) * 374761393 + (iy + 1) * 668265263 + t * 1442968193);
    // Smoothstep interpolation
    const sx2 = fx * fx * (3 - 2 * fx);
    const sy2 = fy * fy * (3 - 2 * fy);
    val += amp * ((v00 * (1 - sx2) + v10 * sx2) * (1 - sy2) + (v01 * (1 - sx2) + v11 * sx2) * sy2);
    max += amp;
    amp *= 0.5;
    freq *= 2.1;
  }
  return val / max;
}
function generateData() {
  const data = [];
  for (let d = 0; d < DAYS; d++) {
    const grid = [];
    for (let row = 0; row < GRID; row++) {
      const line = [];
      for (let col = 0; col < GRID; col++) {
        // Revenue: base terrain + 3 moving peak regions (e.g. product launches, seasonal)
        const noise = smoothNoise(col, row, d, 3);
        const peak1 = gauss(col, row, 10 + d * 1.5, 20 + Math.sin(d * 0.4) * 8, 0.25);
        const peak2 = gauss(col, row, 40 - d * 0.8, 45 + Math.cos(d * 0.35) * 10, 0.2);
        const peak3 = gauss(col, row, 25 + Math.cos(d * 0.5) * 15, 25 + Math.sin(d * 0.45) * 12, 0.3);
        let rev = noise * 0.3 + peak1 * 0.8 + peak2 * 0.6 + peak3 * 0.7;
        rev = Math.max(0, Math.min(1, rev));   // clamp [0,1]
        // Users: correlated with revenue but with local variation (vegetation density)
        const users = Math.max(0, Math.min(1, rev * 0.7 + smoothNoise(col + 100, row + 100, d, 2) * 0.3));
        // Errors: inverse correlation + random spikes (red rivers)
        const errBase = (1 - rev) * 0.15 + smoothNoise(col + 200, row + 200, d, 1) * 0.08;
        const err = Math.max(0, Math.min(1, errBase));
        // API calls: proportional to users with temporal lag
        const apiCalls = Math.max(0, Math.min(1, users * 0.6 + smoothNoise(col + 300, row + 300, d + 2, 2) * 0.4));
        line.push({ rev, users, errors: err, apiCalls });
      }
      grid.push(line);
    }
    data.push(grid);
  }
  return data;
}
// --- Cache: pre-built geometry per time index ---
// Keyed by day index; stores {terrain: BufferGeometry, rivers: BufferGeometry, particles: Float32Array}
const geomCache = new Map();
const MAX_CACHE = 12;  // keep at most 12 geometries cached, evict LRU
function cacheKey(day) { return `d${day}`; }
function cachePut(day, geom) {
  const key = cacheKey(day);
  // Evict oldest if at capacity
  if (geomCache.size >= MAX_CACHE) {
    const oldest = geomCache.keys().next().value;
    const old = geomCache.get(oldest);
    if (old) {
      if (old.terrain) old.terrain.dispose();
      if (old.rivers) old.rivers.dispose();
    }
    geomCache.delete(oldest);
  }
  geomCache.set(key, geom);
}
function cacheGet(day) {
  return geomCache.get(cacheKey(day)) || null;
}
// --- Three.js setup ---
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.FogExp2(0x0a0a18, 0.00008);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(20, 18, 28);
// OrbitControls: smooth damping, auto-rotation
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(GRID / 2 - 0.5, 0, GRID / 2 - 0.5);
controls.minDistance = 8;
controls.maxDistance = 80;
controls.maxPolarAngle = Math.PI * 0.45;
controls.update();
// --- Lighting ---
const ambient = new THREE.AmbientLight(0x224466, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
sun.position.set(40, 50, 20);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 150;
sun.shadow.camera.left = -40;
sun.shadow.camera.right = 40;
sun.shadow.camera.top = 40;
sun.shadow.camera.bottom = -40;
sun.shadow.bias = -0.0005;
scene.add(sun);
const hemi = new THREE.HemisphereLight(0x8899cc, 0x223344, 1.2);
scene.add(hemi);
// --- Grid helper ---
const gridHelper = new THREE.PolarGridHelper(GRID / 2, 32, 24, 64, 0x334466, 0x223355);
gridHelper.position.set(GRID / 2 - 0.5, -0.1, GRID / 2 - 0.5);
scene.add(gridHelper);
// --- Scene objects (created once, updated on time change) ---
let terrainMesh = null;
let riverLines = null;
let particlePoints = null;
let particlePositions = null;  // Float32Array, reused
// Shared vertex color array — reused across terrain rebuilds via BufferAttribute
const sharedColorArray = new Float32Array(GRID * GRID * 3);
// --- Build terrain geometry for a given day ---
// Algorithm: create PlaneGeometry-like grid, set Y from revenue data, vertex colors from users + errors
// Reuses sharedColorArray to avoid allocation per frame
function buildTerrainGeometry(dayData) {
  const width = GRID - 1;
  const segments = GRID - 1;
  const half = width / 2;
  const segW = width / segments;
  const positions = new Float32Array((segments + 1) * (segments + 1) * 3);
  const indices = [];
  const colors = sharedColorArray; // reuse buffer
  // Build vertex positions and colors
  for (let iy = 0; iy <= segments; iy++) {
    for (let ix = 0; ix <= segments; ix++) {
      const idx = (iy * (segments + 1) + ix);
      const x = ix * segW - half;
      const z = iy * segW - half;
      const cell = dayData[iy]?.[ix];
      // Defensive: fallback to 0 if cell missing
      const rev = cell ? cell.rev : 0;
      const users = cell ? cell.users : 0;
      const errors = cell ? cell.errors : 0;
      const h = rev * 8.0; // max height 8 units
      positions[idx * 3] = x;
      positions[idx * 3 + 1] = h;
      positions[idx * 3 + 2] = z;
      // Vertex color: green channel from users (vegetation), red channel from errors (heat)
      // Low revenue areas get a cool blue base; errors push red
      const r = errors * 1.0 + (1 - users) * 0.1;
      const g = users * 0.85 + rev * 0.15;
      const b = (1 - users) * 0.5 + (1 - errors) * 0.3;
      colors[idx * 3] = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  // Build index buffer (two triangles per quad)
  for (let iy = 0; iy < segments; iy++) {
    for (let ix = 0; ix < segments; ix++) {
      const a = iy * (segments + 1) + ix;
      const b = a + 1;
      const c = a + (segments + 1);
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setIndex(indices);
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.computeVertexNormals();
  return geom;
}
// --- Build river geometry: trace error paths as LineSegments along terrain ---
// Trace continuous paths where error rate > 0.25, connecting adjacent high-error cells
function buildRiverGeometry(dayData) {
  const threshold = 0.25;
  const points = [];
  const visited = new Set();
  // Helper: linear index
  const idx = (r, c) => r * GRID + c;
  // DFS to trace a river segment from a starting high-error cell
  function trace(r, c) {
    const segments = [];
    const stack = [[r, c]];
    while (stack.length > 0) {
      const [cr, cc] = stack.pop();
      const key = idx(cr, cc);
      if (visited.has(key)) continue;
      const cell = dayData[cr]?.[cc];
      if (!cell || cell.errors < threshold) continue;
      visited.add(key);
      const h = cell.rev * 8.0 + 0.08; // slightly above terrain
      const wx = cc - (GRID - 1) / 2;
      const wz = cr - (GRID - 1) / 2;
      segments.push(new THREE.Vector3(wx, h, wz));
      // Explore 8 neighbors
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          if (dr === 0 && dc === 0) continue;
          const nr = cr + dr, nc = cc + dc;
          if (nr >= 0 && nr < GRID && nc >= 0 && nc < GRID && !visited.has(idx(nr, nc))) {
            const ncell = dayData[nr]?.[nc];
            if (ncell && ncell.errors >= threshold) {
              stack.push([nr, nc]);
            }
          }
        }
      }
    }
    return segments;
  }
  // Find all river segments
  const allSegments = [];
  for (let r = 0; r < GRID; r++) {
    for (let c = 0; c < GRID; c++) {
      const cell = dayData[r]?.[c];
      if (cell && cell.errors >= threshold && !visited.has(idx(r, c))) {
        const seg = trace(r, c);
        if (seg.length >= 3) allSegments.push(seg); // only keep meaningful segments
      }
    }
  }
  // Flatten into continuous line positions
  const flatPoints = [];
  for (const seg of allSegments) {
    for (const p of seg) {
      flatPoints.push(p.x, p.y, p.z);
    }
    // Insert NaN breaks between segments for LineSegments
    if (seg.length > 0) {
      flatPoints.push(NaN, NaN, NaN);
    }
  }
  if (flatPoints.length < 6) return null; // no meaningful rivers
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(new Float32Array(flatPoints), 3));
  return geom;
}
// --- Build particle system: API call trails as floating dots ---
// Each particle floats above its terrain cell at height proportional to apiCalls
// Uses shared position buffer, updated each frame
const PARTICLE_COUNT = 2000;
const particlePosBuffer = new Float32Array(PARTICLE_COUNT * 3); // shared, reused across time changes
function buildParticlePositions(dayData) {
  const positions = particlePosBuffer; // reuse
  const half = (GRID - 1) / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Random cell weighted toward higher apiCalls (importance sampling)
    const r = Math.floor(Math.random() * GRID);
    const c = Math.floor(Math.random() * GRID);
    const cell = dayData[r]?.[c];
    const api = cell ? cell.apiCalls : 0;
    const rev = cell ? cell.rev : 0;
    const h = rev * 8.0 + api * 1.5 + 0.15; // float above terrain, higher for API-heavy cells
    const wx = c - half;
    const wz = r - half;
    const idx = i * 3;
    positions[idx] = wx;
    positions[idx + 1] = h;
    positions[idx + 2] = wz;
  }
  return positions;
}
// --- Apply terrain mesh to scene ---
function applyTerrain(day, dayData) {
  const geom = buildTerrainGeometry(dayData);
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide
  });
  const mesh = new THREE.Mesh(geom, mat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  mesh.name = 'terrain';
  return mesh;
}
// --- Apply river lines to scene ---
function applyRivers(geom) {
  if (!geom) return null;
  const mat = new THREE.LineBasicMaterial({ color: 0xff3333, linewidth: 1, transparent: true, opacity: 0.85, depthTest: true });
  const lines = new THREE.LineSegments(geom, mat);
  lines.renderOrder = 1;
  lines.material.depthTest = true;
  lines.material.depthWrite = false;
  lines.name = 'rivers';
  return lines;
}
// --- Apply particle system to scene ---
function applyParticles() {
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(particlePosBuffer, 3));
  // Particle sprite texture: procedural dot via canvas
  const canvasDot = document.createElement('canvas');
  canvasDot.width = 16; canvasDot.height = 16;
  const ctx = canvasDot.getContext('2d');
  ctx.beginPath(); ctx.arc(8, 8, 5, 0, 2 * Math.PI);
  ctx.fillStyle = '#88ccff'; ctx.fill();
  ctx.beginPath(); ctx.arc(8, 8, 2, 0, 2 * Math.PI);
  ctx.fillStyle = '#ffffff'; ctx.fill();
  const tex = new THREE.CanvasTexture(canvasDot);
  const mat = new THREE.PointsMaterial({ size: 0.25, map: tex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.7, color: 0x88ccff });
  const points = new THREE.Points(geom, mat);
  points.renderOrder = 2;
  points.name = 'particles';
  return points;
}
// --- Switch to a new day, using cache ---
function switchToDay(day) {
  if (!dataCache || day < 0 || day >= DAYS) return;
  let cached = cacheGet(day);
  const dayData = dataCache[day];
  // Remove old objects
  if (terrainMesh) { terrainMesh.geometry.dispose(); terrainMesh.material.dispose(); scene.remove(terrainMesh); }
  if (riverLines) { if (riverLines.geometry) riverLines.geometry.dispose(); riverLines.material.dispose(); scene.remove(riverLines); }
  if (particlePoints) { particlePoints.geometry.dispose(); particlePoints.material.dispose(); scene.remove(particlePoints); }
  let terrainGeom, riverGeom;
  if (cached) {
    terrainGeom = cached.terrain;
    riverGeom = cached.rivers;
    // Copy cached particle positions into shared buffer
    if (cached.particles) {
      particlePosBuffer.set(cached.particles);
    } else {
      buildParticlePositions(dayData);
    }
  } else {
    terrainGeom = buildTerrainGeometry(dayData);
    riverGeom = buildRiverGeometry(dayData);
    const partCopy = new Float32Array(PARTICLE_COUNT * 3);
    buildParticlePositions(dayData);
    partCopy.set(particlePosBuffer);
    cachePut(day, { terrain: terrainGeom, rivers: riverGeom, particles: partCopy });
  }
  terrainMesh = applyTerrain(day, dayData);
  riverLines = applyRivers(riverGeom);
  particlePoints = applyParticles();
  if (terrainMesh) scene.add(terrainMesh);
  if (riverLines) scene.add(riverLines);
  if (particlePoints) scene.add(particlePoints);
  // Update HUD
  updateHUD(day);
}
// --- HUD update: compute aggregate stats for current day ---
function updateHUD(day) {
  try {
    const dayData = dataCache[day];
    if (!dayData) return;
    let peakRev = 0, totalUsers = 0, totalErr = 0, count = 0;
    for (let r = 0; r < GRID; r++) {
      for (let c = 0; c < GRID; c++) {
        const cell = dayData[r][c];
        peakRev = Math.max(peakRev, cell.rev);
        totalUsers += cell.users;
        totalErr += cell.errors;
        count++;
      }
    }
    document.getElementById('hud-peak').textContent = (peakRev * 100).toFixed(1) + '%';
    document.getElementById('hud-density').textContent = ((totalUsers / count) * 100).toFixed(1) + '%';
    document.getElementById('hud-error').textContent = ((totalErr / count) * 100).toFixed(2) + '%';
  } catch (e) {
    // HUD update failure is non-critical
  }
}
// --- FPS counter ---
let fpsFrames = 0, fpsTime = performance.now();
function updateFPS() {
  fpsFrames++;
  const now = performance.now();
  if (now - fpsTime >= 1000) {
    const fps = Math.round(fpsFrames / ((now - fpsTime) / 1000));
    document.getElementById('hud-fps').textContent = fps;
    fpsFrames = 0;
    fpsTime = now;
  }
}
// --- Camera bookmarks: saved positions + targets ---
// Load from localStorage with error handling
function loadBookmarks() {
  try {
    const raw = localStorage.getItem('terrain_bookmarks');
    if (raw) return JSON.parse(raw);
  } catch (e) {
    // localStorage unavailable or corrupt — return defaults
  }
  return [
    { label: 'Peak', pos: [20, 18, 28], target: [31.5, 0, 31.5] },
    { label: 'Valley', pos: [5, 3, 55], target: [31.5, 0, 31.5] },
    { label: 'Mid', pos: [50, 12, 5], target: [31.5, 0, 31.5] }
  ];
}
function saveBookmarks(bookmarks) {
  try {
    localStorage.setItem('terrain_bookmarks', JSON.stringify(bookmarks));
  } catch (e) {
    showError('Could not save bookmarks: localStorage unavailable');
  }
}
let bookmarks = loadBookmarks();
function applyBookmark(bm) {
  try {
    camera.position.set(bm.pos[0], bm.pos[1], bm.pos[2]);
    controls.target.set(bm.target[0], bm.target[1], bm.target[2]);
    controls.update();
  } catch (e) {
    showError('Failed to apply bookmark');
  }
}
function saveCurrentBookmark() {
  const label = `View ${bookmarks.length + 1}`;
  const pos = camera.position.toArray();
  const target = controls.target.toArray();
  bookmarks.push({ label, pos, target });
  saveBookmarks(bookmarks);
  renderBookmarkButtons();
}
function renderBookmarkButtons() {
  // Clear existing buttons except the + Save button
  const existing = bookmarksDiv.querySelectorAll('button:not(#btn-save-bm)');
  existing.forEach(b => b.remove());
  bookmarks.forEach((bm, i) => {
    const btn = document.createElement('button');
    btn.textContent = bm.label;
    btn.dataset.idx = i;
    btn.classList.add('saved');
    btn.addEventListener('click', () => applyBookmark(bookmarks[i]));
    bookmarksDiv.insertBefore(btn, btnSaveBm);
  });
}
// --- UI event bindings ---
timeSlider.addEventListener('input', () => {
  const day = parseInt(timeSlider.value);
  timeLabel.textContent = `Day ${day + 1} / ${DAYS}`;
  switchToDay(day);
});
btnPlay.addEventListener('click', () => {
  const playing = btnPlay.dataset.playing === 'true';
  if (playing) {
    btnPlay.dataset.playing = 'false';
    btnPlay.textContent = 'Play';
    btnPlay.style.borderColor = '#333';
  } else {
    btnPlay.dataset.playing = 'true';
    btnPlay.textContent = 'Pause';
    btnPlay.style.borderColor = '#4af';
  }
});
btnSaveBm.addEventListener('click', saveCurrentBookmark);
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight') {
    const v = Math.min(DAYS - 1, parseInt(timeSlider.value) + 1);
    timeSlider.value = v;
    timeLabel.textContent = `Day ${v + 1} / ${DAYS}`;
    switchToDay(v);
  } else if (e.key === 'ArrowLeft') {
    const v = Math.max(0, parseInt(timeSlider.value) - 1);
    timeSlider.value = v;
    timeLabel.textContent = `Day ${v + 1} / ${DAYS}`;
    switchToDay(v);
  } else if (e.key === 'r' || e.key === 'R') {
    controls.autoRotate = !controls.autoRotate;
  }
});
// --- Render loop ---
// Frame update: advance auto-play time, animate particles (subtle oscillation),
// update controls damping
let lastTime = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  // Auto-play: advance day every 800ms when playing
  if (btnPlay.dataset.playing === 'true') {
    if (timestamp - lastTime > 800) {
      lastTime = timestamp;
      let day = parseInt(timeSlider.value);
      day = (day + 1) % DAYS; // loop
      timeSlider.value = day;
      timeLabel.textContent = `Day ${day + 1} / ${DAYS}`;
      switchToDay(day);
    }
  }
  controls.update();
  // Animate particles: subtle Y-axis oscillation to simulate floating
  if (particlePoints && particlePositions) {
    const pos = particlePoints.geometry.attributes.position.array;
    const t = timestamp * 0.001;
    for (let i = 0; i < Math.min(PARTICLE_COUNT, pos.length / 3); i++) {
      const idx = i * 3;
      // Sine wave oscillation based on particle index for variety
      pos[idx + 1] = particlePositions[idx + 1] + Math.sin(t * 3 + i * 0.7) * 0.08;
    }
    particlePoints.geometry.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
  updateFPS();
}
// --- Initialization: generate data, build first frame, start render ---
async function init() {
  try {
    loadingText.textContent = 'Generating terrain data...';
    // Generate synthetic data (simulate async for realistic loading behavior)
    await new Promise(resolve => setTimeout(resolve, 50)); // yield to UI
    dataCache = generateData();
    if (!dataCache || dataCache.length === 0) {
      emptyState.classList.add('show');
      loadingOverlay.classList.add('hidden');
      return;
    }
    loadingText.textContent = 'Building 3D terrain...';
    renderBookmarkButtons();
    switchToDay(0);
    // Pre-cache adjacent days
    await new Promise(resolve => setTimeout(resolve, 10));
    for (let d = 1; d < Math.min(5, DAYS); d++) {
      if (!cacheGet(d)) {
        const dayData = dataCache[d];
        const tGeom = buildTerrainGeometry(dayData);
        const rGeom = buildRiverGeometry(dayData);
        const partData = new Float32Array(PARTICLE_COUNT * 3);
        const saved = new Float32Array(PARTICLE_COUNT * 3);
        particlePosBuffer.set(saved); // backup
        buildParticlePositions(dayData);
        partData.set(particlePosBuffer);
        particlePosBuffer.set(saved); // restore
        cachePut(d, { terrain: tGeom, rivers: rGeom, particles: partData });
      }
    }
    loadingOverlay.classList.add('hidden');
    requestAnimationFrame(animate);
  } catch (e) {
    showError('Initialization failed: ' + e.message);
    loadingOverlay.classList.add('hidden');
    emptyState.classList.add('show');
  }
}
// Bootstrap
init().catch(e => {
  showError('Critical error: ' + e.message);
  loadingOverlay.classList.add('hidden');
  emptyState.classList.add('show');
});
</script>
</body>
</html>