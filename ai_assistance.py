import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Performance Optimization: Define static system prompt outside the function to avoid redundant dict creation.
SYSTEM_PROMPT = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

# Performance Optimization: `@st.cache_data` caches LLM responses for duplicate questions.
# This eliminates redundant network/Ollama inference calls on repeated or identical queries.
@st.cache_data
def chef_ai(question):
    # Performance Optimization: Early return for empty or whitespace-only questions to skip expensive LLM calls.
    if not question or not question.strip():
        return "Please enter a valid cooking question."

    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    st.write(chef_ai(question))
