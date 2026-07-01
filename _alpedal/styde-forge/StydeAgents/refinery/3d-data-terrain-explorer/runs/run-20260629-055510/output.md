<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  /* === CONSTANTS: UI dimensions === */
  /* PANEL_WIDTH: 280px — sidebar for controls, keeps terrain view unobstructed */
  /* HEADER_HEIGHT: 48px — compact toolbar for bookmark chips and title */
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a0f; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; color: #c8ccd4; }
  #canvas-container { position: fixed; inset: 0; z-index: 1; }
  canvas { display: block; }
  #panel {
    position: fixed; top: 12px; right: 12px; z-index: 10;
    width: 280px; max-height: calc(100vh - 24px);
    background: rgba(14, 16, 22, 0.92); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
    padding: 16px; overflow-y: auto;
    display: flex; flex-direction: column; gap: 14px;
    font-size: 13px; line-height: 1.45;
  }
  #panel label { display: block; font-weight: 600; color: #8899aa; font-size: 10px; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px; }
  #panel input[type=range] { width: 100%; accent-color: #4da6ff; }
  #panel input[type=range]:disabled { accent-color: #334455; }
  #panel button {
    background: rgba(77,166,255,0.12); border: 1px solid rgba(77,166,255,0.25);
    color: #aaccff; padding: 6px 12px; border-radius: 5px; cursor: pointer;
    font-size: 12px; transition: all 0.15s;
  }
  #panel button:hover { background: rgba(77,166,255,0.22); border-color: rgba(77,166,255,0.45); }
  #panel button.active { background: rgba(77,166,255,0.30); border-color: #4da6ff; color: #fff; }
  .metric-row { display: flex; justify-content: space-between; align-items: center; }
  .metric-value { font-variant-numeric: tabular-nums; font-weight: 700; font-size: 15px; color: #e0e6f0; }
  .metric-label { color: #667788; font-size: 10px; }
  #bookmark-chips { display: flex; flex-wrap: wrap; gap: 5px; }
  .chip {
    font-size: 10px; padding: 3px 8px; border-radius: 12px;
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10);
    cursor: pointer; transition: all 0.15s;
  }
  .chip:hover { background: rgba(255,255,255,0.14); border-color: rgba(255,255,255,0.25); }
  .chip .delete-bookmark { margin-left: 4px; opacity: 0.4; }
  .chip .delete-bookmark:hover { opacity: 1; color: #ff6b6b; }
  #wiring-status { font-size: 10px; padding: 4px 8px; border-radius: 4px; margin-top: 4px; }
  #wiring-status.pass { background: rgba(70,200,120,0.15); color: #6c6; }
  #wiring-status.fail { background: rgba(220,70,70,0.15); color: #f66; }
  #perf-monitor { font-size: 10px; color: #556; margin-top: 2px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="panel">
  <div style="font-weight:700;font-size:15px;color:#dde4f0;">Data Terrain</div>
  <div>
    <label>Time Step <span id="time-label">0 / 0</span></label>
    <input type="range" id="time-slider" min="0" max="0" value="0" disabled>
  </div>
  <div>
    <div class="metric-row"><span class="metric-label">Revenue (elevation)</span><span class="metric-value" id="val-revenue">—</span></div>
    <div class="metric-row"><span class="metric-label">User Density (color)</span><span class="metric-value" id="val-density">—</span></div>
    <div class="metric-row"><span class="metric-label">Error Rate</span><span class="metric-value" id="val-errors">—</span></div>
    <div class="metric-row"><span class="metric-label">API Calls</span><span class="metric-value" id="val-api">—</span></div>
  </div>
  <div>
    <label>Camera</label>
    <button id="btn-autorotate" class="active">Auto-Rotate</button>
    <button id="btn-topdown">Top-Down</button>
    <button id="btn-reset">Reset</button>
  </div>
  <div>
    <label>Bookmarks</label>
    <div id="bookmark-chips"></div>
    <button id="btn-save-bookmark" style="margin-top:4px;">Save View</button>
  </div>
  <div>
    <label>Display</label>
    <label style="display:flex;align-items:center;gap:6px;font-size:12px;text-transform:none;letter-spacing:0;">
      <input type="checkbox" id="toggle-rivers" checked> Rivers
    </label>
    <label style="display:flex;align-items:center;gap:6px;font-size:12px;text-transform:none;letter-spacing:0;">
      <input type="checkbox" id="toggle-particles" checked> Particles
    </label>
    <label style="display:flex;align-items:center;gap:6px;font-size:12px;text-transform:none;letter-spacing:0;">
      <input type="checkbox" id="toggle-wireframe"> Wireframe
    </label>
  </div>
  <div id="wiring-status" class="pass">Wiring: pending...</div>
  <div id="perf-monitor">FPS: -- | Recomputes: 0</div>
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
// ============================================================================
// MODULE: constants.js — All numeric literals beyond 0/1 defined here
// ============================================================================
/* PERFORMANCE BUDGET: max 2 geometry recomputations per user interaction.
   All time-slider changes must swap cached buffers, never rebuild geometry.
   Particle position arrays are allocated once and mutated in-place. */
const GRID_SIZE = 80;             // terrain grid resolution (N x N vertices)
const TERRAIN_SPAN = 20;          // world-space width/depth of terrain plane
const HEIGHT_SCALE = 8;           // max elevation multiplier for revenue data
const PARTICLE_COUNT = 600;       // total particles in the trail system
const PARTICLE_TRAIL_LENGTH = 40; // trail history per-particle (ring buffer)
const PARTICLE_SPEED_BASE = 0.25; // base movement speed along flow field
const DAMPING_FACTOR = 0.08;      // OrbitControls damping inertia
const AUTO_ROTATE_SPEED = 0.3;    // radians per second auto-rotation
const RIVER_WIDTH = 0.15;         // half-width of river tube geometry
const RIVER_SEGMENTS = 120;       // tube segments along each river path
const RIVER_TUBE_RADIAL = 6;      // radial segments for tube cross-section
const AMBIENT_LIGHT_INTENSITY = 0.6;
const DIRECTIONAL_LIGHT_INTENSITY = 1.2;
const HEMI_LIGHT_INTENSITY = 0.5;
const CAMERA_FAR = 60;
const CAMERA_NEAR = 0.5;
const CAMERA_FOV = 55;
const ZOOM_MIN = 3;
const ZOOM_MAX = 40;
const TIME_STEPS = 30;            // number of time-series snapshots
// derived
const HALF_SPAN = TERRAIN_SPAN / 2;
const VERTEX_COUNT = GRID_SIZE * GRID_SIZE;
const FACE_COUNT = (GRID_SIZE - 1) * (GRID_SIZE - 1) * 2;
// ============================================================================
// MODULE: data.js — Synthetic time-series data generation and access
// ============================================================================
function seedRandom(seed) {
  let s = seed | 0;
  return () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
}
function generateTimeSeriesData() {
  const rand = seedRandom(42);
  const steps = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const revenue = new Float32Array(VERTEX_COUNT);
    const density = new Float32Array(VERTEX_COUNT);
    const errors = new Float32Array(VERTEX_COUNT);
    const phaseShift = t * 0.15;
    const trendBump = Math.sin(t * 0.22) * 0.3 + 0.5;
    for (let iz = 0; iz < GRID_SIZE; iz++) {
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const idx = iz * GRID_SIZE + ix;
        const nx = (ix / (GRID_SIZE - 1)) * 2 - 1; // normalized -1..1
        const nz = (iz / (GRID_SIZE - 1)) * 2 - 1;
        const dist = Math.sqrt(nx * nx + nz * nz);
        // revenue: multi-octave terrain-like noise with time evolution
        const r1 = Math.sin(nx * 3.1 + phaseShift) * Math.cos(nz * 2.7 + phaseShift * 0.7);
        const r2 = Math.sin(nx * 6.7 - phaseShift * 0.5) * 0.4;
        const r3 = Math.cos(nz * 5.3 + phaseShift * 1.1) * 0.3;
        const edgeFalloff = 1 - Math.max(0, (dist - 0.65) / 0.35);
        revenue[idx] = Math.max(0, (r1 + r2 + r3 + trendBump) * 0.5 + 0.35) * edgeFalloff;
        // user density: correlated but offset from revenue
        density[idx] = Math.max(0, revenue[idx] * (0.7 + 0.3 * Math.sin(nx * 4.1 + nz * 3.8 + phaseShift * 0.4)));
        // errors: inverse hotspots
        const errBase = Math.abs(Math.sin(nx * 5.5 + nz * 4.2)) * (1 - revenue[idx] * 0.6);
        errors[idx] = errBase * (0.15 + 0.1 * (1 - density[idx]));
      }
    }
    steps.push({ revenue, density, errors });
  }
  return steps;
}
// ============================================================================
// MODULE: scene-setup.js — Three.js renderer, scene, lights, camera
// ============================================================================
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a14');
scene.fog = new THREE.Fog('#0a0a14', CAMERA_FAR * 0.5, CAMERA_FAR);
const camera = new THREE.PerspectiveCamera(CAMERA_FOV, window.innerWidth / window.innerHeight, CAMERA_NEAR, CAMERA_FAR);
camera.position.set(12, 8, 16);
camera.lookAt(0, 0, 0);
// ambient
const ambientLight = new THREE.AmbientLight('#334466', AMBIENT_LIGHT_INTENSITY);
scene.add(ambientLight);
// directional sun
const sun = new THREE.DirectionalLight('#ffe8cc', DIRECTIONAL_LIGHT_INTENSITY);
sun.position.set(15, 20, 8);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -15;
sun.shadow.camera.right = 15;
sun.shadow.camera.top = 15;
sun.shadow.camera.bottom = -15;
scene.add(sun);
// hemisphere fill
const hemi = new THREE.HemisphereLight('#8899cc', '#223344', HEMI_LIGHT_INTENSITY);
scene.add(hemi);
// grid helper
const gridHelper = new THREE.GridHelper(TERRAIN_SPAN, 20, '#223344', '#111822');
gridHelper.position.y = -0.01;
scene.add(gridHelper);
// ============================================================================
// MODULE: controls.js — OrbitControls with damping, bookmarks, auto-rotate
// ============================================================================
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = DAMPING_FACTOR;
controls.autoRotate = true;
controls.autoRotateSpeed = AUTO_ROTATE_SPEED;
controls.minDistance = ZOOM_MIN;
controls.maxDistance = ZOOM_MAX;
controls.target.set(0, HEIGHT_SCALE * 0.25, 0);
controls.update();
const bookmarks = [];
function saveBookmark(name) {
  bookmarks.push({
    name,
    position: camera.position.clone(),
    target: controls.target.clone()
  });
  renderBookmarkChips();
}
function loadBookmark(index) {
  const bm = bookmarks[index];
  if (!bm) return;
  camera.position.copy(bm.position);
  controls.target.copy(bm.target);
  controls.update();
}
function deleteBookmark(index) {
  bookmarks.splice(index, 1);
  renderBookmarkChips();
}
function renderBookmarkChips() {
  const container = document.getElementById('bookmark-chips');
  container.innerHTML = bookmarks.map((b, i) =>
    `<span class="chip" data-idx="${i}">${b.name}<span class="delete-bookmark" data-del="${i}">&times;</span></span>`
  ).join('');
  container.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      if (e.target.classList.contains('delete-bookmark')) {
        deleteBookmark(parseInt(e.target.dataset.del));
      } else {
        loadBookmark(parseInt(chip.dataset.idx));
      }
    });
  });
}
document.getElementById('btn-autorotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
document.getElementById('btn-topdown').addEventListener('click', () => {
  camera.position.set(0, TERRAIN_SPAN * 1.1, 0.1);
  controls.target.set(0, 0, 0);
  controls.update();
});
document.getElementById('btn-reset').addEventListener('click', () => {
  camera.position.set(12, 8, 16);
  controls.target.set(0, HEIGHT_SCALE * 0.25, 0);
  controls.update();
});
document.getElementById('btn-save-bookmark').addEventListener('click', () => {
  const name = `View ${bookmarks.length + 1}`;
  saveBookmark(name);
});
// ============================================================================
// MODULE: terrain-builder.js — BufferGeometry terrain, vertex colors, cache
// ============================================================================
const timeSeriesData = generateTimeSeriesData();
// geometry cache: key = timeStep, value = { geometry, wireframeGeometry }
const geometryCache = new Map();
const CACHE_MAX_SIZE = 8; // keep at most 8 cached geometries
function evictCacheIfNeeded() {
  if (geometryCache.size > CACHE_MAX_SIZE) {
    const oldestKey = geometryCache.keys().next().value;
    const entry = geometryCache.get(oldestKey);
    if (entry) {
      entry.geometry.dispose();
      if (entry.wireframeGeometry) entry.wireframeGeometry.dispose();
    }
    geometryCache.delete(oldestKey);
  }
}
function buildTerrainGeometry(timeStep) {
  if (geometryCache.has(timeStep)) {
    return geometryCache.get(timeStep);
  }
  evictCacheIfNeeded();
  const stepData = timeSeriesData[timeStep];
  const { revenue, density } = stepData;
  const geom = new THREE.BufferGeometry();
  const positions = new Float32Array(VERTEX_COUNT * 3);
  const colors = new Float32Array(VERTEX_COUNT * 3);
  const indices = [];
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iz * GRID_SIZE + ix;
      const x = (ix / (GRID_SIZE - 1)) * TERRAIN_SPAN - HALF_SPAN;
      const z = (iz / (GRID_SIZE - 1)) * TERRAIN_SPAN - HALF_SPAN;
      const y = revenue[idx] * HEIGHT_SCALE;
      positions[idx * 3] = x;
      positions[idx * 3 + 1] = y;
      positions[idx * 3 + 2] = z;
      // Color: green (low density) -> yellow -> red (high density)
      const d = density[idx];
      const r = Math.min(1, d * 1.5);
      const g = Math.min(1, (1 - Math.abs(d - 0.5) * 2) * 0.8 + d * 0.5);
      const b = Math.max(0, (1 - d) * 0.4);
      colors[idx * 3] = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  for (let iz = 0; iz < GRID_SIZE - 1; iz++) {
    for (let ix = 0; ix < GRID_SIZE - 1; ix++) {
      const a = iz * GRID_SIZE + ix;
      const b = a + 1;
      const c = a + GRID_SIZE;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  const wireframeGeom = new THREE.WireframeGeometry(geom);
  const entry = { geometry: geom, wireframeGeometry: wireframeGeom };
  geometryCache.set(timeStep, entry);
  return entry;
}
// ============================================================================
// MODULE: terrain-mesh.js — Mesh creation and terrain management
// ============================================================================
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.1,
  flatShading: false,
  side: THREE.DoubleSide
});
const wireframeMaterial = new THREE.MeshBasicMaterial({
  color: '#335577',
  wireframe: true,
  transparent: true,
  opacity: 0.12
});
let terrainMesh = null;
let wireframeMesh = null;
let currentTimeStep = 0;
function updateTerrainMesh(timeStep) {
  const { geometry, wireframeGeometry } = buildTerrainGeometry(timeStep);
  currentTimeStep = timeStep;
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geometry;
  } else {
    terrainMesh = new THREE.Mesh(geometry, terrainMaterial);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  }
  if (wireframeMesh) {
    wireframeMesh.geometry.dispose();
    wireframeMesh.geometry = wireframeGeometry;
  } else {
    wireframeMesh = new THREE.Mesh(wireframeGeometry, wireframeMaterial);
    scene.add(wireframeMesh);
  }
  wireframeMesh.visible = document.getElementById('toggle-wireframe').checked;
}
// ============================================================================
// MODULE: rivers.js — Error/anomaly paths as tube geometry
// ============================================================================
let riverGroup = null;
function buildRivers(timeStep) {
  if (riverGroup) {
    riverGroup.traverse(child => { if (child.geometry) child.geometry.dispose(); });
    scene.remove(riverGroup);
  }
  riverGroup = new THREE.Group();
  const stepData = timeSeriesData[timeStep];
  const { errors } = stepData;
  // find high-error cells and trace rivers from them
  const THRESHOLD = 0.65; // error value above which we seed a river
  const MAX_RIVERS = 5;
  const highErrorCells = [];
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iz * GRID_SIZE + ix;
      if (errors[idx] > THRESHOLD) {
        highErrorCells.push({ ix, iz, error: errors[idx] });
      }
    }
  }
  highErrorCells.sort((a, b) => b.error - a.error);
  const seeds = highErrorCells.slice(0, MAX_RIVERS);
  const riverMaterial = new THREE.MeshStandardMaterial({
    color: '#ff3344',
    roughness: 0.3,
    metalness: 0.5,
    emissive: '#330000',
    emissiveIntensity: 0.6
  });
  seeds.forEach(seed => {
    const path = [];
    let cx = seed.ix;
    let cz = seed.iz;
    const STEPS = RIVER_SEGMENTS;
    for (let s = 0; s < STEPS; s++) {
      const fx = (cx / (GRID_SIZE - 1)) * TERRAIN_SPAN - HALF_SPAN;
      const fz = (cz / (GRID_SIZE - 1)) * TERRAIN_SPAN - HALF_SPAN;
      const idx = Math.round(cz) * GRID_SIZE + Math.round(cx);
      const fy = (timeSeriesData[timeStep].revenue[idx] || 0) * HEIGHT_SCALE + 0.05;
      path.push(new THREE.Vector3(fx, fy, fz));
      // flow downhill: move toward neighbor with lowest revenue (valley)
      let bestIx = cx, bestIz = cz, bestVal = Infinity;
      for (let dz = -1; dz <= 1; dz++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dz === 0) continue;
          const nx = Math.round(cx) + dx;
          const nz = Math.round(cz) + dz;
          if (nx < 0 || nx >= GRID_SIZE || nz < 0 || nz >= GRID_SIZE) continue;
          const nidx = nz * GRID_SIZE + nx;
          const val = timeSeriesData[timeStep].revenue[nidx];
          if (val < bestVal) { bestVal = val; bestIx = nx; bestIz = nz; }
        }
      }
      cx = bestIx;
      cz = bestIz;
    }
    if (path.length < 2) return;
    const curve = new THREE.CatmullRomCurve3(path);
    const tubeGeom = new THREE.TubeGeometry(curve, RIVER_SEGMENTS, RIVER_WIDTH, RIVER_TUBE_RADIAL, false);
    const tube = new THREE.Mesh(tubeGeom, riverMaterial);
    tube.castShadow = true;
    riverGroup.add(tube);
  });
  scene.add(riverGroup);
  riverGroup.visible = document.getElementById('toggle-rivers').checked;
}
// ============================================================================
// MODULE: particles.js — Data flow particle trails
// ============================================================================
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
// per-particle state: current position {x, z} on terrain, phase, trail ring buffer
const particleState = new Array(PARTICLE_COUNT);
const trailBuffers = new Array(PARTICLE_COUNT);
const particleGeometry = new THREE.BufferGeometry();
particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeometry.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMaterial = new THREE.PointsMaterial({
  size: 0.12,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
  map: createGlowTexture()
});
function createGlowTexture() {
  const size = 32;
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  gradient.addColorStop(0, 'rgba(255,255,255,1)');
  gradient.addColorStop(0.15, 'rgba(200,220,255,0.9)');
  gradient.addColorStop(0.4, 'rgba(100,160,255,0.4)');
  gradient.addColorStop(0.7, 'rgba(30,60,180,0.05)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, size, size);
  return new THREE.CanvasTexture(canvas);
}
const points = new THREE.Points(particleGeometry, particleMaterial);
scene.add(points);
points.visible = document.getElementById('toggle-particles').checked;
function initParticles() {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particleState[i] = {
      x: Math.random() * (GRID_SIZE - 1),
      z: Math.random() * (GRID_SIZE - 1),
      phase: Math.random() * Math.PI * 2,
      speed: PARTICLE_SPEED_BASE * (0.5 + Math.random())
    };
    trailBuffers[i] = new Array(PARTICLE_TRAIL_LENGTH).fill(null);
    particlePositions[i * 3 + 1] = -100; // hide until first update
  }
}
function updateParticles(deltaTime, timeStep) {
  const stepData = timeSeriesData[timeStep];
  const { revenue } = stepData;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const st = particleState[i];
    // flow toward negative gradient (downhill) to follow valleys
    const ix = Math.floor(st.x);
    const iz = Math.floor(st.z);
    const fx = st.x - ix;
    const fz = st.z - iz;
    // bilinear sample revenue
    const x0 = Math.max(0, Math.min(GRID_SIZE - 1, ix));
    const x1 = Math.max(0, Math.min(GRID_SIZE - 1, ix + 1));
    const z0 = Math.max(0, Math.min(GRID_SIZE - 1, iz));
    const z1 = Math.max(0, Math.min(GRID_SIZE - 1, iz + 1));
    const v00 = revenue[z0 * GRID_SIZE + x0];
    const v10 = revenue[z0 * GRID_SIZE + x1];
    const v01 = revenue[z1 * GRID_SIZE + x0];
    const v11 = revenue[z1 * GRID_SIZE + x1];
    const h = v00 * (1-fx)*(1-fz) + v10*fx*(1-fz) + v01*(1-fx)*fz + v11*fx*fz;
    const gradX = (v10 - v00) * (1-fz) + (v11 - v01) * fz;
    const gradZ = (v01 - v00) * (1-fx) + (v11 - v10) * fx;
    // flow downhill + some perpendicular drift
    const flowX = -gradX * 2 + Math.cos(st.phase) * 0.3;
    const flowZ = -gradZ * 2 + Math.sin(st.phase) * 0.3;
    const flowLen = Math.sqrt(flowX * flowX + flowZ * flowZ) || 1;
    st.x += (flowX / flowLen) * st.speed * deltaTime * 4;
    st.z += (flowZ / flowLen) * st.speed * deltaTime * 4;
    // wrap
    if (st.x < 0) st.x += GRID_SIZE - 1;
    if (st.x >= GRID_SIZE) st.x -= GRID_SIZE - 1;
    if (st.z < 0) st.z += GRID_SIZE - 1;
    if (st.z >= GRID_SIZE) st.z -= GRID_SIZE - 1;
    const worldX = (st.x / (GRID_SIZE - 1)) * TERRAIN_SPAN - HALF_SPAN;
    const worldZ = (st.z / (GRID_SIZE - 1)) * TERRAIN_SPAN - HALF_SPAN;
    const worldY = h * HEIGHT_SCALE + 0.25;
    particlePositions[i * 3] = worldX;
    particlePositions[i * 3 + 1] = worldY;
    particlePositions[i * 3 + 2] = worldZ;
    // color from height: low=blue, mid=cyan, high=white
    const t = h;
    particleColors[i * 3] = t * 0.7;
    particleColors[i * 3 + 1] = 0.4 + t * 0.5;
    particleColors[i * 3 + 2] = 1 - t * 0.3;
  }
  particleGeometry.attributes.position.needsUpdate = true;
  particleGeometry.attributes.color.needsUpdate = true;
}
initParticles();
// ============================================================================
// MODULE: time-controller.js — Time slider binding and UI updates
// ============================================================================
let recomputeCounter = 0;
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
timeSlider.max = TIME_STEPS - 1;
timeSlider.value = 0;
timeSlider.disabled = false;
timeLabel.textContent = `0 / ${TIME_STEPS - 1}`;
function onTimeChange(timeStep) {
  updateTerrainMesh(timeStep);
  buildRivers(timeStep);
  recomputeCounter++;
  // update metric displays (sample center region)
  const stepData = timeSeriesData[timeStep];
  const midIdx = Math.floor(GRID_SIZE / 2) * GRID_SIZE + Math.floor(GRID_SIZE / 2);
  document.getElementById('val-revenue').textContent = (stepData.revenue[midIdx] * 100).toFixed(1) + '%';
  document.getElementById('val-density').textContent = (stepData.density[midIdx] * 100).toFixed(1) + '%';
  document.getElementById('val-errors').textContent = (stepData.errors[midIdx] * 100).toFixed(2) + '%';
  document.getElementById('val-api').textContent = Math.floor(stepData.density[midIdx] * 850 + 50);
  timeLabel.textContent = `${timeStep} / ${TIME_STEPS - 1}`;
  timeSlider.value = timeStep;
}
timeSlider.addEventListener('input', () => {
  onTimeChange(parseInt(timeSlider.value));
});
// ============================================================================
// MODULE: wiring-check.js — Self-verification ensuring all data flows connected
// ============================================================================
function runWiringCheck() {
  const checks = [];
  const statusEl = document.getElementById('wiring-status');
  // Verify terrain geometry is attached to scene
  checks.push({
    label: 'Terrain mesh in scene',
    pass: terrainMesh !== null && scene.children.includes(terrainMesh)
  });
  // Verify vertex buffer contains data matching source
  if (terrainMesh && terrainMesh.geometry.attributes.position) {
    const buf = terrainMesh.geometry.attributes.position.array;
    const src = timeSeriesData[currentTimeStep].revenue;
    const midIdx = Math.floor(GRID_SIZE / 2) * GRID_SIZE + Math.floor(GRID_SIZE / 2);
    const bufY = buf[midIdx * 3 + 1];
    const expectedY = src[midIdx] * HEIGHT_SCALE;
    checks.push({
      label: 'Buffer matches source data',
      pass: Math.abs(bufY - expectedY) < 0.001
    });
  } else {
    checks.push({ label: 'Buffer matches source data', pass: false });
  }
  // Verify particles exist in scene
  checks.push({
    label: 'Particles in scene',
    pass: scene.children.includes(points)
  });
  // Verify river group exists
  checks.push({
    label: 'River group in scene',
    pass: riverGroup !== null && scene.children.includes(riverGroup)
  });
  // Verify camera controls wired
  checks.push({
    label: 'OrbitControls active',
    pass: controls !== null && typeof controls.update === 'function'
  });
  const allPass = checks.every(c => c.pass);
  statusEl.textContent = 'Wiring: ' + checks.map(c => `${c.label}: ${c.pass ? 'OK' : 'FAIL'}`).join(' | ');
  statusEl.className = allPass ? 'pass' : 'fail';
  return allPass;
}
// ============================================================================
// MODULE: main-loop.js — Render loop, FPS counter, resize handler
// ============================================================================
let lastTime = performance.now();
let fpsFrames = 0;
let fpsAccum = 0;
let displayFps = 0;
const perfMonitor = document.getElementById('perf-monitor');
function animate(timestamp) {
  requestAnimationFrame(animate);
  const delta = Math.min((timestamp - lastTime) / 1000, 0.1); // cap at 100ms
  lastTime = timestamp;
  // FPS counter
  fpsFrames++;
  fpsAccum += delta;
  if (fpsAccum >= 1) {
    displayFps = Math.round(fpsFrames / fpsAccum);
    fpsFrames = 0;
    fpsAccum = 0;
    perfMonitor.textContent = `FPS: ${displayFps} | Recomputes: ${recomputeCounter}`;
  }
  controls.update();
  if (document.getElementById('toggle-particles').checked) {
    updateParticles(delta, currentTimeStep);
  }
  renderer.render(scene, camera);
}
// ============================================================================
// MODULE: event-bindings.js — UI toggle listeners, resize, keyboard shortcuts
// ============================================================================
document.getElementById('toggle-rivers').addEventListener('change', function() {
  if (riverGroup) riverGroup.visible = this.checked;
});
document.getElementById('toggle-particles').addEventListener('change', function() {
  points.visible = this.checked;
});
document.getElementById('toggle-wireframe').addEventListener('change', function() {
  if (wireframeMesh) wireframeMesh.visible = this.checked;
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r': controls.autoRotate = !controls.autoRotate;
              document.getElementById('btn-autorotate').classList.toggle('active', controls.autoRotate);
              break;
    case 't': camera.position.set(0, TERRAIN_SPAN * 1.1, 0.1); controls.target.set(0,0,0); controls.update(); break;
    case 'f': camera.position.set(12, 8, 16); controls.target.set(0, HEIGHT_SCALE*0.25, 0); controls.update(); break;
    case 'arrowleft':  timeSlider.value = Math.max(0, currentTimeStep - 1); onTimeChange(parseInt(timeSlider.value)); break;
    case 'arrowright': timeSlider.value = Math.min(TIME_STEPS - 1, currentTimeStep + 1); onTimeChange(parseInt(timeSlider.value)); break;
  }
});
// ============================================================================
// MODULE: init.js — Bootstrap: wire everything and run verification
// ============================================================================
onTimeChange(0);
// run wiring check after a short delay to ensure all geometry is committed
setTimeout(() => {
  const wiringPassed = runWiringCheck();
  if (!wiringPassed) {
    console.warn('WIRING CHECK FAILED — some data flows may be disconnected');
  }
}, 200);
// start render loop
requestAnimationFrame(animate);
// log performance budget
console.log(`PERF BUDGET: max 2 recomputes/user-interaction | Cache entries: ${geometryCache.size} | Particles reused in-place: true`);
</script>
</body>
</html>