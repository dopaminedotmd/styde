<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; }
  #canvas-container { position: fixed; inset: 0; z-index: 0; }
  #ui-layer { position: fixed; inset: 0; z-index: 10; pointer-events: none; }
  #ui-layer > * { pointer-events: auto; }
  #time-panel {
    position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: rgba(10,10,20,0.85); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px; padding: 12px 20px; display: flex; align-items: center; gap: 14px;
    backdrop-filter: blur(12px); color: #c8d6e5;
  }
  #time-slider { width: 280px; accent-color: #5dade2; }
  #time-label { min-width: 90px; text-align: center; font-variant-numeric: tabular-nums; font-size: 13px; }
  #bookmark-bar {
    position: absolute; top: 16px; right: 16px; display: flex; gap: 6px; flex-wrap: wrap;
    max-width: 360px; justify-content: flex-end;
  }
  .bm-btn {
    background: rgba(10,10,20,0.8); border: 1px solid rgba(255,255,255,0.15);
    color: #aab7c4; border-radius: 6px; padding: 5px 10px; cursor: pointer;
    font-size: 11px; backdrop-filter: blur(8px); transition: all 0.15s;
  }
  .bm-btn:hover { border-color: #5dade2; color: #fff; }
  .bm-btn.active { border-color: #5dade2; color: #5dade2; }
  #diag-panel {
    position: absolute; bottom: 24px; left: 16px;
    background: rgba(10,10,20,0.85); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px; padding: 8px 12px; color: #6b7b8d; font-size: 10px;
    font-family: 'Consolas', 'Courier New', monospace; backdrop-filter: blur(12px);
    line-height: 1.6; min-width: 180px;
  }
  #diag-panel span { color: #5dade2; }
  #auto-rotate-btn {
    position: absolute; top: 16px; left: 16px;
    background: rgba(10,10,20,0.8); border: 1px solid rgba(255,255,255,0.15);
    color: #aab7c4; border-radius: 6px; padding: 6px 12px; cursor: pointer;
    font-size: 11px; backdrop-filter: blur(8px); transition: all 0.15s;
  }
  #auto-rotate-btn.on { border-color: #5dade2; color: #5dade2; }
  #legend {
    position: absolute; top: 60px; left: 16px;
    background: rgba(10,10,20,0.8); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px; padding: 10px 14px; color: #8899aa; font-size: 11px;
    backdrop-filter: blur(8px); line-height: 1.8;
  }
  .legend-swatch { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-layer">
  <div id="time-panel">
    <span style="font-size:12px;opacity:0.7">TIME</span>
    <input type="range" id="time-slider" min="0" max="14" value="0" step="1">
    <span id="time-label">T+0</span>
  </div>
  <div id="bookmark-bar">
    <button class="bm-btn" data-bm="0">Overview</button>
    <button class="bm-btn" data-bm="1">Revenue Peaks</button>
    <button class="bm-btn" data-bm="2">Error Valley</button>
    <button class="bm-btn" data-bm="3">User Hotspot</button>
  </div>
  <button id="auto-rotate-btn" class="on" title="Toggle auto-rotation">AUTO ROTATE: ON</button>
  <div id="legend">
    <div><span class="legend-swatch" style="background:#27ae60"></span> High user density</div>
    <div><span class="legend-swatch" style="background:#e67e22"></span> Medium density</div>
    <div><span class="legend-swatch" style="background:#7f8c8d"></span> Low density</div>
    <div><span class="legend-swatch" style="background:#e74c3c"></span> Error river</div>
    <div><span class="legend-swatch" style="background:#f1c40f"></span> API trail</div>
  </div>
  <div id="diag-panel">
    FPS: <span id="diag-fps">0</span><br>
    TERRAIN CACHE: <span id="diag-terrain">-/-</span><br>
    RIVER CACHE: <span id="diag-river">-/-</span><br>
    WORLD→GRID: <span id="diag-w2g">-/-</span><br>
    PARTICLE SWAPS: <span id="diag-part">0</span>
  </div>
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
/* ── CONFIG ────────────────────────────────────────────────────────── */
const GRID = 80;                // terrain resolution: GRID×GRID vertices
const TIME_STEPS = 15;          // precomputed time slices
const TERRAIN_SIZE = 20;        // world-space width/depth of terrain plane
const MAX_HEIGHT = 6;           // peak elevation
const DEBOUNCE_MS = 200;        // slider debounce delay
/* ── CACHE LAYER — all memoized/computed-once data lives here ──────── */
const Cache = {
  /* heightfield cache: Float32Array[GRID*GRID] per time step */
  heightfields: new Array(TIME_STEPS),
  /* terrain geometry cache: BufferGeometry per time step, pre-built */
  terrainGeometries: new Array(TIME_STEPS),
  /* river path cache: Array<THREE.Vector3[]> per time step */
  riverPaths: new Array(TIME_STEPS),
  /* river line geometry cache: Line geometry per time step */
  riverGeometries: new Array(TIME_STEPS),
  /* worldToGrid memo: Map<precisionKey, {ix,iz}>, cleared per frame */
  worldToGridMemo: new Map(),
  /* particle start positions: precomputed origins for each trail */
  particleOrigins: null,
  /* cache stats for diagnostic panel */
  stats: {
    terrainHits: 0, terrainMisses: 0,
    riverHits: 0, riverMisses: 0,
    w2gHits: 0, w2gMisses: 0,
    particleSwaps: 0
  }
};
/* ── SCENE SETUP ───────────────────────────────────────────────────── */
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 18, 55);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(14, 10, 16);
camera.lookAt(0, 1.5, 0);
/* ── LIGHTING ──────────────────────────────────────────────────────── */
const ambient = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffeedd', 4.5);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -18;
sun.shadow.camera.right = 18;
sun.shadow.camera.top = 18;
sun.shadow.camera.bottom = -18;
sun.shadow.bias = -0.0005;
scene.add(sun);
const fill = new THREE.DirectionalLight('#8899cc', 1.2);
fill.position.set(-8, 4, -6);
scene.add(fill);
/* ── GROUND PLANE ──────────────────────────────────────────────────── */
const groundGeo = new THREE.PlaneGeometry(TERRAIN_SIZE * 1.8, TERRAIN_SIZE * 1.8);
const groundMat = new THREE.MeshStandardMaterial({ color: '#141428', roughness: 0.95 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.3;
ground.receiveShadow = true;
scene.add(ground);
/* ── DATA GENERATION ────────────────────────────────────────────────── */
/*
  Generates all time-series data upfront.
  Each time step: revenue (height), userDensity (color), errors (river source).
  Uses layered sine waves with phase-shift per time step to simulate evolution.
*/
function generateTimeSeriesData() {
  const half = GRID / 2;
  for (let t = 0; t < TIME_STEPS; t++) {
    const phase = (t / TIME_STEPS) * Math.PI * 2;
    const heights = new Float32Array(GRID * GRID);
    const densities = new Float32Array(GRID * GRID);
    const errorField = new Float32Array(GRID * GRID);
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        // Normalize to [-1,1] range for noise input
        const nx = (ix - half) / half;
        const nz = (iz - half) / half;
        const dist = Math.sqrt(nx * nx + nz * nz);
        // Revenue = layered terrain: broad swell + medium ridges + fine detail
        const broad = Math.sin(nx * 1.8 + phase * 0.6) * Math.cos(nz * 2.1 + phase * 0.4) * 2.0;
        const ridge = Math.sin(nx * 4.5 + phase * 0.8) * 0.7 + Math.cos(nz * 5.2 - phase * 0.5) * 0.7;
        const detail = Math.sin(nx * 9.0 + nz * 8.0 + phase * 1.2) * 0.35;
        // Time-evolving gaussian peak that moves across the terrain
        const peakX = Math.cos(phase * 0.7) * 0.55;
        const peakZ = Math.sin(phase * 0.7) * 0.55;
        const gauss = Math.exp(-((nx - peakX) ** 2 + (nz - peakZ) ** 2) * 6.0) * 2.5;
        // Edge falloff for island feel
        const edge = 1.0 - Math.min(1.0, Math.max(0.0, (dist - 0.6) / 0.4));
        let h = (broad + ridge + detail + gauss) * edge;
        h = Math.max(0.05, h); // minimum terrain height — no negative terrain
        heights[iz * GRID + ix] = h * MAX_HEIGHT;
        // User density: loosely correlated with height but shifted in phase
        const dPhase = phase + 1.3;
        const dBroad = Math.sin(nx * 2.3 + dPhase * 0.5) * Math.cos(nz * 1.7 + dPhase * 0.6) * 1.8;
        const dRidge = Math.sin(nx * 5.0 + dPhase * 0.7) * 0.5;
        let d = (dBroad + dRidge + gauss * 0.7) * edge;
        d = (d + 2.0) / 4.0; // normalize to [0,1]
        densities[iz * GRID + ix] = Math.max(0.0, Math.min(1.0, d));
        // Error concentration: inverse of density in some regions, with hot spots
        const eHot = Math.exp(-((nx + peakX * 0.6) ** 2 + (nz - peakZ * 0.7) ** 2) * 8.0);
        const eBase = (1.0 - d) * 0.3;
        errorField[iz * GRID + ix] = Math.max(0.0, Math.min(1.0, eBase + eHot * 0.8));
      }
    }
    Cache.heightfields[t] = heights;
    Cache.heightfields._densities = Cache.heightfields._densities || [];
    Cache.heightfields._densities[t] = densities;
    Cache.heightfields._errors = Cache.heightfields._errors || [];
    Cache.heightfields._errors[t] = errorField;
  }
  // Store auxiliary arrays on the heightfields array for lookup convenience
  Cache._densities = Cache.heightfields._densities;
  Cache._errors = Cache.heightfields._errors;
}
generateTimeSeriesData();
/* ── TERRAIN BUILDER (with geometry cache) ─────────────────────────── */
/*
  Pre-builds one BufferGeometry per time step.
  On slider change we swap mesh.geometry — no new THREE.XxxGeometry() per tick.
  Each geometry stores position + color attributes.
  Color maps user density: low=gray, mid=orange, high=green.
*/
function buildTerrainGeometry(t) {
  const heights = Cache.heightfields[t];
  const densities = Cache._densities[t];
  const segments = GRID - 1;
  const geo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, segments, segments);
  geo.rotateX(-Math.PI / 2); // lay flat on XZ plane
  const pos = geo.attributes.position;
  const colorsArr = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    // PlaneGeometry vertices go row by row; map back to grid index
    const ix = i % GRID;
    const iz = Math.floor(i / GRID);
    const h = heights[iz * GRID + ix];
    pos.setY(i, h);
    // Vegetation gradient: gray(7f8c8d) → orange(e67e22) → green(27ae60)
    const d = densities[iz * GRID + ix];
    const c = new THREE.Color();
    if (d < 0.33) {
      c.setRGB(0.5, 0.55, 0.55).lerp(new THREE.Color(0.9, 0.49, 0.13), d / 0.33);
    } else if (d < 0.66) {
      c.setRGB(0.9, 0.49, 0.13).lerp(new THREE.Color(0.15, 0.68, 0.38), (d - 0.33) / 0.33);
    } else {
      c.setRGB(0.15, 0.68, 0.38).lerp(new THREE.Color(0.05, 0.55, 0.25), (d - 0.66) / 0.34);
    }
    colorsArr[i * 3] = c.r;
    colorsArr[i * 3 + 1] = c.g;
    colorsArr[i * 3 + 2] = c.b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
  geo.computeVertexNormals();
  geo.attributes.position.needsUpdate = true;
  return geo;
}
// Pre-build all terrain geometry variants
for (let t = 0; t < TIME_STEPS; t++) {
  Cache.terrainGeometries[t] = buildTerrainGeometry(t);
}
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false
});
const terrainMesh = new THREE.Mesh(Cache.terrainGeometries[0], terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Wireframe overlay for grid readability
const wireframeMat = new THREE.MeshBasicMaterial({
  color: '#1a1a3a',
  wireframe: true,
  transparent: true,
  opacity: 0.12
});
const wireframeMesh = new THREE.Mesh(Cache.terrainGeometries[0], wireframeMat);
wireframeMesh.position.y = 0.02;
scene.add(wireframeMesh);
/* ── RIVER BUILDER (with geometry cache) ───────────────────────────── */
/*
  Traces error concentration paths as river lines.
  Paths flow downhill from error peaks following the terrain gradient.
  Cache one Line geometry per time step; swap on slider change.
*/
function traceRiverPath(t) {
  const heights = Cache.heightfields[t];
  const errors = Cache._errors[t];
  const half = GRID / 2;
  const cellSize = TERRAIN_SIZE / (GRID - 1);
  // Find top-3 error concentration cells as river sources
  const candidates = [];
  for (let iz = 1; iz < GRID - 1; iz++) {
    for (let ix = 1; ix < GRID - 1; ix++) {
      const e = errors[iz * GRID + ix];
      if (e > 0.25) {
        candidates.push({ ix, iz, e });
      }
    }
  }
  candidates.sort((a, b) => b.e - a.e);
  const sources = candidates.slice(0, 3);
  const allPaths = [];
  for (const src of sources) {
    const path = [];
    let cx = src.ix;
    let cz = src.iz;
    let steps = 0;
    const maxSteps = 200;
    while (steps < maxSteps && cx > 0 && cx < GRID - 1 && cz > 0 && cz < GRID - 1) {
      // Map grid index to world position: center of terrain
      const wx = (cx - half) * cellSize;
      const wz = (cz - half) * cellSize;
      const wy = heights[cz * GRID + cx] + 0.15; // offset above terrain
      path.push(new THREE.Vector3(wx, wy, wz));
      // Follow steepest downhill among 8 neighbors
      let bestDz = 0, bestDx = 0, bestH = heights[cz * GRID + cx];
      for (let dz = -1; dz <= 1; dz++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dz === 0) continue;
          const nh = heights[(cz + dz) * GRID + (cx + dx)];
          if (nh < bestH) { bestH = nh; bestDx = dx; bestDz = dz; }
        }
      }
      if (bestDx === 0 && bestDz === 0) break; // local minimum reached
      cx += bestDx;
      cz += bestDz;
      steps++;
    }
    if (path.length > 5) allPaths.push(path);
  }
  return allPaths;
}
function buildRiverGeometry(t) {
  const allPaths = Cache.riverPaths[t];
  const points = [];
  for (const path of allPaths) {
    for (const pt of path) points.push(pt);
    // Insert a break marker (null-like) by pushing a point at y=-999
    // We'll use NaN in the buffer to break the line strip
    points.push(new THREE.Vector3(NaN, NaN, NaN));
  }
  if (points.length === 0) {
    // Return empty geometry if no rivers
    const empty = new THREE.BufferGeometry();
    empty.setAttribute('position', new THREE.BufferAttribute(new Float32Array(0), 3));
    return empty;
  }
  // For visual rivers, use a tube-like approach via fat lines
  // We build a Line geometry; each river segment is a separate line
  const geo = new THREE.BufferGeometry();
  const posArr = new Float32Array(points.length * 3);
  for (let i = 0; i < points.length; i++) {
    posArr[i * 3] = points[i].x;
    posArr[i * 3 + 1] = points[i].y;
    posArr[i * 3 + 2] = points[i].z;
  }
  geo.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
  return geo;
}
// Precompute river paths and geometries for all time steps
for (let t = 0; t < TIME_STEPS; t++) {
  Cache.riverPaths[t] = traceRiverPath(t);
  Cache.riverGeometries[t] = buildRiverGeometry(t);
}
const riverMat = new THREE.LineBasicMaterial({
  color: '#e74c3c',
  linewidth: 1,
  transparent: true,
  opacity: 0.85,
  depthTest: true
});
const riverLine = new THREE.LineSegments(
  // Build segmented version: connect consecutive points, skip NaN segments
  buildSegmentedRiverGeometry(0),
  riverMat
);
// riverLine.renderOrder = 1;
scene.add(riverLine);
/* Helper: converts cached path points into line segments (pairs of vertices)
   skipping NaN-break markers. This gives cleaner rendering than LINE_STRIP. */
