Now I have complete system understanding. Here is the Memory Provider Tune assessment and recommendations:
CURRENT STATE:
- Provider: built-in only (MEMORY.md / USER.md). No external provider configured (memory.provider: '').
- Storage: flat files, §-delimited entries, char-bounded (MEMORY.md: 2200, USER.md: 1375).
- Embedding: NONE. No semantic search. Pure substring matching for replace/remove.
- Retrieval: linear scan of entries at session start. Frozen system prompt snapshot.
- Write mechanism: manual `memory` tool (add/replace/remove/operations). No automatic fact extraction.
- Capacity: 591 bytes MEMORY.md (4 entries), 417 bytes USER.md (1 entry). 26% / 29% used respectively.
AVAILABLE EXTERNAL PROVIDERS:
1. Honcho -- dialectic Q&A, peer cards, semantic search. Cloud API (api_key) + SDK. 4 tools (profile, search, context, conclude). Has recall_mode (context/tools/hybrid) + cadence control.
2. Mem0 -- server-side LLM fact extraction, semantic search, dedup. Platform (cloud API) or OSS (self-hosted with Qdrant/PGVector). 5 tools (list, search, add, update, delete). Embedding via OpenAI (text-embedding-3-small @ 1536d) or Ollama (nomic-embed-text @ 768d).
3. Hindsight -- knowledge graph, entity resolution, multi-strategy retrieval. Cloud or local (embedded daemon). Configurable budget (low/mid/high), tags, retention.
4. Holographic -- HRR-based compositional retrieval, entity resolution, trust scoring. SQLite-backed, no external dependencies. Local-only.
5. ByteRover -- hierarchical context tree via CLI (brv). Tiered retrieval (fuzzy text -> LLM search). Local-first, optional cloud sync.
6. openviking -- mentioned in CLI help, no plugin found in this install.
RECOMMENDATION (your use case: Swedish developer, Styde Forge, autonomous multi-agent workflows):
PRIMARY CHOICE: **Mem0 OSS** with local Qdrant + Ollama embedding.
RATIONALE:
- No API dependency (segfault/hosted outages won't block Forge spawning).
- Server-side extraction: each turn (user/assistant) automatically feeds Mem0, which infers facts and stores embeddings. The agent doesn't need to manually call `memory` tool.
- Semantic search at prefetch: queue_prefetch() runs background embedding search before each turn. Relevant context surfaces automatically.
- Open endpoint cost: embedding model runs over Ollama (nomic-embed-text, 768d). Zero per-call cost. Reasonable quality for Swedish + English mixed content.
ALTERNATIVE: Honcho if you want the dialectic reasoning layer (synthesized answers, not just raw fact retrieval). Trade-off: requires cloud API key, adds network latency per turn.
IMMEDIATE ACTION needed in config.yaml:
```
memory:
  memory_enabled: true
  user_profile_enabled: true
  write_approval: false
  memory_char_limit: 2200
  user_char_limit: 1375
  provider: mem0         # <-- empty string currently
  nudge_interval: 10
  flush_min_turns: 6
```
SETUP steps required: run `hermes memory setup mem0` which walks through mode (OSS), Ollama URL, Qdrant path, user_id, agent_id. Then install pip deps (mem0ai, qdrant-client).
EMBEDDING TUNE: For OSS mode, the optimal config is:
- embedder: ollama, model: nomic-embed-text (768d, good for mixed-language)
- vector_store: qdrant, path: ~/.hermes/mem0_qdrant (already default)
- llm: skip the LLM in OSS config for minimal deps -- Mem0's infer=True sync does server-side extraction already
RETRIEVAL TUNE:
- top_k: 5 at prefetch (current default). Sufficient for memory context injection.
- rerank: enabled (platform mode only -- not available in OSS).
- Circuit breaker: 5 consecutive failures -> 120s cooldown. Good for Forge batch runs where a service might be temporarily down.
PRUNE: Mem0 has no built-in pruning. Use mem0_list + mem0_delete via tools, or directly manage the Qdrant collection. Set mem0.json retention if needed.
EVAL: No formal precision/recall measurement exists. Could add by: 1) storing ground-truth facts, 2) running known queries, 3) comparing recall result IDs vs expected IDs. Not implemented upstream.
To execute: Run `hermes memory setup mem0` from your terminal. Answer OSS mode, Ollama URL http://localhost:11434, Qdrant path defaults. This will write the config and activate the provider on next agent start.