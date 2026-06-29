"""Forge Command Center v2 — Real-time forge monitor
Port 8766. Shows ALL forge activity in real-time: spawns, evals, improves, loops.
"""
import sys
import os
import json
import yaml
import glob
import time
import math
import re
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

FORGE_ROOT = Path("E:/Stryde/_alpedal/styde-forge")
STATE_FILE = FORGE_ROOT / "state.yaml"
BP_DIR = FORGE_ROOT / "StydeAgents" / "blueprints"
REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"
PRODUCTION_DIR = FORGE_ROOT / "StydeAgents" / "production"

PORT = 8766
SERVER_START_TIME = time.time()

# ── State cache ──
_state_cache = None
_state_cache_time = 0
CACHE_TTL = 3

# ── compute_state result cache (slow due to eval.yaml scanning) ──
_result_cache = None
_result_cache_time = 0
RESULT_CACHE_TTL = 10

def load_state():
    global _state_cache, _state_cache_time
    now = time.time()
    if _state_cache and (now - _state_cache_time) < CACHE_TTL:
        return _state_cache
    try:
        if STATE_FILE.exists():
            _state_cache = yaml.safe_load(STATE_FILE.read_text(encoding="utf-8")) or {}
        else:
            _state_cache = {}
        _state_cache_time = now
    except Exception:
        _state_cache = {}
    return _state_cache

def compute_state():
    global _result_cache, _result_cache_time
    now = time.time()
    if _result_cache and (now - _result_cache_time) < RESULT_CACHE_TTL:
        return _result_cache

    state = load_state()
    agents = state.get("agents", []) or []
    evals = state.get("evaluations", []) or []
    improvements = state.get("improvements", []) or []
    blueprints = state.get("blueprints", []) or []
    activity = state.get("activity", []) or []

    # Forge overview
    forge_info = {
        "codename": state.get("forge_codename", "The Crucible"),
        "version": state.get("forge_version", "3.0"),
        "loop_iterations": state.get("loop_iterations", 0),
        "total_agents": state.get("total_agents", len(agents)),
        "total_evaluations": state.get("total_evaluations", len(evals)),
        "caveman_ultra": state.get("caveman_ultra", True),
        "last_checkpoint": str(state.get("last_checkpoint", "N/A"))[:30],
    }

    # Pipeline counts — read from FILESYSTEM (state.yaml is always stale)
    rn = len([p for p in (FORGE_ROOT / "StydeAgents" / "refinery").iterdir() 
              if p.is_dir() and not p.name.startswith("_")])
    pn = len([p for p in (FORGE_ROOT / "StydeAgents" / "production").iterdir() 
              if p.is_dir() and not p.name.startswith("_")])
    an = len([p for p in (FORGE_ROOT / "StydeAgents" / "archive").iterdir() 
              if p.is_dir() and not p.name.startswith("_")])

    # Active processes (running items from activity)
    active = []
    for a in activity:
        if a.get("status") == "running":
            active.append({
                "action": a.get("action", "?"),
                "blueprint": a.get("blueprint", "?"),
                "detail": str(a.get("detail", ""))[:80],
                "progress": a.get("progress", 0),
                "timestamp": a.get("timestamp", ""),
            })

    # Recent activity (last 50)
    recent = []
    for a in activity[:50]:
        recent.append({
            "action": a.get("action", "?"),
            "blueprint": a.get("blueprint", "?"),
            "detail": str(a.get("detail", ""))[:100],
            "progress": a.get("progress", 0),
            "status": a.get("status", "?"),
            "timestamp": a.get("timestamp", ""),
        })

    # Parse scores from agents + eval.yaml files on disk
    bp_scores = {}
    for a in agents:
        bp = a.get("blueprint", "")
        sc = a.get("composite_score")
        stage = a.get("stage", "refinery")
        if bp and sc is not None:
            if bp not in bp_scores:
                bp_scores[bp] = {"best": 0, "latest": 0, "stage": stage, "count": 0, "history": []}
            bp_scores[bp]["best"] = max(bp_scores[bp]["best"], sc)
            bp_scores[bp]["latest"] = sc
            bp_scores[bp]["count"] += 1

    # Fill scores from eval.yaml files on disk (refinery + production + archive)
    for zone_dir in [REFINERY_DIR, PRODUCTION_DIR, FORGE_ROOT / "StydeAgents" / "archive"]:
        if not zone_dir.exists():
            continue
        for bp_dir in sorted([d for d in zone_dir.iterdir() if d.is_dir()]):
            bp_name = bp_dir.name
            run_dirs = sorted(
                (bp_dir / "runs").iterdir() if (bp_dir / "runs").exists() else [],
                key=lambda p: p.name, reverse=True,
            )
            scores = []
            for rd in run_dirs:
                ey = rd / "eval.yaml"
                if ey.exists():
                    try:
                        ed = yaml.safe_load(ey.read_text(encoding="utf-8"))
                        cs = ed.get("composite", {}).get("composite_score", 0)
                        if cs:
                            scores.append(cs)
                    except Exception:
                        pass
                if len(scores) >= 3:
                    break
            if scores:
                entry = bp_scores.setdefault(bp_name, {"best": 0, "latest": 0, "stage": "refinery", "count": 0, "history": []})
                entry["best"] = max(entry["best"], max(scores))
                entry["latest"] = scores[0]
                entry["count"] = max(entry["count"], len(scores))
                # Best stage from agents
                for a in agents:
                    if a.get("blueprint") == bp_name:
                        entry["stage"] = a.get("stage", entry["stage"])
                entry["history"] = [{"score": s, "run": "", "ts": ""} for s in scores]

    # Lock status
    lock = None
    lf = FORGE_ROOT / ".forge.lock"
    if lf.exists():
        try:
            lock = json.loads(lf.read_text())
        except:
            lock = {"pid": "?", "acquired": "?"}

    dt_now = datetime.now(timezone.utc)
    hour = dt_now.hour
    peak_active = (1 <= hour < 4) or (6 <= hour < 10)
    peak_msg = ""
    if 1 <= hour < 4:
        peak_msg = f"~{(4 - hour)}h left"
    elif 6 <= hour < 10:
        peak_msg = f"~{(10 - hour)}h left"

    result = {
        "forge": forge_info,
        "pipeline": {"refinery": rn, "production": pn, "archive": an},
        "active_processes": active[:20],
        "activity": recent,
        "bp_scores": dict(sorted(bp_scores.items(), key=lambda x: -x[1].get("best", 0))[:200]),
        "forge_lock": lock,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime": int(time.time() - SERVER_START_TIME),
        "peak_hours": {
            "active": peak_active,
            "current_utc": f"{hour:02d}:00 UTC",
            "ends": peak_msg,
            "slots": "01:00–04:00 / 06:00–10:00 UTC",
        },
    }
    _result_cache = result
    _result_cache_time = now
    return result


