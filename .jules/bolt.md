# Bolt's Journal - Critical Learnings

## 2025-08-15 - Streamlit LLM Response Caching & Payload Optimization
**Learning:** In Streamlit apps calling LLM APIs (like Ollama), every user interaction re-executes the script. Uncached LLM function calls cause expensive repeated API calls for identical user queries, and defining system prompt dicts inside function scope creates unnecessary dict/string allocations on every invocation.
**Action:** Use `@st.cache_data` on query functions and pull static system prompt definitions outside the function body with trimmed whitespace.
