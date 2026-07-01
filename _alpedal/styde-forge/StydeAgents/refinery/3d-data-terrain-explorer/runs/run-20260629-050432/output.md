<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; }
  canvas { display: block; }
  #loading {
    position: fixed; inset: 0; background: #0a0a14; display: flex;
    flex-direction: column; align-items: center; justify-content: center;
    z-index: 100; color: #88aacc; font-size: 14px; transition: opacity 0.5s;
  }
  #loading.hidden { opacity: 0; pointer-events: none; }
  #loading .spinner {
    width: 40px; height: 40px; border: 3px solid #223344;
    border-top-color: #4488cc; border-radius: 50%; animation: spin 0.8s linear infinite;
    margin-bottom: 12px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  #ui {
    position: fixed; bottom: 0; left: 0; right: 0; z-index: 10;
    background: linear-gradient(transparent, rgba(10,10,20,0.92) 30%);
    padding: 20px 24px 18px; display: flex; flex-direction: column; gap: 8px;
  }
  #time-row {
    display: flex; align-items: center; gap: 12px;
  }
  #time-label {
    color: #aaccee; font-size: 12px; min-width: 90px; text-align: right;
    font-variant-numeric: tabular-nums;
  }
  #time-slider {
    flex: 1; -webkit-appearance: none; height: 6px;
    background: linear-gradient(to right, #224466, #4488cc);
    border-radius: 3px; outline: none; cursor: pointer;
  }
  #time-slider::-webkit-slider-thumb {
    -webkit-appearance: none; width: 18px; height: 18px;
    border-radius: 50%; background: #fff; border: 2px solid #4488cc;
    cursor: pointer; box-shadow: 0 0 10px rgba(68,136,204,0.5);
  }
  #btn-row {
    display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
  }
  #btn-row button {
    background: rgba(30,50,70,0.8); border: 1px solid rgba(100,150,200,0.3);
    color: #aaccee; padding: 5px 12px; border-radius: 4px; cursor: pointer;
    font-size: 11px; transition: all 0.2s;
  }
  #btn-row button:hover { background: rgba(50,80,110,0.9); border-color: rgba(100,150,200,0.6); }
  #btn-row button.active { background: #336699; border-color: #5599cc; color: #fff; }
  #bookmark-select {
    background: rgba(30,50,70,0.8); border: 1px solid rgba(100,150,200,0.3);
    color: #aaccee; padding: 5px 8px; border-radius: 4px; font-size: 11px;
    cursor: pointer; outline: none;
  }
  #bookmark-select option { background: #1a2a3a; color: #aaccee; }
  #legend {
    position: fixed; top: 16px; right: 16px; z-index: 10;
    background: rgba(10,10,20,0.85); border: 1px solid rgba(100,150,200,0.2);
    border-radius: 6px; padding: 12px 14px; font-size: 10px; color: #8899aa;
    display: flex; flex-direction: column; gap: 6px;
  }
  #legend .row { display: flex; align-items: center; gap: 8px; }
  #legend .swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
  #legend .swatch.high { background: #22aa44; }
  #legend .swatch.mid { background: #aa8822; }
  #legend .swatch.low { background: #884422; }
  #legend .swatch.river { background: #cc3333; }
  #legend .swatch.particle { background: #ffcc44; }
</style>
</head>
<body>
<div id="loading">
  <div class="spinner"></div>
  <span id="loading-text">Building terrain caches...</span>
</div>
<div id="legend">
  <div class="row"><span class="swatch high"></span> High user density</div>
  <div class="row"><span class="swatch mid"></span> Medium density</div>
  <div class="row"><span class="swatch low"></span> Low density</div>
  <div class="row"><span class="swatch river"></span> Error/anomaly rivers</div>
  <div class="row"><span class="swatch particle"></span> API call trails</div>
