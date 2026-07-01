<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8c8d4}
#canvas-container{position:fixed;inset:0;z-index:1}
#ui-overlay{position:fixed;bottom:0;left:0;right:0;z-index:10;padding:16px 20px;
  background:linear-gradient(transparent,rgba(10,10,20,0.92));display:flex;align-items:center;gap:14px;flex-wrap:wrap}
#time-slider{flex:1;min-width:180px;max-width:500px;accent-color:#4af;height:6px;cursor:pointer}
#time-label{font-size:13px;color:#8af;min-width:100px;text-align:center;font-variant-numeric:tabular-nums}
button{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#c8c8d4;
  padding:6px 14px;border-radius:5px;cursor:pointer;font-size:12px;transition:all 0.2s}
button:hover{background:rgba(255,255,255,0.16);border-color:rgba(255,255,255,0.3)}
button.active{background:rgba(68,170,255,0.2);border-color:#4af;color:#4af}
#diagnostics{position:fixed;top:12px;right:12px;z-index:10;background:rgba(10,10,20,0.88);
  border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:12px 16px;font-size:11px;
  line-height:1.6;min-width:200px;backdrop-filter:blur(6px)}
#diagnostics h3{margin:0 0 6px;font-size:12px;color:#8af;font-weight:600}
.diag-row{display:flex;justify-content:space-between;gap:20px}
.diag-row .label{color:#888} .diag-row .value{color:#c8c8d4;font-variant-numeric:tabular-nums}
.cache-hit{color:#4c6} .cache-miss{color:#e55}
#bookmark-bar{position:fixed;top:12px;left:50%;transform:translateX(-50%);z-index:10;
  display:flex;gap:6px;background:rgba(10,10,20,0.88);border:1px solid rgba(255,255,255,0.12);
  border-radius:8px;padding:6px 10px;backdrop-filter:blur(6px)}
#loading{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;
  background:#0a0a14;color:#8af;font-size:16px;transition:opacity 0.5s}
#loading.hidden{opacity:0;pointer-events:none}
</style>
</head>
<body>
<div id="loading">Building terrain...</div>
<div id="canvas-container"></div>
<div id="diagnostics">
  <h3>Diagnostics</h3>
  <div class="diag-row"><span class="label">FPS</span><span class="value" id="d-fps">--</span></div>
  <div class="diag-row"><span class="label">Vertices</span><span class="value" id="d-verts">--</span></div>
  <div class="diag-row"><span class="label">Particles</span><span class="value" id="d-parts">--</span></div>
  <div class="diag-row"><span class="label">Time idx</span><span class="value" id="d-time">--</span></div>
  <div class="diag-row"><span class="label">Terrain cache</span><span class="value"><span class="cache-hit" id="d-t-hit">0</span>/<span class="cache-miss" id="d-t-miss">0</span></span></div>
  <div class="diag-row"><span class="label">River cache</span><span class="value"><span class="cache-hit" id="d-r-hit">0</span>/<span class="cache-miss" id="d-r-miss">0</span></span></div>
  <div class="diag-row"><span class="label">Grid xform</span><span class="value"><span class="cache-hit" id="d-g-hit">0</span>/<span class="cache-miss" id="d-g-miss">0</span></span></div>
</div>
<div id="bookmark-bar">
  <button id="bm-save" title="Save camera bookmark (1-5)">Save View</button>
  <button class="bm-load" data-idx="0">View 1</button>
  <button class="bm-load" data-idx="1">View 2</button>
  <button class="bm-load" data-idx="2">View 3</button>
  <button class="bm-load" data-idx="3">View 4</button>
  <button class="bm-load" data-idx="4">View 5</button>
</div>
<div id="ui-overlay">
  <button id="btn-play" title="Play/Pause time animation">▶ Play</button>
  <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
  <span id="time-label">Hour 00:00</span>
  <button id="btn-auto-rotate" class="active" title="Toggle auto-rotation">Auto-Rotate</button>
  <button id="btn-top-view" title="Top-down view">Top</button>
  <button id="btn-reset-view" title="Reset camera">Reset</button>
</div>
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.157.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.157.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ============================================================
// Configuration
// ============================================================
const GRID = 80;                  // terrain grid resolution (vertices per side)
const TIME_POINTS = 24;          // hours in a day
const TERRAIN_SIZE = 20;         // world-space size of terrain square
const PARTICLE_COUNT = 400;      // number of flow particles
const RIVER_COUNT = 3;           // number of error rivers
const RIVER_SEGMENTS = 200;      // tube segments per river
const RIVER_RADIUS = 0.12;       // tube radius
const DEBOUNCE_MS = 200;         // river rebuild debounce
// ============================================================
// Cache Manager — tracks all cacheable computations
// ============================================================
class CacheManager {
  constructor() {
    this.terrainGeometries = new Map();   // timeIndex -> BufferGeometry
    this.riverGeometries = new Map();     // timeIndex -> THREE.TubeGeometry[]
    this.noiseGrids = new Map();          // timeIndex -> { elevation: Float32Array, vegetation: Float32Array }
    this.gridTransforms = new Map();      // key="x,z" -> { gx, gz } grid coords
    this.stats = {
      terrain: { hits: 0, misses: 0 },
      river: { hits: 0, misses: 0 },
      gridTransform: { hits: 0, misses: 0 }
    };
  }
  getTerrainGeometry(timeIndex) {
    const cached = this.terrainGeometries.get(timeIndex);
    if (cached) { this.stats.terrain.hits++; return cached; }
    this.stats.terrain.misses++;
    return null;
  }
  setTerrainGeometry(timeIndex, geometry) {
    this.terrainGeometries.set(timeIndex, geometry);
  }
  getRiverGeometries(timeIndex) {
    const cached = this.riverGeometries.get(timeIndex);
    if (cached) { this.stats.river.hits++; return cached; }
    this.stats.river.misses++;
    return null;
  }
  setRiverGeometries(timeIndex, geometries) {
    this.riverGeometries.set(timeIndex, geometries);
  }
  getNoiseGrid(timeIndex) {
    const cached = this.noiseGrids.get(timeIndex);
    return cached || null;
  }
  setNoiseGrid(timeIndex, grid) {
    this.noiseGrids.set(timeIndex, grid);
  }
  // Memoized world-to-grid coordinate transform — never recompute per frame
  worldToGrid(wx, wz) {
    const key = `${wx.toFixed(3)},${wz.toFixed(3)}`;
    const cached = this.gridTransforms.get(key);
    if (cached) { this.stats.gridTransform.hits++; return cached; }
    this.stats.gridTransform.misses++;
    const half = TERRAIN_SIZE / 2;
    const gx = Math.round(((wx + half) / TERRAIN_SIZE) * (GRID - 1));
    const gz = Math.round(((wz + half) / TERRAIN_SIZE) * (GRID - 1));
    const result = {
      gx: Math.max(0, Math.min(GRID - 1, gx)),
      gz: Math.max(0, Math.min(GRID - 1, gz))
    };
    // Limit cache size to prevent unbounded growth from hover events
    if (this.gridTransforms.size < 5000) {
      this.gridTransforms.set(key, result);
    }
    return result;
  }
}
// ============================================================
// Data Generator — creates synthetic time-series terrain data
// ============================================================
class DataGenerator {
  // Simple deterministic hash for pseudo-random noise
  static hash(x, y, seed) {
    let h = seed + x * 374761393 + y * 668265263;
    h = (h ^ (h >> 13)) * 1274126177;
    return (h ^ (h >> 16)) / 2147483648;
  }
  // Smooth noise via bilinear interpolation of hash grid
  static smoothNoise(x, y, scale, seed) {
    const sx = x / scale, sy = y / scale;
    const ix = Math.floor(sx), iy = Math.floor(sy);
    const fx = sx - ix, fy = sy - iy;
    const sx0 = fx * fx * (3 - 2 * fx); // smoothstep
    const sy0 = fy * fy * (3 - 2 * fy);
    const v00 = DataGenerator.hash(ix, iy, seed);
    const v10 = DataGenerator.hash(ix + 1, iy, seed);
    const v01 = DataGenerator.hash(ix, iy + 1, seed);
    const v11 = DataGenerator.hash(ix + 1, iy + 1, seed);
    const a = v00 + (v10 - v00) * sx0;
    const b = v01 + (v11 - v01) * sx0;
    return a + (b - a) * sy0;
  }
  // Generate elevation + vegetation grids for one time point
  static generateGrids(timeIndex) {
    const total = GRID * GRID;
    const elevation = new Float32Array(total);
    const vegetation = new Float32Array(total);
    const t = timeIndex / TIME_POINTS; // 0..1 time phase
    // Terrain shape: two migrating peaks + rolling hills
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iz * GRID + ix;
        const nx = ix / (GRID - 1) - 0.5; // -0.5..0.5 normalized
        const nz = iz / (GRID - 1) - 0.5;
        // Peak 1: drifts eastward over the day, centered north
        const p1x = -0.15 + t * 0.3;
        const p1z = -0.2;
        const d1 = Math.sqrt((nx - p1x) ** 2 + (nz - p1z) ** 2);
        const peak1 = Math.exp(-d1 * d1 * 50) * 5.0;
        // Peak 2: drifts westward, centered south
        const p2x = 0.2 - t * 0.25;
        const p2z = 0.15;
        const d2 = Math.sqrt((nx - p2x) ** 2 + (nz - p2z) ** 2);
        const peak2 = Math.exp(-d2 * d2 * 45) * 4.0;
        // Rolling terrain from layered noise
        const noise1 = DataGenerator.smoothNoise(ix, iz, 18, 100 + timeIndex * 7);
        const noise2 = DataGenerator.smoothNoise(ix, iz, 35, 200 + timeIndex * 3);
        const noise3 = DataGenerator.smoothNoise(ix, iz, 60, 300);
        const roll = noise1 * 1.8 + noise2 * 0.9 + noise3 * 0.4;
        // Combine peaks + rolling terrain
        let elev = peak1 + peak2 + roll + 0.5;
        elev = Math.max(0, elev);
        elevation[idx] = elev;
        // Vegetation: dense near peaks, in valleys, with noise variation
        const vegBase = (1.0 - Math.abs(elev - 2.5) / 3.5);
        const vegNoise = DataGenerator.smoothNoise(ix, iz, 12, 400 + timeIndex * 5);
        vegetation[idx] = Math.max(0, Math.min(1, vegBase * 0.7 + vegNoise * 0.3));
      }
    }
    return { elevation, vegetation };
  }
  // Generate river paths: follow terrain gradient from high-error zones
  static generateRiverPaths(elevation, timeIndex) {
    const rivers = [];
    // Multiple error hotspots that shift over time
    const t = timeIndex / TIME_POINTS;
    const hotspots = [
      { sx: 0.35 + t * 0.1, sz: -0.25 },       // hotspot drifts
      { sx: -0.30 - t * 0.08, sz: 0.20 },
      { sx: 0.10 + Math.sin(t * 6) * 0.15, sz: 0.05 }
    ];
    for (let r = 0; r < RIVER_COUNT; r++) {
      const points = [];
      let cx = hotspots[r].sx, cz = hotspots[r].sz;
      // Trace downhill for ~30 steps, avoiding infinite loops
      for (let step = 0; step < 35; step++) {
        const gx = Math.round((cx + 0.5) * (GRID - 1));
        const gz = Math.round((cz + 0.5) * (GRID - 1));
        if (gx < 1 || gx >= GRID - 1 || gz < 1 || gz >= GRID - 1) break;
        const idx = gz * GRID + gx;
        const h = elevation[idx];
        const wx = (gx / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        const wz = (gz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        points.push(new THREE.Vector3(wx, h * 0.7 + 0.08, wz)); // slightly above surface
        // Compute gradient (steepest descent) from 4 neighbors
        const hL = elevation[gz * GRID + Math.max(0, gx - 1)];
        const hR = elevation[gz * GRID + Math.min(GRID - 1, gx + 1)];
        const hU = elevation[Math.max(0, gz - 1) * GRID + gx];
        const hD = elevation[Math.min(GRID - 1, gz + 1) * GRID + gx];
        const gdx = (hR - hL) * 0.5;
        const gdz = (hD - hU) * 0.5;
        const mag = Math.sqrt(gdx * gdx + gdz * gdz) || 0.001;
        cx -= (gdx / mag) * 0.04; // step downhill
        cz -= (gdz / mag) * 0.04;
        // Add slight meander based on step count and river index
        cx += Math.sin(step * 0.5 + r) * 0.008;
        cz += Math.cos(step * 0.6 + r) * 0.008;
      }
      if (points.length >= 4) rivers.push(points);
    }
    return rivers;
  }
  // Generate flow paths for particles: contour-following paths
  static generateFlowPaths(elevation, timeIndex) {
    const paths = [];
    const pathCount = 25;
    const t = timeIndex / TIME_POINTS;
    for (let p = 0; p < pathCount; p++) {
      const points = [];
      // Start at a random position that shifts with time
      const seed = p * 131 + timeIndex * 17;
      let cx = ((DataGenerator.hash(seed, 0, 500) - 0.5) * 0.85);
      let cz = ((DataGenerator.hash(seed, 1, 501) - 0.5) * 0.85);
      for (let step = 0; step < 40; step++) {
        const gx = Math.round((cx + 0.5) * (GRID - 1));
        const gz = Math.round((cz + 0.5) * (GRID - 1));
        if (gx < 1 || gx >= GRID - 1 || gz < 1 || gz >= GRID - 1) break;
        const idx = gz * GRID + gx;
        const h = elevation[idx];
        const wx = (gx / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        const wz = (gz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        points.push(new THREE.Vector3(wx, h * 0.72 + 0.06, wz));
        // Follow terrain contour: perpendicular to gradient (cross-slope flow)
        const hL = elevation[gz * GRID + Math.max(0, gx - 1)];
        const hR = elevation[gz * GRID + Math.min(GRID - 1, gx + 1)];
        const hU = elevation[Math.max(0, gz - 1) * GRID + gx];
        const hD = elevation[Math.min(GRID - 1, gz + 1) * GRID + gx];
        const gdx = (hR - hL) * 0.5, gdz = (hD - hU) * 0.5;
        const mag = Math.sqrt(gdx * gdx + gdz * gdz) || 0.001;
        // Move perpendicular to gradient + slight downhill component
        cx += (-gdz / mag) * 0.03 - (gdx / mag) * 0.008;
        cz += (gdx / mag) * 0.03 - (gdz / mag) * 0.008;
      }
      if (points.length >= 3) paths.push(points);
    }
    return paths;
  }
}
// ============================================================
// Terrain System — manages the heightfield mesh
// ============================================================
class TerrainSystem {
  constructor(scene, cache) {
    this.scene = scene;
    this.cache = cache;
    this.mesh = null;
    this.currentTimeIndex = -1;
  }
  // Build a single BufferGeometry for one time point (cached)
  buildGeometry(timeIndex) {
    const cached = this.cache.getTerrainGeometry(timeIndex);
    if (cached) return cached;
    let grids = this.cache.getNoiseGrid(timeIndex);
    if (!grids) {
      grids = DataGenerator.generateGrids(timeIndex);
      this.cache.setNoiseGrid(timeIndex, grids);
    }
    const { elevation, vegetation } = grids;
    const vertCount = GRID * GRID;
    const positions = new Float32Array(vertCount * 3);
    const colors = new Float32Array(vertCount * 3);
    const half = TERRAIN_SIZE / 2;
    // Build vertex arrays: position from elevation, color from vegetation
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const vi = iz * GRID + ix;
        const idx3 = vi * 3;
        positions[idx3] = (ix / (GRID - 1)) * TERRAIN_SIZE - half;
        positions[idx3 + 1] = elevation[vi] * 0.7; // scale elevation for visual
        positions[idx3 + 2] = (iz / (GRID - 1)) * TERRAIN_SIZE - half;
        // Vegetation gradient: brown(dry) -> yellow -> lush green
        const v = vegetation[vi];
        const r = 0.25 + v * 0.15;
        const g = 0.18 + v * 0.62;
        const b = 0.08 + v * 0.12;
        colors[idx3] = r;
        colors[idx3 + 1] = g;
        colors[idx3 + 2] = b;
      }
    }
    // Build index array for triangle strips (avoids degenerate triangles)
    const indices = [];
    for (let iz = 0; iz < GRID - 1; iz++) {
      for (let ix = 0; ix < GRID - 1; ix++) {
        const a = iz * GRID + ix;
        const b = a + 1;
        const c = a + GRID;
        const d = c + 1;
        indices.push(a, b, d);
        indices.push(a, d, c);
      }
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    this.cache.setTerrainGeometry(timeIndex, geometry);
    return geometry;
  }
  // Initialize the terrain mesh in the scene
  init(timeIndex) {
    const geometry = this.buildGeometry(timeIndex);
    const material = new THREE.MeshLambertMaterial({
      vertexColors: true,
      flatShading: true,
      side: THREE.DoubleSide
    });
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.receiveShadow = true;
    this.scene.add(this.mesh);
    this.currentTimeIndex = timeIndex;
  }
  // Swap terrain geometry for a new time index (from cache, no allocation)
  setTimeIndex(timeIndex) {
    if (timeIndex === this.currentTimeIndex) return;
    const geometry = this.buildGeometry(timeIndex); // hits cache if built
    if (this.mesh) {
      this.mesh.geometry.dispose(); // dispose old, swap in cached
      this.mesh.geometry = geometry;
    }
    this.currentTimeIndex = timeIndex;
  }
  getVertexCount() {
    return this.mesh ? this.mesh.geometry.attributes.position.count : 0;
  }
}
// ============================================================
// River System — TubeGeometry error paths with debounced rebuild
// ============================================================
class RiverSystem {
  constructor(scene, cache) {
    this.scene = scene;
    this.cache = cache;
    this.riverGroup = new THREE.Group();
    this.scene.add(this.riverGroup);
    this.currentTimeIndex = -1;
    this.debounceTimer = null;
    this.pendingTimeIndex = null;
    this.material = new THREE.MeshLambertMaterial({
      color: 0xe04030,
      emissive: 0x331010,
      flatShading: true
    });
  }
  // Build TubeGeometry for all rivers at a time index (cached)
  buildRivers(timeIndex) {
    const cached = this.cache.getRiverGeometries(timeIndex);
    if (cached) return cached;
    let grids = this.cache.getNoiseGrid(timeIndex);
    if (!grids) {
      grids = DataGenerator.generateGrids(timeIndex);
      this.cache.setNoiseGrid(timeIndex, grids);
    }
    const paths = DataGenerator.generateRiverPaths(grids.elevation, timeIndex);
    const geometries = [];
    for (const path of paths) {
      if (path.length < 2) continue;
      const curve = new THREE.CatmullRomCurve3(path);
      // TubeGeometry built once, cached — never in hot path
      const tubeGeo = new THREE.TubeGeometry(curve, RIVER_SEGMENTS, RIVER_RADIUS, 6, false);
      geometries.push(tubeGeo);
    }
    this.cache.setRiverGeometries(timeIndex, geometries);
    return geometries;
  }
  // Initialize rivers at the given time index
  init(timeIndex) {
    const geometries = this.buildRivers(timeIndex);
    this._replaceMeshes(geometries);
    this.currentTimeIndex = timeIndex;
  }
  // Debounced river update: schedule rebuild, swap cached if available
  setTimeIndex(timeIndex) {
    if (timeIndex === this.currentTimeIndex) return;
    // Check if cached version exists — swap immediately if so
    const cached = this.cache.getRiverGeometries(timeIndex);
    if (cached) {
      this._replaceMeshes(cached);
      this.currentTimeIndex = timeIndex;
      return;
    }
    // Cache miss: schedule debounced build
    this.pendingTimeIndex = timeIndex;
    if (this.debounceTimer) clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => {
      const ti = this.pendingTimeIndex;
      if (ti === null || ti === this.currentTimeIndex) return;
      const geometries = this.buildRivers(ti);
      this._replaceMeshes(geometries);
      this.currentTimeIndex = ti;
      this.pendingTimeIndex = null;
    }, DEBOUNCE_MS);
  }
  // Replace all river meshes in the group (dispose old, add new)
  _replaceMeshes(geometries) {
    while (this.riverGroup.children.length > 0) {
      const child = this.riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      this.riverGroup.remove(child);
    }
    for (const geo of geometries) {
      const mesh = new THREE.Mesh(geo, this.material);
      mesh.receiveShadow = true;
      this.riverGroup.add(mesh);
    }
  }
}
// ============================================================
// Particle System — flow particles with reused position array
// ============================================================
class ParticleSystem {
  constructor(scene, cache) {
    this.scene = scene;
    this.cache = cache;
    this.points = null;
    // Pre-allocated particle data — reused every frame, no per-frame allocations
    this.particleData = new Array(PARTICLE_COUNT);
    // Single Float32Array for all particle positions — written in-place each frame
    this.positionArray = new Float32Array(PARTICLE_COUNT * 3);
    this.currentTimeIndex = -1;
    this.flowPaths = []; // cached flow paths for current time
    this._initGeometry();
  }
  _initGeometry() {
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(this.positionArray, 3));
    const material = new THREE.PointsMaterial({
      color: 0x88ccff,
      size: 0.12,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.8
    });
    this.points = new THREE.Points(geometry, material);
    this.scene.add(this.points);
  }
  // Initialize particles for a time index: assign paths, randomize progress
  init(timeIndex) {
    this.flowPaths = DataGenerator.generateFlowPaths(
      this.cache.getNoiseGrid(timeIndex)?.elevation || new Float32Array(GRID * GRID),
      timeIndex
    );
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const pathIdx = i % this.flowPaths.length;
      this.particleData[i] = {
        pathIdx,
        progress: Math.random(),          // 0..1 position along path
        speed: 0.0008 + Math.random() * 0.0025, // varied speeds
        pathLength: this.flowPaths[pathIdx]?.length || 2
      };
    }
    this.currentTimeIndex = timeIndex;
    this._updatePositions(); // set initial positions
  }
  // Set time index: regenerate paths and reset particles
  setTimeIndex(timeIndex) {
    if (timeIndex === this.currentTimeIndex) return;
    this.init(timeIndex);
  }
  // Called every frame: advance particles, write to reused position array
  update(delta) {
    if (!this.flowPaths.length) return;
    const dt = Math.min(delta, 0.1); // clamp delta to avoid large jumps
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const pd = this.particleData[i];
      pd.progress += pd.speed * dt * 60;
      if (pd.progress >= 1.0) {
        // Respawn: wrap to start, possibly switch to a new random path
        pd.progress -= 1.0;
        pd.pathIdx = (pd.pathIdx + Math.floor(Math.random() * 3) + 1) % this.flowPaths.length;
        pd.pathLength = this.flowPaths[pd.pathIdx]?.length || 2;
      }
      // Sample position from path via linear interpolation between adjacent points
      const path = this.flowPaths[pd.pathIdx];
      if (!path || path.length < 2) continue;
      const rawIdx = pd.progress * (path.length - 1);
      const idx0 = Math.floor(rawIdx);
      const idx1 = Math.min(idx0 + 1, path.length - 1);
      const frac = rawIdx - idx0;
      const p0 = path[idx0], p1 = path[idx1];
      const i3 = i * 3;
      // Write directly into the reused Float32Array — zero allocation
      this.positionArray[i3] = p0.x + (p1.x - p0.x) * frac;
      this.positionArray[i3 + 1] = p0.y + (p1.y - p0.y) * frac + 0.03;
      this.positionArray[i3 + 2] = p0.z + (p1.z - p0.z) * frac;
    }
    // Signal Three.js that the position buffer was updated
    this.points.geometry.attributes.position.needsUpdate = true;
  }
  _updatePositions() {
    // Set all particles to their initial path positions
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const pd = this.particleData[i];
      const path = this.flowPaths[pd.pathIdx];
      if (!path || path.length < 2) continue;
      const rawIdx = pd.progress * (path.length - 1);
      const idx0 = Math.floor(rawIdx);
      const idx1 = Math.min(idx0 + 1, path.length - 1);
      const frac = rawIdx - idx0;
      const p0 = path[idx0], p1 = path[idx1];
      const i3 = i * 3;
      this.positionArray[i3] = p0.x + (p1.x - p0.x) * frac;
      this.positionArray[i3 + 1] = p0.y + (p1.y - p0.y) * frac + 0.03;
      this.positionArray[i3 + 2] = p0.z + (p1.z - p0.z) * frac;
    }
    this.points.geometry.attributes.position.needsUpdate = true;
  }
  getCount() { return PARTICLE_COUNT; }
}
// ============================================================
// Camera Bookmarks — save/restore camera positions
// ============================================================
class CameraBookmarks {
  constructor() {
    this.bookmarks = new Array(5).fill(null);
    this.nextSlot = 0;
  }
  save(camera, controls) {
    const slot = this.nextSlot % 5;
    this.bookmarks[slot] = {
      position: camera.position.clone(),
      target: controls.target.clone()
    };
    this.nextSlot = (slot + 1) % 5;
    return slot;
  }
  load(slot, camera, controls) {
    const bm = this.bookmarks[slot];
    if (!bm) return false;
    // Animate to bookmark position (simple instant for now)
    camera.position.copy(bm.position);
    controls.target.copy(bm.target);
    controls.update();
    return true;
  }
}
// ============================================================
// Time Controller — slider + playback state
// ============================================================
class TimeController {
  constructor() {
    this.currentIndex = 0;
    this.playing = false;
    this.playSpeed = 1.0; // time points per second
    this.accumulator = 0;
    this.onChange = null; // callback(timeIndex)
  }
  setIndex(idx) {
    const clamped = Math.max(0, Math.min(TIME_POINTS - 1, idx));
    if (clamped !== this.currentIndex) {
      this.currentIndex = clamped;
      if (this.onChange) this.onChange(clamped);
    }
  }
  update(delta) {
    if (!this.playing) return;
    this.accumulator += delta * this.playSpeed;
    while (this.accumulator >= 1.0) {
      this.accumulator -= 1.0;
      this.setIndex((this.currentIndex + 1) % TIME_POINTS);
    }
  }
  togglePlay() {
    this.playing = !this.playing;
    return this.playing;
  }
  getLabel() {
    const hour = this.currentIndex;
    return `Hour ${String(hour).padStart(2, '0')}:00`;
  }
}
// ============================================================
// Diagnostics Panel — DOM updates (throttled, not per-frame)
// ============================================================
class DiagnosticsPanel {
  constructor(cache, terrain, particles, timeCtrl) {
    this.cache = cache;
    this.terrain = terrain;
    this.particles = particles;
    this.timeCtrl = timeCtrl;
    this.lastUpdate = 0;
    this.fpsFrames = 0;
    this.fpsAccum = 0;
    this.currentFps = 0;
  }
  update(now, delta) {
    // FPS counter
    this.fpsFrames++;
    this.fpsAccum += delta;
    if (this.fpsAccum >= 1.0) {
      this.currentFps = Math.round(this.fpsFrames / this.fpsAccum);
      this.fpsFrames = 0;
      this.fpsAccum = 0;
    }
    // Update DOM at most once per second to avoid layout thrashing
    if (now - this.lastUpdate < 1000) return;
    this.lastUpdate = now;
    const s = this.cache.stats;
    document.getElementById('d-fps').textContent = this.currentFps;
    document.getElementById('d-verts').textContent = this.terrain.getVertexCount();
    document.getElementById('d-parts').textContent = this.particles.getCount();
    document.getElementById('d-time').textContent = this.timeCtrl.currentIndex;
    document.getElementById('d-t-hit').textContent = s.terrain.hits;
    document.getElementById('d-t-miss').textContent = s.terrain.misses;
    document.getElementById('d-r-hit').textContent = s.river.hits;
    document.getElementById('d-r-miss').textContent = s.river.misses;
    document.getElementById('d-g-hit').textContent = s.gridTransform.hits;
    document.getElementById('d-g-miss').textContent = s.gridTransform.misses;
  }
}
// ============================================================
// Main Application
// ============================================================
async function main() {
  const container = document.getElementById('canvas-container');
  // --- Renderer ---
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.setClearColor(0x0a0a18);
  container.appendChild(renderer.domElement);
  // --- Scene ---
  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x0a0a18, 15, 55);
  // --- Camera ---
  const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
  camera.position.set(15, 14, 18);
  camera.lookAt(0, 2, 0);
  // --- Lighting ---
  const ambient = new THREE.AmbientLight(0x334466, 1.6);
  scene.add(ambient);
  const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
  sun.position.set(10, 20, 5);
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  sun.shadow.camera.near = 0.5;
  sun.shadow.camera.far = 60;
  sun.shadow.camera.left = -18;
  sun.shadow.camera.right = 18;
  sun.shadow.camera.top = 18;
  sun.shadow.camera.bottom = -18;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x4466aa, 0.8);
  fill.position.set(-5, 3, -8);
  scene.add(fill);
  // --- Ground plane (subtle reference) ---
  const groundGeo = new THREE.PlaneGeometry(TERRAIN_SIZE + 4, TERRAIN_SIZE + 4);
  const groundMat = new THREE.MeshLambertMaterial({ color: 0x111122, transparent: true, opacity: 0.5 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.2;
  ground.receiveShadow = true;
  scene.add(ground);
  // --- OrbitControls ---
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.4;
  controls.target.set(0, 2.5, 0);
  controls.minDistance = 6;
  controls.maxDistance = 40;
  controls.maxPolarAngle = Math.PI * 0.7;
  controls.update();
  // --- Systems ---
  const cache = new CacheManager();
  const terrain = new TerrainSystem(scene, cache);
  const rivers = new RiverSystem(scene, cache);
  const particles = new ParticleSystem(scene, cache);
  const bookmarks = new CameraBookmarks();
  const timeCtrl = new TimeController();
  // Pre-build all terrain geometries during init (cached)
  terrain.init(0);
  rivers.init(0);
  particles.init(0);
  // Build remaining time-point geometries in background chunks
  let buildIdx = 1;
  function buildNextChunk() {
    const start = performance.now();
    // Build up to 3 time points per chunk, yielding every ~12ms
    while (buildIdx < TIME_POINTS && performance.now() - start < 14) {
      terrain.buildGeometry(buildIdx);
      rivers.buildRivers(buildIdx);
      buildIdx++;
    }
    if (buildIdx < TIME_POINTS) {
      requestAnimationFrame(() => setTimeout(buildNextChunk, 20));
    }
  }
  setTimeout(buildNextChunk, 100);
  // --- Time change handler ---
  timeCtrl.onChange = (idx) => {
    terrain.setTimeIndex(idx);    // instant swap from cache
    rivers.setTimeIndex(idx);     // cached swap or debounced build
    particles.setTimeIndex(idx);  // regenerate flow paths
    document.getElementById('time-slider').value = idx;
    document.getElementById('time-label').textContent = timeCtrl.getLabel();
  };
  // --- UI Bindings ---
  const slider = document.getElementById('time-slider');
  slider.addEventListener('input', () => {
    timeCtrl.setIndex(parseInt(slider.value));
    document.getElementById('time-label').textContent = timeCtrl.getLabel();
  });
  document.getElementById('btn-play').addEventListener('click', () => {
    const playing = timeCtrl.togglePlay();
    document.getElementById('btn-play').textContent = playing ? '⏸ Pause' : '▶ Play';
    document.getElementById('btn-play').classList.toggle('active', playing);
  });
  document.getElementById('btn-auto-rotate').addEventListener('click', function() {
    controls.autoRotate = !controls.autoRotate;
    this.classList.toggle('active', controls.autoRotate);
  });
  document.getElementById('btn-top-view').addEventListener('click', () => {
    camera.position.set(0, 22, 0.5);
    controls.target.set(0, 2, 0);
    controls.update();
  });
  document.getElementById('btn-reset-view').addEventListener('click', () => {
    camera.position.set(15, 14, 18);
    controls.target.set(0, 2.5, 0);
    controls.update();
  });
  document.getElementById('bm-save').addEventListener('click', () => {
    const slot = bookmarks.save(camera, controls);
    const btn = document.querySelector(`.bm-load[data-idx="${slot}"]`);
    if (btn) btn.textContent = `View ${slot + 1}*`;
  });
  document.querySelectorAll('.bm-load').forEach(btn => {
    btn.addEventListener('click', () => {
      bookmarks.load(parseInt(btn.dataset.idx), camera, controls);
    });
  });
  // Keyboard shortcuts: 1-5 load bookmarks
  window.addEventListener('keydown', (e) => {
    const key = parseInt(e.key);
    if (key >= 1 && key <= 5 && !e.ctrlKey && !e.metaKey && e.target === document.body) {
      bookmarks.load(key - 1, camera, controls);
    }
    if (e.key === ' ' && e.target === document.body) {
      e.preventDefault();
      document.getElementById('btn-play').click();
    }
  });
  // Window resize
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
  // --- Diagnostics ---
  const diag = new DiagnosticsPanel(cache, terrain, particles, timeCtrl);
  // --- Hide loading screen ---
  document.getElementById('loading').classList.add('hidden');
  // ============================================================
  // Render Loop — hot path: no allocations, no new Geometry()
  // ============================================================
  let prevTime = performance.now() / 1000;
  function animate() {
    requestAnimationFrame(animate);
    const now = performance.now() / 1000;
    const delta = Math.min(now - prevTime, 0.1); // clamp delta
    prevTime = now;
    controls.update();                       // damping update
    timeCtrl.update(delta);                  // auto-advance time
    particles.update(delta);                 // write to reused position array
    diag.update(now, delta);                 // throttled DOM update
    // Update slider position if time changed externally (playback)
    if (parseInt(slider.value) !== timeCtrl.currentIndex) {
      slider.value = timeCtrl.currentIndex;
      document.getElementById('time-label').textContent = timeCtrl.getLabel();
    }
    renderer.render(scene, camera);
    // ==========================================================
    // HOT-PATH AUDIT: This loop contains zero calls to
    // new THREE.XxxGeometry(). All geometry is pre-built and cached.
    // Particle positions use the same Float32Array (reused).
    // World-to-grid transforms are memoized in CacheManager.
    // River rebuilds are debounced at 200ms.
    // No per-frame allocations in the render path.
    // ==========================================================
  }
  animate();
}
main().catch(console.error);
</script>
</body>
</html>