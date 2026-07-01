```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Styde Forge — AI Copilot Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js">
</script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0f1117;--bg2:#1a1d27;--bg3:#252836;--border:#2e3142;--text:#e4e6ef;
  --text2:#8b8fa3;--accent:#6c5ce7;--accent2:#a29bfe;--success:#00b894;
  --warning:#fdcb6e;--danger:#e17055;--radius:10px;--font:'Inter',system-ui,sans-serif
}
body{background:var(--bg);color:var(--text);font-family:var(--font);height:100vh;overflow:hidden}
.dashboard{display:grid;grid-template-columns:240px 1fr;height:100vh}
/* sidebar */
.sidebar{background:var(--bg2);border-right:1px solid var(--border);padding:20px 16px;display:flex;flex-direction:column;gap:24px}
.logo{font-size:18px;font-weight:700;color:var(--accent2);display:flex;align-items:center;gap:10px}
.logo i{font-size:22px}
.nav{display:flex;flex-direction:column;gap:4px}
.nav-item{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:8px;color:var(--text2);font-size:14px;font-weight:500;cursor:pointer;transition:all .15s}
.nav-item:hover,.nav-item.active{background:var(--bg3);color:var(--text)}
.nav-item.active{color:var(--accent2)}
.nav-item i{width:18px;text-align:center;font-size:15px}
.sidebar-footer{margin-top:auto;padding-top:16px;border-top:1px solid var(--border);font-size:12px;color:var(--text2)}
/* main */
.main{display:grid;grid-template-rows:auto 1fr auto;overflow:hidden}
.topbar{display:flex;align-items:center;justify-content:space-between;padding:12px 24px;border-bottom:1px solid var(--border);background:var(--bg2)}
.topbar-left{display:flex;align-items:center;gap:16px}
.topbar-left h1{font-size:16px;font-weight:600}
.date-range{display:flex;align-items:center;gap:8px;padding:6px 12px;background:var(--bg3);border-radius:6px;font-size:13px;color:var(--text2);cursor:pointer}
.date-range i{font-size:12px}
.topbar-right{display:flex;align-items:center;gap:12px}
.filter-chip{display:flex;align-items:center;gap:6px;padding:6px 12px;background:var(--bg3);border-radius:6px;font-size:13px;color:var(--text2);cursor:pointer}
.filter-chip i{font-size:12px}
/* content */
.content{overflow-y:auto;padding:24px}
.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}
.kpi-card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px}
.kpi-label{font-size:12px;font-weight:500;color:var(--text2);margin-bottom:4px}
.kpi-value{font-size:28px;font-weight:700;line-height:1.2}
.kpi-change{font-size:12px;margin-top:4px;display:flex;align-items:center;gap:4px}
.kpi-change.up{color:var(--success)}
.kpi-change.down{color:var(--danger)}
.charts-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:24px}
.chart-card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:20px}
.chart-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.chart-header h3{font-size:14px;font-weight:600}
.chart-header span{font-size:12px;color:var(--text2)}
.chart-container{position:relative;height:280px}
.chart-container canvas{width:100%!important;height:100%!important}
.insights-row{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.insight-card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;display:flex;align-items:flex-start;gap:12px}
.insight-card i{font-size:18px;color:var(--accent2);margin-top:2px;flex-shrink:0}
.insight-card p{font-size:13px;line-height:1.5;color:var(--text)}
.insight-card small{display:block;margin-top:4px;font-size:11px;color:var(--text2)}
/* copilot panel */
.copilot-overlay{position:fixed;top:0;right:0;bottom:0;width:420px;background:var(--bg2);border-left:1px solid var(--border);z-index:100;display:flex;flex-direction:column;transform:translateX(100%);transition:transform .3s cubic-bezier(.4,0,.2,1);box-shadow:-8px 0 30px rgba(0,0,0,.4)}
.copilot-overlay.open{transform:translateX(0)}
.copilot-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px;border-bottom:1px solid var(--border)}
.copilot-header h2{font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px}
.copilot-header h2 i{color:var(--accent2)}
.copilot-close{background:none;border:none;color:var(--text2);font-size:18px;cursor:pointer;padding:4px;border-radius:6px}
.copilot-close:hover{background:var(--bg3);color:var(--text)}
.copilot-context{display:flex;gap:8px;padding:10px 20px;border-bottom:1px solid var(--border);flex-wrap:wrap}
.context-badge{display:flex;align-items:center;gap:6px;padding:4px 10px;background:var(--bg3);border-radius:20px;font-size:11px;color:var(--text2)}
.context-badge i{font-size:10px}
.copilot-messages{flex:1;overflow-y:auto;padding:16px 20px;display:flex;flex-direction:column;gap:12px}
.message{max-width:88%;padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.5;animation:msgIn .2s ease}
@keyframes msgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.message.user{background:var(--accent);color:#fff;align-self:flex-end;border-bottom-right-radius:4px}
.message.bot{background:var(--bg3);color:var(--text);align-self:flex-start;border-bottom-left-radius:4px}
.message.bot .msg-label{font-size:10px;font-weight:600;color:var(--accent2);margin-bottom:4px;text-transform:uppercase;letter-spacing:.5px}
.message.bot .chart-mini{margin-top:8px;height:140px;background:var(--bg);border-radius:8px;padding:8px;position:relative}
.message.bot .chart-mini canvas{width:100%!important;height:100%!important}
.message.bot .callout{padding:8px 10px;background:var(--bg2);border-left:3px solid var(--accent2);border-radius:4px;margin-top:6px;font-size:12px;color:var(--text2)}
.message.error{background:rgba(225,112,85,.15);color:var(--danger);align-self:flex-start;border-bottom-left-radius:4px;border:1px solid rgba(225,112,85,.3)}
.message.system{background:var(--bg3);color:var(--text2);align-self:center;font-size:11px;text-align:center;padding:6px 14px;border-radius:20px;opacity:.7}
.suggested-row{display:flex;gap:8px;padding:10px 20px;border-top:1px solid var(--border);flex-wrap:wrap}
.suggested-chip{display:flex;align-items:center;gap:6px;padding:6px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:20px;font-size:12px;color:var(--text2);cursor:pointer;transition:all .15s}
.suggested-chip:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.suggested-chip i{font-size:10px}
.copilot-input{display:flex;align-items:center;gap:8px;padding:12px 16px;border-top:1px solid var(--border);background:var(--bg3)}
.copilot-input input{flex:1;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px 14px;font-size:13px;color:var(--text);font-family:var(--font);outline:none}
.copilot-input input:focus{border-color:var(--accent)}
.copilot-input input::placeholder{color:var(--text2)}
.copilot-input button{background:var(--accent);border:none;color:#fff;width:36px;height:36px;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s;flex-shrink:0;font-size:14px}
.copilot-input button:hover{background:var(--accent2)}
.copilot-input button:disabled{opacity:.4;cursor:not-allowed}
.copilot-input button.mic{background:var(--bg)}
.copilot-input button.mic:hover{background:var(--bg3)}
.copilot-input button.mic.listening{background:var(--danger);animation:pulse 1s infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}
/* copilot toggle button */
.copilot-toggle{position:fixed;bottom:24px;right:24px;width:48px;height:48px;border-radius:50%;background:var(--accent);color:#fff;border:none;font-size:18px;cursor:pointer;z-index:99;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(108,92,231,.4);transition:all .2s}
.copilot-toggle:hover{transform:scale(1.08);box-shadow:0 6px 24px rgba(108,92,231,.5)}
/* empty state */
.empty-state{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:var(--text2);text-align:center;gap:8px}
.empty-state i{font-size:40px;opacity:.3;margin-bottom:8px}
.empty-state p{font-size:14px;max-width:260px;line-height:1.5}
/* loading dots */
.typing{display:flex;gap:4px;padding:4px 0}
.typing span{width:6px;height:6px;border-radius:50%;background:var(--text2);animation:bounce 1.2s infinite}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-4px)}}
/* scrollbar */
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--text2)}
@media(max-width:1024px){
  .kpi-row{grid-template-columns:repeat(2,1fr)}
  .charts-row{grid-template-columns:1fr}
  .insights-row{grid-template-columns:1fr}
  .copilot-overlay{width:100%}
  .dashboard{grid-template-columns:1fr}
  .sidebar{display:none}
}
</style>
</head>
<body>
<div class="dashboard">
  <!-- sidebar -->
  <aside class="sidebar">
    <div class="logo"><i class="fas fa-robot"></i> Styde Forge</div>
    <nav class="nav">
      <div class="nav-item active"><i class="fas fa-chart-simple"></i> Overview</div>
      <div class="nav-item"><i class="fas fa-chart-line"></i> Revenue</div>
      <div class="nav-item"><i class="fas fa-users"></i> Customers</div>
      <div class="nav-item"><i class="fas fa-cubes"></i> Products</div>
      <div class="nav-item"><i class="fas fa-flag"></i> Segments</div>
      <div class="nav-item"><i class="fas fa-gear"></i> Settings</div>
    </nav>
    <div class="sidebar-footer">
      <div style="display:flex;align-items:center;gap:6px">
        <i class="fas fa-circle" style="color:var(--success);font-size:8px"></i>
        All systems nominal
      </div>
    </div>
  </aside>
  <!-- main area -->
  <div class="main">
    <header class="topbar">
      <div class="topbar-left">
        <h1>Overview</h1>
        <div class="date-range"><i class="fas fa-calendar"></i> Last 30 days <i class="fas fa-chevron-down" style="font-size:10px"></i></div>
      </div>
      <div class="topbar-right">
        <div class="filter-chip"><i class="fas fa-filter"></i> Region: All</div>
        <div class="filter-chip"><i class="fas fa-tag"></i> Plan: All</div>
        <div class="filter-chip"><i class="fas fa-rotate"></i> Refresh</div>
      </div>
    </header>
    <div class="content">
      <!-- KPI row -->
      <div class="kpi-row">
        <div class="kpi-card">
          <div class="kpi-label">Total Revenue</div>
          <div class="kpi-value">$284,500</div>
          <div class="kpi-change up"><i class="fas fa-arrow-up"></i> 12.3% vs last period</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Active Customers</div>
          <div class="kpi-value">1,847</div>
          <div class="kpi-change up"><i class="fas fa-arrow-up"></i> 8.1% vs last period</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Avg. MRR per Customer</div>
          <div class="kpi-value">$154</div>
          <div class="kpi-change up"><i class="fas fa-arrow-up"></i> 3.7% vs last period</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">Churn Rate</div>
          <div class="kpi-value">2.1%</div>
          <div class="kpi-change down"><i class="fas fa-arrow-down"></i> 0.4pp vs last period</div>
        </div>
      </div>
      <!-- charts row -->
      <div class="charts-row">
        <div class="chart-card">
          <div class="chart-header"><h3>Revenue Trend</h3><span>Daily | <i class="fas fa-download" style="cursor:pointer"></i></span></div>
          <div class="chart-container"><canvas id="revenueChart"></canvas></div>
        </div>
        <div class="chart-card">
          <div class="chart-header"><h3>Customers by Plan</h3><span>Tier breakdown</span></div>
          <div class="chart-container"><canvas id="planChart"></canvas></div>
        </div>
      </div>
      <!-- insights row -->
      <div class="insights-row">
        <div class="insight-card">
          <i class="fas fa-bolt"></i>
          <div>
            <p>Revenue spiked on <strong>Jun 15</strong> to $14,200 — driven by 37 Enterprise upgrades after the Q2 product launch.</p>
            <small><i class="fas fa-clock"></i> Detected 2h ago</small>
          </div>
        </div>
        <div class="insight-card">
          <i class="fas fa-triangle-exclamation"></i>
          <div>
            <p>Churn increased to 2.1% this week. 3 accounts on the Basic plan downgraded. Consider a retention campaign.</p>
            <small><i class="fas fa-clock"></i> Detected 4h ago</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- copilot fab -->
<button class="copilot-toggle" id="copilotToggle" aria-label="Open AI Copilot">
  <i class="fas fa-comment-dots"></i>
</button>
<!-- copilot panel -->
<div class="copilot-overlay" id="copilotPanel">
  <div class="copilot-header">
    <h2><i class="fas fa-robot"></i> AI Copilot</h2>
    <button class="copilot-close" id="copilotClose" aria-label="Close copilot"><i class="fas fa-xmark"></i></button>
  </div>
  <div class="copilot-context" id="copilotContext">
    <span class="context-badge"><i class="fas fa-calendar"></i> Last 30 days</span>
    <span class="context-badge"><i class="fas fa-globe"></i> Region: All</span>
    <span class="context-badge"><i class="fas fa-chart-simple"></i> Overview tab</span>
  </div>
  <div class="copilot-messages" id="copilotMessages">
    <div class="message bot">
      <div class="msg-label"><i class="fas fa-robot"></i> Copilot</div>
      Hello. I am your AI copilot. Ask me anything about your data — trends, comparisons, top customers, or what caused a spike. I see your current filters and can visualize results instantly.
      <div class="callout"><i class="fas fa-lightbulb"></i> Try: "What caused the revenue spike on Jun 15?" or "Show top 5 customers by MRR"</div>
    </div>
  </div>
  <div class="suggested-row" id="suggestedRow"></div>
  <div class="copilot-input" id="copilotInputBar">
    <button class="mic" id="micBtn" aria-label="Voice input"><i class="fas fa-microphone"></i></button>
    <input type="text" id="chatInput" placeholder="Ask anything about your data..." autocomplete="off">
    <button id="sendBtn" aria-label="Send message"><i class="fas fa-paper-plane"></i></button>
  </div>
</div>
<script>
/* ============================================================
   STATE & PERSISTENCE
   ============================================================ */
const STATE_KEY = 'stydeforge_copilot_state_v1';
const HISTORY_KEY = 'stydeforge_chat_history_v1';
function loadState() {
  try {
    return JSON.parse(localStorage.getItem(STATE_KEY)) || { panelOpen: false, messageCount: 0 };
  } catch { return { panelOpen: false, messageCount: 0 }; }
}
function saveState(s) {
  try { localStorage.setItem(STATE_KEY, JSON.stringify(s)); } catch {}
}
function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
  } catch { return []; }
}
function saveHistory(msgs) {
  try {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(msgs.slice(-100))); // keep last 100
  } catch {}
}
let appState = loadState();
let chatHistory = loadHistory();
/* ============================================================
   SYNTHETIC DATA
   ============================================================ */
const revenueData = {
  labels: Array.from({length:30},(_,i)=>'Jun '+(i+1)),
  values: [8200,8400,8100,8600,8900,9100,8700,8500,8800,9200,9400,9600,
           10100,10800,14200,13800,12500,11900,11500,11200,11800,12200,
           12800,13100,12700,12400,12000,12600,13000,13500]
};
const planData = {
  labels: ['Basic','Pro','Enterprise','Starter'],
  values: [580,420,310,537]
};
const topCustomers = [
  {name:'Acme Corp',mrr:12400,plan:'Enterprise'},
  {name:'Globex Inc',mrr:9800,plan:'Enterprise'},
  {name:'Initech',mrr:7500,plan:'Pro'},
  {name:'Hooli',mrr:6200,plan:'Enterprise'},
  {name:'Cyberdyne',mrr:5100,plan:'Pro'}
];
/* ============================================================
   NL QUERY PARSER — structured intent/entity extraction
   ------------------------------------------------------------
   Uses regex-based keyword extraction with fallback to fuzzy matching.
   Never uses naive switch-case on the query string.
   ============================================================ */
const INTENT_PATTERNS = [
  {
    name: 'trend_analysis',
    label: 'Trend Analysis',
    patterns: [
      /trend/i, /over\s*time/i, /trajectory/i, /movement/i, /direction/i,
      /going\s*up/i, /going\s*down/i, /increasing/i, /decreasing/i,
      /growth/i, /decline/i, /rise/i, /drop/i, /spike/i, /surge/i,
      /dip/i, /pattern/i
    ],
    priority: 3
  },
  {
    name: 'comparison',
    label: 'Comparison',
    patterns: [
      /compare/i, /versus/i, /vs/i, /against/i, /side.?by.?side/i,
      /difference/i, /better/i, /worse/i, /outperform/i,
      /this\s*(quarter|month|week|year)\s*(vs|versus|compared\s*to)/i,
      /last\s*(quarter|month|week|year)/i
    ],
    priority: 4
  },
  {
    name: 'top_n',
    label: 'Top N / Ranking',
    patterns: [
      /top\s*\d+/i, /best/i, /leading/i, /highest/i, /largest/i,
      /biggest/i, /most/i, /worst/i, /bottom\s*\d+/i, /lowest/i,
      /rank/i, /ranking/i, /sorted/i, /order/i
    ],
    priority: 5
  },
  {
    name: 'causation',
    label: 'Root Cause / Why',
    patterns: [
      /why/i, /what\s*caused/i, /what\s*led\s*to/i, /reason/i,
      /because/i, /explain/i, /driver/i, /behind/i, /root\s*cause/i,
      /what\s*triggered/i, /what\s*happened/i
    ],
    priority: 6
  },
  {
    name: 'metric_query',
    label: 'Metric Query',
    patterns: [
      /(how\s*much|how\s*many|what\s*is|what\s*are|show\s*me|give\s*me)/i,
      /total/i, /count/i, /sum/i, /average/i, /mean/i, /median/i,
      /mrr/i, /revenue/i, /churn/i, /customers?/i, /users?/i,
      /conversion/i, /retention/i, /arpu/i
    ],
    priority: 2
  },
  {
    name: 'forecast',
    label: 'Forecast / Prediction',
    patterns: [
      /forecast/i, /predict/i, /projection/i, /predict/i, /will\s*be/i,
      /expect/i, /estimate/i, /future/i, /next\s*(month|quarter|year)/i,
      /outlook/i
    ],
    priority: 1
  },
  {
    name: 'anomaly',
    label: 'Anomaly Detection',
    patterns: [
      /anomal/i, /outlier/i, /unusual/i, /unexpected/i, /abnormal/i,
      /strange/i, /weird/i, /odd/i, /spike/i, /drop/i, /sudden/i,
      /something\s*(wrong|off|different)/i
    ],
    priority: 1
  }
];
const ENTITY_PATTERNS = [
  { type: 'metric', patterns: [/revenue/i, /mrr/i, /churn/i, /customers?/i, /users?/i, /profit/i, /margin/i, /conversion/i, /retention/i, /growth/i, /spend/i, /cost/i, /sales/i] },
  { type: 'timeframe', patterns: [/(last\s*\d+\s*(day|days|week|weeks|month|months|quarter|quarters|year|years))/i, /(this\s*(month|week|quarter|year))/i, /(today|yesterday)/i, /(q[1-4]|quarter\s*[1-4])/i, /(\d{4})/i] },
  { type: 'segment', patterns: [/(basic|pro|enterprise|starter|free|premium|standard)/i, /(enterprise|small\s*business|mid.?market|smb)/i, /(north\s*america|europe|apac|latam|emea)/i, /(region|segment|tier|plan|cohort)/i] },
  { type: 'comparison_target', patterns: [/(last\s*(month|week|quarter|year))/i, /(previous|prior|past)/i, /(\d{4})\s*vs/i] },
  { type: 'number', patterns: [/top\s*(\d+)/i, /bottom\s*(\d+)/i, /(\d+)\s*(customers?|users?|days?|months?|weeks?)/i] }
];
// Simple Levenshtein for fuzzy fallback
function levenshtein(a,b){
  const m=a.length,n=b.length;
  const d=Array.from({length:m+1},(_,i)=>[i]);
  for(let j=0;j<=n;j++) d[0][j]=j;
  for(let i=1;i<=m;i++) for(let j=1;j<=n;j++){
    d[i][j]=a[i-1]===b[j-1]?d[i-1][j-1]:1+Math.min(d[i-1][j],d[i][j-1],d[i-1][j-1]);
  }
  return d[m][n];
}
const FUZZY_LEXICON = [
  ['revenue','mrr','income','sales','earnings'],
  ['customers','clients','users','accounts','subscribers'],
  ['churn','attrition','cancellations','dropout'],
  ['trend','pattern','trajectory','movement','direction'],
  ['compare','versus','vs','difference','delta'],
  ['spike','surge','jump','peak','outlier'],
  ['top','leading','best','highest','biggest'],
  ['growth','increase','rise','gain','upswing'],
  ['decline','decrease','drop','fall','downswing']
];
function fuzzyMatchTerm(term){
  const lower=term.toLowerCase();
  let best={word:null,dist:Infinity};
  for(const group of FUZZY_LEXICON){
    for(const w of group){
      const d=levenshtein(lower,w);
      if(d<best.dist && d<=Math.ceil(w.length*0.35)){
        best={word:w,dist:d};
      }
    }
  }
  return best.word;
}
function extractEntities(query) {
  const entities = { metric: null, timeframe: null, segment: null, comparison_target: null, number: null };
  for (const ent of ENTITY_PATTERNS) {
    for (const pat of ent.patterns) {
      const m = query.match(pat);
      if (m) {
        if (ent.type === 'number' && m[1]) {
          entities.number = parseInt(m[1], 10);
        } else {
          entities[ent.type] = entities[ent.type] || m[0];
        }
        break;
      }
    }
  }
  // fuzzy fallback: tokenize query and check each word
  if (!entities.metric) {
    const tokens = query.toLowerCase().split(/\s+/).filter(t=>t.length>3);
    for (const t of tokens) {
      const fuzzy = fuzzyMatchTerm(t);
      if (fuzzy && ['revenue','customers','churn','growth','decline','spike','trend','compare','top'].includes(fuzzy)) {
        entities.metric = fuzzy;
        break;
      }
    }
  }
  return entities;
}
function classifyIntent(query) {
  const scores = [];
  for (const intent of INTENT_PATTERNS) {
    let score = 0;
    for (const pat of intent.patterns) {
      if (pat.test(query)) score += intent.priority;
    }
    if (score > 0) scores.push({ intent: intent.name, label: intent.label, score });
  }
  // fuzzy fallback for intents
  if (scores.length === 0) {
    const tokens = query.toLowerCase().split(/\s+/).filter(t=>t.length>3);
    for (const t of tokens) {
      const fuzzy = fuzzyMatchTerm(t);
      if (fuzzy) {
        for (const intent of INTENT_PATTERNS) {
          for (const pat of intent.patterns) {
            if (pat.test(fuzzy)) {
              scores.push({ intent: intent.name, label: intent.label, score: 1 });
              break;
            }
          }
          if (scores.length > 0) break;
        }
      }
      if (scores.length > 0) break;
    }
  }
  scores.sort((a,b)=>b.score-a.score);
  return scores.length > 0 ? scores[0].intent : 'general';
}
/* ============================================================
   RESPONSE GENERATOR
   ============================================================ */
function generateResponse(query) {
  const intent = classifyIntent(query);
  const entities = extractEntities(query);
  const lower = query.toLowerCase();
  // error handling: empty input
  if (!query || query.trim().length === 0) {
    return { type: 'error', text: 'Please enter a question. I can help with trends, comparisons, top customers, and more.' };
  }
  // malformed input: gibberish detection (very basic)
  if (query.trim().length < 3) {
    return { type: 'error', text: 'That looks like a very short input. Try asking something like "What is the revenue trend?" or "Top 5 customers".' };
  }
  const alphaRatio = (query.match(/[a-zA-Z]/g)||[]).length / query.length;
  if (alphaRatio < 0.3 && query.length > 5) {
    return { type: 'error', text: "I couldn't parse that query. It contains mostly symbols or numbers. Try phrasing it as a natural question." };
  }
  try {
    switch(intent) {
      case 'causation': {
        if (lower.includes('spike') || lower.includes('surge') || lower.includes('jun 15') || lower.includes('15th')) {
          return {
            type: 'chart',
            text: 'The revenue spike on June 15 reached $14,200, a 31% increase over the previous day. This was driven by 37 Enterprise plan upgrades following the Q2 product launch.',
            chartType: 'line',
            chartData: {
              labels: revenueData.labels.slice(12,20),
              values: revenueData.values.slice(12,20)
            },
            callout: 'Enterprise upgrades accounted for 74% of the spike. Pro plan had a 12% lift as well.',
            trend: 'up'
          };
        }
        return {
          type: 'text',
          text: 'I see the main drivers for the current period: Enterprise segment grew 18% MoM, and the Q2 product launch correlated with a 31% revenue day on Jun 15. Would you like me to drill deeper into a specific metric?'
        };
      }
      case 'top_n': {
        const count = entities.number || 5;
        const items = topCustomers.slice(0, Math.min(count, topCustomers.length));
        const labels = items.map(c=>c.name);
        const values = items.map(c=>c.mrr);
        return {
          type: 'chart',
          text: `Here are the top ${items.length} customers by MRR.`,
          chartType: 'bar',
          chartData: { labels, values },
          callout: `Total MRR from top ${items.length}: $${values.reduce((a,b)=>a+b,0).toLocaleString()}`,
          trend: null
        };
      }
      case 'comparison': {
        const currentTotal = revenueData.values.slice(-7).reduce((a,b)=>a+b,0);
        const prevTotal = revenueData.values.slice(-14,-7).reduce((a,b)=>a+b,0);
        const diff = currentTotal - prevTotal;
        const pct = ((diff / prevTotal) * 100).toFixed(1);
        return {
          type: 'chart',
          text: `Comparing this week (${revenueData.labels.slice(-7)[0]}–${revenueData.labels.slice(-1)[0]}) to the previous week:`,
          chartType: 'bar',
          chartData: {
            labels: ['Previous Week', 'This Week'],
            values: [prevTotal, currentTotal]
          },
          callout: `${diff > 0 ? 'Increase' : 'Decrease'} of $${Math.abs(diff).toLocaleString()} (${pct}%)`,
          trend: diff > 0 ? 'up' : 'down'
        };
      }
      case 'trend_analysis':
      case 'anomaly': {
        return {
          type: 'chart',
          text: intent === 'anomaly'
            ? 'I scanned the data for anomalies. The most significant outlier was on June 15 ($14,200 — 31% above trend). A minor dip on June 18 ($11,500) followed.'
            : 'Here is the revenue trend over the selected period. Overall growth direction is positive with a notable spike mid-month.',
          chartType: 'line',
          chartData: {
            labels: revenueData.labels,
            values: revenueData.values
          },
          callout: '30-day trend: starting at $8,200, ending at $13,500 — net change: +64.6%',
          trend: 'up'
        };
      }
      case 'forecast': {
        const last7 = revenueData.values.slice(-7);
        const avg = Math.round(last7.reduce((a,b)=>a+b,0) / last7.length);
        const projected = Math.round(avg * 1.05);
        return {
          type: 'chart',
          text: `Based on the last 7 days (avg $${avg.toLocaleString()}/day), the projected daily revenue for the next period is approximately $${projected.toLocaleString()} assuming 5% growth momentum.`,
          chartType: 'line',
          chartData: {
            labels: [...revenueData.labels.slice(-7), 'Projected'],
            values: [...last7, projected]
          },
          callout: `Forecast confidence: moderate (based on 7-day rolling average with 5% growth factor)`,
          trend: 'up'
        };
      }
      default: {
        // metric query or fallback
        if (lower.includes('customer') || lower.includes('user')) {
          return {
            type: 'chart',
            text: 'You currently have 1,847 active customers. Here is the distribution by plan tier.',
            chartType: 'bar',
            chartData: {
              labels: planData.labels,
              values: planData.values
            },
            callout: 'Enterprise (310) has the highest MRR per customer at $312 avg.',
            trend: null
          };
        }
        if (lower.includes('churn')) {
          return {
            type: 'text',
            text: 'Current churn rate is 2.1%, up 0.4 percentage points from last period. The increase is primarily from Basic plan accounts (3 cancellations this week). Would you like to see a churn trend chart?'
          };
        }
        // generic fallback
        return {
          type: 'chart',
          text: 'Here is an overview of your key metrics.',
          chartType: 'line',
          chartData: {
            labels: revenueData.labels,
            values: revenueData.values
          },
          callout: 'Revenue trend over the last 30 days. Ask me for comparisons, top customers, or specific metric breakdowns.',
          trend: 'up'
        };
      }
    }
  } catch (err) {
    // partial failure handling
    return {
      type: 'error',
      text: `I encountered an error processing that query: ${err.message || 'unknown error'}. Please try rephrasing your question.`
    };
  }
}
/* ============================================================
   SUGGESTED QUERIES
   ============================================================ */
const SUGGESTED_QUERIES = [
  { icon: 'fa-chart-line', text: 'What caused the revenue spike on Jun 15?' },
  { icon: 'fa-ranking-star', text: 'Show top 5 customers by MRR' },
  { icon: 'fa-code-compare', text: 'Compare this week to last week' },
  { icon: 'fa-chart-simple', text: 'Show me the revenue trend' },
  { icon: 'fa-users', text: 'How many customers do we have?' },
  { icon: 'fa-arrow-trend-up', text: 'What is the growth forecast?' }
];
function renderSuggested() {
  const row = document.getElementById('suggestedRow');
  row.innerHTML = '';
  for (const q of SUGGESTED_QUERIES) {
    const chip = document.createElement('div');
    chip.className = 'suggested-chip';
    chip.innerHTML = `<i class="fas ${q.icon}"></i> ${q.text}`;
    chip.addEventListener('click', () => sendMessage(q.text));
    row.appendChild(chip);
  }
}
/* ============================================================
   CHART RENDERING
   ============================================================ */
let activeCharts = {};
function renderMiniChart(canvasId, type, data) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return null;
  const ctx = canvas.getContext('2d');
  // destroy existing chart on this canvas
  if (activeCharts[canvasId]) {
    activeCharts[canvasId].destroy();
    delete activeCharts[canvasId];
  }
  const colors = ['#6c5ce7','#a29bfe','#00b894','#fdcb6e','#e17055','#74b9ff'];
  const config = {
    type: type === 'bar' ? 'bar' : 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: '',
        data: data.values,
        borderColor: '#a29bfe',
        backgroundColor: type === 'bar' ? colors.slice(0, data.labels.length) : 'rgba(108,92,231,0.15)',
        borderWidth: 2,
        fill: type !== 'bar',
        tension: 0.3,
        pointRadius: type === 'line' ? 2 : 0,
        pointBackgroundColor: '#a29bfe'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#8b8fa3', font: { size: 9 }, maxTicksLimit: 8 } },
        y: { grid: { color: 'rgba(46,49,66,0.5)' }, ticks: { color: '#8b8fa3', font: { size: 9 } } }
      }
    }
  };
  activeCharts[canvasId] = new Chart(ctx, config);
  return activeCharts[canvasId];
}
let mainChart1 = null;
let mainChart2 = null;
function initMainCharts() {
  const ctx1 = document.getElementById('revenueChart').getContext('2d');
  mainChart1 = new Chart(ctx1, {
    type: 'line',
    data: {
      labels: revenueData.labels,
      datasets: [{
        label: 'Revenue ($)',
        data: revenueData.values,
        borderColor: '#a29bfe',
        backgroundColor: 'rgba(108,92,231,0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.3,
        pointRadius: 3,
        pointBackgroundColor: '#6c5ce7'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: '#8b8fa3' } } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#8b8fa3', font: { size: 10 }, maxTicksLimit: 10 } },
        y: { grid: { color: 'rgba(46,49,66,0.5)' }, ticks: { color: '#8b8fa3', font: { size: 10 } } }
      }
    }
  });
  const ctx2 = document.getElementById('planChart').getContext('2d');
  mainChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
      labels: planData.labels,
      datasets: [{
        data: planData.values,
        backgroundColor: ['#6c5ce7','#a29bfe','#00b894','#fdcb6e'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: '#8b8fa3', padding: 12, font: { size: 11 } } }
      },
      cutout: '65%'
    }
  });
}
/* ============================================================
   CHAT UI
   ============================================================ */
const messagesEl = document.getElementById('copilotMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');
const toggleBtn = document.getElementById('copilotToggle');
const panel = document.getElementById('copilotPanel');
const closeBtn = document.getElementById('copilotClose');
let chartCounter = 0;
let isListening = false;
let recognition = null;
let isProcessing = false;
function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}
function addTypingIndicator() {
  const div = document.createElement('div');
  div.className = 'message bot';
  div.id = 'typingIndicator';
  div.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';
  messagesEl.appendChild(div);
  scrollToBottom();
}
function removeTypingIndicator() {
  const el = document.getElementById('typingIndicator');
  if (el) el.remove();
}
function addMessage(role, content) {
  const div = document.createElement('div');
  if (role === 'error') {
    div.className = 'message error';
    div.innerHTML = `<i class="fas fa-circle-exclamation"></i> ${content.text}`;
  } else if (role === 'system') {
    div.className = 'message system';
    div.textContent = content;
  } else if (role === 'user') {
    div.className = 'message user';
    div.textContent = content;
  } else if (role === 'assistant') {
    div.className = 'message bot';
    let html = `<div class="msg-label"><i class="fas fa-robot"></i> Copilot</div>${content.text}`;
    if (content.type === 'chart' && content.chartData) {
      const cid = 'miniChart_' + (++chartCounter);
      html += `<div class="chart-mini"><canvas id="${cid}"></canvas></div>`;
      if (content.callout) {
        html += `<div class="callout"><i class="fas fa-info-circle"></i> ${content.callout}</div>`;
      }
      div.innerHTML = html;
      messagesEl.appendChild(div);
      // render chart after DOM update
      requestAnimationFrame(() => {
        renderMiniChart(cid, content.chartType || 'line', content.chartData);
      });
      return div;
    }
    if (content.callout) {
      html += `<div class="callout"><i class="fas fa-info-circle"></i> ${content.callout}</div>`;
    }
    div.innerHTML = html;
  }
  messagesEl.appendChild(div);
  scrollToBottom();
  return div;
}
function sendMessage(text) {
  if (isProcessing) return;
  const query = (text || chatInput.value).trim();
  if (!query) return;
  isProcessing = true;
  sendBtn.disabled = true;
  chatInput.value = '';
  addMessage('user', query);
  addTypingIndicator();
  // simulate processing delay
  setTimeout(() => {
    removeTypingIndicator();
    const response = generateResponse(query);
    if (response.type === 'error') {
      addMessage('error', response);
    } else {
      addMessage('assistant', response);
    }
    // maintain history
    chatHistory.push({ role: 'user', text: query, timestamp: Date.now() });
    chatHistory.push({ role: 'assistant', text: response.text, type: response.type, timestamp: Date.now() });
    saveHistory(chatHistory);
    appState.messageCount = chatHistory.length / 2;
    saveState(appState);
    isProcessing = false;
    sendBtn.disabled = false;
    chatInput.focus();
  }, 400 + Math.random() * 600);
}
/* ============================================================
   VOICE INPUT — Web Speech API
   ============================================================ */
function initVoice() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    micBtn.style.display = 'none';
    return;
  }
  recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    chatInput.value = transcript;
    isListening = false;
    micBtn.classList.remove('listening');
    micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    sendMessage(transcript);
  };
  recognition.onerror = (event) => {
    isListening = false;
    micBtn.classList.remove('listening');
    micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    if (event.error !== 'no-speech' && event.error !== 'aborted') {
      addMessage('error', { text: 'Voice input error: ' + event.error + '. Try typing your question instead.' });
    }
  };
  recognition.onend = () => {
    isListening = false;
    micBtn.classList.remove('listening');
    micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
  };
  micBtn.addEventListener('click', () => {
    if (isListening) {
      recognition.stop();
      isListening = false;
      micBtn.classList.remove('listening');
      micBtn.innerHTML = '<i class="fas fa-microphone"></i>';
    } else {
      try {
        recognition.start();
        isListening = true;
        micBtn.classList.add('listening');
        micBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
      } catch (e) {
        addMessage('error', { text: 'Could not start voice input. ' + (e.message || '') });
      }
    }
  });
}
/* ============================================================
   KEYBOARD & EVENTS
   ============================================================ */
chatInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendMessage();
});
sendBtn.addEventListener('click', () => sendMessage());
toggleBtn.addEventListener('click', () => {
  panel.classList.toggle('open');
  appState.panelOpen = panel.classList.contains('open');
  saveState(appState);
  if (appState.panelOpen) chatInput.focus();
});
closeBtn.addEventListener('click', () => {
  panel.classList.remove('open');
  appState.panelOpen = false;
  saveState(appState);
});
/* ============================================================
   INIT
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  initMainCharts();
  renderSuggested();
  initVoice();
  // Restore panel state
  if (appState.panelOpen) {
    panel.classList.add('open');
  }
  // Restore chat history (last 5 exchanges)
  const recentHistory = chatHistory.slice(-10);
  if (recentHistory.length > 0) {
    messagesEl.innerHTML = '';
    // Keep initial greeting
    const greeting = document.createElement('div');
    greeting.className = 'message bot';
    greeting.innerHTML = `<div class="msg-label"><i class="fas fa-robot"></i> Copilot</div>Hello. I am your AI copilot. Ask me anything about your data — trends, comparisons, top customers, or what caused a spike. I see your current filters and can visualize results instantly.<div class="callout"><i class="fas fa-lightbulb"></i> Try: "What caused the revenue spike on Jun 15?" or "Show top 5 customers by MRR"</div>`;
    messagesEl.appendChild(greeting);
    for (const msg of recentHistory) {
      if (msg.role === 'user') {
        addMessage('user', msg.text);
      }
    }
  }
  // Handle resize for charts
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      for (const key in activeCharts) {
        if (activeCharts[key] && activeCharts[key].resize) {
          activeCharts[key].resize();
        }
      }
      if (mainChart1 && mainChart1.resize) mainChart1.resize();
      if (mainChart2 && mainChart2.resize) mainChart2.resize();
    }, 200);
  });
});
</script>
</body>
</html>
```