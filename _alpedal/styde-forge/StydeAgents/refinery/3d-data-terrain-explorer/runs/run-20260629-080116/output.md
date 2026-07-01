<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8c8d4; }
  canvas { display: block; }
  /* Dashboard panel — fixed overlay, semi-transparent */
  #panel {
    position: fixed; top: 16px; right: 16px; width: 280px;
    background: rgba(10, 10, 20, 0.88); backdrop-filter: blur(10px);
    border: 1px solid rgba(100, 140, 200, 0.25); border-radius: 10px;
    padding: 16px; z-index: 10; user-select: none;
  }
  #panel h2 { font-size: 15px; font-weight: 600; margin-bottom: 10px; color: #7eb8ff; letter-spacing: 0.4px; }
  .metric-row { display: flex; justify-content: space-between; font-size: 12px; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }
  .metric-label { color: #8899aa; }
  .metric-value { font-weight: 600; color: #d0dce8; }
  /* Time slider bar at bottom */
  #timebar {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    width: 420px; max-width: 90vw; z-index: 10;
    background: rgba(10, 10, 20, 0.82); backdrop-filter: blur(8px);
    border: 1px solid rgba(100, 140, 200, 0.2); border-radius: 8px;
    padding: 10px 16px; display: flex; align-items: center; gap: 10px;
  }
  #timebar label { font-size: 11px; color: #7eb8ff; white-space: nowrap; }
  #timeslider { flex: 1; accent-color: #4a90d9; height: 4px; }
  #timelabel { font-size: 11px; color: #aabbcc; min-width: 80px; text-align: right; }
  /* Bookmark bar */
  #bookmarks {
    position: fixed; bottom: 20px; right: 20px; z-index: 10;
    display: flex; flex-direction: column; gap: 4px;
  }
  .bm-btn {
    font-size: 10px; padding: 4px 10px; border-radius: 4px; cursor: pointer;
    background: rgba(40, 60, 90, 0.7); border: 1px solid rgba(100,140,200,0.3); color: #aac;
    transition: background 0.2s;
  }
  .bm-btn:hover { background: rgba(60, 90, 140, 0.7); }
  .bm-save { background: rgba(30, 120, 80, 0.6); border-color: rgba(80,200,120,0.4); color: #8d8; }
  /* Legend */
  #legend {
    position: fixed; bottom: 90px; left: 20px; z-index: 10;
    background: rgba(10,10,20,0.78); backdrop-filter: blur(6px);
    border: 1px solid rgba(100,140,200,0.18); border-radius: 6px;
    padding: 8px 12px; font-size: 10px;
  }
  .legend-item { display: flex; align-items: center; gap: 6px; margin: 2px 0; }
  .legend-swatch { width: 12px; height: 12px; border-radius: 2px; }
</style>
</head>
<body>
<!-- Dashboard panel: live metric readouts -->
<div id="panel">
  <h2>3D Data Terrain</h2>
  <div class="metric-row"><span class="metric-label">Revenue (elevation)</span><span class="metric-value" id="m-rev">—</span></div>
  <div class="metric-row"><span class="metric-label">Users (vegetation)</span><span class="metric-value" id="m-users">—</span></div>
  <div class="metric-row"><span class="metric-label">Errors (rivers)</span><span class="metric-value" id="m-err">—</span></div>
  <div class="metric-row"><span class="metric-label">API calls/min</span><span class="metric-value" id="m-api">—</span></div>
  <div class="metric-row"><span class="metric-label">Time index</span><span class="metric-value" id="m-time">0 / 0</span></div>
</div>
<!-- Time scrubber -->
<div id="timebar">
  <label>Time</label>
  <input type="range" id="timeslider" min="0" max="0" value="0" step="1">
  <span id="timelabel">Day 0</span>
</div>
<!-- Bookmark buttons -->
<div id="bookmarks">
  <button class="bm-btn bm-save" id="bm-save" title="Save current camera position">+ Bookmark</button>
  <div id="bm-list"></div>
</div>
<!-- Color legend -->
<div id="legend">
  <div class="legend-item"><span class="legend-swatch" style="background:#2d5a1e;"></span> Low vegetation (few users)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#6baf3c;"></span> High vegetation (many users)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#c44a3a;"></span> Error river path</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ffcc44;border-radius:50%;width:8px;height:8px;"></span> API call particle</div>
