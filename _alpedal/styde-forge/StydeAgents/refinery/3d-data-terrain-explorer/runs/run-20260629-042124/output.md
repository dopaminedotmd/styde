<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#ddd}
#canvas{position:fixed;inset:0;z-index:1}
#ui{position:fixed;z-index:10;pointer-events:none}
#ui>*{pointer-events:auto}
#panel{position:fixed;top:16px;left:16px;background:rgba(10,10,30,0.85);border:1px solid rgba(100,140,255,0.3);border-radius:10px;padding:14px 18px;min-width:260px;backdrop-filter:blur(8px)}
#panel h2{font-size:15px;font-weight:600;color:#7eb8ff;margin-bottom:10px;letter-spacing:0.5px}
.row{display:flex;align-items:center;justify-content:space-between;margin:6px 0;font-size:12px;gap:10px}
.row label{color:#aaa;white-space:nowrap}
.row span{color:#fff;font-weight:600;font-variant-numeric:tabular-nums}
#timeslider{width:100%;margin:10px 0;accent-color:#4a8eff;height:6px}
#time-label{text-align:center;font-size:12px;color:#8ab8ff;margin-top:2px}
.btn{display:inline-block;padding:6px 12px;margin:3px 4px;background:rgba(60,100,200,0.25);border:1px solid rgba(100,140,255,0.4);border-radius:6px;color:#cde;font-size:11px;cursor:pointer;transition:all 0.2s}
.btn:hover{background:rgba(80,130,255,0.45);border-color:rgba(130,170,255,0.7)}
.btn.active{background:rgba(80,140,255,0.5);border-color:#5a9eff;color:#fff}
.btn-row{display:flex;flex-wrap:wrap;gap:4px;margin:8px 0}
#import-area{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(10,10,35,0.95);border:2px dashed rgba(100,140,255,0.5);border-radius:14px;padding:30px 40px;text-align:center;z-index:20;display:none;backdrop-filter:blur(12px)}
#import-area.show{display:block}
#import-area h3{color:#8ab8ff;margin-bottom:12px}
#import-area input{display:block;margin:12px auto;color:#fff}
#stats{position:fixed;bottom:16px;right:16px;font-size:10px;color:#556;text-align:right;z-index:10}
#stats span{display:block}
#legend{position:fixed;bottom:16px;left:16px;font-size:10px;color:#667;z-index:10;background:rgba(10,10,30,0.7);padding:8px 12px;border-radius:6px}
#legend div{display:flex;align-items:center;gap:6px;margin:3px 0}
.swatch{width:12px;height:12px;border-radius:2px}
input[type=file]{color:#ccc;font-size:12px}
</style>
</head>
<body>
<div id="canvas"></div>
<div id="ui">
<div id="panel">
<h2>Data Terrain Explorer</h2>
<div class="row"><label>Time slice</label><span id="time-label">Q1 2024</span></div>
<input type="range" id="timeslider" min="0" max="9" value="0" step="1">
<div class="btn-row" id="bookmarks"></div>
<div class="btn-row">
<button class="btn" id="btn-import" title="Import CSV/JSON data">Import</button>
<button class="btn" id="btn-export" title="Export current view as JSON">Export</button>
<button class="btn" id="btn-autorot" title="Toggle auto-rotation">AutoRot</button>
<button class="btn" id="btn-reset" title="Reset camera">Reset</button>
<button class="btn" id="btn-bookmark" title="Save camera bookmark">+Bookmark</button>
</div>
<div class="row"><label>Revenue (elev)</label><span id="val-rev">--</span></div>
<div class="row"><label>Users (color)</label><span id="val-users">--</span></div>
<div class="row"><label>Errors (rivers)</label><span id="val-err">--</span></div>
<div class="row"><label>API calls (trails)</label><span id="val-api">--</span></div>
</div>
</div>
<div id="import-area">
<h3>Import Data (CSV or JSON)</h3>
<p style="color:#889;font-size:11px;margin-bottom:8px">CSV: time,product,revenue,users,errors,api_calls<br>JSON: [{time,product,revenue,users,errors,api_calls},...]</p>
<input type="file" id="file-input" accept=".csv,.json">
<button class="btn" id="btn-import-cancel" style="margin-top:10px">Cancel</button>
</div>
<div id="legend">
<div><span class="swatch" style="background:#2d8a4e"></span> Revenue elevation (height)</div>
<div><span class="swatch" style="background:linear-gradient(90deg,#1a4,#8f4,#fe2)"></span> User density (vertex color)</div>
<div><span class="swatch" style="background:#e33"></span> Error river pathways</div>
<div><span class="swatch" style="background:#4af"></span> API call particle trails</div>
</div>
<div id="stats"><span>FPS: <span id="fps">0</span></span><span>Vertices: <span id="vc">0</span></span><span>Cache: <span id="cache-hits">0</span> hits</span></div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 80;
const TIME_SLICES = 10;
const TIME_LABELS = ['Q1','Q2','Q3','Q4'].flatMap(q=>[2021,2022,2023,2024].map(y=>`${q} ${y}`)).slice(0,TIME_SLICES);
let rawData = generateDefaultData();
let cachedGeometries = new Map();
let cacheHits = 0;
let currentSlice = 0;
let riverLines = [];
let particleSystem;
let autoRotate = false;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 30, 120);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 1, 300);
camera.position.set(45, 35, 55);
camera.lookAt(40, 0, 40);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.getElementById('canvas').appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.target.set(40, 0, 40);
controls.minDistance = 10;
controls.maxDistance = 150;
controls.maxPolarAngle = Math.PI * 0.48;
controls.autoRotate = false;
controls.autoRotateSpeed = 0.3;
controls.update();
const ambientLight = new THREE.AmbientLight(0x223355, 1.2);
scene.add(ambientLight);
const sun = new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(60, 50, 20);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 1;
sun.shadow.camera.far = 200;
sun.shadow.camera.left = -60;
sun.shadow.camera.right = 60;
sun.shadow.camera.top = 60;
sun.shadow.camera.bottom = -60;
scene.add(sun);
const fillLight = new THREE.DirectionalLight(0x4466aa, 0.8);
fillLight.position.set(-30, 20, -20);
scene.add(fillLight);
const gridHelper = new THREE.GridHelper(80, 20, 0x223344, 0x111122);
gridHelper.position.set(40, -0.5, 40);
scene.add(gridHelper);
const groundGeo = new THREE.PlaneGeometry(80, 80);
const groundMat = new THREE.MeshStandardMaterial({color:0x0a0a1e, roughness:0.95, metalness:0.1});
const ground = new THREE.Mesh(groundGeo, groundMat);
ground.rotation.x = -Math.PI/2;
ground.position.set(40, -2, 40);
ground.receiveShadow = true;
scene.add(ground);
let terrainMesh;
function generateDefaultData(){
  const data = [];
  for(let t=0; t<TIME_SLICES; t++){
    const trend = 1 + t * 0.08;
    const seasonality = Math.sin(t * Math.PI/2) * 0.15;
    for(let x=0; x<GRID; x++){
      for(let y=0; y<GRID; y++){
        const cx = (x-GRID/2)/(GRID/3);
        const cy = (y-GRID/2)/(GRID/3);
        const dist = Math.sqrt(cx*cx+cy*cy);
        const rev = Math.max(0, (8 - dist*2.5 + Math.sin(cx*1.7)*1.5 + Math.cos(cy*1.3)*2) * trend + seasonality * (GRID/2-Math.abs(x-GRID/2))/10);
        const users = Math.max(0, rev * (0.6 + Math.sin(cx*0.8+cy*0.6)*0.3));
        const errors = Math.max(0, (Math.abs(cx-0.8) < 0.6 && Math.abs(cy+0.3) < 0.4 ? 1.5 : 0.1) + Math.random()*0.3);
        const api = users * (0.2 + Math.random()*0.4);
        data.push({time:t, product:x*GRID+y, revenue:rev, users, errors, api_calls:api});
      }
    }
  }
  return data;
}
function getSliceData(sliceIdx){
  return rawData.filter(d=>d.time===sliceIdx);
}
function buildTerrainGeometry(sliceIdx){
  if(cachedGeometries.has(sliceIdx)){
    cacheHits++;
    return cachedGeometries.get(sliceIdx).clone();
  }
  const slice = getSliceData(sliceIdx);
  const w = GRID, h = GRID;
  const vertices = new Float32Array(w*h*3);
  const colors = new Float32Array(w*h*3);
  const indices = [];
  let maxRev = 0, maxUsers = 0;
  for(const d of slice){ if(d.revenue>maxRev) maxRev=d.revenue; if(d.users>maxUsers) maxUsers=d.users; }
  maxRev = maxRev || 1; maxUsers = maxUsers || 1;
  for(let i=0;i<slice.length;i++){
    const d = slice[i];
    const x = Math.floor(d.product / GRID);
    const y = d.product % GRID;
    const idx = (y*w + x);
    vertices[idx*3] = x;
    vertices[idx*3+1] = d.revenue * 4;
    vertices[idx*3+2] = y;
    const t = Math.min(1, d.users / maxUsers);
    colors[idx*3] = 0.1 + t*0.3;
    colors[idx*3+1] = 0.2 + t*0.7;
    colors[idx*3+2] = 0.15;
  }
  for(let iy=0; iy<h-1; iy++){
    for(let ix=0; ix<w-1; ix++){
      const a = iy*w+ix, b = a+1, c = a+w, d = c+1;
      indices.push(a,b,d, a,d,c);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  cachedGeometries.set(sliceIdx, geo.clone());
  return geo;
}
function buildRivers(sliceIdx){
  riverLines.forEach(l=>scene.remove(l));
  riverLines = [];
  const slice = getSliceData(sliceIdx);
  const errorMap = new Map();
  for(const d of slice){
    if(d.errors > 1.2) errorMap.set(d.product, d.errors);
  }
  const visited = new Set();
  const dirs = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  function trace(x,y){
    const key = y*GRID+x;
    if(visited.has(key)) return null;
    const points = [[x,0,y]];
    visited.add(key);
    let cx=x, cy=y, steps=0;
    while(steps<40){
      let best = null, bestErr = 0;
      for(const [dx,dy] of dirs){
        const nx=cx+dx, ny=cy+dy;
        if(nx<0||nx>=GRID||ny<0||ny>=GRID) continue;
        const nk = ny*GRID+nx;
        if(visited.has(nk)) continue;
        const e = errorMap.get(nk)||0;
        if(e>bestErr && e>1.0){ bestErr=e; best=[nx,ny]; }
      }
      if(!best) break;
      cx=best[0]; cy=best[1];
      visited.add(cy*GRID+cx);
      const sd = slice[cy*GRID+cx];
      points.push([cx, (sd?sd.revenue:0)*4 + 0.3, cy]);
      steps++;
    }
    return points.length>3 ? points : null;
  }
  for(const [prod, err] of errorMap){
    if(err<1.5) continue;
    const x = Math.floor(prod/GRID), y = prod%GRID;
    const path = trace(x,y);
    if(!path) continue;
    const curve = new THREE.CatmullRomCurve3(path.map(p=>new THREE.Vector3(p[0],p[1],p[2])));
    const pts = curve.getPoints(path.length*3);
    const geo = new THREE.BufferGeometry().setFromPoints(pts);
    const mat = new THREE.LineBasicMaterial({color:0xee3333, linewidth:1, transparent:true, opacity:0.85});
    const line = new THREE.Line(geo, mat);
    scene.add(line);
    riverLines.push(line);
  }
}
function buildParticles(sliceIdx){
  if(particleSystem) scene.remove(particleSystem);
  const slice = getSliceData(sliceIdx);
  const count = Math.min(3000, slice.length);
  const positions = new Float32Array(count*3);
  const velocities = new Float32Array(count*3);
  let pi = 0;
  for(const d of slice){
    if(pi>=count) break;
    if(d.api_calls < 0.5) continue;
    const x = Math.floor(d.product/GRID);
    const y = d.product%GRID;
    positions[pi*3] = x + (Math.random()-0.5)*0.8;
    positions[pi*3+1] = d.revenue*4 + 0.5 + Math.random();
    positions[pi*3+2] = y + (Math.random()-0.5)*0.8;
    velocities[pi*3] = (Math.random()-0.5)*0.3;
    velocities[pi*3+1] = Math.random()*0.2;
    velocities[pi*3+2] = (Math.random()-0.5)*0.3;
    pi++;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.userData = {velocities, count:pi};
  const mat = new THREE.PointsMaterial({color:0x44aaff, size:0.3, blending:THREE.AdditiveBlending, depthWrite:false, transparent:true, opacity:0.7});
  particleSystem = new THREE.Points(geo, mat);
  scene.add(particleSystem);
}
function loadSlice(idx){
  currentSlice = idx;
  if(terrainMesh) scene.remove(terrainMesh);
  const geo = buildTerrainGeometry(idx);
  const mat = new THREE.MeshStandardMaterial({vertexColors:true, roughness:0.6, metalness:0.2, flatShading:false, side:THREE.DoubleSide});
  terrainMesh = new THREE.Mesh(geo, mat);
  terrainMesh.castShadow = true;
  terrainMesh.receiveShadow = true;
  scene.add(terrainMesh);
  buildRivers(idx);
  buildParticles(idx);
  document.getElementById('time-label').textContent = TIME_LABELS[idx];
  updateStats(idx);
  document.getElementById('cache-hits').textContent = cacheHits;
  document.getElementById('vc').textContent = geo.attributes.position.count;
}
function updateStats(idx){
  const slice = getSliceData(idx);
  const sums = slice.reduce((a,d)=>({rev:a.rev+d.revenue, users:a.users+d.users, err:a.err+d.errors, api:a.api+d.api_calls}),{rev:0,users:0,err:0,api:0});
  document.getElementById('val-rev').textContent = (sums.rev/1000).toFixed(1)+'k';
  document.getElementById('val-users').textContent = (sums.users/1000).toFixed(1)+'k';
  document.getElementById('val-err').textContent = sums.err.toFixed(0);
  document.getElementById('val-api').textContent = (sums.api/1000).toFixed(1)+'k';
}
let bookmarks = JSON.parse(localStorage.getItem('terrain-bookmarks')||'[]');
function renderBookmarks(){
  const container = document.getElementById('bookmarks');
  container.innerHTML = '';
  bookmarks.forEach((b,i)=>{
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.textContent = b.label||`View ${i+1}`;
    btn.title = b.label||'';
    btn.onclick = ()=>{
      camera.position.set(b.pos.x,b.pos.y,b.pos.z);
      controls.target.set(b.target.x,b.target.y,b.target.z);
      controls.update();
    };
    btn.oncontextmenu = (e)=>{e.preventDefault(); bookmarks.splice(i,1); saveBookmarks(); renderBookmarks();};
    container.appendChild(btn);
  });
}
function saveBookmarks(){ localStorage.setItem('terrain-bookmarks', JSON.stringify(bookmarks)); }
document.getElementById('timeslider').addEventListener('input',(e)=>{
  loadSlice(parseInt(e.target.value));
});
document.getElementById('btn-autorot').addEventListener('click',function(){
  autoRotate = !autoRotate;
  controls.autoRotate = autoRotate;
  this.classList.toggle('active', autoRotate);
});
document.getElementById('btn-reset').addEventListener('click',()=>{
  camera.position.set(45,35,55);
  controls.target.set(40,0,40);
  controls.update();
});
document.getElementById('btn-bookmark').addEventListener('click',()=>{
  const label = prompt('Bookmark label:')||`View ${bookmarks.length+1}`;
  bookmarks.push({label,pos:{x:camera.position.x,y:camera.position.y,z:camera.position.z},target:{x:controls.target.x,y:controls.target.y,z:controls.target.z}});
  saveBookmarks();
  renderBookmarks();
});
document.getElementById('btn-import').addEventListener('click',()=>{
  document.getElementById('import-area').classList.add('show');
});
document.getElementById('btn-import-cancel').addEventListener('click',()=>{
  document.getElementById('import-area').classList.remove('show');
});
document.getElementById('btn-export').addEventListener('click',()=>{
  const blob = new Blob([JSON.stringify(rawData,null,2)],{type:'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'terrain-data-export.json'; a.click();
  URL.revokeObjectURL(url);
});
document.getElementById('file-input').addEventListener('change',async(e)=>{
  const file = e.target.files[0];
  if(!file) return;
  try{
    const text = await file.text();
    let parsed;
    if(file.name.endsWith('.csv')){
      parsed = parseCSV(text);
    }else{
      parsed = JSON.parse(text);
    }
    if(!Array.isArray(parsed) || parsed.length===0) throw new Error('Empty or invalid data');
    const req = ['time','product','revenue','users','errors','api_calls'];
    for(const k of req) if(!(k in parsed[0])) throw new Error(`Missing field: ${k}`);
    rawData = parsed;
    cachedGeometries.clear();
    cacheHits = 0;
    loadSlice(0);
    document.getElementById('import-area').classList.remove('show');
    document.getElementById('timeslider').max = Math.max(...parsed.map(d=>d.time));
  }catch(err){
    alert('Import failed: '+err.message);
  }
});
function parseCSV(text){
  const lines = text.trim().split('\n');
  const headers = lines[0].split(',').map(h=>h.trim().toLowerCase().replace(/\s+/g,'_'));
  return lines.slice(1).map(line=>{
    const vals = line.split(',');
    const obj = {};
    headers.forEach((h,i)=>obj[h]=isNaN(vals[i])?vals[i]:parseFloat(vals[i]));
    obj.time = obj.time||0;
    obj.product = obj.product||0;
    obj.revenue = obj.revenue||0;
    obj.users = obj.users||0;
    obj.errors = obj.errors||0;
    obj.api_calls = obj.api_calls||0;
    return obj;
  });
}
window.addEventListener('resize',()=>{
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
let frameCount = 0, lastFpsTime = performance.now();
function animate(time){
  requestAnimationFrame(animate);
  controls.update();
  if(particleSystem && particleSystem.geometry.userData.velocities){
    const pos = particleSystem.geometry.attributes.position.array;
    const vel = particleSystem.geometry.userData.velocities;
    const cnt = particleSystem.geometry.userData.count;
    for(let i=0;i<cnt;i++){
      pos[i*3] += vel[i*3];
      pos[i*3+1] += vel[i*3+1];
      pos[i*3+2] += vel[i*3+2];
      if(pos[i*3+1] > 35){ pos[i*3+1] -= 30; }
      if(pos[i*3+1] < 0){ pos[i*3+1] += 8; }
    }
    particleSystem.geometry.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
  frameCount++;
  if(time - lastFpsTime > 1000){
    document.getElementById('fps').textContent = frameCount;
    frameCount = 0;
    lastFpsTime = time;
  }
}
renderBookmarks();
loadSlice(0);
requestAnimationFrame(animate);
</script>
</body>
</html>