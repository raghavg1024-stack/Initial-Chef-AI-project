import ollama
import streamlit as st

st.title("Chef AI")

question = st.text_input("Ask a cooking question...")

# Bolt ⚡ Optimization:
# 1. Hoist pre-formatted SYSTEM_PROMPT to module constant to avoid dictionary/string allocation overhead
#    on every function execution and eliminate redundant whitespace tokens sent over wire.
# 2. Normalize question input so @st.cache_data hashes normalized strings, ensuring whitespace variations
#    (e.g., "How to bake?" vs "How to bake? ") hit the exact same cache entry instead of triggering redundant LLM calls.

SYSTEM_PROMPT = (
    "You are a chef.\n"
    "rules:\n"
    "    - Be polite and friendly\n"
    "    - Keep answers short and to the point\n"
    "    - Suggest recipes and cooking tips"
)

@st.cache_data(show_spinner="Asking Chef AI...")
def _chef_ai_cached(question):
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

def chef_ai(question):
    question = question.strip() if question else ""
    if not question:
        return ""
    return _chef_ai_cached(question)

# Expose clear() on chef_ai for test/cache management compatibility
chef_ai.clear = _chef_ai_cached.clear

if st.button("Send"):
    cleaned_question = question.strip() if question else ""
    if cleaned_question:
        st.write(chef_ai(cleaned_question))
    else:
        st.warning("Please enter a cooking question.")
