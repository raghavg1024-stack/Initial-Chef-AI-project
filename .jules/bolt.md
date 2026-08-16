## 2025-05-18 - Streamlit LLM Response Caching and Early Input Validation
**Learning:** Streamlit apps rerun functions frequently on UI interactions. Caching expensive LLM calls (`ollama.chat`) with `@st.cache_data` and validating inputs early prevents unnecessary model inference and network overhead for duplicate or empty queries.
**Action:** Always check Streamlit helper functions for missing `@st.cache_data` / `@st.cache_resource` decorators and validate empty inputs before invoking external model APIs.
