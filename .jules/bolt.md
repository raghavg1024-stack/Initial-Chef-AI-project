# Bolt Journal

## 2026-11-08 - Streamlit LLM Query Normalization and Client Caching
**Learning:** In LLM-backed Streamlit applications, caching functions with raw user text inputs misses duplicate queries due to minor variations in capitalization and whitespace (e.g. "How to boil pasta?" vs "how to boil pasta?"). Furthermore, using raw `@st.cache_data` without `max_entries` or `ttl` causes unbounded memory growth over prolonged server runtimes, while invoking module-level client calls re-evaluates client connection initialization.
**Action:** Decouple user input from cached functions by preprocessing/normalizing strings (lower-casing and normalizing whitespace), manage cache boundaries with `max_entries` and `ttl`, and persist network clients across script reruns with `@st.cache_resource`.
