import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Pre-allocate system prompt and remove leading/trailing multiline indentation to reduce prompt tokens & HTTP payload size.
# 2. Cache response results with @st.cache_data so duplicate queries avoid expensive LLM inference.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': 'You are a chef.\nrules:\n- Be polite and friendly\n- Keep answers short and to the point\n- Suggest recipes and cooking tips'
}

@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""

    clean_question = question.strip()
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

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
