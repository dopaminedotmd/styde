<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 100%; height: 100%; overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; }
  #container { width: 100%; height: 100%; position: relative; }
  canvas { display: block; }
  #ui-layer {
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none;
    z-index: 10;
  }
  #ui-layer > * { pointer-events: auto; }
  #loading-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(10,10,20,0.92);
    z-index: 100;
  }
  #loading-spinner {
    width: 48px; height: 48px;
    border: 3px solid rgba(100,180,255,0.2);
    border-top-color: rgba(100,180,255,0.9);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  #error-overlay {
    position: absolute;
    inset: 0;
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(10,10,20,0.95);
    z-index: 101;
    color: #ff6b6b;
    text-align: center;
    padding: 2rem;
  }
  #error-overlay .retry-btn {
    margin-top: 1.2rem;
    padding: 0.6rem 1.8rem;
    background: #ff6b6b;
    color: #0a0a14;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
  }
  #empty-overlay {
    position: absolute;
    inset: 0;
    display: none;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(10,10,20,0.9);
    z-index: 99;
    color: rgba(255,255,255,0.6);
    text-align: center;
    padding: 2rem;
  }
  #panel {
    position: absolute;
    bottom: 16px; left: 16px;
    background: rgba(10,10,20,0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 14px 18px;
    color: #ccc;
    font-size: 13px;
    max-width: 260px;
    z-index: 20;
  }
  #panel .label { color: rgba(255,255,255,0.5); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
  #panel .value { color: #fff; font-size: 18px; font-weight: 600; margin-bottom: 6px; }
  #legend {
    position: absolute;
    bottom: 16px; right: 16px;
    background: rgba(10,10,20,0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 12px 16px;
    color: #ccc;
    font-size: 12px;
    z-index: 20;
  }
  .legend-row { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
  #timeline {
    position: absolute;
    bottom: 100px; left: 50%;
    transform: translateX(-50%);
    background: rgba(10,10,20,0.85);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 10px 18px;
    z-index: 20;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  #time-slider {
    width: 240px;
    accent-color: #64b4ff;
    cursor: pointer;
  }
  #time-label {
    color: #ccc;
    font-size: 13px;
    min-width: 80px;
    text-align: center;
  }
  #bookmarks {
    position: absolute;
    top: 16px; right: 16px;
    display: flex;
    gap: 6px;
    z-index: 20;
  }
  .bookmark-btn {
    background: rgba(10,10,20,0.8);
    border: 1px solid rgba(255,255,255,0.2);
    color: #ccc;
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s;
  }
  .bookmark-btn:hover { background: rgba(100,180,255,0.2); border-color: rgba(100,180,255,0.5); }
  .bookmark-btn.active { background: rgba(100,180,255,0.3); border-color: #64b4ff; color: #fff; }
  #help {
    position: absolute;
    top: 16px; left: 16px;
    color: rgba(255,255,255,0.4);
    font-size: 11px;
    z-index: 20;
  }
  #non-webgl {
    display: none;
    position: absolute;
    inset: 0;
    background: #0a0a14;
    color: #ccc;
    align-items: center;
    justify-content: center;
    z-index: 200;
    text-align: center;
    padding: 2rem;
  }
