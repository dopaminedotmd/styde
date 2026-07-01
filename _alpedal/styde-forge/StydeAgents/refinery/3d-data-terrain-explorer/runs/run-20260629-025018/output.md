<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8ccd4}
#canvas-container{position:fixed;inset:0;z-index:1}
#ui-layer{position:fixed;inset:0;z-index:10;pointer-events:none}
#ui-layer>*{pointer-events:auto}
#panel{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(10,10,24,0.92);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:16px 22px;display:flex;align-items:center;gap:18px;min-width:620px}
#time-slider{flex:1;height:6px;-webkit-appearance:none;appearance:none;background:linear-gradient(90deg,#1a3a5c,#2d8a6e,#c4a43e,#d44);border-radius:3px;outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;background:#e8e8f0;border-radius:50%;border:2px solid #4a90d9;cursor:pointer;box-shadow:0 0 12px rgba(74,144,217,0.5)}
#time-label{font-size:13px;font-weight:600;color:#7eb8da;min-width:70px;text-align:center}
#info{position:absolute;top:16px;left:16px;background:rgba(10,10,24,0.88);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:12px 16px;font-size:12px;line-height:1.6}
#info span{color:#7eb8da;font-weight:600}
#bookmarks{position:absolute;top:16px;right:16px;display:flex;flex-direction:column;gap:6px}
.bm-btn{background:rgba(10,10,24,0.85);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,0.1);color:#aab;padding:7px 13px;border-radius:7px;cursor:pointer;font-size:11px;transition:all 0.2s;text-align:left}
.bm-btn:hover{background:rgba(30,30,60,0.9);border-color:rgba(74,144,217,0.4);color:#dde}
#legend{position:absolute;bottom:100px;left:16px;background:rgba(10,10,24,0.85);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:10px 14px;font-size:10px}
.legend-bar{width:120px;height:10px;border-radius:3px;margin:4px 0}
#loading{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;background:#0a0a14;transition:opacity 0.5s}
#loading.hidden{opacity:0;pointer-events:none}
#loading-text{font-size:15px;color:#7eb8da}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-layer">
  <div id="info">
    timestep: <span id="info-ts">1/12</span><br>
    revenue peak: <span id="info-peak">--</span><br>
    vertices: <span id="info-verts">--</span><br>
    rivers: <span id="info-rivers">--</span>
  </div>
  <div id="bookmarks">
    <button class="bm-btn" data-bm="0">top-down</button>
    <button class="bm-btn" data-bm="1">valley flyover</button>
    <button class="bm-btn" data-bm="2">peak closeup</button>
    <button class="bm-btn" data-bm="3">orbit auto</button>
  </div>
  <div id="legend">
    elevation<br><div class="legend-bar" style="background:linear-gradient(90deg,#1a3a5c,#2d8a6e,#8ab848,#c4a43e,#d44)"></div>
    vegetation<br><div class="legend-bar" style="background:linear-gradient(90deg,#2d4a1e,#4a7a2e,#6aaa3e,#8ac848,#aad858)"></div>
  </div>
  <div id="panel">
    <span style="font-size:11px;color:#7eb8da;white-space:nowrap">TIME</span>
    <input type="range" id="time-slider" min="0" max="11" value="0" step="1">
    <span id="time-label">T1</span>
    <button id="btn-play" style="background:rgba(74,144,217,0.15);border:1px solid rgba(74,144,217,0.3);color:#7eb8da;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:11px">play</button>
    <button id="btn-reset" style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#99a;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:11px">reset view</button>
  </div>
</div>
<div id="loading"><span id="loading-text">building terrain...</span></div>
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
const PERM = new Uint8Array(512);
const SEED = 42;
for (let i = 0; i < 256; i++) {
  PERM[i] = i;
}
let s = SEED;
for (let i = 255; i > 0; i--) {
  s = (s * 16807 + 0) % 2147483647;
  const j = s % (i + 1);
  [PERM[i], PERM[j]] = [PERM[j], PERM[i]];
}
for (let i = 0; i < 256; i++) {
  PERM[i + 256] = PERM[i];
}
function hash2D(x, y) {
  return PERM[(PERM[x & 255] + y) & 255] / 255;
}
function fade(t) { return t * t * t * (t * (t * 6 - 15) + 10); }
function lerp(a, b, t) { return a + t * (b - a); }
function noise2D(x, y) {
  const xi = Math.floor(x) & 255;
  const yi = Math.floor(y) & 255;
  const xf = x - Math.floor(x);
  const yf = y - Math.floor(y);
  const u = fade(xf);
  const v = fade(yf);
  const a = PERM[xi + PERM[yi]];
  const b = PERM[xi + 1 + PERM[yi]];
  const c = PERM[xi + PERM[yi + 1]];
  const d = PERM[xi + 1 + PERM[yi + 1]];
  return lerp(lerp(a, b, u), lerp(c, d, u), v) / 255;
}
function fbm(x, y, octaves = 6, lacunarity = 2.0, gain = 0.5) {
  let value = 0, amplitude = 1, frequency = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    value += amplitude * noise2D(x * frequency, y * frequency);
    max += amplitude;
    amplitude *= gain;
    frequency *= lacunarity;
  }
  return value / max;
}
const GRID_W = 80;
const GRID_H = 60;
const TIMESTEPS = 12;
const TERRAIN_SCALE_X = 20;
const TERRAIN_SCALE_Z = 15;
const HEIGHT_SCALE = 6;
function generateData() {
  const data = [];
  for (let t = 0; t < TIMESTEPS; t++) {
    const timePhase = t / TIMESTEPS;
    const grid = [];
    for (let y = 0; y < GRID_H; y++) {
      const row = [];
      for (let x = 0; x < GRID_W; x++) {
        const nx = x / GRID_W;
        const ny = y / GRID_H;
        const revenue = fbm(nx * 4 + timePhase, ny * 4 - timePhase * 0.5, 6, 2.0, 0.5) * HEIGHT_SCALE
          + Math.sin(nx * Math.PI * 2 + timePhase * Math.PI) * 1.2
          + Math.cos(ny * Math.PI * 3 - timePhase) * 0.8
          + (1 - Math.abs(nx - 0.5) * 2) * 1.5;
        const userDensity = fbm(nx * 3.5 + 0.7, ny * 3.5 + 0.3 + timePhase * 0.3, 5, 2.0, 0.55);
        const errorRate = Math.max(0, (noise2D(nx * 5 + timePhase * 2, ny * 5) - 0.4) * 2.5);
        const apiCalls = fbm(nx * 6 + timePhase, ny * 6 + timePhase * 0.7, 4, 2.2, 0.5) * 0.8 + 0.2;
        row.push({ revenue, userDensity, errorRate, apiCalls });
      }
      grid.push(row);
    }
    data.push(grid);
  }
  return data;
}
function revenueColor(value) {
  const h = 0.6 - value * 1.1;
  const s = 0.7 + value * 0.3;
  const l = 0.15 + value * 0.55;
  const c = new THREE.Color();
  c.setHSL(Math.max(0, h), Math.min(1, s), Math.min(0.7, l));
  return c;
}
function vegetationColor(userDensity) {
  const c = new THREE.Color();
  c.setHSL(0.22 + userDensity * 0.18, 0.5 + userDensity * 0.4, 0.18 + userDensity * 0.35);
  return c;
}
function buildTerrainGeometry(grid) {
  const w = grid[0].length;
  const h = grid.length;
  const positions = new Float32Array(w * h * 3);
  const colors = new Float32Array(w * h * 3);
  const indices = [];
  let vi = 0;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const cell = grid[y][x];
      const px = (x / (w - 1) - 0.5) * TERRAIN_SCALE_X;
      const pz = (y / (h - 1) - 0.5) * TERRAIN_SCALE_Z;
      const py = cell.revenue;
      positions[vi * 3] = px;
      positions[vi * 3 + 1] = py;
      positions[vi * 3 + 2] = pz;
      const vegC = vegetationColor(cell.userDensity);
      colors[vi * 3] = vegC.r;
      colors[vi * 3 + 1] = vegC.g;
      colors[vi * 3 + 2] = vegC.b;
      vi++;
    }
  }
  for (let y = 0; y < h - 1; y++) {
    for (let x = 0; x < w - 1; x++) {
      const a = y * w + x;
      const b = a + 1;
      const c = a + w;
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
function updateTerrainAttributes(geometry, grid) {
  const w = grid[0].length;
  const h = grid.length;
  const pos = geometry.attributes.position.array;
  const col = geometry.attributes.color.array;
  let vi = 0;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const cell = grid[y][x];
      pos[vi * 3 + 1] = cell.revenue;
      const vegC = vegetationColor(cell.userDensity);
      col[vi * 3] = vegC.r;
      col[vi * 3 + 1] = vegC.g;
      col[vi * 3 + 2] = vegC.b;
      vi++;
    }
  }
  geometry.attributes.position.needsUpdate = true;
  geometry.attributes.color.needsUpdate = true;
  geometry.computeVertexNormals();
}
function traceRiver(grid, startX, startY, maxLen = 300) {
  const w = grid[0].length;
  const h = grid.length;
  const points = [];
  let cx = startX, cy = startY;
  const visited = new Set();
  for (let step = 0; step < maxLen; step++) {
    if (cx < 1 || cx >= w - 1 || cy < 1 || cy >= h - 1) break;
    const key = `${cx}|${cy}`;
    if (visited.has(key)) break;
    visited.add(key);
    const cell = grid[cy][cx];
    const px = (cx / (w - 1) - 0.5) * TERRAIN_SCALE_X;
    const pz = (cy / (h - 1) - 0.5) * TERRAIN_SCALE_Z;
    points.push(new THREE.Vector3(px, cell.revenue + 0.05, pz));
    let bestDx = 0, bestDy = 0, bestGrad = 0;
    for (let dy = -1; dy <= 1; dy++) {
      for (let dx = -1; dx <= 1; dx++) {
        if (dx === 0 && dy === 0) continue;
        const nx = cx + dx, ny = cy + dy;
        if (nx < 0 || nx >= w || ny < 0 || ny >= h) continue;
        const grad = grid[cy][cx].revenue - grid[ny][nx].revenue;
        if (grad > bestGrad) {
          bestGrad = grad;
          bestDx = dx;
          bestDy = dy;
        }
      }
    }
    if (bestGrad <= 0.001) {
      cx += (Math.random() - 0.5) > 0 ? 1 : -1;
      cy += (Math.random() - 0.5) > 0 ? 1 : -1;
    } else {
      cx += bestDx;
      cy += bestDy;
    }
  }
  return points;
}
function findRiverSources(grid, count = 8) {
  const w = grid[0].length;
  const h = grid.length;
  const candidates = [];
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (grid[y][x].errorRate > 0.55) {
        candidates.push({ x, y, e: grid[y][x].errorRate });
      }
    }
  }
  candidates.sort((a, b) => b.e - a.e);
  if (candidates.length === 0) return [];
  const sources = [];
  const step = Math.max(1, Math.floor(candidates.length / count));
  for (let i = 0; i < candidates.length && sources.length < count; i += step) {
    const c = candidates[i];
    let tooClose = false;
    for (const s of sources) {
      if (Math.abs(s.x - c.x) < 8 && Math.abs(s.y - c.y) < 6) { tooClose = true; break; }
    }
    if (!tooClose) sources.push(c);
  }
  return sources;
}
function buildRiverLines(grid) {
  const sources = findRiverSources(grid);
  const group = new THREE.Group();
  for (const src of sources) {
    const pts = traceRiver(grid, src.x, src.y);
    if (pts.length < 3) continue;
    const curve = new THREE.CatmullRomCurve3(pts);
    const curvePts = curve.getPoints(pts.length * 2);
    const geo = new THREE.BufferGeometry().setFromPoints(curvePts);
    const mat = new THREE.LineBasicMaterial({ color: new THREE.Color().setHSL(0.02, 0.9, 0.45 + src.e * 0.3), linewidth: 1, transparent: true, opacity: 0.8, depthTest: true });
    group.add(new THREE.Line(geo, mat));
  }
  return group;
}
function updateRiverLines(riverGroup, grid) {
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    child.geometry.dispose();
    child.material.dispose();
    riverGroup.remove(child);
  }
  const newGroup = buildRiverLines(grid);
  while (newGroup.children.length > 0) {
    riverGroup.add(newGroup.children[0]);
  }
}
function buildParticleSystem(grid, count = 2500) {
  const w = grid[0].length;
  const h = grid.length;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const velocities = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const x = Math.floor(Math.random() * w);
    const y = Math.floor(Math.random() * h);
    const cell = grid[y][x];
    positions[i * 3] = (x / (w - 1) - 0.5) * TERRAIN_SCALE_X + (Math.random() - 0.5) * 0.3;
    positions[i * 3 + 1] = cell.revenue + 0.15 + Math.random() * 0.6;
    positions[i * 3 + 2] = (y / (h - 1) - 0.5) * TERRAIN_SCALE_Z + (Math.random() - 0.5) * 0.3;
    colors[i * 3] = 0.5 + cell.apiCalls * 0.5;
    colors[i * 3 + 1] = 0.6 + cell.apiCalls * 0.4;
    colors[i * 3 + 2] = 1.0;
    velocities[i * 3] = (Math.random() - 0.5) * 0.3;
    velocities[i * 3 + 1] = Math.random() * 0.2;
    velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.08,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7
  });
  const points = new THREE.Points(geo, mat);
  points.userData = { velocities, grid };
  return points;
}
function updateParticlePositions(particles, grid) {
  const w = grid[0].length;
  const h = grid.length;
  const pos = particles.geometry.attributes.position.array;
  const vel = particles.userData.velocities;
  const dt = 0.016;
  for (let i = 0; i < pos.length / 3; i++) {
    const gx = ((pos[i * 3] / TERRAIN_SCALE_X) + 0.5) * (w - 1);
    const gy = ((pos[i * 3 + 2] / TERRAIN_SCALE_Z) + 0.5) * (h - 1);
    const ix = Math.max(0, Math.min(w - 1, Math.floor(gx)));
    const iy = Math.max(0, Math.min(h - 1, Math.floor(gy)));
    const cell = grid[iy][ix];
    const targetY = cell.revenue + 0.12;
    pos[i * 3] += vel[i * 3] * dt;
    pos[i * 3 + 2] += vel[i * 3 + 2] * dt;
    pos[i * 3 + 1] += (targetY - pos[i * 3 + 1]) * 3 * dt + vel[i * 3 + 1] * dt;
    if (pos[i * 3] < -TERRAIN_SCALE_X / 2 || pos[i * 3] > TERRAIN_SCALE_X / 2) {
      pos[i * 3] = (Math.random() - 0.5) * TERRAIN_SCALE_X;
      pos[i * 3 + 2] = (Math.random() - 0.5) * TERRAIN_SCALE_Z;
      vel[i * 3] = (Math.random() - 0.5) * 0.3;
    }
    if (pos[i * 3 + 2] < -TERRAIN_SCALE_Z / 2 || pos[i * 3 + 2] > TERRAIN_SCALE_Z / 2) {
      pos[i * 3] = (Math.random() - 0.5) * TERRAIN_SCALE_X;
      pos[i * 3 + 2] = (Math.random() - 0.5) * TERRAIN_SCALE_Z;
      vel[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
    }
  }
  particles.geometry.attributes.position.needsUpdate = true;
}
const BOOKMARKS = [
  { pos: [0, 20, 0], target: [0, 0, 0], label: 'top-down' },
  { pos: [8, 4, -10], target: [3, 2, 4], label: 'valley flyover' },
  { pos: [-2, 8, 2], target: [0, 5, 0], label: 'peak closeup' },
  { pos: [10, 7, 8], target: [0, 1, 0], label: 'orbit view' },
];
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 15, 50);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(8, 12, 14);
camera.lookAt(0, 2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.getElementById('canvas-container').appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.target.set(0, 2, 0);
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const gridHelper = new THREE.GridHelper(20, 40, 0x223355, 0x112233);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
const data = generateData();
document.getElementById('info-verts').textContent = `${GRID_W}x${GRID_H} = ${GRID_W * GRID_H}`;
const terrainCache = [];
for (let t = 0; t < TIMESTEPS; t++) {
  terrainCache.push(buildTerrainGeometry(data[t]));
}
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(terrainCache[0], terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
let riverGroup = buildRiverLines(data[0]);
riverGroup.name = 'rivers';
scene.add(riverGroup);
let particleSystem = buildParticleSystem(data[0], 2500);
scene.add(particleSystem);
let currentTimestep = 0;
let isPlaying = false;
let playInterval = null;
function setTimestep(t) {
  currentTimestep = t;
  terrainMesh.geometry = terrainCache[t];
  updateRiverLines(riverGroup, data[t]);
  particleSystem.userData.grid = data[t];
  document.getElementById('time-slider').value = t;
  document.getElementById('time-label').textContent = `T${t + 1}`;
  document.getElementById('info-ts').textContent = `${t + 1}/${TIMESTEPS}`;
  let peak = 0;
  for (const row of data[t]) for (const cell of row) if (cell.revenue > peak) peak = cell.revenue;
  document.getElementById('info-peak').textContent = peak.toFixed(2);
  document.getElementById('info-rivers').textContent = riverGroup.children.length;
}
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  setTimestep(parseInt(slider.value));
});
document.getElementById('btn-play').addEventListener('click', () => {
  if (isPlaying) {
    isPlaying = false;
    clearInterval(playInterval);
    document.getElementById('btn-play').textContent = 'play';
  } else {
    isPlaying = true;
    document.getElementById('btn-play').textContent = 'pause';
    playInterval = setInterval(() => {
      const next = (currentTimestep + 1) % TIMESTEPS;
      setTimestep(next);
    }, 800);
  }
});
document.getElementById('btn-reset').addEventListener('click', () => {
  controls.target.set(0, 2, 0);
  camera.position.set(8, 12, 14);
  camera.lookAt(0, 2, 0);
  controls.update();
});
document.querySelectorAll('.bm-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.bm);
    const bm = BOOKMARKS[idx];
    const target = new THREE.Vector3(...bm.target);
    const pos = new THREE.Vector3(...bm.pos);
    controls.target.copy(target);
    camera.position.copy(pos);
    controls.update();
  });
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
document.getElementById('loading').classList.add('hidden');
setTimestep(0);
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  updateParticlePositions(particleSystem, data[currentTimestep]);
  renderer.render(scene, camera);
}
animate();
if (controls.autoRotate === undefined) {
  Object.defineProperty(controls, 'autoRotate', { get: () => controls.autoRotate, set: (v) => { controls.autoRotate = v; } });
}
</script>
</body>
</html>