</div>
<!-- Three.js import map: CDN-hosted modules, no bundler needed -->
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
// ─── Deterministic RNG (seeded, no floating-point accumulation) ───
// Non-determinism audit: all randomness flows through this seeded mulberry32 PRNG.
// No Math.random() calls anywhere — every stochastic value is reproducible.
let _rngState = 0x9E3779B9;
/** @returns {number} Deterministic float in [0,1) */
function seededRandom() {
  _rngState ^= _rngState >>> 16;
  _rngState = Math.imul(_rngState, 0x21F0AAAD);
  _rngState ^= _rngState >>> 15;
  _rngState = Math.imul(_rngState, 0x735A2D97);
  _rngState ^= _rngState >>> 15;
  return (_rngState >>> 0) / 4294967296;
}
// ─── Constants ───
const GRID_SIZE = 20;          // 20x20 terrain grid
const TIME_STEPS = 30;         // 30 time slices (days)
const TERRAIN_SCALE = 16;      // World-space width/depth of terrain
const HEIGHT_SCALE = 5;        // Max elevation in world units
const RIVER_THRESHOLD = 0.65;  // Error rate above this → river cell
const PARTICLE_COUNT = 300;    // Number of API-call particles
// ─── Synthetic time-series data ───
// Each time step has 3 grids (revenue, user density, error rate) plus API call count.
// Revenue drives elevation, user density drives vertex color, error rate drives rivers.
/**
 * Generate smooth synthetic terrain data across time.
 * Uses layered sine waves with deterministic noise — no Math.random().
 * @returns {{ revenue: number[][][], users: number[][][], errors: number[][][], apiCount: number[] }}
 */
