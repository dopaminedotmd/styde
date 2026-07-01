<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { overflow: hidden; background: #0a0a0f; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8ccd4; }
  #container { position: fixed; inset: 0; z-index: 1; }
  #hud { position: fixed; z-index: 10; pointer-events: none; }
  #hud > * { pointer-events: auto; }
  #time-panel {
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: rgba(10,10,20,0.85); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 12px;
    padding: 12px 20px; display: flex; align-items: center; gap: 14px;
    z-index: 10; min-width: 380px;
  }
  #time-slider { flex: 1; accent-color: #6ee7b7; height: 6px; cursor: pointer; }
  #time-label { font-variant-numeric: tabular-nums; min-width: 60px; text-align: center; font-size: 13px; color: #a0aab4; }
  #bookmarks {
    position: fixed; top: 20px; right: 20px;
    background: rgba(10,10,20,0.85); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
    padding: 10px; z-index: 10; display: flex; flex-direction: column; gap: 6px;
  }
  #bookmarks button {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
    color: #c8ccd4; padding: 6px 12px; border-radius: 6px; cursor: pointer;
    font-size: 12px; transition: background 0.15s;
  }
  #bookmarks button:hover { background: rgba(255,255,255,0.14); }
  #bookmarks button.active { border-color: #6ee7b7; color: #6ee7b7; }
  #diagnostics {
    position: fixed; top: 20px; left: 20px;
    background: rgba(10,10,20,0.85); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
    padding: 12px 16px; z-index: 10; font-size: 11px; line-height: 1.6;
    font-variant-numeric: tabular-nums; min-width: 200px;
  }
  #diagnostics .label { color: #7a8490; }
  #diagnostics .value { color: #c8ccd4; }
  #diagnostics .hit { color: #6ee7b7; }
  #diagnostics .miss { color: #f87171; }
  #tooltip {
    position: fixed; pointer-events: none; z-index: 20;
    background: rgba(10,10,20,0.9); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px; padding: 8px 12px; font-size: 11px; line-height: 1.5;
    display: none; white-space: nowrap;
  }
  #legend {
    position: fixed; bottom: 100px; left: 20px;
    background: rgba(10,10,20,0.85); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
    padding: 12px 14px; z-index: 10; font-size: 10px; line-height: 1.7;
  }
  .legend-swatch { display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 6px; vertical-align: middle; }
</style>
</head>
<body>
<div id="container"></div>
<div id="diagnostics">
  <div><span class="label">FPS </span><span class="value" id="d-fps">0</span></div>
  <div><span class="label">Vertices </span><span class="value" id="d-verts">0</span></div>
  <div><span class="label">Terrain cache </span><span class="hit" id="d-t-hit">0</span><span class="label">/</span><span class="miss" id="d-t-miss">0</span></div>
  <div><span class="label">River cache </span><span class="hit" id="d-r-hit">0</span><span class="label">/</span><span class="miss" id="d-r-miss">0</span></div>
  <div><span class="label">Grid xform cache </span><span class="hit" id="d-g-hit">0</span><span class="label">/</span><span class="miss" id="d-g-miss">0</span></div>
  <div><span class="label">Particle allocs </span><span class="value" id="d-p-alloc">0</span></div>
</div>
<div id="bookmarks">
  <button data-bm="0">Default Overview</button>
  <button data-bm="1">Top-Down</button>
  <button data-bm="2">Valley Closeup</button>
  <button data-bm="3" id="bm-save">Save Current</button>
</div>
<div id="legend">
  <div><span class="legend-swatch" style="background:#3b3b2a;"></span> Low density</div>
  <div><span class="legend-swatch" style="background:#7a9a3a;"></span> Medium density</div>
  <div><span class="legend-swatch" style="background:#2d5a1e;"></span> High density</div>
  <div><span class="legend-swatch" style="background:#e85d5d;"></span> Error river</div>
  <div style="margin-top:4px;color:#7a8490;">Elevation = Revenue</div>
</div>
<div id="time-panel">
  <span style="font-size:12px;color:#7a8490;">Time</span>
  <input type="range" id="time-slider" min="0" max="11" value="6" step="1">
  <span id="time-label">12:00</span>
  <button id="btn-auto-rotate" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);color:#c8ccd4;padding:4px 10px;border-radius:6px;cursor:pointer;font-size:11px;">Auto: OFF</button>
