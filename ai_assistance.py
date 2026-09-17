import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Pre-define static system message structure to eliminate redundant dictionary allocation
# on every function call and remove excess whitespace tokens sent to the LLM backend.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': (
        "You are a chef.\n"
        "rules:\n"
        "- Be polite and friendly\n"
        "- Keep answers short and to the point\n"
        "- Suggest recipes and cooking tips"
    )
}

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""
    question_clean = question.strip()
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': question_clean
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    clean_question = question.strip() if question else ""
    if clean_question:
        st.write(chef_ai(clean_question))
    else:
        st.warning("Please enter a cooking question.")
