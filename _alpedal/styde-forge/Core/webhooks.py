"""
Webhook notifications for Styde Forge — Discord, Slack, generic webhook.

Pre-built templates for forge lifecycle events.
Registers as hooks automatically.
"""
import json
import urllib.request
from pathlib import Path
from typing import Optional

FORGE_ROOT = Path(__file__).resolve().parent.parent


def send_discord(webhook_url: str, title: str, description: str,
                 color: int = 0x4caf50, fields: list[dict] = None) -> bool:
    """Send a Discord webhook embed."""
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }
    if fields:
        embed["fields"] = fields

    payload = json.dumps({"embeds": [embed]}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception:
        return False


def send_slack(webhook_url: str, text: str, color: str = "good") -> bool:
    """Send a Slack webhook message."""
    payload = json.dumps({
        "attachments": [{
            "color": color,
            "text": text,
            "ts": int(__import__("time").time()),
        }]
    }).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception:
        return False


# --- Pre-built hook callbacks ---

def discord_promotion_hook(webhook_url: str):
    """Returns a callback that sends Discord notification on promotion."""
    def callback(data: dict):
        bp = data.get("blueprint", "?")
        score = data.get("score", 0)
        passes = data.get("consecutive_passes", 0)
        send_discord(
            webhook_url=webhook_url,
            title=f"Agent Promoted: {bp}",
            description=f"Score: **{score}/100** | Consecutive passes: {passes}",
            color=0x4caf50,  # green
            fields=[
                {"name": "Blueprint", "value": bp, "inline": True},
                {"name": "Score", "value": str(score), "inline": True},
                {"name": "Consecutive", "value": str(passes), "inline": True},
            ],
        )
    callback.__name__ = "discord:promotion"
    return callback


def discord_archive_hook(webhook_url: str):
    """Returns a callback that sends Discord notification on archive."""
    def callback(data: dict):
        bp = data.get("blueprint", "?")
        score = data.get("score", 0)
        send_discord(
            webhook_url=webhook_url,
            title=f"Agent Archived: {bp}",
            description=f"Score: **{score}/100** | Needs blueprint rewrite",
            color=0xf44336,  # red
            fields=[
                {"name": "Blueprint", "value": bp, "inline": True},
                {"name": "Score", "value": str(score), "inline": True},
            ],
        )
    callback.__name__ = "discord:archive"
    return callback


def discord_error_hook(webhook_url: str):
    """Returns a callback that sends Discord notification on errors."""
    def callback(data: dict):
        bp = data.get("blueprint", "?")
        error = data.get("error", "")[:500]
        stage = data.get("stage", "?")
        send_discord(
            webhook_url=webhook_url,
            title=f"Forge Error: {bp}",
            description=f"Stage: **{stage}**\n```{error}```",
            color=0xff9800,  # orange
        )
    callback.__name__ = "discord:error"
    return callback


def slack_promotion_hook(webhook_url: str):
    """Returns a callback that sends Slack notification on promotion."""
    def callback(data: dict):
        bp = data.get("blueprint", "?")
        score = data.get("score", 0)
        send_slack(
            webhook_url=webhook_url,
            text=f"*Agent Promoted:* `{bp}` — Score: *{score}/100*",
            color="good",
        )
    callback.__name__ = "slack:promotion"
    return callback


# --- Registration helper ---

def register_discord_hooks(webhook_url: str, events: list[str] = None):
    """Register Discord webhooks for forge events."""
    from Core.hooks import register_hook

    if events is None:
        events = ["on_promote", "on_archive", "on_error"]

    mapping = {
        "on_promote": discord_promotion_hook,
        "on_archive": discord_archive_hook,
        "on_error": discord_error_hook,
    }

    for event in events:
        if event in mapping:
            register_hook(event, mapping[event](webhook_url))


def register_slack_hooks(webhook_url: str, events: list[str] = None):
    """Register Slack webhooks for forge events."""
    from Core.hooks import register_hook

    if events is None:
        events = ["on_promote", "on_archive"]

    mapping = {
        "on_promote": slack_promotion_hook,
    }

    for event in events:
        if event in mapping:
            register_hook(event, mapping[event](webhook_url))
