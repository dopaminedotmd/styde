RAG system breakdown for your stack:
Embedding model pipeline: Use Voyage-2 or BGE-M3 for multilingual support. Fine-tune with Matryoshka representation learning for flexible dimensionality. Output dims: 1024 with truncation to 256/512/768 at retrieval time.
Chunking strategy: Recursive semantic splitting. 512 token chunks with 128 overlap. Use cosine similarity breakpoints at 0.3 threshold between sentences. Add sliding window context: prefix each chunk with previous chunk summary via LLM.
Retrieval: Hybrid search. Dense via cosine on embeddings. Sparse via BM25 Okapi. Weighted fusion: 0.7 dense, 0.3 sparse. Use average precision score for dynamic weight adjustment per query.
Reranking: Cross-encoder stage after top-100 retrieval. Cohere rerank-v3 or BGE-reranker-v2. Cuts latency 40% versus full retrieval rerank. Top-10 passes to LLM.
Eval pipeline: Build test set with 200 queries per domain. Three human-labeled relevant docs each. Metrics: MRR@10, NDCG@5, Recall@50. Acceptable baseline: NDCG@5 > 0.85.
Critical gotcha: Embedding distribution drift over time. Set up weekly cosine similarity monitoring on corpus mean vector. Alert when shift exceeds 0.15. Triggers re-indexing.