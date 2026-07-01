Dashboard Report Factory - Export Engine Output
mode: interactive_html
version: 1.0.0
exports:
  - pdf
  - png
  - html_snapshot
  - csv
features:
  - schedule_config
  - brand_customization
  - compare_mode
  - narrative_summary
  - preview_pane
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Report Factory</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f0f2f5; color: #1a1a2e; }
.dashboard-container { max-width: 1400px; margin: 0 auto; padding: 20px; }
/* Header / Brand Bar */
.brand-bar { display: flex; align-items: center; justify-content: space-between; padding: 12px 24px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #fff; border-radius: 12px 12px 0 0; margin-bottom: 0; }
.brand-bar .logo { display: flex; align-items: center; gap: 12px; }
.brand-bar .logo svg { width: 32px; height: 32px; }
.brand-bar .logo h1 { font-size: 18px; font-weight: 600; letter-spacing: 0.5px; }
.brand-bar .brand-controls { display: flex; gap: 12px; align-items: center; }
.brand-bar input[type="color"] { width: 28px; height: 28px; border: 2px solid rgba(255,255,255,0.3); border-radius: 6px; cursor: pointer; background: none; padding: 0; }
.brand-bar input[type="text"] { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #fff; padding: 6px 12px; border-radius: 6px; font-size: 13px; width: 160px; }
.brand-bar input[type="text"]::placeholder { color: rgba(255,255,255,0.4); }
/* Export Toolbar */
.export-toolbar { display: flex; gap: 8px; padding: 12px 24px; background: #fff; border-bottom: 1px solid #e0e0e0; flex-wrap: wrap; align-items: center; }
.export-btn { display: flex; align-items: center; gap: 6px; padding: 8px 16px; border: 1px solid #d0d0d0; border-radius: 8px; background: #fafafa; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.15s; }
.export-btn:hover { background: #e8f0fe; border-color: #1a73e8; color: #1a73e8; }
.export-btn svg { width: 16px; height: 16px; }
.export-btn.primary { background: #1a73e8; color: #fff; border-color: #1a73e8; }
.export-btn.primary:hover { background: #1557b0; }
.export-btn.active { background: #e8f0fe; border-color: #1a73e8; }
.export-divider { width: 1px; height: 28px; background: #e0e0e0; margin: 0 8px; }
/* Dashboard Grid */
.dashboard-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 16px; padding: 16px 0; }
.card { background: #fff; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
.card-header { display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; border-bottom: 1px solid #f0f0f0; font-weight: 600; font-size: 14px; }
.card-body { padding: 18px; }
/* Chart Containers */
.chart-container { width: 100%; height: 220px; position: relative; }
.bar-chart { display: flex; align-items: flex-end; gap: 8px; height: 180px; padding: 0 8px; }
.bar-group { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.bar { width: 100%; border-radius: 4px 4px 0 0; min-height: 4px; transition: height 0.6s cubic-bezier(0.22, 1, 0.36, 1); position: relative; }
.bar-label { font-size: 11px; color: #666; margin-top: 6px; }
.bar-value { font-size: 11px; font-weight: 600; color: #444; }
.metric-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f5f5f5; }
.metric-row:last-child { border-bottom: none; }
.metric-label { font-size: 13px; color: #666; }
.metric-value { font-size: 13px; font-weight: 600; }
.metric-value.up { color: #0d9f6e; }
.metric-value.down { color: #d93025; }
/* Data Table */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th { text-align: left; padding: 10px 14px; background: #f8f9fa; font-weight: 600; color: #444; border-bottom: 2px solid #e0e0e0; }
.data-table td { padding: 10px 14px; border-bottom: 1px solid #f0f0f0; }
.data-table tr:hover td { background: #f8faff; }
/* Schedule Panel */
.schedule-panel { display: none; }
.schedule-panel.visible { display: block; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #fff; border-radius: 14px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 28px; width: 480px; z-index: 1000; }
.schedule-overlay { display: none; }
.schedule-overlay.visible { display: block; position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 999; }
.schedule-panel h2 { font-size: 18px; margin-bottom: 20px; }
.schedule-form label { display: block; font-size: 13px; font-weight: 500; color: #444; margin: 12px 0 4px; }
.schedule-form select, .schedule-form input { width: 100%; padding: 8px 12px; border: 1px solid #d0d0d0; border-radius: 6px; font-size: 13px; }
.schedule-form .row { display: flex; gap: 12px; }
.schedule-form .row > * { flex: 1; }
.schedule-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px; }
.schedule-actions button { padding: 8px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 500; font-size: 13px; }
.schedule-actions .cancel { background: #f0f0f0; color: #444; }
.schedule-actions .save { background: #1a73e8; color: #fff; }
/* Compare Mode */
.compare-toggle { display: inline-flex; align-items: center; gap: 6px; cursor: pointer; padding: 4px 12px; border-radius: 20px; font-size: 12px; background: #f0f0f0; border: 1px solid #d0d0d0; transition: all 0.15s; }
.compare-toggle.active { background: #e8f0fe; border-color: #1a73e8; color: #1a73e8; }
.delta-badge { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; margin-left: 6px; }
.delta-badge.positive { background: #e6f4ea; color: #0d9f6e; }
.delta-badge.negative { background: #fce8e6; color: #d93025; }
.delta-badge.neutral { background: #f0f0f0; color: #666; }
/* Narrative Summary */
.narrative-summary { background: #f8faff; border-left: 4px solid #1a73e8; padding: 14px 18px; margin: 0 0 12px 0; border-radius: 0 8px 8px 0; font-size: 13px; line-height: 1.6; color: #333; }
/* Footer */
.dashboard-footer { text-align: center; padding: 16px; font-size: 12px; color: #888; border-top: 1px solid #e0e0e0; margin-top: 16px; }
/* Notification Toast */
.toast { position: fixed; bottom: 30px; right: 30px; background: #323232; color: #fff; padding: 12px 24px; border-radius: 8px; font-size: 13px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); z-index: 2000; opacity: 0; transform: translateY(20px); transition: all 0.3s; }
.toast.visible { opacity: 1; transform: translateY(0); }
/* Responsive */
@media (max-width: 900px) { .dashboard-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="dashboard-container" id="dashboard">
  <!-- Brand Bar -->
  <div class="brand-bar" id="brandBar">
    <div class="logo">
      <svg viewBox="0 0 32 32" fill="none"><rect width="32" height="32" rx="8" fill="currentColor" opacity="0.8"/><path d="M8 20l6-8 4 4 6-7" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>
      <h1>Dashboard Report Factory</h1>
    </div>
    <div class="brand-controls">
      <input type="text" id="brandTitle" value="Q2 2026 Executive Dashboard" placeholder="Dashboard title">
      <input type="color" id="brandColor" value="#1a1a2e">
    </div>
  </div>
  <!-- Export Toolbar -->
  <div class="export-toolbar">
    <button class="export-btn primary" onclick="exportPDF()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      Export PDF
    </button>
    <button class="export-btn" onclick="exportPNG()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      PNG
    </button>
    <button class="export-btn" onclick="exportHTML()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 002 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>
      HTML Snapshot
    </button>
    <button class="export-btn" onclick="exportCSV()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="16" x2="16" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
      CSV
    </button>
    <div class="export-divider"></div>
    <button class="export-btn" onclick="toggleSchedule()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      Schedule
    </button>
    <button class="export-btn" onclick="toggleCompare()" id="compareBtn">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
      Compare Mode
    </button>
    <div style="margin-left:auto;font-size:12px;color:#888;" id="exportTimestamp">Last export: never</div>
  </div>
  <!-- Narrative Summary -->
  <div class="narrative-summary" id="narrativeSummary">
    <strong>Report Summary:</strong> Revenue grew 14.2% year-over-year driven by Enterprise segment expansion (up 23.5%). User acquisition hit 18.4K new signups in June, a 6-month high. Support ticket volume increased 8.7% but first-response time improved to 2.1 hours. Gross margin held steady at 71.3%. Key risk: churn rate ticked up 0.3pp to 4.1% in the SMB segment.
  </div>
  <!-- Dashboard Grid -->
  <div class="dashboard-grid">
    <!-- Left Column -->
    <div>
      <!-- Revenue Chart Card -->
      <div class="card" style="margin-bottom:16px;">
        <div class="card-header">
          <span>Monthly Revenue (USD)</span>
          <span style="font-size:12px;color:#888;">vs previous period</span>
        </div>
        <div class="card-body">
          <div class="chart-container">
            <div class="bar-chart" id="revenueChart"></div>
          </div>
        </div>
      </div>
      <!-- Data Table Card -->
      <div class="card">
        <div class="card-header">
          <span>Performance Metrics</span>
          <span style="font-size:12px;color:#888;">Last 6 months</span>
        </div>
        <div class="card-body" style="padding:0;">
          <table class="data-table">
            <thead>
              <tr>
                <th>Month</th>
                <th>Revenue</th>
                <th>Users</th>
                <th>Conversion</th>
                <th>Churn</th>
              </tr>
            </thead>
            <tbody id="metricsTableBody"></tbody>
          </table>
        </div>
      </div>
    </div>
    <!-- Right Column -->
    <div>
      <!-- KPI Cards -->
      <div class="card" style="margin-bottom:16px;">
        <div class="card-header">
          <span>Key Metrics (Current Month)</span>
          <span style="font-size:12px;color:#888;">compare</span>
        </div>
        <div class="card-body" id="kpiContainer"></div>
      </div>
      <!-- User Growth Card -->
      <div class="card">
        <div class="card-header">
          <span>User Growth</span>
          <span style="font-size:12px;color:#888;">new signups per month</span>
        </div>
        <div class="card-body">
          <div class="chart-container">
            <div class="bar-chart" id="userChart"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Footer -->
  <div class="dashboard-footer" id="dashboardFooter">
    Dashboard Report Factory v1.0 | Generated 2026-06-28 | Confidential
  </div>
</div>
<!-- Schedule Panel -->
<div class="schedule-overlay" id="scheduleOverlay" onclick="toggleSchedule()"></div>
<div class="schedule-panel" id="schedulePanel">
  <h2>Schedule Auto-Export</h2>
  <div class="schedule-form">
    <label>Export Format</label>
    <select id="schedFormat">
      <option value="pdf">PDF</option>
      <option value="png">PNG</option>
      <option value="html">HTML Snapshot</option>
    </select>
    <label>Frequency</label>
    <div class="row">
      <select id="schedFreq">
        <option value="daily">Daily</option>
        <option value="weekly" selected>Weekly</option>
        <option value="monthly">Monthly</option>
      </select>
      <select id="schedDay">
        <option value="monday">Monday</option>
        <option value="tuesday">Tuesday</option>
        <option value="wednesday">Wednesday</option>
        <option value="thursday">Thursday</option>
        <option value="friday">Friday</option>
        <option value="saturday">Saturday</option>
        <option value="sunday">Sunday</option>
      </select>
    </div>
    <label>Time</label>
    <div class="row">
      <input type="time" id="schedTime" value="09:00">
      <select id="schedTimezone">
        <option value="UTC">UTC</option>
        <option value="US/Eastern">US/Eastern</option>
        <option value="US/Pacific">US/Pacific</option>
        <option value="Europe/London">Europe/London</option>
        <option value="Europe/Berlin" selected>Europe/Berlin</option>
      </select>
    </div>
    <label>Email Recipients (comma separated)</label>
    <input type="text" id="schedEmail" value="reports@company.com" placeholder="email@example.com">
    <label>Include narrative summary</label>
    <div class="row">
      <select id="schedNarrative">
        <option value="yes">Yes</option>
        <option value="no">No</option>
      </select>
    </div>
    <div style="margin-top:12px;padding:10px;background:#f8f9fa;border-radius:6px;font-size:12px;color:#666;">
      <strong>Cron expression:</strong> <span id="cronDisplay">0 9 * * 1</span>
    </div>
    <div class="schedule-actions">
      <button class="cancel" onclick="toggleSchedule()">Cancel</button>
      <button class="save" onclick="saveSchedule()">Save Schedule</button>
    </div>
  </div>
</div>
<!-- Toast -->
<div class="toast" id="toast"></div>
<script>
// === DATA ===
const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
const revenueData = [28400, 31200, 33800, 35900, 38200, 41200];
const usersData = [11200, 13400, 14800, 15900, 17100, 18400];
const baselineRevenue = [26000, 28500, 31000, 33000, 35000, 37000];
const baselineUsers = [9800, 11500, 12800, 14000, 15200, 16300];
const conversionData = [3.2, 3.5, 3.8, 4.0, 4.2, 4.4];
const churnData = [3.8, 3.9, 3.9, 4.0, 4.1, 4.3];
const baselineConversion = [3.0, 3.2, 3.4, 3.6, 3.8, 3.9];
const baselineChurn = [4.1, 4.0, 4.0, 4.2, 4.1, 4.0];
let compareModeActive = false;
function computeDelta(current, baseline) {
  if (!baseline || baseline === 0) return { val: 0, pct: 0 };
  const diff = current - baseline;
  return { val: diff, pct: (diff / baseline * 100) };
}
function formatCurrency(n) { return '$' + n.toLocaleString(); }
function formatNumber(n) { return n.toLocaleString(); }
// Render bar chart
function renderBarChart(containerId, data, baseline, color, label) {
  const container = document.getElementById(containerId);
  const max = Math.max(...data, ...(baseline || data)) * 1.15;
  let html = '';
  data.forEach((val, i) => {
    const h = (val / max * 100);
    const currentVal = compareModeActive && baseline ? 'baseline' : 'current';
    const baseH = baseline ? (baseline[i] / max * 100) : 0;
    html += '<div class="bar-group">';
    html += `<div class="bar-value">${label === 'currency' ? formatCurrency(val) : formatNumber(val)}</div>`;
    html += '<div style="display:flex;gap:2px;align-items:flex-end;width:100%;height:100%;min-height:140px;justify-content:center;">';
    if (compareModeActive && baseline) {
      html += `<div class="bar" style="height:${baseH}%;background:rgba(0,0,0,0.15);width:40%;" title="Baseline: ${baseline[i]}"></div>`;
    }
    html += `<div class="bar" style="height:${h}%;background:${color};width:${compareModeActive && baseline ? '40%' : '80%'};opacity:0.85;" title="${val}"></div>`;
    html += '</div>';
    html += `<div class="bar-label">${months[i]}</div>`;
    html += '</div>';
  });
  container.innerHTML = html;
}
// Render KPIs
function renderKPIs() {
  const container = document.getElementById('kpiContainer');
  const kpis = [
    { label: 'Total Revenue', value: '$41,200', delta: { current: 41200, baseline: 37000, fmt: 'currency' }, up: true },
    { label: 'Active Users', value: '18,400', delta: { current: 18400, baseline: 16300, fmt: 'number' }, up: true },
    { label: 'Gross Margin', value: '71.3%', delta: { current: 71.3, baseline: 70.1, fmt: 'pct' }, up: true },
    { label: 'Conversion Rate', value: '4.4%', delta: { current: 4.4, baseline: 3.9, fmt: 'pct' }, up: true },
    { label: 'Churn Rate', value: '4.3%', delta: { current: 4.3, baseline: 4.0, fmt: 'pct' }, up: false },
    { label: 'Avg Ticket Time', value: '2.1h', delta: { current: 2.1, baseline: 2.8, fmt: 'hours' }, up: true },
  ];
  let html = '';
  kpis.forEach(kpi => {
    let deltaHtml = '';
    if (compareModeActive && kpi.delta) {
      const d = computeDelta(kpi.delta.current, kpi.delta.baseline);
      const isPositive = kpi.up ? d.val > 0 : d.val < 0;
      const cls = d.val > 0 ? (kpi.up ? 'positive' : 'negative') : d.val < 0 ? (kpi.up ? 'negative' : 'positive') : 'neutral';
      let display;
      if (kpi.delta.fmt === 'currency') display = (d.val > 0 ? '+' : '') + formatCurrency(d.val);
      else if (kpi.delta.fmt === 'pct') display = (d.val > 0 ? '+' : '') + d.val.toFixed(1) + 'pp';
      else display = (d.val > 0 ? '+' : '') + d.val.toFixed(1);
      deltaHtml = `<span class="delta-badge ${cls}">${display}</span>`;
    }
    const arrow = kpi.up ? '&#9650;' : '&#9660;';
    const cls = kpi.up ? 'up' : 'down';
    html += `<div class="metric-row"><span class="metric-label">${kpi.label}</span><span class="metric-value ${cls}">${kpi.value} ${deltaHtml}</span></div>`;
  });
  container.innerHTML = html;
}
// Render table
function renderTable() {
  const tbody = document.getElementById('metricsTableBody');
  const revYoy = [28400, 31200, 33800, 35900, 38200, 41200];
  const revPrev = [24500, 27800, 29800, 32000, 34500, 37000];
  let html = '';
  months.forEach((m, i) => {
    const dRev = computeDelta(revYoy[i], revPrev[i]);
    const dConv = computeDelta(conversionData[i], baselineConversion[i]);
    const dChurn = computeDelta(churnData[i], baselineChurn[i]);
    const rCls = dRev.val > 0 ? 'up' : 'down';
    const cCls = dConv.val > 0 ? 'up' : 'down';
    const chCls = dChurn.val > 0 ? 'down' : 'up';
    html += `<tr>
      <td><strong>${m}</strong></td>
      <td>${formatCurrency(revYoy[i])} <span class="metric-value ${rCls}" style="font-size:11px;">${dRev.val > 0 ? '+' : ''}${dRev.pct.toFixed(1)}%</span></td>
      <td>${formatNumber(usersData[i])}</td>
      <td>${conversionData[i]}%</td>
      <td>${churnData[i]}%</td>
    </tr>`;
  });
  tbody.innerHTML = html;
}
function renderDashboard() {
  renderBarChart('revenueChart', revenueData, compareModeActive ? baselineRevenue : null, '#1a73e8', 'currency');
  renderBarChart('userChart', usersData, compareModeActive ? baselineUsers : null, '#0d9f6e', 'number');
  renderKPIs();
  renderTable();
}
function toggleCompare() {
  compareModeActive = !compareModeActive;
  document.getElementById('compareBtn').classList.toggle('active');
  if (compareModeActive) {
    document.getElementById('narrativeSummary').innerHTML = '<strong>Compare Mode Active:</strong> Current period (solid) vs Baseline period (faded). Delta badges show absolute change on KPIs.';
  } else {
    document.getElementById('narrativeSummary').innerHTML = '<strong>Report Summary:</strong> Revenue grew 14.2% year-over-year driven by Enterprise segment expansion (up 23.5%). User acquisition hit 18.4K new signups in June, a 6-month high. Support ticket volume increased 8.7% but first-response time improved to 2.1 hours. Gross margin held steady at 71.3%. Key risk: churn rate ticked up 0.3pp to 4.1% in the SMB segment.';
  }
  renderDashboard();
}
// === EXPORTS ===
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('visible');
  setTimeout(() => t.classList.remove('visible'), 3000);
}
// Update brand color
document.getElementById('brandColor').addEventListener('input', function() {
  document.getElementById('brandBar').style.background = `linear-gradient(135deg, ${this.value} 0%, #16213e 100%)`;
});
document.getElementById('brandTitle').addEventListener('input', function() {
  document.querySelector('.brand-bar .logo h1').textContent = this.value || 'Dashboard';
});
// PDF Export
function exportPDF() {
  showToast('Generating PDF...');
  const { jsPDF } = window.jspdf;
  const dashboard = document.getElementById('dashboard');
  html2canvas(dashboard, {
    scale: 2,
    useCORS: true,
    backgroundColor: '#f0f2f5',
    logging: false,
    windowHeight: dashboard.scrollHeight,
  }).then(canvas => {
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pdfW = 210;
    const pdfH = (canvas.height * pdfW) / canvas.width;
    let heightLeft = pdfH;
    let position = 0;
    const pageHeight = 297;
    pdf.addImage(imgData, 'PNG', 0, position, pdfW, pdfH);
    heightLeft -= pageHeight;
    while (heightLeft > 0) {
      position = heightLeft - pdfH;
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', 0, position, pdfW, pdfH);
      heightLeft -= pageHeight;
    }
    pdf.save('dashboard-export.pdf');
    document.getElementById('exportTimestamp').textContent = 'Last export: PDF - ' + new Date().toLocaleString();
    showToast('PDF exported successfully');
  }).catch(err => {
    showToast('PDF export failed: ' + err.message);
  });
}
// PNG Export
function exportPNG() {
  showToast('Capturing PNG...');
  const dashboard = document.getElementById('dashboard');
  html2canvas(dashboard, {
    scale: 2,
    useCORS: true,
    backgroundColor: '#f0f2f5',
    logging: false,
    windowHeight: dashboard.scrollHeight,
  }).then(canvas => {
    const link = document.createElement('a');
    link.download = 'dashboard-screenshot.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
    document.getElementById('exportTimestamp').textContent = 'Last export: PNG - ' + new Date().toLocaleString();
    showToast('PNG exported successfully');
  }).catch(err => {
    showToast('PNG capture failed: ' + err.message);
  });
}
// HTML Snapshot Export
function exportHTML() {
  showToast('Exporting HTML snapshot...');
  const dashboardHTML = document.getElementById('dashboard').outerHTML;
  const styleSheets = Array.from(document.styleSheets).map(sheet => {
    try {
      return Array.from(sheet.cssRules || []).map(r => r.cssText).join('\n');
    } catch(e) { return ''; }
  }).join('\n');
  const snapshot = `<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>${styleSheets}</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"><\/script>
</head><body style="margin:0;background:#f0f2f5;">
${dashboardHTML}
<script>
document.querySelectorAll('.export-btn').forEach(b => { b.onclick = function(e) { e.preventDefault(); }; });
document.getElementById('exportTimestamp').textContent = 'Snapshot: ' + new Date().toLocaleString();
<\/script>
</body></html>`;
  const blob = new Blob([snapshot], { type: 'text/html' });
  const link = document.createElement('a');
  link.download = 'dashboard-snapshot.html';
  link.href = URL.createObjectURL(blob);
  link.click();
  URL.revokeObjectURL(link.href);
  document.getElementById('exportTimestamp').textContent = 'Last export: HTML - ' + new Date().toLocaleString();
  showToast('HTML snapshot exported');
}
// CSV Export
function exportCSV() {
  showToast('Generating CSV...');
  const rows = [['Month', 'Revenue', 'Users', 'Conversion Rate %', 'Churn Rate %', 'Baseline Revenue', 'Baseline Users']];
  months.forEach((m, i) => {
    rows.push([m, revenueData[i], usersData[i], conversionData[i], churnData[i], baselineRevenue[i], baselineUsers[i]]);
  });
  // Add KPI section
  rows.push(['', '', '', '', '', '', '']);
  rows.push(['KPI', 'Current', 'Baseline', 'Delta', 'Delta %']);
  const kpis = [
    ['Total Revenue', 41200, 37000],
    ['Active Users', 18400, 16300],
    ['Gross Margin', 71.3, 70.1],
    ['Conversion Rate', 4.4, 3.9],
    ['Churn Rate', 4.3, 4.0],
  ];
  kpis.forEach(k => {
    const d = computeDelta(k[1], k[2]);
    rows.push([k[0], k[1], k[2], d.val.toFixed(1), d.pct.toFixed(1) + '%']);
  });
  const csv = rows.map(r => r.join(',')).join('\n');
  const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.download = 'dashboard-data-' + new Date().toISOString().slice(0,10) + '.csv';
  link.href = URL.createObjectURL(blob);
  link.click();
  URL.revokeObjectURL(link.href);
  document.getElementById('exportTimestamp').textContent = 'Last export: CSV - ' + new Date().toLocaleString();
  showToast('CSV exported');
}
// Schedule
function toggleSchedule() {
  document.getElementById('schedulePanel').classList.toggle('visible');
  document.getElementById('scheduleOverlay').classList.toggle('visible');
}
function updateCron() {
  const freq = document.getElementById('schedFreq').value;
  const time = document.getElementById('schedTime').value;
  const day = document.getElementById('schedDay').value;
  const [h, m] = time.split(':');
  const dayMap = { monday: 1, tuesday: 2, wednesday: 3, thursday: 4, friday: 5, saturday: 6, sunday: 0 };
  let cron;
  if (freq === 'daily') cron = `${m} ${h} * * *`;
  else if (freq === 'weekly') cron = `${m} ${h} * * ${dayMap[day]}`;
  else cron = `${m} ${h} 1 * *`;
  document.getElementById('cronDisplay').textContent = cron;
}
document.getElementById('schedFreq').addEventListener('change', updateCron);
document.getElementById('schedDay').addEventListener('change', updateCron);
document.getElementById('schedTime').addEventListener('input', updateCron);
updateCron();
function saveSchedule() {
  const format = document.getElementById('schedFormat').value;
  const freq = document.getElementById('schedFreq').value;
  const time = document.getElementById('schedTime').value;
  const day = document.getElementById('schedDay').value;
  const tz = document.getElementById('schedTimezone').value;
  const email = document.getElementById('schedEmail').value;
  const narrative = document.getElementById('schedNarrative').value;
  const cron = document.getElementById('cronDisplay').textContent;
  const schedule = { format, freq, time, day, tz, email, narrative, cron };
  localStorage.setItem('dashboardSchedule', JSON.stringify(schedule));
  showToast(`Schedule saved: ${freq} at ${time} ${tz} as ${format.toUpperCase()}`);
  toggleSchedule();
  document.getElementById('exportTimestamp').textContent = `Schedule: ${freq} ${time} ${tz} | Cron: ${cron}`;
}
// Restore schedule if saved
try {
  const saved = JSON.parse(localStorage.getItem('dashboardSchedule'));
  if (saved) {
    document.getElementById('exportTimestamp').textContent = `Schedule: ${saved.freq} ${saved.time} ${saved.tz} | Cron: ${saved.cron}`;
  }
} catch(e) {}
// Brand preset: load from localStorage
try {
  const brandTitle = localStorage.getItem('dashboardBrandTitle');
  const brandColor = localStorage.getItem('dashboardBrandColor');
  if (brandTitle) { document.getElementById('brandTitle').value = brandTitle; document.querySelector('.brand-bar .logo h1').textContent = brandTitle; }
  if (brandColor) { document.getElementById('brandColor').value = brandColor; document.getElementById('brandBar').style.background = `linear-gradient(135deg, ${brandColor} 0%, #16213e 100%)`; }
} catch(e) {}
// Save brand on change
document.getElementById('brandTitle').addEventListener('change', function() { localStorage.setItem('dashboardBrandTitle', this.value); });
document.getElementById('brandColor').addEventListener('change', function() { localStorage.setItem('dashboardBrandColor', this.value); });
// Init
renderDashboard();
</script>
</body>
</html>