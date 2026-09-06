## 2025-05-18 - Streamlit @st.cache_data Input Whitespace Normalization
**Learning:** `@st.cache_data` generates cache keys based on exact input arguments. Unstripped user inputs from `st.text_input` result in cache misses for identical queries with whitespace variations.
**Action:** Always strip/normalize query strings prior to calling `@st.cache_data` functions in Streamlit applications.
