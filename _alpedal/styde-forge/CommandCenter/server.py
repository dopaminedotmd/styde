"""
Forge Command Center v1 — Live control panel for 46 blueprints × 10 subagents
Port 8766 (kept separate from dashboard port 8765)

Endpoints:
  GET /  -> index.html (dashboard)
  GET /api/state  -> JSON blueprint scores + activity + subagent state
"""
import sys
import os
import json
import yaml
import glob
import time
import math
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone

FORGE_ROOT = Path("D:/styde/_alpedal/styde-forge")
STATE_FILE = FORGE_ROOT / "state.yaml"
BP_DIR = FORGE_ROOT / "StydeAgents" / "blueprints"
REFINERY_DIR = FORGE_ROOT / "StydeAgents" / "refinery"
PRODUCTION_DIR = FORGE_ROOT / "StydeAgents" / "production"

PORT = 8766

# Priority tiers (matching bp-order.md)
TIERS = {
    "General": {
        "bps": [
            "mockup-to-code-converter", "desktop-native-ui-engineer",
            "data-migration-simulator", "secrets-hardening-auditor",
            "documentation-generator", "orchestration-workflow-builder",
            "caveman-mode-enforcer"
        ],
        "target": 85
    },
    "Fas 0.5": {
        "bps": [
            "desktop-mockup-artist", "web-mockup-artist", "mockup-comparison-curator",
            "neo-brutalist-dashboard-designer", "glass-spatial-interface-designer",
            "editorial-minimal-dashboard-designer", "data-dense-ops-center-designer",
            "organic-fluid-dashboard-designer", "holographic-futurist-designer",
            "clay-soft-interface-designer", "bento-grid-dashboard-architect",
            "terminal-purist-designer", "magazine-cover-dashboard-designer",
            "html-mockup-engineer", "tauri-window-composer", "styde-se-site-integrator",
            "dashboard-system-overview-specialist", "agent-status-panel-designer",
            "activity-feed-designer", "gpu-monitor-visualizer",
            "color-palette-originator", "design-review-critic", "mockup-diversity-enforcer"
        ],
        "target": 85
    },
    "Fas 1": {
        "bps": [
            "bug-hunter-core", "rate-limiting-engineer", "git-hygiene-specialist"
        ],
        "target": 85
    },
    "Fas 1.5": {
        "bps": ["state-migration-engineer"],
        "target": 85
    },
    "Fas 2": {
        "bps": ["code-refactoring-specialist", "prompt-injection-defender"],
        "target": 85
    },
    "Fas 2.5": {
        "bps": ["test-coverage-engineer"],
        "target": 85
    },
    "Fas 3": {
        "bps": ["dashboard-auth-specialist", "wcag-accessibility-engineer"],
        "target": 85
    },
    "Fas 4": {
        "bps": ["pipeline-automation-engineer", "anomaly-detection-specialist"],
        "target": 85
    },
    "Fas 5": {
        "bps": ["hybrid-agent-creator", "agent-promotion-evaluator"],
        "target": 85
    },
    "Fas 6": {
        "bps": ["performance-profiler", "memory-leak-diagnostician", "production-hardening-engineer"],
        "target": 85
    },
}

# Subagent status tracking
SUBAGENTS = {}
for i, (tier, info) in enumerate(TIERS.items()):
    SUBAGENTS[tier] = {
        "id": i + 1,
        "status": "pending",
        "current_bp": "",
        "progress": 0,
        "started_at": None,
        "finished_at": None,
        "error": None,
    }

def load_state():
    """Load and parse state.yaml"""
    try:
        if STATE_FILE.exists():
            data = yaml.safe_load(STATE_FILE.read_text(encoding="utf-8"))
            return data if data else {}
    except Exception as e:
        return {}
    return {}

def parse_scores(state):
    """Parse agent scores from state"""
    agents = state.get("agents", [])
    if not isinstance(agents, list):
        agents = []
    
    bp_scores = {}
    for a in agents:
        bp = a.get("blueprint", "")
        score = a.get("composite_score")
        stage = a.get("stage", "refinery")
        run_id = a.get("run_id", "")
        iteration = a.get("iteration", 0)
        if bp:
            if bp not in bp_scores:
                bp_scores[bp] = {"scores": [], "stage": stage, "run_id": run_id}
            if score is not None:
                bp_scores[bp]["scores"].append(score)
                bp_scores[bp]["stage"] = stage
                bp_scores[bp]["run_id"] = run_id
                bp_scores[bp]["iteration"] = iteration
    
    # Get best and latest scores
    result = {}
    for bp, info in bp_scores.items():
        s = info["scores"]
        result[bp] = {
            "best": max(s) if s else None,
            "latest": s[-1] if s else None,
            "avg": round(sum(s) / len(s), 1) if s else None,
            "count": len(s),
            "stage": info["stage"],
            "run_id": info.get("run_id", ""),
            "iteration": info.get("iteration", 0),
        }
    return result

