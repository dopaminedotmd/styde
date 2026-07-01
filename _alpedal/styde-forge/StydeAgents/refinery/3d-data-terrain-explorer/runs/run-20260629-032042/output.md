<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { overflow: hidden; background: #0d0d1f; font-family: 'Segoe UI', system-ui, sans-serif; }
  #canvas-container { position: fixed; inset: 0; }
  canvas { display: block; }
  #hud {
    position: fixed; top: 16px; left: 16px;
    color: #c8d6e5; font-size: 13px;
    background: rgba(10, 10, 30, 0.75);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 16px 20px;
    min-width: 220px;
    pointer-events: none;
  }
  #hud .title { font-size: 15px; font-weight: 600; letter-spacing: 0.5px; margin-bottom: 8px; color: #ffffff; }
  #hud .stat { display: flex; justify-content: space-between; margin: 3px 0; opacity: 0.8; }
  #hud .stat .val { font-weight: 600; color: #feca57; }
  #controls-panel {
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: rgba(10, 10, 30, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 14px 22px;
    display: flex; gap: 18px; align-items: center;
  }
  #controls-panel label { color: #a0b4cc; font-size: 12px; letter-spacing: 0.3px; }
  #time-slider { width: 200px; accent-color: #feca57; cursor: pointer; }
  #time-label { color: #feca57; font-weight: 700; font-size: 14px; min-width: 55px; text-align: center; }
  .btn {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    color: #c8d6e5;
    padding: 6px 14px;
    border-radius: 7px;
    cursor: pointer;
    font-size: 12px;
    transition: all 0.2s;
  }
  .btn:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.3); }
  .btn.active { background: rgba(254, 202, 87, 0.15); border-color: #feca57; color: #feca57; }
  #bookmark-bar {
    position: fixed; top: 16px; right: 16px;
    display: flex; flex-direction: column; gap: 5px;
  }
  #bookmark-bar .bm-btn {
    background: rgba(10,10,30,0.7);
    border: 1px solid rgba(255,255,255,0.1);
    color: #a0b4cc;
    padding: 5px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 11px;
    transition: all 0.2s;
  }
  #bookmark-bar .bm-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }
  #legend {
    position: fixed; bottom: 100px; right: 20px;
    background: rgba(10,10,30,0.7);
    border-radius: 8px; padding: 10px 14px;
    color: #8899aa; font-size: 11px;
    border: 1px solid rgba(255,255,255,0.06);
  }
  #legend .gradient-bar {
    width: 180px; height: 10px;
    border-radius: 5px;
    margin: 4px 0;
  }
  #legend .row { display: flex; justify-content: space-between; }
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="hud">
  <div class="title">Terrain Explorer</div>
  <div class="stat"><span>Elevation</span><span class="val" id="hud-height">--</span></div>
  <div class="stat"><span>Density</span><span class="val" id="hud-density">--</span></div>
  <div class="stat"><span>Error rate</span><span class="val" id="hud-error">--</span></div>
  <div class="stat"><span>Particles</span><span class="val" id="hud-particles">--</span></div>
  <div class="stat"><span>FPS</span><span class="val" id="hud-fps">--</span></div>
</div>
<div id="controls-panel">
  <button class="btn" id="btn-auto-rotate" title="Auto-rotate camera">Auto Rotate</button>
  <label for="time-slider">Time</label>
  <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
  <span id="time-label">12:00</span>
  <button class="btn" id="btn-wireframe" title="Toggle wireframe">Wire</button>
  <button class="btn" id="btn-top-down" title="Top-down view">Top</button>
  <button class="btn" id="btn-rivers" title="Toggle error rivers">Rivers</button>
</div>
<div id="bookmark-bar">
  <button class="bm-btn" data-preset="overview">Overview</button>
  <button class="bm-btn" data-preset="north-ridge">North Ridge</button>
  <button class="bm-btn" data-preset="valley">River Valley</button>
  <button class="bm-btn" data-preset="peak">Revenue Peak</button>
</div>
<div id="legend">
  <div class="row"><span>Density low</span><span>high</span></div>
  <div class="gradient-bar" style="background: linear-gradient(90deg, #1a5c1a, #4caf50, #ffd54f, #ff8c00);"></div>
  <div class="row" style="margin-top:6px"><span>Error river</span><span style="color:#e74c3c">red channel</span></div>
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
/*
 * CONFIG — all tunable parameters in one discoverable object.
 * Every numeric constant >2 is named with an explanatory comment.
 */
