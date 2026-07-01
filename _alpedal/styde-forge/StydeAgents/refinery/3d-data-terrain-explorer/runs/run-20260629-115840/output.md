<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>3D Data Terrain Explorer</title><style>
*{margin:0;padding:0;box-sizing:border-box}body{overflow:hidden;background:#0a0a14;font-family:system-ui,sans-serif}
#canvas{display:block}#ui{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:12px;align-items:center;z-index:10;background:rgba(10,10,24,.85);padding:10px 20px;border-radius:12px;backdrop-filter:blur(10px)}
#time-slider{width:300px;accent-color:#4fc3f7}#time-label{color:#ccc;font-size:13px;min-width:80px;text-align:center}
button{background:#1a1a2e;border:1px solid #333;color:#ccc;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:12px;transition:all .2s}
button:hover{background:#2a2a3e;border-color:#4fc3f7;color:#fff}button.active{background:#0d3b4f;border-color:#4fc3f7;color:#4fc3f7}
#bookmarks{position:fixed;top:20px;right:20px;display:flex;flex-direction:column;gap:4px;z-index:10}#cache-panel{position:fixed;top:20px;left:20px;color:#4fc3f7;font-size:11px;z-index:10;background:rgba(10,10,24,.8);padding:8px 12px;border-radius:8px;font-family:monospace}
#tooltip{position:fixed;pointer-events:none;color:#fff;font-size:12px;z-index:20;background:rgba(0,0,0,.8);padding:4px 8px;border-radius:4px;display:none}
</style></head><body><canvas id="canvas"></canvas>
<div id="cache-panel">cache: 0 hit / 0 miss</div>
<div id="bookmarks"></div>
<div id="tooltip"></div>
<div id="ui">
  <button id="btn-auto-rotate">AutoRotate</button>
  <button id="btn-bookmark">Save View</button>
  <input type="range" id="time-slider" min="0" max="0" value="0">
  <span id="time-label">t=0</span>
</div>
<script type="importmap">{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// ===== SYNTHETIC DATA: 24 time steps, 64x64 grid =====
const STEPS=24, GRID=64;
const ds=[]; // data[step][y][x] = {revenue, users, errors, apiCalls}
for(let t=0;t<STEPS;t++){
  const plane=[];
  for(let y=0;y<GRID;y++){const row=[];for(let x=0;x<GRID;x++){
    const nx=x/GRID*2-1, ny=y/GRID*2-1;
    const tNorm=t/(STEPS-1);
    // revenue: compound terrain morphing over time
    const rev=0.3+0.2*Math.sin(nx*3+tNorm*4)*Math.cos(ny*2.5+tNorm*3)+0.15*Math.sin(nx*5+ny*4)*Math.cos(tNorm*2);
    // users: separate pattern for vegetation coloring
    const users=0.2+0.15*Math.cos(nx*4.5+tNorm*3)*Math.sin(ny*3.8+tNorm*2.5)+0.1*Math.sin((nx+ny)*6+tNorm*5);
    // errors: sparse anomaly clusters
    const err= Math.abs(Math.sin(nx*8+ny*7))<0.25&&Math.abs(Math.cos(nx*5-ny*4+tNorm*6))>0.7 ? 0.01+Math.random()*0.04 : 0;
    // apiCalls: flowing density
    const api=0.05+0.03*Math.sin(nx*2+ny*3+tNorm*8)*Math.cos(nx*3-ny*2+tNorm*6);
    row.push({revenue:Math.max(0,rev),users:Math.max(0,users),errors:err,apiCalls:Math.max(0,api)});
  }plane.push(row);}
  ds.push(plane);
}
// ===== CACHE SYSTEM (shared buffer pool, no cloning) =====
const cache={geom:{},noise:{},rivers:{},stats:{hit:0,miss:0}};
function cacheGet(k){if(cache.geom[k]){cache.stats.hit++;return cache.geom[k];}cache.stats.miss++;return null;}
function cacheSet(k,v){cache.geom[k]=v;}
// shared position/color pools — allocate once, reuse per rebuild
const posPool=new Float32Array(GRID*GRID*3);
const colPool=new Float32Array(GRID*GRID*3);
// ===== SCENE SETUP =====
const renderer=new THREE.WebGLRenderer({canvas:document.getElementById('canvas'),antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.shadowMap.enabled=true;
const scene=new THREE.Scene();
scene.fog=new THREE.FogExp2(0x0a0a14,0.00015);
const camera=new THREE.PerspectiveCamera(55,window.innerWidth/window.innerHeight,0.5,120);
camera.position.set(18,14,22);
camera.lookAt(0,0,0);
const controls=new OrbitControls(camera,renderer.domElement);
controls.enableDamping=true;controls.dampingFactor=0.08;
controls.autoRotate=true;controls.autoRotateSpeed=0.6;
controls.target.set(0,1.5,0);controls.update();
// lighting
scene.add(new THREE.AmbientLight(0x334466,1.8));
const sun=new THREE.DirectionalLight(0xffeedd,3.5);
sun.position.set(20,25,10);sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.far=80;
sun.shadow.camera.left=-20;sun.shadow.camera.right=20;sun.shadow.camera.top=20;sun.shadow.camera.bottom=-20;
scene.add(sun);
const fill=new THREE.DirectionalLight(0x446688,1.2);fill.position.set(-10,5,-15);scene.add(fill);
// ground reference plane
const groundGeo=new THREE.PlaneGeometry(60,60);groundGeo.rotateX(-Math.PI/2);
scene.add(new THREE.Mesh(groundGeo,new THREE.MeshStandardMaterial({color:0x111122,roughness:1})));
// ===== TERRAIN BUILDER (functional, caches geometry, reuses pools) =====
let terrainMesh=null, riverLine=null, particleSystem=null;
function buildTerrain(step){
  const ck=`terrain_${step}`;
  let geo=cacheGet(ck);
  if(!geo){
    const data=ds[step];
    // fill position pool — single pass over grid
    for(let y=0;y<GRID;y++)for(let x=0;x<GRID;x++){
      const i=(y*GRID+x)*3;
      posPool[i]=x/GRID*20-10;          // world X
      posPool[i+1]=data[y][x].revenue*10;// height = revenue * 10
      posPool[i+2]=y/GRID*20-10;         // world Z
    }
    // compute normals for pooled positions (in-place)
    const normals=new Float32Array(GRID*GRID*3);
    // build indices
    const indices=[];
    for(let y=0;y<GRID-1;y++)for(let x=0;x<GRID-1;x++){
      const a=y*GRID+x, b=a+1, c=a+GRID, d=c+1;
      indices.push(a,c,b, b,c,d);
    }
    // vertex normals: accumulate face normals
    for(let i=0;i<indices.length;i+=3){
      const ia=indices[i]*3,ib=indices[i+1]*3,ic=indices[i+2]*3;
      const ax=posPool[ib]-posPool[ia],ay=posPool[ib+1]-posPool[ia+1],az=posPool[ib+2]-posPool[ia+2];
      const bx=posPool[ic]-posPool[ia],by=posPool[ic+1]-posPool[ia+1],bz=posPool[ic+2]-posPool[ia+2];
      const nx=ay*bz-az*by, ny=az*bx-ax*bz, nz=ax*by-ay*bx;
      const len=Math.sqrt(nx*nx+ny*ny+nz*nz)||1;
      [ia,ib,ic].forEach(oi=>{normals[oi]+=nx/len;normals[oi+1]+=ny/len;normals[oi+2]+=nz/len;});
    }
    // normalize normals
    for(let i=0;i<normals.length;i+=3){const l=Math.sqrt(normals[i]**2+normals[i+1]**2+normals[i+2]**2)||1;normals[i]/=l;normals[i+1]/=l;normals[i+2]/=l;}
    // vertex colors: user density → vegetation gradient (green low, yellow mid, red high)
    for(let y=0;y<GRID;y++)for(let x=0;x<GRID;x++){
      const i=(y*GRID+x)*3;
      const u=data[y][x].users;
      // green→yellow→red via HSL-like blend
      const r=Math.min(1,u*4), g=Math.min(1,0.8-u*1.5), b=Math.max(0,0.2-u*1.2);
      colPool[i]=r;colPool[i+1]=Math.max(0.1,g);colPool[i+2]=Math.max(0.05,b);
    }
    // merge into shared BufferGeometry (no clone — share buffers)
    geo=new THREE.BufferGeometry();
    geo.setAttribute('position',new THREE.BufferAttribute(posPool,3));
    geo.setAttribute('color',new THREE.BufferAttribute(colPool,3));
    geo.setAttribute('normal',new THREE.BufferAttribute(normals,3));
    geo.setIndex(indices);
    geo.computeBoundingSphere(); // for frustum culling
    cacheSet(ck,geo);
  }
  // swap mesh geometry (reuse mesh, only replace geometry ref)
  if(!terrainMesh){
    const mat=new THREE.MeshStandardMaterial({vertexColors:true,roughness:0.7,metalness:0.1,flatShading:false});
    terrainMesh=new THREE.Mesh(geo,mat);
    terrainMesh.castShadow=true;terrainMesh.receiveShadow=true;
    scene.add(terrainMesh);
  }else{terrainMesh.geometry=geo;}
}
// ===== RIVER BUILDER (cached TubeGeometry per step, debounced) =====
let riverTimeout=null;
function buildRivers(step){
  const rk=`river_${step}`;
  let tube=cacheGet(rk);
  if(tube){if(riverLine)riverLine.geometry=tube;return;}
  // trace error anomaly paths: find highest-error spine across grid
  const data=ds[step];
  // find connected error regions via simple flood (top 10 error cells as seed)
  const errCells=[];
  for(let y=0;y<GRID;y++)for(let x=0;x<GRID;x++)if(data[y][x].errors>0.02)errCells.push({x,y,e:data[y][x].errors});
  errCells.sort((a,b)=>b.e-a.e);
  const seeds=errCells.slice(0,8); // top 8 error seeds
  if(seeds.length<2){
    if(riverLine){riverLine.visible=false;}return;
  }
  // build river path as CatmullRom curve through seed centers
  seeds.sort((a,b)=>a.x-b.x); // sort left to right for coherent flow
  const pts=seeds.map(s=>new THREE.Vector3(s.x/GRID*20-10, data[s.y][s.x].revenue*10+0.25, s.y/GRID*20-10));
  const curve=new THREE.CatmullRomCurve3(pts);
  const tubularSegments=Math.min(pts.length*16,128);
  tube=new THREE.TubeGeometry(curve,tubularSegments,0.15,6,false);
  cacheSet(rk,tube);
  if(!riverLine){
    const rmat=new THREE.MeshStandardMaterial({color:0xff2244,emissive:0x440000,roughness:0.3,metalness:0.4});
    riverLine=new THREE.Mesh(tube,rmat);riverLine.renderOrder=1;
    riverLine.material.depthTest=true;riverLine.material.depthWrite=true;
    scene.add(riverLine);
  }else{riverLine.geometry=tube;riverLine.visible=true;}
}
// ===== PARTICLE SYSTEM (reuses position array, no per-frame alloc) =====
const PARTICLE_COUNT=800;
const particlePositions=new Float32Array(PARTICLE_COUNT*3);
const particleColors=new Float32Array(PARTICLE_COUNT*3);
const particleData=[]; // {seedX, seedY, phase, speed} per particle
function buildParticles(step){
  const data=ds[step];
  // precompute particle seeds from apiCalls density map (once per step, cached)
  const pk=`particles_${step}`;
  let cachedSeeds=cacheGet(pk);
  if(!cachedSeeds){
    const seeds=[];
    for(let y=0;y<GRID;y++)for(let x=0;x<GRID;x++){
      const density=data[y][x].apiCalls;
      const count=Math.floor(density*30);
      for(let k=0;k<count;k++)seeds.push({x:x/GRID*20-10+(Math.random()-0.5)*0.4, y:data[y][x].revenue*10, z:y/GRID*20-10+(Math.random()-0.5)*0.4, phase:Math.random()*Math.PI*2, speed:0.3+Math.random()*0.7});
    }
    cachedSeeds=seeds;cacheSet(pk,cachedSeeds);
  }
  // populate particleData from seeds (spiral fill if more seeds than particles)
  for(let i=0;i<PARTICLE_COUNT;i++){
    const s=cachedSeeds[i%cachedSeeds.length];
    if(!particleData[i])particleData.push({...s});
    else Object.assign(particleData[i],s);
    // init position slightly offset
    const off=particleData[i].phase;
    particlePositions[i*3]=particleData[i].x+Math.cos(off)*0.2;
    particlePositions[i*3+1]=particleData[i].y+0.3;
    particlePositions[i*3+2]=particleData[i].z+Math.sin(off)*0.2;
    // cyan-to-white gradient
    particleColors[i*3]=0.3;particleColors[i*3+1]=0.8;particleColors[i*3+2]=1.0;
  }
  if(!particleSystem){
    const pgeo=new THREE.BufferGeometry();
    pgeo.setAttribute('position',new THREE.BufferAttribute(particlePositions,3));
    pgeo.setAttribute('color',new THREE.BufferAttribute(particleColors,3));
    const pmat=new THREE.PointsMaterial({size:0.12,vertexColors:true,blending:THREE.AdditiveBlending,depthWrite:false,transparent:true,opacity:0.85});
    particleSystem=new THREE.Points(pgeo,pmat);particleSystem.renderOrder=2;
    scene.add(particleSystem);
  }
}
// ===== UPDATE PARTICLES EACH FRAME (reuse arrays, no allocations) =====
const _tmpV=new THREE.Vector3(); // pre-allocated temp vector for terrain lookups
function updateParticles(dt){
  if(!particleSystem)return;
  const pos=particleSystem.geometry.attributes.position.array;
  for(let i=0;i<PARTICLE_COUNT;i++){
    const pd=particleData[i], i3=i*3;
    // spiral orbit around seed point
    pd.phase+=pd.speed*dt*1.5;
    const rad=0.3+Math.sin(pd.phase*0.7)*0.2;
    pos[i3]=pd.x+Math.cos(pd.phase)*rad;
    pos[i3+1]=pd.y+0.15+Math.sin(pd.phase*1.3)*0.1; // bob
    pos[i3+2]=pd.z+Math.sin(pd.phase)*rad;
  }
  particleSystem.geometry.attributes.position.needsUpdate=true;
}
// ===== CAMERA BOOKMARKS =====
const bookmarks=JSON.parse(localStorage.getItem('terrainBookmarks')||'[]');
function saveBookmark(){
  bookmarks.push({pos:camera.position.toArray(),target:controls.target.toArray(),label:`View ${bookmarks.length+1}`});
  if(bookmarks.length>8)bookmarks.shift();
  localStorage.setItem('terrainBookmarks',JSON.stringify(bookmarks));
  renderBookmarks();
}
function loadBookmark(i){
  const b=bookmarks[i];if(!b)return;
  camera.position.fromArray(b.pos);controls.target.fromArray(b.target);controls.update();
}
function renderBookmarks(){
  const el=document.getElementById('bookmarks');
  el.innerHTML=bookmarks.map((b,i)=>`<button onclick="window._loadBM(${i})" title="${b.label}">${b.label}</button>`).join('');
  window._loadBM=loadBookmark;
}
// ===== UI BINDINGS =====
const slider=document.getElementById('time-slider');
const label=document.getElementById('time-label');
const cachePanel=document.getElementById('cache-panel');
slider.max=STEPS-1;slider.value=0;
function applyStep(step){
  label.textContent=`t=${step}/${STEPS-1}`;
  buildTerrain(step);
  // debounce river rebuild (200ms)
  if(riverTimeout)clearTimeout(riverTimeout);
  riverTimeout=setTimeout(()=>buildRivers(step),200);
  buildParticles(step);
  cachePanel.textContent=`cache: ${cache.stats.hit} hit / ${cache.stats.miss} miss`;
}
slider.addEventListener('input',()=>applyStep(parseInt(slider.value)));
document.getElementById('btn-auto-rotate').addEventListener('click',function(){
  controls.autoRotate=!controls.autoRotate;this.classList.toggle('active',controls.autoRotate);
});
document.getElementById('btn-bookmark').addEventListener('click',saveBookmark);
// ===== HOVER TOOLTIP (memoized world-to-grid) =====
const raycaster=new THREE.Raycaster();
const tooltip=document.getElementById('tooltip');
let lastGridKey=''; // memoization: skip recompute if same cell
window.addEventListener('mousemove',e=>{
  if(!terrainMesh)return;
  const mouse=new THREE.Vector2((e.clientX/window.innerWidth)*2-1,-(e.clientY/window.innerHeight)*2+1);
  raycaster.setFromCamera(mouse,camera);
  const hits=raycaster.intersectObject(terrainMesh);
  if(hits.length>0){
    const p=hits[0].point;
    // world-to-grid (memoize by snapped cell)
    const gx=Math.round((p.x/20+0.5)*GRID), gy=Math.round((p.z/20+0.5)*GRID);
    const key=`${gx},${gy}`;
    if(key!==lastGridKey){
      lastGridKey=key;
      if(gx>=0&&gx<GRID&&gy>=0&&gy<GRID){
        const d=ds[parseInt(slider.value)][gy][gx];
        tooltip.style.display='block';
        tooltip.innerHTML=`rev:${(d.revenue*100).toFixed(1)}% users:${(d.users*100).toFixed(1)}% err:${(d.errors*100).toFixed(2)}% api:${(d.apiCalls*100).toFixed(1)}%`;
      }
    }
    tooltip.style.left=e.clientX+15+'px';tooltip.style.top=e.clientY-20+'px';
  }else{tooltip.style.display='none';lastGridKey='';}
});
// ===== RESIZE =====
window.addEventListener('resize',()=>{camera.aspect=window.innerWidth/window.innerHeight;camera.updateProjectionMatrix();renderer.setSize(window.innerWidth,window.innerHeight);});
// ===== RENDER LOOP =====
const clock=new THREE.Clock();
function animate(){
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),0.1);
  controls.update();
  updateParticles(dt);
  renderer.render(scene,camera);
}
// ===== INIT =====
applyStep(0);
renderBookmarks();
document.getElementById('btn-auto-rotate').classList.add('active');
animate();
// expose for bookmark buttons
window.loadBookmark=loadBookmark;
</script></body></html>