<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0d14;
    --panel-bg: #111620;
    --text: #c8cdd8;
    --accent: #4da6ff;
    --accent-warm: #ff6b4a;
    --border: #1e2433;
    --slider-track: #1a2030;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow: hidden;
    height: 100vh;
    width: 100vw;
    user-select: none;
    -webkit-user-select: none;
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 1;
  }
  canvas { display: block; }
  #panel {
    position: fixed;
    z-index: 10;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    min-width: 520px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }
  #panel .row {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  #panel label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7280;
    min-width: 70px;
  }
  #time-slider {
    flex: 1;
    -webkit-appearance: none;
    appearance: none;
    height: 6px;
    border-radius: 3px;
    background: var(--slider-track);
    outline: none;
    cursor: pointer;
  }
  #time-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--accent);
    cursor: pointer;
    border: 2px solid #fff;
    box-shadow: 0 0 12px rgba(77,166,255,0.4);
  }
  #time-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--accent);
    min-width: 100px;
    text-align: right;
    font-variant-numeric: tabular-nums;
  }
  .btn {
    padding: 6px 14px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: #1a2030;
    color: var(--text);
    cursor: pointer;
    font-size: 12px;
    transition: background 0.15s, border-color 0.15s;
    white-space: nowrap;
  }
  .btn:hover { background: #252d3d; border-color: #3a4458; }
  .btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  .btn.warm { border-color: var(--accent-warm); color: var(--accent-warm); }
  .btn.warm:hover { background: rgba(255,107,74,0.1); }
  #bookmark-bar {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }
  #legend {
    position: fixed;
    z-index: 10;
    top: 20px;
    right: 20px;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 11px;
    backdrop-filter: blur(12px);
  }
  #legend .item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
  }
  #legend .swatch {
    width: 12px;
    height: 12px;
    border-radius: 3px;
  }
  #stats {
    position: fixed;
    z-index: 10;
    top: 20px;
    left: 20px;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 11px;
    backdrop-filter: blur(12px);
  }
  #stats div { margin: 2px 0; }
  #stats .val { color: var(--accent); font-weight: 600; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="stats">
  <div>FPS <span class="val" id="fps-display">--</span></div>
  <div>Vertices <span class="val" id="vert-count">--</span></div>
  <div>Cache <span class="val" id="cache-size">--</span></div>
  <div>Dirty cells <span class="val" id="dirty-count">--</span></div>
</div>
<div id="legend">
  <div class="item"><span class="swatch" style="background:#1a5c2a;"></span> Low density</div>
  <div class="item"><span class="swatch" style="background:#4da832;"></span> Mid density</div>
  <div class="item"><span class="swatch" style="background:#ffc840;"></span> High density</div>
  <div class="item"><span class="swatch" style="background:#ff4a2a;"></span> Error river</div>
  <div class="item"><span class="swatch" style="background:#7eb8ff;"></span> API trail</div>
