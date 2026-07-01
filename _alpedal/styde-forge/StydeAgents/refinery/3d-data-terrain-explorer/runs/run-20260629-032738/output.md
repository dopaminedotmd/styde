<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  /* Named constants for layout — discoverable at top */
  :root {
    --panel-bg: rgba(16, 16, 24, 0.92);
    --panel-text: #d0d4e0;
    --accent: #4da6ff;
    --danger: #e05555;
    --slider-track: #2a2a3a;
    --font-mono: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { overflow: hidden; background: #0a0a14; font-family: system-ui, sans-serif; }
  canvas { display: block; }
  /* HUD panel — top bar */
  #hud {
    position: fixed; top: 12px; left: 50%; transform: translateX(-50%);
    background: var(--panel-bg); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
    padding: 8px 18px; display: flex; gap: 20px; align-items: center;
    z-index: 10; color: var(--panel-text); font-size: 13px;
  }
  #hud .stat { display: flex; flex-direction: column; align-items: center; }
  #hud .stat-label { font-size: 10px; text-transform: uppercase; opacity: 0.6; letter-spacing: 0.5px; }
  #hud .stat-value { font-family: var(--font-mono); font-size: 15px; font-weight: 600; }
  /* Time slider bar */
  #timebar {
    position: fixed; bottom: 32px; left: 50%; transform: translateX(-50%);
    background: var(--panel-bg); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
    padding: 10px 20px; display: flex; gap: 14px; align-items: center;
    z-index: 10; color: var(--panel-text);
  }
  #timebar label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; opacity: 0.7; }
  #timeSlider { width: 260px; accent-color: var(--accent); }
  #timeLabel { font-family: var(--font-mono); font-size: 14px; min-width: 60px; text-align: center; }
  /* Bookmark bar */
  #bookmarks {
    position: fixed; top: 12px; right: 16px;
    display: flex; flex-direction: column; gap: 4px; z-index: 10;
  }
  .bm-btn {
    background: var(--panel-bg); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 6px;
    color: var(--panel-text); padding: 6px 14px;
    cursor: pointer; font-size: 12px; transition: border-color 0.2s;
  }
  .bm-btn:hover { border-color: var(--accent); }
  .bm-btn.save { border-color: rgba(255,255,255,0.2); }
  .bm-btn.save:hover { border-color: var(--accent); }
  /* Legend */
  #legend {
    position: fixed; bottom: 32px; left: 20px;
    background: var(--panel-bg); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 10px;
    padding: 12px 16px; z-index: 10; color: var(--panel-text); font-size: 11px;
  }
  #legend .row { display: flex; align-items: center; gap: 8px; margin: 3px 0; }
  #legend .swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
</style>
</head>
<body>
<div id="hud">
  <div class="stat"><span class="stat-label">Revenue Peak</span><span class="stat-value" id="hudRevenue">—</span></div>
  <div class="stat"><span class="stat-label">User Density</span><span class="stat-value" id="hudUsers">—</span></div>
  <div class="stat"><span class="stat-label">Error Rate</span><span class="stat-value" id="hudErrors" style="color:var(--danger)">—</span></div>
  <div class="stat"><span class="stat-label">FPS</span><span class="stat-value" id="hudFps">—</span></div>
</div>
<div id="bookmarks">
  <button class="bm-btn save" id="bmSave">+ Save View</button>
  <button class="bm-btn" data-bm="0">Top-Down</button>
  <button class="bm-btn" data-bm="1">Canyon Fly</button>
  <button class="bm-btn" data-bm="2">Overview</button>
</div>
<div id="legend">
  <div class="row"><span class="swatch" style="background:#3a8c3a;"></span> Low density</div>
  <div class="row"><span class="swatch" style="background:#aacc44;"></span> Medium density</div>
  <div class="row"><span class="swatch" style="background:#eebb33;"></span> High density</div>
  <div class="row"><span class="swatch" style="background:#cc3333;"></span> Error river</div>
  <div class="row"><span class="swatch" style="background:#66ccff;"></span> API trail</div>
