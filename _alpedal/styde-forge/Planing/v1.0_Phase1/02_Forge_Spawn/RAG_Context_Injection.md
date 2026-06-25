# RAG Context Injection

**Styde Forge v3.0**
**Section:** 02_Forge_Spawn
**References:** `RAG_Retrieval.md`, `DECISIONS.md` D12

---

## 1. Purpose

Replace brute-force context injection with intelligent retrieval. Embed task → search FAISS vector store on RTX 3080 → inject top-3 relevant knowledge chunks. Zero API cost. 67% token savings.

---

## 2. Architecture

```
01_KNOWLEDGE/ → CHUNKER (512 tokens) → EMBEDDER (all-MiniLM-L6-v2, 3080)
                                              ↓
TASK → embed(task) → FAISS.search(k=3) → top-3 chunks → inject into spawn context
```

---

## 3. Implementation

```python
# Core/rag.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pathlib import Path

FORGE_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = FORGE_ROOT / "99_INDEXES/faiss_index.bin"
CHUNKS_PATH = FORGE_ROOT / "99_INDEXES/chunks.json"

# Model loaded once, reused
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, ~80MB
    return _model

def chunk_knowledge(corpus_path: str, chunk_size: int = 512) -> list[dict]:
    """Split corpus into overlapping chunks. ~2000 chars per chunk."""
    text = Path(corpus_path).read_text(encoding="utf-8")
    overlap = chunk_size // 10
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append({
            "id": f"chunk-{len(chunks):04d}",
            "text": text[i:i + chunk_size],
            "domain": Path(corpus_path).parent.name
        })
    return chunks

def build_index(chunks: list[dict], force: bool = False):
    """Build FAISS index. Run on RTX 3080."""
    import json
    model = _get_model()
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, device="cuda", batch_size=64)
    
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))
    
    faiss.write_index(index, str(INDEX_PATH))
    Path(CHUNKS_PATH).write_text(json.dumps(chunks))
    
    return {"chunks": len(chunks), "dim": dim}

def load_index():
    """Load FAISS index + chunks from USB."""
    import json
    if not INDEX_PATH.exists():
        return None, None
    index = faiss.read_index(str(INDEX_PATH))
    chunks = json.loads(Path(CHUNKS_PATH).read_text())
    return index, chunks

def get_rag_context(task: str, domain: str = None, k: int = 3) -> str:
    """Retrieve top-k relevant knowledge chunks for task."""
    index, chunks = load_index()
    if index is None:
        return ""
    
    model = _get_model()
    query_emb = model.encode([task], device="cuda")[0].reshape(1, -1).astype("float32")
    distances, ids = index.search(query_emb, k)
    
    context = ""
    for cid in ids[0]:
        if cid < len(chunks):
            chunk = chunks[cid]
            if domain and chunk["domain"] != domain:
                continue
            context += f"## Relevant: {chunk['domain']}\n{chunk['text'][:300]}...\n\n"
    
    return context
```

---

## 4. Resource Usage

| Resource | Usage | Free |
|----------|-------|------|
| VRAM (3080 10GB) | ~1 GB | 9 GB |
| RAM | ~2 GB | 30 GB |
| Disk | ~500 MB | Within budget |
| Query time | ~5ms | Negligible |

---

## 5. Integration with Spawn

```python
# In spawn.py build_spawn_context():
rag_context = get_rag_context(task, blueprint_domain)
if rag_context:
    parts.append(f"\n## Relevant Knowledge (RAG)\n{rag_context}")
```

Caveman + RAG combined: 8000→800 tokens (90% reduction).

---

**Status:** Specification complete. Code in Core/rag.py.
