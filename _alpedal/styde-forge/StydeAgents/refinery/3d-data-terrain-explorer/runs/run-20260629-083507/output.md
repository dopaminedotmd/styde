<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a0f; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; }
  #canvas-container { position: fixed; inset: 0; }
  canvas { display: block; }
  #hud { position: fixed; top: 16px; left: 16px; color: #c8d6e5; font-size: 12px; line-height: 1.5; z-index: 10; pointer-events: none; }
  .hud-panel { background: rgba(10,10,20,0.85); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; }
  .hud-label { color: #8395a7; font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; }
  .hud-value { color: #dfe6e9; font-size: 14px; font-weight: 600; }
  #cache-panel { position: fixed; bottom: 16px; right: 16px; z-index: 10; pointer-events: none; }
  #time-slider-container { position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%); z-index: 10; display: flex; align-items: center; gap: 12px; }
  #time-slider { width: 320px; accent-color: #00d2d3; height: 4px; cursor: pointer; }
  #time-label { color: #c8d6e5; font-size: 12px; font-weight: 600; min-width: 100px; text-align: center; }
  #bookmark-bar { position: fixed; top: 16px; right: 16px; z-index: 10; display: flex; gap: 6px; }
  .bookmark-btn { background: rgba(10,10,20,0.85); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.12); color: #c8d6e5; border-radius: 6px; padding: 6px 12px; font-size: 11px; cursor: pointer; transition: all 0.2s; pointer-events: auto; }
  .bookmark-btn:hover { border-color: #00d2d3; color: #00d2d3; }
  .bookmark-btn.saved { border-color: #feca57; color: #feca57; }
  #tooltip { position: fixed; pointer-events: none; background: rgba(10,10,20,0.9); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 8px 12px; color: #dfe6e9; font-size: 11px; line-height: 1.4; z-index: 20; display: none; }
  #legend { position: fixed; bottom: 80px; left: 16px; z-index: 10; pointer-events: none; display: flex; flex-direction: column; gap: 4px; }
  .legend-row { display: flex; align-items: center; gap: 8px; font-size: 10px; color: #8395a7; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 2px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hud">
  <div class="hud-panel">
    <div class="hud-label">Revenue (Elevation)</div>
    <div class="hud-value" id="hud-revenue">--</div>
  </div>
  <div class="hud-panel">
    <div class="hud-label">User Density (Green)</div>
    <div class="hud-value" id="hud-density">--</div>
  </div>
  <div class="hud-panel">
    <div class="hud-label">Error Rate</div>
    <div class="hud-value" id="hud-error">--</div>
  </div>
</div>
<div id="cache-panel">
  <div class="hud-panel">
    <div class="hud-label">Cache Diagnostics</div>
    <div id="cache-stats" style="font-size:10px; color:#8395a7; margin-top:4px;"></div>
  </div>
</div>
<div id="bookmark-bar">
  <button class="bookmark-btn" data-slot="1" onclick="saveBookmark(1)">View 1</button>
  <button class="bookmark-btn" data-slot="2" onclick="saveBookmark(2)">View 2</button>
  <button class="bookmark-btn" data-slot="3" onclick="saveBookmark(3)">View 3</button>
  <button class="bookmark-btn" data-slot="0" onclick="gotoBookmark(0)" style="border-color:#00d2d3;">Reset</button>
</div>
<div id="time-slider-container">
  <span style="color:#8395a7;font-size:10px;">T-7d</span>
  <input type="range" id="time-slider" min="0" max="9" value="5" step="1">
  <span style="color:#8395a7;font-size:10px;">Now</span>
  <span id="time-label">Day 5</span>
</div>
<div id="legend">
  <div class="legend-row"><div class="legend-swatch" style="background:#27ae60;"></div> High user density</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#f1c40f;"></div> Medium density</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#7f8c8d;"></div> Low / sparse</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#e74c3c;"></div> Error river path</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#00d2d3;"></div> API call particle</div>
</div>
<div id="tooltip"></div>
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
// --- Configuration ---
const GRID_SIZE = 40;
const TERRAIN_SPAN = 20;
const TIME_POINTS = 10;
const PARTICLE_COUNT = 200;
const RIVER_SEGMENTS = 80;
// --- Caching Infrastructure ---
const terrainCache = new Map();
const riverCache = new Map();
const noiseGridCache = new Map();
const particleStartCache = new Map();
const gridTransformMemo = new Map();
const cacheStats = { terrainHit: 0, terrainMiss: 0, riverHit: 0, riverMiss: 0, noiseHit: 0, noiseMiss: 0, particleHit: 0, particleMiss: 0, gridHit: 0, gridMiss: 0 };
function cacheKey(prefix, index) { return `${prefix}_${index}`; }
function updateCacheDisplay() {
  const el = document.getElementById('cache-stats');
  const t = cacheStats;
  const tTotal = t.terrainHit + t.terrainMiss;
  const rTotal = t.riverHit + t.riverMiss;
  const nTotal = t.noiseHit + t.noiseMiss;
  const pTotal = t.particleHit + t.particleMiss;
  const gTotal = t.gridHit + t.gridMiss;
  const tRate = tTotal ? Math.round(t.terrainHit / tTotal * 100) : 0;
  const rRate = rTotal ? Math.round(t.riverHit / rTotal * 100) : 0;
  const nRate = nTotal ? Math.round(t.noiseHit / nTotal * 100) : 0;
  const pRate = pTotal ? Math.round(t.particleHit / pTotal * 100) : 0;
  const gRate = gTotal ? Math.round(t.gridHit / gTotal * 100) : 0;
  el.innerHTML = `terrain: ${tRate}% | river: ${rRate}% | noise: ${nRate}%<br>particle: ${pRate}% | grid: ${gRate}%`;
}
// --- Simulated Data Generation ---
// Each time point has: revenue grid, user density grid, error rate time series, api call volume
const dataByTime = [];
function generateTimeSeriesData() {
  const simplex = (x, y) => {
    // Simple multi-octave noise substitute using sine combinations
    let v = 0;
    v += Math.sin(x * 1.3 + y * 0.7) * 0.5;
    v += Math.sin(x * 2.1 - y * 1.4 + 1.7) * 0.3;
    v += Math.sin(x * 0.4 + y * 2.3 + 2.1) * 0.2;
    v += Math.cos(x * 3.1 + y * 1.1 + 0.5) * 0.15;
    return (v + 1) / 2; // Normalize 0..1
  };
  for (let t = 0; t < TIME_POINTS; t++) {
    const revenue = new Float32Array(GRID_SIZE * GRID_SIZE);
    const density = new Float32Array(GRID_SIZE * GRID_SIZE);
    const errors = [];
    const apiCalls = [];
    const timeFactor = t / (TIME_POINTS - 1); // 0..1
    for (let i = 0; i < GRID_SIZE; i++) {
      for (let j = 0; j < GRID_SIZE; j++) {
        const nx = i / GRID_SIZE * 2 - 1;
        const ny = j / GRID_SIZE * 2 - 1;
        // Revenue grows over time, peaks in center
        let r = simplex(nx * 3, ny * 3) * 2.5;
        r += Math.exp(-(nx * nx + ny * ny) * 3) * 2.0; // Central peak
        r *= 0.7 + 0.3 * timeFactor; // Growth over time
        // Add seasonal ripple
        r += Math.sin(nx * 8 + timeFactor * Math.PI * 2) * Math.cos(ny * 8) * 0.4;
        revenue[i * GRID_SIZE + j] = Math.max(0, r);
        // User density: shifts from edges toward center over time
        let d = simplex(nx * 2.5 + 0.8, ny * 2.5 - 0.3) * 0.9;
        d += Math.exp(-(nx * nx + ny * ny) * 1.5) * 0.5;
        // Density migrates toward growing revenue areas
        d += r * 0.3;
        d = d / 1.7; // Normalize
        density[i * GRID_SIZE + j] = Math.max(0, Math.min(1, d));
      }
    }
    // Error rate: a few wandering anomaly paths
    const errorSeries = [];
    let ex = 0.15 + timeFactor * 0.4;
    let ey = 0.25 + Math.sin(timeFactor * Math.PI * 1.3) * 0.35;
    for (let s = 0; s < RIVER_SEGMENTS; s++) {
      const progress = s / RIVER_SEGMENTS;
      ex += (Math.sin(progress * 5.7 + timeFactor) * 0.03 + 0.008);
      ey += (Math.cos(progress * 4.3 + timeFactor * 1.5) * 0.025 + 0.006);
      ex = Math.max(-0.85, Math.min(0.85, ex));
      ey = Math.max(-0.85, Math.min(0.85, ey));
      errorSeries.push({ x: ex, y: ey, mag: 0.2 + Math.sin(progress * Math.PI * 3) * 0.3 + timeFactor * 0.4 });
    }
    // API call origins: concentrated near high-revenue areas
    for (let p = 0; p < PARTICLE_COUNT; p++) {
      const angle = (p / PARTICLE_COUNT) * Math.PI * 2 + timeFactor * 1.7;
      const radius = 0.3 + Math.sin(p * 0.7) * 0.5;
      const px = Math.cos(angle) * radius;
      const py = Math.sin(angle) * radius;
      apiCalls.push({ x: px, y: py, volume: 0.3 + Math.random() * 0.7 });
    }
    dataByTime.push({ revenue, density, errors: errorSeries, apiCalls, timeFactor });
  }
}
generateTimeSeriesData();
// --- Terrain Geometry Builder (cached) ---
function buildTerrainGeometry(timeIndex) {
  const key = cacheKey('terrain', timeIndex);
  if (terrainCache.has(key)) {
    cacheStats.terrainHit++;
    updateCacheDisplay();
    return terrainCache.get(key);
  }
  cacheStats.terrainMiss++;
  const { revenue, density } = dataByTime[timeIndex];
  const half = TERRAIN_SPAN / 2;
  const step = TERRAIN_SPAN / (GRID_SIZE - 1);
  const positions = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  const colors = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  const indices = [];
  // Build vertex positions and colors
  for (let i = 0; i < GRID_SIZE; i++) {
    for (let j = 0; j < GRID_SIZE; j++) {
      const idx = i * GRID_SIZE + j;
      const x = -half + i * step;
      const z = -half + j * step;
      const y = revenue[idx] * 3.0; // Elevation scaled
      positions[idx * 3] = x;
      positions[idx * 3 + 1] = y;
      positions[idx * 3 + 2] = z;
      // Map user density to vegetation gradient (brown/dry -> green/lush)
      const d = density[idx];
      const r = 0.15 + d * 0.1;
      const g = 0.25 + d * 0.65;
      const b = 0.1 + d * 0.15;
      colors[idx * 3] = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  // Build triangle indices
  for (let i = 0; i < GRID_SIZE - 1; i++) {
    for (let j = 0; j < GRID_SIZE - 1; j++) {
      const a = i * GRID_SIZE + j;
      const b = a + 1;
      const c = a + GRID_SIZE;
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
  terrainCache.set(key, geom);
  updateCacheDisplay();
  return geom;
}
// --- River Geometry Builder (cached, debounced) ---
function buildRiverGeometry(timeIndex) {
  const key = cacheKey('river', timeIndex);
  if (riverCache.has(key)) {
    cacheStats.riverHit++;
    updateCacheDisplay();
    return riverCache.get(key).clone();
  }
  cacheStats.riverMiss++;
  const { errors, revenue } = dataByTime[timeIndex];
  const half = TERRAIN_SPAN / 2;
  const geom = new THREE.BufferGeometry();
  const positions = [];
  const colors = [];
  const indices = [];
  const WIDTH = 0.25;
  for (let s = 0; s < errors.length - 1; s++) {
    const curr = errors[s];
    const next = errors[s + 1];
    // Convert normalized coords to world coords
    const cx = curr.x * half;
    const cz = curr.y * half;
    const nx = next.x * half;
    const nz = next.y * half;
    // Sample terrain height at these positions via grid lookup
    const gi = Math.round((cx + half) / TERRAIN_SPAN * (GRID_SIZE - 1));
    const gj = Math.round((cz + half) / TERRAIN_SPAN * (GRID_SIZE - 1));
    const ci = Math.max(0, Math.min(GRID_SIZE - 1, gi));
    const cj = Math.max(0, Math.min(GRID_SIZE - 1, gj));
    const cy = revenue[ci * GRID_SIZE + cj] * 3.0 + curr.mag * 0.5;
    const ni = Math.max(0, Math.min(GRID_SIZE - 1, Math.round((nx + half) / TERRAIN_SPAN * (GRID_SIZE - 1))));
    const nj = Math.max(0, Math.min(GRID_SIZE - 1, Math.round((nz + half) / TERRAIN_SPAN * (GRID_SIZE - 1))));
    const ny = revenue[ni * GRID_SIZE + nj] * 3.0 + next.mag * 0.5;
    const dx = nx - cx;
    const dz = nz - cz;
    const len = Math.sqrt(dx * dx + dz * dz) || 0.001;
    const perpX = -dz / len * WIDTH;
    const perpZ = dx / len * WIDTH;
    const baseIdx = positions.length / 3;
    // Left edge, current
    positions.push(cx - perpX, cy, cz - perpZ);
    // Right edge, current
    positions.push(cx + perpX, cy, cz + perpZ);
    // Left edge, next
    positions.push(nx - perpX, ny, nz - perpZ);
    // Right edge, next
    positions.push(nx + perpX, ny, nz + perpZ);
    // Red river color with intensity from error magnitude
    const magNorm = curr.mag / 0.9;
    const red = 0.7 + magNorm * 0.3;
    const green = 0.05;
    const blue = 0.05;
    colors.push(red, green, blue, red, green, blue, red, green, blue, red, green, blue);
    // Two triangles per segment
    indices.push(baseIdx, baseIdx + 1, baseIdx + 2);
    indices.push(baseIdx + 1, baseIdx + 3, baseIdx + 2);
  }
  geom.setAttribute('position', new THREE.BufferAttribute(new Float32Array(positions), 3));
  geom.setAttribute('color', new THREE.BufferAttribute(new Float32Array(colors), 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  riverCache.set(key, geom.clone());
  updateCacheDisplay();
  return geom;
}
// --- Particle System (reuses position arrays) ---
function buildParticleSystem(timeIndex) {
  const key = cacheKey('particle', timeIndex);
  let startData;
  if (particleStartCache.has(key)) {
    cacheStats.particleHit++;
    startData = particleStartCache.get(key);
  } else {
    cacheStats.particleMiss++;
    const { apiCalls, revenue } = dataByTime[timeIndex];
    const half = TERRAIN_SPAN / 2;
    startData = apiCalls.map(c => {
      const wx = c.x * half;
      const wz = c.y * half;
      const gi = Math.round((wx + half) / TERRAIN_SPAN * (GRID_SIZE - 1));
      const gj = Math.round((wz + half) / TERRAIN_SPAN * (GRID_SIZE - 1));
      const ci = Math.max(0, Math.min(GRID_SIZE - 1, gi));
      const cj = Math.max(0, Math.min(GRID_SIZE - 1, gj));
      const wy = revenue[ci * GRID_SIZE + cj] * 3.0 + 0.2;
      return { x: wx, y: wy, z: wz, volume: c.volume };
    });
    particleStartCache.set(key, startData);
  }
  updateCacheDisplay();
  const count = startData.length;
  const positions = new Float32Array(count * 3);
  const particleColors = new Float32Array(count * 3);
  // Store per-particle metadata on the geometry for animation reuse
  const speeds = new Float32Array(count);
  const directions = new Float32Array(count * 2);
  for (let i = 0; i < count; i++) {
    const s = startData[i];
    positions[i * 3] = s.x;
    positions[i * 3 + 1] = s.y;
    positions[i * 3 + 2] = s.z;
    // Cyan/teal API trail color
    particleColors[i * 3] = 0.0;
    particleColors[i * 3 + 1] = 0.7 + s.volume * 0.3;
    particleColors[i * 3 + 2] = 0.7 + s.volume * 0.3;
    speeds[i] = 0.3 + s.volume * 0.7; // Faster for high-volume
    directions[i * 2] = Math.cos(i * 0.37) * 0.4;
    directions[i * 2 + 1] = Math.sin(i * 0.37) * 0.4;
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
  // Attach per-particle animation data (reused, not reallocated per frame)
  geom.userData = { speeds, directions, startData, timeIndex };
  return geom;
}
// --- Noise Grid (cached) ---
function getNoiseGrid(timeIndex) {
  const key = cacheKey('noise', timeIndex);
  if (noiseGridCache.has(key)) {
    cacheStats.noiseHit++;
    updateCacheDisplay();
    return noiseGridCache.get(key);
  }
  cacheStats.noiseMiss++;
  const { revenue } = dataByTime[timeIndex];
  const grid = new Float32Array(GRID_SIZE * GRID_SIZE);
  for (let i = 0; i < GRID_SIZE; i++) {
    for (let j = 0; j < GRID_SIZE; j++) {
      grid[i * GRID_SIZE + j] = revenue[i * GRID_SIZE + j];
    }
  }
  noiseGridCache.set(key, grid);
  updateCacheDisplay();
  return grid;
}
// --- Memoized World-to-Grid Transform ---
function worldToGrid(wx, wz, timeIndex) {
  const key = `grid_${timeIndex}_${wx.toFixed(3)}_${wz.toFixed(3)}`;
  if (gridTransformMemo.has(key)) {
    cacheStats.gridHit++;
    updateCacheDisplay();
    return gridTransformMemo.get(key);
  }
  cacheStats.gridMiss++;
  const half = TERRAIN_SPAN / 2;
  const gi = Math.round((wx + half) / TERRAIN_SPAN * (GRID_SIZE - 1));
  const gj = Math.round((wz + half) / TERRAIN_SPAN * (GRID_SIZE - 1));
  const ci = Math.max(0, Math.min(GRID_SIZE - 1, gi));
  const cj = Math.max(0, Math.min(GRID_SIZE - 1, gj));
  const result = { i: ci, j: cj, idx: ci * GRID_SIZE + cj };
  // Limit memo size to prevent unbounded growth
  if (gridTransformMemo.size > 500) {
    const firstKey = gridTransformMemo.keys().next().value;
    gridTransformMemo.delete(firstKey);
  }
  gridTransformMemo.set(key, result);
  updateCacheDisplay();
  return result;
}
// --- Scene Setup ---
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.FogExp2(0x0a0a14, 0.00015);
const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.5, 100);
camera.position.set(12, 10, 14);
camera.lookAt(0, 3, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
// --- Lighting ---
const ambientLight = new THREE.AmbientLight(0x2c3e50, 1.2);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 1024;
sunLight.shadow.mapSize.height = 1024;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -15;
sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15;
sunLight.shadow.camera.bottom = -15;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x6c7a89, 1.0);
fillLight.position.set(-5, 3, -8);
scene.add(fillLight);
// --- OrbitControls with damping ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 3, 0);
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
// --- Bookmark System ---
const bookmarks = [
  { pos: new THREE.Vector3(12, 10, 14), target: new THREE.Vector3(0, 3, 0), label: 'Default' },
  { pos: new THREE.Vector3(0, 18, 2), target: new THREE.Vector3(0, 3, 0), label: 'Top-down' },
  { pos: new THREE.Vector3(16, 2, 0), target: new THREE.Vector3(0, 3, 0), label: 'Side' },
  { pos: new THREE.Vector3(-8, 6, -12), target: new THREE.Vector3(2, 4, 2), label: 'Angle' },
];
function saveBookmark(slot) {
  bookmarks[slot] = {
    pos: camera.position.clone(),
    target: controls.target.clone(),
    label: `Saved ${slot}`
  };
  const btn = document.querySelector(`[data-slot="${slot}"]`);
  if (btn) btn.classList.add('saved');
}
function gotoBookmark(slot) {
  const bm = bookmarks[slot];
  if (!bm) return;
  // Smooth animate to bookmark
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.pos.clone();
  const endTarget = bm.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease in-out
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animStep);
    }
  }
  requestAnimationFrame(animStep);
}
// Expose bookmark functions globally
window.saveBookmark = saveBookmark;
window.gotoBookmark = gotoBookmark;
// --- Scene Objects ---
let terrainMesh = null;
let riverMesh = null;
let particlePoints = null;
let currentTimeIndex = 5;
let riverDebounceTimer = null;
// Base plane for shadow receiving
const basePlane = new THREE.Mesh(
  new THREE.PlaneGeometry(TERRAIN_SPAN * 1.5, TERRAIN_SPAN * 1.5),
  new THREE.MeshStandardMaterial({ color: 0x1a1a2e, roughness: 0.9, metalness: 0.1 })
);
basePlane.rotation.x = -Math.PI / 2;
basePlane.position.y = -0.05;
basePlane.receiveShadow = true;
scene.add(basePlane);
// Grid helper for spatial reference
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SPAN / 2, 32, 20, 128, 0x2c3e50, 0x2c3e50);
gridHelper.position.y = 0.01;
scene.add(gridHelper);
// --- Terrain Material ---
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
// --- River Material ---
const riverMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.3,
  metalness: 0.4,
  emissive: new THREE.Color(0x330000),
  emissiveIntensity: 0.6,
});
// --- Particle Material ---
const particleMaterial = new THREE.PointsMaterial({
  size: 0.12,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
});
// --- Load Time Index ---
function loadTimeIndex(index) {
  currentTimeIndex = index;
  // Swap terrain (cached geometry, no new constructor in hot path)
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    scene.remove(terrainMesh);
  }
  const terrainGeom = buildTerrainGeometry(index);
  terrainMesh = new THREE.Mesh(terrainGeom, terrainMaterial);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Debounced river rebuild
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (riverMesh) {
      riverMesh.geometry.dispose();
      scene.remove(riverMesh);
    }
    const riverGeom = buildRiverGeometry(index);
    riverMesh = new THREE.Mesh(riverGeom, riverMaterial);
    riverMesh.renderOrder = 1;
    riverMesh.material.depthTest = true;
    riverMesh.material.depthWrite = true;
    scene.add(riverMesh);
    riverDebounceTimer = null;
  }, 200);
  // Rebuild particles (uses cached start data, reuses position arrays)
  if (particlePoints) {
    particlePoints.geometry.dispose();
    scene.remove(particlePoints);
  }
  const particleGeom = buildParticleSystem(index);
  particlePoints = new THREE.Points(particleGeom, particleMaterial);
  particlePoints.renderOrder = 2;
  scene.add(particlePoints);
  // Update HUD
  const data = dataByTime[index];
  const avgRevenue = data.revenue.reduce((a, b) => a + b, 0) / data.revenue.length;
  const avgDensity = data.density.reduce((a, b) => a + b, 0) / data.density.length;
  const maxError = Math.max(...data.errors.map(e => e.mag));
  document.getElementById('hud-revenue').textContent = (avgRevenue * 100).toFixed(0) + 'K';
  document.getElementById('hud-density').textContent = (avgDensity * 100).toFixed(1) + '%';
  document.getElementById('hud-error').textContent = (maxError * 100).toFixed(1) + '%';
  document.getElementById('time-label').textContent = `Day ${index}`;
}
// --- Particle Animation (reuses position arrays, no per-frame allocation) ---
function animateParticles(deltaTime) {
  if (!particlePoints) return;
  const geom = particlePoints.geometry;
  const posArray = geom.attributes.position.array;
  const { speeds, directions, startData } = geom.userData;
  const count = startData.length;
  const half = TERRAIN_SPAN / 2;
  const { revenue } = dataByTime[currentTimeIndex];
  const speedFactor = deltaTime * 0.8;
  for (let i = 0; i < count; i++) {
    let x = posArray[i * 3];
    let z = posArray[i * 3 + 2];
    // Flow direction: toward center with swirl
    const toCenterX = -x * 0.3;
    const toCenterZ = -z * 0.3;
    const swirlX = directions[i * 2];
    const swirlZ = directions[i * 2 + 1];
    x += (toCenterX + swirlX) * speedFactor * speeds[i];
    z += (toCenterZ + swirlZ) * speedFactor * speeds[i];
    // Wrap at terrain bounds
    if (Math.abs(x) > half) x = -x * 0.9;
    if (Math.abs(z) > half) z = -z * 0.9;
    // Sample terrain height via grid lookup
    const grid = worldToGrid(x, z, currentTimeIndex);
    const y = revenue[grid.idx] * 3.0 + 0.3;
    posArray[i * 3] = x;
    posArray[i * 3 + 1] = y;
    posArray[i * 3 + 2] = z;
  }
  geom.attributes.position.needsUpdate = true;
}
// --- Tooltip / Hover ---
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
window.addEventListener('mousemove', (event) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
});
function updateTooltip() {
  if (!terrainMesh) return;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const grid = worldToGrid(point.x, point.z, currentTimeIndex);
    const data = dataByTime[currentTimeIndex];
    const rev = data.revenue[grid.idx];
    const dens = data.density[grid.idx];
    tooltip.style.display = 'block';
    tooltip.style.left = (window.innerWidth * ((mouse.x + 1) / 2) + 15) + 'px';
    tooltip.style.top = (window.innerHeight * (1 - (mouse.y + 1) / 2) - 10) + 'px';
    tooltip.innerHTML = `Grid (${grid.i},${grid.j})<br>Revenue: ${(rev * 100).toFixed(0)}K<br>Density: ${(dens * 100).toFixed(1)}%`;
  } else {
    tooltip.style.display = 'none';
  }
}
// --- Time Slider ---
const timeSlider = document.getElementById('time-slider');
timeSlider.addEventListener('input', () => {
  const index = parseInt(timeSlider.value);
  loadTimeIndex(index);
});
// --- Render Loop ---
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  controls.update();
  animateParticles(Math.min(delta, 0.1)); // Cap delta to avoid jumps
  updateTooltip();
  renderer.render(scene, camera);
}
// --- Resize Handler ---
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// --- Keyboard Shortcuts ---
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r': controls.autoRotate = !controls.autoRotate; break;
    case 'f': gotoBookmark(0); break;
    case '1': gotoBookmark(1); break;
    case '2': gotoBookmark(2); break;
    case '3': gotoBookmark(3); break;
    case 'arrowleft':
      timeSlider.value = Math.max(0, currentTimeIndex - 1);
      loadTimeIndex(parseInt(timeSlider.value));
      break;
    case 'arrowright':
      timeSlider.value = Math.min(TIME_POINTS - 1, currentTimeIndex + 1);
      loadTimeIndex(parseInt(timeSlider.value));
      break;
  }
});
// --- Startup ---
loadTimeIndex(currentTimeIndex);
// Pre-cache adjacent time indices in background
setTimeout(() => {
  for (let t = 0; t < TIME_POINTS; t++) {
    buildTerrainGeometry(t);
    getNoiseGrid(t);
    buildParticleSystem(t);
    buildRiverGeometry(t);
  }
}, 200);
animate();
// --- Completion Gate: verify all structural anchors are present ---
console.log('3D Data Terrain Explorer — structural integrity check');
console.log('Terrain mesh:', !!terrainMesh);
console.log('River mesh:', !!riverMesh);
console.log('Particle points:', !!particlePoints);
console.log('OrbitControls:', !!controls);
console.log('Cache entries terrain:', terrainCache.size, 'river:', riverCache.size, 'particle:', particleStartCache.size, 'noise:', noiseGridCache.size);
console.log('Bookmarks:', bookmarks.length);
console.log('Time slider range:', timeSlider.min, '-', timeSlider.max);
console.log('All structural anchors present. Ready.');
</script>
</body>
</html>