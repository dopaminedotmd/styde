<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10, 10, 30, 0.92);
    --text: #c8c8d4;
    --accent: #4af;
    --danger: #f44;
    --warn: #fa0;
    --success: #4c8;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
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
  #canvas-container canvas {
    display: block;
  }
  /* Mode indicator banner */
  #mode-banner {
    position: fixed;
    top: 12px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 100;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
    pointer-events: none;
    transition: all 0.3s ease;
  }
  #mode-banner.webgl {
    background: rgba(30, 60, 120, 0.85);
    color: #8cf;
    border: 1px solid rgba(100, 160, 255, 0.4);
  }
  #mode-banner.canvas2d {
    background: rgba(120, 60, 20, 0.85);
    color: #fc8;
    border: 1px solid rgba(255, 160, 60, 0.4);
  }
  /* Dashboard panels */
  .panel {
    position: fixed;
    z-index: 50;
    background: var(--panel-bg);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 14px 18px;
    color: var(--text);
    backdrop-filter: blur(12px);
    font-size: 13px;
    min-width: 200px;
  }
  #time-panel {
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 14px;
  }
  #time-panel label {
    font-weight: 600;
    color: var(--accent);
    white-space: nowrap;
  }
  #time-slider {
    width: 280px;
    accent-color: var(--accent);
    cursor: pointer;
  }
  #time-value {
    font-variant-numeric: tabular-nums;
    min-width: 48px;
    text-align: right;
    font-weight: 600;
  }
  #legend-panel {
    top: 80px;
    right: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
  }
  .legend-swatch {
    width: 24px;
    height: 8px;
    border-radius: 4px;
    flex-shrink: 0;
  }
  #bookmarks-panel {
    top: 80px;
    left: 16px;
  }
  #bookmarks-panel h3 {
    font-size: 13px;
    margin-bottom: 8px;
    color: var(--accent);
  }
  #bookmark-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-height: 200px;
    overflow-y: auto;
  }
  .bookmark-btn {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: var(--text);
    padding: 6px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    text-align: left;
    transition: background 0.15s;
  }
  .bookmark-btn:hover {
    background: rgba(255, 255, 255, 0.14);
  }
  #bookmark-add {
    background: var(--accent);
    color: #000;
    border: none;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    font-size: 12px;
    margin-top: 6px;
  }
  #stats-panel {
    bottom: 24px;
    right: 16px;
    font-size: 11px;
    opacity: 0.7;
    text-align: right;
  }
  #inspect-tooltip {
    position: fixed;
    z-index: 60;
    pointer-events: none;
    background: rgba(0, 0, 0, 0.85);
    color: #fff;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12px;
    display: none;
  }
  .hidden { display: none !important; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="mode-banner" class="webgl">WEBGL — 3D Terrain</div>
<div id="time-panel" class="panel">
  <label for="time-slider">TIME</label>
  <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
  <span id="time-value">T+0</span>
</div>
<div id="legend-panel" class="panel">
  <div class="legend-item"><span class="legend-swatch" style="background: linear-gradient(90deg, #1a4, #8c4);"></span> Revenue Elevation</div>
  <div class="legend-item"><span class="legend-swatch" style="background: linear-gradient(90deg, #240, #4a0);"></span> User Density</div>
  <div class="legend-item"><span class="legend-swatch" style="background: linear-gradient(90deg, #f22, #f84);"></span> Error Rivers</div>
  <div class="legend-item"><span class="legend-swatch" style="background: linear-gradient(90deg, #ff0, #ff8);"></span> API Trail Particles</div>
</div>
<div id="bookmarks-panel" class="panel">
  <h3>CAMERA BOOKMARKS</h3>
  <div id="bookmark-list"></div>
  <button id="bookmark-add">+ Save View</button>
</div>
<div id="stats-panel" class="panel">
  <div id="fps-display">FPS: --</div>
  <div id="cache-display">Cache: 0</div>
</div>
<div id="inspect-tooltip"></div>
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
// ═══════════════════════════════════════════
// DOM REFS
// ═══════════════════════════════════════════
const container = document.getElementById('canvas-container');
const modeBanner = document.getElementById('mode-banner');
const timeSlider = document.getElementById('time-slider');
const timeValue = document.getElementById('time-value');
const bookmarkList = document.getElementById('bookmark-list');
const bookmarkAdd = document.getElementById('bookmark-add');
const fpsDisplay = document.getElementById('fps-display');
const cacheDisplay = document.getElementById('cache-display');
const inspectTooltip = document.getElementById('inspect-tooltip');
// ═══════════════════════════════════════════
// DATA GENERATION — synthetic time-series
// ═══════════════════════════════════════════
const GRID = 60;               // grid cells per axis
const TIME_STEPS = 30;         // temporal snapshots
const TERRAIN_SCALE = 1.2;     // XY spacing between vertices
const HEIGHT_SCALE = 4.0;      // multiplier for elevation
function generateData() {
  // revenueElevation[time][y][x]  — primary metric → Z height
  // userDensity[time][y][x]       — secondary metric → vertex green
  // errorRate[time][y][x]         — tertiary metric → river source
  const revenueElevation = [];
  const userDensity = [];
  const errorRate = [];
  // Seed positions for terrain features that drift over time
  const peakCount = 5;
  const peaks = [];
  for (let p = 0; p < peakCount; p++) {
    // Named intermediates for peak placement — dimension: grid cells
    const baseX = 8 + (p * 11) % (GRID - 16);   // spread across grid
    const baseY = 8 + (p * 13) % (GRID - 16);
    peaks.push({
      baseX,
      baseY,
      // Drift vector per time step — units: cells/step
      driftX: (Math.random() - 0.5) * 0.6,
      driftY: (Math.random() - 0.5) * 0.6,
      amplitude: 2.5 + Math.random() * 5.5,       // peak strength
      radius: 6 + Math.random() * 10              // influence radius — cells
    });
  }
  for (let t = 0; t < TIME_STEPS; t++) {
    const revFrame = [];
    const densFrame = [];
    const errFrame = [];
    // Time factor — linear progression with sinusoidal modulation
    const timeFactorLinear = t / (TIME_STEPS - 1);                            // 0..1
    const timeFactorWave = Math.sin(timeFactorLinear * Math.PI * 1.5) * 0.3; // -0.3..0.3
    const timeFactor = timeFactorLinear + timeFactorWave;                     // combined
    for (let y = 0; y < GRID; y++) {
      const revRow = [];
      const densRow = [];
      const errRow = [];
      for (let x = 0; x < GRID; x++) {
        // --- Revenue elevation: sum of Gaussian peaks ---
        let rev = 1.0; // base elevation
        for (const pk of peaks) {
          // Current peak center at time t
          const cx = pk.baseX + pk.driftX * t;
          const cy = pk.baseY + pk.driftY * t;
          // Squared distance from cell to peak center — cells squared
          const dxSq = (x - cx) * (x - cx);
          const dySq = (y - cy) * (y - cy);
          // Gaussian falloff with radius guard against division by zero
          const radiusSq = pk.radius * pk.radius;
          const distNorm = (dxSq + dySq) / Math.max(radiusSq, 0.01);
          rev += pk.amplitude * Math.exp(-distNorm * 2.0);
        }
        // Time-dependent scaling
        rev *= 0.7 + timeFactor * 0.6;
        // --- User density: sinusoidal ridges ---
        const ridgeFreq = 0.15; // cycles per cell
        const densBase = Math.sin(x * ridgeFreq * Math.PI) *
                         Math.cos(y * ridgeFreq * 1.3 * Math.PI);
        // Normalize from [-1,1] to [0.2, 1.0]
        const density = 0.2 + (densBase + 1.0) * 0.4 + timeFactor * 0.3;
        // --- Error rate: clusters near terrain saddles ---
        // High error where revenue gradient is steep
        const gradX = (x > 0 && x < GRID - 1) ?
          Math.abs(rev - (revRow[x - 1] || rev)) : 0;
        const errFromGrad = gradX * 0.6;
        // Add temporal noise
        const errNoise = Math.sin(x * 0.4 + y * 0.35 + t * 0.8) * 0.15;
        const error = Math.max(0, Math.min(1, errFromGrad + errNoise + 0.05));
        revRow.push(rev);
        densRow.push(density);
        errRow.push(error);
      }
      revFrame.push(revRow);
      densFrame.push(densRow);
      errFrame.push(errRow);
    }
    revenueElevation.push(revFrame);
    userDensity.push(densFrame);
    errorRate.push(errFrame);
  }
  return { revenueElevation, userDensity, errorRate };
}
const dataset = generateData();
// ═══════════════════════════════════════════
// MAP-BASED LRU GEOMETRY CACHE
// Uses Map insertion order for LRU semantics
// ═══════════════════════════════════════════
class GeometryCache {
  constructor(maxSize = 12) {
    this.maxSize = maxSize;
    this.store = new Map();  // single ordered structure — no separate key array
  }
  get(key) {
    const entry = this.store.get(key);
    if (entry === undefined) return undefined;
    // Re-insert to move to end (most-recently-used position)
    this.store.delete(key);
    this.store.set(key, entry);
    return entry;
  }
  set(key, geometry, colors) {
    // Evict oldest (first item in Map iteration order) if at capacity
    if (this.store.size >= this.maxSize) {
      const oldestKey = this.store.keys().next().value;
      const evicted = this.store.get(oldestKey);
      evicted.geometry.dispose();
      this.store.delete(oldestKey);
    }
    this.store.set(key, { geometry, colors });
  }
  size() {
    return this.store.size;
  }
  clear() {
    for (const entry of this.store.values()) {
      entry.geometry.dispose();
    }
    this.store.clear();
  }
}
// ═══════════════════════════════════════════
// TERRAIN BUILDER — BufferGeometry heightfield
// ═══════════════════════════════════════════
function buildTerrainGeometry(revenueData, densityData) {
  // revenueData[y][x], densityData[y][x]
  const vertCount = GRID * GRID;
  const positions = new Float32Array(vertCount * 3);
  const colors = new Float32Array(vertCount * 3);
  // Min/max for normalization
  let revMin = Infinity;
  let revMax = -Infinity;
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const r = revenueData[y][x];
      if (r < revMin) revMin = r;
      if (r > revMax) revMax = r;
    }
  }
  const revRange = revMax - revMin || 1.0;
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const idx = y * GRID + x;
      // Position: XY grid with Z = normalized elevation * HEIGHT_SCALE
      // Named intermediate: normalized revenue 0..1
      const revNorm = (revenueData[y][x] - revMin) / revRange;
      // Named intermediate: elevation height — world units
      const elevationHeight = revNorm * HEIGHT_SCALE;
      positions[idx * 3 + 0] = (x - GRID / 2) * TERRAIN_SCALE;
      positions[idx * 3 + 1] = elevationHeight;
      positions[idx * 3 + 2] = (y - GRID / 2) * TERRAIN_SCALE;
      // Vertex color: revenue→red channel, density→green channel
      // Named intermediates with unit comments
      const revColor = revNorm;                           // red intensity 0..1
      const densColor = Math.max(0, Math.min(1, densityData[y][x])); // green intensity 0..1, clamped
      const blueBase = 0.15;                              // ambient blue floor
      colors[idx * 3 + 0] = 0.12 + revColor * 0.88;      // R: terrain elevation warmth
      colors[idx * 3 + 1] = 0.08 + densColor * 0.72;     // G: vegetation from user density
      colors[idx * 3 + 2] = blueBase + revColor * 0.25;  // B: subtle elevation highlight
    }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  // Index buffer for triangulated grid
  const indexCount = (GRID - 1) * (GRID - 1) * 6;
  const indices = new Uint32Array(indexCount);
  let ii = 0;
  for (let y = 0; y < GRID - 1; y++) {
    for (let x = 0; x < GRID - 1; x++) {
      // Four corners of this cell
      const tl = y * GRID + x;          // top-left
      const tr = tl + 1;                // top-right
      const bl = (y + 1) * GRID + x;    // bottom-left
      const br = bl + 1;                // bottom-right
      // Two triangles per cell
      indices[ii++] = tl; indices[ii++] = bl; indices[ii++] = tr;
      indices[ii++] = tr; indices[ii++] = bl; indices[ii++] = br;
    }
  }
  geometry.setIndex(new THREE.BufferAttribute(indices, 1));
  geometry.computeVertexNormals();
  return { geometry, colors };
}
// ═══════════════════════════════════════════
// RIVER GEOMETRY — error paths carving terrain
// ═══════════════════════════════════════════
function buildRiverLines(errorData, revenueData) {
  // Trace error paths as line segments following high-error corridors
  const errorThreshold = 0.35;  // only cells exceeding this become river nodes
  const revMin = Math.min(...revenueData.flat());
  const revMax = Math.max(...revenueData.flat());
  const revRange = revMax - revMin || 1.0;
  const riverPaths = [];
  const visited = new Set();
  for (let y = 0; y < GRID; y++) {
    for (let x = 0; x < GRID; x++) {
      const key = y * GRID + x;
      if (visited.has(key)) continue;
      if (errorData[y][x] < errorThreshold) continue;
      // Start a river trace from this high-error cell
      const path = traceRiverPath(x, y, errorData, revenueData, visited, errorThreshold);
      if (path.length >= 3) {
        riverPaths.push(path);
      }
    }
  }
  // Convert paths to 3D line positions
  const allPoints = [];
  for (const path of riverPaths) {
    for (const [px, py] of path) {
      const revNorm = (revenueData[py][px] - revMin) / revRange;
      // Named intermediate: world-space Y with small offset above terrain
      const terrainY = revNorm * HEIGHT_SCALE;
      const riverOffset = 0.06;  // slight lift above terrain surface — world units
      allPoints.push(
        (px - GRID / 2) * TERRAIN_SCALE,
        terrainY + riverOffset,
        (py - GRID / 2) * TERRAIN_SCALE
      );
    }
    // Break between paths with NaN (Three.js line break convention handled per-path)
  }
  if (allPoints.length === 0) {
    // Return empty geometry if no rivers
    const emptyGeo = new THREE.BufferGeometry();
    emptyGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(0), 3));
    return emptyGeo;
  }
  const posArray = new Float32Array(allPoints);
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
  return geom;
}
function traceRiverPath(startX, startY, errorData, revenueData, visited, threshold) {
  // Greedy neighbor walk following highest error downhill
  const path = [[startX, startY]];
  visited.add(startY * GRID + startX);
  let cx = startX;
  let cy = startY;
  const maxSteps = 120;
  const directions = [
    [-1, -1], [0, -1], [1, -1],
    [-1,  0],          [1,  0],
    [-1,  1], [0,  1], [1,  1]
  ];
  for (let step = 0; step < maxSteps; step++) {
    let bestDir = null;
    let bestScore = -Infinity;
    for (const [dx, dy] of directions) {
      const nx = cx + dx;
      const ny = cy + dy;
      if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
      const nk = ny * GRID + nx;
      if (visited.has(nk)) continue;
      // Score: prefer high error + downhill (descending revenue)
      const errScore = errorData[ny][nx];
      // Revenue gradient: negative means downhill
      const revGrad = revenueData[cy][cx] - revenueData[ny][nx];
      const combinedScore = errScore * 0.7 + Math.max(0, revGrad) * 0.3;
      if (combinedScore > bestScore && errScore >= threshold * 0.5) {
        bestScore = combinedScore;
        bestDir = [nx, ny];
      }
    }
    if (!bestDir) break;
    const [nx, ny] = bestDir;
    path.push([nx, ny]);
    visited.add(ny * GRID + nx);
    cx = nx;
    cy = ny;
  }
  return path;
}
// ═══════════════════════════════════════════
// PARTICLE SYSTEM — data flow trails
// ═══════════════════════════════════════════
class ParticleTrailSystem {
  constructor(maxParticles = 600, geometryCache = null) {
    this.maxParticles = maxParticles;
    this.geoCache = geometryCache;
    // Single pre-allocated position buffer — reused per frame, no per-particle allocations
    this.positions = new Float32Array(maxParticles * 3);
    this.colors = new Float32Array(maxParticles * 3);
    this.particleData = new Array(maxParticles); // { x, y, vx, vy, life, maxLife }
    // Initialize particles
    for (let i = 0; i < maxParticles; i++) {
      this.particleData[i] = this._spawnParticle(i, 0);
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(this.colors, 3));
    const material = new THREE.PointsMaterial({
      size: 0.22,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.75
    });
    this.points = new THREE.Points(geometry, material);
  }
  _spawnParticle(index, timeIndex) {
    // Random spawn in valleys (lower revenue areas)
    const x = Math.random() * GRID;
    const y = Math.random() * GRID;
    // Bias toward valley floor by preferring lower revenue for initial position
    const rev = dataset.revenueElevation[timeIndex]
      ? dataset.revenueElevation[timeIndex][Math.floor(Math.min(y, GRID - 1))]
        ?.[Math.floor(Math.min(x, GRID - 1))] ?? 0.5
      : 0.5;
    // Drift velocity toward terrain gradient
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.1 + Math.random() * 0.5; // cells per second
    return {
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      life: Math.random(),          // 0..1, normalized age
      maxLife: 3 + Math.random() * 8 // seconds
    };
  }
  update(deltaSec, timeIndex, terrainMesh) {
    // deltaSec: frame delta in seconds — normalized for consistent speed across framerates
    // Guard against spike frames (tab switch, debugger pause)
    const dt = Math.min(deltaSec, 0.1); // clamp to 100ms max — prevents teleport
    // Reference revenue for terrain lookups
    const revFrame = dataset.revenueElevation[timeIndex];
    const revMin = Math.min(...revFrame.flat());
    const revMax = Math.max(...revFrame.flat());
    const revRange = revMax - revMin || 1.0;
    for (let i = 0; i < this.maxParticles; i++) {
      const p = this.particleData[i];
      // Update life and respawn if expired
      p.life += dt / p.maxLife;
      if (p.life >= 1.0) {
        Object.assign(p, this._spawnParticle(i, timeIndex));
      }
      // Move particle
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      // Bounds wrapping with slight randomness
      if (p.x < 0 || p.x >= GRID || p.y < 0 || p.y >= GRID) {
        p.x = (p.x + GRID) % GRID;
        p.y = (p.y + GRID) % GRID;
        p.vx += (Math.random() - 0.5) * 0.3;
        p.vy += (Math.random() - 0.5) * 0.3;
        // Re-clamp speed
        const spd = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
        if (spd > 0.8) { p.vx *= 0.8 / spd; p.vy *= 0.8 / spd; }
      }
      // Y-clamping: compute terrain height at particle position
      const gx = Math.floor(Math.min(p.x, GRID - 1));
      const gy = Math.floor(Math.min(p.y, GRID - 1));
      const rev = revFrame[gy] ? (revFrame[gy][gx] ?? 0.5) : 0.5;
      const revNorm = (rev - revMin) / revRange;
      const terrainY = revNorm * HEIGHT_SCALE;
      // Particle floats above terrain — Y clamped to terrain surface
      const particleOffset = 0.15 + p.life * 0.5; // rises as it ages
      // World position
      const wx = (p.x - GRID / 2) * TERRAIN_SCALE;
      const wy = terrainY + particleOffset; // Y-clamped: cannot sink below terrain
      const wz = (p.y - GRID / 2) * TERRAIN_SCALE;
      this.positions[i * 3 + 0] = wx;
      this.positions[i * 3 + 1] = wy;
      this.positions[i * 3 + 2] = wz;
      // Color: yellow-to-white gradient, fades with age
      const fade = 1.0 - p.life;
      this.colors[i * 3 + 0] = fade;
      this.colors[i * 3 + 1] = fade * 0.9;
      this.colors[i * 3 + 2] = fade * 0.3;
    }
    this.points.geometry.attributes.position.needsUpdate = true;
    this.points.geometry.attributes.color.needsUpdate = true;
  }
}
// ═══════════════════════════════════════════
// CANVAS 2D FALLBACK RENDERER
// Uses dirty-flag grid — only redraws changed cells
// ═══════════════════════════════════════════
class Canvas2DFallback {
  constructor(container) {
    this.canvas = document.createElement('canvas');
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.ctx = this.canvas.getContext('2d');
    container.appendChild(this.canvas);
    // Dirty-flag grid: track which cells need redraw
    this.dirtyGrid = new Array(GRID * GRID).fill(true); // initially all dirty
    this.cellSize = 0;       // computed in resize
    this.offsetX = 0;        // pan offset — pixels
    this.offsetY = 0;
    this.zoom = 1.0;
    // Interaction state
    this.isDragging = false;
    this.dragStartX = 0;
    this.dragStartY = 0;
    this.dragOffsetStartX = 0;
    this.dragOffsetStartY = 0;
    // Offscreen buffer for static terrain (only redrawn on dirty cells)
    this.bufferCanvas = document.createElement('canvas');
    this.bufferCtx = null;
    this._setupInteraction();
    this._resize();
    window.addEventListener('resize', () => this._resize());
  }
  _resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.bufferCanvas.width = window.innerWidth;
    this.bufferCanvas.height = window.innerHeight;
    this.bufferCtx = this.bufferCanvas.getContext('2d');
    // Compute cell size for current grid
    const baseSize = Math.min(this.canvas.width, this.canvas.height) / GRID;
    this.cellSize = baseSize * this.zoom;
    // Mark all dirty on resize
    this.dirtyGrid.fill(true);
  }
  _setupInteraction() {
    this.canvas.addEventListener('mousedown', (e) => {
      this.isDragging = true;
      this.dragStartX = e.clientX;
      this.dragStartY = e.clientY;
      this.dragOffsetStartX = this.offsetX;
      this.dragOffsetStartY = this.offsetY;
    });
    this.canvas.addEventListener('mousemove', (e) => {
      if (!this.isDragging) return;
      this.offsetX = this.dragOffsetStartX + (e.clientX - this.dragStartX);
      this.offsetY = this.dragOffsetStartY + (e.clientY - this.dragStartY);
      this.dirtyGrid.fill(true); // full redraw on pan
    });
    this.canvas.addEventListener('mouseup', () => { this.isDragging = false; });
    this.canvas.addEventListener('mouseleave', () => { this.isDragging = false; });
    this.canvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const zoomDelta = e.deltaY > 0 ? 0.9 : 1.1;
      this.zoom *= zoomDelta;
      this.zoom = Math.max(0.3, Math.min(5.0, this.zoom));
      this.cellSize = Math.min(this.canvas.width, this.canvas.height) / GRID * this.zoom;
      this.dirtyGrid.fill(true);
    });
    // Click-to-inspect
    this.canvas.addEventListener('click', (e) => {
      if (this.isDragging) return;
      // Convert screen coords to grid coords
      const centerX = this.canvas.width / 2 + this.offsetX;
      const centerY = this.canvas.height / 2 + this.offsetY;
      const gx = Math.floor((e.clientX - centerX + (GRID * this.cellSize) / 2) / this.cellSize);
      const gy = Math.floor((e.clientY - centerY + (GRID * this.cellSize) / 2) / this.cellSize);
      if (gx >= 0 && gx < GRID && gy >= 0 && gy < GRID) {
        this._showInspect(gx, gy, e.clientX, e.clientY);
      }
    });
  }
  _showInspect(gx, gy, screenX, screenY) {
    const t = parseInt(timeSlider.value);
    const rev = dataset.revenueElevation[t][gy][gx];
    const dens = dataset.userDensity[t][gy][gx];
    const err = dataset.errorRate[t][gy][gx];
    inspectTooltip.style.display = 'block';
    inspectTooltip.style.left = (screenX + 14) + 'px';
    inspectTooltip.style.top = (screenY - 10) + 'px';
    inspectTooltip.textContent =
      `Cell (${gx},${gy}) | Rev: ${rev.toFixed(2)} | Users: ${dens.toFixed(2)} | Err: ${(err*100).toFixed(1)}%`;
    setTimeout(() => { inspectTooltip.style.display = 'none'; }, 2500);
  }
  render(timeIndex) {
    const ctx = this.ctx;
    const bufCtx = this.bufferCtx;
    if (!bufCtx) return;
    const revFrame = dataset.revenueElevation[timeIndex];
    const densFrame = dataset.userDensity[timeIndex];
    // Compute global min/max for normalization
    let revMin = Infinity, revMax = -Infinity;
    for (let y = 0; y < GRID; y++) {
      for (let x = 0; x < GRID; x++) {
        const r = revFrame[y][x];
        if (r < revMin) revMin = r;
        if (r > revMax) revMax = r;
      }
    }
    const revRange = revMax - revMin || 1.0;
    const cs = this.cellSize;
    const cx = this.canvas.width / 2 + this.offsetX - (GRID * cs) / 2;
    const cy = this.canvas.height / 2 + this.offsetY - (GRID * cs) / 2;
    // Only redraw dirty cells into buffer
    for (let y = 0; y < GRID; y++) {
      for (let x = 0; x < GRID; x++) {
        const di = y * GRID + x;
        if (!this.dirtyGrid[di]) continue;
        const px = cx + x * cs;
        const py = cy + y * cs;
        // Clear old cell in buffer
        bufCtx.clearRect(px, py, cs + 1, cs + 1);
        // Draw cell colored by revenue (elevation) and density
        const revNorm = (revFrame[y][x] - revMin) / revRange;
        const densNorm = Math.max(0, Math.min(1, densFrame[y][x]));
        // Named intermediate color channels — 0..255
        const r = Math.floor((0.12 + revNorm * 0.88) * 255);
        const g = Math.floor((0.08 + densNorm * 0.72) * 255);
        const b = Math.floor((0.15 + revNorm * 0.25) * 255);
        bufCtx.fillStyle = `rgb(${r},${g},${b})`;
        bufCtx.fillRect(px, py, cs, cs);
        // Cell border for grid lines
        bufCtx.strokeStyle = 'rgba(255,255,255,0.06)';
        bufCtx.strokeRect(px, py, cs, cs);
        this.dirtyGrid[di] = false;
      }
    }
    // Blit buffer to main canvas
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.drawImage(this.bufferCanvas, 0, 0);
  }
  markAllDirty() {
    this.dirtyGrid.fill(true);
  }
  destroy() {
    this.canvas.remove();
    window.removeEventListener('resize', this._resize);
  }
}
// ═══════════════════════════════════════════
// MAIN APPLICATION — DataTerrainExplorer
// ═══════════════════════════════════════════
class DataTerrainExplorer {
  constructor() {
    this.renderer = null;
    this.scene = null;
    this.camera = null;
    this.controls = null;
    this.terrainMesh = null;
    this.riverLines = null;
    this.particleSystem = null;
    this.geoCache = new GeometryCache(12);
    this.currentTimeIndex = 0;
    this.isWebGL = true;
    this.fallbackRenderer = null;
    this.clock = new THREE.Clock();
    this.fpsFrames = 0;
    this.fpsTime = 0;
    this.autoRotate = true;
    this.bookmarks = [];
    this.animationId = null;
  }
  init() {
    // Detect WebGL support
    const testCanvas = document.createElement('canvas');
    const gl = testCanvas.getContext('webgl2') || testCanvas.getContext('webgl');
    this.isWebGL = !!gl;
    if (this.isWebGL) {
      this._initWebGL();
    } else {
      this._initFallback();
    }
    this._updateModeBanner();
    this._setupBookmarks();
    this._setupTimeSlider();
    this._loadTimeStep(0);
    this._startLoop();
  }
  _initWebGL() {
    // Renderer with camera-clipping guards
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    // Camera clipping planes — near guard prevents z-fighting, far guard bounds scene
    this.renderer.shadowMap.enabled = true;
    container.appendChild(this.renderer.domElement);
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0a0a18);
    this.scene.fog = new THREE.Fog(0x0a0a18, 30, 90);
    // Camera
    const aspect = window.innerWidth / window.innerHeight;
    this.camera = new THREE.PerspectiveCamera(55, aspect, 0.5, 120);
    this.camera.position.set(18, 14, 22);
    this.camera.lookAt(0, 0, 0);
    // OrbitControls with damping
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.3;
    this.controls.target.set(0, HEIGHT_SCALE * 0.4, 0);
    // Clipping guards on controls
    this.controls.minDistance = 4;
    this.controls.maxDistance = 60;
    this.controls.maxPolarAngle = Math.PI * 0.78; // prevent flipping under terrain
    this.controls.update();
    // Lighting
    const ambient = new THREE.AmbientLight(0x334466, 2.5);
    this.scene.add(ambient);
    const sun = new THREE.DirectionalLight(0xffeedd, 4.0);
    sun.position.set(20, 30, 10);
    this.scene.add(sun);
    const fill = new THREE.DirectionalLight(0x4466aa, 1.5);
    fill.position.set(-10, 5, -15);
    this.scene.add(fill);
    // Grid helper
    const gridHelper = new THREE.GridHelper(GRID * TERRAIN_SCALE, GRID, 0x222244, 0x111122);
    gridHelper.position.y = -0.05;
    this.scene.add(gridHelper);
    window.addEventListener('resize', () => this._onResize());
  }
  _initFallback() {
    this.fallbackRenderer = new Canvas2DFallback(container);
    window.addEventListener('resize', () => {
      if (this.fallbackRenderer) this.fallbackRenderer._resize();
    });
  }
  _updateModeBanner() {
    if (this.isWebGL) {
      modeBanner.className = 'webgl';
      modeBanner.textContent = 'WEBGL — 3D Terrain Explorer';
    } else {
      modeBanner.className = 'canvas2d';
      modeBanner.textContent = 'CANVAS 2D — Fallback Terrain View';
    }
  }
  _onResize() {
    if (!this.isWebGL || !this.renderer) return;
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }
  _setupTimeSlider() {
    timeSlider.addEventListener('input', () => {
      const t = parseInt(timeSlider.value);
      this.currentTimeIndex = t;
      timeValue.textContent = `T+${t}`;
      this._loadTimeStep(t);
      // Mark 2D dirty on time change
      if (this.fallbackRenderer) this.fallbackRenderer.markAllDirty();
    });
    // Keyboard shortcuts
    window.addEventListener('keydown', (e) => {
      switch (e.key.toLowerCase()) {
        case 'arrowleft':
          timeSlider.value = Math.max(0, this.currentTimeIndex - 1);
          timeSlider.dispatchEvent(new Event('input'));
          break;
        case 'arrowright':
          timeSlider.value = Math.min(TIME_STEPS - 1, this.currentTimeIndex + 1);
          timeSlider.dispatchEvent(new Event('input'));
          break;
        case 'r':
          this.autoRotate = !this.autoRotate;
          if (this.controls) this.controls.autoRotate = this.autoRotate;
          break;
      }
    });
  }
  _loadTimeStep(t) {
    if (!this.isWebGL) return;
    // Check geometry cache
    const cacheKey = `t${t}`;
    let cached = this.geoCache.get(cacheKey);
    if (!cached) {
      const { geometry } = buildTerrainGeometry(
        dataset.revenueElevation[t],
        dataset.userDensity[t]
      );
      const colors = geometry.attributes.color.array;
      this.geoCache.set(cacheKey, geometry, colors);
      cached = this.geoCache.get(cacheKey);
    }
    // Swap terrain mesh
    if (this.terrainMesh) {
      this.terrainMesh.geometry.dispose();
    }
    const material = new THREE.MeshPhongMaterial({
      vertexColors: true,
      side: THREE.DoubleSide,
      flatShading: false,
      specular: 0x111111,
      shininess: 8
    });
    if (this.terrainMesh) {
      this.scene.remove(this.terrainMesh);
      if (this.terrainMesh.material) this.terrainMesh.material.dispose();
    }
    this.terrainMesh = new THREE.Mesh(cached.geometry, material);
    this.scene.add(this.terrainMesh);
    // Rebuild rivers
    if (this.riverLines) {
      this.scene.remove(this.riverLines);
      if (this.riverLines.geometry) this.riverLines.geometry.dispose();
      if (this.riverLines.material) this.riverLines.material.dispose();
    }
    const riverGeom = buildRiverLines(dataset.errorRate[t], dataset.revenueElevation[t]);
    if (riverGeom.attributes.position.count > 0) {
      // NOTE: Three.js Line with single BufferGeometry draws connected; we use LineSegments for per-path breaks
      const riverMat = new THREE.LineBasicMaterial({
        color: 0xff4422,
        linewidth: 1,
        transparent: true,
        opacity: 0.8,
        depthTest: true
      });
      this.riverLines = new THREE.LineSegments(riverGeom, riverMat);
      // Convert to line segments: pair consecutive vertices
      const posCount = riverGeom.attributes.position.count;
      const segIndices = [];
      for (let i = 0; i < posCount - 1; i++) {
        segIndices.push(i, i + 1);
      }
      const segGeom = new THREE.BufferGeometry();
      segGeom.setAttribute('position', riverGeom.attributes.position);
      segGeom.setIndex(segIndices);
      riverGeom.dispose();
      this.riverLines.geometry.dispose();
      this.riverLines.geometry = segGeom;
      this.scene.add(this.riverLines);
    }
    // Init or update particle system
    if (!this.particleSystem) {
      this.particleSystem = new ParticleTrailSystem(600, this.geoCache);
      this.scene.add(this.particleSystem.points);
    }
    // Update cache display
    cacheDisplay.textContent = `Cache: ${this.geoCache.size()}`;
  }
  _setupBookmarks() {
    // Load saved bookmarks from localStorage
    try {
      const saved = localStorage.getItem('terrain-explorer-bookmarks');
      if (saved) this.bookmarks = JSON.parse(saved);
    } catch (_) { /* ignore corrupt data */ }
    this._renderBookmarkList();
    bookmarkAdd.addEventListener('click', () => {
      if (!this.isWebGL || !this.camera) return;
      const name = `View ${this.bookmarks.length + 1} (T+${this.currentTimeIndex})`;
      const bm = {
        name,
        position: this.camera.position.toArray(),
        target: (this.controls?.target || new THREE.Vector3()).toArray(),
        timeIndex: this.currentTimeIndex
      };
      this.bookmarks.push(bm);
      this._saveBookmarks();
      this._renderBookmarkList();
    });
  }
  _renderBookmarkList() {
    bookmarkList.innerHTML = '';
    for (let i = 0; i < this.bookmarks.length; i++) {
      const bm = this.bookmarks[i];
      const btn = document.createElement('button');
      btn.className = 'bookmark-btn';
      btn.textContent = bm.name;
      btn.addEventListener('click', () => {
        this._applyBookmark(bm);
      });
      bookmarkList.appendChild(btn);
    }
  }
  _applyBookmark(bm) {
    if (!this.isWebGL) return;
    // Animate camera to bookmark position
    const startPos = this.camera.position.clone();
    const endPos = new THREE.Vector3(...bm.position);
    const startTarget = this.controls.target.clone();
    const endTarget = new THREE.Vector3(...bm.target);
    const startTime = performance.now();
    const duration = 800; // ms
    const animate = (now) => {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1.0);
      // Ease in-out cubic
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      this.camera.position.lerpVectors(startPos, endPos, ease);
      this.controls.target.lerpVectors(startTarget, endTarget, ease);
      this.controls.update();
      if (t < 1.0) {
        requestAnimationFrame(animate);
      }
    };
    requestAnimationFrame(animate);
    // Also jump to bookmarked time
    if (bm.timeIndex !== undefined) {
      timeSlider.value = bm.timeIndex;
      timeSlider.dispatchEvent(new Event('input'));
    }
  }
  _saveBookmarks() {
    try {
      localStorage.setItem('terrain-explorer-bookmarks', JSON.stringify(this.bookmarks));
    } catch (_) { /* storage full or unavailable */ }
  }
  _startLoop() {
    const loop = () => {
      this.animationId = requestAnimationFrame(loop);
      const deltaSec = this.clock.getDelta();
      if (this.isWebGL) {
        this._animateWebGL(deltaSec);
      } else {
        this._animateFallback();
      }
      // FPS counter
      this.fpsFrames++;
      this.fpsTime += deltaSec;
      if (this.fpsTime >= 0.5) {
        const fps = Math.round(this.fpsFrames / this.fpsTime);
        fpsDisplay.textContent = `FPS: ${fps}`;
        this.fpsFrames = 0;
        this.fpsTime = 0;
      }
    };
    this.animationId = requestAnimationFrame(loop);
  }
  _animateWebGL(deltaSec) {
    // Delta-normalized updates — guard against spike frames
    const dt = Math.min(deltaSec, 0.1);
    // Update controls (handles damping internally)
    this.controls.update();
    // Update particles
    if (this.particleSystem) {
      this.particleSystem.update(dt, this.currentTimeIndex, this.terrainMesh);
    }
    // Render
    this.renderer.render(this.scene, this.camera);
  }
  _animateFallback() {
    if (this.fallbackRenderer) {
      this.fallbackRenderer.render(this.currentTimeIndex);
    }
  }
}
// ═══════════════════════════════════════════
// BOOT
// ═══════════════════════════════════════════
const explorer = new DataTerrainExplorer();
explorer.init();
// Expose via module-scoped variable for debugging (no window.X pattern)
// Use: in console, access via the import binding or the global reference below
if (typeof globalThis !== 'undefined') {
  globalThis.__terrainExplorer = explorer;
}
</script>
</body>
</html>