FILE: index.html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Organic Fluid Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles/main.css">
</head>
<body>
<div class="dashboard">
<header class="dashboard__header">
<div class="header__blob" aria-hidden="true"></div>
<div class="header__content">
<h1 class="header__title">Flow State</h1>
<p class="header__subtitle">Your organic metrics at a glance</p>
</div>
<div class="header__time">
<span class="time__label">Current Session</span>
<span class="time__value" id="sessionTimer">00:00:00</span>
</div>
</header>
<main class="dashboard__grid">
<section class="card card--pulse" aria-label="Heart Rate Monitor">
<div class="card__blob card__blob--coral" aria-hidden="true"></div>
<div class="card__icon">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
</svg>
</div>
<h2 class="card__title">Heart Rate</h2>
<div class="card__value" id="heartRate">72</div>
<div class="card__unit">bpm</div>
<div class="card__pulse-ring" id="pulseRing">
<div class="pulse-ring__inner"></div>
</div>
<div class="card__status">
<span class="status__dot status__dot--active"></span>
<span class="status__text">Active</span>
</div>
</section>
<section class="card card--energy" aria-label="Energy Level">
<div class="card__blob card__blob--amber" aria-hidden="true"></div>
<div class="card__icon">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
</svg>
</div>
<h2 class="card__title">Energy Level</h2>
<div class="card__gauge">
<svg class="gauge__svg" viewBox="0 0 120 120">
<circle class="gauge__track" cx="60" cy="60" r="52" fill="none" stroke-width="8"/>
<circle class="gauge__fill" id="energyGauge" cx="60" cy="60" r="52" fill="none" stroke-width="8" stroke-dasharray="326.73" stroke-dashoffset="163.36" transform="rotate(-90 60 60)"/>
</svg>
<div class="gauge__center">
<span class="gauge__value" id="energyValue">74</span>
<span class="gauge__percent">%</span>
</div>
</div>
<div class="card__bars" id="energyBars">
<div class="bar bar--1" style="height: 45%"></div>
<div class="bar bar--2" style="height: 62%"></div>
<div class="bar bar--3" style="height: 58%"></div>
<div class="bar bar--4" style="height: 74%"></div>
<div class="bar bar--5" style="height: 70%"></div>
<div class="bar bar--6" style="height: 68%"></div>
</div>
</section>
<section class="card card--focus" aria-label="Focus Score">
<div class="card__blob card__blob--teal" aria-hidden="true"></div>
<div class="card__icon">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
</svg>
</div>
<h2 class="card__title">Focus Score</h2>
<div class="card__value card__value--large" id="focusScore">88</div>
<div class="card__score-bar">
<div class="score-bar__track">
<div class="score-bar__fill" id="focusBar" style="width: 88%"></div>
</div>
<div class="score-bar__labels">
<span>0</span>
<span>50</span>
<span>100</span>
</div>
</div>
<div class="card__trend" id="focusTrend">
<svg width="80" height="24" viewBox="0 0 80 24">
<polyline class="trend__line" points="0,18 16,14 32,16 48,8 64,10 80,4" fill="none" stroke-width="1.5"/>
</svg>
<span class="trend__label">+12% this week</span>
</div>
</section>
<section class="card card--wave" aria-label="Wave Visualizer">
<div class="card__blob card__blob--moss" aria-hidden="true"></div>
<div class="card__icon">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
<path d="M2 12c2-2 4-4 6 0s4 4 6 0 4-4 6 0 4 4 6 0"/>
</svg>
</div>
<h2 class="card__title">Activity Wave</h2>
<canvas class="wave__canvas" id="waveCanvas" width="320" height="120"></canvas>
<div class="wave__stats">
<span class="wave__stat">Peak: <strong id="wavePeak">0</strong></span>
<span class="wave__stat">Avg: <strong id="waveAvg">0</strong></span>
</div>
</section>
</main>
<footer class="dashboard__footer">
<div class="footer__timeline" id="timeline">
<div class="timeline__dot timeline__dot--active" data-time="6:00"></div>
<div class="timeline__dot" data-time="9:00"></div>
<div class="timeline__dot timeline__dot--active" data-time="12:00"></div>
<div class="timeline__dot" data-time="15:00"></div>
<div class="timeline__dot timeline__dot--active" data-time="18:00"></div>
</div>
<div class="footer__meta">
<span class="meta__item">Organic Dashboard v3.0</span>
<span class="meta__divider" aria-hidden="true">·</span>
<span class="meta__item">Designed with care</span>
</div>
</footer>
</div>
<script>
(function () {
'use strict';
var sessionStart = Date.now();
function updateSessionTimer() {
var elapsed = Date.now() - sessionStart;
var h = Math.floor(elapsed / 3600000);
var m = Math.floor((elapsed % 3600000) / 60000);
var s = Math.floor((elapsed % 60000) / 1000);
var timer = document.getElementById('sessionTimer');
if (timer) {
timer.textContent = String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
}
requestAnimationFrame(updateSessionTimer);
}
requestAnimationFrame(updateSessionTimer);
function simulateHeartRate() {
var hr = document.getElementById('heartRate');
var ring = document.getElementById('pulseRing');
var base = 70;
var variation = Math.random() * 8 - 4;
var val = Math.round(base + variation);
if (hr) hr.textContent = val;
if (ring) {
var scale = 1 + (val - 70) / 140;
ring.style.transform = 'scale(' + scale + ')';
}
setTimeout(simulateHeartRate, 2000 + Math.random() * 1000);
}
simulateHeartRate();
function simulateEnergy() {
var gauge = document.getElementById('energyGauge');
var energyVal = document.getElementById('energyValue');
var bars = document.querySelectorAll('.bar');
var circumference = 326.73;
var base = 70;
var val = Math.round(base + Math.random() * 12 - 6);
var offset = circumference - (val / 100) * circumference;
if (gauge) gauge.setAttribute('stroke-dashoffset', offset);
if (energyVal) energyVal.textContent = val;
bars.forEach(function (bar, i) {
var h = Math.round(40 + Math.random() * 45);
bar.style.height = h + '%';
});
setTimeout(simulateEnergy, 3000);
}
simulateEnergy();
function simulateFocus() {
var score = document.getElementById('focusScore');
var bar = document.getElementById('focusBar');
var base = 82;
var val = Math.round(base + Math.random() * 14 - 7);
if (score) score.textContent = val;
if (bar) bar.style.width = val + '%';
setTimeout(simulateFocus, 4000);
}
simulateFocus();
var waveCanvas = document.getElementById('waveCanvas');
if (waveCanvas) {
var ctx = waveCanvas.getContext('2d');
var w = waveCanvas.width;
var h = waveCanvas.height;
var phase = 0;
var peakEl = document.getElementById('wavePeak');
var avgEl = document.getElementById('waveAvg');
var samples = [];
var maxSamples = 60;
function drawWave() {
ctx.clearRect(0, 0, w, h);
var gradient = ctx.createLinearGradient(0, 0, 0, h);
gradient.addColorStop(0, 'rgba(232, 168, 124, 0.6)');
gradient.addColorStop(0.5, 'rgba(140, 181, 168, 0.4)');
gradient.addColorStop(1, 'rgba(138, 154, 122, 0.15)');
ctx.beginPath();
ctx.moveTo(0, h);
var peak = 0;
var sum = 0;
var count = 0;
for (var x = 0; x <= w; x += 2) {
var t = x / w;
var y = h / 2
+ Math.sin(t * Math.PI * 4 + phase) * 20
+ Math.sin(t * Math.PI * 7 + phase * 0.7) * 12
+ Math.sin(t * Math.PI * 11 + phase * 1.3) * 6;
var amp = Math.abs(y - h / 2);
if (amp > peak) peak = amp;
sum += amp;
count++;
ctx.lineTo(x, y);
}
ctx.lineTo(w, h);
ctx.closePath();
ctx.fillStyle = gradient;
ctx.fill();
ctx.beginPath();
for (var x2 = 0; x2 <= w; x2 += 2) {
var t2 = x2 / w;
var y2 = h / 2
+ Math.sin(t2 * Math.PI * 4 + phase) * 20
+ Math.sin(t2 * Math.PI * 7 + phase * 0.7) * 12
+ Math.sin(t2 * Math.PI * 11 + phase * 1.3) * 6;
if (x2 === 0) ctx.moveTo(x2, y2);
else ctx.lineTo(x2, y2);
}
ctx.strokeStyle = 'rgba(61, 44, 30, 0.3)';
ctx.lineWidth = 1.5;
ctx.stroke();
phase += 0.03;
samples.push(peak);
if (samples.length > maxSamples) samples.shift();
var avg = samples.reduce(function (a, b) { return a + b; }, 0) / samples.length;
if (peakEl) peakEl.textContent = Math.round(peak);
if (avgEl) avgEl.textContent = Math.round(avg);
requestAnimationFrame(drawWave);
}
requestAnimationFrame(drawWave);
}
var dots = document.querySelectorAll('.timeline__dot');
dots.forEach(function (dot) {
dot.addEventListener('click', function () {
dots.forEach(function (d) { d.classList.remove('timeline__dot--selected'); });
dot.classList.add('timeline__dot--selected');
});
});
})();
</script>
</body>
</html>
FILE: styles/main.css
:root {
--bg-primary: #fdf6ee;
--bg-secondary: #f5ebe0;
--bg-card: rgba(255, 255, 255, 0.72);
--text-primary: #3d2c1e;
--text-secondary: #7a6856;
--text-muted: #b8a99a;
--accent-coral: #e8a87c;
--accent-coral-light: #f2c9a8;
--accent-amber: #d4956b;
--accent-amber-light: #e8c4a0;
--accent-teal: #8cb5a8;
--accent-teal-light: #b5d4c8;
--accent-moss: #8a9a7a;
--accent-moss-light: #b0bea0;
--shadow-soft: 0 8px 32px rgba(61, 44, 30, 0.08);
--shadow-glow-coral: 0 4px 24px rgba(232, 168, 124, 0.25);
--shadow-glow-teal: 0 4px 24px rgba(140, 181, 168, 0.25);
--radius-sm: 8px;
--radius-md: 16px;
--radius-lg: 24px;
--radius-xl: 32px;
--radius-round: 50%;
--font-body: 'Inter', system-ui, -apple-system, sans-serif;
--font-display: 'Inter', system-ui, -apple-system, sans-serif;
--transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-2xl: 48px;
--z-header: 10;
--z-card: 1;
--z-blob: 0;
}
*, *::before, *::after {
margin: 0;
padding: 0;
box-sizing: border-box;
}
html {
font-size: 16px;
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
}
body {
font-family: var(--font-body);
background: var(--bg-primary);
color: var(--text-primary);
min-height: 100vh;
overflow-x: hidden;
background-image:
radial-gradient(ellipse at 20% 10%, rgba(232, 168, 124, 0.12) 0%, transparent 50%),
radial-gradient(ellipse at 80% 20%, rgba(140, 181, 168, 0.10) 0%, transparent 50%),
radial-gradient(ellipse at 50% 80%, rgba(138, 154, 122, 0.08) 0%, transparent 50%);
}
.dashboard {
max-width: 1120px;
margin: 0 auto;
padding: var(--spacing-lg);
display: flex;
flex-direction: column;
gap: var(--spacing-xl);
min-height: 100vh;
}
.dashboard__header {
position: relative;
padding: var(--spacing-2xl) var(--spacing-xl);
background: var(--bg-card);
-webkit-backdrop-filter: blur(12px);
backdrop-filter: blur(12px);
border-radius: var(--radius-xl);
box-shadow: var(--shadow-soft);
display: flex;
align-items: center;
justify-content: space-between;
overflow: hidden;
}
.header__blob {
position: absolute;
width: 300px;
height: 300px;
border-radius: var(--radius-round);
background: radial-gradient(circle, var(--accent-coral-light) 0%, transparent 70%);
top: -100px;
right: -60px;
z-index: var(--z-blob);
animation: blobFloat 8s ease-in-out infinite;
}
.header__content {
position: relative;
z-index: var(--z-card);
}
.header__title {
font-family: var(--font-display);
font-size: 2rem;
font-weight: 600;
color: var(--text-primary);
letter-spacing: -0.02em;
line-height: 1.2;
}
.header__subtitle {
font-size: 0.95rem;
color: var(--text-secondary);
margin-top: var(--spacing-xs);
font-weight: 400;
}
.header__time {
text-align: right;
position: relative;
z-index: var(--z-card);
}
.time__label {
display: block;
font-size: 0.75rem;
color: var(--text-muted);
text-transform: uppercase;
letter-spacing: 0.08em;
margin-bottom: 2px;
}
.time__value {
font-family: var(--font-display);
font-size: 1.35rem;
font-weight: 600;
color: var(--accent-coral);
font-variant-numeric: tabular-nums;
}
.dashboard__grid {
display: grid;
grid-template-columns: 1fr 1fr;
gap: var(--spacing-lg);
}
@media (max-width: 720px) {
.dashboard__grid {
grid-template-columns: 1fr;
}
.dashboard {
padding: var(--spacing-md);
}
.header__title {
font-size: 1.5rem;
}
}
.card {
position: relative;
background: var(--bg-card);
-webkit-backdrop-filter: blur(8px);
backdrop-filter: blur(8px);
border-radius: var(--radius-lg);
padding: var(--spacing-lg);
box-shadow: var(--shadow-soft);
overflow: hidden;
transition: var(--transition);
display: flex;
flex-direction: column;
gap: var(--spacing-sm);
}
.card:hover {
transform: translateY(-2px);
box-shadow: 0 12px 40px rgba(61, 44, 30, 0.12);
}
.card__blob {
position: absolute;
width: 180px;
height: 180px;
border-radius: var(--radius-round);
z-index: var(--z-blob);
pointer-events: none;
}
.card__blob--coral {
background: radial-gradient(circle, rgba(232, 168, 124, 0.15) 0%, transparent 70%);
top: -60px;
right: -40px;
animation: blobFloat 10s ease-in-out infinite;
}
.card__blob--amber {
background: radial-gradient(circle, rgba(212, 149, 107, 0.15) 0%, transparent 70%);
bottom: -50px;
left: -30px;
animation: blobFloat 12s ease-in-out infinite reverse;
}
.card__blob--teal {
background: radial-gradient(circle, rgba(140, 181, 168, 0.15) 0%, transparent 70%);
top: -40px;
left: -30px;
animation: blobFloat 9s ease-in-out infinite;
}
.card__blob--moss {
background: radial-gradient(circle, rgba(138, 154, 122, 0.15) 0%, transparent 70%);
bottom: -40px;
right: -20px;
animation: blobFloat 11s ease-in-out infinite reverse;
}
.card__icon {
position: relative;
z-index: var(--z-card);
color: var(--accent-coral);
width: 36px;
height: 36px;
display: flex;
align-items: center;
justify-content: center;
background: rgba(232, 168, 124, 0.12);
border-radius: var(--radius-md);
}
.card--energy .card__icon { color: var(--accent-amber); background: rgba(212, 149, 107, 0.12); }
.card--focus .card__icon { color: var(--accent-teal); background: rgba(140, 181, 168, 0.12); }
.card--wave .card__icon { color: var(--accent-moss); background: rgba(138, 154, 122, 0.12); }
.card__title {
position: relative;
z-index: var(--z-card);
font-size: 0.8rem;
font-weight: 500;
color: var(--text-muted);
text-transform: uppercase;
letter-spacing: 0.06em;
}
.card__value {
position: relative;
z-index: var(--z-card);
font-family: var(--font-display);
font-size: 2.5rem;
font-weight: 700;
color: var(--text-primary);
letter-spacing: -0.03em;
line-height: 1;
}
.card__value--large {
font-size: 3rem;
}
.card__unit {
font-size: 0.8rem;
color: var(--text-secondary);
position: relative;
z-index: var(--z-card);
}
.card__pulse-ring {
position: absolute;
top: 50%;
right: 20px;
transform: translateY(-50%);
z-index: var(--z-card);
transition: transform 0.3s ease;
}
.pulse-ring__inner {
width: 48px;
height: 48px;
border-radius: var(--radius-round);
background: rgba(232, 168, 124, 0.15);
animation: pulse 2s ease-in-out infinite;
}
.card__status {
display: flex;
align-items: center;
gap: var(--spacing-xs);
position: relative;
z-index: var(--z-card);
margin-top: auto;
}
.status__dot {
width: 6px;
height: 6px;
border-radius: var(--radius-round);
background: var(--text-muted);
}
.status__dot--active {
background: var(--accent-coral);
box-shadow: 0 0 8px rgba(232, 168, 124, 0.5);
animation: pulse 2s ease-in-out infinite;
}
.status__text {
font-size: 0.75rem;
color: var(--text-muted);
}
.card__gauge {
position: relative;
z-index: var(--z-card);
display: flex;
justify-content: center;
align-items: center;
width: 120px;
height: 120px;
margin: var(--spacing-sm) auto;
}
.gauge__svg {
width: 120px;
height: 120px;
}
.gauge__track {
stroke: rgba(212, 149, 107, 0.12);
}
.gauge__fill {
stroke: var(--accent-amber);
stroke-linecap: round;
transition: stroke-dashoffset 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.gauge__center {
position: absolute;
top: 50%;
left: 50%;
transform: translate(-50%, -50%);
text-align: center;
}
.gauge__value {
font-family: var(--font-display);
font-size: 1.5rem;
font-weight: 700;
color: var(--text-primary);
}
.gauge__percent {
font-size: 0.7rem;
color: var(--text-secondary);
display: block;
margin-top: -2px;
}
.card__bars {
display: flex;
align-items: flex-end;
gap: 4px;
height: 48px;
position: relative;
z-index: var(--z-card);
margin-top: var(--spacing-sm);
}
.bar {
flex: 1;
border-radius: 4px 4px 0 0;
background: linear-gradient(to top, var(--accent-amber-light), var(--accent-amber));
opacity: 0.6;
transition: height 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
min-height: 8px;
}
.bar:nth-child(odd) {
background: linear-gradient(to top, var(--accent-teal-light), var(--accent-teal));
opacity: 0.5;
}
.card__score-bar {
position: relative;
z-index: var(--z-card);
margin-top: var(--spacing-sm);
}
.score-bar__track {
height: 8px;
background: rgba(140, 181, 168, 0.12);
border-radius: 4px;
overflow: hidden;
}
.score-bar__fill {
height: 100%;
background: linear-gradient(90deg, var(--accent-teal-light), var(--accent-teal));
border-radius: 4px;
transition: width 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.score-bar__labels {
display: flex;
justify-content: space-between;
margin-top: 4px;
font-size: 0.65rem;
color: var(--text-muted);
}
.card__trend {
display: flex;
align-items: center;
gap: var(--spacing-sm);
margin-top: var(--spacing-sm);
position: relative;
z-index: var(--z-card);
}
.trend__line {
stroke: var(--accent-teal);
}
.trend__label {
font-size: 0.75rem;
color: var(--accent-teal);
font-weight: 500;
}
.wave__canvas {
width: 100%;
height: auto;
border-radius: var(--radius-md);
position: relative;
z-index: var(--z-card);
margin-top: var(--spacing-sm);
display: block;
background: rgba(138, 154, 122, 0.04);
}
.wave__stats {
display: flex;
gap: var(--spacing-lg);
position: relative;
z-index: var(--z-card);
margin-top: var(--spacing-xs);
}
.wave__stat {
font-size: 0.75rem;
color: var(--text-secondary);
}
.wave__stat strong {
font-weight: 600;
color: var(--text-primary);
}
.dashboard__footer {
display: flex;
flex-direction: column;
align-items: center;
gap: var(--spacing-lg);
padding: var(--spacing-lg) 0;
}
.footer__timeline {
display: flex;
align-items: center;
gap: 32px;
position: relative;
}
.footer__timeline::before {
content: '';
position: absolute;
top: 50%;
left: 0;
right: 0;
height: 2px;
background: linear-gradient(90deg, transparent, var(--accent-coral-light), var(--accent-teal-light), transparent);
transform: translateY(-50%);
}
.timeline__dot {
width: 12px;
height: 12px;
border-radius: var(--radius-round);
background: var(--bg-secondary);
border: 2px solid var(--accent-coral-light);
cursor: pointer;
position: relative;
transition: var(--transition);
}
.timeline__dot::after {
content: attr(data-time);
position: absolute;
top: 18px;
left: 50%;
transform: translateX(-50%);
font-size: 0.65rem;
color: var(--text-muted);
white-space: nowrap;
}
.timeline__dot--active {
background: var(--accent-coral);
border-color: var(--accent-coral);
box-shadow: 0 0 0 4px rgba(232, 168, 124, 0.15);
}
.timeline__dot--selected {
background: var(--accent-teal);
border-color: var(--accent-teal);
box-shadow: 0 0 0 4px rgba(140, 181, 168, 0.2);
}
.footer__meta {
display: flex;
align-items: center;
gap: var(--spacing-sm);
font-size: 0.7rem;
color: var(--text-muted);
}
.meta__divider {
opacity: 0.5;
}
@keyframes blobFloat {
0%, 100% { transform: translate(0, 0) scale(1); }
33% { transform: translate(10px, -12px) scale(1.05); }
66% { transform: translate(-8px, 8px) scale(0.95); }
}
@keyframes pulse {
0%, 100% { transform: scale(1); opacity: 0.6; }
50% { transform: scale(1.15); opacity: 1; }
}
FILE: scripts/validate.sh
#!/usr/bin/env bash
set -u
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FAIL_COUNT=0
PASS_COUNT=0
check() {
    local label=$1 desc=$2
    shift 2
    "$@"
    local rc=$?
    if [ $rc -ne 0 ]; then
        echo "FAIL | $label | $desc"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        echo "PASS | $label | $desc"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}
check_html5() {
    local file=$1
    local has_doctype
    has_doctype=$(head -1 "$file" | grep -c '<!DOCTYPE html>' || true)
    local has_html
    has_html=$(grep -c '<html' "$file" || true)
    local has_head
    has_head=$(grep -c '<head>' "$file" || true)
    local has_body_open
    has_body_open=$(grep -c '<body>' "$file" || true)
    local has_body_close
    has_body_close=$(grep -c '</body>' "$file" || true)
    local has_html_close
    has_html_close=$(grep -c '</html>' "$file" || true)
    local errors=()
    local line_ref=""
    if [ "$has_doctype" -eq 0 ]; then
        errors+=("missing DOCTYPE")
        line_ref+=" line:1"
    fi
    if [ "$has_html" -eq 0 ]; then
        errors+=("missing <html>")
        line_ref+=" grep:<html>"
    fi
    if [ "$has_head" -eq 0 ]; then
        errors+=("missing <head>")
        line_ref+=" grep:<head>"
    fi
    if [ "$has_body_open" -eq 0 ]; then
        errors+=("missing <body>")
        line_ref+=" grep:<body>"
    fi
    if [ "$has_body_close" -eq 0 ]; then
        errors+=("missing </body>")
        line_ref+=" grep:</body>"
    fi
    if [ "$has_html_close" -eq 0 ]; then
        errors+=("missing </html>")
        line_ref+=" grep:</html>"
    fi
    if [ ${#errors[@]} -gt 0 ]; then
        local msg
        msg=$(IFS=", "; echo "${errors[*]}")
        echo "FAIL | HTML5 Structure | $msg$line_ref"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        return 1
    fi
    echo "PASS | HTML5 Structure | all required tags present"
    PASS_COUNT=$((PASS_COUNT + 1))
    return 0
}
check_tag_balance() {
    local file=$1
    local void_elements=("area" "base" "br" "col" "embed" "hr" "img" "input" "link" "meta" "param" "source" "track" "wbr")
    local tags
    tags=$(grep -oP '</?[a-zA-Z][a-zA-Z0-9]*\b[^>]*>' "$file" || true)
    local open_tags
    local close_tags
    local errors=0
    local line_report=""
    while IFS= read -r tag; do
        local raw_name
        raw_name=$(echo "$tag" | grep -oP '^</?[a-zA-Z][a-zA-Z0-9]*')
        raw_name=${raw_name#</}
        raw_name=${raw_name#<}
        local is_void=0
        for ve in "${void_elements[@]}"; do
            if [ "$raw_name" = "$ve" ]; then is_void=1; break; fi
        done
        local is_self_closing=0
        if echo "$tag" | grep -q '/>$'; then is_self_closing=1; fi
        if [ "$is_void" -eq 1 ] || [ "$is_self_closing" -eq 1 ]; then
            continue
        fi
        if echo "$tag" | grep -q '^</'; then
            close_tags="$close_tags $raw_name"
        else
            open_tags="$open_tags $raw_name"
        fi
    done <<< "$tags"
    local open_list=($open_tags)
    local close_list=($close_tags)
    local unmatched=0
    local depth=0
    local balance_ok=true
    local idx=0
    for tag_name in "${open_list[@]}"; do
        local found=false
        for ((j=idx; j<${#close_list[@]}; j++)); do
            if [ "${close_list[$j]}" = "$tag_name" ]; then
                close_list[$j]="__USED__"
                found=true
                break
            fi
        done
        if [ "$found" = false ]; then
            echo "FAIL | Tag Balance | unmatched <$tag_name> -- no corresponding </$tag_name> found"
            FAIL_COUNT=$((FAIL_COUNT + 1))
            balance_ok=false
        fi
        idx=$((idx + 1))
    done
    if [ "$balance_ok" = true ]; then
        echo "PASS | Tag Balance | all open tags have matching close tags"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}
check_css_vars() {
    local css_file=$1 html_file=$2
    local defined_vars
    defined_vars=$(grep -oP -- '--[a-zA-Z0-9-]+' "$css_file" | sort -u)
    local referenced
    referenced=$(grep -oP -- 'var\(--[a-zA-Z0-9-]+' "$css_file" "$html_file" | grep -oP -- '--[a-zA-Z0-9-]+' | sort -u)
    local missing=0
    while IFS= read -r ref; do
        if [ -z "$ref" ]; then continue; fi
        if ! echo "$defined_vars" | grep -qF "$ref"; then
            local location
            location=$(grep -n "var($ref" "$css_file" "$html_file" | head -3 | paste -sd ' ' || true)
            echo "FAIL | CSS Variable $ref | referenced but not defined in :root -- $location"
            FAIL_COUNT=$((FAIL_COUNT + 1))
            missing=$((missing + 1))
        fi
    done <<< "$referenced"
    if [ "$missing" -eq 0 ]; then
        echo "PASS | CSS Variables | all referenced custom properties defined in :root"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}
check_duplicate_keyframes() {
    local css_file=$1
    local names
    names=$(grep -oP '@keyframes\s+([a-zA-Z0-9_-]+)' "$css_file" | awk '{print $2}' | sort)
    local dupes
    dupes=$(echo "$names" | uniq -d)
    if [ -n "$dupes" ]; then
        while IFS= read -r name; do
            if [ -z "$name" ]; then continue; fi
            local locations
            locations=$(grep -n "@keyframes $name" "$css_file" | awk -F: '{print $1}' | paste -sd ',' || true)
            echo "FAIL | Duplicate Keyframes | '$name' defined multiple times at lines: $locations"
            FAIL_COUNT=$((FAIL_COUNT + 1))
        done <<< "$dupes"
    else
        echo "PASS | Duplicate Keyframes | no duplicate keyframe names found"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}
check_stylesheet_budget() {
    local css_file=$1
    local size
    size=$(wc -c < "$css_file")
    local decl_count
    decl_count=$(grep -c '{\s*$' "$css_file" || true)
    local budget_size=51200
    local budget_decl=800
    local oversize=0
    local file_label="$css_file"
    if [ "$size" -gt "$budget_size" ]; then
        echo "FAIL | Stylesheet Budget | $file_label: ${size} bytes exceeds ${budget_size} byte limit"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        oversize=$((oversize + 1))
    fi
    if [ "$decl_count" -gt "$budget_decl" ]; then
        echo "FAIL | Stylesheet Budget | $file_label: ${decl_count} declarations exceeds ${budget_decl} limit"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        oversize=$((oversize + 1))
    fi
    if [ "$oversize" -eq 0 ]; then
        echo "PASS | Stylesheet Budget | $file_label: ${size} bytes, ${decl_count} declarations within limits"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}
check_animation_usage() {
    local css_file=$1
    local animation_props
    animation_props=$(grep -cP '^\s*(?:animation|animation-name)\s*:' "$css_file" || true)
    local invalid_props
    invalid_props=$(grep -oP '(animation-|transition-)[a-z-]+(?=\s*:)' "$css_file" | grep -vP '^(animation|animation-name|animation-duration|animation-timing-function|animation-delay|animation-iteration-count|animation-direction|animation-fill-mode|animation-play-state|transition|transition-property|transition-duration|transition-timing-function|transition-delay)$' || true)
    if [ -n "$invalid_props" ]; then
        echo "FAIL | Animation Usage | non-standard animation properties detected: $(echo "$invalid_props" | tr '\n' ' ')"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        echo "PASS | Animation Usage | all animation properties use standard browser-compatible values"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}
check_doctype_charset() {
    local file=$1
    local charset_meta
    charset_meta=$(grep -i '<meta.*charset' "$file" || true)
    local line_num
    line_num=$(grep -n -i '<meta.*charset' "$file" | head -1 | awk -F: '{print $1}' || true)
    if [ -z "$charset_meta" ]; then
        echo "FAIL | Charset Meta | missing charset meta tag in <head>"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        echo "PASS | Charset Meta | charset meta found at line $line_num"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
}
HTML_FILE="$ROOT_DIR/index.html"
CSS_FILE="$ROOT_DIR/styles/main.css"
if [ ! -f "$HTML_FILE" ]; then
    echo "FAIL | File Check | index.html not found at $HTML_FILE"
    exit 1
fi
if [ ! -f "$CSS_FILE" ]; then
    echo "FAIL | File Check | main.css not found at $CSS_FILE"
    exit 1
fi
echo "=== Organic Fluid Dashboard Validation ==="
echo ""
check_doctype_charset "$HTML_FILE"
check_html5 "$HTML_FILE"
check_tag_balance "$HTML_FILE"
check_css_vars "$CSS_FILE" "$HTML_FILE"
check_duplicate_keyframes "$CSS_FILE"
check_stylesheet_budget "$CSS_FILE"
check_animation_usage "$CSS_FILE"
echo ""
echo "=== Summary: $PASS_COUNT passed, $FAIL_COUNT failed ==="
if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
fi
exit 0