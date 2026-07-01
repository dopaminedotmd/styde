<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a0f;
    --panel-bg: rgba(10,10,20,0.92);
    --text: #c8ccd4;
    --accent: #4da6ff;
    --accent2: #ff6b6b;
    --border: rgba(255,255,255,0.08);
    --input-bg: rgba(255,255,255,0.05);
    --radius: 8px;
    --font: 'Segoe UI', system-ui, sans-serif;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg);
    overflow: hidden;
    font-family: var(--font);
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
  #tooltip {
    position: fixed;
    z-index: 10;
    pointer-events: none;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 8px 12px;
    font-size: 12px;
    line-height: 1.5;
    opacity: 0;
    transition: opacity 0.12s;
    backdrop-filter: blur(10px);
    min-width: 140px;
  }
  #tooltip.visible { opacity: 1; }
  .tt-row { display:flex; justify-content:space-between; gap:16px; }
  .tt-label { color: #8899aa; }
  .tt-val { color: var(--text); font-weight:600; font-variant-numeric: tabular-nums; }
  .tt-val.elevation { color: #4ecdc4; }
  .tt-val.vegetation { color: #6bcf7f; }
  .tt-val.error { color: var(--accent2); }
  #legend {
    position: fixed;
    z-index: 8;
    bottom: 20px;
    left: 20px;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 16px;
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 11px;
  }
  .legend-item { display:flex; align-items:center; gap:8px; }
  .legend-swatch { width:24px; height:4px; border-radius:2px; flex-shrink:0; }
  .legend-swatch.elevation { height:14px; border-radius:3px; background:linear-gradient(to right,#1a3a2a,#2d6a4f,#52b788,#d4d700,#e09f3e,#c1121f); }
  .legend-swatch.vegetation { background:#6bcf7f; height:4px; }
  .legend-swatch.error { background:var(--accent2); height:4px; }
  #time-panel {
    position: fixed;
    z-index: 8;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 10px 20px;
    backdrop-filter: blur(10px);
    display: flex;
    align-items: center;
    gap: 12px;
  }
  #time-slider {
    -webkit-appearance: none;
    width: 200px;
    height: 4px;
    background: rgba(255,255,255,0.15);
    border-radius: 2px;
    outline: none;
  }
  #time-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--accent);
    cursor: pointer;
    border: 2px solid var(--bg);
  }
  #time-label {
    font-size: 12px;
    font-variant-numeric: tabular-nums;
    min-width: 70px;
    text-align: center;
    color: var(--accent);
    font-weight: 600;
  }
  .time-btn {
    background: var(--input-bg);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 4px;
    padding: 4px 10px;
    font-size: 11px;
    cursor: pointer;
    transition: background 0.15s;
    font-family: var(--font);
  }
  .time-btn:hover { background: rgba(255,255,255,0.1); }
  .time-btn.playing { background: var(--accent); color:#000; border-color:var(--accent); }
  #bookmarks {
    position: fixed;
    z-index: 8;
    top: 20px;
    right: 20px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }
  .bm-btn {
    background: var(--panel-bg);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: var(--radius);
    padding: 8px 14px;
    font-size: 11px;
    cursor: pointer;
    backdrop-filter: blur(10px);
    transition: all 0.15s;
    font-family: var(--font);
    text-align: left;
    white-space: nowrap;
  }
  .bm-btn:hover { border-color: var(--accent); background: rgba(77,166,255,0.1); }
  .bm-save { border-color: rgba(255,255,255,0.2); }
  #data-panel {
    position: fixed;
    z-index: 8;
    top: 20px;
    left: 20px;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 16px;
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    gap: 8px;
    font-size: 11px;
  }
  #data-panel label { color: #8899aa; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
  #file-input {
    display: none;
  }
  .data-btn {
    background: var(--input-bg);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 11px;
    cursor: pointer;
    transition: all 0.15s;
    font-family: var(--font);
  }
  .data-btn:hover { background: rgba(255,255,255,0.1); }
  #data-source-label { font-size: 10px; color: #667788; max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  #loading-overlay {
    position: fixed;
    inset: 0;
    z-index: 100;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    color: var(--accent);
    transition: opacity 0.4s;
  }
  #loading-overlay.hidden { opacity:0; pointer-events:none; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="tooltip">
  <div class="tt-row"><span class="tt-label">Elevation</span><span class="tt-val elevation">--</span></div>
  <div class="tt-row"><span class="tt-label">Vegetation</span><span class="tt-val vegetation">--</span></div>
  <div class="tt-row"><span class="tt-label">Error</span><span class="tt-val error">--</span></div>
  <div class="tt-row"><span class="tt-label">X,Y</span><span class="tt-val">--</span></div>
