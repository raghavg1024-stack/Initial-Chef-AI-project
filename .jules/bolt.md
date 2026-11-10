# Bolt's Journal

## 2026-11-10 - Streamlit Cache Key Sensitivity to Whitespace
**Learning:** `st.cache_data` caches function results based on hashing exact function arguments. When user text input contains trailing or leading whitespace variations (e.g. `'pasta'` vs `' pasta '`), passing raw input results in cache misses and triggers expensive backend LLM calls even if the function strips the input internally.
**Action:** Normalize user inputs (e.g., `.strip()`) at the callsite before passing to `@st.cache_data` decorated functions to ensure maximum cache hit rates across user inputs.
