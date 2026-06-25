# Agent Detail View

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

Clicking an agent in the list opens a detail view — either as a slide-in panel from the right or as an expanded section in the agent list.

---

## 2. Detail View — Layout

```
┌──────────────────────────────────────────────────┐
│ ← Back to Agents                                 │
├──────────────────────────────────────────────────┤
│                                                  │
│  ● code-reviewer-v3                     87/100  │
│  ─────────────────────────────────────────────  │
│                                                  │
│  ┌─ Overview ──────────────────────────────────┐ │
│  │ Status:     Completed                        │ │
│  │ Model:      deepseek-v4-flash                │ │
│  │ Blueprint:  code-reviewer-v3                 │ │
│  │ Duration:   3m 45s                           │ │
│  │ Tokens:     6,842 (4.2K in / 2.6K out)      │ │
│  │ Cost:       $0.019                           │ │
│  │ Speed:      32 t/s avg                       │ │
│  │ Started:    2026-06-25 15:38:12              │ │
│  │ Finished:   2026-06-25 15:41:57              │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Evaluation ────────────────────────────────┐ │
│  │ Overall Score: 87/100                        │ │
│  │                                              │ │
│  │ Category         Score   Weight              │ │
│  │ ────────────────────────────────────         │ │
│  │ Code Quality     91/100  30%                │ │
│  │ Completeness     85/100  25%                │ │
│  │ Best Practices   88/100  20%                │ │
│  │ Efficiency       82/100  15%                │ │
│  │ Documentation    90/100  10%                │ │
│  │                                              │ │
│  │ Judge: deepseek-v4-pro                       │ │
│  │ Eval time: 0.8s                              │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Output ────────────────────────────────────┐ │
│  │ [Preview] [Raw] [Download]                   │ │
│  │ ┌──────────────────────────────────────────┐ │ │
│  │ │ 1│# Code Review: auth-service.ts         │ │ │
│  │ │ 2│                                       │ │ │
│  │ │ 3│## Summary                            │ │ │
│  │ │ 4│The authentication service is well-    │ │ │
│  │ │ 5│structured but has 3 issues:            │ │ │
│  │ │...                                       │ │ │
│  │ └──────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌─ Log ───────────────────────────────────────┐ │
│  │ [All] [Errors] [Warnings] [Info]             │ │
│  │ ┌──────────────────────────────────────────┐ │ │
│  │ │15:38:12 [INFO]  Agent spawned            │ │ │
│  │ │15:38:12 [INFO]  Loading skills...        │ │ │
│  │ │15:38:13 [INFO]  Skills loaded: code-     │ │ │
│  │ │15:38:13 [INFO]  Starting task...         │ │ │
│  │ │15:38:45 [WARN]  File too large, chunking │ │ │
│  │ │...                                       │ │ │
│  │ └──────────────────────────────────────────┘ │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  [🔄 Retry] [📋 Copy Output] [💾 Export] [✕]    │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 3. Section: Overview

| Field | Description |
|-------|-------------|
| Status | ● Running / ✓ Completed / ✗ Failed |
| Model | Model name + provider |
| Blueprint | Blueprint the agent was spawned from |
| Duration | Total runtime |
| Tokens | Input + output tokens |
| Cost | Estimated API cost |
| Speed | Average tokens/second |
| Started | Start time (ISO 8601) |
| Finished | End time (or "—" if running) |
| Skills | List of skills loaded |

---

## 4. Section: Evaluation

Shown only if agent has completed and been evaluated.

| Element | Description |
|---------|-------------|
| Overall Score | 0-100, color-coded (green ≥80, yellow ≥60, red <60) |
| Categories | Table with sub-scores and weights |
| Judge | Which model acted as judge |
| Eval time | How long evaluation took |
| Feedback | Qualitative feedback from judge (if available) |

---

## 5. Section: Output

| View | Description |
|------|-------------|
| Preview | Rendered markdown/syntax highlighting |
| Raw | Raw text |
| Download | Download as .md / .txt / .json |
| Diff | If agent modified files — show unified diff |

---

## 6. Section: Log

| Filter | Shows |
|--------|-------|
| All | All log levels |
| Errors | Only ERROR |
| Warnings | WARN + ERROR |
| Info | INFO + above |

**Features:**
- Search in log (Ctrl+F)
- Copy selected lines
- Auto-scroll (toggle)
- Export entire log

---

## 7. Action Bar

| Button | Function | Visible When |
|--------|----------|-------------|
| 🔄 Retry | Restart agent | Failed / Completed |
| ⏹ Stop | Stop agent | Running |
| 📋 Copy Output | Copy output to clipboard | Completed |
| 💾 Export | Export agent data | Completed / Failed |
| ✕ Close | Close detail view | Always |

---

## 8. Real-time Updates (Running Agent)

While agent is running:
- Duration updates live (ticks every second)
- Token counter increments
- Output streams in (append, not replace)
- Log updates continuously
- Progress bar fills based on expected tokens/time

---

**Status:** Phase 0 — Design