INDEX_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Forge Command Center v2</title>
<style>
:root {
  --bg: #06060e; --surface: #0d0d1a; --border: #1a1a3a;
  --text: #c8c8d8; --text-dim: #606080; --accent: #6C6CF0;
  --green: #2ecc71; --amber: #f39c12; --red: #e74c3c; --blue: #3498db;
  --gap: 8px;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; }

/* ── Top bar ── */
.topbar {
  display: flex; align-items: center; gap: 16px;
  padding: 8px 16px; background: var(--surface);
  border-bottom: 1px solid var(--border);
  font-size: 12px; flex-shrink: 0;
}
.topbar .title { font-size: 14px; font-weight: 700; color: var(--accent); letter-spacing: 1px; }
.topbar .stat { display: flex; align-items: center; gap: 4px; }
.topbar .stat .num { font-weight: 700; font-size: 13px; }
.topbar .stat .label { color: var(--text-dim); font-size: 10px; }
.topbar .divider { width: 1px; height: 20px; background: var(--border); }
.lock-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.lock-locked { background: var(--green); animation: pulseLive 1.5s infinite; }
.lock-free { background: var(--text-dim); }
.peak-badge {
  font-size:9px; padding:1px 6px; border-radius:3px;
  letter-spacing:0.5px; font-weight:600;
}
.peak-on { background:rgba(231,76,60,0.2); color:var(--red); animation:pulseLive 1.5s infinite; }
.peak-off { background:rgba(46,204,113,0.12); color:var(--green); }
.pulse { animation: pulseLive 1.5s ease-in-out infinite; }
@keyframes pulseLive { 0%,100% { opacity: 1; } 50% { opacity: 0.4; } }

