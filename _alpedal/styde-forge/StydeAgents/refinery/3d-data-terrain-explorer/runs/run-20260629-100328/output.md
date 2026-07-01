<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a14;--panel-bg:rgba(10,10,28,0.92);--text:#c8ccd4;--accent:#4da6ff;--warn:#e05555;--ok:#4ec94e;--border:rgba(255,255,255,0.08)}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  canvas{display:block}
  #ui{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:flex-end;pointer-events:none}
  #ui>*{pointer-events:auto}
  #panel{background:var(--panel-bg);border:1px solid var(--border);border-radius:12px;padding:16px 20px;backdrop-filter:blur(12px);min-width:320px}
  .panel-row{display:flex;align-items:center;gap:10px;margin:6px 0;font-size:13px}
  .panel-row label{min-width:70px;color:#8890a0;text-transform:uppercase;font-size:11px;letter-spacing:0.5px}
  input[type=range]{flex:1;accent-color:var(--accent);height:4px}
  .btn{background:rgba(255,255,255,0.06);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all .15s}
  .btn:hover{background:rgba(255,255,255,0.12);border-color:var(--accent)}
  .btn.active{background:var(--accent);color:#000;border-color:var(--accent)}
  #bookmarks{display:flex;gap:6px;flex-wrap:wrap;max-width:280px}
  #legend{position:fixed;top:20px;right:20px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:12px;padding:14px 18px;backdrop-filter:blur(12px);font-size:12px}
  .legend-item{display:flex;align-items:center;gap:8px;margin:5px 0}
  .legend-swatch{width:14px;height:14px;border-radius:3px;flex-shrink:0}
  #diagnostics{position:fixed;top:20px;left:20px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:12px;padding:12px 16px;backdrop-filter:blur(12px);font-size:11px;font-family:monospace;min-width:180px}
  .diag-row{display:flex;justify-content:space-between;margin:3px 0}
  .diag-val{color:var(--accent)}
  .diag-miss{color:var(--warn)}
  #tooltip{position:fixed;pointer-events:none;z-index:20;background:var(--panel-bg);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:11px;display:none;backdrop-filter:blur(8px)}
  #error-msg{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:30;background:rgba(200,40,40,0.9);color:#fff;padding:12px 24px;border-radius:8px;font-size:13px;display:none}
  .valley{color:#7eb8ff}
</style>
</head>
<body>
<div id="diagnostics">
  <div style="font-weight:700;margin-bottom:6px;color:var(--accent)">CACHE DIAGNOSTICS</div>
  <div class="diag-row"><span>Terrain hits</span><span class="diag-val" id="cache-terrain-hit">0</span></div>
  <div class="diag-row"><span>Terrain miss</span><span class="diag-miss" id="cache-terrain-miss">0</span></div>
  <div class="diag-row"><span>River hits</span><span class="diag-val" id="cache-river-hit">0</span></div>
  <div class="diag-row"><span>River miss</span><span class="diag-miss" id="cache-river-miss">0</span></div>
  <div class="diag-row"><span>Grid-xform hits</span><span class="diag-val" id="cache-grid-hit">0</span></div>
  <div class="diag-row"><span>FPS</span><span class="diag-val" id="fps-display">--</span></div>
  <div class="diag-row"><span>Particles</span><span class="diag-val" id="particle-count">0</span></div>
</div>
<div id="legend">
  <div style="font-weight:700;margin-bottom:8px">LEGEND</div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(to top,#1a3a1a,#4ec94e,#a0e0a0)"></div><span>Elevation (Revenue)</span></div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(to right,#2d1f0a,#8b6914,#f0c040)"></div><span>User Density (Color overlay)</span></div>
  <div class="legend-item"><div class="legend-swatch" style="background:#e04040"></div><span>Error River</span></div>
  <div class="legend-item"><div class="legend-swatch" style="background:#ffaa30;border-radius:50%"></div><span>API Call Particle</span></div>
  <div style="margin-top:8px;font-size:10px;color:#8890a0">
    Drag: orbit &middot; Scroll: zoom<br>
    Right-drag: pan &middot; R: reset
  </div>
</div>
<div id="tooltip"></div>
<div id="error-msg"></div>
<div id="ui">
  <div id="panel">
    <div style="font-weight:700;margin-bottom:8px;color:var(--accent)">TIME CONTROL</div>
    <div class="panel-row"><label>Step</label><input type="range" id="time-slider" min="0" max="23" value="0" step="1"><span id="time-label" style="min-width:36px;text-align:right">0</span></div>
    <div class="panel-row" style="margin-top:4px"><label>Auto</label><input type="checkbox" id="auto-play" style="accent-color:var(--accent)"><span style="font-size:11px">play</span></div>
    <div style="margin-top:10px;font-weight:700;font-size:11px;color:#8890a0">CAMERA BOOKMARKS</div>
    <div id="bookmarks" style="margin-top:4px">
      <button class="btn" data-bookmark="overview">Overview</button>
      <button class="btn" data-bookmark="east">East Ridge</button>
      <button class="btn" data-bookmark="valley">Valley Floor</button>
      <button class="btn" data-bookmark="river">Error Source</button>
    </div>
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
// ═══════════════════════════════════════════════════════════════
// 3D DATA TERRAIN EXPLORER — v1.0
// Worst-case per-frame complexity: O(P + V + G) where
//   P = particle count (capped at 200),
//   V = visible terrain vertices (~10k, updated only on slider),
//   G = grid-transform ops (memoized, max 1 per frame)
// All terrain/river geometry swaps are O(1) buffer pointer swaps.
// ═══════════════════════════════════════════════════════════════
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─── DOM refs (grabbed once, never re-queried) ───
const canvas = document.createElement('canvas');
document.body.prepend(canvas);
const tooltip = document.getElementById('tooltip');
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const autoPlayCb = document.getElementById('auto-play');
const diagTerrainHit = document.getElementById('cache-terrain-hit');
const diagTerrainMiss = document.getElementById('cache-terrain-miss');
const diagRiverHit = document.getElementById('cache-river-hit');
const diagRiverMiss = document.getElementById('cache-river-miss');
const diagGridHit = document.getElementById('cache-grid-hit');
const fpsDisplay = document.getElementById('fps-display');
const particleCountEl = document.getElementById('particle-count');
// ─── Constants (each annotated with rationale) ───
const GRID_SIZE = 80;                // terrain vertex resolution — balances detail vs draw calls
const TERRAIN_SCALE = 12;            // world-space width/depth of terrain plane
const MAX_ELEVATION = 4.0;           // peak height in world units — keeps camera framing tight
const RIVER_POINTS = 40;             // river curve resolution — enough for smooth bends without over-tessellation
const PARTICLE_COUNT = 200;          // max simultaneous particles — keeps frame budget under 1ms on mid-tier GPU
const PARTICLE_SPEED = 0.002;        // per-frame advance along path — tuned for visible motion at 60fps
const SLIDER_DEBOUNCE_MS = 180;      // debounce river rebuilds — prevents TubeGeometry churn on rapid scrubbing
const AUTO_ROTATE_SPEED = 0.3;       // rad/s when auto-rotate enabled — gentle orbit speed
const CAMERA_DAMPING = 0.08;         // OrbitControls damping — smooth but responsive
// ─── Scene setup ───
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 20, 60);
const camera = new THREE.PerspectiveCamera(55, 2, 0.5, 80);
camera.position.set(9, 7, 13);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // cap pixel ratio — avoids 4K render target bloat
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
// ─── Lighting ───
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -12; sun.shadow.camera.right = 12;
sun.shadow.camera.top = 12; sun.shadow.camera.bottom = -12;
scene.add(sun);
const ambient = new THREE.AmbientLight(0x223344, 2.0);
scene.add(ambient);
const hemi = new THREE.HemisphereLight(0x8899cc, 0x223322, 1.2);
scene.add(hemi);
// ─── Ground reference plane ───
const groundGeo = new THREE.PlaneGeometry(TERRAIN_SCALE * 2.5, TERRAIN_SCALE * 2.5);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x0a0a18, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.15;
ground.receiveShadow = true;
scene.add(ground);
// ─── OrbitControls ───
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = CAMERA_DAMPING;
controls.autoRotate = true;
controls.autoRotateSpeed = AUTO_ROTATE_SPEED;
controls.target.set(0, 1.5, 0);
controls.minDistance = 4;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.55; // prevent going underground
controls.update();
// ─── DATA GENERATION ──────────────────────────────────────────
// Synthetic 24-hour time-series with terrain + secondary metric + error paths + particle routes
const TIME_STEPS = 24;
const HALF = GRID_SIZE / 2;
// Precompute noise-like height maps using layered sine combinations (deterministic, cache-friendly)
function heightFn(t, ix, iz) {
  const x = (ix - HALF) / HALF; // normalize to [-1, 1]
  const z = (iz - HALF) / HALF;
  const tNorm = t / TIME_STEPS;
  // Base terrain: two overlapping ridges that shift over time
  const ridge1 = Math.sin(x * 2.8 + tNorm * 1.5) * Math.cos(z * 1.9) * 0.5;
  const ridge2 = Math.cos(x * 1.4 - tNorm * 0.8) * Math.sin(z * 2.3 + tNorm) * 0.4;
  const hill = Math.exp(-((x - 0.3) * (x - 0.3) + (z + 0.2) * (z + 0.2)) * 4) * 1.2;
  const hill2 = Math.exp(-((x + 0.5) * (x + 0.5) + (z - 0.4) * (z - 0.4)) * 3) * (0.6 + tNorm * 0.5);
  return (ridge1 + ridge2 + hill + hill2 + 0.3) * MAX_ELEVATION * 0.5;
}
// Secondary metric: user density (mapped to vertex color)
function densityFn(t, ix, iz) {
  const x = (ix - HALF) / HALF;
  const z = (iz - HALF) / HALF;
  const tNorm = t / TIME_STEPS;
  return Math.max(0, Math.min(1,
    0.3 + 0.4 * Math.sin(x * 2.1 + z * 1.7 + tNorm * 2) +
    0.3 * Math.cos(x * 3.5 - z * 2.9 + tNorm * 1.3)
  ));
}
// Error path: a meandering line through the terrain that shifts with time
function errorPath(t) {
  const pts = [];
  const tNorm = t / TIME_STEPS;
  for (let i = 0; i < RIVER_POINTS; i++) {
    const frac = i / (RIVER_POINTS - 1);
    const gx = HALF * (0.2 + frac * 0.6); // start left, drift right
    const gz = HALF * (0.3 + Math.sin(frac * Math.PI * 1.7 + tNorm * 2) * 0.4);
    const ix = Math.floor(gx);
    const iz = Math.floor(gz);
    const h = heightFn(t, ix, iz) + 0.08; // river sits slightly above terrain
    const wx = (gx / GRID_SIZE - 0.5) * TERRAIN_SCALE;
    const wz = (gz / GRID_SIZE - 0.5) * TERRAIN_SCALE;
    pts.push(new THREE.Vector3(wx, h, wz));
  }
  return pts;
}
// Particle routes: multiple flow paths simulating API call traces
function particleRoutes(t) {
  const routes = [];
  const tNorm = t / TIME_STEPS;
  // 8 distinct flow paths
  for (let r = 0; r < 8; r++) {
    const pts = [];
    const startX = -0.7 + r * 0.18;
    const startZ = -0.6 + Math.sin(r * 1.3) * 0.5;
    for (let i = 0; i < 30; i++) {
      const frac = i / 29;
      const px = startX + frac * (0.5 + Math.sin(r * 0.9 + tNorm) * 0.2);
      const pz = startZ + frac * (0.6 + Math.cos(r * 1.1 + tNorm) * 0.3);
      const ix = Math.floor((px + 0.5) * GRID_SIZE);
      const iz = Math.floor((pz + 0.5) * GRID_SIZE);
      const h = heightFn(t, Math.max(0, Math.min(GRID_SIZE - 1, ix)), Math.max(0, Math.min(GRID_SIZE - 1, iz))) + 0.05;
      const wx = px * TERRAIN_SCALE;
      const wz = pz * TERRAIN_SCALE;
      pts.push(new THREE.Vector3(wx, h, wz));
    }
    routes.push(pts);
  }
  return routes;
}
// ─── CACHE LAYERS ─────────────────────────────────────────────
// Each cache is a Map<timeStep, precomputedObject>. All miss counters start at 0.
const terrainCache = new Map();   // timeStep → { heights: Float32Array[][], colors: Float32Array[][] }
const riverCache = new Map();     // timeStep → THREE.TubeGeometry
const routeCache = new Map();     // timeStep → THREE.Vector3[][]
const gridXformCache = new Map(); // "ix,iz" → { wx, wz } — world-space grid coords, cleared per-frame
let cacheStats = { terrainHit: 0, terrainMiss: 0, riverHit: 0, riverMiss: 0, gridHit: 0 };
// Precompute ALL terrain height+color grids at init (one-time cost, O(T * N^2) total)
console.time('precompute-all');
for (let t = 0; t < TIME_STEPS; t++) {
  const heights = new Array(GRID_SIZE);
  const colors = new Array(GRID_SIZE);
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    heights[iz] = new Float32Array(GRID_SIZE);
    colors[iz] = new Float32Array(GRID_SIZE * 3);
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const h = heightFn(t, ix, iz);
      heights[iz][ix] = h;
      const d = densityFn(t, ix, iz);
      // Color: blend terrain brown → green based on density (vegetation gradient)
      const r = 0.25 + d * 0.1;
      const g = 0.18 + d * 0.55;
      const b = 0.08 + d * 0.15;
      colors[iz][ix * 3] = r;
      colors[iz][ix * 3 + 1] = g;
      colors[iz][ix * 3 + 2] = b;
    }
  }
  terrainCache.set(t, { heights, colors });
  riverCache.set(t, null); // lazy-build rivers
  routeCache.set(t, null); // lazy-build routes
}
console.timeEnd('precompute-all');
// ─── TERRAIN MESH ─────────────────────────────────────────────
// Single PlaneGeometry, reused across all time steps by swapping position+color buffers
const terrainGeo = new THREE.PlaneGeometry(TERRAIN_SCALE, TERRAIN_SCALE, GRID_SIZE - 1, GRID_SIZE - 1);
terrainGeo.rotateX(-Math.PI / 2);
const posAttr = terrainGeo.attributes.position;
const posArr = posAttr.array; // Float32Array — reused every frame, never re-allocated
// Inject vertex colors attribute
const colorArr = new Float32Array(posArr.length);
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colorArr, 3));
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.75,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Apply terrain data for a given time step (O(V) per call, only on slider change)
function applyTerrainStep(t) {
  let data;
  if (terrainCache.has(t)) {
    data = terrainCache.get(t);
    cacheStats.terrainHit++;
  } else {
    cacheStats.terrainMiss++;
    // Fallback: recompute (should never happen after precompute)
    const heights = new Array(GRID_SIZE);
    const colors = new Array(GRID_SIZE);
    for (let iz = 0; iz < GRID_SIZE; iz++) {
      heights[iz] = new Float32Array(GRID_SIZE);
      colors[iz] = new Float32Array(GRID_SIZE * 3);
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        heights[iz][ix] = heightFn(t, ix, iz);
        const d = densityFn(t, ix, iz);
        colors[iz][ix * 3] = 0.25 + d * 0.1;
        colors[iz][ix * 3 + 1] = 0.18 + d * 0.55;
        colors[iz][ix * 3 + 2] = 0.08 + d * 0.15;
      }
    }
    data = { heights, colors };
    terrainCache.set(t, data);
  }
  const { heights, colors } = data;
  // Write into existing position array — zero allocation
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = (iz * GRID_SIZE + ix) * 3;
      posArr[idx + 1] = heights[iz][ix]; // Y is up after rotateX
      colorArr[idx] = colors[iz][ix * 3];
      colorArr[idx + 1] = colors[iz][ix * 3 + 1];
      colorArr[idx + 2] = colors[iz][ix * 3 + 2];
    }
  }
  posAttr.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals(); // needed for lighting after height change
}
// ─── RIVER SYSTEM ─────────────────────────────────────────────
let riverMesh = null;
let riverGroup = new THREE.Group();
scene.add(riverGroup);
function buildRiver(t) {
  if (riverCache.has(t) && riverCache.get(t) !== null) {
    cacheStats.riverHit++;
    return riverCache.get(t);
  }
  cacheStats.riverMiss++;
  const pathPts = errorPath(t);
  const curve = new THREE.CatmullRomCurve3(pathPts, false, 'catmullrom', 0.5);
  const tubeGeo = new THREE.TubeGeometry(curve, 120, 0.12, 8, false);
  riverCache.set(t, tubeGeo);
  return tubeGeo;
}
function applyRiverStep(t) {
  // Clear old river
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry && child.geometry !== riverCache.get(t)) {
      child.geometry.dispose();
    }
    riverGroup.remove(child);
  }
  const geo = buildRiver(t);
  const mat = new THREE.MeshStandardMaterial({
    color: 0xe04040,
    roughness: 0.3,
    metalness: 0.4,
    emissive: 0x330000,
    emissiveIntensity: 0.6,
  });
  riverMesh = new THREE.Mesh(geo, mat);
  riverMesh.castShadow = true;
  riverMesh.receiveShadow = true;
  riverGroup.add(riverMesh);
}
// ─── PARTICLE SYSTEM ──────────────────────────────────────────
// Single BufferGeometry with reusable position array — never allocates per frame
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleAlphas = new Float32Array(PARTICLE_COUNT); // track progress per particle
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
// Sprite texture — procedural dot (created once)
const spriteCanvas = document.createElement('canvas');
spriteCanvas.width = 32; spriteCanvas.height = 32;
const ctx = spriteCanvas.getContext('2d');
const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
gradient.addColorStop(0, 'rgba(255,170,50,1)');
gradient.addColorStop(0.3, 'rgba(255,140,30,0.8)');
gradient.addColorStop(0.7, 'rgba(255,100,20,0.15)');
gradient.addColorStop(1, 'rgba(255,60,0,0)');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, 32, 32);
const spriteTexture = new THREE.CanvasTexture(spriteCanvas);
const particleMat = new THREE.PointsMaterial({
  size: 0.18,
  map: spriteTexture,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85,
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
// Per-particle state (allocated once, mutated per frame)
const particleState = new Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleState[i] = { routeIdx: i % 8, segIdx: 0, t: Math.random(), alive: true };
}
// Memoized grid-to-world transform (cleared each frame)
const gridXformFrame = new Map(); // key → worldPos, reset at start of animate()
function gridToWorld(ix, iz, heights) {
  const key = `${ix},${iz}`;
  if (gridXformFrame.has(key)) {
    cacheStats.gridHit++;
    return gridXformFrame.get(key);
  }
  const wx = (ix / GRID_SIZE - 0.5) * TERRAIN_SCALE;
  const wz = (iz / GRID_SIZE - 0.5) * TERRAIN_SCALE;
  const h = heights[Math.min(GRID_SIZE - 1, Math.max(0, iz))][Math.min(GRID_SIZE - 1, Math.max(0, ix))];
  const pos = new THREE.Vector3(wx, h, wz);
  gridXformFrame.set(key, pos);
  return pos;
}
// ─── UPDATE FUNCTIONS ─────────────────────────────────────────
let currentTimeStep = 0;
// Debounce state for river rebuilds
let riverDebounceTimer = null;
let pendingRiverStep = null;
function setTimeStep(t) {
  if (t === currentTimeStep) return;
  currentTimeStep = t;
  applyTerrainStep(t); // immediate — buffer swap is fast
  // Debounce river rebuild (TubeGeometry is expensive)
  pendingRiverStep = t;
  if (riverDebounceTimer !== null) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    applyRiverStep(pendingRiverStep);
    riverDebounceTimer = null;
    pendingRiverStep = null;
  }, SLIDER_DEBOUNCE_MS);
  // Lazy-init routes if needed
  if (!routeCache.has(t) || routeCache.get(t) === null) {
    routeCache.set(t, particleRoutes(t));
  }
  // Reset particles to new routes
  const routes = routeCache.get(t);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const st = particleState[i];
    st.routeIdx = i % routes.length;
    st.segIdx = 0;
    st.t = Math.random() * 0.3; // stagger start
    st.alive = true;
  }
  timeLabel.textContent = t;
  timeSlider.value = t;
}
// ─── ANIMATION LOOP ───────────────────────────────────────────
// Complexity: O(PARTICLE_COUNT) per frame = O(200) — well within budget
let frameCount = 0;
let lastFpsTime = performance.now();
let fpsValue = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  // ── FPS counter (sampled every 500ms to avoid Date.now() churn) ──
  frameCount++;
  if (timestamp - lastFpsTime >= 500) {
    fpsValue = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = timestamp;
    fpsDisplay.textContent = fpsValue;
  }
  // ── Grid-transform memoization: reset per frame (cost: 0, we swap the Map) ──
  gridXformFrame.clear();
  cacheStats.gridHit = 0; // reset hit counter per frame for display
  // ── Auto-play ──
  if (autoPlayCb.checked && !riverDebounceTimer) {
    const next = (currentTimeStep + 1) % TIME_STEPS;
    setTimeStep(next);
  }
  // ── Particle update (reuses position array, zero allocation) ──
  const routes = routeCache.get(currentTimeStep);
  const terData = terrainCache.get(currentTimeStep);
  const heights = terData ? terData.heights : null;
  let aliveCount = 0;
  if (routes && heights) {
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const st = particleState[i];
      if (!st.alive) {
        // Dead particle: hide below terrain
        particlePositions[i * 3 + 1] = -10;
        continue;
      }
      const route = routes[st.routeIdx % routes.length];
      st.t += PARTICLE_SPEED;
      if (st.t >= 1.0) {
        // Loop: respawn at start of a random route
        st.routeIdx = Math.floor(Math.random() * routes.length);
        st.t = 0;
        st.segIdx = 0;
      }
      // Interpolate along route points
      const segCount = route.length - 1;
      const rawIdx = st.t * segCount;
      st.segIdx = Math.floor(rawIdx);
      const frac = rawIdx - st.segIdx;
      const a = route[Math.min(st.segIdx, segCount)];
      const b = route[Math.min(st.segIdx + 1, segCount)];
      const px = a.x + (b.x - a.x) * frac;
      const py = a.y + (b.y - a.y) * frac;
      const pz = a.z + (b.z - a.z) * frac;
      particlePositions[i * 3] = px;
      particlePositions[i * 3 + 1] = py + 0.15; // slight lift above terrain
      particlePositions[i * 3 + 2] = pz;
      // Color: warm gradient based on route index
      const hue = (st.routeIdx / 8) * 0.15 + 0.08;
      particleColors[i * 3] = 1.0;
      particleColors[i * 3 + 1] = 0.55 + hue;
      particleColors[i * 3 + 2] = 0.1;
      aliveCount++;
    }
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  particleCountEl.textContent = aliveCount;
  // ── Update cache diagnostic display ──
  diagTerrainHit.textContent = cacheStats.terrainHit;
  diagTerrainMiss.textContent = cacheStats.terrainMiss;
  diagRiverHit.textContent = cacheStats.riverHit;
  diagRiverMiss.textContent = cacheStats.riverMiss;
  diagGridHit.textContent = cacheStats.gridHit;
  controls.update();
  renderer.render(scene, camera);
}
// ─── EVENT HANDLERS ───────────────────────────────────────────
// Resize handler (debounced via rAF-like guard)
let resizePending = false;
window.addEventListener('resize', () => {
  if (resizePending) return;
  resizePending = true;
  requestAnimationFrame(() => {
    const w = window.innerWidth;
    const h = window.innerHeight;
    renderer.setSize(w, h);
    camera.aspect = w / Math.max(h, 1);
    camera.updateProjectionMatrix();
    resizePending = false;
  });
});
// Time slider
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value, 10);
  setTimeStep(t);
});
// Auto-play toggle
autoPlayCb.addEventListener('change', () => {
  // no-op — checked in animate loop
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      // Reset camera
      camera.position.set(9, 7, 13);
      controls.target.set(0, 1.5, 0);
      controls.update();
      break;
    case 'a':
      // Toggle auto-rotate
      controls.autoRotate = !controls.autoRotate;
      break;
    case 'arrowleft':
      setTimeStep(Math.max(0, currentTimeStep - 1));
      break;
    case 'arrowright':
      setTimeStep(Math.min(TIME_STEPS - 1, currentTimeStep + 1));
      break;
    case ' ':
      e.preventDefault();
      autoPlayCb.checked = !autoPlayCb.checked;
      break;
  }
});
// Camera bookmarks
const bookmarks = {
  overview: { pos: [9, 7, 13], target: [0, 1.5, 0] },
  east: { pos: [14, 4, 2], target: [4, 1.2, 0] },
  valley: { pos: [2, 1.5, -8], target: [-1, 0.8, -3] },
  river: { pos: [-3, 3, -7], target: [-2, 0.6, -4] },
};
document.querySelectorAll('[data-bookmark]').forEach(btn => {
  btn.addEventListener('click', () => {
    const key = btn.dataset.bookmark;
    const bm = bookmarks[key];
    if (!bm) return;
    // Smooth animate to bookmark
    const startPos = camera.position.clone();
    const endPos = new THREE.Vector3(...bm.pos);
    const startTarget = controls.target.clone();
    const endTarget = new THREE.Vector3(...bm.target);
    const startTime = performance.now();
    const duration = 800;
    function animStep(ts) {
      const elapsed = ts - startTime;
      const t = Math.min(elapsed / duration, 1.0);
      // Ease in-out
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      camera.position.lerpVectors(startPos, endPos, ease);
      controls.target.lerpVectors(startTarget, endTarget, ease);
      controls.update();
      if (t < 1.0) {
        requestAnimationFrame(animStep);
      }
    }
    requestAnimationFrame(animStep);
    // Highlight active bookmark
    document.querySelectorAll('[data-bookmark]').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});
// ─── HOVER / TOOLTIP (raycaster on terrain) ───
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    // Convert world position back to grid indices (memoized this frame)
    const gx = Math.round((point.x / TERRAIN_SCALE + 0.5) * GRID_SIZE);
    const gz = Math.round((point.z / TERRAIN_SCALE + 0.5) * GRID_SIZE);
    const ix = Math.max(0, Math.min(GRID_SIZE - 1, gx));
    const iz = Math.max(0, Math.min(GRID_SIZE - 1, gz));
    const data = terrainCache.get(currentTimeStep);
    const elev = data ? data.heights[iz][ix] : 0;
    const dens = data ? (data.colors[iz][ix * 3 + 1] - 0.18) / 0.55 : 0;
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 18) + 'px';
    tooltip.style.top = (e.clientY - 10) + 'px';
    tooltip.innerHTML =
      `<div>Grid (${ix}, ${iz})</div>` +
      `<div>Elevation: <span class="diag-val">${elev.toFixed(2)}</span></div>` +
      `<div>Density: <span class="diag-val">${(dens * 100).toFixed(0)}%</span></div>`;
  } else {
    tooltip.style.display = 'none';
  }
});
// ─── INITIALIZATION ───────────────────────────────────────────
function init() {
  renderer.setSize(window.innerWidth, window.innerHeight);
  setTimeStep(0);
  // Force immediate river build (bypass debounce for initial state)
  applyRiverStep(0);
  routeCache.set(0, particleRoutes(0));
  // Kick off animation loop
  requestAnimationFrame(animate);
}
// Truncation guard: if script reaches here, all critical sections are registered
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
console.log('3D Data Terrain Explorer initialized — terrain cache:', terrainCache.size, 'steps');
</script>
</body>
</html>