export-dashboard.js:
const EXPORT_FOOTER_TEMPLATE = (date) =>
  `StydeForge Mission Control — exported ${date.toISOString().slice(0, 16).replace('T', ' ')} — v3.0`;
const EXPORT_BTN = document.createElement('div');
EXPORT_BTN.className = 'dashboard-export-btn';
EXPORT_BTN.innerHTML = `
  <button class="forge-btn forge-btn--icon" title="Export dashboard" data-export-trigger>
    <svg width="16" height="16" viewBox="0 0 16 16"><path d="M8 1L5 5h2v5h2V5h2L8 1zM2 12v2h12v-2H2z" fill="currentColor"/></svg>
  </button>
  <div class="export-menu" hidden>
    <button data-export="pdf">Export PDF</button>
    <button data-export="png">Export PNG</button>
    <button data-export="html">Export HTML</button>
  </div>
`;
document.querySelector('.dashboard-toolbar')?.appendChild(EXPORT_BTN);
const TOGGLE = EXPORT_BTN.querySelector('[data-export-trigger]');
const MENU = EXPORT_BTN.querySelector('.export-menu');
TOGGLE.addEventListener('click', () => { MENU.hidden = !MENU.hidden; });
document.addEventListener('click', (e) => {
  if (!EXPORT_BTN.contains(e.target)) MENU.hidden = true;
});
MENU.addEventListener('click', async (e) => {
  const fmt = e.target.dataset.export;
  if (!fmt) return;
  MENU.hidden = true;
  if (fmt === 'pdf') await exportPdf();
  else if (fmt === 'png') await exportPng();
  else if (fmt === 'html') await exportHtml();
});
async function exportPdf() {
  const footerText = EXPORT_FOOTER_TEMPLATE(new Date());
  const style = document.createElement('style');
  style.textContent = `
    @media print {
      @page { margin: 15mm; }
      body { font-size: 11pt; }
      .dashboard-grid { break-inside: avoid; }
      .dashboard-card { break-inside: avoid; page-break-inside: avoid; }
      .forge-btn, .dashboard-toolbar, .export-menu,
      [data-export-trigger], .live-indicator, .sse-status { display: none !important; }
      .dashboard-footer { display: block !important; }
      body::after {
        content: "${footerText}";
        position: fixed; bottom: 10mm; left: 15mm; right: 15mm;
        font-size: 8pt; color: #666; text-align: center;
      }
    }
  `;
  document.head.appendChild(style);
  window.print();
  setTimeout(() => style.remove(), 1000);
}
async function exportPng() {
  const el = document.querySelector('.dashboard-grid') || document.querySelector('.dashboard');
  if (!el) return;
  const script = document.createElement('script');
  script.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
  await new Promise((ok, fail) => { script.onload = ok; script.onerror = fail; document.head.appendChild(script); });
  const canvas = await html2canvas(el, {
    backgroundColor: '#fff',
    scale: 2,
    useCORS: true,
    logging: false,
    onclone: (doc) => {
      const footer = doc.createElement('div');
      footer.textContent = EXPORT_FOOTER_TEMPLATE(new Date());
      footer.style.cssText = 'text-align:center;padding:8px;font-size:10px;color:#666;';
      el.appendChild(footer);
    }
  });
  const link = document.createElement('a');
  link.download = `dashboard-${new Date().toISOString().slice(0,10)}.png`;
  link.href = canvas.toDataURL('image/png');
  link.click();
}
async function exportHtml() {
  const footerText = EXPORT_FOOTER_TEMPLATE(new Date());
  const clone = document.querySelector('.dashboard')?.cloneNode(true) || document.querySelector('.dashboard-grid')?.cloneNode(true);
  if (!clone) return;
  const liveSelectors = clone.querySelectorAll(
    '[class*="sse"], [class*="live"], [class*="realtime"], ' +
    '.dashboard-export-btn, .forge-btn, [data-export-trigger], ' +
    '.export-menu, .sse-indicator, .ws-status'
  );
  liveSelectors.forEach(el => el.remove());
  const inline = document.createElement('style');
  inline.textContent = Array.from(document.styleSheets)
    .map(s => { try { return Array.from(s.cssRules).map(r => r.cssText).join('\n'); } catch(e) { return ''; }})
    .join('\n');
  const footer = document.createElement('div');
  footer.style.cssText = 'text-align:center;padding:12px;font-size:10px;color:#666;border-top:1px solid #ddd;margin-top:16px;';
  footer.textContent = footerText;
  clone.appendChild(footer);
  const blob = new Blob([
    '<!DOCTYPE html><html><head><meta charset="utf-8">',
    '<title>StydeForge Dashboard Export</title>',
    inline.outerHTML,
    '</head><body>',
    clone.outerHTML,
    '</body></html>'
  ], { type: 'text/html' });
  const link = document.createElement('a');
  link.download = `dashboard-${new Date().toISOString().slice(0,10)}.html`;
  link.href = URL.createObjectURL(blob);
  link.click();
  URL.revokeObjectURL(link.href);
}
export-dashboard.css:
.dashboard-export-btn { position: relative; display: inline-flex; align-items: center; }
.export-menu {
  position: absolute; top: 100%; right: 0; z-index: 1000;
  background: #fff; border: 1px solid #d0d5dd; border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1); min-width: 140px; padding: 4px 0;
}
.export-menu button {
  display: block; width: 100%; text-align: left; padding: 8px 14px;
  border: none; background: none; cursor: pointer; font-size: 13px; color: #1d2939;
}
.export-menu button:hover { background: #f2f4f7; }
@media print {
  .dashboard-export-btn { display: none !important; }
  .dashboard-footer { display: block !important; }
}
dashboard-footer — add to dashboard.html or app mount:
<div class="dashboard-footer" style="display:none;text-align:center;padding:8px 16px;font-size:10px;color:#98a2b3;border-top:1px solid #eaecf0;margin-top:24px;">
  StydeForge Mission Control — exported <span data-export-date></span> — v3.0
</div>
integrate:
load export-dashboard.js after dashboard mounts.
link export-dashboard.css in main stylesheet.
footer div present DOM but hidden by default (display:none); print CSS overrides to block.
html2canvas loads from CDN on demand for PNG export — no build dependency.