<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a1a;overflow:hidden;font-family:system-ui,-apple-system,sans-serif}
#container{width:100vw;height:100vh;position:fixed;top:0;left:0}
#ui{position:fixed;bottom:0;left:0;right:0;padding:14px 20px;background:linear-gradient(transparent,rgba(0,0,0,0.85));display:flex;gap:12px;align-items:center;z-index:10}
#time-slider{flex:1;accent-color:#4af;height:6px}
#time-label{color:#aac;font-size:13px;min-width:85px;font-variant-numeric:tabular-nums}
#auto-rotate{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);color:#bbc;padding:5px 12px;border-radius:4px;cursor:pointer;font-size:12px}
#auto-rotate:hover{background:rgba(255,255,255,0.16)}
#bookmarks{position:fixed;top:12px;right:12px;display:flex;gap:6px;z-index:10;flex-wrap:wrap;max-width:300px;justify-content:flex-end}
.bmk-btn{background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.15);color:#aab;padding:4px 10px;border-radius:3px;cursor:pointer;font-size:11px;transition:background 0.15s}
.bmk-btn:hover{background:rgba(255,255,255,0.18)}
.bmk-go{background:rgba(100,180,255,0.12);border-color:rgba(100,180,255,0.3);color:#8cf}
#legend{position:fixed;top:12px;left:12px;z-index:10;font-size:11px;line-height:1.6;pointer-events:none}
#legend span{display:block}
.l-elev{color:#aac}.l-color{color:#4f8}.l-river{color:#f55}.l-part{color:#fa0}
</style>
</head>
<body>
<div id="container"></div>
<div id="legend">
<span class="l-elev">Terrain height: Revenue</span>
<span class="l-color">Surface color: User density</span>
<span class="l-river">Red paths: Error rate rivers</span>
<span class="l-part">Gold dots: API call flows</span>
</div>
<div id="bookmarks">
<button class="bmk-btn" data-save="1" title="Ctrl+1 to save">S1</button>
<button class="bmk-btn" data-save="2" title="Ctrl+2 to save">S2</button>
<button class="bmk-btn" data-save="3" title="Ctrl+3 to save">S3</button>
<button class="bmk-btn bmk-go" data-go="1" title="Press 1 to recall">1</button>
<button class="bmk-btn bmk-go" data-go="2" title="Press 2 to recall">2</button>
<button class="bmk-btn bmk-go" data-go="3" title="Press 3 to recall">3</button>
</div>
<div id="ui">
<span id="time-label">Month 1</span>
<input type="range" id="time-slider" min="0" max="11" value="0" step="1">
<button id="auto-rotate">Auto: ON</button>
</div>
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
const GRID=64, SIZE=20, STEPS=12, HALF=SIZE/2, N_PART=280;
const SEG=GRID-1;
let currentTime=0;
function hash(x,z){let h=x*374761393+z*668265263;h=(h^(h>>13))*1274126177;return(h^(h>>16))/2147483648}
function sNoise(x,z){const ix=Math.floor(x),iz=Math.floor(z),fx=x-ix,fz=z-iz;const sx=fx*fx*(3-2*fx),sz=fz*fz*(3-2*fz);const n00=hash(ix,iz),n10=hash(ix+1,iz),n01=hash(ix,iz+1),n11=hash(ix+1,iz+1);return n00*(1-sx)*(1-sz)+n10*sx*(1-sz)+n01*(1-sx)*sz+n11*sx*sz}
function fbm(x,z,o=4){let v=0,a=1,f=1;for(let i=0;i<o;i++){v+=a*sNoise(x*f,z*f);a*=0.5;f*=2}return v}
function hTerrain(x,z,t){
  const nx=x/SIZE*4,nz=z/SIZE*4;
  let h=fbm(nx+0.3*t,nz+0.3*t,5)*3;
  for(let i=0;i<3;i++){
    const cx=Math.sin(i*2.1+t*0.5)*SIZE*0.3,cz=Math.cos(i*1.7+t*0.4)*SIZE*0.3;
    const amp=2+Math.sin(t*0.6+i)*1.5,d=Math.hypot(x-cx,z-cz)/SIZE;
    h+=amp*Math.exp(-d*d*8);
  }
  return h;
}
function uDensity(x,z,t){return fbm(x/SIZE*5+1.7,z/SIZE*5+1.7+t*0.2,4)*0.5+0.5}
function eRate(x,z,t){
  const s=Math.abs(hTerrain(x+0.5,z,t)-hTerrain(x-0.5,z,t))+Math.abs(hTerrain(x,z+0.5,t)-hTerrain(x,z-0.5,t));
  return Math.min(1,s*0.8+Math.abs(fbm(x/SIZE*3+t*0.3,z/SIZE*3,3))*0.4);
}
const terrainGeos=[], riverGroups=[];
function buildGeo(t){
  const g=new THREE.BufferGeometry();
  const v=new Float32Array(GRID*GRID*3),c=new Float32Array(GRID*GRID*3),idx=[];
  for(let iz=0;iz<GRID;iz++)for(let ix=0;ix<GRID;ix++){
    const x=(ix/SEG-0.5)*SIZE,z=(iz/SEG-0.5)*SIZE,y=hTerrain(x,z,t);
    const i=(iz*GRID+ix)*3;
    v[i]=x;v[i+1]=y;v[i+2]=z;
    const d=uDensity(x,z,t);
    c[i]=d*0.15;c[i+1]=0.28+d*0.72;c[i+2]=d*0.08;
  }
  for(let iz=0;iz<SEG;iz++)for(let ix=0;ix<SEG;ix++){
    const a=iz*GRID+ix,b=a+1,d=a+GRID,e=d+1;
    idx.push(a,b,e,a,e,d);
  }
  g.setAttribute('position',new THREE.BufferAttribute(v,3));
  g.setAttribute('color',new THREE.BufferAttribute(c,3));
  g.setIndex(idx);g.computeVertexNormals();
  return g;
}
function traceRiver(t,sx,sz,maxS=70){
  const pts=[];let x=sx,z=sz;
  const step=SIZE/GRID*1.8;
  for(let i=0;i<maxS;i++){
    let best=-1,bx=x,bz=z;
    for(let dx=-1;dx<=1;dx++)for(let dz=-1;dz<=1;dz++){
      if(dx===0&&dz===0)continue;
      const nx=x+dx*step,nz=z+dz*step;
      if(Math.abs(nx)>HALF*0.95||Math.abs(nz)>HALF*0.95)continue;
      const e=eRate(nx,nz,t);
      if(e>best){best=e;bx=nx;bz=nz}
    }
    if(bx===x&&bz===z)break;
    x=bx;z=bz;
    if(best<0.25&&pts.length>8)break;
    pts.push(new THREE.Vector3(x,hTerrain(x,z,t)+0.04,z));
  }
  return pts.length>3?pts:null;
}
function buildRivers(t){
  const grp=new THREE.Group();
  const mat=new THREE.LineBasicMaterial({color:0xff3333,transparent:true,opacity:0.75,depthTest:true});
  for(let i=0;i<7;i++){
    const sx=(Math.random()-0.5)*SIZE*0.75,sz=(Math.random()-0.5)*SIZE*0.75;
    if(eRate(sx,sz,t)<0.45)continue;
    const pts=traceRiver(t,sx,sz,55);
    if(!pts)continue;
    grp.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),mat));
  }
  return grp;
}
for(let t=0;t<STEPS;t++){terrainGeos.push(buildGeo(t));riverGroups.push(buildRivers(t))}
const container=document.getElementById('container');
const scene=new THREE.Scene();
scene.background=new THREE.Color(0x080818);
scene.fog=new THREE.FogExp2(0x080818,0.00035);
const cam=new THREE.PerspectiveCamera(52,container.clientWidth/container.clientHeight,0.5,SIZE*6);
cam.position.set(SIZE*1.1,SIZE*0.75,SIZE*1.1);cam.lookAt(0,0.5,0);
const renderer=new THREE.WebGLRenderer({antialias:true});
renderer.setSize(container.clientWidth,container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0x334466,1.6));
const sun=new THREE.DirectionalLight(0xffeedd,3.5);
sun.position.set(SIZE,SIZE*2.2,SIZE);sun.castShadow=true;
sun.shadow.mapSize.set(1024,1024);
sun.shadow.camera.near=0.5;sun.shadow.camera.far=SIZE*5;
sun.shadow.camera.left=-SIZE;sun.shadow.camera.right=SIZE;
sun.shadow.camera.top=SIZE;sun.shadow.camera.bottom=-SIZE;
scene.add(sun);
scene.add(new THREE.DirectionalLight(0x4466aa,1.2).position.set(-SIZE,0.5*SIZE,-SIZE));
const tMat=new THREE.MeshStandardMaterial({vertexColors:true,roughness:0.65,metalness:0.08,flatShading:false});
const tMesh=new THREE.Mesh(terrainGeos[0],tMat);
tMesh.castShadow=true;tMesh.receiveShadow=true;scene.add(tMesh);
let curRivers=riverGroups[0];scene.add(curRivers);
const gridH=new THREE.GridHelper(SIZE*1.5,30,0x334466,0x141428);
gridH.position.y=-0.02;scene.add(gridH);
const pPaths=[];for(let i=0;i<N_PART;i++){const p=[];let x=(Math.random()-0.5)*SIZE*0.85,z=(Math.random()-0.5)*SIZE*0.85;const seg=35+Math.floor(Math.random()*55);for(let j=0;j<seg;j++){const a=Math.random()*Math.PI*2,d=Math.random()*SIZE*0.12;x+=Math.cos(a)*d;z+=Math.sin(a)*d;x=Math.max(-HALF*0.94,Math.min(HALF*0.94,x));z=Math.max(-HALF*0.94,Math.min(HALF*0.94,z));p.push({x,z})}pPaths.push(p)}
const pPos=new Float32Array(N_PART*3),pProg=new Float32Array(N_PART),pSpd=new Float32Array(N_PART);
for(let i=0;i<N_PART;i++){pProg[i]=Math.random();pSpd[i]=0.0008+Math.random()*0.0035}
const pGeo=new THREE.BufferGeometry();pGeo.setAttribute('position',new THREE.BufferAttribute(pPos,3));
const pMat=new THREE.PointsMaterial({color:0xffaa00,size:0.13,blending:THREE.AdditiveBlending,depthWrite:false,transparent:true,opacity:0.85});
const ptsMesh=new THREE.Points(pGeo,pMat);scene.add(ptsMesh);
function updParticles(t){
  for(let i=0;i<N_PART;i++){pProg[i]+=pSpd[i];if(pProg[i]>=1)pProg[i]-=1;const path=pPaths[i],prog=pProg[i];const idx=Math.floor(prog*(path.length-1)),frac=prog*(path.length-1)-idx;const p0=path[idx],p1=path[Math.min(idx+1,path.length-1)];const x=p0.x+(p1.x-p0.x)*frac,z=p0.z+(p1.z-p0.z)*frac;pPos[i*3]=x;pPos[i*3+1]=hTerrain(x,z,t)+0.12;pPos[i*3+2]=z}
  pGeo.attributes.position.needsUpdate=true;
}
updParticles(0);
const ctrl=new OrbitControls(cam,renderer.domElement);
ctrl.enableDamping=true;ctrl.dampingFactor=0.08;
ctrl.target.set(0,0.8,0);ctrl.minDistance=SIZE*0.25;ctrl.maxDistance=SIZE*3.2;
ctrl.maxPolarAngle=Math.PI*0.47;ctrl.autoRotate=true;ctrl.autoRotateSpeed=0.25;ctrl.update();
const bm=[null,null,null];
function saveBm(i){bm[i]={pos:cam.position.clone(),tgt:ctrl.target.clone()}}
function goBm(i){const b=bm[i];if(!b)return;const sp=cam.position.clone(),st=ctrl.target.clone(),ep=b.pos,et=b.tgt,start=performance.now();function anim(now){const t=Math.min(1,(now-start)/750);const e=t<0.5?2*t*t:-1+(4-2*t)*t;cam.position.lerpVectors(sp,ep,e);ctrl.target.lerpVectors(st,et,e);if(t<1)requestAnimationFrame(anim)}requestAnimationFrame(anim)}
const slider=document.getElementById('time-slider'),tLabel=document.getElementById('time-label');
slider.addEventListener('input',()=>{currentTime=parseInt(slider.value);tLabel.textContent='Month '+(currentTime+1);tMesh.geometry=terrainGeos[currentTime];scene.remove(curRivers);curRivers=riverGroups[currentTime];scene.add(curRivers);updParticles(currentTime)});
document.getElementById('auto-rotate').addEventListener('click',function(){ctrl.autoRotate=!ctrl.autoRotate;this.textContent=ctrl.autoRotate?'Auto: ON':'Auto: OFF'});
document.querySelectorAll('.bmk-btn[data-save]').forEach(b=>b.addEventListener('click',()=>saveBm(parseInt(b.dataset.save)-1)));
document.querySelectorAll('.bmk-btn[data-go]').forEach(b=>b.addEventListener('click',()=>goBm(parseInt(b.dataset.go)-1)));
window.addEventListener('keydown',e=>{if(e.key>='1'&&e.key<='3'){const i=parseInt(e.key)-1;if(e.ctrlKey||e.metaKey)saveBm(i);else goBm(i)}});
window.addEventListener('resize',()=>{cam.aspect=container.clientWidth/container.clientHeight;cam.updateProjectionMatrix();renderer.setSize(container.clientWidth,container.clientHeight)});
function anim(){requestAnimationFrame(anim);ctrl.update();updParticles(currentTime);renderer.render(scene,cam)}
anim();
</script>
</body>
</html>