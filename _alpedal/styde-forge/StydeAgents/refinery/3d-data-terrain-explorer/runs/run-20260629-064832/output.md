<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a0f; --panel: #111118; --text: #c8ccd4; --accent: #4ecdc4; --accent2: #ff6b6b; --slider-track: #1a1a28; --border: #1e1e2e; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, -apple-system, sans-serif; overflow: hidden; height: 100vh; width: 100vw; }
  #canvas-container { position: fixed; inset: 0; z-index: 1; }
  canvas { display: block; }
  #panel { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 10; background: var(--panel); border: 1px solid var(--border); border-radius: 14px; padding: 16px 20px; display: flex; gap: 20px; align-items: center; backdrop-filter: blur(20px); box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
  #panel label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #888; white-space: nowrap; }
  #time-slider { -webkit-appearance: none; width: 220px; height: 6px; border-radius: 3px; background: var(--slider-track); outline: none; cursor: pointer; }
  #time-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 18px; height: 18px; border-radius: 50%; background: var(--accent); cursor: pointer; border: 2px solid #fff; box-shadow: 0 0 12px rgba(78,205,196,0.4); }
  #time-label { font-size: 13px; font-weight: 600; color: var(--accent); min-width: 60px; text-align: center; }
  .btn { background: var(--border); border: 1px solid #2a2a3a; color: var(--text); padding: 8px 14px; border-radius: 8px; cursor: pointer; font-size: 12px; transition: all 0.2s; white-space: nowrap; }
  .btn:hover { background: #2a2a3c; border-color: var(--accent); }
  .btn.active { background: var(--accent); color: #000; border-color: var(--accent); }
  .stat { text-align: center; }
  .stat-val { font-size: 18px; font-weight: 700; color: #fff; }
  .stat-label { font-size: 10px; text-transform: uppercase; color: #666; margin-top: 2px; }
  #legend { position: fixed; top: 20px; right: 20px; z-index: 10; background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 14px 16px; backdrop-filter: blur(20px); font-size: 11px; }
  .legend-item { display: flex; align-items: center; gap: 8px; margin: 6px 0; }
  .legend-swatch { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
  #bookmarks { position: fixed; top: 20px; left: 20px; z-index: 10; display: flex; flex-direction: column; gap: 6px; }
  .bookmark-btn { background: var(--panel); border: 1px solid var(--border); color: var(--text); padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 11px; transition: all 0.2s; text-align: left; }
  .bookmark-btn:hover { border-color: var(--accent); background: #1a1a2a; }
  .bookmark-btn .hotkey { color: #666; font-size: 10px; }
  #tooltip { position: fixed; pointer-events: none; z-index: 20; background: rgba(0,0,0,0.85); border: 1px solid var(--accent); border-radius: 8px; padding: 10px 14px; font-size: 12px; display: none; color: #fff; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="bookmarks">
  <button class="bookmark-btn" data-view="top" title="Top-down view"><span class="hotkey">1</span> Top</button>
  <button class="bookmark-btn" data-view="perspective" title="Default perspective"><span class="hotkey">2</span> Perspective</button>
  <button class="bookmark-btn" data-view="side" title="Side profile"><span class="hotkey">3</span> Side</button>
  <button class="bookmark-btn" data-view="rivers" title="River focus"><span class="hotkey">4</span> Rivers</button>
</div>
<div id="legend">
  <div style="font-weight:700;margin-bottom:8px;color:#fff;">LEGEND</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(180deg,#ff6b6b,#feca57,#48dbfb);"></span> Elevation (Revenue)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(90deg,#2d5016,#7cb342,#c5e1a5);"></span> Vegetation (Users)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ff4444;"></span> Error Rivers</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ffd700;"></span> API Trail Particles</div>
</div>
<div id="tooltip"></div>
<div id="panel">
  <div class="stat"><div class="stat-val" id="stat-rev">—</div><div class="stat-label">Revenue</div></div>
  <div class="stat"><div class="stat-val" id="stat-users">—</div><div class="stat-label">Users</div></div>
  <div class="stat"><div class="stat-val" id="stat-err">—</div><div class="stat-label">Errors</div></div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
    <label>Time Step</label>
    <div style="display:flex;align-items:center;gap:8px;">
      <span style="font-size:11px;color:#666;">T0</span>
      <input type="range" id="time-slider" min="0" max="19" value="0" step="1">
      <span style="font-size:11px;color:#666;">T19</span>
    </div>
    <span id="time-label">T0</span>
  </div>
  <button class="btn active" id="btn-autorot">Auto-Rotate</button>
  <button class="btn" id="btn-rivers">Rivers</button>
  <button class="btn" id="btn-particles">Particles</button>
  <button class="btn" id="btn-wireframe">Wireframe</button>
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
// ─── Data Generation ───
const GRID = 80;
const STEPS = 20;
const SIZE = 20;
function perlin2D(x, y, seed) {
  const n = Math.sin(x * 12.9898 + y * 78.233 + seed * 437.58) * 43758.5453;
  return n - Math.floor(n);
}
function smoothNoise(x, y, scale, seed) {
  const sx = x / scale, sy = y / scale;
  const ix = Math.floor(sx), iy = Math.floor(sy);
  const fx = sx - ix, fy = sy - iy;
  const sx2 = fx * fx * (3 - 2 * fx), sy2 = fy * fy * (3 - 2 * fy);
  const v00 = perlin2D(ix, iy, seed), v10 = perlin2D(ix+1, iy, seed);
  const v01 = perlin2D(ix, iy+1, seed), v11 = perlin2D(ix+1, iy+1, seed);
  const a = v00 + (v10 - v00) * sx2, b = v01 + (v11 - v01) * sx2;
  return a + (b - a) * sy2;
}
function fbm(x, y, seed) {
  let v = 0, amp = 0.5, freq = 1, total = 0;
  for (let o = 0; o < 4; o++) { v += amp * smoothNoise(x, y, SIZE / freq, seed + o * 100); total += amp; amp *= 0.5; freq *= 2.1; }
  return v / total;
}
const timeSeriesData = [];
for (let t = 0; t < STEPS; t++) {
  const revenue = new Float32Array(GRID * GRID);
  const users = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  const phase = t * 0.3;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const x = (ix / (GRID-1) - 0.5) * SIZE;
      const y = (iy / (GRID-1) - 0.5) * SIZE;
      const idx = iy * GRID + ix;
      const cx = x + Math.sin(phase) * 3, cy = y + Math.cos(phase * 0.7) * 2;
      const dist = Math.sqrt(cx*cx + cy*cy);
      const hill1 = 4 * Math.exp(-dist * dist / 18);
      const hill2 = 2.5 * Math.exp(-((x-3)*(x-3)+(y+2)*(y+2)) / 12);
      const hill3 = 1.8 * Math.exp(-((x+4)*(x+4)+(y-3)*(y-3)) / 10);
      const noiseVal = fbm(x + phase * 0.5, y, t) * 1.5;
      revenue[idx] = Math.max(0, hill1 + hill2 + hill3 + noiseVal);
      users[idx] = 0.3 + 0.7 * (fbm(x + 5, y + 5, t + 50) * 0.5 + 0.5);
      const errBase = (Math.abs(cx) < 4 && Math.abs(cy) < 4) ? Math.max(0, 1 - dist/6) * fbm(x*3, y*3, t+200) : 0;
      errors[idx] = errBase * 0.4;
    }
  }
  timeSeriesData.push({ revenue, users, errors });
}
// ─── Scene Setup ───
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a0f');
scene.fog = new THREE.Fog('#0a0a0f', 15, 55);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 100);
camera.position.set(14, 10, 16);
camera.lookAt(0, 2, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 2, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.minDistance = 5;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.75;
controls.update();
// ─── Lights ───
const ambientLight = new THREE.AmbientLight('#334466', 1.5);
scene.add(ambientLight);
const sun = new THREE.DirectionalLight('#ffeec4', 4);
sun.position.set(20, 25, 15);
sun.castShadow = true;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.bias = -0.0001;
scene.add(sun);
const fill = new THREE.DirectionalLight('#4488cc', 1.2);
fill.position.set(-10, 3, -8);
scene.add(fill);
// ─── Ground Plane ───
const groundGeo = new THREE.PlaneGeometry(30, 30);
const groundMat = new THREE.MeshStandardMaterial({ color: '#111118', roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.1;
ground.receiveShadow = true;
scene.add(ground);
// ─── Grid Helper ───
const gridHelper = new THREE.PolarGridHelper(14, 32, 24, 128, '#1a1a2a', '#1a1a2a');
gridHelper.position.y = 0.01;
scene.add(gridHelper);
// ─── Terrain Mesh ───
const terrainGeo = new THREE.BufferGeometry();
const vertices = new Float32Array(GRID * GRID * 3);
const colors = new Float32Array(GRID * GRID * 3);
const indices = [];
for (let iy = 0; iy < GRID - 1; iy++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = iy * GRID + ix, b = a + 1, c = a + GRID, d = c + 1;
    indices.push(a, b, d, a, d, c);
  }
}
for (let i = 0; i < GRID * GRID; i++) {
  vertices[i * 3] = ((i % GRID) / (GRID - 1) - 0.5) * SIZE;
  vertices[i * 3 + 1] = 0;
  vertices[i * 3 + 2] = (Math.floor(i / GRID) / (GRID - 1) - 0.5) * SIZE;
}
terrainGeo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
terrainGeo.setIndex(indices);
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ─── River Lines ───
const riverGroup = new THREE.Group();
scene.add(riverGroup);
let riversVisible = true;
function buildRivers(errors) {
  riverGroup.clear();
  const threshold = 0.15;
  const segments = [];
  const visited = new Uint8Array(GRID * GRID);
  const dirs = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      if (errors[idx] < threshold || visited[idx]) continue;
      const path = [];
      let cx = ix, cy = iy, ci = idx;
      for (let step = 0; step < 60; step++) {
        if (cx < 0 || cx >= GRID || cy < 0 || cy >= GRID) break;
        path.push({ x: (cx/(GRID-1)-0.5)*SIZE, y: (cy/(GRID-1)-0.5)*SIZE, err: errors[cy*GRID+cx] });
        visited[cy * GRID + cx] = 1;
        let bestD = -1, bestErr = -Infinity;
        for (const [dx, dy] of dirs) {
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
          if (errors[ny * GRID + nx] > bestErr) { bestErr = errors[ny*GRID+nx]; bestD = dirs.indexOf([dx,dy]); }
        }
        if (bestErr < threshold) break;
        cx += dirs[Math.floor(Math.random()*Math.min(3,dirs.length))][0];
        cy += dirs[Math.floor(Math.random()*Math.min(3,dirs.length))][1];
      }
      if (path.length > 5) segments.push(path);
    }
  }
  const material = new THREE.MeshBasicMaterial({ color: '#ff4444', transparent: true, opacity: 0.85, side: THREE.DoubleSide });
  for (const path of segments) {
    const curve = new THREE.CatmullRomCurve3(path.map(p => new THREE.Vector3(p.x, p.err * 4 + 0.05, p.y)));
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.06, 6, false);
    const tube = new THREE.Mesh(tubeGeo, material);
    tube.renderOrder = 1;
    tube.material.depthTest = true;
    tube.material.depthWrite = true;
    riverGroup.add(tube);
  }
}
// ─── Particle System ───
const PARTICLE_COUNT = 400;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColorsArr = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColorsArr, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.12,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8,
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
particleSystem.renderOrder = 2;
scene.add(particleSystem);
let particlesVisible = true;
function initParticles() {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const angle = Math.random() * Math.PI * 2;
    const r = 3 + Math.random() * 8;
    particlePositions[i * 3] = Math.cos(angle) * r;
    particlePositions[i * 3 + 1] = 0.5 + Math.random() * 4;
    particlePositions[i * 3 + 2] = Math.sin(angle) * r;
    particleVelocities[i * 3] = (Math.random() - 0.5) * 0.03;
    particleVelocities[i * 3 + 1] = (Math.random() - 0.5) * 0.02;
    particleVelocities[i * 3 + 2] = (Math.random() - 0.5) * 0.03;
    particleColorsArr[i * 3] = 1.0;
    particleColorsArr[i * 3 + 1] = 0.75 + Math.random() * 0.25;
    particleColorsArr[i * 3 + 2] = 0.2 + Math.random() * 0.3;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
initParticles();
// ─── Update Terrain for Time Step ───
function updateTerrain(step) {
  const data = timeSeriesData[step];
  const pos = terrainGeo.attributes.position.array;
  const col = terrainGeo.attributes.color.array;
  for (let i = 0; i < GRID * GRID; i++) {
    const h = data.revenue[i];
    pos[i * 3 + 1] = h;
    const u = data.users[i];
    col[i * 3] = 0.18 + u * 0.6;
    col[i * 3 + 1] = 0.3 + u * 0.78;
    col[i * 3 + 2] = 0.08 + u * 0.2;
    const elevFactor = h / 6;
    col[i * 3] += elevFactor * 0.3;
    col[i * 3 + 1] += elevFactor * 0.1;
    col[i * 3 + 2] -= elevFactor * 0.1;
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  buildRivers(data.errors);
  document.getElementById('time-label').textContent = `T${step}`;
  document.getElementById('time-slider').value = step;
  const totalRev = data.revenue.reduce((a,b)=>a+b,0)/(GRID*GRID);
  const totalUsr = data.users.reduce((a,b)=>a+b,0)/(GRID*GRID);
  const totalErr = data.errors.reduce((a,b)=>a+b,0)/(GRID*GRID);
  document.getElementById('stat-rev').textContent = (totalRev*100).toFixed(0)+'K';
  document.getElementById('stat-users').textContent = (totalUsr*100).toFixed(0)+'K';
  document.getElementById('stat-err').textContent = (totalErr*100).toFixed(1)+'%';
}
// ─── Camera Bookmarks ───
const bookmarks = {
  top: { pos: [0, 20, 1], target: [0, 1, 0] },
  perspective: { pos: [14, 10, 16], target: [0, 2, 0] },
  side: { pos: [20, 3, 0], target: [0, 2, 0] },
  rivers: { pos: [8, 3, 10], target: [0, 1.5, 0] },
};
function animateCamera(posArr, targetArr) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...posArr);
  const endTarget = new THREE.Vector3(...targetArr);
  const startTime = performance.now();
  const duration = 1200;
  function anim(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    const ease = t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2,3)/2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
}
// ─── Event Handlers ───
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  const step = parseInt(slider.value);
  updateTerrain(step);
});
document.querySelectorAll('.bookmark-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const view = btn.dataset.view;
    if (bookmarks[view]) animateCamera(bookmarks[view].pos, bookmarks[view].target);
  });
});
document.addEventListener('keydown', (e) => {
  const map = { '1': 'top', '2': 'perspective', '3': 'side', '4': 'rivers' };
  if (map[e.key] && bookmarks[map[e.key]]) animateCamera(bookmarks[map[e.key]].pos, bookmarks[map[e.key]].target);
  if (e.key === 'r') { riversVisible = !riversVisible; riverGroup.visible = riversVisible; document.getElementById('btn-rivers').classList.toggle('active', riversVisible); }
  if (e.key === 'p') { particlesVisible = !particlesVisible; particleSystem.visible = particlesVisible; document.getElementById('btn-particles').classList.toggle('active', particlesVisible); }
  if (e.key === 'a') { controls.autoRotate = !controls.autoRotate; document.getElementById('btn-autorot').classList.toggle('active', controls.autoRotate); }
  if (e.key === 'w') { terrainMat.wireframe = !terrainMat.wireframe; document.getElementById('btn-wireframe').classList.toggle('active', terrainMat.wireframe); }
  if (e.key === 'ArrowLeft') { slider.value = Math.max(0, parseInt(slider.value)-1); slider.dispatchEvent(new Event('input')); }
  if (e.key === 'ArrowRight') { slider.value = Math.min(STEPS-1, parseInt(slider.value)+1); slider.dispatchEvent(new Event('input')); }
});
document.getElementById('btn-autorot').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
document.getElementById('btn-rivers').addEventListener('click', function() {
  riversVisible = !riversVisible;
  riverGroup.visible = riversVisible;
  this.classList.toggle('active', riversVisible);
});
document.getElementById('btn-particles').addEventListener('click', function() {
  particlesVisible = !particlesVisible;
  particleSystem.visible = particlesVisible;
  this.classList.toggle('active', particlesVisible);
});
document.getElementById('btn-wireframe').addEventListener('click', function() {
  terrainMat.wireframe = !terrainMat.wireframe;
  this.classList.toggle('active', terrainMat.wireframe);
});
// ─── Raycaster for Tooltip ───
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
window.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const gx = Math.round((pt.x / SIZE + 0.5) * (GRID - 1));
    const gy = Math.round((pt.z / SIZE + 0.5) * (GRID - 1));
    if (gx >= 0 && gx < GRID && gy >= 0 && gy < GRID) {
      const step = parseInt(slider.value);
      const d = timeSeriesData[step];
      const idx = gy * GRID + gx;
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 18) + 'px';
      tooltip.style.top = (e.clientY - 10) + 'px';
      tooltip.innerHTML = `Revenue: ${(d.revenue[idx]*100).toFixed(0)}K<br>Users: ${(d.users[idx]*100).toFixed(0)}K<br>Errors: ${(d.errors[idx]*100).toFixed(1)}%`;
    }
  } else {
    tooltip.style.display = 'none';
  }
});
// ─── Resize ───
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── Animate Loop ───
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  const t = clock.getElapsedTime();
  if (particlesVisible) {
    const pos = particleGeo.attributes.position.array;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      const idx = i * 3;
      pos[idx] += particleVelocities[idx] + Math.sin(t * 2 + i) * 0.004;
      pos[idx + 1] += particleVelocities[idx + 1] + Math.cos(t * 1.7 + i) * 0.003;
      pos[idx + 2] += particleVelocities[idx + 2] + Math.cos(t * 2.3 + i + 1) * 0.004;
      if (Math.abs(pos[idx]) > 11 || pos[idx + 1] < 0 || pos[idx + 1] > 7 || Math.abs(pos[idx + 2]) > 11) {
        const angle = Math.random() * Math.PI * 2;
        const r = 3 + Math.random() * 8;
        pos[idx] = Math.cos(angle) * r;
        pos[idx + 1] = 0.5 + Math.random() * 5;
        pos[idx + 2] = Math.sin(angle) * r;
      }
    }
    particleGeo.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
}
// ─── Init ───
updateTerrain(0);
animate();
console.log('3D Data Terrain Explorer ready. Controls: drag=orbit, scroll=zoom, right-drag=pan, 1-4=bookmarks, R=rivers, P=particles, A=auto-rotate, W=wireframe, arrows=time');
</script>
</body>
</html>