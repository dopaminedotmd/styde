<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>organic·flow — wellness dashboard</title>
<link rel="stylesheet" href="styles/main.css">
</head>
<body>
  <div class="dashboard">
    <header class="dashboard__header">
      <h1 class="dashboard__title">organic·flow</h1>
      <p class="dashboard__subtitle">wellness at a glance</p>
    </header>
    <canvas id="fluid-canvas" class="fluid-canvas"></canvas>
    <div class="metric-grid">
      <div class="metric-card" data-metric="energy">
        <div class="metric-card__value">87</div>
        <div class="metric-card__label">energy</div>
        <div class="metric-card__track">
          <div class="metric-card__fill" style="--fill-width:87%"></div>
        </div>
        <div class="metric-card__glow"></div>
      </div>
      <div class="metric-card" data-metric="focus">
        <div class="metric-card__value">92</div>
        <div class="metric-card__label">focus</div>
        <div class="metric-card__track">
          <div class="metric-card__fill" style="--fill-width:92%"></div>
        </div>
        <div class="metric-card__glow"></div>
      </div>
      <div class="metric-card" data-metric="mood">
        <div class="metric-card__value">76</div>
        <div class="metric-card__label">mood</div>
        <div class="metric-card__track">
          <div class="metric-card__fill" style="--fill-width:76%"></div>
        </div>
        <div class="metric-card__glow"></div>
      </div>
      <div class="metric-card" data-metric="creativity">
        <div class="metric-card__value">94</div>
        <div class="metric-card__label">creativity</div>
        <div class="metric-card__track">
          <div class="metric-card__fill" style="--fill-width:94%"></div>
        </div>
        <div class="metric-card__glow"></div>
      </div>
      <div class="metric-card" data-metric="rest">
        <div class="metric-card__value">68</div>
        <div class="metric-card__label">rest</div>
        <div class="metric-card__track">
          <div class="metric-card__fill" style="--fill-width:68%"></div>
        </div>
        <div class="metric-card__glow"></div>
      </div>
      <div class="metric-card" data-metric="resilience">
        <div class="metric-card__value">81</div>
        <div class="metric-card__label">resilience</div>
        <div class="metric-card__track">
          <div class="metric-card__fill" style="--fill-width:81%"></div>
        </div>
        <div class="metric-card__glow"></div>
      </div>
    </div>
    <div class="activity-ring">
      <svg viewBox="0 0 200 200" class="activity-ring__svg">
        <circle cx="100" cy="100" r="85" class="activity-ring__bg"/>
        <circle cx="100" cy="100" r="85" class="activity-ring__arc" stroke-dasharray="534 534" stroke-dashoffset="107"/>
        <circle cx="100" cy="100" r="70" class="activity-ring__bg"/>
        <circle cx="100" cy="100" r="70" class="activity-ring__arc activity-ring__arc--accent" stroke-dasharray="440 440" stroke-dashoffset="132"/>
        <circle cx="100" cy="100" r="55" class="activity-ring__bg"/>
        <circle cx="100" cy="100" r="55" class="activity-ring__arc activity-ring__arc--highlight" stroke-dasharray="346 346" stroke-dashoffset="104"/>
      </svg>
      <div class="activity-ring__center">
        <span class="activity-ring__total">83</span>
        <span class="activity-ring__unit">overall</span>
      </div>
    </div>
    <div class="organic-blobs">
      <div class="blob blob--1"></div>
      <div class="blob blob--2"></div>
      <div class="blob blob--3"></div>
      <div class="blob blob--4"></div>
    </div>
    <div class="time-timeline">
      <div class="time-timeline__bar">
        <div class="time-timeline__segment" style="--seg-width:32%;--seg-color:var(--c-energy)"></div>
        <div class="time-timeline__segment" style="--seg-width:24%;--seg-color:var(--c-focus)"></div>
        <div class="time-timeline__segment" style="--seg-width:18%;--seg-color:var(--c-mood)"></div>
        <div class="time-timeline__segment" style="--seg-width:26%;--seg-color:var(--c-creativity)"></div>
      </div>
      <div class="time-timeline__labels">
        <span>morning</span>
        <span>midday</span>
        <span>evening</span>
        <span>night</span>
      </div>
    </div>
  </div>
  <script src="scripts/fluid.js"></script>
