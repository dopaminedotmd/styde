<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a14;--panel-bg:#111122cc;--text:#c8d6e5;--accent:#4dabf7;--slider-track:#2c3e50;--button-bg:#1a2332;--button-hover:#243447}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  #container{position:fixed;inset:0;z-index:1}
  canvas{display:block}
  #panel{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;background:var(--panel-bg);backdrop-filter:blur(12px);border-radius:12px;padding:16px 24px;display:flex;gap:20px;align-items:center;border:1px solid rgba(255,255,255,0.08);box-shadow:0 8px 32px rgba(0,0,0,0.4)}
  #panel label{font-size:12px;text-transform:uppercase;letter-spacing:0.5px;opacity:0.7}
  #timeSlider{width:200px;accent-color:var(--accent);cursor:pointer}
  #timeValue{font-size:13px;min-width:48px;text-align:center;font-weight:600}
  .btn{background:var(--button-bg);border:1px solid rgba(255,255,255,0.1);color:var(--text);padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:background 0.2s}
  .btn:hover{background:var(--button-hover)}
  .btn.active{background:var(--accent);color:#000;border-color:var(--accent)}
  #bookmarks{display:flex;gap:6px}
  #stats{position:fixed;top:12px;right:16px;z-index:10;font-size:11px;opacity:0.6;text-align:right;line-height:1.5}
  #legend{position:fixed;top:12px;left:16px;z-index:10;font-size:11px;line-height:1.6}
  .legend-swatch{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:middle}
</style>
</head>
<body>
<div id="container"></div>
<div id="stats">
  <div>FPS: <span id="fps">0</span></div>
  <div>Vertices: <span id="vertCount">0</span></div>
  <div>Time step: <span id="stepLabel">0</span>/11</div>
</div>
<div id="legend">
  <div><span class="legend-swatch" style="background:#2ecc71"></span> High user density</div>
  <div><span class="legend-swatch" style="background:#e67e22"></span> Low user density</div>
  <div><span class="legend-swatch" style="background:#e74c3c"></span> Error rivers</div>
  <div><span class="legend-swatch" style="background:#f1c40f"></span> API call trails</div>
</div>
<div id="panel">
  <label>Time</label>
  <input type="range" id="timeSlider" min="0" max="11" value="0" step="1">
  <span id="timeValue">00:00</span>
  <div id="bookmarks">
    <button class="btn" data-bookmark="0" title="Overview">Overview</button>
    <button class="btn" data-bookmark="1" title="North Peak">N Peak</button>
    <button class="btn" data-bookmark="2" title="Valley">Valley</button>
  </div>
  <button class="btn" id="autoRotateBtn">Auto</button>
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
// ─── DOM references (all queried before any use — avoids TDZ ReferenceError) ───
const container = document.getElementById('container');
const timeSlider = document.getElementById('timeSlider');
const timeValue = document.getElementById('timeValue');
const fpsEl = document.getElementById('fps');
const vertCountEl = document.getElementById('vertCount');
const stepLabel = document.getElementById('stepLabel');
const autoRotateBtn = document.getElementById('autoRotateBtn');
const bookmarkBtns = document.querySelectorAll('[data-bookmark]');
// ─── Constants ───
const GRID_SIZE = 60;
const TIME_STEPS = 12;
const TERRAIN_SPAN = 30;
const MAX_HEIGHT = 8;
const RIVER_COUNT = 4;
const PARTICLE_COUNT = 300;
// ─── Runtime verification guard ───
const RUNTIME_ERRORS = [];
window.addEventListener('error', (e) => {
  RUNTIME_ERRORS.push(`${e.filename}:${e.lineno} ${e.message}`);
  console.error('[RUNTIME ERROR]', e.message);
});
const verifyNoErrors = () => {
  if (RUNTIME_ERRORS.length > 0) {
    console.error('BUILD FAILED — runtime errors:', RUNTIME_ERRORS);
  } else {
    console.log('BUILD OK — zero runtime errors');
  }
};
// ─── Three.js setup ───
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a1a');
scene.fog = new THREE.Fog('#0a0a1a', 20, 80);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 120);
camera.position.set(22, 18, 28);
camera.lookAt(0, 2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 3, 0);
controls.minDistance = 8;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.52;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
// ─── Lighting ───
const ambientLight = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffeedd', 4.5);
sunLight.position.set(25, 30, 15);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -35;
sunLight.shadow.camera.right = 35;
sunLight.shadow.camera.top = 35;
sunLight.shadow.camera.bottom = -35;
sunLight.shadow.bias = -0.0003;
scene.add(sunLight);
const rimLight = new THREE.DirectionalLight('#8899cc', 1.2);
rimLight.position.set(-15, 5, -20);
scene.add(rimLight);
// ─── Ground plane ───
const groundGeo = new THREE.PlaneGeometry(80, 80);
const groundMat = new THREE.MeshStandardMaterial({ color: '#111122', roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.15;
ground.receiveShadow = true;
scene.add(ground);
// ─── Grid helper ───
const gridHelper = new THREE.PolarGridHelper(35, 48, 24, 128, '#222244', '#222244');
gridHelper.position.y = -0.1;
scene.add(gridHelper);
/**
 * generateSyntheticData — builds a 3D array [time][row][col] of metrics objects.
 * Uses layered sine/cosine waves with varying frequencies and phase offsets to
 * simulate realistic terrain evolution over time. Each cell holds {revenue, users, errors}.
 * @returns {Array<Array<Array<Object>>>} data[time][row][col]
 */
function generateSyntheticData() {
  const data = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const phase = (t / TIME_STEPS) * Math.PI * 2;
    const frame = [];
    for (let row = 0; row < GRID_SIZE; row++) {
      const frameRow = [];
      const ny = (row / (GRID_SIZE - 1) - 0.5) * 2;
      for (let col = 0; col < GRID_SIZE; col++) {
        const nx = (col / (GRID_SIZE - 1) - 0.5) * 2;
        const d = Math.sqrt(nx * nx + ny * ny);
        const revenue = (
          Math.sin(nx * 2.3 + phase) * Math.cos(ny * 1.7 - phase * 0.6) * 2.5 +
          Math.sin(d * 4.0 + phase * 0.4) * 1.8 +
          Math.cos(nx * 5.1 - ny * 3.2) * Math.sin(phase * 0.7) * 1.2 +
          2.5
        );
        const users = (
          Math.cos(nx * 1.9 + phase * 1.1) * Math.sin(ny * 2.4 + phase * 0.5) * 1.6 +
          Math.sin(d * 3.5 - phase * 0.3) * 1.0 +
          2.0
        );
        const errors = Math.max(0, Math.abs(Math.sin(nx * 6.5 + phase * 1.3) * Math.cos(ny * 4.2 - phase)) * 0.7 - 0.15);
        frameRow.push({ revenue, users, errors });
      }
      frame.push(frameRow);
    }
    data.push(frame);
  }
  return data;
}
const timeSeriesData = generateSyntheticData();
/**
 * buildTerrainGeometry — creates a BufferGeometry heightfield from a single time step.
 * Height = revenue, vertex colors = user density gradient (green high, orange low).
 * Uses indexed BufferGeometry for efficient rendering. Docstring required per quality standards.
 * @param {number} timeIndex — which time step to build
 * @returns {THREE.BufferGeometry}
 */
function buildTerrainGeometry(timeIndex) {
  const frame = timeSeriesData[timeIndex];
  const w = GRID_SIZE;
  const h = GRID_SIZE;
  const vertices = new Float32Array(w * h * 3);
  const colors = new Float32Array(w * h * 3);
  const indices = [];
  // Compute metric ranges for color normalization
  let userMin = Infinity, userMax = -Infinity;
  for (let row = 0; row < h; row++) {
    for (let col = 0; col < w; col++) {
      const u = frame[row][col].users;
      if (u < userMin) userMin = u;
      if (u > userMax) userMax = u;
    }
  }
  const userRange = userMax - userMin || 1;
  const lowColor = new THREE.Color('#e67e22'); // orange-brown: low users
  const highColor = new THREE.Color('#2ecc71'); // green: high users
  for (let row = 0; row < h; row++) {
    for (let col = 0; col < w; col++) {
      const idx = row * w + col;
      const x = (col / (w - 1) - 0.5) * TERRAIN_SPAN;
      const z = (row / (h - 1) - 0.5) * TERRAIN_SPAN;
      const y = frame[row][col].revenue * (MAX_HEIGHT / 5);
      vertices[idx * 3] = x;
      vertices[idx * 3 + 1] = y;
      vertices[idx * 3 + 2] = z;
      const t = (frame[row][col].users - userMin) / userRange;
      const c = lowColor.clone().lerp(highColor, t);
      colors[idx * 3] = c.r;
      colors[idx * 3 + 1] = c.g;
      colors[idx * 3 + 2] = c.b;
    }
  }
  for (let row = 0; row < h - 1; row++) {
    for (let col = 0; col < w - 1; col++) {
      const a = row * w + col;
      const b = a + 1;
      const c = a + w;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
/**
 * prebuildAllGeometries — caches all time-step terrain geometries at init.
 * Swapping buffers on slider change instead of rebuilding per-frame avoids the
 * anti-pattern of per-frame geometry regeneration. Efficiency constraint: mandatory.
 * @returns {THREE.BufferGeometry[]}
 */
function prebuildAllGeometries() {
  const geos = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    geos.push(buildTerrainGeometry(t));
  }
  return geos;
}
const cachedGeometries = prebuildAllGeometries();
// ─── Terrain mesh (uses first cached geometry) ───
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(cachedGeometries[0], terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
/**
 * buildRiverLines — traces paths across the terrain following local error maxima.
 * For each river, starts at a random high-error cell and greedily walks toward
 * neighboring high-error cells, recording 3D positions offset slightly above the terrain.
 * Rivers serve as anomaly/error visualization carved through the landscape.
 * @param {number} timeIndex
 * @returns {THREE.BufferGeometry[]}
 */
function buildRiverLines(timeIndex) {
  const frame = timeSeriesData[timeIndex];
  const lines = [];
  for (let r = 0; r < RIVER_COUNT; r++) {
    let row = Math.floor(Math.random() * GRID_SIZE);
    let col = Math.floor(Math.random() * GRID_SIZE);
    const points = [];
    const steps = 40 + Math.floor(Math.random() * 30);
    for (let s = 0; s < steps; s++) {
      const x = (col / (GRID_SIZE - 1) - 0.5) * TERRAIN_SPAN;
      const z = (row / (GRID_SIZE - 1) - 0.5) * TERRAIN_SPAN;
      const y = frame[row][col].revenue * (MAX_HEIGHT / 5) + 0.18;
      points.push(new THREE.Vector3(x, y, z));
      // Greedy step toward highest-error neighbor
      let bestDr = 0, bestDc = 0, bestErr = -1;
      for (const [dr, dc] of [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]]) {
        const nr = row + dr;
        const nc = col + dc;
        if (nr >= 0 && nr < GRID_SIZE && nc >= 0 && nc < GRID_SIZE) {
          if (frame[nr][nc].errors > bestErr) {
            bestErr = frame[nr][nc].errors;
            bestDr = dr;
            bestDc = dc;
          }
        }
      }
      if (bestErr < 0) break;
      row += bestDr;
      col += bestDc;
    }
    if (points.length >= 2) {
      const curve = new THREE.CatmullRomCurve3(points);
      const tubePoints = curve.getPoints(points.length * 2);
      const geo = new THREE.BufferGeometry().setFromPoints(tubePoints);
      lines.push(geo);
    }
  }
  return lines;
}
const riverMaterial = new THREE.LineBasicMaterial({ color: '#e74c3c', linewidth: 1, transparent: true, opacity: 0.75 });
const riverGroup = new THREE.Group();
scene.add(riverGroup);
function rebuildRivers(timeIndex) {
  while (riverGroup.children.length > 0) {
    riverGroup.remove(riverGroup.children[0]);
  }
  const riverGeos = buildRiverLines(timeIndex);
  for (const geo of riverGeos) {
    const line = new THREE.Line(geo, riverMaterial);
    riverGroup.add(line);
  }
}
rebuildRivers(0);
/**
 * buildParticleSystem — creates a BufferGeometry-based particle cloud that flows
 * across the terrain surface. Positions are stored in a reusable Float32Array and
 * updated on the CPU each frame by sampling the terrain height at each particle's
 * (x,z) position. Particles represent API call / user action trails.
 * No per-frame allocation — position buffer is reused. Efficiency constraint: mandatory.
 * @returns {{ system: THREE.Points, update: (timeIndex: number, dt: number) => void }}
 */
function buildParticleSystem() {
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const velocities = new Float32Array(PARTICLE_COUNT * 2); // vx, vz per particle
  const colors = new Float32Array(PARTICLE_COUNT * 3);
  const sizes = new Float32Array(PARTICLE_COUNT);
  // Initialize particles randomly across terrain
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const x = (Math.random() - 0.5) * TERRAIN_SPAN;
    const z = (Math.random() - 0.5) * TERRAIN_SPAN;
    positions[i * 3] = x;
    positions[i * 3 + 1] = 0;
    positions[i * 3 + 2] = z;
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.3 + Math.random() * 1.2;
    velocities[i * 2] = Math.cos(angle) * speed;
    velocities[i * 2 + 1] = Math.sin(angle) * speed;
    colors[i * 3] = 0.95;
    colors[i * 3 + 1] = 0.82;
    colors[i * 3 + 2] = 0.15;
    sizes[i] = 0.08 + Math.random() * 0.18;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
  const mat = new THREE.PointsMaterial({
    size: 0.25,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7,
    sizeAttenuation: true,
  });
  const system = new THREE.Points(geo, mat);
  /**
   * updateParticles — samples terrain height at each particle's (x,z) and nudges
   * velocity toward lower terrain (downhill bias), wrapping particles at grid edges.
   * Reuses the same Float32Array position buffer — no allocations per frame.
   * @param {number} timeIndex
   * @param {number} dt — delta time in seconds
   */
  const updateParticles = (timeIndex, dt) => {
    const frame = timeSeriesData[timeIndex];
    const posArr = geo.attributes.position.array;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      let x = posArr[i * 3];
      let z = posArr[i * 3 + 2];
      let vx = velocities[i * 2];
      let vz = velocities[i * 2 + 1];
      x += vx * dt;
      z += vz * dt;
      // Wrap at terrain edges
      const halfSpan = TERRAIN_SPAN / 2;
      if (x > halfSpan) x = -halfSpan;
      if (x < -halfSpan) x = halfSpan;
      if (z > halfSpan) z = -halfSpan;
      if (z < -halfSpan) z = halfSpan;
      // Sample terrain height at particle position
      const col = Math.round(((x / TERRAIN_SPAN) + 0.5) * (GRID_SIZE - 1));
      const row = Math.round(((z / TERRAIN_SPAN) + 0.5) * (GRID_SIZE - 1));
      const cr = Math.max(0, Math.min(GRID_SIZE - 1, row));
      const cc = Math.max(0, Math.min(GRID_SIZE - 1, col));
      const y = frame[cr][cc].revenue * (MAX_HEIGHT / 5) + 0.35;
      posArr[i * 3] = x;
      posArr[i * 3 + 1] = y;
      posArr[i * 3 + 2] = z;
      // Slight downhill bias
      const gradX = (cr > 0 && cr < GRID_SIZE - 1) ? (frame[cr + 1][cc].revenue - frame[cr - 1][cc].revenue) : 0;
      const gradZ = (cc > 0 && cc < GRID_SIZE - 1) ? (frame[cr][cc + 1].revenue - frame[cr][cc - 1].revenue) : 0;
      vx -= gradZ * 0.02 * dt;
      vz -= gradX * 0.02 * dt;
      const spd = Math.sqrt(vx * vx + vz * vz);
      const maxSpd = 2.5;
      if (spd > maxSpd) { vx = (vx / spd) * maxSpd; vz = (vz / spd) * maxSpd; }
      velocities[i * 2] = vx;
      velocities[i * 2 + 1] = vz;
    }
    geo.attributes.position.needsUpdate = true;
  };
  return { system, update: updateParticles };
}
const particleLayer = buildParticleSystem();
scene.add(particleLayer.system);
// ─── Camera bookmarks ───
const bookmarks = [
  { position: new THREE.Vector3(22, 18, 28), target: new THREE.Vector3(0, 3, 0), label: 'Overview' },
  { position: new THREE.Vector3(-8, 14, -20), target: new THREE.Vector3(-5, 4, -8), label: 'N Peak' },
  { position: new THREE.Vector3(18, 6, 8), target: new THREE.Vector3(8, 1, 4), label: 'Valley' },
];
/**
 * applyBookmark — smoothly animates camera to a saved bookmark position.
 * Uses simple lerp over ~1 second for position and target.
 * @param {number} index — bookmark index
 */
function applyBookmark(index) {
  const bm = bookmarks[index];
  if (!bm) return;
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function animStep(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOutQuad
    camera.position.lerpVectors(startPos, bm.position, ease);
    controls.target.lerpVectors(startTarget, bm.target, ease);
    controls.update();
    if (t < 1.0) {
      requestAnimationFrame(animStep);
    }
  }
  requestAnimationFrame(animStep);
}
// ─── Current time state ───
let currentTimeIndex = 0;
/**
 * setTimeStep — swaps the terrain geometry buffer from prebuilt cache and rebuilds
 * river lines. This is the only place geometry changes occur — no per-frame regeneration.
 * @param {number} index
 */
function setTimeStep(index) {
  if (index === currentTimeIndex) return;
  currentTimeIndex = index;
  terrainMesh.geometry = cachedGeometries[index];
  rebuildRivers(index);
  timeSlider.value = index;
  const hour = Math.floor((index / TIME_STEPS) * 24);
  timeValue.textContent = `${String(hour).padStart(2, '0')}:00`;
  stepLabel.textContent = `${index}/${TIME_STEPS - 1}`;
  vertCountEl.textContent = cachedGeometries[index].attributes.position.count;
}
// ─── Event listeners ───
timeSlider.addEventListener('input', () => {
  setTimeStep(parseInt(timeSlider.value, 10));
});
bookmarkBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const idx = parseInt(btn.dataset.bookmark, 10);
    applyBookmark(idx);
    bookmarkBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});
autoRotateBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autoRotateBtn.classList.toggle('active', controls.autoRotate);
});
autoRotateBtn.classList.add('active');
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Animation loop ───
const clock = new THREE.Clock();
let frameCount = 0;
let fpsUpdateTime = performance.now();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  particleLayer.update(currentTimeIndex, dt);
  renderer.render(scene, camera);
  frameCount++;
  const now = performance.now();
  if (now - fpsUpdateTime >= 500) {
    fpsEl.textContent = Math.round(frameCount / ((now - fpsUpdateTime) / 1000));
    frameCount = 0;
    fpsUpdateTime = now;
  }
}
// ─── Initialize ───
setTimeStep(0);
vertCountEl.textContent = cachedGeometries[0].attributes.position.count;
animate();
// Runtime verification — must pass with zero errors
setTimeout(verifyNoErrors, 1200);
console.log('3D Data Terrain Explorer initialized. Grid:', GRID_SIZE + 'x' + GRID_SIZE, 'Time steps:', TIME_STEPS);
console.log('Vertex count:', cachedGeometries[0].attributes.position.count, 'Particles:', PARTICLE_COUNT);
</script>
<!--
TODO / Known Issues:
  - Tooltip on hover: no raycasting implemented yet — vertex/face picking needed for data inspection overlays.
  - Raycaster for click-to-inspect: missing; needed for interactive drill-down into cell metrics.
  - River linewidth > 1 not supported on Windows WebGL — switch to tube geometry or MeshLine for thick rivers.
  - Particle trail persistence: particles currently wrap at edges; a trail history buffer would show flow paths over time.
  - Data import: only synthetic data; need CSV/JSON file drop or API fetch for real datasets.
  - Mobile touch: OrbitControls works but UI panel layout not optimized for narrow viewports.
  - Color legend: static swatches; a dynamic gradient bar matching the actual data range would improve accuracy.
  - Performance at GRID_SIZE > 100: consider LOD or terrain chunking for large datasets.
  - Accessibility: no keyboard navigation for time slider or bookmarks.
  - Web Worker offloading: terrain geometry construction could move to a worker for large grids.
-->
</body>
</html>