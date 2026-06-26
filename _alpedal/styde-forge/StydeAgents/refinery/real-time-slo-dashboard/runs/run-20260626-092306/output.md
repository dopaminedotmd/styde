<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SLO Dashboard — Real-Time Reliability Monitoring</title>
<style>
:root {
  --bg: #0b0e15;
  --surface: #131822;
  --surface2: #1a2230;
  --border: #242d3d;
  --text: #e2e8f0;
  --text2: #94a3b8;
  --green: #22c55e;
  --yellow: #eab308;
  --red: #ef4444;
  --blue: #3b82f6;
  --purple: #a855f7;
  --orange: #f97316;
  --cyan: #06b6d4;
  --p50: #3b82f6;
  --p95: #a855f7;
  --p99: #ef4444;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', 'SF Pro', system-ui, -apple-system, sans-serif;
  padding: 24px;
  min-height: 100vh;
}
.header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 28px; flex-wrap: wrap; gap: 12px;
}
.header h1 {
  font-size: 22px; font-weight: 600; letter-spacing: -0.3px;
  background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.header-right { display: flex; gap: 12px; align-items: center; }
.time-badge {
  background: var(--surface2); border: 1px solid var(--border);
  padding: 6px 14px; border-radius: 8px; font-size: 12px; color: var(--text2);
  font-family: 'JetBrains Mono', monospace;
}
.status-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  margin-right: 6px;
}
.status-dot.green { background: var(--green); box-shadow: 0 0 8px #22c55e66; }
.status-dot.red { background: var(--red); box-shadow: 0 0 8px #ef444466; }
.status-dot.yellow { background: var(--yellow); box-shadow: 0 0 8px #eab30866; }
.grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 16px; }
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 14px; padding: 20px; transition: border-color 0.2s;
}
.card:hover { border-color: #334155; }
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 16px;
}
.card-title { font-size: 13px; font-weight: 500; color: var(--text2); text-transform: uppercase; letter-spacing: 0.5px; }
.card-value { font-size: 28px; font-weight: 700; }
/* Error Budget Gauge */
.gauge-card { grid-column: span 3; }
.gauge-container {
  position: relative; width: 100%; aspect-ratio: 1;
  display: flex; align-items: center; justify-content: center;
}
.gauge-svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.gauge-bg { fill: none; stroke: var(--surface2); stroke-width: 8; }
.gauge-fill {
  fill: none; stroke: var(--green); stroke-width: 8; stroke-linecap: round;
  transition: stroke-dashoffset 0.8s ease, stroke 0.4s ease;
}
.gauge-center {
  position: absolute; text-align: center;
}
.gauge-percent { font-size: 32px; font-weight: 700; }
.gauge-label { font-size: 11px; color: var(--text2); margin-top: 2px; }
.burn-rate {
  margin-top: 12px; display: flex; gap: 8px; align-items: center;
  justify-content: center;
}
.burn-badge {
  padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600;
}
.burn-badge.green { background: #22c55e20; color: var(--green); }
.burn-badge.yellow { background: #eab30820; color: var(--yellow); }
.burn-badge.red { background: #ef444420; color: var(--red); }
.burn-value { font-size: 12px; color: var(--text2); font-family: 'JetBrains Mono', monospace; }
/* Latency Chart */
.latency-card { grid-column: span 5; }
.latency-chart { width: 100%; height: 200px; position: relative; }
.latency-chart svg { width: 100%; height: 100%; }
.latency-legend {
  display: flex; gap: 16px; margin-top: 12px; flex-wrap: wrap;
}
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.slo-threshold-line { stroke: var(--orange); stroke-width: 1.5; stroke-dasharray: 6,4; }
/* Health Cards */
.health-card { grid-column: span 2; text-align: center; padding: 16px; }
.health-icon { font-size: 24px; margin-bottom: 8px; }
.health-label { font-size: 11px; color: var(--text2); }
/* Services */
.services-card { grid-column: span 4; }
.service-tree {
  display: flex; flex-direction: column; gap: 6px;
}
.service-node {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 8px;
  background: var(--surface2); transition: all 0.2s;
  cursor: pointer;
}
.service-node:hover { background: #1e2a3a; transform: translateX(2px); }
.service-node .status-badge {
  width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}
.service-node .status-badge.green { background: var(--green); }
.service-node .status-badge.yellow { background: var(--yellow); }
.service-node .status-badge.red { background: var(--red); }
.service-node .name { font-size: 13px; font-weight: 500; }
.service-node .meta { font-size: 11px; color: var(--text2); margin-left: auto; }
.service-children { margin-left: 24px; display: flex; flex-direction: column; gap: 4px; margin-top: 4px; }
.service-children .service-node { background: var(--surface); padding: 8px 12px; font-size: 12px; }
.cascade-highlight {
  border-left: 3px solid var(--red);
  box-shadow: inset 3px 0 0 var(--red);
}
/* Heatmap */
.heatmap-card { grid-column: span 8; }
.heatmap-grid {
  display: grid;
  grid-template-columns: 40px repeat(24, 1fr);
  gap: 2px;
  margin-top: 12px;
}
.heatmap-label {
  font-size: 9px; color: var(--text2); display: flex; align-items: center;
  justify-content: flex-end; padding-right: 6px;
}
.heatmap-cell {
  aspect-ratio: 1; border-radius: 2px; cursor: pointer;
  transition: opacity 0.15s;
}
.heatmap-cell:hover { opacity: 0.7; transform: scale(1.1); }
.heatmap-cell.empty { background: transparent; }
.heatmap-legend {
  display: flex; gap: 8px; align-items: center;
  margin-top: 10px; font-size: 11px; color: var(--text2);
}
.legend-bar { display: flex; gap: 2px; }
.legend-step { width: 14px; height: 14px; border-radius: 2px; }
/* Incident Timeline */
.incidents-card { grid-column: span 6; }
.incident-timeline {
  position: relative; padding-left: 24px;
}
.incident-timeline::before {
  content: ''; position: absolute; left: 7px; top: 0; bottom: 0;
  width: 2px; background: var(--border);
}
.incident-item {
  position: relative; padding: 10px 0; display: flex; gap: 12px;
}
.incident-dot {
  position: absolute; left: -20px; top: 13px;
  width: 12px; height: 12px; border-radius: 50%; border: 2px solid var(--surface);
}
.incident-dot.resolved { background: var(--green); }
.incident-dot.mitigated { background: var(--yellow); }
.incident-dot.active { background: var(--red); animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { box-shadow: 0 0 0 0 #ef444466; } 50% { box-shadow: 0 0 0 6px #ef444400; } }
.incident-time { font-size: 11px; color: var(--text2); min-width: 60px; }
.incident-desc { font-size: 13px; }
.incident-sev {
  font-size: 10px; padding: 2px 6px; border-radius: 4px;
  font-weight: 600; margin-left: auto;
}
.sev-S1 { background: #ef444420; color: var(--red); }
.sev-S2 { background: #f9731620; color: var(--orange); }
.sev-S3 { background: #eab30820; color: var(--yellow); }
/* SLO Definitions */
.slo-card { grid-column: span 6; }
.slo-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.slo-table th {
  text-align: left; padding: 8px 12px; color: var(--text2);
  font-weight: 500; font-size: 11px; text-transform: uppercase;
  border-bottom: 1px solid var(--border);
}
.slo-table td { padding: 8px 12px; border-bottom: 1px solid var(--border2, #1a2230); }
.slo-table tr:hover { background: var(--surface2); }
.slo-attainment {
  font-family: 'JetBrains Mono', monospace; font-weight: 600;
}
.attainment-pass { color: var(--green); }
.attainment-warn { color: var(--yellow); }
.attainment-fail { color: var(--red); }
/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: #00000080;
  display: none; align-items: center; justify-content: center;
  z-index: 100; backdrop-filter: blur(4px);
}
.modal-overlay.active { display: flex; }
.modal {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 16px; padding: 24px; max-width: 500px;
  width: 90%; max-height: 80vh; overflow-y: auto;
}
.modal h3 { font-size: 16px; margin-bottom: 12px; }
.modal p { font-size: 13px; color: var(--text2); line-height: 1.5; }
.modal-close {
  float: right; background: none; border: none; color: var(--text2);
  font-size: 20px; cursor: pointer; padding: 4px;
}
.modal-close:hover { color: var(--text); }
/* Tab/Legend Selector */
.control-row {
  display: flex; gap: 16px; align-items: center; margin-bottom: 16px;
}
.window-tabs {
  display: flex; gap: 4px; background: var(--surface2); padding: 3px;
  border-radius: 8px;
}
.window-tab {
  padding: 5px 14px; border-radius: 6px; font-size: 12px; font-weight: 500;
  cursor: pointer; border: none; background: transparent; color: var(--text2);
  transition: all 0.15s;
}
.window-tab.active { background: var(--bg); color: var(--text); }
.window-tab:hover:not(.active) { color: var(--text); }
@media (max-width: 1200px) {
  .gauge-card, .health-card { grid-column: span 4; }
  .latency-card, .services-card { grid-column: span 6; }
  .heatmap-card, .incidents-card, .slo-card { grid-column: span 12; }
}
@media (max-width: 768px) {
  .gauge-card, .health-card, .latency-card, .services-card { grid-column: span 12; }
}
</style>
</head>
<body>
<div class="header">
  <h1>Real-Time SLO Dashboard</h1>
  <div class="header-right">
    <select id="serviceSelector" style="background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:8px;font-size:13px;outline:none;">
      <option value="api-gateway">api-gateway</option>
      <option value="user-service">user-service</option>
      <option value="payment-service">payment-service</option>
      <option value="order-service">order-service</option>
      <option value="notification-service">notification-service</option>
    </select>
    <div class="window-tabs" id="windowTabs">
      <button class="window-tab active" data-window="24h">24h</button>
      <button class="window-tab" data-window="7d">7d</button>
      <button class="window-tab" data-window="30d">30d</button>
    </div>
    <div class="time-badge" id="liveTime">--</div>
  </div>
</div>
<div class="grid" id="dashboardGrid">
  <!-- Error Budget Gauge -->
  <div class="card gauge-card">
    <div class="card-header">
      <span class="card-title">Error Budget</span>
    </div>
    <div class="gauge-container">
      <svg class="gauge-svg" viewBox="0 0 120 120">
        <circle class="gauge-bg" cx="60" cy="60" r="50"/>
        <circle class="gauge-fill" id="gaugeArc" cx="60" cy="60" r="50"
          stroke-dasharray="314.16" stroke-dashoffset="0"/>
      </svg>
      <div class="gauge-center">
        <div class="gauge-percent" id="gaugePercent">--</div>
        <div class="gauge-label">remaining</div>
      </div>
    </div>
    <div class="burn-rate">
      <span id="burnBadge" class="burn-badge green">Healthy</span>
      <span class="burn-value" id="burnValue">Burn: --</span>
    </div>
    <div style="text-align:center;margin-top:8px;font-size:11px;color:var(--text2)">
      Projected exhaustion: <span id="exhaustDate">--</span>
    </div>
  </div>
  <!-- Latency Chart -->
  <div class="card latency-card">
    <div class="card-header">
      <span class="card-title">Latency (p50 / p95 / p99)</span>
      <span class="card-value" style="font-size:14px;color:var(--text2)">SLO: <span id="latencySloLabel">200ms</span></span>
    </div>
    <div class="latency-chart">
      <svg id="latencySvg" viewBox="0 0 500 200">
        <!-- axes -->
        <line x1="40" y1="20" x2="40" y2="180" stroke="#242d3d" stroke-width="1"/>
        <line x1="40" y1="180" x2="480" y2="180" stroke="#242d3d" stroke-width="1"/>
        <!-- SLO threshold -->
        <line class="slo-threshold-line" id="sloLine" x1="40" y1="60" x2="480" y2="60"/>
        <text x="482" y="64" font-size="9" fill="#f97316">SLO</text>
        <!-- paths -->
        <path id="p50Path" fill="none" stroke="var(--p50)" stroke-width="2"/>
        <path id="p95Path" fill="none" stroke="var(--p95)" stroke-width="2"/>
        <path id="p99Path" fill="none" stroke="var(--p99)" stroke-width="1.5"/>
      </svg>
    </div>
    <div class="latency-legend">
      <span class="legend-item"><span class="legend-dot" style="background:var(--p50)"></span>p50: <strong id="p50Val">--</strong></span>
      <span class="legend-item"><span class="legend-dot" style="background:var(--p95)"></span>p95: <strong id="p95Val">--</strong></span>
      <span class="legend-item"><span class="legend-dot" style="background:var(--p99)"></span>p99: <strong id="p99Val">--</strong></span>
      <span class="legend-item"><span class="legend-dot" style="background:var(--orange)"></span>SLO: <strong id="sloMsVal">200ms</strong></span>
    </div>
  </div>
  <!-- Service Health Summary -->
  <div class="card health-card">
    <div class="health-icon">🟢</div>
    <div class="health-label">Healthy</div>
    <div class="card-value" id="healthyCount" style="font-size:22px">3</div>
  </div>
  <div class="card health-card" style="grid-column:span 2">
    <div class="health-icon">🟡</div>
    <div class="health-label">Degraded</div>
    <div class="card-value" id="degradedCount" style="font-size:22px;color:var(--yellow)">1</div>
  </div>
  <div class="card health-card" style="grid-column:span 2">
    <div class="health-icon">🔴</div>
    <div class="health-label">Critical</div>
    <div class="card-value" id="criticalCount" style="font-size:22px;color:var(--red)">1</div>
  </div>
  <!-- Service Dependency Tree -->
  <div class="card services-card">
    <div class="card-header">
      <span class="card-title">Dependency Tree</span>
      <span style="font-size:11px;color:var(--text2)" id="depTimestamp">updated now</span>
    </div>
    <div class="service-tree" id="serviceTree">
      <!-- populated by JS -->
    </div>
  </div>
  <!-- Error Heatmap -->
  <div class="card heatmap-card">
    <div class="card-header">
      <span class="card-title">Error Rate Heatmap (Time × Severity)</span>
      <span style="font-size:11px;color:var(--text2)">click cell for details</span>
    </div>
    <div class="heatmap-grid" id="heatmapGrid">
      <!-- populated by JS -->
    </div>
    <div class="heatmap-legend">
      <span>Low</span>
      <div class="legend-bar" id="heatmapLegendBar"></div>
      <span>High</span>
    </div>
  </div>
  <!-- Incident Timeline -->
  <div class="card incidents-card">
    <div class="card-header">
      <span class="card-title">Incident Timeline</span>
    </div>
    <div class="incident-timeline" id="incidentTimeline">
      <!-- populated by JS -->
    </div>
  </div>
  <!-- SLO Definitions -->
  <div class="card slo-card">
    <div class="card-header">
      <span class="card-title">SLO Definitions</span>
      <span style="font-size:11px;color:var(--text2)" id="sloWindowLabel">24h window</span>
    </div>
    <table class="slo-table">
      <thead>
        <tr><th>Service</th><th>Target</th><th>Window</th><th>Attainment</th><th>Status</th></tr>
      </thead>
      <tbody id="sloTableBody">
        <!-- populated by JS -->
      </tbody>
    </table>
  </div>
</div>
<!-- Drill-down Modal -->
<div class="modal-overlay" id="drillModal">
  <div class="modal">
    <button class="modal-close" id="modalClose">&times;</button>
    <h3 id="modalTitle">Error Details</h3>
    <div id="modalBody"></div>
  </div>
</div>
<script>
// ============================================================
// Reactive Data Store (Single Source of Truth)
// ============================================================
const DATA_STORE = {
  window: '24h',
  selectedService: 'api-gateway',
  _services: {
    'api-gateway': {
      sloTarget: 0.999,
      sloMs: 200,
      budget: 0.68,
      burnRate: 0.32,
      status: 'healthy',
      p50: 42, p95: 118, p99: 185,
      latencyHistory: [],
      errors: [],
      dependencies: ['user-service', 'payment-service', 'order-service'],
      incidents: ['INC-2026-001', 'INC-2026-003']
    },
    'user-service': {
      sloTarget: 0.995,
      sloMs: 300,
      budget: 0.42,
      burnRate: 0.71,
      status: 'degraded',
      p50: 65, p95: 195, p99: 278,
      latencyHistory: [],
      errors: [],
      dependencies: ['notification-service'],
      incidents: ['INC-2026-002']
    },
    'payment-service': {
      sloTarget: 0.9995,
      sloMs: 150,
      budget: 0.12,
      burnRate: 1.8,
      status: 'critical',
      p50: 88, p95: 245, p99: 420,
      latencyHistory: [],
      errors: [],
      dependencies: [],
      incidents: ['INC-2026-001', 'INC-2026-003']
    },
    'order-service': {
      sloTarget: 0.997,
      sloMs: 250,
      budget: 0.55,
      burnRate: 0.45,
      status: 'healthy',
      p50: 55, p95: 145, p99: 220,
      latencyHistory: [],
      errors: [],
      dependencies: ['payment-service'],
      incidents: []
    },
    'notification-service': {
      sloTarget: 0.99,
      sloMs: 500,
      budget: 0.78,
      burnRate: 0.15,
      status: 'healthy',
      p50: 28, p95: 82, p99: 135,
      latencyHistory: [],
      errors: [],
      dependencies: [],
      incidents: ['INC-2026-002']
    }
  },
  _errors: [],
  _incidents: [
    { id: 'INC-2026-001', service: 'api-gateway', severity: 'S1', title: 'Gateway timeout spike — upstream payment latency', time: '2026-06-25 14:32', status: 'resolved', resolvedAt: '2026-06-25 15:47' },
    { id: 'INC-2026-002', service: 'user-service', severity: 'S2', title: 'Auth token refresh failures, degraded UX', time: '2026-06-25 22:10', status: 'mitigated', resolvedAt: '2026-06-26 01:30' },
    { id: 'INC-2026-003', service: 'payment-service', severity: 'S1', title: 'Payment processing queue backlog, 12% 503 rate', time: '2026-06-26 08:15', status: 'active', resolvedAt: null }
  ],
  get services() { return this._services; },
  get errors() { return this._errors; },
  get incidents() { return this._incidents; },
  genLatencyHistory() {
    for (const name in this._services) {
      const s = this._services[name];
      const baseP50 = s.p50, baseP95 = s.p95, baseP99 = s.p99;
      s.latencyHistory = [];
      for (let i = 0; i < 48; i++) {
        const jitter = () => (Math.random() - 0.5) * 0.4;
        s.latencyHistory.push({
          p50: Math.max(5, baseP50 * (1 + jitter())),
          p95: Math.max(10, baseP95 * (1 + jitter())),
          p99: Math.max(15, baseP99 * (1 + jitter()))
        });
      }
    }
  },
  genErrors() {
    this._errors = [];
    const sevs = ['critical', 'high', 'medium', 'low'];
    const services = Object.keys(this._services);
    for (let day = 0; day < 7; day++) {
      for (let hour = 0; hour < 24; hour++) {
        for (const svc of services) {
          const status = this._services[svc].status;
          const baseRate = status === 'critical' ? 0.7 : status === 'degraded' ? 0.35 : 0.08;
          const rate = baseRate * (0.5 + Math.random());
          const count = Math.round(rate * 5);
          if (count > 0) {
            const sevIdx = count > 3 ? 0 : count > 1 ? Math.floor(Math.random() * 3) : 2 + Math.floor(Math.random() * 2);
            this._errors.push({
              service: svc, day, hour, count,
              severity: sevs[Math.min(sevIdx, 3)],
              samples: Array.from({length: Math.min(count, 3)}, () => ({
                msg: ['Connection timeout','5xx response','DNS resolution failed','TLS handshake slow','Rate limit exceeded'][Math.floor(Math.random()*5)],
                code: [500,502,503,504,429][Math.floor(Math.random()*5)]
              }))
            });
          }
        }
      }
    }
  },
  init() {
    this.genLatencyHistory();
    this.genErrors();
  }
};
DATA_STORE.init();
// ============================================================
// Computed Helpers
// ============================================================
function getService(name) { return DATA_STORE.services[name] || DATA_STORE.services['api-gateway']; }
function getErrorsForService(svc, windowHours) {
  const cutoff = windowHours === 24 ? 0 : windowHours === 168 ? 0 : 0;
  return DATA_STORE.errors.filter(e => e.service === svc);
}
function getIncidentsForService(svc) {
  const svcInc = DATA_STORE.services[svc]?.incidents || [];
  return DATA_STORE.incidents.filter(i => svcInc.includes(i.id));
}
// ============================================================
// Error Budget Gauge
// ============================================================
function renderGauge(svc) {
  const s = getService(svc);
  const pct = Math.round(s.budget * 100);
  const circum = 2 * Math.PI * 50;
  const offset = circum * (1 - s.budget);
  const arc = document.getElementById('gaugeArc');
  arc.setAttribute('stroke-dasharray', circum);
  arc.setAttribute('stroke-dashoffset', offset);
  let color = 'var(--green)';
  let badgeClass = 'green';
  let badgeText = 'Healthy';
  if (s.budget < 0.2) { color = 'var(--red)'; badgeClass = 'red'; badgeText = 'Critical'; }
  else if (s.budget < 0.5) { color = 'var(--yellow)'; badgeClass = 'yellow'; badgeText = 'Warning'; }
  arc.style.stroke = color;
  document.getElementById('gaugePercent').textContent = pct + '%';
  document.getElementById('gaugePercent').style.color = color;
  document.getElementById('burnBadge').textContent = badgeText;
  document.getElementById('burnBadge').className = 'burn-badge ' + badgeClass;
  document.getElementById('burnValue').textContent = 'Burn: ' + s.burnRate.toFixed(2) + 'x';
  // Projected exhaustion
  if (s.burnRate > 0 && s.budget > 0) {
    const daysLeft = s.budget / s.burnRate;
    const d = new Date();
    d.setDate(d.getDate() + Math.ceil(daysLeft));
    document.getElementById('exhaustDate').textContent = daysLeft < 1 ? 'within 24h' :
      d.toLocaleDateString('en-US', {month:'short', day:'numeric'});
  } else {
    document.getElementById('exhaustDate').textContent = 'N/A';
  }
}
// ============================================================
// Latency Chart
// ============================================================
function renderLatency(svc) {
  const s = getService(svc);
  const hist = s.latencyHistory || [];
  const w = 460, h = 160;
  const xScale = w / Math.max(hist.length - 1, 1);
  const maxLat = Math.max(s.sloMs * 1.4, ...hist.map(d => d.p99), 50);
  const yScale = h / maxLat;
  function buildPath(data, key) {
    return data.map((d, i) => {
      const x = 40 + i * xScale;
      const y = 180 - d[key] * yScale;
      return (i === 0 ? 'M' : 'L') + x.toFixed(1) + ' ' + y.toFixed(1);
    }).join(' ');
  }
  document.getElementById('p50Path').setAttribute('d', buildPath(hist, 'p50'));
  document.getElementById('p95Path').setAttribute('d', buildPath(hist, 'p95'));
  document.getElementById('p99Path').setAttribute('d', buildPath(hist, 'p99'));
  const sloY = 180 - s.sloMs * yScale;
  document.getElementById('sloLine').setAttribute('y1', sloY);
  document.getElementById('sloLine').setAttribute('y2', sloY);
  const last = hist[hist.length - 1] || {};
  document.getElementById('p50Val').textContent = (last.p50 || s.p50).toFixed(0) + 'ms';
  document.getElementById('p95Val').textContent = (last.p95 || s.p95).toFixed(0) + 'ms';
  document.getElementById('p99Val').textContent = (last.p99 || s.p99).toFixed(0) + 'ms';
  document.getElementById('sloMsVal').textContent = s.sloMs + 'ms';
  document.getElementById('latencySloLabel').textContent = s.sloMs + 'ms';
}
// ============================================================
// Error Heatmap
// ============================================================
const SEV_COLORS = { 'critical': '#ef4444', 'high': '#f97316', 'medium': '#eab308', 'low': '#22c55e' };
function renderHeatmap(svc, win) {
  const grid = document.getElementById('heatmapGrid');
  const errors = getErrorsForService(svc, win);
  grid.innerHTML = '';
  // header: hours 0-23
  const empty = document.createElement('div');
  empty.className = 'heatmap-label';
  grid.appendChild(empty);
  for (let h = 0; h < 24; h++) {
    const label = document.createElement('div');
    label.className = 'heatmap-label';
    label.textContent = h + 'h';
    grid.appendChild(label);
  }
  const severityOrder = ['critical', 'high', 'medium', 'low'];
  for (const sev of severityOrder) {
    const label = document.createElement('div');
    label.className = 'heatmap-label';
    label.textContent = sev.slice(0, 3);
    grid.appendChild(label);
    for (let h = 0; h < 24; h++) {
      const cell = document.createElement('div');
      const match = errors.find(e => e.hour === h && e.severity === sev);
      if (match) {
        const intensity = Math.min(match.count / 5, 1);
        cell.className = 'heatmap-cell';
        cell.style.background = match.severity === 'critical' || match.severity === 'high'
          ? SEV_COLORS[match.severity]
          : `rgba(34, 197, 94, ${0.2 + intensity * 0.6})`;
        cell.title = match.service + ': ' + match.count + ' errors (' + match.severity + ')';
        cell.dataset.service = match.service;
        cell.dataset.count = match.count;
        cell.dataset.severity = match.severity;
        cell.dataset.hour = h;
        cell.addEventListener('click', () => showDrilldown(svc, match));
      } else {
        cell.className = 'heatmap-cell empty';
      }
      grid.appendChild(cell);
    }
  }
}
// ============================================================
// Dependency Tree
// ============================================================
function renderDependencyTree(svc) {
  const root = document.getElementById('serviceTree');
  root.innerHTML = '';
  const s = getService(svc);
  function buildNode(name, depth, isAffected) {
    const svcData = getService(name);
    const div = document.createElement('div');
    div.className = 'service-node' + (isAffected ? ' cascade-highlight' : '');
    div.style.marginLeft = (depth * 16) + 'px';
    const badge = document.createElement('div');
    badge.className = 'status-badge ' + (svcData.status === 'critical' ? 'red' : svcData.status === 'degraded' ? 'yellow' : 'green');
    div.appendChild(badge);
    const nameSpan = document.createElement('span');
    nameSpan.className = 'name';
    nameSpan.textContent = name;
    div.appendChild(nameSpan);
    const meta = document.createElement('span');
    meta.className = 'meta';
    meta.textContent = svcData.status + ' · ' + Math.round(svcData.budget * 100) + '% budget';
    if (svcData.burnRate > 1) meta.textContent += ' 🔥';
    div.appendChild(meta);
    div.addEventListener('click', () => {
      DATA_STORE.selectedService = name;
      document.getElementById('serviceSelector').value = name;
      refreshAll(name);
    });
    root.appendChild(div);
    return div;
  }
  // Root
  buildNode(svc, 0, false);
  // Direct dependencies
  for (const dep of s.dependencies || []) {
    const depData = getService(dep);
    const isAffected = depData.status === 'critical' || depData.status === 'degraded';
    buildNode(dep, 1, isAffected);
    // Nested
    const nestedDeps = depData.dependencies || [];
    for (const nested of nestedDeps) {
      const nd = getService(nested);
      buildNode(nested, 2, nd.status === 'critical' || nd.status === 'degraded');
    }
  }
  document.getElementById('depTimestamp').textContent = new Date().toLocaleTimeString();
}
// ============================================================
// SLO Table
// ============================================================
function renderSloTable(win) {
  const body = document.getElementById('sloTableBody');
  body.innerHTML = '';
  const winLabel = win === '24h' ? '24h' : win === '7d' ? '7d' : '30d';
  document.getElementById('sloWindowLabel').textContent = winLabel + ' window';
  for (const [name, data] of Object.entries(DATA_STORE.services)) {
    const tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.addEventListener('click', () => {
      DATA_STORE.selectedService = name;
      document.getElementById('serviceSelector').value = name;
      refreshAll(name);
    });
    const attained = data.budget > 0.5 ? true : data.budget > 0.2 ? null : false;
    const pct = Math.round(data.sloTarget * 10000) / 100;
    tr.innerHTML = `
      <td>${name}</td>
      <td>${pct}% · ${data.sloMs}ms</td>
      <td>${winLabel}</td>
      <td class="slo-attainment ${attained === true ? 'attainment-pass' : attained === null ? 'attainment-warn' : 'attainment-fail'}">
        ${attained === true ? '✓ ' : attained === null ? '~ ' : '✗ '}${Math.round(data.budget * 100)}%
      </td>
      <td><span class="status-dot ${data.status === 'critical' ? 'red' : data.status === 'degraded' ? 'yellow' : 'green'}"></span>${data.status}</td>
    `;
    body.appendChild(tr);
  }
}
// ============================================================
// Incident Timeline
// ============================================================
function renderIncidents(svc) {
  const timeline = document.getElementById('incidentTimeline');
  timeline.innerHTML = '';
  const svcIncidents = getIncidentsForService(svc);
  if (svcIncidents.length === 0) {
    timeline.innerHTML = '<div style="color:var(--text2);font-size:13px;padding:16px 0">No incidents in this window</div>';
    return;
  }
  for (const inc of svcIncidents) {
    const item = document.createElement('div');
    item.className = 'incident-item';
    const dot = document.createElement('div');
    dot.className = 'incident-dot ' + (inc.status === 'resolved' ? 'resolved' : inc.status === 'mitigated' ? 'mitigated' : 'active');
    item.appendChild(dot);
    const time = document.createElement('div');
    time.className = 'incident-time';
    time.textContent = inc.time.split(' ')[1];
    item.appendChild(time);
    const desc = document.createElement('div');
    desc.className = 'incident-desc';
    desc.textContent = inc.title;
    item.appendChild(desc);
    const sev = document.createElement('span');
    sev.className = 'incident-sev sev-' + inc.severity;
    sev.textContent = inc.severity + (inc.status === 'active' ? ' · active' : '');
    item.appendChild(sev);
    timeline.appendChild(item);
    // Resolution marker
    if (inc.resolvedAt) {
      const resItem = document.createElement('div');
      resItem.className = 'incident-item';
      resItem.style.opacity = '0.6';
      const resDot = document.createElement('div');
      resDot.className = 'incident-dot resolved';
      resItem.appendChild(resDot);
      const resTime = document.createElement('div');
      resTime.className = 'incident-time';
      resTime.textContent = inc.resolvedAt.split(' ')[1];
      resItem.appendChild(resTime);
      const resDesc = document.createElement('div');
      resDesc.className = 'incident-desc';
      resDesc.textContent = 'Resolved — ' + inc.id;
      resItem.appendChild(resDesc);
      timeline.appendChild(resItem);
    }
  }
}
// ============================================================
// Modal / Drill-down
// ============================================================
function showDrilldown(svc, error) {
  const modal = document.getElementById('drillModal');
  document.getElementById('modalTitle').textContent = 'Errors: ' + svc + ' @ ' + error.hour + ':00 (' + error.severity + ')';
  let html = '<p><strong>Service:</strong> ' + error.service + '</p>';
  html += '<p><strong>Hour:</strong> ' + error.hour + ':00</p>';
  html += '<p><strong>Severity:</strong> ' + error.severity + '</p>';
  html += '<p><strong>Count:</strong> ' + error.count + '</p>';
  if (error.samples && error.samples.length > 0) {
    html += '<p><strong>Sample Errors:</strong></p><ul style="margin-top:4px;padding-left:20px">';
    for (const s of error.samples) {
      html += '<li style="font-size:12px;margin-bottom:4px">' + s.msg + ' (HTTP ' + s.code + ')</li>';
    }
    html += '</ul>';
  }
  document.getElementById('modalBody').innerHTML = html;
  modal.classList.add('active');
}
document.getElementById('modalClose').addEventListener('click', () => {
  document.getElementById('drillModal').classList.remove('active');
});
document.getElementById('drillModal').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) document.getElementById('drillModal').classList.remove('active');
});
// ============================================================
// Health Summary
// ============================================================
function renderHealthSummary() {
  let healthy = 0, degraded = 0, critical = 0;
  for (const s of Object.values(DATA_STORE.services)) {
    if (s.status === 'critical') critical++;
    else if (s.status === 'degraded') degraded++;
    else healthy++;
  }
  document.getElementById('healthyCount').textContent = healthy;
  document.getElementById('degradedCount').textContent = degraded;
  document.getElementById('criticalCount').textContent = critical;
}
// ============================================================
// Heatmap Legend
// ============================================================
function renderHeatmapLegend() {
  const bar = document.getElementById('heatmapLegendBar');
  bar.innerHTML = '';
  const steps = ['#1a2230', '#22c55e44', '#22c55e88', '#22c55e', '#eab308', '#f97316', '#ef4444'];
  for (const c of steps) {
    const div = document.createElement('div');
    div.className = 'legend-step';
    div.style.background = c;
    bar.appendChild(div);
  }
}
// ============================================================
// Clock
// ============================================================
function updateClock() {
  document.getElementById('liveTime').textContent = new Date().toLocaleTimeString();
}
// ============================================================
// Master Refresh
// ============================================================
function refreshAll(svc) {
  svc = svc || DATA_STORE.selectedService;
  const win = DATA_STORE.window;
  renderGauge(svc);
  renderLatency(svc);
  renderHeatmap(svc, win);
  renderDependencyTree(svc);
  renderIncidents(svc);
  renderSloTable(win);
  renderHealthSummary();
}
// ============================================================
// Window Tab Switching
// ============================================================
document.querySelectorAll('.window-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.window-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    DATA_STORE.window = tab.dataset.window;
    refreshAll();
  });
});
// ============================================================
// Service Selector
// ============================================================
document.getElementById('serviceSelector').addEventListener('change', (e) => {
  DATA_STORE.selectedService = e.target.value;
  refreshAll(e.target.value);
});
// ============================================================
// Self-healing: re-bind on visibility change
// ============================================================
document.addEventListener('visibilitychange', () => {
  if (!document.hidden) {
    updateClock();
    refreshAll();
  }
});
// MutationObserver: re-bind interactive elements when DOM changes
const observer = new MutationObserver(() => {
  // Re-attach heatmap click listeners for any newly added cells
  document.querySelectorAll('.heatmap-cell[data-service]').forEach(cell => {
    if (!cell._bound) {
      cell._bound = true;
      // Remove existing and re-add
      cell.replaceWith(cell.cloneNode(true));
    }
  });
});
observer.observe(document.getElementById('dashboardGrid'), { childList: true, subtree: true });
// ============================================================
// Live refresh (every 15s simulated)
// ============================================================
setInterval(() => {
  updateClock();
  // Simulated data drift: small random shifts
  const svc = getService(DATA_STORE.selectedService);
  svc.budget = Math.max(0, Math.min(1, svc.budget + (Math.random() - 0.5) * 0.02));
  svc.burnRate = Math.max(0.05, svc.burnRate + (Math.random() - 0.5) * 0.1);
  svc.p50 = Math.max(5, svc.p50 + (Math.random() - 0.5) * 4);
  svc.p95 = Math.max(10, svc.p95 + (Math.random() - 0.5) * 8);
  svc.p99 = Math.max(15, svc.p99 + (Math.random() - 0.5) * 12);
  // Recompute status from budget
  svc.status = svc.budget < 0.2 ? 'critical' : svc.budget < 0.5 ? 'degraded' : 'healthy';
  refreshAll();
}, 15000);
// ============================================================
// Init
// ============================================================
renderHeatmapLegend();
updateClock();
refreshAll();
console.log('SLO Dashboard initialized: ' + new Date().toISOString());
console.log('Data store has ' + DATA_STORE.errors.length + ' error records across ' +
  Object.keys(DATA_STORE.services).length + ' services');
</script>
</body>
</html>