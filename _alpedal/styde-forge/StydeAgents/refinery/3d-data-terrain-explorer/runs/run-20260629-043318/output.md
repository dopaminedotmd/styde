<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;overflow:hidden;font-family:system-ui,sans-serif}
#c{position:fixed;top:0;left:0;width:100vw;height:100vh}
#p{position:fixed;top:0;left:0;width:260px;height:100vh;background:rgba(10,10,20,0.92);color:#c8d6e5;padding:16px;display:flex;flex-direction:column;gap:12px;z-index:10;border-right:1px solid rgba(255,255,255,0.08);font-size:13px;overflow-y:auto}
#p h3{font-size:15px;color:#fff;margin:0}
#p label{display:block;color:#8395a7;font-size:11px;margin-bottom:2px}
#p input[type=range]{width:100%}
#p button{background:#1e272e;border:1px solid rgba(255,255,255,0.12);color:#c8d6e5;padding:6px 10px;cursor:pointer;border-radius:3px;font-size:12px;width:100%;text-align:left}
#p button:hover{background:#2d3a45}
#p input[type=file]{font-size:11px;color:#8395a7}
.bk-btn{display:flex;gap:4px;margin-bottom:4px}
.bk-btn button{flex:1;font-size:11px;padding:4px 6px;text-align:center}
.bk-btn button.del{flex:0 0 24px;background:#3d1a1a;color:#e66767}
.row{display:flex;align-items:center;gap:8px}
#info{font-size:10px;color:#576574;line-height:1.4;margin-top:auto}
</style>
</head>
<body>
<div id="c"></div>
<div id="p">
<h3>3D Data Terrain Explorer</h3>
<div><label>Time step <span id="tl">0</span>/9</label><input type="range" id="ts" min="0" max="9" value="0"></div>
<div class="row"><input type="checkbox" id="ar" checked><label style="margin:0">Auto-rotate</label></div>
<div><label>Bookmarks</label><div id="bl"></div><button id="sb">Save current view</button></div>
<div><label>Load CSV data</label><input type="file" id="cf" accept=".csv"></div>
<div id="info">Elevation: revenue metric | Green: user density | Red rivers: error paths | Particles: API call flow</div>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID=50, TIME_STEPS=10, CELL=2.0, HEIGHT=0.15, PARTICLES=500, RIVER_THRESH=0.15, MAX_RIVER_STEPS=200;
const HALF=(GRID-1)/2;
function clamp(v,lo,hi){return v<lo?lo:v>hi?hi:v}
// --- Deterministic data generation ---
function genData(){
  const rev=[], ud=[], er=[], ac=[];
  for(let t=0;t<TIME_STEPS;t++){
    const R=[], U=[], E=[], A=[];
    for(let z=0;z<GRID;z++){
      const rR=[], rU=[], rE=[], rA=[];
      for(let x=0;x<GRID;x++){
        const sx=x*0.3, sz=z*0.3, st=t*0.5;
        rR.push(clamp(50+30*Math.sin(sx+st)*Math.cos(sz+t*0.3)+15*Math.sin(x*0.1+z*0.1+t*0.2),0,100));
        rU.push(clamp(0.3+0.4*Math.cos(x*0.4+t*0.4)*Math.sin(z*0.4+t*0.2)+0.1*Math.sin(x*0.7+z*0.7),0,1));
        rE.push(clamp(0.03+0.12*Math.abs(Math.sin(x*0.5+z*0.5+t*0.6))+0.05*Math.abs(Math.cos(x*0.8-z*0.3+t*0.4)),0,1));
        rA.push(clamp(30+25*Math.sin(x*0.6+t*0.7)*Math.cos(z*0.5+t*0.4)+10*Math.cos(x*0.2+z*0.8+t*0.3),0,100));
      }
      R.push(rR); U.push(rU); E.push(rE); A.push(rA);
    }
    rev.push(R); ud.push(U); er.push(E); ac.push(A);
  }
  return {revenue:rev, userDensity:ud, errorRate:er, apiCalls:ac};
}
// --- Robust CSV parser ---
function parseCSV(text){
  const lines=[]; let buf='', inQ=false;
  for(let i=0;i<text.length;i++){
    const ch=text[i];
    if(ch==='"'){inQ=!inQ;buf+=ch}
    else if((ch==='\n'||(ch==='\r'&&text[i+1]==='\n'))&&!inQ){
      if(ch==='\r')i++;
      lines.push(buf); buf='';
    }else{buf+=ch}
  }
  if(buf)lines.push(buf);
  return lines.filter(l=>l.trim()).map(line=>{
    const fields=[]; let f=''; inQ=false;
    for(let i=0;i<line.length;i++){
      const ch=line[i];
      if(ch==='"'){inQ=!inQ}
      else if(ch===','&&!inQ){fields.push(f.trim()); f=''}
      else{f+=ch}
    }
    fields.push(f.trim());
    return fields;
  });
}
// --- Build terrain BufferGeometry for time step t ---
function buildTerrain(data, t){
  const R=data.revenue[t], U=data.userDensity[t], E=data.errorRate[t];
  const vCount=GRID*GRID;
  const pos=new Float32Array(vCount*3);
  const col=new Float32Array(vCount*3);
  for(let z=0;z<GRID;z++){
    for(let x=0;x<GRID;x++){
      const i=(z*GRID+x)*3;
      pos[i]=(x-HALF)*CELL;
      pos[i+2]=(z-HALF)*CELL;
      pos[i+1]=R[z][x]*HEIGHT;
      const g=0.15+U[z][x]*0.75;
      const r=E[z][x];
      col[i]=r*0.9+g*0.1;
      col[i+1]=g*(1-r)*0.9;
      col[i+2]=0.05*(1-r);
    }
  }
  const indices=[];
  for(let z=0;z<GRID-1;z++){
    for(let x=0;x<GRID-1;x++){
      const a=z*GRID+x, b=a+1, c=a+GRID, d=c+1;
      indices.push(a,b,d, a,d,c);
    }
  }
  const geo=new THREE.BufferGeometry();
  geo.setAttribute('position',new THREE.BufferAttribute(pos,3));
  geo.setAttribute('color',new THREE.BufferAttribute(col,3));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}
// --- River tracer: find error hotspots, trace downhill ---
function traceRiver(data, t, sx, sz){
  const R=data.revenue[t], E=data.errorRate[t];
  const path=[[(sx-HALF)*CELL, R[sz][sx]*HEIGHT, (sz-HALF)*CELL]];
  let cx=sx, cz=sz;
  const dirs=[[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]];
  for(let step=1;step<MAX_RIVER_STEPS;step++){
    let bestD=-1, bestH=Infinity, bestX=cx, bestZ=cz;
    for(const [dx,dz] of dirs){
      const nx=cx+dx, nz=cz+dz;
      if(nx<0||nx>=GRID||nz<0||nz>=GRID)continue;
      if(R[nz][nx]<bestH){bestH=R[nz][nx]; bestX=nx; bestZ=nz; bestD=Math.abs(dx)+Math.abs(dz);}
    }
    if(bestD<0||bestH>=R[cz][cx])break;
    cx=bestX; cz=bestZ;
    path.push([(cx-HALF)*CELL, R[cz][cx]*HEIGHT, (cz-HALF)*CELL]);
    if(E[cz][cx]<0.05)break;
  }
  return path;
}
function buildRiverGroup(data, t){
  const E=data.errorRate[t];
  const group=new THREE.Group();
  const seen=new Set();
  for(let z=1;z<GRID-1;z++){
    for(let x=1;x<GRID-1;x++){
      if(E[z][x]<RIVER_THRESH)continue;
      let isMax=true;
      for(let dz=-1;dz<=1&&isMax;dz++)
        for(let dx=-1;dx<=1;dx++)
          if((dx||dz)&&z+dz>=0&&z+dz<GRID&&x+dx>=0&&x+dx<GRID&&E[z+dz][x+dx]>E[z][x]){isMax=false;break}
      if(!isMax)continue;
      const key=`${x},${z}`;
      if(seen.has(key))continue;
      seen.add(key);
      const path=traceRiver(data,t,x,z);
      if(path.length<5)continue;
      const pts=path.map(p=>new THREE.Vector3(p[0],p[1],p[2]));
      const curve=new THREE.CatmullRomCurve3(pts);
      const tubeGeo=new THREE.TubeGeometry(curve, path.length*2, 0.35, 6, false);
      const mat=new THREE.MeshStandardMaterial({color:0xe74c3c, roughness:0.35, metalness:0.1, emissive:0x330000, emissiveIntensity:0.4});
      const mesh=new THREE.Mesh(tubeGeo, mat);
      mesh.castShadow=true;
      group.add(mesh);
    }
  }
  return group;
}
// --- Particle system: single BufferGeometry, reused Float32Array ---
class ParticleFlow {
  constructor(data){
    this.data=data;
    this.count=PARTICLES;
    this.particles=new Float32Array(PARTICLES*3);
    this.colorsArr=new Float32Array(PARTICLES*3);
    this.vels=new Float32Array(PARTICLES*3);
    this.lives=new Float32Array(PARTICLES);
    this.geo=new THREE.BufferGeometry();
    this.geo.setAttribute('position',new THREE.BufferAttribute(this.particles,3));
    this.geo.setAttribute('color',new THREE.BufferAttribute(this.colorsArr,3));
    const canvas=document.createElement('canvas'); canvas.width=32; canvas.height=32;
    const ctx=canvas.getContext('2d');
    const grad=ctx.createRadialGradient(16,16,0,16,16,14);
    grad.addColorStop(0,'rgba(255,255,255,1)'); grad.addColorStop(0.4,'rgba(255,200,100,0.8)'); grad.addColorStop(1,'rgba(255,100,20,0)');
    ctx.fillStyle=grad; ctx.fillRect(0,0,32,32);
    const tex=new THREE.CanvasTexture(canvas);
    this.mat=new THREE.PointsMaterial({size:0.6, map:tex, blending:THREE.AdditiveBlending, depthWrite:false, vertexColors:true, transparent:true, opacity:0.75});
    this.points=new THREE.Points(this.geo, this.mat);
    this.respawnAll();
  }
  respawnAll(){
    for(let i=0;i<this.count;i++){
      this.lives[i]=0.5+Math.random()*3;
      this._spawn(i);
    }
  }
  _spawn(i){
    const x=(Math.random()*0.8+0.1)*(GRID-1);
    const z=(Math.random()*0.8+0.1)*(GRID-1);
    const ix=Math.floor(x), iz=Math.floor(z);
    const h=this.data.revenue[0][clamp(iz,0,GRID-1)][clamp(ix,0,GRID-1)]*HEIGHT;
    this.particles[i*3]=(x-HALF)*CELL;
    this.particles[i*3+1]=h+0.5+Math.random()*2;
    this.particles[i*3+2]=(z-HALF)*CELL;
    this.vels[i*3]=(Math.random()-0.5)*1.5;
    this.vels[i*3+1]=-0.1-Math.random()*0.3;
    this.vels[i*3+2]=(Math.random()-0.5)*1.5;
  }
  update(dt, t){
    const R=this.data.revenue[t], E=this.data.errorRate[t];
    for(let i=0;i<this.count;i++){
      this.lives[i]-=dt;
      if(this.lives[i]<=0){this.lives[i]=0.5+Math.random()*3; this._spawn(i); continue}
      const i3=i*3;
      this.particles[i3]+=this.vels[i3]*dt;
      this.particles[i3+1]+=this.vels[i3+1]*dt;
      this.particles[i3+2]+=this.vels[i3+2]*dt;
      const gx=Math.round(this.particles[i3]/CELL+HALF);
      const gz=Math.round(this.particles[i3+2]/CELL+HALF);
      if(gx>=0&&gx<GRID&&gz>=0&&gz<GRID){
        const surf=R[gz][gx]*HEIGHT;
        if(this.particles[i3+1]<surf+0.3){this.particles[i3+1]=surf+0.3; this.vels[i3+1]=Math.abs(this.vels[i3+1])*0.2}
        const err=E[gz][gx];
        if(err>RIVER_THRESH){
          this.colorsArr[i3]=1; this.colorsArr[i3+1]=0.15; this.colorsArr[i3+2]=0.05;
        }else{
          this.colorsArr[i3]=0.9; this.colorsArr[i3+1]=0.75; this.colorsArr[i3+2]=0.2;
        }
      }
      const bx=(GRID-1)*CELL/2;
      if(Math.abs(this.particles[i3])>bx||Math.abs(this.particles[i3+2])>bx||this.particles[i3+1]<0){this._spawn(i)}
    }
    this.geo.attributes.position.needsUpdate=true;
    this.geo.attributes.color.needsUpdate=true;
  }
}
// --- Init ---
const container=document.getElementById('c');
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.1;
container.appendChild(renderer.domElement);
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x0a0a14);
scene.fog=new THREE.Fog(0x0a0a14, 80, 220);
const camera=new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 1, 500);
camera.position.set(60, 45, 65);
camera.lookAt(0, 5, 0);
const controls=new OrbitControls(camera, renderer.domElement);
controls.enableDamping=true; controls.dampingFactor=0.08;
controls.autoRotate=true; controls.autoRotateSpeed=0.4;
controls.target.set(0, 5, 0);
controls.minDistance=15; controls.maxDistance=180;
controls.maxPolarAngle=Math.PI*0.45;
controls.update();
const ambient=new THREE.AmbientLight(0x334466, 1.8);
scene.add(ambient);
const sun=new THREE.DirectionalLight(0xffeedd, 3.5);
sun.position.set(50, 80, 30);
sun.castShadow=true;
sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.near=0.5; sun.shadow.camera.far=300;
sun.shadow.camera.left=-80; sun.shadow.camera.right=80;
sun.shadow.camera.top=80; sun.shadow.camera.bottom=-80;
sun.shadow.bias=-0.0001;
scene.add(sun);
const fill=new THREE.DirectionalLight(0x4466aa, 1.2);
fill.position.set(-20, 10, -40);
scene.add(fill);
const data=genData();
const terrainGeos=[];
for(let t=0;t<TIME_STEPS;t++)terrainGeos.push(buildTerrain(data,t));
const terrainMat=new THREE.MeshStandardMaterial({vertexColors:true, roughness:0.75, metalness:0.05, flatShading:false});
const terrainMesh=new THREE.Mesh(terrainGeos[0], terrainMat);
terrainMesh.receiveShadow=true; terrainMesh.castShadow=true;
scene.add(terrainMesh);
const riverGroups=[];
for(let t=0;t<TIME_STEPS;t++){
  const g=buildRiverGroup(data,t);
  g.visible=t===0;
  riverGroups.push(g);
  scene.add(g);
}
const gridHelper=new THREE.GridHelper((GRID-1)*CELL, GRID-1, 0x334466, 0x1a1a2e);
gridHelper.position.y=-0.5;
scene.add(gridHelper);
const particles=new ParticleFlow(data);
scene.add(particles.points);
let currentTime=0;
const timeSlider=document.getElementById('ts');
const timeLabel=document.getElementById('tl');
timeSlider.addEventListener('input',()=>{
  currentTime=parseInt(timeSlider.value);
  timeLabel.textContent=currentTime;
  terrainMesh.geometry=terrainGeos[currentTime];
  riverGroups.forEach((g,i)=>g.visible=i===currentTime);
});
document.getElementById('ar').addEventListener('change',e=>{controls.autoRotate=e.target.checked});
const bookmarks=[{pos:camera.position.clone(),tgt:controls.target.clone(),label:'Default'}];
const bl=document.getElementById('bl');
function renderBookmarks(){
  bl.innerHTML=bookmarks.map((b,i)=>`<div class="bk-btn"><button>${b.label||'View '+i}</button><button class="del" data-i="${i}">x</button></div>`).join('');
  bl.querySelectorAll('.bk-btn button:first-child').forEach((btn,i)=>{
    btn.addEventListener('click',()=>{
      const b=bookmarks[i];
      camera.position.copy(b.pos);
      controls.target.copy(b.tgt);
      controls.update();
    });
  });
  bl.querySelectorAll('.bk-btn button.del').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const i=parseInt(btn.dataset.i);
      if(i>0)bookmarks.splice(i,1);
      renderBookmarks();
    });
  });
}
renderBookmarks();
document.getElementById('sb').addEventListener('click',()=>{
  bookmarks.push({pos:camera.position.clone(),tgt:controls.target.clone(),label:'View '+bookmarks.length});
  renderBookmarks();
});
document.getElementById('cf').addEventListener('change',e=>{
  const file=e.target.files[0];
  if(!file)return;
  const reader=new FileReader();
  reader.onload=ev=>{
    const parsed=parseCSV(ev.target.result);
    console.log('CSV parsed:',parsed.length,'rows,',parsed[0]?.length||0,'cols');
  };
  reader.readAsText(file);
});
window.addEventListener('resize',()=>{
  camera.aspect=window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});
const clock=new THREE.Clock();
function animate(){
  requestAnimationFrame(animate);
  const dt=Math.min(clock.getDelta(),0.1);
  controls.update();
  particles.update(dt, currentTime);
  renderer.render(scene, camera);
}
animate();
</script>
</body>
</html>