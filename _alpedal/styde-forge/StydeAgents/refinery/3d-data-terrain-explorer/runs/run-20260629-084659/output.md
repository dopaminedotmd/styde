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
  #ui{position:fixed;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:10}
  #ui>*{pointer-events:auto}
  #time-panel{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(10,10,30,0.85);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:14px 20px;display:flex;align-items:center;gap:12px;backdrop-filter:blur(10px)}
  #time-panel label{color:#aab;font-size:12px;text-transform:uppercase;letter-spacing:1px;white-space:nowrap}
  #time-slider{width:280px;accent-color:#5af}
  #time-value{color:#fff;font-size:13px;font-weight:600;min-width:60px;text-align:center}
  #bookmarks{position:absolute;top:20px;right:20px;display:flex;flex-direction:column;gap:6px}
  #bookmarks button{background:rgba(10,10,30,0.8);border:1px solid rgba(255,255,255,0.15);color:#ccd;padding:8px 14px;border-radius:8px;cursor:pointer;font-size:12px;transition:all 0.2s;backdrop-filter:blur(8px)}
  #bookmarks button:hover{background:rgba(40,40,80,0.9);border-color:rgba(100,160,255,0.4);color:#fff}
  #diag-panel{position:absolute;top:20px;left:20px;background:rgba(10,10,30,0.82);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:12px 16px;font-size:11px;color:#8af;backdrop-filter:blur(8px);line-height:1.7;min-width:180px}
  #diag-panel .label{color:#68a;text-transform:uppercase;letter-spacing:0.5px}
  #diag-panel .val{color:#adf;font-weight:600}
  #diag-panel .miss{color:#f66}
  #legend{position:absolute;bottom:100px;left:20px;display:flex;flex-direction:column;gap:4px;font-size:10px;color:#889}
  #legend span{display:flex;align-items:center;gap:6px}
  #legend .swatch{width:12px;height:12px;border-radius:3px}
</style>
</head>
<body>
<div id="ui">
  <div id="diag-panel">
    <div><span class="label">FPS</span> <span class="val" id="diag-fps">0</span></div>
    <div><span class="label">Time step</span> <span class="val" id="diag-step">0/0</span></div>
    <div><span class="label">Terrain cache</span> <span class="val" id="diag-terrain">H:0 M:0</span></div>
    <div><span class="label">River cache</span> <span class="val" id="diag-river">H:0 M:0</span></div>
    <div><span class="label">Grid xform</span> <span class="val" id="diag-xform">H:0 M:0</span></div>
    <div><span class="label">Particles</span> <span class="val" id="diag-particles">0</span></div>
  </div>
  <div id="bookmarks">
    <button data-bookmark="overview">Overview</button>
    <button data-bookmark="peak1">Revenue Peak</button>
    <button data-bookmark="valley">Error Valley</button>
    <button data-bookmark="flow">Flow Trail</button>
  </div>
  <div id="legend">
    <span><span class="swatch" style="background:#2d8"></span>Elevation: Revenue</span>
    <span><span class="swatch" style="background:#4a8"></span>Green: User Density</span>
    <span><span class="swatch" style="background:#e44"></span>Red Rivers: Errors</span>
    <span><span class="swatch" style="background:#fc0"></span>Gold Particles: API Flow</span>
  </div>
  <div id="time-panel">
    <label>Time</label>
    <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
    <span id="time-value">Day 1</span>
  </div>
