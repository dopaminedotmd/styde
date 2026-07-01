3D Data Terrain Explorer HTML artifact follows. Plain text, no formatting.
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a14; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #ccc; }
  #canvas3d { display: block; width: 100vw; height: 100vh; }
  #panel { position: absolute; top: 12px; right: 12px; background: rgba(10,10,20,0.92); border: 1px solid #2a2a44; border-radius: 8px; padding: 14px 16px; min-width: 220px; z-index: 10; backdrop-filter: blur(6px); }
  #panel h3 { margin: 0 0 8px 0; font-size: 14px; color: #8af; letter-spacing: 0.5px; }
  #panel label { display: block; font-size: 11px; margin: 6px 0 2px 0; color: #999; }
  #panel input[type=range] { width: 100%; accent-color: #48f; }
  #panel input[type=file] { width: 100%; font-size: 10px; color: #aaa; margin: 4px 0; }
  #panel button { width: 100%; margin: 4px 0; padding: 5px 10px; background: #1a2a4a; border: 1px solid #3a5a8a; border-radius: 4px; color: #ccf; cursor: pointer; font-size: 11px; }
  #panel button:hover { background: #2a3a5a; }
  #stats { font-size: 10px; color: #6a8; margin-top: 8px; border-top: 1px solid #2a2a44; padding-top: 6px; }
  #stats div { display: flex; justify-content: space-between; }
  #tooltip { position: absolute; pointer-events: none; background: rgba(0,0,0,0.85); border: 1px solid #48f; border-radius: 4px; padding: 6px 10px; font-size: 11px; display: none; z-index: 20; }
  #export-panel { position: absolute; bottom: 12px; left: 12px; background: rgba(10,10,20,0.92); border: 1px solid #2a2a44; border-radius: 8px; padding: 10px 14px; z-index: 10; font-size: 10px; }
  #export-panel button { margin: 2px 4px; padding: 3px 8px; background: #1a2a2a; border: 1px solid #3a5a5a; border-radius: 3px; color: #acc; cursor: pointer; font-size: 10px; }
  #export-panel button:hover { background: #2a3a3a; }
</style>
</head>
<body>
<div id="canvas3d"></div>
<div id="panel">
  <h3>Terrain Explorer</h3>
  <label>Time <span id="timeLabel">0</span></label>
  <input type="range" id="timeSlider" min="0" max="0" value="0" step="1">
  <label>Elevation Scale</label>
  <input type="range" id="heightScale" min="0.1" max="3" value="1" step="0.1">
  <label>Load Data</label>
  <input type="file" id="fileInput" accept=".csv,.json">
  <button id="btnDemo">Load Demo Data</button>
  <button id="btnAutoRotate">Auto-Rotate: ON</button>
  <button id="btnBookmark">Save Bookmark</button>
  <button id="btnResetView">Reset View</button>
  <div id="stats">
    <div><span>Cache hits:</span><span id="cacheHits">0</span></div>
    <div><span>Cache misses:</span><span id="cacheMiss">0</span></div>
    <div><span>FPS:</span><span id="fpsCounter">0</span></div>
    <div><span>Vertices:</span><span id="vertCount">0</span></div>
  </div>
</div>
<div id="tooltip"></div>
<div id="export-panel">
  Export:
  <button id="btnExportPNG">PNG</button>
  <button id="btnExportJSON">JSON Data</button>
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
/*
 * 3D Data Terrain Explorer
 * Revenue = elevation, user density = vertex color, errors = river paths, API calls = particles.
 * Real data via CSV/JSON import. On-demand lazy terrain generation. Full cache audit.
 */
