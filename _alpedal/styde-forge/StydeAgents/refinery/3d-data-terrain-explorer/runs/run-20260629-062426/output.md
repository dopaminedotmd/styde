<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#0a0a14; overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:#c8d6e5; }
  #canvas3d { display:block; width:100vw; height:100vh; }
  #canvas2d { display:none; width:100vw; height:100vh; position:absolute; top:0; left:0; }
  #panel { position:absolute; top:16px; left:16px; background:rgba(10,10,30,0.85); backdrop-filter:blur(12px); border:1px solid rgba(100,140,255,0.25); border-radius:10px; padding:16px 20px; min-width:280px; z-index:10; }
  #panel h2 { font-size:15px; font-weight:600; letter-spacing:0.5px; margin-bottom:12px; color:#7c9fff; text-transform:uppercase; }
  .metric-row { display:flex; justify-content:space-between; align-items:center; margin:6px 0; font-size:13px; }
  .metric-label { opacity:0.75; }
  .metric-value { font-weight:600; font-variant-numeric:tabular-nums; }
  .legend-dot { display:inline-block; width:8px; height:8px; border-radius:50%; margin-right:6px; }
  #timeslider-wrap { margin-top:14px; }
  #timeslider-wrap label { font-size:12px; opacity:0.7; }
  #timeslider { width:100%; margin-top:4px; accent-color:#5b8cff; cursor:pointer; }
  #time-label { font-size:12px; opacity:0.7; text-align:center; display:block; margin-top:2px; }
  #bookmarks { margin-top:12px; display:flex; gap:6px; flex-wrap:wrap; }
  .bookmark-btn { background:rgba(90,130,255,0.15); border:1px solid rgba(90,130,255,0.4); color:#a0bfff; padding:4px 10px; border-radius:5px; font-size:11px; cursor:pointer; transition:all 0.2s; }
  .bookmark-btn:hover { background:rgba(90,130,255,0.3); border-color:rgba(90,130,255,0.7); }
  .bookmark-btn.active { background:rgba(90,130,255,0.4); border-color:#5b8cff; color:#fff; }
  #import-section { margin-top:14px; border-top:1px solid rgba(100,140,255,0.15); padding-top:10px; }
  #import-section label { font-size:11px; opacity:0.6; display:block; margin-bottom:4px; }
  #csvfile { font-size:11px; color:#a0bfff; width:100%; }
  #status { position:absolute; bottom:16px; left:50%; transform:translateX(-50%); background:rgba(10,10,30,0.8); border:1px solid rgba(100,140,255,0.2); border-radius:6px; padding:6px 16px; font-size:12px; opacity:0.8; z-index:10; pointer-events:none; }
  #fallback-msg { display:none; position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); background:rgba(200,60,60,0.9); padding:12px 24px; border-radius:8px; font-size:14px; z-index:100; }
</style>
</head>
<body>
<canvas id="canvas3d"></canvas>
<canvas id="canvas2d" width="800" height="600"></canvas>
<div id="fallback-msg">WebGL unavailable — 2D fallback active</div>
<div id="panel">
  <h2>Data Terrain</h2>
  <div class="metric-row"><span class="metric-label"><span class="legend-dot" style="background:#4ecdc4"></span>Revenue (elevation)</span><span class="metric-value" id="val-revenue">—</span></div>
  <div class="metric-row"><span class="metric-label"><span class="legend-dot" style="background:#7bed9f"></span>Users (vegetation)</span><span class="metric-value" id="val-users">—</span></div>
  <div class="metric-row"><span class="metric-label"><span class="legend-dot" style="background:#ff6b6b"></span>Errors (rivers)</span><span class="metric-value" id="val-errors">—</span></div>
  <div class="metric-row"><span class="metric-label"><span class="legend-dot" style="background:#ffd93d"></span>API calls (particles)</span><span class="metric-value" id="val-apicalls">—</span></div>
  <div id="timeslider-wrap">
    <label>Time</label>
    <input type="range" id="timeslider" min="0" max="23" value="0" step="1">
    <span id="time-label">Day 1</span>
  </div>
  <div id="bookmarks">
    <button class="bookmark-btn active" data-idx="0">Overview</button>
    <button class="bookmark-btn" data-idx="1">Revenue Peaks</button>
    <button class="bookmark-btn" data-idx="2">Error Valley</button>
    <button class="bookmark-btn" data-idx="3">User Hotspot</button>
  </div>
  <div id="import-section">
    <label>Import terrain data (CSV/GeoJSON)</label>
    <input type="file" id="csvfile" accept=".csv,.geojson,.json">
  </div>
</div>
<div id="status">Drag: orbit | Scroll: zoom | Right-drag: pan | Time slider: reshape terrain</div>
<script type="importmap">
{ "imports": { "three": "https://unpkg.com/three@0.160.0/build/three.module.js", "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/" } }
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 80;
const SLICES = 24;
const LRU_CAP = 8;
const BM_POSITIONS = [
  { pos:[40,55,60], target:[GRID/2,0,GRID/2], label:'Overview' },
  { pos:[10,35,70], target:[50,8,20], label:'Revenue Peaks' },
  { pos:[70,30,10], target:[20,3,50], label:'Error Valley' },
  { pos:[60,45,60], target:[40,5,40], label:'User Hotspot' }
];
function generateDataSlice(t) {
  const f = t / (SLICES - 1);
  const height = new Float32Array(GRID * GRID);
  const vegetation = new Float32Array(GRID * GRID);
  const errorMask = new Float32Array(GRID * GRID);
  const apiDensity = new Float32Array(GRID * GRID);
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      const nx = i / (GRID - 1) * 4 - 2;
      const nz = j / (GRID - 1) * 4 - 2;
      const r = Math.sqrt(nx * nx + nz * nz);
      const phase = f * Math.PI * 2;
      const h1 = 8 * Math.exp(-r * 0.8) * (0.7 + 0.3 * Math.sin(nx * 2.5 + phase));
      const h2 = 4 * Math.exp(-((nx - 0.8) * (nx - 0.8) + (nz + 0.3) * (nz + 0.3)) * 1.5) * (0.7 + 0.3 * Math.cos(phase * 1.3));
      const h3 = 3 * Math.exp(-((nx + 1.1) * (nx + 1.1) + (nz - 0.6) * (nz - 0.6)) * 2.0) * (0.5 + 0.5 * Math.sin(phase * 0.7));
      height[idx] = h1 + h2 + h3;
      vegetation[idx] = 0.2 + 0.8 * Math.max(0, Math.min(1, (h2 + h3 * 0.6) / 5));
      const errBase = 0.15 * Math.exp(-((nx + 0.5) * (nx + 0.5) + (nz - 0.2) * (nz - 0.2)) * 3);
      errorMask[idx] = errBase * (0.5 + 0.5 * Math.sin(phase * 2 + nx * 1.5));
      apiDensity[idx] = 0.1 + 0.9 * (vegetation[idx] * 0.6 + 0.4 * (1 - errorMask[idx]));
    }
  }
  return { height, vegetation, errorMask, apiDensity };
}
function computeMetrics(slice) {
  let rSum = 0, uSum = 0, eSum = 0, aSum = 0;
  for (let i = 0; i < GRID * GRID; i++) {
    rSum += slice.height[i];
    uSum += slice.vegetation[i];
    eSum += slice.errorMask[i];
    aSum += slice.apiDensity[i];
  }
  const n = GRID * GRID;
  return {
    revenue: (rSum / n * 1200).toFixed(0),
    users: (uSum / n * 100).toFixed(1) + '%',
    errors: (eSum / n * 100).toFixed(2) + '%',
    apicalls: (aSum / n * 5000).toFixed(0) + '/s'
  };
}
let renderer, scene, camera, controls, terrainMesh, riverGroup, particleSystem;
let currentSliceIdx = 0;
let slices = [];
let animationId = null;
let idleTimeout = null;
let idleStart = 0;
const IDLE_LIMIT = 8000;
let webglLost = false;
let fallbackCtx = null;
const geometryCache = new Map();
const lruQueue = [];
function cacheGet(key) {
  if (!geometryCache.has(key)) return null;
  lruQueue.splice(lruQueue.indexOf(key), 1);
  lruQueue.push(key);
  return geometryCache.get(key);
}
function cacheSet(key, val) {
  if (geometryCache.has(key)) {
    lruQueue.splice(lruQueue.indexOf(key), 1);
  } else if (geometryCache.size >= LRU_CAP) {
    const evict = lruQueue.shift();
    const geo = geometryCache.get(evict);
    if (geo && geo !== terrainMesh?.geometry) geo.dispose();
    geometryCache.delete(evict);
  }
  geometryCache.set(key, val);
  lruQueue.push(key);
}
function buildTerrainGeometry(slice) {
  const cached = cacheGet(currentSliceIdx);
  if (cached) return cached;
  const geo = new THREE.BufferGeometry();
  const verts = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      const vi = idx * 3;
      verts[vi] = i;
      verts[vi + 1] = slice.height[idx];
      verts[vi + 2] = j;
      const veg = slice.vegetation[idx];
      const err = slice.errorMask[idx];
      const r = 0.15 + veg * 0.35 + err * 0.5;
      const g = 0.50 + veg * 0.45 - err * 0.3;
      const b = 0.20 - err * 0.1;
      colors[vi] = r;
      colors[vi + 1] = g;
      colors[vi + 2] = b;
    }
  }
  const indices = [];
  for (let i = 0; i < GRID - 1; i++) {
    for (let j = 0; j < GRID - 1; j++) {
      const a = i * GRID + j;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  cacheSet(currentSliceIdx, geo);
  return geo;
}
function buildRiverLines(slice, prevSlice) {
  if (riverGroup) {
    while (riverGroup.children.length) {
      const child = riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      riverGroup.remove(child);
    }
  }
  const pointsAll = [];
  const threshold = 0.25;
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      if (slice.errorMask[idx] < threshold) continue;
      if (prevSlice) {
        const delta = slice.errorMask[idx] - prevSlice.errorMask[idx];
        if (Math.abs(delta) < 0.03 && delta >= 0) continue;
      }
      const x = i, y = slice.height[idx] + 0.15, z = j;
      if (pointsAll.length === 0 || 
          Math.hypot(x - pointsAll[pointsAll.length-1].x, z - pointsAll[pointsAll.length-1].z) > 2.5) {
        pointsAll.push(new THREE.Vector3(x, y, z));
      }
    }
  }
  if (pointsAll.length < 2) return;
  const curve = new THREE.CatmullRomCurve3(pointsAll);
  const tubeGeo = new THREE.TubeGeometry(curve, Math.min(pointsAll.length * 4, 200), 0.25, 6, false);
  const tubeMat = new THREE.MeshStandardMaterial({ color: 0xff4444, emissive: 0x330000, roughness: 0.5, metalness: 0.2, transparent: true, opacity: 0.8 });
  const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
  riverGroup.add(tubeMesh);
}
function buildParticles(slice) {
  if (particleSystem) {
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
    scene.remove(particleSystem);
  }
  const N = 400;
  const positions = new Float32Array(N * 3);
  const colors = new Float32Array(N * 3);
  for (let k = 0; k < N; k++) {
    const i = Math.floor(Math.random() * GRID);
    const j = Math.floor(Math.random() * GRID);
    const idx = i * GRID + j;
    const x = i + (Math.random() - 0.5) * 0.8;
    const z = j + (Math.random() - 0.5) * 0.8;
    const y = slice.height[idx] + 1.2 + Math.random() * 2.5;
    positions[k * 3] = x;
    positions[k * 3 + 1] = y;
    positions[k * 3 + 2] = z;
    const v = slice.apiDensity[idx];
    colors[k * 3] = 1.0;
    colors[k * 3 + 1] = 0.75 + v * 0.25;
    colors[k * 3 + 2] = 0.1 + v * 0.3;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  const mat = new THREE.PointsMaterial({ size: 0.22, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.75 });
  particleSystem = new THREE.Points(geo, mat);
  particleSystem.userData.positions = positions;
  particleSystem.userData.slice = slice;
  scene.add(particleSystem);
}
function updateTerrain(sliceIdx) {
  const slice = slices[sliceIdx];
  const prev = currentSliceIdx !== sliceIdx ? slices[currentSliceIdx] : null;
  currentSliceIdx = sliceIdx;
  if (terrainMesh) {
    const oldGeo = terrainMesh.geometry;
    const newGeo = buildTerrainGeometry(slice);
    terrainMesh.geometry = newGeo;
    if (oldGeo !== newGeo && !geometryCache.has(oldGeo)) oldGeo.dispose();
  }
  buildRiverLines(slice, prev);
  buildParticles(slice);
  const m = computeMetrics(slice);
  document.getElementById('val-revenue').textContent = '$' + m.revenue;
  document.getElementById('val-users').textContent = m.users;
  document.getElementById('val-errors').textContent = m.errors;
  document.getElementById('val-apicalls').textContent = m.apicalls;
  document.getElementById('time-label').textContent = 'Day ' + (sliceIdx + 1);
  document.getElementById('timeslider').value = sliceIdx;
  resetIdleTimer();
}
function startAnimation() {
  if (animationId !== null) return;
  idleStart = performance.now();
  function animate(now) {
    animationId = requestAnimationFrame(animate);
    if (webglLost) return;
    controls.update();
    if (particleSystem && particleSystem.userData.positions) {
      const pos = particleSystem.userData.positions;
      const slice = particleSystem.userData.slice;
      for (let k = 0; k < pos.length / 3; k++) {
        pos[k * 3 + 1] += (Math.sin(now * 0.002 + k * 0.3) * 0.015);
        if (pos[k * 3 + 1] > slice.height[Math.floor(k % (GRID*GRID))] + 4) pos[k * 3 + 1] = slice.height[Math.floor(k % (GRID*GRID))] + 0.8;
        if (pos[k * 3 + 1] < slice.height[Math.floor(k % (GRID*GRID))] + 0.3) pos[k * 3 + 1] = slice.height[Math.floor(k % (GRID*GRID))] + 1.5;
      }
      particleSystem.geometry.attributes.position.needsUpdate = true;
    }
    if (idleTimeout === null && performance.now() - idleStart > IDLE_LIMIT) {
      stopAnimation();
      return;
    }
    renderer.render(scene, camera);
  }
  animationId = requestAnimationFrame(animate);
}
function stopAnimation() {
  if (animationId !== null) {
    cancelAnimationFrame(animationId);
    animationId = null;
  }
  if (idleTimeout !== null) {
    clearTimeout(idleTimeout);
    idleTimeout = null;
  }
  document.getElementById('status').textContent = 'Idle — click/drag to resume';
}
function resetIdleTimer() {
  idleStart = performance.now();
  if (idleTimeout !== null) clearTimeout(idleTimeout);
  idleTimeout = setTimeout(() => {
    stopAnimation();
    idleTimeout = null;
  }, IDLE_LIMIT);
  if (animationId === null) {
    startAnimation();
    document.getElementById('status').textContent = 'Drag: orbit | Scroll: zoom | Right-drag: pan | Time slider: reshape terrain';
  }
}
function initWebGL() {
  try {
    const canvas = document.getElementById('canvas3d');
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, preserveDrawingBuffer: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;
    return true;
  } catch (e) {
    return false;
  }
}
function initFallback2D() {
  document.getElementById('canvas3d').style.display = 'none';
  document.getElementById('canvas2d').style.display = 'block';
  document.getElementById('fallback-msg').style.display = 'block';
  const c2d = document.getElementById('canvas2d');
  c2d.width = window.innerWidth;
  c2d.height = window.innerHeight;
  fallbackCtx = c2d.getContext('2d');
  if (!fallbackCtx) return;
  const slice = slices[0];
  const imgData = fallbackCtx.createImageData(GRID, GRID);
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      const h = slice.height[idx] / 10;
      const veg = slice.vegetation[idx];
      const err = slice.errorMask[idx];
      const pi = (GRID - 1 - i) * GRID + j;
      imgData.data[pi * 4] = Math.floor((0.15 + veg * 0.35 + err * 0.5) * 255);
      imgData.data[pi * 4 + 1] = Math.floor((0.50 + veg * 0.45 - err * 0.3) * 255);
      imgData.data[pi * 4 + 2] = Math.floor((0.20 - err * 0.1) * 255);
      imgData.data[pi * 4 + 3] = Math.floor(180 + h * 40);
    }
  }
  createImageBitmap(imgData).then(bmp => {
    fallbackCtx.clearRect(0, 0, c2d.width, c2d.height);
    fallbackCtx.drawImage(bmp, 40, 40, c2d.width - 80, c2d.height - 80);
    fallbackCtx.fillStyle = '#c8d6e5';
    fallbackCtx.font = '14px system-ui';
    fallbackCtx.fillText('2D fallback — WebGL not available', 50, 30);
  });
}
function handleContextLost(e) {
  e.preventDefault();
  webglLost = true;
  stopAnimation();
  initFallback2D();
}
function handleContextRestored() {
  webglLost = false;
  document.getElementById('fallback-msg').style.display = 'none';
  document.getElementById('canvas2d').style.display = 'none';
  document.getElementById('canvas3d').style.display = 'block';
  startAnimation();
  updateTerrain(currentSliceIdx);
}
async function initScene() {
  slices = [];
  for (let t = 0; t < SLICES; t++) slices.push(generateDataSlice(t));
  const ok = initWebGL();
  const canvas = document.getElementById('canvas3d');
  if (ok) {
    canvas.addEventListener('webglcontextlost', handleContextLost);
    canvas.addEventListener('webglcontextrestored', handleContextRestored);
  } else {
    initFallback2D();
    return;
  }
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a1a);
  scene.fog = new THREE.FogExp2(0x0a0a1a, 0.00025);
  camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 300);
  camera.position.set(40, 55, 60);
  camera.lookAt(GRID / 2, 4, GRID / 2);
  const ambient = new THREE.AmbientLight(0x334466, 1.3);
  scene.add(ambient);
  const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
  sun.position.set(60, 80, 40);
  sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024);
  sun.shadow.camera.near = 0.5;
  sun.shadow.camera.far = 200;
  sun.shadow.camera.left = -60;
  sun.shadow.camera.right = 60;
  sun.shadow.camera.top = 60;
  sun.shadow.camera.bottom = -60;
  scene.add(sun);
  const rim = new THREE.DirectionalLight(0x4466aa, 0.8);
  rim.position.set(-20, 10, -30);
  scene.add(rim);
  const gridHelper = new THREE.GridHelper(GRID, 20, 0x334466, 0x1a1a3a);
  gridHelper.position.y = -0.05;
  scene.add(gridHelper);
  const groundGeo = new THREE.PlaneGeometry(GRID + 10, GRID + 10);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x0a0a20, roughness: 0.9 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.set(GRID / 2, -0.1, GRID / 2);
  ground.receiveShadow = true;
  scene.add(ground);
  terrainMesh = new THREE.Mesh(buildTerrainGeometry(slices[0]), new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.7, metalness: 0.05, flatShading: false }));
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  riverGroup = new THREE.Group();
  scene.add(riverGroup);
  buildRiverLines(slices[0], null);
  buildParticles(slices[0]);
  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.25;
  controls.target.set(GRID / 2, 4, GRID / 2);
  controls.minDistance = 10;
  controls.maxDistance = 150;
  controls.maxPolarAngle = Math.PI / 2 + 0.3;
  controls.update();
  controls.addEventListener('start', resetIdleTimer);
  controls.addEventListener('end', resetIdleTimer);
  document.getElementById('timeslider').addEventListener('input', (e) => {
    const idx = parseInt(e.target.value);
    updateTerrain(idx);
  });
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.bookmark-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const bm = BM_POSITIONS[parseInt(btn.dataset.idx)];
      camera.position.set(...bm.pos);
      controls.target.set(...bm.target);
      controls.update();
      resetIdleTimer();
    });
  });
  document.getElementById('csvfile').addEventListener('change', handleFileImport);
  window.addEventListener('resize', () => {
    if (webglLost || !renderer) return;
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
  });
  window.addEventListener('pointermove', resetIdleTimer);
  window.addEventListener('wheel', resetIdleTimer);
  document.getElementById('val-revenue').textContent = '$' + computeMetrics(slices[0]).revenue;
  document.getElementById('val-users').textContent = computeMetrics(slices[0]).users;
  document.getElementById('val-errors').textContent = computeMetrics(slices[0]).errors;
  document.getElementById('val-apicalls').textContent = computeMetrics(slices[0]).apicalls;
  startAnimation();
}
function handleFileImport(e) {
  const file = e.target.files[0];
  if (!file) return;
  const ext = file.name.split('.').pop().toLowerCase();
  const reader = new FileReader();
  reader.onload = (ev) => {
    const text = ev.target.result;
    if (ext === 'csv') {
      try {
        const lines = text.trim().split('\n');
        const headers = lines[0].split(',');
        const rows = lines.slice(1).map(l => l.split(','));
        const hIdx = headers.findIndex(h => h.toLowerCase().includes('height') || h.toLowerCase().includes('elevation'));
        const vIdx = headers.findIndex(h => h.toLowerCase().includes('veg') || h.toLowerCase().includes('user'));
        const eIdx = headers.findIndex(h => h.toLowerCase().includes('err'));
        if (hIdx < 0) { alert('CSV must have a height/elevation column'); return; }
        const newSlice = {
          height: new Float32Array(GRID * GRID),
          vegetation: new Float32Array(GRID * GRID),
          errorMask: new Float32Array(GRID * GRID),
          apiDensity: new Float32Array(GRID * GRID)
        };
        const scale = Math.min(rows.length, GRID * GRID);
        for (let i = 0; i < scale; i++) {
          const row = rows[i];
          newSlice.height[i] = parseFloat(row[hIdx]) || 0;
          newSlice.vegetation[i] = vIdx >= 0 ? (parseFloat(row[vIdx]) || 0.3) : 0.3;
          newSlice.errorMask[i] = eIdx >= 0 ? (parseFloat(row[eIdx]) || 0) : 0;
          newSlice.apiDensity[i] = 0.5;
        }
        slices = [newSlice];
        geometryCache.clear();
        lruQueue.length = 0;
        currentSliceIdx = 0;
        updateTerrain(0);
        document.getElementById('timeslider').max = 0;
        document.getElementById('status').textContent = 'Imported ' + scale + ' data points from CSV';
        setTimeout(() => document.getElementById('status').textContent = 'Drag: orbit | Scroll: zoom | Right-drag: pan', 3000);
      } catch (err) {
        alert('CSV parse error: ' + err.message);
      }
    } else if (ext === 'geojson' || ext === 'json') {
      try {
        const geo = JSON.parse(text);
        const feats = geo.features || (Array.isArray(geo) ? geo : [geo]);
        const newSlice = {
          height: new Float32Array(GRID * GRID),
          vegetation: new Float32Array(GRID * GRID),
          errorMask: new Float32Array(GRID * GRID),
          apiDensity: new Float32Array(GRID * GRID)
        };
        let count = 0;
        for (const feat of feats) {
          const props = feat.properties || {};
          const coords = feat.geometry?.coordinates;
          if (!coords) continue;
          const [x, y, z] = coords.length >= 3 ? coords : [coords[0], coords[1], 0];
          const ix = Math.round((x / 4 + 2) / 4 * (GRID - 1));
          const iz = Math.round((z / 4 + 2) / 4 * (GRID - 1));
          if (ix >= 0 && ix < GRID && iz >= 0 && iz < GRID) {
            const idx = ix * GRID + iz;
            newSlice.height[idx] = (props.height || props.elevation || y || 0);
            newSlice.vegetation[idx] = props.vegetation || props.users || 0.3;
            newSlice.errorMask[idx] = props.errors || 0;
            newSlice.apiDensity[idx] = props.api_calls || 0.5;
            count++;
          }
        }
        slices = [newSlice];
        geometryCache.clear();
        lruQueue.length = 0;
        currentSliceIdx = 0;
        updateTerrain(0);
        document.getElementById('timeslider').max = 0;
        document.getElementById('status').textContent = 'Imported ' + count + ' features from GeoJSON';
        setTimeout(() => document.getElementById('status').textContent = 'Drag: orbit | Scroll: zoom | Right-drag: pan', 3000);
      } catch (err) {
        alert('GeoJSON parse error: ' + err.message);
      }
    }
  };
  reader.readAsText(file);
}
initScene().catch(err => {
  console.error('Scene init failed:', err);
  initFallback2D();
});
</script>
</body>
</html>