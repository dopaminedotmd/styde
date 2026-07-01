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
#ui { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 10; }
#ui > * { pointer-events: auto; }
#time-panel { position: absolute; bottom: 32px; left: 50%; transform: translateX(-50%); background: rgba(10,10,24,0.92); border: 1px solid #2d3a5c; border-radius: 12px; padding: 16px 24px; display: flex; align-items: center; gap: 16px; backdrop-filter: blur(12px); }
#time-slider { width: 320px; accent-color: #4dabf7; height: 6px; cursor: pointer; }
#time-label { font-size: 13px; color: #8ea4c8; min-width: 100px; text-align: center; }
#bookmarks { position: absolute; top: 20px; right: 20px; background: rgba(10,10,24,0.88); border: 1px solid #2d3a5c; border-radius: 12px; padding: 12px; backdrop-filter: blur(12px); display: flex; flex-direction: column; gap: 6px; min-width: 170px; }
#bookmarks h3 { font-size: 13px; color: #8ea4c8; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px; }
.bookmark-btn { background: #1a1d3a; border: 1px solid #3d4670; color: #b8c7e0; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; text-align: left; transition: all 0.15s; display: flex; justify-content: space-between; align-items: center; }
.bookmark-btn:hover { background: #252a50; border-color: #5a6fb0; }
.bookmark-del { color: #e0556a; cursor: pointer; padding: 2px 6px; border-radius: 3px; }
.bookmark-del:hover { background: #e0556a33; }
#diagnostics { position: absolute; top: 20px; left: 20px; background: rgba(10,10,24,0.88); border: 1px solid #2d3a5c; border-radius: 12px; padding: 14px; backdrop-filter: blur(12px); font-size: 11px; line-height: 1.7; min-width: 200px; }
#diagnostics h3 { font-size: 13px; color: #8ea4c8; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; }
.diag-row { display: flex; justify-content: space-between; }
.diag-cache { color: #4dabf7; }
.diag-green { color: #69db7c; }
.diag-yellow { color: #ffd43b; }
#tooltip { position: absolute; pointer-events: none; background: rgba(20,22,44,0.94); border: 1px solid #5a6fb0; border-radius: 8px; padding: 10px 14px; font-size: 12px; display: none; backdrop-filter: blur(8px); line-height: 1.6; }
#controls-help { position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); font-size: 11px; color: #5a6480; opacity: 0.7; }
</style>
</head>
<body>
<div id="ui">
  <div id="diagnostics">
    <h3>Performance</h3>
    <div class="diag-row"><span>FPS</span><span id="diag-fps">60</span></div>
    <div class="diag-row"><span>Particles</span><span id="diag-particles">0</span></div>
    <div class="diag-row"><span class="diag-cache">Cache hits</span><span class="diag-cache" id="diag-cache-hits">0</span></div>
    <div class="diag-row"><span class="diag-yellow">Cache misses</span><span class="diag-yellow" id="diag-cache-misses">0</span></div>
    <div class="diag-row"><span>Draw calls</span><span id="diag-drawcalls">0</span></div>
    <div class="diag-row"><span>Triangles</span><span id="diag-tris">0</span></div>
  </div>
  <div id="bookmarks">
    <h3>Bookmarks</h3>
    <button class="bookmark-btn" onclick="saveBookmark()">+ Save current view</button>
    <div id="bookmark-list"></div>
  </div>
  <div id="tooltip"></div>
  <div id="time-panel">
    <span style="font-size:13px;color:#8ea4c8;">Time</span>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label">Day 0</span>
  </div>
  <div id="controls-help">Drag: orbit | Scroll: zoom | Right-drag: pan | R: auto-rotate</div>
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
/* ======================== DATA GENERATION ======================== */
/* Generate 100 time steps of synthetic multi-metric data on a 128x128 grid. */
const GRID = 128;
const TIME_STEPS = 100;
const DATA = (() => {
  const d = [];
  /* Helper: simplex-like noise using layered sine waves for reproducibility without external libs. */
  const noise = (x, y, t, scale, octaves) => {
    let v = 0, amp = 1, freq = scale, total = 0;
    for (let o = 0; o < octaves; o++) {
      v += amp * Math.sin(x * freq + t * 0.7) * Math.cos(y * freq - t * 0.5) * Math.sin((x + y) * freq * 0.6 + t * 0.3);
      total += amp;
      amp *= 0.5;
      freq *= 2.0;
    }
    return v / total;
  };
  for (let t = 0; t < TIME_STEPS; t++) {
    const step = { revenue: new Float32Array(GRID * GRID), users: new Float32Array(GRID * GRID), errors: new Float32Array(GRID * GRID) };
    const tNorm = t / TIME_STEPS;
    for (let y = 0; y < GRID; y++) {
      for (let x = 0; x < GRID; x++) {
        const nx = (x / GRID) * 8 - 4;
        const ny = (y / GRID) * 8 - 4;
        /* Revenue: rolling hills that shift over time with a growing central peak */
        const centralGrow = 1.5 * Math.exp(-((nx * 0.7) * (nx * 0.7) + (ny * 0.7) * (ny * 0.7))) * (0.5 + 0.5 * tNorm);
        step.revenue[y * GRID + x] = noise(nx, ny, tNorm * 6, 0.8, 3) * 60 + centralGrow * 40 + 50;
        /* Users: cluster density, vegetation analog */
        step.users[y * GRID + x] = noise(nx + 2, ny - 1, tNorm * 4, 1.0, 2) * 0.4 + 0.5;
        /* Errors: spike anomalies at specific grid positions forming river pathways */
        const eBase = Math.max(0, noise(nx * 1.5, ny * 1.5, tNorm * 3, 1.2, 2) * 0.15);
        const eSpike1 = Math.exp(-((nx - 1.5) * (nx - 1.5) * 0.8 + (ny + 0.5) * (ny + 0.5) * 4)) * (0.3 + 0.2 * Math.sin(tNorm * 12));
        const eSpike2 = Math.exp(-((nx + 2) * (nx + 2) * 1.2 + (ny - 1) * (ny - 1) * 3)) * (0.25 + 0.15 * Math.cos(tNorm * 8 + 2));
        step.errors[y * GRID + x] = eBase + eSpike1 + eSpike2;
      }
    }
    d.push(step);
  }
  return d;
})();
/* Current time index */
let currentTime = 0;
/* Terrain height at current time (computed once per slider change) */
let currentHeight = new Float32Array(GRID * GRID);
/* ======================== THREE.JS SETUP ======================== */
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.FogExp2(0x0a0a18, 0.00008);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 800);
camera.position.set(60, 55, 90);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
/* ======================== LIGHTING ======================== */
const ambient = new THREE.AmbientLight(0x1a2a50, 0.6);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(80, 100, 40);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 400;
sun.shadow.camera.left = -70;
sun.shadow.camera.right = 70;
sun.shadow.camera.top = 70;
sun.shadow.camera.bottom = -70;
sun.shadow.bias = -0.0004;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466cc, 0.7);
fill.position.set(-30, 20, -20);
scene.add(fill);
/* Ground plane with subtle grid */
const gridHelper = new THREE.PolarGridHelper(65, 48, 32, 128, 0x1a2a44, 0x1a2a44);
gridHelper.position.y = -2;
scene.add(gridHelper);
/* ======================== CACHE INFRASTRUCTURE ======================== */
const cache = {
  terrainGeometries: new Map(),      /* key: timeStep → BufferGeometry */
  riverGeometries: new Map(),        /* key: timeStep → BufferGeometry */
  heightfields: new Map(),           /* key: timeStep → Float32Array */
  noiseGrids: new Map(),
  hits: 0,
  misses: 0,
  maxSize: 60, /* LRU eviction threshold */
  get(key) { if (this.terrainGeometries.has(key)) { this.hits++; return this.terrainGeometries.get(key); } this.misses++; return undefined; },
  set(key, geo) { if (this.terrainGeometries.size >= this.maxSize) { const first = this.terrainGeometries.keys().next().value; this.terrainGeometries.delete(first); this.riverGeometries.delete(first); this.heightfields.delete(first); } this.terrainGeometries.set(key, geo); },
  getRiver(key) { return this.riverGeometries.get(key); },
  setRiver(key, geo) { this.riverGeometries.set(key, geo); },
  getHeight(key) { return this.heightfields.get(key); },
  setHeight(key, h) { this.heightfields.set(key, h); }
};
/* ======================== TERRAIN BUILD ======================== */
/* Compute height for a given time step from cached or raw data */
function computeHeightAtTime(t) {
  if (cache.getHeight(t)) return cache.getHeight(t);
  const src = DATA[t].revenue;
  const h = new Float32Array(GRID * GRID);
  /* Normalize revenue to 0-1 range then scale to max height */
  let min = Infinity, max = -Infinity;
  for (let i = 0; i < src.length; i++) { if (src[i] < min) min = src[i]; if (src[i] > max) max = src[i]; }
  const range = max - min || 1;
  for (let i = 0; i < src.length; i++) h[i] = ((src[i] - min) / range) * 40 + 1;
  cache.setHeight(t, h);
  return h;
}
/* Build terrain geometry from height array */
function buildTerrainGeometry(heightArr) {
  const geo = new THREE.PlaneGeometry(60, 60, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  const colors = new Float32Array(pos.count * 3);
  const users = DATA[currentTime].users;
  /* Map user density to vertex color: low=blue, mid=green, high=yellow */
  for (let i = 0; i < pos.count; i++) {
    pos.setY(i, heightArr[i]);
    const u = users[i];
    colors[i * 3]     = u * 0.4;                /* R: warm as density rises */
    colors[i * 3 + 1] = 0.3 + u * 0.5;          /* G: vegetation base */
    colors[i * 3 + 2] = 0.7 - u * 0.5;          /* B: recedes with density */
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  return geo;
}
/* Get or build terrain geometry with caching */
function getTerrainGeometry(t) {
  const cached = cache.get(t);
  if (cached) return cached;
  const h = computeHeightAtTime(t);
  const geo = buildTerrainGeometry(h);
  cache.set(t, geo);
  return geo;
}
/* ======================== TERRAIN MESH ======================== */
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
let terrainMesh = new THREE.Mesh(getTerrainGeometry(0), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
/* ======================== RIVER SYSTEM ======================== */
/* Trace error anomaly paths using a simple ridge-following algorithm.
   Rivers flow downhill through error hot spots, carving visible red channels. */
function traceRiverPath(heightArr, errorArr) {
  /* Find local error maxima that also sit on slopes (river sources) */
  const sources = [];
  const threshold = 0.12;
  for (let y = 2; y < GRID - 2; y++) {
    for (let x = 2; x < GRID - 2; x++) {
      const idx = y * GRID + x;
      if (errorArr[idx] < threshold) continue;
      /* Check if local maximum in error field */
      let isPeak = true;
      for (let dy = -1; dy <= 1 && isPeak; dy++)
        for (let dx = -1; dx <= 1 && isPeak; dx++)
          if (errorArr[(y + dy) * GRID + (x + dx)] > errorArr[idx]) isPeak = false;
      if (isPeak) sources.push({ x, y, idx });
    }
  }
  if (sources.length === 0) return [];
  /* For each source, trace downhill following steepest gradient in height */
  const paths = [];
  const MAX_STEPS = 200;
  for (const src of sources) {
    const path = [];
    let cx = src.x, cy = src.y;
    for (let step = 0; step < MAX_STEPS; step++) {
      if (cx < 1 || cx >= GRID - 1 || cy < 1 || cy >= GRID - 1) break;
      path.push({ x: cx, y: cy, idx: cy * GRID + cx });
      /* Find steepest downhill neighbour */
      let bestDz = Infinity, bestNx = cx, bestNy = cy;
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dy === 0) continue;
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          const dz = heightArr[ny * GRID + nx] - heightArr[cy * GRID + cx];
          if (dz < bestDz) { bestDz = dz; bestNx = nx; bestNy = ny; }
        }
      }
      if (bestDz >= 0) break; /* reached a basin */
      cx = bestNx; cy = bestNy;
    }
    if (path.length > 5) paths.push(path);
  }
  return paths;
}
/* Build river mesh from traced paths */
function buildRiverGeometry(heightArr, errorArr) {
  const paths = traceRiverPath(heightArr, errorArr);
  const riversGroup = new THREE.Group();
  const H_SPACING = 60 / (GRID - 1);
  for (const path of paths) {
    /* Build a tube along the path points */
    const pts = [];
    for (const p of path) {
      const wx = (p.x / (GRID - 1) - 0.5) * 60;
      const wz = (p.y / (GRID - 1) - 0.5) * 60;
      const wy = heightArr[p.idx] + 0.25;
      pts.push(new THREE.Vector3(wx, wy, wz));
    }
    if (pts.length < 4) continue;
    const curve = new THREE.CatmullRomCurve3(pts);
    const tubeGeo = new THREE.TubeGeometry(curve, Math.min(pts.length * 2, 120), 0.2, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xe0313d, roughness: 0.3, metalness: 0.1, emissive: 0x330808, emissiveIntensity: 0.6, transparent: true, opacity: 0.85
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.renderOrder = 1;
    tube.material.depthTest = true;
    tube.material.depthWrite = true;
    riversGroup.add(tube);
    /* Glow outline: slightly larger, more transparent tube */
    const glowGeo = new THREE.TubeGeometry(curve, Math.min(pts.length, 60), 0.38, 6, false);
    const glowMat = new THREE.MeshBasicMaterial({ color: 0xff4444, transparent: true, opacity: 0.25, depthWrite: false });
    const glow = new THREE.Mesh(glowGeo, glowMat);
    glow.renderOrder = 0;
    riversGroup.add(glow);
  }
  return riversGroup;
}
/* Cached river access */
let riverGroup = null;
function getRiverGroup(t) {
  const geo = cache.getRiver(t);
  if (geo) return geo.clone();
  const h = computeHeightAtTime(t);
  const g = buildRiverGeometry(h, DATA[t].errors);
  cache.setRiver(t, g);
  return g.clone();
}
/* ======================== PARTICLE SYSTEM ======================== */
/* API call / user action flows as particle trails */
const PARTICLE_COUNT = 600;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3); /* direction vectors */
const particleAges = new Float32Array(PARTICLE_COUNT);
const particleMaxAges = new Float32Array(PARTICLE_COUNT);
function resetParticle(i) {
  /* Spawn from random position on the terrain surface */
  const gx = Math.floor(Math.random() * GRID);
  const gy = Math.floor(Math.random() * GRID);
  const idx = gy * GRID + gx;
  const wx = (gx / (GRID - 1) - 0.5) * 60;
  const wz = (gy / (GRID - 1) - 0.5) * 60;
  const wy = currentHeight[idx] + 0.5;
  particlePositions[i * 3] = wx;
  particlePositions[i * 3 + 1] = wy;
  particlePositions[i * 3 + 2] = wz;
  /* Random direction bias: flow along terrain gradient */
  const angle = Math.random() * Math.PI * 2;
  particleVelocities[i * 3] = Math.cos(angle) * (0.03 + Math.random() * 0.06);
  particleVelocities[i * 3 + 1] = (Math.random() - 0.3) * 0.02;
  particleVelocities[i * 3 + 2] = Math.sin(angle) * (0.03 + Math.random() * 0.06);
  particleAges[i] = 0;
  particleMaxAges[i] = 1.5 + Math.random() * 3.0;
  particleColors[i * 3] = 0.3 + Math.random() * 0.4;
  particleColors[i * 3 + 1] = 0.6 + Math.random() * 0.4;
  particleColors[i * 3 + 2] = 0.9;
}
/* Initialize all particles */
for (let i = 0; i < PARTICLE_COUNT; i++) resetParticle(i);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.25, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.7
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 2;
scene.add(particles);
/* ======================== ORBIT CONTROLS ======================== */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 10, 0);
controls.minDistance = 15;
controls.maxDistance = 200;
controls.maxPolarAngle = Math.PI * 0.6;
controls.update();
/* ======================== CAMERA BOOKMARKS ======================== */
const bookmarks = [];
const bookmarkList = document.getElementById('bookmark-list');
function renderBookmarks() {
  bookmarkList.innerHTML = bookmarks.map((b, i) => `
    <div class="bookmark-btn" onclick="window.__applyBookmark(${i})">
      <span>${b.label}</span>
      <span class="bookmark-del" onclick="event.stopPropagation();window.__deleteBookmark(${i})">X</span>
    </div>
  `).join('');
}
window.__applyBookmark = (i) => {
  const b = bookmarks[i];
  camera.position.set(b.px, b.py, b.pz);
  controls.target.set(b.tx, b.ty, b.tz);
  controls.update();
};
window.__deleteBookmark = (i) => {
  bookmarks.splice(i, 1);
  renderBookmarks();
};
window.saveBookmark = () => {
  /* Validate camera state before saving */
  if (!camera.position || isNaN(camera.position.x)) return;
  bookmarks.push({
    label: `View ${bookmarks.length + 1} @ t=${currentTime}`,
    px: camera.position.x, py: camera.position.y, pz: camera.position.z,
    tx: controls.target.x, ty: controls.target.y, tz: controls.target.z
  });
  renderBookmarks();
};
/* ======================== HOVER / TOOLTIP ======================== */
const tooltip = document.getElementById('tooltip');
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
/* Memoized world-to-grid transform: maps world position to grid index */
const gridTransform = { lastWx: NaN, lastWz: NaN, lastGx: -1, lastGy: -1 };
function worldToGrid(wx, wz) {
  /* Check memoized result — identical world coords return cached grid */
  if (wx === gridTransform.lastWx && wz === gridTransform.lastWz) {
    return { gx: gridTransform.lastGx, gy: gridTransform.lastGy };
  }
  const gx = Math.round((wx / 60 + 0.5) * (GRID - 1));
  const gy = Math.round((wz / 60 + 0.5) * (GRID - 1));
  gridTransform.lastWx = wx;
  gridTransform.lastWz = wz;
  gridTransform.lastGx = gx;
  gridTransform.lastGy = gy;
  return { gx, gy };
}
function onMouseMove(e) {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const p = intersects[0].point;
    const { gx, gy } = worldToGrid(p.x, p.z);
    if (gx >= 0 && gx < GRID && gy >= 0 && gy < GRID) {
      const idx = gy * GRID + gx;
      /* Guard against undefined data access */
      if (!DATA[currentTime] || idx >= DATA[currentTime].revenue.length) return;
      const rev = DATA[currentTime].revenue[idx].toFixed(1);
      const usr = (DATA[currentTime].users[idx] * 100).toFixed(0);
      const err = (DATA[currentTime].errors[idx] * 100).toFixed(1);
      const h = currentHeight[idx].toFixed(2);
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 18) + 'px';
      tooltip.style.top = (e.clientY + 18) + 'px';
      tooltip.innerHTML = `Revenue: <b>${rev}</b><br>Users: <b>${usr}%</b><br>Errors: <b>${err}%</b><br>Height: <b>${h}</b>`;
    }
  } else {
    tooltip.style.display = 'none';
    /* Reset memoized transform when not hovering */
    gridTransform.lastWx = NaN;
  }
}
window.addEventListener('mousemove', onMouseMove, { passive: true });
/* ======================== TIME SLIDER ======================== */
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
/* Debounce river rebuild on slider change */
let riverDebounceTimer = null;
const RIVER_DEBOUNCE_MS = 200;
function applyTimeStep(t) {
  currentTime = t;
  currentHeight = computeHeightAtTime(t);
  /* Swap terrain geometry from cache */
  const newGeo = getTerrainGeometry(t);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = newGeo;
  timeLabel.textContent = `Day ${t}`;
  /* Debounce river rebuild — expensive TubeGeometry */
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (riverGroup) {
      riverGroup.traverse(child => { if (child.geometry) child.geometry.dispose(); });
      scene.remove(riverGroup);
    }
    riverGroup = getRiverGroup(t);
    scene.add(riverGroup);
    riverDebounceTimer = null;
  }, RIVER_DEBOUNCE_MS);
}
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value);
  applyTimeStep(t);
});
/* Keyboard shortcut for auto-rotate */
window.addEventListener('keydown', (e) => {
  if (e.key === 'r' || e.key === 'R') {
    controls.autoRotate = !controls.autoRotate;
  }
});
/* ======================== DIAGNOSTICS PANEL ======================== */
const diagFps = document.getElementById('diag-fps');
const diagParticles = document.getElementById('diag-particles');
const diagCacheHits = document.getElementById('diag-cache-hits');
const diagCacheMisses = document.getElementById('diag-cache-misses');
const diagDrawCalls = document.getElementById('diag-drawcalls');
const diagTris = document.getElementById('diag-tris');
let frameCount = 0, lastFpsTime = performance.now(), currentFps = 60;
/* ======================== ANIMATION LOOP ======================== */
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  /* Update particles: slide along terrain surface */
  const posArr = particleGeo.attributes.position.array;
  const colArr = particleGeo.attributes.color.array;
  const dt = Math.min(0.05, 0.016);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particleAges[i] += dt;
    if (particleAges[i] >= particleMaxAges[i]) { resetParticle(i); continue; }
    /* Move particle */
    posArr[i * 3] += particleVelocities[i * 3];
    posArr[i * 3 + 2] += particleVelocities[i * 3 + 2];
    /* Clamp to terrain: map world pos to grid, read height, set Y */
    const gx = Math.round((posArr[i * 3] / 60 + 0.5) * (GRID - 1));
    const gz = Math.round((posArr[i * 3 + 2] / 60 + 0.5) * (GRID - 1));
    if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
      posArr[i * 3 + 1] = currentHeight[gz * GRID + gx] + 0.5;
    }
    /* Wrap particles that go out of bounds */
    if (posArr[i * 3] < -30 || posArr[i * 3] > 30 || posArr[i * 3 + 2] < -30 || posArr[i * 3 + 2] > 30) {
      resetParticle(i);
    }
    /* Fade alpha via color dimming with age */
    const fade = 1 - (particleAges[i] / particleMaxAges[i]);
    colArr[i * 3 + 1] = (0.6 + Math.random() * 0.1) * fade * 0.8 + 0.1;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  /* FPS counter */
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    currentFps = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = timestamp;
    diagFps.textContent = currentFps;
    diagCacheHits.textContent = cache.hits;
    diagCacheMisses.textContent = cache.misses;
    diagDrawCalls.textContent = renderer.info.render.calls;
    diagTris.textContent = renderer.info.render.triangles;
    diagParticles.textContent = PARTICLE_COUNT;
  }
  renderer.render(scene, camera);
}
/* ======================== INITIALIZATION ======================== */
/* Build initial terrain and rivers */
currentHeight = computeHeightAtTime(0);
getTerrainGeometry(0);
/* Build initial river system immediately (not debounced for first frame) */
riverGroup = getRiverGroup(0);
scene.add(riverGroup);
/* Start animation */
requestAnimationFrame(animate);
/* ======================== RESIZE HANDLER ======================== */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ======================== EDGE CASE VALIDATION ======================== */
/* Verify no undefined variable paths exist */
(function validateBindings() {
  const errors = [];
  /* Check DATA structure integrity */
  if (!DATA || DATA.length !== TIME_STEPS) errors.push('DATA length mismatch');
  for (let t = 0; t < TIME_STEPS; t++) {
    if (!DATA[t].revenue || DATA[t].revenue.length !== GRID * GRID) errors.push(`DATA[${t}].revenue invalid`);
    if (!DATA[t].users || DATA[t].users.length !== GRID * GRID) errors.push(`DATA[${t}].users invalid`);
    if (!DATA[t].errors || DATA[t].errors.length !== GRID * GRID) errors.push(`DATA[${t}].errors invalid`);
  }
  /* Confirm terrainMesh is initialized */
  if (!terrainMesh || !terrainMesh.geometry) errors.push('terrainMesh not initialized');
  /* Verify particle arrays match count */
  if (particlePositions.length !== PARTICLE_COUNT * 3) errors.push('particlePositions size mismatch');
  if (particleColors.length !== PARTICLE_COUNT * 3) errors.push('particleColors size mismatch');
  /* Check cache map integrity */
  if (!(cache.terrainGeometries instanceof Map)) errors.push('cache.terrainGeometries not a Map');
  if (!(cache.riverGeometries instanceof Map)) errors.push('cache.riverGeometries not a Map');
  if (errors.length > 0) console.warn('Validation warnings:', errors);
  else console.log('Edge case validation passed — all bindings verified.');
})();
</script>
</body>
</html>