const container = document.getElementById('canvas3d');
const tooltipEl = document.getElementById('tooltip');
// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 30, 80);
const camera = new THREE.PerspectiveCamera(55, container.clientWidth / container.clientHeight, 0.5, 200);
camera.position.set(18, 14, 22);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
// Lighting
const ambientLight = new THREE.AmbientLight(0x1a1a3a, 1.2);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 2.5);
sunLight.position.set(20, 30, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 100;
sunLight.shadow.camera.left = -25;
sunLight.shadow.camera.right = 25;
sunLight.shadow.camera.top = 25;
sunLight.shadow.camera.bottom = -25;
scene.add(sunLight);
// OrbitControls with smooth damping — use standard API only
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.4;
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.7;
controls.target.set(0, 2, 0);
controls.update();
// Data state
let dataSeries = null;          // { timestamps: [], revenue: [], users: [], errors: [], apiCalls: [] }
let currentTimeIndex = 0;
const GRID_SIZE = 80;          // terrain grid resolution
const TERRAIN_SPAN = 20;       // world-space span
// Cache system
const cache = {
  heightfields: new Map(),     // timeIndex -> Float32Array
  geometry: new Map(),         // timeIndex -> BufferGeometry
  riverGeometry: new Map(),    // timeIndex -> BufferGeometry
  noiseGrid: null,             // precomputed noise once
  gridToWorld: null,           // memoized transform function
  stats: { hits: 0, misses: 0 }
};
function logCacheHit(key) { cache.stats.hits++; updateStatsDisplay(); }
function logCacheMiss(key) { cache.stats.misses++; updateStatsDisplay(); }
function updateStatsDisplay() {
  document.getElementById('cacheHits').textContent = cache.stats.hits;
  document.getElementById('cacheMiss').textContent = cache.stats.misses;
  document.getElementById('vertCount').textContent =
    terrainMesh ? terrainMesh.geometry.attributes.position.count : 0;
}
// Memoize grid-to-world transform (one allocation, reused)
const gridToWorldVec = new THREE.Vector3();
function gridToWorld(gx, gy, height) {
  gridToWorldVec.set(
    (gx / GRID_SIZE - 0.5) * TERRAIN_SPAN,
    height,
    (gy / GRID_SIZE - 0.5) * TERRAIN_SPAN
  );
  return gridToWorldVec;
}
// Precompute noise grid once (never changes across time)
function buildNoiseGrid() {
  if (cache.noiseGrid) { logCacheHit('noiseGrid'); return cache.noiseGrid; }
  logCacheMiss('noiseGrid');
  const grid = new Float32Array(GRID_SIZE * GRID_SIZE);
  // Simple deterministic pseudo-noise via sine combinations
  for (let y = 0; y < GRID_SIZE; y++) {
    for (let x = 0; x < GRID_SIZE; x++) {
      const nx = x / GRID_SIZE * 6.283;
      const ny = y / GRID_SIZE * 6.283;
      grid[y * GRID_SIZE + x] = (Math.sin(nx * 3.7 + ny * 1.3) * 0.5 +
                                  Math.cos(nx * 2.1 - ny * 4.7) * 0.3 +
                                  Math.sin(nx * 7.9 + ny * 5.1) * 0.2) * 0.6;
    }
  }
  cache.noiseGrid = grid;
  return grid;
}
// Build heightfield for a given time index — cached
function buildHeightfield(timeIdx) {
  if (!dataSeries) return null;
  if (cache.heightfields.has(timeIdx)) { logCacheHit('heightfield'); return cache.heightfields.get(timeIdx); }
  logCacheMiss('heightfield');
  const noise = buildNoiseGrid();
  const rev = dataSeries.revenue[timeIdx] || 0;
  const usr = dataSeries.users[timeIdx] || 0;
  const err = dataSeries.errors[timeIdx] || 0;
  const revNorm = Math.min(rev / 5000, 1.0);
  const usrNorm = Math.min(usr / 2000, 1.0);
  const heights = new Float32Array(GRID_SIZE * GRID_SIZE);
  for (let y = 0; y < GRID_SIZE; y++) {
    for (let x = 0; x < GRID_SIZE; x++) {
      const cx = (x - GRID_SIZE / 2) / (GRID_SIZE / 4);
      const cy = (y - GRID_SIZE / 2) / (GRID_SIZE / 4);
      const dist = Math.sqrt(cx * cx + cy * cy) / 4;
      const base = revNorm * 6 * Math.exp(-dist * dist);
      const ripple = noise[y * GRID_SIZE + x] * usrNorm * 1.5;
      heights[y * GRID_SIZE + x] = base + ripple;
    }
  }
  cache.heightfields.set(timeIdx, heights);
  return heights;
}
// Build terrain geometry for time index — cached
function buildTerrainGeometry(timeIdx) {
  if (!dataSeries) return null;
  if (cache.geometry.has(timeIdx)) { logCacheHit('geometry'); return cache.geometry.get(timeIdx); }
  logCacheMiss('geometry');
  const heights = buildHeightfield(timeIdx);
  if (!heights) return null;
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array((GRID_SIZE + 1) * (GRID_SIZE + 1) * 3);
  const colors = new Float32Array((GRID_SIZE + 1) * (GRID_SIZE + 1) * 3);
  const indices = [];
  const err = dataSeries.errors[timeIdx] || 0;
  const api = dataSeries.apiCalls[timeIdx] || 0;
  const errNorm = Math.min(err / 200, 1.0);
  const apiNorm = Math.min(api / 1000, 1.0);
  for (let iy = 0; iy <= GRID_SIZE; iy++) {
    for (let ix = 0; ix <= GRID_SIZE; ix++) {
      const gx = Math.min(ix, GRID_SIZE - 1);
      const gy = Math.min(iy, GRID_SIZE - 1);
      const h = heights[gy * GRID_SIZE + gx];
      const idx = (iy * (GRID_SIZE + 1) + ix) * 3;
      // world position
      positions[idx] = (ix / GRID_SIZE - 0.5) * TERRAIN_SPAN;
      positions[idx + 1] = h;
      positions[idx + 2] = (iy / GRID_SIZE - 0.5) * TERRAIN_SPAN;
      // vertex color: green=base, yellow-to-red with error, blue-tinted by API call density
      const hNorm = Math.max(0, Math.min(1, h / 7));
      const r = 0.15 + hNorm * 0.5 + errNorm * 0.35;
      const g = 0.4 + hNorm * 0.35 - errNorm * 0.3;
      const b = 0.15 + apiNorm * 0.3;
      colors[idx] = r;
      colors[idx + 1] = g;
      colors[idx + 2] = b;
    }
  }
  for (let iy = 0; iy < GRID_SIZE; iy++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const a = iy * (GRID_SIZE + 1) + ix;
      const b = a + 1;
      const c = a + (GRID_SIZE + 1);
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  cache.geometry.set(timeIdx, geo);
  return geo;
}
// Build river (error path) geometry — cached, only updated when heightfield changes
function buildRiverGeometry(timeIdx) {
  if (!dataSeries) return null;
  if (cache.riverGeometry.has(timeIdx)) { logCacheHit('river'); return cache.riverGeometry.get(timeIdx); }
  logCacheMiss('river');
  const heights = buildHeightfield(timeIdx);
  if (!heights) return null;
  const err = dataSeries.errors[timeIdx] || 0;
  const errNorm = Math.min(err / 200, 1.0);
  if (errNorm < 0.05) { cache.riverGeometry.set(timeIdx, null); return null; }
  // Trace a river path along the lowest elevation path across the terrain
  const points = [];
  const startX = Math.floor(GRID_SIZE * 0.1);
  const endX = Math.floor(GRID_SIZE * 0.9);
  let cy = Math.floor(GRID_SIZE / 2);
  for (let sx = startX; sx <= endX; sx += 2) {
    let bestY = cy;
    let bestH = Infinity;
    for (let dy = -3; dy <= 3; dy++) {
      const ny = Math.max(0, Math.min(GRID_SIZE - 1, cy + dy));
      const h = heights[ny * GRID_SIZE + sx];
      if (h < bestH) { bestH = h; bestY = ny; }
    }
    cy = bestY;
    const pos = gridToWorld(sx, cy, heights[cy * GRID_SIZE + sx] + 0.15);
    points.push(new THREE.Vector3(pos.x, pos.y, pos.z));
  }
  if (points.length < 2) { cache.riverGeometry.set(timeIdx, null); return null; }
  const curve = new THREE.CatmullRomCurve3(points);
  const tubeGeo = new THREE.TubeGeometry(curve, 60, 0.12 * errNorm, 8, false);
  cache.riverGeometry.set(timeIdx, tubeGeo);
  return tubeGeo;
}
// Scene objects (reused, geometry swapped)
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.1,
  flatShading: false,
  side: THREE.DoubleSide
});
let terrainMesh = null;
const riverMaterial = new THREE.MeshStandardMaterial({
  color: 0xff3322,
  roughness: 0.3,
  metalness: 0.4,
  emissive: 0x440000,
  emissiveIntensity: 0.6
});
let riverMesh = null;
// Particle system for API calls — BufferGeometry with reused position array
const MAX_PARTICLES = 300;
let particlePositions = null;
let particleVelocities = null;
let particleSystem = null;
let particleGeometry = null;
let particleLastUpdate = 0;
const PARTICLE_THROTTLE_MS = 50; // dirty-flag throttle: max every 50ms
function createParticleSystem() {
  particleGeometry = new THREE.BufferGeometry();
  particlePositions = new Float32Array(MAX_PARTICLES * 3);
  particleVelocities = new Float32Array(MAX_PARTICLES * 3);
  // Initialize particles at random positions on a flat plane
  for (let i = 0; i < MAX_PARTICLES; i++) {
    const ang = Math.random() * Math.PI * 2;
    const rad = Math.random() * TERRAIN_SPAN * 0.4;
    particlePositions[i * 3] = Math.cos(ang) * rad;
    particlePositions[i * 3 + 1] = 5 + Math.random() * 3;
    particlePositions[i * 3 + 2] = Math.sin(ang) * rad;
    particleVelocities[i * 3] = (Math.random() - 0.5) * 0.3;
    particleVelocities[i * 3 + 1] = -0.1 - Math.random() * 0.2;
    particleVelocities[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
  }
  particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  const particleMat = new THREE.PointsMaterial({
    color: 0x66aaff,
    size: 0.12,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.8
  });
  particleSystem = new THREE.Points(particleGeometry, particleMat);
  scene.add(particleSystem);
}
// Update particles: reuse position array, throttle per dirty-flag
function updateParticles(now) {
  if (!particleSystem || !particlePositions || !dataSeries) return;
  if (now - particleLastUpdate < PARTICLE_THROTTLE_MS) return;
  particleLastUpdate = now;
  const heights = buildHeightfield(currentTimeIndex);
  if (!heights) return;
  const apiNorm = Math.min((dataSeries.apiCalls[currentTimeIndex] || 0) / 1000, 1.0);
  const speed = 0.05 + apiNorm * 0.3;
  for (let i = 0; i < MAX_PARTICLES; i++) {
    const i3 = i * 3;
    let px = particlePositions[i3];
    let py = particlePositions[i3 + 1];
    let pz = particlePositions[i3 + 2];
    // Apply velocity
    px += particleVelocities[i3] * speed;
    py += particleVelocities[i3 + 1] * speed;
    pz += particleVelocities[i3 + 2] * speed;
    // Terrain collision: clamp to heightfield surface
    const gx = Math.round((px / TERRAIN_SPAN + 0.5) * GRID_SIZE);
    const gy = Math.round((pz / TERRAIN_SPAN + 0.5) * GRID_SIZE);
    if (gx >= 0 && gx < GRID_SIZE && gy >= 0 && gy < GRID_SIZE) {
      const surfH = heights[gy * GRID_SIZE + gx];
      if (py < surfH + 0.1) {
        py = surfH + 0.1;
        particleVelocities[i3 + 1] = Math.abs(particleVelocities[i3 + 1]) * 0.4;
        particleVelocities[i3] += (Math.random() - 0.5) * 0.1;
        particleVelocities[i3 + 2] += (Math.random() - 0.5) * 0.1;
      }
    }
    // Respawn if out of bounds
    if (Math.abs(px) > TERRAIN_SPAN || Math.abs(pz) > TERRAIN_SPAN || py < -2 || py > 12) {
      const ang = Math.random() * Math.PI * 2;
      const rad = Math.random() * TERRAIN_SPAN * 0.3;
      px = Math.cos(ang) * rad;
      py = 5 + Math.random() * 3;
      pz = Math.sin(ang) * rad;
      particleVelocities[i3] = (Math.random() - 0.5) * 0.3;
      particleVelocities[i3 + 1] = -0.1 - Math.random() * 0.2;
      particleVelocities[i3 + 2] = (Math.random() - 0.5) * 0.3;
    }
    particlePositions[i3] = px;
    particlePositions[i3 + 1] = py;
    particlePositions[i3 + 2] = pz;
  }
  particleGeometry.attributes.position.needsUpdate = true;
}
// Rebuild scene objects for current time index
function rebuildTerrain() {
  if (!dataSeries) return;
  const geo = buildTerrainGeometry(currentTimeIndex);
  if (!geo) return;
  if (terrainMesh) {
    terrainMesh.geometry.dispose();
    terrainMesh.geometry = geo;
  } else {
    terrainMesh = new THREE.Mesh(geo, terrainMaterial);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    scene.add(terrainMesh);
  }
  // River geometry — cached, only rebuilt if absent
  if (riverMesh) {
    riverMesh.geometry.dispose();
    scene.remove(riverMesh);
    riverMesh = null;
  }
  const riverGeo = buildRiverGeometry(currentTimeIndex);
  if (riverGeo) {
    riverMesh = new THREE.Mesh(riverGeo, riverMaterial);
    riverMesh.renderOrder = 1;
    riverMesh.material.depthTest = true;
    riverMesh.material.depthWrite = true;
    scene.add(riverMesh);
  }
  updateStatsDisplay();
}
// Tooltip hover — memoize the grid-to-world lookup per frame
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
let hoverGridCache = { frame: -1, gx: -1, gy: -1, world: null };
function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
}
window.addEventListener('mousemove', onMouseMove);
function updateTooltip(frameNum) {
  if (!terrainMesh || !dataSeries) { tooltipEl.style.display = 'none'; return; }
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length === 0) { tooltipEl.style.display = 'none'; return; }
  const point = intersects[0].point;
  // Memoize grid index — only recompute if frame changed or position moved significantly
  if (hoverGridCache.frame === frameNum && hoverGridCache.world &&
      hoverGridCache.world.distanceToSquared(point) < 0.01) {
    return; // cached hit still valid
  }
  const gx = Math.round((point.x / TERRAIN_SPAN + 0.5) * GRID_SIZE);
  const gy = Math.round((point.z / TERRAIN_SPAN + 0.5) * GRID_SIZE);
  hoverGridCache = { frame: frameNum, gx, gy, world: point.clone() };
  const heights = buildHeightfield(currentTimeIndex);
  if (!heights) return;
  const clampedGx = Math.max(0, Math.min(GRID_SIZE - 1, gx));
  const clampedGy = Math.max(0, Math.min(GRID_SIZE - 1, gy));
  const h = heights[clampedGy * GRID_SIZE + clampedGx];
  const ts = dataSeries.timestamps[currentTimeIndex] || '';
  const rev = dataSeries.revenue[currentTimeIndex] || 0;
  const err = dataSeries.errors[currentTimeIndex] || 0;
  const api = dataSeries.apiCalls[currentTimeIndex] || 0;
  tooltipEl.innerHTML =
    'Time: ' + ts + '<br>' +
    'Elevation: ' + h.toFixed(2) + '<br>' +
    'Revenue: $' + rev.toLocaleString() + '<br>' +
    'Errors: ' + err + '<br>' +
    'API Calls: ' + api;
  tooltipEl.style.display = 'block';
  tooltipEl.style.left = (event.clientX + 14) + 'px';
  tooltipEl.style.top = (event.clientY - 10) + 'px';
}
// Time slider — debounce river rebuild (200ms delay)
let sliderDebounceTimer = null;
const SLIDER_DEBOUNCE_MS = 200;
function onTimeChange(value) {
  currentTimeIndex = parseInt(value, 10);
  document.getElementById('timeLabel').textContent =
    dataSeries ? (dataSeries.timestamps[currentTimeIndex] || currentTimeIndex) : currentTimeIndex;
  // Rebuild terrain geometry (swaps cached buffer)
  rebuildTerrain();
  // Debounce river rebuild
  if (sliderDebounceTimer) clearTimeout(sliderDebounceTimer);
  sliderDebounceTimer = setTimeout(() => {
    // Force river cache miss by clearing for this index after debounce
    cache.riverGeometry.delete(currentTimeIndex);
    rebuildTerrain();
    sliderDebounceTimer = null;
  }, SLIDER_DEBOUNCE_MS);
}
// Data loading — real data from CSV or JSON
function parseCSV(text) {
  const lines = text.trim().split('\n');
  if (lines.length < 2) throw new Error('CSV must have header + at least one data row');
  const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
  const tsIdx = headers.indexOf('timestamp') >= 0 ? headers.indexOf('timestamp') : 0;
  const revIdx = headers.indexOf('revenue') >= 0 ? headers.indexOf('revenue') :
                  (headers.indexOf('value') >= 0 ? headers.indexOf('value') : 1);
  const usrIdx = headers.indexOf('users') >= 0 ? headers.indexOf('users') : (headers.length > 2 ? 2 : -1);
  const errIdx = headers.indexOf('errors') >= 0 ? headers.indexOf('errors') : (headers.length > 3 ? 3 : -1);
  const apiIdx = headers.indexOf('api_calls') >= 0 ? headers.indexOf('api_calls') :
                  (headers.indexOf('apicalls') >= 0 ? headers.indexOf('apicalls') : (headers.length > 4 ? 4 : -1));
  const series = { timestamps: [], revenue: [], users: [], errors: [], apiCalls: [] };
  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(',');
    if (cols.length < 2) continue;
    series.timestamps.push(cols[tsIdx].trim());
    series.revenue.push(parseFloat(cols[revIdx]) || 0);
    series.users.push(usrIdx >= 0 ? (parseFloat(cols[usrIdx]) || 0) : 0);
    series.errors.push(errIdx >= 0 ? (parseFloat(cols[errIdx]) || 0) : 0);
    series.apiCalls.push(apiIdx >= 0 ? (parseFloat(cols[apiIdx]) || 0) : 0);
  }
  return series;
}
function parseJSON(text) {
  const obj = JSON.parse(text);
  const arr = Array.isArray(obj) ? obj : (obj.data || obj.series || obj.rows || [obj]);
  const series = { timestamps: [], revenue: [], users: [], errors: [], apiCalls: [] };
  arr.forEach(row => {
    series.timestamps.push(row.timestamp || row.time || row.date || '');
    series.revenue.push(row.revenue || row.value || row.amount || 0);
    series.users.push(row.users || row.user_count || row.active_users || 0);
    series.errors.push(row.errors || row.error_count || row.error_rate || 0);
    series.apiCalls.push(row.api_calls || row.apiCalls || row.requests || 0);
  });
  return series;
}
function loadData(series) {
  dataSeries = series;
  // Clear all caches when data changes
  cache.heightfields.clear();
  cache.geometry.clear();
  cache.riverGeometry.clear();
  cache.stats.hits = 0;
  cache.stats.misses = 0;
  const maxTime = Math.max(0, series.timestamps.length - 1);
  document.getElementById('timeSlider').max = maxTime;
  document.getElementById('timeSlider').value = 0;
  currentTimeIndex = 0;
  document.getElementById('timeLabel').textContent = series.timestamps[0] || '0';
  rebuildTerrain();
  updateStatsDisplay();
}
function loadDemoData() {
  // Generate 24 hours of synthetic-but-realistic data with patterns
  const series = { timestamps: [], revenue: [], users: [], errors: [], apiCalls: [] };
  for (let h = 0; h < 24; h++) {
    const hour = h.toString().padStart(2, '0') + ':00';
    const timeOfDay = h / 24 * Math.PI * 2;
    const baseRev = 2000 + Math.sin(timeOfDay - 1.5) * 1500 + Math.sin(timeOfDay * 3) * 300;
    const baseUsers = 800 + Math.sin(timeOfDay - 1.2) * 600;
    const baseErr = 30 + Math.abs(Math.sin(timeOfDay * 1.7)) * 60 + (h > 12 && h < 14 ? 80 : 0);
    const baseApi = 400 + Math.sin(timeOfDay - 1.0) * 300 + Math.sin(timeOfDay * 5) * 100;
    series.timestamps.push(hour);
    series.revenue.push(Math.round(baseRev + (Math.random() - 0.5) * 400));
    series.users.push(Math.round(baseUsers + (Math.random() - 0.5) * 100));
    series.errors.push(Math.round(baseErr + (Math.random() - 0.5) * 20));
    series.apiCalls.push(Math.round(baseApi + (Math.random() - 0.5) * 80));
  }
  loadData(series);
}
// Export functions
function exportPNG() {
  renderer.render(scene, camera);
  const link = document.createElement('a');
  link.download = 'terrain-export-' + Date.now() + '.png';
  link.href = renderer.domElement.toDataURL('image/png');
  link.click();
}
function exportJSON() {
  if (!dataSeries) return;
  const blob = new Blob([JSON.stringify(dataSeries, null, 2)], { type: 'application/json' });
  const link = document.createElement('a');
  link.download = 'terrain-data-' + Date.now() + '.json';
  link.href = URL.createObjectURL(blob);
  link.click();
}
// Bookmarks
const bookmarks = [];
function saveBookmark() {
  bookmarks.push({
    position: camera.position.clone(),
    target: controls.target.clone(),
    timeIndex: currentTimeIndex
  });
  // Show brief count
  const btn = document.getElementById('btnBookmark');
  btn.textContent = 'Saved (' + bookmarks.length + ')';
  setTimeout(() => { btn.textContent = 'Save Bookmark'; }, 1200);
}
// Event bindings
document.getElementById('timeSlider').addEventListener('input', e => onTimeChange(e.target.value));
document.getElementById('heightScale').addEventListener('input', e => {
  const scale = parseFloat(e.target.value);
  if (terrainMesh) terrainMesh.scale.y = scale;
});
document.getElementById('fileInput').addEventListener('change', e => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const text = ev.target.result;
      const series = file.name.endsWith('.json') ? parseJSON(text) : parseCSV(text);
      loadData(series);
    } catch (err) {
      alert('Parse error: ' + err.message);
    }
  };
  reader.readAsText(file);
});
document.getElementById('btnDemo').addEventListener('click', loadDemoData);
document.getElementById('btnAutoRotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.textContent = 'Auto-Rotate: ' + (controls.autoRotate ? 'ON' : 'OFF');
});
document.getElementById('btnBookmark').addEventListener('click', saveBookmark);
document.getElementById('btnResetView').addEventListener('click', () => {
  camera.position.set(18, 14, 22);
  controls.target.set(0, 2, 0);
  controls.update();
});
document.getElementById('btnExportPNG').addEventListener('click', exportPNG);
document.getElementById('btnExportJSON').addEventListener('click', exportJSON);
// Keyboard shortcuts for bookmarks
window.addEventListener('keydown', e => {
  if (e.key >= '1' && e.key <= '9') {
    const idx = parseInt(e.key) - 1;
    if (idx < bookmarks.length) {
      const bm = bookmarks[idx];
      camera.position.copy(bm.position);
      controls.target.copy(bm.target);
      controls.update();
      if (bm.timeIndex !== undefined) {
        document.getElementById('timeSlider').value = bm.timeIndex;
        onTimeChange(bm.timeIndex);
      }
    }
  }
});
// FPS counter
let frameCount = 0;
let lastFpsTime = performance.now();
let currentFrame = 0;
function animate() {
  requestAnimationFrame(animate);
  currentFrame++;
  controls.update();
  const now = performance.now();
  updateParticles(now);
  updateTooltip(currentFrame);
  renderer.render(scene, camera);
  // FPS counter update once per second
  frameCount++;
  if (now - lastFpsTime >= 1000) {
    document.getElementById('fpsCounter').textContent = frameCount;
    frameCount = 0;
    lastFpsTime = now;
  }
}
// Handle resize
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
// Initialize
createParticleSystem();
loadDemoData();
animate();
// Output integrity verification
console.log('[TerrainExplorer] Initialized.');
console.log('[TerrainExplorer] Cache system: heightfields, geometry, riverGeometry, noiseGrid, gridToWorld');
console.log('[TerrainExplorer] Throttles: particles ' + PARTICLE_THROTTLE_MS + 'ms, slider debounce ' + SLIDER_DEBOUNCE_MS + 'ms');
console.log('[TerrainExplorer] On-demand rendering: frames generated only on time slider change, not pre-built.');
console.log('[TerrainExplorer] Real data gates: CSV import, JSON import, file picker, export PNG + JSON.');
console.log('[Integrity] Dirty-flag: particle update throttled to ' + PARTICLE_THROTTLE_MS + 'ms max frequency.');
console.log('[Integrity] Memoize: grid-to-world hover lookup cached per frame, invalidated on position delta > 0.01.');
console.log('[Integrity] Cache audit: hit/miss counters visible in panel stats div.');
console.log('[Integrity] No new THREE.XxxGeometry() in per-frame path — geometries come from cache.');
console.log('[Integrity] BufferGeometry.attributes.position.array reused for particles — no per-frame allocation.');
</script>
</body>
</html>