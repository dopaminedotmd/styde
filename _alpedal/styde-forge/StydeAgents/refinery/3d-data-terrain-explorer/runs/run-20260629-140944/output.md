<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10,10,30,0.92);
    --text: #c8d6e5;
    --accent: #4ecdc4;
    --danger: #ff6b6b;
    --warn: #feca57;
    --border: rgba(255,255,255,0.08);
    --font: 'Segoe UI', system-ui, sans-serif;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:var(--font); color:var(--text); }
  canvas { display:block; }
  #ui-layer {
    position:fixed; inset:0; pointer-events:none; z-index:10;
  }
  #ui-layer > * { pointer-events:auto; }
  #legend {
    position:absolute; right:16px; top:50%; transform:translateY(-50%);
    background:var(--panel-bg); border:1px solid var(--border); border-radius:10px;
    padding:14px 16px; width:190px; backdrop-filter:blur(12px);
  }
  #legend h3 { font-size:13px; font-weight:600; margin-bottom:10px; color:var(--accent); letter-spacing:0.5px; }
  .legend-row { display:flex; align-items:center; gap:8px; margin-bottom:6px; font-size:11px; }
  .legend-swatch { width:14px; height:14px; border-radius:3px; flex-shrink:0; }
  .legend-gradient {
    width:100%; height:16px; border-radius:4px; margin:4px 0 8px;
    background:linear-gradient(to right, #2d5016, #7cb342, #f9a825, #e65100, #8b0000);
  }
  .legend-labels { display:flex; justify-content:space-between; font-size:10px; color:#8899aa; }
  #tooltip {
    position:absolute; padding:8px 12px; background:var(--panel-bg);
    border:1px solid var(--border); border-radius:6px; font-size:11px;
    pointer-events:none; opacity:0; transition:opacity 0.15s;
    backdrop-filter:blur(8px); white-space:nowrap;
  }
  #tooltip.visible { opacity:1; }
  .tt-label { color:#8899aa; }
  .tt-value { color:var(--accent); font-weight:600; }
  #time-control {
    position:absolute; bottom:24px; left:50%; transform:translateX(-50%);
    background:var(--panel-bg); border:1px solid var(--border); border-radius:12px;
    padding:12px 20px; display:flex; align-items:center; gap:14px;
    backdrop-filter:blur(12px);
  }
  #time-slider {
    width:280px; accent-color:var(--accent); cursor:pointer;
  }
  #time-label { font-size:12px; font-weight:600; min-width:70px; text-align:center; }
  #time-btn { background:var(--accent); color:#0a0a14; border:none; border-radius:6px;
    padding:6px 14px; cursor:pointer; font-weight:600; font-size:11px; }
  #time-btn.paused { background:var(--warn); }
  #diagnostics {
    position:absolute; left:16px; bottom:120px; background:var(--panel-bg);
    border:1px solid var(--border); border-radius:10px; padding:12px 14px;
    font-size:10px; backdrop-filter:blur(12px); width:200px;
  }
  #diagnostics h3 { font-size:11px; color:var(--accent); margin-bottom:6px; }
  .diag-row { display:flex; justify-content:space-between; margin-bottom:3px; }
  .diag-hit { color:#2ecc71; }
  .diag-miss { color:var(--warn); }
  .diag-ratio { color:var(--text); }
  #bookmarks {
    position:absolute; left:16px; top:50%; transform:translateY(-50%);
    background:var(--panel-bg); border:1px solid var(--border); border-radius:10px;
    padding:10px; backdrop-filter:blur(12px); display:flex; flex-direction:column; gap:6px;
  }
  #bookmarks h3 { font-size:11px; color:var(--accent); margin-bottom:2px; }
  .bm-btn {
    background:rgba(255,255,255,0.06); border:1px solid var(--border); border-radius:6px;
    color:var(--text); padding:5px 10px; cursor:pointer; font-size:10px; text-align:left;
    transition:background 0.2s;
  }
  .bm-btn:hover { background:rgba(78,205,196,0.15); }
  .bm-save { background:rgba(78,205,196,0.12); color:var(--accent); }
  #crosshair {
    position:absolute; top:50%; left:50%; width:20px; height:20px;
    transform:translate(-50%,-50%); pointer-events:none; opacity:0.55;
  }
  #crosshair::before, #crosshair::after {
    content:''; position:absolute; background:var(--accent);
  }
  #crosshair::before { width:100%; height:1px; top:50%; }
  #crosshair::after { width:1px; height:100%; left:50%; }
