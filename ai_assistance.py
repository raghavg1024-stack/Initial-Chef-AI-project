import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Pre-construct static SYSTEM_MESSAGE dictionary at module level to prevent
#    re-allocation on every function execution and eliminate extraneous indentation whitespace
#    tokens in prompt context, saving LLM context window tokens and HTTP payload bytes.
# 2. Cache response results with @st.cache_data so duplicate/identical cooking queries
#    do not trigger redundant and expensive calls to the Ollama LLM backend.

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
    cleaned_question = question.strip() if question else ""
    if not cleaned_question:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': cleaned_question
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
