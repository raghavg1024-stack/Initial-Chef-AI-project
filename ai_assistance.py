import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Module-level constant system prompt to avoid recreating strings on each call
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

@st.cache_data(show_spinner="Asking Chef AI...")
def _cached_chef_ai(normalized_question):
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': normalized_question
            }
        ]
    )
    return response['message']['content']

# Bolt ⚡ Optimization:
# Normalize whitespace before looking up Streamlit cache so "How to boil pasta?" and "  How to boil pasta?  "
# share the exact same cache entry, preventing redundant LLM backend calls.
def chef_ai(question):
    if not question or not question.strip():
        return ""
    return _cached_chef_ai(question.strip())

# Forward clear() to underlying cached function for backward compatibility and test isolation
chef_ai.clear = _cached_chef_ai.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
