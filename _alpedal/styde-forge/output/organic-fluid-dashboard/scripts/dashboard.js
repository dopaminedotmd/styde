(function() {
  'use strict';

  // animate stat counters
  const counters = document.querySelectorAll('.card-stat-value');
  counters.forEach(function(el) {
    const target = parseFloat(el.getAttribute('data-target'));
    const duration = 1200;
    const start = performance.now();
    function tick(now) {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = target < 100 ? eased.toFixed(1) : Math.round(eased * target);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });

  // clock
  const timeEl = document.getElementById('topbarTime');
  function updateClock() {
    const d = new Date();
    timeEl.textContent = d.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
  }
  updateClock();
  setInterval(updateClock, 10000);

  // sparklines (3 mini charts)
  const sparkData = [
    [4, 7, 3, 9, 6, 8, 5, 10, 7, 9],
    [6, 8, 7, 9, 5, 7, 8, 6, 9, 7],
    [9, 8, 7, 8, 9, 8, 9, 8, 7, 9]
  ];
  const sparkColors = ['var(--c-accent)', 'var(--c-green)', 'var(--c-blue)'];

  sparkData.forEach(function(data, idx) {
    const container = document.getElementById('spark' + (idx + 1));
    if (!container) return;
    const w = container.clientWidth || 60;
    const h = container.clientHeight || 30;
    const max = Math.max.apply(null, data);
    const min = Math.min.apply(null, data);
    const range = max - min || 1;
    const pts = data.map(function(v, i) {
      const x = (i / (data.length - 1)) * w;
      const y = h - ((v - min) / range) * (h - 4) - 2;
      return x + ',' + y;
    }).join(' ');
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('width', w);
    svg.setAttribute('height', h);
    const polyline = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    polyline.setAttribute('points', pts);
    polyline.setAttribute('fill', 'none');
    polyline.setAttribute('stroke', sparkColors[idx]);
    polyline.setAttribute('stroke-width', '1.5');
    polyline.setAttribute('stroke-linecap', 'round');
    polyline.setAttribute('stroke-linejoin', 'round');
    svg.appendChild(polyline);
    container.appendChild(svg);
  });

  // main chart (throughput curve)
  const mainCanvas = document.getElementById('mainChart');
  if (mainCanvas) {
    const ctx = mainCanvas.getContext('2d');
    const W = mainCanvas.width, H = mainCanvas.height;
    function drawMain() {
      ctx.clearRect(0, 0, W, H);
      const gradient = ctx.createLinearGradient(0, 0, W, 0);
      gradient.addColorStop(0, 'var(--c-accent-glow)');
      gradient.addColorStop(0.5, 'var(--c-blue)');
      gradient.addColorStop(1, 'var(--c-green)');
      ctx.strokeStyle = gradient;
      ctx.lineWidth = 2.5;
      ctx.lineJoin = 'round';
      ctx.beginPath();
      const n = 40;
      const t = Date.now() / 4000;
      for (let i = 0; i <= n; i++) {
        const x = (i / n) * W;
        const base = (i / n) * 0.8 + 0.1;
        const wave = Math.sin(i * 0.25 + t) * 0.12;
        const wave2 = Math.sin(i * 0.1 + t * 0.7) * 0.08;
        const y = H - (base + wave + wave2) * H * 0.8 - H * 0.05;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      ctx.fillStyle = 'var(--c-accent)';
      ctx.beginPath();
      ctx.arc(W, H - ((1 * 0.8 + 0.1) + Math.sin(n * 0.25 + t) * 0.12 + Math.sin(n * 0.1 + t * 0.7) * 0.08) * H * 0.8 - H * 0.05, 4, 0, Math.PI * 2);
      ctx.fill();
      requestAnimationFrame(drawMain);
    }
    drawMain();
  }

  // distribution chart (donut)
  const distCanvas = document.getElementById('distChart');
  if (distCanvas) {
    const dctx = distCanvas.getContext('2d');
    const DW = distCanvas.width, DH = distCanvas.height;
    const cx = DW / 2, cy = DH / 2, outerR = DW * 0.38, innerR = outerR * 0.55;
    const segments = [
      { label: 'API', value: 45, color: '#d4846a' },
      { label: 'Web', value: 30, color: '#7bb88a' },
      { label: 'DB',  value: 18, color: '#7ba8c4' },
      { label: 'Cache', value: 7, color: '#e8c9b8' }
    ];
    const total = segments.reduce(function(s, seg) { return s + seg.value; }, 0);
    const startAngle = -Math.PI / 2;
    function drawDonut(animP) {
      dctx.clearRect(0, 0, DW, DH);
      let currentAngle = startAngle;
      segments.forEach(function(seg) {
        const sweep = (seg.value / total) * Math.PI * 2 * animP;
        dctx.beginPath();
        dctx.arc(cx, cy, outerR, currentAngle, currentAngle + sweep);
        dctx.arc(cx, cy, innerR, currentAngle + sweep, currentAngle, true);
        dctx.closePath();
        dctx.fillStyle = seg.color;
        dctx.fill();
        currentAngle += sweep;
      });
      if (animP < 1) requestAnimationFrame(function() { drawDonut(Math.min(animP + 0.04, 1)); });
    }
    drawDonut(0);
  }
})();
