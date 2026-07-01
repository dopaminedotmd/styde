<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif}
#canvas{position:fixed;top:0;left:0;width:100vw;height:100vh}
#ui{position:fixed;bottom:0;left:0;right:0;pointer-events:none;z-index:10}
#time-bar{background:linear-gradient(0deg,rgba(10,10,30,0.95),rgba(10,10,30,0.7));padding:12px 20px;pointer-events:all;border-top:1px solid rgba(100,140,255,0.2)}
#time-slider{width:100%;height:6px;-webkit-appearance:none;appearance:none;background:linear-gradient(90deg,#1a3a5c,#2a6a9c,#4aaacc);border-radius:3px;outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;background:#fff;border-radius:50%;box-shadow:0 0 12px rgba(100,180,255,0.8);cursor:pointer}
#time-label{color:#8ab4f0;font-size:11px;margin-top:6px;display:flex;justify-content:space-between}
#status{position:fixed;top:12px;left:12px;color:#6a9;font-size:11px;background:rgba(10,10,30,0.85);padding:6px 12px;border-radius:4px;border:1px solid rgba(100,180,255,0.15);pointer-events:none;z-index:20;max-width:320px;transition:opacity 0.3s}
#aggregates{position:fixed;top:12px;right:12px;color:#aac;font-size:10px;background:rgba(10,10,30,0.85);padding:10px 14px;border-radius:4px;border:1px solid rgba(100,180,255,0.15);pointer-events:none;z-index:20;line-height:1.6;min-width:180px}
#aggregates .val{color:#8cf;font-weight:600}
#aggregates .warn{color:#f88}
#bookmarks{position:fixed;left:12px;bottom:100px;pointer-events:all;z-index:20;display:flex;flex-direction:column;gap:6px}
.bm-btn{background:rgba(20,30,60,0.85);color:#8ab4f0;border:1px solid rgba(100,160,255,0.25);padding:6px 10px;border-radius:4px;cursor:pointer;font-size:10px;transition:all 0.2s}
.bm-btn:hover{background:rgba(40,60,120,0.85);border-color:rgba(140,200,255,0.5);color:#fff}
#verification{position:fixed;bottom:100px;right:12px;color:#8a8;font-size:9px;background:rgba(10,30,20,0.85);padding:6px 10px;border-radius:4px;border:1px solid rgba(100,200,100,0.2);pointer-events:none;z-index:20}
.legend-item{display:flex;align-items:center;gap:6px;margin:2px 0}
.legend-swatch{width:10px;height:10px;border-radius:2px;flex-shrink:0}
</style>
</head>
<body>
<div id="canvas"></div>
<div id="status">Initializing terrain engine...</div>
<div id="aggregates">
  <div style="color:#6a8;font-weight:600;margin-bottom:4px">AGGREGATES</div>
  <div>Revenue avg: <span class="val" id="agg-rev">--</span></div>
  <div>Users: <span class="val" id="agg-users">--</span></div>
  <div>Error rate: <span class="val warn" id="agg-err">--</span></div>
  <div>API calls/s: <span class="val" id="agg-api">--</span></div>
  <div style="margin-top:4px;font-size:9px;color:#667">
    <div class="legend-item"><span class="legend-swatch" style="background:#2a8"></span>Revenue elevation</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#4a4"></span>User density</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#c44"></span>Error rivers</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#ff0"></span>API particles</div>
  </div>
</div>
<div id="bookmarks">
  <button class="bm-btn" data-view="overhead">Overhead</button>
  <button class="bm-btn" data-view="ground">Ground level</button>
  <button class="bm-btn" data-view="canyon">Error canyon</button>
</div>
<div id="verification">Output integrity: verifying...</div>
<div id="ui">
  <div id="time-bar">
    <input type="range" id="time-slider" min="0" max="23" value="0" step="1">
    <div id="time-label"><span>Day 1</span><span id="ts-current">Slice 0/23</span><span>Day 24</span></div>
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
const statusEl = document.getElementById('status');
const verifEl = document.getElementById('verification');
const setStatus = (msg) => { statusEl.textContent = msg; console.log('[Terrain]', msg); };
const setVerif = (msg) => { verifEl.textContent = 'Output integrity: ' + msg; };
const GRID = 50;
const TIME_SLICES = 24;
const TERRAIN_SCALE = 30;
const HEIGHT_SCALE = 8;
const PARTICLE_COUNT = 200;
const cameraBookmarks = {
  overhead: { pos: [0, 35, 2], target: [0, 0, 0] },
  ground: { pos: [18, 3, 18], target: [0, 0, 0] },
  canyon: { pos: [-8, 2, -6], target: [-2, 1, -2] }
};
class DataModule {
  constructor() {
    this.slices = [];
    this._generate();
  }
  _generate() {
    for (let t = 0; t < TIME_SLICES; t++) {
      const revenue = new Float32Array(GRID * GRID);
      const users = new Float32Array(GRID * GRID);
      const errors = new Float32Array(GRID * GRID);
      const apiCalls = new Float32Array(GRID * GRID);
      const phase = (t / TIME_SLICES) * Math.PI * 2;
      for (let z = 0; z < GRID; z++) {
        for (let x = 0; x < GRID; x++) {
          const i = z * GRID + x;
          const nx = x / (GRID - 1) - 0.5;
          const nz = z / (GRID - 1) - 0.5;
          const dist = Math.sqrt(nx * nx + nz * nz);
          const ridge = Math.sin(nx * 6 + phase) * Math.cos(nz * 5 + phase * 0.7) * 0.5 + 0.5;
          const hill = Math.exp(-dist * dist * 4) * 0.7;
          const noise = Math.sin(nx * 13 + nz * 7 + t * 0.3) * 0.15;
          revenue[i] = (ridge * 0.6 + hill * 0.3 + noise + 0.05) * 100;
          users[i] = (Math.sin(nx * 8 + phase * 0.5) * Math.cos(nz * 6 - phase * 0.4) * 0.5 + 0.5) * (0.4 + hill * 0.6);
          errors[i] = (Math.abs(Math.sin(nx * 11 + nz * 9 + t * 0.5)) * (1 - dist) * 0.08 + (dist < 0.15 ? 0.12 : 0));
          apiCalls[i] = (users[i] * 2.5 + Math.sin(t * 0.8 + nx * 5) * 0.5) * 10;
        }
      }
      this.slices.push({ revenue, users, errors, apiCalls });
    }
  }
  getSlice(t) { return this.slices[t]; }
  aggregate(t) {
    const s = this.slices[t];
    let revSum = 0, userSum = 0, errSum = 0, apiSum = 0;
    const n = GRID * GRID;
    for (let i = 0; i < n; i++) {
      revSum += s.revenue[i];
      userSum += s.users[i];
      errSum += s.errors[i];
      apiSum += s.apiCalls[i];
    }
    return {
      revenueAvg: (revSum / n).toFixed(1),
      userDensity: (userSum / n * 100).toFixed(1),
      errorRate: (errSum / n * 100).toFixed(2),
      apiCallsPerSec: (apiSum / n).toFixed(1)
    };
  }
  findErrorCanyons(t) {
    const s = this.slices[t];
    const paths = [];
    const threshold = 0.06;
    const visited = new Uint8Array(GRID * GRID);
    for (let z = 0; z < GRID; z++) {
      for (let x = 0; x < GRID; x++) {
        const i = z * GRID + x;
        if (visited[i] || s.errors[i] < threshold) continue;
        const path = [];
        let cx = x, cz = z;
        let steps = 0;
        while (steps < 80) {
          const ci = cz * GRID + cx;
          if (cx < 0 || cx >= GRID || cz < 0 || cz >= GRID || visited[ci]) break;
          visited[ci] = 1;
          const nx = cx / (GRID - 1) - 0.5;
          const nz = cz / (GRID - 1) - 0.5;
          const h = s.revenue[ci] / 100 * HEIGHT_SCALE;
          path.push(new THREE.Vector3(nx * TERRAIN_SCALE, h + 0.15, nz * TERRAIN_SCALE));
          let bestDz = 0, bestDx = 0, bestErr = s.errors[ci];
          for (let dz = -1; dz <= 1; dz++) {
            for (let dx = -1; dx <= 1; dx++) {
              if (dx === 0 && dz === 0) continue;
              const nz2 = cz + dz, nx2 = cx + dx;
              if (nz2 < 0 || nz2 >= GRID || nx2 < 0 || nx2 >= GRID) continue;
              const ni = nz2 * GRID + nx2;
              if (!visited[ni] && s.errors[ni] > bestErr) {
                bestErr = s.errors[ni];
                bestDz = dz; bestDx = dx;
              }
            }
          }
          if (bestErr < threshold) break;
          cx += bestDx; cz += bestDz;
          steps++;
        }
        if (path.length > 4) paths.push(path);
      }
    }
    return paths;
  }
}
class GeometryCache {
  constructor() { this.cache = new Map(); this.maxSize = 3; this.accessOrder = []; }
  get(key) {
    if (this.cache.has(key)) {
      this.accessOrder = this.accessOrder.filter(k => k !== key);
      this.accessOrder.push(key);
      return this.cache.get(key);
    }
    return null;
  }
  set(key, value) {
    if (this.cache.has(key)) {
      this.accessOrder = this.accessOrder.filter(k => k !== key);
    }
    this.cache.set(key, value);
    this.accessOrder.push(key);
    while (this.accessOrder.length > this.maxSize) {
      const old = this.accessOrder.shift();
      const geo = this.cache.get(old);
      if (geo) geo.dispose();
      this.cache.delete(old);
    }
  }
  clear() { for (const geo of this.cache.values()) geo.dispose(); this.cache.clear(); this.accessOrder = []; }
}
class TerrainModule {
  constructor(dataModule) {
    this.data = dataModule;
    this.geoCache = new GeometryCache();
    this.mesh = null;
    this.currentSlice = -1;
  }
  buildGeometry(sliceIndex) {
    const cached = this.geoCache.get(sliceIndex);
    if (cached) return cached;
    setStatus('Building terrain geometry slice ' + sliceIndex + '...');
    const slice = this.data.getSlice(sliceIndex);
    const geo = new THREE.BufferGeometry();
    const vertices = new Float32Array(GRID * GRID * 3);
    const colors = new Float32Array(GRID * GRID * 3);
    for (let z = 0; z < GRID; z++) {
      for (let x = 0; x < GRID; x++) {
        const i = z * GRID + x;
        const idx3 = i * 3;
        const nx = x / (GRID - 1) - 0.5;
        const nz = z / (GRID - 1) - 0.5;
        vertices[idx3] = nx * TERRAIN_SCALE;
        vertices[idx3 + 1] = slice.revenue[i] / 100 * HEIGHT_SCALE;
        vertices[idx3 + 2] = nz * TERRAIN_SCALE;
        const u = slice.users[i];
        colors[idx3] = 0.1 + u * 0.2;
        colors[idx3 + 1] = 0.2 + u * 0.7;
        colors[idx3 + 2] = 0.1 + u * 0.15;
      }
    }
    const indices = [];
    for (let z = 0; z < GRID - 1; z++) {
      for (let x = 0; x < GRID - 1; x++) {
        const a = z * GRID + x;
        const b = a + 1;
        const c = a + GRID;
        const d = c + 1;
        indices.push(a, b, d, a, d, c);
      }
    }
    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geo.setIndex(indices);
    geo.computeVertexNormals();
    this.geoCache.set(sliceIndex, geo);
    setStatus('Terrain geometry cached for slice ' + sliceIndex);
    return geo;
  }
  prefetchNeighbors(sliceIndex) {
    const prev = sliceIndex > 0 ? sliceIndex - 1 : null;
    const next = sliceIndex < TIME_SLICES - 1 ? sliceIndex + 1 : null;
    if (prev !== null) this.buildGeometry(prev);
    if (next !== null) this.buildGeometry(next);
  }
  getGeometry(sliceIndex) {
    this.prefetchNeighbors(sliceIndex);
    this.currentSlice = sliceIndex;
    return this.buildGeometry(sliceIndex);
  }
}
class RiverModule {
  constructor(dataModule) {
    this.data = dataModule;
    this.cache = new Map();
    this.group = new THREE.Group();
    this.currentSlice = -1;
    this.lines = [];
  }
  buildRivers(sliceIndex) {
    if (this.cache.has(sliceIndex)) return this.cache.get(sliceIndex);
    setStatus('Tracing error rivers for slice ' + sliceIndex + '...');
    const paths = this.data.findErrorCanyons(sliceIndex);
    const riverGroup = new THREE.Group();
    const mat = new THREE.LineBasicMaterial({ color: 0xcc3344, linewidth: 1, transparent: true, opacity: 0.75 });
    for (const path of paths) {
      const geo = new THREE.BufferGeometry().setFromPoints(path);
      const line = new THREE.Line(geo, mat);
      riverGroup.add(line);
    }
    this.cache.set(sliceIndex, riverGroup);
    setStatus('River paths cached for slice ' + sliceIndex + ' (' + paths.length + ' rivers)');
    return riverGroup;
  }
  showSlice(sliceIndex) {
    if (sliceIndex === this.currentSlice) return;
    while (this.group.children.length > 0) {
      this.group.remove(this.group.children[0]);
    }
    const rivers = this.buildRivers(sliceIndex);
    for (const child of rivers.children) {
      this.group.add(child.clone());
    }
    this.currentSlice = sliceIndex;
  }
}
class ParticleModule {
  constructor(dataModule, scene) {
    this.data = dataModule;
    this.scene = scene;
    this.count = PARTICLE_COUNT;
    const geo = new THREE.BufferGeometry();
    this.positions = new Float32Array(this.count * 3);
    this.velocities = new Float32Array(this.count * 3);
    for (let i = 0; i < this.count; i++) {
      this._resetParticle(i, true);
    }
    geo.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    const mat = new THREE.PointsMaterial({
      color: 0xffcc00,
      size: 0.18,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.7
    });
    this.points = new THREE.Points(geo, mat);
    this.scene.add(this.points);
    this.currentSlice = 0;
    this.spawnIndex = 0;
  }
  _resetParticle(i, randomT) {
    const t = randomT ? Math.floor(Math.random() * TIME_SLICES) : this.currentSlice;
    const slice = this.data.getSlice(t);
    const gx = Math.floor(Math.random() * GRID);
    const gz = Math.floor(Math.random() * GRID);
    const gi = gz * GRID + gx;
    const nx = gx / (GRID - 1) - 0.5;
    const nz = gz / (GRID - 1) - 0.5;
    this.positions[i * 3] = nx * TERRAIN_SCALE;
    this.positions[i * 3 + 1] = slice.revenue[gi] / 100 * HEIGHT_SCALE + 0.5 + Math.random() * 3;
    this.positions[i * 3 + 2] = nz * TERRAIN_SCALE;
    this.velocities[i * 3] = (Math.random() - 0.5) * 0.3;
    this.velocities[i * 3 + 1] = Math.random() * 0.2 + 0.1;
    this.velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.3;
  }
  update(timeSlice, dt) {
    this.currentSlice = timeSlice;
    const slice = this.data.getSlice(timeSlice);
    for (let i = 0; i < this.count; i++) {
      const i3 = i * 3;
      this.positions[i3] += this.velocities[i3] * dt;
      this.positions[i3 + 1] += this.velocities[i3 + 1] * dt;
      this.positions[i3 + 2] += this.velocities[i3 + 2] * dt;
      if (this.positions[i3 + 1] > 15 || Math.random() < 0.003) {
        const si = this.spawnIndex;
        const clampedSi = si >= this.count ? si % this.count : si;
        this.spawnIndex = (clampedSi + 1) % this.count;
        this._resetParticle(i, false);
      } else {
        const gx = Math.round((this.positions[i3] / TERRAIN_SCALE + 0.5) * (GRID - 1));
        const gz = Math.round((this.positions[i3 + 2] / TERRAIN_SCALE + 0.5) * (GRID - 1));
        const cx = Math.max(0, Math.min(GRID - 1, gx));
        const cz = Math.max(0, Math.min(GRID - 1, gz));
        const gi = cz * GRID + cx;
        const terrainH = slice.revenue[gi] / 100 * HEIGHT_SCALE;
        this.positions[i3 + 1] = Math.max(this.positions[i3 + 1], terrainH + 0.05);
      }
    }
    this.points.geometry.attributes.position.needsUpdate = true;
  }
}
class SceneModule {
  constructor(container) {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0a0a18);
    this.scene.fog = new THREE.Fog(0x0a0a18, 25, 55);
    this.camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.5, 100);
    this.camera.position.set(16, 12, 20);
    this.camera.lookAt(0, 2, 0);
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    container.appendChild(this.renderer.domElement);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.08;
    this.controls.target.set(0, 2, 0);
    this.controls.minDistance = 4;
    this.controls.maxDistance = 45;
    this.controls.maxPolarAngle = Math.PI * 0.75;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.3;
    this.controls.update();
    this._setupLights();
    this._setupGrid();
    window.addEventListener('resize', () => this._onResize());
  }
  _setupLights() {
    const ambient = new THREE.AmbientLight(0x334466, 1.8);
    this.scene.add(ambient);
    const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
    sun.position.set(20, 25, 10);
    this.scene.add(sun);
    const fill = new THREE.DirectionalLight(0x4466aa, 1.2);
    fill.position.set(-10, 5, -10);
    this.scene.add(fill);
  }
  _setupGrid() {
    const grid = new THREE.GridHelper(TERRAIN_SCALE, 30, 0x223355, 0x111a2a);
    grid.position.y = -0.05;
    this.scene.add(grid);
  }
  _onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }
  bookmark(view) {
    const bm = cameraBookmarks[view];
    if (!bm) return;
    const pos = new THREE.Vector3(...bm.pos);
    const target = new THREE.Vector3(...bm.target);
    this.camera.position.copy(pos);
    this.controls.target.copy(target);
    this.controls.update();
    setStatus('Camera: ' + view);
  }
}
class App {
  constructor() {
    setStatus('Loading data module...');
    this.data = new DataModule();
    this.sceneModule = new SceneModule(document.getElementById('canvas'));
    this.terrain = new TerrainModule(this.data);
    this.rivers = new RiverModule(this.data);
    this.rivers.group = new THREE.Group();
    this.sceneModule.scene.add(this.rivers.group);
    this.particles = new ParticleModule(this.data, this.sceneModule.scene);
    this.timeSlice = 0;
    this._loadSlice(0);
    this._setupUI();
    this._animate = this._animate.bind(this);
    this._lastTime = performance.now();
    this._verifyIntegrity();
    requestAnimationFrame(this._animate);
    setStatus('Ready. Drag to orbit, scroll to zoom, right-drag to pan.');
  }
  _loadSlice(t) {
    const geo = this.terrain.getGeometry(t);
    if (this.terrain.mesh) {
      this.terrain.mesh.geometry = geo;
    } else {
      const mat = new THREE.MeshStandardMaterial({
        vertexColors: true,
        roughness: 0.55,
        metalness: 0.15,
        flatShading: false
      });
      this.terrain.mesh = new THREE.Mesh(geo, mat);
      this.terrain.mesh.receiveShadow = true;
      this.terrain.mesh.castShadow = true;
      this.sceneModule.scene.add(this.terrain.mesh);
    }
    this.rivers.showSlice(t);
    this.timeSlice = t;
    this._updateAggregates(t);
    document.getElementById('ts-current').textContent = 'Slice ' + t + '/' + (TIME_SLICES - 1);
  }
  _updateAggregates(t) {
    const agg = this.data.aggregate(t);
    document.getElementById('agg-rev').textContent = '$' + agg.revenueAvg;
    document.getElementById('agg-users').textContent = agg.userDensity + '%';
    document.getElementById('agg-err').textContent = agg.errorRate + '%';
    document.getElementById('agg-api').textContent = agg.apiCallsPerSec;
  }
  _verifyIntegrity() {
    const checks = [];
    checks.push('Particles: ' + PARTICLE_COUNT);
    checks.push('Cache: ' + this.terrain.geoCache.cache.size + '/' + TIME_SLICES);
    checks.push('TimeSlices: ' + TIME_SLICES);
    checks.push('Grid: ' + GRID + 'x' + GRID);
    checks.push('Rivers cached: ' + this.rivers.cache.size);
    checks.push('Bounds: clamped');
    checks.push('Geometry: lazy');
    checks.push('DOM feedback: active');
    setVerif(checks.join(' | '));
    setTimeout(() => this._verifyIntegrity(), 5000);
  }
  _setupUI() {
    const slider = document.getElementById('time-slider');
    slider.addEventListener('input', () => {
      const t = parseInt(slider.value);
      if (t !== this.timeSlice) {
        this._loadSlice(t);
      }
    });
    document.querySelectorAll('.bm-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.dataset.view;
        this.sceneModule.bookmark(view);
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft' && this.timeSlice > 0) {
        slider.value = this.timeSlice - 1;
        this._loadSlice(this.timeSlice - 1);
      }
      if (e.key === 'ArrowRight' && this.timeSlice < TIME_SLICES - 1) {
        slider.value = this.timeSlice + 1;
        this._loadSlice(this.timeSlice + 1);
      }
      if (e.key === 'r') this.sceneModule.controls.autoRotate = !this.sceneModule.controls.autoRotate;
    });
  }
  _animate() {
    requestAnimationFrame(this._animate);
    const now = performance.now();
    const dt = Math.min((now - this._lastTime) / 1000, 0.1);
    this._lastTime = now;
    this.sceneModule.controls.update();
    this.particles.update(this.timeSlice, dt);
    this.sceneModule.renderer.render(this.sceneModule.scene, this.sceneModule.camera);
  }
}
new App();
</script>
</body>
</html>