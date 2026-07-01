<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a14; --panel-bg: rgba(10,10,20,0.92); --text: #c8ccd4; --accent: #4da6ff; --warn: #ff6b6b; --ok: #51cf66; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  #canvas-container { position:fixed; inset:0; }
  canvas { display:block; }
  #panel {
    position:fixed; bottom:20px; left:50%; transform:translateX(-50%);
    background:var(--panel-bg); border:1px solid rgba(255,255,255,0.08);
    border-radius:12px; padding:16px 24px; display:flex; gap:24px; align-items:center;
    backdrop-filter:blur(12px); z-index:10; flex-wrap:wrap; justify-content:center;
  }
  .ctrl-group { display:flex; align-items:center; gap:8px; }
  .ctrl-group label { font-size:11px; text-transform:uppercase; letter-spacing:0.8px; opacity:0.7; }
  input[type=range] { width:140px; accent-color:var(--accent); }
  button {
    background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12);
    color:var(--text); padding:6px 14px; border-radius:6px; cursor:pointer;
    font-size:12px; transition:all 0.15s;
  }
  button:hover { background:rgba(255,255,255,0.12); border-color:var(--accent); }
  button.active { background:var(--accent); color:#000; border-color:var(--accent); }
  #bookmark-bar { display:flex; gap:6px; }
  #bookmark-bar button { padding:4px 10px; font-size:10px; }
  #stats {
    position:fixed; top:16px; right:16px; background:var(--panel-bg);
    border:1px solid rgba(255,255,255,0.08); border-radius:8px;
    padding:12px 16px; font-size:11px; line-height:1.6; backdrop-filter:blur(8px); z-index:10;
  }
  #stats .metric { display:flex; justify-content:space-between; gap:24px; }
  #stats .val { font-weight:600; }
  #legend {
    position:fixed; top:16px; left:16px; background:var(--panel-bg);
    border:1px solid rgba(255,255,255,0.08); border-radius:8px;
    padding:12px; font-size:10px; backdrop-filter:blur(8px); z-index:10;
    display:flex; flex-direction:column; gap:4px;
  }
  .legend-item { display:flex; align-items:center; gap:8px; }
  .legend-swatch { width:24px; height:3px; border-radius:2px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="legend">
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(to right,#1a3a1a,#4dff4d);"></span> User Density (vegetation)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(to right,#004466,#00ccff);"></span> Elevation = Revenue</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ff4444;"></span> Error Rivers</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ffdd44;"></span> API Trails</div>
</div>
<div id="stats">
  <div class="metric"><span>Time Step</span><span class="val" id="stat-time">0 / 99</span></div>
  <div class="metric"><span>Revenue Peak</span><span class="val" id="stat-rev">--</span></div>
  <div class="metric"><span>Users</span><span class="val" id="stat-users">--</span></div>
  <div class="metric"><span>Error Rate</span><span class="val" id="stat-err">--</span></div>
  <div class="metric"><span>API Calls/s</span><span class="val" id="stat-api">--</span></div>
  <div class="metric"><span>FPS</span><span class="val" id="stat-fps">--</span></div>
</div>
<div id="panel">
  <div class="ctrl-group">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label" style="font-size:12px;min-width:40px;">T0</span>
  </div>
  <button id="btn-play" title="Auto-play through time">Play</button>
  <button id="btn-auto-rotate" title="Auto-rotate camera">Rotate</button>
  <div id="bookmark-bar">
    <button data-slot="1" title="Save/restore camera bookmark 1">Cam1</button>
    <button data-slot="2" title="Save/restore camera bookmark 2">Cam2</button>
    <button data-slot="3" title="Save/restore camera bookmark 3">Cam3</button>
    <button data-slot="4" title="Save/restore camera bookmark 4">Cam4</button>
    <button data-slot="5" title="Save/restore camera bookmark 5">Cam5</button>
  </div>
  <button id="btn-reset" title="Reset camera">Reset</button>
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
// ── Synthetic data generation ─────────────────────────────────────────────
const GRID = 80;
const STEPS = 100;
const EXTENT = 12;
// Generate time-series data: [step][row][col] = {revenue, users, errors, apiCalls}
function buildDataset() {
  const data = [];
  const centers = [
    {cx:0.25, cy:0.25, rx:0.18, ry:0.15, revAmp:1.0, revFreq:0.03},
    {cx:0.65, cy:0.30, rx:0.22, ry:0.12, revAmp:0.85, revFreq:0.025},
    {cx:0.45, cy:0.60, rx:0.30, ry:0.20, revAmp:0.70, revFreq:0.02},
    {cx:0.20, cy:0.70, rx:0.15, ry:0.25, revAmp:0.55, revFreq:0.035},
    {cx:0.75, cy:0.65, rx:0.16, ry:0.18, revAmp:0.60, revFreq:0.028},
    {cx:0.55, cy:0.15, rx:0.12, ry:0.10, revAmp:0.45, revFreq:0.04},
  ];
  // Error river paths (start, end, amplitude variation over time)
  const rivers = [
    {sx:0.1, sy:0.45, ex:0.8, ey:0.55, ampBase:0.12},
    {sx:0.2, sy:0.25, ex:0.7, ey:0.75, ampBase:0.08},
    {sx:0.5, sy:0.1, ex:0.6, ey:0.5, ampBase:0.06},
  ];
  for (let t = 0; t < STEPS; t++) {
    const step = [];
    const timePhase = t * 0.06;
    for (let row = 0; row < GRID; row++) {
      const stepRow = [];
      const y = row / (GRID - 1);
      for (let col = 0; col < GRID; col++) {
        const x = col / (GRID - 1);
        // Revenue: sum of gaussian hills that pulse over time
        let revenue = 0;
        let users = 0;
        for (const c of centers) {
          const dx = (x - c.cx) / c.rx;
          const dy = (y - c.cy) / c.ry;
          const dist2 = dx * dx + dy * dy;
          const gauss = Math.exp(-dist2 * 0.5);
          const pulse = 0.7 + 0.3 * Math.sin(timePhase * c.revFreq * 60 + c.revAmp * 3);
          revenue += c.revAmp * gauss * pulse;
          users += c.revAmp * gauss * pulse * (0.6 + 0.4 * Math.cos(timePhase * 0.04 + c.revAmp));
        }
        // Error rate: rivers + noise
        let errors = 0;
        for (const r of rivers) {
          const tParam = 0.5 + 0.3 * Math.sin(timePhase * 0.05);
          const riverX = r.sx + (r.ex - r.sx) * tParam;
          const riverY = r.sy + (r.ey - r.sy) * tParam;
          const distToRiver = Math.sqrt((x - riverX) ** 2 + (y - riverY) ** 2);
          const riverWidth = 0.04 + 0.02 * Math.sin(timePhase * 2);
          if (distToRiver < riverWidth) {
            errors += r.ampBase * (1 - distToRiver / riverWidth) * (0.6 + 0.4 * Math.sin(timePhase * 3 + r.ampBase * 10));
          }
        }
        errors += 0.01 * Math.abs(Math.sin(x * 15 + timePhase) * Math.cos(y * 12 - timePhase * 0.7));
        // API calls: correlated with revenue + independent noise
        const apiCalls = revenue * 0.4 + 0.08 * Math.abs(Math.sin(x * 20 + timePhase * 1.3) * Math.cos(y * 18 + timePhase * 0.9));
        stepRow.push({ revenue: Math.max(0, revenue), users: Math.max(0, users), errors: Math.max(0, errors), apiCalls: Math.max(0, apiCalls) });
      }
      step.push(stepRow);
    }
    data.push(step);
  }
  return { data, rivers };
}
const { data: DATASET, rivers: RIVER_DEFS } = buildDataset();
// ── Three.js setup ─────────────────────────────────────────────────────────
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 15, 55);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(8, 7.5, 14);
camera.lookAt(0, 1.2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
// Lighting
const ambient = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffe8cc', 4.5);
sun.position.set(10, 18, 6);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -15;
sun.shadow.camera.right = 15;
sun.shadow.camera.top = 15;
sun.shadow.camera.bottom = -15;
sun.shadow.bias = -0.0002;
sun.shadow.normalBias = 0.02;
scene.add(sun);
const fill = new THREE.DirectionalLight('#4466aa', 1.0);
fill.position.set(-4, 2, -2);
scene.add(fill);
const rim = new THREE.DirectionalLight('#8899cc', 0.6);
rim.position.set(0, 1, -12);
scene.add(rim);
// Grid base
const gridHelper = new THREE.PolarGridHelper(EXTENT * 0.7, 40, 24, 64, '#1a1a2e', '#1a1a2e');
gridHelper.position.y = -0.15;
scene.add(gridHelper);
// ── Cached geometry objects (mutate in place, never rebuild) ───────────────
const terrainGeo = new THREE.BufferGeometry();
const SEGMENTS = GRID - 1;
const vertexCount = GRID * GRID;
const indexCount = SEGMENTS * SEGMENTS * 6;
// Pre-allocate arrays
const positionsArr = new Float32Array(vertexCount * 3);
const colorsArr = new Float32Array(vertexCount * 3);
const indicesArr = new Uint32Array(indexCount);
// Build index buffer once
let idx = 0;
for (let row = 0; row < SEGMENTS; row++) {
  for (let col = 0; col < SEGMENTS; col++) {
    const a = row * GRID + col;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    indicesArr[idx++] = a; indicesArr[idx++] = b; indicesArr[idx++] = d;
    indicesArr[idx++] = a; indicesArr[idx++] = d; indicesArr[idx++] = c;
  }
}
terrainGeo.setIndex(new THREE.BufferAttribute(indicesArr, 1));
terrainGeo.setAttribute('position', new THREE.BufferAttribute(positionsArr, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.08,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ── River lines ────────────────────────────────────────────────────────────
const RIVER_POINTS = 200;
const riverLines = [];
const riverLineGroup = new THREE.Group();
scene.add(riverLineGroup);
const riverMatTemplate = new THREE.LineBasicMaterial({ color: '#ff4444', linewidth: 1, transparent: true, opacity: 0.75, depthTest: true });
// Pre-allocate river geometries
for (const rDef of RIVER_DEFS) {
  const positions = new Float32Array(RIVER_POINTS * 3);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const mat = riverMatTemplate.clone();
  const line = new THREE.Line(geo, mat);
  line.renderOrder = 1;
  line.material.depthTest = true;
  riverLineGroup.add(line);
  riverLines.push({ line, rDef, positions });
}
// ── Particle trails ────────────────────────────────────────────────────────
const PARTICLE_COUNT = 800;
const particlePositionsArr = new Float32Array(PARTICLE_COUNT * 3);
const particleColorsArr = new Float32Array(PARTICLE_COUNT * 3);
const particleSizesArr = new Float32Array(PARTICLE_COUNT);
// Particle state: each particle has a parametric position on the terrain
const particleStates = new Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleStates[i] = {
    u: Math.random(),
    v: Math.random(),
    speed: 0.003 + Math.random() * 0.012,
    phase: Math.random() * Math.PI * 2,
    wanderAmp: 0.002 + Math.random() * 0.008,
  };
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositionsArr, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColorsArr, 3));
particleGeo.setAttribute('size', new THREE.BufferAttribute(particleSizesArr, 1));
const particleMat = new THREE.PointsMaterial({
  size: 0.08,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  depthTest: true,
  transparent: true,
  opacity: 0.7,
  sizeAttenuation: true,
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 2;
scene.add(particles);
// ── Camera bookmarks ───────────────────────────────────────────────────────
const bookmarks = new Array(5).fill(null);
// ── State ──────────────────────────────────────────────────────────────────
let currentStep = 0;
let playing = false;
let playInterval = null;
let lastTime = performance.now();
let frameCount = 0;
let fpsUpdateTime = lastTime;
// ── Terrain update (mutate in place, zero allocations) ─────────────────────
function updateTerrain(stepIdx) {
  const step = DATASET[stepIdx];
  let maxRev = 0;
  let sumUsers = 0;
  let sumErrors = 0;
  let sumApi = 0;
  let pi = 0;
  let ci = 0;
  for (let row = 0; row < GRID; row++) {
    const fy = (row / SEGMENTS - 0.5) * EXTENT;
    for (let col = 0; col < GRID; col++) {
      const fx = (col / SEGMENTS - 0.5) * EXTENT;
      const d = step[row][col];
      const height = d.revenue * 5.5;
      positionsArr[pi] = fx;
      positionsArr[pi + 1] = height;
      positionsArr[pi + 2] = fy;
      // Color: user density maps to green intensity (vegetation)
      const userIntensity = Math.min(1, d.users / 0.7);
      const r = 0.04 + userIntensity * 0.06;
      const g = 0.08 + userIntensity * 0.7;
      const b = 0.06 + (1 - userIntensity) * 0.1;
      colorsArr[ci] = r;
      colorsArr[ci + 1] = g;
      colorsArr[ci + 2] = b;
      maxRev = Math.max(maxRev, d.revenue);
      sumUsers += d.users;
      sumErrors += d.errors;
      sumApi += d.apiCalls;
      pi += 3;
      ci += 3;
    }
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  // Rivers
  updateRivers(stepIdx);
  // Stats
  const total = GRID * GRID;
  document.getElementById('stat-time').textContent = `${stepIdx} / ${STEPS - 1}`;
  document.getElementById('stat-rev').textContent = (maxRev * 100).toFixed(1) + 'k';
  document.getElementById('stat-users').textContent = (sumUsers / total * 1000).toFixed(0);
  document.getElementById('stat-err').textContent = (sumErrors / total * 100).toFixed(2) + '%';
  document.getElementById('stat-api').textContent = (sumApi / total * 100).toFixed(0);
}
// ── River update ───────────────────────────────────────────────────────────
function updateRivers(stepIdx) {
  const step = DATASET[stepIdx];
  for (const rl of riverLines) {
    const { rDef, positions } = rl;
    for (let i = 0; i < RIVER_POINTS; i++) {
      const t = i / (RIVER_POINTS - 1);
      // Meandering path
      const baseX = rDef.sx + (rDef.ex - rDef.sx) * t;
      const baseY = rDef.sy + (rDef.ey - rDef.sy) * t;
      const meanderX = baseX + 0.025 * Math.sin(t * 20 + stepIdx * 0.1);
      const meanderY = baseY + 0.025 * Math.cos(t * 17 + stepIdx * 0.13);
      const col = Math.round(meanderX * SEGMENTS);
      const row = Math.round(meanderY * SEGMENTS);
      const cx = Math.max(0, Math.min(SEGMENTS, col));
      const cy = Math.max(0, Math.min(SEGMENTS, row));
      const d = step[cy][cx];
      const wx = (meanderX - 0.5) * EXTENT;
      const wz = (meanderY - 0.5) * EXTENT;
      const wy = d.revenue * 5.5 + 0.12;
      positions[i * 3] = wx;
      positions[i * 3 + 1] = wy;
      positions[i * 3 + 2] = wz;
    }
    rl.line.geometry.attributes.position.needsUpdate = true;
  }
}
// ── Particle update ────────────────────────────────────────────────────────
function updateParticles(stepIdx, dt) {
  const step = DATASET[stepIdx];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const ps = particleStates[i];
    // Wander
    ps.u += Math.cos(ps.phase) * ps.wanderAmp;
    ps.v += Math.sin(ps.phase) * ps.wanderAmp;
    ps.phase += ps.speed * 0.3 * dt;
    // Wrap at edges
    if (ps.u < 0) ps.u += 1;
    if (ps.u > 1) ps.u -= 1;
    if (ps.v < 0) ps.v += 1;
    if (ps.v > 1) ps.v -= 1;
    const col = Math.floor(ps.u * SEGMENTS);
    const row = Math.floor(ps.v * SEGMENTS);
    const cx = Math.max(0, Math.min(SEGMENTS, col));
    const cy = Math.max(0, Math.min(SEGMENTS, row));
    const d = step[cy][cx];
    const wx = (ps.u - 0.5) * EXTENT;
    const wz = (ps.v - 0.5) * EXTENT;
    const wy = d.revenue * 5.5 + 0.25;
    particlePositionsArr[i * 3] = wx;
    particlePositionsArr[i * 3 + 1] = wy;
    particlePositionsArr[i * 3 + 2] = wz;
    // Color: warm yellow-orange, brighter near high API areas
    const apiIntensity = Math.min(1, d.apiCalls / 0.5);
    particleColorsArr[i * 3] = 1.0;
    particleColorsArr[i * 3 + 1] = 0.65 + apiIntensity * 0.35;
    particleColorsArr[i * 3 + 2] = 0.1 + apiIntensity * 0.25;
    particleSizesArr[i] = 0.5 + apiIntensity * 1.5;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  particleGeo.attributes.size.needsUpdate = true;
}
// ── Set time step (main entry for all updates) ─────────────────────────────
function setStep(stepIdx) {
  currentStep = Math.max(0, Math.min(STEPS - 1, stepIdx));
  document.getElementById('time-slider').value = currentStep;
  document.getElementById('time-label').textContent = `T${currentStep}`;
  updateTerrain(currentStep);
}
// ── UI bindings ────────────────────────────────────────────────────────────
document.getElementById('time-slider').addEventListener('input', (e) => {
  setStep(parseInt(e.target.value));
});
document.getElementById('btn-play').addEventListener('click', () => {
  playing = !playing;
  const btn = document.getElementById('btn-play');
  btn.textContent = playing ? 'Pause' : 'Play';
  btn.classList.toggle('active', playing);
  if (playing) {
    playInterval = setInterval(() => {
      let next = currentStep + 1;
      if (next >= STEPS) next = 0;
      setStep(next);
    }, 180);
  } else {
    clearInterval(playInterval);
    playInterval = null;
  }
});
document.getElementById('btn-auto-rotate').addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  document.getElementById('btn-auto-rotate').classList.toggle('active', controls.autoRotate);
});
document.getElementById('btn-reset').addEventListener('click', () => {
  camera.position.set(8, 7.5, 14);
  controls.target.set(0, 1.5, 0);
  controls.update();
});
// Camera bookmarks: click = restore, shift+click = save
document.querySelectorAll('#bookmark-bar button').forEach(btn => {
  const slot = parseInt(btn.dataset.slot) - 1;
  btn.addEventListener('click', (e) => {
    if (e.shiftKey) {
      bookmarks[slot] = {
        pos: camera.position.clone(),
        target: controls.target.clone(),
      };
      btn.style.borderColor = '#51cf66';
      setTimeout(() => { btn.style.borderColor = ''; }, 600);
    } else if (bookmarks[slot]) {
      const bm = bookmarks[slot];
      camera.position.copy(bm.pos);
      controls.target.copy(bm.target);
      controls.update();
    }
  });
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  const num = parseInt(e.key);
  if (num >= 1 && num <= 5) {
    const slot = num - 1;
    if (e.shiftKey) {
      bookmarks[slot] = {
        pos: camera.position.clone(),
        target: controls.target.clone(),
      };
      const btn = document.querySelector(`#bookmark-bar button[data-slot="${num}"]`);
      if (btn) {
        btn.style.borderColor = '#51cf66';
        setTimeout(() => { btn.style.borderColor = ''; }, 600);
      }
    } else if (bookmarks[slot]) {
      camera.position.copy(bookmarks[slot].pos);
      controls.target.copy(bookmarks[slot].target);
      controls.update();
    }
  }
  if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
    controls.autoRotate = !controls.autoRotate;
    document.getElementById('btn-auto-rotate').classList.toggle('active', controls.autoRotate);
  }
  if (e.key === ' ' && !e.ctrlKey && !e.metaKey) {
    e.preventDefault();
    document.getElementById('btn-play').click();
  }
});
// ── Resize ─────────────────────────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ── Render loop ────────────────────────────────────────────────────────────
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  const dt = Math.min(0.1, (timestamp - lastTime) / 1000);
  lastTime = timestamp;
  frameCount++;
  // FPS counter
  if (timestamp - fpsUpdateTime > 1000) {
    const fps = Math.round(frameCount / ((timestamp - fpsUpdateTime) / 1000));
    document.getElementById('stat-fps').textContent = fps;
    frameCount = 0;
    fpsUpdateTime = timestamp;
  }
  // Update particles continuously
  updateParticles(currentStep, dt);
  renderer.render(scene, camera);
}
// ── Initial state ──────────────────────────────────────────────────────────
setStep(0);
updateParticles(0, 0.016);
requestAnimationFrame(animate);
</script>
</body>
</html>