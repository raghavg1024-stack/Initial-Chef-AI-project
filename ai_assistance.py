import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""
    # Bolt ⚡ Optimization: Clean multiline whitespace from system prompt
    # to minimize token overhead and request payload size sent to Ollama LLM.
    system_prompt = (
        "You are a chef.\n"
        "rules:\n"
        "- Be polite and friendly\n"
        "- Keep answers short and to the point\n"
        "- Suggest recipes and cooking tips"
    )

    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': question.strip()
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