</div>
<div id="legend">
  <div class="legend-item"><div class="legend-swatch elevation"></div><span>Revenue (elevation)</span></div>
  <div class="legend-item"><div class="legend-swatch vegetation"></div><span>User density (green)</span></div>
  <div class="legend-item"><div class="legend-swatch error"></div><span>Error rate (river)</span></div>
</div>
<div id="data-panel">
  <label>Data Source</label>
  <button class="data-btn" id="btn-load-json">Load JSON</button>
  <button class="data-btn" id="btn-load-csv">Load CSV</button>
  <button class="data-btn" id="btn-fetch">Fetch API</button>
  <span id="data-source-label">synthetic (noise)</span>
  <input type="file" id="file-input" accept=".json,.csv">
</div>
<div id="bookmarks">
  <button class="bm-btn" data-bm="0">View 1 — Overview</button>
  <button class="bm-btn" data-bm="1">View 2 — Close-up</button>
  <button class="bm-btn" data-bm="2">View 3 — Top-down</button>
  <button class="bm-btn bm-save" id="btn-save-bm">+ Save current view</button>
</div>
<div id="time-panel">
  <button class="time-btn" id="btn-prev">&lt;</button>
  <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
  <button class="time-btn" id="btn-next">&gt;</button>
  <span id="time-label">T=0</span>
  <button class="time-btn" id="btn-play">Play</button>
