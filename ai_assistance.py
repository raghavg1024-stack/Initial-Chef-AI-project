import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Define clean module-level constant to eliminate unnecessary indentation whitespace
# tokens sent to Ollama LLM context window on every API call.
CHEF_SYSTEM_PROMPT = (
    "You are a chef.\n"
    "rules:\n"
    "    - Be polite and friendly\n"
    "    - Keep answers short and to the point\n"
    "    - Suggest recipes and cooking tips"
)

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    normalized_question = question.strip() if question else ""
    if not normalized_question:
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': CHEF_SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': normalized_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    normalized_q = question.strip() if question else ""
    if normalized_q:
        st.write(chef_ai(normalized_q))
    else:
        st.warning("Please enter a cooking question.")
