/* ═══════════════════════════════════════════════════════════
   MISSION CONTROL ENGINE  v5 — Entry Point
   TypeScript refactor: inline JS → modular TS
   ═══════════════════════════════════════════════════════════ */

import { autoRefresh, refreshTimer } from "./state.js";
import type { DashboardState } from "./state.js";
import { renderTemplates, update as renderUpdate } from "./render.js";
import { setRefreshCallback } from "./api.js";

export { openSkillModal, closeModal, apiSpawn, apiEval, apiImprove, apiLoop, apiToggleCaveman } from "./api.js";

const API = "/api/state";

/* ─── Global refresh (called by api.ts via callback) ─── */
export async function fetchState(): Promise<void> {
  if (refreshTimer) clearTimeout(refreshTimer);
  try {
    const r = await fetch(API);
    const d: DashboardState = await r.json();
    renderUpdate(d);
  } catch {
    // silent
  }
  if (autoRefresh) {
    (await import("./state.js")).refreshTimer = setTimeout(fetchState, 3000);
  }
}

/* ─── Register refresh callback with api.ts ─── */
setRefreshCallback(fetchState);

/* ─── Keyboard ─── */
document.addEventListener("keydown", (e: KeyboardEvent) => {
  if (e.key === "Escape") {
    import("./api.js").then((m) => m.closeModal());
  }
  if (e.key === "r" && e.ctrlKey) {
    e.preventDefault();
    fetchState();
  }
  if (e.key === "k" && e.metaKey) {
    e.preventDefault();
    // Placeholder for command palette
  }
});

/* ─── Expose globals for inline onclick handlers ─── */
const win = window as Record<string, unknown>;
win.openSkillModal = (name: string) => import("./api.js").then((m) => m.openSkillModal(name));
win.closeModal = () => import("./api.js").then((m) => m.closeModal());
win.apiSpawn = () => import("./api.js").then((m) => m.apiSpawn());
win.apiEval = () => import("./api.js").then((m) => m.apiEval());
win.apiImprove = () => import("./api.js").then((m) => m.apiImprove());
win.apiLoop = () => import("./api.js").then((m) => m.apiLoop());
win.apiToggleCaveman = (on: boolean) => import("./api.js").then((m) => m.apiToggleCaveman(on));
win.fetchState = () => fetchState();

/* ─── Init ─── */
(async () => {
  renderTemplates();
  try {
    const r = await fetch(API);
    const d: DashboardState = await r.json();
    renderUpdate(d);
  } catch {
    // silent
  }
})();
