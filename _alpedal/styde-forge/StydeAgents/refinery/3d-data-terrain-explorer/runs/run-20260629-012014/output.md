```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0d1117;
    --panel: #161b22;
    --text: #c9d1d9;
    --accent: #58a6ff;
    --danger: #f85149;
    --success: #3fb950;
    --border: #30363d;
    --radius: 8px;
    --font: 'Segoe UI', system-ui, -apple-system, sans-serif;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    overflow: hidden;
    height: 100vh;
    width: 100vw;
  }
  #canvas-container {
    position: fixed;
    inset: 0;
    z-index: 1;
    cursor: grab;
  }
  #canvas-container:active { cursor: grabbing; }
  #canvas-container.panning { cursor: move; }
  /* Loading overlay */
  #loading-overlay {
    position: fixed; inset: 0; z-index: 100;
    background: var(--bg);
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    transition: opacity 0.5s ease;
  }
  #loading-overlay.hidden { opacity: 0; pointer-events: none; }
  #loading-overlay .spinner {
    width: 48px; height: 48px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  #loading-overlay .label { margin-top: 16px; font-size: 14px; color: var(--text); }
  /* Error overlay */
  #error-overlay {
    position: fixed; inset: 0; z-index: 101;
    background: rgba(13, 17, 23, 0.95);
    display: none; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 24px;
  }
  #error-overlay.visible { display: flex; }
  #error-overlay .icon { font-size: 48px; margin-bottom: 16px; }
  #error-overlay .msg { font-size: 16px; max-width: 400px; line-height: 1.5; }
  #error-overlay .retry {
    margin-top: 20px; padding: 10px 24px;
    background: var(--accent); color: #fff;
    border: none; border-radius: var(--radius);
    cursor: pointer; font-size: 14px;
  }
  /* Empty state */
  #empty-state {
    position: fixed; inset: 0; z-index: 99;
    display: none; flex-direction: column;
    align-items: center; justify-content: center;
    color: var(--text); text-align: center;
  }
  #empty-state.visible { display: flex; }
  #empty-state .icon { font-size: 56px; margin-bottom: 16px; opacity: 0.6; }
  #empty-state .title { font-size: 20px; margin-bottom: 8px; }
  #empty-state .subtitle { font-size: 14px; opacity: 0.7; max-width: 360px; line-height: 1.5; }
  /* Bottom control bar */
  #controls {
    position: fixed; bottom: 20px; left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 20px;
    display: flex; gap: 16px; align-items: center;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    flex-wrap: wrap; justify-content: center;
  }
  #controls label { font-size: 12px; white-space: nowrap; }
  #time-slider {
    width: 200px; accent-color: var(--accent);
    cursor: pointer;
  }
  #time-label {
    font-size: 12px; min-width: 60px; text-align: center;
    font-variant-numeric: tabular-nums;
  }
  #controls button {
    background: var(--border); color: var(--text);
    border: 1px solid var(--border);
    border-radius: 4px; padding: 6px 12px;
    cursor: pointer; font-size: 12px;
    transition: background 0.15s;
    white-space: nowrap;
  }
  #controls button:hover { background: #3a3f47; }
  #controls button.active { background: var(--accent); color: #fff; border-color: var(--accent); }
  /* Legend */
  #legend {
    position: fixed; top: 20px; right: 20px; z-index: 10;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 16px;
    font-size: 11px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    max-width: 200px;
  }
  #legend .row { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
  #legend .swatch { width: 12px; height: 12px; border-radius: 2px; flex-shrink: 0; }
  /* Stats HUD */
  #stats {
    position: fixed; top: 20px; left: 20px; z-index: 10;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 10px 14px;
    font-size: 11px; line-height: 1.6;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
  /* Responsive */
  @media (max-width: 768px) {
    #controls { padding: 8px 12px; gap: 8px; }
    #time-slider { width: 120px; }
    #legend { top: auto; bottom: 100px; right: 8px; font-size: 10px; padding: 8px 10px; }
    #stats { font-size: 10px; padding: 6px 10px; top: 8px; left: 8px; }
  }
  @media (max-width: 480px) {
    #controls { flex-direction: column; gap: 4px; padding: 8px; }
    #time-slider { width: 100%; }
    #legend { display: none; }
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="loading-overlay">
  <div class="spinner"></div>
  <div class="label">Building terrain...</div>
</div>
<div id="error-overlay">
  <div class="icon">&#9888;</div>
  <div class="msg"></div>
  <button class="retry" onclick="location.reload()">Retry</button>
</div>
<div id="empty-state">
  <div class="icon">&#127758;</div>
  <div class="title">No data loaded</div>
  <div class="subtitle">Connect a data source or upload a dataset to generate the 3D terrain.</div>
</div>
<div id="stats">
  <div>Draw calls: <span id="stat-draws">0</span></div>
  <div>Vertices: <span id="stat-verts">0</span></div>
  <div>Particles: <span id="stat-particles">0</span></div>
  <div>FPS: <span id="stat-fps">0</span></div>
</div>
<div id="legend">
  <div style="font-weight:600;margin-bottom:6px;">Legend</div>
  <div class="row"><div class="swatch" style="background:#3fb950;"></div> Revenue (height)</div>
  <div class="row"><div class="swatch" style="background:#ff7b72;"></div> Error rivers</div>
  <div class="row"><div class="swatch" style="background:#79c0ff;"></div> API call trails</div>
  <div class="row"><div class="swatch" style="background:linear-gradient(to right,#1a3a2a,#3fb950,#f0e68c);"></div> User density (color)</div>
</div>
<div id="controls">
  <button id="btn-bookmark-1" title="Overview">Overview</button>
  <button id="btn-bookmark-2" title="Revenue peaks">Peaks</button>
  <button id="btn-bookmark-3" title="Error hotspot">Errors</button>
  <button id="btn-auto-rotate">Auto-Rotate</button>
  <label for="time-slider">Time:</label>
  <input type="range" id="time-slider" min="0" max="9" value="0" step="1">
  <span id="time-label">Day 1</span>
  <button id="btn-reset">Reset View</button>
</div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
/*
  Data Contract
  Input format: Array of time slices, each containing:
    timeSlice: {
      label: string,
      grid: number[][]         // [rows][cols] — primary metric (revenue) mapped to elevation
      userDensity: number[][]  // [rows][cols] — secondary metric mapped to vertex color
      errors: [ { fromRow, fromCol, toRow, toCol, magnitude: number } ]
      apiCalls: [ { fromRow, fromCol, toRow, toCol, count: number } ]
    }
  Grid size: configurable, default 60x60
  Vertex budget: gridW * gridH vertices for terrain, per-slice cached
  Draw call budget: 1 terrain mesh + 1 river line segments + 1 particle system = 3 draw calls
  Particle update: throttled to only run when timeIndex changes or every 3rd frame
*/
const GRID_W = 60;
const GRID_H = 60;
const TIME_SLICES = 10;
const PARTICLE_COUNT = 2000;
const TERRAIN_SCALE_XZ = 0.4;
const TERRAIN_SCALE_Y = 8.0;
const PARTICLE_SPEED = 0.015;
const THROTTLE_FRAMES = 3;
function generateSyntheticData() {
  const slices = [];
  for (let t = 0; t < TIME_SLICES; t++) {
    const grid = [];
    const userDensity = [];
    const errors = [];
    const apiCalls = [];
    const phase = (t / TIME_SLICES) * Math.PI * 2;
    const trend = 1 + t * 0.08;
    for (let r = 0; r < GRID_H; r++) {
      const row = [];
      const dRow = [];
      const yr = (r / GRID_H - 0.5) * 2;
      for (let c = 0; c < GRID_W; c++) {
        const xr = (c / GRID_W - 0.5) * 2;
        const dist = Math.sqrt(yr*yr + xr*xr);
        const hill1 = Math.exp(-dist * 3) * 1.2;
        const hill2 = Math.exp(-((yr-0.4)*(yr-0.4)+(xr+0.3)*(xr+0.3))*6) * 0.9;
        const wave = Math.sin(xr*3 + phase) * Math.cos(yr*2.5 - phase*0.7) * 0.3;
        const noise = Math.sin(yr*11 + xr*7 + t*0.5) * Math.cos(xr*9 - yr*5 + t*0.3) * 0.15;
        row.push(((hill1 + hill2 + wave + noise) * trend + 0.2).toFixed(4) * 1);
        dRow.push((0.2 + hill1*0.6 + hill2*0.3 + Math.abs(noise)*0.5).toFixed(4) * 1);
      }
      grid.push(row);
      userDensity.push(dRow);
    }
    const errCount = 3 + Math.floor(Math.sin(phase*2)*2);
    for (let i = 0; i < errCount; i++) {
      const fromRow = 10 + i*12 + Math.floor(Math.sin(phase + i)*8);
      const fromCol = 5 + i*15 + Math.floor(Math.cos(phase + i)*10);
      errors.push({
        fromRow: Math.max(0,Math.min(GRID_H-1,fromRow)),
        fromCol: Math.max(0,Math.min(GRID_W-1,fromCol)),
        toRow: Math.max(0,Math.min(GRID_H-1,fromRow+4+Math.floor(Math.sin(phase)*6))),
        toCol: Math.max(0,Math.min(GRID_W-1,fromCol+6+Math.floor(Math.cos(phase)*8))),
        magnitude: (0.4 + Math.abs(Math.sin(phase + i))*0.6).toFixed(3)*1
      });
    }
    const callCount = 15 + Math.floor((1+Math.sin(phase*1.7))*10);
    for (let i = 0; i < callCount; i++) {
      const fr = Math.floor(Math.random()*GRID_H);
      const fc = Math.floor(Math.random()*GRID_W/3);
      apiCalls.push({
        fromRow: fr, fromCol: fc,
        toRow: Math.floor(GRID_H*0.3 + Math.random()*GRID_H*0.4),
        toCol: Math.floor(GRID_W*0.5 + Math.random()*GRID_W*0.4),
        count: 1 + Math.floor(Math.random()*8)
      });
    }
    slices.push({
      label: `Day ${t+1}`,
      grid,
      userDensity,
      errors,
      apiCalls
    });
  }
  return slices;
}
let dataSlices;
try {
  dataSlices = generateSyntheticData();
  if (!dataSlices || dataSlices.length === 0) {
    document.getElementById('empty-state').classList.add('visible');
    document.getElementById('loading-overlay').classList.add('hidden');
    throw new Error('No data slices generated');
  }
} catch(e) {
  document.getElementById('error-overlay').querySelector('.msg').textContent =
    'Data generation failed: ' + e.message;
  document.getElementById('error-overlay').classList.add('visible');
  document.getElementById('loading-overlay').classList.add('hidden');
  throw e;
}
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d1117);
scene.fog = new THREE.Fog(0x0d1117, 35, 80);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth/container.clientHeight, 0.5, 200);
camera.position.set(18, 12, 20);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 0, 0);
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.55;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.3;
controls.update();
const ambientLight = new THREE.AmbientLight(0x404060, 1.8);
scene.add(ambientLight);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(20, 25, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 100;
sun.shadow.camera.left = -25;
sun.shadow.camera.right = 25;
sun.shadow.camera.top = 25;
sun.shadow.camera.bottom = -25;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x8899cc, 0.8);
fill.position.set(-10, 5, -8);
scene.add(fill);
const groundGeo = new THREE.PlaneGeometry(60, 60);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x1a2332, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI/2;
ground.position.y = -0.3;
ground.receiveShadow = true;
scene.add(ground);
const gridHelper = new THREE.PolarGridHelper(28, 48, 24, 256, 0x2a3a4a, 0x1a2a3a);
gridHelper.position.y = -0.28;
scene.add(gridHelper);
const colorLow = new THREE.Color('#1a3a2a');
const colorMid = new THREE.Color('#3fb950');
const colorHigh = new THREE.Color('#f0e68c');
function buildTerrainGeometry(slice) {
  const { grid, userDensity } = slice;
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array((GRID_W+1) * (GRID_H+1) * 3);
  const colors = new Float32Array((GRID_W+1) * (GRID_H+1) * 3);
  const indices = [];
  for (let r = 0; r <= GRID_H; r++) {
    for (let c = 0; c <= GRID_W; c++) {
      const i = r * (GRID_W+1) + c;
      const x = (c - GRID_W/2) * TERRAIN_SCALE_XZ;
      const z = (r - GRID_H/2) * TERRAIN_SCALE_XZ;
      const gr = Math.min(r, GRID_H-1);
      const gc = Math.min(c, GRID_W-1);
      const height = grid[gr][gc] * TERRAIN_SCALE_Y;
      positions[i*3] = x;
      positions[i*3+1] = height;
      positions[i*3+2] = z;
      const d = userDensity[gr][gc];
      let col;
      if (d < 0.4) col = colorLow.clone().lerp(colorMid, d/0.4);
      else col = colorMid.clone().lerp(colorHigh, (d-0.4)/0.6);
      colors[i*3] = col.r;
      colors[i*3+1] = col.g;
      colors[i*3+2] = col.b;
    }
  }
  for (let r = 0; r < GRID_H; r++) {
    for (let c = 0; c < GRID_W; c++) {
      const a = r * (GRID_W+1) + c;
      const b = a + 1;
      const d = (r+1) * (GRID_W+1) + c;
      const e = d + 1;
      indices.push(a, b, d);
      indices.push(b, e, d);
    }
  }
  geo.setIndex(indices);
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  return geo;
}
const geometryCache = new Array(TIME_SLICES);
for (let t = 0; t < TIME_SLICES; t++) {
  geometryCache[t] = buildTerrainGeometry(dataSlices[t]);
}
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.1,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(geometryCache[0], terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
let riverLines = new THREE.Group();
scene.add(riverLines);
function buildRivers(slice) {
  while (riverLines.children.length) riverLines.remove(riverLines.children[0]);
  const { errors, grid } = slice;
  const material = new THREE.MeshBasicMaterial({ color: 0xff7b72 });
  errors.forEach(err => {
    const fr = err.fromRow, fc = err.fromCol, tr = err.toRow, tc = err.toCol;
    const h1 = grid[fr][fc] * TERRAIN_SCALE_Y;
    const h2 = grid[tr][tc] * TERRAIN_SCALE_Y;
    const x1 = (fc - GRID_W/2) * TERRAIN_SCALE_XZ;
    const z1 = (fr - GRID_H/2) * TERRAIN_SCALE_XZ;
    const x2 = (tc - GRID_W/2) * TERRAIN_SCALE_XZ;
    const z2 = (tr - GRID_H/2) * TERRAIN_SCALE_XZ;
    const dir = new THREE.Vector3(x2-x1, h2-h1, z2-z1);
    const len = dir.length();
    const mid = new THREE.Vector3((x1+x2)/2, (h1+h2)/2+0.15, (z1+z2)/2);
    const geo = new THREE.CylinderGeometry(0.06*err.magnitude, 0.06*err.magnitude, len, 6);
    const mesh = new THREE.Mesh(geo, material);
    mesh.position.copy(mid);
    const up = new THREE.Vector3(0,1,0);
    const quat = new THREE.Quaternion().setFromUnitVectors(up, dir.normalize());
    mesh.setRotationFromQuaternion(quat);
    mesh.renderOrder = 1;
    mesh.material.depthTest = true;
    mesh.material.depthWrite = true;
    riverLines.add(mesh);
    const glowGeo = new THREE.SphereGeometry(0.15*err.magnitude, 8, 8);
    const glowMat = new THREE.MeshBasicMaterial({ color: 0xff4444, transparent: true, opacity: 0.6 });
    const glow = new THREE.Mesh(glowGeo, glowMat);
    glow.position.set(x1, h1+0.2, z1);
    glow.renderOrder = 2;
    riverLines.add(glow);
    const glow2 = new THREE.Mesh(glowGeo, glowMat);
    glow2.position.set(x2, h2+0.2, z2);
    glow2.renderOrder = 2;
    riverLines.add(glow2);
  });
}
buildRivers(dataSlices[0]);
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColorsArr = new Float32Array(PARTICLE_COUNT * 3);
const particleData = new Array(PARTICLE_COUNT);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColorsArr, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.18,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.75,
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 3;
scene.add(particles);
function initParticles(slice) {
  const { grid, apiCalls } = slice;
  const calls = apiCalls.length > 0 ? apiCalls : [{ fromRow:0, fromCol:0, toRow:GRID_H-1, toCol:GRID_W-1, count:1 }];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const call = calls[i % calls.length];
    const t = i / PARTICLE_COUNT;
    const fr = call.fromRow + (call.toRow - call.fromRow) * t;
    const fc = call.fromCol + (call.toCol - call.fromCol) * t;
    const gr = Math.round(Math.max(0, Math.min(GRID_H-1, fr)));
    const gc = Math.round(Math.max(0, Math.min(GRID_W-1, fc)));
    const h = grid[gr][gc] * TERRAIN_SCALE_Y;
    particlePositions[i*3] = (fc - GRID_W/2) * TERRAIN_SCALE_XZ;
    particlePositions[i*3+1] = h + 0.3 + Math.random()*0.6;
    particlePositions[i*3+2] = (fr - GRID_H/2) * TERRAIN_SCALE_XZ;
    particleColorsArr[i*3] = 0.3;
    particleColorsArr[i*3+1] = 0.55 + Math.random()*0.2;
    particleColorsArr[i*3+2] = 0.9 + Math.random()*0.1;
    particleData[i] = {
      callIndex: i % calls.length,
      progress: Math.random(),
      speed: (PARTICLE_SPEED * (0.5 + Math.random())),
      offsetY: Math.random() * 0.5
    };
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
initParticles(dataSlices[0]);
let currentTimeIndex = 0;
let prevTimeIndex = -1;
let frameCount = 0;
function updateTerrainForTime(t) {
  terrainMesh.geometry = geometryCache[t];
  buildRivers(dataSlices[t]);
  initParticles(dataSlices[t]);
}
document.getElementById('time-slider').addEventListener('input', (e) => {
  const t = parseInt(e.target.value);
  document.getElementById('time-label').textContent = dataSlices[t].label;
  currentTimeIndex = t;
});
document.getElementById('btn-auto-rotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
const bookmarks = {
  1: { pos: new THREE.Vector3(18,12,20), target: new THREE.Vector3(0,0,0), label:'Overview' },
  2: { pos: new THREE.Vector3(5,14,8), target: new THREE.Vector3(2,5,-1), label:'Revenue Peaks' },
  3: { pos: new THREE.Vector3(-3,4,-12), target: new THREE.Vector3(5,0,8), label:'Error Hotspot' },
};
Object.entries(bookmarks).forEach(([key, bm]) => {
  document.getElementById(`btn-bookmark-${key}`).addEventListener('click', () => {
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const startTime = performance.now();
    const duration = 800;
    function anim(now) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed/duration, 1.0);
      const ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
      camera.position.lerpVectors(startPos, bm.pos, ease);
      controls.target.lerpVectors(startTarget, bm.target, ease);
      controls.update();
      if (t < 1) requestAnimationFrame(anim);
    }
    requestAnimationFrame(anim);
  });
});
document.getElementById('btn-reset').addEventListener('click', () => {
  const bm = bookmarks[1];
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  const duration = 600;
  function anim(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed/duration, 1.0);
    const ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
    camera.position.lerpVectors(startPos, bm.pos, ease);
    controls.target.lerpVectors(startTarget, bm.target, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
});
let fpsFrames = 0;
let fpsTime = performance.now();
function updateFPS(now) {
  fpsFrames++;
  if (now - fpsTime >= 1000) {
    document.getElementById('stat-fps').textContent = fpsFrames;
    fpsFrames = 0;
    fpsTime = now;
  }
}
function updateParticles(slice) {
  const { grid, apiCalls } = slice;
  const calls = apiCalls.length > 0 ? apiCalls : [{ fromRow:0, fromCol:0, toRow:GRID_H-1, toCol:GRID_W-1, count:1 }];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pd = particleData[i];
    pd.progress += pd.speed;
    if (pd.progress > 1.0) { pd.progress -= 1.0; pd.callIndex = (pd.callIndex+1) % calls.length; }
    const call = calls[pd.callIndex % calls.length];
    const t = pd.progress;
    const fr = call.fromRow + (call.toRow - call.fromRow) * t;
    const fc = call.fromCol + (call.toCol - call.fromCol) * t;
    const gr = Math.round(Math.max(0, Math.min(GRID_H-1, fr)));
    const gc = Math.round(Math.max(0, Math.min(GRID_W-1, fc)));
    const h = grid[gr][gc] * TERRAIN_SCALE_Y;
    particlePositions[i*3] = (fc - GRID_W/2) * TERRAIN_SCALE_XZ;
    particlePositions[i*3+1] = h + 0.3 + pd.offsetY;
    particlePositions[i*3+2] = (fr - GRID_H/2) * TERRAIN_SCALE_XZ;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  updateFPS(timestamp);
  if (currentTimeIndex !== prevTimeIndex) {
    updateTerrainForTime(currentTimeIndex);
    prevTimeIndex = currentTimeIndex;
    document.getElementById('stat-verts').textContent =
      ((GRID_W+1)*(GRID_H+1)).toLocaleString();
  }
  if (frameCount % THROTTLE_FRAMES === 0) {
    updateParticles(dataSlices[currentTimeIndex]);
  }
  frameCount++;
  renderer.render(scene, camera);
  document.getElementById('stat-draws').textContent =
    (1 + riverLines.children.length + 1).toString();
  document.getElementById('stat-particles').textContent = PARTICLE_COUNT.toLocaleString();
}
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
document.getElementById('stat-verts').textContent =
  ((GRID_W+1)*(GRID_H+1)).toLocaleString();
document.getElementById('loading-overlay').classList.add('hidden');
requestAnimationFrame(animate);
</script>
</body>
</html>
```