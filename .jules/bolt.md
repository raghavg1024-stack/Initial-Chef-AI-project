## 2025-05-18 - Input Normalization for Streamlit LLM Caching
**Learning:** Normalizing user queries (stripping whitespace, collapsing multiple spaces, lowercasing) before caching with `@st.cache_data` prevents redundant, expensive LLM calls when users submit queries with varying casing or spacing.
**Action:** Always normalize string input arguments before passing them into cached wrapper functions for LLMs or costly operations.
