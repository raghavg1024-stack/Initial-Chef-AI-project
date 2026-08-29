## 2026-08-29 - Streamlit LLM Response Caching & Static Constant Extraction
**Learning:** Streamlit reruns the entire Python script on every user interaction. Without `@st.cache_data`, expensive external LLM API/inference calls (`ollama.chat`) are re-executed even for identical questions, causing high latency (~seconds per call).
**Action:** Always decorate deterministic or repetitive LLM inference functions with `@st.cache_data` in Streamlit apps, and hoist static prompts outside function scopes to prevent unnecessary string re-allocation on every rerun.
