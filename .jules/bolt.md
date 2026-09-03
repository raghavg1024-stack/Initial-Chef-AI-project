# Bolt's Journal - Critical Learnings

## 2026-03-31 - Streamlit & Ollama Caching Strategy
**Learning:** In Streamlit applications, top-level script re-execution on user interaction triggers expensive LLM calls repeatedly. Wrapping LLM prompt functions with `@st.cache_data` and validating inputs (early return on empty or whitespace strings) eliminates redundant network/inference overhead and improves response times from seconds to sub-millisecond for cached queries.
**Action:** Always decorate deterministic LLM query functions with `@st.cache_data` and perform fast input sanitization before hitting external API endpoints.
