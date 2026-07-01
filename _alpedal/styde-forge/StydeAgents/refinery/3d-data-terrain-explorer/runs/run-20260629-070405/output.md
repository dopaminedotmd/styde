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
#ui{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;background:rgba(10,10,20,0.85);backdrop-filter:blur(12px);padding:12px 20px;border-radius:12px;border:1px solid rgba(255,255,255,0.12);z-index:10}
#time-slider{-webkit-appearance:none;width:240px;height:6px;border-radius:3px;background:linear-gradient(90deg,#2ecc71,#e67e22,#e74c3c);outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 0 12px rgba(255,255,255,0.5);cursor:pointer}
#time-label{color:#ccc;font-size:13px;min-width:80px;text-align:center}
#legend{position:fixed;top:20px;right:20px;display:flex;flex-direction:column;gap:6px;background:rgba(10,10,20,0.85);backdrop-filter:blur(12px);padding:14px 18px;border-radius:10px;border:1px solid rgba(255,255,255,0.12);z-index:10}
.legend-item{display:flex;align-items:center;gap:8px;font-size:12px;color:#aaa}
.legend-swatch{width:14px;height:14px;border-radius:3px}
#bookmark-bar{position:fixed;top:20px;left:20px;display:flex;flex-direction:column;gap:5px;z-index:10}
.bm-btn{background:rgba(10,10,20,0.75);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.15);color:#ccc;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:11px;transition:all 0.2s}
.bm-btn:hover{background:rgba(255,255,255,0.12);color:#fff}
#tooltip{position:fixed;pointer-events:none;background:rgba(0,0,0,0.85);color:#fff;padding:6px 10px;border-radius:6px;font-size:11px;display:none;z-index:20}
</style>
</head>
<body>
<canvas id="canvas"></canvas>
<div id="legend">
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(180deg,#2ecc71,#f1c40f,#e74c3c)"></div>Elevation (Revenue)</div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(180deg,#1a3a1a,#2d8c2d,#5cd65c)"></div>User Density</div>
  <div class="legend-item"><div class="legend-swatch" style="background:#e74c3c"></div>Error Rivers</div>
  <div class="legend-item"><div class="legend-swatch" style="background:linear-gradient(90deg,#3498db,#9b59b6)"></div>API Trail Particles</div>
</div>
<div id="bookmark-bar">
  <button class="bm-btn" data-cam="0">Default Overview</button>
  <button class="bm-btn" data-cam="1">Top-Down</button>
  <button class="bm-btn" data-cam="2">Close Valley</button>
  <button class="bm-btn" data-cam="3">Error Hotspot</button>
</div>
<div id="ui">
  <span style="color:#aaa;font-size:12px">Time</span>
  <input type="range" id="time-slider" min="0" max="23" value="12">
  <span id="time-label">Hour 12</span>
</div>
<div id="tooltip"></div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 80;
const SIZE = 40;
const HALF = SIZE / 2;
const CELL = SIZE / GRID;
const HOURS = 24;
const canvas = document.getElementById('canvas');
const renderer = new THREE.WebGLRenderer({canvas, antialias:true, alpha:false});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a1e);
scene.fog = new THREE.FogExp2(0x0a0a1e, 0.00015);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 2, 200);
camera.position.set(28, 22, 32);
camera.lookAt(0, 4, 0);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.25;
controls.target.set(0, 5, 0);
controls.minDistance = 8;
controls.maxDistance = 60;
controls.maxPolarAngle = Math.PI * 0.48;
controls.update();
const bookmarks = [
  {pos:[28,22,32],tgt:[0,5,0]},
  {pos:[0,38,2],tgt:[0,0,0]},
  {pos:[8,4,14],tgt:[3,2,10]},
  {pos:[-10,6,-8],tgt:[-8,1,-6]}
];
document.querySelectorAll('.bm-btn').forEach(b => {
  b.addEventListener('click', () => {
    const bm = bookmarks[parseInt(b.dataset.cam)];
    animateCamera(bm.pos, bm.tgt);
  });
});
function animateCamera(pos, tgt, duration = 1200) {
  const startPos = camera.position.clone();
  const startTgt = controls.target.clone();
  const endPos = new THREE.Vector3(...pos);
  const endTgt = new THREE.Vector3(...tgt);
  const start = performance.now();
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    const ease = t < 0.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2;
    camera.position.lerpVectors(startPos, endPos, ease);
    controls.target.lerpVectors(startTgt, endTgt, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
const ambientLight = new THREE.AmbientLight(0x1a1a3a, 1.8);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(30, 40, 20);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 120;
sunLight.shadow.camera.left = -35;
sunLight.shadow.camera.right = 35;
sunLight.shadow.camera.top = 35;
sunLight.shadow.camera.bottom = -35;
sunLight.shadow.bias = -0.0004;
scene.add(ambientLight, sunLight);
const fillLight = new THREE.DirectionalLight(0x3344aa, 1.2);
fillLight.position.set(-20, 5, -15);
scene.add(fillLight);
const groundGeo = new THREE.PlaneGeometry(SIZE * 1.6, SIZE * 1.6);
const groundMat = new THREE.MeshStandardMaterial({color:0x111122, roughness:0.95});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI/2;
ground.position.y = -0.3;
ground.receiveShadow = true;
scene.add(ground);
function generateTimeSeriesData() {
  const data = [];
  for (let h = 0; h < HOURS; h++) {
    const t = h / HOURS;
    const heights = new Float32Array(GRID * GRID);
    const density = new Float32Array(GRID * GRID);
    const errors = new Float32Array(GRID * GRID);
    const traffic = new Float32Array(GRID * GRID);
    for (let iz = 0; iz < GRID; iz++) {
      for (let ix = 0; ix < GRID; ix++) {
        const idx = iz * GRID + ix;
        const x = (ix / GRID - 0.5) * SIZE;
        const z = (iz / GRID - 0.5) * SIZE;
        const base = Math.sin(x*0.45 + t*2.1) * Math.cos(z*0.38 + t*1.7) * 4;
        const ridge = Math.sin(x*0.8 + z*0.6) * 2.5 + Math.cos(x*0.5 - z*0.7 + t*0.9) * 1.8;
        const noise = valueNoise(x*1.3, z*1.3, t*3.0) * 3.2;
        heights[idx] = base + ridge + noise + 2.5;
        density[idx] = Math.abs(Math.sin(x*0.35 + t*1.3) * Math.cos(z*0.42 + t*0.8)) * 0.7 + valueNoise(x*0.9, z*0.9, t*2.0)*0.3;
        errors[idx] = Math.max(0, Math.sin(x*0.7 - t*1.5) * Math.cos(z*0.55 + t*1.1) * 0.55 + valueNoise(x*1.5, z*1.5, 0)*0.3);
        traffic[idx] = Math.abs(Math.sin(x*0.5 + z*0.4 + t*2.5)) * 0.5 + valueNoise(x*0.6, z*0.6, t*1.8)*0.4;
      }
    }
    data.push({heights, density, errors, traffic});
  }
  return data;
}
const PERM = new Uint8Array(512);
const GRAD = [[1,1],[-1,1],[1,-1],[-1,-1],[1,0],[-1,0],[0,1],[0,-1]];
(function initPerm() {
  const p = new Uint8Array(256);
  for (let i = 0; i < 256; i++) p[i] = i;
  for (let i = 255; i > 0; i--) {
    const j = Math.floor(Math.random() * (i+1));
    [p[i],p[j]] = [p[j],p[i]];
  }
  for (let i = 0; i < 512; i++) PERM[i] = p[i & 255];
})();
function fade(t) { return t*t*t*(t*(t*6-15)+10); }
function lerp(a,b,t) { return a + t*(b-a); }
function dotGrid(ix,iy,x,y) {
  const g = GRAD[PERM[PERM[ix&255]+(iy&255)] & 7];
  return g[0]*(x-ix) + g[1]*(y-iy);
}
function valueNoise(x, y, z) {
  const ix = Math.floor(x), iy = Math.floor(y), iz = Math.floor(z);
  const fx = fade(x-ix), fy = fade(y-iy), fz = fade(z-iz);
  const c000 = hash3(ix,iy,iz);
  const c100 = hash3(ix+1,iy,iz);
  const c010 = hash3(ix,iy+1,iz);
  const c110 = hash3(ix+1,iy+1,iz);
  const c001 = hash3(ix,iy,iz+1);
  const c101 = hash3(ix+1,iy,iz+1);
  const c011 = hash3(ix,iy+1,iz+1);
  const c111 = hash3(ix+1,iy+1,iz+1);
  return lerp(
    lerp(lerp(c000,c100,fx), lerp(c010,c110,fx), fy),
    lerp(lerp(c001,c101,fx), lerp(c011,c111,fx), fy),
    fz
  );
}
function hash3(x,y,z) {
  let h = PERM[x&255] ^ PERM[y&255] ^ PERM[z&255];
  h = ((h >> 16) ^ h) * 0x45d9f3b;
  h = ((h >> 16) ^ h) * 0x45d9f3b;
  h = (h >> 16) ^ h;
  return (h & 0x7fffffff) / 0x7fffffff * 2 - 1;
}
const timeSeriesData = generateTimeSeriesData();
function aStarPath(heightMap, startX, startZ, endX, endZ) {
  const w = GRID, h = GRID;
  const costMap = new Float32Array(w*h);
  for (let i = 0; i < w*h; i++) costMap[i] = 1 + Math.max(0, heightMap[i]) * 0.8;
  const heuristic = (x1,z1,x2,z2) => Math.abs(x1-x2) + Math.abs(z1-z2);
  const key = (x,z) => z*w + x;
  const open = new Map();
  const closed = new Set();
  const parent = new Map();
  const gScore = new Float32Array(w*h).fill(Infinity);
  const sid = key(startX, startZ);
  gScore[sid] = 0;
  open.set(sid, heuristic(startX,startZ,endX,endZ));
  const dirs = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[1,-1],[-1,1]];
  while (open.size) {
    let bestK = null, bestF = Infinity;
    for (const [k,f] of open) { if (f < bestF) { bestF = f; bestK = k; } }
    const cx = bestK % w, cz = Math.floor(bestK / w);
    if (cx === endX && cz === endZ) {
      const path = [];
      let k = bestK;
      while (k !== sid) { path.unshift(k); k = parent.get(k); }
      return path;
    }
    open.delete(bestK);
    closed.add(bestK);
    for (const [dx,dz] of dirs) {
      const nx = cx+dx, nz = cz+dz;
      if (nx<0||nx>=w||nz<0||nz>=h) continue;
      const nk = key(nx,nz);
      if (closed.has(nk)) continue;
      const cost = costMap[nz*w+nx] * (dx&&dz?1.414:1);
      const tg = gScore[bestK] + cost;
      if (tg < gScore[nk]) {
        parent.set(nk, bestK);
        gScore[nk] = tg;
        open.set(nk, tg + heuristic(nx,nz,endX,endZ));
      }
    }
  }
  return [];
}
const terrainGeo = new THREE.BufferGeometry();
const vertCount = GRID * GRID;
const positions = new Float32Array(vertCount * 3);
const colors = new Float32Array(vertCount * 3);
const normals = new Float32Array(vertCount * 3);
const indices = [];
for (let z = 0; z < GRID-1; z++) {
  for (let x = 0; x < GRID-1; x++) {
    const a = z*GRID+x, b=a+1, c=a+GRID, d=c+1;
    indices.push(a,b,d,a,d,c);
  }
}
for (let i = 0; i < vertCount; i++) {
  const x = (i%GRID)/GRID*SIZE - HALF;
  const z = Math.floor(i/GRID)/GRID*SIZE - HALF;
  positions[i*3] = x;
  positions[i*3+2] = z;
}
terrainGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
terrainGeo.setIndex(indices);
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.55, metalness: 0.1,
  flatShading: false, side: THREE.DoubleSide
});
const terrain = new THREE.Mesh(terrainGeo, terrainMat);
terrain.castShadow = true;
terrain.receiveShadow = true;
scene.add(terrain);
function elevationColor(h) {
  if (h < -0.5) return [0.18,0.7,0.44];
  if (h < 1.5) return [0.35,0.78,0.35];
  if (h < 3.5) return [0.6,0.72,0.25];
  if (h < 5.5) return [0.85,0.65,0.2];
  if (h < 8) return [0.82,0.5,0.2];
  return [0.9,0.85,0.8];
}
function updateTerrainHeights(hour) {
  const data = timeSeriesData[hour];
  const posAttr = terrainGeo.attributes.position;
  const colAttr = terrainGeo.attributes.color;
  const posArr = posAttr.array;
  const colArr = colAttr.array;
  const posNorm = terrainGeo.attributes.normal.array;
  for (let i = 0; i < vertCount; i++) {
    const h = data.heights[i];
    posArr[i*3+1] = h;
    const ec = elevationColor(h);
    const d = data.density[i];
    colArr[i*3] = ec[0]*0.5 + d*0.5;
    colArr[i*3+1] = ec[1]*0.6 + d*0.5;
    colArr[i*3+2] = ec[2]*0.4;
  }
  posAttr.needsUpdate = true;
  colAttr.needsUpdate = true;
  terrainGeo.computeVertexNormals();
}
const RIVER_COUNT = 6;
const riverPaths = [];
const riverLines = [];
function buildRivers(hour) {
  riverLines.forEach(l => { scene.remove(l); l.geometry.dispose(); l.material.dispose(); });
  riverLines.length = 0;
  riverPaths.length = 0;
  const data = timeSeriesData[hour];
  for (let r = 0; r < RIVER_COUNT; r++) {
    const sx = 2 + Math.floor(Math.random()*(GRID-4));
    const sz = 2 + Math.floor(Math.random()*(GRID-4));
    const ex = 2 + Math.floor(Math.random()*(GRID-4));
    const ez = 2 + Math.floor(Math.random()*(GRID-4));
    const path = aStarPath(data.errors, sx, sz, ex, ez);
    if (!path.length) continue;
    const points = [];
    for (const k of path) {
      const cx = (k%GRID)/GRID*SIZE - HALF;
      const cz = Math.floor(k/GRID)/GRID*SIZE - HALF;
      const cy = data.heights[Math.floor(k/GRID)*GRID+(k%GRID)] + 0.08;
      points.push(new THREE.Vector3(cx, cy, cz));
    }
    riverPaths.push(points);
    const curve = new THREE.CatmullRomCurve3(points);
    const tubeGeo = new THREE.TubeGeometry(curve, points.length*3, 0.08, 6, false);
    const tubeMat = new THREE.MeshStandardMaterial({color:0xe74c3c, emissive:0x661111, roughness:0.3, metalness:0.2});
    const tube = new THREE.Mesh(tubeGeo, tubeMat);
    tube.castShadow = true;
    scene.add(tube);
    riverLines.push(tube);
  }
}
const MAX_PARTICLES = 500;
const particlePool = [];
const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(MAX_PARTICLES * 3);
const particleColors = new Float32Array(MAX_PARTICLES * 3);
const particleAlive = new Uint8Array(MAX_PARTICLES);
const particleProgress = new Float32Array(MAX_PARTICLES);
const particlePaths = new Array(MAX_PARTICLES);
for (let i = 0; i < MAX_PARTICLES; i++) {
  particleAlive[i] = 0;
  particleProgress[i] = 0;
  particlePaths[i] = null;
  particlePositions[i*3] = 0;
  particlePositions[i*3+1] = -100;
  particlePositions[i*3+2] = 0;
  particleColors[i*3] = 0.2;
  particleColors[i*3+1] = 0.6;
  particleColors[i*3+2] = 1;
}
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));
const particleMat = new THREE.PointsMaterial({
  size: 0.18, vertexColors: true, blending: THREE.AdditiveBlending,
  depthWrite: false, transparent: true, opacity: 0.85
});
const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);
let particleSpawnTimer = 0;
function spawnParticle(hour) {
  if (!riverPaths.length) return;
  const rp = riverPaths[Math.floor(Math.random()*riverPaths.length)];
  if (rp.length < 2) return;
  for (let i = 0; i < MAX_PARTICLES; i++) {
    if (!particleAlive[i]) {
      particleAlive[i] = 1;
      particleProgress[i] = 0;
      particlePaths[i] = rp;
      return;
    }
  }
}
function updateParticles(dt) {
  particleSpawnTimer += dt;
  const data = timeSeriesData[currentHour];
  if (particleSpawnTimer > 0.03 && riverPaths.length) {
    particleSpawnTimer = 0;
    const spawnCount = 2 + Math.floor(Math.random()*3);
    for (let s = 0; s < spawnCount; s++) spawnParticle(currentHour);
  }
  const posArr = particleGeo.attributes.position.array;
  const colArr = particleGeo.attributes.color.array;
  for (let i = 0; i < MAX_PARTICLES; i++) {
    if (!particleAlive[i]) { posArr[i*3+1] = -100; continue; }
    particleProgress[i] += dt * (0.15 + Math.random()*0.25);
    if (particleProgress[i] >= 1 || !particlePaths[i]) {
      particleAlive[i] = 0;
      particlePaths[i] = null;
      posArr[i*3+1] = -100;
      continue;
    }
    const rp = particlePaths[i];
    const t = particleProgress[i];
    const idx = t * (rp.length-1);
    const i0 = Math.floor(idx);
    const i1 = Math.min(i0+1, rp.length-1);
    const frac = idx - i0;
    const p0 = rp[i0], p1 = rp[i1];
    const gx = p0.x + (p1.x-p0.x)*frac;
    const gy = p0.y + (p1.y-p0.y)*frac + 0.25;
    const gz = p0.z + (p1.z-p0.z)*frac;
    const ix = Math.floor((gx+HALF)/SIZE*GRID);
    const iz = Math.floor((gz+HALF)/SIZE*GRID);
    const clampedIx = Math.max(0,Math.min(GRID-1,ix));
    const clampedIz = Math.max(0,Math.min(GRID-1,iz));
    const actualH = data.heights[clampedIz*GRID+clampedIx];
    posArr[i*3] = gx;
    posArr[i*3+1] = actualH + 0.35;
    posArr[i*3+2] = gz;
    const fadeOut = 1 - t;
    colArr[i*3] = 0.3*fadeOut;
    colArr[i*3+1] = 0.7*fadeOut;
    colArr[i*3+2] = 1*fadeOut;
  }
  particleGeo.attributes.position.needsUpdate = true;
  particleGeo.attributes.color.needsUpdate = true;
}
updateTerrainHeights(12);
buildRivers(12);
const skyGeo = new THREE.SphereGeometry(80, 32, 32);
const skyMat = new THREE.ShaderMaterial({
  side: THREE.BackSide,
  uniforms: {uTime:{value:0}},
  vertexShader: `varying vec3 vPos; void main() { vPos = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
  fragmentShader: `varying vec3 vPos; uniform float uTime; void main() {
    float h = normalize(vPos).y;
    vec3 top = vec3(0.05,0.08,0.22);
    vec3 horizon = vec3(0.02,0.03,0.1);
    vec3 col = mix(horizon, top, smoothstep(-0.1,0.5,h));
    gl_FragColor = vec4(col,1.0);
  }`
});
const sky = new THREE.Mesh(skyGeo, skyMat);
scene.add(sky);
let currentHour = 12;
const slider = document.getElementById('time-slider');
const timeLabel = document.getElementById('time-label');
slider.addEventListener('input', () => {
  currentHour = parseInt(slider.value);
  timeLabel.textContent = `Hour ${currentHour}`;
  updateTerrainHeights(currentHour);
  buildRivers(currentHour);
  particleSpawnTimer = 0.1;
});
const clock = new THREE.Clock();
function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.1);
  controls.update();
  updateParticles(dt);
  sky.material.uniforms.uTime.value += dt;
  renderer.render(scene, camera);
}
animate();
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
const tooltip = document.getElementById('tooltip');
const raycaster = new THREE.Raycaster();
window.addEventListener('mousemove', (e) => {
  const mouse = new THREE.Vector2(
    (e.clientX/window.innerWidth)*2-1,
    -(e.clientY/window.innerHeight)*2+1
  );
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObject(terrain);
  if (hits.length) {
    const p = hits[0].point;
    const ix = Math.floor((p.x+HALF)/SIZE*GRID);
    const iz = Math.floor((p.z+HALF)/SIZE*GRID);
    if (ix>=0&&ix<GRID&&iz>=0&&iz<GRID) {
      const d = timeSeriesData[currentHour];
      tooltip.style.display = 'block';
      tooltip.style.left = (e.clientX+15)+'px';
      tooltip.style.top = (e.clientY-35)+'px';
      tooltip.textContent = `Revenue: ${d.heights[iz*GRID+ix].toFixed(1)} | Density: ${(d.density[iz*GRID+ix]*100).toFixed(0)}% | Errors: ${(d.errors[iz*GRID+ix]*100).toFixed(0)}%`;
      return;
    }
  }
  tooltip.style.display = 'none';
});
console.log('3D Data Terrain Explorer ready — O(rows*cols) per terrain update, A* pathfinding, in-place geometry mutation, object-pooled particles');
</script>
</body>
</html>