<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10,10,25,0.92);
    --text: #c8ccd4;
    --accent: #4da6ff;
    --warn: #ff6644;
    --river: #ff4466;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  canvas { display:block; }
  #ui { position:fixed; bottom:0; left:0; right:0; z-index:10; pointer-events:none; }
  #panel { background:var(--panel-bg); backdrop-filter:blur(12px); border-top:1px solid rgba(255,255,255,0.08); padding:12px 20px; display:flex; align-items:center; gap:16px; pointer-events:auto; flex-wrap:wrap; }
  #panel label { font-size:11px; text-transform:uppercase; letter-spacing:0.08em; opacity:0.7; white-space:nowrap; }
  #time-slider { flex:1; min-width:160px; max-width:400px; -webkit-appearance:none; height:4px; background:rgba(255,255,255,0.12); border-radius:2px; outline:none; }
  #time-slider::-webkit-slider-thumb { -webkit-appearance:none; width:18px; height:18px; border-radius:50%; background:var(--accent); cursor:pointer; border:2px solid #fff; }
  #time-label { font-size:13px; font-weight:600; min-width:100px; text-align:center; }
  .btn { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); color:var(--text); padding:6px 14px; border-radius:6px; cursor:pointer; font-size:12px; transition:all 0.2s; white-space:nowrap; }
  .btn:hover { background:rgba(255,255,255,0.14); border-color:var(--accent); }
  .btn.active { background:var(--accent); border-color:var(--accent); color:#fff; }
  #bookmarks { display:flex; gap:6px; flex-wrap:wrap; }
  #fps { font-size:10px; opacity:0.5; min-width:50px; text-align:right; }
  #legend { position:fixed; top:16px; right:16px; background:var(--panel-bg); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.08); border-radius:8px; padding:12px 16px; font-size:11px; z-index:10; line-height:1.6; }
  .legend-row { display:flex; align-items:center; gap:8px; }
  .legend-swatch { width:12px; height:12px; border-radius:3px; flex-shrink:0; }
  #tooltip { position:fixed; background:rgba(0,0,0,0.85); padding:6px 10px; border-radius:4px; font-size:11px; pointer-events:none; display:none; z-index:20; }
  #perf-warn { position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); background:rgba(255,60,30,0.9); padding:8px 18px; border-radius:6px; font-size:12px; font-weight:600; z-index:30; display:none; pointer-events:none; }
</style>
</head>
<body>
<div id="ui">
  <div id="panel">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="11" value="0" step="1">
    <span id="time-label">T0: Jan</span>
    <button class="btn" id="btn-play">&#9654; Play</button>
    <button class="btn" id="btn-auto-rotate">Auto-Rotate</button>
    <span id="bookmarks"></span>
    <span id="fps">-- fps</span>
  </div>
</div>
<div id="legend">
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to top,#1a3a1a,#4a9,#8d4)"></span> Revenue (elevation)</div>
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#2a1a0a,#8b4,#4a9)"></span> User density (color)</div>
  <div class="legend-row"><span class="legend-swatch" style="background:var(--river)"></span> Error paths (rivers)</div>
  <div class="legend-row"><span class="legend-swatch" style="background:#ffcc44"></span> API flows (particles)</div>
</div>
<div id="tooltip"></div>
<div id="perf-warn">&#9888; Frame budget exceeded</div>
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
// ─── Simplex Noise (compact 2D implementation) ───────────────────────
class SimplexNoise {
  constructor(seed = 1) {
    this.grad3 = [[1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0],[1,0,1],[-1,0,1],[1,0,-1],[-1,0,-1],[0,1,1],[0,-1,1],[0,1,-1],[0,-1,-1]];
    this.perm = new Uint8Array(512);
    this.permMod12 = new Uint8Array(512);
    const p = new Uint8Array(256);
    for (let i = 0; i < 256; i++) p[i] = i;
    for (let i = 255; i > 0; i--) {
      const j = (seed * 16807 + i * 48271) % (i + 1);
      [p[i], p[j]] = [p[j], p[i]];
      seed = (seed * 16807) % 2147483647;
    }
    for (let i = 0; i < 512; i++) {
      this.perm[i] = p[i & 255];
      this.permMod12[i] = this.perm[i] % 12;
    }
  }
  noise2D(x, y) {
    const F2 = 0.5 * (Math.sqrt(3) - 1), G2 = (3 - Math.sqrt(3)) / 6;
    const s = (x + y) * F2, i = Math.floor(x + s), j = Math.floor(y + s);
    const t = (i + j) * G2, X0 = i - t, Y0 = j - t, x0 = x - X0, y0 = y - Y0;
    let i1, j1;
    if (x0 > y0) { i1 = 1; j1 = 0; } else { i1 = 0; j1 = 1; }
    const x1 = x0 - i1 + G2, y1 = y0 - j1 + G2, x2 = x0 - 1 + 2 * G2, y2 = y0 - 1 + 2 * G2;
    const ii = i & 255, jj = j & 255;
    const gi0 = this.permMod12[ii + this.perm[jj]];
    const gi1 = this.permMod12[ii + i1 + this.perm[jj + j1]];
    const gi2 = this.permMod12[ii + 1 + this.perm[jj + 1]];
    let n0 = 0, n1 = 0, n2 = 0;
    let t0 = 0.5 - x0 * x0 - y0 * y0; if (t0 > 0) { t0 *= t0; n0 = t0 * t0 * (this.grad3[gi0][0] * x0 + this.grad3[gi0][1] * y0); }
    let t1 = 0.5 - x1 * x1 - y1 * y1; if (t1 > 0) { t1 *= t1; n1 = t1 * t1 * (this.grad3[gi1][0] * x1 + this.grad3[gi1][1] * y1); }
    let t2 = 0.5 - x2 * x2 - y2 * y2; if (t2 > 0) { t2 *= t2; n2 = t2 * t2 * (this.grad3[gi2][0] * x2 + this.grad3[gi2][1] * y2); }
    return 70 * (n0 + n1 + n2);
  }
}
// ─── Synthetic Time-Series Data Generator ────────────────────────────
const GRID = 64;
const TIMEPOINTS = 12;
const simplex = new SimplexNoise(42);
function generateTimepoint(t) {
  const revenue = new Float32Array(GRID * GRID);
  const users = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  const tNorm = t / (TIMEPOINTS - 1);
  const seasonality = Math.sin(tNorm * Math.PI * 2) * 0.3 + Math.sin(tNorm * Math.PI * 4) * 0.15;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const nx = ix / GRID, ny = iy / GRID;
      const base = simplex.noise2D(nx * 4, ny * 4) * 0.5;
      const detail = simplex.noise2D(nx * 8 + t * 0.3, ny * 8 + t * 0.3) * 0.25;
      const trend = tNorm * 0.4;
      const peak = Math.exp(-((nx - 0.5) ** 2 + (ny - 0.5) ** 2) * 8) * 0.6;
      revenue[idx] = Math.max(0, base + detail + trend + peak + seasonality * peak + 0.3);
      const userBase = simplex.noise2D(nx * 5 + 1.7, ny * 5 + 1.7) * 0.5;
      const userTrend = tNorm * 0.35;
      users[idx] = Math.max(0, userBase + userTrend + detail * 0.6 + peak * 0.4 + 0.25);
      const errBase = simplex.noise2D(nx * 6 + 3.3, ny * 6 + 3.3);
      const errSpike = (t > 3 && t < 6) ? Math.exp(-((nx - 0.35) ** 2 + (ny - 0.6) ** 2) * 20) * 0.4 : 0;
      errors[idx] = Math.max(0, errBase * 0.15 + errSpike + (1 - peak) * 0.08);
    }
  }
  return { revenue, users, errors };
}
// ─── River Path Extraction ────────────────────────────────────────────
function extractRiverPaths(errors, threshold = 0.12) {
  const paths = [];
  const visited = new Uint8Array(GRID * GRID);
  const directions = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]];
  function trace(ix, iy) {
    const points = [];
    let cx = ix, cy = iy;
    let steps = 0;
    while (steps < 300) {
      const idx = cy * GRID + cx;
      if (cx < 0 || cx >= GRID || cy < 0 || cy >= GRID || visited[idx]) break;
      visited[idx] = 1;
      points.push({ x: cx, y: cy });
      let bestDx = 0, bestDy = 0, bestVal = -1;
      for (const [dx, dy] of directions) {
        const nx = cx + dx, ny = cy + dy;
        if (nx >= 0 && nx < GRID && ny >= 0 && ny < GRID && !visited[ny * GRID + nx]) {
          if (errors[ny * GRID + nx] > bestVal) {
            bestVal = errors[ny * GRID + nx];
            bestDx = dx; bestDy = dy;
          }
        }
      }
      if (bestVal < threshold * 0.5) break;
      cx += bestDx; cy += bestDy;
      steps++;
    }
    if (points.length > 4) paths.push(points);
  }
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      if (!visited[iy * GRID + ix] && errors[iy * GRID + ix] > threshold) {
        trace(ix, iy);
      }
    }
  }
  return paths;
}
// ─── API Flow Particle Paths ──────────────────────────────────────────
function generateFlowPaths(count = 8) {
  const paths = [];
  for (let i = 0; i < count; i++) {
    const points = [];
    const startX = 5 + Math.floor(Math.random() * (GRID - 10));
    const startY = 5 + Math.floor(Math.random() * (GRID - 10));
    let cx = startX, cy = startY;
    const len = 20 + Math.floor(Math.random() * 40);
    for (let s = 0; s < len; s++) {
      const angle = simplex.noise2D(cx * 0.15, cy * 0.15) * Math.PI * 2;
      cx += Math.cos(angle) * 2.5;
      cy += Math.sin(angle) * 2.5;
      cx = Math.max(1, Math.min(GRID - 2, cx));
      cy = Math.max(1, Math.min(GRID - 2, cy));
      points.push({ x: cx, y: cy });
    }
    paths.push(points);
  }
  return paths;
}
// ─── Scene Setup ──────────────────────────────────────────────────────
const container = document.body;
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.FogExp2('#0a0a18', 0.00025);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(18, 22, 28);
camera.lookAt(GRID / 2, 0, GRID / 2);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(GRID / 2, 0, GRID / 2);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 8;
controls.maxDistance = 70;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
// ─── Lighting ─────────────────────────────────────────────────────────
const ambientLight = new THREE.AmbientLight('#334466', 0.6);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffe8cc', 2.5);
sunLight.position.set(40, 30, 20);
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#8899cc', 0.5);
fillLight.position.set(-20, 5, -10);
scene.add(fillLight);
// ─── Ground Plane ─────────────────────────────────────────────────────
const groundGeo = new THREE.PlaneGeometry(GRID + 10, GRID + 10);
const groundMat = new THREE.MeshStandardMaterial({ color: '#111122', roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.set(GRID / 2, -0.05, GRID / 2);
ground.receiveShadow = true;
scene.add(ground);
// Grid lines
const gridHelper = new THREE.PolarGridHelper(GRID / 2 + 3, 32, 16, 64, '#1a1a33', '#1a1a33');
gridHelper.position.set(GRID / 2, 0.01, GRID / 2);
scene.add(gridHelper);
// ─── Terrain Mesh (reusable BufferGeometry) ──────────────────────────
const terrainPositions = new Float32Array(GRID * GRID * 3);
const terrainColors = new Float32Array(GRID * GRID * 3);
const terrainIndices = [];
for (let iy = 0; iy < GRID - 1; iy++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = iy * GRID + ix;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    terrainIndices.push(a, b, d);
    terrainIndices.push(a, d, c);
  }
}
const terrainGeo = new THREE.BufferGeometry();
terrainGeo.setAttribute('position', new THREE.BufferAttribute(terrainPositions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(terrainColors, 3));
terrainGeo.setIndex(terrainIndices);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ─── River Geometry (rebuilt on time change) ─────────────────────────
let riverLines = new THREE.Group();
scene.add(riverLines);
function updateRiverGeometry(revenue, errors) {
  while (riverLines.children.length) riverLines.remove(riverLines.children[0]);
  const paths = extractRiverPaths(errors);
  const riverMat = new THREE.MeshBasicMaterial({ color: '#ff4466', transparent: true, opacity: 0.75, side: THREE.DoubleSide });
  for (const path of paths) {
    const curvePoints = [];
    for (const p of path) {
      const idx = Math.floor(p.y) * GRID + Math.floor(p.x);
      const h = revenue[Math.min(GRID * GRID - 1, Math.max(0, idx))] * 8 + 0.15;
      curvePoints.push(new THREE.Vector3(p.x, h, p.y));
    }
    if (curvePoints.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(curvePoints);
    const tubeGeo = new THREE.TubeGeometry(curve, curvePoints.length * 2, 0.13, 6, false);
    const tube = new THREE.Mesh(tubeGeo, riverMat);
    tube.renderOrder = 1;
    tube.material.depthTest = true;
    tube.material.depthWrite = true;
    riverLines.add(tube);
    const glowGeo = new THREE.TubeGeometry(curve, curvePoints.length * 2, 0.28, 6, false);
    const glowMat = new THREE.MeshBasicMaterial({ color: '#ff6688', transparent: true, opacity: 0.18, side: THREE.DoubleSide });
    const glow = new THREE.Mesh(glowGeo, glowMat);
    glow.renderOrder = 0;
    riverLines.add(glow);
  }
}
// ─── Particle System ──────────────────────────────────────────────────
const PARTICLE_COUNT = 500;
const flowPaths = generateFlowPaths(12);
const particlePositionsArr = new Float32Array(PARTICLE_COUNT * 3);
const particleColorsArr = new Float32Array(PARTICLE_COUNT * 3);
const particleData = [];
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const pathIdx = i % flowPaths.length;
  const path = flowPaths[pathIdx];
  const t = Math.random();
  const segIdx = Math.floor(t * (path.length - 1));
  const frac = t * (path.length - 1) - segIdx;
  const p0 = path[Math.min(segIdx, path.length - 1)];
  const p1 = path[Math.min(segIdx + 1, path.length - 1)];
  const px = p0.x + (p1.x - p0.x) * frac;
  const py = p0.y + (p1.y - p0.y) * frac;
  particlePositionsArr[i * 3] = px;
  particlePositionsArr[i * 3 + 1] = 0.3;
  particlePositionsArr[i * 3 + 2] = py;
  particleColorsArr[i * 3] = 1.0;
  particleColorsArr[i * 3 + 1] = 0.75 + Math.random() * 0.25;
  particleColorsArr[i * 3 + 2] = 0.2;
  particleData.push({
    pathIdx,
    t: Math.random(),
    speed: 0.0006 + Math.random() * 0.0018,
    baseY: 0
  });
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositionsArr, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColorsArr, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.22,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 2;
scene.add(particles);
// ─── Decorative boundary markers ──────────────────────────────────────
const markerGeo = new THREE.SphereGeometry(0.18, 8, 8);
const markerMat = new THREE.MeshStandardMaterial({ color: '#4da6ff', emissive: '#1a3366', roughness: 0.3, metalness: 0.6 });
for (let i = 0; i < 4; i++) {
  const cx = i < 2 ? 0 : GRID;
  const cz = i % 2 === 0 ? 0 : GRID;
  const marker = new THREE.Mesh(markerGeo, markerMat);
  marker.position.set(cx, 0.3, cz);
  scene.add(marker);
}
// ─── Terrain Update (on-demand, reuses buffers) ──────────────────────
const geometryCache = new Map();
function getCachedTerrain(t) {
  if (geometryCache.has(t)) return geometryCache.get(t);
  if (geometryCache.size >= 3) {
    const firstKey = geometryCache.keys().next().value;
    geometryCache.delete(firstKey);
  }
  const data = generateTimepoint(t);
  geometryCache.set(t, data);
  return data;
}
function updateTerrain(t) {
  const { revenue, users, errors } = getCachedTerrain(t);
  const heightScale = 8;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const h = revenue[idx] * heightScale;
      const i3 = idx * 3;
      terrainPositions[i3] = ix;
      terrainPositions[i3 + 1] = h;
      terrainPositions[i3 + 2] = iy;
      const userVal = users[idx];
      const r = 0.12 + userVal * 0.4;
      const g = 0.25 + userVal * 0.55;
      const b = 0.08 + userVal * 0.2;
      terrainColors[i3] = r;
      terrainColors[i3 + 1] = g;
      terrainColors[i3 + 2] = b;
    }
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  terrainGeo.index.needsUpdate = true;
  updateRiverGeometry(revenue, errors);
  return { revenue, errors };
}
// ─── State ────────────────────────────────────────────────────────────
let currentTimepoint = 0;
let currentRevenue = null;
let playing = false;
let playTimer = 0;
const { revenue: initRev, errors: initErr } = updateTerrain(0);
currentRevenue = initRev;
// ─── UI Elements ──────────────────────────────────────────────────────
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const btnPlay = document.getElementById('btn-play');
const btnAutoRotate = document.getElementById('btn-auto-rotate');
const bookmarksEl = document.getElementById('bookmarks');
const fpsEl = document.getElementById('fps');
const perfWarn = document.getElementById('perf-warn');
const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dec'];
function setTimepoint(t) {
  currentTimepoint = t;
  timeSlider.value = t;
  timeLabel.textContent = `T${t}: ${monthNames[t]}`;
  const { revenue } = updateTerrain(t);
  currentRevenue = revenue;
}
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value);
  if (t !== currentTimepoint) setTimepoint(t);
});
btnPlay.addEventListener('click', () => {
  playing = !playing;
  btnPlay.textContent = playing ? '\u23F8 Pause' : '\u25B6 Play';
  btnPlay.classList.toggle('active', playing);
});
btnAutoRotate.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAutoRotate.classList.toggle('active', controls.autoRotate);
});
// ─── Camera Bookmarks ─────────────────────────────────────────────────
const bookmarks = [
  { name: 'Top', pos: [GRID / 2, 35, GRID / 2], target: [GRID / 2, 0, GRID / 2] },
  { name: 'Front', pos: [GRID / 2, 4, GRID + 16], target: [GRID / 2, 1, GRID / 2] },
  { name: 'Side', pos: [GRID + 16, 6, GRID / 2], target: [GRID / 2, 1, GRID / 2] },
  { name: 'Close', pos: [GRID / 2 + 6, 12, GRID / 2 + 8], target: [GRID / 2, 2, GRID / 2] },
];
function animateCamera(pos, target, duration = 800) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...pos);
  const endTarget = new THREE.Vector3(...target);
  const startTime = performance.now();
  function step(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
function renderBookmarks() {
  bookmarksEl.innerHTML = '';
  for (const bm of bookmarks) {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.textContent = bm.name;
    btn.addEventListener('click', () => animateCamera(bm.pos, bm.target));
    bookmarksEl.appendChild(btn);
  }
}
renderBookmarks();
// ─── Keyboard shortcuts ───────────────────────────────────────────────
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case ' ':
      e.preventDefault();
      playing = !playing;
      btnPlay.textContent = playing ? '\u23F8 Pause' : '\u25B6 Play';
      btnPlay.classList.toggle('active', playing);
      break;
    case 'arrowleft':
      if (currentTimepoint > 0) setTimepoint(currentTimepoint - 1);
      break;
    case 'arrowright':
      if (currentTimepoint < TIMEPOINTS - 1) setTimepoint(currentTimepoint + 1);
      break;
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      btnAutoRotate.classList.toggle('active', controls.autoRotate);
      break;
    case '1': animateCamera(bookmarks[0].pos, bookmarks[0].target); break;
    case '2': animateCamera(bookmarks[1].pos, bookmarks[1].target); break;
    case '3': animateCamera(bookmarks[2].pos, bookmarks[2].target); break;
    case '4': animateCamera(bookmarks[3].pos, bookmarks[3].target); break;
  }
});
// ─── Animation Loop ───────────────────────────────────────────────────
const FRAME_BUDGET_MS = 16;
let frameTimes = [];
let lastFrameStart = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  const frameStart = performance.now();
  const delta = Math.min(0.1, (timestamp - lastFrameStart) / 1000);
  lastFrameStart = timestamp;
  controls.update();
  // Playback
  if (playing) {
    playTimer += delta;
    if (playTimer > 1.8) {
      playTimer = 0;
      const next = (currentTimepoint + 1) % TIMEPOINTS;
      setTimepoint(next);
    }
  }
  // Particle update (typed array reuse, no per-frame allocation)
  if (currentRevenue) {
    const posArr = particleGeo.attributes.position.array;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const pd = particleData[i];
      pd.t += pd.speed;
      if (pd.t > 1) pd.t -= 1;
      const path = flowPaths[pd.pathIdx];
      const segIdx = Math.floor(pd.t * (path.length - 1));
      const frac = pd.t * (path.length - 1) - segIdx;
      const p0 = path[Math.min(segIdx, path.length - 1)];
      const p1 = path[Math.min(segIdx + 1, path.length - 1)];
      const px = p0.x + (p1.x - p0.x) * frac;
      const pz = p0.y + (p1.y - p0.y) * frac;
      const gx = Math.min(GRID - 1, Math.max(0, Math.floor(px)));
      const gy = Math.min(GRID - 1, Math.max(0, Math.floor(pz)));
      const terrainH = currentRevenue[gy * GRID + gx] * 8;
      const i3 = i * 3;
      posArr[i3] = px;
      posArr[i3 + 1] = terrainH + 0.6;
      posArr[i3 + 2] = pz;
    }
    particleGeo.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
  // Frame budget tracking
  const frameTime = performance.now() - frameStart;
  frameTimes.push(frameTime);
  if (frameTimes.length > 60) frameTimes.shift();
  const avgFrameTime = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length;
  fpsEl.textContent = `${Math.round(1000 / Math.max(avgFrameTime, 0.1))} fps`;
  if (frameTime > FRAME_BUDGET_MS * 1.5 && frameTimes.length > 10) {
    perfWarn.style.display = 'block';
    setTimeout(() => { perfWarn.style.display = 'none'; }, 1200);
  }
}
// ─── Resize Handler ───────────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Start ────────────────────────────────────────────────────────────
lastFrameStart = performance.now();
requestAnimationFrame(animate);
</script>
</body>
</html>