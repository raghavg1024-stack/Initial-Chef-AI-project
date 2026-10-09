# Bolt's Journal - Critical Learnings

## 2025-05-18 - Query Normalization Before Streamlit Cache
**Learning:** In Streamlit apps caching LLM queries with `@st.cache_data`, passing un-stripped user inputs creates cache misses for identical queries with leading/trailing whitespace. Normalizing input queries prior to function invocation eliminates redundant LLM calls and avoids redundant static prompt memory allocation on every query.
**Action:** Always extract static system prompt structures module-wide and normalize/strip input arguments before triggering cached LLM backend functions.
