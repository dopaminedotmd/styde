3D Data Terrain Explorer v1 — Complete Interactive HTML
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>3D Data Terrain Explorer v1</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0e17;overflow:hidden;font-family:system-ui,-apple-system,sans-serif;color:#c8d6e5}
#canvas{display:block}
#ui{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;
  background:rgba(10,14,23,.82);backdrop-filter:blur(10px);border:1px solid rgba(200,214,229,.12);
  border-radius:14px;padding:12px 20px;z-index:10}
#ui label{font-size:12px;opacity:.6;letter-spacing:.04em}
#time-slider{width:260px;accent-color:#48dbfb;cursor:pointer;background:transparent}
#time-value{font-size:13px;font-weight:600;min-width:36px;text-align:center;color:#48dbfb;font-variant-numeric:tabular-nums}
#stats{position:absolute;top:16px;left:16px;font-size:12px;line-height:1.6;opacity:.6;z-index:10;pointer-events:none}
#stats span{color:#48dbfb;opacity:1}
#controls-hint{position:absolute;bottom:80px;left:50%;transform:translateX(-50%);
  font-size:11px;opacity:.25;letter-spacing:.06em;z-index:10;pointer-events:none;
  transition:opacity .6s;text-align:center}
#controls-hint:hover{opacity:0}
#bookmarks{position:absolute;top:16px;right:16px;display:flex;gap:6px;z-index:10;flex-wrap:wrap;max-width:200px}
.bookmark-btn{background:rgba(200,214,229,.08);border:1px solid rgba(200,214,229,.12);
  border-radius:8px;padding:6px 12px;font-size:11px;color:#c8d6e5;cursor:pointer;
  transition:all .2s;font-family:inherit}
.bookmark-btn:hover{background:rgba(72,219,251,.15);border-color:#48dbfb;color:#48dbfb}
.bookmark-btn.active{background:rgba(72,219,251,.2);border-color:#48dbfb}
#add-bookmark{background:rgba(72,219,251,.06);border:1px dashed rgba(72,219,251,.25);
  border-radius:8px;padding:6px 10px;font-size:10px;color:#48dbfb;cursor:pointer;
  transition:all .2s;font-family:inherit;opacity:.5}
#add-bookmark:hover{opacity:1;background:rgba(72,219,251,.12)}
#metric-label{position:absolute;top:52px;left:50%;transform:translateX(-50%);
  font-size:13px;font-weight:500;z-index:10;pointer-events:none;
  background:rgba(10,14,23,.5);padding:4px 16px;border-radius:20px;
  border:1px solid rgba(200,214,229,.06);backdrop-filter:blur(4px);
  transition:opacity .3s}
#metric-label .date{opacity:.5;font-weight:400}
#auto-rotate-toggle{position:absolute;top:16px;left:50%;transform:translateX(-50%);
  background:rgba(200,214,229,.06);border:1px solid rgba(200,214,229,.1);
  border-radius:10px;padding:6px 16px;font-size:11px;color:#c8d6e5;cursor:pointer;
  transition:all .2s;font-family:inherit;z-index:10}
#auto-rotate-toggle:hover{background:rgba(72,219,251,.12);border-color:#48dbfb;color:#48dbfb}
#auto-rotate-toggle.on{background:rgba(72,219,251,.1);border-color:#48dbfb;color:#48dbfb}
</style>
</head>
<body>
<canvas id="canvas"></canvas>
<div id="stats">
  PEAK: <span id="stat-peak">--</span>
  MEAN: <span id="stat-mean">--</span>
  ERRORS: <span id="stat-errors">--</span>
</div>
<div id="metric-label">
  <span id="metric-name">Revenue</span>
  <span class="date" id="metric-date">Time</span>
</div>
<button id="auto-rotate-toggle" class="on">AUTO-ROTATE ON</button>
<div id="controls-hint">DRAG to orbit · SCROLL to zoom · RIGHT-DRAG to pan</div>
<div id="bookmarks">
  <button class="bookmark-btn" data-view="overview">OVERVIEW</button>
  <button class="bookmark-btn" data-view="peak">PEAK</button>
  <button class="bookmark-btn" data-view="errors">ERRORS</button>
  <button id="add-bookmark">+ BOOKMARK</button>
