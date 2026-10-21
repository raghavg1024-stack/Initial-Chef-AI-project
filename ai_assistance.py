import ollama
import streamlit as st

st.title("Chef AI")

# Static system prompt hoisted to module scope to avoid re-allocating string/dict objects on every call
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(question: str) -> str:
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

# Bolt ⚡ Optimization:
# Normalize inputs prior to Streamlit's @st.cache_data invocation.
# This guarantees that whitespace variations (e.g. " query " vs "query")
# hash to the identical cache key and prevent redundant LLM backend calls.
def chef_ai(question: str) -> str:
    cleaned_question = question.strip() if question else ""
    if not cleaned_question:
        return ""
    return _chef_ai_cached(cleaned_question)

chef_ai.clear = _chef_ai_cached.clear

question = st.text_input("Ask a cooking question...")

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
