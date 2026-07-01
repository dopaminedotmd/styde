<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; }
  #canvas-container { position: fixed; inset: 0; }
  #ui-overlay { position: fixed; bottom: 0; left: 0; right: 0; pointer-events: none; z-index: 10; }
  #ui-overlay > * { pointer-events: auto; }
  #time-panel {
    position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%);
    background: rgba(10,10,25,0.85); backdrop-filter: blur(12px);
    border: 1px solid rgba(100,140,255,0.3); border-radius: 12px;
    padding: 14px 24px; display: flex; align-items: center; gap: 16px;
    color: #c8d6f8; font-size: 13px; min-width: 420px;
  }
  #time-slider { flex: 1; accent-color: #5b8def; height: 6px; cursor: pointer; }
  #time-label { white-space: nowrap; min-width: 100px; text-align: center; font-variant-numeric: tabular-nums; }
  #bookmark-bar {
    position: absolute; top: 16px; right: 16px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .bookmark-btn {
    background: rgba(10,10,25,0.8); backdrop-filter: blur(8px);
    border: 1px solid rgba(100,140,255,0.25); border-radius: 8px;
    color: #8aa8f0; padding: 8px 14px; font-size: 12px; cursor: pointer;
    transition: all 0.2s; text-align: left;
  }
  .bookmark-btn:hover { background: rgba(60,90,180,0.4); border-color: rgba(120,160,255,0.6); color: #fff; }
  .bookmark-btn.active { background: rgba(70,110,220,0.5); border-color: #5b8def; color: #fff; }
  #diag-panel {
    position: absolute; top: 16px; left: 16px;
    background: rgba(10,10,25,0.8); backdrop-filter: blur(8px);
    border: 1px solid rgba(100,140,255,0.2); border-radius: 8px;
    padding: 10px 14px; color: #7a9ec8; font-size: 11px; font-family: 'Consolas', monospace;
    line-height: 1.6; min-width: 200px;
  }
  #diag-panel .hit { color: #4ec97a; }
  #diag-panel .miss { color: #e0556a; }
  #diag-panel .warn { color: #e0a055; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-overlay">
  <div id="diag-panel"></div>
  <div id="bookmark-bar"></div>
  <div id="time-panel">
    <span style="opacity:0.7;">TIME</span>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label">Day 1</span>
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
// ─── Cache Manager ───────────────────────────────────────────────────
// Tracks hit/miss for all cached resources; exposes stats to diagnostic panel
class CacheManager {
  constructor() {
    this.stores = new Map();
    this.stats = { hits: 0, misses: 0 };
  }
  store(name) {
    if (!this.stores.has(name)) {
      this.stores.set(name, new Map());
    }
    return this.stores.get(name);
  }
  get(name, key) {
    const s = this.stores.get(name);
    if (s && s.has(key)) { this.stats.hits++; return s.get(key); }
    this.stats.misses++;
    return undefined;
  }
  set(name, key, value) {
    this.store(name).set(key, value);
  }
  clear(name) {
    if (name) { this.stores.get(name)?.clear(); }
    else { for (const s of this.stores.values()) s.clear(); }
  }
  report() {
    const total = this.stats.hits + this.stats.misses || 1;
    return { hits: this.stats.hits, misses: this.stats.misses, rate: (this.stats.hits / total * 100).toFixed(1) };
  }
}
const cache = new CacheManager();
// ─── Data Generator ──────────────────────────────────────────────────
// Produces 100-day mock time-series: revenue (height), users (color), errors (rivers), apiCalls (particles)
function generateTimeSeries(days = 100) {
  const seed = 42;
  function pseudo(ix) {
    let x = Math.sin(ix * 12.9898 + seed) * 43758.5453;
    return x - Math.floor(x);
  }
  const data = [];
  for (let d = 0; d < days; d++) {
    const trend = 0.3 + (d / days) * 0.7;
    const seasonal = Math.sin(d * 0.18) * 0.2 + Math.sin(d * 0.05) * 0.3;
    const noise = (pseudo(d * 3) - 0.5) * 0.15;
    const revenue = Math.max(0.05, trend + seasonal + noise);
    const userDensity = 0.2 + revenue * 0.7 + (pseudo(d * 7 + 1) - 0.5) * 0.25;
    const errorBase = 0.01 + (1 - revenue) * 0.08;
    const errorSpike = (pseudo(d * 13 + 2) > 0.92) ? pseudo(d * 17) * 0.15 : 0;
    const errorRate = Math.min(0.3, errorBase + errorSpike);
    const apiVolume = 200 + revenue * 800 + (pseudo(d * 11 + 3) - 0.5) * 300;
    data.push({ day: d + 1, revenue, userDensity, errorRate, apiVolume, seasonal, trend });
  }
  return data;
}
const timeSeries = generateTimeSeries(100);
// ─── Terrain Builder ─────────────────────────────────────────────────
// Builds heightfield BufferGeometry from data slice; caches by time index
const TERRAIN_RES = 128;
const TERRAIN_SIZE = 20;
function buildTerrainGeometry(timeIndex) {
  const cached = cache.get('terrain', timeIndex);
  if (cached) return cached;
  const segments = TERRAIN_RES;
  const half = TERRAIN_SIZE / 2;
  const vertices = new Float32Array((segments + 1) * (segments + 1) * 3);
  const colors = new Float32Array((segments + 1) * (segments + 1) * 3);
  // Sample a window of 3 days centered on timeIndex for smooth terrain
  const windowSize = 3;
  const halfWin = Math.floor(windowSize / 2);
  for (let iz = 0; iz <= segments; iz++) {
    for (let ix = 0; ix <= segments; ix++) {
      const idx3 = (iz * (segments + 1) + ix) * 3;
      const x = (ix / segments - 0.5) * TERRAIN_SIZE;
      const z = (iz / segments - 0.5) * TERRAIN_SIZE;
      // Smooth height by blending neighboring time slices
      let height = 0;
      let userSum = 0;
      let weightSum = 0;
      for (let w = -halfWin; w <= halfWin; w++) {
        const ti = Math.max(0, Math.min(timeSeries.length - 1, timeIndex + w));
        const weight = 1 - Math.abs(w) / (halfWin + 1);
        height += timeSeries[ti].revenue * weight;
        userSum += timeSeries[ti].userDensity * weight;
        weightSum += weight;
      }
      height /= weightSum;
      userSum /= weightSum;
      vertices[idx3] = x;
      vertices[idx3 + 1] = height * 8;
      vertices[idx3 + 2] = z;
      // Vegetation gradient: low=blue, mid=green, high=yellow
      const u = Math.max(0, Math.min(1, userSum));
      const r = u * 0.9;
      const g = 0.15 + u * 0.7;
      const b = 0.5 * (1 - u);
      colors[idx3] = r;
      colors[idx3 + 1] = g;
      colors[idx3 + 2] = b;
    }
  }
  const indices = [];
  for (let iz = 0; iz < segments; iz++) {
    for (let ix = 0; ix < segments; ix++) {
      const a = iz * (segments + 1) + ix;
      const b = a + 1;
      const c = a + (segments + 1);
      const d = c + 1;
      indices.push(a, b, d, a, d, c);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  cache.set('terrain', timeIndex, geo);
  return geo;
}
// ─── River Builder ───────────────────────────────────────────────────
// Traces error anomaly paths as river geometry; debounced rebuild, caches TubeBufferGeometry
let riverGroup = null;
let riverRebuildTimeout = null;
const RIVER_DEBOUNCE_MS = 200;
function buildRiverGeometry(timeIndex) {
  const cached = cache.get('river', timeIndex);
  if (cached) return cached.clone();
  const points = [];
  const stepX = TERRAIN_SIZE / 16;
  for (let i = 0; i <= 16; i++) {
    const x = -TERRAIN_SIZE / 2 + i * stepX;
    const dataIx = Math.floor((i / 16) * (timeSeries.length - 1));
    const ti = Math.max(0, Math.min(timeSeries.length - 1, timeIndex + Math.floor((i - 8) * 0.4)));
    const d = timeSeries[ti];
    const z = (d.errorRate - 0.05) * TERRAIN_SIZE * 0.8;
    const y = d.revenue * 8 + 0.15;
    points.push(new THREE.Vector3(x, y, z));
  }
  const curve = new THREE.CatmullRomCurve3(points);
  const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.12, 8, false);
  cache.set('river', timeIndex, tubeGeo);
  return tubeGeo.clone();
}
function scheduleRiverRebuild(timeIndex, scene) {
  if (riverRebuildTimeout) clearTimeout(riverRebuildTimeout);
  riverRebuildTimeout = setTimeout(() => {
    rebuildRiverNow(timeIndex, scene);
    riverRebuildTimeout = null;
  }, RIVER_DEBOUNCE_MS);
}
function rebuildRiverNow(timeIndex, scene) {
  if (riverGroup) {
    scene.remove(riverGroup);
    disposeGroup(riverGroup);
  }
  riverGroup = new THREE.Group();
  const geo = buildRiverGeometry(timeIndex);
  const mat = new THREE.MeshStandardMaterial({
    color: 0xe04040, emissive: 0x801010, roughness: 0.3, metalness: 0.1
  });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.renderOrder = 2;
  mesh.material.depthTest = true;
  mesh.material.depthWrite = true;
  riverGroup.add(mesh);
  // Glow outline via slightly scaled wireframe
  const wireGeo = buildRiverGeometry(timeIndex);
  const wireMat = new THREE.MeshBasicMaterial({ color: 0xff6060, wireframe: true, transparent: true, opacity: 0.25 });
  const wireMesh = new THREE.Mesh(wireGeo, wireMat);
  wireMesh.scale.set(1.08, 1.08, 1.08);
  wireMesh.renderOrder = 1;
  riverGroup.add(wireMesh);
  scene.add(riverGroup);
}
function disposeGroup(group) {
  group.traverse(child => {
    if (child.geometry) child.geometry.dispose();
    if (child.material) {
      if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
      else child.material.dispose();
    }
  });
}
// ─── Particle System ─────────────────────────────────────────────────
// Renders data-flow trails with frame-budget awareness (yields every 8ms)
class ParticleFlow {
  constructor(scene, maxParticles = 3000) {
    this.scene = scene;
    this.maxParticles = maxParticles;
    const positions = new Float32Array(maxParticles * 3);
    const colors = new Float32Array(maxParticles * 3);
    const sizes = new Float32Array(maxParticles);
    // Pre-fill position array; reuse every frame, never re-allocate
    this.posArray = positions;
    this.colorArray = colors;
    this.sizeArray = sizes;
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));
    const mat = new THREE.PointsMaterial({
      size: 0.08, vertexColors: true, blending: THREE.AdditiveBlending,
      depthWrite: false, transparent: true, opacity: 0.8
    });
    this.points = new THREE.Points(geo, mat);
    this.points.renderOrder = 3;
    scene.add(this.points);
    this.particleData = [];
    this.geo = geo;
    this.budgetPerFrame = 8;
    this.activeCount = 0;
  }
  // Spawn a trail flowing along the terrain surface
  spawnTrail(startX, startZ, timeIndex) {
    if (this.particleData.length >= this.maxParticles) return;
    const ti = Math.min(timeSeries.length - 1, timeIndex);
    const y = timeSeries[ti].revenue * 8 + 0.3;
    this.particleData.push({
      x: startX, z: startZ, y: y,
      vx: (Math.random() - 0.5) * 0.08,
      vz: (Math.random() - 0.5) * 0.08,
      life: 1.0, decay: 0.003 + Math.random() * 0.006
    });
  }
  update(deltaMs, timeIndex) {
    const startTime = performance.now();
    this.activeCount = 0;
    // Reuse position/color/size arrays from construction — zero allocations
    const pos = this.posArray;
    const col = this.colorArray;
    const siz = this.sizeArray;
    // Spawn new particles based on API volume for current time slice
    const ti = Math.min(timeSeries.length - 1, timeIndex);
    const apiVol = timeSeries[ti].apiVolume;
    const spawnCount = Math.floor(apiVol / 80);
    for (let i = 0; i < spawnCount && this.particleData.length < this.maxParticles; i++) {
      const sx = (Math.random() - 0.5) * TERRAIN_SIZE;
      const sz = (Math.random() - 0.5) * TERRAIN_SIZE;
      this.spawnTrail(sx, sz, timeIndex);
    }
    // Update particles with frame-budget awareness
    for (let i = this.particleData.length - 1; i >= 0; i--) {
      // Yield every 8ms to stay under 16ms frame budget
      if (i % 40 === 0 && performance.now() - startTime > this.budgetPerFrame) break;
      const p = this.particleData[i];
      p.life -= p.decay * (deltaMs / 16);
      if (p.life <= 0) {
        this.particleData.splice(i, 1);
        continue;
      }
      p.x += p.vx * (deltaMs / 16);
      p.z += p.vz * (deltaMs / 16);
      // Clamp to terrain bounds
      p.x = Math.max(-TERRAIN_SIZE / 2, Math.min(TERRAIN_SIZE / 2, p.x));
      p.z = Math.max(-TERRAIN_SIZE / 2, Math.min(TERRAIN_SIZE / 2, p.z));
      // Terrain-following: sample height at current position
      const gx = Math.floor((p.x / TERRAIN_SIZE + 0.5) * TERRAIN_RES);
      const gz = Math.floor((p.z / TERRAIN_SIZE + 0.5) * TERRAIN_RES);
      const gi = Math.max(0, Math.min(timeSeries.length - 1, timeIndex));
      const h = timeSeries[gi].revenue * 8;
      p.y = h + 0.2 + p.life * 0.5;
    }
    const count = Math.min(this.particleData.length, this.maxParticles);
    this.activeCount = count;
    for (let i = 0; i < count; i++) {
      const p = this.particleData[i];
      const i3 = i * 3;
      pos[i3] = p.x;
      pos[i3 + 1] = p.y;
      pos[i3 + 2] = p.z;
      // Color: cyan trails that fade to blue as they age
      const alpha = p.life;
      col[i3] = 0.2 * alpha;
      col[i3 + 1] = 0.7 * alpha;
      col[i3 + 2] = 1.0 * alpha;
      siz[i] = 0.04 + alpha * 0.06;
    }
    // Zero out unused slots so dead particles don't render
    for (let i = count; i < this.maxParticles; i++) {
      const i3 = i * 3;
      pos[i3] = pos[i3 + 1] = pos[i3 + 2] = 0;
      col[i3] = col[i3 + 1] = col[i3 + 2] = 0;
      siz[i] = 0;
    }
    this.geo.attributes.position.needsUpdate = true;
    this.geo.attributes.color.needsUpdate = true;
    this.geo.attributes.size.needsUpdate = true;
    this.geo.setDrawRange(0, count);
  }
  dispose() {
    this.scene.remove(this.points);
    this.geo.dispose();
    this.points.material.dispose();
  }
}
// ─── Bookmark Manager ────────────────────────────────────────────────
// Persists camera bookmarks to localStorage on every camera-move-end
const BOOKMARK_KEY = 'terrain_explorer_bookmarks';
class BookmarkManager {
  constructor(controls, camera) {
    this.controls = controls;
    this.camera = camera;
    this.bookmarks = this.load();
    this.onChangeCallback = null;
  }
  load() {
    try {
      const raw = localStorage.getItem(BOOKMARK_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch { return []; }
  }
  save() {
    try {
      localStorage.setItem(BOOKMARK_KEY, JSON.stringify(this.bookmarks));
    } catch { /* quota exceeded — silently ignore */ }
  }
  add(name) {
    const pos = this.camera.position.clone();
    const target = this.controls.target.clone();
    this.bookmarks.push({ name, pos: pos.toArray(), target: target.toArray() });
    this.save();
    if (this.onChangeCallback) this.onChangeCallback();
  }
  remove(index) {
    this.bookmarks.splice(index, 1);
    this.save();
    if (this.onChangeCallback) this.onChangeCallback();
  }
  apply(index) {
    const bm = this.bookmarks[index];
    if (!bm) return;
    this.camera.position.set(bm.pos[0], bm.pos[1], bm.pos[2]);
    this.controls.target.set(bm.target[0], bm.target[1], bm.target[2]);
    this.controls.update();
  }
  syncFromCamera() {
    // Called on every camera-move-end to keep bookmarks current
    // Only updates if a bookmark is "active" (close match), otherwise no-op
    const pos = this.camera.position;
    const tgt = this.controls.target;
    const threshold = 1.5;
    for (const bm of this.bookmarks) {
      const dx = pos.x - bm.pos[0];
      const dy = pos.y - bm.pos[1];
      const dz = pos.z - bm.pos[2];
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      if (dist < threshold) {
        bm.pos = [pos.x, pos.y, pos.z];
        bm.target = [tgt.x, tgt.y, tgt.z];
        this.save();
        return;
      }
    }
  }
  onChange(fn) { this.onChangeCallback = fn; }
}
// ─── World-to-Grid Memoization ───────────────────────────────────────
// Memoizes grid coordinate transforms; cleared each frame
let memoFrameId = -1;
const worldToGridMemo = new Map();
function worldToGrid(wx, wz, frameId) {
  if (frameId !== memoFrameId) {
    worldToGridMemo.clear();
    memoFrameId = frameId;
  }
  const key = `${wx.toFixed(3)},${wz.toFixed(3)}`;
  if (worldToGridMemo.has(key)) return worldToGridMemo.get(key);
  const gx = Math.floor((wx / TERRAIN_SIZE + 0.5) * TERRAIN_RES);
  const gz = Math.floor((wz / TERRAIN_SIZE + 0.5) * TERRAIN_RES);
  const result = { gx, gz };
  worldToGridMemo.set(key, result);
  return result;
}
// ─── Diagnostic Panel ────────────────────────────────────────────────
function updateDiagnosticPanel(particleFlow, timeIndex, frameTime) {
  const r = cache.report();
  const el = document.getElementById('diag-panel');
  if (!el) return;
  el.innerHTML =
    `Cache: <span class="hit">${r.hits}h</span> / <span class="miss">${r.misses}m</span> (${r.rate}%)` +
    ` | Particles: ${particleFlow.activeCount}` +
    ` | Frame: ${frameTime.toFixed(1)}ms` +
    (frameTime > 14 ? ` <span class="warn">!</span>` : '');
}
// ─── UI Setup ────────────────────────────────────────────────────────
function buildBookmarkUI(bookmarkManager) {
  const bar = document.getElementById('bookmark-bar');
  if (!bar) return;
  function render() {
    bar.innerHTML = '';
    bookmarkManager.bookmarks.forEach((bm, i) => {
      const btn = document.createElement('button');
      btn.className = 'bookmark-btn';
      btn.textContent = bm.name;
      btn.addEventListener('click', () => bookmarkManager.apply(i));
      btn.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        bookmarkManager.remove(i);
        render();
      });
      bar.appendChild(btn);
    });
    const addBtn = document.createElement('button');
    addBtn.className = 'bookmark-btn';
    addBtn.textContent = '+ Save View';
    addBtn.style.opacity = '0.7';
    addBtn.addEventListener('click', () => {
      const name = `View ${bookmarkManager.bookmarks.length + 1}`;
      bookmarkManager.add(name);
      render();
    });
    bar.appendChild(addBtn);
  }
  bookmarkManager.onChange(render);
  render();
}
// ─── Main Application ────────────────────────────────────────────────
async function main() {
  const container = document.getElementById('canvas-container');
  // Renderer
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  container.appendChild(renderer.domElement);
  // Scene
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a1a);
  scene.fog = new THREE.Fog(0x0a0a1a, 15, 50);
  // Camera
  const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 80);
  camera.position.set(12, 10, 16);
  camera.lookAt(0, 2, 0);
  // Controls
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 2.5, 0);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.minDistance = 4;
  controls.maxDistance = 35;
  controls.maxPolarAngle = Math.PI * 0.55;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.3;
  controls.update();
  // Lighting
  const ambient = new THREE.AmbientLight(0x1a1a3a, 1.8);
  scene.add(ambient);
  const sun = new THREE.DirectionalLight(0xffeedd, 4.5);
  sun.position.set(15, 20, 8);
  sun.castShadow = true;
  sun.shadow.mapSize.width = 2048;
  sun.shadow.mapSize.height = 2048;
  sun.shadow.camera.near = 0.5;
  sun.shadow.camera.far = 60;
  sun.shadow.camera.left = -15;
  sun.shadow.camera.right = 15;
  sun.shadow.camera.top = 15;
  sun.shadow.camera.bottom = -15;
  sun.shadow.bias = -0.0001;
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
  fill.position.set(-5, 3, -8);
  scene.add(fill);
  // Ground grid
  const gridHelper = new THREE.GridHelper(TERRAIN_SIZE, 20, 0x223355, 0x111122);
  gridHelper.position.y = -0.02;
  scene.add(gridHelper);
  // ─── Terrain Mesh ───────────────────────────────────────────────
  let terrainMesh = null;
  function updateTerrain(timeIndex) {
    if (terrainMesh) {
      scene.remove(terrainMesh);
      terrainMesh.geometry.dispose();
      terrainMesh.material.dispose();
    }
    const geo = buildTerrainGeometry(timeIndex);
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true, roughness: 0.55, metalness: 0.05,
      flatShading: false
    });
    terrainMesh = new THREE.Mesh(geo, mat);
    terrainMesh.castShadow = true;
    terrainMesh.receiveShadow = true;
    terrainMesh.renderOrder = 0;
    scene.add(terrainMesh);
  }
  // ─── River (sync initial build, defer particle attachment) ─────
  // Build river synchronously on first render pass to avoid 200ms flash
  let currentTimeIndex = 0;
  let timeSlider = document.getElementById('time-slider');
  let timeLabel = document.getElementById('time-label');
  updateTerrain(currentTimeIndex);
  // Synchronous river build during initial render pass
  rebuildRiverNow(currentTimeIndex, scene);
  // ─── Particle System (deferred to idle callback after first paint) ─
  let particleFlow = null;
  function initParticlesDeferred() {
    if (particleFlow) return;
    particleFlow = new ParticleFlow(scene, 3000);
    // Pre-spawn initial trails
    for (let i = 0; i < 120; i++) {
      const sx = (Math.random() - 0.5) * TERRAIN_SIZE;
      const sz = (Math.random() - 0.5) * TERRAIN_SIZE;
      particleFlow.spawnTrail(sx, sz, currentTimeIndex);
    }
  }
  // Defer to idle callback so river renders first
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      initParticlesDeferred();
    });
  });
  // ─── Bookmarks ─────────────────────────────────────────────────
  const bookmarkManager = new BookmarkManager(controls, camera);
  buildBookmarkUI(bookmarkManager);
  // Sync bookmarks to localStorage on every camera-move-end
  let cameraMoveEndTimeout = null;
  controls.addEventListener('end', () => {
    if (cameraMoveEndTimeout) clearTimeout(cameraMoveEndTimeout);
    cameraMoveEndTimeout = setTimeout(() => {
      bookmarkManager.syncFromCamera();
      cameraMoveEndTimeout = null;
    }, 400);
  });
  // ─── Time Slider ───────────────────────────────────────────────
  timeSlider.addEventListener('input', () => {
    const ti = parseInt(timeSlider.value);
    currentTimeIndex = ti;
    const day = timeSeries[ti].day;
    timeLabel.textContent = `Day ${day}`;
    // Terrain swap: use cached geometry when available
    updateTerrain(ti);
    // River rebuild: debounced to avoid per-tick geometry allocation
    scheduleRiverRebuild(ti, scene);
  });
  // ─── Keyboard Shortcuts ────────────────────────────────────────
  window.addEventListener('keydown', (e) => {
    switch (e.key.toLowerCase()) {
      case 'r':
        controls.autoRotate = !controls.autoRotate;
        break;
      case 'b':
        bookmarkManager.add(`View ${bookmarkManager.bookmarks.length + 1}`);
        break;
      case 'f':
        // Reset camera
        camera.position.set(12, 10, 16);
        controls.target.set(0, 2.5, 0);
        controls.update();
        break;
      case 'arrowleft':
        timeSlider.value = Math.max(0, currentTimeIndex - 1);
        timeSlider.dispatchEvent(new Event('input'));
        break;
      case 'arrowright':
        timeSlider.value = Math.min(99, currentTimeIndex + 1);
        timeSlider.dispatchEvent(new Event('input'));
        break;
    }
  });
  // ─── Resize Handler ────────────────────────────────────────────
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
  // ─── Render Loop ───────────────────────────────────────────────
  let lastFrameTime = performance.now();
  let frameTimes = [];
  let frameCount = 0;
  function animate(timestamp) {
    requestAnimationFrame(animate);
    const deltaMs = Math.min(50, timestamp - lastFrameTime);
    lastFrameTime = timestamp;
    frameCount++;
    controls.update();
    // Update particles with frame-budget awareness
    if (particleFlow) {
      particleFlow.update(deltaMs, currentTimeIndex);
    }
    renderer.render(scene, camera);
    // Track rolling average frame time for diagnostics
    frameTimes.push(deltaMs);
    if (frameTimes.length > 30) frameTimes.shift();
    const avgFrame = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length;
    if (frameCount % 15 === 0) {
      updateDiagnosticPanel(particleFlow || { activeCount: 0 }, currentTimeIndex, avgFrame);
    }
  }
  requestAnimationFrame(animate);
}
main().catch(console.error);
</script>
</body>
</html>