import type { DashboardState, GPUData, ActivityItem, SkillData, EvalData, ForgeData } from "./state.js";

// ── DOM helpers ──
export function t(id: string, v: string | number | boolean): void {
  const e = document.getElementById(id);
  const str = String(v);
  if (e && e.textContent !== str) e.textContent = str;
}

export function tw(id: string, pct: number): void {
  const e = document.getElementById(id);
  if (e) e.style.width = pct + "%";
}

// ── Color helpers ──
export function scoreClr(s: number | null | undefined): string {
  if (s == null) return "var(--t3)";
  if (s >= 85) return "var(--emerald)";
  if (s >= 70) return "var(--amber)";
  if (s >= 50) return "var(--t2)";
  return "var(--t3)";
}

export function dotStage(stage: string | undefined): string {
  if (stage === "production") return "var(--emerald)";
  if (stage === "archive") return "var(--t4)";
  return "var(--amber)";
}

// ── GPU Gauge SVG ──
const GR = 22;
const GC = 2 * Math.PI * GR;

export function gaugeSvg(temp: number, maxT: number, id: number | string): string {
  const p = Math.min(temp / maxT, 1);
  const o = GC * (1 - p);
  const c = temp > 80 ? "var(--crimson)" : temp > 60 ? "var(--amber)" : "var(--brand)";
  const glow = temp > 80 ? 'filter:drop-shadow(0 0 10px rgba(240,68,68,0.3))' : "";
  return `<svg class="hw-gauge-svg" width="62" height="62" viewBox="0 0 62 62">
    <circle cx="31" cy="31" r="${GR}" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="3"/>
    <circle cx="31" cy="31" r="${GR}" fill="none" stroke="${c}" stroke-width="3" stroke-linecap="round"
      stroke-dasharray="${GC}" stroke-dashoffset="${o}" transform="rotate(-90 31 31)" id="gf-${id}"
      style="transition:stroke-dashoffset 1s var(--e-smooth),stroke 1s var(--e-smooth);${glow}"/>
    <text x="31" y="31" text-anchor="middle" dominant-baseline="central" font-family="var(--mono)" font-size="14" font-weight="700" fill="var(--t1)" id="gt-${id}">${Math.round(temp)}°</text>
    <text x="31" y="47" text-anchor="middle" font-family="var(--sans)" font-size="7" fill="var(--t4)">TEMP</text>
  </svg>`;
}

// ── Render static templates ──
export function renderTemplates(): void {
  const pipelineEl = document.getElementById("pipeline-blocks");
  if (pipelineEl) {
    pipelineEl.innerHTML = `
    <div class="pipeline-block pb-refinery"><div class="pb-glow"></div>
      <div class="pb-row"><span class="pb-label">Refinery</span><span class="pb-count" id="ct-refinery">--</span></div>
      <div class="pb-bar-outer"><div class="pb-bar-inner" id="bar-refinery" style="width:0"></div></div></div>
    <div class="pipeline-block pb-production"><div class="pb-glow"></div>
      <div class="pb-row"><span class="pb-label">Production</span><span class="pb-count" id="ct-production">--</span></div>
      <div class="pb-bar-outer"><div class="pb-bar-inner" id="bar-production" style="width:0"></div></div></div>
    <div class="pipeline-block pb-archive"><div class="pb-glow"></div>
      <div class="pb-row"><span class="pb-label">Archive</span><span class="pb-count" id="ct-archive">--</span></div>
      <div class="pb-bar-outer"><div class="pb-bar-inner" id="bar-archive" style="width:0"></div></div></div>`;
  }
  const metaEl = document.getElementById("forge-meta");
  if (metaEl) {
    metaEl.innerHTML = `
    <div class="fm-label">Forge Info</div>
    <div class="fm-row"><span>Codename</span><span id="fm-codename">--</span></div>
    <div class="fm-row"><span>Version</span><span id="fm-version">--</span></div>
    <div class="fm-row"><span>Checkpoint</span><span id="fm-checkpoint">--</span></div>
    <div class="fm-row"><span>Caveman</span><span id="fm-caveman">--</span></div>`;
  }
}

