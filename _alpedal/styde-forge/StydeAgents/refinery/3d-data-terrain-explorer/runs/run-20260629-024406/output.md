<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
body{margin:0;overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;background:#0a0a14}
#ui{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none;z-index:10}
#ui>*{pointer-events:auto}
#panel{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);background:rgba(10,10,20,0.92);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:12px 18px;display:flex;gap:16px;align-items:center;backdrop-filter:blur(12px)}
#time-slider{width:240px;accent-color:#4fc3f7}
#time-label{color:#ccc;font-size:13px;min-width:100px;text-align:center;font-variant-numeric:tabular-nums}
#bookmarks{position:absolute;top:16px;right:16px;display:flex;flex-direction:column;gap:6px}
.bkmk-btn{background:rgba(10,10,20,0.85);border:1px solid rgba(255,255,255,0.15);color:#ccc;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:12px;transition:all 0.2s;backdrop-filter:blur(8px)}
.bkmk-btn:hover{background:rgba(79,195,247,0.2);border-color:#4fc3f7;color:#fff}
#legend{position:absolute;bottom:20px;right:20px;background:rgba(10,10,20,0.88);border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:10px 14px;font-size:11px;color:#aaa;backdrop-filter:blur(8px)}
.legend-row{display:flex;align-items:center;gap:8px;margin:4px 0}
.legend-swatch{width:12px;height:12px;border-radius:2px;flex-shrink:0}
#tooltip{position:absolute;pointer-events:none;background:rgba(0,0,0,0.85);color:#fff;padding:6px 10px;border-radius:4px;font-size:12px;display:none;white-space:nowrap}
#file-drop{position:absolute;top:16px;left:16px;background:rgba(10,10,20,0.85);border:2px dashed rgba(255,255,255,0.2);border-radius:10px;padding:10px 18px;color:#888;font-size:12px;cursor:pointer;transition:all 0.2s;backdrop-filter:blur(8px)}
#file-drop:hover{border-color:#4fc3f7;color:#ccc}
#file-drop.drag-over{border-color:#4fc3f7;background:rgba(79,195,247,0.1);color:#fff}
#file-input{display:none}
#status{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#4fc3f7;font-size:14px;pointer-events:none;opacity:0;transition:opacity 0.3s}
#auto-rotate-btn{position:absolute;top:16px;left:50%;transform:translateX(-50%);background:rgba(10,10,20,0.85);border:1px solid rgba(255,255,255,0.15);color:#ccc;padding:6px 16px;border-radius:6px;cursor:pointer;font-size:12px;backdrop-filter:blur(8px);transition:all 0.2s}
#auto-rotate-btn.active{background:rgba(79,195,247,0.3);border-color:#4fc3f7;color:#fff}
</style>
</head>
<body>
<div id="ui">
  <div id="status">Loading terrain...</div>
  <label id="file-drop" for="file-input">Drop CSV grid here or click to load</label>
  <input type="file" id="file-input" accept=".csv,.txt,.json">
  <button id="auto-rotate-btn" onclick="toggleAutoRotate()">Auto-Rotate</button>
  <div id="bookmarks">
    <button class="bkmk-btn" onclick="saveBookmark()">Save View</button>
    <div id="bookmark-list"></div>
  </div>
  <div id="panel">
    <span style="color:#888;font-size:12px">Time</span>
    <input type="range" id="time-slider" min="0" max="99" value="0" step="1">
    <span id="time-label">T=0</span>
  </div>
  <div id="legend">
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#1a237e,#4fc3f7,#fff9c4,#e53935)"></span>Elevation (Revenue)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:linear-gradient(to right,#1b5e20,#66bb6a)"></span>Vegetation (Density)</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#e53935"></span>Error Rivers</div>
    <div class="legend-row"><span class="legend-swatch" style="background:#ffd54f"></span>API Flow Particles</div>
  </div>
  <div id="tooltip"></div>
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
/* ── YAML frontmatter constraints ──
limits:
  max_vertices: 262144
  max_particles: 50000
  max_texture_size: 4096
  target_fps: 60
  terrain_resolution: [256, 256]
  time_steps: 100
  memory_budget_mb: 256
  render_distance: 80
*/
// ── Scene setup ──
const renderer = new THREE.WebGLRenderer({antialias:true,alpha:false});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.2;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a18);
scene.fog = new THREE.Fog(0x0a0a18,30,80);
const camera = new THREE.PerspectiveCamera(50,window.innerWidth/window.innerHeight,0.5,120);
camera.position.set(20,14,22);
camera.lookAt(0,2,0);
const controls = new OrbitControls(camera,renderer.domElement);
controls.target.set(0,2,0);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.autoRotate=false;
controls.autoRotateSpeed=0.4;
controls.minDistance=5;
controls.maxDistance=60;
controls.maxPolarAngle=Math.PI*0.48;
controls.update();
// ── Lighting ──
const ambient = new THREE.AmbientLight(0x334466,1.8);
scene.add(ambient);
const sun = new THREE.DirectionalLight(0xffeedd,4.5);
sun.position.set(25,30,15);
sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.near=0.5; sun.shadow.camera.far=100;
sun.shadow.camera.left=-25; sun.shadow.camera.right=25;
sun.shadow.camera.top=25; sun.shadow.camera.bottom=-25;
sun.shadow.bias=-0.0001;
scene.add(sun);
const fill = new THREE.DirectionalLight(0x4466aa,1.2);
fill.position.set(-10,5,-10);
scene.add(fill);
// ── Grid & ground plane ──
const gridHelper = new THREE.PolarGridHelper(18,32,24,64,0x222244,0x222244);
gridHelper.position.y=-0.5;
scene.add(gridHelper);
// ── Data model ──
const RES=256;
const TIME_STEPS=100;
let currentTime=0;
// Generate synthetic time-series data: revenue=height, density=vegetation, errors=river paths
const heightData = new Float32Array(TIME_STEPS*RES*RES);
const densityData = new Float32Array(TIME_STEPS*RES*RES);
const errorData = new Float32Array(TIME_STEPS*RES*RES);
function fbm(x,z,octaves=4){
  let v=0,amp=1,freq=1,sum=0;
  for(let i=0;i<octaves;i++){
    const sx=x*freq*0.7+1000,sy=z*freq*0.7+2000;
    const ix=Math.floor(sx),iy=Math.floor(sy);
    const fx=sx-ix,fy=sy-iy;
    const sx2=fx*fx*(3-2*fx),sy2=fy*fy*(3-2*fy);
    const n00=(Math.sin(ix*12.9898+iy*78.233)*43758.5453)%1;
    const n10=(Math.sin((ix+1)*12.9898+iy*78.233)*43758.5453)%1;
    const n01=(Math.sin(ix*12.9898+(iy+1)*78.233)*43758.5453)%1;
    const n11=(Math.sin((ix+1)*12.9898+(iy+1)*78.233)*43758.5453)%1;
    const nx0=n00+(n10-n00)*sx2, nx1=n01+(n11-n01)*sx2;
    v+=(nx0+(nx1-nx0)*sy2)*amp;
    sum+=amp; amp*=0.5; freq*=2;
  }
  return v/sum;
}
for(let t=0;t<TIME_STEPS;t++){
  const phase=t*0.06;
  const toff=TIME_STEPS*RES*RES;
  for(let iz=0;iz<RES;iz++){
    for(let ix=0;ix<RES;ix++){
      const idx=t*RES*RES+iz*RES+ix;
      const nx=ix/(RES-1)*2-1, nz=iz/(RES-1)*2-1;
      const dist=Math.sqrt(nx*nx+nz*nz);
      const h0=fbm(nx*3+phase,nz*3)*2.5+Math.sin(dist*2-phase)*1.5+Math.exp(-dist*1.8)*4;
      heightData[idx]=Math.max(0,h0);
      densityData[idx]=Math.max(0,0.3+fbm(nx*2.2+5+phase*0.7,nz*2.2)*0.7);
      const err=fbm(nx*4-phase*1.3,nz*4)*1.2;
      errorData[idx]=err>0.75?(err-0.75)*4:0;
    }
  }
}
// ── Terrain mesh (BufferGeometry with pre-allocated buffers) ──
const terrainGeo = new THREE.BufferGeometry();
const vertCount=(RES-1)*(RES-1)*6;
const posArr = new Float32Array(vertCount*3);
const colArr = new Float32Array(vertCount*3);
const normArr = new Float32Array(vertCount*3);
const idxArr = new Uint32Array(vertCount);
function buildTerrain(t){
  const H=t*RES*RES;
  let vi=0, ii=0;
  const sx=16/(RES-1), sz=16/(RES-1);
  const ox=-8, oz=-8;
  for(let iz=0;iz<RES-1;iz++){
    for(let ix=0;ix<RES-1;ix++){
      const a=H+iz*RES+ix, b=a+1, c=a+RES, d=c+1;
      const ha=heightData[a], hb=heightData[b], hc=heightData[c], hd=heightData[d];
      const da=densityData[a], db=densityData[b], dc=densityData[c], dd=densityData[d];
      const ea=errorData[a], eb=errorData[b], ec=errorData[c], ed=errorData[d];
      const x0=ox+ix*sx, x1=x0+sx;
      const z0=oz+iz*sz, z1=z0+sz;
      // Two triangles per cell
      const verts=[
        [x0,ha,z0,da,ea],[x1,hb,z0,db,eb],[x0,hc,z1,dc,ec],
        [x1,hb,z0,db,eb],[x1,hd,z1,dd,ed],[x0,hc,z1,dc,ec]
      ];
      for(const v of verts){
        const pi=vi*3;
        posArr[pi]=v[0]; posArr[pi+1]=v[1]; posArr[pi+2]=v[2];
        const elev=v[1]/7;
        const dens=v[3];
        colArr[pi]=0.1+elev*0.3+dens*0.2;
        colArr[pi+1]=0.15+elev*0.6+dens*0.4;
        colArr[pi+2]=0.25+elev*0.8+dens*0.1;
        idxArr[ii]=vi;
        vi++; ii++;
      }
    }
  }
  terrainGeo.setAttribute('position',new THREE.BufferAttribute(posArr,3));
  terrainGeo.setAttribute('color',new THREE.BufferAttribute(colArr,3));
  terrainGeo.setIndex(new THREE.BufferAttribute(idxArr,1));
  terrainGeo.computeVertexNormals();
  terrainGeo.attributes.position.needsUpdate=true;
  terrainGeo.attributes.color.needsUpdate=true;
}
buildTerrain(0);
const terrainMat = new THREE.MeshStandardMaterial({
  vertexColors:true, roughness:0.65, metalness:0.05, flatShading:false
});
const terrain = new THREE.Mesh(terrainGeo,terrainMat);
terrain.castShadow=true; terrain.receiveShadow=true;
scene.add(terrain);
// ── River geometry (error paths) ──
const riverGroup = new THREE.Group();
scene.add(riverGroup);
function buildRivers(t){
  while(riverGroup.children.length) riverGroup.remove(riverGroup.children[0]);
  const H=t*RES*RES;
  const points=[];
  const threshold=0.15;
  for(let iz=0;iz<RES;iz+=2){
    let chain=[];
    for(let ix=0;ix<RES;ix++){
      const e=errorData[H+iz*RES+ix];
      if(e>threshold) chain.push([ix,iz,e]);
      else if(chain.length>2){
        if(chain.length>3) points.push(chain);
        chain=[];
      }
    }
    if(chain.length>3) points.push(chain);
  }
  for(let ix=0;ix<RES;ix+=2){
    let chain=[];
    for(let iz=0;iz<RES;iz++){
      const e=errorData[H+iz*RES+ix];
      if(e>threshold) chain.push([ix,iz,e]);
      else if(chain.length>2){
        if(chain.length>3) points.push(chain);
        chain=[];
      }
    }
    if(chain.length>3) points.push(chain);
  }
  const sx=16/(RES-1), sz=16/(RES-1), ox=-8, oz=-8;
  for(const chain of points){
    const curvePts=chain.map(([ix,iz])=>{
      const hi=H+iz*RES+ix;
      return new THREE.Vector3(ox+ix*sx,heightData[hi]+0.05,oz+iz*sz);
    });
    if(curvePts.length<2) continue;
    const curve=new THREE.CatmullRomCurve3(curvePts);
    const tubeGeo=new THREE.TubeGeometry(curve,curvePts.length*2,0.06,6,false);
    const tubeMat=new THREE.MeshStandardMaterial({
      color:0xe53935, emissive:0x881111, emissiveIntensity:0.6, roughness:0.3, metalness:0.1
    });
    const tube=new THREE.Mesh(tubeGeo,tubeMat);
    tube.castShadow=true;
    riverGroup.add(tube);
  }
}
buildRivers(0);
// ── Particle system (API flow trails) ──
const MAX_PARTICLES=8000;
const particlePositions=new Float32Array(MAX_PARTICLES*3);
const particleColors=new Float32Array(MAX_PARTICLES*3);
const particleData=[]; // {phase,speed,path:[{x,z}]}
const particleGeo=new THREE.BufferGeometry();
particleGeo.setAttribute('position',new THREE.BufferAttribute(particlePositions,3));
particleGeo.setAttribute('color',new THREE.BufferAttribute(particleColors,3));
const particleMat=new THREE.PointsMaterial({
  size:0.08, vertexColors:true, blending:THREE.AdditiveBlending,
  depthWrite:false, transparent:true, opacity:0.85
});
const particles=new THREE.Points(particleGeo,particleMat);
scene.add(particles);
function initParticles(t){
  particleData.length=0;
  const H=t*RES*RES;
  const sx=16/(RES-1), sz=16/(RES-1), ox=-8, oz=-8;
  for(let i=0;i<MAX_PARTICLES;i++){
    const ix=Math.floor(Math.random()*(RES-1))+1;
    const iz=Math.floor(Math.random()*(RES-1))+1;
    const h=heightData[H+iz*RES+ix];
    const path=[];
    let cx=ix, cz=iz;
    for(let s=0;s<40;s++){
      path.push({x:ox+cx*sx, z:oz+cz*sz});
      const gradX=(heightData[H+cz*RES+Math.min(cx+1,RES-1)]-heightData[H+cz*RES+Math.max(cx-1,0)])*0.5;
      const gradZ=(heightData[H+Math.min(cz+1,RES-1)*RES+cx]-heightData[H+Math.max(cz-1,0)*RES+cx])*0.5;
      cx+=Math.round(-gradX*3+(Math.random()-0.5)*2);
      cz+=Math.round(-gradZ*3+(Math.random()-0.5)*2);
      cx=Math.max(1,Math.min(RES-2,cx));
      cz=Math.max(1,Math.min(RES-2,cz));
    }
    particleData.push({phase:Math.random(),speed:0.002+Math.random()*0.006,path});
  }
}
initParticles(0);
function updateParticles(t){
  const H=t*RES*RES;
  const sx=16/(RES-1), sz=16/(RES-1), ox=-8, oz=-8;
  for(let i=0;i<MAX_PARTICLES;i++){
    const pd=particleData[i];
    pd.phase+=pd.speed;
    if(pd.phase>=1) pd.phase-=1;
    const idx=Math.floor(pd.phase*(pd.path.length-1));
    const frac=pd.phase*(pd.path.length-1)-idx;
    const p0=pd.path[idx], p1=pd.path[Math.min(idx+1,pd.path.length-1)];
    const px=p0.x+(p1.x-p0.x)*frac;
    const pz=p0.z+(p1.z-p0.z)*frac;
    const gix=Math.round((px-ox)/sx), giz=Math.round((pz-oz)/sz);
    const ci=Math.max(0,Math.min(RES-1,gix)), cj=Math.max(0,Math.min(RES-1,giz));
    const py=heightData[H+cj*RES+ci]+0.15;
    const pi=i*3;
    particlePositions[pi]=px; particlePositions[pi+1]=py; particlePositions[pi+2]=pz;
    const t2=pd.phase;
    particleColors[pi]=1-t2*0.3;
    particleColors[pi+1]=0.7+t2*0.3;
    particleColors[pi+2]=0.2+t2*0.5;
  }
  particleGeo.attributes.position.needsUpdate=true;
  particleGeo.attributes.color.needsUpdate=true;
}
// ── Camera bookmarks ──
const bookmarks=[];
window.saveBookmark=function(){
  const b={
    pos:camera.position.clone(),
    target:controls.target.clone(),
    name:`View ${bookmarks.length+1}`
  };
  bookmarks.push(b);
  renderBookmarkList();
};
function renderBookmarkList(){
  const list=document.getElementById('bookmark-list');
  list.innerHTML=bookmarks.map((b,i)=>`<button class="bkmk-btn" onclick="restoreBookmark(${i})">${b.name}</button>`).join('');
}
window.restoreBookmark=function(i){
  const b=bookmarks[i];
  camera.position.copy(b.pos);
  controls.target.copy(b.target);
  controls.update();
};
// ── Time slider ──
const slider=document.getElementById('time-slider');
const timeLabel=document.getElementById('time-label');
slider.addEventListener('input',()=>{
  currentTime=parseInt(slider.value);
  timeLabel.textContent=`T=${currentTime}`;
  buildTerrain(currentTime);
  buildRivers(currentTime);
  initParticles(currentTime);
});
// ── External data loading (CSV grid format) ──
function parseCSVGrid(text){
  const lines=text.trim().split('\n').filter(l=>l.trim()&&!l.startsWith('#'));
  const data=lines.map(l=>l.split(',').map(parseFloat));
  if(data.length===0||data[0].length===0) throw new Error('Empty CSV');
  const rows=data.length, cols=data[0].length;
  for(let t=0;t<TIME_STEPS;t++){
    const H=t*RES*RES;
    for(let iz=0;iz<RES;iz++){
      for(let ix=0;ix<RES;ix++){
        const di=Math.floor(iz/rows*rows), dj=Math.floor(ix/cols*cols);
        const idx=H+iz*RES+ix;
        heightData[idx]=data[di][dj]*(0.5+0.5*Math.sin(t*0.1));
        densityData[idx]=0.5+0.3*Math.sin(ix*0.1+t*0.05)*Math.cos(iz*0.1);
        errorData[idx]=Math.random()>0.92?Math.random()*0.5:0;
      }
    }
  }
  buildTerrain(currentTime);
  buildRivers(currentTime);
  initParticles(currentTime);
  document.getElementById('status').style.opacity='0';
}
const fileInput=document.getElementById('file-input');
const fileDrop=document.getElementById('file-drop');
fileInput.addEventListener('change',(e)=>{
  const file=e.target.files[0];
  if(!file) return;
  const reader=new FileReader();
  reader.onload=()=>{
    try{parseCSVGrid(reader.result);}
    catch(err){alert('CSV parse error: '+err.message);}
  };
  reader.readAsText(file);
});
['dragenter','dragover'].forEach(ev=>{
  fileDrop.addEventListener(ev,(e)=>{e.preventDefault();fileDrop.classList.add('drag-over');});
});
['dragleave','drop'].forEach(ev=>{
  fileDrop.addEventListener(ev,(e)=>{e.preventDefault();fileDrop.classList.remove('drag-over');});
});
fileDrop.addEventListener('drop',(e)=>{
  const file=e.dataTransfer.files[0];
  if(!file) return;
  const reader=new FileReader();
  reader.onload=()=>{
    try{parseCSVGrid(reader.result);}
    catch(err){alert('CSV parse error: '+err.message);}
  };
  reader.readAsText(file);
});
// ── Auto-rotate toggle ──
window.toggleAutoRotate=function(){
  controls.autoRotate=!controls.autoRotate;
  document.getElementById('auto-rotate-btn').classList.toggle('active',controls.autoRotate);
};
// ── Resize ──
window.addEventListener('resize',()=>{
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});
// ── Keyboard shortcuts ──
window.addEventListener('keydown',(e)=>{
  switch(e.key.toLowerCase()){
    case'r':controls.autoRotate=!controls.autoRotate;
      document.getElementById('auto-rotate-btn').classList.toggle('active',controls.autoRotate);break;
    case'f':camera.position.set(20,14,22);controls.target.set(0,2,0);controls.update();break;
    case't':camera.position.set(0,25,1);controls.target.set(0,2,0);controls.update();break;
    case'1':case'2':case'3':case'4':case'5':
      const idx=parseInt(e.key)-1;
      if(idx<bookmarks.length) restoreBookmark(idx);
      break;
  }
});
// ── Render loop ──
const clock=new THREE.Clock();
function animate(){
  requestAnimationFrame(animate);
  controls.update();
  updateParticles(currentTime);
  const t=performance.now()*0.001;
  sun.position.x=25*Math.cos(t*0.1);
  sun.position.z=15*Math.sin(t*0.1);
  renderer.render(scene,camera);
}
// Startup
setTimeout(()=>{document.getElementById('status').style.opacity='0';},800);
animate();
// ── Preload default bookmarks ──
setTimeout(()=>{
  bookmarks.push({
    pos:new THREE.Vector3(20,14,22),target:new THREE.Vector3(0,2,0),name:'Overview'
  });
  bookmarks.push({
    pos:new THREE.Vector3(0,25,1),target:new THREE.Vector3(0,2,0),name:'Top Down'
  });
  bookmarks.push({
    pos:new THREE.Vector3(-18,8,-14),target:new THREE.Vector3(0,1.5,0),name:'Low Angle'
  });
  renderBookmarkList();
},200);
console.log('3D Data Terrain Explorer ready');
console.log('Controls: drag=orbit | scroll=zoom | right-drag=pan | R=auto-rotate | F=reset | T=top-down');
console.log('Drop CSV grid to load external elevation data');
console.log('Format: comma-separated numeric grid, one row per line');
</script>
</body>
</html>