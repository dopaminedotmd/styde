<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>3D Data Terrain Explorer</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0e1a; overflow: hidden; font-family: system-ui, sans-serif; color: #c8d0e0; }
  canvas { display: block; }
  #ui { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
  #timebar { position: absolute; bottom: 32px; left: 50%; transform: translateX(-50%); pointer-events: auto; display: flex; align-items: center; gap: 12px; background: rgba(10,14,26,0.85); border: 1px solid rgba(200,208,224,0.15); border-radius: 12px; padding: 10px 20px; backdrop-filter: blur(8px); }
  #timebar input[type=range] { width: 260px; height: 4px; -webkit-appearance: none; background: linear-gradient(90deg, #2a6f97, #52b788, #ffd166, #ef476f); border-radius: 2px; outline: none; cursor: pointer; }
  #timebar input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; border-radius: 50%; background: #fff; border: 2px solid #52b788; cursor: pointer; }
  #timelabel { font-size: 13px; font-variant-numeric: tabular-nums; min-width: 80px; text-align: center; letter-spacing: 0.5px; }
  #topbar { position: absolute; top: 16px; left: 50%; transform: translateX(-50%); pointer-events: auto; display: flex; gap: 8px; align-items: center; background: rgba(10,14,26,0.8); border: 1px solid rgba(200,208,224,0.12); border-radius: 10px; padding: 8px 16px; backdrop-filter: blur(8px); }
  #topbar button { pointer-events: auto; background: rgba(82,183,136,0.15); border: 1px solid rgba(82,183,136,0.3); color: #c8d0e0; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; transition: all 0.2s; letter-spacing: 0.3px; }
  #topbar button:hover { background: rgba(82,183,136,0.3); color: #fff; }
  #topbar button.active { background: rgba(82,183,136,0.35); border-color: #52b788; color: #fff; }
  #legend { position: absolute; right: 24px; top: 50%; transform: translateY(-50%); pointer-events: none; display: flex; flex-direction: column; align-items: flex-end; gap: 4px; font-size: 11px; opacity: 0.7; letter-spacing: 0.3px; }
  #legend .gradient { width: 14px; height: 120px; border-radius: 4px; background: linear-gradient(to top, #2d6a4f, #52b788, #ffd166, #ef476f); margin-bottom: 4px; }
  #stats { position: absolute; left: 24px; bottom: 100px; pointer-events: none; font-size: 12px; opacity: 0.5; line-height: 1.6; font-variant-numeric: tabular-nums; }
  #stats span { color: #52b788; }
  .btn-group { display: flex; gap: 6px; }
  .badge { font-size: 10px; opacity: 0.4; margin-left: 4px; }
</style>
</head>
<body>
<div id=ui>
  <div id=topbar>
    <span style="font-size:13px;letter-spacing:1px;text-transform:uppercase;opacity:0.6">Data Terrain</span>
    <div class=btn-group>
      <button id=btnAutorotate class=active>Orbit</button>
      <button id=btnBookmark1>B1</button>
      <button id=btnBookmark2>B2</button>
      <button id=btnBookmark3>B3</button>
    </div>
    <span class=badge>drag to orbit . scroll to zoom</span>
  </div>
  <div id=legend>
    <div class=gradient></div>
    <div>high</div>
    <div style="margin-top:-2px">low</div>
  </div>
  <div id=stats>
    peaks: <span id=statPeaks>0</span><br>
    rivers: <span id=statRivers>0</span><br>
    particles: <span id=statParticles>0</span>
  </div>
  <div id=timebar>
    <span style="font-size:11px;opacity:0.5">time</span>
    <input type=range id=timeSlider min=0 max=29 value=15 step=1>
    <span id=timelabel>t = 15</span>
  </div>