</div>
<div id="panel">
  <div class="row">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
    <span id="time-label">12:00</span>
  </div>
  <div class="row" style="gap:8px;">
    <button class="btn active" id="btn-orbit">Orbit</button>
    <button class="btn" id="btn-top">Top</button>
    <button class="btn" id="btn-front">Front</button>
    <button class="btn" id="btn-auto-rotate">Auto</button>
    <button class="btn warm" id="btn-bookmark">Save View</button>
  </div>
  <div class="row" id="bookmark-bar"></div>
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
const GRID_RES = 64;
const TIME_POINTS = 24;
const TERRAIN_SIZE = 20;
const MAX_HEIGHT = 6;
const LRU_CAPACITY = 5;
const gridCellCount = GRID_RES * GRID_RES;
function formatHour(h) {
  const hh = String(h).padStart(2, '0');
  return hh + ':00';
}
function lerp(a, b, t) { return a + (b - a) * t; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
const DataGenerator = (() => {
  function generate() {
    const revenue = new Float32Array(TIME_POINTS * gridCellCount);
    const userDensity = new Float32Array(TIME_POINTS * gridCellCount);
    const errorRate = new Float32Array(TIME_POINTS * gridCellCount);
    const apiCalls = new Float32Array(TIME_POINTS * gridCellCount);
    for (let t = 0; t < TIME_POINTS; t++) {
      const hourFraction = t / (TIME_POINTS - 1); // ratio [0,1]
      const offset = t * gridCellCount;
      for (let iy = 0; iy < GRID_RES; iy++) {
        for (let ix = 0; ix < GRID_RES; ix++) {
          const idx = offset + iy * GRID_RES + ix;
          const nx = ix / (GRID_RES - 1); // normalized x [0,1]
          const ny = iy / (GRID_RES - 1); // normalized y [0,1]
          const centerDist = Math.sqrt((nx - 0.5) ** 2 + (ny - 0.5) ** 2); // distance from center [0,~0.707]
          const hill1 = Math.exp(-((nx - 0.35) ** 2 + (ny - 0.55) ** 2) * 18); // primary peak
          const hill2 = Math.exp(-((nx - 0.7) ** 2 + (ny - 0.3) ** 2) * 14);  // secondary peak
          const hill3 = Math.exp(-((nx - 0.25) ** 2 + (ny - 0.75) ** 2) * 12); // tertiary peak
          const timeWave = Math.sin(hourFraction * Math.PI * 2 + centerDist * 4) * 0.3 + 0.7;
          const baseRevenue = (hill1 * 0.8 + hill2 * 0.45 + hill3 * 0.25) * timeWave;
          revenue[idx] = baseRevenue * MAX_HEIGHT; // meters
          const densityBase = (hill1 * 0.6 + hill2 * 0.35 + hill3 * 0.15);
          const densityShift = Math.cos(hourFraction * Math.PI * 2 + nx * 3) * 0.2;
          userDensity[idx] = clamp(densityBase + densityShift, 0.05, 0.95); // ratio [0,1]
          const errBase = Math.max(0, (centerDist - 0.25) * 0.4);
          const errSpike = (Math.abs(nx - 0.45) < 0.04 && ny > 0.2 && ny < 0.8) ? 0.7 : 0;
          const errTime = Math.sin(hourFraction * Math.PI * 3) * 0.15 + 0.15;
          errorRate[idx] = clamp(errBase + errSpike * (0.5 + errTime), 0, 0.85); // ratio [0,1]
          const apiBase = (hill1 * 0.5 + hill2 * 0.3) * 120;
          const apiBurst = (hourFraction > 0.65 && hourFraction < 0.9 && centerDist < 0.4) ? 200 : 0;
          apiCalls[idx] = apiBase + apiBurst; // count/s
        }
      }
    }
    return { revenue, userDensity, errorRate, apiCalls };
  }
  return { generate };
})();
const { revenue, userDensity, errorRate, apiCalls } = DataGenerator.generate();
function getTimeSlice(buffer, t) {
  const offset = t * gridCellCount;
  return buffer.subarray(offset, offset + gridCellCount);
}
class LRUCache {
  constructor(capacity) {
    this.capacity = capacity;
    this.map = new Map();
  }
  get(key) {
    if (!this.map.has(key)) return undefined;
    const value = this.map.get(key);
    this.map.delete(key);
    this.map.set(key, value);
    return value;
  }
  set(key, value) {
    if (this.map.has(key)) this.map.delete(key);
    else if (this.map.size >= this.capacity) {
      const oldest = this.map.keys().next().value;
      const evicted = this.map.get(oldest);
      this.map.delete(oldest);
      if (evicted.geometry) evicted.geometry.dispose();
    }
    this.map.set(key, value);
  }
  get size() { return this.map.size; }
}
class DirtyGrid {
  constructor() {
    this.flags = new Uint8Array(gridCellCount);
    this.dirtyCount = 0;
    this.previousSlice = null;
  }
  markAllDirty() {
    this.flags.fill(1);
    this.dirtyCount = gridCellCount;
  }
  computeDiffs(currentSlice, prevSlice) {
    if (!prevSlice) { this.markAllDirty(); return; }
    this.dirtyCount = 0;
    for (let i = 0; i < gridCellCount; i++) {
      const changed = Math.abs(currentSlice[i] - prevSlice[i]) > 0.001;
      this.flags[i] = changed ? 1 : 0;
      if (changed) this.dirtyCount++;
    }
  }
  isDirty(ix, iy) { return this.flags[iy * GRID_RES + ix] === 1; }
}
function buildTerrainGeometry(heightSlice) {
  const segments = GRID_RES - 1;
  const halfSize = TERRAIN_SIZE * 0.5;
  const positions = new Float32Array(gridCellCount * 3);
  const colors = new Float32Array(gridCellCount * 3);
  const densitySlice = getTimeSlice(userDensity, 0);
  for (let iy = 0; iy < GRID_RES; iy++) {
    for (let ix = 0; ix < GRID_RES; ix++) {
      const vi = iy * GRID_RES + ix;
      const pi = vi * 3;
      const x = (ix / segments) * TERRAIN_SIZE - halfSize; // world units
      const z = (iy / segments) * TERRAIN_SIZE - halfSize; // world units
      const y = heightSlice[vi]; // meters elevation
      positions[pi] = x;
      positions[pi + 1] = y;
      positions[pi + 2] = z;
      const dens = densitySlice[vi]; // ratio [0,1]
      const r = lerp(0.08, 1.0, dens);
      const g = lerp(0.25, 0.7, dens);
      const b = lerp(0.10, 0.35, dens);
      colors[pi] = r;
      colors[pi + 1] = g;
      colors[pi + 2] = b;
    }
  }
  const indices = [];
  for (let iy = 0; iy < segments; iy++) {
    for (let ix = 0; ix < segments; ix++) {
      const a = iy * GRID_RES + ix;
      const b = a + 1;
      const c = a + GRID_RES;
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
  return { geometry: geom, positions, colors };
}
function updateTerrainVertexColors(colorsAttr, densitySlice, errorSlice) {
  const colorArr = colorsAttr.array;
  for (let vi = 0; vi < gridCellCount; vi++) {
    const ci = vi * 3;
    const dens = densitySlice[vi];
    const err = errorSlice[vi];
    const r = lerp(0.08, 1.0, dens);
    const g = lerp(0.25, 0.7, dens);
    const b = lerp(0.10, 0.35, dens);
    const errFactor = clamp(err * 2.5, 0, 1); // amplify error for visibility
    const errR = lerp(r, 1.0, errFactor);
    const errG = lerp(g, 0.15, errFactor);
    const errB = lerp(b, 0.08, errFactor);
    colorArr[ci] = errR;
    colorArr[ci + 1] = errG;
    colorArr[ci + 2] = errB;
  }
  colorsAttr.needsUpdate = true;
}
function updateTerrainHeights(positionsAttr, heightSlice, dirtyGrid) {
  const posArr = positionsAttr.array;
  for (let iy = 0; iy < GRID_RES; iy++) {
    for (let ix = 0; ix < GRID_RES; ix++) {
      if (!dirtyGrid.isDirty(ix, iy)) continue;
      const vi = iy * GRID_RES + ix;
      posArr[vi * 3 + 1] = heightSlice[vi];
    }
  }
  positionsAttr.needsUpdate = true;
}
function buildRiverGeometry(errorSlice, heightSlice, threshold) {
  const halfSize = TERRAIN_SIZE * 0.5;
  const segments = GRID_RES - 1;
  const points = [];
  for (let iy = 0; iy < GRID_RES; iy++) {
    for (let ix = 0; ix < GRID_RES; ix++) {
      const vi = iy * GRID_RES + ix;
      if (errorSlice[vi] < threshold) continue;
      const worldX = (ix / segments) * TERRAIN_SIZE - halfSize;
      const worldZ = (iy / segments) * TERRAIN_SIZE - halfSize;
      const worldY = heightSlice[vi] + 0.08; // slightly above terrain surface
      points.push(new THREE.Vector3(worldX, worldY, worldZ));
    }
  }
  if (points.length < 3) return null;
  const curve = new THREE.CatmullRomCurve3(points);
  const curvePoints = curve.getPoints(points.length * 2);
  const tubeGeom = new THREE.TubeGeometry(curve, curvePoints.length * 2, 0.08, 6, false);
  return tubeGeom;
}
class ParticleFlow {
  constructor(scene) {
    this.scene = scene;
    this.maxParticles = 800;
    this.trailLength = 20;
    const positionsArr = new Float32Array(this.maxParticles * 3);
    const colorsArr = new Float32Array(this.maxParticles * 3);
    this.ages = new Float32Array(this.maxParticles);
    for (let i = 0; i < this.maxParticles; i++) {
      positionsArr[i * 3 + 1] = 999; // hidden: y very far
      this.ages[i] = 0;
    }
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positionsArr, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
    const mat = new THREE.PointsMaterial({
      size: 0.12,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.8,
    });
    this.points = new THREE.Points(geom, mat);
    this.scene.add(this.points);
    this.posAttr = geom.attributes.position;
    this.colorAttr = geom.attributes.color;
    this.spawnIndex = 0;
  }
  spawn(originX, originY, originZ) {
    const i = this.spawnIndex % this.maxParticles;
    const pi = i * 3;
    this.posAttr.array[pi] = originX;
    this.posAttr.array[pi + 1] = originY;
    this.posAttr.array[pi + 2] = originZ;
    this.ages[i] = 1.0;
    this.colorAttr.array[pi] = 0.5;
    this.colorAttr.array[pi + 1] = 0.7;
    this.colorAttr.array[pi + 2] = 1.0;
    this.spawnIndex++;
  }
  update(deltaSec, apiSlice, heightSlice) {
    const posArr = this.posAttr.array;
    const halfSize = TERRAIN_SIZE * 0.5;
    const segments = GRID_RES - 1;
    for (let i = 0; i < this.maxParticles; i++) {
      const pi = i * 3;
      if (this.ages[i] <= 0) continue;
      this.ages[i] -= deltaSec * 0.8; // decay rate: per-second
      const alpha = clamp(this.ages[i], 0, 1);
      this.colorAttr.array[pi + 3 - 1] = alpha; // opacity via blue channel fade
      const driftX = posArr[pi] + (Math.sin(i * 0.7 + performance.now() * 0.001) * 0.03);
      const driftZ = posArr[pi + 2] + (Math.cos(i * 0.7 + performance.now() * 0.001) * 0.03);
      const gx = clamp(Math.round(((driftX + halfSize) / TERRAIN_SIZE) * segments), 0, segments);
      const gz = clamp(Math.round(((driftZ + halfSize) / TERRAIN_SIZE) * segments), 0, segments);
      const vi = gz * GRID_RES + gx;
      const terrainY = heightSlice[vi];
      posArr[pi] = driftX;
      posArr[pi + 1] = terrainY + 0.25 + alpha * 0.6;
      posArr[pi + 2] = driftZ;
      if (this.ages[i] <= 0.01) {
        posArr[pi + 1] = 999;
        this.ages[i] = 0;
      }
    }
    this.posAttr.needsUpdate = true;
    this.colorAttr.needsUpdate = true;
  }
  dispose() {
    this.points.geometry.dispose();
    this.points.material.dispose();
    this.scene.remove(this.points);
  }
}
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0d14');
scene.fog = new THREE.Fog('#0a0d14', 20, 55);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(12, 9, 14);
camera.lookAt(0, 1.5, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
const ambientLight = new THREE.AmbientLight('#304060', 2.2);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffe8d0', 4.5);
sunLight.position.set(15, 18, 8);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 1024;
sunLight.shadow.mapSize.height = 1024;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -15;
sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15;
sunLight.shadow.camera.bottom = -15;
sunLight.shadow.bias = -0.0002;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#4060a0', 1.0);
fillLight.position.set(-5, 3, -4);
scene.add(fillLight);
const gridHelper = new THREE.PolarGridHelper(12, 32, 24, 128, '#1a2540', '#121a2a');
gridHelper.position.y = -0.05;
scene.add(gridHelper);
const lruCache = new LRUCache(LRU_CAPACITY);
const dirtyGrid = new DirtyGrid();
let currentTime = 12;
let terrainMesh = null;
let riverMesh = null;
let particleFlow = null;
let bookmarks = [];
function loadTerrain(t) {
  const prevSlice = currentTime !== t ? getTimeSlice(revenue, currentTime) : null;
  const heightSlice = getTimeSlice(revenue, t);
  const densitySlice = getTimeSlice(userDensity, t);
  const errorSlice = getTimeSlice(errorRate, t);
  dirtyGrid.computeDiffs(heightSlice, prevSlice);
  let cached = lruCache.get(t);
  if (!cached) {
    const { geometry, positions, colors } = buildTerrainGeometry(heightSlice);
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.65,
      metalness: 0.05,
      flatShading: false,
    });
    const mesh = new THREE.Mesh(geometry, mat);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    cached = { mesh, positions, colors };
    lruCache.set(t, cached);
    if (terrainMesh) {
      scene.remove(terrainMesh);
      if (terrainMesh.geometry) terrainMesh.geometry.dispose();
      if (terrainMesh.material) terrainMesh.material.dispose();
    }
    terrainMesh = mesh;
    scene.add(terrainMesh);
    updateTerrainVertexColors(terrainMesh.geometry.attributes.color, densitySlice, errorSlice);
  } else {
    if (cached.mesh !== terrainMesh) {
      if (terrainMesh) {
        scene.remove(terrainMesh);
        if (terrainMesh.geometry && terrainMesh.geometry !== cached.mesh.geometry) terrainMesh.geometry.dispose();
        if (terrainMesh.material) terrainMesh.material.dispose();
      }
      terrainMesh = cached.mesh;
      scene.add(terrainMesh);
    }
    updateTerrainHeights(terrainMesh.geometry.attributes.position, heightSlice, dirtyGrid);
    terrainMesh.geometry.computeVertexNormals();
    updateTerrainVertexColors(terrainMesh.geometry.attributes.color, densitySlice, errorSlice);
  }
  if (riverMesh) {
    scene.remove(riverMesh);
    riverMesh.geometry.dispose();
    riverMesh.material.dispose();
    riverMesh = null;
  }
  const riverGeom = buildRiverGeometry(errorSlice, heightSlice, 0.35);
  if (riverGeom) {
    const riverMat = new THREE.MeshStandardMaterial({
      color: '#ff3a1a',
      roughness: 0.3,
      metalness: 0.2,
      emissive: '#801000',
      emissiveIntensity: 0.6,
    });
    riverMesh = new THREE.Mesh(riverGeom, riverMat);
    riverMesh.renderOrder = 1;
    riverMesh.material.depthTest = true;
    riverMesh.material.depthWrite = true;
    scene.add(riverMesh);
  }
  document.getElementById('vert-count').textContent = gridCellCount.toLocaleString();
  document.getElementById('cache-size').textContent = lruCache.size;
  document.getElementById('dirty-count').textContent = dirtyGrid.dirtyCount;
}
function spawnParticlesFromApi(apiSlice, heightSlice) {
  if (!particleFlow) return;
  const halfSize = TERRAIN_SIZE * 0.5;
  const segments = GRID_RES - 1;
  const spawnRate = 0.03;
  for (let vi = 0; vi < gridCellCount; vi++) {
    const calls = apiSlice[vi];
    if (Math.random() > calls * spawnRate * 0.01) continue;
    const ix = vi % GRID_RES;
    const iy = Math.floor(vi / GRID_RES);
    const wx = (ix / segments) * TERRAIN_SIZE - halfSize;
    const wz = (iy / segments) * TERRAIN_SIZE - halfSize;
    const wy = heightSlice[vi] + 0.15;
    particleFlow.spawn(wx, wy, wz);
  }
}
function setTime(t) {
  currentTime = clamp(t, 0, TIME_POINTS - 1);
  document.getElementById('time-slider').value = currentTime;
  document.getElementById('time-label').textContent = formatHour(currentTime);
  loadTerrain(currentTime);
}
function saveBookmark(name) {
  const pos = camera.position.clone();
  const tgt = controls.target.clone();
  bookmarks.push({ name: name || ('View ' + (bookmarks.length + 1)), position: pos, target: tgt, time: currentTime });
  renderBookmarkBar();
}
function loadBookmark(index) {
  const bm = bookmarks[index];
  if (!bm) return;
  camera.position.copy(bm.position);
  controls.target.copy(bm.target);
  controls.update();
  if (bm.time !== undefined) setTime(bm.time);
}
function renderBookmarkBar() {
  const bar = document.getElementById('bookmark-bar');
  bar.innerHTML = '';
  bookmarks.forEach((bm, i) => {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.textContent = bm.name;
    btn.addEventListener('click', () => loadBookmark(i));
    btn.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      bookmarks.splice(i, 1);
      renderBookmarkBar();
    });
    bar.appendChild(btn);
  });
}
setTime(currentTime);
particleFlow = new ParticleFlow(scene);
document.getElementById('time-slider').addEventListener('input', (e) => {
  setTime(parseInt(e.target.value, 10));
});
document.getElementById('btn-orbit').addEventListener('click', () => {
  camera.position.set(12, 9, 14);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
document.getElementById('btn-top').addEventListener('click', () => {
  camera.position.set(0, 16, 0.5);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
document.getElementById('btn-front').addEventListener('click', () => {
  camera.position.set(0, 2, 16);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
let autoRotating = false;
const btnAuto = document.getElementById('btn-auto-rotate');
btnAuto.addEventListener('click', () => {
  autoRotating = !autoRotating;
  controls.autoRotate = autoRotating;
  btnAuto.classList.toggle('active', autoRotating);
});
document.getElementById('btn-bookmark').addEventListener('click', () => {
  const name = prompt('Bookmark name:', formatHour(currentTime) + ' view');
  if (name !== null) saveBookmark(name);
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
let lastFrameTime = performance.now();
let fpsCounter = 0;
let fpsTimer = 0;
let displayedFps = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  const deltaMs = timestamp - lastFrameTime;
  const deltaSec = Math.min(deltaMs * 0.001, 0.1); // seconds, capped to prevent spiral
  lastFrameTime = timestamp;
  fpsCounter++;
  fpsTimer += deltaMs;
  if (fpsTimer >= 1000) {
    displayedFps = fpsCounter;
    fpsCounter = 0;
    fpsTimer -= 1000;
    document.getElementById('fps-display').textContent = displayedFps;
  }
  controls.update();
  const apiSlice = getTimeSlice(apiCalls, currentTime);
  const heightSlice = getTimeSlice(revenue, currentTime);
  spawnParticlesFromApi(apiSlice, heightSlice);
  if (particleFlow) particleFlow.update(deltaSec, apiSlice, heightSlice);
  renderer.render(scene, camera);
}
requestAnimationFrame(animate);
</script>
</body>
</html>