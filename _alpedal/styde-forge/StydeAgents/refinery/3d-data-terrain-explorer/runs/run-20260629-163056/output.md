<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a0f;--panel-bg:rgba(10,10,20,0.92);--text:#c8d6e5;--accent:#48dbfb;--accent2:#ff6b6b;--accent3:#51cf66;--border:rgba(255,255,255,0.08);--radius:8px;font-family:'Segoe UI',system-ui,sans-serif}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;height:100vh;width:100vw;color:var(--text)}
  #canvas-container{position:fixed;inset:0;z-index:0}
  canvas{display:block}
  #ui-layer{position:fixed;inset:0;z-index:10;pointer-events:none}
  #ui-layer>*{pointer-events:auto}
  #time-panel{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);background:var(--panel-bg);border:1px solid var(--border);border-radius:var(--radius);padding:12px 20px;display:flex;align-items:center;gap:14px;backdrop-filter:blur(12px)}
  #time-slider{width:280px;accent-color:var(--accent);cursor:pointer}
  #time-label{font-size:13px;font-weight:600;min-width:90px;text-align:center;color:var(--accent)}
  #time-value{font-size:11px;color:#8899aa;min-width:60px}
  #top-bar{position:absolute;top:16px;left:16px;right:16px;display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
  .panel{background:var(--panel-bg);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px;backdrop-filter:blur(12px);font-size:12px}
  #metrics-panel{min-width:200px}
  #metrics-panel h3{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#8899aa;margin-bottom:8px}
  .metric-row{display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid var(--border)}
  .metric-val{font-weight:700;font-variant-numeric:tabular-nums}
  #cache-panel{min-width:220px}
  #cache-panel h3{font-size:11px;text-transform:uppercase;letter-spacing:1.5px;color:#8899aa;margin-bottom:8px}
  .cache-row{display:flex;justify-content:space-between;padding:3px 0;font-variant-numeric:tabular-nums}
  .cache-hit{color:var(--accent3)}
  .cache-miss{color:var(--accent2)}
  .cache-rate{font-weight:700}
  #bookmark-panel{position:absolute;top:16px;right:16px;display:flex;gap:6px;flex-wrap:wrap;max-width:340px;justify-content:flex-end}
  .bookmark-btn{background:var(--panel-bg);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:4px;cursor:pointer;font-size:11px;transition:all 0.2s;white-space:nowrap}
  .bookmark-btn:hover{border-color:var(--accent);color:var(--accent)}
  .bookmark-btn.saved{background:rgba(72,219,251,0.12);border-color:var(--accent)}
  #legend{position:absolute;bottom:100px;right:20px;background:var(--panel-bg);border:1px solid var(--border);border-radius:var(--radius);padding:12px 16px;backdrop-filter:blur(12px);font-size:11px}
  .legend-item{display:flex;align-items:center;gap:8px;padding:3px 0}
  .legend-swatch{width:14px;height:14px;border-radius:3px;flex-shrink:0}
  #auto-rotate-btn{position:absolute;bottom:100px;left:20px;background:var(--panel-bg);border:1px solid var(--border);color:var(--text);padding:8px 16px;border-radius:var(--radius);cursor:pointer;font-size:12px;transition:all 0.2s}
  #auto-rotate-btn.active{border-color:var(--accent);color:var(--accent);background:rgba(72,219,251,0.1)}
  #tooltip{position:absolute;padding:8px 12px;background:var(--panel-bg);border:1px solid var(--accent);border-radius:4px;font-size:11px;display:none;pointer-events:none;z-index:100}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-layer">
  <div id="top-bar">
    <div id="metrics-panel" class="panel">
      <h3>Terrain Metrics</h3>
      <div class="metric-row"><span>Revenue (max)</span><span class="metric-val" id="m-rev" style="color:var(--accent3)">--</span></div>
      <div class="metric-row"><span>User Density</span><span class="metric-val" id="m-users" style="color:#a29bfe">--</span></div>
      <div class="metric-row"><span>Error Rate</span><span class="metric-val" id="m-err" style="color:var(--accent2)">--</span></div>
      <div class="metric-row"><span>API Calls/s</span><span class="metric-val" id="m-api" style="color:var(--accent)">--</span></div>
      <div class="metric-row"><span>Time Step</span><span class="metric-val" id="m-step">0/0</span></div>
    </div>
    <div id="cache-panel" class="panel">
      <h3>Cache Diagnostics</h3>
      <div class="cache-row"><span>Terrain Hits</span><span class="cache-hit" id="c-terrain-hit">0</span></div>
      <div class="cache-row"><span>Terrain Misses</span><span class="cache-miss" id="c-terrain-miss">0</span></div>
      <div class="cache-row"><span>River Hits</span><span class="cache-hit" id="c-river-hit">0</span></div>
      <div class="cache-row"><span>River Misses</span><span class="cache-miss" id="c-river-miss">0</span></div>
      <div class="cache-row"><span>Grid Transform</span><span class="cache-hit" id="c-grid-hit">0</span></div>
      <div class="cache-row"><span>Cache Rate</span><span class="cache-rate" id="c-rate">0%</span></div>
    </div>
  </div>
  <div id="bookmark-panel">
    <button class="bookmark-btn" data-idx="0">Overview</button>
    <button class="bookmark-btn" data-idx="1">Revenue Peak</button>
    <button class="bookmark-btn" data-idx="2">Error River</button>
    <button class="bookmark-btn saved" data-idx="3" id="bm-save">Save View</button>
  </div>
  <div id="time-panel">
    <button id="time-play" style="background:none;border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:4px;cursor:pointer;font-size:12px">Play</button>
    <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
    <span id="time-label">Step 0</span>
    <span id="time-value">0:00</span>
  </div>
  <button id="auto-rotate-btn">Auto-Rotate: Off</button>
  <div id="legend">
    <div class="legend-item"><span class="legend-swatch" style="background:linear-gradient(to top,#2d5016,#51cf66,#f0f0a0)"></span> Revenue (elevation)</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#a29bfe"></span> User density (vertex color)</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#ff6b6b"></span> Error rivers</div>
    <div class="legend-item"><span class="legend-swatch" style="background:#48dbfb"></span> API particle trails</div>
  </div>
  <div id="tooltip"></div>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ── Constants ────────────────────────────────────────────────────
