<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a0f; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; }
  #container { position: fixed; inset: 0; }
  canvas { display: block; }
  #ui { position: fixed; bottom: 0; left: 0; right: 0; z-index: 10; pointer-events: none; }
  #ui > * { pointer-events: auto; }
  #panel { position: fixed; top: 12px; right: 12px; z-index: 10; background: rgba(10,10,20,0.85); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 12px 16px; color: #ccc; font-size: 12px; min-width: 200px; backdrop-filter: blur(8px); }
  #panel h3 { color: #8af; margin: 0 0 6px 0; font-size: 13px; font-weight: 600; }
  #panel .stat { display: flex; justify-content: space-between; padding: 2px 0; }
  #panel .stat .val { color: #fff; font-variant-numeric: tabular-nums; }
  #panel .stat .hit { color: #4f8; }
  #panel .stat .miss { color: #f84; }
  #timeline { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 10; display: flex; gap: 8px; align-items: center; background: rgba(10,10,20,0.85); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 8px 16px; backdrop-filter: blur(8px); }
  #timeline label { color: #aaa; font-size: 11px; white-space: nowrap; }
  #timeline input[type=range] { width: 200px; accent-color: #8af; }
  #timeline .ts-label { color: #fff; font-size: 12px; min-width: 60px; text-align: center; }
  #bookmarks { position: fixed; bottom: 20px; right: 20px; z-index: 10; display: flex; gap: 4px; }
  #bookmarks button { background: rgba(10,10,20,0.85); border: 1px solid rgba(255,255,255,0.15); color: #aaa; padding: 6px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; transition: all 0.2s; }
  #bookmarks button:hover { border-color: #8af; color: #fff; }
  #legend { position: fixed; top: 12px; left: 12px; z-index: 10; background: rgba(10,10,20,0.85); border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; padding: 10px 14px; backdrop-filter: blur(8px); }
  #legend .item { display: flex; align-items: center; gap: 6px; margin: 3px 0; font-size: 11px; color: #aaa; }
  #legend .swatch { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
</style>
</head>
<body>
<div id="container"></div>
<div id="panel">
  <h3>Cache Diagnostics</h3>
  <div class="stat"><span>Terrain geom</span><span class="val" id="cache-terrain">0/0</span></div>
  <div class="stat"><span>River geom</span><span class="val" id="cache-river">0/0</span></div>
  <div class="stat"><span>Grid lookup</span><span class="val" id="cache-grid">0/0</span></div>
  <div class="stat"><span>FPS</span><span class="val" id="stat-fps">60</span></div>
</div>
<div id="legend">
  <div class="item"><span class="swatch" style="background:#4af;"></span> Revenue (height)</div>
  <div class="item"><span class="swatch" style="background:#f44;"></span> Error rivers</div>
  <div class="item"><span class="swatch" style="background:#ff0;"></span> API call trails</div>
  <div class="item"><span class="swatch" style="background:linear-gradient(90deg,#2a2,#ff0,#f40);"></span> User density color</div>
</div>
<div id="timeline">
  <label>Time</label>
  <input type="range" id="timeSlider" min="0" max="4" value="0" step="1">
  <span class="ts-label" id="timeLabel">T0</span>
