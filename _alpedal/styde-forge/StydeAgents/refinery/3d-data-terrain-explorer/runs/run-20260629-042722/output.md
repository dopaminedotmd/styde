<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a0f;--panel-bg:rgba(16,16,26,0.94);--text:#c8ccd4;--accent:#5b9bd5;--danger:#e0556a;--slider-track:#1e1e32;--border:rgba(255,255,255,0.06)}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  canvas{display:block}
  #panel{position:fixed;top:16px;left:16px;background:var(--panel-bg);border:1px solid var(--border);border-radius:12px;padding:18px 20px;min-width:260px;backdrop-filter:blur(16px);z-index:10}
  #panel h2{font-size:15px;font-weight:600;margin-bottom:12px;color:#e8ecf2;letter-spacing:0.3px}
  .metric-row{display:flex;justify-content:space-between;align-items:center;padding:5px 0;font-size:12px}
  .metric-label{color:#8892a0}
  .metric-value{font-weight:600;font-variant-numeric:tabular-nums}
  .val-revenue{color:#4ecdc4}
  .val-users{color:#a8e6cf}
  .val-errors{color:var(--danger)}
  #time-slider-container{position:fixed;bottom:28px;left:50%;transform:translateX(-50%);background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:12px 24px;display:flex;align-items:center;gap:14px;backdrop-filter:blur(16px);z-index:10}
  #time-slider{-webkit-appearance:none;width:320px;height:6px;border-radius:3px;background:var(--slider-track);outline:none;cursor:pointer}
  #time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:var(--accent);cursor:pointer;border:2px solid #fff;box-shadow:0 0 10px rgba(91,155,213,0.5)}
  #time-label{font-size:13px;font-weight:600;color:var(--accent);min-width:60px;text-align:center;font-variant-numeric:tabular-nums}
  #bookmarks{position:fixed;top:16px;right:16px;background:var(--panel-bg);border:1px solid var(--border);border-radius:12px;padding:14px 16px;backdrop-filter:blur(16px);z-index:10;font-size:12px}
  #bookmarks h3{font-size:13px;margin-bottom:8px;color:#e8ecf2}
  .bm-row{display:flex;align-items:center;gap:8px;padding:3px 0;cursor:pointer;border-radius:4px;padding:4px 8px;transition:background 0.15s}
  .bm-row:hover{background:rgba(255,255,255,0.06)}
  .bm-key{background:rgba(91,155,213,0.2);color:var(--accent);padding:1px 7px;border-radius:3px;font-size:11px;font-weight:600;min-width:22px;text-align:center}
  .bm-name{color:var(--text)}
  #hint{position:fixed;bottom:80px;left:50%;transform:translateX(-50%);font-size:11px;color:#556;pointer-events:none;z-index:5;transition:opacity 0.6s}
  #legend{position:fixed;bottom:28px;right:28px;background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:10px 14px;backdrop-filter:blur(16px);z-index:10;font-size:11px}
  .legend-item{display:flex;align-items:center;gap:8px;padding:2px 0}
  .legend-swatch{width:12px;height:12px;border-radius:3px}
</style>
</head>
<body>
<div id="panel">
  <h2>DATA TERRAIN</h2>
  <div class="metric-row"><span class="metric-label">Revenue (elevation)</span><span class="metric-value val-revenue" id="m-rev">--</span></div>
  <div class="metric-row"><span class="metric-label">Users (vegetation)</span><span class="metric-value val-users" id="m-users">--</span></div>
  <div class="metric-row"><span class="metric-label">Error Rate (rivers)</span><span class="metric-value val-errors" id="m-err">--</span></div>
</div>
<div id="bookmarks">
  <h3>CAMERA BOOKMARKS</h3>
  <div class="bm-row" data-bm="0"><span class="bm-key">1</span><span class="bm-name">Overview</span></div>
  <div class="bm-row" data-bm="1"><span class="bm-key">2</span><span class="bm-name">Top-down</span></div>
  <div class="bm-row" data-bm="2"><span class="bm-key">3</span><span class="bm-name">River trace</span></div>
  <div class="bm-row" data-bm="3"><span class="bm-key">S</span><span class="bm-name">Save view</span></div>
</div>
<div id="legend">
  <div class="legend-item"><span class="legend-swatch" style="background:#4ecdc4"></span>Revenue (height)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#a8e6cf"></span>Users (color)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#e0556a"></span>Errors (rivers)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ffe66d"></span>API calls (particles)</div>
</div>
<div id="hint">Drag to orbit &bull; Scroll to zoom &bull; Right-drag to pan &bull; Press 1-3 for bookmarks &bull; S to save view</div>
<div id="time-slider-container">
  <span style="font-size:12px;color:#8892a0">Day</span>
  <input type="range" id="time-slider" min="0" max="29" value="0" step="1">
  <span id="time-label">1</span>
  <span style="font-size:12px;color:#8892a0">30</span>
</div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─── DETERMINISTIC DATA GENERATOR ──────────────────────────────────────────
// 30 days, 32x32 grid. Revenue = elevation, users = vegetation color, errors = rivers.
const GRID = 32;
const DAYS = 30;
const TERRAIN_SPAN = 20; // world-space extent
function generateDayData(day) {
  // Seed each day deterministically from day index — no random noise.
  // Uses a simple sinusoidal terrain with day-dependent amplitude/phase so
  // scrubbing time shows gradual evolution, not random jumps.
  const t = day / (DAYS - 1); // 0..1
  const revenue = new Float32Array(GRID * GRID);
  const users = new Float32Array(GRID * GRID);
  const errors = new Float32Array(GRID * GRID);
  // Base terrain: two overlapping gaussian hills that shift position over time
  const cx1 = 0.25 + t * 0.35;
  const cz1 = 0.35 + Math.sin(t * Math.PI) * 0.2;
  const cx2 = 0.70 - t * 0.30;
  const cz2 = 0.65 - Math.cos(t * Math.PI) * 0.2;
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const nx = ix / (GRID - 1);
      const nz = iz / (GRID - 1);
      // Revenue: sum of two gaussians + gentle slope
      const d1 = Math.sqrt((nx - cx1) ** 2 + (nz - cz1) ** 2);
      const d2 = Math.sqrt((nx - cx2) ** 2 + (nz - cz2) ** 2);
      const hill1 = Math.exp(-d1 * d1 / 0.08);
      const hill2 = Math.exp(-d2 * d2 / 0.06);
      let rev = hill1 * 0.8 + hill2 * 0.55 + 0.05;
      // Day-dependent amplitude
      rev *= 0.7 + 0.3 * (0.5 + 0.5 * Math.sin(t * 2.5 + nx * 2));
      // Users: correlated with revenue but with spatial offset
      const ud1 = Math.sqrt((nx - cx1 - 0.08) ** 2 + (nz - cz1 + 0.05) ** 2);
      const ud2 = Math.sqrt((nx - cx2 + 0.06) ** 2 + (nz - cz2 - 0.04) ** 2);
      let usr = Math.exp(-ud1 * ud1 / 0.07) * 0.65 + Math.exp(-ud2 * ud2 / 0.055) * 0.45;
      usr *= 0.7 + 0.3 * (0.5 + 0.5 * Math.cos(t * 1.8 + nz * 2.2));
      // Errors: inverse-correlated — valleys and edges collect more errors
      const ridge = Math.abs(nx - 0.5) + Math.abs(nz - 0.5);
      let err = (1.0 - rev) * 0.35 + ridge * 0.12;
      // Spike on specific days in specific regions
      if (day >= 12 && day <= 16 && nx > 0.45 && nx < 0.55 && nz > 0.55 && nz < 0.65) {
        err += 0.15 * (1 - Math.abs(day - 14) / 2);
      }
      err = Math.max(0, Math.min(1, err));
      revenue[idx] = rev;
      users[idx] = usr;
      errors[idx] = err;
    }
  }
  return { revenue, users, errors };
}
// Pre-generate all day data
const allDays = [];
for (let d = 0; d < DAYS; d++) allDays.push(generateDayData(d));
// ─── THREE.JS SETUP ────────────────────────────────────────────────────────
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a0f');
scene.fog = new THREE.Fog('#0a0a0f', 18, 55);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(14, 10, 16);
camera.lookAt(TERRAIN_SPAN / 2, 0, TERRAIN_SPAN / 2);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(TERRAIN_SPAN / 2, 0, TERRAIN_SPAN / 2);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.25;
controls.minDistance = 4;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// ─── LIGHTING ──────────────────────────────────────────────────────────────
const ambient = new THREE.AmbientLight('#334466', 1.6);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffeacc', 3.5);
sun.position.set(18, 22, 8);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
sun.shadow.bias = -0.0003;
sun.shadow.normalBias = 0.015;
scene.add(sun);
const rim = new THREE.DirectionalLight('#8899cc', 1.2);
rim.position.set(-5, 3, -8);
scene.add(rim);
// ─── GEOMETRY CACHE ────────────────────────────────────────────────────────
// Pre-build BufferGeometry for every day. On slider change, swap buffers.
const geometryCache = [];
const terrainMaxHeight = 4.5; // world-space max elevation
function buildTerrainGeometry(dayData) {
  const { revenue, users } = dayData;
  const geo = new THREE.BufferGeometry();
  const vertices = new Float32Array(GRID * GRID * 3);
  const colors = new Float32Array(GRID * GRID * 3);
  const indices = [];
  // Vertex positions
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      const vi = idx * 3;
      const x = (ix / (GRID - 1)) * TERRAIN_SPAN;
      const z = (iz / (GRID - 1)) * TERRAIN_SPAN;
      const y = revenue[idx] * terrainMaxHeight;
      vertices[vi] = x;
      vertices[vi + 1] = y;
      vertices[vi + 2] = z;
      // Color: vegetation gradient (users metric) — green for high users, brown for low
      const u = users[idx];
      const r = 0.12 + u * 0.08;
      const g = 0.18 + u * 0.62;
      const b = 0.10 + u * 0.15;
      colors[vi] = r;
      colors[vi + 1] = g;
      colors[vi + 2] = b;
    }
  }
  // Indices
  for (let iz = 0; iz < GRID - 1; iz++) {
    for (let ix = 0; ix < GRID - 1; ix++) {
      const a = iz * GRID + ix;
      const b = a + 1;
      const c = a + GRID;
      const d = c + 1;
      indices.push(a, c, b);
      indices.push(b, c, d);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
for (let d = 0; d < DAYS; d++) {
  geometryCache.push(buildTerrainGeometry(allDays[d]));
}
// ─── TERRAIN MESH ──────────────────────────────────────────────────────────
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(geometryCache[0], terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// ─── BASE PLANE ────────────────────────────────────────────────────────────
const baseGeo = new THREE.PlaneGeometry(TERRAIN_SPAN + 6, TERRAIN_SPAN + 6);
const baseMat = new THREE.MeshStandardMaterial({ color: '#111122', roughness: 0.9, metalness: 0.1 });
const basePlane = new THREE.Mesh(baseGeo, baseMat);
basePlane.rotation.x = -Math.PI / 2;
basePlane.position.set(TERRAIN_SPAN / 2, -0.15, TERRAIN_SPAN / 2);
basePlane.receiveShadow = true;
scene.add(basePlane);
// ─── RIVER SYSTEM ──────────────────────────────────────────────────────────
// Trace error paths: connect adjacent high-error cells into river lines.
// Uses BufferGeometry with LineSegments for performance.
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const riverCache = [];
function buildRiverGeometry(dayData) {
  const { errors, revenue } = dayData;
  const threshold = 0.35;
  const points = [];
  const width = 0.06;
  const color = new THREE.Color('#e0556a');
  // Find high-error cells and connect to neighbors with steepest error gradient
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const idx = iz * GRID + ix;
      if (errors[idx] < threshold) continue;
      const x = (ix / (GRID - 1)) * TERRAIN_SPAN;
      const z = (iz / (GRID - 1)) * TERRAIN_SPAN;
      const y = revenue[idx] * terrainMaxHeight + 0.02;
      // Look at 8 neighbors, flow toward highest error neighbor
      let bestDr = 0, bestDi = -1, bestDj = -1;
      for (let dj = -1; dj <= 1; dj++) {
        for (let di = -1; di <= 1; di++) {
          if (di === 0 && dj === 0) continue;
          const ni = ix + di, nj = iz + dj;
          if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
          const nidx = nj * GRID + ni;
          const dr = errors[nidx] - errors[idx];
          if (dr > bestDr) { bestDr = dr; bestDi = di; bestDj = dj; }
        }
      }
      if (bestDr > 0 && bestDi !== -1) {
        const nx = ((ix + bestDi * 0.7) / (GRID - 1)) * TERRAIN_SPAN;
        const nz = ((iz + bestDj * 0.7) / (GRID - 1)) * TERRAIN_SPAN;
        const ny = revenue[(iz + bestDj) * GRID + (ix + bestDi)] * terrainMaxHeight + 0.02;
        points.push(x, y, z, nx, ny, nz);
      }
    }
  }
  if (points.length === 0) {
    const empty = new THREE.BufferGeometry();
    empty.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
    return empty;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(points), 3));
  return geo;
}
for (let d = 0; d < DAYS; d++) {
  riverCache.push(buildRiverGeometry(allDays[d]));
}
function setRiverDay(day) {
  while (riverGroup.children.length > 0) riverGroup.remove(riverGroup.children[0]);
  const geo = riverCache[day];
  if (geo.attributes.position.count > 0) {
    const mat = new THREE.LineBasicMaterial({ color: '#e0556a', linewidth: 1, transparent: true, opacity: 0.75, depthTest: true });
    const lines = new THREE.LineSegments(geo, mat);
    lines.renderOrder = 1;
    lines.material.depthTest = true;
    lines.material.depthWrite = true;
    riverGroup.add(lines);
    // Glow tubes along river paths for visibility
    const tubeMat = new THREE.MeshBasicMaterial({ color: '#ff4466', transparent: true, opacity: 0.35, depthTest: true });
    const pos = geo.attributes.position;
    for (let i = 0; i < pos.count; i += 2) {
      const sx = pos.getX(i), sy = pos.getY(i), sz = pos.getZ(i);
      const ex = pos.getX(i + 1), ey = pos.getY(i + 1), ez = pos.getZ(i + 1);
      const mid = new THREE.Vector3((sx + ex) / 2, (sy + ey) / 2, (sz + ez) / 2);
      const dir = new THREE.Vector3(ex - sx, ey - sy, ez - sz);
      const len = dir.length();
      if (len < 0.01) continue;
      const tubeGeo = new THREE.CylinderGeometry(0.025, 0.025, len, 4, 1);
      const tube = new THREE.Mesh(tubeGeo, tubeMat);
      tube.position.copy(mid);
      tube.rotation.z = Math.PI / 2;
      const up = new THREE.Vector3(0, 1, 0);
      const quat = new THREE.Quaternion().setFromUnitVectors(up, dir.normalize());
      tube.setRotationFromQuaternion(quat);
      tube.renderOrder = 2;
      riverGroup.add(tube);
    }
  }
}
setRiverDay(0);
// ─── PARTICLE SYSTEM ────────────────────────────────────────────────────────
// API call trails: particles flow along the terrain surface, representing data flows.
const PARTICLE_COUNT = 600;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3); // direction & speed
const particleLife = new Float32Array(PARTICLE_COUNT); // remaining life 0..1
const particleMaxLife = 8.0; // seconds
function getTerrainHeight(x, z, dayData) {
  const ix = Math.round((x / TERRAIN_SPAN) * (GRID - 1));
  const iz = Math.round((z / TERRAIN_SPAN) * (GRID - 1));
  const ci = Math.max(0, Math.min(GRID - 1, ix));
  const cz = Math.max(0, Math.min(GRID - 1, iz));
  return dayData.revenue[cz * GRID + ci] * terrainMaxHeight;
}
function resetParticle(i) {
  const vi = i * 3;
  // Spawn at edges, flow toward peaks
  const edge = Math.floor(Math.random() * 4);
  let x, z;
  switch (edge) {
    case 0: x = Math.random() * TERRAIN_SPAN; z = 0; break;
    case 1: x = TERRAIN_SPAN; z = Math.random() * TERRAIN_SPAN; break;
    case 2: x = Math.random() * TERRAIN_SPAN; z = TERRAIN_SPAN; break;
    default: x = 0; z = Math.random() * TERRAIN_SPAN; break;
  }
  particlePositions[vi] = x;
  particlePositions[vi + 1] = 0; // will be set by terrain lookup next frame
  particlePositions[vi + 2] = z;
  // Flow toward center (higher revenue)
  const cx = TERRAIN_SPAN / 2, cz = TERRAIN_SPAN / 2;
  const dx = cx - x, dz = cz - z;
  const dl = Math.sqrt(dx * dx + dz * dz) || 1;
  const speed = 0.3 + Math.random() * 1.2;
  particleVelocities[vi] = (dx / dl) * speed;
  particleVelocities[vi + 1] = 0;
  particleVelocities[vi + 2] = (dz / dl) * speed;
  particleLife[i] = 1.0;
}
// Initialize all particles
for (let i = 0; i < PARTICLE_COUNT; i++) resetParticle(i);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
// Custom shader for glowing particle trails
const particleMat = new THREE.PointsMaterial({
  color: '#ffe66d',
  size: 0.15,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  depthTest: true,
  transparent: true,
  opacity: 0.85,
  sizeAttenuation: true,
});
const particles = new THREE.Points(particleGeo, particleMat);
particles.renderOrder = 3;
scene.add(particles);
// Trail lines: store last N positions per particle for persistent trails
const TRAIL_LENGTH = 8;
const trailHistories = new Float32Array(PARTICLE_COUNT * TRAIL_LENGTH * 3);
// Initialize trail histories to particle positions
for (let i = 0; i < PARTICLE_COUNT; i++) {
  const vi = i * 3;
  for (let t = 0; t < TRAIL_LENGTH; t++) {
    const ti = (i * TRAIL_LENGTH + t) * 3;
    trailHistories[ti] = particlePositions[vi];
    trailHistories[ti + 1] = particlePositions[vi + 1];
    trailHistories[ti + 2] = particlePositions[vi + 2];
  }
}
const trailLinesGeo = new THREE.BufferGeometry();
const trailLinePositions = new Float32Array(PARTICLE_COUNT * TRAIL_LENGTH * 3);
trailLinesGeo.setAttribute('position', new THREE.BufferAttribute(trailLinePositions, 3));
const trailLinesMat = new THREE.LineBasicMaterial({
  color: '#ffe66d',
  transparent: true,
  opacity: 0.25,
  blending: THREE.AdditiveBlending,
  depthTest: true,
  depthWrite: false,
});
// Build trail indices: each particle gets a line strip of TRAIL_LENGTH points,
// but LineSegments is simpler — we use line loop per particle via individual segments
const trailGroup = new THREE.Group();
scene.add(trailGroup);
// Rebuild trail meshes each frame — use pooled Line objects
const trailLinePool = [];
function ensureTrailLines() {
  const needed = PARTICLE_COUNT * (TRAIL_LENGTH - 1);
  while (trailLinePool.length < needed) {
    const segGeo = new THREE.BufferGeometry();
    segGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
    const seg = new THREE.Line(segGeo, trailLinesMat.clone());
    seg.renderOrder = 0;
    trailLinePool.push(seg);
  }
  // Remove excess from scene
  while (trailGroup.children.length > needed) {
    trailGroup.remove(trailGroup.children[trailGroup.children.length - 1]);
  }
  // Add needed lines to scene
  while (trailGroup.children.length < needed) {
    trailGroup.add(trailLinePool[trailGroup.children.length]);
  }
}
ensureTrailLines();
function updateTrails(dt, dayData) {
  // Shift trail histories: move each slot forward
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const base = i * TRAIL_LENGTH * 3;
    // Shift: last slot drops, all others move up
    for (let t = TRAIL_LENGTH - 1; t > 0; t--) {
      const ti = base + t * 3;
      const si = base + (t - 1) * 3;
      trailHistories[ti] = trailHistories[si];
      trailHistories[ti + 1] = trailHistories[si + 1];
      trailHistories[ti + 2] = trailHistories[si + 2];
    }
    // Newest slot = current particle position
    const vi = i * 3;
    trailHistories[base] = particlePositions[vi];
    trailHistories[base + 1] = particlePositions[vi + 1];
    trailHistories[base + 2] = particlePositions[vi + 2];
  }
}
function updateTrailMeshes() {
  let segIdx = 0;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const base = i * TRAIL_LENGTH * 3;
    for (let t = 0; t < TRAIL_LENGTH - 1; t++) {
      const a = base + t * 3;
      const b = base + (t + 1) * 3;
      const seg = trailLinePool[segIdx];
      const pos = seg.geometry.attributes.position;
      pos.setXYZ(0, trailHistories[a], trailHistories[a + 1], trailHistories[a + 2]);
      pos.setXYZ(1, trailHistories[b], trailHistories[b + 1], trailHistories[b + 2]);
      pos.needsUpdate = true;
      seg.material.opacity = 0.08 + (t / TRAIL_LENGTH) * 0.18;
      segIdx++;
    }
  }
}
// ─── CAMERA BOOKMARKS ──────────────────────────────────────────────────────
const bookmarks = [
  { pos: [14, 10, 16], target: [TERRAIN_SPAN / 2, 0, TERRAIN_SPAN / 2], name: 'Overview' },
  { pos: [TERRAIN_SPAN / 2, 22, TERRAIN_SPAN / 2], target: [TERRAIN_SPAN / 2, 0, TERRAIN_SPAN / 2 + 0.5], name: 'Top-down' },
  { pos: [6, 3.5, 11], target: [10, 0.3, 10], name: 'River trace' },
];
const savedBookmarks = [...bookmarks]; // index 3+ are user-saved
function applyBookmark(bm) {
  const startPos = camera.position.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const startTarget = controls.target.clone();
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 800; // ms
  function animate() {
    const elapsed = performance.now() - startTime;
    const t = Math.min(1, elapsed / duration);
    // Ease in-out cubic
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animate);
    }
  }
  animate();
}
// ─── UI BINDINGS ───────────────────────────────────────────────────────────
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const hintEl = document.getElementById('hint');
let currentDay = 0;
function setDay(day) {
  currentDay = day;
  // Swap terrain geometry from cache
  terrainMesh.geometry.dispose();
  terrainMesh.geometry = geometryCache[day];
  setRiverDay(day);
  // Update particles: use new day's revenue for terrain height lookups
  slider.value = day;
  timeLabel.textContent = day + 1;
  // Update metric display
  const d = allDays[day];
  let sumRev = 0, sumUsers = 0, sumErr = 0;
  const n = GRID * GRID;
  for (let i = 0; i < n; i++) {
    sumRev += d.revenue[i];
    sumUsers += d.users[i];
    sumErr += d.errors[i];
  }
  document.getElementById('m-rev').textContent = '$' + (sumRev / n * 10000).toFixed(0);
  document.getElementById('m-users').textContent = (sumUsers / n * 1000).toFixed(0);
  document.getElementById('m-err').textContent = (sumErr / n * 100).toFixed(1) + '%';
}
slider.addEventListener('input', () => {
  setDay(parseInt(slider.value));
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  const key = e.key;
  if (key === '1') applyBookmark(savedBookmarks[0]);
  else if (key === '2') applyBookmark(savedBookmarks[1]);
  else if (key === '3') applyBookmark(savedBookmarks[2]);
  else if (key === 's' || key === 'S') {
    // Save current view
    const bm = {
      pos: [camera.position.x, camera.position.y, camera.position.z],
      target: [controls.target.x, controls.target.y, controls.target.z],
      name: 'Saved ' + (savedBookmarks.length - 2),
    };
    savedBookmarks.push(bm);
    // Add to UI
    const bmRow = document.createElement('div');
    bmRow.className = 'bm-row';
    bmRow.dataset.bm = savedBookmarks.length - 1;
    bmRow.innerHTML = '<span class="bm-key">S' + (savedBookmarks.length - 3) + '</span><span class="bm-name">' + bm.name + '</span>';
    bmRow.addEventListener('click', () => applyBookmark(savedBookmarks[parseInt(bmRow.dataset.bm)]));
    document.getElementById('bookmarks').appendChild(bmRow);
  }
  // Arrow keys to scrub time
  else if (key === 'ArrowLeft' && currentDay > 0) setDay(currentDay - 1);
  else if (key === 'ArrowRight' && currentDay < DAYS - 1) setDay(currentDay + 1);
  else if (key === 'r' || key === 'R') {
    controls.autoRotate = !controls.autoRotate;
  }
});
// Bookmark click handlers
document.querySelectorAll('.bm-row[data-bm]').forEach(row => {
  row.addEventListener('click', () => {
    const idx = parseInt(row.dataset.bm);
    if (idx < savedBookmarks.length) applyBookmark(savedBookmarks[idx]);
  });
});
// Hide hint after a few seconds
setTimeout(() => { hintEl.style.opacity = '0'; }, 8000);
// ─── RENDER LOOP ───────────────────────────────────────────────────────────
const clock = new THREE.Clock();
let trailUpdateAccum = 0;
const TRAIL_UPDATE_INTERVAL = 0.05; // update trails every 50ms
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  // Update particles: move along velocity, clamp to terrain, reset when life ends
  const dayData = allDays[currentDay];
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const vi = i * 3;
    particleLife[i] -= dt / particleMaxLife;
    if (particleLife[i] <= 0) {
      resetParticle(i);
    }
    // Move
    particlePositions[vi] += particleVelocities[vi] * dt;
    particlePositions[vi + 2] += particleVelocities[vi + 2] * dt;
    // Wrap at bounds
    if (particlePositions[vi] < 0) particlePositions[vi] += TERRAIN_SPAN;
    if (particlePositions[vi] > TERRAIN_SPAN) particlePositions[vi] -= TERRAIN_SPAN;
    if (particlePositions[vi + 2] < 0) particlePositions[vi + 2] += TERRAIN_SPAN;
    if (particlePositions[vi + 2] > TERRAIN_SPAN) particlePositions[vi + 2] -= TERRAIN_SPAN;
    // Set height from terrain
    particlePositions[vi + 1] = getTerrainHeight(particlePositions[vi], particlePositions[vi + 2], dayData) + 0.12;
  }
  particleGeo.attributes.position.needsUpdate = true;
  // Update trails at reduced rate for performance
  trailUpdateAccum += dt;
  if (trailUpdateAccum >= TRAIL_UPDATE_INTERVAL) {
    trailUpdateAccum -= TRAIL_UPDATE_INTERVAL;
    updateTrails(trailUpdateAccum + TRAIL_UPDATE_INTERVAL, dayData);
    updateTrailMeshes();
  }
  renderer.render(scene, camera);
}
// ─── RESIZE ────────────────────────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ─── START ─────────────────────────────────────────────────────────────────
setDay(0);
animate();
console.log('3D Data Terrain Explorer ready — ' + DAYS + ' days, ' + GRID + 'x' + GRID + ' grid, ' + PARTICLE_COUNT + ' particles, ' + geometryCache.length + ' cached geometries');
</script>
</body>
</html>