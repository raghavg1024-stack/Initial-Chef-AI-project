# Bolt's Journal - Critical Learnings

## 2026-03-29 - Streamlit Cache Key Normalization
**Learning:** `@st.cache_data` computes cache keys directly from function argument inputs before function execution. If input values contain variations like leading/trailing whitespace, Streamlit treats them as distinct keys, missing the cache even if `strip()` is called inside the cached function.
**Action:** Always normalize or strip text inputs before passing them into `@st.cache_data` decorated functions to ensure maximum cache hit rates for duplicate queries.
