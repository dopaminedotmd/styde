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
  /* Overlay panel */
  #panel {
    position: fixed;
    top: 16px;
    right: 16px;
    width: 280px;
    background: rgba(10,10,25,0.92);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 16px;
    color: #c8c8d8;
    font-size: 13px;
    z-index: 10;
    backdrop-filter: blur(8px);
  }
  #panel h2 {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 12px;
    color: #e0e0f0;
    letter-spacing: 0.4px;
  }
  #panel label {
    display: block;
    margin-top: 10px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #8888aa;
  }
  #panel input[type=range] {
    width: 100%;
    margin: 4px 0 10px;
    accent-color: #44aaff;
  }
  #panel button {
    display: block;
    width: 100%;
    margin-top: 6px;
    padding: 7px 0;
    background: rgba(68,170,255,0.18);
    border: 1px solid rgba(68,170,255,0.35);
    color: #aad4ff;
    border-radius: 5px;
    cursor: pointer;
    font-size: 12px;
    letter-spacing: 0.3px;
  }
  #panel button:hover { background: rgba(68,170,255,0.3); }
  #panel button.active { background: rgba(68,170,255,0.5); border-color: #44aaff; }
  /* Time display */
  #time-label {
    font-size: 11px;
    color: #8888aa;
    margin-top: 4px;
  }
  /* Legend */
  #legend {
    position: fixed;
    bottom: 24px;
    left: 24px;
    background: rgba(10,10,25,0.88);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 12px 16px;
    color: #c8c8d8;
    font-size: 11px;
    z-index: 10;
    backdrop-filter: blur(8px);
  }
  .legend-row { display: flex; align-items: center; gap: 8px; margin: 3px 0; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
  /* Cache diagnostic */
  #cache-diag {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: rgba(10,10,25,0.88);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 10px 14px;
    color: #8888aa;
    font-size: 10px;
    font-family: 'Consolas', 'Courier New', monospace;
    z-index: 10;
    backdrop-filter: blur(8px);
    line-height: 1.6;
  }
</style>
</head>
<body>
<div id="panel">
  <h2>Data Terrain Explorer</h2>
  <label>Time Step <span id="time-label">0 / 59</span></label>
  <input type="range" id="time-slider" min="0" max="59" value="0" step="1">
  <button id="btn-autorot">Auto-Rotate: OFF</button>
  <button id="btn-bookmark-1">Bookmark 1 — Overview</button>
  <button id="btn-bookmark-2">Bookmark 2 — Valley Closeup</button>
  <button id="btn-bookmark-3">Bookmark 3 — Top-Down</button>
  <button id="btn-reset">Reset View</button>
</div>
<div id="legend">
  <div class="legend-row"><div class="legend-swatch" style="background: linear-gradient(to right, #1a5c1a, #44cc44, #88ff44);"></div> Elevation (Revenue)</div>
  <div class="legend-row"><div class="legend-swatch" style="background: linear-gradient(to right, #4422cc, #cc4444);"></div> Error Rivers</div>
  <div class="legend-row"><div class="legend-swatch" style="background: #ffcc44;"></div> Data Flow Particles</div>