const GRID = 80;
const SIZE = 20;
const TIME_STEPS = 30;
const PARTICLE_COUNT = 200;
// ── Cache stores ─────────────────────────────────────────────────
// All caches are populated once and reused; no geometry constructor in hot paths
const terrainCache = new Map();       // timeStep -> {geometry, heightData}
const riverCache = new Map();         // timeStep -> TubeGeometry (or Line geometry)
const noiseGridCache = new Map();     // seed -> Float32Array[GRID*GRID]
const gridTransformCache = new Map(); // "x,z" -> {gx,gz,h} — cleared per frame
// Cache hit/miss counters for diagnostic panel
const cacheStats = {terrainHit:0,terrainMiss:0,riverHit:0,riverMiss:0,gridHit:0,gridMiss:0};
// ── Scene setup ──────────────────────────────────────────────────
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0f);
scene.fog = new THREE.Fog(0x0a0a0f, 18, 55);
const camera = new THREE.PerspectiveCamera(50, container.clientWidth/container.clientHeight, 0.5, 100);
camera.position.set(16, 10, 18);
camera.lookAt(0, 0, 0);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);
// ── OrbitControls with damping ────────────────────────────────────
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.4;
controls.target.set(0, 1.5, 0);
controls.maxPolarAngle = Math.PI * 0.55;
controls.minDistance = 5;
controls.maxDistance = 45;
controls.update();
// ── Lighting ──────────────────────────────────────────────────────
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sun = new THREE.DirectionalLight(0xffeedd, 2.5);
sun.position.set(15, 20, 10);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 60;
sun.shadow.camera.left = -20;
sun.shadow.camera.right = 20;
sun.shadow.camera.top = 20;
sun.shadow.camera.bottom = -20;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 0.8);
fill.position.set(-8, 3, -6);
scene.add(fill);
// ── Grid helper ───────────────────────────────────────────────────
const gridHelper = new THREE.GridHelper(SIZE, 40, 0x222244, 0x111122);
gridHelper.position.y = -0.05;
scene.add(gridHelper);
// ── Scene objects (replaced on time step change) ──────────────────
let terrainMesh = null;
let riverLine = null;
let particleSystem = null;
let currentTimeStep = 0;
// ── Camera bookmarks ──────────────────────────────────────────────
const bookmarks = [
  {pos:[16,10,18],target:[0,1.5,0]},      // Overview
  {pos:[6,6,8],target:[-2,2.5,-1]},       // Revenue Peak
  {pos:[10,4,-10],target:[3,1.2,2]},      // Error River
];
// ── Simplex-like noise (deterministic, seedable) ──────────────────
function seededNoise(seed){
  // Return cached noise grid if available — avoids recomputation across time steps
  if(noiseGridCache.has(seed)){return noiseGridCache.get(seed);}
  const data = new Float32Array(GRID*GRID);
  // Simple multi-octave value noise with seed mixing
  const hash = (x,z,s)=>{
    let n = Math.sin(x*12.9898 + z*78.233 + s*437.58)*43758.5453;
    return n - Math.floor(n);
  };
  const smooth = t=>t*t*(3-2*t);
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      let val=0, amp=1, freq=1, max=0;
      // 4 octaves of noise for natural terrain
      for(let o=0;o<4;o++){
        const sx=ix*freq/GRID, sz=iz*freq/GRID;
        const fx=sx-Math.floor(sx), fz=sz-Math.floor(sz);
        const ix0=Math.floor(sx)%GRID, iz0=Math.floor(sz)%GRID;
        const ix1=(ix0+1)%GRID, iz1=(iz0+1)%GRID;
        const sfx=smooth(fx), sfz=smooth(fz);
        const v00=hash(ix0,iz0,seed+o*100),v10=hash(ix1,iz0,seed+o*100);
        const v01=hash(ix0,iz1,seed+o*100),v11=hash(ix1,iz1,seed+o*100);
        const a=v00+(v10-v00)*sfx, b=v01+(v11-v01)*sfx;
        val+=(a+(b-a)*sfz)*amp;
        max+=amp;
        amp*=0.5; freq*=2;
      }
      data[iz*GRID+ix]=val/max; // normalize to [0,1]
    }
  }
  noiseGridCache.set(seed, data);
  return data;
}
// ── Data generation: time-series metrics ──────────────────────────
// Each time step has: revenue (height), userDensity (vertex color), errors (river path)
function generateTimeSeriesData(step){
  const t = step / (TIME_STEPS-1); // normalized 0..1
  const heightData = new Float32Array(GRID*GRID);
  const densityData = new Float32Array(GRID*GRID);
  const baseNoise = seededNoise(0);
  const trendNoise = seededNoise(1000 + step);
  const densityNoise = seededNoise(2000 + step);
  // Central revenue peak that grows over time, with noise variation
  const peakX = 0.35 + Math.sin(t*Math.PI*2)*0.12;
  const peakZ = 0.4 + Math.cos(t*Math.PI*1.7)*0.1;
  let maxRev = 0;
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      const nx = ix/GRID, nz = iz/GRID;
      // Distance from moving peak creates revenue mountain
      const dist = Math.sqrt((nx-peakX)**2 + (nz-peakZ)**2);
      const peakInfluence = Math.exp(-dist*3.5) * (0.7 + 0.3*t);
      const noiseVal = baseNoise[iz*GRID+ix]*0.3 + trendNoise[iz*GRID+ix]*0.5;
      const height = peakInfluence*1.8 + noiseVal*0.7 + Math.sin(nx*3+t*2)*0.15;
      heightData[iz*GRID+ix] = Math.max(0, height);
      if(height>maxRev) maxRev=height;
      // User density: grows around peak, secondary cluster in corner
      const dist2 = Math.sqrt((nx-0.7)**2+(nz-0.75)**2);
      densityData[iz*GRID+ix] = Math.exp(-dist*2.8)*0.9 + Math.exp(-dist2*4)*0.5*(0.5+0.5*t);
    }
  }
  // Error river path: flows from high-error zone to low area
  const riverPoints = [];
  // Start point drifts along a ridge
  const sx = 0.2 + Math.sin(t*Math.PI*1.3)*0.25;
  const sz = 0.15 + Math.cos(t*Math.PI*1.1)*0.2;
  let cx = sx, cz = sz;
  // Simple flow-following path: step downhill
  for(let i=0;i<60;i++){
    const gx = Math.floor(cx*GRID);
    const gz = Math.floor(cz*GRID);
    if(gx<0||gx>=GRID||gz<0||gz>=GRID) break;
    const h = heightData[gz*GRID+gx];
    riverPoints.push({x:(cx-0.5)*SIZE, z:(cz-0.5)*SIZE, h:h+0.15});
    // Flow toward steepest descent with some meander
    let bestDz=0, bestDx=0, lowest=Infinity;
    for(let dz=-1;dz<=1;dz++){
      for(let dx=-1;dx<=1;dx++){
        const ngx=gx+dx, ngz=gz+dz;
        if(ngx<0||ngx>=GRID||ngz<0||ngz>=GRID) continue;
        const nh = heightData[ngz*GRID+ngx];
        if(nh<lowest){lowest=nh;bestDx=dx;bestDz=dz;}
      }
    }
    cx += bestDx*0.018 + (Math.sin(i*0.4+t*5)*0.004);
    cz += bestDz*0.018 + (Math.cos(i*0.35+t*4)*0.004);
  }
  // Error rate: proportional to river path density
  const errorRate = riverPoints.length * 0.01 * (0.8 + 0.4*Math.sin(t*Math.PI*3));
  // API call rate (for particles)
  const apiRate = 80 + 40*Math.sin(t*Math.PI*2) + 20*Math.cos(t*Math.PI*3.5);
  return {heightData, densityData, riverPoints, maxRev, errorRate, apiRate,
          userDensity: densityData.reduce((a,b)=>a+b,0)/(GRID*GRID)};
}
// ── Build terrain geometry (cached) ──────────────────────────────
function buildTerrainGeometry(timeStep){
  // Cache check: return pre-built geometry if available
  if(terrainCache.has(timeStep)){
    cacheStats.terrainHit++;
    updateCacheUI();
    return terrainCache.get(timeStep);
  }
  cacheStats.terrainMiss++;
  updateCacheUI();
  const {heightData, densityData} = generateTimeSeriesData(timeStep);
  const geo = new THREE.BufferGeometry();
  const vertices = new Float32Array(GRID*GRID*3);
  const colors = new Float32Array(GRID*GRID*3);
  const indices = [];
  // Build vertex positions and colors in one pass
  const half = SIZE/2;
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      const idx = iz*GRID+ix;
      const h = heightData[idx];
      const d = densityData[idx];
      vertices[idx*3]   = (ix/(GRID-1)-0.5)*SIZE;
      vertices[idx*3+1] = h * 6; // scale height
      vertices[idx*3+2] = (iz/(GRID-1)-0.5)*SIZE;
      // Color: revenue-green gradient mixed with density-purple overlay
      const r = 0.15 + d*0.4;
      const g = 0.25 + h*0.5 + d*0.15;
      const b = 0.3 + d*0.5;
      colors[idx*3]=r; colors[idx*3+1]=g; colors[idx*3+2]=b;
    }
  }
  // Index buffer: triangle strips
  for(let iz=0;iz<GRID-1;iz++){
    for(let ix=0;ix<GRID-1;ix++){
      const a=iz*GRID+ix, b=a+1, c=a+GRID, d=c+1;
      indices.push(a,b,c, b,d,c);
    }
  }
  geo.setAttribute('position', new THREE.BufferAttribute(vertices,3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors,3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  const result = {geometry:geo, heightData};
  terrainCache.set(timeStep, result);
  return result;
}
// ── Build river geometry (cached) ─────────────────────────────────
function buildRiverGeometry(timeStep){
  if(riverCache.has(timeStep)){
    cacheStats.riverHit++;
    updateCacheUI();
    return riverCache.get(timeStep);
  }
  cacheStats.riverMiss++;
  updateCacheUI();
  const {riverPoints} = generateTimeSeriesData(timeStep);
  if(riverPoints.length<2){
    const empty = new THREE.BufferGeometry();
    riverCache.set(timeStep, empty);
    return empty;
  }
  const pts = riverPoints.map(p=>new THREE.Vector3(p.x, p.h*6+0.2, p.z));
  const curve = new THREE.CatmullRomCurve3(pts);
  const tubeGeo = new THREE.TubeGeometry(curve, 80, 0.12, 8, false);
  riverCache.set(timeStep, tubeGeo);
  return tubeGeo;
}
// ── Build particle system (reuses geometry, only updates positions) ──
function buildParticleSystem(){
  const geo = new THREE.BufferGeometry();
  const positions = new Float32Array(PARTICLE_COUNT*3);
  // Initialize random positions across terrain
  for(let i=0;i<PARTICLE_COUNT;i++){
    positions[i*3] = (Math.random()-0.5)*SIZE*0.9;
    positions[i*3+1] = Math.random()*5+1;
    positions[i*3+2] = (Math.random()-0.5)*SIZE*0.9;
  }
  geo.setAttribute('position', new THREE.BufferAttribute(positions,3));
  const mat = new THREE.PointsMaterial({
    size:0.08, color:0x48dbfb, blending:THREE.AdditiveBlending,
    depthWrite:false, transparent:true, opacity:0.8
  });
  const pts = new THREE.Points(geo, mat);
  // Store reference for hot-path position reuse — no allocation in update loop
  pts.userData.positions = positions;
  // Per-particle state: random seed offsets for organic movement
  pts.userData.seeds = new Float32Array(PARTICLE_COUNT*2);
  for(let i=0;i<PARTICLE_COUNT;i++){
    pts.userData.seeds[i*2] = Math.random()*100;
    pts.userData.seeds[i*2+1] = Math.random()*100;
  }
  return pts;
}
// ── Apply time step to scene ──────────────────────────────────────
function applyTimeStep(step){
  currentTimeStep = step;
  // Remove old objects
  if(terrainMesh){terrainMesh.geometry.dispose();scene.remove(terrainMesh);}
  if(riverLine){riverLine.geometry.dispose();scene.remove(riverLine);}
  // Build terrain from cache (or populate cache on miss)
  const {geometry:terrainGeo} = buildTerrainGeometry(step);
  const terrainMat = new THREE.MeshStandardMaterial({
    vertexColors:true, roughness:0.7, metalness:0.1,
    side:THREE.DoubleSide, flatShading:false
  });
  terrainMesh = new THREE.Mesh(terrainGeo, terrainMat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  terrainMesh.userData.timeStep = step;
  scene.add(terrainMesh);
  // Build river from cache
  const riverGeo = buildRiverGeometry(step);
  const riverMat = new THREE.MeshStandardMaterial({
    color:0xff4444, roughness:0.3, metalness:0.5, emissive:0x330000, emissiveIntensity:0.6
  });
  riverLine = new THREE.Mesh(riverGeo, riverMat);
  riverLine.renderOrder = 1;
  riverLine.material.depthTest = true;
  riverLine.material.depthWrite = true;
  scene.add(riverLine);
  // Update metrics panel
  const data = generateTimeSeriesData(step);
  document.getElementById('m-rev').textContent = (data.maxRev*100).toFixed(0);
  document.getElementById('m-users').textContent = (data.userDensity*100).toFixed(1)+'%';
  document.getElementById('m-err').textContent = (data.errorRate*100).toFixed(2)+'%';
  document.getElementById('m-api').textContent = Math.round(data.apiRate);
  document.getElementById('m-step').textContent = (step+1)+'/'+TIME_STEPS;
  document.getElementById('time-label').textContent = 'Step '+(step+1);
  const mins = Math.floor(step*2);
  const secs = (step*4)%60;
  document.getElementById('time-value').textContent = mins+':'+String(Math.floor(secs)).padStart(2,'0');
}
// ── Particle update (per-frame, reuses position array) ────────────
function updateParticles(delta, elapsed){
  if(!particleSystem) return;
  const pos = particleSystem.userData.positions;
  const seeds = particleSystem.userData.seeds;
  const data = generateTimeSeriesData(currentTimeStep);
  const hd = data.heightData;
  for(let i=0;i<PARTICLE_COUNT;i++){
    const i3 = i*3;
    // Organic drift with terrain-following
    const seedX = seeds[i*2], seedZ = seeds[i*2+1];
    const driftX = Math.sin(elapsed*1.3+seedX)*0.02;
    const driftZ = Math.cos(elapsed*1.1+seedZ)*0.02;
    pos[i3] += driftX;
    pos[i3+2] += driftZ;
    // Wrap around terrain bounds
    const half = SIZE/2;
    if(Math.abs(pos[i3])>half) pos[i3] = -pos[i3]*0.9;
    if(Math.abs(pos[i3+2])>half) pos[i3+2] = -pos[i3+2]*0.9;
    // Clamp to terrain height + offset — no allocation, direct array access
    const gx = Math.floor((pos[i3]/SIZE+0.5)*(GRID-1));
    const gz = Math.floor((pos[i3+2]/SIZE+0.5)*(GRID-1));
    if(gx>=0&&gx<GRID&&gz>=0&&gz<GRID){
      const th = hd[gz*GRID+gx]*6;
      pos[i3+1] += (th+1.2 - pos[i3+1])*0.08; // smooth terrain follow
    }
  }
  particleSystem.geometry.attributes.position.needsUpdate = true;
}
// ── Cache UI update ───────────────────────────────────────────────
function updateCacheUI(){
  const total = cacheStats.terrainHit+cacheStats.terrainMiss+cacheStats.riverHit+cacheStats.riverMiss+cacheStats.gridHit+cacheStats.gridMiss;
  const hits = cacheStats.terrainHit+cacheStats.riverHit+cacheStats.gridHit;
  document.getElementById('c-terrain-hit').textContent = cacheStats.terrainHit;
  document.getElementById('c-terrain-miss').textContent = cacheStats.terrainMiss;
  document.getElementById('c-river-hit').textContent = cacheStats.riverHit;
  document.getElementById('c-river-miss').textContent = cacheStats.riverMiss;
  document.getElementById('c-grid-hit').textContent = cacheStats.gridHit;
  document.getElementById('c-rate').textContent = total>0 ? (hits/total*100).toFixed(1)+'%' : '0%';
}
// ── Grid transform with memoization ───────────────────────────────
function worldToGrid(wx, wz){
  const key = wx.toFixed(4)+','+wz.toFixed(4);
  if(gridTransformCache.has(key)){
    cacheStats.gridHit++;
    return gridTransformCache.get(key);
  }
  cacheStats.gridMiss++;
  const gx = Math.floor((wx/SIZE+0.5)*(GRID-1));
  const gz = Math.floor((wz/SIZE+0.5)*(GRID-1));
  const result = {
    gx:Math.max(0,Math.min(GRID-1,gx)),
    gz:Math.max(0,Math.min(GRID-1,gz))
  };
  gridTransformCache.set(key, result);
  return result;
}
// ── Initialize scene ──────────────────────────────────────────────
applyTimeStep(0);
particleSystem = buildParticleSystem();
scene.add(particleSystem);
// ── UI event handlers ─────────────────────────────────────────────
const slider = document.getElementById('time-slider');
slider.max = TIME_STEPS-1;
slider.value = 0;
// Debounced river rebuild timer
let riverDebounceTimer = null;
slider.addEventListener('input', ()=>{
  const step = parseInt(slider.value);
  // Clear grid transform cache each frame for fresh memoization window
  gridTransformCache.clear();
  applyTimeStep(step);
});
// Auto-play
let playing = false;
let playInterval = null;
document.getElementById('time-play').addEventListener('click', ()=>{
  playing = !playing;
  const btn = document.getElementById('time-play');
  btn.textContent = playing?'Pause':'Play';
  btn.style.borderColor = playing?'var(--accent)':'var(--border)';
  if(playing){
    playInterval = setInterval(()=>{
      let next = (parseInt(slider.value)+1)%TIME_STEPS;
      slider.value = next;
      gridTransformCache.clear();
      applyTimeStep(next);
    }, 400);
  }else{
    clearInterval(playInterval);
  }
});
// Auto-rotate toggle
let autoRotating = false;
document.getElementById('auto-rotate-btn').addEventListener('click', ()=>{
  autoRotating = !autoRotating;
  controls.autoRotate = autoRotating;
  const btn = document.getElementById('auto-rotate-btn');
  btn.textContent = 'Auto-Rotate: '+(autoRotating?'On':'Off');
  btn.classList.toggle('active', autoRotating);
});
// Camera bookmarks
document.querySelectorAll('.bookmark-btn[data-idx]').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    const idx = parseInt(btn.dataset.idx);
    if(idx===3){
      // Save current view
      bookmarks.push({
        pos:camera.position.toArray(),
        target:controls.target.toArray()
      });
      btn.classList.add('saved');
      btn.textContent = 'View '+(bookmarks.length-3);
      return;
    }
    if(idx>=bookmarks.length) return;
    const bm = bookmarks[idx];
    // Smooth animate to bookmark
    const startPos = camera.position.clone();
    const startTarget = controls.target.clone();
    const endPos = new THREE.Vector3(...bm.pos);
    const endTarget = new THREE.Vector3(...bm.target);
    const startTime = performance.now();
    const duration = 800;
    function animCam(now){
      const t = Math.min((now-startTime)/duration, 1);
      const ease = t<0.5?2*t*t:-1+(4-2*t)*t; // ease in-out
      camera.position.lerpVectors(startPos, endPos, ease);
      controls.target.lerpVectors(startTarget, endTarget, ease);
      controls.update();
      if(t<1) requestAnimationFrame(animCam);
    }
    requestAnimationFrame(animCam);
  });
});
// ── Render loop ───────────────────────────────────────────────────
const clock = new THREE.Clock();
let frameCount = 0;
function animate(){
  requestAnimationFrame(animate);
  const delta = Math.min(clock.getDelta(), 0.1);
  const elapsed = clock.elapsedTime;
  controls.update();
  updateParticles(delta, elapsed);
  // Update cache UI every 30 frames (throttled)
  frameCount++;
  if(frameCount%30===0) updateCacheUI();
  renderer.render(scene, camera);
}
animate();
// ── Resize handler ────────────────────────────────────────────────
window.addEventListener('resize', ()=>{
  camera.aspect = container.clientWidth/container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth, container.clientHeight);
});
console.log('3D Data Terrain Explorer initialized');
console.log('Cache stores:',{terrain:terrainCache.size, river:riverCache.size, noise:noiseGridCache.size});
</script>
</body>
</html>