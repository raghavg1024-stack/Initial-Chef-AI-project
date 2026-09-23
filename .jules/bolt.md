## 2026-03-31 - Streamlit Cache Key Normalization
**Learning:** `@st.cache_data` hashes exact raw function argument values. When caching LLM queries or API calls, passing un-normalized strings (with leading/trailing whitespace) causes cache misses on semantically identical inputs, triggering duplicate expensive LLM calls.
**Action:** Normalize string arguments (e.g., `.strip()`) before passing them to `@st.cache_data` decorated functions to ensure maximum cache hit rate.
