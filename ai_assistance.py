import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Static system message defined as module constant to avoid dict/string re-allocations on every invocation.
# 2. Input queries are stripped to ensure queries with whitespace variations produce identical cache keys in @st.cache_data, avoiding redundant LLM calls.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

@st.cache_data(show_spinner="Asking Chef AI...")
def _cached_chef_ai(question):
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question):
    if not question:
        return ""
    question = question.strip()
    if not question:
        return ""
    return _cached_chef_ai(question)

# Attach clear method for compatibility with tests and Streamlit cache clearing
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    clean_question = question.strip() if question else ""
    if clean_question:
        st.write(chef_ai(clean_question))
    else:
        st.warning("Please enter a cooking question.")
