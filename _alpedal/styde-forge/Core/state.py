"""State management: load/save state.yaml with atomic writes."""
import yaml
from pathlib import Path
from Core.persistence import atomic_write

FORGE_ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = FORGE_ROOT / "state.yaml"


def load_state() -> dict:
    """Load forge state from state.yaml. Raises FileNotFoundError if missing."""
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}. Run 'forge.py init' first.")
    return yaml.safe_load(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict):
    """Save forge state atomically to state.yaml."""
    content = yaml.dump(state, default_flow_style=False, allow_unicode=True)
    atomic_write(STATE_FILE, content)
