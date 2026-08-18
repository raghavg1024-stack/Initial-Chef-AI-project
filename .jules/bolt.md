# Bolt's Journal - Critical Learnings

## 2025-05-18 - Caching Ollama LLM responses with `@st.cache_data` in Streamlit
**Learning:** LLM API inference calls (e.g. `ollama.chat`) are high-latency I/O operations (often 500ms - several seconds). Streamlit re-runs the entire script on user interaction. Using `@st.cache_data` caches LLM responses across Streamlit re-runs for identical query inputs, eliminating redundant API calls and dropping repeat query latency to sub-millisecond.
**Action:** Always wrap expensive external I/O or LLM query functions in Streamlit apps with `@st.cache_data` (or `@st.cache_resource` for connections).
