┊ review diff
[38;2;218;165;32ma/migrate_state.py → b/migrate_state.py[0m
[38;2;139;134;130m@@ -0,0 +1,346 @@[0m
[38;2;255;255;255;48;2;19;87;20m+#!/usr/bin/env python3[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+State Migration Engineer — state.yaml → multi-file architecture[0m
[38;2;255;255;255;48;2;19;87;20m+Migrates single-file state to agents/ evaluations/ activity/ + state.meta.yaml[0m
[38;2;255;255;255;48;2;19;87;20m+Verifies semantic equivalence before/after. Backup first. Dry-run available.[0m
[38;2;255;255;255;48;2;19;87;20m+"""[0m
[38;2;255;255;255;48;2;19;87;20m+import os[0m
[38;2;255;255;255;48;2;19;87;20m+import sys[0m
[38;2;255;255;255;48;2;19;87;20m+import shutil[0m
[38;2;255;255;255;48;2;19;87;20m+import hashlib[0m
[38;2;255;255;255;48;2;19;87;20m+import copy[0m
[38;2;255;255;255;48;2;19;87;20m+from datetime import datetime[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+try:[0m
[38;2;255;255;255;48;2;19;87;20m+    import yaml[0m
[38;2;255;255;255;48;2;19;87;20m+except ImportError:[0m
[38;2;255;255;255;48;2;19;87;20m+    print("FATAL: PyYAML required. Install with: pip install pyyaml")[0m
[38;2;255;255;255;48;2;19;87;20m+    sys.exit(1)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── Config ──────────────────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+STATE_FILE = os.path.join(os.path.dirname(__file__), "state.yaml")[0m
[38;2;255;255;255;48;2;19;87;20m+OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "state_db")[0m
[38;2;255;255;255;48;2;19;87;20m+DRY_RUN = "--dry-run" in sys.argv[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── Safe YAML helpers ───────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+def safe_load(path):[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(path, "r", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        return yaml.safe_load(f)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def safe_dump(data, path):[0m
[38;2;255;255;255;48;2;19;87;20m+    with open(path, "w", encoding="utf-8") as f:[0m
[38;2;255;255;255;48;2;19;87;20m+        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+# ── Checksum helpers ────────────────────────────────────────────────[0m
[38;2;255;255;255;48;2;19;87;20m+def compute_checksum(data):[0m
[38;2;255;255;255;48;2;19;87;20m+    """Recursive semantic checksum over a data structure."""[0m
[38;2;255;255;255;48;2;19;87;20m+    s = yaml.safe_dump(data, sort_keys=True, default_flow_style=False)[0m
[38;2;255;255;255;48;2;19;87;20m+    h = hashlib.sha256(s.encode("utf-8")).hexdigest()[:16][0m
[38;2;255;255;255;48;2;19;87;20m+    return h, len(s)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def extract_metrics(state):[0m
[38;2;255;255;255;48;2;19;87;20m+    """Extract verifiable metrics from state data."""[0m
[38;2;255;255;255;48;2;19;87;20m+    activity = state.get("activity", [])[0m
[38;2;255;255;255;48;2;19;87;20m+    total_entries = len(activity)[0m
[38;2;255;255;255;48;2;19;87;20m+    eval_entries = [e for e in activity if e.get("action") == "eval"][0m
[38;2;255;255;255;48;2;19;87;20m+    spawn_entries = [e for e in activity if e.get("action") == "spawn"][0m
[38;2;255;255;255;48;2;19;87;20m+    improve_entries = [e for e in activity if e.get("action") == "improve"][0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    # Extract composite scores from evals[0m
[38;2;255;255;255;48;2;19;87;20m+    scores = [][0m
[38;2;255;255;255;48;2;19;87;20m+    for e in eval_entries:[0m
[38;2;255;255;255;48;2;19;87;20m+        d = e.get("detail", "")[0m
[38;2;255;255;255;48;2;19;87;20m+        if "C:" in d:[0m
[38;2;255;255;255;48;2;19;87;20m+            try:[0m
[38;2;255;255;255;48;2;19;87;20m+                score = float(d.split("C:")[1].split()[0])[0m
[38;2;255;255;255;48;2;19;87;20m+                scores.append(score)[0m
[38;2;255;255;255;48;2;19;87;20m+            except (ValueError, IndexError):[0m
[38;2;255;255;255;48;2;19;87;20m+                pass[0m
[38;2;255;255;255;48;2;19;87;20m+    [0m
[38;2;255;255;255;48;2;19;87;20m+    mean_score = sum(scores) / len(scores) if scores else 0.0[0m
[38;2;255;255;255;48;2;19;87;20m+    unique_blueprints = set(e.get("blueprint", "unknown") for e in activity)[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+    return {[0m
[38;2;255;255;255;48;2;19;87;20m+        "total_entries": total_entries,[0m
[38;2;255;255;255;48;2;19;87;20m+        "eval_count": len(eval_entries),[0m
[38;2;255;255;255;48;2;19;87;20m+        "spawn_count": len(spawn_entries),[0m
[38;2;255;255;255;48;2;19;87;20m+        "improve_count": len(improve_entries),[0m
[38;2;255;255;255;48;2;19;87;20m+        "unique_blueprints": len(unique_blueprints),[0m
[38;2;255;255;255;48;2;19;87;20m+        "total_scores_found": len(scores),[0m
[38;2;255;255;255;48;2;19;87;20m+        "mean_composite_score": round(mean_score, 2),[0m
[38;2;255;255;255;48;2;19;87;20m+        "min_score": round(min(scores), 2) if scores else 0,[0m
[38;2;255;255;255;48;2;19;87;20m+        "max_score": round(max(scores), 2) if scores else 0,[0m
[38;2;255;255;255;48;2;19;87;20m+    }[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+def format_blueprint_filename(name):[0m
[38;2;255;255;255;48;2;19;87;20m+    """Sanitize blueprint name for use as filename."""[0m
[38;2;255;255;255;48;2;19;87;20m+    safe = name.lower().replace(" ", "-").replace("_", "-")[0m
[38;2;255;255;255;48;2;19;87;20m+    safe = "".join(c for c in safe if c.isalnum() or c in "-.")[0m
[38;2;139;134;130m… omitted 268 diff line(s) across 1 additional file(s)/section(s)[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\migrate_state.py → b/D:\styde\_alpedal\styde-forge\migrate_state.py[0m
[38;2;139;134;130m@@ -192,7 +192,7 @@[0m
[38;2;184;134;11m     # Build metadata[0m
[38;2;184;134;11m     metadata = {[0m
[38;2;184;134;11m         "state_version": 2,[0m
[38;2;255;255;255;48;2;119;20;20m-        "migrated_at": datetime.utcnow().isoformat() + "Z",[0m
[38;2;255;255;255;48;2;19;87;20m+        "migrated_at": datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),[0m
[38;2;184;134;11m         "source_file": "state.yaml",[0m
[38;2;184;134;11m         "pre_migration_checksum": pre_checksum,[0m
[38;2;184;134;11m         "pre_migration_metrics": pre_metrics,[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\migrate_state.py → b/D:\styde\_alpedal\styde-forge\migrate_state.py[0m
[38;2;139;134;130m@@ -9,7 +9,7 @@[0m
[38;2;184;134;11m import shutil[0m
[38;2;184;134;11m import hashlib[0m
[38;2;184;134;11m import copy[0m
[38;2;255;255;255;48;2;119;20;20m-from datetime import datetime[0m
[38;2;255;255;255;48;2;19;87;20m+from datetime import datetime, timezone[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m try:[0m
[38;2;184;134;11m     import yaml[0m
  ┊ review diff
[38;2;218;165;32ma/D:\styde\_alpedal\styde-forge\migrate_state.py → b/D:\styde\_alpedal\styde-forge\migrate_state.py[0m
[38;2;139;134;130m@@ -192,7 +192,7 @@[0m
[38;2;184;134;11m     # Build metadata[0m
[38;2;184;134;11m     metadata = {[0m
[38;2;184;134;11m         "state_version": 2,[0m
[38;2;255;255;255;48;2;119;20;20m-        "migrated_at": datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),[0m
[38;2;255;255;255;48;2;19;87;20m+        "migrated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),[0m
[38;2;184;134;11m         "source_file": "state.yaml",[0m
[38;2;184;134;11m         "pre_migration_checksum": pre_checksum,[0m
[38;2;184;134;11m         "pre_migration_metrics": pre_metrics,[0m
Ad-hoc verification: 11/11 PASS — MIGRATION VERIFIED
migrate_state.py created and executed. state.yaml transformed into multi-file architecture at state_db/:
  state_db/
    agents/             17 files (one per blueprint)
    evaluations/        110 files (one per eval)
    activity/           1 chunk (200 entries, canonical order)
    runid_index.yaml    110 entries (O(1) run_id lookup)
    state.meta.yaml     versioned metadata with pre-checksums
Backup preserved at state.yaml.backup. No data loss confirmed.