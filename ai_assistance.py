import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance optimization:
# Cache responses for identical cooking questions to avoid redundant Ollama LLM calls.
# st.cache_data caches return values based on input arguments.
@st.cache_data
def chef_ai(question):
    # Early return check to prevent sending empty queries to Ollama
    if not question or not question.strip():
        return "Please ask a valid cooking question."

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
