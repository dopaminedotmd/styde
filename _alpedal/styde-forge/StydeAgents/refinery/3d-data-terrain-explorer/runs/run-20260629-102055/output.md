<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8d6e5; }
  canvas { display: block; }
  #ui { position: fixed; inset: 0; pointer-events: none; z-index: 10; }
  #ui > * { pointer-events: auto; }
  #tooltip { position: absolute; display: none; background: rgba(10,10,30,0.92); border: 1px solid rgba(100,200,255,0.4); border-radius: 6px; padding: 8px 12px; font-size: 12px; line-height: 1.5; backdrop-filter: blur(8px); white-space: nowrap; }
  #tooltip .label { color: #8899aa; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
  #tooltip .val { color: #e0f0ff; font-weight: 600; }
  #timebar { position: absolute; bottom: 28px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 12px; background: rgba(10,10,30,0.88); border: 1px solid rgba(100,200,255,0.25); border-radius: 8px; padding: 8px 18px; backdrop-filter: blur(8px); }
  #timebar label { font-size: 11px; color: #8899aa; text-transform: uppercase; letter-spacing: 0.5px; }
  #timebar input[type=range] { width: 220px; accent-color: #4ac; }
  #timebar .time-val { font-size: 13px; font-weight: 700; color: #4ac; min-width: 40px; text-align: center; }
  #bookmarks { position: absolute; top: 20px; right: 20px; display: flex; flex-direction: column; gap: 6px; }
  #bookmarks button { background: rgba(10,10,30,0.85); border: 1px solid rgba(100,200,255,0.3); color: #c8d6e5; padding: 6px 14px; border-radius: 5px; cursor: pointer; font-size: 11px; transition: all 0.2s; backdrop-filter: blur(6px); }
  #bookmarks button:hover { background: rgba(30,60,90,0.9); border-color: #4ac; color: #fff; }
  #bookmarks button.active { background: rgba(20,80,120,0.9); border-color: #4ac; color: #4ac; }
  #autorot { position: absolute; top: 20px; right: 20px; }
  #autorot-btn { background: rgba(10,10,30,0.85); border: 1px solid rgba(100,200,255,0.3); color: #c8d6e5; padding: 6px 14px; border-radius: 5px; cursor: pointer; font-size: 11px; backdrop-filter: blur(6px); transition: all 0.2s; }
  #autorot-btn.on { background: rgba(20,80,120,0.9); border-color: #4ac; color: #4ac; }
  #cache-panel { position: absolute; bottom: 28px; left: 20px; background: rgba(10,10,30,0.88); border: 1px solid rgba(100,200,255,0.25); border-radius: 8px; padding: 10px 14px; font-size: 10px; line-height: 1.6; backdrop-filter: blur(8px); min-width: 180px; }
  #cache-panel .title { color: #4ac; font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
  #cache-panel .row { display: flex; justify-content: space-between; gap: 16px; }
  #cache-panel .hit { color: #4caf50; }
  #cache-panel .miss { color: #ff7043; }
</style>
</head>
<body>
<div id="ui">
  <div id="tooltip"><span class="label">HOVER CELL</span><br>Revenue: <span class="val" id="tt-rev">-</span> | Users: <span class="val" id="tt-usr">-</span> | Errors: <span class="val" id="tt-err">-</span></div>
  <div id="timebar">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
    <span class="time-val" id="time-display">00:00</span>
  </div>
  <div id="cache-panel">
    <div class="title">Cache Diagnostics</div>
    <div class="row"><span>Terrain geom</span><span><span class="hit" id="ch-terrain-h">0</span>/<span class="miss" id="ch-terrain-m">0</span></span></div>
    <div class="row"><span>River geom</span><span><span class="hit" id="ch-river-h">0</span>/<span class="miss" id="ch-river-m">0</span></span></div>
    <div class="row"><span>Particle buf</span><span><span class="hit" id="ch-part-h">0</span></span></div>
    <div class="row"><span>Grid xform</span><span><span class="hit" id="ch-xform-h">0</span>/<span class="miss" id="ch-xform-m">0</span></span></div>
  </div>
  <div id="bookmarks">
    <button id="bm-overview" class="active">Overview</button>
    <button id="bm-revenue">Revenue Peak</button>
    <button id="bm-errors">Error Zone</button>
    <button id="bm-save">Save View</button>
  </div>
  <div id="autorot"><button id="autorot-btn" class="on">Auto-Rotate ON</button></div>
