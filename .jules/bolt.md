## 2025-02-17 - Streamlit Cache Key Normalization
**Learning:** Functions cached with `@st.cache_data` hash their exact input parameters. Passing raw string inputs with variable leading or trailing whitespace causes cache misses for logically identical queries, leading to unnecessary and expensive backend LLM calls.
**Action:** Always strip/normalize string parameters before passing them into `@st.cache_data` functions, and hoist static system prompt objects to module scope to avoid redundant memory allocations.
