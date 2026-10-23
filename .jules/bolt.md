## 2026-10-23 - Streamlit Cache Hit Rate Optimization via Input Normalization

**Learning:** Streamlit's `@st.cache_data` uses the exact argument values passed into the cached function as part of the cache key. In interactive chat/input interfaces, passing raw input string with leading or trailing whitespace causes cache misses for conceptually identical inputs. Pre-cleaning/normalizing input strings prior to invoking `@st.cache_data` decorated functions maximizes cache hits and avoids costly LLM backend invocations. Additionally, extracting static system prompt payloads out of the inner loop into module constants prevents unnecessary dictionary allocations per execution.

**Action:** Always ensure inputs passed into cached Streamlit functions are normalized (e.g. `.strip()`) at the call site or UI interaction point, and keep static prompt data defined as module constants.
