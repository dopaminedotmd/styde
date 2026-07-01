<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptive Metric Layout</title>
<style>
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --muted: #8b949e;
  --accent: #58a6ff;
  --danger: #f85149;
  --success: #3fb950;
  --warning: #d2991d;
  --panel-high: 1fr;
  --panel-mid: 1fr;
  --panel-low: 80px;
  --gap: 10px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  padding: 12px;
}
.toolbar {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 8px 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.toolbar button {
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 14px;
  cursor: pointer;
  font-size: 13px;
  transition: background 0.15s;
}
.toolbar button:hover { background: #1c2533; }
.toolbar button.active { background: var(--accent); color: #000; border-color: var(--accent); }
.toolbar .spacer { flex: 1; }
.toolbar .score-display { font-size: 12px; color: var(--muted); }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--gap);
  transition: grid-template-columns 0.3s ease;
}
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  position: relative;
  transition: all 0.35s ease;
  min-height: 120px;
  overflow: hidden;
}
.panel.high-rank {
  grid-column: span 2;
  grid-row: span 2;
  min-height: 260px;
  border-color: var(--accent);
  box-shadow: 0 0 0 1px var(--accent);
}
.panel.compact {
  min-height: 60px;
  padding: 10px 14px;
  font-size: 12px;
  opacity: 0.7;
}
.panel.compact .panel-body { display: none; }
.panel.compact .panel-preview { display: block; }
.panel.locked { border-color: var(--warning); box-shadow: 0 0 0 1px var(--warning); }
.panel.locked::after {
  content: "LOCKED";
  position: absolute;
  top: 6px;
  right: 6px;
  font-size: 9px;
  color: var(--warning);
  letter-spacing: 1px;
  font-weight: 700;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  cursor: grab;
}
.panel-header:active { cursor: grabbing; }
.panel-header h3 { font-size: 15px; font-weight: 600; color: var(--text); }
.panel-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}
.panel-actions button {
  background: none;
  border: none;
  color: var(--muted);
  cursor: pointer;
  font-size: 16px;
  padding: 2px 6px;
  border-radius: 4px;
  line-height: 1;
  transition: color 0.15s, background 0.15s;
}
.panel-actions button:hover { color: var(--text); background: #1c2533; }
.panel-actions button.lock-btn.locked { color: var(--warning); }
.panel-preview { display: none; font-size: 11px; color: var(--muted); }
.metric-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  font-size: 13px;
  border-bottom: 1px solid var(--border);
}
.metric-row:last-child { border-bottom: none; }
.metric-label { color: var(--muted); }
.metric-value { font-weight: 600; }
.metric-value.up { color: var(--success); }
.metric-value.down { color: var(--danger); }
.chart-placeholder {
  width: 100%;
  height: 100px;
  background: linear-gradient(135deg, #1a2332 0%, #0d1117 100%);
  border-radius: 6px;
  display: flex;
  align-items: flex-end;
  padding: 6px;
  gap: 3px;
  margin-top: 8px;
}
.chart-bar {
  flex: 1;
  background: var(--accent);
  border-radius: 3px 3px 0 0;
  transition: height 0.4s ease;
  min-width: 4px;
}
.chart-bar:nth-child(odd) { opacity: 0.7; }
.score-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  font-size: 9px;
  background: #1c2533;
  padding: 2px 6px;
  border-radius: 10px;
  color: var(--muted);
}
.locked .score-badge { display: none; }
.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 13px;
  z-index: 1000;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
</style>
</head>
<body>
<div class="toolbar">
  <button onclick="toggleAutoArrange()" id="btnAuto" class="active">Auto-Arrange: ON</button>
  <button onclick="resetAllScores()">Reset Scores</button>
  <button onclick="exportData()">Export Data</button>
  <button onclick="resetLayout()">Reset Layout</button>
  <span class="spacer"></span>
  <span class="score-display" id="scoreDisplay">Tracking active</span>
