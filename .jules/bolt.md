# Bolt ⚡ Performance Journal

## 2025-05-18 - Input Normalization Before Streamlit Caching
**Learning:** Streamlit's `@st.cache_data` computes cache keys based on raw argument values passed to the function. If string normalization (e.g. `question.strip()`) occurs inside the function body rather than before the function call, queries with leading or trailing whitespace variations miss the cache and trigger redundant, expensive calls to backend services like Ollama LLM.
**Action:** Always normalize string arguments prior to invoking `@st.cache_data` decorated functions to ensure maximum cache hit rate for equivalent user queries.
