## 2026-10-02 - Streamlit Cache Key Normalization for LLM Queries
**Learning:** Streamlit's `@st.cache_data` builds cache key hashes from raw input parameter values before function execution. If query strings with surrounding whitespace or varying formatting are passed into `@st.cache_data` decorated functions, distinct cache entries are created, triggering redundant and expensive multi-second LLM calls.
**Action:** Always strip and normalize string inputs before passing them into cached LLM wrapper functions to maximize cache hit rates on semantically identical user queries.
