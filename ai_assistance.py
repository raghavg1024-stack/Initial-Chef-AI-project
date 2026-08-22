import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")


# Performance optimization: Cache responses for identical cooking questions using @st.cache_data
# to avoid expensive, duplicate Ollama LLM inference calls across Streamlit reruns.
@st.cache_data
def chef_ai(question):
    # Performance optimization: Early return for empty or whitespace-only inputs
    # to avoid wasting CPU/GPU compute and network bandwidth on blank queries.
    if not question or not question.strip():
        return "Please ask a cooking question!"

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
