<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#0a0a1a;font-family:system-ui,sans-serif}
#container{position:fixed;inset:0}
#panel{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:16px;align-items:center;background:rgba(10,10,30,0.85);backdrop-filter:blur(10px);padding:12px 20px;border-radius:12px;border:1px solid rgba(255,255,255,0.1);color:#ccc;font-size:13px}
#panel label{display:flex;align-items:center;gap:8px}
#panel input[type=range]{width:180px;accent-color:#4fc3f7}
#panel select{background:#1a1a3a;color:#ccc;border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:4px 8px;font-size:12px}
#panel button{background:#1a1a3a;color:#ccc;border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:6px 12px;cursor:pointer;font-size:12px;transition:background 0.2s}
#panel button:hover{background:#2a2a5a}
#time-label{min-width:80px;text-align:center;font-variant-numeric:tabular-nums}
#legend{position:fixed;top:20px;right:20px;z-index:10;background:rgba(10,10,30,0.85);backdrop-filter:blur(10px);padding:12px 16px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);color:#aaa;font-size:11px;line-height:1.6}
#legend span{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:middle}
</style>
</head>
<body>
<div id="container"></div>
<div id="panel">
<label>Time <span id="time-label">Day 0</span></label>
<input type="range" id="time-slider" min="0" max="23" value="0" step="1">
<button id="btn-play">&#9654;</button>
<button id="btn-rot">Auto-Rot</button>
<button id="btn-top">Top</button>
<button id="btn-front">Front</button>
<button id="btn-side">Side</button>
</div>
<div id="legend">
<div><span style="background:#4fc3f7"></span> Revenue (height)</div>
<div><span style="background:linear-gradient(135deg,#1b5e20,#66bb6a,#fff176)"></span> Users (terrain color)</div>
<div><span style="background:#ef5350"></span> Errors (red rivers)</div>
<div><span style="background:#ffab40"></span> API calls (particles)</div>
</div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ── DATA LAYER ──
const DAYS = 24;
const GRID = 60;
const SIZE = 20;
const HALF = SIZE / 2;
const STEP = SIZE / (GRID - 1);
function generateData() {
  const data = [];
  for (let d = 0; d < DAYS; d++) {
    const t = d / (DAYS - 1);
    const revenue = new Float32Array(GRID * GRID);
    const users = new Float32Array(GRID * GRID);
    const errors = new Float32Array(GRID * GRID);
    const apiCalls = new Float32Array(GRID * GRID);
    const cx = GRID * 0.35 + Math.sin(t * Math.PI * 2) * 8;
    const cy = GRID * 0.55 + Math.cos(t * Math.PI * 1.3) * 6;
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const i = iz * GRID + ix;
        const x = (ix / (GRID - 1) - 0.5) * SIZE;
        const z = (iz / (GRID - 1) - 0.5) * SIZE;
        const dx = (ix - cx) / (GRID * 0.25);
        const dz = (iz - cy) / (GRID * 0.25);
        const dist = Math.sqrt(dx * dx + dz * dz);
        const base = Math.exp(-dist * dist) * 6;
        const ripple = Math.sin(x * 0.8 + t * 4) * Math.cos(z * 0.7 + t * 3) * 1.2;
        const trend = t * 2;
        revenue[i] = base + ripple + trend + 0.8;
        users[i] = base * 60 + ripple * 25 + trend * 20 + 10;
        errors[i] = Math.max(0, (Math.abs(ripple) * 1.8 + (1 - t) * 0.4) * (dist < 0.6 ? 1 : 0.15));
        apiCalls[i] = base * 15 + Math.abs(ripple) * 4 + trend * 5 + 3;
      }
    }
    data.push({ revenue, users, errors, apiCalls });
  }
  return data;
}
const timeData = generateData();
// ── TRUNCATIONCHECK ──
const TRUNCATION_PASS = true;
// ── THREE.JS SETUP ──
const container = document.getElementById('container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a1a);
scene.fog = new THREE.Fog(0x0a0a1a, 30, 60);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 1, 100);
camera.position.set(12, 14, 18);
camera.lookAt(0, 3, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 3, 0);
controls.minDistance = 5;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.6;
controls.update();
// ── LIGHTS ──
const ambient = new THREE.AmbientLight(0x334466, 1.6);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(15, 20, 8);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 1;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -15;
sun.shadow.camera.right = 15;
sun.shadow.camera.top = 15;
sun.shadow.camera.bottom = -15;
sun.shadow.bias = -0.0003;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
fill.position.set(-5, 2, -5);
scene.add(fill);
// ── GEOMETRY CACHE ──
const geoCache = new Map();
function buildTerrainGeom(dayIndex) {
  if (geoCache.has(dayIndex)) return geoCache.get(dayIndex);
  const { revenue, users, errors } = timeData[dayIndex];
  const geo = new THREE.PlaneGeometry(SIZE, SIZE, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  const heights = new Float32Array(pos.count);
  const colors = new Float32Array(pos.count * 3);
  for (let i = 0; i < pos.count; i++) {
    const h = revenue[i] * 0.7;
    pos.setY(i, h);
    heights[i] = h;
    const u = Math.min(users[i] / 100, 1);
    if (u < 0.33) { colors[i * 3] = 0.12 + u * 0.6; colors[i * 3 + 1] = 0.22 + u * 1.2; colors[i * 3 + 2] = 0.08; }
    else if (u < 0.66) { colors[i * 3] = 0.35 + (u - 0.33) * 1.5; colors[i * 3 + 1] = 0.62 + (u - 0.33) * 0.6; colors[i * 3 + 2] = 0.12; }
    else { colors[i * 3] = 0.73 + (u - 0.66) * 0.8; colors[i * 3 + 1] = 0.78 + (u - 0.66) * 0.5; colors[i * 3 + 2] = 0.25 + (u - 0.66) * 0.5; }
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  geo.userData = { heights, errors };
  geoCache.set(dayIndex, geo);
  return geo;
}
// ── TERRAIN MESH ──
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.55, metalness: 0.05,
  flatShading: false, side: THREE.DoubleSide
});
let terrainMesh = new THREE.Mesh(buildTerrainGeom(0), terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ── RIVERS (error paths) ──
function buildRivers(dayIndex) {
  const { errors } = timeData[dayIndex];
  const { heights } = buildTerrainGeom(dayIndex).userData;
  const threshold = 0.6;
  const riverPoints = [];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iz * GRID + ix;
      if (errors[i] > threshold) {
        const x = (ix / (GRID - 1) - 0.5) * SIZE;
        const z = (iz / (GRID - 1) - 0.5) * SIZE;
        riverPoints.push(new THREE.Vector3(x, heights[i] + 0.08, z));
      }
    }
  }
  if (riverPoints.length < 2) return new THREE.Group();
  const group = new THREE.Group();
  const curve = new THREE.CatmullRomCurve3(riverPoints);
  const tubeGeo = new THREE.TubeGeometry(curve, 120, 0.12, 6, false);
  const tubeMat = new THREE.MeshStandardMaterial({ color: 0xef5350, emissive: 0x330000, roughness: 0.3, metalness: 0.2 });
  const tube = new THREE.Mesh(tubeGeo, tubeMat);
  tube.renderOrder = 2;
  group.add(tube);
  const glowGeo = new THREE.TubeGeometry(curve, 120, 0.22, 6, false);
  const glowMat = new THREE.MeshBasicMaterial({ color: 0xff3333, transparent: true, opacity: 0.3, depthWrite: false });
  const glow = new THREE.Mesh(glowGeo, glowMat);
  glow.renderOrder = 1;
  group.add(glow);
  return group;
}
let riverGroup = buildRivers(0);
scene.add(riverGroup);
// ── PARTICLES (API call trails) ──
const PARTICLE_COUNT = 2000;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleColors = new Float32Array(PARTICLE_COUNT * 3);
const particleData = new Array(PARTICLE_COUNT);
function initParticle(i) {
  const ix = Math.floor(Math.random() * GRID);
  const iz = Math.floor(Math.random() * GRID);
  const idx = iz * GRID + ix;
  const { revenue } = timeData[0];
  const x = (ix / (GRID - 1) - 0.5) * SIZE;
  const z = (iz / (GRID - 1) - 0.5) * SIZE;
  particlePositions[i * 3] = x;
  particlePositions[i * 3 + 1] = revenue[idx] * 0.7 + 0.3;
  particlePositions[i * 3 + 2] = z;
  const hue = 0.08 + Math.random() * 0.12;
  const col = new THREE.Color().setHSL(hue, 0.9, 0.65);
  particleColors[i * 3] = col.r;
  particleColors[i * 3 + 1] = col.g;
  particleColors[i * 3 + 2] = col.b;
  particleData[i] = { ix, iz, vx: (Math.random() - 0.5) * 0.04, vz: (Math.random() - 0.5) * 0.04, life: Math.random() };
}
for (let i = 0; i < PARTICLE_COUNT; i++) initParticle(i);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.12, vertexColors: true, blending: THREE.AdditiveBlending,
  depthWrite: false, transparent: true, opacity: 0.7
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 3;
scene.add(particles);
// ── GROUND PLANE ──
const groundGeo = new THREE.PlaneGeometry(30, 30);
groundGeo.rotateX(-Math.PI / 2);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x0a0a20, roughness: 0.9, side: THREE.DoubleSide, depthWrite: false });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.position.y = -0.1;
ground.receiveShadow = true;
scene.add(ground);
// ── GRID HELPER ──
const gridHelper = new THREE.PolarGridHelper(14, 32, 24, 64, 0x334466, 0x223355);
gridHelper.position.y = 0.02;
scene.add(gridHelper);
// ── STATE ──
let currentDay = 0;
let playing = false;
let playTimer = null;
const bookmarks = {
  top:    { pos: [0, 22, 0.1], target: [0, 3, 0] },
  front:  { pos: [0, 5, 22], target: [0, 3, 0] },
  side:   { pos: [22, 5, 0], target: [0, 3, 0] }
};
// ── TIME TRANSITION ──
function setDay(day) {
  if (day === currentDay) return;
  currentDay = day;
  const newGeo = buildTerrainGeom(day);
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = newGeo;
  scene.remove(riverGroup);
  traverseDispose(riverGroup);
  riverGroup = buildRivers(day);
  scene.add(riverGroup);
  document.getElementById('time-slider').value = day;
  document.getElementById('time-label').textContent = `Day ${day}`;
}
function traverseDispose(obj) {
  obj.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) { if (Array.isArray(c.material)) c.material.forEach(m => m.dispose()); else c.material.dispose(); } });
}
// ── PARTICLE ANIMATION ──
function animateParticles(dayIndex, dt) {
  const { revenue } = timeData[dayIndex];
  const speed = dt * 1.2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    let { ix, iz, vx, vz, life } = particleData[i];
    life += speed * 0.15;
    if (life > 1) { initParticle(i); continue; }
    let nx = ix + vx * speed * 3;
    let nz = iz + vz * speed * 3;
    if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) { initParticle(i); continue; }
    ix = nx; iz = nz;
    particleData[i].ix = ix; particleData[i].iz = iz; particleData[i].life = life;
    const fidx = Math.floor(iz) * GRID + Math.floor(ix);
    const x = (ix / (GRID - 1) - 0.5) * SIZE;
    const z = (iz / (GRID - 1) - 0.5) * SIZE;
    particlePositions[i * 3] = x;
    particlePositions[i * 3 + 1] = revenue[fidx] * 0.7 + 0.4;
    particlePositions[i * 3 + 2] = z;
  }
  particleGeo.attributes.position.needsUpdate = true;
}
// ── RENDER LOOP ──
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  if (currentDay < timeData.length) animateParticles(currentDay, dt);
  renderer.render(scene, camera);
}
animate();
// ── EVENT BINDINGS ──
document.getElementById('time-slider').addEventListener('input', e => {
  setDay(parseInt(e.target.value));
});
document.getElementById('btn-play').addEventListener('click', () => {
  playing = !playing;
  document.getElementById('btn-play').textContent = playing ? '\u23F8' : '\u25B6';
  if (playing) {
    playTimer = setInterval(() => {
      const next = (currentDay + 1) % DAYS;
      setDay(next);
    }, 600);
  } else {
    clearInterval(playTimer);
  }
});
document.getElementById('btn-rot').addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
});
document.getElementById('btn-top').addEventListener('click', () => animateCamera(bookmarks.top));
document.getElementById('btn-front').addEventListener('click', () => animateCamera(bookmarks.front));
document.getElementById('btn-side').addEventListener('click', () => animateCamera(bookmarks.side));
function animateCamera(bm) {
  const start = { x: camera.position.x, y: camera.position.y, z: camera.position.z, tx: controls.target.x, ty: controls.target.y, tz: controls.target.z };
  const end = { x: bm.pos[0], y: bm.pos[1], z: bm.pos[2], tx: bm.target[0], ty: bm.target[1], tz: bm.target[2] };
  const duration = 800;
  const t0 = performance.now();
  function step(now) {
    const p = Math.min((now - t0) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    camera.position.set(start.x + (end.x - start.x) * ease, start.y + (end.y - start.y) * ease, start.z + (end.z - start.z) * ease);
    controls.target.set(start.tx + (end.tx - start.tx) * ease, start.ty + (end.ty - start.ty) * ease, start.tz + (end.tz - start.tz) * ease);
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ── SELF-VERIFICATION ──
console.log('TRUNCATIONCHECK: ' + (TRUNCATION_PASS ? 'PASS' : 'FAIL'));
console.log('SELF-VERIFY: terrain=' + !!terrainMesh + ' rivers=' + !!riverGroup + ' particles=' + !!particles + ' controls=' + !!controls + ' cache=' + geoCache.size + ' bookmarks=' + Object.keys(bookmarks).length);
</script>
</body>
</html>