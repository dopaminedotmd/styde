<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>3D Data Terrain</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{overflow:hidden;background:#0a0a14;font-family:system-ui;-webkit-tap-highlight-color:transparent}
canvas{display:block}
#ui{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);z-index:10;display:flex;gap:12px;align-items:center;background:rgba(10,10,20,0.85);padding:10px 18px;border-radius:10px;backdrop-filter:blur(8px);border:1px solid rgba(79,195,247,0.15)}
#time-slider{width:180px;accent-color:#4fc3f7;cursor:pointer}
#ui label{color:#bbb;font-size:11px;white-space:nowrap;user-select:none}
#bookmarks{position:fixed;top:16px;right:16px;z-index:10;display:flex;gap:5px;flex-wrap:wrap}
#bookmarks button{background:rgba(10,10,20,0.75);color:#4fc3f7;border:1px solid rgba(79,195,247,0.25);padding:5px 10px;border-radius:6px;cursor:pointer;font-size:10px;transition:background .15s}
#bookmarks button:hover{background:rgba(79,195,247,0.18)}
#diag{position:fixed;top:16px;left:16px;z-index:10;color:#7b7;font-size:10px;background:rgba(10,10,20,0.75);padding:7px 12px;border-radius:6px;line-height:1.6;font-family:monospace;border:1px solid rgba(100,180,100,0.2)}
.auto-label{cursor:pointer;color:#4fc3f7;font-size:14px;user-select:none}
@media(max-width:600px){
  #ui{padding:8px 12px;gap:8px;bottom:12px}
  #time-slider{width:110px}
  #bookmarks button{padding:4px 7px;font-size:9px}
  #diag{font-size:9px;padding:5px 10px}
}
</style>
</head>
<body>
<div id="diag">cache hits: 0 | misses: 0 | geom: 0</div>
<div id="bookmarks">
<button onclick="saveBm(0)">Set B1</button>
<button onclick="saveBm(1)">Set B2</button>
<button onclick="saveBm(2)">Set B3</button>
<button onclick="goBm(0)">B1</button>
<button onclick="goBm(1)">B2</button>
<button onclick="goBm(2)">B3</button>
</div>
<div id="ui">
<label>T:</label>
<input type="range" id="time-slider" min="0" max="99" value="0" step="1">
<label id="tl">0/99</label>
<span class="auto-label" onclick="togAR()" title="auto-rotate">⟳</span>
</div>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 40, STEPS = 100, SPACING = 10 / (GRID - 1);
const C = { geom: new Map(), rivers: new Map(), bm: [null, null, null], hits: 0, miss: 0 };
function cget(k, fn) {
  if (C.geom.has(k)) { C.hits++; return C.geom.get(k); }
  C.miss++;
  const v = fn();
  C.geom.set(k, v);
  return v;
}
function updDiag() {
  document.getElementById('diag').textContent =
    `cache hits: ${C.hits} | misses: ${C.miss} | geom: ${C.geom.size} | rivers: ${C.rivers.size}`;
}
// Synthetic time-series: 100 steps of 40x40 grids
const data = [];
(function gen() {
  for (let t = 0; t < STEPS; t++) {
    const h = new Float32Array(GRID * GRID);
    const u = new Float32Array(GRID * GRID);
    const e = new Float32Array(GRID * GRID);
    const tf = t / STEPS;
    for (let i = 0; i < GRID; i++) {
      for (let j = 0; j < GRID; j++) {
        const x = (i - GRID / 2) / (GRID / 4);
        const z = (j - GRID / 2) / (GRID / 4);
        const h1 = 3.2 * Math.exp(-((x - 2 * Math.sin(tf * Math.PI * 2)) ** 2 + (z - 1) ** 2) / 4);
        const h2 = 2.6 * Math.exp(-((x + 1.5) ** 2 + (z + 2 * Math.cos(tf * Math.PI)) ** 2) / 3.2);
        const h3 = 1.7 * Math.exp(-((x - 1) ** 2 + (z - 2.5) ** 2) / 2.5) * (0.6 + 0.4 * Math.sin(tf * Math.PI * 3));
        const hv = h1 + h2 + h3;
        h[i * GRID + j] = hv;
        u[i * GRID + j] = Math.min(1, Math.max(0, hv * 0.28 + (Math.sin(i * 0.7 + tf * 5) * 0.5 + 0.5) * 0.2));
        e[i * GRID + j] = Math.max(0, 0.03 + (1 - u[i * GRID + j]) * 0.25 * (0.4 + 0.6 * Math.abs(Math.sin(x * z * 0.8 + tf * 3))));
      }
    }
    data.push({ h, u, e });
  }
})();
// Renderer
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);
// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x080c16);
scene.fog = new THREE.FogExp2(0x080c16, 0.0008);
// Camera + Controls
const camera = new THREE.PerspectiveCamera(52, window.innerWidth / window.innerHeight, 0.4, 80);
camera.position.set(11, 7, 11);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.07;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.25;
controls.target.set(0, 0.6, 0);
controls.maxPolarAngle = Math.PI * 0.68;
controls.minDistance = 3;
controls.maxDistance = 25;
controls.update();
// Lights
scene.add(new THREE.AmbientLight(0x1a2a3a, 1.6));
const sun = new THREE.DirectionalLight(0xffeedd, 3.8);
sun.position.set(10, 14, 5);
sun.castShadow = true;
sun.shadow.mapSize.set(512, 512);
sun.shadow.camera.near = 0.3;
sun.shadow.camera.far = 50;
sun.shadow.camera.left = -14;
sun.shadow.camera.right = 14;
sun.shadow.camera.top = 14;
sun.shadow.camera.bottom = -14;
sun.shadow.bias = -0.0005;
scene.add(sun);
// Ground plane (receive shadows, add depth reference)
const gGeo = new THREE.PlaneGeometry(22, 22);
const gMat = new THREE.MeshPhongMaterial({ color: 0x141428, transparent: true, opacity: 0.35, depthWrite: true });
const ground = new THREE.Mesh(gGeo, gMat);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.4;
ground.receiveShadow = true;
scene.add(ground);
// Background stars
const sGeo = new THREE.BufferGeometry();
const sPos = new Float32Array(600 * 3);
for (let i = 0; i < 600; i++) {
  sPos[i * 3] = (Math.random() - 0.5) * 42;
  sPos[i * 3 + 1] = Math.random() * 18 + 3;
  sPos[i * 3 + 2] = (Math.random() - 0.5) * 42;
}
sGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3));
scene.add(new THREE.Points(sGeo, new THREE.PointsMaterial({ color: 0x334455, size: 0.05, transparent: true, opacity: 0.5, depthWrite: false })));
// Terrain: pre-allocate arrays, NEVER reallocate per tick
const posA = new Float32Array(GRID * GRID * 3);
const colA = new Float32Array(GRID * GRID * 3);
const idx = [];
for (let i = 0; i < GRID - 1; i++)
  for (let j = 0; j < GRID - 1; j++) {
    const a = i * GRID + j, b = a + 1, c = a + GRID, d = c + 1;
    idx.push(a, b, d, a, d, c);
  }
