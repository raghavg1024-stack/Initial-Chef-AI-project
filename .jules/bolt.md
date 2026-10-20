## 2025-05-18 - Cache Key Canonicalization in Streamlit
**Learning:** Streamlit's `@st.cache_data` hashes raw input arguments before function execution. Unnormalized user inputs with leading or trailing whitespace bypass the cache even if internal function logic normalizes them.
**Action:** Always canonicalize/strip string arguments before passing them to `@st.cache_data` decorated functions to ensure maximum cache hit rates and prevent redundant LLM backend calls.
