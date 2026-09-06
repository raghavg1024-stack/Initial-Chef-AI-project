import ollama
import streamlit as st

st.title("Chef AI")

SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# Cache response results with @st.cache_data so duplicate/identical cooking queries
# do not trigger redundant and expensive calls to the Ollama LLM backend.
# Stripping whitespace from questions ensures whitespace variations share the exact same
# cache key, preventing redundant calls to Ollama.
@st.cache_data(show_spinner="Asking Chef AI...")
def chef_ai(question):
    cleaned_question = question.strip() if question else ""
    if not cleaned_question:
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
                'content': cleaned_question
            }
        ]
    )
    return response['message']['content']

if st.button("Send"):
    cleaned = question.strip() if question else ""
    if cleaned:
        st.write(chef_ai(cleaned))
    else:
        st.warning("Please enter a cooking question.")
