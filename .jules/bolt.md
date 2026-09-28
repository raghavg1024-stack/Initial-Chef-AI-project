## 2026-09-03 - Streamlit @st.cache_data Cache Key Sensitivity
**Learning:** Streamlit `@st.cache_data` keys cached function calls based on argument value equality prior to execution. Normalizing arguments (such as `.strip()` on user text inputs) at the call site ensures query variations share cache hits, preventing redundant LLM backend invocations.
**Action:** Always normalize text inputs at the Streamlit UI call site before passing them to `@st.cache_data` functions.
