```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root {
    --bg: #0a0a14;
    --panel-bg: rgba(10,10,20,0.92);
    --text: #c8d6e5;
    --accent: #48dbfb;
    --warn: #ff6b6b;
    --good: #2ed573;
    --border: rgba(72,219,251,0.2);
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background: var(--bg);
    overflow: hidden;
    font-family: 'Segoe UI', system-ui, sans-serif;
    color: var(--text);
    height: 100vh;
    width: 100vw;
    touch-action: none;
  }
  canvas { display: block; }
  /* Top bar */
  .topbar {
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 44px;
    background: var(--panel-bg);
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 16px;
    z-index: 10;
    backdrop-filter: blur(8px);
  }
  .topbar .title {
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.5px;
    color: var(--accent);
    white-space: nowrap;
  }
  .topbar .spacer { flex:1; }
  /* Time controls */
  .time-controls {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .time-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.7;
    white-space: nowrap;
  }
  .time-value {
    font-size: 13px;
    font-weight: 600;
    min-width: 100px;
    text-align: center;
    color: var(--accent);
  }
  input[type=range] {
    -webkit-appearance: none;
    width: 160px;
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    outline: none;
    cursor: pointer;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--accent);
    border: 2px solid var(--bg);
    cursor: pointer;
  }
  .btn {
    background: rgba(72,219,251,0.1);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 11px;
    letter-spacing: 0.5px;
    transition: background 0.2s;
    white-space: nowrap;
  }
  .btn:hover { background: rgba(72,219,251,0.2); }
  .btn.active { background: rgba(72,219,251,0.3); border-color: var(--accent); }
  /* Panels */
  .panel {
    position: fixed;
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
    z-index: 10;
    backdrop-filter: blur(8px);
    font-size: 11px;
    min-width: 180px;
  }
  .panel-title {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    color: var(--accent);
    opacity: 0.8;
  }
  .legend { right: 16px; top: 60px; }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 4px 0;
  }
  .legend-swatch {
    width: 12px; height: 12px;
    border-radius: 2px;
    flex-shrink: 0;
  }
  .bookmarks { left: 16px; top: 60px; }
  .bookmark-row {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 3px 0;
  }
  .bookmark-row .btn { padding: 3px 8px; font-size: 10px; }
  .bookmark-name {
    flex: 1;
    font-size: 11px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .cache-panel { left: 16px; bottom: 60px; }
  .cache-row {
    display: flex;
    justify-content: space-between;
    margin: 2px 0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 10px;
  }
  .cache-hit { color: var(--good); }
  .cache-miss { color: var(--warn); }
  /* Bottom bar */
  .bottombar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    height: 36px;
    background: var(--panel-bg);
    border-top: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 16px;
    z-index: 10;
    font-size: 10px;
    backdrop-filter: blur(8px);
  }
  .bottombar .metric {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .bottombar .metric-label { opacity: 0.6; text-transform: uppercase; letter-spacing: 0.5px; }
  .bottombar .metric-value { font-weight: 600; color: var(--accent); }
  /* Responsive */
  @media (max-width: 768px) {
    .panel { min-width: 140px; padding: 8px; font-size: 10px; }
    .legend { right: 4px; top: 52px; }
    .bookmarks { left: 4px; top: 52px; }
    .cache-panel { left: 4px; bottom: 44px; }
    input[type=range] { width: 100px; }
    .topbar { padding: 0 8px; gap: 8px; }
    .topbar .title { font-size: 12px; }
    .btn { padding: 4px 7px; font-size: 10px; }
  }
  @media (max-width: 480px) {
    .legend { display: none; }
    .bookmarks { display: none; }
    .cache-panel { left: 4px; right: 4px; bottom: 40px; font-size: 9px; }
    input[type=range] { width: 80px; }
    .time-value { min-width: 70px; font-size: 11px; }
  }
</style>
</head>
<body>
<!-- Top bar -->
<div class="topbar">
  <span class="title">TERRAIN EXPLORER</span>
  <span class="spacer"></span>
  <div class="time-controls">
    <span class="time-label">Time</span>
    <span class="time-value" id="timeDisplay">Day 1</span>
    <input type="range" id="timeSlider" min="0" max="0" value="0" step="1">
    <button class="btn" id="btnPlay" title="Play/Pause">▶</button>
    <button class="btn" id="btnAutoRotate" title="Auto-rotate">↻</button>
  </div>
</div>
<!-- Legend panel -->
<div class="panel legend" id="legendPanel">
  <div class="panel-title">Metrics</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(#1a3a1a,#4caf50,#8bc34a)"></span>Elevation: Revenue</div>
  <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(#3e2723,#795548,#a5d6a7)"></span>Color: User Density</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ff4444"></span>Rivers: Error Rate</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ffd700"></span>Particles: API Calls</div>
</div>
<!-- Bookmarks panel -->
<div class="panel bookmarks" id="bookmarksPanel">
  <div class="panel-title">Bookmarks</div>
  <div id="bookmarkList">
    <div style="opacity:0.5;font-size:10px">Ctrl+1..4 to save<br>1..4 to recall</div>
  </div>
</div>
<!-- Cache diagnostic panel -->
<div class="panel cache-panel" id="cachePanel">
  <div class="panel-title">Cache Diagnostics</div>
  <div id="cacheStats"></div>
</div>
<!-- Bottom bar -->
<div class="bottombar" id="bottomBar">
  <div class="metric"><span class="metric-label">FPS</span><span class="metric-value" id="fpsDisplay">--</span></div>
  <div class="metric"><span class="metric-label">Particles</span><span class="metric-value" id="particleCount">0</span></div>
  <div class="metric"><span class="metric-label">Triangles</span><span class="metric-value" id="triCount">0</span></div>
  <span class="spacer" style="flex:1"></span>
  <div class="metric"><span class="metric-label">Hover</span><span class="metric-value" id="hoverData">--</span></div>
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
// ============================================================================
// DATA GENERATION — Realistic time-series dataset
// Produces 90 days of metrics: revenue, userDensity, errorRate, apiCalls
// Structured as a 64x64 grid per time step (simulating geospatial distribution)
// In production, swap this block for SRTM/GeoTIFF loader or API fetch
// ============================================================================
const GRID_SIZE = 64;
const TIME_STEPS = 90;
const DATA = (() => {
  // Seedable LCG for reproducible pseudo-random terrain
  // Each time step produces slightly different but coherent terrain
  let seed = 42;
  function lcg() { seed = (seed * 1664525 + 1013904223) & 0x7fffffff; return seed / 0x7fffffff; }
  // Simple 2D noise for terrain coherence (no dependency needed)
  function noise2D(x, y, t) {
    const a = Math.sin(x * 12.9898 + y * 78.233 + t * 1.7) * 43758.5453;
    const b = Math.sin(x * 39.346 + y * 21.657 - t * 0.9) * 23421.6312;
    const c = Math.sin((x + y) * 43.177 + t * 2.3) * 54321.1234;
    return ((Math.sin(a) * 0.5 + 0.5) + (Math.sin(b) * 0.3 + 0.3) + (Math.sin(c) * 0.2 + 0.2)) / 1.0;
  }
  const steps = [];
  for (let t = 0; t < TIME_STEPS; t++) {
    const grid = new Float32Array(GRID_SIZE * GRID_SIZE * 4); // [revenue, density, error, apiCalls]
    for (let y = 0; y < GRID_SIZE; y++) {
      for (let x = 0; x < GRID_SIZE; x++) {
        const fx = x / GRID_SIZE;
        const fy = y / GRID_SIZE;
        const i = (y * GRID_SIZE + x) * 4;
        // Revenue: base hills with time-shifting ridges (peak grows over time)
        const baseRevenue = noise2D(fx * 3, fy * 3, t * 0.03) * 0.6
          + noise2D(fx * 7, fy * 7, t * 0.05) * 0.3
          + Math.exp(-((fx - 0.5) ** 2 + (fy - 0.5) ** 2) * 8) * 0.4; // central peak
        grid[i] = Math.max(0, baseRevenue * (1.0 + t / TIME_STEPS * 0.6));
        // User density: correlated with revenue but with own noise pattern
        grid[i + 1] = noise2D(fx * 4 + 0.5, fy * 4 + 0.5, t * 0.04) * 0.5
          + grid[i] * 0.5 + 0.1;
        // Error rate: inverse correlation, spikes in transition zones
        const edgeiness = Math.abs(noise2D(fx * 5, fy * 5, 0) - noise2D(fx * 5, fy * 5, t * 0.02));
        grid[i + 2] = edgeiness * 0.3 + (1 - grid[i + 1]) * 0.15;
        // API calls: proportional to density with temporal variation
        grid[i + 3] = (grid[i + 1] * 200 + noise2D(fx * 6, fy * 6, t * 0.06) * 50) * (0.8 + lcg() * 0.4);
      }
    }
    steps.push(grid);
  }
  return steps;
})();
// ============================================================================
// CACHE LAYER — All cacheable outputs stored here
// Audit: no new THREE.XxxGeometry() in per-frame/tick paths
// Hit/miss counters for diagnostic panel
// ============================================================================
const CACHE = {
  // Terrain geometry cache: keyed by time step index
  terrainGeometries: new Map(),
  terrainHits: 0,
  terrainMisses: 0,
  // River geometry cache: keyed by "timeStep_hash"
  riverGeometries: new Map(),
  riverHits: 0,
  riverMisses: 0,
  // World-to-grid coordinate transform cache (per frame, cleared each frame)
  gridTransforms: new Map(),
  gridHits: 0,
  gridMisses: 0,
  // Vertex color data cache: keyed by time step
  vertexColors: new Map(),
  colorHits: 0,
  colorMisses: 0,
  stats() {
    return {
      terrain: { hits: this.terrainHits, misses: this.terrainMisses, rate: this.rate(this.terrainHits, this.terrainMisses) },
      rivers: { hits: this.riverHits, misses: this.riverMisses, rate: this.rate(this.riverHits, this.riverMisses) },
      grid: { hits: this.gridHits, misses: this.gridMisses, rate: this.rate(this.gridHits, this.gridMisses) },
      colors: { hits: this.colorHits, misses: this.colorMisses, rate: this.rate(this.colorHits, this.colorMisses) },
    };
  },
  rate(h, m) { const t = h + m; return t === 0 ? '0%' : Math.round(h / t * 100) + '%'; },
  resetFrameCache() { this.gridTransforms.clear(); },
};
// ============================================================================
// THREE.JS SCENE SETUP
// ============================================================================
const container = document.body;
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap DPI for mobile
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color('#0a0a18');
scene.fog = new THREE.Fog('#0a0a18', 15, 60);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 200);
camera.position.set(12, 8, 14);
camera.lookAt(0, 0, 0);
// OrbitControls with smooth damping
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 4;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI / 2 + 0.1; // Slightly below horizon
controls.target.set(0, 0, 0);
controls.autoRotate = false;
controls.autoRotateSpeed = 0.5;
controls.update();
// ============================================================================
// LIGHTING
// ============================================================================
const ambientLight = new THREE.AmbientLight('#334466', 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight('#ffeedd', 3.5);
sunLight.position.set(15, 20, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 80;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0003;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight('#8899cc', 0.8);
fillLight.position.set(-5, 2, -5);
scene.add(fillLight);
// ============================================================================
// TERRAIN — Heightfield BufferGeometry from time-series data
// Elevation = revenue, VertexColor = user density (vegetation gradient)
// Cached per time step; swap buffer on slider change, never rebuild per tick
// ============================================================================
const TERRAIN_SIZE = 16;
const MAX_HEIGHT = 4.5;
// Build and cache terrain geometry for a given time step
function buildTerrainGeometry(timeStep) {
  if (CACHE.terrainGeometries.has(timeStep)) {
    CACHE.terrainHits++;
    return CACHE.terrainGeometries.get(timeStep);
  }
  CACHE.terrainMisses++;
  const data = DATA[timeStep];
  const segments = GRID_SIZE - 1;
  const halfSize = TERRAIN_SIZE / 2;
  const positions = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  const colors = new Float32Array(GRID_SIZE * GRID_SIZE * 3);
  // Vegetation color palette: brown (low density) → green (mid) → yellow-green (high)
  const densityToColor = (d) => {
    // d is 0..1, map to brown→green→lime gradient
    if (d < 0.3) {
      const t = d / 0.3;
      return [0.24 * t + 0.1 * (1 - t), 0.19 * t + 0.05 * (1 - t), 0.14 * t + 0.03 * (1 - t)]; // dark brown → brown
    } else if (d < 0.6) {
      const t = (d - 0.3) / 0.3;
      return [0.3 * (1 - t) + 0.0 * t, 0.42 * (1 - t) + 0.65 * t, 0.18 * (1 - t) + 0.22 * t]; // brown → green
    } else {
      const t = (d - 0.6) / 0.4;
      return [0.0 + 0.4 * t, 0.65 + 0.35 * t, 0.22 + 0.3 * t]; // green → lime
    }
  };
  for (let y = 0; y < GRID_SIZE; y++) {
    for (let x = 0; x < GRID_SIZE; x++) {
      const idx = y * GRID_SIZE + x;
      const dataIdx = idx * 4;
      const revenue = data[dataIdx];       // 0..~1
      const density = data[dataIdx + 1];   // 0..~1
      const px = (x / segments - 0.5) * TERRAIN_SIZE;
      const py = revenue * MAX_HEIGHT;
      const pz = (y / segments - 0.5) * TERRAIN_SIZE;
      positions[idx * 3] = px;
      positions[idx * 3 + 1] = py;
      positions[idx * 3 + 2] = pz;
      const [r, g, b] = densityToColor(density);
      colors[idx * 3] = r;
      colors[idx * 3 + 1] = g;
      colors[idx * 3 + 2] = b;
    }
  }
  // Build index buffer for the grid
  const indices = [];
  for (let y = 0; y < GRID_SIZE - 1; y++) {
    for (let x = 0; x < GRID_SIZE - 1; x++) {
      const a = y * GRID_SIZE + x;
      const b = a + 1;
      const c = a + GRID_SIZE;
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
  // Store cached vertex color data for reuse
  if (!CACHE.vertexColors.has(timeStep)) {
    CACHE.vertexColors.set(timeStep, new Float32Array(colors));
    CACHE.colorMisses++;
  }
  CACHE.terrainGeometries.set(timeStep, geom);
  return geom;
}
// Terrain mesh (created once, geometry swapped)
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.6,
  metalness: 0.1,
  flatShading: false,
});
const terrainMesh = new THREE.Mesh(buildTerrainGeometry(0), terrainMaterial);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// Wireframe overlay for structure visibility
const wireframeMaterial = new THREE.MeshBasicMaterial({
  color: '#1a2a3a',
  wireframe: true,
  transparent: true,
  opacity: 0.08,
});
const wireframeMesh = new THREE.Mesh(terrainMesh.geometry, wireframeMaterial);
terrainMesh.add(wireframeMesh);
// ============================================================================
// RIVERS — TubeGeometry tracing error anomaly paths
// Red channels carved into terrain where error rate exceeds threshold
// Debounced rebuild (200ms) on slider change; TubeGeometry cached
// ============================================================================
let riverGroup = new THREE.Group();
scene.add(riverGroup);
let riverDebounceTimer = null;
function findErrorPaths(data) {
  // Find contiguous regions where error rate > 0.25 (high anomaly)
  // Return array of path point arrays for river geometry
  const threshold = 0.25;
  const visited = new Uint8Array(GRID_SIZE * GRID_SIZE);
  const paths = [];
  const segments = GRID_SIZE - 1;
  const halfSize = TERRAIN_SIZE / 2;
  // Find seed points above threshold
  for (let y = 0; y < GRID_SIZE; y++) {
    for (let x = 0; x < GRID_SIZE; x++) {
      const idx = y * GRID_SIZE + x;
      if (visited[idx]) continue;
      const errorRate = data[idx * 4 + 2];
      if (errorRate < threshold) continue;
      // Trace path downhill along error gradient
      const path = [];
      let cx = x, cy = y;
      let steps = 0;
      const maxSteps = 80;
      while (steps < maxSteps && cx >= 0 && cx < GRID_SIZE && cy >= 0 && cy < GRID_SIZE) {
        const ci = cy * GRID_SIZE + cx;
        if (visited[ci] && steps > 0) break;
        visited[ci] = 1;
        const px = (cx / segments - 0.5) * TERRAIN_SIZE;
        const py = data[ci * 4] * MAX_HEIGHT + 0.08; // Slightly above terrain
        const pz = (cy / segments - 0.5) * TERRAIN_SIZE;
        path.push(new THREE.Vector3(px, py, pz));
        // Flow downhill: choose neighbor with lowest revenue (valley)
        let bestDx = 0, bestDy = 0, bestVal = Infinity;
        for (const [dx, dy] of [[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]) {
          const nx = cx + dx, ny = cy + dy;
          if (nx < 0 || nx >= GRID_SIZE || ny < 0 || ny >= GRID_SIZE) continue;
          const val = data[(ny * GRID_SIZE + nx) * 4]; // revenue height
          if (val < bestVal) { bestVal = val; bestDx = dx; bestDy = dy; }
        }
        if (bestDx === 0 && bestDy === 0) break;
        cx += bestDx;
        cy += bestDy;
        steps++;
      }
      if (path.length > 3) paths.push(path);
    }
  }
  return paths;
}
function buildRiverGeometry(timeStep) {
  const cacheKey = `river_${timeStep}`;
  if (CACHE.riverGeometries.has(cacheKey)) {
    CACHE.riverHits++;
    return CACHE.riverGeometries.get(cacheKey);
  }
  CACHE.riverMisses++;
  const data = DATA[timeStep];
  const paths = findErrorPaths(data);
  const group = new THREE.Group();
  // Limit to top 8 longest paths to avoid visual clutter
  const sortedPaths = paths.sort((a, b) => b.length - a.length).slice(0, 8);
  for (const path of sortedPaths) {
    if (path.length < 4) continue;
    const curve = new THREE.CatmullRomCurve3(path);
    const tubeGeom = new THREE.TubeGeometry(curve, Math.min(path.length * 2, 60), 0.06, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({
      color: '#ff3333',
      roughness: 0.3,
      metalness: 0.2,
      emissive: '#330000',
      emissiveIntensity: 0.4,
    });
    const tube = new THREE.Mesh(tubeGeom, tubeMat);
    tube.castShadow = true;
    group.add(tube);
  }
  CACHE.riverGeometries.set(cacheKey, group);
  return group;
}
function updateRivers(timeStep) {
  // Debounce: clear previous pending rebuild, schedule new one
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    // Remove old river group children
    while (riverGroup.children.length > 0) {
      const child = riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
      riverGroup.remove(child);
    }
    // Build new river geometry (cached)
    const newGroup = buildRiverGeometry(timeStep);
    while (newGroup.children.length > 0) {
      riverGroup.add(newGroup.children[0]);
    }
  }, 200);
}
// ============================================================================
// PARTICLES — BufferGeometry with position array reuse
// API call data flows as golden particle trails across the landscape
// No per-frame allocations: reuse position array, update in place
// ============================================================================
const PARTICLE_COUNT = 800;
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleVelocities = new Float32Array(PARTICLE_COUNT * 3); // Velocity vectors for smooth motion
const particleLifetimes = new Float32Array(PARTICLE_COUNT);
const particleMaxLifetime = 3.0; // seconds before respawn
// Initialize particles at random positions on terrain at time step 0
function initParticles(timeStep) {
  const data = DATA[timeStep];
  const segments = GRID_SIZE - 1;
  const halfSize = TERRAIN_SIZE / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const gx = Math.random() * (GRID_SIZE - 1);
    const gy = Math.random() * (GRID_SIZE - 1);
    const gxi = Math.floor(gx);
    const gyi = Math.floor(gy);
    const fx = gx - gxi;
    const fy = gy - gyi;
    // Bilinear interpolation for height at fractional grid position
    const h00 = data[(gyi * GRID_SIZE + gxi) * 4];
    const h10 = data[(gyi * GRID_SIZE + Math.min(gxi + 1, GRID_SIZE - 1)) * 4];
    const h01 = data[(Math.min(gyi + 1, GRID_SIZE - 1) * GRID_SIZE + gxi) * 4];
    const h11 = data[(Math.min(gyi + 1, GRID_SIZE - 1) * GRID_SIZE + Math.min(gxi + 1, GRID_SIZE - 1)) * 4];
    const height = (h00 * (1 - fx) * (1 - fy) + h10 * fx * (1 - fy) + h01 * (1 - fx) * fy + h11 * fx * fy) * MAX_HEIGHT;
    particlePositions[i * 3] = (gx / segments - 0.5) * TERRAIN_SIZE;
    particlePositions[i * 3 + 1] = height + 0.3 + Math.random() * 1.5;
    particlePositions[i * 3 + 2] = (gy / segments - 0.5) * TERRAIN_SIZE;
    // Random velocity: float along terrain surface
    const angle = Math.random() * Math.PI * 2;
    const speed = 0.3 + Math.random() * 1.2;
    particleVelocities[i * 3] = Math.cos(angle) * speed;
    particleVelocities[i * 3 + 1] = (Math.random() - 0.5) * 0.2;
    particleVelocities[i * 3 + 2] = Math.sin(angle) * speed;
    particleLifetimes[i] = Math.random() * particleMaxLifetime;
  }
}
// Particle geometry: created ONCE, position array reused every frame
const particleGeometry = new THREE.BufferGeometry();
particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
// Size attribute for fading
const particleSizes = new Float32Array(PARTICLE_COUNT);
for (let i = 0; i < PARTICLE_COUNT; i++) {
  particleSizes[i] = 0.04 + Math.random() * 0.06;
}
particleGeometry.setAttribute('size', new THREE.BufferAttribute(particleSizes, 1));
const particleMaterial = new THREE.PointsMaterial({
  color: '#ffd700',
  size: 0.12,
  blending: THREE.AdditiveBlending,
  depthWrite: false,
  transparent: true,
  opacity: 0.7,
  sizeAttenuation: true,
});
const particles = new THREE.Points(particleGeometry, particleMaterial);
scene.add(particles);
initParticles(0);
// Update particles each frame — no allocations, reuse position array
function updateParticles(deltaTime, timeStep) {
  const data = DATA[timeStep];
  const segments = GRID_SIZE - 1;
  const halfSize = TERRAIN_SIZE / 2;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Update lifetime
    particleLifetimes[i] += deltaTime;
    if (particleLifetimes[i] > particleMaxLifetime) {
      // Respawn at random terrain position
      const gx = Math.random() * (GRID_SIZE - 1);
      const gy = Math.random() * (GRID_SIZE - 1);
      const gxi = Math.floor(gx);
      const gyi = Math.floor(gy);
      const fx = gx - gxi;
      const fy = gy - gyi;
      const h00 = data[(gyi * GRID_SIZE + gxi) * 4];
      const h10 = data[(gyi * GRID_SIZE + Math.min(gxi + 1, GRID_SIZE - 1)) * 4];
      const h01 = data[(Math.min(gyi + 1, GRID_SIZE - 1) * GRID_SIZE + gxi) * 4];
      const h11 = data[(Math.min(gyi + 1, GRID_SIZE - 1) * GRID_SIZE + Math.min(gxi + 1, GRID_SIZE - 1)) * 4];
      const height = (h00 * (1 - fx) * (1 - fy) + h10 * fx * (1 - fy) + h01 * (1 - fx) * fy + h11 * fx * fy) * MAX_HEIGHT;
      particlePositions[i * 3] = (gx / segments - 0.5) * TERRAIN_SIZE;
      particlePositions[i * 3 + 1] = height + 0.3 + Math.random() * 0.8;
      particlePositions[i * 3 + 2] = (gy / segments - 0.5) * TERRAIN_SIZE;
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.3 + Math.random() * 1.2;
      particleVelocities[i * 3] = Math.cos(angle) * speed;
      particleVelocities[i * 3 + 1] = (Math.random() - 0.5) * 0.15;
      particleVelocities[i * 3 + 2] = Math.sin(angle) * speed;
      particleLifetimes[i] = 0;
      particleSizes[i] = 0.04 + Math.random() * 0.06;
    }
    // Move particle
    particlePositions[i * 3] += particleVelocities[i * 3] * deltaTime;
    particlePositions[i * 3 + 1] += particleVelocities[i * 3 + 1] * deltaTime;
    particlePositions[i * 3 + 2] += particleVelocities[i * 3 + 2] * deltaTime;
    // Clamp to terrain bounds, wrap around
    const px = particlePositions[i * 3];
    const pz = particlePositions[i * 3 + 2];
    if (Math.abs(px) > halfSize || Math.abs(pz) > halfSize) {
      // Bounce: reverse velocity component
      if (Math.abs(px) > halfSize) particleVelocities[i * 3] *= -1;
      if (Math.abs(pz) > halfSize) particleVelocities[i * 3 + 2] *= -1;
      particlePositions[i * 3] = Math.max(-halfSize, Math.min(halfSize, px));
      particlePositions[i * 3 + 2] = Math.max(-halfSize, Math.min(halfSize, pz));
    }
  }
  // Mark position attribute as needing update (no new allocation)
  particleGeometry.attributes.position.needsUpdate = true;
  particleGeometry.attributes.size.needsUpdate = true;
}
// ============================================================================
// GROUND PLANE — Reference grid under terrain
// ============================================================================
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE / 2 + 2, 32, 16, 64, '#1a2a3a', '#0d1520');
gridHelper.position.y = -0.05;
scene.add(gridHelper);
// ============================================================================
// HOVER DETECTION — Raycaster with memoized grid transform
// ============================================================================
const raycaster = new THREE.Raycaster();
raycaster.far = 50;
const mouse = new THREE.Vector2();
const hoverDisplay = document.getElementById('hoverData');
function worldToGrid(worldPos) {
  // Memoize per-frame grid transforms
  const key = `${worldPos.x.toFixed(4)},${worldPos.z.toFixed(4)}`;
  if (CACHE.gridTransforms.has(key)) {
    CACHE.gridHits++;
    return CACHE.gridTransforms.get(key);
  }
  CACHE.gridMisses++;
  const halfSize = TERRAIN_SIZE / 2;
  const segments = GRID_SIZE - 1;
  const gx = Math.round((worldPos.x / halfSize * 0.5 + 0.5) * segments);
  const gy = Math.round((worldPos.z / halfSize * 0.5 + 0.5) * segments);
  const result = {
    x: Math.max(0, Math.min(GRID_SIZE - 1, gx)),
    y: Math.max(0, Math.min(GRID_SIZE - 1, gy)),
  };
  CACHE.gridTransforms.set(key, result);
  return result;
}
function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
}
window.addEventListener('mousemove', onMouseMove, { passive: true });
window.addEventListener('touchmove', (e) => {
  if (e.touches.length === 1) {
    mouse.x = (e.touches[0].clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.touches[0].clientY / window.innerHeight) * 2 + 1;
  }
}, { passive: true });
function updateHover(currentTimeStep) {
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObject(terrainMesh);
  if (intersects.length > 0) {
    const point = intersects[0].point;
    const grid = worldToGrid(point);
    const dataIdx = (grid.y * GRID_SIZE + grid.x) * 4;
    const d = DATA[currentTimeStep];
    if (d) {
      const rev = (d[dataIdx] * 100).toFixed(0);
      const dens = (d[dataIdx + 1] * 100).toFixed(0);
      const err = (d[dataIdx + 2] * 100).toFixed(1);
      hoverDisplay.textContent = `Rev:${rev}% Dens:${dens}% Err:${err}%`;
    }
  } else {
    hoverDisplay.textContent = '--';
  }
}
// ============================================================================
// CAMERA BOOKMARKS — Ctrl+1..4 to save, 1..4 to recall
// ============================================================================
const bookmarks = [
  { name: 'Overview', position: new THREE.Vector3(12, 8, 14), target: new THREE.Vector3(0, 2, 0) },
  { name: 'Top-down', position: new THREE.Vector3(0, 18, 0.1), target: new THREE.Vector3(0, 0, 0) },
  { name: 'Close-up', position: new THREE.Vector3(3, 3, 4), target: new THREE.Vector3(0, 1.5, 0) },
  { name: 'Side', position: new THREE.Vector3(16, 2, 0), target: new THREE.Vector3(0, 1, 0) },
];
function updateBookmarkUI() {
  const list = document.getElementById('bookmarkList');
  list.innerHTML = bookmarks.map((b, i) =>
    `<div class="bookmark-row">
      <span class="bookmark-name">${i + 1}. ${b.name}</span>
      <button class="btn" data-recall="${i}">Go</button>
    </div>`
  ).join('');
  // Attach event listeners
  list.querySelectorAll('[data-recall]').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = parseInt(btn.dataset.recall);
      recallBookmark(idx);
    });
  });
}
function recallBookmark(index) {
  if (index < 0 || index >= bookmarks.length) return;
  const bm = bookmarks[index];
  // Smooth animate camera to bookmark position
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = bm.position.clone();
  const endTarget = bm.target.clone();
  const duration = 800; // ms
  const startTime = performance.now();
  function animateBookmark(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed / duration, 1.0);
    // Ease in-out cubic
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animateBookmark);
    }
  }
  requestAnimationFrame(animateBookmark);
}
window.addEventListener('keydown', (event) => {
  // Save bookmark: Ctrl+1..4
  if (event.ctrlKey && event.key >= '1' && event.key <= '4') {
    event.preventDefault();
    const idx = parseInt(event.key) - 1;
    bookmarks[idx] = {
      name: bookmarks[idx].name,
      position: camera.position.clone(),
      target: controls.target.clone(),
    };
    updateBookmarkUI();
  }
  // Recall bookmark: 1..4 (no modifier, when not typing in input)
  if (!event.ctrlKey && !event.metaKey && !event.altKey
      && event.key >= '1' && event.key <= '4'
      && document.activeElement === document.body) {
    event.preventDefault();
    recallBookmark(parseInt(event.key) - 1);
  }
});
updateBookmarkUI();
// ============================================================================
// TIME SLIDER — Swap cached terrain geometry, debounce rivers
// ============================================================================
const timeSlider = document.getElementById('timeSlider');
timeSlider.max = TIME_STEPS - 1;
timeSlider.value = 0;
const timeDisplay = document.getElementById('timeDisplay');
let currentTimeStep = 0;
let isPlaying = false;
let playDirection = 1;
function setTimeStep(step) {
  step = Math.max(0, Math.min(TIME_STEPS - 1, step));
  if (step === currentTimeStep) return;
  currentTimeStep = step;
  timeSlider.value = step;
  const day = step + 1;
  const month = Math.floor(step / 30) + 1;
  const dayOfMonth = (step % 30) + 1;
  timeDisplay.textContent = `M${month} D${dayOfMonth} (Day ${day})`;
  // Swap terrain geometry (cached — no new constructor call)
  const newGeom = buildTerrainGeometry(step);
  if (terrainMesh.geometry !== newGeom) {
    terrainMesh.geometry = newGeom;
    wireframeMesh.geometry = newGeom;
  }
  // Update rivers (debounced, cached)
  updateRivers(step);
}
timeSlider.addEventListener('input', () => {
  setTimeStep(parseInt(timeSlider.value));
});
// Play/Pause button
const btnPlay = document.getElementById('btnPlay');
btnPlay.addEventListener('click', () => {
  isPlaying = !isPlaying;
  btnPlay.textContent = isPlaying ? '⏸' : '▶';
  btnPlay.classList.toggle('active', isPlaying);
});
// Auto-rotate button
const btnAutoRotate = document.getElementById('btnAutoRotate');
btnAutoRotate.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAutoRotate.classList.toggle('active', controls.autoRotate);
});
// ============================================================================
// CACHE DIAGNOSTIC PANEL — Live hit/miss rates
// ============================================================================
function updateCachePanel() {
  const stats = CACHE.stats();
  document.getElementById('cacheStats').innerHTML = `
    <div class="cache-row"><span>Terrain</span><span class="${stats.terrain.rate === '100%' ? 'cache-hit' : 'cache-miss'}">${stats.terrain.rate} (H:${stats.terrain.hits} M:${stats.terrain.misses})</span></div>
    <div class="cache-row"><span>Rivers</span><span class="${stats.rivers.rate === '100%' ? 'cache-hit' : 'cache-miss'}">${stats.rivers.rate} (H:${stats.rivers.hits} M:${stats.rivers.misses})</span></div>
    <div class="cache-row"><span>Grid Tx</span><span class="${stats.grid.rate === '100%' ? 'cache-hit' : 'cache-miss'}">${stats.grid.rate} (H:${stats.grid.hits} M:${stats.grid.misses})</span></div>
    <div class="cache-row"><span>Colors</span><span class="${stats.colors.rate === '100%' ? 'cache-hit' : 'cache-miss'}">${stats.colors.rate} (H:${stats.colors.hits} M:${stats.colors.misses})</span></div>
  `;
}
// ============================================================================
// RENDER LOOP — FPS tracking, animation, particle update
// ============================================================================
let frameCount = 0;
let lastFpsUpdate = performance.now();
let fps = 0;
function animate(timestamp) {
  requestAnimationFrame(animate);
  const deltaTime = Math.min((timestamp - lastFpsUpdate) / 1000, 0.1); // Cap delta to avoid spiral
  lastFpsUpdate = timestamp;
  // FPS counter
  frameCount++;
  if (frameCount % 30 === 0) {
    const now = performance.now();
    fps = Math.round(30000 / (now - lastFpsUpdate + 1));
    document.getElementById('fpsDisplay').textContent = fps;
  }
  // Play animation
  if (isPlaying) {
    const nextStep = currentTimeStep + playDirection;
    if (nextStep >= TIME_STEPS) {
      playDirection = -1;
      setTimeStep(TIME_STEPS - 2);
    } else if (nextStep < 0) {
      playDirection = 1;
      setTimeStep(1);
    } else {
      setTimeStep(nextStep);
    }
  }
  // Update particles (reuses position array, no allocations)
  updateParticles(deltaTime, currentTimeStep);
  // Update hover
  updateHover(currentTimeStep);
  // Update controls
  controls.update();
  // Render
  renderer.render(scene, camera);
  // Update diagnostics every 120 frames
  if (frameCount % 120 === 0) {
    updateCachePanel();
    document.getElementById('particleCount').textContent = PARTICLE_COUNT;
    const triCount = terrainMesh.geometry.index
      ? Math.floor(terrainMesh.geometry.index.count / 3)
      : Math.floor(terrainMesh.geometry.attributes.position.count / 3);
    document.getElementById('triCount').textContent = triCount;
  }
  // Clear per-frame cache
  CACHE.resetFrameCache();
}
// ============================================================================
// RESIZE HANDLER — Responsive viewport
// ============================================================================
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  // Reduce pixel ratio on narrow screens for performance
  const isMobile = window.innerWidth < 768;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
});
// ============================================================================
// INITIALIZATION
// ============================================================================
// Initialize river display
updateRivers(0);
// Force first cache panel update
updateCachePanel();
document.getElementById('particleCount').textContent = PARTICLE_COUNT;
const initTriCount = terrainMesh.geometry.index
  ? Math.floor(terrainMesh.geometry.index.count / 3)
  : Math.floor(terrainMesh.geometry.attributes.position.count / 3);
document.getElementById('triCount').textContent = initTriCount;
// Start render loop
requestAnimationFrame(animate);
// Log startup
console.log('3D Data Terrain Explorer ready');
console.log(`Grid: ${GRID_SIZE}x${GRID_SIZE}, Time steps: ${TIME_STEPS}, Particles: ${PARTICLE_COUNT}`);
console.log('Controls: drag=orbit, scroll=zoom, right-drag=pan, 1-4=bookmarks, Ctrl+1-4=save bookmark');
console.log('Performance: terrain geometry cached, rivers debounced (200ms), particles reuse position buffer');
</script>
</body>
</html>
```