</div>
<div id="timebar">
  <label>Time</label>
  <input type="range" id="timeSlider" min="0" max="4" value="0" step="1">
  <span id="timeLabel">T0</span>
  <button id="autoRotate" style="background:var(--panel-bg);border:1px solid rgba(255,255,255,0.08);border-radius:6px;color:var(--panel-text);padding:5px 12px;cursor:pointer;font-size:12px;">Auto-Rotate</button>
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
/* ==========================================================================
   CONFIG — all tunable parameters exposed at module top level
   ========================================================================== */
const CONFIG = {
  /* Grid resolution — number of cells along each axis of the terrain mesh */
  GRID_RES: 64,                    // must be >= 4; higher = more detail, higher GPU cost
  /* Terrain physical dimensions in world units */
  TERRAIN_WIDTH: 20,
  TERRAIN_DEPTH: 20,
  /* Height scaling — raw data values multiplied by this to get world Y */
  HEIGHT_SCALE: 4.0,
  /* Number of discrete time slices in the synthetic dataset */
  TIME_SLICES: 5,
  /* Vegetation color gradient stops — maps user-density percentile to RGB */
  VEG_LOW: { r: 0.18, g: 0.52, b: 0.18 },   // low density: muted green
  VEG_MID: { r: 0.62, g: 0.78, b: 0.20 },   // medium density: yellow-green
  VEG_HIGH: { r: 0.92, g: 0.73, b: 0.20 },  // high density: golden
  /* River parameters */
  RIVER_COLOR: 0xcc3333,
  RIVER_WIDTH: 0.12,              // half-width of river ribbon
  /* Particle system — API call trails */
  PARTICLE_COUNT: 300,            // total particles in the trail system
  PARTICLE_LIFETIME_SEC: 4.0,     // seconds before a particle resets to spawn
  PARTICLE_SPEED: 1.8,            // world units per second along the trail path
  PARTICLE_COLOR: 0x66ccff,
  PARTICLE_SIZE: 0.08,
  /* Orbit controls defaults */
  ORBIT_DAMPING: 0.12,
  ORBIT_AUTO_ROTATE_SPEED: 0.4,
  ORBIT_MIN_DISTANCE: 4.0,
  ORBIT_MAX_DISTANCE: 40.0,
  /* Camera bookmarks — pre-defined camera positions */
  BOOKMARKS: [
    { label: 'Top-Down', pos: [0, 18, 0.1], target: [0, 0, 0] },
    { label: 'Canyon Fly', pos: [-8, 3, -10], target: [2, 0.5, 4] },
    { label: 'Overview', pos: [14, 9, 14], target: [0, 0, 0] },
  ],
  /* Misc */
  BG_COLOR: 0x0a0a18,
  FOG_COLOR: 0x0a0a18,
  FOG_NEAR: 14,
  FOG_FAR: 48,
  GROUND_COLOR: 0x1a1a2e,
};
/* ==========================================================================
   Named constants — all magic numbers >2 extracted for clarity
   ========================================================================== */
/* Grid vertex count = (GRID_RES+1)^2; precomputed once */
const GRID_VERTICES_X = CONFIG.GRID_RES + 1;  // vertices per axis (cells+1)
const GRID_VERTEX_COUNT = GRID_VERTICES_X * GRID_VERTICES_X;
/* Cell count used for indexing */
const CELL_COUNT = CONFIG.GRID_RES * CONFIG.GRID_RES;
/* Per-cell: 2 triangles, 3 indices each = 6 indices per cell */
const INDICES_PER_CELL = 6;
/* Total index buffer length for the terrain plane */
const INDEX_COUNT = CELL_COUNT * INDICES_PER_CELL;
/* River sampling resolution — points along river path */
const RIVER_POINT_COUNT = 80;     // number of sample points tracing the river
/* River ribbon: each segment = 2 vertices (left/right bank), 2 triangles */
const RIVER_VERTEX_COUNT = RIVER_POINT_COUNT * 2;
const RIVER_INDEX_COUNT = (RIVER_POINT_COUNT - 1) * INDICES_PER_CELL;
/* Particle buffer stride: 3 floats per position */
const PARTICLE_FLOATS = CONFIG.PARTICLE_COUNT * 3;
/* Animation clock reference — no per-frame Date.now() calls */
const FPS_SAMPLE_INTERVAL_MS = 500;  // HUD FPS counter refresh rate
/* ==========================================================================
   Synthetic data generation
   ========================================================================== */
