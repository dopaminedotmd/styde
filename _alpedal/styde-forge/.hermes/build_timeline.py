#!/usr/bin/env python3
"""Parse FULL state.yaml — activity + agents sections — and generate interactive SVG timeline."""

import re
from datetime import datetime, timezone, timedelta
from collections import defaultdict

with open("state.yaml", "r", encoding="utf-8") as f:
    raw = f.read()

# Split into activity section and agents section
parts = raw.split("\nagents:\n", 1)
activity_section = parts[0]
agents_section = parts[1] if len(parts) > 1 else ""

# --- Parse activity section (recent events with scores) ---
activity_section = re.sub(r"^activity:\n?", "", activity_section)
items_raw = re.split(r"\n- ", activity_section.strip())
items_raw = [it.strip() for it in items_raw if it.strip()]

def parse_yaml_item(text):
    result = {}
    for line in text.split("\n"):
        line = line.strip()
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip("'")
            result[key] = val
    return result

activities = []
for item_text in items_raw:
    rec = parse_yaml_item(item_text)
    if rec.get("action") and rec.get("timestamp"):
        activities.append(rec)

# --- Parse agents section (historical registry) ---
agents_items = re.split(r"\n- ", agents_section.strip())
agents_items = [it.strip() for it in agents_items if it.strip()]

agents = []
for item_text in agents_items:
    rec = parse_yaml_item(item_text)
    bp = rec.get("blueprint", "unknown")
    run_id = rec.get("run_id", "")
    spawned_at = rec.get("spawned_at", "")
    stage = rec.get("stage", "refinery")
    status = rec.get("status", "")
    benchmark = rec.get("benchmark", "")
    iteration = rec.get("iteration", "1")
    
    if spawned_at:
        agents.append({
            "blueprint": bp,
            "timestamp": spawned_at,
            "run_id": run_id,
            "stage": stage,
            "status": status,
            "benchmark": benchmark,
        })

# --- Merge both sources into events ---
all_events = []

# Activity events (with scores, timestamps, action types)
for a in activities:
    ts_str = a.get("timestamp", "")
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except:
        continue
    bp = a.get("blueprint", "unknown")
    action = a.get("action", "")
    detail = a.get("detail", "")
    run_id = a.get("id", "0")
    
    score = None
    stage = action
    
    if action == "eval":
        cm = re.search(r"C:(\d+\.?\d*)", detail)
        if cm:
            score = float(cm.group(1))
            stage = "eval"
        else:
            stage = "eval-running"
    elif action == "spawn":
        stage = "spawn"
    elif action == "improve":
        stage = "improve"
    
    all_events.append({
        "blueprint": bp,
        "timestamp": ts,
        "score": score,
        "stage": stage,
        "detail": detail,
        "id": run_id,
    })

# Agent registry events (treat each as a spawn event)
for ag in agents:
    try:
        ts = datetime.fromisoformat(ag["timestamp"].replace("Z", "+00:00"))
    except:
        continue
    bp = ag["blueprint"]
    
    all_events.append({
        "blueprint": bp,
        "timestamp": ts,
        "score": None,
        "stage": "registry-spawn",
        "detail": f"run_id: {ag['run_id']}, stage: {ag['stage']}, benchmark: {ag.get('benchmark','')}",
        "id": ag["run_id"],
    })

# --- Organize by blueprint ---
blueprint_events = defaultdict(list)
for e in all_events:
    blueprint_events[e["blueprint"]].append(e)

for bp in blueprint_events:
    blueprint_events[bp].sort(key=lambda x: x["timestamp"])

sorted_bps = sorted(blueprint_events.keys(), key=lambda bp: blueprint_events[bp][0]["timestamp"])

all_ts = [e["timestamp"] for events in blueprint_events.values() for e in events]
t_min = min(all_ts)
t_max = max(all_ts)
t_span_secs = (t_max - t_min).total_seconds()
if t_span_secs <= 0:
    t_span_secs = 1

total_blueprints = len(sorted_bps)
total_events = len(all_events)
print(f"Blueprints: {total_blueprints}, Events: {total_events}")
print(f"Range: {t_min} - {t_max} ({t_span_secs}s)")

# --- SVG dimensions ---
BP_COUNT = total_blueprints
W = 1600
H = max(BP_COUNT * 28 + 160, 600)
if H > 12000:
    H = 12000  # cap for sanity

MARGIN_L = 250
MARGIN_R = 80
MARGIN_T = 90
MARGIN_B = 55
TRACK_H = 22
GAP = 6

