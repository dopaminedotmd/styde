rag-system-architect v1
domain: ai-opt
architecture-choices:
  embedding-model: voyage-large-2-instruct
    rationale: best general-purpose 1024d instruct-tuned embedder, supports query prefixes
    fallback: bge-m3 (multilingual, dense+sparse fused)
  chunking-strategy: hierarchical-sentence-window
    base-chunk: 512 tokens, 128 overlap (sentence-boundary-aware via spacy sentencizer)
    parent-window: 2048 tokens (reranker context)
    child-chunks: 256 tokens (dense retrieval units)
    metadata: doc_id, chunk_seq, section_h1, section_h2, page_num
  vector-db: qdrant
    distance: cosine
    index: HNSW, ef_construct=256, M=32
    dense-field: embedding (float32, 1024d)
    sparse-field: splade-v3 (bm25 fallback for hybrid mode)
    payload-indexes: doc_id, section_h1, source_type
  hybrid-search:
    dense-weight: 0.6
    sparse-weight: 0.4
    retrieval-k: 50 (first pass from each branch)
    fusion: rrf (reciprocal rank fusion, k=60)
  reranker: bge-reranker-v2-m3
    max-passage-len: 2048 tokens
    top-k-rerank: 20
    final-top-k: 5
  evaluation:
    metrics: ndcg@5, ndcg@10, mrr@10, recall@50
    ground-truth: annotated qrels per domain (finance, legal, code, general)
    ablation-tracking: chunk-size sweep, hybrid-weight sweep, top-k sweep
pipeline-stages:
  1-ingest:
    - normalize text (unicode NFC, strip control chars)
    - extract metadata (headers, structure, source)
    - hierarchical-sentence-window chunker
    - dense embed (voyage-large-2-instruct, prefix=Represent this document for retrieval:)
    - sparse encode (splade-v3 via onnx, quantized)
    - upsert to qdrant (dense + sparse + payload)
  2-retrieve:
    - embed query (same model, prefix=Represent this query for retrieval:)
    - dense search: top 50
    - sparse search: top 50 (or splade query encoder)
    - RRF fusion -> top 50 candidates
    - cross-encoder rerank -> top 5
  3-generate:
    - concat top-5 contexts in order (reranker score desc)
    - format: <context_i><text>...<source>...</context_i>
    - inject system prompt with citation instructions
    - llm generates answer + inline citations
optimization-targets:
  latency-p95-under: 800ms (embed+retrieve+rerank)
  recall-at-50: 0.92
  ndcg-at-5: 0.85
  chunk-storage-per-1m-docs: ~8gb (payload heavy)