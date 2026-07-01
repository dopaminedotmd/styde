<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8c8d4}
canvas{display:block}
#ui{position:fixed;bottom:0;left:0;right:0;padding:16px 20px;background:linear-gradient(transparent,rgba(10,10,20,0.95) 30%);display:flex;flex-wrap:wrap;gap:12px;align-items:center;z-index:10}
#time-slider{flex:1;min-width:200px;max-width:500px;accent-color:#4af}
#time-label{font-variant-numeric:tabular-nums;min-width:80px;text-align:center;font-size:14px}
button{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#c8c8d4;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:13px;transition:all 0.2s}
button:hover{background:rgba(255,255,255,0.16);border-color:rgba(255,255,255,0.3)}
button.active{background:rgba(74,170,255,0.2);border-color:#4af;color:#4af}
#bookmarks{position:fixed;top:16px;right:16px;display:flex;flex-direction:column;gap:6px;z-index:10}
#bookmarks button{font-size:12px;padding:4px 10px;text-align:left}
#legend{position:fixed;top:16px;left:16px;z-index:10;font-size:11px;line-height:1.6;background:rgba(10,10,20,0.85);padding:10px 14px;border-radius:8px;border:1px solid rgba(255,255,255,0.1)}
#legend span{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:middle}
#stats{position:fixed;top:16px;left:50%;transform:translateX(-50%);font-size:11px;color:rgba(200,200,212,0.6);z-index:10}
</style>
</head>
<body>
<div id="stats">FPS: --</div>
<div id="legend">
<div><span style="background:linear-gradient(135deg,#2d8,#fff)"></span>Revenue (height)</div>
<div><span style="background:linear-gradient(135deg,#f44,#f80)"></span>Error rivers</div>
<div><span style="background:#4af;border-radius:50%"></span>API call particles</div>
<div><span style="background:linear-gradient(135deg,#2a2,#4a4)"></span>User density (color)</div>
</div>
<div id="bookmarks">
<button id="bm-save" title="Save camera bookmark">+ Bookmark</button>
</div>
<div id="ui">
<button id="btn-play" title="Play/Pause time">&#9654;</button>
<input type="range" id="time-slider" min="0" max="23" value="0" step="1">
<span id="time-label">00:00</span>
<button id="btn-speed" title="Speed">1x</button>
<button id="btn-auto-rotate" title="Auto-rotate">Rotate</button>
<button id="btn-top" title="Top view">Top</button>
<button id="btn-front" title="Front view">Front</button>
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
const GRID = 50;
const TIME_STEPS = 24;
const TERRAIN_SIZE = 18;
const MAX_HEIGHT = 5;
const PARTICLE_COUNT = 600;
const RIVER_THRESHOLD = 0.28;
const RIVER_MAX_PATHS = 15;
function hash(x, y) {
  let h = x * 374761393 + y * 668265263;
  h = (h ^ (h >> 13)) * 1274126177;
  return (h ^ (h >> 16)) / 2147483648;
}
function smoothNoise(x, y) {
  const ix = Math.floor(x), iy = Math.floor(y);
  const fx = x - ix, fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
  const n00 = hash(ix, iy), n10 = hash(ix+1, iy);
  const n01 = hash(ix, iy+1), n11 = hash(ix+1, iy+1);
  return n00*(1-sx)*(1-sy) + n10*sx*(1-sy) + n01*(1-sx)*sy + n11*sx*sy;
}
const precomputed = [];
for (let t = 0; t < TIME_STEPS; t++) {
  const phase = (t / TIME_STEPS) * Math.PI * 2;
  const revenue = new Float32Array(GRID * GRID);
  const users = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  const apiCalls = new Float32Array(GRID * GRID);
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      const nx = (j / (GRID-1) - 0.5) * 6;
      const ny = (i / (GRID-1) - 0.5) * 6;
      revenue[idx] = (
        Math.sin(nx * 2.7 + phase) * Math.cos(ny * 2.1 + phase * 0.7) * 0.4 +
        Math.sin(nx * 4.5 - phase * 0.5) * 0.2 +
        Math.cos(ny * 3.8 + phase * 0.3) * 0.2 +
        smoothNoise(nx * 2 + phase * 0.2, ny * 2 + phase * 0.3) * 0.15 +
        0.45
      );
      users[idx] = Math.max(0, Math.min(1, (
        Math.sin(nx * 2.2 - phase * 0.7) * Math.cos(ny * 2.8 + phase * 0.5) * 0.35 +
        Math.cos(nx * 3.6 + phase * 0.6) * 0.15 +
        0.5
      )));
      const errNoise = smoothNoise(nx * 5 + phase * 1.5, ny * 4.5 + phase * 1.2);
      errors[idx] = Math.max(0, Math.min(1, errNoise * 0.45 + 0.08 + Math.sin(phase * 3.3) * 0.08));
      apiCalls[idx] = users[idx] * (0.8 + smoothNoise(nx * 7, ny * 6) * 0.4);
    }
  }
  precomputed.push({ revenue, users, errors, apiCalls });
}
const riverPaths = precomputed.map(slice => {
  const { revenue, errors } = slice;
  const hotspotCells = [];
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i * GRID + j;
      if (errors[idx] > RIVER_THRESHOLD) {
        hotspotCells.push({ i, j, h: revenue[idx], err: errors[idx] });
      }
    }
  }
  hotspotCells.sort((a, b) => b.err - a.err);
  const seeds = hotspotCells.slice(0, RIVER_MAX_PATHS);
  const paths = [];
  const visited = new Uint8Array(GRID * GRID);
  for (const seed of seeds) {
    if (visited[seed.i * GRID + seed.j]) continue;
    const path = [];
    let ci = seed.i, cj = seed.j;
    let steps = 0;
    while (steps < 120) {
      const cidx = ci * GRID + cj;
      if (visited[cidx]) break;
      visited[cidx] = 1;
      path.push({ i: ci, j: cj, h: revenue[cidx] });
      let bestDi = 0, bestDj = 0, bestH = revenue[cidx];
      for (let di = -1; di <= 1; di++) {
        for (let dj = -1; dj <= 1; dj++) {
          if (di === 0 && dj === 0) continue;
          const ni = ci + di, nj = cj + dj;
          if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
          const nidx = ni * GRID + nj;
          if (revenue[nidx] < bestH) {
            bestH = revenue[nidx];
            bestDi = di; bestDj = dj;
          }
        }
      }
      if (bestDi === 0 && bestDj === 0) break;
      ci += bestDi; cj += bestDj;
      steps++;
    }
    if (path.length > 1) paths.push(path);
  }
  return paths;
});
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.FogExp2(0x0a0a18, 0.00012);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(12, 9, 14);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.65;
controls.target.set(0, 1.5, 0);
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(10, 15, 5);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -15;
sunLight.shadow.camera.right = 15;
sunLight.shadow.camera.top = 15;
sunLight.shadow.camera.bottom = -15;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x6688cc, 1.2);
fillLight.position.set(-5, 2, -3);
scene.add(fillLight);
const planeGeo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, GRID-1, GRID-1);
planeGeo.rotateX(-Math.PI / 2);
const posAttr = planeGeo.getAttribute('position');
const heightBuffer = new Float32Array(posAttr.count);
const colorAttr = new THREE.BufferAttribute(new Float32Array(posAttr.count * 3), 3);
planeGeo.setAttribute('color', colorAttr);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
});
const terrain = new THREE.Mesh(planeGeo, terrainMat);
terrain.castShadow = true;
terrain.receiveShadow = true;
scene.add(terrain);
function toWorldX(j) { return (j / (GRID-1) - 0.5) * TERRAIN_SIZE; }
function toWorldZ(i) { return (i / (GRID-1) - 0.5) * TERRAIN_SIZE; }
function sampleTerrainHeight(data, i, j) {
  const ci = Math.max(0, Math.min(GRID-1, Math.round(i)));
  const cj = Math.max(0, Math.min(GRID-1, Math.round(j)));
  return data[ci * GRID + cj] * MAX_HEIGHT;
}
function terrainHeightAt(data, worldX, worldZ) {
  const j = (worldX / TERRAIN_SIZE + 0.5) * (GRID-1);
  const i = (worldZ / TERRAIN_SIZE + 0.5) * (GRID-1);
  const fi = Math.max(0, Math.min(GRID-1, Math.floor(i)));
  const fj = Math.max(0, Math.min(GRID-1, Math.floor(j)));
  const ci = Math.min(fi + 1, GRID-1);
  const cj = Math.min(fj + 1, GRID-1);
  const ifrac = i - fi, jfrac = j - fj;
  const h00 = data[fi * GRID + fj];
  const h10 = data[fi * GRID + cj];
  const h01 = data[ci * GRID + fj];
  const h11 = data[ci * GRID + cj];
  return ((h00*(1-jfrac) + h10*jfrac)*(1-ifrac) + (h01*(1-jfrac) + h11*jfrac)*ifrac) * MAX_HEIGHT;
}
let currentTimeIdx = 0;
function updateTerrain(timeIdx) {
  const { revenue, users, errors } = precomputed[timeIdx];
  for (let k = 0; k < posAttr.count; k++) {
    const i = Math.floor(k / GRID), j = k % GRID;
    const idx = i * GRID + j;
    const h = revenue[idx] * MAX_HEIGHT;
    posAttr.setY(k, h);
    heightBuffer[k] = h;
    const u = users[idx];
    const e = errors[idx];
    const r = 0.15 + u * 0.25 + e * 0.55;
    const g = 0.35 + u * 0.5 - e * 0.3;
    const b = 0.12 + (1 - u) * 0.15;
    colorAttr.setXYZ(k, r, Math.max(0.05, g), Math.max(0.02, b));
  }
  posAttr.needsUpdate = true;
  colorAttr.needsUpdate = true;
  planeGeo.computeVertexNormals();
}
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const riverMaterial = new THREE.MeshBasicMaterial({ color: 0xff3311 });
const riverGlowMaterial = new THREE.MeshBasicMaterial({ color: 0xff5522, transparent: true, opacity: 0.35 });
const riverGeos = [];
function rebuildRiverGeometry(paths) {
  while (riverGroup.children.length > 0) riverGroup.remove(riverGroup.children[0]);
  riverGeos.length = 0;
  for (const path of paths) {
    if (path.length < 2) continue;
    const points = path.map(p => new THREE.Vector3(toWorldX(p.j), p.h * MAX_HEIGHT + 0.04, toWorldZ(p.i)));
    const curve = new THREE.CatmullRomCurve3(points);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 3, 0.08, 6, false);
    const tubeMesh = new THREE.Mesh(tubeGeo, riverMaterial);
    tubeMesh.renderOrder = 1;
    tubeMesh.material.depthTest = true;
    tubeMesh.material.depthWrite = true;
    riverGroup.add(tubeMesh);
    const glowGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.18, 6, false);
    const glowMesh = new THREE.Mesh(glowGeo, riverGlowMaterial);
    glowMesh.renderOrder = 0;
    glowMesh.material.depthTest = true;
    glowMesh.material.depthWrite = false;
    riverGroup.add(glowMesh);
    riverGeos.push(tubeGeo, glowGeo);
  }
}
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 2);
const particleLife = new Float32Array(PARTICLE_COUNT);
function spawnParticle(idx, timeIdx) {
  const { apiCalls } = precomputed[timeIdx];
  let bestI = 0, bestJ = 0, bestVal = 0;
  for (let attempt = 0; attempt < 30; attempt++) {
    const ti = Math.floor(Math.random() * GRID);
    const tj = Math.floor(Math.random() * GRID);
    const val = apiCalls[ti * GRID + tj];
    if (val > bestVal || Math.random() < 0.1) {
      bestI = ti; bestJ = tj; bestVal = val;
    }
  }
  const wx = toWorldX(bestJ) + (Math.random() - 0.5) * 0.6;
  const wz = toWorldZ(bestI) + (Math.random() - 0.5) * 0.6;
  const h = terrainHeightAt(precomputed[timeIdx].revenue, wx, wz);
  particlePositions[idx*3] = wx;
  particlePositions[idx*3+1] = h + 0.15 + Math.random() * 0.3;
  particlePositions[idx*3+2] = wz;
  const angle = Math.random() * Math.PI * 2;
  const speed = 0.3 + Math.random() * 1.2;
  particleVelocities[idx*2] = Math.cos(angle) * speed;
  particleVelocities[idx*2+1] = Math.sin(angle) * speed;
  particleLife[idx] = 2 + Math.random() * 5;
  particleColors[idx*3] = 0.3 + Math.random() * 0.4;
  particleColors[idx*3+1] = 0.6 + Math.random() * 0.3;
  particleColors[idx*3+2] = 0.9 + Math.random() * 0.1;
}
for (let i = 0; i < PARTICLE_COUNT; i++) {
  spawnParticle(i, 0);
  particleLife[i] = Math.random() * 5;
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.12,
  vertexColors: true,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  depthTest: true,
  transparent: true,
  opacity: 0.85,
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 2;
scene.add(particles);
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE/2 + 1, 32, 20, 128, 0x334466, 0x223355);
gridHelper.position.y = -0.01;
scene.add(gridHelper);
updateTerrain(0);
rebuildRiverGeometry(riverPaths[0]);
const bookmarks = JSON.parse(localStorage.getItem('terrainBookmarks') || '[]');
const bmContainer = document.getElementById('bookmarks');
function saveBookmark() {
  const name = `View ${bookmarks.length + 1}`;
  const bm = {
    name,
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
  };
  bookmarks.push(bm);
  localStorage.setItem('terrainBookmarks', JSON.stringify(bookmarks));
  renderBookmarks();
}
function goBookmark(idx) {
  const bm = bookmarks[idx];
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3().fromArray(bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3().fromArray(bm.target);
  const startTime = performance.now();
  const duration = 800;
  function anim(now) {
    const t = Math.min(1, (now - startTime) / duration);
    const ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
}
function deleteBookmark(idx) {
  bookmarks.splice(idx, 1);
  localStorage.setItem('terrainBookmarks', JSON.stringify(bookmarks));
  renderBookmarks();
}
function renderBookmarks() {
  const existing = bmContainer.querySelectorAll('.bm-entry');
  existing.forEach(e => e.remove());
  bookmarks.forEach((bm, i) => {
    const row = document.createElement('div');
    row.className = 'bm-entry';
    row.style.display = 'flex';
    row.style.gap = '4px';
    const goBtn = document.createElement('button');
    goBtn.textContent = bm.name;
    goBtn.onclick = () => goBookmark(i);
    const delBtn = document.createElement('button');
    delBtn.textContent = 'x';
    delBtn.style.padding = '4px 7px';
    delBtn.style.fontSize = '11px';
    delBtn.onclick = (e) => { e.stopPropagation(); deleteBookmark(i); };
    row.appendChild(goBtn);
    row.appendChild(delBtn);
    bmContainer.appendChild(row);
  });
}
document.getElementById('bm-save').onclick = saveBookmark;
renderBookmarks();
let playing = false;
let playSpeed = 1;
let lastTimeAdvance = 0;
const ADVANCE_INTERVAL = 800;
function setTime(idx) {
  currentTimeIdx = ((idx % TIME_STEPS) + TIME_STEPS) % TIME_STEPS;
  document.getElementById('time-slider').value = currentTimeIdx;
  const hrs = Math.floor(currentTimeIdx);
  document.getElementById('time-label').textContent = `${String(hrs).padStart(2,'0')}:00`;
  updateTerrain(currentTimeIdx);
  rebuildRiverGeometry(riverPaths[currentTimeIdx]);
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    if (particleLife[i] <= 0) spawnParticle(i, currentTimeIdx);
  }
}
document.getElementById('time-slider').oninput = function() {
  setTime(parseInt(this.value));
};
document.getElementById('btn-play').onclick = function() {
  playing = !playing;
  this.textContent = playing ? '⏸' : '▶';
  this.classList.toggle('active', playing);
};
document.getElementById('btn-speed').onclick = function() {
  const speeds = [0.5, 1, 2, 4];
  const idx = speeds.indexOf(playSpeed);
  playSpeed = speeds[(idx + 1) % speeds.length];
  this.textContent = playSpeed + 'x';
};
let autoRotate = false;
document.getElementById('btn-auto-rotate').onclick = function() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  controls.autoRotateSpeed = 0.6;
  this.classList.toggle('active', autoRotate);
};
document.getElementById('btn-top').onclick = function() {
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(0, 16, 0.5);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(0, 1.5, 0);
  const t0 = performance.now();
  function anim(now) {
    const t = Math.min(1, (now - t0) / 700);
    const e = t<0.5?2*t*t:-1+(4-2*t)*t;
    camera.position.lerpVectors(startPos, endPos, e);
    controls.target.lerpVectors(startTarget, endTarget, e);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
};
document.getElementById('btn-front').onclick = function() {
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(0, 4, 16);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(0, 1.5, 0);
  const t0 = performance.now();
  function anim(now) {
    const t = Math.min(1, (now - t0) / 700);
    const e = t<0.5?2*t*t:-1+(4-2*t)*t;
    camera.position.lerpVectors(startPos, endPos, e);
    controls.target.lerpVectors(startTarget, endTarget, e);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
};
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
let fpsFrames = 0;
let fpsTime = performance.now();
const statsEl = document.getElementById('stats');
function animate(timestamp) {
  requestAnimationFrame(animate);
  const dt = Math.min(0.1, (timestamp - (animate._prev || timestamp)) / 1000);
  animate._prev = timestamp;
  if (playing && timestamp - lastTimeAdvance > ADVANCE_INTERVAL / playSpeed) {
    lastTimeAdvance = timestamp;
    setTime(currentTimeIdx + 1);
  }
  controls.update();
  const { revenue } = precomputed[currentTimeIdx];
  const posArr = particleGeo.attributes.position.array;
  const colArr = particleGeo.attributes.color.array;
  const velArr = particleVelocities;
  const lifeArr = particleLife;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    lifeArr[i] -= dt;
    if (lifeArr[i] <= 0) {
      spawnParticle(i, currentTimeIdx);
      posArr[i*3] = particlePositions[i*3];
      posArr[i*3+1] = particlePositions[i*3+1];
      posArr[i*3+2] = particlePositions[i*3+2];
      colArr[i*3] = particleColors[i*3];
      colArr[i*3+1] = particleColors[i*3+1];
      colArr[i*3+2] = particleColors[i*3+2];
      continue;
    }
    const wx = posArr[i*3] + velArr[i*2] * dt;
    const wz = posArr[i*3+2] + velArr[i*2+1] * dt;
    if (Math.abs(wx) > TERRAIN_SIZE/2 + 1 || Math.abs(wz) > TERRAIN_SIZE/2 + 1) {
      lifeArr[i] = 0;
      continue;
    }
    const j = (wx / TERRAIN_SIZE + 0.5) * (GRID-1);
    const iv = (wz / TERRAIN_SIZE + 0.5) * (GRID-1);
    const h = terrainHeightAt(revenue, wx, wz);
    posArr[i*3] = wx;
    posArr[i*3+1] = h + 0.15;
    posArr[i*3+2] = wz;
    const ci = Math.max(0, Math.min(GRID-1, Math.round(iv)));
    const cj = Math.max(0, Math.min(GRID-1, Math.round(j)));
    const gradI = (sampleTerrainHeight(revenue, ci+1, cj) - sampleTerrainHeight(revenue, ci-1, cj)) / 2;
    const gradJ = (sampleTerrainHeight(revenue, ci, cj+1) - sampleTerrainHeight(revenue, ci, cj-1)) / 2;
    const gradMag = Math.sqrt(gradI*gradI + gradJ*gradJ) + 0.01;
    const steerStrength = 0.6;
    velArr[i*2] += (-gradJ / gradMag * steerStrength - velArr[i*2] * 0.3) * dt;
    velArr[i*2+1] += (-gradI / gradMag * steerStrength - velArr[i*2+1] * 0.3) * dt;
    const speed = Math.sqrt(velArr[i*2]*velArr[i*2] + velArr[i*2+1]*velArr[i*2+1]);
    const maxSpeed = 1.5;
    if (speed > maxSpeed) {
      velArr[i*2] *= maxSpeed / speed;
      velArr[i*2+1] *= maxSpeed / speed;
    }
    if (speed < 0.2) {
      velArr[i*2] *= 0.2 / speed;
      velArr[i*2+1] *= 0.2 / speed;
    }
    const fadeRatio = Math.min(1, lifeArr[i] / 0.8);
    colArr[i*3] = 0.2 + fadeRatio * 0.3;
    colArr[i*3+1] = 0.5 + fadeRatio * 0.3;
    colArr[i*3+2] = 0.8 + fadeRatio * 0.2;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
  fpsFrames++;
  if (timestamp - fpsTime >= 500) {
    const fps = Math.round(fpsFrames / ((timestamp - fpsTime) / 1000));
    statsEl.textContent = `FPS: ${fps}`;
    fpsFrames = 0;
    fpsTime = timestamp;
  }
  renderer.render(scene, camera);
}
animate._prev = performance.now();
requestAnimationFrame(animate);
</script>
</body>
</html>