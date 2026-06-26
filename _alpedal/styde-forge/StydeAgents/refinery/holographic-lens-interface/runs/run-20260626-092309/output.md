```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Holographic Lens Interface</title>
<style>
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
:root {
  --bg-depth: 400px;
  --fg-speed: 0.06;
  --mg-speed: 0.025;
  --bg-speed: 0.01;
  --blur-fg: 2px;
  --blur-mg: 6px;
  --blur-bg: 14px;
  --glass-opacity-fg: 0.75;
  --glass-opacity-mg: 0.55;
  --glass-opacity-bg: 0.30;
  --hue-base: 220;
  --hue-primary: 190;
  --hue-accent: 280;
  --glow-color: rgba(100, 180, 255, 0.15);
}
body {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #0a0e1a;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  color: #e0e8f0;
  perspective: 1200px;
  perspective-origin: center;
}
#lens-container {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  overflow: hidden;
}
/* ===== BACKGROUND LAYER ===== */
.layer-background {
  position: absolute;
  inset: -20%;
  width: 140%;
  height: 140%;
  transform-style: preserve-3d;
  transform: translateZ(calc(var(--bg-depth) * -1)) scale(1.4);
  pointer-events: none;
  z-index: 0;
}
.bg-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(100, 180, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(100, 180, 255, 0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: gridPulse 8s ease-in-out infinite alternate;
}
.bg-ambient-glow {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse 50% 40% at 20% 30%, rgba(80, 160, 255, 0.12) 0%, transparent 70%),
    radial-gradient(ellipse 40% 50% at 80% 60%, rgba(180, 80, 255, 0.08) 0%, transparent 70%),
    radial-gradient(ellipse 60% 30% at 50% 80%, rgba(0, 200, 255, 0.06) 0%, transparent 70%);
  animation: glowDrift 12s ease-in-out infinite alternate;
}
.bg-orbs {
  position: absolute;
  inset: 0;
  filter: blur(40px);
}
.bg-orb {
  position: absolute;
  border-radius: 50%;
  opacity: 0.3;
  animation: orbFloat 20s ease-in-out infinite;
}
.bg-orb:nth-child(1) {
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(60, 140, 255, 0.25), transparent);
  top: 10%; left: 15%;
  animation-duration: 22s;
  animation-delay: -3s;
}
.bg-orb:nth-child(2) {
  width: 250px; height: 250px;
  background: radial-gradient(circle, rgba(200, 100, 255, 0.2), transparent);
  bottom: 20%; right: 10%;
  animation-duration: 18s;
  animation-delay: -7s;
}
.bg-orb:nth-child(3) {
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(0, 220, 255, 0.15), transparent);
  top: 50%; left: 60%;
  animation-duration: 25s;
  animation-delay: -12s;
}
/* ===== MIDGROUND LAYER ===== */
.layer-midground {
  position: absolute;
  inset: -8%;
  width: 116%;
  height: 116%;
  transform-style: preserve-3d;
  transform: translateZ(0);
  z-index: 1;
  pointer-events: none;
}
.mg-glass-panel {
  position: absolute;
  border-radius: 20px;
  background: rgba(20, 30, 60, var(--glass-opacity-mg));
  backdrop-filter: blur(var(--blur-mg));
  -webkit-backdrop-filter: blur(var(--blur-mg));
  border: 1px solid rgba(100, 180, 255, 0.10);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  pointer-events: auto;
  overflow: hidden;
}
.mg-glass-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, transparent 50%);
  pointer-events: none;
  border-radius: inherit;
}
.panel-metrics {
  width: 420px;
  height: 200px;
  top: 10%;
  left: 5%;
  padding: 24px 28px;
}
.panel-chart {
  width: 380px;
  height: 280px;
  bottom: 12%;
  right: 5%;
  padding: 20px 24px;
}
.panel-activity {
  width: 300px;
  height: 320px;
  top: 12%;
  right: 8%;
  padding: 20px 22px;
}
.panel-data {
  width: 340px;
  height: 180px;
  bottom: 15%;
  left: 8%;
  padding: 20px 24px;
}
.panel-header {
  font-size: 13px;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: rgba(160, 200, 255, 0.7);
  margin-bottom: 12px;
  font-weight: 500;
}
.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(100, 180, 255, 0.06);
}
.metric-label {
  font-size: 13px;
  color: rgba(180, 210, 240, 0.7);
}
.metric-value {
  font-size: 18px;
  font-weight: 600;
  color: #b0d4ff;
  letter-spacing: 0.5px;
}
.metric-value.accent {
  color: #7fcdff;
}
.metric-value.success {
  color: #6fcf97;
}
.metric-value.warning {
  color: #f2c94c;
}
/* Mini bar chart in chart panel */
.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 160px;
  padding-top: 10px;
}
.chart-bar {
  flex: 1;
  border-radius: 4px 4px 0 0;
  background: linear-gradient(180deg, rgba(80, 180, 255, 0.6), rgba(80, 180, 255, 0.2));
  min-height: 8px;
  transition: height 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}
.chart-bar:hover {
  background: linear-gradient(180deg, rgba(100, 200, 255, 0.8), rgba(100, 200, 255, 0.3));
  box-shadow: 0 0 12px rgba(80, 180, 255, 0.3);
}
.chart-bar-label {
  position: absolute;
  bottom: -18px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 9px;
  color: rgba(160, 200, 255, 0.5);
}
/* Activity list */
.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid rgba(100, 180, 255, 0.05);
  font-size: 13px;
}
.activity-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.activity-dot.online { background: #6fcf97; }
.activity-dot.alert { background: #f2c94c; }
.activity-dot.offline { background: #eb5757; }
.activity-dot.info { background: #7fcdff; }
.activity-text {
  flex: 1;
  color: rgba(200, 220, 240, 0.85);
}
.activity-time {
  font-size: 11px;
  color: rgba(160, 200, 255, 0.4);
}
/* Data panel */
.data-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.data-cell {
  background: rgba(100, 180, 255, 0.04);
  border-radius: 10px;
  padding: 12px 14px;
  text-align: center;
}
.data-cell-number {
  font-size: 22px;
  font-weight: 700;
  color: #b0d4ff;
  line-height: 1.2;
}
.data-cell-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: rgba(160, 200, 255, 0.5);
  margin-top: 4px;
}
/* ===== FOREGROUND LAYER ===== */
.layer-foreground {
  position: absolute;
  inset: 0;
  transform-style: preserve-3d;
  transform: translateZ(80px);
  z-index: 2;
  pointer-events: none;
}
.fg-glass-panel {
  position: absolute;
  border-radius: 16px;
  background: rgba(15, 25, 50, var(--glass-opacity-fg));
  backdrop-filter: blur(var(--blur-fg));
  -webkit-backdrop-filter: blur(var(--blur-fg));
  border: 1px solid rgba(100, 180, 255, 0.12);
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.04);
  pointer-events: auto;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.fg-glass-panel:hover {
  transform: translateY(-2px);
  box-shadow:
    0 8px 40px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
}
.fg-glass-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 50%);
  pointer-events: none;
  border-radius: inherit;
}
/* Title bar */
.panel-titlebar {
  position: absolute;
  top: 8%;
  left: 50%;
  transform: translateX(-50%);
  width: 520px;
  height: 56px;
  padding: 0 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.panel-titlebar h1 {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 1.5px;
  background: linear-gradient(90deg, #b0d4ff, #d4b0ff);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.titlebar-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(160, 200, 255, 0.6);
}
.titlebar-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6fcf97;
  animation: pulseDot 2s ease-in-out infinite;
}
/* Control group */
.control-group {
  position: absolute;
  bottom: 6%;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  pointer-events: auto;
}
.ctrl-btn {
  padding: 10px 22px;
  border-radius: 10px;
  border: 1px solid rgba(100, 180, 255, 0.15);
  background: rgba(20, 35, 70, 0.6);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  color: #b0d4ff;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.5px;
  cursor: pointer;
  transition: all 0.2s ease;
  pointer-events: auto;
}
.ctrl-btn:hover {
  background: rgba(60, 120, 220, 0.25);
  border-color: rgba(100, 180, 255, 0.35);
  box-shadow: 0 0 20px rgba(80, 160, 255, 0.15);
  transform: translateY(-1px);
}
.ctrl-btn:active {
  transform: translateY(0);
  background: rgba(60, 120, 220, 0.35);
}
.ctrl-btn.primary {
  background: linear-gradient(135deg, rgba(60, 140, 255, 0.3), rgba(140, 80, 255, 0.2));
  border-color: rgba(100, 180, 255, 0.3);
}
.ctrl-btn.primary:hover {
  background: linear-gradient(135deg, rgba(60, 140, 255, 0.45), rgba(140, 80, 255, 0.35));
  box-shadow: 0 0 25px rgba(80, 160, 255, 0.25);
}
/* Depth control slider */
.depth-slider-container {
  position: absolute;
  right: 3%;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  pointer-events: auto;
}
.depth-slider-label {
  font-size: 10px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: rgba(160, 200, 255, 0.5);
  writing-mode: vertical-lr;
  text-orientation: mixed;
}
.depth-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 120px;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(90deg, rgba(60, 140, 255, 0.3), rgba(140, 80, 255, 0.3));
  outline: none;
  cursor: pointer;
  transform: rotate(-90deg);
}
.depth-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: rgba(100, 180, 255, 0.6);
  border: 2px solid rgba(100, 180, 255, 0.3);
  cursor: pointer;
  transition: all 0.2s ease;
}
.depth-slider::-webkit-slider-thumb:hover {
  background: rgba(100, 180, 255, 0.8);
  box-shadow: 0 0 12px rgba(80, 160, 255, 0.4);
}
.depth-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: rgba(100, 180, 255, 0.6);
  border: 2px solid rgba(100, 180, 255, 0.3);
  cursor: pointer;
}
/* Notification toast */
.toast {
  position: fixed;
  bottom: 80px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  background: rgba(20, 35, 70, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(100, 180, 255, 0.15);
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 13px;
  color: rgba(200, 220, 240, 0.9);
  opacity: 0;
  transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  z-index: 100;
  pointer-events: none;
}
.toast.visible {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
  pointer-events: auto;
}
/* Chromatic aberration on hover */
.chromatic-trigger {
  transition: all 0.3s ease;
}
.chromatic-trigger:hover {
  text-shadow:
    2px 0 0 rgba(255, 50, 50, 0.4),
    -2px 0 0 rgba(50, 100, 255, 0.4);
}
/* SVG refraction overlay */
.refraction-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 50;
  opacity: 0.15;
  mix-blend-mode: overlay;
}
/* Animations */
@keyframes gridPulse {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}
@keyframes glowDrift {
  0% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(2%, -1%) scale(1.02); }
  100% { transform: translate(-1%, 2%) scale(1.01); }
}
@keyframes orbFloat {
  0% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(5%, 3%) scale(1.05); }
  50% { transform: translate(-3%, -4%) scale(0.95); }
  75% { transform: translate(4%, 2%) scale(1.02); }
  100% { transform: translate(0, 0) scale(1); }
}
@keyframes pulseDot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
/* Glass refraction overlap effect */
.mg-glass-panel + .mg-glass-panel,
.fg-glass-panel + .fg-glass-panel {
  transition: filter 0.3s ease;
}
/* Responsive scaling */
@media (max-width: 900px) {
  .panel-metrics { width: 300px; height: 180px; top: 8%; left: 4%; }
  .panel-chart { width: 280px; height: 220px; bottom: 10%; right: 4%; }
  .panel-activity { width: 240px; height: 260px; top: 8%; right: 4%; }
  .panel-data { width: 260px; height: 150px; bottom: 12%; left: 4%; }
  .panel-titlebar { width: 90%; }
}
</style>
</head>
<body>
<div id="lens-container">
  <!-- Background Layer -->
  <div class="layer-background" id="layer-bg">
    <div class="bg-grid"></div>
    <div class="bg-ambient-glow"></div>
    <div class="bg-orbs">
      <div class="bg-orb"></div>
      <div class="bg-orb"></div>
      <div class="bg-orb"></div>
    </div>
  </div>
  <!-- Midground Layer -->
  <div class="layer-midground" id="layer-mg">
    <div class="mg-glass-panel panel-metrics">
      <div class="panel-header">System Metrics</div>
      <div class="metric-row">
        <span class="metric-label">Throughput</span>
        <span class="metric-value accent" id="metric-throughput">847 GB/s</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Latency</span>
        <span class="metric-value success" id="metric-latency">12 ms</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Error Rate</span>
        <span class="metric-value warning" id="metric-errors">0.03%</span>
      </div>
      <div class="metric-row">
        <span class="metric-label">Active Nodes</span>
        <span class="metric-value accent" id="metric-nodes">24 / 24</span>
      </div>
    </div>
    <div class="mg-glass-panel panel-chart">
      <div class="panel-header">Bandwidth (last 24h)</div>
      <div class="chart-bars" id="chart-bars"></div>
    </div>
    <div class="mg-glass-panel panel-activity">
      <div class="panel-header">Live Activity</div>
      <div id="activity-list">
        <div class="activity-item">
          <span class="activity-dot online"></span>
          <span class="activity-text">Node ALPHA-7 connected</span>
          <span class="activity-time">2s ago</span>
        </div>
        <div class="activity-item">
          <span class="activity-dot alert"></span>
          <span class="activity-text">Memory pressure on SIGMA-3</span>
          <span class="activity-time">47s ago</span>
        </div>
        <div class="activity-item">
          <span class="activity-dot online"></span>
          <span class="activity-text">Replication complete — zone B</span>
          <span class="activity-time">3m ago</span>
        </div>
        <div class="activity-item">
          <span class="activity-dot info"></span>
          <span class="activity-text">System check passed</span>
          <span class="activity-time">5m ago</span>
        </div>
        <div class="activity-item">
          <span class="activity-dot offline"></span>
          <span class="activity-text">Node DELTA-2 offline</span>
          <span class="activity-time">12m ago</span>
        </div>
      </div>
    </div>
    <div class="mg-glass-panel panel-data">
      <div class="panel-header">Data Overview</div>
      <div class="data-grid">
        <div class="data-cell">
          <div class="data-cell-number" id="data-total">1.4M</div>
          <div class="data-cell-label">Requests</div>
        </div>
        <div class="data-cell">
          <div class="data-cell-number" id="data-active">847</div>
          <div class="data-cell-label">Active</div>
        </div>
        <div class="data-cell">
          <div class="data-cell-number" id="data-avg">2.3s</div>
          <div class="data-cell-label">Avg Time</div>
        </div>
        <div class="data-cell">
          <div class="data-cell-number" id="data-peak">99.7%</div>
          <div class="data-cell-label">Uptime</div>
        </div>
      </div>
    </div>
  </div>
  <!-- Foreground Layer -->
  <div class="layer-foreground" id="layer-fg">
    <div class="fg-glass-panel panel-titlebar">
      <h1 class="chromatic-trigger">HOLOGRAPHIC LENS</h1>
      <div class="titlebar-status">
        <span class="titlebar-dot"></span>
        <span>SYSTEM ONLINE</span>
      </div>
    </div>
    <div class="control-group">
      <button class="ctrl-btn" id="btn-refresh">Refresh Data</button>
      <button class="ctrl-btn" id="btn-layout">Reset Layout</button>
      <button class="ctrl-btn primary" id="btn-scan">Deep Scan</button>
      <button class="ctrl-btn" id="btn-export">Export Report</button>
    </div>
    <div class="depth-slider-container">
      <span class="depth-slider-label">Depth</span>
      <input type="range" class="depth-slider" id="depth-slider" min="0" max="100" value="50">
    </div>
  </div>
  <!-- Refraction overlay -->
  <svg class="refraction-overlay" viewBox="0 0 100 100" preserveAspectRatio="none">
    <filter id="refraction-filter">
      <feTurbulence type="fractalNoise" baseFrequency="0.008" numOctaves="2" result="noise" />
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="6" xChannelSelector="R" yChannelSelector="G" />
    </filter>
    <rect width="100" height="100" filter="url(#refraction-filter)" opacity="0.3" fill="none" />
  </svg>
  <!-- Toast notification -->
  <div class="toast" id="toast"></div>
</div>
<script>
(function() {
  'use strict';
  var container = document.getElementById('lens-container');
  var bgLayer = document.getElementById('layer-bg');
  var mgLayer = document.getElementById('layer-mg');
  var fgLayer = document.getElementById('layer-fg');
  // Shared parallax handler
  function applyParallax(mouseX, mouseY) {
    var rect = container.getBoundingClientRect();
    var centerX = rect.left + rect.width / 2;
    var centerY = rect.top + rect.height / 2;
    var dx = (mouseX - centerX) / rect.width;
    var dy = (mouseY - centerY) / rect.height;
    var depthVal = parseFloat(document.getElementById('depth-slider').value) / 100;
    var bgFactor = 0.015 + depthVal * 0.02;
    var mgFactor = 0.03 + depthVal * 0.04;
    var fgFactor = 0.06 + depthVal * 0.08;
    bgLayer.style.transform =
      'translateZ(calc(var(--bg-depth) * -1)) scale(1.4) ' +
      'translate(' + (dx * bgFactor * 100) + 'px, ' + (dy * bgFactor * 100) + 'px)';
    mgLayer.style.transform =
      'translateZ(0) ' +
      'translate(' + (dx * mgFactor * 100) + 'px, ' + (dy * mgFactor * 100) + 'px)';
    fgLayer.style.transform =
      'translateZ(80px) ' +
      'translate(' + (dx * fgFactor * 100) + 'px, ' + (dy * fgFactor * 100) + 'px)';
  }
  // Mouse parallax
  document.addEventListener('mousemove', function(e) {
    applyParallax(e.clientX, e.clientY);
  });
  // DeviceOrientation parallax fallback
  if (window.DeviceOrientationEvent) {
    window.addEventListener('deviceorientation', function(e) {
      if (e.beta === null || e.gamma === null) return;
      var rect = container.getBoundingClientRect();
      var cx = rect.left + rect.width / 2;
      var cy = rect.top + rect.height / 2;
      var tiltX = e.gamma * 2;
      var tiltY = e.beta * 2 - 45;
      var px = cx + tiltX * 3;
      var py = cy + tiltY * 3;
      applyParallax(px, py);
    }, { passive: true });
  }
  // Depth slider
  var slider = document.getElementById('depth-slider');
  slider.addEventListener('input', function() {
    var val = this.value;
    // Re-apply parallax with new depth on next mouse move — immediate visual update
    var e = window._lastMouseEvent;
    if (e) applyParallax(e.clientX, e.clientY);
  });
  // Track last mouse event
  document.addEventListener('mousemove', function(e) {
    window._lastMouseEvent = e;
  });
  // Toast system — single shared function
  function showToast(msg, duration) {
    duration = duration || 2000;
    var toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.add('visible');
    if (window._toastTimer) clearTimeout(window._toastTimer);
    window._toastTimer = setTimeout(function() {
      toast.classList.remove('visible');
    }, duration);
  }
  // Bar chart generation
  function generateBars() {
    var container = document.getElementById('chart-bars');
    container.innerHTML = '';
    var data = [35, 55, 42, 78, 65, 92, 58, 44, 71, 83, 49, 62, 88, 53, 38, 76, 94, 60, 45, 69, 81, 56, 72, 40];
    var maxVal = Math.max.apply(null, data);
    var labels = ['0h','1h','2h','3h','4h','5h','6h','7h','8h','9h','10h','11h','12h','13h','14h','15h','16h','17h','18h','19h','20h','21h','22h','23h'];
    data.forEach(function(val, i) {
      var bar = document.createElement('div');
      bar.className = 'chart-bar';
      var pct = (val / maxVal) * 100;
      bar.style.height = Math.max(8, pct) + '%';
      var label = document.createElement('span');
      label.className = 'chart-bar-label';
      label.textContent = labels[i] || '';
      bar.appendChild(label);
      setTimeout(function() {
        bar.style.height = pct + '%';
      }, 50 + i * 30);
      container.appendChild(bar);
    });
  }
  // Functional handlers for all controls
  document.getElementById('btn-refresh').addEventListener('click', function() {
    showToast('Data refresh initiated — pulling latest metrics');
    // Simulate metric update
    var throughput = (700 + Math.floor(Math.random() * 300)) + ' GB/s';
    var latency = (8 + Math.floor(Math.random() * 15)) + ' ms';
    var errors = (Math.random() * 0.08).toFixed(3) + '%';
    var nodes = (20 + Math.floor(Math.random() * 5)) + ' / 24';
    document.getElementById('metric-throughput').textContent = throughput;
    document.getElementById('metric-latency').textContent = latency;
    document.getElementById('metric-errors').textContent = errors;
    document.getElementById('metric-nodes').textContent = nodes;
    // Update data cells
    document.getElementById('data-total').textContent = (1 + Math.random() * 0.8).toFixed(1) + 'M';
    document.getElementById('data-active').textContent = Math.floor(600 + Math.random() * 500);
    document.getElementById('data-avg').textContent = (1.5 + Math.random() * 2.5).toFixed(1) + 's';
    document.getElementById('data-peak').textContent = (98 + Math.random() * 1.9).toFixed(1) + '%';
  });
  document.getElementById('btn-layout').addEventListener('click', function() {
    showToast('Layout reset — panels repositioned');
    // Reset any inline transforms on panels to default
    var panels = document.querySelectorAll('.mg-glass-panel, .fg-glass-panel');
    panels.forEach(function(p) {
      p.style.transform = '';
      p.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
      setTimeout(function() { p.style.transition = ''; }, 600);
    });
  });
  document.getElementById('btn-scan').addEventListener('click', function() {
    var btn = document.getElementById('btn-scan');
    btn.textContent = 'Scanning...';
    btn.disabled = true;
    showToast('Deep scan started — analyzing system topology');
    setTimeout(function() {
      btn.textContent = 'Deep Scan';
      btn.disabled = false;
      // Add an activity entry
      var list = document.getElementById('activity-list');
      var item = document.createElement('div');
      item.className = 'activity-item';
      item.innerHTML =
        '<span class="activity-dot info"></span>' +
        '<span class="activity-text">Deep scan complete — all zones nominal</span>' +
        '<span class="activity-time">just now</span>';
      list.insertBefore(item, list.firstChild);
      // Keep only last 7 items
      while (list.children.length > 7) {
        list.removeChild(list.lastChild);
      }
      showToast('Scan complete — no anomalies detected');
    }, 2000);
  });
  document.getElementById('btn-export').addEventListener('click', function() {
    showToast('Exporting report as HDF5...');
    setTimeout(function() {
      var ts = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      showToast('Report exported: lens-report-' + ts + '.h5');
    }, 800);
  });
  // Keyboard shortcuts
  document.addEventListener('keydown', function(e) {
    if (e.key === 'r' || e.key === 'R') {
      document.getElementById('btn-refresh').click();
    } else if (e.key === 's' || e.key === 'S') {
      document.getElementById('btn-scan').click();
    } else if (e.key === 'e' || e.key === 'E') {
      document.getElementById('btn-export').click();
    } else if (e.key === 'l' || e.key === 'L') {
      document.getElementById('btn-layout').click();
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowRight') {
      slider.value = Math.min(100, parseInt(slider.value) + 5);
      slider.dispatchEvent(new Event('input'));
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowLeft') {
      slider.value = Math.max(0, parseInt(slider.value) - 5);
      slider.dispatchEvent(new Event('input'));
    }
  });
  // Init
  generateBars();
  showToast('Holographic Lens active — move mouse to explore depth', 2500);
})();
</script>
</body>
</html>
```