<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; }
  #canvas-container { position: fixed; inset: 0; z-index: 0; }
  canvas { display: block; }
  #ui-overlay { position: fixed; inset: 0; z-index: 10; pointer-events: none; }
  #ui-overlay > * { pointer-events: auto; }
  #top-bar {
    position: absolute; top: 16px; left: 50%; transform: translateX(-50%);
    display: flex; gap: 8px; align-items: center;
    background: rgba(10,10,20,0.85); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;
    padding: 8px 16px;
  }
  #top-bar button, #top-bar label {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
    color: #c8c8d8; padding: 6px 14px; border-radius: 8px; cursor: pointer;
    font-size: 13px; transition: all 0.15s; white-space: nowrap;
  }
  #top-bar button:hover { background: rgba(255,255,255,0.14); color: #fff; }
  #top-bar button.active { background: #2a5a8a; border-color: #3a7aba; color: #fff; }
  #step-display { color: #88aacc; font-size: 13px; min-width: 80px; text-align: center; font-variant-numeric: tabular-nums; }
  #bottom-bar {
    position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%);
    display: flex; gap: 10px; align-items: center;
    background: rgba(10,10,20,0.85); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;
    padding: 8px 20px;
  }
  #time-slider {
    -webkit-appearance: none; appearance: none; width: 320px; height: 6px;
    background: linear-gradient(to right, #1a3a5a, #3a7aba); border-radius: 3px; outline: none; cursor: pointer;
  }
  #time-slider::-webkit-slider-thumb {
    -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%;
    background: #6ab0e8; border: 2px solid #fff; cursor: pointer;
  }
  #time-label { color: #88aacc; font-size: 13px; min-width: 60px; text-align: center; font-variant-numeric: tabular-nums; }
  #bookmark-bar {
    position: absolute; right: 16px; top: 50%; transform: translateY(-50%);
    display: flex; flex-direction: column; gap: 6px;
    background: rgba(10,10,20,0.85); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;
    padding: 10px;
  }
  #bookmark-bar button {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
    color: #c8c8d8; padding: 5px 12px; border-radius: 6px; cursor: pointer;
    font-size: 11px; transition: all 0.15s;
  }
  #bookmark-bar button:hover { background: rgba(255,255,255,0.14); color: #fff; }
  #bookmark-bar .bm-label { color: #667; font-size: 10px; text-align: center; margin: 2px 0 -2px; }
  #legend {
    position: absolute; left: 16px; bottom: 120px;
    background: rgba(10,10,20,0.85); backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08); border-radius: 12px;
    padding: 14px; color: #99aabb; font-size: 12px; line-height: 1.6;
    display: flex; flex-direction: column; gap: 4px;
  }
  #legend .swatch { display: inline-block; width: 12px; height: 12px; border-radius: 3px; margin-right: 6px; vertical-align: middle; }
  #legend .swatch.elevation { background: linear-gradient(to top, #1a3a2a, #5aaa40, #d4c040, #c08030, #884020); }
  #legend .swatch.river { background: #ff3040; }
  #legend .swatch.particle { background: #40c0ff; }
  #legend .title { color: #aabbcc; font-weight: 600; margin-bottom: 2px; font-size: 13px; }
  #tooltip {
    position: absolute; display: none; background: rgba(10,10,20,0.9); border: 1px solid rgba(255,255,255,0.15);
    border-radius: 8px; padding: 8px 12px; color: #ccd; font-size: 12px; pointer-events: none;
  }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-overlay">
  <div id="top-bar">
    <button id="btn-play" title="Play/Pause time animation">&#9654; Play</button>
    <button id="btn-prev" title="Previous step">&#9664;</button>
    <span id="step-display">Day 1 / 30</span>
    <button id="btn-next" title="Next step">&#9654;</button>
    <button id="btn-auto-rotate" title="Auto-rotate camera">&#8635; Rotate</button>
    <button id="btn-reset-cam" title="Reset camera">Reset</button>
  </div>
  <div id="bookmark-bar">
    <span class="bm-label">BOOKMARKS</span>
    <button id="bm-save-1">Save 1</button><button id="bm-load-1">Load 1</button>
    <button id="bm-save-2">Save 2</button><button id="bm-load-2">Load 2</button>
    <button id="bm-save-3">Save 3</button><button id="bm-load-3">Load 3</button>
  </div>
  <div id="legend">
    <span class="title">LEGEND</span>
    <span><span class="swatch elevation"></span> Elevation = Revenue</span>
    <span><span class="swatch river"></span> Rivers = Error Rate &gt;70%</span>
    <span><span class="swatch particle"></span> Particles = API Calls</span>
  </div>
  <div id="bottom-bar">
    <span id="time-label">Day 1</span>
    <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
    <span id="time-end-label">Day 30</span>
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
// ── Constants ──────────────────────────────────────────────
const GRID = 80;
const TIME_STEPS = 30;
const TERRAIN_SIZE = 60;
const HEIGHT_SCALE = 10;
const PARTICLE_COUNT = 300;
const RIVER_THRESHOLD = 0.7;
const RIVER_Y_OFFSET = 0.25;
// ── DOM refs (all wired) ──────────────────────────────────
const container = document.getElementById('canvas-container');
const btnPlay = document.getElementById('btn-play');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const btnAutoRotate = document.getElementById('btn-auto-rotate');
const btnResetCam = document.getElementById('btn-reset-cam');
const timeSlider = document.getElementById('time-slider');
const stepDisplay = document.getElementById('step-display');
const timeLabel = document.getElementById('time-label');
const tooltip = document.getElementById('tooltip');
// Bookmark buttons
const bmSave = [document.getElementById('bm-save-1'), document.getElementById('bm-save-2'), document.getElementById('bm-save-3')];
const bmLoad = [document.getElementById('bm-load-1'), document.getElementById('bm-load-2'), document.getElementById('bm-load-3')];
// ── State ──────────────────────────────────────────────────
let currentStep = 0;
let playing = false;
const bookmarks = [null, null, null]; // {pos, target}
// ── Three.js setup ─────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 40, 120);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 1, 200);
camera.position.set(35, 28, 45);
camera.lookAt(0, -2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
// OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, -2, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 10;
controls.maxDistance = 90;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// ── Lighting ───────────────────────────────────────────────
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(30, 40, 20);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 150;
sunLight.shadow.camera.left = -50;
sunLight.shadow.camera.right = 50;
sunLight.shadow.camera.top = 50;
sunLight.shadow.camera.bottom = -50;
sunLight.shadow.bias = -0.0003;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466aa, 1.2);
fillLight.position.set(-20, 5, -15);
scene.add(fillLight);
// Ground plane (receive shadows)
const groundGeo = new THREE.PlaneGeometry(120, 120);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x0a0a18, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -HEIGHT_SCALE - 2;
ground.receiveShadow = true;
scene.add(ground);
// Grid helper
const gridHelper = new THREE.GridHelper(TERRAIN_SIZE, 20, 0x1a2a3a, 0x0d1520);
gridHelper.position.y = -HEIGHT_SCALE - 1.9;
scene.add(gridHelper);
// ── Data generation ────────────────────────────────────────
// heightData[timeStep][row][col] = height value 0..1
// densityData[timeStep][row][col] = user density 0..1
// errorData[timeStep][row][col] = error rate 0..1
const heightData = [];
const densityData = [];
const errorData = [];
function gaussian(x, y, cx, cy, sx, sy) {
  const dx = (x - cx) / sx;
  const dy = (y - cy) / sy;
  return Math.exp(-0.5 * (dx * dx + dy * dy));
}
for (let t = 0; t < TIME_STEPS; t++) {
  const phase = t / TIME_STEPS;
  const hGrid = [];
  const dGrid = [];
  const eGrid = [];
  for (let row = 0; row < GRID; row++) {
    const hRow = [];
    const dRow = [];
    const eRow = [];
    const y = (row / (GRID - 1)) * 2 - 1; // -1..1
    for (let col = 0; col < GRID; col++) {
      const x = (col / (GRID - 1)) * 2 - 1;
      // Revenue terrain: multi-peak landscape that shifts over time
      let h = 0;
      h += 0.7 * gaussian(x, y, -0.4, -0.3, 0.7, 0.6);
      h += 0.9 * gaussian(x, y, 0.3 + 0.15 * Math.sin(phase * Math.PI * 2), 0.2 + 0.1 * Math.cos(phase * Math.PI * 2.5), 0.5, 0.55);
      h += 0.5 * gaussian(x, y, 0.5 * Math.cos(phase * Math.PI * 1.3), -0.5, 0.4, 0.45);
      h += 0.35 * gaussian(x, y, -0.6, 0.4 + 0.2 * Math.sin(phase * Math.PI * 3), 0.35, 0.3);
      h += 0.2 * (Math.sin(x * 4 + phase * 3) * Math.cos(y * 3 + phase * 2)) * 0.15; // ripple
      h = Math.max(0, Math.min(1, h));
      // User density: correlated with revenue, with noise
      let d = h * 0.7 + 0.15 * Math.sin(x * 6 + phase) * Math.cos(y * 5 - phase) + 0.15;
      d = Math.max(0, Math.min(1, d));
      // Error rate: inverse correlation with density, spikes in valleys
      let e = (1 - d) * 0.65 + 0.08;
      // Error hotspots that move
      e += 0.25 * gaussian(x, y, -0.5 + 0.3 * Math.cos(phase * Math.PI * 2), 0.3 * Math.sin(phase * Math.PI * 1.7), 0.25, 0.2);
      e += 0.2 * gaussian(x, y, 0.4, -0.4 + 0.2 * Math.sin(phase * Math.PI * 3), 0.18, 0.22);
      e = Math.max(0, Math.min(1, e));
      hRow.push(h);
      dRow.push(d);
      eRow.push(e);
    }
    hGrid.push(hRow);
    dGrid.push(dRow);
    eGrid.push(eRow);
  }
  heightData.push(hGrid);
  densityData.push(dGrid);
  errorData.push(eGrid);
}
// ── Terrain geometry precomputation ────────────────────────
// Cache all geometry variants upfront; swap buffers, never rebuild
const terrainGeometries = [];
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
});
for (let t = 0; t < TIME_STEPS; t++) {
  const geo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  const positions = geo.attributes.position.array;
  const colors = new Float32Array(positions.length);
  const hGrid = heightData[t];
  const dGrid = densityData[t];
  for (let i = 0; i < positions.length / 3; i++) {
    const col = i % GRID;
    const row = Math.floor(i / GRID);
    const h = hGrid[row][col];
    const d = dGrid[row][col];
    positions[i * 3 + 1] = h * HEIGHT_SCALE - HEIGHT_SCALE * 0.1;
    // Vegetation gradient: green (high density) -> brown (low density)
    const r = 0.12 + d * 0.25;
    const g = 0.18 + d * 0.62;
    const b = 0.08 + d * 0.12;
    colors[i * 3] = r;
    colors[i * 3 + 1] = g;
    colors[i * 3 + 2] = b;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  terrainGeometries.push(geo);
}
const terrainMesh = new THREE.Mesh(terrainGeometries[0], terrainMaterial);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ── River geometry precomputation ──────────────────────────
// Find connected high-error cells; draw line segments between adjacent river cells
// Precomputed once per time step, stored as BufferGeometry
const riverMeshes = [];
const riverMaterial = new THREE.MeshBasicMaterial({ color: 0xff2030, side: THREE.DoubleSide, transparent: true, opacity: 0.85 });
function buildRiverGeometry(t) {
  const eGrid = errorData[t];
  const hGrid = heightData[t];
  const cellSize = TERRAIN_SIZE / (GRID - 1);
  const halfTerrain = TERRAIN_SIZE / 2;
  // Find river cells
  const isRiver = [];
  for (let row = 0; row < GRID; row++) {
    isRiver[row] = [];
    for (let col = 0; col < GRID; col++) {
      isRiver[row][col] = eGrid[row][col] > RIVER_THRESHOLD;
    }
  }
  // Build line segments between adjacent river cells
  const vertices = [];
  for (let row = 0; row < GRID; row++) {
    for (let col = 0; col < GRID; col++) {
      if (!isRiver[row][col]) continue;
      const x1 = col * cellSize - halfTerrain;
      const z1 = row * cellSize - halfTerrain;
      const y1 = hGrid[row][col] * HEIGHT_SCALE - HEIGHT_SCALE * 0.1 + RIVER_Y_OFFSET;
      // Right neighbor
      if (col + 1 < GRID && isRiver[row][col + 1]) {
        const x2 = (col + 1) * cellSize - halfTerrain;
        const z2 = row * cellSize - halfTerrain;
        const y2 = hGrid[row][col + 1] * HEIGHT_SCALE - HEIGHT_SCALE * 0.1 + RIVER_Y_OFFSET;
        vertices.push(x1, y1, z1, x2, y2, z2);
      }
      // Down neighbor
      if (row + 1 < GRID && isRiver[row + 1][col]) {
        const x2 = col * cellSize - halfTerrain;
        const z2 = (row + 1) * cellSize - halfTerrain;
        const y2 = hGrid[row + 1][col] * HEIGHT_SCALE - HEIGHT_SCALE * 0.1 + RIVER_Y_OFFSET;
        vertices.push(x1, y1, z1, x2, y2, z2);
      }
    }
  }
  if (vertices.length === 0) {
    // Return empty geometry
    const emptyGeo = new THREE.BufferGeometry();
    emptyGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(0), 3));
    return emptyGeo;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(vertices), 3));
  return geo;
}
// River group with line rendering (use thin box meshes for reliable width)
for (let t = 0; t < TIME_STEPS; t++) {
  const geo = buildRiverGeometry(t);
  const lineSegments = new THREE.LineSegments(
    geo,
    new THREE.LineBasicMaterial({ color: 0xff3040, linewidth: 1, transparent: true, opacity: 0.8, depthTest: true })
  );
  lineSegments.renderOrder = 1;
  lineSegments.material.depthTest = true;
  lineSegments.material.depthWrite = false;
  lineSegments.visible = (t === 0);
  scene.add(lineSegments);
  riverMeshes.push(lineSegments);
}
// ── Particle system ────────────────────────────────────────
// Reusable BufferGeometry with pre-allocated position array
const particleCount = PARTICLE_COUNT;
const particlePositions = new Float32Array(particleCount * 3);
const particleColors = new Float32Array(particleCount * 3);
const particleData = []; // { x, z, vx, vz, life, maxLife }
const halfTerrain = TERRAIN_SIZE / 2;
const cellSize = TERRAIN_SIZE / (GRID - 1);
function sampleTerrainHeight(x, z) {
  // Bilinear sample from current height data
  const col_f = (x + halfTerrain) / cellSize;
  const row_f = (z + halfTerrain) / cellSize;
  const col0 = Math.max(0, Math.min(GRID - 2, Math.floor(col_f)));
  const row0 = Math.max(0, Math.min(GRID - 2, Math.floor(row_f)));
  const col1 = col0 + 1;
  const row1 = row0 + 1;
  const fx = col_f - col0;
  const fy = row_f - row0;
  const hGrid = heightData[currentStep];
  const h00 = hGrid[row0][col0];
  const h10 = hGrid[row0][col1];
  const h01 = hGrid[row1][col0];
  const h11 = hGrid[row1][col1];
  const h = (1 - fx) * (1 - fy) * h00 + fx * (1 - fy) * h10 + (1 - fx) * fy * h01 + fx * fy * h11;
  return h * HEIGHT_SCALE - HEIGHT_SCALE * 0.1;
}
for (let i = 0; i < particleCount; i++) {
  const x = (Math.random() - 0.5) * TERRAIN_SIZE * 0.9;
  const z = (Math.random() - 0.5) * TERRAIN_SIZE * 0.9;
  const y = sampleTerrainHeight(x, z) + 0.3;
  particlePositions[i * 3] = x;
  particlePositions[i * 3 + 1] = y;
  particlePositions[i * 3 + 2] = z;
  particleColors[i * 3] = 0.25;
  particleColors[i * 3 + 1] = 0.65;
  particleColors[i * 3 + 2] = 1.0;
  particleData.push({
    x, z,
    vx: (Math.random() - 0.5) * 2,
    vz: (Math.random() - 0.5) * 2,
    life: Math.random() * 5,
    maxLife: 3 + Math.random() * 7,
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
  opacity: 0.7,
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 2;
scene.add(particles);
// ── Animation loop ─────────────────────────────────────────
const clock = new THREE.Clock();
let lastStepTime = 0;
const STEP_INTERVAL = 0.4; // seconds per time step when playing
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  // Auto-advance time when playing
  if (playing) {
    lastStepTime += dt;
    while (lastStepTime >= STEP_INTERVAL) {
      lastStepTime -= STEP_INTERVAL;
      const next = (currentStep + 1) % TIME_STEPS;
      setTimeStep(next);
    }
  }
  // Update particles — reuse position array, never allocate
  for (let i = 0; i < particleCount; i++) {
    const pd = particleData[i];
    pd.life += dt;
    if (pd.life > pd.maxLife) {
      // Respawn
      pd.x = (Math.random() - 0.5) * TERRAIN_SIZE * 0.85;
      pd.z = (Math.random() - 0.5) * TERRAIN_SIZE * 0.85;
      pd.vx = (Math.random() - 0.5) * 2.5;
      pd.vz = (Math.random() - 0.5) * 2.5;
      pd.life = 0;
      pd.maxLife = 3 + Math.random() * 7;
    }
    pd.x += pd.vx * dt;
    pd.z += pd.vz * dt;
    // Wrap at terrain edges
    if (Math.abs(pd.x) > halfTerrain * 0.92) pd.vx *= -1;
    if (Math.abs(pd.z) > halfTerrain * 0.92) pd.vz *= -1;
    const y = sampleTerrainHeight(pd.x, pd.z) + 0.3 + Math.sin(pd.life * 8) * 0.15;
    particlePositions[i * 3] = pd.x;
    particlePositions[i * 3 + 1] = y;
    particlePositions[i * 3 + 2] = pd.z;
    // Fade alpha via color brightness based on life
    const fade = 1 - (pd.life / pd.maxLife);
    particleColors[i * 3] = 0.2 + fade * 0.15;
    particleColors[i * 3 + 1] = 0.5 + fade * 0.3;
    particleColors[i * 3 + 2] = 0.8 + fade * 0.2;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  renderer.render(scene, camera);
}
// ── Time step switching (buffer swap, no rebuild) ──────────
function setTimeStep(step) {
  if (step === currentStep) return;
  currentStep = step;
  // Swap terrain geometry (precomputed buffer)
  terrainMesh.geometry = terrainGeometries[step];
  // Swap river visibility
  for (let t = 0; t < TIME_STEPS; t++) {
    riverMeshes[t].visible = (t === step);
  }
  // Update UI
  timeSlider.value = step;
  stepDisplay.textContent = `Day ${step + 1} / ${TIME_STEPS}`;
  timeLabel.textContent = `Day ${step + 1}`;
}
// ── Event handlers (all wired) ─────────────────────────────
btnPlay.addEventListener('click', () => {
  playing = !playing;
  btnPlay.textContent = playing ? '⏸ Pause' : '▶ Play';
  btnPlay.classList.toggle('active', playing);
  lastStepTime = 0;
});
btnPrev.addEventListener('click', () => {
  playing = false;
  btnPlay.textContent = '▶ Play';
  btnPlay.classList.remove('active');
  setTimeStep((currentStep - 1 + TIME_STEPS) % TIME_STEPS);
});
btnNext.addEventListener('click', () => {
  playing = false;
  btnPlay.textContent = '▶ Play';
  btnPlay.classList.remove('active');
  setTimeStep((currentStep + 1) % TIME_STEPS);
});
timeSlider.addEventListener('input', () => {
  playing = false;
  btnPlay.textContent = '▶ Play';
  btnPlay.classList.remove('active');
  setTimeStep(parseInt(timeSlider.value));
});
btnAutoRotate.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAutoRotate.classList.toggle('active', controls.autoRotate);
});
btnResetCam.addEventListener('click', () => {
  camera.position.set(35, 28, 45);
  controls.target.set(0, -2, 0);
  controls.update();
});
// Bookmark handlers
for (let i = 0; i < 3; i++) {
  bmSave[i].addEventListener('click', () => {
    bookmarks[i] = {
      pos: camera.position.clone(),
      target: controls.target.clone(),
    };
    bmSave[i].textContent = `Save ${i + 1} \u2713`;
    setTimeout(() => { bmSave[i].textContent = `Save ${i + 1}`; }, 600);
  });
  bmLoad[i].addEventListener('click', () => {
    const bm = bookmarks[i];
    if (!bm) return;
    // Animate to bookmark
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const endPos = bm.pos;
    const endTarget = bm.target;
    const startTime = performance.now();
    const duration = 800;
    function animStep(now) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1.0);
      // Ease in-out
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      camera.position.lerpVectors(startPos, endPos, ease);
      controls.target.lerpVectors(startTarget, endTarget, ease);
      controls.update();
      if (t < 1) {
        requestAnimationFrame(animStep);
      }
    }
    requestAnimationFrame(animStep);
    bmLoad[i].textContent = `Load ${i + 1} \u2192`;
    setTimeout(() => { bmLoad[i].textContent = `Load ${i + 1}`; }, 600);
  });
}
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case ' ':
      e.preventDefault();
      btnPlay.click();
      break;
    case 'arrowleft':
      btnPrev.click();
      break;
    case 'arrowright':
      btnNext.click();
      break;
    case 'r':
      if (!e.ctrlKey && !e.metaKey) {
        btnAutoRotate.click();
      }
      break;
    case '1':
      if (e.ctrlKey || e.metaKey) { e.preventDefault(); bmSave[0].click(); }
      else if (!e.ctrlKey && !e.metaKey) { bmLoad[0].click(); }
      break;
    case '2':
      if (e.ctrlKey || e.metaKey) { e.preventDefault(); bmSave[1].click(); }
      else if (!e.ctrlKey && !e.metaKey) { bmLoad[1].click(); }
      break;
    case '3':
      if (e.ctrlKey || e.metaKey) { e.preventDefault(); bmSave[2].click(); }
      else if (!e.ctrlKey && !e.metaKey) { bmLoad[2].click(); }
      break;
  }
});
// Resize handler
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// ── Start ──────────────────────────────────────────────────
setTimeStep(0);
animate();
</script>
</body>
</html>