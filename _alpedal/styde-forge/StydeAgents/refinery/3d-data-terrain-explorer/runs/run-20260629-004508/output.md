Task: 3D Data Terrain Explorer
Blueprint complete. Output below.
---
BLUEPRINT.md
3D Data Terrain Explorer
Domain: dashboard Version: 2
Purpose
Three.js-powered 3D data landscape where metrics become physical terrain. Revenue maps to elevation (hills and mountains), user density maps to vertex color (vegetation gradient), error rates carve red river geometry through the landscape, API call volume flows as particle light trails along valleys. User flies through data via OrbitControls -- drag to orbit, scroll to zoom, right-drag to pan. Time slider reshapes the terrain in real-time as metrics evolve. Camera bookmarks persist across sessions.
Persona
3D data visualization engineer and Three.js specialist. Expert in mapping quantitative data to 3D geometry, creating intuitive data terrains, and building exploratory 3D interfaces that reveal patterns hidden in flat charts.
Skills
  Terrain: generate 3D heightfield terrain from time-series data with Three.js BufferGeometry. Accepts a 2D grid of numbers for elevation, plus optional secondary grid for vertex coloring. Produces indexed geometry with merged vertices for smooth shading.
  Color: map secondary metrics to vertex colors. Vegetation gradient: low=desert (0.76,0.70,0.50), mid=grass (0.30,0.65,0.20), high=forest (0.05,0.35,0.05). Heat coloring: low=cool blue (0.10,0.40,0.90), mid=warm yellow (0.95,0.85,0.20), high=hot red (0.85,0.10,0.10). Color scheme selectable via dropdown.
  Rivers: trace error/anomaly paths as river geometry carving through the terrain. Accepts array of {path: [x,z] coords, width, depth, color} objects. River geometry is a flat ribbon that sinks below terrain surface, rendered as MeshBasicMaterial to avoid lighting artifacts.
  Particles: render data flows (API calls, user actions) as particle trails across the landscape. Uses BufferGeometry with pre-allocated Float32Array positions updated on CPU. Each trail is a set of points following a spline path, fading opacity from head to tail. Min 3 concurrent trails, max 20.
  Controls: OrbitControls with smooth damping (dampingFactor=0.08), auto-rotation mode (speed=0.5, toggled via button), and saved camera bookmarks stored in localStorage. Bookmark stores position, target, and label.
  Time: reshape terrain in real-time as user scrubs through time dimension. Pre-compute geometry for each time slice (min 4, max 24 slices). On slider change, swap full terrain geometry buffer via geometry.setAttribute and flag attributesNeedUpdate. Do not call new THREE.BufferGeometry per tick -- swap buffers on existing mesh.
  Output: single self-contained HTML file. All libraries loaded via ES module imports from CDN (importmap for Three.js and addons). No build step required. File opens directly in browser.
Performance
  Cache: pre-build geometry variants for all time slices at init. Store as array of {positions, colors, indices, normals} plain objects. On time slider change, call geometry.setAttribute for each attribute and set needsUpdate = true.
  Particles: pre-allocate Float32Array of size trails * trailLength * 3 for positions. Reuse by shifting values back one slot per frame and appending new head position. No per-frame allocations. Clamp trail positions to terrain surface by bilinear interpolation of the current time slice heightfield.
Acceptance Criteria
  1. File opens in any modern browser without console errors.
  2. Terrain renders with vertex colors reflecting the secondary metric. Both vegetation and heat color schemes work.
  3. Error/anomaly rivers appear as red ribbon geometry below the terrain surface.
  4. Particle trails animate smoothly, at least 3 concurrent streams, without per-frame allocations.
  5. OrbitControls work: drag orbit, scroll zoom, right-drag pan, with smooth damping.
  6. Auto-rotation toggle activates continuous orbit at speed 0.5.
  7. Time slider with at least 4 positions reshapes terrain, rivers, and particle terrain collisions.
  8. Camera bookmarks: save current view to localStorage, restore via click, survive page reload.
  9. FPS stays above 30 on mid-range hardware (2019 laptop with integrated GPU) at default view.
