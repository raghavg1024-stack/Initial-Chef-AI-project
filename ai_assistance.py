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
# 1. Normalize input (strip whitespace) before passing to cached function so queries differing only in leading/trailing whitespace hit the cache.
# 2. Re-use static system prompt to avoid dict allocation overhead on repeated calls.
@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(clean_question: str) -> str:
    response = ollama.chat(
        model='mistral',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': clean_question}
        ]
    )
    return response['message']['content']

def chef_ai(question: str) -> str:
    if not question or not question.strip():
        return ""
    return _chef_ai_cached(question.strip())

# Expose clear method on chef_ai wrapper for backwards compatibility with st.cache_data clear interface
chef_ai.clear = _chef_ai_cached.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