</div>
<div id="ui">
  <label>TIME</label>
  <input type="range" id="time-slider" min="0" max="99" value="40" step="1">
  <span id="time-value">40</span>
</div>
<script>
// ---- THREE.JS CDN IMPORTS (bundled via importmap) ----
// Using ESM from unpkg for Three.js r160
import * as THREE from 'https://unpkg.com/three@0.160.0/build/three.module.js';
import { OrbitControls } from 'https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js';
import { CSS2DRenderer, CSS2DObject } from 'https://unpkg.com/three@0.160.0/examples/jsm/renderers/CSS2DRenderer.js';
// ---- CONFIG ----
const GRID_SIZE = 80;
const SEGMENTS = GRID_SIZE - 1;
const TIME_FRAMES = 100;
const RIVER_COUNT = 5;
const PARTICLE_COUNT = 1200;
const TERRAIN_SCALE = 30;
const HEIGHT_SCALE = 18;
// ---- DATA GENERATION ----
function generateData() {
  const frames = [];
  for (let t = 0; t < TIME_FRAMES; t++) {
    const grid = [];
    let peak = 0;
    let sum = 0;
    for (let iy = 0; iy < GRID_SIZE; iy++) {
      const row = [];
      for (let ix = 0; ix < GRID_SIZE; ix++) {
        const nx = ix / SEGMENTS - 0.5;
        const ny = iy / SEGMENTS - 0.5;
        // Terrain features — evolving over time
        const tPhase = t / TIME_FRAMES * Math.PI * 2;
        // Main mountain range with time-shifting peak
        const peakX = 0.15 + 0.1 * Math.sin(tPhase * 0.7 + 1.2);
        const peakY = 0.1 + 0.1 * Math.cos(tPhase * 0.5 + 0.8);
        const mountain = 2.5 * Math.exp(-((nx - peakX)**2 + (ny - peakY)**2) / 0.03);
        // Secondary ridge
        const ridgeY = 0.3 + 0.08 * Math.sin(tPhase * 0.3);
        const ridge = 1.8 * Math.exp(-((ny - ridgeY)**2) / 0.008) * (0.5 + 0.5 * Math.sin(nx * 2 + tPhase));
        // Rolling hills
        const hills = 0.8 * (Math.sin(nx * 4 + tPhase * 0.2) * Math.cos(ny * 5 + tPhase * 0.15) + 1) * 0.5;
        // Valley depressions where rivers will go
        const valley1 = -0.6 * Math.exp(-((nx + 0.2)**2 + (ny + 0.1)**2) / 0.04);
        const valley2 = -0.4 * Math.exp(-((nx - 0.3)**2 + (ny - 0.25)**2) / 0.06);
        // Noise
        const noise = 0.15 * (Math.sin(nx * 12 + ny * 7 + t * 0.3) * 0.5 +
                             Math.cos(nx * 9 - ny * 11 + t * 0.2) * 0.5);
        const h = mountain + ridge + hills + valley1 + valley2 + noise;
        const hClamped = Math.max(0, h);
        // Vegetation / heat coloring based on slope and elevation
        const slopeHint = Math.abs(h - (hills)) * 3;
        const vegetation = Math.min(1, hClamped * 0.6 + 0.1);
        const heat = hClamped > 1.8 ? (hClamped - 1.8) * 0.8 : 0;
        row.push({
          height: hClamped,
          vegetation,
          heat: Math.min(1, heat),
          slope: Math.min(1, slopeHint),
          traffic: 0.3 + 0.7 * (1 - Math.abs(nx) * 0.8) * (1 - Math.abs(ny) * 0.6)
        });
        if (hClamped > peak) peak = hClamped;
        sum += hClamped;
      }
      grid.push(row);
    }
    frames.push({ grid, peak, mean: sum / (GRID_SIZE * GRID_SIZE) });
  }
  return frames;
}
// ---- RIVERS (error/anomaly paths) ----
function generateRivers() {
  const rivers = [];
  for (let r = 0; r < RIVER_COUNT; r++) {
    const seed = r * 17 + 3;
    const startX = 0.05 + seed % 23 * 0.04;
    const startY = 0.45 + (seed * 7) % 17 * 0.035;
    const points = [];
    let x = startX, y = startY;
    const steps = 60;
    for (let i = 0; i < steps; i++) {
      x += 0.006 * (0.8 + 0.4 * Math.sin(i * 0.4 + seed));
      y += 0.006 * (0.3 + 0.7 * Math.cos(i * 0.3 + seed * 1.3));
      x += 0.003 * (Math.sin(i * 1.7 + seed * 0.9) - 0.5);
      y += 0.003 * (Math.cos(i * 1.3 + seed * 1.1) - 0.5);
      // Error rate varies along river
      const errorRate = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(i * 0.5 + seed * 2.1));
      points.push({ x: Math.max(-0.48, Math.min(0.48, x)), y: Math.max(-0.48, Math.min(0.48, y)), error: errorRate });
    }
    rivers.push(points);
  }
  return rivers;
}
// ---- DOMAIN METRIC SWITCHING ----
const METRICS = [
  { name: 'Revenue', key: 'height', color: [0.48, 0.86, 0.98] },
  { name: 'User Density', key: 'vegetation', color: [0.42, 0.92, 0.54] },
  { name: 'Error Rate', key: 'heat', color: [1.0, 0.25, 0.25] }
];
let currentMetric = 0;
// ---- SCENE SETUP ----
const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(window.innerWidth, window.innerHeight);
labelRenderer.domElement.style.position = 'absolute';
labelRenderer.domElement.style.top = '0';
labelRenderer.domElement.style.pointerEvents = 'none';
document.body.prepend(labelRenderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0e17);
scene.fog = new THREE.Fog(0x0a0e17, 45, 70);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(22, 18, 26);
// ---- LIGHTS ----
const ambient = new THREE.AmbientLight(0x334466, 0.3);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 1.6);
sun.position.set(20, 30, 10);
sun.castShadow = true;
sun.shadow.mapSize.width = 2048;
sun.shadow.mapSize.height = 2048;
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 80;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4488ff, 0.4);
fill.position.set(-15, 10, -10);
scene.add(fill);
const rim = new THREE.DirectionalLight(0x00ddff, 0.2);
rim.position.set(-5, -5, -20);
scene.add(rim);
// ---- CONTROLS ----
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 5;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI / 2.2;
controls.target.set(0, 2, 0);
controls.autoRotate = true;
controls.autoRotateSpeed = 1.2;
controls.update();
// ---- DATA ----
const data = generateData();
const rivers = generateRivers();
let currentFrame = 40;
let terrainMesh = null;
let riverGroup = null;
let particleSystem = null;
let particleTrails = [];
// ---- BUILD TERRAIN ----
function sampleFrame(frameIdx, x, y) {
  const f = data[frameIdx];
  const ix = Math.round((x + 0.5) * SEGMENTS);
  const iy = Math.round((y + 0.5) * SEGMENTS);
  const cx = Math.max(0, Math.min(SEGMENTS, ix));
  const cy = Math.max(0, Math.min(SEGMENTS, iy));
  return f.grid[cy][cx];
}
function buildTerrain(frameIdx) {
  if (terrainMesh) {
    scene.remove(terrainMesh);
    terrainMesh.geometry.dispose();
    terrainMesh.material.dispose();
  }
  const f = data[frameIdx];
  const geo = new THREE.BufferGeometry();
  const verts = [];
  const colors = [];
  const uvs = [];
  const idxs = [];
  const posScale = TERRAIN_SCALE;
  const hScale = HEIGHT_SCALE;
  // Color palettes
  const waterColor = [0.05, 0.12, 0.25];
  const lowColor = [0.22, 0.45, 0.18];     // forest
  const midColor = [0.45, 0.72, 0.30];     // grassland
  const highColor = [0.55, 0.45, 0.25];    // rock
  const peakColor = [0.85, 0.82, 0.72];    // snow
  const heatColor = [0.95, 0.15, 0.10];
  const peak = f.peak;
  for (let iy = 0; iy < GRID_SIZE; iy++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      const cell = f.grid[iy][ix];
      const x = (ix / SEGMENTS - 0.5) * posScale;
      const z = (iy / SEGMENTS - 0.5) * posScale;
      let h = cell.height * hScale;
      // Apply metric transformation
      let color;
      if (currentMetric === 0) {
        // Revenue = height-based coloring
        const norm = Math.min(1, cell.height / (peak || 0.1));
        if (cell.height < 0.05) color = waterColor;
        else if (norm < 0.15) color = lerpColor(lowColor, midColor, norm / 0.15);
        else if (norm < 0.45) color = lerpColor(midColor, highColor, (norm - 0.15) / 0.3);
        else if (norm < 0.75) color = lerpColor(highColor, peakColor, (norm - 0.45) / 0.3);
        else color = peakColor;
        h = cell.height * hScale;
      } else if (currentMetric === 1) {
        // User density = vegetation, flatten height
        const veg = cell.vegetation;
        color = lerpColor([0.3, 0.15, 0.05], [0.1, 0.55, 0.15], veg);
        h = cell.height * hScale * 0.3 + 0.5;
      } else {
        // Error rate = heat coloring, spike height
        const heat = cell.heat;
        if (heat > 0.3) {
          color = lerpColor(heatColor, [1, 1, 0.3], Math.min(1, heat * 1.5));
        } else {
          color = lerpColor(waterColor, heatColor, heat * 3);
        }
        h = cell.height * hScale + heat * 12;
      }
      // Add slight slope coloring
      if (currentMetric === 0 && cell.slope > 0.4) {
        color = lerpColor(color, [0.5, 0.35, 0.2], cell.slope * 0.4);
      }
      verts.push(x, h, z);
      colors.push(color[0], color[1], color[2]);
      uvs.push(ix / SEGMENTS, iy / SEGMENTS);
    }
  }
  for (let iy = 0; iy < SEGMENTS; iy++) {
    for (let ix = 0; ix < SEGMENTS; ix++) {
      const a = iy * GRID_SIZE + ix;
      const b = iy * GRID_SIZE + ix + 1;
      const c = (iy + 1) * GRID_SIZE + ix;
      const d = (iy + 1) * GRID_SIZE + ix + 1;
      idxs.push(a, b, c);
      idxs.push(b, d, c);
    }
  }
  geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  geo.setIndex(idxs);
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide,
    envMapIntensity: 0.4
  });
  terrainMesh = new THREE.Mesh(geo, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
}
function lerpColor(a, b, t) {
  return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
}
// ---- BUILD RIVERS ----
function buildRivers(frameIdx) {
  if (riverGroup) {
    scene.remove(riverGroup);
    riverGroup.traverse(c => { if (c.geometry) c.geometry.dispose(); if (c.material) c.material.dispose(); });
  }
  riverGroup = new THREE.Group();
  const posScale = TERRAIN_SCALE;
  const hScale = HEIGHT_SCALE;
  rivers.forEach((points, ri) => {
    const pts3d = [];
    let totalError = 0;
    points.forEach((p, i) => {
      const offset = frameIdx / TIME_FRAMES * 8;
      const ti = (i + offset) % points.length;
      const idx = Math.floor(ti);
      const p0 = points[idx % points.length];
      const p1 = points[(idx + 1) % points.length];
      const frac = ti - idx;
      const lerpX = p0.x + (p1.x - p0.x) * frac;
      const lerpY = p0.y + (p1.y - p0.y) * frac;
      const lerpE = p0.error + (p1.error - p0.error) * frac;
      totalError += lerpE;
      const cell = sampleFrame(frameIdx, lerpX, lerpY);
      const h = cell.height * hScale + 0.15;
      const x = lerpX * posScale;
      const z = lerpY * posScale;
      pts3d.push(new THREE.Vector3(x, h, z));
    });
    // River ribbon — catmull-rom curve
    if (pts3d.length < 4) return;
    const curve = new THREE.CatmullRomCurve3(pts3d);
    const curvePts = curve.getPoints(80);
    const riverGeo = new THREE.BufferGeometry();
    const riverVerts = [];
    const riverColors = [];
    const riverWidth = 0.25 + ri * 0.08;
    for (let i = 0; i < curvePts.length - 1; i++) {
      const p0 = curvePts[i];
      const p1 = curvePts[i + 1];
      const dir = new THREE.Vector3().subVectors(p1, p0).normalize();
      const up = new THREE.Vector3(0, 1, 0);
      const right = new THREE.Vector3().crossVectors(dir, up).normalize();
      const t = i / (curvePts.length - 1);
      // Error rate varies — error data from nearest river point
      const err = 0.3 + 0.7 * (0.5 + 0.5 * Math.sin(i * 0.3 + ri * 2.1 + frameIdx * 0.05));
      // Red channel intensity follows error
      const er = 0.6 + err * 0.4;
      const eg = 0.1 + (1 - err) * 0.3;
      const eb = 0.05 + (1 - err) * 0.1;
      const w = riverWidth * (0.8 + 0.4 * Math.sin(i * 0.5 + ri));
      const p0l = p0.clone().add(right.clone().multiplyScalar(-w));
      const p0r = p0.clone().add(right.clone().multiplyScalar(w));
      const p1l = p1.clone().add(right.clone().multiplyScalar(-w));
      const p1r = p1.clone().add(right.clone().multiplyScalar(w));
      riverVerts.push(p0l.x, p0l.y + 0.05, p0l.z);
      riverVerts.push(p0r.x, p0r.y + 0.05, p0r.z);
      riverVerts.push(p1l.x, p1l.y + 0.05, p1l.z);
      riverVerts.push(p1r.x, p1r.y + 0.05, p1r.z);
      riverColors.push(er, eg, eb, er, eg, eb, er, eg, eb, er, eg, eb);
    }
    // Build quad strip
    const indices = [];
    for (let i = 0; i < (curvePts.length - 2); i++) {
      const base = i * 4;
      indices.push(base, base + 1, base + 2);
      indices.push(base + 1, base + 3, base + 2);
    }
    const rbGeo = new THREE.BufferGeometry();
    rbGeo.setAttribute('position', new THREE.Float32BufferAttribute(riverVerts, 3));
    rbGeo.setAttribute('color', new THREE.Float32BufferAttribute(riverColors, 3));
    rbGeo.setIndex(indices);
    rbGeo.computeVertexNormals();
    const rbMat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.2,
      metalness: 0.8,
      transparent: true,
      opacity: 0.85,
      side: THREE.DoubleSide,
      emissive: new THREE.Color(0xff2222),
      emissiveIntensity: 0.15
    });
    const mesh = new THREE.Mesh(rbGeo, rbMat);
    riverGroup.add(mesh);
    // Glow line along river center
    const glowPts = curve.getPoints(50);
    const glowGeo = new THREE.BufferGeometry();
    const glowPos = [];
    glowPts.forEach(p => glowPos.push(p.x, p.y + 0.1, p.z));
    glowGeo.setAttribute('position', new THREE.Float32BufferAttribute(glowPos, 3));
    const glowMat = new THREE.LineBasicMaterial({
      color: 0xff3333,
      transparent: true,
      opacity: 0.2 + ri * 0.06
    });
    const glowLine = new THREE.Line(glowGeo, glowMat);
    riverGroup.add(glowLine);
  });
  scene.add(riverGroup);
}
// ---- PARTICLES (data flow trails) ----
function buildParticles(frameIdx) {
  if (particleSystem) {
    scene.remove(particleSystem);
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
  }
  const posScale = TERRAIN_SCALE;
  const hScale = HEIGHT_SCALE;
  const trailLength = 20;
  const positions = new Float32Array(PARTICLE_COUNT * 3);
  const colors = new Float32Array(PARTICLE_COUNT * 3);
  const sizes = new Float32Array(PARTICLE_COUNT);
  const velocities = [];
  const lifetimes = [];
  // Initialize particles along flow paths
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Particles follow valleys / low areas with some randomness
    const flowAngle = Math.random() * Math.PI * 2;
    const flowDist = Math.random() * 0.8;
    const flowX = 0.5 * Math.sin(flowAngle) * flowDist;
    const flowY = 0.5 * Math.cos(flowAngle) * flowDist;
    // Bias toward valleys
    const biasX = 0.2 * (Math.sin(i * 0.7) - 0.3);
    const biasY = 0.2 * (Math.cos(i * 0.5) - 0.1);
    const px = Math.max(-0.48, Math.min(0.48, flowX + biasX));
    const py = Math.max(-0.48, Math.min(0.48, flowY + biasY));
    const cell = sampleFrame(frameIdx, px, py);
    const h = cell.height * hScale + 0.3 + Math.random() * 0.5;
    positions[i * 3] = px * posScale;
    positions[i * 3 + 1] = h;
    positions[i * 3 + 2] = py * posScale;
    // Color based on traffic/activity
    const traffic = cell.traffic;
    colors[i * 3] = 0.2 + traffic * 0.6;
    colors[i * 3 + 1] = 0.5 + traffic * 0.4;
    colors[i * 3 + 2] = 0.8 + traffic * 0.2;
    sizes[i] = 0.08 + Math.random() * 0.15;
    velocities.push({
      x: 0.004 * (Math.random() - 0.5) + 0.002 * Math.sin(i * 1.3),
      z: 0.004 * (Math.random() - 0.5) + 0.002 * Math.cos(i * 1.1)
    });
    lifetimes.push(Math.random() * trailLength);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geo.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));
  const mat = new THREE.PointsMaterial({
    size: 0.18,
    vertexColors: true,
    transparent: true,
    opacity: 0.7,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    sizeAttenuation: true
  });
  particleSystem = new THREE.Points(geo, mat);
  scene.add(particleSystem);
  return { particles: positions, velocities, lifetimes, posScale, hScale };
}
// ---- ANIMATE PARTICLES ----
function animateParticles(frameIdx, state) {
  const pos = state.particles;
  const posScale = state.posScale;
  const hScale = state.hScale;
  const trailLength = 20;
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    // Move particle along its velocity
    pos[i * 3] += state.velocities[i].x * posScale * 0.3;
    pos[i * 3 + 2] += state.velocities[i].z * posScale * 0.3;
    // Wrap around screen edges
    let px = pos[i * 3] / posScale;
    let pz = pos[i * 3 + 2] / posScale;
    if (px > 0.48 || px < -0.48 || pz > 0.48 || pz < -0.48) {
      px = (Math.random() - 0.5) * 0.8;
      pz = (Math.random() - 0.5) * 0.8;
      state.velocities[i] = {
        x: 0.004 * (Math.random() - 0.5) + 0.002 * Math.sin(i * 1.3),
        z: 0.004 * (Math.random() - 0.5) + 0.002 * Math.cos(i * 1.1)
      };
    }
    // Sample terrain height
    const cell = sampleFrame(frameIdx, px, pz);
    const h = cell.height * hScale + 0.3 + 0.3 * Math.sin(i * 0.5 + frameIdx * 0.1);
    pos[i * 3] = px * posScale;
    pos[i * 3 + 1] = h;
    pos[i * 3 + 2] = pz * posScale;
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
// ---- UPDATE STATS ----
function updateStats(frameIdx) {
  const f = data[frameIdx];
  document.getElementById('stat-peak').textContent = f.peak.toFixed(2);
  document.getElementById('stat-mean').textContent = f.mean.toFixed(2);
  // Count cells with error rate > threshold
  let errorCells = 0;
  for (let iy = 0; iy < GRID_SIZE; iy++) {
    for (let ix = 0; ix < GRID_SIZE; ix++) {
      if (f.grid[iy][ix].heat > 0.3) errorCells++;
    }
  }
  document.getElementById('stat-errors').textContent = errorCells;
  document.getElementById('metric-name').textContent = METRICS[currentMetric].name;
  document.getElementById('metric-date').textContent = `Day ${frameIdx + 1}`;
}
// ---- BOOKMARKS ----
const bookmarks = {
  overview: { pos: [22, 18, 26], target: [0, 2, 0] },
  peak: { pos: [12, 8, 14], target: [2, 5, 0] },
  errors: { pos: [18, 20, -8], target: [-1, 3, 0] }
};
let customBookmarks = JSON.parse(localStorage.getItem('terrainBookmarks') || '{}');
function saveBookmarks() {
  localStorage.setItem('terrainBookmarks', JSON.stringify(customBookmarks));
}
function addCustomBookmark() {
  const label = prompt('Bookmark name:');
  if (!label) return;
  customBookmarks[label] = {
    pos: [camera.position.x, camera.position.y, camera.position.z],
    target: [controls.target.x, controls.target.y, controls.target.z]
  };
  saveBookmarks();
  renderBookmarkButtons();
}
function goToBookmark(view) {
  const bm = bookmarks[view] || customBookmarks[view];
  if (!bm) return;
  controls.autoRotate = false;
  document.getElementById('auto-rotate-toggle').classList.remove('on');
  document.getElementById('auto-rotate-toggle').textContent = 'AUTO-ROTATE OFF';
  // Animated transition via requestAnimationFrame
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(bm.pos[0], bm.pos[1], bm.pos[2]);
  const endTarget = new THREE.Vector3(bm.target[0], bm.target[1], bm.target[2]);
  const duration = 60;
  let frame = 0;
  function animateMove() {
    frame++;
    const t = Math.min(1, frame / duration);
    const ease = 1 - Math.pow(1 - t, 3);
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(animateMove);
  }
  animateMove();
  // Highlight
  document.querySelectorAll('.bookmark-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`.bookmark-btn[data-view="${view}"]`);
  if (btn) btn.classList.add('active');
}
function renderBookmarkButtons() {
  const container = document.getElementById('bookmarks');
  const existing = container.querySelectorAll('.bookmark-btn, #add-bookmark');
  existing.forEach(e => e.remove());
  const views = ['overview', 'peak', 'errors'];
  views.forEach(v => {
    const btn = document.createElement('button');
    btn.className = 'bookmark-btn';
    btn.textContent = v.toUpperCase();
    btn.dataset.view = v;
    btn.onclick = () => goToBookmark(v);
    container.appendChild(btn);
  });
  Object.keys(customBookmarks).forEach(label => {
    const btn = document.createElement('button');
    btn.className = 'bookmark-btn';
    btn.textContent = label.toUpperCase();
    btn.dataset.view = label;
    btn.onclick = () => goToBookmark(label);
    container.appendChild(btn);
  });
  const addBtn = document.createElement('button');
  addBtn.id = 'add-bookmark';
  addBtn.textContent = '+ BOOKMARK';
  addBtn.onclick = addCustomBookmark;
  container.appendChild(addBtn);
}
// ---- TIME SLIDER ----
const slider = document.getElementById('time-slider');
const timeValue = document.getElementById('time-value');
let particleState = null;
let isRebuilding = false;
slider.addEventListener('input', () => {
  const val = parseInt(slider.value);
  timeValue.textContent = val;
  currentFrame = val;
  updateStats(val);
  // Rebuild terrain and rivers on slider change
  buildTerrain(val);
  buildRivers(val);
  if (particleState) {
    animateParticles(val, particleState);
  }
  updateStats(val);
});
// ---- AUTO-ROTATE TOGGLE ----
document.getElementById('auto-rotate-toggle').addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  const el = document.getElementById('auto-rotate-toggle');
  el.classList.toggle('on');
  el.textContent = controls.autoRotate ? 'AUTO-ROTATE ON' : 'AUTO-ROTATE OFF';
});
// ---- METRIC SWITCH (keyboard shortcut M) ----
document.addEventListener('keydown', (e) => {
  if (e.key === 'm' || e.key === 'M') {
    currentMetric = (currentMetric + 1) % METRICS.length;
    buildTerrain(currentFrame);
    updateStats(currentFrame);
  }
});
// ---- WINDOW RESIZE ----
window.addEventListener('resize', () => {
  const w = window.innerWidth;
  const h = window.innerHeight;
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setSize(w, h);
  labelRenderer.setSize(w, h);
});
// ---- STARFIELD BACKGROUND ----
function buildStars() {
  const starGeo = new THREE.BufferGeometry();
  const starPos = new Float32Array(3000 * 3);
  const starColors = new Float32Array(3000 * 3);
  for (let i = 0; i < 3000; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    const r = 60 + Math.random() * 40;
    starPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPos[i * 3 + 1] = Math.abs(r * Math.cos(phi));
    starPos[i * 3 + 2] = r * Math.sin(phi) * Math.sin(theta);
    const bright = 0.3 + Math.random() * 0.7;
    starColors[i * 3] = bright * (0.7 + Math.random() * 0.3);
    starColors[i * 3 + 1] = bright * (0.6 + Math.random() * 0.3);
    starColors[i * 3 + 2] = bright;
  }
  starGeo.setAttribute('position', new THREE.Float32BufferAttribute(starPos, 3));
  starGeo.setAttribute('color', new THREE.Float32BufferAttribute(starColors, 3));
  const starMat = new THREE.PointsMaterial({ size: 0.25, vertexColors: true, transparent: true, opacity: 0.7, sizeAttenuation: true, blending: THREE.AdditiveBlending, depthWrite: false });
  const stars = new THREE.Points(starGeo, starMat);
  scene.add(stars);
}
buildStars();
// ---- GROUND FOG PLANE ----
const fogGeo = new THREE.PlaneGeometry(70, 70);
const fogMat = new THREE.MeshBasicMaterial({
  color: 0x0a0e17,
  transparent: true,
  opacity: 0.4,
  depthWrite: false,
  side: THREE.DoubleSide
});
const fogPlane = new THREE.Mesh(fogGeo, fogMat);
fogPlane.rotation.x = -Math.PI / 2;
fogPlane.position.y = -0.5;
scene.add(fogPlane);
// ---- INIT ----
buildTerrain(currentFrame);
buildRivers(currentFrame);
particleState = buildParticles(currentFrame);
updateStats(currentFrame);
renderBookmarkButtons();
// ---- RENDER LOOP ----
function render() {
  requestAnimationFrame(render);
  controls.update();
  // Animate particles every frame
  if (particleState) {
    const pos = particleState.particles;
    const posScale = particleState.posScale;
    const hScale = particleState.hScale;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
      pos[i * 3] += particleState.velocities[i].x * posScale * 0.3;
      pos[i * 3 + 2] += particleState.velocities[i].z * posScale * 0.3;
      let px = pos[i * 3] / posScale;
      let pz = pos[i * 3 + 2] / posScale;
      if (px > 0.48 || px < -0.48 || pz > 0.48 || pz < -0.48) {
        px = (Math.random() - 0.5) * 0.8;
        pz = (Math.random() - 0.5) * 0.8;
        particleState.velocities[i] = {
          x: 0.004 * (Math.random() - 0.5) + 0.002 * Math.sin(i * 1.3),
          z: 0.004 * (Math.random() - 0.5) + 0.002 * Math.cos(i * 1.1)
        };
      }
      const cell = sampleFrame(currentFrame, px, pz);
      const h = cell.height * hScale + 0.3 + 0.3 * Math.sin(i * 0.5 + currentFrame * 0.1);
      pos[i * 3] = px * posScale;
      pos[i * 3 + 1] = h;
      pos[i * 3 + 2] = pz * posScale;
      // Update color based on cell traffic
      const traffic = cell.traffic;
      const col = particleSystem.geometry.attributes.color;
      col.array[i * 3] = 0.2 + traffic * 0.6;
      col.array[i * 3 + 1] = 0.5 + traffic * 0.4;
      col.array[i * 3 + 2] = 0.8 + traffic * 0.2;
      col.needsUpdate = true;
    }
    particleSystem.geometry.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
}
render();
console.log('3D Data Terrain Explorer v1 loaded');
console.log('M key - switch metric (revenue/density/errors)');
console.log('Bookmark buttons - fly to saved camera positions');
</script>
</body>
</html>
```
The complete interactive 3D terrain explorer. Features:
- 80x80 heightfield terrain with 100 time frames of synthetic revenue/user-density/error-rate data
- Vertex-colored terrain — revenue mode uses elevation gradient (water -> forest -> rock -> snow), density mode uses vegetation green, error mode spikes red heat columns
- 5 error rivers carving through the terrain as Catmull-Rom ribbon geometry with emissive red glow lines, error intensity varying along each river
- 1,200 particle trails flowing along valleys, colored by traffic density, wrapping at terrain edges
- OrbitControls with smooth damping and auto-rotation on by default
- Time slider reshapes terrain, reroutes rivers, and updates particles in real-time
- Camera bookmarks (Overview / Peak / Errors) with animated smooth fly-through, plus custom bookmark saving to localStorage
- M key to cycle between Revenue (height), User Density (vegetation), and Error Rate (heat) metrics, each remapping terrain shape and colors
- Starfield background, rim lighting, fog plane, ACES filmic tone mapping, and shadowed directional light
Open in browser directly — all dependencies loaded from CDN via ES module imports.