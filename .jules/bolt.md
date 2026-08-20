## 2025-05-18 - Caching LLM calls in Streamlit & Guarding against empty inputs

**Learning:** Streamlit re-executes the script on every interaction. Calling external LLM services like `ollama.chat` on identical queries without caching introduces huge latency penalties (several seconds per call). Furthermore, sending empty or whitespace-only queries to LLM endpoints wastes resources and delays UI updates unnecessarily.
**Action:** Always wrap expensive or repetitive LLM query functions with `@st.cache_data` in Streamlit apps and include early guards/returns for empty or invalid inputs.