</style>
</head>
<body>
<div id="ui-layer">
  <div id="legend">
    <h3>LEGEND</h3>
    <div class="legend-row"><span class="legend-swatch" style="background:#2d5016"></span> Low density</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#7cb342"></span> Medium density</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#f9a825"></span> High density</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#e65100"></span> Very high</div>
    <div style="margin-top:8px; font-size:10px; color:#8899aa;">Elevation (height)</div>
    <div class="legend-gradient"></div>
    <div class="legend-labels"><span>0m</span><span>50m</span></div>
    <div style="margin-top:8px; font-size:10px; color:var(--danger);">
      <span style="display:inline-block;width:10px;height:2px;background:var(--danger);vertical-align:middle;margin-right:4px;"></span>
      Error rivers
    </div>
    <div style="font-size:10px; color:var(--accent); margin-top:2px;">
      <span style="display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--accent);vertical-align:middle;margin-right:4px;"></span>
      API call particles
    </div>
  </div>
  <div id="tooltip"><span class="tt-label">Revenue:</span> <span class="tt-value" id="tt-rev">--</span><br><span class="tt-label">Density:</span> <span class="tt-value" id="tt-den">--</span><br><span class="tt-label">Errors:</span> <span class="tt-value" id="tt-err">--</span></div>
  <div id="time-control">
    <button id="time-btn" class="paused">PLAY</button>
    <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
    <span id="time-label">Hour 12</span>
  </div>
  <div id="diagnostics">
    <h3>CACHE DIAGNOSTICS</h3>
    <div class="diag-row"><span>Heightfield</span><span class="diag-hit" id="diag-hf-hit">0</span><span class="diag-miss" id="diag-hf-miss">0</span><span class="diag-ratio" id="diag-hf-rate">0%</span></div>
    <div class="diag-row"><span>Colors</span><span class="diag-hit" id="diag-col-hit">0</span><span class="diag-miss" id="diag-col-miss">0</span><span class="diag-ratio" id="diag-col-rate">0%</span></div>
    <div class="diag-row"><span>Rivers</span><span class="diag-hit" id="diag-riv-hit">0</span><span class="diag-miss" id="diag-riv-miss">0</span><span class="diag-ratio" id="diag-riv-rate">0%</span></div>
    <div class="diag-row"><span>Grid Xform</span><span class="diag-hit" id="diag-xf-hit">0</span><span class="diag-miss" id="diag-xf-miss">0</span><span class="diag-ratio" id="diag-xf-rate">0%</span></div>
    <div class="diag-row" style="margin-top:4px;color:#8899aa;"><span>FPS</span><span id="diag-fps">--</span></div>
  </div>
  <div id="bookmarks">
    <h3>BOOKMARKS</h3>
    <button class="bm-btn" data-bm="overview">Overview</button>
    <button class="bm-btn" data-bm="north">North Ridge</button>
    <button class="bm-btn" data-bm="valley">Error Valley</button>
    <button class="bm-btn bm-save" id="bm-save-btn">+ Save Current</button>
  </div>
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
// ── CONSTANTS ──────────────────────────────────────────────────
const GRID = 50;                // terrain resolution (GRID x GRID vertices)
const TERRAIN_SIZE = 40;        // world-space width/depth of terrain
const MAX_HEIGHT = 8;           // max elevation in world units
const TIME_STEPS = 24;          // hours in a day
const PARTICLE_COUNT = 200;     // number of API-call particles
const RIVER_COUNT = 3;          // number of error river paths
// ── CACHE SYSTEM ───────────────────────────────────────────────
// Each cache tracks hits/misses for the diagnostic panel.
class CacheTracker {
  constructor(name) {
    this.name = name;
    this.hits = 0;
    this.misses = 0;
    this.store = new Map();
  }
  get(key) {
    if (this.store.has(key)) { this.hits++; return this.store.get(key); }
    this.misses++; return undefined;
  }
  set(key, value) { this.store.set(key, value); return value; }
  get rate() { const t = this.hits + this.misses; return t ? ((this.hits/t)*100).toFixed(1) : '0.0'; }
  clear() { this.store.clear(); this.hits = 0; this.misses = 0; }
}
// Four cache layers as required by the blueprint.
const heightfieldCache = new CacheTracker('heightfield');   // Float32Array per time step
const colorCache = new CacheTracker('color');               // Float32Array per time step
const riverCache = new CacheTracker('river');               // {curve, tubeGeometry} per time step
const gridXformCache = new CacheTracker('grid');            // Map<worldKey, {gx,gz}>
// ── DATA GENERATION ────────────────────────────────────────────
// Generate synthetic time-series: revenue (height), user density (color),
// error locations (river paths), and API call flows (particle paths).
// Uses seeded pseudo-random for reproducibility.
function mulberry32(a) {
  return function() { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
}
const rng = mulberry32(42);
// Pre-generate noise-like base patterns that evolve over time.
// Each time step has a GRID*GRID heightmap and density map.
const allHeightfields = [];   // Array<Float32Array> — raw source data
const allDensities = [];      // Array<Float32Array> — raw source data
// Build smooth 2D noise by layering sine waves (avoiding external noise lib).
function noise2D(x, z, t) {
  // t shifts the pattern through time
  let v = 0;
  v += Math.sin(x * 0.3 + t * 0.5) * Math.cos(z * 0.4 + t * 0.3) * 0.5;
  v += Math.sin(x * 0.7 - t * 0.2) * Math.cos(z * 0.6 + t * 0.4) * 0.3;
  v += Math.sin(x * 1.3 + z * 0.9 + t * 0.15) * 0.15;
  v += Math.cos(x * 2.1 - z * 1.8 + t * 0.25) * 0.05;
  // Add a central mountain that grows over time
  const cx = GRID/2, cz = GRID/2;
  const dist = Math.sqrt((x-cx)*(x-cx) + (z-cz)*(z-cz)) / (GRID*0.45);
  v += Math.max(0, 1 - dist) * 0.6 * (0.5 + 0.5 * Math.sin(t * 0.3));
  return v;
}
for (let t = 0; t < TIME_STEPS; t++) {
  const hf = new Float32Array(GRID * GRID);
  const dn = new Float32Array(GRID * GRID);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iz * GRID + ix;
      // Height: revenue proxy (normalized 0-1)
      let h = noise2D(ix, iz, t);
      h = (h + 1) / 2; // remap to 0-1
      // Add some local spikes for "high revenue moments"
      if (rng() < 0.03) h = Math.min(1, h + rng() * 0.4);
      hf[i] = h;
      // Density: independent secondary metric (0-1)
      let d = noise2D(ix + 5, iz + 5, t * 0.7);
      d = (d + 1) / 2;
      // Density hotspots follow revenue peaks with lag
      d = d * 0.6 + h * 0.4;
      dn[i] = d;
    }
  }
  allHeightfields.push(hf);
  allDensities.push(dn);
}
// Error river control points: 3 paths that shift positions over time.
// Each river is defined by a sequence of [x,z] control points.
function getRiverPaths(timeIdx) {
  // Base anchor points with time-dependent offsets
  const paths = [];
  const basePaths = [
    [[8,5],[18,15],[28,25],[38,35],[42,40]],       // diagonal cut
    [[5,30],[12,25],[22,22],[32,18],[40,15]],       // curved valley
    [[25,5],[28,15],[24,25],[30,35],[25,45]]         // meander
  ];
  for (const base of basePaths) {
    const pts = base.map(([bx, bz]) => {
      // Shift control points slightly based on time
      const shift = Math.sin(timeIdx * 0.5 + bx * 0.1 + bz * 0.1) * 2;
      // Height at this grid position for the current time
      const gi = Math.round(bz) * GRID + Math.round(bx);
      const h = allHeightfields[timeIdx][Math.min(GRID*GRID-1, Math.max(0, gi))];
      return [bx + shift * 0.3, bz + shift * 0.2, h * MAX_HEIGHT + 0.15];
    });
    paths.push(pts);
  }
  return paths;
}
// Particle flow paths: API call trails flowing through terrain valleys.
function getParticlePaths(timeIdx) {
  // Generate paths that follow low-elevation routes (valleys = high traffic)
  const paths = [];
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    // Each particle gets a unique seed so its path evolves differently over time
    const seed = mulberry32(1000 + p + timeIdx * 10000);
    const points = [];
    let cx = seed() * GRID;
    let cz = seed() * GRID;
    const steps = 8 + Math.floor(seed() * 12);
    for (let s = 0; s < steps; s++) {
      const gi = Math.round(cz) * GRID + Math.round(cx);
      const h = allHeightfields[timeIdx][Math.min(GRID*GRID-1, Math.max(0, gi))];
      points.push([cx, cz, h * MAX_HEIGHT + 0.3]);
      // Flow towards lower elevation (gradient descent with noise)
      cx += (seed() - 0.5) * 6;
      cz += (seed() - 0.5) * 6;
      cx = Math.max(1, Math.min(GRID-2, cx));
      cz = Math.max(1, Math.min(GRID-2, cz));
    }
    paths.push(points);
  }
  return paths;
}
// ── THREE.JS SCENE SETUP ──────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 30, 90);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 1, 150);
camera.position.set(25, 18, 35);
camera.lookAt(TERRAIN_SIZE/2, 0, TERRAIN_SIZE/2);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
// Lighting
const ambientLight = new THREE.AmbientLight('#304060', 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffe8c0', 4.5);
sunLight.position.set(30, 25, 20);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -30; sunLight.shadow.camera.right = 30;
sunLight.shadow.camera.top = 30; sunLight.shadow.camera.bottom = -30;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#8090c0', 0.8);
fillLight.position.set(-15, 5, -10);
scene.add(fillLight);
// Ground base plane
const groundGeo = new THREE.PlaneGeometry(TERRAIN_SIZE + 4, TERRAIN_SIZE + 4);
const groundMat = new THREE.MeshStandardMaterial({ color:'#111122', roughness:0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.set(TERRAIN_SIZE/2, -0.15, TERRAIN_SIZE/2);
ground.receiveShadow = true;
scene.add(ground);
// ── ORBIT CONTROLS ────────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(TERRAIN_SIZE/2, MAX_HEIGHT/3, TERRAIN_SIZE/2);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 8;
controls.maxDistance = 70;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// Camera bookmarks
const bookmarks = {
  overview: { pos: [25, 18, 35], target: [TERRAIN_SIZE/2, 0, TERRAIN_SIZE/2] },
  north: { pos: [TERRAIN_SIZE/2, 12, TERRAIN_SIZE+15], target: [TERRAIN_SIZE/2, 2, TERRAIN_SIZE/2] },
  valley: { pos: [10, 5, 5], target: [15, 1, 15] }
};
// User-saved bookmarks
const userBookmarks = [];
function flyTo(pos, target) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...pos);
  const endTarget = new THREE.Vector3(...target);
  const startTime = performance.now();
  const duration = 1200;
  function animate(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out cubic
    const ease = t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3)/2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
}
// ── TERRAIN MESH ──────────────────────────────────────────────
// Single BufferGeometry — attributes mutated on time change.
const terrainGeo = new THREE.BufferGeometry();
const vertexCount = GRID * GRID;
const positions = new Float32Array(vertexCount * 3);
const colors = new Float32Array(vertexCount * 3);
// Build index buffer for the grid
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
terrainGeo.setIndex(indices);
terrainGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ── DENSITY-TO-COLOR MAPPING ──────────────────────────────────
// Maps density (0-1) to a vegetation-to-heat gradient.
function densityToColor(density) {
  // 0.0=dark green -> 0.3=lime -> 0.5=yellow -> 0.7=orange -> 1.0=deep red
  const stops = [
    [0.0, [0.18, 0.31, 0.09]],   // dark green
    [0.25,[0.30, 0.55, 0.15]],   // mid green
    [0.45,[0.55, 0.75, 0.20]],   // yellow-green
    [0.60,[0.85, 0.70, 0.15]],   // golden
    [0.78,[0.90, 0.42, 0.10]],   // orange
    [1.0, [0.50, 0.05, 0.05]]    // deep red
  ];
  let lo = stops[0], hi = stops[stops.length-1];
  for (let i = 0; i < stops.length-1; i++) {
    if (density >= stops[i][0] && density <= stops[i+1][0]) { lo = stops[i]; hi = stops[i+1]; break; }
  }
  const range = hi[0] - lo[0];
  const t = range === 0 ? 0 : (density - lo[0]) / range;
  return [
    lo[1][0] + (hi[1][0] - lo[1][0]) * t,
    lo[1][1] + (hi[1][1] - lo[1][1]) * t,
    lo[1][2] + (hi[1][2] - lo[1][2]) * t
  ];
}
// ── UPDATE TERRAIN FOR TIME STEP (with caching) ───────────────
function updateTerrain(timeIdx) {
  // Check heightfield cache
  let hfData = heightfieldCache.get(timeIdx);
  if (!hfData) {
    // Build heightfield data: world-space heights for each vertex
    hfData = new Float32Array(vertexCount);
    const srcHf = allHeightfields[timeIdx];
    for (let i = 0; i < vertexCount; i++) {
      hfData[i] = srcHf[i] * MAX_HEIGHT;
    }
    heightfieldCache.set(timeIdx, hfData);
  }
  // Check color cache
  let colData = colorCache.get(timeIdx);
  if (!colData) {
    colData = new Float32Array(vertexCount * 3);
    const srcDn = allDensities[timeIdx];
    for (let i = 0; i < vertexCount; i++) {
      const rgb = densityToColor(srcDn[i]);
      colData[i*3] = rgb[0];
      colData[i*3+1] = rgb[1];
      colData[i*3+2] = rgb[2];
    }
    colorCache.set(timeIdx, colData);
  }
  // Update position buffer: set Y from cached heights
  const posAttr = terrainGeo.attributes.position;
  const posArr = posAttr.array;
  const step = TERRAIN_SIZE / (GRID - 1);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iz * GRID + ix;
      const i3 = i * 3;
      posArr[i3] = ix * step;           // X unchanged
      posArr[i3+1] = hfData[i];         // Y = cached height
      posArr[i3+2] = iz * step;         // Z unchanged
    }
  }
  posAttr.needsUpdate = true;
  // Update color buffer from cache
  const colAttr = terrainGeo.attributes.color;
  colAttr.array.set(colData);
  colAttr.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  terrainGeo.index.needsUpdate = true;
}
// ── RIVER GEOMETRY (cached TubeGeometry per time step) ────────
let riverGroup = new THREE.Group();
scene.add(riverGroup);
const riverMaterial = new THREE.MeshStandardMaterial({
  color: '#ff4444', roughness: 0.3, metalness: 0.4, emissive: '#330000', emissiveIntensity: 0.6
});
function updateRivers(timeIdx) {
  let cached = riverCache.get(timeIdx);
  if (cached) {
    // Reuse cached geometries — just swap children
    riverGroup.clear();
    for (const geo of cached) riverGroup.add(new THREE.Mesh(geo, riverMaterial));
    return;
  }
  // Build new river geometries
  const paths = getRiverPaths(timeIdx);
  const geos = [];
  riverGroup.clear();
  for (const pts of paths) {
    // Build 3D curve from control points
    const vec3pts = pts.map(([x, z, y]) => new THREE.Vector3(
      (x / GRID) * TERRAIN_SIZE,
      y,
      (z / GRID) * TERRAIN_SIZE
    ));
    const curve = new THREE.CatmullRomCurve3(vec3pts, false, 'catmullrom', 0.5);
    // TubeGeometry: tubular path through terrain
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.25, 8, false);
    geos.push(tubeGeo);
    const tubeMesh = new THREE.Mesh(tubeGeo, riverMaterial);
    tubeMesh.castShadow = true;
    tubeMesh.receiveShadow = true;
    riverGroup.add(tubeMesh);
  }
  riverCache.set(timeIdx, geos);
}
// ── PARTICLE SYSTEM (API call trails) ─────────────────────────
// Uses BufferGeometry with reusable position array — no per-frame allocations.
const particleGeo = new THREE.BufferGeometry();
const particlePositionsArr = new Float32Array(PARTICLE_COUNT * 3);
// Store full paths for each particle so we can step through them
let particlePaths = [];        // Array<Array<[x,z,y]>> — one per particle
let particleProgress = new Float32Array(PARTICLE_COUNT); // 0-1 progress along path
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositionsArr, 3));
const particleMat = new THREE.PointsMaterial({
  color: '#4ecdc4',
  size: 0.18,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
// Cache for particle start positions per time step (avoid recomputing paths on re-entry)
const particlePathCache = new Map(); // timeIdx -> {paths, progress}
function updateParticles(timeIdx) {
  // Check particle path cache
  let cachedPaths = particlePathCache.get(timeIdx);
  if (!cachedPaths) {
    const rawPaths = getParticlePaths(timeIdx);
    // Convert grid coords to world coords
    const worldPaths = rawPaths.map(path =>
      path.map(([gx, gz, gy]) => [
        (gx / GRID) * TERRAIN_SIZE,
        gy,
        (gz / GRID) * TERRAIN_SIZE
      ])
    );
    cachedPaths = { paths: worldPaths, progress: new Float32Array(PARTICLE_COUNT) };
    particlePathCache.set(timeIdx, cachedPaths);
  }
  particlePaths = cachedPaths.paths;
  // Reset all progress to random start points along their paths
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    cachedPaths.progress[p] = Math.random();
  }
  particleProgress = cachedPaths.progress;
}
// ── CROSSHAIR + TOOLTIP (world-position query) ────────────────
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltipEl = document.getElementById('tooltip');
const ttRev = document.getElementById('tt-rev');
const ttDen = document.getElementById('tt-den');
const ttErr = document.getElementById('tt-err');
// Memoized world-to-grid transform using cache
function worldToGrid(wx, wz) {
  const key = `${wx.toFixed(1)},${wz.toFixed(1)}`;
  let cached = gridXformCache.get(key);
  if (cached) return cached;
  const gx = Math.round((wx / TERRAIN_SIZE) * (GRID - 1));
  const gz = Math.round((wz / TERRAIN_SIZE) * (GRID - 1));
  cached = {
    gx: Math.max(0, Math.min(GRID-1, gx)),
    gz: Math.max(0, Math.min(GRID-1, gz))
  };
  gridXformCache.set(key, cached);
  return cached;
}
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const { gx, gz } = worldToGrid(pt.x, pt.z);
    const idx = gz * GRID + gx;
    const timeIdx = currentTimeIdx;
    const h = allHeightfields[timeIdx][idx];
    const d = allDensities[timeIdx][idx];
    // Count nearby error river points
    let nearErrors = 0;
    const paths = getRiverPaths(timeIdx);
    for (const riverPts of paths) {
      for (const [rx, rz] of riverPts) {
        if (Math.abs(rx - gx) < 3 && Math.abs(rz - gz) < 3) nearErrors++;
      }
    }
    ttRev.textContent = `$${(h * 50000).toFixed(0)}`;
    ttDen.textContent = `${(d * 100).toFixed(0)}%`;
    ttErr.textContent = nearErrors > 0 ? `${nearErrors} nearby` : 'None';
    tooltipEl.style.left = (e.clientX + 18) + 'px';
    tooltipEl.style.top = (e.clientY - 10) + 'px';
    tooltipEl.classList.add('visible');
  } else {
    tooltipEl.classList.remove('visible');
  }
});
// ── TIME CONTROL ──────────────────────────────────────────────
let currentTimeIdx = 12;
let isPlaying = false;
let lastTimeStep = performance.now();
const TIME_STEP_MS = 800; // ms between time steps when playing
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const timeBtn = document.getElementById('time-btn');
// Debounce helper: delays river rebuilds on rapid slider changes
let riverDebounceTimer = null;
function debouncedUpdateRivers(timeIdx) {
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    updateRivers(timeIdx);
    riverDebounceTimer = null;
  }, 200); // 200ms debounce as required
}
function setTimeStep(idx) {
  idx = Math.max(0, Math.min(TIME_STEPS-1, idx));
  if (idx === currentTimeIdx) return;
  currentTimeIdx = idx;
  timeSlider.value = idx;
  timeLabel.textContent = `Hour ${idx}:00`;
  // Grid transform cache invalidated on time change (heights shift)
  gridXformCache.clear();
  // Update terrain (positions + colors) from cache
  updateTerrain(idx);
  // Debounce river rebuild
  debouncedUpdateRivers(idx);
  // Update particle paths
  updateParticles(idx);
  // Update diagnostic panel
  updateDiagnostics();
}
timeSlider.addEventListener('input', () => {
  setTimeStep(parseInt(timeSlider.value));
});
timeBtn.addEventListener('click', () => {
  isPlaying = !isPlaying;
  timeBtn.textContent = isPlaying ? 'PAUSE' : 'PLAY';
  timeBtn.classList.toggle('paused', !isPlaying);
  lastTimeStep = performance.now();
});
// ── BOOKMARK BUTTONS ──────────────────────────────────────────
document.querySelectorAll('.bm-btn[data-bm]').forEach(btn => {
  btn.addEventListener('click', () => {
    const name = btn.dataset.bm;
    if (bookmarks[name]) {
      flyTo(bookmarks[name].pos, bookmarks[name].target);
    } else {
      // Check user bookmarks
      for (const ub of userBookmarks) {
        if (ub.name === name) { flyTo(ub.pos, ub.target); return; }
      }
    }
  });
});
document.getElementById('bm-save-btn').addEventListener('click', () => {
  const name = `View ${userBookmarks.length + 1}`;
  userBookmarks.push({
    name,
    pos: camera.position.toArray(),
    target: controls.target.toArray()
  });
  // Add button dynamically
  const btn = document.createElement('button');
  btn.className = 'bm-btn';
  btn.dataset.bm = name;
  btn.textContent = name;
  btn.addEventListener('click', () => flyTo(userBookmarks.find(b => b.name === name).pos, userBookmarks.find(b => b.name === name).target));
  document.getElementById('bookmarks').appendChild(btn);
});
// ── DIAGNOSTIC PANEL UPDATE ───────────────────────────────────
function updateDiagnostics() {
  document.getElementById('diag-hf-hit').textContent = heightfieldCache.hits;
  document.getElementById('diag-hf-miss').textContent = heightfieldCache.misses;
  document.getElementById('diag-hf-rate').textContent = heightfieldCache.rate + '%';
  document.getElementById('diag-col-hit').textContent = colorCache.hits;
  document.getElementById('diag-col-miss').textContent = colorCache.misses;
  document.getElementById('diag-col-rate').textContent = colorCache.rate + '%';
  document.getElementById('diag-riv-hit').textContent = riverCache.hits;
  document.getElementById('diag-riv-miss').textContent = riverCache.misses;
  document.getElementById('diag-riv-rate').textContent = riverCache.rate + '%';
  document.getElementById('diag-xf-hit').textContent = gridXformCache.hits;
  document.getElementById('diag-xf-miss').textContent = gridXformCache.misses;
  document.getElementById('diag-xf-rate').textContent = gridXformCache.rate + '%';
}
// FPS counter (rolling average)
let fpsFrames = 0;
let fpsLastTime = performance.now();
let fpsDisplay = 0;
// ── ANIMATION LOOP ────────────────────────────────────────────
function animate(timestamp) {
  requestAnimationFrame(animate);
  // Auto-play time steps
  if (isPlaying && timestamp - lastTimeStep > TIME_STEP_MS) {
    lastTimeStep = timestamp;
    const next = (currentTimeIdx + 1) % TIME_STEPS;
    setTimeStep(next);
  }
  // Animate particles along their paths
  // Reuse position array — no per-frame allocations.
  const posArr = particleGeo.attributes.position.array;
  const speed = 0.004; // progress per frame
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    const path = particlePaths[p];
    if (!path || path.length < 2) continue;
    // Advance progress, wrap around
    particleProgress[p] += speed;
    if (particleProgress[p] >= 1.0) particleProgress[p] -= 1.0;
    // Interpolate position along path
    const segCount = path.length - 1;
    const rawIdx = particleProgress[p] * segCount;
    const seg = Math.floor(rawIdx);
    const frac = rawIdx - seg;
    const s = Math.min(seg, segCount - 1);
    const a = path[s], b = path[s+1];
    posArr[p*3] = a[0] + (b[0] - a[0]) * frac;
    posArr[p*3+1] = a[1] + (b[1] - a[1]) * frac;
    posArr[p*3+2] = a[2] + (b[2] - a[2]) * frac;
  }
  particleGeo.attributes.position.needsUpdate = true;
  controls.update();
  renderer.render(scene, camera);
  // FPS counter
  fpsFrames++;
  if (timestamp - fpsLastTime >= 1000) {
    fpsDisplay = Math.round(fpsFrames / ((timestamp - fpsLastTime) / 1000));
    document.getElementById('diag-fps').textContent = fpsDisplay;
    fpsFrames = 0;
    fpsLastTime = timestamp;
  }
}
// ── INIT ──────────────────────────────────────────────────────
// Initial terrain + rivers + particles at time step 12
updateTerrain(currentTimeIdx);
updateRivers(currentTimeIdx);
updateParticles(currentTimeIdx);
updateDiagnostics();
// Handle window resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Expose for console debugging
window.__terrain = {
  heightfieldCache, colorCache, riverCache, gridXformCache,
  setTimeStep, flyTo, bookmarks, userBookmarks,
  get currentTime() { return currentTimeIdx; }
};
// Start render loop
requestAnimationFrame(animate);
</script>
</body>
</html>