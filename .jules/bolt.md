## 2025-05-18 - Input Normalization Before Streamlit Caching
**Learning:** Functions decorated with `@st.cache_data` construct cache keys from raw input arguments. If input normalization (like `.strip()`) occurs inside the cached function, queries differing only by whitespace will trigger separate cache misses and expensive LLM calls. Pre-normalizing input before invoking the cached inner function maximizes cache hits.
**Action:** Wrap `@st.cache_data` functions with a wrapper that normalizes inputs and delegates `.clear()` to the underlying cached function.
