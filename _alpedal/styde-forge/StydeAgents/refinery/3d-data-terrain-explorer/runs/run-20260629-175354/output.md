<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a1a; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #dde; }
  #canvas-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; }
  #ui-panel { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(10,10,26,0.92); border: 1px solid #2a2a4a; border-radius: 12px; padding: 16px 24px; display: flex; gap: 24px; align-items: center; backdrop-filter: blur(12px); z-index: 10; }
  #ui-panel label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #88a; }
  #time-slider { width: 280px; accent-color: #6af; }
  #time-display { font-size: 13px; color: #aac; min-width: 80px; text-align: center; }
  .btn { background: #1a1a3a; border: 1px solid #3a3a5a; color: #aac; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; letter-spacing: 0.5px; transition: all 0.2s; }
  .btn:hover { background: #2a2a5a; border-color: #6af; color: #fff; }
  .btn.active { background: #2a4a6a; border-color: #6af; color: #fff; }
  #bookmark-bar { position: fixed; top: 20px; right: 20px; display: flex; gap: 8px; z-index: 10; }
  #cache-panel { position: fixed; top: 20px; left: 20px; background: rgba(10,10,26,0.85); border: 1px solid #2a2a4a; border-radius: 8px; padding: 10px 16px; font-size: 11px; color: #6a6; z-index: 10; backdrop-filter: blur(8px); }
  #cache-panel span { color: #af8; }
  #legend { position: fixed; bottom: 100px; right: 20px; background: rgba(10,10,26,0.85); border: 1px solid #2a2a4a; border-radius: 8px; padding: 12px; z-index: 10; backdrop-filter: blur(8px); }
  .legend-row { display: flex; align-items: center; gap: 8px; margin: 4px 0; font-size: 11px; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="cache-panel">
  Cache hits: <span id="cache-hits">0</span> | misses: <span id="cache-misses">0</span> | ratio: <span id="cache-ratio">0%</span>
</div>
<div id="bookmark-bar">
  <button class="btn" onclick="saveBookmark()" title="Save current camera position">+ Bookmark</button>
</div>
<div id="legend">
  <div style="font-size:11px;color:#88a;margin-bottom:6px;">Terrain Color: User Density</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#1a4a1a;"></div> Low density</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#4a8a2a;"></div> Medium</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#8aca3a;"></div> High density</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#cafa5a;"></div> Peak density</div>
  <div class="legend-row" style="margin-top:6px;color:#f66;">━ Rivers: Error/anomaly paths</div>
  <div class="legend-row" style="color:#ffa;">✦ Particles: API call flows</div>
</div>
<div id="ui-panel">
  <label>Time</label>
  <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
  <span id="time-display">T+0h</span>
  <button class="btn" id="btn-auto-rotate" onclick="toggleAutoRotate()">Auto-Rotate</button>
  <button class="btn" id="btn-top" onclick="goToView('top')">Top</button>
  <button class="btn" id="btn-front" onclick="goToView('front')">Front</button>
  <button class="btn" id="btn-reset" onclick="goToView('default')">Reset</button>
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
const GRID = 128;                    /* heightfield resolution: 128x128 vertices */
const TERRAIN_SIZE = 20;            /* world-space extent of the terrain square */
const TIME_STEPS = 100;             /* number of discrete time samples */
/* Cache layer — stores precomputed geometry variants keyed by time index.
   Hit/miss counters exposed via the diagnostics panel. */
const cache = {
  terrain: new Map(),               /* timeIndex -> {geometry, heightData} */
  rivers: new Map(),                /* timeIndex -> BufferGeometry */
  particles: null,                  /* single reusable particle system; positions updated per tick */
  hits: 0,
  misses: 0,
  logHit() { this.hits++; this.updatePanel(); },
  logMiss() { this.misses++; this.updatePanel(); },
  updatePanel() {
    const total = this.hits + this.misses;
    const ratio = total > 0 ? Math.round((this.hits / total) * 100) : 0;
    document.getElementById('cache-hits').textContent = this.hits;
    document.getElementById('cache-misses').textContent = this.misses;
    document.getElementById('cache-ratio').textContent = ratio + '%';
  }
};
/* Synthetic time-series dataset.
   Each column: [revenue (elevation), userDensity (color), errorRate (rivers)] */
function generateDataset() {
  const data = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const phase = t / TIME_STEPS;
    const frame = [];
    for (let i = 0; i < GRID; i++) {
      const row = [];
      for (let j = 0; j < GRID; j++) {
        const nx = (i / GRID) * 2 - 1;
        const ny = (j / GRID) * 2 - 1;
        /* Multi-octave synthetic terrain that drifts over time */
        const r1 = Math.sin(nx * 3.5 + phase * Math.PI) * Math.cos(ny * 4.1 + phase * 1.7);
        const r2 = Math.sin(nx * 7.2 - phase * 0.8) * Math.cos(ny * 6.3 + phase * 2.1) * 0.4;
        const r3 = Math.sin(nx * 1.3 + phase * 3.0) * Math.cos(ny * 1.9 - phase * 1.1) * 0.7;
        const revenue = Math.max(0, (r1 + r2 + r3 + 0.6) * 2.5);
        const density = Math.max(0, (Math.sin(nx * 2.7 + phase * 1.3) * Math.cos(ny * 3.4 - phase * 0.9) + 0.5) * 1.8);
        const error = Math.abs(Math.sin(nx * 5.0 + phase * 2.5) * Math.cos(ny * 4.5 - phase * 1.6)) * (0.05 + phase * 0.18);
        row.push({ revenue, density, error });
      }
      frame.push(row);
    }
    data.push(frame);
  }
  return data;
}
const dataset = generateDataset();
/* Build terrain geometry for a given time index.
   Elevation = revenue, vertex color = user density gradient. */
function buildTerrainGeometry(timeIndex) {
  if (cache.terrain.has(timeIndex)) {
    cache.logHit();
    return cache.terrain.get(timeIndex);
  }
  cache.logMiss();
  const frame = dataset[timeIndex];
  const segments = GRID - 1;
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const heightData = new Float32Array(GRID * GRID);
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / segments;
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = (i * GRID + j);
      const posIdx = idx * 3;
      const d = frame[i][j];
      const x = -half + j * step;
      const z = -half + i * step;
      const y = d.revenue;
      positions[posIdx] = x;
      positions[posIdx + 1] = y;
      positions[posIdx + 2] = z;
      heightData[idx] = y;
      /* Vertex color: green gradient mapped to user density.
         Low density = dark green, high = bright yellow-green. */
      const t = Math.min(1, Math.max(0, d.density / 2.0));
      colors[posIdx] = 0.1 + t * 0.15;
      colors[posIdx + 1] = 0.25 + t * 0.65;
      colors[posIdx + 2] = 0.1 + t * 0.12;
    }
  }
  /* Index array for triangulated grid (two triangles per cell) */
  const indices = [];
  for (let i = 0; i < segments; i++) {
    for (let j = 0; j < segments; j++) {
      const a = i * GRID + j;
      const b = a + 1;
      const c = (i + 1) * GRID + j;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  const result = { geometry: geo, heightData };
  cache.terrain.set(timeIndex, result);
  return result;
}
/* River geometry: trace error/anomaly paths as red tubes carving through the terrain.
   River paths follow the gradient of the error field downward — from high-error peaks
   along the steepest descent to local minima. One river per significant error hotspot. */
function buildRiverGeometry(timeIndex) {
  if (cache.rivers.has(timeIndex)) {
    cache.logHit();
    return cache.rivers.get(timeIndex);
  }
  cache.logMiss();
  const frame = dataset[timeIndex];
  const step = TERRAIN_SIZE / (GRID - 1);
  const half = TERRAIN_SIZE / 2;
  const threshold = 0.08;            /* minimum error to spawn a river head */
  const riverPaths = [];
  /* Find error hotspots — sample every 4th cell for performance */
  const hotspots = [];
  for (let i = 4; i < GRID - 4; i += 8) {
    for (let j = 4; j < GRID - 4; j += 8) {
      if (frame[i][j].error > threshold) {
        hotspots.push({ i, j, error: frame[i][j].error });
      }
    }
  }
  /* Keep top 6 hotspots to limit river count */
  hotspots.sort((a, b) => b.error - a.error);
  const topSpots = hotspots.slice(0, 6);
  /* Trace each river: follow steepest-descent in error field.
     Elevation (revenue) adds gravity — rivers flow downhill in revenue terrain too. */
  for (const spot of topSpots) {
    const path = [];
    let ci = spot.i, cj = spot.j;
    const maxSteps = 60;
    for (let s = 0; s < maxSteps; s++) {
      if (ci < 1 || ci >= GRID - 1 || cj < 1 || cj >= GRID - 1) break;
      const x = -half + cj * step;
      const z = -half + ci * step;
      const y = frame[ci][cj].revenue + 0.15; /* slight vertical offset above terrain */
      path.push(new THREE.Vector3(x, y, z));
      /* Compute next step: combined gradient of error + revenue elevation */
      let bestDi = 0, bestDj = 0;
      let bestVal = Infinity;
      for (const [di, dj] of [[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]]) {
        const ni = ci + di, nj = cj + dj;
        if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
        /* Composite: error gradient weight 0.7 + revenue gradient weight 0.3 */
        const val = frame[ni][nj].error * 0.7 + frame[ni][nj].revenue * 0.1;
        if (val < bestVal) { bestVal = val; bestDi = di; bestDj = dj; }
      }
      /* Stop if no downhill neighbor */
      if (bestDi === 0 && bestDj === 0) break;
      ci += bestDi;
      cj += bestDj;
      /* Stop if error drops below noise floor */
      if (frame[ci][cj].error < 0.02) break;
    }
    if (path.length >= 3) riverPaths.push(path);
  }
  /* Merge all river paths into a single BufferGeometry via merged TubeGeometry approach.
     Each path becomes a thin tube; all tubes merged into one geometry for single draw call. */
  const allGeos = [];
  for (const path of riverPaths) {
    const curve = new THREE.CatmullRomCurve3(path);
    /* TubeGeometry is created once per river at build time — NOT per frame.
       Cached in cache.rivers map keyed by timeIndex. */
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.12, 6, false);
    allGeos.push(tubeGeo);
  }
  /* Merge all tube geometries into one for rendering efficiency */
  let merged;
  if (allGeos.length === 0) {
    merged = new THREE.BufferGeometry();
  } else if (allGeos.length === 1) {
    merged = allGeos[0];
  } else {
    merged = THREE.BufferGeometryUtils.mergeGeometries
      ? THREE.BufferGeometryUtils.mergeGeometries(allGeos)
      : allGeos[0]; /* fallback if merge utility unavailable */
    /* Cleanup individual geos after merge to free GPU memory */
    for (const g of allGeos) { if (g !== merged) g.dispose(); }
  }
  cache.rivers.set(timeIndex, merged);
  return merged;
}
/* Particle system: flowing dot trails representing API calls / user actions.
   Particles follow precomputed flow-field paths across the terrain surface.
   Positions updated per-frame via BufferGeometry attribute reuse — no allocation in hot path. */
function buildParticleSystem(timeIndex) {
  const frame = dataset[timeIndex];
  const count = 2000;
  const step = TERRAIN_SIZE / (GRID - 1);
  const half = TERRAIN_SIZE / 2;
  /* Precompute start positions for all particles — cached, never rebuilt */
  if (!cache.particles) {
    const startPositions = new Float32Array(count * 4); /* x,y,z + flow-angle */
    const startColors = new Float32Array(count * 3);
    for (let k = 0; k < count; k++) {
      const i = Math.floor(Math.random() * GRID);
      const j = Math.floor(Math.random() * GRID);
      const x = -half + j * step;
      const z = -half + i * step;
      const y = frame[i][j].revenue + 0.25;
      startPositions[k * 4] = x;
      startPositions[k * 4 + 1] = y;
      startPositions[k * 4 + 2] = z;
      startPositions[k * 4 + 3] = Math.random() * Math.PI * 2;
      /* Golden particle color */
      startColors[k * 3] = 1.0;
      startColors[k * 3 + 1] = 0.75 + Math.random() * 0.2;
      startColors[k * 3 + 2] = 0.2 + Math.random() * 0.15;
    }
    const particleGeo = new THREE.BufferGeometry();
    particleGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(startPositions.buffer, 0, count * 3), 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(startColors, 3));
    /* Store flow angles as a separate attribute for shader or JS update */
    particleGeo.setAttribute('flowAngle', new THREE.BufferAttribute(new Float32Array(startPositions.buffer, count * 3 * 4, count), 1));
    const mat = new THREE.PointsMaterial({
      size: 0.08,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });
    cache.particles = { geometry: particleGeo, material: mat, mesh: null };
  }
  /* Create or reuse the Points mesh — geometry shared, positions updated per frame */
  if (!cache.particles.mesh) {
    cache.particles.mesh = new THREE.Points(cache.particles.geometry, cache.particles.material);
  }
  return cache.particles.mesh;
}
/* Per-frame particle update: animate each particle along its flow angle,
   with terrain height sampling. Reuses position array — zero allocation. */
function updateParticles(terrainData, timeIndex, dt) {
  if (!cache.particles || !cache.particles.mesh) return;
  const posAttr = cache.particles.geometry.attributes.position;
  const flowAttr = cache.particles.geometry.attributes.flowAngle;
  const positions = posAttr.array;
  const flows = flowAttr.array;
  const count = posAttr.count;
  const step = TERRAIN_SIZE / (GRID - 1);
  const half = TERRAIN_SIZE / 2;
  const speed = 1.5;
  for (let k = 0; k < count; k++) {
    const i3 = k * 3;
    let x = positions[i3];
    let z = positions[i3 + 2];
    /* Move particle along its flow angle */
    const angle = flows[k];
    x += Math.cos(angle) * speed * dt;
    z += Math.sin(angle) * speed * dt;
    /* Wrap around when leaving terrain bounds */
    if (x < -half) x = half - 0.01;
    if (x > half) x = -half + 0.01;
    if (z < -half) z = half - 0.01;
    if (z > half) z = -half + 0.01;
    /* Sample terrain height at new position — memoized grid transform:
       grid index computed once per particle per frame, not repeated. */
    const gj = Math.floor((x + half) / step);
    const gi = Math.floor((z + half) / step);
    const ci = Math.min(GRID - 1, Math.max(0, gi));
    const cj = Math.min(GRID - 1, Math.max(0, gj));
    const y = terrainData.heightData[ci * GRID + cj] + 0.25;
    positions[i3] = x;
    positions[i3 + 1] = y;
    positions[i3 + 2] = z;
    /* Slight random walk in flow angle for organic movement */
    flows[k] += (Math.random() - 0.5) * 0.3;
  }
  posAttr.needsUpdate = true;
  flowAttr.needsUpdate = true;
}
/* Scene objects held by reference for swapping on time change */
let terrainMesh = null;
let riverMesh = null;
let currentTimeIndex = 0;
let currentTerrainData = null;
/* Initialize Three.js */
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a1a);
scene.fog = new THREE.Fog(0x0a0a1a, 25, 60);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 80);
camera.position.set(14, 10, 16);
camera.lookAt(0, 2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
/* Lighting */
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 2.5);
sunLight.position.set(15, 20, 10);
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x446688, 0.8);
fillLight.position.set(-10, 5, -8);
scene.add(fillLight);
/* Grid helper on the ground plane */
const gridHelper = new THREE.GridHelper(TERRAIN_SIZE, 20, 0x1a2a3a, 0x0f1a28);
gridHelper.position.y = -0.02;
scene.add(gridHelper);
/* OrbitControls with smooth damping */
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(0, 2.5, 0);
controls.minDistance = 4;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.5;
controls.update();
/* Build initial scene */
function loadTimeStep(timeIndex) {
  /* Dispose old terrain geometry if not from cache */
  if (terrainMesh) {
    if (!cache.terrain.has(currentTimeIndex)) {
      terrainMesh.geometry.dispose();
    }
    scene.remove(terrainMesh);
  }
  if (riverMesh) {
    if (!cache.rivers.has(currentTimeIndex)) {
      riverMesh.geometry.dispose();
    }
    scene.remove(riverMesh);
  }
  const { geometry, heightData } = buildTerrainGeometry(timeIndex);
  const terrainMat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.7,
    metalness: 0.15,
    flatShading: false,
  });
  terrainMesh = new THREE.Mesh(geometry, terrainMat);
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  /* Rivers: instantiate once per time step (cached geometry) */
  const riverGeo = buildRiverGeometry(timeIndex);
  if (riverGeo && riverGeo.attributes.position) {
    const riverMat = new THREE.MeshStandardMaterial({
      color: 0xcc3333,
      roughness: 0.5,
      metalness: 0.3,
      emissive: 0x330000,
      emissiveIntensity: 0.6,
    });
    riverMesh = new THREE.Mesh(riverGeo, riverMat);
    riverMesh.renderOrder = 1;
    riverMesh.material.depthTest = true;
    riverMesh.material.depthWrite = true;
    scene.add(riverMesh);
  }
  /* Particle system: build once, positions updated per frame */
  const particleMesh = buildParticleSystem(timeIndex);
  if (!scene.children.includes(particleMesh)) {
    scene.add(particleMesh);
  }
  currentTerrainData = { heightData };
  currentTimeIndex = timeIndex;
  document.getElementById('time-display').textContent = 'T+' + timeIndex + 'h';
}
/* Animation loop: update particles, render, handle controls damping */
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1); /* cap delta to avoid spiral on tab-switch */
  controls.update();
  if (currentTerrainData) {
    updateParticles(currentTerrainData, currentTimeIndex, dt);
  }
  renderer.render(scene, camera);
}
/* Time slider — debounced river rebuild (200ms delay) */
let debounceTimer = null;
const timeSlider = document.getElementById('time-slider');
timeSlider.addEventListener('input', () => {
  const ti = parseInt(timeSlider.value);
  document.getElementById('time-display').textContent = 'T+' + ti + 'h';
  /* Immediate terrain swap — geometry already cached */
  if (terrainMesh) {
    if (!cache.terrain.has(currentTimeIndex)) terrainMesh.geometry.dispose();
    scene.remove(terrainMesh);
  }
  const { geometry, heightData } = buildTerrainGeometry(ti);
  terrainMesh = new THREE.Mesh(geometry, new THREE.MeshStandardMaterial({
    vertexColors: true, roughness: 0.7, metalness: 0.15,
  }));
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  currentTerrainData = { heightData };
  currentTimeIndex = ti;
  /* Debounce river rebuild: 200ms delay avoids per-tick TubeGeometry construction */
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    if (riverMesh) {
      if (!cache.rivers.has(currentTimeIndex - 1)) riverMesh.geometry.dispose();
      scene.remove(riverMesh);
    }
    const rGeo = buildRiverGeometry(ti);
    if (rGeo && rGeo.attributes.position) {
      riverMesh = new THREE.Mesh(rGeo, new THREE.MeshStandardMaterial({
        color: 0xcc3333, roughness: 0.5, metalness: 0.3, emissive: 0x330000, emissiveIntensity: 0.6,
      }));
      riverMesh.renderOrder = 1;
      scene.add(riverMesh);
    }
    debounceTimer = null;
  }, 200);
});
/* Camera bookmarks */
const bookmarks = [];
window.saveBookmark = function() {
  const bm = {
    position: camera.position.clone(),
    target: controls.target.clone(),
  };
  bookmarks.push(bm);
  /* Render bookmark button */
  const bar = document.getElementById('bookmark-bar');
  const btn = document.createElement('button');
  btn.className = 'btn';
  btn.textContent = 'View ' + bookmarks.length;
  btn.onclick = () => {
    camera.position.copy(bm.position);
    controls.target.copy(bm.target);
    controls.update();
  };
  bar.appendChild(btn);
};
/* Preset views */
window.goToView = function(view) {
  switch (view) {
    case 'top':
      camera.position.set(0, 18, 0.5);
      controls.target.set(0, 2, 0);
      break;
    case 'front':
      camera.position.set(0, 3, 18);
      controls.target.set(0, 2, 0);
      break;
    case 'default':
      camera.position.set(14, 10, 16);
      controls.target.set(0, 2.5, 0);
      break;
  }
  controls.update();
};
/* Auto-rotate toggle */
let autoRotate = false;
window.toggleAutoRotate = function() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  controls.autoRotateSpeed = 0.6;
  document.getElementById('btn-auto-rotate').classList.toggle('active', autoRotate);
};
/* Resize handler */
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
/* Keyboard shortcuts: 1-9 to jump to time indices */
window.addEventListener('keydown', (e) => {
  const key = parseInt(e.key);
  if (key >= 0 && key <= 9) {
    const ti = Math.floor((key / 9) * (TIME_STEPS - 1));
    timeSlider.value = ti;
    timeSlider.dispatchEvent(new Event('input'));
  }
});
/* Initialize and start */
loadTimeStep(0);
animate();
</script>
</body>
</html>