</div>
<script type=importmap>
{
  "imports": {
    "three": "https://cdn.jsdelivr.net/npm/three@0.163.0/build/three.module.js",
    "three/addons/": "https://cdn.jsdelivr.net/npm/three@0.163.0/examples/jsm/"
  }
}
</script>
<script type=module>
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const GRID = 72;
const TIMESTEPS = 30;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0e1a);
scene.fog = new THREE.Fog(0x0a0e1a, 55, 110);
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 200);
camera.position.set(38, 32, 48);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = false;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.prepend(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.06;
controls.autoRotate = true;
controls.autoRotateSpeed = 0.8;
controls.minDistance = 8;
controls.maxDistance = 120;
controls.maxPolarAngle = Math.PI/2.15;
controls.target.set(0, 0, 0);
const clock = new THREE.Clock();
// ---- data generation ----
function buildTimeSeries(grid, timesteps) {
  const data = [];
  for (let t = 0; t < timesteps; t++) {
    const slice = [];
    for (let iz = 0; iz < grid; iz++) {
      for (let ix = 0; ix < grid; ix++) {
        const x = (ix / (grid-1)) * 2 - 1;
        const z = (iz / (grid-1)) * 2 - 1;
        const phase = t / timesteps;
        // revenue: peaks that shift and pulse
        const peak1 = Math.exp(-((x-0.3)**2 + (z+0.1)**2)*5) * (1.8 + 0.6*Math.sin(phase*Math.PI*2));
        const peak2 = Math.exp(-((x+0.5)**2 + (z-0.4)**2)*4) * (1.4 + 0.5*Math.cos(phase*Math.PI*1.3));
        const peak3 = Math.exp(-((x-0.1)**2 + (z+0.6)**2)*6) * (1.2 + 0.4*Math.sin(phase*Math.PI*2.7));
        const ridge = 0.3 * Math.max(0, Math.sin(x*3 + phase*4)*0.5+0.5) * Math.max(0, Math.cos(z*2.5 + phase*3)*0.5+0.5);
        const noise = 0.04 * (Math.sin(x*12+phase*8)*Math.cos(z*10+phase*6) + Math.sin(x*7+z*9+phase*11));
        const h = peak1 + peak2 + peak3 + ridge + noise;
        // density: vegetation / user density
        const density = 0.3 + 0.7 * (0.5 + 0.5*Math.sin(x*4+phase*3)*Math.cos(z*4+phase*2));
        // error rate: spikes near valley edges, some random spikes
        const errRaw = Math.max(0, 0.02 + 0.15*Math.exp(-((x-0.1)**2+(z+0.3)**2)*20) * (1+0.8*Math.sin(phase*8)) + 0.08*(Math.sin(x*5+phase*10)**2*Math.cos(z*5+phase*7)**2));
        const err = Math.min(1, errRaw);
        slice.push({ height: h, density, error: err });
      }
    }
    data.push(slice);
  }
  return data;
}
const fullData = buildTimeSeries(GRID, TIMESTEPS);
// ---- terrain geometry ----
function buildTerrain(timeIndex) {
  const data = fullData[timeIndex];
  const geo = new THREE.BufferGeometry();
  const verts = [];
  const colors = [];
  const idxs = [];
  const uvs = [];
  const scale = 16;
  const spacing = scale / (GRID - 1);
  for (let iz = 0; iz < GRID; iz++) {
    for (let ix = 0; ix < GRID; ix++) {
      const i = iz * GRID + ix;
      const d = data[i];
      const x = (ix / (GRID-1) - 0.5) * scale;
      const z = (iz / (GRID-1) - 0.5) * scale;
      const y = d.height * 5;
      verts.push(x, y, z);
      // color: vegetation gradient based on density + height accent
      const den = d.density;
      const hNorm = Math.min(1, d.height * 0.6);
      // green -> yellow -> red gradient
      const r = 0.15 + 0.85 * (1 - den) * 0.7 + hNorm * 0.3;
      const g = 0.25 + 0.75 * den * 0.8 + hNorm * 0.2;
      const b = 0.1 + 0.3 * (1 - den) * 0.5;
      colors.push(r, g, b);
      uvs.push(ix/(GRID-1), iz/(GRID-1));
    }
  }
  for (let iz = 0; iz < GRID-1; iz++) {
    for (let ix = 0; ix < GRID-1; ix++) {
      const a = iz*GRID + ix;
      const b = iz*GRID + ix+1;
      const c = (iz+1)*GRID + ix;
      const d20 = (iz+1)*GRID + ix+1;
      idxs.push(a, b, c, b, d20, c);
    }
  }
  geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  geo.setIndex(idxs);
  geo.computeVertexNormals();
  return { geo, data };
}
function buildRiverGeo(timeIndex) {
  const data = fullData[timeIndex];
  const scale = 16;
  const spacing = scale / (GRID - 1);
  // find error hot spots and trace rivers
  const threshold = 0.12;
  const points = [];
  const visited = new Set();
  for (let iz = 1; iz < GRID-1; iz++) {
    for (let ix = 1; ix < GRID-1; ix++) {
      const i = iz*GRID + ix;
      if (data[i].error > threshold && !visited.has(i)) {
        // trace a river
        const segs = [];
        let cx = (ix / (GRID-1) - 0.5) * scale;
        let cz = (iz / (GRID-1) - 0.5) * scale;
        let cy = data[i].height * 5;
        segs.push(cx, cy + 0.08, cz);
        visited.add(i);
        let cxIdx = ix, cyIdx = iz;
        for (let step = 0; step < 20; step++) {
          // find steepest downhill neighbor
          let bestDir = null;
          let bestH = data[cyIdx*GRID+cxIdx].height;
          const dirs = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,1],[1,-1],[-1,-1]];
          for (const [dx, dz] of dirs) {
            const nx = cxIdx + dx;
            const nz = cyIdx + dz;
            if (nx < 0 || nx >= GRID || nz < 0 || nz >= GRID) continue;
            const ni = nz*GRID + nx;
            if (visited.has(ni)) continue;
            const nh = data[ni].height;
            if (nh < bestH) {
              bestH = nh;
              bestDir = [dx, dz];
            }
          }
          if (!bestDir) break;
          cxIdx += bestDir[0];
          cyIdx += bestDir[1];
          const ni2 = cyIdx*GRID + cxIdx;
          visited.add(ni2);
          const fx = (cxIdx / (GRID-1) - 0.5) * scale;
          const fz = (cyIdx / (GRID-1) - 0.5) * scale;
          const fy = data[ni2].height * 5;
          segs.push(fx, fy + 0.08, fz);
        }
        if (segs.length >= 6) {
          // create river tube from segments
          const tubePath = [];
          for (let s = 0; s < segs.length; s += 3) {
            tubePath.push(new THREE.Vector3(segs[s], segs[s+1], segs[s+2]));
          }
          if (tubePath.length >= 3) {
            const curve = new THREE.CatmullRomCurve3(tubePath);
            const tubeGeo = new THREE.TubeGeometry(curve, Math.min(tubePath.length*3, 48), 0.06, 4, false);
            points.push(tubeGeo);
          }
        }
      }
    }
  }
  return points;
}
function buildParticles(timeIndex) {
  const data = fullData[timeIndex];
  const count = 1200;
  const positions = new Float32Array(count * 3);
  const sizes = new Float32Array(count);
  const offsets = new Float32Array(count);
  const scale = 16;
  for (let i = 0; i < count; i++) {
    const ix = Math.floor(Math.random() * GRID);
    const iz = Math.floor(Math.random() * GRID);
    const idx = iz * GRID + ix;
    const d = data[idx];
    const x = (ix / (GRID-1) - 0.5) * scale;
    const z = (iz / (GRID-1) - 0.5) * scale;
    const y = d.height * 5 + 0.5 + Math.random() * 1.5;
    positions[i*3] = x;
    positions[i*3+1] = y;
    positions[i*3+2] = z;
    sizes[i] = 0.08 + Math.random() * 0.2;
    offsets[i] = Math.random() * 100;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geo.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));
  return geo;
}
// ---- build scene objects ----
let terrainMesh = null;
let terrainData = null;
let riverGroup = new THREE.Group();
let particleSystem = null;
let particleGeo = null;
function createTerrain(timeIndex) {
  if (terrainMesh) {
    scene.remove(terrainMesh);
    terrainMesh.geometry.dispose();
    terrainMesh.material.dispose();
  }
  const { geo, data } = buildTerrain(timeIndex);
  terrainData = data;
  const mat = new THREE.MeshStandardMaterial({
    vertexColors: true,
    roughness: 0.65,
    metalness: 0.05,
    flatShading: false,
    side: THREE.DoubleSide,
    envMapIntensity: 0.3,
  });
  terrainMesh = new THREE.Mesh(geo, mat);
  terrainMesh.receiveShadow = false;
  terrainMesh.castShadow = false;
  terrainMesh.position.y = 0;
  scene.add(terrainMesh);
}
function createRivers(timeIndex) {
  scene.remove(riverGroup);
  riverGroup.children.forEach(c => {
    if (c.geometry) c.geometry.dispose();
    if (c.material) c.material.dispose();
  });
  riverGroup = new THREE.Group();
  const tubes = buildRiverGeo(timeIndex);
  const mat2 = new THREE.MeshStandardMaterial({
    color: 0xef476f,
    emissive: 0xef476f,
    emissiveIntensity: 0.3,
    roughness: 0.2,
    metalness: 0.1,
    transparent: true,
    opacity: 0.75,
  });
  for (const tubeGeo of tubes) {
    const mesh = new THREE.Mesh(tubeGeo, mat2);
    riverGroup.add(mesh);
  }
  scene.add(riverGroup);
}
function createParticles(timeIndex) {
  if (particleSystem) {
    scene.remove(particleSystem);
    particleSystem.geometry.dispose();
    particleSystem.material.dispose();
  }
  particleGeo = buildParticles(timeIndex);
  const mat3 = new THREE.PointsMaterial({
    size: 0.15,
    sizeAttenuation: true,
    color: 0x52b788,
    transparent: true,
    opacity: 0.7,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
  });
  particleSystem = new THREE.Points(particleGeo, mat3);
  scene.add(particleSystem);
}
// ---- ambient & lights ----
const ambient = new THREE.AmbientLight(0x446688, 0.5);
scene.add(ambient);
const dirLight = new THREE.DirectionalLight(0xffeedd, 1.8);
dirLight.position.set(25, 40, 20);
scene.add(dirLight);
const fillLight = new THREE.DirectionalLight(0x88bbff, 0.6);
fillLight.position.set(-20, 10, -30);
scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0x6688cc, 0.4);
rimLight.position.set(0, -10, 40);
scene.add(rimLight);
// ---- ground plane glow ----
const glowGeo = new THREE.PlaneGeometry(30, 30);
const glowMat = new THREE.MeshBasicMaterial({
  color: 0x1a2a3a,
  transparent: true,
  opacity: 0.15,
  side: THREE.DoubleSide,
});
const glowPlane = new THREE.Mesh(glowGeo, glowMat);
glowPlane.rotation.x = -Math.PI/2;
glowPlane.position.y = -1.5;
scene.add(glowPlane);
// ---- build initial scene ----
let currentTime = 15;
createTerrain(currentTime);
createRivers(currentTime);
createParticles(currentTime);
// update stats
function updateStats() {
  let peaks = 0;
  let riverCount = riverGroup.children.length;
  let particleCount = 0;
  if (terrainData) {
    for (const d of terrainData) {
      if (d.height > 0.8) peaks++;
    }
  }
  if (particleSystem && particleSystem.geometry.attributes.position) {
    particleCount = particleSystem.geometry.attributes.position.count;
  }
  document.getElementById('statPeaks').textContent = peaks;
  document.getElementById('statRivers').textContent = riverCount;
  document.getElementById('statParticles').textContent = particleCount;
}
updateStats();
// ---- time slider ----
const slider = document.getElementById('timeSlider');
const label = document.getElementById('timelabel');
slider.addEventListener('input', () => {
  const t = parseInt(slider.value);
  currentTime = t;
  label.textContent = 't = ' + t;
  createTerrain(t);
  createRivers(t);
  createParticles(t);
  updateStats();
});
// ---- bookmarks ----
const bookmarks = [
  new THREE.Vector3(38, 32, 48),
  new THREE.Vector3(-32, 18, -36),
  new THREE.Vector3(10, 40, -42),
];
document.getElementById('btnBookmark1').addEventListener('click', () => {
  controls.target.set(0, 2, 0);
  camera.position.copy(bookmarks[0]);
  controls.update();
});
document.getElementById('btnBookmark2').addEventListener('click', () => {
  controls.target.set(0, 2, 0);
  camera.position.copy(bookmarks[1]);
  controls.update();
});
document.getElementById('btnBookmark3').addEventListener('click', () => {
  controls.target.set(0, 2, 0);
  camera.position.copy(bookmarks[2]);
  controls.update();
});
// ---- autorotate toggle ----
const btnAuto = document.getElementById('btnAutorotate');
btnAuto.addEventListener('click', () => {
  controls.autoRotate = !controls.autoRotate;
  btnAuto.classList.toggle('active');
  btnAuto.textContent = controls.autoRotate ? 'Orbit' : 'Free';
});
// ---- resize ----
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
// ---- animate ----
function animate() {
  requestAnimationFrame(animate);
  // animate particles: gentle floating
  if (particleSystem && particleSystem.geometry.attributes.position) {
    const pos = particleSystem.geometry.attributes.position.array;
    const time = clock.getElapsedTime();
    const scale = 16;
    for (let i = 0; i < pos.length; i += 3) {
      // gentle vertical bob
      const ox = Math.sin(time * 0.3 + i * 0.01) * 0.04;
      const oy = Math.sin(time * 0.5 + i * 0.02) * 0.06;
      const oz = Math.cos(time * 0.4 + i * 0.015) * 0.04;
      // drift along terrain
      const ix = Math.floor(((pos[i] + scale/2) / scale) * (GRID-1));
      const iz = Math.floor(((pos[i+2] + scale/2) / scale) * (GRID-1));
      const clampedIx = Math.max(0, Math.min(GRID-1, ix));
      const clampedIz = Math.max(0, Math.min(GRID-1, iz));
      const dataIdx = clampedIz * GRID + clampedIx;
      if (terrainData && terrainData[dataIdx]) {
        const targetY = terrainData[dataIdx].height * 5 + 0.8;
        pos[i+1] += (targetY + oy - pos[i+1]) * 0.005;
      }
      pos[i] += ox * 0.01;
      pos[i+2] += oz * 0.01;
    }
    particleSystem.geometry.attributes.position.needsUpdate = true;
  }
  controls.update();
  renderer.render(scene, camera);
}
animate();
// ---- auto-rotate rivers glow pulse -----
let pulseTime = 0;
setInterval(() => {
  pulseTime += 0.05;
  const intensity = 0.2 + 0.2 * Math.sin(pulseTime);
  riverGroup.children.forEach(m => {
    if (m.material) {
      m.material.emissiveIntensity = intensity;
    }
  });
}, 50);
console.log('3D Data Terrain Explorer ready');
console.log('grid:', GRID, 'x', GRID, 'timesteps:', TIMESTEPS);
</script>
</body>
</html>