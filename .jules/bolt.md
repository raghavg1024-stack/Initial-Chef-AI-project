## 2026-03-29 - Streamlit Cache Key Input Normalization
**Learning:** `@st.cache_data` in Streamlit computes cache keys based on exact function parameter values. Inputs with un-normalized whitespace cause cache misses and trigger unnecessary, expensive calls to external LLM services.
**Action:** Always clean/strip string parameters prior to passing them into `@st.cache_data` decorated functions to maximize cache hits.