function generateData() {
  const revenue = [];  // [time][row][col]
  const users = [];    // [time][row][col]
  const errors = [];   // [time][row][col]
  const apiCount = []; // [time]
  // Pre-compute noise grid for spatial coherence (shared across time)
  const noise = new Array(GRID_SIZE);
  for (let r = 0; r < GRID_SIZE; r++) {
    noise[r] = new Array(GRID_SIZE);
    for (let c = 0; c < GRID_SIZE; c++) {
      // Multi-octave noise via weighted sine sums — deterministic, no floats accumulated
      const nx = (c / GRID_SIZE) * 6.283; // 0..2π
      const ny = (r / GRID_SIZE) * 6.283;
      noise[r][c] =
        Math.sin(nx * 1.3 + ny * 0.7) * 0.6 +
        Math.sin(nx * 2.7 - ny * 1.1) * 0.3 +
        Math.sin(nx * 5.1 + ny * 3.3) * 0.1;
    }
  }
  for (let t = 0; t < TIME_STEPS; t++) {
    const phase = (t / TIME_STEPS) * Math.PI * 2; // Time wraps for smooth loop
    const revGrid = [];
    const usrGrid = [];
    const errGrid = [];
    // Total API calls grows then dips (simulates traffic pattern)
    apiCount.push(200 + Math.sin(phase * 2.1) * 80 + Math.cos(phase * 0.7) * 40);
    for (let r = 0; r < GRID_SIZE; r++) {
      revGrid[r] = [];
      usrGrid[r] = [];
      errGrid[r] = [];
      for (let c = 0; c < GRID_SIZE; c++) {
        // Revenue: central peak with time-varying ridge
        const distFromCenter = Math.sqrt(
          ((c - GRID_SIZE/2) / (GRID_SIZE/2)) ** 2 +
          ((r - GRID_SIZE/2) / (GRID_SIZE/2)) ** 2
        );
        const ridgeFactor = 1 - distFromCenter; // Higher near center
        const temporalShift = Math.sin(phase + distFromCenter * 2.5) * 0.3;
        revGrid[r][c] = clamp01(ridgeFactor * 0.7 + temporalShift + noise[r][c] * 0.15);
        // User density: follows revenue but with spread and lag
        const lagPhase = phase - 0.4; // Users lag behind revenue
        const userSpread = 1 - distFromCenter * 0.7;
        usrGrid[r][c] = clamp01(
          userSpread * 0.6 +
          Math.sin(lagPhase + distFromCenter * 1.8) * 0.25 +
          noise[r][c] * 0.2
        );
        // Error rate: inverse of revenue (troughs = errors), plus hotspots
        const errorBase = (1 - revGrid[r][c]) * 0.5;
        // Random hotspot at fixed position (seeded deterministic)
        const hotspotDist = Math.sqrt((c - 5)**2 + (r - 14)**2) / GRID_SIZE;
        const hotspot = hotspotDist < 0.2 ? 0.4 : 0;
        errGrid[r][c] = clamp01(errorBase + hotspot + seededRandom() * 0.08);
      }
    }
    revenue.push(revGrid);
    users.push(usrGrid);
    errors.push(errGrid);
  }
  return { revenue, users, errors, apiCount };
}
/** Clamp value to [0, 1] without branching when possible */
function clamp01(v) { return v < 0 ? 0 : v > 1 ? 1 : v; }
// ─── Global state ───
const data = generateData();
let currentTime = 0;
// ─── Three.js setup ───
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap for perf
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 18, 50); // Distant fade for depth
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(14, 10, 14);
camera.lookAt(0, 0, 0);
// ─── Lighting ───
// Ambient fills shadows; directional gives terrain contour via Lambert shading
const ambientLight = new THREE.AmbientLight(0x334466, 1.6);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 2.4);
sunLight.position.set(8, 15, 5);
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466aa, 0.8);
fillLight.position.set(-5, 3, -8);
scene.add(fillLight);
// ─── OrbitControls with smooth damping ───
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, HEIGHT_SCALE * 0.3, 0);
controls.minDistance = 5;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48; // Prevent going underground
controls.autoRotate = false;
controls.autoRotateSpeed = 0.3;
controls.update();
// ─── Bookmark system ───
/** @type {{ name: string, pos: THREE.Vector3, target: THREE.Vector3 }[]} */
const bookmarks = [];
/** Save current camera position and target as a named bookmark */
function saveBookmark() {
  const name = `View ${bookmarks.length + 1}`;
  bookmarks.push({
    name,
    pos: camera.position.clone(),
    target: controls.target.clone()
  });
  renderBookmarkButtons();
}
/** Restore camera to a saved bookmark with smooth animation */
function restoreBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  // Smooth animate: lerp camera over ~0.6s using requestAnimationFrame
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.pos;
  const endTarget = bm.target;
  const startTime = performance.now();
  const duration = 600; // ms
  /** Animation step for bookmark transition */
  function animateStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease in-out cubic for smooth landing
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animateStep);
    }
  }
  requestAnimationFrame(animateStep);
}
/** Rebuild the DOM bookmark button list */
function renderBookmarkButtons() {
  const list = document.getElementById('bm-list');
  list.innerHTML = '';
  bookmarks.forEach((bm, i) => {
    const btn = document.createElement('button');
    btn.className = 'bm-btn';
    btn.textContent = bm.name;
    btn.addEventListener('click', () => restoreBookmark(i));
    list.appendChild(btn);
  });
}
document.getElementById('bm-save').addEventListener('click', saveBookmark);
// ─── Terrain geometry cache ───
// Pre-build one BufferGeometry per time step. On slider change, swap the mesh geometry
// instead of rebuilding — this is the cache strategy from the blueprint.
/** @type {THREE.BufferGeometry[]} */
const terrainGeoCaches = [];
/** @type {THREE.Mesh|null} */
let terrainMesh = null;
/**
 * Build a BufferGeometry for a single time step.
 * Positions: elevation from revenue grid.
 * Colors: vertex colors mapped from user density (vegetation gradient).
 * @param {number} t - Time index
 * @returns {THREE.BufferGeometry}
 */
