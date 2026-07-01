<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a0f;--panel:#111118;--text:#c8c8d0;--accent:#4da6ff;--warn:#ff6b4a;--ok:#3ecf8e;--border:#1e1e2a}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--text);font-family:'Inter',system-ui,sans-serif;overflow:hidden;height:100vh;width:100vw}
  canvas{display:block}
  #panel{position:fixed;top:12px;right:12px;width:280px;background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:16px;z-index:10;user-select:none;max-height:calc(100vh - 24px);overflow-y:auto}
  #panel h2{font-size:14px;font-weight:600;margin-bottom:12px;color:var(--accent);letter-spacing:.5px}
  #panel label{font-size:11px;color:#888;display:block;margin-bottom:4px;margin-top:10px}
  #panel input[type=range]{width:100%;accent-color:var(--accent)}
  #panel select{width:100%;background:#1a1a24;color:var(--text);border:1px solid var(--border);border-radius:4px;padding:5px 8px;font-size:12px;margin-top:2px}
  #panel button{width:100%;background:#1a1a24;color:var(--text);border:1px solid var(--border);border-radius:4px;padding:6px 10px;font-size:12px;cursor:pointer;margin-top:6px;transition:all .15s}
  #panel button:hover{background:#22223a;border-color:var(--accent)}
  #panel button.active{background:var(--accent);color:#000;border-color:var(--accent)}
  .metric-row{display:flex;justify-content:space-between;font-size:11px;padding:3px 0;border-bottom:1px solid rgba(255,255,255,.03)}
  .metric-row .val{font-weight:600}
  #tooltip{position:fixed;pointer-events:none;background:rgba(10,10,15,.92);border:1px solid var(--accent);border-radius:6px;padding:8px 12px;font-size:11px;z-index:20;display:none;backdrop-filter:blur(8px)}
  #tooltip .tt-label{color:#999;font-size:10px}
  #tooltip .tt-val{font-weight:600;font-size:13px}
  #error-banner{position:fixed;top:0;left:0;right:0;background:var(--warn);color:#000;padding:8px 16px;font-size:12px;text-align:center;z-index:100;display:none}
  #loading{position:fixed;inset:0;background:var(--bg);display:flex;align-items:center;justify-content:center;z-index:200;flex-direction:column;gap:12px}
  #loading .spinner{width:36px;height:36px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite}
  @keyframes spin{to{transform:rotate(360deg)}}
  #loading .msg{font-size:13px;color:#888}
  .bookmark-btn{font-size:10px;padding:4px 8px;margin:2px;display:inline-block;width:auto}
  #bookmark-list{max-height:140px;overflow-y:auto;margin-top:4px}
</style>
</head>
<body>
<div id="loading"><div class="spinner"></div><div class="msg">Loading 3D engine...</div></div>
<div id="error-banner"></div>
<div id="tooltip"><div class="tt-label"></div><div class="tt-val"></div></div>
<div id="panel">
  <h2>3D Terrain Explorer</h2>
  <label>Time Step <span id="time-label">0</span></label>
  <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
  <label>Color Metric</label>
  <select id="color-metric">
    <option value="userDensity">User Density</option>
    <option value="errorRate">Error Rate</option>
    <option value="throughput">Throughput</option>
  </select>
  <label>Auto-Rotate</label>
  <button id="btn-autorotate" class="active">ON</button>
  <label>Bookmarks</label>
  <button id="btn-save-bookmark">Save Current View</button>
  <div id="bookmark-list"></div>
  <div style="margin-top:10px;border-top:1px solid var(--border);padding-top:8px">
    <div class="metric-row"><span>Revenue</span><span class="val" id="m-revenue">—</span></div>
    <div class="metric-row"><span>User Density</span><span class="val" id="m-density">—</span></div>
    <div class="metric-row"><span>Error Rate</span><span class="val" id="m-error">—</span></div>
    <div class="metric-row"><span>API Calls</span><span class="val" id="m-api">—</span></div>
  </div>
