## 2025-02-18 - Input Normalization for Streamlit LLM Caching
**Learning:** Functions decorated with Streamlit's `@st.cache_data` hash exact input arguments. Performing string normalization (e.g., `question.strip()`) inside the cached function causes inputs differing only by whitespace to miss cache and trigger expensive LLM calls.
**Action:** Always normalize string arguments before calling `@st.cache_data` wrapped LLM functions, and pass `keep_alive` to Ollama to eliminate cold-start loading latencies.
