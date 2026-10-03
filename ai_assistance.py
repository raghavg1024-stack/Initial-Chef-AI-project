import ollama
import streamlit as st

st.title("Chef AI")

# Bolt ⚡ Optimization:
# Pre-allocate system message dictionary as a module-level constant to eliminate
# object allocation overhead per call and remove redundant leading indentation tokens.
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': (
        " You are a chef.\n"
        " rules:\n"
        "     - Be polite and friendly\n"
        "     - Keep answers short and to the point\n"
        "     - Suggest recipes and cooking tips"
    )
}

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
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

# Bolt ⚡ Optimization:
# Batch input changes using st.form to prevent Streamlit from re-running the script
# on every keystroke/blur event before the user submits their question.
with st.form(key="chef_form"):
    question = st.text_input("Ask a cooking question...")
    submitted = st.form_submit_button("Send")

if submitted:
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