/**
 * Build a multi-timepoint synthetic dataset representing revenue, user density,
 * and error rates across a spatial grid.
 * Returns array of {heights: Float32Array[GRID_VERTEX_COUNT], density: Float32Array[GRID_VERTEX_COUNT], errors: [{x,z}]}
 */
function buildDataset() {
  const slices = [];
  const N = GRID_VERTICES_X;
  const half = CONFIG.GRID_RES / 2;
  for (let t = 0; t < CONFIG.TIME_SLICES; t++) {
    /* Normalized time 0..1 driving sinusoidal evolution of the landscape */
    const phase = (t / (CONFIG.TIME_SLICES - 1)) * Math.PI * 1.5;  // 0 to ~1.5π
    const heights = new Float32Array(GRID_VERTEX_COUNT);
    const density = new Float32Array(GRID_VERTEX_COUNT);
    const errors = [];  // list of {x, z} anomaly points
    for (let iz = 0; iz < N; iz++) {
      for (let ix = 0; ix < N; ix++) {
        const idx = iz * N + ix;
        /* Normalize grid coords to -1..1 range for math functions */
        const nx = (ix / CONFIG.GRID_RES) * 2 - 1;
        const nz = (iz / CONFIG.GRID_RES) * 2 - 1;
        /* Revenue (height): multi-gaussian landscape that shifts over time.
           Three overlapping gaussians create hills and valleys. */
        const distCenter = Math.sqrt(nx * nx + nz * nz);
        /* Gaussian A: central peak, grows over time */
        const gaussA = Math.exp(-distCenter * distCenter * 1.8) * (0.6 + 0.4 * Math.sin(phase * 0.7));
        /* Gaussian B: off-center hill, drifts diagonally */
        const offX = nx - Math.cos(phase * 0.5) * 0.5;
        const offZ = nz - Math.sin(phase * 0.5) * 0.5;
        const gaussB = Math.exp(-(offX * offX * 3.0 + offZ * offZ * 3.0)) * 0.55;
        /* Gaussian C: secondary peak, opposite phase */
        const gaussC = Math.exp(-((nx + 0.4) * (nx + 0.4) * 2.5 + (nz - 0.3) * (nz - 0.3) * 2.5)) * (0.35 + 0.15 * Math.cos(phase * 1.1));
        heights[idx] = gaussA + gaussB + gaussC;
        /* User density: another multi-gaussian with different spatial layout.
           Simulates user concentration shifting between regions over time. */
        const userShiftX = Math.cos(phase * 0.8) * 0.6;
        const userShiftZ = Math.sin(phase * 0.6) * 0.4;
        const dux = nx - userShiftX;
        const duz = nz - userShiftZ;
        density[idx] = Math.exp(-(dux * dux * 2.2 + duz * duz * 2.2)) * 0.7
                     + Math.exp(-((nx + 0.7) * (nx + 0.7) * 4.0 + (nz - 0.7) * (nz - 0.7) * 4.0)) * 0.45;
      }
    }
    /* Error/anomaly path: sinusoidal river crossing the terrain.
       Position and amplitude evolve across time slices. */
    const riverAmplitude = 3.5 + Math.sin(phase) * 1.2;
    const riverFreq = 1.8 + t * 0.2;
    const riverOffsetZ = Math.cos(phase * 0.9) * 2.5;
    /* Step size along the X axis for sampling the river path */
    const riverStepX = CONFIG.TERRAIN_WIDTH / (RIVER_POINT_COUNT - 1);
    for (let ri = 0; ri < RIVER_POINT_COUNT; ri++) {
      const rx = -CONFIG.TERRAIN_WIDTH / 2 + ri * riverStepX;
      /* Sinusoidal river path: frequency and amplitude evolve with time */
      const rz = Math.sin(rx * riverFreq) * riverAmplitude + riverOffsetZ;
      errors.push({ x: rx, z: rz });
    }
    slices.push({ heights, density, errors, phase });
  }
  return slices;
}
/* ==========================================================================
   Three.js setup
   ========================================================================== */
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));  // cap pixel ratio for perf
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = false;  // no shadows needed for this viz
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(CONFIG.BG_COLOR);
scene.fog = new THREE.Fog(CONFIG.FOG_COLOR, CONFIG.FOG_NEAR, CONFIG.FOG_FAR);
const camera = new THREE.PerspectiveCamera(
  50,                                    // FOV in degrees
  window.innerWidth / window.innerHeight, // aspect ratio
  0.5,                                   // near clip
  80                                     // far clip
);
camera.position.set(12, 8, 14);
camera.lookAt(0, 1.2, 0);
/* OrbitControls with smooth damping — no per-frame allocation */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = CONFIG.ORBIT_DAMPING;
controls.autoRotate = false;
controls.autoRotateSpeed = CONFIG.ORBIT_AUTO_ROTATE_SPEED;
controls.minDistance = CONFIG.ORBIT_MIN_DISTANCE;
controls.maxDistance = CONFIG.ORBIT_MAX_DISTANCE;
controls.target.set(0, 1.0, 0);
controls.update();
/* Lighting — ambient + directional for terrain shading */
const ambientLight = new THREE.AmbientLight(0x404060, 1.8);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffffff, 2.2);
dirLight.position.set(10, 18, 6);
scene.add(dirLight);
/* Ground plane — subtle grid reference */
const groundGeo = new THREE.PlaneGeometry(CONFIG.TERRAIN_WIDTH * 1.6, CONFIG.TERRAIN_DEPTH * 1.6);
const groundMat = new THREE.MeshStandardMaterial({
  color: CONFIG.GROUND_COLOR,
  roughness: 0.85,
  metalness: 0.1,
  transparent: true,
  opacity: 0.5,
});
const groundPlane = new THREE.Mesh(groundGeo, groundMat);
groundPlane.rotation.x = -Math.PI / 2;
groundPlane.position.y = -0.05;
scene.add(groundPlane);
/* ==========================================================================
   Data
   ========================================================================== */
