# RAG — Retrieval-Augmented Generation

**Styde Forge v3.0 — Phase 0**
**Section:** 14_RAG_Retrieval

---

## 1. Purpose

Replace brute-force context injection with intelligent retrieval.
Instead of dumping all knowledge into every agent prompt, use embeddings
to find only the relevant chunks — faster, cheaper, sharper agents.

Runs on the idle RTX 3080 (10 GB VRAM). Costs nothing. Saves tokens.

---

## 2. Problem & Solution

```
BEFORE (no RAG):
  Agent prompt = persona + ALL knowledge + ALL skills + task
  → 8000 tokens → $0.002 per spawn → slow inference

AFTER (RAG):
  Agent prompt = persona + TOP 3 knowledge chunks + skills + task
  → 2000 tokens → $0.0005 per spawn → 4× faster
```

---

## 3. Architecture

```
                        ┌─────────────────────┐
                        │   01_KNOWLEDGE/      │
                        │   corpus.md          │
                        │   (source text)      │
                        └──────────┬──────────┘
                                   │
                        ┌──────────┴──────────┐
                        │   CHUNKER            │
                        │   Split into ~512    │
                        │   token chunks       │
                        └──────────┬──────────┘
                                   │
                        ┌──────────┴──────────┐
                        │   EMBEDDER (3080)    │
                        │   all-MiniLM-L6-v2   │
                        │   or bge-small-en    │
                        │   → 384-dim vectors  │
                        └──────────┬──────────┘
                                   │
                        ┌──────────┴──────────┐
                        │   VECTOR STORE       │
                        │   FAISS (in-memory)  │
                        │   or ChromaDB (disk) │
                        └──────────┬──────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
     ┌────────┴────────┐  ┌───────┴───────┐  ┌────────┴────────┐
     │  AGENT SPAWN    │  │  TEACHER      │  │  EVAL PIPELINE  │
     │  queries RAG    │  │  queries RAG  │  │  queries RAG    │
     │  for context    │  │  for patterns │  │  for rubric ref │
     └─────────────────┘  └───────────────┘  └─────────────────┘
```

---

## 4. Implementation

### 4.1 Chunking

```python
def chunk_knowledge(corpus_path: str, chunk_size: int = 512) -> list:
    """
    Split knowledge corpus into overlapping chunks.
    512 tokens ≈ 2000 chars. 10% overlap for context continuity.
    """
    text = read_file(corpus_path)
    chunks = []
    overlap = chunk_size // 10

    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        chunks.append({
            "id": f"chunk-{len(chunks):04d}",
            "text": chunk,
            "domain": extract_domain(corpus_path),
            "source": corpus_path
        })
    return chunks
```

### 4.2 Embedding (on RTX 3080)

```python
from sentence_transformers import SentenceTransformer

# Load once, reuse forever
model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim, ~80 MB
# Alternative: "BAAI/bge-small-en" — 384-dim, slightly better

def embed_chunks(chunks: list) -> np.ndarray:
    """Run on GPU (RTX 3080). ~1000 chunks/second."""
    texts = [c["text"] for c in chunks]
    return model.encode(texts, device="cuda", batch_size=64)
```

### 4.3 Vector Store (FAISS)

```python
import faiss

def build_index(embeddings: np.ndarray) -> faiss.Index:
    """FAISS flat index. Fast enough for <100K chunks."""
    dim = embeddings.shape[1]  # 384
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype("float32"))
    return index

def search(index, query_embedding, k=3) -> list:
    """Return top-k most relevant chunk IDs."""
    distances, ids = index.search(query_embedding.reshape(1, -1), k)
    return ids[0].tolist()
```

### 4.4 Retrieval at Spawn

```python
def get_rag_context(task: str, domain: str, k: int = 3) -> str:
    """
    Called before every agent spawn.
    1. Embed the task
    2. Search vector store
    3. Return top-k relevant knowledge chunks
    """
    query_embedding = model.encode([task], device="cuda")[0]
    chunk_ids = search(vector_index, query_embedding, k=k)

    context = ""
    for cid in chunk_ids:
        chunk = chunk_store[cid]
        context += f"## Relevant Knowledge ({chunk['domain']})\n"
        context += chunk["text"][:300] + "...\n\n"

    return context
```

---

## 5. Resource Usage

| Resource | Usage | Fits? |
|----------|-------|-------|
| VRAM (3080 10GB) | ~1 GB (model + index) | Yes — 9 GB free |
| RAM | ~2 GB (FAISS index + chunks) | Yes — 30 GB free |
| Disk (USB) | ~500 MB (index file) | Yes — within budget |
| Inference time | ~5ms per query | Negligible |

---

## 6. Integration Points

| Component | How RAG helps |
|-----------|---------------|
| Agent spawn | Inject top-3 relevant knowledge chunks into context |
| Teacher agent | Find similar past successes/failures for pattern analysis |
| Eval pipeline | Retrieve rubric examples for consistent judging |
| Historical Learning | Find similar agents across generations |
| Research agents | Find relevant prior research before searching web |

---

## 7. Index Rebuild Strategy

| Trigger | Action |
|---------|--------|
| New knowledge added | Rebuild index for that domain only |
| 50+ new chunks | Full index rebuild (takes ~30 sec) |
| Machine change | Rebuild on startup if FAISS index missing |
| Weekly | Full rebuild for optimization |

---

## 8. Cost Impact

| Metric | Without RAG | With RAG | Savings |
|--------|------------|----------|---------|
| Tokens per spawn | ~6000 | ~2000 | 67% |
| Cost per spawn | ~$0.001 | ~$0.0003 | 70% |
| Inference time | ~5 sec | ~2 sec | 60% |
| Agent quality | Baseline | Better (more relevant context) | Qualitative |
| GPU usage (3080) | 0% (idle) | ~10% (embeddings) | Using idle resource |

---

## 9. Combined with Caveman Ultra

```
Caveman Ultra alone:   70% token reduction
RAG alone:             67% token reduction
Both combined:         ~90% token reduction vs baseline

8000 tokens → 2400 (Caveman) → 800 (Caveman + RAG)
$0.002/spawn → $0.0006 → $0.0002
```

---

**Status:** Defined. Uses idle RTX 3080. Zero API cost. Phase 0 design.
