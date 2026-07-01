Now I have the full data picture. Building the SVG timeline with interactive scrubber, colored nodes, and click-to-detail popups.
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1200" height="680" viewBox="0 0 1200 680"
     style="background:#0f172a;font-family:'Segoe UI','SF Pro',system-ui,sans-serif">
<defs>
  <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#0f172a"/>
    <stop offset="100%" stop-color="#1e293b"/>
  </linearGradient>
  <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f59e0b"/>
    <stop offset="100%" stop-color="#fbbf24"/>
  </linearGradient>
  <linearGradient id="amberGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#d97706"/>
    <stop offset="100%" stop-color="#f59e0b"/>
  </linearGradient>
  <linearGradient id="coolGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#6366f1"/>
    <stop offset="100%" stop-color="#818cf8"/>
  </linearGradient>
  <linearGradient id="coolerGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#4f46e5"/>
    <stop offset="100%" stop-color="#6366f1"/>
  </linearGradient>
  <linearGradient id="playGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#10b981"/>
    <stop offset="100%" stop-color="#34d399"/>
  </linearGradient>
  <linearGradient id="pauseGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#f59e0b"/>
    <stop offset="100%" stop-color="#fbbf24"/>
  </linearGradient>
  <filter id="glow">
    <feGaussianBlur stdDeviation="2" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="shadow">
    <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.4"/>
  </filter>
  <filter id="popupShadow">
    <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="0.6"/>
  </filter>
</defs>
<rect width="1200" height="680" fill="url(#bgGrad)"/>
<!-- Title -->
<text x="30" y="38" fill="#f1f5f9" font-size="20" font-weight="700" letter-spacing="0.5">Agent Lifecycle Timeline</text>
<text x="30" y="56" fill="#64748b" font-size="12">Styde Forge forge-runs session — 2026-06-27/28</text>
<!-- Legend -->
<rect x="780" y="22" width="12" height="12" rx="6" fill="url(#goldGrad)" filter="url(#glow)"/>
<text x="798" y="33" fill="#94a3b8" font-size="11">Gold 85+</text>
<rect x="858" y="22" width="12" height="12" rx="6" fill="url(#amberGrad)"/>
<text x="876" y="33" fill="#94a3b8" font-size="11">Amber 70-84</text>
<rect x="938" y="22" width="12" height="12" rx="6" fill="url(#coolerGrad)"/>
<text x="956" y="33" fill="#94a3b8" font-size="11">Cool &lt;70</text>
<rect x="1016" y="22" width="12" height="12" rx="6" fill="#475569"/>
<text x="1034" y="33" fill="#94a3b8" font-size="11">Spawn/Iter</text>
<!-- Time axis -->
<line x1="180" y1="585" x2="1140" y2="585" stroke="#334155" stroke-width="2"/>
<!-- Tick marks -->
<g fill="#64748b" font-size="10" text-anchor="middle">
  <line x1="180" y1="580" x2="180" y2="590" stroke="#475569" stroke-width="1.5"/>
  <text x="180" y="604" fill="#64748b">23:50</text>
  <line x1="420" y1="580" x2="420" y2="590" stroke="#475569" stroke-width="1.5"/>
  <text x="420" y="604" fill="#64748b">00:10</text>
  <line x1="660" y1="580" x2="660" y2="590" stroke="#475569" stroke-width="1.5"/>
  <text x="660" y="604" fill="#64748b">00:30</text>
  <line x1="900" y1="580" x2="900" y2="590" stroke="#475569" stroke-width="1.5"/>
  <text x="900" y="604" fill="#64748b">00:50</text>
  <line x1="1140" y1="580" x2="1140" y2="590" stroke="#475569" stroke-width="1.5"/>
  <text x="1140" y="604" fill="#64748b">01:10/28</text>
</g>
<!-- Time indicator (scrubber needle) -->
<g id="scrubber">
  <line x1="180" y1="80" x2="180" y2="572" stroke="#f59e0b" stroke-width="1.5" opacity="0.35"/>
  <polygon points="180,78 174,90 186,90" fill="#f59e0b" filter="url(#shadow)"/>
