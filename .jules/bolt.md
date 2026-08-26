## 2026-08-26 - Streamlit Ollama Response Caching
**Learning:** Streamlit reruns the script on UI interactions. Calling external LLMs (e.g. Ollama `ollama.chat`) directly during Streamlit execution without caching causes redundant model inferences on identical input.
**Action:** Use Streamlit's `@st.cache_data` decorator on functions calling `ollama.chat` to eliminate redundant network/LLM latency and save multiple seconds on repeated queries.
