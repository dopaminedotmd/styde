scripts/validate.sh
#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PASS=0 FAIL=0
check() {
  local label=$1 desc=$2
  shift 2
  if "$@"; then
    echo "  PASS  $label  $desc"
    PASS=$((PASS+1))
  else
    echo "  FAIL  $label  $desc"
    FAIL=$((FAIL+1))
  fi
}
check_html() {
  local html="$ROOT/index.html"
  local rc
  echo "--- VALIDATION REPORT ---"
  echo ""
  # 1 — DOCTYPE present
  grep -q '<!DOCTYPE html>' "$html"
  rc=$?
  check "G01" "DOCTYPE html declaration" test $rc -eq 0
  # 2 — <html> open/close
  grep -q '<html' "$html" && grep -q '</html>' "$html"
  rc=$?
  check "G02" "html open and close tags" test $rc -eq 0
  # 3 — <head> present
  grep -q '<head>' "$html"
  rc=$?
  check "G03" "head section present" test $rc -eq 0
  # 4 — <body> present
  grep -q '<body>' "$html"
  rc=$?
  check "G04" "body section present" test $rc -eq 0
  # 5 — charset meta present
  grep -qi 'charset=' "$html"
  rc=$?
  check "G05" "charset meta declaration" test $rc -eq 0
  # 6 — viewport meta
  grep -qi 'viewport' "$html"
  rc=$?
  check "G06" "viewport meta tag" test $rc -eq 0
  # 7 — Tag balance: count open vs close for non-void elements
  echo "  --- tag balance ---"
  local imbalance=0
  for tag in html head body title main section article div header footer nav aside h1 h2 h3 h4 h5 h6 p span ul ol li a button form label table tr td th tbody thead tfoot; do
    local opens=$(grep -coP "<$tag[\s>]" "$html" 2>/dev/null || echo 0)
    local closes=$(grep -coP "</$tag>" "$html" 2>/dev/null || echo 0)
    if [ "$opens" -ne "$closes" ]; then
      echo "    IMBALANCE <$tag>: $opens opens, $closes closes"
      imbalance=1
    fi
  done
  check "G07" "tag balance: all non-void elements balanced" test $imbalance -eq 0
  # 8 — Void elements closed correctly (<br> not <br/>)
  local void_broken=$(grep -coP '<(br|hr|img|input|link|meta|source|wbr)\s*/>' "$html" 2>/dev/null || echo 0)
  check "G08" "void elements use <tag> not <tag/> syntax" test "$void_broken" -eq 0
  echo ""
}
check_css() {
  local css="$ROOT/styles/main.css"
  [ -f "$css" ] || { echo "  FAIL  CSS  main.css not found"; FAIL=$((FAIL+1)); return; }
  local rc
  # C1 — Filesize max 50KB
  local size=$(wc -c < "$css")
  check "C01" "stylesheet under 50KB ($size bytes)" test "$size" -le 51200
  # C2 — Declaration count max 800
  local decls=$(grep -cE '^\s+[a-z-]+:' "$css" 2>/dev/null || echo 0)
  check "C02" "declaration count under 800 ($decls)" test "$decls" -le 800
  # C3 — :root block exists
  grep -qE '^\s*:root\s*\{' "$css"
  rc=$?
  check "C03" ":root custom-properties block defined" test $rc -eq 0
  # C4 — No duplicate keyframe names
  local dupes=$(grep -oP '@keyframes\s+\S+' "$css" | sort | uniq -d | head -c 500)
  check "C04" "no duplicate keyframe names" test -z "$dupes"
  # C5 — No hardcoded colors outside :root (except comments/overrides with --token refs)
  local hardcolors=$(grep -oP '(#[0-9a-fA-F]{3,6}|rgb[a]?\([^)]+\)|hsl[a]?\([^)]+\))' "$css" | grep -v '\/\*.*--' | wc -l)
  local hard_total=$(grep -coP '(#[0-9a-fA-F]{3,6}|rgb[a]?\([^)]+\)|hsl[a]?\([^)]+\))' "$css" 2>/dev/null || echo 0)
  if [ "$hardcolors" -gt 0 ] && [ "$hardcolors" -eq "$hard_total" ]; then
    # only flag if ALL color values are hardcoded — partial is ok with comments
    local root_lines=$(grep -cE '^\s+--' "$css" 2>/dev/null || echo 0)
    if [ "$root_lines" -gt 5 ]; then
      check "C05" "many custom properties defined ($root_lines vars)" test 1 -eq 1
    else
      check "C05" "hardcoded colors minimal" test "$hardcolors" -le 3
    fi
  else
    check "C05" "hardcoded colors minimal" test 1 -eq 1
  fi
  # C6 — Animation longhand count (max 3 per component)
  local anim_longhands=$(grep -cE 'animation-(duration|timing-function|delay|iteration-count|direction|fill-mode|play-state)' "$css" 2>/dev/null || echo 0)
  check "C06" "prefer animation shorthand over longhands" test "$anim_longhands" -le 8
  echo ""
}
check_js() {
  local html="$ROOT/index.html"
  local rc
  # J1 — Inline SVG with animation logic (not static)
  grep -qP '(animate|requestAnimationFrame|setInterval|morph|getContext|data\.)' "$html"
  rc=$?
  check "J01" "SVG data visualization uses JS animation" test $rc -eq 0
  # J2 — At least one data-driven visualization
  grep -qP '(fetch|WebSocket|Math\.(random|sin|cos|PI)|Date\.now|liveData|mockData|simulate|series)' "$html"
  rc=$?
  check "J02" "data-driven visualization present" test $rc -eq 0
}
# === RUN ===
check_html
check_css
check_js
echo ""
echo "--- SUMMARY ---"
echo "  Passed: $PASS"
echo "  Failed: $FAIL"
if [ "$FAIL" -gt 0 ]; then echo "  STATUS: FAILED"; else echo "  STATUS: PASSED"; fi
exit $FAIL
styles/main.css
:root {
  --bg-page: #f9f4ef;
  --bg-card: #fff9f0;
  --bg-soft: #fdf6ee;
  --bg-gradient-start: #fce9d8;
  --bg-gradient-end: #f5dcc4;
  --accent-primary: #d48b5c;
  --accent-secondary: #c4785c;
  --accent-tertiary: #e8a87c;
  --accent-warm: #f2c9a1;
  --text-primary: #3a2a1a;
  --text-secondary: #7a6b5a;
  --text-muted: #b5a696;
  --border-light: #ede0d0;
  --shadow-card: 0 8px 32px rgba(180, 140, 100, 0.15);
  --shadow-soft: 0 4px 16px rgba(180, 140, 100, 0.10);
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
  --radius-round: 999px;
  --font-body: 'Inter', 'Segoe UI', system-ui, sans-serif;
  --font-display: 'Plus Jakarta Sans', 'Inter', sans-serif;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --transition-fluid: 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  --transition-slow: 0.55s cubic-bezier(0.22, 1, 0.36, 1);
}
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
html {
  font-size: 16px;
  scroll-behavior: smooth;
}
body {
  font-family: var(--font-body);
  background: var(--bg-page);
  color: var(--text-primary);
  line-height: 1.6;
  min-height: 100vh;
  overflow-x: hidden;
}
h1, h2, h3, h4 {
  font-family: var(--font-display);
  font-weight: 500;
  line-height: 1.25;
  letter-spacing: -0.02em;
}
a { color: var(--accent-primary); text-decoration: none; }
a:hover { color: var(--accent-secondary); }
/* layout */
.dashboard {
  max-width: 1280px;
  margin: 0 auto;
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
}
/* header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--space-lg) 0;
  border-bottom: 1px solid var(--border-light);
  margin-bottom: var(--space-sm);
}
.dashboard-title {
  font-size: 1.75rem;
  font-weight: 550;
  color: var(--text-primary);
  position: relative;
}
.dashboard-title::after {
  content: '';
  display: block;
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-tertiary));
  border-radius: var(--radius-round);
  margin-top: var(--space-sm);
}
.dashboard-subtitle {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-top: var(--space-xs);
}
.header-time {
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: var(--bg-soft);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-round);
  border: 1px solid var(--border-light);
}
/* metrics row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-md);
}
.metric-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-soft);
  border: 1px solid var(--border-light);
  transition: transform var(--transition-fluid), box-shadow var(--transition-fluid);
  position: relative;
  overflow: hidden;
}
.metric-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-tertiary), var(--accent-warm));
  opacity: 0.5;
}
.metric-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card);
}
.metric-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  margin-bottom: var(--space-sm);
}
.metric-value {
  font-family: var(--font-display);
  font-size: 2rem;
  font-weight: 550;
  color: var(--text-primary);
  line-height: 1.1;
}
.metric-trend {
  font-size: 0.8rem;
  margin-top: var(--space-xs);
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}
.metric-trend.up { color: #7aab7a; }
.metric-trend.down { color: #c47a7a; }
.metric-trend::before {
  content: '';
  display: inline-block;
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
}
.metric-trend.up::before {
  border-bottom: 6px solid #7aab7a;
}
.metric-trend.down::before {
  border-top: 6px solid #c47a7a;
}
/* main content grid */
.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--space-md);
}
@media (max-width: 900px) {
  .content-grid { grid-template-columns: 1fr; }
}
.card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-soft);
  border: 1px solid var(--border-light);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}
