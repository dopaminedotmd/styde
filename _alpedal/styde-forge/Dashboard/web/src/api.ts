import type { DashboardState } from "./state.js";
import { showMsg } from "./render.js";

// ── Internal refresh (avoids circular dep with main.ts) ──
let _refreshCallback: (() => void) | null = null;
export function setRefreshCallback(cb: () => void): void {
  _refreshCallback = cb;
}

// ── Skill Modal ──
export async function openSkillModal(name: string): Promise<void> {
  const modal = document.getElementById("modal");
  if (modal) modal.classList.add("open");
  const titleEl = document.getElementById("modal-title");
  if (titleEl) titleEl.textContent = name;
  const badgeEl = document.getElementById("modal-badge");
  if (badgeEl) badgeEl.textContent = "Loading...";
  const runsEl = document.getElementById("modal-runs");
  if (runsEl) runsEl.innerHTML = '<div class="empty"><div class="empty-symbol">◆</div>Loading...</div>';
  const outputEl = document.getElementById("modal-output");
  if (outputEl) outputEl.textContent = "...";
  try {
    const r = await fetch("/api/state");
    const d: DashboardState = await r.json();
    const s = d.skills?.find((x) => x.name === name);
    if (!s) {
      const runsEl2 = document.getElementById("modal-runs");
      if (runsEl2) runsEl2.innerHTML = '<div class="empty"><div class="empty-symbol">✕</div>Not found</div>';
      return;
    }
    const badgeEl2 = document.getElementById("modal-badge");
    if (badgeEl2) {
      badgeEl2.textContent = s.stage || "refinery";
      badgeEl2.style.cssText = `
      background:${s.stage === "production" ? "var(--emerald-dim)" : s.stage === "archive" ? "rgba(255,255,255,0.03)" : "var(--amber-dim)"};
      color:${s.stage === "production" ? "var(--emerald)" : s.stage === "archive" ? "var(--t3)" : "var(--amber)"}`;
    }
    const runsEl3 = document.getElementById("modal-runs");
    if (runsEl3) {
      if (s.runs?.length) {
        runsEl3.innerHTML = s.runs
          .slice(0, 15)
          .map((r) => {
            const sc = r.score;
            return `<div class="modal-run-row">
            <span class="mr-score" style="color:${sc != null ? (sc >= 85 ? "var(--emerald)" : sc >= 70 ? "var(--amber)" : "var(--t3)") : "var(--t3)"}">${sc != null ? Math.round(sc) : "--"}</span>
            <span class="mr-id">${r.id}</span>
            <span style="font-size:8px;color:var(--t4)">${(r.task || "").substring(0, 35)}</span>
          </div>`;
          })
          .join("");
      } else {
        runsEl3.innerHTML = '<div class="empty"><div class="empty-symbol">◆</div>No runs</div>';
      }
    }
    const outputEl2 = document.getElementById("modal-output");
    if (outputEl2) {
      outputEl2.textContent = s.runs?.[0]?.output_preview || "No output";
    }
  } catch {
    // silent
  }
}

export function closeModal(): void {
  document.getElementById("modal")?.classList.remove("open");
}

// ── API Controls ──
export function apiSpawn(): void {
  const bpInput = document.getElementById("spawn-bp") as HTMLInputElement | null;
  const bp = bpInput?.value.trim();
  if (!bp) {
    showMsg("Enter a blueprint name first");
    return;
  }
  fetch("/api/spawn", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ blueprint: bp }),
  })
    .then(() => {
      showMsg(`Spawned: ${bp}`);
      setTimeout(() => _refreshCallback?.(), 600);
    })
    .catch(() => showMsg("Spawn failed"));
}

export function apiEval(): void {
  const bp = prompt("Blueprint name:");
  if (!bp) return;
  const rid = prompt("Run ID (or blank for latest):") || "latest";
  fetch("/api/eval", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ blueprint: bp, run_id: rid }),
  })
    .then(() => {
      showMsg(`Eval: ${bp}`);
      setTimeout(() => _refreshCallback?.(), 600);
    })
    .catch(() => showMsg("Eval failed"));
}

export function apiImprove(): void {
  const bp = prompt("Blueprint name:");
  if (!bp) return;
  const rid = prompt("Run ID:");
  if (!rid) return;
  fetch("/api/improve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ blueprint: bp, run_id: rid }),
  })
    .then(() => {
      showMsg(`Improve: ${bp}`);
      setTimeout(() => _refreshCallback?.(), 600);
    })
    .catch(() => showMsg("Improve failed"));
}

export function apiLoop(): void {
  fetch("/api/loop", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: "{}",
  })
    .then(() => {
      showMsg("Forge loop started");
      setTimeout(() => _refreshCallback?.(), 600);
    })
    .catch(() => showMsg("Loop failed"));
}

export function apiToggleCaveman(on: boolean): void {
  fetch("/api/toggle-caveman", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: "{}",
  })
    .then(() => {
      showMsg(on ? "Caveman ON" : "Caveman OFF");
      setTimeout(() => _refreshCallback?.(), 400);
    })
    .catch(() => showMsg("Toggle failed"));
}
