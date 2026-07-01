<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5}
  canvas{display:block}
  #panel{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(10,10,30,0.85);border:1px solid rgba(100,140,255,0.3);border-radius:12px;padding:12px 20px;display:flex;gap:16px;align-items:center;backdrop-filter:blur(8px);z-index:10}
  #panel label{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:#8395a7}
  #timeSlider{width:200px;accent-color:#4a90d9}
  #timeValue{font-size:14px;font-weight:600;color:#4a90d9;min-width:50px;text-align:center}
  button{background:rgba(74,144,217,0.15);border:1px solid rgba(74,144,217,0.4);color:#a0c4f0;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.2s}
  button:hover{background:rgba(74,144,217,0.3);border-color:rgba(74,144,217,0.7)}
  button.active{background:rgba(74,144,217,0.4);border-color:#4a90d9;color:#fff}
  #bookmarks{display:flex;gap:6px}
  #fps{position:absolute;top:12px;right:16px;font-size:11px;color:#5f7a9a;z-index:10}
  #legend{position:absolute;top:12px;left:16px;z-index:10;font-size:11px;color:#8395a7}
  #legend .bar{display:inline-block;width:60px;height:8px;border-radius:4px;background:linear-gradient(to right,#2ecc71,#f1c40f,#e74c3c);margin-left:6px;vertical-align:middle}
  #tooltip{position:absolute;pointer-events:none;background:rgba(0,0,0,0.8);color:#fff;padding:4px 8px;border-radius:4px;font-size:11px;display:none;z-index:20}
</style>
</head>
<body>
<div id="fps">FPS: --</div>
<div id="legend">User Density <span class="bar"></span></div>
<div id="tooltip"></div>
<div id="panel">
  <label>Time</label>
  <input type="range" id="timeSlider" min="0" max="23" value="12" step="1">
  <span id="timeValue">12:00</span>
  <button id="btnPlay">Play</button>
  <button id="btnWireframe">Wire</button>
  <div id="bookmarks">
    <button data-bookmark="0">Top</button>
    <button data-bookmark="1">Valley</button>
    <button data-bookmark="2">Rivers</button>
    <button data-bookmark="3">Close</button>
  </div>
</div>
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
// --- Object Pool ---
const _v3 = { a:new THREE.Vector3(), b:new THREE.Vector3(), c:new THREE.Vector3() };
const _col = { a:new THREE.Color(), b:new THREE.Color() };
const _frustum = new THREE.Frustum();
const _projScreen = new THREE.Matrix4();
const _ray = new THREE.Ray();
// --- Scene Setup ---
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 40, 120);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.5, 200);
camera.position.set(18, 22, 28);
camera.lookAt(0, 0, 0);
// --- Controls ---
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.target.set(0, 2, 0);
controls.minDistance = 8;
controls.maxDistance = 70;
controls.maxPolarAngle = Math.PI * 0.58;
controls.update();
// --- Lights ---
const ambient = new THREE.AmbientLight(0x1a1a3a, 2.5);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 12);
sun.position.set(30, 40, 20);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 150;
sun.shadow.camera.left = -30;
sun.shadow.camera.right = 30;
sun.shadow.camera.top = 30;
sun.shadow.camera.bottom = -30;
sun.shadow.bias = -0.0003;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 4);
fill.position.set(-10, 5, -10);
scene.add(fill);
const rim = new THREE.DirectionalLight(0x8899cc, 3);
rim.position.set(0, -2, 15);
scene.add(rim);
// --- Grid & Ground ---
const gridHelper = new THREE.PolarGridHelper(28, 40, 28, 128, 0x1a1a3a, 0x1a1a3a);
gridHelper.position.y = -0.1;
scene.add(gridHelper);
// --- Data Generator ---
const GRID = 100;
const TIMEPOINTS = 24;
const heights = new Array(TIMEPOINTS);
const densities = new Array(TIMEPOINTS);
const riverPaths = new Array(TIMEPOINTS);
const particleTrails = [];
function gaussian(x, y, cx, cy, sx, sy) {
  const dx = (x - cx) / sx, dy = (y - cy) / sy;
  return Math.exp(-0.5 * (dx*dx + dy*dy));
}
function mix(a, b, t) { return a + (b - a) * t; }
// Precompute all timepoint data
for (let t = 0; t < TIMEPOINTS; t++) {
  const h = new Float32Array(GRID * GRID);
  const d = new Float32Array(GRID * GRID);
  const timeFrac = t / (TIMEPOINTS - 1);
  // Evolving peak clusters
  const peaks = [
    { cx: 0.25 + timeFrac*0.15, cy: 0.35, sx: 0.12, sy: 0.10, amp: 8 + timeFrac*6 },
    { cx: 0.60 - timeFrac*0.10, cy: 0.55 + timeFrac*0.15, sx: 0.14, sy: 0.11, amp: 6 + timeFrac*8 },
    { cx: 0.45, cy: 0.25, sx: 0.10, sy: 0.13, amp: 5 + Math.sin(timeFrac*Math.PI)*4 },
    { cx: 0.70, cy: 0.70, sx: 0.08, sy: 0.09, amp: 4 + timeFrac*3 },
    { cx: 0.15 + timeFrac*0.20, cy: 0.70, sx: 0.11, sy: 0.10, amp: 3 + Math.sin(timeFrac*Math.PI*2)*2 },
  ];
  for (let iy = 0; iy < GRID; iy++) {
    for (let ix = 0; ix < GRID; ix++) {
      const nx = ix / (GRID - 1);
      const ny = iy / (GRID - 1);
      let elevation = 1.0;
      for (const p of peaks) {
        elevation += gaussian(nx, ny, p.cx, p.cy, p.sx, p.sy) * p.amp;
      }
      // Noise ridges
      elevation += Math.sin(nx*8 + timeFrac*3) * Math.cos(ny*6 + timeFrac*2) * 0.8;
      elevation += Math.sin(nx*14 + ny*10) * 0.3;
      elevation = Math.max(0.2, elevation);
      h[iy * GRID + ix] = elevation;
      // Density: blend of proximity to peaks + noise
      let density = 0;
      for (const p of peaks) {
        density += gaussian(nx, ny, p.cx, p.cy, p.sx*1.5, p.sy*1.5) * 0.5;
      }
      density += Math.abs(Math.sin(nx*12 + ny*8 + timeFrac))*0.15;
      density = Math.min(1, Math.max(0, density));
      d[iy * GRID + ix] = density;
    }
  }
  heights[t] = h;
  densities[t] = d;
  // River paths: trace valleys (low elevation) where error spikes
  const riverSegments = [];
  const numRivers = 3;
  for (let r = 0; r < numRivers; r++) {
    const startX = 5 + r * 30;
    const startY = 10 + r * 25;
    const segments = [{x: startX, y: startY}];
    let cx = startX, cy = startY;
    for (let step = 0; step < 60; step++) {
      // Flow downhill: check 8 neighbors, pick lowest
      let bestDx = 0, bestDy = 0, lowest = h[Math.round(cy)*GRID + Math.round(cx)] || 99;
      for (let dy = -1; dy <=1; dy++) {
        for (let dx = -1; dx <=1; dx++) {
          if (dx===0 && dy===0) continue;
          const nx = Math.round(cx + dx), ny = Math.round(cy + dy);
          if (nx<0||nx>=GRID||ny<0||ny>=GRID) continue;
          const val = h[ny*GRID + nx];
          if (val < lowest) { lowest = val; bestDx = dx; bestDy = dy; }
        }
      }
      cx += bestDx; cy += bestDy;
      if (cx<0||cx>=GRID||cy<0||cy>=GRID) break;
      segments.push({x: cx, y: cy});
      if (segments.length > 2) {
        const p0 = segments[segments.length-2];
        const p1 = segments[segments.length-1];
        if (Math.abs(p1.x-p0.x)<0.1 && Math.abs(p1.y-p0.y)<0.1) break;
      }
    }
    riverSegments.push(segments);
  }
  riverPaths[t] = riverSegments;
}
// Precompute particle trails across all timepoints
const NUM_PARTICLES = 600;
const trailWaypoints = [
  { from: [0.25,0.35], to: [0.60,0.55], via: [[0.40,0.40],[0.50,0.45]] },
  { from: [0.45,0.25], to: [0.70,0.70], via: [[0.55,0.45]] },
  { from: [0.15,0.70], to: [0.25,0.35], via: [[0.20,0.50]] },
  { from: [0.60,0.55], to: [0.70,0.70], via: [[0.65,0.62]] },
  { from: [0.25,0.35], to: [0.45,0.25], via: [[0.35,0.30]] },
];
function buildTrail(waypoint) {
  const points = [];
  const [fx, fy] = waypoint.from;
  const [tx, ty] = waypoint.to;
  const vias = waypoint.via || [];
  const allPts = [[fx,fy], ...vias, [tx,ty]];
  for (let i = 0; i < allPts.length - 1; i++) {
    const [ax, ay] = allPts[i];
    const [bx, by] = allPts[i+1];
    const steps = 40;
    for (let s = 0; s <= steps; s++) {
      const t = s / steps;
      points.push([mix(ax, bx, t), mix(ay, by, t)]);
    }
  }
  return points;
}
for (const wp of trailWaypoints) {
  particleTrails.push(buildTrail(wp));
}
// --- Terrain Mesh ---
const terrainGeo = new THREE.BufferGeometry();
const vertCount = GRID * GRID;
const posArray = new Float32Array(vertCount * 3);
const colArray = new Float32Array(vertCount * 3);
const idxArray = new Uint32Array((GRID-1) * (GRID-1) * 6);
// Vertex positions (will be updated on timeslider)
for (let iy = 0; iy < GRID; iy++) {
  for (let ix = 0; ix < GRID; ix++) {
    const i = iy * GRID + ix;
    const x = (ix / (GRID-1) - 0.5) * 30;
    const z = (iy / (GRID-1) - 0.5) * 30;
    posArray[i*3] = x;
    posArray[i*3+1] = 0;
    posArray[i*3+2] = z;
  }
}
terrainGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colArray, 3));
// Indices
let idxPtr = 0;
for (let iy = 0; iy < GRID-1; iy++) {
  for (let ix = 0; ix < GRID-1; ix++) {
    const a = iy * GRID + ix;
    const b = a + 1;
    const c = a + GRID;
    const d = c + 1;
    idxArray[idxPtr++] = a; idxArray[idxPtr++] = b; idxArray[idxPtr++] = d;
    idxArray[idxPtr++] = a; idxArray[idxPtr++] = d; idxArray[idxPtr++] = c;
  }
}
terrainGeo.setIndex(new THREE.BufferAttribute(idxArray, 1));
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.55,
  metalness: 0.05,
  flatShading: false,
  side: THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
