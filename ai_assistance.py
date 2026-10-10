import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data on a normalized/stripped query string
# so whitespace variations (e.g., " How to boil pasta? ") hit the exact same cache entry
# and avoid expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_response(normalized_question: str) -> str:
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
    return _get_chef_response(question.strip())


# Expose clear method on chef_ai for cache invalidation in tests or admin functions
chef_ai.clear = _get_chef_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
