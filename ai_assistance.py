import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Pre-construct static SYSTEM_MESSAGE dictionary at module level to avoid re-allocating
#    the dictionary and string on each request, and normalize indentation whitespace to save
#    LLM prompt tokens and HTTP payload bytes.
# 2. Normalize and strip user input before passing to @st.cache_data so that queries differing
#    only by surrounding whitespace (e.g. "pasta" vs "  pasta  ") hit the cache instead of
#    triggering redundant, expensive LLM calls to Ollama.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': (
        "You are a chef.\n"
        "rules:\n"
        "    - Be polite and friendly\n"
        "    - Keep answers short and to the point\n"
        "    - Suggest recipes and cooking tips"
    )
}

@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': question.strip()
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    cleaned_question = question.strip() if question else ""
    if cleaned_question:
        st.write(chef_ai(cleaned_question))
    else:
        st.warning("Please enter a cooking question.")
