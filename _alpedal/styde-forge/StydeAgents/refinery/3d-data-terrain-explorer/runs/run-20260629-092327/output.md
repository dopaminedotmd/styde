<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a0f; --panel-bg: rgba(10,10,20,0.92); --text: #c8ccd4; --accent: #4da6ff; --warn: #ff6b4a; --ok: #3ecf8e; --border: rgba(255,255,255,0.08); }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); overflow: hidden; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; color: var(--text); }
  canvas { display: block; }
  #panel { position: fixed; top: 16px; left: 16px; width: 280px; background: var(--panel-bg); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; backdrop-filter: blur(12px); z-index: 10; user-select: none; }
  #panel h2 { font-size: 14px; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--accent); margin-bottom: 10px; }
  #panel .row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 12px; }
  #panel .label { opacity: 0.7; }
  #panel .val { font-variant-numeric: tabular-nums; font-weight: 500; }
  #time-slider { width: 100%; margin: 8px 0; accent-color: var(--accent); cursor: pointer; }
  #time-label { text-align: center; font-size: 11px; opacity: 0.6; margin-bottom: 4px; }
  #bookmark-bar { display: flex; gap: 4px; flex-wrap: wrap; margin-top: 6px; }
  #bookmark-bar button { font-size: 10px; padding: 3px 8px; border-radius: 4px; border: 1px solid var(--border); background: rgba(255,255,255,0.04); color: var(--text); cursor: pointer; transition: background 0.15s; }
  #bookmark-bar button:hover { background: rgba(255,255,255,0.1); }
  #bookmark-bar button.del { color: var(--warn); border-color: transparent; background: transparent; padding: 3px 4px; }
  #save-bm { font-size: 10px; padding: 4px 10px; margin-top: 4px; border-radius: 4px; border: 1px solid var(--accent); background: rgba(77,166,255,0.1); color: var(--accent); cursor: pointer; width: 100%; }
  #diag { position: fixed; bottom: 16px; right: 16px; background: var(--panel-bg); border: 1px solid var(--border); border-radius: 10px; padding: 10px 14px; backdrop-filter: blur(12px); z-index: 10; font-size: 10px; font-variant-numeric: tabular-nums; min-width: 180px; }
  #diag .title { font-weight: 600; color: var(--accent); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em; }
  #diag .cache-line { display: flex; justify-content: space-between; }
  #diag .cache-hit { color: var(--ok); }
  #diag .cache-miss { color: var(--warn); }
  #legend { position: fixed; bottom: 16px; left: 16px; background: var(--panel-bg); border: 1px solid var(--border); border-radius: 10px; padding: 10px 14px; backdrop-filter: blur(12px); z-index: 10; font-size: 10px; }
  #legend .swatch { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 4px; vertical-align: middle; }
  #status { position: fixed; top: 16px; right: 16px; font-size: 10px; opacity: 0.6; z-index: 10; }
</style>
</head>
<body>
<div id="panel">
  <h2>Data Terrain</h2>
  <div class="row"><span class="label">Time step</span><span class="val" id="time-label">1 / 20</span></div>
  <input type="range" id="time-slider" min="0" max="19" value="0" step="1">
  <div class="row"><span class="label">Metric</span><span class="val" id="metric-name">Revenue</span></div>
  <div class="row"><span class="label">Peak height</span><span class="val" id="peak-val">--</span></div>
  <div class="row"><span class="label">Error hotspots</span><span class="val" id="error-count">--</span></div>
  <div style="font-size:10px;opacity:0.5;margin:4px 0;">Camera bookmarks</div>
  <div id="bookmark-bar"></div>
  <button id="save-bm">+ Save current view</button>
  <div style="font-size:9px;opacity:0.4;margin-top:6px;">Drag orbit · Scroll zoom · Right-drag pan</div>
</div>
<div id="diag">
  <div class="title">Diagnostics</div>
  <div class="cache-line"><span>Terrain cache</span><span><span class="cache-hit" id="tc-hit">0</span>/<span class="cache-miss" id="tc-miss">0</span></span></div>
  <div class="cache-line"><span>River cache</span><span><span class="cache-hit" id="rc-hit">0</span>/<span class="cache-miss" id="rc-miss">0</span></span></div>
  <div class="cache-line"><span>BFS cache</span><span><span class="cache-hit" id="bc-hit">0</span>/<span class="cache-miss" id="bc-miss">0</span></span></div>
  <div class="cache-line"><span>FPS</span><span id="fps-val">--</span></div>
  <div class="cache-line"><span>Particles</span><span id="particle-count">--</span></div>
  <div class="cache-line"><span>Data source</span><span id="ds-source">synthetic</span></div>