const CONFIG = {
  /* --- Terrain geometry --- */
  TERRAIN_SIZE: 200,            /* grid vertices per side (200x200 = 40k vertices) */
  TERRAIN_SCALE: 0.08,          /* world-space spacing between adjacent vertices */
  HEIGHT_AMPLITUDE: 8,          /* max vertical displacement in world units */
  TERRAIN_SEGMENTS: 199,        /* one less than TERRAIN_SIZE for geometry faces */
  /* --- Time dimension --- */
  TIME_STEPS: 24,               /* number of hourly snapshots in the dataset */
  TIME_DEFAULT_INDEX: 12,       /* initial slider position (noon) */
  /* --- Particle flow system --- */
  PARTICLE_COUNT: 500,          /* active particles in the flow trail system */
  PARTICLE_SPEED_FACTOR: 0.015, /* base speed multiplier for particle advance per frame */
  PARTICLE_LIFETIME_FRAMES: 90, /* frames before a particle respawns at origin */
  PARTICLE_TRAIL_LENGTH: 40,     /* points in each particle's trailing ribbon */
  /* --- River (error anomaly) geometry --- */
  RIVER_WIDTH: 0.35,            /* half-width of the river ribbon in world units */
  RIVER_COLOR: [0.92, 0.15, 0.15], /* error river base color (deep red) */
  RIVER_OPACITY: 0.75,          /* material opacity for river mesh */
  /* --- Vertex coloring (vegetation gradient from density) --- */
  COLOR_LOW: [0.12, 0.45, 0.12],  /* low density: dark forest green */
  COLOR_HIGH: [1.0, 0.78, 0.08],  /* high density: golden amber */
  COLOR_ERROR_TINT: [0.95, 0.2, 0.2], /* error zone tint mixed into vertex color */
  /* --- OrbitControls --- */
  AUTO_ROTATE_SPEED: 0.25,      /* radians per second when auto-rotate is active */
  DAMPING_FACTOR: 0.08,         /* inertia damping (lower = smoother, slower stop) */
  MIN_DISTANCE: 4,              /* closest zoom distance */
  MAX_DISTANCE: 40,             /* farthest zoom distance */
  MAX_POLAR_ANGLE: Math.PI * 0.48, /* prevent camera going underground */
  /* --- Scene --- */
  BACKGROUND_COLOR: [0.04, 0.04, 0.1], /* deep space blue-black */
  FOG_NEAR: 12,                 /* distance where fog begins */
  FOG_FAR: 45,                  /* distance where fog is fully opaque */
  AMBIENT_LIGHT_INTENSITY: 0.4, /* soft fill light level */
  DIRECTIONAL_LIGHT_INTENSITY: 1.2, /* key light simulating sun */
  GRID_OPACITY: 0.12,           /* reference plane grid opacity */
};
/* --- Camera bookmarks: named presets storing position + target --- */
const BOOKMARKS = {
  overview: {
    position: [22, 16, 22],
    target: [0, 3, 0]
  },
  'north-ridge': {
    position: [0, 9, 18],
    target: [0, 3, -3]
  },
  'river-valley': {
    position: [6, 5, 8],
    target: [-2, 2, -1]
  },
  'revenue-peak': {
    position: [3, 11, 3],
    target: [3, 6, 3]
  }
};
/* ---- Synthetic Time-Series Dataset ---- */
/*
 * GenerateMultiOctaveNoise: layered Perlin-style noise across 24 time steps.
 * Each octave adds finer detail at half the amplitude, creating natural terrain evolution.
 */
function generateMultiOctaveNoise(size, timeSteps) {
  const OCTAVES = 4;            /* detail layers from coarse to fine */
  const BASE_FREQ = 4.5;        /* lowest frequency: broad landscape shape */
  const PERSISTENCE = 0.55;     /* amplitude falloff per octave */
  const data = new Array(timeSteps);
  for (let t = 0; t < timeSteps; t++) {
    const slice = new Float32Array(size * size);
    const timeWarp = t / timeSteps; /* [0..1] time progress to shift noise phase */
    for (let iy = 0; iy < size; iy++) {
      for (let ix = 0; ix < size; ix++) {
        const nx = ix / size;
        const ny = iy / size;
        let amplitude = 1.0;
        let frequency = BASE_FREQ;
        let value = 0;
        let maxVal = 0;
        for (let o = 0; o < OCTAVES; o++) {
          /* sin-based pseudo-noise with time-dependent phase shift */
          const phaseShift = timeWarp * Math.PI * 1.5 * (o + 1) * 0.35;
          value += amplitude * (
            Math.sin(frequency * nx * Math.PI * 1.7 + phaseShift) *
            Math.cos(frequency * ny * Math.PI * 1.3 + phaseShift * 0.7) +
            Math.sin(frequency * (nx + ny) * 0.8 + phaseShift * 1.3) * 0.5
          );
          maxVal += amplitude;
          amplitude *= PERSISTENCE;
          frequency *= 2.15;
        }
        slice[iy * size + ix] = value / maxVal; /* normalize to [-1, 1] */
      }
    }
    data[t] = slice;
  }
  return data;
}
/*
 * GenerateDensityField: synthetic user-density data per vertex per time step.
 * Peaks around terrain high points with random hotspots.
 */
