Now I have the full picture. Let me compile the audit.
---
*** Begin Patch
*** Update File: D:\styde\_alpedal\styde-forge\Core\checkpoint.py
@@ verify_checkpoint: _hash_dir timing bug @@
 def _hash_dir(path: Path) -> str:
     hasher = hashlib.sha256()
+    # EXCLUDE checkpoint_manifest.json — it is written AFTER the hash is
+    # computed during creation, so including it makes verification always fail.
+    exclude_files = {"checkpoint_manifest.json"}
     for f in sorted(path.rglob("*")):
         if f.is_file() and not f.name.startswith("."):
+            if f.name in exclude_files:
+                continue
             hasher.update(str(f.relative_to(path)).encode())
             hasher.update(f.read_bytes())
     return hasher.hexdigest()
*** End Patch
*** Begin Patch
*** Update File: D:\styde\_alpedal\styde-forge\Core\forge.py
@@ cmd_loop_parallel: serialise state writes across threads @@
 # ═══════════════════════════════════════════════════════════════
 # PARALLEL LOOP
 # ═══════════════════════════════════════════════════════════════
+_parallel_state_lock = threading.Lock()  # serialise state.yaml RMW in parallel workers
+_parallel_activity_seq_lock = threading.Lock()
 def cmd_loop_parallel(
@@ usage in log_activity calls from parallel code @@
-def log_activity(…) -> dict:
+def log_activity(…) -> dict:
     global _activity_seq
+    with _parallel_activity_seq_lock:
         _activity_seq += 1
+        seq_val = _activity_seq
-    _activity_seq += 1
-    entry = { "id": _activity_seq, … }
+    entry = { "id": seq_val, … }
*** End Patch
*** Begin Patch
*** Update File: D:\styde\_alpedal\styde-forge\Core\hermes_bridge.py
@@ cache: compute truncated key before cache GET to match SET key @@
     hermes_bin = find_hermes()
+    # Truncate BEFORE cache lookup so GET and SET use the same truncated key
+    original_prompt = prompt
+    if len(prompt) > MAX_PROMPT_LENGTH:
+        prompt = prompt[:MAX_PROMPT_LENGTH] + "\n... [truncated]"
     # Smart cache: check before making API call
     if _cache_available:
-        cached = cache_get(model, prompt, content_hash=content_hash)
+        cached = cache_get(model, prompt, content_hash=content_hash or hashlib.sha256(original_prompt.encode()).hexdigest()[:16] if len(original_prompt) > MAX_PROMPT_LENGTH else content_hash)
         if cached:
             return {
                 "success": True,
@@ remove duplicate truncation after this point @@
-    # Truncate long prompts to stay under Windows CreateProcess 32767 limit
-    # Do this BEFORE cache lookup so cache key uses truncated prompt
-    if len(prompt) > MAX_PROMPT_LENGTH:
-        prompt = prompt[:MAX_PROMPT_LENGTH] + "\n... [truncated]"
-
     last_error = None
*** End Patch