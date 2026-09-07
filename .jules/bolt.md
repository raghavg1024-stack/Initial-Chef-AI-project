## 2025-05-18 - Streamlit Cache Key Normalization & Constant Reuse
**Learning:** Streamlit `@st.cache_data` hashes raw argument inputs before function execution. If string arguments have whitespace variations, `@st.cache_data` treats them as distinct cache keys even if internal function logic strips them later. Normalizing inputs prior to calling the cached function prevents redundant backend/LLM invocations.
**Action:** Sanitize/strip input strings before delegating to `@st.cache_data` decorated functions, and reuse static prompt objects at module scope.
