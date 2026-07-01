```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  body { margin:0; overflow:hidden; background:#0a0e17; font-family:'Segoe UI',Arial,sans-serif; color:#fff; }
  #info {
    position:absolute; top:16px; left:50%; transform:translateX(-50%);
    background:rgba(10,14,23,0.85); backdrop-filter:blur(8px);
    padding:10px 24px; border-radius:12px; border:1px solid rgba(255,255,255,0.08);
    font-size:13px; letter-spacing:0.5px; z-index:10;
    text-align:center; pointer-events:none;
  }
  #info span { color:#5b9bd5; font-weight:600; }
  #controls-panel {
    position:absolute; bottom:30px; left:50%; transform:translateX(-50%);
    background:rgba(10,14,23,0.9); backdrop-filter:blur(12px);
    padding:16px 28px; border-radius:16px; border:1px solid rgba(255,255,255,0.1);
    display:flex; align-items:center; gap:20px; z-index:10;
    box-shadow:0 8px 32px rgba(0,0,0,0.5);
  }
  #controls-panel label { font-size:12px; color:rgba(255,255,255,0.6); }
  #time-slider { width:240px; height:4px; cursor:pointer; accent-color:#5b9bd5; }
  #time-value { font-size:13px; color:#5b9bd5; font-weight:600; min-width:36px; text-align:center; }
  #metrics {
    display:flex; gap:20px; font-size:11px;
  }
  #metrics .m { display:flex; align-items:center; gap:6px; }
  #metrics .dot { width:8px; height:8px; border-radius:50%; display:inline-block; }
  .dot-green { background:#4caf50; }
  .dot-red { background:#f44336; }
  .dot-blue { background:#2196f3; }
  #bookmark-btn {
    background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15);
    color:#fff; padding:6px 14px; border-radius:8px; cursor:pointer;
    font-size:11px; transition:all 0.2s;
  }
  #bookmark-btn:hover { background:rgba(91,155,213,0.25); }
  @media(max-width:768px) {
    #controls-panel { flex-wrap:wrap; gap:12px; padding:14px 18px; width:90%; }
    #time-slider { width:160px; }
    #metrics { gap:10px; }
  }
</style>
</head>
<body>
<div id="info"><span>3D Data Terrain</span>  Revenue = elevation  |  User density = vegetation  |  Errors = rivers</div>
<div id="controls-panel">
  <div>
    <label for="time-slider">Time</label>
    <div style="display:flex;align-items:center;gap:8px;margin-top:4px;">
      <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
      <span id="time-value">T+0</span>
    </div>
  </div>
  <div id="metrics">
    <div class="m"><span class="dot dot-green"></span> Users: <span id="user-metric">42</span></div>
    <div class="m"><span class="dot dot-red"></span> Errors: <span id="error-metric">7</span></div>
    <div class="m"><span class="dot dot-blue"></span> Revenue: <span id="rev-metric">$1.2K</span></div>
  </div>
  <button id="bookmark-btn">+ Bookmark</button>
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
// --- config ---
const SIZE = 64;
const SEGMENTS = SIZE - 1;
const SCALE = 1.6;
const HEIGHT_SCALE = 1.8;
const TIME_FRAMES = 100;
// --- procedural data generator ---
function makeHeightData(t) {
  const data = new Float32Array(SIZE * SIZE);
  const tNorm = t / (TIME_FRAMES - 1);
  for (let z = 0; z < SIZE; z++) {
    for (let x = 0; x < SIZE; x++) {
      const nx = x / SEGMENTS - 0.5;
      const nz = z / SEGMENTS - 0.5;
      const dist = Math.sqrt(nx*nx + nz*nz);
      // main ridge
      let h = Math.sin(nx * 3.0 + tNorm * 2.0) * Math.cos(nz * 2.5 + tNorm * 1.2) * 0.6;
      // secondary hills
      h += Math.sin(nx * 6.0 + 1.3) * Math.cos(nz * 5.0 + 0.7) * 0.25;
      h += Math.sin((nx + nz) * 4.0 + tNorm * 3.0) * 0.15;
      // valley (lower center-right)
      h -= 0.3 * Math.exp(-((nx-0.15)*(nx-0.15) + (nz-0.05)*(nz-0.05)) * 15.0);
      // peak
      h += 0.5 * Math.exp(-(nx*nx + nz*nz) * 5.0);
      // time drift
      h += Math.sin(dist * 8.0 - tNorm * 4.0) * 0.1 * (1 - dist);
      data[z * SIZE + x] = h;
    }
  }
  return data;
}
function makeColorData(t) {
  const data = new Float32Array(SIZE * SIZE * 3);
  const tNorm = t / (TIME_FRAMES - 1);
  for (let z = 0; z < SIZE; z++) {
    for (let x = 0; x < SIZE; x++) {
      const nx = x / SEGMENTS - 0.5;
      const nz = z / SEGMENTS - 0.5;
      const dist = Math.sqrt(nx*nx + nz*nz);
      // user density metric
      const density = 0.5 + 0.5 * Math.sin(nx * 3.0 + nz * 2.0 + tNorm * 1.5);
      // vegetation gradient: low=dry brown, high=lush green
      const g = 0.15 + density * 0.7;
      const r = 0.35 + (1 - density) * 0.5;
      const b = 0.05 + density * 0.2;
      const idx = (z * SIZE + x) * 3;
      data[idx] = r;
      data[idx+1] = g;
      data[idx+2] = b;
    }
  }
  return data;
}
function makeErrorRiverPaths(t) {
  const paths = [];
  const tNorm = t / (TIME_FRAMES - 1);
  // two river systems
  for (let r = 0; r < 2; r++) {
    const pts = [];
    let cx = 0.2 + r * 0.3 + Math.sin(tNorm * 0.5 + r) * 0.05;
    let cz = -0.4 + r * 0.1;
    for (let i = 0; i < 40; i++) {
      const u = i / 39;
      cx += (Math.sin(u * 5.0 + tNorm * 2.0 + r) * 0.02);
      cz += 0.02 + Math.sin(u * 3.0 + r * 2.0) * 0.008;
      const gx = Math.round((cx + 0.5) * SEGMENTS);
      const gz = Math.round((cz + 0.5) * SEGMENTS);
      if (gx >= 0 && gx < SIZE && gz >= 0 && gz < SIZE) {
        pts.push(new THREE.Vector3(
          (cx) * SIZE * SCALE,
          0,
          (cz) * SIZE * SCALE
        ));
      }
    }
    paths.push(pts);
  }
  return paths;
}
function makeParticlePaths(t) {
  const particles = [];
  const tNorm = t / (TIME_FRAMES - 1);
  for (let i = 0; i < 200; i++) {
    const startX = (Math.random() - 0.5) * SIZE * SCALE * 0.8;
    const startZ = (Math.random() - 0.5) * SIZE * SCALE * 0.8;
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.1 + Math.random() * 0.3;
    const trailLen = 20 + Math.floor(Math.random() * 20);
    const trail = [];
    for (let j = 0; j < trailLen; j++) {
      const u = j / trailLen;
      const x = startX + Math.sin(u * 3.0 + tNorm * 2.0 + i) * 0.5 * SIZE * SCALE * 0.2;
      const z = startZ + Math.cos(u * 2.0 + tNorm * 1.5 + i * 0.5) * 0.5 * SIZE * SCALE * 0.2;
      // height will be sampled from terrain, set to 0 for now
      trail.push(new THREE.Vector3(x, 0, z));
    }
    particles.push(trail);
  }
  return particles;
}
// --- scene setup ---
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0e17);
scene.fog = new THREE.Fog(0x0a0e17, 40, 80);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(25, 22, 30);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.rotateSpeed = 0.6;
controls.zoomSpeed = 0.8;
controls.minDistance = 5;
controls.maxDistance = 80;
controls.maxPolarAngle = Math.PI / 2.05;
controls.target.set(0, 0, 0);
// --- lighting ---
const ambient = new THREE.AmbientLight(0x334466, 0.4);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 1.6);
sun.position.set(20, 30, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 1024;
sun.shadow.mapSize.height = 1024;
sun.shadow.camera.near = 0.1;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4488ff, 0.3);
fill.position.set(-15, 10, -20);
scene.add(fill);
const rim = new THREE.DirectionalLight(0x88aaff, 0.25);
rim.position.set(0, -10, 20);
scene.add(rim);
// --- ground plane (for shadows) ---
const groundGeo = new THREE.PlaneGeometry(100, 100);
const groundMat = new THREE.ShadowMaterial({ opacity: 0.3, color: 0x000000 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -HEIGHT_SCALE * 0.6;
ground.receiveShadow = true;
scene.add(ground);
// --- build terrain ---
let terrainMesh, terrainGeo, riversGroup, particlesGroup;
let currentTime = 0;
function buildTerrain(t) {
  if (terrainMesh) {
    scene.remove(terrainMesh);
    terrainMesh.geometry.dispose();
    terrainMesh.material.dispose();
  }
  const heightData = makeHeightData(t);
  const colorData = makeColorData(t);
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(SIZE * SIZE * 3);
  const colors = new Float32Array(SIZE * SIZE * 3);
  const indices = [];
  for (let z = 0; z < SIZE; z++) {
    for (let x = 0; x < SIZE; x++) {
      const idx = z * SIZE + x;
      const h = heightData[idx] * HEIGHT_SCALE;
      const px = (x / SEGMENTS - 0.5) * SIZE * SCALE;
      const pz = (z / SEGMENTS - 0.5) * SIZE * SCALE;
      positions[idx * 3] = px;
      positions[idx * 3 + 1] = h;
      positions[idx * 3 + 2] = pz;
      colors[idx * 3] = colorData[idx * 3];
      colors[idx * 3 + 1] = colorData[idx * 3 + 1];
      colors[idx * 3 + 2] = colorData[idx * 3 + 2];
    }
  }
  for (let z = 0; z < SEGMENTS; z++) {
    for (let x = 0; x < SEGMENTS; x++) {
      const a = z * SIZE + x;
      const b = z * SIZE + x + 1;
      const c = (z + 1) * SIZE + x;
      const d = (z + 1) * SIZE + x + 1;
      indices.push(a, b, c);
      indices.push(b, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.6,
    metalness: 0.1,
    flatShading: false,
    side: THREE.DoubleSide,
    envMapIntensity: 0.2,
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  scene.add(mesh);
  terrainMesh = mesh;
  terrainGeo = geo;
  return heightData;
}
function buildRivers(t, heightData) {
  if (riversGroup) {
    scene.remove(riversGroup);
    riversGroup.traverse(c => { if (c.isMesh) { c.geometry.dispose(); c.material.dispose(); } });
  }
  const group = new THREE.Group();
  const paths = makeErrorRiverPaths(t);
  paths.forEach(pathPts => {
    if (pathPts.length < 3) return;
    // sample heights
    const pts = pathPts.map(p => {
      const gx = Math.round(p.x / (SIZE * SCALE) + 0.5);
      const gz = Math.round(p.z / (SIZE * SCALE) + 0.5);
      const idx = Math.min(Math.max(gz, 0), SIZE-1) * SIZE + Math.min(Math.max(gx, 0), SIZE-1);
      const h = heightData ? heightData[idx] * HEIGHT_SCALE : 0;
      return new THREE.Vector3(p.x, h - 0.05, p.z);
    });
    const curve = new THREE.CatmullRomCurve3(pts);
    const curvePts = curve.getPoints(80);
    // river tube
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.2 + Math.random() * 0.15, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xf44336,
      emissive: 0xf44336,
      emissiveIntensity: 0.2 + Math.random() * 0.15,
      transparent: true,
      opacity: 0.7,
      roughness: 0.3,
      metalness: 0.4,
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.castShadow = true;
    group.add(tube);
    // glow line along river
    const glowGeo = new THREE.BufferGeometry().setFromPoints(curvePts);
    const glowMat = new THREE.LineBasicMaterial({
      color: 0xff6666,
      transparent: true,
      opacity: 0.3,
      linewidth: 1,
    });
    const glowLine = new THREE.Line(glowGeo, glowMat);
    group.add(glowLine);
  });
  scene.add(group);
  riversGroup = group;
}
function buildParticles(t, heightData) {
  if (particlesGroup) {
    scene.remove(particlesGroup);
    if (particlesGroup.geometry) particlesGroup.geometry.dispose();
    if (particlesGroup.material) particlesGroup.material.dispose();
  }
  const paths = makeParticlePaths(t);
  const allPositions = [];
  const allColors = [];
  paths.forEach(trail => {
    // sample heights along trail
    const pts = trail.map(p => {
      const gx = Math.round(p.x / (SIZE * SCALE) + 0.5);
      const gz = Math.round(p.z / (SIZE * SCALE) + 0.5);
      const idx = Math.min(Math.max(gz, 0), SIZE-1) * SIZE + Math.min(Math.max(gx, 0), SIZE-1);
      const h = heightData ? heightData[idx] * HEIGHT_SCALE + 0.05 : 0;
      return new THREE.Vector3(p.x, h + 0.3, p.z);
    });
    if (pts.length < 2) return;
    const hue = 0.55 + Math.random() * 0.15; // blue-cyan range
    const color = new THREE.Color().setHSL(hue, 0.8, 0.6);
    pts.forEach(p => {
      allPositions.push(p.x, p.y, p.z);
      allColors.push(color.r, color.g, color.b);
    });
  });
  if (allPositions.length === 0) {
    particlesGroup = new THREE.Group();
    scene.add(particlesGroup);
    return;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(allPositions, 3));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(allColors, 3));
  const mat = new THREE.PointsMaterial({
    size: 0.3,
    vertexColors: true,
    transparent: true,
    opacity: 0.7,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    sizeAttenuation: true,
  });
  const points = new THREE.Points(geo, mat);
  scene.add(points);
  particlesGroup = points;
}
function updateTerrain(t) {
  currentTime = t;
  const heightData = buildTerrain(t);
  buildRivers(t, heightData);
  buildParticles(t, heightData);
  // update UI metrics
  const tNorm = t / (TIME_FRAMES - 1);
  document.getElementById('user-metric').textContent = Math.floor(40 + 30 * (0.5 + 0.5 * Math.sin(tNorm * 1.5)));
  document.getElementById('error-metric').textContent = Math.floor(3 + 8 * (0.5 + 0.5 * Math.sin(tNorm * 2.3 + 0.7)));
  document.getElementById('rev-metric').textContent = '$' + (0.8 + 1.2 * (0.5 + 0.5 * Math.sin(tNorm * 1.8))).toFixed(1) + 'K';
  document.getElementById('time-value').textContent = 'T+' + t;
}
// --- camera bookmarks ---
const bookmarks = [];
document.getElementById('bookmark-btn').addEventListener('click', () => {
  const pos = camera.position.clone();
  const target = controls.target.clone();
  bookmarks.push({ pos, target });
  const btn = document.getElementById('bookmark-btn');
  btn.textContent = bookmarks.length + ' saved';
  setTimeout(() => { btn.textContent = '+ Bookmark'; }, 1500);
  // restore: cycle through with keyboard (R key)
});
window.addEventListener('keydown', (e) => {
  if (e.key === 'r' || e.key === 'R') {
    if (bookmarks.length > 0) {
      const bm = bookmarks.shift();
      bookmarks.push(bm);
      camera.position.copy(bm.pos);
      controls.target.copy(bm.target);
      controls.update();
    }
  }
  // auto-rotation toggle with Space
  if (e.key === ' ') {
    e.preventDefault();
    autoRotate = !autoRotate;
  }
});
// --- init ---
const initialData = makeHeightData(0);
buildTerrain(0);
buildRivers(0, initialData);
buildParticles(0, initialData);
// time slider
const slider = document.getElementById('time-slider');
slider.addEventListener('input', (e) => {
  const val = parseInt(e.target.value);
  updateTerrain(val);
});
// resize
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- auto-rotate ---
let autoRotate = true;
// --- animation loop ---
function animate() {
  requestAnimationFrame(animate);
  if (autoRotate) {
    const radius = Math.sqrt(
      camera.position.x * camera.position.x +
      camera.position.z * camera.position.z
    );
    const angle = Math.atan2(camera.position.z, camera.position.x);
    const newAngle = angle + 0.002;
    camera.position.x = radius * Math.cos(newAngle);
    camera.position.z = radius * Math.sin(newAngle);
    camera.lookAt(controls.target);
  }
  // animate particles (subtle bob)
  if (particlesGroup && particlesGroup.isPoints) {
    const pos = particlesGroup.geometry.attributes.position;
    const array = pos.array;
    for (let i = 1; i < array.length; i += 3) {
      array[i] += Math.sin(Date.now() * 0.001 + i * 0.1) * 0.002;
    }
    pos.needsUpdate = true;
  }
  controls.update();
  renderer.render(scene, camera);
}
animate();
// --- keyboard help (console only) ---
console.log('3D Data Terrain Explorer');
console.log('  Space -> toggle auto-rotation');
console.log('  R     -> cycle camera bookmarks');
console.log('  Drag  -> orbit | Scroll -> zoom | Right-drag -> pan');
</script>
</body>
</html>
```