function generateDensityField(size, timeSteps, heightData) {
  const density = new Array(timeSteps);
  for (let t = 0; t < timeSteps; t++) {
    const slice = new Float32Array(size * size);
    const heights = heightData[t];
    for (let i = 0; i < size * size; i++) {
      /* density correlates with elevation: higher terrain = more users */
      slice[i] = Math.max(0, Math.min(1, (heights[i] + 1) * 0.45 + Math.random() * 0.15));
    }
    density[t] = slice;
  }
  return density;
}
/*
 * GenerateErrorField: locate error anomaly zones (rivers).
 * Errors cluster in low-elevation valleys with time-dependent migration.
 */
function generateErrorField(size, timeSteps, heightData) {
  const errors = new Array(timeSteps);
  for (let t = 0; t < timeSteps; t++) {
    const slice = new Float32Array(size * size);
    const heights = heightData[t];
    for (let i = 0; i < size * size; i++) {
      /* inverse elevation: valleys accumulate errors */
      const valleyFactor = 1.0 - Math.max(0, (heights[i] + 1) * 0.5);
      slice[i] = Math.max(0, Math.min(1, valleyFactor * 0.7 + Math.random() * 0.08));
    }
    errors[t] = slice;
  }
  return errors;
}
/* ---- Generate full dataset ---- */
const SIZE = CONFIG.TERRAIN_SIZE;
const STEPS = CONFIG.TIME_STEPS;
const heightData = generateMultiOctaveNoise(SIZE, STEPS);
const densityData = generateDensityField(SIZE, STEPS, heightData);
const errorData = generateErrorField(SIZE, STEPS, heightData);
/* ---- Three.js Setup ---- */
const container = document.getElementById('canvas-container');
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
container.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(...CONFIG.BACKGROUND_COLOR);
scene.fog = new THREE.Fog(...CONFIG.BACKGROUND_COLOR, CONFIG.FOG_NEAR, CONFIG.FOG_FAR);
const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.5, 80);
camera.position.set(...BOOKMARKS.overview.position);
camera.lookAt(...BOOKMARKS.overview.target);
/* OrbitControls with smooth damping */
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(...BOOKMARKS.overview.target);
controls.enableDamping = true;
controls.dampingFactor = CONFIG.DAMPING_FACTOR;
controls.autoRotate = false;
controls.autoRotateSpeed = CONFIG.AUTO_ROTATE_SPEED;
controls.minDistance = CONFIG.MIN_DISTANCE;
controls.maxDistance = CONFIG.MAX_DISTANCE;
controls.maxPolarAngle = CONFIG.MAX_POLAR_ANGLE;
controls.update();
/* ---- Lighting ---- */
const ambientLight = new THREE.AmbientLight(0x556688, CONFIG.AMBIENT_LIGHT_INTENSITY);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffffff, CONFIG.DIRECTIONAL_LIGHT_INTENSITY);
sunLight.position.set(15, 22, 8);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 1024;
sunLight.shadow.mapSize.height = 1024;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 60;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0003;
scene.add(sunLight);
const rimLight = new THREE.DirectionalLight(0x8899cc, 0.5);
rimLight.position.set(-8, 5, -5);
scene.add(rimLight);
/* ---- Reference grid plane ---- */
const gridHelper = new THREE.PolarGridHelper(12, 32, 24, 128, 0x334455, 0x223344);
gridHelper.position.y = -CONFIG.HEIGHT_AMPLITUDE - 0.1;
scene.add(gridHelper);
/* ---- Terrain Mesh (BufferGeometry heightfield) ---- */
/*
 * BuildTerrainGeometry: creates BufferGeometry from height + density data at given time index.
 * Positions: xz grid with y = heightData[t][i] * HEIGHT_AMPLITUDE.
 * Colors: vertex colors interpolated from COLOR_LOW (low density) to COLOR_HIGH (high density),
 *   with red tint blended in where errorData[t][i] exceeds 0.35.
 */