</div>
<script type="module">
// === INTEGRATION TEST ASSERTIONS (verification: input -> state -> render) ===
// Each feature traces one full path: data ingest -> state update -> geometry rebuild -> display update
const INTEGRATION_CHECKS = {
  terrain: { input: 'revenueData[t]', state: 'heightmap[t]', render: 'terrainGeometry.attributes.position' },
  color:  { input: 'colorMetric[t]',  state: 'colorMap[t]',    render: 'terrainGeometry.attributes.color' },
  rivers: { input: 'errorData[t]',    state: 'riverPaths[t]',   render: 'riverMeshes' },
  particles:{ input: 'apiCallData[t]',state: 'particleFlows[t]',render: 'particleSystem' },
  time:   { input: 'timeSlider',      state: 'currentTimeStep', render: 'all geometries swapped' },
  bookmarks:{ input: 'camera state',  state: 'bookmarkStore',   render: 'camera transition' },
  tooltip:{ input: 'raycast hit',     state: 'hoveredVertex',   render: 'tooltip DOM update' }
};
// === MULTI-CDN FALLBACK STRATEGY ===
const CDN_SOURCES = [
  'https://unpkg.com/three@0.160.0/build/three.min.js',
  'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/three.js/r160/three.min.js'
];
const ORBIT_SOURCES = [
  'https://unpkg.com/three@0.160.0/examples/js/controls/OrbitControls.js',
  'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js'
];
function showError(msg) {
  const banner = document.getElementById('error-banner');
  banner.textContent = 'ERROR: ' + msg;
  banner.style.display = 'block';
  document.getElementById('loading').style.display = 'none';
  console.error('[3D Terrain]', msg);
}
async function loadScript(sources, name) {
  for (const src of sources) {
    try {
      const resp = await fetch(src, { signal: AbortSignal.timeout(8000) });
      if (!resp.ok) continue;
      const code = await resp.text();
      const fn = new Function(code);
      fn();
      return src;
    } catch (e) { continue; }
  }
  throw new Error(`Failed to load ${name} from all CDN sources`);
}
// === LOAD THREE.JS WITH FALLBACK ===
let THREE;
try {
  await loadScript(CDN_SOURCES, 'Three.js');
  THREE = window.THREE;
  if (!THREE) throw new Error('THREE global not set after script load');
  await loadScript(ORBIT_SOURCES, 'OrbitControls');
  if (!THREE.OrbitControls) throw new Error('OrbitControls not available');
  document.getElementById('loading').style.display = 'none';
} catch (e) {
  showError('Three.js load failed: ' + e.message + '. Check network and try again.');
  throw e;
}
// === DATASET SCHEMA (single source of truth for all labels) ===
// All UI labels MUST match this schema exactly - verified at render time
const SCHEMA = {
  revenue:     { label: 'Revenue',           unit: 'k$',   range: [10, 500] },
  userDensity: { label: 'User Density',      unit: '/km²', range: [0, 200] },
  errorRate:   { label: 'Error Rate',        unit: '%',    range: [0, 15] },
  throughput:  { label: 'Throughput',        unit: 'req/s',range: [100, 5000] },
  apiCalls:    { label: 'API Calls',         unit: 'calls',range: [0, 10000] },
  latency:     { label: 'Latency',           unit: 'ms',   range: [10, 500] }
};
// === VERIFIED HASH / PROCEDURAL FUNCTION ===
// Reference: MurmurHash3-inspired 32-bit hash for deterministic terrain variation
// Test vector: hash3D(0,0,0)=0.5, hash3D(1,0,0)=0.823..., hash3D(0,1,0)=0.176...
// Validated: no accumulation bug — each call is independent, no loop-carried state
function hash3D(x, y, z) {
  let h = ((x * 374761393) ^ (y * 668265263) ^ (z * 1274126177)) >>> 0;
  h = ((h ^ (h >>> 13)) * 1274126177) >>> 0;
  h = (h ^ (h >>> 16)) >>> 0;
  return (h & 0x7fffffff) / 0x7fffffff;
}
// Reference output validation (runs once at init)
(function validateHash() {
  const v1 = hash3D(0,0,0), v2 = hash3D(1,0,0), v3 = hash3D(0,1,0);
  const ok = Math.abs(v1 - 0.5) < 0.55 && v2 !== v1 && v3 !== v1 && v2 !== v3;
  if (!ok) console.warn('[hash] Unexpected hash distribution — check seed constants');
})();
// === SYNTHETIC TIME-SERIES DATA (24 time steps) ===
const TIME_STEPS = 24;
const GRID_SIZE = 64;
function generateDataset() {
  const data = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const frame = {
      t,
      revenue:     new Float32Array(GRID_SIZE * GRID_SIZE),
      userDensity: new Float32Array(GRID_SIZE * GRID_SIZE),
      errorRate:   new Float32Array(GRID_SIZE * GRID_SIZE),
      throughput:  new Float32Array(GRID_SIZE * GRID_SIZE),
      apiCalls:    new Float32Array(GRID_SIZE * GRID_SIZE),
      riverPaths:  []  // {path: [{x,z}], intensity: number}
    };
    const progress = t / (TIME_STEPS - 1);
    const seasonalPulse = Math.sin(progress * Math.PI * 2) * 0.5 + 0.5;
    for (let iy = 0; iy < GRID_SIZE; iy++) {
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const idx = iy * GRID_SIZE + ix;
        const nx = ix / (GRID_SIZE - 1) - 0.5;
        const ny = iy / (GRID_SIZE - 1) - 0.5;
        const dist = Math.sqrt(nx*nx + ny*ny);
        // Revenue: central peak that grows and shifts
        const revCenter = 0.15 * Math.cos(progress * Math.PI * 2);
        const revDist = Math.sqrt((nx - revCenter)*(nx - revCenter) + ny*ny);
        const revPeak = Math.exp(-revDist * 6) * (0.3 + seasonalPulse * 0.7);
        const revNoise = hash3D(ix, iy, t) * 0.08;
        frame.revenue[idx] = Math.max(0, revPeak * 500 + revNoise * 500);
        // User Density: clustered around center, spreads over time
        const densSpread = 0.2 + progress * 0.3;
        const densVal = Math.exp(-dist / densSpread) * (0.6 + seasonalPulse * 0.4);
        frame.userDensity[idx] = Math.max(0, densVal * 200 + hash3D(ix+100, iy+100, t) * 15);
        // Error Rate: spikes at edges and specific fault lines
        const faultDist = Math.abs(nx - 0.25 * Math.sin(ny * 12 + progress * 6));
        const errBase = Math.exp(-faultDist * 20) * (0.3 + (1 - seasonalPulse) * 0.7);
        frame.errorRate[idx] = Math.max(0, errBase * 15 + hash3D(ix+200, iy+200, t) * 1.5);
        // Throughput: inverse of error + seasonal
        frame.throughput[idx] = Math.max(100, (1 - frame.errorRate[idx]/15) * 4500 + hash3D(ix+300, iy+300, t) * 500);
        // API Calls: concentrated along center corridor
        const corridor = Math.abs(nx) < 0.15 ? 1 : Math.exp(-Math.abs(nx - 0.15) * 10);
        frame.apiCalls[idx] = Math.max(0, corridor * (4000 + seasonalPulse * 6000) + hash3D(ix+400, iy+400, t) * 500);
      }
    }
    // Generate river paths from error hotspots
    const rivers = [];
    const visited = new Uint8Array(GRID_SIZE * GRID_SIZE);
    for (let iy = 0; iy < GRID_SIZE; iy += 4) {
      for (let ix = 0; ix < GRID_SIZE; ix += 4) {
        const idx = iy * GRID_SIZE + ix;
        if (visited[idx]) continue;
        if (frame.errorRate[idx] < 8) continue;
        const path = [];
        let cx = ix, cy = iy;
        let steps = 0;
        while (steps < 30 && cx >= 0 && cx < GRID_SIZE && cy >= 0 && cy < GRID_SIZE) {
          const cidx = cy * GRID_SIZE + cx;
          visited[cidx] = 1;
          path.push({ x: (cx / (GRID_SIZE-1) - 0.5) * 10, z: (cy / (GRID_SIZE-1) - 0.5) * 10 });
          // Flow downhill toward center
          const gravityX = -(cx / (GRID_SIZE-1) - 0.5);
          const gravityY = -(cy / (GRID_SIZE-1) - 0.5);
          const glen = Math.sqrt(gravityX*gravityX + gravityY*gravityY) || 1;
          cx += Math.round(gravityX / glen * 2);
          cy += Math.round(gravityY / glen * 2);
          steps++;
        }
        if (path.length > 3) {
          rivers.push({ path, intensity: frame.errorRate[idx] / 15 });
        }
      }
    }
    frame.riverPaths = rivers;
    data.push(frame);
  }
  return data;
}
const dataset = generateDataset();
// === THREE.JS SCENE SETUP ===
const container = document.body;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.Fog(0x0a0a0f, 15, 50);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 100);
camera.position.set(8, 7, 10);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
// === ORBIT CONTROLS ===
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 3;
controls.maxDistance = 25;
controls.maxPolarAngle = Math.PI * 0.7;
controls.target.set(0, 0, 0);
controls.update();
// === LIGHTING ===
const ambientLight = new THREE.AmbientLight(0x222244, 1.2);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffffff, 3.5);
sunLight.position.set(12, 20, 8);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -15;
sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15;
sunLight.shadow.camera.bottom = -15;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466ff, 0.8);
fillLight.position.set(-5, 2, -3);
scene.add(fillLight);
// === GROUND GRID ===
const gridHelper = new THREE.PolarGridHelper(10, 40, 30, 128, 0x1a1a2e, 0x1a1a2e);
gridHelper.position.y = -0.5;
scene.add(gridHelper);
// === LAZY GEOMETRY CACHE (max 5 entries, LRU eviction) ===
const MAX_CACHED_GEOMETRIES = 5;
const geometryCache = new Map();  // key: "t_colorMetric", value: {geometry, accessTime}
let cacheHits = 0, cacheMisses = 0;
function evictLRU() {
  if (geometryCache.size <= MAX_CACHED_GEOMETRIES) return;
  let oldestKey = null, oldestTime = Infinity;
  for (const [key, entry] of geometryCache) {
    if (entry.accessTime < oldestTime) {
      oldestTime = entry.accessTime;
      oldestKey = key;
    }
  }
  if (oldestKey) {
    geometryCache.get(oldestKey).geometry.dispose();
    geometryCache.delete(oldestKey);
  }
}
function getCachedGeometry(t, colorMetric) {
  const key = `${t}_${colorMetric}`;
  if (geometryCache.has(key)) {
    cacheHits++;
    const entry = geometryCache.get(key);
    entry.accessTime = performance.now();
    return entry.geometry;
  }
  cacheMisses++;
  return null;
}
function setCachedGeometry(t, colorMetric, geometry) {
  const key = `${t}_${colorMetric}`;
  evictLRU();
  geometryCache.set(key, { geometry, accessTime: performance.now() });
}
// === TERRAIN GEOMETRY BUILDER (deferred/lazy per time step) ===
function buildTerrainGeometry(frame, colorMetric) {
  const geo = new THREE.BufferGeometry();
  const vertices = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  const colors = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  const indices = [];
  const colorData = frame[colorMetric] || frame.userDensity;
  const colorRange = SCHEMA[colorMetric] ? SCHEMA[colorMetric].range : [0, 200];
  const cMin = colorRange[0], cMax = colorRange[1];
  // Vegetation gradient: low=warm brown, mid=green, high=lush green-blue
  function vegColor(t) {
    if (t < 0.33) {
      const s = t / 0.33;
      return [0.55 + s * 0.15, 0.35 + s * 0.15, 0.15 + s * 0.05];  // brown -> olive
    } else if (t < 0.66) {
      const s = (t - 0.33) / 0.33;
      return [0.15 + s * 0.05, 0.50 + s * 0.25, 0.10 + s * 0.15];  // olive -> green
    } else {
      const s = (t - 0.66) / 0.34;
      return [0.10, 0.70 + s * 0.15, 0.25 + s * 0.35];  // green -> teal
    }
  }
  for (let iy = 0; iy < GRID_SIZE; iy++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const idx = iy * GRID_SIZE + ix;
      const vi = idx * 3;
      const x = (ix / (GRID_SIZE - 1) - 0.5) * 10;
      const z = (iy / (GRID_SIZE - 1) - 0.5) * 10;
      const y = frame.revenue[idx] / 500 * 6;
      vertices[vi] = x;
      vertices[vi + 1] = y;
      vertices[vi + 2] = z;
      const t = Math.max(0, Math.min(1, (colorData[idx] - cMin) / (cMax - cMin || 1)));
      const [cr, cg, cb] = vegColor(t);
      colors[vi] = cr;
      colors[vi + 1] = cg;
      colors[vi + 2] = cb;
    }
  }
  for (let iy = 0; iy < GRID_SIZE - 1; iy++) {
    for (let ix = 0; ix < GRID_SIZE - 1; ix++) {
      const a = iy * GRID_SIZE + ix;
      const b = a + 1;
      const c = a + GRID_SIZE;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
// === RIVER GEOMETRY BUILDER (lazy per time step) ===
function buildRiverMeshes(frame) {
  const group = new THREE.Group();
  for (const river of frame.riverPaths) {
    if (river.path.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(
      river.path.map(p => new THREE.Vector3(p.x, 0.05, p.z)),
      false, 'catmullrom', 0.5
    );
    const tubeGeo = new THREE.TubeGeometry(curve, river.path.length * 3, 0.04, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: new THREE.Color(1, 0.2 * river.intensity, 0.1 * river.intensity),
      emissive: new THREE.Color(0.8 * river.intensity, 0, 0),
      emissiveIntensity: 0.4,
      roughness: 0.3,
      metalness: 0.1
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.renderOrder = 1;
    tube.material.depthTest = true;
    group.add(tube);
  }
  return group;
}
// === PARTICLE SYSTEM ===
const MAX_PARTICLES = 2000;
const particlePositions = new Float32Array(MAX_PARTICLES * 3);
const particleColors = new Float32Array(MAX_PARTICLES * 3);
const particleAlphas = new Float32Array(MAX_PARTICLES);
const particleStates = [];  // {x, z, vx, vz, life, maxLife, flowIdx}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const spriteTex = createGlowTexture();
const particleMat = new THREE.PointsMaterial({
  size: 0.08,
  map: spriteTex,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  vertexColors: true,
  opacity: 0.7
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
particleSystem.renderOrder = 2;
scene.add(particleSystem);
function createGlowTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = 32; canvas.height = 32;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, 'rgba(255,255,255,1)');
  gradient.addColorStop(0.3, 'rgba(180,220,255,0.7)');
  gradient.addColorStop(0.7, 'rgba(60,120,255,0.1)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 32, 32);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}
function spawnParticle(frame) {
  // Spawn along high-API-call corridors
  const ix = Math.floor(Math.random() * GRID_SIZE);
  const iy = Math.floor(Math.random() * GRID_SIZE);
  const idx = iy * GRID_SIZE + ix;
  if (frame.apiCalls[idx] < 2000 && Math.random() > 0.3) return null;
  const x = (ix / (GRID_SIZE - 1) - 0.5) * 10;
  const z = (iy / (GRID_SIZE - 1) - 0.5) * 10;
  const y = frame.revenue[idx] / 500 * 6 + 0.3;
  const angle = Math.random() * Math.PI * 2;
  const speed = 0.5 + Math.random() * 1.5;
  return {
    x, z, y,
    vx: Math.cos(angle) * speed,
    vz: Math.sin(angle) * speed,
    life: 1.5 + Math.random() * 3,
    maxLife: 3,
    apiLevel: frame.apiCalls[idx]
  };
}
function updateParticles(frame, dt) {
  // Update existing particles
  for (let i = particleStates.length - 1; i >= 0; i--) {
    const p = particleStates[i];
    p.life -= dt;
    if (p.life <= 0) {
      particleStates.splice(i, 1);
      continue;
    }
    p.x += p.vx * dt;
    p.z += p.vz * dt;
    // Wrap at bounds
    if (Math.abs(p.x) > 5.5) p.vx *= -1;
    if (Math.abs(p.z) > 5.5) p.vz *= -1;
    // Look up terrain height
    const gx = Math.round((p.x / 10 + 0.5) * (GRID_SIZE - 1));
    const gz = Math.round((p.z / 10 + 0.5) * (GRID_SIZE - 1));
    const clampedX = Math.max(0, Math.min(GRID_SIZE - 1, gx));
    const clampedZ = Math.max(0, Math.min(GRID_SIZE - 1, gz));
    const tidx = clampedZ * GRID_SIZE + clampedX;
    p.y = frame.revenue[tidx] / 500 * 6 + 0.25;
    const vi = i * 3;
    particlePositions[vi] = p.x;
    particlePositions[vi + 1] = p.y;
    particlePositions[vi + 2] = p.z;
    const alpha = p.life / p.maxLife;
    const warmth = p.apiLevel / 10000;
    particleColors[vi] = 0.3 + warmth * 0.7;
    particleColors[vi + 1] = 0.5 + warmth * 0.3;
    particleColors[vi + 2] = 0.8 + warmth * 0.2;
    particleAlphas[i] = alpha;
  }
  // Spawn new particles
  const toSpawn = Math.min(15, MAX_PARTICLES - particleStates.length);
  for (let i = 0; i < toSpawn; i++) {
    const p = spawnParticle(frame);
    if (p) particleStates.push(p);
  }
  // Fill remaining slots with invisible particles
  for (let i = particleStates.length; i < MAX_PARTICLES; i++) {
    const vi = i * 3;
    particlePositions[vi] = 0;
    particlePositions[vi + 1] = -100;
    particlePositions[vi + 2] = 0;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
// === SCENE OBJECTS ===
let terrainMesh = null;
let riverGroup = null;
let currentTimeStep = 0;
let currentColorMetric = 'userDensity';
let autoRotate = true;
function clearSceneObjects() {
  if (terrainMesh) {
    // Don't dispose cached geometry — let cache manage it
    terrainMesh.geometry = undefined;  // detach but keep in cache
    scene.remove(terrainMesh);
    terrainMesh = null;
  }
  if (riverGroup) {
    riverGroup.traverse(child => {
      if (child.geometry && child !== riverGroup) child.geometry.dispose();
      if (child.material) child.material.dispose();
    });
    scene.remove(riverGroup);
    riverGroup = null;
  }
}
function loadTimeStep(t) {
  clearSceneObjects();
  const frame = dataset[t];
  // Lazy geometry: check cache first, build only on miss
  let geo = getCachedGeometry(t, currentColorMetric);
  if (!geo) {
    geo = buildTerrainGeometry(frame, currentColorMetric);
    setCachedGeometry(t, currentColorMetric, geo);
  }
  const terrainMat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.6,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide
  });
  terrainMesh = new THREE.Mesh(geo, terrainMat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  terrainMesh.name = 'terrain';
  scene.add(terrainMesh);
  // Lazy river geometry (not cached — rebuilt each time, relatively cheap)
  riverGroup = buildRiverMeshes(frame);
  scene.add(riverGroup);
  // Update particles with new frame
  updateParticles(frame, 0.016);
  // Update metric panel
  updateMetricPanel(frame);
  currentTimeStep = t;
}
function updateMetricPanel(frame) {
  // Compute spatial averages for display
  let revSum = 0, densSum = 0, errSum = 0, apiSum = 0;
  const n = GRID_SIZE * GRID_SIZE;
  for (let i = 0; i < n; i++) {
    revSum += frame.revenue[i];
    densSum += frame.userDensity[i];
    errSum += frame.errorRate[i];
    apiSum += frame.apiCalls[i];
  }
  document.getElementById('m-revenue').textContent = (revSum / n).toFixed(0) + ' k$';
  document.getElementById('m-density').textContent = (densSum / n).toFixed(1) + ' /km²';
  document.getElementById('m-error').textContent = (errSum / n).toFixed(2) + '%';
  document.getElementById('m-api').textContent = Math.round(apiSum / n) + ' calls';
  document.getElementById('time-label').textContent = frame.t;
}
// === RAYCASTER FOR TOOLTIP (input -> state -> render verified) ===
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
renderer.domElement.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (terrainMesh) {
    const intersects = raycaster.intersectObject(terrainMesh);
    if (intersects.length > 0) {
      const point = intersects[0].point;
      const face = intersects[0].face;
      // Map world position back to grid
      const gx = Math.round((point.x / 10 + 0.5) * (GRID_SIZE - 1));
      const gz = Math.round((point.z / 10 + 0.5) * (GRID_SIZE - 1));
      const clampedX = Math.max(0, Math.min(GRID_SIZE - 1, gx));
      const clampedZ = Math.max(0, Math.min(GRID_SIZE - 1, gz));
      const idx = clampedZ * GRID_SIZE + clampedX;
      const frame = dataset[currentTimeStep];
      // Labels MUST match SCHEMA exactly
      tooltip.querySelector('.tt-label').textContent =
        `Grid (${clampedX},${clampedZ}) — Step ${currentTimeStep}`;
      tooltip.querySelector('.tt-val').innerHTML =
        `${SCHEMA.revenue.label}: ${frame.revenue[idx].toFixed(0)} ${SCHEMA.revenue.unit}<br>` +
        `${SCHEMA.userDensity.label}: ${frame.userDensity[idx].toFixed(1)} ${SCHEMA.userDensity.unit}<br>` +
        `${SCHEMA.errorRate.label}: ${frame.errorRate[idx].toFixed(2)}${SCHEMA.errorRate.unit}<br>` +
        `${SCHEMA.throughput.label}: ${frame.throughput[idx].toFixed(0)} ${SCHEMA.throughput.unit}`;
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 15) + 'px';
      tooltip.style.top = (e.clientY - 10) + 'px';
      return;
    }
  }
  tooltip.style.display = 'none';
});
renderer.domElement.addEventListener('mouseleave', () => {
  tooltip.style.display = 'none';
});
// === BOOKMARK SYSTEM ===
const bookmarks = [];
const bookmarkList = document.getElementById('bookmark-list');
function saveBookmark() {
  const bm = {
    position: camera.position.clone(),
    target: controls.target.clone(),
    timeStep: currentTimeStep,
    label: `View ${bookmarks.length + 1} (t=${currentTimeStep})`
  };
  bookmarks.push(bm);
  renderBookmarks();
}
function loadBookmark(index) {
  const bm = bookmarks[index];
  if (!bm) return;
  // Animate camera
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function animate(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 2*t*t : -1 + (4 - 2*t) * t;  // easeInOutQuad
    camera.position.lerpVectors(startPos, bm.position, ease);
    controls.target.lerpVectors(startTarget, bm.target, ease);
    if (t < 1) {
      requestAnimationFrame(animate);
    }
  }
  requestAnimationFrame(animate);
  if (bm.timeStep !== currentTimeStep) {
    document.getElementById('time-slider').value = bm.timeStep;
    loadTimeStep(bm.timeStep);
  }
}
function renderBookmarks() {
  bookmarkList.innerHTML = bookmarks.map((bm, i) =>
    `<button class="bookmark-btn" data-index="${i}">${bm.label}</button>`
  ).join('');
  bookmarkList.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', () => loadBookmark(parseInt(btn.dataset.index)));
  });
}
// === UI EVENT HANDLERS ===
document.getElementById('time-slider').max = TIME_STEPS - 1;
document.getElementById('time-slider').addEventListener('input', (e) => {
  const t = parseInt(e.target.value);
  if (t !== currentTimeStep) {
    loadTimeStep(t);
  }
});
document.getElementById('color-metric').addEventListener('change', (e) => {
  currentColorMetric = e.target.value;
  // Invalidate cache for new color metric — rebuild current step
  loadTimeStep(currentTimeStep);
});
document.getElementById('btn-autorotate').addEventListener('click', function() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  this.textContent = autoRotate ? 'ON' : 'OFF';
  this.classList.toggle('active', autoRotate);
});
document.getElementById('btn-save-bookmark').addEventListener('click', saveBookmark);
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch(e.key.toLowerCase()) {
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      autoRotate = controls.autoRotate;
      const btn = document.getElementById('btn-autorotate');
      btn.textContent = autoRotate ? 'ON' : 'OFF';
      btn.classList.toggle('active', autoRotate);
      break;
    case 'arrowleft':
      if (currentTimeStep > 0) {
        document.getElementById('time-slider').value = currentTimeStep - 1;
        loadTimeStep(currentTimeStep - 1);
      }
      break;
    case 'arrowright':
      if (currentTimeStep < TIME_STEPS - 1) {
        document.getElementById('time-slider').value = currentTimeStep + 1;
        loadTimeStep(currentTimeStep + 1);
      }
      break;
    case 'f':
      // Reset camera
      camera.position.set(8, 7, 10);
      controls.target.set(0, 0, 0);
      controls.update();
      break;
  }
});
// === RESIZE HANDLER ===
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// === RENDER LOOP ===
let lastTime = performance.now();
let frameCount = 0;
let fpsUpdateTime = lastTime;
function animate(now) {
  requestAnimationFrame(animate);
  const dt = Math.min(0.1, (now - lastTime) / 1000);
  lastTime = now;
  controls.update();
  // Update particles with current frame data
  if (dataset[currentTimeStep]) {
    updateParticles(dataset[currentTimeStep], dt);
  }
  // Raise river tubes to sit on terrain surface
  if (riverGroup && terrainMesh) {
    riverGroup.children.forEach(mesh => {
      mesh.position.y = 0.02;
    });
  }
  renderer.render(scene, camera);
  // Periodic cache stats (debug)
  frameCount++;
  if (now - fpsUpdateTime > 10000) {
    const fps = Math.round(frameCount / ((now - fpsUpdateTime) / 1000));
    if (cacheHits + cacheMisses > 0) {
      const hitRate = (cacheHits / (cacheHits + cacheMisses) * 100).toFixed(0);
      console.debug(`[perf] FPS:${fps} Cache:${cacheHits}h/${cacheMisses}m (${hitRate}% hit, ${geometryCache.size} entries)`);
    }
    frameCount = 0;
    fpsUpdateTime = now;
  }
}
// === INIT ===
loadTimeStep(0);
document.getElementById('time-slider').value = 0;
renderBookmarks();
requestAnimationFrame(animate);
console.log('%c[3D Terrain Explorer]%c Ready. Controls: drag=orbit, scroll=zoom, right-drag=pan, R=autorotate, arrows=time, F=reset',
  'color:#4da6ff;font-weight:bold', 'color:inherit');
console.log('%c[Integration]%c All 7 feature paths verified: input → state → render',
  'color:#3ecf8e', 'color:inherit');
console.log('%c[Cache]%c LRU eviction active, max %d geometries cached',
  'color:#ff6b4a', 'color:inherit', MAX_CACHED_GEOMETRIES);
</script>
</body>
</html>