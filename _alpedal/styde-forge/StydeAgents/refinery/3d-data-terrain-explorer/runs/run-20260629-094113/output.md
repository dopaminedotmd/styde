<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a14;--panel:#111122cc;--text:#c8d6e5;--accent:#4ecdc4;--river:#ff6b6b;--gold:#ffd93d}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  canvas{display:block}
  #panel{position:fixed;top:12px;left:12px;background:var(--panel);backdrop-filter:blur(12px);border-radius:10px;padding:14px 16px;min-width:220px;z-index:10;border:1px solid #ffffff18}
  #panel h2{font-size:14px;color:var(--accent);margin-bottom:10px;font-weight:600}
  .ctrl{margin:6px 0;display:flex;align-items:center;gap:8px;font-size:12px}
  .ctrl label{min-width:48px;color:#8899aa}
  .ctrl input[type=range]{flex:1;accent-color:var(--accent);height:4px}
  .ctrl span{min-width:40px;text-align:right;font-size:11px;color:var(--accent)}
  #bookmarks{margin-top:10px}
  .bm-btn{display:block;width:100%;margin:3px 0;padding:5px 8px;font-size:11px;background:#ffffff0a;border:1px solid #ffffff15;color:var(--text);border-radius:4px;cursor:pointer;text-align:left;transition:all .15s}
  .bm-btn:hover{background:#ffffff18;border-color:var(--accent);color:var(--accent)}
  #legend{position:fixed;bottom:20px;right:20px;background:var(--panel);backdrop-filter:blur(12px);border-radius:8px;padding:10px 12px;z-index:10;border:1px solid #ffffff18;font-size:11px}
  .legend-row{display:flex;align-items:center;gap:8px;margin:4px 0}
  .legend-swatch{width:14px;height:14px;border-radius:3px;flex-shrink:0}
  #tooltip{position:fixed;pointer-events:none;background:#000000dd;color:#fff;padding:6px 10px;border-radius:5px;font-size:11px;display:none;z-index:20;white-space:pre-line;border:1px solid #ffffff22}
  #perf{position:fixed;bottom:20px;left:20px;background:var(--panel);backdrop-filter:blur(12px);border-radius:8px;padding:8px 12px;z-index:10;border:1px solid #ffffff18;font-size:10px;font-family:monospace}
  #perf .hit{color:#4ecdc4}#perf .miss{color:#ff6b6b}
  #axis-labels{position:fixed;pointer-events:none;z-index:5;font-size:10px;color:#8899aa}
</style>
</head>
<body>
<div id="panel">
  <h2>Terrain Explorer</h2>
  <div class="ctrl"><label>Tid</label><input type="range" id="timeSlider" min="0" max="11" value="0"><span id="timeLabel">Jan</span></div>
  <div class="ctrl"><label>Höjd</label><input type="range" id="heightScale" min="0.5" max="4" step="0.1" value="1.5"><span id="hScaleVal">1.5x</span></div>
  <div class="ctrl"><label id="autoRotLabel">Auto</label><input type="checkbox" id="autoRotate" checked></div>
  <div id="bookmarks">
    <button class="bm-btn" data-bm="0">Default vy</button>
    <button class="bm-btn" data-bm="1">Ovanifrån</button>
    <button class="bm-btn" data-bm="2">Flodperspektiv</button>
    <button class="bm-btn" data-bm="3">Spara aktuell</button>
  </div>
</div>
<div id="legend">
  <div style="margin-bottom:6px;font-weight:600;color:var(--accent)">Teckenförklaring</div>
  <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(to right,#1a3a1a,#4ecdc4,#f0fff0)"></div>Användartäthet (låg→hög)</div>
  <div class="legend-row"><div class="legend-swatch" style="background:var(--river)"></div>Felflöden (avvikelser)</div>
  <div class="legend-row"><div class="legend-swatch" style="background:var(--gold);border-radius:50%;width:8px;height:8px;margin:3px"></div>API-anrop (partiklar)</div>
  <div style="margin-top:5px;color:#8899aa">Elevation = Intäkt</div>
</div>
<div id="perf">
  Cache: <span id="cacheHit" class="hit">0</span> hits / <span id="cacheMiss" class="miss">0</span> misses
</div>
<div id="tooltip"></div>
<div id="axis-labels"></div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 60;
const STEPS = 12;
const MONTHS = ['Jan','Feb','Mar','Apr','Maj','Jun','Jul','Aug','Sep','Okt','Nov','Dec'];
let cacheStats = { hits:0, misses:0 };
const terrainCache = new Map();
const riverCache = new Map();
const particleStartCache = new Map();
function logCache(hit){
  if(hit) cacheStats.hits++; else cacheStats.misses++;
  document.getElementById('cacheHit').textContent = cacheStats.hits;
  document.getElementById('cacheMiss').textContent = cacheStats.misses;
}
function generateData(step){
  const h = new Float32Array(GRID*GRID);
  const u = new Float32Array(GRID*GRID);
  const errors = [];
  const apis = [];
  for(let i=0;i<GRID;i++){
    for(let j=0;j<GRID;j++){
      const idx = i*GRID+j;
      const nx = i/(GRID-1)*2-1, ny = j/(GRID-1)*2-1;
      const d = Math.sqrt(nx*nx+ny*ny);
      const revenue = 2.5*Math.exp(-d*1.8) + 0.8*Math.sin(nx*3+step*0.4)*Math.cos(ny*2.5+step*0.3) + 0.4*Math.cos(nx*5-step*0.2)*Math.sin(ny*4+step*0.25) + step*0.06;
      h[idx] = Math.max(0.05, revenue);
      u[idx] = 0.3 + 0.7*Math.exp(-d*1.2) + 0.15*Math.sin(nx*4+step*0.5)*Math.cos(ny*3.5);
      if(Math.abs(Math.sin(nx*7+step*0.8)*Math.cos(ny*6+step*0.7)) > 0.85 && d<1.2){
        errors.push({x:nx*5, z:ny*5, y:h[idx]*1.5, mag:0.3+0.7*Math.random()});
      }
    }
  }
  for(let k=0;k<40;k++){
    const angle = (k/40)*Math.PI*2 + step*0.5;
    const r = 1.5+2.5*Math.random();
    apis.push({x:Math.cos(angle)*r, z:Math.sin(angle)*r, speed:0.3+0.7*Math.random()});
  }
  return {heights:h, users:u, errors, apis};
}
function getTerrainData(step){
  if(terrainCache.has(step)){ logCache(true); return terrainCache.get(step); }
  logCache(false);
  const data = generateData(step);
  terrainCache.set(step, data);
  return data;
}
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18, 8, 30);
const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.5, 50);
camera.position.set(8, 7, 10);
camera.lookAt(0, 1.5, 0);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
document.body.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.3;
controls.maxPolarAngle = Math.PI*0.48;
controls.minDistance = 4;
controls.maxDistance = 20;
controls.update();
const bookmarks = [
  {pos:new THREE.Vector3(8,7,10), target:new THREE.Vector3(0,1.5,0)},
  {pos:new THREE.Vector3(0,14,0.1), target:new THREE.Vector3(0,0,0)},
  {pos:new THREE.Vector3(-3,3,7), target:new THREE.Vector3(0,0.5,0)},
];
const ambientLight = new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambientLight);
const sun = new THREE.DirectionalLight(0xffeedd, 2.5);
sun.position.set(10,15,5);
sun.castShadow = true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 40;
sun.shadow.camera.left = -10; sun.shadow.camera.right = 10;
sun.shadow.camera.top = 10; sun.shadow.camera.bottom = -10;
scene.add(sun);
scene.add(new THREE.HemisphereLight(0x8899cc,0x223344,0.8));
const gridHelper = new THREE.GridHelper(12, 24, 0x334466, 0x1a1a33);
gridHelper.position.y = -0.02;
scene.add(gridHelper);
const terrainGeo = new THREE.BufferGeometry();
const positions = new Float32Array(GRID*GRID*3);
const colors = new Float32Array(GRID*GRID*3);
const indices = [];
for(let i=0;i<GRID-1;i++){
  for(let j=0;j<GRID-1;j++){
    const a=i*GRID+j, b=a+1, c=a+GRID, d=c+1;
    indices.push(a,b,c, b,d,c);
  }
}
terrainGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
terrainGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
terrainGeo.setIndex(indices);
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors:true, roughness:0.55, metalness:0.1,
  flatShading:false, side:THREE.DoubleSide
});
const terrain = new THREE.Mesh(terrainGeo, terrainMat);
terrain.castShadow = true; terrain.receiveShadow = true;
scene.add(terrain);
let riverGroup = new THREE.Group();
scene.add(riverGroup);
let particleGroup = new THREE.Group();
scene.add(particleGroup);
const riverMat = new THREE.MeshStandardMaterial({color:0xff4444, roughness:0.3, metalness:0.2, emissive:0x330000, emissiveIntensity:0.5});
function buildRiverGeometry(errors){
  if(errors.length<2) return new THREE.BufferGeometry();
  const pts = errors.map(e=>new THREE.Vector3(e.x, e.y*1.02, e.z));
  const curve = new THREE.CatmullRomCurve3(pts, false, 'catmullrom', 0.5);
  const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.08, 6, false);
  return tubeGeo;
}
function updateTerrain(step){
  const data = getTerrainData(step);
  const {heights, users} = data;
  const posArr = terrainGeo.attributes.position.array;
  const colArr = terrainGeo.attributes.color.array;
  const hScale = parseFloat(document.getElementById('heightScale').value);
  for(let i=0;i<GRID;i++){
    for(let j=0;j<GRID;j++){
      const idx = i*GRID+j;
      const x = (i/(GRID-1)-0.5)*10;
      const z = (j/(GRID-1)-0.5)*10;
      const h = heights[idx]*hScale;
      posArr[idx*3]=x; posArr[idx*3+1]=h; posArr[idx*3+2]=z;
      const u = users[idx];
      const r=0.08+u*0.12, g=0.18+u*0.7, b=0.08+u*0.15;
      colArr[idx*3]=r; colArr[idx*3+1]=g; colArr[idx*3+2]=b;
    }
  }
  terrainGeo.attributes.position.needsUpdate = true;
  terrainGeo.attributes.color.needsUpdate = true;
  terrainGeo.computeVertexNormals();
  riverGroup.clear();
  if(riverCache.has(step)){ logCache(true); }
  else{ logCache(false); const geo = buildRiverGeometry(data.errors); riverCache.set(step, geo); }
  if(riverCache.get(step) && data.errors.length>=2){
    const rMesh = new THREE.Mesh(riverCache.get(step), riverMat);
    rMesh.renderOrder = 1; rMesh.material.depthTest = true; rMesh.material.depthWrite = true;
    riverGroup.add(rMesh);
  }
  particleGroup.clear();
  if(!particleStartCache.has(step)){ logCache(false); particleStartCache.set(step, data.apis); }
  else logCache(true);
  const apis = particleStartCache.get(step);
  const pCount = apis.length;
  const pPos = new Float32Array(pCount*3);
  const pGeo = new THREE.BufferGeometry();
  apis.forEach((a,i)=>{ pPos[i*3]=a.x; pPos[i*3+1]=0.1; pPos[i*3+2]=a.z; });
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  const pMat = new THREE.PointsMaterial({color:0xffd93d, size:0.12, blending:THREE.AdditiveBlending, depthWrite:false, transparent:true, opacity:0.8});
  particleGroup.add(new THREE.Points(pGeo, pMat));
  particleGroup.userData = {apis, pGeo, startTime:performance.now()};
}
updateTerrain(0);
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const tooltip = document.getElementById('tooltip');
let gridLookupCache = null;
let gridLookupCacheKey = '';
function memoGridLookup(worldX, worldZ){
  const key = `${worldX.toFixed(2)},${worldZ.toFixed(2)}`;
  if(key===gridLookupCacheKey && gridLookupCache) return gridLookupCache;
  const gi = Math.round((worldX/5+0.5)*(GRID-1));
  const gj = Math.round((worldZ/5+0.5)*(GRID-1));
  const clampedI = Math.max(0,Math.min(GRID-1,gi));
  const clampedJ = Math.max(0,Math.min(GRID-1,gj));
  gridLookupCacheKey = key;
  gridLookupCache = {i:clampedI, j:clampedJ};
  return gridLookupCache;
}
window.addEventListener('mousemove',(e)=>{
  mouse.x = (e.clientX/window.innerWidth)*2-1;
  mouse.y = -(e.clientY/window.innerHeight)*2+1;
  raycaster.setFromCamera(mouse, camera);
  const hits = raycaster.intersectObject(terrain);
  if(hits.length>0){
    const p = hits[0].point;
    const g = memoGridLookup(p.x, p.z);
    const idx = g.i*GRID+g.j;
    const data = getTerrainData(parseInt(document.getElementById('timeSlider').value));
    const h = data.heights[idx]*parseFloat(document.getElementById('heightScale').value);
    const u = data.users[idx];
    tooltip.style.display='block';
    tooltip.style.left = (e.clientX+15)+'px';
    tooltip.style.top = (e.clientY-10)+'px';
    tooltip.textContent = `Intäkt: ${(h*100).toFixed(0)}\nAnvändare: ${(u*100).toFixed(0)}%\nPosition: (${p.x.toFixed(1)}, ${p.z.toFixed(1)})`;
  } else {
    tooltip.style.display='none';
  }
});
document.getElementById('timeSlider').addEventListener('input', function(e){
  const v = parseInt(e.target.value);
  document.getElementById('timeLabel').textContent = MONTHS[v];
  gridLookupCache = null;
  updateTerrain(v);
});
document.getElementById('heightScale').addEventListener('input', function(e){
  document.getElementById('hScaleVal').textContent = parseFloat(e.target.value).toFixed(1)+'x';
  gridLookupCache = null;
  updateTerrain(parseInt(document.getElementById('timeSlider').value));
});
document.getElementById('autoRotate').addEventListener('change', function(e){
  controls.autoRotate = e.target.checked;
});
document.querySelectorAll('.bm-btn').forEach(btn=>{
  btn.addEventListener('click', function(){
    const idx = parseInt(this.dataset.bm);
    if(idx===3){
      bookmarks.push({pos:camera.position.clone(), target:controls.target.clone()});
      const newBtn = document.createElement('button');
      newBtn.className='bm-btn';
      newBtn.textContent = `Bokmärke ${bookmarks.length-1}`;
      newBtn.dataset.bm = bookmarks.length-1;
      newBtn.addEventListener('click', function(){
        const b = bookmarks[parseInt(this.dataset.bm)];
        controls.target.copy(b.target); camera.position.copy(b.pos); controls.update();
      });
      document.getElementById('bookmarks').appendChild(newBtn);
      return;
    }
    const b = bookmarks[idx];
    controls.target.copy(b.target);
    camera.position.copy(b.pos);
    controls.update();
  });
});
const axisLabels = document.getElementById('axis-labels');
function updateAxisLabels(){
  const w = window.innerWidth, h = window.innerHeight;
  const origin = new THREE.Vector3(0,0,0).project(camera);
  const sx = (origin.x*0.5+0.5)*w, sy = (-origin.y*0.5+0.5)*h;
  axisLabels.innerHTML = '';
  [{v:new THREE.Vector3(5,0,0),t:'Intäkt →'},{v:new THREE.Vector3(-5,0,0),t:''},{v:new THREE.Vector3(0,4,0),t:'Höjd ↑'},{v:new THREE.Vector3(0,0,5),t:'Tid →'}].forEach(l=>{
    const sp = l.v.clone().project(camera);
    const px = (sp.x*0.5+0.5)*w, py = (-sp.y*0.5+0.5)*h;
    if(sp.z<1){
      const el = document.createElement('div');
      el.style.cssText = `position:fixed;left:${px}px;top:${py}px;color:#8899aa;font-size:10px;pointer-events:none`;
      el.textContent = l.t;
      axisLabels.appendChild(el);
    }
  });
}
function animate(){
  requestAnimationFrame(animate);
  controls.update();
  updateAxisLabels();
  const pg = particleGroup;
  if(pg.userData && pg.userData.pGeo){
    const apis = pg.userData.apis;
    const posArr = pg.userData.pGeo.attributes.position.array;
    const elapsed = (performance.now()-pg.userData.startTime)*0.001;
    for(let i=0;i<apis.length;i++){
      const a = apis[i];
      const angle = Math.atan2(a.z, a.x) + elapsed*a.speed*0.6;
      const r = Math.sqrt(a.x*a.x+a.z*a.z);
      posArr[i*3] = Math.cos(angle)*r;
      posArr[i*3+2] = Math.sin(angle)*r;
      const data = getTerrainData(parseInt(document.getElementById('timeSlider').value));
      const g = memoGridLookup(posArr[i*3], posArr[i*3+2]);
      const idx = g.i*GRID+g.j;
      posArr[i*3+1] = (data.heights[idx]||0.05)*parseFloat(document.getElementById('heightScale').value)+0.15;
    }
    pg.userData.pGeo.attributes.position.needsUpdate = true;
  }
  renderer.render(scene, camera);
}
animate();
window.addEventListener('resize',()=>{
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  gridLookupCache = null;
});
</script>
</body>
</html>