```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ops Center — Styde Forge</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
/*
 * DRY DESIGN SYSTEM — CSS CUSTOM PROPERTIES & UTILITY CLASSES
 * No repeated property blocks. Every visual token lives in :root.
 * All spacing, color, typography, and effects cascade from these vars.
 */
:root {
  --bg-deep: #07080b;
  --bg-panel: #0d0f14;
  --bg-card: #111318;
  --bg-hover: #181b24;
  --border-subtle: #1e2230;
  --border-mid: #2a2f42;
  --text-primary: #e4e7f0;
  --text-secondary: #8891a8;
  --text-muted: #556075;
  --amber: #f5a623;
  --amber-dim: #b87a1a;
  --cyan: #27d8b8;
  --cyan-dim: #1a9e87;
  --magenta: #d9469a;
  --magenta-dim: #9f2e71;
  --green: #3ad47a;
  --green-dim: #249e58;
  --red: #e55050;
  --red-dim: #b83636;
  --blue: #4a9eff;
  --blue-dim: #2d6fbe;
  --orange: #f0843a;
  --orange-dim: #b85f23;
  --glow-amber: 0 0 20px rgba(245,166,35,0.15);
  --glow-cyan: 0 0 20px rgba(39,216,184,0.12);
  --glow-magenta: 0 0 20px rgba(217,70,154,0.10);
  --font-mono: 'JetBrains Mono', monospace;
  --font-sans: 'Inter', -apple-system, sans-serif;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 20px;
  --space-2xl: 28px;
  --space-3xl: 36px;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --transition-fast: 150ms var(--ease-out);
  --transition-med: 250ms var(--ease-out);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 14px; }
body {
  background: var(--bg-deep);
  color: var(--text-primary);
  font-family: var(--font-sans);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-xl);
  line-height: 1.5;
}
/* ── UTILITY CLASSES ── */
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.gap-xs { gap: var(--space-xs); }
.gap-sm { gap: var(--space-sm); }
.gap-md { gap: var(--space-md); }
.gap-lg { gap: var(--space-lg); }
.gap-xl { gap: var(--space-xl); }
.gap-2xl { gap: var(--space-2xl); }
.text-xs { font-size: 10px; letter-spacing: 0.04em; }
.text-sm { font-size: 12px; }
.text-base { font-size: 14px; }
.text-lg { font-size: 18px; }
.text-xl { font-size: 24px; }
.text-2xl { font-size: 32px; }
.text-3xl { font-size: 42px; }
.mono { font-family: var(--font-mono); }
.semibold { font-weight: 600; }
.bold { font-weight: 700; }
.medium { font-weight: 500; }
.light { font-weight: 300; }
.text-secondary { color: var(--text-secondary); }
.text-muted { color: var(--text-muted); }
.text-amber { color: var(--amber); }
.text-cyan { color: var(--cyan); }
.text-green { color: var(--green); }
.text-red { color: var(--red); }
.text-magenta { color: var(--magenta); }
.text-blue { color: var(--blue); }
.text-orange { color: var(--orange); }
.truncate { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.w-full { width: 100%; }
.panel {
  background: var(--bg-panel);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
}
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  transition: border-color var(--transition-fast), background var(--transition-fast);
}
.card:hover { border-color: var(--border-mid); background: var(--bg-hover); }
.card-label { font-size: 10px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); font-family: var(--font-mono); margin-bottom: var(--space-xs); }
.card-value { font-family: var(--font-mono); font-weight: 700; letter-spacing: -0.02em; line-height: 1.2; }
.badge {
  display: inline-flex; align-items: center; gap: var(--space-xs);
  padding: 2px 8px; border-radius: 3px; font-size: 10px;
  font-family: var(--font-mono); font-weight: 500; letter-spacing: 0.03em;
}
.badge-ok { background: rgba(58,212,122,0.12); color: var(--green); border: 1px solid rgba(58,212,122,0.2); }
.badge-warn { background: rgba(245,166,35,0.12); color: var(--amber); border: 1px solid rgba(245,166,35,0.2); }
.badge-err { background: rgba(229,80,80,0.12); color: var(--red); border: 1px solid rgba(229,80,80,0.2); }
.badge-info { background: rgba(74,158,255,0.12); color: var(--blue); border: 1px solid rgba(74,158,255,0.2); }
.badge-cyan { background: rgba(39,216,184,0.12); color: var(--cyan); border: 1px solid rgba(39,216,184,0.2); }
.sparkline { display: flex; align-items: flex-end; gap: 2px; height: 32px; }
.sparkline-bar { width: 6px; border-radius: 1px; min-height: 2px; transition: height var(--transition-med); }
.header-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding-bottom: var(--space-lg); margin-bottom: var(--space-xl);
  border-bottom: 1px solid var(--border-subtle);
}
.header-title { font-size: 22px; font-weight: 700; letter-spacing: -0.03em; }
.header-sub { font-size: 12px; color: var(--text-muted); font-family: var(--font-mono); }
.grid-main {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr 1fr;
  gap: var(--space-xl);
  max-width: 1400px;
  width: 100%;
}
.grid-double { grid-column: 1 / -1; display: grid; grid-template-columns: 1.2fr 0.8fr 1fr; gap: var(--space-xl); }
.mini-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-md); }
.mini-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: var(--space-md); }
.radar-dot {
  width: 6px; height: 6px; border-radius: 50%;
  box-shadow: 0 0 6px currentColor; flex-shrink: 0;
}
.progress-bar { height: 4px; border-radius: 2px; background: var(--bg-hover); overflow: hidden; }
.progress-fill { height: 100%; border-radius: 2px; transition: width 600ms var(--ease-out); }
.stream-line {
  display: flex; align-items: center; gap: var(--space-sm);
  padding: var(--space-sm) 0;
  border-bottom: 1px solid rgba(30,34,48,0.5);
  font-size: 12px;
  font-family: var(--font-mono);
}
.stream-line:last-child { border-bottom: none; }
.stream-time { color: var(--text-muted); flex-shrink: 0; width: 50px; }
.stream-level { flex-shrink: 0; width: 44px; }
.service-row {
  display: flex; align-items: center; gap: var(--space-md);
  padding: var(--space-sm) 0;
  border-bottom: 1px solid rgba(30,34,48,0.4);
  font-size: 12px;
  font-family: var(--font-mono);
}
.service-row:last-child { border-bottom: none; }
.service-name { flex: 1; }
.service-uptime { width: 50px; text-align: right; }
@media (max-width: 1100px) {
  .grid-main { grid-template-columns: 1fr; }
  .grid-double { grid-template-columns: 1fr; }
  .mini-grid { grid-template-columns: 1fr 1fr; }
}
/* ── ANIMATIONS ── */
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.pulse { animation: pulse-dot 2s ease-in-out infinite; }
@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fade-in-up 400ms var(--ease-out) both; }
@keyframes scanline {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}
.scan-overlay {
  pointer-events: none; position: fixed; inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(255,255,255,0.015) 2px,
    rgba(255,255,255,0.015) 4px
  );
  z-index: 9999;
}
</style>
</head>
<body>
<div class="scan-overlay"></div>
<div class="grid-main fade-in" style="animation-delay:0ms">
  <!-- COL 1: KPI CORE + SPARKLINES -->
  <div class="flex flex-col gap-xl">
    <div class="panel fade-in" style="animation-delay:60ms">
      <div class="flex items-center justify-between" style="margin-bottom:var(--space-lg)">
        <div>
          <div class="card-label">Throughput</div>
          <div class="card-value text-3xl text-cyan" id="throughput-value">--</div>
        </div>
        <div class="card-value text-lg text-secondary" id="throughput-trend">
          <span class="text-green">+0.0</span>%
        </div>
      </div>
      <div class="sparkline" id="throughput-spark"></div>
    </div>
    <div class="panel fade-in" style="animation-delay:120ms">
      <div class="flex items-center justify-between" style="margin-bottom:var(--space-lg)">
        <div>
          <div class="card-label">Latency P99</div>
          <div class="card-value text-3xl text-amber" id="latency-value">--</div>
        </div>
        <div class="card-value text-lg text-secondary" id="latency-trend">
          <span class="text-green">-0.0</span>%
        </div>
      </div>
      <div class="sparkline" id="latency-spark"></div>
    </div>
    <div class="panel fade-in" style="animation-delay:180ms">
      <div class="flex items-center justify-between" style="margin-bottom:var(--space-lg)">
        <div>
          <div class="card-label">Error Rate</div>
          <div class="card-value text-3xl text-red" id="error-value">--</div>
        </div>
        <div class="card-value text-lg text-secondary" id="error-trend">
          <span class="text-green">-0.0</span>%
        </div>
      </div>
      <div class="sparkline" id="error-spark"></div>
    </div>
  </div>
  <!-- COL 2: SYSTEM HEALTH + SERVICES -->
  <div class="flex flex-col gap-xl">
    <div class="panel fade-in" style="animation-delay:100ms">
      <div class="flex items-center justify-between" style="margin-bottom:var(--space-md)">
        <div class="card-label">System Health</div>
        <span class="badge badge-ok pulse" id="health-badge">● ONLINE</span>
      </div>
      <div class="mini-grid-3" style="margin-bottom:var(--space-lg)">
        <div class="flex flex-col items-center">
          <div class="text-xs text-muted mono">CPU</div>
          <div class="card-value text-lg" id="cpu-val">--</div>
          <div class="progress-bar w-full" style="margin-top:var(--space-xs)"><div class="progress-fill" id="cpu-bar" style="width:0%;background:var(--cyan)"></div></div>
        </div>
        <div class="flex flex-col items-center">
          <div class="text-xs text-muted mono">RAM</div>
          <div class="card-value text-lg" id="ram-val">--</div>
          <div class="progress-bar w-full" style="margin-top:var(--space-xs)"><div class="progress-fill" id="ram-bar" style="width:0%;background:var(--magenta)"></div></div>
        </div>
        <div class="flex flex-col items-center">
          <div class="text-xs text-muted mono">DISK</div>
          <div class="card-value text-lg" id="disk-val">--</div>
          <div class="progress-bar w-full" style="margin-top:var(--space-xs)"><div class="progress-fill" id="disk-bar" style="width:0%;background:var(--amber)"></div></div>
        </div>
      </div>
      <div class="flex items-center justify-between text-xs text-muted mono">
        <span>Uptime: <span id="uptime-val">--</span></span>
        <span>Workers: <span id="workers-val">--</span></span>
        <span>Queue: <span id="queue-val">--</span></span>
      </div>
    </div>
    <div class="panel fade-in" style="animation-delay:160ms; flex:1">
      <div class="flex items-center justify-between" style="margin-bottom:var(--space-md)">
        <div class="card-label">Services</div>
        <span class="text-xs text-muted mono"><span id="svc-ok">0</span>/<span id="svc-total">0</span> up</span>
      </div>
      <div id="services-container"></div>
    </div>
  </div>
  <!-- COL 3: EVENT STREAM -->
  <div class="panel fade-in" style="animation-delay:140ms; overflow:hidden">
    <div class="flex items-center justify-between" style="margin-bottom:var(--space-md)">
      <div class="card-label">Event Stream</div>
      <div class="flex items-center gap-sm">
        <span class="radar-dot text-green pulse" style="background:var(--green)"></span>
        <span class="text-xs mono text-muted">LIVE</span>
      </div>
    </div>
    <div id="stream-container" style="max-height:460px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:var(--border-subtle) transparent"></div>
  </div>
</div>
<script>
/* ── DATA GENERATOR ── */
/* Generates dynamic semi-random data. No hardcoded sample entries. */
const gen = {
  rand: (min, max) => Math.floor(Math.random() * (max - min + 1)) + min,
  float: (min, max, d) => { const n = Math.random() * (max - min) + min; return Number(n.toFixed(d || 1)); },
  pick: (arr) => arr[gen.rand(0, arr.length - 1)],
  clamp: (v, lo, hi) => Math.max(lo, Math.min(hi, v)),
  trend: (prev, drift, min, max) => {
    const next = prev + gen.float(-drift, drift, 2);
    return gen.clamp(next, min, max);
  },
  sparkData: (points, min, max) => {
    const arr = [];
    for (let i = 0; i < points; i++) arr.push(gen.rand(min, max));
    return arr;
  },
  id: () => Math.random().toString(36).substring(2, 8)
};
/* ── STATE ── */
const state = {
  throughput: gen.rand(800, 1600),
  latency: gen.rand(12, 60),
  errorRate: gen.float(0.01, 0.8, 2),
  cpu: gen.rand(20, 85),
  ram: gen.rand(40, 92),
  disk: gen.rand(30, 78),
  services: [],
  events: [],
  eventId: 0
};
const THROUGHPUT_HISTORY = gen.sparkData(20, 400, 2000);
const LATENCY_HISTORY = gen.sparkData(20, 5, 120);
const ERROR_HISTORY = gen.sparkData(20, 0, 3);
/* ── SERVICE DEFINITIONS ── */
const SERVICE_NAMES = [
  'api-gateway', 'auth-service', 'cache-redis', 'postgres-primary',
  'postgres-replica', 'message-queue', 'search-index', 'cdn-origin',
  'worker-pool', 'monitoring', 'rate-limiter', 'session-store'
];
const LOG_LEVELS = ['INFO', 'WARN', 'ERROR', 'DEBUG'];
const LOG_MESSAGES = [
  'request processed in {n}ms', 'connection pool at {n}%',
  'cache hit ratio {n}', 'query completed ({n} rows)',
  'health check passed', 'retry attempt {n}',
  'backpressure detected', 'throttling rate at {n}/s',
  'replication lag {n}ms', 'memory pressure alert',
  'config reloaded successfully', 'session expired for user-{n}',
  'rate limit breached from {n}', 'connection reset by peer',
  'cold start detected ({n}ms)', 'batch job completed ({n} items)'
];
function buildEvent() {
  const level = levelWeighted();
  const ts = new Date();
  const time = ts.toISOString().substring(11, 23);
  const msg = gen.pick(LOG_MESSAGES).replace('{n}', gen.rand(1, 9999));
  const svc = gen.pick(SERVICE_NAMES);
  return { id: ++state.eventId, time, level, msg, svc };
}
function levelWeighted() {
  const r = Math.random();
  if (r < 0.70) return 'INFO';
  if (r < 0.85) return 'DEBUG';
  if (r < 0.95) return 'WARN';
  return 'ERROR';
}
function buildService(name) {
  const cpu = gen.rand(5, 95);
  const mem = gen.rand(20, 90);
  const uptime = gen.rand(1, 720);
  const status = cpu > 85 || mem > 85 ? 'warn' : (gen.rand(1, 25) === 1 ? 'err' : 'ok');
  const p99 = gen.rand(2, 450);
  return { name, cpu, mem, uptime, status, p99 };
}
const EVENTS_PRELOAD = 30;
for (let i = 0; i < EVENTS_PRELOAD; i++) state.events.push(buildEvent());
SERVICE_NAMES.forEach(n => state.services.push(buildService(n)));
/* ── RENDERERS ── */
function renderSparkline(el, data, color) {
  const max = Math.max(...data, 1);
  let html = '';
  for (const v of data) {
    const h = Math.max(2, Math.round((v / max) * 28));
    html += '<div class="sparkline-bar" style="height:' + h + 'px;background:' + color + '"></div>';
  }
  el.innerHTML = html;
}
function renderSparklineAnimated(el, data, color) {
  el.style.opacity = '0';
  renderSparkline(el, data, color);
  requestAnimationFrame(() => { el.style.transition = 'opacity 300ms'; el.style.opacity = '1'; });
}
function formatThroughput(v) { return v >= 1000 ? (v / 1000).toFixed(1) + 'k' : String(v); }
function formatLatency(v) { return v + 'ms'; }
function formatError(v) { return v < 0.1 ? v.toFixed(2) + '%' : v.toFixed(1) + '%'; }
function formatPct(v) { return v + '%'; }
function renderServices() {
  const container = document.getElementById('services-container');
  let ok = 0;
  let html = '';
  for (const s of state.services) {
    if (s.status === 'ok') ok++;
    const badgeCls = s.status === 'ok' ? 'badge-ok' : (s.status === 'warn' ? 'badge-warn' : 'badge-err');
    const badgeTxt = s.status === 'ok' ? 'UP' : (s.status === 'warn' ? 'DEG' : 'DOWN');
    html += '<div class="service-row">';
    html += '<span class="radar-dot ' + (s.status === 'ok' ? 'text-green' : (s.status === 'warn' ? 'text-amber' : 'text-red')) + '" style="background:currentColor"></span>';
    html += '<span class="service-name truncate">' + s.name + '</span>';
    html += '<span class="text-xs text-muted mono">' + s.p99 + 'ms</span>';
    html += '<span class="service-uptime"><span class="badge ' + badgeCls + '">' + badgeTxt + '</span></span>';
    html += '</div>';
  }
  container.innerHTML = html;
  document.getElementById('svc-ok').textContent = ok;
  document.getElementById('svc-total').textContent = state.services.length;
}
function renderStream() {
  const container = document.getElementById('stream-container');
  let html = '';
  const events = state.events.slice(-40);
  for (const e of events) {
    let badgeCls = 'badge-info';
    if (e.level === 'WARN') badgeCls = 'badge-warn';
    else if (e.level === 'ERROR') badgeCls = 'badge-err';
    else if (e.level === 'DEBUG') badgeCls = 'badge-cyan';
    html += '<div class="stream-line">';
    html += '<span class="stream-time">' + e.time + '</span>';
    html += '<span class="stream-level"><span class="badge ' + badgeCls + '">' + e.level + '</span></span>';
    html += '<span class="text-secondary truncate">' + e.svc + '</span>';
    html += '<span class="truncate" style="flex:1">' + e.msg + '</span>';
    html += '</div>';
  }
  container.innerHTML = html;
  container.scrollTop = container.scrollHeight;
}
function renderKpis() {
  document.getElementById('throughput-value').textContent = formatThroughput(Math.round(state.throughput));
  document.getElementById('latency-value').textContent = formatLatency(Math.round(state.latency));
  document.getElementById('error-value').textContent = formatError(state.errorRate);
}
function renderSystem() {
  document.getElementById('cpu-val').textContent = formatPct(state.cpu);
  document.getElementById('ram-val').textContent = formatPct(state.ram);
  document.getElementById('disk-val').textContent = formatPct(state.disk);
  document.getElementById('cpu-bar').style.width = state.cpu + '%';
  document.getElementById('ram-bar').style.width = state.ram + '%';
  document.getElementById('disk-bar').style.width = state.disk + '%';
  const badge = document.getElementById('health-badge');
  if (state.cpu > 85 || state.ram > 88) {
    badge.className = 'badge badge-warn pulse';
    badge.textContent = '● DEGRADED';
  } else if (state.errorRate > 0.3) {
    badge.className = 'badge badge-warn pulse';
    badge.textContent = '● WARNING';
  } else {
    badge.className = 'badge badge-ok pulse';
    badge.textContent = '● ONLINE';
  }
}
function renderSystemMeta() {
  const h = gen.rand(40, 280);
  const m = Math.floor(h / 60) + 'h ' + (h % 60) + 'm';
  document.getElementById('uptime-val').textContent = m;
  document.getElementById('workers-val').textContent = gen.rand(8, 32);
  document.getElementById('queue-val').textContent = gen.rand(0, 120);
}
/* ── UPDATE LOOP ── */
function update() {
  state.throughput = gen.trend(state.throughput, 60, 200, 2200);
  state.latency = gen.trend(state.latency, 5, 3, 150);
  state.errorRate = gen.trend(state.errorRate, 0.05, 0.01, 0.95);
  state.cpu = gen.trend(state.cpu, 4, 5, 98);
  state.ram = gen.trend(state.ram, 3, 20, 96);
  state.disk = gen.trend(state.disk, 1, 20, 90);
  THROUGHPUT_HISTORY.push(Math.round(state.throughput));
  THROUGHPUT_HISTORY.shift();
  LATENCY_HISTORY.push(Math.round(state.latency));
  LATENCY_HISTORY.shift();
  ERROR_HISTORY.push(Number((state.errorRate * 10).toFixed(0)));
  ERROR_HISTORY.shift();
  const tTrend = ((THROUGHPUT_HISTORY[THROUGHPUT_HISTORY.length - 1] - THROUGHPUT_HISTORY[0]) / Math.max(THROUGHPUT_HISTORY[0], 1)) * 100;
  document.getElementById('throughput-trend').innerHTML = '<span class="text-green">+' + tTrend.toFixed(1) + '</span>%';
  renderSparklineAnimated(document.getElementById('throughput-spark'), THROUGHPUT_HISTORY, 'var(--cyan)');
  renderSparklineAnimated(document.getElementById('latency-spark'), LATENCY_HISTORY, 'var(--amber)');
  renderSparklineAnimated(document.getElementById('error-spark'), ERROR_HISTORY, 'var(--red)');
  renderKpis();
  renderSystem();
  state.events.push(buildEvent());
  if (state.events.length > 80) state.events = state.events.slice(-60);
  renderStream();
}
/* ── INIT ── */
renderKpis();
renderSystem();
renderSystemMeta();
renderSparkline(document.getElementById('throughput-spark'), THROUGHPUT_HISTORY, 'var(--cyan)');
renderSparkline(document.getElementById('latency-spark'), LATENCY_HISTORY, 'var(--amber)');
renderSparkline(document.getElementById('error-spark'), ERROR_HISTORY, 'var(--red)');
renderServices();
renderStream();
setInterval(update, 2200);
/* ── SERVICE HEALTH JITTER ── */
setInterval(() => {
  for (const s of state.services) {
    s.cpu = gen.trend(s.cpu, 8, 2, 98);
    s.mem = gen.trend(s.mem, 6, 10, 95);
    s.p99 = gen.trend(s.p99, 15, 1, 600);
    if (s.cpu > 86 || s.mem > 87) s.status = 'warn';
    else if (gen.rand(1, 40) === 1) s.status = 'err';
    else s.status = 'ok';
  }
  renderServices();
}, 4000);
setInterval(renderSystemMeta, 15000);
</script>
</body>
</html>
```