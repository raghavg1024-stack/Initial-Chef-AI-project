import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance Optimization:
# 1. `@st.cache_data` caches LLM responses for duplicate questions across Streamlit rerun cycles,
#    reducing response times for identical queries from seconds (LLM inference) to near 0ms.
# 2. Early return check skips expensive LLM API calls entirely when the query is empty or only whitespace.
@st.cache_data(show_spinner="Chef is thinking...")
def chef_ai(question):
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
