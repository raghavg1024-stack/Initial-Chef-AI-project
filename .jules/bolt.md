# Bolt's Journal - Critical Performance Learnings

## 2026-08-25 - Streamlit @st.cache_data for LLM Inference & Early Returns

**Learning:** Calling local/remote LLM APIs (e.g. Ollama `mistral`) without caching leads to high execution times (often multi-second delays per call) and unnecessary resource consumption for duplicate or empty user inputs. Using Streamlit's `@st.cache_data` caches identical user queries, reducing duplicate response time to ~0ms. Additionally, performing early validation on empty or whitespace-only inputs avoids calling the LLM entirely.
**Action:** Wrap LLM response generator functions with `@st.cache_data` and add early return checks for empty string queries in Streamlit applications.
