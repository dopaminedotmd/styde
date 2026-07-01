<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a14;overflow:hidden;font-family:system-ui}
canvas{display:block}
#panel{position:fixed;top:12px;left:12px;background:rgba(10,10,20,0.85);color:#a0b8d0;padding:10px 14px;border-radius:6px;font-size:11px;line-height:1.5;z-index:10;pointer-events:none}
#panel span{color:#60d0a0;font-weight:600}
#timebar{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:10px;align-items:center;background:rgba(10,10,20,0.85);padding:8px 16px;border-radius:6px}
#timebar label{color:#a0b8d0;font-size:12px}
#timebar input{width:260px;accent-color:#60d0a0}
#timebar button{background:#2a3a50;color:#a0b8d0;border:1px solid #3a4a60;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px}
#timebar button:hover{background:#3a5a70}
#bookmarks{position:fixed;top:12px;right:12px;z-index:10;display:flex;flex-direction:column;gap:4px}
#bookmarks button{background:rgba(10,10,20,0.85);color:#a0b8d0;border:1px solid #3a4a60;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px}
#bookmarks button:hover{background:#3a5a70}
</style>
</head>
<body>
<div id="panel">Time: <span id="tlabel">T0</span> | FPS: <span id="fps">0</span> | Cache: <span id="chits">0</span>h/<span id="cmiss">0</span>m</div>
<div id="bookmarks">
<button onclick="saveBookmark()">Save View</button>
<button onclick="loadBookmark(0)">View 1</button>
<button onclick="loadBookmark(1)">View 2</button>
<button onclick="loadBookmark(2)">View 3</button>
</div>
<div id="timebar">
<label>Time Step</label>
<input type="range" id="slider" min="0" max="11" value="0" step="1">
<button id="playbtn">Play</button>
<button id="autorotbtn">AutoRot</button>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ---- DATA GENERATION: 12 time steps, 80x80 grid ----
const W=80, H=80, STEPS=12;
const data=[]; // data[t][y][x] = {elevation, vegetation, error}
for(let t=0;t<STEPS;t++){
  const grid=[];
  for(let y=0;y<H;y++){
    const row=[];
    for(let x=0;x<W;x++){
      const nx=x/W-0.5, ny=y/H-0.5;
      const phase=t*0.5;
      const elev=2.5*Math.sin(nx*6+phase)*Math.cos(ny*5+phase*0.7)+1.2*Math.sin(nx*12-ny*8+phase*1.3)+0.8*Math.cos(nx*3+ny*3-phase);
      const veg=0.5+0.5*Math.sin(nx*8+ny*6+t*0.3);
      const err=Math.max(0,0.35-Math.abs(nx-0.15-Math.sin(t*0.4)*0.25)-Math.abs(ny+0.1-Math.cos(t*0.35)*0.2));
      row.push({elevation:elev,vegetation:veg,error:err});
    }
    grid.push(row);
  }
  data.push(grid);
}
// ---- SCENE SETUP ----
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x0a0a18);
scene.fog=new THREE.Fog(0x0a0a18,15,60);
const camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,0.5,100);
camera.position.set(8,9,12);
camera.lookAt(0,1.5,0);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(innerWidth,innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.shadowMap.enabled=true;
document.body.appendChild(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.target.set(0,1.5,0);
controls.maxPolarAngle=Math.PI*0.55;
controls.minDistance=5;
controls.maxDistance=30;
controls.autoRotate=false;
controls.autoRotateSpeed=0.4;
controls.update();
// ---- LIGHTING ----
const ambient=new THREE.AmbientLight(0x2a3a50,1.5);
scene.add(ambient);
const sun=new THREE.DirectionalLight(0xffeedd,3.5);
sun.position.set(15,20,10);
sun.castShadow=true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.near=1;
sun.shadow.camera.far=60;
sun.shadow.camera.left=-15;
sun.shadow.camera.right=15;
sun.shadow.camera.top=15;
sun.shadow.camera.bottom=-15;
scene.add(sun);
const fill=new THREE.DirectionalLight(0x4466aa,1.2);
fill.position.set(-5,3,-5);
scene.add(fill);
// ---- GROUND GRID ----
const gridHelper=new THREE.PolarGridHelper(12,32,24,64,0x1a2a3a,0x1a2a3a);
gridHelper.position.y=-3;
scene.add(gridHelper);
// ---- CACHE SYSTEM ----
const cache={geometries:{},rivers:{},particlePositions:{}};
let cacheHits=0,cacheMisses=0;
const cacheLog=(hit)=>{if(hit)cacheHits++;else cacheMisses++;};
// ---- TERRAIN BUILDER ----
// Cache terrain geometry per time step; rebuild only on cache miss
function buildTerrainGeometry(t){
  if(cache.geometries[t]){cacheLog(true);return cache.geometries[t].clone();}
  cacheLog(false);
  const geo=new THREE.BufferGeometry();
  const verts=[],colors=[],indices=[];
  const grid=data[t];
  // Build vertex grid with elevation + color
  for(let y=0;y<H;y++){
    for(let x=0;x<W;x++){
      const d=grid[y][x];
      const px=(x/(W-1)-0.5)*10;
      const pz=(y/(H-1)-0.5)*10;
      const py=d.elevation;
      verts.push(px,py,pz);
      // Vegetation green gradient; error areas get red tint
      const vegCol=new THREE.Color().setHSL(0.25+0.15*d.vegetation,0.7,0.3+0.4*d.vegetation);
      if(d.error>0.15){vegCol.lerp(new THREE.Color(0xff3300),d.error*2.5);}
      colors.push(vegCol.r,vegCol.g,vegCol.b);
    }
  }
  // Indices for triangle strips
  for(let y=0;y<H-1;y++){
    for(let x=0;x<W-1;x++){
      const a=y*W+x, b=a+1, c=a+W, d=c+1;
      indices.push(a,b,c, b,d,c);
    }
  }
  geo.setIndex(indices);
  geo.setAttribute('position',new THREE.Float32BufferAttribute(verts,3));
  geo.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));
  geo.computeVertexNormals();
  cache.geometries[t]=geo;
  return geo.clone();
}
// ---- RIVER BUILDER ----
// Trace error paths along high-error corridors; debounced on slider change
let riverDebounceTimer=null;
function buildRiverGeometry(t){
  if(cache.rivers[t]){cacheLog(true);return cache.rivers[t].clone();}
  cacheLog(false);
  const grid=data[t];
  const paths=[];
  // Find high-error seed points
  const seeds=[];
  for(let y=5;y<H-5;y+=8){
    for(let x=8;x<W-8;x+=12){
      if(grid[y][x].error>0.18)seeds.push({x,y,e:grid[y][x].error});
    }
  }
  seeds.sort((a,b)=>b.e-a.e);
  const topSeeds=seeds.slice(0,6);
  // Trace downstream from each seed (greedy descent on elevation)
  for(const seed of topSeeds){
    const pts=[];
    let cx=seed.x, cy=seed.y;
    for(let step=0;step<40;step++){
      if(cx<0||cx>=W||cy<0||cy>=H)break;
      const d=grid[Math.round(cy)][Math.round(cx)];
      const px=(cx/(W-1)-0.5)*10;
      const pz=(cy/(H-1)-0.5)*10;
      pts.push(new THREE.Vector3(px,d.elevation+0.06,pz));
      // Move toward steepest descent
      let bestD=Infinity,bestNX=cx,bestNY=cy;
      for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]){
        const nx=cx+dx*1.2, ny=cy+dy*1.2;
        if(nx<0||nx>=W-1||ny<0||ny>=H-1)continue;
        const nd=grid[Math.round(ny)][Math.round(nx)];
        if(nd.elevation<bestD){bestD=nd.elevation;bestNX=nx;bestNY=ny;}
      }
      if(bestD>=d.elevation)break; // local minimum
      cx=bestNX;cy=bestNY;
    }
    if(pts.length>2)paths.push(pts);
  }
  // Merge paths into one geometry group
  const group=new THREE.Group();
  for(const pts of paths){
    if(pts.length<3)continue;
    const curve=new THREE.CatmullRomCurve3(pts);
    const tubeGeo=new THREE.TubeGeometry(curve,32,0.06,6,false);
    const mat=new THREE.MeshStandardMaterial({color:0xff4422,emissive:0x331111,roughness:0.4,metalness:0.2});
    group.add(new THREE.Mesh(tubeGeo,mat));
  }
  cache.rivers[t]=group;
  return group.clone(true);
}
// ---- PARTICLE SYSTEM ----
// Reuse position array; update in-place per frame, no per-particle allocations
const PARTICLE_COUNT=1800;
const particleGeo=new THREE.BufferGeometry();
const particlePositions=new Float32Array(PARTICLE_COUNT*3);
const particleVelocities=new Float32Array(PARTICLE_COUNT*3); // stored separately
const particleAges=new Float32Array(PARTICLE_COUNT);
// Initialize particles with random positions + flow directions
for(let i=0;i<PARTICLE_COUNT;i++){
  particlePositions[i*3]=(Math.random()-0.5)*10;
  particlePositions[i*3+1]=Math.random()*4-1;
  particlePositions[i*3+2]=(Math.random()-0.5)*10;
  particleVelocities[i*3]=(Math.random()-0.5)*0.3;
  particleVelocities[i*3+1]=(Math.random()-0.5)*0.1;
  particleVelocities[i*3+2]=(Math.random()-0.5)*0.3;
  particleAges[i]=Math.random()*2;
}
particleGeo.setAttribute('position',new THREE.Float32BufferAttribute(particlePositions,3));
const particleMat=new THREE.PointsMaterial({color:0x88ccff,size:0.06,blending:THREE.AdditiveBlending,depthWrite:false,transparent:true,opacity:0.7});
const particles=new THREE.Points(particleGeo,particleMat);
scene.add(particles);
// ---- SCENE OBJECTS ----
let terrainMesh, riverGroup, currentStep=0;
function loadStep(t){
  currentStep=t;
  // Remove old
  if(terrainMesh){terrainMesh.geometry.dispose();terrainMesh.material.dispose();scene.remove(terrainMesh);}
  if(riverGroup){riverGroup.traverse(c=>{if(c.geometry)c.geometry.dispose();if(c.material)c.material.dispose();});scene.remove(riverGroup);}
  // Build new
  const geo=buildTerrainGeometry(t);
  const mat=new THREE.MeshStandardMaterial({vertexColors:true,roughness:0.65,metalness:0.15,flatShading:false});
  terrainMesh=new THREE.Mesh(geo,mat);
  terrainMesh.castShadow=true;
  terrainMesh.receiveShadow=true;
  scene.add(terrainMesh);
  // Debounce river rebuild (200ms)
  if(riverDebounceTimer)clearTimeout(riverDebounceTimer);
  riverDebounceTimer=setTimeout(()=>{
    riverGroup=buildRiverGeometry(t);
    if(riverGroup)scene.add(riverGroup);
    document.getElementById('tlabel').textContent='T'+t;
  },200);
  document.getElementById('tlabel').textContent='T'+t+' (loading rivers...)';
}
// ---- PARTICLE UPDATE (per frame, zero allocation) ----
function updateParticles(dt,timeStep){
  const grid=data[timeStep];
  const pos=particleGeo.attributes.position.array;
  for(let i=0;i<PARTICLE_COUNT;i++){
    const i3=i*3;
    particleAges[i]+=dt;
    if(particleAges[i]>2.5){
      // Respawn
      pos[i3]=(Math.random()-0.5)*10;
      pos[i3+1]=Math.random()*3+1;
      pos[i3+2]=(Math.random()-0.5)*10;
      particleVelocities[i3]=(Math.random()-0.5)*0.3;
      particleVelocities[i3+1]=Math.random()*0.15;
      particleVelocities[i3+2]=(Math.random()-0.5)*0.3;
      particleAges[i]=0;
      continue;
    }
    // Move particle along flow field (slight drift toward lower elevation)
    const gx=Math.round((pos[i3]/10+0.5)*(W-1));
    const gz=Math.round((pos[i3+2]/10+0.5)*(H-1));
    if(gx>=0&&gx<W&&gz>=0&&gz<H){
      const cell=grid[gz][gx];
      const targetY=cell.elevation+0.3;
      pos[i3+1]+=(targetY-pos[i3+1])*dt*1.5; // float toward terrain surface
      // Bias velocity toward lower neighbor
      let bestY=cell.elevation,bdx=0,bdz=0;
      for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){
        const nx=gx+dx,nz=gz+dz;
        if(nx<0||nx>=W||nz<0||nz>=H)continue;
        if(grid[nz][nx].elevation<bestY){bestY=grid[nz][nx].elevation;bdx=dx;bdz=dz;}
      }
      particleVelocities[i3]+=bdx*dt*0.4;
      particleVelocities[i3+2]+=bdz*dt*0.4;
    }
    // Damp velocity
    particleVelocities[i3]*=0.98;
    particleVelocities[i3+1]*=0.98;
    particleVelocities[i3+2]*=0.98;
    pos[i3]+=particleVelocities[i3]*dt;
    pos[i3+1]+=particleVelocities[i3+1]*dt;
    pos[i3+2]+=particleVelocities[i3+2]*dt;
    // Keep in bounds
    if(pos[i3]<-5.5)pos[i3]=-5.5;
    if(pos[i3]>5.5)pos[i3]=5.5;
    if(pos[i3+2]<-5.5)pos[i3+2]=-5.5;
    if(pos[i3+2]>5.5)pos[i3+2]=5.5;
  }
  particleGeo.attributes.position.needsUpdate=true;
}
// ---- CAMERA BOOKMARKS ----
const bookmarks=[{pos:[8,9,12],target:[0,1.5,0]},{pos:[-10,7,3],target:[0,1,0]},{pos:[0,14,0.5],target:[0,2,0]}];
let bookmarkStore=[...bookmarks];
window.saveBookmark=()=>{
  bookmarkStore.push({pos:camera.position.toArray(),target:controls.target.toArray()});
};
window.loadBookmark=(i)=>{
  if(i>=bookmarkStore.length)return;
  const bm=bookmarkStore[i];
  camera.position.set(...bm.pos);
  controls.target.set(...bm.target);
  controls.update();
};
// ---- UI HANDLERS ----
const slider=document.getElementById('slider');
slider.addEventListener('input',()=>loadStep(parseInt(slider.value)));
let playing=false,playInterval=null;
document.getElementById('playbtn').addEventListener('click',()=>{
  playing=!playing;
  document.getElementById('playbtn').textContent=playing?'Pause':'Play';
  if(playing){
    playInterval=setInterval(()=>{
      let v=(parseInt(slider.value)+1)%STEPS;
      slider.value=v;
      loadStep(v);
    },800);
  }else{clearInterval(playInterval);}
});
document.getElementById('autorotbtn').addEventListener('click',()=>{
  controls.autoRotate=!controls.autoRotate;
  document.getElementById('autorotbtn').textContent=controls.autoRotate?'AutoRot:ON':'AutoRot';
});
window.addEventListener('resize',()=>{
  camera.aspect=innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth,innerHeight);
});
// ---- RENDER LOOP ----
let lastTime=performance.now(),fpsCounter=0,fpsTime=0,fpsDisplay=0;
function animate(){
  requestAnimationFrame(animate);
  const now=performance.now();
  const dt=Math.min((now-lastTime)/1000,0.1);
  lastTime=now;
  controls.update();
  updateParticles(dt,currentStep);
  renderer.render(scene,camera);
  // FPS counter (update display every 500ms)
  fpsCounter++;
  fpsTime+=dt;
  if(fpsTime>=0.5){
    fpsDisplay=Math.round(fpsCounter/fpsTime);
    fpsCounter=0;fpsTime=0;
    document.getElementById('fps').textContent=fpsDisplay;
    document.getElementById('chits').textContent=cacheHits;
    document.getElementById('cmiss').textContent=cacheMisses;
  }
}
// ---- INITIAL LOAD ----
loadStep(0);
animate();
</script>
</body>
</html>