</div>
<script type="importmap">
{"imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 80;
const STEPS = 30;
const WORLD_SIZE = 40;
const CELL = WORLD_SIZE / GRID;
const PARTICLE_COUNT = 600;
const ERROR_THRESHOLD = 0.55;
const RIVER_DEBOUNCE = 200;
const terrainCache = new Map();
const riverCache = new Map();
let terrainHits = 0, terrainMisses = 0;
let riverHits = 0, riverMisses = 0;
let xformHits = 0, xformMisses = 0;
const xformCache = new Map();
let lastXformClear = 0;
const heightfields = [];
const userDensityFields = [];
const errorFields = [];
function hash3(x, y, z) {
  let h = 0;
  for (const v of [x, y, z]) {
    const buf = new ArrayBuffer(4);
    new Float32Array(buf)[0] = v;
    h = ((h << 5) - h + new Int32Array(buf)[0]) | 0;
  }
  return h;
}
function noise2d(x, y) {
  const n = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453;
  return n - Math.floor(n);
}
function smoothNoise(x, y) {
  const ix = Math.floor(x), iy = Math.floor(y);
  const fx = x - ix, fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx);
  const sy = fy * fy * (3 - 2 * fy);
  const n00 = noise2d(ix, iy);
  const n10 = noise2d(ix + 1, iy);
  const n01 = noise2d(ix, iy + 1);
  const n11 = noise2d(ix + 1, iy + 1);
  const nx0 = n00 + (n10 - n00) * sx;
  const nx1 = n01 + (n11 - n01) * sx;
  return nx0 + (nx1 - nx0) * sy;
}
function fbm(x, y, octaves = 3) {
  let val = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    val += smoothNoise(x * freq, y * freq) * amp;
    max += amp;
    amp *= 0.5;
    freq *= 2;
  }
  return val / max;
}
for (let t = 0; t < STEPS; t++) {
  const phase = t / (STEPS - 1);
  const hf = new Float32Array(GRID * GRID);
  const ud = new Float32Array(GRID * GRID);
  const er = new Float32Array(GRID * GRID);
  const cx1 = 0.3 + phase * 0.4, cy1 = 0.35 + Math.sin(phase * 2.5) * 0.15;
  const cx2 = 0.65 - phase * 0.3, cy2 = 0.6 + Math.cos(phase * 1.8) * 0.2;
  const cx3 = 0.5 + Math.sin(phase * 3) * 0.25, cy3 = 0.5 + Math.cos(phase * 2.2) * 0.25;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const nx = ix / GRID, ny = iy / GRID;
      const d1 = Math.hypot(nx - cx1, ny - cy1);
      const d2 = Math.hypot(nx - cx2, ny - cy2);
      const d3 = Math.hypot(nx - cx3, ny - cy3);
      const peak1 = Math.exp(-d1 * d1 * 18) * (0.7 + phase * 0.3);
      const peak2 = Math.exp(-d2 * d2 * 22) * (0.9 - phase * 0.4);
      const peak3 = Math.exp(-d3 * d3 * 25) * (0.4 + Math.sin(phase * 4) * 0.25);
      const detail = fbm(nx * 5, ny * 5, 3) * 0.12;
      hf[idx] = peak1 * 1.2 + peak2 * 0.9 + peak3 * 0.55 + detail;
      ud[idx] = peak1 * 0.7 + peak2 * 0.5 + peak3 * 0.3 + fbm(nx * 3 + 1.7, ny * 3 + 1.7, 2) * 0.3;
      const errBase = (fbm(nx * 4 + 3.1, ny * 4 + 3.1, 2) - 0.3) * 0.5;
      const errBoost = d3 < 0.12 ? (0.12 - d3) * 5 * (0.4 + phase * 0.6) : 0;
      er[idx] = Math.max(0, Math.min(1, errBase + errBoost));
    }
  }
  heightfields.push(hf);
  userDensityFields.push(ud);
  errorFields.push(er);
}
function worldToGrid(wx, wz) {
  const gx = Math.floor((wx + WORLD_SIZE / 2) / CELL);
  const gz = Math.floor((wz + WORLD_SIZE / 2) / CELL);
  if (gx < 0 || gx >= GRID || gz < 0 || gz >= GRID) return null;
  return { gx, gz };
}
function gridToWorld(gx, gz) {
  return {
    x: gx * CELL - WORLD_SIZE / 2 + CELL / 2,
    z: gz * CELL - WORLD_SIZE / 2 + CELL / 2,
  };
}
function getHeightField(timeIndex) {
  return heightfields[Math.min(timeIndex, STEPS - 1)];
}
function buildTerrainGeometry(timeIndex) {
  const hf = getHeightField(timeIndex);
  const ud = userDensityFields[Math.min(timeIndex, STEPS - 1)];
  const vertCount = (GRID + 1) * (GRID + 1);
  const positions = new Float32Array(vertCount * 3);
  const colors = new Float32Array(vertCount * 3);
  for (let iz = 0; iz <= GRID; iz++) {
    for (let ix = 0; ix <= GRID; ix++) {
      const vi = iz * (GRID + 1) + ix;
      const gx = Math.min(ix, GRID - 1), gz = Math.min(iz, GRID - 1);
      const h = hf[gz * GRID + gx];
      const d = ud[gz * GRID + gx];
      const wx = ix * CELL - WORLD_SIZE / 2;
      const wz = iz * CELL - WORLD_SIZE / 2;
      positions[vi * 3] = wx;
      positions[vi * 3 + 1] = h * 6;
      positions[vi * 3 + 2] = wz;
      const r = 0.1 + h * 0.5 + d * 0.3;
      const g = 0.15 + h * 0.3 + d * 0.7;
      const b = 0.2 + h * 0.4;
      colors[vi * 3] = r;
      colors[vi * 3 + 1] = g;
      colors[vi * 3 + 2] = b;
    }
  }
  const indices = [];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const a = iz * (GRID + 1) + ix;
      const b = a + 1;
      const c = a + (GRID + 1);
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
function getTerrainGeometry(timeIndex) {
  if (terrainCache.has(timeIndex)) { terrainHits++; return terrainCache.get(timeIndex); }
  terrainMisses++;
  const geo = buildTerrainGeometry(timeIndex);
  terrainCache.set(timeIndex, geo);
  return geo;
}
function traceErrorPaths(timeIndex) {
  const er = errorFields[Math.min(timeIndex, STEPS - 1)];
  const visited = new Uint8Array(GRID * GRID);
  const paths = [];
  const dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]];
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      if (visited[idx] || er[idx] < ERROR_THRESHOLD) continue;
      const path = [];
      let cx = ix, cy = iy;
      let steps = 0;
      while (steps < 200) {
        const cidx = cy * GRID + cx;
        if (visited[cidx]) break;
        visited[cidx] = 1;
        path.push({ gx: cx, gz: cy });
        let bestDir = null, bestErr = -1;
        for (const [dx, dy] of dirs) {
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          const nidx = ny * GRID + nx;
          if (visited[nidx]) continue;
          if (er[nidx] > bestErr) { bestErr = er[nidx]; bestDir = [nx, ny]; }
        }
        if (!bestDir || bestErr < ERROR_THRESHOLD) break;
        cx = bestDir[0]; cy = bestDir[1];
        steps++;
      }
      if (path.length >= 3) paths.push(path);
    }
  }
  return paths;
}
function buildRiverGeometry(timeIndex) {
  const paths = traceErrorPaths(timeIndex);
  const hf = getHeightField(timeIndex);
  const group = new THREE.Group();
  const riverMat = new THREE.MeshBasicMaterial({ color: 0xe04444, transparent: true, opacity: 0.8 });
  const glowMat = new THREE.MeshBasicMaterial({ color: 0xff6644, transparent: true, opacity: 0.3 });
  for (const path of paths) {
    const pts = path.map(p => {
      const w = gridToWorld(p.gx, p.gz);
      const h = hf[p.gz * GRID + p.gx] * 6 + 0.08;
      return new THREE.Vector3(w.x, h, w.z);
    });
    if (pts.length < 2) continue;
    const curve = new THREE.CatmullRomCurve3(pts);
    const tubeGeo = new THREE.TubeGeometry(curve, pts.length * 2, 0.12, 6, false);
    const tube = new THREE.Mesh(tubeGeo, riverMat);
    group.add(tube);
    const glowGeo = new THREE.TubeGeometry(curve, pts.length * 2, 0.3, 4, false);
    const glow = new THREE.Mesh(glowGeo, glowMat);
    group.add(glow);
  }
  return group;
}
function getRiverGeometry(timeIndex) {
  if (riverCache.has(timeIndex)) { riverHits++; return riverCache.get(timeIndex).clone(); }
  riverMisses++;
  const group = buildRiverGeometry(timeIndex);
  riverCache.set(timeIndex, group);
  return group.clone();
}
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 20, 60);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 120);
camera.position.set(22, 14, 22);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);
const ambientLight = new THREE.AmbientLight(0x223344, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 80;
sunLight.shadow.camera.left = -25;
sunLight.shadow.camera.right = 25;
sunLight.shadow.camera.top = 25;
sunLight.shadow.camera.bottom = -25;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466aa, 1.2);
fillLight.position.set(-8, 3, -6);
scene.add(fillLight);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(getTerrainGeometry(0), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
const wireframeMat = new THREE.MeshBasicMaterial({ color: 0x334466, wireframe: true, transparent: true, opacity: 0.08 });
const wireframeMesh = new THREE.Mesh(getTerrainGeometry(0), wireframeMat);
scene.add(wireframeMesh);
let riverGroup = getRiverGeometry(0);
scene.add(riverGroup);
const groundGeo = new THREE.PlaneGeometry(WORLD_SIZE * 1.5, WORLD_SIZE * 1.5);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x111122, roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.5;
ground.receiveShadow = true;
scene.add(ground);
const gridHelper = new THREE.GridHelper(WORLD_SIZE, GRID, 0x223344, 0x111a22);
gridHelper.position.y = -0.49;
scene.add(gridHelper);
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = [];
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const gx = Math.random() * (GRID - 1);
  const gz = Math.random() * (GRID - 1);
  const w = gridToWorld(gx, gz);
  particlePositions[i * 3] = w.x;
  particlePositions[i * 3 + 1] = 0.15;
  particlePositions[i * 3 + 2] = w.z;
  particleColors[i * 3] = 1;
  particleColors[i * 3 + 1] = 0.75;
  particleColors[i * 3 + 2] = 0.15;
  particleData.push({
    gx, gz,
    vx: (Math.random() - 0.5) * 0.03,
    vz: (Math.random() - 0.5) * 0.03,
    life: Math.random(),
  });
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.18,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.85,
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 1.5, 0);
controls.minDistance = 5;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
const bookmarks = {
  overview: { pos: new THREE.Vector3(22, 14, 22), target: new THREE.Vector3(0, 1.5, 0) },
  peak1: { pos: new THREE.Vector3(8, 5, 2), target: new THREE.Vector3(4, 3, 4) },
  valley: { pos: new THREE.Vector3(-6, 3, -8), target: new THREE.Vector3(-8, 1, -10) },
  flow: { pos: new THREE.Vector3(0, 2.5, 14), target: new THREE.Vector3(0, 1.5, -5) },
};
let cameraAnimTarget = null;
let cameraAnimStartPos = null;
let cameraAnimStartTarget = null;
let cameraAnimT = 0;
const CAMERA_ANIM_DURATION = 0.8;
document.querySelectorAll('#bookmarks button').forEach(btn => {
  btn.addEventListener('click', () => {
    const bm = bookmarks[btn.dataset.bookmark];
    if (!bm) return;
    cameraAnimStartPos = camera.position.clone();
    cameraAnimStartTarget = controls.target.clone();
    cameraAnimTarget = bm;
    cameraAnimT = 0;
  });
});
let currentTimeIndex = 0;
let riverDebounceTimer = null;
let pendingRiverUpdate = false;
function swapTerrain(timeIndex) {
  const geo = getTerrainGeometry(timeIndex);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = geo;
  wireframeMesh.geometry.dispose();
  wireframeMesh.geometry = geo;
}
function updateRivers(timeIndex) {
  if (riverGroup) {
    riverGroup.traverse(child => { if (child.geometry) child.geometry.dispose(); });
    scene.remove(riverGroup);
  }
  riverGroup = getRiverGeometry(timeIndex);
  scene.add(riverGroup);
}
function scheduleRiverUpdate(timeIndex) {
  pendingRiverUpdate = timeIndex;
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (pendingRiverUpdate !== null) {
      updateRivers(pendingRiverUpdate);
      pendingRiverUpdate = null;
    }
  }, RIVER_DEBOUNCE);
}
const slider = document.getElementById('time-slider');
const timeValueEl = document.getElementById('time-value');
slider.addEventListener('input', () => {
  const ti = parseInt(slider.value);
  currentTimeIndex = ti;
  timeValueEl.textContent = `Day ${ti + 1}`;
  swapTerrain(ti);
  scheduleRiverUpdate(ti);
});
function updateParticles(dt) {
  const hf = getHeightField(currentTimeIndex);
  const posArr = particles.geometry.attributes.position.array;
  const colArr = particles.geometry.attributes.color.array;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    pd.life += dt * 0.15;
    if (pd.life > 1) {
      pd.life = 0;
      pd.gx = Math.random() * (GRID - 1);
      pd.gz = Math.random() * (GRID - 1);
      const w = gridToWorld(pd.gx, pd.gz);
      posArr[i * 3] = w.x;
      posArr[i * 3 + 2] = w.z;
    }
    let ngx = pd.gx + pd.vx, ngz = pd.gz + pd.vz;
    if (ngx < 0) ngx += GRID - 1;
    if (ngx >= GRID) ngx -= GRID - 1;
    if (ngz < 0) ngz += GRID - 1;
    if (ngz >= GRID) ngz -= GRID - 1;
    const igx = Math.floor(ngx), igz = Math.floor(ngz);
    const cgx = Math.min(igx, GRID - 1), cgz = Math.min(igz, GRID - 1);
    const currH = hf[Math.floor(pd.gz) * GRID + Math.floor(pd.gx)];
    const nextH = hf[cgz * GRID + cgx];
    if (nextH <= currH + 0.15) {
      pd.gx = ngx;
      pd.gz = ngz;
    }
    const w = gridToWorld(pd.gx, pd.gz);
    const h = hf[cgz * GRID + cgx] * 6 + 0.25;
    posArr[i * 3] = w.x;
    posArr[i * 3 + 1] = h;
    posArr[i * 3 + 2] = w.z;
    const lifeFade = 1 - Math.abs(pd.life - 0.5) * 2;
    colArr[i * 3] = 1;
    colArr[i * 3 + 1] = 0.6 + lifeFade * 0.4;
    colArr[i * 3 + 2] = lifeFade * 0.3;
  }
  particles.geometry.attributes.position.needsUpdate = true;
  particles.geometry.attributes.color.needsUpdate = true;
}
const clock = new THREE.Clock();
let fpsFrames = 0, fpsTime = 0, currentFps = 0;
function updateDiagnostics() {
  document.getElementById('diag-fps').textContent = currentFps;
  document.getElementById('diag-step').textContent = `${currentTimeIndex + 1}/${STEPS}`;
  document.getElementById('diag-terrain').innerHTML = `H:<span class="val">${terrainHits}</span> M:<span class="miss">${terrainMisses}</span>`;
  document.getElementById('diag-river').innerHTML = `H:<span class="val">${riverHits}</span> M:<span class="miss">${riverMisses}</span>`;
  document.getElementById('diag-xform').innerHTML = `H:<span class="val">${xformHits}</span> M:<span class="miss">${xformMisses}</span>`;
  document.getElementById('diag-particles').textContent = PARTICLE_COUNT;
}
function animate(timestamp) {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  fpsFrames++;
  fpsTime += dt;
  if (fpsTime >= 0.5) {
    currentFps = Math.round(fpsFrames / fpsTime);
    fpsFrames = 0;
    fpsTime = 0;
  }
  if (cameraAnimTarget) {
    cameraAnimT += dt / CAMERA_ANIM_DURATION;
    if (cameraAnimT >= 1) {
      cameraAnimT = 1;
      camera.position.copy(cameraAnimTarget.pos);
      controls.target.copy(cameraAnimTarget.target);
      cameraAnimTarget = null;
    } else {
      const t = cameraAnimT;
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      camera.position.lerpVectors(cameraAnimStartPos, cameraAnimTarget.pos, ease);
      controls.target.lerpVectors(cameraAnimStartTarget, cameraAnimTarget.target, ease);
    }
  }
  controls.update();
  updateParticles(dt);
  if (timestamp - lastXformClear > 1000) {
    xformCache.clear();
    lastXformClear = timestamp;
  }
  if (Math.floor(timestamp / 500) !== Math.floor((timestamp - dt * 1000) / 500)) {
    updateDiagnostics();
  }
  renderer.render(scene, camera);
}
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
updateDiagnostics();
requestAnimationFrame(animate);
</script>
</body>
</html>