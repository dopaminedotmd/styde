<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
:root{--bg:#0a0a14;--panel-bg:rgba(10,10,20,0.92);--text:#c8d6e5;--accent:#4dabf7;--accent2:#ff6b6b;--border:rgba(255,255,255,0.08);--slider-track:#1a1a2e;font-size:13px}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);overflow:hidden;font-family:'Inter',system-ui,-apple-system,sans-serif;color:var(--text);height:100vh;width:100vw}
canvas{display:block}
#panel{position:fixed;top:16px;right:16px;width:280px;background:var(--panel-bg);border:1px solid var(--border);border-radius:10px;padding:14px;z-index:10;backdrop-filter:blur(12px);display:flex;flex-direction:column;gap:10px;max-height:calc(100vh - 32px);overflow-y:auto}
#panel h2{font-size:15px;font-weight:600;color:#fff;letter-spacing:0.3px}
#panel label{font-size:11px;text-transform:uppercase;letter-spacing:0.5px;opacity:0.7;margin-bottom:2px;display:block}
#panel input[type=range]{width:100%;accent-color:var(--accent);height:6px}
.time-display{font-size:22px;font-weight:700;color:var(--accent);text-align:center;font-variant-numeric:tabular-nums}
.btn-row{display:flex;gap:6px;flex-wrap:wrap}
.btn{padding:6px 10px;border:1px solid var(--border);border-radius:6px;background:rgba(255,255,255,0.04);color:var(--text);cursor:pointer;font-size:11px;transition:all 0.15s;white-space:nowrap}
.btn:hover{background:rgba(255,255,255,0.1);border-color:var(--accent)}
.btn.active{background:var(--accent);color:#000;border-color:var(--accent);font-weight:600}
.bookmark-btn{padding:4px 8px;font-size:10px}
#diagnostics{font-size:10px;opacity:0.6;font-family:'JetBrains Mono','Fira Code',monospace;line-height:1.5;border-top:1px solid var(--border);padding-top:8px;margin-top:4px}
.stat-row{display:flex;justify-content:space-between}
.stat-val{color:var(--accent)}
.stat-miss{color:var(--accent2)}
#bookmark-list{display:flex;flex-direction:column;gap:3px;max-height:120px;overflow-y:auto}
.mobile-toggle{display:none;position:fixed;top:12px;right:12px;z-index:20;width:38px;height:38px;border-radius:50%;background:var(--panel-bg);border:1px solid var(--border);color:var(--text);font-size:18px;cursor:pointer;align-items:center;justify-content:center}
.legend-row{display:flex;align-items:center;gap:6px;font-size:10px}
.legend-swatch{width:12px;height:12px;border-radius:3px;flex-shrink:0}
@media(max-width:768px){
  #panel{top:auto;bottom:0;right:0;left:0;width:100%;border-radius:14px 14px 0 0;max-height:42vh;padding:12px;gap:6px;font-size:12px}
  #panel.collapsed{max-height:48px;overflow:hidden;padding:10px 12px}
  #panel.collapsed>*:not(.mobile-collapse-bar){display:none}
  .mobile-collapse-bar{display:flex!important;justify-content:space-between;align-items:center;cursor:pointer}
  .mobile-toggle{display:flex}
  .btn-row{gap:4px}
  .btn{padding:5px 8px;font-size:10px}
  #bookmark-list{max-height:60px}
  #diagnostics{font-size:9px}
  .time-display{font-size:18px}
}
@media(min-width:769px){
  .mobile-collapse-bar{display:none!important}
  #panel.collapsed{max-height:100%!important;overflow-y:auto!important}
}
</style>
</head>
<body>
<div id="panel">
  <div class="mobile-collapse-bar" onclick="document.getElementById('panel').classList.toggle('collapsed')">
    <h2 style="margin:0">3D Data Terrain</h2><span style="font-size:14px">▼</span>
  </div>
  <h2>3D Data Terrain</h2>
  <div>
    <label>Time</label>
    <div class="time-display" id="timeLabel">12:00</div>
    <input type="range" id="timeSlider" min="0" max="23" value="12" step="1">
  </div>
  <div class="btn-row">
    <button class="btn active" onclick="setView('orbit')">Orbit</button>
    <button class="btn" onclick="setView('top')">Top</button>
    <button class="btn" onclick="setView('front')">Front</button>
    <button class="btn" id="autoRotateBtn" onclick="toggleAutoRotate()">Auto</button>
  </div>
  <div style="display:flex;gap:6px;align-items:center">
    <input type="text" id="bookmarkName" placeholder="Bookmark name" style="flex:1;padding:5px 8px;border:1px solid var(--border);border-radius:6px;background:rgba(255,255,255,0.04);color:var(--text);font-size:11px" maxlength="20">
    <button class="btn" onclick="saveBookmark()">Save</button>
  </div>
  <div id="bookmark-list"></div>
  <div style="display:flex;flex-direction:column;gap:2px">
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to top,#1a3a1a,#4a9,#cf6)"></span> Revenue (elevation)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to top,#1a1a3a,#44f,#f4a)"></span> User density (color)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#ff4444"></span> Error rivers</div>
  </div>
  <div id="diagnostics"></div>
</div>
<script type="importmap">
{"imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"
}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 120;
const TIME_STEPS = 24;
const TERRAIN_SIZE = 20;
const cacheStats = { terrainHits:0, terrainMisses:0, riverHits:0, riverMisses:0, colorHits:0, colorMisses:0, particleHits:0, particleMisses:0 };
const terrainCache = new Map();
const riverCache = new Map();
const colorCache = new Map();
const particleDataCache = new Map();
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 30, 80);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.5, 120);
camera.position.set(16, 10, 18);
camera.lookAt(0, 1, 0);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.1;
document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 5;
controls.maxDistance = 45;
controls.maxPolarAngle = Math.PI * 0.62;
controls.target.set(0, 2, 0);
controls.update();
const ambientLight = new THREE.AmbientLight(0x334466, 1.5);
scene.add(ambientLight);
const sunLight = new THREE.DirectionalLight(0xffeedd, 4.5);
sunLight.position.set(15, 25, 10);
sunLight.castShadow = true;
sunLight.shadow.mapSize.set(2048, 2048);
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 80;
sunLight.shadow.camera.left = -20;
sunLight.shadow.camera.right = 20;
sunLight.shadow.camera.top = 20;
sunLight.shadow.camera.bottom = -20;
sunLight.shadow.bias = -0.0004;
scene.add(sunLight);
const fillLight = new THREE.DirectionalLight(0x8899cc, 1.2);
fillLight.position.set(-8, 3, -6);
scene.add(fillLight);
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SIZE/2, 40, 30, 64, 0x334466, 0x223355);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
let terrainMesh, riverLine, particleSystem;
const bookmarks = new Map();
function simplex3D(x, y, z) {
  const floor = Math.floor;
  const X = floor(x) & 255, Y = floor(y) & 255, Z = floor(z) & 255;
  x -= floor(x); y -= floor(y); z -= floor(z);
  const u = x*x*x*(x*(x*6-15)+10), v = y*y*y*(y*(y*6-15)+10), w = z*z*z*(z*(z*6-15)+10);
  const p = perm, A = p[X]+Y, AA = p[A]+Z, AB = p[A+1]+Z;
  const B = p[X+1]+Y, BA = p[B]+Z, BB = p[B+1]+Z;
  const grad = (h, x, y, z) => { const b = h&15; const u2 = b<8?x:y, v2 = b<4?y:b===12||b===14?x:z; return ((b&1)?-u2:u2)+((b&2)?-v2:v2); };
  return (1-0.936)*(grad(p[AA],x,y,z)*(1-u)*(1-v)*(1-w)+grad(p[BA],x-1,y,z)*u*(1-v)*(1-w)+grad(p[AB],x,y-1,z)*(1-u)*v*(1-w)+grad(p[BB],x-1,y-1,z)*u*v*(1-w)+grad(p[AA+1],x,y,z-1)*(1-u)*(1-v)*w+grad(p[BA+1],x-1,y,z-1)*u*(1-v)*w+grad(p[AB+1],x,y-1,z-1)*(1-u)*v*w+grad(p[BB+1],x-1,y-1,z-1)*u*v*w);
}
const perm = new Uint8Array(512);
(()=>{const s=[151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180];for(let i=0;i<256;i++)perm[i]=perm[i+256]=s[i];})();
function noise2D(x, y, t) { return simplex3D(x*0.08, y*0.08, t*0.15); }
function noiseDetail(x, y, t) {
  let v = 0, amp = 1, freq = 1, tot = 0;
  for (let o = 0; o < 3; o++) { v += amp * simplex3D(x*0.06*freq, y*0.06*freq, t*0.12*freq); tot += amp; amp *= 0.5; freq *= 2.2; }
  return v / tot;
}
function buildTerrainGeometry(t) {
  if (terrainCache.has(t)) { cacheStats.terrainHits++; return terrainCache.get(t); }
  cacheStats.terrainMisses++;
  const geo = new THREE.PlaneGeometry(TERRAIN_SIZE, TERRAIN_SIZE, GRID-1, GRID-1);
  geo.rotateX(-Math.PI/2);
  const pos = geo.attributes.position.array;
  const colors = new Float32Array(pos.length);
  const hf = new Float32Array((GRID)*(GRID));
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const x = (i/(GRID-1)-0.5)*TERRAIN_SIZE;
      const z = (j/(GRID-1)-0.5)*TERRAIN_SIZE;
      const idx = (i*GRID+j);
      const baseH = noiseDetail(x, z, t);
      const ridge = 1 - Math.abs(noise2D(x*1.7, z*1.7, t+3));
      const h = baseH*4 + ridge*2.5 + 0.8;
      const idx3 = idx*3;
      pos[idx3+1] = h;
      hf[idx] = h;
    }
  }
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.7,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide
  });
  const result = { geometry: geo, material: mat, heightfield: hf };
  terrainCache.set(t, result);
  return result;
}
function computeVertexColors(geo, heightfield, t) {
  const key = `${t}`;
  if (colorCache.has(key)) { cacheStats.colorHits++; return colorCache.get(key); }
  cacheStats.colorMisses++;
  const colors = geo.attributes.color.array;
  const pos = geo.attributes.position.array;
  for (let i = 0; i < GRID; i++) {
    for (let j = 0; j < GRID; j++) {
      const idx = i*GRID+j;
      const x = (i/(GRID-1)-0.5)*TERRAIN_SIZE;
      const z = (j/(GRID-1)-0.5)*TERRAIN_SIZE;
      const h = heightfield[idx];
      const density = noiseDetail(x*0.7, z*0.7, t+7) * 0.5 + 0.5;
      const idx3 = idx*3;
      if (h < 0.6) {
        colors[idx3] = 0.06 + density*0.06;
        colors[idx3+1] = 0.15 + density*0.12;
        colors[idx3+2] = 0.28 + density*0.2;
      } else if (h < 1.8) {
        const f = (h-0.6)/1.2;
        colors[idx3] = 0.08 + f*0.08 + density*0.06;
        colors[idx3+1] = 0.28 + f*0.35 + density*0.08;
        colors[idx3+2] = 0.18 + f*0.05 + density*0.04;
      } else if (h < 3.5) {
        const f = (h-1.8)/1.7;
        colors[idx3] = 0.2 + f*0.35 + density*0.04;
        colors[idx3+1] = 0.55 + f*0.2 - density*0.05;
        colors[idx3+2] = 0.1 + f*0.05;
      } else {
        colors[idx3] = 0.65 + density*0.15;
        colors[idx3+1] = 0.7 + density*0.1;
        colors[idx3+2] = 0.4 + density*0.1;
      }
    }
  }
  geo.attributes.color.needsUpdate = true;
  colorCache.set(key, true);
  return true;
}
function buildRiverGeometry(t, heightfield) {
  if (riverCache.has(t)) { cacheStats.riverHits++; return riverCache.get(t); }
  cacheStats.riverMisses++;
  const paths = [];
  const visited = new Uint8Array(GRID*GRID);
  for (let seed = 0; seed < 12; seed++) {
    const sx = 10 + (seed*23)%(GRID-20);
    const sz = 10 + (seed*37)%(GRID-20);
    const sh = heightfield[sx*GRID+sz];
    if (sh < 2.5) continue;
    const pts = [];
    let cx = sx, cz = sz;
    let stuck = 0;
    while (stuck < 60 && cx > 1 && cx < GRID-2 && cz > 1 && cz < GRID-2) {
      const ci = cx*GRID+cz;
      if (visited[ci] && pts.length < 3) break;
      visited[ci] = 1;
      const h = heightfield[ci];
      let bestD = 999, bx = cx, bz = cz;
      for (let di = -1; di <= 1; di++) {
        for (let dj = -1; dj <= 1; dj++) {
          if (di === 0 && dj === 0) continue;
          const ni = cx+di, nj = cz+dj;
          if (ni < 0 || ni >= GRID || nj < 0 || nj >= GRID) continue;
          const nh = heightfield[ni*GRID+nj];
          const d = h - nh;
          if (d > 0 && d < bestD) { bestD = d; bx = ni; bz = nj; }
        }
      }
      if (bestD > 0 && bestD < 999 && bestD < 0.15) { cx = bx; cz = bz; }
      else { stuck++; }
      if (pts.length === 0 || Math.abs(cx-pts[pts.length-1][0])>0.5 || Math.abs(cz-pts[pts.length-1][1])>0.5) {
        const wx = (cx/(GRID-1)-0.5)*TERRAIN_SIZE;
        const wz = (cz/(GRID-1)-0.5)*TERRAIN_SIZE;
        pts.push([wx, heightfield[ci]+0.08, wz]);
      }
    }
    if (pts.length >= 8) paths.push(pts);
  }
  const group = new THREE.Group();
  const riverMat = new THREE.MeshBasicMaterial({color:0xff3333,transparent:true,opacity:0.7});
  for (const pts of paths) {
    const curve = new THREE.CatmullRomCurve3(pts.map(p=>new THREE.Vector3(p[0],p[1],p[2])));
    const tubeGeo = new THREE.TubeGeometry(curve, pts.length*2, 0.08, 6, false);
    const mesh = new THREE.Mesh(tubeGeo, riverMat.clone());
    group.add(mesh);
  }
  riverCache.set(t, group);
  return group;
}
let riverDebounceTimer = null;
function rebuildRiverWithDebounce(t, heightfield) {
  if (riverDebounceTimer) clearTimeout(riverDebounceTimer);
  riverDebounceTimer = setTimeout(() => {
    if (riverLine) scene.remove(riverLine);
    riverLine = buildRiverGeometry(t, heightfield);
    scene.add(riverLine);
  }, 200);
}
function buildParticleData(t, heightfield) {
  if (particleDataCache.has(t)) { cacheStats.particleHits++; return particleDataCache.get(t); }
  cacheStats.particleMisses++;
  const count = 800;
  const positions = new Float32Array(count*3);
  const velocities = new Float32Array(count);
  const pathIndices = new Uint16Array(count);
  for (let i = 0; i < count; i++) {
    const gx = 10 + Math.floor(Math.random()*(GRID-20));
    const gz = 10 + Math.floor(Math.random()*(GRID-20));
    const h = heightfield[gx*GRID+gz];
    positions[i*3] = (gx/(GRID-1)-0.5)*TERRAIN_SIZE;
    positions[i*3+1] = h + 0.3 + Math.random()*1.5;
    positions[i*3+2] = (gz/(GRID-1)-0.5)*TERRAIN_SIZE;
    velocities[i] = 0.02 + Math.random()*0.06;
    pathIndices[i] = 0;
  }
  const data = { positions, velocities, pathIndices };
  particleDataCache.set(t, data);
  return data;
}
function createOrUpdateParticles(t, heightfield) {
  const data = buildParticleData(t, heightfield);
  if (!particleSystem) {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(data.positions, 3));
    const mat = new THREE.PointsMaterial({
      color: 0x66ccff,
      size: 0.12,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      transparent: true,
      opacity: 0.8
    });
    particleSystem = new THREE.Points(geo, mat);
    particleSystem.userData = { particleData: data, currentTime: t };
    scene.add(particleSystem);
  } else {
    const posAttr = particleSystem.geometry.attributes.position;
    posAttr.array.set(data.positions);
    posAttr.needsUpdate = true;
    particleSystem.userData.particleData = data;
    particleSystem.userData.currentTime = t;
  }
}
function updateParticles(heightfield) {
  if (!particleSystem) return;
  const data = particleSystem.userData.particleData;
  const pos = particleSystem.geometry.attributes.position.array;
  const vel = data.velocities;
  for (let i = 0; i < vel.length; i++) {
    const i3 = i*3;
    const wx = pos[i3], wz = pos[i3+2];
    const gx = Math.round((wx/TERRAIN_SIZE+0.5)*(GRID-1));
    const gz = Math.round((wz/TERRAIN_SIZE+0.5)*(GRID-1));
    const gi = Math.max(0, Math.min(GRID-1, gx))*GRID + Math.max(0, Math.min(GRID-1, gz));
    const terrainY = heightfield[gi];
    let bestD = 999, bx = 0, bz = 0;
    const cgx = Math.max(1, Math.min(GRID-2, gx));
    const cgz = Math.max(1, Math.min(GRID-2, gz));
    for (let di = -1; di <= 1; di++) {
      for (let dj = -1; dj <= 1; dj++) {
        const ni = cgx+di, nj = cgz+dj;
        const nh = heightfield[ni*GRID+nj];
        const d = heightfield[cgx*GRID+cgz] - nh;
        if (d > 0.001 && d < bestD) { bestD = d; bx = (ni/(GRID-1)-0.5)*TERRAIN_SIZE; bz = (nj/(GRID-1)-0.5)*TERRAIN_SIZE; }
      }
    }
    if (bestD < 999) {
      const dx = bx - wx, dz = bz - wz;
      const dist = Math.sqrt(dx*dx+dz*dz) || 1;
      pos[i3] += (dx/dist)*vel[i];
      pos[i3+2] += (dz/dist)*vel[i];
      pos[i3+1] = heightfield[Math.max(0,Math.min(GRID-1,Math.round((pos[i3]/TERRAIN_SIZE+0.5)*(GRID-1))))*GRID+Math.max(0,Math.min(GRID-1,Math.round((pos[i3+2]/TERRAIN_SIZE+0.5)*(GRID-1))))]+0.25;
    }
    if (pos[i3] < -TERRAIN_SIZE/2 || pos[i3] > TERRAIN_SIZE/2 || pos[i3+2] < -TERRAIN_SIZE/2 || pos[i3+2] > TERRAIN_SIZE/2) {
      const rgx = 15 + Math.floor(Math.random()*90);
      const rgz = 15 + Math.floor(Math.random()*90);
      const rh = heightfield[rgx*GRID+rgz];
      pos[i3] = (rgx/(GRID-1)-0.5)*TERRAIN_SIZE;
      pos[i3+1] = rh + 0.3 + Math.random()*1.5;
      pos[i3+2] = (rgz/(GRID-1)-0.5)*TERRAIN_SIZE;
    }
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
let activeView = 'orbit';
let currentTime = 12;
let terrainData = null;
let autoRotate = false;
function setTerrain(t) {
  currentTime = t;
  const result = buildTerrainGeometry(t);
  computeVertexColors(result.geometry, result.heightfield, t);
  terrainData = result;
  if (terrainMesh) scene.remove(terrainMesh);
  terrainMesh = new THREE.Mesh(result.geometry, result.material);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  if (riverLine) scene.remove(riverLine);
  riverLine = buildRiverGeometry(t, result.heightfield);
  scene.add(riverLine);
  createOrUpdateParticles(t, result.heightfield);
  document.getElementById('timeSlider').value = t;
  const h = String(Math.floor(t)).padStart(2,'0');
  document.getElementById('timeLabel').textContent = h+':00';
  updateDiagnostics();
}
function updateDiagnostics() {
  const totalT = cacheStats.terrainHits+cacheStats.terrainMisses;
  const totalR = cacheStats.riverHits+cacheStats.riverMisses;
  const totalC = cacheStats.colorHits+cacheStats.colorMisses;
  const totalP = cacheStats.particleHits+cacheStats.particleMisses;
  const tr = totalT?Math.round(cacheStats.terrainHits/totalT*100):0;
  const rr = totalR?Math.round(cacheStats.riverHits/totalR*100):0;
  const cr = totalC?Math.round(cacheStats.colorHits/totalC*100):0;
  const pr = totalP?Math.round(cacheStats.particleHits/totalP*100):0;
  document.getElementById('diagnostics').innerHTML =
    `<div class="stat-row"><span>Terrain cache</span><span class="stat-val">${tr}%</span></div>`+
    `<div class="stat-row"><span>River cache</span><span class="stat-val">${rr}%</span></div>`+
    `<div class="stat-row"><span>Color cache</span><span class="stat-val">${cr}%</span></div>`+
    `<div class="stat-row"><span>Particle cache</span><span class="stat-val">${pr}%</span></div>`+
    `<div class="stat-row"><span>FPS</span><span>${Math.round(fpsAvg)}</span></div>`;
}
function setView(view) {
  activeView = view;
  document.querySelectorAll('.btn-row .btn').forEach(b=>b.classList.remove('active'));
  const targetMap = {orbit:0,top:1,front:2};
  document.querySelectorAll('.btn-row .btn')[targetMap[view]]?.classList.add('active');
  const target = new THREE.Vector3(0, 2, 0);
  if (view === 'top') {
    animateCamera(new THREE.Vector3(0, 22, 0.5), target);
  } else if (view === 'front') {
    animateCamera(new THREE.Vector3(0, 3, 18), target);
  } else {
    animateCamera(new THREE.Vector3(16, 10, 18), target);
  }
}
function animateCamera(toPos, toTarget) {
  const startPos = camera.position.clone();
  const startTarget = controls.target.clone();
  const startTime = performance.now();
  const duration = 800;
  function step(now) {
    const elapsed = now - startTime;
    const t = Math.min(elapsed/duration, 1);
    const ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
    camera.position.lerpVectors(startPos, toPos, ease);
    controls.target.lerpVectors(startTarget, toTarget, ease);
    controls.update();
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
function toggleAutoRotate() {
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  controls.autoRotateSpeed = 0.6;
  document.getElementById('autoRotateBtn').classList.toggle('active', autoRotate);
}
function saveBookmark() {
  const nameInput = document.getElementById('bookmarkName');
  const name = nameInput.value.trim() || `View ${bookmarks.size+1}`;
  const bm = {
    pos: camera.position.toArray(),
    target: controls.target.toArray(),
    time: currentTime
  };
  bookmarks.set(name, bm);
  nameInput.value = '';
  renderBookmarks();
}
function loadBookmark(name) {
  const bm = bookmarks.get(name);
  if (!bm) return;
  if (bm.time !== currentTime) setTerrain(bm.time);
  animateCamera(new THREE.Vector3(...bm.pos), new THREE.Vector3(...bm.target));
}
function deleteBookmark(name) {
  bookmarks.delete(name);
  renderBookmarks();
}
function renderBookmarks() {
  const list = document.getElementById('bookmark-list');
  if (bookmarks.size === 0) { list.innerHTML = '<span style="font-size:10px;opacity:0.5">No bookmarks saved</span>'; return; }
  list.innerHTML = '';
  for (const [name, bm] of bookmarks) {
    const row = document.createElement('div');
    row.style.cssText = 'display:flex;justify-content:space-between;align-items:center;gap:4px;padding:3px 0;font-size:10px';
    row.innerHTML = `<span style="cursor:pointer;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="Load bookmark">${name} (${bm.time}:00)</span>
      <button class="btn bookmark-btn" style="padding:2px 6px;font-size:9px;flex-shrink:0" data-del="${name}">✕</button>`;
    row.querySelector('span').onclick = ()=>loadBookmark(name);
    row.querySelector('button').onclick = (e)=>{e.stopPropagation();deleteBookmark(name);};
    list.appendChild(row);
  }
}
document.getElementById('timeSlider').addEventListener('input', (e) => {
  const t = parseInt(e.target.value);
  if (t !== currentTime) setTerrain(t);
});
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
let fpsFrames = 0, fpsAvg = 60, fpsLast = performance.now();
function animate(now) {
  requestAnimationFrame(animate);
  if (terrainData && particleSystem) {
    updateParticles(terrainData.heightfield);
  }
  controls.update();
  fpsFrames++;
  if (now - fpsLast >= 1000) {
    fpsAvg = Math.round(fpsFrames/((now-fpsLast)/1000));
    fpsFrames = 0;
    fpsLast = now;
    updateDiagnostics();
  }
  renderer.render(scene, camera);
}
setTerrain(12);
renderBookmarks();
requestAnimationFrame(animate);
window.setView = setView;
window.toggleAutoRotate = toggleAutoRotate;
window.saveBookmark = saveBookmark;
</script>
</body>
</html>