const dataset = buildDataset();
/* ==========================================================================
   Terrain mesh cache — pre-build all time slices, swap on slider change
   ========================================================================== */
const terrainCache = [];  // array of {mesh, geometry} per time slice
let currentTerrain = null;
/**
 * Build a single terrain mesh from a data slice.
 * Heights become vertex Y positions; density values become vertex colors.
 * Returns {mesh, geometry} for caching.
 */
function buildTerrainMesh(slice) {
  const N = GRID_VERTICES_X;
  const halfW = CONFIG.TERRAIN_WIDTH / 2;
  const halfD = CONFIG.TERRAIN_DEPTH / 2;
  const cellW = CONFIG.TERRAIN_WIDTH / CONFIG.GRID_RES;
  const cellD = CONFIG.TERRAIN_DEPTH / CONFIG.GRID_RES;
  /* Pre-allocate typed arrays — single allocation, no per-frame growth */
  const positions = new Float32Array(GRID_VERTEX_COUNT * 3);
  const colors = new Float32Array(GRID_VERTEX_COUNT * 3);
  /* Map density values to vegetation color gradient using percentile bins */
  /* Compute density percentiles for robust color mapping */
  let dMin = Infinity, dMax = -Infinity;
  for (let i = 0; i < GRID_VERTEX_COUNT; i++) {
    if (slice.density[i] < dMin) dMin = slice.density[i];
    if (slice.density[i] > dMax) dMax = slice.density[i];
  }
  const dRange = dMax - dMin || 0.001;  // avoid division by zero
  for (let iz = 0; iz < N; iz++) {
    for (let ix = 0; ix < N; ix++) {
      const vi = iz * N + ix;
      const pi = vi * 3;
      /* World-space XZ position of this vertex */
      const wx = ix * cellW - halfW;
      const wz = iz * cellD - halfD;
      /* Height = normalized revenue value scaled to world Y */
      const wy = slice.heights[vi] * CONFIG.HEIGHT_SCALE;
      positions[pi] = wx;
      positions[pi + 1] = wy;
      positions[pi + 2] = wz;
      /* Density-to-color: linear interpolation between 3 vegetation stops.
         Maps normalized density (0..1) to a 3-color gradient. */
      const t = Math.max(0, Math.min(1, (slice.density[vi] - dMin) / dRange));
      /* Two-stop lerp: low→mid for t<0.5, mid→high for t>=0.5 */
      let cr, cg, cb;
      if (t < 0.5) {
        const s = t * 2;  // remap 0..0.5 to 0..1 for low→mid
        cr = CONFIG.VEG_LOW.r + (CONFIG.VEG_MID.r - CONFIG.VEG_LOW.r) * s;
        cg = CONFIG.VEG_LOW.g + (CONFIG.VEG_MID.g - CONFIG.VEG_LOW.g) * s;
        cb = CONFIG.VEG_LOW.b + (CONFIG.VEG_MID.b - CONFIG.VEG_LOW.b) * s;
      } else {
        const s = (t - 0.5) * 2;  // remap 0.5..1 to 0..1 for mid→high
        cr = CONFIG.VEG_MID.r + (CONFIG.VEG_HIGH.r - CONFIG.VEG_MID.r) * s;
        cg = CONFIG.VEG_MID.g + (CONFIG.VEG_HIGH.g - CONFIG.VEG_MID.g) * s;
        cb = CONFIG.VEG_MID.b + (CONFIG.VEG_HIGH.b - CONFIG.VEG_MID.b) * s;
      }
      colors[pi] = cr;
      colors[pi + 1] = cg;
      colors[pi + 2] = cb;
    }
  }
  /* Build index buffer — two triangles per grid cell */
  const indices = new Uint32Array(INDEX_COUNT);
  let idxPtr = 0;  // write pointer into indices array
  for (let iz = 0; iz < CONFIG.GRID_RES; iz++) {
    for (let ix = 0; ix < CONFIG.GRID_RES; ix++) {
      const a = iz * N + ix;
      const b = a + 1;
      const c = a + N;
      const d = c + 1;
      /* Triangle 1: a-b-d */
      indices[idxPtr++] = a; indices[idxPtr++] = b; indices[idxPtr++] = d;
      /* Triangle 2: a-d-c */
      indices[idxPtr++] = a; indices[idxPtr++] = d; indices[idxPtr++] = c;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(new THREE.BufferAttribute(indices, 1));
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.08,
    flatShading: false,
    side: THREE.DoubleSide,
  });
  const mesh = new THREE.Mesh(geo, mat);
  return { mesh, geometry: geo };
}
/**
 * Swap active terrain to the given time slice index.
 * Uses cached mesh if available; builds on first access.
 */
