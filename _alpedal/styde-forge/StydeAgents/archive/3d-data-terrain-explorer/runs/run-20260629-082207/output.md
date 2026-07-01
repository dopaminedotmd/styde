<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #0a0a12;
    color: #c8ccd4;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
    user-select: none;
    -webkit-user-select: none;
  }
  canvas { display: block; }
  #loading-overlay {
    position: fixed; inset: 0; z-index: 1000;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    background: #0a0a12;
    transition: opacity 0.4s;
  }
  #loading-overlay.hidden { opacity: 0; pointer-events: none; }
  #loading-bar-track {
    width: 280px; height: 6px; background: #1a1a2e; border-radius: 3px; margin-top: 16px; overflow: hidden;
  }
  #loading-bar-fill {
    height: 100%; width: 0%; background: linear-gradient(90deg, #2d8c4a, #4ecb71);
    border-radius: 3px; transition: width 0.15s;
  }
  #loading-text { margin-top: 10px; font-size: 13px; color: #6a7080; }
  #error-overlay {
    position: fixed; inset: 0; z-index: 1001;
    display: none; flex-direction: column; align-items: center; justify-content: center;
    background: #0a0a12; color: #e05555; text-align: center; padding: 40px;
  }
  #error-overlay.visible { display: flex; }
  #error-overlay h2 { font-size: 20px; margin-bottom: 12px; }
  #error-overlay p { font-size: 14px; color: #8a8fa0; max-width: 400px; line-height: 1.5; }
  #empty-overlay {
    position: fixed; inset: 0; z-index: 1001;
    display: none; flex-direction: column; align-items: center; justify-content: center;
    background: #0a0a12; color: #8a8fa0;
  }
  #empty-overlay.visible { display: flex; }
  #ui-bar {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    display: flex; align-items: center; gap: 14px;
    background: rgba(10, 10, 22, 0.85);
    backdrop-filter: blur(10px);
    padding: 10px 20px; border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    z-index: 100;
  }
  #ui-bar button {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
    color: #c8ccd4; padding: 6px 14px; border-radius: 6px; cursor: pointer;
    font-size: 13px; white-space: nowrap; transition: background 0.15s;
  }
  #ui-bar button:hover { background: rgba(255,255,255,0.14); }
  #ui-bar button.active { background: #2d8c4a; border-color: #3eb85a; color: #fff; }
  #time-slider {
    width: 180px; accent-color: #4ecb71; cursor: pointer;
  }
  #time-label { font-size: 12px; color: #6a7080; min-width: 60px; text-align: center; }
  #diag-panel {
    position: fixed; top: 14px; right: 14px; z-index: 100;
    background: rgba(10, 10, 22, 0.82);
    backdrop-filter: blur(8px);
    padding: 10px 14px; border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.06);
    font-size: 11px; line-height: 1.7; color: #5a6070; font-family: 'SF Mono', 'Consolas', monospace;
    min-width: 170px;
  }
  #diag-panel .val { color: #8a90a4; }
  #diag-panel .hit { color: #4ecb71; }
  #diag-panel .miss { color: #e0a055; }
  #bookmark-label {
    position: fixed; top: 50%; left: 50%; transform: translate(-50%,-50%) scale(0);
    background: rgba(0,0,0,0.7); color: #fff; padding: 6px 16px; border-radius: 6px;
    font-size: 14px; pointer-events: none; transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    z-index: 101;
  }
  #bookmark-label.pop { transform: translate(-50%,-50%) scale(1); }
</style>
</head>
<body>
<div id="loading-overlay">
  <div style="font-size:18px;color:#c8ccd4;">Building Terrain</div>
  <div id="loading-bar-track"><div id="loading-bar-fill"></div></div>
  <div id="loading-text">Generating geometry cache...</div>
</div>
<div id="error-overlay">
  <h2>WebGL Not Available</h2>
  <p>Your browser or GPU does not support WebGL. The 3D terrain requires hardware acceleration. Try a modern browser with GPU enabled.</p>
</div>
<div id="empty-overlay">
  <p>No data available. Load a dataset to visualize terrain.</p>
</div>
<div id="diag-panel" aria-label="Performance diagnostics">
  FPS <span class="val" id="diag-fps">--</span><br>
  Terrain cache <span class="hit" id="diag-t-hit">0</span>/<span class="miss" id="diag-t-miss">0</span><br>
  River cache <span class="hit" id="diag-r-hit">0</span>/<span class="miss" id="diag-r-miss">0</span><br>
  Grid memo <span class="hit" id="diag-m-hit">0</span>/<span class="miss" id="diag-m-miss">0</span><br>
  Draw calls <span class="val" id="diag-draws">--</span>
