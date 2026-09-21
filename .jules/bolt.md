# Bolt's Performance Journal

## 2025-05-18 - Streamlit Cache Key Normalization
**Learning:** Streamlit `@st.cache_data` computes cache keys based on exact input argument equality. Passing raw user input with varying leading/trailing whitespace bypasses the cache and triggers duplicate multi-second LLM calls to Ollama.
**Action:** Always normalize/strip input arguments before passing them into `@st.cache_data` decorated functions to maximize cache hit rate for equivalent user queries.