// ── Top Bar ──
export function updTop(d: DashboardState): void {
  const f: ForgeData = d.forge || {};
  t("k-agents", f.total_agents ?? 0);
  t("k-loops", f.loop_iterations ?? 0);
  t("k-evals", f.total_evaluations ?? 0);
  t("k-skills", (d.skills || []).length);
  const g: GPUData[] = (d.hardware || {}).gpus || [];
  t("k-gpu", g.length > 0 ? (parseFloat(String(g[0].load_pct)) || 0) + "%" : "--");
  const p = d.pipeline || {};
  const cnt = (p.refinery || 0) + (p.production || 0);
  t("forge-status-text", cnt > 0 ? `Active · ${cnt} agents` : "Idle");
  const led = document.getElementById("forge-led");
  if (led) led.className = "forge-dot " + (f.is_working || cnt > 0 ? "active" : "idle");
  const cv = document.getElementById("tgl-caveman") as HTMLInputElement | null;
  if (cv && cv.checked !== !!f.caveman_ultra) cv.checked = !!f.caveman_ultra;
}

// ── Forge Core ──
export function updForge(d: DashboardState): void {
  const p = d.pipeline || {};
  const tot = (p.refinery || 0) + (p.production || 0) + (p.archive || 0) || 1;
  t("pb-pipe", tot);
  t("ct-refinery", p.refinery || 0);
  tw("bar-refinery", ((p.refinery || 0) / tot) * 100);
  t("ct-production", p.production || 0);
  tw("bar-production", ((p.production || 0) / tot) * 100);
  t("ct-archive", p.archive || 0);
  tw("bar-archive", ((p.archive || 0) / tot) * 100);

  document.querySelectorAll(".pb-glow").forEach((el) => {
    const n = parseInt(el.closest(".pipeline-block")?.querySelector(".pb-count")?.textContent || "0") || 0;
    (el as HTMLElement).style.opacity = String(Math.min(n / 25, 0.6));
  });

  const f = d.forge || {};
  t("fm-codename", f.codename || "--");
  t("fm-version", f.version || "--");
  t("fm-checkpoint", (f.last_checkpoint || "--").substring(0, 22));
  const ce = document.getElementById("fm-caveman");
  if (ce) {
    ce.textContent = f.caveman_ultra ? "ON" : "OFF";
    ce.style.color = f.caveman_ultra ? "var(--emerald)" : "var(--t3)";
  }
}

// ── Hardware ──
export function updHW(d: DashboardState): void {
  const g: GPUData[] = (d.hardware || {}).gpus || [];
  const h = d.hardware || {};
  t("pb-hw", g.length + " GPU" + (g.length !== 1 ? "s" : ""));
  const html =
    g
      .map((x, i) => {
        const temp = parseFloat(String(x.temp_c)) || 35;
        const load = Math.round(parseFloat(String(x.load_pct)) || 0);
        const vramUsed = parseFloat(String(x.vram_used_mb)) || 0;
        const vramTotal = parseFloat(String(x.vram_total_mb)) || 1;
        const vramPct = (vramUsed / vramTotal) * 100;
        return `
    <div class="hw-card">
      <div class="hw-top"><span class="hw-gpu-name">GPU ${x.index}</span><span class="hw-gpu-model">${x.name || ""}</span></div>
      <div class="hw-gauges">
        ${gaugeSvg(temp, 95, i)}
        <div class="hw-stats">
          <div class="hw-stat"><span>Load</span><span class="hw-val" id="gl-${i}">${load}%</span></div>
          <div class="hw-bar-wrap"><div class="hw-bar hw-bar-load" style="width:${load}%"></div></div>
          <div class="hw-stat"><span>VRAM</span><span class="hw-val" id="gv-${i}">${x.vram_used_mb}/${x.vram_total_mb} MB</span></div>
          <div class="hw-bar-wrap"><div class="hw-bar hw-bar-vram" style="width:${vramPct}%"></div></div>
          <div class="hw-stat"><span>Power</span><span class="hw-val">${x.power_w || "--"}W</span></div>
        </div>
      </div>
    </div>`;
      })
      .join("") +
    `<div class="sys-info"><div class="sys-row"><span>RAM</span><span class="sys-val">${h.ram || "--"}</span></div><div class="sys-row"><span>CPU</span><span class="sys-val">${h.cpu || "--"}</span></div><div class="sys-row"><span>Python</span><span class="sys-val">${h.python || "--"}</span></div></div>`;
  document.getElementById("hw-body")!.innerHTML = html;
}

