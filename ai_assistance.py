import ollama
import streamlit as st

st.title("Chef AI")

# Bolt ⚡ Optimization:
# Extract system prompt and message to module-level constants to avoid redundant string creation,
# multi-line whitespace formatting, and dictionary allocation on every function call.
SYSTEM_PROMPT = (
    "You are a chef.\n"
    "rules:\n"
    "    - Be polite and friendly\n"
    "    - Keep answers short and to the point\n"
    "    - Suggest recipes and cooking tips"
)

SYSTEM_MESSAGE = {
    'role': 'system',
    'content': SYSTEM_PROMPT
}

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
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
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
