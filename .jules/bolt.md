## 2026-03-29 - Streamlit Cache Key Normalization for LLM Queries
**Learning:** Streamlit's `@st.cache_data` generates cache keys based on exact function arguments. Passing raw user input strings with leading/trailing whitespace bypasses the cache and causes redundant, multi-second LLM calls to Ollama. Pre-normalizing (stripping) strings before calling the `@st.cache_data` function ensures identical cache keys for equivalent queries.
**Action:** Always perform input normalization before passing parameters to `@st.cache_data` wrapped functions when wrapping expensive LLM or API calls.
