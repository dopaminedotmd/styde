<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a0f; --panel-bg: rgba(10,10,20,0.92); --text: #c8ccd4; --accent: #4da6ff; --river: #e05540; --slider-track: #1a1a2e; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: var(--text); }
  #canvas-container { position: fixed; inset: 0; z-index: 0; }
  canvas { display: block; }
  #panel {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: var(--panel-bg); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 14px 20px; z-index: 10;
    display: flex; flex-direction: column; gap: 10px; min-width: 460px;
    backdrop-filter: blur(12px); box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  }
  #panel-header { display: flex; justify-content: space-between; align-items: center; }
  #panel-header span { font-size: 13px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: #8892a4; }
  #time-label { color: var(--accent) !important; font-size: 15px !important; }
  #time-slider { width: 100%; height: 6px; -webkit-appearance: none; appearance: none; background: var(--slider-track); border-radius: 3px; outline: none; cursor: pointer; }
  #time-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%; background: var(--accent); border: 2px solid #fff; cursor: pointer; }
  #btn-row { display: flex; gap: 8px; flex-wrap: wrap; }
  .btn {
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
    color: var(--text); padding: 6px 13px; border-radius: 7px; cursor: pointer;
    font-size: 12px; transition: all 0.18s; white-space: nowrap;
  }
  .btn:hover { background: rgba(255,255,255,0.14); border-color: rgba(255,255,255,0.28); }
  .btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  #legend { position: fixed; top: 20px; right: 20px; z-index: 10; background: var(--panel-bg); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px 16px; font-size: 11px; backdrop-filter: blur(12px); display: flex; flex-direction: column; gap: 6px; }
  .legend-item { display: flex; align-items: center; gap: 8px; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
  .legend-swatch.elevation { background: linear-gradient(180deg, #2d1b4e, #3b6f3b, #c9a834); }
  .legend-swatch.river { background: var(--river); width: 14px; height: 3px; border-radius: 2px; }
  .legend-swatch.particle { background: #80d8ff; width: 8px; height: 8px; border-radius: 50%; }
  #stats { position: fixed; top: 20px; left: 20px; z-index: 10; background: var(--panel-bg); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 10px 14px; font-size: 11px; backdrop-filter: blur(12px); display: flex; flex-direction: column; gap: 3px; min-width: 130px; }
  .stat-val { color: var(--accent); font-weight: 600; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="stats">
  <div>FPS <span class="stat-val" id="fps-val">--</span></div>
  <div>Vertices <span class="stat-val" id="vert-val">--</span></div>
  <div>Draw calls <span class="stat-val" id="draw-val">--</span></div>
</div>
<div id="legend">
  <div class="legend-item"><div class="legend-swatch elevation"></div> Revenue elevation</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#3b9b3b;"></div> User density (color)</div>
  <div class="legend-item"><div class="legend-swatch river"></div> Error river</div>
  <div class="legend-item"><div class="legend-swatch particle"></div> API call particles</div>
</div>
<div id="panel">
  <div id="panel-header">
    <span id="time-label">Hour 12:00</span>
    <span style="color:#667080;">Terrain Explorer</span>
  </div>
  <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
  <div id="btn-row">
    <button class="btn active" id="btn-play">Play</button>
    <button class="btn" id="btn-auto-rotate">Auto Rotate</button>
    <button class="btn" id="btn-bookmark-1">Overview</button>
    <button class="btn" id="btn-bookmark-2">River View</button>
    <button class="btn" id="btn-bookmark-3">Peak Closeup</button>
  </div>
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
const GRID = 100;
const TERRAIN_SIZE = 20;
const TIME_STEPS = 24;
const PARTICLE_COUNT = 600;
const BOOKMARKS = {
  overview:    { pos: [12, 14, 16], target: [0, 0, 0] },
  riverView:   { pos: [-6, 5, -8], target: [-4, -1.5, 4] },
  peakCloseup: { pos: [4, 3, 8], target: [3, 1.5, 3] }
};
let scene, camera, renderer, controls;
let terrainMesh, riverLines, particleSystem;
let clock = new THREE.Clock();
let fpsFrames = 0, fpsTime = 0;
let currentHour = 12;
let playing = false, autoRotate = false;
let playInterval = null;
const heightCache = new Array(TIME_STEPS);
const colorCache = new Array(TIME_STEPS);
const riverCache = new Array(TIME_STEPS);
const particlePathCache = new Array(TIME_STEPS);
const posArr = new Float32Array(GRID * GRID * 3);
const colArr = new Float32Array(GRID * GRID * 3);
const idxArr = new Uint32Array((GRID - 1) * (GRID - 1) * 6);
const particlePosArr = new Float32Array(PARTICLE_COUNT * 3);
const particleVelArr = new Float32Array(PARTICLE_COUNT * 3);
let frameCount = 0;
let lastDrawCalls = 0;
function lerp(a, b, t) { return a + (b - a) * t; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
function noise2D(x, z, seed) {
  const n = Math.sin(x * 12.9898 + z * 78.233 + seed * 437.58) * 43758.5453;
  return n - Math.floor(n);
}
function smoothNoise(x, z, octaves, seed) {
  let val = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    val += noise2D(x * freq, z * freq, seed + i * 71) * amp;
    max += amp;
    amp *= 0.5;
    freq *= 2.0;
  }
  return val / max;
}
function generateData(hour) {
  const t = hour / TIME_STEPS;
  const revenue = new Float32Array(GRID * GRID);
  const userDensity = new Float32Array(GRID * GRID);
  const errors = [];
  const particlePaths = [];
  const businessPeak = 1.0 - Math.abs(t - 0.5) * 2.0;
  const eveningBump = Math.exp(-((t - 0.75) * (t - 0.75)) / 0.03) * 0.4;
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const wx = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const wz = (iz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const baseHill = smoothNoise(wx * 0.4, wz * 0.4, 4, 0) * 4.0;
      const ridge = smoothNoise(wx * 0.7 + 2, wz * 0.7, 3, 10) * 3.0;
      const detail = smoothNoise(wx * 1.5, wz * 1.5, 2, 20) * 1.2;
      const timeMod = (businessPeak + eveningBump * smoothNoise(wx * 0.3, wz * 0.3, 2, 30)) * 2.5;
      revenue[iz * GRID + ix] = (baseHill + ridge + detail) * (0.5 + timeMod) + 0.8;
      const densBase = smoothNoise(wx * 0.5 + 5, wz * 0.5 + 5, 3, 40);
      userDensity[iz * GRID + ix] = clamp(densBase * 0.7 + businessPeak * 0.3 + 0.25, 0.1, 1.0);
    }
  }
  const riverSeed = Math.floor(t * 100);
  const riverPoints = [];
  let rx = -TERRAIN_SIZE * 0.45, rz = -TERRAIN_SIZE * 0.4;
  for (let i = 0; i < 80; i++) {
    const progress = i / 79;
    const nx = noise2D(rx * 0.3, rz * 0.3, riverSeed + i * 0.1) - 0.5;
    const nz = noise2D(rx * 0.3 + 10, rz * 0.3 + 10, riverSeed + i * 0.1) - 0.5;
    rx += nx * 0.7;
    rz += nz * 0.7 + 0.15;
    const gx = clamp(Math.round((rx / TERRAIN_SIZE + 0.5) * (GRID - 1)), 0, GRID - 1);
    const gz = clamp(Math.round((rz / TERRAIN_SIZE + 0.5) * (GRID - 1)), 0, GRID - 1);
    const h = revenue[gz * GRID + gx] + 0.05;
    riverPoints.push(new THREE.Vector3(rx, h, rz));
    if (i % 7 === 0) errors.push({ x: rx, z: rz, severity: clamp(noise2D(rx, rz, riverSeed + 99) * 2, 0.3, 1.0) });
  }
  riverCache[hour] = riverPoints;
  heightCache[hour] = revenue;
  colorCache[hour] = userDensity;
  const ppaths = [];
  for (let p = 0; p < 5; p++) {
    const path = [];
    let px = (Math.random() - 0.5) * TERRAIN_SIZE * 0.8;
    let pz = (Math.random() - 0.5) * TERRAIN_SIZE * 0.8;
    for (let s = 0; s < 120; s++) {
      px += (noise2D(px * 0.4, pz * 0.4, p * 73 + s * 0.3) - 0.5) * 0.5;
      pz += (noise2D(px * 0.4 + 77, pz * 0.4 + 77, p * 73 + s * 0.3) - 0.5) * 0.5;
      const gx = clamp(Math.round((px / TERRAIN_SIZE + 0.5) * (GRID - 1)), 0, GRID - 1);
      const gz = clamp(Math.round((pz / TERRAIN_SIZE + 0.5) * (GRID - 1)), 0, GRID - 1);
      const h = revenue[gz * GRID + gx] + 0.2;
      path.push(new THREE.Vector3(px, h, pz));
    }
    ppaths.push(path);
  }
  particlePathCache[hour] = ppaths;
  return { revenue, userDensity, riverPoints, errors, ppaths };
}
function buildGeometry(hour) {
  const revenue = heightCache[hour];
  const density = colorCache[hour];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iz * GRID + ix;
      const wx = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const wz = (iz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const h = revenue[i];
      posArr[i * 3] = wx;
      posArr[i * 3 + 1] = h;
      posArr[i * 3 + 2] = wz;
      const d = density[i];
      const r = lerp(0.18, 0.22, d) + (1 - d) * 0.05;
      const g = lerp(0.22, 0.65, d) + d * 0.1;
      const b = lerp(0.35, 0.25, d) + (1 - d) * 0.05;
      colArr[i * 3] = r;
      colArr[i * 3 + 1] = g;
      colArr[i * 3 + 2] = b;
    }
  }
  let idx = 0;
  for (let iz = 0; iz < GRID - 1; iz++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iz * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      idxArr[idx++] = a; idxArr[idx++] = b; idxArr[idx++] = d;
      idxArr[idx++] = a; idxArr[idx++] = d; idxArr[idx++] = c;
    }
  }
  if (terrainMesh) {
    terrainMesh.geometry.attributes.position.needsUpdate = true;
    terrainMesh.geometry.attributes.color.needsUpdate = true;
    terrainMesh.geometry.index.needsUpdate = true;
  }
}
function buildRiverLines(hour) {
  if (riverLines) {
    scene.remove(riverLines);
    riverLines.geometry.dispose();
    riverLines.material.dispose();
  }
  const points = riverCache[hour];
  const curve = new THREE.CatmullRomCurve3(points);
  const sampled = curve.getPoints(points.length * 3);
  const geo = new THREE.BufferGeometry().setFromPoints(sampled);
  const mat = new THREE.LineBasicMaterial({ color: 0xe05540, linewidth: 1, transparent: true, opacity: 0.85, depthTest: true });
  riverLines = new THREE.Line(geo, mat);
  riverLines.renderOrder = 1;
  riverLines.material.depthTest = true;
  riverLines.material.depthWrite = true;
  scene.add(riverLines);
}
function resetParticles(hour) {
  const paths = particlePathCache[hour];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pathIdx = i % paths.length;
    const path = paths[pathIdx];
    const seg = Math.floor(Math.random() * (path.length - 1));
    const t = Math.random();
    const p0 = path[seg], p1 = path[Math.min(seg + 1, path.length - 1)];
    particlePosArr[i * 3] = lerp(p0.x, p1.x, t);
    particlePosArr[i * 3 + 1] = lerp(p0.y, p1.y, t);
    particlePosArr[i * 3 + 2] = lerp(p0.z, p1.z, t);
    particleVelArr[i * 3] = (Math.random() - 0.5) * 0.3;
    particleVelArr[i * 3 + 1] = Math.random() * 0.15;
    particleVelArr[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
function updateParticles(hour, dt) {
  const revenue = heightCache[hour];
  const speed = 0.8 + (playing ? 1.2 : 0.2);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const i3 = i * 3;
    let px = particlePosArr[i3] + particleVelArr[i3] * dt * speed;
    let pz = particlePosArr[i3 + 2] + particleVelArr[i3 + 2] * dt * speed;
    if (Math.abs(px) > TERRAIN_SIZE * 0.5 || Math.abs(pz) > TERRAIN_SIZE * 0.5) {
      const paths = particlePathCache[hour];
      const path = paths[i % paths.length];
      const p0 = path[0];
      px = p0.x + (Math.random() - 0.5) * 1.5;
      pz = p0.z + (Math.random() - 0.5) * 1.5;
      particleVelArr[i3] = (Math.random() - 0.5) * 0.3;
      particleVelArr[i3 + 2] = (Math.random() - 0.5) * 0.3;
    }
    const gx = clamp(Math.round((px / TERRAIN_SIZE + 0.5) * (GRID - 1)), 0, GRID - 1);
    const gz = clamp(Math.round((pz / TERRAIN_SIZE + 0.5) * (GRID - 1)), 0, GRID - 1);
    const h = revenue[gz * GRID + gx] + 0.25;
    particlePosArr[i3] = px;
    particlePosArr[i3 + 1] = h;
    particlePosArr[i3 + 2] = pz;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
function setHour(hour) {
  currentHour = clamp(hour, 0, TIME_STEPS - 1);
  document.getElementById('time-slider').value = currentHour;
  document.getElementById('time-label').textContent = `Hour ${String(currentHour).padStart(2, '0')}:00`;
  buildGeometry(currentHour);
  buildRiverLines(currentHour);
  resetParticles(currentHour);
}
function applyBookmark(name) {
  const bm = BOOKMARKS[name];
  if (!bm) return;
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800;
  function anim(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
}
function setup() {
  const container = document.getElementById('canvas-container');
  const w = container.clientWidth, h = container.clientHeight;
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setSize(w, h);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  container.appendChild(renderer.domElement);
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a14);
  scene.fog = new THREE.Fog(0x0a0a14, 15, 50);
  camera = new THREE.PerspectiveCamera(55, w / h, 0.5, 80);
  camera.position.set(12, 14, 16);
  const ambientLight = new THREE.AmbientLight(0x303550, 1.8);
  scene.add(ambientLight);
  const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
  sun.position.set(15, 20, 8);
  sun.castShadow = true;
  sun.shadow.mapSize.width = 2048;
  sun.shadow.mapSize.height = 2048;
  sun.shadow.camera.near = 0.5;
  sun.shadow.camera.far = 60;
  sun.shadow.camera.left = -18;
  sun.shadow.camera.right = 18;
  sun.shadow.camera.top = 18;
  sun.shadow.camera.bottom = -18;
  sun.shadow.bias = -0.0001;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x8899cc, 1.2);
  fill.position.set(-8, 4, -6);
  scene.add(fill);
  const hemi = new THREE.HemisphereLight(0x8899cc, 0x223344, 0.8);
  scene.add(hemi);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.target.set(0, 0, 0);
  controls.minDistance = 4;
  controls.maxDistance = 35;
  controls.maxPolarAngle = Math.PI * 0.52;
  controls.update();
  const terrainGeo = new THREE.BufferGeometry();
  terrainGeo.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
  terrainGeo.setAttribute('color', new THREE.BufferAttribute(colArr, 3));
  terrainGeo.setIndex(new THREE.BufferAttribute(idxArr, 1));
  terrainGeo.computeVertexNormals();
  const terrainMat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide
  });
  terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  const gridHelper = new THREE.PolarGridHelper(14, 40, 30, 256, 0x222244, 0x222244);
  gridHelper.position.y = -0.6;
  scene.add(gridHelper);
  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePosArr, 3));
  const particleMat = new THREE.PointsMaterial({
    color: 0x80d8ff,
    size: 0.08,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.75
  });
  particleSystem = new THREE.Points(particleGeo, particleMat);
  particleSystem.renderOrder = 2;
  scene.add(particleSystem);
  window.addEventListener('resize', () => {
    const cw = container.clientWidth, ch = container.clientHeight;
    camera.aspect = cw / ch;
    camera.updateProjectionMatrix();
    renderer.setSize(cw, ch);
  });
  document.getElementById('time-slider').addEventListener('input', (e) => {
    stopPlay();
    setHour(parseInt(e.target.value));
  });
  document.getElementById('btn-play').addEventListener('click', togglePlay);
  document.getElementById('btn-auto-rotate').addEventListener('click', toggleAutoRotate);
  document.getElementById('btn-bookmark-1').addEventListener('click', () => applyBookmark('overview'));
  document.getElementById('btn-bookmark-2').addEventListener('click', () => applyBookmark('riverView'));
  document.getElementById('btn-bookmark-3').addEventListener('click', () => applyBookmark('peakCloseup'));
  document.addEventListener('keydown', (e) => {
    if (e.key === ' ') { e.preventDefault(); togglePlay(); }
    if (e.key === 'r') { e.preventDefault(); toggleAutoRotate(); }
    if (e.key === '1') applyBookmark('overview');
    if (e.key === '2') applyBookmark('riverView');
    if (e.key === '3') applyBookmark('peakCloseup');
  });
}
function togglePlay() {
  playing = !playing;
  const btn = document.getElementById('btn-play');
  btn.textContent = playing ? 'Pause' : 'Play';
  btn.classList.toggle('active', playing);
  if (playing) {
    playInterval = setInterval(() => {
      setHour((currentHour + 1) % TIME_STEPS);
    }, 2800);
  } else {
    stopPlay();
  }
}
function stopPlay() {
  playing = false;
  if (playInterval) { clearInterval(playInterval); playInterval = null; }
  const btn = document.getElementById('btn-play');
  btn.textContent = 'Play';
  btn.classList.remove('active');
}
function toggleAutoRotate() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  controls.autoRotateSpeed = 0.6;
  const btn = document.getElementById('btn-auto-rotate');
  btn.classList.toggle('active', autoRotate);
}
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  updateParticles(currentHour, dt);
  frameCount++;
  fpsFrames++;
  fpsTime += dt;
  if (fpsTime >= 0.5) {
    document.getElementById('fps-val').textContent = Math.round(fpsFrames / fpsTime);
    document.getElementById('vert-val').textContent = (GRID * GRID + PARTICLE_COUNT).toLocaleString();
    document.getElementById('draw-val').textContent = renderer.info.render.calls;
    fpsFrames = 0;
    fpsTime = 0;
  }
  renderer.render(scene, camera);
}
for (let h = 0; h < TIME_STEPS; h++) generateData(h);
setup();
setHour(12);
animate();
</script>
</body>
</html>