</div>
<div class="grid" id="dashboardGrid"></div>
<div class="toast" id="toast"></div>
<script>
"use strict";
const STORAGE_KEY_SCORES = "adaptive_layout_scores";
const STORAGE_KEY_LOCKS = "adaptive_layout_locks";
const STORAGE_KEY_ORDER = "adaptive_layout_order";
const DECAY_HALF_LIFE_MS = 24 * 60 * 60 * 1000;
const COMPACT_THRESHOLD_PERCENTILE = 30;
const TOAST_TIMEOUT = 2000;
let panels = [];
let scores = {};
let locks = {};
let manualOrder = null;
let autoArrange = true;
let observer = null;
let visibilityTimers = {};
let toastTimer = null;
function safeGet(key, fallback) {
  try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; }
  catch(e) { console.warn("localStorage read failed:", e.message); return fallback; }
}
function safeSet(key, value) {
  try { localStorage.setItem(key, JSON.stringify(value)); return true; }
  catch(e) { console.warn("localStorage write failed:", e.message); return false; }
}
function now() { return Date.now(); }
function computeRecencyWeight(lastInteraction, nowMs) {
  if (!lastInteraction) return 0.1;
  const elapsed = nowMs - lastInteraction;
  if (elapsed <= 0) return 1.0;
  return Math.pow(0.5, elapsed / DECAY_HALF_LIFE_MS);
}
function computeScore(panelId, nowMs) {
  const s = scores[panelId] || { frequency: 0, totalDuration: 0, lastInteraction: null, interactions: [] };
  const recencyWeight = computeRecencyWeight(s.lastInteraction, nowMs);
  const freqScore = Math.log2(s.frequency + 1);
  const durScore = Math.log2(s.totalDuration / 1000 + 1);
  const composite = freqScore * durScore * recencyWeight;
  return Math.round(composite * 100) / 100;
}
function recordInteraction(panelId, eventType) {
  const s = scores[panelId] || { frequency: 0, totalDuration: 0, lastInteraction: null, interactions: [] };
  s.frequency = (s.frequency || 0) + 1;
  s.lastInteraction = now();
  s.interactions = s.interactions || [];
  s.interactions.push({ type: eventType, time: now() });
  if (s.interactions.length > 200) s.interactions = s.interactions.slice(-200);
  scores[panelId] = s;
  schedulePersist();
  refreshLayout();
}
function recordDuration(panelId, ms) {
  const s = scores[panelId] || { frequency: 0, totalDuration: 0, lastInteraction: null, interactions: [] };
  s.totalDuration = (s.totalDuration || 0) + ms;
  scores[panelId] = s;
  schedulePersist();
}
let persistTimeout = null;
function schedulePersist() {
  if (persistTimeout) clearTimeout(persistTimeout);
  persistTimeout = setTimeout(() => {
    safeSet(STORAGE_KEY_SCORES, scores);
    safeSet(STORAGE_KEY_LOCKS, locks);
  }, 500);
}
function getScoreRankings() {
  const n = now();
  const ranked = Object.keys(scores).map(id => ({
    id,
    score: computeScore(id, n),
    frequency: scores[id].frequency || 0,
    duration: scores[id].totalDuration || 0,
    lastInteraction: scores[id].lastInteraction || 0
  }));
  ranked.sort((a, b) => b.score - a.score);
  return ranked;
}
function shouldCompact(panelId) {
  if (locks[panelId]) return false;
  if (autoArrange === false) return false;
  const ranked = getScoreRankings();
  if (ranked.length < 3) return false;
  const idx = ranked.findIndex(r => r.id === panelId);
  if (idx === -1) return false;
  const percentile = (idx / ranked.length) * 100;
  return percentile >= COMPACT_THRESHOLD_PERCENTILE;
}
function isHighRank(panelId) {
  if (locks[panelId]) return false;
  if (autoArrange === false) return false;
  const ranked = getScoreRankings();
  const idx = ranked.findIndex(r => r.id === panelId);
  return idx < Math.ceil(ranked.length * 0.25) && idx < 3;
}
function getOrderedPanelIds() {
  if (!autoArrange && manualOrder) return manualOrder;
  const ranked = getScoreRankings();
  return ranked.map(r => r.id);
}
function createPanelElement(panel, orderedIds) {
  const idx = orderedIds.indexOf(panel.id);
  const compact = shouldCompact(panel.id);
  const high = isHighRank(panel.id);
  const locked = !!locks[panel.id];
  const s = scores[panel.id] || { frequency: 0, totalDuration: 0 };
  const scoreVal = computeScore(panel.id, now());
  const el = document.createElement("div");
  el.className = "panel";
  if (high) el.classList.add("high-rank");
  if (compact) el.classList.add("compact");
  if (locked) el.classList.add("locked");
  el.setAttribute("data-panel-id", panel.id);
  el.setAttribute("data-order", String(idx));
  el.innerHTML =
    '<div class="score-badge">Score: ' + scoreVal.toFixed(1) + '</div>' +
    '<div class="panel-header" data-panel-id="' + panel.id + '">' +
      '<h3>' + escapeHtml(panel.title) + '</h3>' +
      '<div class="panel-actions">' +
        '<button class="lock-btn' + (locked ? ' locked' : '') + '" data-action="lock" data-panel-id="' + panel.id + '" title="' + (locked ? 'Unlock' : 'Lock') + ' position">' + (locked ? '&#128274;' : '&#128275;') + '</button>' +
        '<button data-action="collapse" data-panel-id="' + panel.id + '" title="Toggle compact">&#9660;</button>' +
        '<button data-action="close" data-panel-id="' + panel.id + '" title="Close panel">&#10005;</button>' +
      '</div>' +
    '</div>' +
    '<div class="panel-preview">Views: ' + s.frequency + ' | Time: ' + Math.round(s.totalDuration / 1000) + 's | Compact mode</div>' +
    '<div class="panel-body">' +
      renderPanelContent(panel) +
    '</div>';
  el.addEventListener("click", function(e) {
    const target = e.target;
    const btn = target.closest("button");
    if (btn) {
      const action = btn.getAttribute("data-action");
      const pid = btn.getAttribute("data-panel-id");
      if (action === "lock") { toggleLock(pid); e.stopPropagation(); return; }
      if (action === "collapse") { toggleCompactManual(pid); e.stopPropagation(); return; }
      if (action === "close") { removePanel(pid); e.stopPropagation(); return; }
    }
    recordInteraction(panel.id, "click");
  });
  el.addEventListener("mouseenter", function() {
    recordInteraction(panel.id, "hover");
  });
  el.addEventListener("dblclick", function() {
    toggleCompactManual(panel.id);
  });
  return el;
}
function renderPanelContent(panel) {
  let html = "";
  if (panel.type === "metrics" && panel.metrics) {
    for (const m of panel.metrics) {
      const valClass = m.trend === "up" ? "up" : m.trend === "down" ? "down" : "";
      html += '<div class="metric-row"><span class="metric-label">' + escapeHtml(m.label) + '</span><span class="metric-value ' + valClass + '">' + escapeHtml(String(m.value)) + '</span></div>';
    }
  }
  if (panel.type === "chart" || (panel.type === "metrics" && panel.metrics && panel.metrics.length > 2)) {
    html += '<div class="chart-placeholder">';
    const bars = panel.chartData || [40, 65, 45, 80, 55, 70, 60, 85, 50, 75, 65, 90];
    for (let i = 0; i < Math.min(bars.length, 20); i++) {
      const h = Math.max(8, Math.min(100, bars[i]));
      html += '<div class="chart-bar" style="height:' + h + '%"></div>';
    }
    html += '</div>';
  }
  if (panel.type === "text" && panel.content) {
    html += '<div style="font-size:13px;color:var(--muted);line-height:1.5">' + escapeHtml(panel.content) + '</div>';
  }
  return html;
}
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
function toggleLock(panelId) {
  locks[panelId] = !locks[panelId];
  safeSet(STORAGE_KEY_LOCKS, locks);
  showToast(locks[panelId] ? "Panel locked" : "Panel unlocked");
  refreshLayout();
}
function toggleCompactManual(panelId) {
  locks[panelId] = !locks[panelId];
  if (locks[panelId]) {
    safeSet(STORAGE_KEY_LOCKS, locks);
    showToast("Panel locked (manual toggle)");
  } else {
    delete locks[panelId];
    safeSet(STORAGE_KEY_LOCKS, locks);
    showToast("Panel unlocked");
  }
  refreshLayout();
}
function removePanel(panelId) {
  panels = panels.filter(p => p.id !== panelId);
  delete scores[panelId];
  delete locks[panelId];
  safeSet(STORAGE_KEY_SCORES, scores);
  safeSet(STORAGE_KEY_LOCKS, locks);
  showToast("Panel removed");
  refreshLayout();
}
function toggleAutoArrange() {
  autoArrange = !autoArrange;
  const btn = document.getElementById("btnAuto");
  if (autoArrange) {
    btn.textContent = "Auto-Arrange: ON";
    btn.classList.add("active");
    manualOrder = null;
    safeSet(STORAGE_KEY_ORDER, null);
    showToast("Auto-arrange enabled");
  } else {
    btn.textContent = "Auto-Arrange: OFF";
    btn.classList.remove("active");
    const ordered = getOrderedPanelIds();
    manualOrder = [...ordered];
    safeSet(STORAGE_KEY_ORDER, manualOrder);
    showToast("Manual order preserved");
  }
  refreshLayout();
}
function resetAllScores() {
  scores = {};
  safeSet(STORAGE_KEY_SCORES, scores);
  showToast("All scores reset");
  refreshLayout();
}
function resetLayout() {
  scores = {};
  locks = {};
  manualOrder = null;
  autoArrange = true;
  const btn = document.getElementById("btnAuto");
  btn.textContent = "Auto-Arrange: ON";
  btn.classList.add("active");
  safeSet(STORAGE_KEY_SCORES, scores);
  safeSet(STORAGE_KEY_LOCKS, locks);
  safeSet(STORAGE_KEY_ORDER, null);
  showToast("Layout reset complete");
  refreshLayout();
}
function exportData() {
  const data = { scores, locks, manualOrder, autoArrange, exportedAt: new Date().toISOString() };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "adaptive-layout-" + new Date().toISOString().replace(/:/g, "-") + ".json";
  a.click();
  URL.revokeObjectURL(url);
  showToast("Data exported");
}
function showToast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.classList.add("show");
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(function() { el.classList.remove("show"); }, TOAST_TIMEOUT);
}
function checkBoundingBox(el) {
  try {
    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) return false;
    if (rect.right < 0 || rect.bottom < 0) return false;
    if (rect.left > window.innerWidth || rect.top > window.innerHeight) return false;
    return true;
  } catch(e) {
    return false;
  }
}
function refreshLayout() {
  const grid = document.getElementById("dashboardGrid");
  const orderedIds = getOrderedPanelIds();
  const existingEls = grid.querySelectorAll(".panel");
  const existingMap = {};
  existingEls.forEach(function(el) {
    existingMap[el.getAttribute("data-panel-id")] = el;
  });
  grid.innerHTML = "";
  const orderedPanels = [];
  const seenIds = new Set();
  for (const id of orderedIds) {
    if (seenIds.has(id)) continue;
    seenIds.add(id);
    const panel = panels.find(function(p) { return p.id === id; });
    if (panel) orderedPanels.push(panel);
  }
  for (const panel of panels) {
    if (!seenIds.has(panel.id)) {
      orderedPanels.push(panel);
      seenIds.add(panel.id);
    }
  }
  for (let i = 0; i < orderedPanels.length; i++) {
    const panel = orderedPanels[i];
    const el = createPanelElement(panel, orderedPanels.map(function(p) { return p.id; }));
    el.style.order = String(i);
    grid.appendChild(el);
    requestAnimationFrame(function() {
      if (!checkBoundingBox(el)) {
        console.warn("Panel " + panel.id + " has invalid bounding box after render");
        el.style.minHeight = "60px";
        el.style.opacity = "0.6";
      }
    });
  }
  updateScoreDisplay();
}
function updateScoreDisplay() {
  const display = document.getElementById("scoreDisplay");
  const ranked = getScoreRankings();
  if (ranked.length === 0) {
    display.textContent = "No panels tracked";
    return;
  }
  const top = ranked.slice(0, 3).map(function(r) {
    const p = panels.find(function(pp) { return pp.id === r.id; });
    return (p ? p.title : r.id) + ":" + r.score.toFixed(1);
  }).join(" ");
  display.textContent = "Top: " + top;
}
function setupVisibilityTracking() {
  if (observer) observer.disconnect();
  observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      const panelId = entry.target.getAttribute("data-panel-id");
      if (!panelId) return;
      if (entry.isIntersecting && entry.intersectionRatio >= 0.3) {
        visibilityTimers[panelId] = now();
      } else if (visibilityTimers[panelId]) {
        const duration = now() - visibilityTimers[panelId];
        recordDuration(panelId, duration);
        delete visibilityTimers[panelId];
      }
    });
  }, { threshold: [0.3] });
  const panelEls = document.querySelectorAll(".panel");
  panelEls.forEach(function(el) { observer.observe(el); });
}
function flushVisibilityTimers() {
  const n = now();
  for (const panelId in visibilityTimers) {
    if (visibilityTimers.hasOwnProperty(panelId)) {
      recordDuration(panelId, n - visibilityTimers[panelId]);
      delete visibilityTimers[panelId];
    }
  }
}
function init() {
  scores = safeGet(STORAGE_KEY_SCORES, {});
  locks = safeGet(STORAGE_KEY_LOCKS, {});
  manualOrder = safeGet(STORAGE_KEY_ORDER, null);
  if (manualOrder) {
    autoArrange = false;
    const btn = document.getElementById("btnAuto");
    btn.textContent = "Auto-Arrange: OFF";
    btn.classList.remove("active");
  }
  panels = [
    { id: "revenue", title: "Revenue", type: "metrics", metrics: [
      { label: "MRR", value: "$128,400", trend: "up" },
      { label: "ARR", value: "$1.54M", trend: "up" },
      { label: "Churn", value: "2.1%", trend: "down" },
      { label: "LTV", value: "$4,200", trend: "up" }
    ], chartData: [30, 45, 35, 50, 40, 60, 55, 70, 65, 80, 75, 85] },
    { id: "users", title: "User Activity", type: "metrics", metrics: [
      { label: "DAU", value: "24,500", trend: "up" },
      { label: "WAU", value: "89,200", trend: "up" },
      { label: "New Signups", value: "1,240", trend: "up" },
      { label: "Bounce Rate", value: "32%", trend: "down" }
    ], chartData: [50, 55, 48, 60, 58, 65, 62, 70, 68, 75, 72, 80] },
    { id: "performance", title: "System Performance", type: "metrics", metrics: [
      { label: "P95 Latency", value: "145ms", trend: "down" },
      { label: "Error Rate", value: "0.12%", trend: "down" },
      { label: "Uptime", value: "99.97%", trend: "up" }
    ], chartData: [20, 25, 22, 28, 24, 30, 26, 32, 28, 35, 30, 38] },
    { id: "support", title: "Support Queue", type: "metrics", metrics: [
      { label: "Open Tickets", value: "42", trend: "down" },
      { label: "Avg Response", value: "2.3h", trend: "down" },
      { label: "CSAT", value: "94%", trend: "up" }
    ], chartData: [70, 65, 60, 55, 50, 45, 40, 38, 35, 32, 30, 28] },
    { id: "deployments", title: "Deployments", type: "metrics", metrics: [
      { label: "Today", value: "8", trend: "up" },
      { label: "This Week", value: "42", trend: "up" },
      { label: "Success Rate", value: "98.5%", trend: "up" }
    ], chartData: [60, 65, 58, 70, 62, 75, 68, 80, 72, 85, 78, 90] },
    { id: "alerts", title: "Alerts & Incidents", type: "metrics", metrics: [
      { label: "Active Alerts", value: "3", trend: "down" },
      { label: "MTTR", value: "18m", trend: "down" },
      { label: "False Pos.", value: "5%", trend: "down" }
    ], chartData: [10, 15, 12, 8, 5, 10, 7, 5, 8, 3, 6, 2] }
  ];
  refreshLayout();
  requestAnimationFrame(function() {
    setupVisibilityTracking();
  });
  window.addEventListener("beforeunload", function() {
    flushVisibilityTimers();
    safeSet(STORAGE_KEY_SCORES, scores);
    safeSet(STORAGE_KEY_LOCKS, locks);
    if (manualOrder) safeSet(STORAGE_KEY_ORDER, manualOrder);
  });
  document.addEventListener("visibilitychange", function() {
    if (document.hidden) {
      flushVisibilityTimers();
    }
  });
  setInterval(function() {
    flushVisibilityTimers();
    setupVisibilityTracking();
    updateScoreDisplay();
  }, 5000);
}
document.addEventListener("DOMContentLoaded", init);
</script>
</body>
</html>