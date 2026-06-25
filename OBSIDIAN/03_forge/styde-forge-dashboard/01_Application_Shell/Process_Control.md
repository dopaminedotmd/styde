# Process Control

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard manages Hermes as a child process via Tauri's Rust backend:

```
┌─────────────────────────────────┐
│   Dashboard (Tauri Rust Shell)  │
│                                 │
│   spawn("hermes", ["forge",     │
│          "start"])              │
│         │                       │
│         ▼                       │
│   ┌─────────────────────┐       │
│   │ Child Process       │       │
│   │ hermes forge start  │       │
│   │                     │       │
│   │ stdout/stderr pipes │       │
│   └─────────┬───────────┘       │
│             │                   │
│   ┌─────────┴───────────┐       │
│   │ Process Manager     │       │
│   │ • Monitor stdout    │       │
│   │ • Track PID         │       │
│   │ • Handle crashes    │       │
│   │ • Signal (SIGTERM)  │       │
│   └─────────────────────┘       │
└─────────────────────────────────┘
```

---

## 2. Process Spawning

### 2.1 Hermes Forge Loop

```rust
// Pseudocode — Tauri Rust backend
let hermes_process = Command::new("hermes")
    .args(["forge", "start"])
    .env("HERMES_PROFILE", "default")
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()?;

// Save PID for later control
state.hermes_pid = hermes_process.id();
```

### 2.2 Ad-hoc Hermes Commands

Dashboard also runs short-lived Hermes commands for data polling:

```rust
// Poll agent status — runs and returns immediately
let output = Command::new("hermes")
    .args(["process", "list", "--json"])
    .output()?;

let agents: Vec<Agent> = serde_json::from_str(&output.stdout)?;
```

---

## 3. Process Monitoring

Dashboard monitors the Hermes process continuously:

| Event | Detection | Action |
|-------|-----------|--------|
| Process crashes | `WaitForSingleObject` on process handle | Show error, offer restart |
| Process hangs | No stdout for 60s | Warning in UI, offer force kill |
| High CPU | >80% for 30s | Warning: "Hermes using high CPU" |
| High memory | >4GB | Warning: "Hermes using high memory" |

---

## 4. Communication with Hermes

### 4.1 stdout/stderr — Real-time Log

Hermes stdout and stderr pipes are read continuously:
- Each line parsed (JSON-lines format from Hermes logging)
- Relevant data pushed to UI (status updates, errors)
- Raw logs saved to disk for debugging

### 4.2 Signal Handling

| Signal | Usage |
|--------|-------|
| SIGTERM | Graceful stop — Hermes finishes active iteration |
| SIGINT | Pause — Hermes pauses after current step |
| SIGKILL | Force kill (last resort, after timeout) |

---

## 5. Cron Job Management

Dashboard controls Hermes cron jobs:

| Action | Hermes Command |
|--------|---------------|
| List all jobs | `hermes cronjob list --json` |
| Start a job | `hermes cronjob resume <job_id>` |
| Pause a job | `hermes cronjob pause <job_id>` |
| Run a job manually | `hermes cronjob run <job_id>` |
| Remove a job | `hermes cronjob remove <job_id>` |

---

## 6. Error Recovery

```
Process crash detected
        │
        ▼
┌─────────────────────┐
│ 1. Log the crash    │
│    (save last 100   │
│     lines of stderr) │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 2. Show dialog      │
│ "Hermes crashed.    │
│  Options:           │
│  [Restart]          │
│  [View Log]         │
│  [Close Dashboard]" │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ 3. If restart:      │
│    • Load latest    │
│      checkpoint     │
│    • Restore agents │
│    • Restart        │
│      Forge loop     │
└─────────────────────┘
```

---

## 7. Process Safety

| Rule | Reason |
|------|--------|
| Only one Forge process at a time | Avoid race conditions |
| Dashboard owns the process | If Dashboard dies → Hermes dies (no zombies) |
| 30s timeout on shutdown | Prevent shutdown from hanging |
| Log all process events | Full traceability for debugging |

---

**Status:** Phase 0 — Design