</div>
<div id="bookmarks">
  <button data-bm="0">Top-down</button>
  <button data-bm="1">Valley</button>
  <button data-bm="2">Close-up</button>
  <button id="btn-save-bm">Save View</button>
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
const GRID = 64;
const TIME_STEPS = 5;
const TERRAIN_SCALE = 4.0;
const TERRAIN_SIZE = 20;
const container = document.getElementById('container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.Fog(0x0a0a0f, 30, 80);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 120);
camera.position.set(18, 14, 18);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 1, 0);
controls.maxPolarAngle = Math.PI * 0.55;
controls.minDistance = 6;
controls.maxDistance = 45;
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 2.5);
scene.add(ambientLight);
const sun = new THREE.DirectionalLight(0xffeedd, 6);
sun.position.set(20, 25, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -25;
sun.shadow.camera.right = 25;
sun.shadow.camera.top = 25;
sun.shadow.camera.bottom = -25;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x334477, 2);
fill.position.set(-10, 5, -8);
scene.add(fill);
const gridHelper = new THREE.GridHelper(TERRAIN_SIZE, 40, 0x223344, 0x111122);
gridHelper.position.y = -2.5;
scene.add(gridHelper);
function generateData(t) {
  const revenue = new Float32Array(GRID * GRID);
  const users = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  const apiCalls = new Float32Array(GRID * GRID);
  const tp = t * 0.7;
  for (let iy = 0; iy < GRID; iy++) {
    const ny = (iy / (GRID - 1) - 0.5) * TERRAIN_SIZE;
    for (let ix = 0; ix < GRID; ix++) {
      const nx = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const idx = iy * GRID + ix;
      const d = Math.sqrt(nx * nx + ny * ny) * 0.4;
      revenue[idx] = Math.sin(nx * 0.8 + tp) * Math.cos(ny * 0.7 + tp * 0.9) * 2.5
        + Math.sin(nx * 0.3 - ny * 0.4 + d + tp * 0.6) * 2.0
        + Math.cos((nx + ny) * 0.5 + tp * 1.2) * 1.5;
      users[idx] = Math.cos(nx * 0.6 + tp * 0.5) * Math.sin(ny * 0.55 + tp * 0.4) * 1.8
        + Math.sin(nx * 0.25 + ny * 0.25 + tp * 0.8) * 1.5 + 1.0;
      const revDip = Math.max(0, -revenue[idx]) * 0.8;
      const userSpike = Math.max(0, users[idx] - 1.5) * 0.6;
      const anomalySeed = Math.sin(nx * 1.7 + tp) * Math.cos(ny * 1.3 - tp * 0.7);
      errors[idx] = (revDip + userSpike) * 0.7 + Math.max(0, anomalySeed * 0.4);
      apiCalls[idx] = Math.max(0, Math.sin(nx * 0.9 + ny * 0.3 + tp * 1.5) * Math.cos(nx * 0.2 - ny * 0.8 + tp))
        * 1.8 + Math.abs(Math.sin(nx * 0.15 - ny * 0.15 + d * 0.5 + tp)) * 1.2;
    }
  }
  return { revenue, users, errors, apiCalls };
}
const allData = [];
for (let t = 0; t < TIME_STEPS; t++) allData.push(generateData(t));
function userDensityToColor(density) {
  const v = Math.max(0, Math.min(1, density * 0.35));
  if (v < 0.5) return new THREE.Color().setHSL(0.28 - v * 0.25, 0.7, 0.25 + v * 0.6);
  return new THREE.Color().setHSL(0.1 - (v - 0.5) * 0.15, 0.85, 0.4 + v * 0.5);
}
const terrainCache = new Map();
const riverCache = new Map();
const gridLookupCache = { misses: 0, hits: 0 };
function buildTerrainGeometry(t) {
  if (terrainCache.has(t)) { return terrainCache.get(t); }
  const data = allData[t];
  const geom = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, GRID - 1, GRID - 1);
  geom.rotateX(-Math.PI / 2);
  const pos = geom.attributes.position.array;
  const colors = new Float32Array(pos.length);
  for (let i = 0; i < pos.length / 3; i++) {
    const idx = i;
    pos[i * 3 + 1] = data.revenue[idx] * TERRAIN_SCALE;
    const c = userDensityToColor(data.users[idx]);
    colors[i * 3] = c.r;
    colors[i * 3 + 1] = c.g;
    colors[i * 3 + 2] = c.b;
  }
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.computeVertexNormals();
  terrainCache.set(t, geom);
  updateCacheUI();
  return geom;
}
function buildRiverGeometry(t) {
  if (riverCache.has(t)) { return riverCache.get(t); }
  const data = allData[t];
  const points = [];
  const threshold = 0.35;
  const visited = new Uint8Array(GRID * GRID);
  const dirs = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  const half = TERRAIN_SIZE / 2;
  function trace(startX, startY) {
    let cx = startX, cy = startY;
    const path = [];
    for (let step = 0; step < 80; step++) {
      if (cx < 0 || cx >= GRID || cy < 0 || cy >= GRID) break;
      const idx = cy * GRID + cx;
      if (visited[idx]) break;
      visited[idx] = 1;
      const wx = (cx / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const wz = (cy / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      path.push(new THREE.Vector3(wx, data.revenue[idx] * TERRAIN_SCALE + 0.15, wz));
      let bestDir = null, bestErr = -1;
      for (const [dx, dy] of dirs) {
        const nx = cx + dx, ny = cy + dy;
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        const nidx = ny * GRID + nx;
        if (visited[nidx]) continue;
        if (data.errors[nidx] > bestErr) { bestErr = data.errors[nidx]; bestDir = [dx, dy]; }
      }
      if (!bestDir || bestErr < threshold * 0.3) break;
      cx += bestDir[0]; cy += bestDir[1];
    }
    if (path.length > 4) points.push(path);
  }
  for (let iy = 0; iy < GRID; iy += 3) {
    for (let ix = 0; ix < GRID; ix += 3) {
      if (data.errors[iy * GRID + ix] > threshold) trace(ix, iy);
    }
  }
  const group = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: 0xff3030, roughness: 0.4, metalness: 0.3, emissive: 0x330000 });
  points.forEach(path => {
    if (path.length < 5) return;
    const curve = new THREE.CatmullRomCurve3(path);
    const tubeGeom = new THREE.TubeGeometry(curve, path.length * 2, 0.12, 6, false);
    const mesh = new THREE.Mesh(tubeGeom, mat);
    mesh.castShadow = true;
    group.add(mesh);
  });
  riverCache.set(t, group);
  updateCacheUI();
  return group;
}
function gridToWorld(ix, iy) {
  return new THREE.Vector3(
    (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE,
    0,
    (iy / (GRID - 1) - 0.5) * TERRAIN_SIZE
  );
}
const worldToGridCache = new Map();
function worldToGrid(wx, wz) {
  const key = `${wx.toFixed(2)},${wz.toFixed(2)}`;
  if (worldToGridCache.has(key)) { gridLookupCache.hits++; return worldToGridCache.get(key); }
  gridLookupCache.misses++;
  const ix = Math.round(((wx / TERRAIN_SIZE) + 0.5) * (GRID - 1));
  const iy = Math.round(((wz / TERRAIN_SIZE) + 0.5) * (GRID - 1));
  const result = { ix: Math.max(0, Math.min(GRID - 1, ix)), iy: Math.max(0, Math.min(GRID - 1, iy)) };
  worldToGridCache.set(key, result);
  if (worldToGridCache.size > 2000) { const first = worldToGridCache.keys().next().value; worldToGridCache.delete(first); }
  return result;
}
let currentTerrain = null;
let currentRiver = null;
let currentTime = 0;
const terrainGroup = new THREE.Group();
scene.add(terrainGroup);
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.1,
  flatShading: false,
  side: THREE.DoubleSide,
});
function setTimeStep(t) {
  if (t === currentTime && currentTerrain) return;
  currentTime = t;
  if (currentTerrain) { terrainGroup.remove(currentTerrain); currentTerrain.geometry.dispose(); }
  if (currentRiver) { riverGroup.clear(); disposeRiverGroup(currentRiver); currentRiver = null; }
  const geom = buildTerrainGeometry(t);
  currentTerrain = new THREE.Mesh(geom, terrainMat);
  currentTerrain.castShadow = true;
  currentTerrain.receiveShadow = true;
  terrainGroup.add(currentTerrain);
  currentRiver = buildRiverGeometry(t);
  riverGroup.add(currentRiver);
  document.getElementById('timeLabel').textContent = `T${t}`;
}
function disposeRiverGroup(g) {
  g.traverse(child => { if (child.geometry) child.geometry.dispose(); });
}
const PARTICLE_COUNT = 600;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = new Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const sx = Math.random() * GRID;
  const sy = Math.random() * GRID;
  particleData[i] = { x: sx, y: sy, speed: 0.3 + Math.random() * 0.8, phase: Math.random() * Math.PI * 2 };
  const wp = gridToWorld(Math.floor(sx), Math.floor(sy));
  particlePositions[i * 3] = wp.x;
  particlePositions[i * 3 + 1] = 0.2;
  particlePositions[i * 3 + 2] = wp.z;
  particleColors[i * 3] = 1.0;
  particleColors[i * 3 + 1] = 0.85;
  particleColors[i * 3 + 2] = 0.2;
}
const particleGeom = new THREE.BufferGeometry();
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.18,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
});
const particles = new THREE.Points(particleGeom, particleMat);
scene.add(particles);
function updateParticles(dt, t) {
  const data = allData[t];
  const posArr = particles.geometry.attributes.position.array;
  const half = TERRAIN_SIZE / 2;
  const scale = TERRAIN_SCALE;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    const gx = Math.floor(pd.x), gy = Math.floor(pd.y);
    const idx = Math.max(0, Math.min(GRID - 1, gy)) * GRID + Math.max(0, Math.min(GRID - 1, gx));
    const flowX = Math.cos(pd.x * 0.3 + pd.y * 0.2 + pd.phase) * 0.5;
    const flowY = Math.sin(pd.x * 0.2 - pd.y * 0.3 + pd.phase) * 0.5;
    pd.x += flowX * pd.speed * dt;
    pd.y += flowY * pd.speed * dt;
    if (pd.x < 0) pd.x += GRID;
    if (pd.x >= GRID) pd.x -= GRID;
    if (pd.y < 0) pd.y += GRID;
    if (pd.y >= GRID) pd.y -= GRID;
    const wx = (pd.x / (GRID - 1) - 0.5) * TERRAIN_SIZE;
    const wz = (pd.y / (GRID - 1) - 0.5) * TERRAIN_SIZE;
    const h = data.revenue[idx] * scale + 0.4;
    posArr[i * 3] = wx;
    posArr[i * 3 + 1] = h;
    posArr[i * 3 + 2] = wz;
  }
  particles.geometry.attributes.position.needsUpdate = true;
}
const bookmarks = [
  { name: 'Top-down', pos: [0, 28, 0.1], target: [0, 0, 0] },
  { name: 'Valley', pos: [14, 6, 14], target: [2, -0.5, 2] },
  { name: 'Close-up', pos: [5, 3, 7], target: [1, 0.5, 1.5] },
];
function applyBookmark(bm) {
  controls.target.set(bm.target[0], bm.target[1], bm.target[2]);
  camera.position.set(bm.pos[0], bm.pos[1], bm.pos[2]);
  controls.update();
}
document.querySelectorAll('#bookmarks button[data-bm]').forEach(btn => {
  btn.addEventListener('click', () => applyBookmark(bookmarks[parseInt(btn.dataset.bm)]));
});
document.getElementById('btn-save-bm').addEventListener('click', () => {
  const bm = {
    name: `View ${bookmarks.length + 1}`,
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
  };
  bookmarks.push(bm);
  const btn = document.createElement('button');
  btn.dataset.bm = bookmarks.length - 1;
  btn.textContent = bm.name;
  btn.addEventListener('click', () => applyBookmark(bm));
  document.getElementById('bookmarks').insertBefore(btn, document.getElementById('btn-save-bm'));
});
const timeSlider = document.getElementById('timeSlider');
let debounceTimer = null;
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value);
  document.getElementById('timeLabel').textContent = `T${t}`;
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => setTimeStep(t), 200);
});
timeSlider.addEventListener('change', () => {
  if (debounceTimer) { clearTimeout(debounceTimer); debounceTimer = null; }
  setTimeStep(parseInt(timeSlider.value));
});
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
function updateCacheUI() {
  document.getElementById('cache-terrain').innerHTML =
    `<span class="hit">${terrainCache.size}</span> / ${TIME_STEPS}`;
  document.getElementById('cache-river').innerHTML =
    `<span class="hit">${riverCache.size}</span> / ${TIME_STEPS}`;
  const total = gridLookupCache.hits + gridLookupCache.misses;
  const hitRate = total > 0 ? ((gridLookupCache.hits / total) * 100).toFixed(0) : 0;
  document.getElementById('cache-grid').innerHTML =
    `<span class="hit">${gridLookupCache.hits}</span> / <span class="miss">${total}</span> (${hitRate}%)`;
}
let fpsFrames = 0, fpsTime = performance.now();
function updateFPS(now) {
  fpsFrames++;
  if (now - fpsTime >= 1000) {
    document.getElementById('stat-fps').textContent = Math.round(fpsFrames / ((now - fpsTime) / 1000));
    fpsFrames = 0;
    fpsTime = now;
  }
}
setTimeStep(0);
let lastTime = performance.now();
function animate(now) {
  requestAnimationFrame(animate);
  const dt = Math.min((now - lastTime) / 1000, 0.1);
  lastTime = now;
  controls.update();
  updateParticles(dt, currentTime);
  renderer.render(scene, camera);
  updateFPS(now);
  updateCacheUI();
}
requestAnimationFrame(animate);
console.log('3D Data Terrain Explorer ready — GRID:' + GRID + ' TIME_STEPS:' + TIME_STEPS + ' PARTICLES:' + PARTICLE_COUNT);
console.log('Cache: terrain=' + terrainCache.size + ' river=' + riverCache.size);
</script>
</body>
</html>