plot_left = MARGIN_L
plot_right = W - MARGIN_R
plot_width = plot_right - plot_left

def ts_to_x(ts):
    frac = (ts - t_min).total_seconds() / t_span_secs
    return plot_left + frac * plot_width

def score_color(s):
    if s is None:
        return "#6b7280"
    if s >= 85:
        return "#f59e0b"
    if s >= 70:
        return "#d97706"
    return "#6b7280"

def stage_style(stage):
    styles = {
        "spawn":        (5, "#3b82f6", "#60a5fa"),
        "improve":      (4, "#8b5cf6", "#a78bfa"),
        "eval":         (6, "#f59e0b", "#fbbf24"),
        "eval-running": (4, "#6b7280", "#9ca3af"),
        "registry-spawn": (4, "#2dd4bf", "#5eead4"),
    }
    return styles.get(stage, (4, "#6b7280", "#9ca3af"))

svg_parts = []
svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" style="background:#0f172a;font-family:system-ui,sans-serif;">')

svg_parts.append("""
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="shadow">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.4"/>
    </filter>
    <linearGradient id="bg-grad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>
  </defs>
""")

svg_parts.append(f'  <rect width="{W}" height="{H}" fill="url(#bg-grad)"/>')

svg_parts.append(f'  <text x="{W//2}" y="36" text-anchor="middle" fill="#e2e8f0" font-size="22" font-weight="bold">Agent Lifecycle Timeline</text>')
svg_parts.append(f'  <text x="{W//2}" y="56" text-anchor="middle" fill="#94a3b8" font-size="13">{t_min.strftime("%b %d, %Y")} — {t_max.strftime("%b %d, %Y")} UTC</text>')

# Legend
legend_items = [
    ("#3b82f6", "Spawn (activity)"),
    ("#8b5cf6", "Improve"),
    ("#f59e0b", "Eval >=85"),
    ("#d97706", "Eval 70-84"),
    ("#6b7280", "Eval <70 / Running"),
    ("#2dd4bf", "Historical spawn"),
]
lx = plot_left
for color, label in legend_items:
    svg_parts.append(f'  <circle cx="{lx}" cy="72" r="5" fill="{color}" stroke="#1e293b" stroke-width="1"/>')
    svg_parts.append(f'  <text x="{lx + 10}" y="76" fill="#94a3b8" font-size="11">{label}</text>')
    lx += 142

# Time gridlines
tick_count = 10
for i in range(tick_count + 1):
    frac = i / tick_count
    tx = plot_left + frac * plot_width
    tick_ts = t_min + timedelta(seconds=frac * t_span_secs)
    svg_parts.append(f'  <line x1="{tx}" y1="84" x2="{tx}" y2="{H - MARGIN_B + 6}" stroke="#334155" stroke-width="1" stroke-dasharray="3,4" opacity="0.35"/>')
    svg_parts.append(f'  <text x="{tx}" y="{H - MARGIN_B + 18}" text-anchor="middle" fill="#64748b" font-size="9">{tick_ts.strftime("%b %d %H:%M")}</text>')

# Track labels (left) + guides
for i, bp in enumerate(sorted_bps):
    ty = MARGIN_T + 8 + i * (TRACK_H + GAP)
    svg_parts.append(f'  <line x1="{plot_left}" y1="{ty + TRACK_H//2}" x2="{plot_right}" y2="{ty + TRACK_H//2}" stroke="#1e293b" stroke-width="1"/>')
    label = bp[:30]
    svg_parts.append(f'  <text x="{MARGIN_L - 10}" y="{ty + TRACK_H//2 + 4}" text-anchor="end" fill="#cbd5e1" font-size="10" font-weight="500">{label}</text>')

# Event data for JS
detail_popups = []