</style>
</head>
<body>
<div id="non-webgl">Your browser does not support WebGL. This visualization requires a WebGL-enabled browser.</div>
<div id="container"></div>
<div id="ui-layer">
  <div id="loading-overlay"><div id="loading-spinner"></div></div>
  <div id="error-overlay">
    <div id="error-msg">Failed to initialize</div>
    <button class="retry-btn" onclick="init()">Retry</button>
  </div>
  <div id="empty-overlay">No data available for the selected time range.</div>
  <div id="help">Drag: orbit · Scroll: zoom · Right-drag: pan · 1-3: bookmarks</div>
  <div id="bookmarks">
    <button class="bookmark-btn" data-idx="0">Overview</button>
    <button class="bookmark-btn" data-idx="1">Top-down</button>
    <button class="bookmark-btn" data-idx="2">Close-up</button>
  </div>
  <div id="panel">
    <div class="label">Revenue (Elevation)</div>
    <div class="value" id="val-revenue">—</div>
    <div class="label">User Density (Color)</div>
    <div class="value" id="val-users">—</div>
    <div class="label">Error Rate</div>
    <div class="value" id="val-errors">—</div>
  </div>
  <div id="legend">
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#1a4a2a,#8bc34a,#ffeb3b);"></span> User Density</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#ff4444;"></span> Error Flow (Rivers)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#64b4ff;"></span> API Traffic (Particles)</div>
  </div>
  <div id="timeline">
    <span style="color:#888;font-size:12px;">Time</span>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label">T+0</span>
  </div>
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
const GRID = 120;
const SPACING = 0.25;
const TERRAIN_W = (GRID - 1) * SPACING;
const TERRAIN_VERT_COUNT = GRID * GRID;
const RIVER_SEGMENTS = 80;
let scene, camera, renderer, controls;
let terrainMesh, riverLine, particlePoints;
let terrainPositions, terrainColors, particlePositions, particleVelocities;
let particleGeometry;
let timeFrames = [];
let currentTimeIdx = 0;
let animationId;
let clock = new THREE.Clock();
let bookmarks = [
  { pos: new THREE.Vector3(18, 14, 18), target: new THREE.Vector3(TERRAIN_W/2, 0, TERRAIN_W/2) },
  { pos: new THREE.Vector3(TERRAIN_W/2, 28, TERRAIN_W/2 + 0.5), target: new THREE.Vector3(TERRAIN_W/2, 0, TERRAIN_W/2) },
  { pos: new THREE.Vector3(TERRAIN_W/2 - 2, 4, TERRAIN_W/2 - 6), target: new THREE.Vector3(TERRAIN_W/2 + 2, 1.5, TERRAIN_W/2 + 2) }
];
let activeBookmark = -1;
function generateTimeFrames(count) {
  const frames = [];
  const peaks = [];
  for (let i = 0; i < 6; i++) {
    peaks.push({
      cx: 0.15 + Math.random() * 0.7,
      cz: 0.15 + Math.random() * 0.7,
      phase: Math.random() * Math.PI * 2,
      driftX: (Math.random() - 0.5) * 0.015,
      driftZ: (Math.random() - 0.5) * 0.015
    });
  }
  for (let t = 0; t < count; t++) {
    const revenue = new Float32Array(GRID * GRID);
    const userDensity = new Float32Array(GRID * GRID);
    const errorField = new Float32Array(GRID * GRID);
    const tp = t / count;
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iz * GRID + ix;
        const nx = ix / (GRID - 1);
        const nz = iz / (GRID - 1);
        let h = 0;
        for (const p of peaks) {
          const cx = p.cx + p.driftX * t;
          const cz = p.cz + p.driftZ * t;
          const dx = (nx - cx) * 3;
          const dz = (nz - cz) * 3;
          const dist = Math.sqrt(dx * dx + dz * dz);
          const amp = 0.5 + 0.5 * Math.sin(p.phase + tp * Math.PI * 2);
          h += amp * Math.exp(-dist * dist * 1.8) * 5;
        }
        h += 0.3 * Math.sin(nx * 8 + tp * Math.PI) * Math.cos(nz * 6 + tp * Math.PI * 0.7);
        revenue[idx] = Math.max(0, h);
        const ux = nx * 5 + tp * 2;
        const uz = nz * 5;
        userDensity[idx] = 0.15 + 0.85 * (
          0.4 * Math.sin(ux) * Math.cos(uz) +
          0.3 * Math.sin(ux * 2.3 + 1.5) * Math.cos(uz * 1.8) +
          0.3 * Math.cos(ux * 1.1 + uz * 1.4)
        );
        userDensity[idx] = (userDensity[idx] + 1) / 2;
        errorField[idx] = Math.max(0,
          0.08 * Math.sin(nx * 12 + tp * 4) * Math.cos(nz * 10) +
          0.05 * revenue[idx] * (0.3 + 0.7 * Math.abs(Math.sin(nx * 6 + nz * 6 + tp * 8)))
        );
      }
    }
    frames.push({ revenue, userDensity, errorField });
  }
  return frames;
}
function getTerrainHeight(px, pz, frame) {
  const ix = Math.round(px / SPACING);
  const iz = Math.round(pz / SPACING);
  const ci = Math.max(0, Math.min(GRID - 1, iz)) * GRID + Math.max(0, Math.min(GRID - 1, ix));
  return frame.revenue[ci];
}
function updateTerrainBuffer(frame) {
  if (!terrainPositions || !terrainColors) return;
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const i3 = idx * 3;
      const h = frame.revenue[idx];
      terrainPositions[i3 + 1] = h;
      const dens = frame.userDensity[idx];
      const r = 0.1 + dens * 0.55;
      const g = 0.29 + dens * 0.45;
      const b = 0.16 + dens * 0.08;
      terrainColors[i3] = r;
      terrainColors[i3 + 1] = g;
      terrainColors[i3 + 2] = b;
    }
  }
  terrainMesh.geometry.attributes.position.needsUpdate = true;
  terrainMesh.geometry.attributes.color.needsUpdate = true;
  terrainMesh.geometry.computeVertexNormals();
}
function buildRiverPath(frame) {
  const points = [];
  let cx = TERRAIN_W * 0.1;
  let cz = TERRAIN_W * 0.15;
  for (let i = 0; i < RIVER_SEGMENTS; i++) {
    const t = i / (RIVER_SEGMENTS - 1);
    const ix = Math.round(cx / SPACING);
    const iz = Math.round(cz / SPACING);
    const ci = Math.max(0, Math.min(GRID - 1, iz)) * GRID + Math.max(0, Math.min(GRID - 1, ix));
    const gradErr = frame.errorField[ci];
    const gx = (frame.errorField[Math.min(GRID * GRID - 1, ci + 1)] || 0) -
               (frame.errorField[Math.max(0, ci - 1)] || 0);
    const gz = (frame.errorField[Math.min(GRID * GRID - 1, ci + GRID)] || 0) -
               (frame.errorField[Math.max(0, ci - GRID)] || 0);
    const gmag = Math.sqrt(gx * gx + gz * gz) || 0.001;
    cx += (gx / gmag) * 0.35 + (Math.random() - 0.5) * 0.15;
    cz += (gz / gmag) * 0.35 + (Math.random() - 0.5) * 0.15;
    cx = Math.max(0.5, Math.min(TERRAIN_W - 0.5, cx));
    cz = Math.max(0.5, Math.min(TERRAIN_W - 0.5, cz));
    const h = getTerrainHeight(cx, cz, frame) + 0.15;
    points.push(new THREE.Vector3(cx, h, cz));
  }
  return points;
}
function updateRiverGeometry(frame) {
  const path = buildRiverPath(frame);
  const curve = new THREE.CatmullRomCurve3(path);
  const curvePoints = curve.getPoints(RIVER_SEGMENTS * 2);
  const positions = riverLine.geometry.attributes.position.array;
  for (let i = 0; i < curvePoints.length && i * 3 + 2 < positions.length; i++) {
    positions[i * 3] = curvePoints[i].x;
    positions[i * 3 + 1] = curvePoints[i].y;
    positions[i * 3 + 2] = curvePoints[i].z;
  }
  riverLine.geometry.attributes.position.needsUpdate = true;
  riverLine.geometry.setDrawRange(0, Math.min(curvePoints.length, positions.length / 3));
}
function updateParticles(frame, dt) {
  const posArr = particleGeometry.attributes.position.array;
  const COUNT = posArr.length / 3;
  for (let i = 0; i < COUNT; i++) {
    const i3 = i * 3;
    let px = posArr[i3];
    let py = posArr[i3 + 1];
    let pz = posArr[i3 + 2];
    const vx = particleVelocities[i3];
    const vz = particleVelocities[i3 + 2];
    px += vx * dt;
    pz += vz * dt;
    if (px < 0 || px > TERRAIN_W || pz < 0 || pz > TERRAIN_W ||
        Math.random() < dt * 0.6) {
      px = Math.random() * TERRAIN_W;
      pz = Math.random() * TERRAIN_W;
      particleVelocities[i3] = (Math.random() - 0.5) * 6;
      particleVelocities[i3 + 2] = (Math.random() - 0.5) * 6;
    }
    const targetY = getTerrainHeight(px, pz, frame) + 0.4;
    py += (targetY - py) * 3 * dt;
    const ix = Math.round(px / SPACING);
    const iz = Math.round(pz / SPACING);
    const ci = Math.max(0, Math.min(GRID - 1, iz)) * GRID + Math.max(0, Math.min(GRID - 1, ix));
    const err = frame.errorField[ci];
    if (err > 0.15 && Math.random() < err * 8 * dt) {
      py += (Math.random() - 0.5) * 2;
    }
    posArr[i3] = px;
    posArr[i3 + 1] = py;
    posArr[i3 + 2] = pz;
  }
  particleGeometry.attributes.position.needsUpdate = true;
}
function createTerrainGeometry() {
  const geom = new THREE.BufferGeometry();
  terrainPositions = new Float32Array(TERRAIN_VERT_COUNT * 3);
  terrainColors = new Float32Array(TERRAIN_VERT_COUNT * 3);
  const indices = [];
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      terrainPositions[idx * 3] = ix * SPACING;
      terrainPositions[idx * 3 + 1] = 0;
      terrainPositions[idx * 3 + 2] = iz * SPACING;
      terrainColors[idx * 3] = 0.1;
      terrainColors[idx * 3 + 1] = 0.29;
      terrainColors[idx * 3 + 2] = 0.16;
    }
  }
  for (let iz = 0; iz < GRID - 1; iz++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iz * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geom.setAttribute('position', new THREE.BufferAttribute(terrainPositions, 3));
  geom.setAttribute('color', new THREE.BufferAttribute(terrainColors, 3));
  geom.setIndex(indices);
  return geom;
}
function createParticleGeometry(count) {
  const geom = new THREE.BufferGeometry();
  particlePositions = new Float32Array(count * 3);
  particleVelocities = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    particlePositions[i * 3] = Math.random() * TERRAIN_W;
    particlePositions[i * 3 + 1] = 1 + Math.random() * 4;
    particlePositions[i * 3 + 2] = Math.random() * TERRAIN_W;
    particleVelocities[i * 3] = (Math.random() - 0.5) * 6;
    particleVelocities[i * 3 + 2] = (Math.random() - 0.5) * 6;
  }
  geom.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  return geom;
}
function createRiverGeometry() {
  const geom = new THREE.BufferGeometry();
  const pos = new Float32Array(RIVER_SEGMENTS * 2 * 3);
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geom.setDrawRange(0, 0);
  return geom;
}
function showOverlay(id) {
  document.getElementById('loading-overlay').style.display = 'none';
  document.getElementById('error-overlay').style.display = 'none';
  document.getElementById('empty-overlay').style.display = 'none';
  if (id) document.getElementById(id).style.display = 'flex';
}
function hideAllOverlays() {
  showOverlay(null);
}
function init() {
  try {
    const container = document.getElementById('container');
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
    if (!gl) {
      document.getElementById('non-webgl').style.display = 'flex';
      return;
    }
    showOverlay('loading-overlay');
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a14);
    scene.fog = new THREE.Fog(0x0a0a14, 20, 55);
    camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 100);
    camera.position.copy(bookmarks[0].pos);
    camera.lookAt(bookmarks[0].target);
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);
    controls = new OrbitControls(camera, renderer.domElement);
    controls.target.copy(bookmarks[0].target);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.3;
    controls.minDistance = 3;
    controls.maxDistance = 45;
    controls.maxPolarAngle = Math.PI * 0.48;
    controls.update();
    const ambient = new THREE.AmbientLight(0x334466, 1.8);
    scene.add(ambient);
    const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
    sun.position.set(15, 20, 10);
    scene.add(sun);
    const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
    fill.position.set(-8, 5, -5);
    scene.add(fill);
    const gridHelper = new THREE.GridHelper(TERRAIN_W, 20, 0x223344, 0x111122);
    gridHelper.position.y = -0.02;
    scene.add(gridHelper);
    const terrainGeom = createTerrainGeometry();
    const terrainMat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.65,
      metalness: 0.05,
      flatShading: false,
      side: THREE.DoubleSide
    });
    terrainMesh = new THREE.Mesh(terrainGeom, terrainMat);
    terrainMesh.receiveShadow = true;
    terrainMesh.castShadow = true;
    scene.add(terrainMesh);
    const riverGeom = createRiverGeometry();
    const riverMat = new THREE.LineBasicMaterial({
      color: 0xff3333,
      linewidth: 1,
      transparent: true,
      opacity: 0.85
    });
    riverLine = new THREE.Line(riverGeom, riverMat);
    scene.add(riverLine);
    const particleGeom = createParticleGeometry(600);
    const particleMat = new THREE.PointsMaterial({
      color: 0x64b4ff,
      size: 0.18,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.7
    });
    particlePoints = new THREE.Points(particleGeom, particleMat);
    particleGeometry = particleGeom;
    scene.add(particlePoints);
    timeFrames = generateTimeFrames(100);
    if (timeFrames.length === 0) {
      showOverlay('empty-overlay');
    } else {
      updateTerrainBuffer(timeFrames[0]);
      updateRiverGeometry(timeFrames[0]);
    }
    setupUI();
    hideAllOverlays();
    clock.start();
    animate();
  } catch (err) {
    console.error(err);
    document.getElementById('error-msg').textContent = 'Initialization failed: ' + err.message;
    showOverlay('error-overlay');
  }
}
function animate() {
  animationId = requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  if (timeFrames.length > 0) {
    const frame = timeFrames[currentTimeIdx];
    updateParticles(frame, dt);
  }
  renderer.render(scene, camera);
}
function setTimeIndex(idx) {
  if (idx === currentTimeIdx || timeFrames.length === 0) return;
  currentTimeIdx = Math.max(0, Math.min(timeFrames.length - 1, idx));
  const frame = timeFrames[currentTimeIdx];
  updateTerrainBuffer(frame);
  updateRiverGeometry(frame);
  document.getElementById('time-slider').value = currentTimeIdx;
  document.getElementById('time-label').textContent = 'T+' + currentTimeIdx;
  const ix = Math.round(TERRAIN_W / 2 / SPACING);
  const ci = Math.round(GRID / 2) * GRID + Math.round(GRID / 2);
  document.getElementById('val-revenue').textContent = frame.revenue[ci].toFixed(2);
  document.getElementById('val-users').textContent = (frame.userDensity[ci] * 100).toFixed(0) + '%';
  document.getElementById('val-errors').textContent = (frame.errorField[ci] * 100).toFixed(1) + '%';
}
function setBookmark(idx) {
  activeBookmark = idx;
  const bm = bookmarks[idx];
  camera.position.copy(bm.pos);
  controls.target.copy(bm.target);
  controls.update();
  document.querySelectorAll('.bookmark-btn').forEach((btn, i) => {
    btn.classList.toggle('active', i === idx);
  });
}
function setupUI() {
  const slider = document.getElementById('time-slider');
  slider.max = timeFrames.length - 1;
  slider.addEventListener('input', () => setTimeIndex(parseInt(slider.value)));
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', () => setBookmark(parseInt(btn.dataset.idx)));
  });
  window.addEventListener('resize', () => {
    const c = document.getElementById('container');
    camera.aspect = c.clientWidth / c.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(c.clientWidth, c.clientHeight);
  });
  window.addEventListener('keydown', (e) => {
    const key = e.key;
    if (key === '1') setBookmark(0);
    else if (key === '2') setBookmark(1);
    else if (key === '3') setBookmark(2);
    else if (key === 'ArrowLeft' || key === 'ArrowRight') {
      const delta = key === 'ArrowRight' ? 1 : -1;
      setTimeIndex(currentTimeIdx + delta);
    }
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && animationId) {
      cancelAnimationFrame(animationId);
      animationId = null;
    } else if (!document.hidden && !animationId) {
      clock.getDelta();
      animate();
    }
  });
  setTimeIndex(0);
  setBookmark(0);
  setTimeout(() => {
    const container = document.getElementById('container');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
  }, 100);
}
init();
</script>
</body>
</html>