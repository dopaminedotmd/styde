# Hermes CLI Bridge

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard communicates with Hermes Agent via its CLI. All agent, process, cron job, and skill data is fetched by invoking `hermes` commands from the Dashboard's backend.

---

## 2. Command Mapping

| Dashboard Function | Hermes CLI Command | Returns |
|--------------------|--------------------|---------|
| List agents | `hermes process list --json` | Active/background processes |
| Agent details | `hermes process log <id>` | Log for specific process |
| Cron jobs | `hermes cronjob list --json` | All scheduled jobs |
| Skills | `hermes skills list` (or filesystem) | Available skills |
| Forge status | `hermes forge status` (hypothetical) | Forge loop status |
| Spawn agent | `hermes delegate_task --goal "..."` | Start new agent |
| Start Forge | `hermes forge start` | Start Forge loop |
| Stop Forge | `hermes forge stop` | Stop Forge loop |

---

## 3. Implementation via Tauri

```rust
// Tauri command: invoke Hermes CLI and return JSON
#[tauri::command]
async fn hermes_command(args: Vec<String>) -> Result<String, String> {
    let output = Command::new("hermes")
        .args(&args)
        .output()
        .map_err(|e| format!("Failed to run hermes: {}", e))?;

    if output.status.success() {
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    } else {
        Err(String::from_utf8_lossy(&output.stderr).to_string())
    }
}

// Example: fetch agent list
#[tauri::command]
async fn get_agents() -> Result<Vec<Agent>, String> {
    let json = hermes_command(vec![
        "process".into(),
        "list".into(),
        "--json".into()
    ]).await?;

    serde_json::from_str(&json)
        .map_err(|e| format!("Failed to parse: {}", e))
}
```

---

## 4. Poll Strategy

```
┌────────────────────────────────────────────────────┐
│                  Poll Loop                          │
│                                                    │
│  setInterval(() => {                               │
│    1. invoke('get_agents')        // Every 2s      │
│    2. invoke('get_cron_jobs')     // Every 10s     │
│    3. invoke('get_skills')        // On startup +  │
│                                      manual refresh│
│  })                                                │
└────────────────────────────────────────────────────┘
```

| Data | Frequency | Reason |
|------|-----------|--------|
| Agents | Every 2s | Real-time monitoring |
| Cron jobs | Every 10s | Rarely changes |
| Skills | On startup + button | Rarely changes |
| System health | Every 5-60s | See Health Monitoring |

---

## 5. Error Handling

```
hermes command → fail
        │
        ▼
┌───────────────────────────┐
│ Hermes not installed?     │
│ → Show: "Hermes CLI not   │
│   found. Install Hermes   │
│   Agent first."           │
│ → Link to install guide   │
└───────────────────────────┘

hermes command → timeout (15s)
        │
        ▼
┌───────────────────────────┐
│ Hermes busy?              │
│ → Retry ×2                │
│ → Still timeout: "Hermes  │
│   is not responding.      │
│   Check if it's running." │
└───────────────────────────┘

hermes command → invalid JSON
        │
        ▼
┌───────────────────────────┐
│ Version mismatch?         │
│ → Log raw output          │
│ → Show: "Unexpected       │
│   output from Hermes.     │
│   Try updating Hermes."   │
└───────────────────────────┘
```

---

## 6. Version Check

On startup the Dashboard checks the Hermes version:

```
$ hermes --version
Hermes Agent v1.2.3
```

| Scenario | Action |
|----------|--------|
| Version ≥ minimum | OK |
| Version < minimum | Warning: "Update Hermes for full functionality" |
| Hermes missing | Install guide |

---

**Status:** Phase 0 — Design
