import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Normalize input whitespace BEFORE calling the cached function `@st.cache_data`.
# Previously `question.strip()` was called inside the cached function, so identical queries with different
# whitespace (e.g., "How to boil pasta?" vs "  How to boil pasta?  ") produced distinct cache keys
# and resulted in redundant, expensive LLM calls to Ollama.

@st.cache_data(show_spinner="Asking Chef AI...")
def _cached_chef_ai(normalized_question: str) -> str:
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
                'content': normalized_question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    return _cached_chef_ai(question.strip())

chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
