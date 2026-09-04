# Bolt ⚡ Performance Journal

## 2026-03-30 - Streamlit Cache Key Normalization
**Learning:** Functions decorated with `@st.cache_data` use exact string arguments for cache keys. Without upfront whitespace normalization before calling the cached function, inputs like `"pasta "` and `"pasta"` produce cache misses, causing duplicate expensive LLM calls.
**Action:** Always strip and normalize string inputs *before* passing them into `@st.cache_data` functions, and hoist static prompt data out of the cached function body.