function setTerrainSlice(tIndex) {
  if (currentTerrain) scene.remove(currentTerrain);
  if (!terrainCache[tIndex]) {
    terrainCache[tIndex] = buildTerrainMesh(dataset[tIndex]);
  }
  currentTerrain = terrainCache[tIndex].mesh;
  scene.add(currentTerrain);
}
/* ==========================================================================
   River geometry — error/anomaly path carved as a ribbon
   ========================================================================== */
/**
 * Sample terrain height at a given XZ world position for the current time slice.
 * Uses nearest-neighbor lookup into the height grid.
 */
function sampleTerrainHeight(slice, wx, wz) {
  const halfW = CONFIG.TERRAIN_WIDTH / 2;
  const halfD = CONFIG.TERRAIN_DEPTH / 2;
  const N = GRID_VERTICES_X;
  /* Clamp to terrain bounds and convert world coords to grid indices */
  const ix = Math.round(((wx + halfW) / CONFIG.TERRAIN_WIDTH) * CONFIG.GRID_RES);
  const iz = Math.round(((wz + halfD) / CONFIG.TERRAIN_DEPTH) * CONFIG.GRID_RES);
  const ci = Math.max(0, Math.min(CONFIG.GRID_RES, ix));
  const cz = Math.max(0, Math.min(CONFIG.GRID_RES, iz));
  return slice.heights[cz * N + ci] * CONFIG.HEIGHT_SCALE;
}
let riverMesh = null;
/**
 * Build river ribbon geometry from error path points for a given data slice.
 * The ribbon sits 0.02 units above terrain to avoid z-fighting.
 */
