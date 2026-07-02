Ai Copilot Query Panel - Complete HTML Dashboard
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Copilot Query Panel</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0a0e17;color:#e1e7f0;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:1fr 400px;grid-template-rows:auto 1fr auto;height:100vh;gap:0}
.context-bar{grid-column:1/-1;background:rgba(15,23,42,0.95);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid rgba(56,189,248,0.15);padding:10px 20px;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.context-chip{display:flex;align-items:center;gap:6px;background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.2);border-radius:20px;padding:4px 12px;font-size:12px;color:#94a3b8}
.context-chip .label{color:#64748b}
.context-chip .value{color:#38bdf8}
.context-chip .remove{cursor:pointer;color:#64748b;font-size:14px;margin-left:4px}
.context-chip .remove:hover{color:#f87171}
.refresh-indicator{font-size:11px;color:#64748b;margin-left:auto;display:flex;align-items:center;gap:4px}
.refresh-dot{width:6px;height:6px;border-radius:50%;background:#22c55e;animation:pulse-dot 2s ease-in-out infinite}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:0.3}}
.main-area{grid-column:1;grid-row:2;padding:20px;overflow-y:auto;display:flex;flex-direction:column;gap:20px;position:relative}
.main-area::before{content:'';position:absolute;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 20% 50%,rgba(56,189,248,0.03) 0%,transparent 70%);pointer-events:none}
.main-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
.main-header h1{font-size:18px;font-weight:600;color:#f1f5f9;letter-spacing:-0.3px}
.main-header .subtitle{font-size:12px;color:#64748b}
.insight-banner{background:linear-gradient(135deg,rgba(56,189,248,0.08),rgba(139,92,246,0.08));border:1px solid rgba(56,189,248,0.15);border-radius:10px;padding:12px 16px;display:flex;align-items:flex-start;gap:10px}
.insight-banner .icon{font-size:16px;flex-shrink:0;margin-top:1px}
.insight-banner .text{font-size:13px;color:#94a3b8;line-height:1.4}
.insight-banner .text strong{color:#38bdf8;font-weight:500}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.chart-card{background:rgba(15,23,42,0.6);border:1px solid rgba(56,189,248,0.08);border-radius:12px;padding:16px;position:relative}
.chart-card.wide{grid-column:1/-1}
.chart-card h3{font-size:13px;font-weight:500;color:#94a3b8;margin-bottom:12px}
.chart-card .chart-container{position:relative;width:100%;height:200px}
.chart-card .chart-container.tall{height:240px}
.chart-card canvas{width:100%;height:100%}
.chart-callout{position:absolute;background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.2);border-radius:6px;padding:4px 8px;font-size:10px;color:#22c55e;pointer-events:none;white-space:nowrap}
.chart-callout.alert{background:rgba(248,113,113,0.1);border-color:rgba(248,113,113,0.2);color:#f87171}
.metric-row{display:flex;gap:16px;margin-top:8px}
.metric-box{flex:1;background:rgba(15,23,42,0.4);border-radius:8px;padding:12px;text-align:center}
.metric-box .metric-value{font-size:22px;font-weight:600;color:#f1f5f9}
.metric-box .metric-label{font-size:11px;color:#64748b;margin-top:2px}
.metric-box .metric-change{font-size:11px;margin-top:4px}
.metric-box .metric-change.up{color:#22c55e}
.metric-box .metric-change.down{color:#f87171}
.chat-panel{grid-column:2;grid-row:2;background:rgba(10,14,23,0.95);border-left:1px solid rgba(56,189,248,0.1);display:flex;flex-direction:column;overflow:hidden}
.chat-header{padding:14px 16px;border-bottom:1px solid rgba(56,189,248,0.1);background:rgba(15,23,42,0.5)}
.chat-header h2{font-size:14px;font-weight:600;color:#f1f5f9;display:flex;align-items:center;gap:8px}
.chat-header h2 span{font-size:16px}
.chat-header .status{font-size:11px;color:#22c55e;margin-top:2px;display:flex;align-items:center;gap:4px}
.chat-header .status .dot{width:5px;height:5px;border-radius:50%;background:#22c55e}
.suggested-queries{display:flex;flex-wrap:wrap;gap:6px;padding:10px 16px;border-bottom:1px solid rgba(56,189,248,0.06)}
.suggested-query{font-size:11px;background:rgba(56,189,248,0.06);border:1px solid rgba(56,189,248,0.12);border-radius:14px;padding:4px 10px;color:#64748b;cursor:pointer;transition:all 0.15s;white-space:nowrap}
.suggested-query:hover{background:rgba(56,189,248,0.12);border-color:rgba(56,189,248,0.25);color:#38bdf8}
.chat-messages{flex:1;overflow-y:auto;padding:12px 16px;display:flex;flex-direction:column;gap:12px}
.message{display:flex;gap:8px;max-width:100%}
.message.user{flex-direction:row-reverse}
.message .avatar{width:28px;height:28px;border-radius:50%;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:12px;background:rgba(56,189,248,0.1);color:#38bdf8}
.message.user .avatar{background:rgba(139,92,246,0.15);color:#a78bfa}
.message .bubble{font-size:13px;line-height:1.45;padding:8px 12px;border-radius:12px;max-width:85%}
.message.assistant .bubble{background:rgba(30,41,59,0.6);border:1px solid rgba(56,189,248,0.08);color:#cbd5e1}
.message.user .bubble{background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.15);color:#e1e7f0}
.message .bubble .chart-inline{margin-top:8px;background:rgba(15,23,42,0.5);border-radius:8px;padding:8px;position:relative}
.message .bubble .chart-inline canvas{width:100%;height:120px;display:block}
.message .bubble .chart-inline .callout{font-size:10px;color:#64748b;margin-top:4px}
.message .bubble .chart-inline .annot{font-size:10px;color:#22c55e;margin-top:2px}
.chat-input-area{padding:10px 16px 14px;border-top:1px solid rgba(56,189,248,0.06);background:rgba(10,14,23,0.8)}
.chat-input-wrapper{display:flex;align-items:center;gap:8px;background:rgba(30,41,59,0.4);border:1px solid rgba(56,189,248,0.1);border-radius:20px;padding:4px 4px 4px 14px}
.chat-input-wrapper input{flex:1;background:none;border:none;outline:none;color:#e1e7f0;font-size:13px;padding:6px 0;min-width:0}
.chat-input-wrapper input::placeholder{color:#475569}
.chat-input-wrapper .send-btn{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#38bdf8,#818cf8);border:none;color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;transition:transform 0.1s;flex-shrink:0}
.chat-input-wrapper .send-btn:hover{transform:scale(1.05)}
.chat-input-wrapper .send-btn:active{transform:scale(0.95)}
.footer-bar{grid-column:1/-1;grid-row:3;background:rgba(15,23,42,0.9);backdrop-filter:blur(8px);border-top:1px solid rgba(56,189,248,0.06);padding:6px 20px;display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#475569}
.footer-bar .right{display:flex;gap:16px}
.footer-bar .right span{display:flex;align-items:center;gap:4px}
.blink-alert{animation:blink-alert 1.2s ease-in-out infinite}
@keyframes blink-alert{0%,100%{opacity:1}50%{opacity:0.2}}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(56,189,248,0.15);border-radius:2px}
::-webkit-scrollbar-thumb:hover{background:rgba(56,189,248,0.25)}
@media(max-width:900px){.dashboard{grid-template-columns:1fr;grid-template-rows:auto auto 1fr auto}.chat-panel{grid-column:1;grid-row:3;border-left:none;border-top:1px solid rgba(56,189,248,0.1);max-height:50vh}}
</style>
</head>
<body>
<div class="dashboard">
<div class="context-bar">
<div class="context-chip"><span class="label">Period:</span><span class="value">Q2 2026</span><span class="remove">x</span></div>
<div class="context-chip"><span class="label">Segment:</span><span class="value">Enterprise</span><span class="remove">x</span></div>
<div class="context-chip"><span class="label">Region:</span><span class="value">North America + EMEA</span><span class="remove">x</span></div>
<div class="context-chip"><span class="label">Metric:</span><span class="value">Revenue, MRR, Churn</span><span class="remove">x</span></div>
<div class="refresh-indicator"><span class="refresh-dot"></span>Live &middot; updated 12s ago</div>
</div>
<div class="main-area">
<div class="main-header">
<div><h1>Operations Overview</h1><div class="subtitle">AI Copilot &middot; context-aware analytics</div></div>
<div style="display:flex;gap:8px;align-items:center">
<span style="font-size:11px;color:#64748b">Q2 2026</span>
<span style="font-size:11px;color:#f87171;font-weight:500" class="blink-alert">3 thresholds breached</span>
</div>
</div>
<div class="insight-banner">
<span class="icon">i</span>
<div class="text"><strong>Proactive Insight:</strong> Revenue in EMEA grew 23% week-over-week driven by the FinTech segment. Enterprise MRR hit an all-time high of $847K on June 22. Two accounts (AcmeCorp, NexGen) show declining usage &mdash; consider outreach.</div>
</div>
<div class="metric-row">
<div class="metric-box"><div class="metric-value">$2.41M</div><div class="metric-label">Total Revenue (QTD)</div><div class="metric-change up">+18.3% vs Q1</div></div>
<div class="metric-box"><div class="metric-value">$847K</div><div class="metric-label">MRR (Enterprise)</div><div class="metric-change up">+5.2% MoM</div></div>
<div class="metric-box"><div class="metric-value">3.2%</div><div class="metric-label">Churn Rate</div><div class="metric-change down">+0.4pp vs last month</div></div>
<div class="metric-box"><div class="metric-value">64</div><div class="metric-label">Active Deployments</div><div class="metric-change up">+7 this quarter</div></div>
</div>
<div class="chart-grid">
<div class="chart-card wide">
<h3>Revenue Trend &mdash; Q2 2026 (daily, $K)</h3>
<div class="chart-container tall"><canvas id="chart-revenue"></canvas></div>
</div>
<div class="chart-card">
<h3>MRR by Segment</h3>
<div class="chart-container"><canvas id="chart-mrr-segment"></canvas></div>
</div>
<div class="chart-card">
<h3>Churn Breakdown</h3>
<div class="chart-container"><canvas id="chart-churn"></canvas></div>
</div>
<div class="chart-card">
<h3>Top Customers by MRR</h3>
<div class="chart-container"><canvas id="chart-top-customers"></canvas></div>
</div>
<div class="chart-card">
<h3>Weekly Active Users</h3>
<div class="chart-container"><canvas id="chart-wau"></canvas></div>
</div>
</div>
</div>
<div class="chat-panel">
<div class="chat-header">
<h2><span>~</span>AI Copilot</h2>
<div class="status"><span class="dot"></span>Context-aware &middot; 3 filters active</div>
</div>
<div class="suggested-queries" id="suggestion-bar">
<span class="suggested-query" data-query="What caused the revenue spike last Tuesday?">Revenue spike last Tuesday?</span>
<span class="suggested-query" data-query="Top 5 customers by MRR">Top 5 customers by MRR</span>
<span class="suggested-query" data-query="Compare this quarter to last">Compare Q2 vs Q1</span>
<span class="suggested-query" data-query="Show me churn trends this month">Churn trends this month</span>
<span class="suggested-query" data-query="Which accounts need attention?">Accounts needing attention</span>
</div>
<div class="chat-messages" id="chat-messages">
<div class="message assistant">
<div class="avatar">~</div>
<div class="bubble">
Hi, I&rsquo;m your AI copilot. I see you&rsquo;re viewing Enterprise segment in North America and EMEA for Q2 2026. Ask me anything about your data &mdash; I&rsquo;ll generate charts and insights on the fly.
<div class="suggested-queries" style="margin-top:8px;padding:0;border:none">
<span class="suggested-query" data-query="Show revenue breakdown by region">Breakdown by region</span>
<span class="suggested-query" data-query="Show me the top opportunity accounts">Top opportunity accounts</span>
</div>
</div>
</div>
</div>
<div class="chat-input-area">
<div class="chat-input-wrapper">
<input type="text" id="chat-input" placeholder="Ask about your data..." autocomplete="off">
<button class="send-btn" id="send-btn">&rarr;</button>
</div>
</div>
</div>
<div class="footer-bar">
<span>AI Copilot Query Panel &middot; v1.0</span>
<div class="right">
<span>Data source: live backend (simulated for demo)</span>
<span style="color:#22c55e">All charts rendered from computed values</span>
</div>
</div>
</div>
<script>
// ========== Copilot NL Query Engine ==========
const copilot = {
  context: {
    period: 'Q2 2026',
    segment: 'Enterprise',
    regions: ['North America', 'EMEA'],
    metrics: ['Revenue', 'MRR', 'Churn']
  },
  history: [],
  data: {
    revenueDates: [],
    revenueValues: [],
    revenueCallouts: [],
    segments: ['Enterprise', 'SMB', 'Mid-Market', 'Startup'],
    segmentMRR: [847, 210, 385, 142],
    churnReasons: ['Voluntary', 'Involuntary', 'Downgrade', 'Cancellation'],
    churnValues: [1.8, 0.7, 0.4, 0.3],
    topCustomers: ['AcmeCorp', 'NexGen', 'DataFlow', 'CloudBase', 'StreamLine'],
    topMRR: [195, 142, 98, 76, 54],
    wauDates: [],
    wauValues: []
  },
  init: function() {
    const now = new Date();
    for (let i = 89; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i);
      const dateStr = d.toLocaleDateString('en-US', {month:'short', day:'numeric'});
      this.data.revenueDates.push(dateStr);
      let val = 24 + Math.sin(i * 0.2) * 8 + Math.random() * 6;
      if (i === 8) { val = 38.2; this.data.revenueCallouts.push({idx: i, label: 'Spike: $38.2K', color: '#22c55e'}); }
      else if (i === 45) { val = 16.1; this.data.revenueCallouts.push({idx: i, label: 'Dip: $16.1K', color: '#f87171'}); }
      else if (i === 2) { this.data.revenueCallouts.push({idx: i, label: 'ATH: $41.0K', color: '#38bdf8'}); }
      this.data.revenueValues.push(Math.round(val * 10) / 10);
    }
    for (let i = 12; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i * 7);
      const dateStr = d.toLocaleDateString('en-US', {month:'short', day:'numeric'});
      this.data.wauDates.unshift(dateStr);
      this.data.wauValues.unshift(Math.round(1200 + Math.sin(i * 0.5) * 300 + Math.random() * 200));
    }
  },
  parseQuery: function(query) {
    const q = query.toLowerCase();
    const intents = [];
    if (/spike|dip|drop|jump|surge|decline|anomaly|unusual/i.test(q)) intents.push('anomaly');
    if (/top|best|highest|leading|largest/i.test(q)) intents.push('top_n');
    if (/compare|vs|versus|vs\.|difference|change/i.test(q)) intents.push('comparison');
    if (/trend|over time|trajectory|movement|pattern/i.test(q)) intents.push('trend');
    if (/breakdown|by|per|segmented|split|distribution/i.test(q)) intents.push('breakdown');
    if (/churn|attrition|lost|losing/i.test(q)) intents.push('churn');
    if (/revenue|mrr|arr|income/i.test(q)) intents.push('revenue');
    if (/customer|account|client|user|deployment/i.test(q)) intents.push('customers');
    if (/attention|risk|red flag|alert|concern|watch/i.test(q)) intents.push('risk');
    if (!intents.length) intents.push('general');
    const chartType = this.selectChartType(intents, q);
    return { intents, chartType, raw: query };
  },
  selectChartType: function(intents, q) {
    if (/compare.*quarter|quarter.*compare|q2.*q1|q1.*q2/i.test(q)) return 'side-by-side';
    if (intents.includes('anomaly')) return 'annotated-line';
    if (intents.includes('top_n')) return 'horizontal-bar';
    if (intents.includes('breakdown')) return 'doughnut';
    if (intents.includes('comparison')) return 'grouped-bar';
    if (intents.includes('trend')) return 'line';
    if (intents.includes('churn')) return 'stacked-bar';
    if (intents.includes('customers')) return 'bar';
    if (intents.includes('revenue')) return 'line';
    return 'line';
  },
  executeQuery: function(query) {
    const parsed = this.parseQuery(query);
    const q = query.toLowerCase();
    let response = { text: '', charts: [], table: null };
    if (/spike.*last tuesday|tuesday.*spike|what caused.*spike/i.test(q)) {
      response.text = 'On June 24 (last Tuesday), revenue hit $38.2K &mdash; a 62% daily increase. The spike was driven by: (1) AcmeCorp upgraded from Pro to Enterprise ($12K), (2) NexGen closed a $4.5K add-on deal, and (3) seasonal end-of-quarter enterprise renewals. Normalized to $31.2K the following day.';
      response.charts.push({
        type: 'annotated-line',
        title: 'Revenue Spike Analysis &mdash; June 24',
        highlightIdx: 8,
        data: this.data.revenueValues.slice(3, 18),
        labels: this.data.revenueDates.slice(3, 18),
        callout: { idx: 5, label: 'Spike: $38.2K' },
        annotation: 'AcmeCorp upgrade + NexGen add-on = +$16.5K'
      });
    } else if (/top.*(5|five|customer|mrr)/i.test(q)) {
      response.text = 'Here are your top 5 customers by MRR:';
      response.charts.push({
        type: 'horizontal-bar',
        title: 'Top Customers by MRR ($K)',
        labels: this.data.topCustomers,
        values: this.data.topMRR,
        annotation: 'AcmeCorp and NexGen represent 40% of Enterprise MRR'
      });
    } else if (/compare.*(quarter|q2|q1))/i.test(q) || /q2.*q1|quarter.*last|this quarter.*last/i.test(q)) {
      response.text = 'Q2 2026 vs Q1 2026 comparison: Revenue up 18.3% ($2.41M vs $2.04M). MRR grew 5.2% MoM from $805K to $847K. Churn increased 0.4pp (2.8% to 3.2%) &mdash; driven by voluntary churn in SMB segment. Enterprise retention remains strong at 97.1%.';
      response.charts.push({
        type: 'side-by-side',
        title: 'Q1 vs Q2 Comparison',
        series1: { label: 'Q1', values: [2040, 805, 2.8, 58] },
        series2: { label: 'Q2', values: [2410, 847, 3.2, 64] },
        categories: ['Revenue ($K)', 'MRR ($K)', 'Churn %', 'Deployments']
      });
    } else if (/churn/i.test(q)) {
      response.text = 'Churn is at 3.2% this month, up from 2.8% last month. Voluntary churn (1.8%) is the largest component, primarily from SMB customers under 12 months tenure. Enterprise segment churn is stable at 0.3%.';
      response.charts.push({
        type: 'stacked-bar',
        title: 'Churn Breakdown (%)',
        labels: this.data.churnReasons,
        values: this.data.churnValues,
        annotation: 'Voluntary churn is 56% of total &mdash; focus on early-tenure SMB accounts'
      });
    } else if (/attention|risk|account|red flag|need.*(attention|help)/i.test(q)) {
      response.text = 'Two accounts flagged for attention: (1) <strong>AcmeCorp</strong> &mdash; usage dropped 34% over 4 weeks, no support tickets in 21 days. (2) <strong>NexGen</strong> &mdash; license utilization at 42%, renewal in 45 days. Recommended: schedule QBRs with both within 7 days.';
      response.charts.push({
        type: 'horizontal-bar',
        title: 'Accounts Needing Attention',
        labels: ['AcmeCorp', 'NexGen'],
        values: [34, 58],
        annotation: 'Risk score: higher = more attention needed',
        colors: ['#f87171', '#fb923c']
      });
    } else if (/breakdown.*region|region|geo|by region/i.test(q)) {
      response.text = 'Revenue breakdown by region: North America 58% ($1.40M), EMEA 27% ($651K), APAC 11% ($265K), LATAM 4% ($96K). EMEA grew 23% WoW &mdash; strongest growth region this quarter.';
      response.charts.push({
        type: 'doughnut',
        title: 'Revenue by Region',
        labels: ['North America', 'EMEA', 'APAC', 'LATAM'],
        values: [58, 27, 11, 4],
        annotation: 'EMEA is fastest-growing at +23% WoW'
      });
    } else {
      response.text = 'Based on your current context (Enterprise, Q2 2026, NA+EMEA), here are the key metrics. Revenue is $2.41M QTD (+18.3% vs Q1). MRR at $847K (+5.2% MoM). Churn increased to 3.2%. 64 active deployments (+7 this quarter). Would you like to drill into any specific metric?';
      response.charts.push({
        type: 'line',
        title: 'Revenue Trend (90 days)',
        data: this.data.revenueValues.slice(-30),
        labels: this.data.revenueDates.slice(-30),
        annotation: 'Upward trend +18.3% QoQ'
      });
      response.charts.push({
        type: 'doughnut',
        title: 'MRR by Segment',
        labels: this.data.segments,
        values: this.data.segmentMRR,
        annotation: 'Enterprise is 53% of total MRR'
      });
    }
    return response;
  }
};
// ========== Chart Renderer ==========
const Charts = {
  _resizeCanvas: function(canvas) {
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    const w = rect.width;
    const h = rect.height || canvas.getAttribute('height') || 200;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return { ctx, w, h };
  },
  line: function(canvas, labels, values, opts = {}) {
    const { ctx, w, h } = this._resizeCanvas(canvas);
    const pad = { top: 16, right: 12, bottom: 28, left: 40 };
    const cw = w - pad.left - pad.right;
    const ch = h - pad.top - pad.bottom;
    const max = Math.max(...values) * 1.12;
    const min = Math.min(...values) * 0.88;
    const range = max - min || 1;
    const color = opts.color || '#38bdf8';
    const fillColor = opts.fillColor || 'rgba(56,189,248,0.08)';
    ctx.clearRect(0, 0, w, h);
    // Grid
    ctx.strokeStyle = 'rgba(56,189,248,0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = pad.top + (ch * i) / 4;
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
      ctx.fillStyle = '#475569'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'right';
      const val = (max - (range * i) / 4).toFixed(0);
      ctx.fillText(val, pad.left - 6, y + 3);
    }
    // Fill under
    ctx.beginPath();
    ctx.moveTo(pad.left, pad.top + ch);
    values.forEach((v, i) => {
      const x = pad.left + (i / (values.length - 1)) * cw;
      const y = pad.top + ch - ((v - min) / range) * ch;
      ctx.lineTo(x, y);
    });
    ctx.lineTo(pad.left + cw, pad.top + ch);
    ctx.closePath();
    ctx.fillStyle = fillColor;
    ctx.fill();
    // Line
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    values.forEach((v, i) => {
      const x = pad.left + (i / (values.length - 1)) * cw;
      const y = pad.top + ch - ((v - min) / range) * ch;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.stroke();
    // Dots
    values.forEach((v, i) => {
      const x = pad.left + (i / (values.length - 1)) * cw;
      const y = pad.top + ch - ((v - min) / range) * ch;
      ctx.beginPath(); ctx.arc(x, y, 2.5, 0, Math.PI * 2); ctx.fillStyle = color; ctx.fill();
    });
    // Callouts
    if (opts.callouts) {
      opts.callouts.forEach(c => {
        const x = pad.left + (c.idx / (values.length - 1)) * cw;
        const y = pad.top + ch - ((values[c.idx] - min) / range) * ch;
        ctx.beginPath(); ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = c.color || '#22c55e'; ctx.fill();
        ctx.strokeStyle = '#0a0e17'; ctx.lineWidth = 2; ctx.stroke();
        // Label
        ctx.fillStyle = c.color || '#22c55e';
        ctx.font = '9px -apple-system,sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(c.label, x, y - 10);
      });
    }
    // X labels (show some)
    const step = Math.max(1, Math.floor(values.length / 8));
    labels.forEach((l, i) => {
      if (i % step !== 0 && i !== labels.length - 1) return;
      const x = pad.left + (i / (values.length - 1)) * cw;
      ctx.fillStyle = '#475569'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(l, x, h - 6);
    });
    // Annotation
    if (opts.annotation) {
      ctx.fillStyle = '#22c55e';
      ctx.font = '9px -apple-system,sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(opts.annotation, pad.left, 12);
    }
  },
  bar: function(canvas, labels, values, opts = {}) {
    const { ctx, w, h } = this._resizeCanvas(canvas);
    const horizontal = opts.horizontal || false;
    const pad = { top: 14, right: 10, bottom: 24, left: opts.horizontal ? 80 : 36 };
    const cw = w - pad.left - pad.right;
    const ch = h - pad.top - pad.bottom;
    const max = Math.max(...values) * 1.15 || 1;
    const barCount = labels.length;
    const barGap = 4;
    const barW = horizontal ? ch / barCount - barGap : cw / barCount - barGap;
    ctx.clearRect(0, 0, w, h);
    // Grid (vertical bars)
    if (!horizontal) {
      ctx.strokeStyle = 'rgba(56,189,248,0.05)';
      ctx.lineWidth = 1;
      for (let i = 0; i <= 3; i++) {
        const y = pad.top + (ch * i) / 3;
        ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
        ctx.fillStyle = '#475569'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'right';
        ctx.fillText((max - (max * i) / 3).toFixed(0), pad.left - 6, y + 3);
      }
    }
    labels.forEach((l, i) => {
      const val = values[i];
      const color = opts.colors ? opts.colors[i % opts.colors.length] : '#38bdf8';
      const alpha = opts.colors ? 1 : (0.4 + (val / max) * 0.6);
      if (horizontal) {
        const y = pad.top + (i / barCount) * ch + barGap / 2;
        const bw = (val / max) * cw;
        const bh = barW;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.roundRect ? ctx.roundRect(pad.left, y, bw, bh, 3) : ctx.rect(pad.left, y, bw, bh);
        ctx.fill();
        ctx.fillStyle = '#64748b'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'right';
        ctx.fillText(l, pad.left - 6, y + bh / 2 + 3);
        ctx.fillStyle = '#94a3b8'; ctx.textAlign = 'left';
        ctx.fillText(val + 'K', pad.left + bw + 6, y + bh / 2 + 3);
      } else {
        const x = pad.left + (i / barCount) * cw + barGap / 2;
        const bw = barW;
        const bh = (val / max) * ch;
        const y = pad.top + ch - bh;
        ctx.fillStyle = `rgba(56,189,248,${alpha})`;
        ctx.beginPath();
        ctx.roundRect ? ctx.roundRect(x, y, bw, bh, 3) : ctx.rect(x, y, bw, bh);
        ctx.fill();
        ctx.fillStyle = '#475569'; ctx.font = '8px -apple-system,sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(l, x + bw / 2, h - 6);
      }
    });
    if (opts.annotation) {
      ctx.fillStyle = '#22c55e'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(opts.annotation, pad.left, 12);
    }
  },
  doughnut: function(canvas, labels, values, opts = {}) {
    const { ctx, w, h } = this._resizeCanvas(canvas);
    const cx = w / 2, cy = h / 2;
    const outerR = Math.min(cx, cy) - 20;
    const innerR = outerR * 0.55;
    const total = values.reduce((a, b) => a + b, 0);
    const colors = ['#38bdf8', '#818cf8', '#34d399', '#fb923c', '#f87171', '#a78bfa', '#fbbf24'];
    let startAngle = -Math.PI / 2;
    ctx.clearRect(0, 0, w, h);
    values.forEach((v, i) => {
      const sliceAngle = (v / total) * Math.PI * 2;
      const color = opts.colors ? opts.colors[i % opts.colors.length] : colors[i % colors.length];
      ctx.beginPath();
      ctx.arc(cx, cy, outerR, startAngle, startAngle + sliceAngle);
      ctx.arc(cx, cy, innerR, startAngle + sliceAngle, startAngle, true);
      ctx.closePath();
      ctx.fillStyle = color;
      ctx.fill();
      // Label line
      const midAngle = startAngle + sliceAngle / 2;
      const labelR = outerR + 14;
      const lx = cx + Math.cos(midAngle) * labelR;
      const ly = cy + Math.sin(midAngle) * labelR;
      ctx.fillStyle = '#94a3b8';
      ctx.font = '9px -apple-system,sans-serif';
      ctx.textAlign = midAngle > Math.PI / 2 && midAngle < Math.PI * 1.5 ? 'right' : 'left';
      ctx.fillText(`${labels[i]} ${Math.round(v / total * 100)}%`, lx, ly + 3);
      startAngle += sliceAngle;
    });
    ctx.fillStyle = '#f1f5f9';
    ctx.font = 'bold 14px -apple-system,sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(total + '%', cx, cy + 5);
    if (opts.annotation) {
      ctx.fillStyle = '#22c55e'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(opts.annotation, 10, 12);
    }
  },
  groupedBar: function(canvas, categories, series1, series2, opts = {}) {
    const { ctx, w, h } = this._resizeCanvas(canvas);
    const pad = { top: 14, right: 10, bottom: 24, left: 44 };
    const cw = w - pad.left - pad.right;
    const ch = h - pad.top - pad.bottom;
    const max = Math.max(...series1.values, ...series2.values) * 1.15 || 1;
    const groupCount = categories.length;
    const groupW = cw / groupCount;
    const barW = groupW * 0.35;
    ctx.clearRect(0, 0, w, h);
    // Grid
    ctx.strokeStyle = 'rgba(56,189,248,0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 3; i++) {
      const y = pad.top + (ch * i) / 3;
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
      ctx.fillStyle = '#475569'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'right';
      ctx.fillText((max - (max * i) / 3).toFixed(0), pad.left - 6, y + 3);
    }
    categories.forEach((cat, i) => {
      const gx = pad.left + i * groupW;
      // Series 1
      const bh1 = (series1.values[i] / max) * ch;
      const y1 = pad.top + ch - bh1;
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath();
      ctx.roundRect ? ctx.roundRect(gx + 4, y1, barW, bh1, 3) : ctx.rect(gx + 4, y1, barW, bh1);
      ctx.fill();
      // Series 2
      const bh2 = (series2.values[i] / max) * ch;
      const y2 = pad.top + ch - bh2;
      ctx.fillStyle = '#818cf8';
      ctx.beginPath();
      ctx.roundRect ? ctx.roundRect(gx + barW + 8, y2, barW, bh2, 3) : ctx.rect(gx + barW + 8, y2, barW, bh2);
      ctx.fill();
      // Label
      ctx.fillStyle = '#475569'; ctx.font = '8px -apple-system,sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(cat, gx + groupW / 2, h - 6);
    });
    // Legend
    ctx.fillStyle = '#38bdf8'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'left';
    ctx.fillRect(10, 4, 8, 8); ctx.fillText(series1.label, 22, 12);
    ctx.fillStyle = '#818cf8';
    ctx.fillRect(70, 4, 8, 8); ctx.fillText(series2.label, 82, 12);
    if (opts.annotation) {
      ctx.fillStyle = '#22c55e'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'right';
      ctx.fillText(opts.annotation, w - 10, 12);
    }
  },
  stackedBar: function(canvas, labels, values, opts = {}) {
    const { ctx, w, h } = this._resizeCanvas(canvas);
    const pad = { top: 14, right: 10, bottom: 24, left: 36 };
    const cw = w - pad.left - pad.right;
    const ch = h - pad.top - pad.bottom;
    const max = Math.max(...values) * 1.15 || 1;
    const barW = 30;
    const colors = ['#f87171', '#fb923c', '#fbbf24', '#a78bfa'];
    const total = values.reduce((a, b) => a + b, 0);
    ctx.clearRect(0, 0, w, h);
    // Grid
    ctx.strokeStyle = 'rgba(56,189,248,0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 3; i++) {
      const y = pad.top + (ch * i) / 3;
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(w - pad.right, y); ctx.stroke();
      ctx.fillStyle = '#475569'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'right';
      ctx.fillText((max - (max * i) / 3).toFixed(1), pad.left - 6, y + 3);
    }
    // Stacked bars
    const totalBars = labels.length;
    const startX = pad.left + (cw - totalBars * (barW + 8)) / 2;
    let yOffset = 0;
    labels.forEach((l, i) => {
      const x = startX + i * (barW + 8);
      const bh = (values[i] / max) * ch;
      const y = pad.top + ch - bh;
      ctx.fillStyle = colors[i % colors.length];
      ctx.beginPath();
      ctx.roundRect ? ctx.roundRect(x, y, barW, bh, 3) : ctx.rect(x, y, barW, bh);
      ctx.fill();
      ctx.fillStyle = '#475569'; ctx.font = '8px -apple-system,sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(l, x + barW / 2, h - 6);
      ctx.fillStyle = '#94a3b8'; ctx.font = '8px -apple-system,sans-serif';
      ctx.fillText(values[i] + '%', x + barW / 2, y - 4);
    });
    if (opts.annotation) {
      ctx.fillStyle = '#22c55e'; ctx.font = '9px -apple-system,sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(opts.annotation, pad.left, 12);
    }
  }
};
// ========== Render Dashboard ==========
copilot.init();
function renderDashboard() {
  const D = copilot.data;
  // Revenue line
  Charts.line(document.getElementById('chart-revenue'), D.revenueDates, D.revenueValues, {
    color: '#38bdf8', fillColor: 'rgba(56,189,248,0.06)',
    callouts: D.revenueCallouts,
    annotation: 'Jun 24 spike: AcmeCorp upgrade + NexGen add-on'
  });
  // MRR segment doughnut
  Charts.doughnut(document.getElementById('chart-mrr-segment'), D.segments, D.segmentMRR, {
    annotation: 'Enterprise: 53% of total MRR'
  });
  // Churn stacked
  Charts.stackedBar(document.getElementById('chart-churn'), D.churnReasons, D.churnValues, {
    annotation: 'Voluntary churn leading at 1.8%'
  });
  // Top customers
  Charts.bar(document.getElementById('chart-top-customers'), D.topCustomers, D.topMRR, {
    horizontal: true,
    colors: ['#38bdf8', '#818cf8', '#34d399', '#fb923c', '#f87171'],
    annotation: 'AcmeCorp: 23% of Enterprise MRR'
  });
  // WAU line
  Charts.line(document.getElementById('chart-wau'), D.wauDates, D.wauValues, {
    color: '#a78bfa', fillColor: 'rgba(167,139,250,0.06)',
    annotation: 'Steady growth trend +15% QoQ'
  });
}
// ========== Chat Rendering ==========
function renderChatChart(container, chartData) {
  const canvas = document.createElement('canvas');
  canvas.width = 300; canvas.height = 120;
  canvas.style.width = '100%'; canvas.style.height = '120px';
  container.appendChild(canvas);
  setTimeout(() => {
    switch (chartData.type) {
      case 'annotated-line':
        Charts.line(canvas, chartData.labels, chartData.data, {
          color: '#38bdf8', fillColor: 'rgba(56,189,248,0.06)',
          callouts: chartData.callout ? [{ idx: chartData.callout.idx || 5, label: chartData.callout.label, color: '#22c55e' }] : [],
          annotation: chartData.annotation
        });
        break;
      case 'horizontal-bar':
        Charts.bar(canvas, chartData.labels, chartData.values, {
          horizontal: true,
          colors: chartData.colors || ['#38bdf8', '#818cf8', '#34d399', '#fb923c', '#f87171'],
          annotation: chartData.annotation
        });
        break;
      case 'doughnut':
        Charts.doughnut(canvas, chartData.labels, chartData.values, {
          annotation: chartData.annotation
        });
        break;
      case 'side-by-side':
        Charts.groupedBar(canvas, chartData.categories, chartData.series1, chartData.series2, {
          annotation: chartData.annotation
        });
        break;
      case 'stacked-bar':
        Charts.stackedBar(canvas, chartData.labels, chartData.values, {
          annotation: chartData.annotation
        });
        break;
      default:
        Charts.line(canvas, chartData.labels || chartData.data.map((_, i) => i.toString()), chartData.data, {
          annotation: chartData.annotation
        });
    }
    if (chartData.annotation) {
      const annot = document.createElement('div');
      annot.className = 'annot';
      annot.textContent = chartData.annotation;
      container.appendChild(annot);
    }
  }, 50);
}
function addMessage(role, content, charts) {
  const messages = document.getElementById('chat-messages');
  const msg = document.createElement('div');
  msg.className = 'message ' + role;
  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'assistant' ? '~' : 'U';
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.innerHTML = content;
  msg.appendChild(avatar);
  msg.appendChild(bubble);
  messages.appendChild(msg);
  if (charts && charts.length > 0) {
    charts.forEach(cd => {
      const chartContainer = document.createElement('div');
      chartContainer.className = 'chart-inline';
      bubble.appendChild(chartContainer);
      renderChatChart(chartContainer, cd);
    });
  }
  messages.scrollTop = messages.scrollHeight;
}
function handleQuery(query) {
  if (!query.trim()) return;
  addMessage('user', query);
  document.getElementById('chat-input').value = '';
  const response = copilot.executeQuery(query);
  copilot.history.push({ query, response });
  setTimeout(() => addMessage('assistant', response.text, response.charts), 400);
  updateSuggestions();
}
function updateSuggestions() {
  const suggestions = [
    'What caused the revenue spike last Tuesday?',
    'Top 5 customers by MRR',
    'Compare this quarter to last',
    'Show me churn trends this month',
    'Which accounts need attention?',
    'Show revenue breakdown by region',
    'Show me the top opportunity accounts'
  ];
  const bar = document.getElementById('suggestion-bar');
  bar.innerHTML = suggestions.slice(0, 5).map(s =>
    `<span class="suggested-query" data-query="${s.replace(/"/g, '&quot;')}">${s}</span>`
  ).join('');
}
// ========== Events ==========
document.addEventListener('DOMContentLoaded', () => {
  renderDashboard();
  // Input
  const input = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-btn');
  function send() { handleQuery(input.value); }
  sendBtn.addEventListener('click', send);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') send(); });
  // Suggested queries
  document.addEventListener('click', e => {
    const chip = e.target.closest('.suggested-query');
    if (chip) handleQuery(chip.dataset.query);
  });
  // Context chip remove
  document.querySelectorAll('.context-chip .remove').forEach(el => {
    el.addEventListener('click', function() {
      this.parentElement.style.opacity = '0.3';
      this.parentElement.style.pointerEvents = 'none';
    });
  });
  // Resize
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(renderDashboard, 200);
  });
});
</script>
</body>
</html>