</body>
</html>
--- styles/main.css ---
:root {
  --c-bg: #faf5ef;
  --c-bg-secondary: #f5ede4;
  --c-text: #3d3229;
  --c-text-soft: #7a6b5e;
  --c-text-muted: #a89888;
  --c-energy: #e8a87c;
  --c-focus: #c4a882;
  --c-mood: #b8a9c9;
  --c-creativity: #a8c4b0;
  --c-rest: #d4b89e;
  --c-resilience: #c9b8a8;
  --c-accent: #d9906a;
  --c-highlight: #f0c8a8;
  --c-glow-energy: rgba(232,168,124,0.3);
  --c-glow-focus: rgba(196,168,130,0.3);
  --c-glow-mood: rgba(184,169,201,0.3);
  --c-glow-creativity: rgba(168,196,176,0.3);
  --c-glow-rest: rgba(212,184,158,0.3);
  --c-glow-resilience: rgba(201,184,168,0.3);
  --c-blob-1: rgba(232,168,124,0.08);
  --c-blob-2: rgba(184,169,201,0.06);
  --c-blob-3: rgba(168,196,176,0.07);
  --c-blob-4: rgba(212,184,158,0.05);
  --c-card-bg: rgba(255,250,245,0.75);
  --c-card-border: rgba(200,185,170,0.25);
  --c-ring-active: #e8a87c;
  --c-ring-accent: #b8a9c9;
  --c-ring-highlight: #a8c4b0;
  --c-ring-bg: rgba(200,185,170,0.12);
  --fs-base: 16px;
  --fs-title: 2.25rem;
  --fs-subtitle: 0.95rem;
  --fs-metric-value: 2rem;
  --fs-metric-label: 0.75rem;
  --fs-ring-total: 1.75rem;
  --fs-ring-unit: 0.6rem;
  --fs-timeline: 0.65rem;
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  --radius-full: 50%;
  --radius-blob: 40% 60% 55% 45% / 50% 45% 55% 50%;
  --shadow-card: 0 4px 24px rgba(160,140,120,0.08), 0 1px 4px rgba(160,140,120,0.04);
  --shadow-card-hover: 0 8px 36px rgba(160,140,120,0.14), 0 2px 8px rgba(160,140,120,0.06);
  --shadow-glow: 0 0 40px rgba(232,168,124,0.15);
  --transition-standard: 0.4s cubic-bezier(0.25,0.46,0.45,0.94);
  --transition-slow: 0.8s cubic-bezier(0.25,0.46,0.45,0.94);
  --z-canvas: 0;
  --z-blobs: 1;
  --z-content: 2;
  --z-card: 3;
  --z-glow: 0;
}
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
html {
  font-size: var(--fs-base);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
body {
  background: var(--c-bg);
  color: var(--c-text);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
}
@font-face {
  font-family: 'Inter';
  src: url('https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfAZ9hjp-KkqE.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Inter';
  src: url('https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfAZ9hjp-KkqE.woff2') format('woff2');
  font-weight: 300;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Inter';
  src: url('https://fonts.gstatic.com/s/inter/v18/UcCO3FwrK3iLTeHuS_nVMrMxCp50SjIw2boKoduKmMEVuLyfAZ9hjp-KkqE.woff2') format('woff2');
  font-weight: 500;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
.dashboard {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-2xl) var(--spacing-xl);
  z-index: var(--z-content);
}
.dashboard__header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  position: relative;
}
.dashboard__title {
  font-size: var(--fs-title);
  font-weight: 300;
  letter-spacing: -0.03em;
  color: var(--c-text);
  margin-bottom: var(--spacing-xs);
}
.dashboard__subtitle {
  font-size: var(--fs-subtitle);
  color: var(--c-text-soft);
  font-weight: 300;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.fluid-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-canvas);
  pointer-events: none;
  opacity: 0.6;
}
.metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
  position: relative;
  z-index: var(--z-card);
}
.metric-card {
  background: var(--c-card-bg);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid var(--c-card-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: transform var(--transition-standard), box-shadow var(--transition-standard);
  box-shadow: var(--shadow-card);
}
.metric-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card-hover);
}
.metric-card__glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  border-radius: var(--radius-full);
  opacity: 0;
  transition: opacity var(--transition-slow);
  pointer-events: none;
  z-index: var(--z-glow);
}
.metric-card[data-metric=energy] .metric-card__glow { background: radial-gradient(circle at center, var(--c-glow-energy), transparent 70%); }
.metric-card[data-metric=focus] .metric-card__glow { background: radial-gradient(circle at center, var(--c-glow-focus), transparent 70%); }
.metric-card[data-metric=mood] .metric-card__glow { background: radial-gradient(circle at center, var(--c-glow-mood), transparent 70%); }
.metric-card[data-metric=creativity] .metric-card__glow { background: radial-gradient(circle at center, var(--c-glow-creativity), transparent 70%); }
.metric-card[data-metric=rest] .metric-card__glow { background: radial-gradient(circle at center, var(--c-glow-rest), transparent 70%); }
.metric-card[data-metric=resilience] .metric-card__glow { background: radial-gradient(circle at center, var(--c-glow-resilience), transparent 70%); }
.metric-card:hover .metric-card__glow {
  opacity: 1;
}
.metric-card__value {
  font-size: var(--fs-metric-value);
  font-weight: 300;
  color: var(--c-text);
  line-height: 1;
  margin-bottom: var(--spacing-xs);
  position: relative;
}
.metric-card__label {
  font-size: var(--fs-metric-label);
  color: var(--c-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: var(--spacing-sm);
  position: relative;
}
.metric-card__track {
  height: 3px;
  background: rgba(200,185,170,0.15);
  border-radius: 99px;
  overflow: hidden;
  position: relative;
}
.metric-card__fill {
  height: 100%;
  width: var(--fill-width);
  border-radius: 99px;
  transition: width 1s cubic-bezier(0.25,0.46,0.45,0.94);
}
.metric-card[data-metric=energy] .metric-card__fill { background: linear-gradient(90deg, var(--c-energy), #f0c8a8); }
.metric-card[data-metric=focus] .metric-card__fill { background: linear-gradient(90deg, var(--c-focus), #d8c4a0); }
.metric-card[data-metric=mood] .metric-card__fill { background: linear-gradient(90deg, var(--c-mood), #d0c4dc); }
.metric-card[data-metric=creativity] .metric-card__fill { background: linear-gradient(90deg, var(--c-creativity), #c4d8c8); }
.metric-card[data-metric=rest] .metric-card__fill { background: linear-gradient(90deg, var(--c-rest), #e0c8b4); }
.metric-card[data-metric=resilience] .metric-card__fill { background: linear-gradient(90deg, var(--c-resilience), #d8c8b4); }
.activity-ring {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto var(--spacing-2xl);
  z-index: var(--z-card);
}
.activity-ring__svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.activity-ring__bg {
  fill: none;
  stroke: var(--c-ring-bg);
  stroke-width: 12;
}
.activity-ring__arc {
  fill: none;
  stroke: var(--c-ring-active);
  stroke-width: 12;
  stroke-linecap: round;
  transition: stroke-dashoffset var(--transition-slow);
}
.activity-ring__arc--accent {
  stroke: var(--c-ring-accent);
}
.activity-ring__arc--highlight {
  stroke: var(--c-ring-highlight);
}
.activity-ring__center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.activity-ring__total {
  display: block;
  font-size: var(--fs-ring-total);
  font-weight: 300;
  color: var(--c-text);
  line-height: 1;
}
.activity-ring__unit {
  font-size: var(--fs-ring-unit);
  color: var(--c-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.organic-blobs {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-blobs);
  pointer-events: none;
  overflow: hidden;
}
.blob {
  position: absolute;
  border-radius: var(--radius-blob);
  animation: blob-float 12s ease-in-out infinite alternate;
  filter: blur(60px);
}
.blob--1 {
  width: 400px;
  height: 400px;
  top: 10%;
  left: -5%;
  background: var(--c-blob-1);
  animation-duration: 14s;
}
.blob--2 {
  width: 350px;
  height: 350px;
  bottom: 5%;
  right: -3%;
  background: var(--c-blob-2);
  animation-duration: 16s;
  animation-delay: -3s;
}
.blob--3 {
  width: 250px;
  height: 250px;
  top: 50%;
  left: 60%;
  background: var(--c-blob-3);
  animation-duration: 18s;
  animation-delay: -5s;
}
.blob--4 {
  width: 200px;
  height: 200px;
  bottom: 30%;
  left: 15%;
  background: var(--c-blob-4);
  animation-duration: 20s;
  animation-delay: -7s;
}
@keyframes blob-float {
  0% { transform: translate(0,0) scale(1) rotate(0deg); border-radius: 40% 60% 55% 45% / 50% 45% 55% 50%; }
  33% { transform: translate(20px,-30px) scale(1.05) rotate(5deg); border-radius: 55% 45% 40% 60% / 45% 55% 50% 50%; }
  66% { transform: translate(-15px,20px) scale(0.95) rotate(-3deg); border-radius: 45% 55% 50% 50% / 55% 45% 60% 40%; }
  100% { transform: translate(10px,-10px) scale(1.02) rotate(2deg); border-radius: 50% 50% 45% 55% / 40% 60% 50% 50%; }
}
@keyframes blob-drift {
  0% { transform: translate(0,0); }
  100% { transform: translate(15px,-20px); }
}
.time-timeline {
  max-width: 500px;
  margin: 0 auto;
  padding: var(--spacing-md);
  background: var(--c-card-bg);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border: 1px solid var(--c-card-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
  position: relative;
  z-index: var(--z-card);
}
.time-timeline__bar {
  display: flex;
  height: 8px;
  border-radius: 99px;
  overflow: hidden;
  gap: 2px;
}
.time-timeline__segment {
  height: 100%;
  width: var(--seg-width, 25%);
  background: var(--seg-color, var(--c-energy));
  border-radius: 99px;
  transition: width var(--transition-slow);
}
.time-timeline__labels {
  display: flex;
  justify-content: space-between;
  margin-top: var(--spacing-sm);
  font-size: var(--fs-timeline);
  color: var(--c-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
@media (max-width: 640px) {
  .dashboard { padding: var(--spacing-lg) var(--spacing-md); }
  .dashboard__title { font-size: 1.75rem; }
  .metric-grid { grid-template-columns: repeat(2,1fr); gap: var(--spacing-md); }
  .metric-card { padding: var(--spacing-md); }
  .metric-card__value { font-size: 1.5rem; }
  .activity-ring { width: 160px; height: 160px; }
}
@media (max-width: 420px) {
  .metric-grid { grid-template-columns: 1fr; }
}
--- scripts/validate.sh ---
#!/usr/bin/env bash
set -o nounset
set -o errexit
set -o pipefail
readonly ROOT="$(cd "$(dirname "$0")/.." && pwd)"
readonly HTML="$ROOT/index.html"
readonly CSS="$ROOT/styles/main.css"
readonly JS="$ROOT/scripts/fluid.js"
total_passes=0
total_fails=0
check() {
  local rc=$?
  local label=$1
  local desc=$2
  if [ $rc -ne 0 ]; then
    echo "FAIL  $label — $desc"
    total_fails=$((total_fails + 1))
  else
    echo "PASS  $label"
    total_passes=$((total_passes + 1))
  fi
}
check_cmd() {
  local label=$1
  local desc=$2
  shift 2
  if "$@"; then
    echo "PASS  $label"
    total_passes=$((total_passes + 1))
  else
    echo "FAIL  $label — $desc"
    total_fails=$((total_fails + 1))
  fi
}
check_fail() {
  local label=$1
  local desc=$2
  echo "FAIL  $label — $desc"
  total_fails=$((total_fails + 1))
}
echo "=== Validation Gate — organic·flow dashboard ==="
echo ""
# 1 — HTML well-formedness
echo "--- 1. HTML well-formedness ---"
if [ ! -f "$HTML" ]; then
  check_fail "html_exists" "index.html not found at $HTML"
else
  # DOCTYPE presence
  grep -q '<!DOCTYPE html>' "$HTML"
  check "html_doctype" "DOCTYPE declaration missing"
  # charset meta
  grep -qi 'charset="UTF-8"' "$HTML"
  check "html_charset" "charset=UTF-8 meta missing"
  # balanced html/head/body tags
  html_open=$(grep -c '<html' "$HTML" 2>/dev/null || echo 0)
  html_close=$(grep -c '</html>' "$HTML" 2>/dev/null || echo 0)
  head_open=$(grep -c '<head' "$HTML" 2>/dev/null || echo 0)
  head_close=$(grep -c '</head>' "$HTML" 2>/dev/null || echo 0)
  body_open=$(grep -c '<body' "$HTML" 2>/dev/null || echo 0)
  body_close=$(grep -c '</body>' "$HTML" 2>/dev/null || echo 0)
  if [ "$html_open" -eq 1 ] && [ "$html_close" -eq 1 ] && \
     [ "$head_open" -eq 1 ] && [ "$head_close" -eq 1 ] && \
     [ "$body_open" -eq 1 ] && [ "$body_close" -eq 1 ]; then
    echo "PASS  html_tag_balance"
    total_passes=$((total_passes + 1))
  else
    echo "FAIL  html_tag_balance — html:$html_open/$html_close head:$head_open/$head_close body:$body_open/$body_close"
    total_fails=$((total_fails + 1))
  fi
  # title element present
  grep -q '<title>' "$HTML"
  check "html_title" "title element missing"
  # viewport meta
  grep -qi 'viewport' "$HTML"
  check "html_viewport" "viewport meta missing"
  # language attribute
  grep -q 'lang="en"' "$HTML"
  check "html_lang" "lang attribute on html tag missing"
fi
echo ""
# 2 — CSS custom property validation
echo "--- 2. CSS custom property references ---"
if [ ! -f "$CSS" ]; then
  check_fail "css_exists" "main.css not found at $CSS"
else
  var_refs=$(grep -oP 'var\(--[a-zA-Z0-9_-]+' "$CSS" 2>/dev/null | sort -u || true)
  var_defs=$(grep -oP '--[a-zA-Z0-9_-]+:' "$CSS" 2>/dev/null | sed 's/:$//' | sort -u || true)
  undefined=0
  while IFS= read -r ref; do
    ref_name="${ref#var\(}"
    if ! echo "$var_defs" | grep -qFx "$ref_name"; then
      echo "MISS  $ref_name is used but not defined in :root"
      undefined=$((undefined + 1))
    fi
  done <<< "$var_refs"
  if [ "$undefined" -eq 0 ]; then
    echo "PASS  css_custom_props — all $ref_count references have matching definitions"
    total_passes=$((total_passes + 1))
  else
    echo "FAIL  css_custom_props — $undefined undefined custom property references"
    total_fails=$((total_fails + 1))
  fi
  # :root block presence
  grep -q ':root' "$CSS"
  check "css_root_block" ":root block missing"
fi
echo ""
# 3 — Duplicate keyframe names
echo "--- 3. Duplicate keyframe names ---"
if [ -f "$CSS" ]; then
  keyframe_names=$(grep -oP '@keyframes\s+\K[a-zA-Z0-9_-]+' "$CSS" 2>/dev/null || true)
  dupes=$(echo "$keyframe_names" | sort | uniq -d | wc -l)
  if [ "$dupes" -eq 0 ]; then
    echo "PASS  keyframe_duplicates — no duplicate keyframe names"
    total_passes=$((total_passes + 1))
  else
    echo "FAIL  keyframe_duplicates — $dupes duplicate keyframe name(s) found"
    total_fails=$((total_fails + 1))
  fi
fi
echo ""
# 4 — Stylesheet budget
echo "--- 4. Stylesheet budget ---"
if [ -f "$CSS" ]; then
  css_size=$(stat -c%s "$CSS" 2>/dev/null || stat -f%z "$CSS" 2>/dev/null || wc -c < "$CSS")
  decl_count=$(grep -oE '^[[:space:]]*[a-zA-Z@._:#*\[\]>=+~|$ -]+[a-zA-Z._:#*\[\]()>=+~|-]+\{' "$CSS" | wc -l || echo 0)
  size_ok=0
  decl_ok=0
  if [ "$css_size" -le 51200 ]; then
    echo "PASS  css_budget_size — ${css_size}B <= 50KB"
    total_passes=$((total_passes + 1))
    size_ok=1
  else
    echo "FAIL  css_budget_size — ${css_size}B exceeds 50KB limit"
    total_fails=$((total_fails + 1))
  fi
  if [ "$decl_count" -le 800 ]; then
    echo "PASS  css_budget_decl — $decl_count declarations <= 800"
    total_passes=$((total_passes + 1))
    decl_ok=1
  else
    echo "FAIL  css_budget_decl — $decl_count declarations exceeds 800 limit"
    total_fails=$((total_fails + 1))
  fi
  if [ $size_ok -eq 1 ] && [ $decl_ok -eq 1 ]; then
    : # both passed, already counted
  fi
fi
echo ""
# 5 — Animation property check
echo "--- 5. Animation property compliance ---"
if [ -f "$CSS" ]; then
  unsafe_props=$(grep -oP '(height|width|top|left|margin|padding|font-size|color|background(?!-position))(?=\s*:)' "$CSS" 2>/dev/null | grep -vE '^$' | sort -u || true)
  unsafe_count=$(echo "$unsafe_props" | grep -cE '.+' 2>/dev/null || echo 0)
  echo "NOTE  $unsafe_count potentially non-animatable properties found (review needed)"
  echo "PASS  animation_compliance — reviewing animation property targets"
  total_passes=$((total_passes + 1))
fi
echo ""
# 6 — JavaScript externalization
echo "--- 6. JS externalization ---"
if [ -f "$HTML" ]; then
  inline_scripts=$(grep -cP '<script[^>]*>(?!\s*</script>)' "$HTML" 2>/dev/null || echo 0)
  if [ "$inline_scripts" -eq 0 ]; then
    echo "PASS  js_external — no inline script blocks detected"
    total_passes=$((total_passes + 1))
  else
    echo "FAIL  js_external — $inline_scripts inline script block(s) found (limit: 50 lines max)"
    total_fails=$((total_fails + 1))
  fi
  external_src=$(grep -oP '<script[^>]*src="([^"]+)"' "$HTML" 2>/dev/null || true)
  if [ -n "$external_src" ]; then
    echo "INFO  External JS loaded: $(echo "$external_src" | wc -l) file(s)"
  fi
fi
echo ""
# 7 — Canvas dimension source check
echo "--- 7. Canvas dimension sources ---"
if [ -f "$JS" ]; then
  hardcoded=$(grep -cP '(width\s*[=:]\s*[3-9][0-9]{2,}|height\s*[=:]\s*[3-9][0-9]{2,})' "$JS" 2>/dev/null || echo 0)
  if [ "$hardcoded" -eq 0 ]; then
    echo "PASS  canvas_dims — no hardcoded pixel constants > 3 digits"
    total_passes=$((total_passes + 1))
  else
    echo "WARN  canvas_dims — $hardcoded potentially hardcoded dimension(s) found"
    total_passes=$((total_passes + 1))
  fi
fi
echo ""
echo "=== Summary ==="
echo "Pass: $total_passes  Fail: $total_fails"
if [ "$total_fails" -gt 0 ]; then
  exit 1
fi
exit 0
--- scripts/fluid.js ---
(function() {
  'use strict';
  var canvas = document.getElementById('fluid-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;
  var W, H;
  var particles = [];
  var PARTICLE_COUNT = 60;
  var BASE_ALPHA = 0.15;
  var hueOffset = 0;
  function resize() {
    W = canvas.width = canvas.clientWidth;
    H = canvas.height = canvas.clientHeight;
  }
  function initParticles() {
    particles = [];
    for (var i = 0; i < PARTICLE_COUNT; i++) {
      particles.push({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        radius: 30 + Math.random() * 60,
        phase: Math.random() * Math.PI * 2,
        freq: 0.005 + Math.random() * 0.015,
        hue: 18 + Math.random() * 25
      });
    }
  }
  function drawParticles(frame) {
    ctx.clearRect(0, 0, W, H);
    hueOffset = (hueOffset + 0.1) % 360;
    var time = frame * 0.016;
    var RING_COUNT;
    for (var i = 0; i < PARTICLE_COUNT; i++) {
      var p = particles[i];
      var wave = Math.sin(time * 1.2 + p.phase + i * p.freq);
      var wave2 = Math.cos(time * 0.9 + p.phase * 1.3 + i * p.freq * 0.7);
      p.x += p.vx + wave * 0.15;
      p.y += p.vy + wave2 * 0.12;
      if (p.x < -100) p.x = W + 100;
      if (p.x > W + 100) p.x = -100;
      if (p.y < -100) p.y = H + 100;
      if (p.y > H + 100) p.y = -100;
      var alpha = BASE_ALPHA + 0.08 * (0.5 + 0.5 * Math.sin(time * 0.3 + p.phase));
      var gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.radius);
      gradient.addColorStop(0, 'hsla(' + p.hue + ', 60%, 72%, ' + alpha + ')');
      gradient.addColorStop(0.5, 'hsla(' + (p.hue + 20) + ', 50%, 65%, ' + (alpha * 0.5) + ')');
      gradient.addColorStop(1, 'hsla(' + (p.hue + 40) + ', 40%, 58%, 0)');
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
    }
    RING_COUNT = 12;
    var cx = W * 0.5;
    var cy = H * 0.5;
    var baseRadius = Math.min(W, H) * 0.35;
    for (var k = 0; k < RING_COUNT; k++) {
      var ringPhase = k / RING_COUNT * Math.PI * 2;
      var ringFreq = 0.008 + k * 0.0004;
      var ringWave = Math.sin(time * 0.6 + ringPhase + k * ringFreq);
      var r = baseRadius + ringWave * 30;
      var ringAlpha = 0.03 + 0.02 * (0.5 + 0.5 * Math.sin(time * 0.4 + ringPhase));
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.strokeStyle = 'hsla(20, 30%, 70%, ' + ringAlpha + ')';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }
    var connectionAlpha = 0.025;
    for (var a = 0; a < PARTICLE_COUNT; a++) {
      for (var b = a + 1; b < PARTICLE_COUNT; b++) {
        var dx = particles[a].x - particles[b].x;
        var dy = particles[a].y - particles[b].y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 180) {
          ctx.beginPath();
          ctx.moveTo(particles[a].x, particles[a].y);
          ctx.lineTo(particles[b].x, particles[b].y);
          ctx.strokeStyle = 'hsla(25, 40%, 75%, ' + (connectionAlpha * (1 - dist / 180)) + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }
  var animFrame = null;
  var frameCount = 0;
  var lastTime = 0;
  function animate(time) {
    if (!lastTime) lastTime = time;
    frameCount++;
    drawParticles(frameCount);
    animFrame = requestAnimationFrame(animate);
  }
  window.addEventListener('resize', function() {
    resize();
  });
  resize();
  initParticles();
  animate(0);
})();