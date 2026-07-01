<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8ccd4}
#canvas-container{position:fixed;inset:0;z-index:1}
#ui-overlay{position:fixed;inset:0;pointer-events:none;z-index:10}
#ui-overlay>*{pointer-events:auto}
#time-panel{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(10,10,20,0.85);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:12px 20px;display:flex;align-items:center;gap:14px;min-width:420px}
#time-slider{flex:1;height:6px;-webkit-appearance:none;appearance:none;background:linear-gradient(90deg,#1a472a,#4a9,#c4a);border-radius:3px;outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 0 12px rgba(72,170,153,0.6);cursor:grab;border:2px solid #4a9}
#time-label{font-size:13px;font-weight:600;color:#4a9;min-width:80px;text-align:center}
#time-nav{display:flex;gap:4px}
#time-nav button{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#c8ccd4;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:12px;transition:background .15s}
#time-nav button:hover{background:rgba(255,255,255,0.16)}
#btn-auto-rotate{position:absolute;bottom:90px;left:24px;background:rgba(10,10,20,0.85);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:8px 14px;color:#c8ccd4;cursor:pointer;font-size:12px;transition:all .15s}
#btn-auto-rotate.active{color:#4a9;border-color:#4a9;box-shadow:0 0 8px rgba(72,170,153,0.3)}
#bookmarks-panel{position:absolute;top:24px;right:24px;background:rgba(10,10,20,0.85);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:14px;min-width:180px;max-height:60vh;overflow-y:auto}
#bookmarks-panel h3{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#4a9;margin-bottom:10px}
.bookmark-item{display:flex;justify-content:space-between;align-items:center;padding:6px 8px;border-radius:6px;cursor:pointer;font-size:12px;transition:background .12s;margin-bottom:2px}
.bookmark-item:hover{background:rgba(255,255,255,0.08)}
.bookmark-item .del{color:#c44;opacity:0;transition:opacity .12s;padding:2px 6px;border-radius:3px}
.bookmark-item:hover .del{opacity:1}
.bookmark-item .del:hover{background:rgba(204,68,68,0.2)}
#btn-bookmark{width:100%;margin-top:8px;background:rgba(72,170,153,0.15);border:1px solid rgba(72,170,153,0.3);color:#4a9;border-radius:6px;padding:6px;cursor:pointer;font-size:12px;transition:all .15s}
#btn-bookmark:hover{background:rgba(72,170,153,0.25)}
#stats-panel{position:absolute;top:24px;left:24px;background:rgba(10,10,20,0.85);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:12px 16px;font-size:11px;line-height:1.6}
#stats-panel .stat-label{color:#888}
#stats-panel .stat-value{color:#c8ccd4;font-weight:600}
#loading-indicator{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(10,10,20,0.9);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:16px 24px;display:none;flex-direction:column;align-items:center;gap:8px}
#loading-indicator .spinner{width:24px;height:24px;border:2px solid rgba(255,255,255,0.15);border-top-color:#4a9;border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
#loading-indicator .text{font-size:12px;color:#888}
#drop-overlay{position:fixed;inset:0;background:rgba(72,170,153,0.12);border:2px dashed rgba(72,170,153,0.4);z-index:100;display:none;align-items:center;justify-content:center;font-size:16px;color:#4a9;pointer-events:none}
#drop-overlay.visible{display:flex}
#error-toast{position:fixed;top:24px;left:50%;transform:translateX(-50%);background:rgba(180,40,40,0.9);color:#fff;padding:10px 20px;border-radius:8px;font-size:13px;z-index:200;display:none}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-overlay">
  <div id="stats-panel">
    <div><span class="stat-label">Time: </span><span class="stat-value" id="stat-time">--</span></div>
    <div><span class="stat-label">Cache: </span><span class="stat-value" id="stat-cache">0/0</span></div>
    <div><span class="stat-label">Memory: </span><span class="stat-value" id="stat-mem">0 MB</span></div>
    <div><span class="stat-label">FPS: </span><span class="stat-value" id="stat-fps">--</span></div>
  </div>
  <div id="bookmarks-panel">
    <h3>Camera Bookmarks</h3>
    <div id="bookmarks-list"></div>
    <button id="btn-bookmark">+ Save Current View</button>
  </div>
  <button id="btn-auto-rotate" class="active" title="Toggle auto-rotation">⟳ Auto-Rotate</button>
  <div id="time-panel">
    <div id="time-nav"><button id="btn-prev">◀</button></div>
    <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
    <div id="time-nav"><button id="btn-next">▶</button></div>
    <span id="time-label">12:00</span>
  </div>
</div>
<div id="loading-indicator"><div class="spinner"></div><span class="text">Building terrain...</span></div>
<div id="drop-overlay">Drop JSON/CSV file to load external data</div>
<div id="error-toast"></div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─── CONFIGURATION ────────────────────────────────────────────
const IS_MOBILE = window.innerWidth < 768 || /Mobi|Android/i.test(navigator.userAgent);
const CONFIG = {
  grid: IS_MOBILE ? 30 : 60,
  particleCount: IS_MOBILE ? 500 : 2000,
  cacheMaxEntries: IS_MOBILE ? 3 : 10,
  cacheMaxMemoryMB: IS_MOBILE ? 40 : 100,
  timeSteps: 24,
  terrainSize: 40,
  maxHeight: 8,
  riverThreshold: 0.65,
  riverSegments: 120,
  riverRadius: 0.08,
  particleSpeed: 0.3,
  particleLifetime: 4,
  autoRotateSpeed: 0.3,
  dampingFactor: 0.08,
  ambientColor: 0x1a1a2e,
  directionalColor: 0xffffff,
  fogColor: 0x0a0a14,
  fogNear: 30,
  fogFar: 80,
  colorScheme: 'vegetation',
  memoryBudget: {
    terrainPerFrame: IS_MOBILE ? 3 : 5,
    particles: IS_MOBILE ? 1 : 2,
    rivers: 1,
    total: IS_MOBILE ? 5 : 8
  }
};
// ─── DATA GENERATOR ───────────────────────────────────────────
class DataGenerator {
  constructor(config) {
    this.config = config;
    this.seed = 42;
    this.data = null;
  }
  mulberry32(a) {
    return () => { a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; };
  }
  noise2D(x, y, rng) {
    const n = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453;
    return (n - Math.floor(n)) * 0.5 + 0.5;
  }
  generate() {
    const { timeSteps, grid } = this.config;
    const data = [];
    for (let t = 0; t < timeSteps; t++) {
      const rng = this.mulberry32(this.seed + t * 1000);
      const revenue = [];
      const users = [];
      const errors = [];
      const apiCalls = [];
      const hourAngle = (t / timeSteps) * Math.PI * 2;
      const dayPhase = Math.sin(hourAngle) * 0.5 + 0.5;
      for (let i = 0; i < grid; i++) {
        revenue[i] = [];
        users[i] = [];
        errors[i] = [];
        for (let j = 0; j < grid; j++) {
          const nx = (i / grid - 0.5) * 2;
          const ny = (j / grid - 0.5) * 2;
          const dist = Math.sqrt(nx * nx + ny * ny);
          const base = (1 - dist) * (0.6 + dayPhase * 0.4);
          const hotspot = Math.exp(-((nx - 0.3) * (nx - 0.3) + (ny - 0.2) * (ny - 0.2)) * 8) * 0.7
            + Math.exp(-((nx + 0.4) * (nx + 0.4) + (ny - 0.35) * (ny - 0.35)) * 6) * 0.5
            + Math.exp(-((nx + 0.1) * (nx + 0.1) + (ny + 0.4) * (ny + 0.4)) * 7) * 0.45;
          const noise = (rng() - 0.5) * 0.3;
          revenue[i][j] = Math.max(0, base + hotspot + noise * dayPhase);
          users[i][j] = Math.max(0, revenue[i][j] * (0.7 + rng() * 0.6));
          errors[i][j] = Math.max(0, (rng() - 0.7) * (1 - dayPhase * 0.5) * (dist < 0.5 ? 1 : 0.3));
        }
      }
      const callCount = 8 + Math.floor(dayPhase * 20);
      for (let c = 0; c < callCount; c++) {
        const startAngle = rng() * Math.PI * 2;
        const startDist = 0.1 + rng() * 0.8;
        const endAngle = startAngle + (rng() - 0.5) * Math.PI;
        const endDist = 0.1 + rng() * 0.8;
        apiCalls.push({
          from: {
            x: Math.cos(startAngle) * startDist,
            y: revenue[Math.floor((startDist * 0.5 + 0.5) * (grid - 1))]?.[Math.floor(((Math.sin(startAngle) * startDist) * 0.5 + 0.5) * (grid - 1))] * this.config.maxHeight || 0,
            z: Math.sin(startAngle) * startDist
          },
          to: {
            x: Math.cos(endAngle) * endDist,
            y: 0,
            z: Math.sin(endAngle) * endDist
          },
          startTime: rng() * 0.9,
          duration: 0.05 + rng() * 0.15
        });
      }
      data.push({ revenue, users, errors, apiCalls });
    }
    this.data = data;
    return data;
  }
  getRevenue(t, i, j) { return this.data[t].revenue[i][j]; }
  getUsers(t, i, j) { return this.data[t].users[i][j]; }
  getErrors(t, i, j) { return this.data[t].errors[i][j]; }
  getApiCalls(t) { return this.data[t].apiCalls; }
}
// ─── TERRAIN CACHE ────────────────────────────────────────────
class TerrainCache {
  constructor(maxEntries, maxMemoryMB) {
    this.cache = new Map();
    this.maxEntries = maxEntries;
    this.maxMemoryBytes = maxMemoryMB * 1024 * 1024;
    this.accessOrder = [];
    this.primed = new Set();
    this.currentMemoryBytes = 0;
  }
  get(timeIndex) {
    const entry = this.cache.get(timeIndex);
    if (entry && this.primed.has(timeIndex)) {
      this._touch(timeIndex);
      return entry;
    }
    return null;
  }
  has(timeIndex) {
    return this.cache.has(timeIndex) && this.primed.has(timeIndex);
  }
  allocate(timeIndex) {
    this.cache.set(timeIndex, { geometry: null, rivers: null, particles: null, timestamp: Date.now() });
    this.accessOrder.push(timeIndex);
    return timeIndex;
  }
  populate(timeIndex, geometry, rivers, particles) {
    const entry = this.cache.get(timeIndex);
    if (!entry) return false;
    entry.geometry = geometry;
    entry.rivers = rivers;
    entry.particles = particles;
    const size = this._estimateSize(entry);
    this.currentMemoryBytes += size;
    entry._size = size;
    this.primed.add(timeIndex);
    this._evictIfNeeded();
    return true;
  }
  _touch(timeIndex) {
    const idx = this.accessOrder.indexOf(timeIndex);
    if (idx > -1) {
      this.accessOrder.splice(idx, 1);
      this.accessOrder.push(timeIndex);
    }
    const entry = this.cache.get(timeIndex);
    if (entry) entry.timestamp = Date.now();
  }
  _estimateSize(entry) {
    let bytes = 0;
    if (entry.geometry) {
      const pos = entry.geometry.getAttribute('position');
      const col = entry.geometry.getAttribute('color');
      if (pos) bytes += pos.array.byteLength;
      if (col) bytes += col.array.byteLength;
      bytes += (entry.geometry.index?.array.byteLength || 0);
    }
    if (entry.rivers) {
      for (const r of entry.rivers) {
        if (r.geometry) {
          const rpos = r.geometry.getAttribute('position');
          if (rpos) bytes += rpos.array.byteLength;
        }
      }
    }
    return bytes;
  }
  _evictIfNeeded() {
    while (this.cache.size > this.maxEntries || this.currentMemoryBytes > this.maxMemoryBytes) {
      if (this.cache.size <= 1) break;
      let oldest = this.accessOrder[0];
      for (const idx of this.accessOrder) {
        if (this.primed.has(idx)) { oldest = idx; break; }
      }
      this._remove(oldest);
    }
  }
  _remove(timeIndex) {
    const entry = this.cache.get(timeIndex);
    if (entry) {
      if (entry.geometry) entry.geometry.dispose();
      if (entry.rivers) {
        for (const r of entry.rivers) {
          if (r.geometry) r.geometry.dispose();
        }
      }
      this.currentMemoryBytes -= (entry._size || 0);
    }
    this.cache.delete(timeIndex);
    this.primed.delete(timeIndex);
    this.accessOrder = this.accessOrder.filter(i => i !== timeIndex);
  }
  getStats() {
    return {
      entries: this.cache.size,
      primed: this.primed.size,
      memoryMB: (this.currentMemoryBytes / (1024 * 1024)).toFixed(1)
    };
  }
  clear() {
    for (const [key] of this.cache) {
      this._remove(key);
    }
  }
}
// ─── TERRAIN BUILDER ──────────────────────────────────────────
class TerrainBuilder {
  constructor(config, dataGen) {
    this.config = config;
    this.dataGen = dataGen;
    this.material = new THREE.MeshStandardMaterial({
      vertexColors: true,
      side: THREE.DoubleSide,
      roughness: 0.75,
      metalness: 0.1,
      flatShading: false
    });
  }
  buildGeometry(timeIndex) {
    const { grid, terrainSize, maxHeight } = this.config;
    const half = terrainSize / 2;
    const cellSize = terrainSize / (grid - 1);
    const vertices = [];
    const colors = [];
    for (let i = 0; i < grid; i++) {
      for (let j = 0; j < grid; j++) {
        const x = i * cellSize - half;
        const z = j * cellSize - half;
        const revenue = this.dataGen.getRevenue(timeIndex, i, j);
        const users = this.dataGen.getUsers(timeIndex, i, j);
        const y = revenue * maxHeight;
        vertices.push(x, y, z);
        const color = this._mapColor(revenue, users, i, j, grid);
        colors.push(color.r, color.g, color.b);
      }
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    const indices = [];
    for (let i = 0; i < grid - 1; i++) {
      for (let j = 0; j < grid - 1; j++) {
        const a = i * grid + j;
        const b = a + 1;
        const c = a + grid;
        const d = c + 1;
        indices.push(a, b, d);
        indices.push(a, d, c);
      }
    }
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    return geometry;
  }
  _mapColor(revenue, users, i, j, grid) {
    const cfg = this.config;
    if (cfg.colorScheme === 'vegetation') {
      const green = 0.15 + users * 0.85;
      const brown = 0.4 * (1 - users);
      return {
        r: 0.1 + brown * 0.6,
        g: 0.15 + green * 0.7,
        b: 0.08 + revenue * 0.15
      };
    }
    if (cfg.colorScheme === 'heat') {
      const h = 0.66 - revenue * 0.66;
      const s = 0.8;
      const l = 0.2 + revenue * 0.5;
      const c = (1 - Math.abs(2 * l - 1)) * s;
      const x = c * (1 - Math.abs((h * 6) % 2 - 1));
      const m = l - c / 2;
      let r, g, b;
      if (h < 1/6) { r = c; g = x; b = 0; }
      else if (h < 2/6) { r = x; g = c; b = 0; }
      else if (h < 3/6) { r = 0; g = c; b = x; }
      else if (h < 4/6) { r = 0; g = x; b = c; }
      else if (h < 5/6) { r = x; g = 0; b = c; }
      else { r = c; g = 0; b = x; }
      return { r: r + m, g: g + m, b: b + m };
    }
    return { r: 0.4, g: 0.4, b: 0.4 };
  }
  getMaterial() { return this.material; }
}
// ─── RIVER BUILDER ────────────────────────────────────────────
class RiverBuilder {
  constructor(config, dataGen) {
    this.config = config;
    this.dataGen = dataGen;
    this.riverMaterial = new THREE.MeshStandardMaterial({
      color: 0xcc3333,
      roughness: 0.3,
      metalness: 0.5,
      emissive: 0x330000,
      emissiveIntensity: 0.6
    });
  }
  buildRivers(timeIndex) {
    const { grid, terrainSize, maxHeight, riverThreshold, riverSegments, riverRadius } = this.config;
    const half = terrainSize / 2;
    const cellSize = terrainSize / (grid - 1);
    const rivers = [];
    const errorPoints = [];
    for (let i = 0; i < grid; i++) {
      for (let j = 0; j < grid; j++) {
        const err = this.dataGen.getErrors(timeIndex, i, j);
        if (err > riverThreshold) {
          errorPoints.push({ i, j, err, x: i * cellSize - half, z: j * cellSize - half });
        }
      }
    }
    if (errorPoints.length < 3) return rivers;
    const visited = new Set();
    const clusters = [];
    for (const pt of errorPoints) {
      const key = `${pt.i},${pt.j}`;
      if (visited.has(key)) continue;
      const cluster = [];
      const stack = [pt];
      while (stack.length > 0) {
        const curr = stack.pop();
        const ck = `${curr.i},${curr.j}`;
        if (visited.has(ck)) continue;
        visited.add(ck);
        cluster.push(curr);
        for (const n of errorPoints) {
          const nk = `${n.i},${n.j}`;
          if (!visited.has(nk) && Math.abs(n.i - curr.i) <= 2 && Math.abs(n.j - curr.j) <= 2) {
            stack.push(n);
          }
        }
      }
      if (cluster.length >= 3) clusters.push(cluster);
    }
    for (const cluster of clusters) {
      cluster.sort((a, b) => (a.i + a.j) - (b.i + b.j));
      if (cluster.length < 3) continue;
      const stride = Math.max(1, Math.floor(cluster.length / riverSegments));
      const sampled = [];
      for (let i = 0; i < cluster.length; i += stride) {
        sampled.push(cluster[i]);
      }
      if (sampled[sampled.length - 1] !== cluster[cluster.length - 1]) {
        sampled.push(cluster[cluster.length - 1]);
      }
      const points = sampled.map(pt => {
        const y = this.dataGen.getRevenue(timeIndex, pt.i, pt.j) * maxHeight + riverRadius * 2;
        return new THREE.Vector3(pt.x, y, pt.z);
      });
      if (points.length < 2) continue;
      const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
      const tubeGeometry = new THREE.TubeGeometry(curve, Math.min(riverSegments, points.length * 4), riverRadius, 6, false);
      const tube = new THREE.Mesh(tubeGeometry, this.riverMaterial.clone());
      rivers.push(tube);
    }
    return rivers;
  }
  getMaterial() { return this.riverMaterial; }
}
// ─── PARTICLE SYSTEM ──────────────────────────────────────────
class ParticleSystem {
  constructor(config, dataGen) {
    this.config = config;
    this.dataGen = dataGen;
    this.activeCalls = [];
    this.geometry = new THREE.BufferGeometry();
    this.positions = new Float32Array(config.particleCount * 3);
    this.colors = new Float32Array(config.particleCount * 3);
    this.alphas = new Float32Array(config.particleCount);
    this.trailOffsets = new Float32Array(config.particleCount);
    this.geometry.setAttribute('position', new THREE.Float32BufferAttribute(this.positions, 3));
    this.geometry.setAttribute('color', new THREE.Float32BufferAttribute(this.colors, 3));
    const spriteTex = this._createGlowTexture();
    const material = new THREE.PointsMaterial({
      size: 0.25,
      map: spriteTex,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      vertexColors: true,
      transparent: true,
      opacity: 0.8
    });
    this.points = new THREE.Points(this.geometry, material);
    this.trailPoints = [];
    this.maxTrails = Math.floor(config.particleCount * 0.15);
  }
  _createGlowTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 32;
    canvas.height = 32;
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createRadialGradient(16, 16, 0, 16, 16, 16);
    gradient.addColorStop(0, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.2, 'rgba(255,255,200,0.8)');
    gradient.addColorStop(0.5, 'rgba(100,200,255,0.3)');
    gradient.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 32, 32);
    const tex = new THREE.CanvasTexture(canvas);
    tex.needsUpdate = true;
    return tex;
  }
  update(timeIndex, deltaTime, timeInStep, terrainMesh) {
    const { grid, terrainSize, maxHeight, particleSpeed, particleLifetime } = this.config;
    const half = terrainSize / 2;
    const cellSize = terrainSize / (grid - 1);
    const calls = this.dataGen.getApiCalls(timeIndex);
    for (const call of calls) {
      const globalTime = timeInStep;
      if (globalTime >= call.startTime && globalTime <= call.startTime + call.duration) {
        const progress = (globalTime - call.startTime) / call.duration;
        const pos = {
          x: call.from.x + (call.to.x - call.from.x) * progress,
          z: call.from.z + (call.to.z - call.from.z) * progress
        };
        const gi = Math.floor(((pos.x / (terrainSize / 2)) * 0.5 + 0.5) * (grid - 1));
        const gj = Math.floor(((pos.z / (terrainSize / 2)) * 0.5 + 0.5) * (grid - 1));
        const ci = Math.max(0, Math.min(grid - 1, gi));
        const cj = Math.max(0, Math.min(grid - 1, gj));
        const y = this.dataGen.getRevenue(timeIndex, ci, cj) * maxHeight + 0.3;
        this.trailPoints.push({
          x: pos.x * half,
          y: y,
          z: pos.z * half,
          life: particleLifetime,
          color: { r: 0.4 + progress * 0.6, g: 0.7 + progress * 0.3, b: 1.0 }
        });
      }
    }
    if (this.trailPoints.length > this.maxTrails) {
      this.trailPoints.splice(0, this.trailPoints.length - this.maxTrails);
    }
    for (let i = this.trailPoints.length - 1; i >= 0; i--) {
      this.trailPoints[i].life -= deltaTime;
      if (this.trailPoints[i].life <= 0) {
        this.trailPoints.splice(i, 1);
      }
    }
    const count = Math.min(this.trailPoints.length, this.config.particleCount);
    for (let i = 0; i < count; i++) {
      const tp = this.trailPoints[i];
      const idx = i * 3;
      this.positions[idx] = tp.x;
      this.positions[idx + 1] = tp.y;
      this.positions[idx + 2] = tp.z;
      const alpha = Math.max(0, tp.life / particleLifetime);
      this.colors[idx] = tp.color.r * alpha;
      this.colors[idx + 1] = tp.color.g * alpha;
      this.colors[idx + 2] = tp.color.b * alpha;
    }
    for (let i = count; i < this.config.particleCount; i++) {
      const idx = i * 3;
      this.positions[idx] = 0;
      this.positions[idx + 1] = -100;
      this.positions[idx + 2] = 0;
      this.colors[idx] = 0;
      this.colors[idx + 1] = 0;
      this.colors[idx + 2] = 0;
    }
    this.geometry.attributes.position.needsUpdate = true;
    this.geometry.attributes.color.needsUpdate = true;
  }
  getMesh() { return this.points; }
  reset() {
    this.trailPoints = [];
    this.positions.fill(0);
    this.colors.fill(0);
    if (this.geometry.attributes.position) this.geometry.attributes.position.needsUpdate = true;
    if (this.geometry.attributes.color) this.geometry.attributes.color.needsUpdate = true;
  }
}
// ─── DATA LOADER ──────────────────────────────────────────────
class DataLoader {
  constructor(config) {
    this.config = config;
    this.onDataLoaded = null;
  }
  setupDropZone(container) {
    const overlay = document.getElementById('drop-overlay');
    if (!overlay) return;
    const showOverlay = (e) => {
      e.preventDefault();
      overlay.classList.add('visible');
    };
    const hideOverlay = () => overlay.classList.remove('visible');
    document.addEventListener('dragenter', showOverlay);
    document.addEventListener('dragover', (e) => { e.preventDefault(); });
    overlay.addEventListener('dragleave', hideOverlay);
    overlay.addEventListener('drop', (e) => {
      e.preventDefault();
      hideOverlay();
      const file = e.dataTransfer.files[0];
      if (file) this._processFile(file);
    });
    const urlData = new URLSearchParams(window.location.search).get('data');
    if (urlData) {
      this._fetchExternal(urlData);
    }
  }
  async _processFile(file) {
    const text = await file.text();
    this._parseAndLoad(text, file.name);
  }
  async _fetchExternal(url) {
    try {
      const resp = await fetch(url);
      const text = await resp.text();
      this._parseAndLoad(text, url);
    } catch (e) {
      this._showError('Failed to load external data: ' + e.message);
    }
  }
  _parseAndLoad(text, source) {
    try {
      let parsed;
      if (text.trim().startsWith('{')) {
        parsed = JSON.parse(text);
      } else {
        parsed = this._parseCSV(text);
      }
      if (this.onDataLoaded) {
        this.onDataLoaded(parsed, source);
      }
    } catch (e) {
      this._showError('Failed to parse data from ' + source + ': ' + e.message);
    }
  }
  _parseCSV(text) {
    const lines = text.trim().split('\n');
    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
    const timeIdx = headers.indexOf('time') !== -1 ? headers.indexOf('time') : headers.indexOf('t');
    const xIdx = headers.indexOf('x') !== -1 ? headers.indexOf('x') : headers.indexOf('col');
    const yIdx = headers.indexOf('y') !== -1 ? headers.indexOf('y') : headers.indexOf('row');
    const revenueIdx = headers.indexOf('revenue') !== -1 ? headers.indexOf('revenue') : headers.indexOf('value');
    const usersIdx = headers.indexOf('users') !== -1 ? headers.indexOf('users') : -1;
    const errorsIdx = headers.indexOf('errors') !== -1 ? headers.indexOf('errors') : -1;
    const timeMap = {};
    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',').map(c => c.trim());
      const t = timeIdx >= 0 ? parseInt(cols[timeIdx]) : 0;
      if (!timeMap[t]) timeMap[t] = [];
      timeMap[t].push({
        x: xIdx >= 0 ? parseInt(cols[xIdx]) : 0,
        y: yIdx >= 0 ? parseInt(cols[yIdx]) : 0,
        revenue: revenueIdx >= 0 ? parseFloat(cols[revenueIdx]) : 0,
        users: usersIdx >= 0 ? parseFloat(cols[usersIdx]) : 0,
        errors: errorsIdx >= 0 ? parseFloat(cols[errorsIdx]) : 0
      });
    }
    const times = Object.keys(timeMap).sort((a, b) => parseInt(a) - parseInt(b));
    const grid = Math.ceil(Math.sqrt(timeMap[times[0]]?.length || 1));
    const data = [];
    for (const t of times) {
      const revenue = Array.from({ length: grid }, () => Array(grid).fill(0));
      const users = Array.from({ length: grid }, () => Array(grid).fill(0));
      const errors = Array.from({ length: grid }, () => Array(grid).fill(0));
      for (const row of timeMap[t]) {
        if (row.x < grid && row.y < grid) {
          revenue[row.y][row.x] = row.revenue;
          users[row.y][row.x] = row.users;
          errors[row.y][row.x] = row.errors;
        }
      }
      data.push({ revenue, users, errors, apiCalls: [] });
    }
    return data;
  }
  _showError(msg) {
    const toast = document.getElementById('error-toast');
    if (toast) {
      toast.textContent = msg;
      toast.style.display = 'block';
      setTimeout(() => { toast.style.display = 'none'; }, 4000);
    }
  }
}
// ─── APPLICATION ──────────────────────────────────────────────
class DataTerrainApp {
  constructor() {
    this.config = CONFIG;
    this.dataGen = new DataGenerator(this.config);
    this.dataGen.generate();
    this.cache = new TerrainCache(this.config.cacheMaxEntries, this.config.cacheMaxMemoryMB);
    this.terrainBuilder = new TerrainBuilder(this.config, this.dataGen);
    this.riverBuilder = new RiverBuilder(this.config, this.dataGen);
    this.particleSystem = new ParticleSystem(this.config, this.dataGen);
    this.currentTimeIndex = Math.floor(this.config.timeSteps / 2);
    this.timeInStep = 0;
    this.terrainMesh = null;
    this.riverGroup = new THREE.Group();
    this.clock = new THREE.Clock();
    this.fpsFrames = 0;
    this.fpsTime = 0;
    this.fpsValue = 0;
    this.bookmarks = [];
    this.autoRotate = true;
    this.cameraTargets = null;
    this.dataLoader = new DataLoader(this.config);
    this._initScene();
    this._initUI();
    this._loadTimeStep(this.currentTimeIndex);
    this._animate();
  }
  _initScene() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(this.config.fogColor);
    this.scene.fog = new THREE.Fog(this.config.fogColor, this.config.fogNear, this.config.fogFar);
    this.camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 150);
    this.camera.position.set(18, 14, 22);
    this.camera.lookAt(0, 2, 0);
    this.renderer = new THREE.WebGLRenderer({ antialias: !IS_MOBILE, powerPreference: 'high-performance' });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, IS_MOBILE ? 1.5 : 2));
    this.renderer.shadowMap.enabled = !IS_MOBILE;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.1;
    document.getElementById('canvas-container').appendChild(this.renderer.domElement);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.set(0, 2, 0);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = this.config.dampingFactor;
    this.controls.autoRotate = this.autoRotate;
    this.controls.autoRotateSpeed = this.config.autoRotateSpeed;
    this.controls.minDistance = 6;
    this.controls.maxDistance = 60;
    this.controls.maxPolarAngle = Math.PI * 0.55;
    this.controls.update();
    const ambient = new THREE.AmbientLight(this.config.ambientColor, 0.7);
    this.scene.add(ambient);
    const sun = new THREE.DirectionalLight(this.config.directionalColor, 1.5);
    sun.position.set(20, 25, 10);
    sun.castShadow = !IS_MOBILE;
    if (!IS_MOBILE) {
      sun.shadow.mapSize.width = 1024;
      sun.shadow.mapSize.height = 1024;
      sun.shadow.camera.near = 0.5;
      sun.shadow.camera.far = 80;
      sun.shadow.camera.left = -25;
      sun.shadow.camera.right = 25;
      sun.shadow.camera.top = 25;
      sun.shadow.camera.bottom = -25;
      sun.shadow.bias = -0.0001;
    }
    this.scene.add(sun);
    const hemi = new THREE.HemisphereLight(0x334466, 0x111122, 0.4);
    this.scene.add(hemi);
    const gridHelper = new THREE.GridHelper(40, 20, 0x222244, 0x111122);
    gridHelper.position.y = -0.05;
    this.scene.add(gridHelper);
    this.riverGroup = new THREE.Group();
    this.scene.add(this.riverGroup);
    this.particleGroup = this.particleSystem.getMesh();
    this.scene.add(this.particleGroup);
    window.addEventListener('resize', () => {
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }
  _initUI() {
    this.slider = document.getElementById('time-slider');
    this.slider.max = this.config.timeSteps - 1;
    this.slider.value = this.currentTimeIndex;
    this.slider.addEventListener('input', () => {
      const newTime = parseInt(this.slider.value);
      if (newTime !== this.currentTimeIndex) {
        this.currentTimeIndex = newTime;
        this.timeInStep = 0;
        this._loadTimeStep(this.currentTimeIndex);
        this._updateTimeLabel();
      }
    });
    this.timeLabel = document.getElementById('time-label');
    this._updateTimeLabel();
    document.getElementById('btn-prev').addEventListener('click', () => {
      if (this.currentTimeIndex > 0) {
        this.currentTimeIndex--;
        this.slider.value = this.currentTimeIndex;
        this.timeInStep = 0;
        this._loadTimeStep(this.currentTimeIndex);
        this._updateTimeLabel();
      }
    });
    document.getElementById('btn-next').addEventListener('click', () => {
      if (this.currentTimeIndex < this.config.timeSteps - 1) {
        this.currentTimeIndex++;
        this.slider.value = this.currentTimeIndex;
        this.timeInStep = 0;
        this._loadTimeStep(this.currentTimeIndex);
        this._updateTimeLabel();
      }
    });
    const autoBtn = document.getElementById('btn-auto-rotate');
    autoBtn.addEventListener('click', () => {
      this.autoRotate = !this.autoRotate;
      this.controls.autoRotate = this.autoRotate;
      autoBtn.classList.toggle('active', this.autoRotate);
    });
    document.getElementById('btn-bookmark').addEventListener('click', () => {
      this._saveBookmark();
    });
    this._renderBookmarks();
    this.dataLoader.onDataLoaded = (data, source) => {
      this._importExternalData(data, source);
    };
    this.dataLoader.setupDropZone();
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        if (this.currentTimeIndex > 0) {
          this.currentTimeIndex--;
          this.slider.value = this.currentTimeIndex;
          this.timeInStep = 0;
          this._loadTimeStep(this.currentTimeIndex);
          this._updateTimeLabel();
        }
      } else if (e.key === 'ArrowRight') {
        if (this.currentTimeIndex < this.config.timeSteps - 1) {
          this.currentTimeIndex++;
          this.slider.value = this.currentTimeIndex;
          this.timeInStep = 0;
          this._loadTimeStep(this.currentTimeIndex);
          this._updateTimeLabel();
        }
      } else if (e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        this.autoRotate = !this.autoRotate;
        this.controls.autoRotate = this.autoRotate;
        autoBtn.classList.toggle('active', this.autoRotate);
      }
    });
  }
  _updateTimeLabel() {
    const hour = this.currentTimeIndex;
    this.timeLabel.textContent = `${String(hour).padStart(2, '0')}:00`;
  }
  _loadTimeStep(timeIndex) {
    const cached = this.cache.get(timeIndex);
    if (cached) {
      this._applyCachedData(cached);
      this._prefetchAdjacent(timeIndex);
      return;
    }
    this._showLoading(true);
    this.cache.allocate(timeIndex);
    setTimeout(() => {
      const geometry = this.terrainBuilder.buildGeometry(timeIndex);
      const rivers = this.riverBuilder.buildRivers(timeIndex);
      if (this.terrainMesh) {
        this.terrainMesh.geometry.dispose();
        this.terrainMesh.geometry = geometry;
      } else {
        this.terrainMesh = new THREE.Mesh(geometry, this.terrainBuilder.getMaterial());
        this.terrainMesh.castShadow = !IS_MOBILE;
        this.terrainMesh.receiveShadow = !IS_MOBILE;
        this.scene.add(this.terrainMesh);
      }
      while (this.riverGroup.children.length > 0) {
        const child = this.riverGroup.children[0];
        if (child.geometry) child.geometry.dispose();
        this.riverGroup.remove(child);
      }
      for (const river of rivers) {
        this.riverGroup.add(river);
      }
      this.particleSystem.reset();
      this.timeInStep = 0;
      this.cache.populate(timeIndex, geometry, rivers, null);
      this._showLoading(false);
      this._updateStats();
      this._prefetchAdjacent(timeIndex);
    }, 10);
  }
  _applyCachedData(cached) {
    if (!cached || !cached.geometry) return;
    if (this.terrainMesh) {
      this.terrainMesh.geometry.dispose();
      this.terrainMesh.geometry = cached.geometry;
    } else {
      this.terrainMesh = new THREE.Mesh(cached.geometry, this.terrainBuilder.getMaterial());
      this.terrainMesh.castShadow = !IS_MOBILE;
      this.terrainMesh.receiveShadow = !IS_MOBILE;
      this.scene.add(this.terrainMesh);
    }
    while (this.riverGroup.children.length > 0) {
      const child = this.riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      this.riverGroup.remove(child);
    }
    if (cached.rivers) {
      for (const river of cached.rivers) {
        this.riverGroup.add(river);
      }
    }
    this.particleSystem.reset();
    this.timeInStep = 0;
    this._updateStats();
  }
  _prefetchAdjacent(currentIndex) {
    const toPrefetch = [];
    if (currentIndex > 0 && !this.cache.has(currentIndex - 1)) toPrefetch.push(currentIndex - 1);
    if (currentIndex < this.config.timeSteps - 1 && !this.cache.has(currentIndex + 1)) toPrefetch.push(currentIndex + 1);
    for (const idx of toPrefetch) {
      this.cache.allocate(idx);
      setTimeout(() => {
        if (!this.cache.has(idx)) {
          const geometry = this.terrainBuilder.buildGeometry(idx);
          const rivers = this.riverBuilder.buildRivers(idx);
          this.cache.populate(idx, geometry, rivers, null);
          this._updateStats();
        }
      }, 50);
    }
  }
  _importExternalData(data, source) {
    this.cache.clear();
    if (this.terrainMesh) {
      this.terrainMesh.geometry.dispose();
      this.scene.remove(this.terrainMesh);
      this.terrainMesh = null;
    }
    while (this.riverGroup.children.length > 0) {
      const child = this.riverGroup.children[0];
      if (child.geometry) child.geometry.dispose();
      this.riverGroup.remove(child);
    }
    if (Array.isArray(data)) {
      this.dataGen.data = data;
      this.config.timeSteps = data.length;
    } else if (data.timeSteps && Array.isArray(data.timeSteps)) {
      this.dataGen.data = data.timeSteps;
      this.config.timeSteps = data.timeSteps.length;
    }
    this.slider.max = this.config.timeSteps - 1;
    this.currentTimeIndex = Math.floor(this.config.timeSteps / 2);
    this.slider.value = this.currentTimeIndex;
    this.timeInStep = 0;
    this._updateTimeLabel();
    this._loadTimeStep(this.currentTimeIndex);
    this._showError(''); // clear
  }
  _saveBookmark() {
    const pos = this.camera.position.clone();
    const target = this.controls.target.clone();
    const name = `View ${this.bookmarks.length + 1} (t=${this.currentTimeIndex})`;
    this.bookmarks.push({ name, position: pos, target: target, timeIndex: this.currentTimeIndex });
    this._renderBookmarks();
  }
  _renderBookmarks() {
    const list = document.getElementById('bookmarks-list');
    list.innerHTML = '';
    for (let i = 0; i < this.bookmarks.length; i++) {
      const bm = this.bookmarks[i];
      const div = document.createElement('div');
      div.className = 'bookmark-item';
      div.innerHTML = `<span>${bm.name}</span><span class="del">×</span>`;
      div.querySelector('span').addEventListener('click', () => this._gotoBookmark(i));
      div.querySelector('.del').addEventListener('click', (e) => {
        e.stopPropagation();
        this.bookmarks.splice(i, 1);
        this._renderBookmarks();
      });
      list.appendChild(div);
    }
  }
  _gotoBookmark(index) {
    const bm = this.bookmarks[index];
    if (!bm) return;
    const startPos = this.camera.position.clone();
    const startTarget = this.controls.target.clone();
    const endPos = bm.position.clone();
    const endTarget = bm.target.clone();
    const duration = 800;
    const startTime = performance.now();
    if (bm.timeIndex !== undefined && bm.timeIndex !== this.currentTimeIndex) {
      this.currentTimeIndex = bm.timeIndex;
      this.slider.value = bm.timeIndex;
      this.timeInStep = 0;
      this._loadTimeStep(bm.timeIndex);
      this._updateTimeLabel();
    }
    const animate = (now) => {
      const elapsed = now - startTime;
      const t = Math.min(1, elapsed / duration);
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
      this.camera.position.lerpVectors(startPos, endPos, ease);
      this.controls.target.lerpVectors(startTarget, endTarget, ease);
      this.controls.update();
      if (t < 1) {
        requestAnimationFrame(animate);
      }
    };
    requestAnimationFrame(animate);
  }
  _showLoading(show) {
    const el = document.getElementById('loading-indicator');
    if (el) el.style.display = show ? 'flex' : 'none';
  }
  _showError(msg) {
    const toast = document.getElementById('error-toast');
    if (toast) {
      toast.textContent = msg || '';
      toast.style.display = msg ? 'block' : 'none';
      if (msg) setTimeout(() => { toast.style.display = 'none'; }, 4000);
    }
  }
  _updateStats() {
    const cacheStats = this.cache.getStats();
    document.getElementById('stat-cache').textContent = `${cacheStats.primed}/${cacheStats.entries}`;
    document.getElementById('stat-mem').textContent = `${cacheStats.memoryMB} MB`;
    document.getElementById('stat-time').textContent = `${String(this.currentTimeIndex).padStart(2, '0')}:00`;
    document.getElementById('stat-fps').textContent = this.fpsValue;
  }
  _animate() {
    requestAnimationFrame(() => this._animate());
    const delta = this.clock.getDelta();
    this.timeInStep += delta * 0.5;
    this.controls.update();
    this.particleSystem.update(this.currentTimeIndex, delta, this.timeInStep, this.terrainMesh);
    this.renderer.render(this.scene, this.camera);
    this.fpsFrames++;
    this.fpsTime += delta;
    if (this.fpsTime >= 0.5) {
      this.fpsValue = Math.round(this.fpsFrames / this.fpsTime);
      this.fpsFrames = 0;
      this.fpsTime = 0;
      document.getElementById('stat-fps').textContent = this.fpsValue;
    }
  }
}
// ─── BOOT ─────────────────────────────────────────────────────
const app = new DataTerrainApp();
</script>
</body>
</html>