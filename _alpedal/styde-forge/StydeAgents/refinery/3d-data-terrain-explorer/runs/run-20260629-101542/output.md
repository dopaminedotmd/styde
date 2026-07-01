<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0a0f; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8ccd4; }
canvas { display: block; }
#ui { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; }
#ui > * { pointer-events: auto; }
#time-panel { position: absolute; bottom: 28px; left: 50%; transform: translateX(-50%); background: rgba(10,10,20,0.85); border: 1px solid #2a2a40; border-radius: 10px; padding: 12px 20px; display: flex; align-items: center; gap: 16px; backdrop-filter: blur(10px); }
#time-slider { width: 320px; accent-color: #5b9bd5; height: 6px; border-radius: 3px; cursor: pointer; }
#time-label { font-size: 13px; color: #8899aa; min-width: 90px; text-align: center; font-variant-numeric: tabular-nums; }
#btn-play { background: none; border: 1px solid #3a3a55; color: #aabbcc; border-radius: 6px; padding: 5px 12px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
#btn-play:hover { background: #2a2a40; border-color: #5b9bd5; }
#btn-play.playing { background: #5b9bd5; color: #fff; border-color: #5b9bd5; }
#bookmarks-panel { position: absolute; top: 20px; right: 20px; background: rgba(10,10,20,0.85); border: 1px solid #2a2a40; border-radius: 10px; padding: 12px 16px; backdrop-filter: blur(10px); max-height: 60vh; overflow-y: auto; min-width: 180px; }
#bookmarks-panel h3 { font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; color: #667788; margin-bottom: 10px; }
.bookmark-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 8px; margin: 2px 0; border-radius: 5px; cursor: pointer; font-size: 12px; transition: background 0.15s; }
.bookmark-row:hover { background: #1a1a30; }
.bookmark-row .del { color: #664444; margin-left: 10px; padding: 0 4px; border-radius: 3px; }
.bookmark-row .del:hover { color: #cc4444; background: #331111; }
#diag-panel { position: absolute; top: 20px; left: 20px; background: rgba(10,10,20,0.85); border: 1px solid #2a2a40; border-radius: 10px; padding: 10px 14px; backdrop-filter: blur(10px); font-size: 11px; font-family: 'SF Mono', 'Cascadia Code', monospace; line-height: 1.6; }
.diag-label { color: #556677; }
.diag-hit { color: #4caf84; }
.diag-miss { color: #cc7744; }
.diag-neutral { color: #8899aa; }
#legend { position: absolute; bottom: 90px; left: 20px; background: rgba(10,10,20,0.75); border: 1px solid #2a2a40; border-radius: 8px; padding: 8px 12px; font-size: 10px; backdrop-filter: blur(6px); }
.legend-row { display: flex; align-items: center; gap: 8px; margin: 3px 0; }
.legend-swatch { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
#tooltip { position: fixed; pointer-events: none; background: rgba(5,5,15,0.9); border: 1px solid #3a3a55; border-radius: 6px; padding: 6px 10px; font-size: 11px; display: none; z-index: 20; white-space: nowrap; }
</style>
</head>
<body>
<div id="ui">
  <div id="diag-panel">
    <div>Terrain cache: <span id="diag-terrain-hit" class="diag-hit">0</span>/<span id="diag-terrain-miss" class="diag-miss">0</span></div>
    <div>River cache:  <span id="diag-river-hit" class="diag-hit">0</span>/<span id="diag-river-miss" class="diag-miss">0</span></div>
    <div>FPS: <span id="diag-fps" class="diag-neutral">--</span></div>
  </div>
  <div id="bookmarks-panel">
    <h3>Camera Bookmarks</h3>
    <div id="bookmarks-list"></div>
    <button id="btn-add-bookmark" style="margin-top:8px;width:100%;background:rgba(90,150,210,0.2);border:1px solid #3a5580;color:#aaccee;border-radius:5px;padding:5px;cursor:pointer;font-size:11px;">+ Save View</button>
  </div>
  <div id="legend">
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to top,#1a3a1a,#4caf50,#8fde8f);"></span> Elevation (Revenue)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#cc4444;"></span> Error River</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#ffcc44;"></span> API Trail</div>
  </div>
  <div id="time-panel">
    <button id="btn-play">▶</button>
    <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
    <span id="time-label">Day 0</span>
  </div>
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
// ─── Constants ─────────────────────────────────────────────────
const GRID = 50;
const TERRAIN_SIZE = 40;
const MAX_ELEVATION = 8;
const FRAMES = 30;
const RIVER_COLOR = 0xcc3333;
const PARTICLE_COLOR = 0xffcc44;
const DEBOUNCE_RIVER_MS = 200;
const FPS_WINDOW = 60;
// ─── DOM refs ──────────────────────────────────────────────────
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const btnPlay = document.getElementById('btn-play');
const tooltip = document.getElementById('tooltip');
const bookmarksList = document.getElementById('bookmarks-list');
const btnAddBookmark = document.getElementById('btn-add-bookmark');
const diagTerrainHit = document.getElementById('diag-terrain-hit');
const diagTerrainMiss = document.getElementById('diag-terrain-miss');
const diagRiverHit = document.getElementById('diag-river-hit');
const diagRiverMiss = document.getElementById('diag-river-miss');
const diagFps = document.getElementById('diag-fps');
// ─── Scene setup ───────────────────────────────────────────────
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 30, 80);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 120);
camera.position.set(22, 18, 28);
camera.lookAt(0, 2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 2, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 8;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.55;
controls.update();
// ─── Lighting ──────────────────────────────────────────────────
const ambient = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
sun.position.set(30, 25, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 100;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
sun.shadow.bias = -0.0003;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x6688cc, 0.8);
fill.position.set(-10, 3, -10);
scene.add(fill);
// ─── Ground grid ───────────────────────────────────────────────
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2, 32, 20, 64, 0x222244, 0x222244);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
// ─── Synthetic data generation ─────────────────────────────────
// Each frame: grid of [elevation(revenue), userDensity, errorCount, apiCallCount]
function generateData() {
  const frames = [];
  // Seedable pseudo-noise for reproducibility
  function noise(x, z, t) {
    const n = Math.sin(x * 1.37 + z * 0.91 + t * 0.47) * Math.cos(x * 0.73 - z * 1.13 + t * 0.31) +
              Math.sin(x * 2.11 - z * 1.57 + t * 0.23) * 0.5 +
              Math.cos((x + z) * 0.89 + t * 0.67) * 0.3;
    return (n + 1.0) / 3.0; // normalize to ~0..1
  }
  for (let t = 0; t < FRAMES; t++) {
    const grid = [];
    // Trend component: revenue grows over time with seasonal dip mid-month
    const trend = 1.0 + 0.4 * Math.sin(t / FRAMES * Math.PI * 2);
    for (let iz = 0; iz < GRID; iz++) {
      const row = [];
      for (let ix = 0; ix < GRID; ix++) {
        const fx = (ix - GRID / 2) / (GRID / 2); // -1..1
        const fz = (iz - GRID / 2) / (GRID / 2);
        // Central peak with time-varying amplitude
        const dist = Math.sqrt(fx * fx + fz * fz);
        const hill = Math.max(0, 1.0 - dist * 1.3) * (1.5 + noise(fx * 2, fz * 2, t * 0.3) * 0.6);
        const revenue = hill * trend * MAX_ELEVATION;
        // User density: correlated with revenue but shifted
        const users = Math.max(0, 0.1 + hill * trend * 0.8 + noise(fx * 1.7, fz * 1.7, t * 0.4 + 5) * 0.3);
        // Error count: spikes where revenue is volatile (derivative zones)
        const errBase = noise(fx * 3.1, fz * 3.1, t * 0.9) * 0.5;
        const errSensitivity = Math.abs(noise(fx * 1.5, fz * 1.5, t * 0.35) - noise(fx * 1.5, fz * 1.5, (t + 0.1) * 0.35)) * 4;
        const errors = Math.min(1, Math.max(0, errBase * 0.6 + errSensitivity * 0.4));
        // API calls: flow along valleys (low elevation, high user density)
        const api = Math.max(0, (users * 2.5 - revenue * 0.08) * (0.5 + noise(fx * 2.5, fz * 2.5, t * 0.55) * 0.5));
        row.push({ revenue, users, errors, api });
      }
      grid.push(row);
    }
    frames.push(grid);
  }
  return frames;
}
const timeSeriesData = generateData();
// ─── Caches ────────────────────────────────────────────────────
const terrainCache = new Map();  // frameIndex -> { geometry, colorAttr }
const riverCache = new Map();    // frameIndex -> THREE.BufferGeometry
let terrainHits = 0, terrainMisses = 0;
let riverHits = 0, riverMisses = 0;
// ─── Terrain mesh (reusable, swapped on frame change) ──────────
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(new THREE.BufferGeometry(), terrainMaterial);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Build terrain geometry for a given frame index
function buildTerrainGeometry(frameIndex) {
  // Clamp frame index to valid range (edge-case guard)
  const idx = Math.max(0, Math.min(FRAMES - 1, Math.floor(frameIndex)));
  if (terrainCache.has(idx)) {
    terrainHits++;
    return terrainCache.get(idx);
  }
  terrainMisses++;
  const grid = timeSeriesData[idx];
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (GRID - 1);
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iz * GRID + ix;
      const cell = grid[iz][ix];
      const x = ix * step - half;
      const z = iz * step - half;
      const y = cell.revenue;
      // Out-of-bounds clamping for elevation (edge-case guard)
      const yClamped = Math.max(0, Math.min(MAX_ELEVATION * 1.5, y));
      positions[i * 3] = x;
      positions[i * 3 + 1] = yClamped;
      positions[i * 3 + 2] = z;
      // Vegetation gradient: low=dark green, high=bright green mixed with elevation gold
      const u = cell.users; // 0..~1
      const r = 0.05 + u * 0.15 + (yClamped / MAX_ELEVATION) * 0.25;
      const g = 0.12 + u * 0.75;
      const b = 0.06 + u * 0.1;
      colors[i * 3] = Math.min(1, r);
      colors[i * 3 + 1] = Math.min(1, g);
      colors[i * 3 + 2] = Math.min(1, b);
    }
  }
  // Build indices
  const indices = [];
  for (let iz = 0; iz < GRID - 1; iz++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iz * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  const cached = { geometry: geom, colorAttr: colors };
  terrainCache.set(idx, cached);
  return cached;
}
// Apply terrain for current frame (swaps geometry reference)
let currentTerrainFrame = -1;
function applyTerrain(frameIndex) {
  const idx = Math.max(0, Math.min(FRAMES - 1, Math.floor(frameIndex)));
  if (idx === currentTerrainFrame) return; // debounce identical frame
  currentTerrainFrame = idx;
  const cached = buildTerrainGeometry(idx);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = cached.geometry;
}
// ─── River geometry ────────────────────────────────────────────
const riverMaterial = new THREE.MeshBasicMaterial({ color: RIVER_COLOR, transparent: true, opacity: 0.7, side: THREE.DoubleSide });
let riverMesh = null;
let riverDebounceTimer = null;
let pendingRiverFrame = -1;
function buildRiverGeometry(frameIndex) {
  const idx = Math.max(0, Math.min(FRAMES - 1, Math.floor(frameIndex)));
  if (riverCache.has(idx)) {
    riverHits++;
    return riverCache.get(idx);
  }
  riverMisses++;
  const grid = timeSeriesData[idx];
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (GRID - 1);
  // Find error hotspots as river control points
  const hotspots = [];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      if (grid[iz][ix].errors > 0.45) {
        const x = ix * step - half;
        const z = iz * step - half;
        const y = grid[iz][ix].revenue + 0.15; // float slightly above terrain
        hotspots.push(new THREE.Vector3(x, y, z));
      }
    }
  }
  // If no hotspots, create a minimal degenerate geometry (edge-case guard)
  if (hotspots.length < 2) {
    const emptyGeom = new THREE.BufferGeometry();
    emptyGeom.setAttribute('position', new THREE.BufferAttribute(new Float32Array([0, 0, 0, 0, 0, 0]), 3));
    riverCache.set(idx, emptyGeom);
    return emptyGeom;
  }
  // Sort hotspots into a path: greedy nearest-neighbor chain
  // Prefer globally-optimal: sort by x then z for a consistent sweep
  hotspots.sort((a, b) => a.x !== b.x ? a.x - b.x : a.z - b.z);
  // Build CatmullRom curve through hotspots
  const curve = new THREE.CatmullRomCurve3(hotspots, false, 'catmullrom', 0.5);
  const tubularSegments = Math.min(200, hotspots.length * 4);
  const tubeRadius = 0.12;
  const tubeGeom = new THREE.TubeGeometry(curve, tubularSegments, tubeRadius, 6, false);
  riverCache.set(idx, tubeGeom);
  return tubeGeom;
}
function applyRiver(frameIndex) {
  // Debounce: don't rebuild on every tick during rapid slider scrubbing
  const idx = Math.max(0, Math.min(FRAMES - 1, Math.floor(frameIndex)));
  pendingRiverFrame = idx;
  if (riverDebounceTimer) return; // already waiting
  riverDebounceTimer = setTimeout(() => {
    riverDebounceTimer = null;
    const geom = buildRiverGeometry(pendingRiverFrame);
    if (riverMesh) {
      riverMesh.geometry.dispose();
      riverMesh.geometry = geom;
    }
  }, DEBOUNCE_RIVER_MS);
}
function createRiverMesh() {
  if (riverMesh) {
    riverMesh.geometry.dispose();
    scene.remove(riverMesh);
  }
  const geom = buildRiverGeometry(0);
  riverMesh = new THREE.Mesh(geom, riverMaterial);
  riverMesh.renderOrder = 1;
  riverMesh.material.depthTest = true;
  riverMesh.material.depthWrite = true;
  scene.add(riverMesh);
}
// ─── Particle system (API call trails) ─────────────────────────
const PARTICLE_COUNT = 800;
const particleGeom = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3); // reused, never reallocated
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = new Array(PARTICLE_COUNT); // per-particle state: {x, z, vx, vz, life, speed}
// Initialize particles
const halfTerrain = TERRAIN_SIZE / 2;
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleData[i] = {
    x: (Math.random() - 0.5) * TERRAIN_SIZE,
    z: (Math.random() - 0.5) * TERRAIN_SIZE,
    vx: (Math.random() - 0.5) * 0.8,
    vz: (Math.random() - 0.5) * 0.8,
    life: Math.random(),
    speed: 0.3 + Math.random() * 0.7,
  };
  particlePositions[i * 3] = particleData[i].x;
  particlePositions[i * 3 + 1] = 0;
  particlePositions[i * 3 + 2] = particleData[i].z;
  particleColors[i * 3] = 1.0;
  particleColors[i * 3 + 1] = 0.75 + Math.random() * 0.25;
  particleColors[i * 3 + 2] = 0.1 + Math.random() * 0.2;
}
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.15,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.7,
});
const particles = new THREE.Points(particleGeom, particleMat);
particles.renderOrder = 2;
scene.add(particles);
// Memoized world-to-grid coordinate transform for tooltip/hover path
const gridCoordCache = new Map(); // key: "ix,iz" -> {x, z} for current frame
let gridCoordCacheFrame = -1;
function getTerrainHeight(wx, wz, frameIndex) {
  const idx = Math.max(0, Math.min(FRAMES - 1, Math.floor(frameIndex)));
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (GRID - 1);
  // Clamp world coords to grid bounds
  const cx = Math.max(0, Math.min(GRID - 1, Math.round((wx + half) / step)));
  const cz = Math.max(0, Math.min(GRID - 1, Math.round((wz + half) / step)));
  // Build cache key
  if (gridCoordCacheFrame !== idx) {
    gridCoordCache.clear();
    gridCoordCacheFrame = idx;
  }
  const key = `${cx},${cz}`;
  if (gridCoordCache.has(key)) {
    return gridCoordCache.get(key);
  }
  const h = timeSeriesData[idx][cz][cx].revenue;
  gridCoordCache.set(key, h);
  return h;
}
// ─── Frame update (particles, time, rivers) ────────────────────
let currentFrame = 0;
let isPlaying = false;
let playInterval = null;
const fpsHistory = new Array(FPS_WINDOW).fill(0);
let fpsHistoryIndex = 0;
let lastFrameTime = performance.now();
function setFrame(idx) {
  const clamped = Math.max(0, Math.min(FRAMES - 1, Math.floor(idx)));
  if (clamped === currentFrame && terrainMesh.geometry.attributes.position.count > 0) return;
  currentFrame = clamped;
  slider.value = clamped;
  timeLabel.textContent = `Day ${clamped + 1}/${FRAMES}`;
  applyTerrain(clamped);
  applyRiver(clamped);
}
function updateParticles(dt) {
  const posArr = particleGeom.attributes.position.array;
  // Clamp dt to prevent tunneling on lag spikes (edge-case guard)
  const dtClamped = Math.min(0.1, dt);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const p = particleData[i];
    // Update position with wrapping
    p.x += p.vx * p.speed * dtClamped;
    p.z += p.vz * p.speed * dtClamped;
    // Wrap at terrain boundaries
    if (p.x > halfTerrain) p.x = -halfTerrain;
    if (p.x < -halfTerrain) p.x = halfTerrain;
    if (p.z > halfTerrain) p.z = -halfTerrain;
    if (p.z < -halfTerrain) p.z = halfTerrain;
    // Lift particle to terrain surface + small offset
    const h = getTerrainHeight(p.x, p.z, currentFrame);
    posArr[i * 3] = p.x;
    posArr[i * 3 + 1] = h + 0.2 + p.life * 0.6;
    posArr[i * 3 + 2] = p.z;
  }
  particleGeom.attributes.position.needsUpdate = true;
}
// ─── Camera bookmarks ──────────────────────────────────────────
const bookmarks = [];
function saveBookmark() {
  const bm = {
    name: `View ${bookmarks.length + 1}`,
    position: camera.position.clone(),
    target: controls.target.clone(),
  };
  bookmarks.push(bm);
  renderBookmarks();
}
function loadBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return; // edge-case guard
  const bm = bookmarks[index];
  // Smooth animate to bookmark position
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.position;
  const endTarget = bm.target;
  const startTime = performance.now();
  const duration = 800;
  function animateBookmark(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animateBookmark);
    }
  }
  requestAnimationFrame(animateBookmark);
}
function deleteBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return;
  bookmarks.splice(index, 1);
  renderBookmarks();
}
function renderBookmarks() {
  bookmarksList.innerHTML = bookmarks.map((bm, i) =>
    `<div class="bookmark-row" data-index="${i}">
      <span>${bm.name}</span>
      <span class="del" data-del="${i}">✕</span>
    </div>`
  ).join('');
  // Attach event listeners (using event delegation)
  bookmarksList.querySelectorAll('.bookmark-row').forEach(row => {
    row.addEventListener('click', (e) => {
      if (e.target.classList.contains('del')) {
        deleteBookmark(parseInt(e.target.dataset.del));
      } else {
        loadBookmark(parseInt(row.dataset.index));
      }
    });
  });
}
// ─── Event handlers ────────────────────────────────────────────
slider.addEventListener('input', () => {
  setFrame(parseInt(slider.value));
});
btnPlay.addEventListener('click', () => {
  isPlaying = !isPlaying;
  btnPlay.textContent = isPlaying ? '⏸' : '▶';
  btnPlay.classList.toggle('playing', isPlaying);
  if (isPlaying) {
    playInterval = setInterval(() => {
      const next = (currentFrame + 1) % FRAMES;
      setFrame(next);
    }, 400);
  } else {
    clearInterval(playInterval);
    playInterval = null;
  }
});
btnAddBookmark.addEventListener('click', saveBookmark);
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Double-click to save bookmark
renderer.domElement.addEventListener('dblclick', saveBookmark);
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'b': saveBookmark(); break;
    case ' ': e.preventDefault(); btnPlay.click(); break;
    case 'arrowleft': setFrame(currentFrame - 1); break;
    case 'arrowright': setFrame(currentFrame + 1); break;
    case 'r': controls.autoRotate = !controls.autoRotate; break;
    default: break;
  }
});
// ─── Render loop ───────────────────────────────────────────────
function animate(timestamp) {
  requestAnimationFrame(animate);
  // FPS calculation with rolling window
  const now = performance.now();
  const rawDelta = (now - lastFrameTime) / 1000;
  const delta = Math.min(0.5, Math.max(0.001, rawDelta)); // clamp to prevent spikes
  lastFrameTime = now;
  fpsHistory[fpsHistoryIndex] = delta > 0 ? 1 / delta : 0;
  fpsHistoryIndex = (fpsHistoryIndex + 1) % FPS_WINDOW;
  controls.update();
  updateParticles(delta);
  renderer.render(scene, camera);
  // Update diagnostics every 30 frames (debounced UI update)
  if (fpsHistoryIndex % 30 === 0) {
    const validFps = fpsHistory.filter(v => v > 0);
    const avgFps = validFps.length > 0
      ? Math.round(validFps.reduce((a, b) => a + b, 0) / validFps.length)
      : 0;
    diagFps.textContent = avgFps;
    diagTerrainHit.textContent = terrainHits;
    diagTerrainMiss.textContent = terrainMisses;
    diagRiverHit.textContent = riverHits;
    diagRiverMiss.textContent = riverMisses;
  }
}
// ─── Initialization ────────────────────────────────────────────
createRiverMesh();
setFrame(0);
renderBookmarks();
requestAnimationFrame(animate);
// ─── Edge-case audit log (console-only, non-blocking) ──────────
console.log('Edge-case guards active:',
  'frame clamping,',
  'elevation clamping,',
  'dt clamping,',
  'hotspot <2 degenerate geometry,',
  'bookmark bounds check,',
  'grid coord bounds clamping,',
  'fps window filtering'
);
console.log('Caches active: terrain geometry cache, river TubeGeometry cache, grid-to-height memoization');
console.log('Hot-path audit: no new Geometry() in per-frame path; particle positions array reused; river rebuild debounced 200ms');
</script>
</body>
</html>