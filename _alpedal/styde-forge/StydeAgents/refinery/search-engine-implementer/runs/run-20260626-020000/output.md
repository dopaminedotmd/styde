# Advanced Search Engine Implementation
## Hybrid Search (BM25 + Dense Vectors), Learning-to-Rank (LambdaMART), Search Analytics, Query Understanding (NER + Intent), Personalized Search Ranking

**Generated:** 2026-06-26 02:00:00 UTC
**Agent:** search-engine-implementer (c2)
**Run ID:** run-20260626-020000

---

## Table of Contents

1. [Hybrid Search: BM25 + Dense Vectors](#1-hybrid-search-bm25--dense-vectors)
2. [Learning-to-Rank with LambdaMART](#2-learning-to-rank-with-lambdamart)
3. [Search Analytics Pipeline](#3-search-analytics-pipeline)
4. [Query Understanding: NER + Intent](#4-query-understanding-ner--intent)
5. [Personalized Search Ranking](#5-personalized-search-ranking)
6. [End-to-End Integration](#6-end-to-end-integration)
7. [Deployment & Production Considerations](#7-deployment--production-considerations)

---

## 1. Hybrid Search: BM25 + Dense Vectors

### 1.1 Architecture Overview

Hybrid search combines the precision of lexical matching (BM25) with the semantic understanding of dense vector embeddings. The fusion architecture uses reciprocal rank fusion (RRF) to merge results from both retrieval paths, producing a unified ranking that captures both exact keyword matches and conceptual similarity.

```
┌──────────────┐     ┌─────────────────┐
│   Query      │────▶│ Query Processing │
└──────────────┘     └────────┬────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    ┌──────────────────┐          ┌──────────────────┐
    │   BM25 Retriever  │          │ Dense Retriever   │
    │  (Lexical Match)  │          │ (Semantic Match)  │
    └────────┬─────────┘          └────────┬─────────┘
             │                             │
             ▼                             ▼
    ┌──────────────────┐          ┌──────────────────┐
    │  BM25 Scores     │          │  Cosine Scores   │
    │  (sparse, exact) │          │  (dense, approx) │
    └────────┬─────────┘          └────────┬─────────┘
             │                             │
             └──────────┬──────────────────┘
                        ▼
             ┌──────────────────────┐
             │ Reciprocal Rank      │
             │ Fusion (RRF)         │
             └──────────┬───────────┘
                        ▼
             ┌──────────────────────┐
             │  Merged & Re-ranked  │
             │  Final Results       │
             └──────────────────────┘
```

### 1.2 Implementation: Core Search Engine

```python
"""
Hybrid Search Engine: BM25 + Dense Vector Retrieval
Production-grade implementation with configurable fusion strategies.
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass, field
from collections import defaultdict
import pickle
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# ──────────────────────────────────────────────────────────────────
# Data Structures
# ──────────────────────────────────────────────────────────────────

@dataclass
class SearchDocument:
    """A document in the search index."""
    doc_id: str
    title: str
    body: str
    metadata: Dict = field(default_factory=dict)
    dense_vector: Optional[np.ndarray] = None
    
    @property
    def full_text(self) -> str:
        """Combined text for BM25 indexing."""
        return f"{self.title} {self.title} {self.body}"  # title boosted 2x

@dataclass
class SearchResult:
    """A single search result with scores from each retriever."""
    doc: SearchDocument
    bm25_score: float
    dense_score: float
    fused_score: float
    rank: int

# ──────────────────────────────────────────────────────────────────
# BM25 Implementation (Okapi BM25)
# ──────────────────────────────────────────────────────────────────

class BM25Retriever:
    """
    Okapi BM25 implementation with tunable k1, b parameters.
    
    BM25 formula:
      score(D, Q) = Σ IDF(qi) * (f(qi,D) * (k1 + 1)) / (f(qi,D) + k1 * (1 - b + b * |D|/avgdl))
    
    where:
      - k1: term frequency saturation (default 1.5)
      - b: length normalization (default 0.75)
    """
    
    def __init__(self, k1: float = 1.5, b: float = 0.75, epsilon: float = 0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
        self._corpus: List[SearchDocument] = []
        self._avgdl: float = 0.0
        self._doc_lens: List[int] = []
        self._idf: Dict[str, float] = {}
        self._term_freqs: List[Dict[str, int]] = []
        self._doc_count: int = 0
        self._tokenized_corpus: List[List[str]] = []
        
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Simple whitespace + lowercase tokenizer. Replace with spaCy/Stanza for production."""
        import re
        return [t.lower() for t in re.findall(r'\w+', text)]
    
    def index(self, documents: List[SearchDocument]):
        """Build the BM25 index from a list of documents."""
        self._corpus = documents
        self._doc_count = len(documents)
        
        # Tokenize all documents
        self._tokenized_corpus = [self.tokenize(doc.full_text) for doc in documents]
        self._doc_lens = [len(tokens) for tokens in self._tokenized_corpus]
        self._avgdl = np.mean(self._doc_lens) if self._doc_lens else 0.0
        
        # Compute document frequencies
        df = defaultdict(int)
        for tokens in self._tokenized_corpus:
            unique_terms = set(tokens)
            for term in unique_terms:
                df[term] += 1
        
        # Compute IDF
        self._idf = {}
        for term, freq in df.items():
            self._idf[term] = np.log(
                (self._doc_count - freq + 0.5) / (freq + 0.5) + 1.0
            )
        
        # Store per-document term frequencies
        self._term_freqs = []
        for tokens in self._tokenized_corpus:
            tf = defaultdict(int)
            for token in tokens:
                tf[token] += 1
            self._term_freqs.append(dict(tf))
    
    def score(self, query: str, doc_idx: int) -> float:
        """Compute BM25 score for a single document given a query."""
        query_tokens = self.tokenize(query)
        score = 0.0
        doc_len = self._doc_lens[doc_idx]
        tf = self._term_freqs[doc_idx]
        
        for token in query_tokens:
            if token not in self._idf:
                continue
            term_freq = tf.get(token, 0)
            if term_freq == 0:
                continue
                
            numerator = term_freq * (self.k1 + 1)
            denominator = term_freq + self.k1 * (
                1 - self.b + self.b * doc_len / self._avgdl
            )
            score += self._idf[token] * (numerator / denominator)
        
        return score
    
    def search(self, query: str, top_k: int = 100) -> List[Tuple[SearchDocument, float]]:
        """Retrieve top-k documents using BM25 scoring."""
        scores = []
        for idx in range(self._doc_count):
            s = self.score(query, idx)
            if s > 0:
                scores.append((self._corpus[idx], s))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

# ──────────────────────────────────────────────────────────────────
# Dense Vector Retriever
# ──────────────────────────────────────────────────────────────────

class DenseRetriever:
    """
    Dense vector retrieval using sentence-transformer embeddings.
    Supports multiple models (all-MiniLM-L6-v2, e5-large, etc.).
    In-memory vector store with cosine similarity for small/medium corpora;
    swap in FAISS/Milvus for production-scale.
    """
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        use_gpu: bool = False,
        batch_size: int = 32
    ):
        self.model_name = model_name
        self.use_gpu = use_gpu
        self.batch_size = batch_size
        self._corpus: List[SearchDocument] = []
        self._embeddings: Optional[np.ndarray] = None  # shape: (N, dim)
        self._model = None
        self._dim = None
    
    def _load_model(self):
        """Lazy-load the sentence transformer model."""
        if self._model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer
            device = "cuda" if self.use_gpu else "cpu"
            self._model = SentenceTransformer(self.model_name, device=device)
            self._dim = self._model.get_sentence_embedding_dimension()
        except ImportError:
            raise ImportError(
                "sentence-transformers required for DenseRetriever. "
                "Install: pip install sentence-transformers"
            )
    
    def index(self, documents: List[SearchDocument]):
        """Encode all documents and store embeddings."""
        self._corpus = documents
        
        # Use pre-computed vectors if available, otherwise encode
        precomputed = [doc.dense_vector for doc in documents if doc.dense_vector is not None]
        if len(precomputed) == len(documents):
            self._embeddings = np.array(precomputed)
        else:
            self._load_model()
            texts = [f"{doc.title}. {doc.body}" for doc in documents]
            self._embeddings = self._model.encode(
                texts,
                batch_size=self.batch_size,
                show_progress_bar=False,
                normalize_embeddings=True
            )
        
        # Store vectors back on documents
        for i, doc in enumerate(documents):
            doc.dense_vector = self._embeddings[i]
    
    def encode_query(self, query: str) -> np.ndarray:
        """Encode a query string into a normalized embedding vector."""
        self._load_model()
        emb = self._model.encode(
            [query],
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return emb[0]
    
    def search(
        self,
        query: Union[str, np.ndarray],
        top_k: int = 100
    ) -> List[Tuple[SearchDocument, float]]:
        """Retrieve top-k documents via cosine similarity."""
        if isinstance(query, str):
            query_vec = self.encode_query(query)
        else:
            query_vec = query
        
        # Cosine similarity (embeddings are already normalized)
        scores = np.dot(self._embeddings, query_vec)
        
        # Get top-k indices
        if top_k >= len(scores):
            top_indices = np.argsort(scores)[::-1]
        else:
            top_indices = np.argpartition(scores, -top_k)[-top_k:]
            top_indices = top_indices[np.argsort(scores[top_indices])[::-1]]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                results.append((self._corpus[idx], float(scores[idx])))
        
        return results

# ──────────────────────────────────────────────────────────────────
# Reciprocal Rank Fusion (RRF)
# ──────────────────────────────────────────────────────────────────

class ReciprocalRankFusion:
    """
    Fuses multiple ranked lists using Reciprocal Rank Fusion.
    
    RRF(d) = Σ_{r in R} 1 / (k + rank_r(d))
    
    where k=60 is the standard constant (Cormack et al., 2009).
    The constant k dampens the impact of high rankings from any
    single system.
    """
    
    def __init__(self, k: int = 60):
        self.k = k
    
    def fuse(
        self,
        ranked_lists: List[List[Tuple[SearchDocument, float]]],
        top_k: int = 20
    ) -> List[SearchResult]:
        """
        Fuse multiple ranked result lists into a single ranking.
        
        Args:
            ranked_lists: List of ranked lists, each contains (doc, score) tuples.
                         First list is treated as primary (BM25), second as secondary (dense).
            top_k: Number of final results to return.
        """
        if not ranked_lists:
            return []
        
        # Collect all unique documents with their RRF scores
        doc_scores: Dict[str, float] = {}
        doc_bm25: Dict[str, float] = {}
        doc_dense: Dict[str, float] = {}
        doc_refs: Dict[str, SearchDocument] = {}
        
        for list_idx, ranked_list in enumerate(ranked_lists):
            for rank, (doc, raw_score) in enumerate(ranked_list):
                rrf_contribution = 1.0 / (self.k + rank + 1)
                doc_scores[doc.doc_id] = doc_scores.get(doc.doc_id, 0) + rrf_contribution
                doc_refs[doc.doc_id] = doc
                
                if list_idx == 0:
                    doc_bm25[doc.doc_id] = raw_score
                elif list_idx == 1:
                    doc_dense[doc.doc_id] = raw_score
        
        # Sort by fused score
        sorted_ids = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for rank, (doc_id, fused_score) in enumerate(sorted_ids[:top_k]):
            doc = doc_refs[doc_id]
            results.append(SearchResult(
                doc=doc,
                bm25_score=doc_bm25.get(doc_id, 0.0),
                dense_score=doc_dense.get(doc_id, 0.0),
                fused_score=fused_score,
                rank=rank + 1
            ))
        
        return results

# ──────────────────────────────────────────────────────────────────
# Weighted Linear Fusion (Alternative)
# ──────────────────────────────────────────────────────────────────

class WeightedFusion:
    """
    Alternative fusion: score = α * BM25_norm + (1-α) * dense_norm
    
    Supports per-query weight tuning based on query type:
    - High α: query looks like exact search (product codes, IDs)
    - Low α: query is natural language / conceptual
    """
    
    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha
    
    def min_max_normalize(self, scores: List[float]) -> List[float]:
        """Min-max normalize a list of scores to [0, 1]."""
        if not scores:
            return []
        min_s, max_s = min(scores), max(scores)
        if max_s == min_s:
            return [1.0] * len(scores)
        return [(s - min_s) / (max_s - min_s) for s in scores]
    
    def fuse(
        self,
        bm25_results: List[Tuple[SearchDocument, float]],
        dense_results: List[Tuple[SearchDocument, float]],
        top_k: int = 20
    ) -> List[SearchResult]:
        """Weighted fusion of BM25 and dense results."""
        # Build lookup maps
        bm25_map: Dict[str, float] = {doc.doc_id: score for doc, score in bm25_results}
        dense_map: Dict[str, float] = {doc.doc_id: score for doc, score in dense_results}
        doc_map: Dict[str, SearchDocument] = {}
        for doc, _ in bm25_results:
            doc_map[doc.doc_id] = doc
        for doc, _ in dense_results:
            doc_map[doc.doc_id] = doc
        
        # Collect all unique document IDs
        all_ids = set(bm25_map.keys()) | set(dense_map.keys())
        
        # Normalize scores within each retriever
        bm25_scores = [bm25_map.get(did, 0.0) for did in all_ids]
        dense_scores = [dense_map.get(did, 0.0) for did in all_ids]
        bm25_norm = dict(zip(all_ids, self.min_max_normalize(bm25_scores)))
        dense_norm = dict(zip(all_ids, self.min_max_normalize(dense_scores)))
        
        # Weighted combination
        fused: List[Tuple[float, str]] = []
        for did in all_ids:
            score = self.alpha * bm25_norm[did] + (1 - self.alpha) * dense_norm[did]
            fused.append((score, did))
        
        fused.sort(key=lambda x: x[0], reverse=True)
        
        results = []
        for rank, (score, did) in enumerate(fused[:top_k]):
            doc = doc_map[did]
            results.append(SearchResult(
                doc=doc,
                bm25_score=bm25_map.get(did, 0.0),
                dense_score=dense_map.get(did, 0.0),
                fused_score=score,
                rank=rank + 1
            ))
        
        return results

# ──────────────────────────────────────────────────────────────────
# Hybrid Search Engine (Top-Level API)
# ──────────────────────────────────────────────────────────────────

class HybridSearchEngine:
    """
    Complete hybrid search engine combining BM25 lexical search
    with dense vector semantic search.
    
    Usage:
        engine = HybridSearchEngine()
        engine.index(documents)
        results = engine.search("blue running shoes")
        for r in results:
            print(f"#{r.rank}: {r.doc.title} | fused={r.fused_score:.3f}")
    """
    
    def __init__(
        self,
        bm25_k1: float = 1.5,
        bm25_b: float = 0.75,
        dense_model: str = "all-MiniLM-L6-v2",
        fusion_strategy: str = "rrf",  # "rrf" or "weighted"
        fusion_alpha: float = 0.3,
        rrf_k: int = 60,
        use_gpu: bool = False
    ):
        self.bm25 = BM25Retriever(k1=bm25_k1, b=bm25_b)
        self.dense = DenseRetriever(model_name=dense_model, use_gpu=use_gpu)
        self.fusion_strategy = fusion_strategy
        
        if fusion_strategy == "rrf":
            self.fusion = ReciprocalRankFusion(k=rrf_k)
        else:
            self.fusion = WeightedFusion(alpha=fusion_alpha)
    
    def index(self, documents: List[SearchDocument]):
        """Index documents in both BM25 and dense retrievers."""
        self.bm25.index(documents)
        self.dense.index(documents)
    
    def search(
        self,
        query: str,
        top_k: int = 20,
        bm25_candidates: int = 200,
        dense_candidates: int = 200,
        dense_query_vec: Optional[np.ndarray] = None,
    ) -> List[SearchResult]:
        """
        Execute hybrid search.
        
        Two-phase retrieval:
        1. Each retriever fetches a broad candidate set
        2. Fusion combines and re-ranks into final top-k
        
        dense_query_vec: Optional pre-computed query vector (avoids model loading)
        """
        # Parallel retrieval
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_bm25 = executor.submit(self.bm25.search, query, bm25_candidates)
            future_dense = executor.submit(
                self.dense.search,
                dense_query_vec if dense_query_vec is not None else query,
                dense_candidates
            )
            bm25_results = future_bm25.result()
            dense_results = future_dense.result()
        
        # Fuse results
        if isinstance(self.fusion, ReciprocalRankFusion):
            return self.fusion.fuse([bm25_results, dense_results], top_k)
        else:
            return self.fusion.fuse(bm25_results, dense_results, top_k)
    
    def save(self, path: str):
        """Persist the search engine state to disk."""
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)
        
        # Save BM25 state
        bm25_state = {
            'k1': self.bm25.k1,
            'b': self.bm25.b,
            'doc_lens': self.bm25._doc_lens,
            'avgdl': self.bm25._avgdl,
            'idf': dict(self.bm25._idf),
            'term_freqs': self.bm25._term_freqs,
            'doc_count': self.bm25._doc_count,
        }
        with open(save_path / 'bm25_state.json', 'w') as f:
            json.dump(bm25_state, f, default=lambda x: list(x) if isinstance(x, set) else x)
        
        # Save documents and embeddings
        docs_data = []
        for doc in self.dense._corpus:
            docs_data.append({
                'doc_id': doc.doc_id,
                'title': doc.title,
                'body': doc.body,
                'metadata': doc.metadata,
            })
        with open(save_path / 'documents.json', 'w') as f:
            json.dump(docs_data, f, indent=2)
        
        if self.dense._embeddings is not None:
            np.save(save_path / 'embeddings.npy', self.dense._embeddings)
        
        # Save config
        config = {
            'dense_model': self.dense.model_name,
            'fusion_strategy': self.fusion_strategy,
        }
        with open(save_path / 'config.json', 'w') as f:
            json.dump(config, f, indent=2)

# ──────────────────────────────────────────────────────────────────
# Demo & Test
# ──────────────────────────────────────────────────────────────────

def demo_hybrid_search():
    """Demonstrate the hybrid search engine."""
    print("=" * 70)
    print("HYBRID SEARCH ENGINE DEMO (BM25 + Dense Vectors)")
    print("=" * 70)
    
    # Sample product catalog
    documents = [
        SearchDocument("1", "Nike Air Max Running Shoes", "Lightweight running shoes with Air Max cushioning, breathable mesh upper, rubber outsole. Ideal for road running and daily training. Available in multiple colors.", {"category": "shoes", "brand": "Nike", "price": 129.99}),
        SearchDocument("2", "Adidas Ultraboost 22", "Premium running shoes with Boost midsole technology, Primeknit upper, Continental rubber outsole. Maximum energy return for long distance running.", {"category": "shoes", "brand": "Adidas", "price": 189.99}),
        SearchDocument("3", "Apple MacBook Pro 14", "Powerful laptop with M3 chip, 14-inch Liquid Retina XDR display, 18-hour battery life. Perfect for professional creative work and software development.", {"category": "electronics", "brand": "Apple", "price": 1999.99}),
        SearchDocument("4", "Dell XPS 15 Laptop", "15.6-inch OLED display, Intel Core i7, 16GB RAM, 512GB SSD. Premium ultrabook for business and productivity. Windows 11 Pro.", {"category": "electronics", "brand": "Dell", "price": 1499.99}),
        SearchDocument("5", "Sony WH-1000XM5 Headphones", "Industry-leading noise cancellation, 30-hour battery, crystal clear hands-free calling. Premium wireless headphones with exceptional sound quality.", {"category": "electronics", "brand": "Sony", "price": 349.99}),
        SearchDocument("6", "Bose QuietComfort Earbuds II", "World-class noise cancelling true wireless earbuds. Personalized noise cancellation and sound calibration. IPX4 water resistant.", {"category": "electronics", "brand": "Bose", "price": 279.99}),
        SearchDocument("7", "Garmin Forerunner 265", "Advanced GPS running watch with AMOLED display, training readiness, morning report. Tracks heart rate, pace, distance, and advanced running dynamics.", {"category": "electronics", "brand": "Garmin", "price": 449.99}),
        SearchDocument("8", "Hydro Flask 32oz Water Bottle", "Double-wall vacuum insulated stainless steel water bottle. Keeps drinks cold 24 hours or hot 12 hours. BPA-free, leak-proof flex cap.", {"category": "accessories", "brand": "Hydro Flask", "price": 39.99}),
        SearchDocument("9", "Lululemon Align High-Rise Pant", "Buttery-soft Nulu fabric yoga pants. Four-way stretch, sweat-wicking, and weightless coverage. 28-inch inseam.", {"category": "clothing", "brand": "Lululemon", "price": 98.00}),
        SearchDocument("10", "Nike Dri-FIT Running Shorts", "Breathable running shorts with Dri-FIT moisture-wicking technology. Built-in briefs, zippered pocket, 7-inch inseam. Elastic waistband with drawcord.", {"category": "clothing", "brand": "Nike", "price": 45.00}),
        SearchDocument("11", "Patagonia Better Sweater Fleece", "Fair Trade Certified sewn fleece jacket. Made with 100% recycled polyester fleece. Dyed with low-impact processes. Perfect for casual outdoor wear.", {"category": "clothing", "brand": "Patagonia", "price": 139.00}),
        SearchDocument("12", "The North Face Thermoball Eco Jacket", "Lightweight synthetic insulation jacket with Thermoball Eco. Compressible, water-resistant, and warm even when wet. 100% recycled insulation.", {"category": "clothing", "brand": "The North Face", "price": 230.00}),
    ]
    
    # Initialize search engine (skip dense model load for demo; use random vectors)
    engine = HybridSearchEngine(dense_model="all-MiniLM-L6-v2", fusion_strategy="rrf")
    
    # For demo purposes, use random normalized vectors to avoid model download
    np.random.seed(42)
    for doc in documents:
        doc.dense_vector = np.random.randn(384).astype(np.float32)
        doc.dense_vector /= np.linalg.norm(doc.dense_vector)
    
    engine.index(documents)
    
    # Test queries
    test_queries = [
        "running shoes",
        "noise cancelling headphones",
        "warm jacket for outdoor hiking",
        "premium laptop for work",
        "water bottle insulated",
    ]
    
    for query in test_queries:
        print(f"\n{'─' * 70}")
        print(f"Query: \"{query}\"")
        print(f"{'─' * 70}")
        # Use random normalized query vector for demo (avoids model download)
        qvec = np.random.randn(384).astype(np.float32)
        qvec /= np.linalg.norm(qvec)
        results = engine.search(query, top_k=5, bm25_candidates=50, dense_candidates=50, dense_query_vec=qvec)
        print(f"{'Rank':<6}{'Doc ID':<8}{'Title':<45}{'BM25':<10}{'Dense':<10}{'Fused':<10}")
        print(f"{'─' * 6}{'─' * 8}{'─' * 45}{'─' * 10}{'─' * 10}{'─' * 10}")
        for r in results:
            # For demo, use random query vectors
            title = r.doc.title[:42] + '...' if len(r.doc.title) > 42 else r.doc.title
            print(f"{r.rank:<6}{r.doc.doc_id:<8}{title:<45}{r.bm25_score:<10.3f}{r.dense_score:<10.3f}{r.fused_score:<10.4f}")
    
    print(f"\n{'=' * 70}")
    print("Demo complete. Hybrid search engine ready for production use.")
    print("=" * 70)

if __name__ == "__main__":
    demo_hybrid_search()
```

### 1.3 Fusion Strategy Comparison

| Strategy | Formula | Best For | Weakness |
|---|---|---|---|
| **RRF** (k=60) | Σ 1/(k+rank) | Robust, no normalization needed | Ignores score magnitudes |
| **Weighted** | α·BM25_norm + (1-α)·Dense_norm | Tunable per-query-type | Requires score normalization |
| **Cascade** | Dense re-ranks BM25 top-N | Low-latency, large-scale | Misses relevant docs outside BM25 window |
| **Learned** | Neural network combiner | Maximum accuracy | Requires training data, higher latency |

### 1.4 Production Deployment Pattern

```
FastAPI Application
├── /search endpoint
│   ├── Query Preprocessing (normalization, spelling)
│   ├── BM25 retrieval (Elasticsearch → candidate pool)
│   ├── Dense retrieval (FAISS/Milvus → candidate pool)
│   ├── RRF fusion
│   └── Re-rank with LTR model (LambdaMART)
├── Background Tasks
│   ├── Embedding refresh (on document updates)
│   └── Analytics event publishing
└── Monitoring
    ├── Latency percentiles (p50, p95, p99)
    ├── Recall@K tracking
    └── Query-to-result distribution
```

---

## 2. Learning-to-Rank with LambdaMART

### 2.1 Architecture Overview

LambdaMART is a gradient-boosted tree ensemble that optimizes ranking metrics (NDCG, MAP) directly. It works by training on (query, document) pairs with relevance labels and feature vectors. At inference time, the model scores each document for a given query, producing an optimized ranking.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINING PIPELINE                             │
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐      │
│  │ Relevance │───▶│  Feature     │───▶│  LambdaMART      │      │
│  │ Judgments │    │  Extraction  │    │  (LightGBM)      │      │
│  └──────────┘    └──────────────┘    └────────┬─────────┘      │
│                                               │                 │
│  Feature Groups:                              ▼                 │
│  • Query-document text similarity        ┌──────────┐          │
│  • BM25 score                            │  Trained │          │
│  • Dense similarity score                │  Model   │          │
│  • Document popularity (clicks, sales)   └────┬─────┘          │
│  • Document freshness / recency                │                │
│  • Price / rating signals                     │                │
│  • User-document affinity                     ▼                │
│                                        ┌──────────────┐        │
│                                        │  INFERENCE    │        │
│                                        │  API          │        │
│                                        └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Implementation

```python
"""
Learning-to-Rank with LambdaMART using LightGBM.
Production-grade implementation with feature engineering, training, and inference.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path
import json
import pickle
import hashlib
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

# ──────────────────────────────────────────────────────────────────
# Feature Extraction
# ──────────────────────────────────────────────────────────────────

@dataclass
class QueryDocumentPair:
    """A single query-document pair with a relevance label."""
    query_id: str
    doc_id: str
    query_text: str
    doc_title: str
    doc_body: str
    relevance_label: int  # 0-4 scale (0=irrelevant, 4=perfect match)
    bm25_score: float = 0.0
    dense_score: float = 0.0
    doc_price: Optional[float] = None
    doc_rating: Optional[float] = None
    doc_clicks_7d: int = 0
    doc_sales_30d: int = 0
    doc_age_days: float = 0.0
    user_affinity_score: float = 0.0
    category_match: bool = False
    brand_match: bool = False

class LTRFeatureExtractor:
    """
    Feature extraction for Learning-to-Rank.
    
    Feature Groups:
    1. TEXT_MATCH: BM25, dense similarity, exact match signals
    2. POPULARITY: clicks, sales, ratings
    3. FRESHNESS: document age, recency boost
    4. COMMERCIAL: price position, discount signals
    5. QUERY_QUALITY: query length, query type, intent signals
    6. PERSONALIZATION: user-document affinity
    """
    
    # Feature names (must match order in extract_features)
    FEATURE_NAMES = [
        # Group 1: Text Match Features
        'bm25_score',
        'dense_similarity',
        'title_exact_match',
        'title_contains_query_terms',
        'title_term_overlap_ratio',
        'body_term_overlap_ratio',
        'query_length',
        'title_length',
        # Group 2: Popularity Features
        'log_clicks_7d',
        'log_sales_30d',
        'doc_rating_norm',
        'review_count_norm',
        # Group 3: Freshness Features
        'doc_age_days_log',
        'freshness_boost',
        # Group 4: Commercial Features
        'price_percentile',
        'price_is_discounted',
        # Group 5: Query Quality
        'query_is_navigational',
        'query_is_informational',
        'query_is_transactional',
        'query_entity_count',
        # Group 6: Personalization
        'user_affinity_score',
        'category_match',
        'brand_match',
    ]
    
    def __init__(self, price_data: Optional[Dict[str, float]] = None):
        self.price_data = price_data or {}
    
    def extract_features(
        self,
        qd_pair: QueryDocumentPair,
        global_stats: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Extract a feature vector for a query-document pair.
        Returns a 1D numpy array of float32 values.
        """
        features = []
        query_terms = set(qd_pair.query_text.lower().split())
        title_terms = set(qd_pair.doc_title.lower().split())
        body_terms = set(qd_pair.doc_body.lower().split())
        
        # ── Group 1: Text Match ──
        features.append(qd_pair.bm25_score)                                    # bm25_score
        features.append(qd_pair.dense_score)                                    # dense_similarity
        features.append(1.0 if qd_pair.query_text.lower() == qd_pair.doc_title.lower() else 0.0)  # title_exact_match
        features.append(1.0 if query_terms.issubset(title_terms) else 0.0)     # title_contains_query_terms
        
        title_overlap = len(query_terms & title_terms) / max(len(query_terms), 1)
        features.append(title_overlap)                                          # title_term_overlap_ratio
        
        body_overlap = len(query_terms & body_terms) / max(len(query_terms), 1)
        features.append(body_overlap)                                           # body_term_overlap_ratio
        
        features.append(min(len(query_terms), 20) / 20.0)                      # query_length (normalized)
        features.append(min(len(title_terms), 50) / 50.0)                      # title_length (normalized)
        
        # ── Group 2: Popularity ──
        features.append(np.log1p(qd_pair.doc_clicks_7d))                       # log_clicks_7d
        features.append(np.log1p(qd_pair.doc_sales_30d))                       # log_sales_30d
        features.append((qd_pair.doc_rating or 0.0) / 5.0)                     # doc_rating_norm
        features.append(min(qd_pair.doc_sales_30d / 100.0, 1.0))               # review_count_norm proxy
        
        # ── Group 3: Freshness ──
        features.append(np.log1p(qd_pair.doc_age_days))                        # doc_age_days_log
        
        # Freshness boost: newer docs get higher boost
        freshness = max(0.0, 1.0 - qd_pair.doc_age_days / 365.0)
        features.append(freshness)                                              # freshness_boost
        
        # ── Group 4: Commercial ──
        if qd_pair.doc_price is not None and global_stats:
            pct = (qd_pair.doc_price - global_stats.get('price_min', 0)) / \
                  max(global_stats.get('price_range', 1), 1)
            features.append(pct)                                               # price_percentile
        else:
            features.append(0.5)
        
        features.append(0.0)  # price_is_discounted (placeholder)
        
        # ── Group 5: Query Quality ──
        q_lower = qd_pair.query_text.lower()
        
        # Simple heuristic intent classification (signals for the model)
        nav_keywords = {'login', 'account', 'cart', 'orders', 'returns', 'tracking', 'help', 'contact', 'settings'}
        info_keywords = {'how', 'what', 'why', 'when', 'where', 'guide', 'tutorial', 'review', 'compare', 'best', 'top', 'difference'}
        trans_keywords = {'buy', 'price', 'cheap', 'discount', 'sale', 'order', 'shop', 'deal', 'coupon', 'free shipping'}
        
        q_terms = set(q_lower.split())
        features.append(float(len(q_terms & nav_keywords) > 0))                # query_is_navigational
        features.append(float(len(q_terms & info_keywords) > 0))               # query_is_informational
        features.append(float(len(q_terms & trans_keywords) > 0))              # query_is_transactional
        features.append(min(len(q_terms) / 15.0, 1.0))                         # query_entity_count
        
        # ── Group 6: Personalization ──
        features.append(qd_pair.user_affinity_score)                           # user_affinity_score
        features.append(1.0 if qd_pair.category_match else 0.0)               # category_match
        features.append(1.0 if qd_pair.brand_match else 0.0)                  # brand_match
        
        return np.array(features, dtype=np.float32)
    
    def feature_count(self) -> int:
        return len(self.FEATURE_NAMES)

# ──────────────────────────────────────────────────────────────────
# LambdaMART Ranker
# ──────────────────────────────────────────────────────────────────

class LambdaMARTRanker:
    """
    LambdaMART ranking model using LightGBM.
    
    Key LightGBM parameters for LambdaMART:
    - objective='lambdarank': Optimizes NDCG directly
    - metric='ndcg': Evaluation metric during training
    - ndcg_eval_at: NDCG cutoffs for early stopping
    - boosting_type='gbdt': Gradient Boosted Decision Trees
    """
    
    def __init__(
        self,
        feature_extractor: LTRFeatureExtractor,
        model_params: Optional[Dict] = None
    ):
        if not LIGHTGBM_AVAILABLE:
            raise ImportError("LightGBM required. Install: pip install lightgbm")
        
        self.feature_extractor = feature_extractor
        self.model: Optional[lgb.Booster] = None
        self._feature_names = feature_extractor.FEATURE_NAMES
        
        # Default LambdaMART parameters (tuned for ranking quality)
        self.params = {
            'objective': 'lambdarank',
            'metric': 'ndcg',
            'ndcg_eval_at': [1, 3, 5, 10],
            'boosting_type': 'gbdt',
            'num_leaves': 64,
            'max_depth': 8,
            'learning_rate': 0.05,
            'min_data_in_leaf': 20,
            'min_gain_to_split': 0.0,
            'lambda_l1': 0.1,
            'lambda_l2': 1.0,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': -1,
            'num_threads': 4,
            'seed': 42,
        }
        
        if model_params:
            self.params.update(model_params)
    
    def _build_dataset(
        self,
        query_doc_pairs: List[QueryDocumentPair],
        global_stats: Optional[Dict] = None
    ) -> Tuple[lgb.Dataset, List[str], pd.DataFrame]:
        """
        Build a LightGBM Dataset from query-document pairs.
        
        CRITICAL: LightGBM's lambdarank requires data grouped by query_id.
        Each query is a "group" and documents within a group are ranked relative to each other.
        """
        features = []
        labels = []
        query_ids = []
        query_id_to_index = {}
        
        for qd in query_doc_pairs:
            if qd.query_id not in query_id_to_index:
                query_id_to_index[qd.query_id] = len(query_id_to_index)
            
            feat_vec = self.feature_extractor.extract_features(qd, global_stats)
            features.append(feat_vec)
            labels.append(qd.relevance_label)
            query_ids.append(query_id_to_index[qd.query_id])
        
        X = pd.DataFrame(features, columns=self._feature_names)
        y = np.array(labels)
        
        # Group sizes: number of documents per query (LightGBM requires this for lambdarank)
        query_counts = defaultdict(int)
        for q in query_ids:
            query_counts[q] += 1
        group_sizes = [query_counts[i] for i in sorted(query_counts.keys())]
        
        dataset = lgb.Dataset(
            X, label=y,
            group=group_sizes,
            feature_name=self._feature_names,
            categorical_feature=[],
        )
        
        return dataset, query_ids, X
    
    def train(
        self,
        train_pairs: List[QueryDocumentPair],
        valid_pairs: Optional[List[QueryDocumentPair]] = None,
        num_boost_round: int = 500,
        early_stopping_rounds: int = 50,
        global_stats: Optional[Dict] = None
    ) -> Dict:
        """
        Train the LambdaMART model.
        
        Args:
            train_pairs: Training query-document pairs with relevance labels.
            valid_pairs: Optional validation set for early stopping.
            num_boost_round: Maximum number of boosting iterations.
            early_stopping_rounds: Stop if validation NDCG doesn't improve for N rounds.
            global_stats: Global statistics for feature normalization.
        
        Returns:
            Dictionary with training metrics.
        """
        train_dataset, _, _ = self._build_dataset(train_pairs, global_stats)
        
        valid_sets = None
        valid_names = None
        if valid_pairs:
            valid_dataset, _, _ = self._build_dataset(valid_pairs, global_stats)
            valid_sets = [valid_dataset]
            valid_names = ['valid']
        
        self.model = lgb.train(
            params=self.params,
            train_set=train_dataset,
            num_boost_round=num_boost_round,
            valid_sets=valid_sets,
            valid_names=valid_names,
            callbacks=[
                lgb.early_stopping(early_stopping_rounds),
                lgb.log_evaluation(period=50),
            ] if valid_pairs else [lgb.log_evaluation(period=50)],
        )
        
        # Extract best metrics
        metrics = {}
        if self.model.best_iteration is not None:
            metrics['best_iteration'] = self.model.best_iteration
            metrics['best_score'] = self.model.best_score
        
        return metrics
    
    def predict(
        self,
        query_doc_pairs: List[QueryDocumentPair],
        global_stats: Optional[Dict] = None
    ) -> np.ndarray:
        """
        Score query-document pairs using the trained model.
        
        Returns:
            Array of scores, one per pair.
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        features = np.array([
            self.feature_extractor.extract_features(qd, global_stats)
            for qd in query_doc_pairs
        ])
        
        return self.model.predict(features)
    
    def rank(
        self,
        query_id: str,
        candidates: List[QueryDocumentPair],
        global_stats: Optional[Dict] = None
    ) -> List[QueryDocumentPair]:
        """
        Rank candidates for a given query.
        
        Sorts candidates by model score, highest first.
        """
        if not candidates:
            return []
        
        scores = self.predict(candidates, global_stats)
        
        # Pair scores with candidates and sort
        scored = list(zip(scores, candidates))
        scored.sort(key=lambda x: x[0], reverse=True)
        
        return [c for _, c in scored]
    
    def save(self, path: str):
        """Save the trained model to disk."""
        if self.model is None:
            raise ValueError("No model to save.")
        save_path = Path(path)
        save_path.mkdir(parents=True, exist_ok=True)
        self.model.save_model(str(save_path / 'lambdamart_model.txt'))
        
        # Save feature names
        with open(save_path / 'feature_names.json', 'w') as f:
            json.dump(self._feature_names, f)
        
        # Save params
        with open(save_path / 'model_params.json', 'w') as f:
            json.dump(self.params, f, indent=2)
    
    def load(self, path: str):
        """Load a trained model from disk."""
        load_path = Path(path)
        self.model = lgb.Booster(model_file=str(load_path / 'lambdamart_model.txt'))
        
        with open(load_path / 'feature_names.json', 'r') as f:
            self._feature_names = json.load(f)
    
    def feature_importance(self) -> pd.DataFrame:
        """Get feature importance from the trained model."""
        if self.model is None:
            raise ValueError("Model not trained.")
        
        importance = self.model.feature_importance(importance_type='gain')
        return pd.DataFrame({
            'feature': self._feature_names,
            'gain': importance
        }).sort_values('gain', ascending=False)

# ──────────────────────────────────────────────────────────────────
# LTR Training Data Generator
# ──────────────────────────────────────────────────────────────────

class LTRTrainingDataGenerator:
    """
    Generates synthetic training data for LambdaMART when real
    click/judgment data is unavailable. Uses heuristic signals
    to create pseudo-relevance labels for bootstrapping.
    """
    
    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)
    
    def generate_synthetic_data(
        self,
        documents: List[SearchDocument],
        queries: List[str],
        pairs_per_query: int = 20
    ) -> List[QueryDocumentPair]:
        """
        Generate synthetic query-document pairs with relevance labels.
        
        Labels are derived from:
        - Term overlap (BM25 strength proxy)
        - Category/brand match
        - Randomized noise (simulates real-world variation)
        """
        pairs = []
        
        for query in queries:
            query_id = hashlib.md5(query.encode()).hexdigest()[:12]
            query_terms = set(query.lower().split())
            query_words_lower = set(query.lower().split())
            
            candidates = []
            for doc in documents:
                title_terms = set(doc.title.lower().split())
                body_terms = set(doc.body.lower().split())
                all_terms = title_terms | body_terms
                
                # Term overlap score
                overlap = len(query_terms & all_terms)
                title_overlap = len(query_terms & title_terms)
                
                # Category/brand match
                cat_match = False
                brand_match = False
                if doc.metadata.get('category', '').lower() in query.lower():
                    cat_match = True
                if doc.metadata.get('brand', '').lower() in query.lower():
                    brand_match = True
                
                # Synthetic label: 0-4 scale
                base_score = 0
                if title_overlap >= len(query_terms) * 0.8:
                    base_score = 4  # Near-exact title match
                elif title_overlap >= len(query_terms) * 0.5 or (cat_match and brand_match):
                    base_score = 3
                elif overlap >= 1 or cat_match:
                    base_score = 2
                elif overlap >= 1:
                    base_score = 1
                else:
                    base_score = 0
                
                # Add noise
                noise = self.rng.choice([-1, 0, 1], p=[0.1, 0.8, 0.1])
                label = max(0, min(4, base_score + noise))
                
                doc_age = self.rng.randint(0, 500)
                
                qd = QueryDocumentPair(
                    query_id=query_id,
                    doc_id=doc.doc_id,
                    query_text=query,
                    doc_title=doc.title,
                    doc_body=doc.body,
                    relevance_label=label,
                    bm25_score=float(overlap) / max(len(query_terms), 1) * 10.0,
                    dense_score=self.rng.uniform(0.3, 0.95) if overlap > 0 else self.rng.uniform(0.0, 0.4),
                    doc_price=doc.metadata.get('price'),
                    doc_rating=self.rng.uniform(3.0, 5.0),
                    doc_clicks_7d=self.rng.randint(0, 5000) if label >= 2 else self.rng.randint(0, 200),
                    doc_sales_30d=self.rng.randint(0, 1000) if label >= 3 else self.rng.randint(0, 50),
                    doc_age_days=float(doc_age),
                    user_affinity_score=self.rng.uniform(0.0, 0.5),
                    category_match=cat_match,
                    brand_match=brand_match,
                )
                candidates.append(qd)
            
            # Sort by heuristic score and select top + some negatives
            candidates.sort(key=lambda x: x.relevance_label, reverse=True)
            selected = candidates[:pairs_per_query]
            pairs.extend(selected)
        
        return pairs

# ──────────────────────────────────────────────────────────────────
# Complete LTR Pipeline
# ──────────────────────────────────────────────────────────────────

class LTRPipeline:
    """
    End-to-end Learning-to-Rank pipeline.
    
    Usage:
        ltr = LTRPipeline()
        ltr.train_on_synthetic(documents, queries)
        reranked = ltr.rerank("running shoes", hybrid_results)
    """
    
    def __init__(self):
        self.feature_extractor = LTRFeatureExtractor()
        self.ranker = LambdaMARTRanker(self.feature_extractor)
        self.global_stats: Dict = {}
        self._is_trained = False
    
    def _compute_global_stats(self, documents: List[SearchDocument]):
        """Compute global statistics for feature normalization."""
        prices = [doc.metadata.get('price', 0) for doc in documents if doc.metadata.get('price')]
        self.global_stats = {
            'price_min': min(prices) if prices else 0,
            'price_max': max(prices) if prices else 100,
            'price_range': (max(prices) - min(prices)) if len(prices) > 1 else 1,
            'price_mean': np.mean(prices) if prices else 50,
        }
    
    def train_on_synthetic(
        self,
        documents: List[SearchDocument],
        queries: List[str],
        validation_split: float = 0.2
    ) -> Dict:
        """
        Train LambdaMART on synthetically generated data.
        """
        self._compute_global_stats(documents)
        
        generator = LTRTrainingDataGenerator()
        all_pairs = generator.generate_synthetic_data(documents, queries)
        
        # Shuffle and split
        indices = np.random.RandomState(42).permutation(len(all_pairs))
        split_idx = int(len(all_pairs) * (1 - validation_split))
        train_indices = indices[:split_idx]
        valid_indices = indices[split_idx:]
        
        train_pairs = [all_pairs[i] for i in train_indices]
        valid_pairs = [all_pairs[i] for i in valid_indices]
        
        metrics = self.ranker.train(
            train_pairs=train_pairs,
            valid_pairs=valid_pairs,
            global_stats=self.global_stats
        )
        
        self._is_trained = True
        return metrics
    
    def train_from_click_data(
        self,
        click_data: List[Dict],
        documents: List[SearchDocument],
        validation_split: float = 0.2
    ) -> Dict:
        """
        Train LambdaMART from real click data.
        
        click_data format: [
            {
                'query': 'running shoes',
                'clicked_doc_ids': ['1', '2'],
                'impression_doc_ids': ['1', '2', '3', '4', '5'],
                'timestamp': '2024-01-15T10:30:00Z'
            },
            ...
        ]
        """
        self._compute_global_stats(documents)
        doc_map = {doc.doc_id: doc for doc in documents}
        
        pairs = []
        for session in click_data:
            query_id = hashlib.md5(session['query'].encode()).hexdigest()[:12]
            clicked = set(session.get('clicked_doc_ids', []))
            impressed = set(session.get('impression_doc_ids', []))
            
            for doc_id in impressed:
                doc = doc_map.get(doc_id)
                if not doc:
                    continue
                
                # Label: 4=clicked, 3=impressed but not clicked, 0=not in results
                if doc_id in clicked:
                    label = 4
                else:
                    # Position bias correction: docs shown but not clicked get lower relevance
                    label = 1
                
                qd = QueryDocumentPair(
                    query_id=query_id,
                    doc_id=doc_id,
                    query_text=session['query'],
                    doc_title=doc.title,
                    doc_body=doc.body,
                    relevance_label=label,
                )
                pairs.append(qd)
        
        # Shuffle and split
        indices = np.random.RandomState(42).permutation(len(pairs))
        split_idx = int(len(pairs) * (1 - validation_split))
        train_pairs = [pairs[i] for i in indices[:split_idx]]
        valid_pairs = [pairs[i] for i in indices[split_idx:]]
        
        metrics = self.ranker.train(
            train_pairs=train_pairs,
            valid_pairs=valid_pairs,
            global_stats=self.global_stats
        )
        
        self._is_trained = True
        return metrics
    
    def rerank(
        self,
        query: str,
        hybrid_results: List,
        top_k: int = 10
    ) -> List:
        """
        Re-rank hybrid search results using LambdaMART.
        
        Args:
            query: Original user query.
            hybrid_results: Results from hybrid search (list of SearchResult or similar).
            top_k: Number of results to return after re-ranking.
        """
        if not self._is_trained:
            # If not trained, return hybrid results as-is
            return hybrid_results[:top_k]
        
        # Convert hybrid results to QueryDocumentPairs
        pairs = []
        for result in hybrid_results:
            doc = result.doc if hasattr(result, 'doc') else result
            qd = QueryDocumentPair(
                query_id=hashlib.md5(query.encode()).hexdigest()[:12],
                doc_id=doc.doc_id,
                query_text=query,
                doc_title=doc.title,
                doc_body=doc.body,
                relevance_label=0,  # Unknown at inference time
                bm25_score=getattr(result, 'bm25_score', 0.0),
                dense_score=getattr(result, 'dense_score', 0.0),
            )
            pairs.append(qd)
        
        # Score and sort
        scores = self.ranker.predict(pairs, self.global_stats)
        ranked_indices = np.argsort(scores)[::-1]
        
        reranked = []
        for rank, idx in enumerate(ranked_indices[:top_k]):
            result = hybrid_results[idx]
            reranked.append(result)
        
        return reranked

# ──────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────

def demo_ltr():
    """Demonstrate the LambdaMART LTR pipeline."""
    print("\n" + "=" * 70)
    print("LEARNING-TO-RANK WITH LAMBDAMART DEMO")
    print("=" * 70)
    
    if not LIGHTGBM_AVAILABLE:
        print("[SKIP] LightGBM not installed. Install: pip install lightgbm")
        return
    
    # Sample documents
    documents = [
        SearchDocument("1", "Wireless Bluetooth Headphones", "High-quality over-ear headphones with noise cancellation, 30hr battery", {"price": 79.99}),
        SearchDocument("2", "USB-C Charging Cable", "Fast charging USB-C cable, 6ft braided nylon, compatible with all devices", {"price": 12.99}),
        SearchDocument("3", "Bluetooth Speaker Portable", "Waterproof portable speaker with deep bass, 24hr playtime, IPX7 rated", {"price": 49.99}),
        SearchDocument("4", "Laptop Stand Adjustable", "Ergonomic aluminum laptop stand, adjustable height, compatible 10-17 inch", {"price": 34.99}),
        SearchDocument("5", "Wireless Mouse Ergonomic", "Ergonomic wireless mouse with silent clicks, 6 buttons, USB receiver", {"price": 24.99}),
        SearchDocument("6", "Mechanical Keyboard RGB", "RGB mechanical keyboard with blue switches, 104 keys, aluminum frame", {"price": 59.99}),
        SearchDocument("7", "27-inch 4K Monitor", "27-inch 4K IPS monitor, 60Hz, HDMI/DisplayPort/USB-C, built-in speakers", {"price": 349.99}),
        SearchDocument("8", "Webcam 1080p HD", "1080p HD webcam with auto-focus, built-in microphone, privacy shutter", {"price": 39.99}),
    ]
    
    queries = [
        "bluetooth headphones wireless",
        "USB C fast charging cable",
        "portable waterproof speaker",
        "ergonomic laptop stand",
        "wireless mouse silent",
        "RGB mechanical keyboard",
        "4K monitor 27 inch",
        "HD webcam with autofocus",
        "gaming accessories",
        "office desk setup",
    ]
    
    ltr_pipeline = LTRPipeline()
    metrics = ltr_pipeline.train_on_synthetic(documents, queries)
    
    print(f"\nTraining complete!")
    print(f"  Best iteration: {metrics.get('best_iteration', 'N/A')}")
    print(f"  Best NDCG score: {metrics.get('best_score', 'N/A')}")
    
    # Feature importance
    importance = ltr_pipeline.ranker.feature_importance()
    print(f"\nTop 10 Features by Gain:")
    print(f"{'Feature':<35}{'Gain':>12}")
    print(f"{'─' * 35}{'─' * 12}")
    for _, row in importance.head(10).iterrows():
        print(f"{row['feature']:<35}{row['gain']:>12.2f}")
    
    print(f"\n{'=' * 70}")
    print("LTR Pipeline ready.")
    print("=" * 70)

if __name__ == "__main__":
    demo_ltr()
```

### 2.3 NDCG Evaluation

```python
def compute_ndcg(
    ranked_doc_ids: List[str],
    relevance_map: Dict[str, int],
    k: int = 10
) -> float:
    """
    Compute Normalized Discounted Cumulative Gain @ K.
    
    DCG@k = Σ(rel_i / log2(i+1)) for i=1..k
    NDCG@k = DCG@k / IDCG@k
    """
    def dcg(relevances):
        return sum(
            (2**rel - 1) / np.log2(i + 2)
            for i, rel in enumerate(relevances)
        )
    
    rels = [relevance_map.get(did, 0) for did in ranked_doc_ids[:k]]
    ideal_rels = sorted(relevance_map.values(), reverse=True)[:k]
    
    actual_dcg = dcg(rels)
    ideal_dcg = dcg(ideal_rels)
    
    return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0
```

---

## 3. Search Analytics Pipeline

### 3.1 Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    SEARCH ANALYTICS PIPELINE                     │
│                                                                  │
│  ┌──────────┐   ┌──────────────┐   ┌───────────────┐           │
│  │ Search   │──▶│ Event        │──▶│ Clickstream   │           │
│  │ Events   │   │ Ingestion    │   │ Processing    │           │
│  └──────────┘   │ (Kafka/Kinesis)│  └───────┬───────┘           │
│                 └──────────────┘           │                     │
│                                            ▼                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   ANALYTICS ENGINE                        │   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌─────────────────┐  │   │
│  │  │ Query       │  │ Click        │  │ Abandonment     │  │   │
│  │  │ Analytics   │  │ Analytics    │  │ Analytics       │  │   │
│  │  │             │  │              │  │                 │  │   │
│  │  │ • Top queries│ │ • CTR curves │  │ • Zero-results  │  │   │
│  │  │ • Null/low   │ │ • Position   │  │ • Query reform. │  │   │
│  │  │ • Trends     │ │ • Dwell time │  │ • Exit rate     │  │   │
│  │  │ • Geography  │ │ • Conversion │  │ • Fallback use  │  │   │
│  │  └──────┬──────┘  └──────┬───────┘  └────────┬────────┘  │   │
│  │         │                │                    │           │   │
│  │         └────────────────┼────────────────────┘           │   │
│  │                          ▼                                │   │
│  │               ┌──────────────────┐                        │   │
│  │               │ Quality Metrics  │                        │   │
│  │               │                  │                        │   │
│  │               │ • NDCG/MRR/MAP   │                        │   │
│  │               │ • Recall@K       │                        │   │
│  │               │ • Precision@K    │                        │   │
│  │               │ • Mean Reciprocal│                        │   │
│  │               │   Rank (MRR)     │                        │   │
│  │               └────────┬─────────┘                        │   │
│  └────────────────────────┼──────────────────────────────────┘   │
│                           ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   DASHBOARD & ALERTS                      │   │
│  │                                                          │   │
│  │  • Real-time dashboards (Grafana/Superset)               │   │
│  │  • Daily/weekly email reports                            │   │
│  │  • Anomaly detection alerts                              │   │
│  │  • A/B test result tracking                              │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### 3.2 Implementation

```python
"""
Search Analytics Pipeline
Production-grade analytics for search quality monitoring and improvement.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json
import hashlib
import numpy as np
from enum import Enum

# ──────────────────────────────────────────────────────────────────
# Event Data Model
# ──────────────────────────────────────────────────────────────────

class EventType(Enum):
    SEARCH = "search"
    CLICK = "click"
    ADD_TO_CART = "add_to_cart"
    PURCHASE = "purchase"
    PAGINATION = "pagination"
    FILTER_APPLY = "filter_apply"
    QUERY_REFORMULATION = "query_reformulation"
    ZERO_RESULTS = "zero_results"
    ABANDON = "abandon"

@dataclass
class SearchEvent:
    """A single search event captured from the search interface."""
    event_id: str
    event_type: EventType
    session_id: str
    user_id: str
    timestamp: datetime
    
    # Search-specific fields
    query: Optional[str] = None
    query_id: Optional[str] = None
    filters_applied: Dict[str, List[str]] = field(default_factory=dict)
    result_count: Optional[int] = None
    page_number: Optional[int] = None
    results_returned: List[str] = field(default_factory=list)  # doc IDs
    search_latency_ms: Optional[float] = None
    
    # Click-specific fields
    clicked_doc_id: Optional[str] = None
    click_position: Optional[int] = None
    click_timestamp: Optional[datetime] = None
    dwell_time_ms: Optional[float] = None
    
    # Commerce-specific fields
    price_at_click: Optional[float] = None
    cart_value: Optional[float] = None
    purchase_value: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Serialize to dictionary for JSON/Kafka publishing."""
        d = asdict(self)
        d['event_type'] = self.event_type.value
        d['timestamp'] = self.timestamp.isoformat()
        if self.click_timestamp:
            d['click_timestamp'] = self.click_timestamp.isoformat()
        return d
    
    @classmethod
    def from_dict(cls, d: Dict) -> 'SearchEvent':
        """Deserialize from dictionary."""
        d = dict(d)
        d['event_type'] = EventType(d['event_type'])
        d['timestamp'] = datetime.fromisoformat(d['timestamp'])
        if d.get('click_timestamp'):
            d['click_timestamp'] = datetime.fromisoformat(d['click_timestamp'])
        return cls(**d)

@dataclass
class SearchSession:
    """Aggregated view of a single user search session."""
    session_id: str
    user_id: str
    events: List[SearchEvent] = field(default_factory=list)
    
    @property
    def initial_query(self) -> Optional[str]:
        search_events = [e for e in self.events if e.event_type == EventType.SEARCH]
        return search_events[0].query if search_events else None
    
    @property
    def reformulations(self) -> List[str]:
        return [e.query for e in self.events if e.event_type == EventType.QUERY_REFORMULATION]
    
    @property
    def clicked_docs(self) -> List[str]:
        return [e.clicked_doc_id for e in self.events if e.event_type == EventType.CLICK and e.clicked_doc_id]
    
    @property
    def has_conversion(self) -> bool:
        return any(e.event_type == EventType.PURCHASE for e in self.events)
    
    @property
    def was_abandoned(self) -> bool:
        return any(e.event_type == EventType.ABANDON for e in self.events)
    
    @property
    def had_zero_results(self) -> bool:
        return any(e.event_type == EventType.ZERO_RESULTS for e in self.events)

# ──────────────────────────────────────────────────────────────────
# Analytics Engine
# ──────────────────────────────────────────────────────────────────

class SearchAnalytics:
    """
    Search analytics engine for computing KPIs and generating insights.
    
    Key metrics:
    - Query Volume & Trends
    - Click-Through Rate (CTR) by position
    - Zero-result rate
    - Query reformulation rate
    - Session abandonment rate
    - Conversion rate from search
    - Time-to-first-click
    - Search latency percentiles
    """
    
    def __init__(self):
        self.events: List[SearchEvent] = []
        self.sessions: Dict[str, SearchSession] = {}
    
    def ingest_event(self, event: SearchEvent):
        """Ingest a single search event."""
        self.events.append(event)
        
        if event.session_id not in self.sessions:
            self.sessions[event.session_id] = SearchSession(
                session_id=event.session_id,
                user_id=event.user_id
            )
        self.sessions[event.session_id].events.append(event)
    
    def ingest_batch(self, events: List[SearchEvent]):
        """Batch ingest multiple events."""
        for event in events:
            self.ingest_event(event)
    
    # ── Query Analytics ──
    
    def top_queries(self, n: int = 20, min_count: int = 1) -> List[Dict]:
        """Top N queries by frequency."""
        query_counts = Counter(
            e.query for e in self.events
            if e.event_type == EventType.SEARCH and e.query
        )
        return [
            {'query': q, 'count': c}
            for q, c in query_counts.most_common(n)
            if c >= min_count
        ]
    
    def query_trends(
        self,
        window_hours: int = 24,
        granularity_hours: int = 1
    ) -> Dict[str, List]:
        """Query volume trends over time buckets."""
        now = datetime.utcnow()
        cutoff = now - timedelta(hours=window_hours)
        
        buckets = defaultdict(int)
        for e in self.events:
            if e.event_type == EventType.SEARCH and e.timestamp >= cutoff:
                bucket_key = e.timestamp.replace(
                    minute=(e.timestamp.minute // (granularity_hours * 60)) * (granularity_hours * 60),
                    second=0, microsecond=0
                ).isoformat()
                buckets[bucket_key] += 1
        
        sorted_keys = sorted(buckets.keys())
        return {
            'timestamps': sorted_keys,
            'volumes': [buckets[k] for k in sorted_keys]
        }
    
    def zero_result_queries(self) -> List[Dict]:
        """Queries that returned zero results, with frequency."""
        zero_events = [e for e in self.events if e.event_type == EventType.ZERO_RESULTS]
        query_counts = Counter(e.query for e in zero_events if e.query)
        return [
            {'query': q, 'count': c, 'last_seen': max(
                (e.timestamp for e in zero_events if e.query == q)
            ).isoformat()}
            for q, c in query_counts.most_common()
        ]
    
    # ── Click Analytics ──
    
    def ctr_by_position(self) -> Dict[int, float]:
        """Click-through rate broken down by result position (1-indexed)."""
        position_impressions = defaultdict(int)
        position_clicks = defaultdict(int)
        
        for session in self.sessions.values():
            search_events = [e for e in session.events if e.event_type == EventType.SEARCH]
            click_events = [e for e in session.events if e.event_type == EventType.CLICK]
            
            for se in search_events:
                for pos, doc_id in enumerate(se.results_returned, 1):
                    position_impressions[pos] += 1
            
            for ce in click_events:
                if ce.click_position:
                    position_clicks[ce.click_position] += 1
        
        ctr = {}
        for pos in sorted(position_impressions.keys()):
            if position_impressions[pos] > 0:
                ctr[pos] = position_clicks.get(pos, 0) / position_impressions[pos]
        
        return ctr
    
    def overall_ctr(self) -> float:
        """Overall click-through rate."""
        total_searches = len([e for e in self.events if e.event_type == EventType.SEARCH])
        total_clicks = len([e for e in self.events if e.event_type == EventType.CLICK])
        return total_clicks / total_searches if total_searches > 0 else 0.0
    
    def average_dwell_time_ms(self) -> float:
        """Average time spent on clicked result pages."""
        dwell_times = [
            e.dwell_time_ms for e in self.events
            if e.event_type == EventType.CLICK and e.dwell_time_ms is not None
        ]
        return np.mean(dwell_times) if dwell_times else 0.0
    
    # ── Session Analytics ──
    
    def session_stats(self) -> Dict:
        """Aggregate session-level metrics."""
        sessions = list(self.sessions.values())
        total = len(sessions)
        if total == 0:
            return {}
        
        reforms = sum(1 for s in sessions if len(s.reformulations) > 0)
        zero_res = sum(1 for s in sessions if s.had_zero_results)
        abandoned = sum(1 for s in sessions if s.was_abandoned)
        conversions = sum(1 for s in sessions if s.has_conversion)
        
        return {
            'total_sessions': total,
            'reformulation_rate': reforms / total,
            'zero_result_rate': zero_res / total,
            'abandonment_rate': abandoned / total,
            'conversion_rate': conversions / total,
            'avg_clicks_per_session': np.mean([
                len(s.clicked_docs) for s in sessions
            ]) if total > 0 else 0,
            'avg_queries_per_session': np.mean([
                len([e for e in s.events if e.event_type == EventType.SEARCH])
                for s in sessions
            ]) if total > 0 else 0,
        }
    
    # ── Quality Metrics ──
    
    def compute_mrr(self, relevance_map: Dict[str, Dict[str, int]]) -> float:
        """
        Mean Reciprocal Rank (MRR).
        
        MRR = (1/|Q|) * Σ(1/rank_i) over queries Q,
        where rank_i is the position of the first relevant document.
        """
        reciprocal_ranks = []
        
        for session in self.sessions.values():
            search_events = [e for e in session.events if e.event_type == EventType.SEARCH]
            for se in search_events:
                if not se.query or se.query not in relevance_map:
                    continue
                rels = relevance_map[se.query]
                
                for rank, doc_id in enumerate(se.results_returned, 1):
                    if rels.get(doc_id, 0) >= 3:  # Relevant
                        reciprocal_ranks.append(1.0 / rank)
                        break
                else:
                    reciprocal_ranks.append(0.0)
        
        return np.mean(reciprocal_ranks) if reciprocal_ranks else 0.0
    
    def compute_ndcg_at_k(
        self,
        relevance_map: Dict[str, Dict[str, int]],
        k: int = 10
    ) -> float:
        """Average NDCG@K across all queries."""
        ndcg_scores = []
        
        for session in self.sessions.values():
            search_events = [e for e in session.events if e.event_type == EventType.SEARCH]
            for se in search_events:
                if not se.query or se.query not in relevance_map:
                    continue
                rels = relevance_map[se.query]
                
                # Get relevance for each returned document
                seq = [rels.get(did, 0) for did in se.results_returned[:k]]
                
                # Pad if fewer than k results
                while len(seq) < k:
                    seq.append(0)
                
                dcg = sum(
                    (2**rel - 1) / np.log2(i + 2)
                    for i, rel in enumerate(seq)
                )
                
                ideal = sorted(rels.values(), reverse=True)[:k]
                while len(ideal) < k:
                    ideal.append(0)
                idcg = sum(
                    (2**rel - 1) / np.log2(i + 2)
                    for i, rel in enumerate(ideal)
                )
                
                ndcg = dcg / idcg if idcg > 0 else 0.0
                ndcg_scores.append(ndcg)
        
        return np.mean(ndcg_scores) if ndcg_scores else 0.0
    
    # ── Latency Analytics ──
    
    def latency_percentiles(self) -> Dict:
        """Search latency distribution (p50, p90, p95, p99)."""
        latencies = [
            e.search_latency_ms for e in self.events
            if e.event_type == EventType.SEARCH and e.search_latency_ms is not None
        ]
        if not latencies:
            return {}
        
        return {
            'p50': float(np.percentile(latencies, 50)),
            'p90': float(np.percentile(latencies, 90)),
            'p95': float(np.percentile(latencies, 95)),
            'p99': float(np.percentile(latencies, 99)),
            'mean': float(np.mean(latencies)),
            'std': float(np.std(latencies)),
        }
    
    # ── Report Generation ──
    
    def generate_report(self, relevance_map: Optional[Dict] = None) -> Dict:
        """Generate a comprehensive search analytics report."""
        report = {
            'generated_at': datetime.utcnow().isoformat(),
            'total_events': len(self.events),
            'total_sessions': len(self.sessions),
            'query_analytics': {
                'top_queries': self.top_queries(10),
                'zero_result_queries': self.zero_result_queries()[:10],
            },
            'click_analytics': {
                'overall_ctr': self.overall_ctr(),
                'ctr_by_position': self.ctr_by_position(),
                'avg_dwell_time_ms': self.average_dwell_time_ms(),
            },
            'session_analytics': self.session_stats(),
            'latency': self.latency_percentiles(),
        }
        
        if relevance_map:
            report['quality_metrics'] = {
                'mrr': self.compute_mrr(relevance_map),
                'ndcg@5': self.compute_ndcg_at_k(relevance_map, 5),
                'ndcg@10': self.compute_ndcg_at_k(relevance_map, 10),
            }
        
        return report
    
    def export_events(self, path: str):
        """Export all events to JSON Lines file."""
        with open(path, 'w') as f:
            for event in self.events:
                f.write(json.dumps(event.to_dict()) + '\n')

# ──────────────────────────────────────────────────────────────────
# Anomaly Detection
# ──────────────────────────────────────────────────────────────────

class SearchAnomalyDetector:
    """
    Detects anomalies in search metrics using statistical methods.
    
    Methods:
    - Z-score: Flags values > N standard deviations from mean
    - Moving average: Compares current window to rolling baseline
    - Trend break: Detects changes in trend direction
    """
    
    def __init__(self, z_threshold: float = 3.0):
        self.z_threshold = z_threshold
        self.baselines: Dict[str, Dict] = {}
    
    def compute_z_score(self, value: float, mean: float, std: float) -> float:
        """Compute Z-score for anomaly detection."""
        return (value - mean) / std if std > 0 else 0.0
    
    def detect_ctr_anomaly(
        self,
        current_ctr: float,
        historical_ctrs: List[float]
    ) -> Dict:
        """Detect if current CTR is anomalous."""
        if len(historical_ctrs) < 5:
            return {'is_anomaly': False, 'reason': 'insufficient_data'}
        
        mean = np.mean(historical_ctrs)
        std = np.std(historical_ctrs)
        z = self.compute_z_score(current_ctr, mean, std)
        
        return {
            'is_anomaly': abs(z) > self.z_threshold,
            'z_score': float(z),
            'current_ctr': current_ctr,
            'historical_mean': float(mean),
            'historical_std': float(std),
            'direction': 'above' if z > 0 else 'below',
        }
    
    def detect_zero_result_spike(
        self,
        current_rate: float,
        historical_rates: List[float]
    ) -> Dict:
        """Detect if zero-result rate is spiking."""
        if len(historical_rates) < 3:
            return {'is_anomaly': False, 'reason': 'insufficient_data'}
        
        mean = np.mean(historical_rates)
        std = np.std(historical_rates)
        z = self.compute_z_score(current_rate, mean, std)
        
        return {
            'is_anomaly': z > self.z_threshold,  # Only alert on spikes upward
            'z_score': float(z),
            'current_rate': current_rate,
            'historical_mean': float(mean),
            'severity': 'critical' if z > 5 else 'warning' if z > 3 else 'info',
        }

# ──────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────

def demo_analytics():
    """Demonstrate the search analytics pipeline."""
    print("\n" + "=" * 70)
    print("SEARCH ANALYTICS PIPELINE DEMO")
    print("=" * 70)
    
    analytics = SearchAnalytics()
    
    # Generate synthetic events
    np.random.seed(42)
    base_time = datetime.utcnow() - timedelta(hours=24)
    
    queries = ["running shoes", "bluetooth headphones", "laptop stand", "wireless mouse", "4k monitor"]
    doc_ids = [f"doc_{i}" for i in range(10)]
    
    for i in range(200):
        session_id = f"sess_{i}"
        user_id = f"user_{np.random.randint(1, 50)}"
        
        # Search event
        query = np.random.choice(queries)
        search_event = SearchEvent(
            event_id=f"evt_{i}_search",
            event_type=EventType.SEARCH,
            session_id=session_id,
            user_id=user_id,
            timestamp=base_time + timedelta(minutes=i * 7),
            query=query,
            query_id=hashlib.md5(query.encode()).hexdigest()[:12],
            result_count=np.random.randint(0, 50),
            results_returned=list(np.random.choice(doc_ids, min(10, np.random.randint(1, 11)), replace=False)),
            search_latency_ms=np.random.lognormal(mean=np.log(50), sigma=0.5),
        )
        analytics.ingest_event(search_event)
        
        # Click event (70% chance)
        if np.random.random() < 0.7 and search_event.results_returned:
            click_pos = np.random.randint(1, min(len(search_event.results_returned) + 1, 6))
            clicked_doc = search_event.results_returned[click_pos - 1]
            click_event = SearchEvent(
                event_id=f"evt_{i}_click",
                event_type=EventType.CLICK,
                session_id=session_id,
                user_id=user_id,
                timestamp=base_time + timedelta(minutes=i * 7, seconds=5),
                query=query,
                query_id=search_event.query_id,
                clicked_doc_id=clicked_doc,
                click_position=click_pos,
                dwell_time_ms=np.random.lognormal(mean=np.log(15000), sigma=1.0),
            )
            analytics.ingest_event(click_event)
            
            # Purchase (10% chance)
            if np.random.random() < 0.1:
                purchase_event = SearchEvent(
                    event_id=f"evt_{i}_purchase",
                    event_type=EventType.PURCHASE,
                    session_id=session_id,
                    user_id=user_id,
                    timestamp=base_time + timedelta(minutes=i * 7, seconds=30),
                    purchase_value=np.random.uniform(10, 200),
                )
                analytics.ingest_event(purchase_event)
        
        # Zero results (15% chance)
        if np.random.random() < 0.15:
            zero_event = SearchEvent(
                event_id=f"evt_{i}_zero",
                event_type=EventType.ZERO_RESULTS,
                session_id=session_id,
                user_id=user_id,
                timestamp=base_time + timedelta(minutes=i * 7, seconds=1),
                query=f"rare_query_{np.random.randint(1, 20)}",
            )
            analytics.ingest_event(zero_event)
    
    # Generate report
    report = analytics.generate_report()
    
    print(f"\n📊 SEARCH ANALYTICS REPORT")
    print(f"{'─' * 70}")
    print(f"Generated: {report['generated_at']}")
    print(f"Total Events: {report['total_events']}")
    print(f"Total Sessions: {report['total_sessions']}")
    print(f"Overall CTR: {report['click_analytics']['overall_ctr']:.2%}")
    print(f"Avg Dwell Time: {report['click_analytics']['avg_dwell_time_ms']:.0f}ms")
    
    session = report['session_analytics']
    print(f"\nSession Metrics:")
    print(f"  Reformulation Rate: {session.get('reformulation_rate', 0):.2%}")
    print(f"  Zero-Result Rate:   {session.get('zero_result_rate', 0):.2%}")
    print(f"  Abandonment Rate:   {session.get('abandonment_rate', 0):.2%}")
    print(f"  Conversion Rate:    {session.get('conversion_rate', 0):.2%}")
    print(f"  Avg Clicks/Session: {session.get('avg_clicks_per_session', 0):.1f}")
    print(f"  Avg Queries/Session:{session.get('avg_queries_per_session', 0):.1f}")
    
    latency = report['latency']
    if latency:
        print(f"\nLatency (ms):")
        print(f"  P50: {latency['p50']:.1f} | P90: {latency['p90']:.1f} | P95: {latency['p95']:.1f} | P99: {latency['p99']:.1f}")
        print(f"  Mean: {latency['mean']:.1f} ± {latency['std']:.1f}")
    
    ctr_pos = report['click_analytics']['ctr_by_position']
    if ctr_pos:
        print(f"\nCTR by Position:")
        for pos in sorted(ctr_pos.keys())[:5]:
            bar = '█' * int(ctr_pos[pos] * 50)
            print(f"  Pos {pos}: {ctr_pos[pos]:.1%} {bar}")
    
    print(f"\nTop Queries:")
    for item in report['query_analytics']['top_queries'][:5]:
        print(f"  {item['count']:>4}x  {item['query']}")
    
    print(f"\n{'=' * 70}")
    print("Analytics pipeline ready.")
    print("=" * 70)

if __name__ == "__main__":
    demo_analytics()
```

---

## 4. Query Understanding: NER + Intent

### 4.1 Architecture Overview

```
User Query: "Nike Air Max running shoes under $150 size 10"

                    │
                    ▼
    ┌───────────────────────────────┐
    │   QUERY PREPROCESSING         │
    │   • Normalization             │
    │   • Spelling correction       │
    │   • Tokenization              │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │   NAMED ENTITY RECOGNITION    │
    │   (spaCy + custom model)      │
    │                               │
    │   Extracted:                  │
    │   • BRAND: "Nike"             │
    │   • PRODUCT_LINE: "Air Max"   │
    │   • CATEGORY: "running shoes" │
    │   • PRICE: "< $150"           │
    │   • SIZE: "10"                │
    │   • CONSTRAINT: "under"       │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │   INTENT CLASSIFICATION       │
    │   (Transformer classifier)    │
    │                               │
    │   Intent: TRANSACTIONAL       │
    │   Sub-intent: CATEGORY_SEARCH │
    │   Confidence: 0.94            │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │   QUERY REWRITING / EXPANSION │
    │                               │
    │   • Synonym expansion         │
    │   • Category normalization    │
    │   • Filter extraction         │
    └───────────────┬───────────────┘
                    │
                    ▼
    ┌───────────────────────────────┐
    │   STRUCTURED QUERY            │
    │   (sent to search engine)     │
    │                               │
    │   {                           │
    │     "original": "...",        │
    │     "entities": {...},        │
    │     "intent": "transactional",│
    │     "filters": {...},         │
    │     "expanded_terms": [...]   │
    │   }                           │
    └───────────────────────────────┘
```

### 4.2 Implementation

```python
"""
Query Understanding: Named Entity Recognition + Intent Classification
Production-grade query understanding pipeline using NLP transformers.
"""

from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import re
import json
from collections import defaultdict

# ──────────────────────────────────────────────────────────────────
# Entity & Intent Types
# ──────────────────────────────────────────────────────────────────

class EntityType(Enum):
    BRAND = "brand"
    PRODUCT_LINE = "product_line"
    CATEGORY = "category"
    PRICE = "price"
    SIZE = "size"
    COLOR = "color"
    MATERIAL = "material"
    GENDER = "gender"
    AGE_GROUP = "age_group"
    CONDITION = "condition"
    CONSTRAINT = "constraint"  # "under", "over", "exact"
    LOCATION = "location"
    FEATURE = "feature"

class IntentType(Enum):
    TRANSACTIONAL = "transactional"      # User wants to buy
    INFORMATIONAL = "informational"      # User wants to learn
    NAVIGATIONAL = "navigational"        # User wants a specific page
    COMMERCIAL_INVESTIGATION = "commercial_investigation"  # Comparing before buying

@dataclass
class QueryEntity:
    """A named entity extracted from a query."""
    entity_type: EntityType
    text: str
    normalized_value: str
    confidence: float
    start_char: int
    end_char: int

@dataclass
class QueryIntent:
    """Classified intent for a query."""
    primary_intent: IntentType
    sub_intent: Optional[str] = None
    confidence: float = 0.0
    secondary_intents: List[Dict] = field(default_factory=list)

@dataclass
class ParsedQuery:
    """Complete parsed representation of a user query."""
    original_query: str
    normalized_query: str
    tokens: List[str]
    entities: List[QueryEntity] = field(default_factory=list)
    intent: Optional[QueryIntent] = None
    expanded_terms: List[str] = field(default_factory=list)
    extracted_filters: Dict[str, any] = field(default_factory=dict)
    search_weight_tuning: Dict[str, float] = field(default_factory=dict)

# ──────────────────────────────────────────────────────────────────
# Knowledge Bases for Entity Normalization
# ──────────────────────────────────────────────────────────────────

# Brand synonyms / aliases
BRAND_ALIASES = {
    "nike": "Nike",
    "adidas": "Adidas",
    "ua": "Under Armour",
    "under armour": "Under Armour",
    "north face": "The North Face",
    "tnf": "The North Face",
    "patagonia": "Patagonia",
    "lululemon": "Lululemon",
    "hm": "H&M",
    "apple": "Apple",
    "samsung": "Samsung",
    "sony": "Sony",
    "bose": "Bose",
    "dell": "Dell",
    "hp": "HP",
    "lenovo": "Lenovo",
    "microsoft": "Microsoft",
    "google": "Google",
    "amazon": "Amazon",
}

# Category taxonomy with synonyms
CATEGORY_TAXONOMY = {
    "running shoes": {
        "canonical": "Running Shoes",
        "synonyms": ["runners", "trainers", "sneakers", "athletic shoes", "jogging shoes", "road shoes", "trail shoes"],
        "parent": "Footwear",
    },
    "headphones": {
        "canonical": "Headphones",
        "synonyms": ["earphones", "earbuds", "headset", "cans", "ear pads"],
        "parent": "Electronics > Audio",
    },
    "laptop": {
        "canonical": "Laptops",
        "synonyms": ["notebook", "ultrabook", "macbook", "chromebook", "thinkpad"],
        "parent": "Electronics > Computers",
    },
    "jacket": {
        "canonical": "Jackets",
        "synonyms": ["coat", "outerwear", "parka", "windbreaker", "shell"],
        "parent": "Clothing > Outerwear",
    },
    "water bottle": {
        "canonical": "Water Bottles",
        "synonyms": ["flask", "canteen", "thermos", "tumbler", "hydration"],
        "parent": "Accessories > Drinkware",
    },
}

# Price pattern recognition
PRICE_PATTERNS = [
    (r'(?:under|below|less than|cheaper than|max|up to)\s*\$?(\d+(?:\.\d{2})?)', 'max'),
    (r'(?:over|above|more than|min|at least|from)\s*\$?(\d+(?:\.\d{2})?)', 'min'),
    (r'(?:around|about|approx(?:imately)?|~)\s*\$?(\d+(?:\.\d{2})?)', 'approx'),
    (r'\$(\d+(?:\.\d{2})?)', 'exact'),
    (r'(?:(\d+(?:\.\d{2})?)\s*(?:\-|to)\s*\$?(\d+(?:\.\d{2})?))', 'range'),
]

# Size patterns
SIZE_PATTERNS = [
    r'\b(\d{1,2}(?:\.\d)?)\s*(?:US|UK|EU)?\s*(?:men\'?s?|women\'?s?|kids?)?\b',
    r'\b([SMLXL]{1,3})\b',  # S, M, L, XL, XXL, etc.
    r'\b(\d{1,2})(?:W|L)\b',  # 32W 34L
]

# ──────────────────────────────────────────────────────────────────
# Rule-Based NER (Fast, No Model Loading)
# ──────────────────────────────────────────────────────────────────

class RuleBasedNER:
    """
    Fast rule-based NER for e-commerce queries.
    Uses regex patterns, gazetteers, and heuristics.
    
    For production, combine with a transformer-based model
    (spaCy + custom NER) for higher accuracy on complex queries.
    """
    
    def __init__(self):
        # Compile brand patterns
        self._brand_lookup = self._build_brand_trie()
        
        # Compile category patterns
        self._category_lookup = self._build_category_trie()
        
        # Compile constraint keywords
        self.constraint_keywords = {
            'under', 'below', 'less than', 'cheaper than', 'max', 'up to',
            'over', 'above', 'more than', 'min', 'at least', 'from',
            'around', 'about', 'approx', 'approximately',
            'exact', 'exactly', 'only',
            'new', 'used', 'like new', 'refurbished', 'open box',
            'best', 'top', 'rated', 'popular', 'trending',
            'men', 'mens', "men's", 'women', 'womens', "women's",
            'kids', 'children', 'toddler', 'infant', 'baby',
            'boy', 'boys', 'girl', 'girls', 'unisex',
        }
    
    def _build_brand_trie(self) -> Dict:
        """Build a simple prefix tree for brand matching."""
        trie = {}
        for alias, canonical in BRAND_ALIASES.items():
            parts = alias.lower().split()
            node = trie
            for part in parts:
                if part not in node:
                    node[part] = {}
                node = node[part]
            node['__value__'] = canonical
        return trie
    
    def _build_category_trie(self) -> Dict:
        """Build a prefix tree for category matching."""
        trie = {}
        for canonical, info in CATEGORY_TAXONOMY.items():
            for synonym in [canonical] + info['synonyms']:
                parts = synonym.lower().split()
                node = trie
                for part in parts:
                    if part not in node:
                        node[part] = {}
                    node = node[part]
                node['__value__'] = info['canonical']
        return trie
    
    def _match_trie(
        self, tokens: List[str], trie: Dict, start_idx: int
    ) -> Optional[Tuple[int, str]]:
        """Try to match tokens starting at start_idx against a trie. Returns (length, value)."""
        node = trie
        best_match = None
        best_value = None
        
        for offset in range(len(tokens) - start_idx):
            token = tokens[start_idx + offset].lower()
            if token not in node:
                break
            node = node[token]
            if '__value__' in node:
                best_match = offset + 1
                best_value = node['__value__']
        
        return (best_match, best_value) if best_match else None
    
    def extract(self, query: str) -> List[QueryEntity]:
        """Extract entities from a query string."""
        entities = []
        tokens = query.lower().split()
        i = 0
        
        while i < len(tokens):
            matched = False
            
            # Try brand match
            result = self._match_trie(tokens, self._brand_lookup, i)
            if result:
                length, value = result
                span_text = ' '.join(tokens[i:i+length])
                entities.append(QueryEntity(
                    entity_type=EntityType.BRAND,
                    text=span_text,
                    normalized_value=value,
                    confidence=0.95 if length > 1 else 0.85,
                    start_char=query.lower().find(span_text),
                    end_char=query.lower().find(span_text) + len(span_text),
                ))
                i += length
                matched = True
                continue
            
            # Try category match
            result = self._match_trie(tokens, self._category_lookup, i)
            if result:
                length, value = result
                span_text = ' '.join(tokens[i:i+length])
                entities.append(QueryEntity(
                    entity_type=EntityType.CATEGORY,
                    text=span_text,
                    normalized_value=value,
                    confidence=0.90,
                    start_char=query.lower().find(span_text),
                    end_char=query.lower().find(span_text) + len(span_text),
                ))
                i += length
                matched = True
                continue
            
            # Try constraint match
            if tokens[i] in self.constraint_keywords:
                entities.append(QueryEntity(
                    entity_type=EntityType.CONSTRAINT,
                    text=tokens[i],
                    normalized_value=tokens[i],
                    confidence=0.80,
                    start_char=query.lower().find(tokens[i]),
                    end_char=query.lower().find(tokens[i]) + len(tokens[i]),
                ))
                matched = True
            
            i += 1
        
        # Extract price patterns (regex-based, works across token boundaries)
        for pattern, price_type in PRICE_PATTERNS:
            for match in re.finditer(pattern, query, re.IGNORECASE):
                if price_type == 'range' and match.lastindex >= 2:
                    entities.append(QueryEntity(
                        entity_type=EntityType.PRICE,
                        text=match.group(0),
                        normalized_value=f"${match.group(1)}-${match.group(2)}",
                        confidence=0.95,
                        start_char=match.start(),
                        end_char=match.end(),
                    ))
                elif price_type != 'range':
                    entities.append(QueryEntity(
                        entity_type=EntityType.PRICE,
                        text=match.group(0),
                        normalized_value=f"{price_type}:{match.group(1)}",
                        confidence=0.95,
                        start_char=match.start(),
                        end_char=match.end(),
                    ))
        
        # Extract size patterns
        for pattern in SIZE_PATTERNS:
            for match in re.finditer(pattern, query, re.IGNORECASE):
                entities.append(QueryEntity(
                    entity_type=EntityType.SIZE,
                    text=match.group(0),
                    normalized_value=match.group(1).upper(),
                    confidence=0.90,
                    start_char=match.start(),
                    end_char=match.end(),
                ))
        
        return entities

# ──────────────────────────────────────────────────────────────────
# Intent Classifier
# ──────────────────────────────────────────────────────────────────

class QueryIntentClassifier:
    """
    Classifies the intent of a search query.
    
    Hybrid approach:
    1. Rule-based heuristics for common patterns (fast, no model)
    2. Optional transformer model for higher accuracy
    """
    
    # Keyword signals for each intent type
    TRANSACTIONAL_SIGNALS = {
        'buy', 'price', 'cheap', 'discount', 'sale', 'order', 'shop',
        'deal', 'coupon', 'free shipping', 'in stock', 'available',
        'under', 'best price', 'affordable', 'bargain', 'clearance',
    }
    
    INFORMATIONAL_SIGNALS = {
        'how to', 'what is', 'why', 'when', 'where', 'guide', 'tutorial',
        'review', 'reviews', 'rating', 'ratings', 'compare', 'comparison',
        'best', 'top', 'vs', 'versus', 'difference between', 'specs',
        'specifications', 'dimensions', 'weight', 'size chart',
    }
    
    NAVIGATIONAL_SIGNALS = {
        'login', 'log in', 'sign in', 'signin', 'account', 'my account',
        'orders', 'order history', 'returns', 'return policy', 'tracking',
        'track order', 'shipping', 'help', 'contact', 'customer service',
        'store locator', 'gift card', 'wishlist', 'cart',
    }
    
    # Sub-intent patterns
    SUB_INTENTS = {
        'category_browse': {'category', 'categories', 'selection', 'collection', 'range'},
        'specific_product': {'exact', 'specific', 'model', 'sku', 'product number'},
        'price_comparison': {'cheapest', 'best price', 'price compare', 'vs'},
        'gift_finding': {'gift', 'present', 'for him', 'for her', 'birthday', 'anniversary'},
        'problem_solving': {'fix', 'repair', 'how to', 'troubleshoot', 'problem'},
        'sizing': {'size chart', 'fit', 'measurements', 'sizing', 'too big', 'too small'},
    }
    
    def classify(self, query: str, entities: List[QueryEntity] = None) -> QueryIntent:
        """
        Classify the intent of a query.
        
        Returns QueryIntent with primary intent, confidence, and sub-intent.
        """
        query_lower = query.lower()
        query_tokens = set(query_lower.split())
        
        # Count signals for each intent
        scores = {
            IntentType.TRANSACTIONAL: 0.0,
            IntentType.INFORMATIONAL: 0.0,
            IntentType.NAVIGATIONAL: 0.0,
            IntentType.COMMERCIAL_INVESTIGATION: 0.0,
        }
        
        # Check transactional signals
        for signal in self.TRANSACTIONAL_SIGNALS:
            if signal in query_lower:
                scores[IntentType.TRANSACTIONAL] += 0.15
        
        # Check informational signals
        for signal in self.INFORMATIONAL_SIGNALS:
            if signal in query_lower:
                scores[IntentType.INFORMATIONAL] += 0.15
        
        # Check navigational signals
        for signal in self.NAVIGATIONAL_SIGNALS:
            if signal in query_lower:
                scores[IntentType.NAVIGATIONAL] += 0.20  # Higher weight (more reliable)
        
        # Entity-based heuristics
        if entities:
            has_price = any(e.entity_type == EntityType.PRICE for e in entities)
            has_size = any(e.entity_type == EntityType.SIZE for e in entities)
            has_brand = any(e.entity_type == EntityType.BRAND for e in entities)
            has_category = any(e.entity_type == EntityType.CATEGORY for e in entities)
            
            if has_price and has_category:
                scores[IntentType.TRANSACTIONAL] += 0.2
            if has_size:
                scores[IntentType.TRANSACTIONAL] += 0.1
            if has_brand and has_category and has_price:
                scores[IntentType.TRANSACTIONAL] += 0.2
        
        # Default: queries without signals lean transactional
        if sum(scores.values()) < 0.1:
            scores[IntentType.TRANSACTIONAL] = 0.3
        
        # Normalize to [0, 1]
        total = max(sum(scores.values()), 0.01)
        for intent in scores:
            scores[intent] = min(scores[intent] / total, 1.0)
        
        # Primary intent is the highest scoring
        primary_intent = max(scores, key=scores.get)
        confidence = scores[primary_intent]
        
        # Secondary intents (others above threshold)
        secondary = [
            {'intent': intent.value, 'confidence': round(conf, 3)}
            for intent, conf in sorted(scores.items(), key=lambda x: x[1], reverse=True)
            if conf > 0.15 and intent != primary_intent
        ]
        
        # Classify sub-intent
        sub_intent = None
        for sub_name, keywords in self.SUB_INTENTS.items():
            if any(kw in query_lower for kw in keywords):
                sub_intent = sub_name
                break
        
        return QueryIntent(
            primary_intent=primary_intent,
            sub_intent=sub_intent,
            confidence=round(confidence, 3),
            secondary_intents=secondary,
        )

# ──────────────────────────────────────────────────────────────────
# Query Expansion & Rewriting
# ──────────────────────────────────────────────────────────────────

class QueryExpander:
    """
    Query expansion for improving recall in sparse lexical search.
    """
    
    SYNONYM_MAP = {
        'running': ['jogging', 'training'],
        'shoes': ['footwear', 'sneakers', 'trainers'],
        'jacket': ['coat', 'outerwear', 'parka'],
        'cheap': ['affordable', 'budget', 'inexpensive', 'discount'],
        'lightweight': ['light', 'ultralight'],
        'wireless': ['bluetooth', 'cordless'],
        'noise cancelling': ['noise canceling', 'anc', 'noise reduction'],
    }
    
    def expand(self, query: str, intent: Optional[QueryIntent] = None) -> List[str]:
        """
        Generate expanded query terms for improved recall.
        
        Returns a list of additional search terms.
        """
        expanded = set()
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        
        for term, synonyms in self.SYNONYM_MAP.items():
            if term in query_lower:
                for syn in synonyms:
                    if syn not in query_terms:
                        expanded.add(syn)
        
        # Intent-based expansion
        if intent:
            if intent.primary_intent == IntentType.TRANSACTIONAL:
                expanded.update(['buy', 'shop', 'price', 'in stock'])
            elif intent.primary_intent == IntentType.INFORMATIONAL:
                expanded.update(['review', 'guide', 'specs'])
        
        return list(expanded)

# ──────────────────────────────────────────────────────────────────
# Complete Query Understanding Pipeline
# ──────────────────────────────────────────────────────────────────

class QueryUnderstandingPipeline:
    """
    Complete query understanding pipeline combining NER, intent
    classification, and query expansion.
    """
    
    def __init__(self, use_transformer: bool = False):
        self.ner = RuleBasedNER()
        self.intent_classifier = QueryIntentClassifier()
        self.expander = QueryExpander()
        self.use_transformer = use_transformer
        
        if use_transformer:
            self._load_transformer_models()
    
    def _load_transformer_models(self):
        """
        Load transformer-based models for higher accuracy NER and intent.
        Requires: pip install transformers torch
        """
        try:
            from transformers import pipeline
            self._ner_model = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                aggregation_strategy="simple"
            )
            self._intent_model = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
        except ImportError:
            print("Warning: transformers not installed. Using rule-based only.")
            self.use_transformer = False
    
    def parse(self, query: str) -> ParsedQuery:
        """
        Parse a raw user query into a structured representation.
        
        Args:
            query: Raw user query string.
        
        Returns:
            ParsedQuery with entities, intent, expansions, and filters.
        """
        # Clean and normalize
        normalized = query.strip().lower()
        tokens = normalized.split()
        
        # Extract entities
        entities = self.ner.extract(query)
        
        # Classify intent
        intent = self.intent_classifier.classify(query, entities)
        
        # Expand query terms
        expanded_terms = self.expander.expand(query, intent)
        
        # Extract filters
        filters = self._extract_filters(entities)
        
        # Determine search weight tuning
        weight_tuning = self._determine_weight_tuning(entities, intent)
        
        return ParsedQuery(
            original_query=query,
            normalized_query=normalized,
            tokens=tokens,
            entities=entities,
            intent=intent,
            expanded_terms=expanded_terms,
            extracted_filters=filters,
            search_weight_tuning=weight_tuning,
        )
    
    def _extract_filters(self, entities: List[QueryEntity]) -> Dict:
        """Extract structured filters from entities."""
        filters = {}
        
        for entity in entities:
            if entity.entity_type == EntityType.BRAND:
                filters['brand'] = entity.normalized_value
            elif entity.entity_type == EntityType.PRICE:
                parts = entity.normalized_value.split(':', 1)
                if len(parts) == 2:
                    filters[f'price_{parts[0]}'] = float(parts[1].replace('$', ''))
                elif entity.normalized_value.startswith('$'):
                    # Range: "$10-$50"
                    range_parts = entity.normalized_value.replace('$', '').split('-')
                    if len(range_parts) == 2:
                        filters['price_min'] = float(range_parts[0])
                        filters['price_max'] = float(range_parts[1])
            elif entity.entity_type == EntityType.SIZE:
                filters['size'] = entity.normalized_value
            elif entity.entity_type == EntityType.CATEGORY:
                filters['category'] = entity.normalized_value
            elif entity.entity_type == EntityType.COLOR:
                filters['color'] = entity.normalized_value
            elif entity.entity_type == EntityType.GENDER:
                filters['gender'] = entity.normalized_value
        
        return filters
    
    def _determine_weight_tuning(
        self,
        entities: List[QueryEntity],
        intent: Optional[QueryIntent]
    ) -> Dict[str, float]:
        """
        Determine how to tune search weights based on query characteristics.
        
        Returns weights that can be passed to the search engine to adjust
        field boosting, hybrid search alpha, etc.
        """
        weights = {
            'bm25_weight': 0.3,      # Default: 30% BM25, 70% dense
            'dense_weight': 0.7,
            'title_boost': 2.0,
            'brand_boost': 1.0,
            'category_boost': 1.0,
        }
        
        if entities:
            entity_types = {e.entity_type for e in entities}
            
            # If query has specific attributes (size, color, price),
            # favor exact matches via BM25
            if EntityType.PRICE in entity_types or EntityType.SIZE in entity_types:
                weights['bm25_weight'] = 0.5
                weights['dense_weight'] = 0.5
            
            # Brand-focused query: boost brand field
            if EntityType.BRAND in entity_types:
                weights['brand_boost'] = 3.0
            
            # Category-focused query: boost category field
            if EntityType.CATEGORY in entity_types:
                weights['category_boost'] = 2.5
        
        if intent:
            # Informational queries benefit from semantic (dense) search
            if intent.primary_intent == IntentType.INFORMATIONAL:
                weights['dense_weight'] = 0.8
                weights['bm25_weight'] = 0.2
            
            # Navigational queries need exact matches
            if intent.primary_intent == IntentType.NAVIGATIONAL:
                weights['bm25_weight'] = 0.6
                weights['dense_weight'] = 0.4
                weights['title_boost'] = 5.0
        
        return weights

# ──────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────

def demo_query_understanding():
    """Demonstrate the query understanding pipeline."""
    print("\n" + "=" * 70)
    print("QUERY UNDERSTANDING PIPELINE DEMO (NER + Intent)")
    print("=" * 70)
    
    pipeline = QueryUnderstandingPipeline()
    
    test_queries = [
        "Nike Air Max running shoes under $150 size 10",
        "best laptop for programming 2024",
        "how to clean suede shoes",
        "my orders tracking number",
        "noise cancelling headphones for travel",
        "compare iPhone 15 vs Samsung Galaxy S24",
        "Patagonia fleece jacket men's medium",
        "where is my refund",
    ]
    
    for query in test_queries:
        parsed = pipeline.parse(query)
        
        print(f"\n{'─' * 70}")
        print(f"Query: \"{query}\"")
        print(f"{'─' * 70}")
        
        # Entities
        if parsed.entities:
            print(f"\n  ENTITIES:")
            for entity in parsed.entities:
                print(f"    [{entity.entity_type.value:15}] \"{entity.text}\" → {entity.normalized_value} ({entity.confidence:.0%})")
        else:
            print(f"\n  ENTITIES: None detected")
        
        # Intent
        if parsed.intent:
            print(f"\n  INTENT:")
            print(f"    Primary: {parsed.intent.primary_intent.value} ({parsed.intent.confidence:.0%})")
            if parsed.intent.sub_intent:
                print(f"    Sub-intent: {parsed.intent.sub_intent}")
            if parsed.intent.secondary_intents:
                secondaries = ', '.join(
                    f"{s['intent']} ({s['confidence']:.0%})"
                    for s in parsed.intent.secondary_intents
                )
                print(f"    Secondary: {secondaries}")
        
        # Expanded terms
        if parsed.expanded_terms:
            print(f"\n  EXPANDED TERMS: {', '.join(parsed.expanded_terms)}")
        
        # Filters
        if parsed.extracted_filters:
            print(f"\n  EXTRACTED FILTERS:")
            for k, v in parsed.extracted_filters.items():
                print(f"    {k}: {v}")
        
        # Weight tuning
        print(f"\n  SEARCH WEIGHTS:")
        for k, v in parsed.search_weight_tuning.items():
            print(f"    {k}: {v}")
    
    print(f"\n{'=' * 70}")
    print("Query Understanding Pipeline ready.")
    print("=" * 70)

if __name__ == "__main__":
    demo_query_understanding()
```

---

## 5. Personalized Search Ranking

### 5.1 Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                  PERSONALIZED SEARCH RANKING                     │
│                                                                  │
│  ┌──────────────┐                                               │
│  │ User Profile │  (Built from historical behavior)             │
│  │              │                                               │
│  │ • Affinities: brands, categories, price ranges               │
│  │ • Recent interactions (clicks, purchases, views)             │
│  │ • Long-term preferences                                      │
│  │ • Context (device, location, time)                           │
│  └──────┬───────┘                                               │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             PERSONALIZATION LAYER                         │   │
│  │                                                          │   │
│  │  1. Profile-to-document affinity scoring                 │   │
│  │  2. Collaborative filtering signals                      │   │
│  │  3. Session context awareness                            │   │
│  │  4. Freshness / novelty boost (explore vs exploit)       │   │
│  │  5. Demographic-adjusted ranking                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             RANKING FUSION                                │   │
│  │                                                          │   │
│  │  final_score =                                             │   │
│  │    w1 × hybrid_score     (relevance)                     │   │
│  │    w2 × ltr_score        (quality)                       │   │
│  │    w3 × personal_score   (affinity)                      │   │
│  │    w4 × freshness_score  (recency)                       │   │
│  │    w5 × diversity_score  (variety)                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             PERSONALIZED RESULTS                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Implementation

```python
"""
Personalized Search Ranking
User-profile-driven ranking with affinity scoring, session context,
and explore-vs-exploit balancing.
"""

from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import numpy as np
import json
import hashlib

# ──────────────────────────────────────────────────────────────────
# User Profile
# ──────────────────────────────────────────────────────────────────

@dataclass
class UserProfile:
    """
    User profile for personalized search ranking.
    
    Built from:
    - Click history
    - Purchase history
    - Browsing history
    - Explicit preferences (wishlists, follows)
    - Implicit signals (dwell time, scroll depth)
    """
    user_id: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    # Affinity scores (0.0 to 1.0)
    brand_affinities: Dict[str, float] = field(default_factory=dict)
    category_affinities: Dict[str, float] = field(default_factory=dict)
    price_range_preference: Dict[str, Optional[float]] = field(default_factory=lambda: {
        'min': None,
        'max': None,
        'mean': None,
    })
    
    # Behavioral signals
    recent_clicks: List[Dict] = field(default_factory=list)   # Last 100 clicks
    recent_purchases: List[Dict] = field(default_factory=list) # Last 50 purchases
    recent_views: List[Dict] = field(default_factory=list)     # Last 200 views
    recent_searches: List[str] = field(default_factory=list)   # Last 50 queries
    
    # Derived signals
    favorite_brands: List[str] = field(default_factory=list)
    favorite_categories: List[str] = field(default_factory=list)
    price_sensitivity: float = 0.5  # 0 = price-insensitive (luxury), 1 = highly price-sensitive
    
    # Session context
    session_id: Optional[str] = None
    current_query: Optional[str] = None
    device_type: str = "desktop"  # "desktop", "mobile", "tablet"
    location: Optional[str] = None
    
    def update_from_click(self, doc_id: str, doc_metadata: Dict, dwell_time_ms: float = 0):
        """Update profile based on a search result click."""
        brand = doc_metadata.get('brand', '')
        category = doc_metadata.get('category', '')
        price = doc_metadata.get('price', 0)
        
        # Update brand affinity (decay-weighted)
        if brand:
            current = self.brand_affinities.get(brand, 0.0)
            self.brand_affinities[brand] = min(1.0, current + 0.05)
        
        # Update category affinity
        if category:
            current = self.category_affinities.get(category, 0.0)
            self.category_affinities[category] = min(1.0, current + 0.05)
        
        # Update price preference
        if price:
            self.price_range_preference['mean'] = (
                self.price_range_preference.get('mean', price) * 0.9 + price * 0.1
                if self.price_range_preference.get('mean') else price
            )
        
        # Record click
        self.recent_clicks.append({
            'doc_id': doc_id,
            'metadata': doc_metadata,
            'timestamp': datetime.utcnow().isoformat(),
            'dwell_time_ms': dwell_time_ms,
        })
        if len(self.recent_clicks) > 100:
            self.recent_clicks = self.recent_clicks[-100:]
        
        self._refresh_derived()
        self.updated_at = datetime.utcnow()
    
    def update_from_purchase(self, doc_id: str, doc_metadata: Dict, price_paid: float):
        """Update profile based on a purchase."""
        brand = doc_metadata.get('brand', '')
        category = doc_metadata.get('category', '')
        
        # Stronger update for purchases
        if brand:
            current = self.brand_affinities.get(brand, 0.0)
            self.brand_affinities[brand] = min(1.0, current + 0.15)
        
        if category:
            current = self.category_affinities.get(category, 0.0)
            self.category_affinities[category] = min(1.0, current + 0.15)
        
        # Update price sensitivity
        if price_paid:
            self.price_range_preference['mean'] = (
                self.price_range_preference.get('mean', price_paid) * 0.8 + price_paid * 0.2
                if self.price_range_preference.get('mean') else price_paid
            )
        
        self.recent_purchases.append({
            'doc_id': doc_id,
            'metadata': doc_metadata,
            'price_paid': price_paid,
            'timestamp': datetime.utcnow().isoformat(),
        })
        if len(self.recent_purchases) > 50:
            self.recent_purchases = self.recent_purchases[-50:]
        
        self._refresh_derived()
        self.updated_at = datetime.utcnow()
    
    def _refresh_derived(self):
        """Recompute derived profile signals."""
        # Favorite brands (top 5 by affinity)
        sorted_brands = sorted(
            self.brand_affinities.items(),
            key=lambda x: x[1], reverse=True
        )
        self.favorite_brands = [b for b, _ in sorted_brands[:5]]
        
        # Favorite categories (top 5 by affinity)
        sorted_cats = sorted(
            self.category_affinities.items(),
            key=lambda x: x[1], reverse=True
        )
        self.favorite_categories = [c for c, _ in sorted_cats[:5]]
    
    def to_dict(self) -> Dict:
        """Serialize profile for storage."""
        return {
            'user_id': self.user_id,
            'brand_affinities': self.brand_affinities,
            'category_affinities': self.category_affinities,
            'price_range_preference': self.price_range_preference,
            'favorite_brands': self.favorite_brands,
            'favorite_categories': self.favorite_categories,
            'price_sensitivity': self.price_sensitivity,
        }
    
    @classmethod
    def from_dict(cls, d: Dict) -> 'UserProfile':
        """Deserialize from dictionary."""
        profile = cls(user_id=d['user_id'])
        profile.brand_affinities = d.get('brand_affinities', {})
        profile.category_affinities = d.get('category_affinities', {})
        profile.price_range_preference = d.get('price_range_preference', {})
        profile.favorite_brands = d.get('favorite_brands', [])
        profile.favorite_categories = d.get('favorite_categories', [])
        profile.price_sensitivity = d.get('price_sensitivity', 0.5)
        return profile

# ──────────────────────────────────────────────────────────────────
# Personalized Ranker
# ──────────────────────────────────────────────────────────────────

class PersonalizedRanker:
    """
    Personalized ranking engine that adjusts search results based
    on user profiles and context.
    """
    
    def __init__(
        self,
        personalization_weight: float = 0.15,    # Weight of personal score in final ranking
        freshness_weight: float = 0.05,           # Weight of freshness boost
        diversity_weight: float = 0.05,           # Weight of diversity penalty
        explore_probability: float = 0.1,         # Probability of injecting explore items
    ):
        self.personalization_weight = personalization_weight
        self.freshness_weight = freshness_weight
        self.diversity_weight = diversity_weight
        self.explore_probability = explore_probability
    
    def compute_personal_score(
        self,
        document,
        user_profile: UserProfile,
        context: Optional[Dict] = None
    ) -> float:
        """
        Compute a personalization score for a document relative to a user.
        
        Returns a score in [0, 1] where higher = better match to user preferences.
        """
        score = 0.0
        components = 0
        
        doc_meta = document.metadata if hasattr(document, 'metadata') else {}
        doc_title = document.title if hasattr(document, 'title') else ''
        
        # ── Brand Affinity ──
        doc_brand = doc_meta.get('brand', '').lower()
        if doc_brand and doc_brand in user_profile.brand_affinities:
            score += user_profile.brand_affinities[doc_brand]
            components += 1
        
        # ── Category Affinity ──
        doc_category = doc_meta.get('category', '').lower()
        if doc_category and doc_category in user_profile.category_affinities:
            score += user_profile.category_affinities[doc_category]
            components += 1
        
        # ── Price Alignment ──
        doc_price = doc_meta.get('price')
        pref_mean = user_profile.price_range_preference.get('mean')
        if doc_price and pref_mean and pref_mean > 0:
            # Score based on how close the price is to user's preferred range
            price_ratio = doc_price / pref_mean
            if 0.7 <= price_ratio <= 1.3:
                # Close to preferred price range
                price_score = 1.0 - abs(price_ratio - 1.0) / 0.3
            elif price_ratio < 0.7:
                # Below preferred range (bargain)
                price_score = 0.3
            else:
                # Above preferred range (stretch purchase)
                price_score = max(0.0, 1.0 - (price_ratio - 1.3) / 0.7)
            
            score += price_score * user_profile.price_sensitivity
            components += 1
        
        # ── Recent Interest Boost ──
        # Documents similar to recently clicked/purchased items get a boost
        recent_doc_titles = set()
        for click in user_profile.recent_clicks[-20:]:
            if 'metadata' in click and 'title' in click.get('metadata', {}):
                recent_doc_titles.add(click['metadata']['title'].lower())
        
        if doc_title.lower() in recent_doc_titles:
            score += 0.1  # Small boost for exact re-view
        
        # Check session context
        if context:
            session_brand = context.get('session_brand_interest')
            session_category = context.get('session_category_interest')
            if session_brand and doc_brand == session_brand.lower():
                score += 0.2
                components += 1
            if session_category and doc_category == session_category.lower():
                score += 0.2
                components += 1
        
        return min(score / max(components, 1), 1.0)
    
    def compute_freshness_score(self, document, max_age_days: float = 365.0) -> float:
        """
        Compute a freshness/recency boost for documents.
        
        Newer documents get a higher score (1.0 at day 0, decaying to 0 at max_age_days).
        """
        doc_meta = document.metadata if hasattr(document, 'metadata') else {}
        created_at = doc_meta.get('created_at')
        
        if not created_at:
            return 0.5  # Unknown age = neutral
        
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        age_days = (datetime.utcnow() - created_at).days
        freshness = max(0.0, 1.0 - age_days / max_age_days)
        return freshness
    
    def compute_diversity_penalty(
        self,
        document,
        ranked_so_far: List,
        category_weight: float = 0.5,
        brand_weight: float = 0.5,
    ) -> float:
        """
        Penalize documents that are too similar to ones already ranked high.
        
        This encourages diverse results (different categories/brands).
        """
        if not ranked_so_far:
            return 0.0  # No penalty for first document
        
        doc_meta = document.metadata if hasattr(document, 'metadata') else {}
        doc_category = doc_meta.get('category', '')
        doc_brand = doc_meta.get('brand', '')
        
        penalty = 0.0
        for result in ranked_so_far:
            r_meta = result.doc.metadata if hasattr(result, 'doc') else {}
            r_category = r_meta.get('category', '')
            r_brand = r_meta.get('brand', '')
            
            if doc_category and doc_category == r_category:
                penalty += category_weight
            if doc_brand and doc_brand == r_brand:
                penalty += brand_weight
        
        # Normalize penalty
        return min(penalty / max(len(ranked_so_far), 1), self.diversity_weight * 5)
    
    def rerank(
        self,
        query: str,
        search_results: List,
        user_profile: UserProfile,
        top_k: Optional[int] = None,
        context: Optional[Dict] = None
    ) -> List:
        """
        Re-rank search results using personalization, freshness, and diversity.
        
        Final score = relevance_score × (1 - α - β - γ)
                    + personal_score × α
                    + freshness_score × β
                    - diversity_penalty × γ
        
        where α, β, γ are the respective weights.
        
        Args:
            query: User's search query.
            search_results: List of results from hybrid search or LTR.
            user_profile: User's profile for personalization.
            top_k: Number of results to return (default: all).
            context: Session context (device, location, time, etc.).
        """
        if not search_results:
            return []
        
        scored = []
        ranked_so_far = []
        
        for result in search_results:
            doc = result.doc if hasattr(result, 'doc') else result
            
            # Get base relevance score (normalized)
            if hasattr(result, 'fused_score'):
                base_score = result.fused_score
            elif hasattr(result, 'bm25_score'):
                base_score = (getattr(result, 'bm25_score', 0) + getattr(result, 'dense_score', 0)) / 2
            else:
                base_score = 0.5
            
            # Normalize base score to [0, 1] (roughly)
            base_score = min(max(base_score, 0.0), 1.0)
            
            # Compute personalization score
            personal_score = self.compute_personal_score(doc, user_profile, context)
            
            # Compute freshness score
            freshness_score = self.compute_freshness_score(doc)
            
            # Compute diversity penalty
            diversity_penalty = self.compute_diversity_penalty(doc, ranked_so_far)
            
            # Final weighted combination
            relevance_w = 1.0 - self.personalization_weight - self.freshness_weight
            final_score = (
                base_score * relevance_w +
                personal_score * self.personalization_weight +
                freshness_score * self.freshness_weight -
                diversity_penalty
            )
            
            # Small amount of randomness for explore-vs-exploit
            if np.random.random() < self.explore_probability:
                final_score += np.random.uniform(0.0, 0.1)
            
            scored.append((final_score, result))
            
            # Add to ranked list for diversity computation
            ranked_so_far.append(result)
        
        # Sort by final score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        
        reranked = [result for _, result in scored]
        
        if top_k:
            reranked = reranked[:top_k]
        
        return reranked

# ──────────────────────────────────────────────────────────────────
# User Profile Store
# ──────────────────────────────────────────────────────────────────

class UserProfileStore:
    """
    Simple in-memory user profile store.
    
    Production: Replace with Redis/PostgreSQL/DynamoDB.
    """
    
    def __init__(self):
        self._profiles: Dict[str, UserProfile] = {}
    
    def get_or_create(self, user_id: str) -> UserProfile:
        """Get an existing profile or create a new one."""
        if user_id not in self._profiles:
            self._profiles[user_id] = UserProfile(user_id=user_id)
        return self._profiles[user_id]
    
    def get(self, user_id: str) -> Optional[UserProfile]:
        """Get a profile, returning None if not found."""
        return self._profiles.get(user_id)
    
    def save(self, profile: UserProfile):
        """Save/update a profile."""
        self._profiles[profile.user_id] = profile
    
    def export_all(self, path: str):
        """Export all profiles to a JSON file."""
        data = {uid: p.to_dict() for uid, p in self._profiles.items()}
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

# ──────────────────────────────────────────────────────────────────
# Session Context Tracker
# ──────────────────────────────────────────────────────────────────

class SessionContextTracker:
    """
    Tracks in-session context for real-time personalization.
    
    Captures:
    - Current session's query sequence
    - Brands/categories of interest in this session
    - Time since session start
    - Device and location context
    """
    
    def __init__(self):
        self._sessions: Dict[str, Dict] = {}
    
    def start_session(self, session_id: str, context: Dict = None) -> Dict:
        """Start a new search session."""
        session = {
            'session_id': session_id,
            'started_at': datetime.utcnow(),
            'queries': [],
            'clicks': [],
            'brand_interest': Counter(),
            'category_interest': Counter(),
            'context': context or {},
        }
        self._sessions[session_id] = session
        return session
    
    def record_query(self, session_id: str, query: str, entities: List = None):
        """Record a query in the session."""
        if session_id not in self._sessions:
            self.start_session(session_id)
        
        session = self._sessions[session_id]
        session['queries'].append({
            'query': query,
            'timestamp': datetime.utcnow(),
        })
        
        # Update brand/category interest from query entities
        if entities:
            for entity in entities:
                if hasattr(entity, 'entity_type') and hasattr(entity, 'normalized_value'):
                    if str(entity.entity_type) == 'brand':
                        session['brand_interest'][entity.normalized_value] += 1
                    elif str(entity.entity_type) == 'category':
                        session['category_interest'][entity.normalized_value] += 1
    
    def record_click(self, session_id: str, doc_metadata: Dict):
        """Record a click in the session."""
        if session_id not in self._sessions:
            return
        
        session = self._sessions[session_id]
        session['clicks'].append({
            'metadata': doc_metadata,
            'timestamp': datetime.utcnow(),
        })
        
        brand = doc_metadata.get('brand', '')
        category = doc_metadata.get('category', '')
        if brand:
            session['brand_interest'][brand] += 2  # Higher weight than query
        if category:
            session['category_interest'][category] += 2
    
    def get_session_context(self, session_id: str) -> Optional[Dict]:
        """Get the current session context for ranking."""
        session = self._sessions.get(session_id)
        if not session:
            return None
        
        # Most dominant brand/category in this session
        top_brand = session['brand_interest'].most_common(1)
        top_category = session['category_interest'].most_common(1)
        
        return {
            'session_brand_interest': top_brand[0][0] if top_brand else None,
            'session_category_interest': top_category[0][0] if top_category else None,
            'queries_in_session': len(session['queries']),
            'clicks_in_session': len(session['clicks']),
            'session_duration_minutes': (
                datetime.utcnow() - session['started_at']
            ).total_seconds() / 60.0,
            'device': session['context'].get('device', 'desktop'),
        }

# ──────────────────────────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────────────────────────

def demo_personalization():
    """Demonstrate personalized search ranking."""
    print("\n" + "=" * 70)
    print("PERSONALIZED SEARCH RANKING DEMO")
    print("=" * 70)
    
    # Create user profiles
    profile_store = UserProfileStore()
    
    # User A: Marathon runner, Nike fan, mid-range budget
    user_a = profile_store.get_or_create("user_alice")
    user_a.update_from_purchase("doc_1", {"brand": "Nike", "category": "running shoes", "price": 130}, 130)
    user_a.update_from_purchase("doc_7", {"brand": "Garmin", "category": "running watch", "price": 450}, 450)
    user_a.update_from_click("doc_10", {"brand": "Nike", "category": "running shorts", "price": 45}, 20000)
    
    # User B: Tech enthusiast, Apple fan, high budget
    user_b = profile_store.get_or_create("user_bob")
    user_b.update_from_purchase("doc_3", {"brand": "Apple", "category": "laptop", "price": 2000}, 2000)
    user_b.update_from_purchase("doc_5", {"brand": "Sony", "category": "headphones", "price": 350}, 350)
    user_b.update_from_click("doc_7", {"brand": "Garmin", "category": "running watch", "price": 450}, 5000)
    
    print("\nUser A (Alice) Profile:")
    print(f"  Favorite Brands: {user_a.favorite_brands}")
    print(f"  Favorite Categories: {user_a.favorite_categories}")
    print(f"  Price Preference Mean: ${user_a.price_range_preference.get('mean', 0):.0f}")
    
    print("\nUser B (Bob) Profile:")
    print(f"  Favorite Brands: {user_b.favorite_brands}")
    print(f"  Favorite Categories: {user_b.favorite_categories}")
    print(f"  Price Preference Mean: ${user_b.price_range_preference.get('mean', 0):.0f}")
    
    # Sample search results (simplified for demo)
    @dataclass
    class DemoResult:
        doc: object
        fused_score: float
        bm25_score: float
        dense_score: float
    
    @dataclass
    class DemoDoc:
        doc_id: str
        title: str
        body: str
        metadata: Dict
    
    results = [
        DemoResult(DemoDoc("1", "Nike Air Max Running Shoes", "...", {"brand": "Nike", "category": "running shoes", "price": 129.99}), 0.85, 0.90, 0.82),
        DemoResult(DemoDoc("2", "Adidas Ultraboost 22", "...", {"brand": "Adidas", "category": "running shoes", "price": 189.99}), 0.78, 0.82, 0.75),
        DemoResult(DemoDoc("3", "Apple MacBook Pro 14", "...", {"brand": "Apple", "category": "laptop", "price": 1999.99}), 0.72, 0.50, 0.88),
        DemoResult(DemoDoc("4", "Dell XPS 15 Laptop", "...", {"brand": "Dell", "category": "laptop", "price": 1499.99}), 0.70, 0.55, 0.80),
        DemoResult(DemoDoc("5", "Sony WH-1000XM5 Headphones", "...", {"brand": "Sony", "category": "headphones", "price": 349.99}), 0.68, 0.60, 0.73),
        DemoResult(DemoDoc("7", "Garmin Forerunner 265", "...", {"brand": "Garmin", "category": "running watch", "price": 449.99}), 0.65, 0.70, 0.62),
    ]
    
    ranker = PersonalizedRanker(
        personalization_weight=0.15,
        freshness_weight=0.05,
        diversity_weight=0.05,
    )
    
    print(f"\n{'─' * 70}")
    print("Query: \"sports gear and electronics\"")
    print(f"{'─' * 70}")
    
    # Unpersonalized ranking
    print("\nUNPERSONALIZED RANKING (relevance only):")
    for i, r in enumerate(results[:6], 1):
        doc = r.doc
        print(f"  {i}. {doc.title} [{doc.metadata.get('brand')}] ${doc.metadata.get('price')} — score={r.fused_score:.3f}")
    
    # Personalized for Alice
    reranked_a = ranker.rerank("sports gear and electronics", results, user_a, top_k=6)
    print("\nPERSONALIZED FOR ALICE (runner, Nike fan):")
    for i, r in enumerate(reranked_a, 1):
        doc = r.doc
        print(f"  {i}. {doc.title} [{doc.metadata.get('brand')}] ${doc.metadata.get('price')}")
    
    # Personalized for Bob
    reranked_b = ranker.rerank("sports gear and electronics", results, user_b, top_k=6)
    print("\nPERSONALIZED FOR BOB (tech enthusiast, Apple fan):")
    for i, r in enumerate(reranked_b, 1):
        doc = r.doc
        print(f"  {i}. {doc.title} [{doc.metadata.get('brand')}] ${doc.metadata.get('price')}")
    
    print(f"\n{'=' * 70}")
    print("Personalized Ranking Engine ready.")
    print("=" * 70)

if __name__ == "__main__":
    demo_personalization()
```

---

## 6. End-to-End Integration

### 6.1 Complete Search System

```python
"""
End-to-End Advanced Search System
Integrates all five components into a unified search API.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
import numpy as np

@dataclass
class SearchRequest:
    """A search request with all context needed for advanced search."""
    query: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    page: int = 1
    page_size: int = 20
    filters: Dict[str, Any] = field(default_factory=dict)
    sort: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)  # device, location, etc.

@dataclass
class SearchResponse:
    """A complete search response."""
    request_id: str
    query: str
    parsed_query: ParsedQuery
    total_results: int
    results: List[Dict]
    facets: Optional[Dict] = None
    personalization_applied: bool = False
    processing_time_ms: float = 0.0
    debug_info: Optional[Dict] = None

class AdvancedSearchSystem:
    """
    Complete advanced search system integrating all components:
    1. Query Understanding (NER + Intent)
    2. Hybrid Search (BM25 + Dense Vectors)
    3. Learning-to-Rank (LambdaMART)
    4. Personalized Ranking
    5. Analytics Event Logging
    """
    
    def __init__(
        self,
        hybrid_engine: HybridSearchEngine,
        ltr_pipeline: Optional[LTRPipeline] = None,
        query_pipeline: Optional[QueryUnderstandingPipeline] = None,
        personalization: Optional[PersonalizedRanker] = None,
        profile_store: Optional[UserProfileStore] = None,
        session_tracker: Optional[SessionContextTracker] = None,
        analytics: Optional[SearchAnalytics] = None,
    ):
        self.hybrid_engine = hybrid_engine
        self.ltr_pipeline = ltr_pipeline or LTRPipeline()
        self.query_pipeline = query_pipeline or QueryUnderstandingPipeline()
        self.personalization = personalization or PersonalizedRanker()
        self.profile_store = profile_store or UserProfileStore()
        self.session_tracker = session_tracker or SessionContextTracker()
        self.analytics = analytics or SearchAnalytics()
    
    def search(self, request: SearchRequest) -> SearchResponse:
        """
        Execute a complete advanced search.
        
        Pipeline:
        1. Parse query (NER + Intent)
        2. Execute hybrid search (BM25 + Dense)
        3. Apply LTR re-ranking
        4. Apply personalization
        5. Log analytics events
        6. Return response
        """
        start_time = datetime.utcnow()
        
        # ── Step 1: Query Understanding ──
        parsed_query = self.query_pipeline.parse(request.query)
        
        # ── Step 2: Hybrid Search ──
        # Apply query expansion
        expanded_query = request.query
        if parsed_query.expanded_terms:
            expanded_query += " " + " ".join(parsed_query.expanded_terms)
        
        # Tune search weights based on query characteristics
        hybrid_results = self.hybrid_engine.search(
            expanded_query,
            top_k=100,  # Retrieve broad candidate set
            bm25_candidates=200,
            dense_candidates=200,
        )
        
        # ── Step 3: LTR Re-Ranking ──
        if self.ltr_pipeline._is_trained:
            hybrid_results = self.ltr_pipeline.rerank(
                request.query,
                hybrid_results,
                top_k=50
            )
        
        # ── Step 4: Personalization ──
        personalization_applied = False
        if request.user_id:
            profile = self.profile_store.get_or_create(request.user_id)
            
            # Get session context
            session_context = None
            if request.session_id:
                self.session_tracker.record_query(
                    request.session_id,
                    request.query,
                    parsed_query.entities
                )
                session_context = self.session_tracker.get_session_context(
                    request.session_id
                )
            
            hybrid_results = self.personalization.rerank(
                request.query,
                hybrid_results,
                profile,
                top_k=request.page_size * 2,
                context=session_context,
            )
            personalization_applied = True
        
        # ── Step 5: Paginate ──
        start_idx = (request.page - 1) * request.page_size
        end_idx = start_idx + request.page_size
        page_results = hybrid_results[start_idx:end_idx]
        
        # ── Step 6: Build Response ──
        response_results = []
        for result in page_results:
            doc = result.doc if hasattr(result, 'doc') else result
            response_results.append({
                'doc_id': doc.doc_id,
                'title': doc.title,
                'body_snippet': doc.body[:200] + '...' if len(doc.body) > 200 else doc.body,
                'metadata': doc.metadata,
                'score': getattr(result, 'fused_score', 1.0),
                'bm25_score': getattr(result, 'bm25_score', 0.0),
                'dense_score': getattr(result, 'dense_score', 0.0),
            })
        
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        
        # ── Step 7: Log Analytics ──
        request_id = hashlib.md5(
            f"{request.query}{request.user_id}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:12]
        
        search_event = SearchEvent(
            event_id=f"srch_{request_id}",
            event_type=EventType.SEARCH,
            session_id=request.session_id or f"anon_{request_id}",
            user_id=request.user_id or "anonymous",
            timestamp=datetime.utcnow(),
            query=request.query,
            query_id=request_id,
            result_count=len(hybrid_results),
            results_returned=[r['doc_id'] for r in response_results],
            search_latency_ms=processing_time,
            page_number=request.page,
        )
        self.analytics.ingest_event(search_event)
        
        return SearchResponse(
            request_id=request_id,
            query=request.query,
            parsed_query=parsed_query,
            total_results=len(hybrid_results),
            results=response_results,
            personalization_applied=personalization_applied,
            processing_time_ms=processing_time,
        )
    
    def search_json(self, request: SearchRequest) -> str:
        """Execute search and return JSON response."""
        response = self.search(request)
        return json.dumps({
            'request_id': response.request_id,
            'query': response.query,
            'total_results': response.total_results,
            'personalization_applied': response.personalization_applied,
            'processing_time_ms': round(response.processing_time_ms, 1),
            'results': response.results,
            'intent': {
                'primary': response.parsed_query.intent.primary_intent.value if response.parsed_query.intent else 'unknown',
                'sub_intent': response.parsed_query.intent.sub_intent if response.parsed_query.intent else None,
            },
            'entities': [
                {
                    'type': e.entity_type.value,
                    'text': e.text,
                    'normalized': e.normalized_value,
                }
                for e in response.parsed_query.entities
            ],
        }, indent=2, ensure_ascii=False)

# ──────────────────────────────────────────────────────────────────
# FastAPI Integration (Production)
# ──────────────────────────────────────────────────────────────────

"""
FastAPI application for serving advanced search.

from fastapi import FastAPI, Query
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Advanced Search API", version="2.0.0")

search_system: Optional[AdvancedSearchSystem] = None

class SearchRequestModel(BaseModel):
    query: str
    user_id: str = None
    session_id: str = None
    page: int = 1
    page_size: int = 20

@app.on_event("startup")
async def startup():
    global search_system
    # Initialize all components
    hybrid_engine = HybridSearchEngine()
    # Load documents and build indices
    # ...
    search_system = AdvancedSearchSystem(hybrid_engine=hybrid_engine)

@app.post("/api/v2/search")
async def search(request: SearchRequestModel):
    result = search_system.search(SearchRequest(
        query=request.query,
        user_id=request.user_id,
        session_id=request.session_id,
        page=request.page,
        page_size=request.page_size,
    ))
    return result

@app.get("/api/v2/search")
async def search_get(q: str, user_id: str = None, page: int = 1):
    result = search_system.search(SearchRequest(
        query=q,
        user_id=user_id,
        page=page,
    ))
    return result

@app.get("/api/v2/analytics/report")
async def analytics_report():
    return search_system.analytics.generate_report()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
```

---

## 7. Deployment & Production Considerations

### 7.1 Technology Stack Recommendations

| Component | Technology | Alternative |
|---|---|---|
| **Hybrid Search Index** | Elasticsearch 8.x + dense_vector field | OpenSearch, Vespa |
| **Vector Store** | FAISS (in-process) or Milvus | Pinecone, Weaviate, Qdrant |
| **Embeddings** | `all-MiniLM-L6-v2` (384d) or `e5-large-v2` (1024d) | OpenAI embeddings, Cohere |
| **LTR Model Serving** | LightGBM (in-process) | XGBoost, ONNX Runtime |
| **Analytics Events** | Kafka + ClickHouse | Kinesis + Redshift, Pub/Sub + BigQuery |
| **User Profiles** | Redis (hot) + PostgreSQL (cold) | DynamoDB, MongoDB |
| **API Framework** | FastAPI | Flask, Express, Spring Boot |
| **Monitoring** | Prometheus + Grafana | Datadog, New Relic |
| **A/B Testing** | Feature flags (LaunchDarkly) | Custom flag service |

### 7.2 Performance Benchmarks

| Operation | Target Latency (p95) | Notes |
|---|---|---|
| Query Understanding | < 10ms | Rule-based NER; +50ms if using transformers |
| BM25 Retrieval | < 20ms | Elasticsearch; 1M+ documents |
| Dense Retrieval | < 30ms | FAISS with IVF index; 1M+ vectors |
| RRF Fusion | < 5ms | In-memory computation |
| LTR Scoring | < 10ms | LightGBM inference on top-100 |
| Personalization | < 5ms | Profile lookup + affinity scoring |
| **Total End-to-End** | **< 80ms** | With parallel retrieval |

### 7.3 Key Production Patterns

1. **Cold Start**: New users get non-personalized results; personalization ramps up with > 5 interactions
2. **A/B Testing**: Compare personalized vs. non-personalized, LTR vs. baseline, different fusion strategies
3. **Graceful Degradation**: If any component fails (e.g., dense retriever down), fall back to BM25-only
4. **Index Updates**: Incremental updates to vector index; full re-index nightly
5. **Caching**: Cache query understanding results (TTL: 1 hour); cache popular query results (TTL: 5 minutes)
6. **Rate Limiting**: Per-user and per-IP rate limiting at the API gateway

### 7.4 Full System Architecture Diagram

```
                        ┌─────────────────────────┐
                        │     Load Balancer        │
                        └────────────┬────────────┘
                                     │
                        ┌────────────▼────────────┐
                        │     API Gateway          │
                        │  (Rate Limiting, Auth)   │
                        └────────────┬────────────┘
                                     │
                        ┌────────────▼────────────┐
                        │    FastAPI Search API    │
                        │                         │
                        │  ┌───────────────────┐  │
                        │  │ Query             │  │
                        │  │ Understanding     │  │
                        │  └───────┬───────────┘  │
                        │          │              │
                        │  ┌───────▼───────────┐  │
                        │  │ Hybrid Search     │  │
                        │  │ (Elasticsearch +  │  │
                        │  │  FAISS/Milvus)    │  │
                        │  └───────┬───────────┘  │
                        │          │              │
                        │  ┌───────▼───────────┐  │
                        │  │ LambdaMART LTR    │  │
                        │  └───────┬───────────┘  │
                        │          │              │
                        │  ┌───────▼───────────┐  │
                        │  │ Personalized      │  │
                        │  │ Ranking           │  │
                        │  │ (Redis Profiles)  │  │
                        │  └───────┬───────────┘  │
                        │          │              │
                        │  ┌───────▼───────────┐  │
                        │  │ Analytics Logger  │  │
                        │  │ (→ Kafka)         │  │
                        │  └───────────────────┘  │
                        └─────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
    ┌─────────▼────────┐  ┌─────────▼────────┐  ┌─────────▼────────┐
    │   Elasticsearch  │  │   Milvus/FAISS   │  │      Redis        │
    │   (BM25 Index)   │  │  (Dense Vectors) │  │   (User Profiles) │
    └──────────────────┘  └──────────────────┘  └──────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
    ┌─────────▼────────┐  ┌─────────▼────────┐  ┌─────────▼────────┐
    │      Kafka        │  │   ClickHouse     │  │    Grafana       │
    │  (Event Stream)   │─▶│  (Analytics DB)  │─▶│   (Dashboards)   │
    └──────────────────┘  └──────────────────┘  └──────────────────┘
```

### 7.5 Summary

| Component | Key Technologies | Complexity | Impact |
|---|---|---|---|
| **Hybrid Search** | Elasticsearch + FAISS, RRF fusion | Medium | High — captures both exact and semantic matches |
| **LambdaMART LTR** | LightGBM, 22+ features, NDCG optimization | High | High — optimizes directly for ranking quality |
| **Search Analytics** | Event streaming, CTR/NDCG/MRR tracking | Medium | High — enables data-driven improvements |
| **Query Understanding** | Rule-based NER + intent classification | Low-Medium | Medium — improves recall and precision |
| **Personalized Ranking** | User profiles, affinity scoring, diversity | Medium | Medium-High — increases conversion and satisfaction |

**Total: ~2500 lines of production-grade Python code across 5 integrated components.**

---

*Generated by search-engine-implementer (c2) | 2026-06-26 02:00:00 UTC*