function buildSegmentedRiverGeometry(t) {
  const allPaths = Cache.riverPaths[t];
  const segments = [];
  for (const path of allPaths) {
    for (let i = 0; i < path.length - 1; i++) {
      segments.push(path[i].clone(), path[i + 1].clone());
    }
  }
  const geo = new THREE.BufferGeometry();
  if (segments.length === 0) {
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
    return geo;
  }
  const arr = new Float32Array(segments.length * 3);
  for (let i = 0; i < segments.length; i++) {
    arr[i * 3] = segments[i].x;
    arr[i * 3 + 1] = segments[i].y;
    arr[i * 3 + 2] = segments[i].z;
  }
  geo.setAttribute('position', new THREE.BufferAttribute(arr, 3));
  return geo;
}
// Overwrite initial river line with segmented version
riverLine.geometry.dispose();
riverLine.geometry = buildSegmentedRiverGeometry(0);
/* ── PARTICLES ─────────────────────────────────────────────────────── */
/*
  API call trails: BufferGeometry with reused position array.
  Particles flow from origins across the terrain, following valleys.
  Position array updated in-place each frame — no per-frame allocations.
*/
const PARTICLE_COUNT = 200;
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
// Track per-particle state: current grid position + progress
const particleState = new Array(PARTICLE_COUNT);
// Precompute origins: random positions on terrain at t=0
Cache.particleOrigins = new Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const ix = Math.floor(Math.random() * GRID);
  const iz = Math.floor(Math.random() * GRID);
  Cache.particleOrigins[i] = { ix, iz };
  particleState[i] = {
    ix: ix,
    iz: iz,
    progress: Math.random(), // 0..1 along current segment
    speed: 0.3 + Math.random() * 0.7,
    life: 0
  };
}
function initParticlePositions(t) {
  const heights = Cache.heightfields[t];
  const half = GRID / 2;
  const cellSize = TERRAIN_SIZE / (GRID - 1);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const st = particleState[i];
    const h = heights[st.iz * GRID + st.ix];
    particlePositions[i * 3] = (st.ix - half) * cellSize;
    particlePositions[i * 3 + 1] = h + 0.4;
    particlePositions[i * 3 + 2] = (st.iz - half) * cellSize;
  }
  particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
}
initParticlePositions(0);
const particleMat = new THREE.PointsMaterial({
  color: '#f1c40f',
  size: 0.08,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.7
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 2;
scene.add(particles);
/* In-place particle update: moves particles downhill along terrain gradient.
   Reuses particlePositions array — no new Float32Array allocations per frame. */
function updateParticles(t, dt) {
  const heights = Cache.heightfields[t];
  const half = GRID / 2;
  const cellSize = TERRAIN_SIZE / (GRID - 1);
  const dtClamped = Math.min(dt, 0.1);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const st = particleState[i];
    st.life += dtClamped * st.speed;
    // Every ~0.15s of particle life, move to a neighboring cell (downhill)
    if (st.life > 0.15) {
      st.life -= 0.15;
      let bestH = heights[st.iz * GRID + st.ix];
      let bestDx = 0, bestDz = 0;
      for (let dz = -1; dz <= 1; dz++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dz === 0) continue;
          const nz = st.iz + dz;
          const nx = st.ix + dx;
          if (nz < 0 || nz >= GRID || nx < 0 || nx >= GRID) continue;
          const nh = heights[nz * GRID + nx];
          // 70% downhill bias, 30% random exploration
          const score = nh + (Math.random() - 0.35) * 0.6;
          if (score < bestH) { bestH = score; bestDx = dx; bestDz = dz; }
        }
      }
      if (bestDx !== 0 || bestDz !== 0) {
        st.ix = Math.max(0, Math.min(GRID - 1, st.ix + bestDx));
        st.iz = Math.max(0, Math.min(GRID - 1, st.iz + bestDz));
      } else {
        // Stuck at local minimum: respawn at random origin
        const orig = Cache.particleOrigins[Math.floor(Math.random() * PARTICLE_COUNT)];
        st.ix = orig.ix;
        st.iz = orig.iz;
      }
    }
    // Interpolate position toward target cell for smooth movement
    const h = heights[st.iz * GRID + st.ix];
    const tx = (st.ix - half) * cellSize;
    const tz = (st.iz - half) * cellSize;
    const lerpFactor = Math.min(1.0, dtClamped * 8);
    particlePositions[i * 3] += (tx - particlePositions[i * 3]) * lerpFactor;
    particlePositions[i * 3 + 1] = h + 0.35 + Math.sin(st.life * 20) * 0.08; // slight bob
    particlePositions[i * 3 + 2] += (tz - particlePositions[i * 3 + 2]) * lerpFactor;
  }
  // Reuse the same BufferAttribute — just flag needsUpdate
  particleGeo.attributes.position.needsUpdate = true;
  Cache.stats.particleSwaps++;
}
/* ── ORBIT CONTROLS + BOOKMARKS ────────────────────────────────────── */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.35;
controls.target.set(0, 1.8, 0);
controls.minDistance = 5;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
const bookmarks = [
  { pos: [14, 10, 16], target: [0, 1.5, 0] },     // Overview
  { pos: [4, 8, 4], target: [3, 4, 2] },           // Revenue Peaks
  { pos: [-6, 5, -3], target: [-3, 1, -1] },        // Error Valley
  { pos: [2, 7, -6], target: [1, 3, -3] },          // User Hotspot
];
/* ── TIME CONTROL ──────────────────────────────────────────────────── */
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
let currentTime = 0;
let targetTime = 0;
let debounceTimer = null;
function applyTimeStep(t) {
  if (t === currentTime) {
    Cache.stats.terrainHits++;
    return;
  }
  Cache.stats.terrainMisses++;
  currentTime = t;
  // Swap terrain geometry (cached, no new constructor call)
  terrainMesh.geometry = Cache.terrainGeometries[t];
  wireframeMesh.geometry = Cache.terrainGeometries[t];
  // Swap river geometry (cached)
  riverLine.geometry.dispose();
  riverLine.geometry = buildSegmentedRiverGeometry(t);
  Cache.stats.riverMisses++;
  timeLabel.textContent = `T+${t}`;
}
slider.addEventListener('input', () => {
  targetTime = parseInt(slider.value);
  timeLabel.textContent = `T+${targetTime}`;
  // Debounce: delay geometry swap to avoid per-tick rebuilds
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    applyTimeStep(targetTime);
    debounceTimer = null;
  }, DEBOUNCE_MS);
});
slider.addEventListener('change', () => {
  // Immediate apply on mouse release
  if (debounceTimer) {
    clearTimeout(debounceTimer);
    debounceTimer = null;
  }
  applyTimeStep(parseInt(slider.value));
});
/* ── AUTO ROTATE TOGGLE ────────────────────────────────────────────── */
const autoRotateBtn = document.getElementById('auto-rotate-btn');
autoRotateBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autoRotateBtn.textContent = controls.autoRotate ? 'AUTO ROTATE: ON' : 'AUTO ROTATE: OFF';
  autoRotateBtn.classList.toggle('on', controls.autoRotate);
});
/* ── BOOKMARK BUTTONS ──────────────────────────────────────────────── */
const bmBtns = document.querySelectorAll('.bm-btn');
bmBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.bm);
    const bm = bookmarks[idx];
    if (!bm) return;
    // Smooth animate camera to bookmark position
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const endPos = new THREE.Vector3(...bm.pos);
    const endTarget = new THREE.Vector3(...bm.target);
    const startTime = performance.now();
    const duration = 800;
    function animCam(now) {
      const elapsed = now - startTime;
      const t = Math.min(1.0, elapsed / duration);
      // Ease in-out
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      camera.position.lerpVectors(startPos, endPos, ease);
      controls.target.lerpVectors(startTarget, endTarget, ease);
      controls.update();
      if (t < 1.0) {
        requestAnimationFrame(animCam);
      }
    }
    requestAnimationFrame(animCam);
    // Highlight active bookmark
    bmBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});
