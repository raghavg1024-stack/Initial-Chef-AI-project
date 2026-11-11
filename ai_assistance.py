import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

SYSTEM_PROMPT = """ You are a chef.
                rules:
                    - Be polite and friendly
                    - Keep answers short and to the point
                    - Suggest recipes and cooking tips
                """

# Bolt ⚡ Optimization:
# 1. Cache LLM response results with @st.cache_data to avoid duplicate expensive model inferences.
# 2. Bound cache size with max_entries=500 to prevent unbounded memory growth.
# 3. Separate raw input handling from the cached function: return early for empty/whitespace queries
#    without cache hashing overhead or cache pollution, and normalize (strip) query strings so
#    equivalent queries with varying whitespace hit the cache rather than invoking redundant LLM calls.
@st.cache_data(show_spinner="Asking Chef AI...", max_entries=500)
def _cached_chef_ai(clean_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT,
            },
            {
                'role': 'user',
                'content': clean_question,
            },
        ],
    )
    return response['message']['content']


def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    return _cached_chef_ai(question.strip())


# Maintain compatibility for cache management (e.g. chef_ai.clear())
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    cleaned_input = question.strip() if question else ""
    if cleaned_input:
        st.write(chef_ai(cleaned_input))
    else:
        st.warning("Please enter a cooking question.")