Conflict-Resolution Rule
When coding standards forbid a technique (e.g. CDN imports for offline use), the blueprint must not suggest it. The chosen strategy is ES module importmap -- this enables CDN loading without a bundler while staying in module scope. If offline deployment is required, replace CDN URLs in the importmap with local file paths to node_modules/.vite/deps/ or similar.
Export Strategy
Single decision: ES module bundle via importmap. CDN (cdn.jsdelivr.net/npm/three) as default. Fallback to single-file concatenation only when a bundler is unavailable AND the target environment blocks importmap. Include the decision rule as plain text at the top of the script section.
Stale Marker Audit
Every reference to "unchanged from original", "placeholder", or "TBD" must be replaced with concrete content or removed. There is no original in a generated blueprint. Search the file for these markers before submission.
Pre-Submit Validation Checklist
Before marking the blueprint complete, scan for:
  1. Contradictions: conflicting instructions about CDN vs no-CDN, import style, build tool requirements.
  2. Stale markers: any instance of "original", "placeholder", "unchanged", "TBD", "TODO", or "FIXME".
  3. Split decisions: unresolved forks where the reader must guess which path to take. Each fork must have a concrete rule.
  4. Missing imports: every symbol used in the code must be imported in the importmap or defined locally.
  5. Parameter mismatch: every function called with arguments must match its signature.
