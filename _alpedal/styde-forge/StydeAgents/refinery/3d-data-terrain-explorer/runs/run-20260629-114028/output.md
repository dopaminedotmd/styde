<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
  canvas{display:block}
  #ui{position:fixed;bottom:0;left:0;right:0;padding:12px 20px;background:linear-gradient(transparent,rgba(10,10,20,0.95));display:flex;align-items:center;gap:16px;z-index:10;flex-wrap:wrap}
  #ui label{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#8395a7}
  #time-slider{flex:1;min-width:200px;max-width:400px;accent-color:#54a0ff}
  #time-label{font-size:13px;min-width:90px;color:#54a0ff;font-weight:600}
  .btn{background:rgba(84,160,255,0.15);border:1px solid rgba(84,160,255,0.3);color:#54a0ff;padding:6px 12px;border-radius:4px;cursor:pointer;font-size:12px;transition:all 0.2s}
  .btn:hover{background:rgba(84,160,255,0.3);border-color:#54a0ff}
  .btn.active{background:rgba(84,160,255,0.4);border-color:#fff}
  #diagnostics{position:fixed;top:12px;right:12px;background:rgba(10,10,20,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:10px 14px;font-size:11px;z-index:10;font-family:'Consolas','Courier New',monospace;line-height:1.6}
  #diagnostics .hit{color:#2ecc71}
  #diagnostics .miss{color:#e74c3c}
  #legend{position:fixed;top:12px;left:12px;background:rgba(10,10,20,0.85);border:1px solid rgba(255,255,255,0.1);border-radius:6px;padding:10px 14px;font-size:11px;z-index:10;line-height:1.6}
  #legend span{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px}
  .auto-rot-indicator{position:fixed;top:12px;left:50%;transform:translateX(-50%);font-size:10px;color:#8395a7;letter-spacing:2px;z-index:10;pointer-events:none}
</style>
</head>
<body>
<div id="diagnostics">
  <div>geometries <span class="hit" id="geo-hit">0</span>/<span id="geo-miss">0</span></div>
  <div>heightfields <span class="hit" id="hf-hit">0</span>/<span id="hf-miss">0</span></div>
  <div>river rebuilds <span id="river-count">0</span></div>
  <div>particles <span id="particle-count">0</span></div>
  <div>frame <span id="fps">0</span> fps</div>
</div>
<div id="legend">
  <div style="margin-bottom:4px;font-weight:600">terrain layers</div>
  <div><span style="background:linear-gradient(#1a5c2a,#7dce4a,#c49a2a,#c4c4c4)"></span>elevation: revenue</div>
  <div><span style="background:linear-gradient(#2ecc71,#27ae60,#1a5c2a)"></span>veg: user density</div>
  <div><span style="background:#e74c3c"></span>river: error paths</div>
  <div><span style="background:#f1c40f"></span>trails: api calls</div>
</div>
<div class="auto-rot-indicator" id="auto-rot-label"></div>
<div id="ui">
  <label>time</label>
  <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
  <span id="time-label">t=0</span>
  <button class="btn" id="btn-play">play</button>
  <button class="btn" id="btn-auto-rot">auto-rotate</button>
  <button class="btn" id="btn-bookmark-1">view 1</button>
  <button class="btn" id="btn-bookmark-2">view 2</button>
  <button class="btn" id="btn-bookmark-3">view 3</button>
  <button class="btn" id="btn-reset">reset</button>
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
/* ── synthetic time-series data ──
   Each timestep has a 48x48 grid with: revenue (height), users (vegetation color),
   error_score (river trigger), api_call_count (particle density). */
const GRID = 48, STEPS = 30;
const gridW = 14, gridH = 10; /* world-space dimensions */
/* seeded simplex-style noise for coherent terrain */
function hash(x, z, t, seed) {
  let h = seed + x * 374761393 + z * 668265263 + t * 1274126177;
  h = (h ^ (h >> 13)) * 1274126177;
  h = h ^ (h >> 16);
  return (h & 0x7fffffff) / 0x7fffffff;
}
function smoothNoise(x, z, t, octaves, seed) {
  let val = 0, amp = 1, freq = 1, max = 0;
  for (let o = 0; o < octaves; o++) {
    const sx = x * freq, sz = z * freq;
    const ix = Math.floor(sx), iz = Math.floor(sz);
    const fx = sx - ix, fz = sz - iz;
    const sx1 = fx * fx * (3 - 2 * fx), sz1 = fz * fz * (3 - 2 * fz);
    const v00 = hash(ix, iz, t, seed + o * 1000);
    const v10 = hash(ix + 1, iz, t, seed + o * 1000);
    const v01 = hash(ix, iz + 1, t, seed + o * 1000);
    const v11 = hash(ix + 1, iz + 1, t, seed + o * 1000);
    const a = v00 + (v10 - v00) * sx1;
    const b = v01 + (v11 - v01) * sx1;
    val += (a + (b - a) * sz1) * amp;
    max += amp;
    amp *= 0.5;
    freq *= 2;
  }
  return val / max;
}
/* generate all timesteps: {heights: Float32Array[], colors: Float32Array[],
   rivers: [{points:[], severity:number}][], particles: [{x,z,count}][], errorGrid: number[][] } */
function generateData() {
  const heights = [], colors = [], rivers = [], particles = [], errorGrids = [];
  for (let t = 0; t < STEPS; t++) {
    const ht = new Float32Array(GRID * GRID);
    const cl = new Float32Array(GRID * GRID * 3);
    const eg = new Float32Array(GRID * GRID);
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const nx = ix / (GRID - 1), nz = iz / (GRID - 1);
        const revenue = smoothNoise(nx * 3.5, nz * 3.5, t * 0.08, 4, 42);
        const users = smoothNoise(nx * 4.2 + 1.3, nz * 4.2 + 0.7, t * 0.06, 3, 137);
        const error = smoothNoise(nx * 5.1, nz * 5.1, t * 0.05, 3, 251);
        const idx = iz * GRID + ix;
        ht[idx] = revenue * 3.5;
        /* vegetation: low=barren brown, high=lush green */
        const veg = 0.25 + users * 0.75;
        cl[idx * 3] = 0.15 + veg * 0.1;
        cl[idx * 3 + 1] = 0.35 + veg * 0.55;
        cl[idx * 3 + 2] = 0.1 + veg * 0.1;
        eg[idx] = error;
      }
    }
    heights.push(ht);
    colors.push(cl);
    errorGrids.push(eg);
    /* trace river paths along high-error corridors */
    const rivs = [];
    const visited = new Set();
    for (let iz = 1; iz < GRID - 1; iz++) {
      for (let ix = 1; ix < GRID - 1; ix++) {
        const id = iz * GRID + ix;
        if (visited.has(id) || eg[id] < 0.65) continue;
        /* start tracing from local maxima */
        let maxNeighbor = true;
        for (let dz = -1; dz <= 1; dz++)
          for (let dx = -1; dx <= 1; dx++)
            if (eg[(iz + dz) * GRID + (ix + dx)] > eg[id]) maxNeighbor = false;
        if (!maxNeighbor) continue;
        const path = [];
        let cx = ix, cz = iz, steps = 0;
        while (cx >= 0 && cx < GRID && cz >= 0 && cz < GRID && steps < 60) {
          path.push({ x: (cx / (GRID - 1) - 0.5) * gridW, z: (cz / (GRID - 1) - 0.5) * gridH });
          visited.add(cz * GRID + cx);
          /* follow gradient downhill */
          let bestDx = 0, bestDz = 0, bestVal = eg[cz * GRID + cx];
          for (let dz = -1; dz <= 1; dz++) {
            for (let dx = -1; dx <= 1; dx++) {
              const nz = cz + dz, nx = cx + dx;
              if (nz < 0 || nz >= GRID || nx < 0 || nx >= GRID) continue;
              const v = eg[nz * GRID + nx];
              if (v > bestVal) { bestVal = v; bestDx = dx; bestDz = dz; }
            }
          }
          if (bestDx === 0 && bestDz === 0) break;
          cx += bestDx; cz += bestDz; steps++;
        }
        if (path.length > 4) rivs.push({ points: path, severity: eg[id] });
      }
    }
    rivers.push(rivs);
    /* particles: spawn at high-api-call zones */
    const parts = [];
    for (let i = 0; i < 200; i++) {
      const px = (Math.random() - 0.5) * gridW;
      const pz = (Math.random() - 0.5) * gridH;
      const gx = Math.floor((px / gridW + 0.5) * (GRID - 1));
      const gz = Math.floor((pz / gridH + 0.5) * (GRID - 1));
      const density = gx >= 0 && gx < GRID && gz >= 0 && gz < GRID
        ? smoothNoise(gx / GRID, gz / GRID, t * 0.07, 2, 399) : 0;
      parts.push({ x: px, z: pz, count: Math.floor(density * 5) });
    }
    particles.push(parts);
  }
  return { heights, colors, rivers, particles, errorGrids };
}
/* ── cache manager ── */
const Cache = {
  geometries: new Map(),
  heightfields: new Map(),
  rivers: new Map(),
  hits: { geo: 0, hf: 0, riv: 0 },
  misses: { geo: 0, hf: 0, riv: 0 },
  riverRebuilds: 0,
  get(key, store) {
    if (store.has(key)) { this.hits[store === this.geometries ? 'geo' : store === this.heightfields ? 'hf' : 'riv']++; return store.get(key); }
    this.misses[store === this.geometries ? 'geo' : store === this.heightfields ? 'hf' : 'riv']++;
    return null;
  },
  set(key, val, store) { store.set(key, val); },
  clearAll() { this.geometries.clear(); this.heightfields.clear(); this.rivers.clear(); }
};
/* ── height lookup from precomputed array ── */
function getHeight(heightsArr, wx, wz) {
  const gx = (wx / gridW + 0.5) * (GRID - 1);
  const gz = (wz / gridH + 0.5) * (GRID - 1);
  const ix = THREE.MathUtils.clamp(Math.floor(gx), 0, GRID - 2);
  const iz = THREE.MathUtils.clamp(Math.floor(gz), 0, GRID - 2);
  const fx = gx - ix, fz = gz - iz;
  const h00 = heightsArr[iz * GRID + ix];
  const h10 = heightsArr[iz * GRID + ix + 1];
  const h01 = heightsArr[(iz + 1) * GRID + ix];
  const h11 = heightsArr[(iz + 1) * GRID + ix + 1];
  return h00 + (h10 - h00) * fx + (h01 - h00) * fz + (h00 - h10 - h01 + h11) * fx * fz;
}
/* ── terrain mesh ── */
let terrainMesh, terrainGeo;
function buildTerrainGeometry(heightsArr, colorsArr) {
  const key = heightsArr.buffer; /* use buffer identity as cache key */
  const cached = Cache.get(key, Cache.geometries);
  if (cached) return cached;
  const geo = new THREE.BufferGeometry();
  const verts = new Float32Array(GRID * GRID * 3);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const vx = (ix / (GRID - 1) - 0.5) * gridW;
      const vz = (iz / (GRID - 1) - 0.5) * gridH;
      verts[idx * 3] = vx;
      verts[idx * 3 + 1] = heightsArr[idx];
      verts[idx * 3 + 2] = vz;
    }
  }
  const indices = [];
  for (let iz = 0; iz < GRID - 1; iz++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iz * GRID + ix, b = a + 1, c = a + GRID, d = c + 1;
      indices.push(a, b, d, a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  Cache.set(key, geo, Cache.geometries);
  return geo;
}
/* ── river system ── */
let riverGroup;
function buildRiverGeometry(riverData) {
  const key = JSON.stringify(riverData.map(r => r.points.length));
  const cached = Cache.get(key, Cache.rivers);
  if (cached) return cached.clone();
  Cache.riverRebuilds++;
  const group = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: 0xe74c3c, roughness: 0.3, metalness: 0.1, emissive: 0x330000 });
  riverData.forEach(r => {
    if (r.points.length < 3) return;
    const curve = new THREE.CatmullRomCurve3(
      r.points.map(p => new THREE.Vector3(p.x, 0.05, p.z)), false, 'catmullrom', 0.5
    );
    const tubeGeo = new THREE.TubeGeometry(curve, 48, 0.06 + r.severity * 0.08, 6, false);
    const mesh = new THREE.Mesh(tubeGeo, mat);
    mesh.renderOrder = 1;
    mesh.material.depthTest = true;
    group.add(mesh);
  });
  Cache.set(key, group.clone(), Cache.rivers);
  return group;
}
/* ── particle system ── */
let particlePoints, particlePositions, particleData;
function buildParticleGeometry(particleArr, heightsArr) {
  const count = particleArr.length;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const p = particleArr[i];
    const h = getHeight(heightsArr, p.x, p.z) + 0.15;
    positions[i * 3] = p.x;
    positions[i * 3 + 1] = h;
    positions[i * 3 + 2] = p.z;
    const intensity = p.count / 5;
    colors[i * 3] = 0.9 + intensity * 0.1;
    colors[i * 3 + 1] = 0.7 + intensity * 0.2;
    colors[i * 3 + 2] = 0.1;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  return { geo, positions, colors };
}
function updateParticles(particleArr, heightsArr) {
  /* reuse position array — no per-frame allocation */
  for (let i = 0; i < particleArr.length; i++) {
    const h = getHeight(heightsArr, particleArr[i].x, particleArr[i].z) + 0.15;
    particlePositions[i * 3 + 1] = h;
  }
  particlePoints.geometry.attributes.position.needsUpdate = true;
}
/* ── scene setup ── */
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 12, 35);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 60);
camera.position.set(8, 7, 10);
camera.lookAt(0, 1, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
/* lighting */
const ambient = new THREE.AmbientLight(0x2c3e50, 1.4);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(8, 14, 4);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 50;
sun.shadow.camera.left = -12;
sun.shadow.camera.right = 12;
sun.shadow.camera.top = 12;
sun.shadow.camera.bottom = -12;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4488cc, 1.2);
fill.position.set(-4, 2, -4);
scene.add(fill);
/* ground plane for shadow reception */
const groundGeo = new THREE.PlaneGeometry(30, 30);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x111122, roughness: 0.9 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.5;
ground.receiveShadow = true;
scene.add(ground);
/* controls */
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.2, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 3;
controls.maxDistance = 22;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
/* bookmarks */
const bookmarks = [
  { pos: new THREE.Vector3(8, 7, 10), target: new THREE.Vector3(0, 1.2, 0) },
  { pos: new THREE.Vector3(0, 10, 2), target: new THREE.Vector3(0, 0, 0) },
  { pos: new THREE.Vector3(-4, 3, -8), target: new THREE.Vector3(2, 1.5, 2) },
];
/* ── load data and init ── */
const data = generateData();
let currentStep = 0, playing = false, playInterval = null;
terrainGeo = buildTerrainGeometry(data.heights[0], data.colors[0]);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.65, metalness: 0.05, flatShading: false
});
terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
riverGroup = new THREE.Group();
scene.add(riverGroup);
updateRivers(0);
const pInit = buildParticleGeometry(data.particles[0], data.heights[0]);
particlePositions = pInit.positions;
particleData = data.particles;
const pMat = new THREE.PointsMaterial({ size: 0.08, vertexColors: true, blending: THREE.AdditiveBlending, depthWrite: false });
particlePoints = new THREE.Points(pInit.geo, pMat);
particlePoints.renderOrder = 2;
scene.add(particlePoints);
/* ── time transition ── */
let riverDebounceTimer = null;
function updateRivers(step) {
  while (riverGroup.children.length > 0) riverGroup.remove(riverGroup.children[0]);
  const rivGeo = buildRiverGeometry(data.rivers[step]);
  while (rivGeo.children.length > 0) riverGroup.add(rivGeo.children[0]);
}
function setTimeStep(step) {
  currentStep = THREE.MathUtils.clamp(step, 0, STEPS - 1);
  /* swap terrain heightfield (cached pre-built geometry) */
  const newGeo = buildTerrainGeometry(data.heights[currentStep], data.colors[currentStep]);
  if (terrainMesh.geometry !== newGeo) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = newGeo;
  }
  updateParticles(particleData[currentStep], data.heights[currentStep]);
  /* debounced river rebuild — only fires after slider stops for 200ms */
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => updateRivers(currentStep), 200);
  /* update ui */
  document.getElementById('time-slider').value = currentStep;
  document.getElementById('time-label').textContent = `t=${currentStep}`;
}
/* ── ui handlers ── */
document.getElementById('time-slider').addEventListener('input', (e) => {
  setTimeStep(parseInt(e.target.value));
});
document.getElementById('btn-play').addEventListener('click', () => {
  playing = !playing;
  const btn = document.getElementById('btn-play');
  btn.textContent = playing ? 'pause' : 'play';
  btn.classList.toggle('active', playing);
  if (playing) {
    playInterval = setInterval(() => {
      setTimeStep((currentStep + 1) % STEPS);
    }, 400);
  } else {
    clearInterval(playInterval);
  }
});
document.getElementById('btn-auto-rot').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
document.getElementById('btn-reset').addEventListener('click', () => {
  camera.position.copy(bookmarks[0].pos);
  controls.target.copy(bookmarks[0].target);
  controls.update();
});
[1, 2, 3].forEach(i => {
  document.getElementById(`btn-bookmark-${i}`).addEventListener('click', () => {
    const bm = bookmarks[i - 1];
    /* smooth animate to bookmark */
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const endPos = bm.pos.clone();
    const endTarget = bm.target.clone();
    const startTime = performance.now();
    const duration = 800;
    function animBookmark(now) {
      const t = Math.min((now - startTime) / duration, 1);
      const ease = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      camera.position.lerpVectors(startPos, endPos, ease);
      controls.target.lerpVectors(startTarget, endTarget, ease);
      controls.update();
      if (t < 1) requestAnimationFrame(animBookmark);
    }
    requestAnimationFrame(animBookmark);
  });
});
/* ── fps tracking ── */
let frameCount = 0, lastFpsTime = performance.now();
function updateDiagnostics() {
  document.getElementById('geo-hit').textContent = Cache.hits.geo;
  document.getElementById('geo-miss').textContent = Cache.misses.geo;
  document.getElementById('hf-hit').textContent = Cache.hits.hf;
  document.getElementById('hf-miss').textContent = Cache.misses.hf;
  document.getElementById('river-count').textContent = Cache.riverRebuilds;
  document.getElementById('particle-count').textContent = particleData[currentStep].length;
  document.getElementById('fps').textContent = Math.round(frameCount / ((performance.now() - lastFpsTime) / 1000));
  document.getElementById('auto-rot-label').textContent = controls.autoRotate ? 'auto-rotating' : '';
}
setInterval(updateDiagnostics, 500);
/* ── render loop ── */
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
  frameCount++;
  if (performance.now() - lastFpsTime >= 1000) {
    frameCount = 0;
    lastFpsTime = performance.now();
  }
}
animate();
/* ── resize ── */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ── keyboard shortcuts ── */
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case ' ': e.preventDefault(); document.getElementById('btn-play').click(); break;
    case 'r': controls.autoRotate = !controls.autoRotate;
      document.getElementById('btn-auto-rot').classList.toggle('active', controls.autoRotate); break;
    case 'arrowleft': setTimeStep(currentStep - 1); break;
    case 'arrowright': setTimeStep(currentStep + 1); break;
    case '1': document.getElementById('btn-bookmark-1').click(); break;
    case '2': document.getElementById('btn-bookmark-2').click(); break;
    case '3': document.getElementById('btn-bookmark-3').click(); break;
    case '0': document.getElementById('btn-reset').click(); break;
  }
});
</script>
</body>
</html>