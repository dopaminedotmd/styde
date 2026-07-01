<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a0f;--panel:#12121a;--text:#c8ccd4;--accent:#4da6ff;--error:#e05555;--river:#e04040;--slider-track:#1e1e2e}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  #container{position:fixed;inset:0}
  canvas{display:block}
  #panel{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:var(--panel);border:1px solid #1e1e30;border-radius:12px;padding:14px 20px;display:flex;gap:18px;align-items:center;z-index:10;backdrop-filter:blur(12px);box-shadow:0 8px 32px rgba(0,0,0,0.5)}
  #panel label{font-size:12px;text-transform:uppercase;letter-spacing:0.08em;color:#7a7f8a;white-space:nowrap}
  #timeSlider{-webkit-appearance:none;width:200px;height:6px;border-radius:3px;background:var(--slider-track);outline:none;cursor:pointer}
  #timeSlider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:var(--accent);border:2px solid #fff;cursor:pointer}
  #timeValue{font-size:13px;font-weight:600;min-width:70px;text-align:center;color:var(--accent)}
  .bookmark-btn{background:#1a1a2e;border:1px solid #2a2a40;color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.2s;white-space:nowrap}
  .bookmark-btn:hover{background:#252540;border-color:var(--accent);color:#fff}
  .bookmark-btn.active{background:var(--accent);color:#000;border-color:var(--accent);font-weight:600}
  #legend{position:fixed;top:20px;right:20px;background:var(--panel);border:1px solid #1e1e30;border-radius:10px;padding:12px 16px;z-index:10;font-size:11px;display:flex;flex-direction:column;gap:8px}
  .legend-row{display:flex;align-items:center;gap:8px}
  .legend-swatch{width:14px;height:14px;border-radius:3px;flex-shrink:0}
  #info{position:fixed;top:20px;left:20px;font-size:11px;color:#5a5f6a;z-index:10}
</style>
</head>
<body>
<div id="container"></div>
<div id="info">DRAG orbit &bull; SCROLL zoom &bull; RIGHT-DRAG pan &bull; 1-3 bookmarks</div>
<div id="panel">
  <label>Time</label>
  <input type="range" id="timeSlider" min="0" max="19" value="0" step="1">
  <span id="timeValue">Day 1</span>
  <button class="bookmark-btn active" data-idx="0">Overview</button>
  <button class="bookmark-btn" data-idx="1">Error Hotspot</button>
  <button class="bookmark-btn" data-idx="2">Revenue Peak</button>
</div>
<div id="legend">
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(180deg,#2d5a27,#7cb342,#f9a825,#e53935)"></span><span>User Density (low→high)</span></div>
  <div class="legend-row"><span class="legend-swatch" style="background:var(--river)"></span><span>Error Rivers (&gt;threshold)</span></div>
  <div class="legend-row"><span class="legend-swatch" style="background:var(--accent);border-radius:50%"></span><span>API Call Particles</span></div>
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
const container = document.getElementById('container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a0f');
scene.fog = new THREE.Fog('#0a0a0f', 20, 80);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(18, 14, 22);
camera.lookAt(0, 3, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 3, 0);
controls.minDistance = 6;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.7;
controls.update();
const ambientLight = new THREE.AmbientLight('#304060', 1.6);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffe8d0', 4.5);
sunLight.position.set(20, 30, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -25;
sunLight.shadow.camera.right = 25;
sunLight.shadow.camera.top = 25;
sunLight.shadow.camera.bottom = -25;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#8090c0', 0.8);
fillLight.position.set(-10, 5, -5);
scene.add(fillLight);
const GRID = 60;
const TIME_STEPS = 20;
const TERRAIN_SIZE = 20;
const HEIGHT_SCALE = 8;
const ERROR_THRESHOLD = 0.55;
function simplexLike(x, y, t) {
  const f1 = Math.sin(x*0.8 + t*0.3) * Math.cos(y*0.7 + t*0.25);
  const f2 = Math.sin(x*1.5 - t*0.2) * Math.sin(y*1.3 + t*0.35) * 0.6;
  const f3 = Math.cos(x*2.1 + y*1.9 + t*0.15) * 0.35;
  const f4 = Math.sin((x+y)*1.1 + t*0.4) * Math.cos((x-y)*0.9 - t*0.22) * 0.25;
  return (f1 + f2 + f3 + f4 + 1) / 2.6;
}
function generateData() {
  const revenue = new Float32Array(TIME_STEPS * GRID * GRID);
  const userDensity = new Float32Array(TIME_STEPS * GRID * GRID);
  const errorRate = new Float32Array(TIME_STEPS * GRID * GRID);
  for (let t = 0; t < TIME_STEPS; t++) {
    const phase = t / TIME_STEPS * Math.PI * 2;
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = t * GRID * GRID + iz * GRID + ix;
        const nx = ix / (GRID - 1) * 2 - 1;
        const nz = iz / (GRID - 1) * 2 - 1;
        revenue[idx] = simplexLike(nx * 2.5, nz * 2.5, phase) * 0.7 + simplexLike(nx * 3.8, nz * 3.8, phase * 0.7) * 0.3;
        userDensity[idx] = simplexLike(nx * 2.2 + 0.5, nz * 2.2 + 0.5, phase * 0.8) * 0.6 + revenue[idx] * 0.4;
        const errBase = Math.abs(simplexLike(nx * 5, nz * 5, phase * 1.3) - 0.5) * 1.6;
        const errSpike = (Math.abs(nx - 0.3 + Math.sin(phase)*0.2) < 0.25 && Math.abs(nz + 0.15 + Math.cos(phase)*0.2) < 0.25) ? 0.4 : 0;
        errorRate[idx] = Math.min(1, errBase + errSpike);
      }
    }
  }
  return { revenue, userDensity, errorRate };
}
const data = generateData();
const terrainGeo = new THREE.BufferGeometry();
const posCount = GRID * GRID;
const posArray = new Float32Array(posCount * 3);
const colorArray = new Float32Array(posCount * 3);
const indexArray = new Uint32Array((GRID - 1) * (GRID - 1) * 6);
function updateTerrainBuffers(timeIdx) {
  const rev = data.revenue;
  const dens = data.userDensity;
  const base = timeIdx * posCount;
  const half = TERRAIN_SIZE / 2;
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const vi = iz * GRID + ix;
      const di = base + vi;
      const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const z = (iz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const h = rev[di] * HEIGHT_SCALE;
      posArray[vi * 3] = x;
      posArray[vi * 3 + 1] = h;
      posArray[vi * 3 + 2] = z;
      const d = dens[di];
      const r = d < 0.33 ? 0.18 + d * 0.55 : d < 0.66 ? 0.36 + (d - 0.33) * 1.9 : 0.98;
      const g = d < 0.33 ? 0.55 + d * 1.2 : d < 0.66 ? 0.95 - (d - 0.33) * 1.1 : 0.58 - (d - 0.66) * 1.5;
      const b = d < 0.33 ? 0.25 + d * 0.3 : d < 0.66 ? 0.35 - (d - 0.33) * 0.2 : 0.28 - (d - 0.66) * 0.6;
      colorArray[vi * 3] = Math.max(0, Math.min(1, r));
      colorArray[vi * 3 + 1] = Math.max(0, Math.min(1, g));
      colorArray[vi * 3 + 2] = Math.max(0, Math.min(1, b));
    }
  }
  let ii = 0;
  for (let iz = 0; iz < GRID - 1; iz++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iz * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indexArray[ii++] = a; indexArray[ii++] = c; indexArray[ii++] = b;
      indexArray[ii++] = b; indexArray[ii++] = c; indexArray[ii++] = d;
    }
  }
}
updateTerrainBuffers(0);
terrainGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colorArray, 3));
terrainGeo.setIndex(new THREE.BufferAttribute(indexArray, 1));
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2 + 2, 40, 20, 64, '#1a1a30', '#1a1a30');
gridHelper.position.y = -0.05;
scene.add(gridHelper);
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const riverLineMat = new THREE.LineBasicMaterial({ color: '#e04040', linewidth: 1, transparent: true, opacity: 0.85, depthTest: true });
function rebuildRivers(timeIdx) {
  while (riverGroup.children.length > 0) riverGroup.remove(riverGroup.children[0]);
  const err = data.errorRate;
  const rev = data.revenue;
  const base = timeIdx * posCount;
  const visited = new Uint8Array(GRID * GRID);
  const dirs = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]];
  const half = TERRAIN_SIZE / 2;
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const ci = iz * GRID + ix;
      if (visited[ci]) continue;
      if (err[base + ci] < ERROR_THRESHOLD) continue;
      const segment = [];
      const stack = [[ix, iz]];
      while (stack.length > 0) {
        const [cx, cz] = stack.pop();
        const si = cz * GRID + cx;
        if (cx < 0 || cx >= GRID || cz < 0 || cz >= GRID) continue;
        if (visited[si]) continue;
        if (err[base + si] < ERROR_THRESHOLD * 0.7) continue;
        visited[si] = 1;
        segment.push([cx, cz]);
        for (const [dx, dz] of dirs) {
          const nx = cx + dx, nz = cz + dz;
          if (nx >= 0 && nx < GRID && nz >= 0 && nz < GRID) {
            const ni = nz * GRID + nx;
            if (!visited[ni] && err[base + ni] >= ERROR_THRESHOLD * 0.7) {
              stack.push([nx, nz]);
            }
          }
        }
      }
      if (segment.length < 3) continue;
      const points = [];
      for (const [sx, sz] of segment) {
        const sxNorm = (sx / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        const szNorm = (sz / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        const si = sz * GRID + sx;
        const h = rev[base + si] * HEIGHT_SCALE + 0.25;
        points.push(new THREE.Vector3(sxNorm, h, szNorm));
      }
      if (points.length < 2) continue;
      const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
      const line = new THREE.Line(lineGeo, riverLineMat);
      riverGroup.add(line);
    }
  }
}
rebuildRivers(0);
const PARTICLE_COUNT = 600;
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = new Float32Array(PARTICLE_COUNT * 6);
function initParticles() {
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const angle = Math.random() * Math.PI * 2;
    const radius = Math.random() * TERRAIN_SIZE * 0.42;
    const px = Math.cos(angle) * radius;
    const pz = Math.sin(angle) * radius;
    particleData[i * 6] = px;
    particleData[i * 6 + 1] = pz;
    particleData[i * 6 + 2] = (Math.random() - 0.5) * 0.6;
    particleData[i * 6 + 3] = (Math.random() - 0.5) * 0.6;
    particleData[i * 6 + 4] = Math.random();
    particleData[i * 6 + 5] = 0.3 + Math.random() * 0.7;
    particlePositions[i * 3] = px;
    particlePositions[i * 3 + 1] = 0;
    particlePositions[i * 3 + 2] = pz;
    particleColors[i * 3] = 0.3;
    particleColors[i * 3 + 1] = 0.65;
    particleColors[i * 3 + 2] = 1.0;
  }
  particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
}
initParticles();
const particleMat = new THREE.PointsMaterial({
  size: 0.12,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.8
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
function getTerrainHeight(px, pz, timeIdx) {
  const half = TERRAIN_SIZE / 2;
  const fx = (px / TERRAIN_SIZE + 0.5) * (GRID - 1);
  const fz = (pz / TERRAIN_SIZE + 0.5) * (GRID - 1);
  const ix = Math.max(0, Math.min(GRID - 2, Math.floor(fx)));
  const iz = Math.max(0, Math.min(GRID - 2, Math.floor(fz)));
  const tx = fx - ix;
  const tz = fz - iz;
  const rev = data.revenue;
  const base = timeIdx * posCount;
  const h00 = rev[base + iz * GRID + ix];
  const h10 = rev[base + iz * GRID + ix + 1];
  const h01 = rev[base + (iz + 1) * GRID + ix];
  const h11 = rev[base + (iz + 1) * GRID + ix + 1];
  const h0 = h00 + (h10 - h00) * tx;
  const h1 = h01 + (h11 - h01) * tx;
  return (h0 + (h1 - h0) * tz) * HEIGHT_SCALE;
}
const bookmarks = [
  { pos: new THREE.Vector3(18, 14, 22), target: new THREE.Vector3(0, 3, 0), label: 'Overview' },
  { pos: new THREE.Vector3(2, 5, -4), target: new THREE.Vector3(2, 3, -2), label: 'Error Hotspot' },
  { pos: new THREE.Vector3(-4, 8, 8), target: new THREE.Vector3(-3, 5, 6), label: 'Revenue Peak' }
];
let currentBookmark = 0;
function animateCamera(pos, target, duration) {
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
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
function setBookmark(idx) {
  currentBookmark = idx;
  const bm = bookmarks[idx];
  animateCamera(bm.pos, bm.target, 1200);
  document.querySelectorAll('.bookmark-btn').forEach((btn, i) => {
    btn.classList.toggle('active', i === idx);
  });
}
document.querySelectorAll('.bookmark-btn').forEach(btn => {
  btn.addEventListener('click', () => setBookmark(parseInt(btn.dataset.idx)));
});
const slider = document.getElementById('timeSlider');
const timeValue = document.getElementById('timeValue');
let currentTimeIdx = 0;
let targetTimeIdx = 0;
let timeTransition = 0;
const TRANSITION_SPEED = 0.15;
slider.addEventListener('input', () => {
  targetTimeIdx = parseInt(slider.value);
  timeValue.textContent = 'Day ' + (targetTimeIdx + 1);
});
const clock = new THREE.Clock();
let elapsedTotal = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  elapsedTotal += dt;
  controls.update();
  if (timeTransition < 1 && currentTimeIdx !== targetTimeIdx) {
    timeTransition = Math.min(1, timeTransition + dt * TRANSITION_SPEED * 8);
    if (timeTransition >= 1) {
      currentTimeIdx = targetTimeIdx;
      timeTransition = 0;
      updateTerrainBuffers(currentTimeIdx);
      terrainGeo.attributes.position.needsUpdate = true;
      terrainGeo.attributes.color.needsUpdate = true;
      terrainGeo.computeVertexNormals();
      terrainGeo.attributes.normal.needsUpdate = true;
      rebuildRivers(currentTimeIdx);
    } else {
      const mix = timeTransition;
      for (let i = 0; i < posCount; i++) {
        const baseCur = currentTimeIdx * posCount + i;
        const baseTgt = targetTimeIdx * posCount + i;
        const hCur = data.revenue[baseCur] * HEIGHT_SCALE;
        const hTgt = data.revenue[baseTgt] * HEIGHT_SCALE;
        const hMix = hCur + (hTgt - hCur) * mix;
        posArray[i * 3 + 1] = hMix;
        const dCur = data.userDensity[baseCur];
        const dTgt = data.userDensity[baseTgt];
        const dMix = dCur + (dTgt - dCur) * mix;
        const d = dMix;
        const r = d < 0.33 ? 0.18 + d * 0.55 : d < 0.66 ? 0.36 + (d - 0.33) * 1.9 : 0.98;
        const g = d < 0.33 ? 0.55 + d * 1.2 : d < 0.66 ? 0.95 - (d - 0.33) * 1.1 : 0.58 - (d - 0.66) * 1.5;
        const b = d < 0.33 ? 0.25 + d * 0.3 : d < 0.66 ? 0.35 - (d - 0.33) * 0.2 : 0.28 - (d - 0.66) * 0.6;
        colorArray[i * 3] = Math.max(0, Math.min(1, r));
        colorArray[i * 3 + 1] = Math.max(0, Math.min(1, g));
        colorArray[i * 3 + 2] = Math.max(0, Math.min(1, b));
      }
      terrainGeo.attributes.position.needsUpdate = true;
      terrainGeo.attributes.color.needsUpdate = true;
      terrainGeo.computeVertexNormals();
      terrainGeo.attributes.normal.needsUpdate = true;
    }
  }
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const pBase = i * 6;
    let px = particleData[pBase];
    let pz = particleData[pBase + 1];
    let vx = particleData[pBase + 2];
    let vz = particleData[pBase + 3];
    const seed = particleData[pBase + 4];
    const speed = particleData[pBase + 5];
    const angle = elapsedTotal * 0.6 * speed + seed * Math.PI * 2;
    const flowRadius = 0.08 * TERRAIN_SIZE;
    vx += (Math.cos(angle) * flowRadius - px) * 0.004 * speed;
    vz += (Math.sin(angle) * flowRadius - pz) * 0.004 * speed;
    vx += (Math.random() - 0.5) * 0.03;
    vz += (Math.random() - 0.5) * 0.03;
    const damp = 0.94;
    vx *= damp;
    vz *= damp;
    px += vx * 0.5;
    pz += vz * 0.5;
    const limit = TERRAIN_SIZE * 0.48;
    if (Math.abs(px) > limit) { px = Math.sign(px) * limit * 0.9; vx *= -0.5; }
    if (Math.abs(pz) > limit) { pz = Math.sign(pz) * limit * 0.9; vz *= -0.5; }
    const h = getTerrainHeight(px, pz, currentTimeIdx) + 0.4;
    particleData[pBase] = px;
    particleData[pBase + 1] = pz;
    particleData[pBase + 2] = vx;
    particleData[pBase + 3] = vz;
    particlePositions[i * 3] = px;
    particlePositions[i * 3 + 1] = h;
    particlePositions[i * 3 + 2] = pz;
  }
  particleGeo.attributes.position.needsUpdate = true;
  renderer.render(scene, camera);
}
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
window.addEventListener('keydown', (e) => {
  if (e.key >= '1' && e.key <= '3') {
    setBookmark(parseInt(e.key) - 1);
  }
  if (e.key === 'ArrowLeft' && targetTimeIdx > 0) {
    targetTimeIdx--;
    slider.value = targetTimeIdx;
    timeValue.textContent = 'Day ' + (targetTimeIdx + 1);
  }
  if (e.key === 'ArrowRight' && targetTimeIdx < TIME_STEPS - 1) {
    targetTimeIdx++;
    slider.value = targetTimeIdx;
    timeValue.textContent = 'Day ' + (targetTimeIdx + 1);
  }
  if (e.key === ' ') {
    controls.autoRotate = !controls.autoRotate;
    e.preventDefault();
  }
});
animate();
console.log('3D Data Terrain Explorer ready — 60x60 terrain, 20 time steps, 600 particles, 3 bookmarks');
// SELF-VERIFICATION: file ends with complete module, script, body, html closure
</script>
</body>
</html>