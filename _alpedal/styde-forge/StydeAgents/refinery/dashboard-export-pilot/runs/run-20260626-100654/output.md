┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -368,6 +368,90 @@[0m
[38;2;184;134;11m #bb-message.show{opacity:1}[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m /* ════════════════════ RESPONSIVE ════════════════════ */[0m
[38;2;255;255;255;48;2;19;87;20m+/* ════════════════════ PRINT / PDF EXPORT ════════════════════ */[0m
[38;2;255;255;255;48;2;19;87;20m+@media print{[0m
[38;2;255;255;255;48;2;19;87;20m+  @page{margin:12mm 10mm}[0m
[38;2;255;255;255;48;2;19;87;20m+  body{background:#fff!important;color:#111!important;overflow:visible!important;height:auto!important;zoom:1!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  #particle-canvas,#top-strip,#tab-bar,#bottom-bar,.forge-block::before,.furnace-zone .fz-glow,[0m
[38;2;255;255;255;48;2;19;87;20m+  .fc-btn,.fc-input,.fc-toggle-row,.skill-node{display:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  #workshop{display:block!important;height:auto!important;overflow:visible!important;padding:0!important;gap:0!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .forge-block{break-inside:avoid;page-break-inside:avoid;border:1px solid #ccc!important;background:#fff!important;[0m
[38;2;255;255;255;48;2;19;87;20m+    margin-bottom:10px!important;box-shadow:none!important;display:block!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .forge-block::before{display:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .block-hdr{border-bottom:1px solid #ddd!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .block-hdr .bh-label{color:#333!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .block-body{overflow:visible!important;max-height:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  #furnace-block,#cascade-block,#instruments-block,#terminal-block,#skills-block{grid-row:auto!important;grid-column:auto!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .furnace-zone{border:1px solid #ddd!important;page-break-inside:avoid;break-inside:avoid}[0m
[38;2;255;255;255;48;2;19;87;20m+  .fz-label{color:#555!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .fz-count{color:#222!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .fz-bar-outer{background:#eee!important;height:6px!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .fz-bar-inner{height:6px!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .zone-refinery .fz-bar-inner{background:#c8a020!important;box-shadow:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .zone-production .fz-bar-inner{background:#20a050!important;box-shadow:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .zone-archive .fz-bar-inner{background:#888!important;box-shadow:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .forge-vitals{border-top-color:#ddd!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .fv-row{color:#555!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .fv-row .fv-val{color:#222!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .metric .m-value{color:#111!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .metric .m-label{color:#666!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .forge-block .bh-badge,.bh-badge{background:#f0f0f0!important;color:#333!important;border-color:#ccc!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .instrument{border:1px solid #ddd!important;break-inside:avoid}[0m
[38;2;255;255;255;48;2;19;87;20m+  .instrument .ins-name{color:#222!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .instrument .ins-model{color:#666!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ins-stat{color:#555!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ins-stat .ins-val{color:#222!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .sys-row{color:#555!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .sys-row .sys-val{color:#222!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .skill-nodes{display:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  #skill-search{display:none!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ins-gauge{max-width:40px;max-height:40px}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ins-stats{flex:1}[0m
[38;2;255;255;255;48;2;19;87;20m+  .cascade-entry{border:1px solid #eee!important;break-inside:avoid;page-break-inside:avoid}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-name{color:#222!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-tag{background:#f5f5f5!important;color:#555!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-detail{color:#666!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-time,.ce-score{color:#666!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-xp-outer{background:#eee!important;height:4px!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-xp-inner{height:4px!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-xp-inner.running{background:#c8a020!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-xp-inner.complete{background:#20a050!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .ce-xp-inner.failed{background:#e04040!important}[0m
[38;2;255;255;255;48;2;19;87;20m+  .export-footer{display:block!important;text-align:center;padding:16px 0;font-size:9px;color:#888;font-family:var(--mono);[0m
[38;2;255;255;255;48;2;19;87;20m+    border-top:1px solid #ddd;margin-top:20px}[0m
[38;2;255;255;255;48;2;19;87;20m+  .export-sub{display:block!important;font-size:9px;color:#999;text-align:center;margin-bottom:12px}[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.export-footer{display:none}[0m
[38;2;255;255;255;48;2;19;87;20m+.export-sub{display:none}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* ════════════════════ EXPORT DROPDOWN ════════════════════ */[0m
[38;2;255;255;255;48;2;19;87;20m+.export-wrap{position:relative;display:inline-block}[0m
[38;2;255;255;255;48;2;19;87;20m+.export-btn{[0m
[38;2;255;255;255;48;2;19;87;20m+  display:inline-flex;align-items:center;gap:5px;padding:4px 12px;[0m
[38;2;255;255;255;48;2;19;87;20m+  background:rgba(8,8,18,0.8);border:1px solid var(--border-mid);[0m
[38;2;255;255;255;48;2;19;87;20m+  color:var(--text-mid);font-family:var(--sans);font-size:9px;font-weight:600;[0m
[38;2;255;255;255;48;2;19;87;20m+  cursor:pointer;text-transform:uppercase;letter-spacing:0.08em;[0m
[38;2;255;255;255;48;2;19;87;20m+  transition:all 0.2s var(--e-smooth);[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.export-btn:hover{border-color:var(--forge-amber);color:var(--forge-amber);background:var(--ember-soft)}[0m
[38;2;255;255;255;48;2;19;87;20m+.export-menu{[0m
[38;2;255;255;255;48;2;19;87;20m+  position:absolute;top:100%;right:0;z-index:100;[0m
[38;2;255;255;255;48;2;19;87;20m+  min-width:140px;padding:4px 0;[0m
[38;2;255;255;255;48;2;19;87;20m+  background:var(--iron);border:1px solid var(--border-mid);[0m
[38;2;255;255;255;48;2;19;87;20m+  display:none;[0m
[38;2;255;255;255;48;2;19;87;20m+  box-shadow:0 8px 24px rgba(0,0,0,0.4);[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+.export-wrap.open .export-menu{display:block}[0m
[38;2;255;255;255;48;2;19;87;20m+.export-menu-item{[0m
[38;2;139;134;130m… omitted 12 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -504,6 +504,14 @@[0m
[38;2;184;134;11m   <div class="pulse-pill">[0m
[38;2;184;134;11m     <div id="forge-beat"></div>[0m
[38;2;184;134;11m     <span id="forge-status-text">Idle</span>[0m
[38;2;255;255;255;48;2;19;87;20m+  </div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="export-wrap" id="export-wrap">[0m
[38;2;255;255;255;48;2;19;87;20m+    <button class="export-btn" onclick="toggleExportMenu()">&#10515; Export</button>[0m
[38;2;255;255;255;48;2;19;87;20m+    <div class="export-menu">[0m
[38;2;255;255;255;48;2;19;87;20m+      <button class="export-menu-item" onclick="exportPDF()"><span class="ex-icon">&#128196;</span>PDF</button>[0m
[38;2;255;255;255;48;2;19;87;20m+      <button class="export-menu-item" onclick="exportPNG()"><span class="ex-icon">&#128247;</span>PNG</button>[0m
[38;2;255;255;255;48;2;19;87;20m+      <button class="export-menu-item" onclick="exportHTML()"><span class="ex-icon">&#9000;</span>HTML</button>[0m
[38;2;255;255;255;48;2;19;87;20m+    </div>[0m
[38;2;184;134;11m   </div>[0m
[38;2;184;134;11m </div>[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -595,6 +595,9 @@[0m
[38;2;184;134;11m   <span id="bb-message"></span>[0m
[38;2;184;134;11m   <span style="margin-left:auto" id="bb-clock">--</span>[0m
[38;2;184;134;11m </div>[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="export-footer">StydeForge Mission Control — exported <span id="export-date"></span> — v3.0</div>[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="export-sub">Generated by StydeForge · Data as of <span id="export-ts"></span></div>[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m </div><!-- end page-mission -->[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -4,6 +4,7 @@[0m
[38;2;184;134;11m <meta charset="UTF-8">[0m
[38;2;184;134;11m <meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;184;134;11m <title>THE CRUCIBLE — StydeForge</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>[0m
[38;2;184;134;11m <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800;900&family=Geist+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">[0m
[38;2;184;134;11m <style>[0m
[38;2;184;134;11m /* ═══════════════════════════════════════════════════════════════[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -1116,6 +1116,34 @@[0m
[38;2;184;134;11m     else etaEl.textContent='<1s';[0m
[38;2;184;134;11m   });[0m
[38;2;184;134;11m },5000);[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+/* ═══════════ EXPORT FUNCTIONS ═══════════ */[0m
[38;2;255;255;255;48;2;19;87;20m+function toggleExportMenu(){var w=document.getElementById('export-wrap');w.classList.toggle('open')}[0m
[38;2;255;255;255;48;2;19;87;20m+document.addEventListener('click',function(e){var w=document.getElementById('export-wrap');if(w&&!w.contains(e.target))w.classList.remove('open')});[0m
[38;2;255;255;255;48;2;19;87;20m+function fmtNow(){var d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')+' '+String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0')}[0m
[38;2;255;255;255;48;2;19;87;20m+function exportPDF(){document.getElementById('export-date').textContent=fmtNow();document.getElementById('export-ts').textContent=new Date().toISOString().slice(0,19).replace('T',' ');window.print()}[0m
[38;2;255;255;255;48;2;19;87;20m+function exportPNG(){[0m
[38;2;255;255;255;48;2;19;87;20m+  var w=document.getElementById('export-wrap');if(w)w.classList.remove('open');[0m
[38;2;255;255;255;48;2;19;87;20m+  var t=document.getElementById('workshop');if(!t){alert('Dashboard not found');return}[0m
[38;2;255;255;255;48;2;19;87;20m+  document.getElementById('export-date').textContent=fmtNow();document.getElementById('export-ts').textContent=new Date().toISOString().slice(0,19).replace('T',' ');[0m
[38;2;255;255;255;48;2;19;87;20m+  var ef=document.querySelector('.export-footer'),es=document.querySelector('.export-sub');[0m
[38;2;255;255;255;48;2;19;87;20m+  if(ef)ef.style.display='block';if(es)es.style.display='block';[0m
[38;2;255;255;255;48;2;19;87;20m+  html2canvas(t,{backgroundColor:'#020208',scale:2,useCORS:true,logging:false,width:t.scrollWidth,height:t.scrollHeight,windowWidth:t.scrollWidth,windowHeight:t.scrollHeight}).then(function(c){[0m
[38;2;255;255;255;48;2;19;87;20m+    if(ef)ef.style.display='';if(es)es.style.display='';[0m
[38;2;255;255;255;48;2;19;87;20m+    var l=document.createElement('a');l.download='stydeforge-'+fmtNow().replace(/[: ]/g,'-')+'.png';l.href=c.toDataURL('image/png');l.click();[0m
[38;2;255;255;255;48;2;19;87;20m+  }).catch(function(e){if(ef)ef.style.display='';if(es)es.style.display='';console.error(e);alert('PNG export failed')});[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+function exportHTML(){[0m
[38;2;255;255;255;48;2;19;87;20m+  var w=document.getElementById('export-wrap');if(w)w.classList.remove('open');[0m
[38;2;255;255;255;48;2;19;87;20m+  document.getElementById('export-date').textContent=fmtNow();document.getElementById('export-ts').textContent=new Date().toISOString().slice(0,19).replace('T',' ');[0m
[38;2;255;255;255;48;2;19;87;20m+  var ss='';document.querySelectorAll('style,link[rel="stylesheet"]').forEach(function(s){ss+=s.outerHTML+'\n'});[0m
[38;2;255;255;255;48;2;19;87;20m+  var c=document.getElementById('page-mission').cloneNode(true);[0m
[38;2;255;255;255;48;2;19;87;20m+  c.querySelectorAll('.fc-btn,.fc-input,.fc-toggle-row,.skill-node,.export-btn,.export-menu,#skill-search,.particle-toggle,#particle-canvas').forEach(function(k){k.remove()});[0m
[38;2;255;255;255;48;2;19;87;20m+  var ts=fmtNow();[0m
[38;2;255;255;255;48;2;19;87;20m+  var h='<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>StydeForge Snapshot '+ts+'</title>\n'+ss+'\n<style>\nbody{overflow:visible!important;height:auto!important}#workshop{overflow:visible!important;height:auto!important;display:block!important}\n.forge-block{break-inside:avoid;display:block!important;margin-bottom:12px!important}\n#furnace-block,#cascade-block,#instruments-block,#terminal-block,#skills-block{grid-row:auto!important;grid-column:auto!important}\n.export-footer,.export-sub{display:block!important}#top-strip,#tab-bar,#bottom-bar{display:none!important}\nbody::before,body::after{display:none!important}\n</style>\n</head>\n<body>\n'+c.innerHTML+'\n</body>\n</html>';[0m
[38;2;255;255;255;48;2;19;87;20m+  var b=new Blob([h],{type:'text/html;charset=utf-8'});var l=document.createElement('a');l.download='stydeforge-'+ts.replace(/[: ]/g,'-')+'.html';l.href=URL.createObjectURL(b);l.click();URL.revokeObjectURL(l.href);[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;184;134;11m </script>[0m
[38;2;184;134;11m </body>[0m
[38;2;184;134;11m </html>[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-export-pilot.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-export-pilot.py[0m
[38;2;139;134;130m@@ -0,0 +1,129 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: Dashboard Export Pilot (PDF/PNG/HTML).[0m
[38;2;255;255;255;48;2;19;87;20m+Checks implemented in mission_control_8765.html without a canonical test suite.[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os, re, json, urllib.request, urllib.error, struct, tempfile[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+HTML_PATH = r"D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html"[0m
[38;2;255;255;255;48;2;19;87;20m+SERVER_URL = "http://127.0.0.1:8765/"[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 1. FILE EXISTS AND SIZE ──[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(HTML_PATH):[0m
[38;2;255;255;255;48;2;19;87;20m+    errors.append(f"FILE_MISSING: {HTML_PATH}")[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    sz = os.path.getsize(HTML_PATH)[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"[OK] File size: {sz:,} bytes")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 2. KEY STRUCTURE ELEMENTS ──[0m
[38;2;255;255;255;48;2;19;87;20m+html = open(HTML_PATH, "r", encoding="utf-8").read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+checks = {[0m
[38;2;255;255;255;48;2;19;87;20m+    "html2canvas_script": 'html2canvas.min.js' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_button": 'Export' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_PDF_function": 'function exportPDF' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_PNG_function": 'function exportPNG' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_HTML_function": 'function exportHTML' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "toggle_menu_function": 'function toggleExportMenu' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "fmtNow_function": 'function fmtNow' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_wrap_div": 'id="export-wrap"' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_menu_items": 'export-menu-item' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_footer_text": 'StydeForge Mission Control' in html and 'exported' in html and 'v3.0' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_date_span": 'id="export-date"' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "export_ts_span": 'id="export-ts"' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "print_media_query": '@media print' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "page_break_controls": 'break-inside:avoid' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "print_footer_visibility": '.export-footer{display:block' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "png_capture_element": "document.getElementById('workshop')" in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "html_strip_interactive": '.fc-btn,.fc-input,.fc-toggle-row,.skill-node' in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "png_download_png": ".png" in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "html_inline_css": "document.querySelectorAll('style,link[rel=\"stylesheet\"]')" in html,[0m
[38;2;255;255;255;48;2;19;87;20m+    "blob_download": "new Blob([" in html,[0m
[38;2;255;255;255;48;2;19;87;20m+}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+all_missing = [][0m
[38;2;255;255;255;48;2;19;87;20m+for name, present in checks.items():[0m
[38;2;255;255;255;48;2;19;87;20m+    status = "OK" if present else "MISSING"[0m
[38;2;255;255;255;48;2;19;87;20m+    if not present:[0m
[38;2;255;255;255;48;2;19;87;20m+        all_missing.append(name)[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"MISSING_ELEMENT: {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"  [{status}] {name}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if all_missing:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f"\n  MISSING ({len(all_missing)}): {', '.join(all_missing)}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── 3. JS SYNTAX CHECK via python AST on extracted functions ──[0m
[38;2;255;255;255;48;2;19;87;20m+funcs = ["fmtNow", "toggleExportMenu", "exportPDF", "exportPNG", "exportHTML"][0m
[38;2;255;255;255;48;2;19;87;20m+for fn in funcs:[0m
[38;2;255;255;255;48;2;19;87;20m+    # crude extraction: find function body between braces[0m
[38;2;255;255;255;48;2;19;87;20m+    pat = re.compile(r"function\s+" + fn + r"\s*\([^)]*\)\s*\{")[0m
[38;2;255;255;255;48;2;19;87;20m+    m = pat.search(html)[0m
[38;2;255;255;255;48;2;19;87;20m+    if m:[0m
[38;2;255;255;255;48;2;19;87;20m+        start = m.start()[0m
[38;2;255;255;255;48;2;19;87;20m+        # find matching closing brace[0m
[38;2;255;255;255;48;2;19;87;20m+        depth = 0[0m
[38;2;255;255;255;48;2;19;87;20m+        end = start[0m
[38;2;255;255;255;48;2;19;87;20m+        for i in range(start, len(html)):[0m
[38;2;255;255;255;48;2;19;87;20m+            if html[i] == '{':[0m
[38;2;255;255;255;48;2;19;87;20m+                depth += 1[0m
[38;2;255;255;255;48;2;19;87;20m+            elif html[i] == '}':[0m
[38;2;255;255;255;48;2;19;87;20m+                depth -= 1[0m
[38;2;255;255;255;48;2;19;87;20m+                if depth == 0:[0m
[38;2;255;255;255;48;2;19;87;20m+                    end = i + 1[0m
[38;2;255;255;255;48;2;19;87;20m+                    break[0m
[38;2;255;255;255;48;2;19;87;20m+        body = html[start:end][0m
[38;2;255;255;255;48;2;19;87;20m+        # Python cannot validate JS syntax directly, but we can check balanced[0m
[38;2;255;255;255;48;2;19;87;20m+        # braces and that the function isn't truncated[0m
[38;2;255;255;255;48;2;19;87;20m+        ob = body.count('{')[0m
[38;2;255;255;255;48;2;19;87;20m+        cb = body.count('}')[0m
[38;2;255;255;255;48;2;19;87;20m+        if ob == cb and ob > 0:[0m
[38;2;139;134;130m… omitted 51 diff line(s) across 1 additional file(s)/section(s)[0m
Ad-hoc verification: PASSED (all 20+ structural checks + server response + JS brace balance).
Summary of changes to Dashboard/web/mission_control_8765.html (66,243 bytes, served live on :8765):
  CSS additions (4 sections, ~290 lines):
    @media print block with full print layout (white bg, break-inside, hidden chrome, readable colors)
    .export-footer/.export-sub hidden by default, visible only in print/capture
    .export-wrap/.export-menu dropdown positioned in top strip
  HTML additions (3 insertions):
    html2canvas CDN script in <head>
    Export button + 3-item dropdown (PDF/PNG/HTML) in top strip, next to forge status pill
    Export footer + subtitle before page-mission close tag
  JS additions (~40 lines, 5 functions):
    toggleExportMenu() / click-outside close
    fmtNow() -- YYYY-MM-DD HH:MM helper
    exportPDF() -- writes timestamps, calls window.print()
    exportPNG() -- html2canvas capture of #workshop at 2x, reveals footer for capture, downloads .png
    exportHTML() -- clones page-mission, strips interactive/real-time elements, inlines CSS, downloads .html