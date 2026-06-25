# Auto-Update

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard updates itself. When a new version is available, the user gets a notification and can update with one click. Uses Tauri's built-in updater plugin.

---

## 2. Auto-Update Flow

```
┌──────────────────────────────────────────┐
│  Dashboard starts                        │
│        │                                 │
│        ▼                                 │
│  Check GitHub Releases API:              │
│  GET /repos/Alpedal/StydeForge/releases  │
│        │                                 │
│        ▼                                 │
│  Compare versions:                       │
│  current: 1.0.0  vs  latest: 1.1.0      │
│        │                                 │
│    ┌───┴───┐                              │
│    │       │                              │
│  Same   Newer                             │
│    │       │                              │
│    ▼       ▼                              │
│  Done   Show notification:                │
│         "🔄 StydeForge v1.1.0             │
│          available!"                      │
│              │                            │
│              ▼                            │
│         [Update Now] [Later]              │
│              │                            │
│              ▼                            │
│         Download .msi                     │
│         Verify checksum                   │
│         Run installer                     │
│         Restart Dashboard                 │
└──────────────────────────────────────────┘
```

---

## 3. Implementation (Tauri)

```rust
// tauri.conf.json
{
  "plugins": {
    "updater": {
      "endpoints": [
        "https://github.com/Alpedal/StydeForge/releases/latest/download/latest.json"
      ],
      "pubkey": "BASE64_PUBLIC_KEY",  // Signing key
      "windows": {
        "installMode": "passive"
      }
    }
  }
}
```

```json
// latest.json (hosted on GitHub Releases)
{
  "version": "1.1.0",
  "notes": "Bug fixes and performance improvements",
  "pub_date": "2026-07-01T12:00:00Z",
  "platforms": {
    "windows-x86_64": {
      "signature": "BASE64_SIGNATURE",
      "url": "https://github.com/Alpedal/StydeForge/releases/download/v1.1.0/StydeForge.msi"
    }
  }
}
```

---

## 4. Update Settings

```
┌──────────────────────────────────────────────────┐
│ ⚙ SETTINGS — Updates                             │
├──────────────────────────────────────────────────┤
│                                                  │
│  Auto-check for updates:                         │
│  ● Every launch                                  │
│  ○ Daily                                         │
│  ○ Weekly                                        │
│  ○ Never                                         │
│                                                  │
│  Update channel:                                 │
│  ● Stable (recommended)                          │
│  ○ Beta (early features, may have bugs)          │
│                                                  │
│  Current version: 1.0.0                          │
│  Last checked: 2026-06-25 15:42                  │
│                                                  │
│  [Check Now]                                     │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 5. Security

| Measure | Description |
|---------|-------------|
| Signed updates | All releases signed with private key, verified with public key |
| HTTPS only | All downloads over HTTPS |
| Checksum verification | SHA256 checksum compared after download |
| Rollback | If update fails → restore previous version |

---

## 6. Changelog In-App

```
┌──────────────────────────────────────────────────┐
│ 🔄 Update Available — v1.1.0                     │
├──────────────────────────────────────────────────┤
│                                                  │
│  What's new:                                     │
│                                                  │
│  ✨ New: Ollama auto-detection                   │
│  ✨ New: Custom provider support                 │
│  🐛 Fix: Agent panel not updating on resume      │
│  🐛 Fix: Chat streaming cuts off long responses │
│  ⚡ Improvement: 40% faster startup              │
│                                                  │
│  [Update Now]  [Remind Later]  [Skip This Version]│
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 7. Download Progress

```
┌──────────────────────────────────────────────────┐
│ 🔄 Updating StydeForge...                        │
├──────────────────────────────────────────────────┤
│                                                  │
│  Downloading v1.1.0...                           │
│  ████████████████░░░░░░░░  68%  (2.1 / 3.1 MB)  │
│                                                  │
│  [Cancel]                                        │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 8. Edge Cases

| Scenario | Behavior |
|----------|----------|
| No internet | Silent — check again next launch |
| Download interrupted | Resume next time |
| Installer fails | Show error, offer manual download |
| User declines update | Remind again in 3 days |
| Forge running during update | Stop Forge → update → restart Forge |

---

**Status:** Phase 0 — Design
