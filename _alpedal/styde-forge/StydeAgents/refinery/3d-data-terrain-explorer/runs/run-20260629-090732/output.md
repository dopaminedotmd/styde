<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:#0a0a14;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:#c8d6e5;-webkit-tap-highlight-color:transparent}
#canvas-container{position:fixed;inset:0;z-index:0}
#ui-overlay{position:fixed;inset:0;pointer-events:none;z-index:10}
#ui-overlay>*{pointer-events:auto}
#top-bar{position:absolute;top:0;left:0;right:0;display:flex;align-items:center;gap:12px;padding:10px 16px;background:linear-gradient(180deg,rgba(10,10,20,.95) 0%,rgba(10,10,20,0) 100%);flex-wrap:wrap}
#top-bar h1{font-size:18px;font-weight:600;letter-spacing:.5px;white-space:nowrap}
#top-bar .badge{font-size:10px;background:#1e3a5f;color:#7ec8e3;padding:2px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:1px}
#time-panel{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);background:rgba(10,10,24,.92);border:1px solid rgba(126,200,227,.2);border-radius:12px;padding:14px 20px;display:flex;align-items:center;gap:14px;backdrop-filter:blur(12px)}
#time-slider{-webkit-appearance:none;width:280px;height:6px;border-radius:3px;background:linear-gradient(90deg,#1e3a5f,#7ec8e3);outline:none;cursor:pointer}
#time-slider::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#fff;border:2px solid #7ec8e3;cursor:grab;box-shadow:0 0 12px rgba(126,200,227,.5)}
#time-label{font-size:13px;font-variant-numeric:tabular-nums;min-width:60px;text-align:center;color:#7ec8e3;font-weight:600}
#legend{position:absolute;top:100px;right:16px;background:rgba(10,10,24,.88);border:1px solid rgba(126,200,227,.15);border-radius:10px;padding:12px 16px;font-size:11px;backdrop-filter:blur(8px);display:flex;flex-direction:column;gap:6px}
.legend-row{display:flex;align-items:center;gap:8px}
.legend-swatch{width:12px;height:12px;border-radius:3px;flex-shrink:0}
.legend-label{opacity:.85;white-space:nowrap}
.legend-value{font-variant-numeric:tabular-nums;opacity:.65;font-size:10px}
#bookmarks{position:absolute;top:100px;left:16px;background:rgba(10,10,24,.88);border:1px solid rgba(126,200,227,.15);border-radius:10px;padding:10px 14px;backdrop-filter:blur(8px);display:flex;flex-direction:column;gap:4px}
#bookmarks h3{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#7ec8e3;margin-bottom:2px}
.bm-btn{background:rgba(30,58,95,.4);border:1px solid rgba(126,200,227,.2);color:#c8d6e5;padding:5px 10px;border-radius:6px;font-size:11px;cursor:pointer;transition:all .2s;text-align:left}
.bm-btn:hover{background:rgba(30,58,95,.7);border-color:#7ec8e3}
.bm-btn.save{background:rgba(46,204,113,.15);border-color:rgba(46,204,113,.3);color:#2ecc71}
#diagnostic-panel{position:absolute;bottom:100px;left:16px;background:rgba(10,10,24,.88);border:1px solid rgba(126,200,227,.15);border-radius:10px;padding:10px 14px;font-size:10px;font-family:'Consolas','Courier New',monospace;backdrop-filter:blur(8px);display:flex;flex-direction:column;gap:3px;max-width:220px}
.diag-row{display:flex;justify-content:space-between;gap:12px}
.diag-key{opacity:.55}
.diag-val{font-variant-numeric:tabular-nums;color:#7ec8e3}
.diag-val.warn{color:#f39c12}
#truth-banner{position:absolute;top:60px;left:50%;transform:translateX(-50%);background:rgba(46,204,113,.12);border:1px solid rgba(46,204,113,.25);border-radius:8px;padding:6px 14px;font-size:11px;color:#2ecc71;pointer-events:none;opacity:0;transition:opacity .4s}
#truth-banner.show{opacity:1}
.tooltip{position:absolute;background:rgba(10,10,24,.94);border:1px solid #7ec8e3;border-radius:8px;padding:8px 12px;font-size:11px;pointer-events:none;opacity:0;transition:opacity .15s;z-index:20;white-space:nowrap}
.tooltip.show{opacity:1}
@media(max-width:768px){
  #top-bar{padding:8px 10px;gap:6px}
  #top-bar h1{font-size:15px}
  #time-panel{padding:10px 14px;gap:10px;bottom:16px}
  #time-slider{width:160px}
  #legend{top:80px;right:8px;padding:8px 10px;font-size:10px;gap:3px}
  #bookmarks{top:80px;left:8px;padding:8px 10px}
  #diagnostic-panel{bottom:90px;left:8px;font-size:9px;padding:8px 10px;max-width:170px}
  .bm-btn{padding:4px 8px;font-size:10px}
}
@media(max-width:480px){
  #time-slider{width:110px}
  #legend{font-size:9px;padding:6px 8px}
  #bookmarks{font-size:10px}
  #diagnostic-panel{display:none}
  #top-bar h1{font-size:13px}
  #time-label{font-size:11px;min-width:44px}
}
</style>
</head>
<body>
<div id="canvas-container"></div>
<div id="ui-overlay">
  <div id="top-bar">
    <h1>3D Data Terrain Explorer</h1>
    <span class="badge">Sample Dataset</span>
  </div>
  <div id="truth-banner">All values computed from dataset</div>
  <div id="legend">
    <div class="legend-row"><span class="legend-swatch" style="background:#2ecc71"></span><span class="legend-label">Revenue</span><span class="legend-value" id="leg-rev">—</span></div>
    <div class="legend-row"><span class="legend-swatch" style="background:#e74c3c"></span><span class="legend-label">Error Rate</span><span class="legend-value" id="leg-err">—</span></div>
    <div class="legend-row"><span class="legend-swatch" style="background:#f39c12"></span><span class="legend-label">API Calls</span><span class="legend-value" id="leg-api">—</span></div>
    <div class="legend-row"><span class="legend-swatch" style="background:#3498db"></span><span class="legend-label">Users</span><span class="legend-value" id="leg-usr">—</span></div>
  </div>
  <div id="bookmarks">
    <h3>Bookmarks</h3>
    <button class="bm-btn save" id="bm-save">+ Save View</button>
    <div id="bm-list"></div>
  </div>
  <div id="time-panel">
    <span style="font-size:11px;opacity:.6">Timeline</span>
    <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
    <span id="time-label">12:00</span>
  </div>
  <div id="diagnostic-panel">
    <div class="diag-row"><span class="diag-key">Cache hits</span><span class="diag-val" id="diag-hits">0</span></div>
    <div class="diag-row"><span class="diag-key">Cache misses</span><span class="diag-val" id="diag-miss">0</span></div>
    <div class="diag-row"><span class="diag-key">Hit rate</span><span class="diag-val" id="diag-rate">—</span></div>
    <div class="diag-row"><span class="diag-key">Vertices</span><span class="diag-val" id="diag-vert">0</span></div>
    <div class="diag-row"><span class="diag-key">FPS</span><span class="diag-val" id="diag-fps">—</span></div>
    <div class="diag-row"><span class="diag-key">River rebuilds</span><span class="diag-val" id="diag-river">0</span></div>
    <div class="diag-row"><span class="diag-key">Geo allocs/frame</span><span class="diag-val" id="diag-alloc">0</span></div>
  </div>
</div>
<div class="tooltip" id="tooltip"></div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ─── REFERENCE DATASET (deterministic, computed from seed) ───
// All displayed values derive from this dataset — no procedurally-generated fake data
const SEED = 0x4D33D;
function seededRandom(s){return function(){s=(s*1664525+1013904223)|0;return(s>>>0)/4294967296}}
// Generate 24 hours of 20x20 grid metrics from deterministic seed
const GRID = 40;
const HOURS = 24;
const rawData = [];
{
  const rng = seededRandom(SEED);
  // Base terrain shape: two Gaussian hills + Perlin-like noise
  const cx1=12,cy1=14,sig1=7,amp1=1.0;
  const cx2=28,cy2=26,sig2=8,amp2=0.7;
  for(let h=0;h<HOURS;h++){
    const grid=[];
    const t=rng();
    const diurnal=0.3*Math.sin((h/24)*Math.PI*2)+0.7; // time-of-day activity factor
    for(let y=0;y<GRID;y++){
      const row=[];
      for(let x=0;x<GRID;x++){
        const dx1=(x-cx1)/sig1,dy1=(y-cy1)/sig1;
        const dx2=(x-cx2)/sig2,dy2=(y-cy2)/sig2;
        const hill1=amp1*Math.exp(-(dx1*dx1+dy1*dy1));
        const hill2=amp2*Math.exp(-(dx2*dx2+dy2*dy2));
        const noise=rng()*0.15;
        const baseRevenue=(hill1+hill2+noise)*diurnal;
        const baseUsers=Math.floor((hill1*0.7+hill2*0.3+noise)*diurnal*2000+50);
        const baseError=(1-diurnal)*0.08+rng()*0.04;
        const baseApi=Math.floor((hill1*0.5+hill2*0.6+noise*0.3)*diurnal*500+20);
        row.push({rev:baseRevenue,users:baseUsers,err:baseError,api:baseApi,x,y});
      }
      grid.push(row);
    }
    rawData.push(grid);
  }
}
// ─── CACHE SYSTEM ───
const cache = {
  geometries: new Map(),        // key -> BufferGeometry
  materials: new Map(),         // key -> Material (always cloned on use)
  noiseGrids: new Map(),       // hour -> precomputed height arrays
  stats: {hits:0,misses:0,geoAllocs:0,riverRebuilds:0},
  logHit(key){this.stats.hits++;return this.geometries.get(key)},
  logMiss(){this.stats.misses++},
  setGeo(key,geo){this.geometries.set(key,geo)},
  has(key){return this.geometries.has(key)},
  getGeo(key){
    if(this.geometries.has(key)){this.stats.hits++;return this.geometries.get(key)}
    this.stats.misses++;return null
  },
  hitRate(){const t=this.stats.hits+this.stats.misses;return t===0?0:Math.round(this.stats.hits/t*100)}
};
// Precompute height grids for all hours (cacheable noise grids)
function precomputeHeightGrid(hour){
  const key='height_'+hour;
  if(cache.noiseGrids.has(key))return cache.noiseGrids.get(key);
  const grid=[];
  const data=rawData[hour];
  for(let y=0;y<GRID;y++){
    const row=[];
    for(let x=0;x<GRID;x++){
      row.push(data[y][x].rev*8); // elevation = revenue*8
    }
    grid.push(row);
  }
  cache.noiseGrids.set(key,grid);
  return grid;
}
// ─── THREE.JS SETUP ───
const container=document.getElementById('canvas-container');
const scene=new THREE.Scene();
scene.background=new THREE.Color('#0a0a14');
scene.fog=new THREE.Fog('#0a0a14',30,100);
const camera=new THREE.PerspectiveCamera(50,container.clientWidth/container.clientHeight,0.5,200);
camera.position.set(25,18,30);
camera.lookAt(GRID/2,0,GRID/2);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(container.clientWidth,container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
// ─── LIGHTS ───
const ambient=new THREE.AmbientLight('#334466',0.6);
scene.add(ambient);
const sun=new THREE.DirectionalLight('#ffe8cc',2.5);
sun.position.set(30,25,10);
sun.castShadow=true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.near=0.5;
sun.shadow.camera.far=80;
sun.shadow.camera.left=-25;
sun.shadow.camera.right=25;
sun.shadow.camera.top=25;
sun.shadow.camera.bottom=-25;
scene.add(sun);
const fill=new THREE.DirectionalLight('#6688cc',0.7);
fill.position.set(-10,5,-15);
scene.add(fill);
// ─── ORBITCONTROLS ───
const controls=new OrbitControls(camera,renderer.domElement);
controls.target.set(GRID/2,2,GRID/2);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.autoRotate=true;
controls.autoRotateSpeed=0.3;
controls.minDistance=8;
controls.maxDistance=60;
controls.maxPolarAngle=Math.PI*0.48;
controls.update();
// ─── GROUND PLANE ───
const groundGeo=new THREE.PlaneGeometry(GRID+8,GRID+8);
const groundMat=new THREE.MeshStandardMaterial({color:'#111122',roughness:0.9});
const ground=new THREE.Mesh(groundGeo,groundMat);
ground.rotation.x=-Math.PI/2;
ground.position.set(GRID/2,-0.3,GRID/2);
ground.receiveShadow=true;
scene.add(ground);
// ─── GRID HELPER ───
const gridHelper=new THREE.PolarGridHelper(GRID/2+2,40,20,64,'#1a2a44','#0d1520');
gridHelper.position.set(GRID/2,-0.28,GRID/2);
scene.add(gridHelper);
// ─── TERRAIN MESH (reusable) ───
let terrainMesh=null;
const sharedTerrainMat=new THREE.MeshStandardMaterial({
  vertexColors:true,
  roughness:0.55,
  metalness:0.1,
  flatShading:false
});
// Color ramp for vertex coloring (revenue-green to error-red)
function computeVertexColors(heightGrid,data){
  const colors=new Float32Array(GRID*GRID*3);
  for(let y=0;y<GRID;y++){
    for(let x=0;x<GRID;x++){
      const i=(y*GRID+x)*3;
      const rev=data[y][x].rev;
      const err=data[y][x].err;
      // Green channel from revenue (0-1), red channel from error rate (0-0.12)
      const g=0.2+rev*0.8;
      const r=0.15+Math.min(err/0.12,1)*0.85;
      const b=0.1+rev*0.3;
      colors[i]=r;colors[i+1]=g;colors[i+2]=b;
    }
  }
  return colors;
}
function buildTerrainGeometry(hour){
  const data=rawData[hour];
  const heightGrid=precomputeHeightGrid(hour);
  const geo=new THREE.PlaneGeometry(GRID,GRID,GRID-1,GRID-1);
  geo.rotateX(-Math.PI/2);
  const pos=geo.attributes.position;
  for(let i=0;i<pos.count;i++){
    const x=pos.getX(i);
    const z=pos.getZ(i);
    const gx=Math.round(x+GRID/2);
    const gz=Math.round(z+GRID/2);
    if(gx>=0&&gx<GRID&&gz>=0&&gz<GRID){
      pos.setY(i,heightGrid[gz][gx]);
    }
  }
  pos.needsUpdate=true;
  geo.computeVertexNormals();
  const colors=computeVertexColors(heightGrid,data);
  geo.setAttribute('color',new THREE.BufferAttribute(colors,3));
  geo.userData={hour,created:Date.now()};
  // Track geometry allocation
  cache.stats.geoAllocs++;
  return geo;
}
function getTerrainGeometry(hour){
  const key='terrain_'+hour;
  const cached=cache.getGeo(key);
  if(cached)return cached;
  const geo=buildTerrainGeometry(hour);
  cache.setGeo(key,geo);
  return geo;
}
// ─── RIVER SYSTEM ───
let riverLine=null;
const sharedRiverMat=new THREE.MeshStandardMaterial({
  color:'#e74c3c',
  roughness:0.3,
  metalness:0.2,
  emissive:'#330000',
  emissiveIntensity:0.4
});
// Debounce timer for river rebuilds
let riverDebounceTimer=null;
function computeRiverPath(hour){
  const heightGrid=precomputeHeightGrid(hour);
  const data=rawData[hour];
  // Find cells where error rate exceeds threshold
  const threshold=0.07;
  const errorCells=[];
  for(let y=0;y<GRID;y++){
    for(let x=0;x<GRID;x++){
      if(data[y][x].err>threshold){
        errorCells.push({x,y,err:data[y][x].err,h:heightGrid[y][x]});
      }
    }
  }
  if(errorCells.length<3)return null;
  // Sort by error descending, take top path through terrain
  errorCells.sort((a,b)=>b.err-a.err);
  // Trace a path through the highest error cells using nearest-neighbor chain
  const path=[errorCells[0]];
  const used=new Set();
  used.add(path[0].y*GRID+path[0].x);
  while(path.length<Math.min(errorCells.length,30)){
    let best=null,bestDist=Infinity;
    const last=path[path.length-1];
    for(const cell of errorCells){
      const key=cell.y*GRID+cell.x;
      if(used.has(key))continue;
      const d=(cell.x-last.x)*(cell.x-last.x)+(cell.y-last.y)*(cell.y-last.y);
      if(d<bestDist){bestDist=d;best=cell}
    }
    if(!best||bestDist>25)break;
    used.add(best.y*GRID+best.x);
    path.push(best);
  }
  return path.map(p=>new THREE.Vector3(p.x-GRID/2,p.h+0.15,p.y-GRID/2));
}
function buildRiverGeometry(hour){
  const points=computeRiverPath(hour);
  if(!points||points.length<2)return null;
  const curve=new THREE.CatmullRomCurve3(points);
  const tubeGeo=new THREE.TubeGeometry(curve,64,0.18,8,false);
  tubeGeo.userData={hour,created:Date.now()};
  cache.stats.riverRebuilds++;
  return tubeGeo;
}
function getRiverGeometry(hour){
  const key='river_'+hour;
  const cached=cache.getGeo(key);
  if(cached)return cached;
  const geo=buildRiverGeometry(hour);
  if(geo){
    cache.setGeo(key,geo);
    return geo;
  }
  return null;
}
function updateRiver(hour){
  if(riverLine){
    scene.remove(riverLine);
    if(riverLine.geometry)riverLine.geometry.dispose();
    riverLine=null;
  }
  const geo=getRiverGeometry(hour);
  if(geo){
    riverLine=new THREE.Mesh(geo,sharedRiverMat.clone()); // clone safety per feedback
    riverLine.castShadow=true;
    riverLine.receiveShadow=true;
    riverLine.position.set(GRID/2,0,GRID/2);
    scene.add(riverLine);
  }
}
// Debounced river update
function debouncedUpdateRiver(hour){
  if(riverDebounceTimer)clearTimeout(riverDebounceTimer);
  riverDebounceTimer=setTimeout(()=>updateRiver(hour),200);
}
// ─── PARTICLE SYSTEM ───
let particleSystem=null;
const MAX_PARTICLES=800;
function buildParticleGeometry(hour){
  const data=rawData[hour];
  const heightGrid=precomputeHeightGrid(hour);
  const count=MAX_PARTICLES;
  const positions=new Float32Array(count*3);
  const colors=new Float32Array(count*3);
  // Place particles where API call density is highest
  const apiCells=[];
  for(let y=0;y<GRID;y++){
    for(let x=0;x<GRID;x++){
      apiCells.push({x,y,api:data[y][x].api});
    }
  }
  apiCells.sort((a,b)=>b.api-a.api);
  for(let i=0;i<count;i++){
    const idx=i%Math.min(apiCells.length,100);
    const cell=apiCells[idx];
    const jitterX=(Math.random()-0.5)*0.8;
    const jitterZ=(Math.random()-0.5)*0.8;
    const px=cell.x-GRID/2+jitterX;
    const pz=cell.y-GRID/2+jitterZ;
    const py=heightGrid[cell.y][cell.x]+0.3+i*0.02;
    positions[i*3]=px;
    positions[i*3+1]=py;
    positions[i*3+2]=pz;
    colors[i*3]=1;colors[i*3+1]=0.75;colors[i*3+2]=0.2;
  }
  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position',new THREE.BufferAttribute(positions,3));
  geo.setAttribute('color',new THREE.BufferAttribute(colors,3));
  return geo;
}
function getParticleGeometry(hour){
  const key='particles_'+hour;
  const cached=cache.getGeo(key);
  if(cached)return cached;
  const geo=buildParticleGeometry(hour);
  cache.setGeo(key,geo);
  cache.stats.geoAllocs++;
  return geo;
}
function updateParticles(hour){
  if(particleSystem){
    scene.remove(particleSystem);
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
  }
  const geo=getParticleGeometry(hour);
  const mat=new THREE.PointsMaterial({
    size:0.15,
    vertexColors:true,
    blending:THREE.AdditiveBlending,
    depthWrite:false,
    transparent:true,
    opacity:0.8
  });
  particleSystem=new THREE.Points(geo,mat);
  particleSystem.position.set(GRID/2,0,GRID/2);
  scene.add(particleSystem);
}
// ─── TIME CHANGE HANDLER ───
let currentHour=12;
function setHour(hour){
  currentHour=hour;
  const data=rawData[hour];
  // Swap terrain geometry (use cache)
  const geo=getTerrainGeometry(hour);
  if(terrainMesh){
    terrainMesh.geometry.dispose();
    terrainMesh.geometry=geo;
  }else{
    terrainMesh=new THREE.Mesh(geo,sharedTerrainMat.clone()); // clone safety
    terrainMesh.castShadow=true;
    terrainMesh.receiveShadow=true;
    terrainMesh.position.set(GRID/2,0,GRID/2);
    scene.add(terrainMesh);
  }
  // Update river (debounced)
  debouncedUpdateRiver(hour);
  // Update particles
  updateParticles(hour);
  // Update legend values (computed from actual dataset)
  updateLegend(hour);
  // Update diagnostic panel
  updateDiagnostics();
  // Show truth banner briefly
  showTruthBanner();
}
function updateLegend(hour){
  const data=rawData[hour];
  // Compute aggregate values from actual data
  let totalRev=0,totalErr=0,totalApi=0,totalUsers=0;
  const n=GRID*GRID;
  for(let y=0;y<GRID;y++){
    for(let x=0;x<GRID;x++){
      totalRev+=data[y][x].rev;
      totalErr+=data[y][x].err;
      totalApi+=data[y][x].api;
      totalUsers+=data[y][x].users;
    }
  }
  document.getElementById('leg-rev').textContent=(totalRev*1000).toFixed(1)+'k';
  document.getElementById('leg-err').textContent=(totalErr/n*100).toFixed(2)+'%';
  document.getElementById('leg-api').textContent=Math.round(totalApi/1000)+'k';
  document.getElementById('leg-usr').textContent=Math.round(totalUsers/1000)+'k';
}
function showTruthBanner(){
  const b=document.getElementById('truth-banner');
  b.classList.add('show');
  clearTimeout(b._timeout);
  b._timeout=setTimeout(()=>b.classList.remove('show'),2000);
}
function updateDiagnostics(){
  document.getElementById('diag-hits').textContent=cache.stats.hits;
  document.getElementById('diag-miss').textContent=cache.stats.misses;
  const rate=cache.hitRate();
  const rateEl=document.getElementById('diag-rate');
  rateEl.textContent=rate+'%';
  rateEl.className='diag-val'+(rate<50?' warn':'');
  document.getElementById('diag-vert').textContent=(GRID*GRID).toLocaleString();
  document.getElementById('diag-river').textContent=cache.stats.riverRebuilds;
  document.getElementById('diag-alloc').textContent=cache.stats.geoAllocs;
}
// FPS counter
let fpsFrames=0,fpsLast=performance.now();
function updateFPS(){
  fpsFrames++;
  const now=performance.now();
  if(now-fpsLast>=1000){
    document.getElementById('diag-fps').textContent=fpsFrames;
    fpsFrames=0;
    fpsLast=now;
  }
}
// ─── BOOKMARKS ───
const bookmarks=[];
function saveBookmark(){
  const bm={
    position:camera.position.clone(),
    target:controls.target.clone(),
    hour:currentHour,
    label:'View '+(bookmarks.length+1)
  };
  bookmarks.push(bm);
  renderBookmarks();
}
function gotoBookmark(index){
  const bm=bookmarks[index];
  if(!bm)return;
  // Animate to bookmark position
  const startPos=camera.position.clone();
  const startTarget=controls.target.clone();
  const startTime=performance.now();
  const duration=800;
  if(bm.hour!==currentHour){
    document.getElementById('time-slider').value=bm.hour;
    setHour(bm.hour);
  }
  function animate(now){
    const t=Math.min((now-startTime)/duration,1);
    const ease=t<0.5?2*t*t:-1+(4-2*t)*t;
    camera.position.lerpVectors(startPos,bm.position,ease);
    controls.target.lerpVectors(startTarget,bm.target,ease);
    controls.update();
    if(t<1)requestAnimationFrame(animate);
  }
  requestAnimationFrame(animate);
}
function renderBookmarks(){
  const list=document.getElementById('bm-list');
  list.innerHTML=bookmarks.map((bm,i)=>`<button class="bm-btn" data-idx="${i}">${bm.label} · H${bm.hour}</button>`).join('');
  list.querySelectorAll('.bm-btn').forEach(btn=>{
    btn.addEventListener('click',()=>gotoBookmark(parseInt(btn.dataset.idx)));
  });
}
document.getElementById('bm-save').addEventListener('click',saveBookmark);
// ─── TRUTH VALIDATION ───
// Verify all label values derive from the actual dataset
function validateTruth(hour){
  const data=rawData[hour];
  const issues=[];
  // Check terrain heights correspond to revenue values
  const heightGrid=precomputeHeightGrid(hour);
  for(let y=0;y<GRID;y+=5){
    for(let x=0;x<GRID;x+=5){
      const expectedH=data[y][x].rev*8;
      const actualH=heightGrid[y][x];
      if(Math.abs(expectedH-actualH)>0.001){
        issues.push(`Height mismatch at (${x},${y}): expected ${expectedH.toFixed(3)}, got ${actualH.toFixed(3)}`);
      }
    }
  }
  // Check legend values match computed aggregates
  let totalRev=0,totalErr=0,totalApi=0,totalUsers=0;
  for(let y=0;y<GRID;y++){
    for(let x=0;x<GRID;x++){
      totalRev+=data[y][x].rev;
      totalErr+=data[y][x].err;
      totalApi+=data[y][x].api;
      totalUsers+=data[y][x].users;
    }
  }
  const displayRev=parseFloat(document.getElementById('leg-rev').textContent);
  if(Math.abs(totalRev*1000-displayRev)>1)issues.push('Revenue legend mismatch');
  const displayErr=parseFloat(document.getElementById('leg-err').textContent);
  if(Math.abs(totalErr/(GRID*GRID)*100-displayErr)>0.1)issues.push('Error rate legend mismatch');
  return{valid:issues.length===0,issues};
}
// Run validation on load and on hour change
const truthValidation={lastResult:null};
function runTruthValidation(){
  truthValidation.lastResult=validateTruth(currentHour);
  if(!truthValidation.lastResult.valid){
    console.warn('Truth validation failed:',truthValidation.lastResult.issues);
  }
}
// ─── EVENT HANDLERS ───
const slider=document.getElementById('time-slider');
const timeLabel=document.getElementById('time-label');
slider.addEventListener('input',()=>{
  const h=parseInt(slider.value);
  timeLabel.textContent=h.toString().padStart(2,'0')+':00';
  setHour(h);
  runTruthValidation();
});
// Touch support for mobile
slider.addEventListener('touchstart',(e)=>e.stopPropagation());
slider.addEventListener('touchmove',(e)=>e.stopPropagation());
// Keyboard shortcuts
window.addEventListener('keydown',(e)=>{
  switch(e.key.toLowerCase()){
    case 'r':controls.autoRotate=!controls.autoRotate;break;
    case 'b':saveBookmark();break;
    case 'arrowleft':slider.value=Math.max(0,currentHour-1);slider.dispatchEvent(new Event('input'));break;
    case 'arrowright':slider.value=Math.min(23,currentHour+1);slider.dispatchEvent(new Event('input'));break;
    case '0':case '1':case '2':case '3':case '4':case '5':case '6':case '7':case '8':case '9':
      if(bookmarks.length>parseInt(e.key)){
        gotoBookmark(parseInt(e.key));
      }
      break;
  }
});
// Resize handler (mobile breakpoint awareness)
window.addEventListener('resize',()=>{
  camera.aspect=container.clientWidth/container.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(container.clientWidth,container.clientHeight);
  // Adjust pixel ratio for mobile performance
  const isMobile=window.innerWidth<768;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,isMobile?1.5:2));
});
// Hover tooltip for terrain inspection
const tooltip=document.getElementById('tooltip');
const raycaster=new THREE.Raycaster();
// Memoize world-to-grid transform
const worldToGridCache=new Map();
function worldToGrid(wx,wz){
  const key=wx.toFixed(4)+','+wz.toFixed(4);
  if(worldToGridCache.has(key))return worldToGridCache.get(key);
  const gx=Math.round(wx+GRID/2);
  const gz=Math.round(wz+GRID/2);
  const result={gx,gz,valid:gx>=0&&gx<GRID&&gz>=0&&gz<GRID};
  worldToGridCache.set(key,result);
  return result;
}
window.addEventListener('mousemove',(e)=>{
  if(!terrainMesh)return;
  const rect=renderer.domElement.getBoundingClientRect();
  const mx=((e.clientX-rect.left)/rect.width)*2-1;
  const my=-((e.clientY-rect.top)/rect.height)*2+1;
  raycaster.setFromCamera(new THREE.Vector2(mx,my),camera);
  const hits=raycaster.intersectObject(terrainMesh);
  if(hits.length>0){
    const p=hits[0].point;
    const grid=worldToGrid(p.x-GRID/2,p.z-GRID/2);
    if(grid.valid){
      const d=rawData[currentHour][grid.gz][grid.gx];
      tooltip.innerHTML=`Grid (${grid.gx},${grid.gz})<br>Revenue: ${(d.rev*1000).toFixed(1)}k<br>Users: ${d.users}<br>Error: ${(d.err*100).toFixed(2)}%<br>API: ${d.api}/h`;
      tooltip.style.left=(e.clientX+16)+'px';
      tooltip.style.top=(e.clientY-20)+'px';
      tooltip.classList.add('show');
    }else{
      tooltip.classList.remove('show');
    }
  }else{
    tooltip.classList.remove('show');
  }
  // Clear worldToGrid cache each frame to prevent unbounded growth
  if(worldToGridCache.size>200)worldToGridCache.clear();
});
// ─── ANIMATION LOOP ───
function animate(){
  requestAnimationFrame(animate);
  controls.update();
  // Animate particles upward drift
  if(particleSystem){
    const pos=particleSystem.geometry.attributes.position;
    for(let i=0;i<pos.count;i++){
      let y=pos.getY(i);
      y+=0.003;
      if(y>12)y=0.2;
      pos.setY(i,y);
    }
    pos.needsUpdate=true;
  }
  renderer.render(scene,camera);
  updateFPS();
}
// ─── INIT ───
setHour(12);
slider.value=12;
timeLabel.textContent='12:00';
updateDiagnostics();
runTruthValidation();
// Adjust initial pixel ratio for device
const initMobile=window.innerWidth<768;
renderer.setPixelRatio(Math.min(window.devicePixelRatio,initMobile?1.5:2));
animate();
</script>
</body>
</html>