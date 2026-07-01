E:\Stryde\_alpedal\styde-forge\3d_data_terrain_explorer.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;overflow:hidden;font-family:system-ui,sans-serif}
#canvas{display:block}
#ui{position:fixed;bottom:0;left:0;right:0;background:rgba(10,10,20,0.92);backdrop-filter:blur(8px);padding:12px 20px;display:flex;gap:16px;align-items:center;z-index:10;border-top:1px solid #222}
#ui label{color:#aaa;font-size:11px;text-transform:uppercase;letter-spacing:0.5px}
#time-slider{flex:1;accent-color:#4af}
#time-value{color:#4af;font-weight:600;min-width:48px;text-align:center}
button{background:#1a1a2e;color:#ccc;border:1px solid #333;padding:6px 12px;cursor:pointer;border-radius:4px;font-size:11px;letter-spacing:0.3px}
button:hover{background:#2a2a4e;border-color:#4af}
button.active{background:#1a3a5e;border-color:#4af;color:#4af}
#bookmarks{display:flex;gap:6px}
#diag-panel{position:fixed;top:12px;right:12px;background:rgba(10,10,20,0.9);padding:10px 14px;border-radius:6px;border:1px solid #222;font-size:10px;color:#888;z-index:10;min-width:180px}
#diag-panel .hit{color:#4a4}
#diag-panel .miss{color:#a44}
#diag-panel .val{color:#ccc;float:right}
</style>
</head>
<body>
<div id="ui">
  <label>Time</label>
  <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
  <span id="time-value">T0</span>
  <button id="btn-play">Play</button>
  <button id="btn-pause" style="display:none">Pause</button>
  <button id="btn-auto-rotate">Auto-Rotate</button>
  <div id="bookmarks">
    <button class="bm-btn" data-idx="0">Top</button>
    <button class="bm-btn" data-idx="1">Side</button>
    <button class="bm-btn" data-idx="2">Close</button>
    <button id="btn-save-bm">+Save</button>
  </div>
</div>
<div id="diag-panel">
  <div>Cache <span class="val"><span class="hit" id="diag-hit">0</span>/<span class="miss" id="diag-miss">0</span></span></div>
  <div>FPS <span class="val" id="diag-fps">--</span></div>
  <div>Particles <span class="val" id="diag-pcount">0</span></div>
</div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
/* ── Synthetic time-series data grid 20×20 × 100 time steps ── */
const GRID = 20, TICKS = 100;
const data = {revenue:[], users:[], errors:[], api_calls:[]};
// Generate smooth time-varying fields using layered sine waves + perlin-like noise
function genField(t, seed){
  const f = []; for(let i=0;i<GRID*GRID;i++){
    const x = i%GRID/GRID, y = Math.floor(i/GRID)/GRID;
    const sx = Math.sin(x*6 + t*0.02 + seed)*0.5 + Math.sin(y*4 + t*0.03)*0.5;
    const sy = Math.cos(y*5 - t*0.015 + seed*1.3)*0.5 + Math.cos(x*3.5 + t*0.025 + seed*0.7)*0.5;
    f.push(Math.max(0, sx*sy + 0.5));
  }
  // Add cluster hotspots that move over time
  const cx = 0.3 + Math.sin(t*0.01)*0.3, cy = 0.4 + Math.cos(t*0.012)*0.3;
  for(let i=0;i<GRID*GRID;i++){
    const x=i%GRID/GRID,y=Math.floor(i/GRID)/GRID;
    const d=Math.hypot(x-cx,y-cy); f[i]=Math.max(0,f[i]+Math.exp(-d*3)*0.6);
  }
  return f;
}
for(let t=0;t<TICKS;t++){
  data.revenue[t] = genField(t, 0);
  data.users[t] = genField(t, 2.5);
  data.errors[t] = genField(t, 5.0);
  data.api_calls[t] = genField(t, 7.5);
}
/* ── Cache system tracked with hit/miss counters for the diagnostic panel ── */
const cache = new Map();
let cacheHits = 0, cacheMisses = 0;
function cacheGet(key){ if(cache.has(key)){cacheHits++; return cache.get(key)} cacheMisses++; return null }
function cacheSet(key, val){ cache.set(key, val) }
function cacheClear(){ cache.clear() }
/* ── Three.js scene setup ── */
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
document.body.prepend(renderer.domElement);
renderer.domElement.id = 'canvas';
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 8, 35);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.5, 60);
camera.position.set(8, 6, 10);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; controls.dampingFactor = 0.08;
controls.autoRotate = false; controls.autoRotateSpeed = 0.4;
controls.target.set(GRID/2, 1.5, GRID/2);
controls.maxPolarAngle = Math.PI * 0.48; controls.minDistance = 4; controls.maxDistance = 25;
controls.update();
/* ── Lighting ── */
const ambient = new THREE.AmbientLight(0x222244, 1.2); scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd, 2.5); sun.position.set(12, 18, 8);
sun.castShadow = true; sun.shadow.mapSize.set(1024,1024); sun.shadow.camera.near=0.5; sun.shadow.camera.far=50;
sun.shadow.camera.left=-15; sun.shadow.camera.right=15; sun.shadow.camera.top=15; sun.shadow.camera.bottom=-15;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa, 0.8); fill.position.set(-6, 3, -4); scene.add(fill);
/* ── Grid plane (translucent) ── */
const gridHelper = new THREE.PolarGridHelper(GRID*0.75, 40, 30, 64, 0x222244, 0x222244);
gridHelper.position.set(GRID/2, -0.05, GRID/2); scene.add(gridHelper);
/* ── Terrain mesh (reusable geometry, swap vertex data per tick) ── */
const terrainGeo = new THREE.PlaneGeometry(GRID, GRID, GRID-1, GRID-1);
terrainGeo.rotateX(-Math.PI/2);
terrainGeo.setAttribute('color', new THREE.BufferAttribute(new Float32Array(GRID*GRID*3), 3));
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors: true, roughness: 0.75, metalness: 0.05, flatShading: false
});
const terrain = new THREE.Mesh(terrainGeo, terrainMat);
terrain.receiveShadow = true; terrain.castShadow = true;
scene.add(terrain);
/* ── River lines (geometry reused, updated per tick with debounce) ── */
const riverGroup = new THREE.Group(); scene.add(riverGroup);
// We store river curve objects keyed by tick for cache reuse
const riverGeoCache = {}; // {tick: THREE.BufferGeometry}
function buildRivers(tick){
  const cached = cacheGet('rivers_'+tick);
  if(cached) return cached;
  // Clear previous rivers
  while(riverGroup.children.length) riverGroup.remove(riverGroup.children[0]);
  const err = data.errors[tick];
  // Find error hotspots: cells where error > 0.65
  const hotspots = [];
  for(let i=0;i<GRID*GRID;i++) if(err[i]>0.65) hotspots.push({x:i%GRID, z:Math.floor(i/GRID), v:err[i]});
  if(hotspots.length<2){ cacheSet('rivers_'+tick, []); return [] }
  // Sort hotspots into a path connecting them by proximity (greedy nearest-neighbor)
  const path = [hotspots.shift()];
  while(hotspots.length){
    let bestIdx=0, bestDist=Infinity;
    const last=path[path.length-1];
    for(let i=0;i<hotspots.length;i++){
      const d=Math.hypot(hotspots[i].x-last.x, hotspots[i].z-last.z);
      if(d<bestDist){bestDist=d; bestIdx=i}
    }
    path.push(...hotspots.splice(bestIdx,1));
  }
  // Build CatmullRom curve through these points, elevated above terrain
  const pts = path.map(p=>{
    const idx = Math.floor(p.z)*GRID+Math.floor(p.x);
    const h = data.revenue[tick][idx]*2.5 + 0.15; // height offset above terrain
    return new THREE.Vector3(p.x, h, p.z);
  });
  const curve = new THREE.CatmullRomCurve3(pts);
  const tubeGeo = new THREE.TubeGeometry(curve, 40, 0.12, 6, false);
  const tubeMat = new THREE.MeshStandardMaterial({color:0xee3333, emissive:0x661111, roughness:0.4});
  const tube = new THREE.Mesh(tubeGeo, tubeMat); tube.receiveShadow=true;
  riverGroup.add(tube);
  // Glow line
  const lineGeo = new THREE.BufferGeometry().setFromPoints(curve.getPoints(100));
  const line = new THREE.Line(lineGeo, new THREE.LineBasicMaterial({color:0xff4444, linewidth:1}));
  riverGroup.add(line);
  const result = {tube, line, curve};
  cacheSet('rivers_'+tick, result);
  return result;
}
/* ── Particles: flowing dots along API call density paths ── */
const PARTICLE_COUNT = 400;
const particlePositions = new Float32Array(PARTICLE_COUNT*3);
// Each particle has: progress along path, path index, speed
const particleData = new Float32Array(PARTICLE_COUNT*3); // [progress, pathIdx, speed]
const particleGeo = new THREE.BufferGeometry();
particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
const particleMat = new THREE.PointsMaterial({color:0x44aaff, size:0.12, blending:THREE.AdditiveBlending, depthWrite:false});
const particles = new THREE.Points(particleGeo, particleMat); scene.add(particles);
// Precompute flow paths from api_calls data — reuse across frames
let flowPaths = []; // [{points: [Vector3], tick}] — cached per tick
function buildFlowPaths(tick){
  const cached = cacheGet('flowpaths_'+tick);
  if(cached) return cached;
  const api = data.api_calls[tick];
  // Find cells with high API activity as waypoints
  const waypoints = [];
  for(let i=0;i<GRID*GRID;i++) if(api[i]>0.55) waypoints.push(i);
  const paths = [];
  // Chain waypoints into 3-5 node mini-paths
  for(let p=0;p<Math.min(waypoints.length-1, 20);p+=2){
    const a = waypoints[p], b = waypoints[Math.min(p+1, waypoints.length-1)];
    const ax=a%GRID, az=Math.floor(a/GRID), bx=b%GRID, bz=Math.floor(b/GRID);
    const ah=data.revenue[tick][a]*2.5+0.08, bh=data.revenue[tick][b]*2.5+0.08;
    paths.push([new THREE.Vector3(ax,ah,az), new THREE.Vector3(bx,bh,bz)]);
  }
  cacheSet('flowpaths_'+tick, paths);
  return paths;
}
// Initialize particles randomly along paths
function resetParticles(tick){
  const paths = buildFlowPaths(tick); flowPaths = paths;
  for(let i=0;i<PARTICLE_COUNT;i++){
    const pathIdx = Math.floor(Math.random()*Math.max(1, paths.length));
    particleData[i*3] = Math.random();     // progress 0-1
    particleData[i*3+1] = pathIdx;
    particleData[i*3+2] = 0.003 + Math.random()*0.007; // speed
    updateParticlePosition(i, tick);
  }
}
// CPU-side position update reusing position array — no per-frame allocation
function updateParticlePosition(i, tick){
  const paths=flowPaths;
  const pi=i*3, di=i*3;
  const pathIdx=Math.floor(particleData[di+1]);
  if(pathIdx>=paths.length||paths[pathIdx].length<2){ particlePositions[pi]=0; particlePositions[pi+1]=0; particlePositions[pi+2]=0; return }
  const t=particleData[di];
  const segs=paths[pathIdx]; const totalSegs=segs.length-1;
  const segFloat=t*totalSegs; const segIdx=Math.min(totalSegs-1, Math.floor(segFloat));
  const frac=segFloat-segIdx;
  const a=segs[segIdx], b=segs[segIdx+1];
  particlePositions[pi]=a.x+(b.x-a.x)*frac;
  particlePositions[pi+1]=a.y+(b.y-a.y)*frac;
  particlePositions[pi+2]=a.z+(b.z-a.z)*frac;
}
/* ── Terrain update per tick (reuse geometry, swap attribute arrays) ── */
function updateTerrain(tick){
  const cached = cacheGet('terrain_'+tick);
  const rev = data.revenue[tick], usr = data.users[tick];
  const posArr = terrainGeo.attributes.position.array;
  const colArr = terrainGeo.attributes.color.array;
  if(cached){
    // Use cached position + color arrays
    const cp = cached.pos, cc = cached.col;
    for(let i=0;i<posArr.length;i++) posArr[i]=cp[i];
    for(let i=0;i<colArr.length;i++) colArr[i]=cc[i];
  } else {
    const cp = new Float32Array(posArr.length), cc = new Float32Array(colArr.length);
    for(let i=0;i<GRID*GRID;i++){
      const h = rev[i]*2.5; // Revenue → elevation 0-2.5
      const vi = i*3;
      posArr[vi+1] = h; cp[vi]=posArr[vi]; cp[vi+1]=h; cp[vi+2]=posArr[vi+2];
      // Vegetation coloring: high users = green, low = brown
      const u = usr[i];
      const r = 0.15 + u*0.1, g = 0.1 + u*0.6, b = 0.05 + u*0.1;
      colArr[vi]=r; colArr[vi+1]=g; colArr[vi+2]=b;
      cc[vi]=r; cc[vi+1]=g; cc[vi+2]=b;
    }
    cacheSet('terrain_'+tick, {pos:cp, col:cc});
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
}
/* ── Bookmarks ── */
const bookmarks = [
  {pos:[8,6,10], target:[GRID/2,1.5,GRID/2], label:'Top'},
  {pos:[18,2,GRID/2], target:[GRID/2,1,GRID/2], label:'Side'},
  {pos:[5,2,3], target:[GRID/2,1,GRID/2], label:'Close'}
];
function applyBookmark(idx){
  if(idx>=bookmarks.length) return;
  const bm=bookmarks[idx];
  camera.position.set(...bm.pos); controls.target.set(...bm.target); controls.update();
}
document.querySelectorAll('.bm-btn').forEach(btn=>{
  btn.addEventListener('click',()=>applyBookmark(parseInt(btn.dataset.idx)));
});
document.getElementById('btn-save-bm').addEventListener('click',()=>{
  const bm={pos:camera.position.toArray(), target:controls.target.toArray(), label:'BM'+bookmarks.length};
  bookmarks.push(bm);
  const b=document.createElement('button'); b.className='bm-btn'; b.dataset.idx=bookmarks.length-1;
  b.textContent=bm.label; b.addEventListener('click',()=>applyBookmark(bookmarks.length-1));
  document.getElementById('bookmarks').insertBefore(b, document.getElementById('btn-save-bm'));
});
/* ── Time slider ── */
let currentTick = 0, playing = false, playInterval = null;
const slider = document.getElementById('time-slider');
const timeVal = document.getElementById('time-value');
function setTick(tick){
  currentTick = Math.max(0, Math.min(TICKS-1, tick));
  slider.value = currentTick;
  timeVal.textContent = 'T'+currentTick;
  updateTerrain(currentTick);
  buildRivers(currentTick);
  resetParticles(currentTick);
}
slider.addEventListener('input', ()=>{ setTick(parseInt(slider.value)) });
document.getElementById('btn-play').addEventListener('click',()=>{
  playing=true;
  document.getElementById('btn-play').style.display='none';
  document.getElementById('btn-pause').style.display='';
  playInterval=setInterval(()=>{
    if(currentTick<TICKS-1) setTick(currentTick+1); else { playing=false; clearInterval(playInterval); document.getElementById('btn-play').style.display=''; document.getElementById('btn-pause').style.display='none' }
  }, 120);
});
document.getElementById('btn-pause').addEventListener('click',()=>{
  playing=false; clearInterval(playInterval);
  document.getElementById('btn-play').style.display=''; document.getElementById('btn-pause').style.display='none';
});
document.getElementById('btn-auto-rotate').addEventListener('click',function(){
  controls.autoRotate=!controls.autoRotate; this.classList.toggle('active', controls.autoRotate);
});
/* ── Responsive ── */
window.addEventListener('resize',()=>{
  camera.aspect = window.innerWidth/window.innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
/* ── FPS counter ── */
let fpsFrames=0, fpsLast=performance.now();
const diagHit = document.getElementById('diag-hit'), diagMiss = document.getElementById('diag-miss');
const diagFps = document.getElementById('diag-fps'), diagPcount = document.getElementById('diag-pcount');
/* ── Render loop ── */
function animate(time){
  requestAnimationFrame(animate);
  controls.update();
  // Animate particles along flow paths — reuse position array, no allocation
  if(flowPaths.length>0){
    for(let i=0;i<PARTICLE_COUNT;i++){
      const di=i*3;
      particleData[di] += particleData[di+2];
      if(particleData[di]>1.0){
        // Wrap to random new path
        particleData[di]=0;
        particleData[di+1]=Math.floor(Math.random()*Math.max(1, flowPaths.length));
        particleData[di+2]=0.003+Math.random()*0.007;
      }
      updateParticlePosition(i, currentTick);
    }
    particleGeo.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
  // Update diagnostic panel every 30 frames
  fpsFrames++;
  if(fpsFrames>=30){
    const now=performance.now();
    const fps=Math.round(30000/(now-fpsLast));
    diagHit.textContent=cacheHits; diagMiss.textContent=cacheMisses;
    diagFps.textContent=fps; diagPcount.textContent=PARTICLE_COUNT;
    fpsFrames=0; fpsLast=now;
  }
}
/* ── Initialize and start ── */
setTick(0);
animate(0);
</script>
</body>
</html>