<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { overflow: hidden; background: #0a0a14; font-family: 'Segoe UI', system-ui, sans-serif; color: #ccc; }
  #canvas-container { position: fixed; inset: 0; z-index: 0; }
  canvas { display: block; }
  #ui { position: fixed; z-index: 10; pointer-events: none; }
  #ui > * { pointer-events: auto; }
  #panel { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: rgba(10,10,30,0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 16px 20px; display: flex; gap: 18px; align-items: center; z-index: 10; }
  #time-slider { width: 260px; accent-color: #4fc3f7; cursor: pointer; }
  #time-label { font-variant-numeric: tabular-nums; min-width: 70px; text-align: center; font-size: 13px; color: #81d4fa; }
  .btn { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.18); color: #ccc; padding: 6px 14px; border-radius: 8px; cursor: pointer; font-size: 12px; transition: all 0.2s; white-space: nowrap; }
  .btn:hover { background: rgba(255,255,255,0.16); border-color: rgba(255,255,255,0.35); color: #fff; }
  .btn.active { background: rgba(79,195,247,0.2); border-color: #4fc3f7; color: #4fc3f7; }
  #bookmarks { position: fixed; top: 20px; right: 20px; display: flex; flex-direction: column; gap: 6px; z-index: 10; }
  #legend { position: fixed; top: 20px; left: 20px; background: rgba(10,10,30,0.8); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 12px 16px; z-index: 10; font-size: 11px; line-height: 1.7; }
  .legend-row { display: flex; align-items: center; gap: 8px; }
  .legend-swatch { width: 14px; height: 14px; border-radius: 3px; flex-shrink: 0; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="legend">
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to top,#1a5c2a,#6db33f,#f5e6a3,#c4a35a,#e8e8e8)"></span> Elevation (revenue)</div>
  <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#1a3a1a,#3d7a3d,#8bc34a)"></span> User density</div>
  <div class="legend-row"><span class="legend-swatch" style="background:#ef5350;border-radius:50%"></span> Error rivers</div>
  <div class="legend-row"><span class="legend-swatch" style="background:#ffd54f;border-radius:50%"></span> API traffic</div>
</div>
<div id="bookmarks"></div>
<div id="panel">
  <button class="btn" id="btn-play">Play</button>
  <button class="btn" id="btn-auto-rotate">Auto-rotate</button>
  <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
  <span id="time-label">T0</span>
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
// === Value Noise (interpolated gradient noise) ===
// Replaces simplex — smoother gradients, lower computational cost
class ValueNoise {
  constructor(seed = 42) {
    this.perm = new Uint8Array(512);
    this.grad = new Float32Array(512);
    let s = seed | 0;
    const mix = (x) => { x = ((x >>> 0) ^ (x << 13)) * 15731; return (x ^ (x >>> 16)) & 0xff; };
    for (let i = 0; i < 256; i++) {
      this.perm[i] = mix(s + i * 127 + 31);
      this.grad[i] = (this.perm[i] / 255) * 2 - 1;
    }
    for (let i = 0; i < 256; i++) {
      this.perm[i + 256] = this.perm[i];
      this.grad[i + 256] = this.grad[i];
    }
  }
  fade(t) { return t * t * t * (t * (t * 6 - 15) + 10); }
  lerp(a, b, t) { return a + t * (b - a); }
  noise2D(x, y) {
    const X = Math.floor(x) & 255;
    const Y = Math.floor(y) & 255;
    const xf = x - Math.floor(x);
    const yf = y - Math.floor(y);
    const u = this.fade(xf);
    const v = this.fade(yf);
    const p = this.perm;
    const g = this.grad;
    const aa = g[p[p[X] + Y]]; const ba = g[p[p[X + 1] + Y]];
    const ab = g[p[p[X] + Y + 1]]; const bb = g[p[p[X + 1] + Y + 1]];
    return this.lerp(
      this.lerp(aa, ba, u),
      this.lerp(ab, bb, u),
      v
    );
  }
  fbm(x, y, octaves = 4, lacunarity = 2.0, gain = 0.5) {
    let value = 0, amplitude = 1, frequency = 1, maxValue = 0;
    for (let i = 0; i < octaves; i++) {
      value += amplitude * this.noise2D(x * frequency, y * frequency);
      maxValue += amplitude;
      amplitude *= gain;
      frequency *= lacunarity;
    }
    return value / maxValue;
  }
}
// === Synthetic Data Generator ===
// Produces time-series: revenue (elevation), user density (vertex color), error rate (rivers), api calls (particles)
function generateDataset(timesteps, gridSize) {
  const noise = new ValueNoise(137);
  const data = [];
  for (let t = 0; t < timesteps; t++) {
    const timeFactor = t / (timesteps - 1);
    const height = new Float32Array(gridSize * gridSize);
    const userDensity = new Float32Array(gridSize * gridSize);
    const errorRate = new Float32Array(gridSize * gridSize);
    const apiTraffic = new Float32Array(gridSize * gridSize);
    for (let iy = 0; iy < gridSize; iy++) {
      for (let ix = 0; ix < gridSize; ix++) {
        const idx = iy * gridSize + ix;
        const nx = ix / gridSize * 4;
        const ny = iy / gridSize * 4;
        const base = noise.fbm(nx + timeFactor * 0.5, ny, 5, 2.0, 0.55);
        // Revenue hills grow over time in center region
        const cx = (ix / gridSize - 0.5) * 2;
        const cy = (iy / gridSize - 0.5) * 2;
        const centerBump = Math.exp(-(cx * cx + cy * cy) * 2.5) * (0.6 + timeFactor * 0.4);
        height[idx] = base * 0.7 + centerBump * 0.5 + 0.15;
        // User density: higher near center, grows over time
        userDensity[idx] = Math.exp(-(cx * cx + cy * cy) * 1.8) * (0.4 + timeFactor * 0.6);
        // Error rate: inverse of density + noise (edges have more errors)
        errorRate[idx] = (1 - userDensity[idx]) * 0.6 + Math.abs(noise.noise2D(nx * 3 + 5, ny * 3 + 5)) * 0.4;
        errorRate[idx] = Math.max(0, Math.min(1, errorRate[idx]));
        // API traffic: follows user density with lag
        const tLag = Math.max(0, t - 1) / (timesteps - 1);
        const densLag = Math.exp(-(cx * cx + cy * cy) * 1.8) * (0.4 + tLag * 0.6);
        apiTraffic[idx] = densLag * 0.8 + Math.abs(noise.noise2D(nx * 2 + 2, ny * 2 + 2)) * 0.2;
      }
    }
    data.push({ height, userDensity, errorRate, apiTraffic });
  }
  return data;
}
// === River Tracer ===
// Traces error paths across terrain using gradient ascent on error field with Map-keyed direction lookup
class RiverTracer {
  constructor(gridSize) {
    this.gridSize = gridSize;
    // 8-directional flow with Map lookup (fixes array-comparison bug)
    this.flowDirs = [
      { dx: -1, dy: -1 }, { dx: 0, dy: -1 }, { dx: 1, dy: -1 },
      { dx: -1, dy: 0 },                      { dx: 1, dy: 0 },
      { dx: -1, dy: 1 },  { dx: 0, dy: 1 },  { dx: 1, dy: 1 }
    ];
    this.flowMap = new Map();
    for (const d of this.flowDirs) {
      this.flowMap.set(`${d.dx},${d.dy}`, d);
    }
  }
  trace(errorField, heightField, startX, startY, maxSteps = 200) {
    const path = [];
    let cx = startX, cy = startY;
    const visited = new Set();
    for (let step = 0; step < maxSteps; step++) {
      if (cx < 1 || cx >= this.gridSize - 1 || cy < 1 || cy >= this.gridSize - 1) break;
      const key = `${cx},${cy}`;
      if (visited.has(key)) break;
      visited.add(key);
      path.push({ x: cx, y: cy });
      // Gradient ascent on error field
      let bestErr = errorField[cy * this.gridSize + cx];
      let bestDir = null;
      for (const d of this.flowDirs) {
        const nx = cx + d.dx, ny = cy + d.dy;
        if (nx < 0 || nx >= this.gridSize || ny < 0 || ny >= this.gridSize) continue;
        const err = errorField[ny * this.gridSize + nx];
        if (err > bestErr) {
          bestErr = err;
          bestDir = d;
        }
      }
      if (!bestDir) break;
      cx += bestDir.dx;
      cy += bestDir.dy;
    }
    return path;
  }
  findRiverSources(errorField, heightField, threshold = 0.65, minSpacing = 8) {
    const sources = [];
    for (let iy = minSpacing; iy < this.gridSize - minSpacing; iy += minSpacing) {
      for (let ix = minSpacing; ix < this.gridSize - minSpacing; ix += minSpacing) {
        const idx = iy * this.gridSize + ix;
        if (errorField[idx] > threshold) {
          // Check local maximum
          let isMax = true;
          for (const d of this.flowDirs) {
            const nx = ix + d.dx, ny = iy + d.dy;
            if (nx >= 0 && nx < this.gridSize && ny >= 0 && ny < this.gridSize) {
              if (errorField[ny * this.gridSize + nx] > errorField[idx]) { isMax = false; break; }
            }
          }
          if (isMax) sources.push({ x: ix, y: iy });
        }
      }
    }
    return sources.slice(0, 6);
  }
}
// === Terrain Builder with Geometry Caching ===
class TerrainBuilder {
  constructor(gridSize, worldScale) {
    this.gridSize = gridSize;
    this.worldScale = worldScale;
    this.cache = new Map(); // timestep -> { positions, colors }
  }
  build(heightData, userDensityData, timestep) {
    if (this.cache.has(timestep)) return this.cache.get(timestep);
    const gs = this.gridSize;
    const ws = this.worldScale;
    const cellSize = ws / (gs - 1);
    const half = ws / 2;
    const positions = new Float32Array(gs * gs * 3);
    const colors = new Float32Array(gs * gs * 3);
    for (let iy = 0; iy < gs; iy++) {
      for (let ix = 0; ix < gs; ix++) {
        const idx = iy * gs + ix;
        const pi = idx * 3;
        const h = heightData[idx] * ws * 0.4;
        positions[pi] = ix * cellSize - half;
        positions[pi + 1] = h;
        positions[pi + 2] = iy * cellSize - half;
        // Vertex color: blend elevation gradient (brown->green->white) with user density (green intensity)
        const dens = userDensityData[idx];
        const elev = heightData[idx];
        // Low elevation: dark green/brown. Mid: bright green. High: rocky/white.
        let r, g, b;
        if (elev < 0.2) { r = 0.15 + elev * 0.3; g = 0.25 + elev * 0.5; b = 0.12; }
        else if (elev < 0.5) { r = 0.2 + (elev - 0.2) * 0.4; g = 0.35 + (elev - 0.2) * 1.0; b = 0.1 + (elev - 0.2) * 0.2; }
        else if (elev < 0.75) { r = 0.32 + (elev - 0.5) * 1.6; g = 0.65 + (elev - 0.5) * 0.6; b = 0.16 + (elev - 0.5) * 0.8; }
        else { r = 0.72 + (elev - 0.75) * 1.12; g = 0.8 + (elev - 0.75) * 0.8; b = 0.36 + (elev - 0.75) * 2.56; }
        // User density boosts green channel
        g += dens * 0.3;
        colors[pi] = Math.min(1, r);
        colors[pi + 1] = Math.min(1, g);
        colors[pi + 2] = Math.min(1, b);
      }
    }
    const entry = { positions, colors };
    this.cache.set(timestep, entry);
    return entry;
  }
  buildIndices() {
    const gs = this.gridSize;
    const indices = [];
    for (let iy = 0; iy < gs - 1; iy++) {
      for (let ix = 0; ix < gs - 1; ix++) {
        const a = iy * gs + ix;
        const b = a + 1;
        const c = a + gs;
        const d = c + 1;
        indices.push(a, b, d);
        indices.push(a, d, c);
      }
    }
    return new Uint32Array(indices);
  }
}
// === Particle System with BufferGeometry Reuse ===
class ParticleSystem {
  constructor(maxParticles, gridSize, worldScale, getTerrainHeight) {
    this.maxParticles = maxParticles;
    this.gridSize = gridSize;
    this.worldScale = worldScale;
    this.getTerrainHeight = getTerrainHeight;
    this.positions = new Float32Array(maxParticles * 3);
    this.colors = new Float32Array(maxParticles * 3);
    this.sizes = new Float32Array(maxParticles);
    this.alive = new Uint8Array(maxParticles);
    this.particleData = new Float32Array(maxParticles * 6); // x,z, vx,vz, life, maxLife
    this.count = 0;
    this.geometry = new THREE.BufferGeometry();
    this.geometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    this.geometry.setAttribute('color', new THREE.BufferAttribute(this.colors, 3));
    this.geometry.setAttribute('size', new THREE.BufferAttribute(this.sizes, 1));
    const mat = new THREE.PointsMaterial({
      size: 0.25, vertexColors: true, blending: THREE.AdditiveBlending,
      depthWrite: false, transparent: true, opacity: 0.8,
      sizeAttenuation: true
    });
    this.points = new THREE.Points(this.geometry, mat);
    this.points.frustumCulled = false;
  }
  spawn(x, z, vx, vz, life = 3 + Math.random() * 4) {
    if (this.count >= this.maxParticles) return;
    const i = this.count;
    const pd = i * 6;
    this.particleData[pd] = x;
    this.particleData[pd + 1] = z;
    this.particleData[pd + 2] = vx;
    this.particleData[pd + 3] = vz;
    this.particleData[pd + 4] = life;
    this.particleData[pd + 5] = life;
    this.alive[i] = 1;
    this.count++;
  }
  spawnFromTraffic(apiTraffic, gridSize, worldScale, heightData, count) {
    const cellSize = worldScale / (gridSize - 1);
    const half = worldScale / 2;
    for (let k = 0; k < count && this.count < this.maxParticles; k++) {
      // Weighted random by traffic
      let ix, iy, attempts = 0;
      do {
        ix = Math.floor(Math.random() * gridSize);
        iy = Math.floor(Math.random() * gridSize);
        attempts++;
      } while (attempts < 50 && Math.random() > apiTraffic[iy * gridSize + ix]);
      const x = ix * cellSize - half;
      const z = iy * cellSize - half;
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.3 + Math.random() * 0.8;
      this.spawn(x, z, Math.cos(angle) * speed, Math.sin(angle) * speed, 2 + Math.random() * 4);
    }
  }
  update(dt, heightData, gridSize, worldScale) {
    const cellSize = worldScale / (gridSize - 1);
    const half = worldScale / 2;
    let writeIdx = 0;
    for (let i = 0; i < this.count; i++) {
      if (!this.alive[i]) continue;
      const pd = i * 6;
      this.particleData[pd + 4] -= dt;
      if (this.particleData[pd + 4] <= 0) { this.alive[i] = 0; continue; }
      this.particleData[pd] += this.particleData[pd + 2] * dt;
      this.particleData[pd + 1] += this.particleData[pd + 3] * dt;
      let px = this.particleData[pd], pz = this.particleData[pd + 1];
      // Wrap at world bounds
      if (px < -half) px += worldScale;
      if (px > half) px -= worldScale;
      if (pz < -half) pz += worldScale;
      if (pz > half) pz -= worldScale;
      this.particleData[pd] = px; this.particleData[pd + 1] = pz;
      const h = this.getTerrainHeight(px, pz, heightData, gridSize, worldScale);
      const lifeRatio = this.particleData[pd + 4] / this.particleData[pd + 5];
      const pi = writeIdx * 3;
      this.positions[pi] = px;
      this.positions[pi + 1] = h + 0.3 + lifeRatio * 0.5;
      this.positions[pi + 2] = pz;
      // Gold to white as particle ages
      this.colors[pi] = 1;
      this.colors[pi + 1] = 0.7 + lifeRatio * 0.3;
      this.colors[pi + 2] = 0.2 + lifeRatio * 0.3;
      this.sizes[writeIdx] = 0.15 + lifeRatio * 0.2;
      writeIdx++;
    }
    // Compact alive particles
    let compactIdx = 0;
    for (let i = 0; i < this.count; i++) {
      if (this.alive[i]) {
        if (i !== compactIdx) {
          this.alive[compactIdx] = 1;
          const src = i * 6, dst = compactIdx * 6;
          for (let j = 0; j < 6; j++) this.particleData[dst + j] = this.particleData[src + j];
        }
        compactIdx++;
      }
    }
    this.count = compactIdx;
    this.geometry.attributes.position.needsUpdate = true;
    this.geometry.attributes.color.needsUpdate = true;
    this.geometry.attributes.size.needsUpdate = true;
    this.geometry.setDrawRange(0, this.count);
  }
}
// === Camera Bookmarks ===
const BOOKMARKS = [
  { name: 'Overview', pos: [18, 14, 18], target: [0, 2, 0] },
  { name: 'Top-down', pos: [0, 22, 0.5], target: [0, 0, 0] },
  { name: 'East ridge', pos: [16, 6, -6], target: [4, 1, -4] },
  { name: 'Valley', pos: [-8, 3, -8], target: [0, 0.5, 0] },
];
// === Main Application ===
const GRID_SIZE = 100;
const WORLD_SCALE = 20;
const TIMESTEPS = 12;
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a1a);
scene.fog = new THREE.Fog(0x0a0a1a, 25, 55);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.5, 80);
camera.position.set(16, 12, 16);
camera.lookAt(0, 2, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
// Lighting
const ambientLight = new THREE.AmbientLight(0x304060, 1.8);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xfff5e8, 3.5);
sunLight.position.set(15, 20, 8);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0003;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x8090c0, 0.8);
fillLight.position.set(-6, 3, -4);
scene.add(fillLight);
// Base plane
const baseGeo = new THREE.PlaneGeometry(WORLD_SCALE * 1.4, WORLD_SCALE * 1.4);
const baseMat = new THREE.MeshStandardMaterial({ color: 0x0a1020, roughness: 0.9 });
const basePlane = new THREE.Mesh(baseGeo, baseMat);
basePlane.rotation.x = -Math.PI / 2;
basePlane.position.y = -0.05;
basePlane.receiveShadow = true;
scene.add(basePlane);
// Grid overlay
const gridHelper = new THREE.PolarGridHelper(WORLD_SCALE / 2 + 0.5, 40, 20, 64, 0x1a2a4a, 0x1a2a4a);
gridHelper.position.y = 0.01;
scene.add(gridHelper);
// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 2, 0);
controls.minDistance = 4;
controls.maxDistance = 35;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
// Data
const dataset = generateDataset(TIMESTEPS, GRID_SIZE);
const terrainBuilder = new TerrainBuilder(GRID_SIZE, WORLD_SCALE);
const riverTracer = new RiverTracer(GRID_SIZE);
const indices = terrainBuilder.buildIndices();
// Terrain mesh
let terrainGeo = new THREE.BufferGeometry();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.65, metalness: 0.05, flatShading: false
});
let terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// River groups (cached per timestep)
const riverGroups = new Map();
let activeRiverGroup = null;
// Particle system
let getTerrainHeightFn = (x, z, hd, gs, ws) => {
  const cellSize = ws / (gs - 1);
  const half = ws / 2;
  const ix = Math.round((x + half) / cellSize);
  const iy = Math.round((z + half) / cellSize);
  const cx = Math.max(0, Math.min(gs - 1, ix));
  const cy_ = Math.max(0, Math.min(gs - 1, iy));
  return hd[cy_ * gs + cx] * ws * 0.4;
};
const particleSys = new ParticleSystem(2500, GRID_SIZE, WORLD_SCALE, getTerrainHeightFn);
scene.add(particleSys.points);
// State
let currentTimestep = 0;
let isPlaying = false;
let playTimer = 0;
const PLAY_INTERVAL = 0.8;
// === Helpers ===
function getHeightAt(x, z, heightData) {
  return getTerrainHeightFn(x, z, heightData, GRID_SIZE, WORLD_SCALE);
}
function buildRiverGeometry(paths, heightData) {
  const group = new THREE.Group();
  const riverMat = new THREE.MeshStandardMaterial({
    color: 0xcc3333, roughness: 0.3, metalness: 0.4, emissive: 0x330808, emissiveIntensity: 0.5
  });
  const glowMat = new THREE.MeshBasicMaterial({
    color: 0xff4444, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.35
  });
  for (const path of paths) {
    if (path.length < 2) continue;
    const pts = [];
    for (const p of path) {
      const px = (p.x / (GRID_SIZE - 1) - 0.5) * WORLD_SCALE;
      const pz = (p.y / (GRID_SIZE - 1) - 0.5) * WORLD_SCALE;
      const h = getHeightAt(px, pz, heightData) + 0.15;
      pts.push(new THREE.Vector3(px, h, pz));
    }
    const curve = new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.5);
    const tubeGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.12, 6, false);
    const tube = new THREE.Mesh(tubeGeo, riverMat);
    tube.castShadow = true;
    group.add(tube);
    // Glow tube
    const glowGeo = new THREE.TubeGeometry(curve, path.length * 2, 0.22, 6, false);
    const glow = new THREE.Mesh(glowGeo, glowMat);
    group.add(glow);
  }
  return group;
}
function switchTimestep(t) {
  currentTimestep = t;
  const d = dataset[t];
  const built = terrainBuilder.build(d.height, d.userDensity, t);
  // Update terrain geometry
  terrainGeo.dispose();
  terrainGeo = new THREE.BufferGeometry();
  terrainGeo.setAttribute('position', new THREE.BufferAttribute(built.positions, 3));
  terrainGeo.setAttribute('color', new THREE.BufferAttribute(built.colors, 3));
  terrainGeo.setIndex(new THREE.BufferAttribute(indices, 1));
  terrainGeo.computeVertexNormals();
  terrainMesh.geometry = terrainGeo;
  // Switch rivers
  if (activeRiverGroup) { scene.remove(activeRiverGroup); activeRiverGroup = null; }
  if (!riverGroups.has(t)) {
    const sources = riverTracer.findRiverSources(d.errorRate, d.height, 0.6, 7);
    const paths = sources.map(s => riverTracer.trace(d.errorRate, d.height, s.x, s.y, 150));
    const filtered = paths.filter(p => p.length > 3);
    const group = buildRiverGeometry(filtered, d.height);
    riverGroups.set(t, group);
  }
  activeRiverGroup = riverGroups.get(t);
  scene.add(activeRiverGroup);
  // Update UI
  document.getElementById('time-slider').value = t;
  document.getElementById('time-label').textContent = `T${t}`;
}
// === Bookmarks UI ===
const bookmarksContainer = document.getElementById('bookmarks');
BOOKMARKS.forEach((bm, i) => {
  const btn = document.createElement('button');
  btn.className = 'btn';
  btn.textContent = bm.name;
  btn.addEventListener('click', () => {
    animateCamera(bm.pos, bm.target);
  });
  bookmarksContainer.appendChild(btn);
});
function animateCamera(targetPos, targetLook) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...targetPos);
  const endTarget = new THREE.Vector3(...targetLook);
  const startTime = performance.now();
  const duration = 1200;
  function anim(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
}
// === UI Events ===
const timeSlider = document.getElementById('time-slider');
timeSlider.max = TIMESTEPS - 1;
timeSlider.value = 0;
timeSlider.addEventListener('input', () => {
  const t = parseInt(timeSlider.value);
  switchTimestep(t);
});
document.getElementById('btn-play').addEventListener('click', function() {
  isPlaying = !isPlaying;
  this.textContent = isPlaying ? 'Pause' : 'Play';
  this.classList.toggle('active', isPlaying);
  playTimer = 0;
});
document.getElementById('btn-auto-rotate').addEventListener('click', function() {
  controls.autoRotate = !controls.autoRotate;
  this.classList.toggle('active', controls.autoRotate);
});
// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  switch(e.key.toLowerCase()) {
    case ' ': e.preventDefault(); isPlaying = !isPlaying; document.getElementById('btn-play').textContent = isPlaying ? 'Pause' : 'Play'; document.getElementById('btn-play').classList.toggle('active', isPlaying); playTimer = 0; break;
    case 'arrowleft': e.preventDefault(); switchTimestep(Math.max(0, currentTimestep - 1)); break;
    case 'arrowright': e.preventDefault(); switchTimestep(Math.min(TIMESTEPS - 1, currentTimestep + 1)); break;
    case 'r': e.preventDefault(); controls.autoRotate = !controls.autoRotate; document.getElementById('btn-auto-rotate').classList.toggle('active', controls.autoRotate); break;
    case '0': e.preventDefault(); animateCamera(BOOKMARKS[0].pos, BOOKMARKS[0].target); break;
    case '1': e.preventDefault(); animateCamera(BOOKMARKS[1].pos, BOOKMARKS[1].target); break;
    case '2': e.preventDefault(); animateCamera(BOOKMARKS[2].pos, BOOKMARKS[2].target); break;
    case '3': e.preventDefault(); animateCamera(BOOKMARKS[3].pos, BOOKMARKS[3].target); break;
  }
});
// === Render Loop ===
const clock = new THREE.Clock();
let particleSpawnTimer = 0;
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  // Time playback
  if (isPlaying) {
    playTimer += dt;
    if (playTimer >= PLAY_INTERVAL) {
      playTimer -= PLAY_INTERVAL;
      const next = (currentTimestep + 1) % TIMESTEPS;
      switchTimestep(next);
    }
  }
  // Particles
  const d = dataset[currentTimestep];
  particleSpawnTimer += dt;
  if (particleSpawnTimer > 0.15) {
    particleSpawnTimer -= 0.15;
    particleSys.spawnFromTraffic(d.apiTraffic, GRID_SIZE, WORLD_SCALE, d.height, 8);
  }
  particleSys.update(dt, d.height, GRID_SIZE, WORLD_SCALE);
  renderer.render(scene, camera);
}
// === Init ===
switchTimestep(0);
animate();
// Resize handler
window.addEventListener('resize', () => {
  camera.aspect = container.clientWidth / container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
console.log('3D Data Terrain Explorer ready — T=0..' + (TIMESTEPS - 1) + ' | Grid=' + GRID_SIZE + 'x' + GRID_SIZE + ' | River paths cached per timestep');
</script>
</body>
</html>