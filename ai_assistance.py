import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance optimization: Cache responses for identical questions using Streamlit's data caching.
# Avoids expensive repeat calls to Ollama LLM, turning ~1-5s inference delays into instant cached retrievals (<1ms).
@st.cache_data
def chef_ai(question):
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': """ You are a chef.
                rules:
                    - Be polite and friendly
                    - Keep answers short and to the point
                    - Suggest recipes and cooking tips
                """
            },
            {
                'role': 'user',
                'content': question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    st.write(chef_ai(question))
