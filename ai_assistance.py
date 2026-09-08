import ollama
import streamlit as st

# Bolt ⚡ Optimization:
# 1. Static SYSTEM_PROMPT constant prevents recreating prompt dictionary and string objects on every call,
#    and removes redundant leading indentation whitespace to reduce prompt token count sent to Ollama LLM.
SYSTEM_PROMPT = """You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips"""

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    if not question or not question.strip():
        return ""
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': question.strip()
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    cleaned_question = question.strip() if question else ""
    if cleaned_question:
        # Bolt ⚡ Optimization:
        # Pass pre-stripped question to chef_ai so whitespace variations (e.g. trailing spaces)
        # share the exact same cache key in @st.cache_data, avoiding redundant LLM backend calls.
        st.write(chef_ai(cleaned_question))
    else:
        st.warning("Please enter a cooking question.")