for i, bp in enumerate(sorted_bps):
    ty = MARGIN_T + 8 + i * (TRACK_H + GAP)
    events = blueprint_events[bp]
    
    # Connecting line
    first_x = ts_to_x(events[0]["timestamp"])
    last_x = ts_to_x(events[-1]["timestamp"])
    svg_parts.append(f'  <line x1="{first_x}" y1="{ty + TRACK_H//2}" x2="{last_x}" y2="{ty + TRACK_H//2}" stroke="#334155" stroke-width="1.5" stroke-linecap="round"/>')
    
    for j, e in enumerate(events):
        cx = ts_to_x(e["timestamp"])
        cy = ty + TRACK_H // 2
        
        r, fill, stroke = stage_style(e["stage"])
        
        # Score-based color override for eval
        if e["stage"] == "eval" and e["score"] is not None:
            fill = score_color(e["score"])
            stroke = "#fbbf24" if e["score"] >= 85 else ("#f59e0b" if e["score"] >= 70 else "#9ca3af")
        
        glow = ' filter="url(#glow)"' if (e.get("score") is not None and e["score"] >= 85) else ""
        svg_parts.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2"{glow} class="node" data-idx="{i}" data-event="{j}" style="cursor:pointer;"/>')
        
        score_str = f"{e['score']:.1f}" if e.get("score") is not None else "N/A"
        detail_popups.append(
            f'{{idx:{i},ev:{j},bp:"{bp}",score:"{score_str}",stage:"{e["stage"]}",'
            f'detail:"{e.get("detail","")[:50]}",ts:"{e["timestamp"].strftime("%Y-%m-%d %H:%M")}",id:"{e.get("id","")}"}}'
        )

# Scrubber + Play button
scrubber_y = H - MARGIN_B + 30
svg_parts.append(f'  <text x="{plot_left}" y="{scrubber_y - 8}" fill="#94a3b8" font-size="11">Time scrubber</text>')
svg_parts.append(f'  <rect x="{plot_left}" y="{scrubber_y}" width="{plot_width}" height="6" rx="3" fill="#334155"/>')
svg_parts.append(f'  <rect x="{plot_left}" y="{scrubber_y}" width="0" height="6" rx="3" fill="#f59e0b" id="scrubber-progress"/>')
svg_parts.append(f'  <circle cx="{plot_left}" cy="{scrubber_y + 3}" r="8" fill="#f59e0b" stroke="#fbbf24" stroke-width="2" id="scrubber-handle" style="cursor:ew-resize;"/>')
svg_parts.append(f'  <text x="{plot_left}" y="{scrubber_y + 24}" fill="#64748b" font-size="10" id="scrubber-label">Drag scrubber or press Play</text>')
svg_parts.append(f'  <rect x="{plot_right + 10}" y="{scrubber_y - 4}" width="60" height="22" rx="4" fill="#1e293b" stroke="#334155" stroke-width="1" id="play-btn" style="cursor:pointer;"/>')
svg_parts.append(f'  <text x="{plot_right + 40}" y="{scrubber_y + 10}" text-anchor="middle" fill="#e2e8f0" font-size="11" id="play-label">\u25B6 Play</text>')

# Tooltip (hidden)
svg_parts.append(f'  <rect x="0" y="0" width="340" height="155" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1" id="popup-bg" visibility="hidden"/>')
svg_parts.append(f'  <text x="0" y="0" fill="#e2e8f0" font-size="13" font-weight="bold" id="popup-title" visibility="hidden">-</text>')
for off, key in [(42,"line1"),(60,"line2"),(78,"line3"),(96,"line4")]:
    svg_parts.append(f'  <text x="0" y="0" fill="#94a3b8" font-size="11" id="popup-{key}" visibility="hidden">-</text>')

# Summary footer
top_scores = sorted(
    [(e["score"], e["blueprint"], e["timestamp"]) for events in blueprint_events.values() for e in events if e.get("score") is not None],
    reverse=True
)[:5]

svg_parts.append(f'  <text x="{plot_left}" y="{H - 10}" fill="#64748b" font-size="10">{total_blueprints} blueprints | {total_events} events | Top scores:')
for s, bp, ts in top_scores:
    svg_parts.append(f'  <text x="{plot_left + 200}" y="{H - 10}" fill="#64748b" font-size="10">{s:.1f} {bp}</text>')

