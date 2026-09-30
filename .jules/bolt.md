## 2026-09-30 - Normalize inputs prior to `@st.cache_data` in Streamlit
**Learning:** Streamlit's `@st.cache_data` computes cache keys based on exact argument values. Normalizing user query strings (trimming whitespace and lowercasing) in a wrapper function before calling the cached function prevents cache misses caused purely by casing or spacing variations. Re-binding `wrapper.clear = cached_fn.clear` preserves cache invalidation functionality.
**Action:** When using `@st.cache_data` on user text inputs, normalize inputs in an outer wrapper function before forwarding to the cached function.
