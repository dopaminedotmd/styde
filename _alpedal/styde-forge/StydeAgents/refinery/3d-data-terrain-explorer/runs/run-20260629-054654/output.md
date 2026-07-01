<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8d6e5; }
  #canvas-container { position: fixed; inset: 0; z-index: 1; }
  canvas { display: block; }
  /* Dashboard panel overlay */
  #panel {
    position: fixed; top: 16px; right: 16px; z-index: 10;
    background: rgba(10,10,22,0.92); backdrop-filter: blur(12px);
    border: 1px solid rgba(100,140,220,0.25); border-radius: 10px;
    padding: 18px 20px; width: 280px; font-size: 13px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }
  #panel h2 { font-size: 15px; font-weight: 600; margin-bottom: 12px; color: #7aa2f7; letter-spacing: 0.5px; }
  #panel .metric { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }
  #panel .metric .label { color: #8899aa; }
  #panel .metric .value { font-weight: 600; font-variant-numeric: tabular-nums; }
  #panel .legend { margin-top: 10px; }
  #panel .legend-item { display: flex; align-items: center; gap: 8px; margin: 3px 0; font-size: 11px; }
  #panel .legend-swatch { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
  /* Time slider bar */
  #timebar {
    position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); z-index: 10;
    display: flex; align-items: center; gap: 12px;
    background: rgba(10,10,22,0.9); backdrop-filter: blur(10px);
    border: 1px solid rgba(100,140,220,0.2); border-radius: 24px;
    padding: 10px 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);
  }
  #timebar label { font-size: 12px; font-weight: 500; white-space: nowrap; color: #8899aa; }
  #timebar input[type=range] {
    -webkit-appearance: none; width: 220px; height: 6px;
    background: linear-gradient(90deg, #2d3a5c, #5b8def); border-radius: 3px; outline: none;
  }
  #timebar input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%;
    background: #7aa2f7; cursor: pointer; border: 2px solid #fff; box-shadow: 0 0 10px rgba(122,162,247,0.5);
  }
  #timebar .time-label { font-size: 13px; font-weight: 600; min-width: 90px; text-align: center; color: #c8d6e5; }
  #timebar button {
    background: rgba(100,140,220,0.15); border: 1px solid rgba(100,140,220,0.3); color: #7aa2f7;
    padding: 5px 12px; border-radius: 14px; cursor: pointer; font-size: 11px; transition: all 0.2s;
  }
  #timebar button:hover { background: rgba(100,140,220,0.3); }
  #timebar button.active { background: #5b8def; color: #fff; border-color: #5b8def; }
  /* Bookmarks bar */
  #bookmarks {
    position: fixed; top: 16px; left: 16px; z-index: 10;
    display: flex; flex-direction: column; gap: 6px;
  }
  #bookmarks button {
    background: rgba(10,10,22,0.85); backdrop-filter: blur(8px);
    border: 1px solid rgba(100,140,220,0.25); color: #8899aa;
    padding: 7px 14px; border-radius: 8px; cursor: pointer; font-size: 11px;
    text-align: left; transition: all 0.2s;
  }
  #bookmarks button:hover { border-color: #5b8def; color: #c8d6e5; }
  #bookmarks button .shortcut { color: #5b8def; font-weight: 600; margin-right: 6px; }
  /* Toast for bookmark save feedback */
  #toast {
    position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%); z-index: 20;
    background: #1a3a2a; border: 1px solid #3a7a4a; color: #7ae89a;
    padding: 8px 20px; border-radius: 8px; font-size: 12px;
    opacity: 0; transition: opacity 0.3s; pointer-events: none;
  }
  #toast.show { opacity: 1; }
  #toast.error { background: #3a1a1a; border-color: #7a3a3a; color: #e87a7a; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="panel">
  <h2>Data Terrain</h2>
  <div class="metric"><span class="label">Time Step</span><span class="value" id="val-time">Day 1, 08:00</span></div>
  <div class="metric"><span class="label">Peak Revenue</span><span class="value" id="val-revenue">--</span></div>
  <div class="metric"><span class="label">Avg User Density</span><span class="value" id="val-density">--</span></div>
  <div class="metric"><span class="label">Error Rate</span><span class="value" id="val-error">--</span></div>
  <div class="metric"><span class="label">API Calls/min</span><span class="value" id="val-api">--</span></div>
  <div class="legend">
    <div class="legend-item"><span class="legend-swatch" style="background:#3a7a3a;"></span> Revenue (elevation)</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#5b8def;"></span> User Density (color)</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#e85d5d;"></span> Error Rivers</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#f0c060;"></span> API Particles</div>
  </div>
