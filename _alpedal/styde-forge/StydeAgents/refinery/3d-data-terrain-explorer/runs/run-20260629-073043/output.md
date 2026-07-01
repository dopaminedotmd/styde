<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#0a0a14;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
#canvas-container{position:fixed;inset:0;z-index:1}
#legend{position:fixed;top:16px;right:16px;z-index:10;background:rgba(10,10,20,0.85);border:1px solid rgba(100,140,220,0.3);border-radius:8px;padding:14px 16px;min-width:180px;backdrop-filter:blur(12px)}
#legend h3{font-size:13px;font-weight:600;margin:0 0 10px;color:#8ab4f8;text-transform:uppercase;letter-spacing:0.5px}
.legend-row{display:flex;align-items:center;margin:4px 0;font-size:11px;gap:8px}
.legend-swatch{width:24px;height:12px;border-radius:2px;flex-shrink:0}
#tooltip{position:fixed;z-index:20;background:rgba(10,10,22,0.92);border:1px solid rgba(100,180,255,0.5);border-radius:6px;padding:8px 12px;font-size:11px;line-height:1.5;pointer-events:none;opacity:0;transition:opacity 0.1s;backdrop-filter:blur(8px);white-space:nowrap}
#tooltip.visible{opacity:1}
#tooltip .tt-val{color:#8ab4f8;font-weight:600}
#timebar{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;display:flex;align-items:center;gap:12px;background:rgba(10,10,20,0.85);border:1px solid rgba(100,140,220,0.3);border-radius:8px;padding:10px 18px;backdrop-filter:blur(12px)}
#timebar label{font-size:11px;color:#8ab4f8;text-transform:uppercase;letter-spacing:0.5px;white-space:nowrap}
#time-slider{-webkit-appearance:none;width:240px;height:4px;border-radius:2px;background:rgba(100,140,220,0.3);outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#8ab4f8;cursor:pointer;border:2px solid #0a0a14}
#time-label{font-size:11px;color:#c8d6e5;min-width:48px;text-align:center;font-variant-numeric:tabular-nums}
#bookmarks{position:fixed;top:16px;left:16px;z-index:10;display:flex;flex-direction:column;gap:6px}
.bm-btn{background:rgba(10,10,20,0.8);border:1px solid rgba(100,140,220,0.3);color:#c8d6e5;padding:6px 12px;border-radius:6px;font-size:11px;cursor:pointer;transition:all 0.2s;text-align:left;backdrop-filter:blur(8px)}
.bm-btn:hover{background:rgba(100,140,220,0.2);border-color:rgba(100,180,255,0.6)}
#datapanel{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:8px}
.dp-btn{background:rgba(10,10,20,0.8);border:1px solid rgba(100,140,220,0.3);color:#8ab4f8;padding:6px 14px;border-radius:6px;font-size:11px;cursor:pointer;transition:all 0.2s;backdrop-filter:blur(8px)}
.dp-btn:hover{background:rgba(100,140,220,0.2)}
#loading{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;background:rgba(10,10,20,0.9);transition:opacity 0.4s}
#loading.hidden{opacity:0;pointer-events:none}
#loading span{color:#8ab4f8;font-size:14px}
#fps{position:fixed;bottom:20px;right:20px;z-index:10;font-size:10px;color:rgba(200,214,229,0.5);font-variant-numeric:tabular-nums}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="legend">
  <h3>Legend</h3>
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#1a5c2a,#4a9, #c8b44a,#e8dcc8)"></span>Elevation (Revenue)</div>
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#2d5016,#6bcf3a)"></span>Vegetation (Users)</div>
  <div class="legend-row"><span class="legend-swatch" style="background:#e04040"></span>Rivers (Errors)</div>
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#ffcc00,#ff6600)"></span>Particles (API Calls)</div>
</div>
<div id="tooltip"><div><span class="tt-val" id="tt-elev">--</span> elevation</div><div><span class="tt-val" id="tt-veg">--</span> vegetation</div><div><span class="tt-val" id="tt-err">--</span> errors</div></div>
<div id="timebar">
  <label>Time</label>
  <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
  <span id="time-label">00:00</span>
</div>
<div id="bookmarks">
  <button class="bm-btn" data-bm="overview">Overview</button>
  <button class="bm-btn" data-bm="north">North Face</button>
  <button class="bm-btn" data-bm="valley">Valley View</button>
  <button class="bm-btn" data-bm="peak">Peak Closeup</button>
</div>
<div id="datapanel">
  <button class="dp-btn" id="btn-sample">Load Sample Data</button>
  <button class="dp-btn" id="btn-noise">Regenerate Noise</button>
  <button class="dp-btn" id="btn-auto-rotate">Auto-Rotate</button>
</div>
<div id="loading"><span>Generating terrain...</span></div>
<div id="fps">FPS: --</div>
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
const GRID = 128;
const PARTICLE_CAPACITY = 600;
const TIME_FRAMES = 24;
const TERRAIN_SIZE = 20;
const TERRAIN_HEIGHT = 8;
const HALF = TERRAIN_SIZE / 2;
const container = document.getElementById('canvas-container');
const tooltip = document.getElementById('tooltip');
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const fpsEl = document.getElementById('fps');
const loadingEl = document.getElementById('loading');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 25, 60);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 100);
camera.position.set(16, 12, 18);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 2, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 4;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.55;
controls.minPolarAngle = 0.2;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 2.5);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0001;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x4466aa, 1.5);
fillLight.position.set(-5, 2, -5);
scene.add(fillLight);
const GROUND_Y = -0.05;
const groundGeo = new THREE.PlaneGeometry(30, 30);
const groundMat = new THREE.MeshStandardMaterial({ color: 0x111122, roughness: 0.95, metalness: 0.1 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = GROUND_Y;
ground.receiveShadow = true;
scene.add(ground);
const gridHelper = new THREE.PolarGridHelper(14, 32, 24, 128, 0x222244, 0x222244);
gridHelper.position.y = GROUND_Y;
scene.add(gridHelper);
let terrainMesh = null;
let riverLines = [];
let particleSystem = null;
let allFramesData = [];
let currentFrame = 0;
function hash(x, y) {
  let h = x * 374761393 + y * 668265263 + 1274126177;
  h = (h ^ (h >> 13)) * 1274126177;
  h = h ^ (h >> 16);
  return (h & 0x7fffffff) / 0x7fffffff;
}
function smoothNoise(x, y) {
  const ix = Math.floor(x), iy = Math.floor(y);
  const fx = x - ix, fy = y - iy;
  const sx = fx * fx * (3 - 2 * fx);
  const sy = fy * fy * (3 - 2 * fy);
  const n00 = hash(ix, iy), n10 = hash(ix + 1, iy);
  const n01 = hash(ix, iy + 1), n11 = hash(ix + 1, iy + 1);
  const nx0 = n00 + (n10 - n00) * sx;
  const nx1 = n01 + (n11 - n01) * sx;
  return nx0 + (nx1 - nx0) * sy;
}
function fbm(x, y, octaves = 4) {
  let v = 0, amp = 1, freq = 1, max = 0;
  for (let i = 0; i < octaves; i++) {
    v += smoothNoise(x * freq, y * freq) * amp;
    max += amp;
    amp *= 0.5;
    freq *= 2.0;
  }
  return v / max;
}
function generateFrameData(seed, t) {
  const terrain = new Float32Array(GRID * GRID);
  const vegetation = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  const timeWarp = t * 0.15;
  const seedOff = seed * 1000;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const nx = ix / GRID * 6 - 3;
      const ny = iy / GRID * 6 - 3;
      const dist = Math.sqrt(nx * nx + ny * ny) / 4;
      const e = fbm(nx + seedOff, ny + seedOff + timeWarp, 5);
      const ridge = 1 - Math.abs(e * 2 - 1);
      const el = e * 0.7 + ridge * 0.3 - dist * 0.25;
      terrain[iy * GRID + ix] = Math.max(0, el);
      vegetation[iy * GRID + ix] = fbm(nx + seedOff + 5, ny + seedOff + 3 + timeWarp * 0.7, 4);
      const errBase = fbm(nx + seedOff + 10, ny + seedOff - 5 + timeWarp * 0.5, 3);
      errors[iy * GRID + ix] = errBase * (1 - dist * 1.2);
    }
  }
  const flows = [];
  const flowCount = 80 + Math.floor(Math.random() * 40);
  for (let i = 0; i < flowCount; i++) {
    const fx = Math.random() * GRID;
    const fy = Math.random() * GRID;
    const tx = fx + (Math.random() - 0.5) * GRID * 0.5;
    const ty = fy + (Math.random() - 0.5) * GRID * 0.5;
    const cx = Math.max(0, Math.min(GRID - 1, Math.floor(fx)));
    const cy = Math.max(0, Math.min(GRID - 1, Math.floor(fy)));
    flows.push({ fromX: fx, fromY: fy, toX: tx, toY: ty, intensity: terrain[cy * GRID + cx] * (0.3 + Math.random() * 0.7) });
  }
  return { terrain, vegetation, errors, flows };
}
function generateAllFrames(seed) {
  const frames = [];
  for (let t = 0; t < TIME_FRAMES; t++) {
    frames.push(generateFrameData(seed, t));
  }
  return frames;
}
function sampleData(data, ix, iy) {
  const cx = Math.max(0, Math.min(GRID - 1, Math.round(ix)));
  const cy = Math.max(0, Math.min(GRID - 1, Math.round(iy)));
  return {
    terrain: data.terrain[cy * GRID + cx],
    vegetation: data.vegetation[cy * GRID + cx],
    errors: data.errors[cy * GRID + cx]
  };
}
function elevationColor(el, veg) {
  const h = 0.25 - el * 0.22 + veg * 0.08;
  const s = 0.5 + el * 0.3;
  const l = 0.15 + el * 0.55;
  const c = new THREE.Color();
  c.setHSL(Math.max(0.05, Math.min(0.45, h)), Math.max(0.2, Math.min(0.9, s)), Math.max(0.08, Math.min(0.85, l)));
  return c;
}
const positions = new Float32Array(GRID * GRID * 3);
const colors = new Float32Array(GRID * GRID * 3);
const indices = new Uint32Array((GRID - 1) * (GRID - 1) * 6);
let idxIdx = 0;
for (let iy = 0; iy < GRID - 1; iy++) {
  for (let ix = 0; ix < GRID - 1; ix++) {
    const a = iy * GRID + ix;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    indices[idxIdx++] = a; indices[idxIdx++] = b; indices[idxIdx++] = d;
    indices[idxIdx++] = a; indices[idxIdx++] = d; indices[idxIdx++] = c;
  }
}
function buildTerrainGeometry(data) {
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iy * GRID + ix;
      const idx3 = i * 3;
      const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const z = (iy / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const el = data.terrain[i];
      positions[idx3] = x;
      positions[idx3 + 1] = el * TERRAIN_HEIGHT;
      positions[idx3 + 2] = z;
      const col = elevationColor(el, data.vegetation[i]);
      colors[idx3] = col.r;
      colors[idx3 + 1] = col.g;
      colors[idx3 + 2] = col.b;
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(new THREE.BufferAttribute(indices, 1));
  geo.computeVertexNormals();
  return geo;
}
function rebuildTerrain(data) {
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
  }
  const geo = buildTerrainGeometry(data);
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.05,
    flatShading: false
  });
  terrainMesh = new THREE.Mesh(geo, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
}
function updateTerrainBuffers(data) {
  if (!terrainMesh) { rebuildTerrain(data); return; }
  const posAttr = terrainMesh.geometry.attributes.position;
  const colAttr = terrainMesh.geometry.attributes.color;
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iy * GRID + ix;
      const idx3 = i * 3;
      const x = (ix / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const z = (iy / (GRID - 1) - 0.5) * TERRAIN_SIZE;
      const el = data.terrain[i];
      posAttr.array[idx3] = x;
      posAttr.array[idx3 + 1] = el * TERRAIN_HEIGHT;
      posAttr.array[idx3 + 2] = z;
      const col = elevationColor(el, data.vegetation[i]);
      colAttr.array[idx3] = col.r;
      colAttr.array[idx3 + 1] = col.g;
      colAttr.array[idx3 + 2] = col.b;
    }
  }
  posAttr.needsUpdate = true;
  colAttr.needsUpdate = true;
  terrainMesh.geometry.computeVertexNormals();
}
function clearRivers() {
  riverLines.forEach(l => { l.geometry.dispose(); l.material.dispose(); scene.remove(l); });
  riverLines = [];
}
function buildRivers(data) {
  clearRivers();
  const threshold = 0.55;
  const riverPoints = [];
  const visited = new Uint8Array(GRID * GRID);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iy * GRID + ix;
      if (data.errors[i] < threshold || visited[i]) continue;
      const segment = [];
      let cx = ix, cy = iy;
      let steps = 0;
      while (steps < 120) {
        const ci = cy * GRID + cx;
        if (cx < 0 || cx >= GRID || cy < 0 || cy >= GRID || visited[ci]) break;
        visited[ci] = 1;
        const x = (cx / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        const z = (cy / (GRID - 1) - 0.5) * TERRAIN_SIZE;
        const el = data.terrain[ci] * TERRAIN_HEIGHT;
        segment.push(new THREE.Vector3(x, el + 0.08, z));
        let bestDir = [-1, -1], bestErr = -1;
        for (const [dx, dy] of [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]) {
          const nx = cx + dx, ny = cy + dy;
          if (nx >= 0 && nx < GRID && ny >= 0 && ny < GRID) {
            const ni = ny * GRID + nx;
            if (!visited[ni] && data.errors[ni] > bestErr) { bestErr = data.errors[ni]; bestDir = [dx, dy]; }
          }
        }
        if (bestErr < threshold) break;
        cx += bestDir[0]; cy += bestDir[1];
        steps++;
      }
      if (segment.length > 3) riverPoints.push(segment);
    }
  }
  const riverMat = new THREE.LineBasicMaterial({ color: 0xe04040, linewidth: 1, transparent: true, opacity: 0.85, depthTest: true });
  riverPoints.forEach(pts => {
    const geo = new THREE.BufferGeometry().setFromPoints(pts);
    const line = new THREE.Line(geo, riverMat);
    line.renderOrder = 1;
    scene.add(line);
    riverLines.push(line);
  });
}
const particleDummy = new THREE.Object3D();
let particleInstancedMesh = null;
let particleFlowData = [];
let particlePhases = new Float32Array(PARTICLE_CAPACITY);
let particleSpeeds = new Float32Array(PARTICLE_CAPACITY);
let particleActive = 0;
function buildParticleSystem() {
  if (particleInstancedMesh) {
    particleInstancedMesh.geometry.dispose();
    particleInstancedMesh.material.dispose();
    scene.remove(particleInstancedMesh);
  }
  const dotGeo = new THREE.SphereGeometry(0.08, 6, 4);
  const dotMat = new THREE.MeshBasicMaterial({ color: 0xffaa33, transparent: true, opacity: 0.85, depthTest: true });
  particleInstancedMesh = new THREE.InstancedMesh(dotGeo, dotMat, PARTICLE_CAPACITY);
  particleInstancedMesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  particleInstancedMesh.renderOrder = 2;
  particleInstancedMesh.frustumCulled = false;
  for (let i = 0; i < PARTICLE_CAPACITY; i++) {
    particleDummy.position.set(0, -100, 0);
    particleDummy.scale.set(0, 0, 0);
    particleDummy.updateMatrix();
    particleInstancedMesh.setMatrixAt(i, particleDummy.matrix);
    particleInstancedMesh.setColorAt(i, new THREE.Color(0xffaa33));
  }
  particleInstancedMesh.instanceMatrix.needsUpdate = true;
  if (particleInstancedMesh.instanceColor) particleInstancedMesh.instanceColor.needsUpdate = true;
  scene.add(particleInstancedMesh);
}
function resetParticles(data) {
  particleFlowData = data.flows.slice(0, PARTICLE_CAPACITY);
  particleActive = Math.min(data.flows.length, PARTICLE_CAPACITY);
  for (let i = 0; i < PARTICLE_CAPACITY; i++) {
    particlePhases[i] = Math.random();
    particleSpeeds[i] = 0.3 + Math.random() * 0.7;
  }
}
function updateParticles(data, dt) {
  if (!particleInstancedMesh) return;
  for (let i = 0; i < particleActive; i++) {
    particlePhases[i] += particleSpeeds[i] * dt * 0.5;
    if (particlePhases[i] > 1) particlePhases[i] -= 1;
    const flow = particleFlowData[i];
    if (!flow) { particleDummy.scale.set(0, 0, 0); particleDummy.position.set(0, -100, 0); }
    else {
      const t = particlePhases[i];
      const fx = flow.fromX / (GRID - 1) - 0.5;
      const fz = flow.fromY / (GRID - 1) - 0.5;
      const tx = flow.toX / (GRID - 1) - 0.5;
      const tz = flow.toY / (GRID - 1) - 0.5;
      const px = (fx + (tx - fx) * t) * TERRAIN_SIZE;
      const pz = (fz + (tz - fz) * t) * TERRAIN_SIZE;
      const gx = Math.max(0, Math.min(GRID - 1, Math.round((px / TERRAIN_SIZE + 0.5) * (GRID - 1))));
      const gz = Math.max(0, Math.min(GRID - 1, Math.round((pz / TERRAIN_SIZE + 0.5) * (GRID - 1))));
      const el = data.terrain[gz * GRID + gx] * TERRAIN_HEIGHT + 0.25;
      const intensity = flow.intensity || 0.5;
      const scale = 0.4 + intensity * 0.8;
      particleDummy.position.set(px, el, pz);
      particleDummy.scale.set(scale, scale, scale);
    }
    particleDummy.updateMatrix();
    particleInstancedMesh.setMatrixAt(i, particleDummy.matrix);
  }
  for (let i = particleActive; i < PARTICLE_CAPACITY; i++) {
    particleDummy.scale.set(0, 0, 0);
    particleDummy.position.set(0, -100, 0);
    particleDummy.updateMatrix();
    particleInstancedMesh.setMatrixAt(i, particleDummy.matrix);
  }
  particleInstancedMesh.instanceMatrix.needsUpdate = true;
}
const raycaster = new THREE.Raycaster();
raycaster.far = 50;
const mouse = new THREE.Vector2();
function updateTooltip(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(mouse, camera);
  if (!terrainMesh) { tooltip.classList.remove('visible'); return; }
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const pt = intersects[0].point;
    const ix = Math.round((pt.x / TERRAIN_SIZE + 0.5) * (GRID - 1));
    const iy = Math.round((pt.z / TERRAIN_SIZE + 0.5) * (GRID - 1));
    const data = allFramesData[currentFrame];
    const s = sampleData(data, ix, iy);
    document.getElementById('tt-elev').textContent = (s.terrain * 100).toFixed(1) + '%';
    document.getElementById('tt-veg').textContent = (s.vegetation * 100).toFixed(1) + '%';
    document.getElementById('tt-err').textContent = (s.errors * 100).toFixed(1) + '%';
    tooltip.style.left = (event.clientX + 18) + 'px';
    tooltip.style.top = (event.clientY - 10) + 'px';
    tooltip.classList.add('visible');
  } else {
    tooltip.classList.remove('visible');
  }
}
window.addEventListener('mousemove', updateTooltip, { passive: true });
window.addEventListener('mouseleave', () => tooltip.classList.remove('visible'));
const bookmarks = {
  overview: { pos: [16, 12, 18], target: [0, 2, 0] },
  north: { pos: [0, 16, 22], target: [0, 2, 0] },
  valley: { pos: [-8, 5, -10], target: [-3, 1, -3] },
  peak: { pos: [4, 5, 4], target: [2, 3.5, 2] }
};
document.querySelectorAll('.bm-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const bm = bookmarks[btn.dataset.bm];
    if (!bm) return;
    controls.target.set(...bm.target);
    camera.position.set(...bm.pos);
    controls.update();
  });
});
timeSlider.addEventListener('input', () => {
  currentFrame = parseInt(timeSlider.value);
  const h = Math.floor(currentFrame);
  const m = Math.round((currentFrame - h) * 60);
  timeLabel.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;
  updateTerrainBuffers(allFramesData[currentFrame]);
  buildRivers(allFramesData[currentFrame]);
  resetParticles(allFramesData[currentFrame]);
});
document.getElementById('btn-sample').addEventListener('click', () => {
  const seed = Date.now() % 1000;
  const sampleTerrain = new Float32Array(GRID * GRID);
  const sampleVeg = new Float32Array(GRID * GRID);
  const sampleErrors = new Float32Array(GRID * GRID);
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const nx = ix / GRID * 6 - 3, ny = iy / GRID * 6 - 3;
      const dist = Math.sqrt(nx * nx + ny * ny) / 4;
      const peak1 = Math.exp(-((nx - 0.8) * (nx - 0.8) + (ny - 0.4) * (ny - 0.4)) / 2.5);
      const peak2 = Math.exp(-((nx + 1.2) * (nx + 1.2) + (ny + 0.8) * (ny + 0.8)) / 3.0);
      const peak3 = Math.exp(-((nx - 0.1) * (nx - 0.1) + (ny + 1.5) * (ny + 1.5)) / 2.0);
      const el = peak1 * 0.8 + peak2 * 0.65 + peak3 * 0.5 + fbm(nx + seed, ny + seed, 3) * 0.2 - dist * 0.15;
      sampleTerrain[iy * GRID + ix] = Math.max(0, el);
      sampleVeg[iy * GRID + ix] = fbm(nx + seed + 7, ny + seed + 2, 4);
      sampleErrors[iy * GRID + ix] = Math.max(0, (1 - el) * 0.7 * fbm(nx + seed + 12, ny + seed - 3, 3));
    }
  }
  const flows = [];
  for (let i = 0; i < 120; i++) {
    const fx = Math.random() * GRID, fy = Math.random() * GRID;
    flows.push({ fromX: fx, fromY: fy, toX: fx + (Math.random() - 0.5) * GRID * 0.4, toY: fy + (Math.random() - 0.5) * GRID * 0.4, intensity: 0.4 + Math.random() * 0.6 });
  }
  const sampleFrame = { terrain: sampleTerrain, vegetation: sampleVeg, errors: sampleErrors, flows };
  allFramesData = [sampleFrame];
  timeSlider.max = '0';
  timeSlider.value = '0';
  currentFrame = 0;
  updateTerrainBuffers(sampleFrame);
  buildRivers(sampleFrame);
  resetParticles(sampleFrame);
  timeLabel.textContent = '00:00';
});
document.getElementById('btn-noise').addEventListener('click', () => {
  const seed = Math.floor(Math.random() * 10000);
  allFramesData = generateAllFrames(seed);
  timeSlider.max = String(TIME_FRAMES - 1);
  timeSlider.value = '0';
  currentFrame = 0;
  updateTerrainBuffers(allFramesData[0]);
  buildRivers(allFramesData[0]);
  resetParticles(allFramesData[0]);
  timeLabel.textContent = '00:00';
});
let autoRotate = true;
document.getElementById('btn-auto-rotate').addEventListener('click', function() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  this.textContent = autoRotate ? 'Auto-Rotate: ON' : 'Auto-Rotate: OFF';
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
const seed = 42;
allFramesData = generateAllFrames(seed);
rebuildTerrain(allFramesData[0]);
buildRivers(allFramesData[0]);
buildParticleSystem();
resetParticles(allFramesData[0]);
loadingEl.classList.add('hidden');
let lastTime = performance.now();
let fpsCount = 0;
let fpsTimer = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  const dt = Math.min((timestamp - lastTime) / 1000, 0.2);
  lastTime = timestamp;
  controls.update();
  const data = allFramesData[currentFrame];
  updateParticles(data, dt);
  fpsCount++;
  fpsTimer += dt;
  if (fpsTimer >= 1) {
    fpsEl.textContent = `FPS: ${Math.round(fpsCount / fpsTimer)}`;
    fpsCount = 0;
    fpsTimer = 0;
  }
  renderer.render(scene, camera);
}
requestAnimationFrame(animate);
</script>
</body>
</html>