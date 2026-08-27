## 2026-08-27 - Streamlit LLM Query Caching
**Learning:** In Streamlit applications, user interactions trigger a full rerun of the script. Without caching (`@st.cache_data`), button clicks or input updates cause redundant network/computation calls to Ollama.
**Action:** Always wrap Ollama/LLM inference functions in Streamlit apps with `@st.cache_data` when deterministic responses for identical prompts are expected.
