<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#0a0a14;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
canvas{display:block}
#ui{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:10}
#ui>*{pointer-events:auto}
#panel{position:absolute;top:16px;left:16px;background:rgba(10,10,25,0.85);border:1px solid rgba(100,140,220,0.25);border-radius:10px;padding:14px 18px;min-width:240px;backdrop-filter:blur(10px)}
#panel h1{font-size:16px;font-weight:600;margin:0 0 4px;color:#7eb8ff;letter-spacing:0.5px}
#panel .sub{font-size:11px;color:#6b7d99;margin-bottom:12px}
.metric{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px}
.metric .label{color:#8899b4}
.metric .value{font-weight:600;font-variant-numeric:tabular-nums}
.metric .val-revenue{color:#4ecb71}
.metric .val-users{color:#5dade2}
.metric .val-errors{color:#e74c3c}
#time-control{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(10,10,25,0.85);border:1px solid rgba(100,140,220,0.25);border-radius:10px;padding:14px 24px;display:flex;align-items:center;gap:14px;backdrop-filter:blur(10px)}
#time-slider{-webkit-appearance:none;width:320px;height:6px;border-radius:3px;background:linear-gradient(90deg,#1a2a4a,#4a7ab5,#1a2a4a);outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#7eb8ff;cursor:pointer;box-shadow:0 0 12px rgba(126,184,255,0.5);border:2px solid #fff}
#time-label{font-size:12px;color:#8899b4;min-width:70px;text-align:center;font-variant-numeric:tabular-nums}
#bookmarks{position:absolute;top:16px;right:16px;display:flex;flex-direction:column;gap:6px;max-height:60vh;overflow-y:auto}
.bkm-btn{background:rgba(10,10,25,0.8);border:1px solid rgba(100,140,220,0.2);color:#8899b4;padding:8px 14px;border-radius:6px;cursor:pointer;font-size:11px;text-align:left;transition:all 0.2s;white-space:nowrap;backdrop-filter:blur(8px)}
.bkm-btn:hover{background:rgba(30,40,70,0.85);border-color:rgba(126,184,255,0.4);color:#c8d6e5}
.bkm-btn.save{color:#4ecb71;border-color:rgba(78,203,113,0.3)}
.bkm-btn.save:hover{background:rgba(20,40,25,0.85);border-color:#4ecb71}
#legend{position:absolute;bottom:24px;left:24px;background:rgba(10,10,25,0.8);border:1px solid rgba(100,140,220,0.2);border-radius:8px;padding:10px 14px;font-size:10px;backdrop-filter:blur(8px)}
.legend-row{display:flex;align-items:center;gap:8px;margin:3px 0}
.legend-swatch{width:12px;height:12px;border-radius:2px;flex-shrink:0}
#tooltip{position:absolute;background:rgba(10,10,30,0.9);border:1px solid rgba(126,184,255,0.3);border-radius:6px;padding:8px 12px;font-size:11px;pointer-events:none;display:none;backdrop-filter:blur(8px);z-index:20}
</style>
</head>
<body>
<div id="ui">
  <div id="panel">
    <h1>Data Terrain Explorer</h1>
    <div class="sub">Revenue elevation · User density color · Error rivers</div>
    <div class="metric"><span class="label">Peak Revenue</span><span class="value val-revenue" id="val-revenue">—</span></div>
    <div class="metric"><span class="label">Avg User Density</span><span class="value val-users" id="val-users">—</span></div>
    <div class="metric"><span class="label">Error Rate</span><span class="value val-errors" id="val-errors">—</span></div>
  </div>
  <div id="bookmarks">
    <button class="bkm-btn save" id="btn-save-bkm">+ Save View</button>
    <div id="bkm-list"></div>
  </div>
  <div id="time-control">
    <span style="font-size:11px;color:#6b7d99">⏮</span>
    <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
    <span style="font-size:11px;color:#6b7d99">⏭</span>
    <span id="time-label">Day 0</span>
    <button id="btn-play" style="background:none;border:1px solid rgba(126,184,255,0.3);color:#7eb8ff;border-radius:4px;padding:4px 10px;cursor:pointer;font-size:12px">▶</button>
  </div>
  <div id="legend">
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#1a3a1a,#4ecb71,#f4d03f,#e67e22,#c0392b)"></span> Revenue (height + color)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#e74c3c"></span> Error river (&gt;8% rate)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#5dade2;border-radius:50%"></span> Data flow particles</div>
  </div>
  <div id="tooltip"></div>
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
const GRID = 60;
const TERRAIN_SIZE = 30;
const TIME_POINTS = 30;
const RIVER_THRESHOLD = 0.08;
const PARTICLE_COUNT = 800;
const container = document.body;
const tooltip = document.getElementById('tooltip');
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const btnPlay = document.getElementById('btn-play');
let playing = false;
let currentTimeIndex = 0;
let bookmarks = [];
let rafId;
let clock = new THREE.Clock();
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 25, 80);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(18, 16, 22);
camera.lookAt(0, 2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 2, 0);
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.45;
controls.update();
const ambientLight = new THREE.AmbientLight(0x2a3a5a, 1.4);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(20, 30, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x8899cc, 0.8);
fillLight.position.set(-10, 5, -10);
scene.add(fillLight);
function generateTimeSeriesData() {
  const frames = [];
  const baseSeed = 42;
  function pseudo(seed) { let s = seed; return () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; }; }
  const rng = pseudo(baseSeed);
  const plateauX = 0.35 + rng() * 0.3;
  const plateauZ = 0.35 + rng() * 0.3;
  const peakDriftX = new Array(TIME_POINTS).fill(0).map(() => (rng() - 0.5) * 0.1);
  const peakDriftZ = new Array(TIME_POINTS).fill(0).map(() => (rng() - 0.5) * 0.1);
  for (let t = 0; t < TIME_POINTS; t++) {
    const heights = new Float32Array(GRID * GRID);
    const users = new Float32Array(GRID * GRID);
    const errors = new Float32Array(GRID * GRID);
    const cx = plateauX + peakDriftX[t];
    const cz = plateauZ + peakDriftZ[t];
    const seasonality = 1 + 0.25 * Math.sin((t / TIME_POINTS) * Math.PI * 2);
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const nx = ix / (GRID - 1);
        const nz = iz / (GRID - 1);
        const dx = nx - cx;
        const dz = nz - cz;
        const dist = Math.sqrt(dx * dx + dz * dz);
        const gauss = Math.exp(-dist * dist * 6);
        const ridge = Math.exp(-Math.abs(dx) * 3) * (1 - Math.abs(dz - 0.5) * 1.5);
        const ripple = Math.sin(nx * 8) * Math.cos(nz * 6) * 0.08;
        const height = (gauss * 4.5 + ridge * 1.8 + ripple * 1.0) * seasonality * (0.8 + rng() * 0.4);
        heights[iz * GRID + ix] = Math.max(0.1, height);
        const userDensity = (gauss * 0.7 + Math.exp(-dist * dist * 2) * 0.3) * seasonality * (0.5 + rng() * 0.5);
        users[iz * GRID + ix] = Math.max(0.05, Math.min(1, userDensity));
        const errBase = (rng() < 0.06 ? 0.1 + rng() * 0.35 : rng() * 0.04);
        const errSpike = dist < 0.25 && rng() < 0.15 ? 0.12 + rng() * 0.3 : 0;
        errors[iz * GRID + ix] = Math.max(0.001, errBase + errSpike);
      }
    }
    frames.push({ heights, users, errors });
  }
  return frames;
}
const allFrames = generateTimeSeriesData();
timeSlider.max = TIME_POINTS - 1;
timeSlider.value = 0;
updateTimeLabel(0);
function getRevenueColor(value01) {
  const v = Math.max(0, Math.min(1, value01));
  const stops = [
    { pos: 0.00, r: 0.10, g: 0.20, b: 0.10 },
    { pos: 0.25, r: 0.15, g: 0.55, b: 0.20 },
    { pos: 0.50, r: 0.30, g: 0.75, b: 0.35 },
    { pos: 0.70, r: 0.85, g: 0.70, b: 0.20 },
    { pos: 0.90, r: 0.85, g: 0.40, b: 0.10 },
    { pos: 1.00, r: 0.75, g: 0.15, b: 0.15 },
  ];
  let lo = stops[0], hi = stops[stops.length - 1];
  for (let i = 0; i < stops.length - 1; i++) {
    if (v >= stops[i].pos && v <= stops[i + 1].pos) { lo = stops[i]; hi = stops[i + 1]; break; }
  }
  const t = lo.pos === hi.pos ? 0 : (v - lo.pos) / (hi.pos - lo.pos);
  return { r: lo.r + (hi.r - lo.r) * t, g: lo.g + (hi.g - lo.g) * t, b: lo.b + (hi.b - lo.b) * t };
}
const terrainGeo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, GRID - 1, GRID - 1);
terrainGeo.rotateX(-Math.PI / 2);
const colorsArr = new Float32Array(GRID * GRID * 3);
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.1,
  flatShading: false,
});
const terrain = new THREE.Mesh(terrainGeo, terrainMat);
terrain.castShadow = true;
terrain.receiveShadow = true;
scene.add(terrain);
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2, 30, 20, 64, 0x1a2a44, 0x1a2a44);
gridHelper.position.y = 0.02;
scene.add(gridHelper);
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const riverMaterial = new THREE.MeshStandardMaterial({
  color: 0xe74c3c,
  roughness: 0.3,
  metalness: 0.6,
  emissive: 0x330000,
  emissiveIntensity: 0.5,
});
function buildRiverGeometry(heights, errors, frameIdx) {
  while (riverGroup.children.length > 0) riverGroup.remove(riverGroup.children[0]);
  const visited = new Uint8Array(GRID * GRID);
  const directions = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  const allPaths = [];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      if (visited[idx] || errors[idx] < RIVER_THRESHOLD) continue;
      const path = [];
      let cx = ix, cz = iz;
      let steps = 0;
      while (steps < 80) {
        const cidx = cz * GRID + cx;
        if (cx < 0 || cx >= GRID || cz < 0 || cz >= GRID) break;
        if (visited[cidx] && steps > 0) break;
        visited[cidx] = 1;
        path.push({ ix: cx, iz: cz, h: heights[cidx], e: errors[cidx] });
        let bestDir = null, bestErr = -1;
        for (const [dx, dz] of directions) {
          const nx = cx + dx, nz = cz + dz;
          if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
          const nidx = nz * GRID + nx;
          if (errors[nidx] > bestErr) { bestErr = errors[nidx]; bestDir = [dx, dz]; }
        }
        if (!bestDir || bestErr < RIVER_THRESHOLD) break;
        cx += bestDir[0]; cz += bestDir[1];
        steps++;
      }
      if (path.length >= 4) allPaths.push(path);
    }
  }
  const half = TERRAIN_SIZE / 2;
  const stepX = TERRAIN_SIZE / (GRID - 1);
  const stepZ = TERRAIN_SIZE / (GRID - 1);
  for (const path of allPaths) {
    const points = path.map(p => new THREE.Vector3(
      p.ix * stepX - half,
      p.h * 1.05 + 0.15,
      p.iz * stepZ - half
    ));
    if (points.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
    const tubePoints = curve.getPoints(points.length * 2);
    for (let i = 1; i < tubePoints.length; i++) {
      const a = tubePoints[i - 1], b = tubePoints[i];
      const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5);
      const dir = new THREE.Vector3().subVectors(b, a);
      const len = dir.length();
      if (len < 0.01) continue;
      const cylGeo = new THREE.CylinderGeometry(0.08, 0.06, len, 6, 1);
      const cyl = new THREE.Mesh(cylGeo, riverMaterial);
      cyl.position.copy(mid);
      cyl.castShadow = true;
      const up = new THREE.Vector3(0, 1, 0);
      const quat = new THREE.Quaternion().setFromUnitVectors(up, dir.normalize());
      cyl.setRotationFromQuaternion(quat);
      riverGroup.add(cyl);
    }
  }
}
const particlesGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = new Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleData[i] = {
    pathIdx: Math.floor(Math.random() * 20),
    t: Math.random(),
    speed: 0.0003 + Math.random() * 0.0012,
    baseIx: Math.floor(Math.random() * GRID),
    baseIz: Math.floor(Math.random() * GRID),
    offset: (Math.random() - 0.5) * 0.8,
  };
  particlePositions[i * 3] = 0;
  particlePositions[i * 3 + 1] = -10;
  particlePositions[i * 3 + 2] = 0;
  particleColors[i * 3] = 0.36;
  particleColors[i * 3 + 1] = 0.68;
  particleColors[i * 3 + 2] = 0.89;
}
particlesGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particlesGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particlesMat = new THREE.PointsMaterial({
  size: 0.14,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.75,
});
const particles = new THREE.Points(particlesGeo, particlesMat);
scene.add(particles);
function updateTerrain(frameIdx) {
  const frame = allFrames[frameIdx];
  const posArr = terrainGeo.attributes.position.array;
  const stepX = TERRAIN_SIZE / (GRID - 1);
  const stepZ = TERRAIN_SIZE / (GRID - 1);
  const half = TERRAIN_SIZE / 2;
  let maxH = 0;
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const h = frame.heights[idx];
      if (h > maxH) maxH = h;
      const vi = idx * 3;
      posArr[vi + 1] = h;
      const users01 = frame.users[idx];
      const combined = h / 5.5 * 0.55 + users01 * 0.45;
      const col = getRevenueColor(Math.min(1, combined));
      colorsArr[vi] = col.r;
      colorsArr[vi + 1] = col.g;
      colorsArr[vi + 2] = col.b;
    }
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  const avgErr = frame.errors.reduce((a, b) => a + b, 0) / frame.errors.length;
  const avgUsers = frame.users.reduce((a, b) => a + b, 0) / frame.users.length;
  document.getElementById('val-revenue').textContent = '$' + (maxH * 2800).toFixed(0);
  document.getElementById('val-users').textContent = (avgUsers * 100).toFixed(1) + '%';
  document.getElementById('val-errors').textContent = (avgErr * 100).toFixed(2) + '%';
}
function updateRivers(frameIdx) {
  const frame = allFrames[frameIdx];
  buildRiverGeometry(frame.heights, frame.errors, frameIdx);
}
function updateAll(frameIdx) {
  updateTerrain(frameIdx);
  updateRivers(frameIdx);
}
updateAll(0);
function getTerrainHeight(ix, iz, frame) {
  const fx = Math.max(0, Math.min(GRID - 1, Math.round(ix)));
  const fz = Math.max(0, Math.min(GRID - 1, Math.round(iz)));
  return frame.heights[fz * GRID + fx];
}
function animate() {
  rafId = requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  const frame = allFrames[currentTimeIndex];
  const half = TERRAIN_SIZE / 2;
  const stepX = TERRAIN_SIZE / (GRID - 1);
  const stepZ = TERRAIN_SIZE / (GRID - 1);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    pd.t += pd.speed;
    if (pd.t > 1) { pd.t = 0; pd.baseIx = Math.floor(Math.random() * GRID); pd.baseIz = Math.floor(Math.random() * GRID); }
    let ix = pd.baseIx + Math.sin(pd.t * Math.PI * 2 + pd.offset) * 12;
    let iz = pd.baseIz + Math.cos(pd.t * Math.PI * 2 + pd.offset) * 12;
    ix = Math.max(0, Math.min(GRID - 1, ix));
    iz = Math.max(0, Math.min(GRID - 1, iz));
    const fi = Math.floor(ix), fj = Math.floor(iz);
    const fx = ix - fi, fz = iz - fj;
    const ci = Math.min(fi, GRID - 2), cj = Math.min(fj, GRID - 2);
    const h00 = frame.heights[cj * GRID + ci];
    const h10 = frame.heights[cj * GRID + Math.min(ci + 1, GRID - 1)];
    const h01 = frame.heights[Math.min(cj + 1, GRID - 1) * GRID + ci];
    const h11 = frame.heights[Math.min(cj + 1, GRID - 1) * GRID + Math.min(ci + 1, GRID - 1)];
    const h = (h00 * (1 - fx) + h10 * fx) * (1 - fz) + (h01 * (1 - fx) + h11 * fx) * fz;
    const wx = ix * stepX - half;
    const wz = iz * stepZ - half;
    const pi = i * 3;
    particlePositions[pi] = wx;
    particlePositions[pi + 1] = h + 0.3 + Math.sin(pd.t * 6) * 0.15;
    particlePositions[pi + 2] = wz;
  }
  particlesGeo.attributes.position.needsUpdate = true;
  if (playing) {
    const next = (currentTimeIndex + 1) % TIME_POINTS;
    setTimeIndex(next);
  }
}
function setTimeIndex(idx) {
  currentTimeIndex = idx;
  timeSlider.value = idx;
  updateAll(idx);
  updateTimeLabel(idx);
}
function updateTimeLabel(idx) {
  timeLabel.textContent = 'Day ' + (idx + 1);
}
timeSlider.addEventListener('input', () => {
  playing = false;
  btnPlay.textContent = '▶';
  setTimeIndex(parseInt(timeSlider.value));
});
btnPlay.addEventListener('click', () => {
  playing = !playing;
  btnPlay.textContent = playing ? '⏸' : '▶';
});
function saveBookmark() {
  const pos = camera.position.clone();
  const target = controls.target.clone();
  const tIdx = currentTimeIndex;
  const name = 'View ' + (bookmarks.length + 1) + ' (Day ' + (tIdx + 1) + ')';
  bookmarks.push({ name, pos, target, timeIndex: tIdx });
  renderBookmarks();
}
function gotoBookmark(index) {
  const bm = bookmarks[index];
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.pos.clone();
  const endTarget = bm.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animStep);
  }
  requestAnimationFrame(animStep);
  setTimeIndex(bm.timeIndex);
}
function deleteBookmark(index) {
  bookmarks.splice(index, 1);
  renderBookmarks();
}
function renderBookmarks() {
  const list = document.getElementById('bkm-list');
  list.innerHTML = bookmarks.map((bm, i) =>
    '<button class="bkm-btn" data-idx="' + i + '">' + bm.name +
    '<span style="float:right;opacity:0.5;margin-left:8px;font-size:10px" data-del="' + i + '">✕</span></button>'
  ).join('');
  list.querySelectorAll('.bkm-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      if (e.target.dataset.del !== undefined) {
        deleteBookmark(parseInt(e.target.dataset.del));
        return;
      }
      gotoBookmark(parseInt(btn.dataset.idx));
    });
  });
}
document.getElementById('btn-save-bkm').addEventListener('click', saveBookmark);
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r': controls.autoRotate = !controls.autoRotate; break;
    case 'f': controls.target.set(0, 2, 0); camera.position.set(18, 16, 22); controls.update(); break;
    case 'arrowleft': setTimeIndex(Math.max(0, currentTimeIndex - 1)); playing = false; btnPlay.textContent = '▶'; break;
    case 'arrowright': setTimeIndex(Math.min(TIME_POINTS - 1, currentTimeIndex + 1)); playing = false; btnPlay.textContent = '▶'; break;
    case ' ': e.preventDefault(); playing = !playing; btnPlay.textContent = playing ? '⏸' : '▶'; break;
    case 's': if (!e.ctrlKey && !e.metaKey) { saveBookmark(); } break;
  }
});
renderBookmarks();
animate();
console.log('3D Data Terrain Explorer ready — drag to orbit, scroll to zoom, right-drag to pan, R to toggle auto-rotate, Space to play/pause, S to save bookmark, ← → to scrub time');
</script>
</body>
</html>