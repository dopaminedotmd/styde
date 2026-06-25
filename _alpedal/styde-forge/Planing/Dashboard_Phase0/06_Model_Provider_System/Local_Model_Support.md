# Local Model Support

**StydeForge Dashboard — Mission Control**
**Phase 0 Design Document**

---

## 1. Overview

The Dashboard supports local AI models via Ollama, llama.cpp, and other local inference servers. No internet connection required — everything runs on your own hardware.

---

## 2. Ollama

### 2.1 Auto-Detection

The Dashboard checks if Ollama is running locally at startup:

```
1. GET http://localhost:11434/api/tags
   └─ 200: Ollama detected! Add as provider
   └─ Connection refused: Ollama not installed → show installation guide
```

### 2.2 Ollama Provider

```typescript
class OllamaProvider implements ModelProvider {
  name = "ollama";
  displayName = "Ollama (Local)";
  icon = "🦙";
  baseURL = "http://localhost:11434/v1";  // OpenAI-compatible API

  // Models auto-discovered
  async listModels(): Promise<Model[]> {
    const response = await fetch("http://localhost:11434/api/tags");
    const data = await response.json();
    return data.models.map(m => ({
      id: `ollama:${m.name}`,
      name: m.name,
      contextWindow: m.details?.context_length || 4096,
      maxOutputTokens: 4096
    }));
  }
}
```

---

## 3. Ollama — Installation Guide (in-app)

```
┌──────────────────────────────────────────────────┐
│ 🦙 Ollama Not Detected                           │
├──────────────────────────────────────────────────┤
│                                                  │
│ Ollama lets you run AI models locally            │
│ on your own hardware. No internet required.      │
│                                                  │
│ Steps to get started:                            │
│                                                  │
│ 1. Install Ollama:                               │
│    [Download from ollama.com]                    │
│                                                  │
│ 2. Pull a model:                                 │
│    $ ollama pull llama3.2                        │
│    $ ollama pull deepseek-r1:8b                  │
│    $ ollama pull codellama:7b                    │
│                                                  │
│ 3. Restart the Dashboard                         │
│    → Ollama appears automatically                │
│                                                  │
│ [I already have Ollama — Test again]             │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## 4. GPU Detection

The Dashboard reports GPU usage for local models:

```
┌──────────────────────────────────────────────────┐
│ 🦙 Ollama (Local)                                 │
│                                                   │
│ Models:                                           │
│ • llama3.2:3b          GPU: 2.1GB    │ 3080     │
│ • deepseek-r1:8b       GPU: 5.8GB    │ 3080     │
│ • codellama:7b         GPU: 4.2GB    │ 3070 Ti  │
│                                                   │
│ VRAM available: 10.6GB / 18GB total               │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## 5. Recommended Models (by Hardware)

Based on the user's hardware (18GB VRAM total):

| Model | Size | VRAM | Recommendation |
|--------|------|------|----------------|
| `llama3.2:3b` | 3B | ~2.5GB | ✅ Fast — good for simple tasks |
| `deepseek-r1:8b` | 8B | ~6GB | ✅ Good balance — code and reasoning |
| `codellama:7b` | 7B | ~5.5GB | ✅ Specialized for code |
| `llama3.1:8b` | 8B | ~6GB | ✅ General — good all-round |
| `qwen2.5:14b` | 14B | ~9GB | ⚠ Works but leaves little VRAM |
| `deepseek-r1:14b` | 14B | ~9GB | ⚠ Works — slower |
| `llama3.1:70b` | 70B | ~42GB | ❌ Too large — requires 2× GPU or quantization |

---

## 6. llama.cpp (Future)

For users who want maximum control:

```json
{
  "providers": {
    "llamacpp:local": {
      "name": "llamacpp:local",
      "displayName": "llama.cpp (Local)",
      "icon": "🔥",
      "baseURL": "http://localhost:8080/v1",
      "models": [
        {
          "id": "llamacpp:custom-model",
          "name": "Custom GGUF Model"
        }
      ]
    }
  }
}
```

---

## 7. Local vs Cloud — Auto-Select

The Dashboard can auto-select between local and cloud models based on:

| Factor | Local model | Cloud model |
|--------|-------------|-------------|
| Internet | Not required | Required |
| Speed | Depends on GPU | Generally faster |
| Cost | Free (electricity) | Per token |
| Quality | Smaller models | Larger models |
| Privacy | 100% local | Data leaves machine |
| Offline | ✅ | ❌ |

**Auto-select (future):**
- Internet down? → Local model
- Want to save money? → Local model
- Need max quality? → Cloud (deepseek-v4-pro)
- Sensitive data? → Local model

---

**Status:** Phase 0 — Design
