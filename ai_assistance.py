import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Reusable system prompt message dict at module level
SYSTEM_MESSAGE = {
    'role': 'system',
    'content': """ You are a chef.
    rules:
        - Be polite and friendly
        - Keep answers short and to the point
        - Suggest recipes and cooking tips
    """
}

# Bolt ⚡ Optimization:
# Normalize string argument using `hash_funcs` so user query variations
# with leading/trailing or multiple internal spaces map to the same cache key in Streamlit.
# This prevents redundant, expensive LLM calls to Ollama.
@st.cache_data(
    show_spinner="Asking Chef AI...",
    hash_funcs={str: lambda s: " ".join(s.strip().split()).encode('utf-8')}
)
def chef_ai(question):
    if not question or not question.strip():
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_MESSAGE,
            {
                'role': 'user',
                'content': question.strip()
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
