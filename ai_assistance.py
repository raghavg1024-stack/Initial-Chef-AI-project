import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance Optimization:
# 1. `@st.cache_data` caches LLM responses for identical queries, reducing latency from seconds to <1ms.
# 2. Early return check for empty/whitespace input avoids wasting expensive LLM API calls.
@st.cache_data
def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return "Please enter a valid cooking question."

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
