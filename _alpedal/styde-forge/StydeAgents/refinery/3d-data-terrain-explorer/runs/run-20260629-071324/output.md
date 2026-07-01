<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{overflow:hidden;background:#0a0a14;font-family:'Segoe UI',system-ui,sans-serif}
  #canvas-container{position:fixed;inset:0}
  #panel{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:12px;z-index:10}
  .panel-card{background:rgba(10,10,20,0.85);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px 18px;color:#c8ccd4;min-width:150px}
  .panel-card .label{font-size:10px;text-transform:uppercase;letter-spacing:0.08em;color:#6a6f7a;margin-bottom:4px}
  .panel-card .value{font-size:20px;font-weight:600;color:#e8ecf0}
  .panel-card .value.revenue{color:#4ecb71}
  .panel-card .value.errors{color:#e0556a}
  .panel-card .value.particles{color:#5b9cf5}
  #time-slider-container{position:fixed;bottom:100px;left:50%;transform:translateX(-50%);width:400px;max-width:80vw;z-index:10}
  #time-slider{-webkit-appearance:none;width:100%;height:6px;border-radius:3px;background:rgba(255,255,255,0.08);outline:none}
  #time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#4ecb71;cursor:pointer;border:2px solid #0a0a14}
  #time-label{text-align:center;color:#6a6f7a;font-size:11px;margin-top:6px;letter-spacing:0.04em}
  #bookmark-bar{position:fixed;top:16px;right:16px;display:flex;flex-direction:column;gap:6px;z-index:10}
  .bookmark-btn{background:rgba(10,10,20,0.8);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.1);border-radius:6px;color:#8a8f9a;padding:8px 14px;cursor:pointer;font-size:11px;transition:all 0.2s}
  .bookmark-btn:hover{color:#e8ecf0;border-color:rgba(255,255,255,0.25);background:rgba(20,20,40,0.85)}
  .bookmark-btn.saved{color:#4ecb71;border-color:rgba(78,203,113,0.3)}
  #hint{position:fixed;bottom:140px;left:50%;transform:translateX(-50%);color:#4a4f5a;font-size:11px;z-index:10;pointer-events:none}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hint">drag orbit · scroll zoom · right-drag pan · B save bookmark · 1-4 recall</div>
<div id="bookmark-bar"></div>
<div id="panel">
  <div class="panel-card"><div class="label">Revenue</div><div class="value revenue" id="val-revenue">--</div></div>
  <div class="panel-card"><div class="label">Active Users</div><div class="value" id="val-users">--</div></div>
  <div class="panel-card"><div class="label">Error Count</div><div class="value errors" id="val-errors">--</div></div>
  <div class="panel-card"><div class="label">API Calls/sec</div><div class="value particles" id="val-api">--</div></div>
</div>
<div id="time-slider-container">
  <input type="range" id="time-slider" min="0" max="11" value="0" step="1">
  <div id="time-label">Month 1</div>
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
// ═══════════════════════════════════════════════
// SECTION: Dependency guard
// ═══════════════════════════════════════════════
if (!THREE || !THREE.BufferGeometry) {
  document.body.innerHTML = '<div style="color:#e0556a;padding:40px;font-family:sans-serif">Three.js failed to load.</div>';
  throw new Error('Three.js import failed');
}
if (!OrbitControls) {
  document.body.innerHTML = '<div style="color:#e0556a;padding:40px;font-family:sans-serif">OrbitControls failed to load.</div>';
  throw new Error('OrbitControls import failed');
}
// ═══════════════════════════════════════════════
// SECTION: Constants
// ═══════════════════════════════════════════════
const GRID_RES = 120;
const TERRAIN_SIZE = 80;
const MAX_HEIGHT = 22;
const PARTICLE_COUNT = 600;
const TARGET_FPS = 30;
const FRAME_BUDGET_MS = 1000 / TARGET_FPS;
const LOD_LEVELS = [GRID_RES, Math.floor(GRID_RES * 0.5), Math.floor(GRID_RES * 0.25)];
const LOD_DISTANCES = [30, 65, Infinity];
const BOOKMARK_COUNT = 4;
// ═══════════════════════════════════════════════
// SECTION: Synthetic time-series data generator
// ═══════════════════════════════════════════════
function generateDataMonths(count) {
  if (!count || count < 1) { count = 12; }
  const months = [];
  for (let i = 0; i < count; i++) {
    const t = i / (count - 1);
    const seasonal = Math.sin(t * Math.PI * 2) * 0.35;
    const trend = t * 0.5;
    const noise = (Math.random() - 0.5) * 0.15;
    const baseRevenue = 0.4 + trend + seasonal + noise;
    const revenue = Math.max(0.05, baseRevenue);
    const users = Math.max(0.05, revenue * (0.75 + Math.random() * 0.5));
    const errorRate = 0.02 + Math.random() * 0.12 + (t > 0.7 ? (t - 0.7) * 0.3 : 0);
    const apiCalls = Math.max(0.05, revenue * (1.2 + Math.random() * 0.8));
    months.push({ revenue, users, errorRate, apiCalls, index: i });
  }
  return months;
}
// ═══════════════════════════════════════════════
// SECTION: Heightfield from grid data
// ═══════════════════════════════════════════════
function heightAt(grid, x, z) {
  if (!grid || grid.length === 0) { return 0; }
  const rows = grid.length;
  const cols = grid[0] ? grid[0].length : 0;
  if (cols === 0) { return 0; }
  const fx = Math.max(0, Math.min(cols - 1, x));
  const fz = Math.max(0, Math.min(rows - 1, z));
  const ix = Math.floor(fx);
  const iz = Math.floor(fz);
  const nx = Math.min(ix + 1, cols - 1);
  const nz = Math.min(iz + 1, rows - 1);
  const dx = fx - ix;
  const dz = fz - iz;
  const h00 = (grid[iz] && grid[iz][ix] !== undefined) ? grid[iz][ix] : 0;
  const h10 = (grid[iz] && grid[iz][nx] !== undefined) ? grid[iz][nx] : 0;
  const h01 = (grid[nz] && grid[nz][ix] !== undefined) ? grid[nz][ix] : 0;
  const h11 = (grid[nz] && grid[nz][nx] !== undefined) ? grid[nz][nx] : 0;
  return (h00 * (1 - dx) + h10 * dx) * (1 - dz) + (h01 * (1 - dx) + h11 * dx) * dz;
}
// ═══════════════════════════════════════════════
// SECTION: Build height grid from month data
// ═══════════════════════════════════════════════
function buildHeightGrid(monthData, res) {
  if (!monthData) { return []; }
  const r = res || GRID_RES;
  const grid = [];
  for (let z = 0; z < r; z++) {
    const row = [];
    for (let x = 0; x < r; x++) {
      const cx = x / (r - 1) - 0.5;
      const cz = z / (r - 1) - 0.5;
      const dist = Math.sqrt(cx * cx + cz * cz) * 1.8;
      const gauss = Math.exp(-dist * dist * 3.5);
      const ridge = Math.abs(Math.sin(cx * 7 + cz * 3)) * 0.3;
      const valley = -Math.abs(Math.cos(cx * 5 - cz * 4)) * 0.2;
      const h = (gauss * monthData.revenue + ridge * 0.25 + valley * 0.15 + monthData.revenue * 0.1 * (Math.sin(cx * 9) * Math.cos(cz * 7))) * MAX_HEIGHT;
      row.push(h);
    }
    grid.push(row);
  }
  return grid;
}
// ═══════════════════════════════════════════════
// SECTION: Build color grid from secondary metric
// ═══════════════════════════════════════════════
function buildColorGrid(monthData, res) {
  if (!monthData) { return []; }
  const r = res || GRID_RES;
  const grid = [];
  for (let z = 0; z < r; z++) {
    const row = [];
    for (let x = 0; x < r; x++) {
      const cx = x / (r - 1) - 0.5;
      const cz = z / (r - 1) - 0.5;
      const dist = Math.sqrt(cx * cx + cz * cz);
      const noise = Math.sin(cx * 11 + cz * 8) * 0.2;
      const v = Math.max(0, Math.min(1, monthData.users * (1 - dist * 0.6) + noise));
      row.push(v);
    }
    grid.push(row);
  }
  return grid;
}
// ═══════════════════════════════════════════════
// SECTION: Vegetation color ramp
// ═══════════════════════════════════════════════
function vegetationColor(t) {
  const v = Math.max(0, Math.min(1, t));
  const r = 0.05 + v * 0.08;
  const g = 0.10 + v * 0.60;
  const b = 0.04 + v * 0.18;
  return new THREE.Color(r, g, b);
}
// ═══════════════════════════════════════════════
// SECTION: Build terrain mesh (BufferGeometry)
// ═══════════════════════════════════════════════
function buildTerrainMesh(heightGrid, colorGrid, res) {
  if (!heightGrid || heightGrid.length === 0) { return new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ color: 0x333333 })); }
  const r = res || GRID_RES;
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (r - 1);
  const vertCount = r * r;
  const positions = new Float32Array(vertCount * 3);
  const colors = new Float32Array(vertCount * 3);
  const indices = [];
  for (let z = 0; z < r; z++) {
    for (let x = 0; x < r; x++) {
      const i = z * r + x;
      const h = (heightGrid[z] && heightGrid[z][x] !== undefined) ? heightGrid[z][x] : 0;
      positions[i * 3] = x * step - half;
      positions[i * 3 + 1] = h;
      positions[i * 3 + 2] = z * step - half;
      const cv = (colorGrid[z] && colorGrid[z][x] !== undefined) ? colorGrid[z][x] : 0;
      const col = vegetationColor(cv);
      colors[i * 3] = col.r;
      colors[i * 3 + 1] = col.g;
      colors[i * 3 + 2] = col.b;
      if (z < r - 1 && x < r - 1) {
        const a = i;
        const b = i + 1;
        const c = i + r;
        const d = i + r + 1;
        indices.push(a, b, d);
        indices.push(a, d, c);
      }
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.08,
    flatShading: false,
    side: THREE.DoubleSide
  });
  return new THREE.Mesh(geo, mat);
}
// ═══════════════════════════════════════════════
// SECTION: Error river geometry builder
// ═══════════════════════════════════════════════
function buildRiverLines(heightGrid, errorRate, res) {
  if (!heightGrid || heightGrid.length === 0) {
    return new THREE.Group();
  }
  const group = new THREE.Group();
  const r = res || GRID_RES;
  const half = TERRAIN_SIZE / 2;
  const step = TERRAIN_SIZE / (r - 1);
  const pathCount = Math.floor(errorRate * 18) + 2;
  for (let p = 0; p < pathCount; p++) {
    const points = [];
    const startX = Math.floor(r * 0.1 + Math.random() * r * 0.8);
    const startZ = Math.floor(r * 0.1 + Math.random() * r * 0.8);
    let cx = startX;
    let cz = startZ;
    const segments = 40 + Math.floor(Math.random() * 50);
    for (let s = 0; s < segments; s++) {
      const h = heightAt(heightGrid, cx, cz);
      const wx = cx / r - 0.5;
      const wz = cz / r - 0.5;
      const gradX = -(wx) * 4;
      const gradZ = -(wz) * 4;
      cx += gradX * 0.6 + (Math.random() - 0.5) * 2.5;
      cz += gradZ * 0.6 + (Math.random() - 0.5) * 2.5;
      cx = Math.max(0, Math.min(r - 1, cx));
      cz = Math.max(0, Math.min(r - 1, cz));
      const px = cx * step - half;
      const pz = cz * step - half;
      const py = heightAt(heightGrid, cx, cz) + 0.18;
      points.push(new THREE.Vector3(px, py, pz));
      if (points.length >= 2 && Math.random() < 0.12) { break; }
    }
    if (points.length < 2) { continue; }
    const curve = new THREE.CatmullRomCurve3(points);
    const tubePoints = curve.getPoints(points.length * 2);
    const geo = new THREE.BufferGeometry().setFromPoints(tubePoints);
    const intensity = 0.5 + Math.random() * 0.5;
    const mat = new THREE.LineBasicMaterial({
      color: new THREE.Color(0.9, 0.08 + intensity * 0.15, 0.12),
      linewidth: 1,
      transparent: true,
      opacity: 0.7 + errorRate * 0.3
    });
    const line = new THREE.Line(geo, mat);
    line.renderOrder = 1;
    line.material.depthTest = true;
    line.material.depthWrite = false;
    group.add(line);
  }
  return group;
}
// ═══════════════════════════════════════════════
// SECTION: Particle system (data flow trails)
// ═══════════════════════════════════════════════
function buildParticleSystem(count) {
  const c = count || PARTICLE_COUNT;
  const positions = new Float32Array(c * 3);
  const velBuffer = new Float32Array(c * 3);
  const lifeBuffer = new Float32Array(c);
  for (let i = 0; i < c; i++) {
    positions[i * 3] = (Math.random() - 0.5) * TERRAIN_SIZE * 0.9;
    positions[i * 3 + 1] = MAX_HEIGHT * 0.5;
    positions[i * 3 + 2] = (Math.random() - 0.5) * TERRAIN_SIZE * 0.9;
    velBuffer[i * 3] = (Math.random() - 0.5) * 3;
    velBuffer[i * 3 + 1] = -1 - Math.random() * 2;
    velBuffer[i * 3 + 2] = (Math.random() - 0.5) * 3;
    lifeBuffer[i] = Math.random();
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const mat = new THREE.PointsMaterial({
    color: 0x5b9cf5,
    size: 0.28,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    transparent: true,
    opacity: 0.7
  });
  const points = new THREE.Points(geo, mat);
  points.renderOrder = 2;
  points.userData = { velBuffer, lifeBuffer, heightGrid: null, spatialGrid: null, spatialCellSize: 0 };
  return points;
}
// ═══════════════════════════════════════════════
// SECTION: Spatial index (uniform grid for O(1) height lookup)
// ═══════════════════════════════════════════════
function buildSpatialIndex(heightGrid, res) {
  if (!heightGrid || heightGrid.length === 0) { return null; }
  const r = res || GRID_RES;
  const cellSize = TERRAIN_SIZE / (r - 1);
  const half = TERRAIN_SIZE / 2;
  return {
    cellSize,
    half,
    r,
    grid: heightGrid,
    query(wx, wz) {
      if (!this.grid || this.grid.length === 0) { return 0; }
      const gx = (wx + half) / cellSize;
      const gz = (wz + half) / cellSize;
      return heightAt(this.grid, gx, gz);
    }
  };
}
// ═══════════════════════════════════════════════
// SECTION: View-frustum AABB check
// ═══════════════════════════════════════════════
function isInFrustum(camera, minX, minZ, maxX, maxZ, margin) {
  if (!camera || !camera.matrixWorldInverse || !camera.projectionMatrix) { return true; }
  const m = margin || 5;
  const corners = [
    new THREE.Vector3(minX - m, 0, minZ - m),
    new THREE.Vector3(minX - m, 0, maxZ + m),
    new THREE.Vector3(maxX + m, 0, minZ - m),
    new THREE.Vector3(maxX + m, 0, maxZ + m),
    new THREE.Vector3(minX - m, MAX_HEIGHT, minZ - m),
    new THREE.Vector3(minX - m, MAX_HEIGHT, maxZ + m),
    new THREE.Vector3(maxX + m, MAX_HEIGHT, minZ - m),
    new THREE.Vector3(maxX + m, MAX_HEIGHT, maxZ + m)
  ];
  const frustum = new THREE.Frustum();
  try {
    frustum.setFromProjectionMatrix(new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse));
  } catch (e) {
    return true;
  }
  return corners.some(c => frustum.containsPoint(c));
}
// ═══════════════════════════════════════════════
// SECTION: Tri-planar grid floor
// ═══════════════════════════════════════════════
function buildGridFloor() {
  const size = TERRAIN_SIZE * 1.3;
  const divisions = 40;
  const step = size / divisions;
  const half = size / 2;
  const positions = [];
  for (let i = 0; i <= divisions; i++) {
    const offset = -half + i * step;
    positions.push(offset, -0.4, -half);
    positions.push(offset, -0.4, half);
    positions.push(-half, -0.4, offset);
    positions.push(half, -0.4, offset);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(positions), 3));
  const mat = new THREE.LineBasicMaterial({ color: 0x1a1a2e, transparent: true, opacity: 0.4 });
  return new THREE.LineSegments(geo, mat);
}
// ═══════════════════════════════════════════════
// SECTION: Scene setup
// ═══════════════════════════════════════════════
const container = document.getElementById('canvas-container');
if (!container) { throw new Error('Container element not found'); }
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x080c14);
scene.fog = new THREE.FogExp2(0x080c14, 0.00018);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 300);
camera.position.set(28, 32, 42);
camera.lookAt(0, 4, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
// ═══════════════════════════════════════════════
// SECTION: OrbitControls
// ═══════════════════════════════════════════════
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 5, 0);
controls.minDistance = 10;
controls.maxDistance = 120;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// ═══════════════════════════════════════════════
// SECTION: Lighting
// ═══════════════════════════════════════════════
const ambientLight = new THREE.AmbientLight(0x1a1a3a, 1.0);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 2.8);
sunLight.position.set(35, 50, 20);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 1024;
sunLight.shadow.mapSize.height = 1024;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 200;
sunLight.shadow.camera.left = -60;
sunLight.shadow.camera.right = 60;
sunLight.shadow.camera.top = 60;
sunLight.shadow.camera.bottom = -60;
sunLight.shadow.bias = -0.0004;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x334466, 0.8);
fillLight.position.set(-20, 15, -15);
scene.add(fillLight);
// ═══════════════════════════════════════════════
// SECTION: Scene objects (managed)
// ═══════════════════════════════════════════════
const gridFloor = buildGridFloor();
scene.add(gridFloor);
const waterPlaneGeo = new THREE.PlaneGeometry(TERRAIN_SIZE * 1.3, TERRAIN_SIZE * 1.3);
const waterPlaneMat = new THREE.MeshStandardMaterial({
  color: 0x101830,
  roughness: 0.5,
  metalness: 0.3,
  transparent: true,
  opacity: 0.5,
  side: THREE.DoubleSide
});
const waterPlane = new THREE.Mesh(waterPlaneGeo, waterPlaneMat);
waterPlane.rotation.x = -Math.PI / 2;
waterPlane.position.y = -0.35;
waterPlane.renderOrder = 0;
scene.add(waterPlane);
// ═══════════════════════════════════════════════
// SECTION: Geometry cache (buffer swap)
// ═══════════════════════════════════════════════
const geometryCache = new Map();
let activeTerrainMesh = null;
let activeRiverGroup = null;
function cacheKey(monthIndex, res) {
  return `m${monthIndex}_r${res}`;
}
function getOrBuildTerrain(monthData, monthIndex) {
  const key = cacheKey(monthIndex, GRID_RES);
  if (geometryCache.has(key)) {
    return geometryCache.get(key);
  }
  const hGrid = buildHeightGrid(monthData, GRID_RES);
  const cGrid = buildColorGrid(monthData, GRID_RES);
  const mesh = buildTerrainMesh(hGrid, cGrid, GRID_RES);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  const rivers = buildRiverLines(hGrid, monthData.errorRate, GRID_RES);
  const spatial = buildSpatialIndex(hGrid, GRID_RES);
  const entry = { mesh, rivers, heightGrid: hGrid, spatial };
  geometryCache.set(key, entry);
  return entry;
}
// ═══════════════════════════════════════════════
// SECTION: Cache eviction (keep max 8 entries)
// ═══════════════════════════════════════════════
function evictCache(maxEntries) {
  const max = maxEntries || 8;
  if (geometryCache.size <= max) { return; }
  const keys = Array.from(geometryCache.keys());
  const toRemove = keys.slice(0, keys.length - max);
  for (const k of toRemove) {
    const entry = geometryCache.get(k);
    if (entry) {
      if (entry.mesh && entry.mesh.geometry) { entry.mesh.geometry.dispose(); }
      if (entry.mesh && entry.mesh.material) { entry.mesh.material.dispose(); }
      if (entry.rivers && entry.rivers.traverse) {
        entry.rivers.traverse(child => {
          if (child.geometry) { child.geometry.dispose(); }
          if (child.material) { child.material.dispose(); }
        });
      }
    }
    geometryCache.delete(k);
  }
}
// ═══════════════════════════════════════════════
// SECTION: Apply terrain to scene (swap buffers)
// ═══════════════════════════════════════════════
function applyTerrain(entry) {
  if (!entry) { return; }
  if (activeTerrainMesh) { scene.remove(activeTerrainMesh); }
  if (activeRiverGroup) { scene.remove(activeRiverGroup); }
  activeTerrainMesh = entry.mesh;
  activeRiverGroup = entry.rivers;
  scene.add(activeTerrainMesh);
  scene.add(activeRiverGroup);
  if (particleSystem && entry.spatial) {
    particleSystem.userData.spatialIndex = entry.spatial;
    particleSystem.userData.heightGrid = entry.heightGrid;
  }
}
// ═══════════════════════════════════════════════
// SECTION: Particle system
// ═══════════════════════════════════════════════
const particleSystem = buildParticleSystem(PARTICLE_COUNT);
scene.add(particleSystem);
// ═══════════════════════════════════════════════
// SECTION: Update particles (reuse buffers, spatial query)
// ═══════════════════════════════════════════════
function updateParticles(dt, apiMultiplier) {
  if (!particleSystem) { return; }
  const geo = particleSystem.geometry;
  if (!geo || !geo.attributes || !geo.attributes.position) { return; }
  const pos = geo.attributes.position.array;
  const vel = particleSystem.userData.velBuffer;
  const life = particleSystem.userData.lifeBuffer;
  const spatial = particleSystem.userData.spatialIndex;
  const hGrid = particleSystem.userData.heightGrid;
  const half = TERRAIN_SIZE / 2;
  const count = pos.length / 3;
  const speed = 3 + (apiMultiplier || 1) * 6;
  const dtClamped = Math.min(dt, 0.1);
  for (let i = 0; i < count; i++) {
    const i3 = i * 3;
    life[i] += dtClamped * 0.8;
    if (life[i] > 1.0) {
      pos[i3] = (Math.random() - 0.5) * TERRAIN_SIZE * 0.9;
      pos[i3 + 1] = MAX_HEIGHT * 1.2;
      pos[i3 + 2] = (Math.random() - 0.5) * TERRAIN_SIZE * 0.9;
      vel[i3] = (Math.random() - 0.5) * 2;
      vel[i3 + 1] = -1 - Math.random() * 4;
      vel[i3 + 2] = (Math.random() - 0.5) * 2;
      life[i] = 0;
    }
    pos[i3] += vel[i3] * speed * dtClamped;
    pos[i3 + 1] += vel[i3 + 1] * speed * dtClamped;
    pos[i3 + 2] += vel[i3 + 2] * speed * dtClamped;
    if (pos[i3] < -half || pos[i3] > half || pos[i3 + 2] < -half || pos[i3 + 2] > half) {
      life[i] = 1.0;
      continue;
    }
    let terrainH = 0;
    if (spatial && typeof spatial.query === 'function') {
      terrainH = spatial.query(pos[i3], pos[i3 + 2]);
    } else if (hGrid && hGrid.length > 0) {
      const gx = (pos[i3] + half) / TERRAIN_SIZE * (GRID_RES - 1);
      const gz = (pos[i3 + 2] + half) / TERRAIN_SIZE * (GRID_RES - 1);
      terrainH = heightAt(hGrid, gx, gz);
    }
    if (pos[i3 + 1] < terrainH + 0.15) {
      pos[i3 + 1] = terrainH + 0.15;
      vel[i3 + 1] = Math.abs(vel[i3 + 1]) * 0.4;
    }
    if (pos[i3 + 1] < -5) { life[i] = 1.0; }
  }
  geo.attributes.position.needsUpdate = true;
}
// ═══════════════════════════════════════════════
// SECTION: LOD selection (distance-based)
// ═══════════════════════════════════════════════
function selectLOD() {
  if (!camera) { return 0; }
  const dist = camera.position.distanceTo(controls.target);
  for (let i = 0; i < LOD_DISTANCES.length; i++) {
    if (dist < LOD_DISTANCES[i]) { return i; }
  }
  return LOD_LEVELS.length - 1;
}
// ═══════════════════════════════════════════════
// SECTION: Bookmarks
// ═══════════════════════════════════════════════
const bookmarks = [];
for (let i = 0; i < BOOKMARK_COUNT; i++) {
  bookmarks.push({ position: null, target: null });
}
function saveBookmark(slot) {
  if (slot < 0 || slot >= BOOKMARK_COUNT) { return; }
  if (!camera || !controls) { return; }
  bookmarks[slot] = {
    position: camera.position.clone(),
    target: controls.target.clone()
  };
  updateBookmarkButtons();
}
function recallBookmark(slot) {
  if (slot < 0 || slot >= BOOKMARK_COUNT) { return; }
  const bm = bookmarks[slot];
  if (!bm || !bm.position) { return; }
  if (!camera || !controls) { return; }
  camera.position.copy(bm.position);
  controls.target.copy(bm.target);
  controls.update();
}
function updateBookmarkButtons() {
  const bar = document.getElementById('bookmark-bar');
  if (!bar) { return; }
  bar.innerHTML = '';
  for (let i = 0; i < BOOKMARK_COUNT; i++) {
    const btn = document.createElement('button');
    btn.className = 'bookmark-btn' + (bookmarks[i] && bookmarks[i].position ? ' saved' : '');
    btn.textContent = 'Slot ' + (i + 1) + (bookmarks[i] && bookmarks[i].position ? ' \u2714' : '');
    btn.addEventListener('click', () => {
      if (bookmarks[i] && bookmarks[i].position) {
        recallBookmark(i);
      } else {
        saveBookmark(i);
      }
    });
    bar.appendChild(btn);
  }
}
// ═══════════════════════════════════════════════
// SECTION: Data and state
// ═══════════════════════════════════════════════
const allMonths = generateDataMonths(12);
let currentMonthIndex = 0;
let lastFrameTime = performance.now();
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
if (timeSlider) {
  timeSlider.max = allMonths.length - 1;
  timeSlider.addEventListener('input', () => {
    currentMonthIndex = parseInt(timeSlider.value, 10);
    if (timeLabel) {
      timeLabel.textContent = 'Month ' + (currentMonthIndex + 1);
    }
    const entry = getOrBuildTerrain(allMonths[currentMonthIndex], currentMonthIndex);
    applyTerrain(entry);
    updatePanelValues(allMonths[currentMonthIndex]);
  });
}
// ═══════════════════════════════════════════════
// SECTION: Panel value update
// ═══════════════════════════════════════════════
function updatePanelValues(data) {
  if (!data) { return; }
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) { el.textContent = val; }
  };
  setVal('val-revenue', '$' + (data.revenue * 1000).toFixed(0) + 'K');
  setVal('val-users', (data.users * 100).toFixed(0) + 'K');
  setVal('val-errors', Math.floor(data.errorRate * 500));
  setVal('val-api', Math.floor(data.apiCalls * 200));
}
// ═══════════════════════════════════════════════
// SECTION: Keyboard controls
// ═══════════════════════════════════════════════
window.addEventListener('keydown', (e) => {
  const key = e.key.toLowerCase();
  if (key === 'a' && controls) {
    controls.autoRotate = !controls.autoRotate;
  }
  if (key === 'b') {
    saveBookmark(0);
    for (let s = 1; s < BOOKMARK_COUNT; s++) {
      if (!bookmarks[s] || !bookmarks[s].position) {
        saveBookmark(s);
        break;
      }
    }
  }
  const slotMap = { '1': 0, '2': 1, '3': 2, '4': 3 };
  if (slotMap[key] !== undefined) {
    recallBookmark(slotMap[key]);
  }
  if (key === 'arrowleft' && timeSlider) {
    timeSlider.value = Math.max(0, currentMonthIndex - 1);
    timeSlider.dispatchEvent(new Event('input'));
  }
  if (key === 'arrowright' && timeSlider) {
    timeSlider.value = Math.min(allMonths.length - 1, currentMonthIndex + 1);
    timeSlider.dispatchEvent(new Event('input'));
  }
});
// ═══════════════════════════════════════════════
// SECTION: Resize handler
// ═══════════════════════════════════════════════
window.addEventListener('resize', () => {
  if (!camera || !renderer) { return; }
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ═══════════════════════════════════════════════
// SECTION: Render loop
// ═══════════════════════════════════════════════
function animate(timestamp) {
  requestAnimationFrame(animate);
  const now = timestamp || performance.now();
  let dt = (now - lastFrameTime) / 1000;
  lastFrameTime = now;
  if (dt <= 0 || dt > 0.5) { dt = 0.016; }
  if (controls) { controls.update(); }
  const lodLevel = selectLOD();
  if (activeTerrainMesh && activeTerrainMesh.geometry) {
    const frustumVisible = isInFrustum(camera, -TERRAIN_SIZE / 2, -TERRAIN_SIZE / 2, TERRAIN_SIZE / 2, TERRAIN_SIZE / 2, 2);
    activeTerrainMesh.visible = frustumVisible;
    if (activeRiverGroup) { activeRiverGroup.visible = frustumVisible; }
  }
  const currentData = allMonths[currentMonthIndex];
  updateParticles(dt, currentData ? currentData.apiCalls : 1);
  if (renderer && scene && camera) {
    renderer.render(scene, camera);
  }
}
// ═══════════════════════════════════════════════
// SECTION: Initialization
// ═══════════════════════════════════════════════
function init() {
  try {
    const entry = getOrBuildTerrain(allMonths[0], 0);
    applyTerrain(entry);
    updatePanelValues(allMonths[0]);
    updateBookmarkButtons();
    for (let i = 1; i < Math.min(3, allMonths.length); i++) {
      getOrBuildTerrain(allMonths[i], i);
    }
    evictCache(8);
    requestAnimationFrame(animate);
  } catch (err) {
    console.error('Init failed:', err);
    container.innerHTML = '<div style="color:#e0556a;padding:40px;font-family:sans-serif">Initialization failed: ' + (err.message || 'unknown error') + '</div>';
  }
}
init();
</script>
</body>
</html>