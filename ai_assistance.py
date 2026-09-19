import ollama
import streamlit as st

st.title("Chef AI")

# Bolt ⚡ Optimization:
# Define system prompt at module level to avoid re-allocating dictionary and string objects
# on every function invocation.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': """ You are a chef.
                rules:
                    - Be polite and friendly
                    - Keep answers short and to the point
                    - Suggest recipes and cooking tips
                """
}

# Bolt ⚡ Optimization:
# 1. @st.cache_data caches responses based on exact parameter values. Passing normalized (stripped)
#    strings ensures that queries differing only by leading/trailing whitespace hit the cache,
#    saving expensive LLM backend calls to Ollama.
# 2. Returning early for empty/whitespace inputs in chef_ai() avoids unnecessary cache lookup overhead
#    and spinner rendering for blank queries.
@st.cache_data(show_spinner="Asking Chef AI...")
def _cached_chef_ai(clean_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': clean_question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    return _cached_chef_ai(question.strip())

# Forward clear() to underlying cache function for cache management and testing
chef_ai.clear = _cached_chef_ai.clear

question = st.text_input("Ask a cooking question...")

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