</div>
<div id="legend">
  <div><span class="swatch" style="background:#3ecf8e;"></span> High user density</div>
  <div><span class="swatch" style="background:#1a472a;"></span> Low user density</div>
  <div><span class="swatch" style="background:#ff4d4d;"></span> Error river</div>
  <div><span class="swatch" style="background:#ffdd57;"></span> API call trail</div>
</div>
<div id="status">Terrain Explorer v1.0</div>
<script type="importmap">
{
  "imports": {
    "three": "https://unpkg.com/three@0.157.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.157.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ──────────────────────────────────────────────
// Configuration
// ──────────────────────────────────────────────
const GRID = 100;
const GRID_HALF = GRID / 2;
const TERRAIN_SCALE = 12;
const HEIGHT_SCALE = 4.0;
const TIME_STEPS = 20;
const PARTICLE_COUNT = 600;
const RIVER_THRESHOLD = 0.72;
const RIVER_DEBOUNCE_MS = 200;
const SYNTHETIC_DATA_RATIO = 0.5;
// ──────────────────────────────────────────────
// Coordinate validation
// ──────────────────────────────────────────────
const validationLog = [];
function assertFinite(val, label) {
  if (!Number.isFinite(val)) { validationLog.push(`NON-FINITE: ${label}=${val}`); return false; }
  return true;
}
function assertInBounds(idx, min, max, label) {
  if (idx < min || idx > max) { validationLog.push(`OOB: ${label}=${idx} range[${min},${max}]`); return false; }
  return true;
}
function assertValidGrid(i, j) {
  return assertInBounds(i, 0, GRID-1, 'grid_i') & assertInBounds(j, 0, GRID-1, 'grid_j');
}
function drainValidationLog() {
  if (validationLog.length === 0) return;
  const el = document.getElementById('status');
  el.textContent = `VALIDATION: ${validationLog[validationLog.length-1]} (${validationLog.length} total)`;
  el.style.color = '#ff6b4a';
  console.warn('Validation issues:', validationLog);
  validationLog.length = 0;
}
// ──────────────────────────────────────────────
// Data generation — synthetic + real fallback
// ──────────────────────────────────────────────
function generateSyntheticData(t) {
  // t normalised 0..1 across time steps
  const revenue = new Float32Array(GRID * GRID);
  const users = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  const apiCalls = new Float32Array(GRID * GRID);
  // Phase-shifted noise centers that drift over time
  const cx1 = 0.3 + 0.15 * Math.sin(t * Math.PI * 2.3);
  const cy1 = 0.55 + 0.12 * Math.cos(t * Math.PI * 1.7);
  const cx2 = 0.7 + 0.1 * Math.cos(t * Math.PI * 1.9);
  const cy2 = 0.35 + 0.14 * Math.sin(t * Math.PI * 2.1);
  const cx3 = 0.5 + 0.18 * Math.cos(t * Math.PI * 2.5 + 1.2);
  const cy3 = 0.6 + 0.16 * Math.sin(t * Math.PI * 1.3 + 0.8);
  for (let j = 0; j < GRID; j++) {
    const ny = j / (GRID - 1);
    for (let i = 0; i < GRID; i++) {
      const nx = i / (GRID - 1);
      const idx = j * GRID + i;
      // Revenue: multi-peak Gaussian landscape
      const d1 = Math.hypot(nx - cx1, ny - cy1);
      const d2 = Math.hypot(nx - cx2, ny - cy2);
      const d3 = Math.hypot(nx - cx3, ny - cy3);
      let r = Math.exp(-d1 * d1 * 14) * 0.8 + Math.exp(-d2 * d2 * 18) * 0.6 + Math.exp(-d3 * d3 * 12) * 0.45;
      // Add Perlin-like noise via stacked sine
      r += 0.08 * Math.sin(nx * 18 + t * 4) * Math.cos(ny * 15 + t * 3);
      r += 0.05 * Math.sin(nx * 31 - t * 2) * Math.sin(ny * 27 + t * 5);
      revenue[idx] = Math.max(0, Math.min(1, r));
      // User density: offset from revenue centers
      const ud1 = Math.hypot(nx - (cx1 + 0.08), ny - (cy1 - 0.05));
      const ud2 = Math.hypot(nx - (cx2 - 0.06), ny - (cy2 + 0.07));
      let u = Math.exp(-ud1 * ud1 * 10) * 0.7 + Math.exp(-ud2 * ud2 * 14) * 0.5;
      u += 0.06 * Math.sin(nx * 22 + t * 2.8) * Math.cos(ny * 19 + t * 4.1);
      users[idx] = Math.max(0, Math.min(1, u));
      // Error rate: inverse correlation with revenue, plus noise
      let e = (1 - revenue[idx]) * 0.6 + 0.15 * Math.abs(Math.sin(nx * 25 + t * 6) * Math.cos(ny * 20));
      e += 0.1 * ((Math.sin(nx * 40 + ny * 35 + t * 7) + 1) / 2);
      errors[idx] = Math.max(0, Math.min(1, e));
      // API calls: proportional to user density with temporal variation
      apiCalls[idx] = users[idx] * (0.5 + 0.5 * Math.sin(t * Math.PI * 3 + nx * 4 + ny * 3));
    }
  }
  return { revenue, users, errors, apiCalls };
}
// Real-world data attempt — OpenTopography / OpenStreetMap elevation tile fetch
// Falls back to synthetic with realistic noise blending
async function fetchRealElevationData() {
  try {
    // Attempt to fetch a small SRTM tile via OpenTopography public API
    // Bounding box: small region in Colorado Rockies (approx 1 arc-second)
    const url = 'https://portal.opentopography.org/API/globaldem?' +
      'demtype=SRTMGL1&west=-105.32&east=-105.28&south=39.98&north=40.02&outputFormat=JSON';
    const resp = await fetch(url, { signal: AbortSignal.timeout(5000) });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const json = await resp.json();
    if (!json.raster || !json.raster.length) throw new Error('Empty raster');
    // Downsample to our grid
    const srcW = json.raster[0].length;
    const srcH = json.raster.length;
    const elevation = new Float32Array(GRID * GRID);
    let minH = Infinity, maxH = -Infinity;
    for (let j = 0; j < GRID; j++) {
      const sy = Math.floor(j / (GRID - 1) * (srcH - 1));
      for (let i = 0; i < GRID; i++) {
        const sx = Math.floor(i / (GRID - 1) * (srcW - 1));
        const h = json.raster[sy][sx];
        if (h != null) { minH = Math.min(minH, h); maxH = Math.max(maxH, h); }
        elevation[j * GRID + i] = h ?? 0;
      }
    }
    // Normalize
    const range = maxH - minH || 1;
    for (let i = 0; i < elevation.length; i++) {
      if (elevation[i] != null && Number.isFinite(elevation[i])) {
        elevation[i] = (elevation[i] - minH) / range;
      } else {
        elevation[i] = 0;
      }
    }
    return { elevation, source: 'OpenTopography SRTMGL1' };
  } catch (err) {
    console.log('Real elevation fetch failed, using synthetic blend:', err.message);
    return null;
  }
}
function blendRealWithSynthetic(realElevation, syntheticRevenue, t) {
  // Blend real terrain shape into revenue data
  const blended = new Float32Array(GRID * GRID);
  const ratio = 1 - SYNTHETIC_DATA_RATIO; // how much real data to use
  for (let i = 0; i < blended.length; i++) {
    blended[i] = realElevation[i] * ratio + syntheticRevenue[i] * SYNTHETIC_DATA_RATIO;
    assertFinite(blended[i], `blended_revenue[${i}]`);
  }
  return blended;
}
// ──────────────────────────────────────────────
// Cache infrastructure
// ──────────────────────────────────────────────
const cacheStats = { terrain: { hits: 0, misses: 0 }, river: { hits: 0, misses: 0 }, bfs: { hits: 0, misses: 0 } };
// Terrain geometry cache: Map<timeIndex, {geometry, positionArray, colorArray}>
const terrainCache = new Map();
// River geometry cache: key = `${timeIndex}:${hotspotI}:${hotspotJ}`
const riverCache = new Map();
// BFS path cache: Map<timeIndex, Map<sourceKey, pathArray>>
const bfsCache = new Map();
// World-to-grid transform memo: cleared each frame
let gridMemo = null;
function worldToGrid(wx, wz) {
  // Convert world XZ to grid indices (i, j)
  const gi = Math.round(wx / TERRAIN_SCALE * (GRID - 1) + GRID_HALF);
  const gj = Math.round(wz / TERRAIN_SCALE * (GRID - 1) + GRID_HALF);
  return { i: gi, j: gj };
}
function gridToWorld(i, j, height) {
  const wx = (i - GRID_HALF) / (GRID - 1) * TERRAIN_SCALE;
  const wz = (j - GRID_HALF) / (GRID - 1) * TERRAIN_SCALE;
  return { x: wx, y: height * HEIGHT_SCALE, z: wz };
}
function updateDiagnostics() {
  document.getElementById('tc-hit').textContent = cacheStats.terrain.hits;
  document.getElementById('tc-miss').textContent = cacheStats.terrain.misses;
  document.getElementById('rc-hit').textContent = cacheStats.river.hits;
  document.getElementById('rc-miss').textContent = cacheStats.river.misses;
  document.getElementById('bc-hit').textContent = cacheStats.bfs.hits;
  document.getElementById('bc-miss').textContent = cacheStats.bfs.misses;
  document.getElementById('particle-count').textContent = PARTICLE_COUNT;
}
// ──────────────────────────────────────────────
// Terrain geometry builder (cached per time step)
// ──────────────────────────────────────────────
function buildTerrainGeometry(revenueData, usersData) {
  // Uses PlaneGeometry as base, then overwrites position and adds color attribute
  const geo = new THREE.PlaneGeometry(TERRAIN_SCALE, TERRAIN_SCALE, GRID - 1, GRID - 1);
  geo.rotateX(-Math.PI / 2); // lay flat on XZ plane
  const pos = geo.attributes.position;
  const posArr = pos.array; // Float32Array, length = vertexCount * 3
  // Create color attribute
  const colorsArr = new Float32Array(posArr.length);
  geo.setAttribute('color', new THREE.BufferAttribute(colorsArr, 3));
  for (let i = 0; i < posArr.length; i += 3) {
    // Map vertex index to grid position
    const vIdx = i / 3;
    const col = vIdx % GRID;
    const row = Math.floor(vIdx / GRID);
    const gridIdx = row * GRID + col;
    const h = revenueData[gridIdx];
    assertFinite(h, `revenue[${gridIdx}]`);
    posArr[i + 1] = h * HEIGHT_SCALE;
    // Color: user density → green gradient (dark green to bright green)
    const u = usersData[gridIdx];
    const g = 0.15 + u * 0.75;
    const r = 0.05 + u * 0.15;
    const b = 0.08 + u * 0.2;
    colorsArr[i] = r;
    colorsArr[i + 1] = g;
    colorsArr[i + 2] = b;
  }
  geo.computeVertexNormals();
  return geo;
}
function getTerrainGeometry(timeIndex, data) {
  if (terrainCache.has(timeIndex)) {
    cacheStats.terrain.hits++;
    return terrainCache.get(timeIndex);
  }
  cacheStats.terrain.misses++;
  const geo = buildTerrainGeometry(data.revenue, data.users);
  terrainCache.set(timeIndex, geo);
  return geo;
}
// ──────────────────────────────────────────────
// River BFS (cached until terrain rebuild)
// ──────────────────────────────────────────────
function findErrorHotspots(errors) {
  const hotspots = [];
  for (let j = 0; j < GRID; j++) {
    for (let i = 0; i < GRID; i++) {
      const e = errors[j * GRID + i];
      if (e > RIVER_THRESHOLD) {
        // Check local maximum (8-neighbor)
        let isLocalMax = true;
        for (let dj = -1; dj <= 1 && isLocalMax; dj++) {
          for (let di = -1; di <= 1; di++) {
            if (di === 0 && dj === 0) continue;
            const ni = i + di, nj = j + dj;
            if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
            if (errors[nj * GRID + ni] > e) { isLocalMax = false; break; }
          }
        }
        if (isLocalMax) hotspots.push({ i, j, error: e });
      }
    }
  }
  // Sort by error, take top 5
  hotspots.sort((a, b) => b.error - a.error);
  return hotspots.slice(0, 5);
}
function bfsDownhillPath(startI, startJ, revenueData) {
  // BFS that always flows to lowest neighbor (greedy downhill)
  // Cache key uses terrain hash — if terrain unchanged, path is deterministic
  const path = [];
  let ci = startI, cj = startJ;
  const visited = new Set();
  const maxSteps = GRID * 2; // safety limit
  for (let step = 0; step < maxSteps; step++) {
    const key = `${ci},${cj}`;
    if (visited.has(key)) break; // loop detected
    visited.add(key);
    path.push({ i: ci, j: cj });
    // Find lowest 8-neighbor
    let bestDi = 0, bestDj = 0;
    let lowestH = revenueData[cj * GRID + ci];
    for (let dj = -1; dj <= 1; dj++) {
      for (let di = -1; di <= 1; di++) {
        if (di === 0 && dj === 0) continue;
        const ni = ci + di, nj = cj + dj;
        if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
        const nh = revenueData[nj * GRID + ni];
        if (nh < lowestH) { lowestH = nh; bestDi = di; bestDj = dj; }
      }
    }
    if (bestDi === 0 && bestDj === 0) break; // local minimum reached
    ci += bestDi;
    cj += bestDj;
  }
  return path;
}
function getBFSPath(timeIndex, startI, startJ, revenueData) {
  if (!bfsCache.has(timeIndex)) {
    bfsCache.set(timeIndex, new Map());
  }
  const timeCache = bfsCache.get(timeIndex);
  const skey = `${startI},${startJ}`;
  if (timeCache.has(skey)) {
    cacheStats.bfs.hits++;
    return timeCache.get(skey);
  }
  cacheStats.bfs.misses++;
  const path = bfsDownhillPath(startI, startJ, revenueData);
  timeCache.set(skey, path);
  return path;
}
function buildRiverGeometry(hotspot, revenueData, timeIndex) {
  const cacheKey = `${timeIndex}:${hotspot.i}:${hotspot.j}`;
  if (riverCache.has(cacheKey)) {
    cacheStats.river.hits++;
    return riverCache.get(cacheKey).clone();
  }
  cacheStats.river.misses++;
  const path = getBFSPath(timeIndex, hotspot.i, hotspot.j, revenueData);
  if (path.length < 3) return null;
  // Convert grid path to 3D points
  const points = path.map(p => {
    const h = revenueData[p.j * GRID + p.i];
    const w = gridToWorld(p.i, p.j, h);
    return new THREE.Vector3(w.x, w.y + 0.08, w.z);
  });
  const curve = new THREE.CatmullRomCurve3(points);
  const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.06, 6, false);
  riverCache.set(cacheKey, tubeGeo);
  return tubeGeo.clone();
}
// ──────────────────────────────────────────────
// Particle system (BufferGeometry with position array reuse)
// ──────────────────────────────────────────────
let particleGeometry, particleMaterial, particleMesh;
let particleData = []; // { targetI, targetJ, progress, speed }
let particlePositions; // Float32Array reference to geometry attribute
let particleGradientMap = null; // cached flow directions, rebuilt on terrain change
let lastTerrainForGradient = -1;
function buildGradientMap(revenueData) {
  // Precompute downhill direction for each cell (lazy, on terrain change)
  const gradient = new Int8Array(GRID * GRID * 2); // di, dj per cell
  for (let j = 0; j < GRID; j++) {
    for (let i = 0; i < GRID; i++) {
      let bestDi = 0, bestDj = 0;
      let lowestH = revenueData[j * GRID + i];
      for (let dj = -1; dj <= 1; dj++) {
        for (let di = -1; di <= 1; di++) {
          if (di === 0 && dj === 0) continue;
          const ni = i + di, nj = j + dj;
          if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
          const nh = revenueData[nj * GRID + ni];
          if (nh < lowestH) { lowestH = nh; bestDi = di; bestDj = dj; }
        }
      }
      const idx = (j * GRID + i) * 2;
      gradient[idx] = bestDi;
      gradient[idx + 1] = bestDj;
    }
  }
  return gradient;
}
function getGradientMap(timeIndex, revenueData) {
  if (lastTerrainForGradient === timeIndex && particleGradientMap) {
    return particleGradientMap;
  }
  particleGradientMap = buildGradientMap(revenueData);
  lastTerrainForGradient = timeIndex;
  return particleGradientMap;
}
function initParticles(scene, revenueData, timeIndex) {
  if (particleMesh) {
    scene.remove(particleMesh);
    particleGeometry.dispose();
    particleMaterial.dispose();
  }
  particleGeometry = new THREE.BufferGeometry();
  const count = PARTICLE_COUNT;
  particlePositions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  // Ensure gradient map is built
  const gradMap = getGradientMap(timeIndex, revenueData);
  // Seed particles at high user-density areas
  particleData = [];
  for (let p = 0; p < count; p++) {
    // Pick a random cell biased toward high terrain
    let gi, gj;
    for (let attempts = 0; attempts < 20; attempts++) {
      gi = Math.floor(Math.random() * GRID);
      gj = Math.floor(Math.random() * GRID);
      if (revenueData[gj * GRID + gi] > Math.random() * 0.6) break;
    }
    const h = revenueData[gj * GRID + gi];
    const w = gridToWorld(gi, gj, h);
    particlePositions[p * 3] = w.x;
    particlePositions[p * 3 + 1] = w.y + 0.12;
    particlePositions[p * 3 + 2] = w.z;
    // Particle color: warm yellow-orange
    colors[p * 3] = 1.0;
    colors[p * 3 + 1] = 0.75 + Math.random() * 0.25;
    colors[p * 3 + 2] = 0.15 + Math.random() * 0.2;
    particleData.push({
      gi, gj,
      progress: Math.random(),
      speed: 0.002 + Math.random() * 0.006
    });
  }
  particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  particleGeometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  particleMaterial = new THREE.PointsMaterial({
    size: 0.06,
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7
  });
  particleMesh = new THREE.Points(particleGeometry, particleMaterial);
  scene.add(particleMesh);
}
function updateParticles(revenueData, timeIndex) {
  if (!particleMesh || !particlePositions) return;
  const gradMap = getGradientMap(timeIndex, revenueData);
  for (let p = 0; p < particleData.length; p++) {
    const pd = particleData[p];
    pd.progress += pd.speed;
    if (pd.progress >= 1.0) {
      // Respawn at new location
      pd.progress = 0;
      let gi, gj;
      for (let a = 0; a < 15; a++) {
        gi = Math.floor(Math.random() * GRID);
        gj = Math.floor(Math.random() * GRID);
        if (revenueData[gj * GRID + gi] > 0.15) break;
      }
      pd.gi = gi; pd.gj = gj;
    } else {
      // Flow downhill using cached gradient
      const gIdx = (pd.gj * GRID + pd.gi) * 2;
      const di = gradMap[gIdx];
      const dj = gradMap[gIdx + 1];
      if (di !== 0 || dj !== 0) {
        // Move toward neighbor cell
        const ni = pd.gi + di;
        const nj = pd.gj + dj;
        if (ni >= 0 && ni < GRID && nj >= 0 && nj < GRID) {
          pd.gi = ni;
          pd.gj = nj;
        }
      }
    }
    // Place particle at grid position on terrain surface
    const gi = Math.round(pd.gi);
    const gj = Math.round(pd.gj);
    const giClamped = Math.max(0, Math.min(GRID - 1, gi));
    const gjClamped = Math.max(0, Math.min(GRID - 1, gj));
    const h = revenueData[gjClamped * GRID + giClamped];
    const w = gridToWorld(giClamped, gjClamped, h);
    const i3 = p * 3;
    particlePositions[i3] = w.x;
    particlePositions[i3 + 1] = w.y + 0.12;
    particlePositions[i3 + 2] = w.z;
  }
  particleGeometry.attributes.position.needsUpdate = true;
}
// ──────────────────────────────────────────────
// Scene setup
// ──────────────────────────────────────────────
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a14);
scene.fog = new THREE.Fog(0x0a0a14, 18, 40);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 60);
camera.position.set(9, 6.5, 11);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
// OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 1.5, 0);
controls.minDistance = 3;
controls.maxDistance = 22;
controls.maxPolarAngle = Math.PI * 0.45;
controls.update();
// Lighting
const ambientLight = new THREE.AmbientLight(0x334466, 1.6);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 2.8);
sunLight.position.set(8, 12, 4);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(1024, 1024);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 40;
sunLight.shadow.camera.left = -10;
sunLight.shadow.camera.right = 10;
sunLight.shadow.camera.top = 10;
sunLight.shadow.camera.bottom = -10;
scene.add(sunLight);
const rimLight = new THREE.DirectionalLight(0x4488cc, 1.0);
rimLight.position.set(-4, 2, -6);
scene.add(rimLight);
// Base grid plane
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SCALE / 2 + 0.3, 24, 12, 64, 0x334466, 0x1a2a3a);
gridHelper.position.y = -0.02;
scene.add(gridHelper);
// ──────────────────────────────────────────────
// Data storage
// ──────────────────────────────────────────────
const allTimeData = []; // Array of { revenue, users, errors, apiCalls }
let currentTimeIndex = 0;
let terrainMesh = null;
const riverMeshes = [];
let realElevationData = null;
let dataSourceLabel = 'synthetic';
// ──────────────────────────────────────────────
// Terrain swap
// ──────────────────────────────────────────────
function swapTerrain(timeIndex) {
  if (timeIndex < 0 || timeIndex >= allTimeData.length) return;
  currentTimeIndex = timeIndex;
  const data = allTimeData[timeIndex];
  // Remove old terrain
  if (terrainMesh) {
    scene.remove(terrainMesh);
    // Dispose old geometry — but NOT cached ones
    if (terrainMesh.geometry && !terrainCache.has(timeIndex)) {
      terrainMesh.geometry.dispose();
    }
  }
  // Get cached or build new geometry
  const geo = getTerrainGeometry(timeIndex, data);
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.55,
    metalness: 0.08,
    flatShading: false,
    side: THREE.DoubleSide
  });
  terrainMesh = new THREE.Mesh(geo, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  // Update UI
  document.getElementById('time-label').textContent = `${timeIndex + 1} / ${TIME_STEPS}`;
  document.getElementById('time-slider').value = timeIndex;
  const peakH = Math.max(...data.revenue);
  document.getElementById('peak-val').textContent = (peakH * HEIGHT_SCALE).toFixed(2);
  // Error hotspots
  const hotspots = findErrorHotspots(data.errors);
  document.getElementById('error-count').textContent = hotspots.length;
  // Schedule debounced river rebuild
  scheduleRiverRebuild(timeIndex, data);
}
// ──────────────────────────────────────────────
// Debounced river rebuild
// ──────────────────────────────────────────────
let riverRebuildTimer = null;
function scheduleRiverRebuild(timeIndex, data) {
  if (riverRebuildTimer) clearTimeout(riverRebuildTimer);
  riverRebuildTimer = setTimeout(() => {
    rebuildRivers(timeIndex, data);
  }, RIVER_DEBOUNCE_MS);
}
function rebuildRivers(timeIndex, data) {
  // Remove old rivers
  for (const rm of riverMeshes) {
    scene.remove(rm);
    // Don't dispose — they're cached
  }
  riverMeshes.length = 0;
  const hotspots = findErrorHotspots(data.errors);
  for (const hs of hotspots) {
    const tubeGeo = buildRiverGeometry(hs, data.revenue, timeIndex);
    if (!tubeGeo) continue;
    const mat = new THREE.MeshStandardMaterial({
      color: 0xff3333,
      roughness: 0.3,
      metalness: 0.4,
      emissive: 0x330000,
      emissiveIntensity: 0.6
    });
    const mesh = new THREE.Mesh(tubeGeo, mat);
    mesh.renderOrder = 1;
    mesh.material.depthTest = true;
    mesh.material.depthWrite = true;
    scene.add(mesh);
    riverMeshes.push(mesh);
  }
}
// ──────────────────────────────────────────────
// Camera bookmarks (localStorage)
// ──────────────────────────────────────────────
const BOOKMARK_KEY = 'terrain_explorer_bookmarks';
function loadBookmarks() {
  try {
    const raw = localStorage.getItem(BOOKMARK_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch { return []; }
}
function saveBookmarks(bookmarks) {
  localStorage.setItem(BOOKMARK_KEY, JSON.stringify(bookmarks));
}
function renderBookmarkBar() {
  const bar = document.getElementById('bookmark-bar');
  const bookmarks = loadBookmarks();
  bar.innerHTML = '';
  for (let i = 0; i < bookmarks.length; i++) {
    const bm = bookmarks[i];
    const btn = document.createElement('button');
    btn.textContent = bm.name || `View ${i + 1}`;
    btn.onclick = () => goToBookmark(i);
    const del = document.createElement('button');
    del.textContent = '×';
    del.className = 'del';
    del.onclick = (e) => { e.stopPropagation(); deleteBookmark(i); };
    bar.appendChild(btn);
    bar.appendChild(del);
  }
}
function goToBookmark(index) {
  const bookmarks = loadBookmarks();
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  camera.position.set(bm.px, bm.py, bm.pz);
  controls.target.set(bm.tx, bm.ty, bm.tz);
  controls.update();
}
function deleteBookmark(index) {
  const bookmarks = loadBookmarks();
  bookmarks.splice(index, 1);
  saveBookmarks(bookmarks);
  renderBookmarkBar();
}
function saveCurrentBookmark() {
  const bookmarks = loadBookmarks();
  const name = `View ${bookmarks.length + 1}`;
  bookmarks.push({
    name,
    px: camera.position.x, py: camera.position.y, pz: camera.position.z,
    tx: controls.target.x, ty: controls.target.y, tz: controls.target.z
  });
  saveBookmarks(bookmarks);
  renderBookmarkBar();
}
document.getElementById('save-bm').addEventListener('click', saveCurrentBookmark);
// ──────────────────────────────────────────────
// Time slider
// ──────────────────────────────────────────────
const slider = document.getElementById('time-slider');
slider.addEventListener('input', () => {
  const idx = parseInt(slider.value);
  swapTerrain(idx);
});
// ──────────────────────────────────────────────
// Keyboard shortcuts
// ──────────────────────────────────────────────
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r': controls.autoRotate = !controls.autoRotate; break;
    case 'f': controls.target.set(0, 1.5, 0); camera.position.set(9, 6.5, 11); controls.update(); break;
    case 't': camera.position.set(0, 14, 0.5); controls.target.set(0, 0, 0); controls.update(); break;
    case 'arrowleft': if (currentTimeIndex > 0) swapTerrain(currentTimeIndex - 1); break;
    case 'arrowright': if (currentTimeIndex < TIME_STEPS - 1) swapTerrain(currentTimeIndex + 1); break;
    case 'b': saveCurrentBookmark(); break;
  }
});
// ──────────────────────────────────────────────
// Resize handler
// ──────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ──────────────────────────────────────────────
// FPS counter
// ──────────────────────────────────────────────
let frameCount = 0;
let fpsTime = performance.now();
let currentFPS = 0;
// ──────────────────────────────────────────────
// Animation loop
// ──────────────────────────────────────────────
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  // Update particles (reuses position array — no allocation)
  if (currentTimeIndex < allTimeData.length) {
    updateParticles(allTimeData[currentTimeIndex].revenue, currentTimeIndex);
  }
  renderer.render(scene, camera);
  // FPS tracking
  frameCount++;
  if (timestamp - fpsTime >= 1000) {
    currentFPS = Math.round(frameCount / ((timestamp - fpsTime) / 1000));
    frameCount = 0;
    fpsTime = timestamp;
    document.getElementById('fps-val').textContent = currentFPS;
    updateDiagnostics();
  }
  // Drain validation log periodically
  if (frameCount % 60 === 0) drainValidationLog();
}
// ──────────────────────────────────────────────
// Startup
// ──────────────────────────────────────────────
async function startup() {
  // Attempt real elevation data fetch
  const realResult = await fetchRealElevationData();
  if (realResult) {
    realElevationData = realResult.elevation;
    dataSourceLabel = realResult.source;
    document.getElementById('ds-source').textContent = 'real+synth';
  }
  // Generate all time steps
  for (let t = 0; t < TIME_STEPS; t++) {
    const tn = t / (TIME_STEPS - 1 || 1);
    const synthetic = generateSyntheticData(tn);
    let revenue;
    if (realElevationData) {
      revenue = blendRealWithSynthetic(realElevationData, synthetic.revenue, tn);
    } else {
      revenue = synthetic.revenue;
    }
    allTimeData.push({
      revenue,
      users: synthetic.users,
      errors: synthetic.errors,
      apiCalls: synthetic.apiCalls
    });
  }
  // Set slider max
  slider.max = TIME_STEPS - 1;
  // Build initial terrain
  swapTerrain(0);
  // Initialize particles
  initParticles(scene, allTimeData[0].revenue, 0);
  // Render bookmarks
  renderBookmarkBar();
  // Start render loop
  requestAnimationFrame(animate);
}
startup().catch(err => {
  console.error('Startup failed:', err);
  document.getElementById('status').textContent = 'ERROR: ' + err.message;
  document.getElementById('status').style.color = '#ff4d4d';
});
</script>
</body>
</html>