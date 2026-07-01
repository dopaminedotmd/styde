<div style="background:#1a1a2e;color:#e0e0e0;font-family:system-ui;padding:20px;min-height:100vh">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
    <h2 style="margin:0">Adaptive Metric Dashboard</h2>
    <div>
      <button id="resetBtn" style="background:#e94560;color:#fff;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;margin-right:8px">Reset All Data</button>
      <button id="exportBtn" style="background:#0f3460;color:#fff;border:none;padding:8px 16px;border-radius:6px;cursor:pointer">Export Tracking Data</button>
    </div>
  </div>
  <div id="statusBar" style="font-size:12px;color:#888;margin-bottom:12px">Tracking active — idle</div>
  <div id="grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;grid-auto-rows:minmax(140px,auto)"></div>
  <div id="moreSection" style="margin-top:16px">
    <details id="moreDetails"><summary style="cursor:pointer;color:#aaa;font-size:13px">More panels (<span id="moreCount">0</span>)</summary>
      <div id="moreGrid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px;grid-auto-rows:minmax(80px,auto)"></div>
    </details>
  </div>
</div>
<script>
(function(){
  const STORAGE_KEY = 'adaptive_layout_v1';
  const TRACK_INTERVAL = 500;
  const LAYOUT_RECALC_MS = 5000;
  const COMPACT_THRESHOLD = 0.15;
  const MINIATURE_THRESHOLD = 0.05;
  const RECENCY_HALFLIFE = 1000 * 60 * 30;
  const defaultPanels = [
    {id:'cpu',title:'CPU Usage',content:'<div style="height:80px;background:linear-gradient(135deg,#0f3460,#16213e);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">42%</div>'},
    {id:'memory',title:'Memory',content:'<div style="height:80px;background:linear-gradient(135deg,#16213e,#1a1a2e);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">7.2 GB</div>'},
    {id:'requests',title:'Requests/s',content:'<div style="height:80px;background:linear-gradient(135deg,#0f3460,#533483);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">1.2k</div>'},
    {id:'errors',title:'Error Rate',content:'<div style="height:80px;background:linear-gradient(135deg,#e94560,#533483);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">0.3%</div>'},
    {id:'latency',title:'P99 Latency',content:'<div style="height:80px;background:linear-gradient(135deg,#16213e,#0f3460);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">42ms</div>'},
    {id:'disk',title:'Disk I/O',content:'<div style="height:80px;background:linear-gradient(135deg,#1a1a2e,#16213e);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">320 MB/s</div>'},
    {id:'users',title:'Active Users',content:'<div style="height:80px;background:linear-gradient(135deg,#533483,#0f3460);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">847</div>'},
    {id:'uptime',title:'Uptime',content:'<div style="height:80px;background:linear-gradient(135deg,#0f3460,#e94560);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold">99.9%</div>'}
  ];
  let tracking = {};
  let locks = {};
  let manualPositions = {};
  let viewStartTimes = {};
  let rAFId = null;
  let frameCount = 0;
  let lastLayoutRecalc = 0;
  const FRAME_SKIP_LAYOUT = Math.floor(LAYOUT_RECALC_MS / 16.67);
  const FRAME_SKIP_TRACK = Math.floor(TRACK_INTERVAL / 16.67);
  function loadState(){
    try{
      const raw = localStorage.getItem(STORAGE_KEY);
      if(raw){
        const data = JSON.parse(raw);
        tracking = data.tracking || {};
        locks = data.locks || {};
        manualPositions = data.manualPositions || {};
      }
    }catch(e){}
    defaultPanels.forEach(p => {
      if(!tracking[p.id]) tracking[p.id] = {duration:0,interactions:0,lastInteraction:0};
      if(!(p.id in locks)) locks[p.id] = false;
    });
  }
  function saveState(){
    localStorage.setItem(STORAGE_KEY, JSON.stringify({tracking,locks,manualPositions}));
  }
  function computeScore(panelId, now){
    const t = tracking[panelId] || {duration:0,interactions:0,lastInteraction:0};
    const freq = Math.min(t.interactions, 100) / 100;
    const dur = Math.min(t.duration / (1000 * 60 * 5), 1);
    const age = now - t.lastInteraction;
    const recency = t.lastInteraction ? Math.exp(-age / RECENCY_HALFLIFE) : 0.01;
    return freq * 0.35 + dur * 0.35 + recency * 0.30;
  }
  function reconcile(now){
    const scored = defaultPanels.map(p => ({
      ...p,
      score: computeScore(p.id, now),
      locked: !!locks[p.id],
      manualPos: manualPositions[p.id] || null
    }));
    const locked = scored.filter(p => p.locked);
    const unlocked = scored.filter(p => !p.locked);
    locked.sort((a,b) => b.score - a.score);
    unlocked.sort((a,b) => b.score - a.score);
    const all = [...locked, ...unlocked];
    const diff = {toLarge:[],toMedium:[],toCompact:[],toMiniature:[],order:[]};
    const maxScore = all.length ? Math.max(...all.map(p=>p.score)) : 1;
    all.forEach((p,i) => {
      const norm = maxScore > 0 ? p.score / maxScore : 0;
      let size;
      if(norm >= 0.6) size = 'large';
      else if(norm >= COMPACT_THRESHOLD) size = 'medium';
      else if(norm >= MINIATURE_THRESHOLD) size = 'compact';
      else size = 'miniature';
      diff[`to${size.charAt(0).toUpperCase()+size.slice(1)}`].push(p.id);
      diff.order.push({id:p.id,size,locked:p.locked});
    });
    return diff;
  }
  function applyDiff(diff){
    const grid = document.getElementById('grid');
    const moreGrid = document.getElementById('moreGrid');
    const moreCount = document.getElementById('moreCount');
    grid.innerHTML = '';
    moreGrid.innerHTML = '';
    let moreItems = [];
    diff.order.forEach((item,i) => {
      const panel = defaultPanels.find(p=>p.id===item.id);
      if(!panel) return;
      const card = createCard(panel, item.size, item.locked);
      if(item.size === 'miniature'){
        moreItems.push(card);
      } else {
        grid.appendChild(card);
      }
    });
    moreItems.forEach(c => moreGrid.appendChild(c));
    moreCount.textContent = moreItems.length;
    const details = document.getElementById('moreDetails');
    if(moreItems.length === 0) details.open = false;
  }
  function createCard(panel, size, locked){
    const div = document.createElement('div');
    div.className = `size-${size}`;
    div.setAttribute('data-panel-id', panel.id);
    div.style.cssText = `
      background:#16213e;border-radius:10px;padding:12px;
      border:1px solid ${locked?'#e94560':'#0f3460'};
      transition:all 0.3s ease;position:relative;overflow:hidden;
      cursor:pointer;min-height:${size==='large'?'180px':size==='medium'?'140px':size==='compact'?'100px':'60px'};
    `;
    if(size === 'large') div.style.gridColumn = 'span 2';
    if(size === 'large') div.style.gridRow = 'span 2';
    const header = document.createElement('div');
    header.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:6px';
    const title = document.createElement('span');
    title.style.cssText = 'font-size:12px;color:#aaa;text-transform:uppercase;letter-spacing:1px';
    title.textContent = panel.title;
    header.appendChild(title);
    const controls = document.createElement('div');
    controls.style.cssText = 'display:flex;gap:4px';
    const lockBtn = document.createElement('button');
    lockBtn.textContent = locked ? '🔒' : '🔓';
    lockBtn.title = locked ? 'Unlock panel' : 'Lock panel position';
    lockBtn.style.cssText = 'background:transparent;border:none;cursor:pointer;font-size:14px;padding:2px 4px;opacity:0.7';
    lockBtn.onclick = function(e){ e.stopPropagation(); toggleLock(panel.id); };
    controls.appendChild(lockBtn);
    header.appendChild(controls);
    div.appendChild(header);
    const body = document.createElement('div');
    body.innerHTML = panel.content;
    if(size === 'compact'){
      body.style.cssText = 'transform:scale(0.75);transform-origin:top left;opacity:0.7';
    }
    div.appendChild(body);
    if(size === 'miniature'){
      div.style.cssText += 'font-size:11px;padding:8px';
      body.style.cssText = 'transform:scale(0.5);transform-origin:top left;opacity:0.5;pointer-events:none';
    }
    const score = computeScore(panel.id, Date.now());
    const indicator = document.createElement('div');
    indicator.style.cssText = `position:absolute;bottom:4px;right:8px;font-size:10px;color:#666`;
    indicator.textContent = `score:${(score*100).toFixed(0)}`;
    div.appendChild(indicator);
    div.addEventListener('mouseenter', function(){ startView(panel.id); });
    div.addEventListener('mouseleave', function(){ endView(panel.id); });
    div.addEventListener('click', function(e){
      if(e.target.tagName === 'BUTTON') return;
      recordInteraction(panel.id);
    });
    return div;
  }
  function startView(id){ viewStartTimes[id] = performance.now(); }
  function endView(id){
    if(!viewStartTimes[id]) return;
    const elapsed = performance.now() - viewStartTimes[id];
    if(!tracking[id]) tracking[id] = {duration:0,interactions:0,lastInteraction:0};
    tracking[id].duration += elapsed;
    tracking[id].lastInteraction = Date.now();
    delete viewStartTimes[id];
    saveState();
  }
  function recordInteraction(id){
    if(!tracking[id]) tracking[id] = {duration:0,interactions:0,lastInteraction:0};
    tracking[id].interactions++;
    tracking[id].lastInteraction = Date.now();
    saveState();
    updateStatus(`Interaction: ${id} (total: ${tracking[id].interactions})`);
  }
  function toggleLock(id){
    locks[id] = !locks[id];
    if(!locks[id]) delete manualPositions[id];
    saveState();
    const now = Date.now();
    const diff = reconcile(now);
    applyDiff(diff);
    updateStatus(`${id} ${locks[id]?'locked':'unlocked'}`);
  }
  function updateStatus(msg){
    document.getElementById('statusBar').textContent = `Tracking active — ${msg}`;
  }
  function mainLoop(timestamp){
    rAFId = requestAnimationFrame(mainLoop);
    frameCount++;
    if(frameCount % FRAME_SKIP_TRACK === 0){
      for(const id in viewStartTimes){
        const elapsed = performance.now() - viewStartTimes[id];
        if(!tracking[id]) tracking[id] = {duration:0,interactions:0,lastInteraction:0};
        tracking[id].duration += TRACK_INTERVAL;
        tracking[id].lastInteraction = Date.now();
        viewStartTimes[id] = performance.now();
      }
      saveState();
    }
    if(frameCount % FRAME_SKIP_LAYOUT === 0){
      const diff = reconcile(Date.now());
      applyDiff(diff);
    }
  }
  document.getElementById('resetBtn').onclick = function(){
    tracking = {};
    locks = {};
    manualPositions = {};
    viewStartTimes = {};
    defaultPanels.forEach(p => {
      tracking[p.id] = {duration:0,interactions:0,lastInteraction:0};
      locks[p.id] = false;
    });
    saveState();
    applyDiff(reconcile(Date.now()));
    updateStatus('All data reset');
  };
  document.getElementById('exportBtn').onclick = function(){
    const data = {tracking,locks,manualPositions,exportedAt:new Date().toISOString()};
    const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'adaptive-layout-data.json'; a.click();
    URL.revokeObjectURL(url);
    updateStatus('Data exported');
  };
  window.addEventListener('beforeunload', function(){
    for(const id in viewStartTimes) endView(id);
    saveState();
  });
  loadState();
  rAFId = requestAnimationFrame(mainLoop);
  applyDiff(reconcile(Date.now()));
  updateStatus('Initialized — hover panels to train layout');
})();
</script>