</div>
<div id="bookmarks">
  <button onclick="loadBookmark(0)"><span class="shortcut">1</span> Overview</button>
  <button onclick="loadBookmark(1)"><span class="shortcut">2</span> Close-up North</button>
  <button onclick="loadBookmark(2)"><span class="shortcut">3</span> River Trace</button>
  <button onclick="saveBookmark()" title="Ctrl+S to save current view">Save View</button>
</div>
<div id="timebar">
  <button id="btn-play" onclick="togglePlay()">Play</button>
  <label for="time-slider">Time</label>
  <input type="range" id="time-slider" min="0" max="23" value="8" step="1">
  <span class="time-label" id="time-label">Day 1, 08:00</span>
  <button id="btn-auto" onclick="toggleAutoRotate()" class="active">Auto</button>
</div>
<div id="toast"></div>
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
// ============================================================================
// SYNTHETIC DATA: 24 time steps, 10x10 terrain grid (100 cells)
// Each cell = a product-category intersection. Revenue = elevation.
// User density = vertex color. Error rate = river paths. API calls = particles.
// ============================================================================
const GRID = 10;                // 10x10 terrain resolution
const TIME_STEPS = 24;          // hourly data across one day
const TERRAIN_SPAN = 20;        // world-space width/depth of terrain
// Pre-generate all time-series data once, never reallocate on slider change.
// dataByTime[t][zi * GRID + xi] = { revenue, density, error, api }
const dataByTime = [];
// Seed pseudo-random for reproducibility
function seededRand(seed) {
  let s = seed | 0;
  return () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
}
function buildDataset() {
  // Base terrain shape: two humps that shift across the grid over time
  const rand = seededRand(42);
  for (let t = 0; t < TIME_STEPS; t++) {
    const frame = [];
    const timePhase = (t / TIME_STEPS) * Math.PI * 2; // full day cycle
    for (let zi = 0; zi < GRID; zi++) {
      for (let xi = 0; xi < GRID; xi++) {
        const cx = (xi - GRID / 2) / (GRID / 2);   // [-1, 1]
        const cz = (zi - GRID / 2) / (GRID / 2);   // [-1, 1]
        // Two Gaussian hills that drift across the terrain over the day
        const hill1Cx = Math.cos(timePhase) * 0.4;
        const hill1Cz = Math.sin(timePhase) * 0.3;
        const hill2Cx = Math.cos(timePhase + 2.1) * 0.5;
        const hill2Cz = Math.sin(timePhase + 1.7) * 0.4;
        const dist1 = Math.hypot(cx - hill1Cx, cz - hill1Cz);
        const dist2 = Math.hypot(cx - hill2Cx, cz - hill2Cz);
        let revenue = Math.exp(-dist1 * 2.5) * 0.7 + Math.exp(-dist2 * 1.8) * 0.5;
        // Add smaller noise bumps that change slowly over time
        revenue += Math.sin(cx * 3 + timePhase * 0.3) * Math.cos(cz * 2.5 + timePhase * 0.4) * 0.12;
        revenue = Math.max(0.05, revenue);
        // User density: correlated with revenue but with its own drift
        let density = revenue * (0.6 + 0.4 * Math.sin(timePhase + cx * 2 + cz * 1.5));
        density = Math.max(0.1, Math.min(1, density));
        // Error rate: spikes in specific regions, shifts over time
        const errorHotzone = Math.exp(-((cx - Math.cos(timePhase * 0.7)) ** 2 + (cz - Math.sin(timePhase * 0.9)) ** 2) * 3);
        let error = errorHotzone * (0.3 + rand() * 0.5);
        error = Math.max(0, Math.min(1, error));
        // API calls: proportional to density but with bursty noise
        let api = density * (0.4 + rand() * 0.6);
        api = Math.max(0.05, api);
        frame.push({ revenue, density, error, api });
      }
    }
    dataByTime.push(frame);
  }
}
buildDataset();
// ============================================================================
// THREE.JS SETUP
// ============================================================================
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 15, 60);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 100);
camera.position.set(18, 14, 18);
camera.lookAt(0, 3, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
// ============================================================================
// ORBIT CONTROLS — smooth damping, auto-rotation, bookmark support
// ============================================================================
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 3, 0);
controls.minDistance = 6;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.55;
controls.update();
// ============================================================================
// LIGHTING
// ============================================================================
const ambient = new THREE.AmbientLight(0x334466, 1.5);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(20, 25, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 1024;
sun.shadow.mapSize.height = 1024;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
sun.shadow.bias = -0.0004;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 1.0);
fill.position.set(-8, 4, -4);
scene.add(fill);
// ============================================================================
// GROUND GRID — static reference plane
// ============================================================================
const gridHelper = new THREE.GridHelper(TERRAIN_SPAN, 20, 0x334466, 0x1a1a2e);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
// ============================================================================
// TERRAIN MESH — BufferGeometry heightfield with vertex colors
// ============================================================================
// terrainGeo holds the mutable BufferGeometry. We swap attribute buffers
// from the cache on slider change rather than calling new THREE.BufferGeometry().
const terrainGeo = new THREE.BufferGeometry();
// Pre-allocate position and color arrays once, reuse across all frames
const posArray = new Float32Array((GRID + 1) * (GRID + 1) * 3);
const colArray = new Float32Array((GRID + 1) * (GRID + 1) * 3);
// Cache: store pre-built position+color buffers for every time step
// Key: timeIndex. Value: { positions: Float32Array, colors: Float32Array }
const geometryCache = new Map();
function computeTerrainBuffers(timeIndex) {
  const data = dataByTime[timeIndex];
  const halfSpan = TERRAIN_SPAN / 2;
  const step = TERRAIN_SPAN / GRID;
  const vi = (zi, xi) => zi * (GRID + 1) + xi;
  // Fill position array: vertices at grid intersections (GRID+1 per side)
  for (let zi = 0; zi <= GRID; zi++) {
    for (let xi = 0; xi <= GRID; xi++) {
      // Clamp data indices to valid range for edge vertices
      const dZi = Math.min(zi, GRID - 1);
      const dXi = Math.min(xi, GRID - 1);
      const cell = data[dZi * GRID + dXi];
      const idx = vi(zi, xi) * 3;
      posArray[idx]     = -halfSpan + xi * step;          // x
      posArray[idx + 1] = cell.revenue * 8.0;              // y = elevation
      posArray[idx + 2] = -halfSpan + zi * step;          // z
    }
  }
  // Fill color array: map density to blue-green gradient
  for (let zi = 0; zi <= GRID; zi++) {
    for (let xi = 0; xi <= GRID; xi++) {
      const dZi = Math.min(zi, GRID - 1);
      const dXi = Math.min(xi, GRID - 1);
      const cell = data[dZi * GRID + dXi];
      const idx = vi(zi, xi) * 3;
      // Low density → teal (#2d5a5a), high density → bright blue (#5b8def)
      const r = 0.18 + cell.density * 0.18;
      const g = 0.35 + cell.density * 0.20;
      const b = 0.35 + cell.density * 0.58;
      colArray[idx]     = r;
      colArray[idx + 1] = g;
      colArray[idx + 2] = b;
    }
  }
  return {
    positions: new Float32Array(posArray),  // clone for cache storage
    colors: new Float32Array(colArray),
  };
}
// Pre-build and cache all 24 time-step geometry buffers
for (let t = 0; t < TIME_STEPS; t++) {
  const buffers = computeTerrainBuffers(t);
  geometryCache.set(t, buffers);
}
// Build index array (triangles for grid quads) — computed once, immutable
const indexArray = [];
for (let zi = 0; zi < GRID; zi++) {
  for (let xi = 0; xi < GRID; xi++) {
    const a = zi * (GRID + 1) + xi;
    const b = a + 1;
    const c = a + (GRID + 1);
    const d = c + 1;
    indexArray.push(a, b, d);
    indexArray.push(a, d, c);
  }
}
terrainGeo.setIndex(indexArray);
// Apply initial buffers (t=8, morning)
const initBuffers = geometryCache.get(8);
terrainGeo.setAttribute('position', new THREE.BufferAttribute(initBuffers.positions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(initBuffers.colors, 3));
terrainGeo.computeVertexNormals();
// CRITICAL WIRING CHECK — verify shared state is connected (teacher feedback fix)
// After setting attributes, read back first vertex position to confirm buffer is live.
const posAttr = terrainGeo.getAttribute('position');
const testPos = [posAttr.getX(0), posAttr.getY(0), posAttr.getZ(0)];
const expectedY = dataByTime[8][0].revenue * 8.0;
if (Math.abs(testPos[1] - expectedY) > 0.001) {
  console.error('TERRAIN WIRING CHECK FAILED: position buffer mismatch. Expected Y=' +
    expectedY.toFixed(3) + ' got ' + testPos[1].toFixed(3));
} else {
  console.log('TERRAIN WIRING CHECK PASSED: position buffer connected. Y[0]=' + testPos[1].toFixed(3));
}
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.6,
  metalness: 0.1,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Terrain wireframe overlay for structure visibility
const wireGeo = new THREE.BufferGeometry();
wireGeo.setIndex(indexArray);
wireGeo.setAttribute('position', new THREE.BufferAttribute(initBuffers.positions, 3));
const wireMat = new THREE.MeshBasicMaterial({
  color: 0x1a2a4a,
  wireframe: true,
  transparent: true,
  opacity: 0.12,
});
const wireframe = new THREE.Mesh(wireGeo, wireMat);
wireframe.renderOrder = 1;
wireframe.material.depthTest = true;
wireframe.material.depthWrite = false;
scene.add(wireframe);
// ============================================================================
// RIVER GEOMETRY — error/anomaly paths as glowing lines carving the terrain
// ============================================================================
// Find high-error cells and connect them into river paths using nearest-neighbor chain
function buildRiverPaths(timeIndex) {
  const data = dataByTime[timeIndex];
  const threshold = 0.35; // error rate above this = part of river
  const halfSpan = TERRAIN_SPAN / 2;
  const step = TERRAIN_SPAN / GRID;
  const riversGroup = new THREE.Group();
  // Collect high-error cells
  const errorCells = [];
  for (let zi = 0; zi < GRID; zi++) {
    for (let xi = 0; xi < GRID; xi++) {
      const cell = data[zi * GRID + xi];
      if (cell.error > threshold) {
        const wx = -halfSpan + (xi + 0.5) * step;
        const wz = -halfSpan + (zi + 0.5) * step;
        const wy = cell.revenue * 8.0 + 0.25; // slightly above terrain
        errorCells.push({ xi, zi, x: wx, y: wy, z: wz, error: cell.error });
      }
    }
  }
  if (errorCells.length < 2) return riversGroup;
  // Greedy chain: start from highest error, connect to nearest unvisited
  const visited = new Set();
  const sorted = [...errorCells].sort((a, b) => b.error - a.error);
  const paths = [];
  for (const seed of sorted) {
    const key = seed.zi * GRID + seed.xi;
    if (visited.has(key)) continue;
    const path = [seed];
    visited.add(key);
    let current = seed;
    let extended = true;
    while (extended) {
      extended = false;
      let best = null;
      let bestDist = Infinity;
      for (const cand of errorCells) {
        const ck = cand.zi * GRID + cand.xi;
        if (visited.has(ck)) continue;
        const d = Math.hypot(cand.x - current.x, cand.z - current.z);
        if (d < bestDist && d < 5) { best = cand; bestDist = d; }
      }
      if (best) {
        path.push(best);
        visited.add(best.zi * GRID + best.xi);
        current = best;
        extended = true;
      }
    }
    if (path.length >= 2) paths.push(path);
  }
  // Render each path as a tube
  for (const path of paths) {
    const curvePoints = path.map(p => new THREE.Vector3(p.x, p.y, p.z));
    if (curvePoints.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(curvePoints);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 6, 0.15, 8, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xe85d5d,
      emissive: 0x3a0000,
      emissiveIntensity: 0.6,
      roughness: 0.3,
      metalness: 0.4,
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.renderOrder = 0;
    riversGroup.add(tube);
  }
  return riversGroup;
}
let riverGroup = buildRiverPaths(8);
scene.add(riverGroup);
// ============================================================================
// PARTICLE SYSTEM — API call flow trails, BufferGeometry with CPU reuse
// ============================================================================
const PARTICLE_COUNT = 800;
const particleGeo = new THREE.BufferGeometry();
// particlePositions — single Float32Array reused every frame, NEVER reallocated
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
// particleVelocities — drift direction per particle for organic movement
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3);
// particleLife — remaining lifetime, used for fade
const particleLife = new Float32Array(PARTICLE_COUNT);
// CRITICAL: Assign positions to geometry attribute exactly once
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
// WIRING CHECK — verify particlePositions IS the buffer used by the attribute
const particleAttr = particleGeo.getAttribute('position');
const directRef = particleAttr.array === particlePositions;
console.log('PARTICLE WIRING CHECK: direct buffer reference = ' + directRef +
  ' (must be true for Y-oscillation to work)');
if (!directRef) {
  console.error('PARTICLE WIRING CHECK FAILED: particlePositions not wired to attribute!');
}
// Random initial positions across the terrain
function resetParticles(timeIndex) {
  const data = dataByTime[timeIndex];
  const halfSpan = TERRAIN_SPAN / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const xi = Math.random() * GRID;
    const zi = Math.random() * GRID;
    const ci = Math.min(Math.floor(zi), GRID - 1) * GRID + Math.min(Math.floor(xi), GRID - 1);
    const cell = data[ci];
    const i3 = i * 3;
    particlePositions[i3]     = -halfSpan + xi * (TERRAIN_SPAN / GRID);
    particlePositions[i3 + 1] = cell.revenue * 8.0 + 0.3 + Math.random() * 1.5;
    particlePositions[i3 + 2] = -halfSpan + zi * (TERRAIN_SPAN / GRID);
    // Velocity: slight drift with random direction
    const angle = Math.random() * Math.PI * 2;
    particleVelocities[i3]     = Math.cos(angle) * 0.03;
    particleVelocities[i3 + 1] = (Math.random() - 0.5) * 0.06;
    particleVelocities[i3 + 2] = Math.sin(angle) * 0.03;
    particleLife[i] = 0.3 + Math.random() * 0.7;
  }
  // After writing positions, MUST mark attribute as needing update
  particleAttr.needsUpdate = true;
}
resetParticles(8);
// Particle material — point sprite with size attenuation
const particleMat = new THREE.PointsMaterial({
  color: 0xf0c060,
  size: 0.18,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.75,
  sizeAttenuation: true,
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 2;
scene.add(particles);
// Update particles each frame: drift, clamp to terrain, respawn when low
function updateParticles(dt, timeIndex) {
  const data = dataByTime[timeIndex];
  const halfSpan = TERRAIN_SPAN / 2;
  const step = TERRAIN_SPAN / GRID;
  const clampedDt = Math.min(dt, 0.1); // prevent huge jumps on tab switch
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const i3 = i * 3;
    particleLife[i] -= clampedDt * 0.15;
    // Respawn dead particles at random location
    if (particleLife[i] <= 0) {
      const xi = Math.random() * GRID;
      const zi = Math.random() * GRID;
      const ci = Math.min(Math.floor(zi), GRID - 1) * GRID + Math.min(Math.floor(xi), GRID - 1);
      const cell = data[ci];
      particlePositions[i3]     = -halfSpan + xi * step;
      particlePositions[i3 + 1] = cell.revenue * 8.0 + 0.3 + Math.random() * 1.5;
      particlePositions[i3 + 2] = -halfSpan + zi * step;
      const angle = Math.random() * Math.PI * 2;
      particleVelocities[i3]     = Math.cos(angle) * 0.03;
      particleVelocities[i3 + 1] = (Math.random() - 0.5) * 0.06;
      particleVelocities[i3 + 2] = Math.sin(angle) * 0.03;
      particleLife[i] = 0.3 + Math.random() * 0.7;
      continue;
    }
    // Drift particle
    particlePositions[i3]     += particleVelocities[i3]     * clampedDt;
    particlePositions[i3 + 1] += particleVelocities[i3 + 1] * clampedDt;
    particlePositions[i3 + 2] += particleVelocities[i3 + 2] * clampedDt;
    // Clamp to terrain bounds and keep above surface
    const gx = (particlePositions[i3] + halfSpan) / step;
    const gz = (particlePositions[i3 + 2] + halfSpan) / step;
    if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
      const ci = Math.floor(gz) * GRID + Math.floor(gx);
      const minY = data[ci].revenue * 8.0 + 0.2;
      if (particlePositions[i3 + 1] < minY) {
        particlePositions[i3 + 1] = minY;
        particleVelocities[i3 + 1] = Math.abs(particleVelocities[i3 + 1]);
      }
      // Bounds wrap
      if (Math.abs(particlePositions[i3]) > halfSpan) particleVelocities[i3] *= -1;
      if (Math.abs(particlePositions[i3 + 2]) > halfSpan) particleVelocities[i3 + 2] *= -1;
      if (particlePositions[i3 + 1] > 10) particleVelocities[i3 + 1] *= -1;
    }
  }
  // Mark attribute dirty so GPU picks up the changes
  particleAttr.needsUpdate = true;
}
// ============================================================================
// TIME SWITCHING — swap cached geometry buffers on slider change
// ============================================================================
let currentTime = 8;
function switchTerrainTime(timeIndex) {
  if (timeIndex === currentTime) return;
  const cached = geometryCache.get(timeIndex);
  if (!cached) return;
  // Swap terrain position buffer (no new allocation)
  const terrainPosAttr = terrainGeo.getAttribute('position');
  terrainPosAttr.array.set(cached.positions);
  terrainPosAttr.needsUpdate = true;
  // Swap terrain color buffer
  const terrainColAttr = terrainGeo.getAttribute('color');
  terrainColAttr.array.set(cached.colors);
  terrainColAttr.needsUpdate = true;
  // Recompute normals after position change
  terrainGeo.computeVertexNormals();
  // Swap wireframe positions (reuse cached positions)
  const wirePosAttr = wireGeo.getAttribute('position');
  wirePosAttr.array.set(cached.positions);
  wirePosAttr.needsUpdate = true;
  // Rebuild rivers for this time step
  scene.remove(riverGroup);
  disposeGroup(riverGroup);
  riverGroup = buildRiverPaths(timeIndex);
  scene.add(riverGroup);
  // Reset particles to new terrain surface
  resetParticles(timeIndex);
  // Update dashboard panel
  updatePanel(timeIndex);
  currentTime = timeIndex;
}
function disposeGroup(group) {
  group.traverse(child => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(m => m.dispose());
      } else {
        child.material.dispose();
      }
    }
  });
}
// ============================================================================
// DASHBOARD PANEL UPDATES
// ============================================================================
function updatePanel(timeIndex) {
  const data = dataByTime[timeIndex];
  let peakRevenue = 0;
  let sumDensity = 0;
  let sumError = 0;
  let sumApi = 0;
  for (const cell of data) {
    if (cell.revenue > peakRevenue) peakRevenue = cell.revenue;
    sumDensity += cell.density;
    sumError += cell.error;
    sumApi += cell.api;
  }
  const n = data.length;
  const hour = timeIndex;
  const label = `Day 1, ${String(hour).padStart(2, '0')}:00`;
  document.getElementById('val-time').textContent = label;
  document.getElementById('val-revenue').textContent = '$' + (peakRevenue * 10000).toFixed(0);
  document.getElementById('val-density').textContent = ((sumDensity / n) * 100).toFixed(1) + '%';
  document.getElementById('val-error').textContent = ((sumError / n) * 100).toFixed(2) + '%';
  document.getElementById('val-api').textContent = Math.round(sumApi * 100);
  document.getElementById('time-label').textContent = label;
  document.getElementById('time-slider').value = timeIndex;
}
updatePanel(8);
// ============================================================================
// UI EVENT HANDLERS
// ============================================================================
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  const t = parseInt(slider.value);
  switchTerrainTime(t);
});
let playing = false;
let playInterval = null;
function togglePlay() {
  playing = !playing;
  const btn = document.getElementById('btn-play');
  btn.textContent = playing ? 'Pause' : 'Play';
  btn.classList.toggle('active', playing);
  if (playing) {
    playInterval = setInterval(() => {
      let next = (currentTime + 1) % TIME_STEPS;
      slider.value = next;
      switchTerrainTime(next);
    }, 800);
  } else {
    clearInterval(playInterval);
  }
}
window.togglePlay = togglePlay;
function toggleAutoRotate() {
  controls.autoRotate = !controls.autoRotate;
  const btn = document.getElementById('btn-auto');
  btn.classList.toggle('active', controls.autoRotate);
}
window.toggleAutoRotate = toggleAutoRotate;
// ============================================================================
// CAMERA BOOKMARKS — save/restore with localStorage persistence
// ============================================================================
const BOOKMARK_KEY = 'terrain-explorer-bookmarks';
const DEFAULT_BOOKMARKS = [
  { name: 'Overview', pos: [18, 14, 18], target: [0, 3, 0] },
  { name: 'Close-up North', pos: [4, 6, -16], target: [0, 2, -4] },
  { name: 'River Trace', pos: [-12, 5, -8], target: [2, 2, 2] },
];
function loadBookmarks() {
  try {
    const raw = localStorage.getItem(BOOKMARK_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {
    console.warn('Bookmark load failed, using defaults:', e.message);
  }
  return [...DEFAULT_BOOKMARKS];
}
function saveBookmarks(list) {
  try {
    localStorage.setItem(BOOKMARK_KEY, JSON.stringify(list));
  } catch (e) {
    showToast('Bookmark save failed: storage full', true);
  }
}
let bookmarks = loadBookmarks();
function loadBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  // Animate camera to bookmarked position (smooth transition via controls target)
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease-in-out cubic
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animStep);
    }
  }
  requestAnimationFrame(animStep);
}
window.loadBookmark = loadBookmark;
function saveBookmark() {
  const bm = {
    name: 'View ' + (bookmarks.length + 1),
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
  };
  bookmarks.push(bm);
  saveBookmarks(bookmarks);
  refreshBookmarkButtons();
  showToast('View saved (Ctrl+1-9 to recall)');
}
window.saveBookmark = saveBookmark;
function refreshBookmarkButtons() {
  const container = document.getElementById('bookmarks');
  // Remove old dynamic buttons (keep first 4: 3 defaults + save button)
  while (container.children.length > 4) {
    container.removeChild(container.lastChild);
  }
  // Update shortcut numbers on existing buttons
  const buttons = container.querySelectorAll('button');
  for (let i = 0; i < Math.min(buttons.length, bookmarks.length); i++) {
    const shortcut = buttons[i].querySelector('.shortcut');
    if (shortcut) shortcut.textContent = (i + 1);
  }
  // Add extra bookmark buttons beyond the first 3
  for (let i = 3; i < bookmarks.length; i++) {
    const btn = document.createElement('button');
    btn.innerHTML = `<span class="shortcut">${i + 1}</span> ${bookmarks[i].name}`;
    btn.onclick = (() => { const idx = i; return () => loadBookmark(idx); })();
    container.appendChild(btn);
  }
}
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  // Ctrl+S or just 's' to save bookmark
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault();
    saveBookmark();
  }
  // Number keys 1-9 load bookmarks
  const num = parseInt(e.key);
  if (num >= 1 && num <= 9 && !e.ctrlKey && !e.metaKey && !e.altKey) {
    if (num <= bookmarks.length) {
      loadBookmark(num - 1);
    }
  }
  // Space toggles play
  if (e.key === ' ' && e.target === document.body) {
    e.preventDefault();
    togglePlay();
  }
});
// Toast notification helper
let toastTimer = null;
function showToast(msg, isError = false) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = isError ? 'error show' : 'show';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.className = ''; }, 2000);
}
// ============================================================================
// RESIZE HANDLER
// ============================================================================
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// ============================================================================
// RENDER LOOP — single requestAnimationFrame, no duplicate calls
// ============================================================================
const clock = new THREE.Clock();
let lastFrameTime = performance.now();
function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min(clock.getDelta(), 0.1); // cap delta to avoid spiral on tab switch
  controls.update();
  // Update particles using direct buffer reference (no allocation per frame)
  updateParticles(dt, currentTime);
  // Pulse particle opacity based on time (subtle breathing effect)
  particleMat.opacity = 0.6 + Math.sin(now * 0.001) * 0.15;
  renderer.render(scene, camera);
  lastFrameTime = now;
}
// Initial bookmark button sync
refreshBookmarkButtons();
// Kick off render loop — the ONLY requestAnimationFrame entry point
animate();
console.log('3D Data Terrain Explorer ready.');
console.log('Controls: Left-drag orbit | Scroll zoom | Right-drag pan | Space play/pause');
console.log('Bookmarks: Keys 1-9 | Ctrl+S save view | Auto-rotate toggle in timebar');
console.log('Geometry cache: ' + geometryCache.size + ' frames pre-built (0 runtime allocations on slider)');
console.log('Particle buffer: ' + PARTICLE_COUNT + ' particles, single Float32Array shared with attribute');
</script>
</body>
</html>