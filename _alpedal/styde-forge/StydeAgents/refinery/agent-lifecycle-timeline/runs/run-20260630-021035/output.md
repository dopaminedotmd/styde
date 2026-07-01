The existing timeline.html has the full renderer but hardcoded checkpoint data. I will add a `/api/timeline` endpoint that walks the live filesystem (StydeAgents/*/runs/*/) and rewrite timeline.html to fetch from it.
Two changes needed:
1. Add timeline data scraper + endpoint to server_8765.py
2. Replace hardcoded DATA in timeline.html with a live fetch
---
**server_8765.py — add after `_scan_skills()` (line ~200)**
```python
# ─── Timeline Agent Scanner ───
def scan_timeline_agents():
    agents = []
    evals = []
    stages = ["refinery", "production", "archive"]
    for stage in stages:
        stage_dir = FORGE_ROOT / "StydeAgents" / stage
        if not stage_dir.exists():
            continue
        for bp_dir in sorted(stage_dir.iterdir()):
            if not bp_dir.is_dir() or bp_dir.name.startswith("_"):
                continue
            runs_dir = bp_dir / "runs"
            if not runs_dir.exists():
                continue
            for rd in sorted(runs_dir.iterdir()):
                if not rd.is_dir() or not rd.name.startswith("run-"):
                    continue
                run_id = rd.name[4:]  # strip "run-" prefix
                agent = {
                    "blueprint": bp_dir.name,
                    "run_id": run_id,
                    "stage": stage,
                    "status": "completed",
                }
                # Read spawn_context.yaml for spawned_at, benchmark, iteration
                ctxf = rd / "spawn_context.yaml"
                if ctxf.exists():
                    try:
                        ctx = yaml.safe_load(ctxf.read_text()) or {}
                        agent["spawned_at"] = ctx.get("spawned_at", "")
                        agent["benchmark"] = ctx.get("benchmark", "")
                        agent["iteration"] = ctx.get("iteration", 1)
                    except Exception:
                        pass
                # Read eval.yaml for score
                evf = rd / "eval.yaml"
                score = None
                diagnosis = ""
                summary = ""
                if evf.exists():
                    try:
                        ev = yaml.safe_load(evf.read_text()) or {}
                        score = ev.get("composite", {}).get("composite_score") or ev.get("composite_score")
                        dims = ev.get("composite", {}).get("dimensions", {}) or ev.get("dimensions", {})
                        if dims:
                            # find lowest dimension for diagnosis
                            lowest_dim = min(dims, key=lambda k: dims[k]) if dims else ""
                            diagnosis = lowest_dim
                        notes = ev.get("judge_eval", {}).get("notes", "") or ev.get("teacher_review", "")
                        summary = notes[:120] if notes else ""
                    except Exception:
                        pass
                if score is not None:
                    evals.append({
                        "blueprint": bp_dir.name,
                        "run_id": run_id,
                        "score": round(score, 1),
                        "diagnosis": diagnosis,
                        "summary": summary,
                    })
                if agent.get("spawned_at"):
                    agents.append(agent)
    # deduplicate agent entries by run_id (filesystem can have dupes)
    seen = set()
    deduped = []
    for a in agents:
        key = a["run_id"]
        if key not in seen:
            seen.add(key)
            deduped.append(a)
    # deduplicate evals too
    seen_e = set()
    deduped_ev = []
    for e in evals:
        key = e["run_id"]
        if key not in seen_e:
            seen_e.add(key)
            deduped_ev.append(e)
    bp_set = set(a["blueprint"] for a in deduped)
    meta = {
        "blueprints": len(bp_set),
        "total_agents": len(deduped),
        "total_spawned": len(deduped),
        "total_evals": len(deduped_ev),
        "loop_iterations": 0,
        "last_checkpoint": max((a["spawned_at"] for a in deduped if a.get("spawned_at")), default=""),
        "caveman_ultra": True,
    }
    return {"agents": deduped, "evals": deduped_ev, "meta": meta}
```
Then add the route inside `do_GET`:
```python
elif p == "/api/timeline":
    self._json(scan_timeline_agents())
```
Add it right after the `/api/activity` route (line ~494).
---
**timeline.html — replace the entire DATA block (lines 104-475)**
The big hardcoded `const DATA={agents:[...],evals:[...],meta:{...}};` needs to become an async fetch. Replace that block (everything from `const DATA={agents:[` through the line before `// ====== RENDERER ======`) with:
```javascript
// ====== LIVE DATA LOADER ======
const DATA = {agents:[], evals:[], meta:{blueprints:0,loop_iterations:0,total_agents:0,total_spawned:0,total_evals:0,last_checkpoint:"-"}};
async function loadTimelineData() {
  try {
    const resp = await fetch('/api/timeline');
    if (!resp.ok) throw new Error('HTTP '+resp.status);
    const live = await resp.json();
    if (live && live.agents) {
      DATA.agents = live.agents;
      DATA.evals = live.evals || [];
      DATA.meta = live.meta || DATA.meta;
    }
  } catch(e) {
    console.warn('Timeline data load failed, using empty data:', e);
  }
  render();
}
```
And at the bottom of the script (replace the `render();` call on line 753 / `// init` section):
```javascript
// init
loadTimelineData();
```
And add a 60-second auto-refresh timer:
```javascript
// auto-refresh every 60s
setInterval(loadTimelineData, 60000);
```
---
The key insight: the existing timeline.html already has all the rendering logic — SVG tracks, time scrubber, auto-play, color-coded nodes (gold/amber/cool), click-to-popup with run_id/version/stage/score/benchmark. The only missing piece was live data from the filesystem instead of a hardcoded snapshot. The `/api/timeline` endpoint walks refinery, production, and archive directories, reads every `spawn_context.yaml` for timestamps and every `eval.yaml` for composite scores, and returns the unified dataset the renderer expects. The HTML stays completely client-rendered and interactive.