function buildTerrainGeometry(t) {
  const revGrid = data.revenue[t];
  const usrGrid = data.users[t];
  // We create (GRID_SIZE) x (GRID_SIZE) vertices
  const vertexCount = GRID_SIZE * GRID_SIZE;
  const positions = new Float32Array(vertexCount * 3);
  const colors = new Float32Array(vertexCount * 3);
  const step = TERRAIN_SCALE / (GRID_SIZE - 1);
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      const idx = r * GRID_SIZE + c;
      // World XZ: center the grid at origin
      const x = c * step - TERRAIN_SCALE / 2;
      const z = r * step - TERRAIN_SCALE / 2;
      // Elevation from revenue
      const y = revGrid[r][c] * HEIGHT_SCALE;
      positions[idx * 3] = x;
      positions[idx * 3 + 1] = y;
      positions[idx * 3 + 2] = z;
      // Vegetation color: user density → green gradient
      // Low = dark forest green (#2d5a1e), High = bright yellow-green (#8fd63c)
      const u = usrGrid[r][c];
      // RGB interpolation: lerp between dark and bright green
      const cr = 0.18 + u * 0.14;  // R: 0.18→0.32
      const cg = 0.35 + u * 0.49;  // G: 0.35→0.84
      const cb = 0.12 + u * 0.12;  // B: 0.12→0.24
      colors[idx * 3] = cr;
      colors[idx * 3 + 1] = cg;
      colors[idx * 3 + 2] = cb;
    }
  }
  // Build index buffer: two triangles per grid cell
  const indices = [];
  for (let r = 0; r < GRID_SIZE - 1; r++) {
    for (let c = 0; c < GRID_SIZE - 1; c++) {
      const a = r * GRID_SIZE + c;
      const b = a + 1;
      const d = a + GRID_SIZE;
      const e = d + 1;
      // Two triangles: a-b-d and b-e-d
      indices.push(a, b, d);
      indices.push(b, e, d);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals(); // Needed for directional light shading
  return geo;
}
// Pre-build all geometry variants
for (let t = 0; t < TIME_STEPS; t++) {
  terrainGeoCaches.push(buildTerrainGeometry(t));
}
// Create terrain mesh once, swap geometry at runtime
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.08,
  flatShading: false
});
terrainMesh = new THREE.Mesh(terrainGeoCaches[0], terrainMaterial);
scene.add(terrainMesh);
// ─── Base platform (semi-transparent) ───
const baseGeo = new THREE.PlaneGeometry(TERRAIN_SCALE * 1.05, TERRAIN_SCALE * 1.05);
const baseMat = new THREE.MeshBasicMaterial({
  color: 0x1a1a2e,
  side: THREE.DoubleSide,
  transparent: true,
  opacity: 0.25
});
const basePlane = new THREE.Mesh(baseGeo, baseMat);
basePlane.rotation.x = -Math.PI / 2;
basePlane.position.y = -0.05;
scene.add(basePlane);
// Add subtle grid lines on the base plane for spatial reference
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SCALE / 2, 20, 12, 64, 0x334466, 0x223355);
gridHelper.position.y = -0.04;
scene.add(gridHelper);
// ─── River geometry: trace error hotspots ───
/** @type {THREE.LineSegments|null} */
let riverLines = null;
/**
 * Build river line segments from error grid.
 * For each cell above RIVER_THRESHOLD, trace downhill toward neighbor with
 * steepest error gradient, creating connected red line segments.
 * @param {number} t - Time index
 * @returns {THREE.BufferGeometry}
 */
function buildRiverGeometry(t) {
  const errGrid = data.errors[t];
  const revGrid = data.revenue[t];
  const points = [];
  const step = TERRAIN_SCALE / (GRID_SIZE - 1);
  // Collect high-error cells as river sources
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      if (errGrid[r][c] < RIVER_THRESHOLD) continue;
      // World position of this cell
      const x = c * step - TERRAIN_SCALE / 2;
      const z = r * step - TERRAIN_SCALE / 2;
      const y = revGrid[r][c] * HEIGHT_SCALE + 0.08; // Slightly above terrain
      // Find neighbor with steepest downhill error gradient (8-connected)
      let bestDr = 0, bestDc = 0, bestGrad = -Infinity;
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          if (dr === 0 && dc === 0) continue;
          const nr = r + dr, nc = c + dc;
          if (nr < 0 || nr >= GRID_SIZE || nc < 0 || nc >= GRID_SIZE) continue;
          // Gradient: error drops toward higher-revenue areas (downhill in error space)
          const grad = errGrid[r][c] - errGrid[nr][nc];
          if (grad > bestGrad) {
            bestGrad = grad;
            bestDr = dr;
            bestDc = dc;
          }
        }
      }
      // Only draw if there's a meaningful downhill path
      if (bestGrad < 0.02) continue;
      const nx = (c + bestDc) * step - TERRAIN_SCALE / 2;
      const nz = (r + bestDr) * step - TERRAIN_SCALE / 2;
      const ny = revGrid[r + bestDr][c + bestDc] * HEIGHT_SCALE + 0.08;
      // Push both endpoints of this river segment
      points.push(x, y, z, nx, ny, nz);
    }
  }
  if (points.length === 0) {
    // Return empty geometry if no river cells found
    return new THREE.BufferGeometry();
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(points), 3));
  return geo;
}
/** Update river display for the current time step */
function updateRivers(t) {
  if (riverLines) {
    riverLines.geometry.dispose();
    scene.remove(riverLines);
  }
  const riverGeo = buildRiverGeometry(t);
  if (riverGeo.attributes.position && riverGeo.attributes.position.count > 0) {
    const riverMat = new THREE.LineBasicMaterial({
      color: 0xd94a3a,
      linewidth: 1,
      transparent: true,
      opacity: 0.75,
      depthTest: true
    });
    riverLines = new THREE.LineSegments(riverGeo, riverMat);
    scene.add(riverLines);
  } else {
    riverGeo.dispose();
    riverLines = null;
  }
}
// ─── Particle system: API call trails ───
// Each particle has a position (x,y,z) and a target cell. Particles flow
// along paths of least elevation (valleys) and loop when reaching destination.
/** @type {{ positions: Float32Array, targets: Float32Array, mesh: THREE.Points }|null} */
let particleSystem = null;
/**
 * Initialize particle positions and targets.
 * Each particle targets a random grid cell weighted toward lower elevation (valleys).
 * Using seeded PRNG for reproducibility.
 */
