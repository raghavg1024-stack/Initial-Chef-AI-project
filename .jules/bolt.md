## 2026-08-24 - Streamlit LLM Response Caching
**Learning:** Streamlit re-executes the python script from top to bottom on every user interaction (e.g. button click or input modification). Wrapping LLM query calls with `@st.cache_data` prevents duplicate expensive model calls for repeated inputs across reruns.
**Action:** Always decorate expensive LLM generation functions with `@st.cache_data` and add early returns for empty/whitespace inputs in Streamlit applications.
