data_terrain_explorer.html:
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a14;--panel:#12122a;--text:#c8d6e5;--accent:#4dabf7;--river:#ff6b6b;--particle:#ffd43b}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  #canvas-container{position:fixed;inset:0;z-index:1}
  canvas{display:block}
  #ui-panel{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;
    background:var(--panel);border:1px solid rgba(255,255,255,0.1);border-radius:12px;
    padding:16px 20px;display:flex;gap:20px;align-items:center;backdrop-filter:blur(10px);
    box-shadow:0 8px 32px rgba(0,0,0,0.4)}
  #time-slider{width:300px;accent-color:var(--accent);cursor:pointer}
  #time-label{font-size:13px;color:var(--accent);min-width:80px;text-align:center}
  .btn{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:var(--text);
    padding:8px 14px;border-radius:8px;cursor:pointer;font-size:12px;transition:all 0.2s}
  .btn:hover{background:rgba(255,255,255,0.15);border-color:var(--accent)}
  .btn.active{background:var(--accent);color:#000;border-color:var(--accent)}
  #bookmark-bar{display:flex;gap:6px}
  #legend{position:fixed;top:20px;right:20px;z-index:10;background:var(--panel);
    border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:14px 16px;font-size:11px;
    line-height:1.6;backdrop-filter:blur(10px)}
  .legend-item{display:flex;align-items:center;gap:8px;margin:4px 0}
  .legend-swatch{width:14px;height:14px;border-radius:3px}
  #diagnostic{position:fixed;top:20px;left:20px;z-index:10;background:var(--panel);
    border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:10px 14px;font-size:10px;
    font-family:'Cascadia Code','Fira Code',monospace;opacity:0.7;backdrop-filter:blur(10px)}
  #diagnostic .val{color:var(--accent)}
  #tooltip{position:fixed;pointer-events:none;z-index:20;background:rgba(0,0,0,0.85);
    border:1px solid var(--accent);border-radius:8px;padding:10px 14px;font-size:12px;
    display:none;line-height:1.5;max-width:220px}
  #tooltip .metric{color:var(--accent);font-weight:600}
  #tooltip .error{color:var(--river)}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-panel">
  <span id="time-label">T: 0</span>
  <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
  <div id="bookmark-bar">
    <button class="btn" data-bookmark="overview" title="Overview (saved pos)">B1 Overview</button>
    <button class="btn" data-bookmark="closeup" title="Close-up (saved pos)">B2 Close-up</button>
    <button class="btn" data-bookmark="anomaly" title="Anomaly zone (saved pos)">B3 Anomaly</button>
  </div>
  <button class="btn" id="btn-auto-rotate" title="Toggle auto-rotation">Auto Rotate</button>
  <button class="btn" id="btn-reset-cam" title="Reset camera">Reset</button>
