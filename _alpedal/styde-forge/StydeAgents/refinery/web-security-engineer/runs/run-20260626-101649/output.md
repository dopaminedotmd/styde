┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py → b/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py[0m
[38;2;139;134;130m@@ -1,10 +1,13 @@[0m
[38;2;184;134;11m """[0m
[38;2;255;255;255;48;2;119;20;20m-Forge Mission Control v6 - Production-Grade Dashboard Server[0m
[38;2;255;255;255;48;2;19;87;20m+"""Forge Mission Control v6 - Production-Grade Dashboard Server[0m
[38;2;184;134;11m Port 8765. Serves HTML + JSON API with cached state, forge controls,[0m
[38;2;184;134;11m skill detail, activity feed, hardware telemetry, gzip compression,[0m
[38;2;184;134;11m and health endpoint.[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Security: CSP, CORS (locked), CSRF tokens, security headers,[0m
[38;2;255;255;255;48;2;19;87;20m+body size limiting, input validation. OWASP-aligned.[0m
[38;2;184;134;11m """[0m
[38;2;255;255;255;48;2;119;20;20m-import json, os, sys, time, subprocess, threading, gzip, io[0m
[38;2;255;255;255;48;2;19;87;20m+import json, os, sys, time, subprocess, threading, gzip, io, hmac, hashlib, secrets[0m
[38;2;184;134;11m from pathlib import Path[0m
[38;2;184;134;11m from http.server import HTTPServer, BaseHTTPRequestHandler[0m
[38;2;184;134;11m from urllib.parse import urlparse[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py → b/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py[0m
[38;2;139;134;130m@@ -1,5 +1,5 @@[0m
[38;2;184;134;11m """[0m
[38;2;255;255;255;48;2;119;20;20m-"""Forge Mission Control v6 - Production-Grade Dashboard Server[0m
[38;2;255;255;255;48;2;19;87;20m+Forge Mission Control v6 - Production-Grade Dashboard Server[0m
[38;2;184;134;11m Port 8765. Serves HTML + JSON API with cached state, forge controls,[0m
[38;2;184;134;11m skill detail, activity feed, hardware telemetry, gzip compression,[0m
[38;2;184;134;11m and health endpoint.[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py → b/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py[0m
[38;2;139;134;130m@@ -16,6 +16,65 @@[0m
[38;2;184;134;11m STATE_FILE = FORGE_ROOT / "state.yaml"[0m
[38;2;184;134;11m DASHBOARD_HTML = Path(__file__).resolve().parent / "mission_control_8765.html"[0m
[38;2;184;134;11m REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# --- Security ---[0m
[38;2;255;255;255;48;2;19;87;20m+MAX_BODY_BYTES = 65536  # 64 KB request body limit[0m
[38;2;255;255;255;48;2;19;87;20m+CSRF_SECRET = secrets.token_hex(32)[0m
[38;2;255;255;255;48;2;19;87;20m+ALLOWED_ORIGINS = frozenset(["http://localhost:8765", "http://127.0.0.1:8765"])[0m
[38;2;255;255;255;48;2;19;87;20m+BLUEPRINT_RE = __import__("re").compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")[0m
[38;2;255;255;255;48;2;19;87;20m+RUN_ID_RE = __import__("re").compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def csrf_token() -> str:[0m
[38;2;255;255;255;48;2;19;87;20m+    """Generate a signed CSRF token valid for this session."""[0m
[38;2;255;255;255;48;2;19;87;20m+    ts = str(int(time.time()))[0m
[38;2;255;255;255;48;2;19;87;20m+    raw = ts + "." + secrets.token_hex(16)[0m
[38;2;255;255;255;48;2;19;87;20m+    sig = hmac.new(CSRF_SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()[:16][0m
[38;2;255;255;255;48;2;19;87;20m+    return f"{raw}.{sig}"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def verify_csrf(token: str) -> bool:[0m
[38;2;255;255;255;48;2;19;87;20m+    """Verify a signed CSRF token (30-minute expiry)."""[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        parts = token.split(".")[0m
[38;2;255;255;255;48;2;19;87;20m+        if len(parts) != 4:[0m
[38;2;255;255;255;48;2;19;87;20m+            return False[0m
[38;2;255;255;255;48;2;19;87;20m+        ts_str, nonce, sig = parts[0], parts[1], ".".join(parts[2:4])[0m
[38;2;255;255;255;48;2;19;87;20m+        ts = int(ts_str)[0m
[38;2;255;255;255;48;2;19;87;20m+        if time.time() - ts > 1800:  # 30 min expiry[0m
[38;2;255;255;255;48;2;19;87;20m+            return False[0m
[38;2;255;255;255;48;2;19;87;20m+        expected_sig = hmac.new(CSRF_SECRET.encode(), (ts_str + "." + nonce).encode(), hashlib.sha256).hexdigest()[:16][0m
[38;2;255;255;255;48;2;19;87;20m+        return hmac.compare_digest(sig, expected_sig)[0m
[38;2;255;255;255;48;2;19;87;20m+    except (ValueError, IndexError):[0m
[38;2;255;255;255;48;2;19;87;20m+        return False[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def validate_blueprint(name: str) -> bool:[0m
[38;2;255;255;255;48;2;19;87;20m+    """Block path traversal and command injection via blueprint names."""[0m
[38;2;255;255;255;48;2;19;87;20m+    return bool(BLUEPRINT_RE.match(name))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def validate_run_id(rid: str) -> bool:[0m
[38;2;255;255;255;48;2;19;87;20m+    """Block path traversal and command injection via run IDs."""[0m
[38;2;255;255;255;48;2;19;87;20m+    return bool(RUN_ID_RE.match(rid))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def security_headers(handler, mime_type="text/html; charset=utf-8", add_csp=True):[0m
[38;2;255;255;255;48;2;19;87;20m+    """Emit OWASP-aligned security headers."""[0m
[38;2;255;255;255;48;2;19;87;20m+    handler.send_header("X-Content-Type-Options", "nosniff")[0m
[38;2;255;255;255;48;2;19;87;20m+    handler.send_header("X-Frame-Options", "DENY")[0m
[38;2;255;255;255;48;2;19;87;20m+    handler.send_header("X-XSS-Protection", "0")  # Deprecated; CSP handles it.[0m
[38;2;255;255;255;48;2;19;87;20m+    handler.send_header("Referrer-Policy", "strict-origin-when-cross-origin")[0m
[38;2;255;255;255;48;2;19;87;20m+    handler.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")[0m
[38;2;255;255;255;48;2;19;87;20m+    if add_csp:[0m
[38;2;255;255;255;48;2;19;87;20m+        csp = ([0m
[38;2;255;255;255;48;2;19;87;20m+            "default-src 'self'; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "font-src 'self' https://cdn.jsdelivr.net; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "img-src 'self' data: blob:; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "connect-src 'self'; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "frame-ancestors 'none'; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "form-action 'self'; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "base-uri 'self'; "[0m
[38;2;255;255;255;48;2;19;87;20m+            "object-src 'none'"[0m
[38;2;255;255;255;48;2;19;87;20m+        )[0m
[38;2;255;255;255;48;2;19;87;20m+        handler.send_header("Content-Security-Policy", csp)[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m try:[0m
[38;2;184;134;11m     import yaml[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py → b/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py[0m
[38;2;139;134;130m@@ -411,6 +411,23 @@[0m
[38;2;184;134;11m class Handler(BaseHTTPRequestHandler):[0m
[38;2;184;134;11m     def log_message(self, *a): pass[0m
[38;2;184;134;11m [0m
[38;2;255;255;255;48;2;19;87;20m+    def _set_cors(self):[0m
[38;2;255;255;255;48;2;19;87;20m+        """Set CORS header only if origin matches allowed list."""[0m
[38;2;255;255;255;48;2;19;87;20m+        origin = self.headers.get("Origin", "")[0m
[38;2;255;255;255;48;2;19;87;20m+        if origin in ALLOWED_ORIGINS:[0m
[38;2;255;255;255;48;2;19;87;20m+            self.send_header("Access-Control-Allow-Origin", origin)[0m
[38;2;255;255;255;48;2;19;87;20m+            self.send_header("Vary", "Origin")[0m
[38;2;255;255;255;48;2;19;87;20m+            self.send_header("Access-Control-Allow-Credentials", "true")[0m
[38;2;255;255;255;48;2;19;87;20m+            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")[0m
[38;2;255;255;255;48;2;19;87;20m+            self.send_header("Access-Control-Allow-Headers", "Content-Type, X-CSRF-Token")[0m
[38;2;255;255;255;48;2;19;87;20m+            self.send_header("Access-Control-Max-Age", "86400")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    def do_OPTIONS(self):[0m
[38;2;255;255;255;48;2;19;87;20m+        """CORS preflight."""[0m
[38;2;255;255;255;48;2;19;87;20m+        self.send_response(204)[0m
[38;2;255;255;255;48;2;19;87;20m+        self._set_cors()[0m
[38;2;255;255;255;48;2;19;87;20m+        self.end_headers()[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;184;134;11m     def do_GET(self):[0m
[38;2;184;134;11m         p = urlparse(self.path).path[0m
[38;2;184;134;11m         if p == "/api/state":[0m
[38;2;139;134;130m@@ -423,65 +440,89 @@[0m
[38;2;184;134;11m             self._json({"skills": get_skills()})[0m
[38;2;184;134;11m         elif p == "/api/activity":[0m
[38;2;184;134;11m             self._json({"activity": list(ACTIVITY_LOG[:50])})[0m
[38;2;255;255;255;48;2;19;87;20m+        elif p == "/api/csrf-token":[0m
[38;2;255;255;255;48;2;19;87;20m+            self._json({"csrf_token": csrf_token()})[0m
[38;2;184;134;11m         elif p == "/" or p == "/index.html":[0m
[38;2;184;134;11m             if DASHBOARD_HTML.exists():[0m
[38;2;184;134;11m                 self._raw(DASHBOARD_HTML.read_bytes(), "text/html; charset=utf-8")[0m
[38;2;184;134;11m             else:[0m
[38;2;184;134;11m                 self._raw(b"<h1>Dashboard not found</h1>", "text/html")[0m
[38;2;184;134;11m         else:[0m
[38;2;255;255;255;48;2;119;20;20m-            self.send_response(404); self.end_headers()[0m
[38;2;255;255;255;48;2;119;20;20m-            self.wfile.write(b"Not found")[0m
[38;2;255;255;255;48;2;19;87;20m+            self._json({"error": "not found"}, 404)[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m     def do_POST(self):[0m
[38;2;184;134;11m         p = urlparse(self.path).path[0m
[38;2;255;255;255;48;2;119;20;20m-        cl = int(self.headers.get("Content-Length", 0))[0m
[38;2;255;255;255;48;2;119;20;20m-        body = self.rfile.read(cl).decode() if cl else "{}"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+        # CSRF check on all POST endpoints except health/ping[0m
[38;2;255;255;255;48;2;19;87;20m+        token = self.headers.get("X-CSRF-Token", "")[0m
[38;2;255;255;255;48;2;19;87;20m+        if not verify_csrf(token):[0m
[38;2;255;255;255;48;2;19;87;20m+            self._json({"error": "invalid or missing CSRF token"}, 403)[0m
[38;2;255;255;255;48;2;19;87;20m+            return[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+        # Body size limit[0m
[38;2;255;255;255;48;2;19;87;20m+        raw_cl = self.headers.get("Content-Length", "0")[0m
[38;2;255;255;255;48;2;19;87;20m+        try:[0m
[38;2;255;255;255;48;2;19;87;20m+            cl = int(raw_cl)[0m
[38;2;255;255;255;48;2;19;87;20m+        except ValueError:[0m
[38;2;255;255;255;48;2;19;87;20m+            self._json({"error": "invalid Content-Length"}, 400)[0m
[38;2;255;255;255;48;2;19;87;20m+            return[0m
[38;2;255;255;255;48;2;19;87;20m+        if cl > MAX_BODY_BYTES:[0m
[38;2;255;255;255;48;2;19;87;20m+            self._json({"error": "request body too large"}, 413)[0m
[38;2;255;255;255;48;2;19;87;20m+            return[0m
[38;2;255;255;255;48;2;19;87;20m+        body = self.rfile.read(cl).decode("utf-8", errors="replace") if cl else "{}"[0m
[38;2;184;134;11m         try:[0m
[38;2;184;134;11m             data = json.loads(body)[0m
[38;2;255;255;255;48;2;119;20;20m-        except:[0m
[38;2;255;255;255;48;2;119;20;20m-            data = {}[0m
[38;2;255;255;255;48;2;19;87;20m+        except json.JSONDecodeError:[0m
[38;2;255;255;255;48;2;19;87;20m+            self._json({"error": "invalid JSON body"}, 400)[0m
[38;2;255;255;255;48;2;19;87;20m+            return[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m         fp = FORGE_ROOT / "Core" / "forge.py"[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m         if p == "/api/spawn":[0m
[38;2;184;134;11m             bp = data.get("blueprint", "")[0m
[38;2;255;255;255;48;2;119;20;20m-            if bp:[0m
[38;2;255;255;255;48;2;119;20;20m-                log_activity("spawn", bp, "Spawn dispatched", 50, "running")[0m
[38;2;255;255;255;48;2;119;20;20m-                try:[0m
[38;2;255;255;255;48;2;119;20;20m-                    subprocess.Popen([sys.executable, str(fp), "spawn", bp],[0m
[38;2;255;255;255;48;2;119;20;20m-                                     cwd=str(FORGE_ROOT),[0m
[38;2;139;134;130m… omitted 92 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -1062,8 +1062,14 @@[0m
[38;2;184;134;11m });[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m /* ─── BOOT ─── */[0m
[38;2;255;255;255;48;2;19;87;20m+let csrfToken = '';[0m
[38;2;184;134;11m (async function(){[0m
[38;2;184;134;11m   renderStatic();[0m
[38;2;255;255;255;48;2;19;87;20m+  try{[0m
[38;2;255;255;255;48;2;19;87;20m+    const tokResp = await fetch('/api/csrf-token');[0m
[38;2;255;255;255;48;2;19;87;20m+    const tokData = await tokResp.json();[0m
[38;2;255;255;255;48;2;19;87;20m+    csrfToken = tokData.csrf_token || '';[0m
[38;2;255;255;255;48;2;19;87;20m+  }catch(e){}[0m
[38;2;184;134;11m   try{const r=await fetch(API);const d=await r.json();[0m
[38;2;184;134;11m     // Pre-populate terminal from seed activity[0m
[38;2;184;134;11m     termSeen.clear();[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -961,7 +961,7 @@[0m
[38;2;184;134;11m function apiSpawn(){[0m
[38;2;184;134;11m   const bp=document.getElementById('spawn-input').value.trim();[0m
[38;2;184;134;11m   if(!bp)return flash('Enter blueprint name first');[0m
[38;2;255;255;255;48;2;119;20;20m-  fetch('/api/spawn',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({blueprint:bp})})[0m
[38;2;255;255;255;48;2;19;87;20m+  fetch('/api/spawn',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrfToken},body:JSON.stringify({blueprint:bp})})[0m
[38;2;184;134;11m     .then(()=>{flash(`Spawned: ${bp}`);setTimeout(fetchState,600)});[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m function apiEval(){[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -967,7 +967,7 @@[0m
[38;2;184;134;11m function apiEval(){[0m
[38;2;184;134;11m   const bp=prompt('Blueprint:');if(!bp)return;[0m
[38;2;184;134;11m   const rid=prompt('Run ID (blank=latest):')||'latest';[0m
[38;2;255;255;255;48;2;119;20;20m-  fetch('/api/eval',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({blueprint:bp,run_id:rid})})[0m
[38;2;255;255;255;48;2;19;87;20m+  fetch('/api/eval',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrfToken},body:JSON.stringify({blueprint:bp,run_id:rid})})[0m
[38;2;184;134;11m     .then(()=>{flash(`Eval: ${bp}`);setTimeout(fetchState,600)});[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m function apiImprove(){[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -973,7 +973,7 @@[0m
[38;2;184;134;11m function apiImprove(){[0m
[38;2;184;134;11m   const bp=prompt('Blueprint:');if(!bp)return;[0m
[38;2;184;134;11m   const rid=prompt('Run ID:');if(!rid)return;[0m
[38;2;255;255;255;48;2;119;20;20m-  fetch('/api/improve',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({blueprint:bp,run_id:rid})})[0m
[38;2;255;255;255;48;2;19;87;20m+  fetch('/api/improve',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrfToken},body:JSON.stringify({blueprint:bp,run_id:rid})})[0m
[38;2;184;134;11m     .then(()=>{flash(`Improve: ${bp}`);setTimeout(fetchState,600)});[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m function apiLoop(){[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -977,7 +977,7 @@[0m
[38;2;184;134;11m     .then(()=>{flash(`Improve: ${bp}`);setTimeout(fetchState,600)});[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m function apiLoop(){[0m
[38;2;255;255;255;48;2;119;20;20m-  fetch('/api/loop',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'})[0m
[38;2;255;255;255;48;2;19;87;20m+  fetch('/api/loop',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrfToken},body:'{}'})[0m
[38;2;184;134;11m     .then(()=>{flash('Loop started');setTimeout(fetchState,600)});[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m function apiCaveman(on){[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html → b/D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html[0m
[38;2;139;134;130m@@ -981,7 +981,7 @@[0m
[38;2;184;134;11m     .then(()=>{flash('Loop started');setTimeout(fetchState,600)});[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m function apiCaveman(on){[0m
[38;2;255;255;255;48;2;119;20;20m-  fetch('/api/toggle-caveman',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'})[0m
[38;2;255;255;255;48;2;19;87;20m+  fetch('/api/toggle-caveman',{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrfToken},body:'{}'})[0m
[38;2;184;134;11m     .then(()=>{flash(on?'Caveman ON':'Caveman OFF');setTimeout(fetchState,400)});[0m
[38;2;184;134;11m }[0m
[38;2;184;134;11m [0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py → b/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py[0m
[38;2;139;134;130m@@ -7,7 +7,7 @@[0m
[38;2;184;134;11m Security: CSP, CORS (locked), CSRF tokens, security headers,[0m
[38;2;184;134;11m body size limiting, input validation. OWASP-aligned.[0m
[38;2;184;134;11m """[0m
[38;2;255;255;255;48;2;119;20;20m-import json, os, sys, time, subprocess, threading, gzip, io, hmac, hashlib, secrets[0m
[38;2;255;255;255;48;2;19;87;20m+import json, os, sys, time, subprocess, threading, gzip, io, hmac, hashlib, secrets, re[0m
[38;2;184;134;11m from pathlib import Path[0m
[38;2;184;134;11m from http.server import HTTPServer, BaseHTTPRequestHandler[0m
[38;2;184;134;11m from urllib.parse import urlparse[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py → b/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py[0m
[38;2;139;134;130m@@ -21,8 +21,8 @@[0m
[38;2;184;134;11m MAX_BODY_BYTES = 65536  # 64 KB request body limit[0m
[38;2;184;134;11m CSRF_SECRET = secrets.token_hex(32)[0m
[38;2;184;134;11m ALLOWED_ORIGINS = frozenset(["http://localhost:8765", "http://127.0.0.1:8765"])[0m
[38;2;255;255;255;48;2;119;20;20m-BLUEPRINT_RE = __import__("re").compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")[0m
[38;2;255;255;255;48;2;119;20;20m-RUN_ID_RE = __import__("re").compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")[0m
[38;2;255;255;255;48;2;19;87;20m+BLUEPRINT_RE = re.compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")[0m
[38;2;255;255;255;48;2;19;87;20m+RUN_ID_RE = re.compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m def csrf_token() -> str:[0m
[38;2;184;134;11m     """Generate a signed CSRF token valid for this session."""[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-security.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-security.py[0m
[38;2;139;134;130m@@ -0,0 +1,224 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+Ad-hoc verification: security controls in server_8765.py.[0m
[38;2;255;255;255;48;2;19;87;20m+Tests CSP, CORS, CSRF, body limits, input validation, security headers.[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import sys, os, json, time, tempfile, http.client, threading, subprocess[0m
[38;2;255;255;255;48;2;19;87;20m+from pathlib import Path[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+FORGE_ROOT = Path("D:/styde/_alpedal/styde-forge")[0m
[38;2;255;255;255;48;2;19;87;20m+SERVER_PATH = FORGE_ROOT / "Dashboard" / "web" / "server_8765.py"[0m
[38;2;255;255;255;48;2;19;87;20m+HTML_PATH = FORGE_ROOT / "Dashboard" / "web" / "mission_control_8765.html"[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+errors = [][0m
[38;2;255;255;255;48;2;19;87;20m+passes = [][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check(desc, condition, detail=""):[0m
[38;2;255;255;255;48;2;19;87;20m+    if condition:[0m
[38;2;255;255;255;48;2;19;87;20m+        passes.append(f"PASS: {desc}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"FAIL: {desc}  {detail}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def check_eq(desc, got, expected):[0m
[38;2;255;255;255;48;2;19;87;20m+    if got == expected:[0m
[38;2;255;255;255;48;2;19;87;20m+        passes.append(f"PASS: {desc}")[0m
[38;2;255;255;255;48;2;19;87;20m+    else:[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"FAIL: {desc}  got={repr(got)} expected={repr(expected)}")[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 1. Import the module and test its functions[0m
[38;2;255;255;255;48;2;19;87;20m+sys.path.insert(0, str(SERVER_PATH.parent))[0m
[38;2;255;255;255;48;2;19;87;20m+import importlib.util[0m
[38;2;255;255;255;48;2;19;87;20m+spec = importlib.util.spec_from_file_location("server_mod", SERVER_PATH)[0m
[38;2;255;255;255;48;2;19;87;20m+mod = importlib.util.module_from_spec(spec)[0m
[38;2;255;255;255;48;2;19;87;20m+spec.loader.exec_module(mod)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 2. Test CSRF functions[0m
[38;2;255;255;255;48;2;19;87;20m+print("--- CSRF ---")[0m
[38;2;255;255;255;48;2;19;87;20m+t1 = mod.csrf_token()[0m
[38;2;255;255;255;48;2;19;87;20m+check("csrf_token() returns string", isinstance(t1, str) and len(t1) > 20)[0m
[38;2;255;255;255;48;2;19;87;20m+check("verify_csrf accepts valid token", mod.verify_csrf(t1))[0m
[38;2;255;255;255;48;2;19;87;20m+check("verify_csrf rejects empty string", not mod.verify_csrf(""))[0m
[38;2;255;255;255;48;2;19;87;20m+check("verify_csrf rejects garbage", not mod.verify_csrf("abc.def.ghi"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("verify_csrf rejects tampered sig", not mod.verify_csrf(t1[:-1] + ("X" if t1[-1] != "X" else "Y")))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 3. Test input validation[0m
[38;2;255;255;255;48;2;19;87;20m+print("--- Input Validation ---")[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_blueprint('hello-world')", mod.validate_blueprint("hello-world"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_blueprint('agent_v2.1')", mod.validate_blueprint("agent_v2.1"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_blueprint rejects '../etc'", not mod.validate_blueprint("../etc"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_blueprint rejects 'a;rm -rf'", not mod.validate_blueprint("a;rm -rf"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_blueprint rejects 'a|id'", not mod.validate_blueprint("a|id"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_blueprint rejects '$PATH'", not mod.validate_blueprint("$PATH"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_blueprint rejects blank", not mod.validate_blueprint(""))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_run_id('run_001')", mod.validate_run_id("run_001"))[0m
[38;2;255;255;255;48;2;19;87;20m+check("validate_run_id rejects '../../etc'", not mod.validate_run_id("../../etc"))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# 4. Test security_headers helper[0m
[38;2;255;255;255;48;2;19;87;20m+print("--- Security Headers ---")[0m
[38;2;255;255;255;48;2;19;87;20m+from http.server import BaseHTTPRequestHandler[0m
[38;2;255;255;255;48;2;19;87;20m+from io import BytesIO[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+class FakeHandler:[0m
[38;2;255;255;255;48;2;19;87;20m+    def __init__(self):[0m
[38;2;255;255;255;48;2;19;87;20m+        self.headers_list = [][0m
[38;2;255;255;255;48;2;19;87;20m+    def send_header(self, k, v):[0m
[38;2;255;255;255;48;2;19;87;20m+        self.headers_list.append((k, v))[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+fh = FakeHandler()[0m
[38;2;255;255;255;48;2;19;87;20m+mod.security_headers(fh)[0m
[38;2;255;255;255;48;2;19;87;20m+hdr_names = {k for k, v in fh.headers_list}[0m
[38;2;255;255;255;48;2;19;87;20m+check("X-Content-Type-Options present", "X-Content-Type-Options" in hdr_names)[0m
[38;2;255;255;255;48;2;19;87;20m+check("X-Frame-Options present", "X-Frame-Options" in hdr_names)[0m
[38;2;255;255;255;48;2;19;87;20m+check("Referrer-Policy present", "Referrer-Policy" in hdr_names)[0m
[38;2;255;255;255;48;2;19;87;20m+check("Permissions-Policy present", "Permissions-Policy" in hdr_names)[0m
[38;2;255;255;255;48;2;19;87;20m+check("Content-Security-Policy present", "Content-Security-Policy" in hdr_names)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# Verify CSP values[0m
[38;2;255;255;255;48;2;19;87;20m+csp = dict(fh.headers_list).get("Content-Security-Policy", "")[0m
[38;2;255;255;255;48;2;19;87;20m+check("CSP contains frame-ancestors 'none'", "frame-ancestors 'none'" in csp)[0m
[38;2;139;134;130m… omitted 146 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-security.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-security.py[0m
[38;2;139;134;130m@@ -153,13 +153,17 @@[0m
[38;2;184;134;11m     conn.close()[0m
[38;2;184;134;11m     [0m
[38;2;184;134;11m     # Test POST with oversized body[0m
[38;2;255;255;255;48;2;119;20;20m-    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)[0m
[38;2;255;255;255;48;2;119;20;20m-    big_body = "x" * 70000[0m
[38;2;184;134;11m     # First get a valid CSRF token[0m
[38;2;255;255;255;48;2;19;87;20m+    conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)[0m
[38;2;184;134;11m     conn.request("GET", "/api/csrf-token")[0m
[38;2;184;134;11m     tr = conn.getresponse()[0m
[38;2;255;255;255;48;2;119;20;20m-    td = json.loads(tr.read())[0m
[38;2;255;255;255;48;2;119;20;20m-    tok = td.get("csrf_token", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    raw = tr.read()[0m
[38;2;255;255;255;48;2;19;87;20m+    try:[0m
[38;2;255;255;255;48;2;19;87;20m+        td = json.loads(raw)[0m
[38;2;255;255;255;48;2;19;87;20m+        tok = td.get("csrf_token", "")[0m
[38;2;255;255;255;48;2;19;87;20m+    except (json.JSONDecodeError, ValueError):[0m
[38;2;255;255;255;48;2;19;87;20m+        tok = ""[0m
[38;2;255;255;255;48;2;19;87;20m+        errors.append(f"FAIL: CSRF token endpoint returned unparseable: {raw[:200]}")[0m
[38;2;184;134;11m     conn.close()[0m
[38;2;184;134;11m     [0m
[38;2;184;134;11m     conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)[0m
  ┊ review diff
[38;2;218;165;32ma/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-security.py → b/C:\Users\Pontus\AppData\Local\Temp\hermes-verify-security.py[0m
[38;2;139;134;130m@@ -165,7 +165,8 @@[0m
[38;2;184;134;11m         tok = ""[0m
[38;2;184;134;11m         errors.append(f"FAIL: CSRF token endpoint returned unparseable: {raw[:200]}")[0m
[38;2;184;134;11m     conn.close()[0m
[38;2;255;255;255;48;2;119;20;20m-    [0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    big_body = "x" * 70000[0m
[38;2;184;134;11m     conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)[0m
[38;2;184;134;11m     conn.request("POST", "/api/spawn", big_body,[0m
[38;2;184;134;11m                  {"Content-Type": "application/json", "X-CSRF-Token": tok})[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py → b/D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py[0m
[38;2;139;134;130m@@ -35,9 +35,9 @@[0m
[38;2;184;134;11m     """Verify a signed CSRF token (30-minute expiry)."""[0m
[38;2;184;134;11m     try:[0m
[38;2;184;134;11m         parts = token.split(".")[0m
[38;2;255;255;255;48;2;119;20;20m-        if len(parts) != 4:[0m
[38;2;255;255;255;48;2;19;87;20m+        if len(parts) != 3:[0m
[38;2;184;134;11m             return False[0m
[38;2;255;255;255;48;2;119;20;20m-        ts_str, nonce, sig = parts[0], parts[1], ".".join(parts[2:4])[0m
[38;2;255;255;255;48;2;19;87;20m+        ts_str, nonce, sig = parts[0], parts[1], parts[2][0m
[38;2;184;134;11m         ts = int(ts_str)[0m
[38;2;184;134;11m         if time.time() - ts > 1800:  # 30 min expiry[0m
[38;2;184;134;11m             return False[0m
Ad-hoc verification result: 52 passed, 0 failed. All security controls operational.
FINAL SECURITY POSTURE
  CSP             Content-Security-Policy on HTML responses. Inline scripts allowed (unsafe-inline, required by existing HTML design). frame-ancestors: none, form-action: self, object-src: none.
  CORS            Locked to localhost:8765 and 127.0.0.1:8765. Wildcard removed. Preflight (OPTIONS) supported.
  CSRF            HMAC-SHA256 signed tokens with 30-min expiry. All 5 POST endpoints (spawn, eval, improve, loop, toggle-caveman) require X-CSRF-Token header.
  Body limit      64KB max. Invalid Content-Length returns 400. Oversized returns 413.
  Input validation  Blueprint and run_id restricted to [a-zA-Z0-9_.-], max 128 chars. Rejects ../ ; | $ shell metacharacters.
  Security headers  X-Content-Type-Options: nosniff, X-Frame-Options: DENY, X-XSS-Protection: 0, Referrer-Policy: strict-origin-when-cross-origin, Permissions-Policy: camera=(), microphone=(), geolocation=().
  Cache control    no-cache, no-store, must-revalidate on all dynamic responses.
  HTML client      All 5 POST fetch calls in the dashboard now include X-CSRF-Token header. Token fetched at page boot from /api/csrf-token.
Files hardened:
  D:\styde\_alpedal\styde-forge\Dashboard\web\server_8765.py
  D:\styde\_alpedal\styde-forge\Dashboard\web\mission_control_8765.html
One bug caught during verification: CSRF verify function had wrong parts count (4 instead of 3) — fixed before final test pass.