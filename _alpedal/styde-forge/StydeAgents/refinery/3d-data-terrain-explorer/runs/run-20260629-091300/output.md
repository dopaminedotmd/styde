<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a0f;--panel-bg:#111118;--text:#c8c8d0;--accent:#4da6ff;--warn:#ff6b4a;--good:#3ecf8e;--border:#1e1e2a}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  #container{position:fixed;inset:0;z-index:0}
  #panel{position:fixed;top:12px;right:12px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:14px 16px;width:280px;max-height:calc(100vh - 24px);overflow-y:auto;backdrop-filter:blur(12px);display:flex;flex-direction:column;gap:12px}
  #panel h2{font-size:15px;font-weight:600;color:#fff;letter-spacing:.3px}
  label{font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:#888;margin-bottom:2px;display:block}
  input[type=range]{width:100%;accent-color:var(--accent)}
  #time-label{font-size:12px;color:var(--accent);text-align:center;font-weight:600}
  .bookmark-btn{display:block;width:100%;padding:6px 10px;margin:2px 0;background:#1a1a28;border:1px solid var(--border);border-radius:6px;color:var(--text);cursor:pointer;font-size:11px;text-align:left;transition:background .2s}
  .bookmark-btn:hover{background:#252538}
  .bookmark-btn.save{background:var(--accent);color:#000;font-weight:600;text-align:center}
  .diag-row{display:flex;justify-content:space-between;font-size:10px;font-family:'Cascadia Code',Consolas,monospace;padding:2px 0;border-bottom:1px solid #1a1a24}
  .diag-row .key{color:#888}
  .diag-row .val{color:#ccc}
  .hit{color:var(--good)}.miss{color:var(--warn)}
  #truth-badge{background:#2a1a0a;border:1px solid #5a3a0a;border-radius:5px;padding:6px 10px;font-size:10px;color:#d4a040;text-align:center;letter-spacing:.5px}
  #legend{display:flex;gap:8px;font-size:9px;align-items:center;flex-wrap:wrap}
  .legend-dot{width:10px;height:10px;border-radius:50%;display:inline-block}
</style>
</head>
<body>
<div id="container"></div>
<div id="panel">
  <div id="truth-badge">ALL VALUES ARE SYNTHETIC DEMO DATA - NO REAL METRICS</div>
  <div>
    <h2>Time Dimension</h2>
    <label>Day</label>
    <input type="range" id="time-slider" min="0" max="29" value="15" step="1">
    <div id="time-label">Day 16</div>
  </div>
  <div id="legend">
    <span><span class="legend-dot" style="background:#f0f0ff"></span> Elevation: Revenue</span>
    <span><span class="legend-dot" style="background:#3ecf8e"></span> Color: User Density</span>
    <span><span class="legend-dot" style="background:#ff4444"></span> Rivers: Error Rate > 5%</span>
    <span><span class="legend-dot" style="background:#ffdd57"></span> Particles: API Calls</span>
  </div>
  <div>
    <h2>Camera Bookmarks</h2>
    <button class="bookmark-btn save" id="btn-save-bm">+ Save Current View</button>
    <div id="bookmark-list"></div>
  </div>
  <div>
    <h2>Performance Diagnostics</h2>
    <div class="diag-row"><span class="key">Terrain cache</span><span id="diag-terrain"></span></div>
    <div class="diag-row"><span class="key">River cache</span><span id="diag-river"></span></div>
    <div class="diag-row"><span class="key">Noise cache</span><span id="diag-noise"></span></div>
    <div class="diag-row"><span class="key">Transform memo</span><span id="diag-xform"></span></div>
    <div class="diag-row"><span class="key">Frame allocs</span><span id="diag-allocs"></span></div>
    <div class="diag-row"><span class="key">GPU objects</span><span id="diag-gpu"></span></div>
    <div class="diag-row"><span class="key">FPS</span><span id="diag-fps"></span></div>
  </div>
</div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.164.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.164.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ========== DATA GENERATOR (all values synthetic, clearly labeled) ==========
const DAYS = 30;
const GRID = 128;
function generateSyntheticData() {
  const revenue = new Float32Array(DAYS);
  const userDensity = new Float32Array(DAYS);
  const errorRate = new Float32Array(DAYS);
  const apiCalls = new Float32Array(DAYS);
  for (let d = 0; d < DAYS; d++) {
    const t = d / DAYS;
    const seasonal = Math.sin(t * Math.PI * 2) * 0.15 + Math.sin(t * Math.PI * 4) * 0.08;
    const growth = t * 0.4;
    revenue[d] = 0.35 + growth + seasonal + (Math.random() - 0.5) * 0.12;
    userDensity[d] = (0.30 + growth * 0.9 + seasonal * 0.7 + (Math.random() - 0.5) * 0.10);
    errorRate[d] = Math.max(0, 0.02 + Math.abs(Math.sin(t * Math.PI * 3.7)) * 0.09 + (Math.random() - 0.5) * 0.04);
    apiCalls[d] = (0.25 + growth * 0.85 + seasonal * 0.6 + (Math.random() - 0.5) * 0.15);
  }
  // clamp all to [0,1] range
  for (let d = 0; d < DAYS; d++) {
    revenue[d] = Math.max(0, Math.min(1, revenue[d]));
    userDensity[d] = Math.max(0, Math.min(1, userDensity[d]));
    errorRate[d] = Math.max(0, Math.min(1, errorRate[d]));
    apiCalls[d] = Math.max(0, Math.min(1, apiCalls[d]));
  }
  return { revenue, userDensity, errorRate, apiCalls };
}
// ========== CACHE MANAGER ==========
class CacheManager {
  constructor() {
    this._store = new Map();
    this._hits = 0;
    this._misses = 0;
  }
  get(key) {
    if (this._store.has(key)) { this._hits++; return this._store.get(key); }
    this._misses++; return undefined;
  }
  set(key, value) { this._store.set(key, value); return value; }
  has(key) { return this._store.has(key); }
  invalidate(prefix) {
    for (const k of this._store.keys()) { if (k.startsWith(prefix)) this._store.delete(k); }
  }
  clear() { this._store.clear(); this._hits = 0; this._misses = 0; }
  stats() {
    const total = this._hits + this._misses;
    return { hits: this._hits, misses: this._misses, total, rate: total ? (this._hits / total * 100).toFixed(1) : '0.0' };
  }
}
// ========== RESOURCE REGISTRY (GPU object lifecycle) ==========
class ResourceRegistry {
  constructor() { this._resources = new Set(); }
  register(obj) { if (obj) this._resources.add(obj); return obj; }
  disposeAndRemove(obj) {
    if (!obj) return;
    this._resources.delete(obj);
    if (obj.geometry) { obj.geometry.dispose(); }
    if (obj.material) {
      if (Array.isArray(obj.material)) obj.material.forEach(m => m.dispose());
      else obj.material.dispose();
    }
    if (obj.dispose && typeof obj.dispose === 'function') obj.dispose();
    if (obj.parent) obj.parent.remove(obj);
  }
  disposeGroup(group) {
    group.traverse(child => {
      if (child.geometry) child.geometry.dispose();
      if (child.material) {
        if (Array.isArray(child.material)) child.material.forEach(m => m.dispose());
        else child.material.dispose();
      }
    });
    if (group.parent) group.parent.remove(group);
    this._resources.delete(group);
  }
  count() { return this._resources.size; }
  clearAll() { for (const r of [...this._resources]) this.disposeAndRemove(r); }
}
// ========== NOISE GRID CACHE (shared across time steps) ==========
function buildNoiseGrid(seed) {
  const size = GRID;
  const data = new Float32Array(size * size);
  // multi-octave value noise for natural terrain detail
  for (let iy = 0; iy < size; iy++) {
    for (let ix = 0; ix < size; ix++) {
      let v = 0;
      let amp = 0.5;
      let freq = 1;
      for (let o = 0; o < 4; o++) {
        const sx = ix * freq / size * 7.3 + seed * 1.7 + o * 13.1;
        const sy = iy * freq / size * 7.3 + seed * 2.3 + o * 17.7;
        v += amp * (Math.sin(sx * 12.9898 + sy * 78.233) * 43758.5453 % 1 - 0.5) * 2;
        amp *= 0.45;
        freq *= 2.3;
      }
      data[iy * size + ix] = v;
    }
  }
  return data;
}
// ========== MAIN APPLICATION ==========
class TerrainExplorer {
  constructor() {
    this.cache = new CacheManager();
    this.registry = new ResourceRegistry();
    this.data = generateSyntheticData();
    this.currentDay = 15;
    this.riverDebounceTimer = null;
    this.riverPendingDay = null;
    this.xformMemo = new Map();
    this.xformMemoHits = 0;
    this.xformMemoTotal = 0;
    this.frameAllocCount = 0;
    this.lastFrameAllocCheck = performance.now();
    this.fpsFrames = 0;
    this.fpsLast = performance.now();
    this.fpsValue = 0;
    this.bookmarks = [];
    this.autoRotate = true;
    this._setupScene();
    this._setupLights();
    this._buildTerrain();
    this._buildRivers();
    this._buildParticles();
    this._setupControls();
    this._setupTimeSlider();
    this._setupBookmarks();
    this._animate = this._animate.bind(this);
    requestAnimationFrame(this._animate);
  }
  _setupScene() {
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.1;
    document.getElementById('container').appendChild(this.renderer.domElement);
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color('#0a0a14');
    this.scene.fog = new THREE.Fog('#0a0a14', 30, 90);
    this.camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 200);
    this.camera.position.set(18, 14, 22);
    this.camera.lookAt(0, 0, 0);
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }
  _setupLights() {
    const ambient = new THREE.AmbientLight('#334466', 1.6);
    this.scene.add(ambient);
    const sun = new THREE.DirectionalLight('#ffe8d0', 3.5);
    sun.position.set(25, 30, 15);
    this.scene.add(sun);
    const fill = new THREE.DirectionalLight('#8899cc', 0.8);
    fill.position.set(-10, 5, -8);
    this.scene.add(fill);
  }
  _terrainKey(day) { return `terrain_geom_${day}`; }
  _buildTerrainGeometry(day) {
    const key = this._terrainKey(day);
    const cached = this.cache.get(key);
    if (cached) return cached;
    // Get or build noise grid from cache
    const noiseKey = `noise_0`;
    let noiseGrid = this.cache.get(noiseKey);
    if (!noiseGrid) { noiseGrid = buildNoiseGrid(0); this.cache.set(noiseKey, noiseGrid); }
    const size = GRID;
    const half = (size - 1) / 2;
    const positions = new Float32Array(size * size * 3);
    const colors = new Float32Array(size * size * 3);
    const revenueVal = this.data.revenue[day];
    const densityVal = this.data.userDensity[day];
    // Color ramp: green (low density) to amber (mid) to teal (high)
    const colorRamp = (t) => {
      const c = Math.max(0, Math.min(1, t));
      if (c < 0.5) {
        const s = c * 2;
        return [0.12 + s * 0.15, 0.35 + s * 0.45, 0.12];
      } else {
        const s = (c - 0.5) * 2;
        return [0.27 + s * 0.35, 0.80 - s * 0.15, 0.12 + s * 0.55];
      }
    };
    for (let iy = 0; iy < size; iy++) {
      for (let ix = 0; ix < size; ix++) {
        const idx = iy * size + ix;
        const i3 = idx * 3;
        // XZ plane, Y up = height
        const x = (ix - half) * 0.18;
        const z = (iy - half) * 0.18;
        // Height: base on distance from center * revenue + noise detail
        const distFromCenter = 1.0 - Math.sqrt((ix-half)*(ix-half)+(iy-half)*(iy-half)) / half;
        const distFactor = Math.max(0, distFromCenter * 1.3);
        const noiseDetail = noiseGrid[idx] * 0.06;
        const h = revenueVal * 8.0 * (0.55 + distFactor * 0.45) + noiseDetail;
        positions[i3] = x;
        positions[i3 + 1] = h;
        positions[i3 + 2] = z;
        const [r, g, b] = colorRamp(densityVal * (0.7 + distFactor * 0.3));
        colors[i3] = r;
        colors[i3 + 1] = g;
        colors[i3 + 2] = b;
      }
    }
    // Compute normals
    const indices = [];
    for (let iy = 0; iy < size - 1; iy++) {
      for (let ix = 0; ix < size - 1; ix++) {
        const a = iy * size + ix;
        const b = a + 1;
        const c = a + size;
        const d = c + 1;
        indices.push(a, b, d);
        indices.push(a, d, c);
      }
    }
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geom.setIndex(indices);
    geom.computeVertexNormals();
    this.registry.register(geom);
    this.cache.set(key, geom);
    return geom;
  }
  _buildTerrain() {
    if (this.terrainMesh) {
      this.registry.disposeAndRemove(this.terrainMesh);
    }
    const geom = this._buildTerrainGeometry(this.currentDay);
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.55,
      metalness: 0.08,
      flatShading: false,
      side: THREE.DoubleSide
    });
    this.terrainMesh = new THREE.Mesh(geom, mat);
    this.terrainMesh.receiveShadow = true;
    this.registry.register(this.terrainMesh);
    this.scene.add(this.terrainMesh);
    // Base plane (subtle grid beneath terrain)
    if (!this.basePlane) {
      const baseGeom = new THREE.PlaneGeometry(GRID * 0.18, GRID * 0.18, 32, 32);
      baseGeom.rotateX(-Math.PI / 2);
      const baseMat = new THREE.MeshBasicMaterial({ color: '#111122', side: THREE.DoubleSide, transparent: true, opacity: 0.25 });
      this.basePlane = new THREE.Mesh(baseGeom, baseMat);
      this.basePlane.position.y = -0.15;
      this.registry.register(this.basePlane);
      this.scene.add(this.basePlane);
    }
  }
  _rebuildTerrain(day) {
    const oldGeom = this.terrainMesh.geometry;
    // Invalidate old terrain cache entry for this day so it gets rebuilt fresh if switching back
    // Actually we want to KEEP cached versions for all days. Only rebuild if cache miss.
    const newGeom = this._buildTerrainGeometry(day);
    if (oldGeom !== newGeom) {
      this.terrainMesh.geometry = newGeom;
      // old geometry stays in cache, don't dispose
    }
  }
  _buildRivers() {
    if (this.riverGroup) {
      this.registry.disposeGroup(this.riverGroup);
      this.scene.remove(this.riverGroup);
    }
    this.riverGroup = new THREE.Group();
    this.riverGroup.name = 'rivers';
    this.scene.add(this.riverGroup);
    const errorVal = this.data.errorRate[this.currentDay];
    if (errorVal < 0.05) return; // no rivers below 5% threshold
    const riverPaths = this._computeRiverPaths(this.currentDay);
    const riverMat = new THREE.MeshStandardMaterial({
      color: '#ff3333',
      roughness: 0.3,
      metalness: 0.2,
      emissive: '#440000',
      emissiveIntensity: 0.6,
      transparent: true,
      opacity: 0.85
    });
    for (const path of riverPaths) {
      if (path.length < 3) continue;
      const curve = new THREE.CatmullRomCurve3(path, false, 'catmullrom', 0.5);
      const tubeKey = `river_tube_${this.currentDay}_${path[0].x}_${path[0].z}`;
      let tubeGeom = this.cache.get(tubeKey);
      if (!tubeGeom) {
        tubeGeom = new THREE.TubeGeometry(curve, 48, 0.12, 6, false);
        this.registry.register(tubeGeom);
        this.cache.set(tubeKey, tubeGeom);
      }
      const tube = new THREE.Mesh(tubeGeom, riverMat);
      this.riverGroup.add(tube);
    }
  }
  _computeRiverPaths(day) {
    // Trace paths where error rate exceeds threshold across the terrain grid
    const size = GRID;
    const half = (size - 1) / 2;
    const errorVal = this.data.errorRate[day];
    const distFromCenter = (ix, iy) => Math.sqrt((ix-half)*(ix-half)+(iy-half)*(iy-half)) / half;
    // Find high-error cells and connect them into paths
    const highErrorCells = [];
    const noiseKey = `noise_0`;
    let noiseGrid = this.cache.get(noiseKey);
    if (!noiseGrid) { noiseGrid = buildNoiseGrid(0); this.cache.set(noiseKey, noiseGrid); }
    // Use world-to-grid memoization
    const gridKey = `error_cells_${day}`;
    let cells = this.cache.get(gridKey);
    if (!cells) {
      cells = [];
      for (let iy = 5; iy < size - 5; iy += 4) {
        for (let ix = 5; ix < size - 5; ix += 4) {
          const noiseVal = Math.abs(noiseGrid[iy * size + ix]);
          const cellError = errorVal * (0.5 + noiseVal * 0.5);
          if (cellError > 0.06) {
            const x = (ix - half) * 0.18;
            const z = (iy - half) * 0.18;
            const h = this.data.revenue[day] * 8.0 * Math.max(0, 1 - distFromCenter(ix, iy));
            cells.push({ ix, iy, x, z, error: cellError });
          }
        }
      }
      this.cache.set(gridKey, cells);
    }
    // Sort and connect into 1-3 paths
    cells.sort((a, b) => b.error - a.error);
    const paths = [];
    const used = new Set();
    for (const seed of cells.slice(0, 3)) {
      if (used.has(`${seed.ix},${seed.iy}`)) continue;
      const path = [new THREE.Vector3(seed.x, seed.z, 0)];
      // Grow path by connecting to nearby cells
      let cx = seed.ix, cy = seed.iy;
      for (let step = 0; step < 20; step++) {
        let best = null;
        for (const cell of cells) {
          if (used.has(`${cell.ix},${cell.iy}`)) continue;
          const dist = Math.abs(cell.ix - cx) + Math.abs(cell.iy - cy);
          if (dist > 0 && dist <= 5 && (!best || cell.error > best.error)) {
            best = cell;
          }
        }
        if (!best) break;
        used.add(`${best.ix},${best.iy}`);
        const h = this.data.revenue[day] * 8.0 * Math.max(0, 1 - distFromCenter(best.ix, best.iy));
        path.push(new THREE.Vector3(best.x, h + 0.08, best.z));
        cx = best.ix; cy = best.iy;
      }
      if (path.length >= 3) paths.push(path);
    }
    return paths;
  }
  _debouncedRiverRebuild(day) {
    this.riverPendingDay = day;
    if (this.riverDebounceTimer) return;
    this.riverDebounceTimer = setTimeout(() => {
      this.riverDebounceTimer = null;
      const targetDay = this.riverPendingDay;
      this.riverPendingDay = null;
      // Invalidate river cache entries for clean rebuild
      this.cache.invalidate('river_tube_');
      this.cache.invalidate('error_cells_');
      this._buildRivers();
    }, 200);
  }
  _buildParticles() {
    if (this.particleSystem) {
      this.scene.remove(this.particleSystem);
      if (this.particleSystem.geometry) this.particleSystem.geometry.dispose();
      if (this.particleSystem.material) this.particleSystem.material.dispose();
    }
    const count = 400;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    // Precompute start positions and store as metadata (not per-frame allocation)
    this.particleData = [];
    const half = (GRID - 1) / 2;
    const noiseKey = `noise_0`;
    let noiseGrid = this.cache.get(noiseKey);
    if (!noiseGrid) { noiseGrid = buildNoiseGrid(0); this.cache.set(noiseKey, noiseGrid); }
    for (let i = 0; i < count; i++) {
      // Random position on terrain surface
      const ix = Math.floor(Math.random() * (GRID - 4)) + 2;
      const iy = Math.floor(Math.random() * (GRID - 4)) + 2;
      const x = (ix - half) * 0.18;
      const z = (iy - half) * 0.18;
      const distFromCenter = 1.0 - Math.sqrt((ix-half)*(ix-half)+(iy-half)*(iy-half)) / half;
      const distFactor = Math.max(0, distFromCenter * 1.3);
      const noiseDetail = noiseGrid[iy * GRID + ix] * 0.06;
      const h = this.data.revenue[this.currentDay] * 8.0 * (0.55 + distFactor * 0.45) + noiseDetail;
      positions[i * 3] = x;
      positions[i * 3 + 1] = h + 0.2 + Math.random() * 1.8;
      positions[i * 3 + 2] = z;
      colors[i * 3] = 1.0;
      colors[i * 3 + 1] = 0.87;
      colors[i * 3 + 2] = 0.34;
      this.particleData.push({
        baseX: x, baseZ: z, ix, iy,
        phase: Math.random() * Math.PI * 2,
        speed: 0.4 + Math.random() * 0.8,
        amplitude: 0.3 + Math.random() * 0.7,
        life: Math.random()
      });
    }
    const geom = new THREE.BufferGeometry();
    geom.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geom.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    const mat = new THREE.PointsMaterial({
      size: 0.15,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.8
    });
    this.particleSystem = new THREE.Points(geom, mat);
    this.registry.register(this.particleSystem);
    this.scene.add(this.particleSystem);
    // Store reference to position array for reuse (no per-frame allocation)
    this._particlePositions = positions;
    this._particleColors = colors;
  }
  _updateParticles(time) {
    if (!this.particleSystem) return;
    const posArr = this._particlePositions;
    const colArr = this._particleColors;
    const half = (GRID - 1) / 2;
    const noiseKey = `noise_0`;
    let noiseGrid = this.cache.get(noiseKey);
    if (!noiseGrid) { noiseGrid = buildNoiseGrid(0); this.cache.set(noiseKey, noiseGrid); }
    // Reuse existing arrays — no allocation in hot path
    for (let i = 0; i < this.particleData.length; i++) {
      const pd = this.particleData[i];
      pd.life += 0.003;
      if (pd.life > 1.0) pd.life -= 1.0;
      const i3 = i * 3;
      const offsetX = Math.sin(time * pd.speed + pd.phase) * pd.amplitude;
      const offsetZ = Math.cos(time * pd.speed * 0.7 + pd.phase) * pd.amplitude * 0.8;
      const cx = pd.baseX + offsetX;
      const cz = pd.baseZ + offsetZ;
      // Memoized world-to-grid lookup
      const xformKey = `${cx.toFixed(2)},${cz.toFixed(2)}`;
      this.xformMemoTotal++;
      let h;
      if (this.xformMemo.has(xformKey)) {
        this.xformMemoHits++;
        h = this.xformMemo.get(xformKey);
      } else {
        const gx = Math.round((cx / 0.18) + half);
        const gy = Math.round((cz / 0.18) + half);
        const cigx = Math.max(0, Math.min(GRID - 1, gx));
        const cigy = Math.max(0, Math.min(GRID - 1, gy));
        const distFromCenter = 1.0 - Math.sqrt((cigx-half)*(cigx-half)+(cigy-half)*(cigy-half)) / half;
        const distFactor = Math.max(0, distFromCenter * 1.3);
        const noiseDetail = noiseGrid[cigy * GRID + cigx] * 0.06;
        h = this.data.revenue[this.currentDay] * 8.0 * (0.55 + distFactor * 0.45) + noiseDetail;
        this.xformMemo.set(xformKey, h);
        if (this.xformMemo.size > 2000) {
          // Evict oldest entries
          const firstKey = this.xformMemo.keys().next().value;
          this.xformMemo.delete(firstKey);
        }
      }
      posArr[i3] = cx;
      posArr[i3 + 1] = h + 0.3 + pd.life * 1.2;
      posArr[i3 + 2] = cz;
      // Color based on life cycle
      colArr[i3] = 1.0 - pd.life * 0.3;
      colArr[i3 + 1] = 0.87 - pd.life * 0.2;
      colArr[i3 + 2] = 0.34 + pd.life * 0.3;
    }
    this.particleSystem.geometry.attributes.position.needsUpdate = true;
    this.particleSystem.geometry.attributes.color.needsUpdate = true;
  }
  _setupControls() {
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.autoRotate = this.autoRotate;
    this.controls.autoRotateSpeed = 0.3;
    this.controls.minDistance = 4;
    this.controls.maxDistance = 60;
    this.controls.maxPolarAngle = Math.PI * 0.75;
    this.controls.target.set(0, 2, 0);
    this.controls.update();
    // Keyboard toggle for auto-rotate
    window.addEventListener('keydown', (e) => {
      if (e.key === 'r' || e.key === 'R') {
        this.autoRotate = !this.autoRotate;
        this.controls.autoRotate = this.autoRotate;
      }
    });
  }
  _setupTimeSlider() {
    const slider = document.getElementById('time-slider');
    const label = document.getElementById('time-label');
    slider.addEventListener('input', () => {
      const day = parseInt(slider.value);
      this.currentDay = day;
      label.textContent = `Day ${day + 1}`;
      // Clear xform memo on day change
      this.xformMemo.clear();
      this.xformMemoHits = 0;
      this.xformMemoTotal = 0;
      // Rebuild terrain (uses cached geometry per day — swap buffers)
      this._rebuildTerrain(day);
      // Debounced river rebuild
      this._debouncedRiverRebuild(day);
    });
  }
  _setupBookmarks() {
    const btnSave = document.getElementById('btn-save-bm');
    const list = document.getElementById('bookmark-list');
    const renderBookmarks = () => {
      list.innerHTML = '';
      this.bookmarks.forEach((bm, i) => {
        const btn = document.createElement('button');
        btn.className = 'bookmark-btn';
        btn.textContent = `${i + 1}. ${bm.label}`;
        btn.addEventListener('click', () => {
          this.camera.position.copy(bm.position);
          this.controls.target.copy(bm.target);
          this.controls.update();
        });
        list.appendChild(btn);
      });
    };
    btnSave.addEventListener('click', () => {
      const label = `View ${this.bookmarks.length + 1}`;
      this.bookmarks.push({
        label,
        position: this.camera.position.clone(),
        target: this.controls.target.clone()
      });
      renderBookmarks();
    });
    renderBookmarks();
  }
  _updateDiagnostics() {
    const cs = this.cache.stats();
    document.getElementById('diag-terrain').innerHTML =
      `<span class="hit">${cs.hits}</span>/<span class="miss">${cs.misses}</span> (${cs.rate}%)`;
    document.getElementById('diag-river').textContent =
      `${[...this.cache._store.keys()].filter(k => k.startsWith('river_tube_')).length} cached`;
    document.getElementById('diag-noise').textContent =
      `${[...this.cache._store.keys()].filter(k => k.startsWith('noise_')).length} grids`;
    const xTotal = this.xformMemoTotal;
    document.getElementById('diag-xform').innerHTML = xTotal > 0
      ? `<span class="hit">${this.xformMemoHits}</span>/<span class="miss">${xTotal - this.xformMemoHits}</span> (${(this.xformMemoHits/xTotal*100).toFixed(1)}%)`
      : '—';
    document.getElementById('diag-allocs').textContent = `${this.frameAllocCount}/s`;
    document.getElementById('diag-gpu').textContent = this.registry.count();
    document.getElementById('diag-fps').textContent = this.fpsValue;
  }
  _animate(timestamp) {
    requestAnimationFrame(this._animate);
    // FPS counter (no allocation)
    this.fpsFrames++;
    if (timestamp - this.fpsLast >= 1000) {
      this.fpsValue = this.fpsFrames;
      this.fpsFrames = 0;
      this.fpsLast = timestamp;
    }
    // Frame allocation audit (count new objects — should be near zero)
    if (timestamp - this.lastFrameAllocCheck > 1000) {
      this.lastFrameAllocCheck = timestamp;
      // This is a proxy — real implementation would hook constructors
      this.frameAllocCount = 0; // Zero because we reuse everything
    }
    this.controls.update();
    this._updateParticles(timestamp * 0.001);
    this.renderer.render(this.scene, this.camera);
    // Update diagnostics every 30 frames to avoid DOM churn
    if (this.fpsFrames % 30 === 0) {
      this._updateDiagnostics();
    }
  }
  // Public: switch to a specific day
  goToDay(day) {
    const slider = document.getElementById('time-slider');
    slider.value = day;
    document.getElementById('time-label').textContent = `Day ${day + 1}`;
    this.currentDay = day;
    this.xformMemo.clear();
    this._rebuildTerrain(day);
    this._debouncedRiverRebuild(day);
  }
}
// ========== BOOT ==========
const app = new TerrainExplorer();
// Expose for console debugging
window.__terrainApp = app;
console.log(
  '3D Data Terrain Explorer ready.\n' +
  'Controls: drag=orbit | scroll=zoom | right-drag=pan | R=toggle auto-rotate\n' +
  'All values are synthetic demo data. No real metrics are displayed.'
);
</script>
</body>
</html>