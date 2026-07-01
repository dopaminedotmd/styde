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
  #ui{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:12px;align-items:center}
  #time-slider{width:400px;accent-color:#4fc3f7}
  #time-label{color:#ccc;font-size:13px;min-width:80px;text-align:center}
  #bookmarks{position:fixed;top:20px;left:20px;z-index:10;display:flex;gap:6px}
  #bookmarks button{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#aaa;width:36px;height:36px;border-radius:6px;cursor:pointer;font-size:13px;transition:all 0.2s}
  #bookmarks button:hover{background:rgba(255,255,255,0.16);color:#fff}
  #bookmarks button.saved{background:rgba(79,195,247,0.25);border-color:#4fc3f7;color:#4fc3f7}
  #diag{position:fixed;top:20px;right:20px;z-index:10;background:rgba(0,0,0,0.7);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:12px 16px;color:#aaa;font-size:11px;line-height:1.7;min-width:180px;backdrop-filter:blur(6px)}
  #diag .label{color:#888}
  #diag .val{color:#ddd;font-variant-numeric:tabular-nums}
  #diag .hit{color:#66bb6a}
  #diag .miss{color:#ef5350}
  #diag .warn{color:#ff9800}
  #legend{position:fixed;bottom:20px;right:20px;z-index:10;display:flex;gap:16px;color:#888;font-size:11px}
  #legend span{display:flex;align-items:center;gap:5px}
  #legend .swatch{width:12px;height:12px;border-radius:3px}
  #auto-rotate-btn{position:fixed;top:20px;left:230px;z-index:10;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#aaa;padding:8px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.2s}
  #auto-rotate-btn:hover{color:#fff;background:rgba(255,255,255,0.14)}
  #auto-rotate-btn.active{background:rgba(79,195,247,0.25);border-color:#4fc3f7;color:#4fc3f7}
</style>
</head>
<body>
<div id="bookmarks">
  <button data-idx="0" title="Shift+1: save | 1: restore">1</button>
  <button data-idx="1" title="Shift+2: save | 2: restore">2</button>
  <button data-idx="2" title="Shift+3: save | 3: restore">3</button>
  <button data-idx="3" title="Shift+4: save | 4: restore">4</button>
  <button data-idx="4" title="Shift+5: save | 5: restore">5</button>
</div>
<button id="auto-rotate-btn" class="active" title="Toggle auto-rotation">AUTO</button>
<div id="diag">
  <div><span class="label">Time slice</span> <span id="d-time" class="val">6</span></div>
  <div><span class="label">FPS</span> <span id="d-fps" class="val">--</span></div>
  <div><span class="label">Terrain cache</span> <span id="d-t-hit" class="hit">0</span>/<span id="d-t-miss" class="miss">0</span></div>
  <div><span class="label">Particles</span> <span id="d-particles" class="val">0</span></div>
  <div><span class="label">Vertices</span> <span id="d-verts" class="val">0</span></div>
</div>
<div id="ui">
  <span id="time-label">Month 6</span>
  <input type="range" id="time-slider" min="0" max="11" value="5" step="0.01">