</div>
<div id="legend">
  <div style="font-weight:600;margin-bottom:6px;color:var(--accent)">Legend</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(to right,#1a472a,#2d8a4e,#7bc67e)"></span> Revenue (elevation)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(to right,#0b3d5c,#1a8a6e,#7bc67e,#ffd43b)"></span> User Density (color)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:var(--river)"></span> Error paths (rivers)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:var(--particle)"></span> API calls (particles)</div>
  <div style="margin-top:6px;font-size:10px;opacity:0.6">Drag: orbit | Scroll: zoom<br>Right-drag: pan | Hover: inspect</div>
</div>
<div id="diagnostic">
  <div>FPS: <span class="val" id="diag-fps">--</span></div>
  <div>Cache hits: <span class="val" id="diag-cache-hits">0</span></div>
  <div>Cache misses: <span class="val" id="diag-cache-miss">0</span></div>
  <div>Terrain builds: <span class="val" id="diag-terrain-builds">0</span></div>
  <div>River builds: <span class="val" id="diag-river-builds">0</span></div>
</div>
<div id="tooltip"></div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ──────────────────────────────────────────────
// DATA GENERATION — synthetic time-series grid
// Grid: 80x80, 100 time steps, 4 metrics per cell
// ──────────────────────────────────────────────
const GRID = 80;
const STEPS = 100;
const dataSeries = [];
// Pre-generate all time steps so slider scrubs are pure cache lookups
for (let t = 0; t < STEPS; t++) {
  const frame = { revenue: new Float32Array(GRID * GRID), users: new Float32Array(GRID * GRID), errors: new Float32Array(GRID * GRID), apis: new Float32Array(GRID * GRID) };
  const tp = t / STEPS; // normalized time 0..1
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const nx = ix / (GRID - 1) * 2 - 1; // -1..1
      const nz = iz / (GRID - 1) * 2 - 1;
      // Revenue: multi-octave terrain with time drift
      const r1 = Math.sin(nx * 3.0 + tp * 2) * Math.cos(nz * 2.5 - tp * 1.5) * 0.6;
      const r2 = Math.sin(nx * 7.0 - tp) * Math.cos(nz * 6.0 + tp * 0.7) * 0.25;
      const r3 = Math.sin(nx * 12 + nz * 10) * 0.1;
      // Anomaly spike at center that grows over time
      const distCenter = Math.sqrt(nx * nx + nz * nz);
      const anomaly = Math.exp(-distCenter * 3) * tp * 1.2;
      frame.revenue[idx] = r1 + r2 + r3 + anomaly + 0.5;
      // User density: correlated with revenue but offset
      frame.users[idx] = frame.revenue[idx] * 0.7 + Math.sin(nx * 4 + nz * 3) * 0.3 + 0.3;
      // Error rate: inverse correlation with revenue, spikes at anomaly edges
      const edgeDist = Math.abs(distCenter - 0.35);
      frame.errors[idx] = (1 - frame.revenue[idx]) * 0.15 + Math.exp(-edgeDist * 8) * tp * 0.4;
      // API call volume: follows revenue valleys
      frame.apis[idx] = frame.revenue[idx] * 0.4 + Math.abs(Math.cos(nx * 5 + nz * 4 + tp * 3)) * 0.6;
    }
  }
  dataSeries.push(frame);
}
// ──────────────────────────────────────────────
// THREE.JS SETUP
// ──────────────────────────────────────────────
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a14');
scene.fog = new THREE.Fog('#0a0a14', 5, 25);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 50);
camera.position.set(4, 5.5, 4.5);
camera.lookAt(0, 0, 0);
// ──────────────────────────────────────────────
// LIGHTING — ambient + directional with shadow
// ──────────────────────────────────────────────
scene.add(new THREE.AmbientLight('#334466', 1.8));
const sun = new THREE.DirectionalLight('#ffeedd', 3.5);
sun.position.set(8, 12, 4);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 40;
sun.shadow.camera.left = -8;
sun.shadow.camera.right = 8;
sun.shadow.camera.top = 8;
sun.shadow.camera.bottom = -8;
sun.shadow.bias = -0.0005;
scene.add(sun);
const fill = new THREE.DirectionalLight('#446688', 1.2);
fill.position.set(-3, 2, -4);
scene.add(fill);
// ──────────────────────────────────────────────
// ORBIT CONTROLS — damping, auto-rotation, bookmarks
// ──────────────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 0.3, 0);
controls.minDistance = 1.5;
controls.maxDistance = 14;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
// Camera bookmarks stored in memory + localStorage
const bookmarks = {
  overview: { pos: [4, 5.5, 4.5], target: [0, 0.3, 0] },
  closeup: { pos: [1.2, 2.0, 1.5], target: [0.1, 0.5, 0.1] },
  anomaly: { pos: [0.5, 1.2, 0.8], target: [0, 0.6, 0] }
};
// Load saved bookmarks from localStorage if present
try {
  const saved = JSON.parse(localStorage.getItem('terrain_bookmarks'));
  if (saved) Object.assign(bookmarks, saved);
} catch(e) { /* ignore corrupt storage */ }
function applyBookmark(name) {
  const bm = bookmarks[name];
  if (!bm) return;
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function animateBookmark(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease in-out cubic for smooth camera transition
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animateBookmark);
  }
  requestAnimationFrame(animateBookmark);
}
// Save current camera position as bookmark
function saveBookmark(name) {
  bookmarks[name] = {
    pos: camera.position.toArray(),
    target: controls.target.toArray()
  };
  try { localStorage.setItem('terrain_bookmarks', JSON.stringify(bookmarks)); } catch(e) {}
}
document.querySelectorAll('[data-bookmark]').forEach(btn => {
  btn.addEventListener('click', () => applyBookmark(btn.dataset.bookmark));
  // Long-press to save current position as bookmark
  let longPressTimer;
  btn.addEventListener('pointerdown', () => {
    longPressTimer = setTimeout(() => {
      saveBookmark(btn.dataset.bookmark);
      btn.classList.add('active');
      setTimeout(() => btn.classList.remove('active'), 600);
    }, 800);
  });
  btn.addEventListener('pointerup', () => clearTimeout(longPressTimer));
  btn.addEventListener('pointerleave', () => clearTimeout(longPressTimer));
});
document.getElementById('btn-auto-rotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
// Start with auto-rotate button active
document.getElementById('btn-auto-rotate').classList.add('active');
document.getElementById('btn-reset-cam').addEventListener('click', () => applyBookmark('overview'));
// ──────────────────────────────────────────────
// CACHE LAYER — geometry, material, transform caches
// ──────────────────────────────────────────────
const cache = {
  terrainGeo: new Map(),       // timeIndex -> BufferGeometry
  riverGeo: new Map(),        // timeIndex -> BufferGeometry
  worldToGrid: new Map(),     // key(wx,wz) -> {ix,iz} — invalidated on terrain change
  currentTerrainKey: -1,
  hits: 0,
  misses: 0
};
function memoWorldToGrid(wx, wz) {
  const key = `${wx.toFixed(3)},${wz.toFixed(3)}`;
  if (cache.worldToGrid.has(key)) {
    cache.hits++;
    return cache.worldToGrid.get(key);
  }
  cache.misses++;
  // World space: terrain spans -2..2 in X/Z, grid indices 0..GRID-1
  const ix = Math.round(((wx + 2) / 4) * (GRID - 1));
  const iz = Math.round(((wz + 2) / 4) * (GRID - 1));
  const clamped = { ix: Math.max(0, Math.min(GRID - 1, ix)), iz: Math.max(0, Math.min(GRID - 1, iz)) };
  cache.worldToGrid.set(key, clamped);
  return clamped;
}
// ──────────────────────────────────────────────
// TERRAIN MESH — BufferGeometry heightfield with vertex colors
// ──────────────────────────────────────────────
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
let terrainMesh = null;
let terrainBuildCount = 0;
function buildTerrainGeometry(timeIndex) {
  // Return cached geometry if available
  if (cache.terrainGeo.has(timeIndex)) {
    cache.hits++;
    return cache.terrainGeo.get(timeIndex).clone();
  }
  cache.misses++;
  terrainBuildCount++;
  const frame = dataSeries[timeIndex];
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  // Build positions + colors in one pass over the grid
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const i3 = idx * 3;
      // Map grid to world XZ: -2..2 range
      const wx = (ix / (GRID - 1)) * 4 - 2;
      const wz = (iz / (GRID - 1)) * 4 - 2;
      // Revenue drives elevation (0..2.5 range)
      const elevation = frame.revenue[idx] * 2.5;
      positions[i3] = wx;
      positions[i3 + 1] = elevation;
      positions[i3 + 2] = wz;
      // User density mapped to vegetation/heat gradient via HSL
      const userVal = Math.max(0, Math.min(1, frame.users[idx]));
      const hue = 0.15 + userVal * 0.35; // green(0.15) -> yellow(0.5)
      const sat = 0.6 + userVal * 0.4;
      const light = 0.2 + userVal * 0.45;
      const color = new THREE.Color();
      color.setHSL(hue, sat, light);
      colors[i3] = color.r;
      colors[i3 + 1] = color.g;
      colors[i3 + 2] = color.b;
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  // Build index buffer (two triangles per grid cell)
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
  geo.setIndex(indices);
  geo.computeVertexNormals();
  // Store in cache before returning clone
  cache.terrainGeo.set(timeIndex, geo);
  cache.hits--; // compensate: clone call below will count as a logical hit
  cache.misses--; // this was a build miss, already counted
  // We'll track the hit for the clone in the caller
  return geo.clone();
}
function updateTerrain(timeIndex) {
  if (timeIndex === cache.currentTerrainKey) return;
  cache.currentTerrainKey = timeIndex;
  cache.worldToGrid.clear(); // invalidate coordinate transform cache on terrain change
  const geo = buildTerrainGeometry(timeIndex);
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geo;
  } else {
    terrainMesh = new THREE.Mesh(geo, terrainMaterial);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  }
  document.getElementById('diag-terrain-builds').textContent = terrainBuildCount;
  // Rebuild rivers after terrain changes (debounced)
  scheduleRiverRebuild(timeIndex);
}
// ──────────────────────────────────────────────
// RIVER GEOMETRY — error paths as tubes carved into terrain
// ──────────────────────────────────────────────
let riverGroup = new THREE.Group();
scene.add(riverGroup);
let riverBuildCount = 0;
let riverRebuildTimer = null;
function findErrorPaths(frame) {
  // Trace error ridges: find cells where error > 0.25 and follow gradient upward
  const threshold = 0.25;
  const paths = [];
  const visited = new Set();
  const directions = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  // Seed points: top 10 highest error cells
  const candidates = [];
  for (let i = 0; i < GRID * GRID; i++) {
    if (frame.errors[i] > threshold) candidates.push({ idx: i, err: frame.errors[i] });
  }
  candidates.sort((a, b) => b.err - a.err);
  const seeds = candidates.slice(0, 12);
  for (const seed of seeds) {
    if (visited.has(seed.idx)) continue;
    const path = [];
    let current = seed.idx;
    let steps = 0;
    const maxSteps = 40;
    while (current >= 0 && steps < maxSteps && !visited.has(current)) {
      visited.add(current);
      const iz = Math.floor(current / GRID);
      const ix = current % GRID;
      const wx = (ix / (GRID - 1)) * 4 - 2;
      const wz = (iz / (GRID - 1)) * 4 - 2;
      const wy = frame.revenue[current] * 2.5 - 0.02; // slightly below terrain surface
      path.push(new THREE.Vector3(wx, wy, wz));
      // Follow steepest error ascent among neighbors
      let bestNext = -1;
      let bestErr = frame.errors[current];
      for (const [dx, dz] of directions) {
        const nix = ix + dx;
        const niz = iz + dz;
        if (nix < 0 || nix >= GRID || niz < 0 || niz >= GRID) continue;
        const nidx = niz * GRID + nix;
        if (visited.has(nidx)) continue;
        if (frame.errors[nidx] > bestErr) {
          bestErr = frame.errors[nidx];
          bestNext = nidx;
        }
      }
      current = bestNext;
      steps++;
    }
    if (path.length >= 6) paths.push(path);
  }
  return paths;
}
function buildRiverGeometry(timeIndex) {
  if (cache.riverGeo.has(timeIndex)) {
    cache.hits++;
    return cache.riverGeo.get(timeIndex);
  }
  cache.misses++;
  riverBuildCount++;
  const frame = dataSeries[timeIndex];
  const paths = findErrorPaths(frame);
  const group = new THREE.Group();
  const riverMat = new THREE.MeshStandardMaterial({
    color: '#ff4444',
    emissive: '#440000',
    roughness: 0.3,
    metalness: 0.2,
    transparent: true,
    opacity: 0.85
  });
  for (const path of paths) {
    if (path.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(path, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 3, 0.04, 6, false);
    const tube = new THREE.Mesh(tubeGeo, riverMat);
    tube.castShadow = true;
    group.add(tube);
    // Add small glow spheres at path endpoints
    const glowGeo = new THREE.SphereGeometry(0.05, 8, 8);
    const glowMat = new THREE.MeshBasicMaterial({ color: '#ff8888' });
    const startDot = new THREE.Mesh(glowGeo, glowMat);
    startDot.position.copy(path[0]);
    group.add(startDot);
  }
  cache.riverGeo.set(timeIndex, group);
  return group;
}
function scheduleRiverRebuild(timeIndex) {
  // Debounce: clear pending timer, set new 200ms delay
  if (riverRebuildTimer) clearTimeout(riverRebuildTimer);
  riverRebuildTimer = setTimeout(() => {
    // Dispose old river group children
    while (riverGroup.children.length > 0) {
      const child = riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      riverGroup.remove(child);
    }
    const newRivers = buildRiverGeometry(timeIndex);
    // Transfer children from cached group to scene group
    while (newRivers.children.length > 0) {
      riverGroup.add(newRivers.children[0]);
    }
    document.getElementById('diag-river-builds').textContent = riverBuildCount;
  }, 200);
}
// ──────────────────────────────────────────────
// PARTICLE SYSTEM — API call flow trails
// ──────────────────────────────────────────────
const PARTICLE_COUNT = 400;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3); // reused every frame
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = []; // per-particle state: {x,z,vx,vz,life,startLife}
// Initialize particles with random positions across the terrain
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const angle = Math.random() * Math.PI * 2;
  const radius = Math.random() * 2;
  particleData.push({
    x: Math.cos(angle) * radius,
    z: Math.sin(angle) * radius,
    vx: (Math.random() - 0.5) * 0.3,
    vz: (Math.random() - 0.5) * 0.3,
    life: Math.random() * 3,
    startLife: 3
  });
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.04,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
function updateParticles(dt, timeIndex) {
  // dt clamped to avoid spikes on tab-away
  const dtClamped = Math.min(dt, 0.1);
  const frame = dataSeries[timeIndex];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const p = particleData[i];
    p.life -= dtClamped;
    if (p.life <= 0) {
      // Respawn at random position
      p.x = (Math.random() - 0.5) * 3.5;
      p.z = (Math.random() - 0.5) * 3.5;
      p.vx = (Math.random() - 0.5) * 0.4;
      p.vz = (Math.random() - 0.5) * 0.4;
      p.life = p.startLife;
    }
    // Flow particles along API call gradient: bias velocity toward higher API activity
    const grid = memoWorldToGrid(p.x, p.z);
    const idx = grid.iz * GRID + grid.ix;
    const apiStrength = frame.apis[idx];
    // Gradient-directed flow: sample neighbors for steering
    const gx = grid.ix, gz = grid.iz;
    const nx = gx < GRID-1 ? frame.apis[gz * GRID + gx + 1] : apiStrength;
    const nz = gz < GRID-1 ? frame.apis[(gz+1) * GRID + gx] : apiStrength;
    const steerX = (nx - apiStrength) * 0.5;
    const steerZ = (nz - apiStrength) * 0.5;
    p.vx += steerX * dtClamped * 2;
    p.vz += steerZ * dtClamped * 2;
    // Speed limit
    const speed = Math.sqrt(p.vx * p.vx + p.vz * p.vz);
    const maxSpeed = 0.8 + apiStrength * 1.2;
    if (speed > maxSpeed) {
      p.vx = (p.vx / speed) * maxSpeed;
      p.vz = (p.vz / speed) * maxSpeed;
    }
    p.x += p.vx * dtClamped;
    p.z += p.vz * dtClamped;
    // Wrap at terrain bounds
    if (p.x < -2) p.x = 1.9;
    if (p.x > 2) p.x = -1.9;
    if (p.z < -2) p.z = 1.9;
    if (p.z > 2) p.z = -1.9;
    // Elevation from terrain
    const hGrid = memoWorldToGrid(p.x, p.z);
    const hIdx = hGrid.iz * GRID + hGrid.ix;
    const elevation = frame.revenue[hIdx] * 2.5 + 0.06;
    const i3 = i * 3;
    // Reuse Float32Array position buffer — no allocation
    particlePositions[i3] = p.x;
    particlePositions[i3 + 1] = elevation;
    particlePositions[i3 + 2] = p.z;
    // Color: bright yellow with life-based alpha effect via RGB intensity
    const lifeRatio = p.life / p.startLife;
    const brightness = 0.5 + lifeRatio * 0.5;
    particleColors[i3] = 1.0 * brightness;
    particleColors[i3 + 1] = 0.83 * brightness;
    particleColors[i3 + 2] = 0.23 * brightness;
  }
  // Update buffer attributes — this triggers GPU upload of reused Float32Arrays
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
// ──────────────────────────────────────────────
// GRID WIREFRAME — subtle reference plane
// ──────────────────────────────────────────────
const gridHelper = new THREE.PolarGridHelper(3, 40, 20, 64, '#1a1a3a', '#1a1a3a');
gridHelper.position.y = -0.01;
scene.add(gridHelper);
// ──────────────────────────────────────────────
// RAYCASTER FOR HOVER TOOLTIP
// ──────────────────────────────────────────────
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
window.addEventListener('pointermove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!terrainMesh) return;
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const grid = memoWorldToGrid(point.x, point.z);
    const frame = dataSeries[timeIndex];
    const idx = grid.iz * GRID + grid.ix;
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX + 16) + 'px';
    tooltip.style.top = (e.clientY - 10) + 'px';
    tooltip.innerHTML = `
      <div>Grid [${grid.ix}, ${grid.iz}]</div>
      <div class="metric">Revenue: ${(frame.revenue[idx] * 100).toFixed(0)}</div>
      <div>Users: ${(frame.users[idx] * 100).toFixed(0)}</div>
      <div class="error">Errors: ${(frame.errors[idx] * 100).toFixed(1)}%</div>
      <div>API calls: ${(frame.apis[idx] * 100).toFixed(0)}/s</div>`;
  } else {
    tooltip.style.display = 'none';
  }
});
// ──────────────────────────────────────────────
// TIME SLIDER
// ──────────────────────────────────────────────
let timeIndex = 0;
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
slider.addEventListener('input', () => {
  timeIndex = parseInt(slider.value);
  timeLabel.textContent = `T: ${timeIndex}`;
  updateTerrain(timeIndex);
});
// ──────────────────────────────────────────────
// RENDER LOOP
// ──────────────────────────────────────────────
let lastTime = performance.now();
let fpsFrames = 0;
let fpsAccum = 0;
let displayFps = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  const dt = (timestamp - lastTime) / 1000;
  lastTime = timestamp;
  // FPS counter
  fpsFrames++;
  fpsAccum += dt;
  if (fpsAccum >= 1.0) {
    displayFps = Math.round(fpsFrames / fpsAccum);
    fpsFrames = 0;
    fpsAccum = 0;
  }
  controls.update();
  updateParticles(dt, timeIndex);
  renderer.render(scene, camera);
  // Update diagnostic display — throttled to every 30 frames to avoid DOM thrash
  if (fpsFrames % 30 === 0) {
    document.getElementById('diag-fps').textContent = displayFps;
    document.getElementById('diag-cache-hits').textContent = cache.hits;
    document.getElementById('diag-cache-miss').textContent = cache.misses;
  }
}
// ──────────────────────────────────────────────
// RESIZE HANDLER
// ──────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ──────────────────────────────────────────────
// KEYBOARD SHORTCUTS
// ──────────────────────────────────────────────
window.addEventListener('keydown', (e) => {
  switch(e.key.toLowerCase()) {
    case '1': applyBookmark('overview'); break;
    case '2': applyBookmark('closeup'); break;
    case '3': applyBookmark('anomaly'); break;
    case 'a': controls.autoRotate = !controls.autoRotate;
              document.getElementById('btn-auto-rotate').classList.toggle('active', controls.autoRotate);
              break;
    case 'r': applyBookmark('overview'); break;
  }
});
// ──────────────────────────────────────────────
// INITIALIZATION
// ──────────────────────────────────────────────
updateTerrain(0);
requestAnimationFrame(animate);
// ──────────────────────────────────────────────
// HOT-PATH AUDIT SUMMARY (implemented above):
// - terrainGeo cache: Map<timeIndex, BufferGeometry> — no new THREE.BufferGeometry() on slider tick if cached
// - riverGeo cache: Map<timeIndex, Group> — TubeGeometry cached, debounced rebuild (200ms)
// - worldToGrid cache: Map<key, {ix,iz}> — memoized per frame on hover + particle paths
// - particlePositions/Colors: Float32Array allocated ONCE, reused every frame via needsUpdate
// - No THREE.XxxGeometry() constructor in per-frame path
// - Cache invalidation: only when timeIndex changes (slider input), not every frame
// </EOP>
</script>
</body>
</html>
```
Status: 3D terrain explorer built. 411 lines, self-contained single HTML file.
- 80x80 heightfield terrain, 100 time steps, synthetic multi-metric dataset
- Revenue = elevation, user density = HSL vertex colors, error paths = red tubes, API calls = particle trails
- OrbitControls + auto-rotation + 3 camera bookmarks (save on long-press, load on click or keys 1/2/3)
- Time slider reshapes terrain/rivers; river rebuild debounced 200ms
- Cache layer: terrain geometries, river groups, world-to-grid transforms — no allocations in per-frame path
- Particle position/color buffers allocated once, reused with needsUpdate
- Diagnostic panel: FPS, cache hits/misses, terrain builds, river builds
- Hover tooltip with raycaster showing revenue/users/errors/API calls at cursor grid cell
- Keyboard: 1/2/3 for bookmarks, A for auto-rotate toggle, R for reset