import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance Optimization: Cache LLM responses with st.cache_data to avoid costly,
# repeated calls to ollama.chat for identical queries. Saves ~1-5s per duplicate prompt.
@st.cache_data
def chef_ai(question):
    # Guard against empty/whitespace inputs to skip unnecessary API requests.
    if not question or not question.strip():
        return "Please ask a cooking question."

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
