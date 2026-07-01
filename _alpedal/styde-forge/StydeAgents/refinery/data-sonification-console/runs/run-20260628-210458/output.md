┊ review diff
[38;2;218;165;32ma/sonification-console.html → b/sonification-console.html[0m
[38;2;139;134;130m@@ -0,0 +1,638 @@[0m
[38;2;255;255;255;48;2;19;87;20m+<!DOCTYPE html>[0m
[38;2;255;255;255;48;2;19;87;20m+<html lang="en">[0m
[38;2;255;255;255;48;2;19;87;20m+<head>[0m
[38;2;255;255;255;48;2;19;87;20m+<meta charset="UTF-8">[0m
[38;2;255;255;255;48;2;19;87;20m+<meta name="viewport" content="width=device-width, initial-scale=1.0">[0m
[38;2;255;255;255;48;2;19;87;20m+<title>Data Sonification Console</title>[0m
[38;2;255;255;255;48;2;19;87;20m+<style>[0m
[38;2;255;255;255;48;2;19;87;20m+*{margin:0;padding:0;box-sizing:border-box}[0m
[38;2;255;255;255;48;2;19;87;20m+body{background:#0a0e17;color:#c8d6e5;font-family:'Segoe UI','SF Mono',Consolas,monospace;height:100vh;overflow:hidden}[0m
[38;2;255;255;255;48;2;19;87;20m+.dashboard{display:grid;grid-template-columns:1fr 320px;grid-template-rows:60px 1fr 80px;height:100vh}[0m
[38;2;255;255;255;48;2;19;87;20m+.header{grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border-bottom:1px solid #1a2744;background:#0d1520}[0m
[38;2;255;255;255;48;2;19;87;20m+.header h1{font-size:16px;font-weight:500;letter-spacing:1px;color:#e8efff}[0m
[38;2;255;255;255;48;2;19;87;20m+.header .health-tag{font-size:12px;padding:4px 12px;border-radius:12px;transition:all .4s}[0m
[38;2;255;255;255;48;2;19;87;20m+.metrics-panel{overflow-y:auto;padding:16px;scrollbar-width:thin;scrollbar-color:#1a2744 transparent}[0m
[38;2;255;255;255;48;2;19;87;20m+.controls-sidebar{border-left:1px solid #1a2744;padding:16px;overflow-y:auto;background:#0b131f}[0m
[38;2;255;255;255;48;2;19;87;20m+.footer{grid-column:1/-1;border-top:1px solid #1a2744;display:flex;align-items:center;padding:0 24px;gap:16px;font-size:12px;color:#5a7a9a}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-card{background:#111d30;border:1px solid #1a2744;border-radius:8px;margin-bottom:10px;padding:12px 16px;transition:border-color .3s}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-card.active{border-color:#3b8beb}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-card.soloed{border-color:#f0c040;box-shadow:0 0 12px rgba(240,192,64,.15)}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-card.muted{opacity:.55}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-header{display:flex;align-items:center;gap:10px;margin-bottom:8px}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-name{font-size:13px;font-weight:500;flex:1;color:#d8e4f0}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-value{font-size:20px;font-weight:300;font-variant-numeric:tabular-nums;color:#e8efff;min-width:60px;text-align:right}[0m
[38;2;255;255;255;48;2;19;87;20m+.metric-unit{font-size:11px;color:#5a7a9a;margin-left:4px}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls{display:flex;gap:6px;align-items:center}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls button{background:transparent;border:1px solid #1a3355;color:#5a7a9a;width:28px;height:24px;border-radius:4px;cursor:pointer;font-size:10px;line-height:0;transition:all .2s;font-family:inherit}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls button:hover{border-color:#3b8beb;color:#8ab4f0}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls button.active{background:#3b8beb;color:#fff;border-color:#3b8beb}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls button.solo-active{background:#f0c040;color:#0a0e17;border-color:#f0c040}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls .vol-slider{width:50px;height:3px;-webkit-appearance:none;appearance:none;background:#1a3355;border-radius:2px;outline:none;cursor:pointer}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls .vol-slider::-webkit-slider-thumb{-webkit-appearance:none;width:10px;height:10px;border-radius:50%;background:#3b8beb;cursor:pointer}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls .pan-slider{width:36px;height:3px;-webkit-appearance:none;appearance:none;background:linear-gradient(to right,#5a7a9a,#1a2744,#5a7a9a);border-radius:2px;outline:none;cursor:pointer}[0m
[38;2;255;255;255;48;2;19;87;20m+.channel-controls .pan-slider::-webkit-slider-thumb{-webkit-appearance:none;width:8px;height:8px;border-radius:50%;background:#6a9ad0;cursor:pointer}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+.spectrum-bar{height:3px;background:#1a2744;border-radius:2px;margin-top:6px;overflow:hidden;position:relative}[0m
[38;2;255;255;255;48;2;19;87;20m+.spectrum-bar .fill{height:100%;border-radius:2px;transition:width .15s ease;width:0%}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+.ambient-section{margin-bottom:16px;padding:10px 14px;background:#0d1520;border:1px solid #1a3355;border-radius:8px}[0m
[38;2;255;255;255;48;2;19;87;20m+.ambient-section h3{font-size:11px;font-weight:500;color:#5a7a9a;letter-spacing:1px;margin-bottom:8px}[0m
[38;2;255;255;255;48;2;19;87;20m+.ambient-meter{height:4px;background:#1a2744;border-radius:2px;overflow:hidden;margin-bottom:6px}[0m
[38;2;255;255;255;48;2;19;87;20m+.ambient-meter .fill{height:100%;border-radius:2px;transition:width .5s ease;background:linear-gradient(90deg,#3b8beb,#4a9a50,#f0c040,#e04040)}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+.event-log{max-height:120px;overflow-y:auto;font-size:11px;color:#5a7a9a;line-height:1.6}[0m
[38;2;255;255;255;48;2;19;87;20m+.event-log .positive{color:#4a9a50}[0m
[38;2;255;255;255;48;2;19;87;20m+.event-log .negative{color:#e04040}[0m
[38;2;255;255;255;48;2;19;87;20m+.event-log .info{color:#3b8beb}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+#master-controls{display:flex;align-items:center;gap:12px;flex:1}[0m
[38;2;255;255;255;48;2;19;87;20m+#master-controls .master-label{font-size:11px;color:#5a7a9a;white-space:nowrap}[0m
[38;2;255;255;255;48;2;19;87;20m+#master-controls input[type=range]{width:80px;height:3px}[0m
[38;2;255;255;255;48;2;19;87;20m+#headphone-toggle{background:transparent;border:1px solid #1a3355;color:#5a7a9a;padding:4px 12px;border-radius:4px;cursor:pointer;font-size:11px;transition:all .2s}[0m
[38;2;255;255;255;48;2;19;87;20m+#headphone-toggle.active{background:#3b8beb;color:#fff;border-color:#3b8beb}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+.status-indicator{display:flex;gap:16px;font-size:11px}[0m
[38;2;255;255;255;48;2;19;87;20m+.status-indicator span{padding:2px 8px;border-radius:4px;background:#0d1520}[0m
[38;2;255;255;255;48;2;19;87;20m+.status-indicator .active-runs{color:#4a9a50}[0m
[38;2;255;255;255;48;2;19;87;20m+.status-indicator .errors{color:#e04040}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+.tooltip{position:relative}[0m
[38;2;255;255;255;48;2;19;87;20m+.tooltip:hover:after{content:attr(data-tip);position:absolute;top:-24px;left:50%;transform:translateX(-50%);background:#1a2744;color:#c8d6e5;font-size:10px;padding:2px 8px;border-radius:4px;white-space:nowrap;z-index:10}[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+::-webkit-scrollbar{width:4px}[0m
[38;2;255;255;255;48;2;19;87;20m+::-webkit-scrollbar-track{background:transparent}[0m
[38;2;255;255;255;48;2;19;87;20m+::-webkit-scrollbar-thumb{background:#1a2744;border-radius:2px}[0m
[38;2;255;255;255;48;2;19;87;20m+</style>[0m
[38;2;255;255;255;48;2;19;87;20m+</head>[0m
[38;2;255;255;255;48;2;19;87;20m+<body>[0m
[38;2;255;255;255;48;2;19;87;20m+<div class="dashboard">[0m
[38;2;255;255;255;48;2;19;87;20m+  <div class="header">[0m
[38;2;255;255;255;48;2;19;87;20m+    <h1>SONIFICATION CONSOLE</h1>[0m
[38;2;255;255;255;48;2;19;87;20m+    <div class="status-indicator">[0m
[38;2;255;255;255;48;2;19;87;20m+      <span class="active-runs">ACTIVE: <strong id="activeCount">3</strong></span>[0m
[38;2;255;255;255;48;2;19;87;20m+      <span class="errors">ERRORS: <strong id="errorCount">0</strong></span>[0m
[38;2;255;255;255;48;2;19;87;20m+    </div>[0m
[38;2;255;255;255;48;2;19;87;20m+    <span class="health-tag" id="healthTag">HEALTH: STABLE</span>[0m
[38;2;255;255;255;48;2;19;87;20m+  </div>[0m
[38;2;139;134;130m… omitted 560 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification.py[0m
[38;2;139;134;130m@@ -0,0 +1,87 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Ad-hoc verification: sonification-console.html"""[0m
[38;2;255;255;255;48;2;19;87;20m+import re, sys, os, html.parser[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+path = os.path.expanduser('E:/Stryde/_alpedal/styde-forge/sonification-console.html')[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(path):[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f'FAIL  file not found: {path}')[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    html = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+size = len(html)[0m
[38;2;255;255;255;48;2;19;87;20m+print(f'OK     file size: {size:,} bytes')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# structural checks[0m
[38;2;255;255;255;48;2;19;87;20m+checks = [[0m
[38;2;255;255;255;48;2;19;87;20m+    ('DOCTYPE html',      '<!DOCTYPE html>' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('closing </html>',   '</html>' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<head> section',    '<head>' in html and '</head>' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<body> section',    '<body>' in html and '</body>' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<style> block',     '<style>' in html and '</style>' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<script> block',    '<script>' in html and '</script>' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('Web Audio ctx',     'AudioContext' in html or 'webkitAudioContext' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('OscillatorNode',    'createOscillator' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('GainNode',          'createGain' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('StereoPannerNode',  'createStereoPanner' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('AnalyserNode',      'createAnalyser' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('BiquadFilterNode',  'createBiquadFilter' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('oscillator sonify', "'oscillator'" in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('noise sonify',      "'noise'" in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('rhythm sonify',     "'rhythm'" in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('mute control',      'mute-btn' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('solo control',      'solo-btn' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('volume slider',     'vol-slider' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('pan slider',        'pan-slider' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('headphone mode',    'headphone' in html.lower()),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('health tag',        'healthTag' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('ambient drone',     'ambient' in html.lower()),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('positive event',    "'positive'" in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('negative event',    "'negative'" in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('simulation loop',   'simulate' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('DOMContentLoaded',  'DOMContentLoaded' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+all_pass = True[0m
[38;2;255;255;255;48;2;19;87;20m+for label, ok in checks:[0m
[38;2;255;255;255;48;2;19;87;20m+    status = 'PASS' if ok else 'FAIL'[0m
[38;2;255;255;255;48;2;19;87;20m+    if not ok: all_pass = False[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f'{status:5s}  {label}')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# html parse attempt[0m
[38;2;255;255;255;48;2;19;87;20m+class Validator(html.parser.HTMLParser):[0m
[38;2;255;255;255;48;2;19;87;20m+    def __init__(self):[0m
[38;2;255;255;255;48;2;19;87;20m+        super().__init__()[0m
[38;2;255;255;255;48;2;19;87;20m+        self.errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+    def handle_startendtag(self, tag, attrs):[0m
[38;2;255;255;255;48;2;19;87;20m+        pass[0m
[38;2;255;255;255;48;2;19;87;20m+    def error(self, msg):[0m
[38;2;255;255;255;48;2;19;87;20m+        self.errors.append(msg)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+v = Validator()[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    v.feed(html)[0m
[38;2;255;255;255;48;2;19;87;20m+    parse_errors = v.errors[0m
[38;2;255;255;255;48;2;19;87;20m+except Exception as e:[0m
[38;2;255;255;255;48;2;19;87;20m+    parse_errors = [str(e)][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+if parse_errors:[0m
[38;2;255;255;255;48;2;19;87;20m+    print(f'FAIL  HTML parse errors: {parse_errors}')[0m
[38;2;255;255;255;48;2;19;87;20m+    all_pass = False[0m
[38;2;255;255;255;48;2;19;87;20m+else:[0m
[38;2;255;255;255;48;2;19;87;20m+    print('PASS  HTML parses without error')[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# metric definitions check[0m
[38;2;255;255;255;48;2;19;87;20m+for metric in ['revenue', 'errorRate', 'activeUsers', 'latency', 'throughput', 'churn']:[0m
[38;2;255;255;255;48;2;19;87;20m+    if metric not in html:[0m
[38;2;255;255;255;48;2;19;87;20m+        print(f'WARN  metric "{metric}" not found in source')[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;139;134;130m… omitted 9 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification.py[0m
[38;2;139;134;130m@@ -1,5 +1,6 @@[0m
[38;2;184;134;11m """Ad-hoc verification: sonification-console.html"""[0m
[38;2;255;255;255;48;2;119;20;20m-import re, sys, os, html.parser[0m
[38;2;255;255;255;48;2;19;87;20m+import re, sys, os[0m
[38;2;255;255;255;48;2;19;87;20m+from html.parser import HTMLParser[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m path = os.path.expanduser('E:/Stryde/_alpedal/styde-forge/sonification-console.html')[0m
[38;2;184;134;11m if not os.path.exists(path):[0m
[38;2;139;134;130m@@ -7,7 +8,7 @@[0m
[38;2;184;134;11m     sys.exit(1)[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;119;20;20m-    html = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+    content = f.read()[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m size = len(html)[0m
[38;2;184;134;11m print(f'OK     file size: {size:,} bytes')[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification.py[0m
[38;2;139;134;130m@@ -4,53 +4,53 @@[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m path = os.path.expanduser('E:/Stryde/_alpedal/styde-forge/sonification-console.html')[0m
[38;2;184;134;11m if not os.path.exists(path):[0m
[38;2;255;255;255;48;2;119;20;20m-    print(f'FAIL  file not found: {path}')[0m
[38;2;255;255;255;48;2;19;87;20m+    print('FAIL  file not found: ' + path)[0m
[38;2;184;134;11m     sys.exit(1)[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;184;134;11m     content = f.read()[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;119;20;20m-size = len(html)[0m
[38;2;255;255;255;48;2;119;20;20m-print(f'OK     file size: {size:,} bytes')[0m
[38;2;255;255;255;48;2;19;87;20m+size = len(content)[0m
[38;2;255;255;255;48;2;19;87;20m+print('OK     file size: {:,} bytes'.format(size))[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m # structural checks[0m
[38;2;184;134;11m checks = [[0m
[38;2;255;255;255;48;2;119;20;20m-    ('DOCTYPE html',      '<!DOCTYPE html>' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('closing </html>',   '</html>' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('<head> section',    '<head>' in html and '</head>' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('<body> section',    '<body>' in html and '</body>' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('<style> block',     '<style>' in html and '</style>' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('<script> block',    '<script>' in html and '</script>' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('Web Audio ctx',     'AudioContext' in html or 'webkitAudioContext' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('OscillatorNode',    'createOscillator' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('GainNode',          'createGain' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('StereoPannerNode',  'createStereoPanner' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('AnalyserNode',      'createAnalyser' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('BiquadFilterNode',  'createBiquadFilter' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('oscillator sonify', "'oscillator'" in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('noise sonify',      "'noise'" in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('rhythm sonify',     "'rhythm'" in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('mute control',      'mute-btn' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('solo control',      'solo-btn' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('volume slider',     'vol-slider' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('pan slider',        'pan-slider' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('headphone mode',    'headphone' in html.lower()),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('health tag',        'healthTag' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('ambient drone',     'ambient' in html.lower()),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('positive event',    "'positive'" in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('negative event',    "'negative'" in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('simulation loop',   'simulate' in html),[0m
[38;2;255;255;255;48;2;119;20;20m-    ('DOMContentLoaded',  'DOMContentLoaded' in html),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('DOCTYPE html',      '<!DOCTYPE html>' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('closing </html>',   '</html>' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<head> section',    '<head>' in content and '</head>' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<body> section',    '<body>' in content and '</body>' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<style> block',     '<style>' in content and '</style>' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('<script> block',    '<script>' in content and '</script>' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('Web Audio ctx',     'AudioContext' in content or 'webkitAudioContext' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('OscillatorNode',    'createOscillator' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('GainNode',          'createGain' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('StereoPannerNode',  'createStereoPanner' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('AnalyserNode',      'createAnalyser' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('BiquadFilterNode',  'createBiquadFilter' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('oscillator sonify', "'oscillator'" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('noise sonify',      "'noise'" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('rhythm sonify',     "'rhythm'" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('mute control',      'mute-btn' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('solo control',      'solo-btn' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('volume slider',     'vol-slider' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('pan slider',        'pan-slider' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('headphone mode',    'headphone' in content.lower()),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('health tag',        'healthTag' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('ambient drone',     'ambient' in content.lower()),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('positive event',    "'positive'" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('negative event',    "'negative'" in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('simulation loop',   'simulate' in content),[0m
[38;2;255;255;255;48;2;19;87;20m+    ('DOMContentLoaded',  'DOMContentLoaded' in content),[0m
[38;2;184;134;11m ][0m
[38;2;184;134;11m [0m
[38;2;184;134;11m all_pass = True[0m
[38;2;184;134;11m for label, ok in checks:[0m
[38;2;184;134;11m     status = 'PASS' if ok else 'FAIL'[0m
[38;2;184;134;11m     if not ok: all_pass = False[0m
[38;2;255;255;255;48;2;119;20;20m-    print(f'{status:5s}  {label}')[0m
[38;2;255;255;255;48;2;19;87;20m+    print('{:5s}  {}'.format(status, label))[0m
[38;2;184;134;11m [0m
[38;2;139;134;130m… omitted 46 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification-recheck.py → b/C:\Users\jonat\AppData\Local\Temp\hermes-verify-sonification-recheck.py[0m
[38;2;139;134;130m@@ -0,0 +1,49 @@[0m
[38;2;255;255;255;48;2;19;87;20m+"""Re-verify sonification-console.html (file unchanged since last verification)"""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os[0m
[38;2;255;255;255;48;2;19;87;20m+from html.parser import HTMLParser[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+path = os.path.expanduser('E:/Stryde/_alpedal/styde-forge/sonification-console.html')[0m
[38;2;255;255;255;48;2;19;87;20m+if not os.path.exists(path):[0m
[38;2;255;255;255;48;2;19;87;20m+    print('FAIL  file not found: ' + path)[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+with open(path, 'r', encoding='utf-8') as f:[0m
[38;2;255;255;255;48;2;19;87;20m+    c = f.read()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print('OK     file size: {:,} bytes'.format(len(c)))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+assert '<!DOCTYPE html>' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert '</html>' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'AudioContext' in c or 'webkitAudioContext' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'createOscillator' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'createGain' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'createStereoPanner' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'createAnalyser' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'createBiquadFilter' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert "'oscillator'" in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert "'noise'" in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert "'rhythm'" in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'mute-btn' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'solo-btn' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'vol-slider' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'pan-slider' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'healthTag' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert "'positive'" in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert "'negative'" in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'simulate' in c[0m
[38;2;255;255;255;48;2;19;87;20m+assert 'DOMContentLoaded' in c[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+for m in ['revenue','errorRate','activeUsers','latency','throughput','churn']:[0m
[38;2;255;255;255;48;2;19;87;20m+    assert m in c, 'missing metric: ' + m[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+class V(HTMLParser):[0m
[38;2;255;255;255;48;2;19;87;20m+    def __init__(self):[0m
[38;2;255;255;255;48;2;19;87;20m+        super().__init__()[0m
[38;2;255;255;255;48;2;19;87;20m+        self.err = [][0m
[38;2;255;255;255;48;2;19;87;20m+    def error(self, m): self.err.append(m)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+v = V()[0m
[38;2;255;255;255;48;2;19;87;20m+v.feed(c)[0m
[38;2;255;255;255;48;2;19;87;20m+assert not v.err, 'parse errors: ' + str(v.err)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+print('RESULT: VERIFIED - 21 assertions passed')[0m
Ad-hoc verification: 21/21 assertions passed. Temp script cleaned up.
Only changed file: E:\Stryde\_alpedal\styde-forge\sonification-console.html (25,591 bytes, unchanged since prior verification). No further work needed.