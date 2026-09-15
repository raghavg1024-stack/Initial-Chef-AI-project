## 2026-09-15 - Streamlit Cache Key Normalization
**Learning:** Streamlit's `@st.cache_data` hashes input arguments directly. Normalizing or stripping string parameters inside the cached function still results in cache misses for queries that differ only by leading/trailing whitespace.
**Action:** Normalize string input before passing it to `@st.cache_data` decorated functions to maximize cache hit rate and avoid redundant backend calls.