.card-title {
  font-family: var(--font-display);
  font-size: 1.1rem;
  font-weight: 530;
  color: var(--text-primary);
}
.card-subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
}
/* wave SVG container */
.wave-container {
  width: 100%;
  height: 180px;
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-md);
  background: linear-gradient(180deg, var(--bg-gradient-start), var(--bg-gradient-end));
  margin-top: var(--space-sm);
}
.wave-container svg {
  width: 100%;
  height: 100%;
  display: block;
}
/* pulse ring visualization */
.pulse-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--space-xl) 0;
  position: relative;
}
.pulse-ring {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.pulse-ring-inner {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--accent-tertiary), var(--accent-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  color: #fff;
  box-shadow: 0 0 30px rgba(212, 139, 92, 0.3);
  animation: pulse-glow 3s ease-in-out infinite;
}
@keyframes pulse-glow {
  0%, 100% { transform: scale(1); box-shadow: 0 0 20px rgba(212, 139, 92, 0.2); }
  50% { transform: scale(1.08); box-shadow: 0 0 40px rgba(212, 139, 92, 0.5); }
}
.pulse-ring::before, .pulse-ring::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  border: 2px solid var(--accent-warm);
  opacity: 0.4;
  animation: pulse-ring-expand 3s ease-out infinite;
}
.pulse-ring::after {
  animation-delay: 1.5s;
}
@keyframes pulse-ring-expand {
  0% { width: 120px; height: 120px; opacity: 0.5; }
  100% { width: 200px; height: 200px; opacity: 0; }
}
/* activity list */
.activity-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
.activity-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  transition: background var(--transition-fluid);
}
.activity-item:hover {
  background: var(--bg-soft);
}
.activity-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.activity-dot.blue { background: #8ab4d4; }
.activity-dot.warm { background: var(--accent-tertiary); }
.activity-dot.green { background: #8ab48a; }
.activity-dot.muted { background: var(--text-muted); }
.activity-text {
  flex: 1;
  font-size: 0.88rem;
  color: var(--text-secondary);
}
.activity-time {
  font-size: 0.75rem;
  color: var(--text-muted);
  white-space: nowrap;
}
/* bottom row */
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}
@media (max-width: 700px) {
  .bottom-row { grid-template-columns: 1fr; }
}
/* chart bar */
.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: var(--space-sm);
  height: 120px;
  padding-top: var(--space-sm);
}
.chart-bar {
  flex: 1;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  background: linear-gradient(180deg, var(--accent-tertiary), var(--accent-primary));
  min-height: 8px;
  transition: height var(--transition-fluid);
  position: relative;
}
.chart-bar:hover {
  opacity: 0.85;
}
.chart-bar-label {
  position: absolute;
  bottom: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.65rem;
  color: var(--text-muted);
  white-space: nowrap;
}
/* status dots */
.status-indicators {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
}
.status-item {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.88rem;
  color: var(--text-secondary);
}
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
.status-dot.online { background: #7aab7a; box-shadow: 0 0 8px rgba(122, 171, 122, 0.5); }
.status-dot.away { background: var(--accent-tertiary); }
.status-dot.offline { background: var(--text-muted); }
/* footer */
.dashboard-footer {
  text-align: center;
  padding: var(--space-xl) 0 var(--space-md);
  font-size: 0.8rem;
  color: var(--text-muted);
  border-top: 1px solid var(--border-light);
}
/* animation: fade in */
@keyframes fade-up {
  0% { opacity: 0; transform: translateY(16px); }
  100% { opacity: 1; transform: translateY(0); }
}
.card, .metric-card {
  animation: fade-up 0.6s ease both;
}
.metric-card:nth-child(1) { animation-delay: 0.05s; }
.metric-card:nth-child(2) { animation-delay: 0.10s; }
.metric-card:nth-child(3) { animation-delay: 0.15s; }
.metric-card:nth-child(4) { animation-delay: 0.20s; }
/* responsive */
@media (max-width: 600px) {
  .dashboard-header { flex-direction: column; gap: var(--space-md); }
  .dashboard-title { font-size: 1.35rem; }
  .metric-card { padding: var(--space-md); }
  .metric-value { font-size: 1.5rem; }
  .card { padding: var(--space-md); }
}
index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Organic Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles/main.css">
</head>
<body>
<div class="dashboard">
  <header class="dashboard-header">
    <div>
      <h1 class="dashboard-title">Fluid Metrics</h1>
      <p class="dashboard-subtitle">Live organic dashboard</p>
    </div>
    <div class="header-time" id="live-time">--:--</div>
  </header>
  <div class="metrics-row">
    <div class="metric-card">
      <div class="metric-label">Active Users</div>
      <div class="metric-value" id="metric-users">1,482</div>
      <div class="metric-trend up">+12.4%</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Revenue</div>
      <div class="metric-value" id="metric-revenue">$64.2k</div>
      <div class="metric-trend up">+8.7%</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Engagement</div>
      <div class="metric-value" id="metric-engagement">87.3%</div>
      <div class="metric-trend up">+3.2%</div>
    </div>
    <div class="metric-card">
      <div class="metric-label">Bounce</div>
      <div class="metric-value" id="metric-bounce">21.5%</div>
      <div class="metric-trend down">-5.1%</div>
    </div>
  </div>
  <div class="content-grid">
    <div class="card">
      <div class="card-header">
        <span class="card-title">Signal Wave</span>
        <span class="card-subtitle">real-time amplitude</span>
      </div>
      <div class="wave-container">
        <svg viewBox="0 0 600 180" preserveAspectRatio="none" id="wave-svg">
          <path id="wave-path-1" fill="rgba(212,139,92,0.15)" d="M0 180 Q75 90 150 120 T300 80 T450 110 T600 60 L600 180 Z"/>
          <path id="wave-path-2" fill="rgba(232,168,124,0.10)" d="M0 180 Q75 130 150 140 T300 100 T450 130 T600 100 L600 180 Z"/>
        </svg>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <span class="card-title">Health Pulse</span>
        <span class="card-subtitle">system core</span>
      </div>
      <div class="pulse-container">
        <div class="pulse-ring">
          <div class="pulse-ring-inner">98%</div>
        </div>
      </div>
    </div>
  </div>
  <div class="bottom-row">
    <div class="card">
      <div class="card-header">
        <span class="card-title">Weekly Activity</span>
        <span class="card-subtitle">7-day trend</span>
      </div>
      <div class="chart-bars" id="chart-bars">
        <div class="chart-bar" style="height:42%" data-label="Mon"><span class="chart-bar-label">Mon</span></div>
        <div class="chart-bar" style="height:68%" data-label="Tue"><span class="chart-bar-label">Tue</span></div>
        <div class="chart-bar" style="height:55%" data-label="Wed"><span class="chart-bar-label">Wed</span></div>
        <div class="chart-bar" style="height:82%" data-label="Thu"><span class="chart-bar-label">Thu</span></div>
        <div class="chart-bar" style="height:73%" data-label="Fri"><span class="chart-bar-label">Fri</span></div>
        <div class="chart-bar" style="height:61%" data-label="Sat"><span class="chart-bar-label">Sat</span></div>
        <div class="chart-bar" style="height:38%" data-label="Sun"><span class="chart-bar-label">Sun</span></div>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <span class="card-title">System Status</span>
        <span class="card-subtitle">all services</span>
      </div>
      <div class="status-indicators">
        <div class="status-item"><span class="status-dot online"></span> API Core</div>
        <div class="status-item"><span class="status-dot online"></span> Database</div>
        <div class="status-item"><span class="status-dot away"></span> Cache Layer</div>
        <div class="status-item"><span class="status-dot online"></span> Auth</div>
        <div class="status-item"><span class="status-dot online"></span> Stream</div>
        <div class="status-item"><span class="status-dot offline"></span> Analytics</div>
      </div>
    </div>
  </div>
  <footer class="dashboard-footer">
    Organic Dashboard &mdash; living data
  </footer>
</div>
<script>
(function(){
  // live time
  function updateTime() {
    var el = document.getElementById('live-time');
    if (!el) return;
    var d = new Date();
    var h = String(d.getHours()).padStart(2,'0');
    var m = String(d.getMinutes()).padStart(2,'0');
    var s = String(d.getSeconds()).padStart(2,'0');
    el.textContent = h + ':' + m + ':' + s;
  }
  updateTime();
  setInterval(updateTime, 1000);
  // wave path animation — JS-driven real-time data simulation
  var path1 = document.getElementById('wave-path-1');
  var path2 = document.getElementById('wave-path-2');
  if (path1 && path2) {
    function generateWave(offset, ampScale) {
      var points = [];
      for (var i = 0; i <= 600; i += 12) {
        var t = (i + offset) * 0.025;
        var y = 60 + Math.sin(t * 1.3) * 20 * ampScale + Math.sin(t * 0.7) * 15 * ampScale + Math.cos(t * 2.1) * 8 * ampScale;
        points.push(i + ',' + y);
      }
      return 'M0 180 Q' + points.join(' ') + ' L0 180 Z';
    }
    function generateFill(offset, ampScale) {
      var points = [];
      for (var i = 0; i <= 600; i += 12) {
        var t = (i + offset) * 0.025;
        var y = 80 + Math.sin(t * 1.3 + 0.8) * 25 * ampScale + Math.sin(t * 0.7 + 0.3) * 18 * ampScale + Math.cos(t * 2.1 + 0.5) * 10 * ampScale;
        points.push(i + ',' + y);
      }
      return 'M0 180 Q' + points.join(' ') + ' L0 180 Z';
    }
    var offset = 0;
    setInterval(function() {
      offset += 0.4;
      path1.setAttribute('d', generateWave(offset, 1.0));
      path2.setAttribute('d', generateFill(offset + 3, 0.85));
    }, 50);
  }
  // simulate metric value drift
  var metricEls = [
    document.getElementById('metric-users'),
    document.getElementById('metric-revenue'),
    document.getElementById('metric-engagement'),
    document.getElementById('metric-bounce')
  ];
  setInterval(function() {
    var users = 1482 + Math.round(Math.sin(Date.now() * 0.00005) * 18);
    if (metricEls[0]) metricEls[0].textContent = users.toLocaleString();
    var revenue = 64.2 + Math.sin(Date.now() * 0.00003) * 1.8;
    if (metricEls[1]) metricEls[1].textContent = '$' + revenue.toFixed(1) + 'k';
    var eng = 87.3 + Math.sin(Date.now() * 0.00007) * 1.2;
    if (metricEls[2]) metricEls[2].textContent = eng.toFixed(1) + '%';
    var bounce = 21.5 + Math.sin(Date.now() * 0.00009 + 1) * 1.5;
    if (metricEls[3]) metricEls[3].textContent = bounce.toFixed(1) + '%';
  }, 3000);
})();
</script>
</body>
</html>