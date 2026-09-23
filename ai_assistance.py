import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

# Bolt ⚡ Optimization:
# Normalize (strip) string inputs prior to cache key lookup so queries with whitespace variations
# (e.g. leading/trailing spaces) hit the @st.cache_data cache instead of making redundant,
# expensive LLM backend requests to Ollama.
@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_ai_response(clean_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': clean_question
            }
        ]
    )
    return response['message']['content']


def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    return _get_chef_ai_response(question.strip())


# Preserve .clear() interface on chef_ai for Streamlit cache invalidation and test isolation
chef_ai.clear = _get_chef_ai_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