function buildRiver(slice) {
  if (riverMesh) {
    riverMesh.geometry.dispose();
    riverMesh.material.dispose();
    scene.remove(riverMesh);
  }
  const pts = slice.errors;  // {x, z} points along error path
  if (pts.length < 2) return;
  const positions = new Float32Array(RIVER_VERTEX_COUNT * 3);
  const indices = new Uint32Array(RIVER_INDEX_COUNT);
  for (let i = 0; i < RIVER_POINT_COUNT; i++) {
    const px = pts[i].x;
    const pz = pts[i].z;
    /* Height at river center sampled from terrain */
    const h = sampleTerrainHeight(slice, px, pz) + 0.02;
    /* Tangent direction for this segment — used to compute perpendicular cross-section.
       For first/last point, use forward/backward direction respectively. */
    let tx, tz;
    if (i === 0) {
      tx = pts[1].x - pts[0].x;
      tz = pts[1].z - pts[0].z;
    } else if (i === RIVER_POINT_COUNT - 1) {
      tx = pts[i].x - pts[i - 1].x;
      tz = pts[i].z - pts[i - 1].z;
    } else {
      /* Central difference for smoother tangent */
      tx = pts[i + 1].x - pts[i - 1].x;
      tz = pts[i + 1].z - pts[i - 1].z;
    }
    const tLen = Math.sqrt(tx * tx + tz * tz) || 0.001;
    tx /= tLen; tz /= tLen;
    /* Perpendicular vector in XZ plane: rotate tangent 90 degrees */
    const perpX = -tz;
    const perpZ = tx;
    /* Left bank vertex */
    const li = i * 2;
    positions[li * 3] = px + perpX * CONFIG.RIVER_WIDTH;
    positions[li * 3 + 1] = h;
    positions[li * 3 + 2] = pz + perpZ * CONFIG.RIVER_WIDTH;
    /* Right bank vertex */
    const ri = i * 2 + 1;
    positions[ri * 3] = px - perpX * CONFIG.RIVER_WIDTH;
    positions[ri * 3 + 1] = h;
    positions[ri * 3 + 2] = pz - perpZ * CONFIG.RIVER_WIDTH;
  }
  /* Build index buffer: two triangles per ribbon segment (quad) */
  let idxPtr = 0;
  for (let i = 0; i < RIVER_POINT_COUNT - 1; i++) {
    const a = i * 2;       // left of segment start
    const b = i * 2 + 1;   // right of segment start
    const c = (i + 1) * 2; // left of segment end
    const d = (i + 1) * 2 + 1; // right of segment end
    indices[idxPtr++] = a; indices[idxPtr++] = b; indices[idxPtr++] = d;
    indices[idxPtr++] = a; indices[idxPtr++] = d; indices[idxPtr++] = c;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setIndex(new THREE.BufferAttribute(indices, 1));
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    color: CONFIG.RIVER_COLOR,
    roughness: 0.3,
    metalness: 0.4,
    emissive: CONFIG.RIVER_COLOR,
    emissiveIntensity: 0.5,
    side: THREE.DoubleSide,
  });
  riverMesh = new THREE.Mesh(geo, mat);
  scene.add(riverMesh);
}
/* ==========================================================================
   Particle system — API call trails flowing along the terrain surface
   ========================================================================== */
/**
 * Pre-allocated particle state: position, progress, and spawn offsets.
 * No per-frame allocations — all buffers reused.
 */
