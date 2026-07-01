<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
:root{--bg:#0a0a14;--panel:#12122a;--border:#2a2a4a;--text:#c8c8e0;--accent:#4af;--danger:#f44;--warn:#fa0;--success:#4f8}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);font-family:'Segoe UI',system-ui,sans-serif;overflow:hidden;height:100vh;color:var(--text)}
#canvas{position:fixed;inset:0;z-index:1}
#panel{position:fixed;top:0;left:0;width:320px;height:100vh;z-index:10;background:var(--panel);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:16px;gap:12px;overflow-y:auto;backdrop-filter:blur(12px)}
#panel h1{font-size:1.1rem;font-weight:600;color:#fff;letter-spacing:.02em;text-transform:uppercase;border-bottom:1px solid var(--border);padding-bottom:10px;margin-bottom:2px}
.section-label{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:#888;margin-top:4px}
#time-display{font-size:1.6rem;font-weight:700;color:var(--accent);text-align:center;font-variant-numeric:tabular-nums}
input[type=range]{width:100%;accent-color:var(--accent);margin:4px 0}
.btn-row{display:flex;gap:6px;flex-wrap:wrap}
button{background:#1a1a3a;border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:4px;cursor:pointer;font-size:.75rem;transition:all .15s;white-space:nowrap}
button:hover{background:#2a2a5a;border-color:var(--accent);color:#fff}
button.active{background:var(--accent);color:#000;border-color:var(--accent);font-weight:600}
button.danger{background:#3a1a1a;border-color:#5a2a2a}
button.danger:hover{background:#5a2a2a;border-color:var(--danger)}
.bookmark-btn{display:block;width:100%;text-align:left;margin:2px 0;font-size:.7rem;padding:5px 8px}
.bookmark-btn .time{color:var(--accent);float:right}
.legend-row{display:flex;align-items:center;gap:8px;margin:2px 0;font-size:.7rem}
.legend-swatch{width:14px;height:14px;border-radius:3px;flex-shrink:0}
.stats{font-size:.7rem;color:#999;line-height:1.5}
.stats span{color:var(--accent);font-weight:600}
#tooltip{position:fixed;pointer-events:none;z-index:20;background:rgba(0,0,0,.85);color:#fff;padding:6px 10px;border-radius:4px;font-size:.7rem;display:none;border:1px solid var(--border)}
</style>
</head>
<body>
<div id="canvas"></div>
<div id="panel">
  <h1>Terrain Explorer</h1>
  <div id="time-display">12:00</div>
  <div class="section-label">Time</div>
  <input type="range" id="time-slider" min="0" max="23" value="12" step="1">
  <div class="btn-row">
    <button id="btn-play">Play</button>
    <button id="btn-speed-1" class="active">1x</button>
    <button id="btn-speed-2">2x</button>
    <button id="btn-speed-4">4x</button>
  </div>
  <div class="section-label">View</div>
  <div class="btn-row">
    <button id="btn-top">Top</button>
    <button id="btn-persp">Perspective</button>
    <button id="btn-auto-rotate">Auto Rotate</button>
    <button id="btn-wireframe">Wireframe</button>
  </div>
  <div class="section-label">Bookmarks</div>
  <div id="bookmark-list"></div>
  <div class="btn-row">
    <button id="btn-save-bm">Save View</button>
    <button id="btn-clear-bm" class="danger">Clear All</button>
  </div>
  <div class="section-label">Legend</div>
  <div class="legend-row"><div class="legend-swatch" style="background:linear-gradient(90deg,#1a4,#4f8,#fa0,#f44)"></div>User Density</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#e22"></div>Error Rivers (>60%)</div>
  <div class="legend-row"><div class="legend-swatch" style="background:#0ff"></div>API Call Particles</div>
  <div class="section-label">Stats</div>
  <div class="stats" id="stats">
    Vertices: <span id="stat-verts">-</span><br>
    Rivers: <span id="stat-rivers">-</span><br>
    Particles: <span id="stat-particles">-</span><br>
    FPS: <span id="stat-fps">-</span>
  </div>
</div>
<div id="tooltip"></div>
<script type="importmap">
{"imports":{
  "three":"https://unpkg.com/three@0.160.0/build/three.module.js",
  "three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"
}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 60;
const TIMES = 24;
const CELL_SIZE = 0.5;
const TERRAIN_W = (GRID-1) * CELL_SIZE;
const TERRAIN_H = (GRID-1) * CELL_SIZE;
const HEIGHT_SCALE = 8;
const RIVER_THRESH = 0.6;
const PARTICLE_COUNT = 600;
function hash(x,y){let h=0;for(let i=0;i<4;i++){h+=Math.sin((x*12.9898+y*78.233+h)*43758.5453+i*631.1);}return h-Math.floor(h);}
function noise(x,y,t,freq,amp){let v=0;const octaves=3;for(let o=0;o<octaves;o++){const s=Math.pow(2,o);v+=Math.sin(x*freq*s+t*0.7+o)*Math.cos(y*freq*s*1.3-t*0.5+o)*amp/s;}return v;}
function genData(){
  const N=GRID*GRID;
  const heights=new Float32Array(TIMES*N);
  const density=new Float32Array(TIMES*N);
  const errors=new Float32Array(TIMES*N);
  const apiAct=new Float32Array(TIMES*N);
  for(let t=0;t<TIMES;t++){
    const phase=t/TIMES*Math.PI*2;
    const biz=Math.max(0,Math.sin((t-8)/24*Math.PI*2)*0.7+0.3); // business hours 8-20 peak
    for(let iy=0;iy<GRID;iy++){
      for(let ix=0;ix<GRID;ix++){
        const idx=t*N+iy*GRID+ix;
        const x=(ix-GRID/2)/(GRID/4);
        const y=(iy-GRID/2)/(GRID/4);
        const n1=noise(x,y,phase,0.6,1.0);
        const n2=noise(x+5,y+3,phase*1.4,0.8,0.6);
        const dist=Math.sqrt(x*x+y*y)/3;
        const h=n1*0.5+n2*0.3+Math.exp(-dist)*0.4+biz*0.25;
        heights[idx]=Math.max(0,Math.min(1,h*0.7+0.15));
        const d=noise(x+2,y-1,phase*0.8,0.5,0.8)+biz*0.4+Math.exp(-((x-1)*(x-1)+(y-0.5)*(y-0.5))*0.5)*0.3;
        density[idx]=Math.max(0,Math.min(1,d*0.65+0.1));
        const e=Math.abs(noise(x*2.5,y*2.5,phase*1.6,1.2,0.5));
        const spike=(hash(ix*7+iy*13+t*3)<0.08)?hash(ix+iy*31+t*17)*0.7+0.3:0;
        errors[idx]=Math.max(0,Math.min(1,e*0.5+spike*0.5));
        apiAct[idx]=Math.pow(Math.max(0,noise(x-1,y+1,phase*1.2,0.7,0.7)+biz*0.5),2);
      }
    }
  }
  return {heights,density,errors,apiAct};
}
const data=genData();
const N=GRID*GRID;
// --- SCENE SETUP ---
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:false});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.1;
document.getElementById('canvas').appendChild(renderer.domElement);
const scene=new THREE.Scene();
scene.background=new THREE.Color('#0a0a1e');
scene.fog=new THREE.Fog('#0a0a1e',20,80);
const camera=new THREE.PerspectiveCamera(55,window.innerWidth/window.innerHeight,0.5,150);
camera.position.set(18,14,22);
camera.lookAt(0,0,0);
const controls=new OrbitControls(camera,renderer.domElement);
controls.target.set(0,2,0);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.minDistance=5;
controls.maxDistance=60;
controls.maxPolarAngle=Math.PI*0.48;
controls.autoRotate=false;
controls.autoRotateSpeed=0.3;
controls.update();
// --- LIGHTS ---
const ambient=new THREE.AmbientLight('#334466',1.8);
scene.add(ambient);
const sun=new THREE.DirectionalLight('#ffe8d0',4.5);
sun.position.set(20,25,10);
sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.near=0.5;
sun.shadow.camera.far=100;
sun.shadow.camera.left=-25;sun.shadow.camera.right=25;
sun.shadow.camera.top=25;sun.shadow.camera.bottom=-25;
sun.shadow.bias=-0.0004;
scene.add(sun);
const fill=new THREE.DirectionalLight('#8899cc',0.8);
fill.position.set(-10,5,-15);
scene.add(fill);
// --- GROUND PLANE ---
const groundGeo=new THREE.PlaneGeometry(50,50);
const groundMat=new THREE.MeshStandardMaterial({color:'#111122',roughness:0.95,metalness:0.1});
const ground=new THREE.Mesh(groundGeo,groundMat);
ground.rotation.x=-Math.PI/2;
ground.position.y=-3;
ground.receiveShadow=true;
scene.add(ground);
// --- TERRAIN MESH ---
const terrainGeo=new THREE.BufferGeometry();
const posArray=new Float32Array(N*3);
const colArray=new Float32Array(N*3);
const idxArray=new Uint32Array((GRID-1)*(GRID-1)*6);
let vi=0;
for(let iy=0;iy<GRID;iy++){
  for(let ix=0;ix<GRID;ix++){
    posArray[vi*3]=(ix-GRID/2)*CELL_SIZE;
    posArray[vi*3+2]=(iy-GRID/2)*CELL_SIZE;
    posArray[vi*3+1]=0;
    vi++;
  }
}
let ii=0;
for(let iy=0;iy<GRID-1;iy++){
  for(let ix=0;ix<GRID-1;ix++){
    const a=iy*GRID+ix;
    const b=a+1;
    const c=a+GRID;
    const d=c+1;
    idxArray[ii++]=a;idxArray[ii++]=b;idxArray[ii++]=d;
    idxArray[ii++]=a;idxArray[ii++]=d;idxArray[ii++]=c;
  }
}
terrainGeo.setAttribute('position',new THREE.BufferAttribute(posArray,3));
terrainGeo.setAttribute('color',new THREE.BufferAttribute(colArray,3));
terrainGeo.setIndex(new THREE.BufferAttribute(idxArray,1));
terrainGeo.computeVertexNormals();
const terrainMat=new THREE.MeshStandardMaterial({
  vertexColors:true,roughness:0.7,metalness:0.05,flatShading:false
});
const terrain=new THREE.Mesh(terrainGeo,terrainMat);
terrain.castShadow=true;terrain.receiveShadow=true;
scene.add(terrain);
// --- TERRAIN UPDATE ---
const posAttr=terrainGeo.getAttribute('position');
const colAttr=terrainGeo.getAttribute('color');
function heatColor(t){
  t=Math.max(0,Math.min(1,t));
  if(t<0.25){const s=t/0.25;return [0.1+s*0.4,0.27+s*0.5,0.1+s*0.15];}
  else if(t<0.5){const s=(t-0.25)/0.25;return [0.5+s*0.4,0.77-s*0.3,0.25-s*0.1];}
  else if(t<0.75){const s=(t-0.5)/0.25;return [0.9+s*0.1,0.47-s*0.2,0.15-s*0.05];}
  else{const s=(t-0.75)/0.25;return [1.0,0.27-s*0.15,0.1+s*0.6];}
}
function updateTerrain(timeIdx){
  const off=timeIdx*N;
  const h=data.heights;
  const d=data.density;
  for(let i=0;i<N;i++){
    posAttr.array[i*3+1]=h[off+i]*HEIGHT_SCALE;
    const [r,g,b]=heatColor(d[off+i]);
    colAttr.array[i*3]=r;colAttr.array[i*3+1]=g;colAttr.array[i*3+2]=b;
  }
  posAttr.needsUpdate=true;
  colAttr.needsUpdate=true;
  terrainGeo.computeVertexNormals();
}
// --- RIVERS ---
const riverGroup=new THREE.Group();
const riverMaterial=new THREE.MeshStandardMaterial({color:'#e03030',roughness:0.3,metalness:0.2,emissive:'#801010',emissiveIntensity:0.6});
const riverCache=[];
function buildRiversForTime(timeIdx){
  const off=timeIdx*N;
  const visited=new Uint8Array(N);
  const meshes=[];
  const dirs=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]];
  for(let iy=0;iy<GRID;iy++){
    for(let ix=0;ix<GRID;ix++){
      const idx=iy*GRID+ix;
      if(visited[idx]||data.errors[off+idx]<RIVER_THRESH)continue;
      const component=[];
      const stack=[idx];
      visited[idx]=1;
      while(stack.length>0){
        const cur=stack.pop();
        component.push(cur);
        const cx=cur%GRID,cy=Math.floor(cur/GRID);
        for(const [dx,dy] of dirs){
          const nx=cx+dx,ny=cy+dy;
          if(nx<0||nx>=GRID||ny<0||ny>=GRID)continue;
          const ni=ny*GRID+nx;
          if(!visited[ni]&&data.errors[off+ni]>=RIVER_THRESH){visited[ni]=1;stack.push(ni);}
        }
      }
      if(component.length<3)continue;
      component.sort((a,b)=>{
        const ax=a%GRID,ay=Math.floor(a/GRID),bx=b%GRID,by=Math.floor(b/GRID);
        return (ax+ay*0.5)-(bx+by*0.5);
      });
      const pts=component.map(ci=>{
        const cx=ci%GRID,cy=Math.floor(ci/GRID);
        const hVal=data.heights[off+ci]*HEIGHT_SCALE+0.15;
        return new THREE.Vector3((cx-GRID/2)*CELL_SIZE,hVal,(cy-GRID/2)*CELL_SIZE);
      });
      if(pts.length<2)continue;
      const curve=new THREE.CatmullRomCurve3(pts,false,'catmullrom',0.5);
      const tubeGeo=new THREE.TubeGeometry(curve,Math.min(pts.length*3,80),0.12,6,false);
      const mesh=new THREE.Mesh(tubeGeo,riverMaterial);
      mesh.castShadow=true;
      meshes.push(mesh);
    }
  }
  return meshes;
}
for(let t=0;t<TIMES;t++){riverCache[t]=buildRiversForTime(t);}
function setRivers(timeIdx){
  while(riverGroup.children.length>0)riverGroup.remove(riverGroup.children[0]);
  for(const m of riverCache[timeIdx])riverGroup.add(m);
  document.getElementById('stat-rivers').textContent=riverCache[timeIdx].length;
}
scene.add(riverGroup);
// --- PARTICLES ---
const particleGeo=new THREE.BufferGeometry();
const particlePositions=new Float32Array(PARTICLE_COUNT*3);
const particleColors=new Float32Array(PARTICLE_COUNT*3);
const particleData=[];
for(let i=0;i<PARTICLE_COUNT;i++){
  particlePositions[i*3]=(Math.random()-0.5)*TERRAIN_W;
  particlePositions[i*3+1]=3;
  particlePositions[i*3+2]=(Math.random()-0.5)*TERRAIN_H;
  particleColors[i*3]=0.3;particleColors[i*3+1]=0.9;particleColors[i*3+2]=1.0;
  particleData.push({
    x:particlePositions[i*3],z:particlePositions[i*3+2],y:0,
    vx:(Math.random()-0.5)*0.08,vz:(Math.random()-0.5)*0.08,
    life:Math.random()*4,age:0
  });
}
particleGeo.setAttribute('position',new THREE.BufferAttribute(particlePositions,3));
particleGeo.setAttribute('color',new THREE.BufferAttribute(particleColors,3));
const particleMat=new THREE.PointsMaterial({
  size:0.18,vertexColors:true,blending:THREE.AdditiveBlending,depthWrite:false,
  transparent:true,opacity:0.85
});
const particles=new THREE.Points(particleGeo,particleMat);
scene.add(particles);
const pPos=particleGeo.getAttribute('position');
const pCol=particleGeo.getAttribute('color');
function sampleTerrainHeight(px,pz,timeIdx){
  const gx=Math.round(px/CELL_SIZE+GRID/2);
  const gy=Math.round(pz/CELL_SIZE+GRID/2);
  if(gx<0||gx>=GRID||gy<0||gy>=GRID)return 0;
  return data.heights[timeIdx*N+gy*GRID+gx]*HEIGHT_SCALE;
}
function sampleTerrainGradient(px,pz,timeIdx){
  const eps=CELL_SIZE;
  const hL=sampleTerrainHeight(px-eps,pz,timeIdx);
  const hR=sampleTerrainHeight(px+eps,pz,timeIdx);
  const hD=sampleTerrainHeight(px,pz-eps,timeIdx);
  const hU=sampleTerrainHeight(px,pz+eps,timeIdx);
  return {gx:(hR-hL)/(2*eps),gz:(hU-hD)/(2*eps)};
}
function updateParticles(dt,timeIdx){
  for(let i=0;i<PARTICLE_COUNT;i++){
    const pd=particleData[i];
    pd.age+=dt;
    if(pd.age>pd.life){
      pd.age=0;pd.life=2+Math.random()*5;
      pd.x=(Math.random()-0.5)*TERRAIN_W;
      pd.z=(Math.random()-0.5)*TERRAIN_H;
      pd.y=sampleTerrainHeight(pd.x,pd.z,timeIdx)+0.3;
      const grad=sampleTerrainGradient(pd.x,pd.z,timeIdx);
      const speed=0.04+Math.random()*0.08;
      const mag=Math.sqrt(grad.gx*grad.gx+grad.gz*grad.gz)+0.001;
      pd.vx=-grad.gx/mag*speed+(Math.random()-0.5)*0.02;
      pd.vz=-grad.gz/mag*speed+(Math.random()-0.5)*0.02;
    }
    pd.x+=pd.vx;
    pd.z+=pd.vz;
    if(Math.abs(pd.x)>TERRAIN_W/2+1||Math.abs(pd.z)>TERRAIN_H/2+1){pd.age=pd.life;continue;}
    pd.y=sampleTerrainHeight(pd.x,pd.z,timeIdx)+0.3;
    const grad=sampleTerrainGradient(pd.x,pd.z,timeIdx);
    const mag=Math.sqrt(grad.gx*grad.gx+grad.gz*grad.gz)+0.001;
    pd.vx+=-grad.gx/mag*0.015;
    pd.vz+=-grad.gz/mag*0.015;
    const spd=Math.sqrt(pd.vx*pd.vx+pd.vz*pd.vz);
    if(spd>0.12){pd.vx*=0.12/spd;pd.vz*=0.12/spd;}
    const t=pd.age/pd.life;
    particlePositions[i*3]=pd.x;
    particlePositions[i*3+1]=pd.y;
    particlePositions[i*3+2]=pd.z;
    particleColors[i*3]=0.2+t*0.4;
    particleColors[i*3+1]=0.7+t*0.3;
    particleColors[i*3+2]=1.0;
  }
  pPos.needsUpdate=true;
  pCol.needsUpdate=true;
  document.getElementById('stat-particles').textContent=PARTICLE_COUNT;
}
// --- STATE ---
let currentTime=12;
let playing=false;
let playSpeed=1;
let wireframe=false;
let autoRotate=false;
let bookmarks=JSON.parse(localStorage.getItem('terrain-bookmarks')||'[]');
// --- INIT ---
updateTerrain(currentTime);
setRivers(currentTime);
document.getElementById('stat-verts').textContent=N.toLocaleString();
// --- BOOKMARKS UI ---
function renderBookmarks(){
  const list=document.getElementById('bookmark-list');
  list.innerHTML='';
  bookmarks.forEach((bm,i)=>{
    const btn=document.createElement('button');
    btn.className='bookmark-btn';
    btn.innerHTML=`${bm.label||'View '+i}<span class="time">${bm.time||'--'}:00</span>`;
    btn.onclick=()=>recallBookmark(i);
    btn.oncontextmenu=(e)=>{e.preventDefault();bookmarks.splice(i,1);saveBookmarks();renderBookmarks();};
    list.appendChild(btn);
  });
}
function saveBookmarks(){localStorage.setItem('terrain-bookmarks',JSON.stringify(bookmarks));}
function recallBookmark(i){
  const bm=bookmarks[i];
  if(!bm)return;
  camera.position.set(bm.px,bm.py,bm.pz);
  controls.target.set(bm.tx,bm.ty,bm.tz);
  controls.update();
  if(bm.time!==undefined){currentTime=bm.time;syncUIToTime();}
}
renderBookmarks();
document.getElementById('btn-save-bm').onclick=()=>{
  const label=prompt('Bookmark name:','View '+bookmarks.length)||('View '+bookmarks.length);
  bookmarks.push({
    label,time:currentTime,
    px:camera.position.x,py:camera.position.y,pz:camera.position.z,
    tx:controls.target.x,ty:controls.target.y,tz:controls.target.z
  });
  saveBookmarks();renderBookmarks();
};
document.getElementById('btn-clear-bm').onclick=()=>{bookmarks=[];saveBookmarks();renderBookmarks();};
// --- UI WIRING ---
function syncUIToTime(){
  document.getElementById('time-slider').value=currentTime;
  document.getElementById('time-display').textContent=String(currentTime).padStart(2,'0')+':00';
  updateTerrain(currentTime);
  setRivers(currentTime);
}
const slider=document.getElementById('time-slider');
slider.oninput=()=>{currentTime=parseInt(slider.value);syncUIToTime();};
document.getElementById('btn-play').onclick=()=>{
  playing=!playing;
  document.getElementById('btn-play').textContent=playing?'Pause':'Play';
  document.getElementById('btn-play').classList.toggle('active',playing);
};
document.querySelectorAll('[id^=btn-speed-]').forEach(b=>{
  b.onclick=()=>{
    document.querySelectorAll('[id^=btn-speed-]').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    playSpeed=parseInt(b.textContent);
  };
});
document.getElementById('btn-top').onclick=()=>{
  const t=controls.target;
  camera.position.set(t.x,t.y+25,t.z+0.1);
  controls.update();
};
document.getElementById('btn-persp').onclick=()=>{
  camera.position.set(18,14,22);
  controls.target.set(0,2,0);
  controls.update();
};
document.getElementById('btn-auto-rotate').onclick=()=>{
  autoRotate=!autoRotate;
  controls.autoRotate=autoRotate;
  document.getElementById('btn-auto-rotate').classList.toggle('active',autoRotate);
};
document.getElementById('btn-wireframe').onclick=()=>{
  wireframe=!wireframe;
  terrainMat.wireframe=wireframe;
  document.getElementById('btn-wireframe').classList.toggle('active',wireframe);
};
window.addEventListener('resize',()=>{
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});
// --- TOOLTIP ---
const tooltip=document.getElementById('tooltip');
const raycaster=new THREE.Raycaster();
const mouse=new THREE.Vector2();
renderer.domElement.addEventListener('mousemove',(e)=>{
  mouse.x=(e.clientX/renderer.domElement.clientWidth)*2-1;
  mouse.y=-(e.clientY/renderer.domElement.clientHeight)*2+1;
  raycaster.setFromCamera(mouse,camera);
  const hits=raycaster.intersectObject(terrain);
  if(hits.length>0){
    const p=hits[0].point;
    const gx=Math.round(p.x/CELL_SIZE+GRID/2);
    const gz=Math.round(p.z/CELL_SIZE+GRID/2);
    if(gx>=0&&gx<GRID&&gz>=0&&gz<GRID){
      const off=currentTime*N+gz*GRID+gx;
      tooltip.style.display='block';
      tooltip.style.left=(e.clientX+16)+'px';
      tooltip.style.top=(e.clientY-10)+'px';
      tooltip.innerHTML=
        `Cell (${gx},${gz})<br>`+
        `Revenue: ${(data.heights[off]*100).toFixed(0)}%<br>`+
        `Users: ${(data.density[off]*100).toFixed(0)}%<br>`+
        `Errors: ${(data.errors[off]*100).toFixed(0)}%<br>`+
        `API: ${(data.apiAct[off]*100).toFixed(0)}%`;
    }
  }else{tooltip.style.display='none';}
});
// --- ANIMATION LOOP ---
let lastTime=performance.now();
let timeAccum=0;
const fpsFrames=[];
function animate(now){
  requestAnimationFrame(animate);
  const dt=Math.min((now-lastTime)/1000,0.1);
  lastTime=now;
  if(playing){
    timeAccum+=dt*playSpeed;
    if(timeAccum>=1.0){
      timeAccum-=1.0;
      currentTime=(currentTime+1)%TIMES;
      syncUIToTime();
    }
  }
  controls.update();
  updateParticles(dt,currentTime);
  renderer.render(scene,camera);
  fpsFrames.push(now);
  while(fpsFrames.length>0&&fpsFrames[0]<now-1000)fpsFrames.shift();
  document.getElementById('stat-fps').textContent=fpsFrames.length;
}
syncUIToTime();
requestAnimationFrame(animate);
</script>
</body>
</html>