</div>
<div id="tooltip"></div>
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
/* ---- CONFIG ---- */
const GRID = 64;
const TIME_SLICES = 12;
const TERRAIN_SIZE = 40;
const MAX_HEIGHT = 8;
const PARTICLE_COUNT = 300;
/* ---- STATE ---- */
let currentTime = 6;
let autoRotate = false;
let frameCount = 0;
let lastFpsTime = performance.now();
let fps = 0;
/* ---- CACHE ---- */
const terrainCache = new Map();
const riverCache = new Map();
const gridXformCache = new Map();
const GRID_XFORM_CACHE_MAX = 64;
let cacheStats = { tHit: 0, tMiss: 0, rHit: 0, rMiss: 0, gHit: 0, gMiss: 0, pAlloc: 0 };
/* ---- THREE.JS SETUP ---- */
const container = document.getElementById('container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#1a1a2e');
scene.fog = new THREE.Fog('#1a1a2e', 30, 90);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 200);
camera.position.set(28, 22, 32);
camera.lookAt(0, 2, 0);
/* ---- LIGHTS ---- */
const ambient = new THREE.AmbientLight('#4466aa', 0.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffeedd', 3.5);
sun.position.set(25, 30, 15);
scene.add(sun);
const fill = new THREE.DirectionalLight('#8899cc', 0.6);
fill.position.set(-15, 5, -10);
scene.add(fill);
/* ---- CONTROLS ---- */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 2, 0);
controls.minDistance = 8;
controls.maxDistance = 70;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
/* ---- BOOKMARKS ---- */
const bookmarks = [
  { pos: [28, 22, 32], target: [0, 2, 0] },
  { pos: [0, 35, 1], target: [0, 2, 0] },
  { pos: [-8, 6, -14], target: [-4, 1.5, -10] },
  null,
];
function saveBookmark() {
  bookmarks[3] = {
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
  };
  document.querySelector('[data-bm="3"]').textContent = 'Saved ✓';
  setTimeout(() => { document.querySelector('[data-bm="3"]').textContent = 'Save Current'; }, 1500);
}
function loadBookmark(idx) {
  const bm = bookmarks[idx];
  if (!bm) { saveBookmark(); return; }
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTgt = controls.target.clone();
  const endTgt = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function anim(now) {
    const t = Math.min((now - startTime) / duration, 1.0);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTgt, endTgt, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
  document.querySelectorAll('#bookmarks button').forEach(b => b.classList.remove('active'));
  document.querySelector(`[data-bm="${idx}"]`)?.classList.add('active');
}
document.querySelectorAll('#bookmarks button[data-bm]').forEach(btn => {
  btn.addEventListener('click', () => loadBookmark(parseInt(btn.dataset.bm)));
});
/* ---- DATA GENERATION ---- */
function spatialHash(x, y, seed) {
  const n = Math.sin(x * 127.1 + y * 311.7 + seed) * 43758.5453;
  return n - Math.floor(n);
}
function smoothNoise(x, y, seed) {
  const ix = Math.floor(x); const iy = Math.floor(y);
  const fx = x - ix; const fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx);
  const sy = fy * fy * (3 - 2 * fy);
  const n00 = spatialHash(ix, iy, seed);
  const n10 = spatialHash(ix + 1, iy, seed);
  const n01 = spatialHash(ix, iy + 1, seed);
  const n11 = spatialHash(ix + 1, iy + 1, seed);
  return n00 * (1 - sx) * (1 - sy) + n10 * sx * (1 - sy) + n01 * (1 - sx) * sy + n11 * sx * sy;
}
function fbm(x, y, seed, octaves = 4) {
  let val = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    val += smoothNoise(x * freq, y * freq, seed + i * 100) * amp;
    max += amp;
    amp *= 0.5;
    freq *= 2.0;
  }
  return val / max;
}
function timeFactor(hour) {
  const h = hour / TIME_SLICES * 24;
  const morning = Math.exp(-((h - 8) ** 2) / 18);
  const afternoon = Math.exp(-((h - 14) ** 2) / 28);
  const evening = Math.exp(-((h - 19) ** 2) / 22) * 0.7;
  return Math.max(0.08, morning * 0.9 + afternoon * 1.0 + evening * 0.55);
}
function generateTimeSlice(t) {
  const heights = new Float32Array(GRID * GRID);
  const densities = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  const apiCalls = new Float32Array(GRID * GRID);
  const tf = timeFactor(t);
  const half = GRID / 2;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const nx = (ix - half) / half;
      const ny = (iy - half) / half;
      const base = fbm(nx * 3, ny * 3, 42) * 0.6 + 0.4;
      const ridge = 1 - Math.abs(fbm(nx * 2.1 + 1, ny * 2.1 + 1, 77) * 2 - 1);
      const revenue = (base * 0.7 + ridge * 0.3) * tf * MAX_HEIGHT;
      heights[idx] = Math.max(0.1, revenue);
      const densBase = fbm(nx * 2.5, ny * 2.5, 133) * 0.5 + 0.5;
      densities[idx] = densBase * tf;
      const errBase = fbm(nx * 4.1, ny * 4.1, 201) * 0.5 + 0.5;
      const errBoost = tf > 0.6 ? (tf - 0.6) * 1.5 : 0;
      errors[idx] = Math.min(1, errBase * 0.3 + errBoost);
      apiCalls[idx] = densBase * tf * (80 + fbm(nx * 3.3, ny * 3.3, 311) * 200);
    }
  }
  return { heights, densities, errors, apiCalls };
}
/* ---- PRE-BUILD ALL TIME SLICES ---- */
const allSlices = [];
for (let t = 0; t < TIME_SLICES; t++) {
  allSlices.push(generateTimeSlice(t));
}
/* ---- COLOR LOOKUP ---- */
function densityColor(d) {
  const stops = [
    [0.00, [0.18, 0.20, 0.12]],
    [0.20, [0.28, 0.32, 0.15]],
    [0.40, [0.42, 0.52, 0.18]],
    [0.60, [0.38, 0.58, 0.14]],
    [0.80, [0.22, 0.42, 0.09]],
    [1.00, [0.10, 0.28, 0.05]],
  ];
  let lo = stops[0], hi = stops[stops.length - 1];
  for (let i = 0; i < stops.length - 1; i++) {
    if (d >= stops[i][0] && d <= stops[i + 1][0]) { lo = stops[i]; hi = stops[i + 1]; break; }
  }
  const range = hi[0] - lo[0];
  const t = range < 0.001 ? 0 : (d - lo[0]) / range;
  return [
    lo[1][0] + (hi[1][0] - lo[1][0]) * t,
    lo[1][1] + (hi[1][1] - lo[1][1]) * t,
    lo[1][2] + (hi[1][2] - lo[1][2]) * t,
  ];
}
/* ---- BUILD TERRAIN GEOMETRY ---- */
function buildTerrainGeometry(slice) {
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const indices = [];
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (GRID - 1);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const pi = idx * 3;
      positions[pi] = ix * step - half;
      positions[pi + 1] = slice.heights[idx];
      positions[pi + 2] = iy * step - half;
      const col = densityColor(slice.densities[idx]);
      colors[pi] = col[0];
      colors[pi + 1] = col[1];
      colors[pi + 2] = col[2];
    }
  }
  for (let iy = 0; iy < GRID - 1; iy++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iy * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
/* ---- BUILD RIVER GEOMETRY ---- */
function buildRiverGeometry(slice) {
  const threshold = 0.42;
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (GRID - 1);
  const visited = new Uint8Array(GRID * GRID);
  const riverPaths = [];
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      if (visited[idx] || slice.errors[idx] < threshold) continue;
      const path = [];
      const stack = [[ix, iy]];
      while (stack.length > 0) {
        const [cx, cy] = stack.pop();
        const ci = cy * GRID + cx;
        if (cx < 0 || cx >= GRID || cy < 0 || cy >= GRID || visited[ci]) continue;
        if (slice.errors[ci] < threshold * 0.7) continue;
        visited[ci] = 1;
        path.push([cx, cy]);
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          stack.push([cx + dx, cy + dy]);
        }
      }
      if (path.length > 6) riverPaths.push(path);
    }
  }
  const group = new THREE.Group();
  for (const path of riverPaths) {
    if (path.length < 4) continue;
    const points = path.map(([ix, iy]) => {
      const idx = iy * GRID + ix;
      return new THREE.Vector3(
        ix * step - half,
        slice.heights[idx] + 0.15,
        iy * step - half,
      );
    });
    const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, Math.min(path.length * 2, 64), 0.18, 6, false);
    const mat = new THREE.MeshStandardMaterial({
      color: '#e85d5d',
      roughness: 0.35,
      metalness: 0.1,
      emissive: '#330000',
      emissiveIntensity: 0.3,
    });
    group.add(new THREE.Mesh(tubeGeo, mat));
  }
  return group;
}
/* ---- BUILD ALL CACHED GEOMETRIES ---- */
const terrainMeshes = [];
for (let t = 0; t < TIME_SLICES; t++) {
  const geo = buildTerrainGeometry(allSlices[t]);
  terrainCache.set(t, geo);
}
/* ---- TERRAIN MESH ---- */
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.75,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(terrainCache.get(currentTime), terrainMat);
scene.add(terrainMesh);
/* ---- RIVER GROUP ---- */
const riverGroup = new THREE.Group();
scene.add(riverGroup);
function swapRiver(timeIdx) {
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    if (child.material) child.material.dispose();
    riverGroup.remove(child);
  }
  if (riverCache.has(timeIdx)) {
    cacheStats.rHit++;
    const cached = riverCache.get(timeIdx);
    cached.children.forEach(c => riverGroup.add(c.clone()));
  } else {
    cacheStats.rMiss++;
    const built = buildRiverGeometry(allSlices[timeIdx]);
    riverCache.set(timeIdx, built);
    built.children.forEach(c => riverGroup.add(c.clone()));
  }
}
swapRiver(currentTime);
/* ---- PARTICLES ---- */
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = new Array(PARTICLE_COUNT);
function spawnParticle(i) {
  const slice = allSlices[currentTime];
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (GRID - 1);
  const ix = Math.floor(Math.random() * GRID);
  const iy = Math.floor(Math.random() * GRID);
  const idx = iy * GRID + ix;
  const px = ix * step - half;
  const pz = iy * step - half;
  const py = slice.heights[idx] + 0.4;
  particlePositions[i * 3] = px;
  particlePositions[i * 3 + 1] = py;
  particlePositions[i * 3 + 2] = pz;
  const angle = Math.random() * Math.PI * 2;
  const speed = 0.02 + Math.random() * 0.06;
  particleData[i] = {
    dirX: Math.cos(angle) * speed,
    dirZ: Math.sin(angle) * speed,
    life: 1,
    decay: 0.0003 + Math.random() * 0.001,
    ix, iy,
  };
  particleColors[i * 3] = 1;
  particleColors[i * 3 + 1] = 0.9;
  particleColors[i * 3 + 2] = 0.55;
}
for (let i = 0; i < PARTICLE_COUNT; i++) spawnParticle(i);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.18,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.7,
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
/* ---- GROUND GRID ---- */
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2 + 2, 40, 20, 64, '#334455', '#223344');
gridHelper.position.y = -0.05;
scene.add(gridHelper);
/* ---- ANIMATION LOOP ---- */
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    fps = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = timestamp;
  }
  const slice = allSlices[currentTime];
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (GRID - 1);
  const posArr = particleGeo.attributes.position.array;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    let px = posArr[pi];
    let pz = posArr[pi + 2];
    const pd = particleData[i];
    px += pd.dirX;
    pz += pd.dirZ;
    if (px < -half || px > half || pz < -half || pz > half) {
      spawnParticle(i);
      cacheStats.pAlloc++;
      continue;
    }
    const gx = Math.round((px + half) / step);
    const gy = Math.round((pz + half) / step);
    const clampedX = Math.max(0, Math.min(GRID - 1, gx));
    const clampedY = Math.max(0, Math.min(GRID - 1, gy));
    const height = slice.heights[clampedY * GRID + clampedX];
    posArr[pi] = px;
    posArr[pi + 1] = height + 0.5;
    posArr[pi + 2] = pz;
    pd.life -= pd.decay;
    particleColors[pi] = 1;
    particleColors[pi + 1] = 0.7 + pd.life * 0.3;
    particleColors[pi + 2] = 0.3 + pd.life * 0.4;
    if (pd.life <= 0) {
      spawnParticle(i);
      cacheStats.pAlloc++;
    }
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  updateDiagnostics();
  renderer.render(scene, camera);
}
/* ---- DIAGNOSTICS ---- */
function updateDiagnostics() {
  document.getElementById('d-fps').textContent = fps;
  document.getElementById('d-verts').textContent = (GRID * GRID).toLocaleString();
  document.getElementById('d-t-hit').textContent = cacheStats.tHit;
  document.getElementById('d-t-miss').textContent = cacheStats.tMiss;
  document.getElementById('d-r-hit').textContent = cacheStats.rHit;
  document.getElementById('d-r-miss').textContent = cacheStats.rMiss;
  document.getElementById('d-g-hit').textContent = cacheStats.gHit;
  document.getElementById('d-g-miss').textContent = cacheStats.gMiss;
  document.getElementById('d-p-alloc').textContent = cacheStats.pAlloc;
}
/* ---- TIME SLIDER ---- */
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
function formatTime(t) {
  const hour = Math.round(t / TIME_SLICES * 24);
  return `${String(hour).padStart(2, '0')}:00`;
}
slider.addEventListener('input', () => {
  const newTime = parseInt(slider.value);
  if (newTime === currentTime) return;
  currentTime = newTime;
  timeLabel.textContent = formatTime(currentTime);
  if (terrainCache.has(currentTime)) {
    cacheStats.tHit++;
    terrainMesh.geometry = terrainCache.get(currentTime);
  } else {
    cacheStats.tMiss++;
    const geo = buildTerrainGeometry(allSlices[currentTime]);
    terrainCache.set(currentTime, geo);
    terrainMesh.geometry = geo;
  }
  swapRiver(currentTime);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    spawnParticle(i);
    cacheStats.pAlloc++;
  }
});
/* ---- AUTO ROTATE ---- */
const btnAuto = document.getElementById('btn-auto-rotate');
btnAuto.addEventListener('click', () => {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  btnAuto.textContent = `Auto: ${autoRotate ? 'ON' : 'OFF'}`;
  btnAuto.style.borderColor = autoRotate ? '#6ee7b7' : 'rgba(255,255,255,0.1)';
  btnAuto.style.color = autoRotate ? '#6ee7b7' : '#c8ccd4';
});
/* ---- TOOLTIP / HOVER ---- */
const tooltip = document.getElementById('tooltip');
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let lastGridQuery = null;
let gridQueryCacheTime = 0;
renderer.domElement.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const half = TERRAIN_SIZE / 2;
    const step = TERRAIN_SIZE / (GRID - 1);
    const gx = Math.round((pt.x + half) / step);
    const gy = Math.round((pt.z + half) / step);
    const cacheKey = `${gx},${gy}`;
    const now = performance.now();
    if (lastGridQuery && lastGridQuery.key === cacheKey && now - gridQueryCacheTime < 200) {
      cacheStats.gHit++;
    } else {
      cacheStats.gMiss++;
      if (gridXformCache.size >= GRID_XFORM_CACHE_MAX) {
        const firstKey = gridXformCache.keys().next().value;
        gridXformCache.delete(firstKey);
      }
      gridXformCache.set(cacheKey, { gx, gy, ts: now });
      lastGridQuery = { key: cacheKey };
      gridQueryCacheTime = now;
    }
    if (gx >= 0 && gx < GRID && gy >= 0 && gy < GRID) {
      const idx = gy * GRID + gx;
      const slice = allSlices[currentTime];
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 16) + 'px';
      tooltip.style.top = (e.clientY - 10) + 'px';
      tooltip.innerHTML =
        `Grid (${gx},${gy})<br>` +
        `Revenue: ${slice.heights[idx].toFixed(2)}m<br>` +
        `Density: ${(slice.densities[idx] * 100).toFixed(0)}%<br>` +
        `Errors: ${(slice.errors[idx] * 100).toFixed(1)}%<br>` +
        `API calls: ${slice.apiCalls[idx].toFixed(0)}/s`;
    }
  } else {
    tooltip.style.display = 'none';
  }
});
/* ---- RESIZE ---- */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ---- START ---- */
timeLabel.textContent = formatTime(currentTime);
slider.value = currentTime;
updateDiagnostics();
requestAnimationFrame(animate);
</script>
</body>
</html>