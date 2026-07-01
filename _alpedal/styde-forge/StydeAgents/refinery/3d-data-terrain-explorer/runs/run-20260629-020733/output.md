<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#0a0a14;font-family:'Segoe UI',system-ui,sans-serif}
#container{width:100vw;height:100vh}
#ui{position:fixed;top:16px;left:16px;z-index:10;display:flex;flex-direction:column;gap:8px;pointer-events:none}
#ui>*{pointer-events:auto}
.panel{background:rgba(10,10,30,0.85);border:1px solid rgba(100,140,255,0.25);border-radius:10px;padding:14px 18px;color:#c8d6f0;backdrop-filter:blur(12px);min-width:220px}
.panel h3{font-size:13px;text-transform:uppercase;letter-spacing:2px;color:#6a8fff;margin-bottom:10px}
.row{display:flex;align-items:center;gap:10px;margin:6px 0;font-size:12px}
.row label{color:#8899bb;min-width:70px}
.row span{color:#c8d6f0;font-weight:600}
.slider{width:100%;height:4px;-webkit-appearance:none;appearance:none;background:rgba(100,140,255,0.2);border-radius:2px;outline:none;margin:8px 0}
.slider::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#6a8fff;cursor:pointer;border:2px solid #0a0a14}
#time-label{text-align:center;font-size:11px;color:#6a8fff;margin-top:2px}
.btn{background:rgba(100,140,255,0.15);border:1px solid rgba(100,140,255,0.35);color:#8aabff;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:11px;transition:all 0.2s;letter-spacing:1px;text-transform:uppercase}
.btn:hover{background:rgba(100,140,255,0.3);color:#fff}
.btn.active{background:rgba(100,200,140,0.25);border-color:rgba(100,200,140,0.5);color:#8fdfaf}
.bookmark-row{display:flex;gap:6px;flex-wrap:wrap}
.bookmark-row .btn{flex:1;min-width:40px;text-align:center}
.legend{position:fixed;bottom:24px;right:24px;z-index:10;pointer-events:none}
.legend-item{display:flex;align-items:center;gap:8px;margin:4px 0;font-size:11px;color:#8899bb}
.legend-swatch{width:12px;height:12px;border-radius:3px;flex-shrink:0}
#tooltip{position:fixed;pointer-events:none;background:rgba(10,10,30,0.9);border:1px solid rgba(100,140,255,0.4);border-radius:6px;padding:8px 12px;color:#c8d6f0;font-size:11px;display:none;z-index:20}
</style>
</head>
<body>
<div id="container"></div>
<div id="ui">
  <div class="panel">
    <h3>Terrain Explorer</h3>
    <div class="row"><label>Revenue</label><span id="revenue-val">$0</span></div>
    <div class="row"><label>Users</label><span id="users-val">0</span></div>
    <div class="row"><label>Errors</label><span id="errors-val">0%</span></div>
    <div class="row"><label>API Calls</label><span id="api-val">0/s</span></div>
    <input type="range" id="time-slider" class="slider" min="0" max="99" value="0">
    <div id="time-label">Day 1</div>
    <div style="display:flex;gap:6px;margin-top:8px">
      <button class="btn active" id="btn-auto-rotate">Auto</button>
      <button class="btn" id="btn-top-down">Top</button>
      <button class="btn" id="btn-wireframe">Wire</button>
    </div>
    <div style="font-size:10px;color:#556688;margin-top:6px">Bookmarks:</div>
    <div class="bookmark-row" id="bookmark-row">
      <button class="btn" data-idx="0">1</button>
      <button class="btn" data-idx="1">2</button>
      <button class="btn" data-idx="2">3</button>
      <button class="btn" data-idx="3">4</button>
    </div>
  </div>
</div>
<div class="legend">
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(135deg,#1a3a1a,#4a8a2a,#aad44a)"></div>Users (green=high)</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#e04040"></div>Error rivers</div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(135deg,#f0c030,#f06030)"></div>API particles</div>
</div>
<div id="tooltip"></div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 128;
const SIZE = 40;
const TIME_STEPS = 100;
const SCALE_Y = 8;
const container = document.getElementById('container');
const tooltip = document.getElementById('tooltip');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 30, 120);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 200);
camera.position.set(28, 22, 32);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 0, 0);
controls.maxPolarAngle = Math.PI * 0.55;
controls.minDistance = 12;
controls.maxDistance = 70;
controls.update();
const ambientLight = new THREE.AmbientLight('#223366', 1.8);
scene.add(ambientLight);
const sun = new THREE.DirectionalLight('#ffeedd', 4.5);
sun.position.set(30, 40, 20);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 150;
sun.shadow.camera.left = -40;
sun.shadow.camera.right = 40;
sun.shadow.camera.top = 40;
sun.shadow.camera.bottom = -40;
sun.shadow.bias = -0.0005;
scene.add(sun);
const rim = new THREE.DirectionalLight('#4455aa', 1.5);
rim.position.set(-20, 5, -25);
scene.add(rim);
const gridHelper = new THREE.PolarGridHelper(22, 40, 30, 128, '#1a2a44', '#1a2a44');
gridHelper.position.y = -0.05;
scene.add(gridHelper);
function createTimeSeriesData() {
  const data = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const step = { revenue: new Float32Array(GRID * GRID), users: new Float32Array(GRID * GRID), errors: new Float32Array(GRID * GRID), apiCalls: new Float32Array(GRID * GRID) };
    const phase = t / TIME_STEPS * Math.PI * 2;
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iy * GRID + ix;
        const nx = (ix / GRID - 0.5) * 2;
        const ny = (iy / GRID - 0.5) * 2;
        const d = Math.sqrt(nx * nx + ny * ny);
        const base = Math.sin(nx * 2.5 + phase) * Math.cos(ny * 1.8 + phase * 0.7) * 0.6 + Math.sin(nx * 5.1 + ny * 3.3 + phase * 0.3) * 0.25 + Math.cos(d * 4.5 - phase * 0.5) * (1 - d) * 0.3;
        step.revenue[idx] = base * 1.8 + 0.6;
        step.users[idx] = Math.max(0, (Math.sin(nx * 3.0 + phase * 0.8) * Math.cos(ny * 2.5 + phase * 0.4) + 0.8) * 0.55 + base * 0.15);
        step.errors[idx] = Math.max(0, (Math.abs(Math.sin(nx * 7 + ny * 5 + phase * 0.6)) * 0.25 + (d > 0.7 ? (1 - d) * 0.3 : 0)) * (0.4 + Math.sin(phase * 1.3) * 0.15));
        step.apiCalls[idx] = Math.max(0, (Math.sin(nx * 4.2 - phase * 0.7) * Math.cos(ny * 3.8 + phase * 0.5) * 0.4 + 0.5) * step.revenue[idx] * 0.7);
      }
    }
    data.push(step);
  }
  return data;
}
const timeSeriesData = createTimeSeriesData();
const noiseTextureSize = 64;
const noiseData = new Float32Array(noiseTextureSize * noiseTextureSize * noiseTextureSize);
for (let z = 0; z < noiseTextureSize; z++) {
  for (let y = 0; y < noiseTextureSize; y++) {
    for (let x = 0; x < noiseTextureSize; x++) {
      const idx = (z * noiseTextureSize + y) * noiseTextureSize + x;
      const nx = x / noiseTextureSize, ny = y / noiseTextureSize, nz = z / noiseTextureSize;
      let v = 0;
      for (let o = 1; o <= 4; o++) {
        const s = 1 << o;
        v += Math.sin(nx * s * 7.1 + ny * s * 11.3 + nz * s * 5.7) * Math.cos(ny * s * 9.1 + nz * s * 13.2 + nx * s * 3.9) / s;
      }
      noiseData[idx] = v * 0.5 + 0.5;
    }
  }
}
const precomputedNoiseTexture = noiseData;
function sampleNoise3D(x, y, z) {
  const tx = ((x % 1 + 1) % 1) * (noiseTextureSize - 1);
  const ty = ((y % 1 + 1) % 1) * (noiseTextureSize - 1);
  const tz = ((z % 1 + 1) % 1) * (noiseTextureSize - 1);
  const ix = Math.floor(tx), iy = Math.floor(ty), iz = Math.floor(tz);
  const fx = tx - ix, fy = ty - iy, fz = tz - iz;
  const nx = Math.min(ix + 1, noiseTextureSize - 1), ny = Math.min(iy + 1, noiseTextureSize - 1), nz = Math.min(iz + 1, noiseTextureSize - 1);
  const n = noiseTextureSize;
  const v000 = precomputedNoiseTexture[(iz * n + iy) * n + ix];
  const v100 = precomputedNoiseTexture[(iz * n + iy) * n + nx];
  const v010 = precomputedNoiseTexture[(iz * n + ny) * n + ix];
  const v110 = precomputedNoiseTexture[(iz * n + ny) * n + nx];
  const v001 = precomputedNoiseTexture[(nz * n + iy) * n + ix];
  const v101 = precomputedNoiseTexture[(nz * n + iy) * n + nx];
  const v011 = precomputedNoiseTexture[(nz * n + ny) * n + ix];
  const v111 = precomputedNoiseTexture[(nz * n + ny) * n + nx];
  const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy), sz = fz * fz * (3 - 2 * fz);
  const v00 = v000 + (v100 - v000) * sx;
  const v10 = v010 + (v110 - v010) * sx;
  const v01 = v001 + (v101 - v001) * sx;
  const v11 = v011 + (v111 - v011) * sx;
  const v0 = v00 + (v10 - v00) * sy;
  const v1 = v01 + (v11 - v01) * sy;
  return v0 + (v1 - v0) * sz;
}
const terrainGeom = new THREE.BufferGeometry();
const positions = new Float32Array(GRID * GRID * 3);
const colors = new Float32Array(GRID * GRID * 3);
const indices = [];
for (let iy = 0; iy < GRID; iy++) {
  for (let ix = 0; ix < GRID; ix++) {
    const idx = iy * GRID + ix;
    const x = (ix / (GRID - 1) - 0.5) * SIZE;
    const z = (iy / (GRID - 1) - 0.5) * SIZE;
    positions[idx * 3] = x;
    positions[idx * 3 + 2] = z;
  }
}
for (let iy = 0; iy < GRID - 1; iy++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = iy * GRID + ix, b = a + 1, c = a + GRID, d = c + 1;
    indices.push(a, b, d, a, d, c);
  }
}
terrainGeom.setIndex(indices);
terrainGeom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
terrainGeom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
terrainGeom.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.1,
  flatShading: false,
  side: THREE.DoubleSide,
  wireframe: false
});
const terrainMesh = new THREE.Mesh(terrainGeom, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
const baseGeom = new THREE.CylinderGeometry(21, 22, 1.5, 64);
const baseMat = new THREE.MeshStandardMaterial({ color: '#1a1a2e', roughness: 0.7, metalness: 0.3 });
const baseMesh = new THREE.Mesh(baseGeom, baseMat);
baseMesh.position.y = -1.6;
baseMesh.receiveShadow = true;
scene.add(baseMesh);
function elevationColor(y, users) {
  if (y < 0.2) return new THREE.Color().setHSL(0.58, 0.3, 0.12 + y * 0.4);
  if (y < 0.5) return new THREE.Color().setHSL(0.45 + users * 0.2, 0.5, 0.18 + y * 0.35);
  if (y < 0.75) return new THREE.Color().setHSL(0.35 + users * 0.15, 0.65, 0.22 + y * 0.4);
  return new THREE.Color().setHSL(0.25 + users * 0.1, 0.8, 0.28 + y * 0.45);
}
function updateTerrain(timeIndex) {
  const data = timeSeriesData[timeIndex];
  const posArr = terrainGeom.attributes.position.array;
  const colArr = terrainGeom.attributes.color.array;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const r = data.revenue[idx];
      const u = data.users[idx];
      const y = r * SCALE_Y;
      posArr[idx * 3 + 1] = y;
      const c = elevationColor(r, u);
      colArr[idx * 3] = c.r;
      colArr[idx * 3 + 1] = c.g;
      colArr[idx * 3 + 2] = c.b;
    }
  }
  terrainGeom.attributes.position.needsUpdate = true;
  terrainGeom.attributes.color.needsUpdate = true;
  terrainGeom.computeVertexNormals();
}
const RIVER_COUNT = 8;
const riverMeshes = [];
const riverBaseGeomTemplate = [];
const riverMaterial = new THREE.MeshStandardMaterial({ color: '#e04040', roughness: 0.25, metalness: 0.15, emissive: '#330000', emissiveIntensity: 0.5, transparent: true, opacity: 0.85 });
for (let r = 0; r < RIVER_COUNT; r++) {
  const points = 200;
  const riverPositions = new Float32Array(points * 3 * 2);
  const riverIndices = [];
  for (let i = 0; i < points - 1; i++) {
    const a = i * 2, b = a + 1, c = a + 2, d = a + 3;
    riverIndices.push(a, b, d, a, d, c);
  }
  const riverGeom = new THREE.BufferGeometry();
  riverGeom.setAttribute('position', new THREE.BufferAttribute(riverPositions, 3));
  riverGeom.setIndex(riverIndices);
  riverBaseGeomTemplate.push({ positions: riverPositions, indices: riverIndices, geom: riverGeom, count: points });
  const riverMesh = new THREE.Mesh(riverGeom, riverMaterial.clone());
  riverMesh.renderOrder = 1;
  riverMesh.material.depthTest = true;
  riverMesh.material.depthWrite = true;
  riverMesh.material.colorWrite = true;
  riverMesh.renderOrder = 1;
  scene.add(riverMesh);
  riverMeshes.push({ mesh: riverMesh, seedX: Math.random() * 100, seedZ: Math.random() * 100 });
}
function updateRivers(timeIndex) {
  const data = timeSeriesData[timeIndex];
  for (let r = 0; r < riverMeshes.length; r++) {
    const rm = riverMeshes[r];
    const tmpl = riverBaseGeomTemplate[r];
    const posArr = tmpl.positions;
    const n = tmpl.count;
    const ax = (rm.seedX * 0.8 - 0.4);
    const az = (rm.seedZ * 0.8 - 0.4);
    let cx = ax, cz = az;
    for (let i = 0; i < n; i++) {
      const t = i / (n - 1);
      const nx = cx + sampleNoise3D(cx * 2.1 + r * 0.7, cz * 2.1, t * 0.9) * 0.15 - 0.075;
      const nz = cz + sampleNoise3D(cz * 2.1 + r * 0.7, cx * 2.1, t * 0.9 + 0.5) * 0.15 - 0.075;
      cx = Math.max(-0.48, Math.min(0.48, nx));
      cz = Math.max(-0.48, Math.min(0.48, nz));
      const gx = Math.round((cx + 0.5) * (GRID - 1));
      const gz = Math.round((cz + 0.5) * (GRID - 1));
      const didx = Math.min(Math.max(gz, 0), GRID - 1) * GRID + Math.min(Math.max(gx, 0), GRID - 1);
      const terrainY = data.revenue[didx] * SCALE_Y;
      const width = 0.08 + data.errors[didx] * 0.4;
      const sx = cx * SIZE * 0.5;
      const sz = cz * SIZE * 0.5;
      posArr[i * 6] = sx - width;
      posArr[i * 6 + 1] = terrainY + data.errors[didx] * 2.5 + 0.15;
      posArr[i * 6 + 2] = sz;
      posArr[i * 6 + 3] = sx + width;
      posArr[i * 6 + 4] = terrainY + data.errors[didx] * 2.5 + 0.15;
      posArr[i * 6 + 5] = sz;
    }
    tmpl.geom.attributes.position.needsUpdate = true;
  }
}
const PARTICLE_COUNT = 3000;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleSizes = new Float32Array(PARTICLE_COUNT);
const particleData = [];
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleData.push({
    path: [],
    t: Math.random(),
    speed: 0.002 + Math.random() * 0.006,
    pathSeedX: Math.random() * 100,
    pathSeedZ: Math.random() * 100,
    life: 0,
    maxLife: 40 + Math.random() * 80
  });
  particlePositions[i * 3] = (Math.random() - 0.5) * SIZE * 0.9;
  particlePositions[i * 3 + 1] = 0;
  particlePositions[i * 3 + 2] = (Math.random() - 0.5) * SIZE * 0.9;
  particleColors[i * 3] = 0.9;
  particleColors[i * 3 + 1] = 0.55;
  particleColors[i * 3 + 2] = 0.2;
  particleSizes[i] = 0.15 + Math.random() * 0.5;
}
const particleGeom = new THREE.BufferGeometry();
particleGeom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeom.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
particleGeom.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
const particleTex = (() => {
  const c = document.createElement('canvas');
  c.width = 32; c.height = 32;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  g.addColorStop(0, 'rgba(255,220,140,1)');
  g.addColorStop(0.2, 'rgba(255,180,60,0.8)');
  g.addColorStop(0.5, 'rgba(255,100,20,0.3)');
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 32, 32);
  const tex = new THREE.CanvasTexture(c);
  tex.needsUpdate = true;
  return tex;
})();
const particleMat = new THREE.PointsMaterial({
  size: 0.4,
  map: particleTex,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  vertexColors: true,
  transparent: true,
  opacity: 0.7
});
const particleSystem = new THREE.Points(particleGeom, particleMat);
particleSystem.renderOrder = 2;
scene.add(particleSystem);
function getTerrainY(data, px, pz) {
  const gx = Math.round((px / (SIZE * 0.5) + 0.5) * (GRID - 1));
  const gz = Math.round((pz / (SIZE * 0.5) + 0.5) * (GRID - 1));
  const didx = Math.min(Math.max(gz, 0), GRID - 1) * GRID + Math.min(Math.max(gx, 0), GRID - 1);
  return data.revenue[didx] * SCALE_Y;
}
function updateParticles(timeIndex, dt) {
  const data = timeSeriesData[timeIndex];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    pd.t += pd.speed * dt;
    pd.life += dt;
    if (pd.life > pd.maxLife) {
      pd.t = Math.random();
      pd.life = 0;
      pd.pathSeedX = Math.random() * 100;
      pd.pathSeedZ = Math.random() * 100;
    }
    const nsx = sampleNoise3D(pd.pathSeedX * 0.6, pd.t * 3.1, pd.pathSeedZ * 0.6) * 2 - 1;
    const nsz = sampleNoise3D(pd.pathSeedZ * 0.6, pd.t * 3.1 + 0.5, pd.pathSeedX * 0.6) * 2 - 1;
    const x = nsx * SIZE * 0.48;
    const z = nsz * SIZE * 0.48;
    const terrainY = getTerrainY(data, x, z);
    const h = terrainY + 0.5 + pd.t * 1.2;
    particlePositions[i * 3] = x;
    particlePositions[i * 3 + 1] = h;
    particlePositions[i * 3 + 2] = z;
    const lifeRatio = 1 - (pd.life / pd.maxLife);
    particleColors[i * 3] = 0.9 + lifeRatio * 0.1;
    particleColors[i * 3 + 1] = 0.35 + lifeRatio * 0.35;
    particleColors[i * 3 + 2] = 0.15 + lifeRatio * 0.25;
  }
  particleGeom.attributes.position.needsUpdate = true;
  particleGeom.attributes.color.needsUpdate = true;
}
const rayCaster = new THREE.Raycaster();
rayCaster.far = 80;
const mouse = new THREE.Vector2();
renderer.domElement.addEventListener('pointermove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
});
const bookmarks = [
  { pos: [28, 22, 32], target: [0, 2, 0], label: 'Quarter View' },
  { pos: [0, 40, 2], target: [0, 0, 0], label: 'Top Down' },
  { pos: [35, 8, -35], target: [0, 0, 0], label: 'Low Angle' },
  { pos: [-30, 18, 20], target: [5, 0, -5], label: 'Reverse' }
];
let currentTimeIndex = 0;
let autoRotate = true;
let wireframe = false;
let clock = new THREE.Clock();
let savedCameras = bookmarks.map(b => ({ pos: b.pos.slice(), target: b.target.slice() }));
document.getElementById('btn-auto-rotate').addEventListener('click', function() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  this.classList.toggle('active', autoRotate);
});
document.getElementById('btn-top-down').addEventListener('click', () => {
  const bm = bookmarks[1];
  camera.position.set(...bm.pos);
  controls.target.set(...bm.target);
  controls.update();
});
document.getElementById('btn-wireframe').addEventListener('click', function() {
  wireframe = !wireframe;
  terrainMat.wireframe = wireframe;
  this.classList.toggle('active', wireframe);
});
document.getElementById('time-slider').addEventListener('input', function() {
  currentTimeIndex = parseInt(this.value);
  document.getElementById('time-label').textContent = 'Day ' + (currentTimeIndex + 1);
  updateTerrain(currentTimeIndex);
  updateRivers(currentTimeIndex);
});
document.querySelectorAll('#bookmark-row .btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.idx);
    if (e.shiftKey) {
      savedCameras[idx] = {
        pos: camera.position.toArray(),
        target: controls.target.toArray()
      };
      btn.style.borderColor = '#f0c030';
      setTimeout(() => btn.style.borderColor = '', 600);
    } else {
      const sc = savedCameras[idx];
      camera.position.set(...sc.pos);
      controls.target.set(...sc.target);
      controls.update();
    }
  });
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
window.addEventListener('keydown', (e) => {
  if (e.key >= '1' && e.key <= '4') {
    const idx = parseInt(e.key) - 1;
    const sc = savedCameras[idx];
    camera.position.set(...sc.pos);
    controls.target.set(...sc.target);
    controls.update();
  }
  if (e.key === 'r') {
    document.getElementById('btn-auto-rotate').click();
  }
  if (e.key === 'w') {
    document.getElementById('btn-wireframe').click();
  }
});
updateTerrain(0);
updateRivers(0);
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  updateParticles(currentTimeIndex, dt);
  rayCaster.setFromCamera(mouse, camera);
  const intersects = rayCaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const p = intersects[0].point;
    const data = timeSeriesData[currentTimeIndex];
    const gx = Math.round((p.x / (SIZE * 0.5) + 0.5) * (GRID - 1));
    const gz = Math.round((p.z / (SIZE * 0.5) + 0.5) * (GRID - 1));
    const didx = Math.min(Math.max(gz, 0), GRID - 1) * GRID + Math.min(Math.max(gx, 0), GRID - 1);
    tooltip.style.display = 'block';
    tooltip.style.left = (mouse.x * 0.5 + 0.5) * window.innerWidth + 15 + 'px';
    tooltip.style.top = (-mouse.y * 0.5 + 0.5) * window.innerHeight - 10 + 'px';
    tooltip.innerHTML = [
      'Revenue: $' + (data.revenue[didx] * 100).toFixed(0) + 'K',
      'Users: ' + (data.users[didx] * 1000).toFixed(0),
      'Errors: ' + (data.errors[didx] * 100).toFixed(1) + '%',
      'API: ' + (data.apiCalls[didx] * 100).toFixed(0) + '/s'
    ].join('<br>');
    document.getElementById('revenue-val').textContent = '$' + (data.revenue[didx] * 100).toFixed(0) + 'K';
    document.getElementById('users-val').textContent = (data.users[didx] * 1000).toFixed(0);
    document.getElementById('errors-val').textContent = (data.errors[didx] * 100).toFixed(1) + '%';
    document.getElementById('api-val').textContent = (data.apiCalls[didx] * 100).toFixed(0) + '/s';
  } else {
    tooltip.style.display = 'none';
  }
  renderer.render(scene, camera);
}
animate();
console.log('3D Data Terrain Explorer ready — drag to orbit, scroll to zoom, right-drag to pan, 1-4 for bookmarks, R for auto-rotate, W for wireframe, Shift+click bookmark to save camera');
</script>
</body>
</html>