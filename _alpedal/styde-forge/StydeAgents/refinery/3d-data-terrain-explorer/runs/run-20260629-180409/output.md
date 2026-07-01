<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#0a0a14; overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:#c8d6e5; }
  #canvas-container { position:fixed; inset:0; }
  #hud { position:fixed; top:16px; left:16px; pointer-events:none; z-index:10; }
  #hud h1 { font-size:18px; font-weight:600; color:#8395a7; letter-spacing:0.04em; margin-bottom:2px; }
  #hud .subtitle { font-size:11px; color:#576574; }
  #time-panel { position:fixed; bottom:32px; left:50%; transform:translateX(-50%); z-index:10;
    background:rgba(10,10,20,0.85); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.08);
    border-radius:14px; padding:14px 24px; display:flex; gap:16px; align-items:center; min-width:420px; }
  #time-slider { flex:1; height:4px; -webkit-appearance:none; appearance:none; background:linear-gradient(90deg,#0abde3,#48dbfb,#0abde3);
    border-radius:2px; outline:none; cursor:pointer; }
  #time-slider::-webkit-slider-thumb { -webkit-appearance:none; width:18px; height:18px; border-radius:50%;
    background:#48dbfb; border:2px solid #0abde3; box-shadow:0 0 12px rgba(72,219,251,0.5); cursor:pointer; }
  #time-label { font-size:12px; color:#48dbfb; font-weight:600; min-width:70px; text-align:center; letter-spacing:0.03em; }
  #time-nav { display:flex; gap:6px; }
  #time-nav button { background:rgba(72,219,251,0.12); border:1px solid rgba(72,219,251,0.25); color:#48dbfb;
    border-radius:6px; width:28px; height:28px; cursor:pointer; font-size:14px; display:flex; align-items:center; justify-content:center; }
  #time-nav button:hover { background:rgba(72,219,251,0.25); }
  #bookmarks { position:fixed; top:16px; right:16px; z-index:10; display:flex; gap:6px; }
  #bookmarks button { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:#8395a7;
    padding:6px 12px; border-radius:8px; cursor:pointer; font-size:11px; letter-spacing:0.03em; transition:all 0.2s; }
  #bookmarks button:hover { background:rgba(255,255,255,0.14); color:#c8d6e5; }
  #bookmarks button.active { background:rgba(72,219,251,0.2); border-color:rgba(72,219,251,0.4); color:#48dbfb; }
  #diagnostics { position:fixed; bottom:32px; right:24px; z-index:10; background:rgba(10,10,20,0.8);
    border:1px solid rgba(255,255,255,0.06); border-radius:10px; padding:10px 14px; font-size:10px;
    font-family:'Courier New',monospace; color:#576574; line-height:1.6; min-width:160px; }
  #diagnostics .val { color:#48dbfb; }
  #legend { position:fixed; bottom:120px; right:24px; z-index:10; display:flex; flex-direction:column; gap:3px; font-size:10px; color:#576574; }
  .legend-item { display:flex; align-items:center; gap:6px; }
  .legend-swatch { width:10px; height:10px; border-radius:2px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hud">
  <h1>DATA TERRAIN EXPLORER</h1>
  <div class="subtitle">Revenue elevation · User density vegetation · Error rivers · API particle flows</div>
</div>
<div id="bookmarks">
  <button data-view="overhead" title="Top-down">&#9650; Top</button>
  <button data-view="perspective" class="active" title="Default 3/4">&#9671; 3/4</button>
  <button data-view="valley" title="Valley flyover">&#9660; Valley</button>
  <button data-view="closeup" title="Peak closeup">&#9670; Peak</button>
</div>
<div id="time-panel">
  <div id="time-nav">
    <button id="btn-prev" title="Previous timestep">&#9664;</button>
    <button id="btn-play" title="Auto-play">&#9654;</button>
    <button id="btn-next" title="Next timestep">&#9654;</button>
  </div>
  <input type="range" id="time-slider" min="0" max="19" value="0" step="1">
  <div id="time-label">T+00:00</div>
</div>
<div id="diagnostics">
  <div>cache hits: <span class="val" id="diag-hits">0</span></div>
  <div>cache misses: <span class="val" id="diag-misses">0</span></div>
  <div>geometries: <span class="val" id="diag-geos">0</span></div>
  <div>fps: <span class="val" id="diag-fps">60</span></div>
</div>
<div id="legend">
  <div class="legend-item"><span class="legend-swatch" style="background:#1dd1a1;"></span> High elevation (revenue)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#2e86de;"></span> Mid elevation</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#576574;"></span> Low elevation</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ee5a24;"></span> Error river</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#feca57;"></span> API particle</div>
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
// ─── CONSTANTS ───────────────────────────────────────────
const GRID = 50;
const SPACING = 0.5;
const TERRAIN_W = GRID * SPACING;
const TIME_STEPS = 20;
const RIVER_SEGMENTS = 120;
const PARTICLE_COUNT = 300;
// ─── SYNTHETIC DATA GENERATOR ────────────────────────────
// Each timestep: revenue (elevation), userDensity (vegetation 0-1), errorPaths (array of [x,z] coords), apiFlow (array of {from,to} endpoints)
function generateTimeSeries() {
  const steps = [];
  // Seed-driven pseudo-random so terrain evolves smoothly across time
  const seededRandom = (seed) => {
    let s = seed | 0;
    return () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
  };
  const rand = seededRandom(42);
  // Build base terrain: several Gaussian hills that shift over time
  const baseHills = [
    { cx: 0.55, cz: 0.45, amp: 1.0, sx: 0.22, sz: 0.20, driftX: 0.002, driftZ: 0.001 },
    { cx: 0.30, cz: 0.70, amp: 0.7, sx: 0.18, sz: 0.16, driftX: -0.001, driftZ: 0.002 },
    { cx: 0.72, cz: 0.25, amp: 0.85, sx: 0.16, sz: 0.19, driftX: 0.001, driftZ: -0.001 },
    { cx: 0.40, cz: 0.30, amp: 0.55, sx: 0.25, sz: 0.22, driftX: 0.0, driftZ: 0.003 },
  ];
  for (let t = 0; t < TIME_STEPS; t++) {
    const revenue = new Float32Array(GRID * GRID);
    const userDensity = new Float32Array(GRID * GRID);
    const errorPaths = [];
    const apiFlows = [];
    // Move hills over time
    const driftScale = t / (TIME_STEPS - 1);
    for (let i = 0; i < GRID; i++) {
      for (let j = 0; j < GRID; j++) {
        const x = i / (GRID - 1);
        const z = j / (GRID - 1);
        let h = 0;
        for (const hill of baseHills) {
          const cx = hill.cx + hill.driftX * t * 4;
          const cz = hill.cz + hill.driftZ * t * 4;
          const dx = (x - cx) / hill.sx;
          const dz = (z - cz) / hill.sz;
          h += hill.amp * Math.exp(-(dx * dx + dz * dz) * 0.5);
        }
        // Add some perlin-like noise
        h += 0.08 * Math.sin(x * 12 + t * 0.3) * Math.cos(z * 10 + t * 0.2);
        h += 0.05 * Math.sin(x * 25 - t * 0.5) * Math.sin(z * 20 + t * 0.4);
        h = Math.max(0, h * 4.0); // Scale to 0-4
        revenue[i * GRID + j] = h;
        // User density: correlated but not identical — offset by noise and hill position
        userDensity[i * GRID + j] = Math.min(1, Math.max(0,
          h * 0.22 + 0.15 * Math.sin(x * 8 + t * 0.15) * Math.cos(z * 7 - t * 0.1) + 0.3));
      }
    }
    // Error rivers: trace paths through low-density / high-gradient zones
    // 1-3 rivers per timestep
    const riverCount = 1 + Math.floor(rand() * 3);
    for (let r = 0; r < riverCount; r++) {
      const path = [];
      // Start at a random edge
      const startEdge = Math.floor(rand() * 4);
      let cx, cz;
      if (startEdge === 0) { cx = rand(); cz = 0; }
      else if (startEdge === 1) { cx = 1; cz = rand(); }
      else if (startEdge === 2) { cx = rand(); cz = 1; }
      else { cx = 0; cz = rand(); }
      // Flow downhill using gradient descent on revenue field
      for (let s = 0; s < RIVER_SEGMENTS; s++) {
        path.push([cx, cz]);
        // Sample gradient at current position
        const gi = Math.min(GRID - 2, Math.max(0, Math.floor(cx * (GRID - 1))));
        const gj = Math.min(GRID - 2, Math.max(0, Math.floor(cz * (GRID - 1))));
        const h00 = revenue[gi * GRID + gj];
        const h10 = revenue[(gi + 1) * GRID + gj];
        const h01 = revenue[gi * GRID + (gj + 1)];
        const gx = h10 - h00;
        const gz = h01 - h00;
        const mag = Math.sqrt(gx * gx + gz * gz) || 0.001;
        // Move opposite to gradient (downhill) with some lateral wander
        const wanderAngle = (rand() - 0.5) * 0.4;
        const baseAngle = Math.atan2(-gz, -gx);
        const angle = baseAngle + wanderAngle;
        cx += 0.008 * Math.cos(angle);
        cz += 0.008 * Math.sin(angle);
        cx = Math.max(0, Math.min(1, cx));
        cz = Math.max(0, Math.min(1, cz));
      }
      errorPaths.push(path);
    }
    // API flows: 15-40 random point-to-point paths
    const flowCount = 15 + Math.floor(rand() * 25);
    for (let f = 0; f < flowCount; f++) {
      apiFlows.push({
        from: [rand(), rand()],
        to: [rand(), rand()],
        weight: 0.3 + rand() * 0.7
      });
    }
    steps.push({ revenue, userDensity, errorPaths, apiFlows });
  }
  return steps;
}
const timeSeries = generateTimeSeries();
// ─── CACHE LAYER ─────────────────────────────────────────
const cache = {
  terrains: new Map(),       // timestep -> {geometry, material}
  rivers: new Map(),         // timestep -> THREE.Group
  particles: new Map(),      // timestep -> {geometry, positions array}
  noiseGrids: new Map(),     // timestep -> precomputed noise grid
  hits: 0,
  misses: 0,
  get(key, builder) {
    if (this[key]) { this.hits++; return this[key]; }
    this.misses++;
    const val = builder();
    this[key] = val;
    return val;
  },
  clearAll() {
    this.terrains.clear();
    this.rivers.clear();
    this.particles.clear();
    this.noiseGrids.clear();
  }
};
// ─── TERRAIN GEOMETRY BUILDER ────────────────────────────
// Pre-build all geometries at init — slider swaps buffer references
function buildTerrainGeometry(timestep) {
  const { revenue, userDensity } = timeSeries[timestep];
  const geo = new THREE.BufferGeometry();
  const vertices = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const indices = [];
  // Fill vertex positions and colors
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      const vtx = idx * 3;
      const x = (i - GRID / 2) * SPACING;
      const z = (j - GRID / 2) * SPACING;
      const h = revenue[idx];
      vertices[vtx] = x;
      vertices[vtx + 1] = h;
      vertices[vtx + 2] = z;
      // Vertex color: vegetation gradient from user density
      // Low density (0) = sandy brown, high density (1) = lush green
      const d = userDensity[idx];
      colors[vtx] = 0.18 + d * 0.12;
      colors[vtx + 1] = 0.35 + d * 0.45;
      colors[vtx + 2] = 0.12 + d * 0.08;
    }
  }
  // Build index buffer (two triangles per grid cell)
  for (let i = 0; i < GRID - 1; i++) {
    for (let j = 0; j < GRID - 1; j++) {
      const a = i * GRID + j;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, c);
      indices.push(b, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
// ─── RIVER GEOMETRY BUILDER ──────────────────────────────
function buildRiverGroup(timestep) {
  const { revenue, errorPaths } = timeSeries[timestep];
  const group = new THREE.Group();
  for (const path of errorPaths) {
    // Sample river path through terrain, lifting to surface height
    const curvePoints = path.map(([cx, cz]) => {
      const gi = Math.min(GRID - 1, Math.max(0, Math.round(cx * (GRID - 1))));
      const gj = Math.min(GRID - 1, Math.max(0, Math.round(cz * (GRID - 1))));
      const h = revenue[gi * GRID + gj] + 0.03; // Slightly above terrain
      const wx = (cx * (GRID - 1) - GRID / 2) * SPACING;
      const wz = (cz * (GRID - 1) - GRID / 2) * SPACING;
      return new THREE.Vector3(wx, h, wz);
    });
    const curve = new THREE.CatmullRomCurve3(curvePoints);
    const tubeGeo = new THREE.TubeGeometry(curve, 80, 0.08, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xee5a24,
      emissive: 0x441200,
      roughness: 0.3,
      metalness: 0.1,
      transparent: true,
      opacity: 0.85
    });
    group.add(new THREE.Mesh(tubeGeo, tubeMat));
  }
  return group;
}
// ─── PARTICLE SYSTEM BUILDER ─────────────────────────────
function buildParticleSystem(timestep) {
  const { revenue, apiFlows } = timeSeries[timestep];
  // Each particle: position along its flow path (0-1 t_param) + from/to
  const particleData = [];
  // Assign flows to particles, cycling if needed
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    const flow = apiFlows[p % apiFlows.length];
    particleData.push({
      from: flow.from,
      to: flow.to,
      t: Math.random(),        // Random progress along path
      speed: 0.0008 + Math.random() * 0.0025,
      weight: flow.weight
    });
  }
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const colors = new Float32Array(PARTICLE_COUNT * 3);
  // Initialize all particle positions
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    const pd = particleData[p];
    const pt = p * 3;
    const cx = pd.from[0] + (pd.to[0] - pd.from[0]) * pd.t;
    const cz = pd.from[1] + (pd.to[1] - pd.from[1]) * pd.t;
    const gi = Math.min(GRID - 1, Math.max(0, Math.round(cx * (GRID - 1))));
    const gj = Math.min(GRID - 1, Math.max(0, Math.round(cz * (GRID - 1))));
    const h = revenue[gi * GRID + gj] + 0.15;
    positions[pt] = (cx * (GRID - 1) - GRID / 2) * SPACING;
    positions[pt + 1] = h;
    positions[pt + 2] = (cz * (GRID - 1) - GRID / 2) * SPACING;
    colors[pt] = 0.98;
    colors[pt + 1] = 0.79;
    colors[pt + 2] = 0.34;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.12,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.8
  });
  const points = new THREE.Points(geo, mat);
  // Attach particle update data to the mesh for per-frame reuse
  points.userData = { particleData, positions, colors, revenue };
  return points;
}
// ─── THREE.JS SCENE SETUP ────────────────────────────────
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 15, 50);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 100);
camera.position.set(12, 8, 14);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
// ─── LIGHTING ────────────────────────────────────────────
const ambientLight = new THREE.AmbientLight(0x1a1a3a, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.0);
sunLight.position.set(15, 20, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4488cc, 1.0);
fillLight.position.set(-8, 3, -5);
scene.add(fillLight);
// ─── GROUND GRID ─────────────────────────────────────────
const gridHelper = new THREE.PolarGridHelper(TERRAIN_W / 2 + 2, 40, 25, 64, 0x1a1a3a, 0x1a1a3a);
gridHelper.position.y = -0.02;
scene.add(gridHelper);
// ─── ORBIT CONTROLS ──────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.8, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.15;
controls.minDistance = 4;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.55;
controls.update();
// ─── PRE-CACHE ALL GEOMETRIES ────────────────────────────
// Build every timestep's terrain and river geometry at startup
// Only the active one is added to scene; slider swaps references
console.time('precache');
const terrainCache = [];
const riverCache = [];
const particleCache = [];
for (let t = 0; t < TIME_STEPS; t++) {
  terrainCache.push(buildTerrainGeometry(t));
  riverCache.push(buildRiverGroup(t));
  particleCache.push(buildParticleSystem(t));
}
console.timeEnd('precache');
// ─── SCENE OBJECTS (active timestep) ─────────────────────
let activeTimestep = 0;
let terrainMesh, riverGroup, particleSystem;
// Shared material — reused across all terrain swaps to avoid material allocation
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.05,
  flatShading: false
});
function loadTimestep(t) {
  // Remove old objects from scene
  if (terrainMesh) scene.remove(terrainMesh);
  if (riverGroup) scene.remove(riverGroup);
  if (particleSystem) scene.remove(particleSystem);
  // Dispose old geometries that are no longer cached (cache holds all)
  // We swap buffers — no allocation
  // Terrain: swap geometry reference on reused mesh
  if (!terrainMesh) {
    terrainMesh = new THREE.Mesh(terrainCache[t], terrainMaterial);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
  } else {
    terrainMesh.geometry = terrainCache[t];
  }
  scene.add(terrainMesh);
  // River: swap group reference
  riverGroup = riverCache[t];
  scene.add(riverGroup);
  // Particles: swap point cloud
  particleSystem = particleCache[t];
  scene.add(particleSystem);
  activeTimestep = t;
  // Diagnostic update
  document.getElementById('diag-hits').textContent = cache.hits;
  document.getElementById('diag-misses').textContent = cache.misses;
  document.getElementById('diag-geos').textContent = terrainCache.length + riverCache.length + particleCache.length;
}
// Initial load
loadTimestep(0);
// ─── TIME SLIDER ─────────────────────────────────────────
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
let sliderDebounceTimer = null;
function updateTimeLabel(t) {
  const hours = Math.floor(t * 0.5);
  const mins = (t * 30) % 60;
  timeLabel.textContent = `T+${String(hours).padStart(2,'0')}:${String(mins).padStart(2,'0')}`;
}
slider.addEventListener('input', () => {
  const t = parseInt(slider.value);
  updateTimeLabel(t);
  // Debounce terrain/river swap: 200ms delay
  // Only label updates immediately; geometry swap waits
  if (sliderDebounceTimer) clearTimeout(sliderDebounceTimer);
  sliderDebounceTimer = setTimeout(() => {
    loadTimestep(t);
  }, 200);
});
// Also handle direct click on slider (no debounce on programmatic change)
slider.addEventListener('change', () => {
  if (sliderDebounceTimer) clearTimeout(sliderDebounceTimer);
  loadTimestep(parseInt(slider.value));
});
document.getElementById('btn-prev').addEventListener('click', () => {
  const t = Math.max(0, activeTimestep - 1);
  slider.value = t;
  updateTimeLabel(t);
  if (sliderDebounceTimer) clearTimeout(sliderDebounceTimer);
  loadTimestep(t);
});
document.getElementById('btn-next').addEventListener('click', () => {
  const t = Math.min(TIME_STEPS - 1, activeTimestep + 1);
  slider.value = t;
  updateTimeLabel(t);
  if (sliderDebounceTimer) clearTimeout(sliderDebounceTimer);
  loadTimestep(t);
});
// Auto-play toggle
let autoPlayInterval = null;
const btnPlay = document.getElementById('btn-play');
btnPlay.addEventListener('click', () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval);
    autoPlayInterval = null;
    btnPlay.textContent = '\u25b6';
  } else {
    btnPlay.textContent = '\u23f8';
    autoPlayInterval = setInterval(() => {
      let t = activeTimestep + 1;
      if (t >= TIME_STEPS) t = 0;
      slider.value = t;
      updateTimeLabel(t);
      loadTimestep(t);
    }, 800);
  }
});
// ─── CAMERA BOOKMARKS ────────────────────────────────────
const bookmarks = {
  overhead:   { pos: [0, 22, 0.1],    target: [0, 0, 0] },
  perspective:{ pos: [12, 8, 14],     target: [0, 1.8, 0] },
  valley:     { pos: [-4, 1.2, -10],  target: [-1, 0.5, -2] },
  closeup:    { pos: [3, 2.5, 5],     target: [1.5, 1.5, 1] }
};
let activeBookmark = 'perspective';
// Animate camera to bookmark position
function animateToBookmark(name) {
  const bm = bookmarks[name];
  if (!bm) return;
  activeBookmark = name;
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 1200; // ms
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out cubic
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animStep);
    }
  }
  requestAnimationFrame(animStep);
  // Update button states
  document.querySelectorAll('#bookmarks button').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.view === name);
  });
}
document.querySelectorAll('#bookmarks button').forEach(btn => {
  btn.addEventListener('click', () => animateToBookmark(btn.dataset.view));
});
// ─── MEMOIZED WORLD-TO-GRID TRANSFORM ────────────────────
// Reused on hover/tooltip — never recompute per frame
const gridTransformCache = new Map();
function worldToGrid(wx, wz) {
  const key = `${wx.toFixed(3)}|${wz.toFixed(3)}`;
  if (gridTransformCache.has(key)) return gridTransformCache.get(key);
  const cx = (wx / SPACING + GRID / 2) / (GRID - 1);
  const cz = (wz / SPACING + GRID / 2) / (GRID - 1);
  const result = {
    col: Math.round(cx * (GRID - 1)),
    row: Math.round(cz * (GRID - 1)),
    cx, cz
  };
  gridTransformCache.set(key, result);
  return result;
}
// ─── PER-FRAME PARTICLE UPDATE ───────────────────────────
// Reuse position and color arrays — no per-frame allocation
const clock = new THREE.Clock();
function updateParticles(delta) {
  if (!particleSystem || !particleSystem.userData.particleData) return;
  const { particleData, positions, colors, revenue } = particleSystem.userData;
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    const pd = particleData[p];
    pd.t += pd.speed * delta * 60; // Normalize speed to ~60fps
    if (pd.t > 1) pd.t -= 1;
    const pt = p * 3;
    // Interpolate position along from-to path
    const cx = pd.from[0] + (pd.to[0] - pd.from[0]) * pd.t;
    const cz = pd.from[1] + (pd.to[1] - pd.from[1]) * pd.t;
    // Terrain height lookup
    const gi = Math.min(GRID - 1, Math.max(0, Math.round(cx * (GRID - 1))));
    const gj = Math.min(GRID - 1, Math.max(0, Math.round(cz * (GRID - 1))));
    const h = revenue[gi * GRID + gj] + 0.15;
    positions[pt] = (cx * (GRID - 1) - GRID / 2) * SPACING;
    positions[pt + 1] = h;
    positions[pt + 2] = (cz * (GRID - 1) - GRID / 2) * SPACING;
    // Color pulse based on position in flow
    const brightness = 0.5 + 0.5 * Math.sin(pd.t * Math.PI);
    colors[pt] = 0.98;       // R
    colors[pt + 1] = 0.59 + brightness * 0.3; // G
    colors[pt + 2] = 0.14 + brightness * 0.2; // B
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
  particleSystem.geometry.attributes.color.needsUpdate = true;
}
// ─── FPS COUNTER ─────────────────────────────────────────
let fpsFrames = 0;
let fpsTime = performance.now();
const fpsEl = document.getElementById('diag-fps');
// ─── RENDER LOOP ─────────────────────────────────────────
function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1); // Cap delta to avoid spiral on tab switch
  controls.update();
  updateParticles(delta);
  // FPS counter
  fpsFrames++;
  const now = performance.now();
  if (now - fpsTime >= 1000) {
    fpsEl.textContent = Math.round(fpsFrames / ((now - fpsTime) / 1000));
    fpsFrames = 0;
    fpsTime = now;
  }
  renderer.render(scene, camera);
}
// ─── RESIZE HANDLER ──────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// ─── KEYBOARD SHORTCUTS ──────────────────────────────────
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case '1': animateToBookmark('overhead'); break;
    case '2': animateToBookmark('perspective'); break;
    case '3': animateToBookmark('valley'); break;
    case '4': animateToBookmark('closeup'); break;
    case 'arrowleft':
      e.preventDefault();
      document.getElementById('btn-prev').click();
      break;
    case 'arrowright':
      e.preventDefault();
      document.getElementById('btn-next').click();
      break;
    case ' ':
      e.preventDefault();
      btnPlay.click();
      break;
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      break;
  }
});
// ─── START ───────────────────────────────────────────────
updateTimeLabel(0);
animate();
console.log('3D Data Terrain Explorer initialized');
console.log(`  ${TIME_STEPS} timesteps pre-cached`);
console.log(`  ${GRID}x${GRID} terrain grid`);
console.log(`  ${PARTICLE_COUNT} particles`);
console.log('  Controls: drag=orbit | scroll=zoom | right-drag=pan | 1-4=bookmarks | space=play | R=autorotate');
</script>
</body>
</html>