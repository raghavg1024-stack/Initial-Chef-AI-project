import ollama
import streamlit as st

st.title("Chef AI")

SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Cache expensive Ollama LLM response to avoid redundant inference calls for identical questions
@st.cache_data
def chef_ai(question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': question
            }
        ]
    )
    return response['message']['content']

question = st.text_input("Ask a cooking question...")

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question.strip()))
    else:
        st.warning("Please enter a cooking question.")
