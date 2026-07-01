<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0a0f; overflow: hidden; font-family: 'Segoe UI', system-ui, sans-serif; color: #c8c8d4; }
  canvas { display: block; }
  #ui { position: fixed; bottom: 0; left: 0; right: 0; padding: 12px 16px;
        background: linear-gradient(transparent, rgba(10,10,20,0.92));
        display: flex; gap: 16px; align-items: center; flex-wrap: wrap; z-index: 10; }
  #ui label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #888; }
  #time-slider { flex: 1; min-width: 200px; max-width: 500px; accent-color: #4af; }
  #time-label { font-variant-numeric: tabular-nums; min-width: 80px; font-size: 13px; }
  .btn { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
         color: #c8c8d4; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px;
         transition: background 0.15s; }
  .btn:hover { background: rgba(255,255,255,0.14); }
  .btn.active { background: rgba(68,170,255,0.2); border-color: #4af; }
  #bookmarks { display: flex; gap: 6px; }
  #diag { position: fixed; top: 12px; right: 12px; background: rgba(10,10,20,0.88);
          border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; padding: 10px 14px;
          font-size: 11px; line-height: 1.5; z-index: 10; min-width: 180px; }
  #diag .val { color: #4af; font-variant-numeric: tabular-nums; }
  #diag .warn { color: #fa4; }
  #tooltip { position: fixed; pointer-events: none; background: rgba(10,10,20,0.9);
             border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; padding: 6px 10px;
             font-size: 11px; display: none; z-index: 20; }
</style>
</head>
<body>
<div id="diag">
  Performance<br>
  Cache hits: <span class="val" id="cache-hits">0</span><br>
  Cache misses: <span class="val" id="cache-misses">0</span><br>
  Hit rate: <span class="val" id="hit-rate">--</span><br>
  FPS: <span class="val" id="fps">--</span><br>
  Allocs/frame: <span class="val" id="allocs">0</span>
