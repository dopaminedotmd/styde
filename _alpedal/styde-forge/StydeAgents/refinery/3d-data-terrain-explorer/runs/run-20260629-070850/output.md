<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a14; --panel: #111122cc; --text: #c8d0e0; --accent: #4af; --warn: #f64; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  canvas { display:block; }
  #panel { position:fixed; top:16px; right:16px; width:260px; background:var(--panel);
    border:1px solid #ffffff22; border-radius:10px; padding:16px; backdrop-filter:blur(12px);
    z-index:10; display:flex; flex-direction:column; gap:10px; }
  #panel h1 { font-size:15px; font-weight:600; color:var(--accent); letter-spacing:0.5px; }
  .metric { display:flex; justify-content:space-between; font-size:12px; opacity:0.85; }
  .metric span:last-child { font-weight:600; }
  input[type=range] { width:100%; accent-color:var(--accent); }
  .btn-row { display:flex; gap:6px; flex-wrap:wrap; }
  button { flex:1; padding:6px 8px; border:1px solid #ffffff33; border-radius:6px;
    background:#ffffff0a; color:var(--text); cursor:pointer; font-size:11px; transition:0.2s; min-width:60px; }
  button:hover { background:#ffffff1a; border-color:var(--accent); }
  button.active { background:var(--accent); color:#000; border-color:var(--accent); }
  #time-label { font-size:11px; text-align:center; opacity:0.7; }
  #bookmark-list { max-height:100px; overflow-y:auto; font-size:10px; display:flex; flex-direction:column; gap:3px; }
  .bm { padding:3px 6px; background:#ffffff08; border-radius:4px; cursor:pointer; }
  .bm:hover { background:#ffffff18; }
  .divider { height:1px; background:#ffffff15; margin:2px 0; }
</style>
</head>
<body>
<div id="panel">
  <h1>3D Data Terrain</h1>
  <div class="metric"><span>Revenue (elev)</span><span id="val-rev">--</span></div>
  <div class="metric"><span>Users (color)</span><span id="val-usr">--</span></div>
  <div class="metric"><span>Errors (rivers)</span><span id="val-err">--</span></div>
  <div class="metric"><span>API Calls</span><span id="val-api">--</span></div>
  <div class="divider"></div>
  <label id="time-label">Time: T0</label>
  <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
  <div class="btn-row">
    <button id="btn-auto" class="active">Auto</button>
    <button id="btn-top">Top</button>
    <button id="btn-front">Front</button>
    <button id="btn-save-bm">Save</button>
  </div>
  <div class="divider"></div>
  <div id="bookmark-list"></div>
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
// ═══════════════════════════════════════════
// IMPORTS
// ═══════════════════════════════════════════
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ═══════════════════════════════════════════
// GUARD: THREE availability
// ═══════════════════════════════════════════
if (!THREE || !THREE.WebGLRenderer) {
  document.body.textContent = 'WebGL not available.';
  throw new Error('THREE.js failed to load');
}
// ═══════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════
const GRID = 100;
const SIZE = 40;
const TIME_SLOTS = 24;
const PARTICLE_COUNT = 800;
// ═══════════════════════════════════════════
// DATA GENERATION — synthetic 24h time-series
// ═══════════════════════════════════════════
function generateTimeSeries() {
  const data = [];
  for (let t = 0; t < TIME_SLOTS; t++) {
    const hour = t;
    const revenue = [];     // elevation
    const users = [];       // vertex color
    const errors = [];      // river paths
    for (let i = 0; i < GRID; i++) {
      revenue[i] = [];
      users[i] = [];
      errors[i] = [];
      for (let j = 0; j < GRID; j++) {
        const nx = i / GRID - 0.5;
        const ny = j / GRID - 0.5;
        const dist = Math.sqrt(nx * nx + ny * ny);
        const wave = Math.sin(dist * 8 + hour * 0.5) * 0.5 + 0.5;
        const hill = Math.exp(-dist * 4) * 3;
        const drift = Math.cos(nx * 3 + hour * 0.3) * Math.sin(ny * 3 - hour * 0.2);
        revenue[i][j] = hill + wave * 2.5 + drift * 0.8 + (Math.random() - 0.5) * 0.3;
        users[i][j] = Math.max(0, revenue[i][j] * 0.4 + Math.sin(nx * 6) * Math.cos(ny * 6 + hour * 0.4) * 0.3 + 0.3);
        errors[i][j] = revenue[i][j] < 0.3 ? 0.7 + Math.random() * 0.3 : (Math.random() < 0.04 ? Math.random() : 0);
      }
    }
    data.push({ revenue, users, errors });
  }
  return data;
}
// ═══════════════════════════════════════════
// THREE.JS SETUP
// ═══════════════════════════════════════════
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a14');
scene.fog = new THREE.Fog('#0a0a14', 25, 80);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(22, 16, 28);
camera.lookAt(0, 2, 0);
// ═══════════════════════════════════════════
// LIGHTS
// ═══════════════════════════════════════════
const ambient = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffeedd', 3.5);
sun.position.set(30, 25, 20);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 100;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
scene.add(sun);
const fill = new THREE.DirectionalLight('#4466aa', 0.8);
fill.position.set(-15, 5, -10);
scene.add(fill);
// ═══════════════════════════════════════════
// ORBIT CONTROLS
// ═══════════════════════════════════════════
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.6;
controls.target.set(0, 2, 0);
controls.maxPolarAngle = Math.PI * 0.55;
controls.minDistance = 8;
controls.maxDistance = 65;
controls.update();
// ═══════════════════════════════════════════
// TERRAIN GEOMETRY BUILDER — BufferGeometry
// ═══════════════════════════════════════════
function buildHeightData(slot) {
  const { revenue } = slot;
  const arr = new Float32Array(GRID * GRID);
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      arr[i * GRID + j] = revenue[i][j];
    }
  }
  return arr;
}
function buildColorData(usersGrid) {
  const arr = new Float32Array(GRID * GRID * 3);
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const v = usersGrid[i][j];
      const idx = (i * GRID + j) * 3;
      arr[idx] = 0.1 + v * 0.9;
      arr[idx + 1] = 0.8 - v * 0.65;
      arr[idx + 2] = 0.15 + v * 0.2;
    }
  }
  return arr;
}
function buildTerrainGeometry(heightData, colorData) {
  const geo = new THREE.BufferGeometry();
  const verts = new Float32Array(GRID * GRID * 3);
  const indices = [];
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const x = (i / (GRID - 1) - 0.5) * SIZE;
      const z = (j / (GRID - 1) - 0.5) * SIZE;
      const y = heightData[i * GRID + j];
      const vi = (i * GRID + j) * 3;
      verts[vi] = x;
      verts[vi + 1] = y;
      verts[vi + 2] = z;
      if (i < GRID - 1 && j < GRID - 1) {
        const a = i * GRID + j;
        const b = a + 1;
        const c = a + GRID;
        const d = c + 1;
        indices.push(a, b, d, a, d, c);
      }
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
  geo.setIndex(indices);
  geo.setAttribute('color', new THREE.BufferAttribute(colorData, 3));
  geo.computeVertexNormals();
  return geo;
}
// ═══════════════════════════════════════════
// GEOMETRY CACHE — pre-built variants
// ═══════════════════════════════════════════
const timeSeries = generateTimeSeries();
const geometryCache = new Map();
function getCachedGeometry(t) {
  if (geometryCache.has(t)) return geometryCache.get(t);
  const h = buildHeightData(timeSeries[t]);
  const c = buildColorData(timeSeries[t].users);
  const geo = buildTerrainGeometry(h, c);
  geometryCache.set(t, geo);
  return geo;
}
// ═══════════════════════════════════════════
// TERRAIN MESH — swap geometry on slider
// ═══════════════════════════════════════════
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.55, metalness: 0.05, flatShading: false
});
const terrainMesh = new THREE.Mesh(getCachedGeometry(0), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ═══════════════════════════════════════════
// RIVER GEOMETRY — error paths
// ═══════════════════════════════════════════
let riverGroup = new THREE.Group();
scene.add(riverGroup);
function buildRivers(slot) {
  riverGroup.clear();
  const { errors, revenue } = slot;
  const riverMat = new THREE.MeshStandardMaterial({
    color: '#ff3344', emissive: '#330000', roughness: 0.3, metalness: 0.1
  });
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      if (errors[i][j] <= 0.2) continue;
      const x = (i / (GRID - 1) - 0.5) * SIZE;
      const z = (j / (GRID - 1) - 0.5) * SIZE;
      const y = revenue[i][j] + 0.08;
      const seg = new THREE.CylinderGeometry(0.12, 0.12, 0.3, 6);
      const mesh = new THREE.Mesh(seg, riverMat);
      mesh.position.set(x, y, z);
      riverGroup.add(mesh);
    }
  }
}
// ═══════════════════════════════════════════
// PARTICLE SYSTEM — reuse position buffer
// ═══════════════════════════════════════════
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particlePhases = new Float32Array(PARTICLE_COUNT);
const particleSpeeds = new Float32Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particlePhases[i] = Math.random() * Math.PI * 2;
  particleSpeeds[i] = 0.3 + Math.random() * 1.2;
  const sx = (Math.random() - 0.5) * SIZE * 0.9;
  const sz = (Math.random() - 0.5) * SIZE * 0.9;
  particlePositions[i * 3] = sx;
  particlePositions[i * 3 + 1] = 0.5;
  particlePositions[i * 3 + 2] = sz;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const ci = i * 3;
  particleColors[ci] = 0.6 + Math.random() * 0.4;
  particleColors[ci + 1] = 0.7 + Math.random() * 0.3;
  particleColors[ci + 2] = 0.9 + Math.random() * 0.1;
}
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.15, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.7
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
// ═══════════════════════════════════════════
// PARTICLE UPDATE — in-place buffer mutation
// ═══════════════════════════════════════════
function sampleHeight(slotData, wx, wz) {
  const i = Math.round(((wx / SIZE) + 0.5) * (GRID - 1));
  const j = Math.round(((wz / SIZE) + 0.5) * (GRID - 1));
  const ci = Math.max(0, Math.min(GRID - 1, i));
  const cj = Math.max(0, Math.min(GRID - 1, j));
  return slotData.revenue[ci][cj];
}
function updateParticles(slotData, time) {
  for (let p = 0; p < PARTICLE_COUNT; p++) {
    const phi = particlePhases[p] + time * particleSpeeds[p] * 0.4;
    const radius = 12 + Math.sin(phi * 0.7) * 8;
    const wx = Math.cos(phi) * radius;
    const wz = Math.sin(phi * 0.8) * radius;
    const h = sampleHeight(slotData, wx, wz);
    const pi = p * 3;
    particlePositions[pi] = wx;
    particlePositions[pi + 1] = h + 0.4;
    particlePositions[pi + 2] = wz;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ═══════════════════════════════════════════
// GRID HELPER
// ═══════════════════════════════════════════
const grid = new THREE.GridHelper(44, 30, '#ffffff15', '#ffffff08');
grid.position.y = -0.02;
scene.add(grid);
// ═══════════════════════════════════════════
// CAMERA BOOKMARKS
// ═══════════════════════════════════════════
const bookmarks = [];
function saveBookmark() {
  bookmarks.push({
    pos: camera.position.clone(),
    target: controls.target.clone(),
    label: 'B' + (bookmarks.length + 1)
  });
  renderBookmarks();
}
function renderBookmarks() {
  const list = document.getElementById('bookmark-list');
  list.innerHTML = '';
  for (let i = 0; i < bookmarks.length; i++) {
    const bm = bookmarks[i];
    const div = document.createElement('div');
    div.className = 'bm';
    div.textContent = bm.label + ' pos(' + bm.pos.x.toFixed(1) + ',' + bm.pos.y.toFixed(1) + ',' + bm.pos.z.toFixed(1) + ')';
    div.onclick = () => {
      camera.position.copy(bm.pos);
      controls.target.copy(bm.target);
      controls.update();
    };
    list.appendChild(div);
  }
}
// ═══════════════════════════════════════════
// UI STATE
// ═══════════════════════════════════════════
let currentTimeSlot = 0;
let autoRotate = true;
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const btnAuto = document.getElementById('btn-auto');
const btnTop = document.getElementById('btn-top');
const btnFront = document.getElementById('btn-front');
const btnSaveBm = document.getElementById('btn-save-bm');
const valRev = document.getElementById('val-rev');
const valUsr = document.getElementById('val-usr');
const valErr = document.getElementById('val-err');
const valApi = document.getElementById('val-api');
// ═══════════════════════════════════════════
// TIME SLIDER HANDLER
// ═══════════════════════════════════════════
function setTimeSlot(t) {
  if (t === currentTimeSlot) return;
  currentTimeSlot = t;
  slider.value = t;
  timeLabel.textContent = 'Time: T' + t;
  terrainMesh.geometry = getCachedGeometry(t);
  buildRivers(timeSeries[t]);
  updatePanelStats(t);
}
slider.addEventListener('input', () => {
  setTimeSlot(parseInt(slider.value));
});
// ═══════════════════════════════════════════
// PANEL STATS
// ═══════════════════════════════════════════
function updatePanelStats(t) {
  const slot = timeSeries[t];
  let sumRev = 0, sumUsr = 0, sumErr = 0;
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      sumRev += slot.revenue[i][j];
      sumUsr += slot.users[i][j];
      sumErr += slot.errors[i][j];
    }
  }
  const n = GRID * GRID;
  valRev.textContent = (sumRev / n).toFixed(2);
  valUsr.textContent = (sumUsr / n * 100).toFixed(0) + '%';
  valErr.textContent = (sumErr / n * 100).toFixed(1) + '%';
  valApi.textContent = Math.floor(PARTICLE_COUNT * (0.6 + Math.sin(t * 0.7) * 0.3));
}
// ═══════════════════════════════════════════
// BUTTON HANDLERS
// ═══════════════════════════════════════════
btnAuto.addEventListener('click', () => {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  btnAuto.classList.toggle('active', autoRotate);
});
btnTop.addEventListener('click', () => {
  camera.position.set(0, 35, 0.5);
  controls.target.set(0, 2, 0);
  controls.update();
});
btnFront.addEventListener('click', () => {
  camera.position.set(0, 6, 35);
  controls.target.set(0, 2, 0);
  controls.update();
});
btnSaveBm.addEventListener('click', saveBookmark);
// ═══════════════════════════════════════════
// RESIZE HANDLER
// ═══════════════════════════════════════════
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ═══════════════════════════════════════════
// ANIMATION LOOP
// ═══════════════════════════════════════════
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const elapsed = clock.getElapsedTime();
  controls.update();
  updateParticles(timeSeries[currentTimeSlot], elapsed);
  renderer.render(scene, camera);
}
// ═══════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════
buildRivers(timeSeries[0]);
updatePanelStats(0);
renderBookmarks();
animate();
</script>
</body>
</html>