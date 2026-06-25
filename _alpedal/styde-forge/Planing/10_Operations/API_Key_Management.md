# API & Key Management

**Styde Forge v3.0 — Phase 0**
**Section:** 10_Operations

---

## 1. Purpose

Define how API keys and credentials are managed across the forge. The forge
uses multiple providers (DeepSeek, Claude, Grok, local Ollama) and must
handle keys securely without hardcoding or leaking them.

---

## 2. Supported Providers

| Provider | Auth Type | Key Location | Role |
|----------|-----------|-------------|------|
| DeepSeek (Flash) | API key | `DEEPSEEK_API_KEY` env var | Agent spawn — fast, cheap |
| DeepSeek (Pro) | API key | `DEEPSEEK_API_KEY` env var | Eval, Teacher, Meta — quality |
| Anthropic (Claude) | API key | `ANTHROPIC_API_KEY` env var | Optional judge |
| xAI (Grok) | API key | `XAI_API_KEY` env var | Optional judge |

---

## 3. Key Storage

Keys are NEVER stored in forge files. They are read from environment
variables only, managed by Hermes Agent's credential system:

```
~/.hermes/.env          # Hermes-managed env file
~/.hermes/auth.json     # OAuth tokens (Hermes-managed)
```

```bash
# Set via Hermes CLI:
hermes auth add deepseek
hermes config set model.provider deepseek
```

---

## 4. Provider Selection Logic

```python
def resolve_provider(blueprint_name: str, hardware_profile: str) -> dict:
    """
    Choose provider based on blueprint config and hardware.

    Priority:
    1. Blueprint's hardware_profiles.<active_profile>.provider
    2. Local Ollama (if model fits in VRAM)
    3. Fallback to state.yaml default_provider
    """
    config = load_blueprint_config(blueprint_name)
    hw_config = config.get("hardware_profiles", {}).get(hardware_profile, {})

    if hw_config.get("provider"):
        return {
            "provider": hw_config["provider"],
            "model": hw_config["model"]
        }

    # Try local first for cost savings
    if can_run_locally(hw_config.get("model"), hardware_profile):
        return {"provider": "ollama", "model": hw_config["model"]}

    # Fallback
    state = load_state()
    return {
        "provider": state.get("default_provider", "deepseek"),
        "model": state.get("default_model", "deepseek-v4-pro")
    }
```

---

## 5. Key Validation

At startup, validate that required keys are available:

```python
def validate_keys() -> dict:
    required = {
        "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
    }
    optional = {
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "XAI_API_KEY": os.getenv("XAI_API_KEY"),
        "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY"),
    }

    missing = [k for k, v in required.items() if not v]
    available_optional = [k for k, v in optional.items() if v]

    return {
        "ok": len(missing) == 0,
        "missing_required": missing,
        "available_optional": available_optional
    }
```

---

## 6. Cost-Aware Provider Selection

```python
def select_cost_optimal_provider(task_complexity: str) -> str:
    """
    Choose cheapest provider that can handle the task.

    Simple tasks → try local Ollama first (free)
    Medium tasks → DeepSeek (cheapest cloud)
    Complex tasks → Claude/Grok (best quality)
    """
    if task_complexity == "simple":
        return "ollama" if ollama_available() else "deepseek"
    elif task_complexity == "medium":
        return "deepseek"
    else:
        return "deepseek"  # Default for now
```

---

## 7. Security Rules

- **Never** write API keys to forge files
- **Never** include keys in logs
- **Never** pass keys in agent context
- Keys are read from environment at process start only
- Hermes handles key rotation and credential pooling

---

**Status:** Defined. Keys via Hermes env/auth, never in forge files.
