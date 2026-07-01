<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8ccd4}
  canvas{display:block}
  #ui{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:10}
  #ui>*{pointer-events:auto}
  #title{position:absolute;top:20px;left:24px;font-size:22px;font-weight:600;letter-spacing:0.5px;color:#e8ecf0;text-shadow:0 2px 8px rgba(0,0,0,0.6)}
  #title span{font-weight:300;color:#7eb8da;font-size:14px;display:block;margin-top:2px}
  #legend{position:absolute;bottom:100px;right:20px;background:rgba(10,10,20,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:14px 16px;font-size:12px;line-height:1.7;backdrop-filter:blur(8px)}
  .leg-item{display:flex;align-items:center;gap:8px;margin:3px 0}
  .leg-swatch{width:14px;height:14px;border-radius:3px;flex-shrink:0}
  #bookmarks{position:absolute;top:100px;right:20px;display:flex;flex-direction:column;gap:6px}
  .bm-btn{background:rgba(10,10,20,0.8);border:1px solid rgba(255,255,255,0.15);color:#c8ccd4;padding:7px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.2s;backdrop-filter:blur(8px);text-align:left}
  .bm-btn:hover{background:rgba(40,60,100,0.6);border-color:rgba(126,184,218,0.5);color:#fff}
  #controls{position:absolute;bottom:60px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:16px;background:rgba(10,10,20,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:12px 20px;backdrop-filter:blur(8px)}
  #time-label{font-size:13px;color:#7eb8da;min-width:110px;text-align:center;font-variant-numeric:tabular-nums}
  #time-slider{-webkit-appearance:none;width:240px;height:6px;border-radius:3px;background:linear-gradient(90deg,#1a3a5c,#7eb8da,#1a3a5c);outline:none;cursor:pointer}
  #time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#e8ecf0;border:2px solid #7eb8da;cursor:pointer;box-shadow:0 0 12px rgba(126,184,218,0.5)}
  #auto-rotate{background:rgba(10,10,20,0.8);border:1px solid rgba(255,255,255,0.2);color:#c8ccd4;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.2s}
  #auto-rotate.active{background:rgba(126,184,218,0.3);border-color:#7eb8da;color:#fff}
  #tooltip{position:absolute;background:rgba(10,10,20,0.9);border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:8px 12px;font-size:11px;display:none;pointer-events:none;line-height:1.5}
  @media(max-width:768px){
    #legend{display:none}
    #bookmarks{top:70px;right:8px;gap:4px}
    .bm-btn{padding:5px 10px;font-size:11px}
    #controls{padding:10px 14px;gap:10px}
    #time-slider{width:140px}
  }
</style>
</head>
<body>
<div id="ui">
  <div id="title">Data Terrain<span>Revenue elevation · User density vegetation · Error rivers · API particle flows</span></div>
  <div id="bookmarks">
    <button class="bm-btn" data-view="overview">Overview</button>
    <button class="bm-btn" data-view="topdown">Top-Down</button>
    <button class="bm-btn" data-view="canyon">Canyon Flyby</button>
    <button class="bm-btn" data-view="peak">Peak Closeup</button>
  </div>
  <div id="legend">
    <div style="font-weight:600;margin-bottom:6px;color:#e8ecf0">Legend</div>
    <div class="leg-item"><div class="leg-swatch" style="background:linear-gradient(135deg,#1a4d2e,#6db341,#d4a832)"></div>User density</div>
    <div class="leg-item"><div class="leg-swatch" style="background:#d64545"></div>Error rivers</div>
    <div class="leg-item"><div class="leg-swatch" style="background:#f0c060"></div>API call flows</div>
    <div class="leg-item"><div class="leg-swatch" style="background:linear-gradient(180deg,#1a3a5c,#7eb8da)"></div>Revenue height</div>
  </div>
  <div id="controls">
    <span id="time-label">Hour 12 / 24</span>
    <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
    <button id="auto-rotate" class="active">Auto-Rotate</button>
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
const GRID = 100;
const TIME_STEPS = 24;
const TERRAIN_SPAN = 20;
const HEIGHT_SCALE = 4.0;
const RIVER_THRESHOLD = 0.65;
const PARTICLE_COUNT = 600;
const PARTICLE_PATHS = 20;
const COLOR_VEG_LOW = new THREE.Color('#1a4d2e');
const COLOR_VEG_MID = new THREE.Color('#6db341');
const COLOR_VEG_HIGH = new THREE.Color('#d4a832');
const COLOR_RIVER = new THREE.Color('#d64545');
const COLOR_PARTICLE = new THREE.Color('#f0c060');
const BOOKMARKS = {
  overview: { pos: [22, 18, 22], tgt: [0, 0, 0] },
  topdown: { pos: [0, 28, 0.5], tgt: [0, 0, 0] },
  canyon: { pos: [4, 3, -8], tgt: [2, -0.5, 4] },
  peak: { pos: [-8, 6, 6], tgt: [-3, 1.5, -2] }
};
function lerp(a, b, t) { return a + (b - a) * t; }
function fract(x) { return x - Math.floor(x); }
function hash2D(x, y) {
  let h = x * 374761393 + y * 668265263 + 1274126177;
  h = (h ^ (h >> 13)) * 1274126177;
  return (h ^ (h >> 16)) / 2147483648 + 0.5;
}
function smoothNoise(x, y) {
  const ix = Math.floor(x), iy = Math.floor(y);
  const fx = x - ix, fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
  const n00 = hash2D(ix, iy), n10 = hash2D(ix + 1, iy);
  const n01 = hash2D(ix, iy + 1), n11 = hash2D(ix + 1, iy + 1);
  return lerp(lerp(n00, n10, sx), lerp(n01, n11, sx), sy);
}
function fbm(x, y, octaves = 4) {
  let v = 0, amp = 0.6, freq = 1.0, total = 0;
  for (let i = 0; i < octaves; i++) {
    v += amp * smoothNoise(x * freq, y * freq);
    total += amp;
    amp *= 0.5;
    freq *= 2.0;
  }
  return v / total;
}
const heightMaps = new Array(TIME_STEPS);
const userMaps = new Array(TIME_STEPS);
const errorMaps = new Array(TIME_STEPS);
const apiMaps = new Array(TIME_STEPS);
for (let t = 0; t < TIME_STEPS; t++) {
  const phase = t / TIME_STEPS;
  const hm = new Float32Array(GRID * GRID);
  const um = new Float32Array(GRID * GRID);
  const em = new Float32Array(GRID * GRID);
  const am = new Float32Array(GRID * GRID);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iy * GRID + ix;
      const nx = ix / GRID, ny = iy / GRID;
      const warp = Math.sin(phase * Math.PI * 2) * 0.3;
      let h = fbm(nx * 5 + warp, ny * 5 - warp * 0.7, 5);
      h += 0.25 * Math.sin(nx * 8 + phase * 3) * Math.cos(ny * 6 - phase * 2);
      h += 0.15 * Math.exp(-((nx - 0.5) ** 2 + (ny - 0.5) ** 2) * 8);
      h = (h + 0.5) * 0.5;
      hm[idx] = Math.max(0, Math.min(1, h));
      let u = fbm(nx * 4 + 1.7 + warp * 0.5, ny * 4 - 0.3 + warp * 0.6, 4);
      u = (u + 0.5) * 0.5;
      u = u * 0.6 + hm[idx] * 0.4;
      um[idx] = Math.max(0, Math.min(1, u));
      let e = 0;
      const distFromPeak = Math.sqrt((nx - 0.55) ** 2 + (ny - 0.45) ** 2);
      if (distFromPeak < 0.35) {
        e = (1 - distFromPeak / 0.35) * 0.7;
        e += smoothNoise(nx * 12 + phase, ny * 12 - phase) * 0.3;
      }
      const dist2 = Math.sqrt((nx - 0.75) ** 2 + (ny - 0.25) ** 2);
      if (dist2 < 0.2) {
        e = Math.max(e, (1 - dist2 / 0.2) * 0.5);
      }
      e *= 0.5 + 0.5 * Math.sin(phase * Math.PI * 3);
      em[idx] = Math.max(0, Math.min(1, e));
      let a = fbm(nx * 6 + 3.3 + warp, ny * 6 + 1.1 - warp, 3);
      a = (a + 0.5) * 0.5;
      a = a * 0.35 + hm[idx] * 0.2 + um[idx] * 0.45;
      am[idx] = Math.max(0, Math.min(1, a));
    }
  }
  heightMaps[t] = hm;
  userMaps[t] = um;
  errorMaps[t] = em;
  apiMaps[t] = am;
}
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 25, 60);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(22, 18, 22);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
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
controls.autoRotate = true;
controls.autoRotateSpeed = 0.35;
controls.target.set(0, 0, 0);
controls.minDistance = 3;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
const ambient = new THREE.AmbientLight('#3a4a6a', 1.4);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffeedd', 3.5);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -18;
sun.shadow.camera.right = 18;
sun.shadow.camera.top = 18;
sun.shadow.camera.bottom = -18;
sun.shadow.bias = -0.0003;
scene.add(sun);
const fill = new THREE.DirectionalLight('#4466aa', 1.0);
fill.position.set(-8, 3, -8);
scene.add(fill);
const groundGeo = new THREE.PlaneGeometry(TERRAIN_SPAN * 1.5, TERRAIN_SPAN * 1.5);
const groundMat = new THREE.MeshStandardMaterial({ color: '#141428', roughness: 0.9, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.3;
ground.receiveShadow = true;
scene.add(ground);
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SPAN / 2, 40, 20, 64, '#1a1a3a', '#1a1a3a');
gridHelper.position.y = -0.28;
scene.add(gridHelper);
const terrainGeo = new THREE.PlaneGeometry(TERRAIN_SPAN, TERRAIN_SPAN, GRID - 1, GRID - 1);
terrainGeo.rotateX(-Math.PI / 2);
const positions = terrainGeo.attributes.position;
const colorsArr = new Float32Array(positions.count * 3);
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
function updateTerrain(timeIndex) {
  const hm = heightMaps[timeIndex];
  const um = userMaps[timeIndex];
  const pos = positions.array;
  const col = colorsArr;
  for (let i = 0; i < positions.count; i++) {
    const idx3 = i * 3;
    const colI = idx3;
    const gx = (pos[idx3] / TERRAIN_SPAN) * 0.5 + 0.5;
    const gy = (pos[idx3 + 2] / TERRAIN_SPAN) * 0.5 + 0.5;
    const ix = Math.min(GRID - 1, Math.max(0, Math.floor(gx * GRID)));
    const iy = Math.min(GRID - 1, Math.max(0, Math.floor(gy * GRID)));
    const di = iy * GRID + ix;
    const h = hm[di];
    const u = um[di];
    pos[idx3 + 1] = h * HEIGHT_SCALE;
    const vegColor = new THREE.Color();
    if (u < 0.5) vegColor.copy(COLOR_VEG_LOW).lerp(COLOR_VEG_MID, u * 2);
    else vegColor.copy(COLOR_VEG_MID).lerp(COLOR_VEG_HIGH, (u - 0.5) * 2);
    const heightTint = 0.75 + h * 0.25;
    col[colI] = vegColor.r * heightTint;
    col[colI + 1] = vegColor.g * heightTint;
    col[colI + 2] = vegColor.b * heightTint;
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
}
updateTerrain(12);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
});
const terrain = new THREE.Mesh(terrainGeo, terrainMat);
terrain.castShadow = true;
terrain.receiveShadow = true;
scene.add(terrain);
const RIVER_SEGMENTS = 40;
const riverGroup = new THREE.Group();
scene.add(riverGroup);
function buildRivers(timeIndex) {
  while (riverGroup.children.length > 0) riverGroup.remove(riverGroup.children[0]);
  const em = errorMaps[timeIndex];
  const hm = heightMaps[timeIndex];
  const sources = [];
  for (let iy = 1; iy < GRID - 1; iy++) {
    for (let ix = 1; ix < GRID - 1; ix++) {
      const idx = iy * GRID + ix;
      if (em[idx] > RIVER_THRESHOLD) sources.push({ ix, iy, val: em[idx] });
    }
  }
  sources.sort((a, b) => b.val - a.val);
  const topSources = sources.slice(0, 25);
  const material = new THREE.LineBasicMaterial({
    color: COLOR_RIVER,
    linewidth: 1,
    transparent: true,
    opacity: 0.8,
    depthTest: true,
  });
  const RIVER_OFFSET = 0.12;
  for (const src of topSources) {
    const points = [];
    let cx = src.ix, cy = src.iy;
    for (let s = 0; s < RIVER_SEGMENTS; s++) {
      if (cx < 1 || cx >= GRID - 1 || cy < 1 || cy >= GRID - 1) break;
      const idx = cy * GRID + cx;
      const worldX = (cx / GRID - 0.5) * TERRAIN_SPAN;
      const worldZ = (cy / GRID - 0.5) * TERRAIN_SPAN;
      const worldY = hm[idx] * HEIGHT_SCALE + RIVER_OFFSET;
      points.push(new THREE.Vector3(worldX, worldY, worldZ));
      let bestDx = 0, bestDy = 0, bestDrop = -Infinity;
      for (const [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, -1], [-1, 1], [1, 1]]) {
        const nx = cx + dx, ny = cy + dy;
        if (nx < 0 || nx >= GRID || ny < 0 || ny >= GRID) continue;
        const ni = ny * GRID + nx;
        const drop = hm[idx] - hm[ni];
        if (drop > bestDrop) { bestDrop = drop; bestDx = dx; bestDy = dy; }
      }
      if (bestDrop <= 0) break;
      cx += bestDx;
      cy += bestDy;
    }
    if (points.length < 2) continue;
    const geo = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geo, material);
    line.renderOrder = 1;
    riverGroup.add(line);
  }
}
buildRivers(12);
const particleGroup = new THREE.Group();
scene.add(particleGroup);
const particlePathsData = [];
function generateParticlePaths(timeIndex) {
  const am = apiMaps[timeIndex];
  const hm = heightMaps[timeIndex];
  particlePathsData.length = 0;
  const hubs = [];
  const threshold = 0.55;
  for (let iy = 5; iy < GRID - 5; iy += 10) {
    for (let ix = 5; ix < GRID - 5; ix += 10) {
      const idx = iy * GRID + ix;
      if (am[idx] > threshold) {
        hubs.push({
          ix, iy,
          val: am[idx],
          wx: (ix / GRID - 0.5) * TERRAIN_SPAN,
          wz: (iy / GRID - 0.5) * TERRAIN_SPAN,
          wy: hm[idx] * HEIGHT_SCALE
        });
      }
    }
  }
  for (let i = 0; i < Math.min(PARTICLE_PATHS, hubs.length - 1); i++) {
    const from = hubs[i];
    const to = hubs[(i + 1) % hubs.length];
    const steps = 80;
    const path = [];
    for (let s = 0; s <= steps; s++) {
      const t = s / steps;
      const wx = lerp(from.wx, to.wx, t);
      const wz = lerp(from.wz, to.wz, t);
      const gx = Math.min(GRID - 1, Math.max(0, Math.round((wx / TERRAIN_SPAN + 0.5) * GRID)));
      const gy = Math.min(GRID - 1, Math.max(0, Math.round((wz / TERRAIN_SPAN + 0.5) * GRID)));
      const hi = gy * GRID + gx;
      const wy = hm[hi] * HEIGHT_SCALE + 0.15;
      path.push(new THREE.Vector3(wx, wy, wz));
    }
    particlePathsData.push({ path, fromVal: from.val, toVal: to.val });
  }
}
function buildParticles() {
  while (particleGroup.children.length > 0) particleGroup.remove(particleGroup.children[0]);
  if (particlePathsData.length === 0) return;
  const particlesPerPath = Math.floor(PARTICLE_COUNT / particlePathsData.length);
  for (const pathData of particlePathsData) {
    const geo = new THREE.BufferGeometry();
    const posArr = new Float32Array(particlesPerPath * 3);
    const progArr = new Float32Array(particlesPerPath);
    const speedArr = new Float32Array(particlesPerPath);
    for (let p = 0; p < particlesPerPath; p++) {
      const prog = Math.random();
      progArr[p] = prog;
      speedArr[p] = 0.0008 + Math.random() * 0.0025;
      const idx = Math.floor(prog * (pathData.path.length - 1));
      const frac = prog * (pathData.path.length - 1) - idx;
      const nextIdx = Math.min(idx + 1, pathData.path.length - 1);
      const pt = pathData.path[idx].clone().lerp(pathData.path[nextIdx], frac);
      posArr[p * 3] = pt.x;
      posArr[p * 3 + 1] = pt.y;
      posArr[p * 3 + 2] = pt.z;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(posArr, 3));
    geo.userData = { progress: progArr, speeds: speedArr, path: pathData.path };
    const mat = new THREE.PointsMaterial({
      color: COLOR_PARTICLE,
      size: 0.08,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.7,
    });
    const points = new THREE.Points(geo, mat);
    points.renderOrder = 2;
    particleGroup.add(points);
  }
}
generateParticlePaths(12);
buildParticles();
const starGeo = new THREE.BufferGeometry();
const starPos = new Float32Array(400 * 3);
for (let i = 0; i < 400; i++) {
  starPos[i * 3] = (Math.random() - 0.5) * 50;
  starPos[i * 3 + 1] = 15 + Math.random() * 20;
  starPos[i * 3 + 2] = (Math.random() - 0.5) * 50;
}
starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
const starMat = new THREE.PointsMaterial({ color: '#556688', size: 0.06, transparent: true, opacity: 0.6, depthWrite: false });
const stars = new THREE.Points(starGeo, starMat);
scene.add(stars);
let currentTimeIndex = 12;
function setTime(index) {
  currentTimeIndex = index;
  updateTerrain(index);
  buildRivers(index);
  generateParticlePaths(index);
  buildParticles();
  document.getElementById('time-label').textContent = `Hour ${index} / 24`;
}
document.getElementById('time-slider').addEventListener('input', (e) => {
  setTime(parseInt(e.target.value, 10));
});
document.getElementById('auto-rotate').addEventListener('click', (e) => {
  controls.autoRotate = !controls.autoRotate;
  e.currentTarget.classList.toggle('active', controls.autoRotate);
});
document.querySelectorAll('.bm-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    const view = e.currentTarget.dataset.view;
    const bm = BOOKMARKS[view];
    if (!bm) return;
    const targetPos = new THREE.Vector3(...bm.pos);
    const targetTgt = new THREE.Vector3(...bm.tgt);
    const startPos = camera.position.clone();
    const startTgt = controls.target.clone();
    const startTime = performance.now();
    const DURATION = 1200;
    function animStep(now) {
      const elapsed = now - startTime;
      const t = Math.min(1, elapsed / DURATION);
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      camera.position.lerpVectors(startPos, targetPos, ease);
      controls.target.lerpVectors(startTgt, targetTgt, ease);
      controls.update();
      if (t < 1) requestAnimationFrame(animStep);
    }
    requestAnimationFrame(animStep);
  });
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  for (const child of particleGroup.children) {
    const geo = child.geometry;
    if (!geo.userData.progress) continue;
    const posArr = geo.attributes.position.array;
    const progArr = geo.userData.progress;
    const speedArr = geo.userData.speeds;
    const path = geo.userData.path;
    const count = progArr.length;
    for (let p = 0; p < count; p++) {
      progArr[p] += speedArr[p] * dt * 60;
      if (progArr[p] > 1) progArr[p] -= 1;
      const t = progArr[p];
      const idx = Math.floor(t * (path.length - 1));
      const frac = t * (path.length - 1) - idx;
      const nextIdx = Math.min(idx + 1, path.length - 1);
      const pt = path[idx].clone().lerp(path[nextIdx], frac);
      posArr[p * 3] = pt.x;
      posArr[p * 3 + 1] = pt.y;
      posArr[p * 3 + 2] = pt.z;
    }
    geo.attributes.position.needsUpdate = true;
  }
  stars.rotation.y += dt * 0.015;
  renderer.render(scene, camera);
}
animate();
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
renderer.domElement.addEventListener('mousemove', (e) => {
  mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrain);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const gx = (pt.x / TERRAIN_SPAN + 0.5);
    const gz = (pt.z / TERRAIN_SPAN + 0.5);
    const ix = Math.floor(gx * GRID);
    const iy = Math.floor(gz * GRID);
    if (ix >= 0 && ix < GRID && iy >= 0 && iy < GRID) {
      const idx = iy * GRID + ix;
      const hm = heightMaps[currentTimeIndex];
      const um = userMaps[currentTimeIndex];
      const em = errorMaps[currentTimeIndex];
      const am = apiMaps[currentTimeIndex];
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX + 18) + 'px';
      tooltip.style.top = (e.clientY - 10) + 'px';
      tooltip.innerHTML =
        `Revenue: ${(hm[idx] * 100).toFixed(0)}%<br>` +
        `Users: ${(um[idx] * 100).toFixed(0)}%<br>` +
        `Errors: ${(em[idx] * 100).toFixed(0)}%<br>` +
        `API load: ${(am[idx] * 100).toFixed(0)}%`;
    }
  } else {
    tooltip.style.display = 'none';
  }
});
setTime(12);
</script>
</body>
</html>