// ── Activity Feed (smart diff) ──
export function updActivity(d: DashboardState): void {
  const acts: ActivityItem[] = d.activity || [];
  t("pb-acts", acts.length);
  const body = document.getElementById("activity-body");
  if (!body) return;
  if (!acts.length) {
    body.innerHTML = '<div class="empty"><div class="empty-symbol">◆</div>No activity</div>';
    return;
  }

  const currentIds = new Set<number>();
  acts.forEach((a) => currentIds.add(a.id));

  // Remove gone items
  body.querySelectorAll(".activity-item").forEach((el) => {
    const id = parseInt((el as HTMLElement).dataset.actId || "", 10);
    if (!currentIds.has(id)) el.remove();
  });

  // Update existing + add new
  acts.forEach((a) => {
    const existing = body.querySelector(`.activity-item[data-act-id="${a.id}"]`);
    const actCls = "act-" + a.action;
    const prog = Math.min(a.progress || 0, 100);
    if (existing) {
      const xpFill = existing.querySelector(".act-xp-inner");
      if (xpFill) {
        (xpFill as HTMLElement).style.width = prog + "%";
        xpFill.className = "act-xp-inner " + a.status;
      }
    } else {
      const div = document.createElement("div");
      div.className = `activity-item ${a.status}`;
      div.dataset.actId = String(a.id);
      div.style.animationDelay = "0s";
      div.innerHTML = `
        <div class="act-top">
          <span class="act-bp">${a.blueprint}</span>
          <span class="act-tag ${actCls}">${a.action}</span>
        </div>
        <div class="act-detail">${a.detail || ""}</div>
        <div class="act-xp-outer"><div class="act-xp-inner ${a.status}" style="width:${prog}%"></div></div>
        <div class="act-time">${(a.timestamp || "").substring(11, 19)}</div>`;
      const first = body.firstChild;
      if (first) body.insertBefore(div, first);
      else body.appendChild(div);
    }
  });
}

// ── Skills ──
export function renderSkills(d: DashboardState): void {
  const all: SkillData[] = d.skills || [];
  const searchEl = document.getElementById("skill-search") as HTMLInputElement | null;
  const q = (searchEl?.value || "").toLowerCase();
  const filtered = q ? all.filter((s) => s.name?.toLowerCase().includes(q)) : all.slice(0, 80);
  t("pb-skills", all.length);
  const body = document.getElementById("skills-body");
  if (!body) return;
  if (!filtered.length) {
    body.innerHTML = '<div class="empty"><div class="empty-symbol">◆</div>No skills</div>';
    return;
  }
  body.innerHTML = filtered
    .map((s) => {
      const stage = s.stage || "refinery";
      const sc = s.latest_score;
      return `<div class="skill-chip" onclick="openSkillModal('${s.name}')">
      <div class="sc-dot" style="background:${dotStage(stage)}"></div>
      <span class="sc-name">${s.name}</span>
      <span class="sc-score" style="color:${scoreClr(sc)}">${sc != null ? Math.round(sc) : "--"}</span>
    </div>`;
    })
    .join("");
}

// ── Evaluations ──
export function renderEvals(d: DashboardState): void {
  const ev: EvalData[] = (d.evaluations || []).slice().reverse().slice(0, 18);
  t("pb-evals", ev.length);
  const body = document.getElementById("eval-body");
  if (!body) return;
  if (!ev.length) {
    body.innerHTML = '<div class="empty"><div class="empty-symbol">◆</div>No evaluations</div>';
    return;
  }
  body.innerHTML = ev
    .map((e, i) => {
      const s = e.composite_score || 0;
      return `<div class="eval-row" style="animation:actIn 0.3s var(--e-spring) ${i * 0.02}s both">
      <span class="ev-bp">${e.blueprint || "--"}</span>
      <span class="ev-score" style="color:${scoreClr(s)}">${Math.round(s)}</span>
      <span class="eval-tag ${e.passed ? "pass" : "fail"}">${e.passed ? "PASS" : "FAIL"}</span>
      <span class="ev-ts">${(e.timestamp || "").substring(11, 19)}</span></div>`;
    })
    .join("");
}

// ── Main update (dispatches all sub-renders) ──
export function update(d: DashboardState): void {
  updTop(d);
  updForge(d);
  updHW(d);
  updActivity(d);
  renderSkills(d);
  renderEvals(d);
  updStatus(d);
}

// ── Status Bar ──
export function updStatus(d: DashboardState): void {
  const p = d.pipeline || {};
  t("sb-stats", `Refinery ${p.refinery || 0}  ·  Production ${p.production || 0}  ·  Archive ${p.archive || 0}`);
  t("sb-clock", new Date().toLocaleTimeString());
}

export function showMsg(msg: string): void {
  const el = document.getElementById("sb-message");
  if (!el) return;
  el.textContent = "▶ " + msg;
  el.classList.add("show");
  setTimeout(() => el.classList.remove("show"), 3000);
}