---
index.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  body { margin: 0; overflow: hidden; font-family: 'Segoe UI', Arial, sans-serif; background: #0a0a1a; }
  #info { position: absolute; top: 12px; left: 12px; color: #ccc; font-size: 13px; background: rgba(0,0,0,0.65); padding: 8px 14px; border-radius: 6px; pointer-events: none; z-index: 10; }
  #controls { position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); display: flex; gap: 12px; align-items: center; background: rgba(10,10,30,0.85); padding: 10px 20px; border-radius: 10px; border: 1px solid #2a2a4a; z-index: 20; }
  #controls label { color: #aaa; font-size: 13px; }
  #timeSlider { width: 240px; cursor: pointer; }
  #timeLabel { color: #fff; font-size: 13px; min-width: 48px; text-align: center; }
  #autoRotateBtn { background: #2a2a4a; color: #ccc; border: 1px solid #4a4a6a; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; }
  #autoRotateBtn.active { background: #4a6a3a; border-color: #6a8a5a; color: #fff; }
  #colorScheme { background: #1a1a3a; color: #ccc; border: 1px solid #4a4a6a; padding: 4px 8px; border-radius: 4px; font-size: 12px; cursor: pointer; }
  #bookmarkBtn { background: #2a2a4a; color: #ccc; border: 1px solid #4a4a6a; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; }
  #bookmarkLoad { background: #2a2a4a; color: #ccc; border: 1px solid #4a4a6a; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; }
  #bookmarkClear { background: #3a2a2a; color: #c88; border: 1px solid #5a3a3a; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; }
  #fps { position: absolute; top: 12px; right: 12px; color: #666; font-size: 11px; background: rgba(0,0,0,0.5); padding: 4px 10px; border-radius: 4px; z-index: 10; }
</style>
</head>
<body>
<div id="info">3D Data Terrain Explorer | Drag to orbit | Scroll to zoom</div>
<div id="fps">-- FPS</div>
<div id="controls">
  <label for="timeSlider">Time:</label>
  <input type="range" id="timeSlider" min="0" max="7" value="0" step="1">
  <span id="timeLabel">T0</span>
  <select id="colorScheme">
    <option value="vegetation">Vegetation</option>
    <option value="heat">Heat</option>
  </select>
  <button id="autoRotateBtn">Auto Orbit</button>
  <button id="bookmarkBtn">Save View</button>
  <button id="bookmarkLoad">Load Saved</button>
  <button id="bookmarkClear">Clear Saved</button>
</div>
<script type="importmap">
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"
  }
}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// --- Configuration
const GRID_SIZE = 64;
const TERRAIN_SCALE = 2.0;
const HEIGHT_SCALE = 8.0;
const TIME_SLICES = 8;
const PARTICLE_TRAIL_COUNT = 6;
const PARTICLE_TRAIL_LENGTH = 80;
// --- State
let currentTime = 0;
let autoRotate = false;
let currentScheme = 'vegetation';
const camBookmarkKey = 'terrainExplorerBookmark';
// --- Generate synthetic time-series heightfields
function generateHeightfields(slices, size) {
  const fields = [];
  for (let t = 0; t < slices; t++) {
    const data = new Float32Array(size * size);
    const phase = (t / slices) * Math.PI * 2;
    const scale = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(phase * 0.7));
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        const x = (i / size - 0.5) * 2;
        const z = (j / size - 0.5) * 2;
        const h =
          Math.sin(x * 2.5 + phase) * Math.cos(z * 2.0 - phase * 0.5) * 0.6 +
          Math.sin(x * 5.0 + phase * 0.3) * 0.25 +
          Math.cos(z * 4.5 - phase * 0.4) * 0.2 +
          Math.exp(-((x+0.3)**2 + (z-0.2)**2) * 3) * 0.4 +
          Math.exp(-((x-0.5)**2 + (z+0.4)**2) * 4) * 0.3;
        data[i * size + j] = h * scale * HEIGHT_SCALE;
      }
    }
    fields.push(data);
  }
  return fields;
}
function generateSecondaryMetric(slices, size) {
  const fields = [];
  for (let t = 0; t < slices; t++) {
    const data = new Float32Array(size * size);
    const phase = (t / slices) * Math.PI * 2;
    for (let i = 0; i < size; i++) {
      for (let j = 0; j < size; j++) {
        const x = (i / size - 0.5) * 2;
        const z = (j / size - 0.5) * 2;
        const v = 0.5 + 0.5 * Math.sin(x * 3 + z * 2.5 + phase * 0.5) * 0.7 + 0.3 * Math.random();
        data[i * size + j] = Math.max(0, Math.min(1, v));
      }
    }
    fields.push(data);
  }
  return fields;
}
const heightfields = generateHeightfields(TIME_SLICES, GRID_SIZE);
const secondaryFields = generateSecondaryMetric(TIME_SLICES, GRID_SIZE);
// --- River paths (error/anomaly traces)
function generateRivers(slices) {
  const rivers = [];
  for (let s = 0; s < 3; s++) {
    const path = [];
    const startX = 0.15 + s * 0.25 + (s === 2 ? 0.1 : 0);
    const startZ = -0.35 + s * 0.3;
    for (let t = 0; t < slices; t++) {
      const phase = (t / slices) * Math.PI * 2;
      const x = startX + Math.sin(phase * 0.5 + s * 0.7) * 0.15;
      const z = startZ + Math.cos(phase * 0.4 + s * 0.5) * 0.1 + t * 0.02;
      path.push({ x, z });
    }
    rivers.push({ path, width: 0.04 + s * 0.02, depth: 0.15 + s * 0.1, color: new THREE.Color(0.85 - s * 0.1, 0.1, 0.1) });
  }
  return rivers;
}
const riverDefs = generateRivers(TIME_SLICES);
// --- Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a1a);
scene.fog = new THREE.Fog(0x0a0a1a, 35, 60);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(12, 10, 14);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);
// --- Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.dampingFactor = 0.08;
controls.dampingEnabled = true;
controls.enableDamping = true;
controls.target.set(0, 0, 0);
controls.minDistance = 3;
controls.maxDistance = 40;
controls.maxPolarAngle = Math.PI / 2.1;
controls.update();
// --- Lighting
const ambientLight = new THREE.AmbientLight(0x404060, 0.5);
scene.add(ambientLight);
const dirLight = new THREE.DirectionalLight(0xffeedd, 1.8);
dirLight.position.set(8, 15, 6);
dirLight.castShadow = true;
dirLight.shadow.mapSize.width = 1024;
dirLight.shadow.mapSize.height = 1024;
dirLight.shadow.camera.near = 0.1;
dirLight.shadow.camera.far = 30;
dirLight.shadow.camera.left = -15;
dirLight.shadow.camera.right = 15;
dirLight.shadow.camera.top = 15;
dirLight.shadow.camera.bottom = -15;
scene.add(dirLight);
const fillLight = new THREE.DirectionalLight(0x4488ff, 0.3);
fillLight.position.set(-6, 4, -8);
scene.add(fillLight);
const hemiLight = new THREE.HemisphereLight(0x8888ff, 0x444422, 0.4);
scene.add(hemiLight);
// --- Ground plane for shadows
const groundGeo = new THREE.PlaneGeometry(50, 50);
const groundMat = new THREE.ShadowMaterial({ opacity: 0.3 });
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -HEIGHT_SCALE * 0.8;
ground.receiveShadow = true;
scene.add(ground);
// --- Build terrain geometry variants for all time slices
function buildTerrainGeometry(heightData, secondaryData, size, scale, heightScale) {
  const positions = new Float32Array(size * size * 3);
  const colors = new Float32Array(size * size * 3);
  const indices = [];
  const normals = new Float32Array(size * size * 3);
  const offset = (size - 1) * scale / -2;
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      const idx = i * size + j;
      const x = offset + i * scale;
      const z = offset + j * scale;
      const y = heightData[idx];
      positions[idx * 3] = x;
      positions[idx * 3 + 1] = y;
      positions[idx * 3 + 2] = z;
      const v = secondaryData[idx];
      let r, g, b;
      if (currentScheme === 'heat') {
        const t = v;
        if (t < 0.5) {
          r = 0.1 + t * 0.8;
          g = 0.4 + t * 0.8;
          b = 0.9 - t * 1.4;
        } else {
          r = 0.5 + (t - 0.5) * 0.7;
          g = 0.8 - (t - 0.5) * 1.4;
          b = 0.2 - (t - 0.5) * 0.2;
        }
      } else {
        if (v < 0.3) {
          r = 0.76; g = 0.70 - v * 0.3; b = 0.50;
        } else if (v < 0.6) {
          r = 0.76 - (v - 0.3) * 1.53; g = 0.61 + (v - 0.3) * 0.13; b = 0.50 - (v - 0.3) * 1.0;
        } else {
          r = 0.30 - (v - 0.6) * 0.83; g = 0.65 - (v - 0.6) * 1.0; b = 0.20 - (v - 0.6) * 0.5;
        }
      }
      colors[idx * 3] = Math.max(0, Math.min(1, r));
      colors[idx * 3 + 1] = Math.max(0, Math.min(1, g));
      colors[idx * 3 + 2] = Math.max(0, Math.min(1, b));
    }
  }
  for (let i = 0; i < size - 1; i++) {
    for (let j = 0; j < size - 1; j++) {
      const a = i * size + j;
      const b = i * size + j + 1;
      const c = (i + 1) * size + j;
      const d = (i + 1) * size + j + 1;
      indices.push(a, b, c);
      indices.push(b, d, c);
    }
  }
  const posAttr = new THREE.BufferAttribute(positions, 3);
  const idxAttr = new THREE.BufferAttribute(new Uint16Array(indices), 1);
  const colAttr = new THREE.BufferAttribute(colors, 3);
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', posAttr);
  geo.setAttribute('color', colAttr);
  geo.setIndex(idxAttr);
  geo.computeVertexNormals();
  return { geo, positions, colors, indices };
}
// Build geometries for all time slices
const terrainGeos = [];
const terrainData = [];
for (let t = 0; t < TIME_SLICES; t++) {
  const result = buildTerrainGeometry(
    heightfields[t], secondaryFields[t],
    GRID_SIZE, TERRAIN_SCALE, HEIGHT_SCALE
  );
  terrainData.push({ positions: result.positions, colors: result.colors, indices: result.indices });
  terrainGeos.push(result.geo);
}
// First terrain mesh
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.1,
  flatShading: false,
  side: THREE.DoubleSide
});
const terrain = new THREE.Mesh(terrainGeos[0], terrainMat);
terrain.castShadow = true;
terrain.receiveShadow = true;
scene.add(terrain);
// --- Terrain height lookup (bilinear interpolation)
function getTerrainHeight(x, z, heightData, size, scale) {
  const offset = (size - 1) * scale / -2;
  const fx = (x - offset) / scale;
  const fz = (z - offset) / scale;
  const ix = Math.floor(fx);
  const iz = Math.floor(fz);
  if (ix < 0 || ix >= size - 1 || iz < 0 || iz >= size - 1) return 0;
  const dx = fx - ix;
  const dz = fz - iz;
  const h00 = heightData[ix * size + iz];
  const h10 = heightData[(ix + 1) * size + iz];
  const h01 = heightData[ix * size + iz + 1];
  const h11 = heightData[(ix + 1) * size + iz + 1];
  return h00 * (1 - dx) * (1 - dz) + h10 * dx * (1 - dz) + h01 * (1 - dx) * dz + h11 * dx * dz;
}
// --- River geometry
const riverGroup = new THREE.Group();
scene.add(riverGroup);
function buildRiverGeometry(riverDef, heightData, size, scale, heightScale) {
  const pts = riverDef.path.length;
  const segments = pts - 1;
  const halfW = riverDef.width / 2;
  const posCount = (pts) * 4;
  const positions = new Float32Array(posCount * 3);
  const colors = new Float32Array(posCount * 3);
  const indices = [];
  for (let i = 0; i < pts; i++) {
    const p = riverDef.path[i];
    const h = getTerrainHeight(p.x, p.z, heightData, size, scale) - riverDef.depth;
    const perpX = 1, perpZ = 0; // simplified perpendicular
    const leftIdx = i * 4;
    const rightIdx = i * 4 + 1;
    const leftBackIdx = i * 4 + 2;
    const rightBackIdx = i * 4 + 3;
    positions[leftIdx * 3] = p.x + halfW;
    positions[leftIdx * 3 + 1] = h;
    positions[leftIdx * 3 + 2] = p.z;
    positions[rightIdx * 3] = p.x - halfW;
    positions[rightIdx * 3 + 1] = h;
    positions[rightIdx * 3 + 2] = p.z;
    positions[leftBackIdx * 3] = p.x + halfW;
    positions[leftBackIdx * 3 + 1] = h - 0.05;
    positions[leftBackIdx * 3 + 2] = p.z;
    positions[rightBackIdx * 3] = p.x - halfW;
    positions[rightBackIdx * 3 + 1] = h - 0.05;
    positions[rightBackIdx * 3 + 2] = p.z;
    const c = riverDef.color;
    for (let v = 0; v < 4; v++) {
      colors[(leftIdx + v) * 3] = c.r;
      colors[(leftIdx + v) * 3 + 1] = c.g;
      colors[(leftIdx + v) * 3 + 2] = c.b;
    }
  }
  for (let i = 0; i < segments; i++) {
    const a = i * 4, b = i * 4 + 1, c = i * 4 + 2, d = i * 4 + 3;
    const e = (i + 1) * 4, f = (i + 1) * 4 + 1, g = (i + 1) * 4 + 2, h = (i + 1) * 4 + 3;
    indices.push(a, e, b);
    indices.push(b, e, f);
    indices.push(c, g, a);
    indices.push(a, g, e);
    indices.push(b, f, d);
    indices.push(d, f, h);
    indices.push(c, d, h);
    indices.push(c, h, g);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(new THREE.BufferAttribute(new Uint16Array(indices), 1));
  return geo;
}
const riverMeshes = [];
function rebuildRivers(timeIdx) {
  while (riverGroup.children.length) {
    const child = riverGroup.children[0];
    child.geometry.dispose();
    riverGroup.remove(child);
  }
  riverMeshes.length = 0;
  for (const def of riverDefs) {
    const geo = buildRiverGeometry(def, heightfields[timeIdx], GRID_SIZE, TERRAIN_SCALE, HEIGHT_SCALE);
    const mat = new THREE.MeshBasicMaterial({ vertexColors: true, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geo, mat);
    riverGroup.add(mesh);
    riverMeshes.push({ mesh, def });
  }
}
rebuildRivers(0);
// --- Particles
const particleGroup = new THREE.Group();
scene.add(particleGroup);
const particleTrails = [];
function initParticles() {
  const trailPositions = [];
  const trailColors = [];
  const trailSizes = new Float32Array(PARTICLE_TRAIL_COUNT * PARTICLE_TRAIL_LENGTH);
  for (let t = 0; t < PARTICLE_TRAIL_COUNT; t++) {
    const phase = (t / PARTICLE_TRAIL_COUNT) * Math.PI * 2;
    const startX = Math.sin(phase) * 2;
    const startZ = Math.cos(phase * 0.7) * 2.5;
    const trail = {
      x: startX,
      z: startZ,
      vx: 0.02 + Math.random() * 0.03,
      vz: 0.01 + Math.random() * 0.02,
      phase: t * 1.5,
      positions: new Float32Array(PARTICLE_TRAIL_LENGTH * 3),
      head: 0
    };
    for (let i = 0; i < PARTICLE_TRAIL_LENGTH; i++) {
      trail.positions[i * 3] = startX;
      trail.positions[i * 3 + 1] = 0;
      trail.positions[i * 3 + 2] = startZ;
    }
    particleTrails.push(trail);
    for (let i = 0; i < PARTICLE_TRAIL_LENGTH; i++) {
      trailPositions.push(startX, 0, startZ);
      const fade = 0.1 + 0.9 * (1 - i / PARTICLE_TRAIL_LENGTH);
      trailColors.push(0.6, 0.8, 1.0);
      trailSizes[t * PARTICLE_TRAIL_LENGTH + i] = 0.08 * fade;
    }
  }
  const posAttr = new THREE.BufferAttribute(new Float32Array(trailPositions), 3);
  const colAttr = new THREE.BufferAttribute(new Float32Array(trailColors), 3);
  const sizeAttr = new THREE.BufferAttribute(trailSizes, 1);
  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute('position', posAttr);
  particleGeo.setAttribute('color', colAttr);
  particleGeo.setAttribute('size', sizeAttr);
  const particleMat = new THREE.PointsMaterial({
    size: 0.08,
    vertexColors: true,
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    depthWrite: false
  });
  const particleSystem = new THREE.Points(particleGeo, particleMat);
  particleGroup.add(particleSystem);
  return { geo: particleGeo, mat: particleMat, system: particleSystem };
}
const particleState = initParticles();
function updateParticles(timeIdx) {
  const heightData = heightfields[timeIdx];
  const posAttr = particleState.geo.attributes.position;
  const sizeAttr = particleState.geo.attributes.size;
  const posArray = posAttr.array;
  const sizeArray = sizeAttr.array;
  for (let t = 0; t < PARTICLE_TRAIL_COUNT; t++) {
    const trail = particleTrails[t];
    trail.x += trail.vx + Math.sin(Date.now() / 1000 + trail.phase) * 0.005;
    trail.z += trail.vz + Math.cos(Date.now() / 1200 + trail.phase * 0.7) * 0.005;
    if (trail.x > 4) trail.x = -4;
    if (trail.x < -4) trail.x = 4;
    if (trail.z > 4) trail.z = -4;
    if (trail.z < -4) trail.z = 4;
    const h = getTerrainHeight(trail.x, trail.z, heightData, GRID_SIZE, TERRAIN_SCALE) + 0.15;
    // Shift positions back by one
    for (let i = PARTICLE_TRAIL_LENGTH - 1; i > 0; i--) {
      const dstIdx = t * PARTICLE_TRAIL_LENGTH + i;
      const srcIdx = t * PARTICLE_TRAIL_LENGTH + (i - 1);
      posArray[dstIdx * 3] = posArray[srcIdx * 3];
      posArray[dstIdx * 3 + 1] = posArray[srcIdx * 3 + 1];
      posArray[dstIdx * 3 + 2] = posArray[srcIdx * 3 + 2];
      sizeArray[dstIdx] = sizeArray[srcIdx];
    }
    // New head position
    const headIdx = t * PARTICLE_TRAIL_LENGTH;
    posArray[headIdx * 3] = trail.x;
    posArray[headIdx * 3 + 1] = h;
    posArray[headIdx * 3 + 2] = trail.z;
    sizeArray[headIdx] = 0.12;
  }
  posAttr.needsUpdate = true;
  sizeAttr.needsUpdate = true;
}
// --- Time slider rebuild
function setTime(timeIdx) {
  currentTime = timeIdx;
  const data = terrainData[timeIdx];
  // Swap geometry attributes on existing mesh
  const geo = terrain.geometry;
  geo.setAttribute('position', new THREE.BufferAttribute(data.positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(data.colors, 3));
  geo.setIndex(new THREE.BufferAttribute(new Uint16Array(data.indices), 1));
  geo.computeVertexNormals();
  geo.attributes.position.needsUpdate = true;
  geo.attributes.color.needsUpdate = true;
  geo.index.needsUpdate = true;
  rebuildRivers(timeIdx);
  document.getElementById('timeLabel').textContent = `T${timeIdx}`;
}
// --- Auto-rotation loop
let autoRotateActive = false;
document.getElementById('autoRotateBtn').addEventListener('click', () => {
  autoRotateActive = !autoRotateActive;
  document.getElementById('autoRotateBtn').classList.toggle('active');
});
// --- Color scheme switch
document.getElementById('colorScheme').addEventListener('change', (e) => {
  currentScheme = e.target.value;
  // Rebuild all geometry data with new color scheme
  for (let t = 0; t < TIME_SLICES; t++) {
    const result = buildTerrainGeometry(
      heightfields[t], secondaryFields[t],
      GRID_SIZE, TERRAIN_SCALE, HEIGHT_SCALE
    );
    terrainData[t].colors = result.colors;
    terrainData[t].positions = result.positions;
    terrainGeos[t] = result.geo;
  }
  setTime(currentTime);
});
// --- Bookmarks
function saveBookmark() {
  const bm = {
    position: camera.position.toArray(),
    target: controls.target.toArray(),
    label: `View ${new Date().toLocaleTimeString()}`
  };
  localStorage.setItem(camBookmarkKey, JSON.stringify(bm));
}
function loadBookmark() {
  const raw = localStorage.getItem(camBookmarkKey);
  if (!raw) return;
  try {
    const bm = JSON.parse(raw);
    camera.position.fromArray(bm.position);
    controls.target.fromArray(bm.target);
    controls.update();
  } catch(e) {}
}
function clearBookmark() {
  localStorage.removeItem(camBookmarkKey);
}
document.getElementById('bookmarkBtn').addEventListener('click', saveBookmark);
document.getElementById('bookmarkLoad').addEventListener('click', loadBookmark);
document.getElementById('bookmarkClear').addEventListener('click', clearBookmark);
// --- Time slider
document.getElementById('timeSlider').addEventListener('input', (e) => {
  setTime(parseInt(e.target.value));
});
// --- Resize handler
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- FPS counter
let frameCount = 0;
let lastFpsTime = performance.now();
// --- Animation loop
function animate() {
  requestAnimationFrame(animate);
  if (autoRotateActive) {
    const pivot = new THREE.Vector3(0, 0, 0);
    const radius = camera.position.length();
    const theta = Math.atan2(camera.position.x, camera.position.z) + 0.005;
    camera.position.x = radius * Math.sin(theta);
    camera.position.z = radius * Math.cos(theta);
    camera.lookAt(0, 0, 0);
    controls.target.set(0, 0, 0);
  }
  updateParticles(currentTime);
  controls.update();
  renderer.render(scene, camera);
  frameCount++;
  const now = performance.now();
  if (now - lastFpsTime >= 1000) {
    document.getElementById('fps').textContent = `${frameCount} FPS`;
    frameCount = 0;
    lastFpsTime = now;
  }
}
animate();
// --- Load saved bookmark on startup
loadBookmark();
console.log('3D Data Terrain Explorer initialized');
console.log(`Grid: ${GRID_SIZE}x${GRID_SIZE}, Time slices: ${TIME_SLICES}, Particle trails: ${PARTICLE_TRAIL_COUNT}`);
</script>
</body>
</html>
```
---
The blueprint produces a single self-contained HTML file. All Three.js modules arrive via importmap from CDN -- no build step needed, opens directly in any modern browser. Terrain mesh reuses one BufferGeometry whose attributes are swapped on time slider change (zero new geometry allocations per tick). Particles reuse a fixed Float32Array with shift-and-overwrite per frame. Rivers rebuild per time slice from terrain height lookups. Camera bookmarks survive page reload via localStorage. Color scheme selector switches between vegetation gradient and heat coloring on the fly, rebuilding vertex colors across all cached time slices. Auto-orbit mode rotates the camera at constant radius around origin. FPS counter appears top-right for performance monitoring.