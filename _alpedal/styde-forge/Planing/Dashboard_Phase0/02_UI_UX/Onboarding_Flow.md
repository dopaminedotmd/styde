# Onboarding Flow — First-Run Experience

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document** — Gap Fill

---

## 1. Overview

The first time a user launches StydeForge, they need guided setup. Without onboarding, the user faces a blank dashboard with no providers configured, no Hermes path set, and no indication of what to do next.

**This document fills a gap:** the 35 Phase 0 docs define the fully-configured dashboard state but never specify the first-run experience.

---

## 2. Onboarding Detection

The Dashboard detects first-run by checking for the config file:

```
%APPDATA%/StydeForge/config.json
```

If the file does not exist → onboarding mode. If it exists but is invalid/corrupt → recovery mode.

After onboarding completes, `localStorage.onboarding_complete = true` is set (per `Local_Storage.md`).

---

## 3. Onboarding Wizard — Step-by-Step

### Step 1: Welcome

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                    ⬡ StydeForge                          │
│                  MISSION CONTROL                         │
│                                                          │
│     Monitor agents · Control the Forge · Chat with AI    │
│                                                          │
│     Your desktop command center for the Hermes Agent     │
│     ecosystem. Everything in one window.                 │
│                                                          │
│                                                          │
│                    [Get Started →]                       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

| Element | Description |
|---------|-------------|
| Logo | StydeForge "S" hexagon (large, centered) |
| Tagline | "Monitor agents · Control the Forge · Chat with AI" |
| CTA | Single "Get Started" button |
| Skip | No skip — onboarding is mandatory for first config |

### Step 2: Detect Hermes

```
┌──────────────────────────────────────────────────────────┐
│ ⚙ Setup — Step 1/4: Hermes Agent                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Detecting Hermes installation...                        │
│                                                          │
│  ✅ Hermes found at:                                     │
│     C:\Users\Pontus\.hermes                              │
│                                                          │
│  Profile: [default ▼]                                    │
│                                                          │
│  ── OR ──                                               │
│                                                          │
│  ❌ Hermes not found.                                    │
│                                                          │
│  Hermes Agent is required to use StydeForge.             │
│  [Install Hermes Agent] → opens website                  │
│  [Locate manually...]    → file picker                   │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│                        [Back]  [Next →]                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Detection logic:**

| Method | Command | Expected Output |
|--------|---------|-----------------|
| PATH search | `which hermes` (git-bash) or `where hermes` (cmd) | Path to `hermes` binary |
| Version check | `hermes --version` | `Hermes Agent vX.Y.Z` |
| Home directory | Look for `~/.hermes/` | Directory exists |
| Config parse | Read `~/.hermes/profiles/default/config.yaml` | Valid YAML |

**Fallback if not found:**
- Show installation guide with link
- Allow manual path entry
- Allow skipping (limited mode — chat only, no agent monitoring)

### Step 3: Configure First Provider

```
┌──────────────────────────────────────────────────────────┐
│ ⚙ Setup — Step 2/4: AI Provider                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Choose your first AI provider for chat:                  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🔮 DeepSeek                        [Configure →]  │  │
│  │    v4-pro · v4-flash · From $0.14/M tokens         │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🧠 OpenAI                          [Configure →]  │  │
│  │    GPT-4o · GPT-4o-mini · From $0.15/M tokens      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🎭 Anthropic                       [Configure →]  │  │
│  │    Claude Sonnet 4 · Haiku 3.5                     │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 🦙 Ollama (Local)                  [Auto-detect]   │  │
│  │    Run models on your own hardware                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  You can add more providers later in Settings.           │
│                                                          │
│                        [Skip for now]  [Back]  [Next →]  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Configure flow (per provider):**
- DeepSeek/OpenAI/Anthropic: Enter API key → Test connection → Done
- Ollama: Auto-detect → Show installed models → Done
- "Skip for now": Dashboard works in limited mode (only show agent monitor if Hermes found)

**API Key input:**
```
┌──────────────────────────────────────┐
│ 🔮 DeepSeek — API Key                │
│                                      │
│  API Key: [sk-••••••••••••••••••]   │
│                                      │
│  Get your key at:                    │
│  platform.deepseek.com/api_keys      │
│                                      │
│  Your key is stored encrypted and    │
│  never leaves your machine.          │
│                                      │
│  [Test Connection]  [Cancel]  [Save] │
└──────────────────────────────────────┘
```

