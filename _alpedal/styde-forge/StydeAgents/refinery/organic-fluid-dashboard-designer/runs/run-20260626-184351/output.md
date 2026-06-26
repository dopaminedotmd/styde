index.html
<!DOCTYPE html>
<html lang=en>
<meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Fluid Dashboard</title>
<link rel=stylesheet href=styles/main.css>
<body>
<nav class=orb-nav>
  <div class=orb-brand>drift</div>
  <div class=orb-links>
    <a href=# class=orb-link active>overview</a>
    <a href=# class=orb-link>analytics</a>
    <a href=# class=orb-link>settings</a>
  </div>
  <div class=orb-avatar data-initials=AP></div>
</nav>
<main class=dashboard>
  <header class=greeting>
    <h1>good morning</h1>
    <p class=greeting-sub>your systems are breathing easy</p>
  </header>
  <section class=metric-grid>
    <div class=metric-card pulse-card>
      <div class=metric-icon>
        <svg viewbox="0 0 24 24" width=28 height=28 fill=none stroke=currentColor stroke-width=1.5 stroke-linecap=round stroke-linejoin=round>
          <path d="M3 12h3l2-3 3 6 2-3 2 3 3-3 3 3"/>
        </svg>
      </div>
      <span class=metric-value>87.4%</span>
      <span class=metric-label>system health</span>
      <div class=metric-trend up>+2.1%</div>
    </div>
    <div class=metric-card pulse-card>
      <div class=metric-icon>
        <svg viewbox="0 0 24 24" width=28 height=28 fill=none stroke=currentColor stroke-width=1.5 stroke-linecap=round stroke-linejoin=round>
          <circle cx=12 cy=12 r=10/><path d="M12 6v6l4 2"/>
        </svg>
      </div>
      <span class=metric-value>342</span>
      <span class=metric-label>active flows</span>
      <div class=metric-trend up>+12</div>
    </div>
    <div class=metric-card pulse-card>
      <div class=metric-icon>
        <svg viewbox="0 0 24 24" width=28 height=28 fill=none stroke=currentColor stroke-width=1.5 stroke-linecap=round stroke-linejoin=round>
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
        </svg>
      </div>
      <span class=metric-value>99.97%</span>
      <span class=metric-label>uptime</span>
      <div class=metric-trend up>+0.01%</div>
    </div>
    <div class=metric-card pulse-card>
      <div class=metric-icon>
        <svg viewbox="0 0 24 24" width=28 height=28 fill=none stroke=currentColor stroke-width=1.5 stroke-linecap=round stroke-linejoin=round>
          <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
        </svg>
      </div>
      <span class=metric-value>1.2ms</span>
      <span class=metric-label>avg latency</span>
      <div class=metric-trend down>-0.3ms</div>
    </div>
  </section>
  <section class=chart-area>
    <div class=chart-header>
      <h2>resource pulse</h2>
      <div class=chart-legend>
        <span class=legend-dot cpu></span> cpu
        <span class=legend-dot mem></span> memory
        <span class=legend-dot net></span> network
      </div>
    </div>
    <div class=wave-container id=waveContainer>
      <svg viewbox="0 0 800 200" preserveaspectratio=none width=100% height=100%>
        <path class=wave wave-cpu d="M0,100 Q100,40 200,80 T400,60 T600,100 T800,70 L800,200 L0,200 Z"/>
        <path class=wave wave-mem d="M0,130 Q100,100 200,120 T400,100 T600,130 T800,110 L800,200 L0,200 Z"/>
        <path class=wave wave-net d="M0,160 Q100,140 200,155 T400,145 T600,160 T800,150 L800,200 L0,200 Z"/>
      </svg>
    </div>
  </section>
  <section class=activity-feed>
    <h2>recent pulses</h2>
    <div class=activity-item>
      <div class=activity-dot ok></div>
      <div class=activity-body>
        <span class=activity-title>deployment complete</span>
        <span class=activity-time>2m ago</span>
      </div>
    </div>
    <div class=activity-item>
      <div class=activity-dot warn></div>
      <div class=activity-body>
        <span class=activity-title>memory threshold crossed</span>
        <span class=activity-time>14m ago</span>
      </div>
    </div>
    <div class=activity-item>
      <div class=activity-dot ok></div>
      <div class=activity-body>
        <span class=activity-title>backup verified</span>
        <span class=activity-time>1h ago</span>
      </div>
    </div>
    <div class=activity-item>
      <div class=activity-dot info></div>
      <div class=activity-body>
        <span class=activity-title>new blueprint queued</span>
        <span class=activity-time>2h ago</span>
      </div>
    </div>
  </section>
