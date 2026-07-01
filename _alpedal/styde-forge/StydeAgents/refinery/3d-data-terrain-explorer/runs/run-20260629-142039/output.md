```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10,10,30,0.92);
    --text: #c8d6e5;
    --accent: #4ecdc4;
    --warn: #ff6b6b;
    --muted: #5f6b7a;
    --border: rgba(255,255,255,0.08);
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  #canvas-container { position:fixed; inset:0; z-index:0; }
  canvas { display:block; }
  /* Panel */
  #panel {
    position:fixed; top:16px; right:16px; z-index:10;
    background:var(--panel-bg); backdrop-filter:blur(20px);
    border:1px solid var(--border); border-radius:12px;
    padding:16px 20px; width:280px; max-height:calc(100vh - 32px);
    overflow-y:auto; font-size:13px; line-height:1.5;
    box-shadow:0 8px 32px rgba(0,0,0,0.5);
  }
  #panel h2 { font-size:15px; font-weight:600; color:var(--accent); margin-bottom:12px; letter-spacing:0.02em; }
  /* Slider */
  .slider-group { margin-bottom:14px; }
  .slider-group label { display:flex; justify-content:space-between; font-size:11px; color:var(--muted); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px; }
  .slider-group label span { color:var(--accent); font-weight:600; }
  input[type=range] { width:100%; accent-color:var(--accent); }
  /* Legend */
  #legend { margin:12px 0; }
  .legend-row { display:flex; align-items:center; gap:8px; margin-bottom:3px; font-size:11px; }
  .legend-swatch { width:48px; height:10px; border-radius:2px; flex-shrink:0; }
  .legend-label { flex:1; text-align:right; color:var(--muted); }
  /* Bookmarks */
  #bookmarks { margin-top:12px; }
  .bookmark-btn {
    display:block; width:100%; text-align:left; padding:6px 10px;
    margin-bottom:3px; background:rgba(255,255,255,0.04);
    border:1px solid var(--border); border-radius:6px;
    color:var(--text); cursor:pointer; font-size:11px;
    transition:background 0.15s;
  }
  .bookmark-btn:hover { background:rgba(78,205,196,0.12); }
  /* Tooltip */
  #tooltip {
    position:fixed; pointer-events:none; z-index:20;
    background:rgba(0,0,0,0.85); backdrop-filter:blur(8px);
    border:1px solid var(--accent); border-radius:8px;
    padding:8px 12px; font-size:11px; line-height:1.5;
    display:none; white-space:nowrap;
  }
  #tooltip .val { color:var(--accent); font-weight:600; }
  #tooltip .err { color:var(--warn); }
  /* Cache panel */
  #cache-panel {
    margin-top:12px; padding:8px; border-top:1px solid var(--border);
    font-size:10px; color:var(--muted);
  }
  #cache-panel .hit { color:#51cf66; }
  #cache-panel .miss { color:var(--warn); }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="panel">
  <h2>Terrain Explorer</h2>
  <div class="slider-group">
    <label>Time <span id="time-label">Day 15 / 30</span></label>
    <input type="range" id="time-slider" min="0" max="29" value="14" step="1">
  </div>
  <div class="slider-group">
    <label>Exaggeration <span id="exag-label">3.0x</span></label>
    <input type="range" id="exag-slider" min="1" max="8" value="3" step="0.5">
  </div>
  <div id="legend">
    <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to right,#2d5016,#7ba828,#c8d643,#f5e56c,#d4a843);"></div><div class="legend-label">Revenue (height)</div></div>
    <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to right,#1a3a1a,#3a6b2a,#6ba340,#a0c860,#d4e88c);"></div><div class="legend-label">User Density</div></div>
    <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to right,#4a0a0a,#a82020,#e84040);"></div><div class="legend-label">Error Rate</div></div>
  </div>
  <div id="bookmarks">
    <button class="bookmark-btn" data-view="overview">Overview (isometric)</button>
    <button class="bookmark-btn" data-view="topdown">Top-down</button>
    <button class="bookmark-btn" data-view="front">Front face</button>
    <button class="bookmark-btn" data-view="side">Side profile</button>
  </div>
  <div id="cache-panel">
    Cache: <span class="hit" id="cache-hits">0</span> hits / <span class="miss" id="cache-misses">0</span> misses
  </div>
</div>
<div id="tooltip"></div>
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
/* ===== SYNTHETIC TIME-SERIES DATA GENERATOR ===== */
const GRID = 64;
const DAYS = 30;
const seeds = {
  revenue:  [0.3, 0.7, 1.2, 2.1, 1.8, 2.5, 3.0, 2.7, 3.5, 4.0, 3.9, 4.5, 5.1, 5.8, 5.2, 5.9, 6.3, 6.0, 6.8, 7.2, 7.0, 7.5, 8.0, 7.7, 8.3, 8.8, 8.5, 9.0, 9.3, 9.1],
  users:    [0.5, 0.8, 1.0, 1.3, 1.5, 1.9, 2.2, 2.1, 2.4, 2.8, 3.0, 3.3, 3.5, 3.8, 3.7, 4.0, 4.2, 4.1, 4.4, 4.6, 4.5, 4.8, 5.0, 4.9, 5.1, 5.3, 5.2, 5.5, 5.7, 5.6],
  errors:   [1.2, 0.9, 0.7, 1.0, 0.8, 0.6, 0.5, 0.7, 0.4, 0.3, 0.5, 0.4, 0.3, 0.5, 0.6, 0.4, 0.3, 0.5, 0.4, 0.3, 0.2, 0.4, 0.3, 0.2, 0.3, 0.4, 0.3, 0.2, 0.3, 0.2]
};
function gaussRandom(mean=0, stdev=1) {
  let u=0,v=0;
  while(u===0) u=Math.random();
  while(v===0) v=Math.random();
  return mean + stdev * Math.sqrt(-2*Math.log(u)) * Math.cos(2*Math.PI*v);
}
function generateTerrainData(dayIndex) {
  const t = dayIndex / (DAYS - 1);
  const baseRevenue = seeds.revenue[dayIndex];
  const baseUsers = seeds.users[dayIndex];
  const baseErrors = seeds.errors[dayIndex];
  const heightData = new Float32Array(GRID * GRID);
  const colorData = new Float32Array(GRID * GRID); // user density 0-1
  const errorMask = new Float32Array(GRID * GRID); // error severity 0-1
  const mid = GRID / 2;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const dx = (ix - mid) / mid;
      const dy = (iy - mid) / mid;
      const dist = Math.sqrt(dx*dx + dy*dy);
      // Revenue terrain: peaks near center, grows with time
      const peak = 1.0 - Math.min(dist * 1.4, 1.0);
      const noise = gaussRandom(0, 0.08);
      heightData[idx] = baseRevenue * (peak * 0.8 + 0.2) + noise;
      // User density: spreads outward as time passes
      const userSpread = 0.3 + t * 0.5;
      const userPeak = Math.exp(-dist * dist / (userSpread * userSpread));
      colorData[idx] = Math.min(baseUsers * (userPeak * 0.7 + 0.3) / 10.0 + noise * 0.5, 1.0);
      // Error rivers: concentrated in valleys, strongest early in cycle
      const valleyFactor = Math.max(0, (0.5 - peak) * 2.0);
      const errNoise = Math.abs(gaussRandom(0, 0.03));
      errorMask[idx] = Math.min(baseErrors * valleyFactor + errNoise, 1.0);
    }
  }
  return { heightData, colorData, errorMask };
}
/* ===== CACHE LAYER ===== */
const cache = {
  /* terrain variants keyed by dayIndex */
  terrainGeometries: new Map(),
  /* noise grids keyed by seed+dim */
  noiseGrids: new Map(),
  /* river TubeGeometry keyed by dayIndex+threshold */
  riverGeometries: new Map(),
  /* world-to-grid transform memo (one per frame) */
  worldToGridFrameId: -1,
  worldToGridCache: new Map(),
  /* stats */
  hits: 0,
  misses: 0,
};
function cacheKey(...parts) {
  return parts.join('|');
}
function cacheGet(map, key) {
  if (map.has(key)) { cache.hits++; return map.get(key); }
  cache.misses++;
  return undefined;
}
function cacheSet(map, key, value) {
  map.set(key, value);
}
function updateCacheUI() {
  const hEl = document.getElementById('cache-hits');
  const mEl = document.getElementById('cache-misses');
  if (hEl) hEl.textContent = cache.hits;
  if (mEl) mEl.textContent = cache.misses;
}
/* ===== RIVER PATH GENERATION ===== */
function generateRiverPaths(errorMask, resolution) {
  const threshold = 0.15;
  const visited = new Uint8Array(resolution * resolution);
  const paths = [];
  const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
  for (let iy = 0; iy < resolution; iy++) {
    for (let ix = 0; ix < resolution; ix++) {
      const idx = iy * resolution + ix;
      if (visited[idx] || errorMask[idx] < threshold) continue;
      // Start a river trace from this high-error cell
      const path = [];
      let cx = ix, cy = iy;
      let steps = 0;
      const maxSteps = resolution * 2;
      while (steps < maxSteps) {
        const cidx = cy * resolution + cx;
        if (visited[cidx]) break;
        visited[cidx] = 1;
        path.push([cx, cy, errorMask[cidx]]);
        // Greedy descent: move to unvisited neighbor with highest error
        let bestDir = null;
        let bestVal = -1;
        for (const [dx,dy] of dirs) {
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= resolution || ny < 0 || ny >= resolution) continue;
          const nidx = ny * resolution + nx;
          if (visited[nidx]) continue;
          if (errorMask[nidx] > bestVal) { bestVal = errorMask[nidx]; bestDir = [dx,dy]; }
        }
        if (!bestDir || bestVal < threshold * 0.5) break;
        cx += bestDir[0];
        cy += bestDir[1];
        steps++;
      }
      if (path.length >= 3) paths.push(path);
    }
  }
  return paths;
}
/* ===== THREE.JS SCENE SETUP ===== */
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 8, 30);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 60);
camera.position.set(8, 6, 10);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
/* OrbitControls with saved bookmarks */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 3;
controls.maxDistance = 25;
controls.maxPolarAngle = Math.PI * 0.75;
controls.target.set(0, 1.2, 0);
controls.update();
const bookmarks = {
  overview: { pos:[8,6,10], target:[0,1.2,0] },
  topdown:  { pos:[0,12,0.1], target:[0,0.5,0] },
  front:    { pos:[0,2,12], target:[0,1,0] },
  side:     { pos:[12,2,0], target:[0,1,0] },
};
function applyBookmark(name) {
  const bm = bookmarks[name];
  if (!bm) return;
  // Animate to bookmark position
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  const duration = 800;
  const startTime = performance.now();
  function animate(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease in-out cubic
    const ease = t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3)/2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1.0) requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
}
document.querySelectorAll('.bookmark-btn').forEach(btn => {
  btn.addEventListener('click', () => applyBookmark(btn.dataset.view));
});
/* Lighting */
const ambient = new THREE.AmbientLight('#304060', 1.2);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffe8c8', 3.5);
sun.position.set(10, 15, 8);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 40;
sun.shadow.camera.left = -15;
sun.shadow.camera.right = 15;
sun.shadow.camera.top = 15;
sun.shadow.camera.bottom = -15;
sun.shadow.bias = -0.0003;
scene.add(sun);
const fill = new THREE.DirectionalLight('#4060a0', 0.8);
fill.position.set(-5, 2, -3);
scene.add(fill);
/* Ground reference plane */
const groundGeo = new THREE.PlaneGeometry(16, 16);
const groundMat = new THREE.MeshStandardMaterial({ color:'#0d1117', roughness:0.9, metalness:0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.3;
ground.receiveShadow = true;
scene.add(ground);
/* Grid helper */
const gridHelper = new THREE.PolarGridHelper(7.5, 32, 24, 64, '#1a2a3a', '#1a2a3a');
gridHelper.position.y = -0.29;
scene.add(gridHelper);
/* ===== TERRAIN MESH (object pool pattern) ===== */
const terrainGroup = new THREE.Group();
scene.add(terrainGroup);
let activeTerrainMesh = null;
let activeRiverGroup = null;
// Precompute/cache terrain geometries
function getOrCreateTerrainGeometry(dayIndex) {
  const key = cacheKey('terrain', dayIndex);
  const cached = cacheGet(cache.terrainGeometries, key);
  if (cached) return cached;
  const { heightData, colorData } = generateTerrainData(dayIndex);
  const geo = new THREE.PlaneGeometry(8, 8, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  const cols = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    // PlaneGeometry creates vertices in row-major order matching our data layout
    const x = pos.getX(i);
    const z = pos.getZ(i);
    const h = heightData[i] * 1.5;
    pos.setY(i, h);
    // Vegetation coloring: user density maps to green intensity
    const density = colorData[i];
    // Base terrain colors: low=dark earth, mid=green, high=rock/snow
    const r = 0.15 + h * 0.25 + density * 0.15;
    const g = 0.25 + h * 0.15 + density * 0.55;
    const b = 0.12 + h * 0.08;
    cols[i*3]   = Math.min(r, 1);
    cols[i*3+1] = Math.min(g, 1);
    cols[i*3+2] = Math.min(b, 1);
  }
  geo.setAttribute('color', new THREE.BufferAttribute(cols, 3));
  geo.computeVertexNormals();
  cacheSet(cache.terrainGeometries, key, geo);
  return geo;
}
// River geometry cache — reuse TubeGeometry, only update when terrain changes
function getOrCreateRiverGeometry(dayIndex, exaggeration) {
  const key = cacheKey('river', dayIndex, exaggeration.toFixed(1));
  const cached = cacheGet(cache.riverGeometries, key);
  if (cached) return cached;
  const { errorMask, heightData } = generateTerrainData(dayIndex);
  const paths = generateRiverPaths(errorMask, GRID);
  const group = new THREE.Group();
  const halfExtent = 4; // terrain half-size
  const cellSize = (halfExtent * 2) / GRID;
  paths.forEach(path => {
    if (path.length < 3) return;
    // Build CatmullRom curve from path points
    const points = path.map(([gx, gy, errVal]) => {
      const wx = (gx / (GRID-1) - 0.5) * halfExtent * 2;
      const wz = (gy / (GRID-1) - 0.5) * halfExtent * 2;
      const idx = gy * GRID + gx;
      // Place river slightly above terrain surface
      const wy = heightData[idx] * 1.5 * exaggeration + 0.03;
      return new THREE.Vector3(wx, wy, wz);
    });
    const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
    // TubeGeometry: tubular segments, radius, radial segments, closed
    const tubeGeo = new THREE.TubeGeometry(curve, Math.min(path.length * 4, 80), 0.04, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: '#e83030',
      emissive: '#600000',
      emissiveIntensity: 0.5,
      roughness: 0.4,
      metalness: 0.3,
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.castShadow = true;
    group.add(tube);
    // Glow ribbon alongside
    const ribbonGeo = new THREE.TubeGeometry(curve, Math.min(path.length * 4, 80), 0.015, 4, false);
    const ribbonMat = new THREE.MeshBasicMaterial({ color:'#ff4444', transparent:true, opacity:0.6 });
    const ribbon = new THREE.Mesh(ribbonGeo, ribbonMat);
    group.add(ribbon);
  });
  cacheSet(cache.riverGeometries, key, group);
  return group;
}
/* ===== PARTICLE SYSTEM (InstancedMesh for object pooling) ===== */
const PARTICLE_COUNT = 800;
let particleMesh = null;
let particleData = []; // { velocity, pathIndex, pathProgress, path }
let particlePaths = []; // reusable path cache
function buildParticlePaths(dayIndex) {
  // Generate flow paths along terrain valleys where user-density is moderate
  const { heightData, colorData } = generateTerrainData(dayIndex);
  const halfExtent = 4;
  const cellSize = (halfExtent * 2) / GRID;
  const paths = [];
  // Create paths that follow valleys (high revenue, moderate density)
  const mid = GRID / 2;
  for (let seed = 0; seed < 15; seed++) {
    const startX = Math.floor(5 + Math.random() * (GRID - 10));
    const startY = Math.floor(5 + Math.random() * (GRID - 10));
    const path = [];
    let cx = startX, cy = startY;
    let stuck = 0;
    while (path.length < 40 && stuck < 10) {
      const idx = cy * GRID + cx;
      path.push({
        x: (cx / (GRID-1) - 0.5) * halfExtent * 2,
        z: (cy / (GRID-1) - 0.5) * halfExtent * 2,
        h: heightData[idx] * 1.5,
      });
      // Gradient descent: move toward lower elevation neighbor
      let bestNx = cx, bestNy = cy;
      let bestH = heightData[idx];
      for (const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]) {
        const nx = cx + dx, ny = cy + dy;
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        const nidx = ny * GRID + nx;
        // Prefer valleys: lower elevation + moderate density
        const score = heightData[nidx] - colorData[nidx] * 0.3;
        if (score < bestH) { bestH = score; bestNx = nx; bestNy = ny; }
      }
      if (bestNx === cx && bestNy === cy) stuck++;
      else stuck = 0;
      cx = bestNx;
      cy = bestNy;
    }
    if (path.length >= 8) paths.push(path);
  }
  return paths;
}
function initParticles() {
  // Dispose old mesh if exists
  if (particleMesh) {
    particleMesh.geometry.dispose();
    particleMesh.material.dispose();
    scene.remove(particleMesh);
  }
  // Particle geometry: small glowing spheres
  const sphereGeo = new THREE.SphereGeometry(0.04, 4, 4);
  // InstancedMesh for efficient rendering
  particleMesh = new THREE.InstancedMesh(sphereGeo, new THREE.MeshBasicMaterial({
    color: '#ffe8a0',
    transparent: true,
    opacity: 0.85,
  }), PARTICLE_COUNT);
  particleMesh.castShadow = false;
  particleMesh.frustumCulled = true;
  // Initialize particle data
  particleData = [];
  const dummy = new THREE.Object3D();
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Spread particles initially across a random distribution
    dummy.position.set(
      (Math.random() - 0.5) * 7,
      Math.random() * 3 + 0.2,
      (Math.random() - 0.5) * 7
    );
    dummy.scale.setScalar(0.6 + Math.random() * 0.8);
    dummy.updateMatrix();
    particleMesh.setMatrixAt(i, dummy.matrix);
    particleData.push({
      velocity: 0.3 + Math.random() * 1.2,
      pathIndex: -1, // unassigned
      pathProgress: Math.random(),
      path: null,
      phase: Math.random() * Math.PI * 2,
    });
  }
  particleMesh.instanceMatrix.needsUpdate = true;
  scene.add(particleMesh);
}
function assignParticlesToPaths(dayIndex) {
  particlePaths = buildParticlePaths(dayIndex);
  const dummy = new THREE.Object3D();
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    if (particlePaths.length > 0) {
      pd.pathIndex = i % particlePaths.length;
      pd.path = particlePaths[pd.pathIndex];
      pd.pathProgress = Math.random(); // stagger start positions
    }
    // Position at path start
    if (pd.path && pd.path.length > 0) {
      const pt = pd.path[0];
      dummy.position.set(pt.x, pt.h + 0.1, pt.z);
    } else {
      dummy.position.set((Math.random()-0.5)*7, 0.3, (Math.random()-0.5)*7);
    }
    dummy.scale.setScalar(0.6 + Math.random() * 0.8);
    dummy.updateMatrix();
    particleMesh.setMatrixAt(i, dummy.matrix);
  }
  particleMesh.instanceMatrix.needsUpdate = true;
}
function updateParticles(dt, exaggeration) {
  if (!particleMesh) return;
  const dummy = new THREE.Object3D();
  const clampDt = Math.min(dt, 0.1); // Cap dt to avoid large jumps
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    if (!pd.path || pd.path.length < 2) {
      // Free-floating: gentle drift
      particleMesh.getMatrixAt(i, dummy.matrix);
      dummy.position.y += Math.sin(Date.now()*0.001 + pd.phase) * clampDt * 0.3;
      dummy.position.x += Math.cos(Date.now()*0.0007 + pd.phase) * clampDt * 0.2;
      dummy.position.z += Math.sin(Date.now()*0.0009 + pd.phase) * clampDt * 0.2;
      dummy.position.y = Math.max(0.1, Math.min(dummy.position.y, 5));
      dummy.updateMatrix();
      particleMesh.setMatrixAt(i, dummy.matrix);
      continue;
    }
    // Advance along path
    pd.pathProgress += pd.velocity * clampDt * 0.15;
    if (pd.pathProgress >= 1.0) pd.pathProgress -= 1.0;
    if (pd.pathProgress < 0) pd.pathProgress += 1.0;
    const t = pd.pathProgress * (pd.path.length - 1);
    const idx = Math.floor(t);
    const frac = t - idx;
    const a = pd.path[Math.min(idx, pd.path.length - 1)];
    const b = pd.path[Math.min(idx + 1, pd.path.length - 1)];
    const h = a.h + (b.h - a.h) * frac;
    // Reuse dummy to set instance matrix
    dummy.position.set(
      a.x + (b.x - a.x) * frac,
      h * exaggeration + 0.08,
      a.z + (b.z - a.z) * frac
    );
    dummy.scale.setScalar(0.5 + Math.sin(pd.pathProgress * Math.PI) * 0.5);
    dummy.updateMatrix();
    particleMesh.setMatrixAt(i, dummy.matrix);
  }
  particleMesh.instanceMatrix.needsUpdate = true;
}
/* ===== TERRAIN REBUILD (swaps cached geometry) ===== */
let currentDayIndex = 14;
let currentExaggeration = 3.0;
let rebuildTimer = null;
const REBUILD_DEBOUNCE_MS = 200;
function rebuildTerrain(dayIndex, exaggeration) {
  updateCacheUI();
  // Remove old terrain
  if (activeTerrainMesh) {
    activeTerrainMesh.geometry.dispose();
    activeTerrainMesh.material.dispose();
    terrainGroup.remove(activeTerrainMesh);
    activeTerrainMesh = null;
  }
  // Remove old rivers
  if (activeRiverGroup) {
    activeRiverGroup.traverse(child => {
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
    });
    terrainGroup.remove(activeRiverGroup);
    activeRiverGroup = null;
  }
  const geo = getOrCreateTerrainGeometry(dayIndex);
  // Scale heights by exaggeration
  const pos = geo.attributes.position;
  const { heightData } = generateTerrainData(dayIndex);
  // Apply exaggeration to cached geometry's Y values
  // Since we cache the raw geometry, adjust Y per swap
  for (let i = 0; i < pos.count; i++) {
    pos.setY(i, heightData[i] * 1.5 * exaggeration);
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
  });
  activeTerrainMesh = new THREE.Mesh(geo, mat);
  activeTerrainMesh.castShadow = true;
  activeTerrainMesh.receiveShadow = true;
  terrainGroup.add(activeTerrainMesh);
  // Add rivers
  activeRiverGroup = getOrCreateRiverGeometry(dayIndex, exaggeration);
  terrainGroup.add(activeRiverGroup);
  // Reassign particles to new paths
  assignParticlesToPaths(dayIndex);
  updateCacheUI();
}
function scheduleRebuild() {
  if (rebuildTimer) clearTimeout(rebuildTimer);
  rebuildTimer = setTimeout(() => {
    rebuildTerrain(currentDayIndex, currentExaggeration);
    rebuildTimer = null;
  }, REBUILD_DEBOUNCE_MS);
}
/* ===== UI EVENT HANDLERS ===== */
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const exagSlider = document.getElementById('exag-slider');
const exagLabel = document.getElementById('exag-label');
timeSlider.addEventListener('input', () => {
  currentDayIndex = parseInt(timeSlider.value);
  timeLabel.textContent = `Day ${currentDayIndex + 1} / ${DAYS}`;
  scheduleRebuild();
});
exagSlider.addEventListener('input', () => {
  currentExaggeration = parseFloat(exagSlider.value);
  exagLabel.textContent = currentExaggeration.toFixed(1) + 'x';
  scheduleRebuild();
});
/* ===== HOVER TOOLTIP WITH WORLD-TO-GRID MEMO ===== */
const tooltip = document.getElementById('tooltip');
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
// Memoization state for world-to-grid transforms
let lastFrameW2G = -1;
function worldToGrid(worldX, worldZ, frameId) {
  if (frameId === lastFrameW2G && cache.worldToGridCache.has(`w2g|${worldX.toFixed(3)}|${worldZ.toFixed(3)}`)) {
    return cache.worldToGridCache.get(`w2g|${worldX.toFixed(3)}|${worldZ.toFixed(3)}`);
  }
  const halfExtent = 4;
  const gx = Math.round(((worldX / (halfExtent * 2)) + 0.5) * (GRID - 1));
  const gy = Math.round(((worldZ / (halfExtent * 2)) + 0.5) * (GRID - 1));
  const result = {
    gx: Math.max(0, Math.min(GRID-1, gx)),
    gy: Math.max(0, Math.min(GRID-1, gy)),
  };
  const key = `w2g|${worldX.toFixed(3)}|${worldZ.toFixed(3)}`;
  cache.worldToGridCache.set(key, result);
  return result;
}
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!activeTerrainMesh) { tooltip.style.display = 'none'; return; }
  const intersects = raycaster.intersectObject(activeTerrainMesh, false);
  if (intersects.length === 0) { tooltip.style.display = 'none'; return; }
  const point = intersects[0].point;
  const frameId = performance.now();
  const grid = worldToGrid(point.x, point.z, frameId);
  const idx = grid.gy * GRID + grid.gx;
  const { heightData, colorData, errorMask } = generateTerrainData(currentDayIndex);
  const h = heightData[idx] * 1.5 * currentExaggeration;
  const density = colorData[idx];
  const err = errorMask[idx];
  tooltip.style.display = 'block';
  tooltip.style.left = (e.clientX + 18) + 'px';
  tooltip.style.top = (e.clientY - 10) + 'px';
  tooltip.innerHTML =
    `Grid (${grid.gx}, ${grid.gy})<br>` +
    `Height: <span class="val">${h.toFixed(2)}</span><br>` +
    `Density: <span class="val">${(density*100).toFixed(1)}%</span><br>` +
    `Error: <span class="${err > 0.2 ? 'err' : 'val'}">${(err*100).toFixed(2)}%</span>`;
});
window.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
/* ===== ANIMATION LOOP ===== */
let lastTime = performance.now();
function animate(now) {
  requestAnimationFrame(animate);
  const dt = (now - lastTime) / 1000;
  lastTime = now;
  controls.update();
  updateParticles(dt, currentExaggeration);
  // Reset world-to-grid memo each frame
  if (lastFrameW2G !== Math.floor(now)) {
    lastFrameW2G = Math.floor(now);
    cache.worldToGridCache.clear();
  }
  renderer.render(scene, camera);
}
/* ===== RESIZE HANDLER ===== */
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
/* ===== KEYBOARD SHORTCUTS ===== */
window.addEventListener('keydown', (e) => {
  switch(e.key.toLowerCase()) {
    case '1': applyBookmark('overview'); break;
    case '2': applyBookmark('topdown'); break;
    case '3': applyBookmark('front'); break;
    case '4': applyBookmark('side'); break;
    case 'a': controls.autoRotate = !controls.autoRotate; break;
    case 'r':
      // Reset to default view
      applyBookmark('overview');
      currentDayIndex = 14;
      currentExaggeration = 3.0;
      timeSlider.value = 14;
      exagSlider.value = 3;
      timeLabel.textContent = 'Day 15 / 30';
      exagLabel.textContent = '3.0x';
      rebuildTerrain(currentDayIndex, currentExaggeration);
      break;
  }
});
/* ===== INIT ===== */
initParticles();
rebuildTerrain(currentDayIndex, currentExaggeration);
requestAnimationFrame(animate);
/* Periodic cache stats refresh */
setInterval(updateCacheUI, 2000);
console.log('3D Data Terrain Explorer initialized');
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan');
console.log('Shortcuts: 1-4 bookmarks, A=toggle auto-rotate, R=reset');
console.log('Cache diagnostics visible in panel');
</script>
</body>
</html>
```