/* ── Main layout ── */
.main-wrap {
  display: flex; flex: 1; overflow: hidden;
}

/* ── Left: Activity feed ── */
.activity-panel {
  flex: 0 0 400px; display: flex; flex-direction: column;
  border-right: 1px solid var(--border); background: var(--surface);
}
.activity-header {
  padding: 8px 12px; font-size: 11px; font-weight: 600;
  border-bottom: 1px solid var(--border); color: var(--text-dim);
  flex-shrink: 0; display: flex; justify-content: space-between;
}
.activity-list { flex: 1; overflow-y: auto; padding: 4px 0; }
.activity-item {
  display: flex; align-items: flex-start; gap: 8px;
  padding: 6px 12px; border-bottom: 1px solid rgba(26,26,58,0.3);
  font-size: 11px; line-height: 1.3;
  transition: background 0.15s;
}
.activity-item:hover { background: #12122a; }
.activity-item.running { border-left: 2px solid var(--blue); }
.activity-item.complete { border-left: 2px solid var(--green); }
.activity-item.failed { border-left: 2px solid var(--red); }
.activity-icon { font-size: 12px; flex-shrink: 0; margin-top: 1px; }
.activity-body { flex: 1; min-width: 0; }
.activity-action { font-weight: 600; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
.activity-action.spawn { color: var(--accent); }
.activity-action.eval { color: var(--green); }
.activity-action.improve { color: var(--amber); }
.activity-action.loop { color: var(--blue); }
.activity-bp { font-weight: 600; }
.activity-detail { color: var(--text-dim); font-size: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.activity-time { color: var(--text-dim); font-size: 9px; flex-shrink: 0; }
.activity-progress { height: 2px; background: #1a1a3a; border-radius: 1px; margin-top: 3px; overflow: hidden; }
.activity-progress .fill { height: 100%; border-radius: 1px; background: var(--blue); transition: width 0.5s; }

/* ── Center: forge status + pipeline ── */
.center-panel {
  flex: 1; display: flex; flex-direction: column; overflow: hidden;
}
.pipeline-bar {
  display: flex; gap: 12px; padding: 10px 16px;
  border-bottom: 1px solid var(--border); background: var(--surface);
  flex-shrink: 0;
}
.pipeline-stage {
  flex: 1; padding: 8px 12px; border-radius: 6px;
  background: rgba(26,26,58,0.3); text-align: center;
  border: 1px solid var(--border);
}
.pipeline-stage .count { font-size: 20px; font-weight: 800; }
.pipeline-stage .label { font-size: 9px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; }
.pipeline-stage.refinery .count { color: var(--amber); }
.pipeline-stage.production .count { color: var(--green); }
.pipeline-stage.archive .count { color: var(--red); }

/* ── Active processes ── */
.active-section {
  padding: 8px 16px; border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.active-section .section-title { font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.active-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 6px; }
.active-card {
  padding: 6px 10px; border-radius: 4px;
  background: rgba(52,152,219,0.08); border: 1px solid rgba(52,152,219,0.2);
  font-size: 10px;
}
.active-card .ac-action { font-weight: 600; text-transform: uppercase; font-size: 9px; color: var(--blue); }
.active-card .ac-bp { font-weight: 600; font-size: 11px; }
.active-card .ac-detail { color: var(--text-dim); font-size: 9px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.active-card .ac-progress { height: 3px; background: #1a1a3a; border-radius: 2px; margin-top: 4px; overflow: hidden; }
.active-card .ac-progress .fill { height: 100%; border-radius: 2px; background: var(--blue); transition: width 1s; }

/* ── Blueprint score grid ── */
.bp-section {
  flex: 1; overflow-y: auto; padding: 8px 16px;
}
.bp-section .section-title { font-size: 10px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
.bp-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 4px; }
.bp-card {
  display: flex; align-items: center; gap: 6px;
  padding: 5px 8px; border-radius: 4px;
  font-size: 10px; border: 1px solid var(--border);
  background: rgba(13,13,26,0.5);
}
.bp-card .bp-name { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500; }
.bp-card .bp-score { font-weight: 700; font-size: 11px; min-width: 28px; text-align: right; }
.bp-card .bp-bar { flex: 0 0 50px; height: 4px; background: #1a1a3a; border-radius: 2px; overflow: hidden; }
.bp-card .bp-bar .fill { height: 100%; border-radius: 2px; transition: width 0.5s; }
.bp-card .bp-evals { font-size: 8px; color: var(--text-dim); min-width: 16px; text-align: center; }
.bp-card .bp-history { display: flex; gap: 2px; align-items: center; margin-left: 4px; }
.bp-card .bp-dot { width: 12px; height: 12px; border-radius: 2px; font-size: 7px; font-weight: 700; display: flex; align-items: center; justify-content: center; line-height: 1; }
.score-0 { color: var(--text-dim); }
.score-low { color: var(--red); }
.score-mid { color: var(--amber); }
.score-high { color: var(--green); }

/* ── Right sidebar: forge info ── */
.info-panel {
  flex: 0 0 220px; display: flex; flex-direction: column;
  border-left: 1px solid var(--border); background: var(--surface);
  font-size: 11px; padding: 12px;
  overflow-y: auto;
}
.info-section { margin-bottom: 12px; }
.info-section .info-title { font-size: 9px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.info-row { display: flex; justify-content: space-between; padding: 2px 0; }
.info-row .key { color: var(--text-dim); }
.info-row .val { font-weight: 600; }
</style>
</head>
<body>

<div class="topbar" id="topbar">
  <span class="title">⚡ FORGE CMD CTR</span>
  <span class="divider"></span>
  <span class="stat"><span class="lock-dot" id="lockDot"></span><span id="lockLabel">idle</span></span>
  <span class="stat"><span class="num" id="statLoop">-</span><span class="label">loops</span></span>
  <span class="stat"><span class="num" id="statAgents">-</span><span class="label">agents</span></span>
  <span class="stat"><span class="num" id="statEvals">-</span><span class="label">evals</span></span>
  <span class="stat"><span class="num" id="statActive">0</span><span class="label" id="activeLabel">active</span></span>
  <span style="flex:1"></span>
  <span class="stat"><span id="cavemanBadge" style="font-size:9px;padding:1px 6px;border-radius:3px;background:rgba(46,204,113,0.15);color:var(--green)">CAVEMAN ON</span></span>
  <span class="stat"><span class="peak-badge" id="peakBadge">⚡ PEAK</span></span>
  <span class="stat" style="color:var(--text-dim);font-size:10px" id="uptimeDisplay">0s</span>
</div>

<div class="main-wrap">
  <!-- Left: Activity Feed -->
  <div class="activity-panel">
    <div class="activity-header">
      <span>📡 LIVE FORGE ACTIVITY</span>
      <span id="activityCount">0</span>
    </div>
    <div class="activity-list" id="activityList"></div>
  </div>

  <!-- Center: Pipeline + Active + Scores -->
  <div class="center-panel">
    <div class="pipeline-bar" id="pipelineBar">
      <div class="pipeline-stage refinery">
        <div class="count" id="pipeRefinery">-</div>
        <div class="label">Refinery</div>
      </div>
      <div class="pipeline-stage production">
        <div class="count" id="pipeProduction">-</div>
        <div class="label">Production</div>
      </div>
      <div class="pipeline-stage archive">
        <div class="count" id="pipeArchive">-</div>
        <div class="label">Archive</div>
      </div>
    </div>

    <div class="active-section" id="activeSection">
      <div class="section-title">▶ Active Processes</div>
      <div class="active-grid" id="activeGrid">
        <div style="color:var(--text-dim);font-size:10px">No active processes</div>
      </div>
    </div>

    <div class="bp-section">
      <div class="section-title">📊 Blueprint Scores</div>
      <div class="bp-grid" id="bpGrid"></div>
    </div>
  </div>

  <!-- Right: Forge Info -->
  <div class="info-panel" id="infoPanel">
    <div class="info-section">
      <div class="info-title">Forge</div>
      <div class="info-row"><span class="key">Codename</span><span class="val" id="infoCodename">-</span></div>
      <div class="info-row"><span class="key">Version</span><span class="val" id="infoVersion">-</span></div>
      <div class="info-row"><span class="key">Checkpoint</span><span class="val" id="infoCheckpoint">-</span></div>
    </div>
    <div class="info-section">
      <div class="info-title">Pipeline</div>
      <div class="info-row"><span class="key">Total agents</span><span class="val" id="infoTotalAgents">-</span></div>
      <div class="info-row"><span class="key">Total evals</span><span class="val" id="infoTotalEvals">-</span></div>
      <div class="info-row"><span class="key">Loop iter</span><span class="val" id="infoLoopIter">-</span></div>
    </div>
    <div class="info-section">
      <div class="info-title">Lock</div>
      <div class="info-row"><span class="key">PID</span><span class="val" id="infoLockPid">-</span></div>
      <div class="info-row"><span class="key">Acquired</span><span class="val" id="infoLockTime">-</span></div>
    </div>
  </div>
</div>

<script>
let state = {};
let startTime = Date.now();

function fmtTime(ts) {
  if (!ts) return "";
  try {
    const d = new Date(ts);
    const now = Date.now();
    const diff = Math.floor((now - d.getTime()) / 1000);
    if (diff < 5) return "just now";
    if (diff < 60) return diff + "s ago";
    if (diff < 3600) return Math.floor(diff/60) + "m ago";
    return d.toLocaleTimeString();
  } catch(e) { return ts; }
}

function scoreClass(s) {
  if (!s && s !== 0) return "score-0";
  if (s >= 85) return "score-high";
  if (s >= 60) return "score-mid";
  return "score-low";
}

function barColor(s) {
  if (s >= 85) return "var(--green)";
  if (s >= 60) return "var(--amber)";
  if (s >= 30) return "var(--red)";
  return "var(--text-dim)";
}

function actionIcon(a) {
  switch(a) {
    case "spawn": return "🌱";
    case "eval": return "📊";
    case "improve": return "🔧";
    case "loop": return "🔄";
    case "promote": return "🏆";
    default: return "•";
  }
}

function render() {
  const d = state;
  if (!d) return;

  // Topbar
  const lock = d.forge_lock;
  if (lock) {
    document.getElementById("lockDot").className = "lock-dot lock-locked";
    document.getElementById("lockLabel").textContent = "forge running";
  } else {
    document.getElementById("lockDot").className = "lock-dot lock-free";
    document.getElementById("lockLabel").textContent = "idle";
  }
  document.getElementById("statLoop").textContent = d.forge?.loop_iterations || 0;
  document.getElementById("statAgents").textContent = d.forge?.total_agents || 0;
  document.getElementById("statEvals").textContent = d.forge?.total_evaluations || 0;
  const active = d.active_processes || [];
  document.getElementById("statActive").textContent = active.length;
  document.getElementById("activeLabel").textContent = active.length === 1 ? "active" : "active";
  document.getElementById("cavemanBadge").textContent = d.forge?.caveman_ultra ? "CAVEMAN ON" : "CAVEMAN OFF";
  document.getElementById("cavemanBadge").style.background = d.forge?.caveman_ultra ? "rgba(46,204,113,0.15)" : "rgba(231,76,60,0.15)";
  document.getElementById("cavemanBadge").style.color = d.forge?.caveman_ultra ? "var(--green)" : "var(--red)";
  // Peak-hours badge
  const pk = d.peak_hours || {};
  const pb = document.getElementById("peakBadge");
  if (pk.active) {
    pb.textContent = `⚡ PEAK ${pk.ends ? "— " + pk.ends : ""}`;
    pb.className = "peak-badge peak-on";
    pb.title = `DeepSeek 2x pricing! Slots: ${pk.slots || "01:00–04:00 / 06:00–10:00 UTC"}  |  Now: ${pk.current_utc || "?"}`;
  } else {
    pb.textContent = `✓ ${pk.slots ? "Off-peak" : "—"}`;
    pb.className = "peak-badge peak-off";
    pb.title = `DeepSeek off-peak. Slots: ${pk.slots || "01:00–04:00 / 06:00–10:00 UTC"}  |  Now: ${pk.current_utc || "?"}`;
  }
  document.getElementById("uptimeDisplay").textContent = Math.floor((Date.now() - startTime)/1000) + "s";

  // Pipeline
  const pipe = d.pipeline || {};
  document.getElementById("pipeRefinery").textContent = pipe.refinery || 0;
  document.getElementById("pipeProduction").textContent = pipe.production || 0;
  document.getElementById("pipeArchive").textContent = pipe.archive || 0;

  // Activity feed
  const al = document.getElementById("activityList");
  const acts = d.activity || [];
  document.getElementById("activityCount").textContent = acts.length;
  if (acts.length === 0) {
    al.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text-dim);font-size:11px">No forge activity yet</div>';
  } else {
    al.innerHTML = acts.map(a => {
      const status = a.status === "running" ? "running" : a.status === "complete" ? "complete" : "failed";
      const icon = actionIcon(a.action);
      const pct = Math.min(a.progress || 0, 100);
      return `<div class="activity-item ${status}">
        <span class="activity-icon">${icon}</span>
        <div class="activity-body">
          <div><span class="activity-action ${a.action}">${a.action}</span> <span class="activity-bp">${a.blueprint}</span></div>
          <div class="activity-detail">${a.detail || ""}</div>
          ${status === "running" ? `<div class="activity-progress"><div class="fill" style="width:${pct}%"></div></div>` : ""}
        </div>
        <span class="activity-time">${fmtTime(a.timestamp)}</span>
      </div>`;
    }).join("");
  }

  // Active processes
  const ag = document.getElementById("activeGrid");
  if (active.length === 0) {
    ag.innerHTML = '<div style="color:var(--text-dim);font-size:10px">No active processes</div>';
  } else {
    ag.innerHTML = active.map(a => {
      const pct = Math.min(a.progress || 0, 100);
      return `<div class="active-card">
        <div class="ac-action">${a.action}</div>
        <div class="ac-bp">${a.blueprint}</div>
        <div class="ac-detail">${(a.detail || "").slice(0, 50)}</div>
        <div class="ac-progress"><div class="fill" style="width:${pct}%"></div></div>
      </div>`;
    }).join("");
  }

  // Blueprint scores
  const bg = document.getElementById("bpGrid");
  const bps = d.bp_scores || {};
  const entries = Object.entries(bps).filter(([_, info]) => info.stage !== "production");
  if (entries.length === 0) {
    bg.innerHTML = '<div style="color:var(--text-dim);font-size:10px">No scores yet</div>';
  } else {
    bg.innerHTML = entries.map(([name, info]) => {
      const best = info.best || 0;
      const pct = Math.min(best, 100);
      const hist = (info.history || []).map(h => {
        const s = h.score || 0;
        return `<span class="bp-dot" style="background:${barColor(s)};color:#06060e" title="${s.toFixed(1)} @ ${h.ts} (${h.run})">${Math.round(s)}</span>`;
      }).join("");
      return `<div class="bp-card">
        <span class="bp-name">${name}</span>
        <span class="bp-evals">${info.count || 0}x</span>
        <div class="bp-bar"><div class="fill" style="width:${pct}%;background:${barColor(best)}"></div></div>
        <span class="bp-score ${scoreClass(best)}">${best.toFixed(1) || "--"}</span>
        ${hist ? `<span class="bp-history">${hist}</span>` : ""}
      </div>`;
    }).join("");
  }

  // Info panel
  const f = d.forge || {};
  document.getElementById("infoCodename").textContent = f.codename || "-";
  document.getElementById("infoVersion").textContent = f.version || "-";
  document.getElementById("infoCheckpoint").textContent = (f.last_checkpoint || "-").slice(0, 25);
  document.getElementById("infoTotalAgents").textContent = f.total_agents || 0;
  document.getElementById("infoTotalEvals").textContent = f.total_evaluations || 0;
  document.getElementById("infoLoopIter").textContent = f.loop_iterations || 0;
  document.getElementById("infoLockPid").textContent = lock?.pid || "-";
  document.getElementById("infoLockTime").textContent = lock ? (lock.acquired || "").slice(11, 19) : "-";
}

async function fetchState() {
  try {
    const r = await fetch("/api/state");
    state = await r.json();
    render();
  } catch(e) {
    // retry next tick
  }
}

// Poll every 3s
setInterval(fetchState, 3000);
fetchState();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode("utf-8"))
        elif self.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache, max-age=0")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(compute_state(), default=str).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"⚡ Forge Command Center v2 → http://localhost:{PORT}")
    print(f"   Shows ALL forge activity in real-time")
    print(f"   Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.server_close()


if __name__ == "__main__":
    main()