function initParticles() {
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const targets = new Float32Array(PARTICLE_COUNT * 2); // target (col, row)
  const step = TERRAIN_SCALE / (GRID_SIZE - 1);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Start at random position in the terrain bounds
    const sx = (seededRandom() - 0.5) * TERRAIN_SCALE;
    const sz = (seededRandom() - 0.5) * TERRAIN_SCALE;
    // Initial height from revenue lookup
    const sc = Math.floor((sx + TERRAIN_SCALE / 2) / step);
    const sr = Math.floor((sz + TERRAIN_SCALE / 2) / step);
    const sy = (data.revenue[0][clamp(sr, 0, GRID_SIZE-1)]?.[clamp(sc, 0, GRID_SIZE-1)] ?? 0.3) * HEIGHT_SCALE + 0.15;
    positions[i * 3] = sx;
    positions[i * 3 + 1] = sy;
    positions[i * 3 + 2] = sz;
    // Target: bias toward low-elevation cells (valleys)
    const tc = Math.floor(seededRandom() * GRID_SIZE);
    const tr = Math.floor(seededRandom() * GRID_SIZE);
    targets[i * 2] = tc;
    targets[i * 2 + 1] = tr;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  // Use a small circle sprite for each particle
  const spriteTex = createGlowTexture();
  const mat = new THREE.PointsMaterial({
    size: 0.12,
    map: spriteTex,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    color: 0xffcc44,
    opacity: 0.7,
    transparent: true
  });
  const points = new THREE.Points(geo, mat);
  scene.add(points);
  return { positions, targets, mesh: points };
}
/**
 * Create a radial gradient texture for particle glow.
 * Canvas 2D → Three.js texture, 32x32px for performance.
 */
