```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Dashboard</title>
<style>
:root {
  --bg: #0f1117;
  --panel-bg: #1a1d28;
  --panel-border: #2a2d3a;
  --text: #e1e4ed;
  --text-dim: #8b8fa9;
  --accent: #6c8aff;
  --accent-glow: rgba(108,138,255,0.15);
  --compact-scale: 0.45;
  --gap: 10px;
  --radius: 8px;
}
* { box-sizing:border-box; margin:0; padding:0; }
body {
  font-family:'Inter',system-ui,-apple-system,sans-serif;
  background:var(--bg);
  color:var(--text);
  min-height:100vh;
  overflow-x:hidden;
}
.dashboard {
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:var(--gap);
  padding:16px;
  min-height:100vh;
  align-content:start;
}
.panel {
  background:var(--panel-bg);
  border:1px solid var(--panel-border);
  border-radius:var(--radius);
  transition:all 0.35s cubic-bezier(0.22,0.61,0.36,1);
  position:relative;
  overflow:hidden;
  cursor:grab;
  display:flex;
  flex-direction:column;
}
.panel.dragging { opacity:0.7; cursor:grabbing; z-index:100; box-shadow:0 8px 32px rgba(0,0,0,0.5); }
.panel.locked { border-color:var(--accent); box-shadow:0 0 0 1px var(--accent),0 0 16px var(--accent-glow); }
.panel.compact { transform:scale(var(--compact-scale)); transform-origin:top left; opacity:0.75; }
.panel.compact:hover { opacity:0.95; }
.panel-header {
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:10px 14px;
  border-bottom:1px solid var(--panel-border);
  background:rgba(255,255,255,0.02);
  user-select:none;
}
.panel-title { font-weight:600; font-size:0.9rem; letter-spacing:0.01em; }
.panel-controls { display:flex; gap:4px; }
.panel-controls button {
  background:none; border:none; color:var(--text-dim); cursor:pointer;
  width:24px; height:24px; border-radius:4px; font-size:0.75rem;
  display:flex; align-items:center; justify-content:center;
  transition:all 0.15s;
}
.panel-controls button:hover { background:rgba(255,255,255,0.08); color:var(--text); }
.panel-controls button.lock-btn.locked { color:var(--accent); }
.panel-body { padding:14px; flex:1; }
.panel-body.compact-view { display:none; }
.panel.compact .panel-body.full-view { display:none; }
.panel.compact .panel-body.compact-view { display:block; font-size:0.8rem; }
.metric-value { font-size:2rem; font-weight:700; line-height:1; }
.metric-label { font-size:0.75rem; color:var(--text-dim); margin-top:4px; }
.metric-spark { margin-top:8px; height:40px; }
.rank-badge {
  position:absolute; top:6px; right:6px; background:var(--accent);
  color:#fff; font-size:0.6rem; padding:2px 6px; border-radius:10px;
  opacity:0; transition:opacity 0.3s;
}
.panel:hover .rank-badge { opacity:1; }
.score-indicator {
  height:3px; background:var(--accent);
  position:absolute; bottom:0; left:0;
  border-radius:0 0 var(--radius) var(--radius);
  transition:width 0.5s;
}
.toolbar {
  display:flex; gap:8px; padding:12px 16px; flex-wrap:wrap;
  border-bottom:1px solid var(--panel-border);
  background:rgba(255,255,255,0.01);
}
.toolbar button {
  background:var(--panel-bg); color:var(--text); border:1px solid var(--panel-border);
  padding:6px 14px; border-radius:6px; cursor:pointer; font-size:0.8rem;
  transition:all 0.15s;
}
.toolbar button:hover { border-color:var(--accent); color:var(--accent); }
.toolbar button.active { background:var(--accent); color:#fff; border-color:var(--accent); }
.more-section { display:none; }
.more-section.visible { display:block; }
.more-toggle { text-align:center; padding:8px; color:var(--accent); cursor:pointer; font-size:0.8rem; }
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="engine.forceReRank()" title="Re-rank all panels based on current usage data">Re-rank Now</button>
  <button onclick="engine.resetAll()" title="Clear all tracking data and reset layout">Reset All Data</button>
  <button id="showMoreBtn" onclick="engine.toggleMore()" title="Show/hide compacted panels">More Panels</button>
  <span style="margin-left:auto;color:var(--text-dim);font-size:0.75rem;display:flex;align-items:center;">
    Drag to reorder | Lock to pin | Auto-adapts to usage
  </span>
</div>
<div class="dashboard" id="dashboard"></div>
<div class="more-section" id="moreSection">
  <div class="more-toggle" onclick="engine.toggleMore()">Show compact panels</div>
  <div class="dashboard" id="moreDashboard"></div>
</div>
<script>
(function() {
  const STORAGE_KEY = 'adaptive_dashboard_v1';
  const DEBOUNCE_MS = 300;
  const RERANK_COOLDOWN_MS = 2000;
  const DECAY_HALF_LIFE_HOURS = 24;
  const COMPACT_THRESHOLD = 0.25;
  const PANEL_DEFS = [
    { id:'revenue', title:'Revenue', metric:'$128,430', label:'+12.3% vs last month', color:'#6c8aff' },
    { id:'users', title:'Active Users', metric:'18,423', label:'+5.7% weekly growth', color:'#4ade80' },
    { id:'conversion', title:'Conversion Rate', metric:'3.82%', label:'+0.4pp improvement', color:'#f59e0b' },
    { id:'latency', title:'API Latency', metric:'42ms', label:'p95 | -8ms from last deploy', color:'#f87171' },
    { id:'errors', title:'Error Rate', metric:'0.12%', label:'Below 0.5% threshold', color:'#a78bfa' },
    { id:'bandwidth', title:'Bandwidth', metric:'2.4 TB', label:'Daily egress', color:'#38bdf8' },
    { id:'cpu', title:'CPU Utilization', metric:'67%', label:'Avg across 12 nodes', color:'#fb923c' },
    { id:'memory', title:'Memory', metric:'48.2 GB', label:'72% of allocated', color:'#e879f9' },
    { id:'sessions', title:'Sessions', metric:'94,201', label:'Today so far', color:'#2dd4bf' },
    { id:'churn', title:'Churn Rate', metric:'2.1%', label:'Monthly rolling', color:'#f87171' },
    { id:'nps', title:'NPS Score', metric:'72', label:'+4 points QoQ', color:'#4ade80' },
    { id:'storage', title:'Storage', metric:'8.7 TB', label:'41% capacity used', color:'#a78bfa' }
  ];
  function now() { return Date.now(); }
  function loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch(e) { return null; }
  }
  function saveState(state) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
  }
  function defaultState() {
    const panels = PANEL_DEFS.map((def, i) => ({
      id: def.id,
      order: i,
      locked: false,
      compact: false,
      views: 0,
      totalDuration: 0,
      lastViewed: 0,
      interactions: 0,
      collapsed: false
    }));
    return { panels, version: 1, lastRankAt: 0 };
  }
  function decayMultiplier(lastViewed, decayHours) {
    if (!lastViewed) return 0.5;
    const hoursSince = (now() - lastViewed) / (1000 * 60 * 60);
    return Math.pow(0.5, hoursSince / decayHours);
  }
  function computeScore(p) {
    const freq = p.views || 0;
    const dur = Math.min((p.totalDuration || 0) / 1000, 300);
    const decay = decayMultiplier(p.lastViewed, DECAY_HALF_LIFE_HOURS);
    const interactionBonus = 1 + Math.log1p(p.interactions || 0) * 0.2;
    return (freq * 0.35 + dur * 0.40 + (p.interactions || 0) * 0.25) * decay * interactionBonus;
  }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
  const Engine = {
    state: null,
    rankCache: null,
    rerankTimer: null,
    visibleTimers: {},
    debouncedSave: null,
    observer: null,
    init() {
      this.state = loadState() || defaultState();
      const storedIds = new Set(this.state.panels.map(p => p.id));
      PANEL_DEFS.forEach((def, i) => {
        if (!storedIds.has(def.id)) {
          this.state.panels.push({
            id: def.id, order: this.state.panels.length + i,
            locked: false, compact: false, views: 0, totalDuration: 0,
            lastViewed: 0, interactions: 0, collapsed: false
          });
        }
      });
      this.rankCache = null;
      this.debouncedSave = this._debounce(() => saveState(this.state), DEBOUNCE_MS);
      this.render();
      this._setupIntersectionObserver();
      this._scheduleAutoReRank();
    },
    _debounce(fn, ms) {
      let t;
      return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
    },
    _scheduleAutoReRank() {
      setInterval(() => {
        this.forceReRank();
      }, 30000);
    },
    _setupIntersectionObserver() {
      this.observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const id = entry.target.dataset.panelId;
          if (!id) return;
          if (entry.isIntersecting) {
            this.visibleTimers[id] = now();
          } else if (this.visibleTimers[id]) {
            const dur = now() - this.visibleTimers[id];
            const p = this.state.panels.find(p => p.id === id);
            if (p) { p.totalDuration += dur; this._markDirty(); }
            delete this.visibleTimers[id];
          }
        });
      }, { threshold: 0.3 });
    },
    _observePanel(el) {
      if (this.observer && el) this.observer.observe(el);
    },
    _markDirty() { this.rankCache = null; this.debouncedSave(); },
    getSorted() {
      if (this.rankCache) return this.rankCache;
      const scored = this.state.panels.map(p => ({
        ...p, score: computeScore(p), def: PANEL_DEFS.find(d => d.id === p.id)
      }));
      const maxScore = Math.max(...scored.map(s => s.score), 0.01);
      scored.forEach(s => { s.normScore = s.score / maxScore; });
      const locked = scored.filter(s => s.locked).sort((a,b) => a.order - b.order);
      const unlocked = scored.filter(s => !s.locked).sort((a,b) => b.score - a.score);
      const result = [...locked, ...unlocked];
      const threshold = maxScore * COMPACT_THRESHOLD;
      result.forEach(s => {
        if (!s.locked) s.compact = s.score < threshold && s.score > 0;
      });
      this.rankCache = result;
      return result;
    },
    forceReRank() {
      if (now() - (this.state.lastRankAt || 0) < RERANK_COOLDOWN_MS) return;
      this.state.lastRankAt = now();
      this.rankCache = null;
      const sorted = this.getSorted();
      sorted.forEach((s, i) => {
        if (!s.locked) {
          const p = this.state.panels.find(p => p.id === s.id);
          if (p) p.order = i;
        }
      });
      this._markDirty();
      this.render();
    },
    trackInteraction(panelId) {
      const p = this.state.panels.find(p => p.id === panelId);
      if (!p) return;
      p.interactions = (p.interactions || 0) + 1;
      p.lastViewed = now();
      this._markDirty();
      this._scheduleReRankDebounced();
    },
    trackView(panelId) {
      const p = this.state.panels.find(p => p.id === panelId);
      if (!p) return;
      p.views = (p.views || 0) + 1;
      p.lastViewed = now();
      this._markDirty();
    },
    _scheduleReRankDebounced() {
      clearTimeout(this.rerankTimer);
      this.rerankTimer = setTimeout(() => this.forceReRank(), 5000);
    },
    toggleLock(panelId) {
      const p = this.state.panels.find(p => p.id === panelId);
      if (!p) return;
      p.locked = !p.locked;
      if (p.locked) { p.order = this.state.panels.filter(pp => pp.locked).length; }
      this.rankCache = null;
      this._markDirty();
      this.render();
    },
    toggleCollapse(panelId) {
      const p = this.state.panels.find(p => p.id === panelId);
      if (!p) return;
      p.collapsed = !p.collapsed;
      this._markDirty();
      this.render();
    },
    movePanel(panelId, newOrder) {
      const p = this.state.panels.find(p => p.id === panelId);
      if (!p) return;
      p.order = clamp(newOrder, 0, this.state.panels.length - 1);
      p.locked = true;
      this.rankCache = null;
      this._markDirty();
      this.render();
    },
    toggleMore() {
      const sec = document.getElementById('moreSection');
      sec.classList.toggle('visible');
    },
    resetAll() {
      localStorage.removeItem(STORAGE_KEY);
      this.state = defaultState();
      this.rankCache = null;
      this.render();
    },
    _sparkPath(def) {
      const hue = parseInt(def.color.slice(1), 16) || 0x6c8aff;
      const r = (hue>>16)&0xff, g = (hue>>8)&0xff, b = hue&0xff;
      const pts = Array.from({length:12}, (_,i) => {
        const x = (i/11)*100;
        const y = 50 + Math.sin(i*0.9 + (PANEL_DEFS.indexOf(def)*0.7)) * 25 + (Math.random()-0.5)*15;
        return `${x},${y}`;
      });
      return `<svg width="100%" height="40" viewBox="0 0 100 40" preserveAspectRatio="none">
        <defs><linearGradient id="g${def.id}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="rgba(${r},${g},${b},0.4)"/>
          <stop offset="100%" stop-color="rgba(${r},${g},${b},0.02)"/>
        </linearGradient></defs>
        <polygon fill="url(#g${def.id})" points="0,40 ${pts.join(' ')} 100,40"/>
        <polyline fill="none" stroke="rgba(${r},${g},${b},0.8)" stroke-width="1.5"
          points="${pts.join(' ')}"/>
      </svg>`;
    },
    render() {
      const sorted = this.getSorted();
      const mainDash = document.getElementById('dashboard');
      const moreDash = document.getElementById('moreDashboard');
      const moreBtn = document.getElementById('showMoreBtn');
      const visiblePanels = sorted.filter(s => !s.compact);
      const compactPanels = sorted.filter(s => s.compact);
      mainDash.innerHTML = visiblePanels.map((s, i) => {
        const def = s.def || PANEL_DEFS.find(d => d.id === s.id);
        if (!def) return '';
        return `<div class="panel${s.locked ? ' locked' : ''}${s.compact ? ' compact' : ''}"
          data-panel-id="${s.id}" data-order="${i}" draggable="true"
          onmouseenter="engine.trackView('${s.id}')"
          onclick="engine.trackInteraction('${s.id}')">
          <span class="rank-badge">#${i+1}</span>
          <div class="panel-header">
            <span class="panel-title">${def.title}</span>
            <div class="panel-controls">
              <button class="lock-btn${s.locked ? ' locked' : ''}"
                onclick="event.stopPropagation();engine.toggleLock('${s.id}')"
                title="${s.locked ? 'Unlock' : 'Lock'}">${s.locked ? '🔒' : '🔓'}</button>
              <button onclick="event.stopPropagation();engine.toggleCollapse('${s.id}')"
                title="Collapse">${s.collapsed ? '▶' : '▼'}</button>
            </div>
          </div>
          ${s.collapsed ? '' : `
          <div class="panel-body full-view">
            <div class="metric-value" style="color:${def.color}">${def.metric}</div>
            <div class="metric-label">${def.label}</div>
            <div class="metric-spark">${this._sparkPath(def)}</div>
            <div style="margin-top:8px;font-size:0.7rem;color:var(--text-dim);">
              Score: ${s.normScore.toFixed(3)} | Views: ${s.views} | Int: ${s.interactions || 0}
            </div>
          </div>
          <div class="panel-body compact-view">
            <span style="color:${def.color};font-weight:600;">${def.metric}</span>
            <span style="margin-left:8px;color:var(--text-dim);font-size:0.7rem;">${def.title}</span>
          </div>`}
          <div class="score-indicator" style="width:${(s.normScore*100).toFixed(1)}%;background:${def.color};"></div>
        </div>`;
      }).join('');
      moreDash.innerHTML = compactPanels.map((s, i) => {
        const def = s.def || PANEL_DEFS.find(d => d.id === s.id);
        if (!def) return '';
        return `<div class="panel compact" data-panel-id="${s.id}" data-order="${i}"
          onmouseenter="engine.trackView('${s.id}')"
          onclick="engine.trackInteraction('${s.id}')">
          <div class="panel-header">
            <span class="panel-title">${def.title}</span>
            <div class="panel-controls">
              <button class="lock-btn" onclick="event.stopPropagation();engine.toggleLock('${s.id}')" title="Lock">🔓</button>
            </div>
          </div>
          <div class="panel-body compact-view">
            <span style="color:${def.color};font-weight:600;">${def.metric}</span>
          </div>
          <div class="score-indicator" style="width:${(s.normScore*100).toFixed(1)}%;background:${def.color};"></div>
        </div>`;
      }).join('');
      moreBtn.textContent = compactPanels.length > 0
        ? `More Panels (${compactPanels.length})`
        : 'More Panels';
      moreBtn.classList.toggle('active', compactPanels.length > 0);
      document.querySelectorAll('.panel').forEach(el => this._observePanel(el));
      this._setupDragDrop();
    },
    _setupDragDrop() {
      let dragSrc = null;
      const panels = document.querySelectorAll('.panel[draggable="true"]');
      panels.forEach(p => {
        p.addEventListener('dragstart', e => {
          dragSrc = p;
          p.classList.add('dragging');
          e.dataTransfer.effectAllowed = 'move';
          e.dataTransfer.setData('text/plain', p.dataset.panelId);
        });
        p.addEventListener('dragend', e => {
          p.classList.remove('dragging');
          dragSrc = null;
        });
        p.addEventListener('dragover', e => {
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';
        });
        p.addEventListener('drop', e => {
          e.preventDefault();
          if (!dragSrc || dragSrc === p) return;
          const srcId = dragSrc.dataset.panelId;
          const targetOrder = parseInt(p.dataset.order);
          engine.movePanel(srcId, targetOrder);
        });
      });
    }
  };
  window.engine = Engine;
  Engine.init();
})();
</script>
</body>
</html>
```