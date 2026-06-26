```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bento Grid Dashboard</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0a0a0f;
    color: #e4e4e7;
    padding: 24px;
    min-height: 100vh;
  }
  .dashboard {
    max-width: 1440px;
    margin: 0 auto;
  }
  h1 {
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #52525b;
    margin-bottom: 24px;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 16px;
    grid-auto-rows: 80px;
  }
  .card {
    background: linear-gradient(145deg, #14141a, #1a1a23);
    border: 1px solid #27272a;
    border-radius: 16px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    transition: border-color 0.2s, box-shadow 0.2s;
    overflow: hidden;
    position: relative;
  }
  .card:hover {
    border-color: #3f3f46;
    box-shadow: 0 0 0 1px rgba(168, 85, 247, 0.08);
  }
  .card .label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #71717a;
    margin-bottom: 8px;
  }
  .card .value {
    font-size: 32px;
    font-weight: 600;
    letter-spacing: -0.03em;
    color: #fafafa;
    line-height: 1;
  }
  .card .sub {
    font-size: 12px;
    color: #71717a;
    margin-top: 4px;
  }
  .card .unit { font-size: 14px; color: #52525b; margin-left: 2px; }
  .card .trend-up { color: #22c55e; }
  .card .trend-down { color: #ef4444; }
  .span-3 { grid-column: span 3; }
  .span-4 { grid-column: span 4; }
  .span-5 { grid-column: span 5; }
  .span-6 { grid-column: span 6; }
  .span-7 { grid-column: span 7; }
  .span-8 { grid-column: span 8; }
  .span-9 { grid-column: span 9; }
  .span-12 { grid-column: span 12; }
  .row-2 { grid-row: span 2; }
  .row-3 { grid-row: span 3; }
  .row-4 { grid-row: span 4; }
  .row-5 { grid-row: span 5; }
  .row-6 { grid-row: span 6; }
  .accent-purple { border-color: rgba(168, 85, 247, 0.15); }
  .accent-purple:hover { border-color: rgba(168, 85, 247, 0.35); }
  .accent-blue { border-color: rgba(59, 130, 246, 0.15); }
  .accent-blue:hover { border-color: rgba(59, 130, 246, 0.35); }
  .accent-green { border-color: rgba(34, 197, 94, 0.15); }
  .accent-green:hover { border-color: rgba(34, 197, 94, 0.35); }
  .accent-amber { border-color: rgba(245, 158, 11, 0.15); }
  .accent-amber:hover { border-color: rgba(245, 158, 11, 0.35); }
  .accent-rose { border-color: rgba(244, 63, 94, 0.15); }
  .accent-rose:hover { border-color: rgba(244, 63, 94, 0.35); }
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 999px;
    background: rgba(168, 85, 247, 0.1);
    color: #a78bfa;
    font-weight: 500;
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }
  .mini-chart {
    display: flex;
    align-items: flex-end;
    gap: 3px;
    height: 40px;
    margin-top: auto;
  }
  .mini-chart .bar {
    width: 8px;
    border-radius: 4px 4px 0 0;
    background: linear-gradient(to top, #3b3b44, #52525b);
    transition: background 0.2s;
  }
  .card:hover .mini-chart .bar { background: linear-gradient(to top, rgba(168,85,247,0.4), rgba(168,85,247,0.6)); }
  .mini-chart .bar.active { background: linear-gradient(to top, rgba(168,85,247,0.6), #a78bfa); }
  .card:hover .mini-chart .bar.active { background: linear-gradient(to top, #a78bfa, #c4b5fd); }
  .activity-dot {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 0;
    font-size: 13px;
    color: #a1a1aa;
  }
  .activity-dot .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .dot-purple { background: #a78bfa; }
  .dot-blue { background: #60a5fa; }
  .dot-green { background: #4ade80; }
  .dot-amber { background: #fbbf24; }
  .dot-rose { background: #fb7185; }
  .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #27272a;
    font-size: 13px;
  }
  .metric-row:last-child { border-bottom: none; }
  .metric-row .m-label { color: #a1a1aa; }
  .metric-row .m-value { color: #fafafa; font-weight: 500; }
  .progress-track {
    width: 100%;
    height: 4px;
    background: #27272a;
    border-radius: 999px;
    margin-top: 8px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #a78bfa, #7c3aed);
    transition: width 0.4s ease;
  }
  .map-placeholder {
    width: 100%;
    height: 100%;
    min-height: 120px;
    background: radial-gradient(circle at 30% 40%, #1e1e2a, #14141a);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #3f3f46;
    font-size: 12px;
    letter-spacing: 0.05em;
    position: relative;
    overflow: hidden;
  }
  .map-placeholder::before {
    content: '';
    position: absolute;
    width: 60%; height: 60%;
    border: 1px solid rgba(168,85,247,0.06);
    border-radius: 50%;
    top: 20%; left: 20%;
  }
  .map-placeholder::after {
    content: '';
    position: absolute;
    width: 30%; height: 30%;
    border: 1px solid rgba(168,85,247,0.04);
    border-radius: 50%;
    top: 35%; left: 35%;
  }
  .timeline-item {
    display: flex;
    gap: 12px;
    padding: 8px 0;
    position: relative;
  }
  .timeline-item::before {
    content: '';
    position: absolute;
    left: 3px; top: 20px;
    width: 2px; height: calc(100% - 20px);
    background: #27272a;
  }
  .timeline-item:last-child::before { display: none; }
  .timeline-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-top: 4px;
    flex-shrink: 0;
    position: relative;
    z-index: 1;
  }
  .timeline-content { font-size: 13px; }
  .timeline-content .t-time { color: #52525b; font-size: 11px; }
  .timeline-content .t-text { color: #d4d4d8; margin-top: 1px; }
  @media (max-width: 900px) {
    .grid { grid-template-columns: repeat(6, 1fr); gap: 12px; grid-auto-rows: 70px; }
    .span-3,.span-4,.span-5,.span-6,.span-7,.span-8,.span-9,.span-12 { grid-column: span 6; }
  }
  @media (max-width: 600px) {
    .grid { grid-template-columns: 1fr; gap: 10px; grid-auto-rows: auto; }
    .span-3,.span-4,.span-5,.span-6,.span-7,.span-8,.span-9,.span-12 { grid-column: 1; }
  }
</style>
</head>
<body>
<div class="dashboard">
  <h1>Bento Grid Dashboard</h1>
  <div class="grid">
    <div class="card span-3 row-2 accent-purple">
      <div class="card-header">
        <span class="label">Total Revenue</span>
        <span class="badge">+12.4%</span>
      </div>
      <div class="value">$48,295</div>
      <div class="sub">vs $42,940 last period</div>
      <div class="mini-chart">
        <div class="bar active" style="height:24px"></div>
        <div class="bar active" style="height:32px"></div>
        <div class="bar active" style="height:18px"></div>
        <div class="bar active" style="height:28px"></div>
        <div class="bar active" style="height:36px"></div>
        <div class="bar" style="height:20px"></div>
        <div class="bar" style="height:12px"></div>
      </div>
    </div>
    <div class="card span-3 row-2 accent-blue">
      <div class="card-header">
        <span class="label">Active Users</span>
        <span class="badge">+3.2%</span>
      </div>
      <div class="value">7,341</div>
      <div class="sub">2,892 online now</div>
      <div class="mini-chart">
        <div class="bar" style="height:10px"></div>
        <div class="bar" style="height:16px"></div>
        <div class="bar active" style="height:28px"></div>
        <div class="bar active" style="height:34px"></div>
        <div class="bar active" style="height:26px"></div>
        <div class="bar active" style="height:38px"></div>
        <div class="bar" style="height:20px"></div>
      </div>
    </div>
    <div class="card span-3 row-2 accent-green">
      <div class="card-header">
        <span class="label">Conversion</span>
        <span class="badge">+0.8%</span>
      </div>
      <div class="value">5.34<span class="unit">%</span></div>
      <div class="sub">target: 6.0%</div>
      <div class="progress-track"><div class="progress-fill" style="width:64%"></div></div>
      <div style="display:flex;justify-content:space-between;font-size:11px;color:#52525b;margin-top:4px">
        <span>0%</span><span>100%</span>
      </div>
    </div>
    <div class="card span-3 row-2 accent-amber">
      <div class="card-header">
        <span class="label">Avg. Session</span>
        <span class="badge">+1.6%</span>
      </div>
      <div class="value">4m 32s</div>
      <div class="sub">bounce rate: 31.2%</div>
      <div style="margin-top:8px;display:flex;gap:4px;flex-wrap:wrap">
        <span style="font-size:11px;padding:2px 6px;background:#27272a;border-radius:4px;color:#a1a1aa">M</span>
        <span style="font-size:11px;padding:2px 6px;background:#27272a;border-radius:4px;color:#a1a1aa">T</span>
        <span style="font-size:11px;padding:2px 6px;background:#27272a;border-radius:4px;color:#a1a1aa">W</span>
        <span style="font-size:11px;padding:2px 6px;background:rgba(168,85,247,0.15);border-radius:4px;color:#a78bfa">T</span>
        <span style="font-size:11px;padding:2px 6px;background:#27272a;border-radius:4px;color:#a1a1aa">F</span>
        <span style="font-size:11px;padding:2px 6px;background:#27272a;border-radius:4px;color:#a1a1aa">S</span>
        <span style="font-size:11px;padding:2px 6px;background:#27272a;border-radius:4px;color:#a1a1aa">S</span>
      </div>
    </div>
    <div class="card span-4 row-4 accent-purple">
      <div class="card-header">
        <span class="label">Traffic Sources</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;justify-content:center;gap:8px">
        <div class="metric-row">
          <span class="m-label">Organic Search</span>
          <span style="display:flex;align-items:center;gap:8px">
            <span style="width:70px;height:4px;background:#27272a;border-radius:999px;overflow:hidden">
              <span style="display:block;height:100%;width:65%;background:#a78bfa;border-radius:999px"></span>
            </span>
            <span class="m-value">42.3%</span>
          </span>
        </div>
        <div class="metric-row">
          <span class="m-label">Direct</span>
          <span style="display:flex;align-items:center;gap:8px">
            <span style="width:70px;height:4px;background:#27272a;border-radius:999px;overflow:hidden">
              <span style="display:block;height:100%;width:45%;background:#60a5fa;border-radius:999px"></span>
            </span>
            <span class="m-value">24.1%</span>
          </span>
        </div>
        <div class="metric-row">
          <span class="m-label">Social</span>
          <span style="display:flex;align-items:center;gap:8px">
            <span style="width:70px;height:4px;background:#27272a;border-radius:999px;overflow:hidden">
              <span style="display:block;height:100%;width:35%;background:#4ade80;border-radius:999px"></span>
            </span>
            <span class="m-value">18.6%</span>
          </span>
        </div>
        <div class="metric-row">
          <span class="m-label">Referral</span>
          <span style="display:flex;align-items:center;gap:8px">
            <span style="width:70px;height:4px;background:#27272a;border-radius:999px;overflow:hidden">
              <span style="display:block;height:100%;width:25%;background:#fbbf24;border-radius:999px"></span>
            </span>
            <span class="m-value">15.0%</span>
          </span>
        </div>
      </div>
    </div>
    <div class="card span-4 row-2 accent-blue">
      <div class="card-header">
        <span class="label">Geographic Distribution</span>
      </div>
      <div class="map-placeholder">
        <span style="position:relative;z-index:1;opacity:0.5">GEO MAP</span>
      </div>
    </div>
    <div class="card span-4 row-2 accent-amber">
      <div class="card-header">
        <span class="label">Recent Activity</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:0">
        <div class="activity-dot">
          <span class="dot dot-purple"></span>
          <span>New user registered</span>
          <span style="margin-left:auto;font-size:11px;color:#52525b">2m ago</span>
        </div>
        <div class="activity-dot">
          <span class="dot dot-blue"></span>
          <span>Order #2847 completed</span>
          <span style="margin-left:auto;font-size:11px;color:#52525b">8m ago</span>
        </div>
        <div class="activity-dot">
          <span class="dot dot-green"></span>
          <span>Payment received — $1,240</span>
          <span style="margin-left:auto;font-size:11px;color:#52525b">14m ago</span>
        </div>
        <div class="activity-dot">
          <span class="dot dot-amber"></span>
          <span>Server deployment finished</span>
          <span style="margin-left:auto;font-size:11px;color:#52525b">23m ago</span>
        </div>
        <div class="activity-dot">
          <span class="dot dot-rose"></span>
          <span>Flagged: unusual login attempt</span>
          <span style="margin-left:auto;font-size:11px;color:#52525b">31m ago</span>
        </div>
      </div>
    </div>
    <div class="card span-3 row-2 accent-rose">
      <div class="card-header">
        <span class="label">Churn Rate</span>
        <span class="badge">-2.1%</span>
      </div>
      <div class="value">4.2<span class="unit">%</span></div>
      <div class="sub">lowest in 6 months</div>
      <div style="display:flex;gap:6px;margin-top:8px">
        <span style="font-size:11px;padding:3px 8px;background:rgba(244,63,94,0.1);border-radius:6px;color:#fb7185;border:1px solid rgba(244,63,94,0.1)">J</span>
        <span style="font-size:11px;padding:3px 8px;background:rgba(244,63,94,0.1);border-radius:6px;color:#fb7185;border:1px solid rgba(244,63,94,0.1)">F</span>
        <span style="font-size:11px;padding:3px 8px;background:rgba(244,63,94,0.1);border-radius:6px;color:#fb7185;border:1px solid rgba(244,63,94,0.1)">M</span>
        <span style="font-size:11px;padding:3px 8px;background:rgba(244,63,94,0.1);border-radius:6px;color:#fb7185;border:1px solid rgba(244,63,94,0.1)">A</span>
        <span style="font-size:11px;padding:3px 8px;background:rgba(244,63,94,0.15);border-radius:6px;color:#f43f5e;border:1px solid rgba(244,63,94,0.2)">M</span>
        <span style="font-size:11px;padding:3px 8px;background:rgba(244,63,94,0.1);border-radius:6px;color:#fb7185;border:1px solid rgba(244,63,94,0.1)">J</span>
      </div>
    </div>
    <div class="card span-4 row-3 accent-green">
      <div class="card-header">
        <span class="label">Timeline</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:0;padding-left:4px">
        <div class="timeline-item">
          <span class="timeline-dot" style="background:#a78bfa"></span>
          <div class="timeline-content">
            <div class="t-time">09:42 AM</div>
            <div class="t-text">Deployed v3.2.1 to production — server health nominal</div>
          </div>
        </div>
        <div class="timeline-item">
          <span class="timeline-dot" style="background:#60a5fa"></span>
          <div class="timeline-content">
            <div class="t-time">08:15 AM</div>
            <div class="t-text">Database migration completed — 14s downtime</div>
          </div>
        </div>
        <div class="timeline-item">
          <span class="timeline-dot" style="background:#4ade80"></span>
          <div class="timeline-content">
            <div class="t-time">07:00 AM</div>
            <div class="t-text">Weekly report generated — revenue up 12.4%</div>
          </div>
        </div>
        <div class="timeline-item">
          <span class="timeline-dot" style="background:#fbbf24"></span>
          <div class="timeline-content">
            <div class="t-time">Yesterday</div>
            <div class="t-text">A/B test variant B reaches statistical significance</div>
          </div>
        </div>
      </div>
    </div>
    <div class="card span-5 row-3 accent-blue">
      <div class="card-header">
        <span class="label">Performance Overview</span>
        <span class="badge">Last 7 days</span>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:10px;justify-content:center">
        <div class="metric-row">
          <span class="m-label">Response Time (p95)</span>
          <span class="m-value">142ms <span class="trend-down" style="font-size:11px">-8ms</span></span>
        </div>
        <div class="metric-row">
          <span class="m-label">Error Rate</span>
          <span class="m-value">0.04<span class="unit">%</span> <span class="trend-down" style="font-size:11px">-0.02%</span></span>
        </div>
        <div class="metric-row">
          <span class="m-label">Throughput</span>
          <span class="m-value">2,847 req/s <span class="trend-up" style="font-size:11px">+312</span></span>
        </div>
        <div class="metric-row">
          <span class="m-label">Uptime</span>
          <span class="m-value">99.97<span class="unit">%</span></span>
        </div>
        <div class="metric-row">
          <span class="m-label">Cache Hit Ratio</span>
          <span class="m-value">87.3<span class="unit">%</span> <span class="trend-up" style="font-size:11px">+2.1%</span></span>
        </div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
```