</div>
<div id="legend">
  <span><span class="swatch" style="background:#4caf50"></span> Revenue (height)</span>
  <span><span class="swatch" style="background:#ef5350"></span> Anomalies (rivers)</span>
  <span><span class="swatch" style="background:#4fc3f7"></span> API flow (particles)</span>
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
// ─── noise: simple 2D value noise (no external deps) ───
const NOISE_SIZE = 256;
const noiseBuf = new Float32Array(NOISE_SIZE * NOISE_SIZE);
for (let i = 0; i < NOISE_SIZE * NOISE_SIZE; i++) noiseBuf[i] = Math.random();
function noise2D(x, y) {
  const ix = Math.floor(x) & (NOISE_SIZE - 1);
  const iy = Math.floor(y) & (NOISE_SIZE - 1);
  return noiseBuf[ix + iy * NOISE_SIZE];
}
function smoothNoise(x, y) {
  const fx = x - Math.floor(x), fy = y - Math.floor(y);
  const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
  const n00 = noise2D(x, y), n10 = noise2D(x + 1, y);
  const n01 = noise2D(x, y + 1), n11 = noise2D(x + 1, y + 1);
  return n00 + (n10 - n00) * sx + (n01 - n00) * sy + (n11 - n10 - n01 + n00) * sx * sy;
}
function fbm(x, y, octaves = 4) {
  let v = 0, amp = 0.6, freq = 1, total = 0;
  for (let i = 0; i < octaves; i++) {
    v += smoothNoise(x * freq, y * freq) * amp;
    total += amp;
    amp *= 0.5;
    freq *= 2.0;
  }
  return v / total;
}
// ─── DATA STORE: 12 time slices, 64x64 grid ───
const GRID = 64;
const SLICES = 12;
const dataSlices = []; // Array<{heights:Float32Array, veg:Float32Array, anomaly:Float32Array}>
function generateSlice(t) {
  const phase = t / SLICES * Math.PI * 2;
  const h = new Float32Array(GRID * GRID);
  const veg = new Float32Array(GRID * GRID);
  const anom = new Float32Array(GRID * GRID);
  // Revenue clusters that shift over time
  const cx1 = 0.3 + Math.cos(phase) * 0.15;
  const cy1 = 0.5 + Math.sin(phase * 1.3) * 0.2;
  const cx2 = 0.7 + Math.cos(phase * 0.7 + 1) * 0.15;
  const cy2 = 0.3 + Math.sin(phase * 1.1 + 0.5) * 0.2;
  for (let iy = 0; iy < GRID; iy++) {
    const ny = iy / (GRID - 1);
    for (let ix = 0; ix < GRID; ix++) {
      const nx = ix / (GRID - 1);
      const idx = ix + iy * GRID;
      // Base terrain from FBM noise
      let elev = fbm(nx * 8, ny * 8, 4) * 0.4;
      // Revenue hills (time-varying Gaussian bumps)
      const d1 = ((nx - cx1) ** 2 + (ny - cy1) ** 2);
      const d2 = ((nx - cx2) ** 2 + (ny - cy2) ** 2);
      elev += Math.exp(-d1 * 12) * 0.5;
      elev += Math.exp(-d2 * 20) * 0.35;
      // Edge depression (natural boundary)
      const edgeFade = Math.min(nx, 1 - nx, ny, 1 - ny) * 6;
      elev *= Math.min(1, edgeFade);
      h[idx] = Math.max(0, elev);
      // Vegetation (user density): correlated with height + own noise
      veg[idx] = Math.min(1, Math.max(0, elev * 1.2 + fbm(nx * 6 + 3, ny * 6 + 3, 3) * 0.3));
      // Anomalies: error clusters that carve rivers
      const anomalyNoise = fbm(nx * 5 + phase, ny * 5 - phase, 3);
      // Shift anomaly hot zones over time
      const ax = 0.25 + Math.cos(phase * 0.8 + 2) * 0.2;
      const ay = 0.4 + Math.sin(phase * 0.9) * 0.25;
      const ad = ((nx - ax) ** 2 + (ny - ay) ** 2);
      const anomalyStrength = Math.exp(-ad * 30) * 0.8 + anomalyNoise * 0.2;
      anom[idx] = anomalyStrength > 0.55 ? (anomalyStrength - 0.55) / 0.45 : 0;
    }
  }
  return { heights: h, veg, anomaly: anom };
}
for (let t = 0; t < SLICES; t++) dataSlices.push(generateSlice(t));
// ─── TERRAIN CACHE ───
const terrainCache = new Map(); // timeIndex -> {positions:Float32Array, colors:Float32Array}
let cacheHits = 0, cacheMisses = 0;
function buildTerrainVariant(tIdx) {
  const slice = dataSlices[tIdx];
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const gridSpacing = 8 / (GRID - 1);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = ix + iy * GRID;
      const i3 = idx * 3;
      const x = (ix - GRID / 2) * gridSpacing;
      const z = (iy - GRID / 2) * gridSpacing;
      // Height: revenue elevated, anomalies carved down
      let height = slice.heights[idx] * 5;
      const anom = slice.anomaly[idx];
      if (anom > 0.05) {
        // Carve river: depress terrain proportionally to anomaly strength
        height -= anom * 1.5;
      }
      positions[i3] = x;
      positions[i3 + 1] = Math.max(0, height);
      positions[i3 + 2] = z;
      // Color: vegetation gradient base, red overlay for anomalies
      const veg = slice.veg[idx];
      if (anom > 0.1) {
        // Blend from green to red based on anomaly strength
        const a = Math.min(1, anom * 1.5);
        colors[i3] = 0.2 + a * 0.7;     // R
        colors[i3 + 1] = veg * (1 - a);  // G
        colors[i3 + 2] = 0.05;           // B
      } else {
        // Vegetation: dark green (low) to bright green/yellow (high)
        colors[i3] = veg * 0.3;
        colors[i3 + 1] = 0.2 + veg * 0.7;
        colors[i3 + 2] = veg * 0.15;
      }
    }
  }
  return { positions, colors };
}
function getTerrainVariant(tIdx) {
  if (terrainCache.has(tIdx)) {
    cacheHits++;
    return terrainCache.get(tIdx);
  }
  cacheMisses++;
  const variant = buildTerrainVariant(tIdx);
  terrainCache.set(tIdx, variant);
  return variant;
}
// ─── THREE.JS SETUP ───
const container = document.body;
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 15, 40);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 60);
camera.position.set(8, 7, 10);
camera.lookAt(0, 2, 0);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 2.2, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 3;
controls.maxDistance = 22;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// ─── LIGHTING ───
const ambientLight = new THREE.AmbientLight(0x303050, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4);
sunLight.position.set(10, 15, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 50;
sunLight.shadow.camera.left = -15;
sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15;
sunLight.shadow.camera.bottom = -15;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4488cc, 1.5);
fillLight.position.set(-4, 2, -6);
scene.add(fillLight);
// ─── GRID HELPER ───
const gridHelper = new THREE.GridHelper(8, 32, 0x333355, 0x1a1a2e);
gridHelper.position.y = -0.02;
scene.add(gridHelper);
// ─── TERRAIN MESH ───
const terrainGeo = new THREE.BufferGeometry();
const posAttr = new THREE.BufferAttribute(new Float32Array(GRID * GRID * 3), 3);
const colAttr = new THREE.BufferAttribute(new Float32Array(GRID * GRID * 3), 3);
terrainGeo.setAttribute('position', posAttr);
terrainGeo.setAttribute('color', colAttr);
// Build index buffer for the grid (two triangles per cell)
const indices = [];
for (let iy = 0; iy < GRID - 1; iy++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = ix + iy * GRID;
    const b = ix + 1 + iy * GRID;
    const c = ix + (iy + 1) * GRID;
    const d = ix + 1 + (iy + 1) * GRID;
    indices.push(a, b, c, b, d, c);
  }
}
terrainGeo.setIndex(indices);
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ─── PARTICLE SYSTEM ───
const PARTICLE_COUNT = 400;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3); // reused every frame
const particleSizes = new Float32Array(PARTICLE_COUNT);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
// Pre-compute particle paths across the terrain
// Each particle: { path: [{ix,iy}], progress: 0..1, speed: float }
const particlePaths = [];
const gridSpacing = 8 / (GRID - 1);
function createFlowPath() {
  // Start from a random edge point, flow downhill toward center valleys
  const side = Math.floor(Math.random() * 4);
  let ix, iy;
  if (side === 0) { ix = Math.floor(Math.random() * GRID); iy = 0; }
  else if (side === 1) { ix = GRID - 1; iy = Math.floor(Math.random() * GRID); }
  else if (side === 2) { ix = Math.floor(Math.random() * GRID); iy = GRID - 1; }
  else { ix = 0; iy = Math.floor(Math.random() * GRID); }
  const path = [];
  const visited = new Set();
  const maxSteps = 80;
  let cx = ix, cy = iy;
  for (let step = 0; step < maxSteps; step++) {
    const key = cx + cy * GRID;
    if (visited.has(key)) break;
    visited.add(key);
    path.push({ ix: cx, iy: cy });
    // Find steepest downhill neighbor
    const slice = dataSlices[0]; // flow paths use base terrain shape
    const ch = slice.heights[cx + cy * GRID];
    let bestDz = 0, bestNx = cx, bestNy = cy;
    for (const [dx, dy] of [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[1,-1],[-1,1],[1,1]]) {
      const nx = cx + dx, ny = cy + dy;
      if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
      const nh = slice.heights[nx + ny * GRID];
      const dz = ch - nh;
      if (dz > bestDz) { bestDz = dz; bestNx = nx; bestNy = ny; }
    }
    if (bestDz <= 0.001) break; // reached local minimum
    cx = bestNx;
    cy = bestNy;
  }
  return path;
}
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const path = createFlowPath();
  if (path.length < 2) {
    // Fallback: simple linear path
    particlePaths.push({ path: [{ix:0,iy:0},{ix:GRID-1,iy:GRID-1}], progress: Math.random(), speed: 0.02 + Math.random() * 0.06 });
  } else {
    particlePaths.push({
      path,
      progress: Math.random(),
      speed: 0.02 + Math.random() * 0.06,
    });
  }
  particleSizes[i] = 1.2 + Math.random() * 2.5;
}
const particleMat = new THREE.PointsMaterial({
  color: 0x4fc3f7,
  size: 0.08,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.75,
  sizeAttenuation: true,
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
scene.add(particleSystem);
// ─── CAMERA BOOKMARKS ───
const bookmarks = new Array(5).fill(null); // {position:Vector3, target:Vector3}
const bookmarkBtns = document.querySelectorAll('#bookmarks button');
function saveBookmark(idx) {
  bookmarks[idx] = {
    position: camera.position.clone(),
    target: controls.target.clone(),
  };
  bookmarkBtns[idx].classList.add('saved');
}
function restoreBookmark(idx) {
  const bm = bookmarks[idx];
  if (!bm) return;
  // Smooth animate to bookmark
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.position.clone();
  const endTarget = bm.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function animBookmark(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animBookmark);
  }
  requestAnimationFrame(animBookmark);
}
// ─── TIME SLIDER ───
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
let currentSliceFloat = 5.0;
let displaySlice = 5; // integer slice index for cached terrain
function updateTerrainDisplay(tFloat) {
  const t0 = Math.floor(tFloat);
  const t1 = Math.min(SLICES - 1, t0 + 1);
  const frac = tFloat - t0;
  const v0 = getTerrainVariant(t0);
  const v1 = getTerrainVariant(t1);
  // Interpolate positions and colors between cached variants
  const pArr = posAttr.array;
  const cArr = colAttr.array;
  const p0 = v0.positions;
  const p1 = v1.positions;
  const c0 = v0.colors;
  const c1 = v1.colors;
  for (let i = 0; i < pArr.length; i++) {
    pArr[i] = p0[i] + (p1[i] - p0[i]) * frac;
    cArr[i] = c0[i] + (c1[i] - c0[i]) * frac;
  }
  posAttr.needsUpdate = true;
  colAttr.needsUpdate = true;
  terrainGeo.computeVertexNormals();
}
slider.addEventListener('input', () => {
  currentSliceFloat = parseFloat(slider.value);
  updateTerrainDisplay(currentSliceFloat);
  const displayMonth = Math.round(currentSliceFloat) + 1;
  timeLabel.textContent = `Month ${displayMonth}`;
  document.getElementById('d-time').textContent = displayMonth;
});
// Initial terrain load
updateTerrainDisplay(5.0);
// ─── AUTO-ROTATE TOGGLE ───
const autoRotateBtn = document.getElementById('auto-rotate-btn');
autoRotateBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autoRotateBtn.classList.toggle('active', controls.autoRotate);
});
// ─── KEYBOARD SHORTCUTS ───
window.addEventListener('keydown', (e) => {
  const key = parseInt(e.key);
  if (isNaN(key) || key < 1 || key > 5) return;
  const idx = key - 1;
  if (e.shiftKey) {
    saveBookmark(idx);
  } else {
    restoreBookmark(idx);
  }
});
// ─── DIAGNOSTIC PANEL UPDATES ───
const diagTime = document.getElementById('d-time');
const diagFps = document.getElementById('d-fps');
const diagTHit = document.getElementById('d-t-hit');
const diagTMiss = document.getElementById('d-t-miss');
const diagParticles = document.getElementById('d-particles');
const diagVerts = document.getElementById('d-verts');
diagParticles.textContent = PARTICLE_COUNT;
diagVerts.textContent = (GRID * GRID).toLocaleString();
// FPS tracking
let frameCount = 0, lastFpsTime = performance.now(), currentFps = 0;
// ─── RENDER LOOP ───
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  // Update particles: advance each along its pre-computed path
  const pArr = particleGeo.attributes.position.array;
  const currentSliceIdx = Math.round(currentSliceFloat);
  const slice = dataSlices[currentSliceIdx];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pp = particlePaths[i];
    pp.progress += pp.speed * 0.016; // frame-rate independent approximation
    if (pp.progress > 1) pp.progress -= 1;
    const pathLen = pp.path.length;
    const rawIdx = pp.progress * (pathLen - 1);
    const segIdx = Math.floor(rawIdx);
    const segFrac = rawIdx - segIdx;
    const s0 = pp.path[Math.min(segIdx, pathLen - 1)];
    const s1 = pp.path[Math.min(segIdx + 1, pathLen - 1)];
    // Interpolate grid position
    const gx = s0.ix + (s1.ix - s0.ix) * segFrac;
    const gy = s0.iy + (s1.iy - s0.iy) * segFrac;
    // World position
    const wx = (gx - GRID / 2) * gridSpacing;
    const wz = (gy - GRID / 2) * gridSpacing;
    // Sample terrain height at this position
    const gi = Math.round(gx), gj = Math.round(gy);
    const clampedI = Math.max(0, Math.min(GRID - 1, gi));
    const clampedJ = Math.max(0, Math.min(GRID - 1, gj));
    const hIdx = clampedI + clampedJ * GRID;
    let terrainH = slice.heights[hIdx] * 5;
    if (slice.anomaly[hIdx] > 0.05) terrainH -= slice.anomaly[hIdx] * 1.5;
    terrainH = Math.max(0, terrainH);
    const i3 = i * 3;
    pArr[i3] = wx;
    pArr[i3 + 1] = terrainH + 0.15; // float slightly above terrain
    pArr[i3 + 2] = wz;
  }
  particleGeo.attributes.position.needsUpdate = true;
  renderer.render(scene, camera);
  // FPS
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    currentFps = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    frameCount = 0;
    lastFpsTime = timestamp;
    diagFps.textContent = currentFps;
    diagTHit.textContent = cacheHits;
    diagTMiss.textContent = cacheMisses;
  }
}
// ─── RESIZE HANDLER ───
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── START ───
requestAnimationFrame(animate);
// Save default bookmark on slot 1
saveBookmark(0);
console.log(
  '3D Data Terrain Explorer ready\n' +
  'Terrain: ' + (GRID * GRID).toLocaleString() + ' vertices, ' + SLICES + ' time slices (lazy-cached)\n' +
  'Particles: ' + PARTICLE_COUNT + ' (BufferGeometry, position array reused)\n' +
  'Controls: OrbitControls | 1-5 restore bookmark | Shift+1-5 save bookmark\n' +
  'Terrain cache: lazy-build on first slider access, interpolated between adjacent slices'
);
</script>
</body>
</html>