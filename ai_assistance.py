import ollama
import streamlit as st

st.title("Chef AI")

SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data after normalizing whitespace.
# Normalizing input query strings before hashing ensures duplicate queries with
# leading/trailing spaces or newlines hit the cache key and avoid redundant,
# expensive Ollama LLM calls.
@st.cache_data(show_spinner="Asking Chef AI...")
def _cached_chef_ai(question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
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
    return _cached_chef_ai(cleaned_question)


chef_ai.clear = _cached_chef_ai.clear

question = st.text_input("Ask a cooking question...")

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
