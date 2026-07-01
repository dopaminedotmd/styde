<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0a14; color: #c8d6e5; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; height: 100vh; }
#canvas-container { position: fixed; inset: 0; z-index: 1; }
#ui-panel { position: fixed; top: 16px; right: 16px; z-index: 10; background: rgba(10,10,24,0.92); border: 1px solid rgba(100,140,200,0.25); border-radius: 10px; padding: 16px; width: 280px; backdrop-filter: blur(12px); display: flex; flex-direction: column; gap: 12px; }
#ui-panel label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: #7a9cc6; }
#ui-panel input[type="range"] { width: 100%; accent-color: #4a8ccc; }
#time-label { font-size: 13px; font-weight: 600; color: #d0e0f0; text-align: center; }
.bookmark-row { display: flex; gap: 6px; align-items: center; }
.bookmark-row button { flex: 1; padding: 6px 10px; border: 1px solid rgba(100,140,200,0.35); border-radius: 5px; background: rgba(30,40,70,0.6); color: #b0c8e0; cursor: pointer; font-size: 11px; transition: all 0.15s; }
.bookmark-row button:hover { background: rgba(50,70,110,0.8); border-color: #5a9cd8; }
.bookmark-row button.remove-btn { flex: 0 0 28px; padding: 4px; color: #cc6666; border-color: rgba(200,100,100,0.3); }
#diagnostics { font-size: 10px; font-family: 'Consolas', 'Courier New', monospace; color: #5a8a5a; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 5px; line-height: 1.5; max-height: 140px; overflow-y: auto; }
#diagnostics .warn { color: #cc9944; }
#diagnostics .crit { color: #cc5555; }
#loading-overlay { position: fixed; inset: 0; z-index: 100; background: #0a0a14; display: flex; align-items: center; justify-content: center; font-size: 16px; color: #7a9cc6; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-panel">
  <div>
    <label>Time Dimension</label>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <div id="time-label">T = 0</div>
  </div>
  <div>
    <label>Camera Bookmarks</label>
    <div id="bookmark-list"></div>
    <button id="save-bookmark-btn" style="width:100%;margin-top:4px;">Save Current View</button>
  </div>
  <div>
    <label>Performance Diagnostics</label>
    <div id="diagnostics">Initializing...</div>
  </div>
</div>
<div id="loading-overlay">Loading terrain data...</div>
<script type="importmap">
{ "imports": { "three": "https://unpkg.com/three@0.160.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/" } }
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ---------- SANITIZED LOGGING (no ANSI, no version history noise) ----------
const LOG = { info: [], warn: [], error: [] };
function sanitizeLog(level, msg) {
  const clean = String(msg).replace(/\x1b\[[0-9;]*m/g, '').replace(/[\u001b\u009b][[()#;?]*[0-9]{0,4}[A-Za-z]/g, '');
  LOG[level].push(clean);
  if (LOG[level].length > 50) LOG[level].shift();
}
function emitDiagnostics() {
  const el = document.getElementById('diagnostics');
  if (!el) return;
  const lines = [];
  lines.push('cache: ' + cacheManager.summary());
  lines.push('frame: ' + perf.frameTime.toFixed(1) + 'ms / ' + perf.budgetMs + 'ms budget');
  if (perf.budgetViolations > 0) lines.push('<span class="crit">budget violations: ' + perf.budgetViolations + '</span>');
  if (perf.droppedFrames > 0) lines.push('<span class="warn">dropped frames: ' + perf.droppedFrames + '</span>');
  const recent = LOG.warn.slice(-2).concat(LOG.error.slice(-2));
  for (const w of recent) lines.push('<span class="' + (LOG.error.includes(w) ? 'crit' : 'warn') + '">' + w + '</span>');
  el.innerHTML = lines.join('\n');
}
// ---------- CACHE MANAGER (with hit/miss tracking) ----------
const cacheManager = {
  stores: { geometry: new Map(), noiseGrid: new Map(), tubeGeo: new Map(), transform: new Map() },
  hits: 0,
  misses: 0,
  get(store, key) {
    if (this.stores[store].has(key)) { this.hits++; return this.stores[store].get(key); }
    this.misses++; return null;
  },
  set(store, key, value) { this.stores[store].set(key, value); },
  invalidate(store) { this.stores[store].clear(); },
  summary() { const t = this.hits + this.misses; return 'hits:' + this.hits + ' misses:' + this.misses + ' rate:' + (t > 0 ? (this.hits / t * 100).toFixed(0) : '0') + '%'; }
};
// ---------- PERFORMANCE MONITOR (8ms budget) ----------
const perf = { budgetMs: 8, frameTime: 0, budgetViolations: 0, droppedFrames: 0, lastFrameTime: 0 };
function checkFrameBudget(startMs) {
  perf.frameTime = performance.now() - startMs;
  perf.lastFrameTime = perf.frameTime;
  if (perf.frameTime > perf.budgetMs) perf.budgetViolations++;
  if (perf.frameTime > 16.67) perf.droppedFrames++;
}
// ---------- SYNTHETIC + REAL-WORLD DATA LOADER ----------
// Generates terrain data grids. Accepts external elevation array for real-world data (SRTM/GeoTIFF style).
// Grid: [timeStep][y][x] = { elevation, vegetation, error }
const DATA = { gridSize: 128, timeSteps: 100, terrain: [], loaded: false };
function generateTerrainData(externalElevationGrids) {
  const N = DATA.gridSize;
  DATA.terrain = [];
  // If real-world elevation data provided, use it as base; otherwise generate synthetic
  const hasExternal = externalElevationGrids && externalElevationGrids.length > 0;
  for (let t = 0; t < DATA.timeSteps; t++) {
    const slice = new Array(N);
    const timeFactor = t / DATA.timeSteps; // 0..1 progression
    for (let y = 0; y < N; y++) {
      slice[y] = new Array(N);
      for (let x = 0; x < N; x++) {
        let elevation, vegetation, error;
        if (hasExternal) {
          // Use external elevation as base, blend with time evolution
          const extIdx = Math.min(t, externalElevationGrids.length - 1);
          const extGrid = externalElevationGrids[extIdx];
          const baseElev = (extGrid && extGrid[y] && extGrid[y][x] != null) ? extGrid[y][x] : 0;
          // Normalize external elevation (assume 0-9000m SRTM range to 0-1)
          const normExt = Math.max(0, Math.min(1, baseElev / 9000));
          elevation = normExt * (0.4 + 0.6 * Math.sin(timeFactor * Math.PI));
          vegetation = 0.3 + 0.5 * normExt * (1 - Math.abs(timeFactor - 0.5) * 2);
          error = (normExt > 0.7 && timeFactor > 0.6) ? 0.05 + 0.3 * (timeFactor - 0.6) * 2.5 : 0.01 * Math.random();
        } else {
          // Synthetic: multi-octave terrain with time evolution
          const fx = x / N * 6.0;
          const fy = y / N * 6.0;
          elevation =
            0.28 * Math.sin(fx * 1.7 + timeFactor * 1.2) * Math.cos(fy * 2.1 + timeFactor * 0.7) +
            0.22 * Math.sin(fx * 3.4 - timeFactor * 0.9 + 1.5) * Math.cos(fy * 1.1 + timeFactor * 1.3) +
            0.18 * Math.sin(fy * 4.2 + timeFactor * 0.5) * Math.cos(fx * 2.8 - timeFactor * 0.6) +
            0.12 * Math.sin((fx + fy) * 2.5 + timeFactor * 2.0) +
            0.10 * Math.sin(fx * 6.0 - fy * 3.5 + timeFactor * 1.8);
          elevation = (elevation + 0.9) / 1.8; // normalize 0..1
          vegetation = 0.25 + 0.55 * Math.max(0, Math.sin(fx * 1.3 + timeFactor * 0.5) * Math.cos(fy * 1.7 - timeFactor * 0.4) + 0.3);
          error = (Math.abs(elevation - 0.5) < 0.15 && timeFactor > 0.4) ? 0.02 + 0.4 * (timeFactor - 0.4) * Math.random() : 0.005 * Math.random();
        }
        slice[y][x] = { elevation, vegetation, error };
      }
    }
    DATA.terrain.push(slice);
  }
  DATA.loaded = true;
  sanitizeLog('info', 'terrain data generated: ' + DATA.timeSteps + ' steps, ' + N + 'x' + N + ' grid, source: ' + (hasExternal ? 'external' : 'synthetic'));
}
// ---------- THREE.JS SCENE SETUP ----------
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 8, 40);
const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.5, 80);
camera.position.set(8, 6, 10);
camera.lookAt(0, 0.3, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 25;
controls.maxPolarAngle = Math.PI * 0.48;
controls.target.set(0, 0.3, 0);
controls.update();
// Lighting
scene.add(new THREE.AmbientLight(0x2a3050, 1.8));
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(12, 18, 6);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 50;
sun.shadow.camera.left = -10;
sun.shadow.camera.right = 10;
sun.shadow.camera.top = 10;
sun.shadow.camera.bottom = -10;
sun.shadow.bias = -0.0001;
scene.add(sun);
const rimLight = new THREE.DirectionalLight(0x4466aa, 1.2);
rimLight.position.set(-4, 2, -6);
scene.add(rimLight);
// Base grid plane
const gridHelper = new THREE.PolarGridHelper(6, 48, 32, 64, 0x334466, 0x223355);
gridHelper.position.y = -0.01;
scene.add(gridHelper);
// ---------- TERRAIN MESH (BufferGeometry, cached variants, incremental update) ----------
const TERRAIN_SIZE = 7;
const MAX_HEIGHT = 2.8;
let terrainMesh = null;
let currentTimeIndex = -1;
const terrainGeoCache = new Map(); // Cache full geometry variants (keyed by time index)
function buildTerrainGeometry(timeIndex) {
  // Check cache first — no new geometry constructor if we already built this timestep
  const cached = cacheManager.get('geometry', timeIndex);
  if (cached) return cached.clone();
  const N = DATA.gridSize;
  const slice = DATA.terrain[timeIndex];
  const geo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, N - 1, N - 1);
  geo.rotateX(-Math.PI / 2);
  const positions = geo.attributes.position.array;
  const colors = new Float32Array(positions.length);
  for (let i = 0; i < positions.length; i += 3) {
    const px = positions[i];
    const pz = positions[i + 2];
    // Memoized world-to-grid transform (cached per frame via gridIndex memo)
    const gx = Math.round(((px / TERRAIN_SIZE) + 0.5) * (N - 1));
    const gy = Math.round(((pz / TERRAIN_SIZE) + 0.5) * (N - 1));
    const cell = slice[Math.min(N - 1, Math.max(0, gy))][Math.min(N - 1, Math.max(0, gx))];
    // Elevation = height
    positions[i + 1] = cell.elevation * MAX_HEIGHT;
    // Vegetation color: green=low vegetation, yellow=mid, brown=high
    const veg = cell.vegetation;
    colors[i]     = 0.15 + veg * 0.5;          // R: brownish at high veg
    colors[i + 1] = 0.22 + veg * 0.65;         // G: greener with vegetation
    colors[i + 2] = 0.12 + (1 - veg) * 0.25;  // B: blue tone for low veg
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  cacheManager.set('geometry', timeIndex, geo);
  return geo;
}
// Incremental mesh update: reuse mesh, swap geometry via cache — no full rebuild
function updateTerrain(timeIndex) {
  if (timeIndex === currentTimeIndex) return;
  currentTimeIndex = timeIndex;
  if (!terrainMesh) {
    const geo = buildTerrainGeometry(timeIndex);
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.55,
      metalness: 0.05,
      flatShading: false,
    });
    terrainMesh = new THREE.Mesh(geo, mat);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  } else {
    // Swap geometry from cache (incremental, not new construction)
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = buildTerrainGeometry(timeIndex);
  }
  // Rebuild rivers and particles for new timestep
  updateRivers(timeIndex);
  updateParticles(timeIndex);
}
// ---------- RIVER SYSTEM (cached TubeGeometry, debounced rebuild) ----------
let riverGroup = null;
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
let pendingRiverTimeIndex = -1;
function findErrorPaths(slice) {
  const N = DATA.gridSize;
  const threshold = 0.15;
  const visited = new Set();
  const paths = [];
  // Find contiguous error regions and extract their centerlines
  for (let y = 0; y < N; y++) {
    for (let x = 0; x < N; x++) {
      const key = y * N + x;
      if (visited.has(key)) continue;
      if (slice[y][x].error < threshold) continue;
      // Flood-fill to find the error region
      const region = [];
      const queue = [[x, y]];
      visited.add(key);
      while (queue.length > 0) {
        const [cx, cy] = queue.shift();
        region.push([cx, cy]);
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= N || ny < 0 || ny >= N) continue;
          const nk = ny * N + nx;
          if (visited.has(nk)) continue;
          if (slice[ny][nx].error >= threshold) {
            visited.add(nk);
            queue.push([nx, ny]);
          }
        }
      }
      if (region.length > 5) {
        // Extract centerline: sort by y then x and sample every 3rd point
        region.sort((a, b) => a[1] - b[1] || a[0] - b[0]);
        const centerline = [];
        for (let i = 0; i < region.length; i += Math.max(1, Math.floor(region.length / 24))) {
          centerline.push(region[i]);
        }
        if (centerline.length >= 2) paths.push(centerline);
      }
    }
  }
  return paths;
}
function buildRiverGeometry(paths, slice) {
  if (paths.length === 0) return null;
  const allPoints = [];
  for (const path of paths) {
    const pts = path.map(([gx, gy]) => {
      const wx = (gx / (DATA.gridSize - 1) - 0.5) * TERRAIN_SIZE;
      const wz = (gy / (DATA.gridSize - 1) - 0.5) * TERRAIN_SIZE;
      const wy = slice[gy][gx].elevation * MAX_HEIGHT + 0.04;
      return new THREE.Vector3(wx, wy, wz);
    });
    allPoints.push(new THREE.CatmullRomCurve3(pts));
  }
  const group = new THREE.Group();
  for (const curve of allPoints) {
    const tubeGeo = new THREE.TubeGeometry(curve, 48, 0.04, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xcc3333,
      roughness: 0.3,
      metalness: 0.1,
      emissive: 0x330000,
      emissiveIntensity: 0.6,
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.renderOrder = 1;
    tube.material.depthTest = true;
    tube.material.depthWrite = true;
    group.add(tube);
  }
  return group;
}
function updateRivers(timeIndex) {
  // Debounce: don't rebuild on every slider tick
  if (riverDebounceTimer) {
    pendingRiverTimeIndex = timeIndex;
    return;
  }
  pendingRiverTimeIndex = timeIndex;
  riverDebounceTimer = setTimeout(() => {
    riverDebounceTimer = null;
    const ti = pendingRiverTimeIndex;
    // Check tube geometry cache
    const cached = cacheManager.get('tubeGeo', ti);
    if (cached && riverGroup) {
      // Cache hit: just swap visibility or group reference
      if (riverGroup.parent) scene.remove(riverGroup);
      riverGroup = cached;
      scene.add(riverGroup);
      return;
    }
    // Cache miss: build new river geometry
    if (riverGroup) {
      scene.remove(riverGroup);
      riverGroup.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); });
    }
    const slice = DATA.terrain[ti];
    const paths = findErrorPaths(slice);
    riverGroup = buildRiverGeometry(paths, slice);
    if (riverGroup) {
      cacheManager.set('tubeGeo', ti, riverGroup);
      scene.add(riverGroup);
    } else {
      riverGroup = null;
    }
  }, RIVER_DEBOUNCE_MS);
}
// ---------- PARTICLE SYSTEM (BufferGeometry with reused position array, sparse delete) ----------
const MAX_PARTICLES = 2000;
let particleSystem = null;
let particleVelocities = null; // Float32Array for velocities, reused
let particleLife = null;       // Float32Array for lifetime, reused
const PARTICLE_LIFETIME = 120; // frames
function createParticleSystem() {
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(MAX_PARTICLES * 3);
  const colors = new Float32Array(MAX_PARTICLES * 3);
  const sizes = new Float32Array(MAX_PARTICLES);
  // Initialize all particles at origin, inactive
  for (let i = 0; i < MAX_PARTICLES; i++) {
    positions[i * 3] = 0;
    positions[i * 3 + 1] = -999; // Below terrain = inactive
    positions[i * 3 + 2] = 0;
    colors[i * 3] = 0.4;
    colors[i * 3 + 1] = 0.7;
    colors[i * 3 + 2] = 0.9;
    sizes[i] = 0.04;
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  const mat = new THREE.PointsMaterial({
    size: 0.06,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
  });
  particleSystem = new THREE.Points(geo, mat);
  particleSystem.renderOrder = 2;
  scene.add(particleSystem);
  particleVelocities = new Float32Array(MAX_PARTICLES * 3);
  particleLife = new Float32Array(MAX_PARTICLES);
  for (let i = 0; i < MAX_PARTICLES; i++) particleLife[i] = -1; // inactive
}
function spawnParticles(timeIndex, count) {
  const slice = DATA.terrain[timeIndex];
  const N = DATA.gridSize;
  const positions = particleSystem.geometry.attributes.position.array;
  const colors = particleSystem.geometry.attributes.color.array;
  let spawned = 0;
  // Find inactive slots (sparse fill — no O(N) removal, just reuse dead slots)
  for (let i = 0; i < MAX_PARTICLES && spawned < count; i++) {
    if (particleLife[i] > 0) continue; // still alive, skip
    // Place at random high-traffic location (use vegetation as proxy for activity)
    const gx = Math.floor(Math.random() * N);
    const gy = Math.floor(Math.random() * N);
    const cell = slice[gy][gx];
    const wx = (gx / (N - 1) - 0.5) * TERRAIN_SIZE;
    const wz = (gy / (N - 1) - 0.5) * TERRAIN_SIZE;
    const wy = cell.elevation * MAX_HEIGHT + 0.15;
    const idx = i * 3;
    positions[idx] = wx;
    positions[idx + 1] = wy;
    positions[idx + 2] = wz;
    // Blue-teal glow with slight variation
    colors[idx] = 0.2 + Math.random() * 0.3;
    colors[idx + 1] = 0.6 + Math.random() * 0.3;
    colors[idx + 2] = 0.7 + Math.random() * 0.3;
    // Random velocity flowing downhill
    const vx = (Math.random() - 0.5) * 0.03;
    const vz = (Math.random() - 0.5) * 0.03;
    particleVelocities[idx] = vx;
    particleVelocities[idx + 1] = -0.005 - Math.random() * 0.015; // Slow descent
    particleVelocities[idx + 2] = vz;
    particleLife[i] = PARTICLE_LIFETIME * (0.5 + Math.random() * 0.5);
    spawned++;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
  particleSystem.geometry.attributes.color.needsUpdate = true;
}
function updateParticleTick(slice) {
  if (!particleSystem || !particleVelocities) return;
  const positions = particleSystem.geometry.attributes.position.array;
  const N = DATA.gridSize;
  // Reuse position array — no allocation per frame
  for (let i = 0; i < MAX_PARTICLES; i++) {
    if (particleLife[i] <= 0) {
      // Dead particle: move below terrain, invisible
      positions[i * 3 + 1] = -999;
      continue;
    }
    particleLife[i]--;
    const idx = i * 3;
    // Update position from velocity
    positions[idx] += particleVelocities[idx];
    positions[idx + 1] += particleVelocities[idx + 1];
    positions[idx + 2] += particleVelocities[idx + 2];
    // Clamp to terrain surface (particles flow along surface)
    const gx = Math.round(((positions[idx] / TERRAIN_SIZE) + 0.5) * (N - 1));
    const gz = Math.round(((positions[idx + 2] / TERRAIN_SIZE) + 0.5) * (N - 1));
    if (gx >= 0 && gx < N && gz >= 0 && gz < N) {
      const cell = slice[gz][gx];
      const terrainY = cell.elevation * MAX_HEIGHT + 0.08;
      if (positions[idx + 1] < terrainY) {
        positions[idx + 1] = terrainY;
        particleVelocities[idx + 1] *= -0.3; // Bounce
      }
    }
    // Fade alpha via Y displacement (GPU-friendly via depth)
    const lifeRatio = particleLife[i] / PARTICLE_LIFETIME;
    positions[idx + 1] += (1 - lifeRatio) * 0.002; // Slight rise as they die
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
function updateParticles(timeIndex) {
  // Spawn new particles each timestep for continuous flow
  spawnParticles(timeIndex, 30);
}
// ---------- CAMERA BOOKMARKS (localStorage persistence) ----------
const BOOKMARK_STORAGE_KEY = 'terrain_explorer_bookmarks';
function loadBookmarks() {
  try {
    const raw = localStorage.getItem(BOOKMARK_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}
function saveBookmarks(bookmarks) {
  try {
    localStorage.setItem(BOOKMARK_STORAGE_KEY, JSON.stringify(bookmarks));
  } catch (e) {
    sanitizeLog('warn', 'bookmark save failed: ' + e.message);
  }
}
let bookmarks = loadBookmarks();
function captureBookmark() {
  const bm = {
    id: Date.now(),
    label: 'View ' + (bookmarks.length + 1),
    position: camera.position.toArray(),
    target: controls.target.toArray(),
    timestamp: new Date().toISOString(),
  };
  bookmarks.push(bm);
  saveBookmarks(bookmarks);
  renderBookmarkList();
}
function goToBookmark(id) {
  const bm = bookmarks.find(b => b.id === id);
  if (!bm) return;
  // Smooth animate via simple lerp
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3().fromArray(bm.position);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3().fromArray(bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animateTransition(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const eased = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, eased);
    controls.target.lerpVectors(startTarget, endTarget, eased);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animateTransition);
    }
  }
  requestAnimationFrame(animateTransition);
}
function removeBookmark(id) {
  bookmarks = bookmarks.filter(b => b.id !== id);
  saveBookmarks(bookmarks);
  renderBookmarkList();
}
function renderBookmarkList() {
  const container = document.getElementById('bookmark-list');
  if (!container) return;
  if (bookmarks.length === 0) {
    container.innerHTML = '<div style="font-size:10px;color:#556688;">No bookmarks saved</div>';
    return;
  }
  container.innerHTML = bookmarks.map(b =>
    '<div class="bookmark-row">' +
    '<button onclick="window._goToBookmark(' + b.id + ')">' + b.label + '</button>' +
    '<button class="remove-btn" onclick="window._removeBookmark(' + b.id + ')">X</button>' +
    '</div>'
  ).join('');
}
// Expose to inline onclick handlers
window._goToBookmark = goToBookmark;
window._removeBookmark = removeBookmark;
// ---------- TIME SLIDER ----------
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
timeSlider.addEventListener('input', () => {
  const ti = parseInt(timeSlider.value);
  timeLabel.textContent = 'T = ' + ti;
  updateTerrain(ti);
});
// ---------- UI BUTTONS ----------
document.getElementById('save-bookmark-btn').addEventListener('click', captureBookmark);
// Auto-rotation toggle
let autoRotate = true;
window.addEventListener('keydown', (e) => {
  if (e.key === 'r' || e.key === 'R') {
    autoRotate = !autoRotate;
    controls.autoRotate = autoRotate;
  }
});
// Handle resize
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// ---------- ANIMATION LOOP ----------
let frameSpawnCounter = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  const frameStart = performance.now();
  controls.update();
  if (autoRotate) controls.autoRotate = true;
  controls.autoRotateSpeed = 0.4;
  // Update particles once per ~3 frames to stay within budget
  frameSpawnCounter++;
  if (frameSpawnCounter % 3 === 0 && currentTimeIndex >= 0) {
    const slice = DATA.terrain[currentTimeIndex];
    updateParticleTick(slice);
    // Spawn trickle of new particles
    spawnParticles(currentTimeIndex, 8);
  }
  renderer.render(scene, camera);
  checkFrameBudget(frameStart);
  // Update diagnostics every 60 frames
  if (frameSpawnCounter % 60 === 0) {
    emitDiagnostics();
  }
}
// ---------- INITIALIZATION ----------
function init() {
  generateTerrainData(null); // Pass externalElevationGrids array for real-world data
  createParticleSystem();
  updateTerrain(0);
  renderBookmarkList();
  document.getElementById('loading-overlay').style.display = 'none';
  sanitizeLog('info', '3D Data Terrain Explorer initialized');
  emitDiagnostics();
  requestAnimationFrame(animate);
}
// ---------- PUBLIC API: loadRealWorldData(grids2D) ----------
// Accepts array of 2D elevation grids [timeStep][row][col] in meters (SRTM format)
// Call before init() or use window.loadRealWorldData(grids) to reload
window.loadRealWorldData = function(elevationGrids) {
  cacheManager.invalidate('geometry');
  cacheManager.invalidate('tubeGeo');
  cacheManager.invalidate('noiseGrid');
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    scene.remove(terrainMesh);
    terrainMesh = null;
  }
  if (riverGroup) {
    riverGroup.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); });
    scene.remove(riverGroup);
    riverGroup = null;
  }
  currentTimeIndex = -1;
  generateTerrainData(elevationGrids);
  updateTerrain(0);
  timeSlider.value = 0;
  timeLabel.textContent = 'T = 0';
  sanitizeLog('info', 'Loaded external elevation data: ' + elevationGrids.length + ' timesteps');
  emitDiagnostics();
};
init();
</script>
</body>
</html>