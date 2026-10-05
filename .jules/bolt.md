# Bolt Journal ⚡

## 2025-05-18 - Streamlit Cache Key Normalization
**Learning:** Streamlit's `@st.cache_data` caches function execution based on raw positional/keyword argument inputs. Passing unnormalized user inputs (e.g. inputs with surrounding whitespace) directly into a cached LLM function causes cache misses for semantically identical inputs, triggering unnecessary, expensive LLM calls.
**Action:** Always normalize/clean query input parameters before hitting `@st.cache_data` cached execution functions.