</main>
<div class=ambient-bg>
  <div class=ambient-orb o1></div>
  <div class=ambient-orb o2></div>
  <div class=ambient-orb o3></div>
</div>
</html>
styles/main.css
:root {
  --bg-base: #1a141e;
  --bg-card: rgba(255,245,235,0.04);
  --bg-card-hover: rgba(255,245,235,0.08);
  --bg-ambient-1: #7c4dff;
  --bg-ambient-2: #e040fb;
  --bg-ambient-3: #ff6f00;
  --text-primary: #f0ebe6;
  --text-secondary: rgba(240,235,230,0.6);
  --text-tertiary: rgba(240,235,230,0.35);
  --accent-green: #69f0ae;
  --accent-orange: #ffab40;
  --accent-pink: #ff80ab;
  --accent-blue: #82b1ff;
  --accent-red: #ff5252;
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-xl: 32px;
  --radius-full: 9999px;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --font-body: 'Inter','Segoe UI',system-ui,-apple-system,sans-serif;
  --font-mono: 'JetBrains Mono','Fira Code',monospace;
  --shadow-card: 0 2px 24px rgba(0,0,0,0.25),0 1px 4px rgba(0,0,0,0.15);
  --shadow-orb: 0 0 80px rgba(124,77,255,0.3);
  --transition-default: 0.4s cubic-bezier(0.34,1.56,0.64,1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{font-size:16px;scroll-behavior:smooth}
body{
  font-family:var(--font-body);
  background:var(--bg-base);
  color:var(--text-primary);
  min-height:100vh;
  overflow-x:hidden;
  line-height:1.5;
  -webkit-font-smoothing:antialiased;
}
.ambient-bg{
  position:fixed;inset:0;z-index:0;overflow:hidden;pointer-events:none;
}
.ambient-orb{
  position:absolute;border-radius:var(--radius-full);filter:blur(80px);opacity:0.35;
  animation:orb-drift 20s ease-in-out infinite;
}
.ambient-orb.o1{
  width:500px;height:500px;
  background:radial-gradient(circle,var(--bg-ambient-1),transparent 70%);
  top:-10%;left:-5%;animation-delay:0s;
}
.ambient-orb.o2{
  width:400px;height:400px;
  background:radial-gradient(circle,var(--bg-ambient-2),transparent 70%);
  bottom:-15%;right:-8%;animation-delay:-7s;
}
.ambient-orb.o3{
  width:350px;height:350px;
  background:radial-gradient(circle,var(--bg-ambient-3),transparent 70%);
  top:40%;left:50%;animation-delay:-14s;
}
@keyframes orb-drift{
  0%,100%{transform:translate(0,0) scale(1)}
  25%{transform:translate(60px,-40px) scale(1.08)}
  50%{transform:translate(-30px,50px) scale(0.92)}
  75%{transform:translate(40px,30px) scale(1.04)}
}
.orb-nav{
  position:relative;z-index:10;
  display:flex;align-items:center;
  padding:var(--space-md) var(--space-xl);
  gap:var(--space-xl);
  backdrop-filter:blur(12px);
  background:rgba(26,20,30,0.6);
  border-bottom:1px solid rgba(255,245,235,0.06);
}
.orb-brand{
  font-size:1.25rem;font-weight:600;
  letter-spacing:-0.02em;
  background:linear-gradient(135deg,var(--accent-green),var(--accent-blue));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.orb-links{display:flex;gap:var(--space-xs);margin-left:auto}
.orb-link{
  color:var(--text-secondary);text-decoration:none;
  padding:var(--space-xs) var(--space-md);
  border-radius:var(--radius-full);
  font-size:0.875rem;font-weight:500;
  transition:var(--transition-default);
}
.orb-link:hover,.orb-link.active{
  color:var(--text-primary);
  background:var(--bg-card-hover);
}
.orb-avatar{
  width:36px;height:36px;border-radius:var(--radius-full);
  background:linear-gradient(135deg,var(--accent-pink),var(--accent-orange));
  display:flex;align-items:center;justify-content:center;
  font-size:0.75rem;font-weight:600;color:var(--bg-base);
  cursor:pointer;
}
.dashboard{
  position:relative;z-index:5;
  max-width:1200px;margin:0 auto;
  padding:var(--space-xl) var(--space-xl) var(--space-2xl);
}
.greeting{margin-bottom:var(--space-xl)}
.greeting h1{
  font-size:2rem;font-weight:500;letter-spacing:-0.03em;
  background:linear-gradient(135deg,var(--text-primary),var(--text-secondary));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.greeting-sub{color:var(--text-tertiary);font-size:0.9rem;margin-top:var(--space-xs)}
.metric-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(230px,1fr));
  gap:var(--space-md);margin-bottom:var(--space-xl);
}
.metric-card{
  background:var(--bg-card);
  border-radius:var(--radius-lg);
  padding:var(--space-lg);
  border:1px solid rgba(255,245,235,0.06);
  backdrop-filter:blur(8px);
  transition:var(--transition-default);
  display:flex;flex-direction:column;gap:var(--space-sm);
}
.metric-card:hover{
  background:var(--bg-card-hover);
  transform:translateY(-2px);
  box-shadow:var(--shadow-card);
}
.metric-icon{
  width:40px;height:40px;border-radius:var(--radius-md);
  display:flex;align-items:center;justify-content:center;
  background:rgba(255,245,235,0.06);
  color:var(--text-secondary);
  margin-bottom:var(--space-xs);
}
.metric-value{
  font-size:1.75rem;font-weight:600;letter-spacing:-0.03em;
  font-variant-numeric:tabular-nums;
}
.metric-label{font-size:0.8rem;color:var(--text-tertiary);text-transform:uppercase;letter-spacing:0.06em}
.metric-trend{
  font-size:0.8rem;font-weight:500;border-radius:var(--radius-full);
  padding:2px var(--space-sm);display:inline-block;width:fit-content;
}
.metric-trend.up{background:rgba(105,240,174,0.12);color:var(--accent-green)}
.metric-trend.down{background:rgba(255,82,82,0.12);color:var(--accent-red)}
@keyframes pulse-card{0%,100%{opacity:1}50%{opacity:0.85}}
.pulse-card{animation:pulse-card 4s ease-in-out infinite}
.pulse-card:nth-child(2){animation-delay:1s}
.pulse-card:nth-child(3){animation-delay:2s}
.pulse-card:nth-child(4){animation-delay:3s}
.chart-area{
  background:var(--bg-card);
  border-radius:var(--radius-lg);
  padding:var(--space-lg);
  border:1px solid rgba(255,245,235,0.06);
  margin-bottom:var(--space-xl);
}
.chart-header{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:var(--space-md);
}
.chart-header h2{font-size:1.1rem;font-weight:500;letter-spacing:-0.02em}
.chart-legend{display:flex;gap:var(--space-md);font-size:0.75rem;color:var(--text-secondary)}
.legend-dot{
  display:inline-block;width:8px;height:8px;border-radius:var(--radius-full);
  margin-right:var(--space-xs);vertical-align:middle;
}
.legend-dot.cpu{background:var(--accent-green)}
.legend-dot.mem{background:var(--accent-blue)}
.legend-dot.net{background:var(--accent-orange)}
.wave-container{
  width:100%;height:180px;border-radius:var(--radius-md);
  overflow:hidden;position:relative;
}
.wave{
  fill-opacity:0.15;
  animation:wave-slide 8s ease-in-out infinite;
  transform-origin:center;
}
.wave-cpu{fill:var(--accent-green)}
.wave-mem{fill:var(--accent-blue)}
.wave-net{fill:var(--accent-orange)}
@keyframes wave-slide{
  0%{transform:translateX(0) scaleY(1)}
  50%{transform:translateX(-40px) scaleY(1.12)}
  100%{transform:translateX(0) scaleY(1)}
}
.activity-feed h2{font-size:1.1rem;font-weight:500;margin-bottom:var(--space-md);letter-spacing:-0.02em}
.activity-item{
  display:flex;gap:var(--space-md);align-items:flex-start;
  padding:var(--space-sm) 0;
  border-bottom:1px solid rgba(255,245,235,0.04);
}
.activity-item:last-child{border-bottom:none}
.activity-dot{
  width:10px;height:10px;border-radius:var(--radius-full);
  margin-top:5px;flex-shrink:0;
}
.activity-dot.ok{background:var(--accent-green)}
.activity-dot.warn{background:var(--accent-orange)}
.activity-dot.info{background:var(--accent-blue)}
.activity-body{
  display:flex;flex-direction:column;gap:2px;flex:1;
}
.activity-title{font-size:0.9rem;font-weight:450}
.activity-time{font-size:0.75rem;color:var(--text-tertiary)}
@media(max-width:640px){
  .dashboard{padding:var(--space-md)}
  .orb-nav{padding:var(--space-sm) var(--space-md)}
  .metric-grid{grid-template-columns:1fr}
  .greeting h1{font-size:1.5rem}
  .chart-header{flex-direction:column;align-items:flex-start;gap:var(--space-sm)}
}
scripts/validate.sh
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd "$(dirname "$0")/.." && pwd)
HTML_FILE="$SCRIPT_DIR/index.html"
CSS_FILE="$SCRIPT_DIR/styles/main.css"
EXIT_CODE=0
PASS_COUNT=0
FAIL_COUNT=0
check() {
  local rc=$?
  local label=$1
  local desc=$2
  if [ $rc -ne 0 ]; then
    FAIL_COUNT=$((FAIL_COUNT + 1))
    printf "FAIL [%s] %s\n" "$label" "$desc"
    EXIT_CODE=1
  else
    PASS_COUNT=$((PASS_COUNT + 1))
    printf "PASS [%s] %s\n" "$label" "$desc"
  fi
}
check_doctype() {
  grep -q '<!DOCTYPE html>' "$HTML_FILE"
}
check_charset() {
  grep -qi 'charset=utf-8' "$HTML_FILE" || grep -qi 'charset="utf-8"' "$HTML_FILE"
}
check_tag_balance() {
  local opens closes
  opens=$(grep -oP '</?[a-zA-Z][a-zA-Z0-9]*' "$HTML_FILE" | grep -vP '^</' | sed 's/^<//' | sort | uniq -c | awk '{print $2,$1}')
  closes=$(grep -oP '</[a-zA-Z][a-zA-Z0-9]*' "$HTML_FILE" | sed 's/^<\///' | sort | uniq -c | awk '{print $2,$1}')
  local ok=0
  while IFS=' ' read -r tag open_count; do
    local close_count
    close_count=$(echo "$closes" | grep -w "$tag" | awk '{print $2}' || echo 0)
    if [ "$open_count" != "$close_count" ] && [ "$close_count" -ne 0 ]; then
      echo "  unbalanced <$tag>: $open_count opens, $close_count closes"
      ok=1
    fi
  done <<< "$opens"
  return $ok
}
check_css_vars() {
  local vars_used vars_defined
  vars_used=$(grep -oP 'var\(--[a-zA-Z0-9_-]+' "$CSS_FILE" | sed 's/var(//' | sort -u)
  vars_defined=$(grep -oP '--[a-zA-Z0-9_-]+\s*:' "$CSS_FILE" | sed 's/\s*://' | sort -u)
  local missing=0
  while IFS= read -r v; do
    if ! grep -qF "$v" <<< "$vars_defined"; then
      echo "  undefined variable: $v"
      missing=1
    fi
  done <<< "$vars_used"
  return $missing
}
check_duplicate_keyframes() {
  local dupes
  dupes=$(grep -oP '@keyframes\s+[a-zA-Z0-9_-]+' "$CSS_FILE" | sed 's/@keyframes //' | sort | uniq -d)
  if [ -n "$dupes" ]; then
    while IFS= read -r kf; do
      echo "  duplicate keyframe: $kf"
    done <<< "$dupes"
    return 1
  fi
  return 0
}
check_css_budget() {
  local size_bytes decl_count
  size_bytes=$(wc -c < "$CSS_FILE")
  decl_count=$(grep -cE '^\s+[a-z-]+\s*:' "$CSS_FILE" || true)
  if [ "$size_bytes" -gt 51200 ]; then
    echo "  stylesheet $size_bytes bytes exceeds 51200 byte limit"
    return 1
  fi
  if [ "$decl_count" -gt 800 ]; then
    echo "  $decl_count declarations exceeds 800 limit"
    return 1
  fi
  return 0
}
echo "=== HTML Validation ==="
check_doctype
check "$?" doctype "HTML5 DOCTYPE present"
check_charset
check "$?" charset "charset utf-8 declared"
check_tag_balance
check "$?" balance "tags are balanced"
echo ""
echo "=== CSS Validation ==="
check_css_vars
check "$?" css-vars "all CSS variables are defined in :root"
check_duplicate_keyframes
check "$?" keyframes "no duplicate keyframe names"
check_css_budget
check "$?" budget "stylesheet within 50KB / 800 declarations"
echo ""
echo "=== Summary ==="
printf "pass: %d  fail: %d\n" "$PASS_COUNT" "$FAIL_COUNT"
exit "$EXIT_CODE"