# Bolt's Journal

## 2026-11-11 - Streamlit Cache Key Normalization
**Learning:** Streamlit's `@st.cache_data` hashes raw function arguments to generate the cache key before the function body executes. If a function accepting user input is decorated directly, variations in whitespace (e.g. leading/trailing spaces or tabs) cause cache misses and trigger redundant, expensive backend calls (such as LLM inference) even when the backend receives a stripped string. Additionally, caching empty inputs wastes cache storage.
**Action:** Validate and normalize input arguments (e.g. via `strip()`) in an outer wrapper before calling a separate `@st.cache_data`-decorated helper, returning early for empty inputs and exposing `.clear = _helper.clear` for cache invalidation.
