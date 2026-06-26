/* ═══════════════════════════════════════════════════════════
   MISSION CONTROL ENGINE  v5 — TypeScript
   Smart-diff rendering, spring physics, no blink.
   ═══════════════════════════════════════════════════════════ */

// ── Types ──
export interface GPUData {
  index: number;
  name: string;
  temp_c: number | string;
  load_pct: number | string;
  vram_used_mb: number | string;
  vram_total_mb: number | string;
  power_w: number | string;
}

export interface HardwareData {
  gpus?: GPUData[];
  ram?: string;
  cpu?: string;
  python?: string;
}

export interface PipelineData {
  refinery?: number;
  production?: number;
  archive?: number;
}

export interface ForgeData {
  total_agents?: number;
  total_evaluations?: number;
  loop_iterations?: number;
  caveman_ultra?: boolean;
  codename?: string;
  version?: string;
  last_checkpoint?: string;
  is_working?: boolean;
}

export interface ActivityItem {
  id: number;
  action: string;
  blueprint: string;
  detail?: string;
  progress?: number;
  status: string;
  timestamp?: string;
}

export interface SkillData {
  name: string;
  stage?: string;
  latest_score?: number;
  runs?: SkillRun[];
}

export interface SkillRun {
  score?: number;
  id: string;
  task?: string;
  output_preview?: string;
}

export interface EvalData {
  blueprint?: string;
  composite_score?: number;
  passed?: boolean;
  timestamp?: string;
}

export interface DashboardState {
  forge?: ForgeData;
  pipeline?: PipelineData;
  hardware?: HardwareData;
  activity?: ActivityItem[];
  skills?: SkillData[];
  evaluations?: EvalData[];
}

// ── State ──
export let prevState: DashboardState | null = null;
export let autoRefresh = true;
export let refreshTimer: ReturnType<typeof setTimeout> | null = null;
