## 2026-10-10 - Streamlit Caching Parameter Normalization
**Learning:** Streamlit's `@st.cache_data` caches function outputs based on exact parameter values passed to the decorated function. If input strings contain unstripped leading/trailing whitespace, Streamlit treats them as distinct keys, causing unnecessary LLM invocations for duplicate queries.
**Action:** Always normalize/strip string arguments before passing them into functions decorated with `@st.cache_data`, or wrap the decorated function inside a helper that handles input normalization.
