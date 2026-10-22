import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Define SYSTEM_PROMPT at module level to avoid re-allocating strings and dictionary structures on every call.
# 2. Extract cached LLM call function _chef_ai_cached and normalize input in chef_ai() prior to cache lookup.
#    This guarantees that queries with whitespace variations (e.g. "  How to bake cookies?  " vs "How to bake cookies?")
#    share the exact same cache key in Streamlit @st.cache_data, completely eliminating redundant LLM calls.
SYSTEM_PROMPT = """ You are a chef.
rules:
    - Be polite and friendly
    - Keep answers short and to the point
    - Suggest recipes and cooking tips
"""

@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(cleaned_question):
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

def chef_ai(question):
    if not question:
        return ""
    cleaned_question = question.strip() if isinstance(question, str) else question
    if not cleaned_question:
        return ""
    return _chef_ai_cached(cleaned_question)

# Preserve .clear() method on chef_ai for test isolation and cache resetting
chef_ai.clear = _chef_ai_cached.clear

if st.button("Send"):
    if question and question.strip():
        st.write(chef_ai(question))
    else:
        st.warning("Please enter a cooking question.")