terrainMesh.castShadow = true;
terrainMesh.receiveShadow = true;
scene.add(terrainMesh);
// --- Wireframe overlay ---
const wireGeo = new THREE.BufferGeometry();
const wirePosArray = new Float32Array(vertCount * 3);
wireGeo.setAttribute('position', new THREE.BufferAttribute(wirePosArray, 3));
wireGeo.setIndex(new THREE.BufferAttribute(new Uint32Array(idxArray), 1));
const wireMat = new THREE.MeshBasicMaterial({ color:0x334466, wireframe:true, transparent:true, opacity:0.15 });
const wireMesh = new THREE.Mesh(wireGeo, wireMat);
wireMesh.visible = false;
scene.add(wireMesh);
// --- River Lines ---
const riverGroup = new THREE.Group();
scene.add(riverGroup);
const riverMaterial = new THREE.LineBasicMaterial({ color:0xff3344, linewidth:1, transparent:true, opacity:0.85 });
function createRiverGeometry(segments) {
  const pts = [];
  for (const seg of segments) {
    for (const p of seg) {
      const x = (p.x/(GRID-1)-0.5)*30;
      const z = (p.y/(GRID-1)-0.5)*30;
      const idx = Math.round(p.y)*GRID + Math.round(p.x);
      const y = (idx>=0 && idx<vertCount) ? posArray[idx*3+1] : 0;
      pts.push(x, y + 0.15, z);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
  return geo;
}
// --- Particles ---
const particleGroup = new THREE.Group();
scene.add(particleGroup);
const particleMat = new THREE.PointsMaterial({
  color:0x4af0ff,
  size:0.12,
  blending:THREE.AdditiveBlending,
  depthWrite:false,
  transparent:true,
  opacity:0.8,
});
const particlePositions = new Float32Array(NUM_PARTICLES * 3);
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
const particlePoints = new THREE.Points(particleGeo, particleMat);
particleGroup.add(particlePoints);
// Particle state
const particleState = [];
for (let i = 0; i < NUM_PARTICLES; i++) {
  const trailIdx = i % particleTrails.length;
  const trail = particleTrails[trailIdx];
  const segStart = Math.floor(Math.random() * (trail.length - 1));
  particleState.push({
    trailIdx,
    t: Math.random(),
    speed: 0.0008 + Math.random() * 0.0025,
    offset: Math.random() * 0.3,
    segStart,
  });
}
// --- Camera Bookmarks ---
const bookmarks = [
  { pos:[18,22,28], target:[0,2,0], label:'Overview' },
  { pos:[5,4,5], target:[-3,3,-3], label:'Valley View' },
  { pos:[12,6,-10], target:[0,2,3], label:'Rivers' },
  { pos:[3,3,2], target:[2,3.5,3], label:'Close-up' },
];
// --- Height update function ---
function getHeightAt(hdata, nx, nz) {
  const gx = nx / 30 + 0.5;
  const gz = nz / 30 + 0.5;
  const ix = Math.round(gx * (GRID-1));
  const iy = Math.round(gz * (GRID-1));
  if (ix<0||ix>=GRID||iy<0||iy>=GRID) return 0.5;
  return hdata[iy*GRID + ix];
}
function updateTerrainToTimepoint(t) {
  const h = heights[t];
  const d = densities[t];
  const pos = terrainGeo.attributes.position.array;
  const col = terrainGeo.attributes.color.array;
  for (let i = 0; i < vertCount; i++) {
    pos[i*3+1] = h[i];
    // Color from density: green->yellow->red
    const density = d[i];
    _col.a.setRGB(
      density < 0.5 ? density*2 : 1,
      density < 0.5 ? 0.8 : 2*(1-density),
      0.15 + density*0.1
    );
    col[i*3] = _col.a.r;
    col[i*3+1] = _col.a.g;
    col[i*3+2] = _col.a.b;
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  // Wireframe
  const wpos = wireGeo.attributes.position.array;
  wpos.set(pos);
  wireGeo.attributes.position.needsUpdate = true;
  // Rivers
  while (riverGroup.children.length) riverGroup.remove(riverGroup.children[0]);
  const rivers = riverPaths[t];
  for (const seg of rivers) {
    const geo = createRiverGeometry(seg);
    const line = new THREE.Line(geo, riverMaterial);
    riverGroup.add(line);
  }
}
// --- Initial state ---
let currentTime = 12;
updateTerrainToTimepoint(currentTime);
// --- UI Handlers ---
const slider = document.getElementById('timeSlider');
const timeValue = document.getElementById('timeValue');
const btnPlay = document.getElementById('btnPlay');
const btnWireframe = document.getElementById('btnWireframe');
let playing = false;
let playTimer = null;
function formatTime(t) {
  const h = String(t).padStart(2,'0');
  return `${h}:00`;
}
slider.addEventListener('input', () => {
  currentTime = parseInt(slider.value);
  timeValue.textContent = formatTime(currentTime);
  updateTerrainToTimepoint(currentTime);
});
btnPlay.addEventListener('click', () => {
  playing = !playing;
  btnPlay.textContent = playing ? 'Pause' : 'Play';
  btnPlay.classList.toggle('active', playing);
  if (playing) {
    function step() {
      if (!playing) return;
      currentTime = (currentTime + 1) % TIMEPOINTS;
      slider.value = currentTime;
      timeValue.textContent = formatTime(currentTime);
      updateTerrainToTimepoint(currentTime);
      playTimer = setTimeout(step, 600);
    }
    step();
  } else {
    clearTimeout(playTimer);
  }
});
btnWireframe.addEventListener('click', () => {
  wireMesh.visible = !wireMesh.visible;
  btnWireframe.classList.toggle('active', wireMesh.visible);
});
document.getElementById('bookmarks').addEventListener('click', (e) => {
  const btn = e.target.closest('button');
  if (!btn || btn.dataset.bookmark === undefined) return;
  const bm = bookmarks[parseInt(btn.dataset.bookmark)];
  if (!bm) return;
  // Animate camera
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const endPos = new THREE.Vector3(...bm.pos);
  const endTarget = new THREE.Vector3(...bm.target);
  const startTime = performance.now();
  const duration = 1200;
  function anim(now) {
    const elapsed = now - startTime;
    const t = Math.min(1, elapsed / duration);
    const ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t; // easeInOutQuad
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTarget, endTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
});
// --- FPS Counter ---
const fpsEl = document.getElementById('fps');
let frameCount = 0;
let lastFpsTime = performance.now();
// --- Render Loop ---
function animate(timestamp) {
  requestAnimationFrame(animate);
  controls.update();
  // Update particles
  const pp = particleGeo.attributes.position.array;
  const h = heights[currentTime];
  for (let i = 0; i < NUM_PARTICLES; i++) {
    const state = particleState[i];
    state.t += state.speed;
    const trail = particleTrails[state.trailIdx];
    if (state.t >= 1) { state.t -= 1; }
    const idx = Math.floor(state.t * (trail.length - 1));
    const frac = state.t * (trail.length - 1) - idx;
    const nextIdx = Math.min(idx + 1, trail.length - 1);
    const p0 = trail[idx], p1 = trail[nextIdx];
    const nx = mix(p0[0], p1[0], frac);
    const nz = mix(p0[1], p1[1], frac);
    const x = (nx - 0.5) * 30;
    const z = (nz - 0.5) * 30;
    const y = getHeightAt(h, x, z) + 0.4 + state.offset;
    pp[i*3] = x;
    pp[i*3+1] = y;
    pp[i*3+2] = z;
  }
  particleGeo.attributes.position.needsUpdate = true;
  renderer.render(scene, camera);
  // FPS
  frameCount++;
  if (timestamp - lastFpsTime >= 1000) {
    const fps = Math.round(frameCount / ((timestamp - lastFpsTime) / 1000));
    fpsEl.textContent = `FPS: ${fps}`;
    frameCount = 0;
    lastFpsTime = timestamp;
  }
}
// --- Resize ---
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// --- Keyboard shortcuts ---
window.addEventListener('keydown', (e) => {
  switch(e.key.toLowerCase()) {
    case ' ':
      e.preventDefault();
      btnPlay.click();
      break;
    case 'w':
      btnWireframe.click();
      break;
    case '1': currentTime=0; slider.value=0; timeValue.textContent=formatTime(0); updateTerrainToTimepoint(0); break;
    case '2': currentTime=6; slider.value=6; timeValue.textContent=formatTime(6); updateTerrainToTimepoint(6); break;
    case '3': currentTime=12; slider.value=12; timeValue.textContent=formatTime(12); updateTerrainToTimepoint(12); break;
    case '4': currentTime=18; slider.value=18; timeValue.textContent=formatTime(18); updateTerrainToTimepoint(18); break;
    case 'r':
      controls.autoRotate = !controls.autoRotate;
      break;
  }
});
// --- Start ---
requestAnimationFrame(animate);
console.log('3D Data Terrain Explorer ready — drag to orbit, scroll to zoom, right-drag to pan');
console.log('Space=play/pause  W=wireframe  R=auto-rotate  1-4=time snap  buttons=bookmarks');
</script>
</body>
</html>