# JavaScript
js_data = ",\n    ".join(detail_popups)
svg_parts.append(f"""
  <script type="text/javascript"><![CDATA[
    var eventsData = [
    {js_data}
    ];
    var totalDuration = {t_span_secs};
    var isPlaying = false;
    var playInterval = null;
    var currentFrac = 0;

    function showPopup(evt, idx, eventIdx) {{
        var d = eventsData.filter(function(e) {{ return e.idx === idx && e.ev === eventIdx; }})[0];
        if (!d) return;
        var bg = document.getElementById('popup-bg');
        var title = document.getElementById('popup-title');
        var lines = ['popup-line1','popup-line2','popup-line3','popup-line4'];
        var x = Math.min(evt.clientX + 12, {W} - 350);
        var y = Math.min(evt.clientY - 60, {H} - 175);
        bg.setAttribute('x', x); bg.setAttribute('y', y); bg.setAttribute('visibility', 'visible');
        title.setAttribute('x', x + 14); title.setAttribute('y', y + 22);
        title.textContent = d.bp; title.setAttribute('visibility', 'visible');
        var texts = ['Stage: ' + d.stage, 'Score: ' + d.score, 'Time: ' + d.ts, 'Run: ' + d.id];
        for (var k = 0; k < 4; k++) {{
            var el = document.getElementById(lines[k]);
            el.setAttribute('x', x + 14); el.setAttribute('y', y + 42 + k*18);
            el.textContent = texts[k]; el.setAttribute('visibility', 'visible');
        }}
    }}

    function hidePopup() {{
        document.getElementById('popup-bg').setAttribute('visibility', 'hidden');
        ['popup-title','popup-line1','popup-line2','popup-line3','popup-line4'].forEach(function(id) {{
            document.getElementById(id).setAttribute('visibility', 'hidden');
        }});
    }}

    document.querySelectorAll('.node').forEach(function(n) {{
        n.addEventListener('click', function(evt) {{ showPopup(evt, parseInt(this.dataset.idx), parseInt(this.dataset.event)); }});
    }});
    document.addEventListener('click', function(evt) {{
        if (!evt.target.classList.contains('node')) hidePopup();
    }});

    var scrubberHandle = document.getElementById('scrubber-handle');
    var scrubberProgress = document.getElementById('scrubber-progress');
    var scrubberLabel = document.getElementById('scrubber-label');
    var isDragging = false;
    var plotLeft = {plot_left};
    var plotWidth = {plot_width};

    function updateScrubber(frac) {{
        currentFrac = Math.max(0, Math.min(1, frac));
        var x = plotLeft + currentFrac * plotWidth;
        scrubberHandle.setAttribute('cx', x);
        scrubberProgress.setAttribute('width', currentFrac * plotWidth);
        var totalSecs = Math.round(currentFrac * totalDuration);
        var mins = Math.floor(totalSecs / 60);
        var secs = totalSecs % 60;
        var days = Math.floor(mins / 1440);
        mins = mins % 1440;
        var h = Math.floor(mins / 60);
        mins = mins % 60;
        scrubberLabel.textContent = (days ? days + 'd ' : '') + (h < 10 ? '0' : '') + h + ':' + (mins < 10 ? '0' : '') + mins + ':' + (secs < 10 ? '0' : '') + secs;
    }}

    scrubberHandle.addEventListener('mousedown', function(evt) {{ isDragging = true; evt.preventDefault(); }});
    document.addEventListener('mousemove', function(evt) {{
        if (!isDragging) return;
        var rect = document.querySelector('svg').getBoundingClientRect();
        var frac = (evt.clientX - rect.left - plotLeft) / plotWidth;
        updateScrubber(frac);
    }});
    document.addEventListener('mouseup', function() {{ isDragging = false; }});

    document.getElementById('play-btn').addEventListener('click', function() {{
        if (isPlaying) {{
            clearInterval(playInterval);
            isPlaying = false;
            document.getElementById('play-label').textContent = '\\u25B6 Play';
        }} else {{
            isPlaying = true;
            document.getElementById('play-label').textContent = '\\u23F8 Pause';
            playInterval = setInterval(function() {{
                if (currentFrac >= 1) {{
                    clearInterval(playInterval);
                    isPlaying = false;
                    document.getElementById('play-label').textContent = '\\u25B6 Play';
                    updateScrubber(0);
                    return;
                }}
                updateScrubber(currentFrac + 0.003);
            }}, 100);
        }}
    }});
  ]]></script>""")

svg_parts.append('</svg>')

svg_content = "\n".join(svg_parts)
out_path = "E:/Stryde/_alpedal/styde-forge/outputs/agent-lifecycle-timeline.svg"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"SVG: {out_path}")
print(f"  {len(svg_content)} bytes")
print(f"  {total_blueprints} blueprints | {total_events} events")
print(f"  Range: {t_min.strftime('%Y-%m-%d %H:%M:%S')} -> {t_max.strftime('%Y-%m-%d %H:%M:%S')} ({t_span_secs:.0f}s)")
print(f"  Height: {H}px")
print(f"\nTop 5 scores:")
for s, bp, ts in top_scores:
    print(f"  {s:.1f}  {bp}")