</div>
<div id="loading-overlay">Loading 3D Terrain...</div>
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
const GRID_SIZE = 128;
const MAX_PARTICLES = 600;
const PARTICLE_POOL_SIZE = 600;
const container = document.getElementById('canvas-container');
const tooltip = document.getElementById('tooltip');
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const loadingOverlay = document.getElementById('loading-overlay');
const dataSourceLabel = document.getElementById('data-source-label');
let currentTimeIndex = 0;
let timeSeriesData = [];
let isPlaying = false;
let playInterval = null;
let dataSourceType = 'synthetic';
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.Fog(0x0a0a0f, 20, 80);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 200);
camera.position.set(18, 14, 22);
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
controls.target.set(0, 1.5, 0);
controls.minDistance = 3;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.55;
controls.update();
const bookmarks = [
  { pos: new THREE.Vector3(18, 14, 22), target: new THREE.Vector3(0, 1.5, 0) },
  { pos: new THREE.Vector3(5, 6, 8), target: new THREE.Vector3(1, 2, 1) },
  { pos: new THREE.Vector3(0, 25, 0.5), target: new THREE.Vector3(0, 2, 0) },
];
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 1024;
sunLight.shadow.mapSize.height = 1024;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 80;
sunLight.shadow.camera.left = -25;
sunLight.shadow.camera.right = 25;
sunLight.shadow.camera.top = 25;
sunLight.shadow.camera.bottom = -25;
sunLight.shadow.bias = -0.0008;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466aa, 1.2);
fillLight.position.set(-8, 3, -5);
scene.add(fillLight);
const terrainGroup = new THREE.Group();
scene.add(terrainGroup);
let terrainMesh = null;
let riverLines = [];
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const particleGroup = new THREE.Group();
scene.add(particleGroup);
const gridHelper = new THREE.GridHelper(24, 24, 0x334466, 0x1a2233);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
class ParticlePool {
  constructor(maxParticles) {
    this.maxParticles = maxParticles;
    this.geometry = new THREE.BufferGeometry();
    this.positions = new Float32Array(maxParticles * 3);
    this.colors = new Float32Array(maxParticles * 3);
    this.sizes = new Float32Array(maxParticles);
    this.velocities = new Float32Array(maxParticles * 3);
    this.lifetimes = new Float32Array(maxParticles);
    this.activeCount = 0;
    this.geometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    this.geometry.setAttribute('color', new THREE.BufferAttribute(this.colors, 3));
    this.geometry.setAttribute('size', new THREE.BufferAttribute(this.sizes, 1));
    for (let i = 0; i < maxParticles; i++) {
      this.positions[i * 3 + 1] = -999;
      this.lifetimes[i] = -1;
      this.sizes[i] = 0.04;
    }
    const material = new THREE.PointsMaterial({
      size: 0.08,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.85,
    });
    this.points = new THREE.Points(this.geometry, material);
    this.points.frustumCulled = false;
  }
  spawn(x, y, z, vx, vy, vz, r, g, b) {
    for (let i = 0; i < this.maxParticles; i++) {
      if (this.lifetimes[i] <= 0) {
        const idx = i * 3;
        this.positions[idx] = x;
        this.positions[idx + 1] = y;
        this.positions[idx + 2] = z;
        this.velocities[idx] = vx;
        this.velocities[idx + 1] = vy;
        this.velocities[idx + 2] = vz;
        this.colors[idx] = r;
        this.colors[idx + 1] = g;
        this.colors[idx + 2] = b;
        this.lifetimes[i] = 1.5 + Math.random() * 2.5;
        this.activeCount++;
        return;
      }
    }
  }
  update(dt, getTerrainHeight) {
    this.activeCount = 0;
    for (let i = 0; i < this.maxParticles; i++) {
      if (this.lifetimes[i] <= 0) continue;
      this.lifetimes[i] -= dt;
      const idx = i * 3;
      this.positions[idx] += this.velocities[idx] * dt;
      this.positions[idx + 1] += this.velocities[idx + 1] * dt;
      this.positions[idx + 2] += this.velocities[idx + 2] * dt;
      const th = getTerrainHeight(this.positions[idx], this.positions[idx + 2]);
      const minY = th + 0.15;
      if (this.positions[idx + 1] < minY) {
        this.positions[idx + 1] = minY;
        this.velocities[idx + 1] = Math.abs(this.velocities[idx + 1]) * 0.3;
        this.velocities[idx] += (Math.random() - 0.5) * 0.3;
        this.velocities[idx + 2] += (Math.random() - 0.5) * 0.3;
      }
      if (this.lifetimes[i] <= 0) {
        this.positions[idx + 1] = -999;
      } else {
        this.activeCount++;
      }
    }
    this.geometry.attributes.position.needsUpdate = true;
    this.geometry.attributes.color.needsUpdate = true;
  }
}
const particlePool = new ParticlePool(PARTICLE_POOL_SIZE);
particleGroup.add(particlePool.points);
function buildTerrainGeometry(data) {
  const segments = GRID_SIZE - 1;
  const half = GRID_SIZE / 2;
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  const colors = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  const indices = [];
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = (iz * GRID_SIZE + ix) * 3;
      const cell = data[iz * GRID_SIZE + ix];
      const x = (ix / segments - 0.5) * 20;
      const z = (iz / segments - 0.5) * 20;
      const elevation = cell.elevation;
      positions[idx] = x;
      positions[idx + 1] = elevation;
      positions[idx + 2] = z;
      colors[idx] = 0.15 + cell.vegetation * 0.7;
      colors[idx + 1] = 0.25 + cell.vegetation * 0.65;
      colors[idx + 2] = 0.08 + cell.vegetation * 0.15;
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
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  return { geometry, positions, colors };
}
function updateTerrainColors(geometry, data) {
  const colors = geometry.attributes.color.array;
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = (iz * GRID_SIZE + ix) * 3;
      const cell = data[iz * GRID_SIZE + ix];
      colors[idx] = 0.15 + cell.vegetation * 0.7;
      colors[idx + 1] = 0.25 + cell.vegetation * 0.65;
      colors[idx + 2] = 0.08 + cell.vegetation * 0.15;
    }
  }
  geometry.attributes.color.needsUpdate = true;
}
function buildRivers(data, threshold) {
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    if (child.material) child.material.dispose();
    riverGroup.remove(child);
  }
  riverLines = [];
  const segments = GRID_SIZE - 1;
  const half = GRID_SIZE / 2;
  const visited = new Uint8Array(GRID_SIZE * GRID_SIZE);
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iz * GRID_SIZE + ix;
      if (visited[idx]) continue;
      const cell = data[idx];
      if (cell.error < threshold) continue;
      const path = [];
      const stack = [[ix, iz]];
      visited[idx] = 1;
      while (stack.length > 0) {
        const [cx, cz] = stack.pop();
        path.push([cx, cz]);
        const neighbors = [[cx + 1, cz], [cx - 1, cz], [cx, cz + 1], [cx, cz - 1]];
        let bestN = null;
        let bestV = -Infinity;
        for (const [nx, nz] of neighbors) {
          if (nx < 0 || nx >= GRID_SIZE || nz < 0 || nz >= GRID_SIZE) continue;
          const ni = nz * GRID_SIZE + nx;
          if (visited[ni]) continue;
          if (data[ni].error >= threshold && data[ni].error > bestV) {
            bestV = data[ni].error;
            bestN = [nx, nz];
          }
        }
        if (bestN) {
          visited[bestN[1] * GRID_SIZE + bestN[0]] = 1;
          stack.push(bestN);
        }
      }
      if (path.length < 3) continue;
      const points = path.map(([px, pz]) => {
        const cell = data[pz * GRID_SIZE + px];
        return new THREE.Vector3(
          (px / segments - 0.5) * 20,
          cell.elevation + 0.06,
          (pz / segments - 0.5) * 20
        );
      });
      const curve = new THREE.CatmullRomCurve3(points);
      const tubeGeom = new THREE.TubeGeometry(curve, path.length * 2, 0.06, 6, false);
      const tubeMat = new THREE.MeshStandardMaterial({
        color: 0xff4444,
        emissive: 0x440000,
        roughness: 0.5,
        metalness: 0.1,
        transparent: true,
        opacity: 0.75,
        depthWrite: true,
      });
      const tube = new THREE.Mesh(tubeGeom, tubeMat);
      tube.renderOrder = 1;
      tube.material.depthTest = true;
      riverGroup.add(tube);
      riverLines.push({ mesh: tube, path });
    }
  }
}
function getTerrainHeight(wx, wz) {
  const segments = GRID_SIZE - 1;
  const ix = Math.round((wx / 20 + 0.5) * segments);
  const iz = Math.round((wz / 20 + 0.5) * segments);
  if (ix < 0 || ix >= GRID_SIZE || iz < 0 || iz >= GRID_SIZE) return 0;
  if (!timeSeriesData[currentTimeIndex]) return 0;
  return timeSeriesData[currentTimeIndex][iz * GRID_SIZE + ix].elevation;
}
function setTerrainFrame(frameIndex) {
  if (!terrainMesh) return;
  const data = timeSeriesData[frameIndex];
  const positions = terrainMesh.geometry.attributes.position.array;
  const segments = GRID_SIZE - 1;
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = (iz * GRID_SIZE + ix) * 3;
      const cell = data[iz * GRID_SIZE + ix];
      positions[idx + 1] = cell.elevation;
    }
  }
  terrainMesh.geometry.attributes.position.needsUpdate = true;
  terrainMesh.geometry.computeVertexNormals();
  updateTerrainColors(terrainMesh.geometry, data);
  buildRivers(data, 0.38);
}
let cachedGeometries = new Map();
function switchToFrame(frameIndex) {
  currentTimeIndex = frameIndex;
  timeSlider.value = frameIndex;
  timeLabel.textContent = `T=${frameIndex}`;
  const data = timeSeriesData[frameIndex];
  if (cachedGeometries.has(frameIndex)) {
    const cached = cachedGeometries.get(frameIndex);
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = cached.geometry.clone();
    updateTerrainColors(terrainMesh.geometry, data);
    buildRivers(data, 0.38);
  } else {
    setTerrainFrame(frameIndex);
  }
}
function generateSyntheticData(numFrames) {
  const frames = [];
  const simplex = (x, y) => {
    const val = Math.sin(x * 1.8) * Math.cos(y * 1.5) * 0.5
      + Math.sin(x * 3.7 + y * 2.1) * 0.3
      + Math.cos(x * 5.2 - y * 4.3) * 0.2;
    return (val + 1) / 2;
  };
  for (let t = 0; t < numFrames; t++) {
    const phase = t * 0.15;
    const frame = new Array(GRID_SIZE * GRID_SIZE);
    for (let iz = 0; iz < GRID_SIZE; iz++) {
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const nx = ix / (GRID_SIZE - 1) * 5;
        const nz = iz / (GRID_SIZE - 1) * 5;
        const elevation = simplex(nx + phase, nz) * 4.5
          + simplex(nx * 0.4, nz * 0.4 + phase * 0.7) * 2.5;
        const vegetation = simplex(nx + 2.7, nz - 1.3 + phase * 0.5) * 0.85;
        const error = Math.pow(Math.max(0, simplex(nx * 2.1 - phase, nz * 1.8) * 1.3 - 0.35), 1.8);
        frame[iz * GRID_SIZE + ix] = { elevation, vegetation, error };
      }
    }
    frames.push(frame);
  }
  return frames;
}
function loadData(frames) {
  timeSeriesData = frames;
  cachedGeometries.clear();
  timeSlider.max = frames.length - 1;
  timeSlider.value = 0;
  currentTimeIndex = 0;
  timeLabel.textContent = 'T=0';
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.material.dispose();
    terrainGroup.remove(terrainMesh);
  }
  const { geometry } = buildTerrainGeometry(frames[0]);
  const material = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.75,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide,
  });
  terrainMesh = new THREE.Mesh(geometry, material);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  terrainGroup.add(terrainMesh);
  buildRivers(frames[0], 0.38);
}
function handleJSONUpload(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const raw = JSON.parse(e.target.result);
      let frames;
      if (Array.isArray(raw)) {
        frames = raw.map(frame => {
          if (Array.isArray(frame)) return frame;
          if (frame.data && Array.isArray(frame.data)) return frame.data;
          return frame;
        });
      } else if (raw.frames && Array.isArray(raw.frames)) {
        frames = raw.frames;
      } else if (raw.data && Array.isArray(raw.data)) {
        frames = raw.data;
      } else {
        frames = [raw];
      }
      frames = frames.map(normalizeFrame);
      if (frames.length === 0) throw new Error('No frames parsed');
      dataSourceType = 'json';
      dataSourceLabel.textContent = file.name;
      loadData(frames);
    } catch (err) {
      alert('JSON parse error: ' + err.message);
    }
  };
  reader.readAsText(file);
}
function handleCSVUpload(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const lines = e.target.result.split('\n').filter(l => l.trim());
      if (lines.length < 2) throw new Error('CSV too short');
      const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
      const frameMap = new Map();
      for (let i = 1; i < lines.length; i++) {
        const cols = lines[i].split(',').map(c => c.trim());
        const t = parseInt(cols[0]) || 0;
        const x = parseInt(cols[1]) || 0;
        const z = parseInt(cols[2]) || 0;
        const elevation = parseFloat(cols[3]) || 0;
        const vegetation = parseFloat(cols[4]) || 0;
        const error = parseFloat(cols[5]) || 0;
        if (!frameMap.has(t)) frameMap.set(t, new Array(GRID_SIZE * GRID_SIZE));
        const frame = frameMap.get(t);
        const idx = z * GRID_SIZE + x;
        if (idx < frame.length) frame[idx] = { elevation, vegetation, error };
      }
      const frames = Array.from(frameMap.entries())
        .sort((a, b) => a[0] - b[0])
        .map(([, f]) => f.map(c => c || { elevation: 0, vegetation: 0, error: 0 }));
      if (frames.length === 0) throw new Error('No frames from CSV');
      dataSourceType = 'csv';
      dataSourceLabel.textContent = file.name;
      loadData(frames);
    } catch (err) {
      alert('CSV parse error: ' + err.message);
    }
  };
  reader.readAsText(file);
}
function normalizeFrame(frame) {
  const out = new Array(GRID_SIZE * GRID_SIZE);
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iz * GRID_SIZE + ix;
      const cell = frame[idx] || {};
      out[idx] = {
        elevation: typeof cell.elevation === 'number' ? cell.elevation : (cell.y || cell.value || cell.height || 0),
        vegetation: typeof cell.vegetation === 'number' ? cell.vegetation : (cell.green || cell.density || cell.users || 0),
        error: typeof cell.error === 'number' ? cell.error : (cell.err || cell.anomaly || 0),
      };
    }
  }
  return out;
}
async function fetchAPIData() {
  const url = prompt('API endpoint URL (returns JSON):');
  if (!url) return;
  try {
    loadingOverlay.classList.remove('hidden');
    const resp = await fetch(url);
    const json = await resp.json();
    let frames;
    if (Array.isArray(json)) frames = json;
    else if (json.frames) frames = json.frames;
    else if (json.data) frames = [json.data];
    else frames = [json];
    frames = frames.map(normalizeFrame);
    dataSourceType = 'api';
    dataSourceLabel.textContent = url.substring(0, 30);
    loadData(frames);
  } catch (err) {
    alert('API fetch error: ' + err.message);
  } finally {
    loadingOverlay.classList.add('hidden');
  }
}
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
function onMouseMove(e) {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (terrainMesh) {
    const intersects = raycaster.intersectObject(terrainMesh);
    if (intersects.length > 0) {
      const point = intersects[0].point;
      const data = timeSeriesData[currentTimeIndex];
      const segments = GRID_SIZE - 1;
      const ix = Math.round((point.x / 20 + 0.5) * segments);
      const iz = Math.round((point.z / 20 + 0.5) * segments);
      if (ix >= 0 && ix < GRID_SIZE && iz >= 0 && iz < GRID_SIZE && data) {
        const cell = data[iz * GRID_SIZE + ix];
        tooltip.querySelector('.elevation').textContent = cell.elevation.toFixed(3);
        tooltip.querySelector('.vegetation').textContent = (cell.vegetation * 100).toFixed(1) + '%';
        tooltip.querySelector('.error').textContent = (cell.error * 100).toFixed(1) + '%';
        tooltip.querySelector('.tt-val:last-child').textContent = `${ix},${iz}`;
        tooltip.style.left = (e.clientX + 18) + 'px';
        tooltip.style.top = (e.clientY - 10) + 'px';
        tooltip.classList.add('visible');
        return;
      }
    }
  }
  tooltip.classList.remove('visible');
}
function onResize() {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
}
window.addEventListener('mousemove', onMouseMove, { passive: true });
window.addEventListener('resize', onResize);
document.getElementById('btn-load-json').addEventListener('click', () => {
  document.getElementById('file-input').accept = '.json';
  document.getElementById('file-input').click();
});
document.getElementById('btn-load-csv').addEventListener('click', () => {
  document.getElementById('file-input').accept = '.csv';
  document.getElementById('file-input').click();
});
document.getElementById('btn-fetch').addEventListener('click', fetchAPIData);
document.getElementById('file-input').addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (!file) return;
  if (file.name.endsWith('.json')) handleJSONUpload(file);
  else if (file.name.endsWith('.csv')) handleCSVUpload(file);
  e.target.value = '';
});
document.querySelectorAll('.bm-btn[data-bm]').forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.bm);
    if (idx < bookmarks.length) {
      const bm = bookmarks[idx];
      animateCamera(bm.pos.clone(), bm.target.clone());
    }
  });
});
document.getElementById('btn-save-bm').addEventListener('click', () => {
  bookmarks.push({
    pos: camera.position.clone(),
    target: controls.target.clone(),
  });
  const btn = document.createElement('button');
  btn.className = 'bm-btn';
  btn.textContent = `View ${bookmarks.length}`;
  btn.addEventListener('click', () => {
    const bm = bookmarks[bookmarks.length - 1];
    animateCamera(bm.pos.clone(), bm.target.clone());
  });
  document.getElementById('bookmarks').insertBefore(btn, document.getElementById('btn-save-bm'));
});
function animateCamera(targetPos, targetLook) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function step(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, targetPos, ease);
    controls.target.lerpVectors(startTarget, targetLook, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(step);
    }
  }
  requestAnimationFrame(step);
}
timeSlider.addEventListener('input', () => {
  const idx = parseInt(timeSlider.value);
  if (idx !== currentTimeIndex) {
    switchToFrame(idx);
  }
});
document.getElementById('btn-prev').addEventListener('click', () => {
  if (currentTimeIndex > 0) switchToFrame(currentTimeIndex - 1);
});
document.getElementById('btn-next').addEventListener('click', () => {
  if (currentTimeIndex < timeSeriesData.length - 1) switchToFrame(currentTimeIndex + 1);
});
const btnPlay = document.getElementById('btn-play');
btnPlay.addEventListener('click', () => {
  if (isPlaying) {
    stopPlayback();
  } else {
    startPlayback();
  }
});
function startPlayback() {
  isPlaying = true;
  btnPlay.textContent = 'Pause';
  btnPlay.classList.add('playing');
  playInterval = setInterval(() => {
    let next = currentTimeIndex + 1;
    if (next >= timeSeriesData.length) next = 0;
    switchToFrame(next);
  }, 350);
}
function stopPlayback() {
  isPlaying = false;
  btnPlay.textContent = 'Play';
  btnPlay.classList.remove('playing');
  if (playInterval) {
    clearInterval(playInterval);
    playInterval = null;
  }
}
const spawnTimer = { accumulator: 0, interval: 0.08 };
function spawnParticles(dt) {
  spawnTimer.accumulator += dt;
  const data = timeSeriesData[currentTimeIndex];
  if (!data) return;
  while (spawnTimer.accumulator >= spawnTimer.interval) {
    spawnTimer.accumulator -= spawnTimer.interval;
    const segments = GRID_SIZE - 1;
    const sx = Math.random() * GRID_SIZE;
    const sz = Math.random() * GRID_SIZE;
    const cell = data[Math.floor(sz) * GRID_SIZE + Math.floor(sx)];
    if (!cell) continue;
    const wx = (sx / segments - 0.5) * 20;
    const wz = (sz / segments - 0.5) * 20;
    const wy = cell.elevation + 0.3;
    const vx = (Math.random() - 0.5) * 2.5;
    const vz = (Math.random() - 0.5) * 2.5;
    const vy = Math.random() * 0.8 + 0.3;
    const warm = cell.error > 0.35;
    particlePool.spawn(wx, wy, wz, vx, vy, vz,
      warm ? 1.0 : 0.3,
      warm ? 0.25 : 0.55,
      warm ? 0.1 : 0.9
    );
  }
}
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  if (timeSeriesData.length > 0) {
    spawnParticles(dt);
    particlePool.update(dt, getTerrainHeight);
  }
  renderer.render(scene, camera);
}
loadData(generateSyntheticData(10));
loadingOverlay.classList.add('hidden');
animate();
console.log('3D Data Terrain Explorer ready');
console.log('Grid:', GRID_SIZE + 'x' + GRID_SIZE);
console.log('Particle pool:', PARTICLE_POOL_SIZE);
console.log('Frames:', timeSeriesData.length);
console.log('Data source:', dataSourceType);
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan');
console.log('Load real data via JSON/CSV/API buttons (top-left)');
</script>
</body>
</html>