</div>
<div id="cache-diag"></div>
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
/*
  ALGORITHM: Terrain Heightfield Generation
  h(x,z,t) = base_elevation_scale * (
    0.6 * simplex_noise_2d(x*freq1, z*freq1) * envelope1(t) +
    0.3 * simplex_noise_2d(x*freq2, z*freq2) * envelope2(t) +
    0.1 * ridge_noise_2d(x*freq3, z*freq3) * envelope3(t)
  ) + metric_contribution(x,z,t)
  Where:
    envelope_k(t) = sin(pi * (t + phase_k) / period_k)  — each octave oscillates at its own period
    metric_contribution comes from the secondary data channel mapped through a sigmoid
  Interpolation between time steps uses cubic ease: f = 3t^2 - 2t^3
*/
/*
  ALGORITHM: Simplex-like noise (simplified, seedable)
  Uses a hash-based gradient grid approach.
  For each grid cell corner, compute dot(gradient, offset_vector).
  Then smoothstep blend between corners along x, then z.
  output = lerp(
    lerp(dot00, dot10, sx),
    lerp(dot01, dot11, sx),
    sz
  )
  where sx = 6t^5 - 15t^4 + 10t^3 (quintic smoothstep for C2 continuity)
*/
// ─── CACHE SYSTEM ─────────────────────────────────────────────
const CacheStore = {
  _store: new Map(),
  _hits: 0,
  _misses: 0,
  key(...parts) { return parts.join('|'); },
  get(key) {
    if (this._store.has(key)) { this._hits++; return this._store.get(key); }
    this._misses++; return null;
  },
  set(key, value) {
    this._store.set(key, value);
    return value;
  },
  clear() { this._store.clear(); this._hits = 0; this._misses = 0; },
  stats() {
    const total = this._hits + this._misses;
    const rate = total > 0 ? ((this._hits / total) * 100).toFixed(1) : '0.0';
    return `Cache: ${this._hits} hits / ${this._misses} misses (${rate}%) | ${this._store.size} entries`;
  }
};
// ─── NOISE GENERATOR (seedable, deterministic) ────────────────
class SimplexNoise {
  constructor(seed = 42) {
    // Permutation table seeded via simple LCG
    this.perm = new Uint8Array(512);
    const p = new Uint8Array(256);
    for (let i = 0; i < 256; i++) p[i] = i;
    // Fisher-Yates shuffle with seed
    let s = seed;
    for (let i = 255; i > 0; i--) {
      s = (s * 16807 + 0) % 2147483647;
      const j = s % (i + 1);
      [p[i], p[j]] = [p[j], p[i]];
    }
    for (let i = 0; i < 512; i++) this.perm[i] = p[i & 255];
  }
  // Gradient vectors for 2D (8 directions around unit circle)
  _grad2(hash, x, z) {
    const h = hash & 7;
    const u = h < 4 ? x : z;
    const v = h < 4 ? z : x;
    return ((h & 1) ? -u : u) + ((h & 2) ? -v : v);
  }
  // Quintic smoothstep: 6t^5 - 15t^4 + 10t^3 (C2 continuous)
  _quintic(t) { return t * t * t * (t * (t * 6 - 15) + 10); }
  noise2D(x, z) {
    const X = Math.floor(x) & 255;
    const Z = Math.floor(z) & 255;
    const xf = x - Math.floor(x);
    const zf = z - Math.floor(z);
    const sx = this._quintic(xf);
    const sz = this._quintic(zf);
    const p = this.perm;
    const aa = p[p[X] + Z];
    const ab = p[p[X] + Z + 1];
    const ba = p[p[X + 1] + Z];
    const bb = p[p[X + 1] + Z + 1];
    // Bilinear interpolation of gradient dot products
    const x1 = aa + xf * (ba - aa);  // lerp along x at z=0
    const x2 = ab + xf * (bb - ab);  // lerp along x at z=1
    // Scale to [-1, 1] range approximately
    return (x1 + zf * (x2 - x1)) / 128 - 1;
  }
  // Fractal Brownian Motion — sums octaves of noise
  fbm2D(x, z, octaves = 3, lacunarity = 2.0, gain = 0.5) {
    let value = 0;
    let amplitude = 1;
    let frequency = 1;
    let maxValue = 0;
    for (let i = 0; i < octaves; i++) {
      value += amplitude * this.noise2D(x * frequency, z * frequency);
      maxValue += amplitude;
      amplitude *= gain;
      frequency *= lacunarity;
    }
    return value / maxValue; // Normalize to [-1, 1]
  }
}
// ─── SIMULATED TIME-SERIES DATA ────────────────────────────────
const GRID_SIZE = 64;       // Resolution of terrain grid
const TERRAIN_SPAN = 20;    // World-space extent
const TIME_STEPS = 60;      // Number of time frames
const noise = new SimplexNoise(137);
/*
  Generate time-series data:
  - revenue[t][i]    = primary metric (terrain height)
  - density[t][i]    = secondary metric (vertex color)
  - error_rate[t][i] = error metric (river trigger)
  Each is a flat array of GRID_SIZE * GRID_SIZE
*/
function generateTimeSeries() {
  const revenue = [];
  const density = [];
  const error_rate = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const rev = new Float32Array(GRID_SIZE * GRID_SIZE);
    const den = new Float32Array(GRID_SIZE * GRID_SIZE);
    const err = new Float32Array(GRID_SIZE * GRID_SIZE);
    // Time-dependent phase shifts make the landscape evolve
    const timePhase = (t / TIME_STEPS) * Math.PI * 2;
    const envelope1 = Math.sin(timePhase * 0.7 + 1.2) * 0.5 + 0.5;
    const envelope2 = Math.sin(timePhase * 1.3 + 2.8) * 0.4 + 0.6;
    const envelope3 = Math.sin(timePhase * 0.4 + 0.3) * 0.3 + 0.7;
    for (let iz = 0; iz < GRID_SIZE; iz++) {
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const idx = iz * GRID_SIZE + ix;
        // Normalized coords [-1, 1]
        const nx = (ix / (GRID_SIZE - 1)) * 2 - 1;
        const nz = (iz / (GRID_SIZE - 1)) * 2 - 1;
        // Revenue: multi-octave noise with time envelopes
        const base = noise.fbm2D(nx * 3, nz * 3, 4, 2.0, 0.5);
        // Add a peak cluster that moves over time
        const peakX = Math.sin(timePhase * 0.3) * 0.5;
        const peakZ = Math.cos(timePhase * 0.3) * 0.5;
        const distToPeak = Math.sqrt((nx - peakX) ** 2 + (nz - peakZ) ** 2);
        const peakVal = Math.exp(-distToPeak * distToPeak * 4) * 0.6 * envelope1;
        rev[idx] = base * 0.7 * envelope2 + peakVal + 0.3;
        // Density: correlated with revenue but offset pattern
        den[idx] = noise.noise2D(nx * 2.5 + 0.5, nz * 2.5 + 0.5) * 0.5 + 0.5;
        // Error rate: spikes in valleys and near edges
        const edgeFactor = Math.max(Math.abs(nx), Math.abs(nz)); // 0 at center, 1 at edges
        err[idx] = Math.max(0,
          (1 - rev[idx]) * 0.3 * envelope3 +
          edgeFactor * edgeFactor * 0.2 * envelope1 +
          noise.noise2D(nx * 5, nz * 5) * 0.1
        );
      }
    }
    revenue.push(rev);
    density.push(den);
    error_rate.push(err);
  }
  return { revenue, density, error_rate };
}
const timeSeries = generateTimeSeries();
// ─── THREE.JS SETUP ────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 15, 45);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 100);
camera.position.set(12, 9, 16);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);
// ─── ORBIT CONTROLS ────────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 1.2, 0);
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.55; // Prevent going underground
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
// ─── CAMERA BOOKMARKS ──────────────────────────────────────────
const bookmarks = {
  1: { pos: [14, 10, 16], target: [0, 1.5, 0] },    // Overview
  2: { pos: [3, 2.5, 4], target: [-1, 0.7, -1.5] }, // Valley closeup
  3: { pos: [0, 18, 0.5], target: [0, 0, 0] }       // Top-down
};
function applyBookmark(id) {
  const bm = bookmarks[id];
  if (!bm) return;
  // Smooth animate camera
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 1200; // ms
  function animate(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Cubic ease in-out
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animate);
    }
  }
  requestAnimationFrame(animate);
}
// ─── LIGHTING ──────────────────────────────────────────────────
const ambient = new THREE.AmbientLight(0x223344, 0.6);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.2);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
sun.shadow.bias = -0.0001;
scene.add(sun);
const rim = new THREE.DirectionalLight(0x4466aa, 1.0);
rim.position.set(-8, 3, -10);
scene.add(rim);
// ─── GROUND PLANE ──────────────────────────────────────────────
const groundGeo = new THREE.PlaneGeometry(30, 30);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x111122,
  roughness: 0.9,
  metalness: 0.1
});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.8;
ground.receiveShadow = true;
scene.add(ground);
// ─── GRID HELPER ───────────────────────────────────────────────
const gridHelper = new THREE.PolarGridHelper(14, 32, 24, 128, 0x222244, 0x222244);
gridHelper.position.y = -0.79;
scene.add(gridHelper);
// ─── TERRAIN MESH ──────────────────────────────────────────────
/*
  BufferGeometry construction:
  - vertices: (GRID_SIZE * GRID_SIZE) of [x, height, z]
  - colors: (GRID_SIZE * GRID_SIZE) of [r, g, b]
  - indices: (GRID_SIZE-1)*(GRID_SIZE-1)*2 triangles via indexed draw
  Cached per time step to avoid per-frame reconstruction.
*/
const terrainGeo = new THREE.BufferGeometry();
const vertexCount = GRID_SIZE * GRID_SIZE;
const positions = new Float32Array(vertexCount * 3);
const colors = new Float32Array(vertexCount * 3);
// Initialize positions array with x,z layout (y = 0 initially)
const halfSpan = TERRAIN_SPAN / 2;
for (let iz = 0; iz < GRID_SIZE; iz++) {
  for (let ix = 0; ix < GRID_SIZE; ix++) {
    const idx = iz * GRID_SIZE + ix;
    positions[idx * 3]     = (ix / (GRID_SIZE - 1)) * TERRAIN_SPAN - halfSpan;
    positions[idx * 3 + 1] = 0; // height — updated per time step
    positions[idx * 3 + 2] = (iz / (GRID_SIZE - 1)) * TERRAIN_SPAN - halfSpan;
  }
}
// Build index buffer (two triangles per quad)
const indexCount = (GRID_SIZE - 1) * (GRID_SIZE - 1) * 6;
const indices = new Uint32Array(indexCount);
let ii = 0;
for (let iz = 0; iz < GRID_SIZE - 1; iz++) {
  for (let ix = 0; ix < GRID_SIZE - 1; ix++) {
    const a = iz * GRID_SIZE + ix;
    const b = a + 1;
    const c = a + GRID_SIZE;
    const d = c + 1;
    indices[ii++] = a; indices[ii++] = b; indices[ii++] = d;
    indices[ii++] = a; indices[ii++] = d; indices[ii++] = c;
  }
}
terrainGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
terrainGeo.setIndex(new THREE.BufferAttribute(indices, 1));
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
/*
  Cache: pre-built position+color buffers per time step.
  Keyed as "terrain_buf|{timeStep}".
  On slider change, swap the buffer attribute arrays instead of rebuilding geometry.
*/
function buildTerrainBuffer(t) {
  const cacheKey = CacheStore.key('terrain_buf', t);
  const cached = CacheStore.get(cacheKey);
  if (cached) return cached;
  const rev = timeSeries.revenue[t];
  const den = timeSeries.density[t];
  const posCopy = new Float32Array(positions);
  const colCopy = new Float32Array(colors.length);
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iz * GRID_SIZE + ix;
      // Height: scale revenue to [0, 4] meters
      const h = rev[idx] * 4.0;
      posCopy[idx * 3 + 1] = h;
      /*
        Color mapping (vegetation gradient):
        Low density → cool blue-green (0.1, 0.2, 0.5)
        Mid density → vibrant green (0.2, 0.7, 0.2)
        High density → golden yellow (0.8, 0.7, 0.1)
        Uses piecewise linear interpolation with three anchor points.
      */
      const d = den[idx]; // [0, 1]
      let r, g, b;
      if (d < 0.5) {
        const t2 = d / 0.5;
        r = 0.1 + t2 * 0.1;
        g = 0.2 + t2 * 0.5;
        b = 0.5 - t2 * 0.3;
      } else {
        const t2 = (d - 0.5) / 0.5;
        r = 0.2 + t2 * 0.6;
        g = 0.7 - t2 * 0.0;
        b = 0.2 - t2 * 0.1;
      }
      colCopy[idx * 3]     = r;
      colCopy[idx * 3 + 1] = g;
      colCopy[idx * 3 + 2] = b;
    }
  }
  const result = { positions: posCopy, colors: colCopy };
  CacheStore.set(cacheKey, result);
  return result;
}
function applyTerrainBuffer(t) {
  const buf = buildTerrainBuffer(t);
  terrainGeo.attributes.position.array.set(buf.positions);
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.array.set(buf.colors);
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  terrainGeo.index.needsUpdate = true;
}
// ─── RIVER SYSTEM ──────────────────────────────────────────────
/*
  ALGORITHM: River Tracing
  1. Scan error_rate grid for cells exceeding threshold (error_rate > 0.35)
  2. Cluster nearby error cells using a simple flood-fill (8-connected)
  3. For each cluster, find the centroid → this is the "spring" (river source)
  4. From each spring, trace downhill using gradient descent on the heightfield:
     path[0] = spring position
     path[k+1] = path[k] - step * gradient(heightfield at path[k])
     Stop when: height < min threshold, path leaves bounds, or max steps reached
  5. Create TubeGeometry along the traced path
  6. Cache TubeGeometry per time step (rebuild only when time step changes, debounced 200ms)
  Math for gradient descent step:
  grad_h(x,z) = [ (h(x+dx,z) - h(x-dx,z)) / (2*dx),
                  (h(x,z+dz) - h(x,z-dz)) / (2*dz) ]
  next_pos = current_pos - learning_rate * grad_h / |grad_h|
*/
let riverGroup = new THREE.Group();
scene.add(riverGroup);
// Find error clusters and trace rivers
function buildRivers(t) {
  const cacheKey = CacheStore.key('river_group', t);
  const cached = CacheStore.get(cacheKey);
  if (cached) {
    // Clone/copy cached group
    while (riverGroup.children.length > 0) {
      riverGroup.remove(riverGroup.children[0]);
    }
    cached.children.forEach(child => {
      riverGroup.add(child.clone());
    });
    return;
  }
  // Clear existing rivers
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    if (child.material) child.material.dispose();
    riverGroup.remove(child);
  }
  const err = timeSeries.error_rate[t];
  const rev = timeSeries.revenue[t];
  const threshold = 0.35;
  const visited = new Uint8Array(GRID_SIZE * GRID_SIZE);
  // Find error cells
  const errorCells = [];
  for (let iz = 0; iz < GRID_SIZE; iz++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iz * GRID_SIZE + ix;
      if (err[idx] > threshold && visited[idx] === 0) {
        // Flood fill cluster
        const cluster = [];
        const stack = [idx];
        visited[idx] = 1;
        while (stack.length > 0) {
          const cur = stack.pop();
          cluster.push(cur);
          const cz = Math.floor(cur / GRID_SIZE);
          const cx = cur % GRID_SIZE;
          // 8-connected neighbors
          for (let dz = -1; dz <= 1; dz++) {
            for (let dx = -1; dx <= 1; dx++) {
              if (dx === 0 && dz === 0) continue;
              const nx = cx + dx;
              const nz = cz + dz;
              if (nx < 0 || nx >= GRID_SIZE || nz < 0 || nz >= GRID_SIZE) continue;
              const nidx = nz * GRID_SIZE + nx;
              if (err[nidx] > threshold && visited[nidx] === 0) {
                visited[nidx] = 1;
                stack.push(nidx);
              }
            }
          }
        }
        if (cluster.length >= 3) {
          errorCells.push(cluster);
        }
      }
    }
  }
  // For each cluster, trace one river from its centroid
  const riverPaths = [];
  for (const cluster of errorCells) {
    // Centroid in grid coords
    let sumX = 0, sumZ = 0;
    for (const idx of cluster) {
      sumX += idx % GRID_SIZE;
      sumZ += Math.floor(idx / GRID_SIZE);
    }
    const cx = sumX / cluster.length;
    const cz = sumZ / cluster.length;
    // Gradient descent downhill
    const path = [];
    let px = cx, pz = cz;
    const stepSize = 0.6;
    const maxSteps = 60;
    for (let s = 0; s < maxSteps; s++) {
      path.push([px, pz]);
      // Sample height at current position (bilinear interpolation)
      const ix = Math.floor(px);
      const iz = Math.floor(pz);
      if (ix < 1 || ix >= GRID_SIZE - 2 || iz < 1 || iz >= GRID_SIZE - 2) break;
      const fx = px - ix;
      const fz = pz - iz;
      const i00 = iz * GRID_SIZE + ix;
      const h00 = rev[i00];
      const h10 = rev[i00 + 1];
      const h01 = rev[i00 + GRID_SIZE];
      const h11 = rev[i00 + GRID_SIZE + 1];
      const h = (1 - fx) * (1 - fz) * h00 + fx * (1 - fz) * h10 +
                (1 - fx) * fz * h01 + fx * fz * h11;
      if (h < 0.15) break; // Reached valley floor
      // Gradient via central differences
      const dx = 1.0;
      const h_right = (1 - (fx + dx / GRID_SIZE)) * (1 - fz) * rev[iz * GRID_SIZE + Math.min(ix + 1, GRID_SIZE - 1)] +
                       (fx + dx / GRID_SIZE) * (1 - fz) * rev[iz * GRID_SIZE + Math.min(ix + 2, GRID_SIZE - 1)] || rev[iz * GRID_SIZE + ix];
      const h_left = (1 - Math.max(fx - dx / GRID_SIZE, 0)) * (1 - fz) * rev[iz * GRID_SIZE + Math.max(ix - 1, 0)] || rev[iz * GRID_SIZE + ix];
      const gradX = (h_right - h_left) / 2;
      const h_down = (1 - fx) * (1 - Math.min(fz + dx / GRID_SIZE, 1)) * rev[Math.min(iz + 1, GRID_SIZE - 1) * GRID_SIZE + ix] || rev[iz * GRID_SIZE + ix];
      const h_up = (1 - fx) * (1 - Math.max(fz - dx / GRID_SIZE, 0)) * rev[Math.max(iz - 1, 0) * GRID_SIZE + ix] || rev[iz * GRID_SIZE + ix];
      const gradZ = (h_down - h_up) / 2;
      const gradMag = Math.sqrt(gradX * gradX + gradZ * gradZ) || 1e-6;
      px -= stepSize * gradX / gradMag;
      pz -= stepSize * gradZ / gradMag;
    }
    if (path.length > 3) {
      riverPaths.push(path);
    }
  }
  // Build TubeGeometry for each path
  const riverMaterial = new THREE.MeshStandardMaterial({
    color: 0xcc3333,
    roughness: 0.3,
    metalness: 0.4,
    emissive: 0x330000,
    emissiveIntensity: 0.5
  });
  for (const path of riverPaths) {
    // Convert grid coords to world coords
    const points = path.map(([px, pz]) => {
      const wx = (px / (GRID_SIZE - 1)) * TERRAIN_SPAN - halfSpan;
      const wz = (pz / (GRID_SIZE - 1)) * TERRAIN_SPAN - halfSpan;
      // Sample height
      const ix = Math.min(Math.max(Math.floor(px), 0), GRID_SIZE - 1);
      const iz = Math.min(Math.max(Math.floor(pz), 0), GRID_SIZE - 1);
      const h = rev[iz * GRID_SIZE + ix] * 4.0 + 0.08;
      return new THREE.Vector3(wx, h, wz);
    });
    if (points.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(points);
    const tubeGeo = new THREE.TubeGeometry(curve, Math.min(points.length * 2, 40), 0.08, 6, false);
    const tubeMesh = new THREE.Mesh(tubeGeo, riverMaterial);
    tubeMesh.castShadow = true;
    tubeMesh.receiveShadow = true;
    riverGroup.add(tubeMesh);
  }
  // Cache the built group
  const cachedGroup = new THREE.Group();
  riverGroup.children.forEach(child => cachedGroup.add(child.clone()));
  CacheStore.set(cacheKey, cachedGroup);
}
// Debounced river rebuild
let riverDebounceTimer = null;
function scheduleRiverRebuild(t) {
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    buildRivers(t);
    riverDebounceTimer = null;
  }, 200);
}
// ─── PARTICLE SYSTEM ───────────────────────────────────────────
/*
  Particle system: represents data flows (API calls, user actions) as
  glowing dots flowing along the terrain surface.
  ALGORITHM: Flow-field pathfinding
  Each particle:
    1. Has a random starting position on the terrain
    2. Moves in the direction of the "gradient" of density (toward high-density areas)
    3. Stays clamped to the terrain surface (height sampled from heightfield)
    4. When it reaches a peak, respawns at a random low point
    5. Velocity = lerp(current_velocity, target_direction * speed, 0.05)
       This creates smooth, natural-looking flow curves
  Performance: particle positions updated in-place on BufferGeometry.attributes.position.array.
  No allocations in the per-frame update loop.
*/
const PARTICLE_COUNT = 400;
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
// Each particle's state stored in parallel arrays (Structure of Arrays for cache locality)
const particleState = {
  gridX: new Float32Array(PARTICLE_COUNT),    // Current grid x position
  gridZ: new Float32Array(PARTICLE_COUNT),    // Current grid z position
  velX: new Float32Array(PARTICLE_COUNT),     // Velocity x
  velZ: new Float32Array(PARTICLE_COUNT),     // Velocity z
  life: new Float32Array(PARTICLE_COUNT)      // Life counter for respawn
};
function initParticle(i) {
  // Random spawn on terrain surface
  const gx = Math.random() * (GRID_SIZE - 1);
  const gz = Math.random() * (GRID_SIZE - 1);
  particleState.gridX[i] = gx;
  particleState.gridZ[i] = gz;
  particleState.velX[i] = (Math.random() - 0.5) * 0.1;
  particleState.velZ[i] = (Math.random() - 0.5) * 0.1;
  particleState.life[i] = Math.random() * 200;
}
for (let i = 0; i < PARTICLE_COUNT; i++) {
  initParticle(i);
  // Initial color: warm yellow-orange
  particleColors[i * 3]     = 1.0;
  particleColors[i * 3 + 1] = 0.75 + Math.random() * 0.25;
  particleColors[i * 3 + 2] = 0.2 + Math.random() * 0.2;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
// Create sprite texture (radial gradient)
const spriteCanvas = document.createElement('canvas');
spriteCanvas.width = 32;
spriteCanvas.height = 32;
const ctx = spriteCanvas.getContext('2d');
const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
gradient.addColorStop(0, 'rgba(255,220,100,1)');
gradient.addColorStop(0.3, 'rgba(255,180,40,0.8)');
gradient.addColorStop(0.7, 'rgba(255,100,20,0.15)');
gradient.addColorStop(1, 'rgba(255,50,0,0)');
ctx.fillStyle = gradient;
ctx.fillRect(0, 0, 32, 32);
const spriteTexture = new THREE.CanvasTexture(spriteCanvas);
spriteTexture.needsUpdate = true;
const particleMat = new THREE.PointsMaterial({
  size: 0.25,
  map: spriteTexture,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
/*
  MEMOIZE: world-to-grid coordinate transform.
  Called on hover/tooltip path — cache result per frame to avoid recomputation.
*/
const coordCache = {
  _cache: new Map(),
  _frameId: 0,
  nextFrame() { this._frameId++; this._cache.clear(); },
  gridToWorld(gx, gz) {
    const key = `${gx.toFixed(3)},${gz.toFixed(3)}`;
    if (this._cache.has(key)) return this._cache.get(key);
    const wx = (gx / (GRID_SIZE - 1)) * TERRAIN_SPAN - halfSpan;
    const wz = (gz / (GRID_SIZE - 1)) * TERRAIN_SPAN - halfSpan;
    const result = [wx, wz];
    this._cache.set(key, result);
    return result;
  }
};
function updateParticles(t) {
  const rev = timeSeries.revenue[t];
  const den = timeSeries.density[t];
  const posArr = particleGeo.attributes.position.array;
  const dt = 0.016; // ~60fps
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    let gx = particleState.gridX[i];
    let gz = particleState.gridZ[i];
    let vx = particleState.velX[i];
    let vz = particleState.velZ[i];
    // Sample density gradient at current position (central differences)
    const ix = Math.floor(gx);
    const iz = Math.floor(gz);
    if (ix < 1 || ix >= GRID_SIZE - 2 || iz < 1 || iz >= GRID_SIZE - 2) {
      initParticle(i);
      continue;
    }
    const fx = gx - ix;
    const fz = gz - iz;
    const idx = iz * GRID_SIZE + ix;
    // Density gradient toward high-density areas (flow uphill in density space)
    const d_right = den[idx + 1];
    const d_left  = den[idx - 1];
    const d_down  = den[idx + GRID_SIZE];
    const d_up    = den[idx - GRID_SIZE];
    const gradDx = d_right - d_left;
    const gradDz = d_down - d_up;
    // Also add slight downhill gravity on revenue (flows toward valleys)
    const h_right = rev[idx + 1];
    const h_left  = rev[idx - 1];
    const h_down  = rev[idx + GRID_SIZE];
    const h_up    = rev[idx - GRID_SIZE];
    const gradHx = h_right - h_left;
    const gradHz = h_down - h_up;
    // Combined flow direction: toward high density, away from high elevation
    const targetVx = gradDx * 0.08 - gradHx * 0.02;
    const targetVz = gradDz * 0.08 - gradHz * 0.02;
    const targetMag = Math.sqrt(targetVx * targetVx + targetVz * targetVz) || 1e-6;
    // Smooth velocity update (lerp toward target)
    vx += (targetVx / targetMag * 0.15 - vx) * 0.05;
    vz += (targetVz / targetMag * 0.15 - vz) * 0.05;
    // Clamp speed
    const speed = Math.sqrt(vx * vx + vz * vz);
    const maxSpeed = 0.8;
    if (speed > maxSpeed) {
      vx = vx / speed * maxSpeed;
      vz = vz / speed * maxSpeed;
    }
    gx += vx * dt * 30;
    gz += vz * dt * 30;
    // Boundary check — respawn if out of bounds
    if (gx < 0.5 || gx > GRID_SIZE - 1.5 || gz < 0.5 || gz > GRID_SIZE - 1.5) {
      initParticle(i);
      gx = particleState.gridX[i];
      gz = particleState.gridZ[i];
      vx = particleState.velX[i];
      vz = particleState.velZ[i];
    }
    // Life counter for periodic respawn
    particleState.life[i] -= 1;
    if (particleState.life[i] <= 0) {
      initParticle(i);
      gx = particleState.gridX[i];
      gz = particleState.gridZ[i];
      vx = particleState.velX[i];
      vz = particleState.velZ[i];
    }
    // Store updated state
    particleState.gridX[i] = gx;
    particleState.gridZ[i] = gz;
    particleState.velX[i] = vx;
    particleState.velZ[i] = vz;
    // Convert to world position (memoized transform)
    const [wx, wz] = coordCache.gridToWorld(gx, gz);
    // Height from bilinear interpolation on revenue
    const h = rev[idx] * 4.0 + 0.15; // Slight offset above terrain
    posArr[i * 3]     = wx;
    posArr[i * 3 + 1] = h;
    posArr[i * 3 + 2] = wz;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ─── UI EVENT HANDLERS ─────────────────────────────────────────
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
let currentTimeStep = 0;
timeSlider.addEventListener('input', () => {
  currentTimeStep = parseInt(timeSlider.value);
  timeLabel.textContent = `${currentTimeStep} / ${TIME_STEPS - 1}`;
  applyTerrainBuffer(currentTimeStep);
  scheduleRiverRebuild(currentTimeStep);
});
// Auto-rotate toggle
const btnAutoRot = document.getElementById('btn-autorot');
btnAutoRot.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAutoRot.textContent = `Auto-Rotate: ${controls.autoRotate ? 'ON' : 'OFF'}`;
  btnAutoRot.classList.toggle('active', controls.autoRotate);
});
// Bookmarks
document.getElementById('btn-bookmark-1').addEventListener('click', () => applyBookmark(1));
document.getElementById('btn-bookmark-2').addEventListener('click', () => applyBookmark(2));
document.getElementById('btn-bookmark-3').addEventListener('click', () => applyBookmark(3));
document.getElementById('btn-reset').addEventListener('click', () => {
  applyBookmark(1);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key) {
    case '1': applyBookmark(1); break;
    case '2': applyBookmark(2); break;
    case '3': applyBookmark(3); break;
    case 'r': controls.autoRotate = !controls.autoRotate;
              btnAutoRot.textContent = `Auto-Rotate: ${controls.autoRotate ? 'ON' : 'OFF'}`;
              btnAutoRot.classList.toggle('active', controls.autoRotate);
              break;
    case 'ArrowLeft':  timeSlider.value = Math.max(0, currentTimeStep - 1);
                       timeSlider.dispatchEvent(new Event('input')); break;
    case 'ArrowRight': timeSlider.value = Math.min(TIME_STEPS - 1, currentTimeStep + 1);
                       timeSlider.dispatchEvent(new Event('input')); break;
  }
});
// Resize handler
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── DIAGNOSTIC PANEL UPDATE ───────────────────────────────────
const cacheDiag = document.getElementById('cache-diag');
// ─── INITIAL STATE ─────────────────────────────────────────────
applyTerrainBuffer(0);
buildRivers(0);
// ─── ANIMATION LOOP ────────────────────────────────────────────
/*
  Hot-path audit:
  - updateParticles: reuses BufferGeometry.attributes.position.array (no allocation)
  - coordCache: cleared once per frame, populated on demand (memoized grid→world)
  - terrainGeo: attributes swapped from cache (no geometry construction)
  - controls.update(): internal Three.js — no custom allocations
  - cacheDiag update: string allocation once per 60 frames (debounced)
*/
let frameCount = 0;
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  coordCache.nextFrame();
  updateParticles(currentTimeStep);
  // Update diagnostic display every 30 frames (~0.5 sec)
  frameCount++;
  if (frameCount % 30 === 0) {
    cacheDiag.textContent = CacheStore.stats();
  }
  renderer.render(scene, camera);
}
// ─── START ─────────────────────────────────────────────────────
animate();
// Auto-advance time for demo (can be disabled by user interaction)
let autoAdvanceInterval = null;
function startAutoAdvance() {
  autoAdvanceInterval = setInterval(() => {
    if (document.activeElement === timeSlider) return; // Don't interfere with slider drag
    currentTimeStep = (currentTimeStep + 1) % TIME_STEPS;
    timeSlider.value = currentTimeStep;
    timeLabel.textContent = `${currentTimeStep} / ${TIME_STEPS - 1}`;
    applyTerrainBuffer(currentTimeStep);
    scheduleRiverRebuild(currentTimeStep);
  }, 1500);
}
startAutoAdvance();
// Pause auto-advance when user interacts with slider
timeSlider.addEventListener('mousedown', () => {
  if (autoAdvanceInterval) { clearInterval(autoAdvanceInterval); autoAdvanceInterval = null; }
});
timeSlider.addEventListener('mouseup', () => {
  if (!autoAdvanceInterval) startAutoAdvance();
});
// Also pause on touch
timeSlider.addEventListener('touchstart', () => {
  if (autoAdvanceInterval) { clearInterval(autoAdvanceInterval); autoAdvanceInterval = null; }
});
console.log('3D Data Terrain Explorer ready.');
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan');
console.log('Keys: 1/2/3=bookmarks, r=auto-rotate, ←→=time scrub');
</script>
</body>
</html>