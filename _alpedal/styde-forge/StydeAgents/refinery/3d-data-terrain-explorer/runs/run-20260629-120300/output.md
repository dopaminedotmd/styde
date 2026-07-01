<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>3D Data Terrain Explorer</title><style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#0a0a14;font-family:system-ui,sans-serif;color:#ccc}
#c{width:100vw;height:100vh;display:block}
#panel{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:12px;align-items:center;background:rgba(10,10,20,0.85);padding:10px 20px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);backdrop-filter:blur(8px)}
#panel label{font-size:13px;white-space:nowrap}
#panel input[type=range]{width:200px;accent-color:#4fc3f7}
#panel span{font-size:12px;min-width:32px;text-align:center}
#bookmarks{position:fixed;top:16px;right:16px;z-index:10;display:flex;flex-direction:column;gap:6px}
#bookmarks button{background:rgba(10,10,20,0.8);border:1px solid rgba(255,255,255,0.15);color:#aaa;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:11px;transition:all 0.2s}
#bookmarks button:hover{color:#fff;border-color:#4fc3f7}
#diag{position:fixed;top:16px;left:16px;z-index:10;background:rgba(10,10,20,0.8);padding:8px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.1);font-size:11px;line-height:1.5;font-family:monospace;max-width:220px}
#diag .hit{color:#66bb6a}
#diag .miss{color:#ef5350}
#diag .fps{color:#4fc3f7}
#tooltip{position:fixed;pointer-events:none;z-index:20;background:rgba(0,0,0,0.85);color:#fff;padding:6px 10px;border-radius:6px;font-size:11px;display:none;white-space:nowrap}
</style></head><body>
<canvas id="c"></canvas>
<div id="panel">
  <label>Time</label><input type="range" id="slider" min="0" max="23" value="12" step="1"><span id="tlabel">12:00</span>
  <button id="autoplay" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);color:#ccc;padding:4px 12px;border-radius:6px;cursor:pointer;font-size:12px">Play</button>
</div>
<div id="bookmarks">
  <button data-bm="overview">Overview</button>
  <button data-bm="peak1">Revenue Peak</button>
  <button data-bm="river">River View</button>
  <button data-bm="valley">Valley</button>
</div>
<div id="diag">
  <div>FPS: <span class="fps" id="fpsV">--</span></div>
  <div>Terrain: <span class="hit" id="tHit">0</span>h <span class="miss" id="tMiss">0</span>m</div>
  <div>River: <span class="hit" id="rHit">0</span>h <span class="miss" id="rMiss">0</span>m</div>
  <div>Step: <span id="curStep">12</span></div>
