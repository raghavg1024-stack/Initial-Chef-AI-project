import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Hoist constant system message prompt to module scope to avoid dict allocation on each request.
# 2. Cache response results with @st.cache_data so duplicate/identical cooking queries
#    do not trigger redundant and expensive calls to the Ollama LLM backend.
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
def chef_ai(question):
    normalized_question = question.strip() if question else ""
    if not normalized_question:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': normalized_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    # Bolt ⚡ Optimization: Normalize question whitespace before calling chef_ai
    # so queries with leading/trailing spaces share identical cache keys with clean queries.
    cleaned_question = question.strip() if question else ""
    if cleaned_question:
        st.write(chef_ai(cleaned_question))
    else:
        st.warning("Please enter a cooking question.")
