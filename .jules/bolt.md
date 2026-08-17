# Bolt's Journal - Critical Learnings

## 2025-02-17 - Caching LLM calls in Streamlit
**Learning:** In Streamlit apps calling local or remote LLMs (like Ollama), identical prompt inputs re-trigger slow LLM inference on every user interaction unless cached with `@st.cache_data`. Early guard against empty prompts avoids accidental LLM invocations.
**Action:** Always decorate expensive pure AI prompt functions with `@st.cache_data` and guard against empty inputs.