</div>
<div id="tooltip"></div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// === CONFIG ===
const GRID = 80, SIZE = 20, TIMESTEPS = 24, RIVER_COUNT = 4;
const PARTICLE_COUNT = 180, DEBOUNCE_MS = 200, MAX_HEIGHT = 10;
const HALF = SIZE / 2;
// === UTILS ===
function gauss(x, y, cx, cy, sx, sy) {
  const dx = (x - cx) / sx, dy = (y - cy) / sy;
  return Math.exp(-0.5 * (dx * dx + dy * dy));
}
function lerp(a, b, t) { return a + (b - a) * t; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
// === DATA GENERATION (synthetic time-series) ===
const data = { revenue: [], users: [], errors: [], apiFlows: [] };
const peaks = [
  { cx: 0.30, cy: 0.40, sx: 0.15, sy: 0.12, amp: 80 },
  { cx: 0.60, cy: 0.60, sx: 0.10, sy: 0.18, amp: 60 },
  { cx: 0.50, cy: 0.30, sx: 0.20, sy: 0.10, amp: 45 },
];
const hubs = [
  { x: 0.2, y: 0.3 }, { x: 0.7, y: 0.5 },
  { x: 0.4, y: 0.7 }, { x: 0.6, y: 0.2 },
];
for (let t = 0; t < TIMESTEPS; t++) {
  const rev = new Float32Array(GRID * GRID);
  const usr = new Float32Array(GRID * GRID);
  const err = new Float32Array(GRID * GRID);
  const tf = t / TIMESTEPS;
  // Evolving peak centers drift over time
  const tp = peaks.map((p, i) => ({
    cx: p.cx + Math.sin(tf * Math.PI * 2 + i) * 0.06,
    cy: p.cy + Math.cos(tf * Math.PI * 2 + i * 1.3) * 0.05,
    sx: p.sx, sy: p.sy,
    amp: p.amp + t * (i === 0 ? 2 : i === 1 ? 1 : 1.5),
  }));
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const x = j / GRID, y = i / GRID;
      let h = 0;
      for (const p of tp) h += p.amp * gauss(x, y, p.cx, p.cy, p.sx, p.sy);
      // Terrain detail ridges
      h += Math.sin(x * 14 + tf * 6) * Math.cos(y * 9) * 6;
      h += Math.sin(y * 20 - tf * 4) * Math.cos(x * 7) * 3;
      rev[i * GRID + j] = h;
      // User density: broad center blob + gentle oscillations
      usr[i * GRID + j] = clamp(
        20 + 55 * gauss(x, y, 0.5 + tf * 0.08, 0.48 + Math.sin(tf * 3) * 0.06, 0.38, 0.42)
          + 18 * Math.sin(x * 7 + tf * 3) * Math.cos(y * 6), 0, 100);
      // Error spikes: concentrated hotspot that drifts + random noise floor
      const ex = 0.26 + tf * 0.12, ey = 0.54 + Math.cos(tf * 5) * 0.04;
      const spike = gauss(x, y, ex, ey, 0.025, 0.035);
      err[i * GRID + j] = clamp(
        spike * (55 + Math.sin(tf * 7) * 25) + (Math.random() < 0.015 ? Math.random() * 40 : 0), 0, 100);
    }
  }
  data.revenue.push(rev);
  data.users.push(usr);
  data.errors.push(err);
  // API flows between hubs, volume varies over time
  const flows = [];
  for (let a = 0; a < hubs.length; a++) {
    for (let b = a + 1; b < hubs.length; b++) {
      const vol = 0.25 + Math.random() * 0.5 + Math.sin(tf * 5 + a * 1.7) * 0.25;
      if (vol > 0.2) flows.push({ from: hubs[a], to: hubs[b], volume: vol });
    }
  }
  data.apiFlows.push(flows);
}
// === SCENE SETUP ===
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 25, 55);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 100);
camera.position.set(8, 14, 18);
camera.lookAt(0, 3, 0);
// Lighting
const ambient = new THREE.AmbientLight(0x303050, 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 4);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 1;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -15;
sun.shadow.camera.right = 15;
sun.shadow.camera.top = 15;
sun.shadow.camera.bottom = -15;
sun.shadow.bias = -0.0005;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
fill.position.set(-5, 3, -8);
scene.add(fill);
// OrbitControls with smoothing
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 3, 0);
controls.maxPolarAngle = Math.PI * 0.52;
controls.minDistance = 5;
controls.maxDistance = 35;
controls.update();
// Ground reference plane
const groundGeo = new THREE.PlaneGeometry(SIZE * 1.4, SIZE * 1.4);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a1a2e, roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.15;
ground.receiveShadow = true;
scene.add(ground);
// Grid helper for spatial reference
const grid = new THREE.GridHelper(SIZE, 40, 0x333355, 0x1a1a2e);
grid.position.y = -0.1;
scene.add(grid);
// === TERRAIN SYSTEM ===
// Precompute all heightfield variants (Float32Array per timestep)
const terrainCache = new Map(); // timestep -> { heightData: Float32Array, colorData: Float32Array }
function computeTerrainVariant(t) {
  if (terrainCache.has(t)) {
    cacheStats.terrainHits++;
    return terrainCache.get(t);
  }
  cacheStats.terrainMisses++;
  const rev = data.revenue[t];
  const usr = data.users[t];
  const vertCount = (GRID + 1) * (GRID + 1);
  // Height data for vertex positions (z-axis = height)
  const heights = new Float32Array(vertCount);
  // Vertex colors from user density (vegetation gradient: blue->green->yellow)
  const colors = new Float32Array(vertCount * 3);
  for (let i = 0; i <= GRID; i++) {
    for (let j = 0; j <= GRID; j++) {
      const idx = i * (GRID + 1) + j;
      // Sample from grid (clamp edges)
      const gi = Math.min(i, GRID - 1), gj = Math.min(j, GRID - 1);
      const h = rev[gi * GRID + gj];
      const u = usr[gi * GRID + gj];
      heights[idx] = (h / 100) * MAX_HEIGHT;
      // Color gradient: low=blue(0,0.4,1), mid=green(0.1,0.8,0.3), high=yellow(1,0.9,0.1)
      const tCol = u / 100;
      if (tCol < 0.5) {
        const s = tCol / 0.5;
        colors[idx * 3] = lerp(0.05, 0.1, s);
        colors[idx * 3 + 1] = lerp(0.35, 0.75, s);
        colors[idx * 3 + 2] = lerp(0.9, 0.3, s);
      } else {
        const s = (tCol - 0.5) / 0.5;
        colors[idx * 3] = lerp(0.1, 0.95, s);
        colors[idx * 3 + 1] = lerp(0.75, 0.88, s);
        colors[idx * 3 + 2] = lerp(0.3, 0.12, s);
      }
    }
  }
  const entry = { heightData: heights, colorData: colors };
  terrainCache.set(t, entry);
  return entry;
}
// Build terrain mesh (once, geometry reused)
const terrainGeo = new THREE.PlaneGeometry(SIZE, SIZE, GRID, GRID);
terrainGeo.rotateX(-Math.PI / 2); // Lay flat, Y becomes height axis
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
});
const terrain = new THREE.Mesh(terrainGeo, terrainMat);
terrain.castShadow = true;
terrain.receiveShadow = true;
scene.add(terrain);
// Current and target heightfields for smooth interpolation
let currentHeights = null;
let targetHeights = null;
let currentColors = null;
let targetColors = null;
let lerpProgress = 1.0; // 1.0 = fully at target
const LERP_SPEED = 0.12;
function applyTerrainVariant(t) {
  const variant = computeTerrainVariant(t);
  targetHeights = variant.heightData;
  targetColors = variant.colorData;
  lerpProgress = 0.0; // Start interpolation toward new target
}
// === RIVER SYSTEM ===
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const riverCache = new Map(); // timestep -> THREE.Group
function traceDownhill(errData, revData, startI, startJ) {
  // Follow negative terrain gradient from error hotspot
  const path = [];
  let ci = startI, cj = startJ;
  const visited = new Set();
  const maxSteps = 60;
  for (let s = 0; s < maxSteps; s++) {
    if (ci < 0 || ci >= GRID || cj < 0 || cj >= GRID) break;
    const key = ci * GRID + cj;
    if (visited.has(key)) break;
    visited.add(key);
    const h = revData[key];
    const x = (cj / GRID - 0.5) * SIZE;
    const z = (ci / GRID - 0.5) * SIZE;
    const y = (h / 100) * MAX_HEIGHT + 0.08; // Slightly above terrain
    path.push(new THREE.Vector3(x, y, z));
    // Find steepest downhill neighbor
    let bestDi = 0, bestDj = 0, bestDrop = -Infinity;
    for (let di = -1; di <= 1; di++) {
      for (let dj = -1; dj <= 1; dj++) {
        if (di === 0 && dj === 0) continue;
        const ni = ci + di, nj = cj + dj;
        if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
        const drop = h - revData[ni * GRID + nj];
        if (drop > bestDrop) { bestDrop = drop; bestDi = di; bestDj = dj; }
      }
    }
    if (bestDrop <= 0) break; // Local minimum reached
    ci += bestDi;
    cj += bestDj;
  }
  return path;
}
function findErrorHotspots(errData, count) {
  // Find top-N error locations
  const spots = [];
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      spots.push({ i, j, v: errData[i * GRID + j] });
    }
  }
  spots.sort((a, b) => b.v - a.v);
  // Filter: only spots above threshold, with minimum spatial separation
  const selected = [];
  for (const s of spots) {
    if (s.v < 20) break;
    if (selected.length >= count) break;
    let tooClose = false;
    for (const sel of selected) {
      const dist = Math.hypot(s.i - sel.i, s.j - sel.j);
      if (dist < 12) { tooClose = true; break; }
    }
    if (!tooClose) selected.push(s);
  }
  return selected;
}
function buildRivers(t) {
  if (riverCache.has(t)) {
    cacheStats.riverHits++;
    return riverCache.get(t);
  }
  cacheStats.riverMisses++;
  const group = new THREE.Group();
  const errData = data.errors[t];
  const revData = data.revenue[t];
  const hotspots = findErrorHotspots(errData, RIVER_COUNT);
  const riverMat = new THREE.MeshStandardMaterial({
    color: 0xcc3322, roughness: 0.35, metalness: 0.3, emissive: 0x330808, emissiveIntensity: 0.5,
  });
  for (const hs of hotspots) {
    const path = traceDownhill(errData, revData, hs.i, hs.j);
    if (path.length < 3) continue;
    const curve = new THREE.CatmullRomCurve3(path, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, 40, 0.08, 6, false);
    const tube = new THREE.Mesh(tubeGeo, riverMat);
    tube.castShadow = true;
    tube.receiveShadow = true;
    group.add(tube);
    // Small glow sphere at river source
    const srcGeo = new THREE.SphereGeometry(0.18, 8, 8);
    const srcMat = new THREE.MeshStandardMaterial({ color: 0xff4422, emissive: 0x661100, emissiveIntensity: 0.8 });
    const srcMesh = new THREE.Mesh(srcGeo, srcMat);
    srcMesh.position.copy(path[0]);
    group.add(srcMesh);
  }
  riverCache.set(t, group);
  return group;
}
function applyRivers(t) {
  // Clear current rivers
  while (riverGroup.children.length > 0) {
    riverGroup.remove(riverGroup.children[0]);
  }
  const newGroup = buildRivers(t);
  // Clone children into persistent group (avoid Three.js parent conflicts)
  for (const child of [...newGroup.children]) {
    riverGroup.add(child);
  }
}
// === PARTICLE SYSTEM ===
const particleGroup = new THREE.Group();
scene.add(particleGroup);
const particleDataCache = new Map(); // timestep -> { positions, velocities }
function buildParticles(t) {
  if (particleDataCache.has(t)) {
    cacheStats.particleHits++;
    return particleDataCache.get(t);
  }
  cacheStats.particleMisses++;
  const flows = data.apiFlows[t];
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const velocities = new Float32Array(PARTICLE_COUNT * 3);
  // Distribute particles across active flows
  let pi = 0;
  const totalVol = flows.reduce((s, f) => s + f.volume, 0) || 1;
  for (const flow of flows) {
    const count = Math.max(1, Math.floor((flow.volume / totalVol) * PARTICLE_COUNT));
    for (let c = 0; c < count && pi < PARTICLE_COUNT; c++, pi++) {
      // Random position along flow path
      const tr = Math.random();
      const fx = lerp(flow.from.x, flow.to.x, tr);
      const fy = lerp(flow.from.y, flow.to.y, tr);
      const wx = (fx - 0.5) * SIZE;
      const wz = (fy - 0.5) * SIZE;
      // Sample terrain height at position
      const gi = clamp(Math.floor(fy * GRID), 0, GRID - 1);
      const gj = clamp(Math.floor(fx * GRID), 0, GRID - 1);
      const h = data.revenue[t][gi * GRID + gj];
      const wy = (h / 100) * MAX_HEIGHT + 0.3 + Math.random() * 0.8;
      positions[pi * 3] = wx;
      positions[pi * 3 + 1] = wy;
      positions[pi * 3 + 2] = wz;
      // Velocity toward destination at slightly different speeds
      const dx = (flow.to.x - flow.from.x) * SIZE;
      const dz = (flow.to.y - flow.from.y) * SIZE;
      const speed = 0.3 + Math.random() * 0.7;
      const mag = Math.hypot(dx, dz) || 1;
      velocities[pi * 3] = (dx / mag) * speed;
      velocities[pi * 3 + 1] = (Math.random() - 0.5) * 0.15;
      velocities[pi * 3 + 2] = (dz / mag) * speed;
    }
  }
  // Fill remaining slots with random positions
  for (; pi < PARTICLE_COUNT; pi++) {
    positions[pi * 3] = (Math.random() - 0.5) * SIZE * 0.8;
    positions[pi * 3 + 1] = Math.random() * 4;
    positions[pi * 3 + 2] = (Math.random() - 0.5) * SIZE * 0.8;
    velocities[pi * 3] = (Math.random() - 0.5) * 0.5;
    velocities[pi * 3 + 1] = (Math.random() - 0.5) * 0.2;
    velocities[pi * 3 + 2] = (Math.random() - 0.5) * 0.5;
  }
  const entry = { positions, velocities };
  particleDataCache.set(t, entry);
  return entry;
}
// Single particle geometry, reused every frame
const particleGeo = new THREE.BufferGeometry();
const particlePosArr = new Float32Array(PARTICLE_COUNT * 3);
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePosArr, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.15, color: 0x88ccff, blending: THREE.AdditiveBlending,
  depthWrite: false, transparent: true, opacity: 0.8,
});
const particles = new THREE.Points(particleGeo, particleMat);
particleGroup.add(particles);
let particleData = null;
let particleFlowsRef = null; // Reference flows for respawning
function applyParticles(t) {
  const pd = buildParticles(t);
  particleData = pd;
  particleFlowsRef = data.apiFlows[t];
  // Initialize particle positions from cache
  particlePosArr.set(pd.positions);
  particleGeo.attributes.position.needsUpdate = true;
}
function updateParticles(dt, t) {
  if (!particleData) return;
  const pos = particleGeo.attributes.position.array;
  const vel = particleData.velocities;
  const dtClamped = Math.min(dt, 0.1); // Cap dt for stability
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    pos[i * 3] += vel[i * 3] * dtClamped;
    pos[i * 3 + 1] += vel[i * 3 + 1] * dtClamped;
    pos[i * 3 + 2] += vel[i * 3 + 2] * dtClamped;
    // Wrap particles that leave bounds
    if (Math.abs(pos[i * 3]) > HALF + 1 || Math.abs(pos[i * 3 + 2]) > HALF + 1
        || pos[i * 3 + 1] < 0 || pos[i * 3 + 1] > MAX_HEIGHT + 2) {
      // Respawn near a random active flow source
      const flows = particleFlowsRef;
      if (flows && flows.length > 0) {
        const f = flows[Math.floor(Math.random() * flows.length)];
        pos[i * 3] = (f.from.x - 0.5) * SIZE + (Math.random() - 0.5) * 2;
        pos[i * 3 + 1] = 0.5 + Math.random() * 2;
        pos[i * 3 + 2] = (f.from.y - 0.5) * SIZE + (Math.random() - 0.5) * 2;
      } else {
        pos[i * 3] = (Math.random() - 0.5) * SIZE;
        pos[i * 3 + 1] = Math.random() * 4;
        pos[i * 3 + 2] = (Math.random() - 0.5) * SIZE;
      }
    }
    // Gentle vertical oscillation
    pos[i * 3 + 1] += Math.sin(Date.now() * 0.004 + i * 0.7) * dtClamped * 0.2;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// === TIME SLIDER LOGIC ===
const slider = document.getElementById('slider');
const tlabel = document.getElementById('tlabel');
const autoplayBtn = document.getElementById('autoplay');
let currentStep = 12;
let autoPlaying = false;
let debounceTimer = null;
function formatHour(t) {
  return String(t).padStart(2, '0') + ':00';
}
function setTimeStep(t, immediate = false) {
  t = clamp(t, 0, TIMESTEPS - 1);
  if (t === currentStep && lerpProgress >= 1.0) return;
  currentStep = t;
  slider.value = t;
  tlabel.textContent = formatHour(t);
  document.getElementById('curStep').textContent = t;
  // Debounce river rebuild (expensive TubeGeometry construction)
  if (debounceTimer) clearTimeout(debounceTimer);
  if (immediate) {
    applyRivers(t);
    applyParticles(t);
  } else {
    // Terrain updates immediately (smooth interpolation handles visual)
    applyTerrainVariant(t);
    debounceTimer = setTimeout(() => {
      applyRivers(t);
      applyParticles(t);
      debounceTimer = null;
    }, DEBOUNCE_MS);
    // But still update terrain reference immediately
    if (immediate) applyTerrainVariant(t);
    else applyTerrainVariant(t);
  }
}
slider.addEventListener('input', () => {
  setTimeStep(parseInt(slider.value));
});
autoplayBtn.addEventListener('click', () => {
  autoPlaying = !autoPlaying;
  autoplayBtn.textContent = autoPlaying ? 'Pause' : 'Play';
  autoplayBtn.style.background = autoPlaying ? 'rgba(79,195,247,0.2)' : 'rgba(255,255,255,0.1)';
});
// === CAMERA BOOKMARKS ===
const bookmarks = {
  overview:   { pos: [8, 14, 18],    target: [0, 3, 0] },
  peak1:      { pos: [5, 9, 3],      target: [1.5, 6, -1.5] },
  river:      { pos: [-2, 5, -4],    target: [-3, 1.5, -3] },
  valley:     { pos: [-10, 12, -8],  target: [0, 1, 0] },
};
function animateCamera(posArr, tgtArr) {
  const startPos = camera.position.clone();
  const startTgt = controls.target.clone();
  const endPos = new THREE.Vector3(...posArr);
  const endTgt = new THREE.Vector3(...tgtArr);
  const duration = 800; // ms
  const startTime = performance.now();
  function step(now) {
    const elapsed = now - startTime;
    const tEased = Math.min(1, elapsed / duration);
    // Ease in-out cubic
    const t = tEased < 0.5 ? 4 * tEased * tEased * tEased
      : 1 - Math.pow(-2 * tEased + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, t);
    controls.target.lerpVectors(startTgt, endTgt, t);
    controls.update();
    if (tEased < 1) {
      requestAnimationFrame(step);
    }
  }
  requestAnimationFrame(step);
}
document.getElementById('bookmarks').addEventListener('click', (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;
  const bm = bookmarks[btn.dataset.bm];
  if (bm) {
    controls.autoRotate = false;
    animateCamera(bm.pos, bm.target);
    // Re-enable auto-rotate after 4 seconds
    setTimeout(() => { controls.autoRotate = true; }, 4000);
  }
});
// === CACHE DIAGNOSTICS ===
const cacheStats = {
  terrainHits: 0, terrainMisses: 0,
  riverHits: 0, riverMisses: 0,
  particleHits: 0, particleMisses: 0,
};
function updateDiagnostics(fps) {
  document.getElementById('fpsV').textContent = fps;
  document.getElementById('tHit').textContent = cacheStats.terrainHits;
  document.getElementById('tMiss').textContent = cacheStats.terrainMisses;
  document.getElementById('rHit').textContent = cacheStats.riverHits;
  document.getElementById('rMiss').textContent = cacheStats.riverMisses;
}
// === TOOLTIP (world-to-grid coordinate memoization) ===
const tooltip = document.getElementById('tooltip');
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let lastGridQuery = null; // Memoized: { screenX, screenY, result }
const GRID_MEMO_TTL = 500; // ms
canvas.addEventListener('mousemove', (e) => {
  const now = performance.now();
  // Memoize: skip raycast if mouse hasn't moved significantly
  if (lastGridQuery && Math.abs(e.clientX - lastGridQuery.screenX) < 3
      && Math.abs(e.clientY - lastGridQuery.screenY) < 3
      && now - lastGridQuery.time < GRID_MEMO_TTL) {
    return; // Use memoized result
  }
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObject(terrain);
  if (hits.length > 0) {
    const p = hits[0].point;
    // Convert world position to grid coordinates
    const gx = Math.floor((p.x / SIZE + 0.5) * GRID);
    const gz = Math.floor((p.z / SIZE + 0.5) * GRID);
    if (gx >= 0 && gx < GRID && gz >= 0 && gz < GRID) {
      const rev = data.revenue[currentStep][gz * GRID + gx];
      const usr = data.users[currentStep][gz * GRID + gx];
      const err = data.errors[currentStep][gz * GRID + gx];
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 18) + 'px';
      tooltip.style.top = (e.clientY - 12) + 'px';
      tooltip.textContent = `Revenue: ${rev.toFixed(0)} | Users: ${usr.toFixed(0)} | Errors: ${err.toFixed(0)}`;
      lastGridQuery = { screenX: e.clientX, screenY: e.clientY, time: now, result: true };
    } else {
      tooltip.style.display = 'none';
    }
  } else {
    tooltip.style.display = 'none';
  }
});
canvas.addEventListener('mouseleave', () => {
  tooltip.style.display = 'none';
  lastGridQuery = null;
});
// === ANIMATION LOOP ===
let lastTime = performance.now();
let fpsCounter = 0, fpsTime = 0, currentFPS = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  const dt = (timestamp - lastTime) / 1000;
  lastTime = timestamp;
  // FPS counter
  fpsCounter++;
  fpsTime += dt;
  if (fpsTime >= 1.0) {
    currentFPS = Math.round(fpsCounter / fpsTime);
    fpsCounter = 0;
    fpsTime = 0;
    updateDiagnostics(currentFPS);
  }
  // Auto-play
  if (autoPlaying && lerpProgress >= 0.95) {
    const next = (currentStep + 1) % TIMESTEPS;
    setTimeStep(next);
  }
  // Smooth terrain interpolation between current and target heightfields
  if (targetHeights && currentHeights && lerpProgress < 1.0) {
    lerpProgress = Math.min(1.0, lerpProgress + LERP_SPEED);
    const posArr = terrainGeo.attributes.position.array;
    const count = posArr.length / 3;
    // Interpolate height (Y component, index 1 in each vertex triple)
    for (let i = 0; i < count; i++) {
      posArr[i * 3 + 1] = lerp(currentHeights[i], targetHeights[i], lerpProgress);
    }
    terrainGeo.attributes.position.needsUpdate = true;
    terrainGeo.computeVertexNormals();
    // Interpolate vertex colors
    if (targetColors && currentColors) {
      const colArr = terrainGeo.attributes.color.array;
      for (let i = 0; i < colArr.length; i++) {
        colArr[i] = lerp(currentColors[i], targetColors[i], lerpProgress);
      }
      terrainGeo.attributes.color.needsUpdate = true;
    }
    // On completion, current becomes the completed target
    if (lerpProgress >= 1.0) {
      currentHeights = new Float32Array(targetHeights);
      currentColors = new Float32Array(targetColors);
    }
  }
  // Update particles
  updateParticles(dt, currentStep);
  // Update controls
  controls.update();
  // Render
  renderer.render(scene, camera);
}
// === RESIZE HANDLER ===
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// === KEYBOARD SHORTCUTS ===
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r': // Reset camera
      controls.autoRotate = true;
      animateCamera(bookmarks.overview.pos, bookmarks.overview.target);
      break;
    case ' ': // Toggle auto-rotate
      e.preventDefault();
      controls.autoRotate = !controls.autoRotate;
      break;
    case 'arrowleft':
      setTimeStep(currentStep - 1);
      break;
    case 'arrowright':
      setTimeStep(currentStep + 1);
      break;
  }
});
// === CLEANUP / TEARDOWN HOOK ===
function cleanup() {
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = null;
  autoPlaying = false;
  // Clear caches to free memory
  terrainCache.clear();
  riverCache.clear();
  particleDataCache.clear();
  cacheStats.terrainHits = 0; cacheStats.terrainMisses = 0;
  cacheStats.riverHits = 0; cacheStats.riverMisses = 0;
  cacheStats.particleHits = 0; cacheStats.particleMisses = 0;
  lastGridQuery = null;
}
// Expose cleanup for external lifecycle management
window.__terrainExplorerCleanup = cleanup;
// Before unload, run cleanup
window.addEventListener('beforeunload', cleanup);
// === INIT ===
function init() {
  // Build initial terrain variant
  const variant = computeTerrainVariant(currentStep);
  currentHeights = new Float32Array(variant.heightData);
  targetHeights = new Float32Array(variant.heightData);
  currentColors = new Float32Array(variant.colorData);
  targetColors = new Float32Array(variant.colorData);
  lerpProgress = 1.0;
  // Apply heights to terrain geometry
  const posArr = terrainGeo.attributes.position.array;
  for (let i = 0; i < currentHeights.length; i++) {
    posArr[i * 3 + 1] = currentHeights[i];
  }
  terrainGeo.attributes.position.needsUpdate = true;
  // Apply vertex colors
  terrainGeo.setAttribute('color', new THREE.BufferAttribute(currentColors, 3));
  terrainGeo.computeVertexNormals();
  // Build rivers and particles
  applyRivers(currentStep);
  applyParticles(currentStep);
  // Set slider
  slider.value = currentStep;
  tlabel.textContent = formatHour(currentStep);
  // Start animation
  requestAnimationFrame(animate);
}
init();
</script></body></html>