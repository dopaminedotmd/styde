RAG SYSTEM ARCHITECTURE FRAMEWORK
Embedding Strategy:
  model: voyage-3-large
  dimensions: 1024
  fallback: text-embedding-3-small (384d)
  pooling: cls (for voyage), mean (for openai)
  normalization: l2 normalize all vectors
  fine_tune: True
  fine_tune_data: domain-specific query-doc pairs
  fine_tune_method: cosent loss with hard negatives
  eval_metric: NDCG@10
Chunking Strategy:
  chunk_size: 512
  chunk_overlap: 64
  strategy: semantic (split on section boundaries first, then sentence)
  fallback: recursive character split
  min_chunk_chars: 128
  max_chunk_chars: 1024
  metadata_preserved: title, section, page_num, doc_id, chunk_idx, parent_chunk_id
Index Structure:
  dense_index: faiss (ivf_flat, nprobe=10)
  sparse_index: bm25 (custom tokenizer, k1=1.5, b=0.75)
  hybrid_alpha: 0.7 (dense_weight) / 0.3 (sparse_weight)
  reranker: cohere-rerank-v3 (cross-encoder, top 50 -> top 10)
  vector_db: qdrant (local on-prem, grpc)
Retrieval Pipeline:
  query -> query_expansion (2 alternate queries via llm) -> embed -> hybrid_search -> top_k=50 -> rerank -> top_k=10 -> context_assembly
Query Expansion:
  generate 2 paraphrases
  embed all 3 (original + 2 expansions)
  take mean embedding
  optional: add hyde (hypothetical doc embedding) for abstract queries
Reranking Pipeline:
  cross_encoder: cohere-rerank-v3
  candidates_per_query: 50
  final_k: 10
  threshold: min_score 0.3 (discard irrelevant)
  batch_size: 16
Evaluation:
  metrics: NDCG@5, NDCG@10, MRR@10, Recall@10, precision@5
  test_set: 500 annotated query-relevance pairs
  ab_test: every deployment gets 1 week live a/b
  monitoring: p95 latency < 500ms, recall@10 > 0.85
Production Architecture:
  ingestion: parallel doc processing, 16 workers
  index_update: daily full rebuild, incremental updates every 15 min
  cache: redis (query-result pairs, ttl=1hr)
  fallback: if vector db down -> bm25 only
  circuit_breaker: 5 consecutive failures -> fallback mode, retry after 30s