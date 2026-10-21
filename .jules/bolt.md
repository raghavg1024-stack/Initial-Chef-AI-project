# Bolt Performance Journal

## 2025-05-18 - Streamlit Cache Key Normalization
**Learning:** Functions cached via `@st.cache_data` in Streamlit compute cache keys directly from positional and keyword arguments. Pre-normalizing input strings (such as stripping leading/trailing whitespace) before passing them to the cached function prevents cache misses across equivalent inputs and avoids redundant expensive backend LLM calls.
**Action:** Always trim/normalize input arguments before invoking `@st.cache_data` decorated functions in Streamlit.