</div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID_SIZE = 80;
const TERRAIN_W = 20;
const TERRAIN_D = 20;
const HEIGHT_SCALE = 5.0;
const TIME_STEPS = 24;
const RIVER_DEBOUNCE_MS = 200;
const ERROR_THRESHOLD = 0.65;
const PARTICLE_COUNT = 500;
const cache = {
  terrainGeom: new Map(),
  riverGeom: new Map(),
  terrainHits: 0, terrainMisses: 0,
  riverHits: 0, riverMisses: 0,
  particleReuses: 0,
  xformHits: 0, xformMisses: 0
};
function gaussian(x, z, cx, cz, sx, sz) {
  const dx = (x - cx) / sx;
  const dz = (z - cz) / sz;
  return Math.exp(-0.5 * (dx * dx + dz * dz));
}
function generateData() {
  const series = [];
  const hillDefs = [
    { cx: -0.35, cz: -0.25, sx: 0.40, sz: 0.35, amp: 1.6, driftX: 0.08, driftZ: 0.04 },
    { cx: 0.22, cz: 0.12, sx: 0.50, sz: 0.42, amp: 2.2, driftX: -0.05, driftZ: 0.07 },
    { cx: 0.02, cz: -0.32, sx: 0.55, sz: 0.48, amp: 1.1, driftX: 0.03, driftZ: -0.06 },
    { cx: -0.24, cz: 0.28, sx: 0.32, sz: 0.38, amp: 0.9, driftX: -0.06, driftZ: -0.03 },
    { cx: 0.30, cz: -0.15, sx: 0.28, sz: 0.30, amp: 0.7, driftX: 0.04, driftZ: 0.05 }
  ];
  const errorHotspots = [
    { cx: -0.20, cz: 0.05, sx: 0.18, sz: 0.20, amp: 1.0, driftX: 0.10, driftZ: -0.06, phase: 0 },
    { cx: 0.15, cz: -0.20, sx: 0.14, sz: 0.16, amp: 0.9, driftX: -0.07, driftZ: 0.09, phase: 2.5 },
    { cx: 0.30, cz: 0.22, sx: 0.12, sz: 0.14, amp: 0.7, driftX: 0.05, driftZ: 0.04, phase: 5.0 }
  ];
  for (let t = 0; t < TIME_STEPS; t++) {
    const frac = t / (TIME_STEPS - 1);
    const revenue = new Float32Array(GRID_SIZE * GRID_SIZE);
    const users = new Float32Array(GRID_SIZE * GRID_SIZE);
    const errors = new Float32Array(GRID_SIZE * GRID_SIZE);
    for (let iz = 0; iz < GRID_SIZE; iz++) {
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const x = (ix / (GRID_SIZE - 1) - 0.5);
        const z = (iz / (GRID_SIZE - 1) - 0.5);
        let h = 0;
        // Sum gaussian hills with time drift
        for (const hill of hillDefs) {
          const cx = hill.cx + hill.driftX * frac;
          const cz = hill.cz + hill.driftZ * frac;
          const phaseAmp = 1.0 + 0.2 * Math.sin(frac * Math.PI * 2 + hill.cx * 3);
          h += hill.amp * phaseAmp * gaussian(x, z, cx, cz, hill.sx, hill.sz);
        }
        // Add small-scale noise
        h += 0.08 * Math.sin(x * 12 + frac * 3) * Math.cos(z * 10 - frac * 2);
        h += 0.06 * Math.sin(x * 20 + z * 18 + frac * 5);
        revenue[iz * GRID_SIZE + ix] = Math.max(0, h);
        // User density derived from terrain with offset noise
        let u = h / 3.0 + 0.15 * Math.sin(x * 8 + z * 7) + 0.1 * Math.cos(x * 15 - z * 12 + frac * 4);
        u = Math.max(0, Math.min(1, u));
        users[iz * GRID_SIZE + ix] = u;
        // Error hotspots
        let e = 0;
        for (const hs of errorHotspots) {
          const cx = hs.cx + hs.driftX * frac;
          const cz = hs.cz + hs.driftZ * frac;
          const pulse = 0.7 + 0.3 * Math.sin(frac * Math.PI * 1.5 + hs.phase);
          e += hs.amp * pulse * gaussian(x, z, cx, cz, hs.sx, hs.sz);
        }
        e += 0.04 * Math.abs(Math.sin(x * 14 + z * 13 + frac * 6));
        errors[iz * GRID_SIZE + ix] = Math.max(0, Math.min(1, e));
      }
    }
    series.push({ revenue, users, errors });
  }
  return series;
}
const timeSeries = generateData();
function heightColor(usersVal) {
  // Vegetation gradient: dry brown (0) -> yellow-green (0.5) -> lush green (1)
  if (usersVal < 0.5) {
    const f = usersVal / 0.5;
    return [0.55 + f * 0.15, 0.32 + f * 0.28, 0.12 + f * 0.06];
  }
  const f = (usersVal - 0.5) / 0.5;
  return [0.70 - f * 0.45, 0.60 + f * 0.20, 0.18 + f * 0.30];
}
function buildTerrainGeometry(timeIndex) {
  if (cache.terrainGeom.has(timeIndex)) {
    cache.terrainHits++;
    return cache.terrainGeom.get(timeIndex);
  }
  cache.terrainMisses++;
  const data = timeSeries[timeIndex];
  const geo = new THREE.PlaneGeometry(TERRAIN_W, TERRAIN_D, GRID_SIZE - 1, GRID_SIZE - 1);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position.array;
  const vcount = pos.length / 3;
  const colors = new Float32Array(vcount * 3);
  for (let i = 0; i < vcount; i++) {
    const x = pos[i * 3];
    const z = pos[i * 3 + 2];
    const ix = Math.round((x / TERRAIN_W + 0.5) * (GRID_SIZE - 1));
    const iz = Math.round((z / TERRAIN_D + 0.5) * (GRID_SIZE - 1));
    const ci = Math.max(0, Math.min(GRID_SIZE - 1, ix));
    const cj = Math.max(0, Math.min(GRID_SIZE - 1, iz));
    const h = data.revenue[cj * GRID_SIZE + ci] * HEIGHT_SCALE;
    pos[i * 3 + 1] = h;
    const [cr, cg, cb] = heightColor(data.users[cj * GRID_SIZE + ci]);
    colors[i * 3] = cr;
    colors[i * 3 + 1] = cg;
    colors[i * 3 + 2] = cb;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  cache.terrainGeom.set(timeIndex, geo);
  return geo;
}
function findErrorPaths(timeIndex) {
  const data = timeSeries[timeIndex];
  const visited = new Uint8Array(GRID_SIZE * GRID_SIZE);
  const paths = [];
  // Find all error cells above threshold
  const errorCells = [];
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      if (data.errors[iz * GRID_SIZE + ix] > ERROR_THRESHOLD) {
        errorCells.push({ ix, iz, err: data.errors[iz * GRID_SIZE + ix] });
      }
    }
  }
  // Group connected error cells and trace river for each group
  const dirs = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  for (const seed of errorCells) {
    if (visited[seed.iz * GRID_SIZE + seed.ix]) continue;
    // Flood fill to find connected component
    const component = [];
    const stack = [seed];
    visited[seed.iz * GRID_SIZE + seed.ix] = 1;
    while (stack.length > 0) {
      const cell = stack.pop();
      component.push(cell);
      for (const [dx, dz] of dirs) {
        const nx = cell.ix + dx;
        const nz = cell.iz + dz;
        if (nx < 0 || nx >= GRID_SIZE || nz < 0 || nz >= GRID_SIZE) continue;
        if (visited[nz * GRID_SIZE + nx]) continue;
        if (data.errors[nz * GRID_SIZE + nx] > ERROR_THRESHOLD * 0.7) {
          visited[nz * GRID_SIZE + nx] = 1;
          stack.push({ ix: nx, iz: nz, err: data.errors[nz * GRID_SIZE + nx] });
        }
      }
    }
    if (component.length < 3) continue;
    // Sort by error value descending, take top points as path
    component.sort((a, b) => b.err - a.err);
    const pathPoints = [];
    const step = Math.max(1, Math.floor(component.length / 12));
    for (let i = 0; i < component.length && pathPoints.length < 15; i += step) {
      const c = component[i];
      const wx = (c.ix / (GRID_SIZE - 1) - 0.5) * TERRAIN_W;
      const wz = (c.iz / (GRID_SIZE - 1) - 0.5) * TERRAIN_D;
      const wy = data.revenue[c.iz * GRID_SIZE + c.ix] * HEIGHT_SCALE + 0.08;
      pathPoints.push(new THREE.Vector3(wx, wy, wz));
    }
    if (pathPoints.length >= 2) paths.push(pathPoints);
  }
  return paths;
}
function buildRiverGeometry(timeIndex) {
  if (cache.riverGeom.has(timeIndex)) {
    cache.riverHits++;
    return cache.riverGeom.get(timeIndex);
  }
  cache.riverMisses++;
  const paths = findErrorPaths(timeIndex);
  const group = new THREE.Group();
  const material = new THREE.MeshStandardMaterial({
    color: 0xe63946, roughness: 0.4, metalness: 0.2, emissive: 0x330808, emissiveIntensity: 0.6
  });
  for (const points of paths) {
    if (points.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, 48, 0.12, 8, false);
    const mesh = new THREE.Mesh(tubeGeo, material);
    mesh.renderOrder = 1;
    mesh.material.depthTest = true;
    mesh.material.depthWrite = true;
    group.add(mesh);
  }
  cache.riverGeom.set(timeIndex, group);
  return group;
}
let riverDebounceTimer = null;
let pendingRiverTimeIndex = null;
function requestRiverRebuild(timeIndex, callback) {
  pendingRiverTimeIndex = timeIndex;
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    riverDebounceTimer = null;
    if (pendingRiverTimeIndex !== null) {
      callback(pendingRiverTimeIndex);
      pendingRiverTimeIndex = null;
    }
  }, RIVER_DEBOUNCE_MS);
}
function createGlowTexture() {
  const size = 32;
  const canvas = document.createElement('canvas');
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0, 'rgba(255,255,220,1)');
  grad.addColorStop(0.15, 'rgba(255,220,150,0.9)');
  grad.addColorStop(0.4, 'rgba(255,180,80,0.5)');
  grad.addColorStop(0.7, 'rgba(255,120,40,0.1)');
  grad.addColorStop(1, 'rgba(255,60,20,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}
function buildParticleSystem() {
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const particleData = [];
  // Define source/sink regions in world space
  const sources = [
    { x: -4, z: -4 }, { x: 5, z: 2 }, { x: -6, z: 3 }, { x: 3, z: -5 }
  ];
  const sinks = [
    { x: 3, z: 3 }, { x: -5, z: -2 }, { x: 4, z: -3 }, { x: -3, z: 4 }
  ];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const src = sources[i % sources.length];
    const dst = sinks[Math.floor(Math.random() * sinks.length)];
    const t = Math.random();
    const sx = src.x + (Math.random() - 0.5) * 2.0;
    const sz = src.z + (Math.random() - 0.5) * 2.0;
    positions[i * 3] = sx;
    positions[i * 3 + 1] = 0;
    positions[i * 3 + 2] = sz;
    particleData.push({
      srcX: sx, srcZ: sz,
      dstX: dst.x + (Math.random() - 0.5) * 1.5,
      dstZ: dst.z + (Math.random() - 0.5) * 1.5,
      t: t,
      speed: 0.08 + Math.random() * 0.18
    });
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.18,
    map: createGlowTexture(),
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    color: 0xffcc66,
    opacity: 0.85
  });
  const points = new THREE.Points(geo, mat);
  points.renderOrder = 2;
  return { points, data: particleData, positions };
}
function sampleTerrainHeight(wx, wz, timeIndex) {
  const data = timeSeries[timeIndex];
  const ix = Math.round((wx / TERRAIN_W + 0.5) * (GRID_SIZE - 1));
  const iz = Math.round((wz / TERRAIN_D + 0.5) * (GRID_SIZE - 1));
  const ci = Math.max(0, Math.min(GRID_SIZE - 1, ix));
  const cj = Math.max(0, Math.min(GRID_SIZE - 1, iz));
  return data.revenue[cj * GRID_SIZE + ci] * HEIGHT_SCALE;
}
function updateParticles(particleSys, timeIndex, dt) {
  const { data, positions } = particleSys;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const p = data[i];
    p.t += p.speed * dt;
    if (p.t > 1.0) p.t -= 1.0;
    const wx = p.srcX + (p.dstX - p.srcX) * p.t;
    const wz = p.srcZ + (p.dstZ - p.srcZ) * p.t;
    const wy = sampleTerrainHeight(wx, wz, timeIndex) + 0.3 + 0.15 * Math.sin(p.t * Math.PI);
    positions[i * 3] = wx;
    positions[i * 3 + 1] = wy;
    positions[i * 3 + 2] = wz;
  }
  particleSys.points.geometry.attributes.position.needsUpdate = true;
  cache.particleReuses++;
}
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 15, 60);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(8, 10, 14);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 4;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.48;
controls.target.set(0, 1.5, 0);
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 1.4);
scene.add(ambientLight);
const hemiLight = new THREE.HemisphereLight(0x8899cc, 0x223344, 0.9);
scene.add(hemiLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 2.5);
sunLight.position.set(10, 15, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -15;
sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15;
sunLight.shadow.camera.bottom = -15;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.65, metalness: 0.05, flatShading: false, side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(new THREE.BufferGeometry(), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
let riverGroup = new THREE.Group();
scene.add(riverGroup);
const particleSys = buildParticleSystem();
scene.add(particleSys.points);
// Base reference grid
const gridHelper = new THREE.PolarGridHelper(12, 32, 24, 128, 0x334466, 0x223355);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
const ttRev = document.getElementById('tt-rev');
const ttUsr = document.getElementById('tt-usr');
const ttErr = document.getElementById('tt-err');
// Memoization state for world-to-grid transform on hover path
const memoWorldPos = new THREE.Vector3();
let memoGridResult = null;
const MEMO_EPSILON = 0.015;
function worldToGrid(worldPos) {
  if (memoGridResult && worldPos.distanceToSquared(memoWorldPos) < MEMO_EPSILON * MEMO_EPSILON) {
    cache.xformHits++;
    return memoGridResult;
  }
  cache.xformMisses++;
  const ix = Math.round((worldPos.x / TERRAIN_W + 0.5) * (GRID_SIZE - 1));
  const iz = Math.round((worldPos.z / TERRAIN_D + 0.5) * (GRID_SIZE - 1));
  memoWorldPos.copy(worldPos);
  memoGridResult = { ix: Math.max(0, Math.min(GRID_SIZE - 1, ix)), iz: Math.max(0, Math.min(GRID_SIZE - 1, iz)) };
  return memoGridResult;
}
let currentTimeIndex = 0;
function swapTerrain(timeIndex) {
  const geo = buildTerrainGeometry(timeIndex);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = geo;
}
function swapRivers(timeIndex) {
  // Remove old river children
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    riverGroup.remove(child);
  }
  scene.remove(riverGroup);
  riverGroup = buildRiverGeometry(timeIndex);
  scene.add(riverGroup);
}
function setTimeIndex(idx) {
  currentTimeIndex = idx;
  swapTerrain(idx);
  // Debounced river rebuild — avoids TubeGeometry allocation on every tick
  requestRiverRebuild(idx, (ti) => swapRivers(ti));
  updateUIDisplay(idx);
}
function updateUIDisplay(idx) {
  const hours = Math.floor(idx);
  document.getElementById('time-display').textContent =
    String(hours).padStart(2, '0') + ':00';
  document.getElementById('time-slider').value = idx;
}
// Camera bookmarks
const bookmarks = [
  { name: 'overview', pos: new THREE.Vector3(8, 10, 14), target: new THREE.Vector3(0, 1.5, 0) },
  { name: 'revenue', pos: new THREE.Vector3(2, 5, 6), target: new THREE.Vector3(1.5, 3.5, 0.8) },
  { name: 'errors', pos: new THREE.Vector3(-3, 3, 3), target: new THREE.Vector3(-2.5, 1.8, 0.5) }
];
let activeBookmark = 'overview';
function applyBookmark(bm) {
  controls.target.copy(bm.target);
  camera.position.copy(bm.pos);
  controls.update();
  activeBookmark = bm.name;
  document.querySelectorAll('#bookmarks button').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById('bm-' + bm.name);
  if (btn) btn.classList.add('active');
}
function saveCurrentView() {
  const existing = bookmarks.find(b => b.name === 'saved');
  const bm = existing || { name: 'saved', pos: new THREE.Vector3(), target: new THREE.Vector3() };
  bm.pos.copy(camera.position);
  bm.target.copy(controls.target);
  if (!existing) bookmarks.push(bm);
}
// UI event wiring — every named UI element has a real event handler
document.getElementById('time-slider').addEventListener('input', (e) => {
  setTimeIndex(parseInt(e.target.value));
});
document.getElementById('bm-overview').addEventListener('click', () => applyBookmark(bookmarks[0]));
document.getElementById('bm-revenue').addEventListener('click', () => applyBookmark(bookmarks[1]));
document.getElementById('bm-errors').addEventListener('click', () => applyBookmark(bookmarks[2]));
document.getElementById('bm-save').addEventListener('click', () => {
  saveCurrentView();
  applyBookmark(bookmarks.find(b => b.name === 'saved') || bookmarks[0]);
});
const autorotBtn = document.getElementById('autorot-btn');
autorotBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autorotBtn.textContent = controls.autoRotate ? 'Auto-Rotate ON' : 'Auto-Rotate OFF';
  autorotBtn.classList.toggle('on', controls.autoRotate);
});
// Tooltip hover with raycasting
window.addEventListener('mousemove', (event) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const grid = worldToGrid(point);
    const data = timeSeries[currentTimeIndex];
    const idx = grid.iz * GRID_SIZE + grid.ix;
    ttRev.textContent = (data.revenue[idx] * 100).toFixed(1) + '%';
    ttUsr.textContent = (data.users[idx] * 100).toFixed(1) + '%';
    ttErr.textContent = (data.errors[idx] * 100).toFixed(1) + '%';
    tooltip.style.display = 'block';
    tooltip.style.left = (event.clientX + 18) + 'px';
    tooltip.style.top = (event.clientY - 10) + 'px';
  } else {
    tooltip.style.display = 'none';
    memoGridResult = null;
  }
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Cache diagnostics panel update
function updateCachePanel() {
  document.getElementById('ch-terrain-h').textContent = cache.terrainHits;
  document.getElementById('ch-terrain-m').textContent = cache.terrainMisses;
  document.getElementById('ch-river-h').textContent = cache.riverHits;
  document.getElementById('ch-river-m').textContent = cache.riverMisses;
  document.getElementById('ch-part-h').textContent = cache.particleReuses;
  document.getElementById('ch-xform-h').textContent = cache.xformHits;
  document.getElementById('ch-xform-m').textContent = cache.xformMisses;
}
// Animation loop
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  updateParticles(particleSys, currentTimeIndex, dt);
  renderer.render(scene, camera);
  updateCachePanel();
}
// Initialization
setTimeIndex(0);
applyBookmark(bookmarks[0]);
animate();
</script>
</body>
</html>