### Step 4: Basic Preferences

```
┌──────────────────────────────────────────────────────────┐
│ ⚙ Setup — Step 3/4: Preferences                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Default chat model:                                     │
│  [deepseek-v4-pro ▼]                                     │
│                                                          │
│  ☑ Minimize to system tray when closing                  │
│  ☐ Start StydeForge when Windows starts                  │
│  ☐ Auto-start Forge on launch                            │
│                                                          │
│  Theme: Dark (only)                                      │
│  Font size: [14] px                                      │
│                                                          │
│                        [Back]  [Next →]                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Step 5: Done — Ready

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│                    ⬡ You're Ready!                       │
│                                                          │
│     ✅ Hermes Agent detected                             │
│     ✅ DeepSeek configured                               │
│     ✅ Preferences saved                                 │
│                                                          │
│     Your dashboard is ready. Here's what you can do:     │
│                                                          │
│     📡 Monitor agents in the left panel                  │
│     💬 Chat with AI in the right panel                   │
│     ▶ Start the Forge from the top bar                  │
│                                                          │
│                    [Open Dashboard →]                    │
│                                                          │
│     Tip: Press Ctrl+K to focus the chat input at         │
│           any time. Type /skills to see capabilities.    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 4. Limited Mode (no Hermes, no provider)

If the user skips both Hermes detection AND provider setup:

| Feature | Available? | Note |
|---------|-----------|------|
| Chat | ❌ | No provider configured |
| Agent Monitor | ❌ | No Hermes to poll |
| Benchmarks | ❌ | No data |
| Settings | ✅ | Can configure later |
| System Health | ✅ | Local system only |
| Appearance | ✅ | Always available |

Dashboard shows a prominent banner:
```
┌──────────────────────────────────────────────────────────┐
│ ⚠ StydeForge is in limited mode. Configure a provider    │
│    and connect Hermes to unlock all features.             │
│                              [Setup Now]  [Dismiss]       │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Post-Onboarding States

### 5.1 Fully Configured (normal)
- `config.json` exists and is valid
- At least 1 provider configured
- Hermes path valid
- → Dashboard opens to standard 3-panel layout

### 5.2 Config Exists but Provider Missing
- User skipped provider during onboarding
- → Prompt to add provider on first chat message

### 5.3 Config Corrupt
- `config.json` parse error
- → Show recovery: "Config file is corrupted. [Reset to defaults] [Restore backup]"

### 5.4 Hermes Path Changed / Broken
- Previously valid path now missing
- → Banner: "Hermes not found at [path]. [Locate] [Reinstall]"

---

## 6. Onboarding Re-trigger

Users can re-run onboarding from Settings → "Re-run Setup Wizard".

This is useful if:
- Hermes was installed AFTER the Dashboard
- User wants to add their first provider with guidance
- Config was reset

---

## 7. Edge Cases

| Scenario | Behavior |
|----------|----------|
| User closes wizard mid-onboarding | Save partial config, resume where they left off next launch |
| User has Hermes but no provider | Skip provider step, enter limited mode |
| User has provider but no Hermes | Skip Hermes detection, enter limited mode (chat works) |
| Multiple Hermes versions installed | Show picker: select which one to use |
| User comes from v0.x (upgrade) | Detect existing config → skip onboarding OR show "what's new" |
| First launch on new machine (config synced) | If config.json exists and valid → skip onboarding |

---

## 8. Config Written by Onboarding

```json
{
  "version": "1.0",
  "hermes_path": "C:\\Users\\Pontus\\.hermes",
  "hermes_profile": "default",
  "providers": {
    "deepseek": {
      "api_key": "sk-...",
      "enabled": true
    }
  },
  "ui": {
    "theme": "dark",
    "font_size": 14
  },
  "forge": {
    "auto_start": false,
    "stop_on_exit": true
  },
  "onboarding": {
    "completed": true,
    "completed_at": "2026-06-25T15:42:00Z",
    "version": 1
  }
}
```

---

**Status:** Phase 0 — Gap Fill (new document)
**Created:** 2026-06-25
