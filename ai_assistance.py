import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Module-level static prompt definition to avoid dict/string allocation overhead per call.
# 2. Input sanitization (stripping) before calling `chef_ai` ensures trailing/leading whitespace
#    variations (e.g., "pasta " vs "pasta") share the same `@st.cache_data` cache key, improving cache hit rates.
SYSTEM_PROMPT = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_response(question: str) -> str:
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

def chef_ai(question: str) -> str:
    cleaned_question = question.strip() if question else ""
    if not cleaned_question:
        return ""
    return _get_chef_response(cleaned_question)

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
