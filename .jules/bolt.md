# Bolt's Performance Journal

## 2026-11-04 - Streamlit LLM Query Cache Canonicalization and Memory Bounding
**Learning:** In Streamlit applications wrapping LLM endpoints with `@st.cache_data`, users frequently introduce accidental leading/trailing whitespace into inputs. Because Streamlit hashes function input parameters directly for cache keys, unnormalized inputs cause cache misses and trigger expensive, redundant LLM API calls. Canonicalizing inputs within the cached function and bounding cache capacity (`max_entries`) prevents duplicate calls and avoids memory exhaustion.
**Action:** When decorating LLM prompt generators or query functions with `@st.cache_data`, canonicalize query arguments before fetching and set `max_entries` to prevent cache bloat.
