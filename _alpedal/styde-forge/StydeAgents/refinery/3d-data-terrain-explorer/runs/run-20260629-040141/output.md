<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: #12122a;
    --text: #c8c8e0;
    --accent: #4da6ff;
    --accent2: #ff6b6b;
    --border: #1e1e3a;
    --slider-track: #2a2a4a;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Segoe UI', system-ui, sans-serif;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 1;
  }
  canvas { display: block; }
  #hud {
    position: fixed;
    z-index: 10;
    pointer-events: none;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  #hud > * { pointer-events: auto; }
  #top-bar {
    top: 12px;
    left: 12px;
    right: 12px;
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }
  #bottom-bar {
    bottom: 12px;
    left: 12px;
    right: 12px;
  }
  .panel {
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    backdrop-filter: blur(8px);
  }
  #legend {
    max-width: 220px;
    font-size: 12px;
    line-height: 1.5;
  }
  #legend h3 { color: var(--accent); margin-bottom: 6px; font-size: 14px; }
  .legend-item { display: flex; align-items: center; gap: 6px; margin: 3px 0; }
  .legend-swatch { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
  #bookmarks-panel { max-width: 200px; }
  #bookmarks-panel h3 { color: var(--accent); margin-bottom: 6px; font-size: 14px; }
  #bookmark-list { display: flex; flex-direction: column; gap: 4px; max-height: 160px; overflow-y: auto; }
  .bookmark-btn {
    background: var(--slider-track);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 4px 8px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 11px;
    text-align: left;
    display: flex;
    justify-content: space-between;
  }
  .bookmark-btn:hover { background: #3a3a5a; }
  .bookmark-del { color: var(--accent2); margin-left: 6px; cursor: pointer; }
  #time-panel {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }
  #time-slider {
    flex: 1;
    min-width: 120px;
    accent-color: var(--accent);
    height: 6px;
  }
  #time-label { font-size: 13px; white-space: nowrap; min-width: 90px; }
  #auto-rotate-btn {
    background: var(--slider-track);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
  }
  #auto-rotate-btn.active { background: var(--accent); color: #000; }
  #save-bookmark-btn {
    background: var(--accent);
    border: none;
    color: #000;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 600;
  }
  #import-btn {
    background: var(--slider-track);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
  }
  #tooltip {
    position: fixed;
    pointer-events: none;
    z-index: 20;
    background: rgba(10,10,30,0.92);
    border: 1px solid var(--accent);
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    line-height: 1.4;
    display: none;
    white-space: nowrap;
  }
  #file-input { display: none; }
  @media (max-width: 768px) {
    #legend { display: none; }
    #bookmarks-panel { max-width: 140px; font-size: 10px; }
    #time-panel { gap: 6px; }
    #time-label { font-size: 11px; min-width: 70px; }
    #top-bar { flex-wrap: wrap; gap: 6px; }
  }
  @media (max-width: 480px) {
    #bookmarks-panel { display: none; }
    #time-panel { width: 100%; }
    #save-bookmark-btn { font-size: 10px; padding: 4px 8px; }
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hud" id="top-bar" style="top:12px;left:12px;right:12px;flex-direction:row;justify-content:space-between;align-items:flex-start;">
  <div class="panel" id="legend">
    <h3>Terrain Legend</h3>
    <div class="legend-item"><span class="legend-swatch" style="background:#4da6ff;"></span> Elevation = Revenue</div>
    <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(135deg,#1a5c1a,#7cfc00);"></span> Green = User Density</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#ff4444;"></span> Red Rivers = Errors</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#ffdd44;"></span> Gold Trails = API Calls</div>
  </div>
  <div style="display:flex;flex-direction:column;gap:8px;">
    <div class="panel" id="bookmarks-panel">
      <h3>Bookmarks</h3>
      <div id="bookmark-list"></div>
      <button id="save-bookmark-btn" style="margin-top:6px;width:100%;">Save View</button>
    </div>
    <button id="import-btn" class="panel" style="width:100%;">Import Data (JSON/CSV)</button>
    <input type="file" id="file-input" accept=".json,.csv">
  </div>
</div>
<div id="hud" id="bottom-bar" style="bottom:12px;left:12px;right:12px;">
  <div class="panel" id="time-panel">
    <span id="time-label">T0 / 12</span>
    <input type="range" id="time-slider" min="0" max="11" value="0" step="1">
    <button id="auto-rotate-btn">Auto-Rotate: Off</button>
  </div>
</div>
<div id="tooltip"></div>
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
const GRID = 60;
const TERRAIN_SIZE = 20;
const TIME_POINTS = 12;
const container = document.getElementById('canvas-container');
const tooltip = document.getElementById('tooltip');
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const autoRotateBtn = document.getElementById('auto-rotate-btn');
const saveBookmarkBtn = document.getElementById('save-bookmark-btn');
const bookmarkList = document.getElementById('bookmark-list');
const importBtn = document.getElementById('import-btn');
const fileInput = document.getElementById('file-input');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 25, 60);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 100);
camera.position.set(16, 12, 18);
camera.lookAt(0, 2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 2, 0);
controls.minDistance = 5;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.7;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 2.5);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466aa, 1.5);
fillLight.position.set(-8, 2, -6);
scene.add(fillLight);
const raycaster = new THREE.Raycaster();
raycaster.params.Points.threshold = 0.3;
raycaster.params.Line.threshold = 0.3;
const mouse = new THREE.Vector2();
let terrainMesh = null;
let riverLines = [];
let particleSystem = null;
let timeSeriesData = null;
let currentTimeIndex = 0;
let bookmarks = [];
let autoRotate = false;
let cachedGeometries = new Map();
function simplex2D(x, y) {
  const F2 = 0.5 * (Math.sqrt(3) - 1);
  const G2 = (3 - Math.sqrt(3)) / 6;
  const floor = Math.floor;
  const s = (x + y) * F2;
  const i = floor(x + s);
  const j = floor(y + s);
  const t = (i + j) * G2;
  const X0 = i - t;
  const Y0 = j - t;
  const x0 = x - X0;
  const y0 = y - Y0;
  let i1, j1;
  if (x0 > y0) { i1 = 1; j1 = 0; }
  else { i1 = 0; j1 = 1; }
  const x1 = x0 - i1 + G2;
  const y1 = y0 - j1 + G2;
  const x2 = x0 - 1 + 2 * G2;
  const y2 = y0 - 1 + 2 * G2;
  const grad = [
    [1,1],[-1,1],[1,-1],[-1,-1],[1,0],[-1,0],[0,1],[0,-1]
  ];
  function hash(ix, iy) {
    let h = (ix * 374761393 + iy * 668265263 + 1013904223) | 0;
    h = ((h ^ (h >>> 13)) * 1274126177) | 0;
    return ((h ^ (h >>> 16)) & 7);
  }
  function dot(g, dx, dy) { return g[0] * dx + g[1] * dy; }
  function contrib(ix, iy, dx, dy) {
    const t2 = 0.5 - dx * dx - dy * dy;
    if (t2 < 0) return 0;
    const t4 = t2 * t2;
    return t4 * t4 * dot(grad[hash(ix, iy)], dx, dy);
  }
  let n0 = contrib(i, j, x0, y0);
  let n1 = contrib(i + i1, j + j1, x1, y1);
  let n2 = contrib(i + 1, j + 1, x2, y2);
  return 70 * (n0 + n1 + n2);
}
function generateTimeSeriesData() {
  const data = [];
  for (let t = 0; t < TIME_POINTS; t++) {
    const revenue = [];
    const users = [];
    const errors = [];
    const apiCalls = [];
    const phase = t * 0.4;
    for (let y = 0; y < GRID; y++) {
      const rowR = [];
      const rowU = [];
      const rowE = [];
      const rowA = [];
      for (let x = 0; x < GRID; x++) {
        const nx = (x / GRID - 0.5) * 4;
        const ny = (y / GRID - 0.5) * 4;
        const base = simplex2D(nx + phase * 0.3, ny + phase * 0.2) * 0.5;
        const ridge = simplex2D(nx * 1.7 + 2, ny * 1.7) * 0.4;
        const trend = Math.sin(nx * 0.8 + phase) * Math.cos(ny * 0.6 + phase * 0.7) * 0.5;
        let rev = (base + ridge * 0.6 + trend * 0.7 + 0.6);
        rev = Math.max(0.05, rev);
        const amp = 0.4 + simplex2D(nx * 2.1 + 3, ny * 2.1 + phase * 0.5) * 0.3;
        rev *= (0.7 + amp);
        rowR.push(rev);
        const ud = Math.max(0.05, (rev * 0.8 + simplex2D(nx * 3 + 5, ny * 3 + t * 0.2) * 0.3 + 0.2));
        rowU.push(ud);
        const err = Math.max(0, (1 - rev) * 0.5 + simplex2D(nx * 5 + 7, ny * 5 + t * 0.15) * 0.2);
        rowE.push(err);
        const api = Math.max(0.02, rev * 0.5 + simplex2D(nx * 4 + 9, ny * 4 + t * 0.25) * 0.25);
        rowA.push(api);
      }
      revenue.push(rowR);
      users.push(rowU);
      errors.push(rowE);
      apiCalls.push(rowA);
    }
    data.push({ revenue, users, errors, apiCalls });
  }
  return data;
}
function buildTerrainGeometry(timepoint) {
  if (cachedGeometries.has(timepoint)) {
    return cachedGeometries.get(timepoint).clone();
  }
  const tp = timeSeriesData[timepoint];
  const segments = GRID - 1;
  const half = TERRAIN_SIZE / 2;
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = (iy * GRID + ix) * 3;
      const px = (ix / segments) * TERRAIN_SIZE - half;
      const pz = (iy / segments) * TERRAIN_SIZE - half;
      const height = tp.revenue[iy][ix] * 6;
      positions[idx] = px;
      positions[idx + 1] = height;
      positions[idx + 2] = pz;
      const ud = tp.users[iy][ix];
      const color = new THREE.Color();
      color.setHSL(0.28 + ud * 0.2, 0.7, 0.15 + ud * 0.5);
      colors[idx] = color.r;
      colors[idx + 1] = color.g;
      colors[idx + 2] = color.b;
    }
  }
  const indices = [];
  for (let iy = 0; iy < segments; iy++) {
    for (let ix = 0; ix < segments; ix++) {
      const a = iy * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  cachedGeometries.set(timepoint, geom);
  return geom.clone();
}
function buildRiverGeometry(timepoint) {
  const tp = timeSeriesData[timepoint];
  const half = TERRAIN_SIZE / 2;
  const segments = GRID - 1;
  const threshold = 0.35;
  const visited = new Uint8Array(GRID * GRID);
  const riverPaths = [];
  const directions = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      if (visited[iy * GRID + ix]) continue;
      if (tp.errors[iy][ix] < threshold) continue;
      const path = [];
      let cx = ix, cy = iy;
      while (cx >= 0 && cx < GRID && cy >= 0 && cy < GRID && !visited[cy * GRID + cx] && tp.errors[cy][cx] >= threshold * 0.6) {
        visited[cy * GRID + cx] = 1;
        const px = (cx / segments) * TERRAIN_SIZE - half;
        const pz = (cy / segments) * TERRAIN_SIZE - half;
        const py = tp.revenue[cy][cx] * 6 + 0.15;
        path.push(new THREE.Vector3(px, py, pz));
        let bestDir = null;
        let bestErr = -1;
        for (const [dx, dy] of directions) {
          const nx = cx + dx;
          const ny = cy + dy;
          if (nx >= 0 && nx < GRID && ny >= 0 && ny < GRID && !visited[ny * GRID + nx]) {
            if (tp.errors[ny][nx] > bestErr) {
              bestErr = tp.errors[ny][nx];
              bestDir = [dx, dy];
            }
          }
        }
        if (!bestDir || bestErr < threshold * 0.4) break;
        cx += bestDir[0];
        cy += bestDir[1];
      }
      if (path.length >= 3) riverPaths.push(path);
    }
  }
  return riverPaths;
}
function buildParticleSystem(timepoint) {
  const tp = timeSeriesData[timepoint];
  const half = TERRAIN_SIZE / 2;
  const segments = GRID - 1;
  const count = 800;
  const positions = new Float32Array(count * 3);
  const velocities = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const ix = Math.floor(Math.random() * GRID);
    const iy = Math.floor(Math.random() * GRID);
    const px = (ix / segments) * TERRAIN_SIZE - half;
    const pz = (iy / segments) * TERRAIN_SIZE - half;
    const py = tp.revenue[iy][ix] * 6 + 0.3;
    positions[i * 3] = px;
    positions[i * 3 + 1] = py;
    positions[i * 3 + 2] = pz;
    const vx = (Math.random() - 0.5) * 0.8;
    const vz = (Math.random() - 0.5) * 0.8;
    const vy = Math.random() * 0.3;
    velocities[i * 3] = vx;
    velocities[i * 3 + 1] = vy;
    velocities[i * 3 + 2] = vz;
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.08,
    color: 0xffdd44,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
  });
  const points = new THREE.Points(geom, mat);
  points.userData = { velocities, timepoint };
  return points;
}
function updateParticles(delta) {
  if (!particleSystem) return;
  const tp = timeSeriesData[currentTimeIndex];
  const half = TERRAIN_SIZE / 2;
  const segments = GRID - 1;
  const positions = particleSystem.geometry.attributes.position.array;
  const velocities = particleSystem.userData.velocities;
  const count = positions.length / 3;
  for (let i = 0; i < count; i++) {
    const i3 = i * 3;
    let px = positions[i3] + velocities[i3] * delta;
    let py = positions[i3 + 1] + velocities[i3 + 1] * delta;
    let pz = positions[i3 + 2] + velocities[i3 + 2] * delta;
    const gx = Math.round(((px + half) / TERRAIN_SIZE) * segments);
    const gy = Math.round(((pz + half) / TERRAIN_SIZE) * segments);
    if (gx < 0 || gx >= GRID || gy < 0 || gy >= GRID) {
      const nix = Math.floor(Math.random() * GRID);
      const niy = Math.floor(Math.random() * GRID);
      px = (nix / segments) * TERRAIN_SIZE - half;
      pz = (niy / segments) * TERRAIN_SIZE - half;
      py = tp.revenue[niy][nix] * 6 + 0.3;
      velocities[i3] = (Math.random() - 0.5) * 0.8;
      velocities[i3 + 1] = Math.random() * 0.4;
      velocities[i3 + 2] = (Math.random() - 0.5) * 0.8;
    } else {
      const ground = tp.revenue[gy][gx] * 6 + 0.25;
      if (py < ground) {
        py = ground;
        velocities[i3 + 1] = Math.abs(velocities[i3 + 1]) * 0.5;
      }
    }
    positions[i3] = px;
    positions[i3 + 1] = py;
    positions[i3 + 2] = pz;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
function clearRivers() {
  for (const line of riverLines) {
    scene.remove(line);
    if (line.geometry) line.geometry.dispose();
    if (line.material) line.material.dispose();
  }
  riverLines = [];
}
function buildRivers(timepoint) {
  clearRivers();
  const paths = buildRiverGeometry(timepoint);
  for (const path of paths) {
    const curve = new THREE.CatmullRomCurve3(path);
    const points = curve.getPoints(path.length * 3);
    const geom = new THREE.BufferGeometry().setFromPoints(points);
    const mat = new THREE.LineBasicMaterial({
      color: 0xff3333,
      linewidth: 1,
      transparent: true,
      opacity: 0.75,
      depthTest: true,
    });
    const line = new THREE.Line(geom, mat);
    line.renderOrder = 1;
    line.material.depthTest = true;
    line.material.depthWrite = true;
    scene.add(line);
    riverLines.push(line);
  }
}
function setTimepoint(index) {
  if (index === currentTimeIndex && terrainMesh) return;
  currentTimeIndex = index;
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    scene.remove(terrainMesh);
  }
  const geom = buildTerrainGeometry(index);
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.15,
    flatShading: false,
    side: THREE.DoubleSide,
  });
  terrainMesh = new THREE.Mesh(geom, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  buildRivers(index);
  if (particleSystem) {
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
    scene.remove(particleSystem);
  }
  particleSystem = buildParticleSystem(index);
  scene.add(particleSystem);
  timeSlider.value = index;
  timeLabel.textContent = 'T' + index + ' / ' + (TIME_POINTS - 1);
}
function saveBookmark() {
  const bm = {
    position: camera.position.clone(),
    target: controls.target.clone(),
    timeIndex: currentTimeIndex,
    label: 'View ' + (bookmarks.length + 1),
  };
  bookmarks.push(bm);
  renderBookmarks();
}
function loadBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  camera.position.copy(bm.position);
  controls.target.copy(bm.target);
  controls.update();
  setTimepoint(bm.timeIndex);
}
function deleteBookmark(index) {
  bookmarks.splice(index, 1);
  renderBookmarks();
}
function renderBookmarks() {
  bookmarkList.innerHTML = '';
  for (let i = 0; i < bookmarks.length; i++) {
    const btn = document.createElement('button');
    btn.className = 'bookmark-btn';
    btn.innerHTML = bookmarks[i].label + ' (T' + bookmarks[i].timeIndex + ')<span class="bookmark-del" data-idx="' + i + '">x</span>';
    btn.addEventListener('click', function(e) {
      if (e.target.classList.contains('bookmark-del')) {
        e.stopPropagation();
        deleteBookmark(parseInt(e.target.dataset.idx));
      } else {
        loadBookmark(i);
      }
    });
    bookmarkList.appendChild(btn);
  }
}
function toggleAutoRotate() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  autoRotateBtn.textContent = 'Auto-Rotate: ' + (autoRotate ? 'On' : 'Off');
  autoRotateBtn.classList.toggle('active', autoRotate);
}
function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!terrainMesh) {
    tooltip.style.display = 'none';
    return;
  }
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const half = TERRAIN_SIZE / 2;
    const gx = Math.round(((point.x + half) / TERRAIN_SIZE) * (GRID - 1));
    const gy = Math.round(((point.z + half) / TERRAIN_SIZE) * (GRID - 1));
    if (gx >= 0 && gx < GRID && gy >= 0 && gy < GRID) {
      const tp = timeSeriesData[currentTimeIndex];
      const rev = (tp.revenue[gy][gx] * 100).toFixed(0);
      const usr = (tp.users[gy][gx] * 100).toFixed(0);
      const err = (tp.errors[gy][gx] * 100).toFixed(1);
      const api = (tp.apiCalls[gy][gx] * 100).toFixed(0);
      tooltip.innerHTML = 'Revenue: ' + rev + '% | Users: ' + usr + '% | Errors: ' + err + '% | API: ' + api + '%';
      tooltip.style.display = 'block';
      tooltip.style.left = (event.clientX + 18) + 'px';
      tooltip.style.top = (event.clientY - 10) + 'px';
      return;
    }
  }
  tooltip.style.display = 'none';
}
function importJSON(jsonText) {
  try {
    const parsed = JSON.parse(jsonText);
    if (Array.isArray(parsed) && parsed.length > 0 && parsed[0].revenue) {
      timeSeriesData = parsed;
      timeSlider.max = parsed.length - 1;
      timeLabel.textContent = 'T0 / ' + (parsed.length - 1);
      cachedGeometries.clear();
      setTimepoint(0);
      return true;
    }
    alert('Invalid format. Expected array of {revenue, users, errors, apiCalls} objects.');
    return false;
  } catch (e) {
    alert('Invalid JSON: ' + e.message);
    return false;
  }
}
function importCSV(csvText) {
  const lines = csvText.trim().split('\n');
  if (lines.length < 2) { alert('CSV too short'); return false; }
  const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
  const timeCol = headers.indexOf('time') >= 0 ? headers.indexOf('time') : headers.indexOf('t');
  const revCol = headers.indexOf('revenue') >= 0 ? headers.indexOf('revenue') : 0;
  const usrCol = headers.indexOf('users') >= 0 ? headers.indexOf('users') : headers.indexOf('user_density');
  const errCol = headers.indexOf('errors') >= 0 ? headers.indexOf('errors') : headers.indexOf('error_rate');
  const apiCol = headers.indexOf('api') >= 0 ? headers.indexOf('api') : headers.indexOf('api_calls');
  const groups = new Map();
  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(',');
    if (cols.length < 3) continue;
    const t = timeCol >= 0 ? parseInt(cols[timeCol]) || 0 : 0;
    if (!groups.has(t)) groups.set(t, []);
    groups.get(t).push({
      revenue: parseFloat(cols[revCol]) || 0,
      users: usrCol >= 0 ? (parseFloat(cols[usrCol]) || 0) : 0,
      errors: errCol >= 0 ? (parseFloat(cols[errCol]) || 0) : 0,
      api: apiCol >= 0 ? (parseFloat(cols[apiCol]) || 0) : 0,
    });
  }
  const data = [];
  const sortedTimes = [...groups.keys()].sort((a, b) => a - b);
  for (const t of sortedTimes) {
    const rows = groups.get(t);
    const side = Math.ceil(Math.sqrt(rows.length));
    const revenue = []; const users = []; const errors = []; const apiCalls = [];
    for (let y = 0; y < side; y++) {
      const rR = []; const rU = []; const rE = []; const rA = [];
      for (let x = 0; x < side; x++) {
        const idx = y * side + x;
        if (idx < rows.length) {
          rR.push(rows[idx].revenue);
          rU.push(rows[idx].users);
          rE.push(rows[idx].errors);
          rA.push(rows[idx].api);
        } else {
          rR.push(0);
          rU.push(0);
          rE.push(0);
          rA.push(0);
        }
      }
      revenue.push(rR); users.push(rU); errors.push(rE); apiCalls.push(rA);
    }
    data.push({ revenue, users, errors, apiCalls });
  }
  timeSeriesData = data;
  timeSlider.max = data.length - 1;
  timeLabel.textContent = 'T0 / ' + (data.length - 1);
  cachedGeometries.clear();
  setTimepoint(0);
  return true;
}
function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    const text = e.target.result;
    if (file.name.endsWith('.json')) {
      importJSON(text);
    } else if (file.name.endsWith('.csv')) {
      importCSV(text);
    } else {
      try {
        importJSON(text);
      } catch (_) {
        importCSV(text);
      }
    }
  };
  reader.readAsText(file);
  fileInput.value = '';
}
function onResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
function addGridHelper() {
  const gridHelper = new THREE.GridHelper(TERRAIN_SIZE, 20, 0x334466, 0x1a1a3a);
  gridHelper.position.y = 0.01;
  scene.add(gridHelper);
}
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  const delta = Math.min(0.1, timestamp ? 0.016 : 0.016);
  updateParticles(delta);
  renderer.render(scene, camera);
}
timeSeriesData = generateTimeSeriesData();
addGridHelper();
setTimepoint(0);
renderBookmarks();
timeSlider.addEventListener('input', function() {
  setTimepoint(parseInt(this.value));
});
autoRotateBtn.addEventListener('click', toggleAutoRotate);
saveBookmarkBtn.addEventListener('click', saveBookmark);
importBtn.addEventListener('click', function() { fileInput.click(); });
fileInput.addEventListener('change', handleFileUpload);
window.addEventListener('resize', onResize);
window.addEventListener('mousemove', onMouseMove);
window.addEventListener('touchmove', function(e) {
  if (e.touches.length === 1) {
    const t = e.touches[0];
    mouse.x = (t.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(t.clientY / window.innerHeight) * 2 + 1;
  }
}, { passive: true });
requestAnimationFrame(animate);
</script>
</body>
</html>