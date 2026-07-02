# Skill Command System

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The chat agent can load and use Hermes skills via a simple command system. The user types `/skill:name` or mentions a skill by name, and the agent loads it for the next response.

---

## 2. Skill Commands

### 2.1 `/skill:name`

```
👤 You:
/skill:code-review Review auth-service.ts

🤖 Agent:
✅ Skill loaded: code-review (GitHub code review)
Reviewing auth-service.ts...
```

### 2.2 `/skills`

```
👤 You:
/skills

🤖 Agent:
Available skills (72):

Category: software-development
  • code-review — Review PRs via gh CLI or REST
  • test-driven-development — TDD enforce RED-GREEN-REFACTOR
  • systematic-debugging — 4-phase root cause debugging
  • simplify-code — Parallel 3-agent cleanup
  ...

Category: creative
  • architecture-diagram — SVG architecture diagrams
  • excalidraw — Hand-drawn diagrams
  ...
```

### 2.3 `/skill:name info`

```
👤 You:
/skill:code-review info

🤖 Agent:
📦 code-review (GitHub → software-development)
────────────────────────────────────────
Review PRs: diffs, inline comments via gh or REST.

Tools used: terminal, file, web
Triggers: PR review, code review, review code
```

---

## 3. Skill Loading — Flow

```
1. User types "/skill:code-review Review auth.ts"
        │
2. Chat Controller parses the message:
   • command: "skill:code-review"
   • args: "Review auth.ts"
        │
3. Chat Controller calls Hermes:
   hermes skill_view code-review --json
        │
4. Skill content (SKILL.md) injected into system prompt:
   "You have loaded the 'code-review' skill. Follow its
    instructions: ... [skill content] ..."
        │
5. The message "Review auth.ts" sent to AI provider
   with the extended system prompt
        │
6. Agent responds using the skill instructions as basis
```

---

## 4. Skill Context Window

Skills have a token budget to avoid exceeding the context window:

| Rule | Value |
|------|-------|
| Max simultaneous skills | 3 |
| Max tokens per skill | 4000 (truncated if larger) |
| Priority | Most recently loaded skill → highest priority |
| Auto-unload | After 5 messages without reference to the skill |

---

## 5. Implicit Skill Detection

The agent can also load skills implicitly — if the user's question matches a skill's triggers:

```
👤 You:
Do a code review on PR #42

🤖 Agent:
Auto-loading code-review skill for this...
✅ Skill loaded: code-review
[continues with review...]
```

Triggers are defined in SKILL.md frontmatter:
```yaml
---
triggers:
  - "code review"
  - "review PR"
  - "review code"
  - "PR review"
---
```

---

## 6. Skill Error Scenarios

| Scenario | Behavior |
|----------|----------|
| Skill not found | "Skill 'xyz' not found. /skills to see available." |
| Skill too large | "Skill 'xyz' is 8200 tokens. Showing summary instead." |
| Max skills reached | "You already have 3 skills loaded. Replace one? [list]" |
| Hermes not available | "Cannot load skills — Hermes is not running. [Start Forge]" |

---

## 7. User Experience

| Element | Display |
|---------|---------|
| Loaded skill | Badge in chat header: `[📦 code-review] [📦 tdd]` |
| Skill usage in response | Small 📦 icon by message with skill name |
| Tooltip on badge | Click → show skill description |
| Remove skill | Click ✕ on badge → unload |
| Skill history | Recently used skills → autocomplete in input |

---

**Status:** Phase 0 — Design