</g>
<!-- Slider track -->
<rect x="180" y="618" width="960" height="4" rx="2" fill="#334155"/>
<rect id="sliderFill" x="180" y="618" width="0" height="4" rx="2" fill="url(#goldGrad)"/>
<circle id="sliderThumb" cx="180" cy="620" r="10" fill="#f59e0b" stroke="#fbbf24" stroke-width="2" filter="url(#shadow)" style="cursor:pointer"/>
<circle id="sliderThumbInner" cx="180" cy="620" r="4" fill="#1e293b"/>
<!-- Play/Pause button -->
<rect id="playBtn" x="50" y="606" width="80" height="28" rx="14" fill="url(#playGrad)" filter="url(#shadow)" style="cursor:pointer"/>
<text id="playLabel" x="90" y="625" fill="#0f172a" font-size="12" font-weight="600" text-anchor="middle">Play</text>
<!-- Time label on slider -->
<text id="timeLabel" x="180" y="650" fill="#f59e0b" font-size="11" font-weight="600">23:50</text>
<!-- Click detail popup (hidden by default) -->
<g id="popup" display="none">
  <rect id="popupBg" x="0" y="0" width="0" height="0" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1" filter="url(#popupShadow)"/>
  <text id="popupTitle" x="0" y="0" fill="#f1f5f9" font-size="14" font-weight="700"/>
  <text id="popupRunId" x="0" y="0" fill="#64748b" font-size="11"/>
  <text id="popupVersion" x="0" y="0" fill="#94a3b8" font-size="12"/>
  <text id="popupStage" x="0" y="0" fill="#94a3b8" font-size="12"/>
  <text id="popupScore" x="0" y="0" fill="#fbbf24" font-size="14" font-weight="700"/>
  <text id="popupBench" x="0" y="0" fill="#94a3b8" font-size="11"/>
  <rect id="popupClose" x="0" y="0" width="20" height="20" rx="4" fill="#475569" style="cursor:pointer"/>
  <text id="popupCloseX" x="0" y="0" fill="#f1f5f9" font-size="12" font-weight="700" text-anchor="middle" style="cursor:pointer">X</text>
</g>
<!-- Blueprint tracks and node data -->
<script type="text/ecmascript"><![CDATA[
var data = {
  blueprints: [
    {
      name: '3d-data-terrain-explorer',
      y: 92,
      nodes: [
        {x:240, stage:'eval', score:90.2, run_id:'20260627-235152', detail:'S:89 J:91 C:90.2', version:'iter 3', benchmark:'auto'},
        {x:260, stage:'spawn', score:-1, run_id:'20260627-235120', detail:'18028 chars', version:'spawn', benchmark:''},
        {x:300, stage:'eval', score:87.4, run_id:'20260627-235836', detail:'S:91 J:85 C:87.4', version:'iter 4', benchmark:'auto'},
        {x:310, stage:'spawn', score:-1, run_id:'20260627-235801', detail:'1648 chars', version:'spawn', benchmark:''},
        {x:330, stage:'eval', score:87.2, run_id:'20260627-235721', detail:'S:80 J:92 C:87.2', version:'iter 5', benchmark:'auto'},
        {x:345, stage:'spawn', score:-1, run_id:'20260627-235923', detail:'4338 chars', version:'spawn', benchmark:''},
        {x:370, stage:'eval', score:86.6, run_id:'20260628-000003', detail:'S:89 J:85 C:86.6', version:'iter 6', benchmark:'auto'},
        {x:385, stage:'spawn', score:-1, run_id:'20260628-000253', detail:'3996 chars', version:'spawn', benchmark:''},
        {x:410, stage:'eval', score:78.4, run_id:'20260628-000325', detail:'S:70 J:84 C:78.4', version:'iter 7', benchmark:'auto'},
        {x:425, stage:'spawn', score:-1, run_id:'20260628-000613', detail:'17498 chars', version:'spawn', benchmark:''},
        {x:440, stage:'eval', score:85.2, run_id:'20260628-000642', detail:'S:84 J:86 C:85.2', version:'iter 8', benchmark:'auto'},
        {x:460, stage:'spawn', score:-1, run_id:'20260628-000805', detail:'14307 chars', version:'spawn', benchmark:''},
        {x:475, stage:'eval', score:90.4, run_id:'20260628-000841', detail:'S:91 J:90 C:90.4', version:'iter 9', benchmark:'auto'},
        {x:490, stage:'spawn', score:-1, run_id:'20260628-001205', detail:'6614 chars', version:'spawn', benchmark:''},
        {x:510, stage:'eval', score:93.0, run_id:'20260628-001231', detail:'S:87 J:97 C:93.0', version:'iter 10', benchmark:'auto'},
        {x:530, stage:'spawn', score:-1, run_id:'20260628-001252', detail:'iter 8/5', version:'spawn', benchmark:''},
        {x:560, stage:'spawn', score:-1, run_id:'20260628-004211', detail:'7299 chars', version:'spawn', benchmark:''},
        {x:580, stage:'eval', score:91.0, run_id:'20260628-004247', detail:'S:88 J:93 C:91.0', version:'iter 11', benchmark:'auto'},
        {x:610, stage:'spawn', score:-1, run_id:'20260628-004459', detail:'9250 chars', version:'spawn', benchmark:''},
        {x:625, stage:'eval', score:68.0, run_id:'20260628-004527', detail:'S:62 J:72 C:68.0', version:'eval', benchmark:'auto'},
        {x:820, stage:'improve', score:-1, run_id:'20260628-012633', detail:'S:65 J:62 C:63.2', version:'improve', benchmark:'alt'}
      ]
    },
    {
      name: 'ab-testing-statistician',
      y: 137,
      nodes: [
        {x:200, stage:'spawn', score:-1, run_id:'20260627-234813', detail:'iter 1/5', version:'spawn', benchmark:''},
        {x:330, stage:'spawn', score:-1, run_id:'20260628-000056', detail:'673 chars', version:'spawn', benchmark:''},
        {x:340, stage:'eval', score:68.0, run_id:'20260628-000125', detail:'S:62 J:72 C:68.0', version:'init', benchmark:'auto'},
        {x:360, stage:'spawn', score:-1, run_id:'20260628-000213', detail:'2952 chars', version:'spawn', benchmark:''},
        {x:370, stage:'eval', score:73.8, run_id:'20260628-000245', detail:'S:72 J:75 C:73.8', version:'iter 2', benchmark:'auto'},
        {x:390, stage:'spawn', score:-1, run_id:'20260628-000636', detail:'9671 chars', version:'spawn', benchmark:''},
        {x:410, stage:'eval', score:92.2, run_id:'20260628-000706', detail:'S:94 J:91 C:92.2', version:'prod', benchmark:'auto'}
      ]
    },
    {
      name: 'accessibility-auditor',
      y: 182,
      nodes: [
        {x:190, stage:'spawn', score:-1, run_id:'20260627-234813', detail:'iter 1/5', version:'spawn', benchmark:''},
        {x:620, stage:'eval', score:51.0, run_id:'20260628-004653', detail:'S:30 J:65 C:51.0', version:'init', benchmark:'auto'},
        {x:640, stage:'spawn', score:-1, run_id:'20260628-004653', detail:'iter 2', version:'spawn', benchmark:''},
        {x:670, stage:'eval', score:88.0, run_id:'20260628-005217', detail:'S:82 J:92 C:88.0', version:'prod', benchmark:'auto'}
      ]
    },
    {
      name: 'activity-feed-designer',
      y: 227,
      nodes: [
        {x:185, stage:'spawn', score:-1, run_id:'20260627-234903', detail:'iter 1/5', version:'spawn', benchmark:''},
        {x:620, stage:'spawn', score:-1, run_id:'20260628-004642', detail:'10796 chars', version:'spawn', benchmark:''},
        {x:630, stage:'eval', score:84.6, run_id:'20260628-004712', detail:'S:72 J:93 C:84.6', version:'eval 1', benchmark:'auto'},
        {x:640, stage:'spawn', score:-1, run_id:'20260628-004814', detail:'9962 chars', version:'spawn', benchmark:''},
        {x:650, stage:'eval', score:92.6, run_id:'20260628-004843', detail:'S:92 J:93 C:92.6', version:'eval 2', benchmark:'auto'},
        {x:660, stage:'spawn', score:-1, run_id:'20260628-005013', detail:'17823 chars', version:'spawn', benchmark:''},
        {x:670, stage:'eval', score:92.2, run_id:'20260628-005112', detail:'S:91 J:93 C:92.2', version:'eval 3', benchmark:'auto'},
        {x:680, stage:'spawn', score:-1, run_id:'20260628-005232', detail:'14723 chars', version:'spawn', benchmark:''},
        {x:690, stage:'spawn', score:-1, run_id:'20260628-005410', detail:'12214 chars', version:'spawn', benchmark:''},
        {x:700, stage:'eval', score:91.0, run_id:'20260628-005305', detail:'S:88 J:93 C:91.0', version:'eval 4', benchmark:'auto'},
        {x:710, stage:'spawn', score:-1, run_id:'20260628-005548', detail:'15389 chars', version:'spawn', benchmark:''},
        {x:720, stage:'eval', score:88.6, run_id:'20260628-005437', detail:'S:82 J:93 C:88.6', version:'eval 5', benchmark:'auto'},
        {x:730, stage:'spawn', score:-1, run_id:'20260628-005753', detail:'24693 chars', version:'spawn', benchmark:''},
        {x:740, stage:'eval', score:94.6, run_id:'20260628-005617', detail:'S:91 J:97 C:94.6', version:'eval 6', benchmark:'auto'},
        {x:750, stage:'spawn', score:-1, run_id:'20260628-005936', detail:'11121 chars', version:'spawn', benchmark:''},
        {x:760, stage:'eval', score:89.4, run_id:'20260628-005833', detail:'S:93 J:87 C:89.4', version:'eval 7', benchmark:'auto'},
        {x:770, stage:'spawn', score:-1, run_id:'20260628-005959', detail:'16644 chars', version:'spawn', benchmark:''},
        {x:780, stage:'eval', score:88.2, run_id:'20260628-010021', detail:'S:90 J:87 C:88.2', version:'eval 8', benchmark:'auto'},
        {x:800, stage:'eval', score:69.2, run_id:'20260628-010509', detail:'S:68 J:70 C:69.2', version:'eval 9', benchmark:'auto'}
      ]
    },
    {
      name: 'adaptive-metric-layout',
      y: 272,
      nodes: [
        {x:410, stage:'spawn', score:-1, run_id:'20260628-000641', detail:'17301 chars', version:'spawn', benchmark:''},
        {x:425, stage:'eval', score:87.2, run_id:'20260628-010717', detail:'S:83 J:90 C:87.2', version:'eval 1', benchmark:'auto'},
        {x:440, stage:'spawn', score:-1, run_id:'20260628-010846', detail:'23177 chars', version:'spawn', benchmark:''},
        {x:455, stage:'spawn', score:-1, run_id:'20260628-011133', detail:'32118 chars', version:'spawn', benchmark:''},
        {x:465, stage:'eval', score:80.2, run_id:'20260628-010932', detail:'S:76 J:83 C:80.2', version:'eval 2', benchmark:'auto'},
        {x:478, stage:'spawn', score:-1, run_id:'20260628-011529', detail:'22218 chars', version:'spawn', benchmark:''},
        {x:490, stage:'eval', score:77.0, run_id:'20260628-011222', detail:'S:56 J:91 C:77.0', version:'eval 3', benchmark:'auto'},
        {x:500, stage:'spawn', score:-1, run_id:'20260628-011318', detail:'6407 chars', version:'spawn', benchmark:''},
        {x:515, stage:'eval', score:89.8, run_id:'20260628-011403', detail:'S:82 J:95 C:89.8', version:'eval 4', benchmark:'auto'},
        {x:540, stage:'spawn', score:-1, run_id:'20260628-012052', detail:'22765 chars', version:'spawn', benchmark:''},
        {x:555, stage:'eval', score:77.2, run_id:'20260628-011609', detail:'S:58 J:90 C:77.2', version:'eval 5', benchmark:'auto'},
        {x:570, stage:'spawn', score:-1, run_id:'20260628-012507', detail:'39540 chars', version:'spawn', benchmark:''},
        {x:585, stage:'eval', score:88.2, run_id:'20260628-012141', detail:'S:84 J:91 C:88.2', version:'eval 6', benchmark:'auto'},
        {x:605, stage:'eval', score:62.0, run_id:'20260628-012543', detail:'S:62 J:62 C:62.0', version:'eval 7', benchmark:'auto'}
      ]
    },
    {
      name: 'aesthetic-style-composer',
      y: 317,
      nodes: [
        {x:415, stage:'spawn', score:-1, run_id:'20260628-001301', detail:'10371 chars', version:'spawn', benchmark:''},
        {x:425, stage:'eval', score:86.8, run_id:'20260628-010805', detail:'S:79 J:92 C:86.8', version:'eval 1', benchmark:'auto'},
        {x:435, stage:'spawn', score:-1, run_id:'20260628-011602', detail:'54627 chars', version:'spawn', benchmark:''},
        {x:465, stage:'eval', score:85.4, run_id:'20260628-011333', detail:'S:80 J:89 C:85.4', version:'eval 2', benchmark:'auto'},
        {x:480, stage:'spawn', score:-1, run_id:'20260628-011855', detail:'33964 chars', version:'spawn', benchmark:''},
        {x:495, stage:'eval', score:83.8, run_id:'20260628-011641', detail:'S:82 J:85 C:83.8', version:'eval 3', benchmark:'auto'},
        {x:510, stage:'spawn', score:-1, run_id:'20260628-012254', detail:'70052 chars', version:'spawn', benchmark:''},
        {x:525, stage:'eval', score:85.2, run_id:'20260628-011947', detail:'S:78 J:90 C:85.2', version:'eval 4', benchmark:'auto'},
        {x:535, stage:'spawn', score:-1, run_id:'20260628-012357', detail:'iter 6/5', version:'spawn', benchmark:''},
        {x:555, stage:'eval', score:75.6, run_id:'20260628-012328', detail:'S:72 J:78 C:75.6', version:'eval 5', benchmark:'auto'},
        {x:575, stage:'spawn', score:-1, run_id:'20260628-012357', detail:'iter 6/5', version:'spawn', benchmark:''},
        {x:605, stage:'eval', score:63.2, run_id:'20260628-012631', detail:'S:65 J:62 C:63.2', version:'eval 6', benchmark:'auto'}
      ]
    },
    {
      name: 'agent-promotion-evaluator',
      y: 362,
      nodes: [
        {x:580, stage:'spawn', score:-1, run_id:'20260628-012827', detail:'4353 chars', version:'spawn', benchmark:''},
        {x:605, stage:'eval', score:90.2, run_id:'20260628-012856', detail:'S:86 J:93 C:90.2', version:'eval', benchmark:'auto'},
        {x:615, stage:'spawn', score:-1, run_id:'20260628-012917', detail:'iter 2/5', version:'spawn', benchmark:''}
      ]
    },
    {
      name: 'agent-lifecycle-timeline',
      y: 407,
      nodes: [
        {x:600, stage:'spawn', score:-1, run_id:'20260628-012917', detail:'iter 1/5', version:'spawn', benchmark:''},
        {x:630, stage:'eval', score:75.6, run_id:'20260628-013616', detail:'S:78 J:74 C:75.6', version:'eval', benchmark:'auto'},
        {x:640, stage:'spawn', score:-1, run_id:'20260628-013643', detail:'iter 2/5', version:'spawn', benchmark:''}
      ]
    },
    {
      name: 'zero-knowledge-proof-dev',
      y: 452,
      nodes: [
        {x:50, stage:'spawn', score:-1, run_id:'20260627-232257', detail:'iter 1/5', version:'spawn', benchmark:''},
        {x:835, stage:'spawn', score:-1, run_id:'20260628-013536', detail:'17727 chars', version:'spawn', benchmark:''}
      ]
    }
  ]
};
var popup = document.getElementById('popup');
var popupBg = document.getElementById('popupBg');
var popupTitle = document.getElementById('popupTitle');
var popupRunId = document.getElementById('popupRunId');
var popupVersion = document.getElementById('popupVersion');
var popupStage = document.getElementById('popupStage');
var popupScore = document.getElementById('popupScore');
var popupBench = document.getElementById('popupBench');
var popupClose = document.getElementById('popupClose');
var popupCloseX = document.getElementById('popupCloseX');
function showPopup(evt, d) {
  var rect = evt.target.getBoundingClientRect();
  var svgRect = document.querySelector('svg').getBoundingClientRect();
  var px = rect.left - svgRect.left + 20;
  var py = rect.top - svgRect.top - 10;
  if (px + 280 > 1160) px = rect.left - svgRect.left - 280;
  if (py + 120 > 660) py = rect.top - svgRect.top - 120;
  if (py < 80) py = rect.top - svgRect.top + 10;
  popupBg.setAttribute('x', px);
  popupBg.setAttribute('y', py);
  popupBg.setAttribute('width', 270);
  popupBg.setAttribute('height', d.stage === 'spawn' ? 110 : 130);
  popupTitle.setAttribute('x', px + 14);
  popupTitle.setAttribute('y', py + 20);
  popupTitle.textContent = d.bp;
  popupRunId.setAttribute('x', px + 14);
  popupRunId.setAttribute('y', py + 38);
  popupRunId.textContent = 'Run: ' + d.run_id;
  popupVersion.setAttribute('x', px + 14);
  popupVersion.setAttribute('y', py + 54);
  popupVersion.textContent = 'Version: ' + d.version;
  popupStage.setAttribute('x', px + 14);
  popupStage.setAttribute('y', py + 70);
  popupStage.textContent = 'Stage: ' + d.stage;
  if (d.stage === 'eval' && d.score >= 0) {
    popupScore.setAttribute('x', px + 14);
    popupScore.setAttribute('y', py + 90);
    popupScore.textContent = 'Score: ' + d.score.toFixed(1);
    popupScore.setAttribute('display', 'block');
    popupBench.setAttribute('x', px + 14);
    popupBench.setAttribute('y', py + 108);
    popupBench.textContent = 'Benchmark: ' + d.benchmark;
    popupBench.setAttribute('display', 'block');
    popupVersion.setAttribute('y', py + 54);
    popupStage.setAttribute('y', py + 70);
  } else {
    popupScore.setAttribute('display', 'none');
    popupBench.setAttribute('display', 'none');
    if (d.detail) {
      popupStage.textContent = 'Detail: ' + d.detail;
    }
  }
  popupClose.setAttribute('x', px + 240);
  popupClose.setAttribute('y', py + 4);
  popupCloseX.setAttribute('x', px + 250);
  popupCloseX.setAttribute('y', py + 17);
  popupClose.setAttribute('data-px', px);
  popupClose.setAttribute('data-py', py);
  popup.setAttribute('display', 'block');
}
function hidePopup() {
  popup.setAttribute('display', 'none');
}
popupClose.addEventListener('click', hidePopup);
popupCloseX.addEventListener('click', hidePopup);
function nodeColor(score) {
  if (score >= 85) return 'url(#goldGrad)';
  if (score >= 70) return 'url(#amberGrad)';
  if (score >= 0) return 'url(#coolerGrad)';
  return '#475569';
}
function nodeSize(score) {
  if (score >= 85) return 10;
  if (score >= 70) return 8;
  if (score >= 0) return 7;
  return 5;
}
function renderNodes() {
  var ns = 'http://www.w3.org/2000/svg';
  var tracks = document.querySelector('svg');
  for (var b = 0; b < data.blueprints.length; b++) {
    var bp = data.blueprints[b];
    for (var n = 0; n < bp.nodes.length; n++) {
      var node = bp.nodes[n];
      node.bp = bp.name;
      var color = nodeColor(node.score);
      var r = nodeSize(node.score);
      var circle = document.createElementNS(ns, 'circle');
      circle.setAttribute('cx', node.x);
      circle.setAttribute('cy', bp.y);
      circle.setAttribute('r', r);
      circle.setAttribute('fill', color);
      if (node.score >= 85) circle.setAttribute('filter', 'url(#glow)');
      circle.setAttribute('stroke', '#0f172a');
      circle.setAttribute('stroke-width', '1.5');
      circle.setAttribute('style', 'cursor:pointer;transition:r 0.15s');
      circle.addEventListener('mouseenter', function(e) { e.target.setAttribute('r', Math.min(14, parseFloat(e.target.getAttribute('r')) + 3)); });
      circle.addEventListener('mouseleave', function(e) { e.target.setAttribute('r', Math.max(5, parseFloat(e.target.getAttribute('r')) - 3)); });
      (function(d) {
        circle.addEventListener('click', function(e) { showPopup(e, d); });
      })(node);
      tracks.insertBefore(circle, tracks.firstChild);
      // Score label for eval nodes
      if (node.stage === 'eval' && node.score >= 0) {
        var lbl = document.createElementNS(ns, 'text');
        lbl.setAttribute('x', node.x);
        lbl.setAttribute('y', bp.y - r - 6);
        lbl.setAttribute('fill', node.score >= 85 ? '#fbbf24' : node.score >= 70 ? '#f59e0b' : '#818cf8');
        lbl.setAttribute('font-size', '9');
        lbl.setAttribute('text-anchor', 'middle');
        lbl.setAttribute('font-weight', '600');
        lbl.textContent = node.score.toFixed(1);
        tracks.insertBefore(lbl, tracks.firstChild);
      }
      // Connecting line between nodes on same track
      if (n > 0) {
        var prev = bp.nodes[n - 1];
        var line = document.createElementNS(ns, 'line');
        line.setAttribute('x1', prev.x);
        line.setAttribute('y1', bp.y);
        line.setAttribute('x2', node.x);
        line.setAttribute('y2', bp.y);
        line.setAttribute('stroke', '#334155');
        line.setAttribute('stroke-width', '1');
        line.setAttribute('stroke-dasharray', node.stage === 'eval' ? '' : '3,3');
        line.setAttribute('opacity', '0.5');
        tracks.insertBefore(line, tracks.firstChild);
      }
    }
  }
}
renderNodes();
// Blueprint label rendering
(function() {
  var ns = 'http://www.w3.org/2000/svg';
  var tracks = document.querySelector('svg');
  for (var b = 0; b < data.blueprints.length; b++) {
    var bp = data.blueprints[b];
    var lbl = document.createElementNS(ns, 'text');
    lbl.setAttribute('x', 175);
    lbl.setAttribute('y', bp.y + 4);
    lbl.setAttribute('fill', '#94a3b8');
    lbl.setAttribute('font-size', '10');
    lbl.setAttribute('text-anchor', 'end');
    lbl.setAttribute('font-weight', '500');
    lbl.textContent = bp.name;
    tracks.appendChild(lbl);
  }
})();
// Scrubber interaction
var isDragging = false;
var isPlaying = false;
var playInterval = null;
var sliderThumb = document.getElementById('sliderThumb');
var sliderFill = document.getElementById('sliderFill');
var scrubber = document.getElementById('scrubber');
var timeLabel = document.getElementById('timeLabel');
var playBtn = document.getElementById('playBtn');
var playLabel = document.getElementById('playLabel');
function timeFromX(x) {
  x = Math.max(180, Math.min(1140, x));
  var fraction = (x - 180) / 960;
  var totalMin = fraction * 102; // 23:50 to 01:32 = 102 min
  var startH = 23, startM = 50;
  var mins = startH * 60 + startM + totalMin;
  var h = Math.floor(mins / 60) % 24;
  var m = Math.floor(mins % 60);
  return {h:h, m:m, frac:fraction, x:x};
}
function updateScrubber(x) {
  var t = timeFromX(x);
  scrubber.setAttribute('transform', 'translate(' + (t.x - 180) + ',0)');
  sliderFill.setAttribute('width', t.x - 180);
  sliderThumb.setAttribute('cx', t.x);
  document.getElementById('sliderThumbInner').setAttribute('cx', t.x);
  timeLabel.textContent = (t.h < 10 ? '0' : '') + t.h + ':' + (t.m < 10 ? '0' : '') + t.m;
  if (t.h < 24) timeLabel.textContent = t.h + ':' + (t.m < 10 ? '0' : '') + t.m;
}
sliderThumb.addEventListener('mousedown', function(e) {
  isDragging = true;
  if (isPlaying) togglePlay();
});
document.addEventListener('mousemove', function(e) {
  if (!isDragging) return;
  var svgRect = document.querySelector('svg').getBoundingClientRect();
  var mx = e.clientX - svgRect.left;
  updateScrubber(mx);
});
document.addEventListener('mouseup', function() { isDragging = false; });
function togglePlay() {
  isPlaying = !isPlaying;
  if (isPlaying) {
    playLabel.textContent = 'Pause';
    playBtn.setAttribute('fill', 'url(#pauseGrad)');
    playInterval = setInterval(function() {
      var cx = parseFloat(sliderThumb.getAttribute('cx'));
      if (cx >= 1140) {
        cx = 180;
      } else {
        cx += 2.5;
      }
      updateScrubber(cx);
    }, 80);
  } else {
    playLabel.textContent = 'Play';
    playBtn.setAttribute('fill', 'url(#playGrad)');
    clearInterval(playInterval);
  }
}
playBtn.addEventListener('click', togglePlay);
// Click on background to hide popup
document.querySelector('svg').addEventListener('click', function(e) {
  if (e.target.tagName === 'svg') hidePopup();
});
// Initial render
updateScrubber(180);
]]></script>
</svg>