def get_progress(bp_name, bp_scores, target=85):
    """Calculate XP progress 0-100 toward target"""
    info = bp_scores.get(bp_name, {})
    latest = info.get("latest") or info.get("best") or 0
    if latest >= target:
        return 100
    return round((latest / target) * 100, 1)

def get_bp_dir_info(bp_name):
    """Check dirs for run output existence"""
    bp_dir = BP_DIR / bp_name
    refinery_dir = REFINERY_DIR / bp_name
    prod_dir = PRODUCTION_DIR / bp_name
    
    runs = []
    if refinery_dir.exists():
        for r in sorted(refinery_dir.glob("runs/*"), reverse=True)[:5]:
            runs.append(r.name)
    
    return {
        "has_blueprint": bp_dir.exists() and (bp_dir / "BLUEPRINT.md").exists(),
        "in_refinery": refinery_dir.exists(),
        "in_production": prod_dir.exists(),
        "recent_runs": runs,
    }

def check_forge_lock():
    """Check if forge is currently running"""
    lock_file = FORGE_ROOT / ".forge.lock"
    if lock_file.exists():
        try:
            data = json.loads(lock_file.read_text(encoding="utf-8"))
            return data
        except:
            return None
    return None

def get_activity_cascade(state):
    """Get recent activity entries"""
    activity = state.get("activity", [])
    if isinstance(activity, list):
        return activity[-30:]
    return []

# ── Real-time forge log parser ────────────────────────────────────
import re

FORGE_LOG_PATTERN = re.compile(
    r"\[([^\]]+)\]\s+Self:\s*(\d+)\s+Judge:\s*(\d+)\s+Composite:\s*([\d.]+)"
)

