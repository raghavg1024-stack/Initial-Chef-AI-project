## 2026-08-22 - Streamlit LLM Call Caching with `@st.cache_data`

**Learning:** Streamlit re-executes the script from top to bottom on every user interaction (e.g., clicking a button or changing an input field). Uncached LLM function calls (like `ollama.chat`) re-trigger local inference or network requests repeatedly even for duplicate queries, causing significant latency (~seconds down to <1ms cached) and unneeded compute overhead.
**Action:** Use `@st.cache_data` on LLM query functions and validate inputs with early returns to ensure repeated queries return instantly from memory cache without hitting the LLM model again.
