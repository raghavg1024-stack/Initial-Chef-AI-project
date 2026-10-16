## 2026-03-31 - Streamlit Cache Key Normalization
**Learning:** `@st.cache_data` hashes raw input arguments. Minor string variations like leading/trailing whitespace bypass the cache and trigger expensive LLM calls.
**Action:** Always normalize inputs (`question.strip()`) before passing them to `@st.cache_data` decorated functions.
