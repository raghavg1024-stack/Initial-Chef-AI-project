import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Reuse module-level constant for system message prompt to avoid dict/string re-allocations.
# 2. Strip whitespace from questions before querying cache so trailing/leading spaces reuse identical cache entries.
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
    if not question or not question.strip():
        return ""
    return _cached_chef_ai(question.strip())

chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    cleaned_question = question.strip() if question else ""
    if cleaned_question:
        st.write(chef_ai(cleaned_question))
    else:
        st.warning("Please enter a cooking question.")
