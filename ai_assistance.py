import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data and normalize user input (lowercasing and collapsing whitespace)
# so variations in casing/whitespace (e.g. "How to boil pasta?", "HOW TO BOIL PASTA?  ") hit the cache
# without making redundant and expensive LLM calls to Ollama.
@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(normalized_question: str) -> str:
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
    # Normalize question by stripping leading/trailing whitespace, converting to lower case, and normalizing internal spaces
    normalized_question = " ".join(question.strip().lower().split())
    if not normalized_question:
        return ""
    return _chef_ai_cached(normalized_question)


# Expose clear method on chef_ai for easy cache clearing in tests/UI
chef_ai.clear = _chef_ai_cached.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
