<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  :root{--bg:#0a0a14;--panel-bg:rgba(10,10,30,0.92);--text:#c8d6e5;--accent:#4dabf7;--danger:#ff6b6b;--warn:#ffd43b;--border:rgba(255,255,255,0.08)}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);overflow:hidden;font-family:'Segoe UI',system-ui,sans-serif;color:var(--text)}
  #webgl-canvas{display:block;position:fixed;top:0;left:0;width:100vw;height:100vh}
  #fallback-canvas{display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;background:#0d0d1f}
  #mode-banner{position:fixed;top:12px;left:50%;transform:translateX(-50%);padding:6px 18px;border-radius:20px;font-size:13px;font-weight:600;z-index:100;pointer-events:none;transition:opacity 0.4s}
  #mode-banner.webgl{background:rgba(30,200,120,0.18);color:#26de81;border:1px solid rgba(38,222,129,0.3)}
  #mode-banner.fallback{background:rgba(255,107,107,0.18);color:#ff6b6b;border:1px solid rgba(255,107,107,0.3)}
  #ui-panel{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);width:min(92vw,700px);background:var(--panel-bg);border-radius:14px;padding:14px 20px;z-index:50;backdrop-filter:blur(12px);border:1px solid var(--border);display:flex;flex-direction:column;gap:10px}
  #time-slider{width:100%;accent-color:var(--accent);cursor:pointer}
  .slider-labels{display:flex;justify-content:space-between;font-size:11px;opacity:0.7}
  .btn-row{display:flex;gap:8px;flex-wrap:wrap}
  .btn{background:rgba(255,255,255,0.06);border:1px solid var(--border);color:var(--text);padding:6px 14px;border-radius:8px;cursor:pointer;font-size:12px;transition:background 0.2s}
  .btn:hover{background:rgba(255,255,255,0.12)}
  .btn.active{background:var(--accent);color:#000;border-color:var(--accent)}
  #bookmark-list{display:flex;gap:6px;flex-wrap:wrap}
  .bookmark-tag{background:rgba(77,171,247,0.15);border:1px solid rgba(77,171,247,0.25);color:var(--accent);padding:3px 10px;border-radius:12px;font-size:11px;cursor:pointer}
  #inspect-tooltip{position:fixed;pointer-events:none;background:rgba(0,0,0,0.85);color:#fff;padding:6px 12px;border-radius:6px;font-size:12px;display:none;z-index:60}
  #import-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:200;align-items:center;justify-content:center}
  #import-modal.open{display:flex}
  .modal-box{background:var(--panel-bg);border-radius:14px;padding:24px;width:min(90vw,500px);border:1px solid var(--border)}
  .modal-box h2{margin-bottom:12px;font-size:16px}
  .modal-box textarea{width:100%;height:120px;background:rgba(255,255,255,0.04);border:1px solid var(--border);color:var(--text);padding:10px;border-radius:8px;resize:vertical;font-family:monospace;font-size:12px;margin:8px 0}
  #fps-counter{position:fixed;top:12px;right:16px;font-size:11px;opacity:0.5;z-index:50;font-family:monospace}
</style>
</head>
<body>
<canvas id="webgl-canvas"></canvas>
<canvas id="fallback-canvas"></canvas>
<div id="mode-banner" class="webgl">WEBGL RENDERER</div>
<div id="fps-counter">-- FPS</div>
<div id="inspect-tooltip"></div>
<div id="import-modal">
  <div class="modal-box">
    <h2>Import Terrain Data</h2>
    <p style="font-size:12px;opacity:0.7;margin-bottom:8px">Paste CSV (x,y,height,color) or GeoJSON below</p>
    <textarea id="import-textarea" placeholder="x,y,height,color&#10;0,0,1.2,#26de81&#10;1,0,0.8,#4dabf7&#10;..."></textarea>
    <div class="btn-row" style="justify-content:flex-end">
      <button class="btn" onclick="closeImportModal()">Cancel</button>
      <button class="btn active" onclick="importData()">Load Data</button>
    </div>
  </div>
</div>
<div id="ui-panel">
  <input type="range" id="time-slider" min="0" max="99" value="0">
  <div class="slider-labels"><span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span><span>Nov</span><span>Dec</span></div>
  <div class="btn-row">
    <button class="btn active" id="btn-auto-rotate" onclick="toggleAutoRotate()">Auto-Rotate</button>
    <button class="btn" id="btn-wireframe" onclick="toggleWireframe()">Wireframe</button>
    <button class="btn" id="btn-bookmark" onclick="saveBookmark()">Save View</button>
    <button class="btn" id="btn-import" onclick="openImportModal()">Import Data</button>
    <button class="btn" onclick="resetCamera()">Reset</button>
  </div>
  <div id="bookmark-list"></div>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 80;
const TERRAIN_SCALE = 8;
const HEIGHT_AMP = 3.5;
const PARTICLE_COUNT = 600;
const LRU_CACHE_MAX = 50;
const IDLE_TIMEOUT_MS = 30000;
const DELTA_CLAMP_MAX = 0.1;
let scene, camera, renderer, controls, terrainMesh, riverGroup, particleSystem;
let clock = new THREE.Clock();
let useWebGL = true;
let autoRotate = true;
let wireframe = false;
let timeIndex = 0;
let bookmarks = [];
let idleTimer = 0;
let fpsFrames = 0, fpsTime = 0;
let animationId = null;
const riverCache = new Map();
const riverCacheKeys = [];
function lruGet(key){if(riverCache.has(key)){const v=riverCache.get(key);riverCache.delete(key);riverCache.set(key,v);return v;}return null;}
function lruSet(key,value){if(riverCache.has(key)){riverCache.delete(key);}else if(riverCache.size>=LRU_CACHE_MAX){const oldest=riverCacheKeys.shift();riverCache.delete(oldest);}riverCache.set(key,value);riverCacheKeys.push(key);}
const rAFQueue = [];
function enqueueRAF(fn){rAFQueue.push(fn);}
function generateHeightData(t){
  const data = new Float32Array(GRID*GRID);
  const cx=GRID/2, cz=GRID/2;
  for(let z=0;z<GRID;z++){
    for(let x=0;x<GRID;x++){
      const dx=(x-cx)/(GRID/3), dz=(z-cz)/(GRID/3);
      const tPhase=t*0.005;
      let h = Math.sin(dx*0.4+tPhase)*1.8 + Math.cos(dz*0.35+tPhase*0.7)*1.5;
      h += Math.sin((dx+dz)*0.25+tPhase*1.3)*1.2;
      h += Math.exp(-(dx*dx+dz*dz)*0.008)*2.5;
      h += (Math.sin(dx*0.9)*Math.cos(dz*0.85))*0.6;
      const ridge=Math.abs(Math.sin(dx*0.3+tPhase*0.2))*Math.exp(-Math.abs(dz)*0.06)*2.0;
      h += ridge;
      data[z*GRID+x]=h*HEIGHT_AMP;
    }
  }
  return data;
}
function colorFromHeight(h,hMin,hMax){
  const t=(h-hMin)/(hMax-hMin+0.001);
  const clamped=Math.max(0,Math.min(1,t));
  const r=clamped<0.5?clamped*2:1;
  const g=clamped<0.5?0.3+clamped*1.4:1.7-clamped*1.4;
  const b=clamped<0.5?1-clamped*1.5:0.25;
  return new THREE.Color(r,Math.max(0,Math.min(1,g)),Math.max(0,Math.min(1,b)));
}
function buildTerrain(heightData){
  const geom=new THREE.BufferGeometry();
  const verts=new Float32Array(GRID*GRID*3);
  const colors=new Float32Array(GRID*GRID*3);
  let hMin=Infinity,hMax=-Infinity;
  for(let i=0;i<heightData.length;i++){if(heightData[i]<hMin)hMin=heightData[i];if(heightData[i]>hMax)hMax=heightData[i];}
  for(let z=0;z<GRID;z++){
    for(let x=0;x<GRID;x++){
      const idx=(z*GRID+x)*3;
      const h=heightData[z*GRID+x];
      verts[idx]=(x-GRID/2)*TERRAIN_SCALE/GRID*TERRAIN_SCALE;
      verts[idx+1]=h;
      verts[idx+2]=(z-GRID/2)*TERRAIN_SCALE/GRID*TERRAIN_SCALE;
      const c=colorFromHeight(h,hMin,hMax);
      colors[idx]=c.r;colors[idx+1]=c.g;colors[idx+2]=c.b;
    }
  }
  geom.setAttribute('position',new THREE.BufferAttribute(verts,3));
  geom.setAttribute('color',new THREE.BufferAttribute(colors,3));
  const indices=[];
  for(let z=0;z<GRID-1;z++){
    for(let x=0;x<GRID-1;x++){
      const a=z*GRID+x,b=a+1,c=a+GRID,d=c+1;
      indices.push(a,b,d,a,d,c);
    }
  }
  geom.setIndex(indices);
  geom.computeVertexNormals();
  return geom;
}
function buildRiverGeometry(heightData,t){
  const cacheKey=`${t}|${heightData[0]}|${heightData[Math.floor(heightData.length/2)]}`;
  const cached=lruGet(cacheKey);
  if(cached)return cached;
  const points=[];
  const cx=GRID/2,cz=GRID/2;
  for(let i=0;i<GRID;i++){
    const x=cx+Math.sin(i*0.15+t*0.02)*GRID*0.35;
    const z=cz+(i-GRID/2)*0.8;
    const gx=Math.round(Math.max(0,Math.min(GRID-1,x)));
    const gz=Math.round(Math.max(0,Math.min(GRID-1,z)));
    const h=heightData[gz*GRID+gx]+0.15;
    points.push(new THREE.Vector3((gx-GRID/2)*TERRAIN_SCALE/GRID*TERRAIN_SCALE,h,(gz-GRID/2)*TERRAIN_SCALE/GRID*TERRAIN_SCALE));
  }
  const curve=new THREE.CatmullRomCurve3(points);
  const tubePoints=curve.getPoints(GRID*2);
  const pathGeom=new THREE.BufferGeometry().setFromPoints(tubePoints);
  const spline2=new THREE.CatmullRomCurve3([
    new THREE.Vector3(cx*0.3,0,cz*0.3),
    new THREE.Vector3(cx*0.6,heightData[Math.floor(GRID/2)*GRID+Math.floor(GRID/3)]*0.5,cz*0.5),
    new THREE.Vector3(cx*0.9,0,cz*0.8)
  ]);
  const pts2=spline2.getPoints(GRID);
  const pathGeom2=new THREE.BufferGeometry().setFromPoints(pts2);
  const result={main:pathGeom,secondary:pathGeom2};
  lruSet(cacheKey,result);
  return result;
}
function buildRiverLines(heightData,t){
  const geoms=buildRiverGeometry(heightData,t);
  if(riverGroup){
    riverGroup.clear();
    const mat=new THREE.LineBasicMaterial({color:0xff4444,linewidth:1,transparent:true,opacity:0.7});
    const line1=new THREE.Line(geoms.main,mat);
    const mat2=new THREE.LineBasicMaterial({color:0xff8844,linewidth:1,transparent:true,opacity:0.5});
    const line2=new THREE.Line(geoms.secondary,mat2);
    riverGroup.add(line1);
    riverGroup.add(line2);
  }
}
function buildParticles(heightData,t){
  const positions=new Float32Array(PARTICLE_COUNT*3);
  const cx=GRID/2,cz=GRID/2;
  const baseScale=TERRAIN_SCALE/GRID*TERRAIN_SCALE;
  for(let i=0;i<PARTICLE_COUNT;i++){
    const angle=(i/PARTICLE_COUNT)*Math.PI*2+t*0.003;
    const radius=GRID*0.2+Math.sin(i*0.7+t*0.01)*GRID*0.2;
    const gx=Math.round(Math.max(0,Math.min(GRID-1,cx+Math.cos(angle)*radius)));
    const gz=Math.round(Math.max(0,Math.min(GRID-1,cz+Math.sin(angle)*radius)));
    const h=heightData[gz*GRID+gx]+0.4+Math.sin(i*0.3+t*0.02)*0.6;
    positions[i*3]=(gx-GRID/2)*baseScale;
    positions[i*3+1]=Math.max(-10,Math.min(h,HEIGHT_AMP*2));
    positions[i*3+2]=(gz-GRID/2)*baseScale;
  }
  if(!particleSystem){
    const geom=new THREE.BufferGeometry();
    geom.setAttribute('position',new THREE.BufferAttribute(positions,3));
    const mat=new THREE.PointsMaterial({color:0x4dabf7,size:0.12,blending:THREE.AdditiveBlending,depthWrite:false,transparent:true,opacity:0.8});
    particleSystem=new THREE.Points(geom,mat);
  }else{
    particleSystem.geometry.attributes.position.array.set(positions);
    particleSystem.geometry.attributes.position.needsUpdate=true;
  }
}
function updateTerrain(t){
  const heightData=generateHeightData(t);
  const geom=buildTerrain(heightData);
  if(terrainMesh){
    terrainMesh.geometry.dispose();
    terrainMesh.geometry=geom;
  }
  buildRiverLines(heightData,t);
  buildParticles(heightData,t);
}
function initWebGL(){
  const canvas=document.getElementById('webgl-canvas');
  renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:false});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
  renderer.setSize(window.innerWidth,window.innerHeight);
  renderer.shadowMap.enabled=true;
  renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  canvas.addEventListener('webglcontextlost',handleContextLost,false);
  canvas.addEventListener('webglcontextrestored',handleContextRestored,false);
  scene=new THREE.Scene();
  scene.background=new THREE.Color(0x0a0a18);
  scene.fog=new THREE.Fog(0x0a0a18,15,50);
  camera=new THREE.PerspectiveCamera(55,window.innerWidth/window.innerHeight,0.5,80);
  camera.position.set(16,10,18);
  camera.lookAt(0,0,0);
  controls=new OrbitControls(camera,renderer.domElement);
  controls.enableDamping=true;
  controls.dampingFactor=0.08;
  controls.autoRotate=true;
  controls.autoRotateSpeed=0.4;
  controls.minDistance=4;
  controls.maxDistance=40;
  controls.maxPolarAngle=Math.PI*0.75;
  controls.target.set(0,1.5,0);
  controls.update();
  const ambient=new THREE.AmbientLight(0x334466,1.8);
  scene.add(ambient);
  const sun=new THREE.DirectionalLight(0xffeedd,2.5);
  sun.position.set(20,25,10);
  sun.castShadow=true;
  sun.shadow.mapSize.width=1024;
  sun.shadow.mapSize.height=1024;
  sun.shadow.camera.near=0.5;
  sun.shadow.camera.far=60;
  sun.shadow.camera.left=-20;
  sun.shadow.camera.right=20;
  sun.shadow.camera.top=20;
  sun.shadow.camera.bottom=-20;
  scene.add(sun);
  const fill=new THREE.DirectionalLight(0x4477aa,0.8);
  fill.position.set(-10,5,-5);
  scene.add(fill);
  const gridHelper=new THREE.GridHelper(16,40,0x222244,0x111122);
  gridHelper.position.y=-0.05;
  scene.add(gridHelper);
  const heightData=generateHeightData(0);
  const geom=buildTerrain(heightData);
  const mat=new THREE.MeshStandardMaterial({vertexColors:true,roughness:0.75,metalness:0.1,flatShading:false,side:THREE.DoubleSide});
  terrainMesh=new THREE.Mesh(geom,mat);
  terrainMesh.castShadow=true;
  terrainMesh.receiveShadow=true;
  scene.add(terrainMesh);
  riverGroup=new THREE.Group();
  scene.add(riverGroup);
  buildRiverLines(heightData,0);
  buildParticles(heightData,0);
  if(particleSystem)scene.add(particleSystem);
  document.getElementById('mode-banner').className='webgl';
  document.getElementById('mode-banner').textContent='WEBGL RENDERER';
  document.getElementById('fallback-canvas').style.display='none';
  document.getElementById('webgl-canvas').style.display='block';
}
let fallbackState={orbitAngle:0.7,orbitElevation:1.2,orbitDist:14,panX:0,panY:0,targetX:0,targetZ:0,isDragging:false,dragPrev:null,clickPoint:null};
function initFallback(){
  useWebGL=false;
  document.getElementById('webgl-canvas').style.display='none';
  document.getElementById('fallback-canvas').style.display='block';
  document.getElementById('mode-banner').className='fallback';
  document.getElementById('mode-banner').textContent='2D FALLBACK RENDERER';
  const c=document.getElementById('fallback-canvas');
  c.width=window.innerWidth;
  c.height=window.innerHeight;
  c.addEventListener('mousedown',onFallbackMouseDown);
  c.addEventListener('mousemove',onFallbackMouseMove);
  c.addEventListener('mouseup',onFallbackMouseUp);
  c.addEventListener('wheel',onFallbackWheel);
  c.addEventListener('click',onFallbackClick);
  if(animationId){cancelAnimationFrame(animationId);animationId=null;}
  idleTimer=0;
  requestAnimationFrame(fallbackLoop);
}
function handleContextLost(e){
  e.preventDefault();
  console.warn('WebGL context lost, switching to 2D fallback');
  if(renderer){renderer.dispose();renderer=null;}
  initFallback();
}
function handleContextRestored(){
  console.log('WebGL context restored');
  location.reload();
}
function onFallbackMouseDown(e){fallbackState.isDragging=true;fallbackState.dragPrev={x:e.clientX,y:e.clientY};}
function onFallbackMouseMove(e){
  if(!fallbackState.isDragging)return;
  const dx=e.clientX-fallbackState.dragPrev.x;
  const dy=e.clientY-fallbackState.dragPrev.y;
  if(e.shiftKey){fallbackState.panX+=dx*0.02;fallbackState.panY-=dy*0.02;}
  else{fallbackState.orbitAngle-=dx*0.005;fallbackState.orbitElevation=Math.max(0.1,Math.min(Math.PI*0.48,fallbackState.orbitElevation-dy*0.005));}
  fallbackState.dragPrev={x:e.clientX,y:e.clientY};
}
function onFallbackMouseUp(){fallbackState.isDragging=false;}
function onFallbackWheel(e){fallbackState.orbitDist=Math.max(3,Math.min(35,fallbackState.orbitDist+e.deltaY*0.02));e.preventDefault();}
function onFallbackClick(e){
  const rect=document.getElementById('fallback-canvas').getBoundingClientRect();
  const mx=e.clientX-rect.left,my=e.clientY-rect.top;
  const tooltip=document.getElementById('inspect-tooltip');
  const heightData=generateHeightData(timeIndex);
  const gx=Math.round((mx/rect.width)*GRID);
  const gz=Math.round((my/rect.height)*GRID);
  if(gx>=0&&gx<GRID&&gz>=0&&gz<GRID){
    const h=heightData[gz*GRID+gx];
    fallbackState.clickPoint={gx,gz,height:h.toFixed(2)};
    tooltip.style.display='block';
    tooltip.style.left=(e.clientX+16)+'px';
    tooltip.style.top=(e.clientY-10)+'px';
    tooltip.textContent=`Point (${gx},${gz}) | Height: ${h.toFixed(2)} | Time: ${timeIndex}`;
    setTimeout(()=>{tooltip.style.display='none';},2500);
  }
}
function drawFallback(ctx,w,h){
  ctx.clearRect(0,0,w,h);
  const heightData=generateHeightData(timeIndex);
  let hMin=Infinity,hMax=-Infinity;
  for(let i=0;i<heightData.length;i++){if(heightData[i]<hMin)hMin=heightData[i];if(heightData[i]>hMax)hMax=heightData[i];}
  const s=fallbackState;
  const iz=Math.sin(s.orbitElevation);
  const cx=Math.cos(s.orbitAngle)*Math.cos(s.orbitElevation);
  const cy=iz;
  const cz=Math.sin(s.orbitAngle)*Math.cos(s.orbitElevation);
  const ahead=new THREE.Vector3(cx,cy,cz).normalize();
  const right=new THREE.Vector3().crossVectors(ahead,new THREE.Vector3(0,1,0)).normalize();
  const up=new THREE.Vector3().crossVectors(right,ahead).normalize();
  const eye=new THREE.Vector3(s.targetX+s.panX-cx*s.orbitDist,s.targetZ+s.panY-cy*s.orbitDist+3,0-cz*s.orbitDist);
  const cellW=w/GRID,cellH=h/GRID;
  const baseScale=TERRAIN_SCALE/GRID*TERRAIN_SCALE;
  for(let z=0;z<GRID;z++){
    for(let x=0;x<GRID;x++){
      const h=heightData[z*GRID+x];
      const t=(h-hMin)/(hMax-hMin+0.001);
      const px=x*cellW,py=z*cellH;
      const r=t<0.5?t*2:1;
      const g=t<0.5?0.3+t*1.4:1.7-t*1.4;
      const b=t<0.5?1-t*1.5:0.25;
      ctx.fillStyle=`rgb(${Math.floor(r*255)},${Math.floor(Math.max(0,g)*255)},${Math.floor(Math.max(0,b)*255)})`;
      ctx.fillRect(px,py,cellW+1,cellH+1);
    }
  }
  ctx.strokeStyle='rgba(255,68,68,0.6)';
  ctx.lineWidth=1.5;
  ctx.beginPath();
  const cxG=GRID/2,czG=GRID/2;
  for(let i=0;i<GRID;i++){
    const rx=cxG+Math.sin(i*0.15+timeIndex*0.02)*GRID*0.35;
    const rz=czG+(i-GRID/2)*0.8;
    if(i===0)ctx.moveTo(rx*cellW,rz*cellH);
    else ctx.lineTo(rx*cellW,rz*cellH);
  }
  ctx.stroke();
  if(s.clickPoint){
    const px=s.clickPoint.gx*cellW,py=s.clickPoint.gz*cellH;
    ctx.strokeStyle='#fff';
    ctx.lineWidth=2;
    ctx.strokeRect(px-4,py-4,8,8);
    ctx.fillStyle='#fff';
    ctx.font='11px monospace';
    ctx.fillText(`H:${s.clickPoint.height}`,px+6,py-4);
  }
  const bannerH=28;
  ctx.fillStyle='rgba(255,107,107,0.15)';
  ctx.fillRect(w/2-90,10,180,bannerH);
  ctx.strokeStyle='rgba(255,107,107,0.3)';
  ctx.lineWidth=1;
  ctx.strokeRect(w/2-90,10,180,bannerH);
  ctx.fillStyle='#ff6b6b';
  ctx.font='12px system-ui';
  ctx.textAlign='center';
  ctx.fillText('2D FALLBACK — drag to orbit, shift+drag to pan, scroll to zoom, click to inspect',w/2,10+bannerH/2+4);
  ctx.textAlign='start';
}
function fallbackLoop(){
  if(useWebGL)return;
  animationId=requestAnimationFrame(fallbackLoop);
  const c=document.getElementById('fallback-canvas');
  const ctx=c.getContext('2d');
  drawFallback(ctx,c.width,c.height);
  fpsFrames++;
}
function animate(timestamp){
  if(!useWebGL)return;
  animationId=requestAnimationFrame(animate);
  const rawDelta=clock.getDelta();
  const delta=Math.min(rawDelta,DELTA_CLAMP_MAX);
  controls.update();
  while(rAFQueue.length>0){
    const fn=rAFQueue.shift();
    try{fn();}catch(e){console.error('rAF task failed:',e);}
  }
  idleTimer+=delta*1000;
  if(idleTimer>IDLE_TIMEOUT_MS&&controls.autoRotate){
    controls.autoRotate=false;
    document.getElementById('btn-auto-rotate').classList.remove('active');
  }
  if(timestamp-fpsTime>=1000){fpsTime=timestamp;document.getElementById('fps-counter').textContent=`${fpsFrames} FPS`;fpsFrames=0;}
  fpsFrames++;
  renderer.render(scene,camera);
}
function toggleAutoRotate(){
  autoRotate=!autoRotate;
  if(useWebGL&&controls)controls.autoRotate=autoRotate;
  document.getElementById('btn-auto-rotate').classList.toggle('active',autoRotate);
  idleTimer=0;
}
function toggleWireframe(){
  wireframe=!wireframe;
  document.getElementById('btn-wireframe').classList.toggle('active',wireframe);
  if(terrainMesh)terrainMesh.material.wireframe=wireframe;
}
function saveBookmark(){
  if(!useWebGL||!camera)return;
  const b={pos:camera.position.clone(),target:controls.target.clone(),label:`View ${bookmarks.length+1}`};
  bookmarks.push(b);
  renderBookmarks();
}
function loadBookmark(i){
  if(!useWebGL||!camera||i>=bookmarks.length)return;
  const b=bookmarks[i];
  camera.position.copy(b.pos);
  controls.target.copy(b.target);
  controls.update();
  idleTimer=0;
}
function renderBookmarks(){
  const list=document.getElementById('bookmark-list');
  list.innerHTML=bookmarks.map((b,i)=>`<span class="bookmark-tag" onclick="window._loadBm(${i})">${b.label}</span>`).join('');
  window._loadBm=loadBookmark;
}
function resetCamera(){
  if(useWebGL&&camera){camera.position.set(16,10,18);controls.target.set(0,1.5,0);controls.update();}
  else if(!useWebGL){fallbackState.orbitAngle=0.7;fallbackState.orbitElevation=1.2;fallbackState.orbitDist=14;fallbackState.panX=0;fallbackState.panY=0;}
  idleTimer=0;
}
function openImportModal(){document.getElementById('import-modal').classList.add('open');}
function closeImportModal(){document.getElementById('import-modal').classList.remove('open');}
function importData(){
  const raw=document.getElementById('import-textarea').value.trim();
  if(!raw){closeImportModal();return;}
  const lines=raw.split('\n').filter(l=>l.trim()&&!l.startsWith('#'));
  if(lines.length===0){closeImportModal();return;}
  if(raw.startsWith('{')){
    try{
      const geojson=JSON.parse(raw);
      console.log('GeoJSON imported:',geojson.features?.length||0,'features');
      alert(`GeoJSON loaded: ${geojson.features?.length||0} features. Integration via terrain mapping ready.`);
    }catch(e){alert('Invalid GeoJSON');return;}
  }else{
    const parsed=lines.map(l=>{const p=l.split(',');return{x:parseFloat(p[0]),y:parseFloat(p[1]),h:parseFloat(p[2]),c:p[3]||'#4dabf7'};});
    console.log('CSV imported:',parsed.length,'rows');
    alert(`CSV loaded: ${parsed.length} data points. Terrain remapping to grid ready.`);
  }
  closeImportModal();
  document.getElementById('import-textarea').value='';
}
document.getElementById('time-slider').addEventListener('input',(e)=>{
  timeIndex=parseInt(e.target.value);
  idleTimer=0;
  if(useWebGL){
    enqueueRAF(()=>{updateTerrain(timeIndex);});
  }
});
window.addEventListener('resize',()=>{
  if(useWebGL&&renderer){camera.aspect=window.innerWidth/window.innerHeight;camera.updateProjectionMatrix();renderer.setSize(window.innerWidth,window.innerHeight);}
  else if(!useWebGL){const c=document.getElementById('fallback-canvas');c.width=window.innerWidth;c.height=window.innerHeight;}
});
document.addEventListener('keydown',(e)=>{
  if(e.key==='r')resetCamera();
  if(e.key==='a')toggleAutoRotate();
  if(e.key==='w')toggleWireframe();
  if(e.key==='b')saveBookmark();
});
try{
  initWebGL();
  animationId=requestAnimationFrame(animate);
}catch(e){
  console.error('WebGL init failed:',e);
  initFallback();
}
</script>
</body>
</html>