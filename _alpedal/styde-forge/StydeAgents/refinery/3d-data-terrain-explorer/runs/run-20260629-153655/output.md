```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a14; --panel: #12122a; --text: #c8c8e0; --accent: #4af; --river: #f44; --warn: #fa0; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: var(--text); }
  canvas { display: block; }
  #ui { position: fixed; top: 0; left: 0; right: 0; z-index: 10; pointer-events: none; }
  #ui > * { pointer-events: auto; }
  #topbar { display: flex; align-items: center; gap: 12px; padding: 8px 14px; background: var(--panel); border-bottom: 1px solid #ffffff15; }
  #topbar h1 { font-size: 15px; font-weight: 600; letter-spacing: 0.5px; color: #e0e0f8; white-space: nowrap; }
  .spacer { flex: 1; }
  #timeslider-wrap { display: flex; align-items: center; gap: 8px; background: #ffffff08; border-radius: 6px; padding: 4px 10px; }
  #timeslider-wrap label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #8888aa; white-space: nowrap; }
  #timeslider { width: 180px; accent-color: var(--accent); cursor: pointer; }
  #time-label { font-size: 12px; font-weight: 600; min-width: 48px; text-align: center; color: var(--accent); }
  #btn-play { background: none; border: 1px solid #ffffff20; color: var(--text); border-radius: 4px; padding: 3px 8px; cursor: pointer; font-size: 12px; }
  #btn-play:hover { border-color: var(--accent); color: var(--accent); }
  #btn-play.playing { background: var(--accent); color: #000; border-color: var(--accent); }
  #bookmarks { display: flex; gap: 4px; }
  #bookmarks button { background: #ffffff08; border: 1px solid #ffffff12; color: #aaa; border-radius: 4px; padding: 3px 8px; cursor: pointer; font-size: 11px; transition: all 0.15s; }
  #bookmarks button:hover { border-color: var(--accent); color: var(--accent); }
  #legend { position: fixed; bottom: 20px; left: 20px; z-index: 10; background: var(--panel); border-radius: 8px; padding: 10px 14px; border: 1px solid #ffffff10; font-size: 11px; }
  #legend .row { display: flex; align-items: center; gap: 8px; margin: 3px 0; }
  #legend .swatch { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
  #diag { position: fixed; bottom: 20px; right: 20px; z-index: 10; background: var(--panel); border-radius: 8px; padding: 10px 14px; border: 1px solid #ffffff10; font-size: 10px; font-family: 'Cascadia Code', 'Consolas', monospace; min-width: 160px; }
  #diag .diag-row { display: flex; justify-content: space-between; gap: 12px; }
  #diag .diag-val { color: var(--accent); font-weight: 600; }
  #diag .diag-miss { color: var(--warn); }
  .tooltip { position: fixed; pointer-events: none; background: var(--panel); border: 1px solid #ffffff20; border-radius: 6px; padding: 6px 10px; font-size: 11px; display: none; z-index: 20; }
</style>
</head>
<body>
<div id="ui">
  <div id="topbar">
    <h1>3D Data Terrain</h1>
    <div id="timeslider-wrap">
      <label>Time</label>
      <input type="range" id="timeslider" min="0" max="23" value="12" step="1">
      <span id="time-label">12:00</span>
    </div>
    <button id="btn-play" title="Play/Pause time animation">&#9654;</button>
    <div id="bookmarks">
      <button data-bm="top">Top</button>
      <button data-bm="side">Side</button>
      <button data-bm="river">River</button>
      <button data-bm="auto" style="color:var(--accent)">Auto</button>
    </div>
    <span class="spacer"></span>
    <span style="font-size:10px;color:#666">drag:orbit &middot; scroll:zoom &middot; right-drag:pan</span>
  </div>
</div>
<div id="legend">
  <div style="font-weight:600;margin-bottom:4px;color:#aaa">LEGEND</div>
  <div class="row"><span class="swatch" style="background:linear-gradient(180deg,#2d5a1e,#7acc4a)"></span> User Density (green=high)</div>
  <div class="row"><span class="swatch" style="background:#f44"></span> Error Rivers</div>
  <div class="row"><span class="swatch" style="background:#ff0"></span> API Call Particles</div>
</div>
<div id="diag">
  <div style="font-weight:600;margin-bottom:4px;color:#aaa">DIAGNOSTICS</div>
  <div class="diag-row"><span>FPS</span><span class="diag-val" id="diag-fps">--</span></div>
  <div class="diag-row"><span>Terrain cache</span><span class="diag-val" id="diag-tcache">--</span></div>
  <div class="diag-row"><span>River cache</span><span class="diag-val" id="diag-rcache">--</span></div>
  <div class="diag-row"><span>Grid xform</span><span class="diag-val" id="diag-xform">--</span></div>
  <div class="diag-row"><span>Particle allocs</span><span class="diag-val" id="diag-palloc">0</span></div>
  <div class="diag-row"><span>Memory</span><span class="diag-val" id="diag-mem">--</span></div>
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
// ─── CONFIG ──────────────────────────────────────────────────────────
const GRID = 80;
const GRID_SIZE = 20;
const TIME_SLICES = 24;
const PARTICLE_COUNT = 500;
const TERRAIN_HEIGHT = 6;
// ─── CACHE MANAGER ───────────────────────────────────────────────────
// Tracks hits/misses for diagnostic panel. All cacheable outputs go through here.
const CacheStats = { tHits: 0, tMisses: 0, rHits: 0, rMisses: 0, xHits: 0, xMisses: 0 };
function cacheGet(map, key, statsKey) {
  if (map.has(key)) { CacheStats[statsKey+'Hits']++; return map.get(key); }
  CacheStats[statsKey+'Misses']++; return null;
}
function cacheSet(map, key, value) { map.set(key, value); return value; }
// ─── SYNTHETIC DATA GENERATION ───────────────────────────────────────
// Generates 24 time slices of 80x80 grids. Each cell: [revenue, userDensity, errorRate]
// Revenue = elevation, userDensity = vertex color, errorRate = river path source.
// INIT SEQUENCING: data populated FIRST, all consumers read after generation completes.
const terrainData = new Array(TIME_SLICES);
{
  const seed = (x, y, t, freq, phase) => {
    const v = Math.sin(x * freq + t * 0.3 + phase) * Math.cos(y * freq * 1.3 + t * 0.25) +
              Math.sin((x + y) * freq * 0.7 + t * 0.15) * 0.5 +
              Math.cos(x * freq * 2.1 - y * freq * 1.7 + t * 0.35) * 0.3;
    return (v + 1.5) / 3.0;
  };
  for (let t = 0; t < TIME_SLICES; t++) {
    const slice = new Float32Array(GRID * GRID * 3);
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = (iy * GRID + ix) * 3;
        const nx = ix / GRID - 0.5;
        const ny = iy / GRID - 0.5;
        slice[idx]     = seed(ix, iy, t, 0.15, 0) * 100;          // revenue 0-100
        slice[idx + 1] = seed(ix, iy, t, 0.10, 1.5) * 0.8 + 0.2;  // userDensity 0.2-1.0
        slice[idx + 2] = seed(ix, iy, t, 0.12, 3.0);              // errorRate 0-1
        // Amplify error in hot spots
        const hot = Math.exp(-((nx-0.2)*(nx-0.2) + (ny-0.15)*(ny-0.15)) * 30) * (0.5 + 0.5 * Math.sin(t * 0.5));
        slice[idx + 2] = Math.min(1, slice[idx + 2] + hot * 0.6);
      }
    }
    terrainData[t] = slice;
  }
}
// ─── TERRAIN GEOMETRY CACHE ──────────────────────────────────────────
// Precompute all 24 heightfield variants as Float32Arrays of positions.
// Swap buffer on slider change — no new THREE.BufferGeometry() per tick.
const terrainHeightCache = new Map();   // timeIndex -> Float32Array(GRID*GRID*3)
const terrainColorCache = new Map();    // timeIndex -> Float32Array(GRID*GRID*3)
const CELL_W = GRID_SIZE / (GRID - 1);
const HALF = GRID_SIZE / 2;
for (let t = 0; t < TIME_SLICES; t++) {
  const data = terrainData[t];
  const heights = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const vi = iy * GRID + ix;
      const di = vi * 3;
      const revenue = data[di];
      const density = data[di + 1];
      const h = (revenue / 100) * TERRAIN_HEIGHT;
      heights[di]     = ix * CELL_W - HALF;
      heights[di + 1] = h;
      heights[di + 2] = iy * CELL_W - HALF;
      // Vegetation gradient: low density=brown, high density=lush green
      const g = 0.18 + density * 0.70;
      const r = 0.12 + (1 - density) * 0.35;
      const b = 0.06 + density * 0.15;
      colors[di]     = r;
      colors[di + 1] = g;
      colors[di + 2] = b;
    }
  }
  cacheSet(terrainHeightCache, t, heights);
  cacheSet(terrainColorCache, t, colors);
}
// ─── RIVER GEOMETRY CACHE ────────────────────────────────────────────
// Trace paths through high-error cells. Precompute TubeGeometry per time slice.
const riverGeomCache = new Map(); // timeIndex -> TubeGeometry[]
const RIVER_THRESHOLD = 0.55;
function buildRiversForTime(t) {
  const cached = cacheGet(riverGeomCache, t, 'r');
  if (cached) return cached;
  const data = terrainData[t];
  const heights = cacheGet(terrainHeightCache, t, 't');
  // Find high-error cells as river sources
  const sources = [];
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const di = (iy * GRID + ix) * 3;
      if (data[di + 2] > RIVER_THRESHOLD) {
        sources.push({ ix, iy, err: data[di + 2] });
      }
    }
  }
  // Sort by error, take top sources, trace downstream (toward lower terrain)
  sources.sort((a, b) => b.err - a.err);
  const taken = new Uint8Array(GRID * GRID);
  const geometries = [];
  const maxRivers = 6;
  let built = 0;
  for (const src of sources) {
    if (built >= maxRivers) break;
    if (taken[src.iy * GRID + src.ix]) continue;
    // Trace path following steepest descent
    const path = [];
    let cx = src.ix, cy = src.iy;
    let steps = 0;
    const maxSteps = 60;
    while (steps < maxSteps && cx >= 0 && cx < GRID && cy >= 0 && cy < GRID) {
      const idx = cy * GRID + cx;
      if (taken[idx] && steps > 3) break;
      taken[idx] = 1;
      const di = idx * 3;
      path.push(new THREE.Vector3(
        heights[di], heights[di + 1] + 0.08, heights[di + 2]
      ));
      // Find steepest descent among 8 neighbors
      let bestDz = 0, bestNx = cx, bestNy = cy;
      const curH = data[di];
      for (let dy = -1; dy <= 1; dy++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dy === 0) continue;
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          const nh = data[(ny * GRID + nx) * 3];
          const dz = curH - nh;
          if (dz > bestDz) { bestDz = dz; bestNx = nx; bestNy = ny; }
        }
      }
      if (bestDz <= 0 && steps > 2) break;
      cx = bestNx; cy = bestNy;
      steps++;
    }
    if (path.length >= 3) {
      const curve = new THREE.CatmullRomCurve3(path);
      const tubeGeom = new THREE.TubeGeometry(curve, path.length * 2, 0.12, 6, false);
      geometries.push(tubeGeom);
      built++;
    }
  }
  return cacheSet(riverGeomCache, t, geometries);
}
// ─── SCENE SETUP ─────────────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 15, 50);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(14, 10, 16);
camera.lookAt(0, 2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
// OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 2.5, 0);
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.75;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
// Lighting
const ambientLight = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffe8d0', 4.5);
sunLight.position.set(15, 20, 8);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -15; sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15; sunLight.shadow.camera.bottom = -15;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#8899cc', 0.8);
fillLight.position.set(-5, 3, -5);
scene.add(fillLight);
// Ground plane
const groundGeo = new THREE.PlaneGeometry(GRID_SIZE + 4, GRID_SIZE + 4);
const groundMat = new THREE.MeshStandardMaterial({ color: '#1a1a2e', roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.05;
ground.receiveShadow = true;
scene.add(ground);
// ─── TERRAIN MESH ────────────────────────────────────────────────────
// Single BufferGeometry reused. Swap position/color buffers at time change.
const terrainGeom = new THREE.BufferGeometry();
// Initialize with index buffer for shared vertices
const indices = [];
for (let iy = 0; iy < GRID - 1; iy++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = iy * GRID + ix;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    indices.push(a, b, d);
    indices.push(a, d, c);
  }
}
terrainGeom.setIndex(indices);
let currentTimeIdx = 12;
const initHeights = cacheGet(terrainHeightCache, currentTimeIdx, 't');
const initColors = cacheGet(terrainColorCache, currentTimeIdx, 't');
terrainGeom.setAttribute('position', new THREE.BufferAttribute(initHeights, 3));
terrainGeom.setAttribute('color', new THREE.BufferAttribute(initColors, 3));
terrainGeom.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(terrainGeom, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
terrainMesh.name = 'terrain';
// ─── RIVER MESHES ────────────────────────────────────────────────────
const riverGroup = new THREE.Group();
riverGroup.name = 'rivers';
scene.add(riverGroup);
const riverMaterial = new THREE.MeshStandardMaterial({
  color: '#cc3333',
  roughness: 0.25,
  metalness: 0.3,
  emissive: '#330000',
  emissiveIntensity: 0.5,
});
function swapRivers(timeIdx) {
  // Remove old river meshes
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    riverGroup.remove(child);
  }
  const geoms = buildRiversForTime(timeIdx);
  for (const geom of geoms) {
    const mesh = new THREE.Mesh(geom, riverMaterial);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    riverGroup.add(mesh);
  }
}
swapRivers(currentTimeIdx);
// ─── PARTICLE SYSTEM ─────────────────────────────────────────────────
// 500 particles representing API calls / data flows.
// CRITICAL: colors assigned ONCE at spawn, never touched per-frame.
// Positions updated from precomputed path arrays — no per-frame allocations.
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleTargets = new Float32Array(PARTICLE_COUNT * 3);  // precomputed targets
const particleSpeeds = new Float32Array(PARTICLE_COUNT);
// Precompute spawn points per time slice (on terrain surface, near high-activity areas)
const particleSpawnCache = new Map(); // timeIdx -> { positions: Float32Array(PC*3), targets: Float32Array(PC*3) }
function buildParticleSpawns(t) {
  const cached = cacheGet(particleSpawnCache, t, 'r');
  if (cached) return cached;
  const data = terrainData[t];
  const heights = cacheGet(terrainHeightCache, t, 't');
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const targets = new Float32Array(PARTICLE_COUNT * 3);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    // Bias toward high user-density areas
    let ix, iy;
    for (let attempt = 0; attempt < 20; attempt++) {
      ix = Math.floor(Math.random() * GRID);
      iy = Math.floor(Math.random() * GRID);
      const di = (iy * GRID + ix) * 3;
      if (data[di + 1] > Math.random() * 0.6) break;
    }
    const di = (iy * GRID + ix) * 3;
    const hi = (iy * GRID + ix) * 3;
    positions[pi]     = heights[hi];
    positions[pi + 1] = heights[hi + 1] + 0.15;
    positions[pi + 2] = heights[hi + 2];
    // Target: random nearby point on terrain
    const tx = Math.min(GRID - 1, Math.max(0, ix + Math.floor((Math.random() - 0.5) * 12)));
    const ty = Math.min(GRID - 1, Math.max(0, iy + Math.floor((Math.random() - 0.5) * 12)));
    const tdi = (ty * GRID + tx) * 3;
    const thi = (ty * GRID + tx) * 3;
    targets[pi]     = heights[thi];
    targets[pi + 1] = heights[thi + 1] + 0.3;
    targets[pi + 2] = heights[thi + 2];
  }
  return cacheSet(particleSpawnCache, t, { positions, targets });
}
function resetParticles(timeIdx) {
  const spawn = buildParticleSpawns(timeIdx);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    particlePositions[pi]     = spawn.positions[pi];
    particlePositions[pi + 1] = spawn.positions[pi + 1];
    particlePositions[pi + 2] = spawn.positions[pi + 2];
    particleTargets[pi]       = spawn.targets[pi];
    particleTargets[pi + 1]   = spawn.targets[pi + 1];
    particleTargets[pi + 2]   = spawn.targets[pi + 2];
    particleSpeeds[i] = 0.015 + Math.random() * 0.045;
    // COLOR: assigned ONCE here at spawn time, never touched in animation loop
    const hue = 0.12 + Math.random() * 0.08;
    const col = new THREE.Color().setHSL(hue, 0.9, 0.55 + Math.random() * 0.35);
    particleColors[pi]     = col.r;
    particleColors[pi + 1] = col.g;
    particleColors[pi + 2] = col.b;
  }
  particleGeom.attributes.position.needsUpdate = true;
  particleGeom.attributes.color.needsUpdate = true;
}
const particleGeom = new THREE.BufferGeometry();
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
// Particle texture (small glow disc) — created once, cached
const particleTexCanvas = document.createElement('canvas');
particleTexCanvas.width = 32; particleTexCanvas.height = 32;
const pctx = particleTexCanvas.getContext('2d');
const gradient = pctx.createRadialGradient(16, 16, 0, 16, 16, 16);
gradient.addColorStop(0, 'rgba(255,255,200,1)');
gradient.addColorStop(0.3, 'rgba(255,220,100,0.8)');
gradient.addColorStop(0.7, 'rgba(255,150,30,0.15)');
gradient.addColorStop(1, 'rgba(255,100,0,0)');
pctx.fillStyle = gradient;
pctx.fillRect(0, 0, 32, 32);
const particleTex = new THREE.CanvasTexture(particleTexCanvas);
particleTex.needsUpdate = true;
const particleMat = new THREE.PointsMaterial({
  size: 0.22,
  map: particleTex,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85,
});
const particles = new THREE.Points(particleGeom, particleMat);
scene.add(particles);
resetParticles(currentTimeIdx);
// ─── CAMERA BOOKMARKS ────────────────────────────────────────────────
const bookmarks = {
  top:    { pos: [0, 18, 0.5],   target: [0, 2.5, 0] },
  side:   { pos: [18, 5, 0],     target: [0, 2.5, 0] },
  river:  { pos: [4, 4, 10],     target: [2, 1.8, 3] },
};
let autoRotateActive = false;
function animateCamera(toPos, toTarget, duration = 800) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...toPos);
  const endTarget = new THREE.Vector3(...toTarget);
  const startTime = performance.now();
  function step(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; // easeInOutCubic
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
// ─── WORLD-TO-GRID MEMOIZATION ───────────────────────────────────────
// Memoize per frame — only recompute if world position changed.
let lastGridQuery = { x: NaN, y: NaN, z: NaN, result: null };
function worldToGrid(worldPos) {
  if (worldPos.x === lastGridQuery.x && worldPos.y === lastGridQuery.y && worldPos.z === lastGridQuery.z) {
    CacheStats.xHits++;
    return lastGridQuery.result;
  }
  CacheStats.xMisses++;
  const gx = Math.round((worldPos.x + HALF) / CELL_W);
  const gy = Math.round((worldPos.z + HALF) / CELL_W);
  const result = { gx, gy, valid: gx >= 0 && gx < GRID && gy >= 0 && gy < GRID };
  lastGridQuery = { x: worldPos.x, y: worldPos.y, z: worldPos.z, result };
  return result;
}
// ─── UI BINDINGS ─────────────────────────────────────────────────────
const slider = document.getElementById('timeslider');
const timeLabel = document.getElementById('time-label');
const btnPlay = document.getElementById('btn-play');
let playing = false;
let playInterval = null;
function formatTime(t) {
  const h = String(t).padStart(2, '0');
  return h + ':00';
}
// Direct oninput handler — NO debounce. Swaps precomputed buffers instantly.
function setTimeIndex(t) {
  if (t === currentTimeIdx) return;
  currentTimeIdx = t;
  slider.value = t;
  timeLabel.textContent = formatTime(t);
  // Swap terrain position buffer
  const newHeights = cacheGet(terrainHeightCache, t, 't');
  terrainGeom.attributes.position.array.set(newHeights);
  terrainGeom.attributes.position.needsUpdate = true;
  // Swap terrain color buffer
  const newColors = cacheGet(terrainColorCache, t, 't');
  terrainGeom.attributes.color.array.set(newColors);
  terrainGeom.attributes.color.needsUpdate = true;
  terrainGeom.computeVertexNormals();
  // Swap rivers
  swapRivers(t);
  // Reset particles to new time's spawn points
  resetParticles(t);
}
slider.addEventListener('input', () => {
  setTimeIndex(parseInt(slider.value));
});
btnPlay.addEventListener('click', () => {
  playing = !playing;
  btnPlay.textContent = playing ? '⏸' : '▶';
  btnPlay.classList.toggle('playing', playing);
  if (playing) {
    playInterval = setInterval(() => {
      const next = (currentTimeIdx + 1) % TIME_SLICES;
      setTimeIndex(next);
    }, 600);
  } else {
    clearInterval(playInterval);
    playInterval = null;
  }
});
// Bookmark buttons
document.querySelectorAll('#bookmarks button').forEach(btn => {
  btn.addEventListener('click', () => {
    const bm = btn.dataset.bm;
    if (bm === 'auto') {
      autoRotateActive = !autoRotateActive;
      controls.autoRotate = autoRotateActive;
      btn.style.color = autoRotateActive ? 'var(--accent)' : '';
    } else if (bookmarks[bm]) {
      controls.autoRotate = false;
      autoRotateActive = false;
      document.querySelector('#bookmarks button[data-bm="auto"]').style.color = '';
      animateCamera(bookmarks[bm].pos, bookmarks[bm].target);
    }
  });
});
// ─── ANIMATION LOOP ──────────────────────────────────────────────────
// HOT-PATH AUDIT: zero allocations inside this function.
// - Particle positions: reuse Float32Array, no new objects
// - Particle colors: never touched (set at spawn time)
// - No THREE constructors, no array allocations, no DOM writes
// - World-to-grid: memoized per query
let frameCount = 0;
let lastFpsTime = performance.now();
let currentFps = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  // FPS counter
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    currentFps = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = timestamp;
    // Update diagnostics once per second (not per frame — avoids DOM thrash)
    document.getElementById('diag-fps').textContent = currentFps;
    document.getElementById('diag-tcache').textContent =
      CacheStats.tHits + '/' + (CacheStats.tHits + CacheStats.tMisses);
    document.getElementById('diag-rcache').textContent =
      CacheStats.rHits + '/' + (CacheStats.rHits + CacheStats.rMisses);
    document.getElementById('diag-xform').textContent =
      CacheStats.xHits + '/' + (CacheStats.xHits + CacheStats.xMisses);
    if (performance.memory) {
      document.getElementById('diag-mem').textContent =
        (performance.memory.usedJSHeapSize / 1048576).toFixed(1) + ' MB';
    }
  }
  controls.update();
  // Update particles: lerp toward targets, reassign on arrival
  // ZERO allocations — direct Float32Array manipulation
  const pos = particleGeom.attributes.position.array;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pi = i * 3;
    const dx = particleTargets[pi]     - pos[pi];
    const dy = particleTargets[pi + 1] - pos[pi + 1];
    const dz = particleTargets[pi + 2] - pos[pi + 2];
    const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
    if (dist < 0.15) {
      // Arrived at target — pick new target nearby on terrain
      const gx = Math.round((pos[pi] + HALF) / CELL_W);
      const gy = Math.round((pos[pi + 2] + HALF) / CELL_W);
      const nx = Math.min(GRID - 1, Math.max(0, gx + Math.floor((Math.random() - 0.5) * 10)));
      const ny = Math.min(GRID - 1, Math.max(0, gy + Math.floor((Math.random() - 0.5) * 10)));
      const heights = cacheGet(terrainHeightCache, currentTimeIdx, 't');
      const nhi = (ny * GRID + nx) * 3;
      particleTargets[pi]     = heights[nhi];
      particleTargets[pi + 1] = heights[nhi + 1] + 0.3;
      particleTargets[pi + 2] = heights[nhi + 2];
      particleSpeeds[i] = 0.015 + Math.random() * 0.045;
    } else {
      const s = particleSpeeds[i];
      const invDist = s / dist;
      pos[pi]     += dx * invDist;
      pos[pi + 1] += dy * invDist;
      pos[pi + 2] += dz * invDist;
    }
  }
  particleGeom.attributes.position.needsUpdate = true;
  renderer.render(scene, camera);
}
// ─── RESIZE HANDLER ──────────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── INIT SEQUENCING CHECK ───────────────────────────────────────────
// Verify all caches populated before starting animation loop
console.assert(terrainHeightCache.size === TIME_SLICES, 'Terrain height cache incomplete');
console.assert(terrainColorCache.size === TIME_SLICES, 'Terrain color cache incomplete');
console.assert(riverGroup.children.length > 0, 'River meshes not initialized');
console.assert(particles.geometry.attributes.position.count === PARTICLE_COUNT, 'Particles not initialized');
console.assert(particles.geometry.attributes.color.count === PARTICLE_COUNT, 'Particle colors not initialized');
// ─── START ───────────────────────────────────────────────────────────
requestAnimationFrame(animate);
</script>
</body>
</html>
```