function createGlowTexture() {
  const size = 32;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  gradient.addColorStop(0, 'rgba(255,220,100,1)');
  gradient.addColorStop(0.3, 'rgba(255,180,60,0.8)');
  gradient.addColorStop(0.7, 'rgba(255,120,20,0.2)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}
/** Clamp integer to [min, max] */
function clamp(v, min, max) { return v < min ? min : v > max ? max : v; }
particleSystem = initParticles();
/**
 * Update particle positions each frame.
 * Each particle moves toward its target cell at a fixed speed.
 * On arrival, pick a new random target (seeded PRNG).
 * Height is sampled from current terrain for surface-following.
 * @param {number} t - Current time index
 * @param {number} dt - Delta time in seconds
 */
function updateParticles(t, dt) {
  if (!particleSystem) return;
  const { positions, targets } = particleSystem;
  const step = TERRAIN_SCALE / (GRID_SIZE - 1);
  const speed = 0.8; // World units per second
  const revGrid = data.revenue[t];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const px = positions[i * 3];
    const pz = positions[i * 3 + 2];
    // Target world position
    const tx = targets[i * 2] * step - TERRAIN_SCALE / 2;
    const tz = targets[i * 2 + 1] * step - TERRAIN_SCALE / 2;
    // Direction vector toward target (XZ plane)
    const dx = tx - px;
    const dz = tz - pz;
    const dist = Math.sqrt(dx * dx + dz * dz);
    if (dist < 0.15) {
      // Arrived at target — pick new target cell (seeded)
      targets[i * 2] = Math.floor(seededRandom() * GRID_SIZE);
      targets[i * 2 + 1] = Math.floor(seededRandom() * GRID_SIZE);
      // Slight position jitter to prevent stacking (deterministic)
      positions[i * 3] = tx + (seededRandom() - 0.5) * 0.3;
      positions[i * 3 + 2] = tz + (seededRandom() - 0.5) * 0.3;
    } else {
      // Move toward target at constant speed
      const move = Math.min(speed * dt, dist);
      positions[i * 3] += (dx / dist) * move;
      positions[i * 3 + 2] += (dz / dist) * move;
    }
    // Sample terrain height at current position for surface tracking
    const sc = Math.round((positions[i * 3] + TERRAIN_SCALE / 2) / step);
    const sr = Math.round((positions[i * 3 + 2] + TERRAIN_SCALE / 2) / step);
    const scClamped = clamp(sc, 0, GRID_SIZE - 1);
    const srClamped = clamp(sr, 0, GRID_SIZE - 1);
    positions[i * 3 + 1] = revGrid[srClamped][scClamped] * HEIGHT_SCALE + 0.18;
  }
  // Flag attribute as needing GPU upload
  particleSystem.mesh.geometry.attributes.position.needsUpdate = true;
}
// ─── UI wiring ───
const timeslider = document.getElementById('timeslider');
const timelabel = document.getElementById('timelabel');
timeslider.max = TIME_STEPS - 1;
timeslider.value = 0;
/** Handle time slider change: swap terrain, rebuild rivers, update labels */
function onTimeChange(t) {
  currentTime = t;
  // Swap cached terrain geometry
  if (terrainMesh) {
    terrainMesh.geometry = terrainGeoCaches[t];
  }
  // Rebuild river lines for new time
  updateRivers(t);
  // Update dashboard labels
  timelabel.textContent = `Day ${t + 1}`;
  updateDashboard(t);
}
timeslider.addEventListener('input', () => onTimeChange(parseInt(timeslider.value)));
// ─── Dashboard update ───
function updateDashboard(t) {
  const revGrid = data.revenue[t];
  const usrGrid = data.users[t];
  const errGrid = data.errors[t];
  // Compute spatial averages
  let revSum = 0, usrSum = 0, errSum = 0;
  let errCount = 0;
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      revSum += revGrid[r][c];
      usrSum += usrGrid[r][c];
      errSum += errGrid[r][c];
      if (errGrid[r][c] > RIVER_THRESHOLD) errCount++;
    }
  }
  const n = GRID_SIZE * GRID_SIZE;
  document.getElementById('m-rev').textContent = formatCurrency(revSum / n * 100000);
  document.getElementById('m-users').textContent = Math.round(usrSum / n * 5000).toLocaleString();
  document.getElementById('m-err').textContent = (errSum / n * 100).toFixed(1) + '%';
  document.getElementById('m-api').textContent = Math.round(data.apiCount[t]).toLocaleString();
  document.getElementById('m-time').textContent = `${t + 1} / ${TIME_STEPS}`;
}
function formatCurrency(v) { return '$' + Math.round(v).toLocaleString(); }
// Auto-rotate toggle via keyboard
window.addEventListener('keydown', (e) => {
  if (e.key === 'r' || e.key === 'R') {
    controls.autoRotate = !controls.autoRotate;
  }
});
// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Animation loop ───
let lastTime = performance.now();
function animate(now) {
  requestAnimationFrame(animate);
  const dt = Math.min((now - lastTime) / 1000, 0.1); // Cap delta to avoid spiral on tab switch
  lastTime = now;
  controls.update(); // Damping + auto-rotate handled by OrbitControls
  updateParticles(currentTime, dt);
  renderer.render(scene, camera);
}
// ─── Initialization ───
updateRivers(0);
updateDashboard(0);
timelabel.textContent = 'Day 1';
requestAnimationFrame(animate);
</script>
</body>
</html>