function buildTerrainGeometry(timeIndex) {
  const geo = new THREE.BufferGeometry();
  const count = SIZE * SIZE;
  const positions = new Float32Array(count * 3);
  const colors = new Float32Array(count * 3);
  const heights = heightData[timeIndex];
  const densities = densityData[timeIndex];
  const errors = errorData[timeIndex];
  const amp = CONFIG.HEIGHT_AMPLITUDE;
  const scale = CONFIG.TERRAIN_SCALE;
  const half = (SIZE - 1) * scale * 0.5;
  const cl = CONFIG.COLOR_LOW;
  const ch = CONFIG.COLOR_HIGH;
  const ct = CONFIG.COLOR_ERROR_TINT;
  const ERROR_THRESHOLD = 0.35; /* density value above which error tint appears */
  for (let iy = 0; iy < SIZE; iy++) {
    for (let ix = 0; ix < SIZE; ix++) {
      const idx = iy * SIZE + ix;
      const i3 = idx * 3;
      positions[i3]     = ix * scale - half;       /* x */
      positions[i3 + 1] = heights[idx] * amp;       /* y (elevation) */
      positions[i3 + 2] = iy * scale - half;       /* z */
      const d = densities[idx];
      /* blend low-to-high color based on density */
      let r = cl[0] + (ch[0] - cl[0]) * d;
      let g = cl[1] + (ch[1] - cl[1]) * d;
      let b = cl[2] + (ch[2] - cl[2]) * d;
      /* overlay error red tint in high-error zones */
      const err = errors[idx];
      if (err > ERROR_THRESHOLD) {
        const tintFactor = (err - ERROR_THRESHOLD) / (1.0 - ERROR_THRESHOLD);
        r = r * (1 - tintFactor) + ct[0] * tintFactor;
        g = g * (1 - tintFactor * 0.7) + ct[1] * tintFactor * 0.3;
        b = b * (1 - tintFactor * 0.7) + ct[2] * tintFactor * 0.3;
      }
      colors[i3]     = r;
      colors[i3 + 1] = g;
      colors[i3 + 2] = b;
    }
  }
  /* Build index array for triangle strips */
  const indices = [];
  for (let iy = 0; iy < SIZE - 1; iy++) {
    for (let ix = 0; ix < SIZE - 1; ix++) {
      const a = iy * SIZE + ix;
      const b = a + 1;
      const c = a + SIZE;
      const d = c + 1;
      indices.push(a, b, d);
      indices.push(a, d, c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
let currentTimeIndex = CONFIG.TIME_DEFAULT_INDEX;
let terrainGeo = buildTerrainGeometry(currentTimeIndex);
const terrainMaterial = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.65,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMaterial);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
/* ---- River Geometry (error anomaly paths) ---- */
/*
 * BuildRiverGeometry: traces high-error paths across the terrain as extruded ribbon.
 * Uses the error field above ERROR_RIVER_THRESH to sample waypoints, then constructs
 * a tube-like ribbon that follows those waypoints at terrain height.
 */
const ERROR_RIVER_THRESH = 0.6; /* minimum error value to be considered a river waypoint */
let riverMesh = null;
function buildRiverGeometry(timeIndex) {
  const heights = heightData[timeIndex];
  const errors = errorData[timeIndex];
  const amp = CONFIG.HEIGHT_AMPLITUDE;
  const scale = CONFIG.TERRAIN_SCALE;
  const half = (SIZE - 1) * scale * 0.5;
  /* Sample waypoints: scan grid for error hot spots */
  const waypoints = [];
  const STEP = 4; /* sample every Nth vertex to keep waypoint count manageable */
  for (let iy = 0; iy < SIZE; iy += STEP) {
    for (let ix = 0; ix < SIZE; ix += STEP) {
      const idx = iy * SIZE + ix;
      if (errors[idx] > ERROR_RIVER_THRESH) {
        waypoints.push({
          x: ix * scale - half,
          y: heights[idx] * amp + 0.15, /* offset slightly above terrain to avoid z-fighting */
          z: iy * scale - half,
          err: errors[idx]
        });
      }
    }
  }
  /* Cluster waypoints into continuous river segments by proximity */
  if (waypoints.length < 3) return new THREE.Group();
  /* k-nearest-neighbor clustering: group consecutive close points into river strands */
  const CLUSTER_DIST = 2.5; /* max world-unit distance between consecutive river waypoints */
  const strands = [];
  const visited = new Set();
  for (let i = 0; i < waypoints.length; i++) {
    if (visited.has(i)) continue;
    const strand = [waypoints[i]];
    visited.add(i);
    let grown = true;
    while (grown) {
      grown = false;
      const last = strand[strand.length - 1];
      let bestJ = -1;
      let bestDist = Infinity;
      for (let j = 0; j < waypoints.length; j++) {
        if (visited.has(j)) continue;
        const dx = waypoints[j].x - last.x;
        const dz = waypoints[j].z - last.z;
        const dist = Math.sqrt(dx * dx + dz * dz);
        if (dist < CLUSTER_DIST && dist < bestDist) {
          bestDist = dist;
          bestJ = j;
        }
      }
      if (bestJ >= 0) {
        strand.push(waypoints[bestJ]);
        visited.add(bestJ);
        grown = true;
      }
    }
    if (strand.length >= 3) strands.push(strand);
  }
  const group = new THREE.Group();
  for (const strand of strands) {
    if (strand.length < 3) continue;
    /* Build Catmull-Rom curve through waypoints for smooth river path */
    const points = strand.map(w => new THREE.Vector3(w.x, w.y, w.z));
    const curve = new THREE.CatmullRomCurve3(points, false, 'catmullrom', 0.5);
    /* Create ribbon geometry along the curve */
    const curvePoints = curve.getPoints(strand.length * 6);
    const ribbonGeo = new THREE.BufferGeometry();
    const rVerts = [];
    const rIndices = [];
    const rColors = [];
    const hw = CONFIG.RIVER_WIDTH;
    for (let i = 0; i < curvePoints.length; i++) {
      const tangent = i < curvePoints.length - 1
        ? new THREE.Vector3().subVectors(curvePoints[i + 1], curvePoints[i]).normalize()
        : new THREE.Vector3().subVectors(curvePoints[i], curvePoints[i - 1]).normalize();
      /* perpendicular vector in xz-plane for ribbon width */
      const perp = new THREE.Vector3(-tangent.z, 0, tangent.x).normalize();
      const left = curvePoints[i].clone().addScaledVector(perp, -hw);
      const right = curvePoints[i].clone().addScaledVector(perp, hw);
      /* drop ribbon edges slightly below terrain surface */
      left.y -= 0.05;
      right.y -= 0.05;
      rVerts.push(left.x, left.y, left.z);
      rVerts.push(right.x, right.y, right.z);
      /* color: deep red, pulsing slightly with error intensity */
      const pulse = 0.7 + 0.3 * strand[Math.min(Math.floor(i / 6), strand.length - 1)].err;
      rColors.push(CONFIG.RIVER_COLOR[0] * pulse, CONFIG.RIVER_COLOR[1], CONFIG.RIVER_COLOR[2]);
      rColors.push(CONFIG.RIVER_COLOR[0] * pulse, CONFIG.RIVER_COLOR[1], CONFIG.RIVER_COLOR[2]);
      if (i < curvePoints.length - 1) {
        const base = i * 2;
        rIndices.push(base, base + 1, base + 2);
        rIndices.push(base + 1, base + 3, base + 2);
      }
    }
    ribbonGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(rVerts), 3));
    ribbonGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(rColors), 3));
    ribbonGeo.setIndex(rIndices);
    ribbonGeo.computeVertexNormals();
    const ribbonMat = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.3,
      metalness: 0.2,
      transparent: true,
      opacity: CONFIG.RIVER_OPACITY,
      side: THREE.DoubleSide,
      depthWrite: false,
    });
    const ribbonMesh = new THREE.Mesh(ribbonGeo, ribbonMat);
    ribbonMesh.renderOrder = 1;
    group.add(ribbonMesh);
  }
  return group;
}
riverMesh = buildRiverGeometry(currentTimeIndex);
scene.add(riverMesh);
/* ---- Particle Flow System ---- */
/*
 * ParticleFlowSystem: manages a pool of particles representing API call / data flow trails.
 * Each particle advances across the terrain surface, sampling height at its xz position.
 * Particles respawn at random positions when they hit terrain edges or exceed lifetime.
 */
