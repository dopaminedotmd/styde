# Knowledge Management

**Styde Forge v3.0 — Phase 0**
**Section:** 11_Knowledge_Management

---

## 1. Purpose

Define how knowledge is created, stored, indexed, and retrieved within the
forge. Knowledge bases are one of the six content types that fill the USB.

---

## 2. Knowledge Lifecycle

```
ACQUIRE → SYNTHESIZE → INDEX → STORE → RETRIEVE → UPDATE
    │                                               │
    └───────────────────────────────────────────────┘
```

### Acquire
- Research agents search web, arXiv, docs
- Sources are captured with URLs and access dates
- Raw materials saved temporarily for synthesis

### Synthesize
- Agent processes multiple sources into coherent knowledge
- Redundancy removed, contradictions flagged
- Confidence levels assigned per finding

### Index
- `index.json` created per knowledge domain
- Full-text searchable
- Cross-references to related domains

### Store
- Written atomically to `01_KNOWLEDGE/<domain>/`
- `corpus.md` — the synthesized knowledge
- `sources/` — original source references
- `index.json` — searchable index

### Retrieve
- RAG system searches vector store for relevant chunks
- Query embedded on RTX 3080 (all-MiniLM-L6-v2, 384-dim)
- Top-k chunks injected into agent context
- Relevance scored by cosine similarity

### Update
- New research findings merged into existing corpus
- Version history tracked
- Outdated information flagged (not deleted)

---

## 3. Knowledge Domain Structure

```
01_KNOWLEDGE/
├── coding/                        # Coding patterns, best practices
│   ├── corpus.md
│   ├── index.json
│   └── sources/
├── research/                      # Research methodologies
│   ├── corpus.md
│   ├── index.json
│   └── sources/
├── automation/                    # Automation patterns
│   ├── corpus.md
│   ├── index.json
│   └── sources/
├── documentation/                 # Documentation standards
│   ├── corpus.md
│   ├── index.json
│   └── sources/
├── testing/                       # Testing methodologies
│   ├── corpus.md
│   ├── index.json
│   └── sources/
├── meta/                          # Forge self-knowledge
│   ├── corpus.md
│   ├── index.json
│   └── sources/
├── ai_ml/                         # AI/ML fundamentals
│   ├── corpus.md
│   ├── index.json
│   └── sources/
└── systems/                       # System design patterns
    ├── corpus.md
    ├── index.json
    └── sources/
```

---

## 4. Index Format (`index.json`)

```json
{
  "domain": "coding",
  "version": 3,
  "last_updated": "2026-06-25T12:00:00Z",
  "total_entries": 47,
  "entries": [
    {
      "id": "coding-001",
      "title": "SQL Injection Prevention",
      "tags": ["security", "sql", "python"],
      "confidence": "high",
      "sources": ["https://owasp.org/..."],
      "related": ["coding-012", "coding-033"],
      "last_verified": "2026-06-20T00:00:00Z"
    }
  ]
}
```

---

## 5. Knowledge Retrieval

```python
def get_knowledge_context(domain: str, task: str, max_entries: int = 5) -> str:
    """
    Retrieve relevant knowledge for agent context.

    1. Load domain index
    2. Match task keywords against entry tags
    3. Return top N most relevant entries
    4. Format as context string
    """
    index = load_json(f"01_KNOWLEDGE/{domain}/index.json")
    relevant = keyword_match(task, index["entries"])
    context = ""
    for entry in relevant[:max_entries]:
        context += f"## {entry['title']} (confidence: {entry['confidence']})\n"
        context += f"Source: {entry['sources'][0]}\n\n"
    return context
```

---

## 6. Quality Standards

| Standard | Requirement |
|----------|-------------|
| Sources | Minimum 2 independent sources per claim |
| Confidence | Explicit high/medium/low per entry |
| Currency | Entries verified within last 90 days |
| Non-redundancy | No duplicate entries across domains |
| Traceability | Every claim links to source |

---

**Status:** Defined. Knowledge lifecycle, 8 domains, index schema.
