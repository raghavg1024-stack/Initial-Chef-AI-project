# Bolt's Journal - Critical Learnings

## 2025-05-18 - Input Normalization for Streamlit Cache Keys
**Learning:** Streamlit's `@st.cache_data` builds cache keys directly from raw function parameters. Passing raw user string inputs (with leading/trailing whitespace) to cached LLM wrappers creates cache key misses for semantically identical queries.
**Action:** Always normalize/strip string inputs before passing them into `@st.cache_data` wrapped functions to maximize cache hit rates and eliminate redundant LLM API calls.
