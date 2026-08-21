## 2026-08-21 - Streamlit LLM Response Caching
**Learning:** In Streamlit applications, full-script re-execution triggers redundant LLM calls on every button click or widget state change. Using `@st.cache_data` on model query functions prevents redundant local model invocations for identical queries, bringing latency down from seconds to ~0ms.
**Action:** Always decorate expensive LLM/API querying functions in Streamlit with `@st.cache_data` and guard against empty string queries.
