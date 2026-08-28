# Bolt's Journal - Performance Learnings

## 2026-08-28 - Streamlit LLM Response Caching
**Learning:** In Streamlit applications querying local/remote LLMs (like Ollama), uncached function calls execute on every rerun/button press, causing expensive repeated inference latency (1-5+ seconds per request). `@st.cache_data` memoizes responses for identical input strings.
**Action:** Always wrap deterministic LLM query functions with `@st.cache_data` in Streamlit apps to ensure instantaneous response for repeated queries.
