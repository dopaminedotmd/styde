<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; }
  canvas { display: block; }
  #overlay {
    position: fixed; top: 16px; left: 16px; z-index: 10;
    display: flex; flex-direction: column; gap: 8px;
    pointer-events: none;
  }
  #overlay > * { pointer-events: auto; }
  .panel {
    background: rgba(10, 10, 24, 0.85); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12); border-radius: 10px;
    padding: 14px 18px; color: #ccc; min-width: 260px;
  }
  .panel h3 { font-size: 13px; text-transform: uppercase; letter-spacing: 1.2px;
    color: #8af; margin-bottom: 10px; font-weight: 600; }
  input[type=range] { width: 100%; accent-color: #4af; margin: 4px 0; }
  button {
    background: rgba(68, 170, 255, 0.15); border: 1px solid rgba(68, 170, 255, 0.35);
    color: #adf; padding: 7px 14px; border-radius: 6px; cursor: pointer;
    font-size: 12px; letter-spacing: 0.5px; transition: all 0.2s;
    margin: 2px;
  }
  button:hover { background: rgba(68, 170, 255, 0.28); border-color: rgba(68, 170, 255, 0.6); }
  button.active { background: rgba(68, 170, 255, 0.35); border-color: #4af; color: #fff; }
  button.bookmark-btn { font-family: monospace; font-size: 11px; padding: 5px 10px; }
  .metric-row { display: flex; justify-content: space-between; font-size: 11px;
    padding: 3px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
  .metric-row .val { color: #8cf; font-family: monospace; }
  #diag { font-family: 'Cascadia Code', 'Fira Code', monospace; font-size: 10px;
    line-height: 1.5; color: #7a7; }
  #data-url { background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2);
    color: #ccc; padding: 6px 10px; border-radius: 5px; width: 100%; font-size: 11px; }
  #load-btn { width: 100%; margin-top: 6px; }
  .row { display: flex; gap: 8px; align-items: center; }
  label { font-size: 11px; color: #888; }
  .tick-label { display: flex; justify-content: space-between; font-size: 10px; color: #666; }
</style>
</head>
<body>
<div id="overlay">
  <div class="panel">
    <h3>Time Dimension</h3>
    <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
    <div class="tick-label"><span>00:00</span><span id="time-label">12:00</span><span>23:00</span></div>
    <div class="row" style="margin-top:8px">
      <button id="play-btn">Play</button>
      <button id="auto-rotate-btn">Auto-Rotate</button>
    </div>
  </div>
  <div class="panel">
    <h3>Camera Bookmarks</h3>
    <div class="row" style="flex-wrap:wrap" id="bookmark-row">
      <button class="bookmark-btn" data-key="1">1</button>
      <button class="bookmark-btn" data-key="2">2</button>
      <button class="bookmark-btn" data-key="3">3</button>
      <button class="bookmark-btn" data-key="4">4</button>
      <button class="bookmark-btn" data-key="5">5</button>
    </div>
    <div class="row" style="margin-top:6px">
      <button id="save-bm">Save Ctrl+1-5</button>
      <button id="clear-bm">Clear All</button>
    </div>
  </div>
  <div class="panel">
    <h3>Data Source</h3>
    <input type="text" id="data-url" placeholder="Paste URL to heightmap JSON/GeoJSON...">
    <button id="load-btn">Load External Data</button>
    <div style="margin-top:6px;font-size:10px;color:#555">
      Presets:
      <button class="preset-btn" data-preset="alps">Alps</button>
      <button class="preset-btn" data-preset="canyon">Canyon</button>
      <button class="preset-btn" data-preset="islands">Islands</button>
    </div>
  </div>
  <div class="panel" id="diag-panel" style="max-height:180px;overflow-y:auto">
    <h3>Cache Diagnostics</h3>
    <div id="diag">initializing...</div>
  </div>
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
// ─── Constants ──────────────────────────────────────────────────
const GRID = 128;
const GRID_SPACING = 0.4;
const TERRAIN_SIZE = GRID * GRID_SPACING;
const PEAK_HEIGHT = 8;
const PARTICLE_COUNT = 600;
const TIME_SLICES = 24;
const RIVER_SEGMENTS = 80;
// ─── DOM refs ────────────────────────────────────────────────────
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const playBtn = document.getElementById('play-btn');
const autoRotateBtn = document.getElementById('auto-rotate-btn');
const diagEl = document.getElementById('diag');
const bookmarkRow = document.getElementById('bookmark-row');
// ─── Scene setup ─────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.FogExp2(0x0a0a18, 0.00025);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.8, 200);
camera.position.set(18, 14, 22);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);
// ─── Lighting ────────────────────────────────────────────────────
const ambient = new THREE.AmbientLight(0x1a1a3a, 1.4);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(20, 30, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 120;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
sun.shadow.bias = -0.0002;
scene.add(sun);
const rim = new THREE.DirectionalLight(0x4466cc, 1.2);
rim.position.set(-10, -2, -5);
scene.add(rim);
// ─── Ground plane ────────────────────────────────────────────────
const groundGeo = new THREE.PlaneGeometry(TERRAIN_SIZE * 2.5, TERRAIN_SIZE * 2.5);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x0a0a1a, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.2;
ground.receiveShadow = true;
scene.add(ground);
// ─── Grid helper ─────────────────────────────────────────────────
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2, 32, 24, 64, 0x222244, 0x111122);
gridHelper.position.y = -0.15;
scene.add(gridHelper);
// ─── Controls ────────────────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.12;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 3, 0);
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// ═══════════════════════════════════════════════════════════════════
// DATA ADAPTER LAYER
// ═══════════════════════════════════════════════════════════════════
// Supports: synthetic Perlin noise, procedural presets, URL-loaded
// heightmap JSON, and GeoJSON elevation tiles.
class DataAdapter {
  constructor() {
    this.slices = [];       // Array of {height:[], revenue:[], density:[], errors:[]}
    this.currentPreset = 'synthetic';
  }
  // Generate synthetic time-series data with Perlin-like coherent noise
  generateSynthetic() {
    this.slices = [];
    // Pre-seed a static noise field shared across time slices for coherence
    const noiseSeed = this._buildNoiseGrid(GRID + 1, 7);
    for (let t = 0; t < TIME_SLICES; t++) {
      const phase = t / TIME_SLICES;
      const height = new Float32Array((GRID + 1) * (GRID + 1));
      const density = new Float32Array((GRID + 1) * (GRID + 1));
      const errorMask = new Float32Array((GRID + 1) * (GRID + 1));
      for (let iy = 0; iy <= GRID; iy++) {
        for (let ix = 0; ix <= GRID; ix++) {
          const idx = iy * (GRID + 1) + ix;
          // Combine base noise with time-varying sinusoidal modulation
          const base = noiseSeed[idx];
          const wave = Math.sin(phase * Math.PI * 2 + ix * 0.15) *
                       Math.cos(phase * Math.PI * 1.3 + iy * 0.12);
          const peakFactor = 0.5 + 0.5 * Math.sin(phase * Math.PI * 0.7);
          height[idx] = (base * 0.7 + wave * 0.3) * peakFactor;
          // Density: correlated with height but independent phase
          density[idx] = 0.3 + 0.7 * (
            0.5 + 0.5 * Math.sin(ix * 0.1 + phase * 2.5) *
            Math.cos(iy * 0.13 - phase * 1.8)
          );
          // Error mask: sparse spike regions
          const spike = Math.abs(Math.sin(ix * 0.4 + t * 0.9) *
                                 Math.cos(iy * 0.35 + t * 0.7));
          errorMask[idx] = spike > 0.78 ? (spike - 0.78) * 4.5 : 0;
        }
      }
      this.slices.push({ height, density, errorMask });
    }
    this._extractRiverPaths();
    this.currentPreset = 'synthetic';
  }
  // Procedural presets for recognizable terrain shapes
  generatePreset(name) {
    this.slices = [];
    for (let t = 0; t < TIME_SLICES; t++) {
      const phase = t / TIME_SLICES;
      const height = new Float32Array((GRID + 1) * (GRID + 1));
      const density = new Float32Array((GRID + 1) * (GRID + 1));
      const errorMask = new Float32Array((GRID + 1) * (GRID + 1));
      for (let iy = 0; iy <= GRID; iy++) {
        for (let ix = 0; ix <= GRID; ix++) {
          const idx = iy * (GRID + 1) + ix;
          const nx = (ix / GRID - 0.5) * 2;
          const ny = (iy / GRID - 0.5) * 2;
          let h = 0;
          if (name === 'alps') {
            // Ridge line with peaks
            const ridge = Math.exp(-ny * ny * 1.5) * (0.6 + 0.4 * Math.sin(nx * 5));
            h = ridge * (0.7 + 0.3 * Math.sin(phase * Math.PI * 2));
          } else if (name === 'canyon') {
            // Deep canyon carved through a plateau
            const plateau = 0.5 + 0.1 * Math.sin(nx * 3 + ny * 2);
            const canyon = 1 - Math.exp(-ny * ny * 12) * (0.85 + 0.08 * Math.sin(nx * 8));
            h = plateau * canyon * (0.8 + 0.2 * Math.cos(phase * Math.PI * 1.5));
          } else if (name === 'islands') {
            // Archipelago of peaks
            const d1 = Math.sqrt((nx - 0.3) ** 2 + (ny - 0.2) ** 2);
            const d2 = Math.sqrt((nx + 0.4) ** 2 + (ny + 0.3) ** 2);
            const d3 = Math.sqrt((nx + 0.1) ** 2 + (ny - 0.4) ** 2);
            h = Math.max(
              Math.exp(-d1 * d1 * 6) * 0.9,
              Math.exp(-d2 * d2 * 5) * 0.7,
              Math.exp(-d3 * d3 * 7) * 0.6
            );
            h *= 0.7 + 0.3 * Math.sin(phase * Math.PI * 1.8);
          }
          height[idx] = h;
          density[idx] = 0.25 + 0.75 * h;
          const spike = Math.abs(Math.sin(nx * 8 + t * 0.5) * Math.cos(ny * 7 + t * 0.6));
          errorMask[idx] = spike > 0.82 ? (spike - 0.82) * 4 : 0;
        }
      }
      this.slices.push({ height, density, errorMask });
    }
    this._extractRiverPaths();
    this.currentPreset = name;
  }
  // Load external heightmap from URL (expects JSON with slices or single grid)
  async loadFromURL(url) {
    try {
      const resp = await fetch(url);
      const raw = await resp.json();
      this.slices = this._parseExternalData(raw);
      this._extractRiverPaths();
      this.currentPreset = 'external';
      return true;
    } catch (e) {
      console.error('Failed to load external data:', e);
      return false;
    }
  }
  // Parse external data format: {slices: [{height:number[][]}, ...]} or {grid:number[][]}
  _parseExternalData(raw) {
    const slices = [];
    const sourceSlices = raw.slices || [raw];
    for (const src of sourceSlices) {
      const grid = src.height || src.grid || src.elevation || [];
      const height = new Float32Array((GRID + 1) * (GRID + 1));
      const density = new Float32Array((GRID + 1) * (GRID + 1));
      const errorMask = new Float32Array((GRID + 1) * (GRID + 1));
      for (let iy = 0; iy <= GRID; iy++) {
        for (let ix = 0; ix <= GRID; ix++) {
          const idx = iy * (GRID + 1) + ix;
          const row = grid[iy] || [];
          height[idx] = (row[ix] || 0);
        }
      }
      // Normalize height to 0-1 range if raw values exceed 1
      let maxH = 0;
      for (let i = 0; i < height.length; i++) maxH = Math.max(maxH, height[i]);
      if (maxH > 1.5) {
        for (let i = 0; i < height.length; i++) height[i] /= maxH;
      }
      // Derive density from height if not provided
      const srcDensity = src.density || src.vegetation || [];
      for (let iy = 0; iy <= GRID; iy++) {
        for (let ix = 0; ix <= GRID; ix++) {
          const idx = iy * (GRID + 1) + ix;
          const row = srcDensity[iy] || [];
          density[idx] = row[ix] !== undefined ? row[ix] : height[idx] * 0.8;
        }
      }
      const srcErrors = src.errors || src.anomalies || [];
      for (let iy = 0; iy <= GRID; iy++) {
        for (let ix = 0; ix <= GRID; ix++) {
          const idx = iy * (GRID + 1) + ix;
          const row = srcErrors[iy] || [];
          errorMask[idx] = row[ix] || 0;
        }
      }
      slices.push({ height, density, errorMask });
    }
    // If only one slice provided, replicate with slight variation for time dimension
    while (slices.length < TIME_SLICES && slices.length > 0) {
      const base = slices[0];
      const t = slices.length;
      const h2 = new Float32Array(base.height);
      const d2 = new Float32Array(base.density);
      const e2 = new Float32Array(base.errorMask);
      const phase = t / TIME_SLICES;
      for (let i = 0; i < h2.length; i++) {
        const ix = i % (GRID + 1);
        const iy = Math.floor(i / (GRID + 1));
        h2[i] *= 0.85 + 0.3 * Math.sin(phase * Math.PI * 2 + ix * 0.1 + iy * 0.08);
        d2[i] *= 0.9 + 0.2 * Math.cos(phase * Math.PI * 1.7 + ix * 0.07);
        e2[i] *= 0.7 + 0.6 * Math.abs(Math.sin(phase * Math.PI * 0.9 + ix * 0.25));
      }
      slices.push({ height: h2, density: d2, errorMask: e2 });
    }
    return slices.slice(0, TIME_SLICES);
  }
  // Build Perlin-like coherent noise grid
  _buildNoiseGrid(size, octaves) {
    const grid = new Float32Array(size * size);
    // Multi-octave value noise with smooth interpolation
    for (let iy = 0; iy < size; iy++) {
      for (let ix = 0; ix < size; ix++) {
        let val = 0;
        let amp = 1;
        let freq = 1;
        let totalAmp = 0;
        for (let o = 0; o < octaves; o++) {
          const sx = ix * freq / size;
          const sy = iy * freq / size;
          val += this._valueNoise(sx, sy) * amp;
          totalAmp += amp;
          amp *= 0.5;
          freq *= 2;
        }
        grid[iy * size + ix] = val / totalAmp;
      }
    }
    return grid;
  }
  _valueNoise(x, y) {
    const ix = Math.floor(x);
    const iy = Math.floor(y);
    const fx = x - ix;
    const fy = y - iy;
    const a = this._hash(ix, iy);
    const b = this._hash(ix + 1, iy);
    const c = this._hash(ix, iy + 1);
    const d = this._hash(ix + 1, iy + 1);
    // Smoothstep interpolation
    const sx = fx * fx * (3 - 2 * fx);
    const sy = fy * fy * (3 - 2 * fy);
    const lo = a + (b - a) * sx;
    const hi = c + (d - c) * sx;
    return lo + (hi - lo) * sy;
  }
  _hash(x, y) {
    let h = x * 374761393 + y * 668265263;
    h = (h ^ (h >> 13)) * 1274126177;
    return ((h ^ (h >> 16)) & 0x7fffffff) / 0x7fffffff;
  }
  // Extract continuous river paths from error masks using gradient descent
  _extractRiverPaths() {
    for (const slice of this.slices) {
      const paths = [];
      const visited = new Uint8Array((GRID + 1) * (GRID + 1));
      // Find error hotspots as river sources
      const sources = [];
      for (let iy = 1; iy < GRID; iy++) {
        for (let ix = 1; ix < GRID; ix++) {
          const idx = iy * (GRID + 1) + ix;
          if (slice.errorMask[idx] > 0.15 && !visited[idx]) {
            sources.push({ x: ix, y: iy, strength: slice.errorMask[idx] });
          }
        }
      }
      sources.sort((a, b) => b.strength - a.strength);
      // Trace each source downstream following gradient of height
      for (const src of sources.slice(0, 5)) {
        const path = [];
        let cx = src.x, cy = src.y;
        let steps = 0;
        while (cx > 0 && cx < GRID && cy > 0 && cy < GRID && steps < RIVER_SEGMENTS) {
          const idx = cy * (GRID + 1) + cx;
          if (visited[idx] > 2) break;
          visited[idx]++;
          path.push({ x: (cx / GRID - 0.5) * TERRAIN_SIZE,
                      y: (cy / GRID - 0.5) * TERRAIN_SIZE });
          // Gradient descent on height map — follow steepest downhill
          const h = slice.height[idx];
          const hl = slice.height[idx - 1] || h;
          const hr = slice.height[idx + 1] || h;
          const hu = slice.height[idx - (GRID + 1)] || h;
          const hd = slice.height[idx + (GRID + 1)] || h;
          const gx = hr - hl;
          const gy = hd - hu;
          const glen = Math.sqrt(gx * gx + gy * gy) || 1;
          cx += (gx / glen) * 1.2;
          cy += (gy / glen) * 1.2;
          steps++;
        }
        if (path.length > 3) paths.push(path);
      }
      slice.riverPaths = paths;
    }
  }
  getSlice(t) {
    const idx = Math.min(Math.max(Math.floor(t), 0), this.slices.length - 1);
    return this.slices[idx];
  }
}
// ═══════════════════════════════════════════════════════════════════
// CACHE SYSTEM
// ═══════════════════════════════════════════════════════════════════
// Stores pre-built geometries per time slice to avoid per-frame allocation.
class TerrainCache {
  constructor() {
    this.geometries = new Map();   // key: sliceIndex -> BufferGeometry
    this.riverGroups = new Map();  // key: sliceIndex -> THREE.Group
    this.hits = 0;
    this.misses = 0;
    this.maxSize = TIME_SLICES + 2;
  }
  key(sliceIdx) { return sliceIdx; }
  getGeo(sliceIdx) {
    const k = this.key(sliceIdx);
    if (this.geometries.has(k)) { this.hits++; return this.geometries.get(k); }
    this.misses++;
    return null;
  }
  setGeo(sliceIdx, geo) {
    const k = this.key(sliceIdx);
    if (this.geometries.size >= this.maxSize) {
      // Evict oldest entry
      const firstKey = this.geometries.keys().next().value;
      const oldGeo = this.geometries.get(firstKey);
      if (oldGeo) oldGeo.dispose();
      this.geometries.delete(firstKey);
    }
    this.geometries.set(k, geo);
  }
  getRiverGroup(sliceIdx) {
    const k = this.key(sliceIdx);
    if (this.riverGroups.has(k)) { return this.riverGroups.get(k); }
    return null;
  }
  setRiverGroup(sliceIdx, group) {
    const k = this.key(sliceIdx);
    if (this.riverGroups.size >= this.maxSize) {
      const firstKey = this.riverGroups.keys().next().value;
      const oldGroup = this.riverGroups.get(firstKey);
      if (oldGroup) { oldGroup.traverse(c => { if (c.geometry) c.geometry.dispose(); }); }
      this.riverGroups.delete(firstKey);
    }
    this.riverGroups.set(k, group);
  }
  stats() {
    const total = this.hits + this.misses;
    const rate = total > 0 ? ((this.hits / total) * 100).toFixed(1) : '0.0';
    return `hits:${this.hits} misses:${this.misses} rate:${rate}% entries:${this.geometries.size}`;
  }
  clear() {
    for (const geo of this.geometries.values()) geo.dispose();
    this.geometries.clear();
    for (const group of this.riverGroups.values()) {
      group.traverse(c => { if (c.geometry) c.geometry.dispose(); });
    }
    this.riverGroups.clear();
    this.hits = 0;
    this.misses = 0;
  }
}
// ═══════════════════════════════════════════════════════════════════
// TERRAIN BUILDER
// ═══════════════════════════════════════════════════════════════════
class TerrainBuilder {
  constructor(dataAdapter, cache) {
    this.adapter = dataAdapter;
    this.cache = cache;
    this.mesh = null;     // current terrain mesh in scene
  }
  // Build a BufferGeometry terrain for a given time slice
  buildGeometry(sliceIdx) {
    const cached = this.cache.getGeo(sliceIdx);
    if (cached) return cached;
    const slice = this.adapter.getSlice(sliceIdx);
    const geo = new THREE.BufferGeometry();
    const vertices = new Float32Array((GRID + 1) * (GRID + 1) * 3);
    const colors = new Float32Array((GRID + 1) * (GRID + 1) * 3);
    const indices = [];
    for (let iy = 0; iy <= GRID; iy++) {
      for (let ix = 0; ix <= GRID; ix++) {
        const idx = iy * (GRID + 1) + ix;
        const vi = idx * 3;
        // Position: xz grid, y from height data scaled by peak
        vertices[vi] = (ix / GRID - 0.5) * TERRAIN_SIZE;
        vertices[vi + 1] = slice.height[idx] * PEAK_HEIGHT;
        vertices[vi + 2] = (iy / GRID - 0.5) * TERRAIN_SIZE;
        // Vertex color: blend height (warm peaks) and density (green valleys)
        const h = slice.height[idx];
        const d = slice.density[idx];
        // Peak warmth: yellow-orange at top, green at mid, blue at base
        const r = 0.15 + h * 0.85;
        const g = 0.1 + d * 0.75;
        const b = 0.5 - h * 0.3 + d * 0.1;
        colors[vi] = r;
        colors[vi + 1] = g;
        colors[vi + 2] = b;
      }
    }
    // Index buffer: two triangles per quad
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const a = iy * (GRID + 1) + ix;
        const b = a + 1;
        const c = a + (GRID + 1);
        const d = c + 1;
        indices.push(a, b, d);
        indices.push(a, d, c);
      }
    }
    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.setIndex(indices);
    geo.computeVertexNormals();
    this.cache.setGeo(sliceIdx, geo);
    return geo;
  }
  // Create or update the terrain mesh in the scene
  updateMesh(sliceIdx) {
    const geo = this.buildGeometry(sliceIdx);
    if (this.mesh) {
      // Swap geometry — reuse material, avoid new draw calls
      this.mesh.geometry.dispose();
      this.mesh.geometry = geo;
    } else {
      const mat = new THREE.MeshStandardMaterial({
        vertexColors: true,
        roughness: 0.55,
        metalness: 0.05,
        flatShading: false,
      });
      this.mesh = new THREE.Mesh(geo, mat);
      this.mesh.castShadow = true;
      this.mesh.receiveShadow = true;
      scene.add(this.mesh);
    }
    // Update rivers
    this._buildRivers(sliceIdx);
  }
  // Build river TubeGeometry from pre-extracted paths
  _buildRivers(sliceIdx) {
    // Remove previous river group
    const oldGroup = this.cache.getRiverGroup(sliceIdx);
    if (oldGroup) {
      if (oldGroup.parent) oldGroup.parent.remove(oldGroup);
    }
    // Check if mesh has riverGroup child
    if (this.mesh) {
      const existing = this.mesh.children.find(c => c.userData.isRiverGroup);
      if (existing) this.mesh.remove(existing);
    }
    const cachedGroup = this.cache.getRiverGroup(sliceIdx);
    if (cachedGroup) {
      this.mesh.add(cachedGroup);
      return;
    }
    const slice = this.adapter.getSlice(sliceIdx);
    const group = new THREE.Group();
    group.userData.isRiverGroup = true;
    const pathMat = new THREE.MeshStandardMaterial({
      color: 0xff3344,
      roughness: 0.3,
      metalness: 0.4,
      emissive: 0x330000,
      emissiveIntensity: 0.6,
    });
    for (const path of slice.riverPaths || []) {
      if (path.length < 3) continue;
      const points = [];
      for (const p of path) {
        // Lookup terrain height at this xz position
        const gx = (p.x / TERRAIN_SIZE + 0.5) * GRID;
        const gy = (p.y / TERRAIN_SIZE + 0.5) * GRID;
        const ix = Math.round(Math.max(0, Math.min(GRID, gx)));
        const iy = Math.round(Math.max(0, Math.min(GRID, gy)));
        const idx = iy * (GRID + 1) + ix;
        const terrainY = (slice.height[idx] || 0) * PEAK_HEIGHT;
        points.push(new THREE.Vector3(p.x, terrainY + 0.15, p.y));
      }
      if (points.length < 2) continue;
      const curve = new THREE.CatmullRomCurve3(points);
      const tubeGeo = new THREE.TubeGeometry(curve, Math.min(path.length * 2, 64), 0.12, 6, false);
      const tube = new THREE.Mesh(tubeGeo, pathMat);
      tube.castShadow = false;
      tube.receiveShadow = true;
      group.add(tube);
    }
    this.cache.setRiverGroup(sliceIdx, group);
    if (this.mesh) this.mesh.add(group);
  }
}
// ═══════════════════════════════════════════════════════════════════
// PARTICLE SYSTEM
// ═══════════════════════════════════════════════════════════════════
class ParticleSystem {
  constructor(adapter) {
    this.adapter = adapter;
    this.count = PARTICLE_COUNT;
    // Pre-allocate position, velocity, and lifetime arrays — reused every frame
    this.positions = new Float32Array(this.count * 3);
    this.velocities = new Float32Array(this.count * 3);
    this.lifetimes = new Float32Array(this.count);
    this.points = null; // THREE.Points in scene
    this.geo = null;    // BufferGeometry — attribute arrays reused
    this._initParticles();
  }
  _initParticles() {
    // Distribute particles randomly across terrain surface
    for (let i = 0; i < this.count; i++) {
      this._resetParticle(i, Math.random());
    }
    this.geo = new THREE.BufferGeometry();
    this.geo.setAttribute('position',
      new THREE.BufferAttribute(this.positions, 3));
    const sizes = new Float32Array(this.count);
    for (let i = 0; i < this.count; i++) sizes[i] = 1.8 + Math.random() * 2.5;
    this.geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    // Glow sprite texture via canvas
    const spriteCanvas = document.createElement('canvas');
    spriteCanvas.width = 16;
    spriteCanvas.height = 16;
    const ctx = spriteCanvas.getContext('2d');
    const gradient = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    gradient.addColorStop(0, 'rgba(180,220,255,1)');
    gradient.addColorStop(0.35, 'rgba(100,180,255,0.7)');
    gradient.addColorStop(0.7, 'rgba(40,100,255,0.15)');
    gradient.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 16, 16);
    const spriteTex = new THREE.CanvasTexture(spriteCanvas);
    spriteTex.needsUpdate = true;
    const mat = new THREE.PointsMaterial({
      map: spriteTex,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      color: 0x88ccff,
      size: 0.35,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.75,
    });
    this.points = new THREE.Points(this.geo, mat);
    this.points.renderOrder = 1;
    scene.add(this.points);
  }
  _resetParticle(i, phase) {
    const pi = i * 3;
    // Random position on terrain surface
    const rx = Math.random();
    const ry = Math.random();
    this.positions[pi] = (rx - 0.5) * TERRAIN_SIZE;
    this.positions[pi + 2] = (ry - 0.5) * TERRAIN_SIZE;
    // Height from current terrain data
    const ix = Math.floor(rx * GRID);
    const iy = Math.floor(ry * GRID);
    const idx = iy * (GRID + 1) + ix;
    const slice = this.adapter.getSlice(phase * (TIME_SLICES - 1));
    this.positions[pi + 1] = (slice.height[idx] || 0) * PEAK_HEIGHT + 0.3;
    // Velocity: slow drift along surface gradient
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.02 + Math.random() * 0.06;
    this.velocities[pi] = Math.cos(angle) * speed;
    this.velocities[pi + 2] = Math.sin(angle) * speed;
    this.velocities[pi + 1] = 0;
    this.lifetimes[i] = Math.random() * 3 + 1.5;
  }
  update(dt, sliceIdx) {
    if (!this.points) return;
    const slice = this.adapter.getSlice(sliceIdx);
    for (let i = 0; i < this.count; i++) {
      this.lifetimes[i] -= dt;
      if (this.lifetimes[i] <= 0) {
        this._resetParticle(i, sliceIdx / (TIME_SLICES - 1));
        continue;
      }
      const pi = i * 3;
      // Move particle along velocity
      this.positions[pi] += this.velocities[pi] * dt * 8;
      this.positions[pi + 2] += this.velocities[pi + 2] * dt * 8;
      // Clamp to terrain bounds
      const half = TERRAIN_SIZE / 2;
      if (Math.abs(this.positions[pi]) > half + 0.5 ||
          Math.abs(this.positions[pi + 2]) > half + 0.5) {
        this.lifetimes[i] = 0;
        continue;
      }
      // Project onto terrain surface
      const gx = (this.positions[pi] / TERRAIN_SIZE + 0.5) * GRID;
      const gy = (this.positions[pi + 2] / TERRAIN_SIZE + 0.5) * GRID;
      const ix = Math.round(Math.max(0, Math.min(GRID, gx)));
      const iy = Math.round(Math.max(0, Math.min(GRID, gy)));
      const idx = iy * (GRID + 1) + ix;
      const targetY = (slice.height[idx] || 0) * PEAK_HEIGHT + 0.35;
      this.positions[pi + 1] += (targetY - this.positions[pi + 1]) * 0.3;
    }
    // Flag attribute for GPU upload — reuses same Float32Array, no allocation
    this.geo.attributes.position.needsUpdate = true;
  }
}
// ═══════════════════════════════════════════════════════════════════
// BOOKMARK MANAGER
// ═══════════════════════════════════════════════════════════════════
class BookmarkManager {
  constructor(controls) {
    this.controls = controls;
    this.bookmarks = new Map(); // key: '1'-'5' -> {pos, target}
    this._loadFromStorage();
  }
  save(key) {
    this.bookmarks.set(key, {
      pos: this.controls.object.position.clone(),
      target: this.controls.target.clone(),
    });
    this._persist();
  }
  load(key) {
    const bm = this.bookmarks.get(key);
    if (!bm) return;
    this.controls.object.position.copy(bm.pos);
    this.controls.target.copy(bm.target);
    this.controls.update();
  }
  _persist() {
    const data = {};
    for (const [k, v] of this.bookmarks) {
      data[k] = {
        pos: [v.pos.x, v.pos.y, v.pos.z],
        target: [v.target.x, v.target.y, v.target.z],
      };
    }
    try { localStorage.setItem('terrain_bookmarks', JSON.stringify(data)); } catch (_) {}
  }
  _loadFromStorage() {
    try {
      const raw = localStorage.getItem('terrain_bookmarks');
      if (!raw) return;
      const data = JSON.parse(raw);
      for (const [k, v] of Object.entries(data)) {
        this.bookmarks.set(k, {
          pos: new THREE.Vector3(v.pos[0], v.pos[1], v.pos[2]),
          target: new THREE.Vector3(v.target[0], v.target[1], v.target[2]),
        });
      }
    } catch (_) {}
  }
  clear() {
    this.bookmarks.clear();
    localStorage.removeItem('terrain_bookmarks');
  }
  hasAny() { return this.bookmarks.size > 0; }
}
// ═══════════════════════════════════════════════════════════════════
// APPLICATION
// ═══════════════════════════════════════════════════════════════════
const adapter = new DataAdapter();
const cache = new TerrainCache();
const builder = new TerrainBuilder(adapter, cache);
const particles = new ParticleSystem(adapter);
const bookmarks = new BookmarkManager(controls);
let currentSlice = 0;
let playing = false;
let playTimer = null;
let riverDebounceTimer = null;
// Generate initial data
adapter.generateSynthetic();
builder.updateMesh(0);
timeSlider.max = TIME_SLICES - 1;
// ─── Time slider ─────────────────────────────────────────────────
function setSlice(idx) {
  if (idx === currentSlice) return;
  currentSlice = idx;
  timeSlider.value = idx;
  const hours = Math.floor((idx / TIME_SLICES) * 24);
  const mins = Math.floor(((idx / TIME_SLICES) * 24 - hours) * 60);
  timeLabel.textContent = `${String(hours).padStart(2,'0')}:${String(mins).padStart(2,'0')}`;
  // Terrain swap: cached geometry swap (no new THREE.XxxGeometry in hot path)
  builder.updateMesh(idx);
  // Debounce river rebuilds — TubeGeometry is expensive
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    builder._buildRivers(idx);
    diagEl.textContent = cache.stats() + ' | slice:' + idx;
  }, 200);
}
timeSlider.addEventListener('input', () => {
  setSlice(parseInt(timeSlider.value));
});
// ─── Play/pause ──────────────────────────────────────────────────
playBtn.addEventListener('click', () => {
  playing = !playing;
  playBtn.textContent = playing ? 'Pause' : 'Play';
  playBtn.classList.toggle('active', playing);
  if (playing) {
    const tick = () => {
      if (!playing) return;
      const next = (currentSlice + 1) % TIME_SLICES;
      setSlice(next);
      playTimer = setTimeout(tick, 600);
    };
    tick();
  } else {
    if (playTimer) clearTimeout(playTimer);
  }
});
// ─── Auto-rotate ─────────────────────────────────────────────────
autoRotateBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autoRotateBtn.classList.toggle('active', controls.autoRotate);
});
// ─── Bookmarks ────────────────────────────────────────────────────
function updateBookmarkButtons() {
  const buttons = bookmarkRow.querySelectorAll('.bookmark-btn');
  for (const btn of buttons) {
    const key = btn.dataset.key;
    btn.classList.toggle('active', bookmarks.bookmarks.has(key));
  }
}
bookmarkRow.addEventListener('click', (e) => {
  const btn = e.target.closest('.bookmark-btn');
  if (!btn) return;
  bookmarks.load(btn.dataset.key);
});
document.getElementById('save-bm').addEventListener('click', () => {
  // Save to first available slot or prompt via console
  for (let i = 1; i <= 5; i++) {
    const key = String(i);
    if (!bookmarks.bookmarks.has(key)) {
      bookmarks.save(key);
      updateBookmarkButtons();
      return;
    }
  }
  // All slots full, overwrite slot 1
  bookmarks.save('1');
  updateBookmarkButtons();
});
document.getElementById('clear-bm').addEventListener('click', () => {
  bookmarks.clear();
  updateBookmarkButtons();
});
// Keyboard shortcuts: Ctrl+1-5 to save bookmark
window.addEventListener('keydown', (e) => {
  if (e.ctrlKey && e.key >= '1' && e.key <= '5') {
    e.preventDefault();
    bookmarks.save(e.key);
    updateBookmarkButtons();
  }
});
// ─── Presets ──────────────────────────────────────────────────────
document.querySelectorAll('.preset-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const preset = btn.dataset.preset;
    cache.clear();
    adapter.generatePreset(preset);
    setSlice(0);
    builder.updateMesh(0);
    diagEl.textContent = 'preset:' + preset + ' | ' + cache.stats();
  });
});
// ─── External data load ──────────────────────────────────────────
document.getElementById('load-btn').addEventListener('click', async () => {
  const url = document.getElementById('data-url').value.trim();
  if (!url) return;
  cache.clear();
  const ok = await adapter.loadFromURL(url);
  if (ok) {
    setSlice(0);
    builder.updateMesh(0);
    diagEl.textContent = 'loaded external data | ' + cache.stats();
  } else {
    diagEl.textContent = 'FAILED to load: ' + url;
  }
});
// ─── Resize handler ───────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Render loop ──────────────────────────────────────────────────
let lastTime = performance.now();
let frameCount = 0;
let fpsUpdateTime = lastTime;
function animate(now) {
  requestAnimationFrame(animate);
  const dt = Math.min((now - lastTime) / 1000, 0.1);
  lastTime = now;
  controls.update();
  // Update particles with terrain-aware positions — reuses pre-allocated arrays
  particles.update(dt, currentSlice);
  renderer.render(scene, camera);
  // Periodic FPS + cache stats update to diagnostic panel (throttled)
  frameCount++;
  if (now - fpsUpdateTime > 2000) {
    const fps = Math.round(frameCount / ((now - fpsUpdateTime) / 1000));
    diagEl.textContent = cache.stats() + ' | fps:' + fps + ' | slice:' + currentSlice;
    frameCount = 0;
    fpsUpdateTime = now;
  }
}
// ─── Start ────────────────────────────────────────────────────────
updateBookmarkButtons();
diagEl.textContent = cache.stats();
requestAnimationFrame(animate);
</script>
</body>
</html>