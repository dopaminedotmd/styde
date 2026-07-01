<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --panel-bg: rgba(16, 16, 24, 0.94);
    --text: #c8ccd4;
    --accent: #4da6ff;
    --danger: #e05555;
    --border: rgba(255,255,255,0.08);
    --input-bg: rgba(255,255,255,0.06);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0a0a12;
    overflow: hidden;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    color: var(--text);
    user-select: none;
    -webkit-user-select: none;
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 1;
  }
  canvas { display: block; }
  /* Dashboard panel — overlaid on the 3D scene */
  #panel {
    position: fixed;
    top: 16px;
    right: 16px;
    z-index: 10;
    width: 300px;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 16px 14px;
    backdrop-filter: blur(14px);
    display: flex;
    flex-direction: column;
    gap: 14px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }
  #panel h2 {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.02em;
    color: #e8ecf2;
    margin: 0 0 2px 0;
  }
  .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
  }
  .metric-label { opacity: 0.7; }
  .metric-value { font-weight: 600; font-variant-numeric: tabular-nums; }
  .metric-value.revenue { color: #5ecc7a; }
  .metric-value.users { color: #4da6ff; }
  .metric-value.errors { color: var(--danger); }
  input[type="range"] {
    -webkit-appearance: none;
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: var(--input-bg);
    outline: none;
    cursor: pointer;
  }
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid #fff;
    cursor: pointer;
  }
  .btn-row {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }
  button {
    flex: 1;
    min-width: 60px;
    padding: 7px 10px;
    font-size: 11px;
    font-weight: 500;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--input-bg);
    color: var(--text);
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
    white-space: nowrap;
  }
  button:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.2); }
  button.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  button.bookmark-btn { font-size: 10px; padding: 5px 8px; }
  #tooltip {
    position: fixed;
    pointer-events: none;
    z-index: 20;
    background: rgba(0,0,0,0.82);
    color: #e8ecf2;
    padding: 6px 10px;
    border-radius: 5px;
    font-size: 11px;
    display: none;
    white-space: nowrap;
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="panel">
  <h2>Data Terrain</h2>
  <div class="metric-row"><span class="metric-label">Revenue</span><span class="metric-value revenue" id="val-revenue">—</span></div>
  <div class="metric-row"><span class="metric-label">Active Users</span><span class="metric-value users" id="val-users">—</span></div>
  <div class="metric-row"><span class="metric-label">Error Rate</span><span class="metric-value errors" id="val-errors">—</span></div>
  <div style="display:flex;flex-direction:column;gap:4px">
    <div style="display:flex;justify-content:space-between;font-size:11px">
      <span>Time</span><span id="time-label">Day 0</span>
    </div>
    <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
  </div>
  <div class="btn-row">
    <button id="btn-auto-rotate">Auto-Rotate</button>
    <button id="btn-wireframe">Wireframe</button>
  </div>
  <div class="btn-row" style="margin-top:2px">
    <button class="bookmark-btn" data-idx="0">Overview</button>
    <button class="bookmark-btn" data-idx="1">Top-Down</button>
    <button class="bookmark-btn" data-idx="2">Close-Up</button>
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
// ── Seeded PRNG — ensures deterministic data across reloads (non-determinism audit) ──
// Notes: Mulberry32 algorithm, 32-bit state, reproducible sequence.
function createRNG(seed) {
  let s = seed | 0;
  return function() {
    s |= 0; s = s + 0x6D2B79F5 | 0;
    let t = Math.imul(s ^ s >>> 15, 1 | s);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
// ── Synthetic time-series data ──
// Notes: 30 days, 20×20 grid. Each cell has revenue, users, error_rate per day.
// Revenue drives terrain height. Users drive vertex color. Errors drive river paths.
const GRID = 20;                // grid resolution
const DAYS = 30;               // time steps
const SEED = 20240629;         // fixed seed for reproducibility
const rng = createRNG(SEED);
// Generate base terrain shape — sum of 3 gaussians for natural-looking landscape
// Notes: Precompute base elevation per cell (day-invariant shape).
// Day-specific data is overlaid as multiplier + noise on top of this base.
const baseElevation = new Float32Array(GRID * GRID);
const cx1 = GRID * 0.35, cz1 = GRID * 0.4, sigma1 = GRID * 0.22;
const cx2 = GRID * 0.65, cz2 = GRID * 0.6, sigma2 = GRID * 0.18;
const cx3 = GRID * 0.5,  cz3 = GRID * 0.5, sigma3 = GRID * 0.35;
for (let z = 0; z < GRID; z++) {
  for (let x = 0; x < GRID; x++) {
    const dx1 = x - cx1, dz1 = z - cz1;
    const dx2 = x - cx2, dz2 = z - cz2;
    const dx3 = x - cx3, dz3 = z - cz3;
    const g1 = Math.exp(-(dx1*dx1 + dz1*dz1) / (2*sigma1*sigma1));
    const g2 = Math.exp(-(dx2*dx2 + dz2*dz2) / (2*sigma2*sigma2));
    const g3 = Math.exp(-(dx3*dx3 + dz3*dz3) / (2*sigma3*sigma3));
    baseElevation[z * GRID + x] = g1 * 0.7 + g2 * 0.5 + g3 * 0.35;
  }
}
// Per-day data: [day][cell] = {revenue, users, error_rate}
// Notes: Revenue = base * (1 + day trend) + noise. Users = revenue * 0.6 + independent noise.
// Error rate = low base + spikes in low-revenue regions (rivers).
const timeSeries = [];
for (let d = 0; d < DAYS; d++) {
  const dayData = [];
  const trend = 1.0 + d * 0.015; // gentle upward trend
  for (let i = 0; i < GRID * GRID; i++) {
    const base = baseElevation[i];
    const revenue = Math.max(0.02, base * trend * (0.85 + rng() * 0.3));
    const users = Math.max(1, Math.round(revenue * 1200 * (0.8 + rng() * 0.4)));
    // Error rate spike in valleys (low revenue) plus random anomalies
    const errorRate = Math.max(0.001, (1.0 - base) * 0.08 * (0.5 + rng()) + (rng() < 0.04 ? rng() * 0.15 : 0));
    dayData.push({ revenue, users, errorRate });
  }
  timeSeries.push(dayData);
}
// ── River path computation (cached per day) ──
// Notes: Follows steepest error-rate gradient from high-error cells downhill.
// Each river is a polyline of 3D points tracing through the grid.
const riverCache = new Map(); // dayIndex -> array of river point arrays
function computeRivers(dayIndex) {
  if (riverCache.has(dayIndex)) return riverCache.get(dayIndex);
  const data = timeSeries[dayIndex];
  const threshold = 0.06; // error rate above which we seed a river
  const rivers = [];
  const visited = new Uint8Array(GRID * GRID); // prevent duplicate traces
  // Find seed cells with high error rate
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      const idx = z * GRID + x;
      if (visited[idx] || data[idx].errorRate < threshold) continue;
      // Trace river downhill along steepest error descent
      const points = [];
      let cx = x, cz = z;
      let steps = 0;
      const maxSteps = 40;
      while (steps < maxSteps) {
        const ci = cz * GRID + cx;
        if (visited[ci]) break;
        visited[ci] = 1;
        const cellData = data[ci];
        const h = cellData.revenue * 8.0; // terrain height
        points.push(new THREE.Vector3(
          (cx / (GRID - 1) - 0.5) * 10,
          h,
          (cz / (GRID - 1) - 0.5) * 10
        ));
        // Check 4 neighbors for steepest error descent
        let bestDz = 0, bestDx = 0, bestErr = cellData.errorRate;
        const neighbors = [[0,-1],[0,1],[-1,0],[1,0]];
        for (const [dx, dz] of neighbors) {
          const nx = cx + dx, nz = cz + dz;
          if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
          const nErr = data[nz * GRID + nx].errorRate;
          if (nErr < bestErr) { bestErr = nErr; bestDx = dx; bestDz = dz; }
        }
        if (bestDx === 0 && bestDz === 0) break; // local minimum reached
        cx += bestDx;
        cz += bestDz;
        steps++;
      }
      if (points.length >= 3) rivers.push(points);
    }
  }
  riverCache.set(dayIndex, rivers);
  return rivers;
}
// ── Cached geometry buffers for terrain mesh ──
// Notes: We reuse position and color arrays to avoid allocation per frame.
// Swap buffer approach: write new vertex data into existing Float32Array.
const terrainPositions = new Float32Array(GRID * GRID * 3);
const terrainColors = new Float32Array(GRID * GRID * 3);
// ── Three.js setup ──
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a16);
scene.fog = new THREE.Fog(0x0a0a16, 12, 40);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 60);
camera.position.set(8, 7, 10);
camera.lookAt(0, 2, 0);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 25;
controls.maxPolarAngle = Math.PI * 0.55; // prevent going underground
controls.target.set(0, 2.5, 0);
controls.update();
// ── Lighting ──
// Notes: Directional sun + ambient + hemisphere for natural terrain shading.
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const hemiLight = new THREE.HemisphereLight(0xddeeff, 0x332211, 0.9);
scene.add(hemiLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(8, 14, 3);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 50;
sunLight.shadow.camera.left = -12;
sunLight.shadow.camera.right = 12;
sunLight.shadow.camera.top = 12;
sunLight.shadow.camera.bottom = -12;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
// ── Ground plane ──
const groundGeo = new THREE.PlaneGeometry(20, 20);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a1a28, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.5;
ground.receiveShadow = true;
scene.add(ground);
// ── Grid helper ──
const gridHelper = new THREE.PolarGridHelper(7, 32, 24, 64, 0x333355, 0x222233);
gridHelper.position.y = -0.48;
scene.add(gridHelper);
// ── Terrain mesh ──
// Notes: BufferGeometry with indexed faces. Heights updated from cached position array.
const terrainGeo = new THREE.BufferGeometry();
// Initialize position attribute with cached buffer
terrainGeo.setAttribute('position', new THREE.BufferAttribute(terrainPositions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(terrainColors, 3));
// Build index buffer (triangles for regular grid)
const indices = [];
for (let z = 0; z < GRID - 1; z++) {
  for (let x = 0; x < GRID - 1; x++) {
    const a = z * GRID + x;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    indices.push(a, b, d);
    indices.push(a, d, c);
  }
}
terrainGeo.setIndex(indices);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ── River lines group ──
const riverGroup = new THREE.Group();
scene.add(riverGroup);
// ── Particle system for data flows ──
// Notes: CPU-side position array reused each frame. Particles follow random paths
// between high-revenue nodes, representing API calls / user actions flowing through the landscape.
const PARTICLE_COUNT = 600;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = []; // per-particle state: {targetIdx, progress, speed, fromIdx, toIdx}
// Precompute high-revenue node indices for particle targeting (cached)
function getHighValueNodes(dayIndex) {
  const data = timeSeries[dayIndex];
  const nodes = [];
  for (let i = 0; i < GRID * GRID; i++) {
    if (data[i].revenue > 0.35) nodes.push(i);
  }
  if (nodes.length < 4) {
    // Fallback: top quartile
    const sorted = data.map((d, i) => ({ v: d.revenue, i })).sort((a, b) => b.v - a.v);
    const topN = Math.max(4, Math.floor(GRID * GRID * 0.15));
    for (let k = 0; k < topN; k++) nodes.push(sorted[k].i);
  }
  return nodes;
}
// Initialize particles with random positions near high-value nodes
function initParticles(dayIndex) {
  const nodes = getHighValueNodes(dayIndex);
  const data = timeSeries[dayIndex];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const nodeIdx = nodes[Math.floor(rng() * nodes.length)];
    const gx = nodeIdx % GRID;
    const gz = Math.floor(nodeIdx / GRID);
    const h = data[nodeIdx].revenue * 8.0;
    particlePositions[i * 3] = (gx / (GRID - 1) - 0.5) * 10 + (rng() - 0.5) * 2;
    particlePositions[i * 3 + 1] = h + 0.3;
    particlePositions[i * 3 + 2] = (gz / (GRID - 1) - 0.5) * 10 + (rng() - 0.5) * 2;
    // Assign target for flow animation
    const toIdx = nodes[Math.floor(rng() * nodes.length)];
    const tx = toIdx % GRID;
    const tz = Math.floor(toIdx / GRID);
    particleData[i] = {
      fromIdx: nodeIdx,
      toIdx,
      progress: rng(),
      speed: 0.003 + rng() * 0.012,
      tx: (tx / (GRID - 1) - 0.5) * 10,
      tz: (tz / (GRID - 1) - 0.5) * 10,
    };
    // Warm particle colors — gold to white
    particleColors[i * 3] = 0.9 + rng() * 0.1;
    particleColors[i * 3 + 1] = 0.7 + rng() * 0.25;
    particleColors[i * 3 + 2] = 0.3 + rng() * 0.3;
  }
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.08,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
// ── Camera bookmarks ──
// Notes: Stored as {position, target} vectors for instant recall.
const bookmarks = [
  { position: new THREE.Vector3(8, 7, 10), target: new THREE.Vector3(0, 2.5, 0) },   // Overview
  { position: new THREE.Vector3(0, 12, 0.5), target: new THREE.Vector3(0, 2, 0) },    // Top-Down
  { position: new THREE.Vector3(3, 3.5, 5), target: new THREE.Vector3(1, 1.8, 1) },   // Close-Up
];
// ── Update terrain for a given day ──
// Notes: This is the core update function. Called on slider change and initial load.
// Writes directly into cached Float32Arrays to avoid GC pressure.
let currentDay = 0;
function updateTerrain(dayIndex) {
  currentDay = dayIndex;
  const data = timeSeries[dayIndex];
  // Update vertex positions (height = revenue) and colors (users = blue gradient)
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      const idx = z * GRID + x;
      const i3 = idx * 3;
      const cell = data[idx];
      // Position: XZ on a plane, Y from revenue
      terrainPositions[i3] = (x / (GRID - 1) - 0.5) * 10;
      terrainPositions[i3 + 1] = cell.revenue * 8.0;
      terrainPositions[i3 + 2] = (z / (GRID - 1) - 0.5) * 10;
      // Color: user density mapped to vegetation gradient (low=tan/brown, high=lush green)
      const userNorm = Math.min(1, cell.users / 800); // normalize
      // Two-color gradient: brown (low users) → green (high users)
      const r = 0.35 + userNorm * 0.05;                 // 0.35 → 0.40
      const g = 0.28 + userNorm * 0.52;                 // 0.28 → 0.80
      const b = 0.12 + userNorm * 0.08;                 // 0.12 → 0.20
      terrainColors[i3] = r;
      terrainColors[i3 + 1] = g;
      terrainColors[i3 + 2] = b;
    }
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  // Update rivers
  rebuildRivers(dayIndex);
  // Reinitialize particles for this day's high-value nodes
  initParticles(dayIndex);
  // Update panel metrics (aggregate stats)
  updatePanelMetrics(dayIndex);
}
// ── Rebuild river line geometries ──
// Notes: Clears old river meshes, creates new Line objects from cached river paths.
function rebuildRivers(dayIndex) {
  // Remove old rivers
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    if (child.material) child.material.dispose();
    riverGroup.remove(child);
  }
  const rivers = computeRivers(dayIndex);
  const riverMat = new THREE.MeshBasicMaterial({
    color: 0xe04040,
    transparent: true,
    opacity: 0.75,
    depthTest: true,
    depthWrite: true,
  });
  for (const points of rivers) {
    // Create a tube-like thick line using a thin box geometry along each segment
    // Notes: Using CatmullRom curve for smooth river flow, TubeGeometry for thickness.
    const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, points.length * 3, 0.06, 6, false);
    const tube = new THREE.Mesh(tubeGeo, riverMat);
    tube.renderOrder = 1;
    tube.material.depthTest = true;
    riverGroup.add(tube);
  }
}
// ── Panel metrics update ──
function updatePanelMetrics(dayIndex) {
  const data = timeSeries[dayIndex];
  let totalRevenue = 0, totalUsers = 0, maxError = 0;
  for (const cell of data) {
    totalRevenue += cell.revenue;
    totalUsers += cell.users;
    if (cell.errorRate > maxError) maxError = cell.errorRate;
  }
  document.getElementById('val-revenue').textContent = '$' + (totalRevenue * 1000).toFixed(0) + 'K';
  document.getElementById('val-users').textContent = Math.round(totalUsers).toLocaleString();
  document.getElementById('val-errors').textContent = (maxError * 100).toFixed(2) + '%';
  document.getElementById('time-label').textContent = 'Day ' + dayIndex;
}
// ── Particle animation (per-frame update) ──
// Notes: Moves particles along paths between high-value nodes. Resets on arrival.
// CPU-side position update reused on cached Float32Array.
function animateParticles(dayIndex) {
  const data = timeSeries[dayIndex];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    pd.progress += pd.speed;
    if (pd.progress >= 1.0) {
      // Arrived at target — pick new destination
      pd.progress = 0;
      const nodes = getHighValueNodes(dayIndex);
      const newTo = nodes[Math.floor(rng() * nodes.length)];
      const ntx = newTo % GRID;
      const ntz = Math.floor(newTo / GRID);
      pd.fromIdx = pd.toIdx;
      pd.toIdx = newTo;
      pd.tx = (ntx / (GRID - 1) - 0.5) * 10;
      pd.tz = (ntz / (GRID - 1) - 0.5) * 10;
    }
    // Interpolate position
    const fx = pd.fromIdx % GRID;
    const fz = Math.floor(pd.fromIdx / GRID);
    const sx = (fx / (GRID - 1) - 0.5) * 10;
    const sz = (fz / (GRID - 1) - 0.5) * 10;
    const sh = data[pd.fromIdx].revenue * 8.0;
    const th = data[pd.toIdx].revenue * 8.0;
    const t = pd.progress;
    // Ease in-out for smoother flow
    const et = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    const i3 = i * 3;
    particlePositions[i3] = sx + (pd.tx - sx) * et + Math.sin(t * Math.PI * 3) * 0.25;
    particlePositions[i3 + 1] = sh + (th - sh) * et + 0.35 + Math.sin(t * Math.PI * 2) * 0.3;
    particlePositions[i3 + 2] = sz + (pd.tz - sz) * et + Math.cos(t * Math.PI * 3) * 0.25;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ── Render loop ──
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  // Animate particles every frame
  animateParticles(currentDay);
  // Auto-rotate if enabled
  if (controls.autoRotate) {
    // OrbitControls handles this via its own autoRotate property
  }
  renderer.render(scene, camera);
}
// ── Event handlers ──
// Time slider
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  const day = parseInt(slider.value, 10);
  updateTerrain(day);
});
// Auto-rotate toggle
const btnAutoRotate = document.getElementById('btn-auto-rotate');
let autoRotateOn = false;
btnAutoRotate.addEventListener('click', () => {
  autoRotateOn = !autoRotateOn;
  controls.autoRotate = autoRotateOn;
  controls.autoRotateSpeed = 0.6;
  btnAutoRotate.classList.toggle('active', autoRotateOn);
});
// Wireframe toggle
const btnWireframe = document.getElementById('btn-wireframe');
let wireframeOn = false;
btnWireframe.addEventListener('click', () => {
  wireframeOn = !wireframeOn;
  terrainMat.wireframe = wireframeOn;
  btnWireframe.classList.toggle('active', wireframeOn);
});
// Bookmark buttons
document.querySelectorAll('.bookmark-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.idx, 10);
    const bm = bookmarks[idx];
    // Smooth animate camera to bookmark position
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const endPos = bm.position;
    const endTarget = bm.target;
    const startTime = performance.now();
    const duration = 800; // ms
    function animStep(now) {
      const elapsed = now - startTime;
      const t = Math.min(1, elapsed / duration);
      // Ease in-out
      const et = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      camera.position.lerpVectors(startPos, endPos, et);
      controls.target.lerpVectors(startTarget, endTarget, et);
      controls.update();
      if (t < 1) {
        requestAnimationFrame(animStep);
      }
    }
    requestAnimationFrame(animStep);
  });
});
// Responsive resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Keyboard shortcuts
// Notes: 1/2/3 for bookmarks, Space for auto-rotate, R for reset
window.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT') return; // don't capture slider input
  switch (e.key) {
    case '1': document.querySelector('.bookmark-btn[data-idx="0"]').click(); break;
    case '2': document.querySelector('.bookmark-btn[data-idx="1"]').click(); break;
    case '3': document.querySelector('.bookmark-btn[data-idx="2"]').click(); break;
    case ' ':
      e.preventDefault();
      btnAutoRotate.click();
      break;
    case 'r':
      controls.target.set(0, 2.5, 0);
      camera.position.set(8, 7, 10);
      controls.update();
      break;
  }
});
// ── Mouse hover tooltip (world position → data cell) ──
const raycaster = new THREE.Raycaster();
const tooltip = document.getElementById('tooltip');
const mouse = new THREE.Vector2();
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    // Convert world XZ to grid indices
    const gx = Math.round((point.x / 10 + 0.5) * (GRID - 1));
    const gz = Math.round((point.z / 10 + 0.5) * (GRID - 1));
    if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
      const cell = timeSeries[currentDay][gz * GRID + gx];
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 16) + 'px';
      tooltip.style.top = (e.clientY - 8) + 'px';
      tooltip.textContent =
        `Revenue: $${(cell.revenue * 1000).toFixed(0)}K  Users: ${cell.users}  Errors: ${(cell.errorRate * 100).toFixed(2)}%`;
      return;
    }
  }
  tooltip.style.display = 'none';
});
// ── Initialize ──
updateTerrain(0);
animate();
// ── Export for debugging ──
// Notes: Expose key objects to window for console inspection during development.
if (typeof window !== 'undefined') {
  window.__terrainExplorer = {
    scene, camera, controls, terrainMesh, particles, riverGroup,
    updateTerrain, timeSeries, bookmarks, currentDay,
  };
}
console.log('3D Data Terrain Explorer ready — drag to orbit, scroll to zoom, use slider to scrub time.');
console.log('Keyboard: 1/2/3 = bookmarks, Space = auto-rotate, R = reset view');
</script>
</body>
</html>