const tGeo = new THREE.BufferGeometry();
tGeo.setIndex(idx);
tGeo.setAttribute('position', new THREE.BufferAttribute(posA, 3));
tGeo.setAttribute('color', new THREE.BufferAttribute(colA, 3));
const tMat = new THREE.MeshPhongMaterial({ vertexColors: true, specular: 0x111122, shininess: 18, side: THREE.DoubleSide, flatShading: false });
const tMesh = new THREE.Mesh(tGeo, tMat);
tMesh.castShadow = true;
tMesh.receiveShadow = true;
scene.add(tMesh);
function updTerrain(t) {
  const d = data[t];
  for (let i = 0; i < GRID; i++)
    for (let j = 0; j < GRID; j++) {
      const k = i * GRID + j;
      const hv = d.h[k], uv = d.u[k];
      posA[k * 3] = (i - GRID / 2) * SPACING;
      posA[k * 3 + 1] = hv;
      posA[k * 3 + 2] = (j - GRID / 2) * SPACING;
      colA[k * 3] = 0.08 + uv * 0.45;
      colA[k * 3 + 1] = 0.18 + uv * 0.58;
      colA[k * 3 + 2] = 0.04 + (1 - uv) * 0.18;
    }
  tGeo.attributes.position.needsUpdate = true;
  tGeo.attributes.color.needsUpdate = true;
  tGeo.computeVertexNormals();
  C.geom.clear(); // invalidate dependent caches on terrain change
  updRivers(t);
  updParticles(t);
}
// Rivers: cached TubeGeometry per time step (debounced via slider)
let riverMesh;
function updRivers(t) {
  if (C.rivers.has(t)) { C.hits++; return; }
  C.miss++;
  const d = data[t];
  // Greedy path: start at max-error cell, walk to highest-error neighbor
  let cur = 0, mx = 0;
  for (let i = 0; i < d.e.length; i++) if (d.e[i] > mx) { mx = d.e[i]; cur = i; }
  const seen = new Set(), pts = [];
  for (let s = 0; s < 45 && !seen.has(cur); s++) {
    seen.add(cur);
    const ci = Math.floor(cur / GRID), cj = cur % GRID;
    pts.push(new THREE.Vector3((ci - GRID / 2) * SPACING, d.h[cur] + 0.18, (cj - GRID / 2) * SPACING));
    let best = -1, be = -1;
    for (const [di, dj] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
      const ni = ci + di, nj = cj + dj;
      if (ni >= 0 && ni < GRID && nj >= 0 && nj < GRID) {
        const nk = ni * GRID + nj;
        if (!seen.has(nk) && d.e[nk] > be) { be = d.e[nk]; best = nk; }
      }
    }
    if (best < 0) break;
    cur = best;
  }
  if (pts.length < 2) return;
  const curve = new THREE.CatmullRomCurve3(pts);
  const tubeGeo = new THREE.TubeGeometry(curve, 36, 0.10, 6, false);
  C.rivers.set(t, tubeGeo);
  if (riverMesh) { riverMesh.geometry.dispose(); riverMesh.geometry = tubeGeo; }
  else {
    riverMesh = new THREE.Mesh(tubeGeo, new THREE.MeshPhongMaterial({ color: 0xff3311, emissive: 0x330000, transparent: true, opacity: 0.82, depthWrite: true }));
    riverMesh.renderOrder = 1;
    scene.add(riverMesh);
  }
}
// Particles: reusable BufferGeometry + pre-allocated position array
const PCOUNT = 180;
const pPos = new Float32Array(PCOUNT * 3);
const pState = []; // {si,sj,ei,ej,prog} per particle
(function initP() {
  for (let i = 0; i < PCOUNT; i++)
    pState.push({
      si: Math.floor(Math.random() * GRID), sj: Math.floor(Math.random() * GRID),
      ei: Math.floor(Math.random() * GRID), ej: Math.floor(Math.random() * GRID),
      prog: Math.random()
    });
  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
  const pMat = new THREE.PointsMaterial({ color: 0x4fc3f7, size: 0.14, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.65 });
  const pSys = new THREE.Points(pGeo, pMat);
  pSys.name = 'particles';
  scene.add(pSys);
})();
function updParticles(t) {
  const d = data[t];
  for (let i = 0; i < PCOUNT; i++) {
    const s = pState[i];
    s.prog += 0.0025 + Math.random() * 0.0035;
    if (s.prog > 1) s.prog -= 1;
    const ci = s.si + (s.ei - s.si) * s.prog;
    const cj = s.sj + (s.ej - s.sj) * s.prog;
    const fi = Math.max(0, Math.min(GRID - 1, Math.floor(ci)));
    const fj = Math.max(0, Math.min(GRID - 1, Math.floor(cj)));
    pPos[i * 3] = (ci - GRID / 2) * SPACING;
    pPos[i * 3 + 1] = d.h[fi * GRID + fj] + 0.5;
    pPos[i * 3 + 2] = (cj - GRID / 2) * SPACING;
  }
  scene.getObjectByName('particles').geometry.attributes.position.needsUpdate = true;
}
// Bookmarks
window.saveBm = function(s) { C.bm[s] = { p: camera.position.clone(), t: controls.target.clone() }; };
window.goBm = function(s) {
  const b = C.bm[s];
  if (!b) return;
  const sp = camera.position.clone(), st = controls.target.clone();
  const t0 = performance.now();
  (function anim(now) {
    const f = Math.min(1, (now - t0) / 750);
    const e = f < 0.5 ? 2 * f * f : 1 - Math.pow(-2 * f + 2, 2) / 2;
    camera.position.lerpVectors(sp, b.p, e);
    controls.target.lerpVectors(st, b.t, e);
    controls.update();
    if (f < 1) requestAnimationFrame(anim);
  })(t0);
};
window.togAR = function() { controls.autoRotate = !controls.autoRotate; };
C.bm[0] = { p: new THREE.Vector3(11, 7, 11), t: new THREE.Vector3(0, 0.6, 0) };
C.bm[1] = { p: new THREE.Vector3(2.5, 1.8, 7), t: new THREE.Vector3(-1.2, 1.4, 1.8) };
C.bm[2] = { p: new THREE.Vector3(7, 4.5, -3), t: new THREE.Vector3(2, 2.2, -2.3) };
// Time slider with 200ms debounce
let dbTimer = null, curT = 0;
const slider = document.getElementById('time-slider');
const tl = document.getElementById('tl');
slider.addEventListener('input', () => {
  curT = parseInt(slider.value);
  tl.textContent = `${curT}/99`;
  if (dbTimer) clearTimeout(dbTimer);
  dbTimer = setTimeout(() => { updTerrain(curT); updDiag(); }, 200);
});
updTerrain(0);
updDiag();
// Render loop: controls + render, NO geometry allocation
function loop() {
  requestAnimationFrame(loop);
  controls.update();
  renderer.render(scene, camera);
}
loop();
// Responsive: resize + reduce DPI on narrow screens for mobile performance
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, window.innerWidth < 600 ? 1.5 : 2));
});
renderer.domElement.addEventListener('touchstart', () => { controls.autoRotate = false; }, { once: true });
</script>
</body>
</html>