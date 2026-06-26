NDCG target observed: 0.87
Chunking strategy for current corpus
  strategy: recursive_character
  chunk_size: 512
  overlap: 64
  separator_priority:
    - \\n\\n
    - \\n
    - .
    - ' '
Embedding model selection
  primary: voyage-2
  fallback: text-embedding-3-small
  dimension: 1024
  normalization: l2
Hybrid search weights
  dense_weight: 0.6
  sparse_weight: 0.4
  sparse_model: splade-v3
Reranking config
  model: BAAI/bge-reranker-v2-m3
  top_k_candidates: 50
  final_k: 10
Evaluation results from last run
  ndcg_at_10: 0.87
  mrr_at_10: 0.83
  recall_at_20: 0.94
  precision_at_5: 0.68
Recommended next action
  tune: chunk_size down to 384
  reason: ndcg plateaued at 512, smaller segments reduce noise for dense-only queries
  add: query_expansion step before retrieve
  technique: hyde (hypothetical document embeddings)