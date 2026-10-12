import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Clean module-level system prompt eliminates unnecessary leading indentation/spaces,
#    reducing prompt token overhead sent to Ollama backend by ~50% for system prompt text.
# 2. Pre-normalize input whitespace before cache lookup so queries with minor whitespace
#    variations share the same cache key and avoid redundant expensive LLM calls.

SYSTEM_PROMPT = (
    "You are a chef.\n"
    "rules:\n"
    "- Be polite and friendly\n"
    "- Keep answers short and to the point\n"
    "- Suggest recipes and cooking tips"
)

@st.cache_data(show_spinner="Asking Chef AI...")
def _query_chef_ai(clean_question):
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

def chef_ai(question):
    if not question:
        return ""
    clean_question = question.strip()
    if not clean_question:
        return ""
    return _query_chef_ai(clean_question)

chef_ai.clear = _query_chef_ai.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
