# Bolt's Performance Journal

## 2025-05-18 - Streamlit LLM Response Caching
**Learning:** Calling local LLM APIs (like `ollama.chat`) during Streamlit re-renders introduces latency (~seconds per call). Streamlit re-runs the script on user interactions.
**Action:** Use `@st.cache_data` on functions querying Ollama so identical cooking questions return instantly without repeating LLM inference calls.
