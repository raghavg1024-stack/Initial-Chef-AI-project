## 2025-05-20 - Streamlit LLM Response Caching
**Learning:** Streamlit apps re-run the entire script execution on every user interaction. Wrapping expensive LLM API calls like `ollama.chat` with `@st.cache_data` avoids redundant processing and network calls for repeated user prompts.
**Action:** Use `@st.cache_data` on functions querying LLMs or external APIs in Streamlit applications.
