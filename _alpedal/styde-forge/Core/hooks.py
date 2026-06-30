"""
Hooks system for Styde Forge — lifecycle event callbacks.

Register callbacks for forge events: on_spawn, on_eval, on_improve,
on_promote, on_archive, on_error, on_loop_start, on_loop_end.

Hooks can be registered programmatically or via config files in
StydeAgents/hooks/*.yaml
"""
import time
import threading
import traceback
from pathlib import Path
from typing import Callable, Optional
from datetime import datetime, timezone


FORGE_ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = FORGE_ROOT / "StydeAgents" / "hooks"


class HookRegistry:
    """Thread-safe registry of lifecycle hooks."""

    def __init__(self):
        self._hooks: dict[str, list[Callable]] = {
            "on_spawn": [],
            "on_spawn_complete": [],
            "on_spawn_fail": [],
            "on_eval_start": [],
            "on_eval_complete": [],
            "on_eval_fail": [],
            "on_improve_start": [],
            "on_improve_complete": [],
            "on_improve_fail": [],
            "on_promote": [],
            "on_archive": [],
            "on_error": [],
            "on_loop_start": [],
            "on_loop_end": [],
            "on_loop_iteration": [],
            "on_checkpoint": [],
            "before_spawn": [],
            "after_eval": [],
        }
        self._lock = threading.Lock()
        self._stats: dict[str, int] = {}
        self._loaded_from_disk = False

    def register(self, event: str, callback: Callable) -> None:
        """Register a callback for a lifecycle event.

        Callback receives a dict with event data:
            {event, blueprint, run_id, score, stage, timestamp, ...}
        """
        if event not in self._hooks:
            raise ValueError(f"Unknown event: {event}. Valid: {list(self._hooks.keys())}")
        with self._lock:
            self._hooks[event].append(callback)

    def unregister(self, event: str, callback: Callable) -> None:
        """Remove a registered callback."""
        with self._lock:
            if event in self._hooks and callback in self._hooks[event]:
                self._hooks[event].remove(callback)

    def fire(self, event: str, data: dict = None) -> list[dict]:
        """Fire all callbacks for an event. Returns list of results (or errors).

        Callbacks run synchronously in registration order.
        Errors are caught and reported — one callback failure doesn't block others.
        """
        if data is None:
            data = {}

        data.setdefault("event", event)
        data.setdefault("timestamp", datetime.now(timezone.utc).isoformat())

        results = []
        with self._lock:
            callbacks = list(self._hooks.get(event, []))

        for cb in callbacks:
            start = time.time()
            try:
                result = cb(data)
                results.append({
                    "callback": getattr(cb, "__name__", str(cb)),
                    "success": True,
                    "result": result,
                    "duration_ms": (time.time() - start) * 1000,
                })
            except Exception as e:
                results.append({
                    "callback": getattr(cb, "__name__", str(cb)),
                    "success": False,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "duration_ms": (time.time() - start) * 1000,
                })

        # Update stats
        event_key = f"hook:{event}"
        self._stats[event_key] = self._stats.get(event_key, 0) + 1
        self._stats[f"hook:{event}:errors"] = self._stats.get(
            f"hook:{event}:errors", 0
        ) + sum(1 for r in results if not r["success"])

        return results

    def get_callbacks(self, event: str) -> list[str]:
        """List registered callback names for an event."""
        with self._lock:
            return [getattr(cb, "__name__", str(cb)) for cb in self._hooks.get(event, [])]

    def get_stats(self) -> dict:
        """Get hook invocation statistics."""
        return dict(self._stats)

    def clear_event(self, event: str) -> None:
        """Remove all callbacks for an event."""
        with self._lock:
            if event in self._hooks:
                self._hooks[event].clear()

    def clear_all(self) -> None:
        """Remove all registered callbacks."""
        with self._lock:
            for event in self._hooks:
                self._hooks[event].clear()
            self._stats.clear()

    def list_events(self) -> list[str]:
        """List all available hook events."""
        return sorted(self._hooks.keys())

    def summary(self) -> dict:
        """Return a summary of registered hooks."""
        result = {"events": {}, "total_hooks": 0}
        with self._lock:
            for event, cbs in self._hooks.items():
                if cbs:
                    result["events"][event] = len(cbs)
                    result["total_hooks"] += len(cbs)
        result["stats"] = dict(self._stats)
        return result

    def load_from_disk(self) -> int:
        """Load hooks from StydeAgents/hooks/*.yaml config files.

        Hook config format:
            event: on_spawn
            type: log  # log, webhook, script, python
            config:
              path: /some/script.py  # for script/python types
              url: https://...       # for webhook type
              file: /var/log/forge.log  # for log type

        Returns number of hooks loaded.
        """
        if not HOOKS_DIR.exists():
            return 0

        import yaml
        loaded = 0
        for hook_file in sorted(HOOKS_DIR.glob("*.yaml")):
            try:
                cfg = yaml.safe_load(hook_file.read_text(encoding="utf-8"))
                if not isinstance(cfg, dict):
                    continue
                event = cfg.get("event", "")
                hook_type = cfg.get("type", "")
                config = cfg.get("config", {})

                if event not in self._hooks:
                    continue

                callback = self._build_callback(hook_type, config, hook_file.stem)
                if callback:
                    self.register(event, callback)
                    loaded += 1
            except Exception:
                pass

        self._loaded_from_disk = True
        return loaded

    def _build_callback(self, hook_type: str, config: dict, name: str) -> Optional[Callable]:
        """Build a callable from hook config."""
        if hook_type == "log":
            log_path = Path(config.get("file", FORGE_ROOT / "logs" / "hooks.log"))
            log_path.parent.mkdir(parents=True, exist_ok=True)

            def log_hook(data, _path=log_path):
                import json
                entry = json.dumps(data, default=str) + "\n"
                with open(_path, "a", encoding="utf-8") as f:
                    f.write(entry)

            log_hook.__name__ = f"log:{name}"
            return log_hook

        elif hook_type == "webhook":
            url = config.get("url", "")
            if not url:
                return None

            def webhook_hook(data, _url=url, _timeout=config.get("timeout", 10)):
                import json
                import urllib.request
                payload = json.dumps(data, default=str).encode("utf-8")
                req = urllib.request.Request(
                    _url,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                urllib.request.urlopen(req, timeout=_timeout)

            webhook_hook.__name__ = f"webhook:{name}"
            return webhook_hook

        elif hook_type == "script":
            import subprocess
            script_path = config.get("path", "")

            def script_hook(data, _path=script_path, _timeout=config.get("timeout", 30)):
                import json
                payload = json.dumps(data, default=str)
                subprocess.run(
                    ["python", "-u", _path],
                    input=payload,
                    capture_output=True,
                    text=True,
                    timeout=_timeout,
                )

            script_hook.__name__ = f"script:{name}"
            return script_hook

        elif hook_type == "python":
            module_path = config.get("path", "")
            func_name = config.get("function", "hook")

            def python_hook(data, _mp=module_path, _fn=func_name):
                import importlib.util
                spec = importlib.util.spec_from_file_location("hook_module", _mp)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                hook_fn = getattr(mod, _fn, None)
                if hook_fn:
                    return hook_fn(data)

            python_hook.__name__ = f"python:{name}"
            return python_hook

        return None


# Singleton registry
_registry: Optional[HookRegistry] = None
_registry_lock = threading.Lock()


def get_hooks() -> HookRegistry:
    """Get the singleton hook registry."""
    global _registry
    if _registry is None:
        with _registry_lock:
            if _registry is None:
                _registry = HookRegistry()
                _registry.load_from_disk()
    return _registry


def fire_hook(event: str, data: dict = None) -> list[dict]:
    """Convenience: fire a hook event on the singleton registry."""
    return get_hooks().fire(event, data)


def register_hook(event: str, callback: Callable) -> None:
    """Convenience: register a hook on the singleton registry."""
    get_hooks().register(event, callback)


# Built-in hooks
def _builtin_promotion_logger(data: dict):
    """Log promotions to a dedicated file."""
    log_path = FORGE_ROOT / "logs" / "promotions.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    bp = data.get("blueprint", "?")
    score = data.get("score", "?")
    timestamp = data.get("timestamp", "")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | PROMOTED | {bp} | score={score}\n")


def _builtin_error_logger(data: dict):
    """Log errors to a dedicated file."""
    log_path = FORGE_ROOT / "logs" / "errors.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    bp = data.get("blueprint", "?")
    error = data.get("error", "?")
    timestamp = data.get("timestamp", "")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | ERROR | {bp} | {error}\n")


# Register built-in hooks on import
_builtins_registered = False


def _register_builtins():
    global _builtins_registered
    if _builtins_registered:
        return
    hooks = get_hooks()
    hooks.register("on_promote", _builtin_promotion_logger)
    hooks.register("on_error", _builtin_error_logger)
    _builtins_registered = True


_register_builtins()
