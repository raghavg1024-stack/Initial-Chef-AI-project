import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

SYSTEM_PROMPT = (
    "You are a chef.\n"
    "rules:\n"
    "- Be polite and friendly\n"
    "- Keep answers short and to the point\n"
    "- Suggest recipes and cooking tips"
)


# Bolt ⚡ Optimization:
# 1. Normalize query string BEFORE Streamlit @st.cache_data cache lookup so queries with leading/trailing
#    whitespace (e.g. " pasta " vs "pasta") share the exact same cache entry, preventing redundant LLM calls.
# 2. Clean system prompt tokens (removing unnecessary indentation spaces) to minimize LLM context prefill latency.
@st.cache_data(show_spinner="Asking Chef AI...")
def _get_chef_response(clean_question: str) -> str:
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
    if not question:
        return ""
    clean_question = question.strip()
    if not clean_question:
        return ""
    return _get_chef_response(clean_question)


# Preserve .clear() on chef_ai for Streamlit cache clearing in tests and UI
chef_ai.clear = _get_chef_response.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
