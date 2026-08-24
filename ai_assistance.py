import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance optimization: Cache Ollama API responses for identical questions
# to prevent expensive LLM calls on repeated queries (reducing latency from seconds to ~0ms).
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    # Early return validation for empty or whitespace-only inputs
    # to avoid making unnecessary external API requests.
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
                'content': question.strip()
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    st.write(chef_ai(question))
