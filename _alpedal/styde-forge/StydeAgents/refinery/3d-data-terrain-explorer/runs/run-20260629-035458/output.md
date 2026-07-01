<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0a0f; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8ccd4; }
#container { position: fixed; inset: 0; z-index: 0; }
#ui { position: fixed; z-index: 10; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 12px; align-items: flex-end; }
#panel { background: rgba(10,10,20,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 20px; display: flex; flex-direction: column; gap: 10px; min-width: 340px; }
#panel .row { display: flex; align-items: center; gap: 10px; }
#panel label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #7a7f8c; white-space: nowrap; }
#timeSlider { flex: 1; -webkit-appearance: none; height: 4px; background: #2a2d38; border-radius: 2px; outline: none; cursor: pointer; }
#timeSlider::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; border-radius: 50%; background: #5b8def; border: 2px solid #1a1d28; cursor: pointer; }
#timeLabel { font-size: 13px; font-weight: 600; color: #e0e4f0; min-width: 70px; text-align: right; }
#bookmarks { display: flex; gap: 6px; flex-wrap: wrap; }
#bookmarks button, .action-btn { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); color: #b0b8cc; padding: 5px 10px; border-radius: 6px; font-size: 11px; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
#bookmarks button:hover, .action-btn:hover { background: rgba(255,255,255,0.1); color: #fff; border-color: rgba(255,255,255,0.2); }
.action-btn.active { background: rgba(91,141,239,0.2); border-color: #5b8def; color: #5b8def; }
#legend { position: fixed; top: 20px; right: 20px; z-index: 10; background: rgba(10,10,20,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 16px; font-size: 10px; }
#legend .item { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
#legend .swatch { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
#tooltip { position: fixed; pointer-events: none; z-index: 20; background: rgba(0,0,0,0.85); border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 6px 10px; font-size: 11px; display: none; white-space: nowrap; }
#stats { position: fixed; top: 20px; left: 20px; z-index: 10; font-size: 10px; color: #5a5f70; display: flex; gap: 16px; }
</style>
</head>
<body>
<div id="container"></div>
<div id="tooltip"></div>
<div id="legend">
  <div style="font-weight:600;margin-bottom:6px;color:#e0e4f0">LEGEND</div>
  <div class="item"><span class="swatch" style="background:linear-gradient(180deg,#4a9,#296);"></span> Revenue (elevation)</div>
  <div class="item"><span class="swatch" style="background:linear-gradient(90deg,#2255cc,#33aa55,#ffaa00,#ff3344);"></span> User Density (color)</div>
  <div class="item"><span class="swatch" style="background:#ff3344;box-shadow:0 0 6px #ff3344;"></span> Error Rivers</div>
  <div class="item"><span class="swatch" style="background:#ffcc44;box-shadow:0 0 4px #ffcc44;"></span> API Flow Particles</div>
</div>
<div id="stats"><span id="fps">FPS: --</span><span id="vertCount">Verts: --</span><span id="particleCount">Particles: --</span></div>
<div id="ui">
  <div id="panel">
    <div class="row">
      <label>Time</label>
      <input type="range" id="timeSlider" min="0" max="11" value="0" step="1">
      <span id="timeLabel">T0</span>
    </div>
    <div id="bookmarks">
      <button data-bookmark="overview">Overview</button>
      <button data-bookmark="north">North Peak</button>
      <button data-bookmark="valley">Error Valley</button>
      <button data-bookmark="flow">Flow Corridor</button>
    </div>
    <div class="row" style="justify-content:space-between">
      <button id="btnAutoRotate" class="action-btn">Auto-Rotate</button>
      <button id="btnWireframe" class="action-btn">Wireframe</button>
      <button id="btnReset" class="action-btn">Reset</button>
    </div>
  </div>
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
const GRID = 128;
const TIMEPOINTS = 12;
const TERRAIN_SIZE = 20;
const MAX_HEIGHT = 8;
function lerp(a, b, t) { return a + (b - a) * t; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function smoothstep(edge0, edge1, x) { const t = clamp((x - edge0) / (edge1 - edge0), 0, 1); return t * t * (3 - 2 * t); }
let perm;
function seedPRNG(s) {
  perm = new Uint8Array(512);
  const p = new Uint8Array(256);
  for (let i = 0; i < 256; i++) p[i] = i;
  let ss = s;
  for (let i = 255; i > 0; i--) {
    ss = (ss * 16807 + 0) % 2147483647;
    const j = ss % (i + 1);
    [p[i], p[j]] = [p[j], p[i]];
  }
  for (let i = 0; i < 512; i++) perm[i] = p[i & 255];
}
function noise2D(x, y) {
  const X = Math.floor(x) & 255;
  const Y = Math.floor(y) & 255;
  const xf = x - Math.floor(x);
  const yf = y - Math.floor(y);
  const u = smoothstep(0, 1, xf);
  const v = smoothstep(0, 1, yf);
  const a = perm[perm[X] + Y];
  const b = perm[perm[X + 1] + Y];
  const c = perm[perm[X] + Y + 1];
  const d = perm[perm[X + 1] + Y + 1];
  return lerp(lerp(a / 255, b / 255, u), lerp(c / 255, d / 255, u), v);
}
function fbm(x, y, octaves, lacunarity, gain) {
  let val = 0, amp = 1, freq = 1, maxVal = 0;
  for (let i = 0; i < octaves; i++) {
    val += amp * noise2D(x * freq, y * freq);
    maxVal += amp;
    amp *= gain;
    freq *= lacunarity;
  }
  return val / maxVal;
}
seedPRNG(42);
function generateTimepoint(t) {
  const toff = t * 0.7;
  const revenue = new Float32Array(GRID * GRID);
  const userDensity = new Float32Array(GRID * GRID);
  const errorPaths = [];
  const apiFlows = [];
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const nx = ix / GRID;
      const ny = iy / GRID;
      const idx = iy * GRID + ix;
      const r1 = fbm(nx * 4 + toff * 0.3, ny * 3.5, 5, 2.0, 0.55);
      const r2 = fbm(nx * 2.5 - toff * 0.15, ny * 2.2 + 1.3, 3, 2.3, 0.5);
      const ridge = 1 - Math.abs(fbm(nx * 3 + 2, ny * 3 - 1, 4, 2.1, 0.5) * 2 - 1);
      const valley = Math.sin(nx * Math.PI * 1.5 + toff * 0.2) * Math.cos(ny * Math.PI * 1.7 + toff * 0.25);
      let h = r1 * 0.55 + r2 * 0.3 + ridge * 0.1 + valley * 0.05;
      h = clamp(h, 0, 1);
      revenue[idx] = h;
      const d1 = fbm(nx * 3.8 + toff * 0.2 + 1.7, ny * 3.3 + 0.9, 4, 2.2, 0.5);
      const d2 = fbm(nx * 5 + toff * 0.35, ny * 4.5 - toff * 0.1, 3, 2.0, 0.6);
      userDensity[idx] = clamp(d1 * 0.6 + d2 * 0.4, 0, 1);
    }
  }
  const errorCount = 3 + Math.floor(Math.abs(Math.sin(toff * 1.3)) * 5);
  for (let e = 0; e < errorCount; e++) {
    const seedE = t * 100 + e * 17;
    const startX = (noise2D(seedE * 0.1, 0) * 0.7 + 0.15) * GRID;
    const startY = (noise2D(0, seedE * 0.1) * 0.6 + 0.2) * GRID;
    const points = [];
    let cx = startX, cy = startY;
    const steps = 30 + Math.floor(noise2D(seedE * 0.3, 1) * 40);
    for (let s = 0; s < steps; s++) {
      const frac = s / steps;
      const ang = noise2D(seedE + frac * 3, 2) * Math.PI * 2;
      cx += Math.cos(ang) * (1 + noise2D(seedE, frac) * 3);
      cy += Math.sin(ang) * (1.5 + noise2D(seedE + 1, frac) * 2);
      cx = clamp(cx, 0, GRID - 1);
      cy = clamp(cy, 0, GRID - 1);
      const ix = Math.round(cx);
      const iy = Math.round(cy);
      const ridx = iy * GRID + ix;
      const h = revenue[ridx] * MAX_HEIGHT + 0.15;
      points.push({ x: (ix / GRID - 0.5) * TERRAIN_SIZE, y: h, z: (iy / GRID - 0.5) * TERRAIN_SIZE });
    }
    errorPaths.push(points);
  }
  const flowCount = 40 + Math.floor(noise2D(t * 0.5, 42) * 60);
  for (let f = 0; f < flowCount; f++) {
    const seedF = t * 1000 + f * 31;
    const sx = (noise2D(seedF * 0.07, 0) * 0.8 + 0.1) * GRID;
    const sy = (noise2D(0, seedF * 0.07) * 0.8 + 0.1) * GRID;
    const sxi = clamp(Math.round(sx), 0, GRID - 1);
    const syi = clamp(Math.round(sy), 0, GRID - 1);
    const sh = revenue[syi * GRID + sxi] * MAX_HEIGHT;
    const ex = sx + (noise2D(seedF * 0.13, 1) - 0.5) * GRID * 0.5;
    const ey = sy + (noise2D(seedF * 0.13, 2) - 0.5) * GRID * 0.5;
    const exi = clamp(Math.round(ex), 0, GRID - 1);
    const eyi = clamp(Math.round(ey), 0, GRID - 1);
    const eh = revenue[eyi * GRID + exi] * MAX_HEIGHT;
    apiFlows.push({
      sx: (sx / GRID - 0.5) * TERRAIN_SIZE,
      sy: sh + 0.3,
      sz: (sy / GRID - 0.5) * TERRAIN_SIZE,
      ex: (ex / GRID - 0.5) * TERRAIN_SIZE,
      ey: eh + 0.3,
      ez: (ey / GRID - 0.5) * TERRAIN_SIZE,
      speed: 0.3 + noise2D(seedF * 0.2, 3) * 0.7,
      phase: noise2D(seedF * 0.2, 4),
    });
  }
  return { revenue, userDensity, errorPaths, apiFlows };
}
const allTimepoints = [];
for (let t = 0; t < TIMEPOINTS; t++) {
  allTimepoints.push(generateTimepoint(t));
}
function buildTerrainGeometry(tp) {
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const i3 = idx * 3;
      const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const z = (iy / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const h = tp.revenue[idx] * MAX_HEIGHT;
      positions[i3] = x;
      positions[i3 + 1] = h;
      positions[i3 + 2] = z;
      const d = tp.userDensity[idx];
      let r, g, b;
      if (d < 0.25) { r = lerp(0.08, 0.15, d / 0.25); g = lerp(0.2, 0.45, d / 0.25); b = lerp(0.7, 0.65, d / 0.25); }
      else if (d < 0.5) { const t = (d - 0.25) / 0.25; r = lerp(0.15, 0.25, t); g = lerp(0.45, 0.7, t); b = lerp(0.65, 0.25, t); }
      else if (d < 0.75) { const t = (d - 0.5) / 0.25; r = lerp(0.25, 0.9, t); g = lerp(0.7, 0.68, t); b = lerp(0.25, 0.05, t); }
      else { const t = (d - 0.75) / 0.25; r = lerp(0.9, 1.0, t); g = lerp(0.68, 0.15, t); b = lerp(0.05, 0.1, t); }
      colors[i3] = r;
      colors[i3 + 1] = g;
      colors[i3 + 2] = b;
    }
  }
  const indices = [];
  for (let iy = 0; iy < GRID - 1; iy++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iy * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
function buildRiverLines(tp) {
  const group = new THREE.Group();
  for (const path of tp.errorPaths) {
    if (path.length < 2) continue;
    const pts = path.map(p => new THREE.Vector3(p.x, p.y, p.z));
    const curve = new THREE.CatmullRomCurve3(pts);
    const curvePts = curve.getPoints(path.length * 4);
    const lineGeo = new THREE.BufferGeometry().setFromPoints(curvePts);
    const lineMat = new THREE.LineBasicMaterial({ color: 0xff2244, linewidth: 1, transparent: true, opacity: 0.85, depthTest: true });
    const line = new THREE.Line(lineGeo, lineMat);
    group.add(line);
    const glowGeo = new THREE.BufferGeometry().setFromPoints(curvePts);
    const glowMat = new THREE.LineBasicMaterial({ color: 0xff4466, linewidth: 1, transparent: true, opacity: 0.25, depthTest: false });
    const glow = new THREE.Line(glowGeo, glowMat);
    glow.renderOrder = 999;
    group.add(glow);
  }
  return group;
}
const terrainGeos = allTimepoints.map(tp => buildTerrainGeometry(tp));
const riverGroups = allTimepoints.map(tp => buildRiverLines(tp));
const container = document.getElementById('container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.FogExp2(0x0a0a14, 0.00025);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(12, 9, 14);
camera.lookAt(0, 2.5, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 2.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.55;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 1.6);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(15, 18, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x6699cc, 0.8);
fillLight.position.set(-8, 3, -6);
scene.add(fillLight);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
const wireframeMat = new THREE.MeshBasicMaterial({
  vertexColors: true,
  wireframe: true,
  transparent: true,
  opacity: 0.6,
});
let currentTimepoint = 0;
let useWireframe = false;
const terrainMesh = new THREE.Mesh(terrainGeos[currentTimepoint], terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
let activeRiverGroup = riverGroups[currentTimepoint];
scene.add(activeRiverGroup);
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE * 0.7, 40, 24, 64, 0x1a1d2a, 0x1a1d2a);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
const groundGeo = new THREE.PlaneGeometry(TERRAIN_SIZE * 1.2, TERRAIN_SIZE * 1.2);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x0d0d18, roughness: 0.9, metalness: 0, side: THREE.DoubleSide });
const groundPlane = new THREE.Mesh(groundGeo, groundMat);
groundPlane.rotation.x = -Math.PI / 2;
groundPlane.position.y = -0.1;
groundPlane.receiveShadow = true;
scene.add(groundPlane);
const particleGroup = new THREE.Group();
scene.add(particleGroup);
const MAX_PARTICLES = 300;
const particlePositionsArr = new Float32Array(MAX_PARTICLES * 3);
const particleColorsArr = new Float32Array(MAX_PARTICLES * 3);
const particleSizesArr = new Float32Array(MAX_PARTICLES);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositionsArr, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColorsArr, 3));
particleGeo.setAttribute('size', new THREE.BufferAttribute(particleSizesArr, 1));
const particleSpriteTex = (() => {
  const c = document.createElement('canvas');
  c.width = 32; c.height = 32;
  const ctx = c.getContext('2d');
  const grad = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  grad.addColorStop(0, 'rgba(255,220,100,1)');
  grad.addColorStop(0.15, 'rgba(255,200,60,0.9)');
  grad.addColorStop(0.4, 'rgba(255,160,20,0.4)');
  grad.addColorStop(0.7, 'rgba(255,100,10,0.05)');
  grad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 32, 32);
  return new THREE.CanvasTexture(c);
})();
const particleMat = new THREE.PointsMaterial({
  size: 0.25,
  map: particleSpriteTex,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
});
const particlePoints = new THREE.Points(particleGeo, particleMat);
particlePoints.renderOrder = 999;
particleGroup.add(particlePoints);
const particleData = [];
for (let i = 0; i < MAX_PARTICLES; i++) {
  particleData.push({ active: false, flowIdx: -1, t: 0, speed: 0 });
  particlePositionsArr[i * 3 + 1] = -999;
}
let particleAllocPtr = 0;
function spawnParticle(flowIdx, flow) {
  const pd = particleData[particleAllocPtr];
  pd.active = true;
  pd.flowIdx = flowIdx;
  pd.t = flow.phase;
  pd.speed = flow.speed;
  const i3 = particleAllocPtr * 3;
  particlePositionsArr[i3] = flow.sx;
  particlePositionsArr[i3 + 1] = flow.sy;
  particlePositionsArr[i3 + 2] = flow.sz;
  particleColorsArr[i3] = 1;
  particleColorsArr[i3 + 1] = 0.85;
  particleColorsArr[i3 + 2] = 0.3;
  particleSizesArr[particleAllocPtr] = 1;
  particleAllocPtr = (particleAllocPtr + 1) % MAX_PARTICLES;
}
function updateParticleColors(tp) {
  const flows = allTimepoints[tp].apiFlows;
  for (let i = 0; i < MAX_PARTICLES; i++) {
    if (!particleData[i].active) continue;
    const fi = particleData[i].flowIdx;
    if (fi < 0 || fi >= flows.length) continue;
    const flow = flows[fi];
    const midY = (flow.sy + flow.ey) / 2;
    const hue = (midY / MAX_HEIGHT);
    const i3 = i * 3;
    particleColorsArr[i3] = lerp(0.9, 1.0, hue);
    particleColorsArr[i3 + 1] = lerp(0.9, 0.5, hue);
    particleColorsArr[i3 + 2] = lerp(0.1, 0.4, hue);
  }
}
function setTimepoint(t) {
  if (t === currentTimepoint) return;
  currentTimepoint = t;
  const tp = allTimepoints[t];
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = terrainGeos[t];
  scene.remove(activeRiverGroup);
  activeRiverGroup.traverse(child => { if (child.geometry) child.geometry.dispose(); });
  activeRiverGroup = riverGroups[t];
  scene.add(activeRiverGroup);
  for (let i = 0; i < MAX_PARTICLES; i++) {
    particleData[i].active = false;
    particleData[i].t = 0;
    particlePositionsArr[i * 3 + 1] = -999;
  }
  particleAllocPtr = 0;
  updateParticleColors(t);
  updateTimeLabel(t);
}
function updateTimeLabel(t) {
  document.getElementById('timeLabel').textContent = `T${t}`;
  document.getElementById('timeSlider').value = t;
}
const timeSlider = document.getElementById('timeSlider');
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value, 10);
  setTimepoint(t);
});
const bookmarks = {
  overview: { pos: [12, 8, 14], target: [0, 2.5, 0] },
  north: { pos: [0, 12, 2], target: [0, 4, 0] },
  valley: { pos: [-3, 3, 10], target: [-3, 1.5, 3] },
  flow: { pos: [5, 5, -8], target: [3, 2, -3] },
};
let bookmarkAnim = null;
document.querySelectorAll('#bookmarks button').forEach(btn => {
  btn.addEventListener('click', () => {
    const name = btn.dataset.bookmark;
    const bm = bookmarks[name];
    if (!bm) return;
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const endPos = new THREE.Vector3(...bm.pos);
    const endTarget = new THREE.Vector3(...bm.target);
    const startTime = performance.now();
    const duration = 800;
    bookmarkAnim = { startPos, startTarget, endPos, endTarget, startTime, duration };
  });
});
document.getElementById('btnAutoRotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
document.getElementById('btnWireframe').addEventListener('click', function() {
  useWireframe = !useWireframe;
  this.classList.toggle('active', useWireframe);
  terrainMesh.material = useWireframe ? wireframeMat : terrainMat;
});
document.getElementById('btnReset').addEventListener('click', () => {
  setTimepoint(0);
  controls.target.set(0, 2.5, 0);
  camera.position.set(12, 9, 14);
  controls.update();
  updateTimeLabel(0);
});
const tooltipEl = document.getElementById('tooltip');
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hoveredVertex = null;
renderer.domElement.addEventListener('mousemove', (evt) => {
  mouse.x = (evt.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(evt.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const tp = allTimepoints[currentTimepoint];
    const ix = Math.round((pt.x / TERRAIN_SIZE + 0.5) * (GRID - 1));
    const iy = Math.round((pt.z / TERRAIN_SIZE + 0.5) * (GRID - 1));
    const ci = clamp(ix, 0, GRID - 1);
    const cj = clamp(iy, 0, GRID - 1);
    const idx = cj * GRID + ci;
    const rev = (tp.revenue[idx] * 100).toFixed(1);
    const dens = (tp.userDensity[idx] * 100).toFixed(1);
    tooltipEl.style.display = 'block';
    tooltipEl.style.left = (evt.clientX + 18) + 'px';
    tooltipEl.style.top = (evt.clientY - 10) + 'px';
    tooltipEl.textContent = `Revenue: ${rev}%  |  Density: ${dens}%  |  (${ci},${cj})`;
  } else {
    tooltipEl.style.display = 'none';
  }
});
renderer.domElement.addEventListener('mouseleave', () => {
  tooltipEl.style.display = 'none';
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
let lastTime = performance.now();
let frameCount = 0;
let fpsTimer = 0;
let currentFPS = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  frameCount++;
  fpsTimer += timestamp - lastTime;
  if (fpsTimer >= 1000) {
    currentFPS = Math.round(frameCount / (fpsTimer / 1000));
    frameCount = 0;
    fpsTimer = 0;
    document.getElementById('fps').textContent = `FPS: ${currentFPS}`;
    document.getElementById('vertCount').textContent = `Verts: ${(GRID * GRID).toLocaleString()}`;
    const activeP = particleData.filter(p => p.active).length;
    document.getElementById('particleCount').textContent = `Particles: ${activeP}`;
  }
  lastTime = timestamp;
  if (bookmarkAnim) {
    const elapsed = timestamp - bookmarkAnim.startTime;
    const t = Math.min(elapsed / bookmarkAnim.duration, 1);
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(bookmarkAnim.startPos, bookmarkAnim.endPos, ease);
    controls.target.lerpVectors(bookmarkAnim.startTarget, bookmarkAnim.endTarget, ease);
    if (t >= 1) bookmarkAnim = null;
  }
  controls.update();
  const dt = Math.min((timestamp - lastTime) / 1000, 0.1);
  const flows = allTimepoints[currentTimepoint].apiFlows;
  const tp = allTimepoints[currentTimepoint];
  for (let i = 0; i < MAX_PARTICLES; i++) {
    const pd = particleData[i];
    if (!pd.active) {
      const fi = Math.floor(Math.random() * flows.length);
      const flow = flows[fi];
      spawnParticle(fi, flow);
      continue;
    }
    pd.t += pd.speed * dt;
    if (pd.t >= 1) {
      pd.active = false;
      particlePositionsArr[i * 3 + 1] = -999;
      continue;
    }
    const fi = pd.flowIdx;
    if (fi < 0 || fi >= flows.length) { pd.active = false; continue; }
    const flow = flows[fi];
    const tEased = smoothstep(0, 1, pd.t);
    const i3 = i * 3;
    const px = lerp(flow.sx, flow.ex, tEased);
    const py = lerp(flow.sy, flow.ey, tEased) + Math.sin(pd.t * Math.PI) * 0.8;
    const pz = lerp(flow.sz, flow.ez, tEased);
    particlePositionsArr[i3] = px;
    particlePositionsArr[i3 + 1] = py;
    particlePositionsArr[i3 + 2] = pz;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  particleGeo.attributes.size.needsUpdate = true;
  renderer.render(scene, camera);
}
updateTimeLabel(0);
requestAnimationFrame(animate);
</script>
</body>
</html>