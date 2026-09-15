import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Module-level constant SYSTEM_PROMPT avoids re-instantiating prompt payload dict and string on every chat request.
# 2. Pre-stripping user input before invoking _cached_chef_ai ensures queries with leading/trailing whitespace
#    share the exact same Streamlit cache entry, preventing redundant, expensive LLM calls.
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
def _cached_chef_ai(cleaned_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            SYSTEM_PROMPT,
            {
                'role': 'user',
                'content': cleaned_question
            }
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    cleaned = question.strip() if question else ""
    if not cleaned:
        return ""
    return _cached_chef_ai(cleaned)

# Forward clear method so existing callers can invalidate cache via chef_ai.clear()
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    cleaned_question = question.strip() if question else ""
    if cleaned_question:
        st.write(chef_ai(cleaned_question))
    else:
        st.warning("Please enter a cooking question.")
