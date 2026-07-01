<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a0f;
    --panel-bg: rgba(10,10,20,0.92);
    --text: #c8ccd4;
    --accent: #4da6ff;
    --river: #e63946;
    --btn-bg: rgba(30,30,50,0.85);
    --btn-hover: rgba(60,60,100,0.9);
    --slider-track: #2a2a3a;
    --slider-fill: #4da6ff;
    --border: rgba(255,255,255,0.08);
    --shadow: 0 2px 16px rgba(0,0,0,0.5);
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg);
    overflow:hidden;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: var(--text);
    user-select: none;
    -webkit-user-select: none;
    height: 100vh;
    width: 100vw;
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 1;
  }
  canvas { display: block; }
  #fallback {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 10;
    background: var(--bg);
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 16px;
  }
  #fallback canvas { border-radius: 8px; border: 1px solid var(--border); }
  #panel {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 5;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 12px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 420px;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
  }
  #panel-top {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }
  #time-label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--accent);
    min-width: 80px;
    text-align: right;
  }
  #time-slider {
    flex: 1;
    -webkit-appearance: none;
    height: 6px;
    border-radius: 3px;
    background: var(--slider-track);
    outline: none;
    cursor: pointer;
  }
  #time-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: var(--slider-fill);
    border: 2px solid #fff;
    cursor: pointer;
    box-shadow: 0 0 8px rgba(77,166,255,0.5);
  }
  #panel-bottom {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
  }
  button {
    background: var(--btn-bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 6px 11px;
    font-size: 11px;
    font-weight: 500;
    cursor: pointer;
    letter-spacing: 0.03em;
    transition: background 0.15s, border-color 0.15s;
    white-space: nowrap;
  }
  button:hover { background: var(--btn-hover); border-color: rgba(255,255,255,0.18); }
  button.active { background: var(--accent); color: #000; border-color: var(--accent); font-weight: 700; }
  button.bm { font-size: 10px; padding: 4px 9px; }
  #info-overlay {
    position: fixed;
    top: 16px;
    left: 16px;
    z-index: 5;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 12px;
    line-height: 1.6;
    backdrop-filter: blur(12px);
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .metric { display: flex; gap: 8px; align-items: center; }
  .metric-swatch { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
  .metric-label { opacity: 0.7; min-width: 70px; }
  .metric-value { font-weight: 600; }
  #help-overlay {
    display: none;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%,-50%);
    z-index: 20;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    font-size: 12px;
    line-height: 1.8;
    backdrop-filter: blur(16px);
    box-shadow: var(--shadow);
    min-width: 280px;
  }
  #help-overlay kbd {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 3px;
    padding: 1px 5px;
    font-family: inherit;
    font-size: 11px;
  }
  #help-overlay.visible { display: block; }
  @media (max-width: 600px) {
    #panel { min-width: auto; left: 8px; right: 8px; transform: none; border-radius: 8px; padding: 10px 14px; }
    #info-overlay { top: 8px; left: 8px; font-size: 10px; padding: 8px 12px; }
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="fallback">
  <p style="font-size:18px;font-weight:600;">WebGL not available</p>
  <p style="opacity:0.6;font-size:13px;">Showing 2D heatmap fallback</p>
  <canvas id="fallback-canvas" width="640" height="400"></canvas>
</div>
<div id="info-overlay">
  <div class="metric"><span class="metric-swatch" style="background:#4ecdc4;"></span><span class="metric-label">Revenue</span><span class="metric-value" id="val-revenue">--</span></div>
  <div class="metric"><span class="metric-swatch" style="background:#ffe66d;"></span><span class="metric-label">Users</span><span class="metric-value" id="val-users">--</span></div>
  <div class="metric"><span class="metric-swatch" style="background:#e63946;"></span><span class="metric-label">Errors</span><span class="metric-value" id="val-errors">--</span></div>
  <div class="metric"><span class="metric-swatch" style="background:#a78bfa;"></span><span class="metric-label">API Calls</span><span class="metric-value" id="val-api">--</span></div>
</div>
<div id="panel">
  <div id="panel-top">
    <span id="time-label">Day 1</span>
    <input type="range" id="time-slider" min="0" max="29" value="0" step="1" aria-label="Time slider, use left/right arrow keys to scrub through days">
  </div>
  <div id="panel-bottom">
    <button class="bm" data-idx="0">Overview</button>
    <button class="bm" data-idx="1">Revenue Peak</button>
    <button class="bm" data-idx="2">River Trace</button>
    <button class="bm" data-idx="3">Top-Down</button>
    <button id="btn-play" aria-label="Toggle auto-rotation">Auto</button>
    <button id="btn-help">?</button>
  </div>
</div>
<div id="help-overlay" role="dialog" aria-label="Keyboard shortcuts">
  <strong style="color:var(--accent);">Keyboard Shortcuts</strong><br>
  <kbd>1</kbd>-<kbd>4</kbd> Camera bookmarks<br>
  <kbd>&larr;</kbd><kbd>&rarr;</kbd> Time scrub<br>
  <kbd>Space</kbd> Toggle auto-rotate<br>
  <kbd>R</kbd> Reset view<br>
  <kbd>F</kbd> Fit all<br>
  <kbd>+</kbd><kbd>-</kbd> Zoom<br>
  <kbd>?</kbd> Toggle this help<br>
  <span style="opacity:0.5;font-size:10px;">Mouse: drag=orbit, scroll=zoom, right-drag=pan</span>
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
const TIME_STEPS = 30;
const TERRAIN_SCALE = 8;
const HEIGHT_SCALE = 3.5;
const PARTICLE_COUNT = 600;
const fallbackEl = document.getElementById('fallback');
const container = document.getElementById('canvas-container');
const webglSupported = (() => {
  try {
    const c = document.createElement('canvas');
    return !!(c.getContext('webgl2') || c.getContext('webgl'));
  } catch { return false; }
})();
if (!webglSupported) {
  fallbackEl.style.display = 'flex';
  renderFallback();
}
let scene, camera, renderer, controls;
let terrainMesh, riverGroup, particleSystem;
let heightData = [];
let userData = [];
let errorData = [];
let apiData = [];
let cachedGeometries = [];
let cachedColors = [];
let currentTimeIdx = 0;
let autoRotate = true;
let bookmarks = [];
let clock = new THREE.Clock();
function generateData() {
  const simplex2D = (x, y, seed) => {
    const f = 2.3;
    const a = [1.0, 0.5, 0.25, 0.125, 0.06];
    const fx = [f, f*2.1, f*4.3, f*8.7, f*17.1];
    const fy = [f*1.3, f*2.7, f*5.1, f*9.3, f*18.7];
    let v = 0;
    for (let i = 0; i < a.length; i++) {
      v += a[i] * Math.sin(x * fx[i] + seed * 1.7 + i * 2.3) * Math.cos(y * fy[i] + seed * 0.9 - i * 1.4);
    }
    return v / 1.8;
  };
  for (let t = 0; t < TIME_STEPS; t++) {
    const phase = t / TIME_STEPS;
    const hSlice = new Float32Array(GRID * GRID);
    const uSlice = new Float32Array(GRID * GRID);
    const eSlice = new Float32Array(GRID * GRID);
    const aSlice = new Float32Array(GRID * GRID);
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const nx = ix / (GRID - 1);
        const ny = iy / (GRID - 1);
        let height = simplex2D(nx * 3, ny * 3, phase * 5);
        height += 0.4 * Math.sin(nx * 8 + phase * 3) * Math.cos(ny * 7 - phase * 2);
        height += 0.3 * nx * (1 - ny);
        const peakX = 0.35 + 0.3 * Math.sin(phase * Math.PI * 2);
        const peakY = 0.55 + 0.2 * Math.cos(phase * Math.PI * 1.7);
        const distPeak = Math.sqrt((nx - peakX)**2 + (ny - peakY)**2);
        height += 0.65 * Math.exp(-distPeak * 4.5);
        height = Math.max(0, Math.min(1, height * 0.5 + 0.25));
        hSlice[iy * GRID + ix] = height;
        let users = simplex2D(nx * 2.5 + 1, ny * 2.5 + 1, phase * 4 + 2);
        users += 0.6 * height;
        users += 0.25 * Math.exp(-((nx-0.6)**2 + (ny-0.4)**2) * 6);
        users = Math.max(0, Math.min(1, users * 0.5 + 0.3));
        uSlice[iy * GRID + ix] = users;
        let err = Math.abs(simplex2D(nx * 4.2 + 2, ny * 4.2 + 2, phase * 3.5 + 1));
        err += 0.35 * (1 - height);
        const riverPath = Math.abs(ny - (0.25 + 0.5 * nx + 0.15 * Math.sin(nx * 8 + phase * 4)));
        err -= 0.15 * Math.exp(-riverPath * 20);
        err = Math.max(0, Math.min(1, err * 0.65));
        eSlice[iy * GRID + ix] = err;
        let api = simplex2D(nx * 3.7 + 3, ny * 3.7 + 3, phase * 2.8 + 3);
        api += 0.5 * height;
        api += 0.2 * users;
        const valleyMask = Math.exp(-((nx-0.7)**2 + (ny-0.3)**2) * 3);
        api += 0.3 * valleyMask;
        api = Math.max(0, Math.min(1, api * 0.5 + 0.25));
        aSlice[iy * GRID + ix] = api;
      }
    }
    heightData.push(hSlice);
    userData.push(uSlice);
    errorData.push(eSlice);
    apiData.push(aSlice);
  }
}
function prebuildGeometries() {
  for (let t = 0; t < TIME_STEPS; t++) {
    const h = heightData[t];
    const u = userData[t];
    const positions = new Float32Array(GRID * GRID * 3);
    const colors = new Float32Array(GRID * GRID * 3);
    for (let iy = 0; iy < GRID; iy++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iy * GRID + ix;
        const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SCALE;
        const z = (iy / (GRID - 1) - 0.5) * TERRAIN_SCALE;
        const y = h[idx] * HEIGHT_SCALE;
        positions[idx * 3] = x;
        positions[idx * 3 + 1] = y;
        positions[idx * 3 + 2] = z;
        const uv = u[idx];
        const r = 0.12 + uv * 0.55;
        const g = 0.55 + uv * 0.4;
        const b = 0.08 + uv * 0.08;
        colors[idx * 3] = r;
        colors[idx * 3 + 1] = g;
        colors[idx * 3 + 2] = b;
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
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.setIndex(indices);
    geo.computeVertexNormals();
    cachedGeometries.push(geo);
    cachedColors.push(colors);
  }
}
function buildRiverGeometry(timeIdx) {
  if (riverGroup) {
    while (riverGroup.children.length) riverGroup.remove(riverGroup.children[0]);
  }
  const err = errorData[timeIdx];
  const h = heightData[timeIdx];
  const threshold = 0.35;
  const points = [];
  for (let iy = 1; iy < GRID - 1; iy++) {
    let maxErr = 0;
    let maxIx = 0;
    for (let ix = 0; ix < GRID; ix++) {
      const e = err[iy * GRID + ix];
      if (e > maxErr) { maxErr = e; maxIx = ix; }
    }
    if (maxErr > threshold) {
      const x = (maxIx / (GRID - 1) - 0.5) * TERRAIN_SCALE;
      const z = (iy / (GRID - 1) - 0.5) * TERRAIN_SCALE;
      const y = h[iy * GRID + maxIx] * HEIGHT_SCALE + 0.04;
      points.push(new THREE.Vector3(x, y, z));
    }
  }
  if (points.length < 2) return;
  const curve = new THREE.CatmullRomCurve3(points);
  const tubePoints = curve.getPoints(points.length * 2);
  const tubeGeo = new THREE.BufferGeometry().setFromPoints(tubePoints);
  const positions = tubeGeo.attributes.position.array;
  const riverColors = new Float32Array(positions.length);
  for (let i = 0; i < tubePoints.length; i++) {
    const alpha = i / (tubePoints.length - 1);
    riverColors[i * 3] = 0.9;
    riverColors[i * 3 + 1] = 0.15 + alpha * 0.15;
    riverColors[i * 3 + 2] = 0.1 + alpha * 0.2;
  }
  tubeGeo.setAttribute('color', new THREE.BufferAttribute(riverColors, 3));
  const mat = new THREE.MeshBasicMaterial({
    vertexColors: true,
    transparent: true,
    opacity: 0.85,
    linewidth: 1,
  });
  const riverCurve = new THREE.Line(tubeGeo, mat);
  riverCurve.renderOrder = 1;
  riverCurve.material.depthTest = true;
  riverCurve.material.depthWrite = false;
  riverGroup.add(riverCurve);
  const glowGeo = tubeGeo.clone();
  const glowMat = new THREE.MeshBasicMaterial({
    vertexColors: true,
    transparent: true,
    opacity: 0.25,
  });
  const glowLine = new THREE.Line(glowGeo, glowMat);
  glowLine.renderOrder = 0;
  glowLine.material.depthTest = true;
  glowLine.material.depthWrite = false;
  glowLine.scale.set(1, 1.03, 1);
  riverGroup.add(glowLine);
}
class ParticleFlow {
  constructor(count, timeIdx) {
    this.count = count;
    this.positions = new Float32Array(count * 3);
    this.velocities = new Float32Array(count * 3);
    this.lifetimes = new Float32Array(count);
    this.seeds = new Float32Array(count * 2);
    for (let i = 0; i < count; i++) {
      this.seeds[i * 2] = Math.random();
      this.seeds[i * 2 + 1] = Math.random();
      this.lifetimes[i] = Math.random();
    }
    this.updatePositions(timeIdx);
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    const pointSizes = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      pointSizes[i] = 1.2 + Math.random() * 1.8;
    }
    geo.setAttribute('size', new THREE.BufferAttribute(pointSizes, 1));
    const mat = new THREE.PointsMaterial({
      color: 0xa78bfa,
      size: 0.04,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      depthTest: true,
      transparent: true,
      opacity: 0.75,
      sizeAttenuation: true,
    });
    this.points = new THREE.Points(geo, mat);
    this.points.renderOrder = 2;
  }
  updatePositions(timeIdx) {
    const h = heightData[timeIdx];
    const a = apiData[timeIdx];
    for (let i = 0; i < this.count; i++) {
      let sx = this.seeds[i * 2];
      let sy = this.seeds[i * 2 + 1];
      const life = this.lifetimes[i];
      sx = (sx + life * 0.03 + Math.sin(life * 13.7) * 0.012) % 1;
      sy = (sy + life * 0.025 + Math.cos(life * 11.3) * 0.01) % 1;
      this.seeds[i * 2] = sx;
      this.seeds[i * 2 + 1] = sy;
      const ix = Math.floor(sx * (GRID - 1));
      const iy = Math.floor(sy * (GRID - 1));
      const idx = Math.max(0, Math.min(GRID * GRID - 1, iy * GRID + ix));
      const height = h[idx] * HEIGHT_SCALE;
      const x = (sx - 0.5) * TERRAIN_SCALE;
      const z = (sy - 0.5) * TERRAIN_SCALE;
      const y = height + 0.06 + a[idx] * 0.3;
      this.positions[i * 3] = x;
      this.positions[i * 3 + 1] = y;
      this.positions[i * 3 + 2] = z;
      this.lifetimes[i] = (life + 0.003 + Math.random() * 0.002) % 1;
    }
    this.points.geometry.attributes.position.needsUpdate = true;
  }
  getObject() { return this.points; }
}
function initThree() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a14);
  scene.fog = new THREE.Fog(0x0a0a14, 8, 28);
  camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 50);
  camera.position.set(5.5, 4.8, 7.2);
  camera.lookAt(0, 0.8, 0);
  renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setSize(container.clientWidth, container.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  container.appendChild(renderer.domElement);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = autoRotate;
  controls.autoRotateSpeed = 0.3;
  controls.target.set(0, 1.2, 0);
  controls.minDistance = 3;
  controls.maxDistance = 16;
  controls.maxPolarAngle = Math.PI * 0.7;
  controls.update();
  const ambientLight = new THREE.AmbientLight(0x303050, 1.6);
  scene.add(ambientLight);
  const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
  sun.position.set(8, 12, 4);
  sun.castShadow = true;
  sun.shadow.mapSize.width = 1024;
  sun.shadow.mapSize.height = 1024;
  sun.shadow.camera.near = 0.5;
  sun.shadow.camera.far = 40;
  sun.shadow.camera.left = -8;
  sun.shadow.camera.right = 8;
  sun.shadow.camera.top = 8;
  sun.shadow.camera.bottom = -8;
  sun.shadow.bias = -0.0004;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x4466aa, 1.0);
  fill.position.set(-4, 2, -3);
  scene.add(fill);
  const rim = new THREE.DirectionalLight(0x8899cc, 0.8);
  rim.position.set(0, -1, 6);
  scene.add(rim);
  const material = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.15,
    flatShading: false,
  });
  terrainMesh = new THREE.Mesh(cachedGeometries[0], material);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  terrainMesh.frustumCulled = true;
  scene.add(terrainMesh);
  const gridHelper = new THREE.GridHelper(TERRAIN_SCALE, 20, 0x222244, 0x111122);
  gridHelper.position.y = -0.01;
  scene.add(gridHelper);
  riverGroup = new THREE.Group();
  scene.add(riverGroup);
  buildRiverGeometry(0);
  particleSystem = new ParticleFlow(PARTICLE_COUNT, 0);
  scene.add(particleSystem.getObject());
  bookmarks = [
    { pos: new THREE.Vector3(5.5, 4.8, 7.2), target: new THREE.Vector3(0, 1.2, 0), label: 'Overview' },
    { pos: new THREE.Vector3(3.0, 3.5, 2.5), target: new THREE.Vector3(0.2, 1.8, 0.4), label: 'Revenue Peak' },
    { pos: new THREE.Vector3(1.5, 1.8, -3.5), target: new THREE.Vector3(0.3, 0.9, -0.1), label: 'River Trace' },
    { pos: new THREE.Vector3(0, 7.5, 0.3), target: new THREE.Vector3(0, 1.2, 0), label: 'Top-Down' },
  ];
}
function swapTerrain(timeIdx) {
  if (timeIdx === currentTimeIdx) return;
  currentTimeIdx = timeIdx;
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = cachedGeometries[timeIdx];
  buildRiverGeometry(timeIdx);
  particleSystem.updatePositions(timeIdx);
  updateInfoPanel(timeIdx);
}
function updateInfoPanel(timeIdx) {
  const h = heightData[timeIdx];
  const u = userData[timeIdx];
  const e = errorData[timeIdx];
  const a = apiData[timeIdx];
  let sumH = 0, sumU = 0, sumE = 0, sumA = 0;
  const n = GRID * GRID;
  for (let i = 0; i < n; i++) { sumH += h[i]; sumU += u[i]; sumE += e[i]; sumA += a[i]; }
  const avgH = sumH / n;
  const avgU = sumU / n;
  const avgE = sumE / n;
  const avgA = sumA / n;
  document.getElementById('val-revenue').textContent = (avgH * 100).toFixed(0) + '%';
  document.getElementById('val-users').textContent = (avgU * 100).toFixed(0) + '%';
  document.getElementById('val-errors').textContent = (avgE * 100).toFixed(1) + '%';
  document.getElementById('val-api').textContent = (avgA * 100).toFixed(0) + '%';
  document.getElementById('time-label').textContent = 'Day ' + (timeIdx + 1);
  document.getElementById('time-slider').value = timeIdx;
}
function animateCameraTo(pos, target, duration = 800) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  function step(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, pos, ease);
    controls.target.lerpVectors(startTarget, target, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(step);
    }
  }
  requestAnimationFrame(step);
}
function goToBookmark(idx) {
  const bm = bookmarks[idx];
  if (!bm) return;
  animateCameraTo(bm.pos, bm.target);
  document.querySelectorAll('button.bm').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`button.bm[data-idx="${idx}"]`);
  if (btn) btn.classList.add('active');
}
function resetView() {
  animateCameraTo(
    new THREE.Vector3(5.5, 4.8, 7.2),
    new THREE.Vector3(0, 1.2, 0)
  );
  document.querySelectorAll('button.bm').forEach(b => b.classList.remove('active'));
}
function fitView() {
  const box = new THREE.Box3().setFromObject(terrainMesh);
  const center = new THREE.Vector3();
  box.getCenter(center);
  const size = new THREE.Vector3();
  box.getSize(size);
  const maxDim = Math.max(size.x, size.y, size.z);
  const dist = maxDim / (2 * Math.tan((camera.fov * Math.PI) / 360));
  const pos = center.clone().add(new THREE.Vector3(dist * 0.7, dist * 0.5, dist * 0.7));
  animateCameraTo(pos, center);
}
function renderFallback() {
  const fc = document.getElementById('fallback-canvas');
  const ctx = fc.getContext('2d');
  const w = fc.width, h = fc.height;
  const imgData = ctx.createImageData(w, h);
  for (let py = 0; py < h; py++) {
    for (let px = 0; px < w; px++) {
      const nx = px / w;
      const ny = py / h;
      const val = Math.sin(nx * 8) * Math.cos(ny * 6) * 0.5 + 0.5;
      const i = (py * w + px) * 4;
      imgData.data[i] = Math.floor(val * 60 + 20);
      imgData.data[i + 1] = Math.floor(val * 140 + 40);
      imgData.data[i + 2] = Math.floor(val * 200 + 30);
      imgData.data[i + 3] = 255;
    }
  }
  ctx.putImageData(imgData, 0, 0);
}
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  if (particleSystem) {
    particleSystem.updatePositions(currentTimeIdx);
  }
  renderer.render(scene, camera);
}
function setupUI() {
  const slider = document.getElementById('time-slider');
  slider.addEventListener('input', () => {
    const idx = parseInt(slider.value);
    swapTerrain(idx);
  });
  document.querySelectorAll('button.bm').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = parseInt(btn.dataset.idx);
      goToBookmark(idx);
    });
  });
  document.getElementById('btn-play').addEventListener('click', function() {
    autoRotate = !autoRotate;
    controls.autoRotate = autoRotate;
    this.classList.toggle('active', autoRotate);
    this.textContent = autoRotate ? 'Auto:ON' : 'Auto';
  });
  document.getElementById('btn-play').classList.add('active');
  document.getElementById('btn-help').addEventListener('click', () => {
    const help = document.getElementById('help-overlay');
    help.classList.toggle('visible');
  });
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;
    switch (e.key) {
      case '1': case '2': case '3': case '4':
        goToBookmark(parseInt(e.key) - 1);
        break;
      case 'ArrowLeft':
        e.preventDefault();
        slider.value = Math.max(0, currentTimeIdx - 1);
        swapTerrain(parseInt(slider.value));
        break;
      case 'ArrowRight':
        e.preventDefault();
        slider.value = Math.min(TIME_STEPS - 1, currentTimeIdx + 1);
        swapTerrain(parseInt(slider.value));
        break;
      case ' ':
        e.preventDefault();
        autoRotate = !autoRotate;
        controls.autoRotate = autoRotate;
        const playBtn = document.getElementById('btn-play');
        playBtn.classList.toggle('active', autoRotate);
        playBtn.textContent = autoRotate ? 'Auto:ON' : 'Auto';
        break;
      case 'r': case 'R':
        resetView();
        break;
      case 'f': case 'F':
        fitView();
        break;
      case '=': case '+':
        camera.zoom *= 1.15;
        camera.updateProjectionMatrix();
        break;
      case '-':
        camera.zoom /= 1.15;
        camera.updateProjectionMatrix();
        break;
      case '?':
        document.getElementById('help-overlay').classList.toggle('visible');
        break;
      case 'Escape':
        document.getElementById('help-overlay').classList.remove('visible');
        break;
    }
  });
  window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
  });
  document.getElementById('help-overlay').addEventListener('click', function(e) {
    if (e.target === this) this.classList.remove('visible');
  });
}
generateData();
prebuildGeometries();
initThree();
setupUI();
updateInfoPanel(0);
animate();
</script>
</body>
</html>