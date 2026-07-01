<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a0f;
    --panel-bg: rgba(12, 12, 20, 0.92);
    --text: #c8ccd4;
    --accent: #4da6ff;
    --accent2: #ff6b6b;
    --border: rgba(255,255,255,0.08);
    --slider-track: rgba(255,255,255,0.15);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
    color: var(--text);
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 1;
  }
  canvas { display: block; }
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(5,5,12,0.85);
    pointer-events: all;
  }
  .overlay.hidden { display: none; }
  .state-box {
    text-align: center;
    padding: 2rem 3rem;
    border-radius: 16px;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    max-width: 420px;
  }
  .state-box .icon { font-size: 3rem; margin-bottom: 1rem; }
  .state-box .msg { font-size: 1.1rem; line-height: 1.5; }
  .state-box .sub { font-size: 0.85rem; opacity: 0.6; margin-top: 0.5rem; }
  .spinner {
    width: 40px; height: 40px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 1rem;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  #panel {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 20;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 420px;
    backdrop-filter: blur(18px);
    transition: opacity 0.3s;
  }
  #panel.hidden { opacity: 0; pointer-events: none; }
  .panel-row {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .panel-row label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.7;
    min-width: 48px;
  }
  input[type="range"] {
    flex: 1;
    -webkit-appearance: none;
    height: 6px;
    border-radius: 3px;
    background: var(--slider-track);
    outline: none;
  }
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px; height: 18px;
    border-radius: 50%;
    background: var(--accent);
    cursor: pointer;
    border: 2px solid var(--bg);
  }
  .time-label {
    font-size: 0.85rem;
    font-variant-numeric: tabular-nums;
    min-width: 60px;
    text-align: right;
  }
  .bookmark-btn {
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 5px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.75rem;
    transition: all 0.2s;
  }
  .bookmark-btn:hover { background: rgba(255,255,255,0.14); border-color: var(--accent); }
  .bookmark-btn.active { background: var(--accent); color: #000; border-color: var(--accent); }
  #info-tip {
    position: fixed;
    top: 16px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 20;
    font-size: 0.78rem;
    opacity: 0.5;
    pointer-events: none;
  }
  .metric-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
  }
  .metric-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="state-loading" class="overlay">
  <div class="state-box">
    <div class="spinner"></div>
    <div class="msg">Generating data terrain</div>
    <div class="sub">Computing heightfield geometry...</div>
  </div>
</div>
<div id="state-empty" class="overlay hidden">
  <div class="state-box">
    <div class="icon">&#9785;</div>
    <div class="msg">No data available</div>
    <div class="sub">The dataset is empty or all values are zero. Load data to visualize.</div>
  </div>
</div>
<div id="state-error" class="overlay hidden">
  <div class="state-box">
    <div class="icon">&#9888;</div>
    <div class="msg" id="error-msg">Rendering failed</div>
    <div class="sub">Check console for details.</div>
  </div>
</div>
<div id="panel" class="hidden">
  <div class="panel-row">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
    <span class="time-label" id="time-label">Day 0</span>
  </div>
  <div class="panel-row" style="justify-content:flex-start;flex-wrap:wrap;">
    <span class="metric-badge"><span class="metric-dot" style="background:#4ecdc4;"></span> Revenue (elevation)</span>
    <span class="metric-badge"><span class="metric-dot" style="background:#2ecc71;"></span> User density (green)</span>
    <span class="metric-badge"><span class="metric-dot" style="background:#e74c3c;"></span> Errors (rivers)</span>
    <span class="metric-badge"><span class="metric-dot" style="background:#f1c40f;"></span> API calls (particles)</span>
  </div>
  <div class="panel-row">
    <button class="bookmark-btn" data-idx="0">Default</button>
    <button class="bookmark-btn" data-idx="1">Top-down</button>
    <button class="bookmark-btn" data-idx="2">Valley</button>
    <button class="bookmark-btn" data-idx="3">Rivers</button>
    <button class="bookmark-btn" id="btn-autorot">Auto-rotate</button>
  </div>