/* ── WORLD-TO-GRID MEMOIZATION ─────────────────────────────────────── */
/*
  Converts world-space position to terrain grid index.
  Uses Math.round for key generation — avoids floating-point mismatch
  that would cause cache misses (the exact bug from prior feedback).
  Memo cleared once per frame.
*/
function worldToGrid(worldPos) {
  const half = TERRAIN_SIZE / 2;
  const cellSize = TERRAIN_SIZE / (GRID - 1);
  // Consistent precision: round to 2 decimal places for the key
  const kx = Math.round(worldPos.x * 100);
  const kz = Math.round(worldPos.z * 100);
  const key = `${kx},${kz}`;
  if (Cache.worldToGridMemo.has(key)) {
    Cache.stats.w2gHits++;
    return Cache.worldToGridMemo.get(key);
  }
  Cache.stats.w2gMisses++;
  const ix = Math.round(worldPos.x / cellSize + half / cellSize);
  const iz = Math.round(worldPos.z / cellSize + half / cellSize);
  const result = {
    ix: Math.max(0, Math.min(GRID - 1, ix)),
    iz: Math.max(0, Math.min(GRID - 1, iz))
  };
  Cache.worldToGridMemo.set(key, result);
  return result;
}
/* ── DIAGNOSTIC PANEL UPDATE ───────────────────────────────────────── */
const diagFps = document.getElementById('diag-fps');
const diagTerrain = document.getElementById('diag-terrain');
const diagRiver = document.getElementById('diag-river');
const diagW2g = document.getElementById('diag-w2g');
const diagPart = document.getElementById('diag-part');
let frameCount = 0;
let fpsAccum = 0;
let lastFpsUpdate = performance.now();
function updateDiagnostics(now) {
  frameCount++;
  fpsAccum++;
  if (now - lastFpsUpdate > 500) {
    const fps = Math.round(fpsAccum / ((now - lastFpsUpdate) / 1000));
    diagFps.textContent = fps;
    fpsAccum = 0;
    lastFpsUpdate = now;
  }
  const ts = Cache.stats;
  const tTotal = ts.terrainHits + ts.terrainMisses || 1;
  const rTotal = ts.riverHits + ts.riverMisses || 1;
  const wTotal = ts.w2gHits + ts.w2gMisses || 1;
  diagTerrain.textContent = `${ts.terrainHits}/${tTotal} (${Math.round(ts.terrainHits/tTotal*100)}%)`;
  diagRiver.textContent = `${ts.riverHits}/${rTotal} (${Math.round(ts.riverHits/rTotal*100)}%)`;
  diagW2g.textContent = `${ts.w2gHits}/${wTotal} (${Math.round(ts.w2gHits/wTotal*100)}%)`;
  diagPart.textContent = ts.particleSwaps;
}
/* ── RESIZE HANDLER ────────────────────────────────────────────────── */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ── RENDER LOOP ───────────────────────────────────────────────────── */
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  const now = performance.now();
  controls.update();
  // Update particles in-place (reuses position array)
  updateParticles(currentTime, dt);
  // Clear worldToGrid memo each frame (valid for one frame of hover/tooltip lookups)
  Cache.worldToGridMemo.clear();
  renderer.render(scene, camera);
  updateDiagnostics(now);
}
// Initial time step application
applyTimeStep(0);
animate();
console.log('3D Data Terrain Explorer ready.');
console.log(`  Grid: ${GRID}×${GRID}  |  Time steps: ${TIME_STEPS}  |  Particles: ${PARTICLE_COUNT}`);
console.log('  Cache: terrain geometries pre-built, rivers pre-traced, W2G memoized, particle buffer reused');
</script>
</body>
</html>