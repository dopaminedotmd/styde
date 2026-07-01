<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{overflow:hidden;background:#0a0a14;font-family:'Segoe UI',system-ui,sans-serif}
  canvas{display:block}
  #panel{position:fixed;top:12px;left:12px;background:rgba(10,10,26,0.88);border:1px solid rgba(255,255,255,0.12);border-radius:10px;padding:16px;color:#c8c8e0;min-width:220px;backdrop-filter:blur(12px);z-index:10}
  #panel h3{font-size:14px;font-weight:600;margin-bottom:10px;color:#e0e0f8;letter-spacing:0.03em}
  #panel label{font-size:11px;display:block;margin:6px 0 3px;color:#9898b8}
  #panel input[type=range]{width:100%;accent-color:#6c9cff}
  #panel button{background:rgba(108,156,255,0.15);border:1px solid rgba(108,156,255,0.35);color:#b8c8f8;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:11px;margin:4px 2px;transition:all 0.2s}
  #panel button:hover{background:rgba(108,156,255,0.28);border-color:rgba(108,156,255,0.6)}
  #panel button.active{background:rgba(108,156,255,0.4);border-color:#6c9cff;color:#fff}
  #time-label{font-size:12px;text-align:center;margin:4px 0;color:#aab8d8}
  #diag{position:fixed;bottom:12px;right:12px;background:rgba(10,10,26,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:10px 14px;color:#78a878;font-size:10px;font-family:monospace;z-index:10;backdrop-filter:blur(8px)}
  .bookmark-row{display:flex;gap:4px;margin-top:2px}
  .bookmark-row button{flex:1;font-size:10px}
</style>
</head>
<body>
<div id="panel">
  <h3>Terrain Explorer</h3>
  <label>Time Step</label>
  <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
  <div id="time-label">t = 0</div>
  <label>Auto-Rotate</label>
  <input type="range" id="auto-speed" min="0" max="100" value="30" step="1">
  <div style="margin-top:8px;font-size:10px;color:#8888a8">Bookmarks</div>
  <div class="bookmark-row">
    <button onclick="saveBookmark()">Save</button>
    <button onclick="restoreBookmark(0)">1</button>
    <button onclick="restoreBookmark(1)">2</button>
    <button onclick="restoreBookmark(2)">3</button>
  </div>
</div>
<div id="diag">
  <div>Cache hits: <span id="ch">0</span> / misses: <span id="cm">0</span></div>
  <div>FPS: <span id="fps">60</span> | Tris: <span id="tris">0</span></div>
  <div>Coord valid: <span id="cv">yes</span></div>
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
// ---- DATA GENERATION: mixed real+synthetic time-series ----
const GRID = 64;
const TIME_STEPS = 100;
const realDataRatio = 0.5; // 50% real-pattern, 50% synthetic — config.yaml driven
const realDataSource = 'simulated-usgs-elevation-tiles'; // config.yaml: realdatasource
// Synthetic base: layered sine/cosine to simulate terrain patterns
function synthHeight(x, z, t) {
  const fx = x / GRID, fz = z / GRID, ft = t / TIME_STEPS;
  return Math.sin(fx * 5.3 + ft * 2.1) * Math.cos(fz * 4.7 - ft * 1.3) * 1.8
       + Math.sin(fx * 8.1) * Math.cos(fz * 7.3 + ft * 0.9) * 0.7
       + Math.cos(fx * 2.3 + fz * 2.9) * Math.sin(ft * 3.5) * 1.2;
}
// Real-pattern simulator: ridge lines, basins, plateaus mimicking real terrain
function realHeight(x, z, t) {
  const fx = x / GRID, fz = z / GRID, ft = t / TIME_STEPS;
  // Ridge at z=0.4 that grows over time
  const ridge = Math.exp(-Math.pow((fz - 0.4) * 6, 2)) * (2.2 + ft * 0.8);
  // Basin at (0.6, 0.6) that deepens
  const basin = -Math.exp(-(Math.pow((fx - 0.65) * 5, 2) + Math.pow((fz - 0.6) * 5, 2))) * 1.6 * (1 + ft * 0.4);
  // Plateau in corner
  const plateau = 1.0 / (1 + Math.exp(-(fx - 0.75) * 8)) * 1.0 / (1 + Math.exp(-(fz - 0.75) * 8)) * 1.4;
  return ridge + basin + plateau + Math.sin(fx * 10 + fz * 8) * 0.15;
}
// Blended heightfield
function getHeight(x, z, t) {
  const s = synthHeight(x, z, t);
  const r = realHeight(x, z, t);
  return s * (1 - realDataRatio) + r * realDataRatio;
}
// Secondary metric: vegetation / user-density (0-1)
function getVeg(x, z, t) {
  const ft = t / TIME_STEPS;
  return THREE.MathUtils.clamp(
    0.35 + Math.sin(x / GRID * 6.2 + ft * 1.7) * 0.25 + Math.cos(z / GRID * 5.1 - ft) * 0.2
    + (1 - Math.abs(getHeight(x, z, t)) / 3.5) * 0.3,
    0, 1
  );
}
// Error / anomaly detection: where gradient exceeds threshold
function isError(x, z, t) {
  if (x < 1 || x >= GRID - 1 || z < 1 || z >= GRID - 1) return false;
  const h = getHeight(x, z, t);
  const gx = getHeight(x + 1, z, t) - h;
  const gz = getHeight(x, z + 1, t) - h;
  return Math.sqrt(gx * gx + gz * gz) > 0.18;
}
// Error river path: trace contiguous error cells
function traceRivers(t) {
  const visited = new Uint8Array(GRID * GRID);
  const rivers = [];
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      const idx = z * GRID + x;
      if (visited[idx] || !isError(x, z, t)) continue;
      // BFS to collect contiguous error cluster
      const cluster = [];
      const queue = [[x, z]];
      visited[idx] = 1;
      while (queue.length > 0) {
        const [cx, cz] = queue.shift();
        cluster.push([cx, cz]);
        for (const [dx, dz] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nx = cx + dx, nz = cz + dz;
          if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
          const ni = nz * GRID + nx;
          if (!visited[ni] && isError(nx, nz, t)) {
            visited[ni] = 1;
            queue.push([nx, nz]);
          }
        }
      }
      // Convert cluster to centerline via thinning: take every 3rd point sorted by x+z
      cluster.sort((a, b) => (a[0] + a[1]) - (b[0] + b[1]));
      const path = [];
      for (let i = 0; i < cluster.length; i += Math.max(1, Math.floor(cluster.length / 12))) {
        path.push(cluster[i]);
      }
      if (path.length >= 3) rivers.push(path);
    }
  }
  return rivers;
}
// ---- COORDINATE VALIDATION ----
function validateCoordinate(ix, iz) {
  if (ix < 0 || ix >= GRID || iz < 0 || iz >= GRID) return false;
  if (!Number.isFinite(ix) || !Number.isFinite(iz)) return false;
  return true;
}
function worldToGrid(wx, wz, gridMin, gridMax) {
  const ix = Math.round(((wx - gridMin) / (gridMax - gridMin)) * (GRID - 1));
  const iz = Math.round(((wz - gridMin) / (gridMax - gridMin)) * (GRID - 1));
  return { ix: THREE.MathUtils.clamp(ix, 0, GRID - 1), iz: THREE.MathUtils.clamp(iz, 0, GRID - 1) };
}
// ---- CACHE SYSTEM ----
const cache = {
  heightfields: new Map(),  // key: t -> Float32Array[GRID*GRID]
  vegMaps: new Map(),
  riverPaths: new Map(),
  riverGeometries: new Map(),
  terrainGeometries: new Map(),
  gridToWorld: null,       // memoized
  hits: 0,
  misses: 0,
};
function cacheGet(map, key) {
  if (map.has(key)) { cache.hits++; return map.get(key); }
  cache.misses++;
  return null;
}
function cacheSet(map, key, value) {
  map.set(key, value);
  if (map.size > 128) {
    const firstKey = map.keys().next().value;
    map.delete(firstKey);
  }
}
// ---- THREE.JS SETUP ----
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 6, 25);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.3, 60);
camera.position.set(6.5, 5.2, 8.3);
camera.lookAt(3.2, 0.8, 3.2);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
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
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(GRID / 2 * 0.1, 0.5, GRID / 2 * 0.1);
controls.minDistance = 1.5;
controls.maxDistance = 15;
controls.maxPolarAngle = Math.PI * 0.78;
controls.update();
// Bookmarks storage
const bookmarks = [];
// Lighting
const ambient = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
sun.position.set(8, 12, 4);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 40;
sun.shadow.camera.left = -10;
sun.shadow.camera.right = 10;
sun.shadow.camera.top = 10;
sun.shadow.camera.bottom = -10;
sun.shadow.bias = -0.0004;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 1.5);
fill.position.set(-3, 2, -4);
scene.add(fill);
// Base grid plane
const gridHelper = new THREE.PolarGridHelper(5, 32, 24, 64, 0x334466, 0x223355);
gridHelper.position.set(GRID / 2 * 0.1, -0.05, GRID / 2 * 0.1);
scene.add(gridHelper);
// ---- TERRAIN GEOMETRY CONSTRUCTION (called on time change) ----
let terrainMesh = null;
let riverGroup = null;
let particlesMesh = null;
let currentTime = 0;
const GRID_SPACING = 0.1;
function buildHeightfieldArray(t) {
  let data = cacheGet(cache.heightfields, t);
  if (data) return data;
  data = new Float32Array(GRID * GRID);
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      data[z * GRID + x] = getHeight(x, z, t);
    }
  }
  cacheSet(cache.heightfields, t, data);
  return data;
}
function buildVegArray(t) {
  let data = cacheGet(cache.vegMaps, t);
  if (data) return data;
  data = new Float32Array(GRID * GRID);
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      data[z * GRID + x] = getVeg(x, z, t);
    }
  }
  cacheSet(cache.vegMaps, t, data);
  return data;
}
function buildTerrainGeometry(t) {
  let geom = cacheGet(cache.terrainGeometries, t);
  if (geom) return geom;
  const heights = buildHeightfieldArray(t);
  const veg = buildVegArray(t);
  const segments = GRID - 1;
  geom = new THREE.BufferGeometry();
  // Pre-allocate arrays — single allocation, no per-frame churn
  const pos = new Float32Array(GRID * GRID * 3);
  const col = new Float32Array(GRID * GRID * 3);
  const idx = new Uint32Array(segments * segments * 6);
  // Build position + color arrays
  for (let z = 0; z < GRID; z++) {
    for (let x = 0; x < GRID; x++) {
      const i = (z * GRID + x) * 3;
      pos[i] = x * GRID_SPACING;
      pos[i + 1] = heights[z * GRID + x];
      pos[i + 2] = z * GRID_SPACING;
      // Vegetation gradient: green (low density, high veg) to brown (barren)
      const v = veg[z * GRID + x];
      const h = heights[z * GRID + x];
      const hNorm = (h + 2) / 4; // normalize roughly -2..2 to 0..1
      // Blend: high veg = green, low veg = brown/yellow; high elevation = snow white tint
      const r = THREE.MathUtils.lerp(0.22, 0.18, v) + hNorm * 0.4;
      const g = THREE.MathUtils.lerp(0.18, 0.52, v) + hNorm * 0.35;
      const b = THREE.MathUtils.lerp(0.12, 0.18, v) + hNorm * 0.25;
      col[i] = THREE.MathUtils.clamp(r, 0, 1);
      col[i + 1] = THREE.MathUtils.clamp(g, 0, 1);
      col[i + 2] = THREE.MathUtils.clamp(b, 0, 1);
    }
  }
  // Build index array
  let ii = 0;
  for (let z = 0; z < segments; z++) {
    for (let x = 0; x < segments; x++) {
      const a = z * GRID + x;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      idx[ii++] = a; idx[ii++] = c; idx[ii++] = b;
      idx[ii++] = b; idx[ii++] = c; idx[ii++] = d;
    }
  }
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(col, 3));
  geom.setIndex(new THREE.BufferAttribute(idx, 1));
  geom.computeVertexNormals();
  cacheSet(cache.terrainGeometries, t, geom);
  return geom;
}
// ---- RIVER GEOMETRY (cached, debounced) ----
let riverRebuildTimeout = null;
let pendingRiverTime = -1;
function buildRiverGroup(t) {
  const key = `river_${t}`;
  let group = cacheGet(cache.riverGeometries, key);
  if (group) return group;
  const paths = traceRivers(t);
  group = new THREE.Group();
  paths.forEach((path) => {
    if (path.length < 3) return;
    const pts = path.map(([x, z]) => {
      const h = getHeight(x, z, t) + 0.03;
      return new THREE.Vector3(x * GRID_SPACING, h, z * GRID_SPACING);
    });
    const curve = new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.5);
    const tubeGeom = new THREE.TubeGeometry(curve, Math.min(path.length * 2, 40), 0.04, 6, false);
    const mat = new THREE.MeshStandardMaterial({
      color: 0xcc3322,
      emissive: 0x441111,
      roughness: 0.3,
      metalness: 0.1,
    });
    const tube = new THREE.Mesh(tubeGeom, mat);
    tube.castShadow = true;
    group.add(tube);
  });
  cacheSet(cache.riverGeometries, key, group);
  return group;
}
// Debounced river rebuild — avoids per-tick TubeGeometry construction
function scheduleRiverRebuild(t) {
  pendingRiverTime = t;
  if (riverRebuildTimeout) return;
  riverRebuildTimeout = setTimeout(() => {
    riverRebuildTimeout = null;
    rebuildRivers(pendingRiverTime);
    pendingRiverTime = -1;
  }, 200);
}
function rebuildRivers(t) {
  if (riverGroup) {
    // Dispose old river meshes' geometries (materials kept simple, let GC handle)
    riverGroup.traverse((child) => {
      if (child.geometry && child !== riverGroup) child.geometry.dispose();
    });
    scene.remove(riverGroup);
  }
  riverGroup = buildRiverGroup(t);
  scene.add(riverGroup);
}
// ---- PARTICLE SYSTEM (reuses position array, no per-frame allocations) ----
const PARTICLE_COUNT = 800;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3); // direction cache
function initParticles() {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    resetParticle(i, currentTime);
    // Randomize initial position age so trails are spread
    for (let step = 0; step < Math.floor(Math.random() * 30); step++) {
      advanceParticle(i, currentTime);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.06,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.75,
  });
  particlesMesh = new THREE.Points(geom, mat);
  scene.add(particlesMesh);
}
function resetParticle(i, t) {
  const x = Math.random() * (GRID - 1);
  const z = Math.random() * (GRID - 1);
  const h = getHeight(x, z, t);
  particlePositions[i * 3] = x * GRID_SPACING;
  particlePositions[i * 3 + 1] = h + 0.08;
  particlePositions[i * 3 + 2] = z * GRID_SPACING;
  // Random flow direction
  const angle = Math.random() * Math.PI * 2;
  particleVelocities[i * 3] = Math.cos(angle) * 0.015;
  particleVelocities[i * 3 + 1] = (Math.random() - 0.5) * 0.005;
  particleVelocities[i * 3 + 2] = Math.sin(angle) * 0.015;
  // Color: warm gold to cyan based on velocity magnitude
  const speed = 0.5 + Math.random() * 0.5;
  particleColors[i * 3] = 0.9 * speed;
  particleColors[i * 3 + 1] = 0.7 * (1 - speed);
  particleColors[i * 3 + 2] = 1.0 - speed * 0.8;
}
function advanceParticle(i, t) {
  const i3 = i * 3;
  // Gravity-like: drift toward lower terrain
  const px = particlePositions[i3];
  const pz = particlePositions[i3 + 2];
  const gx = px / GRID_SPACING;
  const gz = pz / GRID_SPACING;
  if (!validateCoordinate(Math.round(gx), Math.round(gz))) {
    resetParticle(i, t);
    return;
  }
  // Terrain gradient steering
  const hCenter = getHeight(gx, gz, t);
  const hRight = getHeight(Math.min(gx + 0.2, GRID - 1), gz, t);
  const hDown = getHeight(gx, Math.min(gz + 0.2, GRID - 1), t);
  const gradX = (hRight - hCenter) * 0.03;
  const gradZ = (hDown - hCenter) * 0.03;
  particleVelocities[i3] -= gradX;
  particleVelocities[i3 + 2] -= gradZ;
  // Damping
  particleVelocities[i3] *= 0.98;
  particleVelocities[i3 + 2] *= 0.98;
  particlePositions[i3] += particleVelocities[i3];
  particlePositions[i3 + 2] += particleVelocities[i3 + 2];
  // Bounds check
  if (particlePositions[i3] < 0 || particlePositions[i3] > (GRID - 1) * GRID_SPACING ||
      particlePositions[i3 + 2] < 0 || particlePositions[i3 + 2] > (GRID - 1) * GRID_SPACING) {
    resetParticle(i, t);
  }
  // Recompute height at new position
  const nx = particlePositions[i3] / GRID_SPACING;
  const nz = particlePositions[i3 + 2] / GRID_SPACING;
  particlePositions[i3 + 1] = getHeight(nx, nz, t) + 0.08;
}
// ---- TIME CHANGE HANDLER ----
function setTime(t) {
  if (t === currentTime) return;
  currentTime = t;
  // Swap terrain geometry (cached)
  const newGeom = buildTerrainGeometry(t);
  if (terrainMesh) {
    terrainMesh.geometry.dispose(); // dispose old — new was from cache
    terrainMesh.geometry = newGeom;
  } else {
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.65,
      metalness: 0.05,
      flatShading: false,
    });
    terrainMesh = new THREE.Mesh(newGeom, mat);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  }
  // Schedule debounced river rebuild
  scheduleRiverRebuild(t);
  // Update particle positions to new terrain height
  if (particlesMesh) {
    const posArr = particlesMesh.geometry.attributes.position.array;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const i3 = i * 3;
      const nx = posArr[i3] / GRID_SPACING;
      const nz = posArr[i3 + 2] / GRID_SPACING;
      posArr[i3 + 1] = getHeight(nx, nz, t) + 0.08;
    }
    particlesMesh.geometry.attributes.position.needsUpdate = true;
  }
  document.getElementById('time-label').textContent = `t = ${t}`;
}
// ---- DIAGNOSTICS UPDATE ----
let frameCount = 0;
let lastFpsTime = performance.now();
let currentFps = 60;
function updateDiagnostics() {
  frameCount++;
  const now = performance.now();
  if (now - lastFpsTime >= 1000) {
    currentFps = Math.round(frameCount / ((now - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = now;
  }
  document.getElementById('ch').textContent = cache.hits;
  document.getElementById('cm').textContent = cache.misses;
  document.getElementById('fps').textContent = currentFps;
  const tris = terrainMesh ? terrainMesh.geometry.index.count / 3 : 0;
  document.getElementById('tris').textContent = Math.round(tris);
  // Coordinate spot-check
  const testGx = Math.round(GRID / 2), testGz = Math.round(GRID / 2);
  document.getElementById('cv').textContent = validateCoordinate(testGx, testGz) ? 'yes' : 'NO';
}
// ---- BOOKMARK SYSTEM ----
window.saveBookmark = function() {
  if (bookmarks.length >= 3) bookmarks.shift();
  bookmarks.push({
    position: camera.position.clone(),
    target: controls.target.clone(),
    time: currentTime,
  });
  // Visual feedback
  const btns = document.querySelectorAll('.bookmark-row button');
  const idx = bookmarks.length;
  if (btns[idx]) btns[idx].classList.add('active');
};
window.restoreBookmark = function(index) {
  if (index >= bookmarks.length) return;
  const bm = bookmarks[index];
  // Animate camera to bookmark
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.position;
  const endTarget = bm.target;
  const startTime = performance.now();
  const duration = 800; // ms
  function animateCam(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease in-out
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1.0) {
      requestAnimationFrame(animateCam);
    }
  }
  requestAnimationFrame(animateCam);
  if (bm.time !== currentTime) {
    setTime(bm.time);
    document.getElementById('time-slider').value = bm.time;
  }
};
// ---- EVENT HANDLERS ----
document.getElementById('time-slider').addEventListener('input', (e) => {
  setTime(parseInt(e.target.value));
});
document.getElementById('auto-speed').addEventListener('input', (e) => {
  controls.autoRotateSpeed = parseInt(e.target.value) / 100;
  controls.autoRotate = controls.autoRotateSpeed > 0.01;
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      break;
    case 'f':
      // Reset view
      camera.position.set(6.5, 5.2, 8.3);
      controls.target.set(GRID / 2 * 0.1, 0.5, GRID / 2 * 0.1);
      controls.update();
      break;
    case '1': restoreBookmark(0); break;
    case '2': restoreBookmark(1); break;
    case '3': restoreBookmark(2); break;
  }
});
// ---- RENDER LOOP ----
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  // Update particles — reuse position array directly
  if (particlesMesh) {
    const posArr = particlesMesh.geometry.attributes.position.array;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      advanceParticle(i, currentTime);
    }
    // Copy back from our cached arrays
    posArr.set(particlePositions);
    particlesMesh.geometry.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
  updateDiagnostics();
}
// ---- INITIALIZATION ----
// Grid-to-world memoized transform
cache.gridToWorld = {
  min: 0,
  max: (GRID - 1) * GRID_SPACING,
  spacing: GRID_SPACING,
};
setTime(0);
initParticles();
rebuildRivers(0);
requestAnimationFrame(animate);
</script>
</body>
</html>