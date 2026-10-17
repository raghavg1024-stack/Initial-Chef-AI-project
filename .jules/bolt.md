## 2026-10-17 - Streamlit Cache Key Normalization
**Learning:** Normalizing user inputs (e.g., stripping whitespace) prior to passing arguments into `@st.cache_data` functions dramatically increases cache hit rates when users input variations with leading/trailing spaces, saving costly LLM inference calls.
**Action:** Always sanitize and normalize input parameters before invoking `@st.cache_data` decorated helpers.
