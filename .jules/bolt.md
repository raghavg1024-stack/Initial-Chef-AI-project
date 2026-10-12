# Bolt's Journal

## 2025-05-18 - Input Normalization for Streamlit Caching
**Learning:** Streamlit `@st.cache_data` hashes input arguments directly. Unstripped input strings with trailing spaces generate unique cache keys for identical logical queries, leading to unnecessary LLM calls.
**Action:** Always normalize/strip string inputs before passing them into cached Streamlit functions, and optimize static system prompts to minimize token payload overhead.
