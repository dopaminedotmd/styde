`E:\Stryde\_alpedal\styde-forge\output\3d-data-terrain-explorer.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; overflow: hidden; height: 100vh; color: #c8c8d8; }
#container { width: 100vw; height: 100vh; position: relative; }
canvas { display: block; }
#ui-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; }
#ui-overlay > * { pointer-events: auto; }
#state-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 100; transition: opacity .4s; }
#state-overlay.success { opacity: 0; pointer-events: none; }
#state-overlay .state-card { background: rgba(10,10,25,.92); border: 1px solid rgba(120,140,200,.25); border-radius: 12px; padding: 32px 40px; text-align: center; max-width: 420px; backdrop-filter: blur(8px); }
#state-overlay .state-icon { font-size: 40px; margin-bottom: 12px; }
#state-overlay .state-title { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
#state-overlay .state-desc { font-size: 13px; color: #889; line-height: 1.5; }
#state-overlay .spinner { width: 36px; height: 36px; border: 3px solid rgba(120,180,240,.2); border-top-color: #78b4f0; border-radius: 50%; animation: spin .8s linear infinite; margin: 0 auto 16px; }
@keyframes spin { to { transform: rotate(360deg); } }
.state-icon.error { color: #e06060; }
.state-icon.empty { color: #909090; }
#top-bar { position: absolute; top: 16px; left: 16px; right: 16px; display: flex; align-items: center; gap: 12px; z-index: 10; flex-wrap: wrap; }
#top-bar .panel { background: rgba(10,10,28,.85); border: 1px solid rgba(120,140,200,.2); border-radius: 8px; padding: 10px 16px; backdrop-filter: blur(6px); font-size: 12px; }
.metric-pill { display: flex; align-items: center; gap: 8px; }
.metric-pill .dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.metric-pill .label { color: #889; text-transform: uppercase; letter-spacing: .8px; font-size: 10px; }
.metric-pill .value { font-weight: 700; font-variant-numeric: tabular-nums; font-size: 14px; }
#time-bar { position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); z-index: 10; background: rgba(10,10,28,.88); border: 1px solid rgba(120,140,200,.2); border-radius: 10px; padding: 12px 20px; display: flex; align-items: center; gap: 14px; backdrop-filter: blur(6px); }
#time-slider { width: 280px; accent-color: #78b4f0; cursor: pointer; }
#time-label { font-variant-numeric: tabular-nums; font-size: 13px; font-weight: 600; min-width: 48px; text-align: center; color: #d0d8f0; }
#time-bar button { background: rgba(120,180,240,.12); border: 1px solid rgba(120,180,240,.3); color: #a0b8e0; border-radius: 5px; padding: 4px 10px; cursor: pointer; font-size: 12px; transition: all .2s; }
#time-bar button:hover { background: rgba(120,180,240,.25); }
#time-bar button:active { background: rgba(120,180,240,.4); }
#bookmark-bar { position: absolute; top: 90px; right: 16px; z-index: 10; display: flex; flex-direction: column; gap: 6px; }
#bookmark-bar button { background: rgba(10,10,28,.85); border: 1px solid rgba(120,140,200,.2); color: #a0b8e0; border-radius: 6px; padding: 7px 12px; cursor: pointer; font-size: 11px; backdrop-filter: blur(6px); transition: all .2s; text-align: left; }
#bookmark-bar button:hover { background: rgba(120,180,240,.18); border-color: rgba(120,180,240,.45); }
#bookmark-bar button.save { color: #90e890; border-color: rgba(120,220,120,.3); }
#bookmark-bar button.save:hover { background: rgba(120,220,120,.15); }
#legend { position: absolute; bottom: 90px; left: 16px; z-index: 10; background: rgba(10,10,28,.85); border: 1px solid rgba(120,140,200,.2); border-radius: 8px; padding: 12px 16px; backdrop-filter: blur(6px); font-size: 11px; display: flex; flex-direction: column; gap: 8px; }
#legend .legend-row { display: flex; align-items: center; gap: 8px; }
#legend .legend-swatch { width: 30px; height: 4px; border-radius: 2px; }
#legend .legend-label { color: #889; text-transform: uppercase; letter-spacing: .7px; font-size: 10px; min-width: 70px; }
#legend .legend-val { color: #c0c8e0; font-weight: 600; font-variant-numeric: tabular-nums; font-size: 11px; }
#tooltip { position: absolute; pointer-events: none; z-index: 50; background: rgba(5,5,20,.92); border: 1px solid rgba(120,160,220,.4); border-radius: 6px; padding: 8px 12px; font-size: 11px; display: none; white-space: nowrap; }
</style>
</head>
<body>
<div id="container">
  <div id="state-overlay" class="loading">
    <div class="state-card">
      <div class="spinner"></div>
      <div class="state-title">Loading Data Landscape</div>
      <div class="state-desc">Generating terrain from time-series metrics...</div>
    </div>
  </div>
  <div id="ui-overlay" style="visibility:hidden;">
    <div id="top-bar">
      <div class="panel metric-pill"><span class="dot" style="background:#78d4f0;"></span><span class="label">Revenue</span><span class="value" id="val-rev">—</span></div>
      <div class="panel metric-pill"><span class="dot" style="background:#90e870;"></span><span class="label">Users</span><span class="value" id="val-users">—</span></div>
      <div class="panel metric-pill"><span class="dot" style="background:#e06060;"></span><span class="label">Errors</span><span class="value" id="val-err">—</span></div>
      <div class="panel metric-pill"><span class="dot" style="background:#f0c040;"></span><span class="label">API Calls</span><span class="value" id="val-api">—</span></div>
    </div>
    <div id="bookmark-bar">
      <button class="save" id="btn-save-bm">+ Save View</button>
      <button data-bm="0" style="display:none;">View 1</button>
      <button data-bm="1" style="display:none;">View 2</button>
      <button data-bm="2" style="display:none;">View 3</button>
    </div>
    <div id="legend">
      <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(90deg,#1a3a60,#78d4f0,#ffffff);"></span><span class="legend-label">Elevation</span><span class="legend-val">Revenue ($)</span></div>
      <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(90deg,#2d1a0a,#6b8c3a,#90e870);"></span><span class="legend-label">Vegetation</span><span class="legend-val">User Density</span></div>
      <div class="legend-row"><span class="legend-swatch" style="background:#e06060;"></span><span class="legend-label">Rivers</span><span class="legend-val">Error Paths</span></div>
      <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(90deg,#f0c040,#f08040);"></span><span class="legend-label">Particles</span><span class="legend-val">API Calls</span></div>
    </div>
    <div id="time-bar">
      <button id="btn-play">▶</button>
      <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
      <span id="time-label">T=0</span>
      <button id="btn-auto-rotate">⟳ Auto</button>
    </div>
    <div id="tooltip"></div>
  </div>
</div>
<script type="importmap">
{ "imports": { "three": "https://unpkg.com/three@0.160.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/" } }
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const STATE = { LOADING: 'loading', EMPTY: 'empty', ERROR: 'error', SUCCESS: 'success' };
const CONFIG = {
  gridSize: 80,
  terrainWidth: 60,
  terrainDepth: 60,
  heightScale: 12,
  timeSteps: 30,
  particleCount: 600,
  riverSamples: 200,
  dataDelayMs: 800,
  cameraDamping: 0.12,
  autoRotateSpeed: 0.4
};
function assert(cond, msg) { if (!cond) throw new Error(`[Terrain] ${msg}`); }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function lerp(a, b, t) { return a + (b - a) * t; }
let dataCache = null;
let geoCache = [];
let scene, camera, renderer, controls;
let terrainMesh, riverLines, particlePoints;
let currentTimeIdx = 0;
let isPlaying = false;
let playInterval = null;
let bookmarks = [];
let tooltipEl;
const elStateOverlay = document.getElementById('state-overlay');
const elUiOverlay = document.getElementById('ui-overlay');
const elTimeSlider = document.getElementById('time-slider');
const elTimeLabel = document.getElementById('time-label');
const elBtnPlay = document.getElementById('btn-play');
const elBtnAutoRotate = document.getElementById('btn-auto-rotate');
const elBtnSaveBm = document.getElementById('btn-save-bm');
const elBmBtns = document.querySelectorAll('#bookmark-bar button[data-bm]');
const elTooltip = document.getElementById('tooltip');
function setUIState(state) {
  elStateOverlay.className = state;
  if (state === STATE.LOADING) {
    elStateOverlay.querySelector('.state-icon')?.remove();
    elStateOverlay.querySelector('.state-title').textContent = 'Loading Data Landscape';
    elStateOverlay.querySelector('.state-desc').textContent = 'Generating terrain from time-series metrics...';
    elStateOverlay.querySelector('.spinner').style.display = 'block';
    elUiOverlay.style.visibility = 'hidden';
  } else if (state === STATE.EMPTY) {
    elStateOverlay.innerHTML = `<div class="state-card"><div class="state-icon empty">◇</div><div class="state-title">No Data Available</div><div class="state-desc">The dataset is empty. Import time-series data to generate the terrain.</div></div>`;
    elUiOverlay.style.visibility = 'hidden';
  } else if (state === STATE.ERROR) {
    elStateOverlay.innerHTML = `<div class="state-card"><div class="state-icon error">!</div><div class="state-title">Data Load Failed</div><div class="state-desc">Could not load terrain data. Check data source and try again.</div></div>`;
    elUiOverlay.style.visibility = 'hidden';
  } else if (state === STATE.SUCCESS) {
    elStateOverlay.className = 'success';
    elUiOverlay.style.visibility = 'visible';
  }
}
function generateData() {
  const G = CONFIG.gridSize;
  const T = CONFIG.timeSteps;
  const totalVertices = G * G;
  const revenue = new Float32Array(T * totalVertices);
  const userDensity = new Float32Array(T * totalVertices);
  const errors = new Float32Array(T * totalVertices);
  for (let t = 0; t < T; t++) {
    const timeFrac = t / (T - 1);
    const seasonal = Math.sin(timeFrac * Math.PI * 2) * 0.3;
    const trend = timeFrac * 0.5;
    const baseOffset = t * totalVertices;
    for (let iz = 0; iz < G; iz++) {
      for (let ix = 0; ix < G; ix++) {
        const idx = baseOffset + iz * G + ix;
        if (idx < 0 || idx >= T * totalVertices) {
          throw new Error(`[Bounds] revenue index ${idx} out of [0, ${T * totalVertices})`);
        }
        const nx = ix / (G - 1) - 0.5;
        const nz = iz / (G - 1) - 0.5;
        const dist = Math.sqrt(nx * nx + nz * nz);
        const ridge = Math.cos(nx * 3.5) * Math.cos(nz * 2.8) * 0.25;
        const valley = -Math.exp(-dist * 4) * 0.3;
        const baseRevenue = 0.3 + ridge + valley + trend + seasonal + Math.sin(nx * 8 + timeFrac * 3) * 0.08;
        revenue[idx] = clamp(baseRevenue + (Math.random() - 0.5) * 0.06, 0, 1);
        const centerBias = 1 - dist * 1.2;
        userDensity[idx] = clamp(centerBias + seasonal * 0.4 + (Math.random() - 0.5) * 0.1, 0.05, 1);
        const errSpike = (Math.abs(nx + 0.1) < 0.04 && timeFrac > 0.4 && timeFrac < 0.6) ? 0.7 : 0;
        const errZone = (dist < 0.25 && timeFrac > 0.7) ? 0.5 : 0;
        errors[idx] = clamp(errSpike + errZone + (Math.random() - 0.8) * 0.15, 0, 0.85);
      }
    }
  }
  return { revenue, userDensity, errors, gridSize: G, timeSteps: T };
}
function computeRiverPaths(data, timeIdx) {
  const G = data.gridSize;
  const baseOffset = timeIdx * G * G;
  const threshold = 0.15;
  const paths = [];
  const visited = new Uint8Array(G * G);
  for (let iz = 1; iz < G - 1; iz++) {
    for (let ix = 1; ix < G - 1; ix++) {
      const vi = iz * G + ix;
      if (visited[vi] || data.errors[baseOffset + vi] < threshold) continue;
      const path = [];
      let cx = ix, cz = iz;
      let steps = 0;
      const maxSteps = 150;
      while (steps < maxSteps && cx > 0 && cx < G - 1 && cz > 0 && cz < G - 1) {
        const ci = cz * G + cx;
        if (visited[ci]) break;
        visited[ci] = 1;
        path.push({ x: cx, z: cz, err: data.errors[baseOffset + ci] });
        let bestDir = -1, bestH = Infinity;
        const dirs = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]];
        for (let d = 0; d < 8; d++) {
          const nx = cx + dirs[d][0];
          const nz = cz + dirs[d][1];
          if (nx < 0 || nx >= G || nz < 0 || nz >= G) continue;
          const ni = nz * G + nx;
          if (data.revenue[baseOffset + ni] < bestH && data.errors[baseOffset + ni] > threshold * 0.6) {
            bestH = data.revenue[baseOffset + ni];
            bestDir = d;
          }
        }
        if (bestDir < 0) break;
        cx += dirs[bestDir][0];
        cz += dirs[bestDir][1];
        steps++;
      }
      if (path.length >= 4) paths.push(path);
    }
  }
  return paths;
}
function buildTerrainGeometry(data, timeIdx) {
  const G = data.gridSize;
  const W = CONFIG.terrainWidth;
  const D = CONFIG.terrainDepth;
  const HS = CONFIG.heightScale;
  const vertexCount = G * G;
  const baseOffset = timeIdx * vertexCount;
  const positions = new Float32Array(vertexCount * 3);
  const colors = new Float32Array(vertexCount * 3);
  for (let iz = 0; iz < G; iz++) {
    for (let ix = 0; ix < G; ix++) {
      const vi = iz * G + ix;
      const base3 = vi * 3;
      assert(base3 + 2 < vertexCount * 3, `position index ${base3 + 2} >= ${vertexCount * 3}`);
      const x = (ix / (G - 1) - 0.5) * W;
      const z = (iz / (G - 1) - 0.5) * D;
      const rev = data.revenue[baseOffset + vi];
      const y = rev * HS;
      positions[base3] = x;
      positions[base3 + 1] = y;
      positions[base3 + 2] = z;
    }
  }
  for (let iz = 0; iz < G; iz++) {
    for (let ix = 0; ix < G; ix++) {
      const vi = iz * G + ix;
      const base3 = vi * 3;
      assert(base3 + 2 < vertexCount * 3, `color index ${base3 + 2} >= ${vertexCount * 3}`);
      const density = data.userDensity[baseOffset + vi];
      const r = lerp(0.18, 0.08, density);
      const g = lerp(0.10, 0.55, density);
      const b = lerp(0.06, 0.22, density);
      colors[base3] = r;
      colors[base3 + 1] = g;
      colors[base3 + 2] = b;
    }
  }
  const indices = [];
  for (let iz = 0; iz < G - 1; iz++) {
    for (let ix = 0; ix < G - 1; ix++) {
      const a = iz * G + ix;
      const b = a + 1;
      const c = a + G;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geom.setIndex(indices);
  geom.computeVertexNormals();
  return geom;
}
function buildRiverGeometry(data, timeIdx) {
  const G = data.gridSize;
  const W = CONFIG.terrainWidth;
  const D = CONFIG.terrainDepth;
  const HS = CONFIG.heightScale;
  const baseOffset = timeIdx * G * G;
  const paths = computeRiverPaths(data, timeIdx);
  const group = new THREE.Group();
  for (let p = 0; p < paths.length; p++) {
    const path = paths[p];
    const pts = [];
    for (let i = 0; i < path.length; i++) {
      const x = (path[i].x / (G - 1) - 0.5) * W;
      const z = (path[i].z / (G - 1) - 0.5) * D;
      const vi = path[i].z * G + path[i].x;
      const y = data.revenue[baseOffset + vi] * HS + 0.15;
      pts.push(new THREE.Vector3(x, y, z));
    }
    const curve = new THREE.CatmullRomCurve3(pts);
    const sampled = curve.getPoints(CONFIG.riverSamples);
    const lineGeom = new THREE.BufferGeometry().setFromPoints(sampled);
    const alpha = clamp(path[0].err * 1.4, 0.3, 0.9);
    const mat = new THREE.LineBasicMaterial({
      color: new THREE.Color().setHSL(0, 0.85, 0.45 + alpha * 0.25),
      linewidth: 1,
      transparent: true,
      opacity: alpha,
      depthWrite: true
    });
    group.add(new THREE.Line(lineGeom, mat));
  }
  return group;
}
function buildParticleSystem(data, timeIdx, poolGeom, poolPositions) {
  const G = data.gridSize;
  const W = CONFIG.terrainWidth;
  const D = CONFIG.terrainDepth;
  const HS = CONFIG.heightScale;
  const baseOffset = timeIdx * G * G;
  const N = CONFIG.particleCount;
  const positions = poolPositions || new Float32Array(N * 3);
  const sizes = new Float32Array(N);
  for (let i = 0; i < N; i++) {
    const base3 = i * 3;
    assert(base3 + 2 < N * 3, `particle position index ${base3 + 2} >= ${N * 3}`);
    const gx = Math.random() * (G - 1);
    const gz = Math.random() * (G - 1);
    const ix = Math.floor(gx);
    const iz = Math.floor(gz);
    const fx = gx - ix;
    const fz = gz - iz;
    const ix1 = clamp(ix + 1, 0, G - 1);
    const iz1 = clamp(iz + 1, 0, G - 1);
    const h00 = data.revenue[baseOffset + clamp(iz, 0, G - 1) * G + clamp(ix, 0, G - 1)];
    const h10 = data.revenue[baseOffset + clamp(iz, 0, G - 1) * G + ix1];
    const h01 = data.revenue[baseOffset + iz1 * G + clamp(ix, 0, G - 1)];
    const h11 = data.revenue[baseOffset + iz1 * G + ix1];
    const h = lerp(lerp(h00, h10, fx), lerp(h01, h11, fx), fz);
    const x = (gx / (G - 1) - 0.5) * W;
    const z = (gz / (G - 1) - 0.5) * D;
    const y = h * HS + 0.4 + Math.random() * 0.8;
    positions[base3] = x;
    positions[base3 + 1] = y;
    positions[base3 + 2] = z;
    sizes[i] = 0.08 + Math.random() * 0.22;
  }
  let geom;
  if (poolGeom) {
    geom = poolGeom;
    geom.attributes.position.needsUpdate = true;
    geom.attributes.size.needsUpdate = true;
  } else {
    geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  }
  return { geometry: geom, positions, sizes };
}
function createScene() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color('#0a0a18');
  scene.fog = new THREE.Fog('#0a0a18', 30, 100);
  const ambient = new THREE.AmbientLight('#304060', 1.4);
  scene.add(ambient);
  const sun = new THREE.DirectionalLight('#ffe8d0', 3.5);
  sun.position.set(40, 50, 35);
  scene.add(sun);
  const fill = new THREE.DirectionalLight('#6080c0', 1.2);
  fill.position.set(-20, 10, -15);
  scene.add(fill);
  const gridHelper = new THREE.GridHelper(60, 40, '#1a2a40', '#0d1520');
  gridHelper.position.y = -0.05;
  scene.add(gridHelper);
}
function createRenderer() {
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  document.getElementById('container').appendChild(renderer.domElement);
}
function createControls() {
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 200);
  camera.position.set(28, 22, 36);
  camera.lookAt(0, 3, 0);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 3, 0);
  controls.enableDamping = true;
  controls.dampingFactor = CONFIG.cameraDamping;
  controls.autoRotate = true;
  controls.autoRotateSpeed = CONFIG.autoRotateSpeed;
  controls.minDistance = 8;
  controls.maxDistance = 80;
  controls.maxPolarAngle = Math.PI * 0.48;
  controls.update();
}
function applyTerrain(timeIdx) {
  if (!dataCache) return;
  currentTimeIdx = timeIdx;
  elTimeSlider.value = timeIdx;
  elTimeLabel.textContent = `T=${timeIdx}`;
  if (geoCache[timeIdx]) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geoCache[timeIdx];
  } else {
    const newGeom = buildTerrainGeometry(dataCache, timeIdx);
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = newGeom;
    geoCache[timeIdx] = newGeom;
  }
  if (riverLines) {
    scene.remove(riverLines);
    riverLines.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); });
  }
  riverLines = buildRiverGeometry(dataCache, timeIdx);
  scene.add(riverLines);
  const poolGeom = particlePoints ? particlePoints.geometry : null;
  const poolPos = particlePoints ? particlePoints.geometry.attributes.position.array : null;
  const { geometry: newParticleGeom, positions } = buildParticleSystem(dataCache, timeIdx, poolGeom, poolPos);
  if (particlePoints) {
    if (particlePoints.geometry !== newParticleGeom) {
      particlePoints.geometry.dispose();
      particlePoints.geometry = newParticleGeom;
    }
  } else {
    const pMat = new THREE.PointsMaterial({
      size: 0.25,
      color: '#f0c040',
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.75,
      sizeAttenuation: true
    });
    particlePoints = new THREE.Points(newParticleGeom, pMat);
    scene.add(particlePoints);
  }
  updateMetricsDisplay(timeIdx);
}
function updateMetricsDisplay(timeIdx) {
  if (!dataCache) return;
  const G = dataCache.gridSize;
  const offset = timeIdx * G * G;
  let sumRev = 0, sumUsers = 0, sumErr = 0, sumApi = 0;
  const N = G * G;
  for (let i = 0; i < N; i++) {
    sumRev += dataCache.revenue[offset + i];
    sumUsers += dataCache.userDensity[offset + i];
    sumErr += dataCache.errors[offset + i];
  }
  const apiCalls = Math.round(3000 + sumRev * 8000 + (Math.sin(timeIdx * 0.4) * 2000));
  document.getElementById('val-rev').textContent = '$' + (Math.round(sumRev / N * 1000) / 100).toFixed(1) + 'K';
  document.getElementById('val-users').textContent = Math.round(sumUsers / N * 100) + '%';
  document.getElementById('val-err').textContent = (sumErr / N * 100).toFixed(2) + '%';
  document.getElementById('val-api').textContent = (apiCalls / 1000).toFixed(1) + 'K';
}
function saveBookmark() {
  if (bookmarks.length >= 3) {
    bookmarks.shift();
  }
  bookmarks.push({
    position: camera.position.clone(),
    target: controls.target.clone(),
    timeIdx: currentTimeIdx
  });
  for (let i = 0; i < elBmBtns.length; i++) {
    if (i < bookmarks.length) {
      elBmBtns[i].style.display = 'block';
      elBmBtns[i].textContent = `View ${i + 1}  T=${bookmarks[i].timeIdx}`;
    } else {
      elBmBtns[i].style.display = 'none';
    }
  }
}
function loadBookmark(idx) {
  if (idx < 0 || idx >= bookmarks.length) return;
  const bm = bookmarks[idx];
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function animate(now) {
    const elapsed = now - startTime;
    const t = clamp(elapsed / duration, 0, 1);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    camera.position.lerpVectors(startPos, bm.position, ease);
    controls.target.lerpVectors(startTarget, bm.target, ease);
    if (t < 1) {
      requestAnimationFrame(animate);
    }
  }
  if (bm.timeIdx !== currentTimeIdx) {
    applyTerrain(bm.timeIdx);
  }
  requestAnimationFrame(animate);
}
async function init() {
  setUIState(STATE.LOADING);
  try {
    const dataPromise = new Promise((resolve) => {
      setTimeout(() => {
        const data = generateData();
        const G = data.gridSize;
        const hasData = data.revenue.some(v => v > 0.01);
        if (!hasData) {
          throw new Error('empty');
        }
        resolve(data);
      }, CONFIG.dataDelayMs);
    });
    const result = await Promise.race([
      dataPromise,
      new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 8000))
    ]);
    if (!result || !result.revenue || result.revenue.length === 0) {
      setUIState(STATE.EMPTY);
      return;
    }
    dataCache = result;
    geoCache = new Array(dataCache.timeSteps);
    createScene();
    createRenderer();
    createControls();
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.7,
      metalness: 0.05,
      flatShading: false,
      side: THREE.DoubleSide
    });
    const initGeom = buildTerrainGeometry(dataCache, 0);
    geoCache[0] = initGeom;
    terrainMesh = new THREE.Mesh(initGeom, mat);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
    riverLines = buildRiverGeometry(dataCache, 0);
    scene.add(riverLines);
    const { geometry: pGeom } = buildParticleSystem(dataCache, 0, null, null);
    const pMat = new THREE.PointsMaterial({
      size: 0.25,
      color: '#f0c040',
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.75,
      sizeAttenuation: true
    });
    particlePoints = new THREE.Points(pGeom, pMat);
    scene.add(particlePoints);
    elTimeSlider.max = dataCache.timeSteps - 1;
    elTimeSlider.value = 0;
    elTimeLabel.textContent = 'T=0';
    updateMetricsDisplay(0);
    controls.addEventListener('change', () => {
      if (controls.autoRotate) {
        elBtnAutoRotate.textContent = '⟳ Auto';
      }
    });
    setUIState(STATE.SUCCESS);
    animate();
  } catch (err) {
    console.error('[Terrain] Init failed:', err);
    setUIState(STATE.ERROR);
    createScene();
    createRenderer();
    createControls();
    const errorGeom = new THREE.SphereGeometry(0.5);
    const errorMat = new THREE.MeshBasicMaterial({ color: '#e06060', wireframe: true });
    scene.add(new THREE.Mesh(errorGeom, errorMat));
    elUiOverlay.style.visibility = 'visible';
    animate();
  }
}
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  if (isPlaying && dataCache) {
    const next = (currentTimeIdx + 1) % dataCache.timeSteps;
    applyTerrain(next);
  }
  renderer.render(scene, camera);
}
elTimeSlider.addEventListener('input', () => {
  const idx = parseInt(elTimeSlider.value, 10);
  if (idx >= 0 && idx < (dataCache?.timeSteps || 0)) {
    applyTerrain(idx);
  }
});
elBtnPlay.addEventListener('click', () => {
  isPlaying = !isPlaying;
  elBtnPlay.textContent = isPlaying ? '⏸' : '▶';
});
elBtnAutoRotate.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  elBtnAutoRotate.textContent = controls.autoRotate ? '⟳ Auto' : '⟳ Off';
});
elBtnSaveBm.addEventListener('click', saveBookmark);
elBmBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.bm, 10);
    loadBookmark(idx);
  });
});
window.addEventListener('resize', () => {
  if (camera && renderer) {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }
});
init();
</script>
</body>
</html>
```