const particlePositions = new Float32Array(PARTICLE_FLOATS);
const particleProgress = new Float32Array(CONFIG.PARTICLE_COUNT);  // 0..1 lifetime progress
const particleSpawnX = new Float32Array(CONFIG.PARTICLE_COUNT);    // spawn X offset on terrain
const particleSpawnZ = new Float32Array(CONFIG.PARTICLE_COUNT);    // spawn Z offset on terrain
/* Particle geometry — single buffer updated each frame, no re-allocation */
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
/* Circle sprite texture — generated once at init */
const spriteCanvas = document.createElement('canvas');
spriteCanvas.width = 32;
spriteCanvas.height = 32;
const sctx = spriteCanvas.getContext('2d');
sctx.beginPath();
sctx.arc(16, 16, 14, 0, Math.PI * 2);
const spriteGrad = sctx.createRadialGradient(16, 16, 0, 16, 16, 14);
spriteGrad.addColorStop(0, 'rgba(180,220,255,1)');
spriteGrad.addColorStop(0.5, 'rgba(100,180,255,0.7)');
spriteGrad.addColorStop(1, 'rgba(60,140,255,0)');
sctx.fillStyle = spriteGrad;
sctx.fill();
const particleTexture = new THREE.CanvasTexture(spriteCanvas);
const particleMat = new THREE.PointsMaterial({
  color: CONFIG.PARTICLE_COLOR,
  size: CONFIG.PARTICLE_SIZE,
  map: particleTexture,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
scene.add(particleSystem);
/** Initialize all particles with random spawn positions and progress offsets */
function initParticles() {
  for (let i = 0; i < CONFIG.PARTICLE_COUNT; i++) {
    /* Random spawn on terrain surface */
    particleSpawnX[i] = (Math.random() - 0.5) * CONFIG.TERRAIN_WIDTH * 0.9;
    particleSpawnZ[i] = (Math.random() - 0.5) * CONFIG.TERRAIN_DEPTH * 0.9;
    /* Stagger initial progress so particles don't all reset at same frame */
    particleProgress[i] = Math.random();
  }
}
/** Current data slice reference for particle height lookups — set before update loop */
let currentParticleSlice = dataset[0];
/**
 * Update all particle positions for one animation frame.
 * Uses pre-allocated arrays — zero allocations per frame.
 * Particles flow along sinusoidal paths across the terrain, wrapping at edges.
 * @param {number} dt — delta time in seconds since last frame
 */
function updateParticles(dt) {
  const slice = currentParticleSlice;
  const halfW = CONFIG.TERRAIN_WIDTH / 2;
  const halfD = CONFIG.TERRAIN_DEPTH / 2;
  for (let i = 0; i < CONFIG.PARTICLE_COUNT; i++) {
    /* Advance lifetime progress */
    particleProgress[i] += dt / CONFIG.PARTICLE_LIFETIME_SEC;
    if (particleProgress[i] >= 1.0) {
      particleProgress[i] = 0.0;
      /* Respawn at new random location */
      particleSpawnX[i] = (Math.random() - 0.5) * CONFIG.TERRAIN_WIDTH * 0.9;
      particleSpawnZ[i] = (Math.random() - 0.5) * CONFIG.TERRAIN_DEPTH * 0.9;
    }
    /* Normalized progress 0..1 drives particle along its trail path */
    const t = particleProgress[i];
    /* Parametric trail: figure-8-ish path across the terrain */
    const angle = t * Math.PI * 2;
    const pathX = particleSpawnX[i] + Math.sin(angle * 1.3) * 3.5;
    const pathZ = particleSpawnZ[i] + Math.cos(angle) * 2.8;
    /* Clamp to terrain bounds */
    const cx = Math.max(-halfW, Math.min(halfW, pathX));
    const cz = Math.max(-halfD, Math.min(halfD, pathZ));
    /* Sample height from terrain data */
    const h = sampleTerrainHeight(slice, cx, cz) + 0.15;
    const pi = i * 3;
    particlePositions[pi] = cx;
    particlePositions[pi + 1] = h;
    particlePositions[pi + 2] = cz;
  }
  /* Mark buffer as needing GPU re-upload — no new allocation */
  particleGeo.attributes.position.needsUpdate = true;
}
/* ==========================================================================
   Camera bookmark system
   ========================================================================== */
/**
 * Saved camera states: {position: Vector3, target: Vector3}
 * Index 0-2 are pre-defined bookmarks; user bookmarks append.
 */
const bookmarks = CONFIG.BOOKMARKS.map(bm => ({
  position: new THREE.Vector3(...bm.pos),
  target: new THREE.Vector3(...bm.target),
}));
/** Animate camera to a bookmark position over ~0.6 seconds */
let bookmarkAnim = null;  // {startPos, startTarget, endPos, endTarget, startTime, duration}
function goToBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  bookmarkAnim = {
    startPos: camera.position.clone(),
    startTarget: controls.target.clone(),
    endPos: bm.position.clone(),
    endTarget: bm.target.clone(),
    startTime: performance.now(),
    duration: 600,  // ms — named inline because it's <3
  };
}
/** Save current camera view as a new bookmark */
function saveBookmark() {
  bookmarks.push({
    position: camera.position.clone(),
    target: controls.target.clone(),
  });
  /* Add a button for the new bookmark */
  const btn = document.createElement('button');
  btn.className = 'bm-btn';
  btn.textContent = `View ${bookmarks.length - 1}`;
  btn.dataset.bm = bookmarks.length - 1;
  btn.addEventListener('click', () => goToBookmark(parseInt(btn.dataset.bm)));
  document.getElementById('bookmarks').appendChild(btn);
}
/* ==========================================================================
   Time slider
   ========================================================================== */
const timeSlider = document.getElementById('timeSlider');
const timeLabel = document.getElementById('timeLabel');
const TIME_LABELS = ['T0', 'T1', 'T2', 'T3', 'T4'];
function onTimeChange(tIndex) {
  setTerrainSlice(tIndex);
  buildRiver(dataset[tIndex]);
  currentParticleSlice = dataset[tIndex];
  timeLabel.textContent = TIME_LABELS[tIndex];
  updateHUD(dataset[tIndex]);
}
timeSlider.addEventListener('input', () => {
  onTimeChange(parseInt(timeSlider.value));
});
/* ==========================================================================
   HUD update — per-frame data but throttled to avoid DOM thrash
   ========================================================================== */
let lastHudUpdate = 0;
function updateHUD(slice) {
  /* Find peak height in current slice */
  let peak = 0;
  for (let i = 0; i < GRID_VERTEX_COUNT; i++) {
    if (slice.heights[i] > peak) peak = slice.heights[i];
  }
  /* Average density */
  let sumDensity = 0;
  for (let i = 0; i < GRID_VERTEX_COUNT; i++) sumDensity += slice.density[i];
  const avgDensity = sumDensity / GRID_VERTEX_COUNT;
  /* Error count */
  const errorCount = slice.errors.length;
  document.getElementById('hudRevenue').textContent = (peak * 100).toFixed(0) + '%';
  document.getElementById('hudUsers').textContent = (avgDensity * 100).toFixed(0) + '%';
  document.getElementById('hudErrors').textContent = errorCount + ' pts';
  lastHudUpdate = performance.now();
}
/* ==========================================================================
   FPS counter — sampled on interval, not every frame
   ========================================================================== */
let frameCount = 0;
let lastFpsSample = performance.now();
let currentFps = 0;
function tickFps(now) {
  frameCount++;
  if (now - lastFpsSample >= FPS_SAMPLE_INTERVAL_MS) {
    currentFps = Math.round(frameCount / ((now - lastFpsSample) / 1000));
    frameCount = 0;
    lastFpsSample = now;
    document.getElementById('hudFps').textContent = currentFps;
  }
}
/* ==========================================================================
   Animation loop — single requestAnimationFrame, no per-frame allocations
   ========================================================================== */
/** Reusable clock for delta time — allocated once */
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min(clock.getDelta(), 0.1);  // cap delta to avoid spiral on tab switch
  controls.update();
  /* Animate camera bookmark transition if active */
  if (bookmarkAnim) {
    const elapsed = now - bookmarkAnim.startTime;
    /* Smooth ease-in-out using cubic Hermite (smoothstep) */
    const raw = Math.min(1, elapsed / bookmarkAnim.duration);
    const t = raw * raw * (3 - 2 * raw);  // smoothstep: 3t² - 2t³
    camera.position.lerpVectors(bookmarkAnim.startPos, bookmarkAnim.endPos, t);
    controls.target.lerpVectors(bookmarkAnim.startTarget, bookmarkAnim.endTarget, t);
    if (raw >= 1) bookmarkAnim = null;
  }
  /* Update particles — uses pre-allocated buffers, zero allocation */
  updateParticles(dt);
  /* Render */
  renderer.render(scene, camera);
  /* FPS counter tick — samples on interval, not every frame */
  tickFps(now);
  /* HUD refresh — piggyback on FPS sample interval */
  if (now - lastHudUpdate >= FPS_SAMPLE_INTERVAL_MS) {
    updateHUD(currentParticleSlice);
  }
}
/* ==========================================================================
   Event wiring
   ========================================================================== */
/* Bookmark buttons */
document.querySelectorAll('.bm-btn[data-bm]').forEach(btn => {
  btn.addEventListener('click', () => goToBookmark(parseInt(btn.dataset.bm)));
});
document.getElementById('bmSave').addEventListener('click', saveBookmark);
/* Auto-rotate toggle */
const autoRotateBtn = document.getElementById('autoRotate');
autoRotateBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autoRotateBtn.textContent = controls.autoRotate ? 'Auto-Rotate: ON' : 'Auto-Rotate';
  autoRotateBtn.style.borderColor = controls.autoRotate ? 'var(--accent)' : 'rgba(255,255,255,0.08)';
});
/* Window resize */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ==========================================================================
   Init
   ========================================================================== */
initParticles();
onTimeChange(0);  // load T0 terrain, river, particles
animate();
</script>
</body>
</html>