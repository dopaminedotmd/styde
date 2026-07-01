<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10, 10, 30, 0.85);
    --text: #c8c8d4;
    --accent: #4fc3f7;
    --warn: #ff7043;
    --good: #66bb6a;
    --border: rgba(255,255,255,0.08);
    --radius: 10px;
    --gap: 10px;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    overflow: hidden;
    font-family: 'Segoe UI', system-ui, sans-serif;
    color: var(--text);
    user-select: none;
  }
  canvas { display: block; }
  .panel {
    position: fixed;
    background: var(--panel-bg);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 16px;
    z-index: 10;
    font-size: 13px;
    min-width: 220px;
  }
  .top-left { top: 16px; left: 16px; }
  .top-right { top: 16px; right: 16px; width: 260px; }
  .bottom-left { bottom: 16px; left: 16px; }
  .bottom-center { bottom: 16px; left: 50%; transform: translateX(-50%); }
  .row { display: flex; align-items: center; gap: var(--gap); margin-bottom: 8px; }
  .row:last-child { margin-bottom: 0; }
  .row.col { flex-direction: column; align-items: flex-start; }
  label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; color: #888; }
  .val { font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums; }
  .val.good { color: var(--good); }
  .val.warn { color: var(--warn); }
  input[type=range] {
    width: 100%;
    height: 4px;
    -webkit-appearance: none;
    background: rgba(255,255,255,0.12);
    border-radius: 2px;
    outline: none;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px; height: 16px;
    background: var(--accent);
    border-radius: 50%;
    cursor: pointer;
  }
  button {
    background: rgba(255,255,255,0.08);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    transition: background 0.15s;
  }
  button:hover { background: rgba(255,255,255,0.16); }
  button.active { background: var(--accent); color: #000; border-color: var(--accent); }
  .bookmark-row { gap: 4px; }
  .bookmark-row button { flex: 1; padding: 5px 0; min-width: 0; }
  .stat-line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }
  .stat-label { font-size: 11px; color: #999; }
  .stat-val { font-size: 12px; font-weight: 600; }
  .legend-item { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; font-size: 11px; }
  .swatch { width: 12px; height: 12px; border-radius: 2px; flex-shrink: 0; }
  #time-label { min-width: 48px; text-align: center; }
</style>
</head>
<body>
<div class="panel top-left" id="control-panel">
  <div class="row"><label>Terrain Explorer</label></div>
  <div class="row">
    <button id="btn-play" title="Play/Pause time">&#9654;</button>
    <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
    <span class="val" id="time-label">12:00</span>
  </div>
  <div class="row">
    <label>Speed</label>
    <input type="range" id="speed-slider" min="1" max="10" value="3" step="1" style="width:80px;">
    <span class="val" id="speed-label">3x</span>
  </div>
  <div class="row">
    <button id="btn-autorot" class="active">Auto-Rotate</button>
    <button id="btn-reset-cam">Reset View</button>
  </div>
  <div class="row"><label>Camera Bookmarks</label></div>
  <div class="row bookmark-row">
    <button class="bm-save" data-slot="0">S1</button>
    <button class="bm-load" data-slot="0">L1</button>
    <button class="bm-save" data-slot="1">S2</button>
    <button class="bm-load" data-slot="1">L2</button>
  </div>
  <div class="row bookmark-row">
    <button class="bm-save" data-slot="2">S3</button>
    <button class="bm-load" data-slot="2">L3</button>
    <button class="bm-save" data-slot="3">S3</button>
    <button class="bm-load" data-slot="3">L3</button>
  </div>
</div>
<div class="panel top-right" id="diag-panel">
  <div class="row"><label>Cache Diagnostics</label></div>
  <div class="stat-line"><span class="stat-label">Terrain</span><span class="stat-val" id="stat-terrain">h:0 m:0</span></div>
  <div class="stat-line"><span class="stat-label">River</span><span class="stat-val" id="stat-river">h:0 m:0</span></div>
  <div class="stat-line"><span class="stat-label">Transform</span><span class="stat-val" id="stat-transform">h:0 m:0</span></div>
  <div class="stat-line"><span class="stat-label">Particle alloc/frame</span><span class="stat-val good" id="stat-particle">0</span></div>
  <div class="stat-line"><span class="stat-label">Geometry ctors/frame</span><span class="stat-val good" id="stat-ctors">0</span></div>
  <div class="stat-line"><span class="stat-label">FPS</span><span class="stat-val" id="stat-fps">60</span></div>
</div>
<div class="panel bottom-left" id="legend">
  <div class="row"><label>Legend</label></div>
  <div class="legend-item"><span class="swatch" style="background:linear-gradient(to right,#3e2723,#8d6e63);"></span>Low elevation (revenue)</div>
  <div class="legend-item"><span class="swatch" style="background:linear-gradient(to right,#8d6e63,#ffd54f);"></span>High elevation (revenue)</div>
  <div class="legend-item"><span class="swatch" style="background:#66bb6a;"></span>Dense users (vegetation)</div>
  <div class="legend-item"><span class="swatch" style="background:#ff5252;"></span>Error rivers</div>
  <div class="legend-item"><span class="swatch" style="background:#ffd740;"></span>API call particles</div>
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
// ---------- Cache Manager ----------
// Tracks hit/miss for terrain, river, and transform caches.
// Exposes counters to the diagnostic panel for user visibility.
class CacheManager {
  constructor() {
    this.terrainCache = new Map();       // timeIndex -> BufferGeometry
    this.riverGeometry = null;           // cached TubeGeometry, null when invalid
    this.riverValidFor = -1;            // timeIndex the cached river was built for
    this.transformCache = new Map();    // key -> {gridX, gridZ}, cleared per frame
    this.stats = { terrainHits: 0, terrainMisses: 0, riverHits: 0, riverMisses: 0, transformHits: 0, transformMisses: 0 };
    this.perFrameAllocs = 0;             // counter for new geometry constructor calls per frame
  }
  getTerrain(timeIndex) {
    if (this.terrainCache.has(timeIndex)) {
      this.stats.terrainHits++;
      // Return shared geometry — no cloning (performance constraint: share buffers)
      return this.terrainCache.get(timeIndex);
    }
    this.stats.terrainMisses++;
    return null;
  }
  setTerrain(timeIndex, geometry) {
    this.terrainCache.set(timeIndex, geometry);
  }
  getRiver(timeIndex) {
    if (this.riverGeometry && this.riverValidFor === timeIndex) {
      this.stats.riverHits++;
      return this.riverGeometry;
    }
    this.stats.riverMisses++;
    return null;
  }
  setRiver(timeIndex, geometry) {
    // Dispose old geometry before replacing
    if (this.riverGeometry) this.riverGeometry.dispose();
    this.riverGeometry = geometry;
    this.riverValidFor = timeIndex;
  }
  invalidateRiver() {
    this.riverValidFor = -1;
  }
  getTransform(worldX, worldZ) {
    // Simple grid-key memoization; key precision at 0.01 resolution
    const key = `${worldX.toFixed(2)},${worldZ.toFixed(2)}`;
    if (this.transformCache.has(key)) {
      this.stats.transformHits++;
      return this.transformCache.get(key);
    }
    this.stats.transformMisses++;
    return null;
  }
  setTransform(worldX, worldZ, gridPos) {
    const key = `${worldX.toFixed(2)},${worldZ.toFixed(2)}`;
    this.transformCache.set(key, gridPos);
  }
  clearTransforms() {
    this.transformCache.clear();
    this.perFrameAllocs = 0;
  }
}
// ---------- Data Generator ----------
// Produces 24 time steps of mock metrics across a SPARSE_GRID x SPARSE_GRID layout.
// Each cell: {revenue, users, errors, apiCalls}
const SPARSE_GRID = 20;
const TERRAIN_SEGMENTS = 150;
const TERRAIN_SIZE = 60;
function generateMockData() {
  const steps = 24;
  const data = [];
  for (let t = 0; t < steps; t++) {
    const hour = t;
    const grid = [];
    // Base patterns: revenue peaks midday, errors spike late-night, users follow revenue
    const hourFactor = Math.sin((hour / 24) * Math.PI); // 0 at midnight, 1 at noon
    for (let row = 0; row < SPARSE_GRID; row++) {
      const rowData = [];
      for (let col = 0; col < SPARSE_GRID; col++) {
        // Spatial variation: gaussian-like hills centered at various positions
        const cx1 = 5, cy1 = 5, cx2 = 14, cy2 = 14, cx3 = 10, cy3 = 10;
        const d1 = Math.sqrt((row - cx1) ** 2 + (col - cy1) ** 2) / 8;
        const d2 = Math.sqrt((row - cx2) ** 2 + (col - cy2) ** 2) / 7;
        const d3 = Math.sqrt((row - cx3) ** 2 + (col - cy3) ** 2) / 5;
        const spatialFactor = Math.exp(-d1 * d1) * 0.7 + Math.exp(-d2 * d2) * 0.5 + Math.exp(-d3 * d3);
        const revenue = (spatialFactor * hourFactor * 8000 + 2000 + Math.random() * 500);
        const users = Math.round(revenue / 80 + Math.random() * 30);
        // Errors spike when revenue is very high (overload) or very low (idle anomalies)
        const errorRate = (Math.abs(revenue - 5000) / 3000) * (0.5 + 0.5 * Math.random());
        const errors = Math.round(errorRate * 50);
        const apiCalls = Math.round(users * (2 + Math.random() * 3));
        rowData.push({ revenue, users, errors, apiCalls });
      }
      grid.push(rowData);
    }
    data.push({ hour, grid });
  }
  return data;
}
// ---------- Bilinear Interpolation ----------
// Maps sparse grid values to dense terrain vertex grid.
// Returns a flat Float32Array of shape [TERRAIN_SEGMENTS+1][TERRAIN_SEGMENTS+1] per metric.
function interpolateGrid(sparseGrid, metricKey) {
  const segs = TERRAIN_SEGMENTS;
  const result = new Float32Array((segs + 1) * (segs + 1));
  const sparseRes = SPARSE_GRID - 1;
  for (let vi = 0; vi <= segs; vi++) {
    // Map vertex row to sparse grid fractional coordinate
    const fy = (vi / segs) * sparseRes;
    const y0 = Math.min(Math.floor(fy), sparseRes - 1);
    const y1 = Math.min(y0 + 1, sparseRes);
    const ty = fy - y0;
    for (let vj = 0; vj <= segs; vj++) {
      const fx = (vj / segs) * sparseRes;
      const x0 = Math.min(Math.floor(fx), sparseRes - 1);
      const x1 = Math.min(x0 + 1, sparseRes);
      const tx = fx - x0;
      // Bilinear interpolation across the 4 surrounding sparse cells
      const v00 = sparseGrid[y0][x0][metricKey];
      const v10 = sparseGrid[y0][x1][metricKey];
      const v01 = sparseGrid[y1][x0][metricKey];
      const v11 = sparseGrid[y1][x1][metricKey];
      const val = (1 - ty) * ((1 - tx) * v00 + tx * v10) +
                  ty * ((1 - tx) * v01 + tx * v11);
      result[vi * (segs + 1) + vj] = val;
    }
  }
  return result;
}
// ---------- Terrain Builder ----------
// Builds a single BufferGeometry heightfield from interpolated revenue and user data.
// Uses vertex colors for user density (vegetation gradient).
// Geometry is cached per time index — never rebuilt on the same frame.
function buildTerrainGeometry(revenueGrid, usersGrid) {
  const segs = TERRAIN_SEGMENTS;
  const size = TERRAIN_SIZE;
  const half = size / 2;
  const positions = new Float32Array((segs + 1) * (segs + 1) * 3);
  const colors = new Float32Array((segs + 1) * (segs + 1) * 3);
  // Normalize users for color mapping
  let maxUsers = 0;
  for (let i = 0; i < usersGrid.length; i++) {
    if (usersGrid[i] > maxUsers) maxUsers = usersGrid[i];
  }
  maxUsers = Math.max(maxUsers, 1);
  for (let vi = 0; vi <= segs; vi++) {
    for (let vj = 0; vj <= segs; vj++) {
      const idx = vi * (segs + 1) + vj;
      const x = (vj / segs) * size - half;
      const z = (vi / segs) * size - half;
      // Revenue drives elevation: normalize 0-10k to 0-8 units height
      const height = (revenueGrid[idx] / 10000) * 8;
      positions[idx * 3] = x;
      positions[idx * 3 + 1] = height;
      positions[idx * 3 + 2] = z;
      // User density -> vegetation color (brown -> green -> bright green)
      const t = Math.min(usersGrid[idx] / maxUsers, 1);
      const r = 0.24 * (1 - t) + 0.15 * t;
      const g = 0.15 * (1 - t) + 0.75 * t;
      const b = 0.09 * (1 - t) + 0.15 * t;
      colors[idx * 3] = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  // Build index buffer for triangulated grid
  const indices = [];
  for (let vi = 0; vi < segs; vi++) {
    for (let vj = 0; vj < segs; vj++) {
      const a = vi * (segs + 1) + vj;
      const b = a + 1;
      const c = a + (segs + 1);
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
// ---------- River Builder ----------
// Traces error "rivers" by following downhill gradient from high-error cells.
// Returns a TubeGeometry or null if no significant rivers found.
// Debounced externally: only called after 200ms idle on slider.
function buildRiverGeometry(revenueGrid, errorGrid, terrainSize) {
  const segs = TERRAIN_SEGMENTS;
  const size = terrainSize;
  const half = size / 2;
  const cellSize = size / segs;
  // Find river source cells: error > 80th percentile
  const errors = Array.from(errorGrid);
  errors.sort((a, b) => a - b);
  const threshold = errors[Math.floor(errors.length * 0.80)];
  const allPaths = [];
  const visited = new Set();
  // For each high-error cell, trace downhill
  for (let vi = 1; vi < segs; vi++) {
    for (let vj = 1; vj < segs; vj++) {
      const idx = vi * (segs + 1) + vj;
      if (errorGrid[idx] < threshold || visited.has(idx)) continue;
      const path = [];
      let ci = vi, cj = vj, cidx = idx;
      let steps = 0;
      const maxSteps = 60;
      while (steps < maxSteps) {
        path.push({ vi: ci, vj: cj, height: revenueGrid[cidx] });
        visited.add(cidx);
        // Find steepest downhill neighbor
        let bestDi = 0, bestDj = 0;
        let bestDrop = 0;
        for (let di = -1; di <= 1; di++) {
          for (let dj = -1; dj <= 1; dj++) {
            if (di === 0 && dj === 0) continue;
            const ni = ci + di, nj = cj + dj;
            if (ni < 0 || ni > segs || nj < 0 || nj > segs) continue;
            const nidx = ni * (segs + 1) + nj;
            const drop = revenueGrid[cidx] - revenueGrid[nidx];
            if (drop > bestDrop) { bestDrop = drop; bestDi = di; bestDj = dj; }
          }
        }
        // Stop if flat or uphill
        if (bestDrop <= 0.001) break;
        ci += bestDi;
        cj += bestDj;
        cidx = ci * (segs + 1) + cj;
        steps++;
      }
      if (path.length >= 5) allPaths.push(path);
    }
  }
  if (allPaths.length === 0) return null;
  // Convert the longest paths to 3D curves and build TubeGeometry
  // Take top 5 longest paths to avoid visual clutter
  allPaths.sort((a, b) => b.length - a.length);
  const topPaths = allPaths.slice(0, 5);
  const tubeGroup = new THREE.Group();
  const riverMaterial = new THREE.MeshStandardMaterial({
    color: 0xff3d3d,
    emissive: 0x661111,
    roughness: 0.3,
    metalness: 0.1,
  });
  for (const path of topPaths) {
    if (path.length < 3) continue;
    const points = path.map(p => {
      const x = (p.vj / segs) * size - half;
      const z = (p.vi / segs) * size - half;
      // Slightly above terrain to prevent z-fighting
      return new THREE.Vector3(x, p.height + 0.08, z);
    });
    const curve = new THREE.CatmullRomCurve3(points);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.12, 6, false);
    const tubeMesh = new THREE.Mesh(tubeGeo, riverMaterial);
    tubeGroup.add(tubeMesh);
  }
  return tubeGroup;
}
// ---------- Particle System ----------
// Renders API call flows as glowing particles traversing the terrain surface.
// Reuses position array in-place each frame — zero per-frame allocations.
class ParticleSystem {
  constructor(count, terrainSize) {
    this.count = count;
    this.terrainSize = terrainSize;
    this.half = terrainSize / 2;
    // Pre-allocate position array — reused every frame
    this.positions = new Float32Array(count * 3);
    // Store per-particle velocity and lifespan
    this.particleData = new Float32Array(count * 4); // vx, vz, life, maxLife
    // Initialize random positions on terrain surface
    for (let i = 0; i < count; i++) {
      this.resetParticle(i);
      // Start with varied life so particles don't all reset at once
      this.particleData[i * 4 + 2] = Math.random() * this.particleData[i * 4 + 3];
    }
    // Create sprite texture via canvas
    const canvas = document.createElement('canvas');
    canvas.width = 32; canvas.height = 32;
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
    gradient.addColorStop(0, 'rgba(255, 215, 64, 1)');
    gradient.addColorStop(0.3, 'rgba(255, 180, 40, 0.7)');
    gradient.addColorStop(0.7, 'rgba(255, 120, 20, 0.1)');
    gradient.addColorStop(1, 'rgba(255, 80, 0, 0)');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 32, 32);
    const spriteTexture = new THREE.CanvasTexture(canvas);
    spriteTexture.needsUpdate = true;
    // BufferGeometry with shared position buffer
    this.geometry = new THREE.BufferGeometry();
    this.geometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    this.material = new THREE.PointsMaterial({
      size: 0.6,
      map: spriteTexture,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      color: 0xffd740,
    });
    this.points = new THREE.Points(this.geometry, this.material);
  }
  resetParticle(i) {
    const half = this.half;
    // Spawn at random position on terrain plane
    this.positions[i * 3] = (Math.random() - 0.5) * this.terrainSize;
    this.positions[i * 3 + 1] = 0.15; // slightly above surface
    this.positions[i * 3 + 2] = (Math.random() - 0.5) * this.terrainSize;
    // Random velocity direction
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.5 + Math.random() * 1.5;
    this.particleData[i * 4] = Math.cos(angle) * speed;
    this.particleData[i * 4 + 1] = Math.sin(angle) * speed;
    this.particleData[i * 4 + 2] = 0;
    this.particleData[i * 4 + 3] = 3 + Math.random() * 5;
  }
  // Update positions in-place — no allocations
  update(deltaTime, getHeightAt) {
    const dt = Math.min(deltaTime, 0.1); // clamp to avoid jumps on tab switch
    for (let i = 0; i < this.count; i++) {
      const base = i * 4;
      this.particleData[base + 2] += dt;
      // Respawn if life expired
      if (this.particleData[base + 2] >= this.particleData[base + 3]) {
        this.resetParticle(i);
        continue;
      }
      // Move particle
      const px = this.positions[i * 3] + this.particleData[base] * dt;
      const pz = this.positions[i * 3 + 2] + this.particleData[base + 1] * dt;
      // Wrap around terrain bounds
      const half = this.half;
      let wx = px, wz = pz;
      if (wx < -half) wx += this.terrainSize;
      if (wx > half) wx -= this.terrainSize;
      if (wz < -half) wz += this.terrainSize;
      if (wz > half) wz -= this.terrainSize;
      // Height from terrain lookup
      const h = getHeightAt ? getHeightAt(wx, wz) : 0;
      this.positions[i * 3] = wx;
      this.positions[i * 3 + 1] = h + 0.25;
      this.positions[i * 3 + 2] = wz;
    }
    // Mark position attribute as needing GPU upload
    this.geometry.attributes.position.needsUpdate = true;
  }
}
// ---------- Main Application ----------
class TerrainExplorer {
  constructor() {
    this.data = generateMockData();
    this.cache = new CacheManager();
    this.currentTimeIdx = 12;
    this.playing = false;
    this.playSpeed = 3;
    this.autoRotate = true;
    this.bookmarks = [null, null, null, null];
    this.lastRiverSliderVal = 12;
    this.riverDebounceTimer = null;
    this.fpsFrames = 0;
    this.fpsTime = performance.now();
    this.initScene();
    this.initTerrain();
    this.initRivers();
    this.initParticles();
    this.initUI();
    this.animate();
  }
  initScene() {
    // Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;
    document.body.appendChild(this.renderer.domElement);
    // Scene
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0a0a18);
    this.scene.fog = new THREE.FogExp2(0x0a0a18, 0.00025);
    // Camera
    this.camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 300);
    this.camera.position.set(35, 28, 40);
    this.camera.lookAt(0, 2, 0);
    // OrbitControls with smooth damping
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.set(0, 2, 0);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.4;
    this.controls.minDistance = 8;
    this.controls.maxDistance = 80;
    this.controls.maxPolarAngle = Math.PI * 0.48; // prevent going underground
    this.controls.update();
    // Lighting
    const ambient = new THREE.AmbientLight(0x303050, 1.8);
    this.scene.add(ambient);
    const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
    sun.position.set(30, 40, 20);
    sun.castShadow = true;
    sun.shadow.mapSize.width = 2048;
    sun.shadow.mapSize.height = 2048;
    sun.shadow.camera.near = 0.5;
    sun.shadow.camera.far = 150;
    sun.shadow.camera.left = -40;
    sun.shadow.camera.right = 40;
    sun.shadow.camera.top = 40;
    sun.shadow.camera.bottom = -40;
    sun.shadow.bias = -0.0001;
    this.scene.add(sun);
    const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
    fill.position.set(-20, 10, -15);
    this.scene.add(fill);
    // Grid helper on the floor
    const gridHelper = new THREE.GridHelper(TERRAIN_SIZE, 30, 0x222244, 0x111122);
    gridHelper.position.y = -0.05;
    this.scene.add(gridHelper);
    // Resize handler
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }
  initTerrain() {
    // Build terrain for initial time index
    const timeData = this.data[this.currentTimeIdx];
    const revenueGrid = interpolateGrid(timeData.grid, 'revenue');
    const usersGrid = interpolateGrid(timeData.grid, 'users');
    const geo = buildTerrainGeometry(revenueGrid, usersGrid);
    this.cache.setTerrain(this.currentTimeIdx, geo);
    // Also store height data for particle/raycasting lookups
    this.currentRevenueGrid = revenueGrid;
    this.currentUsersGrid = usersGrid;
    const material = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.75,
      metalness: 0.05,
      flatShading: false,
      side: THREE.DoubleSide,
    });
    this.terrainMesh = new THREE.Mesh(geo, material);
    this.terrainMesh.castShadow = true;
    this.terrainMesh.receiveShadow = true;
    this.scene.add(this.terrainMesh);
  }
  initRivers() {
    this.riverGroup = new THREE.Group();
    this.scene.add(this.riverGroup);
    this.rebuildRivers();
  }
  rebuildRivers() {
    // Dispose existing river meshes
    while (this.riverGroup.children.length > 0) {
      const child = this.riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      this.riverGroup.remove(child);
    }
    const timeData = this.data[this.currentTimeIdx];
    const errorGrid = interpolateGrid(timeData.grid, 'errors');
    const riverGeom = buildRiverGeometry(this.currentRevenueGrid, errorGrid, TERRAIN_SIZE);
    if (riverGeom) {
      this.cache.setRiver(this.currentTimeIdx, riverGeom);
      this.riverGroup.add(riverGeom);
    } else {
      this.cache.setRiver(this.currentTimeIdx, new THREE.Group());
    }
  }
  initParticles() {
    this.particleSystem = new ParticleSystem(800, TERRAIN_SIZE);
    this.scene.add(this.particleSystem.points);
  }
  // Height lookup for particles (bilinear on the dense grid)
  getHeightAt(worldX, worldZ) {
    const segs = TERRAIN_SEGMENTS;
    const size = TERRAIN_SIZE;
    const half = size / 2;
    // World to grid coordinates — memoized per frame
    const cached = this.cache.getTransform(worldX, worldZ);
    let gi, gj;
    if (cached) {
      gi = cached.gi; gj = cached.gj;
    } else {
      const fx = (worldX + half) / size * segs;
      const fz = (worldZ + half) / size * segs;
      gi = Math.max(0, Math.min(segs, Math.round(fz)));
      gj = Math.max(0, Math.min(segs, Math.round(fx)));
      this.cache.setTransform(worldX, worldZ, { gi, gj });
    }
    const idx = gi * (segs + 1) + gj;
    return this.currentRevenueGrid ? this.currentRevenueGrid[idx] / 10000 * 8 : 0;
  }
  switchToTime(idx) {
    if (idx === this.currentTimeIdx) return;
    this.currentTimeIdx = idx;
    // Try cache first
    let geo = this.cache.getTerrain(idx);
    if (!geo) {
      // Build and cache
      this.cache.perFrameAllocs++;
      const timeData = this.data[idx];
      this.currentRevenueGrid = interpolateGrid(timeData.grid, 'revenue');
      this.currentUsersGrid = interpolateGrid(timeData.grid, 'users');
      geo = buildTerrainGeometry(this.currentRevenueGrid, this.currentUsersGrid);
      this.cache.setTerrain(idx, geo);
    } else {
      // Update revenue grid for particle lookups when using cached geometry
      const timeData = this.data[idx];
      this.currentRevenueGrid = interpolateGrid(timeData.grid, 'revenue');
      this.currentUsersGrid = interpolateGrid(timeData.grid, 'users');
    }
    // Swap geometry on mesh (no dispose — cached geometry is shared)
    this.terrainMesh.geometry = geo;
    // Debounced river rebuild: 200ms delay
    this.lastRiverSliderVal = idx;
    if (this.riverDebounceTimer) clearTimeout(this.riverDebounceTimer);
    this.riverDebounceTimer = setTimeout(() => {
      if (this.lastRiverSliderVal === idx) {
        this.rebuildRivers();
      }
      this.riverDebounceTimer = null;
    }, 200);
    // Update UI
    const hours = String(idx).padStart(2, '0');
    document.getElementById('time-label').textContent = hours + ':00';
    document.getElementById('time-slider').value = idx;
  }
  initUI() {
    const slider = document.getElementById('time-slider');
    const playBtn = document.getElementById('btn-play');
    const speedSlider = document.getElementById('speed-slider');
    const autorotBtn = document.getElementById('btn-autorot');
    const resetBtn = document.getElementById('btn-reset-cam');
    // Time slider input
    slider.addEventListener('input', () => {
      const idx = parseInt(slider.value);
      this.switchToTime(idx);
    });
    // Play/pause
    playBtn.addEventListener('click', () => {
      this.playing = !this.playing;
      playBtn.innerHTML = this.playing ? '&#9646;&#9646;' : '&#9654;';
    });
    // Speed control
    speedSlider.addEventListener('input', () => {
      this.playSpeed = parseInt(speedSlider.value);
      document.getElementById('speed-label').textContent = this.playSpeed + 'x';
    });
    // Auto-rotate toggle
    autorotBtn.addEventListener('click', () => {
      this.autoRotate = !this.autoRotate;
      this.controls.autoRotate = this.autoRotate;
      autorotBtn.classList.toggle('active', this.autoRotate);
    });
    // Reset camera
    resetBtn.addEventListener('click', () => {
      this.animateCamera(new THREE.Vector3(35, 28, 40), new THREE.Vector3(0, 2, 0));
    });
    // Bookmarks
    document.querySelectorAll('.bm-save').forEach(btn => {
      btn.addEventListener('click', () => {
        const slot = parseInt(btn.dataset.slot);
        this.bookmarks[slot] = {
          position: this.camera.position.clone(),
          target: this.controls.target.clone(),
        };
        // Visual feedback
        btn.style.background = 'rgba(79,195,247,0.3)';
        setTimeout(() => { btn.style.background = ''; }, 300);
      });
    });
    document.querySelectorAll('.bm-load').forEach(btn => {
      btn.addEventListener('click', () => {
        const slot = parseInt(btn.dataset.slot);
        const bm = this.bookmarks[slot];
        if (bm) {
          this.animateCamera(bm.position.clone(), bm.target.clone());
        }
      });
    });
    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {
      switch (e.key.toLowerCase()) {
        case ' ':
          e.preventDefault();
          this.playing = !this.playing;
          playBtn.innerHTML = this.playing ? '&#9646;&#9646;' : '&#9654;';
          break;
        case 'r':
          this.animateCamera(new THREE.Vector3(35, 28, 40), new THREE.Vector3(0, 2, 0));
          break;
        case 'arrowleft':
          this.switchToTime(Math.max(0, this.currentTimeIdx - 1));
          break;
        case 'arrowright':
          this.switchToTime(Math.min(23, this.currentTimeIdx + 1));
          break;
        case 'a':
          this.autoRotate = !this.autoRotate;
          this.controls.autoRotate = this.autoRotate;
          autorotBtn.classList.toggle('active', this.autoRotate);
          break;
      }
    });
  }
  animateCamera(targetPos, targetLookAt) {
    const startPos = this.camera.position.clone();
    const startTarget = this.controls.target.clone();
    const startTime = performance.now();
    const duration = 800; // ms
    const step = (now) => {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      // Ease in-out cubic
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      this.camera.position.lerpVectors(startPos, targetPos, ease);
      this.controls.target.lerpVectors(startTarget, targetLookAt, ease);
      this.controls.update();
      if (t < 1) {
        requestAnimationFrame(step);
      }
    };
    requestAnimationFrame(step);
  }
  updateDiagnostics(deltaTime) {
    // FPS calculation with 500ms averaging window
    this.fpsFrames++;
    const now = performance.now();
    if (now - this.fpsTime >= 500) {
      const fps = Math.round(this.fpsFrames / ((now - this.fpsTime) / 1000));
      document.getElementById('stat-fps').textContent = fps;
      this.fpsFrames = 0;
      this.fpsTime = now;
    }
    const s = this.cache.stats;
    document.getElementById('stat-terrain').textContent = `h:${s.terrainHits} m:${s.terrainMisses}`;
    document.getElementById('stat-river').textContent = `h:${s.riverHits} m:${s.riverMisses}`;
    document.getElementById('stat-transform').textContent = `h:${s.transformHits} m:${s.transformMisses}`;
    document.getElementById('stat-particle').textContent = '0';
    document.getElementById('stat-ctors').textContent = this.cache.perFrameAllocs;
  }
  animate() {
    requestAnimationFrame(() => this.animate());
    const deltaTime = Math.min(0.1, this.controls.autoRotate ? 0.016 : 0.016);
    // Play time slider
    if (this.playing) {
      // Advance time based on speed — use accumulated delta
      if (!this._playAccum) this._playAccum = 0;
      this._playAccum += deltaTime * this.playSpeed * 0.5; // 0.5 = seconds per time step at 1x
      while (this._playAccum >= 1) {
        this._playAccum -= 1;
        const next = (this.currentTimeIdx + 1) % 24;
        this.switchToTime(next);
      }
    }
    this.controls.update();
    // Update particles with current terrain height data
    this.particleSystem.update(deltaTime, (wx, wz) => this.getHeightAt(wx, wz));
    // Clear per-frame caches
    this.cache.clearTransforms();
    // Diagnostics update (throttled internally)
    this.updateDiagnostics(deltaTime);
    this.renderer.render(this.scene, this.camera);
  }
}
// Boot
const app = new TerrainExplorer();
console.log('3D Data Terrain Explorer ready');
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan, space=play, arrows=time, R=reset, A=autorotate');
console.log('Terrain cache slots:', app.cache.terrainCache.size, '/ 24');
</script>
</body>
</html>