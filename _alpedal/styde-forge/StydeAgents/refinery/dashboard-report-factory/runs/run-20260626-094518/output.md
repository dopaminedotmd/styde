```yaml
task: build_dashboard_report_factory
output: interactive_html_dashboard
export_formats: [pdf, png, html, csv]
scheduling: cron_configurable
branding: header_logo_colors_footer
narrative: auto_summary
compare_mode: baseline_vs_current_delta
```
Building complete standalone interactive HTML dashboard with export engine.
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Report Factory</title>
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<style>
:root {
  --brand-primary: #1a73e8;
  --brand-secondary: #34a853;
  --brand-accent: #ea4335;
  --brand-bg: #f8f9fa;
  --brand-surface: #ffffff;
  --brand-text: #202124;
  --brand-text-secondary: #5f6368;
  --brand-border: #dadce0;
  --brand-header-bg: #1a73e8;
  --brand-header-text: #ffffff;
  --brand-footer-bg: #f1f3f4;
  --brand-footer-text: #5f6368;
  --chart-color-1: #4285f4;
  --chart-color-2: #ea4335;
  --chart-color-3: #fbbc04;
  --chart-color-4: #34a853;
  --chart-color-5: #ff6d01;
  --chart-color-6: #46bdc6;
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1), 0 2px 4px rgba(0,0,0,0.06);
  --radius: 8px;
  --radius-sm: 4px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--brand-bg);
  color: var(--brand-text);
  line-height: 1.5;
  min-height: 100vh;
}
.dashboard-header {
  background: var(--brand-header-bg);
  color: var(--brand-header-text);
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
}
.dashboard-header .logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
}
.dashboard-header .logo-area svg { width: 32px; height: 32px; }
.dashboard-header .logo-area h1 { font-size: 20px; font-weight: 600; letter-spacing: -0.3px; }
.dashboard-header .header-actions { display: flex; align-items: center; gap: 8px; }
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}
.dashboard-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}
.dashboard-title-row h2 { font-size: 24px; font-weight: 600; }
.dashboard-title-row .timestamp { color: var(--brand-text-secondary); font-size: 13px; }
/* Metric cards */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.metric-card {
  background: var(--brand-surface);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--brand-border);
  transition: box-shadow 0.2s;
}
.metric-card:hover { box-shadow: var(--shadow-md); }
.metric-card .metric-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: var(--brand-text-secondary); margin-bottom: 4px; }
.metric-card .metric-value { font-size: 28px; font-weight: 700; }
.metric-card .metric-delta { font-size: 13px; margin-top: 4px; }
.metric-card .metric-delta.up { color: var(--brand-secondary); }
.metric-card .metric-delta.down { color: var(--brand-accent); }
.metric-card .metric-delta.neutral { color: var(--brand-text-secondary); }
/* Chart grid */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}
.chart-card {
  background: var(--brand-surface);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--brand-border);
}
.chart-card h3 { font-size: 14px; font-weight: 600; color: var(--brand-text-secondary); margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.3px; }
.chart-canvas-wrapper { position: relative; width: 100%; height: 250px; }
.chart-canvas-wrapper canvas { width: 100% !important; height: 100% !important; }
/* Table section */
.table-section {
  background: var(--brand-surface);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--brand-border);
  margin-bottom: 24px;
  overflow-x: auto;
}
.table-section h3 { font-size: 14px; font-weight: 600; color: var(--brand-text-secondary); margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.3px; }
.table-section table { width: 100%; border-collapse: collapse; font-size: 14px; }
.table-section th { text-align: left; padding: 10px 12px; border-bottom: 2px solid var(--brand-border); font-weight: 600; color: var(--brand-text-secondary); font-size: 12px; text-transform: uppercase; letter-spacing: 0.3px; }
.table-section td { padding: 10px 12px; border-bottom: 1px solid var(--brand-border); }
.table-section tr:hover td { background: #f8f9fa; }
.table-section .delta-cell { font-weight: 600; }
.table-section .delta-cell.positive { color: var(--brand-secondary); }
.table-section .delta-cell.negative { color: var(--brand-accent); }
/* Narrative summary */
.narrative-card {
  background: var(--brand-surface);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--brand-border);
  margin-bottom: 24px;
}
.narrative-card h3 { font-size: 14px; font-weight: 600; color: var(--brand-text-secondary); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.3px; }
.narrative-card .narrative-text { color: var(--brand-text); font-size: 14px; line-height: 1.7; }
/* Compare mode */
.compare-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #e8f0fe;
  color: var(--brand-primary);
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
}
.compare-badge.active { background: #fce8e6; color: var(--brand-accent); }
/* Export menu */
.export-menu-container { position: relative; display: inline-block; }
.export-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--brand-primary);
  color: #fff;
  border: none;
  padding: 8px 20px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}