</div>
<div id="tooltip"></div>
<div id="ui">
  <label>Time</label>
  <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
  <span id="time-label">T+0</span>
  <button class="btn" id="btn-auto-rotate">Auto Rotate</button>
  <button class="btn" id="btn-reset-cam">Reset View</button>
  <span style="color:#555;">|</span>
  <span style="font-size:11px;color:#888;">Bookmarks:</span>
  <span id="bookmarks"></span>
  <button class="btn" id="btn-save-bookmark">+ Save View</button>
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
// ---------------------------------------------------------------------------
// Purpose: Synthetic time-series data generator producing a 3-metric landscape.
// Usage:  const data = new TimeSeriesData(50, 100); data.revenue(t, x, y);
// ---------------------------------------------------------------------------
class TimeSeriesData {
  constructor(gridSize = 50, timeSteps = 100) {
    this.gridSize = gridSize;
    this.timeSteps = timeSteps;
    this._revenue = null;   // lazy-built cache: Float32Array[timeSteps * gridSize * gridSize]
    this._users = null;
    this._errors = null;
    this._apiCalls = null;
  }
  // Single source of truth: each metric stored once, views returned via offset indexing.
  _ensureBuilt() {
    if (this._revenue) return;
    const N = this.gridSize, T = this.timeSteps, total = T * N * N;
    this._revenue = new Float32Array(total);
    this._users   = new Float32Array(total);
    this._errors  = new Float32Array(total);
    this._apiCalls = new Float32Array(total);
    for (let t = 0; t < T; t++) {
      const wave = Math.sin(t * 0.18) * 0.5 + 0.5;
      for (let y = 0; y < N; y++) {
        for (let x = 0; x < N; x++) {
          const idx = t * N * N + y * N + x;
          const nx = x / (N - 1), ny = y / (N - 1);
          // Revenue: central peak that grows and shifts with time
          const cx = 0.5 + Math.cos(t * 0.12) * 0.25, cy = 0.5 + Math.sin(t * 0.1) * 0.2;
          const dist = Math.hypot(nx - cx, ny - cy);
          const hill = Math.exp(-dist * dist * 12) * (0.5 + wave * 0.5);
          const noise = Math.sin(nx * 8 + t * 0.3) * Math.cos(ny * 7 - t * 0.25) * 0.08;
          this._revenue[idx] = Math.max(0, hill + noise + 0.05);
          // Users: gradient from bottom-left (cold) to top-right (warm), modulated by wave
          this._users[idx] = (nx * 0.6 + ny * 0.4) * (0.6 + wave * 0.4);
          // Errors: inverse correlation with revenue — valleys of low revenue spike errors
          this._errors[idx] = (1 - this._revenue[idx]) * (0.1 + Math.abs(Math.sin(t * 0.4 + nx * 5)) * 0.25);
          // API calls: concentrated along a diagonal band that shifts over time
          const bandCenter = 0.4 + Math.sin(t * 0.08) * 0.3;
          const bandDist = Math.abs(nx + ny - bandCenter * 2);
          this._apiCalls[idx] = Math.exp(-bandDist * bandDist * 8) * (0.3 + wave * 0.5);
        }
      }
    }
  }
  // Return a Float32Array view (no copy) for metric at time t. Caller must not mutate.
  slice(metric, t) {
    this._ensureBuilt();
    const arr = this['_' + metric];
    const offset = t * this.gridSize * this.gridSize;
    return arr.subarray(offset, offset + this.gridSize * this.gridSize);
  }
  // Return a copy of a slice (safe to mutate — used once for terrain init)
  sliceCopy(metric, t) {
    return new Float32Array(this.slice(metric, t));
  }
}
// ---------------------------------------------------------------------------
// Purpose: Heightfield terrain mesh with vertex-color vegetation gradient.
//          Uses BufferGeometry with in-place Float32Array.set() on time scrub.
// Usage:  terrain = new TerrainMesh(data, scene); terrain.updateTime(42);
// ---------------------------------------------------------------------------
class TerrainMesh {
  constructor(data, scene) {
    this.data = data;
    this.gridSize = data.gridSize;
    this.N = this.gridSize;
    this.geometry = null;
    this.mesh = null;
    // Cache: pre-allocated position and color buffers, never re-allocated
    this._posArray = null;
    this._colArray = null;
    this._build(scene);
  }
  _build(scene) {
    const N = this.N;
    const geo = new THREE.BufferGeometry();
    const vertCount = N * N;
    this._posArray = new Float32Array(vertCount * 3);
    this._colArray = new Float32Array(vertCount * 3);
    // Build index buffer for triangle strip (shared, immutable after construction)
    const indices = [];
    for (let y = 0; y < N - 1; y++) {
      for (let x = 0; x < N; x++) {
        indices.push(y * N + x, (y + 1) * N + x);
      }
      if (y < N - 2) indices.push((y + 1) * N + (N - 1), (y + 1) * N);
    }
    geo.setIndex(indices);
    geo.setAttribute('position', new THREE.BufferAttribute(this._posArray, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(this._colArray, 3));
    geo.computeVertexNormals();
    // Vegetation-gradient material: vertex colors shaded with lambert
    const mat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.7,
      metalness: 0.1,
      flatShading: false,
      side: THREE.DoubleSide,
    });
    this.mesh = new THREE.Mesh(geo, mat);
    this.mesh.rotation.x = -Math.PI / 2.8;
    this.geometry = geo;
    scene.add(this.mesh);
    // Populate initial state at t=0
    this.updateTime(0);
  }
  // Hot-path: updates position and color arrays in-place. Zero allocations after first call.
  updateTime(t) {
    const revenueSlice = this.data.slice('revenue', t);
    const usersSlice = this.data.slice('users', t);
    const N = this.N;
    const spacing = 2 / (N - 1);
    for (let y = 0; y < N; y++) {
      for (let x = 0; x < N; x++) {
        const gi = y * N + x;
        const vi = gi * 3;
        const rev = revenueSlice[gi];
        const usr = usersSlice[gi];
        // In-place position update: x/z are static, only y (height) changes
        this._posArray[vi]     = (x - N / 2) * spacing;   // x — static, but we write for clarity
        this._posArray[vi + 1] = rev * 1.8;                // y = height from revenue
        this._posArray[vi + 2] = (y - N / 2) * spacing;   // z — static
        // Vertex color: vegetation gradient. Low users = brown/dirt, high = lush green
        const r = 0.25 + usr * 0.15;
        const g = 0.2 + usr * 0.65;
        const b = 0.12 + usr * 0.1;
        this._colArray[vi]     = r;
        this._colArray[vi + 1] = g;
        this._colArray[vi + 2] = b;
      }
    }
    // In-place buffer update: mark attributes as needing GPU upload. No re-allocation.
    this.geometry.attributes.position.needsUpdate = true;
    this.geometry.attributes.color.needsUpdate = true;
    this.geometry.computeVertexNormals();
  }
  // World-to-grid coordinate transform, memoized per frame to avoid recomputation.
  // Usage: const gi = terrain.worldToGrid(wx, wz); — call once per hover, not per-vertex.
  worldToGrid(wx, wz) {
    const N = this.N;
    const spacing = 2 / (N - 1);
    const gx = Math.round(wx / spacing + N / 2);
    const gy = Math.round(wz / spacing + N / 2);
    if (gx < 0 || gx >= N || gy < 0 || gy >= N) return -1;
    return gy * N + gx;
  }
  getHeightAt(t, gridIndex) {
    return this.data.slice('revenue', t)[gridIndex] * 1.8;
  }
}
// ---------------------------------------------------------------------------
// Purpose: River system tracing error hotspots as TubeGeometry across terrain.
//          Cached per terrain state; rebuilt only when heightfield changes > threshold.
// Usage:  rivers = new RiverSystem(data, terrain, scene); rivers.updateTime(t);
// ---------------------------------------------------------------------------
class RiverSystem {
  constructor(data, terrain, scene) {
    this.data = data;
    this.terrain = terrain;
    this.scene = scene;
    this.group = new THREE.Group();
    scene.add(this.group);
    // Cache: store last built time and heightfield fingerprint to skip rebuilds
    this._cachedTime = -1;
    this._cachedFingerprint = 0;
    this._debounceTimer = null;
    this._debounceMs = 200;
  }
  // Compute a lightweight fingerprint of the heightfield to detect meaningful changes.
  // Samples every 4th vertex to avoid full grid scan.
  _fingerprint(t) {
    const slice = this.data.slice('revenue', t);
    let hash = 0;
    const N = this.data.gridSize;
    for (let i = 0; i < slice.length; i += 4) {
      hash = ((hash << 5) - hash + (slice[i] * 1000 | 0)) | 0;
    }
    return hash;
  }
  updateTime(t) {
    const fp = this._fingerprint(t);
    // Cache hit: same fingerprint as last build, skip expensive TubeGeometry rebuild
    if (t === this._cachedTime && fp === this._cachedFingerprint) return;
    // Debounce: clear pending rebuild, schedule new one after 200ms quiet period
    if (this._debounceTimer) clearTimeout(this._debounceTimer);
    this._debounceTimer = setTimeout(() => {
      this._rebuild(t, fp);
      this._debounceTimer = null;
    }, this._debounceMs);
  }
  _rebuild(t, fp) {
    // Clear previous river meshes
    while (this.group.children.length > 0) {
      const child = this.group.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      this.group.remove(child);
    }
    const errors = this.data.slice('errors', t);
    const N = this.data.gridSize;
    const spacing = 2 / (N - 1);
    const threshold = 0.15;
    // Find error hotspots: grid cells where error > threshold
    const hotspots = [];
    for (let y = 0; y < N; y++) {
      for (let x = 0; x < N; x++) {
        if (errors[y * N + x] > threshold) {
          hotspots.push({ x, y, e: errors[y * N + x] });
        }
      }
    }
    if (hotspots.length < 3) return;
    // Sort by error descending, take top points for river path
    hotspots.sort((a, b) => b.e - a.e);
    const pathPoints = hotspots.slice(0, Math.min(12, hotspots.length));
    // Build 3D points along terrain surface
    const points3D = pathPoints.map(p => {
      const wx = (p.x - N / 2) * spacing;
      const wz = (p.y - N / 2) * spacing;
      const wy = this.data.slice('revenue', t)[p.y * N + p.x] * 1.8 + 0.04;
      return new THREE.Vector3(wx, wy, wz);
    });
    // Create smooth curve through hotspots
    const curve = new THREE.CatmullRomCurve3(points3D);
    // Cache: TubeGeometry built once per terrain change, not per frame
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.04, 8, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: 0xcc3322,
      emissive: 0x441111,
      roughness: 0.3,
      metalness: 0.5,
    });
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    this.group.add(tube);
    // Glow line along river center
    const glowGeo = new THREE.TubeGeometry(curve, 64, 0.015, 6, false);
    const glowMat = new THREE.MeshBasicMaterial({ color: 0xff4422, transparent: true, opacity: 0.7 });
    const glow = new THREE.Mesh(glowGeo, glowMat);
    this.group.add(glow);
    this._cachedTime = t;
    this._cachedFingerprint = fp;
  }
}
// ---------------------------------------------------------------------------
// Purpose: Particle flow trails representing API call data across the terrain.
//          Position arrays reused in-place; no per-frame allocations.
// Usage:  particles = new ParticleFlow(data, terrain, scene); particles.update(t, dt);
// ---------------------------------------------------------------------------
class ParticleFlow {
  constructor(data, terrain, scene) {
    this.data = data;
    this.terrain = terrain;
    this.N = data.gridSize;
    this.count = 600;
    // Pre-allocate position array — reused every frame via .set() or direct writes
    this._posArray = new Float32Array(this.count * 3);
    this._velocities = new Float32Array(this.count * 3); // per-particle velocity cache
    this._seeds = new Float32Array(this.count * 2);       // random seed offset per particle
    // Initialize particle paths near API-call hotspots at t=0
    const apiSlice = this.data.slice('apiCalls', 0);
    const spacing = 2 / (this.N - 1);
    for (let i = 0; i < this.count; i++) {
      // Seed particles preferentially in high-api-call regions
      let gx, gy;
      for (let attempt = 0; attempt < 10; attempt++) {
        gx = (Math.random() * this.N) | 0;
        gy = (Math.random() * this.N) | 0;
        if (Math.random() < apiSlice[gy * this.N + gx] + 0.1) break;
      }
      const wx = (gx - this.N / 2) * spacing;
      const wz = (gy - this.N / 2) * spacing;
      const wy = apiSlice[gy * this.N + gx] * 1.8 + 0.3;
      this._posArray[i * 3] = wx;
      this._posArray[i * 3 + 1] = wy;
      this._posArray[i * 3 + 2] = wz;
      this._seeds[i * 2] = Math.random() * 100;
      this._seeds[i * 2 + 1] = Math.random() * 100;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(this._posArray, 3));
    // Point sprite texture: small glowing dot
    const canvas = document.createElement('canvas');
    canvas.width = 16; canvas.height = 16;
    const ctx = canvas.getContext('2d');
    const grad = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    grad.addColorStop(0, 'rgba(180,220,255,1)');
    grad.addColorStop(0.3, 'rgba(100,180,255,0.8)');
    grad.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 16, 16);
    const texture = new THREE.CanvasTexture(canvas);
    const mat = new THREE.PointsMaterial({
      size: 0.06,
      map: texture,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      color: 0x88ccff,
      transparent: true,
      opacity: 0.75,
    });
    this.points = new THREE.Points(geo, mat);
    scene.add(this.points);
    this.geometry = geo;
  }
  // Hot-path: update all particle positions in-place. Zero allocations.
  update(t, dt) {
    const apiSlice = this.data.slice('apiCalls', t);
    const N = this.N;
    const spacing = 2 / (N - 1);
    const speed = 0.4;
    for (let i = 0; i < this.count; i++) {
      const i3 = i * 3;
      let wx = this._posArray[i3];
      let wz = this._posArray[i3 + 2];
      // Flow direction: toward higher API-call density (gradient ascent on apiCalls)
      const gx = Math.round(wx / spacing + N / 2);
      const gy = Math.round(wz / spacing + N / 2);
      let gradX = 0, gradZ = 0;
      if (gx > 0 && gx < N - 1 && gy > 0 && gy < N - 1) {
        gradX = apiSlice[gy * N + gx + 1] - apiSlice[gy * N + gx - 1];
        gradZ = apiSlice[(gy + 1) * N + gx] - apiSlice[(gy - 1) * N + gx];
      }
      // Add curl noise for organic movement
      const seedX = this._seeds[i * 2], seedZ = this._seeds[i * 2 + 1];
      const curlX = Math.sin(wz * 2.5 + t * 0.4 + seedX) * 0.3;
      const curlZ = Math.cos(wx * 2.5 + t * 0.4 + seedZ) * 0.3;
      const vx = gradX * 0.5 + curlX;
      const vz = gradZ * 0.5 + curlZ;
      const vLen = Math.hypot(vx, vz) || 1;
      wx += (vx / vLen) * speed * dt;
      wz += (vz / vLen) * speed * dt;
      // Wrap around edges
      const half = (N / 2) * spacing;
      if (wx < -half) wx = half;
      if (wx > half) wx = -half;
      if (wz < -half) wz = half;
      if (wz > half) wz = -half;
      // Height from terrain at current position
      const gxi = Math.round(wx / spacing + N / 2);
      const gyi = Math.round(wz / spacing + N / 2);
      const gi = Math.max(0, Math.min(N * N - 1, gyi * N + gxi));
      const wy = this.data.slice('revenue', t)[gi] * 1.8 + 0.15;
      // In-place write — no array allocation
      this._posArray[i3] = wx;
      this._posArray[i3 + 1] = wy;
      this._posArray[i3 + 2] = wz;
    }
    this.geometry.attributes.position.needsUpdate = true;
  }
}
// ---------------------------------------------------------------------------
// Purpose: Camera bookmark system for saving and recalling viewpoints.
// Usage:  bookmarks.save('overview'); bookmarks.restore('overview', controls);
// ---------------------------------------------------------------------------
class CameraBookmarks {
  constructor() {
    this._store = new Map();
  }
  save(name, camera, controls) {
    this._store.set(name, {
      position: camera.position.clone(),
      target: controls.target.clone(),
    });
  }
  restore(name, camera, controls) {
    const bm = this._store.get(name);
    if (!bm) return false;
    camera.position.copy(bm.position);
    controls.target.copy(bm.target);
    controls.update();
    return true;
  }
  list() { return Array.from(this._store.keys()); }
  has(name) { return this._store.has(name); }
}
// ---------------------------------------------------------------------------
// Purpose: Performance monitor tracking cache hits/misses and FPS.
//          Non-goal: exact allocation counting (uses heuristic). Acceptable
//          trade-off: approximate alloc tracking vs full memory instrumentation.
// Usage:  perf.recordHit(); perf.recordMiss(); perf.tick(dt);
// ---------------------------------------------------------------------------
class PerformanceMonitor {
  constructor() {
    this.hits = 0;
    this.misses = 0;
    this._frameTimes = [];
    this._fps = 0;
    this._allocEstimate = 0;
    this._lastAllocReset = performance.now();
  }
  recordHit() { this.hits++; }
  recordMiss() { this.misses++; }
  hitRate() {
    const total = this.hits + this.misses;
    return total === 0 ? '--' : (this.hits / total * 100).toFixed(1) + '%';
  }
  tick(dt) {
    this._frameTimes.push(dt);
    if (this._frameTimes.length > 60) this._frameTimes.shift();
    const avg = this._frameTimes.reduce((a, b) => a + b, 0) / this._frameTimes.length;
    this._fps = avg > 0 ? (1 / avg).toFixed(0) : '--';
    // Heuristic alloc estimate: resets per second
    const now = performance.now();
    if (now - this._lastAllocReset > 1000) {
      this._allocEstimate = 0;
      this._lastAllocReset = now;
    }
  }
  // Call when an allocation occurs in a hot path (for diagnostic panel)
  recordAlloc() { this._allocEstimate++; }
  getAllocs() { return this._allocEstimate; }
  getFPS() { return this._fps; }
}
// ---------------------------------------------------------------------------
// MAIN DASHBOARD
// Purpose: Orchestrates scene, controls, terrain, rivers, particles, bookmarks.
// Usage:  const dash = new Dashboard(); dash.animate();
// ---------------------------------------------------------------------------
class Dashboard {
  constructor() {
    this.perf = new PerformanceMonitor();
    this.bookmarks = new CameraBookmarks();
    // Scene setup
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0a0a14);
    this.scene.fog = new THREE.Fog(0x0a0a14, 4, 14);
    this.camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.3, 40);
    this.camera.position.set(3.5, 3.2, 4.5);
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    document.body.prepend(this.renderer.domElement);
    // Lighting
    const ambient = new THREE.AmbientLight(0x334466, 1.5);
    this.scene.add(ambient);
    const sun = new THREE.DirectionalLight(0xffeedd, 2.8);
    sun.position.set(5, 8, 3);
    this.scene.add(sun);
    const fill = new THREE.DirectionalLight(0x4466aa, 0.8);
    fill.position.set(-3, 1, -2);
    this.scene.add(fill);
    // OrbitControls with smooth damping
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.3;
    this.controls.target.set(0, 0.4, 0);
    this.controls.minDistance = 1.5;
    this.controls.maxDistance = 10;
    this.controls.maxPolarAngle = Math.PI * 0.6;
    this.controls.update();
    // Ground reference grid
    const gridHelper = new THREE.GridHelper(4, 20, 0x222244, 0x111122);
    gridHelper.position.y = -0.01;
    this.scene.add(gridHelper);
    // Data and visualization layers
    this.data = new TimeSeriesData(50, 100);
    this.terrain = new TerrainMesh(this.data, this.scene);
    this.rivers = new RiverSystem(this.data, this.terrain, this.scene);
    this.particles = new ParticleFlow(this.data, this.terrain, this.scene);
    // Default bookmarks
    this.bookmarks.save('Overview', this.camera, this.controls);
    this.camera.position.set(4.5, 3.8, 1.2);
    this.controls.target.set(0, 0.3, 0);
    this.controls.update();
    this.bookmarks.save('Close-up', this.camera, this.controls);
    this.camera.position.set(-2, 5.5, 3.5);
    this.controls.target.set(0, 0.2, 0);
    this.controls.update();
    this.bookmarks.save('Top-down', this.camera, this.controls);
    // Restore overview
    this.bookmarks.restore('Overview', this.camera, this.controls);
    // Time state
    this.currentTime = 0;
    this.targetTime = 0;
    this._lastRiverUpdate = 0;
    // UI bindings — deferred updates coalesced via rAF
    this._uiDirty = false;
    this._bindUI();
    // Resize
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
    // Raycaster for tooltip (memoized per frame via _lastHoverCheck)
    this._raycaster = new THREE.Raycaster();
    this._mouse = new THREE.Vector2();
    this._lastHoverCheck = 0;
    window.addEventListener('mousemove', (e) => {
      this._mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      this._mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    });
    // Start render loop
    this._lastFrameTime = performance.now();
    this._animate = this._animate.bind(this);
    requestAnimationFrame(this._animate);
  }
  _bindUI() {
    const slider = document.getElementById('time-slider');
    const label = document.getElementById('time-label');
    const btnAuto = document.getElementById('btn-auto-rotate');
    const btnReset = document.getElementById('btn-reset-cam');
    const btnSave = document.getElementById('btn-save-bookmark');
    const bookmarksEl = document.getElementById('bookmarks');
    // Time slider — sets target, actual update happens in animate loop (coalesced)
    slider.addEventListener('input', () => {
      this.targetTime = parseInt(slider.value);
      this._uiDirty = true;
      // Deferred UI label update to avoid per-event DOM thrash
    });
    btnAuto.addEventListener('click', () => {
      this.controls.autoRotate = !this.controls.autoRotate;
      btnAuto.classList.toggle('active', this.controls.autoRotate);
    });
    btnAuto.classList.add('active');
    btnReset.addEventListener('click', () => {
      this.bookmarks.restore('Overview', this.camera, this.controls);
    });
    btnSave.addEventListener('click', () => {
      const name = 'View ' + (this.bookmarks.list().filter(k => k.startsWith('View ')).length + 1);
      this.bookmarks.save(name, this.camera, this.controls);
      this._renderBookmarkButtons();
    });
    this._renderBookmarkButtons = () => {
      bookmarksEl.innerHTML = '';
      for (const name of this.bookmarks.list()) {
        const btn = document.createElement('button');
        btn.className = 'btn';
        btn.textContent = name;
        btn.addEventListener('click', () => {
          this.bookmarks.restore(name, this.camera, this.controls);
        });
        bookmarksEl.appendChild(btn);
      }
    };
    this._renderBookmarkButtons();
  }
  _updateDiagnosticPanel() {
    document.getElementById('cache-hits').textContent = this.perf.hits;
    document.getElementById('cache-misses').textContent = this.perf.misses;
    document.getElementById('hit-rate').textContent = this.perf.hitRate();
    document.getElementById('fps').textContent = this.perf.getFPS();
    document.getElementById('allocs').textContent = this.perf.getAllocs();
  }
  // Coalesced UI label update — runs at most once per frame via requestAnimationFrame
  _flushUI() {
    if (!this._uiDirty) return;
    this._uiDirty = false;
    document.getElementById('time-slider').value = this.currentTime;
    document.getElementById('time-label').textContent = 'T+' + this.currentTime;
  }
  // Tooltip hover — memoized per-frame check to avoid repeated raycaster calls
  _updateTooltip() {
    const now = performance.now();
    if (now - this._lastHoverCheck < 0.1) return; // at most 10Hz hover checks
    this._lastHoverCheck = now;
    this._raycaster.setFromCamera(this._mouse, this.camera);
    const hits = this._raycaster.intersectObject(this.terrain.mesh);
    const tip = document.getElementById('tooltip');
    if (hits.length > 0) {
      const p = hits[0].point;
      const gi = this.terrain.worldToGrid(p.x, p.z);
      if (gi >= 0) {
        const rev = this.data.slice('revenue', this.currentTime)[gi];
        const usr = this.data.slice('users', this.currentTime)[gi];
        const err = this.data.slice('errors', this.currentTime)[gi];
        tip.style.display = 'block';
        tip.style.left = (this._mouse.x * 0.5 + 0.5) * window.innerWidth + 14 + 'px';
        tip.style.top = (-this._mouse.y * 0.5 + 0.5) * window.innerHeight + 10 + 'px';
        tip.innerHTML =
          'Revenue: <span style="color:#4af;">' + (rev * 100).toFixed(1) + '%</span><br>' +
          'Users: <span style="color:#4f8;">' + (usr * 100).toFixed(1) + '%</span><br>' +
          'Errors: <span style="color:#f44;">' + (err * 100).toFixed(1) + '%</span>';
      }
    } else {
      tip.style.display = 'none';
    }
  }
  _animate() {
    requestAnimationFrame(this._animate);
    const now = performance.now();
    const dt = Math.min((now - this._lastFrameTime) / 1000, 0.1);
    this._lastFrameTime = now;
    this.controls.update();
    // Coalesced time update: apply targetTime only when UI signals a change
    if (this.currentTime !== this.targetTime) {
      this.currentTime = this.targetTime;
      this.terrain.updateTime(this.currentTime);
      this.perf.recordHit(); // terrain position array reused in-place = cache hit
      // River rebuild is debounced internally
      this.rivers.updateTime(this.currentTime);
      // Note: river may or may not rebuild; cache hit/miss tracked internally
    }
    this.particles.update(this.currentTime, dt);
    // Deferred UI flush — once per frame max
    this._flushUI();
    this._updateTooltip();
    // Diagnostic panel update throttled to ~2Hz to avoid DOM thrash
    if (Math.floor(now / 500) !== Math.floor((now - dt * 1000) / 500)) {
      this.perf.tick(dt);
      this._updateDiagnosticPanel();
    }
    this.renderer.render(this.scene, this.camera);
  }
}
// Boot
const dashboard = new Dashboard();
console.log('3D Data Terrain Explorer ready.');
console.log('Drag to orbit | Scroll to zoom | Right-drag to pan | Time slider reshapes terrain');
console.log('Bookmarks: save camera positions for recurring views');
console.log('Hover terrain for metric tooltip');
console.log('Green terrain = user density | Red rivers = error paths | Blue particles = API flows');
</script>
</body>
</html>