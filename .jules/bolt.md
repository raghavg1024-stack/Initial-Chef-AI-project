## 2025-05-18 - Normalizing Input Keys Before Streamlit Caching

**Learning:** `@st.cache_data` in Streamlit hashes exact argument values to construct cache keys. Unnormalized text input from UI fields (containing leading, trailing, or inconsistent whitespace) results in cache misses and redundant LLM API calls for identical semantic user queries.
**Action:** Strip and normalize user input strings before passing them to `@st.cache_data` decorated functions so equivalent queries hit the same cached response.
