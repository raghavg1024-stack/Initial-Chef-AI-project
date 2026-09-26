## 2026-09-26 - Streamlit `@st.cache_data` Argument Normalization
**Learning:** Streamlit's `@st.cache_data` hashes input arguments at the wrapper level before the decorated function body executes. Normalizing or stripping strings inside the cached function body does not prevent different raw inputs (such as `"query "` vs `"query"`) from creating separate cache keys and missing the cache.
**Action:** Always sanitize/normalize input parameters in an outer wrapper function before passing them into the `@st.cache_data` cached inner function.
