# Bolt's Journal - Critical Learnings

## 2025-05-15 - Streamlit @st.cache_data for Ollama API Calls
**Learning:** Caching expensive LLM API calls with `@st.cache_data` in Streamlit prevents redundant network overhead and backend inference latency for repeated user queries.
**Action:** Always wrap deterministic/repeated LLM query functions with `@st.cache_data`.
