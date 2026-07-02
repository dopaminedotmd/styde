# Spawn New Agent

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard lets the user manually spawn a new agent — without going through the Forge loop. This is for ad-hoc tasks: "run code review on this file", "generate tests for this module".

---

## 2. Spawn Flow

```
Click [+ New Agent] in agent panel
        │
        ▼
┌─────────────────────────────────┐
│  SPAWN NEW AGENT                │
│                                 │
│  ┌─ Blueprint ────────────────┐ │
│  │ [Select blueprint ▼]       │ │
│  │  • code-review             │ │
│  │  • test-generator          │ │
│  │  • doc-writer              │ │
│  │  • custom (write prompt)   │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─ Model ────────────────────┐ │
│  │ [deepseek-v4-flash ▼]      │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─ Skills ───────────────────┐ │
│  │ ☑ code-review              │ │
│  │ ☐ test-driven-development  │ │
│  │ ☑ systematic-debugging     │ │
│  │ [+ Add skill]              │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─ Prompt / Instructions ────┐ │
│  │ ┌─────────────────────────┐ │ │
│  │ │ Review auth-service.ts  │ │ │
│  │ │ for security issues     │ │ │
│  │ │                         │ │ │
│  │ └─────────────────────────┘ │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─ Options ──────────────────┐ │
│  │ ☐ Caveman Ultra mode      │ │
│  │ ☑ Save output to file     │ │
│  │ ☐ Evaluate after completion│ │
│  └────────────────────────────┘ │
│                                 │
│  [Cancel]              [▶ Spawn]│
└─────────────────────────────────┘
```

---

## 3. Form Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| Blueprint | Dropdown | Last used | Select from available blueprints or "custom" |
| Model | Dropdown | deepseek-v4-flash | Select model from active providers |
| Skills | Multi-select | Empty | Select skills to load |
| Prompt | Textarea | Empty | Instructions for the agent |
| Caveman Ultra | Checkbox | true | Enable Caveman Ultra (70% fewer tokens) |
| Save output | Checkbox | true | Save output to file |
| Evaluate | Checkbox | true | Run eval after completion |

---

## 4. Blueprint System

### 4.1 Built-in Blueprints

| Blueprint | Description | Default Skills |
|-----------|-------------|----------------|
| `code-review` | Review code | requesting-code-review, systematic-debugging |
| `test-generator` | Generate tests | test-driven-development |
| `doc-writer` | Write documentation | — |
| `refactor` | Refactor code | simplify-code |
| `debug` | Debug an issue | systematic-debugging |
| `custom` | Free-text prompt | Manual selection |

### 4.2 Custom Blueprints

Users can save custom blueprints:
```json
{
  "name": "my-security-audit",
  "description": "Review code for OWASP Top 10 vulnerabilities",
  "model": "deepseek-v4-pro",
  "skills": ["systematic-debugging"],
  "caveman_ultra": false
}
```

---

## 5. Spawn Mechanism

When user clicks [▶ Spawn]:

```
1. Build command:
   hermes delegate_task \
     --goal "<prompt>" \
     --model "<model>" \
     --skills "<skill1>,<skill2>" \
     --caveman-ultra

2. Run as child process

3. Agent appears in Agent panel with status ● Running

4. Output streams to Agent Detail View
```

---

## 6. Validation

| Rule | Error Message |
|------|---------------|
| Prompt must not be empty | "Please enter instructions for the agent" |
| At least one skill (non-custom) | "Select at least one skill" |
| Model must have active provider | "Provider not connected. Check settings." |

---

## 7. Quick Spawn (Shortcut)

From chat: type `/spawn code-review auth-service.ts`

Chat agent interprets command and spawns agent without opening the form.

---

**Status:** Phase 0 — Design
