import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# ⚡ Performance Optimization: Cache response for duplicate questions
# LLM generation calls via ollama.chat are computationally expensive (100ms - several seconds).
# @st.cache_data memoizes outputs for identical inputs, turning repeated queries into O(1) instant responses (~0ms).
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