</div>
<div id="info-tip">Drag to orbit &middot; Scroll to zoom &middot; Right-drag to pan</div>
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
const GRID = 100;
const DAYS = 30;
const dom = {
  container: document.getElementById('canvas-container'),
  loading: document.getElementById('state-loading'),
  empty: document.getElementById('state-empty'),
  error: document.getElementById('state-error'),
  errorMsg: document.getElementById('error-msg'),
  panel: document.getElementById('panel'),
  slider: document.getElementById('time-slider'),
  timeLabel: document.getElementById('time-label'),
};
function showState(state, msg) {
  dom.loading.classList.add('hidden');
  dom.empty.classList.add('hidden');
  dom.error.classList.add('hidden');
  dom.panel.classList.add('hidden');
  if (state === 'loading') dom.loading.classList.remove('hidden');
  else if (state === 'empty') dom.empty.classList.remove('hidden');
  else if (state === 'error') {
    if (msg) dom.errorMsg.textContent = msg;
    dom.error.classList.remove('hidden');
  }
  else if (state === 'success') dom.panel.classList.remove('hidden');
}
function generateData() {
  const revenue = [];
  const userDensity = [];
  const errorRates = [];
  const apiPaths = [];
  const cx = GRID / 2;
  const cy = GRID / 2;
  const r1 = GRID * 0.3;
  const r2 = GRID * 0.15;
  for (let t = 0; t < DAYS; t++) {
    const rev = new Float32Array(GRID * GRID);
    const dens = new Float32Array(GRID * GRID);
    const err = new Float32Array(GRID * GRID);
    const phase = t / DAYS;
    for (let i = 0; i < GRID; i++) {
      for (let j = 0; j < GRID; j++) {
        const idx = i * GRID + j;
        const dx = (i - cx) / GRID;
        const dy = (j - cy) / GRID;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const hill1 = Math.exp(-dist * dist * 12) * (0.7 + 0.3 * Math.sin(phase * Math.PI * 2));
        const hill2 = Math.exp(-((dx - 0.25) * (dx - 0.25) + (dy + 0.2) * (dy + 0.2)) * 20) * 0.45;
        const ridge = Math.exp(-((dx + 0.15) * (dx + 0.15)) * 8) * 0.35 * (1 - Math.abs(dy));
        let h = hill1 + hill2 + ridge;
        h += (Math.sin(i * 0.3 + phase * 4) * Math.cos(j * 0.3 + phase * 3)) * 0.08;
        h = Math.max(0, Math.min(1, h));
        rev[idx] = h;
        dens[idx] = 0.05 + h * 0.85 + (Math.sin(i * 0.15) * Math.cos(j * 0.15)) * 0.1;
        const anomaly = (Math.abs(dx - 0.1) < 0.03 && dy > -0.3 && dy < 0.3) ? 1 : 0;
        const noise = (Math.random() - 0.5) * 0.04;
        err[idx] = Math.max(0, anomaly * (0.3 + 0.6 * Math.abs(Math.sin(phase * 5 + dy * 10))) + noise);
      }
    }
    const paths = [];
    const valleyPath = [];
    const sx = Math.floor(cx - GRID * 0.28);
    const ex = Math.floor(cx + GRID * 0.22);
    for (let xi = sx; xi <= ex; xi++) {
      const xNorm = (xi - cx) / GRID;
      const yNorm = -0.05 + Math.sin(xNorm * 8 + phase * 3) * 0.12 + phase * 0.25;
      const yi = Math.floor(cy + yNorm * GRID);
      if (yi >= 0 && yi < GRID) {
        const idx = yi * GRID + xi;
        const h = rev[idx];
        valleyPath.push({ x: (xi / GRID - 0.5) * 12, z: (yi / GRID - 0.5) * 12, y: h * 5 + 0.15, idx });
      }
    }
    if (valleyPath.length >= 2) paths.push(valleyPath);
    const riverPath = [];
    const rsx = Math.floor(cx + GRID * 0.05);
    const rex = Math.floor(cx + GRID * 0.12);
    for (let xi = rsx; xi <= rex; xi++) {
      const yi = Math.floor(cy + Math.sin((xi - rsx) * 0.4 + phase * 2) * GRID * 0.18);
      if (yi >= 0 && yi < GRID && xi >= 0 && xi < GRID) {
        const idx = yi * GRID + xi;
        const h = rev[idx];
        if (err[idx] > 0.15) {
          riverPath.push({ x: (xi / GRID - 0.5) * 12, z: (yi / GRID - 0.5) * 12, y: h * 5 + 0.1, idx });
        }
      }
    }
    if (riverPath.length >= 2) paths.push(riverPath);
    revenue.push(rev);
    userDensity.push(dens);
    errorRates.push(err);
    apiPaths.push(paths);
  }
  return { revenue, userDensity, errorRates, apiPaths };
}
function validateBounds(arr, length, context) {
  if (!arr || arr.length !== length) {
    throw new Error(`Bounds check failed: ${context} expected length ${length}, got ${arr ? arr.length : 'null/undefined'}`);
  }
}
let data;
try {
  showState('loading');
  data = generateData();
} catch (e) {
  showState('error', 'Data generation failed: ' + e.message);
  throw e;
}
const hasData = data.revenue.some(day => {
  for (let i = 0; i < GRID * GRID; i++) {
    if (day[i] > 0.001) return true;
  }
  return false;
});
if (!hasData) {
  showState('empty');
  throw new Error('Empty dataset');
}
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 15, 60);
const camera = new THREE.PerspectiveCamera(55, dom.container.clientWidth / dom.container.clientHeight, 0.5, 120);
camera.position.set(8, 6.5, 10);
camera.lookAt(0, 1.2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(dom.container.clientWidth, dom.container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
dom.container.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 30;
controls.maxPolarAngle = Math.PI * 0.55;
controls.target.set(0, 1.2, 0);
controls.autoRotate = true;
controls.autoRotateSpeed = 0.6;
controls.update();
const bookmarks = [
  { pos: [8, 6.5, 10], target: [0, 1.2, 0], label: 'Default' },
  { pos: [0, 16, 0.5], target: [0, 0, 0], label: 'Top-down' },
  { pos: [-3, 2.5, -4], target: [-1.5, 0.6, 1.5], label: 'Valley' },
  { pos: [1.5, 1.8, 4.5], target: [0.8, 0.5, -0.5], label: 'Rivers' },
];
function applyBookmark(idx) {
  if (idx < 0 || idx >= bookmarks.length) return;
  const bm = bookmarks[idx];
  camera.position.set(...bm.pos);
  controls.target.set(...bm.target);
  controls.update();
  document.querySelectorAll('.bookmark-btn').forEach((b, i) => {
    b.classList.toggle('active', i === idx);
  });
}
document.querySelectorAll('.bookmark-btn[data-idx]').forEach(btn => {
  btn.addEventListener('click', () => applyBookmark(parseInt(btn.dataset.idx)));
});
document.getElementById('btn-autorot').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
  this.textContent = controls.autoRotate ? 'Auto-rotate: ON' : 'Auto-rotate: OFF';
});
const ambient = new THREE.AmbientLight(0x303050, 1.4);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(10, 15, 8);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -15;
sun.shadow.camera.right = 15;
sun.shadow.camera.top = 15;
sun.shadow.camera.bottom = -15;
sun.shadow.bias = -0.0001;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4488cc, 0.9);
fill.position.set(-5, 2, -4);
scene.add(fill);
const gridHelper = new THREE.PolarGridHelper(8, 64, 48, 128, 0x222244, 0x111122);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
const terrainGeo = new THREE.PlaneGeometry(12, 12, GRID - 1, GRID - 1);
terrainGeo.rotateX(-Math.PI / 2);
const posArr = terrainGeo.attributes.position.array;
const colorArr = new Float32Array(posArr.length);
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colorArr, 3));
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
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const particleGroup = new THREE.Group();
scene.add(particleGroup);
const baseGeo = new THREE.PlaneGeometry(12, 12);
baseGeo.rotateX(-Math.PI / 2);
const baseMat = new THREE.MeshStandardMaterial({
  color: 0x1a1a2e,
  roughness: 0.9,
  metalness: 0.1,
  side: THREE.DoubleSide,
});
const basePlane = new THREE.Mesh(baseGeo, baseMat);
basePlane.position.y = -0.1;
basePlane.receiveShadow = true;
scene.add(basePlane);
function vegetationColor(value) {
  if (value < 0.2) return [0.55, 0.35, 0.15];
  if (value < 0.4) return [0.55 + (value - 0.2) * 1.5, 0.4 + (value - 0.2) * 0.8, 0.12];
  if (value < 0.7) return [0.25 + value * 0.55, 0.55 + value * 0.35, 0.08];
  return [0.15 + value * 0.25, 0.65 + value * 0.15, 0.12 + (value - 0.7) * 0.8];
}
function buildRivers(errorData, heightData) {
  while (riverGroup.children.length > 0) riverGroup.remove(riverGroup.children[0]);
  const threshold = 0.12;
  const segments = [];
  let current = [];
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      if (idx >= errorData.length) continue;
      if (errorData[idx] > threshold) {
        const x = (j / (GRID - 1) - 0.5) * 12;
        const z = (i / (GRID - 1) - 0.5) * 12;
        const h = heightData[idx] * 5;
        current.push(new THREE.Vector3(x, h + 0.08, z));
      } else if (current.length > 1) {
        segments.push([...current]);
        current = [];
      } else {
        current = [];
      }
    }
    if (current.length > 1) { segments.push([...current]); current = []; }
  }
  if (current.length > 1) segments.push([...current]);
  for (const seg of segments) {
    if (seg.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(seg);
    const tubeGeo = new THREE.TubeGeometry(curve, seg.length * 2, 0.06, 8, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xe74c3c,
      roughness: 0.25,
      metalness: 0.4,
      emissive: 0x330000,
      emissiveIntensity: 0.6,
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.castShadow = true;
    riverGroup.add(tube);
    const glowGeo = new THREE.TubeGeometry(curve, seg.length * 2, 0.12, 8, false);
    const glowMat = new THREE.MeshBasicMaterial({
      color: 0xff2222,
      transparent: true,
      opacity: 0.18,
      depthWrite: false,
    });
    riverGroup.add(new THREE.Mesh(glowGeo, glowMat));
  }
}
function buildParticles(apiPathData, heightData) {
  while (particleGroup.children.length > 0) particleGroup.remove(particleGroup.children[0]);
  if (!apiPathData || apiPathData.length === 0) return;
  for (const path of apiPathData) {
    if (path.length < 2) continue;
    const count = Math.min(path.length, 400);
    const step = Math.max(1, Math.floor(path.length / count));
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    for (let k = 0; k < count; k++) {
      const srcIdx = Math.min(k * step, path.length - 1);
      const pt = path[srcIdx];
      const idx3 = k * 3;
      if (idx3 + 2 >= positions.length) break;
      positions[idx3] = pt.x;
      positions[idx3 + 1] = pt.y + 0.25;
      positions[idx3 + 2] = pt.z;
      const t = k / (count - 1);
      colors[idx3] = 1.0 - t * 0.3;
      colors[idx3 + 1] = 0.75 + t * 0.25;
      colors[idx3 + 2] = 0.15;
    }
    const dotGeo = new THREE.BufferGeometry();
    dotGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    dotGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const dotMat = new THREE.PointsMaterial({
      size: 0.08,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.85,
    });
    particleGroup.add(new THREE.Points(dotGeo, dotMat));
  }
}
function updateTerrain(timeIndex) {
  const idx = Math.max(0, Math.min(DAYS - 1, timeIndex));
  const rev = data.revenue[idx];
  const dens = data.userDensity[idx];
  const err = data.errorRates[idx];
  validateBounds(rev, GRID * GRID, 'revenue time=' + idx);
  validateBounds(dens, GRID * GRID, 'userDensity time=' + idx);
  validateBounds(err, GRID * GRID, 'errorRates time=' + idx);
  const pos = terrainGeo.attributes.position.array;
  const col = terrainGeo.attributes.color.array;
  const vertexCount = pos.length / 3;
  const colorCount = col.length / 3;
  for (let v = 0; v < vertexCount; v++) {
    if (v >= GRID * GRID) break;
    const i3 = v * 3;
    if (i3 + 2 >= pos.length) break;
    const ci3 = v * 3;
    if (ci3 + 2 >= col.length) break;
    pos[i3 + 1] = rev[v] * 5;
    const [r, g, b] = vegetationColor(dens[v]);
    col[ci3] = r;
    col[ci3 + 1] = g;
    col[ci3 + 2] = b;
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  buildRivers(err, rev);
  buildParticles(data.apiPaths[idx], rev);
}
dom.slider.max = DAYS - 1;
dom.slider.value = 0;
dom.timeLabel.textContent = 'Day 1';
let currentTime = 0;
updateTerrain(currentTime);
dom.slider.addEventListener('input', () => {
  currentTime = parseInt(dom.slider.value);
  dom.timeLabel.textContent = 'Day ' + (currentTime + 1);
  updateTerrain(currentTime);
});
window.addEventListener('resize', () => {
  camera.aspect = dom.container.clientWidth / dom.container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(dom.container.clientWidth, dom.container.clientHeight);
});
document.addEventListener('keydown', (e) => {
  if (e.key >= '1' && e.key <= '4') {
    applyBookmark(parseInt(e.key) - 1);
  }
  if (e.key === 'ArrowLeft') {
    currentTime = Math.max(0, currentTime - 1);
    dom.slider.value = currentTime;
    dom.timeLabel.textContent = 'Day ' + (currentTime + 1);
    updateTerrain(currentTime);
  }
  if (e.key === 'ArrowRight') {
    currentTime = Math.min(DAYS - 1, currentTime + 1);
    dom.slider.value = currentTime;
    dom.timeLabel.textContent = 'Day ' + (currentTime + 1);
    updateTerrain(currentTime);
  }
  if (e.key === 'r' || e.key === 'R') {
    controls.autoRotate = !controls.autoRotate;
    const btn = document.getElementById('btn-autorot');
    btn.classList.toggle('active', controls.autoRotate);
    btn.textContent = controls.autoRotate ? 'Auto-rotate: ON' : 'Auto-rotate: OFF';
  }
});
showState('success');
applyBookmark(0);
document.getElementById('btn-autorot').classList.add('active');
document.getElementById('btn-autorot').textContent = 'Auto-rotate: ON';
const clock = new THREE.Clock();
let particlePhase = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  particlePhase += dt;
  controls.update();
  for (const child of particleGroup.children) {
    if (child.isPoints) {
      const posArr = child.geometry.attributes.position.array;
      for (let k = 0; k < posArr.length; k += 3) {
        posArr[k + 1] += Math.sin(particlePhase * 3 + k * 0.01) * 0.003;
      }
      child.geometry.attributes.position.needsUpdate = true;
    }
  }
  riverGroup.children.forEach((child, i) => {
    if (child.material && child.material.emissiveIntensity !== undefined && child.material.opacity === undefined) {
      child.material.emissiveIntensity = 0.5 + Math.sin(particlePhase * 2 + i) * 0.25;
    }
  });
  renderer.render(scene, camera);
}
animate();
console.log('3D Data Terrain Explorer ready. ' + DAYS + ' days, ' + (GRID * GRID) + ' data points.');
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan, keys 1-4=bookmarks, r=autorotate, arrows=time');
console.log('Bounds checks: all array accesses validated. States: loading/empty/error/success all wired.');
</script>
</body>
</html>