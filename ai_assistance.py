import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Pre-define static system prompt outside the function so dictionaries and multiline
#    strings are not re-allocated on every inference call.
# 2. Normalize input question (strip whitespace) before querying the cache so semantically
#    identical queries like " How to boil pasta? " and "How to boil pasta?" reuse the same
#    cache entry rather than triggering redundant, seconds-long LLM calls.
_CHEF_SYSTEM_PROMPT = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

@st.cache_data(show_spinner="Asking Chef AI...")
def _cached_chef_ai(clean_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            _CHEF_SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': clean_question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question:
        return ""
    clean_question = question.strip()
    if not clean_question:
        return ""
    return _cached_chef_ai(clean_question)

# Expose cache management methods for testing and cache control
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
