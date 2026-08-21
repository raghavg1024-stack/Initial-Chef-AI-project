import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance optimization: @st.cache_data caches LLM query results to avoid expensive
# model re-inference when asking duplicate or identical questions (reducing latency from seconds to <1ms).
@st.cache_data
def chef_ai(question):
    # Guard against empty/whitespace inputs to skip unnecessary LLM API calls entirely.
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
                'content': question.strip()
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    st.write(chef_ai(question))
