<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#0a0a14; overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; }
  canvas { display:block; }
  #ui { position:fixed; top:0; left:0; right:0; bottom:0; pointer-events:none; z-index:10; }
  #ui > * { pointer-events:auto; }
  #panel { position:absolute; top:16px; left:16px; background:rgba(8,8,24,0.85); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:16px 20px; color:#c8c8d8; font-size:13px; min-width:260px; }
  #panel h2 { font-size:15px; font-weight:600; color:#e0e0f0; margin:0 0 6px 0; letter-spacing:0.3px; }
  #panel .stat { display:flex; justify-content:space-between; padding:3px 0; border-bottom:1px solid rgba(255,255,255,0.04); }
  #panel .stat .label { color:#8888a8; }
  #panel .stat .value { color:#d0d0e8; font-variant-numeric:tabular-nums; }
  #timeline { position:absolute; bottom:24px; left:50%; transform:translateX(-50%); background:rgba(8,8,24,0.85); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:14px 20px; display:flex; align-items:center; gap:14px; }
  #timeline label { color:#a0a0c0; font-size:12px; white-space:nowrap; }
  #timeline input[type=range] { width:320px; accent-color:#6890e0; cursor:pointer; }
  #timeline .time-label { color:#d0d0e8; font-size:13px; font-variant-numeric:tabular-nums; min-width:90px; text-align:right; }
  #bookmarks { position:absolute; top:16px; right:16px; background:rgba(8,8,24,0.85); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:10px 14px; color:#c8c8d8; font-size:12px; min-width:160px; }
  #bookmarks h3 { font-size:13px; font-weight:600; margin:0 0 8px 0; color:#e0e0f0; }
  #bookmarks button { display:block; width:100%; margin:3px 0; padding:7px 10px; background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:6px; color:#c0c0d8; cursor:pointer; font-size:12px; text-align:left; transition:background 0.2s; }
  #bookmarks button:hover { background:rgba(104,144,224,0.2); border-color:rgba(104,144,224,0.4); }
  #bookmarks button.save { background:rgba(104,144,224,0.15); border-color:rgba(104,144,224,0.3); color:#a0c0ff; }
  #dropzone { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; pointer-events:none; opacity:0; transition:opacity 0.3s; z-index:100; }
  #dropzone.active { opacity:1; pointer-events:auto; }
  #dropzone .inner { background:rgba(8,8,24,0.92); border:2px dashed rgba(104,144,224,0.6); border-radius:16px; padding:48px 64px; color:#a0b8e0; font-size:16px; text-align:center; }
  #legend { position:absolute; bottom:24px; right:24px; background:rgba(8,8,24,0.85); backdrop-filter:blur(12px); border:1px solid rgba(255,255,255,0.1); border-radius:10px; padding:12px 14px; color:#c8c8d8; font-size:11px; }
  #legend .bar { width:120px; height:10px; border-radius:5px; margin:4px 0 8px 0; }
  #loading { position:fixed; top:50%; left:50%; transform:translate(-50%,-50%); color:#6888c0; font-size:14px; z-index:200; pointer-events:none; }
  .btn-icon { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:6px; color:#c0c0d8; cursor:pointer; padding:6px 12px; font-size:12px; transition:background 0.2s; }
  .btn-icon:hover { background:rgba(104,144,224,0.2); }
</style>
</head>
<body>
<div id="loading">building terrain...</div>
<div id="dropzone"><div class="inner">drop heightmap .json or .png here</div></div>
<div id="ui">
  <div id="panel">
    <h2>data terrain</h2>
    <div class="stat"><span class="label">time slice</span><span class="value" id="statTime">—</span></div>
    <div class="stat"><span class="label">peak elevation</span><span class="value" id="statPeak">—</span></div>
    <div class="stat"><span class="label">active particles</span><span class="value" id="statParticles">—</span></div>
    <div class="stat"><span class="label">river segments</span><span class="value" id="statRivers">—</span></div>
    <div class="stat"><span class="label">cache hits</span><span class="value" id="statCache">—</span></div>
  </div>
  <div id="bookmarks">
    <h3>camera bookmarks</h3>
    <button onclick="saveBookmark()" class="save">+ save current view</button>
    <div id="bookmarkList"></div>
    <button onclick="resetView()">reset view</button>
    <button id="btnAutoRotate" onclick="toggleAutoRotate()">auto-rotate: on</button>
  </div>
  <div id="timeline">
    <label>time</label>
    <input type="range" id="timeSlider" min="0" max="99" value="0" step="1">
    <span class="time-label" id="timeLabel">day 0</span>
  </div>
  <div id="legend">
    <div>revenue elevation</div>
    <div class="bar" style="background:linear-gradient(90deg,#1a3a2a,#3a7a3a,#a0c040,#e0d060,#e0a040)"></div>
    <div>vegetation: user density</div>
    <div class="bar" style="background:linear-gradient(90deg,#402020,#604020,#406020,#206040,#204060)"></div>
    <div>rivers: error rate</div>
    <div class="bar" style="background:linear-gradient(90deg,#800020,#c02020,#e04040)"></div>
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
const SIZE = 10;
const TIME_SLICES = 100;
const PARTICLE_COUNT = 2000;
const RIVER_THRESHOLD = 0.15;
const state = {
  timeIndex: 0,
  data: null,
  terrainMesh: null,
  riverLines: null,
  particleSystem: null,
  terrainDirty: true,
  riversDirty: true,
  particlesDirty: true,
  autoRotate: true,
  bookmarks: [],
  cacheHits: 0,
  cacheMisses: 0,
  externalHeightmap: null
};
const geometryCache = new Map();
function getCacheKey(timeIdx, external) {
  return external ? `ext_${timeIdx}` : `t${timeIdx}`;
}
function getCachedGeometry(timeIdx) {
  const key = getCacheKey(timeIdx, state.externalHeightmap !== null);
  const entry = geometryCache.get(key);
  if (!entry) {
    state.cacheMisses++;
    return null;
  }
  if (!entry.primed || !entry.geometry || !entry.geometry.attributes.position) {
    state.cacheMisses++;
    return null;
  }
  state.cacheHits++;
  return entry;
}
function setCachedGeometry(timeIdx, geometry) {
  const key = getCacheKey(timeIdx, state.externalHeightmap !== null);
  const entry = { geometry, primed: true, timestamp: performance.now() };
  geometryCache.set(key, entry);
}
function generateData() {
  const data = [];
  const seed = 42;
  function hash(x, y, t) {
    let h = seed;
    h = (h * 16807 + x * 1271 + y * 7621 + t * 31337) & 0x7fffffff;
    return (h % 10000) / 10000;
  }
  for (let t = 0; t < TIME_SLICES; t++) {
    const frame = { revenue: new Float32Array(GRID * GRID), users: new Float32Array(GRID * GRID), errors: new Float32Array(GRID * GRID) };
    const seasonPhase = (t / TIME_SLICES) * Math.PI * 4;
    const trend = 1 + (t / TIME_SLICES) * 0.6;
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iy * GRID + ix;
        const nx = ix / (GRID - 1) - 0.5;
        const ny = iy / (GRID - 1) - 0.5;
        const dist = Math.sqrt(nx * nx + ny * ny) * 2;
        const ridge = 1 - Math.abs(dist - 0.4) * 1.5;
        const hill1 = Math.exp(-((nx - 0.2) ** 2 + (ny - 0.15) ** 2) * 8);
        const hill2 = Math.exp(-((nx + 0.25) ** 2 + (ny + 0.2) ** 2) * 6);
        const hill3 = Math.exp(-((nx + 0.05) ** 2 + (ny - 0.3) ** 2) * 10);
        const noise = hash(ix, iy, t) * 0.15;
        const season = Math.sin(seasonPhase + nx * 3 + ny * 2) * 0.12;
        let rev = (ridge * 0.4 + hill1 * 0.5 + hill2 * 0.35 + hill3 * 0.3 + noise + season) * trend;
        rev = Math.max(0, Math.min(1, rev));
        frame.revenue[idx] = rev;
        const userBase = hash(ix + 1000, iy + 1000, 0) * 0.6 + rev * 0.4;
        const userGrowth = 1 + (t / TIME_SLICES) * 1.5;
        frame.users[idx] = Math.max(0, Math.min(1, userBase * userGrowth + (Math.sin(t * 0.1 + nx * 2) * 0.08)));
        const errBase = hash(ix + 2000, iy + 2000, t) * 0.1;
        const errSpike = (Math.sin(t * 0.3 + nx * 5) * 0.5 + 0.5) * (rev > 0.6 ? 0.15 : 0.05);
        frame.errors[idx] = Math.max(0, Math.min(1, errBase + errSpike));
      }
    }
    data.push(frame);
  }
  return data;
}
function getHeight(data, ix, iy) {
  if (!data) return 0;
  return data.revenue[iy * GRID + ix];
}
function getUserColor(data, ix, iy) {
  if (!data) return new THREE.Color(0x204020);
  const v = data.users[iy * GRID + ix];
  if (v < 0.3) return new THREE.Color().setHSL(0.08, 0.4, 0.15 + v * 0.5);
  if (v < 0.6) return new THREE.Color().setHSL(0.25, 0.6, 0.2 + (v - 0.3) * 0.6);
  return new THREE.Color().setHSL(0.35, 0.7, 0.3 + (v - 0.6) * 0.7);
}
function buildTerrainGeometry(data) {
  const geo = new THREE.BufferGeometry();
  const vertices = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const indices = [];
  const heightScale = SIZE * 0.4;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const x = (ix / (GRID - 1) - 0.5) * SIZE;
      const z = (iy / (GRID - 1) - 0.5) * SIZE;
      const h = getHeight(data, ix, iy) * heightScale;
      vertices[idx * 3] = x;
      vertices[idx * 3 + 1] = h;
      vertices[idx * 3 + 2] = z;
      const col = getUserColor(data, ix, iy);
      colors[idx * 3] = col.r;
      colors[idx * 3 + 1] = col.g;
      colors[idx * 3 + 2] = col.b;
    }
  }
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
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
function getOrBuildTerrainGeometry(data, timeIdx) {
  const cached = getCachedGeometry(timeIdx);
  if (cached) {
    if (state.terrainMesh) {
      state.terrainMesh.geometry.dispose();
    }
    return cached.geometry;
  }
  const geo = buildTerrainGeometry(data);
  setCachedGeometry(timeIdx, geo);
  return geo;
}
function buildRiverGeometry(data) {
  const errorGrid = data.errors;
  const segments = [];
  const heightScale = SIZE * 0.4;
  const visited = new Uint8Array(GRID * GRID);
  const directions = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]];
  for (let iy = 0; iy < GRID; iy += 2) {
    for (let ix = 0; ix < GRID; ix += 2) {
      const idx = iy * GRID + ix;
      if (visited[idx]) continue;
      if (errorGrid[idx] < RIVER_THRESHOLD) continue;
      const path = [];
      let cx = ix, cy = iy;
      let steps = 0;
      const maxSteps = GRID;
      while (steps < maxSteps) {
        const cidx = cy * GRID + cx;
        visited[cidx] = 1;
        const h = getHeight(data, cx, cy) * heightScale + 0.02;
        const px = (cx / (GRID - 1) - 0.5) * SIZE;
        const pz = (cy / (GRID - 1) - 0.5) * SIZE;
        path.push(new THREE.Vector3(px, h, pz));
        let bestDir = null;
        let bestErr = errorGrid[cidx];
        for (const [dx, dy] of directions) {
          const nx = cx + dx;
          const ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          const nidx = ny * GRID + nx;
          if (visited[nidx]) continue;
          if (errorGrid[nidx] > bestErr) {
            bestErr = errorGrid[nidx];
            bestDir = [dx, dy];
          }
        }
        if (!bestDir || bestErr < RIVER_THRESHOLD) break;
        cx += bestDir[0];
        cy += bestDir[1];
        steps++;
      }
      if (path.length >= 3) {
        segments.push(path);
      }
    }
  }
  return segments;
}
function createRiverMesh(segments) {
  const group = new THREE.Group();
  const mat = new THREE.MeshBasicMaterial({ color: 0xc03030, side: THREE.DoubleSide, transparent: true, opacity: 0.75, depthWrite: false });
  segments.forEach(path => {
    if (path.length < 2) return;
    const curve = new THREE.CatmullRomCurve3(path);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.06, 6, false);
    const mesh = new THREE.Mesh(tubeGeo, mat);
    group.add(mesh);
  });
  return group;
}
function buildParticleSystem(data) {
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const alphas = new Float32Array(PARTICLE_COUNT);
  const particleData = [];
  const heightScale = SIZE * 0.4;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const ix = Math.floor(Math.random() * GRID);
    const iy = Math.floor(Math.random() * GRID);
    const h = getHeight(data, ix, iy) * heightScale + 0.08;
    const x = (ix / (GRID - 1) - 0.5) * SIZE + (Math.random() - 0.5) * 0.3;
    const z = (iy / (GRID - 1) - 0.5) * SIZE + (Math.random() - 0.5) * 0.3;
    positions[i * 3] = x;
    positions[i * 3 + 1] = h;
    positions[i * 3 + 2] = z;
    alphas[i] = 0.3 + Math.random() * 0.7;
    particleData.push({
      ix, iy,
      offsetX: (Math.random() - 0.5) * 0.3,
      offsetZ: (Math.random() - 0.5) * 0.3,
      speed: 0.5 + Math.random() * 2,
      phase: Math.random() * Math.PI * 2,
      homeIx: ix,
      homeIy: iy
    });
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('alpha', new THREE.BufferAttribute(alphas, 1));
  const spriteTex = createGlowTexture();
  const mat = new THREE.PointsMaterial({
    size: 0.08,
    map: spriteTex,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    color: 0x80c0ff,
    opacity: 0.7
  });
  const points = new THREE.Points(geo, mat);
  points.userData = { particleData, positions, alphas };
  return points;
}
function createGlowTexture() {
  const canvas = document.createElement('canvas');
  canvas.width = 32;
  canvas.height = 32;
  const ctx = canvas.getContext('2d');
  const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
  gradient.addColorStop(0, 'rgba(255,255,255,1)');
  gradient.addColorStop(0.15, 'rgba(200,220,255,0.9)');
  gradient.addColorStop(0.4, 'rgba(100,160,255,0.5)');
  gradient.addColorStop(0.7, 'rgba(40,80,200,0.1)');
  gradient.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 32, 32);
  const tex = new THREE.CanvasTexture(canvas);
  tex.needsUpdate = true;
  return tex;
}
function updateParticles(data, dt) {
  if (!state.particleSystem) return;
  const { particleData, positions, alphas } = state.particleSystem.userData;
  const heightScale = SIZE * 0.4;
  const gridStep = SIZE / (GRID - 1);
  const halfSize = SIZE / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    pd.phase += pd.speed * dt * 0.3;
    const wander = Math.sin(pd.phase) * 0.6;
    const wanderZ = Math.cos(pd.phase * 1.3) * 0.6;
    let fx = pd.ix + wander;
    let fz = pd.iy + wanderZ;
    fx = Math.max(0, Math.min(GRID - 1, fx));
    fz = Math.max(0, Math.min(GRID - 1, fz));
    const ixFloor = Math.floor(fx);
    const iyFloor = Math.floor(fz);
    const ixCeil = Math.min(GRID - 1, ixFloor + 1);
    const iyCeil = Math.min(GRID - 1, iyFloor + 1);
    const fx_frac = fx - ixFloor;
    const fz_frac = fz - iyFloor;
    const h00 = getHeight(data, ixFloor, iyFloor);
    const h10 = getHeight(data, ixCeil, iyFloor);
    const h01 = getHeight(data, ixFloor, iyCeil);
    const h11 = getHeight(data, ixCeil, iyCeil);
    const h = (h00 * (1 - fx_frac) + h10 * fx_frac) * (1 - fz_frac) + (h01 * (1 - fx_frac) + h11 * fx_frac) * fz_frac;
    positions[i * 3] = fx * gridStep - halfSize + pd.offsetX;
    positions[i * 3 + 1] = h * heightScale + 0.08;
    positions[i * 3 + 2] = fz * gridStep - halfSize + pd.offsetZ;
    const errorAt = data.errors[iyFloor * GRID + ixFloor];
    alphas[i] = 0.25 + (1 - errorAt) * 0.6 + Math.sin(pd.phase) * 0.15;
  }
  state.particleSystem.geometry.attributes.position.needsUpdate = true;
  state.particleSystem.geometry.attributes.alpha.needsUpdate = true;
}
function applyExternalHeightmap(urlOrData) {
  if (typeof urlOrData === 'string') {
    fetch(urlOrData).then(r => r.json()).then(json => {
      applyHeightmapData(json);
    }).catch(err => {
      console.warn('Failed to load external heightmap, using generated data', err);
      state.externalHeightmap = null;
    });
  } else {
    applyHeightmapData(urlOrData);
  }
}
function applyHeightmapData(json) {
  if (!json || !Array.isArray(json.heights) && !Array.isArray(json.data)) {
    console.warn('Invalid heightmap format');
    return;
  }
  const raw = json.heights || json.data;
  state.externalHeightmap = new Float32Array(GRID * GRID);
  const rawLen = Math.min(raw.length, GRID * GRID);
  const rawGrid = Math.floor(Math.sqrt(rawLen));
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const sx = Math.floor((ix / (GRID - 1)) * (rawGrid - 1));
      const sy = Math.floor((iy / (GRID - 1)) * (rawGrid - 1));
      const val = raw[sy * rawGrid + sx] || 0;
      state.externalHeightmap[iy * GRID + ix] = typeof val === 'number' ? val : (val.revenue || val.elevation || val.height || 0);
    }
  }
  geometryCache.clear();
  state.cacheHits = 0;
  state.cacheMisses = 0;
  state.terrainDirty = true;
  state.riversDirty = true;
  state.particlesDirty = true;
}
function refreshTerrain() {
  const data = state.data ? state.data[state.timeIndex] : null;
  if (!data) return;
  const geo = getOrBuildTerrainGeometry(data, state.timeIndex);
  if (state.terrainMesh) {
    state.terrainMesh.geometry = geo;
  } else {
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.7,
      metalness: 0.1,
      flatShading: false
    });
    state.terrainMesh = new THREE.Mesh(geo, mat);
    state.terrainMesh.receiveShadow = true;
    state.terrainMesh.castShadow = true;
    scene.add(state.terrainMesh);
  }
  state.terrainDirty = false;
}
function refreshRivers() {
  const data = state.data ? state.data[state.timeIndex] : null;
  if (!data) return;
  if (state.riverLines) {
    scene.remove(state.riverLines);
    state.riverLines.traverse(c => { if (c.geometry) c.geometry.dispose(); });
    state.riverLines = null;
  }
  const segments = buildRiverGeometry(data);
  if (segments.length > 0) {
    state.riverLines = createRiverMesh(segments);
    scene.add(state.riverLines);
  }
  document.getElementById('statRivers').textContent = segments.length;
  state.riversDirty = false;
}
function refreshParticles() {
  const data = state.data ? state.data[state.timeIndex] : null;
  if (!data) return;
  if (state.particleSystem) {
    scene.remove(state.particleSystem);
    state.particleSystem.geometry.dispose();
    state.particleSystem.material.dispose();
    state.particleSystem = null;
  }
  state.particleSystem = buildParticleSystem(data);
  scene.add(state.particleSystem);
  document.getElementById('statParticles').textContent = PARTICLE_COUNT;
  state.particlesDirty = false;
}
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 8, 30);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 50);
camera.position.set(6, 5.5, 8);
camera.lookAt(0, 1.2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.2, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 3;
controls.maxDistance = 16;
controls.maxPolarAngle = Math.PI * 0.45;
controls.update();
const ambientLight = new THREE.AmbientLight(0x303060, 1.6);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 3.5);
sunLight.position.set(8, 12, 4);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 40;
sunLight.shadow.camera.left = -10;
sunLight.shadow.camera.right = 10;
sunLight.shadow.camera.top = 10;
sunLight.shadow.camera.bottom = -10;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466aa, 1.2);
fillLight.position.set(-4, 2, -3);
scene.add(fillLight);
const gridHelper = new THREE.PolarGridHelper(7, 32, 20, 128, 0x1a1a3a, 0x1a1a3a);
gridHelper.position.y = -0.01;
scene.add(gridHelper);
state.data = generateData();
function updateUI() {
  const data = state.data[state.timeIndex];
  const peak = data ? Math.max(...data.revenue) : 0;
  document.getElementById('statTime').textContent = `${state.timeIndex}`;
  document.getElementById('timeLabel').textContent = `day ${state.timeIndex}`;
  document.getElementById('statPeak').textContent = (peak * 100).toFixed(1) + '%';
  document.getElementById('statCache').textContent = `${state.cacheHits} hits / ${state.cacheMisses} misses`;
  document.getElementById('statParticles').textContent = state.particleSystem ? PARTICLE_COUNT : '—';
  document.getElementById('statRivers').textContent = state.riverLines ? 'active' : '—';
}
function fullRefresh() {
  const data = state.data[state.timeIndex];
  if (!data) return;
  refreshTerrain();
  refreshRivers();
  refreshParticles();
  updateUI();
}
document.getElementById('timeSlider').addEventListener('input', (e) => {
  state.timeIndex = parseInt(e.target.value);
  state.terrainDirty = true;
  state.riversDirty = true;
  state.particlesDirty = true;
  fullRefresh();
});
window.saveBookmark = function() {
  const bm = {
    position: camera.position.toArray(),
    target: controls.target.toArray(),
    zoom: camera.zoom,
    timeIndex: state.timeIndex
  };
  state.bookmarks.push(bm);
  renderBookmarks();
};
window.loadBookmark = function(index) {
  const bm = state.bookmarks[index];
  if (!bm) return;
  camera.position.set(...bm.position);
  controls.target.set(...bm.target);
  camera.zoom = bm.zoom;
  camera.updateProjectionMatrix();
  controls.update();
  if (bm.timeIndex !== undefined) {
    state.timeIndex = bm.timeIndex;
    document.getElementById('timeSlider').value = bm.timeIndex;
    state.terrainDirty = true;
    state.riversDirty = true;
    state.particlesDirty = true;
    fullRefresh();
  }
};
window.deleteBookmark = function(index) {
  state.bookmarks.splice(index, 1);
  renderBookmarks();
};
function renderBookmarks() {
  const list = document.getElementById('bookmarkList');
  list.innerHTML = state.bookmarks.map((bm, i) => {
    const pos = bm.position.map(v => v.toFixed(1)).join(', ');
    return `<button onclick="loadBookmark(${i})" title="pos: ${pos}">view ${i + 1} <span style="float:right;opacity:0.4;cursor:pointer" onclick="event.stopPropagation();deleteBookmark(${i})">x</span></button>`;
  }).join('');
}
window.resetView = function() {
  camera.position.set(6, 5.5, 8);
  controls.target.set(0, 1.2, 0);
  camera.zoom = 1;
  camera.updateProjectionMatrix();
  controls.update();
};
window.toggleAutoRotate = function() {
  state.autoRotate = !state.autoRotate;
  controls.autoRotate = state.autoRotate;
  document.getElementById('btnAutoRotate').textContent = `auto-rotate: ${state.autoRotate ? 'on' : 'off'}`;
};
const dropzone = document.getElementById('dropzone');
document.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('active'); });
document.addEventListener('dragleave', (e) => {
  if (e.target === document.documentElement || e.target === document.body) {
    dropzone.classList.remove('active');
  }
});
dropzone.addEventListener('dragover', (e) => { e.preventDefault(); });
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('active');
  const file = e.dataTransfer.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    try {
      const json = JSON.parse(ev.target.result);
      applyHeightmapData(json);
      fullRefresh();
    } catch (err) {
      console.warn('Failed to parse dropped file as JSON', err);
    }
  };
  reader.readAsText(file);
});
document.addEventListener('paste', (e) => {
  const text = e.clipboardData.getData('text');
  if (!text || !text.trim().startsWith('{')) return;
  try {
    const json = JSON.parse(text);
    if (json.heights || json.data) {
      applyHeightmapData(json);
      fullRefresh();
    }
  } catch (_) {}
});
function lazyPreloadCache() {
  let pending = 0;
  const maxConcurrent = 4;
  let nextIdx = 0;
  function processNext() {
    if (nextIdx >= TIME_SLICES) return;
    const idx = nextIdx++;
    pending++;
    const key = getCacheKey(idx, false);
    if (geometryCache.has(key)) {
      pending--;
      processNext();
      return;
    }
    const entry = { geometry: null, primed: false, timestamp: 0 };
    geometryCache.set(key, entry);
    setTimeout(() => {
      const data = state.data[idx];
      const geo = buildTerrainGeometry(data);
      entry.geometry = geo;
      entry.primed = true;
      entry.timestamp = performance.now();
      pending--;
      processNext();
    }, 0);
  }
  for (let i = 0; i < maxConcurrent; i++) processNext();
}
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  if (state.particleSystem) {
    updateParticles(state.data[state.timeIndex], dt);
  }
  renderer.render(scene, camera);
}
fullRefresh();
lazyPreloadCache();
document.getElementById('loading').style.display = 'none';
animate();
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
</script>
</body>
</html>