</div>
<div id="ui-bar" role="toolbar" aria-label="Terrain controls">
  <button id="btn-play" aria-label="Play/pause time animation" title="Play/Pause (Space)">▶</button>
  <input type="range" id="time-slider" min="0" max="0" value="0" aria-label="Time step slider" title="Scrub through time">
  <span id="time-label">0 / 0</span>
  <button id="btn-autorot" aria-label="Toggle auto-rotation" title="Auto-rotate (R)">⟳</button>
  <button id="btn-bm1" aria-label="Bookmark 1: overview" title="Bookmark 1 (Key 1)">View 1</button>
  <button id="btn-bm2" aria-label="Bookmark 2: close-up" title="Bookmark 2 (Key 2)">View 2</button>
  <button id="btn-bm3" aria-label="Bookmark 3: top-down" title="Bookmark 3 (Key 3)">View 3</button>
</div>
<div id="bookmark-label" aria-live="polite"></div>
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
// ============================================================
// Configuration
// ============================================================
const GRID_SIZE = 80;
const TIME_STEPS = 48;
const PARTICLE_COUNT = 600;
const RIVER_DEBOUNCE_MS = 200;
const TERRAIN_SIZE = 20;
const MAX_HEIGHT = 6;
const RIVER_ERROR_THRESHOLD = 0.55;
const BOOKMARK_PRESETS = [
  { pos: [18, 10, 18], target: [0, 1.5, 0], label: 'Overview' },
  { pos: [4, 4, 4], target: [2, 1.2, 2], label: 'Close-up' },
  { pos: [0, 16, 0.5], target: [0, 1.5, 0], label: 'Top-down' }
];
// ============================================================
// Diagnostics tracking
// ============================================================
const diag = {
  terrainHits: 0, terrainMisses: 0,
  riverHits: 0, riverMisses: 0,
  memoHits: 0, memoMisses: 0,
  fps: 0, frames: 0, lastFpsTime: performance.now(),
  drawCalls: 0
};
function updateDiagPanel() {
  document.getElementById('diag-fps').textContent = diag.fps;
  document.getElementById('diag-t-hit').textContent = diag.terrainHits;
  document.getElementById('diag-t-miss').textContent = diag.terrainMisses;
  document.getElementById('diag-r-hit').textContent = diag.riverHits;
  document.getElementById('diag-r-miss').textContent = diag.riverMisses;
  document.getElementById('diag-m-hit').textContent = diag.memoHits;
  document.getElementById('diag-m-miss').textContent = diag.memoMisses;
  document.getElementById('diag-draws').textContent = diag.drawCalls;
}
// ============================================================
// Data generation — synthetic time-series terrain
// ============================================================
function generateGrid(t, gridSize) {
  const grid = [];
  const half = (gridSize - 1) / 2;
  for (let row = 0; row < gridSize; row++) {
    grid[row] = [];
    for (let col = 0; col < gridSize; col++) {
      const x = (col - half) / half;
      const z = (row - half) / half;
      const dist = Math.sqrt(x * x + z * z);
      // Multi-octave height field evolving over time
      const h1 = Math.sin(x * 2.5 + t * 0.3) * Math.cos(z * 2.0 + t * 0.4);
      const h2 = Math.sin(x * 5.0 - t * 0.2) * Math.cos(z * 4.5 + t * 0.35);
      const h3 = Math.sin((x + z) * 3.0 + t * 0.5) * 0.5;
      const edge = 1 - Math.min(1, dist * 1.1);
      let height = (h1 * 0.5 + h2 * 0.3 + h3 * 0.2) * edge + 0.5;
      height = Math.max(0.03, Math.min(1, height));
      // User density: independent pattern
      const d1 = Math.cos(x * 3.0 + t * 0.25) * Math.sin(z * 2.8 - t * 0.3);
      const d2 = Math.sin(x * 6.0 + z * 5.0 + t * 0.15) * 0.4;
      let density = (d1 * 0.6 + d2 * 0.4) * edge + 0.5;
      density = Math.max(0, Math.min(1, density));
      // Error rate: concentrates at high-frequency terrain and edges
      const e1 = Math.abs(Math.sin(x * 7.0 + t * 0.6)) * Math.abs(Math.cos(z * 6.0 + t * 0.55));
      const e2 = (1 - edge) * 0.7;
      let error = e1 * 0.65 + e2 * 0.35;
      error = Math.max(0, Math.min(1, error));
      grid[row][col] = { height, userDensity: density, errorRate: error };
    }
  }
  return grid;
}
function generateAllTimeSeries(numSteps, gridSize) {
  const series = [];
  for (let t = 0; t < numSteps; t++) {
    const phase = (t / numSteps) * Math.PI * 2;
    series.push(generateGrid(phase, gridSize));
  }
  return series;
}
// ============================================================
// Vertex color: vegetation-like gradient from density + height
// ============================================================
function vertexColor(height, density) {
  // Reddish-brown at peaks, green in vegetated midlands, darker in valleys
  const r = 0.18 + height * 0.38;
  const g = 0.22 + density * 0.48;
  const b = 0.10 + (1 - height) * 0.12;
  return [r, g, b];
}
// ============================================================
// Shared index buffer — computed once, reused across all terrains
// ============================================================
function buildSharedIndexBuffer(gridSize) {
  const indices = [];
  for (let row = 0; row < gridSize - 1; row++) {
    for (let col = 0; col < gridSize - 1; col++) {
      const a = row * gridSize + col;
      const b = a + 1;
      const c = a + gridSize;
      const d = c + 1;
      indices.push(a, b, d, a, d, c);
    }
  }
  return new Uint32Array(indices);
}
// ============================================================
// Terrain geometry builder — creates one BufferGeometry per time step
// ============================================================
function buildTerrainGeometry(grid, gridSize, sizeX, sizeZ, maxH, sharedIndices) {
  const vertCount = gridSize * gridSize;
  const positions = new Float32Array(vertCount * 3);
  const colors = new Float32Array(vertCount * 3);
  const halfX = sizeX / 2;
  const halfZ = sizeZ / 2;
  for (let row = 0; row < gridSize; row++) {
    for (let col = 0; col < gridSize; col++) {
      const idx = row * gridSize + col;
      const cell = grid[row][col];
      const px = (col / (gridSize - 1)) * sizeX - halfX;
      const pz = (row / (gridSize - 1)) * sizeZ - halfZ;
      const py = cell.height * maxH;
      positions[idx * 3] = px;
      positions[idx * 3 + 1] = py;
      positions[idx * 3 + 2] = pz;
      const [cr, cg, cb] = vertexColor(cell.height, cell.userDensity);
      colors[idx * 3] = cr;
      colors[idx * 3 + 1] = cg;
      colors[idx * 3 + 2] = cb;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(new THREE.BufferAttribute(sharedIndices, 1));
  geo.computeVertexNormals();
  return geo;
}
// ============================================================
// Cache: pre-computed terrain geometries keyed by time index
// ============================================================
const terrainGeometryCache = new Map();
function getTerrainGeometry(timeIndex) {
  if (terrainGeometryCache.has(timeIndex)) {
    diag.terrainHits++;
    return terrainGeometryCache.get(timeIndex);
  }
  diag.terrainMisses++;
  return null;
}
// ============================================================
// River path builder — traces high-error cells into a spline
// ============================================================
function buildRiverPath(grid, gridSize, sizeX, sizeZ, maxH) {
  const halfX = sizeX / 2;
  const halfZ = sizeZ / 2;
  const points = [];
  // Scan each row and find peak error column, collecting waypoints
  for (let row = 2; row < gridSize - 2; row += 3) {
    let bestCol = -1;
    let bestErr = 0;
    for (let col = 2; col < gridSize - 2; col++) {
      if (grid[row][col].errorRate > bestErr) {
        bestErr = grid[row][col].errorRate;
        bestCol = col;
      }
    }
    if (bestErr > RIVER_ERROR_THRESHOLD) {
      const cell = grid[row][bestCol];
      const px = (bestCol / (gridSize - 1)) * sizeX - halfX;
      const pz = (row / (gridSize - 1)) * sizeZ - halfZ;
      const py = cell.height * maxH + 0.12;
      points.push(new THREE.Vector3(px, py, pz));
    }
  }
  if (points.length < 3) return null;
  const curve = new THREE.CatmullRomCurve3(points);
  const tubeGeo = new THREE.TubeGeometry(curve, 80, 0.18, 8, false);
  return tubeGeo;
}
// ============================================================
// River geometry cache + debounce
// ============================================================
const riverGeometryCache = new Map();
let riverDebounceTimer = null;
let pendingRiverTimeIndex = -1;
function requestRiverRebuild(timeIndex) {
  if (riverGeometryCache.has(timeIndex)) {
    diag.riverHits++;
    applyRiverGeometry(riverGeometryCache.get(timeIndex));
    return;
  }
  diag.riverMisses++;
  // Debounce: only rebuild after user stops scrubbing for 200ms
  pendingRiverTimeIndex = timeIndex;
  if (riverDebounceTimer !== null) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    riverDebounceTimer = null;
    const grid = timeSeriesData[pendingRiverTimeIndex];
    const geo = buildRiverPath(grid, GRID_SIZE, TERRAIN_SIZE, TERRAIN_SIZE, MAX_HEIGHT);
    if (geo) {
      riverGeometryCache.set(pendingRiverTimeIndex, geo);
      applyRiverGeometry(geo);
    } else {
      // No significant error path — hide river
      if (riverMesh) riverMesh.visible = false;
    }
  }, RIVER_DEBOUNCE_MS);
}
function applyRiverGeometry(geo) {
  if (!riverMesh) return;
  // Dispose old geometry to free GPU memory
  if (riverMesh.geometry) riverMesh.geometry.dispose();
  riverMesh.geometry = geo;
  riverMesh.visible = true;
}
// ============================================================
// Particle system — single BufferGeometry with reused position array
// ============================================================
function createParticleSystem(count, sizeX, sizeZ, maxH) {
  const positions = new Float32Array(count * 3);
  const velocities = new Float32Array(count * 3);
  const halfX = sizeX / 2;
  const halfZ = sizeZ / 2;
  // Initialize particle positions randomly across terrain surface
  for (let i = 0; i < count; i++) {
    positions[i * 3] = (Math.random() - 0.5) * sizeX;
    positions[i * 3 + 1] = Math.random() * maxH * 0.7 + 0.3;
    positions[i * 3 + 2] = (Math.random() - 0.5) * sizeZ;
    // Random drift velocity
    velocities[i * 3] = (Math.random() - 0.5) * 0.06;
    velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.02;
    velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.06;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  // Create sprite texture via canvas
  const canvas = document.createElement('canvas');
  canvas.width = 32; canvas.height = 32;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, 'rgba(180,220,255,1)');
  gradient.addColorStop(0.35, 'rgba(120,180,240,0.7)');
  gradient.addColorStop(0.7, 'rgba(40,100,180,0.15)');
  gradient.addColorStop(1, 'rgba(0,0,40,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 32, 32);
  const texture = new THREE.CanvasTexture(canvas);
  texture.needsUpdate = true;
  const mat = new THREE.PointsMaterial({
    size: 0.25,
    map: texture,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    color: 0x88bbff
  });
  const points = new THREE.Points(geo, mat);
  return { points, velocities, positions };
}
// ============================================================
// Memoized world-to-grid lookup (single-entry last-value cache)
// ============================================================
const gridMemo = { worldX: NaN, worldZ: NaN, col: -1, row: -1 };
function worldToGrid(worldX, worldZ) {
  // Check memo: if same world position as last lookup, return cached result
  const eps = 0.01;
  if (Math.abs(worldX - gridMemo.worldX) < eps && Math.abs(worldZ - gridMemo.worldZ) < eps) {
    diag.memoHits++;
    return { col: gridMemo.col, row: gridMemo.row };
  }
  diag.memoMisses++;
  const halfX = TERRAIN_SIZE / 2;
  const halfZ = TERRAIN_SIZE / 2;
  const col = Math.round(((worldX + halfX) / TERRAIN_SIZE) * (GRID_SIZE - 1));
  const row = Math.round(((worldZ + halfZ) / TERRAIN_SIZE) * (GRID_SIZE - 1));
  // Update memo
  gridMemo.worldX = worldX;
  gridMemo.worldZ = worldZ;
  gridMemo.col = col;
  gridMemo.row = row;
  return { col, row };
}
// ============================================================
// Global state
// ============================================================
let timeSeriesData = [];
let timeIndex = 0;
let isPlaying = false;
let playInterval = null;
let terrainMesh, riverMesh, particleSystem;
let scene, camera, renderer, controls;
const sharedIndices = buildSharedIndexBuffer(GRID_SIZE);
// ============================================================
// Scene setup
// ============================================================
function setupScene() {
  const container = document.body;
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  container.appendChild(renderer.domElement);
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0d0d1a);
  scene.fog = new THREE.Fog(0x0d0d1a, 22, 48);
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
  camera.position.set(14, 8, 16);
  camera.lookAt(0, 2, 0);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 1.8, 0);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = false;
  controls.autoRotateSpeed = 0.4;
  controls.minDistance = 3;
  controls.maxDistance = 30;
  controls.maxPolarAngle = Math.PI * 0.48;
  controls.update();
  // Lighting
  const ambient = new THREE.AmbientLight(0x334466, 1.8);
  scene.add(ambient);
  const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
  sun.position.set(12, 18, 6);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.near = 0.5;
  sun.shadow.camera.far = 60;
  sun.shadow.camera.left = -18;
  sun.shadow.camera.right = 18;
  sun.shadow.camera.top = 18;
  sun.shadow.camera.bottom = -18;
  sun.shadow.bias = -0.0002;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x8899cc, 1.2);
  fill.position.set(-4, 3, -2);
  scene.add(fill);
  // Base plane
  const baseGeo = new THREE.PlaneGeometry(TERRAIN_SIZE + 2, TERRAIN_SIZE + 2);
  const baseMat = new THREE.MeshStandardMaterial({ color: 0x1a1a2e, roughness: 0.9 });
  const basePlane = new THREE.Mesh(baseGeo, baseMat);
  basePlane.rotation.x = -Math.PI / 2;
  basePlane.position.y = -0.05;
  basePlane.receiveShadow = true;
  scene.add(basePlane);
  // Grid helper
  const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2 + 1, 40, 20, 64, 0x222244, 0x222244);
  gridHelper.position.y = 0.01;
  scene.add(gridHelper);
}
// ============================================================
// Terrain mesh creation and update
// ============================================================
function createTerrainMesh(initialGeo) {
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false
  });
  const mesh = new THREE.Mesh(initialGeo, mat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  scene.add(mesh);
  return mesh;
}
function setTerrainTime(timeIdx) {
  const cachedGeo = getTerrainGeometry(timeIdx);
  if (cachedGeo && terrainMesh) {
    // Dispose old geometry to avoid GPU memory leak
    if (terrainMesh.geometry) terrainMesh.geometry.dispose();
    terrainMesh.geometry = cachedGeo;
  }
  requestRiverRebuild(timeIdx);
}
// ============================================================
// River mesh
// ============================================================
function createRiverMesh() {
  const mat = new THREE.MeshStandardMaterial({
    color: 0xdd4422,
    roughness: 0.3,
    metalness: 0.2,
    emissive: 0x331111,
    emissiveIntensity: 0.4
  });
  const mesh = new THREE.Mesh(new THREE.BufferGeometry(), mat);
  mesh.renderOrder = 1;
  mesh.material.depthTest = true;
  mesh.material.depthWrite = true;
  mesh.visible = false;
  scene.add(mesh);
  return mesh;
}
// ============================================================
// Precompute all terrain geometries (with loading progress)
// ============================================================
async function precomputeTerrains(series) {
  const loadingFill = document.getElementById('loading-bar-fill');
  const loadingText = document.getElementById('loading-text');
  const total = series.length;
  for (let i = 0; i < total; i++) {
    // Yield to main thread every 4 geometries to keep UI responsive
    if (i % 4 === 0 && i > 0) {
      await new Promise(r => setTimeout(r, 0));
    }
    const geo = buildTerrainGeometry(series[i], GRID_SIZE, TERRAIN_SIZE, TERRAIN_SIZE, MAX_HEIGHT, sharedIndices);
    terrainGeometryCache.set(i, geo);
    const pct = Math.round(((i + 1) / total) * 100);
    loadingFill.style.width = pct + '%';
    loadingText.textContent = 'Cached ' + (i + 1) + ' / ' + total + ' geometries';
  }
}
// ============================================================
// Particle update: reuse position array, no per-frame allocations
// ============================================================
function updateParticles(delta) {
  if (!particleSystem || !timeSeriesData[timeIndex]) return;
  const { positions, velocities } = particleSystem;
  const grid = timeSeriesData[timeIndex];
  const halfX = TERRAIN_SIZE / 2;
  const halfZ = TERRAIN_SIZE / 2;
  const count = positions.length / 3;
  const dt = Math.min(delta, 0.1);
  for (let i = 0; i < count; i++) {
    const i3 = i * 3;
    // Apply velocity
    positions[i3] += velocities[i3] * dt;
    positions[i3 + 1] += velocities[i3 + 1] * dt;
    positions[i3 + 2] += velocities[i3 + 2] * dt;
    // Boundary wrap
    if (Math.abs(positions[i3]) > halfX) positions[i3] *= -0.95;
    if (Math.abs(positions[i3 + 2]) > halfZ) positions[i3 + 2] *= -0.95;
    // Terrain-following: clamp Y to terrain height + small offset
    const { col, row } = worldToGrid(positions[i3], positions[i3 + 2]);
    if (col >= 0 && col < GRID_SIZE && row >= 0 && row < GRID_SIZE) {
      const terrainH = grid[row][col].height * MAX_HEIGHT;
      const targetY = terrainH + 0.25 + Math.abs(velocities[i3 + 1]) * 5;
      // Smooth Y toward terrain surface
      positions[i3 + 1] += (targetY - positions[i3 + 1]) * Math.min(dt * 6, 1);
    }
    // Slight random drift in velocity
    velocities[i3] += (Math.random() - 0.5) * 0.015 * dt;
    velocities[i3 + 2] += (Math.random() - 0.5) * 0.015 * dt;
    // Clamp velocity magnitude
    const speed = Math.sqrt(velocities[i3]**2 + velocities[i3+2]**2);
    if (speed > 0.15) {
      const scale = 0.15 / speed;
      velocities[i3] *= scale;
      velocities[i3 + 2] *= scale;
    }
  }
  // Signal Three.js that position buffer was modified in-place
  particleSystem.points.geometry.attributes.position.needsUpdate = true;
}
// ============================================================
// UI event wiring
// ============================================================
function setupUI() {
  const slider = document.getElementById('time-slider');
  slider.max = TIME_STEPS - 1;
  slider.value = 0;
  document.getElementById('time-label').textContent = '0 / ' + (TIME_STEPS - 1);
  slider.addEventListener('input', () => {
    timeIndex = parseInt(slider.value);
    document.getElementById('time-label').textContent = timeIndex + ' / ' + (TIME_STEPS - 1);
    setTerrainTime(timeIndex);
  });
  document.getElementById('btn-play').addEventListener('click', togglePlay);
  document.getElementById('btn-autorot').addEventListener('click', toggleAutoRotate);
  // Bookmark buttons
  for (let i = 0; i < 3; i++) {
    const btn = document.getElementById('btn-bm' + (i + 1));
    btn.addEventListener('click', () => loadBookmark(i));
  }
  // Keyboard shortcuts
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    switch (e.key) {
      case ' ': e.preventDefault(); togglePlay(); break;
      case 'r': case 'R': toggleAutoRotate(); break;
      case '1': loadBookmark(0); break;
      case '2': loadBookmark(1); break;
      case '3': loadBookmark(2); break;
      case 'ArrowLeft': stepTime(-1); break;
      case 'ArrowRight': stepTime(1); break;
    }
  });
  // Resize handler
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
  // Integration: listen for parent dashboard messages
  window.addEventListener('message', (event) => {
    const { command, payload } = event.data || {};
    switch (command) {
      case 'setTime':
        if (typeof payload?.index === 'number') jumpToTime(payload.index);
        break;
      case 'setAutoRotate':
        controls.autoRotate = !!payload?.enabled;
        updateAutoRotateButton();
        break;
      case 'loadBookmark':
        if (typeof payload?.index === 'number') loadBookmark(payload.index);
        break;
      case 'getState':
        event.source.postMessage({
          type: 'terrainExplorerState',
          payload: {
            timeIndex,
            autoRotate: controls.autoRotate,
            cameraPosition: camera.position.toArray(),
            cameraTarget: controls.target.toArray()
          }
        }, event.origin);
        break;
    }
  });
}
function togglePlay() {
  isPlaying = !isPlaying;
  const btn = document.getElementById('btn-play');
  btn.textContent = isPlaying ? '⏸' : '▶';
  btn.classList.toggle('active', isPlaying);
}
function toggleAutoRotate() {
  controls.autoRotate = !controls.autoRotate;
  updateAutoRotateButton();
}
function updateAutoRotateButton() {
  const btn = document.getElementById('btn-autorot');
  btn.classList.toggle('active', controls.autoRotate);
}
function stepTime(delta) {
  timeIndex = Math.max(0, Math.min(TIME_STEPS - 1, timeIndex + delta));
  document.getElementById('time-slider').value = timeIndex;
  document.getElementById('time-label').textContent = timeIndex + ' / ' + (TIME_STEPS - 1);
  setTerrainTime(timeIndex);
}
function jumpToTime(idx) {
  timeIndex = Math.max(0, Math.min(TIME_STEPS - 1, idx));
  document.getElementById('time-slider').value = timeIndex;
  document.getElementById('time-label').textContent = timeIndex + ' / ' + (TIME_STEPS - 1);
  setTerrainTime(timeIndex);
}
function loadBookmark(index) {
  const bm = BOOKMARK_PRESETS[index];
  if (!bm) return;
  // Animate camera to bookmark
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animStep);
    }
  }
  requestAnimationFrame(animStep);
  // Show bookmark label pop
  const label = document.getElementById('bookmark-label');
  label.textContent = bm.label;
  label.classList.add('pop');
  setTimeout(() => label.classList.remove('pop'), 1200);
}
// ============================================================
// Initialize
// ============================================================
async function init() {
  // WebGL support check
  try {
    const testCanvas = document.createElement('canvas');
    const gl = testCanvas.getContext('webgl2') || testCanvas.getContext('webgl');
    if (!gl) throw new Error('No WebGL');
  } catch (e) {
    document.getElementById('loading-overlay').classList.add('hidden');
    document.getElementById('error-overlay').classList.add('visible');
    return;
  }
  setupScene();
  // Generate synthetic time-series data
  timeSeriesData = generateAllTimeSeries(TIME_STEPS, GRID_SIZE);
  // Check for empty data
  if (!timeSeriesData || timeSeriesData.length === 0) {
    document.getElementById('loading-overlay').classList.add('hidden');
    document.getElementById('empty-overlay').classList.add('visible');
    return;
  }
  // Precompute all terrain geometries with progress
  await precomputeTerrains(timeSeriesData);
  // Create terrain mesh with first geometry
  const firstGeo = getTerrainGeometry(0);
  terrainMesh = createTerrainMesh(firstGeo);
  // Create river mesh and trigger initial build
  riverMesh = createRiverMesh();
  requestRiverRebuild(0);
  // Create particle system
  const ps = createParticleSystem(PARTICLE_COUNT, TERRAIN_SIZE, TERRAIN_SIZE, MAX_HEIGHT);
  // Store particle system without the closure
  particleSystem = {
    points: ps.points,
    velocities: ps.velocities,
    positions: ps.positions
  };
  scene.add(particleSystem.points);
  // Setup UI
  setupUI();
  // Hide loading overlay
  document.getElementById('loading-overlay').classList.add('hidden');
  // Signal parent that we're ready (integration)
  window.parent.postMessage({ type: 'terrainExplorerReady', payload: { timeSteps: TIME_STEPS } }, '*');
  // Start render loop
  let lastTime = performance.now();
  function animate(now) {
    requestAnimationFrame(animate);
    const delta = (now - lastTime) / 1000;
    lastTime = now;
    // FPS counter
    diag.frames++;
    if (now - diag.lastFpsTime >= 1000) {
      diag.fps = diag.frames;
      diag.frames = 0;
      diag.lastFpsTime = now;
    }
    // Playback
    if (isPlaying && delta > 0) {
      // Advance time at ~2 steps per second
      const advance = delta * 2;
      // Accumulate fractional steps
      if (!init._playAccum) init._playAccum = 0;
      init._playAccum += advance;
      while (init._playAccum >= 1 && timeIndex < TIME_STEPS - 1) {
        init._playAccum -= 1;
        stepTime(1);
      }
      if (timeIndex >= TIME_STEPS - 1) {
        isPlaying = false;
        document.getElementById('btn-play').textContent = '▶';
        document.getElementById('btn-play').classList.remove('active');
      }
    }
    controls.update();
    updateParticles(delta);
    // Track draw calls (approximate)
    diag.drawCalls = scene.children.length;
    renderer.render(scene, camera);
    updateDiagPanel();
  }
  requestAnimationFrame(animate);
}
// Boot
init().catch((err) => {
  console.error('Init failed:', err);
  document.getElementById('loading-overlay').classList.add('hidden');
  document.getElementById('error-overlay').classList.add('visible');
});
</script>
</body>
</html>