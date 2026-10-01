import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Normalize question (strip leading/trailing whitespace and lowercasing if applicable,
# or strip whitespace) prior to caching so queries like "  how to boil pasta  " and
# "how to boil pasta" share the exact same cached result, avoiding redundant expensive LLM calls.
@st.cache_data(show_spinner="Asking Chef AI...")
def _cached_chef_ai(normalized_question):
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

def chef_ai(question):
    if not question or not question.strip():
        return ""
    return _cached_chef_ai(question.strip())

# Expose cache clear helper on chef_ai for easy cache invalidation during testing/management
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