</div>
<div id="ui">
  <div id="time-row">
    <span id="time-label">T 0 / 0</span>
    <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
  </div>
  <div id="btn-row">
    <button id="btn-autorot">Auto-Rotate: Off</button>
    <button id="btn-save-bm">Save View</button>
    <select id="bookmark-select"><option value="">— Bookmarks —</option></select>
    <button id="btn-recall-bm">Recall</button>
    <button id="btn-reset-cam">Reset Camera</button>
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
const CONFIG = {
  gridSize: 80,
  terrainWidth: 40,
  maxHeight: 10,
  numTimePoints: 30,
  particleCount: 600,
  particleSpeed: 0.35,
  riverCount: 3,
  ribbonHalfWidth: 0.12,
  riverTubeRadius: 0.09,
};
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const lerp = (a, b, t) => a + (b - a) * t;
const smoothstep = (edge0, edge1, x) => {
  const t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
  return t * t * (3 - 2 * t);
};
function sampleHeight(heights, gx, gz, gs, tw) {
  const ix = clamp(Math.round((gx / tw + 0.5) * (gs - 1)), 0, gs - 1);
  const iz = clamp(Math.round((gz / tw + 0.5) * (gs - 1)), 0, gs - 1);
  return heights[iz * gs + ix];
}
function worldToGrid(wx, wz, gs, tw) {
  const ix = clamp(Math.round((wx / tw + 0.5) * (gs - 1)), 0, gs - 1);
  const iz = clamp(Math.round((wz / tw + 0.5) * (gs - 1)), 0, gs - 1);
  return { ix, iz };
}
const timeSeriesData = [];
{
  const { gridSize: gs, numTimePoints: ntp } = CONFIG;
  for (let t = 0; t < ntp; t++) {
    const revenue = new Float32Array(gs * gs);
    const density = new Float32Array(gs * gs);
    const errorField = new Float32Array(gs * gs);
    const apiSources = [];
    const apiSinks = [];
    for (let iz = 0; iz < gs; iz++) {
      for (let ix = 0; ix < gs; ix++) {
        const idx = iz * gs + ix;
        const fx = ix / (gs - 1) - 0.5;
        const fz = iz / (gs - 1) - 0.5;
        const tp = t / ntp;
        let rev = 0;
        rev += Math.sin(fx * 5.5 + tp * 1.8) * Math.cos(fz * 4.2 + tp * 1.3) * 3.5;
        rev += Math.sin(fx * 7.8 - tp * 0.9) * Math.cos(fz * 6.1 + tp * 1.1) * 2.2;
        rev += Math.cos(fx * 2.3 + fz * 3.1) * Math.sin(tp * 2.4) * 1.8;
        rev += Math.sin(fx * 11.0 + fz * 9.0 + tp * 3.0) * 0.9;
        rev += tp * 4.0 * (1 + Math.sin(fx * 1.2) * 0.4);
        revenue[idx] = rev;
        let dens = 0;
        dens += Math.sin(fx * 4.5 + fz * 3.8 + tp * 0.7) * 0.5 + 0.5;
        dens += Math.cos(fx * 5.2 - fz * 4.1 + tp * 0.5) * 0.35;
        dens += Math.sin(fx * 8.0 + fz * 7.0 + tp * 1.5) * 0.15;
        dens = clamp(dens, 0, 1);
        density[idx] = dens;
        let err = 0;
        err += Math.abs(Math.sin(fx * 9.0 + fz * 7.0 + tp * 2.0)) * 1.5;
        err += Math.abs(Math.cos(fx * 6.0 - fz * 5.0 + tp * 1.6)) * 1.2;
        err += Math.abs(Math.sin(fx * 13.0 + fz * 11.0 + tp * 0.9)) * 0.8;
        err *= (0.6 + 0.4 * Math.abs(Math.sin(tp * 3.0 + fx * 2.0)));
        errorField[idx] = err;
      }
    }
    const numSources = 3 + (t % 4);
    const numSinks = 2 + (t % 3);
    for (let i = 0; i < numSources; i++) {
      apiSources.push({
        gx: Math.floor(Math.random() * gs),
        gz: Math.floor(Math.random() * gs),
        strength: 0.5 + Math.random() * 0.5,
      });
    }
    for (let i = 0; i < numSinks; i++) {
      apiSinks.push({
        gx: Math.floor(Math.random() * gs),
        gz: Math.floor(Math.random() * gs),
      });
    }
    timeSeriesData.push({ revenue, density, errorField, apiSources, apiSinks });
  }
}
const terrainCache = new Map();
const riverCache = new Map();
const particleCache = new Map();
function buildTerrainCacheEntry(t) {
  if (terrainCache.has(t)) return;
  const { gridSize: gs, terrainWidth: tw, maxHeight: mh } = CONFIG;
  const data = timeSeriesData[t];
  const positions = new Float32Array(gs * gs * 3);
  const colors = new Float32Array(gs * gs * 3);
  const heights1D = new Float32Array(gs * gs);
  const rev = data.revenue;
  const dens = data.density;
  let revMin = Infinity, revMax = -Infinity;
  for (let i = 0; i < rev.length; i++) {
    if (rev[i] < revMin) revMin = rev[i];
    if (rev[i] > revMax) revMax = rev[i];
  }
  const revRange = revMax - revMin || 1;
  for (let iz = 0; iz < gs; iz++) {
    for (let ix = 0; ix < gs; ix++) {
      const idx = iz * gs + ix;
      const wx = (ix / (gs - 1) - 0.5) * tw;
      const wz = (iz / (gs - 1) - 0.5) * tw;
      const h = ((rev[idx] - revMin) / revRange) * mh;
      positions[idx * 3] = wx;
      positions[idx * 3 + 1] = h;
      positions[idx * 3 + 2] = wz;
      heights1D[idx] = h;
      const d = clamp(dens[idx], 0, 1);
      let cr, cg, cb;
      if (d < 0.33) {
        const t2 = d / 0.33;
        cr = lerp(0.4, 0.55, t2);
        cg = lerp(0.2, 0.45, t2);
        cb = lerp(0.1, 0.15, t2);
      } else if (d < 0.66) {
        const t2 = (d - 0.33) / 0.33;
        cr = lerp(0.55, 0.3, t2);
        cg = lerp(0.45, 0.65, t2);
        cb = lerp(0.15, 0.12, t2);
      } else {
        const t2 = (d - 0.66) / 0.34;
        cr = lerp(0.3, 0.1, t2);
        cg = lerp(0.65, 0.75, t2);
        cb = lerp(0.12, 0.15, t2);
      }
      colors[idx * 3] = cr;
      colors[idx * 3 + 1] = cg;
      colors[idx * 3 + 2] = cb;
    }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const indices = [];
  for (let iz = 0; iz < gs - 1; iz++) {
    for (let ix = 0; ix < gs - 1; ix++) {
      const a = iz * gs + ix;
      const b = a + 1;
      const c = a + gs;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geometry.setIndex(indices);
  geometry.computeVertexNormals();
  const entry = {
    geometry,
    heights: heights1D,
    ready: true,
    primed: true,
  };
  terrainCache.set(t, entry);
}
function buildRiverCacheEntry(t) {
  if (riverCache.has(t)) return;
  const { gridSize: gs, terrainWidth: tw } = CONFIG;
  const data = timeSeriesData[t];
  const err = data.errorField;
  const riverPaths = [];
  const numRivers = CONFIG.riverCount;
  for (let r = 0; r < numRivers; r++) {
    let cx = Math.floor(gs * (0.15 + Math.random() * 0.7));
    let cz = Math.floor(gs * (0.15 + Math.random() * 0.7));
    const points = [];
    const visited = new Set();
    const maxSteps = 120;
    for (let step = 0; step < maxSteps; step++) {
      const key = `${cx},${cz}`;
      if (visited.has(key)) break;
      visited.add(key);
      const wx = (cx / (gs - 1) - 0.5) * tw;
      const wz = (cz / (gs - 1) - 0.5) * tw;
      const h = sampleHeight(terrainCache.get(t).heights, wx, wz, gs, tw);
      points.push({ x: wx, y: h, z: wz });
      let bestErr = -1;
      let bestNx = cx, bestNz = cz;
      for (let dz = -1; dz <= 1; dz++) {
        for (let dx = -1; dx <= 1; dx++) {
          if (dx === 0 && dz === 0) continue;
          const nx = cx + dx;
          const nz = cz + dz;
          if (nx < 0 || nx >= gs || nz < 0 || nz >= gs) continue;
          const nk = `${nx},${nz}`;
          if (visited.has(nk)) continue;
          const e = err[nz * gs + nx];
          if (e > bestErr) {
            bestErr = e;
            bestNx = nx;
            bestNz = nz;
          }
        }
      }
      if (bestErr < 0.01) break;
      cx = bestNx;
      cz = bestNz;
    }
    if (points.length >= 3) {
      riverPaths.push(points);
    }
  }
  const geometries = riverPaths.map(pts => {
    const curve = new THREE.CatmullRomCurve3(
      pts.map(p => new THREE.Vector3(p.x, p.y + 0.15, p.z))
    );
    return new THREE.TubeGeometry(curve, 80, CONFIG.riverTubeRadius, 6, false);
  });
  const entry = {
    geometries,
    paths: riverPaths,
    ready: true,
    primed: true,
  };
  riverCache.set(t, entry);
}
function buildParticleCacheEntry(t) {
  if (particleCache.has(t)) return;
  const { gridSize: gs, terrainWidth: tw, particleCount: pc } = CONFIG;
  const data = timeSeriesData[t];
  const heights = new Float32Array(gs * gs);
  const entry = terrainCache.get(t);
  if (!entry || !entry.primed) {
    buildTerrainCacheEntry(t);
  }
  const tentry = terrainCache.get(t);
  heights.set(tentry.heights);
  const paths = [];
  const { apiSources, apiSinks } = data;
  const numPaths = Math.max(20, Math.floor(pc / 10));
  for (let i = 0; i < numPaths; i++) {
    const src = apiSources[Math.floor(Math.random() * apiSources.length)];
    const snk = apiSinks[Math.floor(Math.random() * apiSinks.length)];
    const waypoints = [];
    const sx = (src.gx / (gs - 1) - 0.5) * tw;
    const sz = (src.gz / (gs - 1) - 0.5) * tw;
    const ex = (snk.gx / (gs - 1) - 0.5) * tw;
    const ez = (snk.gz / (gs - 1) - 0.5) * tw;
    const segments = 4 + Math.floor(Math.random() * 4);
    for (let s = 0; s <= segments; s++) {
      const t2 = s / segments;
      const sx2 = lerp(sx, ex, t2);
      const sz2 = lerp(sz, ez, t2);
      const jitterX = (s > 0 && s < segments) ? (Math.random() - 0.5) * tw * 0.12 : 0;
      const jitterZ = (s > 0 && s < segments) ? (Math.random() - 0.5) * tw * 0.12 : 0;
      waypoints.push({ x: sx2 + jitterX, z: sz2 + jitterZ });
    }
    paths.push({ waypoints, speed: CONFIG.particleSpeed * (0.6 + Math.random() * 0.8) });
  }
  const progress = new Float32Array(pc);
  const pathIdx = new Uint16Array(pc);
  for (let i = 0; i < pc; i++) {
    progress[i] = Math.random();
    pathIdx[i] = Math.floor(Math.random() * numPaths);
  }
  const pentry = {
    heights,
    paths,
    states: { progress, pathIdx },
    ready: true,
    primed: true,
  };
  particleCache.set(t, pentry);
}
function buildAllCaches() {
  const total = CONFIG.numTimePoints;
  const loader = document.getElementById('loading-text');
  for (let t = 0; t < total; t++) {
    buildTerrainCacheEntry(t);
    if (t % 5 === 0 && loader) {
      loader.textContent = `Building terrain caches... ${t + 1}/${total}`;
    }
  }
  for (let t = 0; t < total; t++) {
    buildRiverCacheEntry(t);
    if (t % 5 === 0 && loader) {
      loader.textContent = `Building river caches... ${t + 1}/${total}`;
    }
  }
  for (let t = 0; t < total; t++) {
    buildParticleCacheEntry(t);
    if (t % 5 === 0 && loader) {
      loader.textContent = `Building particle caches... ${t + 1}/${total}`;
    }
  }
  if (loader) loader.textContent = 'Ready.';
}
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0d1117');
scene.fog = new THREE.Fog('#0d1117', 20, 80);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(16, 14, 22);
camera.lookAt(0, 2, 0);
const ambientLight = new THREE.AmbientLight('#334466', 1.4);
scene.add(ambientLight);
const hemiLight = new THREE.HemisphereLight('#8899cc', '#223344', 0.8);
scene.add(hemiLight);
const sunLight = new THREE.DirectionalLight('#ffeedd', 2.5);
sunLight.position.set(20, 30, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -30;
sunLight.shadow.camera.right = 30;
sunLight.shadow.camera.top = 30;
sunLight.shadow.camera.bottom = -30;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 2.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.6;
controls.minDistance = 6;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.75,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(terrainCache.get(0).geometry, terrainMaterial);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
const riverMaterial = new THREE.MeshStandardMaterial({
  color: '#cc3333',
  roughness: 0.35,
  metalness: 0.15,
  emissive: '#331111',
  emissiveIntensity: 0.4,
});
const riverGroup = new THREE.Group();
scene.add(riverGroup);
function swapRivers(t) {
  while (riverGroup.children.length > 0) {
    const child = riverGroup.children[0];
    if (child.geometry) child.geometry.dispose();
    riverGroup.remove(child);
  }
  const rentry = riverCache.get(t);
  if (!rentry || !rentry.primed) return;
  for (const geom of rentry.geometries) {
    const mesh = new THREE.Mesh(geom, riverMaterial);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    riverGroup.add(mesh);
  }
}
swapRivers(0);
const glowCanvas = document.createElement('canvas');
glowCanvas.width = 32;
glowCanvas.height = 32;
const gctx = glowCanvas.getContext('2d');
const gradient = gctx.createRadialGradient(16, 16, 0, 16, 16, 16);
gradient.addColorStop(0, 'rgba(255, 220, 140, 1)');
gradient.addColorStop(0.2, 'rgba(255, 180, 80, 0.9)');
gradient.addColorStop(0.5, 'rgba(255, 120, 40, 0.4)');
gradient.addColorStop(0.8, 'rgba(255, 60, 20, 0.05)');
gradient.addColorStop(1, 'rgba(255, 30, 10, 0)');
gctx.fillStyle = gradient;
gctx.fillRect(0, 0, 32, 32);
const glowTexture = new THREE.CanvasTexture(glowCanvas);
glowTexture.needsUpdate = true;
const particlePositions = new Float32Array(CONFIG.particleCount * 3);
const particleGeometry = new THREE.BufferGeometry();
particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
const particleMaterial = new THREE.PointsMaterial({
  size: 0.2,
  map: glowTexture,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  color: '#ffaa44',
  transparent: true,
  opacity: 0.85,
});
const particleSystem = new THREE.Points(particleGeometry, particleMaterial);
scene.add(particleSystem);
let currentTimeIndex = 0;
function interpolateWaypoints(waypoints, t) {
  if (waypoints.length === 0) return { x: 0, z: 0 };
  if (waypoints.length === 1) return { x: waypoints[0].x, z: waypoints[0].z };
  const clampedT = clamp(t, 0, 1);
  const segFloat = clampedT * (waypoints.length - 1);
  const segIdx = Math.min(Math.floor(segFloat), waypoints.length - 2);
  const localT = segFloat - segIdx;
  const a = waypoints[segIdx];
  const b = waypoints[Math.min(segIdx + 1, waypoints.length - 1)];
  return {
    x: lerp(a.x, b.x, localT),
    z: lerp(a.z, b.z, localT),
  };
}
function updateParticles(dt) {
  const entry = particleCache.get(currentTimeIndex);
  if (!entry || !entry.primed) return;
  const { heights, paths, states } = entry;
  const { progress, pathIdx } = states;
  const pos = particlePositions;
  const gs = CONFIG.gridSize;
  const tw = CONFIG.terrainWidth;
  const pc = CONFIG.particleCount;
  for (let i = 0; i < pc; i++) {
    const pi = pathIdx[i];
    if (pi >= paths.length) {
      progress[i] = 0;
      pathIdx[i] = 0;
      continue;
    }
    const p = paths[pi];
    progress[i] += p.speed * dt;
    if (progress[i] >= 1.0) {
      progress[i] = 0;
      pathIdx[i] = (pi + 1) % paths.length;
    }
    const wp = interpolateWaypoints(p.waypoints, progress[i]);
    const h = sampleHeight(heights, wp.x, wp.z, gs, tw);
    const j = i * 3;
    pos[j] = wp.x;
    pos[j + 1] = h + 0.2;
    pos[j + 2] = wp.z;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
function swapTerrain(t) {
  const entry = terrainCache.get(t);
  if (!entry || !entry.primed) return;
  terrainMesh.geometry = entry.geometry;
}
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const maxT = CONFIG.numTimePoints - 1;
timeSlider.max = maxT;
timeSlider.value = 0;
timeLabel.textContent = `T 0 / ${maxT}`;
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value, 10);
  if (t !== currentTimeIndex) {
    currentTimeIndex = t;
    swapTerrain(t);
    swapRivers(t);
  }
  timeLabel.textContent = `T ${t} / ${maxT}`;
});
const bookmarks = [];
function saveBookmark() {
  const name = `View ${bookmarks.length + 1}`;
  const bm = {
    name,
    position: camera.position.clone(),
    target: controls.target.clone(),
    zoom: camera.zoom,
  };
  bookmarks.push(bm);
  refreshBookmarkSelect();
}
function recallBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  camera.position.copy(bm.position);
  controls.target.copy(bm.target);
  camera.zoom = bm.zoom;
  camera.updateProjectionMatrix();
  controls.update();
}
function refreshBookmarkSelect() {
  const sel = document.getElementById('bookmark-select');
  sel.innerHTML = '<option value="">— Bookmarks —</option>';
  for (let i = 0; i < bookmarks.length; i++) {
    const opt = document.createElement('option');
    opt.value = i;
    opt.textContent = bookmarks[i].name;
    sel.appendChild(opt);
  }
}
document.getElementById('btn-save-bm').addEventListener('click', saveBookmark);
document.getElementById('btn-recall-bm').addEventListener('click', () => {
  const sel = document.getElementById('bookmark-select');
  const idx = parseInt(sel.value, 10);
  if (!isNaN(idx)) recallBookmark(idx);
});
document.getElementById('btn-reset-cam').addEventListener('click', () => {
  camera.position.set(16, 14, 22);
  controls.target.set(0, 2.5, 0);
  camera.zoom = 1;
  camera.updateProjectionMatrix();
  controls.update();
});
const btnAutorot = document.getElementById('btn-autorot');
btnAutorot.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAutorot.textContent = `Auto-Rotate: ${controls.autoRotate ? 'On' : 'Off'}`;
  btnAutorot.classList.toggle('active', controls.autoRotate);
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
document.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      btnAutorot.textContent = `Auto-Rotate: ${controls.autoRotate ? 'On' : 'Off'}`;
      btnAutorot.classList.toggle('active', controls.autoRotate);
      break;
    case 'b':
      saveBookmark();
      break;
    case 'arrowleft':
      if (currentTimeIndex > 0) {
        currentTimeIndex--;
        timeSlider.value = currentTimeIndex;
        swapTerrain(currentTimeIndex);
        swapRivers(currentTimeIndex);
        timeLabel.textContent = `T ${currentTimeIndex} / ${maxT}`;
      }
      break;
    case 'arrowright':
      if (currentTimeIndex < maxT) {
        currentTimeIndex++;
        timeSlider.value = currentTimeIndex;
        swapTerrain(currentTimeIndex);
        swapRivers(currentTimeIndex);
        timeLabel.textContent = `T ${currentTimeIndex} / ${maxT}`;
      }
      break;
  }
});
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  updateParticles(dt);
  controls.update();
  renderer.render(scene, camera);
}
buildAllCaches();
document.getElementById('loading').classList.add('hidden');
animate();
</script>
</body>
</html>