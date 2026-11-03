# Bolt's Performance Journal

## 2026-11-03 - Query normalization unlocks dramatic LLM cache hit rate
**Learning:** Exact string caching (`@st.cache_data`) for conversational LLM interfaces fails when users introduce trivial whitespace differences or casing variations, unnecessarily executing costly multi-second LLM inferences. Text normalization (`" ".join(question.strip().lower().split())`) costs under 1 microsecond while converting redundant queries into instant cache hits.
**Action:** When caching expensive backend/LLM queries, separate semantic normalization from caching logic and delegate the cache key to the canonical representation.
