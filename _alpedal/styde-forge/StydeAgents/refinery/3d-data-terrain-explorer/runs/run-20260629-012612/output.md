<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;background:#0a0a14;color:#d0d0e0}
#app{width:100%;height:100%;position:relative}
#terrain-container{width:100%;height:100%;display:none}
#terrain-container.active{display:block}
.state-overlay{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;flex-direction:column;z-index:10;background:rgba(10,10,20,0.95)}
.state-overlay.hidden{display:none}
.spinner{width:48px;height:48px;border:3px solid rgba(100,200,255,0.2);border-top-color:#64c8ff;border-radius:50%;animation:spin 0.8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.state-title{font-size:1.4rem;margin-top:16px;color:#8899bb}
.state-subtitle{font-size:0.85rem;color:#556677;margin-top:6px}
.retry-btn{margin-top:16px;padding:8px 24px;background:#1a3355;border:1px solid #335577;color:#88bbdd;border-radius:4px;cursor:pointer;font-size:0.9rem}
.retry-btn:hover{background:#224466}
#hud{position:absolute;top:12px;left:12px;z-index:5;pointer-events:none}
.hud-panel{background:rgba(8,8,20,0.85);border:1px solid rgba(80,120,180,0.3);border-radius:6px;padding:10px 14px;font-size:0.78rem;line-height:1.5;pointer-events:auto;backdrop-filter:blur(6px)}
.hud-panel .label{color:#667a99}
.hud-panel .value{color:#aaccee;font-weight:600}
#timeline{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);z-index:5;display:flex;align-items:center;gap:10px;background:rgba(8,8,20,0.85);border:1px solid rgba(80,120,180,0.3);border-radius:8px;padding:8px 16px;backdrop-filter:blur(6px)}
#time-slider{width:260px;accent-color:#4488cc;cursor:pointer}
#time-label{font-size:0.78rem;color:#aaccee;min-width:70px;text-align:center}
#bookmarks{position:absolute;top:12px;right:12px;z-index:5;display:flex;flex-direction:column;gap:4px}
.bm-btn{background:rgba(8,8,20,0.8);border:1px solid rgba(80,120,180,0.25);color:#88aacc;padding:6px 10px;border-radius:4px;cursor:pointer;font-size:0.7rem;text-align:left;transition:all 0.15s}
.bm-btn:hover{background:rgba(20,40,70,0.8);border-color:rgba(100,160,220,0.5)}
.bm-btn.saved{color:#44cc88;border-color:rgba(68,204,136,0.4)}
#legend{position:absolute;bottom:100px;right:16px;z-index:5;background:rgba(8,8,20,0.85);border:1px solid rgba(80,120,180,0.3);border-radius:6px;padding:10px 12px;font-size:0.7rem;backdrop-filter:blur(6px)}
.legend-row{display:flex;align-items:center;gap:8px;margin:3px 0}
.legend-swatch{width:14px;height:14px;border-radius:3px}
@media(max-width:768px){
  #timeline{bottom:10px;padding:6px 10px;gap:6px}
  #time-slider{width:160px}
  #hud{top:6px;left:6px}
  .hud-panel{font-size:0.7rem;padding:6px 10px}
  #bookmarks{top:6px;right:6px;gap:2px}
  .bm-btn{padding:4px 7px;font-size:0.65rem}
  #legend{bottom:80px;right:6px;font-size:0.65rem}
}
</style>
</head>
<body>
<div id="app">
  <div id="loading-state" class="state-overlay"><div class="spinner"></div><div class="state-title">Loading terrain data...</div><div class="state-subtitle">Fetching time-series metrics</div></div>
  <div id="empty-state" class="state-overlay hidden"><div class="state-title">No data available</div><div class="state-subtitle">The dataset is empty. Upload or generate data to begin.</div><button class="retry-btn" onclick="generateDemoData()">Generate Demo Data</button></div>
  <div id="error-state" class="state-overlay hidden"><div class="state-title">Failed to load data</div><div class="state-subtitle" id="error-msg">Network error or invalid format.</div><button class="retry-btn" onclick="retryLoad()">Retry</button></div>
  <div id="terrain-container"><canvas id="terrain-canvas"></canvas></div>
  <div id="hud"><div class="hud-panel"><span class="label">Revenue </span><span class="value" id="hud-revenue">—</span><br><span class="label">Users </span><span class="value" id="hud-users">—</span><br><span class="label">Error rate </span><span class="value" id="hud-errors">—</span><br><span class="label">FPS </span><span class="value" id="hud-fps">—</span></div></div>
  <div id="timeline"><span style="font-size:0.7rem;color:#667a99">Time</span><input type="range" id="time-slider" min="0" max="0" value="0"><span id="time-label">—</span></div>
  <div id="bookmarks"><button class="bm-btn" onclick="saveBookmark(1)">Save View 1</button><button class="bm-btn" onclick="saveBookmark(2)">Save View 2</button><button class="bm-btn" onclick="saveBookmark(3)">Save View 3</button><button class="bm-btn" onclick="loadBookmark(1)">Load View 1</button><button class="bm-btn" onclick="loadBookmark(2)">Load View 2</button><button class="bm-btn" onclick="loadBookmark(3)">Load View 3</button></div>
  <div id="legend"><div class="legend-row"><span class="legend-swatch" style="background:#22aa44"></span> High user density</div><div class="legend-row"><span class="legend-swatch" style="background:#aaaa22"></span> Medium density</div><div class="legend-row"><span class="legend-swatch" style="background:#aa4422"></span> Low density</div><div class="legend-row"><span class="legend-swatch" style="background:#cc2222"></span> Error river</div><div class="legend-row"><span class="legend-swatch" style="background:#4488ff"></span> API particle</div></div>
</div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
/*
DATA CONTRACT — timeSeriesData
Array of time-slice objects:
{
  timestamp: number,    // Unix ms or index
  revenue: number,      // Primary metric → terrain height
  users: number,        // Secondary metric → vertex color
  errors: number,       // Error count → river trigger
  apiCalls: number      // Activity → particle density
}
Cross-cutting concerns:
  Loading state: spinner overlay while fetch/build in progress
  Empty state: shown when array length === 0
  Error state: shown on fetch/parse failure, with retry button
  Success state: terrain container visible with 3D scene active
Responsive breakpoints: mobile <768px, tablet 768-1024px, desktop >1024px
Frame throttling: terrain rebuild capped at 30fps (33ms min interval), camera render at 60fps
*/
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const dom = {
  loading: document.getElementById('loading-state'),
  empty: document.getElementById('empty-state'),
  error: document.getElementById('error-state'),
  errorMsg: document.getElementById('error-msg'),
  terrain: document.getElementById('terrain-container'),
  canvas: document.getElementById('terrain-canvas'),
  slider: document.getElementById('time-slider'),
  timeLabel: document.getElementById('time-label'),
  hudRevenue: document.getElementById('hud-revenue'),
  hudUsers: document.getElementById('hud-users'),
  hudErrors: document.getElementById('hud-errors'),
  hudFps: document.getElementById('hud-fps'),
};
let scene, camera, renderer, controls, clock;
let terrainMesh, riverGroup, particleSystem;
let timeSeriesData = null;
let currentTimeIndex = 0;
let geometryCache = new Map();
let bookmarks = [null, null, null];
let lastTerrainBuild = 0;
const TERRAIN_BUILD_INTERVAL = 33;
let fpsFrames = 0, fpsLastTime = performance.now();
function showState(state) {
  dom.loading.classList.toggle('hidden', state !== 'loading');
  dom.empty.classList.toggle('hidden', state !== 'empty');
  dom.error.classList.toggle('hidden', state !== 'error');
  dom.terrain.classList.toggle('active', state === 'success');
}
function generateDemoData() {
  const points = 120;
  const data = [];
  const baseRevenue = 5000 + Math.random() * 3000;
  const baseUsers = 800 + Math.random() * 400;
  for (let i = 0; i < points; i++) {
    const t = i / points;
    const seasonal = Math.sin(t * Math.PI * 4) * 1500;
    const trend = t * 2000;
    const noise = (Math.random() - 0.5) * 800;
    const revenue = baseRevenue + trend + seasonal + noise;
    const users = baseUsers + trend * 0.3 + seasonal * 0.2 + (Math.random() - 0.5) * 150;
    const spikeChance = Math.random();
    const errors = spikeChance > 0.92 ? 20 + Math.random() * 40 : Math.random() * 5;
    const apiCalls = 200 + revenue * 0.08 + (Math.random() - 0.5) * 40;
    data.push({ timestamp: i, revenue: Math.max(100, revenue), users: Math.max(10, users), errors, apiCalls: Math.max(10, apiCalls) });
  }
  return data;
}
async function fetchData() {
  showState('loading');
  try {
    await new Promise(r => setTimeout(r, 400 + Math.random() * 300));
    const data = generateDemoData();
    if (!Array.isArray(data) || data.length === 0) {
      showState('empty');
      return null;
    }
    timeSeriesData = data;
    return data;
  } catch (e) {
    dom.errorMsg.textContent = e.message || 'Unknown error loading data';
    showState('error');
    return null;
  }
}
function retryLoad() { fetchData().then(d => d && initScene(d)); }
window.retryLoad = retryLoad;
window.generateDemoData = () => { timeSeriesData = generateDemoData(); initScene(timeSeriesData); };
function initRenderer() {
  renderer = new THREE.WebGLRenderer({ canvas: dom.canvas, antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
}
function initCamera() {
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 10, 20000);
  camera.position.set(4000, 3500, 5000);
  camera.lookAt(0, 0, -1000);
}
function initControls() {
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.3;
  controls.target.set(0, 0, -1000);
  controls.minDistance = 800;
  controls.maxDistance = 12000;
  controls.maxPolarAngle = Math.PI * 0.45;
  controls.update();
}
function initLighting() {
  const ambient = new THREE.AmbientLight(0x223344, 2.5);
  scene.add(ambient);
  const sun = new THREE.DirectionalLight(0xffeedd, 6);
  sun.position.set(5000, 8000, 3000);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.camera.left = -6000; sun.shadow.camera.right = 6000;
  sun.shadow.camera.top = 6000; sun.shadow.camera.bottom = -6000;
  sun.shadow.camera.near = 100; sun.shadow.camera.far = 20000;
  sun.shadow.bias = -0.0001;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x4466aa, 2);
  fill.position.set(-3000, 2000, -4000);
  scene.add(fill);
}
function hexToRgb(hex) {
  const v = parseInt(hex.slice(1), 16);
  return { r: ((v >> 16) & 255) / 255, g: ((v >> 8) & 255) / 255, b: (v & 255) / 255 };
}
function userDensityColor(normalizedUsers) {
  if (normalizedUsers > 0.75) return hexToRgb('#22aa44');
  if (normalizedUsers > 0.5) return hexToRgb('#55aa33');
  if (normalizedUsers > 0.25) return hexToRgb('#aaaa22');
  return hexToRgb('#aa4422');
}
function buildTerrainGeometry(data) {
  const cols = data.length;
  const rows = 40;
  const heightScale = 0.6;
  const xSpacing = 30;
  const zSpacing = 40;
  const totalWidth = (cols - 1) * xSpacing;
  const totalDepth = (rows - 1) * zSpacing;
  const startX = -totalWidth / 2;
  const startZ = -totalDepth / 2;
  const revenueMin = Math.min(...data.map(d => d.revenue));
  const revenueMax = Math.max(...data.map(d => d.revenue));
  const revenueRange = revenueMax - revenueMin || 1;
  const usersMin = Math.min(...data.map(d => d.users));
  const usersMax = Math.max(...data.map(d => d.users));
  const usersRange = usersMax - usersMin || 1;
  const vertices = new Float32Array(cols * rows * 3);
  const colors = new Float32Array(cols * rows * 3);
  const indices = [];
  for (let iz = 0; iz < rows; iz++) {
    for (let ix = 0; ix < cols; ix++) {
      const idx = (iz * cols + ix);
      const d = data[ix];
      const revenueNorm = (d.revenue - revenueMin) / revenueRange;
      const height = revenueNorm * heightScale * 3000 + 50;
      const x = startX + ix * xSpacing;
      const z = startZ + iz * zSpacing;
      const zVariation = (Math.sin(ix * 0.3 + iz * 0.4) * 0.03 + Math.cos(iz * 0.5) * 0.02) * height;
      vertices[idx * 3] = x;
      vertices[idx * 3 + 1] = height + zVariation;
      vertices[idx * 3 + 2] = z;
      const userNorm = (d.users - usersMin) / usersRange;
      const col = userDensityColor(userNorm);
      colors[idx * 3] = col.r;
      colors[idx * 3 + 1] = col.g;
      colors[idx * 3 + 2] = col.b;
    }
  }
  for (let iz = 0; iz < rows - 1; iz++) {
    for (let ix = 0; ix < cols - 1; ix++) {
      const a = iz * cols + ix;
      const b = a + 1;
      const c = a + cols;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  return geom;
}
function buildTerrainMesh(geometry) {
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.7,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide,
  });
  const mesh = new THREE.Mesh(geometry, mat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  return mesh;
}
function buildRiverGeometry(data) {
  const group = new THREE.Group();
  const threshold = 10;
  const cols = data.length;
  const xSpacing = 30;
  const totalWidth = (cols - 1) * xSpacing;
  const startX = -totalWidth / 2;
  const revenueMin = Math.min(...data.map(d => d.revenue));
  const revenueMax = Math.max(...data.map(d => d.revenue));
  const revenueRange = revenueMax - revenueMin || 1;
  const heightScale = 0.6;
  let riverPoints = [];
  for (let ix = 0; ix < cols; ix++) {
    const d = data[ix];
    if (d.errors > threshold) {
      const revenueNorm = (d.revenue - revenueMin) / revenueRange;
      const height = revenueNorm * heightScale * 3000 + 50;
      const x = startX + ix * xSpacing;
      riverPoints.push(new THREE.Vector3(x, height + 12, -200 + (d.errors - threshold) * 6));
    }
  }
  if (riverPoints.length < 2) return group;
  const curve = new THREE.CatmullRomCurve3(riverPoints);
  const tubeGeom = new THREE.TubeGeometry(curve, riverPoints.length * 4, 8, 6, false);
  const tubeMat = new THREE.MeshStandardMaterial({ color: 0xcc2222, emissive: 0x440000, roughness: 0.3, metalness: 0.4 });
  const tube = new THREE.Mesh(tubeGeom, tubeMat);
  tube.castShadow = true;
  group.add(tube);
  const glowGeom = new THREE.TubeGeometry(curve, riverPoints.length * 4, 18, 6, false);
  const glowMat = new THREE.MeshBasicMaterial({ color: 0xff2222, transparent: true, opacity: 0.12, depthWrite: false });
  group.add(new THREE.Mesh(glowGeom, glowMat));
  return group;
}
function buildParticleSystem(data) {
  const maxParticles = 2000;
  const positions = new Float32Array(maxParticles * 3);
  const velocities = new Float32Array(maxParticles * 3);
  const colors = new Float32Array(maxParticles * 3);
  const particleData = [];
  const cols = data.length;
  const xSpacing = 30;
  const totalWidth = (cols - 1) * xSpacing;
  const startX = -totalWidth / 2;
  const revenueMin = Math.min(...data.map(d => d.revenue));
  const revenueMax = Math.max(...data.map(d => d.revenue));
  const revenueRange = revenueMax - revenueMin || 1;
  const heightScale = 0.6;
  for (let i = 0; i < maxParticles; i++) {
    const colIdx = Math.floor(Math.random() * cols);
    const d = data[colIdx];
    const revenueNorm = (d.revenue - revenueMin) / revenueRange;
    const height = revenueNorm * heightScale * 3000 + 50;
    const x = startX + colIdx * xSpacing + (Math.random() - 0.5) * 200;
    const z = -800 + Math.random() * 1600;
    positions[i * 3] = x;
    positions[i * 3 + 1] = height + 20 + Math.random() * 100;
    positions[i * 3 + 2] = z;
    velocities[i * 3] = (Math.random() - 0.5) * 15;
    velocities[i * 3 + 1] = -2 + Math.random() * -8;
    velocities[i * 3 + 2] = 30 + Math.random() * 60;
    colors[i * 3] = 0.25 + Math.random() * 0.3;
    colors[i * 3 + 1] = 0.5 + Math.random() * 0.3;
    colors[i * 3 + 2] = 0.9 + Math.random() * 0.1;
    particleData.push({ colIdx, birthZ: z, lifetime: 3 + Math.random() * 8, age: Math.random() * 8 });
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.PointsMaterial({
    size: 6,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
  });
  const points = new THREE.Points(geom, mat);
  return { points, positions, velocities, colors, particleData, maxParticles };
}
function updateParticles(delta, data) {
  if (!particleSystem || !data) return;
  const { positions, velocities, colors, particleData, maxParticles } = particleSystem;
  const cols = data.length;
  const xSpacing = 30;
  const totalWidth = (cols - 1) * xSpacing;
  const startX = -totalWidth / 2;
  const revenueMin = Math.min(...data.map(d => d.revenue));
  const revenueMax = Math.max(...data.map(d => d.revenue));
  const revenueRange = revenueMax - revenueMin || 1;
  const heightScale = 0.6;
  for (let i = 0; i < maxParticles; i++) {
    const pd = particleData[i];
    pd.age += delta;
    if (pd.age > pd.lifetime) {
      pd.age = 0;
      pd.lifetime = 3 + Math.random() * 8;
      const colIdx = Math.floor(Math.random() * cols);
      pd.colIdx = colIdx;
      pd.birthZ = -800 + Math.random() * 1600;
      const d = data[colIdx];
      const revenueNorm = (d.revenue - revenueMin) / revenueRange;
      const height = revenueNorm * heightScale * 3000 + 50;
      positions[i * 3] = startX + colIdx * xSpacing + (Math.random() - 0.5) * 200;
      positions[i * 3 + 1] = height + 20 + Math.random() * 100;
      positions[i * 3 + 2] = pd.birthZ;
      velocities[i * 3] = (Math.random() - 0.5) * 15;
      velocities[i * 3 + 1] = -2 + Math.random() * -8;
      velocities[i * 3 + 2] = 30 + Math.random() * 60;
    }
    positions[i * 3] += velocities[i * 3] * delta;
    positions[i * 3 + 1] += velocities[i * 3 + 1] * delta;
    positions[i * 3 + 2] += velocities[i * 3 + 2] * delta;
    const d = data[pd.colIdx];
    const revenueNorm = (d.revenue - revenueMin) / revenueRange;
    const terrainH = revenueNorm * heightScale * 3000 + 50;
    if (positions[i * 3 + 1] < terrainH + 5) {
      positions[i * 3 + 1] = terrainH + 5;
      velocities[i * 3 + 1] = Math.abs(velocities[i * 3 + 1]) * 0.5;
    }
    const lifeRatio = pd.age / pd.lifetime;
    colors[i * 3 + 3] = lifeRatio < 0.5 ? 1.0 : 2.0 * (1.0 - lifeRatio);
    positions[i * 3 + 2] += (Math.sin(pd.age * 3 + i) * 0.5) * delta * 10;
  }
  particleSystem.points.geometry.attributes.position.needsUpdate = true;
  particleSystem.points.geometry.attributes.color.needsUpdate = true;
}
function rebuildSceneForTimeIndex(index) {
  if (!timeSeriesData || index < 0 || index >= timeSeriesData.length) return;
  currentTimeIndex = index;
  const dataSlice = timeSeriesData.slice(0, index + 1);
  if (dataSlice.length < 2) return;
  let geom = geometryCache.get(dataSlice.length);
  if (!geom) {
    geom = buildTerrainGeometry(dataSlice);
    if (geometryCache.size > 30) {
      const firstKey = geometryCache.keys().next().value;
      geometryCache.get(firstKey)?.dispose();
      geometryCache.delete(firstKey);
    }
    geometryCache.set(dataSlice.length, geom);
  }
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    scene.remove(terrainMesh);
  }
  terrainMesh = buildTerrainMesh(geom);
  scene.add(terrainMesh);
  if (riverGroup) {
    riverGroup.traverse(c => { if (c.geometry && c !== riverGroup) c.geometry.dispose(); });
    scene.remove(riverGroup);
  }
  riverGroup = buildRiverGeometry(dataSlice);
  scene.add(riverGroup);
  if (particleSystem) {
    scene.remove(particleSystem.points);
    particleSystem.points.geometry.dispose();
  }
  particleSystem = buildParticleSystem(dataSlice);
  scene.add(particleSystem.points);
  const last = dataSlice[dataSlice.length - 1];
  dom.hudRevenue.textContent = last.revenue.toFixed(0);
  dom.hudUsers.textContent = last.users.toFixed(0);
  dom.hudErrors.textContent = (last.errors).toFixed(1) + '%';
  dom.timeLabel.textContent = 't=' + index + '/' + (timeSeriesData.length - 1);
}
function onSliderChange() {
  const now = performance.now();
  if (now - lastTerrainBuild < TERRAIN_BUILD_INTERVAL) return;
  lastTerrainBuild = now;
  const idx = parseInt(dom.slider.value);
  rebuildSceneForTimeIndex(idx);
}
function saveBookmark(slot) {
  bookmarks[slot - 1] = {
    position: camera.position.clone(),
    target: controls.target.clone(),
  };
  const btns = document.querySelectorAll('#bookmarks .bm-btn');
  const saveBtn = btns[slot - 1];
  if (saveBtn) saveBtn.classList.add('saved');
}
window.saveBookmark = saveBookmark;
function loadBookmark(slot) {
  const bm = bookmarks[slot - 1];
  if (!bm) return;
  camera.position.copy(bm.position);
  controls.target.copy(bm.target);
  controls.update();
}
window.loadBookmark = loadBookmark;
function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
function animate() {
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1);
  controls.update();
  if (particleSystem && timeSeriesData) {
    const dataSlice = timeSeriesData.slice(0, currentTimeIndex + 1);
    if (dataSlice.length >= 2) updateParticles(delta, dataSlice);
  }
  renderer.render(scene, camera);
  fpsFrames++;
  const now = performance.now();
  if (now - fpsLastTime >= 1000) {
    dom.hudFps.textContent = fpsFrames;
    fpsFrames = 0;
    fpsLastTime = now;
  }
}
function initScene(data) {
  if (!data || data.length === 0) { showState('empty'); return; }
  if (scene) {
    geometryCache.forEach(g => g.dispose());
    geometryCache.clear();
    if (terrainMesh) { terrainMesh.geometry.dispose(); scene.remove(terrainMesh); terrainMesh = null; }
    if (riverGroup) { riverGroup.traverse(c => { if (c.geometry && c !== riverGroup) c.geometry.dispose(); }); scene.remove(riverGroup); riverGroup = null; }
    if (particleSystem) { scene.remove(particleSystem.points); particleSystem.points.geometry.dispose(); particleSystem = null; }
    bookmarks = [null, null, null];
    document.querySelectorAll('#bookmarks .bm-btn').forEach(b => b.classList.remove('saved'));
  }
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a18);
  scene.fog = new THREE.FogExp2(0x0a0a18, 0.000015);
  initRenderer();
  initCamera();
  initControls();
  initLighting();
  const gridHelper = new THREE.GridHelper(8000, 40, 0x223344, 0x111a22);
  scene.add(gridHelper);
  timeSeriesData = data;
  dom.slider.max = data.length - 1;
  dom.slider.value = data.length - 1;
  currentTimeIndex = data.length - 1;
  rebuildSceneForTimeIndex(currentTimeIndex);
  showState('success');
}
async function boot() {
  clock = new THREE.Clock();
  dom.slider.addEventListener('input', onSliderChange);
  window.addEventListener('resize', onResize);
  const data = await fetchData();
  if (data) { initScene(data); animate(); }
}
boot();
</script>
</body>
</html>