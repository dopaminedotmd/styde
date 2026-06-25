# Hooks & Events

**Styde Forge v3.0 — Phase 0**
**Section:** 13_Hooks_Events

---

## 1. Purpose

Define the hook system — lightweight, focused integration points that trigger
actions at specific moments in the forge loop. Hooks enable extensibility
without modifying core loop logic.

---

## 2. Hook Architecture

```
Forge Loop Event → Hook Registry → Execute Matching Hooks
                                         │
                              ┌──────────┼──────────┐
                              ▼          ▼          ▼
                           Log it    Send alert  Run script
```

---

## 3. Event Types

| Event | Trigger Point | Payload |
|-------|--------------|---------|
| `forge.startup` | Forge initialized | hardware_profile |
| `forge.shutdown` | Graceful shutdown | uptime, iterations |
| `blueprint.created` | New blueprint added | blueprint_name |
| `blueprint.updated` | Blueprint version bumped | name, old_ver, new_ver, delta |
| `agent.spawned` | Agent delegated | agent_id, blueprint, model |
| `agent.completed` | Agent finished | agent_id, duration_ms |
| `agent.failed` | Agent error/timeout | agent_id, error_message |
| `eval.started` | Evaluation begun | agent_id, benchmark |
| `eval.completed` | Evaluation finished | agent_id, score, passed |
| `eval.failed_quality_gate` | Score < 80 | agent_id, score, reason |
| `loop.iteration_complete` | One loop done | blueprint, iteration, score |
| `checkpoint.created` | Checkpoint saved | checkpoint_id, size_bytes |
| `recovery.started` | Crash recovery initiated | last_checkpoint |
| `recovery.completed` | Recovery successful | transactions_replayed |
| `budget.warning` | Cost > 80% of daily | current_cost, limit |
| `budget.exceeded` | Cost > daily limit | current_cost, limit |
| `security.alert` | Sandbox violation | agent_id, violation_type |
| `storage.warning` | USB > 90% full | current_gb, limit_gb |

---

## 4. Hook Definition Format

Hooks are defined as minimal YAML files in `03_HOOKS/`:

```yaml
# 03_HOOKS/integrations/slack_alert.yaml
name: "slack_eval_alert"
event: "eval.failed_quality_gate"
description: "Post to Slack when an agent fails quality gate"
action:
  type: "webhook"
  url: "https://hooks.slack.com/services/..."
  method: "POST"
  body:
    text: "Agent {agent_id} scored {score}/100 on {benchmark}. Needs review."
conditions:
  min_score: 0
  max_score: 79
```

```yaml
# 03_HOOKS/events/checkpoint_cleanup.yaml
name: "checkpoint_cleanup"
event: "checkpoint.created"
description: "Remove checkpoints older than 7 days"
action:
  type: "script"
  command: "python scripts/cleanup_checkpoints.py --older-than 7d"
conditions: {}
```

---

## 5. Hook Types

| Type | Description | Example |
|------|-------------|---------|
| `webhook` | HTTP POST to URL | Slack, Discord notifications |
| `script` | Run shell/Python script | Cleanup, backup, export |
| `log` | Write to log file | Audit trail, metrics |
| `alert` | Send via Hermes messaging | DM to user on critical events |
| `throttle` | Modify forge behavior | Reduce parallelism on budget warning |

---

## 6. Hook Execution

```python
class HookRegistry:
    def __init__(self):
        self.hooks = self._load_hooks()

    def _load_hooks(self) -> dict:
        """Load all hook definitions from 03_HOOKS/"""
        hooks = {}
        hooks_dir = Path("03_HOOKS")
        for hook_file in hooks_dir.rglob("*.yaml"):
            hook = load_yaml(hook_file)
            event = hook["event"]
            if event not in hooks:
                hooks[event] = []
            hooks[event].append(hook)
        return hooks

    def trigger(self, event: str, payload: dict):
        """Execute all hooks registered for this event."""
        if event not in self.hooks:
            return

        for hook in self.hooks[event]:
            if self._conditions_met(hook, payload):
                self._execute(hook, payload)

    def _execute(self, hook: dict, payload: dict):
        """Execute a single hook."""
        action = hook["action"]
        if action["type"] == "webhook":
            import requests
            body = self._interpolate(action["body"], payload)
            requests.post(action["url"], json=body)
        elif action["type"] == "script":
            cmd = self._interpolate(action["command"], payload)
            subprocess.run(cmd, shell=True)
        elif action["type"] == "log":
            log_event(hook["name"], payload)
```

---

## 7. Size Constraint

Hooks are minimal — target < 40 KB each. They are integration glue,
not business logic. Complex logic belongs in skills or scripts.

---

**Status:** Defined. 17 event types, 4 hook types, minimal YAML format.
