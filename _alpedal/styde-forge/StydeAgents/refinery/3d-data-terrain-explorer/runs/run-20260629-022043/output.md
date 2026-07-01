<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10,10,25,0.92);
    --text: #c8c8d8;
    --accent: #4fc3f7;
    --danger: #ef5350;
    --success: #66bb6a;
    --warn: #ffa726;
    --border: rgba(255,255,255,0.08);
    --shadow: 0 4px 24px rgba(0,0,0,0.5);
    --radius: 10px;
    --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    font-family: var(--font);
    overflow: hidden;
    height: 100vh;
    width: 100vw;
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
  .panel {
    position: fixed;
    z-index: 10;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: var(--shadow);
    padding: 14px 18px;
    font-size: 13px;
    min-width: 200px;
  }
  #time-panel {
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 20px;
  }
  #time-slider {
    width: 320px;
    accent-color: var(--accent);
    cursor: pointer;
  }
  #time-label {
    font-variant-numeric: tabular-nums;
    font-weight: 600;
    color: var(--accent);
    min-width: 110px;
    text-align: center;
  }
  #legend-panel {
    top: 20px;
    right: 20px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .legend-item { display: flex; align-items: center; gap: 8px; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
  #bookmark-panel {
    top: 20px;
    left: 20px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .bookmark-btn {
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    font-family: var(--font);
    transition: all 0.2s;
    text-align: left;
  }
  .bookmark-btn:hover { background: rgba(255,255,255,0.12); border-color: var(--accent); }
  #metrics-panel {
    bottom: 100px;
    left: 20px;
    display: flex;
    gap: 16px;
  }
  .metric {
    text-align: center;
  }
  .metric-value {
    font-size: 22px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    color: var(--accent);
  }
  .metric-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.6;
  }
  #status-bar {
    position: fixed;
    bottom: 10px;
    right: 20px;
    z-index: 10;
    font-size: 11px;
    opacity: 0.5;
    font-variant-numeric: tabular-nums;
  }
  .tooltip {
    position: fixed;
    pointer-events: none;
    z-index: 100;
    background: rgba(0,0,0,0.85);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    display: none;
    white-space: nowrap;
  }
  @media (max-width: 768px) {
    #time-slider { width: 180px; }
    .panel { padding: 10px 14px; font-size: 11px; }
    #legend-panel { top: 8px; right: 8px; }
    #bookmark-panel { top: 8px; left: 8px; }
    #metrics-panel { bottom: 90px; left: 8px; }
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div class="panel" id="legend-panel">
  <div class="legend-item"><span class="legend-swatch" style="background:#4caf50;"></span> Elevation (Revenue)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(135deg,#2e7d32,#ff9800,#f44336);"></span> User Density</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ef5350;"></span> Error Rivers</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#4fc3f7;"></span> API Call Trails</div>
</div>
<div class="panel" id="bookmark-panel">
  <button class="bookmark-btn" data-bookmark="overview">Overview</button>
  <button class="bookmark-btn" data-bookmark="north">North Face</button>
  <button class="bookmark-btn" data-bookmark="valley">Valley View</button>
  <button class="bookmark-btn" data-bookmark="topdown">Top-Down</button>
  <button class="bookmark-btn" data-bookmark="save" style="color:var(--accent);">Save Current</button>
</div>
<div class="panel" id="metrics-panel">
  <div class="metric"><div class="metric-value" id="metric-revenue">$0</div><div class="metric-label">Revenue</div></div>
  <div class="metric"><div class="metric-value" id="metric-users">0</div><div class="metric-label">Users</div></div>
  <div class="metric"><div class="metric-value" id="metric-errors">0%</div><div class="metric-label">Error Rate</div></div>
  <div class="metric"><div class="metric-value" id="metric-calls">0</div><div class="metric-label">API Calls/s</div></div>
</div>
<div class="panel" id="time-panel">
  <span style="opacity:0.5;">◀</span>
  <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
  <span style="opacity:0.5;">▶</span>
  <span id="time-label">12:00</span>
  <button id="auto-play-btn" style="background:none;border:1px solid var(--border);color:var(--text);padding:4px 10px;border-radius:5px;cursor:pointer;font-size:12px;">▶ Play</button>
</div>
<div class="tooltip" id="tooltip"></div>
<div id="status-bar">3D Data Terrain | Drag: orbit · Scroll: zoom · Right-drag: pan</div>
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
const GRID = 80;
const SPACING = 0.5;
const TERRAIN_W = GRID * SPACING;
const TERRAIN_D = GRID * SPACING;
const HEIGHT_SCALE = 8;
const PARTICLE_COUNT = 400;
const RIVER_COUNT = 5;
let scene, camera, renderer, controls;
let terrainMesh, riverGroup, particleSystem;
let clock = new THREE.Clock();
let timeIndex = 12;
let autoPlaying = false;
let autoPlayDir = 1;
let autoPlayTimer = null;
let raycaster = new THREE.Raycaster();
let mouse = new THREE.Vector2();
let hoveredVertex = null;
let bookmarks = {
  overview: { pos: [18, 14, 18], target: [TERRAIN_W/2, 0, TERRAIN_D/2] },
  north: { pos: [TERRAIN_W/2, 12, -8], target: [TERRAIN_W/2, 0, TERRAIN_D/2] },
  valley: { pos: [TERRAIN_W+6, 4, TERRAIN_D/2], target: [TERRAIN_W/2, -2, TERRAIN_D/2] },
  topdown: { pos: [TERRAIN_W/2, 22, TERRAIN_D/2+0.1], target: [TERRAIN_W/2, 0, TERRAIN_D/2] }
};
let savedBookmark = null;
const statsEl = {
  revenue: document.getElementById('metric-revenue'),
  users: document.getElementById('metric-users'),
  errors: document.getElementById('metric-errors'),
  calls: document.getElementById('metric-calls')
};
const timeLabel = document.getElementById('time-label');
const timeSlider = document.getElementById('time-slider');
const tooltip = document.getElementById('tooltip');
const autoPlayBtn = document.getElementById('auto-play-btn');
const generatedData = generateTimeSeriesData();
function generateTimeSeriesData() {
  const hours = 24;
  const data = [];
  const seed = 42;
  function pseudo(ix, s) {
    let h = ((ix * 31 + s * 17) ^ (seed * 7)) & 0x7fffffff;
    h = (h ^ (h >>> 13)) * 0x5bd1e995;
    h = h ^ (h >>> 15);
    return (h & 0xffff) / 0xffff;
  }
  for (let h = 0; h < hours; h++) {
    const grid = new Float32Array(GRID * GRID);
    const users = new Float32Array(GRID * GRID);
    const errors = new Float32Array(GRID * GRID);
    for (let z = 0; z < GRID; z++) {
      for (let x = 0; x < GRID; x++) {
        const cx = (x - GRID/2) / (GRID/4);
        const cz = (z - GRID/2) / (GRID/4);
        const t = h / 24;
        const hill1 = 2.5 * Math.exp(-(cx*cx + cz*cz) * 0.3) * (0.7 + 0.3 * Math.sin(t * Math.PI * 2));
        const hill2 = 1.8 * Math.exp(-((cx-3)*(cx-3) + (cz+2)*(cz+2)) * 0.2) * (0.5 + 0.5 * Math.cos(t * Math.PI * 2 + 1));
        const hill3 = 1.5 * Math.exp(-((cx+4)*(cx+4) + (cz-1)*(cz-1)) * 0.25) * (0.6 + 0.4 * Math.sin(t * Math.PI * 2 + 2.5));
        const ridge = 0.8 * Math.exp(-((cx-0.5)*(cx-0.5)) * 0.1) * (1 - Math.abs(cz) / 4) * (0.7 + 0.3 * Math.sin(t * Math.PI * 2 + 0.8));
        const noise = 0.3 * (pseudo(x + z * GRID, h) - 0.5);
        grid[z * GRID + x] = Math.max(0, hill1 + hill2 + hill3 + ridge + noise);
        users[z * GRID + x] = 0.3 + 0.7 * (hill1 + hill2 * 0.6) / 4.5 * (0.8 + 0.2 * pseudo(x * 7 + z * 13, h));
        const rawErr = 0.01 + 0.12 * pseudo(x * 3 + z * 5, h + 100);
        const spike = (Math.abs(cx - 1) < 0.4 && Math.abs(cz + 1.5) < 0.4) ? 0.15 * Math.sin(t * Math.PI * 4) : 0;
        errors[z * GRID + x] = Math.min(0.3, rawErr + Math.max(0, spike));
      }
    }
    const rivers = computeRiverPaths(errors, GRID);
    data.push({ grid, users, errors, rivers });
  }
  return data;
}
function computeRiverPaths(errors, N) {
  const paths = [];
  const visited = new Uint8Array(N * N);
  const highThreshold = 0.08;
  const seeds = [];
  for (let z = 0; z < N; z++) {
    for (let x = 0; x < N; x++) {
      if (errors[z * N + x] > highThreshold && !visited[z * N + x]) {
        seeds.push([x, z]);
        visited[z * N + x] = 1;
      }
    }
  }
  seeds.sort((a, b) => errors[b[1] * N + b[0]] - errors[a[1] * N + a[0]]);
  const dirs = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]];
  for (let s = 0; s < Math.min(seeds.length, RIVER_COUNT); s++) {
    let [cx, cz] = seeds[s];
    const path = [[cx, cz]];
    for (let step = 0; step < 60; step++) {
      let bestDir = null, bestErr = -1;
      for (const [dx, dz] of dirs) {
        const nx = cx + dx, nz = cz + dz;
        if (nx < 0 || nx >= N || nz < 0 || nz >= N) continue;
        if (visited[nz * N + nx]) continue;
        const e = errors[nz * N + nx];
        if (e > bestErr) { bestErr = e; bestDir = [dx, dz]; }
      }
      if (!bestDir || bestErr < 0.02) break;
      cx += bestDir[0]; cz += bestDir[1];
      visited[cz * N + cx] = 1;
      path.push([cx, cz]);
    }
    if (path.length > 4) paths.push(path);
  }
  return paths;
}
function initScene() {
  const container = document.getElementById('canvas-container');
  scene = new THREE.Scene();
  scene.background = new THREE.Color('#0a0a1a');
  scene.fog = new THREE.Fog('#0a0a1a', 20, 60);
  camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 80);
  camera.position.set(18, 14, 18);
  camera.lookAt(TERRAIN_W / 2, 0, TERRAIN_D / 2);
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  container.appendChild(renderer.domElement);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(TERRAIN_W / 2, 0, TERRAIN_D / 2);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.3;
  controls.minDistance = 5;
  controls.maxDistance = 35;
  controls.maxPolarAngle = Math.PI * 0.48;
  controls.update();
  const ambient = new THREE.AmbientLight('#334466', 1.8);
  scene.add(ambient);
  const sun = new THREE.DirectionalLight('#ffe8cc', 3.5);
  sun.position.set(20, 18, 10);
  sun.castShadow = true;
  sun.shadow.mapSize.width = 2048;
  sun.shadow.mapSize.height = 2048;
  sun.shadow.camera.near = 0.5;
  sun.shadow.camera.far = 80;
  sun.shadow.camera.left = -25;
  sun.shadow.camera.right = 25;
  sun.shadow.camera.top = 25;
  sun.shadow.camera.bottom = -25;
  sun.shadow.bias = -0.0002;
  scene.add(sun);
  const fill = new THREE.DirectionalLight('#8899cc', 0.8);
  fill.position.set(-10, 4, -8);
  scene.add(fill);
  const gridHelper = new THREE.PolarGridHelper(TERRAIN_W / 2 + 2, 32, 20, 64, '#222244', '#222244');
  gridHelper.position.set(TERRAIN_W / 2, -0.05, TERRAIN_D / 2);
  scene.add(gridHelper);
  buildTerrain(12);
  buildRivers(12);
  buildParticles(12);
}
function buildTerrain(tIdx) {
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.material.dispose();
    scene.remove(terrainMesh);
    terrainMesh = null;
  }
  const data = generatedData[tIdx];
  const geo = new THREE.BufferGeometry();
  const verts = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const indices = [];
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      const i = z * GRID + x;
      const h = data.grid[i] * HEIGHT_SCALE;
      verts[i * 3] = x * SPACING;
      verts[i * 3 + 1] = h;
      verts[i * 3 + 2] = z * SPACING;
      const u = data.users[i];
      const c = new THREE.Color();
      if (u < 0.4) c.setHSL(0.55, 0.6, 0.22 + u * 0.4);
      else if (u < 0.7) c.setHSL(0.45 - (u - 0.4) * 0.6, 0.7, 0.3 + u * 0.3);
      else c.setHSL(0.08, 0.8, 0.35 + (u - 0.7) * 0.5);
      colors[i * 3] = c.r;
      colors[i * 3 + 1] = c.g;
      colors[i * 3 + 2] = c.b;
    }
  }
  for (let z = 0; z < GRID - 1; z++) {
    for (let x = 0; x < GRID - 1; x++) {
      const a = z * GRID + x;
      const b = a + 1;
      const c = (z + 1) * GRID + x;
      const d = c + 1;
      indices.push(a, c, b);
      indices.push(b, c, d);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide
  });
  terrainMesh = new THREE.Mesh(geo, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
}
function buildRivers(tIdx) {
  if (riverGroup) {
    riverGroup.traverse(c => {
      if (c.geometry) c.geometry.dispose();
      if (c.material) c.material.dispose();
    });
    scene.remove(riverGroup);
    riverGroup = null;
  }
  riverGroup = new THREE.Group();
  const data = generatedData[tIdx];
  const mat = new THREE.MeshBasicMaterial({ color: '#ef5350', transparent: true, opacity: 0.7, depthWrite: false });
  for (const path of data.rivers) {
    if (path.length < 2) continue;
    const pts = [];
    for (const [x, z] of path) {
      const i = z * GRID + x;
      const h = data.grid[i] * HEIGHT_SCALE + 0.15;
      pts.push(new THREE.Vector3(x * SPACING, h, z * SPACING));
    }
    const curve = new THREE.CatmullRomCurve3(pts);
    const curvePts = curve.getPoints(path.length * 3);
    const tubeGeo = new THREE.TubeGeometry(curve, curvePts.length * 2, 0.08, 6, false);
    const tube = new THREE.Mesh(tubeGeo, mat);
    tube.renderOrder = 1;
    tube.material.depthTest = true;
    riverGroup.add(tube);
  }
  scene.add(riverGroup);
}
function buildParticles(tIdx) {
  if (particleSystem) {
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
    scene.remove(particleSystem);
    particleSystem = null;
  }
  const data = generatedData[tIdx];
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const pColors = new Float32Array(PARTICLE_COUNT * 3);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const px = Math.random() * TERRAIN_W;
    const pz = Math.random() * TERRAIN_D;
    const gx = Math.floor(px / SPACING);
    const gz = Math.floor(pz / SPACING);
    const gi = Math.min(gz, GRID - 1) * GRID + Math.min(gx, GRID - 1);
    const h = data.grid[gi] * HEIGHT_SCALE + 0.3 + Math.random() * 0.6;
    positions[i * 3] = px;
    positions[i * 3 + 1] = h;
    positions[i * 3 + 2] = pz;
    const hue = 0.55 + Math.random() * 0.08;
    const col = new THREE.Color().setHSL(hue, 0.8, 0.5 + Math.random() * 0.4);
    pColors[i * 3] = col.r;
    pColors[i * 3 + 1] = col.g;
    pColors[i * 3 + 2] = col.b;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(pColors, 3));
  const spriteTex = createGlowTexture();
  const mat = new THREE.PointsMaterial({
    size: 0.25,
    map: spriteTex,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.75
  });
  particleSystem = new THREE.Points(geo, mat);
  particleSystem.renderOrder = 2;
  scene.add(particleSystem);
}
function createGlowTexture() {
  const size = 64;
  const canvas = document.createElement('canvas');
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  const grad = ctx.createRadialGradient(size/2, size/2, 0, size/2, size/2, size/2);
  grad.addColorStop(0, 'rgba(255,255,255,1)');
  grad.addColorStop(0.15, 'rgba(200,230,255,0.8)');
  grad.addColorStop(0.4, 'rgba(100,180,255,0.3)');
  grad.addColorStop(0.7, 'rgba(30,80,200,0.05)');
  grad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, size, size);
  return new THREE.CanvasTexture(canvas);
}
function updateTerrain(tIdx) {
  const data = generatedData[tIdx];
  if (!terrainMesh) { buildTerrain(tIdx); return; }
  const geo = terrainMesh.geometry;
  const posArr = geo.attributes.position.array;
  const colArr = geo.attributes.color.array;
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      const i = z * GRID + x;
      const h = data.grid[i] * HEIGHT_SCALE;
      posArr[i * 3 + 1] = h;
      const u = data.users[i];
      const c = new THREE.Color();
      if (u < 0.4) c.setHSL(0.55, 0.6, 0.22 + u * 0.4);
      else if (u < 0.7) c.setHSL(0.45 - (u - 0.4) * 0.6, 0.7, 0.3 + u * 0.3);
      else c.setHSL(0.08, 0.8, 0.35 + (u - 0.7) * 0.5);
      colArr[i * 3] = c.r;
      colArr[i * 3 + 1] = c.g;
      colArr[i * 3 + 2] = c.b;
    }
  }
  geo.attributes.position.needsUpdate = true;
  geo.attributes.color.needsUpdate = true;
  geo.computeVertexNormals();
  buildRivers(tIdx);
  buildParticles(tIdx);
  updateMetrics(tIdx);
}
function updateMetrics(tIdx) {
  const data = generatedData[tIdx];
  let sumRev = 0, sumUsers = 0, sumErr = 0, maxCalls = 0;
  for (let i = 0; i < GRID * GRID; i++) {
    sumRev += data.grid[i];
    sumUsers += data.users[i];
    sumErr += data.errors[i];
  }
  const n = GRID * GRID;
  const avgRev = sumRev / n;
  const avgUsers = sumUsers / n;
  const avgErr = sumErr / n;
  maxCalls = Math.round(30 + avgRev * 60 + avgUsers * 40);
  statsEl.revenue.textContent = '$' + (avgRev * 18000 + 5000).toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  statsEl.users.textContent = Math.round(avgUsers * 25000 + 2000).toLocaleString();
  statsEl.errors.textContent = (avgErr * 100).toFixed(2) + '%';
  statsEl.calls.textContent = maxCalls;
}
function setTimeIndex(idx) {
  timeIndex = ((idx % 24) + 24) % 24;
  timeSlider.value = timeIndex;
  const h = timeIndex;
  timeLabel.textContent = String(h).padStart(2, '0') + ':00';
  updateTerrain(timeIndex);
}
function goToBookmark(name) {
  let bm;
  if (name === 'save') {
    bm = {
      pos: [camera.position.x, camera.position.y, camera.position.z],
      target: [controls.target.x, controls.target.y, controls.target.z]
    };
    savedBookmark = bm;
    document.querySelector('[data-bookmark="save"]').textContent = 'Saved ✓';
    setTimeout(() => {
      const btn = document.querySelector('[data-bookmark="save"]');
      if (btn) btn.textContent = 'Save Current';
    }, 1200);
    return;
  }
  bm = savedBookmark && name === 'saved' ? savedBookmark : bookmarks[name];
  if (!bm) return;
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function anim(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(anim);
    }
  }
  requestAnimationFrame(anim);
}
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  if (particleSystem) {
    const posArr = particleSystem.geometry.attributes.position.array;
    const data = generatedData[timeIndex];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      let px = posArr[i * 3] + (Math.sin(dt * 3 + i * 0.7) * 0.06);
      let pz = posArr[i * 3 + 2] + (Math.cos(dt * 3.5 + i * 0.9) * 0.06);
      if (px < 0) px += TERRAIN_W;
      if (px > TERRAIN_W) px -= TERRAIN_W;
      if (pz < 0) pz += TERRAIN_D;
      if (pz > TERRAIN_D) pz -= TERRAIN_D;
      const gx = Math.min(Math.max(Math.floor(px / SPACING), 0), GRID - 1);
      const gz = Math.min(Math.max(Math.floor(pz / SPACING), 0), GRID - 1);
      const gi = gz * GRID + gx;
      posArr[i * 3] = px;
      posArr[i * 3 + 1] = data.grid[gi] * HEIGHT_SCALE + 0.35 + Math.sin(dt * 5 + i) * 0.15;
      posArr[i * 3 + 2] = pz;
    }
    particleSystem.geometry.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
}
function onMouseMove(e) {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!terrainMesh) return;
  const hits = raycaster.intersectObject(terrainMesh);
  if (hits.length > 0) {
    const p = hits[0].point;
    const gx = Math.round(p.x / SPACING);
    const gz = Math.round(p.z / SPACING);
    if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
      const data = generatedData[timeIndex];
      const i = gz * GRID + gx;
      const rev = (data.grid[i] * 18000 + 5000).toFixed(0);
      const users = Math.round(data.users[i] * 25000 + 2000);
      const err = (data.errors[i] * 100).toFixed(2);
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 16) + 'px';
      tooltip.style.top = (e.clientY - 10) + 'px';
      tooltip.innerHTML = `Revenue: $${rev}<br>Users: ${users}<br>Error rate: ${err}%`;
      return;
    }
  }
  tooltip.style.display = 'none';
}
function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
function onKeyDown(e) {
  switch(e.key.toLowerCase()) {
    case 'r': controls.autoRotate = !controls.autoRotate; break;
    case 'f': goToBookmark('overview'); break;
    case '1': goToBookmark('overview'); break;
    case '2': goToBookmark('north'); break;
    case '3': goToBookmark('valley'); break;
    case '4': goToBookmark('topdown'); break;
    case ' ': e.preventDefault(); toggleAutoPlay(); break;
    case 'arrowleft': setTimeIndex(timeIndex - 1); break;
    case 'arrowright': setTimeIndex(timeIndex + 1); break;
  }
}
function toggleAutoPlay() {
  autoPlaying = !autoPlaying;
  autoPlayBtn.textContent = autoPlaying ? '⏸ Pause' : '▶ Play';
  if (autoPlaying) {
    autoPlayDir = 1;
    autoPlayTimer = setInterval(() => {
      let next = timeIndex + autoPlayDir;
      if (next >= 23) { autoPlayDir = -1; next = 22; }
      if (next <= 0) { autoPlayDir = 1; next = 1; }
      setTimeIndex(next);
    }, 600);
  } else {
    clearInterval(autoPlayTimer);
    autoPlayTimer = null;
  }
}
timeSlider.addEventListener('input', () => {
  if (autoPlaying) toggleAutoPlay();
  setTimeIndex(parseInt(timeSlider.value));
});
autoPlayBtn.addEventListener('click', toggleAutoPlay);
document.getElementById('bookmark-panel').addEventListener('click', (e) => {
  const btn = e.target.closest('.bookmark-btn');
  if (!btn) return;
  goToBookmark(btn.dataset.bookmark);
});
window.addEventListener('mousemove', onMouseMove, { passive: true });
window.addEventListener('resize', onWindowResize);
window.addEventListener('keydown', onKeyDown);
initScene();
updateMetrics(12);
animate();
</script>
</body>
</html>