def find_latest_forge_log():
    """Find the most recently modified forge batch log file."""
    logs = sorted(FORGE_ROOT.glob("forge_batch*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    if logs:
        return logs[0]
    # fallback to any forge log
    logs = sorted(FORGE_ROOT.glob("forge_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    return logs[0] if logs else None

def parse_forge_log_scores(log_path=None):
    """Parse eval scores from forge log file(s). 
    If log_path is None, reads ALL forge_batch*.log files and merges.
    Returns {bp_name: {self, judge, composite}}"""
    all_scores = {}
    pattern = re.compile(
        r"\[([^\]]+)\]\s+Self:\s*(\d+)\s+Judge:\s*(\d+)\s+Composite:\s*([\d.]+)"
    )
    
    if log_path:
        logs = [log_path] if log_path.exists() else []
    else:
        # Read ALL batch logs, keep latest score per BP across all
        logs = sorted(FORGE_ROOT.glob("forge_batch*.log"), 
                      key=lambda p: p.stat().st_mtime, reverse=True)
        if not logs:
            logs = sorted(FORGE_ROOT.glob("forge_*.log"),
                          key=lambda p: p.stat().st_mtime, reverse=True)
    
    for lp in logs:
        try:
            text = lp.read_text(encoding="utf-8", errors="replace")
            for match in pattern.finditer(text):
                bp = match.group(1).strip()
                self_s = int(match.group(2))
                judge_s = int(match.group(3))
                comp = float(match.group(4))
                # Keep latest composite per blueprint across ALL logs
                if bp not in all_scores or True:  # always overwrite with newest log match
                    all_scores[bp] = {"self": self_s, "judge": judge_s, "composite": comp, "source": "log_live"}
        except Exception:
            pass
    return all_scores

def merge_live_scores(bp_scores_from_state, state=None):
    """Merge real-time forge log scores into state.yaml scores.
    Also parses activity detail strings from state as fallback.
    Live scores REPLACE stale state data for blueprints currently in training."""
    result = dict(bp_scores_from_state)
    
    # 1. Parse activity entries from state.yaml (detail: "S:XX J:XX C:XX.X")
    if state:
        activity = state.get("activity", [])
        if isinstance(activity, list):
            act_pat = re.compile(r"S:(\d+)\s+J:(\d+)\s+C:([\d.]+)")
            for entry in activity:
                bp = entry.get("blueprint", "")
                detail = entry.get("detail", "")
                m = act_pat.search(detail)
                if m and bp:
                    c = float(m.group(3))
                    existing = result.get(bp, {})
                    best = existing.get("best", 0) or 0
                    result[bp] = {
                        "best": max(c, best),
                        "latest": c,
                        "avg": c,
                        "count": (existing.get("count", 0) or 0) + 1,
                        "stage": existing.get("stage", "refinery"),
                        "run_id": "ACTIVITY",
                        "iteration": 0,
                        "live": False,
                        "self": int(m.group(1)),
                        "judge": int(m.group(2)),
                    }
    
    # 2. Override with live forge log scores (more current)
    live = parse_forge_log_scores()
    for bp, ls in live.items():
        c = ls["composite"]
        existing = result.get(bp, {})
        best = existing.get("best", 0) or 0
        result[bp] = {
            "best": max(c, best),
            "latest": c,
            "avg": c,
            "count": (existing.get("count", 0) or 0) + 1,
            "stage": "refinery",
            "run_id": "LIVE",
            "iteration": 0,
            "live": True,
            "self": ls["self"],
            "judge": ls["judge"],
        }
    return result

def get_tier_stats(tier_name, tier_info, bp_scores):
    """Get aggregate stats for a tier"""
    bps = tier_info["bps"]
    scores = []
    target = tier_info["target"]
    
    for bp in bps:
        info = bp_scores.get(bp, {})
        latest = info.get("latest") or info.get("best") or 0
        stage = info.get("stage", "not_started")
        count = info.get("count", 0)
        scores.append({
            "name": bp,
            "score": latest,
            "best": info.get("best") or 0,
            "target": target,
            "stage": stage,
            "eval_count": count,
            "live": info.get("live", False),
            "progress": get_progress(bp, bp_scores, target),
        })
    
    avg = sum(s["score"] for s in scores if s["score"]) / max(len(scores), 1)
    highest = max((s["score"] for s in scores if s["score"]), default=0)
    passed = sum(1 for s in scores if s["score"] >= target)
    
    return {
        "tier": tier_name,
        "total": len(bps),
        "passed": passed,
        "avg_score": round(avg, 1),
        "highest": round(highest, 1),
        "agents": scores,
        "subagent": SUBAGENTS.get(tier_name, {}),
    }


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Forge Command Center</title>
<style>
:root {
  --bg: #06060e;
  --surface: #0d0d1a;
  --border: #1a1a3a;
  --text: #c8c8d8;
  --text-dim: #606080;
  --accent: #6C6CF0;
  --accent2: #9B6DFF;
  --green: #2ecc71;
  --amber: #f39c12;
  --red: #e74c3c;
  --blue: #3498db;
  --gap: 12px;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); height: 100vh; display: flex; }
.sidebar {
  width: 340px; min-width: 340px;
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  height: 100vh;
}
.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(180deg, #0d0d1a 0%, #080816 100%);
}
.sidebar-header h1 { font-size: 16px; color: var(--accent); letter-spacing: 1px; }
.sidebar-header .sub { font-size: 11px; color: var(--text-dim); margin-top: 2px; }
.sidebar-search {
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}
.sidebar-search input {
  width: 100%; padding: 8px 12px;
  background: #111128; border: 1px solid var(--border);
  color: var(--text); border-radius: 6px;
  font-size: 12px; outline: none;
}
.sidebar-search input:focus { border-color: var(--accent); }
.sidebar-list {
  flex: 1; overflow-y: auto;
  padding: 8px 0;
}
.agent-card {
  padding: 10px 16px; cursor: pointer;
  border-bottom: 1px solid rgba(26,26,58,0.5);
  transition: background 0.2s;
}
.agent-card:hover { background: #12122a; }
.agent-card .name { font-size: 12px; font-weight: 600; }
.agent-card .name .tier-badge {
  display: inline-block; font-size: 9px; padding: 1px 6px;
  border-radius: 3px; margin-left: 6px;
  color: #fff; font-weight: 500;
}
.agent-card .meta { display: flex; justify-content: space-between; margin-top: 4px; }
.agent-card .meta .score { font-size: 13px; font-weight: 700; }
.agent-card .meta .stage { font-size: 10px; padding: 1px 6px; border-radius: 3px; }
.agent-card .xp-bar { margin-top: 6px; height: 4px; background: #1a1a3a; border-radius: 2px; overflow: hidden; }
.agent-card .xp-bar .fill { height: 100%; border-radius: 2px; transition: width 0.5s ease; }
.stage-not_started { color: var(--text-dim); background: rgba(255,255,255,0.05); }
.stage-refinery { color: var(--amber); background: rgba(243,156,18,0.15); }
.stage-production { color: var(--green); background: rgba(46,204,113,0.15); }
.stage-archive { color: var(--red); background: rgba(231,76,60,0.15); }
.score-none { color: var(--text-dim); }
.score-low { color: var(--red); }
.score-mid { color: var(--amber); }
.score-high { color: var(--green); }
.score-90 { color: var(--accent); }

.main {
  flex: 1; display: flex; flex-direction: column;
  height: 100vh; overflow: hidden;
}
.main-header {
  padding: 12px 24px;
  border-bottom: 1px solid var(--border);
  background: var(--surface);
  display: flex; justify-content: space-between; align-items: center;
}
.main-header h2 { font-size: 14px; color: var(--accent); }
.main-header .status-bar { display: flex; gap: 20px; font-size: 11px; }
.main-header .status-bar .stat { text-align: center; }
.main-header .status-bar .stat .num { font-size: 18px; font-weight: 700; display: block; }
.main-header .status-bar .stat .label { color: var(--text-dim); }
.main-content {
  flex: 1; overflow-y: auto; padding: 20px;
  display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--gap);
}
.main-content.full-col { grid-template-columns: 1fr; }
@media (max-width: 1200px) { .main-content { grid-template-columns: 1fr; } }
.tier-panel {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; overflow: hidden;
}
.tier-header {
  padding: 12px 16px;
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid var(--border);
  background: linear-gradient(90deg, rgba(108,108,240,0.05) 0%, transparent 100%);
}
.tier-header .tier-name { font-size: 13px; font-weight: 600; }
.tier-header .tier-stats { font-size: 11px; color: var(--text-dim); }
.tier-header .tier-target { font-size: 10px; color: var(--accent); }
.subagent-badge {
  font-size: 10px; padding: 2px 8px; border-radius: 10px;
  background: rgba(108,108,240,0.15); color: var(--accent);
  border: 1px solid rgba(108,108,240,0.3);
}
.subagent-status {
  font-size: 10px; padding: 2px 8px; border-radius: 10px;
}
.subagent-running { background: rgba(52,152,219,0.15); color: var(--blue); border: 1px solid rgba(52,152,219,0.3); }
.subagent-done { background: rgba(46,204,113,0.15); color: var(--green); border: 1px solid rgba(46,204,113,0.3); }
.subagent-pending { background: rgba(255,255,255,0.05); color: var(--text-dim); border: 1px solid var(--border); }
.tier-agents {
  padding: 8px;
}
.tier-agent {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 8px; border-radius: 6px;
  margin-bottom: 4px; cursor: default;
  transition: background 0.2s;
}
.tier-agent:hover { background: #12122a; }
.tier-agent .ta-name { flex: 1; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tier-agent .ta-score { font-size: 11px; font-weight: 700; min-width: 36px; text-align: right; }
.tier-agent .ta-target { font-size: 10px; color: var(--text-dim); min-width: 24px; text-align: right; }
.tier-agent .ta-bar { flex: 0 0 80px; height: 6px; background: #1a1a3a; border-radius: 3px; overflow: hidden; }
.tier-agent .ta-bar .fill { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.tier-agent .ta-evals { font-size: 9px; color: var(--text-dim); min-width: 20px; text-align: center; }
.countdown-timer {
  font-family: 'Cascadia Code', 'Fira Code', monospace;
  font-size: 10px; padding: 2px 6px;
  border-radius: 4px; background: rgba(0,0,0,0.3);
}
.countdown-active { color: var(--amber); }
.countdown-done { color: var(--green); }
.run-num {
  font-size: 9px; color: var(--text-dim);
  background: rgba(255,255,255,0.05);
  padding: 1px 5px; border-radius: 3px;
}
.live-badge {
  font-size: 9px; padding: 1px 6px;
  border-radius: 3px;
  background: rgba(46,204,113,0.2);
  color: var(--green);
  border: 1px solid rgba(46,204,113,0.4);
  animation: pulseLive 1.5s ease-in-out infinite;
  white-space: nowrap;
}
@keyframes pulseLive {
  0%,100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.flash-green { animation: flashGreen 0.6s ease; }
@keyframes flashGreen { 0%,100% { background: transparent; } 50% { background: rgba(46,204,113,0.2); } }
</style>
</head>
<body>
<div class="sidebar" id="sidebar">
  <div class="sidebar-header">
    <h1>⚡ FORGE CMD CTR</h1>
    <div class="sub">46 agents · 10 subagents · Caveman Ultra</div>
  </div>
  <div class="sidebar-search">
    <input type="text" id="search" placeholder="Search agent..." oninput="filterAgents()">
  </div>
  <div class="sidebar-list" id="agentList"></div>
</div>
<div class="main">
  <div class="main-header">
    <h2 id="headerTitle">■ Mission Overview</h2>
    <div class="status-bar" id="statusBar"></div>
  </div>
  <div class="main-content" id="mainContent"></div>
</div>
<script>
const TIERS = ["General", "Fas 0.5", "Fas 1", "Fas 1.5", "Fas 2", "Fas 2.5", "Fas 3", "Fas 4", "Fas 5", "Fas 6"];
const TIER_COLORS = ["#6C6CF0", "#9B6DFF", "#3498db", "#2ecc71", "#f39c12", "#e74c3c", "#1abc9c", "#e67e22", "#9b59b6", "#34495e"];

let state = { bp_scores: {}, tiers: [], totals: {} };
let updates = {};
let startTime = Date.now();

function fmtTime(ts) {
  if (!ts) return "--:--:--";
  const d = new Date(ts);
  return d.toLocaleTimeString();
}

function tierColor(i) { return TIER_COLORS[i % TIER_COLORS.length]; }

function scoreClass(s, target) {
  if (!s && s !== 0) return 'score-none';
  if (s >= 95) return 'score-90';
  if (s >= target) return 'score-high';
  if (s >= target * 0.7) return 'score-mid';
  return 'score-low';
}

function formatCountdown(start, elapsed) {
  if (!start) return { text: "--:--", active: false };
  const startMs = new Date(start).getTime();
  const now = Date.now();
  const diff = Math.max(0, now - startMs);
  const mins = Math.floor(diff/60000);
  const secs = Math.floor((diff%60000)/1000);
  return {
    text: `${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`,
    active: diff > 0
  };
}

function render() {
  const data = state;
  const bp = data.bp_scores || {};
  const tiers = data.tiers || {};
  const totals = data.totals || {};
  
  // Status bar
  const sb = document.getElementById('statusBar');
  sb.innerHTML = [
    `<div class="stat"><span class="num">${totals.total||0}</span><span class="label">Total</span></div>`,
    `<div class="stat"><span class="num" style="color:var(--green)">${totals.production||0}</span><span class="label">Production</span></div>`,
    `<div class="stat"><span class="num" style="color:var(--amber)">${totals.refinery||0}</span><span class="label">Refinery</span></div>`,
    `<div class="stat"><span class="num" style="color:var(--accent)">${totals.passed_target||0}</span><span class="label">At Target</span></div>`,
    `<div class="stat"><span class="num" style="color:var(--text)">${totals.avg_all||'--'}</span><span class="label">Avg Score</span></div>`,
  ].join('');
  
  // Sidebar
  const al = document.getElementById('agentList');
  const search = document.getElementById('search').value.toLowerCase();
  let rows = [];
  for (const tier of TIERS) {
    const t = tiers[tier];
    if (!t) continue;
    for (const a of t.agents || []) {
      if (search && !a.name.includes(search)) continue;
      const s = a.score || 0;
      const p = Math.min(a.progress || 0, 100);
      const sc = scoreClass(a.score, a.target);
      rows.push(`<div class="agent-card" onclick="scrollToTier('${tier}')">
        <div class="name">${a.name}<span class="tier-badge" style="background:${tierColor(TIERS.indexOf(tier))}">${tier}</span></div>
        <div class="meta">
          <span class="score ${sc}">${a.score != null ? a.score.toFixed(1) : '--'}</span>
          <span class="stage stage-${a.stage || 'not_started'}">${a.stage || 'not_started'}</span>
        </div>
        <div class="xp-bar"><div class="fill" style="width:${p}%;background:${a.score >= a.target ? 'var(--green)' : a.score >= a.target*0.7 ? 'var(--amber)' : 'var(--accent)'}"></div></div>
        <div style="display:flex;justify-content:space-between;font-size:9px;color:var(--text-dim);margin-top:2px">
          <span>${a.eval_count||0} evals</span>
          <span>target: ${a.target}</span>
        </div>
      </div>`);
    }
  }
  al.innerHTML = rows.join('');
  
  // Main content - tier panels
  const mc = document.getElementById('mainContent');
  let panels = [];
  for (let i = 0; i < TIERS.length; i++) {
    const tier = TIERS[i];
    const t = tiers[tier];
    if (!t) continue;
    const color = tierColor(i);
    const sub = t.subagent || {};
    const subStatus = sub.status || 'pending';
    const subLabel = subStatus === 'running' ? '▶ Running' : subStatus === 'done' ? '✓ Done' : '○ Pending';
    const subClass = subStatus === 'running' ? 'subagent-running' : subStatus === 'done' ? 'subagent-done' : 'subagent-pending';
    
    const agents = (t.agents || []).map(a => {
      const p = Math.min(a.progress || 0, 100);
      const sc = scoreClass(a.score, a.target);
      const c = a.score >= a.target ? 'var(--green)' : a.score >= a.target*0.7 ? 'var(--amber)' : color;
      const liveTag = a.live ? '<span class="live-badge">● LIVE</span>' : '';
      return `<div class="tier-agent">
        <span class="ta-name">${a.name}</span>
        <span class="ta-evals">${a.eval_count||0}x</span>
        <div class="ta-bar"><div class="fill" style="width:${p}%;background:${c}"></div></div>
        <span class="ta-score ${sc}">${a.score != null ? a.score.toFixed(1) : '--'}</span>
        <span class="ta-target">/${a.target}</span>
        ${liveTag}
      </div>`;
    }).join('');
    
    const pct = t.total > 0 ? Math.round(t.passed / t.total * 100) : 0;
    
    panels.push(`<div class="tier-panel" id="tier-${tier.replace(/\s/g,'')}">
      <div class="tier-header" style="border-left: 3px solid ${color}">
        <div>
          <div class="tier-name" style="color:${color}">Subagent ${i+1} · ${tier}</div>
          <div class="tier-stats">${t.passed}/${t.total} passed · avg ${t.avg_score} · best ${t.highest}</div>
        </div>
        <div style="text-align:right">
          <span class="subagent-badge">SA-${String(i+1).padStart(2,'0')}</span>
          <span class="subagent-status ${subClass}">${subLabel}</span>
          <div class="tier-target" style="margin-top:4px">Target: ${t.agents?.[0]?.target || 85} × 3 evals</div>
        </div>
      </div>
      <div class="tier-agents">${agents}</div>
    </div>`);
  }
  mc.innerHTML = panels.join('');
}

function scrollToTier(tier) {
  const el = document.getElementById('tier-' + tier.replace(/\s/g,''));
  if (el) el.scrollIntoView({behavior:'smooth', block:'start'});
}

function filterAgents() {
  render();
}

async function fetchState() {
  try {
    const r = await fetch('/api/state');
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
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(INDEX_HTML.encode('utf-8'))
        elif self.path == '/api/state':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            state = load_state()
            bp_scores = merge_live_scores(parse_scores(state), state)
            
            # Build tier data
            tiers = {}
            all_scores = []
            total_bps = 0
            in_production = 0
            in_refinery = 0
            passed_target = 0
            
            for tier_name, tier_info in TIERS.items():
                stats = get_tier_stats(tier_name, tier_info, bp_scores)
                tiers[tier_name] = stats
                for a in stats["agents"]:
                    total_bps += 1
                    if a["score"] and a["score"] > 0:
                        all_scores.append(a["score"])
                    if a["stage"] == "production":
                        in_production += 1
                    elif a["stage"] == "refinery":
                        in_refinery += 1
                    if a["score"] and a["score"] >= a["target"]:
                        passed_target += 1
            
            # Check forge lock
            lock = check_forge_lock()
            
            # Get recent activity
            activity = get_activity_cascade(state)
            
            data = {
                "bp_scores": bp_scores,
                "tiers": tiers,
                "totals": {
                    "total": total_bps,
                    "production": in_production,
                    "refinery": in_refinery,
                    "passed_target": passed_target,
                    "avg_all": round(sum(all_scores) / len(all_scores), 1) if all_scores else 0,
                },
                "forge_lock": lock,
                "activity": activity[-20:],
                "uptime": int(time.time() - start_time),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            
            self.wfile.write(json.dumps(data, default=str).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # suppress default logging

def main():
    global start_time
    start_time = time.time()
    
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"⚡ Forge Command Center → http://localhost:{PORT}")
    print(f"   46 agents · 10 subagent tiers · probing state.yaml")
    print(f"   Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.server_close()

if __name__ == '__main__':
    main()
