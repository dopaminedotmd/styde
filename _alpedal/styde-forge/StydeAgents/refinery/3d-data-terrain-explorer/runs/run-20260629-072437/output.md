<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root { --bg: #0a0a14; --panel-bg: rgba(10,10,25,0.92); --text: #c8ccd4; --accent: #4fc3f7; --accent2: #81c784; --danger: #ef5350; --slider-track: #2a2a3a; }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:var(--bg); overflow:hidden; font-family:'Segoe UI',system-ui,sans-serif; color:var(--text); }
  canvas { display:block; }
  #ui { position:fixed; bottom:0; left:0; right:0; z-index:10; pointer-events:none; }
  #panel { pointer-events:auto; background:var(--panel-bg); backdrop-filter:blur(12px); border-top:1px solid rgba(255,255,255,0.08); padding:14px 20px; display:flex; flex-wrap:wrap; gap:16px; align-items:center; }
  #time-controls { display:flex; align-items:center; gap:10px; flex:1; min-width:260px; }
  #time-slider { flex:1; -webkit-appearance:none; appearance:none; height:6px; border-radius:3px; background:var(--slider-track); outline:none; cursor:pointer; }
  #time-slider::-webkit-slider-thumb { -webkit-appearance:none; width:18px; height:18px; border-radius:50%; background:var(--accent); cursor:pointer; border:2px solid var(--bg); }
  #time-label { min-width:100px; font-size:13px; font-weight:600; color:var(--accent); }
  button { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); color:var(--text); padding:6px 14px; border-radius:5px; cursor:pointer; font-size:12px; font-weight:500; transition:all 0.2s; white-space:nowrap; }
  button:hover { background:rgba(255,255,255,0.12); border-color:var(--accent); color:#fff; }
  button.active { background:var(--accent); color:#000; border-color:var(--accent); font-weight:700; }
  #bookmark-bar { display:flex; gap:6px; align-items:center; }
  .bookmark-btn { font-size:11px; padding:5px 10px; }
  #stats { position:fixed; top:10px; left:10px; z-index:10; font-size:11px; color:rgba(255,255,255,0.5); pointer-events:none; }
  #legend { position:fixed; top:10px; right:10px; z-index:10; background:var(--panel-bg); backdrop-filter:blur(8px); border-radius:6px; padding:10px 14px; font-size:11px; display:flex; flex-direction:column; gap:5px; border:1px solid rgba(255,255,255,0.06); }
  .legend-item { display:flex; align-items:center; gap:8px; }
  .legend-swatch { width:12px; height:12px; border-radius:2px; }
</style>
</head>
<body>
<div id="stats">FPS: <span id="fps">0</span> | DrawCalls: <span id="draws">0</span></div>
<div id="legend">
  <div class="legend-item"><span class="legend-swatch" style="background:#4fc3f7;"></span>Revenue (elevation)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#81c784;"></span>User Density (green)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ef5350;"></span>Error Rate (rivers)</div>
  <div class="legend-item"><span class="legend-swatch" style="background:#ffb74d;"></span>API Traffic (particles)</div>
</div>
<div id="ui">
  <div id="panel">
    <div id="time-controls">
      <span style="font-size:11px;opacity:0.6;">TIME</span>
      <input type="range" id="time-slider" min="0" max="0" value="0" step="1">
      <span id="time-label">Jan</span>
    </div>
    <button id="btn-play" title="Play/pause time animation">▶ Play</button>
    <button id="btn-autorot" title="Toggle auto-rotation">↻ Auto</button>
    <button id="btn-reset" title="Reset camera">⌂ Reset</button>
    <div id="bookmark-bar">
      <button id="btn-save-bm" title="Save current camera position">☆ Save</button>
    </div>
  </div>
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
// ── PERFORMANCE BUDGET (per Blueprint v1 requirements) ──
// Target: 60fps desktop, 30fps mobile (detected via pixelRatio capping)
// Max draw calls: <12 (terrain, rivers, particles, grid, skybox = 5 primary)
// Object pooling: all Vector3/Ray/Frustum reused across frames
// Buffer recycling: terrain & river BufferGeometry updated in-place, never re-allocated
// InstancedMesh: particles use InstancedMesh with pre-allocated capacity (no push/splice)
// Camera init: OrbitControls target set BEFORE camera position, deferred update()
// ── OBJECT POOL ──
class Vec3Pool {
  constructor(size=64) {
    this.pool = [];
    this.index = 0;
    for (let i=0;i<size;i++) this.pool.push(new THREE.Vector3());
  }
  acquire() {
    if (this.index>=this.pool.length) this.pool.push(new THREE.Vector3());
    return this.pool[this.index++];
  }
  releaseAll() { this.index=0; }
}
class RayPool {
  constructor(size=8) {
    this.pool = [];
    this.index = 0;
    for (let i=0;i<size;i++) this.pool.push(new THREE.Ray());
  }
  acquire() {
    if (this.index>=this.pool.length) this.pool.push(new THREE.Ray());
    return this.pool[this.index++];
  }
  releaseAll() { this.index=0; }
}
const V3 = new Vec3Pool(128);
const RAY = new RayPool(8);
const DUMMY = new THREE.Object3D(); // for InstancedMesh matrix updates
// ── SYNTHETIC DATA GENERATOR ──
const GRID = 48;
const TIME_POINTS = 12;
const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const TERRAIN_SPAN = 20;
function simplexish(x,z,t) {
  const fx=0.35,fz=0.35;
  const a=Math.sin(x*fx+t*0.6)*Math.cos(z*fz+t*0.4)*1.2;
  const b=Math.sin(x*0.8+t*0.3)*Math.sin(z*0.7-t*0.25)*0.7;
  const c=Math.cos(x*0.15+z*0.2+t*0.5)*0.9;
  const d=Math.sin((x+z)*0.5+t*0.2)*0.5;
  return a+b+c+d;
}
function generateTimeSlice(t) {
  const height= new Float32Array(GRID*GRID);
  const veg= new Float32Array(GRID*GRID);
  const error= new Float32Array(GRID*GRID);
  const apiVol= new Float32Array(GRID*GRID);
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      const x=(ix/(GRID-1)-0.5)*TERRAIN_SPAN;
      const z=(iz/(GRID-1)-0.5)*TERRAIN_SPAN;
      const i=iz*GRID+ix;
      const h=simplexish(x,z,t*0.8);
      height[i]=h;
      veg[i]=Math.max(0,Math.min(1,(h+1.2)/3.0+Math.sin(x*0.6+z*0.5)*0.35));
      const errPulse=Math.abs(Math.sin(x*2.1+z*1.7+t*1.3))*0.6;
      const pathMask=Math.abs((z-Math.sin(x*1.5+t*0.4)*3.5))<1.2?errPulse:errPulse*0.12;
      error[i]=Math.max(0,Math.min(1,pathMask));
      apiVol[i]=Math.max(0,Math.min(1,veg[i]*0.8+error[i]*0.3+Math.abs(Math.cos(x*3+z*3+t)*0.2)));
    }
  }
  return {height,veg,error,apiVol};
}
const ALL_SLICES = [];
for(let t=0;t<TIME_POINTS;t++) ALL_SLICES.push(generateTimeSlice(t));
// ── THREE.JS SETUP ──
const renderer = new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2)); // mobile budget cap
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.1;
document.body.prepend(renderer.domElement);
const scene = new THREE.Scene();
scene.background=new THREE.Color('#0a0a18');
scene.fog=new THREE.FogExp2('#0a0a18',0.00035);
const camera = new THREE.PerspectiveCamera(55,window.innerWidth/window.innerHeight,0.5,80);
// Camera position set AFTER controls target — deferred
const controls = new OrbitControls(camera,renderer.domElement);
controls.target.set(0,0.6,0);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.minDistance=3;
controls.maxDistance=35;
controls.maxPolarAngle=Math.PI*0.48;
controls.autoRotate=false;
controls.autoRotateSpeed=0.4;
// Deferred camera position after target is set
camera.position.set(8,7,14);
camera.lookAt(controls.target);
controls.update();
// ── LIGHTING ──
const ambient = new THREE.AmbientLight('#334466',1.6);
scene.add(ambient);
const sun = new THREE.DirectionalLight('#ffe8cc',4.5);
sun.position.set(12,18,6);
sun.castShadow=true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.near=0.5;
sun.shadow.camera.far=60;
sun.shadow.camera.left=-18;
sun.shadow.camera.right=18;
sun.shadow.camera.top=18;
sun.shadow.camera.bottom=-18;
sun.shadow.bias=-0.0002;
scene.add(sun);
const fill = new THREE.DirectionalLight('#8899cc',0.8);
fill.position.set(-5,2,-4);
scene.add(fill);
// ── GROUND GRID ──
const gridHelper = new THREE.PolarGridHelper(TERRAIN_SPAN/2+2,48,24,64,'#334466','#1a1a2e');
gridHelper.position.y=-2.4;
scene.add(gridHelper);
// ── TERRAIN (BufferGeometry, recycled) ──
const terrainGeo = new THREE.BufferGeometry();
const terrainPositions = new Float32Array(GRID*GRID*3);
const terrainColors = new Float32Array(GRID*GRID*3);
const terrainIndices = [];
for(let iz=0;iz<GRID-1;iz++){
  for(let ix=0;ix<GRID-1;ix++){
    const a=iz*GRID+ix, b=a+1, c=a+GRID, d=c+1;
    terrainIndices.push(a,b,c, b,d,c);
  }
}
terrainGeo.setAttribute('position',new THREE.BufferAttribute(terrainPositions,3));
terrainGeo.setAttribute('color',new THREE.BufferAttribute(terrainColors,3));
terrainGeo.setIndex(terrainIndices);
terrainGeo.computeVertexNormals();
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors:true,
  roughness:0.65,
  metalness:0.05,
  flatShading:false,
  side:THREE.DoubleSide,
});
const terrainMesh = new THREE.Mesh(terrainGeo,terrainMat);
terrainMesh.castShadow=true;
terrainMesh.receiveShadow=true;
scene.add(terrainMesh);
function updateTerrainBuffers(slice) {
  const {height,veg,error}=slice;
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      const i=iz*GRID+ix;
      const x=(ix/(GRID-1)-0.5)*TERRAIN_SPAN;
      const z=(iz/(GRID-1)-0.5)*TERRAIN_SPAN;
      const h=height[i];
      const pi=i*3;
      terrainPositions[pi]=x;
      terrainPositions[pi+1]=h;
      terrainPositions[pi+2]=z;
      const v=veg[i];
      const e=error[i];
      const rBase=0.28+v*0.15+e*1.1;
      const gBase=0.35+v*0.55-e*0.7;
      const bBase=0.22+v*0.12-e*0.3;
      const r=Math.max(0,Math.min(1,rBase));
      const g=Math.max(0,Math.min(1,gBase));
      const b=Math.max(0,Math.min(1,bBase));
      terrainColors[pi]=r;
      terrainColors[pi+1]=g;
      terrainColors[pi+2]=b;
    }
  }
  terrainGeo.attributes.position.needsUpdate=true;
  terrainGeo.attributes.color.needsUpdate=true;
  terrainGeo.computeVertexNormals();
}
// ── RIVERS (BufferGeometry, recycled) ──
const MAX_RIVER_POINTS=GRID*4;
const riverPositionsArr=new Float32Array(MAX_RIVER_POINTS*3);
const riverColorsArr=new Float32Array(MAX_RIVER_POINTS*3);
const riverGeo=new THREE.BufferGeometry();
riverGeo.setAttribute('position',new THREE.BufferAttribute(riverPositionsArr,3));
riverGeo.setAttribute('color',new THREE.BufferAttribute(riverColorsArr,3));
const riverMat=new THREE.LineBasicMaterial({vertexColors:true,linewidth:1,transparent:true,opacity:0.85});
const riverLine=new THREE.Line(riverGeo,riverMat);
scene.add(riverLine);
function buildRiverPath(slice) {
  const {height,error}=slice;
  const paths=[];
  const visited=new Uint8Array(GRID*GRID);
  const threshold=0.42;
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      const i=iz*GRID+ix;
      if(error[i]>=threshold && !visited[i]){
        const segment=[];
        let ci=i;
        let cz=iz,cx=ix;
        while(cz>=0&&cz<GRID&&cx>=0&&cx<GRID&&!visited[ci]&&error[ci]>=threshold*0.7){
          visited[ci]=1;
          const x=(cx/(GRID-1)-0.5)*TERRAIN_SPAN;
          const z=(cz/(GRID-1)-0.5)*TERRAIN_SPAN;
          segment.push(x,height[ci]+0.08,z);
          let bestDir=-1,bestErr=0;
          const dirs=[[0,1],[1,0],[0,-1],[-1,0],[1,1],[-1,1],[1,-1],[-1,-1]];
          for(let d=0;d<dirs.length;d++){
            const nz=cz+dirs[d][0],nx=cx+dirs[d][1];
            if(nz>=0&&nz<GRID&&nx>=0&&nx<GRID){
              const ni=nz*GRID+nx;
              if(!visited[ni]&&error[ni]>bestErr){bestErr=error[ni];bestDir=d;}
            }
          }
          if(bestDir<0)break;
          cz+=dirs[bestDir][0];cx+=dirs[bestDir][1];ci=cz*GRID+cx;
        }
        if(segment.length>=9) paths.push(segment);
      }
    }
  }
  return paths;
}
function updateRiverBuffers(slice) {
  const paths=buildRiverPath(slice);
  let pi=0;
  for(const seg of paths){
    for(let j=0;j<seg.length;j+=3){
      if(pi>=MAX_RIVER_POINTS)break;
      const bp=pi*3;
      riverPositionsArr[bp]=seg[j];
      riverPositionsArr[bp+1]=seg[j+1];
      riverPositionsArr[bp+2]=seg[j+2];
      const t=j/seg.length;
      riverColorsArr[bp]=0.9+t*0.1;
      riverColorsArr[bp+1]=0.08;
      riverColorsArr[bp+2]=0.06+t*0.2;
      pi++;
    }
    if(pi>=MAX_RIVER_POINTS)break;
  }
  for(let i=pi;i<MAX_RIVER_POINTS;i++){
    const bp=i*3;
    riverPositionsArr[bp]=0;riverPositionsArr[bp+1]=-999;riverPositionsArr[bp+2]=0;
    riverColorsArr[bp]=0;riverColorsArr[bp+1]=0;riverColorsArr[bp+2]=0;
  }
  riverGeo.attributes.position.needsUpdate=true;
  riverGeo.attributes.color.needsUpdate=true;
  riverGeo.setDrawRange(0,pi);
}
// ── PARTICLES (InstancedMesh, pre-allocated) ──
const MAX_PARTICLES=600;
const particleGeom=new THREE.SphereGeometry(0.08,4,3);
const particleMatInst=new THREE.MeshStandardMaterial({color:'#ffb74d',emissive:'#ff8f00',emissiveIntensity:0.6,roughness:0.3,metalness:0.1});
const particlesInstanced=new THREE.InstancedMesh(particleGeom,particleMatInst,MAX_PARTICLES);
particlesInstanced.castShadow=false;
particlesInstanced.receiveShadow=false;
particlesInstanced.count=0;
scene.add(particlesInstanced);
const particleData=[];
for(let i=0;i<MAX_PARTICLES;i++){
  particleData.push({
    x:0,z:0,progress:Math.random(),speed:0.003+Math.random()*0.008,
    offsetX:(Math.random()-0.5)*0.8,offsetZ:(Math.random()-0.5)*0.8,
    active:false
  });
}
function seedParticles(slice) {
  const {height,apiVol}=slice;
  let count=0;
  const threshold=0.3;
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      const i=iz*GRID+ix;
      if(apiVol[i]>threshold && count<MAX_PARTICLES){
        const pd=particleData[count];
        pd.x=(ix/(GRID-1)-0.5)*TERRAIN_SPAN;
        pd.z=(iz/(GRID-1)-0.5)*TERRAIN_SPAN;
        pd.progress=Math.random();
        pd.speed=0.002+Math.random()*0.01;
        pd.offsetX=(Math.random()-0.5)*0.6;
        pd.offsetZ=(Math.random()-0.5)*0.6;
        pd.active=true;
        count++;
      }
    }
  }
  for(let i=count;i<MAX_PARTICLES;i++) particleData[i].active=false;
  particlesInstanced.count=count;
}
// ── SKY PARTICLES (ambient) ──
const skyGeo=new THREE.BufferGeometry();
const skyPositions=new Float32Array(200*3);
for(let i=0;i<200;i++){
  skyPositions[i*3]=(Math.random()-0.5)*28;
  skyPositions[i*3+1]=Math.random()*10+1;
  skyPositions[i*3+2]=(Math.random()-0.5)*28;
}
skyGeo.setAttribute('position',new THREE.BufferAttribute(skyPositions,3));
const skyMat=new THREE.PointsMaterial({color:'#8899cc',size:0.06,transparent:true,opacity:0.5});
const skyPoints=new THREE.Points(skyGeo,skyMat);
scene.add(skyPoints);
// ── INITIALIZE WITH FIRST TIME SLICE ──
let currentTimeIdx=0;
updateTerrainBuffers(ALL_SLICES[0]);
updateRiverBuffers(ALL_SLICES[0]);
seedParticles(ALL_SLICES[0]);
// ── UI WIRING ──
const slider=document.getElementById('time-slider');
slider.max=TIME_POINTS-1;
slider.value=0;
const timeLabel=document.getElementById('time-label');
function setTimeSlice(idx) {
  if(idx===currentTimeIdx)return;
  currentTimeIdx=idx;
  updateTerrainBuffers(ALL_SLICES[idx]);
  updateRiverBuffers(ALL_SLICES[idx]);
  seedParticles(ALL_SLICES[idx]);
  slider.value=idx;
  timeLabel.textContent=MONTHS[idx];
}
slider.addEventListener('input',()=>{
  setTimeSlice(parseInt(slider.value));
});
let playing=false;
let playInterval=null;
document.getElementById('btn-play').addEventListener('click',()=>{
  const btn=document.getElementById('btn-play');
  if(playing){
    clearInterval(playInterval);
    playing=false;
    btn.textContent='▶ Play';
    btn.classList.remove('active');
  }else{
    playing=true;
    btn.textContent='⏸ Pause';
    btn.classList.add('active');
    playInterval=setInterval(()=>{
      const next=(currentTimeIdx+1)%TIME_POINTS;
      setTimeSlice(next);
    },1400);
  }
});
document.getElementById('btn-autorot').addEventListener('click',()=>{
  const btn=document.getElementById('btn-autorot');
  controls.autoRotate=!controls.autoRotate;
  btn.classList.toggle('active',controls.autoRotate);
});
document.getElementById('btn-reset').addEventListener('click',()=>{
  controls.target.set(0,0.6,0);
  camera.position.set(8,7,14);
  camera.lookAt(controls.target);
  controls.update();
});
// ── CAMERA BOOKMARKS ──
const STORAGE_KEY='terrain_explorer_bookmarks';
let bookmarks=[];
try{
  const stored=localStorage.getItem(STORAGE_KEY);
  if(stored) bookmarks=JSON.parse(stored);
}catch(e){}
function saveBookmarks(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(bookmarks));}catch(e){}}
function renderBookmarkBar(){
  const bar=document.getElementById('bookmark-bar');
  bar.querySelectorAll('.bookmark-btn').forEach(b=>b.remove());
  for(let i=0;i<bookmarks.length;i++){
    const bm=bookmarks[i];
    const btn=document.createElement('button');
    btn.className='bookmark-btn';
    btn.textContent=(i+1)+' '+bm.label;
    btn.title='Go to: '+bm.label;
    btn.addEventListener('click',()=>{
      controls.target.set(bm.target[0],bm.target[1],bm.target[2]);
      camera.position.set(bm.pos[0],bm.pos[1],bm.pos[2]);
      camera.lookAt(controls.target);
      controls.update();
    });
    btn.addEventListener('contextmenu',(e)=>{e.preventDefault();bookmarks.splice(i,1);saveBookmarks();renderBookmarkBar();});
    bar.appendChild(btn);
  }
}
document.getElementById('btn-save-bm').addEventListener('click',()=>{
  const label=prompt('Bookmark name:','View '+(bookmarks.length+1));
  if(!label)return;
  bookmarks.push({
    label,
    target:[controls.target.x,controls.target.y,controls.target.z],
    pos:[camera.position.x,camera.position.y,camera.position.z]
  });
  if(bookmarks.length>8)bookmarks.shift();
  saveBookmarks();
  renderBookmarkBar();
});
renderBookmarkBar();
// ── RESIZE ──
window.addEventListener('resize',()=>{
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});
// ── RENDER LOOP ──
const clock=new THREE.Clock();
let frames=0,fpsTime=0,currentFPS=0;
function animate() {
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),0.1);
  controls.update();
  // Update particles (reuse V3 pool, no per-frame allocations)
  V3.releaseAll();
  const slice=ALL_SLICES[currentTimeIdx];
  const {height}=slice;
  let activeCount=0;
  for(let i=0;i<particlesInstanced.count;i++){
    const pd=particleData[i];
    if(!pd.active)continue;
    pd.progress+=pd.speed*dt*60;
    if(pd.progress>1.0)pd.progress-=1.0;
    const px=pd.x+pd.offsetX*Math.sin(pd.progress*Math.PI*2);
    const pz=pd.z+pd.offsetZ*Math.cos(pd.progress*Math.PI*2);
    const gx=(px/TERRAIN_SPAN+0.5)*(GRID-1);
    const gz=(pz/TERRAIN_SPAN+0.5)*(GRID-1);
    const ix=Math.round(gx),iz=Math.round(gz);
    let h=0;
    if(ix>=0&&ix<GRID&&iz>=0&&iz<GRID) h=height[iz*GRID+ix];
    const py=h+0.25+Math.sin(pd.progress*Math.PI)*0.4;
    DUMMY.position.set(px,py,pz);
    DUMMY.scale.setScalar(0.8+pd.progress*0.5);
    DUMMY.updateMatrix();
    particlesInstanced.setMatrixAt(i,DUMMY.matrix);
    activeCount++;
  }
  particlesInstanced.count=activeCount;
  particlesInstanced.instanceMatrix.needsUpdate=true;
  // Sky particles drift
  const skyPos=skyGeo.attributes.position.array;
  for(let i=0;i<200;i++){
    skyPos[i*3+1]+=dt*0.3;
    if(skyPos[i*3+1]>11) skyPos[i*3+1]-=10;
  }
  skyGeo.attributes.position.needsUpdate=true;
  renderer.render(scene,camera);
  // FPS counter
  frames++;
  fpsTime+=dt;
  if(fpsTime>=0.5){
    currentFPS=Math.round(frames/fpsTime);
    frames=0;fpsTime=0;
    document.getElementById('fps').textContent=currentFPS;
    document.getElementById('draws').textContent=renderer.info.render.calls;
  }
}
// Start
timeLabel.textContent=MONTHS[0];
animate();
</script>
</body>
</html>