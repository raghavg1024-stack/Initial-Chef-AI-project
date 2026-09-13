import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Normalizing user query input (lowercasing and trimming whitespace) before passing it
# to the cached function increases cache hit rates significantly.
# Variations like "How to boil pasta?" and "how to boil pasta?  " will hit the exact
# same cache key, avoiding expensive roundtrips to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_response(query: str) -> str:
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
                'content': query
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    normalized_question = question.strip().lower()
    return _get_chef_response(normalized_question)

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