class ParticleFlowSystem {
  constructor(count) {
    this.count = count;
    this.active = true;
    /* Pre-allocate position and velocity arrays for CPU-side reuse */
    this.positions = new Float32Array(count * 3);    /* world xyz */
    this.velocities = new Float32Array(count * 2);    /* vx, vz in xz-plane */
    this.ages = new Float32Array(count);              /* frames since spawn */
    this.colors = new Float32Array(count * 3);        /* per-particle rgb */
    this.PARTICLE_SIZE = 0.08; /* world-unit radius for each particle dot */
    this.initParticles();
    this.buildGeometry();
  }
  /*
   * initParticles: scatter particles randomly across the terrain footprint.
   */
  initParticles() {
    const half = (SIZE - 1) * CONFIG.TERRAIN_SCALE * 0.5;
    for (let i = 0; i < this.count; i++) {
      this.positions[i * 3]     = (Math.random() - 0.5) * half * 2;
      this.positions[i * 3 + 1] = 0;
      this.positions[i * 3 + 2] = (Math.random() - 0.5) * half * 2;
      /* random flow direction, biased along x */
      const angle = (Math.random() - 0.5) * Math.PI * 0.7;
      const speed = 0.03 + Math.random() * 0.07;
      this.velocities[i * 2]     = Math.cos(angle) * speed;
      this.velocities[i * 2 + 1] = Math.sin(angle) * speed;
      this.ages[i] = Math.floor(Math.random() * CONFIG.PARTICLE_LIFETIME_FRAMES);
      /* color: golden flow with slight hue variation */
      const hue = 0.12 + Math.random() * 0.08; /* gold/orange range */
      const rgb = new THREE.Color().setHSL(hue, 0.9, 0.55 + Math.random() * 0.25);
      this.colors[i * 3]     = rgb.r;
      this.colors[i * 3 + 1] = rgb.g;
      this.colors[i * 3 + 2] = rgb.b;
    }
  }
  buildGeometry() {
    this.geometry = new THREE.BufferGeometry();
    this.geometry.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    this.geometry.setAttribute('color', new THREE.BufferAttribute(this.colors, 3));
    const mat = new THREE.PointsMaterial({
      size: this.PARTICLE_SIZE,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.7,
    });
    this.points = new THREE.Points(this.geometry, mat);
    this.points.renderOrder = 2;
  }
  /*
   * sampleHeight: bilinear lookup of terrain height at world-space xz coordinate.
   * Returns 0 if the coordinate falls outside the terrain bounds.
   */
  sampleHeight(wx, wz, timeIndex) {
    const scale = CONFIG.TERRAIN_SCALE;
    const half = (SIZE - 1) * scale * 0.5;
    const gx = (wx + half) / scale;
    const gz = (wz + half) / scale;
    if (gx < 0 || gx >= SIZE - 1 || gz < 0 || gz >= SIZE - 1) return null;
    const ix0 = Math.floor(gx);
    const iz0 = Math.floor(gz);
    const ix1 = Math.min(ix0 + 1, SIZE - 1);
    const iz1 = Math.min(iz0 + 1, SIZE - 1);
    const fx = gx - ix0;
    const fz = gz - iz0;
    const h = heightData[timeIndex];
    const h00 = h[iz0 * SIZE + ix0];
    const h10 = h[iz0 * SIZE + ix1];
    const h01 = h[iz1 * SIZE + ix0];
    const h11 = h[iz1 * SIZE + ix1];
    return ((h00 * (1 - fx) + h10 * fx) * (1 - fz) +
            (h01 * (1 - fx) + h11 * fx) * fz) * CONFIG.HEIGHT_AMPLITUDE;
  }
  /*
   * update: advance each particle along its velocity vector, sample terrain height,
   * respawn particles that exit bounds or exceed lifetime.
   */
  update(timeIndex) {
    const half = (SIZE - 1) * CONFIG.TERRAIN_SCALE * 0.5;
    const bounds = half * 0.95;
    for (let i = 0; i < this.count; i++) {
      this.ages[i] += 1;
      const i3 = i * 3;
      const i2 = i * 2;
      /* respawn if too old or out of bounds */
      if (this.ages[i] > CONFIG.PARTICLE_LIFETIME_FRAMES ||
          Math.abs(this.positions[i3]) > bounds ||
          Math.abs(this.positions[i3 + 2]) > bounds) {
        this.positions[i3]     = (Math.random() - 0.5) * half * 2;
        this.positions[i3 + 2] = (Math.random() - 0.5) * half * 2;
        const angle = (Math.random() - 0.5) * Math.PI * 0.7;
        const speed = 0.03 + Math.random() * 0.07;
        this.velocities[i2]     = Math.cos(angle) * speed;
        this.velocities[i2 + 1] = Math.sin(angle) * speed;
        this.ages[i] = 0;
      }
      /* advance */
      this.positions[i3]     += this.velocities[i2] * CONFIG.PARTICLE_SPEED_FACTOR;
      this.positions[i3 + 2] += this.velocities[i2 + 1] * CONFIG.PARTICLE_SPEED_FACTOR;
      /* clamp y to terrain surface + small offset */
      const h = this.sampleHeight(this.positions[i3], this.positions[i3 + 2], timeIndex);
      if (h !== null) {
        this.positions[i3 + 1] = h + 0.25;
      } else {
        this.positions[i3 + 1] = 0.25;
      }
      /* fade alpha via color dimming as particle ages */
      const lifeRatio = 1 - this.ages[i] / CONFIG.PARTICLE_LIFETIME_FRAMES;
      const rgb = new THREE.Color().setHSL(0.12 + Math.random() * 0.02, 0.9, 0.55);
      this.colors[i3]     = rgb.r * lifeRatio;
      this.colors[i3 + 1] = rgb.g * lifeRatio;
      this.colors[i3 + 2] = rgb.b * lifeRatio;
    }
    this.geometry.attributes.position.needsUpdate = true;
    this.geometry.attributes.color.needsUpdate = true;
  }
}
const particleSystem = new ParticleFlowSystem(CONFIG.PARTICLE_COUNT);
scene.add(particleSystem.points);
/* ---- Sub-surface glow plane (ambient glow beneath terrain) ---- */
const glowGeo = new THREE.PlaneGeometry(CONFIG.TERRAIN_SIZE * CONFIG.TERRAIN_SCALE * 1.1, CONFIG.TERRAIN_SIZE * CONFIG.TERRAIN_SCALE * 1.1);
const glowMat = new THREE.ShaderMaterial({
  uniforms: {
    uTime: { value: 0 }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying vec2 vUv;
    uniform float uTime;
    void main() {
      float dist = length(vUv - 0.5) * 2.0;
      float glow = exp(-dist * 3.5) * 0.15;
      glow += sin(dist * 20.0 + uTime * 0.5) * 0.03;
      gl_FragColor = vec4(0.2, 0.35, 0.7, glow);
    }
  `,
  transparent: true,
  depthWrite: false,
});
const glowPlane = new THREE.Mesh(glowGeo, glowMat);
glowPlane.rotation.x = -Math.PI / 2;
glowPlane.position.y = -CONFIG.HEIGHT_AMPLITUDE - 0.5;
glowPlane.renderOrder = 0;
scene.add(glowPlane);
/* ---- UI State ---- */
let wireframeMode = false;
let riversVisible = true;
/* ---- DOM references ---- */
const timeSlider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
const btnAutoRotate = document.getElementById('btn-auto-rotate');
const btnWireframe = document.getElementById('btn-wireframe');
const btnTopDown = document.getElementById('btn-top-down');
const btnRivers = document.getElementById('btn-rivers');
const hudHeight = document.getElementById('hud-height');
const hudDensity = document.getElementById('hud-density');
const hudError = document.getElementById('hud-error');
const hudParticles = document.getElementById('hud-particles');
const hudFps = document.getElementById('hud-fps');
/* ---- Time Slider: reshape terrain on scrub ---- */
function updateTerrain(newIndex) {
  currentTimeIndex = newIndex;
  /* Dispose old geometry and build new one */
  terrainGeo.dispose();
  terrainGeo = buildTerrainGeometry(newIndex);
  terrainMesh.geometry = terrainGeo;
  /* Rebuild rivers */
  if (riverMesh) {
    riverMesh.traverse(child => {
      if (child.geometry) child.geometry.dispose();
      if (child.material) child.material.dispose();
    });
    scene.remove(riverMesh);
  }
  riverMesh = buildRiverGeometry(newIndex);
  riverMesh.visible = riversVisible;
  scene.add(riverMesh);
  /* Update HUD */
  const heights = heightData[newIndex];
  const densities = densityData[newIndex];
  const errors = errorData[newIndex];
  let sumH = 0, sumD = 0, sumE = 0;
  const total = heights.length;
  for (let i = 0; i < total; i++) {
    sumH += heights[i] * CONFIG.HEIGHT_AMPLITUDE;
    sumD += densities[i];
    sumE += errors[i];
  }
  hudHeight.textContent = (sumH / total).toFixed(1) + 'm';
  hudDensity.textContent = (sumD / total * 100).toFixed(0) + '%';
  hudError.textContent = (sumE / total * 100).toFixed(1) + '%';
  /* Format time label as HH:00 */
  const hour = String(newIndex).padStart(2, '0');
  timeLabel.textContent = hour + ':00';
}
timeSlider.addEventListener('input', () => {
  const idx = parseInt(timeSlider.value);
  updateTerrain(idx);
});
/* ---- Buttons ---- */
btnAutoRotate.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAutoRotate.classList.toggle('active', controls.autoRotate);
});
btnWireframe.addEventListener('click', () => {
  wireframeMode = !wireframeMode;
  terrainMaterial.wireframe = wireframeMode;
  btnWireframe.classList.toggle('active', wireframeMode);
});
btnTopDown.addEventListener('click', () => {
  /* Animate to top-down view */
  const target = new THREE.Vector3(0, CONFIG.HEIGHT_AMPLITUDE * 0.3, 0);
  const pos = new THREE.Vector3(0, 22, 0.1);
  /* Smooth transition using GSAP-like lerp over several frames */
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  const DURATION = 800; /* ms for animation */
  function animateTopDown(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / DURATION);
    /* easeInOutCubic */
    const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    camera.position.lerpVectors(startPos, pos, ease);
    controls.target.lerpVectors(startTarget, target, ease);
    controls.update();
    if (t < 1) {
      requestAnimationFrame(animateTopDown);
    }
  }
  requestAnimationFrame(animateTopDown);
});
btnRivers.addEventListener('click', () => {
  riversVisible = !riversVisible;
  if (riverMesh) riverMesh.visible = riversVisible;
  btnRivers.classList.toggle('active', !riversVisible);
});
/* ---- Camera bookmarks ---- */
document.querySelectorAll('.bm-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const preset = BOOKMARKS[btn.dataset.preset];
    if (!preset) return;
    const pos = new THREE.Vector3(...preset.position);
    const target = new THREE.Vector3(...preset.target);
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const startTime = performance.now();
    const DURATION = 700;
    function animateBookmark(now) {
      const elapsed = now - startTime;
      const t = Math.min(1, elapsed / DURATION);
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      camera.position.lerpVectors(startPos, pos, ease);
      controls.target.lerpVectors(startTarget, target, ease);
      controls.update();
      if (t < 1) {
        requestAnimationFrame(animateBookmark);
      }
    }
    requestAnimationFrame(animateBookmark);
  });
});
/* ---- Keyboard shortcuts ---- */
window.addEventListener('keydown', (e) => {
  switch (e.key.toLowerCase()) {
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      btnAutoRotate.classList.toggle('active', controls.autoRotate);
      break;
    case 'w':
      wireframeMode = !wireframeMode;
      terrainMaterial.wireframe = wireframeMode;
      btnWireframe.classList.toggle('active', wireframeMode);
      break;
    case 't':
      btnTopDown.click();
      break;
    case 'arrowleft':
      timeSlider.value = Math.max(0, currentTimeIndex - 1);
      updateTerrain(parseInt(timeSlider.value));
      break;
    case 'arrowright':
      timeSlider.value = Math.min(STEPS - 1, currentTimeIndex + 1);
      updateTerrain(parseInt(timeSlider.value));
      break;
  }
});
/* ---- FPS counter ---- */
let frameCount = 0;
let lastFpsTime = performance.now();
/* ---- Render Loop ---- */
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  /* Update particles with current time slice */
  particleSystem.update(currentTimeIndex);
  /* Update glow shader uniform */
  glowMat.uniforms.uTime.value = timestamp * 0.001;
  /* FPS counter */
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    hudFps.textContent = frameCount;
    hudParticles.textContent = CONFIG.PARTICLE_COUNT;
    frameCount = 0;
    lastFpsTime = timestamp;
  }
  renderer.render(scene, camera);
}
/* ---- Resize handler ---- */
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ---- Initialize HUD with default time slice ---- */
updateTerrain(CONFIG.TIME_DEFAULT_INDEX);
timeSlider.value = CONFIG.TIME_DEFAULT_INDEX;
/* ---- Start ---- */
requestAnimationFrame(animate);
console.log('3D Data Terrain Explorer ready — drag to orbit, scroll to zoom, right-drag to pan');
</script>
</body>
</html>