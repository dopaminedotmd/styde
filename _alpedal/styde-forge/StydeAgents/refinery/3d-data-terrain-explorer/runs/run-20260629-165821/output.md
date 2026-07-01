```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer v1.1</title>
<style>
  :root{--bg:#0a0a0f;--panel-bg:#111118;--text:#c8c8d4;--accent:#4da6ff;--warn:#ff6b6b;--ok:#4dff88;--border:#222233}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  #canvas{position:fixed;inset:0;z-index:0}
  #panel{position:fixed;bottom:16px;left:16px;right:16px;z-index:10;display:flex;gap:12px;align-items:flex-end;pointer-events:none}
  #panel>*{pointer-events:auto}
  .card{background:var(--panel-bg);border:1px solid var(--border);border-radius:8px;padding:12px 16px;backdrop-filter:blur(12px)}
  #time-bar{flex:1;display:flex;flex-direction:column;gap:6px}
  #time-bar label{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#888}
  #time-slider{width:100%;accent-color:var(--accent);height:6px}
  #time-value{font-size:12px;color:var(--accent);font-weight:600}
  .btn-row{display:flex;gap:6px;flex-wrap:wrap}
  button{background:var(--panel-bg);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:all .15s}
  button:hover{border-color:var(--accent);color:var(--accent)}
  button.active{background:var(--accent);color:#000;border-color:var(--accent)}
  #diag{position:fixed;top:12px;right:12px;z-index:10;background:var(--panel-bg);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-size:10px;font-family:monospace;line-height:1.6;min-width:180px}
  .diag-key{color:#888}.diag-val{color:var(--accent)}.diag-miss{color:var(--warn)}
</style>
</head>
<body>
<div id="canvas"></div>
<div id="diag">
  <div><span class="diag-key">cache</span> <span class="diag-val" id="d-hit">0</span>/<span class="diag-miss" id="d-miss">0</span></div>
  <div><span class="diag-key">fps</span> <span class="diag-val" id="d-fps">0</span></div>
  <div><span class="diag-key">particles</span> <span class="diag-val" id="d-part">0</span></div>
  <div><span class="diag-key">slice</span> <span class="diag-val" id="d-slice">0</span></div>
</div>
<div id="panel">
  <div class="card btn-row">
    <button onclick="setBookmark(0)">Overview</button>
    <button onclick="setBookmark(1)">Top-down</button>
    <button onclick="setBookmark(2)">Valley</button>
    <button id="btn-rot" onclick="toggleRotate()">Rotate</button>
    <button onclick="switchDataset()">Dataset</button>
  </div>
  <div id="time-bar" class="card">
    <label>Time Slice <span id="time-value">0 / 11</span></label>
    <input type="range" id="time-slider" min="0" max="11" value="0" step="1">
  </div>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
// ── Ring buffer for diagnostics (no per-frame alloc) ──
class RingBuffer{constructor(cap){this.buf=new Array(cap);this.head=0;this.size=0;this.cap=cap}
  push(v){this.buf[this.head]=v;this.head=(this.head+1)%this.cap;if(this.size<this.cap)this.size++}
  avg(){if(this.size===0)return 0;let s=0;for(let i=0;i<this.size;i++)s+=this.buf[i];return s/this.size}}
const fpsRing=new RingBuffer(60);
// ── Cache tracker ──
let cacheHits=0,cacheMisses=0;
function cacheHit(){cacheHits++;document.getElementById('d-hit').textContent=cacheHits}
function cacheMiss(){cacheMisses++;document.getElementById('d-miss').textContent=cacheMisses}
// ── Dataset provider interface (swappable for DEM/geotiff) ──
// Implementations must provide: getHeight(t,x,z) -> float, getMetric(t,x,z) -> float, getAnomalies(t) -> [{x,z}[]], getFlows(t) -> [{x,z}[][]], numSlices -> int
let activeDataset=0;
const GRID=64;
const datasets=[];
function buildProceduralDataset(seed){
  const slices=[];
  const n=12;
  for(let t=0;t<n;t++){
    const h=new Float32Array(GRID*GRID);
    const m=new Float32Array(GRID*GRID);
    for(let iz=0;iz<GRID;iz++){for(let ix=0;ix<GRID;ix++){
      const fx=ix/(GRID-1),fz=iz/(GRID-1);
      // Height: multi-octave noise + time drift
      const tt=t/(n-1);
      const h1=Math.sin(fx*6+seed)*Math.cos(fz*5+seed*1.3)*0.5+0.5;
      const h2=Math.sin(fx*12+fz*8+seed*0.7)*0.3;
      const ridge=1-Math.abs(fx-0.5)*2;
      const valley=Math.sin(fz*Math.PI)*ridge;
      const drift=tt*0.4*Math.sin(fx*3+seed);
      h[iz*GRID+ix]=h1*0.6+h2*0.25+valley*0.4+drift;
      // Secondary metric: user density / vegetation
      m[iz*GRID+ix]=Math.abs(Math.cos(fx*7+seed*1.1)*Math.sin(fz*6+seed*0.9))*(0.5+0.5*h1);
    }}
    // Anomaly paths (rivers)
    const anomalies=[];
    const na=2+(t%3);
    for(let a=0;a<na;a++){
      const path=[];
      const sx=0.1+(seed+a)*0.15,sy=0.92;
      for(let s=0;s<30;s++){path.push({x:sx+(s/29)*0.8-0.4, z:sy-s*0.03+(Math.sin(s*0.4+a)*0.04)})}
      anomalies.push(path);
    }
    // Flow paths (API calls)
    const flows=[];
    const nf=8+(t%5);
    for(let f=0;f<nf;f++){
      const path=[];
      const sx=0.15+(seed+f)*0.08,sz=0.1+f*0.07;
      for(let s=0;s<20;s++){
        const prog=s/19;
        path.push({x:sx+prog*0.6+Math.sin(prog*5+f)*0.05, z:sz+prog*0.8});
      }
      flows.push(path);
    }
    slices.push({height:h,metric:m,anomalies,flows});
  }
  return {slices,numSlices:n,
    getHeight(t,x,z){
      const s=this.slices[Math.round(t)];
      const ix=Math.round(x*(GRID-1)),iz=Math.round(z*(GRID-1));
      const ci=Math.max(0,Math.min(GRID-1,ix)),cz=Math.max(0,Math.min(GRID-1,iz));
      return s.height[cz*GRID+ci];
    },
    getMetric(t,x,z){
      const s=this.slices[Math.round(t)];
      const ix=Math.round(x*(GRID-1)),iz=Math.round(z*(GRID-1));
      const ci=Math.max(0,Math.min(GRID-1,ix)),cz=Math.max(0,Math.min(GRID-1,iz));
      return s.metric[cz*GRID+ci];
    },
    getAnomalies(t){return this.slices[Math.round(t)].anomalies},
    getFlows(t){return this.slices[Math.round(t)].flows}
  };
}
datasets.push(buildProceduralDataset(1.7));
datasets.push(buildProceduralDataset(4.2));
datasets.push(buildProceduralDataset(8.9));
let ds=datasets[activeDataset];
// ── Three.js setup ──
const container=document.getElementById('canvas');
const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.2;
container.appendChild(renderer.domElement);
const scene=new THREE.Scene();
scene.background=new THREE.Color('#0a0a0f');
scene.fog=new THREE.Fog('#0a0a0f',15,45);
const camera=new THREE.PerspectiveCamera(55,window.innerWidth/window.innerHeight,0.5,80);
camera.position.set(6,5.5,7.5);
camera.lookAt(0,0.4,0);
const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;controls.dampingFactor=0.08;
controls.target.set(0,0.35,0);
controls.minDistance=2;controls.maxDistance=20;
controls.maxPolarAngle=Math.PI*0.7;
controls.autoRotate=false;controls.autoRotateSpeed=0.4;
controls.update();
// Lighting
scene.add(new THREE.AmbientLight('#334466',2.5));
const sun=new THREE.DirectionalLight('#ffeedd',4);
sun.position.set(8,14,4);
scene.add(sun);
const fill=new THREE.DirectionalLight('#4466aa',1.2);
fill.position.set(-4,3,-2);
scene.add(fill);
const rim=new THREE.DirectionalLight('#ff8866',0.8);
rim.position.set(0,1,8);
scene.add(rim);
// ── Bookmarks ──
const bookmarks=[
  {pos:[6,5.5,7.5],target:[0,0.35,0]},
  {pos:[0,9,0.01],target:[0,0,0.5]},
  {pos:[1.5,1.8,3.5],target:[0.6,0.25,0.8]},
];
// ── Terrain cache ──
const terrainGeoCache=new Map(); // key: dataset+slice -> BufferGeometry
// Lazy-init: geometry created on first access, NOT at load
function getTerrainGeometry(datasetIdx,sliceIdx){
  const key=`${datasetIdx}_${sliceIdx}`;
  if(terrainGeoCache.has(key)){cacheHit();return terrainGeoCache.get(key)}
  cacheMiss();
  const d=datasets[datasetIdx];
  const s=d.slices[sliceIdx];
  const geo=new THREE.BufferGeometry();
  const verts=new Float32Array(GRID*GRID*3);
  const colors=new Float32Array(GRID*GRID*3);
  for(let iz=0;iz<GRID;iz++){
    for(let ix=0;ix<GRID;ix++){
      const i=iz*GRID+ix;
      const x=(ix/(GRID-1)-0.5)*8;
      const z=(iz/(GRID-1)-0.5)*6;
      const h=s.height[i]*3;
      verts[i*3]=x;verts[i*3+1]=h;verts[i*3+2]=z;
      // Color: green (low metric) -> yellow -> red (high)
      const m=s.metric[i];
      const cr=new THREE.Color();
      cr.setHSL(0.08+m*0.25,0.8,0.25+m*0.45);
      colors[i*3]=cr.r;colors[i*3+1]=cr.g;colors[i*3+2]=cr.b;
    }
  }
  // Indices
  const indices=new Uint16Array((GRID-1)*(GRID-1)*6);
  let idx=0;
  for(let iz=0;iz<GRID-1;iz++){
    for(let ix=0;ix<GRID-1;ix++){
      const a=iz*GRID+ix,b=a+1,c=a+GRID,d=c+1;
      indices[idx++]=a;indices[idx++]=c;indices[idx++]=b;
      indices[idx++]=b;indices[idx++]=c;indices[idx++]=d;
    }
  }
  geo.setAttribute('position',new THREE.BufferAttribute(verts,3));
  geo.setAttribute('color',new THREE.BufferAttribute(colors,3));
  geo.setIndex(new THREE.BufferAttribute(indices,1));
  geo.computeVertexNormals();
  terrainGeoCache.set(key,geo);
  return geo;
}
// Terrain mesh — single instance, swap geometry on slice change
const terrainMat=new THREE.MeshStandardMaterial({vertexColors:true,flatShading:false,roughness:0.7,metalness:0.05});
const terrainMesh=new THREE.Mesh(getTerrainGeometry(activeDataset,0),terrainMat);
scene.add(terrainMesh);
// ── River cache ──
const riverCache=new Map(); // key -> TubeGeometry
let riverGroup=new THREE.Group();
scene.add(riverGroup);
function buildRiverGeometry(path,heightFn,sliceIdx){
  const key=`river_${activeDataset}_${sliceIdx}_${path.length}`;
  if(riverCache.has(key)){cacheHit();return riverCache.get(key).clone()}
  cacheMiss();
  const pts=[];
  for(let i=0;i<path.length;i++){
    const p=path[i];
    const h=heightFn(sliceIdx,p.x,p.z);
    pts.push(new THREE.Vector3((p.x-0.5)*8,h*3+0.04,(p.z-0.5)*6));
  }
  if(pts.length<2)return null;
  const curve=new THREE.CatmullRomCurve3(pts);
  const geo=new THREE.TubeGeometry(curve,48,0.06,6,false);
  riverCache.set(key,geo);
  return geo.clone();
}
// River rebuild with 200ms debounce
let riverDebounceTimer=null;
let pendingRiverSlice=-1;
function rebuildRivers(sliceIdx){
  if(riverDebounceTimer!==null){
    pendingRiverSlice=sliceIdx;
    return;
  }
  _doRebuildRivers(sliceIdx);
  riverDebounceTimer=setTimeout(()=>{
    riverDebounceTimer=null;
    if(pendingRiverSlice>=0&&pendingRiverSlice!==sliceIdx){
      const ps=pendingRiverSlice;pendingRiverSlice=-1;
      _doRebuildRivers(ps);
    }
  },200);
}
function _doRebuildRivers(sliceIdx){
  riverGroup.clear();
  const anomalies=ds.getAnomalies(sliceIdx);
  const mat=new THREE.MeshStandardMaterial({color:'#ff4444',roughness:0.3,metalness:0.2,emissive:'#440000',emissiveIntensity:0.5});
  for(const path of anomalies){
    const geo=buildRiverGeometry(path,ds.getHeight.bind(ds),sliceIdx);
    if(geo){const mesh=new THREE.Mesh(geo,mat);riverGroup.add(mesh)}
  }
}
// ── Particle system with pool (reuse, no per-frame alloc) ──
const MAX_PARTICLES=600;
const particlePositions=new Float32Array(MAX_PARTICLES*3);
const particleColors=new Float32Array(MAX_PARTICLES*3);
// Particle state pool: {active,flowIdx,segment,progress,life,speed}
const particlePool=[];
for(let i=0;i<MAX_PARTICLES;i++){
  particlePool.push({active:false,flowIdx:0,segment:0,progress:0,life:0,speed:0.15+Math.random()*0.25,pathX:0,pathZ:0});
  // init offscreen
  particlePositions[i*3]=0;particlePositions[i*3+1]=-10;particlePositions[i*3+2]=0;
  particleColors[i*3]=0.3;particleColors[i*3+1]=0.8;particleColors[i*3+2]=1;
}
const particleGeo=new THREE.BufferGeometry();
particleGeo.setAttribute('position',new THREE.BufferAttribute(particlePositions,3));
particleGeo.setAttribute('color',new THREE.BufferAttribute(particleColors,3));
particleGeo.setDrawRange(0,0);
const particleMat=new THREE.PointsMaterial({size:0.06,vertexColors:true,blending:THREE.AdditiveBlending,depthWrite:false,transparent:true,opacity:0.85});
const particlePoints=new THREE.Points(particleGeo,particleMat);
scene.add(particlePoints);
function spawnParticle(flowPaths,sliceIdx){
  for(let i=0;i<MAX_PARTICLES;i++){
    const p=particlePool[i];
    if(!p.active){
      const fi=Math.floor(Math.random()*flowPaths.length);
      p.active=true;p.flowIdx=fi;p.segment=0;p.progress=0;
      p.life=2+Math.random()*3;p.speed=0.12+Math.random()*0.3;
      const flow=flowPaths[fi];
      if(flow.length>0){p.pathX=flow[0].x;p.pathZ=flow[0].z}
      const h=ds.getHeight(sliceIdx,p.pathX,p.pathZ);
      particlePositions[i*3]=(p.pathX-0.5)*8;
      particlePositions[i*3+1]=h*3+0.15;
      particlePositions[i*3+2]=(p.pathZ-0.5)*6;
      particleGeo.attributes.position.needsUpdate=true;
      return;
    }
  }
}
function updateParticles(dt,sliceIdx){
  const flows=ds.getFlows(sliceIdx);
  let activeCount=0;
  for(let i=0;i<MAX_PARTICLES;i++){
    const p=particlePool[i];
    if(!p.active)continue;
    p.life-=dt;
    if(p.life<=0){p.active=false;
      particlePositions[i*3+1]=-10; // hide below terrain
      continue;
    }
    const flow=flows[p.flowIdx];
    if(!flow||flow.length<2){p.active=false;continue}
    p.progress+=p.speed*dt;
    if(p.progress>=1){p.progress-=1;p.segment++;
      if(p.segment>=flow.length-1){
        // Loop or deactivate
        p.segment=0;p.progress=0;
        p.pathX=flow[0].x;p.pathZ=flow[0].z;
      }
    }
    const seg=p.segment;
    const a=flow[seg],b=flow[Math.min(seg+1,flow.length-1)];
    const px=a.x+(b.x-a.x)*p.progress;
    const pz=a.z+(b.z-a.z)*p.progress;
    p.pathX=px;p.pathZ=pz;
    // PER-FRAME height sampling from time-varying heightfield (teacher fix)
    const h=ds.getHeight(sliceIdx,px,pz);
    particlePositions[i*3]=(px-0.5)*8;
    particlePositions[i*3+1]=h*3+0.15;
    particlePositions[i*3+2]=(pz-0.5)*6;
    // Color fade with life
    const alpha=p.life/3;
    particleColors[i*3]=0.3+alpha*0.7;
    particleColors[i*3+1]=0.5+alpha*0.5;
    particleColors[i*3+2]=alpha;
    activeCount++;
  }
  particleGeo.attributes.position.needsUpdate=true;
  particleGeo.attributes.color.needsUpdate=true;
  particleGeo.setDrawRange(0,activeCount);
  document.getElementById('d-part').textContent=activeCount;
}
// ── Time slider ──
let currentSlice=0;
const slider=document.getElementById('time-slider');
const timeVal=document.getElementById('time-value');
slider.addEventListener('input',()=>{
  currentSlice=parseInt(slider.value);
  timeVal.textContent=currentSlice+' / '+(ds.numSlices-1);
  document.getElementById('d-slice').textContent=currentSlice;
  // Swap terrain geometry (from cache — lazy-init ensures it exists)
  terrainMesh.geometry=getTerrainGeometry(activeDataset,currentSlice);
  rebuildRivers(currentSlice);
});
slider.max=ds.numSlices-1;
timeVal.textContent='0 / '+(ds.numSlices-1);
// ── Bookmarks ──
window.setBookmark=function(i){
  const b=bookmarks[i];
  // Smooth animate
  const startPos=camera.position.clone();
  const startTarget=controls.target.clone();
  const endPos=new THREE.Vector3(...b.pos);
  const endTarget=new THREE.Vector3(...b.target);
  const startTime=performance.now();
  const duration=800;
  function anim(now){
    const t=Math.min((now-startTime)/duration,1);
    const ease=t<0.5?2*t*t:-1+(4-2*t)*t; // easeInOutQuad
    camera.position.lerpVectors(startPos,endPos,ease);
    controls.target.lerpVectors(startTarget,endTarget,ease);
    controls.update();
    if(t<1)requestAnimationFrame(anim);
  }
  requestAnimationFrame(anim);
};
window.toggleRotate=function(){
  controls.autoRotate=!controls.autoRotate;
  document.getElementById('btn-rot').classList.toggle('active',controls.autoRotate);
};
window.switchDataset=function(){
  activeDataset=(activeDataset+1)%datasets.length;
  ds=datasets[activeDataset];
  slider.max=ds.numSlices-1;
  currentSlice=0;slider.value=0;
  timeVal.textContent='0 / '+(ds.numSlices-1);
  document.getElementById('d-slice').textContent=0;
  terrainMesh.geometry=getTerrainGeometry(activeDataset,0);
  rebuildRivers(0);
  // Reset particles — deactivate all
  for(let i=0;i<MAX_PARTICLES;i++){
    particlePool[i].active=false;
    particlePositions[i*3+1]=-10;
  }
  particleGeo.attributes.position.needsUpdate=true;
  particleGeo.setDrawRange(0,0);
};
// ── Spawn particles periodically ──
let spawnTimer=0;
function spawnBatch(dt,sliceIdx){
  spawnTimer+=dt;
  const interval=0.08;
  while(spawnTimer>=interval){
    spawnTimer-=interval;
    spawnParticle(ds.getFlows(sliceIdx),sliceIdx);
  }
}
// ── Render loop ──
let lastTime=performance.now();
let fpsUpdateTimer=0;
function animate(now){
  requestAnimationFrame(animate);
  const rawDt=(now-lastTime)/1000;
  // Clamp deltaTime to avoid spiral of death, but USE actual value (teacher fix)
  const dt=Math.min(rawDt,0.1);
  lastTime=now;
  controls.update();
  updateParticles(dt,currentSlice);
  spawnBatch(dt,currentSlice);
  renderer.render(scene,camera);
  // FPS ring buffer
  fpsRing.push(rawDt>0?1/rawDt:60);
  fpsUpdateTimer+=rawDt;
  if(fpsUpdateTimer>=0.5){
    fpsUpdateTimer=0;
    document.getElementById('d-fps').textContent=Math.round(fpsRing.avg());
  }
}
requestAnimationFrame(animate);
// ── Initial river build ──
rebuildRivers(0);
// ── Resize ──
window.addEventListener('resize',()=>{
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});
// ── Keyboard shortcuts ──
window.addEventListener('keydown',e=>{
  if(e.key==='r'){toggleRotate()}
  if(e.key>='1'&&e.key<='3'){setBookmark(parseInt(e.key)-1)}
  if(e.key==='ArrowLeft'){slider.value=Math.max(0,currentSlice-1);slider.dispatchEvent(new Event('input'))}
  if(e.key==='ArrowRight'){slider.value=Math.min(ds.numSlices-1,currentSlice+1);slider.dispatchEvent(new Event('input'))}
});
</script>
</body>
</html>
```