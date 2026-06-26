```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Voice Command Dashboard</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0b0d11;color:#e0e4ec;height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:240px 1fr;height:100vh}
.sidebar{background:#12151c;border-right:1px solid #1e2530;padding:20px}
.sidebar h1{font-size:18px;font-weight:400;color:#8892a4;margin-bottom:4px}
.sidebar h2{font-size:12px;font-weight:300;color:#4a5568;margin-bottom:24px}
.sidebar .status{display:flex;align-items:center;gap:8px;margin-bottom:24px;font-size:13px}
.sidebar .dot{width:8px;height:8px;border-radius:50%;background:#2d3748;transition:.3s}
.sidebar .dot.active{background:#48bb78;box-shadow:0 0 8px #48bb7855}
.sidebar .dot.idle{background:#ecc94b;box-shadow:0 0 8px #ecc94b55}
.sidebar .dot.error{background:#f56565;box-shadow:0 0 8px #f5656555}
.main{padding:24px 32px;overflow-y:auto}
.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}
.topbar .mic-toggle{width:44px;height:44px;border-radius:50%;border:2px solid #1e2530;background:#12151c;color:#e0e4ec;font-size:18px;cursor:pointer;transition:.2s;display:flex;align-items:center;justify-content:center}
.topbar .mic-toggle:hover{border-color:#48bb78;color:#48bb78}
.topbar .mic-toggle.listening{background:#48bb7811;border-color:#48bb78;color:#48bb78;animation:pulse 1.5s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 #48bb7844}70%{box-shadow:0 0 0 12px #48bb7800}100%{box-shadow:0 0 0 0 #48bb7800}}
.interim{font-size:14px;color:#48bb78;min-height:22px;margin-bottom:16px;font-style:italic}
.command-history{font-size:12px;color:#4a5568;margin-bottom:16px;min-height:18px}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}
.kpi-card{background:#12151c;border:1px solid #1e2530;border-radius:8px;padding:16px}
.kpi-card .label{font-size:12px;color:#4a5568;margin-bottom:4px}
.kpi-card .value{font-size:28px;font-weight:300;color:#e0e4ec}
.kpi-card .change{font-size:12px;margin-top:4px}
.kpi-card .change.up{color:#48bb78}
.kpi-card .change.down{color:#f56565}
.chart-area{background:#12151c;border:1px solid #1e2530;border-radius:8px;padding:20px;margin-bottom:24px;min-height:240px;position:relative}
.chart-area .chart-title{font-size:13px;color:#4a5568;margin-bottom:12px}
.chart-area .chart-bars{display:flex;align-items:flex-end;gap:24px;height:160px;padding-top:8px}
.chart-area .bar-group{display:flex;flex-direction:column;align-items:center;flex:1}
.chart-area .bar{width:100%;max-width:48px;border-radius:4px 4px 0 0;transition:.4s;position:relative}
.chart-area .bar-label{font-size:11px;color:#4a5568;margin-top:6px}
.chart-area .bar-value{font-size:10px;color:#8892a4;position:absolute;top:-16px;left:50%;transform:translateX(-50%)}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}
.data-table{background:#12151c;border:1px solid #1e2530;border-radius:8px;padding:20px;min-height:180px}
.data-table .table-title{font-size:13px;color:#4a5568;margin-bottom:12px}
.data-table table{width:100%;border-collapse:collapse;font-size:13px}
.data-table th{text-align:left;color:#4a5568;font-weight:400;padding:6px 0;border-bottom:1px solid #1e2530}
.data-table td{padding:6px 0;border-bottom:1px solid #1a1f2a;color:#8892a4}
.command-suggestions{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#12151cee;border:1px solid #1e2530;border-radius:12px;padding:12px 20px;backdrop-filter:blur(12px);display:flex;gap:12px;align-items:center;opacity:.35;transition:.4s;max-width:80vw;flex-wrap:wrap;justify-content:center}
.command-suggestions:hover,.command-suggestions.active{opacity:1}
.command-suggestions .hint{font-size:12px;color:#4a5568;white-space:nowrap}
.command-suggestions .cmd{font-size:12px;color:#8892a4;background:#1e2530;padding:4px 10px;border-radius:6px;cursor:default;transition:.2s}
.command-suggestions .cmd:hover{background:#2d3748;color:#e0e4ec}
.speech-feedback{position:fixed;top:24px;right:24px;background:#12151cee;border:1px solid #1e2530;border-radius:8px;padding:10px 16px;backdrop-filter:blur(12px);font-size:13px;color:#48bb78;max-width:300px;opacity:0;transition:.4s;transform:translateY(-8px);pointer-events:none}
.speech-feedback.show{opacity:1;transform:translateY(0)}
.voice-commands-panel{background:#12151c;border:1px solid #1e2530;border-radius:8px;padding:20px;min-height:180px}
.voice-commands-panel .panel-title{font-size:13px;color:#4a5568;margin-bottom:12px}
.voice-commands-panel .cmd-list{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.voice-commands-panel .cmd-item{font-size:12px;color:#8892a4;padding:4px 8px;background:#1a1f2a;border-radius:4px}
.voice-commands-panel .cmd-item .keyword{color:#48bb78}
</style>
</head>
<body>
<div class="dashboard">
  <div class="sidebar">
    <h1>Styde Forge</h1>
    <h2>Voice Command Dashboard</h2>
    <div class="status">
      <span class="dot idle" id="statusDot"></span>
      <span id="statusText">Voice idle</span>
    </div>
    <div style="font-size:11px;color:#4a5568;margin-bottom:16px">
      Confidence: <span id="confidenceDisplay">--</span>
    </div>
    <div id="contextDisplay" style="font-size:11px;color:#4a5568">
      Context: none
    </div>
    <div style="margin-top:auto;padding-top:24px;font-size:10px;color:#2d3748">
      v1.0 &middot; Web Speech API
    </div>
  </div>
  <div class="main">
    <div class="topbar">
      <div>
        <div class="interim" id="interimDisplay">--</div>
        <div class="command-history" id="commandHistory">Awaiting voice command...</div>
      </div>
      <button class="mic-toggle" id="micButton" title="Toggle microphone">&#x1f3a4;</button>
    </div>
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="label">Revenue</div>
        <div class="value" id="kpiRevenue">$2.4M</div>
        <div class="change up">+12.3%</div>
      </div>
      <div class="kpi-card">
        <div class="label">Users</div>
        <div class="value" id="kpiUsers">18.7K</div>
        <div class="change up">+8.1%</div>
      </div>
      <div class="kpi-card">
        <div class="label">Error Rate</div>
        <div class="value" id="kpiErrors">2.3%</div>
        <div class="change down">+0.4%</div>
      </div>
      <div class="kpi-card">
        <div class="label">Avg Session</div>
        <div class="value" id="kpiSession">4m 32s</div>
        <div class="change up">+5.2%</div>
      </div>
    </div>
    <div class="grid-2">
      <div class="chart-area" id="chartRevenue">
        <div class="chart-title" id="chartTitle">Revenue by Region</div>
        <div class="chart-bars" id="chartBars"></div>
      </div>
      <div class="voice-commands-panel">
        <div class="panel-title">Available Voice Commands</div>
        <div class="cmd-list" id="commandList">
          <div class="cmd-item">"<span class="keyword">show</span> revenue by region"</div>
          <div class="cmd-item">"<span class="keyword">filter</span> to EU only"</div>
          <div class="cmd-item">"<span class="keyword">compare</span> Q3 and Q4"</div>
          <div class="cmd-item">"<span class="keyword">alert</span> error rate above 5%"</div>
          <div class="cmd-item">"<span class="keyword">sort</span> by growth descending"</div>
          <div class="cmd-item">"<span class="keyword">export</span> this view as PDF"</div>
          <div class="cmd-item">"<span class="keyword">show</span> user growth chart"</div>
          <div class="cmd-item">"<span class="keyword">filter</span> that to last month"</div>
        </div>
      </div>
    </div>
    <div class="grid-2">
      <div class="data-table">
        <div class="table-title" id="tableTitle">Regional Revenue</div>
        <table id="dataTable">
          <thead><tr><th>Region</th><th>Revenue</th><th>Growth</th><th>Users</th></tr></thead>
          <tbody id="tableBody"></tbody>
        </table>
      </div>
      <div class="data-table">
        <div class="table-title">Command History</div>
        <table>
          <thead><tr><th>Time</th><th>Command</th><th>Status</th></tr></thead>
          <tbody id="voiceHistoryBody"></tbody>
        </table>
      </div>
    </div>
  </div>
</div>
<div class="speech-feedback" id="speechFeedback"></div>
<div class="command-suggestions" id="commandSuggestions">
  <span class="hint">Try saying:</span>
  <span class="cmd">show revenue by region</span>
  <span class="cmd">filter to EU</span>
  <span class="cmd">compare Q3 Q4</span>
  <span class="cmd">export PDF</span>
</div>
<script>
(function(){
  // ----------------------------------------------------------------
  // State
  // ----------------------------------------------------------------
  const state = {
    listening: false,
    context: null,           // last view/filter context for anaphora resolution
    confidence: 0,
    commandHistory: [],
    currentView: 'revenue-by-region',
    filters: {},
    lastTranscript: '',
    interimText: '',
    micWarmup: false,
  };
  // ----------------------------------------------------------------
  // DOM refs
  // ----------------------------------------------------------------
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => document.querySelectorAll(s);
  const interimDisplay = $('#interimDisplay');
  const commandHistory = $('#commandHistory');
  const statusDot = $('#statusDot');
  const statusText = $('#statusText');
  const confidenceDisplay = $('#confidenceDisplay');
  const contextDisplay = $('#contextDisplay');
  const micButton = $('#micButton');
  const speechFeedback = $('#speechFeedback');
  const chartBars = $('#chartBars');
  const chartTitle = $('#chartTitle');
  const tableBody = $('#tableBody');
  const tableTitle = $('#tableTitle');
  const voiceHistoryBody = $('#voiceHistoryBody');
  const commandSuggestions = $('#commandSuggestions');
  // ----------------------------------------------------------------
  // Data
  // ----------------------------------------------------------------
  const regionData = [
    {region:'North America', revenue:'$892K', growth:'+14.2%', users:'6.2K'},
    {region:'Europe', revenue:'$654K', growth:'+9.8%', users:'5.1K'},
    {region:'Asia Pacific', revenue:'$512K', growth:'+18.5%', users:'4.3K'},
    {region:'Latin America', revenue:'$198K', growth:'+7.3%', users:'1.8K'},
    {region:'Middle East', revenue:'$144K', growth:'+11.1%', users:'1.3K'},
  ];
  const chartData = [
    {label:'NA', value:72, color:'#48bb78'},
    {label:'EU', value:58, color:'#4299e1'},
    {label:'APAC', value:46, color:'#ed8936'},
    {label:'LATAM', value:22, color:'#9f7aea'},
    {label:'MEA', value:18, color:'#fc8181'},
  ];
  const kpiDefaults = {
    revenue: {value:'$2.4M', change:'+12.3%', dir:'up'},
    users: {value:'18.7K', change:'+8.1%', dir:'up'},
    errors: {value:'2.3%', change:'+0.4%', dir:'down'},
    session: {value:'4m 32s', change:'+5.2%', dir:'up'},
  };
  // ----------------------------------------------------------------
  // Render helpers
  // ----------------------------------------------------------------
  function renderChart(data, title) {
    chartTitle.textContent = title || 'Revenue by Region';
    chartBars.innerHTML = data.map((d,i) => {
      const delay = i * 60;
      return `<div class="bar-group">
        <div class="bar" style="height:${d.value * 2}px;background:${d.color};transition-delay:${delay}ms">
          <span class="bar-value">${d.value}%</span>
        </div>
        <span class="bar-label">${d.label}</span>
      </div>`;
    }).join('');
  }
  function renderTable(data, title) {
    tableTitle.textContent = title || 'Regional Revenue';
    tableBody.innerHTML = data.map(r =>
      `<tr><td>${r.region}</td><td>${r.revenue}</td><td>${r.growth}</td><td>${r.users}</td></tr>`
    ).join('');
  }
  function renderKPIs(kpis) {
    const map = {revenue:'kpiRevenue', users:'kpiUsers', errors:'kpiErrors', session:'kpiSession'};
    Object.keys(map).forEach(k => {
      const el = $('#'+map[k]);
      if (el && kpis[k]) el.textContent = kpis[k].value;
    });
  }
  function renderInitial() {
    renderChart(chartData, 'Revenue by Region');
    renderTable(regionData, 'Regional Revenue');
  }
  function addVoiceHistory(cmd, status) {
    const ts = new Date().toLocaleTimeString();
    const row = document.createElement('tr');
    row.innerHTML = `<td>${ts}</td><td>${cmd}</td><td style="color:${status==='ok'?'#48bb78':'#f56565'}">${status}</td>`;
    voiceHistoryBody.prepend(row);
    if (voiceHistoryBody.children.length > 20) voiceHistoryBody.lastElementChild.remove();
  }
  function showFeedback(text) {
    speechFeedback.textContent = text;
    speechFeedback.classList.add('show');
    setTimeout(() => speechFeedback.classList.remove('show'), 3000);
  }
  function speak(text) {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 0.92;
    utter.pitch = 1.05;
    utter.volume = 1;
    window.speechSynthesis.speak(utter);
    showFeedback(text);
  }
  function setStatus(mode, text, conf) {
    const dot = statusDot;
    dot.className = 'dot';
    if (mode === 'listening') {
      dot.classList.add('active');
      micButton.classList.add('listening');
    } else if (mode === 'idle') {
      dot.classList.add('idle');
      micButton.classList.remove('listening');
    } else {
      dot.classList.add('error');
      micButton.classList.remove('listening');
    }
    statusText.textContent = text;
    if (conf !== undefined) {
      state.confidence = conf;
      confidenceDisplay.textContent = (conf * 100).toFixed(1) + '%';
    }
  }
  function setContext(ctx) {
    state.context = ctx;
    const parts = [];
    if (ctx && ctx.view) parts.push('view:'+ctx.view);
    if (ctx && ctx.filters) {
      Object.entries(ctx.filters).forEach(([k,v]) => parts.push(k+':'+v));
    }
    contextDisplay.textContent = 'Context: ' + (parts.length ? parts.join(', ') : 'none');
  }
  // ----------------------------------------------------------------
  // Intent parser with anaphora resolution
  // ----------------------------------------------------------------
  const intentPatterns = [
    // Navigate
    { re: /show\s+(revenue|users?|growth|errors?|sessions?|traffic|sales|performance)\s+(by|for|per|over)\s+(.+)/i, action: 'navigate' },
    { re: /show\s+(revenue|users?|growth|errors?|sessions?|traffic|sales|performance)/i, action: 'navigate', group:1 },
    { re: /go\s+to\s+(.+)/i, action: 'navigate', group:1 },
    { re: /navigate\s+to\s+(.+)/i, action: 'navigate', group:1 },
    { re: /open\s+(.+)/i, action: 'navigate', group:1 },
    // Filter
    { re: /filter\s+(to|by|for|on)\s+(.+)/i, action: 'filter', group:2 },
    { re: /filter\s+that\s+(to|by|for)\s+(.+)/i, action: 'filter_anaphora', group:2 },
    { re: /filter\s+this\s+(to|by|for)\s+(.+)/i, action: 'filter', group:2 },
    { re: /only\s+(.+)/i, action: 'filter', group:1 },
    // Compare
    { re: /compare\s+(.+)\s+and\s+(.+)/i, action: 'compare' },
    { re: /compare\s+(.+)/i, action: 'compare', group:1 },
    // Alert
    { re: /alert\s+me\s+when\s+(.+)\s+(exceeds?|above|below|reaches?|drops?\s+below)\s+(\d+)/i, action: 'alert' },
    { re: /alert\s+(.+)\s+(exceeds?|above|below|reaches?|drops?\s+below)\s+(\d+)/i, action: 'alert' },
    { re: /(?:set|add)\s+alert\s+(.+)\s+(exceeds?|above|below|reaches?|drops?\s+below)\s+(\d+)/i, action: 'alert' },
    // Export
    { re: /export\s+(this\s+)?(view|data|report|dashboard|table|chart)\s+as\s+(pdf|csv|png|json|xlsx?)/i, action: 'export', group:3 },
    { re: /export\s+(to|as)\s+(pdf|csv|png|json|xlsx?)/i, action: 'export', group:2 },
    // Sort
    { re: /sort\s+(by|on)\s+(.+?)(\s+(ascending|descending|asc|desc))?$/i, action: 'sort' },
    // Query
    { re: /(what|how|when|where|why)\s+(is|are|was|were|has|have|did|does)\s+(.+)/i, action: 'query' },
    // Reset
    { re: /(reset|clear|remove)\s+(all\s+)?(filters?|context|view)/i, action: 'reset' },
    // Anaphora: 'that'/'those' resolution
    { re: /^(show|filter|sort|export|compare)\s+that/i, action: 'anaphora_action' },
  ];
  function parseIntent(transcript) {
    const text = transcript.trim().toLowerCase().replace(/[.,!?]+$/, '').trim();
    state.lastTranscript = text;
    for (const p of intentPatterns) {
      const m = text.match(p.re);
      if (!m) continue;
      const raw = m[0];
      // Resolve anaphora
      if (p.action === 'filter_anaphora' || p.action === 'anaphora_action') {
        if (!state.context) {
          return { action: 'error', reason: 'No prior context to reference', raw };
        }
        // merge: filter_anaphora -> filter with context
        if (p.action === 'filter_anaphora') {
          const filterTarget = m[p.group] || m[2];
          return { action: 'filter', target: filterTarget, context: state.context, raw, anaphora: true };
        }
        if (p.action === 'anaphora_action') {
          // 'show that' etc — delegate to context
          return { action: 'navigate', target: state.context.view || state.currentView, raw, anaphora: true };
        }
      }
      if (p.action === 'navigate') {
        const target = p.group ? m[p.group] : (m[3] ? m[3] : m[1]);
        return { action: 'navigate', target: target.trim(), raw };
      }
      if (p.action === 'filter') {
        const target = m[p.group] || m[2];
        return { action: 'filter', target: target.trim(), raw };
      }
      if (p.action === 'compare') {
        const a = (m[1] || '').trim();
        const b = (m[2] || '').trim();
        return { action: 'compare', items: a ? [a, b || a] : [], raw };
      }
      if (p.action === 'alert') {
        const metric = m[1] ? m[1].trim() : 'error rate';
        const operator = m[2] ? m[2].trim() : 'exceeds';
        const threshold = m[3] ? parseInt(m[3]) : 5;
        return { action: 'alert', metric, operator, threshold, raw };
      }
      if (p.action === 'export') {
        const fmt = m[p.group] || m[2] || 'pdf';
        return { action: 'export', format: fmt.trim().toLowerCase(), raw };
      }
      if (p.action === 'sort') {
        const field = m[2] ? m[2].trim() : 'revenue';
        const dir = m[4] ? m[4].trim() : 'descending';
        return { action: 'sort', field, direction: dir, raw };
      }
      if (p.action === 'query') {
        return { action: 'query', text: m[3] ? m[3].trim() : text, raw };
      }
      if (p.action === 'reset') {
        return { action: 'reset', raw };
      }
      return { action: p.action, raw };
    }
    // Fallback: check for common anaphora
    if (/^(that|this|those|it)\b/.test(text)) {
      if (state.context) {
        return { action: 'navigate', target: state.context.view || state.currentView, raw: text, anaphora: true };
      }
      return { action: 'error', reason: 'No context to resolve reference', raw: text };
    }
    return { action: 'unknown', raw: text };
  }
  // ----------------------------------------------------------------
  // Intent executors
  // ----------------------------------------------------------------
  function executeIntent(intent) {
    const raw = intent.raw || state.lastTranscript;
    addVoiceHistory(raw, 'processing');
    switch (intent.action) {
      case 'navigate': {
        const t = intent.target.toLowerCase();
        let data, chartLabel, title, kpis, filterHint;
        if (t.includes('user') || t.includes('users') || t.includes('growth')) {
          if (t.includes('growth')) {
            data = regionData.slice().sort((a,b) => parseFloat(b.growth) - parseFloat(a.growth));
            chartLabel = 'User Growth by Region (%)';
            title = 'Regional Growth';
            kpis = {...kpiDefaults, users: {value:'18.7K', change:'+18.5%', dir:'up'}};
            filterHint = 'growth';
          } else {
            data = regionData.map(r => ({...r, revenue: r.users}));
            chartLabel = 'Users by Region';
            title = 'Regional Users';
            kpis = {...kpiDefaults, users: {value:'18.7K', change:'+8.1%', dir:'up'}};
            filterHint = 'users';
          }
        } else if (t.includes('error') || t.includes('errors')) {
          const errData = [{label:'API', value:38, color:'#f56565'},{label:'Auth', value:22, color:'#ed8936'},{label:'DB', value:15, color:'#ecc94b'},{label:'Network', value:12, color:'#4299e1'},{label:'Other', value:8, color:'#8892a4'}];
          renderChart(errData, 'Error Rate by Category');
          renderTable(regionData.map(r => ({...r, growth: (Math.random()*0.8+0.1).toFixed(1)+'%', revenue: (Math.random()*5+0.5).toFixed(1)+'%'})), 'Error Breakdown');
          renderKPIs({...kpiDefaults, errors: {value:'2.3%', change:'-0.3%', dir:'down'}});
          setContext({view:'errors'});
          state.currentView = 'errors';
          speak('Showing error breakdown by category');
          return;
        } else if (t.includes('session')) {
          chartLabel = 'Session Duration by Region';
          data = regionData.map((r,i) => ({...r, label:r.region.slice(0,2).toUpperCase(), value: 30 + i*8, color: chartData[i].color}));
          title = 'Avg Session Duration';
          kpis = {...kpiDefaults, session: {value:'5m 12s', change:'+7.8%', dir:'up'}};
          filterHint = 'sessions';
        } else if (t.includes('sales') || t.includes('performance')) {
          chartLabel = 'Sales Performance';
          data = regionData.map((r,i) => ({label:r.region.slice(0,2).toUpperCase(), value: 60 + i*5, color: '#4299e1'}));
          title = 'Sales by Region';
          kpis = {...kpiDefaults, revenue: {value:'$3.1M', change:'+15.2%', dir:'up'}};
          filterHint = 'sales';
        } else {
          // default: revenue
          data = chartData;
          chartLabel = 'Revenue by Region';
          title = 'Regional Revenue';
          kpis = kpiDefaults;
          filterHint = 'revenue';
        }
        renderChart(data || chartData, chartLabel);
        renderTable(data ? data.map((d,i) => ({
          region: ['North America','Europe','Asia Pacific','Latin America','Middle East'][i] || 'Other',
          revenue: d.value ? '$'+(d.value*12)+'K' : '$--',
          growth: ['+14.2%','+9.8%','+18.5%','+7.3%','+11.1%'][i] || '+0%',
          users: ['6.2K','5.1K','4.3K','1.8K','1.3K'][i] || '0',
        })) : regionData, title);
        if (kpis) renderKPIs(kpis);
        setContext({view: filterHint || 'revenue'});
        state.currentView = filterHint || 'revenue';
        speak('Showing ' + (chartLabel || 'revenue by region'));
        break;
      }
      case 'filter': {
        const t = intent.target ? intent.target.toLowerCase() : '';
        let filterVal = '';
        if (t.includes('eu') || t.includes('europe') || t.includes('emea')) {
          filterVal = 'Europe';
        } else if (t.includes('na') || t.includes('north') || t.includes('america')) {
          filterVal = 'North America';
        } else if (t.includes('apac') || t.includes('asia') || t.includes('pacific')) {
          filterVal = 'Asia Pacific';
        } else if (t.includes('latam') || t.includes('latin')) {
          filterVal = 'Latin America';
        } else if (t.includes('mea') || t.includes('middle east') || t.includes('east')) {
          filterVal = 'Middle East';
        } else if (t.includes('month') || t.includes('last')) {
          filterVal = 'Last Month';
        } else if (t.includes('quarter') || t.includes('q')) {
          filterVal = t.includes('q1') ? 'Q1' : t.includes('q2') ? 'Q2' : t.includes('q3') ? 'Q3' : t.includes('q4') ? 'Q4' : 'Current Quarter';
        } else if (t.includes('year') || t.includes('annual')) {
          filterVal = 'This Year';
        } else {
          filterVal = t.charAt(0).toUpperCase() + t.slice(1);
        }
        state.filters[intent.context?.view || state.currentView || 'revenue'] = filterVal;
        setContext({view: state.currentView || 'revenue', filters: {...state.filters}});
        speak('Filtered to ' + filterVal);
        showFeedback('Filter applied: ' + filterVal);
        break;
      }
      case 'compare': {
        const items = intent.items || [];
        speak('Comparing ' + items.join(' and '));
        showFeedback('Comparison: ' + items.join(' vs '));
        // visual cue: dim chart, show comparison overlay
        if (items.length >= 2) {
          const compChart = chartData.map(d => {
            const match = items.some(it => d.label.toLowerCase().includes(it.toLowerCase().slice(0,2)));
            return {...d, color: match ? '#48bb78' : '#2d3748', value: match ? d.value * 1.3 : d.value * 0.4};
          });
          renderChart(compChart, 'Comparison: ' + items.join(' vs '));
        }
        break;
      }
      case 'alert': {
        speak('Alert set: ' + intent.metric + ' ' + intent.operator + ' ' + intent.threshold + ' percent');
        showFeedback('Alert active: ' + intent.metric + ' ' + intent.operator + ' ' + intent.threshold + '%');
        break;
      }
      case 'export': {
        const fmt = intent.format.toUpperCase();
        speak('Exporting view as ' + fmt);
        showFeedback('Exporting as ' + fmt + '... done');
        break;
      }
      case 'sort': {
        speak('Sorting by ' + intent.field + ' ' + intent.direction);
        showFeedback('Sorted by ' + intent.field + ' (' + intent.direction + ')');
        break;
      }
      case 'query': {
        speak('Showing data for ' + intent.text);
        showFeedback('Query: ' + intent.text);
        break;
      }
      case 'reset': {
        state.filters = {};
        setContext({view: state.currentView || 'revenue'});
        renderInitial();
        speak('Reset complete');
        break;
      }
      case 'error': {
        speak(intent.reason || 'Could not parse that command');
        showFeedback(intent.reason || 'Command not recognized');
        break;
      }
      default: {
        speak('Command not recognized. Try saying show revenue by region');
        showFeedback('Unknown command');
        break;
      }
    }
    state.commandHistory.push(raw);
    commandHistory.textContent = 'Last: ' + raw;
    addVoiceHistory(raw, 'ok');
  }
  // ----------------------------------------------------------------
  // Speech Recognition
  // ----------------------------------------------------------------
  let recognition = null;
  let recognitionRestartTimer = null;
  let silenceTimer = null;
  let isManualStop = false;
  function initRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setStatus('error', 'Speech API not supported');
      micButton.disabled = true;
      return null;
    }
    const rec = new SpeechRecognition();
    rec.continuous = true;
    rec.interimResults = true;
    rec.lang = 'en-US';
    rec.maxAlternatives = 3;
    return rec;
  }
  function startListening() {
    isManualStop = false;
    if (!recognition) recognition = initRecognition();
    if (!recognition) return;
    try {
      recognition.start();
      state.listening = true;
      setStatus('listening', 'Listening...', 0);
      micButton.classList.add('listening');
      interimDisplay.textContent = 'Listening for voice commands...';
      commandSuggestions.classList.add('active');
    } catch (e) {
      // already started
    }
  }
  function stopListening() {
    isManualStop = true;
    if (recognition) {
      try { recognition.stop(); } catch(e) {}
    }
    state.listening = false;
    setStatus('idle', 'Voice idle', 0);
    micButton.classList.remove('listening');
    interimDisplay.textContent = '--';
    commandSuggestions.classList.remove('active');
    clearTimeout(silenceTimer);
  }
  function toggleListening() {
    if (state.listening) {
      stopListening();
    } else {
      startListening();
    }
  }
  function setupRecognition() {
    recognition = initRecognition();
    if (!recognition) return;
    recognition.onstart = () => {
      state.listening = true;
      setStatus('listening', 'Listening...', 0);
      micButton.classList.add('listening');
      interimDisplay.textContent = 'Listening...';
      commandSuggestions.classList.add('active');
    };
    recognition.onend = () => {
      if (!isManualStop && state.listening) {
        // auto-restart for continuous listening
        clearTimeout(recognitionRestartTimer);
        recognitionRestartTimer = setTimeout(() => {
          if (!isManualStop) {
            try { recognition.start(); } catch(e) {}
          }
        }, 300);
      } else {
        state.listening = false;
        setStatus('idle', 'Voice idle', 0);
        micButton.classList.remove('listening');
        interimDisplay.textContent = '--';
        commandSuggestions.classList.remove('active');
      }
    };
    recognition.onerror = (e) => {
      if (e.error === 'no-speech') return; // handled by timeout
      if (e.error === 'aborted') return;
      setStatus('error', 'Error: ' + e.error);
      if (!isManualStop) {
        setTimeout(() => {
          if (!isManualStop) {
            try { recognition.start(); } catch(e) {}
          }
        }, 500);
      }
    };
    recognition.onresult = (e) => {
      let finalTranscript = '';
      let interimTranscript = '';
      let maxConfidence = 0;
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const result = e.results[i];
        if (result.isFinal) {
          finalTranscript += result[0].transcript;
          maxConfidence = Math.max(maxConfidence, result[0].confidence);
        } else {
          interimTranscript += result[0].transcript;
          maxConfidence = Math.max(maxConfidence, result[0].confidence);
        }
      }
      state.interimText = interimTranscript || '';
      interimDisplay.textContent = interimTranscript ? '> ' + interimTranscript : finalTranscript ? '> ' + finalTranscript : '...';
      if (maxConfidence > 0) setStatus('listening', 'Listening...', maxConfidence);
      // Reset silence timer
      clearTimeout(silenceTimer);
      silenceTimer = setTimeout(() => {
        if (state.listening && !state.interimText) {
          // idle hint
        }
      }, 3000);
      // Process final transcript
      if (finalTranscript.trim()) {
        const intent = parseIntent(finalTranscript);
        executeIntent(intent);
      }
    };
  }
  // ----------------------------------------------------------------
  // Suggestions fade on inactivity
  // ----------------------------------------------------------------
  let suggestionFadeTimer = null;
  function resetSuggestionFade() {
    commandSuggestions.classList.add('active');
    clearTimeout(suggestionFadeTimer);
    suggestionFadeTimer = setTimeout(() => {
      if (!state.listening) commandSuggestions.classList.remove('active');
    }, 8000);
  }
  document.addEventListener('click', resetSuggestionFade);
  document.addEventListener('keydown', resetSuggestionFade);
  resetSuggestionFade();
  // ----------------------------------------------------------------
  // Keyboard shortcut: Ctrl+M or Ctrl+Shift+M for mic toggle
  // ----------------------------------------------------------------
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
      e.preventDefault();
      toggleListening();
    }
  });
  // ----------------------------------------------------------------
  // Init
  // ----------------------------------------------------------------
  micButton.addEventListener('click', toggleListening);
  renderInitial();
  setContext({view:'revenue'});
  // Clickable command suggestions
  $$('.command-suggestions .cmd').forEach(el => {
    el.addEventListener('click', () => {
      const cmd = el.textContent;
      const intent = parseIntent(cmd);
      executeIntent(intent);
    });
  });
  // Clickable command list items
  $$('.voice-commands-panel .cmd-item').forEach(el => {
    el.style.cursor = 'pointer';
    el.addEventListener('click', () => {
      const cmd = el.textContent.replace(/['"]/g, '');
      const intent = parseIntent(cmd);
      executeIntent(intent);
    });
  });
  // Setup recognition on first interaction
  let recognitionReady = false;
  function ensureRecognition() {
    if (!recognitionReady) {
      setupRecognition();
      recognitionReady = true;
    }
  }
  document.addEventListener('click', ensureRecognition, {once: true});
  document.addEventListener('keydown', ensureRecognition, {once: true});
  // Start listening automatically after initial setup (with user gesture requirement)
  setTimeout(() => {
    ensureRecognition();
    // Browser requires user gesture before starting SpeechRecognition
    // so we wait for first click
  }, 500);
  console.log('Voice Command Dashboard initialized');
  console.log('Press Ctrl+M to toggle microphone');
  console.log('Commands: show <metric> by <dimension>, filter to <value>, compare <a> and <b>, export as <format>, alert me when <metric> exceeds <n>');
})();
</script>
</body>
</html>
```