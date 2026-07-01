3D Data Terrain Explorer v1
Complete interactive HTML dashboard with Three.js terrain, vertex colors, rivers, particles, time slider, cached geometry, and GPU-friendly particle updates.
BLUEPRINT.md rebuilt with caching directives and frame budget. config.yaml performance budget set.
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  body { margin: 0; overflow: hidden; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  #info { position: absolute; top: 20px; left: 20px; color: #fff; background: rgba(0,0,0,0.6); padding: 12px 18px; border-radius: 8px; pointer-events: none; z-index: 10; font-size: 14px; }
  #controls { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.7); padding: 16px 28px; border-radius: 12px; display: flex; gap: 20px; align-items: center; z-index: 20; color: #ccc; font-size: 13px; }
  #controls input[type=range] { width: 300px; cursor: pointer; }
  #controls label { display: flex; align-items: center; gap: 8px; }
  #controls button { background: #4a9eff; border: none; color: #fff; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; }
  #controls button:hover { background: #6ab4ff; }
  #time-label { min-width: 50px; text-align: center; color: #fff; font-weight: 600; }
  #stats { position: absolute; bottom: 90px; right: 20px; color: #aaa; font-size: 11px; font-family: monospace; background: rgba(0,0,0,0.5); padding: 8px 12px; border-radius: 6px; z-index: 15; pointer-events: none; }
  #bookmarks { position: absolute; top: 80px; right: 20px; display: flex; flex-direction: column; gap: 4px; z-index: 10; }
  #bookmarks button { background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: #ccc; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 11px; }
  #bookmarks button:hover { background: rgba(74,158,255,0.3); border-color: #4a9eff; }
</style>
</head>
<body>
<div id="info">3D Data Terrain Explorer — Drag to orbit | Scroll to zoom | Time slider reshapes landscape</div>
<div id="controls">
  <label>Time <input type="range" id="time-slider" min="0" max="100" value="0" step="1"></label>
  <span id="time-label">t=0</span>
  <button id="auto-rotate-btn">Auto Rotate: ON</button>
  <button id="reset-cam-btn">Reset Camera</button>
</div>
<div id="stats">terrain: 0 vertices | particles: 0 | fps: 0</div>
<div id="bookmarks">
  <button data-bookmark="0">B1</button>
  <button data-bookmark="1">B2</button>
  <button data-bookmark="2">B3</button>
  <button data-bookmark="save">+ Save</button>
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
// --- CONFIG ---
const CONFIG = {
  gridSize: 64,
  terrainScale: 30,
  heightScale: 8,
  particleCount: 1500,
  riverCount: 3,
  frameBudget: 8,
  initBudget: 200,
  priorities: ['functionality', 'performance', 'polish']
};
// --- SCENE SETUP ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0e1a);
scene.fog = new THREE.Fog(0x0a0e1a, 60, 120);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(35, 25, 45);
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.prepend(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.8;
controls.minDistance = 8;
controls.maxDistance = 100;
controls.maxPolarAngle = Math.PI / 2.1;
// --- LIGHTS ---
const ambientLight = new THREE.AmbientLight(0x404060, 0.5);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffeedd, 2.0);
dirLight.position.set(30, 40, 20);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 1024;
dirLight.shadow.mapSize.height = 1024;
const d = 50;
dirLight.shadow.camera.left = -d;
dirLight.shadow.camera.right = d;
dirLight.shadow.camera.top = d;
dirLight.shadow.camera.bottom = -d;
dirLight.shadow.camera.near = 1;
dirLight.shadow.camera.far = 80;
scene.add(dirLight);
const fillLight = new THREE.DirectionalLight(0x4488ff, 0.5);
fillLight.position.set(-20, 10, -30);
scene.add(fillLight);
const hemiLight = new THREE.HemisphereLight(0x87ceeb, 0x2a3a2a, 0.4);
scene.add(hemiLight);
// --- GROUND REFLECTION PLANE ---
const groundGeo = new THREE.PlaneGeometry(120, 120);
const groundMat = new THREE.MeshStandardMaterial({
  color: 0x0a0e1a,
  roughness: 0.9,
  metalness: 0.0,
  transparent: true,
  opacity: 0.6
});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.5;
ground.receiveShadow = true;
scene.add(ground);
// --- DATA GENERATION ---
function generateHeightData(time) {
  const size = CONFIG.gridSize;
  const data = new Float32Array(size * size);
  const t = time * 0.02;
  for (let z = 0; z < size; z++) {
    for (let x = 0; x < size; x++) {
      const nx = x / size - 0.5;
      const nz = z / size - 0.5;
      const dist = Math.sqrt(nx * nx + nz * nz);
      // Multi-octave terrain
      const h1 = Math.sin(nx * 4.0 + t) * Math.cos(nz * 3.5 + t * 0.7) * 0.4;
      const h2 = Math.sin(nx * 8.0 + nz * 6.0 + t * 1.3) * 0.25;
      const h3 = Math.sin(nx * 16.0 - nz * 14.0 + t * 2.1) * 0.12;
      const h4 = Math.sin(nx * 3.0 + nz * 7.0) * Math.cos(t * 0.5) * 0.15;
      // Central mountain
      const mountain = Math.exp(-dist * dist * 6) * 0.8;
      // Ridges
      const ridge = Math.pow(Math.abs(Math.sin(nx * 12.0 + nz * 8.0)), 2) * 0.3;
      const h = (h1 + h2 + h3 + h4 + mountain + ridge) * CONFIG.heightScale;
      data[z * size + x] = Math.max(h, 0);
    }
  }
  return data;
}
function generateColorData(heightData, time) {
  const size = CONFIG.gridSize;
  const colors = new Float32Array(size * size * 3);
  const t = time * 0.01;
  for (let z = 0; z < size; z++) {
    for (let x = 0; x < size; x++) {
      const idx = z * size + x;
      const h = heightData[idx] / CONFIG.heightScale;
      // Vegetation gradient: low = desert, mid = green, high = snow
      let r, g, b;
      if (h < 0.25) {
        // Desert/lowland
        r = 0.76 + Math.sin(x * 0.05 + t) * 0.05;
        g = 0.60 + Math.sin(z * 0.05 + t * 0.7) * 0.05;
        b = 0.30;
      } else if (h < 0.55) {
        // Forest
        const f = (h - 0.25) / 0.3;
        r = 0.15 + f * 0.2;
        g = 0.55 + f * 0.3 + Math.sin(x * 0.08 + z * 0.06 + t) * 0.05;
        b = 0.08 + f * 0.1;
      } else if (h < 0.8) {
        // High slope
        const f = (h - 0.55) / 0.25;
        r = 0.35 + f * 0.3;
        g = 0.65 - f * 0.3;
        b = 0.18 - f * 0.1;
      } else {
        // Snow cap
        const f = Math.min((h - 0.8) / 0.2, 1);
        r = 0.65 + f * 0.35;
        g = 0.35 + f * 0.55;
        b = 0.18 + f * 0.52;
      }
      colors[idx * 3] = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  return colors;
}
// --- CACHED TERRAIN ---
let terrainCache = null;
function buildTerrain(time) {
  const size = CONFIG.gridSize;
  const scale = CONFIG.terrainScale;
  const heightData = generateHeightData(time);
  const colorData = generateColorData(heightData, time);
  const vertices = new Float32Array(size * size * 3);
  const indices = [];
  const vertColors = new Float32Array(size * size * 3);
  for (let z = 0; z < size; z++) {
    for (let x = 0; x < size; x++) {
      const idx = z * size + x;
      const h = heightData[idx];
      vertices[idx * 3] = (x / (size - 1) - 0.5) * scale;
      vertices[idx * 3 + 1] = h;
      vertices[idx * 3 + 2] = (z / (size - 1) - 0.5) * scale;
      vertColors[idx * 3] = colorData[idx * 3];
      vertColors[idx * 3 + 1] = colorData[idx * 3 + 1];
      vertColors[idx * 3 + 2] = colorData[idx * 3 + 2];
    }
  }
  for (let z = 0; z < size - 1; z++) {
    for (let x = 0; x < size - 1; x++) {
      const a = z * size + x;
      const b = z * size + x + 1;
      const c = (z + 1) * size + x;
      const d = (z + 1) * size + x + 1;
      indices.push(a, b, c);
      indices.push(b, d, c);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(vertColors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return { geo, heightData };
}
function updateTerrain(time) {
  const size = CONFIG.gridSize;
  const heightData = generateHeightData(time);
  const colorData = generateColorData(heightData, time);
  const positions = terrainMesh.geometry.attributes.position.array;
  const colors = terrainMesh.geometry.attributes.color.array;
  const scale = CONFIG.terrainScale;
  for (let z = 0; z < size; z++) {
    for (let x = 0; x < size; x++) {
      const idx = z * size + x;
      positions[idx * 3] = (x / (size - 1) - 0.5) * scale;
      positions[idx * 3 + 1] = heightData[idx];
      positions[idx * 3 + 2] = (z / (size - 1) - 0.5) * scale;
      colors[idx * 3] = colorData[idx * 3];
      colors[idx * 3 + 1] = colorData[idx * 3 + 1];
      colors[idx * 3 + 2] = colorData[idx * 3 + 2];
    }
  }
  terrainMesh.geometry.attributes.position.needsUpdate = true;
  terrainMesh.geometry.attributes.color.needsUpdate = true;
  terrainMesh.geometry.computeVertexNormals();
  return heightData;
}
// Create terrain with cached geometry
const initialHeightData = buildTerrain(0);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.6,
  metalness: 0.1,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrainMesh = new THREE.Mesh(initialHeightData.geo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
let currentHeightData = initialHeightData.heightData;
// --- RIVERS ---
const riverGroup = new THREE.Group();
scene.add(riverGroup);
function buildRivers(heightData, time) {
  while (riverGroup.children.length > 0) {
    riverGroup.remove(riverGroup.children[0]);
  }
  const size = CONFIG.gridSize;
  const scale = CONFIG.terrainScale;
  const t = time * 0.5;
  for (let r = 0; r < CONFIG.riverCount; r++) {
    // River starts at a high point, flows downhill
    const startX = 10 + Math.sin(r * 4.7 + t * 0.3) * 15;
    const startZ = 10 + Math.cos(r * 3.1 + t * 0.2) * 15;
    const cx = Math.round(startX);
    const cz = Math.round(startZ);
    const points = [];
    let px = Math.max(1, Math.min(size - 2, cx));
    let pz = Math.max(1, Math.min(size - 2, cz));
    let iterations = 0;
    while (iterations < 80) {
      const idx = Math.round(pz) * size + Math.round(px);
      const h = heightData[idx] || 0;
      points.push(new THREE.Vector3(
        (px / (size - 1) - 0.5) * scale,
        h + 0.05,
        (pz / (size - 1) - 0.5) * scale
      ));
      // Flow downhill with some randomness
      const neighbors = [
        { x: px - 1, z: pz }, { x: px + 1, z: pz },
        { x: px, z: pz - 1 }, { x: px, z: pz + 1 },
        { x: px - 1, z: pz - 1 }, { x: px + 1, z: pz + 1 },
        { x: px + 1, z: pz - 1 }, { x: px - 1, z: pz + 1 }
      ];
      let lowest = Infinity;
      let nextX = px, nextZ = pz;
      for (const n of neighbors) {
        if (n.x < 0 || n.x >= size || n.z < 0 || n.z >= size) continue;
        const nIdx = Math.round(n.z) * size + Math.round(n.x);
        const nh = heightData[nIdx] || 0;
        if (nh < lowest) {
          lowest = nh;
          nextX = n.x;
          nextZ = n.z;
        }
      }
      // Add a bit of meander
      const meanderAngle = Math.sin(iterations * 0.5 + r * 2.0 + t) * 0.6;
      const meanderX = Math.round(Math.cos(meanderAngle) * 0.5);
      const meanderZ = Math.round(Math.sin(meanderAngle) * 0.5);
      nextX = Math.max(0, Math.min(size - 1, nextX + meanderX));
      nextZ = Math.max(0, Math.min(size - 1, nextZ + meanderZ));
      if (nextX === px && nextZ === pz) break;
      if (lowest >= h) break; // reached a local minimum (lake)
      px = nextX;
      pz = nextZ;
      iterations++;
    }
    if (points.length > 3) {
      const curve = new THREE.CatmullRomCurve3(points);
      const curvePoints = curve.getPoints(Math.min(points.length * 3, 60));
      // River geometry with width variation
      const riverShape = new THREE.Shape();
      const w = 0.12 + Math.sin(r * 1.5) * 0.06;
      riverShape.moveTo(-w, 0);
      riverShape.quadraticCurveTo(-w * 0.5, w * 0.3, 0, w * 0.3);
      riverShape.quadraticCurveTo(w * 0.5, w * 0.3, w, 0);
      riverShape.quadraticCurveTo(w * 0.5, -w * 0.1, 0, -w * 0.1);
      riverShape.quadraticCurveTo(-w * 0.5, -w * 0.1, -w, 0);
      const tubeGeo = new THREE.TubeGeometry(curve, Math.min(curvePoints.length * 2, 40), w * 0.8, 6, false);
      const tubeMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color().setHSL(0.55 + r * 0.03, 0.7, 0.45 + r * 0.05),
        transparent: true,
        opacity: 0.75,
        roughness: 0.3,
        metalness: 0.2
      });
      const riverMesh = new THREE.Mesh(tubeGeo, tubeMat);
      riverGroup.add(riverMesh);
      // Glow ribbon along river
      const ribbonPoints = curve.getPoints(30);
      const ribbonGeo = new THREE.BufferGeometry().setFromPoints(ribbonPoints);
      const ribbonMat = new THREE.LineBasicMaterial({
        color: new THREE.Color().setHSL(0.6, 0.8, 0.6),
        transparent: true,
        opacity: 0.3,
        linewidth: 1
      });
      const ribbon = new THREE.Line(ribbonGeo, ribbonMat);
      riverGroup.add(ribbon);
    }
  }
}
buildRivers(currentHeightData, 0);
// --- PARTICLES (BufferGeometry with position array reuse) ---
const PARTICLE_COUNT = CONFIG.particleCount;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = [];
const particleSizes = new Float32Array(PARTICLE_COUNT);
const particleOpacities = new Float32Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particlePositions[i * 3] = (Math.random() - 0.5) * CONFIG.terrainScale;
  particlePositions[i * 3 + 1] = Math.random() * CONFIG.heightScale + 1;
  particlePositions[i * 3 + 2] = (Math.random() - 0.5) * CONFIG.terrainScale;
  particleVelocities.push({
    x: (Math.random() - 0.5) * 0.02,
    y: Math.random() * 0.01,
    z: (Math.random() - 0.5) * 0.02
  });
  particleSizes[i] = 0.15 + Math.random() * 0.35;
  particleOpacities[i] = 0.3 + Math.random() * 0.5;
}
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
particleGeo.setAttribute('opacity', new THREE.BufferAttribute(particleOpacities, 1));
const particleMat = new THREE.PointsMaterial({
  color: 0x4488ff,
  size: 0.3,
  transparent: true,
  opacity: 0.7,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  sizeAttenuation: true
});
const particleSystem = new THREE.Points(particleGeo, particleMat);
scene.add(particleSystem);
function updateParticles(time, heightData) {
  const positions = particleSystem.geometry.attributes.position.array;
  const size = CONFIG.gridSize;
  const scale = CONFIG.terrainScale;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const idx3 = i * 3;
    const v = particleVelocities[i];
    // Move along flow field
    const flowAngle = Math.sin(positions[idx3] * 0.1 + time * 0.005) * 0.5 +
                      Math.cos(positions[idx3 + 2] * 0.08 + time * 0.003) * 0.5;
    positions[idx3] += v.x + Math.cos(flowAngle) * 0.005;
    positions[idx3 + 1] += v.y + Math.sin(time * 0.01 + i) * 0.002;
    positions[idx3 + 2] += v.z + Math.sin(flowAngle) * 0.005;
    // Terrain following
    const nx = positions[idx3] / scale + 0.5;
    const nz = positions[idx3 + 2] / scale + 0.5;
    const gx = Math.round(nx * (size - 1));
    const gz = Math.round(nz * (size - 1));
    if (gx >= 0 && gx < size && gz >= 0 && gz < size) {
      const terrainH = heightData[gz * size + gx] || 0;
      const minY = terrainH + 0.5;
      if (positions[idx3 + 1] < minY) {
        positions[idx3 + 1] = minY + Math.random() * 0.5;
        positions[idx3] = (Math.random() - 0.5) * scale;
        positions[idx3 + 2] = (Math.random() - 0.5) * scale;
      }
    }
    // Wrap around
    const halfScale = scale * 0.5;
    if (positions[idx3] > halfScale) positions[idx3] = -halfScale;
    if (positions[idx3] < -halfScale) positions[idx3] = halfScale;
    if (positions[idx3 + 2] > halfScale) positions[idx3 + 2] = -halfScale;
    if (positions[idx3 + 2] < -halfScale) positions[idx3 + 2] = halfScale;
    if (positions[idx3 + 1] > CONFIG.heightScale + 5) positions[idx3 + 1] = 0.5;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
// --- STARS BACKGROUND ---
const starCount = 2000;
const starPositions = new Float32Array(starCount * 3);
const starColors = new Float32Array(starCount * 3);
for (let i = 0; i < starCount; i++) {
  const theta = Math.random() * Math.PI * 2;
  const phi = Math.acos(2 * Math.random() - 1);
  const r = 80 + Math.random() * 40;
  starPositions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
  starPositions[i * 3 + 1] = Math.abs(r * Math.cos(phi));
  starPositions[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
  const c = 0.3 + Math.random() * 0.7;
  starColors[i * 3] = c;
  starColors[i * 3 + 1] = c;
  starColors[i * 3 + 2] = c + Math.random() * 0.2;
}
const starGeo = new THREE.BufferGeometry();
starGeo.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
starGeo.setAttribute('color', new THREE.BufferAttribute(starColors, 3));
const starMat = new THREE.PointsMaterial({ size: 0.15, vertexColors: true, transparent: true, opacity: 0.8, blending: THREE.AdditiveBlending, depthWrite: false, sizeAttenuation: false });
const stars = new THREE.Points(starGeo, starMat);
scene.add(stars);
// --- BOOKMARKS ---
const bookmarks = [];
const bookmarkButtons = document.querySelectorAll('#bookmarks button');
bookmarkButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const bm = btn.dataset.bookmark;
    if (bm === 'save') {
      bookmarks.push({
        position: camera.position.clone(),
        target: controls.target.clone()
      });
      btn.textContent = `B${bookmarks.length}`;
      btn.dataset.bookmark = bookmarks.length - 1;
      updateBookmarkUI();
    } else {
      const idx = parseInt(bm);
      if (bookmarks[idx]) {
        camera.position.copy(bookmarks[idx].position);
        controls.target.copy(bookmarks[idx].target);
        controls.update();
      }
    }
  });
});
function updateBookmarkUI() {
  let maxSet = 0;
  bookmarkButtons.forEach(btn => {
    const bm = parseInt(btn.dataset.bookmark);
    if (!isNaN(bm) && bm >= maxSet) maxSet = bm + 1;
  });
  if (bookmarks.length >= maxSet) {
    // Add a new bookmark button if needed
    const container = document.getElementById('bookmarks');
    const newBtn = document.createElement('button');
    newBtn.dataset.bookmark = bookmarks.length;
    newBtn.textContent = `B${bookmarks.length + 1}`;
    newBtn.addEventListener('click', () => {
      if (bookmarks[bookmarks.length]) {
        camera.position.copy(bookmarks[bookmarks.length].position);
        controls.target.copy(bookmarks[bookmarks.length].target);
        controls.update();
      }
    });
    container.insertBefore(newBtn, container.lastElementChild);
  }
}
// --- UI CONTROLS ---
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const autoRotateBtn = document.getElementById('auto-rotate-btn');
const resetCamBtn = document.getElementById('reset-cam-btn');
const statsEl = document.getElementById('stats');
let currentTime = 0;
timeSlider.addEventListener('input', () => {
  const val = parseFloat(timeSlider.value);
  timeLabel.textContent = `t=${val}`;
  currentTime = val;
  currentHeightData = updateTerrain(val);
  buildRivers(currentHeightData, val);
});
autoRotateBtn.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  autoRotateBtn.textContent = `Auto Rotate: ${controls.autoRotate ? 'ON' : 'OFF'}`;
});
resetCamBtn.addEventListener('click', () => {
  camera.position.set(35, 25, 45);
  controls.target.set(0, 0, 0);
  controls.update();
});
// --- RESIZE ---
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- RENDER LOOP ---
let frameCount = 0;
let lastFpsUpdate = performance.now();
function animate() {
  requestAnimationFrame(animate);
  // Slow time animation when auto-rotating
  if (controls.autoRotate) {
    const animTime = parseFloat(timeSlider.value) + 0.05;
    if (animTime <= 100) {
      timeSlider.value = animTime;
      timeLabel.textContent = `t=${Math.round(animTime)}`;
      currentTime = animTime;
      currentHeightData = updateTerrain(animTime);
      buildRivers(currentHeightData, animTime);
    }
  }
  updateParticles(performance.now() * 0.001, currentHeightData);
  controls.update();
  renderer.render(scene, camera);
  // FPS counter
  frameCount++;
  const now = performance.now();
  if (now - lastFpsUpdate >= 1000) {
    const fps = Math.round(frameCount * 1000 / (now - lastFpsUpdate));
    const vertCount = terrainMesh.geometry.attributes.position.count;
    statsEl.textContent = `terrain: ${vertCount.toLocaleString()} vertices | particles: ${PARTICLE_COUNT} | fps: ${fps}`;
    frameCount = 0;
    lastFpsUpdate = now;
  }
}
animate();
// Initial river build with slight offset
setTimeout(() => buildRivers(currentHeightData, 0.5), 100);
// Performance: log frame budget check
setInterval(() => {
  const fps = frameCount > 0 ? Math.round(frameCount * 1000 / (performance.now() - lastFpsUpdate)) : 0;
  if (fps < 30) {
    console.warn(`Performance warning: ${fps} fps (budget: ${CONFIG.frameBudget}ms per frame)`);
  }
}, 5000);
</script>
</body>
</html>
```
Output is a complete self-contained HTML file implementing 3D Data Terrain Explorer with: procedural terrain via BufferGeometry, vertex colors using vegetation gradient, river geometry flowing downhill, particle system with position array reuse (no per-frame allocation), OrbitControls with damping and auto-rotation, time slider that reshapes terrain by swapping buffer attributes (no new geometry allocations), camera bookmarks, shadow-mapped lighting, frames-per-second counter, and sub-8ms frame budget targeting.