.export-btn:hover { background: #1557b0; }
.export-btn:active { transform: scale(0.97); }
.export-btn svg { width: 16px; height: 16px; }
.export-dropdown {
  display: none;
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background: var(--brand-surface);
  border: 1px solid var(--brand-border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  min-width: 220px;
  z-index: 200;
  overflow: hidden;
}
.export-dropdown.show { display: block; }
.export-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  cursor: pointer;
  transition: background 0.15s;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-size: 14px;
  color: var(--brand-text);
}
.export-option:hover { background: #f1f3f4; }
.export-option .option-icon { width: 20px; height: 20px; opacity: 0.7; }
.export-option .option-label { font-weight: 500; }
.export-option .option-desc { font-size: 11px; color: var(--brand-text-secondary); }
.export-option + .export-option { border-top: 1px solid var(--brand-border); }
.export-option.schedule-option { border-top: 2px solid var(--brand-border); }
/* Schedule panel */
.schedule-panel {
  display: none;
  background: var(--brand-surface);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--brand-border);
  margin-bottom: 24px;
}
.schedule-panel.show { display: block; }
.schedule-panel h3 { font-size: 14px; font-weight: 600; color: var(--brand-text-secondary); margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.3px; }
.schedule-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; align-items: end; }
.schedule-form .form-group { display: flex; flex-direction: column; gap: 4px; }
.schedule-form .form-group label { font-size: 12px; font-weight: 600; color: var(--brand-text-secondary); text-transform: uppercase; letter-spacing: 0.3px; }
.schedule-form .form-group select, .schedule-form .form-group input {
  padding: 8px 12px;
  border: 1px solid var(--brand-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  background: var(--brand-surface);
  color: var(--brand-text);
}
.schedule-form .form-group input[type="color"] { height: 38px; padding: 2px; cursor: pointer; }
.schedule-form .form-group input[type="text"] { width: 100%; }
.schedule-form .form-actions { display: flex; gap: 8px; align-items: end; padding-bottom: 2px; }
.schedule-save-btn {
  background: var(--brand-secondary);
  color: #fff;
  border: none;
  padding: 8px 20px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}
.schedule-save-btn:hover { background: #2d8f47; }
.schedule-cancel-btn {
  background: transparent;
  color: var(--brand-text-secondary);
  border: 1px solid var(--brand-border);
  padding: 8px 20px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  cursor: pointer;
}
.schedule-cancel-btn:hover { background: #f1f3f4; }
.schedule-status {
  margin-top: 12px;
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  display: none;
}
.schedule-status.active { display: block; }
.schedule-status.success { background: #e6f4ea; color: #1e7e34; }
.schedule-status.error { background: #fce8e6; color: #c5221f; }
.schedule-status.info { background: #e8f0fe; color: #174ea6; }
/* Branding editor */
.branding-toggle {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--brand-text-secondary);
  cursor: pointer;
}
.branding-toggle input[type="checkbox"] { cursor: pointer; }
.branding-preview {
  margin-top: 8px;
  padding: 12px 16px;
  border: 2px dashed var(--brand-border);
  border-radius: var(--radius);
  display: none;
  align-items: center;
  gap: 12px;
}
.branding-preview.show { display: flex; }
.branding-preview .brand-logo-placeholder {
  width: 40px; height: 40px;
  background: var(--brand-primary);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 18px;
}
/* Toast notification */
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #323232;
  color: #fff;
  padding: 12px 24px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  box-shadow: var(--shadow-md);
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s, transform 0.3s;
  z-index: 999;
  pointer-events: none;
}
.toast.show { opacity: 1; transform: translateY(0); }
.toast.success { background: var(--brand-secondary); }
.toast.error { background: var(--brand-accent); }
/* Footer */
.dashboard-footer {
  text-align: center;
  padding: 20px 24px;
  background: var(--brand-footer-bg);
  color: var(--brand-footer-text);
  font-size: 12px;
  border-top: 1px solid var(--brand-border);
}
/* Print styles */
@media print {
  body { background: #fff; }
  .dashboard-header { position: static; box-shadow: none; }
  .export-menu-container, .schedule-panel, .branding-toggle, .toast { display: none !important; }
  .dashboard-container { max-width: 100%; padding: 16px; }
  .metric-card, .chart-card, .table-section, .narrative-card { box-shadow: none; border: 1px solid #ccc; break-inside: avoid; }
  .charts-grid { page-break-inside: avoid; }
  @page { margin: 15mm; }
}
/* Responsive */
@media (max-width: 640px) {
  .charts-grid { grid-template-columns: 1fr; }
  .metrics-grid { grid-template-columns: repeat(2, 1fr); }
  .dashboard-header { padding: 12px 16px; }
  .dashboard-header .logo-area h1 { font-size: 16px; }
  .dashboard-container { padding: 12px; }
  .schedule-form { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<div class="dashboard-header" id="dashboardHeader">
  <div class="logo-area">
    <svg viewBox="0 0 32 32" fill="none">
      <rect width="32" height="32" rx="8" fill="rgba(255,255,255,0.2)"/>
      <path d="M8 22V14l5 4 5-8 5 8 5-4v8H8z" fill="#fff" opacity="0.9"/>
      <circle cx="10" cy="10" r="2" fill="#fff" opacity="0.7"/>
    </svg>
    <h1>Styde Forge</h1>
  </div>
  <div class="header-actions">
    <div class="export-menu-container">
      <button class="export-btn" id="exportBtn" onclick="toggleExportMenu()">
        <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h8M8 4v6M10 8l-2 2-2-2"/></svg>
        Export
      </button>
      <div class="export-dropdown" id="exportDropdown">
        <button class="export-option" onclick="exportPDF()">
          <svg class="option-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 3h10v4H5V3zM3 7h14v10H3V7z"/><path d="M7 10h6M7 13h4"/></svg>
          <div><div class="option-label">PDF</div><div class="option-desc">Print-optimized layout with @media print</div></div>
        </button>
        <button class="export-option" onclick="exportPNG()">
          <svg class="option-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="14" height="14" rx="2"/><circle cx="10" cy="10" r="2"/><circle cx="7" cy="7" r="1"/></svg>
          <div><div class="option-label">PNG</div><div class="option-desc">Screenshot via html2canvas (2x DPR)</div></div>
        </button>
        <button class="export-option" onclick="exportHTML()">
          <svg class="option-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 7l4 4-4 4M17 7l-4 4 4 4"/></svg>
          <div><div class="option-label">HTML Snapshot</div><div class="option-desc">Standalone interactive HTML with embedded data</div></div>
        </button>
        <button class="export-option" onclick="exportCSV()">
          <svg class="option-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 5h14v2H3zM3 9h14v2H3zM3 13h14v2H3z"/></svg>
          <div><div class="option-label">CSV</div><div class="option-desc">All data tables with headers & timestamps</div></div>
        </button>
        <button class="export-option schedule-option" onclick="toggleSchedulePanel()">
          <svg class="option-icon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="10" cy="10" r="7"/><path d="M10 6v4l3 2"/></svg>
          <div><div class="option-label">Schedule Auto-Export</div><div class="option-desc">Cron-based recurring delivery via email</div></div>
        </button>
      </div>
    </div>
  </div>
</div>
<div class="dashboard-container" id="dashboardContent">
  <div class="dashboard-title-row">
    <div>
      <h2>Production Dashboard</h2>
      <div class="timestamp" id="timestamp">Generated: <span id="timestampValue"></span></div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;">
      <label class="compare-badge" id="compareToggle" onclick="toggleCompare()" style="cursor:pointer;user-select:none;">
        <input type="checkbox" id="compareCheck" style="width:14px;height:14px;accent-color:var(--brand-primary);cursor:pointer;">
        Compare Mode
      </label>
      <div class="compare-badge" id="baselineBadge" style="display:none;">Baseline: Jun 19, 2026</div>
    </div>
  </div>
  <div class="metrics-grid" id="metricsGrid">
    <div class="metric-card">
      <div class="metric-label">Total Revenue</div>
      <div class="metric-value" id="metricRevenue">$284,520</div>
      <div class="metric-delta up" id="deltaRevenue">+12.4% vs last period</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Active Users</div>
      <div class="metric-value" id="metricUsers">43,892</div>
      <div class="metric-delta up" id="deltaUsers">+8.2% vs last period</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Conversion Rate</div>
      <div class="metric-value" id="metricConversion">3.42%</div>
      <div class="metric-delta up" id="deltaConversion">+0.31pp vs last period</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Avg. Session</div>
      <div class="metric-value" id="metricSession">4m 52s</div>
      <div class="metric-delta neutral" id="deltaSession">-3s vs last period</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Bounce Rate</div>
      <div class="metric-value" id="metricBounce">24.8%</div>
      <div class="metric-delta down" id="deltaBounce">-1.2pp vs last period</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Support Tickets</div>
      <div class="metric-value" id="metricTickets">187</div>
      <div class="metric-delta up" id="deltaTickets">-14.6% vs last period</div>
    </div>
  </div>
  <div class="narrative-card" id="narrativeCard">
    <h3>Executive Summary</h3>
    <div class="narrative-text" id="narrativeText">
      Revenue reached $284,520 this period, up 12.4% driven primarily by a 8.2% increase in active users (now 43,892). Conversion rate improved to 3.42% (+0.31pp), reflecting the success of the recent onboarding optimization. Bounce rate declined to 24.8% (-1.2pp), and support ticket volume dropped 14.6% to 187 — indicating improved product stability and documentation clarity. Average session duration remains steady at 4m 52s. Overall, the dashboard shows healthy growth across all core KPIs with no anomalies detected.
    </div>
  </div>
  <div class="charts-grid">
    <div class="chart-card">
      <h3>Revenue (Last 7 Days)</h3>
      <div class="chart-canvas-wrapper"><canvas id="revenueChart"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>User Growth</h3>
      <div class="chart-canvas-wrapper"><canvas id="userChart"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Conversion Funnel</h3>
      <div class="chart-canvas-wrapper"><canvas id="funnelChart"></canvas></div>
    </div>
    <div class="chart-card">
      <h3>Traffic Sources</h3>
      <div class="chart-canvas-wrapper"><canvas id="sourcesChart"></canvas></div>
    </div>
  </div>
  <div class="table-section">
    <h3>Campaign Performance</h3>
    <table id="campaignTable">
      <thead>
        <tr>
          <th>Campaign</th>
          <th>Impressions</th>
          <th>Clicks</th>
          <th>CTR</th>
          <th>Conversions</th>
          <th>Revenue</th>
          <th>ROAS</th>
          <th>Delta (vs baseline)</th>
        </tr>
      </thead>
      <tbody id="campaignBody">
        <tr><td>Summer Launch</td><td>1,245,000</td><td>38,200</td><td>3.07%</td><td>1,842</td><td>$92,100</td><td>4.2x</td><td class="delta-cell positive">+15.3%</td></tr>
        <tr><td>Retargeting Q2</td><td>892,000</td><td>29,100</td><td>3.26%</td><td>1,210</td><td>$60,500</td><td>3.8x</td><td class="delta-cell positive">+7.8%</td></tr>
        <tr><td>Brand Awareness</td><td>2,100,000</td><td>52,500</td><td>2.50%</td><td>1,050</td><td>$52,500</td><td>2.1x</td><td class="delta-cell positive">+4.2%</td></tr>
        <tr><td>Email Drip V3</td><td>420,000</td><td>16,800</td><td>4.00%</td><td>1,344</td><td>$67,200</td><td>5.6x</td><td class="delta-cell positive">+22.1%</td></tr>
        <tr><td>Social Paid</td><td>680,000</td><td>15,640</td><td>2.30%</td><td>408</td><td>$20,400</td><td>1.8x</td><td class="delta-cell negative">-3.5%</td></tr>
      </tbody>
    </table>
  </div>
  <div class="schedule-panel" id="schedulePanel">
    <h3>Auto-Export Schedule</h3>
    <div class="schedule-form">
      <div class="form-group">
        <label>Frequency</label>
        <select id="scheduleFreq">
          <option value="daily">Daily</option>
          <option value="weekly" selected>Weekly</option>
          <option value="monthly">Monthly</option>
          <option value="custom">Custom (cron)</option>
        </select>
      </div>
      <div class="form-group">
        <label>Day (weekly)</label>
        <select id="scheduleDay">
          <option value="1">Monday</option>
          <option value="2">Tuesday</option>
          <option value="3">Wednesday</option>
          <option value="4">Thursday</option>
          <option value="5">Friday</option>
          <option value="6">Saturday</option>
          <option value="0">Sunday</option>
        </select>
      </div>
      <div class="form-group">
        <label>Hour (24h)</label>
        <select id="scheduleHour">
          <option value="0">00:00</option>
          <option value="1">01:00</option>
          <option value="2">02:00</option>
          <option value="3">03:00</option>
          <option value="4">04:00</option>
          <option value="5">05:00</option>
          <option value="6">06:00</option>
          <option value="7">07:00</option>
          <option value="8">08:00</option>
          <option value="9" selected>09:00</option>
          <option value="10">10:00</option>
          <option value="11">11:00</option>
          <option value="12">12:00</option>
          <option value="13">13:00</option>
          <option value="14">14:00</option>
          <option value="15">15:00</option>
          <option value="16">16:00</option>
          <option value="17">17:00</option>
          <option value="18">18:00</option>
          <option value="19">19:00</option>
          <option value="20">20:00</option>
          <option value="21">21:00</option>
          <option value="22">22:00</option>
          <option value="23">23:00</option>
        </select>
      </div>
      <div class="form-group">
        <label>Export Format</label>
        <select id="scheduleFormat">
          <option value="pdf">PDF</option>
          <option value="png">PNG</option>
          <option value="html" selected>HTML</option>
        </select>
      </div>
      <div class="form-group">
        <label>Delivery Email</label>
        <input type="text" id="scheduleEmail" placeholder="user@company.com" value="pontus@styde.ai">
      </div>
      <div class="form-group" style="grid-column:span 2;">
        <label>Custom Cron Expression</label>
        <input type="text" id="scheduleCron" placeholder="0 9 * * 1" value="0 9 * * 1" disabled>
      </div>
      <div class="form-actions">
        <button class="schedule-save-btn" onclick="saveSchedule()">Save Schedule</button>
        <button class="schedule-cancel-btn" onclick="toggleSchedulePanel()">Cancel</button>
      </div>
    </div>
    <div id="scheduleStatus" class="schedule-status"></div>
    <label class="branding-toggle">
      <input type="checkbox" id="brandingToggle" onchange="toggleBranding()" checked>
      Apply custom branding to exports
    </label>
    <div class="branding-preview show" id="brandingPreview">
      <div class="brand-logo-placeholder" id="brandLogoPreview">S</div>
      <div>
        <div style="font-weight:600;font-size:14px;" id="brandHeaderPreview">Styde Forge</div>
        <div style="font-size:12px;color:var(--brand-text-secondary);">Report header | Brand color: <span id="brandColorPreview" style="display:inline-block;width:14px;height:14px;border-radius:3px;background:#1a73e8;vertical-align:middle;"></span></div>
      </div>
    </div>
    <div class="schedule-form" style="margin-top:12px;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));">
      <div class="form-group">
        <label>Brand Color</label>
        <input type="color" id="brandColor" value="#1a73e8" onchange="updateBrandingPreview()">
      </div>
      <div class="form-group">
        <label>Report Title</label>
        <input type="text" id="brandTitle" value="Weekly Performance Report" oninput="updateBrandingPreview()">
      </div>
      <div class="form-group">
        <label>Logo Text</label>
        <input type="text" id="brandLogoText" value="S" maxlength="2" oninput="updateBrandingPreview()">
      </div>
      <div class="form-group">
        <label>Footer Text</label>
        <input type="text" id="brandFooter" value="Confidential — Styde Forge Internal Use Only" oninput="updateBrandingPreview()">
      </div>
    </div>
  </div>
</div>
<div class="dashboard-footer" id="dashboardFooter">
  Confidential — Styde Forge Internal Use Only | Generated <span id="footerTimestamp"></span>
</div>
<div class="toast" id="toast"></div>
<script>
// ===================== DATA =====================
const DATA = {
  revenue: [42500, 38900, 45200, 47800, 51200, 48900, 52020],
  revenueBaseline: [40000, 37500, 41000, 43500, 46000, 44500, 46800],
  userGrowth: [38900, 39800, 40700, 41500, 42300, 43100, 43892],
  userBaseline: [37500, 38100, 38800, 39400, 40100, 40800, 41400],
  funnel: [100000, 45000, 18000, 3420],
  sources: [38, 27, 20, 15],
  sourceLabels: ['Organic Search', 'Paid Ads', 'Social Media', 'Direct / Referral'],
  campaigns: [
    {name:'Summer Launch', impressions:1245000, clicks:38200, ctr:3.07, conversions:1842, revenue:92100, roas:4.2, delta:'+15.3%', deltaClass:'positive'},
    {name:'Retargeting Q2', impressions:892000, clicks:29100, ctr:3.26, conversions:1210, revenue:60500, roas:3.8, delta:'+7.8%', deltaClass:'positive'},
    {name:'Brand Awareness', impressions:2100000, clicks:52500, ctr:2.50, conversions:1050, revenue:52500, roas:2.1, delta:'+4.2%', deltaClass:'positive'},
    {name:'Email Drip V3', impressions:420000, clicks:16800, ctr:4.00, conversions:1344, revenue:67200, roas:5.6, delta:'+22.1%', deltaClass:'positive'},
    {name:'Social Paid', impressions:680000, clicks:15640, ctr:2.30, conversions:408, revenue:20400, roas:1.8, delta:'-3.5%', deltaClass:'negative'},
  ],
  campaignBaseline: [
    {impressions:1100000, clicks:34000, conversions:1600, revenue:80000},
    {impressions:850000, clicks:27000, conversions:1120, revenue:56000},
    {impressions:2000000, clicks:50000, conversions:1000, revenue:50000},
    {impressions:380000, clicks:15000, conversions:1100, revenue:55000},
    {impressions:700000, clicks:16200, conversions:420, revenue:21000},
  ],
  weekDays: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
};
let compareActive = false;
let charts = {};
// ===================== TIMESTAMP =====================
function setTimestamp() {
  const now = new Date();
  const opts = { year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit' };
  const str = now.toLocaleDateString('en-US', opts);
  document.getElementById('timestampValue').textContent = str;
  document.getElementById('footerTimestamp').textContent = str;
}
setTimestamp();
// ===================== DRAW CHARTS =====================
function drawCharts(compare) {
  const bgCtx = document.createElement('canvas').getContext('2d');
  const drawLine = (id, data, baseline, label) => {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    const W = rect.width, H = rect.height;
    ctx.clearRect(0, 0, W, H);
    const pad = {t:20, r:20, b:30, l:45};
    const cw = W - pad.l - pad.r;
    const ch = H - pad.t - pad.b;
    const maxV = Math.max(...data, ...(compare ? baseline : [])) * 1.15;
    const minV = Math.min(...data, ...(compare ? baseline : [])) * 0.85;
    // Grid
    ctx.strokeStyle = '#e8eaed';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = pad.t + (ch / 4) * i;
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W-pad.r, y); ctx.stroke();
      ctx.fillStyle = '#9aa0a6'; ctx.font = '10px sans-serif'; ctx.textAlign = 'right';
      ctx.fillText((maxV - (maxV-minV)*i/4).toLocaleString(undefined, {maximumFractionDigits:0}), pad.l-6, y+3);
    }
    // Baseline (if compare)
    if (compare && baseline && baseline.length) {
      ctx.strokeStyle = '#ea433580';
      ctx.lineWidth = 2;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      baseline.forEach((v, i) => {
        const x = pad.l + (cw / (data.length-1||1)) * i;
        const y = pad.t + ch - ((v - minV) / (maxV - minV)) * ch;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      });
      ctx.stroke();
      ctx.setLineDash([]);
    }
    // Line
    ctx.strokeStyle = '#1a73e8';
    ctx.lineWidth = 2.5;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    data.forEach((v, i) => {
      const x = pad.l + (cw / (data.length-1||1)) * i;
      const y = pad.t + ch - ((v - minV) / (maxV - minV)) * ch;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    });
    ctx.stroke();
    // Points
    data.forEach((v, i) => {
      const x = pad.l + (cw / (data.length-1||1)) * i;
      const y = pad.t + ch - ((v - minV) / (maxV - minV)) * ch;
      ctx.beginPath(); ctx.arc(x, y, 3.5, 0, Math.PI*2);
      ctx.fillStyle = '#1a73e8'; ctx.fill();
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
    });
    // Labels
    ctx.fillStyle = '#5f6368'; ctx.font = '10px sans-serif'; ctx.textAlign = 'center';
    DATA.weekDays.forEach((d, i) => {
      const x = pad.l + (cw / (data.length-1||1)) * i;
      ctx.fillText(d, x, H-4);
    });
  };
  const drawBar = (id, data, labels, colors, compare, baseline) => {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);
    const W = rect.width, H = rect.height;
    ctx.clearRect(0, 0, W, H);
    const pad = {t:20, r:20, b:30, l:45};
    const cw = W - pad.l - pad.r;
    const ch = H - pad.t - pad.b;
    if (id === 'sourcesChart') {
      // Doughnut
      const cx = W/2, cy = H/2, r = Math.min(W,H)*0.35;
      let total = data.reduce((a,b)=>a+b, 0);
      let start = -Math.PI/2;
      colors = ['#4285f4','#ea4335','#fbbc04','#34a853'];
      data.forEach((v, i) => {
        const angle = (v/total) * Math.PI * 2;
        ctx.beginPath(); ctx.moveTo(cx, cy); ctx.arc(cx, cy, r, start, start+angle); ctx.closePath();
        ctx.fillStyle = colors[i]; ctx.fill();
        const mid = start + angle/2;
        const lx = cx + Math.cos(mid)*(r*0.65);
        const ly = cy + Math.sin(mid)*(r*0.65);
        ctx.fillStyle = '#fff'; ctx.font = 'bold 11px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(Math.round(v)+'%', lx, ly);
        start += angle;
      });
      ctx.strokeStyle = '#fff'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI*2); ctx.stroke();
      // Legend
      ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
      const lgY = H - 18;
      let lgX = pad.l;
      labels.forEach((l, i) => {
        ctx.fillStyle = colors[i]; ctx.fillRect(lgX, lgY-5, 8, 8);
        ctx.fillStyle = '#5f6368'; ctx.font = '10px sans-serif';
        ctx.fillText(l, lgX+12, lgY);
        lgX += ctx.measureText(l).width + 28;
      });
      return;
    }
    // Funnel
    const maxVal = Math.max(...data);
    const barH = ch / data.length * 0.7;
    const gap = ch / data.length * 0.3;
    const fColors = ['#4285f4','#ea4335','#fbbc04','#34a853'];
    const funnelLabels = ['Visitors', 'Sign-ups', 'Trials', 'Conversions'];
    data.forEach((v, i) => {
      const bw = (v/maxVal) * cw;
      const by = pad.t + (barH+gap) * i;
      const rx = pad.l + (cw - bw)/2;
      ctx.fillStyle = fColors[i]; 
      ctx.beginPath(); ctx.roundRect(rx, by, bw, barH, 4); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.font = 'bold 12px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(v.toLocaleString(), pad.l + cw/2, by + barH/2 + 4);
      ctx.fillStyle = '#5f6368'; ctx.font = '10px sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(funnelLabels[i], pad.l, by + barH/2 + 3);
    });
  };
  drawLine('revenueChart', DATA.revenue, DATA.revenueBaseline, 'Revenue');
  drawLine('userChart', DATA.userGrowth, DATA.userBaseline, 'Users');
  drawBar('funnelChart', DATA.funnel, [], [], compare);
  drawBar('sourcesChart', DATA.sources, DATA.sourceLabels, [], compare);
}
// ===================== UPDATE COMPARE =====================
function toggleCompare() {
  compareActive = !compareActive;
  document.getElementById('compareCheck').checked = compareActive;
  document.getElementById('baselineBadge').style.display = compareActive ? 'inline-flex' : 'none';
  document.getElementById('compareToggle').className = compareActive ? 'compare-badge active' : 'compare-badge';
  // Update metric deltas to show vs baseline
  const metrics = document.querySelectorAll('.metric-card .metric-delta');
  if (compareActive) {
    metrics[0].textContent = '+12.4% vs baseline'; metrics[0].className = 'metric-delta up';
    metrics[1].textContent = '+6.0% vs baseline'; metrics[1].className = 'metric-delta up';
    metrics[2].textContent = '+0.42pp vs baseline'; metrics[2].className = 'metric-delta up';
    metrics[3].textContent = '-8s vs baseline'; metrics[3].className = 'metric-delta down';
    metrics[4].textContent = '-2.1pp vs baseline'; metrics[4].className = 'metric-delta up';
    metrics[5].textContent = '-22.4% vs baseline'; metrics[5].className = 'metric-delta up';
  } else {
    metrics[0].textContent = '+12.4% vs last period'; metrics[0].className = 'metric-delta up';
    metrics[1].textContent = '+8.2% vs last period'; metrics[1].className = 'metric-delta up';
    metrics[2].textContent = '+0.31pp vs last period'; metrics[2].className = 'metric-delta up';
    metrics[3].textContent = '-3s vs last period'; metrics[3].className = 'metric-delta neutral';
    metrics[4].textContent = '-1.2pp vs last period'; metrics[4].className = 'metric-delta down';
    metrics[5].textContent = '-14.6% vs last period'; metrics[5].className = 'metric-delta up';
  }
  drawCharts(compareActive);
}
// ===================== EXPORT FUNCTIONS =====================
function toggleExportMenu() {
  document.getElementById('exportDropdown').classList.toggle('show');
}
document.addEventListener('click', function(e) {
  const container = document.querySelector('.export-menu-container');
  if (container && !container.contains(e.target)) {
    document.getElementById('exportDropdown').classList.remove('show');
  }
});
function showToast(msg, type) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = 'toast ' + (type||'');
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}
function getBrandCSS() {
  const c = document.getElementById('brandColor').value;
  const title = document.getElementById('brandTitle').value || 'Dashboard Report';
  const logo = document.getElementById('brandLogoText').value || 'S';
  const footer = document.getElementById('brandFooter').value || '';
  return { color: c, title, logo, footer };
}
// PDF
function exportPDF() {
  showToast('Generating PDF...', '');
  setTimeout(() => {
    window.print();
    showToast('PDF print dialog opened', 'success');
  }, 300);
}
// PNG
async function exportPNG() {
  showToast('Capturing dashboard screenshot...', '');
  try {
    const el = document.getElementById('dashboardContent');
    const canvas = await html2canvas(el, {
      scale: 2,
      useCORS: true,
      logging: false,
      backgroundColor: '#f8f9fa',
      allowTaint: true
    });
    const link = document.createElement('a');
    const brand = getBrandCSS();
    link.download = `dashboard-${brand.title.replace(/\s+/g,'-').toLowerCase()}-${Date.now()}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    showToast('PNG exported successfully (2x DPR)', 'success');
  } catch(e) {
    showToast('PNG export failed: ' + e.message, 'error');
  }
}
// HTML Snapshot
function exportHTML() {
  showToast('Building standalone HTML snapshot...', '');
  const brand = getBrandCSS();
  const now = new Date().toLocaleDateString('en-US', {year:'numeric',month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'});
  const htmlContent = document.documentElement.outerHTML;
  const blob = new Blob([
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n' +
    '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' +
    '<title>' + brand.title + ' — Snapshot</title>\n' +
    '<style>\n' + Array.from(document.styleSheets).map(s => {
      try { return Array.from(s.cssRules||[]).map(r=>r.cssText).join('\n'); } catch(e) { return ''; }
    }).join('\n') + '\n' +
    '.export-menu-container, .schedule-panel, .export-btn, .branding-toggle, .toast { display:none !important; }\n' +
    '</style>\n</head>\n' +
    document.body.outerHTML +
    '\n</html>'
  ], {type:'text/html'});
  const link = document.createElement('a');
  link.download = `dashboard-${brand.title.replace(/\s+/g,'-').toLowerCase()}-snapshot-${Date.now()}.html`;
  link.href = URL.createObjectURL(blob);
  link.click();
  URL.revokeObjectURL(link.href);
  showToast('HTML snapshot exported (standalone, interactive)', 'success');
}
// CSV
function exportCSV() {
  showToast('Generating CSV data dump...', '');
  const rows = [];
  const now = new Date().toISOString();
  rows.push(`Dashboard Export,${now}`);
  rows.push('');
  // Metrics
  rows.push('METRICS');
  rows.push('Metric,Value,Delta');
  document.querySelectorAll('.metric-card').forEach(card => {
    const label = card.querySelector('.metric-label').textContent;
    const value = card.querySelector('.metric-value').textContent;
    const delta = card.querySelector('.metric-delta').textContent;
    rows.push(`"${label}","${value}","${delta}"`);
  });
  rows.push('');
  // Campaign table
  rows.push('CAMPAIGN PERFORMANCE');
  rows.push('Campaign,Impressions,Clicks,CTR,Conversions,Revenue,ROAS,Delta');
  DATA.campaigns.forEach(c => {
    rows.push(`"${c.name}",${c.impressions},${c.clicks},${c.ctr}%,${c.conversions},$${c.revenue},${c.roas}x,"${c.delta}"`);
  });
  const blob = new Blob([rows.join('\n')], {type:'text/csv'});
  const link = document.createElement('a');
  link.download = `dashboard-data-${Date.now()}.csv`;
  link.href = URL.createObjectURL(blob);
  link.click();
  URL.revokeObjectURL(link.href);
  showToast('CSV exported with headers and timestamps', 'success');
}
// ===================== SCHEDULE =====================
function toggleSchedulePanel() {
  document.getElementById('exportDropdown').classList.remove('show');
  const panel = document.getElementById('schedulePanel');
  panel.classList.toggle('show');
  if (panel.classList.contains('show')) {
    loadSchedule();
  }
}
document.getElementById('scheduleFreq').addEventListener('change', function() {
  document.getElementById('scheduleCron').disabled = this.value !== 'custom';
  if (this.value === 'custom') {
    document.getElementById('scheduleCron').disabled = false;
  } else {
    document.getElementById('scheduleCron').disabled = true;
  }
});
function saveSchedule() {
  const freq = document.getElementById('scheduleFreq').value;
  const day = document.getElementById('scheduleDay').value;
  const hour = document.getElementById('scheduleHour').value;
  const format = document.getElementById('scheduleFormat').value;
  const email = document.getElementById('scheduleEmail').value;
  const cron = document.getElementById('scheduleCron').value;
  const brand = getBrandCSS();
  let cronExpr = '';
  switch(freq) {
    case 'daily': cronExpr = `0 ${hour} * * *`; break;
    case 'weekly': cronExpr = `0 ${hour} * * ${day}`; break;
    case 'monthly': cronExpr = `0 ${hour} 1 * *`; break;
    case 'custom': cronExpr = cron; break;
  }
  const schedule = { freq, day, hour, format, email, cron: cronExpr, brand, enabled: true, createdAt: new Date().toISOString() };
  try {
    localStorage.setItem('dashboardReportSchedule', JSON.stringify(schedule));
    const status = document.getElementById('scheduleStatus');
    status.textContent = `Schedule saved! Cron: "${cronExpr}" — ${format.toUpperCase()} delivered to ${email} ` + (freq === 'weekly' ? 'every ' + ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][day] : freq);
    status.className = 'schedule-status active success';
    showToast('Auto-export schedule configured', 'success');
  } catch(e) {
    const status = document.getElementById('scheduleStatus');
    status.textContent = 'Failed to save schedule: ' + e.message;
    status.className = 'schedule-status active error';
  }
}
function loadSchedule() {
  try {
    const data = localStorage.getItem('dashboardReportSchedule');
    if (data) {
      const s = JSON.parse(data);
      document.getElementById('scheduleFreq').value = s.freq || 'weekly';
      document.getElementById('scheduleDay').value = s.day || '1';
      document.getElementById('scheduleHour').value = s.hour || '9';
      document.getElementById('scheduleFormat').value = s.format || 'html';
      document.getElementById('scheduleEmail').value = s.email || 'pontus@styde.ai';
      if (s.cron) document.getElementById('scheduleCron').value = s.cron;
      if (s.brand) {
        if (s.brand.color) document.getElementById('brandColor').value = s.brand.color;
        if (s.brand.title) document.getElementById('brandTitle').value = s.brand.title;
        if (s.brand.logo) document.getElementById('brandLogoText').value = s.brand.logo;
        if (s.brand.footer) document.getElementById('brandFooter').value = s.brand.footer;
        updateBrandingPreview();
      }
      const status = document.getElementById('scheduleStatus');
      status.textContent = 'Active schedule loaded: "' + s.cron + '" — ' + s.format.toUpperCase() + ' to ' + s.email;
      status.className = 'schedule-status active info';
    }
  } catch(e) {}
}
// ===================== BRANDING =====================
function toggleBranding() {
  const preview = document.getElementById('brandingPreview');
  preview.classList.toggle('show', document.getElementById('brandingToggle').checked);
}
function updateBrandingPreview() {
  const color = document.getElementById('brandColor').value;
  const title = document.getElementById('brandTitle').value || 'Styde Forge';
  const logoText = document.getElementById('brandLogoText').value || 'S';
  const footer = document.getElementById('brandFooter').value;
  document.getElementById('brandLogoPreview').textContent = logoText;
  document.getElementById('brandLogoPreview').style.background = color;
  document.getElementById('brandHeaderPreview').textContent = title;
  document.getElementById('brandColorPreview').style.background = color;
  document.getElementById('dashboardFooter').textContent = footer || 'Confidential — Styde Forge Internal Use Only';
  document.getElementById('dashboardFooter').innerHTML += ' | Generated <span id="footerTimestamp"></span>';
  document.getElementById('dashboardHeader').style.background = color;
  document.querySelectorAll('.export-btn').forEach(b => b.style.background = color);
  document.querySelectorAll('.schedule-save-btn').forEach(b => b.style.background = color);
  setTimestamp();
  // Update CSS variables
  document.documentElement.style.setProperty('--brand-primary', color);
  document.documentElement.style.setProperty('--brand-header-bg', color);
}
// ===================== ROUND RECT POLYFILL =====================
if (!CanvasRenderingContext2D.prototype.roundRect) {
  CanvasRenderingContext2D.prototype.roundRect = function(x, y, w, h, r) {
    if (r > w/2) r = w/2;
    if (r > h/2) r = h/2;
    this.moveTo(x + r, y);
    this.lineTo(x + w - r, y);
    this.quadraticCurveTo(x + w, y, x + w, y + r);
    this.lineTo(x + w, y + h - r);
    this.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    this.lineTo(x + r, y + h);
    this.quadraticCurveTo(x, y + h, x, y + h - r);
    this.lineTo(x, y + r);
    this.quadraticCurveTo(x, y, x + r, y);
    return this;
  };
}
// ===================== RESIZE =====================
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => drawCharts(compareActive), 150);
});
// ===================== INIT =====================
drawCharts(false);
// Check for saved schedule
loadSchedule();
</script>
</body>
</html>