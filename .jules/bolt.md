## 2026-09-13 - String Normalization Before `@st.cache_data`

**Learning:** Streamlit's `@st.cache_data` hashes function arguments as raw objects (including exact case and surrounding whitespace for strings). Standard string custom hash functions passed via `hash_funcs={str: ...}` in `@st.cache_data` can lead to recursive hashing stack overflows in Streamlit's inner hasher.
**Action:** Always perform string normalization (trimming whitespace and lowercased case-folding) in an un-cached wrapper function before calling the `@st.cache_data` decorated function to maximize cache hit rates for expensive LLM / external API calls.
