## 2025-09-08 - Streamlit Cache Key Normalization & Prompt Token Overhead

**Learning:** Streamlit's `@st.cache_data` computes cache hashes directly from the function arguments at the call site. Passing un-stripped string inputs (e.g. from `st.text_input`) causes identical semantic queries with differing whitespace to miss the cache and trigger redundant LLM backend calls. Additionally, multi-line indented strings in prompt templates add unnecessary whitespace tokens to every LLM request.

**Action:** Normalize user inputs prior to passing them to `@st.cache_data` cached functions, and define system prompts as clean module-level constants without extra indentation.
